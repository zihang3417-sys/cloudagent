from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from infra.auth import resolve_demo_user
from infra.error_response import rate_limited_error
from infra.rate_limiter import RateLimiter
from schemas.chat import ChatRequest
from service.chat_service import stream_chat

router = APIRouter()
chat_rate_limiter = RateLimiter.from_env()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, authorization: str | None = Header(default=None)):
    """
    处理多智能体聊天请求，并使用 SSE (Server-Sent Events) 返回流式响应。
    如果命中 L1 语义缓存，将直接返回缓存结果。
    否则进入 Agent 图编排流程。
    """
    auth_user = resolve_demo_user(authorization)
    limit_decision = chat_rate_limiter.check(auth_user["user_id"])
    if not limit_decision.allowed:
        retry_after = limit_decision.retry_after_seconds
        return JSONResponse(
            status_code=429,
            content={"error": rate_limited_error(retry_after)},
            headers={"Retry-After": str(retry_after)},
        )

    return StreamingResponse(
        stream_chat(
            request.query,
            auth_user["user_id"],
            request.session_id,
            auth_mode=auth_user["auth_mode"],
        ),
        media_type="text/event-stream"
    )
