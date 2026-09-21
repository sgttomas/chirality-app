import json
from pathlib import Path

import pytest

from build_workflow_index import CENTRAL, CORE, CORE_DISPLAY_NAMES, parse_navigation, parse_yaml_mapping, validate_and_build
from validate_skill_metadata import validate_skill_dir
from validate_workflow_metadata import validate_workflow_dir


ROOT = Path(__file__).resolve().parents[2]


def _core_navigation() -> list:
    return [
        {"name": name, **({"displayName": CORE_DISPLAY_NAMES[name]} if name in CORE_DISPLAY_NAMES else {})}
        for name in CORE
    ]


def _write_catalog(root: Path, specialist=None, superseded=None) -> None:
    (root / "workflows" / "catalog.yaml").write_text(json.dumps({
        "schema": "chirality-workflow-catalog/v1",
        "library": {"source": "bundled", "sourceRootId": "fixture-bundle"},
        "centralWorkflowNames": list(CENTRAL),
        "navigation": {"core": _core_navigation(), "specialist": specialist or [], "superseded": superseded or []},
    }))


def _write_package(workflows: Path, name: str) -> None:
    package = workflows / name
    package.mkdir()
    (package / "WORKFLOW.md").write_text(f"---\nname: {name}\ndescription: Fixture {name}\n---\n\n# {name}\n")


def _fixture_root(tmp_path: Path) -> Path:
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    _write_catalog(tmp_path)
    (workflows / "legacy-agents.json").write_text(json.dumps({"schema_version": 1, "aliases": {}}))
    (workflows / "legacy-methods.json").write_text(json.dumps({
        "schema": "chirality-legacy-methods/v1", "convertedWorkflowAliases": {},
        "historicalOnly": [], "unknownLegacyBehavior": "error",
    }))
    for name in CORE:
        _write_package(workflows, name)
        (workflows / name / "execution.json").write_text(json.dumps({"schema_version": 1, "compatible_roles": ["WORKING_ITEMS"]}))
    return tmp_path


SUPERSEDED = {
    "pandid-valve-tile": "pandid-valve-symbol-instance",
    "pdf2md-page": "pdf2md-page-full",
    "pdf2md-page-assets": "pdf2md-page-full",
}
# Group order follows catalog.yaml navigation.specialist authoring order.
SPECIALIST_GROUPS = [
    ("plan-organize", "Plan & organize", 6),
    ("research-understand", "Research & understand", 8),
    ("extract-documents", "Extract from documents", 15),
    ("create-publish-documents", "Create & publish documents", 8),
    ("build-maintain-software", "Build & maintain software", 4),
    ("estimate-cost", "Estimate & cost", 3),
    ("review-check", "Review & check", 10),
    ("manage-changes", "Manage changes", 5),
]
SPECIALIST_GROUP_SIZES = {key: size for key, _, size in SPECIALIST_GROUPS}


def test_root_index_is_fresh_and_classification_is_bounded():
    index = validate_and_build(ROOT)
    assert (ROOT / "workflows/index.json").read_text() == json.dumps(index, indent=2, sort_keys=False) + "\n"
    workflows = [item for item in index["methods"] if item["kind"] == "workflow"]
    skills = [item for item in index["methods"] if item["kind"] == "skill"]
    assert {item["name"] for item in workflows if item["central"]} == set(CENTRAL)
    assert {item["name"] for item in workflows if item["compatibility"] == "legacy"} == set(SUPERSEDED)
    assert all(item["compatibility"] == "canonical" for item in workflows if item["name"] not in SUPERSEDED)
    assert len(skills) == 8 and {item["compatibility"] for item in skills} == {"canonical"}
    assert not any("navigation" in item for item in skills)
    assert index["legacy"]["convertedWorkflowAliases"]["deliverable-consistency"] == {"kind": "skill", "name": "deliverable-consistency"}


