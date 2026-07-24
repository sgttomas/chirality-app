#!/usr/bin/env python3
"""GEN-9 agent-registry currency tests (K-AGENTS-1).

Live reproduction case (the check's first detection target, 2026-07-01
consistency-audit §4 item 3): `AGENTS.md` indexes DELIVERABLE_TASK as live
while `agents/AGENT_DELIVERABLE_TASK.md` exists only in the gitignored
`agents/.archive/` tree. The fixtures below model that shape (a cited token
resolving nowhere, with and without an archived copy).

Severity per TYPES.md §11 / D-GOV-02: REVIEW (forward direction; fix-vs-
retain is a human disposition) and WARN (reverse direction; live-but-
unindexed hygiene); NOT_APPLICABLE when the registry preconditions are
absent. BLOCK is never emitted by this check's own severity design
(registry currency is hygiene surfacing, not a gate); K-AGENTS-1 itself
is RATIFIED (docs/CONTRACT.md, owner ratification 2026-07-11).
v1 observation boundary: backticked file tokens only; role-name narrative
mentions never fire either direction.
"""

from __future__ import annotations

from harness_common import Severity, find_claim_language
from test_self_check_fixtures import _findings, _has, _write, build_mini_repo

import cmd_self_check

# --- Fixture material (modeled on the live registry shape) ---------------------

REGISTRY_MD = """# AGENTS — fixture registry

Use `AGENT_*` for instruction files (e.g., `AGENT_TASK.md`). All files are
in `agents/`.

| Role | File | Purpose |
|---|---|---|
| TASK | `AGENT_TASK.md` | Generic bounded-task shell |
| DELIVERABLE_TASK | `AGENT_DELIVERABLE_TASK.md` | Preserved helper workflow |

Dispatch notes cite `AGENT_DELIVERABLE_TASK.md` a second time here; only
the FIRST citing line anchors a finding. A bare DELIVERABLE_TASK role-name
mention is outside the v1 file-token boundary.
"""

MISSING_TOKEN = "AGENT_DELIVERABLE_TASK.md"
MISSING_TOKEN_FIRST_LINE = 9  # the table row above; the line-11 citation is second


def _build_registry(repo, index_text=REGISTRY_MD, agent_files=("AGENT_TASK.md",),
                    archived_files=()):
    _write(repo / "AGENTS.md", index_text)
    (repo / "agents").mkdir(exist_ok=True)
    for name in agent_files:
        _write(repo / "agents" / name, "# agent instruction (fixture)\n")
    for name in archived_files:
        _write(repo / "agents" / ".archive" / name,
               "# archived agent instruction (fixture)\n")


def _gen9_findings(report):
    return [f for f in report.findings
            if f.code in ("REGISTRY_TARGET_MISSING", "AGENT_FILE_UNINDEXED",
                          "REGISTRY_CHECK_NOT_APPLICABLE")]


# --- (a) forward: cited token resolves nowhere -----------------------------------

def test_registry_target_missing_fires_review_at_first_citing_line(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_registry(repo)  # AGENT_DELIVERABLE_TASK.md cited, never created
    report, _ = cmd_self_check.run_self_check(repo)
    hits = _findings(report, "REGISTRY_TARGET_MISSING")
    assert [(f.source_path, f.source_line) for f in hits] == [
        ("AGENTS.md", MISSING_TOKEN_FIRST_LINE)]  # distinct token, first line
    f = hits[0]
    assert f.severity is Severity.REVIEW
    assert f.invariant == "K-AGENTS-1"
    assert MISSING_TOKEN in f.message
    # K-AGENTS-1 quoted accurately (CONTRACT §1.11), never paraphrased stronger.
    assert ("the live registry governs and the discrepancy is surfaced"
            in f.message)
    assert "human review required" in f.message
    # No archived copy in this fixture: the conditional note MUST be absent
    # (fresh checkouts/worktrees never materialize gitignored archives).
    assert "A same-named file sits under" not in f.message
    assert find_claim_language(f.message) == []


# --- (b) fully-resolving registry is quiet ---------------------------------------

def test_fully_resolving_registry_yields_no_gen9_findings(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_registry(repo, agent_files=("AGENT_TASK.md", MISSING_TOKEN))
    report, _ = cmd_self_check.run_self_check(repo)
    assert _gen9_findings(report) == []


# --- (c) preconditions absent -> NOT_APPLICABLE ----------------------------------

def test_absent_registry_yields_not_applicable(tmp_path):
    repo = build_mini_repo(tmp_path)  # no AGENTS.md, no agents/
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "REGISTRY_CHECK_NOT_APPLICABLE", "AGENTS.md",
             severity=Severity.NOT_APPLICABLE)
    assert f.invariant == "K-AGENTS-1"
    assert "preconditions absent" in f.message
    assert not _findings(report, "REGISTRY_TARGET_MISSING")
    assert not _findings(report, "AGENT_FILE_UNINDEXED")


def test_registry_without_agents_dir_is_also_not_applicable(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo / "AGENTS.md", REGISTRY_MD)  # agents/ never created
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "REGISTRY_CHECK_NOT_APPLICABLE", "AGENTS.md",
         severity=Severity.NOT_APPLICABLE)


