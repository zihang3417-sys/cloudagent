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
    print(f"[{flag}] {name}{suffix}")


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

    import app_main  # noqa: F401
    import service.chat_service as chat_service

    await chat_service.init_agent_system()
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


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
