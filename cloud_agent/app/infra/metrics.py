from threading import Lock


class MetricsRecorder:
    """In-process counters for local operations and CI-friendly tests."""

    def __init__(self) -> None:
        self._lock = Lock()
        self.reset()

    def record_request(self, *, latency_ms: float, success: bool) -> None:
        with self._lock:
            self._requests_total += 1
            self._total_latency_ms += max(float(latency_ms), 0.0)
            if not success:
                self._requests_failed_total += 1

    def record_cache_hit(self) -> None:
        with self._lock:
            self._cache_hits_total += 1

    def record_cache_miss(self) -> None:
        with self._lock:
            self._cache_misses_total += 1

    def record_security_block(self) -> None:
        with self._lock:
            self._security_blocks_total += 1

    def snapshot(self) -> dict[str, int | float]:
        with self._lock:
            avg_latency_ms = 0.0
            if self._requests_total:
                avg_latency_ms = round(self._total_latency_ms / self._requests_total, 2)
            return {
                "requests_total": self._requests_total,
                "requests_failed_total": self._requests_failed_total,
                "cache_hits_total": self._cache_hits_total,
                "cache_misses_total": self._cache_misses_total,
                "security_blocks_total": self._security_blocks_total,
                "avg_latency_ms": avg_latency_ms,
            }

    def reset(self) -> None:
        with self._lock:
            self._requests_total = 0
            self._requests_failed_total = 0
            self._cache_hits_total = 0
            self._cache_misses_total = 0
            self._security_blocks_total = 0
            self._total_latency_ms = 0.0


request_metrics = MetricsRecorder()
