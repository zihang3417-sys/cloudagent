from infra.request_context import RequestContext


def test_request_context_generates_trace_id():
    context = RequestContext.create(user_id="user_1001", session_id="session_a")

    assert len(context.trace_id) == 32
    assert context.trace_id.isalnum()


def test_request_context_serializes_log_fields():
    context = RequestContext(
        trace_id="abc123",
        user_id="user_1001",
        session_id="session_a",
    )

    assert context.to_log_fields() == {
        "trace_id": "abc123",
        "user_id": "user_1001",
        "session_id": "session_a",
    }
