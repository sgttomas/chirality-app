#!/usr/bin/env python3
"""Tests for the prose-bullet-v1 parser plugin (ruled baseline material)."""

from __future__ import annotations

import prose_bullet_v1 as pb

LIFECYCLE = ["OPEN", "INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING", "ISSUED"]


# --- Rule 1 (strict; TS-parser list regex) -------------------------------------

def test_rule1_strict_hyphen():
    e = pb.parse_bullet("2026-04-30 - State set to OPEN (PREPARATION)")
    assert e.rule == "strict"
    assert e.caveat_class == pb.PARSED
    assert e.state == "OPEN"
    assert e.actor == "PREPARATION"
    assert e.date == "2026-04-30"


def test_rule1_strict_em_dash():
    e = pb.parse_bullet("2026-04-30 — State set to INITIALIZED (TASK+four-documents)")
    assert e.rule == "strict"
    assert e.state == "INITIALIZED"


def test_rule1_strict_trailing_notes():
    e = pb.parse_bullet(
        "2026-06-16 - State set to IN_PROGRESS (HUMAN) [Human authority: active code implementation underway.]")
    assert e.rule == "strict"
    assert e.state == "IN_PROGRESS"
    assert e.actor == "HUMAN"


def test_rule1_requires_full_line_shape():
    # Extra prose after the actor parens (no [notes] bracket) breaks the strict rule
    # but rule 2 still classifies it with assumptions.
    e = pb.parse_bullet("2026-04-30 - State set to CHECKING (X) with follow-up prose")
    assert e.rule == "verb_moved"
    assert e.caveat_class == pb.PARSED_WITH_ASSUMPTIONS


# --- Rules 2-9 -------------------------------------------------------------------

def test_rule2_verb_moved_variants():
    for verb in ("moved to", "advanced to", "changed to", "reset to",
                 "transitioned to", "set/verified as", "set to"):
        e = pb.parse_bullet(f"2026-06-04 - State {verb} CHECKING (reviewer note)")
        assert e.state == "CHECKING", verb
        # 'State set to CHECKING (reviewer note)' is the strict shape itself.
        assert e.caveat_class in (pb.PARSED, pb.PARSED_WITH_ASSUMPTIONS)


def test_rule2_case_insensitive():
    e = pb.parse_bullet("2026-06-04 - state moved to CHECKING per review")
    assert e.rule == "verb_moved"
    assert e.state == "CHECKING"


def test_rule3_advanced_deliverable():
    e = pb.parse_bullet("2026-06-04 - Owner review advanced this deliverable to CHECKING.")
    assert e.rule == "advanced_deliv"
    assert e.state == "CHECKING"


def test_rule4_advancing_from_to_captures_to_state():
    e = pb.parse_bullet(
        "2026-06-04 - advancing the record from IN_PROGRESS to CHECKING after re-review")
    assert e.rule == "advancing_from_to"
    assert e.state == "CHECKING"


def test_rule5_moving_to():
    e = pb.parse_bullet("2026-06-04 - moving the deliverable to CHECKING for inspection")
    assert e.rule == "moving_to"
    assert e.state == "CHECKING"


def test_rule6_transition_to():
    e = pb.parse_bullet("2026-06-04 - lifecycle transition to CHECKING recorded")
    assert e.rule == "transition_to"
    assert e.state == "CHECKING"


def test_rule7_set_state_to():
    e = pb.parse_bullet("2026-06-04 - re-ran the tool to set state to CHECKING")
    assert e.rule == "set_state_to"
    assert e.state == "CHECKING"


def test_rule8_remains():
    e = pb.parse_bullet(
        "2026-04-30 - Dependency register generated; state remains SEMANTIC_READY (TASK)")
    assert e.rule == "remains"
    assert e.state == "SEMANTIC_READY"


def test_rule8_does_not_match_status_remains():
    # 'status remains X' is a documented v1 limitation (only state/Current State).
    e = pb.parse_bullet(
        "2026-04-30 - Four-document P3 enrichment completed; status remains SEMANTIC_READY.")
    assert e.caveat_class == pb.UNPARSEABLE


def test_rule9_aligned_to():
    e = pb.parse_bullet("2026-06-04 - record realigned to CHECKING after audit")
    assert e.rule == "aligned_to"
    assert e.state == "CHECKING"


# --- Timezone/odd-date bullets ---------------------------------------------------

