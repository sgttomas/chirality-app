#!/usr/bin/env python3
"""Archive fixture corpus — adversarial fixtures from the real pre-cleanup tree.

Provenance manifest: the PRE_* constants below are VERBATIM pre-images taken
from `git show 15c958e06^` (the repo state immediately before the D-GOV-06
cleanup slice), per plan v3 "The Evidence Problem": the archived contradictions
become the adversarial fixtures the checks are proven against. Machine-absolute
paths in pre-images are re-anchored from the real machine prefix to
`/Users/fixture/...` before embedding (export boundary + path-anchor lint).

Sources (all at `15c958e06^`):
- `_DomainEngines/profiles/open_pipe_stress.DRAFT.yaml` (header block, the
  `profile_status` field line, the 5-entry `open_issues` block)
- `_DomainEngines/RULINGS_PUBLISHED.md` (stale closing paragraph)
- `_DomainEngines/DOMAIN_ENGINE_INDEX.md` (stale banner line)
- `_DomainEngines/_DECISIONS/D-T0-06_profile_adoption_lifecycle.md`
  (unannotated ruling line + progress note; POST form from HEAD)
- `_DomainEngines/_LATEST.md` (stale pointer framing line)
- `_DomainEngines/profiles/_validation/open_pipe_stress.validation.json`
  (abs-path evidence body; path re-anchored)

All fixture content lives in this `test_`-prefixed module as string constants:
loose fixture data files under `tools/` would fail
`tools/validation/validate_path_anchors.py` and ship into the public export.

Scenario tests use the in-test mutation pattern: build a fresh
`build_mini_repo`, overwrite/add files, run, assert (shared constants consumed
by other test modules are never mutated).
"""

from __future__ import annotations

import cmd_self_check
from harness_common import Severity
from test_self_check_fixtures import (
    RULINGS_PUBLISHED_MD,
    _findings,
    _has,
    _write,
    build_mini_repo,
)

# --- Verbatim pre-images (git show 15c958e06^) ---------------------------------

# open_pipe_stress.DRAFT.yaml lines 1-10 (the pre-cleanup header comment block).
PRE_PROFILE_HEADER = '''# OpenPipeStress Domain Engine Profile — DRAFT (NOT validated, NOT adopted)
#
# Status: DRAFT. This is an INSTANCE binding of the generic DomainEngineProfile
# contract to the OpenPipeStress engine. It is authored from the VERIFIED piping
# layout (schema-driven + persistence-abstracted), NOT from the persona's
# OpenPipeStress Example Binding (AGENT_DOMAIN_ENGINE.md:709-718), which is
# aspirational and diverges from reality (see FM-03 and ARTIFACT_INVENTORY.md).
#
# Nothing here is adopted. No deterministic profile-schema validator exists yet
# (TOOLMAKER handoff). No tool is invoked. No professional status is claimed.'''

# open_pipe_stress.DRAFT.yaml line 19 (profile_status + its historical-".DRAFT"
# comment), verbatim.
PRE_PROFILE_STATUS_FIELD = (
    '  profile_status: "ADOPTED"      # human Gate 2 approved by owner '
    '2026-06-21 (D-T0-06): governed-authoritative boundary. Validator passed '
    '(report: _validation/open_pipe_stress.validation.json). Filename retains '
    'historical ".DRAFT"; profile_status is authoritative. '
    '(see D-T0-02 / FM-01 / D-T0-06)')

# open_pipe_stress.DRAFT.yaml: the entire 5-entry open_issues block, verbatim.
# Entry 1 is the defective stale claim; entry 5 is the lawful RESOLVED-annotated
# in-block negative control.
PRE_OPEN_ISSUES_BLOCK = '''  open_issues:
    - "Profile stays DRAFT: no deterministic profile-schema validator exists yet (TOOLMAKER brief emitted; VALIDATED gated on it per D-T0-06)."
    - "Readable run/state/comparison instances are TBD (schemas exist; artifacts produced on demand)."
    - "operation_risk_class is proposed (engine-checkable vs engine-silent; D-T0-03), not yet implemented in the engine."
    - "Live binding (L2-L3) gated x4: tier-0 adoption, app-dev F3, piping D-21, DEC-041 automation condition (residency is NOT a blocker post D-T0-04)."
    - "RES-RECONCILE: RESOLVED 2026-06-21 (both halves published) — app-dev F1 via D-APP-44 @ d83e63b95; piping OPS-K-PRIV-1/SPEC §4.4/IP_AND_DATA_BOUNDARY via DEC-051 @ 9db0eef27. Net posture default-closed (see data_residency_reconciliation). No longer an open issue."'''

