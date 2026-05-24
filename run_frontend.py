"""PyCharm-friendly frontend launcher for CloudAgent.

Run this file from the project root to start the Vue/Vite frontend.
Node.js and npm must be installed on the machine.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_ROOT / "cloud_agent" / "front" / "cloud_agent"
COMMON_NODE_DIRS = [
    Path(r"C:\Program Files\nodejs"),
    Path(r"C:\Program Files (x86)\nodejs"),
]


def find_npm() -> str | None:
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if npm:
        return npm

    for node_dir in COMMON_NODE_DIRS:
        npm_cmd = node_dir / "npm.cmd"
        if npm_cmd.exists():
            os.environ["PATH"] = f"{node_dir}{os.pathsep}{os.environ.get('PATH', '')}"
            return str(npm_cmd)

    return None


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    npm = find_npm()
    if not npm:
        print("npm was not found. Please install Node.js 20.19+ or 22.12+ first.")
        return 1

    if not (FRONTEND_DIR / "node_modules").exists():
        print("node_modules not found; running npm install first...")
        subprocess.check_call([npm, "install"], cwd=FRONTEND_DIR)

    env = os.environ.copy()
    env.setdefault("NO_PROXY", "127.0.0.1,localhost")
    env.setdefault("no_proxy", "127.0.0.1,localhost")

    print("Starting CloudAgent frontend. Vite will print the local URL below.")
    return subprocess.call([npm, "run", "dev"], cwd=FRONTEND_DIR, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
