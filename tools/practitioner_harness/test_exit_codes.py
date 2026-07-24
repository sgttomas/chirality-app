#!/usr/bin/env python3
"""Exit-code and severity-policy tests (D-GOV-02, D-GOV-04, D-GOV-05)."""

from __future__ import annotations

import harness
from harness_common import (
    Finding,
    GENERATED_ROOT_NAME,
    Severity,
    cap_severity_for_unadopted_brief,
    compute_exit_code,
    make_finding,
)
from test_self_check_fixtures import build_mini_repo


def _f(severity: Severity) -> Finding:
    return Finding(severity=severity, code="X", dimension="d", message="m",
                   source_path="p")


def test_block_yields_1():
    assert compute_exit_code([_f(Severity.BLOCK), _f(Severity.INFO)]) == 1


def test_review_only_yields_0():
    assert compute_exit_code([_f(Severity.REVIEW), _f(Severity.WARN)]) == 0


def test_review_with_strict_yields_1():
    assert compute_exit_code([_f(Severity.REVIEW)], strict=True) == 1


def test_not_applicable_yields_0():
    assert compute_exit_code([_f(Severity.NOT_APPLICABLE)]) == 0
    assert compute_exit_code([_f(Severity.NOT_APPLICABLE)], strict=True) == 0


def test_no_findings_yields_0():
    assert compute_exit_code([]) == 0


def test_severity_cap_for_unadopted_brief():
    f = _f(Severity.BLOCK)
    capped = cap_severity_for_unadopted_brief(f)
    assert capped.severity is Severity.REVIEW
    assert "D-GOV-04" in capped.caveat
    # Non-BLOCK findings pass through unchanged.
    g = _f(Severity.INFO)
    assert cap_severity_for_unadopted_brief(g).severity is Severity.INFO


def test_draft_invariant_block_downgraded_unless_local_technical():
    # K-FUTURE-99 is synthetic: an uncataloged K-* ID labels DRAFT via the
    # fail-closed startswith fallback, keeping the BLOCK->REVIEW downgrade
    # path covered after the 2026-07-11 full ratification of the catalog.
    f = make_finding(Severity.BLOCK, "X", "d", "m", "p", invariant="K-FUTURE-99")
    assert f.severity is Severity.REVIEW
    assert "D-GOV-05" in f.caveat
    g = make_finding(Severity.BLOCK, "X", "d", "m", "p", invariant="K-FUTURE-99",
                     local_technical=True)
    assert g.severity is Severity.BLOCK
    # A cataloged (RATIFIED, 2026-07-11) invariant stays BLOCK.
    h = make_finding(Severity.BLOCK, "X", "d", "m", "p", invariant="K-CONFLICT-1")
    assert h.severity is Severity.BLOCK
    assert h.invariant_ratification == "RATIFIED"


def test_identity_dependent_check_with_allowlist_absent_exits_2(tmp_path, capsys):
    repo = build_mini_repo(tmp_path, with_allowlist=False)
    rc = harness.main(["--repo-root", str(repo), "self-check"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "D-GOV-04" in err


def test_missing_manifest_exits_2(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    manifest = repo / "projects" / "chirality-app-dev" / "_harness" / "adapter.yaml"
    manifest.unlink()
    rc = harness.main(["--repo-root", str(repo), "status", "--project", "app-dev"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


def test_generated_labeling_block_exits_1(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    stray = repo / GENERATED_ROOT_NAME / "stray.md"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text("no header here\n", encoding="utf-8")
    rc = harness.main(["--repo-root", str(repo), "self-check"])
    assert rc == 1
    out = capsys.readouterr().out
    assert "GENERATED_DISCLAIMER_MISSING" in out


def test_self_check_live_shape_exits_0_and_strict_1(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    assert harness.main(["--repo-root", str(repo), "self-check"]) == 0
    assert harness.main(["--repo-root", str(repo), "--strict", "self-check"]) == 1
    capsys.readouterr()
