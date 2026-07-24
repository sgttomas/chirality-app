#!/usr/bin/env python3
"""GEN-8 project-tree machine-absolute-path lint tests (SPEC §0.2.4).

Plan-of-record basis: plan v3 parked-findings row "Machine-absolute-path
lint — Now — Folded into self-check; detect, never rewrite"; audit basis:
`plans/consistency_audit_2026-07-01.md` §4 item 6 (~82 instruction/plan
files carry machine-absolute paths; worst: the app-dev pi-assessment
cluster) and §6 item 5 (relativization when files are next touched).

All machine-absolute fixture content is re-anchored to the synthetic
`/Users/fixture/...` prefix and lives as string constants INSIDE this
`test_`-prefixed module (never loose data files under `tools/`), the same
export-boundary idiom as `test_archive_fixture_corpus.py`.

Severity per TYPES.md §11 / D-GOV-02: REVIEW, one finding per FILE (the
worst live file carries 21 hit lines; per-line findings would flood human
triage). Evidence-marker and unclassified files are counted as facts, never
findings. BLOCK is never emitted by this check's own severity design
(detect, never rewrite; relativization is a human disposition) — SPEC
§0.2.4 itself is RATIFIED (docs/ owner ratification 2026-07-11).
"""

from __future__ import annotations

import shutil
import subprocess

import pytest

from harness_common import Severity, find_claim_language
from test_self_check_fixtures import _findings, _has, _write, build_mini_repo

import cmd_self_check

# --- Fixture material (synthetic /Users/fixture prefix) --------------------------

FIXTURE_ABS = "/Users/fixture/ai-env/projects/example"

PLAN_THREE_HITS_MD = f"""# Fixture assessment plan

Working notes anchored at {FIXTURE_ABS}/notes.md — machine-local anchor.

Repo-relative prose between the hits (must not count).

Second anchor: {FIXTURE_ABS}/plans/other_assessment.md
Third anchor: {FIXTURE_ABS}/execution/run_output.log
"""
PLAN_HIT_LINES = (3, 7, 8)  # ABS_PATH_RE hit lines in the constant above

DECISION_ONE_HIT_MD = f"""# D-99 — fixture ruling record

**Context:** session ran from {FIXTURE_ABS}/worktree — machine-local anchor.
"""

STATUS_ONE_HIT_MD = f"""# Status: DEL-09-01

**Current State:** OPEN
**Working copy:** {FIXTURE_ABS}/execution/DEL-09-01

## History
- 2026-06-30 - State set to OPEN (PREPARATION)
"""

RUN_RECORD_TWO_HITS_MD = f"""# Run record (fixture evidence)

Executed: {FIXTURE_ABS}/tools/run.sh
Output captured at {FIXTURE_ABS}/execution/_run_records/out.log
"""

WORKING_CONTENT_ONE_HIT_MD = f"""# Working content artifact (fixture)

Draft cites a local screenshot at {FIXTURE_ABS}/Desktop/capture.png for now.
"""

NON_USERS_ROOTS_PLAN_MD = """# Fixture broader roots

Temp output: /tmp/chirality-harness/out.json
Private tmp output: /private/tmp/chirality-harness/out.json
Home output: /home/fixture/chirality-harness/out.json
macOS temp output: /var/folders/0s/fixture/T/chirality-harness/out.json
Boundary prose: public/private/protected-content is not a machine path.
"""

APP_DEV = ("projects", "chirality-app-dev")


def _fact(report, fact_id):
    for f in report.facts:
        if f.fact_id == fact_id:
            return f
    raise AssertionError(
        f"fact {fact_id} missing: {[f.fact_id for f in report.facts]}")


def _gen8(report):
    return _findings(report, "ABS_PATH_IN_PROJECT_SURFACE")


