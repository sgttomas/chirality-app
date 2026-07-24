#!/usr/bin/env python3
"""Self-check fixture tests.

The `_DomainEngines` fixtures are modeled VERBATIM on the live pre-cleanup
contradiction forms (the D-GOV-06 cleanup slice diff), so the checks are
exercised against the shapes they were built for. Also exports the shared
`build_mini_repo` fixture-tree builder used by the other harness tests.
"""

from __future__ import annotations

from pathlib import Path

import cmd_self_check
from harness_common import Severity

# --- Fixture material (verbatim pre-cleanup forms) -----------------------------

PROFILE_DRAFT_YAML = '''# OpenPipeStress Domain Engine Profile — DRAFT (NOT validated, NOT adopted)
#
# Status: DRAFT. This is an INSTANCE binding of the generic DomainEngineProfile
# contract to the OpenPipeStress engine.
#
# Nothing here is adopted. No deterministic profile-schema validator exists yet
# (TOOLMAKER handoff). No tool is invoked. No professional status is claimed.

domain_profile:
  schema_version: "1.0"
  id: "open_pipe_stress"
  name: "OpenPipeStress Piping-Stress Engine"
  profile_version: "0.1-DRAFT"
  profile_status: "ADOPTED"
  integration_level: "MANUAL_BRIDGE"
  protected_write_paths:
    - "projects/chirality-piping/core/**"
    - "projects/chirality-piping/schemas/**"
  agent_writable_paths:
    - "_DomainEngines/proposals/open_pipe_stress/**"
'''

RULINGS_PUBLISHED_MD = '''# RULINGS_PUBLISHED — Tier-0 Bridge (2026-06-21)

The owner ruled all 8 tier-0 decisions in-session on 2026-06-21. The profile passed
validation and the owner then **ruled Gate 2 (`VALIDATED → ADOPTED`) on 2026-06-21**
→ ProfileStatus **ADOPTED**.

**Tier-0:** FM-01..04 are gated diffs to be applied by a framework-maintenance pass
and published by CHANGE — not self-applied. Update the DRAFT profile per rulings.

Profile remains **DRAFT** (not VALIDATED — validator not built; D-T0-06) and **not ADOPTED**.
'''

INDEX_MD = '''# Domain Engine Integration — Control Area Index

> **Status of everything under this root: `PROPOSAL` / unratified.** No profile is `ADOPTED`. No decision is ruled.

| DOMAIN_ENGINE_ID | Engine | Profile | ProfileStatus |
|---|---|---|---|
| `open_pipe_stress` | OpenPipeStress | `profiles/open_pipe_stress.DRAFT.yaml` | **ADOPTED** (validated + Gate-2 adopted 2026-06-21) |

## Layout

```
  _DECISIONS/
    _REGISTER.md                  ← 8 tier-0 decision records (PROPOSAL; HumanRuling = TBD)
```
'''

REGISTER_MD = '''# Tier-0 Bridge — Decision Register (**RULED 2026-06-21**; SHAs bind at CHANGE publish)

| ID | Decision | My recommendation | HumanRuling | Unblocks |
|---|---|---|---|---|
| D-T0-06 | Profile adoption lifecycle | Persona cadence | **RULED: persona cadence** | profile off DRAFT |
'''

D_T0_06_MD = '''# D-T0-06 — Profile adoption lifecycle + sub-gates  (PROPOSAL; HumanRuling: TBD)

**Decision:** Adopt the `DRAFT→VALIDATED→ADOPTED` lifecycle and the sub-gates.

**HumanRuling:** **Persona cadence** `DRAFT→VALIDATED→ADOPTED`.   **RuledBy:** owner (in-session)   **Ruling SHA:** TBD (binds at CHANGE publish)   **Date:** 2026-06-21
'''

CHANGE_HANDOFF_MD = '''# CHANGE handoff (fixture)

Working root: /Users/fixture/ai-env/projects/example/notes.md — machine-local anchor.
'''

VALIDATION_JSON = '''{
  "contract_source": "fixture",
  "findings": [],
  "profile_id": "open_pipe_stress",
  "profile_path": "/Users/fixture/ai-env/projects/example/_DomainEngines/profiles/open_pipe_stress.DRAFT.yaml",
  "profile_status": "ADOPTED",
  "result": "VALID",
  "summary": {"error_count": 0, "warning_count": 0}
}
'''

