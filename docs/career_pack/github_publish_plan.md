# GitHub Publish Plan

## Current Situation

Original repository:

```text
https://github.com/zihang3417-sys/cloudagent
```

Local enterprise copy:

```text
F:\agent0520\cloudagent_enterprise
```

The enterprise copy currently points to the same remote:

```text
origin https://github.com/zihang3417-sys/cloudagent.git
```

## Recommended Strategy

Use the original GitHub repository as the public-facing project, but preserve
the old learning prototype as a branch or tag.

Recommended layout:

```text
main                 -> enterprise/refactored version
learning-prototype   -> original learning version
enterprise-baseline  -> optional tag after final verification
```

Why this is recommended:

- Your resume can keep one clean GitHub URL.
- Recruiters see the strongest version first.
- The original project is not deleted; it becomes the learning/prototype branch.
- The commit history tells a credible story: toy prototype -> enterprise MVP.

## Safer Alternative

Create a new repository:

```text
cloudagent-enterprise
```

Use this if you want to avoid overwriting the old repository's `main` branch.

Tradeoff:

- Cleaner separation.
- But the resume has two project URLs, which is less focused.

## Suggested Push Flow

Do this only after verifying both folders are clean and the old repository is
backed up.

### 1. In original project, create backup branch

```powershell
cd F:\agent0520\cloudagent
git status
git branch learning-prototype
git push origin learning-prototype
```

### 2. In enterprise project, confirm final verification

```powershell
cd F:\agent0520\cloudagent_enterprise
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode static
.\.venv\Scripts\python.exe cloud_agent\evals\run_eval.py --mode route
docker compose -f infra\docker-compose.yml -f infra\docker-compose.enterprise.yml config --quiet
```

### 3. Push enterprise copy to main

```powershell
cd F:\agent0520\cloudagent_enterprise
git status
git push origin main
```

If Git refuses because remote history differs, stop and inspect first. Do not
force-push until the backup branch has been verified on GitHub.

### 4. Optional tag

```powershell
git tag enterprise-mvp-v1
git push origin enterprise-mvp-v1
```

## README Front Page Recommendation

The public README should start with:

```text
CloudAgent Enterprise is a cloud-platform AI assistant MVP for internal pilot
scenarios. It combines FastAPI, Vue3, LangGraph multi-agent orchestration,
MCP-style business tools, RAG/GraphRAG, memory, semantic cache, observability,
security guardrails, and deployment-readiness scaffolding.
```

Then show:

1. What it does.
2. Architecture diagram.
3. Quick start.
4. Demo questions.
5. Enterprise trust features.
6. Current limits.

## What Not To Publish

Do not publish:

- `.env`
- `.env.container`
- `.venv/`
- `node_modules/`
- `data/`
- SQLite checkpoint files
- API keys
- local IDE config

The current `.gitignore` and `.dockerignore` already cover these categories,
but check `git status --short` before pushing.
