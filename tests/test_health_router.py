from fastapi import FastAPI
from fastapi.testclient import TestClient

from router import health
from service import chat_service


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health.router, prefix="/api")
    return app


def test_health_endpoint_returns_ok():
    client = TestClient(create_test_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "cloudagent-enterprise",
    }


def test_ready_endpoint_reports_ready_when_core_services_initialized(monkeypatch):
    monkeypatch.setattr(chat_service, "graph", object())
    monkeypatch.setattr(chat_service, "memory", object())
    client = TestClient(create_test_app())

    response = client.get("/api/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "graph_initialized": True,
            "memory_initialized": True,
        },
    }


def test_ready_endpoint_reports_degraded_before_initialization(monkeypatch):
    monkeypatch.setattr(chat_service, "graph", None)
    monkeypatch.setattr(chat_service, "memory", None)
    client = TestClient(create_test_app())

    response = client.get("/api/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "checks": {
            "graph_initialized": False,
            "memory_initialized": False,
        },
    }


def test_app_registers_health_routes():
    from app_main import app

    paths = {route.path for route in app.routes}

    assert "/api/health" in paths
    assert "/api/ready" in paths
