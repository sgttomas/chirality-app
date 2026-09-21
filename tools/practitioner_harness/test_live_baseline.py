#!/usr/bin/env python3
"""LIVE-tree baseline tests (skippable when the live roots are absent or when
CHIRALITY_SKIP_LIVE_TESTS=1). Pins the ruled drift baseline (piping 0/101,
app-dev 0/54 — conscious pin update 2026-07-02: the original 92/101 class was
resolved by the owner's class-wide K-CONFLICT-1 ruling, header IN_PROGRESS
authoritative, recorded at projects/chirality-piping/execution/_Reconciliation/
LifecycleCorrection/LIFECYCLE_CORRECTION_2026-07-02_2050/Decision_Log.md),
the current aggregate self-check severity totals, the three deliberately
retained stale surfaces (owner ruling
2026-07-01; post-cleanup exact counts pinned per the D-T0 clean + backfill
owner ruling, 2026-07-02) that self-check MUST catch, the retired piping
reconciliation pointer (the GEN-7 pointer-currency check's first detection
target), the
GEN-8 25-file instruction-class abs-path baseline (a drift metric: it trends
DOWN as files are relativized when next touched, and a conscious pin update
accompanies each reduction), and the GEN-9 registry zero-drift state (its
first detection target, the AGENTS.md DELIVERABLE_TASK row, was removed at
owner direction 2026-07-01)."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

import cmd_bridge_status
import cmd_drift
import cmd_self_check

LIVE_REPO = Path(__file__).resolve().parents[2]

live = pytest.mark.skipif(
    os.environ.get("CHIRALITY_SKIP_LIVE_TESTS") == "1"
    or not (LIVE_REPO / "projects" / "chirality-piping" / "_harness" / "adapter.yaml").is_file()
    or not (LIVE_REPO / "projects" / "chirality-app-dev" / "_harness" / "adapter.yaml").is_file()
    or not (LIVE_REPO / "_DomainEngines").is_dir(),
    reason="live pilot roots/manifests absent (or live tests disabled by env)",
)


def _fact(report, fact_id):
    for f in report.facts:
        if f.fact_id == fact_id:
            return f
    raise AssertionError(f"fact {fact_id} missing: {[f.fact_id for f in report.facts]}")


@pytest.fixture(scope="module")
def live_self_check():
    """One shared live self-check for every test in this module. The report is
    read-only and the tree cannot change mid-run, so per-test re-runs (each a
    full repo scan) would assert against byte-identical reports."""
    return cmd_self_check.run_self_check(LIVE_REPO)


@live
def test_live_drift_baseline_0_of_102_and_0_of_54():
    # Conscious pin update 2026-07-02 (was 92/101): the STATUS_HISTORY_MISMATCH
    # class was resolved by the owner's class-wide K-CONFLICT-1 ruling ("all
    # shall be IN_PROGRESS"); one parser-verified reversal history line was
    # appended per file. Ruling record: projects/chirality-piping/execution/
    # _Reconciliation/LifecycleCorrection/LIFECYCLE_CORRECTION_2026-07-02_2050/
    # Decision_Log.md. Pin updates here are conscious, never silent. SCA-009
    # added DEL-07-09 as the 102nd Piping status file on 2026-08-21; it has no
    # asserted lifecycle state, so matches remain 101 and mismatches remain 0.
    # SCA-APP-009 adds DEL-09-07 as the 54th App status file on 2026-09-04;
    # all 54 App statuses parse and match, so the combined total is 156.
    report = cmd_drift.run_drift(LIVE_REPO, [
        LIVE_REPO / "projects" / "chirality-app-dev",
        LIVE_REPO / "projects" / "chirality-piping",
    ])
    piping = _fact(report, "drift.chirality-piping").value
    assert "files=102" in piping
    assert "mismatches=0" in piping
    assert "unparseable_docs=0" in piping
    app_dev = _fact(report, "drift.chirality-app-dev").value
    assert "files=54" in app_dev
    assert "mismatches=0" in app_dev
    assert report.summary["files_total"] == 156
    assert report.summary["mismatches_total"] == 0


@live
def test_live_self_check_catches_the_three_retained_surfaces(live_self_check):
    # Conscious pin update (owner ruling 2026-07-02, in-session): the D-T0
    # stale-title/TBD-SHA drift was cleaned and backfilled to the tier-0
    # publication commit 6e70b5aace4a3a7c4ebb20490a3bf57bfd912f45 per the
    # D-GOV pattern (f1549afb1). The D-T0-16 PEC harness tranche removed the
    # DOMAIN_ENGINE_INDEX stale PEC-proposal annotation; the remaining live
    # fixture surfaces MUST keep firing (asserted individually below, then
    # pinned as exact counts).
    report, refusal = live_self_check
    assert refusal is None
    keyed = {(f.code, f.source_path, f.source_line) for f in report.findings}
    assert ("STALE_RULING_ANNOTATION",
            "_DomainEngines/_DECISIONS/D-T0-06_profile_adoption_lifecycle.md",
            1) in keyed
    assert ("TITLE_CONTRADICTS_RULING",
            "_DomainEngines/_DECISIONS/D-T0-06_profile_adoption_lifecycle.md",
            1) in keyed
    assert ("STALE_DRAFT_DIRECTIVE",
            "_DomainEngines/RULINGS_PUBLISHED.md", 20) in keyed
    # Post-cleanup exact counts: ONLY the retained surfaces remain. The seven
    # other D-T0 titles now read "(RULED 2026-06-21)"; all eight records'
    # Ruling SHA fields are backfilled to the publication commit;
    # RULINGS_PUBLISHED.md:3 was reworded with the dated note; and the
    # D-GOV-02:36 backtick-QUOTED `Ruling SHA: TBD` mention is excluded by
    # the GEN-2 quotation suppression (prose quoting the rule, not a live
    # field).
    counts: dict[str, int] = {}
    for f in report.findings:
        counts[f.code] = counts.get(f.code, 0) + 1
    assert counts.get("STALE_RULING_ANNOTATION", 0) == 1
    assert counts.get("TITLE_CONTRADICTS_RULING", 0) == 1
    assert counts.get("STALE_DRAFT_DIRECTIVE", 0) == 1
    assert counts.get("RULING_SHA_TBD", 0) == 0


@live
def test_live_self_check_abs_path_in_evidence_reports_are_pinned(live_self_check):
    report, _ = live_self_check
    hits = [f for f in report.findings if f.code == "ABS_PATH_IN_EVIDENCE"]
    assert len(hits) == 1
    assert {(h.source_path, h.source_line) for h in hits} == {
        ("_DomainEngines/profiles/_validation/open_pipe_stress.validation.json", 5),
    }


@live
def test_live_bridge_status_reports_pec_adopted_read_only_profile():
    # Conscious live-pin update: D-T0-27 O-A materializes the exact PEC v2
    # profile as ADOPTED / READ_ONLY; application effectiveness remains governed.
    report = cmd_bridge_status.run_bridge_status(LIVE_REPO)
    assert _fact(report, "bridge_status.profile.pec.profile_status").value == "ADOPTED"
    assert _fact(report, "bridge_status.profile.pec.gate_posture").value == (
        "Gate 2 adopted"
    )
    md = report.render_markdown()
    assert "| `pec` | `ADOPTED` | Gate 2 adopted | `READ_ONLY` |" in md


@live
def test_live_self_check_stale_open_issue_is_zero(live_self_check):
    # Post-cleanup live corpus: open_issues entries are annotated in place and
    # the D-T0-06 ruling condition carries its "[Condition met ...]" note.
    report, _ = live_self_check
    assert [f for f in report.findings if f.code == "STALE_OPEN_ISSUE"] == []


@live
def test_live_self_check_live_binding_gate_drift_is_detected(live_self_check):
    # Conscious pin inversion 2026-07-04: this test originally pinned the
    # HB-8 STALE_LIVE_BINDING_GATE finding at profile :145 (the line still
    # named the cleared tier-0-adoption and piping D-21 gates). The
    # owner-delegated tier-0 CHANGE
    # (CHANGE_PREP_2026-07-04_live_binding_gate_destale.md) rewrote the line
    # to the single genuinely open gate (app-dev F3), so the live corpus now
    # lawfully carries ZERO findings of this code. Detector behaviour on
    # synthetic stale input stays covered by the HB-8 fixture tests.
    report, _ = live_self_check
    hits = [f for f in report.findings if f.code == "STALE_LIVE_BINDING_GATE"]
    assert hits == []


@live
def test_live_self_check_draft_basis_pins(live_self_check):
    from harness_common import Severity
    report, _ = live_self_check
    assert [f for f in report.findings if f.code == "DRAFT_BASIS_AS_BINDING"] == []
    info = [f for f in report.findings if f.code == "DRAFT_BASIS_RULED_CLOSED"]
    # The seven D-GOV records' `FramedBy: governance_harness_plan_v3` lines:
    # the plan HTML self-declares "PROPOSAL, pending D-GOV-01"; D-GOV-01 is
    # RULED -> closure recorded as INFO (conditional per the D-GOV-02 model).
    assert len(info) == 7
    assert all(f.severity is Severity.INFO for f in info)
    assert {(f.source_path, f.source_line) for f in info} == {
        (f"docs/governance_harness/_DECISIONS/{name}", 7)
        for name in (
            "D-GOV-01_substrate_authority.md",
            "D-GOV-02_verifier_severity_and_override.md",
            "D-GOV-03_pilot_scope.md",
            "D-GOV-04_human_actor_identity.md",
            "D-GOV-05_minimal_governance_basis.md",
            "D-GOV-06_domain_profile_current_truth.md",
            "D-GOV-07_domain_gate_sha_binding.md",
        )}


@live
def test_live_pointer_currency_first_detection_target(live_self_check):
    # The 2026-07-01 consistency audit's live reproduction case: the piping
    # reconciliation pointer designated the 2026-05-09 DEV001 run summary,
    # retired to .archive/ on 2026-06-03 (349a2ab33). The owner ruled the
    # disposition REPOINT (piping D-28, applied on main at d74b991db), so this
    # test is disposition-aware: on a tree predating the repoint the check
    # MUST fire (the check's first detection target); on the repointed tree
    # the pointer resolves to the newest surviving sibling and MUST be quiet.
    pointer = (LIVE_REPO / "projects" / "chirality-piping" / "execution"
               / "_Reconciliation" / "_LATEST.md")
    first_line = pointer.read_text(encoding="utf-8").splitlines()[0]
    report, _ = live_self_check
    hits = [f for f in report.findings if f.code == "POINTER_TARGET_UNRESOLVED"]
    if "2026-05-09_DEV001" in first_line:  # pre-disposition tree
        assert [(f.source_path, f.source_line) for f in hits] == [
            ("projects/chirality-piping/execution/_Reconciliation/_LATEST.md", 1)]
        msg = hits[0].message
        assert ("Reconciliation_Run_Summary_2026-05-09_DEV001_REV05_CANDIDATE_"
                "EDGE_RECONCILIATION.md") in msg
        # Newest surviving same-class sibling cited as triage context.
        assert ("Reconciliation_Run_Summary_2026-05-03_SCA002_REV05_"
                "COMPATIBILITY_PLANNING.md") in msg
    else:  # repointed per the D-28 ruling
        assert ("Reconciliation_Run_Summary_2026-05-03_SCA002_REV05_"
                "COMPATIBILITY_PLANNING.md") in first_line
        assert hits == []
    # Every other live pointer resolves and is the newest of its class.
    assert [f for f in report.findings
            if f.code == "POINTER_TARGET_NOT_NEWEST"] == []
    # docs/governance_harness carries no pointer files -> NOT_APPLICABLE.
    # Conscious pin update 2026-07-24 (was: projects/pec listed here too):
    # the D-PEC-60 decomposition session created
    # projects/pec/execution/_Decomposition/_LATEST.md (Gate 7 accepted same
    # day), so pec entered pointer-currency scope and its pointer must
    # resolve quietly (asserted by the zero-findings checks above).
    from harness_common import Severity
    na = [f for f in report.findings if f.code == "POINTER_CHECK_NOT_APPLICABLE"]
    assert {f.source_path for f in na} == {"docs/governance_harness"}
    assert all(f.severity is Severity.NOT_APPLICABLE for f in na)


@live
def test_live_gen8_semantic_portability_invariants(live_self_check):
    report, _ = live_self_check
    assert [f for f in report.findings if f.code in {
        "ABS_PATH_IN_PROJECT_SURFACE",
        "ABS_PATH_IN_UNCLASSIFIED_SURFACE",
    }] == []
    assert [f for f in report.findings
            if f.code.startswith("PORTABILITY_POLICY_")] == []
    piping = _fact(report, "abs_path_lint.chirality-piping.semantic_invariants")
    assert re.fullmatch(
        r"unacknowledged_control=0; active_unclassified=0; "
        r"policy_issues=0; acknowledged_control=[0-9]+",
        piping.value,
    )
    # Valid acknowledged-control and historical growth are telemetry only:
    # no exact finding count or path set is pinned.
    historical = _fact(report, "abs_path_lint.chirality-piping.historical")
    assert re.fullmatch(r"files=\d+; hit_lines=\d+", historical.value)


@live
def test_live_gen9_registry_currency_zero_drift(live_self_check):
    # Consistency-audit §4 item 3 was the check's first detection target: the
    # registry indexed DELIVERABLE_TASK as live (AGENTS.md:89 at 4e01db61e)
    # while the file existed only under the gitignored agents/.archive/. The
    # owner ruled the disposition REMOVE (directed 2026-07-01; applied in this
    # PR — the detection state is pinned by the prior commit, fcca5fedd), so
    # the live registry is pinned clean in BOTH directions. A regression in
    # either direction is a conscious pin update, never a silent one; the
    # detector itself is proven by test_agent_registry_fixtures.py.
    report, _ = live_self_check
    assert [f for f in report.findings
            if f.code == "REGISTRY_TARGET_MISSING"] == []
    assert [f for f in report.findings
            if f.code == "AGENT_FILE_UNINDEXED"] == []
    assert [f for f in report.findings
            if f.code == "REGISTRY_CHECK_NOT_APPLICABLE"] == []


@live
def test_live_self_check_reports_root_ratified_governance_and_exits_clean(live_self_check):
    report, _ = live_self_check
    for name in ("DIRECTIVE.md", "CONTRACT.md", "SPEC.md", "TYPES.md"):
        fact = _fact(report, f"root_governance.{name}")
        assert "RATIFIED" in fact.value
        assert "2026-07-11" in fact.value
    from harness_common import Severity, compute_exit_code
    assert compute_exit_code(report.findings) == 0
    assert not any(f.severity is Severity.BLOCK for f in report.findings)