# RULINGS_PUBLISHED.md final line (the stale closing paragraph), verbatim.
PRE_RULINGS_CLOSING = (
    'Profile remains **DRAFT** (not VALIDATED — validator not built; D-T0-06) '
    'and **not ADOPTED**.')

# DOMAIN_ENGINE_INDEX.md line 7 (the stale banner; both contradicted halves —
# "No profile is `ADOPTED`. No decision is ruled." — on the one line), verbatim.
PRE_INDEX_BANNER = (
    '> **Status of everything under this root: `PROPOSAL` / unratified.** '
    'No profile is `ADOPTED`. No decision is ruled. No approval, SHA, or '
    'professional status is claimed (APEGA ceiling, K-AUTH-1). Publication is '
    'handed to CHANGE; DOMAIN_ENGINE does not commit.')

# D-T0-06 line 14 (the ruling line, UNANNOTATED pre-image), verbatim.
PRE_D_T0_06_RULING_LINE = (
    '**HumanRuling:** **Persona cadence** `DRAFT→VALIDATED→ADOPTED`; '
    '`VALIDATED` gated on the **TOOLMAKER profile-schema validator** (briefed, '
    'not built — see `TOOLMAKER_BRIEF-profile_schema_validator.md`). Profile '
    'stays DRAFT until the validator exists.   **RuledBy:** owner (in-session) '
    '  **Ruling SHA:** TBD (binds at CHANGE publish)   **Date:** 2026-06-21')

# D-T0-06 line 16 (the later progress note declaring the condition met), verbatim.
D_T0_06_PROGRESS_LINE = (
    '**Progress (2026-06-21):** validator built '
    '(`tools/validation/validate_domain_engine_profile.py`, 8/8 tests) and the '
    'profile **passed** (report '
    '`_DomainEngines/profiles/_validation/open_pipe_stress.validation.json`) → '
    '`DRAFT → VALIDATED`. **Human Gate 2 (`VALIDATED → ADOPTED`) ruled by the '
    'owner 2026-06-21** → ProfileStatus **ADOPTED**; the OpenPipeStress '
    'integration boundary is governed-authoritative. Lifecycle complete.')

# The POST (annotate-in-place) form of the same ruling line, verbatim from HEAD
# (the lawful K-STALE-2 resolution the cleanup slice applied).
POST_D_T0_06_RULING_LINE = (
    '**HumanRuling:** **Persona cadence** `DRAFT→VALIDATED→ADOPTED`; '
    '`VALIDATED` gated on the **TOOLMAKER profile-schema validator** (briefed, '
    'not built — see `TOOLMAKER_BRIEF-profile_schema_validator.md`). Profile '
    'stays DRAFT until the validator exists. *[Condition met 2026-06-21: '
    'validator built, profile **VALIDATED → ADOPTED** per the Progress note '
    'below; contradiction cleanup directed by D-GOV-06, ruled 2026-07-01.]*   '
    '**RuledBy:** owner (in-session)   **Ruling SHA:** TBD (binds at CHANGE '
    'publish)   **Date:** 2026-06-21')

# _LATEST.md line 3 (the stale pointer framing), verbatim.
PRE_LATEST_FRAMING = '**Latest snapshot (PROPOSAL, not yet owner-accepted):**'

# profiles/_validation/open_pipe_stress.validation.json, verbatim EXCEPT the
# machine-absolute profile_path, re-anchored to the /Users/fixture prefix.
PRE_VALIDATION_JSON_ABS = '''{
  "contract_source": "agents/AGENT_DOMAIN_ENGINE.md@77a327727",
  "findings": [],
  "profile_id": "open_pipe_stress",
  "profile_path": "/Users/fixture/ai-env/projects/example/_DomainEngines/profiles/open_pipe_stress.DRAFT.yaml",
  "profile_status": "ADOPTED",
  "result": "VALID",
  "schema": "domain-engine-profile-validation/v1",
  "summary": {
    "error_count": 0,
    "warning_count": 0
  },
  "tool": "validate_domain_engine_profile",
  "valid": true
}
'''