def test_root_navigation_partition_is_complete_and_ordered():
    index = validate_and_build(ROOT)
    workflows = {item["name"]: item for item in index["methods"] if item["kind"] == "workflow"}
    assert set(workflows) == {folder.name for folder in (ROOT / "workflows").iterdir() if (folder / "WORKFLOW.md").is_file()}
    assert all("navigation" in item for item in workflows.values())
    core = sorted((item for item in workflows.values() if item["navigation"]["category"] == "core"), key=lambda item: item["navigation"]["order"])
    assert [item["name"] for item in core] == list(CORE)
    assert [item["navigation"]["order"] for item in core] == list(range(len(CORE)))
    assert {item["name"]: item["navigation"].get("displayName") for item in core if "displayName" in item["navigation"]} == CORE_DISPLAY_NAMES
    assert all(item["navigation"]["tier"] == "primary" and "group" not in item["navigation"] for item in core)
    specialist = [item for item in workflows.values() if item["navigation"]["category"] == "specialist"]
    assert len(specialist) == 59
    groups = {}
    group_identity = {}
    for item in specialist:
        navigation = item["navigation"]
        assert set(navigation) == {"category", "tier", "order", "group"}
        assert navigation["tier"] in ("primary", "supporting")
        assert set(navigation["group"]) == {"key", "label", "order"} and navigation["group"]["label"].strip()
        groups.setdefault(navigation["group"]["key"], []).append(navigation["order"])
        group_identity.setdefault(navigation["group"]["key"], set()).add((navigation["group"]["label"], navigation["group"]["order"]))
    assert {key: len(orders) for key, orders in groups.items()} == SPECIALIST_GROUP_SIZES
    assert all(sorted(orders) == list(range(len(orders))) for orders in groups.values())
    assert group_identity == {key: {(label, order)} for order, (key, label, _) in enumerate(SPECIALIST_GROUPS)}
    assert workflows["semantic-matrix-build"]["navigation"]["tier"] == "supporting"
    assert workflows["researcher"]["navigation"]["tier"] == "primary"
    superseded = {item["name"]: item for item in workflows.values() if item["navigation"]["category"] == "superseded"}
    assert {name: item["navigation"]["supersededBy"] for name, item in superseded.items()} == SUPERSEDED
    assert sorted(item["navigation"]["order"] for item in superseded.values()) == [0, 1, 2]
    assert all(item["compatibility"] == "legacy" for item in superseded.values())
    for replacement in SUPERSEDED.values():
        assert workflows[replacement]["navigation"]["category"] != "superseded"
    assert len(core) + len(specialist) + len(superseded) == len(workflows)


def test_navigation_partition_rejects_missing_extra_and_malformed_entries(tmp_path):
    root = _fixture_root(tmp_path)
    workflows = root / "workflows"
    _write_package(workflows, "helper")
    with pytest.raises(ValueError, match=r"missing=\['helper'\], extra=\[\]"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}, {"name": "ghost", "tier": "supporting"}]}])
    with pytest.raises(ValueError, match=r"missing=\[\], extra=\['ghost'\]"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper", "tier": "optional"}]}])
    with pytest.raises(ValueError, match="tier"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": " ", "workflows": [{"name": "helper"}]}])
    with pytest.raises(ValueError, match="non-empty label"):
        validate_and_build(root)
    _write_catalog(root, specialist=[
        {"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]},
        {"key": "tools", "label": "Again", "workflows": [{"name": "helper"}]},
    ])
    with pytest.raises(ValueError, match="more than once|not unique"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]}])
    descriptor = next(item for item in validate_and_build(root)["methods"] if item["name"] == "helper")
    assert descriptor["compatibility"] == "canonical"
    assert descriptor["navigation"] == {"category": "specialist", "tier": "primary", "order": 0, "group": {"key": "tools", "label": "Tools", "order": 0}}
    _write_package(workflows, "second")
    _write_catalog(root, specialist=[
        {"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]},
        {"key": "more", "label": "More", "workflows": [{"name": "second", "tier": "supporting"}]},
    ])
    by_name = {item["name"]: item for item in validate_and_build(root)["methods"]}
    assert by_name["second"]["navigation"] == {"category": "specialist", "tier": "supporting", "order": 0, "group": {"key": "more", "label": "More", "order": 1}}
    assert by_name["helper"]["navigation"]["group"]["order"] == 0


def test_navigation_superseded_requires_current_replacement(tmp_path):
    root = _fixture_root(tmp_path)
    workflows = root / "workflows"
    _write_package(workflows, "old-helper")
    _write_package(workflows, "helper")
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]}],
                   superseded=[{"name": "old-helper", "replacedBy": "vanished"}])
    with pytest.raises(ValueError, match="replacedBy must name an existing non-superseded workflow"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]}],
                   superseded=[{"name": "old-helper", "replacedBy": "old-helper"}])
    with pytest.raises(ValueError, match="replacedBy must name an existing non-superseded workflow"):
        validate_and_build(root)
    _write_catalog(root, specialist=[{"key": "tools", "label": "Tools", "workflows": [{"name": "helper"}]}],
                   superseded=[{"name": "old-helper", "replacedBy": "helper"}])
    by_name = {item["name"]: item for item in validate_and_build(root)["methods"]}
    assert by_name["old-helper"]["compatibility"] == "legacy"
    assert by_name["old-helper"]["navigation"] == {"category": "superseded", "tier": "primary", "order": 0, "supersededBy": "helper"}
    assert by_name["helper"]["compatibility"] == "canonical"
    assert all(by_name[name]["compatibility"] == "canonical" for name in CORE)


