from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def test_backend_dockerfile_has_runtime_safety_defaults():
    content = read_text("Dockerfile.backend")

    assert "FROM python:3.11-slim" in content
    assert "cloud_agent/agent/requirements.txt" in content
    assert "COPY run_backend.py" in content
    assert "COPY cloud_agent" in content
    assert "USER cloudagent" in content
    assert "EXPOSE 5000" in content
    assert "HEALTHCHECK" in content
    assert "/api/health" in content
    assert 'CMD ["python", "run_backend.py"]' in content


def test_dockerignore_keeps_secrets_and_heavy_artifacts_out_of_image_context():
    content = read_text(".dockerignore")

    required_patterns = [
        ".env",
        ".env.*",
        ".venv/",
        "node_modules/",
        "data/",
        "*.sqlite",
        "*.db",
        ".git/",
    ]

    for pattern in required_patterns:
        assert pattern in content


def test_enterprise_compose_adds_backend_without_replacing_data_services():
    content = read_text("infra/docker-compose.enterprise.yml")

    assert "backend:" in content
    assert "dockerfile: Dockerfile.backend" in content
    assert "../cloud_agent/agent/.env.container.example" in content
    assert "../cloud_agent/agent/.env.container" in content
    assert "required: false" in content
    assert "cloudagent-backend" in content
    assert '"5000:5000"' in content
    assert "backend_data:" in content
    assert "redis:" in content
    assert "mysql:" in content
    assert "milvus:" in content
    assert "neo4j:" in content
    assert "host.docker.internal:host-gateway" in content


def test_container_env_example_uses_container_service_hostnames():
    content = read_text("cloud_agent/agent/.env.container.example")
    gitignore = read_text(".gitignore")

    assert "BASE_URL=http://host.docker.internal:11434/v1" in content
    assert "REDIS_URL=redis://redis:6379" in content
    assert "MYSQL_HOST=mysql" in content
    assert "NEO4J_URI=bolt://neo4j:7687" in content
    assert "MILVUS_HOST=milvus" in content
    assert "LANGGRAPH_CHECKPOINT_PATH=/app/data/langgraph_checkpoints.sqlite" in content
    assert "CHAT_RATE_LIMIT=60" in content
    assert "CHAT_RATE_LIMIT_WINDOW_SECONDS=60" in content
    assert "CHAT_WORKFLOW_TIMEOUT_SECONDS=45" in content
    assert "!cloud_agent/agent/.env.container.example" in gitignore


def test_deployment_doc_contains_copy_build_and_healthcheck_commands():
    content = read_text("docs/deployment.md")

    assert "Copy-Item cloud_agent\\agent\\.env.container.example cloud_agent\\agent\\.env.container" in content
    assert "docker compose -f infra/docker-compose.yml -f infra/docker-compose.enterprise.yml up -d --build" in content
    assert "http://127.0.0.1:5000/api/health" in content
    assert "internal pilot" in content