HUMAN_ACTORS_MD = '''# human_actors — fixture allowlist

## Actors

| Canonical name | Role | Matchable aliases | Git identity | Email | Effective |
|---|---|---|---|---|---|
| Ryan Tufts | Owner | `owner`, `Owner`, `Ryan Tufts (owner)` | `Ryan Tufts <ryan@example.invalid>` | ryan@example.invalid | 2026-07-01 |
'''

GOV_DOC_MD = '''# {name}

> **Status: DRAFT pending human ratification.** Fixture governance document.

Body.
'''

ADAPTER_YAML = '''# Harness configuration authority only — governed, committed, human-reviewed; never lifecycle or project truth (plan v3 §Authority Classes).
schema: practitioner-harness-adapter/v1
project: {project}
plan: docs/PLAN.md
coordination: execution/_Coordination/_COORDINATION.md
decision_register: execution/_Coordination/_DECISIONS/_REGISTER.md
dag_pointer: execution/_DAG/_LATEST.md
status_glob: "execution/PKG-*/1_Working/*/_STATUS.md"
exclude_globs: [".archive/**", "node_modules/**"]
states: [OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED]
parser_dialect: prose-bullet-v1
drift_baseline_mismatch: {baseline_mismatch}
drift_baseline_files: {baseline_files}
validation_commands: []
guard_requires_committed_ruling_path: true
guard_requires_approval_sha: {requires_sha}
guard_approval_sha_field: "{sha_field}"
'''

STATUS_MISMATCH = '''# Status: DEL-01-01

**Current State:** IN_PROGRESS
**Last Updated:** 2026-06-04

## History
- 2026-04-30 - State set to OPEN (PREPARATION)
- 2026-05-01 - State set to IN_PROGRESS (TASK+x)
- 2026-06-04 - State moved to CHECKING (corrected package re-review)
'''

STATUS_MATCH = '''# Status: DEL-01-02

**Current State:** CHECKING
**Last Updated:** 2026-06-04

## History
- 2026-04-30 - State set to OPEN (PREPARATION)
- 2026-06-04 - State set to CHECKING (HUMAN)
'''

STATUS_UNPARSEABLE_HISTORY = '''# Status: DEL-01-03

**Current State:** SEMANTIC_READY
**Last Updated:** 2026-05-01

## History
- 2026-05-01 - Evidence promoted to COMMITTED for the record.
- 2026-05-02 - Narrative note only.
'''

STATUS_MISSING_CURRENT_STATE = '''# Status: DEL-01-04

**Last Updated:** 2026-05-01

## History
- 2026-05-01 - State set to OPEN (PREPARATION)
'''


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_domain_engines(repo: Path) -> None:
    de = repo / "_DomainEngines"
    _write(de / "DOMAIN_ENGINE_INDEX.md", INDEX_MD)
    _write(de / "RULINGS_PUBLISHED.md", RULINGS_PUBLISHED_MD)
    _write(de / "CHANGE_HANDOFF.md", CHANGE_HANDOFF_MD)
    _write(de / "_DECISIONS" / "_REGISTER.md", REGISTER_MD)
    _write(de / "_DECISIONS" / "D-T0-06_profile_adoption_lifecycle.md", D_T0_06_MD)
    _write(de / "profiles" / "open_pipe_stress.DRAFT.yaml", PROFILE_DRAFT_YAML)
    _write(de / "profiles" / "_validation" / "open_pipe_stress.validation.json",
           VALIDATION_JSON)


def build_project(repo: Path, project: str, statuses: dict[str, str],
                  baseline_mismatch: int = 0, baseline_files: int = 0,
                  requires_sha: bool = False, sha_field: str = "") -> Path:
    root = repo / "projects" / project
    _write(root / "_harness" / "adapter.yaml", ADAPTER_YAML.format(
        project=project, baseline_mismatch=baseline_mismatch,
        baseline_files=baseline_files,
        requires_sha="true" if requires_sha else "false", sha_field=sha_field))
    _write(root / "docs" / "PLAN.md", "# PLAN\n\n**Status:** fixture posture\n")
    _write(root / "execution" / "_Coordination" / "_COORDINATION.md",
           "# Coordination\n\n**Recorded:** 2026-06-13\n")
    _write(root / "execution" / "_Coordination" / "_DECISIONS" / "_REGISTER.md",
           "# Register\n\n| ID | Decision | State |\n|---|---|---|\n| D-01 | Fixture | RULED |\n")
    _write(root / "execution" / "_DAG" / "_LATEST.md",
           "# Latest DAG Pointer\n\n- Approved graph authority: `execution/_DAG/DAG-001/`\n")
    # The designated graph directory exists, so the GEN-7 pointer-currency
    # check is quiet on the default fixture tree.
    _write(root / "execution" / "_DAG" / "DAG-001" / "APPROVAL_RECORD.md",
           "# DAG-001 record (fixture)\n")
    for name, text in statuses.items():
        _write(root / "execution" / "PKG-01_Fixture Pkg" / "1_Working"
               / name / "_STATUS.md", text)
    return root


