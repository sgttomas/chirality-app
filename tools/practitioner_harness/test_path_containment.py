#!/usr/bin/env python3
"""Containment tests for `ensure_generated_scope` (D-GOV-01 / K-WRITE-2)."""

from __future__ import annotations

from pathlib import Path

import pytest

import harness
from harness_common import (
    GENERATED_ROOT_NAME,
    GeneratedScopeError,
    ensure_generated_scope,
)
from test_self_check_fixtures import build_mini_repo


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / GENERATED_ROOT_NAME).mkdir(parents=True, exist_ok=True)
    return repo


def test_absolute_path_outside_refused(tmp_path):
    repo = _repo(tmp_path)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope(Path("/etc/x.json"), repo)


def test_dotdot_traversal_refused(tmp_path):
    repo = _repo(tmp_path)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope("../escape.md", repo)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope(
            repo / GENERATED_ROOT_NAME / ".." / ".." / "escape.md", repo)


def test_symlink_inside_out_dir_pointing_outside_refused(tmp_path):
    repo = _repo(tmp_path)
    outside = tmp_path / "outside_dir"
    outside.mkdir()
    link = repo / GENERATED_ROOT_NAME / "link"
    link.symlink_to(outside)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope(link / "f.md", repo)


def test_case_variant_prefix_spoof_refused(tmp_path):
    repo = _repo(tmp_path)
    spoof = str(repo / GENERATED_ROOT_NAME.upper() / "x.md")
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope(spoof, repo)


def test_sibling_prefix_spoof_refused(tmp_path):
    repo = _repo(tmp_path)
    spoof = str(repo / (GENERATED_ROOT_NAME + "_evil") / "x.md")
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope(spoof, repo)


def test_legit_nested_path_allowed(tmp_path):
    repo = _repo(tmp_path)
    resolved = ensure_generated_scope("briefs/nested/deep/x.md", repo)
    assert str(resolved).startswith(str((repo / GENERATED_ROOT_NAME).resolve()))
    resolved2 = ensure_generated_scope(
        repo / GENERATED_ROOT_NAME / "reports" / "y.json", repo)
    assert resolved2.name == "y.json"


def test_cli_json_report_outside_generated_root_exits_2(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    rc = harness.main([
        "--repo-root", str(repo), "--json-report", "/etc/x.json", "self-check"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "generated root" in err


def test_cli_json_report_inside_generated_root_succeeds(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    target = repo / GENERATED_ROOT_NAME / "reports" / "sc.json"
    rc = harness.main([
        "--repo-root", str(repo), "--json-report", str(target), "self-check"])
    assert rc == 0
    assert target.is_file()
    assert '"authority_class": "generated_view"' in target.read_text(encoding="utf-8")
    capsys.readouterr()


def test_writes_never_land_outside_generated_root(tmp_path):
    repo = build_mini_repo(tmp_path)
    before = {p for p in repo.rglob("*") if p.is_file()}
    rc = harness.main([
        "--repo-root", str(repo),
        "--json-report", str(repo / GENERATED_ROOT_NAME / "d.json"),
        "drift", "--all"])
    assert rc == 0
    after = {p for p in repo.rglob("*") if p.is_file()}
    new = after - before
    gen_root = (repo / GENERATED_ROOT_NAME).resolve()
    for p in new:
        assert gen_root in p.resolve().parents, f"write escaped: {p}"
    # os-level scan of tmp outside repo too
    stray = [p for p in tmp_path.rglob("*")
             if p.is_file() and repo not in p.parents]
    assert stray == []


def test_generated_root_symlink_to_outside_repo_refused(tmp_path):
    """Regression: `_harness_generated` itself as a symlink must not relocate
    the containment boundary outside the repo (adversarial-review finding)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    exfil = tmp_path / "EXFIL"
    exfil.mkdir()
    (repo / GENERATED_ROOT_NAME).symlink_to(exfil)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope("pwned.json", repo)
    assert list(exfil.iterdir()) == []


def test_generated_root_symlink_into_governed_tree_refused(tmp_path):
    """A symlinked generated root pointing INSIDE the repo (at a governed
    tree) must be refused too — containment is not just repo-containment."""
    repo = tmp_path / "repo"
    governed = repo / "docs"
    governed.mkdir(parents=True)
    (repo / GENERATED_ROOT_NAME).symlink_to(governed)
    with pytest.raises(GeneratedScopeError):
        ensure_generated_scope("report.json", repo)
    assert list(governed.iterdir()) == []


def test_generated_root_symlink_cli_exits_2(tmp_path):
    repo = build_mini_repo(tmp_path)
    gen = repo / GENERATED_ROOT_NAME
    if gen.exists():
        import shutil
        shutil.rmtree(gen)
    exfil = tmp_path / "EXFIL_CLI"
    exfil.mkdir()
    gen.symlink_to(exfil)
    rc = harness.main([
        "--repo-root", str(repo),
        "--json-report", "escape.json",
        "self-check"])
    assert rc == 2
    assert list(exfil.iterdir()) == []
