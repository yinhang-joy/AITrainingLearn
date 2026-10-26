#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地练习重置及模拟考试服务：http://localhost:8765/考试目录/"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, quote, urlsplit

from exam_manager import ConflictError, ExamStore, MATERIALS
import start_services

ROOT = Path(__file__).resolve().parent.parent


def jupyter_location(relative):
    path = (ROOT / relative).resolve()
    if not any(path.is_relative_to((ROOT / p).resolve()) for p in (MATERIALS, "考试目录/试卷")):
        raise ValueError("只能打开题库或考试作答目录")
    if not path.exists():
        raise FileNotFoundError("作答文件不存在")
    info = start_services.running_jupyter()
    if info:
        token = info.get("token", "")
        if start_services.jupyter_ready(token):
            return start_services.JUPYTER_URL + "/lab/tree/" + quote(path.relative_to(ROOT).as_posix(), safe="/") + "?token=" + quote(token, safe="")
    raise RuntimeError("Jupyter 尚未启动，请先启动本项目的 Jupyter 服务（8891 端口）")


class ResetHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    @property
    def store(self):
        return self.server.exam_store

    def _allow_origin(self):
        origin = self.headers.get("Origin")
        if not origin or origin == "null":
            return True
        return bool(re.fullmatch(r"http://(?:localhost|127\.0\.0\.1):(?:8000|8765)", origin))

    def end_headers(self):
        origin = self.headers.get("Origin")
        if origin and self._allow_origin():
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, error):
        status = 409 if isinstance(error, ConflictError) else 404 if isinstance(error, FileNotFoundError) else 400 if isinstance(error, (ValueError, TypeError)) else 500
        self._json({"success": False, "error": str(error)}, status)

    def do_GET(self):
        route = urlsplit(self.path)
        try:
            if route.path == "/api/health":
                return self._json({"service": "practice-and-exams", "version": 1})
            if route.path == "/api/exam/current":
                return self._json(self.store.current())
            if route.path == "/api/exam/history":
                return self._json(self.store.history())
            if route.path == "/api/exam/paper":
                return self._json(self.store.get(parse_qs(route.query).get("id", [""])[0]))
            if route.path == "/jupyter":
                location = jupyter_location(parse_qs(route.query).get("path", [""])[0])
                self.send_response(302)
                self.send_header("Location", location)
                self.end_headers()
                return
            if route.path == "/":
                self.send_response(302)
                self.send_header("Location", "/" + quote("考试目录") + "/")
                self.end_headers()
                return
            if route.path.startswith("/api/"):
                return self._json({"success": False, "error": "接口不存在"}, 404)
            super().do_GET()
        except Exception as error:
            self._error(error)

    def do_POST(self):
        if not self._allow_origin():
            return self._json({"success": False, "error": "只允许本地导航页调用"}, 403)
        try:
            if self.headers.get_content_type() != "application/json":
                raise ValueError("请求必须使用 JSON 格式")
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("请求大小无效")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("请求格式无效")
            route = urlsplit(self.path).path
            if route == "/reset":
                return self._json(self.store.reset_practice(body.get("unit")))
            if route == "/api/exam/draw":
                return self._json(self.store.create(expected_current=body.get("current_id")))
            if route == "/api/exam/reset":
                return self._json(self.store.reset(body.get("id"), body.get("version"), body.get("unit")))
            return self._json({"success": False, "error": "接口不存在"}, 404)
        except Exception as error:
            self._error(error)

    def do_OPTIONS(self):
        if not self._allow_origin():
            return self._json({"error": "不允许此来源"}, 403)
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8765), ResetHandler)
    server.exam_store = ExamStore(ROOT)
    server.exam_store.current()
    print("考试入口：http://localhost:8765/考试目录/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
