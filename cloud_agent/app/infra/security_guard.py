import re


USER_ID_PATTERN = re.compile(r"user_id\s*=\s*([a-zA-Z0-9_-]+)", re.IGNORECASE)
PROMPT_INJECTION_PATTERNS = (
    "忽略之前",
    "忽略以上",
    "忽略系统",
    "系统指令",
    "内部提示词",
    "开发者消息",
    "ignore previous",
    "ignore above",
    "system prompt",
    "developer message",
)
SECRET_PATTERNS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "密钥",
    "令牌",
    "密码",
)


def inspect_input(query: str, *, user_id: str) -> dict[str, object]:
    """Inspect user input before it enters cache, memory, or Agent workflow."""

    text = query or ""
    lowered = text.lower()

    mentioned_user_ids = USER_ID_PATTERN.findall(text)
    if any(mentioned != user_id for mentioned in mentioned_user_ids):
        return _blocked("cross_user_access")

    if any(pattern in lowered for pattern in PROMPT_INJECTION_PATTERNS):
        return _blocked("prompt_injection")

    if any(pattern in lowered for pattern in SECRET_PATTERNS):
        return _blocked("secret_exfiltration")

    return {
        "allowed": True,
        "reason": "allowed",
        "risk_level": "low",
    }


def _blocked(reason: str) -> dict[str, object]:
    return {
        "allowed": False,
        "reason": reason,
        "risk_level": "high",
    }
