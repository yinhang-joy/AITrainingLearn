"""按考核规则抽题，维护互相独立的试卷和作答版本。"""
from datetime import datetime, timedelta, timezone
import html
import json
from pathlib import Path, PurePosixPath
import random
import re
import shutil
import subprocess
import tarfile
import threading
from urllib.parse import quote
import uuid
import zipfile

MATERIALS = "人工智能训练师三级上网素材"
BASELINE = "40a287a2"  # 首次合并任务要求的提交，代码尚未作答。
INITIAL_UNITS = ["1.1.1", "2.1.5", "2.2.5", "3.1.1", "3.2.5", "4.1.2"]
GROUPS = {
    "1.1": ("业务流程设计", 30, 25), "1.2": ("业务模块效果优化", 30, 25),
    "2.1": ("数据处理规范制定", 20, 15), "2.2": ("算法测试", 20, 20),
    "3.1": ("智能系统监控和优化", 20, 15), "3.2": ("人机交互流程设计", 20, 20),
    "4.1": ("培训", 10, 5), "4.2": ("指导", 10, 5),
}


class ConflictError(ValueError):
    pass


def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="microseconds")


def validate_units(units):
    if not isinstance(units, list) or len(units) != 6:
        raise ValueError("每套试卷必须包含 6 道题")
    if any(not isinstance(u, str) or not re.fullmatch(r"[1-4]\.[12]\.[1-5]", u) for u in units):
        raise ValueError("题号无效")
    groups = [u.rsplit(".", 1)[0] for u in units]
    if (len(set(units)) != 6 or sum(g in ("1.1", "1.2") for g in groups) != 1
            or sum(g in ("4.1", "4.2") for g in groups) != 1
            or any(groups.count(g) != 1 for g in ("2.1", "2.2", "3.1", "3.2"))):
        raise ValueError("题目组合不符合考核规则")
    return sorted(units)


def draw_units(previous=None, rng=None):
    rng = rng or random.SystemRandom()
    for _ in range(100):
        groups = [rng.choice(("1.1", "1.2")), "2.1", "2.2", "3.1", "3.2", rng.choice(("4.1", "4.2"))]
        units = [f"{g}.{rng.randint(1, 5)}" for g in groups]
        if units != previous:
            return validate_units(units)
    raise ValueError("抽题未生成新的组合，请重试")


