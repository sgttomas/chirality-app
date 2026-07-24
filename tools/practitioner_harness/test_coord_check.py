#!/usr/bin/env python3
"""coord-check fixture tests.

HB-10 fixture note: all machine-absolute content is re-anchored to the
synthetic `/Users/fixture/...` prefix and lives as string constants inside
this `test_`-prefixed module (the export-boundary idiom of
`test_abs_path_lint_fixtures.py`; never loose data files under `tools/`).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import cmd_coord_check
import harness
from harness_common import GENERATED_ROOT_NAME, Report, Severity, find_claim_language
from test_brief_adoption import _git
from test_self_check_fixtures import _write

requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    _write(repo / ".gitignore", GENERATED_ROOT_NAME + "/\n")
    _write(repo / "_DomainEngines" / "bridge" / "existing.md",
           "# Existing bridge artifact\n")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "_REGISTER.md",
           "# Register\n\n| ID | Decision | State |\n|---|---|---|\n"
           "| D-31 | Fixture packet | RULED |\n")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    return repo


def _codes(report):
    return {f.code for f in report.findings}


@requires_git
def test_coord_check_clean_packet_with_register_precedent_and_resolved_ref(tmp_path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "D-31_fixture_packet.md",
           "# D-31 fixture packet\n\n"
           "Precedent: D-28 packet skeleton.\n\n"
           "Source: `_DomainEngines/bridge/existing.md`\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "packet")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert report.findings == []
    assert report.summary["coordination_paths"] == 1
    assert report.extras["coord_check"]["coordination_paths"][0]["path"].endswith(
        "D-31_fixture_packet.md")


@requires_git
def test_coord_check_flags_missing_ref_register_row_and_precedent(tmp_path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "D-32_missing_packet.md",
           "# D-32 missing packet\n\n"
           "Source: `_DomainEngines/bridge/missing.md`\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "bad packet")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert _codes(report) == {
        "COORD_UNRESOLVED_REF",
        "COORD_REGISTER_ROW_MISSING",
        "COORD_PRECEDENT_NOT_NAMED",
    }
    assert all(f.severity is Severity.REVIEW for f in report.findings)


@requires_git
def test_coord_check_generated_root_ref_is_info_and_cli_wired(tmp_path, capsys):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "_DomainEngines" / "bridge" / "CHANGE_PREP_fixture.md",
           "# CHANGE prep fixture\n\n"
           "Precedent: framework-maintenance pattern.\n\n"
           "Evidence: `_harness_generated/evidence/fixture.json`\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "change prep")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    hits = [f for f in report.findings if f.code == "COORD_GENERATED_REF_ABSENT"]
    assert len(hits) == 1
    assert hits[0].severity is Severity.INFO
    rc = harness.main([
        "--repo-root", str(repo), "coord-check", "--diff", f"{base}..HEAD"])
    assert rc == 0
    assert "COORD_GENERATED_REF_ABSENT" in capsys.readouterr().out


# --- HB-10 diff-added machine-absolute-path check (SPEC §0.2.4) -------------------

FIXTURE_ABS = "/Users/fixture/ai-env/projects"

D05B_RELPATH = ("projects/chirality-piping/execution/_Coordination/"
                "_DECISIONS/D-05b_public_export_ci_activation.md")

# The D-05b:54 hunk shape (2026-07-04, commit a7e554d3a; fixed a605f1b37),
# re-anchored to the synthetic fixture prefix: a decision-packet table row
# quoting a machine-absolute path verbatim lands at new-file line 54. The
# abs-path-bearing CONTEXT line above and REMOVED line in the same hunk must
# never fire — only the ADDED line may.
D05B_FIXTURE_DIFF = (
    f"diff --git a/{D05B_RELPATH} b/{D05B_RELPATH}\n"
    "index b997d6384..336b20902 100644\n"
    f"--- a/{D05B_RELPATH}\n"
    f"+++ b/{D05B_RELPATH}\n"
    "@@ -53,3 +53,3 @@ All paths below are relative to "
    "`projects/chirality-piping/`\n"
    f" | Context row | path {FIXTURE_ABS}/context-only is not added |\n"
    f"-| Old row | path {FIXTURE_ABS}/removed-only goes away |\n"
    "+| No public OpenPipeStress repo exists | `{REPO_ROOT}/exports/"
    "README.md:5`: \"The real public repository remains "
    f"`{FIXTURE_ABS}/chirality-app`\" — a public surface for the tier-0 "
    "chirality-app, not for OpenPipeStress. |\n"
    " | Next row | unchanged |\n"
)


def test_parse_added_lines_reproduces_d05b_hunk_and_check_fires():
    added = cmd_coord_check._parse_added_lines(D05B_FIXTURE_DIFF)
    # Exactly the one ADDED line, numbered against the NEW file (D-05b:54);
    # the +++ header, context, and removed lines yield nothing.
    assert [line_no for line_no, _ in added] == [54]
    assert added[0][1].startswith("| No public OpenPipeStress repo exists")

    report = Report(command="coord-check")
    assert cmd_coord_check._check_added_abs_paths(
        report, Path.cwd(), D05B_RELPATH, added) == 1
    f = report.findings[0]
    assert f.code == "COORD_ABS_PATH_ADDED"
    assert f.severity is Severity.REVIEW
    assert (f.source_path, f.source_line) == (D05B_RELPATH, 54)
    assert f.invariant == "SPEC-0.2.4"
    assert "actionable by default" in f.message
    assert find_claim_language(f.message) == []

    # The same added lines on an evidence-class relpath are exempt (evidence
    # artifacts lawfully carry absolute paths per SPEC §0.2.4).
    evidence = Report(command="coord-check")
    assert cmd_coord_check._check_added_abs_paths(
        evidence, Path.cwd(), "projects/chirality-piping/execution/_Coordination/"
        "_run_records/run_2026-07-04.md", added) == 0
    assert evidence.findings == []


@requires_git
def test_coord_check_flags_added_machine_absolute_path_line(tmp_path, capsys):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "D-31_fixture_packet.md",
           "# D-31 fixture packet\n\n"
           "Precedent: D-28 packet skeleton.\n\n"
           "Source: `_DomainEngines/bridge/existing.md`\n\n"
           f"Worktree anchor: {FIXTURE_ABS}/worktree — machine-local.\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "packet with anchor")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert _codes(report) == {"COORD_ABS_PATH_ADDED"}
    f = report.findings[0]
    assert f.severity is Severity.REVIEW
    assert f.source_line == 7
    row = report.extras["coord_check"]["coordination_paths"][0]
    assert row["abs_path_findings"] == 1
    rc = harness.main([
        "--repo-root", str(repo), "coord-check", "--diff", f"{base}..HEAD"])
    assert rc == 0  # REVIEW never gates by default (D-GOV-02)
    assert "COORD_ABS_PATH_ADDED" in capsys.readouterr().out


@requires_git
def test_coord_check_added_repo_relative_and_boundary_lines_do_not_fire(tmp_path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "D-31_fixture_packet.md",
           "# D-31 fixture packet\n\n"
           "Precedent: D-28 packet skeleton.\n\n"
           "Source: `_DomainEngines/bridge/existing.md`\n\n"
           "Repo-relative anchor: projects/chirality-piping/execution/x.md\n"
           "Placeholder anchor: {REPO_ROOT}/exports/README.md\n"
           "Boundary prose: /Usersfoo/nope is not a machine root.\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "packet with relative anchors")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert report.findings == []
    row = report.extras["coord_check"]["coordination_paths"][0]
    assert row["abs_path_findings"] == 0


@requires_git
def test_coord_check_evidence_class_added_line_is_exempt(tmp_path):
    repo = _repo(tmp_path)
    base = _git(repo, "rev-parse", "HEAD")
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_run_records" / "run_2026-07-04.md",
           "# Run record (fixture evidence)\n\n"
           f"Executed from {FIXTURE_ABS}/worktree at 2026-07-04.\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "run record")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert report.findings == []
    row = report.extras["coord_check"]["coordination_paths"][0]
    assert row["path"].endswith("_run_records/run_2026-07-04.md")
    assert row["abs_path_findings"] == 0


@requires_git
def test_coord_check_removed_abs_path_line_does_not_fire(tmp_path):
    repo = _repo(tmp_path)
    packet = (repo / "projects" / "chirality-piping" / "execution"
              / "_Coordination" / "_DECISIONS" / "D-31_fixture_packet.md")
    _write(packet,
           "# D-31 fixture packet\n\n"
           "Precedent: D-28 packet skeleton.\n\n"
           f"Worktree anchor: {FIXTURE_ABS}/worktree — machine-local.\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "packet with anchor committed earlier")
    base = _git(repo, "rev-parse", "HEAD")
    _write(packet,
           "# D-31 fixture packet\n\n"
           "Precedent: D-28 packet skeleton.\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "anchor removed")

    report = cmd_coord_check.run_coord_check(repo, f"{base}..HEAD")

    assert report.findings == []
    row = report.extras["coord_check"]["coordination_paths"][0]
    assert row["abs_path_findings"] == 0
