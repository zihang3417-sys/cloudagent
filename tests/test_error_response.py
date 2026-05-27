from infra.error_response import classify_error


def test_classify_cache_error_from_runtime_message():
    error = classify_error(RuntimeError("cache exploded"))

    assert error == {
        "code": "CACHE_ERROR",
        "message": "系统暂时无法处理请求，请稍后重试。",
        "retryable": True,
    }


def test_classify_workflow_error_from_runtime_message():
    error = classify_error(RuntimeError("graph workflow failed"))

    assert error == {
        "code": "WORKFLOW_ERROR",
        "message": "智能体工作流暂时不可用，请稍后重试。",
        "retryable": True,
    }


def test_classify_unknown_error_uses_safe_generic_message():
    error = classify_error(ValueError("secret internal detail"))

    assert error == {
        "code": "INTERNAL_ERROR",
        "message": "系统暂时无法处理请求，请稍后重试。",
        "retryable": True,
    }


def test_classify_timeout_error_uses_workflow_timeout_code():
    import asyncio

    error = classify_error(asyncio.TimeoutError())

    assert error == {
        "code": "WORKFLOW_TIMEOUT",
        "message": "Workflow timed out. Please retry later.",
        "retryable": True,
    }
