"""Check whether the full CloudAgent demo environment is ready.

This script is safe to run from PyCharm. It does not print secrets.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Awaitable, Callable


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


def status(name: str, ok: bool, detail: str = "") -> None:
    flag = "OK" if ok else "FAIL"
    suffix = f" - {detail}" if detail else ""
    print(f"[{flag}] {name}{suffix}", flush=True)


def init_timeout_seconds_from_env() -> float:
    value = os.getenv("CHECK_FULL_DEMO_INIT_TIMEOUT_SECONDS", "60")
    try:
        timeout = float(value)
    except ValueError:
        return 60.0
    return timeout if timeout > 0 else 60.0


def print_missing_python_dependency(exc: ModuleNotFoundError) -> None:
    missing_name = exc.name or str(exc)
    expected_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    print(f"[FAIL] 缺少 Python 依赖：{missing_name}")
    print(f"当前 Python 解释器：{sys.executable}")
    print(f"建议在 PyCharm 里选择企业副本解释器：{expected_python}")
    print("或者在项目根目录执行：")
    print(r".\.venv\Scripts\python.exe -m pip install -r cloud_agent\agent\requirements.txt")


async def initialize_agent_system(chat_service) -> bool:
    timeout = init_timeout_seconds_from_env()
    try:
        await asyncio.wait_for(chat_service.init_agent_system(), timeout=timeout)
    except asyncio.TimeoutError:
        status("Agent system initialization", False, f"timeout after {timeout:g}s")
        print("通常是 Docker 基础服务还没启动，或 MySQL/Redis/Milvus/Neo4j 正在初始化。", flush=True)
        print("建议先在 PyCharm 运行 run_infra.py，等容器启动后再运行 check_full_demo.py。", flush=True)
        return False
    return True


def check_ollama() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        models = [item.get("name", "") for item in payload.get("models", [])]
        ok = any(model == "qwen2.5:7b" for model in models)
        status("Ollama qwen2.5:7b", ok, ", ".join(models) if models else "no models")
        return ok
    except Exception as exc:
        status("Ollama qwen2.5:7b", False, str(exc))
        return False


async def run_check(name: str, fn: Callable[[], Awaitable[str] | str]) -> bool:
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            result = await result
        status(name, True, str(result)[:160])
        return True
    except Exception as exc:
        status(name, False, str(exc))
        return False


async def main() -> int:
    configure_runtime()
    checks: list[bool] = []

    env_file = AGENT_DIR / ".env"
    env_ok = env_file.exists()
    status(".env exists", env_ok, str(env_file))
    checks.append(env_ok)

    checks.append(check_ollama())

    try:
        import app_main  # noqa: F401
        import service.chat_service as chat_service
    except ModuleNotFoundError as exc:
        print_missing_python_dependency(exc)
        return 1

    if not await initialize_agent_system(chat_service):
        return 1

    checks.append(chat_service.graph is not None)
    status("LangGraph compiled", chat_service.graph is not None)
    checks.append(chat_service.memory.short_term.available)
    status("Redis short-term memory", chat_service.memory.short_term.available)
    checks.append(chat_service.memory.long_term.available)
    status("Milvus long-term memory", chat_service.memory.long_term.available)
    checks.append(chat_service.semantic_cache.available)
    status("Milvus semantic cache", chat_service.semantic_cache.available)

    from mcp_servers.cloud_platform_server import (
        analyze_instance_usage,
        query_user_instances,
        query_user_orders,
    )
    from tools.graph_tool import query_knowledge_graph
    from tools.vector_tool import query_vector_db

    checks.append(await run_check("MySQL orders tool", lambda: query_user_orders("user_1001", 2)))
    checks.append(await run_check("MySQL instances tool", lambda: query_user_instances("user_1001", 5)))
    checks.append(
        await run_check(
            "MySQL FinOps metrics tool",
            lambda: analyze_instance_usage("i-bp1_user1001_ecs", "user_1001"),
        )
    )
    checks.append(await run_check("Milvus document RAG", lambda: query_vector_db.invoke({"query": "什么是VPC？"})))
    checks.append(
        await run_check(
            "Neo4j GraphRAG",
            lambda: query_knowledge_graph.invoke({"query": "ecs.g8a.xlarge 支持多少块弹性网卡？"}),
        )
    )
    checks.append(
        await run_check(
            "Semantic cache exact hit",
            lambda: chat_service.semantic_cache.get_cache("VPC 专有网络怎么计费？", "user_1001"),
        )
    )

    print()
    if all(checks):
        print("Full demo environment is ready.")
        return 0
    print("Some checks failed. See FULL_DEMO_SETUP.md for initialization steps.")
    return 1


def run_cli() -> None:
    exit_code = 1
    try:
        exit_code = asyncio.run(main())
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
    os._exit(exit_code)


if __name__ == "__main__":
    run_cli()