# Dangling refs MODELED ON the pre-image shapes (the pre-cleanup surfaces cited
# `ARTIFACT_INVENTORY.md` and per-tool schema paths that resolve nowhere).
# v1 limitation (documented): the real pre-image dangling refs were
# basename-only (e.g. `ARTIFACT_INVENTORY.md`); GEN-5 v1 deliberately captures
# only slash-bearing concrete refs, so these are re-shaped with their pre-image
# directory prefixes to pass the capture filters while still resolving nowhere.
UNRESOLVED_REF_LINES = (
    'Inventory cited at `_DomainEngines/ARTIFACT_INVENTORY.md` (pre-image dangling shape).\n'
    'Schema declared at `profiles/schemas/model_operation.schema.json` (pre-image dangling shape).\n'
    'Control ref (resolves; must NOT fire): `profiles/open_pipe_stress.DRAFT.yaml`.\n')

# GEN-6 basis fixtures (constructed, not pre-images; the live analogue is the
# seven D-GOV `FramedBy: governance_harness_plan_v3` lines).
BASIS_UNDISCLOSED = 'FramedBy:     fixture_plan_v9 (2026-07-01, merged)'
BASIS_DISCLOSED = 'FramedBy: fixture_plan_v9 (PROPOSAL, pending D-FIX-01)'
FIXTURE_PLAN_MD = '''# fixture plan v9

Status: PROPOSAL, pending D-FIX-01

Body.
'''
D_FIX_01_RULED_MD = '''# D-FIX-01 — Fixture ruling

Status:       RULED
HumanRuling:  recorded for the corpus test
'''


# --- Helpers --------------------------------------------------------------------

def _pre_profile_yaml(open_issues: bool = False) -> str:
    """Assemble a parseable profile from the verbatim pre-image pieces."""
    parts = [
        PRE_PROFILE_HEADER,
        "",
        "domain_profile:",
        '  schema_version: "1.0"',
        '  id: "open_pipe_stress"',
        '  name: "OpenPipeStress Piping-Stress Engine"',
        '  profile_version: "0.1-DRAFT"',
        PRE_PROFILE_STATUS_FIELD,
        '  integration_level: "MANUAL_BRIDGE"',
    ]
    if open_issues:
        parts.append(PRE_OPEN_ISSUES_BLOCK)
    return "\n".join(parts) + "\n"


def _line_of(text: str, needle: str) -> int:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    raise AssertionError(f"needle not found: {needle!r}")


# --- Scenario tests ---------------------------------------------------------------

def test_fixture_profile_status_conflict(tmp_path):
    repo = build_mini_repo(tmp_path)
    profile = repo / "_DomainEngines" / "profiles" / "open_pipe_stress.DRAFT.yaml"
    _write(profile, _pre_profile_yaml())
    report, _ = cmd_self_check.run_self_check(repo)
    hits = _findings(report, "HEADER_CONTRADICTS_STATUS")
    lines = {f.source_line for f in hits}
    assert lines == {1, 3, 9}  # '— DRAFT (NOT ...)', '# Status: DRAFT.',
    #                            '# Nothing here is adopted. No ... validator ...'
    assert all(f.severity is Severity.REVIEW for f in hits)
    _has(report, "FILENAME_CONTRADICTS_STATUS", "open_pipe_stress.DRAFT.yaml",
         severity=Severity.REVIEW)


def test_fixture_rulings_head_tail(tmp_path):
    repo = build_mini_repo(tmp_path)
    rulings = repo / "_DomainEngines" / "RULINGS_PUBLISHED.md"
    text = RULINGS_PUBLISHED_MD + "\n" + PRE_RULINGS_CLOSING + "\n"
    _write(rulings, text)
    report, _ = cmd_self_check.run_self_check(repo)
    appended_line = len(text.splitlines())
    _has(report, "HEAD_CONTRADICTS_TAIL", "RULINGS_PUBLISHED.md",
         line=appended_line, severity=Severity.REVIEW)


def test_fixture_index_banner(tmp_path):
    repo = build_mini_repo(tmp_path)
    index_text = (
        "# Domain Engine Integration — Control Area Index\n"
        "\n"
        + PRE_INDEX_BANNER + "\n"
        "\n"
        "| DOMAIN_ENGINE_ID | Engine | Profile | ProfileStatus |\n"
        "|---|---|---|---|\n"
        "| `open_pipe_stress` | OpenPipeStress | `profiles/open_pipe_stress.DRAFT.yaml`"
        " | **ADOPTED** (validated + Gate-2 adopted 2026-06-21) |\n")
    _write(repo / "_DomainEngines" / "DOMAIN_ENGINE_INDEX.md", index_text)
    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "BANNER_CONTRADICTS_REGISTER")
            if f.source_path.endswith("DOMAIN_ENGINE_INDEX.md")]
    # Both contradicted halves sit on the one banner line -> exactly one finding.
    assert [f.source_line for f in hits] == [3]
    assert hits[0].severity is Severity.REVIEW


