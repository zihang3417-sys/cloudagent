import json
import logging
import sys
from typing import Any

from infra.request_context import RequestContext


LOGGER_NAME = "cloudagent.enterprise"
SENSITIVE_FIELDS = {"query", "prompt", "api_key", "token", "password", "secret"}


def get_enterprise_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


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
        record[key] = value
    return record


def log_event(event: str, *, context: RequestContext, **fields: Any) -> None:
    record = build_event_record(event, context=context, **fields)
    get_enterprise_logger().info(json.dumps(record, ensure_ascii=False, sort_keys=True))