def build_mini_repo(tmp_path: Path, with_allowlist: bool = True) -> Path:
    """Shared fixture tree: two projects (aliased names, spaces in paths),
    a pre-cleanup _DomainEngines area, and root governance docs."""
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    for name in ("DIRECTIVE.md", "CONTRACT.md", "SPEC.md", "TYPES.md"):
        _write(repo / "docs" / name, GOV_DOC_MD.format(name=name))
    if with_allowlist:
        _write(repo / "docs" / "governance_harness" / "human_actors.md",
               HUMAN_ACTORS_MD)
    build_domain_engines(repo)
    build_project(repo, "chirality-piping", {
        "DEL-01-01_Fixture deliverable with spaces": STATUS_MISMATCH,
        "DEL-01-02_Second fixture": STATUS_MATCH,
        "DEL-01-03_Third fixture": STATUS_UNPARSEABLE_HISTORY,
        "DEL-01-04_Fourth fixture": STATUS_MISSING_CURRENT_STATE,
    }, baseline_mismatch=1, baseline_files=4)
    build_project(repo, "chirality-app-dev", {
        "DEL-02-01_Match one": STATUS_MATCH,
        "DEL-02-02_Match two": STATUS_MATCH,
    }, baseline_mismatch=0, baseline_files=2)
    return repo


# --- Assertions helpers ---------------------------------------------------------

def _findings(report, code):
    return [f for f in report.findings if f.code == code]


def _has(report, code, path_suffix, line=None, severity=None):
    for f in _findings(report, code):
        if not f.source_path.endswith(path_suffix):
            continue
        if line is not None and f.source_line != line:
            continue
        if severity is not None and f.severity is not severity:
            continue
        return f
    raise AssertionError(
        f"no finding code={code} path~{path_suffix} line={line}: "
        + str([(f.code, f.source_path, f.source_line) for f in report.findings]))


# --- Tests -----------------------------------------------------------------------

