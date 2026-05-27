from infra.rate_limiter import RateLimiter


def test_rate_limiter_allows_requests_until_limit_then_blocks():
    now = 1000.0
    limiter = RateLimiter(limit=2, window_seconds=60, clock=lambda: now)

    first = limiter.check("user_1001")
    second = limiter.check("user_1001")
    third = limiter.check("user_1001")

    assert first.allowed is True
    assert second.allowed is True
    assert third.allowed is False
    assert third.retry_after_seconds == 60


def test_rate_limiter_resets_after_window():
    now = 1000.0
    limiter = RateLimiter(limit=1, window_seconds=10, clock=lambda: now)

    assert limiter.check("user_1001").allowed is True
    assert limiter.check("user_1001").allowed is False

    now = 1011.0

    assert limiter.check("user_1001").allowed is True


def test_rate_limiter_is_isolated_by_key():
    now = 1000.0
    limiter = RateLimiter(limit=1, window_seconds=60, clock=lambda: now)

    assert limiter.check("user_1001").allowed is True
    assert limiter.check("user_1002").allowed is True
    assert limiter.check("user_1001").allowed is False


def test_rate_limiter_can_be_disabled_for_local_debugging():
    limiter = RateLimiter(limit=0, window_seconds=60)

    assert limiter.check("user_1001").allowed is True
    assert limiter.check("user_1001").allowed is True