def test_navigation_core_is_fixed_and_display_names_are_bounded():
    with pytest.raises(ValueError, match="core must be exactly"):
        parse_navigation({"core": _core_navigation()[:6], "specialist": [], "superseded": []})
    reordered = list(reversed(_core_navigation()))
    with pytest.raises(ValueError, match="core must be exactly"):
        parse_navigation({"core": reordered, "specialist": [], "superseded": []})
    renamed = [dict(item) for item in _core_navigation()]
    renamed[0]["displayName"] = "Set up"
    with pytest.raises(ValueError, match="displayName"):
        parse_navigation({"core": renamed, "specialist": [], "superseded": []})
    with pytest.raises(ValueError, match="exactly core, specialist and superseded"):
        parse_navigation({"core": _core_navigation(), "specialist": []})
    placements = parse_navigation({"core": _core_navigation(), "specialist": [], "superseded": []})
    assert placements["create-workflow"] == {"category": "core", "tier": "primary", "order": 0}
    assert placements["project-setup"] == {"category": "core", "tier": "primary", "order": 1}
    assert placements["reconciliation"] == {"category": "core", "tier": "primary", "order": CORE.index("reconciliation"), "displayName": "Check project status"}


def test_workflow_purpose_metadata_reaches_descriptors(tmp_path):
    index = validate_and_build(ROOT)
    workflows = {item["name"]: item for item in index["methods"] if item["kind"] == "workflow"}
    expected_categories = {
        "review": "Review and validation",
        "reconciliation": "Review and validation",
        "pdf2md-orchestration": "Documents and drawings",
        "drawing-extract": "Documents and drawings",
        "dbm-publisher": "Documents and drawings",
    }
    for name, category in expected_categories.items():
        metadata = workflows[name]["metadata"]
        assert metadata["category"] == category
        assert isinstance(metadata["applicability"], str)
        assert metadata["applicability"].strip()

    root = _fixture_root(tmp_path)
    target_name = CENTRAL[0]
    target = root / "workflows" / target_name / "WORKFLOW.md"
    fixture_metadata = {"category": "Fixture group", "applicability": "Fixture use"}
    target.write_text(
        f"---\nname: {target_name}\ndescription: Fixture\nmetadata:\n"
        "  category: Fixture group\n  applicability: Fixture use\n---\n"
    )
    descriptor = next(item for item in validate_and_build(root)["methods"] if item["name"] == target_name)
    assert descriptor["metadata"] == fixture_metadata