def test_de1_stale_ruling_annotation(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, refusal = cmd_self_check.run_self_check(repo)
    assert refusal is None
    f = _has(report, "STALE_RULING_ANNOTATION", "DOMAIN_ENGINE_INDEX.md",
             severity=Severity.REVIEW)
    assert f.source_line is not None
    _has(report, "STALE_RULING_ANNOTATION",
         "D-T0-06_profile_adoption_lifecycle.md", line=1, severity=Severity.REVIEW)


def test_de2_title_contradicts_ruling_with_allowlist(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, refusal = cmd_self_check.run_self_check(repo)
    assert refusal is None
    f = _has(report, "TITLE_CONTRADICTS_RULING",
             "D-T0-06_profile_adoption_lifecycle.md", line=1,
             severity=Severity.REVIEW)
    assert "Ryan Tufts" in f.message


def test_de2_refuses_without_allowlist(tmp_path):
    repo = build_mini_repo(tmp_path, with_allowlist=False)
    report, refusal = cmd_self_check.run_self_check(repo)
    assert refusal is not None
    assert "D-GOV-04" in refusal
    assert not _findings(report, "TITLE_CONTRADICTS_RULING")


def test_de3_stale_draft_directive(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "STALE_DRAFT_DIRECTIVE", "RULINGS_PUBLISHED.md",
         severity=Severity.REVIEW)


def test_de4_filename_vs_field(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "FILENAME_CONTRADICTS_STATUS", "open_pipe_stress.DRAFT.yaml",
         severity=Severity.REVIEW)


def test_de5_header_comment_vs_field(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    hits = _findings(report, "HEADER_CONTRADICTS_STATUS")
    lines = {f.source_line for f in hits}
    assert 1 in lines  # '— DRAFT (NOT validated, NOT adopted)'
    assert 3 in lines  # '# Status: DRAFT.'
    assert all(f.severity is Severity.REVIEW for f in hits)


def test_de5_version_string_is_info_not_conflict(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "VERSION_STRING_DRAFT_AMBIGUITY", "open_pipe_stress.DRAFT.yaml",
             severity=Severity.INFO)
    assert "NOT a status conflict" in f.message


def test_de6_banner_vs_table(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "BANNER_CONTRADICTS_REGISTER", "DOMAIN_ENGINE_INDEX.md", line=3,
         severity=Severity.REVIEW)


def test_de7_head_vs_tail(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "HEAD_CONTRADICTS_TAIL", "RULINGS_PUBLISHED.md",
             severity=Severity.REVIEW)
    assert f.source_line == 10  # the stale closing paragraph line


def test_gen1_abs_path_dimension_aware(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    governed = _has(report, "ABS_PATH_IN_GOVERNED_SURFACE", "CHANGE_HANDOFF.md",
                    line=3, severity=Severity.REVIEW)
    assert governed.dimension == "path-anchoring"
    evidence = _has(report, "ABS_PATH_IN_EVIDENCE",
                    "open_pipe_stress.validation.json", line=5,
                    severity=Severity.INFO)
    assert "permitted" in evidence.message


def test_gen2_ruling_sha_tbd_conditional_review_not_block(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    hits = _findings(report, "RULING_SHA_TBD")
    assert hits, "expected RULING_SHA_TBD findings"
    for f in hits:
        assert f.severity is Severity.REVIEW  # NEVER BLOCK (D-GOV-02 conditional)
    record_hit = _has(report, "RULING_SHA_TBD",
                      "D-T0-06_profile_adoption_lifecycle.md",
                      severity=Severity.REVIEW)
    assert "bind-at-publish" in record_hit.caveat


def test_gen2_backtick_quoted_tbd_is_not_a_finding(tmp_path):
    # A backtick-QUOTED `Ruling SHA: TBD` mention is prose quoting the rule
    # (the live false-positive shape: D-GOV-02:36), never a live TBD field;
    # an UNQUOTED field-style "**Ruling SHA:** TBD" in the SAME file (and
    # mid-line, as the D-T0 records carry it) must still fire.
    repo = build_mini_repo(tmp_path)
    fixture = repo / "_DomainEngines" / "QUOTED_TBD_FIXTURE.md"
    _write(fixture, (
        "# Quoted-rule fixture\n"
        "\n"
        "- `Ruling SHA: TBD` is **conditional**: REVIEW when the artifact\n"
        "  self-declares bind-at-publish (prose quoting the D-GOV-02 rule).\n"
        "\n"
        "**HumanRuling:** fixture ruling   **RuledBy:** owner (in-session)"
        "   **Ruling SHA:** TBD (binds at CHANGE publish)"
        "   **Date:** 2026-06-21\n"))
    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "RULING_SHA_TBD")
            if f.source_path.endswith("QUOTED_TBD_FIXTURE.md")]
    # Exactly one finding: the unquoted field line — NOT the quoted line 3.
    assert [f.source_line for f in hits] == [6]
    assert hits[0].severity is Severity.REVIEW


def test_gen10_latest_receipt_requires_canonical_labels(tmp_path):
    repo = build_mini_repo(tmp_path)
    receipts = repo / "_DomainEngines" / "bridge" / "LOOP_RECEIPTS.md"
    _write(
        receipts,
        "# Bridge Loop Receipts\n\n"
        "## Receipts\n\n"
        "- **2026-07-03 - Receipt 1**\n"
        "  - Owner directions of record: pluralized fixture direction.\n"
        "  - Gate outcome: fixture gate.\n"
        "  - Parked lanes: PR #42.\n",
    )

    report, refusal = cmd_self_check.run_self_check(repo)

    assert refusal is None
    hit = _has(
        report,
        "RECEIPT_STRUCTURE_LABEL_MISSING",
        "_DomainEngines/bridge/LOOP_RECEIPTS.md",
        5,
        Severity.WARN,
    )
    assert "Owner direction of record" in hit.message


def test_gen10_receipt_only_lane_without_carry_forward_or_retirement(tmp_path):
    repo = build_mini_repo(tmp_path)
    receipts = repo / "_DomainEngines" / "bridge" / "LOOP_RECEIPTS.md"
    _write(
        receipts,
        "# Bridge Loop Receipts\n\n"
        "## Receipts\n\n"
        "- **2026-07-02 - Receipt 0**\n"
        "  - Owner direction of record: fixture direction.\n"
        "  - Gate outcome: fixture gate.\n"
        "  - Parked lanes: PR #41.\n"
        "- **2026-07-03 - Receipt 1**\n"
        "  - Owner direction of record: fixture direction.\n"
        "  - Gate outcome: fixture gate.\n"
        "  - Parked lanes: unanchored fixture lane.\n",
    )

    report, refusal = cmd_self_check.run_self_check(repo)

    assert refusal is None
    hit = _has(
        report,
        "PARKED_LANE_RECEIPT_ONLY",
        "_DomainEngines/bridge/LOOP_RECEIPTS.md",
        12,
        Severity.REVIEW,
    )
    assert "unanchored fixture lane" in hit.message


def test_de_live_binding_gate_line_reports_resolved_named_gates(tmp_path):
    repo = build_mini_repo(tmp_path)
    profile = repo / "_DomainEngines" / "profiles" / "open_pipe_stress.DRAFT.yaml"
    _write(
        profile,
        profile.read_text(encoding="utf-8")
        + '\n  open_issues:\n'
          '    - "Live binding (L2-L3) gated x4: tier-0 adoption, app-dev F3, '
          'piping D-21, DEC-041 automation condition."\n',
    )
    piping_register = (
        repo
        / "projects"
        / "chirality-piping"
        / "execution"
        / "_Coordination"
        / "_DECISIONS"
        / "_REGISTER.md"
    )
    _write(
        piping_register,
        piping_register.read_text(encoding="utf-8")
        + "| D-21 | Fixture scope change | RULED |\n",
    )

    report, refusal = cmd_self_check.run_self_check(repo)

    assert refusal is None
    hit = _has(
        report,
        "STALE_LIVE_BINDING_GATE",
        "_DomainEngines/profiles/open_pipe_stress.DRAFT.yaml",
        23,
        Severity.REVIEW,
    )
    assert "tier-0 adoption" in hit.message
    assert "piping D-21" in hit.message


def test_root_governance_status_reported_as_facts(tmp_path):
    repo = build_mini_repo(tmp_path)
    report, _ = cmd_self_check.run_self_check(repo)
    ids = {fact.fact_id for fact in report.facts}
    for name in ("DIRECTIVE.md", "CONTRACT.md", "SPEC.md", "TYPES.md"):
        assert f"root_governance.{name}" in ids
    fact = next(f for f in report.facts if f.fact_id == "root_governance.DIRECTIVE.md")
    assert "DRAFT" in fact.value


def test_gen5_unresolved_source_ref(tmp_path):
    repo = build_mini_repo(tmp_path)
    # Add an unresolved concrete ref to a control file.
    reg = repo / "_DomainEngines" / "_DECISIONS" / "_REGISTER.md"
    reg.write_text(reg.read_text(encoding="utf-8")
                   + "\nSee `_DomainEngines/does_not_exist/NOPE.md` for details.\n",
                   encoding="utf-8")
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "UNRESOLVED_SOURCE_REF", "_REGISTER.md", severity=Severity.WARN)


def test_gen5_generated_root_source_ref_is_environment_dependent_info(tmp_path):
    repo = build_mini_repo(tmp_path)
    brief = repo / "docs" / "governance_harness" / "briefs" / "TRB-fixture.md"
    _write(brief, """# Fixture brief

## evidence_targets

- `_harness_generated/briefs/TRB-fixture.md` (under the declared generated root)
- `_harness_generated/briefs/TRB-fixture.json` (under the declared generated root)
- `docs/governance_harness/briefs/missing.md`
""")
    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "UNRESOLVED_SOURCE_REF")
            if f.source_path.endswith("TRB-fixture.md")]
    assert [(f.source_line, f.severity) for f in hits] == [
        (5, Severity.INFO),
        (6, Severity.INFO),
        (7, Severity.WARN),
    ]
    messages = " || ".join(f.message for f in hits)
    assert "declared generated root" in messages
    assert "does not resolve to an existing repo path" in messages


