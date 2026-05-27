from __future__ import annotations

import asyncio

import check_full_demo


def test_missing_dependency_message_points_to_enterprise_interpreter(capsys):
    exc = ModuleNotFoundError("No module named 'aiosqlite'", name="aiosqlite")

    check_full_demo.print_missing_python_dependency(exc)

    output = capsys.readouterr().out
    assert "缺少 Python 依赖：aiosqlite" in output
    assert "当前 Python 解释器" in output
    assert "cloudagent_enterprise\\.venv\\Scripts\\python.exe" in output
    assert "pip install -r cloud_agent\\agent\\requirements.txt" in output


def test_agent_initialization_timeout_prints_next_step(monkeypatch, capsys):
    class SlowChatService:
        async def init_agent_system(self):
            await asyncio.sleep(0.1)

    monkeypatch.setenv("CHECK_FULL_DEMO_INIT_TIMEOUT_SECONDS", "0.01")

    ok = asyncio.run(check_full_demo.initialize_agent_system(SlowChatService()))

    output = capsys.readouterr().out
    assert ok is False
    assert "Agent system initialization" in output
    assert "run_infra.py" in output


def test_run_cli_exits_with_main_exit_code(monkeypatch):
    calls: list[int] = []

    async def fake_main() -> int:
        return 7

    monkeypatch.setattr(check_full_demo, "main", fake_main)
    monkeypatch.setattr(check_full_demo.os, "_exit", lambda code: calls.append(code))

    check_full_demo.run_cli()

    assert calls == [7]
