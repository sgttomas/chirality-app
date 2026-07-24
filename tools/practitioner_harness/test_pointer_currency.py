#!/usr/bin/env python3
"""GEN-7 `_LATEST*` pointer-currency tests (K-PROV-1 / K-STALE-2).

Live reproduction case (the check's first detection target, 2026-07-01
consistency-audit follow-through): `projects/chirality-piping/execution/
_Reconciliation/_LATEST.md` points at the 2026-05-09 DEV001 run summary,
retired to `.archive/` on 2026-06-03 (commit 349a2ab33); the newest surviving
same-class sibling is the 2026-05-03 SCA002 summary. The fixture below models
that shape verbatim (pointer line, sibling set, archive location).

Severity per TYPES.md §11 / D-GOV-02: REVIEW throughout — the check is
judgment-adjacent (repoint vs retain is the owner's disposition), so BLOCK is
never appropriate; NOT_APPLICABLE when a root carries no pointer files.
"""

from __future__ import annotations

import harness
from harness_common import Severity, find_claim_language
from test_self_check_fixtures import _findings, _has, _write, build_mini_repo

import cmd_self_check

# --- Fixture material (modeled verbatim on the live reproduction case) ---------

RETIRED_NAME = ("Reconciliation_Run_Summary_2026-05-09_DEV001_REV05_"
                "CANDIDATE_EDGE_RECONCILIATION.md")
POINTER_LIVE_SHAPE = f"Latest: {RETIRED_NAME}\nUpdated: 2026-05-09\n"
SURVIVING_SIBLINGS = (
    "Reconciliation_Run_Summary_2026-04-30_PKG-12_POST_SETUP.md",
    "Reconciliation_Run_Summary_2026-05-02_DEL0805_CANDIDATE_E0621.md",
    "Reconciliation_Run_Summary_2026-05-03_SCA002_REV05_COMPATIBILITY_PLANNING.md",
)
NEWEST_SURVIVOR = SURVIVING_SIBLINGS[-1]
ARCHIVE_SUBDIR = ".archive/DEV-001_RETIRED_2026-06-03"


def _build_recon(repo, pointer_text: str = POINTER_LIVE_SHAPE,
                 archived: bool = False):
    recon = (repo / "projects" / "chirality-piping" / "execution"
             / "_Reconciliation")
    _write(recon / "_LATEST.md", pointer_text)
    for name in SURVIVING_SIBLINGS:
        _write(recon / name, "# run summary (fixture)\n")
    if archived:
        _write(recon / ARCHIVE_SUBDIR / RETIRED_NAME,
               "# retired run summary (fixture)\n")
    return recon


def _pointer_findings(report, path_suffix):
    return [f for f in report.findings
            if f.code.startswith("POINTER_TARGET")
            and f.source_path.endswith(path_suffix)]


# --- (a) target resolution outside .archive/ ------------------------------------

def test_pointer_target_retired_to_archive_fires_review(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_recon(repo, archived=True)
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "POINTER_TARGET_UNRESOLVED", "_Reconciliation/_LATEST.md",
             line=1, severity=Severity.REVIEW)
    assert f.invariant == "K-PROV-1"
    assert RETIRED_NAME in f.message
    # Archive probe: the retired copy is cited as triage context.
    assert ARCHIVE_SUBDIR in f.message
    assert "retired into `.archive/`" in f.message
    # Newest surviving same-class sibling (the 2026-05-03 SCA002 summary).
    assert NEWEST_SURVIVOR in f.message
    assert "human review required" in f.message
    # The unresolved pointer never additionally fires the newest-sibling arm.
    assert [g.code for g in
            _pointer_findings(report, "_Reconciliation/_LATEST.md")] == [
        "POINTER_TARGET_UNRESOLVED"]
    assert find_claim_language(f.message) == []


def test_pointer_target_missing_entirely_still_fires(tmp_path):
    repo = build_mini_repo(tmp_path)
    _build_recon(repo, archived=False)  # e.g. fresh clone: .archive untracked
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "POINTER_TARGET_UNRESOLVED", "_Reconciliation/_LATEST.md",
             line=1, severity=Severity.REVIEW)
    assert "A same-named entry exists" not in f.message
    assert NEWEST_SURVIVOR in f.message


# --- (b) newest-same-class-sibling by date-in-filename ---------------------------

def test_pointer_resolvable_but_not_newest_is_review(tmp_path):
    repo = build_mini_repo(tmp_path)
    stale_target = SURVIVING_SIBLINGS[1]  # 2026-05-02; 2026-05-03 survives
    _build_recon(repo, pointer_text=f"Latest: {stale_target}\n"
                                    "Updated: 2026-05-02\n")
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "POINTER_TARGET_NOT_NEWEST", "_Reconciliation/_LATEST.md",
             line=1, severity=Severity.REVIEW)
    assert f.invariant == "K-STALE-2"
    assert stale_target in f.message
    assert NEWEST_SURVIVOR in f.message
    assert "human-triaged" in f.message
    assert not _findings(report, "POINTER_TARGET_UNRESOLVED")
    assert find_claim_language(f.message) == []