class ExamStore:
    def __init__(self, root, baseline=BASELINE):
        self.root = Path(root).resolve()
        self.directory = self.root / "考试目录"
        self.papers = self.directory / "试卷"
        self.current_file = self.directory / "current.json"
        self.baseline = self._git("rev-parse", "--verify", baseline).decode().strip()
        paths = self._git("ls-tree", "-r", "--name-only", "-z", self.baseline, "--", MATERIALS)
        self.source_files = paths.decode("utf-8").strip("\0").split("\0")
        self.lock = threading.RLock()

    def _git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE)

    @staticmethod
    def _save_json(path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(path)

    def _paper_file(self, paper_id):
        if not isinstance(paper_id, str) or not re.fullmatch(r"\d{8}-\d{6}-[a-f0-9]{8}", paper_id):
            raise ValueError("试卷编号无效")
        path = self.papers / paper_id / "paper.json"
        if not path.resolve().is_relative_to(self.papers.resolve()):
            raise ValueError("试卷路径无效")
        return path

    def _read(self, paper_id):
        path = self._paper_file(paper_id)
        if not path.is_file():
            raise FileNotFoundError("试卷不存在")
        return json.loads(path.read_text(encoding="utf-8"))

    def _files(self, unit):
        if not isinstance(unit, str) or not re.fullmatch(r"[1-4]\.[12]\.[1-5]", unit):
            raise ValueError("题号无效")
        files = [p for p in self.source_files if p.startswith(f"{MATERIALS}/{unit}/")]
        if not files:
            raise ValueError("题目不存在")
        return files

    def _prepare_question(self, paper_id, unit):
        self._files(unit)
        attempt = datetime.now(timezone(timedelta(hours=8))).strftime("%H%M%S") + "-" + uuid.uuid4().hex[:8]
        folder = self.papers / paper_id / "作答" / unit / attempt
        if not folder.resolve().is_relative_to(self.papers.resolve()):
            raise ValueError("作答路径无效")
        folder.mkdir(parents=True, exist_ok=False)
        prefix = PurePosixPath(MATERIALS) / unit
        # 流式复制原始素材，包含模型、图片、vision 模块；不复制用户已有答案。
        process = subprocess.Popen(["git", "archive", self.baseline, "--", prefix.as_posix()],
                                   cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
                for member in archive:
                    if member.isdir():
                        continue
                    if not member.isfile():
                        raise ValueError("素材中包含不支持的文件类型")
                    relative = PurePosixPath(member.name).relative_to(prefix)
                    target = folder.joinpath(*relative.parts)
                    if not target.resolve().is_relative_to(folder.resolve()):
                        raise ValueError("素材路径无效")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as src, target.open("wb") as dst:
                        shutil.copyfileobj(src, dst, 1024 * 1024)
        finally:
            process.stdout.close()
            error = process.stderr.read()
            process.stderr.close()
            status = process.wait()
        if status:
            raise RuntimeError("读取原始素材失败：" + error.decode("utf-8", errors="replace"))
        notebook = folder / f"{unit}.ipynb"
        has_code = False
        if notebook.is_file():
            nb = json.loads(notebook.read_text(encoding="utf-8"))
            for cell in nb.get("cells", []):
                if cell.get("cell_type") == "code":
                    has_code = True
                    cell["outputs"] = []
                    cell["execution_count"] = None
            self._save_json(notebook, nb)
        raw = (folder / f"{unit}.html").read_text(encoding="utf-8")
        match = re.search(r"<title>(.*?)</title>", raw, re.S | re.I)
        title = html.unescape(match.group(1).strip()) if match else unit
        title = re.sub(r"^" + re.escape(unit) + r"\s*", "", title)
        group = unit.rsplit(".", 1)[0]
        name, minutes, points = GROUPS[group]
        return {"unit": unit, "group": group, "group_name": name, "title": title,
                "minutes": minutes, "points": points, "has_code": has_code,
                "folder": folder.relative_to(self.root).as_posix()}

    def _present(self, paper):
        paper = json.loads(json.dumps(paper))
        paper["folder_url"] = "/" + quote(f"考试目录/试卷/{paper['id']}/", safe="/")
        for question in paper["questions"]:
            folder = self.root / question["folder"]
            question["folder_url"] = "/" + quote(question["folder"] + "/", safe="/")
            question["files"] = []
            for path in sorted(folder.iterdir()):
                if path.name.startswith("."):
                    continue
                rel = path.relative_to(self.root).as_posix()
                question["files"].append({"name": path.name, "directory": path.is_dir(), "suffix": path.suffix,
                    "url": "/" + quote(rel, safe="/") + ("/" if path.is_dir() else "")})
            notebook = folder / f"{question['unit']}.ipynb"
            target = notebook if notebook.is_file() else folder
            question["jupyter_url"] = "/jupyter?path=" + quote(target.relative_to(self.root).as_posix(), safe="")
        return paper

    def current(self):
        with self.lock:
            if not self.current_file.exists():
                return self.create(INITIAL_UNITS)
            return self.get(json.loads(self.current_file.read_text(encoding="utf-8"))["id"])

    def get(self, paper_id):
        with self.lock:
            return self._present(self._read(paper_id))

    def create(self, units=None, expected_current=None):
        with self.lock:
            previous = None
            if self.current_file.exists():
                current_id = json.loads(self.current_file.read_text(encoding="utf-8"))["id"]
                if expected_current is not None and expected_current != current_id:
                    raise ConflictError("其他页面已抽取新试卷，请刷新后重试")
                previous = [q["unit"] for q in self._read(current_id)["questions"]]
            units = validate_units(units) if units is not None else draw_units(previous)
            stamp = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d-%H%M%S")
            paper_id = stamp + "-" + uuid.uuid4().hex[:8]
            questions = [self._prepare_question(paper_id, unit) for unit in units]
            paper = {"id": paper_id, "created_at": now(), "version": 1, "questions": questions,
                     "minutes": sum(q["minutes"] for q in questions),
                     "points": sum(q["points"] for q in questions), "resets": []}
            self._save_json(self._paper_file(paper_id), paper)
            self._save_json(self.current_file, {"id": paper_id})
            return self._present(paper)

    def reset(self, paper_id, version, unit=None):
        with self.lock:
            paper = self._read(paper_id)
            if version != paper["version"]:
                raise ConflictError("试卷作答版本已更新，请刷新后再重置")
            if unit is not None and unit not in [q["unit"] for q in paper["questions"]]:
                raise ValueError("本套试卷中没有这道题")
            replaced, questions = [], []
            for question in paper["questions"]:
                if unit is None or unit == question["unit"]:
                    fresh = self._prepare_question(paper_id, question["unit"])
                    replaced.append({"unit": question["unit"], "folder": question["folder"]})
                    questions.append(fresh)
                else:
                    questions.append(question)
            paper["questions"] = questions
            paper["version"] += 1
            paper["resets"].append({"at": now(), "previous": replaced})
            # 旧目录保留；旧标签页的自动保存不会覆盖重置后的副本。
            self._save_json(self._paper_file(paper_id), paper)
            return self._present(paper)

    def history(self):
        with self.lock:
            result = []
            for path in sorted(self.papers.glob("*/paper.json"), reverse=True):
                paper = json.loads(path.read_text(encoding="utf-8"))
                result.append({"id": paper["id"], "created_at": paper["created_at"],
                               "units": [q["unit"] for q in paper["questions"]]})
            return sorted(result, key=lambda item: item["created_at"], reverse=True)

    def reset_practice(self, unit):
        """兼容练习导航的重置；仅重置笔记本，并先备份当前作答。"""
        with self.lock:
            self._files(unit)
            rel = f"{MATERIALS}/{unit}/{unit}.ipynb"
            if rel not in self.source_files or not (self.root / rel).is_file():
                raise FileNotFoundError("该题没有练习笔记本")
            data = json.loads(self._git("show", f"{self.baseline}:{rel}"))
            for cell in data["cells"]:
                if cell["cell_type"] == "code":
                    cell["outputs"], cell["execution_count"] = [], None
            backup = self.root / ".venv" / "reset-backups" / f"{unit}-{uuid.uuid4().hex[:12]}.zip"
            backup.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(backup, "x", zipfile.ZIP_DEFLATED) as archive:
                archive.write(self.root / rel, rel)
            self._save_json(self.root / rel, data)
            return {"success": True, "message": f"{unit} 已恢复原始填空；旧作答已备份。请刷新笔记本页面。"}
