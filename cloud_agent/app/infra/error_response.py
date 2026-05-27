GENERIC_RETRY_MESSAGE = "系统暂时无法处理请求，请稍后重试。"
WORKFLOW_RETRY_MESSAGE = "智能体工作流暂时不可用，请稍后重试。"


WORKFLOW_TIMEOUT_MESSAGE = "Workflow timed out. Please retry later."
RATE_LIMITED_MESSAGE = "Too many chat requests. Please retry later."


def classify_error(exc: Exception) -> dict[str, object]:
    """Map internal exceptions to safe client-facing error payloads."""

    if isinstance(exc, TimeoutError) or exc.__class__.__name__ == "TimeoutError":
        return {
            "code": "WORKFLOW_TIMEOUT",
            "message": WORKFLOW_TIMEOUT_MESSAGE,
            "retryable": True,
        }

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


def rate_limited_error(retry_after_seconds: int) -> dict[str, object]:
    return {
        "code": "RATE_LIMITED",
        "message": RATE_LIMITED_MESSAGE,
        "retryable": True,
        "retry_after_seconds": retry_after_seconds,
    }