def test_timezone_date_fails_strict_but_rule2_matches():
    # A time suffix breaks the strict full-line regex; rule 2 still classifies.
    e = pb.parse_bullet("2026-06-04 14:32Z - State set to CHECKING (HUMAN)")
    assert e.rule == "verb_moved"
    assert e.caveat_class == pb.PARSED_WITH_ASSUMPTIONS
    assert e.state == "CHECKING"


# --- Deliberate v1 limitations (must stay UNPARSEABLE) ----------------------------

def test_no_issued_claim_disclaimer_not_parsed():
    e = pb.parse_bullet(
        "2026-06-20 - No ISSUED or professional-acceptance claim was made for this deliverable.")
    assert e.caveat_class == pb.UNPARSEABLE
    assert e.state is None


def test_evidence_promoted_to_committed_never_yields_state():
    e = pb.parse_bullet("2026-06-20 - Evidence promoted to COMMITTED for the run record.")
    assert e.caveat_class == pb.UNPARSEABLE
    assert e.state is None


def test_state_preserved_as_is_unparseable():
    e = pb.parse_bullet("2026-06-20 - state preserved as CHECKING during reconciliation")
    assert e.caveat_class == pb.UNPARSEABLE


def test_retained_kept_verified_updated_are_unparseable():
    for phrase in (
        "state retained SEMANTIC_READY (TASK+dependency-extract)",
        "state kept CHECKING",
        "status updated to CHECKING",
    ):
        e = pb.parse_bullet(f"2026-04-30 - Work done; {phrase}")
        assert e.caveat_class == pb.UNPARSEABLE, phrase


# --- Document-level parsing --------------------------------------------------------

DOC = """# Status: DEL-99-01

**Current State:** CHECKING
**Last Updated:** 2026-06-04
**Extra Field:** hello

## History
- 2026-04-30 - State set to OPEN (PREPARATION)
- 2026-05-01 - Evidence promoted to COMMITTED for the record.
- 2026-06-04 - State moved to CHECKING (re-review)
- 2026-06-05 - Narrative note without any state assertion.
- 2026-06-06 - Another narrative note.

## Next
- nothing
"""


def test_parse_status_document_fields_and_history():
    doc = pb.parse_status_document(DOC)
    assert doc.title == "Status: DEL-99-01"
    assert doc.current_state == "CHECKING"
    assert doc.last_updated == "2026-06-04"
    assert doc.fields["Extra Field"] == "hello"
    assert doc.doc_caveat_class == pb.PARSED
    assert len(doc.history) == 5  # bullets under '## Next' are outside the section


def test_last_state_assertion_and_trailing_unparseable_count():
    doc = pb.parse_status_document(DOC)
    assertion, trailing = pb.last_state_assertion(doc.history, LIFECYCLE)
    assert assertion is not None
    assert assertion.state == "CHECKING"
    assert assertion.rule == "verb_moved"
    assert trailing == 2  # two trailing narrative bullets after the assertion


def test_missing_current_state_is_doc_level_unparseable():
    doc = pb.parse_status_document("# T\n\n**Last Updated:** 2026-01-01\n\n## History\n")
    assert doc.doc_caveat_class == pb.UNPARSEABLE
    assert any("Current State" in c for c in doc.doc_caveats)


def test_missing_last_updated_is_doc_level_unparseable():
    doc = pb.parse_status_document("# T\n\n**Current State:** OPEN\n\n## History\n")
    assert doc.doc_caveat_class == pb.UNPARSEABLE


def test_non_lifecycle_states_are_skipped_by_last_state_assertion():
    text = (
        "# T\n\n**Current State:** CHECKING\n**Last Updated:** 2026-01-01\n\n"
        "## History\n"
        "- 2026-01-01 - State set to CHECKING (HUMAN)\n"
        "- 2026-01-02 - State set to PREPARATION (SCAFFOLD)\n"
    )
    doc = pb.parse_status_document(text)
    assertion, trailing = pb.last_state_assertion(doc.history, LIFECYCLE)
    # PREPARATION parses (in vocab) but is outside the manifest lifecycle states.
    assert assertion is not None
    assert assertion.state == "CHECKING"
    assert trailing == 0


def test_no_state_bearing_assertion_returns_none():
    text = (
        "# T\n\n**Current State:** OPEN\n**Last Updated:** 2026-01-01\n\n"
        "## History\n- 2026-01-01 - Narrative only.\n"
    )
    doc = pb.parse_status_document(text)
    assertion, trailing = pb.last_state_assertion(doc.history, LIFECYCLE)
    assert assertion is None
    assert trailing == 1
