from __future__ import annotations

import run_infra


def test_build_compose_command_uses_project_infra_compose_file():
    command = run_infra.build_compose_command("docker")

    assert command == ["docker", "compose", "up", "-d"]


def test_main_explains_missing_docker_in_chinese(monkeypatch, capsys):
    monkeypatch.setattr(run_infra, "find_docker", lambda: None)

    exit_code = run_infra.main(["--check-only"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "没有找到 Docker 命令" in output
    assert "Docker Desktop" in output