def test_candidate_refs_strip_trailing_parenthetical_annotations():
    """Regression (bridge Loop 1, 2026-07-02): committed adopted briefs emit
    refs like `path.md (line 9)` and `path.md (declared references surface)`;
    the annotation is descriptive, not part of the path."""
    line = ("- `projects/chirality-app-dev/execution/PKG-00_DAG/1_Working/"
            "DAG_CLOSURE_CONTROL.md (line 9)`")
    assert cmd_self_check._candidate_refs(line) == [
        "projects/chirality-app-dev/execution/PKG-00_DAG/1_Working/"
        "DAG_CLOSURE_CONTROL.md"]
    line = ("- `execution/PKG-10/1_Working/DEL-10-01_Draft/_REFERENCES.md "
            "(declared references surface)`")
    assert cmd_self_check._candidate_refs(line) == [
        "execution/PKG-10/1_Working/DEL-10-01_Draft/_REFERENCES.md"]


def test_gen5_brief_format_annotated_refs_resolve_to_base_path(tmp_path):
    """GEN-5 must resolve the brief generator's annotated emission format to
    the base path: annotated refs to existing files produce no finding, and
    an annotated ref to a missing file is still WARNed (with the stripped
    ref named)."""
    repo = build_mini_repo(tmp_path)
    reg = repo / "_DomainEngines" / "_DECISIONS" / "_REGISTER.md"
    reg.write_text(
        reg.read_text(encoding="utf-8")
        + "\n- source: `_DomainEngines/_DECISIONS/_REGISTER.md (line 9)`\n"
        + "- source: `_DomainEngines/_DECISIONS/_REGISTER.md "
        + "(declared references surface)`\n"
        + "- source: `_DomainEngines/does_not_exist/NOPE.md (line 3)`\n",
        encoding="utf-8")
    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "UNRESOLVED_SOURCE_REF")
            if f.source_path.endswith("_REGISTER.md")]
    # Only the missing base path is flagged — as the stripped ref.
    assert len(hits) == 1
    assert "`_DomainEngines/does_not_exist/NOPE.md`" in hits[0].message


