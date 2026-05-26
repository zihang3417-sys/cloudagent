GENERIC_RETRY_MESSAGE = "系统暂时无法处理请求，请稍后重试。"
WORKFLOW_RETRY_MESSAGE = "智能体工作流暂时不可用，请稍后重试。"


def classify_error(exc: Exception) -> dict[str, object]:
    """Map internal exceptions to safe client-facing error payloads."""

    detail = str(exc).lower()
    if "cache" in detail:
        return {
            "code": "CACHE_ERROR",
            "message": GENERIC_RETRY_MESSAGE,
            "retryable": True,
        }
    if "workflow" in detail or "graph" in detail:
        return {
            "code": "WORKFLOW_ERROR",
            "message": WORKFLOW_RETRY_MESSAGE,
            "retryable": True,
        }
    return {
        "code": "INTERNAL_ERROR",
        "message": GENERIC_RETRY_MESSAGE,
        "retryable": True,
    }
