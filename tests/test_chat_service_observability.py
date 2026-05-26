import json

import pytest

from infra.metrics import request_metrics
from service import chat_service


class FakeSemanticCache:
    async def get_cache(self, query, user_id):
        return {
            "answer": "缓存答案",
            "level": "exact",
            "distance": 0.0,
            "matched_question": "测试问题",
        }


@pytest.mark.asyncio
async def test_stream_chat_logs_trace_id_for_cache_hit(monkeypatch, capsys):
    request_metrics.reset()
    monkeypatch.setattr(chat_service, "semantic_cache", FakeSemanticCache())
    monkeypatch.setattr(chat_service, "memory", None)

    chunks = []
    async for chunk in chat_service.stream_chat(
        query="测试问题",
        user_id="user_1001",
        session_id="session_a",
    ):
        chunks.append(chunk)

    output = capsys.readouterr().out
    log_lines = [
        json.loads(line)
        for line in output.splitlines()
        if line.startswith("{") and "trace_id" in line
    ]

    assert any(line["event"] == "chat.request.started" for line in log_lines)
    assert any(line["event"] == "chat.cache.hit" for line in log_lines)
    assert any(line["event"] == "chat.request.completed" for line in log_lines)
    assert all(line["user_id"] == "user_1001" for line in log_lines)
    assert chunks[-1] == 'data: {"done": true}\n\n'
    assert request_metrics.snapshot()["requests_total"] == 1
    assert request_metrics.snapshot()["cache_hits_total"] == 1


class FailingSemanticCache:
    async def get_cache(self, query, user_id):
        raise RuntimeError("cache exploded")


@pytest.mark.asyncio
async def test_stream_chat_records_failed_request_metrics(monkeypatch):
    request_metrics.reset()
    monkeypatch.setattr(chat_service, "semantic_cache", FailingSemanticCache())
    monkeypatch.setattr(chat_service, "memory", None)

    with pytest.raises(RuntimeError):
        async for _ in chat_service.stream_chat(
            query="测试问题",
            user_id="user_1001",
            session_id="session_a",
        ):
            pass

    snapshot = request_metrics.snapshot()
    assert snapshot["requests_total"] == 1
    assert snapshot["requests_failed_total"] == 1
