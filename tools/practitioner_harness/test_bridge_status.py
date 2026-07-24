#!/usr/bin/env python3
"""Tests for the generated bridge-status view."""

from __future__ import annotations

import harness
import cmd_bridge_status
from test_self_check_fixtures import build_mini_repo


def _append(path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_bridge_status_derives_open_rows_profile_and_receipt(tmp_path):
    repo = build_mini_repo(tmp_path)
    app_register = (
        repo
        / "projects"
        / "chirality-app-dev"
        / "execution"
        / "_Coordination"
        / "_DECISIONS"
        / "_REGISTER.md"
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
    profile = repo / "_DomainEngines" / "profiles" / "open_pipe_stress.DRAFT.yaml"
    receipts = repo / "_DomainEngines" / "bridge" / "LOOP_RECEIPTS.md"
    receipts.parent.mkdir(parents=True, exist_ok=True)

    _append(app_register, "| D-APP-99 | Fixture bridge packet | AWAITING_RULING |\n")
    _append(piping_register, "| D-06 | Fixture release matrix | NOT_PREPARED |\n")
    _append(piping_register, "| D-21 | Fixture scoped gate | RULED |\n")
    _append(
        profile,
        '\n  open_issues:\n'
        '    - "Live binding (L2-L3) gated x4: tier-0 adoption, app-dev F3, '
        'piping D-21, DEC-041 automation condition."\n',
    )
    receipts.write_text(
        "# Bridge Loop Receipts\n\n"
        "## Receipts\n\n"
        "- **2026-07-02 - Receipt 0**\n"
        "  - Gate outcome: historical fixture.\n"
        "- **2026-07-03 - Receipt 1**\n"
        "  - Owner direction of record: fixture direction.\n"
        "  - Gate outcome: fixture gate waits on owner merge.\n"
        "  - Parked lanes: fixture lane remains owner-directed.\n",
        encoding="utf-8",
    )

    report = cmd_bridge_status.run_bridge_status(repo)
    md = report.render_markdown()

    assert report.summary["open_register_rows"] == 2
    assert report.summary["latest_receipt"] == "2026-07-03 - Receipt 1"
    assert report.summary["owner_act_rows"] >= 5
    assert report.summary["parked_lane_rows"] == 1
    assert report.summary["parked_lane_receipt_only"] == 1
    assert report.summary["live_binding_gate_rows"] == 4
    assert report.summary["blocked_on_links"] == 0
    assert "D-APP-99" in md
    assert "D-06" in md
    assert "Live binding (L2-L3) gated x4" in md
    assert "piping D-21" in md
    assert "D-21 State=RULED" in md
    assert "fixture gate waits on owner merge" in md
    assert "fixture lane remains owner-directed" in md
    assert "receipt-only" in md
    assert "tool never selects" in md


def test_bridge_status_indexes_status_blocked_on_tokens(tmp_path):
    repo = build_mini_repo(tmp_path)
    app_status = (
        repo
        / "projects"
        / "chirality-app-dev"
        / "execution"
        / "PKG-01_Fixture Pkg"
        / "1_Working"
        / "DEL-02-01_Match one"
        / "_STATUS.md"
    )
    app_status.write_text(
        app_status.read_text(encoding="utf-8").replace(
            "**Last Updated:** 2026-06-04",
            "**Last Updated:** 2026-06-04\n**blocked-on:** D-T0-09, D-30",
        ),
        encoding="utf-8",
    )
    register = (
        repo
        / "projects"
        / "chirality-piping"
        / "execution"
        / "_Coordination"
        / "_DECISIONS"
        / "_REGISTER.md"
    )
    _append(register, "| D-30 | Fixture package consumption | NOT_PREPARED |\n")

    report = cmd_bridge_status.run_bridge_status(repo)
    md = report.render_markdown()

    assert report.summary["blocked_on_links"] == 2
    assert "## Deliverable blocked-on links" in md
    assert "`D-30` | chirality-app-dev | `DEL-02-01_Match one`" in md
    assert "D-30 blocked deliverable chirality-app-dev/DEL-02-01_Match one" in md


def test_bridge_status_warns_on_latest_receipt_label_drift(tmp_path):
    repo = build_mini_repo(tmp_path)
    receipts = repo / "_DomainEngines" / "bridge" / "LOOP_RECEIPTS.md"
    receipts.parent.mkdir(parents=True, exist_ok=True)
    receipts.write_text(
        "# Bridge Loop Receipts\n\n"
        "## Receipts\n\n"
        "- **2026-07-03 - Receipt 1**\n"
        "  - Owner directions of record: pluralized fixture direction.\n"
        "  - Gate outcome: fixture gate.\n"
        "  - Parked lanes: PR #42.\n",
        encoding="utf-8",
    )

    report = cmd_bridge_status.run_bridge_status(repo)

    hits = [f for f in report.findings if f.code == "RECEIPT_BULLET_LABEL_DRIFT"]
    assert len(hits) == 1
    assert hits[0].severity.value == "WARN"
    assert "Owner direction of record" in hits[0].message


def test_bridge_status_cli_runs_on_minimal_fixture(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)

    rc = harness.main(["--repo-root", str(repo), "bridge-status"])

    out = capsys.readouterr().out
    assert rc == 0
    assert "Generated view" in out
    assert "# Bridge status - owner-shaped act pick-list" in out


def test_bridge_status_reports_pec_profile_as_draft_gate_open(tmp_path):
    repo = build_mini_repo(tmp_path)
    _write(
        repo / "_DomainEngines" / "profiles" / "pec.yaml",
        """domain_profile:
  id: "pec"
  profile_status: "DRAFT"
  profile_version: "0.1"
  integration_level: "MANUAL_BRIDGE"
""",
    )
    _write(
        repo
        / "projects"
        / "pec"
        / "execution"
        / "_Coordination"
        / "_DECISIONS"
        / "_REGISTER.md",
        "# PEC register\n\n| ID | Decision | State |\n|---|---|---|\n"
        "| D-PEC-01 | Fixture data residency export case | NOT_PREPARED |\n",
    )

    report = cmd_bridge_status.run_bridge_status(repo)
    md = report.render_markdown()
    facts = {fact.fact_id: fact.value for fact in report.facts}

    assert facts["bridge_status.profile.pec.profile_status"] == "DRAFT"
    assert facts["bridge_status.profile.pec.gate_posture"] == "Gate 2 open"
    assert "| `pec` | `DRAFT` | Gate 2 open | `MANUAL_BRIDGE` |" in md
    assert "D-PEC-01" in md
