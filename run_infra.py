"""PyCharm-friendly infrastructure launcher for CloudAgent.

Run this file from PyCharm to start the Docker Compose services without
manually switching into the infra directory.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parent
INFRA_DIR = PROJECT_ROOT / "infra"
COMPOSE_FILE = INFRA_DIR / "docker-compose.yml"
COMMON_DOCKER_PATHS = [
    Path(r"C:\Program Files\Docker\Docker\resources\bin\docker.exe"),
]


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def find_docker() -> str | None:
    docker = shutil.which("docker")
    if docker:
        return docker

    for docker_path in COMMON_DOCKER_PATHS:
        if docker_path.exists():
            os.environ["PATH"] = f"{docker_path.parent}{os.pathsep}{os.environ.get('PATH', '')}"
            return str(docker_path)

    return None


def build_compose_command(docker: str) -> list[str]:
    return [docker, "compose", "up", "-d"]


def print_missing_docker() -> None:
    print("没有找到 Docker 命令。")
    print("这通常表示本机还没有安装 Docker Desktop，或者安装后当前终端/PyCharm 还没刷新 PATH。")
    print("处理方式：")
    print("1. 安装并打开 Docker Desktop，等它显示正在运行。")
    print("2. 关闭并重新打开 PowerShell 或 PyCharm。")
    print("3. 在终端里执行 docker --version，能看到版本号后再运行本脚本。")


def main(argv: Sequence[str] | None = None) -> int:
    configure_console()

    parser = argparse.ArgumentParser(description="启动 CloudAgent 本地 Docker 基础服务。")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="只检查 Docker 和 compose 文件是否可用，不真正启动容器。",
    )
    args = parser.parse_args(argv)

    if not COMPOSE_FILE.exists():
        print(f"没有找到 compose 文件：{COMPOSE_FILE}")
        print("请确认 PyCharm 打开的是项目根目录 F:\\agent0520\\cloudagent_enterprise。")
        return 1

    docker = find_docker()
    if not docker:
        print_missing_docker()
        return 1

    print(f"已找到 Docker：{docker}")
    print(f"基础服务目录：{INFRA_DIR}")

    if args.check_only:
        print("检查完成：Docker 命令和 compose 文件都可以被找到。")
        return 0

    print("正在启动 MySQL / Redis / Milvus / Neo4j 等基础服务...")
    print("如果这里提示 Docker daemon 没启动，请先打开 Docker Desktop。")

    try:
        subprocess.check_call(build_compose_command(docker), cwd=INFRA_DIR)
    except FileNotFoundError:
        print_missing_docker()
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"Docker Compose 启动失败，退出码：{exc.returncode}")
        print("请先确认 Docker Desktop 已经打开，并且本机端口 3306、6379、7474、7687、19530 没被占用。")
        return exc.returncode

    print("基础服务启动命令已执行。下一步可以在 PyCharm 运行 check_full_demo.py 做自检。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