# --- (d) reverse: live file unindexed -> WARN -------------------------------------

def test_live_agent_file_unindexed_is_warn(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_registry(repo, agent_files=("AGENT_TASK.md", MISSING_TOKEN,
                                       "AGENT_ORPHAN.md"))
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "AGENT_FILE_UNINDEXED", "agents/AGENT_ORPHAN.md",
             severity=Severity.WARN)
    assert f.invariant == "K-AGENTS-1"
    assert "the live registry governs" in f.message
    assert "human review" in f.message
    # Indexed files never fire the reverse direction.
    assert [g.source_path for g in _findings(report, "AGENT_FILE_UNINDEXED")] == [
        "agents/AGENT_ORPHAN.md"]
    assert find_claim_language(f.message) == []


# --- (e) archived-only copy: conditional note fires -------------------------------

def test_archived_only_copy_is_review_with_archive_note(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_registry(repo, archived_files=(MISSING_TOKEN,))
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "REGISTRY_TARGET_MISSING", "AGENTS.md",
             line=MISSING_TOKEN_FIRST_LINE, severity=Severity.REVIEW)
    assert f"agents/.archive/{MISSING_TOKEN}" in f.message
    assert "gitignored; absent in fresh checkouts/worktrees" in f.message
    # The archived copy is triage context only; it never indexes as live, so
    # the reverse direction stays quiet.
    assert not _findings(report, "AGENT_FILE_UNINDEXED")
    assert find_claim_language(f.message) == []


# --- (f) never BLOCK ---------------------------------------------------------------

def test_gen9_never_blocks(tmp_path):
    for sub, builder in (
            ("missing", lambda r: _build_registry(r)),
            ("orphan", lambda r: _build_registry(
                r, agent_files=("AGENT_TASK.md", MISSING_TOKEN,
                                "AGENT_ORPHAN.md"))),
            ("archived", lambda r: _build_registry(
                r, archived_files=(MISSING_TOKEN,))),
            ("absent", lambda r: None)):
        (tmp_path / sub).mkdir()
        repo = build_mini_repo(tmp_path / sub)
        builder(repo)
        report, _ = cmd_self_check.run_self_check(repo)
        gen9 = _gen9_findings(report)
        assert gen9, sub  # every shape above yields at least one finding
        assert all(f.severity is not Severity.BLOCK for f in gen9), sub


# --- (g) superset filenames never phantom-match (token left boundary) --------------

SUPERSET_REGISTRY_MD = """# AGENTS — fixture registry

| Role | File | Purpose |
|---|---|---|
| SUB_TASK | `SUB_AGENT_TASK.md` | Wrapper whose filename embeds a token |
"""


def test_superset_token_no_phantom_forward_and_reverse_fires(tmp_path):
    # 2026-07-02 adversarial-review regression: without a left boundary the
    # token regex extracted a phantom AGENT_TASK.md from inside
    # SUB_AGENT_TASK.md (fabricated forward finding), and the raw-substring
    # reverse test treated a live AGENT_TASK.md as indexed by that same
    # superset token (suppressed WARN). Both directions now token-match.
    repo = build_mini_repo(tmp_path)
    _build_registry(repo, index_text=SUPERSET_REGISTRY_MD,
                    agent_files=("AGENT_TASK.md", "SUB_AGENT_TASK.md"))
    report, _ = cmd_self_check.run_self_check(repo)
    assert not _findings(report, "REGISTRY_TARGET_MISSING")
    assert [f.source_path
            for f in _findings(report, "AGENT_FILE_UNINDEXED")] == [
        "agents/AGENT_TASK.md"]