def test_canonical_skill_execution_policies_and_catalog_projection():
    # Current policy expectations belong here, not in the one-time conversion
    # evidence or retired workflow packages. Role order has no policy meaning.
    expected_tools = {
        "chirality-change": None,
        "preparation": {"capabilities": ["read", "write", "bash", "report_coordination_notice", "ack_agent_update"]},
        "researcher": {"capabilities": ["read", "write", "bash", "report_coordination_notice", "ack_agent_update"]},
        "deliverable-consistency": {"commands": ["python3 tools/validation/scan_deliverable_consistency.py:*"]},
        "drawing-titleblock-page": {"commands": []},
        "proposal-format": {"commands": []},
        "software-code-review": {"commands": [
            "python3 tools/software_workflow/select_affected_checks.py:*",
            "python3 tools/software_workflow/validate_change_scope.py:*",
            "python3 tools/software_workflow/compare_structured.py:*",
            "python3 tools/software_workflow/verify_generated_manifest.py:*",
        ]},
        "software-defect-diagnosis": {"commands": [
            "python3 tools/software_workflow/discover_repository.py:*",
            "python3 tools/software_workflow/select_affected_checks.py:*",
            "python3 tools/software_workflow/run_registered_checks.py:*",
        ]},
    }
    index = validate_and_build(ROOT)
    by_name = {(item["kind"], item["name"]): item for item in index["methods"]}
    for skill_name, tools in expected_tools.items():
        target = json.loads((ROOT / ".agents/skills" / skill_name / "execution.json").read_text())
        assert set(target["compatible_roles"]) == {"HELPS_HUMANS", "WORKING_ITEMS", "TASK"}
        assert target.get("tools") == tools
        descriptor = by_name[("skill", skill_name)]
        assert descriptor["executionRoleIds"] == target["compatible_roles"]
        assert descriptor["execution"]["compatibleRoles"] == target["compatible_roles"]
        assert descriptor["execution"].get("tools") == tools


def test_absent_skill_execution_inherits_and_empty_roles_deny_all(tmp_path):
    root = _fixture_root(tmp_path)
    skill = root / ".agents/skills/portable"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: portable\ndescription: Portable\n---\n")
    method = next(item for item in validate_and_build(root)["methods"] if item["kind"] == "skill")
    assert method["executionRoleIds"] == ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]
    assert "execution" not in method
    (skill / "execution.json").write_text(json.dumps({"schema_version": 1, "compatible_roles": []}))
    method = next(item for item in validate_and_build(root)["methods"] if item["kind"] == "skill")
    assert method["executionRoleIds"] == []
    assert method["execution"]["compatibleRoles"] == []


def test_malformed_frontmatter_and_optional_workflow_execution(tmp_path):
    root = _fixture_root(tmp_path)
    target = root / "workflows" / CENTRAL[0]
    (target / "WORKFLOW.md").write_text("# no metadata\n")
    with pytest.raises(ValueError, match="frontmatter"):
        validate_and_build(root)
    (target / "WORKFLOW.md").write_text(f"---\nname: {CENTRAL[0]}\ndescription: fixed\n---\n")
    (target / "execution.json").unlink()
    method = next(item for item in validate_and_build(root)["methods"] if item["name"] == CENTRAL[0])
    assert method["executionRoleIds"] == ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]
    assert "execution" not in method
    (target / "execution.json").write_text(json.dumps({"schema_version": 1, "compatible_roles": []}))
    method = next(item for item in validate_and_build(root)["methods"] if item["name"] == CENTRAL[0])
    assert method["executionRoleIds"] == []
    assert method["execution"]["compatibleRoles"] == []
    (target / "execution.json").write_text(json.dumps({"schema_version": 1, "compatible_roles": "TASK"}))
    with pytest.raises(ValueError, match="malformed execution"):
        validate_and_build(root)


def test_resource_symlink_escape_fails(tmp_path):
    root = _fixture_root(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("outside")
    (root / "workflows" / CENTRAL[0] / "escape.txt").symlink_to(outside)
    with pytest.raises(ValueError, match="escaping resource"):
        validate_and_build(root)


def test_skill_package_symlink_escape_fails(tmp_path):
    root = _fixture_root(tmp_path)
    outside = tmp_path / "outside-skill"
    outside.mkdir()
    (outside / "SKILL.md").write_text("---\nname: escape\ndescription: Outside\n---\n")
    skills = root / ".agents/skills"
    skills.mkdir(parents=True)
    (skills / "escape").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="escaping skill package"):
        validate_and_build(root)


