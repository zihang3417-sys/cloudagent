from fastapi import APIRouter

from service import chat_service


router = APIRouter()


@router.get("/health")
async def health_endpoint() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "cloudagent-enterprise",
    }


@router.get("/ready")
async def ready_endpoint() -> dict[str, object]:
    checks = {
        "graph_initialized": chat_service.graph is not None,
        "memory_initialized": chat_service.memory is not None,
    }
    status = "ready" if all(checks.values()) else "degraded"
    return {
        "status": status,
        "checks": checks,
    }
