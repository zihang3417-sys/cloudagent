import json
import logging
import re
import sys
from collections.abc import Mapping, Sequence
from typing import Any

from infra.request_context import RequestContext


LOGGER_NAME = "cloudagent.enterprise"
SENSITIVE_FIELDS = {"query", "prompt", "api_key", "token", "password", "secret"}
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?86[- ]?)?1[3-9]\d{9}\b")
BEARER_PATTERN = re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+\b", re.IGNORECASE)
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"\b(api[_-]?key|token|secret|password)\s*[:=]\s*[A-Za-z0-9._~+/=-]{6,}\b",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERN = re.compile(r"\bsk-[A-Za-z0-9]{10,}\b")


def get_enterprise_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    else:
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.stream = sys.stdout
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def redact_log_value(value: Any) -> Any:
    if isinstance(value, str):
        text = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", value)
        text = PHONE_PATTERN.sub("[REDACTED_PHONE]", text)
        text = BEARER_PATTERN.sub("Bearer [REDACTED_TOKEN]", text)
        text = SECRET_ASSIGNMENT_PATTERN.sub(
            lambda match: f"{match.group(1)}=[REDACTED_SECRET]",
            text,
        )
        return SECRET_VALUE_PATTERN.sub("[REDACTED_SECRET]", text)

    if isinstance(value, Mapping):
        redacted: dict[str, Any] = {}
        for key, nested_value in value.items():
            key_text = str(key)
            if key_text.lower() in SENSITIVE_FIELDS:
                redacted[key_text] = "[REDACTED]"
            else:
                redacted[key_text] = redact_log_value(nested_value)
        return redacted

    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [redact_log_value(item) for item in value]

    return value


def build_event_record(
    event: str,
    *,
    context: RequestContext,
    **fields: Any,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "event": event,
        **context.to_log_fields(),
    }
    for key, value in fields.items():
        if value is None or key in SENSITIVE_FIELDS:
            continue
        record[key] = redact_log_value(value)
    return record


def log_event(event: str, *, context: RequestContext, **fields: Any) -> None:
    record = build_event_record(event, context=context, **fields)
    get_enterprise_logger().info(json.dumps(record, ensure_ascii=False, sort_keys=True))