def test_skill_collection_symlink_escape_fails(tmp_path):
    root = _fixture_root(tmp_path)
    outside = tmp_path.parent / f"{tmp_path.name}-outside-skills"
    skill = outside / "portable"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: portable\ndescription: Outside\n---\n")
    (root / ".agents").mkdir()
    (root / ".agents/skills").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="skill collection escapes"):
        validate_and_build(root)


def test_frontmatter_delimiters_are_complete_lines(tmp_path):
    root = _fixture_root(tmp_path)
    target = root / "workflows" / CENTRAL[0] / "WORKFLOW.md"
    target.write_text(f"---\nname: {CENTRAL[0]}\ndescription: before---after\n---\n\n# Body\n")
    method = next(item for item in validate_and_build(root)["methods"] if item["name"] == CENTRAL[0])
    assert method["description"] == "before---after"


def test_method_name_rejects_empty_hyphen_segment(tmp_path):
    root = _fixture_root(tmp_path)
    target = root / "workflows" / CENTRAL[0]
    bad = root / "workflows/a--b"
    target.rename(bad)
    (bad / "WORKFLOW.md").write_text("---\nname: a--b\ndescription: Invalid name\n---\n")
    with pytest.raises(ValueError, match="invalid bundled workflow identity"):
        validate_and_build(root)


def test_method_name_fixture_enforces_length_and_segments():
    from build_workflow_index import NAME_RE
    fixture = json.loads((ROOT / "tools/validation/fixtures/method_discovery_v1.json").read_text())
    for case in fixture["methodNameCases"]:
        assert bool(NAME_RE.fullmatch(case["name"])) is case["valid"]


def test_standalone_validators_share_name_and_deny_all_contract(tmp_path):
    fixture = json.loads((ROOT / "tools/validation/fixtures/method_discovery_v1.json").read_text())
    for case in fixture["methodNameCases"]:
        skill = tmp_path / case["name"]
        skill.mkdir()
        (skill / "SKILL.md").write_text(f"---\nname: {case['name']}\ndescription: Fixture\n---\n")
        assert validate_skill_dir(skill, tmp_path)["valid"] is case["valid"]
    workflow = tmp_path / "deny-all"
    workflow.mkdir()
    (workflow / "WORKFLOW.md").write_text("---\nname: deny-all\ndescription: Fixture\n---\n")
    (workflow / "execution.json").write_text(json.dumps({"schema_version": 1, "compatible_roles": []}))
    assert validate_workflow_dir(workflow, tmp_path)["valid"]


def test_exact_central_refs_and_public_export_exclusion():
    registry = json.loads((ROOT / "agents/registry.json").read_text())
    assert registry["workflow_catalog"] == {
        "schema": "chirality-method-index/v1",
        "catalog": "workflows/catalog.yaml",
        "index": "workflows/index.json",
    }
    index = validate_and_build(ROOT)
    assert index["centralWorkflowNames"] == list(CENTRAL)
    exported = validate_and_build(ROOT, public_export=True)
    assert {(item["kind"], item["name"]) for item in index["methods"]} - {(item["kind"], item["name"]) for item in exported["methods"]} == {("skill", "chirality-change")}
    assert len(exported["methods"]) == len(index["methods"]) - 1
    assert not any(item["kind"] == "skill" and item["name"] == "chirality-change" for item in exported["methods"])
    assert not any("chirality-change" in str(item) for item in exported.get("diagnostics", []))


