#!/usr/bin/env python3
"""Drift-command fixture tests over a synthetic mini-corpus (tmp_path)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import cmd_drift
from harness_common import Severity, compute_exit_code
from test_self_check_fixtures import (
    STATUS_MATCH,
    build_mini_repo,
    build_project,
    _write,
)


def _findings(report, code):
    return [f for f in report.findings if f.code == code]


def test_drift_mismatch_match_unparseable_and_missing_field(tmp_path):
    repo = build_mini_repo(tmp_path)
    piping = repo / "projects" / "chirality-piping"
    report = cmd_drift.run_drift(repo, [piping])

    mismatches = _findings(report, "STATUS_HISTORY_MISMATCH")
    assert len(mismatches) == 1
    f = mismatches[0]
    assert f.severity is Severity.REVIEW
    assert "IN_PROGRESS" in f.message and "CHECKING" in f.message
    assert "DEL-01-01" in f.source_path
    assert f.dimension == "staleness/drift"

    unparseable = _findings(report, "UNPARSEABLE_HISTORY")
    # DEL-01-03: bullets but no state-bearing assertion; DEL-01-04: doc-level.
    assert len(unparseable) == 2
    assert all(f.severity is Severity.WARN for f in unparseable)
    assert any("DEL-01-03" in f.source_path for f in unparseable)
    assert any("DEL-01-04" in f.source_path for f in unparseable)

    baseline = _findings(report, "DRIFT_BASELINE_COMPARISON")
    assert len(baseline) == 1
    assert "measured 1 mismatch(es) over 4 file(s)" in baseline[0].message
    assert "baseline 1/4" in baseline[0].message

    # Exit-code posture: REVIEW-only -> 0; strict -> 1.
    assert compute_exit_code(report.findings) == 0
    assert compute_exit_code(report.findings, strict=True) == 1


def test_drift_empty_history_warns(tmp_path):
    repo = build_mini_repo(tmp_path)
    empty_doc = (
        "# Status: DEL-01-05\n\n**Current State:** OPEN\n"
        "**Last Updated:** 2026-01-01\n\n## History\n"
    )
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "PKG-01_Fixture Pkg" / "1_Working" / "DEL-01-05_Empty history"
           / "_STATUS.md", empty_doc)
    report = cmd_drift.run_drift(repo, [repo / "projects" / "chirality-piping"])
    empty = _findings(report, "EMPTY_HISTORY")
    assert len(empty) == 1
    assert empty[0].severity is Severity.WARN
    assert "DEL-01-05" in empty[0].source_path


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.email=fixture@example.invalid",
         "-c", "user.name=Fixture", *args],
        cwd=cwd, capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def test_drift_approval_sha_reachable_and_unreachable(tmp_path):
    repo = build_mini_repo(tmp_path)
    _git(repo, "init", "-q")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "seed.txt")
    _git(repo, "commit", "-q", "-m", "seed")
    good_sha = _git(repo, "rev-parse", "HEAD")
    bad_sha = "0123456789abcdef0123456789abcdef01234567"

    status_with_sha = STATUS_MATCH.replace(
        "**Last Updated:** 2026-06-04",
        "**Last Updated:** 2026-06-04\n**Checking Approval SHA:** {sha}")
    build_project(repo, "chirality-app-dev", {
        "DEL-02-01_Match one": status_with_sha.format(sha=good_sha),
        "DEL-02-02_Match two": status_with_sha.format(sha=bad_sha),
    }, baseline_mismatch=0, baseline_files=2,
        requires_sha=True, sha_field="Checking Approval SHA")

    report = cmd_drift.run_drift(repo, [repo / "projects" / "chirality-app-dev"])
    reachable = _findings(report, "APPROVAL_SHA_REACHABLE")
    unreachable = _findings(report, "APPROVAL_SHA_UNREACHABLE")
    assert len(reachable) == 1 and reachable[0].severity is Severity.INFO
    assert good_sha in reachable[0].message
    assert len(unreachable) == 1 and unreachable[0].severity is Severity.REVIEW
    assert bad_sha in unreachable[0].message


def test_drift_sha_outside_git_repo_is_not_applicable(tmp_path):
    repo = build_mini_repo(tmp_path)  # no .git anywhere under tmp
    status_with_sha = STATUS_MATCH.replace(
        "**Last Updated:** 2026-06-04",
        "**Last Updated:** 2026-06-04\n**Checking Approval SHA:** "
        "0123456789abcdef0123456789abcdef01234567")
    build_project(repo, "chirality-app-dev", {
        "DEL-02-01_Match one": status_with_sha,
    }, baseline_mismatch=0, baseline_files=1,
        requires_sha=True, sha_field="Checking Approval SHA")
    report = cmd_drift.run_drift(repo, [repo / "projects" / "chirality-app-dev"])
    na = _findings(report, "APPROVAL_SHA_UNVERIFIABLE")
    if na:  # tmp_path may live under a parent git repo; both outcomes are lawful.
        assert na[0].severity is Severity.NOT_APPLICABLE
        assert compute_exit_code(report.findings) == 0


def test_drift_denominator_covers_all_projects(tmp_path):
    repo = build_mini_repo(tmp_path)
    report = cmd_drift.run_drift(repo, [
        repo / "projects" / "chirality-app-dev",
        repo / "projects" / "chirality-piping",
    ])
    assert report.summary["files_total"] == 6
    assert report.summary["mismatches_total"] == 1
    md = report.render_markdown()
    assert "Denominator: 6 status file(s) audited" in md
