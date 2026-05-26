import json

from infra.request_context import RequestContext
from infra.structured_logging import build_event_record


def test_build_event_record_is_json_serializable():
    context = RequestContext(
        trace_id="trace-1",
        user_id="user_1001",
        session_id="session_a",
    )

    record = build_event_record(
        "chat.workflow.completed",
        context=context,
        agent="billing_agent",
        latency_ms=42,
    )

    encoded = json.dumps(record, ensure_ascii=False)
    decoded = json.loads(encoded)

    assert decoded["event"] == "chat.workflow.completed"
    assert decoded["trace_id"] == "trace-1"
    assert decoded["agent"] == "billing_agent"
    assert decoded["latency_ms"] == 42


def test_build_event_record_omits_none_values_and_prompt_text():
    context = RequestContext(
        trace_id="trace-1",
        user_id="user_1001",
        session_id="session_a",
    )

    record = build_event_record(
        "chat.request.started",
        context=context,
        agent=None,
        query="帮我查一下订单",
        api_key=None,
    )

    assert "agent" not in record
    assert "query" not in record
    assert "api_key" not in record
