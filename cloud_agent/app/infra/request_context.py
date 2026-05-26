from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class RequestContext:
    """Request-scoped metadata used for logs, evals, and debugging."""

    trace_id: str
    user_id: str
    session_id: str

    @classmethod
    def create(cls, user_id: str, session_id: str) -> "RequestContext":
        return cls(
            trace_id=uuid4().hex,
            user_id=user_id or "anonymous",
            session_id=session_id or "default_session",
        )

    def to_log_fields(self) -> dict[str, str]:
        return {
            "trace_id": self.trace_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
        }
