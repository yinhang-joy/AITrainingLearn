"""验证抽题规则、原始素材恢复、作答隔离及 HTTP 接口。测试只操作临时题库。"""
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from exam_manager import ConflictError, ExamStore, GROUPS, INITIAL_UNITS, MATERIALS, draw_units, validate_units
import reset_service


class ExamTests(unittest.TestCase):
    def setUp(self):
        # 临时目录留在忽略的 .venv 中，便于失败时检查；不接触真实作答目录。
        base = Path(__file__).resolve().parent.parent / ".venv" / "exam-tests"
        base.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="case-", dir=base)).resolve()
        assert self.root.is_relative_to(base.resolve())
        self.git("init", "-q")
        for group in GROUPS:
            for number in range(1, 6):
                unit = f"{group}.{number}"
                folder = self.root / MATERIALS / unit
                folder.mkdir(parents=True)
                (folder / f"{unit}.html").write_text(f"<title>{unit} 测试题目</title>", encoding="utf-8")
                (folder / f"{unit}.docx").write_bytes(b"blank document")
                (folder / "data.csv").write_text("value\n1\n", encoding="utf-8")
                (folder / "imgs").mkdir()
                (folder / "imgs" / "input.jpg").write_bytes(b"image fixture")
                nb = {"nbformat":4,"nbformat_minor":5,"metadata":{},"cells":[
                    {"cell_type":"markdown","metadata":{},"source":["题目 <!-- auto:enriched -->"]}]}
                if group in ("1.1", "2.1", "2.2", "3.2"):
                    nb["cells"].append({"cell_type":"code","metadata":{},"source":["answer = __________"],"outputs":[],"execution_count":None})
                (folder / f"{unit}.ipynb").write_text(json.dumps(nb), encoding="utf-8")
        self.git("add", ".")
        self.git("-c", "user.name=Exam tests", "-c", "user.email=exam-test@example.invalid", "commit", "-qm", "blank fixtures")
        self.store = ExamStore(self.root, "HEAD")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE)

    def test_rule_distribution_and_rejection(self):
        rng = random.Random(57)
        seen = set()
        previous = None
        for _ in range(1000):
            units = draw_units(previous, rng)
            self.assertEqual(validate_units(units), units)
            self.assertNotEqual(units, previous)
            self.assertEqual(sum(GROUPS[u.rsplit('.',1)[0]][1] for u in units), 120)
            self.assertEqual(sum(GROUPS[u.rsplit('.',1)[0]][2] for u in units), 100)
            seen.update(units)
            previous = units
        self.assertEqual(len(seen), 40)
        for invalid in [INITIAL_UNITS[:5], ["../../bad"]*6, [None]*6,
                        ["1.1.1","1.2.1","2.1.1","2.2.1","3.1.1","4.1.1"]]:
            with self.assertRaises(ValueError):
                validate_units(invalid)

    def test_initial_copy_is_pristine_and_persistent(self):
        source = self.root / MATERIALS / "1.1.1" / "1.1.1.ipynb"
        source.write_text('{"user":"already answered"}', encoding="utf-8")
        paper = self.store.current()
        self.assertEqual([q["unit"] for q in paper["questions"]], INITIAL_UNITS)
        self.assertEqual((paper["minutes"], paper["points"]), (120, 100))
        self.assertEqual(ExamStore(self.root, "HEAD").current()["id"], paper["id"])
        for q in paper["questions"]:
            folder = self.root / q["folder"]
            self.assertTrue((folder / "imgs" / "input.jpg").is_file())
            nb = json.loads((folder / f"{q['unit']}.ipynb").read_text(encoding="utf-8"))
            for cell in nb["cells"]:
                if cell["cell_type"] == "code":
                    self.assertIn("__________", ''.join(cell["source"]))
                    self.assertEqual(cell["outputs"], [])
                    self.assertIsNone(cell["execution_count"])
        self.assertIn("already answered", source.read_text(encoding="utf-8"))

    def test_reset_preserves_answers_and_stale_tabs_cannot_overwrite(self):
        paper = self.store.current()
        old = self.root / paper["questions"][0]["folder"]
        answer = old / "1.1.1.ipynb"
        answer.write_text("saved answer", encoding="utf-8")
        (old / "result.txt").write_text("result", encoding="utf-8")
        paper2 = self.store.reset(paper["id"], 1, "1.1.1")
        fresh = self.root / paper2["questions"][0]["folder"]
        self.assertNotEqual(old, fresh)
        self.assertEqual(answer.read_text(encoding="utf-8"), "saved answer")
        self.assertFalse((fresh / "result.txt").exists())
        self.assertEqual(paper2["questions"][1]["folder"], paper["questions"][1]["folder"])
        answer.write_text("late autosave", encoding="utf-8")
        self.assertNotIn("late autosave", (fresh / "1.1.1.ipynb").read_text(encoding="utf-8"))
        with self.assertRaises(ConflictError):
            self.store.reset(paper["id"], 1)
        with self.assertRaises(ValueError):
            self.store.reset(paper["id"], 2, "../../requirements.txt")
        paper3 = self.store.reset(paper["id"], 2)
        self.assertTrue(all(a["folder"] != b["folder"] for a,b in zip(paper2["questions"],paper3["questions"])))
        for q in paper3["questions"]:
            self.assertEqual((self.root/q["folder"]/f"{q['unit']}.docx").read_bytes(), b"blank document")
        new = self.store.create(expected_current=paper3["id"])
        self.assertNotEqual(new["id"], paper3["id"])
        self.assertNotEqual([q["unit"] for q in new["questions"]], INITIAL_UNITS)
        self.assertEqual(len(self.store.history()), 2)
        self.assertEqual(self.store.get(paper3["id"])["version"], 3)
        with self.assertRaises(ConflictError):
            self.store.create(expected_current=paper3["id"])

    def test_http_and_legacy_reset(self):
        old_root = reset_service.ROOT
        reset_service.ROOT = self.root
        server = reset_service.ThreadingHTTPServer(("127.0.0.1",0), reset_service.ResetHandler)
        server.exam_store = self.store
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        def request(path, body=None, **headers):
            payload = None if body is None else json.dumps(body).encode()
            if body is not None:
                headers["Content-Type"] = "application/json"
            with urlopen(Request(base+path,data=payload,headers=headers),timeout=10) as response:
                return json.load(response)
        try:
            paper = request("/api/exam/current")
            with self.assertRaises(HTTPError) as error:
                request("/api/exam/reset", {"id":paper["id"],"version":0})
            self.assertEqual(error.exception.code,409)
            with self.assertRaises(HTTPError) as error:
                request("/api/exam/draw", {}, Origin="https://example.com")
            self.assertEqual(error.exception.code,403)
            with self.assertRaises(HTTPError) as error:
                request("/reset", {"unit":"../../README"})
            self.assertEqual(error.exception.code,400)
            new = request("/api/exam/draw", {"current_id":paper["id"]})
            self.assertEqual(len(new["questions"]),6)
            self.assertEqual(len(request("/api/exam/history")),2)
            source = self.root/MATERIALS/"1.1.1"/"1.1.1.ipynb"
            source.write_text("old answer",encoding="utf-8")
            self.assertTrue(request("/reset",{"unit":"1.1.1"})["success"])
            self.assertIn("__________",source.read_text(encoding="utf-8"))
            self.assertEqual(len(list((self.root/".venv/reset-backups").glob("*.zip"))),1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            reset_service.ROOT = old_root


if __name__ == "__main__":
    unittest.main(verbosity=2)
