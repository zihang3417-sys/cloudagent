# CloudAgent Deployment Readiness

This guide is for a local or small-company internal pilot. It is not a public
SaaS production runbook yet.

## Scope

The enterprise compose stack adds a containerized FastAPI backend on top of the
existing infrastructure services:

- MySQL for demo business data.
- Redis for short-term memory and semantic cache support.
- Milvus, etcd, and MinIO for vector retrieval.
- Neo4j for GraphRAG.
- CloudAgent backend on port `5000`.

Ollama still runs on the host machine. The backend container reaches it through
`host.docker.internal`.

## Prepare Environment

```powershell
Copy-Item cloud_agent\agent\.env.container.example cloud_agent\agent\.env.container
```

Edit `cloud_agent\agent\.env.container` and fill:

```text
DASHSCOPE_API_KEY=your_dashscope_api_key
```

Keep `.env.container` local. It is ignored by Git.

The compose file loads `.env.container.example` first so the stack can be
validated with `docker compose config`. Your local `.env.container` is loaded
after it and overrides the placeholder values.

## Start Stack

```powershell
docker compose -f infra/docker-compose.yml -f infra/docker-compose.enterprise.yml up -d --build
```

The first start can take a while because Milvus and the backend image both need
to initialize.

## Health Check

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
Invoke-RestMethod http://127.0.0.1:5000/api/ready
```

The backend Dockerfile also includes a container healthcheck against:

```text
http://127.0.0.1:5000/api/health
```

## Stop Stack

```powershell
docker compose -f infra/docker-compose.yml -f infra/docker-compose.enterprise.yml down
```

Add `-v` only when you intentionally want to delete local Docker volumes.

## Current Limits

- Demo auth is still token-based, not real OAuth/JWT.
- SQLite checkpoint persistence is stored in the backend container volume.
- In-process metrics reset when the backend container restarts.
- This profile is suitable for an internal pilot, not for internet-facing
  multi-tenant production traffic.
