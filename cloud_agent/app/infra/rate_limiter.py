import math
import os
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    retry_after_seconds: int = 0


class RateLimiter:
    """Small in-process fixed-window limiter for local pilots and tests."""

    def __init__(
        self,
        *,
        limit: int,
        window_seconds: int,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self.limit = int(limit)
        self.window_seconds = int(window_seconds)
        self._clock = clock
        self._lock = Lock()
        self._requests: defaultdict[str, deque[float]] = defaultdict(deque)

    @classmethod
    def from_env(cls) -> "RateLimiter":
        return cls(
            limit=int(os.getenv("CHAT_RATE_LIMIT", "60")),
            window_seconds=int(os.getenv("CHAT_RATE_LIMIT_WINDOW_SECONDS", "60")),
        )

    def check(self, key: str) -> RateLimitDecision:
        if self.limit <= 0 or self.window_seconds <= 0:
            return RateLimitDecision(allowed=True)

        now = self._clock()
        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._requests[key]
            while timestamps and timestamps[0] <= window_start:
                timestamps.popleft()

            if len(timestamps) >= self.limit:
                retry_after = self.window_seconds - (now - timestamps[0])
                return RateLimitDecision(
                    allowed=False,
                    retry_after_seconds=max(1, math.ceil(retry_after)),
                )

            timestamps.append(now)
            return RateLimitDecision(allowed=True)