def test_gen5_pec_project_relative_refs_resolve(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(repo / "projects" / "pec" / "docs" / "STATUS.md", "# PEC status\n")
    reg = repo / "_DomainEngines" / "_DECISIONS" / "_REGISTER.md"
    reg.write_text(
        reg.read_text(encoding="utf-8")
        + "\n- PEC project-local source: `docs/STATUS.md`\n",
        encoding="utf-8",
    )

    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "UNRESOLVED_SOURCE_REF")
            if f.source_path.endswith("_REGISTER.md")]

    assert all("docs/STATUS.md" not in hit.message for hit in hits)


def test_gen11_piping_receipt_validator_failure_is_blocking(tmp_path):
    repo = tmp_path / "repo"
    piping = repo / "projects" / "chirality-piping"
    _write(piping / "loop" / "LOOP_RECEIPTS.md", "# fixture ledger\n")
    _write(
        repo / "tools" / "validation" / "validate_piping_loop_receipts.py",
        "print('INVALID FIXTURE: receipt contract failed')\n"
        "raise SystemExit(1)\n",
    )

    report, _ = cmd_self_check.run_self_check(repo, root_filter=piping)
    hits = _findings(report, "PIPING_RECEIPT_CONTRACT")
    assert len(hits) == 1
    assert hits[0].severity == Severity.BLOCK
    assert "INVALID FIXTURE" in hits[0].message


def test_gen12_app_dev_receipt_validator_failure_is_blocking(tmp_path):
    repo = tmp_path / "repo"
    app_dev = repo / "projects" / "chirality-app-dev"
    _write(app_dev / "loop" / "LOOP_RECEIPTS.md", "# fixture ledger\n")
    _write(
        repo / "tools" / "validation" / "validate_app_dev_loop_receipts.py",
        "print('INVALID FIXTURE: app-dev receipt contract failed')\n"
        "raise SystemExit(1)\n",
    )

    report, _ = cmd_self_check.run_self_check(repo, root_filter=app_dev)
    hits = _findings(report, "APP_DEV_RECEIPT_CONTRACT")
    assert len(hits) == 1
    assert hits[0].severity == Severity.BLOCK
    assert "INVALID FIXTURE" in hits[0].message
