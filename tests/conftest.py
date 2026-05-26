from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "cloud_agent" / "app"
AGENT_DIR = ROOT_DIR / "cloud_agent" / "agent"

for path in (APP_DIR, AGENT_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
