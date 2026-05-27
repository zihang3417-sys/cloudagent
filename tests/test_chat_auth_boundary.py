from fastapi import FastAPI
from fastapi.testclient import TestClient

from infra.rate_limiter import RateLimiter
from router import chat


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat.router, prefix="/api")
    return app


def test_chat_endpoint_uses_user_id_from_demo_token(monkeypatch):
    captured = {}

    async def fake_stream_chat(query, user_id, session_id, auth_mode=None):
        captured.update(
            {
                "query": query,
                "user_id": user_id,
                "session_id": session_id,
                "auth_mode": auth_mode,
            }
        )
        yield 'data: {"done": true}\n\n'

    monkeypatch.setattr(chat, "stream_chat", fake_stream_chat)
    client = TestClient(create_test_app())

    response = client.post(
        "/api/chat",
        headers={"Authorization": "Bearer demo-user-1001"},
        json={
            "query": "帮我查一下订单",
            "user_id": "user_1002",
            "session_id": "session_a",
        },
    )

    assert response.status_code == 200
    assert captured == {
        "query": "帮我查一下订单",
        "user_id": "user_1001",
        "session_id": "session_a",
        "auth_mode": "demo_token",
    }


def test_chat_endpoint_keeps_local_demo_working_without_token(monkeypatch):
    captured = {}

    async def fake_stream_chat(query, user_id, session_id, auth_mode=None):
        captured.update({"user_id": user_id, "auth_mode": auth_mode})
        yield 'data: {"done": true}\n\n'

    monkeypatch.setattr(chat, "stream_chat", fake_stream_chat)
    client = TestClient(create_test_app())

    response = client.post(
        "/api/chat",
        json={
            "query": "帮我查一下订单",
            "user_id": "user_1002",
            "session_id": "session_a",
        },
    )

    assert response.status_code == 200
    assert captured == {
        "user_id": "user_1001",
        "auth_mode": "demo_default",
    }


def test_chat_endpoint_returns_429_when_user_rate_limit_is_exceeded(monkeypatch):
    calls = {"count": 0}

    async def fake_stream_chat(query, user_id, session_id, auth_mode=None):
        calls["count"] += 1
        yield 'data: {"done": true}\n\n'

    limiter = RateLimiter(limit=1, window_seconds=60, clock=lambda: 1000.0)
    monkeypatch.setattr(chat, "chat_rate_limiter", limiter)
    monkeypatch.setattr(chat, "stream_chat", fake_stream_chat)
    client = TestClient(create_test_app())

    first_response = client.post(
        "/api/chat",
        headers={"Authorization": "Bearer demo-user-1001"},
        json={
            "query": "first request",
            "user_id": "user_1001",
            "session_id": "session_a",
        },
    )
    second_response = client.post(
        "/api/chat",
        headers={"Authorization": "Bearer demo-user-1001"},
        json={
            "query": "second request",
            "user_id": "user_1001",
            "session_id": "session_a",
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 429
    assert second_response.headers["Retry-After"] == "60"
    assert second_response.json() == {
        "error": {
            "code": "RATE_LIMITED",
            "message": "Too many chat requests. Please retry later.",
            "retryable": True,
            "retry_after_seconds": 60,
        }
    }
    assert calls["count"] == 1
