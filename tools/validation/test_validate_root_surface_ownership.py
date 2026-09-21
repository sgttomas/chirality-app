"""Tests for G2, the D-GOV-21 static root surface-ownership register guard."""

import csv
from pathlib import Path

import yaml

import validate_root_surface_ownership as g2


def _write_register(root: Path, data: dict) -> None:
    path = root / g2.REGISTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _materialize(root: Path, name: str) -> None:
    (root / "execution" / name).mkdir(parents=True, exist_ok=True)


def _entry(entry_id: str = "PKG-01_Example", **overrides) -> dict:
    entry = {
        "id": entry_id,
        "kind": "package",
        "decomposition_ref": "TBD",
        "write_targets": [f"execution/{entry_id}/**"],
        "instruction_surface": False,
        "serialization": None,
    }
    entry.update(overrides)
    return entry


def _register(entries: list[dict] | None = None, **overrides) -> dict:
    data = {
        "schema": "root-surface-ownership/v1",
        "decomposition": "TBD",
        "entries": entries if entries is not None else [],
    }
    data.update(overrides)
    return data


def _write_decomposition_and_deliverable_register(
    root: Path, rows: list[dict[str, str]]
) -> str:
    decomposition_rel = "execution/_Decomposition/ACCEPTED.md"
    decomposition = root / decomposition_rel
    decomposition.parent.mkdir(parents=True, exist_ok=True)
    decomposition.write_text(
        "\n".join(
            [
                *(row["ParentPackageID"] for row in rows),
                *(row["DeliverableID"] for row in rows),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    register = decomposition.parent / "root_deliverable_register.csv"
    with register.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["DeliverableID", "ParentPackageID"]
        )
        writer.writeheader()
        writer.writerows(rows)
    return decomposition_rel


def _deliverable_entry(
    deliverable_id: str = "DEL-01-01_Example",
    package_id: str = "PKG-01_Example",
    **overrides,
) -> dict:
    entry = {
        "id": deliverable_id,
        "kind": "deliverable",
        "decomposition_ref": deliverable_id,
        "write_targets": [
            f"execution/{package_id}/1_Working/{deliverable_id}/**"
        ],
        "instruction_surface": False,
        "serialization": None,
    }
    entry.update(overrides)
    return entry


def test_pass_idle_when_no_structure_and_no_register(tmp_path):
    code, lines = g2.check(tmp_path)
    assert code == 0
    assert any("guard idle" in line for line in lines)


def test_pass_idle_with_control_plane_only(tmp_path):
    (tmp_path / "execution" / "_Coordination").mkdir(parents=True)
    code, _ = g2.check(tmp_path)
    assert code == 0


def test_block_when_structure_exists_without_register(tmp_path):
    _materialize(tmp_path, "PKG-01_Example")
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("is absent while PKG-*/DEL-* structure exists" in line for line in lines)


def test_pass_with_empty_register_and_no_structure(tmp_path):
    _write_register(tmp_path, _register([]))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines
    assert any("G2 PASS" in line for line in lines)


def test_pass_with_registered_materialized_package(tmp_path):
    _materialize(tmp_path, "PKG-01_Example")
    _write_register(tmp_path, _register([_entry()]))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_package_entry_behavior_does_not_require_tree_to_exist(tmp_path):
    """Regression: the deliverable correction must not change package semantics."""
    _write_register(tmp_path, _register([_entry()]))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_pass_with_registered_nested_deliverable_tree(tmp_path):
    package_id = "PKG-01_Example"
    deliverable_id = "DEL-01-01_Example"
    decomposition = _write_decomposition_and_deliverable_register(
        tmp_path,
        [{"DeliverableID": deliverable_id, "ParentPackageID": package_id}],
    )
    _materialize(tmp_path, package_id)
    (
        tmp_path
        / "execution"
        / package_id
        / "1_Working"
        / deliverable_id
    ).mkdir(parents=True)
    entries = [
        _entry(package_id, decomposition_ref=package_id),
        _deliverable_entry(deliverable_id, package_id),
    ]
    _write_register(tmp_path, _register(entries, decomposition=decomposition))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_block_when_declared_deliverable_tree_does_not_exist(tmp_path):
    package_id = "PKG-01_Example"
    deliverable_id = "DEL-01-01_Example"
    decomposition = _write_decomposition_and_deliverable_register(
        tmp_path,
        [{"DeliverableID": deliverable_id, "ParentPackageID": package_id}],
    )
    _materialize(tmp_path, package_id)
    entries = [
        _entry(package_id, decomposition_ref=package_id),
        _deliverable_entry(deliverable_id, package_id),
    ]
    _write_register(tmp_path, _register(entries, decomposition=decomposition))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("does not exist as a directory" in line for line in lines)


def test_block_on_foreign_tree_deliverable_entry(tmp_path):
    owning_package = "PKG-01_Example"
    foreign_package = "PKG-02_Foreign"
    deliverable_id = "DEL-01-01_Example"
    decomposition = _write_decomposition_and_deliverable_register(
        tmp_path,
        [{"DeliverableID": deliverable_id, "ParentPackageID": owning_package}],
    )
    _materialize(tmp_path, owning_package)
    _materialize(tmp_path, foreign_package)
    (
        tmp_path
        / "execution"
        / foreign_package
        / "1_Working"
        / deliverable_id
    ).mkdir(parents=True)
    entries = [
        _entry(owning_package, decomposition_ref=owning_package),
        _entry(foreign_package, decomposition_ref=foreign_package),
        _deliverable_entry(deliverable_id, foreign_package),
    ]
    _write_register(tmp_path, _register(entries, decomposition=decomposition))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("is not contained within its owning package tree" in line for line in lines)


def test_block_when_deliverable_entry_has_no_exact_register_match(tmp_path):
    package_id = "PKG-01_Example"
    registered_deliverable = "DEL-01-01_Registered"
    entry_deliverable = "DEL-01-01_Different"
    decomposition = _write_decomposition_and_deliverable_register(
        tmp_path,
        [
            {
                "DeliverableID": registered_deliverable,
                "ParentPackageID": package_id,
            }
        ],
    )
    _materialize(tmp_path, package_id)
    (
        tmp_path
        / "execution"
        / package_id
        / "1_Working"
        / entry_deliverable
    ).mkdir(parents=True)
    entries = [
        _entry(package_id, decomposition_ref=package_id),
        _deliverable_entry(entry_deliverable, package_id),
    ]
    # Preserve the existing decomposition-ref literal check so this test
    # isolates the new deliverable-register equality check.
    (tmp_path / decomposition).write_text(
        f"{package_id}\n{registered_deliverable}\n{entry_deliverable}\n",
        encoding="utf-8",
    )
    _write_register(tmp_path, _register(entries, decomposition=decomposition))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("no exact DeliverableID match" in line for line in lines)


def test_block_when_deliverable_decomposition_ref_is_not_its_exact_id(tmp_path):
    package_id = "PKG-01_Example"
    deliverable_id = "DEL-01-01_Example"
    decomposition = _write_decomposition_and_deliverable_register(
        tmp_path,
        [{"DeliverableID": deliverable_id, "ParentPackageID": package_id}],
    )
    _materialize(tmp_path, package_id)
    (
        tmp_path
        / "execution"
        / package_id
        / "1_Working"
        / deliverable_id
    ).mkdir(parents=True)
    wrong_ref = "DEL-99-99_Other"
    entries = [
        _entry(package_id, decomposition_ref=package_id),
        _deliverable_entry(
            deliverable_id, package_id, decomposition_ref=wrong_ref
        ),
    ]
    (tmp_path / decomposition).write_text(
        f"{package_id}\n{deliverable_id}\n{wrong_ref}\n",
        encoding="utf-8",
    )
    _write_register(tmp_path, _register(entries, decomposition=decomposition))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any(
        "decomposition_ref must exactly equal its DeliverableID" in line
        for line in lines
    )


def test_block_on_unregistered_materialized_package(tmp_path):
    _materialize(tmp_path, "PKG-01_Example")
    _materialize(tmp_path, "PKG-02_Unregistered")
    _write_register(tmp_path, _register([_entry()]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("unregistered materialized package" in line for line in lines)


def test_block_on_undeclared_own_tree(tmp_path):
    _materialize(tmp_path, "PKG-01_Example")
    entry = _entry(write_targets=["execution/PKG-99_Other/**"])
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("undeclared write target" in line for line in lines)


def test_block_on_absolute_write_target(tmp_path):
    entry = _entry(write_targets=["/var/tmp/anything", "execution/PKG-01_Example/**"])
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("not a repo-relative POSIX path" in line for line in lines)


def test_block_on_unmarked_instruction_surface_target(tmp_path):
    entry = _entry(write_targets=["execution/PKG-01_Example/**", "tools/validation/**"])
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("intersect the instruction surface" in line for line in lines)


def test_pass_on_marked_instruction_surface_target(tmp_path):
    entry = _entry(
        write_targets=["execution/PKG-01_Example/**", "docs/PRD_ROOT.md"],
        instruction_surface=True,
    )
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_dot_github_workflows_is_instruction_surface():
    """Regression: naive `lstrip('./')` ate the leading dot of `.github/`."""
    assert g2.intersects_instruction_surface(".github/workflows/governance-harness.yml")
    assert g2.intersects_instruction_surface("tools/validation/**")
    assert not g2.intersects_instruction_surface("execution/PKG-01_Example/**")


def test_claude_md_is_instruction_surface():
    """D-GOV-26 item 2: `CLAUDE.md` is the session-init instruction pointer."""
    assert g2.intersects_instruction_surface("CLAUDE.md")
    assert g2.intersects_instruction_surface("./CLAUDE.md")
    assert g2.intersects_instruction_surface("AGENTS.md")
    assert not g2.intersects_instruction_surface("projects/demo/CLAUDE.md")


def test_block_on_unmarked_claude_md_write_target(tmp_path):
    entry = _entry(write_targets=["execution/PKG-01_Example/**", "CLAUDE.md"])
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("intersect the instruction surface" in line for line in lines)
    assert any("CLAUDE.md" in line for line in lines)


def test_pass_on_marked_claude_md_write_target(tmp_path):
    entry = _entry(
        write_targets=["execution/PKG-01_Example/**", "CLAUDE.md"],
        instruction_surface=True,
    )
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_block_on_duplicate_entry_ids(tmp_path):
    _write_register(tmp_path, _register([_entry(), _entry()]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("duplicate register entry" in line for line in lines)


def test_block_on_bad_identifier_or_kind(tmp_path):
    entry = _entry()
    entry["id"] = "NotAPackage"
    entry["kind"] = "widget"
    _write_register(tmp_path, _register([entry]))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("is not a PKG-*/DEL-* identifier" in line for line in lines)
    assert any("kind" in line for line in lines)


def test_block_when_declared_decomposition_missing(tmp_path):
    _write_register(
        tmp_path,
        _register([_entry()], decomposition="execution/_Decomposition/ACCEPTED.md"),
    )
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("does not exist" in line for line in lines)


def test_block_on_tbd_ref_when_decomposition_declared(tmp_path):
    decomposition = tmp_path / "execution" / "_Decomposition" / "ACCEPTED.md"
    decomposition.parent.mkdir(parents=True, exist_ok=True)
    decomposition.write_text("PKG-01_Example\n", encoding="utf-8")
    _write_register(
        tmp_path,
        _register([_entry()], decomposition="execution/_Decomposition/ACCEPTED.md"),
    )
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("register/decomposition mismatch" in line for line in lines)


def test_block_on_ref_absent_from_declared_decomposition(tmp_path):
    decomposition = tmp_path / "execution" / "_Decomposition" / "ACCEPTED.md"
    decomposition.parent.mkdir(parents=True, exist_ok=True)
    decomposition.write_text("PKG-07_Something_Else\n", encoding="utf-8")
    _write_register(
        tmp_path,
        _register(
            [_entry(decomposition_ref="PKG-01_Example")],
            decomposition="execution/_Decomposition/ACCEPTED.md",
        ),
    )
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("does not appear in" in line for line in lines)


def test_pass_when_ref_present_in_declared_decomposition(tmp_path):
    decomposition = tmp_path / "execution" / "_Decomposition" / "ACCEPTED.md"
    decomposition.parent.mkdir(parents=True, exist_ok=True)
    decomposition.write_text("PKG-01_Example is accepted.\n", encoding="utf-8")
    _write_register(
        tmp_path,
        _register(
            [_entry(decomposition_ref="PKG-01_Example")],
            decomposition="execution/_Decomposition/ACCEPTED.md",
        ),
    )
    code, lines = g2.check(tmp_path)
    assert code == 0, lines


def test_overlapping_targets_are_info_not_block(tmp_path):
    """Static facts only: G2 makes no concurrency claim about shared targets."""
    shared = "execution/PKG-01_Example/shared"
    entries = [
        _entry("PKG-01_Example", write_targets=["execution/PKG-01_Example/**", shared]),
        _entry("PKG-02_Other", write_targets=["execution/PKG-02_Other/**", shared]),
    ]
    _write_register(tmp_path, _register(entries))
    code, lines = g2.check(tmp_path)
    assert code == 0, lines
    assert any("no concurrency claim" in line for line in lines)


def test_block_on_unknown_schema(tmp_path):
    _write_register(tmp_path, _register([], schema="something-else/v1"))
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("this guard understands" in line for line in lines)


def test_block_on_unparseable_register(tmp_path):
    path = tmp_path / g2.REGISTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("entries: [unterminated\n", encoding="utf-8")
    code, lines = g2.check(tmp_path)
    assert code == 1
    assert any("unparseable" in line for line in lines)


def test_live_repo_state_passes():
    """G2 must PASS on the actual checkout: no root PKG-*/DEL-* and no register
    is the lawful pre-instantiation condition (packet §5.3)."""
    code, _ = g2.check(g2.repo_root())
    assert code == 0

# Governance unit fixtures replace only the separately tested accepted-state
# resolver. No fixture acceptance is a live owner act.
import pytest


def _governance_fixture(root, monkeypatch):
    import root_governance_state as state_module
    successors = [
        {"target": "root::GOV-01", "write_targets": ["tools/checks/**"]},
        {"target": "chirality-runtime::DEL-02-06", "write_targets": ["projects/chirality-runtime/packages/core/**"]},
    ]
    state = {"successors": successors, "governance_ids": ["root::GOV-01"], "runtime_ids": ["chirality-runtime::DEL-02-06"]}
    monkeypatch.setattr(state_module, "load_governance_state", lambda *a, **kw: state)
    monkeypatch.setattr(state_module, "status_verification", lambda *a, **kw: "postimage")
    entries = [
        {"id": "root::GOV-01", "kind": "governance-control", "project": "root", "write_targets": ["tools/checks/**"], "instruction_surface": True, "read_targets": ["execution/PKG-01/1_Working/DEL-01/**"]},
        {"id": "chirality-runtime::DEL-02-06", "kind": "runtime-carrier", "project": "chirality-runtime", "write_targets": ["projects/chirality-runtime/packages/core/**"], "instruction_surface": False},
    ]
    data = {"schema": g2.REGISTER_SCHEMA, "mode": "governance-only", "governance_state": {"path": "fixture", "sha256": "0" * 64}, "entries": entries}
    return data, state


def test_governance_ownership_historical_reads(tmp_path, monkeypatch):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    _write_register(tmp_path, data)
    assert g2.check(tmp_path)[0] == 0


@pytest.mark.parametrize("target", ["runtime/**", "projects/other/**", "../outside/**", "/tmp/outside/**", "tools/checks*/**", "execution/PKG-01/**", "projects/chirality-runtime/packages/core/**"])
def test_governance_rejects_root_foreign_or_historical_write(tmp_path, monkeypatch, target):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    data["entries"][0]["write_targets"] = [target]
    assert g2.check_governance(tmp_path, data)[0] == 1


def test_governance_rejects_duplicate_owner(tmp_path, monkeypatch):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    data["entries"].append(dict(data["entries"][1]))
    assert g2.check_governance(tmp_path, data)[0] == 1


def test_governance_rejects_missing_successor(tmp_path, monkeypatch):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    data["entries"].pop()
    assert g2.check_governance(tmp_path, data)[0] == 1


def test_governance_unaccepted_state_blocks(tmp_path, monkeypatch):
    import root_governance_state as state_module
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    def reject(*a, **kw):
        raise state_module.GovernanceError("unaccepted transfer")
    monkeypatch.setattr(state_module, "load_governance_state", reject)
    assert g2.check_governance(tmp_path, data)[0] == 1


def test_governance_symlink_missing_descendant_escapes(tmp_path, monkeypatch):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    outside = tmp_path.parent / (tmp_path.name + "-foreign")
    outside.mkdir()
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools/checks").symlink_to(outside, target_is_directory=True)
    data["entries"][0]["write_targets"] = ["tools/checks/missing/leaf/**"]
    assert g2.check_governance(tmp_path, data)[0] == 1


def test_governance_rejects_kind_spoof(tmp_path, monkeypatch):
    data, _ = _governance_fixture(tmp_path, monkeypatch)
    data["entries"][1]["project"] = "root"
    assert g2.check_governance(tmp_path, data)[0] == 1