def test_abs_path_regex_matches_supported_machine_roots_without_privacy_false_positive():
    matches = [
        "/Users/fixture/project/file.md",
        "/private/tmp/chirality/file.md",
        "/home/fixture/project/file.md",
        "/tmp/chirality/file.md",
        "/var/folders/0s/chirality/file.md",
    ]
    for value in matches:
        assert cmd_self_check.ABS_PATH_RE.search(value), value

    misses = [
        "public/private/protected-content",
        "core/private/report-template.txt",
        "docs/home/page.md",
    ]
    for value in misses:
        assert cmd_self_check.ABS_PATH_RE.search(value) is None, value


# --- (a) non-active historical surfaces are telemetry, not path pins --------------

def test_plans_file_is_historical_telemetry_not_active_control(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo.joinpath(*APP_DEV, "plans", "fixture_assessment.md"),
           PLAN_THREE_HITS_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    fact = _fact(report, "abs_path_lint.chirality-app-dev.historical")
    assert fact.value == "files=1; hit_lines=3"
    assert "not a path pin" in fact.caveat


def test_historical_telemetry_counts_non_users_machine_roots(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo.joinpath(*APP_DEV, "plans", "broader_roots.md"),
           NON_USERS_ROOTS_PLAN_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    fact = _fact(report, "abs_path_lint.chirality-app-dev.historical")
    assert fact.value == "files=1; hit_lines=4"


# --- (b) _Coordination/_DECISIONS record -> REVIEW --------------------------------

def test_historical_decision_is_observability_not_active_control(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo / "projects" / "chirality-piping" / "execution"
           / "_Coordination" / "_DECISIONS" / "D-99_fixture_ruling.md",
           DECISION_ONE_HIT_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    assert _fact(report, "abs_path_lint.chirality-piping.historical").value == (
        "files=1; hit_lines=1")


# --- (c) _STATUS.md filename pattern -> REVIEW -------------------------------------

def test_non_entry_status_is_historical_observability(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo.joinpath(*APP_DEV, "execution", "PKG-09_Fixture",
                         "1_Working", "DEL-09-01_Abs anchor", "_STATUS.md"),
           STATUS_ONE_HIT_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    assert _fact(report, "abs_path_lint.chirality-app-dev.historical").value == (
        "files=1; hit_lines=1")


# --- (d) evidence-marker file: NO finding; counted in the evidence fact -----------

def test_run_record_is_counted_as_evidence_not_finding(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo.joinpath(*APP_DEV, "execution", "_run_records",
                         "run_2026-07-01.md"), RUN_RECORD_TWO_HITS_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    fact = _fact(report, "abs_path_lint.chirality-app-dev.evidence")
    assert fact.value == "files=1; hit_lines=2"
    assert "permitted as exact provenance" in fact.caveat
    assert find_claim_language(fact.caveat) == []


# --- (e) unclassified working surface: NO finding; counted in its fact -------------

def test_working_content_is_counted_as_historical_not_active_unclassified(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo.joinpath(*APP_DEV, "execution", "PKG-01_Fixture Pkg",
                         "1_Working", "DEL-02-01_Match one",
                         "content_notes.md"), WORKING_CONTENT_ONE_HIT_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    fact = _fact(report, "abs_path_lint.chirality-app-dev.historical")
    assert fact.value == "files=1; hit_lines=1"
    assert "not active execution controls" in fact.caveat
    assert find_claim_language(fact.caveat) == []


# --- (f) clean project: quiet, zero-count facts ------------------------------------

def test_clean_project_tree_yields_no_gen8_findings(tmp_path):
    repo = build_mini_repo(tmp_path)  # project fixtures carry no abs paths
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    for project in ("chirality-app-dev", "chirality-piping"):
        for cls in ("evidence", "unclassified"):
            fact = _fact(report, f"abs_path_lint.{project}.{cls}")
            assert fact.value == "files=0; hit_lines=0"


# --- (g) GEN-1 control-area behavior unchanged (per-line) --------------------------

def test_gen1_control_area_per_line_behavior_unchanged(tmp_path):
    repo = build_mini_repo(tmp_path)
    # Two hit lines in one control-area file -> TWO per-line GEN-1 findings
    # (GEN-8's per-file collapse never reaches the control roots).
    _write(repo / "_DomainEngines" / "TWO_ANCHORS.md",
           f"# two anchors (fixture)\n\nA: {FIXTURE_ABS}/a.md\n"
           f"B: {FIXTURE_ABS}/b.md\n")
    report, _ = cmd_self_check.run_self_check(repo)
    governed = [f for f in _findings(report, "ABS_PATH_IN_GOVERNED_SURFACE")
                if f.source_path.endswith("TWO_ANCHORS.md")]
    assert [f.source_line for f in governed] == [3, 4]
    assert all(f.severity is Severity.REVIEW for f in governed)
    # The mini repo's standing control-area shapes still fire as before.
    _has(report, "ABS_PATH_IN_GOVERNED_SURFACE", "CHANGE_HANDOFF.md", line=3,
         severity=Severity.REVIEW)
    _has(report, "ABS_PATH_IN_EVIDENCE", "open_pipe_stress.validation.json",
         line=5, severity=Severity.INFO)
    # Control-area files never fire the project-surface code, and no GEN-8
    # finding is ever BLOCK.
    assert all(not f.source_path.startswith("_DomainEngines")
               for f in _gen8(report))
    assert all(f.severity is not Severity.BLOCK for f in _gen8(report))


# --- (h) symlinked repo_root/root_filter still routes control areas to GEN-1 -------

def test_symlinked_root_filter_routes_control_area_to_gen1(tmp_path):
    # 2026-07-02 adversarial-review regression: run_self_check resolves
    # root_filter but compared it against control roots built from the
    # caller's repo_root verbatim; a symlinked repo_root misrouted control
    # areas into the project-tree lint. repo_root is now normalized once.
    (tmp_path / "real").mkdir()
    repo = build_mini_repo(tmp_path / "real")
    _write(repo / "docs" / "governance_harness" / "SYMLINK_NOTE.md",
           f"# note (fixture)\n\nSee {FIXTURE_ABS}/x.md\n")
    link = tmp_path / "link"
    link.symlink_to(tmp_path / "real")
    linked_repo = link / "repo"
    report, _ = cmd_self_check.run_self_check(
        linked_repo, root_filter=linked_repo / "docs" / "governance_harness")
    _has(report, "ABS_PATH_IN_GOVERNED_SURFACE", "SYMLINK_NOTE.md", line=3,
         severity=Severity.REVIEW)
    assert _gen8(report) == []


# --- (i) gitignored build output is excluded (only tracked files audited) ---------

def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@example.com",
                    "-c", "user.name=fixture", *args],
                   check=True, capture_output=True, text=True)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_gitignored_build_output_is_not_audited(tmp_path):
    # 2026-07-02 post-merge regression: on a dev checkout GEN-8 walked into
    # gitignored build output (frontend/dist/ packaged .app bundle) and
    # flagged packaged docs/README.md copies, inflating the 19-file baseline
    # by 2. Untracked artifacts are not governed surfaces (D-GOV-01); GEN-8
    # now audits git-tracked files only.
    repo = build_mini_repo(tmp_path)
    # A tracked historical surface remains telemetry.
    _write(repo.joinpath(*APP_DEV, "plans", "tracked_assessment.md"),
           DECISION_ONE_HIT_MD)
    # A gitignored build artifact carrying an abs path -> must NOT be audited.
    _write(repo / ".gitignore", "**/dist/\n")
    _write(repo.joinpath(*APP_DEV, "frontend", "dist", "docs", "README.md"),
           f"# packaged copy (fixture)\n\nBuilt from {FIXTURE_ABS}/src\n")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")           # respects .gitignore: dist/ stays untracked
    _git(repo, "commit", "-q", "-m", "fixture tree")
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen8(report) == []
    assert _fact(report, "abs_path_lint.chirality-app-dev.historical").value == (
        "files=1; hit_lines=1")