def test_shared_discovery_fixture_contract():
    fixture = json.loads((ROOT / "tools/validation/fixtures/method_discovery_v1.json").read_text())
    assert fixture["precedence"] == ["project", "user", "bundled"]
    collision = next(case for case in fixture["cases"] if case["id"] == "qualified-collision-precedence")
    assert collision["expected"]["selected"]["source"] == "project"
    assert len({candidate["sourceRootId"] for candidate in collision["candidates"]}) == 3
    malformed = next(case for case in fixture["cases"] if case["id"] == "malformed-higher-source-blocks")
    assert malformed["expected"]["selected"] is None
    assert malformed["expected"]["error"] == "MALFORMED_HIGHER_PRECEDENCE"
    for case in fixture["packageYamlCases"]:
        if "expectedError" in case:
            with pytest.raises(Exception, match="duplicate key"):
                parse_yaml_mapping(case["yaml"], case["id"])
        else:
            assert parse_yaml_mapping(case["yaml"], case["id"]) == case["expected"]
    assert next(case for case in fixture["frontmatterDocumentCases"] if case["id"] == "delimiter-substring-preserved")["expectedDescription"] == "before---after"
    assert next(case for case in fixture["methodNameCases"] if case["name"] == "a--b")["valid"] is False
    assert next(case for case in fixture["packageContainmentCases"] if case["id"] == "skill-package-symlink-escape")["expectedError"] == "PACKAGE_OUTSIDE_LIBRARY_ROOT"
    workflow_absent = next(case for case in fixture["workflowExecutionCases"] if case["id"] == "absent-companion-inherits")
    assert workflow_absent["expectedExecutionRoleIds"] == ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]


def test_canonical_skill_has_no_task_specific_companions(tmp_path):
    skill = tmp_path / "skills" / "portable"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: portable\ndescription: Portable skill\n---\n")
    assert validate_skill_dir(skill, tmp_path)["valid"]
    legacy = validate_skill_dir(skill, tmp_path, legacy_task_contract=True)
    assert not legacy["valid"]
    assert any("legacy TASK skill contract" in issue for issue in legacy["issues"])
    (skill / "SKILL.md").write_text(
        "---\nname: portable\ndescription: Portable skill\nmetadata:\n"
        "  chirality-skill-version: '1'\n  chirality-task-profile: NONE\n---\n"
    )
    for name in ("BRIEF_SCHEMA.md", "TOOL_POLICY.md", "QA_CHECKS.md"):
        (skill / name).write_text(f"# {name}\n")
    assert validate_skill_dir(skill, tmp_path, legacy_task_contract=True)["valid"]


def test_grouped_checkpoint_boundaries_use_accepted_snapshots():
    standard = (ROOT / "docs/DECOMPOSITION_STANDARD.md").read_text()
    assert "After every required human checkpoint is accepted" in standard
    assert "consumes that accepted snapshot" in standard

    for name in ("project-decomp", "software-decomp"):
        method = (ROOT / "workflows" / name / "resources/method.md").read_text()
        assert "_LATEST_GROUP1.md" in method
        assert "_LATEST_GROUP2.md" in method
        assert "_LATEST_ACCEPTED.md" in method
        assert "Resolve and consume the accepted group-1 snapshot" in method
        assert "Resolve and consume the accepted group-2 snapshot" in method

    domain = (ROOT / "workflows/domain-decomp/resources/method.md").read_text()
    for pointer in ("_LATEST_SOURCE.md", "_LATEST_GROUP1.md", "_LATEST_GROUP2.md", "_LATEST_ACCEPTED.md"):
        assert pointer in domain

    scope_change = (ROOT / "workflows/scope-change/resources/method.md").read_text()
    assert "Group-1 and\ngroup-2 snapshots live under `_ScopeChange/checkpoint_snapshots/`" in scope_change
    assert "Do not update `_LATEST.md` before checkpoint group 3 acceptance" in scope_change


def test_research_uses_grouped_domain_acceptance_with_legacy_fallback():
    contract = (ROOT / "workflows/research-orchestration/resources/contract.md").read_text()
    method = (ROOT / "workflows/research-orchestration/resources/method.md").read_text()
    assert "checkpoint_snapshots/_LATEST_ACCEPTED.md" in contract
    assert "checkpoint_snapshots/_LATEST_ACCEPTED.md" in method
    assert "LEGACY_ACCEPTED_GATE_POINTER" in contract
    assert "Gate6_Publication_Manifest.csv" in contract
    assert "clearly label that compatibility basis" in method
