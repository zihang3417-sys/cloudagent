from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def test_ci_validates_enterprise_compose_configuration():
    content = read_text(".github/workflows/ci.yml")

    assert "Validate enterprise compose config" in content
    assert "docker compose -f infra/docker-compose.yml -f infra/docker-compose.enterprise.yml config --quiet" in content


def test_progress_lists_deployment_gate_verification_command():
    content = read_text("docs/codex-plans/enterprise-trust-foundation/progress.md")

    assert "docker compose -f infra\\docker-compose.yml -f infra\\docker-compose.enterprise.yml config --quiet" in content
    assert "Phase 12: Release Gate" in content
