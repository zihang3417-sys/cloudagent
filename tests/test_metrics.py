from infra.metrics import MetricsRecorder


def test_metrics_recorder_starts_empty():
    metrics = MetricsRecorder()

    assert metrics.snapshot() == {
        "requests_total": 0,
        "requests_failed_total": 0,
        "cache_hits_total": 0,
        "cache_misses_total": 0,
        "security_blocks_total": 0,
        "avg_latency_ms": 0.0,
    }


def test_metrics_recorder_tracks_requests_cache_and_latency():
    metrics = MetricsRecorder()

    metrics.record_cache_hit()
    metrics.record_cache_miss()
    metrics.record_security_block()
    metrics.record_request(latency_ms=10, success=True)
    metrics.record_request(latency_ms=30, success=False)

    assert metrics.snapshot() == {
        "requests_total": 2,
        "requests_failed_total": 1,
        "cache_hits_total": 1,
        "cache_misses_total": 1,
        "security_blocks_total": 1,
        "avg_latency_ms": 20.0,
    }


def test_metrics_recorder_can_reset_for_tests_and_local_demos():
    metrics = MetricsRecorder()
    metrics.record_cache_hit()
    metrics.record_security_block()
    metrics.record_request(latency_ms=50, success=True)

    metrics.reset()

    assert metrics.snapshot()["requests_total"] == 0
    assert metrics.snapshot()["cache_hits_total"] == 0
    assert metrics.snapshot()["security_blocks_total"] == 0
