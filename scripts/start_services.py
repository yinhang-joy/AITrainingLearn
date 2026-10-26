"""Windows 一键启动练习服务，不安装依赖、不修改练习或讲义。"""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import time
from urllib.parse import quote
from urllib.request import build_opener, ProxyHandler, Request
import webbrowser


ROOT = Path(__file__).resolve().parent.parent
JUPYTER_PORT = 8891
RESET_PORT = 8765
JUPYTER_URL = f"http://localhost:{JUPYTER_PORT}"
NAVIGATION = ROOT / "练习导航.html"
OPENER = build_opener(ProxyHandler({}))  # 本机服务不经过系统 HTTP 代理。


def port_in_use(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5):
            return True
    except OSError:
        return False


def request(url, *, token="", method="GET"):
    headers = {"Authorization": "token " + token} if token else {}
    with OPENER.open(Request(url, headers=headers, method=method), timeout=1) as response:
        return response.status, response.headers, response.read()


def jupyter_ready(token):
    try:
        status, _, body = request(JUPYTER_URL + "/api/status", token=token)
        return status == 200 and "connections" in json.loads(body)
    except (OSError, ValueError):
        return False


def reset_ready():
    try:
        status, headers, _ = request(f"http://localhost:{RESET_PORT}/reset", method="OPTIONS")
        return (
            status == 200
            and "POST" in headers.get("Access-Control-Allow-Methods", "")
            and headers.get("Access-Control-Allow-Origin") == "*"
        )
    except OSError:
        return False


def running_jupyter():
    from jupyter_server.serverapp import list_running_servers

    for server in list_running_servers():
        root_dir = server.get("root_dir") or server.get("notebook_dir")
        if (
            server.get("port") == JUPYTER_PORT
            and root_dir
            and Path(root_dir).resolve() == ROOT
            and server.get("base_url", "/") == "/"
        ):
            return server
    return None


@contextmanager
def startup_lock(state_dir):
    import msvcrt

    with (state_dir / "startup.lock").open("a+b") as lock:
        if lock.seek(0, os.SEEK_END) == 0:
            lock.write(b"\0")
            lock.flush()
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise RuntimeError("另一个启动脚本正在运行，请稍后重试。") from exc
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def start_background(name, arguments, log_dir, *, token=""):
    env = os.environ.copy()
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    if name == "jupyter":
        env["JUPYTER_TOKEN"] = token
    log_path = log_dir / f"{name}-{datetime.now():%Y%m%d-%H%M%S}-{os.getpid()}.log"
    with log_path.open("ab") as output:
        process = subprocess.Popen(
            [sys.executable, "-X", "utf8", "-u", *arguments],
            cwd=ROOT,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=output,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    return process, log_path


def wait_ready(label, check, process, log_path):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if check():
            return
        if process.poll() is not None:
            break
        time.sleep(0.3)
    raise RuntimeError(f"{label} 未能启动。请查看本机日志：{log_path}")


def ensure_jupyter(log_dir):
    server = running_jupyter()
    if port_in_use(JUPYTER_PORT):
        if server and jupyter_ready(server.get("token", "")):
            print(f"Jupyter 已运行，复用 {JUPYTER_PORT} 端口。")
            return server.get("token", "")
        raise RuntimeError(f"{JUPYTER_PORT} 端口已被其他服务占用，或该 Jupyter 无法认证。不会终止现有进程。")

    token = secrets.token_hex(32)
    process, log = start_background(
        "jupyter",
        [
            "-m", "jupyterlab", "--no-browser", "--ip=127.0.0.1",
            f"--port={JUPYTER_PORT}", "--ServerApp.port_retries=0",
            f"--ServerApp.root_dir={ROOT}",
        ],
        log_dir,
        token=token,
    )
    wait_ready("Jupyter", lambda: jupyter_ready(token), process, log)
    print(f"Jupyter 已启动：{JUPYTER_URL}/lab")
    return token


def ensure_reset(log_dir):
    if port_in_use(RESET_PORT):
        if reset_ready():
            print(f"重置服务已运行，复用 {RESET_PORT} 端口。")
            return
        raise RuntimeError(f"{RESET_PORT} 端口已被其他服务占用，不会终止现有进程。")
    process, log = start_background("reset", [str(ROOT / "scripts/reset_service.py")], log_dir)
    wait_ready("重置服务", reset_ready, process, log)
    print(f"重置服务已启动：http://localhost:{RESET_PORT}")


def refresh_navigation(state_dir):
    backup = state_dir / f"navigation-before-{datetime.now():%Y%m%d-%H%M%S}-{os.getpid()}.html"
    had_navigation = NAVIGATION.is_file()
    if had_navigation:
        shutil.copy2(NAVIGATION, backup)
    env = os.environ.copy()
    # 共享导航不保存 token；浏览器通过单独的认证入口建立会话。
    env.update(JUPYTER_PORT=str(JUPYTER_PORT), JUPYTER_TOKEN="", PYTHONUTF8="1")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "scripts/generate_nav.py"), "--navigation-only"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        if had_navigation:
            shutil.copy2(backup, NAVIGATION)
        raise RuntimeError("导航生成失败，原导航已保留。\n" + result.stderr.strip())
    print("练习导航已更新；讲义与练习文件未改动。")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-browser", action="store_true", help="只启动服务，不打开浏览器")
    args = parser.parse_args(argv)
    if os.name != "nt":
        raise RuntimeError("此启动入口用于 Windows。")
    # 启动前检查依赖，失败时不自动安装或修改虚拟环境。
    import jupyterlab  # noqa: F401
    import pandas  # noqa: F401
    import openpyxl  # noqa: F401

    workspace_id = hashlib.sha256(str(ROOT).encode("utf-8")).hexdigest()[:12]
    state_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "AITraining" / workspace_id
    log_dir = state_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    with startup_lock(state_dir):
        token = ensure_jupyter(log_dir)
        ensure_reset(log_dir)
        refresh_navigation(state_dir)
    print(f"服务就绪。日志和导航备份：{state_dir}")
    if not args.no_browser:
        auth_url = JUPYTER_URL + "/lab"
        if token:
            auth_url += "?token=" + quote(token, safe="")
        try:
            # 先认证 localhost 会话，再打开导航；token 不输出到控制台或导航文件。
            if not webbrowser.open(auth_url):
                raise RuntimeError("没有可用的默认浏览器")
            if not webbrowser.open(NAVIGATION.as_uri()):
                raise RuntimeError("无法打开导航")
        except Exception as exc:
            print(f"服务已运行，但无法自动打开浏览器：{type(exc).__name__}。请检查默认浏览器设置后重新运行。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ImportError) as exc:
        print(f"启动失败：{exc}", file=sys.stderr)
        raise SystemExit(1)
