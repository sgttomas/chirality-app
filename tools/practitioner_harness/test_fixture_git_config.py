#!/usr/bin/env python3
"""Regression coverage for quiescent Git-backed fixture templates."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

import harness_template_cache


requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _assert_auto_maintenance_disabled(repo: Path) -> None:
    assert _git(repo, "config", "--get", "maintenance.auto") == "false"
    assert _git(repo, "config", "--get", "gc.auto") == "0"
    assert _git(repo, "config", "--get", "gc.autoDetach") == "false"


@requires_git
def test_cached_fixture_repo_disables_automatic_git_maintenance(tmp_path: Path):
    """Every fixture Git subprocess inherits the quiescence configuration."""

    def _build(repo: Path) -> None:
        repo.mkdir(parents=True)
        _git(repo, "init", "-q")
        _assert_auto_maintenance_disabled(repo)
        (repo / "fixture.txt").write_text("fixture\n", encoding="utf-8")
        _git(repo, "add", "fixture.txt")
        _git(
            repo,
            "-c", "user.name=Fixture",
            "-c", "user.email=fixture@example.invalid",
            "commit", "-qm", "fixture",
        )
        _assert_auto_maintenance_disabled(repo)

    repo = harness_template_cache.materialize(
        ("fixture_git_config_regression",),
        _build,
        tmp_path / "repo",
    )

    _assert_auto_maintenance_disabled(repo)
