"""Exercise the launcher and exam service together without touching real answers."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, quote, urlsplit


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reset_service
import start_services


@contextmanager
def serve(handler):
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class JupyterStatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        authorized = self.path == "/api/status" and self.headers.get("Authorization") == "token test-token"
        payload = b'{"connections":0}' if authorized else b'{}'
        self.send_response(200 if authorized else 403)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


class ExamStartupIntegrationTests(unittest.TestCase):
    def test_launcher_recognizes_exam_service_without_reading_answers(self):
        # No ExamStore is attached: health checks must not create or read a paper.
        with serve(reset_service.ResetHandler) as server, patch.object(start_services, "RESET_PORT", server.server_port):
            self.assertTrue(start_services.reset_ready())
            with patch.object(start_services, "start_background") as spawn:
                start_services.ensure_reset(Path("unused-logs"))
                spawn.assert_not_called()

    def check_jupyter_location(self, *, legacy=False, foreign_root=False):
        with tempfile.TemporaryDirectory() as directory, serve(JupyterStatusHandler) as server:
            root = Path(directory).resolve()
            relative = "人工智能训练师三级上网素材/1.1.1/1.1.1.ipynb"
            notebook = root / relative
            notebook.parent.mkdir(parents=True)
            notebook.write_text("{}", encoding="utf-8")
            default_runtime = root / "default-runtime"
            runtime = root / ".venv/service-runtime" if legacy else default_runtime
            runtime.mkdir(parents=True)
            info = {
                "pid": os.getpid(), "port": server.server_port,
                "root_dir": str(root / "another-project" if foreign_root else root),
                "base_url": "/", "token": "test-token",
            }
            (runtime / f"jpserver-{os.getpid()}.json").write_text(json.dumps(info), encoding="utf-8")
            with (
                patch.object(reset_service, "ROOT", root),
                patch.object(start_services, "ROOT", root),
                patch.object(start_services, "JUPYTER_PORT", server.server_port),
                patch.object(start_services, "JUPYTER_URL", f"http://localhost:{server.server_port}"),
                patch("jupyter_server.serverapp.jupyter_runtime_dir", return_value=str(default_runtime)),
            ):
                if foreign_root:
                    with self.assertRaises(RuntimeError):
                        reset_service.jupyter_location(relative)
                else:
                    location = urlsplit(reset_service.jupyter_location(relative))
                    self.assertEqual(location.netloc, f"localhost:{server.server_port}")
                    self.assertEqual(location.path, "/lab/tree/" + quote(relative, safe="/"))
                    self.assertEqual(parse_qs(location.query), {"token": ["test-token"]})

    def test_exam_opens_jupyter_from_default_runtime(self):
        self.check_jupyter_location()

    def test_exam_still_opens_jupyter_from_legacy_runtime(self):
        self.check_jupyter_location(legacy=True)

    def test_exam_rejects_jupyter_for_another_project(self):
        self.check_jupyter_location(foreign_root=True)


if __name__ == "__main__":
    unittest.main()
