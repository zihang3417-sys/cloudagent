# Enterprise Trust Foundation Progress

## Implemented

### Phase 1: Trust Foundation

- Added request-scoped `trace_id` via `RequestContext`.
- Added JSON structured event helper for backend observability.
- Added server-side structured logs to the `/api/chat` service path.
- Added golden eval cases for billing, product, FinOps, and cross-user injection scenarios.
- Added local eval runner with `static` and `route` modes.
- Added pytest regression coverage for request context, logging, eval cases, and Billing user isolation.

### Phase 2: Operational Health

- Added `/api/health` for simple process liveness checks.
- Added `/api/ready` for lightweight readiness checks of Agent graph and memory initialization.
- Registered health routes in the FastAPI app.
- Added pytest coverage for health route behavior and app registration.

### Phase 3: CI Verification

- Added GitHub Actions workflow for enterprise CI.
- CI installs Python dependencies, runs pytest, and runs both static and route golden evals.
- Local verification mirrors the CI commands before commit.

### Phase 4: Request Metrics

- Added in-process metrics recorder for local operations visibility.
- Added `/api/metrics` endpoint for request, failure, cache, and average latency counters.
- Wired chat service cache-hit/cache-miss and success/failure paths into metrics.
- Added pytest coverage for metrics recorder, metrics endpoint, and chat-service metric writes.

### Phase 5: Stable Error Responses

- Added safe error classification for cache, workflow, and unknown failures.
- Changed chat SSE failure path to return stable `error` and `done` events instead of leaking raw exceptions to the client.
- Added `error_code` to structured failure logs for easier operations triage.
- Added pytest coverage for safe error payloads, failed-request metrics, and failure log classification.

### Phase 6: Lightweight Input Security Guard

- Added rule-based input inspection before cache, memory, or Agent workflow execution.
- Blocks obvious cross-user access attempts, prompt-injection phrasing, and secret-exfiltration requests.
- Returns stable SSE `SECURITY_BLOCKED` errors without entering downstream dependencies.
- Added `security_blocks_total` to in-process metrics.
- Added pytest coverage for guard rules, metrics, and chat-service security blocking.

### Phase 7: Demo Authentication Boundary

- Added demo token resolution for backend-trusted user identity.
- `/api/chat` now derives `user_id` from `Authorization: Bearer <demo-token>` instead of trusting the request body.
- Keeps local demos runnable with a safe default user when no token is provided.
- Logs `auth_mode` on chat request start for observability.
- Added pytest coverage for token mapping and body-user spoofing protection.

### Phase 8: LangGraph Checkpoint Persistence

- Added SQLite checkpoint resources using `langgraph-checkpoint-sqlite`.
- `AgentGraphManager` now compiles LangGraph with a SQLite checkpointer when enabled.
- Chat and CLI graph calls now pass a stable `thread_id` based on `user_id:session_id`.
- Supports `LANGGRAPH_CHECKPOINT_ENABLED` and `LANGGRAPH_CHECKPOINT_PATH` environment variables.
- Added pytest coverage for checkpoint resource creation and graph checkpointer wiring.

### Phase 9: Structured Log Redaction

- Added recursive redaction for structured log field values.
- Redacts common email addresses, mainland China mobile numbers, Bearer tokens, `api_key/token/secret/password` assignments, and `sk-...` style secret values before JSON logs are emitted.
- Keeps top-level sensitive fields such as `query`, `prompt`, `api_key`, `token`, `password`, and `secret` out of logs entirely.
- Added pytest coverage for PII and secret redaction in allowed string fields and nested structures.

### Phase 10: Backend Deployment Readiness

- Added `Dockerfile.backend` for a containerized FastAPI backend runtime.
- Added `.dockerignore` to keep secrets, virtual environments, node modules, caches, logs, and local data out of Docker build context.
- Added `infra/docker-compose.enterprise.yml` as a backend compose override on top of the existing data-service stack.
- Added `cloud_agent/agent/.env.container.example` with container service hostnames for Redis, MySQL, Milvus, Neo4j, and host Ollama access.
- Added `docs/deployment.md` with internal-pilot startup, health-check, shutdown, and current-limit notes.
- Added pytest coverage for deployment artifacts and required safety defaults.

### Phase 11: Runtime Guardrails

- Added an in-process per-user chat rate limiter for local and small internal pilots.
- `/api/chat` now returns a stable `429` JSON error with `Retry-After` when a user exceeds the configured request window.
- Added a configurable LangGraph workflow timeout using `CHAT_WORKFLOW_TIMEOUT_SECONDS`.
- Timeout failures now return stable SSE `WORKFLOW_TIMEOUT` errors and failed-request metrics instead of hanging indefinitely.
- Added container env defaults for `CHAT_RATE_LIMIT`, `CHAT_RATE_LIMIT_WINDOW_SECONDS`, and `CHAT_WORKFLOW_TIMEOUT_SECONDS`.
- Added pytest coverage for rate-limiter behavior, chat-route limiting, timeout classification, and timeout SSE responses.

## Verification Commands

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode static
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode route
```

## Remaining Enterprise Gaps

- No real authentication or tenant management yet.
- No hosted tracing system such as LangFuse or OpenTelemetry yet.
- Metrics are in-process only; they reset when the backend process restarts.
- Error classification is still lightweight and should later be expanded with typed exception classes.
- Security guard is rule-based and should later be paired with model-based guardrails for broader prompt-injection coverage.
- Authentication is demo-token based only; production auth/OAuth/JWT verification is still future work.
- SQLite checkpoints are local-process persistence; production deployment should move to Postgres or managed checkpointer.
- Log redaction is rule-based and should later be paired with centralized audit logging and configurable data-classification policy.
- Backend Docker deployment is now scaffolded, but a real production release still needs image build verification in CI, secret management, TLS, ingress, and resource limits.
- Rate limiting is in-process only; multi-replica deployment should move the counters to Redis or an API gateway.
- Some CLI/demo scripts still use `print()` intentionally for interactive teaching output.
