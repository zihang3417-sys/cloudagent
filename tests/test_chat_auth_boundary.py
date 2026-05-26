from fastapi import FastAPI
from fastapi.testclient import TestClient

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