def test_fixture_stale_open_issue(tmp_path):
    repo = build_mini_repo(tmp_path)
    profile = repo / "_DomainEngines" / "profiles" / "open_pipe_stress.DRAFT.yaml"
    text = _pre_profile_yaml(open_issues=True)
    _write(profile, text)
    report, _ = cmd_self_check.run_self_check(repo)
    hits = _findings(report, "STALE_OPEN_ISSUE")
    # Exactly ONE finding: entry 1 ("Profile stays DRAFT: ...").
    assert len(hits) == 1
    f = hits[0]
    assert f.severity is Severity.REVIEW
    assert f.invariant == "K-STALE-2"
    assert f.source_path.endswith("open_pipe_stress.DRAFT.yaml")
    assert f.source_line == _line_of(text, "Profile stays DRAFT:")
    assert "Profile stays DRAFT" in f.message
    assert "human-triaged" in f.message
    # Negative control: the RESOLVED-annotated entry 5 must NOT fire.
    resolved_line = _line_of(text, "RES-RECONCILE: RESOLVED")
    assert all(h.source_line != resolved_line for h in hits)


def test_fixture_stale_ruling_condition(tmp_path):
    repo = build_mini_repo(tmp_path)
    rec = (repo / "_DomainEngines" / "_DECISIONS"
           / "D-T0-06_profile_adoption_lifecycle.md")
    pre_text = ("# D-T0-06 — Profile adoption lifecycle + sub-gates\n"
                "\n" + PRE_D_T0_06_RULING_LINE + "\n"
                "\n" + D_T0_06_PROGRESS_LINE + "\n")
    _write(rec, pre_text)
    report, _ = cmd_self_check.run_self_check(repo)
    _has(report, "STALE_OPEN_ISSUE", "D-T0-06_profile_adoption_lifecycle.md",
         line=3, severity=Severity.REVIEW)

    # POST form (annotate-in-place resolution, verbatim at HEAD): no finding.
    post_text = ("# D-T0-06 — Profile adoption lifecycle + sub-gates\n"
                 "\n" + POST_D_T0_06_RULING_LINE + "\n"
                 "\n" + D_T0_06_PROGRESS_LINE + "\n")
    _write(rec, post_text)
    report, _ = cmd_self_check.run_self_check(repo)
    assert not [f for f in _findings(report, "STALE_OPEN_ISSUE")
                if f.source_path.endswith("D-T0-06_profile_adoption_lifecycle.md")]


def test_fixture_abs_path_leak(tmp_path):
    repo = build_mini_repo(tmp_path)
    validation = (repo / "_DomainEngines" / "profiles" / "_validation"
                  / "open_pipe_stress.validation.json")
    _write(validation, PRE_VALIDATION_JSON_ABS)
    notes_text = "# Pre-image validation body (fixture)\n\n" + PRE_VALIDATION_JSON_ABS
    _write(repo / "_DomainEngines" / "PRE_VALIDATION_NOTES.md", notes_text)
    report, _ = cmd_self_check.run_self_check(repo)
    evidence = _has(report, "ABS_PATH_IN_EVIDENCE",
                    "open_pipe_stress.validation.json",
                    line=_line_of(PRE_VALIDATION_JSON_ABS, "/Users/fixture/"),
                    severity=Severity.INFO)
    assert "permitted" in evidence.message
    _has(report, "ABS_PATH_IN_GOVERNED_SURFACE", "PRE_VALIDATION_NOTES.md",
         line=_line_of(notes_text, "/Users/fixture/"), severity=Severity.REVIEW)


def test_fixture_unresolved_refs(tmp_path):
    repo = build_mini_repo(tmp_path)
    reg = repo / "_DomainEngines" / "_DECISIONS" / "_REGISTER.md"
    reg.write_text(reg.read_text(encoding="utf-8") + "\n" + UNRESOLVED_REF_LINES,
                   encoding="utf-8")
    report, _ = cmd_self_check.run_self_check(repo)
    hits = [f for f in _findings(report, "UNRESOLVED_SOURCE_REF")
            if f.source_path.endswith("_REGISTER.md")]
    messages = " || ".join(f.message for f in hits)
    assert "_DomainEngines/ARTIFACT_INVENTORY.md" in messages
    assert "profiles/schemas/model_operation.schema.json" in messages
    assert all(f.severity is Severity.WARN for f in hits)
    # Resolvable control ref must NOT fire.
    assert "open_pipe_stress.DRAFT.yaml" not in messages


