#!/usr/bin/env python3
"""Claim-language lint over the harness's own emitted templates and rendered
reports: no output may claim approved/issued/certified/sealed/safe/ready-for-
construction/closed status except quoting a labeled human source. This lints
templates, not data values (uppercase state tokens are data)."""

from __future__ import annotations

import brief_adoption
import cmd_brief
import cmd_bridge_status
import cmd_closeout
import cmd_coord_check
import cmd_drift
import cmd_evidence_check
import cmd_next
import cmd_run_validations
import cmd_scope_check
import cmd_self_check
import cmd_status
import evidence_records
import harness
import harness_common
from harness_common import FORBIDDEN_CLAIM_WORDS, find_claim_language
from test_self_check_fixtures import build_mini_repo

TEMPLATE_MODULES = (harness_common, cmd_brief, cmd_self_check, cmd_drift,
                    cmd_status, cmd_next, cmd_bridge_status, brief_adoption,
                    cmd_run_validations, evidence_records,
                    cmd_scope_check, cmd_evidence_check, cmd_closeout,
                    cmd_coord_check)


def test_find_claim_language_flags_lowercase_claims():
    assert find_claim_language("This deliverable is approved.") == ["approved"]
    assert "issued" in find_claim_language("the package was issued to the client")
    assert "ready for construction" in find_claim_language(
        "Ready for Construction status granted")


def test_find_claim_language_allows_state_tokens_and_pinned_phrases():
    assert find_claim_language("State set to ISSUED (HUMAN)") == []
    assert find_claim_language("states: OPEN, CHECKING, ISSUED, CLOSED") == []
    assert find_claim_language("Regenerate from project files; safe to delete.") == []


def test_registered_templates_carry_no_claim_language():
    for module in TEMPLATE_MODULES:
        for template in getattr(module, "TEMPLATES", []):
            assert find_claim_language(template) == [], (module.__name__, template)


def test_rendered_markdown_reports_carry_no_claim_language(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    runs = [
        ["status", "--project", "piping"],
        ["status", "--project", "app-dev"],
        ["status", "--domain-engines"],
        ["drift", "--all"],
        ["self-check"],
        ["bridge-status"],
        ["next"],
        ["brief", "--project", "piping", "--deliverable", "DEL-01-02",
         "--tranche-id", "TRB-lint-001"],
        # Verifies the brief the previous run generated (CANDIDATE, in
        # scratch): exit 0, one INFO finding, claim-clean output.
        ["brief", "--verify-adoption", "_harness_generated/briefs/TRB-lint-001.md"],
    ]
    for cmd in runs:
        rc = harness.main(["--repo-root", str(repo), *cmd])
        assert rc in (0, 1), cmd
        out = capsys.readouterr().out
        hits = find_claim_language(out)
        assert hits == [], (cmd, hits)


def test_forbidden_vocabulary_is_pinned():
    # The ruled list (constraint 3); state names as data are exempted by the
    # helper, not by shrinking this list.
    for word in ("approved", "issued", "certified", "sealed", "safe",
                 "ready for construction", "closed", "professionally accepted"):
        assert word in FORBIDDEN_CLAIM_WORDS
