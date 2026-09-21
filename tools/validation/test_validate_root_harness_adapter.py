"""Tests for G1, the D-GOV-21 root harness adapter guard."""

from pathlib import Path

import yaml

import validate_root_harness_adapter as g1


def _seed_tree(root: Path) -> None:
    """Minimal root-shaped tree the adapter's declared pointers can reference."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "PRD_ROOT.md").write_text("# PRD\n", encoding="utf-8")
    coordination = root / "execution" / "_Coordination"
    coordination.mkdir(parents=True, exist_ok=True)
    (coordination / "_COORDINATION.md").write_text("# coord\n", encoding="utf-8")
    decisions = coordination / "_DECISIONS"
    decisions.mkdir(parents=True, exist_ok=True)
    (decisions / "_REGISTER.md").write_text("# register\n", encoding="utf-8")


def _adapter(**overrides) -> dict:
    data = {
        "schema": "root-harness-adapter/v1",
        "product": "chirality-root",
        "working_root": ".",
        "execution_root": "execution",
        "prd": "docs/PRD_ROOT.md",
        "coordination": "execution/_Coordination/_COORDINATION.md",
        "decision_register": "execution/_Coordination/_DECISIONS/_REGISTER.md",
        "status_glob": "execution/PKG-*/1_Working/DEL-*/_STATUS.md",
        "states": ["OPEN", "IN_PROGRESS", "ISSUED"],
        "parser_dialect": "prose-bullet-v1",
        "exclude_globs": [".archive/**"],
        "baselines": {
            "status_files": 0,
            "status_mismatch": 0,
            "pinned_at": "ba2b80bf25b6",
        },
    }
    data.update(overrides)
    return data


def _write_adapter(root: Path, data: dict) -> None:
    path = root / g1.ADAPTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _materialize(root: Path, name: str = "PKG-01_Example") -> Path:
    target = root / "execution" / name / "1_Working" / "DEL-01-01_Example"
    target.mkdir(parents=True, exist_ok=True)
    return target


def test_pass_idle_when_adapter_absent_and_nothing_materialized(tmp_path):
    code, lines = g1.check(tmp_path)
    assert code == 0
    assert any("guard idle" in line for line in lines)


def test_pass_idle_with_control_plane_only(tmp_path):
    _seed_tree(tmp_path)
    code, _ = g1.check(tmp_path)
    assert code == 0


def test_block_when_adapter_absent_but_package_materialized(tmp_path):
    _seed_tree(tmp_path)
    _materialize(tmp_path)
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("is absent while PKG-*/DEL-* structure exists" in line for line in lines)


def test_pass_with_valid_adapter(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter())
    code, lines = g1.check(tmp_path)
    assert code == 0, lines
    assert any("G1 PASS" in line and "schema-valid" in line for line in lines)


def test_pass_with_valid_adapter_and_matching_baseline(tmp_path):
    _seed_tree(tmp_path)
    status = _materialize(tmp_path) / "_STATUS.md"
    status.write_text("- state: OPEN\n", encoding="utf-8")
    _write_adapter(
        tmp_path,
        _adapter(
            baselines={
                "status_files": 1,
                "status_mismatch": 0,
                "pinned_at": "ba2b80bf25b6",
            }
        ),
    )
    code, lines = g1.check(tmp_path)
    assert code == 0, lines


def test_block_on_baseline_drift(tmp_path):
    _seed_tree(tmp_path)
    _materialize(tmp_path)  # no _STATUS.md written: observed count is 0
    _write_adapter(
        tmp_path,
        _adapter(
            baselines={
                "status_files": 7,
                "status_mismatch": 0,
                "pinned_at": "ba2b80bf25b6",
            }
        ),
    )
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("pinned baseline drift" in line for line in lines)


def test_block_on_unknown_schema(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter(schema="practitioner-harness-adapter/v1"))
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("this guard understands" in line for line in lines)


def test_block_on_missing_required_keys(tmp_path):
    _seed_tree(tmp_path)
    data = _adapter()
    del data["parser_dialect"]
    del data["states"]
    _write_adapter(tmp_path, data)
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("missing required keys" in line for line in lines)


def test_block_on_machine_absolute_pointer(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter(prd="/etc/PRD_ROOT.md"))
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("not a repo-relative POSIX path" in line for line in lines)


def test_block_on_parent_escaping_pointer(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter(coordination="../elsewhere/_COORDINATION.md"))
    code, lines = g1.check(tmp_path)
    assert code == 1


def test_block_on_missing_pointer_target(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter(prd="docs/PRD_DOES_NOT_EXIST.md"))
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("does not exist" in line for line in lines)


def test_block_on_wrong_working_root(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(tmp_path, _adapter(working_root="projects/chirality-root"))
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("working root is" in line for line in lines)


def test_block_on_bad_pinned_sha(tmp_path):
    _seed_tree(tmp_path)
    _write_adapter(
        tmp_path,
        _adapter(
            baselines={"status_files": 0, "status_mismatch": 0, "pinned_at": "HEAD"}
        ),
    )
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("hex SHA" in line for line in lines)


def test_block_on_undisposed_nonzero_mismatch(tmp_path):
    _seed_tree(tmp_path)
    status = _materialize(tmp_path) / "_STATUS.md"
    status.write_text("- state: OPEN\n", encoding="utf-8")
    _write_adapter(
        tmp_path,
        _adapter(
            baselines={
                "status_files": 1,
                "status_mismatch": 1,
                "pinned_at": "ba2b80bf25b6",
            }
        ),
    )
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("mismatch_disposition" in line for line in lines)


def test_pass_on_disposed_nonzero_mismatch(tmp_path):
    _seed_tree(tmp_path)
    status = _materialize(tmp_path) / "_STATUS.md"
    status.write_text("- state: OPEN\n", encoding="utf-8")
    _write_adapter(
        tmp_path,
        _adapter(
            baselines={
                "status_files": 1,
                "status_mismatch": 1,
                "pinned_at": "ba2b80bf25b6",
                "mismatch_disposition": "known control-deliverable exception",
            }
        ),
    )
    code, lines = g1.check(tmp_path)
    assert code == 0, lines


def test_block_on_unparseable_adapter(tmp_path):
    path = tmp_path / g1.ADAPTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("schema: [unterminated\n", encoding="utf-8")
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("unparseable" in line for line in lines)


def test_block_when_top_level_is_not_a_mapping(tmp_path):
    path = tmp_path / g1.ADAPTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("- just\n- a list\n", encoding="utf-8")
    code, lines = g1.check(tmp_path)
    assert code == 1
    assert any("not a mapping" in line for line in lines)


def test_live_repo_state_passes():
    """G1 must PASS on the 53-file live tree after the seven R7 transitions."""
    code, _ = g1.check(g1.repo_root())
    assert code == 0

from test_root_governance_state import complete, put
import pytest

def full_governance_adapter(root,state,config):
    data={**config,'schema':'root-harness-adapter/v1','product':'chirality-root','working_root':'.','execution_root':'execution','prd':'docs/PRD_ROOT.md','coordination':'execution/_Coordination/CURRENT_WORKPLAN.md','decision_register':'docs/governance_harness/_DECISIONS/_REGISTER.md','loop_init':'execution/_Coordination/LOOP_INIT.md','receipts':'execution/_Coordination/LOOP_RECEIPTS.md','status_glob':'execution/PKG-*/1_Working/DEL-*/_STATUS.md','parser_dialect':'root-historical-v1','states':['RETIRED'],'exclude_globs':['.archive/**'],'baselines':{'status_files':53,'status_mismatch':0,'pinned_at':state['gate4']['commit']}}
    for key in ['prd','coordination','decision_register','loop_init','receipts']:put(root,data[key],'Fixture pointer target\n')
    return data

def test_governance_adapter_full_published_subject(complete):
    root,state,config,_=complete;data=full_governance_adapter(root,state,config)
    put(root,str(g1.ADAPTER_RELPATH),yaml.safe_dump(data));assert g1.check(root)[0]==0

@pytest.mark.parametrize('field',['prd','coordination','decision_register','loop_init','receipts','mode','parser_dialect','states','exclude_globs','status_glob','baselines'])
def test_governance_adapter_each_required_surface(complete,field):
    root,state,config,_=complete;data=full_governance_adapter(root,state,config);data.pop(field)
    put(root,str(g1.ADAPTER_RELPATH),yaml.safe_dump(data));assert g1.check(root)[0]==1