def test_fixture_draft_basis(tmp_path, monkeypatch):
    monkeypatch.setitem(cmd_self_check.KNOWN_BASIS_TARGETS,
                        "fixture_plan_v9", "plans/fixture_plan_v9.md")
    for sub in ("undisclosed", "disclosed", "ruled_closed"):
        (tmp_path / sub).mkdir()

    # (i) undisclosed citation of a PROPOSAL basis, pending decision NOT ruled
    #     -> REVIEW DRAFT_BASIS_AS_BINDING.
    repo = build_mini_repo(tmp_path / "undisclosed")
    _write(repo / "plans" / "fixture_plan_v9.md", FIXTURE_PLAN_MD)
    _write(repo / "docs" / "governance_harness" / "FIXTURE_BASIS_NOTE.md",
           "# Fixture basis note\n\n" + BASIS_UNDISCLOSED + "\n")
    report, _ = cmd_self_check.run_self_check(repo)
    f = _has(report, "DRAFT_BASIS_AS_BINDING", "FIXTURE_BASIS_NOTE.md",
             line=3, severity=Severity.REVIEW)
    assert "PROPOSAL, pending D-FIX-01" in f.message
    assert "outside this run's observation boundary" in f.message
    assert f.invariant == "K-CLAIM-1"

    # (ii) the citing line itself discloses the status -> no finding.
    repo = build_mini_repo(tmp_path / "disclosed")
    _write(repo / "plans" / "fixture_plan_v9.md", FIXTURE_PLAN_MD)
    _write(repo / "docs" / "governance_harness" / "FIXTURE_BASIS_NOTE.md",
           "# Fixture basis note\n\n" + BASIS_DISCLOSED + "\n")
    report, _ = cmd_self_check.run_self_check(repo)
    assert not _findings(report, "DRAFT_BASIS_AS_BINDING")
    assert not _findings(report, "DRAFT_BASIS_RULED_CLOSED")

    # (iii) pending decision has a RULED record -> INFO DRAFT_BASIS_RULED_CLOSED
    #       (conditional modeled on D-GOV-02's SHA-TBD rule).
    repo = build_mini_repo(tmp_path / "ruled_closed")
    _write(repo / "plans" / "fixture_plan_v9.md", FIXTURE_PLAN_MD)
    _write(repo / "docs" / "governance_harness" / "FIXTURE_BASIS_NOTE.md",
           "# Fixture basis note\n\n" + BASIS_UNDISCLOSED + "\n")
    _write(repo / "docs" / "governance_harness" / "_DECISIONS"
           / "D-FIX-01_fixture_ruling.md", D_FIX_01_RULED_MD)
    report, _ = cmd_self_check.run_self_check(repo)
    assert not _findings(report, "DRAFT_BASIS_AS_BINDING")
    f = _has(report, "DRAFT_BASIS_RULED_CLOSED", "FIXTURE_BASIS_NOTE.md",
             line=3, severity=Severity.INFO)
    assert "D-FIX-01 is RULED per" in f.message
    assert "D-FIX-01_fixture_ruling.md" in f.message


def test_fixture_latest_framing(tmp_path):
    # v1 has no dedicated pointer-FRAMING check: the pre-image _LATEST.md
    # framing line ("PROPOSAL, not yet owner-accepted") next to an ADOPTED
    # adoption-facts table fires NOTHING today. (GEN-7 audits pointer
    # CURRENCY — target resolution and newest-sibling — not framing prose,
    # and this fixture designates no target.) Asserted explicitly as the
    # recorded gap (rather than skipped) so a future check flips this test.
    repo = build_mini_repo(tmp_path)
    latest_text = (
        "# _LATEST — Domain Engine control-area pointer\n"
        "\n"
        + PRE_LATEST_FRAMING + "\n"
        "\n"
        "| Field | Value |\n"
        "|---|---|\n"
        "| ProfileStatus | **ADOPTED** (Gate 2 approved by owner 2026-06-21) |\n")
    _write(repo / "_DomainEngines" / "_LATEST.md", latest_text)
    report, _ = cmd_self_check.run_self_check(repo)
    latest_findings = [f for f in report.findings
                       if f.source_path.endswith("_LATEST.md")]
    assert latest_findings == []  # the recorded v1 gap: no check fires here
