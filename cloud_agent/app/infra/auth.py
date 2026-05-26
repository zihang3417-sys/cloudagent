DEMO_TOKEN_USERS = {
    "demo-user-1001": "user_1001",
    "demo-user-1002": "user_1002",
}
DEFAULT_DEMO_USER_ID = "user_1001"


def resolve_demo_user(authorization: str | None) -> dict[str, str]:
    """Resolve a trusted demo user id from an Authorization header."""

    token = _extract_bearer_token(authorization)
    if token and token in DEMO_TOKEN_USERS:
        return {
            "user_id": DEMO_TOKEN_USERS[token],
            "auth_mode": "demo_token",
        }
    return {
        "user_id": DEFAULT_DEMO_USER_ID,
        "auth_mode": "demo_default",
    }


def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()
