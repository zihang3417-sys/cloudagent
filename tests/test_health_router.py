from fastapi import FastAPI
from fastapi.testclient import TestClient

from router import health
from infra.metrics import request_metrics
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


def test_metrics_endpoint_returns_current_process_snapshot():
    request_metrics.reset()
    request_metrics.record_cache_hit()
    request_metrics.record_request(latency_ms=12, success=True)
    client = TestClient(create_test_app())

    response = client.get("/api/metrics")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "metrics": {
            "requests_total": 1,
            "requests_failed_total": 0,
            "cache_hits_total": 1,
            "cache_misses_total": 0,
            "avg_latency_ms": 12.0,
        },
    }
