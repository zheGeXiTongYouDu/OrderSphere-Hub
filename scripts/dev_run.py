import subprocess
import sys
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def run_backend():
    # 如果你在 backend 里用了 venv，可以在这里改成 venv 下的 python
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    return subprocess.Popen(cmd, cwd=BACKEND_DIR)


def run_frontend():
    # Windows 下用 npm.cmd，其他平台用 npm
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    cmd = [npm_cmd, "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
    return subprocess.Popen(cmd, cwd=FRONTEND_DIR)


def main():
    print(">>> OrderSphere-Hub 一键启动（开发模式）")
    print("后端目录:", BACKEND_DIR)
    print("前端目录:", FRONTEND_DIR)

    backend_proc = run_backend()
    # 稍等后端起来
    time.sleep(2)
    frontend_proc = run_frontend()

    print("\n后端: http://127.0.0.1:8000")
    print("前端: http://127.0.0.1:5173")
    print("按 Ctrl+C 结束所有进程。\n")

    try:
        # 阻塞等待任意一个进程退出
        while True:
            backend_ret = backend_proc.poll()
            frontend_ret = frontend_proc.poll()
            if backend_ret is not None or frontend_ret is not None:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n收到中断信号，正在关闭前后端进程...")

    for p in (backend_proc, frontend_proc):
        if p and p.poll() is None:
            p.terminate()

    print("已退出。")


if __name__ == "__main__":
    main()
