import pytest
"""Tests for G0, the D-GOV-21 root materialization fence."""

from pathlib import Path

import validate_root_materialization_fence as g0


def _write_registration(root: Path, guards: dict) -> None:
    harness = root / "execution" / "_harness"
    harness.mkdir(parents=True, exist_ok=True)
    lines = ["guards:"]
    for name, fields in guards.items():
        lines.append(f"  {name}:")
        for key, value in fields.items():
            rendered = "true" if value is True else ("false" if value is False else str(value))
            lines.append(f"    {key}: {rendered}")
    (root / "execution" / "_harness" / "root_guards.yaml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


ALL_PASSING = {
    g: {"registered": True, "status": "passing"} for g in ("G1", "G2", "G3", "G4")
}


def test_pass_when_no_execution_dir(tmp_path):
    code, lines = g0.check(tmp_path)
    assert code == 0
    assert any("fence idle" in line for line in lines)


def test_pass_when_execution_has_only_control_plane(tmp_path):
    (tmp_path / "execution" / "_Coordination").mkdir(parents=True)
    code, _ = g0.check(tmp_path)
    assert code == 0


def test_block_when_pkg_exists_without_registration(tmp_path):
    (tmp_path / "execution" / "PKG-01_Example").mkdir(parents=True)
    code, lines = g0.check(tmp_path)
    assert code == 1
    assert any("absent or unreadable" in line for line in lines)


def test_block_when_del_exists_without_registration(tmp_path):
    (tmp_path / "execution" / "DEL-01-01_Example").mkdir(parents=True)
    code, _ = g0.check(tmp_path)
    assert code == 1


def test_block_when_registration_incomplete(tmp_path):
    (tmp_path / "execution" / "PKG-01_Example").mkdir(parents=True)
    partial = {g: {"registered": True, "status": "passing"} for g in ("G1", "G2", "G3")}
    _write_registration(tmp_path, partial)
    code, lines = g0.check(tmp_path)
    assert code == 1
    assert any("G4: not registered" in line for line in lines)


def test_block_when_guard_not_passing(tmp_path):
    (tmp_path / "execution" / "PKG-01_Example").mkdir(parents=True)
    guards = dict(ALL_PASSING)
    guards["G2"] = {"registered": True, "status": "failing"}
    _write_registration(tmp_path, guards)
    code, lines = g0.check(tmp_path)
    assert code == 1
    assert any("G2: status != passing" in line for line in lines)


def test_pass_when_all_guards_registered_and_passing(tmp_path):
    (tmp_path / "execution" / "PKG-01_Example").mkdir(parents=True)
    _write_registration(tmp_path, ALL_PASSING)
    code, lines = g0.check(tmp_path)
    assert code == 0
    assert any("materialization gate satisfied" in line for line in lines)


def test_pkg_file_not_directory_is_ignored(tmp_path):
    (tmp_path / "execution").mkdir()
    (tmp_path / "execution" / "PKG-notes.md").write_text("x", encoding="utf-8")
    code, _ = g0.check(tmp_path)
    assert code == 0


def test_live_repo_fence_passes():
    """The fence must PASS on the actual checkout. Before D-GOV-21 §6 step 9
    this held via the idle branch (no materialized children at ruling time,
    packet §10); since the step-9 materialization (D-GOV-25) it holds via the
    registration branch — G1-G4 registered and passing in
    execution/_harness/root_guards.yaml. Renamed from
    test_live_repo_state_is_clean in the step-9 tranche; assertion unchanged."""
    code, _ = g0.check(g0.repo_root())
    assert code == 0

# Full pinned subject fixture verifies actual published Git records, not authority labels.
from test_root_governance_state import complete, put
import json

def governance_registration(root,config):
    import yaml
    data={**config,'guards':{k:{'registered':True,'status':'passing'} for k in g0.REQUIRED_GUARDS}}
    put(root,str(g0.REGISTRATION_RELPATH),yaml.safe_dump(data))

def test_governance_full_real_subject(complete):
    root,_,config,_=complete;governance_registration(root,config)
    assert g0.check(root)[0]==0

@pytest.mark.parametrize('extra',['execution/DEL-99-New','execution/PKG-99-New','execution/other/DEL-99-New','execution/other/PKG-99-New','execution/PKG-01_Product_Definition_Normative_Basis_and_Authority/extra/DEL-99-New'])
def test_governance_nested_direct_extra_refused(complete,extra):
    root,_,config,_=complete;governance_registration(root,config);(root/extra).mkdir(parents=True)
    assert g0.check(root)[0]==1

def test_immutable_snapshot_carrier_names_not_active(complete):
    root,_,config,_=complete;governance_registration(root,config)
    (root/'execution/_ScopeChange/historical/PKG-99/DEL-99').mkdir(parents=True)
    assert g0.check(root)[0]==0

def test_governance_registration_cannot_claim_unknown_mode(complete):
    root,_,config,_=complete;config=dict(config,mode='unknown');governance_registration(root,config)
    assert g0.check(root)[0]==1

def test_accepted_deliverable_run_records_are_historical_evidence(complete):
    root,_,config,statuses=complete;governance_registration(root,config)
    evidence=root/str(Path(statuses[0]['Target']).parent)/'_run_records/DEL-01-01-OLD-RUN/PKG-HISTORICAL'
    evidence.mkdir(parents=True)
    assert g0.check(root)[0]==0
    # An identically named folder outside the registered source evidence home is live materialization.
    (root/'execution/other/_run_records/DEL-99-NEW').mkdir(parents=True)
    assert g0.check(root)[0]==1
