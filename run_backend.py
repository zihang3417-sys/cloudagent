"""PyCharm-friendly backend launcher for CloudAgent.

Run this file from the project root to start the FastAPI backend on port 5000.
It configures the working directory and import paths so you do not need to run
commands from ``cloud_agent/app`` manually.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = PROJECT_ROOT / "cloud_agent" / "app"
AGENT_DIR = PROJECT_ROOT / "cloud_agent" / "agent"


def configure_runtime() -> None:
    os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")
    os.environ.setdefault("no_proxy", "127.0.0.1,localhost")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    for path in (str(APP_DIR), str(AGENT_DIR)):
        if path not in sys.path:
            sys.path.insert(0, path)

    os.chdir(APP_DIR)


if __name__ == "__main__":
    configure_runtime()

    import uvicorn

    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "5000"))
    reload_enabled = os.getenv("BACKEND_RELOAD", "false").lower() in {"1", "true", "yes"}

    print(f"Starting CloudAgent backend: http://127.0.0.1:{port}")
    uvicorn.run("app_main:app", host=host, port=port, reload=reload_enabled)
