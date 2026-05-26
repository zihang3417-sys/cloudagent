from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
from infra.auth import resolve_demo_user
from schemas.chat import ChatRequest
from service.chat_service import stream_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, authorization: str | None = Header(default=None)):
    """
    处理多智能体聊天请求，并使用 SSE (Server-Sent Events) 返回流式响应。
    如果命中 L1 语义缓存，将直接返回缓存结果。
    否则进入 Agent 图编排流程。
    """
    auth_user = resolve_demo_user(authorization)
    return StreamingResponse(
        stream_chat(
            request.query,
            auth_user["user_id"],
            request.session_id,
            auth_mode=auth_user["auth_mode"],
        ),
        media_type="text/event-stream"
    )
