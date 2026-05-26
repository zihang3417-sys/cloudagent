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


def test_build_event_record_redacts_pii_inside_allowed_string_fields():
    context = RequestContext(
        trace_id="trace-1",
        user_id="user_1001",
        session_id="session_a",
    )

    record = build_event_record(
        "chat.cache.hit",
        context=context,
        matched_question=(
            "Contact alice@example.com or 13800138000. "
            "Authorization: Bearer secret-token-123. api_key=sk-abcdef1234567890"
        ),
    )

    encoded = json.dumps(record, ensure_ascii=False)

    assert "alice@example.com" not in encoded
    assert "13800138000" not in encoded
    assert "secret-token-123" not in encoded
    assert "sk-abcdef1234567890" not in encoded
    assert "[REDACTED_EMAIL]" in encoded
    assert "[REDACTED_PHONE]" in encoded
    assert "[REDACTED_TOKEN]" in encoded
    assert "[REDACTED_SECRET]" in encoded


def test_build_event_record_redacts_nested_sensitive_fields():
    context = RequestContext(
        trace_id="trace-1",
        user_id="user_1001",
        session_id="session_a",
    )

    record = build_event_record(
        "chat.security.blocked",
        context=context,
        details={
            "email": "bob@example.com",
            "token": "nested-token-value",
            "messages": ["call 13900139000"],
        },
    )

    encoded = json.dumps(record, ensure_ascii=False)

    assert "bob@example.com" not in encoded
    assert "nested-token-value" not in encoded
    assert "13900139000" not in encoded
    assert record["details"]["email"] == "[REDACTED_EMAIL]"
    assert record["details"]["token"] == "[REDACTED]"
    assert record["details"]["messages"] == ["call [REDACTED_PHONE]"]
