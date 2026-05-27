from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT_DIR / relative_path).read_text(encoding="utf-8")


def test_project_handoff_document_separates_claims_from_limits():
    content = read_text("docs/project_handoff.md")

    required_sections = [
        "## 项目定位",
        "## 已确认实现的能力",
        "## 简历安全写法",
        "## 面试讲述路径",
        "## 暂时不要这样说",
        "## 下一步建议",
    ]

    for section in required_sections:
        assert section in content


def test_project_handoff_contains_enterprise_boundaries():
    content = read_text("docs/project_handoff.md")

    required_phrases = [
        "内部 AI 助手试点",
        "不是公网 SaaS 生产平台",
        "demo-token based",
        "SQLite checkpoint",
        "in-process metrics",
        "in-process rate limiting",
        "JWT/OAuth",
        "Postgres",
        "LangFuse or OpenTelemetry",
    ]

    for phrase in required_phrases:
        assert phrase in content


def test_progress_records_career_handoff_phase():
    content = read_text("docs/codex-plans/enterprise-trust-foundation/progress.md")

    assert "Phase 13: Career Handoff" in content
    assert "docs/project_handoff.md" in content
