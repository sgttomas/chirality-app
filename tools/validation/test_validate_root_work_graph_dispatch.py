"""Tests for G3, the D-GOV-21 pre-dispatch root work-graph guard."""

from pathlib import Path

import yaml

import validate_root_work_graph_dispatch as g3


def _write_graph(root: Path, data: dict, relpath: Path | None = None) -> Path:
    path = root / (relpath or g3.WORK_GRAPH_RELPATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _write_register(root: Path, entries: list[dict]) -> None:
    path = root / g3.REGISTER_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            {
                "schema": "root-surface-ownership/v1",
                "decomposition": "TBD",
                "entries": entries,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _node(node_id: str = "N1", **overrides) -> dict:
    node = {
        "id": node_id,
        "status": "active",
        "write_targets": [f"execution/PKG-01_Example/1_Working/{node_id}/**"],
    }
    node.update(overrides)
    return node


def _graph(nodes: list[dict] | None = None, **overrides) -> dict:
    data = {
        "schema": "root-work-graph/v1",
        "accepted_basis": "ba2b80bf25b6",
        "nodes": nodes if nodes is not None else [],
    }
    data.update(overrides)
    return data


def _marker_target(root: Path) -> str:
    relpath = "docs/governance_harness/tranche_manifests/T-1.yaml"
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("schema: instruction-tranche-manifest/v1\n", encoding="utf-8")
    return relpath


def _write_brief(root: Path, name: str, data: dict, markdown: bool = False) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    body = yaml.safe_dump(data, sort_keys=False)
    if markdown:
        path.write_text(f"---\n{body}---\n\n# Brief\n\nProse.\n", encoding="utf-8")
    else:
        path.write_text(body, encoding="utf-8")
    return path


def test_pass_idle_when_work_graph_absent(tmp_path):
    code, lines = g3.check(tmp_path)
    assert code == 0
    assert any("guard idle" in line for line in lines)


def test_pass_on_valid_graph(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1"), _node("N2")]))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines
    assert any("G3 PASS (CI mode)" in line for line in lines)


def test_note_when_register_absent(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1")]))
    code, lines = g3.check(tmp_path)
    assert code == 0
    assert any("NOT_APPLICABLE" in line for line in lines)


def test_block_on_unknown_schema(tmp_path):
    _write_graph(tmp_path, _graph([], schema="root-work-graph/v0"))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("this guard understands" in line for line in lines)


def test_block_on_missing_accepted_basis(tmp_path):
    _write_graph(tmp_path, _graph([], accepted_basis="HEAD"))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("accepted_basis" in line for line in lines)


def test_block_on_duplicate_node_id(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1"), _node("N1")]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("duplicate node id" in line for line in lines)


def test_block_on_unknown_status(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", status="running")]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("status" in line for line in lines)


def test_block_when_active_node_declares_no_write_targets(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", write_targets=[])]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("write_targets must be a non-empty list" in line for line in lines)


def test_complete_node_may_omit_write_targets(tmp_path):
    node = {"id": "N0", "status": "complete"}
    _write_graph(tmp_path, _graph([node, _node("N1")]))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_block_on_absolute_write_target(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", write_targets=["/var/tmp/x"])]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("not a repo-relative POSIX path" in line for line in lines)


def test_block_on_unknown_dependency_reference(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", depends_on=["N9"])]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("references unknown node" in line for line in lines)


def test_block_on_dependency_cycle(tmp_path):
    nodes = [_node("N1", depends_on=["N2"]), _node("N2", depends_on=["N1"])]
    _write_graph(tmp_path, _graph(nodes))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("dependency cycle" in line for line in lines)
    assert any("never linearizes a cycle" in line for line in lines)


def test_block_on_overlapping_active_targets(tmp_path):
    shared = "execution/PKG-01_Example/1_Working/shared/**"
    nodes = [
        _node("N1", write_targets=[shared]),
        _node("N2", write_targets=["execution/PKG-01_Example/1_Working/shared/sub/x.md"]),
    ]
    _write_graph(tmp_path, _graph(nodes))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("overlapping" in line and "no declared serialization" in line for line in lines)


def test_pass_when_overlap_is_serialized(tmp_path):
    shared = "execution/PKG-01_Example/1_Working/shared/**"
    nodes = [
        _node("N1", write_targets=[shared]),
        _node("N2", write_targets=[shared], serialized_after=["N1"]),
    ]
    _write_graph(tmp_path, _graph(nodes))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines
    assert any("serialized as declared" in line for line in lines)


def test_pass_when_overlap_has_one_declared_integration_owner(tmp_path):
    shared = "execution/PKG-01_Example/1_Working/shared/**"
    nodes = [
        _node("N1", write_targets=[shared], integration_owner="WORKING_ITEMS"),
        _node("N2", write_targets=[shared], integration_owner="WORKING_ITEMS"),
    ]
    _write_graph(tmp_path, _graph(nodes))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_pending_nodes_do_not_trigger_disjointness(tmp_path):
    shared = "execution/PKG-01_Example/1_Working/shared/**"
    nodes = [
        _node("N1", write_targets=[shared]),
        _node("N2", write_targets=[shared], status="pending"),
    ]
    _write_graph(tmp_path, _graph(nodes))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_dot_github_workflows_is_instruction_surface():
    """Regression: naive `lstrip('./')` ate the leading dot of `.github/`."""
    assert g3.intersects_instruction_surface(".github/workflows/governance-harness.yml")
    assert not g3.intersects_instruction_surface("execution/PKG-01_Example/**")


def test_claude_md_is_instruction_surface():
    """D-GOV-26 item 2: `CLAUDE.md` is the session-init instruction pointer."""
    assert g3.intersects_instruction_surface("CLAUDE.md")
    assert g3.intersects_instruction_surface("./CLAUDE.md")
    assert g3.intersects_instruction_surface("AGENTS.md")
    assert not g3.intersects_instruction_surface("projects/demo/CLAUDE.md")


def test_block_on_claude_md_target_without_marker(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", write_targets=["CLAUDE.md"])]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("intersect the instruction surface" in line for line in lines)


def test_pass_on_claude_md_target_with_valid_m2_marker(tmp_path):
    marker = _marker_target(tmp_path)
    node = _node("N1", write_targets=["CLAUDE.md"], m2_marker=f"M2:{marker}")
    _write_graph(tmp_path, _graph([node]))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_block_on_instruction_surface_without_marker(tmp_path):
    _write_graph(tmp_path, _graph([_node("N1", write_targets=["tools/validation/**"])]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("intersect the instruction surface" in line for line in lines)


def test_block_when_marker_names_missing_manifest(tmp_path):
    node = _node(
        "N1",
        write_targets=["tools/validation/**"],
        m2_marker="M2:docs/governance_harness/tranche_manifests/ABSENT.yaml",
    )
    _write_graph(tmp_path, _graph([node]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("which does not exist" in line for line in lines)


def test_pass_with_valid_m2_marker(tmp_path):
    marker = _marker_target(tmp_path)
    node = _node("N1", write_targets=["tools/validation/**"], m2_marker=f"M2:{marker}")
    _write_graph(tmp_path, _graph([node]))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_block_when_owner_absent_from_register(tmp_path):
    _write_register(tmp_path, [{"id": "PKG-01_Example", "write_targets": ["execution/PKG-01_Example/**"]}])
    _write_graph(tmp_path, _graph([_node("N1", owner="PKG-99_Missing")]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("has no entry in the G2" in line for line in lines)


def test_block_when_node_target_outside_owner_register_entry(tmp_path):
    _write_register(tmp_path, [{"id": "PKG-01_Example", "write_targets": ["execution/PKG-01_Example/**"]}])
    node = _node("N1", owner="PKG-01_Example", write_targets=["execution/PKG-02_Other/x.md"])
    _write_graph(tmp_path, _graph([node]))
    code, lines = g3.check(tmp_path)
    assert code == 1
    assert any("not covered by the register entry" in line for line in lines)


def test_pass_when_node_target_inside_owner_register_entry(tmp_path):
    _write_register(tmp_path, [{"id": "PKG-01_Example", "write_targets": ["execution/PKG-01_Example/**"]}])
    _write_graph(tmp_path, _graph([_node("N1", owner="PKG-01_Example")]))
    code, lines = g3.check(tmp_path)
    assert code == 0, lines


def test_dispatch_mode_pass(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1")]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.yaml",
        {
            "node": "N1",
            "write_targets": ["execution/PKG-01_Example/1_Working/N1/out.md"],
        },
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 0, lines
    assert any("G3 PASS (dispatch mode)" in line for line in lines)


def test_dispatch_mode_accepts_markdown_front_matter_brief(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1")]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.md",
        {
            "node": "N1",
            "write_targets": ["execution/PKG-01_Example/1_Working/N1/out.md"],
        },
        markdown=True,
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 0, lines


def test_dispatch_mode_blocks_undeclared_write_target(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1")]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.yaml",
        {"node": "N1", "write_targets": ["execution/PKG-02_Other/out.md"]},
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 1
    assert any("undeclared write target" in line for line in lines)


def test_dispatch_mode_blocks_non_active_node(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1", status="pending")]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.yaml",
        {
            "node": "N1",
            "write_targets": ["execution/PKG-01_Example/1_Working/N1/out.md"],
        },
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 1
    assert any("only 'active' nodes may be dispatched" in line for line in lines)


def test_dispatch_mode_blocks_unknown_node(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1")]))
    brief = _write_brief(
        tmp_path, "briefs/n9.yaml", {"node": "N9", "write_targets": ["execution/x"]}
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 1
    assert any("is not a node of the accepted work graph" in line for line in lines)


def test_dispatch_mode_blocks_brief_without_dispatch_block(tmp_path):
    graph_path = _write_graph(tmp_path, _graph([_node("N1")]))
    brief = tmp_path / "briefs" / "prose.md"
    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text("# Brief\n\nAll prose, no front matter.\n", encoding="utf-8")
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 1
    assert any("no machine-readable dispatch block" in line for line in lines)


def test_dispatch_mode_requires_m2_marker_on_instruction_surface_brief(tmp_path):
    marker = _marker_target(tmp_path)
    node = _node("N1", write_targets=["tools/validation/**"], m2_marker=f"M2:{marker}")
    graph_path = _write_graph(tmp_path, _graph([node]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.yaml",
        {"node": "N1", "write_targets": ["tools/validation/new_tool.py"]},
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 1
    assert any("no M2:<path> marker is declared" in line for line in lines)


def test_dispatch_mode_pass_with_matching_marker(tmp_path):
    marker = _marker_target(tmp_path)
    node = _node("N1", write_targets=["tools/validation/**"], m2_marker=f"M2:{marker}")
    graph_path = _write_graph(tmp_path, _graph([node]))
    brief = _write_brief(
        tmp_path,
        "briefs/n1.yaml",
        {
            "node": "N1",
            "write_targets": ["tools/validation/new_tool.py"],
            "m2_marker": f"M2:{marker}",
        },
    )
    code, lines = g3.check(tmp_path, graph_path, [brief])
    assert code == 0, lines


def test_dispatch_mode_operational_when_graph_missing(tmp_path):
    brief = _write_brief(tmp_path, "briefs/n1.yaml", {"node": "N1", "write_targets": ["x"]})
    code, lines = g3.check(tmp_path, tmp_path / "absent.yaml", [brief])
    assert code == 2
    assert any("OPERATIONAL" in line for line in lines)


def test_cli_rejects_half_specified_dispatch_mode():
    assert g3.main(["--work-graph", "some/graph.yaml"]) == 2


def test_live_repo_state_passes():
    """G3 must PASS on the actual checkout: no accepted root work graph exists
    yet, which is the lawful pre-instantiation condition (packet §5.3)."""
    code, _ = g3.check(g3.repo_root())
    assert code == 0

import hashlib
import json
import pytest


def _governance_graph_fixture(root, monkeypatch):
    from test_validate_root_surface_ownership import _governance_fixture, _write_register as write_ownership
    import root_governance_state as state_module
    register, state = _governance_fixture(root, monkeypatch)
    state.update(gate4={"subject_sha256": "a" * 64}, held_capabilities=["HELD-FEATURE"])
    write_ownership(root, register)
    monkeypatch.setattr(state_module, "verify_owner_act", lambda root, ref, expected: None)
    marker = _marker_target(root)
    node = _node(owner="root::GOV-01", write_targets=["tools/checks/out/**"], m2_marker="M2:" + marker,
                 execution_class="governance-migration", stage="dispatch", session_id="actual-child-1", parent_session_id="parent-1", capability_basis={"path": "owner.json"})
    evidence = {"kind": "child-execution", "node": "N1", "stage": "dispatch", "session_id": "actual-child-1", "parent_session_id": "parent-1"}
    raw = json.dumps(evidence).encode()
    (root / "execution-record.json").write_bytes(raw)
    node["child_evidence"] = {"path": "execution-record.json", "sha256": hashlib.sha256(raw).hexdigest()}
    graph = _graph([node], mode="governance-only", governance_state=register["governance_state"])
    return graph, node, evidence


def test_governance_actual_launch_no_return_required(tmp_path, monkeypatch):
    graph, _, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 0


@pytest.mark.parametrize("change", ["retired", "missing-child", "held", "unknown-owner", "foreign", "cycle", "parentage", "fan-in-without-return"])
def test_governance_dispatch_mutations(tmp_path, monkeypatch, change):
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    if change == "retired": node["owner"] = "DEL-02-06"
    elif change == "missing-child": node.pop("child_evidence")
    elif change == "held": node["runtime_capabilities"] = ["HELD-FEATURE"]
    elif change == "unknown-owner": node["owner"] = "root::GOV-UNKNOWN"
    elif change == "foreign": node["write_targets"] = ["projects/other/**"]
    elif change == "cycle": node["depends_on"] = ["N1"]
    elif change == "parentage": node["parent_session_id"] = "wrong-parent"
    elif change == "fan-in-without-return": node["stage"] = "fan-in"
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 1


def test_governance_owner_branch_evidence_rejected(tmp_path, monkeypatch):
    import root_governance_state as state_module
    graph, _, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    def reject(root, ref, expected):
        raise state_module.GovernanceError("owner act not published origin/main")
    monkeypatch.setattr(state_module, "verify_owner_act", reject)
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 1


def test_governance_complete_branch_predecessor_allowed(tmp_path, monkeypatch):
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    graph["nodes"].append(_node("PRE", status="complete", owner="root::GOV-01", write_targets=[]))
    node["depends_on"] = ["PRE"]
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 0


def test_governance_overlap_rejected(tmp_path, monkeypatch):
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    other = dict(node, id="N2")
    graph["nodes"].append(other)
    failures, _, _ = g3.check_graph(tmp_path, tmp_path / "graph.yaml", graph)
    assert any("overlap" in failure for failure in failures)


def test_governance_missing_register_cannot_skip(tmp_path, monkeypatch):
    graph, _, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    (tmp_path / g3.REGISTER_RELPATH).unlink()
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 1


def test_governance_fan_in_binds_actual_return(tmp_path, monkeypatch):
    graph, node, evidence = _governance_graph_fixture(tmp_path, monkeypatch)
    returned = b"Actual child result\n"
    (tmp_path / "return.md").write_bytes(returned)
    node["stage"] = evidence["stage"] = "fan-in"
    evidence["return"] = {"path": "return.md", "sha256": hashlib.sha256(returned).hexdigest()}
    raw = json.dumps(evidence).encode()
    (tmp_path / "execution-record.json").write_bytes(raw)
    node["child_evidence"]["sha256"] = hashlib.sha256(raw).hexdigest()
    path = _write_graph(tmp_path, graph)
    assert g3.check(tmp_path, path)[0] == 0
    (tmp_path / "return.md").write_bytes(b"Replaced return\n")
    assert g3.check(tmp_path, path)[0] == 1


def test_governance_graph_cannot_downgrade_to_legacy(tmp_path, monkeypatch):
    graph, _, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    graph.pop("mode")
    graph.pop("governance_state")
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 1


def test_governance_brief_binds_child_identity(tmp_path, monkeypatch):
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    graph_path = _write_graph(tmp_path, graph)
    brief = {"node": "N1", **{k: node[k] for k in ("write_targets", "m2_marker", "stage", "child_evidence", "session_id", "parent_session_id")}}
    brief_path = _write_brief(tmp_path, "brief.yaml", brief)
    assert g3.check(tmp_path, graph_path, [brief_path])[0] == 0
    brief["session_id"] = "other-child"
    _write_brief(tmp_path, "brief.yaml", brief)
    assert g3.check(tmp_path, graph_path, [brief_path])[0] == 1


@pytest.mark.parametrize("execution_class,expected", [("governance-migration", False), ("governance-operation", True)])
def test_governance_execution_class_effect_boundary(tmp_path, monkeypatch, execution_class, expected):
    import root_governance_state as state_module
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    original = state_module.load_governance_state
    observed = []
    def observe(*args, **kwargs):
        observed.append(kwargs.get("require_effective", False))
        return original(*args, **kwargs)
    monkeypatch.setattr(state_module, "load_governance_state", observe)
    node["execution_class"] = execution_class
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 0
    assert observed[0] is expected


@pytest.mark.parametrize("status", ["PREPARED", "APPLYING", "ROLLING_BACK", "ROLLED_BACK", "BLOCKED_PARTIAL"])
def test_governance_migration_cannot_dispatch_during_transaction(tmp_path, monkeypatch, status):
    import root_governance_state as state_module
    graph, _, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    state = state_module.load_governance_state(tmp_path, graph)
    (tmp_path / "journal.json").write_text(json.dumps({"status": status}))
    state["transaction"] = {"path": "journal.json", "sha256": None}
    assert g3.check(tmp_path, _write_graph(tmp_path, graph))[0] == 1


@pytest.mark.parametrize("mutation", ["none", "branch-only", "wrong-subject"])
def test_governance_published_owner_gate_with_real_git(tmp_path, monkeypatch, mutation):
    """Only state resolution is isolated; owner proof executes real local Git."""
    import subprocess
    import root_governance_state as state_module
    verify = state_module.verify_owner_act
    graph, node, _ = _governance_graph_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(state_module, "verify_owner_act", verify)
    def git(*args):
        return subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True, text=True).stdout.strip()
    git("init", "-q")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@example.invalid")
    owner = tmp_path / "owner.md"
    owner.write_text("Fixture acceptance of " + "a" * 64 + "\n")
    git("add", "owner.md")
    git("commit", "-qm", "Isolated fixture owner record\n\nCo-Authored-By: GPT-6 <noreply@openai.com>")
    published = git("rev-parse", "HEAD")
    git("update-ref", "refs/remotes/origin/main", published)
    if mutation == "branch-only":
        owner.write_text(owner.read_text() + "Branch-only amendment\n")
        git("add", "owner.md")
        git("commit", "-qm", "Isolated fixture branch amendment\n\nCo-Authored-By: GPT-6 <noreply@openai.com>")
    node["capability_basis"] = {"path": "owner.md", "sha256": hashlib.sha256(owner.read_bytes()).hexdigest(), "commit": git("rev-parse", "HEAD"), "subject_sha256": ("b" if mutation == "wrong-subject" else "a") * 64}
    result = g3.check(tmp_path, _write_graph(tmp_path, graph))[0]
    assert result == (0 if mutation == "none" else 1)

@pytest.mark.parametrize('capabilities', [['unknown-feature'], ['source_identity'], [None], [123], [''], 'feature'])
def test_migration_grant_never_opens_runtime_feature_alias(tmp_path,monkeypatch,capabilities):
    graph,node,_=_governance_graph_fixture(tmp_path,monkeypatch)
    node['runtime_capabilities']=capabilities
    assert g3.check(tmp_path,_write_graph(tmp_path,graph))[0]==1