def test_pointer_newest_target_is_quiet(tmp_path):
    repo = build_mini_repo(tmp_path)
    recon = _build_recon(repo, pointer_text=f"Latest: {NEWEST_SURVIVOR}\n"
                                            "Updated: 2026-05-03\n")
    # Later-dated entries OUTSIDE the class (different pre-date prefix) and a
    # same-class SAME-date entry must not flag: the comparison is date-strict
    # and class-strict ("where the convention allows").
    _write(recon / "Other_Class_Run_2026-06-30.md", "# other class (fixture)\n")
    _write(recon / "Reconciliation_Run_Summary_2026-05-03_OTHERTAG.md",
           "# same date, same class (fixture)\n")
    report, _ = cmd_self_check.run_self_check(repo)
    assert _pointer_findings(report, "_Reconciliation/_LATEST.md") == []


# --- Target-shape coverage: directories, project-relative refs, none-values ------

def test_pointer_directory_and_subdir_targets_resolve(tmp_path):
    repo = build_mini_repo(tmp_path)
    # Snapshot DIRECTORY designated by bare name from a parent-level pointer
    # (the DepClosure convention): resolves via the pointer directory's
    # immediate subdirectories.
    recon = (repo / "projects" / "chirality-app-dev" / "execution"
             / "_Reconciliation")
    _write(recon / "_LATEST.md",
           "Latest accepted DepClosure snapshot: "
           "CLOSURE_FIX_2026-06-16_0325Z\n")
    _write(recon / "DepClosure" / "CLOSURE_FIX_2026-06-16_0325Z"
           / "closure.md", "# closure (fixture)\n")
    report, _ = cmd_self_check.run_self_check(repo)
    assert _pointer_findings(report, "_Reconciliation/_LATEST.md") == []
    # The default fixture tree is pointer-quiet overall (the two project DAG
    # pointers designate `execution/_DAG/DAG-001/`, which exists).
    assert not _findings(report, "POINTER_TARGET_UNRESOLVED")
    assert not _findings(report, "POINTER_TARGET_NOT_NEWEST")


def test_pointer_history_annotated_entries_are_not_designations(tmp_path):
    # Live coordination-pointer shape: a 'Latest/Active ...:' heading followed
    # by an explicitly historical entry, with the current entry on the next
    # line. Only the current designation is audited; history words AFTER the
    # ref (e.g. '... stays exhausted') must not suppress a real designation.
    repo = build_mini_repo(tmp_path)
    coord = (repo / "projects" / "chirality-app-dev" / "execution"
             / "_Coordination")
    _write(coord / "_LATEST.md", "\n".join((
        "# Latest Coordination Pointer",
        "",
        "Active development queue:",
        "",
        "- **Exhausted (predecessor to the active queue): "
        "`plans/PLAN_2026-06-20_gone.md`** (history; resolves nowhere).",
        "- **ACTIVE queue: `plans/PLAN_2026-06-21_active.md`** — the prior "
        "queue stays exhausted.",
        "")))
    _write(repo / "projects" / "chirality-app-dev" / "plans"
           / "PLAN_2026-06-21_active.md", "# plan (fixture)\n")
    report, _ = cmd_self_check.run_self_check(repo)
    # The historical (and dangling) predecessor entry is never designated;
    # the ACTIVE entry resolves and is the newest PLAN_* of its class.
    assert _pointer_findings(report, "_Coordination/_LATEST.md") == []


def test_pointer_none_value_yields_no_findings(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo / "projects" / "chirality-app-dev" / "execution" / "_Sources"
           / "_LATEST.md", "Latest: (none)\n")
    report, _ = cmd_self_check.run_self_check(repo)
    assert _pointer_findings(report, "_Sources/_LATEST.md") == []


# --- NOT_APPLICABLE + exit-code posture -------------------------------------------

def test_not_applicable_when_root_has_no_pointer_files(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    na = _findings(report, "POINTER_CHECK_NOT_APPLICABLE")
    assert {f.source_path for f in na} == {"_DomainEngines",
                                           "docs/governance_harness"}
    assert all(f.severity is Severity.NOT_APPLICABLE for f in na)
    assert all("preconditions absent" in f.message for f in na)
    assert report.summary["pointer_files_scanned"] == 2  # the two DAG pointers


def test_pointer_review_exit_codes(tmp_path, capsys):
    # REVIEW per TYPES §11: exit 0, nonzero only under --strict; never BLOCK.
    repo = build_mini_repo(tmp_path)
    _build_recon(repo, archived=True)
    assert harness.main(["--repo-root", str(repo), "self-check"]) == 0
    out = capsys.readouterr().out
    assert "POINTER_TARGET_UNRESOLVED" in out
    assert find_claim_language(out) == []
    assert harness.main(["--repo-root", str(repo), "--strict", "self-check"]) == 1
    capsys.readouterr()
