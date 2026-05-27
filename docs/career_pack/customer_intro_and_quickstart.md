# CloudAgent Enterprise Customer Introduction

## Customer-Friendly Summary

CloudAgent Enterprise is an internal AI assistant MVP for cloud-service teams.
It helps users ask natural-language questions about orders, cloud instances,
product knowledge, cost optimization, and promotion materials.

Instead of being a simple chatbot, it combines:

- A web chat interface.
- A FastAPI streaming backend.
- LangGraph multi-agent orchestration.
- Specialist agents for billing, product Q&A, recommendation, promotion, and
  FinOps.
- Business tools for querying demo orders, instances, monitoring data, products,
  and promotion materials.
- Milvus RAG for document knowledge.
- Neo4j GraphRAG for structured product/spec relationships.
- Redis and Milvus memory/cache components.
- Observability, security, eval, and deployment-readiness scaffolding.

## What A Customer Can Do

A user can ask:

```text
Help me check my recent orders.
Show my running cloud instances.
What is VPC?
My server utilization is low. How can I reduce cost?
I run Java API service + MySQL. Is 2C4G enough?
How many elastic network interfaces does ecs.g8a.xlarge support?
```

The system routes each question to the proper specialist agent, calls tools or
knowledge bases when needed, and streams the answer back to the browser.

## Simple Mental Model

```text
User question
-> Web chat
-> FastAPI /api/chat
-> demo auth boundary
-> rate limiter
-> input security guard
-> semantic cache
-> memory context
-> LangGraph orchestrator
-> specialist agent
-> business tool / RAG / GraphRAG
-> streaming answer
-> metrics and structured logs
```

## Current Startup Options

### Option A: Learning-Friendly Local Demo

Use this for PyCharm/local learning.

```powershell
cd F:\agent0520\cloudagent_enterprise
Copy-Item cloud_agent\agent\.env.full_demo.example cloud_agent\agent\.env
# Fill DASHSCOPE_API_KEY in cloud_agent\agent\.env

cd infra
docker compose up -d
cd ..

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r cloud_agent\agent\requirements.txt

cd cloud_agent\front\cloud_agent
npm install
cd ..\..\..
```

Initialize demo data:

```powershell
docker exec -i cloudagent-mysql mysql -uroot -pRootPass123! cloud_platform < cloud_agent\agent\database\init_mock_data.sql
.\.venv\Scripts\python.exe cloud_agent\agent\test\milvus_rag.py --ingest --data-dir cloud_agent\mock_data --query "什么是VPC？"
.\.venv\Scripts\python.exe cloud_agent\app\preload_cache.py
.\.venv\Scripts\python.exe cloud_agent\agent\test\import_kg_jsons.py --clear
```

Check the environment:

```powershell
.\.venv\Scripts\python.exe check_full_demo.py
```

Start backend:

```powershell
.\.venv\Scripts\python.exe run_backend.py
```

Start frontend:

```powershell
.\.venv\Scripts\python.exe run_frontend.py
```

### Option B: Enterprise Backend Container Profile

Use this to validate the backend deployment skeleton.

```powershell
cd F:\agent0520\cloudagent_enterprise
Copy-Item cloud_agent\agent\.env.container.example cloud_agent\agent\.env.container
# Fill DASHSCOPE_API_KEY in cloud_agent\agent\.env.container

docker compose -f infra\docker-compose.yml -f infra\docker-compose.enterprise.yml up -d --build
```

Health checks:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
Invoke-RestMethod http://127.0.0.1:5000/api/ready
```

## Recommended One-Click Experience

The project already has:

- `check_full_demo.py`
- `run_backend.py`
- `run_frontend.py`

For GitHub polish, add three PowerShell wrappers next:

```text
scripts/setup_demo.ps1        -> install dependencies and copy env example
scripts/init_demo_data.ps1    -> import MySQL, Milvus, cache, and Neo4j demo data
scripts/start_demo.ps1        -> start Docker services, backend, and frontend
```

This keeps the Python scripts PyCharm-friendly while giving GitHub visitors a
single command path.

Recommended README quick start:

```powershell
.\scripts\setup_demo.ps1
.\scripts\init_demo_data.ps1
.\scripts\start_demo.ps1
```

## Honest Customer Boundary

This is suitable for:

- Internal pilot.
- Resume demo.
- Small-team AI assistant prototype.
- Local reproducible demo.

It is not yet:

- Public SaaS production.
- Real OAuth/JWT multi-tenant system.
- Distributed observability platform.
- Distributed rate-limited deployment.
- Production secret-management solution.
