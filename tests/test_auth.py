from infra.auth import resolve_demo_user


def test_resolve_demo_user_from_bearer_token():
    user = resolve_demo_user("Bearer demo-user-1001")

    assert user == {
        "user_id": "user_1001",
        "auth_mode": "demo_token",
    }


def test_resolve_demo_user_uses_safe_default_without_token():
    user = resolve_demo_user(None)

    assert user == {
        "user_id": "user_1001",
        "auth_mode": "demo_default",
    }


def test_resolve_demo_user_rejects_unknown_token():
    user = resolve_demo_user("Bearer unknown-token")

    assert user == {
        "user_id": "user_1001",
        "auth_mode": "demo_default",
    }
