"""App operational/harness receiving of Chirality library 2.1.0.

Executes the exact, unchanged Library ``library-v2.1.0`` code retained as a
partial test-source fixture under ``reference/library-v2.1.0/source`` (see its
``MANIFEST.json``). Nothing here reads a sibling Library checkout, Git objects
or the network. Cases marked "constructed" build packages or registries in a
temporary directory; they are App harness cases, not Library fixture cases.

This exercises development-agent practice only. It is not product role adoption:
the packaged App role set stays at its own pinned four-role basis, which the
final group of tests guards.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
RECEIVING = ROOT / "reference" / "library-v2.1.0"
SOURCE = RECEIVING / "source"
MANIFEST = json.loads((RECEIVING / "MANIFEST.json").read_text(encoding="utf-8"))
COMMIT = "c35b7bbc463f81c1fed566c744ea49d168d29eee"
NORMAL_ROLES = ("HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK")
ALL_ROLES = NORMAL_ROLES + ("INTERLOCUTOR",)
# Observed at library-v2.0.0 (2f981163), the App's prior operational selection.
V2_0_0_CHILDREN = {
    "HELP_HUMAN": {"HELPS_HUMANS", "WORKING_ITEMS", "TASK"},
    "HELPS_HUMANS": {"TASK"},
    "WORKING_ITEMS": {"TASK"},
    "TASK": set(),
}
CONSTRUCTED_SOURCE_ROOT_ID = "app-harness-constructed"


def _load(name: str, relative: str):
    """Load one fixture module by path without writing bytecode into it."""
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    previous, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


AGENTS = _load("library_v2_1_validate_agent_instructions", "tools/validation/validate_agent_instructions.py")
RESOLVER = _load("library_v2_1_resolve_workflow", "tools/workflow_runtime/resolve_workflow.py")
BUILDER = _load("library_v2_1_build_workflow_index", "tools/validation/build_workflow_index.py")
DISCOVERY = json.loads((SOURCE / "tools/validation/fixtures/method_discovery_v1.json").read_text(encoding="utf-8"))
REGISTRY = json.loads((SOURCE / "agents/registry.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def metadata_validator():
    """validate_workflow_metadata imports its sibling by bare module name."""
    saved = sys.modules.get("build_workflow_index")
    sys.modules["build_workflow_index"] = BUILDER
    try:
        yield _load("library_v2_1_validate_workflow_metadata", "tools/validation/validate_workflow_metadata.py")
    finally:
        if saved is None:
            sys.modules.pop("build_workflow_index", None)
        else:
            sys.modules["build_workflow_index"] = saved


# --- Source identity and self-contained closure ---------------------------------

def test_fixture_bytes_modes_and_closure_match_manifest():
    assert MANIFEST["commit"] == COMMIT and MANIFEST["tag"] == "library-v2.1.0"
    listed = {item["path"] for item in MANIFEST["files"]}
    present = {
        path.relative_to(SOURCE).as_posix()
        for path in SOURCE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    assert present == listed
    for item in MANIFEST["files"]:
        raw = (SOURCE / item["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], item["path"]
        assert len(raw) == item["bytes"], item["path"]
        assert item["gitMode"] == "100644" and item["readExtent"] == "full"
        header = b"blob %d\0" % len(raw)
        assert hashlib.sha1(header + raw).hexdigest() == item["gitBlob"], item["path"]


def test_unchanged_validator_passes_relocated_fixture_without_sibling_library(tmp_path):
    relocated = tmp_path / "isolated-source"
    shutil.copytree(SOURCE, relocated, ignore=shutil.ignore_patterns("__pycache__"))
    completed = subprocess.run(
        [sys.executable, "-I", "-B", str(relocated / "tools/validation/validate_agent_instructions.py"), "--json"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report == {"files_checked": 5, "errors": 0, "warnings": 0, "findings": []}


# --- Role registration (unchanged Library validator) -----------------------------

def test_registry_registers_interlocutor_as_opt_in_nondelegating_type2():
    roles = REGISTRY["roles"]
    assert tuple(roles) == ALL_ROLES
    assert REGISTRY["workflow_catalog"]["schema"] == "chirality-method-index/v1"
    advisor = roles["INTERLOCUTOR"]
    assert (advisor["type"], advisor["direct_entry"], advisor["default_for_new_chat"]) == (2, False, False)
    assert advisor["delegates_to"] == [] and advisor["allow_generalist_agent2"] is False
    assert "delegate_agent" not in advisor["tools"]
    assert [name for name, cfg in roles.items() if cfg["default_for_new_chat"]] == ["HELP_HUMAN"]
    parents = {name for name, cfg in roles.items() if "INTERLOCUTOR" in cfg["delegates_to"]}
    assert parents == {name for name, cfg in roles.items() if cfg["direct_entry"]}
    assert parents == {"HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS"}


def test_normal_roles_change_only_by_interlocutor_eligibility():
    for name, children in V2_0_0_CHILDREN.items():
        assert set(REGISTRY["roles"][name]["delegates_to"]) - {"INTERLOCUTOR"} == children
    unchanged = {item["path"] for item in MANIFEST["files"] if item["sameBytesAtLibraryV2_0_0"]}
    assert unchanged == {f"agents/AGENT_{name}.md" for name in NORMAL_ROLES}


def test_discovery_fixture_role_descriptors_agree_with_registry():
    projected = [
        {"id": name, "agentType": cfg["type"], "directEntry": cfg["direct_entry"],
         "defaultForNewChat": cfg["default_for_new_chat"], "instruction": cfg["instruction"]}
        for name, cfg in REGISTRY["roles"].items()
    ]
    described = [{k: v for k, v in item.items() if k != "description"} for item in DISCOVERY["roleDescriptors"]]
    assert described == projected


def _registry_copy(tmp_path):
    root = tmp_path / "registry-case"
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns("__pycache__"))
    return root


def _codes(root, mutate):
    path = root / "agents/registry.json"
    registry = json.loads(path.read_text())
    mutate(registry)
    path.write_text(json.dumps(registry))
    return {(f.code, f.message.split(":")[0]) for f in AGENTS.validate_registry(root)}


@pytest.mark.parametrize("label, mutate, expected", [
    ("interlocutor-direct-entry",
     lambda r: r["roles"]["INTERLOCUTOR"].update(direct_entry=True), {("ROLE_ENTRY", "INTERLOCUTOR")}),
    ("interlocutor-default-for-new-chat",
     lambda r: r["roles"]["INTERLOCUTOR"].update(default_for_new_chat=True), {("ROLE_DESCRIPTOR", "INTERLOCUTOR")}),
    ("interlocutor-delegates-task",
     lambda r: r["roles"]["INTERLOCUTOR"].update(delegates_to=["TASK"]), {("ROLE_DELEGATION", "INTERLOCUTOR")}),
    ("interlocutor-generalist-agent2",
     lambda r: r["roles"]["INTERLOCUTOR"].update(allow_generalist_agent2=True),
     {("ROLE_DELEGATION", "INTERLOCUTOR"), ("TYPE2_DELEGATION", "INTERLOCUTOR")}),
    ("interlocutor-delegate-tool",
     lambda r: r["roles"]["INTERLOCUTOR"]["tools"].append("delegate_agent"), {("TYPE2_DELEGATION", "INTERLOCUTOR")}),
    ("working-items-without-interlocutor-eligibility",
     lambda r: r["roles"]["WORKING_ITEMS"]["delegates_to"].remove("INTERLOCUTOR"), {("ROLE_DELEGATION", "WORKING_ITEMS")}),
    ("task-delegates-interlocutor",
     lambda r: r["roles"]["TASK"]["delegates_to"].append("INTERLOCUTOR"), {("ROLE_DELEGATION", "TASK")}),
])
def test_constructed_registry_violations_are_refused(tmp_path, label, mutate, expected):
    assert _codes(_registry_copy(tmp_path), mutate) == expected, label


def test_constructed_four_role_registry_no_longer_satisfies_2_1(tmp_path):
    """A consumer enumerating exactly four roles must deliberately support the fifth."""
    root = _registry_copy(tmp_path)

    def four(registry):
        del registry["roles"]["INTERLOCUTOR"]
        for cfg in registry["roles"].values():
            if "INTERLOCUTOR" in cfg["delegates_to"]:
                cfg["delegates_to"].remove("INTERLOCUTOR")

    (root / "agents/AGENT_INTERLOCUTOR.md").unlink()
    codes = {code for code, _ in _codes(root, four)}
    assert {"ROLE_REGISTRY", "ROLE_DELEGATION", "ROLE_ROSTER"} <= codes


# --- Method eligibility (unchanged Library builder, metadata validator, resolver) --

def _package(root: Path, kind: str, name: str, execution) -> Path:
    if kind == "workflow":
        folder, entry = root / "workflows" / name, "WORKFLOW.md"
    else:
        folder, entry = root / ".agents" / "skills" / name, "SKILL.md"
    folder.mkdir(parents=True)
    (folder / entry).write_text(f"---\nname: {name}\ndescription: Constructed App harness package\n---\n\n# {name}\n")
    if execution is not None:
        (folder / "execution.json").write_text(json.dumps(execution))
    return folder


@pytest.fixture()
def method_root(tmp_path):
    """Constructed declared root: fixture source plus a minimal catalog identity."""
    root = tmp_path / "method-root"
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns("__pycache__"))
    (root / "workflows").mkdir()
    (root / "workflows/catalog.yaml").write_text(json.dumps({
        "schema": "chirality-workflow-catalog/v1",
        "library": {"source": "bundled", "sourceRootId": CONSTRUCTED_SOURCE_ROOT_ID},
    }))
    return root


def _admitted(root: Path, kind: str, name: str, roles=ALL_ROLES):
    admitted, errors = [], {}
    for role in roles:
        try:
            RESOLVER.resolve(root, role, methods=[{"kind": kind, "name": name}])
            admitted.append(role)
        except ValueError as error:
            errors[role] = str(error)
    return admitted, errors


def test_builder_and_resolver_share_legacy_default_roles():
    assert BUILDER.LEGACY_DEFAULT_ROLES == RESOLVER.LEGACY_DEFAULT_ROLES == NORMAL_ROLES
    assert BUILDER.KNOWN_ROLES == tuple(REGISTRY["roles"]) == ALL_ROLES
    assert BUILDER.INDEX_SCHEMA == "chirality-method-index/v1"


# Resolver behaviour for each unchanged discovery-fixture execution case. Where the
# builder treats metadata as malformed, the resolver distinction is intentional:
# an omitted list inherits for registered non-INTERLOCUTOR roles, a string is malformed.
RESOLVER_EXPECTATION = {
    "absent-companion-inherits": (NORMAL_ROLES, "method incompatible with role"),
    "missing-compatible-roles-is-malformed": (NORMAL_ROLES, "method incompatible with role"),
    "empty-compatible-roles-denies-all": ((), "method incompatible with role"),
    "malformed-compatible-roles-type": ((), "malformed compatible_roles"),
    "explicit-interlocutor-opt-in": (("INTERLOCUTOR",), "method incompatible with role"),
    "empty-command-list-denies": (("TASK",), "method incompatible with role"),
}
EXECUTION_CASES = [("workflow", case) for case in DISCOVERY["workflowExecutionCases"]] + [
    ("skill", case) for case in DISCOVERY["skillExecutionCases"]]


@pytest.mark.parametrize("kind, case", EXECUTION_CASES, ids=[f"{k}:{c['id']}" for k, c in EXECUTION_CASES])
def test_unchanged_discovery_execution_cases(method_root, kind, case):
    folder = _package(method_root, kind, "fixture-case", case["executionJson"])
    if "expectedError" in case:
        assert case["expectedError"] == "MALFORMED_EXECUTION_METADATA"
        with pytest.raises(ValueError):
            BUILDER.parse_execution(folder, method_root, required=False)
    else:
        execution = BUILDER.parse_execution(folder, method_root, required=False)
        role_ids = execution["compatibleRoles"] if execution else list(BUILDER.LEGACY_DEFAULT_ROLES)
        assert role_ids == case["expectedExecutionRoleIds"]
        if "expectedExecution" in case:
            assert execution == case["expectedExecution"]
        if "expectedCommands" in case:
            assert execution["tools"]["commands"] == case["expectedCommands"]
    expected_roles, refusal = RESOLVER_EXPECTATION[case["id"]]
    admitted, errors = _admitted(method_root, kind, "fixture-case")
    assert tuple(admitted) == expected_roles
    assert all(message == refusal for message in errors.values()), errors
    if "expectedError" not in case:
        assert tuple(admitted) == tuple(case["expectedExecutionRoleIds"])


def test_interlocutor_needs_no_method_for_its_advisory_brief():
    result = RESOLVER.resolve(SOURCE, "INTERLOCUTOR")
    assert result["methods"] == [] and result["workflow"] is None
    instruction = next(i for i in MANIFEST["files"] if i["path"] == "agents/AGENT_INTERLOCUTOR.md")
    assert [(c["path"], c["sha256"]) for c in result["context"]] == [("agents/AGENT_INTERLOCUTOR.md", instruction["sha256"])]
    assert result["role_configuration"]["delegates_to"] == []


def test_explicit_qualified_interlocutor_method_and_mixed_selection(method_root):
    _package(method_root, "workflow", "advice-method", {"schema_version": 1, "compatible_roles": ["INTERLOCUTOR"]})
    _package(method_root, "workflow", "legacy-method", None)
    qualified = f"{CONSTRUCTED_SOURCE_ROOT_ID}:bundled:workflow:advice-method"
    result = RESOLVER.resolve(method_root, "INTERLOCUTOR", methods=[qualified])
    assert result["methods"] == [{"sourceRootId": CONSTRUCTED_SOURCE_ROOT_ID, "source": "bundled",
                                  "kind": "workflow", "name": "advice-method"}]
    with pytest.raises(ValueError, match="method incompatible with role"):
        RESOLVER.resolve(method_root, "INTERLOCUTOR", methods=[qualified, {"kind": "workflow", "name": "legacy-method"}])
    with pytest.raises(ValueError, match="method incompatible with role"):
        RESOLVER.resolve(method_root, "INTERLOCUTOR", workflow="legacy-method")


def test_empty_command_policy_denies_commands(method_root):
    _package(method_root, "skill", "no-commands", {"schema_version": 1, "compatible_roles": ["TASK"], "tools": {"commands": []}})
    result = RESOLVER.resolve(method_root, "TASK", methods=[{"kind": "skill", "name": "no-commands"}])
    assert result["effective_tools"]["commands"] == {"all_of": [[]]}
    assert RESOLVER.command_allowed(result["effective_tools"]["commands"], "python3", "tools/x.py", ["a"]) is False


def test_constructed_registered_custom_role_keeps_legacy_inheritance(method_root):
    """A registered custom role is resolver input only; the Library validator refuses it."""
    path = method_root / "agents/registry.json"
    registry = json.loads(path.read_text())
    custom = copy.deepcopy(registry["roles"]["TASK"])
    custom.update(description="Constructed custom role", instruction="agents/AGENT_TASK.md")
    registry["roles"]["CUSTOM_REVIEWER"] = custom
    path.write_text(json.dumps(registry))
    _package(method_root, "workflow", "inherited", None)
    _package(method_root, "workflow", "omitted-list", {"schema_version": 1})
    _package(method_root, "workflow", "task-only", {"schema_version": 1, "compatible_roles": ["TASK"]})
    _package(method_root, "workflow", "string-list", {"schema_version": 1, "compatible_roles": "CUSTOM_REVIEWER"})
    assert _admitted(method_root, "workflow", "inherited", ["CUSTOM_REVIEWER"])[0] == ["CUSTOM_REVIEWER"]
    assert _admitted(method_root, "workflow", "omitted-list", ["CUSTOM_REVIEWER"])[0] == ["CUSTOM_REVIEWER"]
    assert _admitted(method_root, "workflow", "task-only", ["CUSTOM_REVIEWER"])[1] == {"CUSTOM_REVIEWER": "method incompatible with role"}
    assert _admitted(method_root, "workflow", "string-list", ["CUSTOM_REVIEWER"])[1] == {"CUSTOM_REVIEWER": "malformed compatible_roles"}
    custom_named = _package(method_root, "workflow", "custom-named", {"schema_version": 1, "compatible_roles": ["CUSTOM_REVIEWER"]})
    assert _admitted(method_root, "workflow", "custom-named", ["CUSTOM_REVIEWER"])[0] == ["CUSTOM_REVIEWER"]
    with pytest.raises(ValueError, match="malformed compatible_roles"):
        BUILDER.parse_execution(custom_named, method_root, required=False)
    assert ("ROLE_REGISTRY", "registry.json") in {(f.code, Path(f.path).name) for f in AGENTS.validate_registry(method_root)}
    with pytest.raises(ValueError, match="unknown role"):
        RESOLVER.resolve(method_root, "UNREGISTERED_ROLE")


@pytest.mark.parametrize("compatible, valid", [
    (["INTERLOCUTOR"], True),
    (["TASK", "INTERLOCUTOR"], True),
    ("INTERLOCUTOR", False),
    (["ADVISOR"], False),
    ([], True),
])
def test_metadata_validator_compatible_roles(tmp_path, metadata_validator, compatible, valid):
    root = tmp_path / "metadata-root"
    (root / "tools").mkdir(parents=True)
    folder = _package(root, "workflow", "metadata-case", {"schema_version": 1, "compatible_roles": compatible})
    result = metadata_validator.validate_workflow_dir(folder, root)
    assert result["valid"] is valid, result


# --- Capability ceilings do not grant write targets ------------------------------

@pytest.mark.parametrize("brief, policy, targets, has_write", [
    (None, None, [], False),
    ({}, None, [], False),
    ({"AllowedWriteTargets": ["notes/advice.md"]}, None, ["notes/advice.md"], True),
    ({"AllowedWriteTargets": ["notes/advice.md"]}, {"host": {"capabilities": ["read"]}}, [], False),
])
def test_interlocutor_write_needs_explicit_targets_and_host_permission(brief, policy, targets, has_write):
    result = RESOLVER.resolve(SOURCE, "INTERLOCUTOR", policy=policy)
    assert "write" in REGISTRY["roles"]["INTERLOCUTOR"]["tools"]
    RESOLVER.bind_write_authority(result, brief)
    assert result["allowed_write_targets"] == targets
    assert ("write" in result["effective_tools"]["capabilities"]) is has_write
    assert result["enforcement"] == "instruction-asserted; host must enforce effective restrictions"


# --- Operational instructions and product boundary --------------------------------

def test_operational_roster_is_compatible():
    # AGENTS.md states the roster as relationship -> role texts: Agent 0 is
    # type 0, and "Type n" is type n. Every entry of a relationship cell must be
    # one backticked role name, so nothing in a cell goes unread; every registry
    # role must appear once, under the relationship that matches its type.
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    table = re.findall(r"^\| (Agent 0|Type [12]) \| (.+?) \|$", agents, re.MULTILINE)
    assert [relationship for relationship, _ in table] == ["Agent 0", "Type 1", "Type 2"]
    pairs = []
    for relationship, cell in table:
        for entry in cell.split(","):
            role = re.fullmatch(r"\s*`([A-Z_]+)`\s*", entry)
            assert role, f"unreadable roster entry under {relationship}: {entry!r}"
            pairs.append((role.group(1), "0" if relationship == "Agent 0" else relationship[-1]))
    assert len(pairs) == len(dict(pairs))
    assert dict(pairs) == {name: str(cfg["type"]) for name, cfg in REGISTRY["roles"].items()}


def test_packaged_product_role_set_remains_pinned_four_roles():
    instructions = ROOT / "app/src-tauri/resources/instructions"
    raw = (instructions / "roles.json").read_bytes()
    binding = json.loads((instructions / "ROLE_SET_SOURCE_BINDING.json").read_text())
    assert binding["basisCommit"] == "89acac6a3983c605820496d0d121c73bb2297706"
    assert binding["roleSet"]["sha256"] == hashlib.sha256(raw).hexdigest()
    assert [row["name"] for row in json.loads(raw)["roles"]] == list(NORMAL_ROLES)
    assert sorted(p.name for p in (instructions / "agents").iterdir()) == sorted(f"AGENT_{n}.md" for n in NORMAL_ROLES)
    # Check the existing source binding, not Rust/JSX formatting. Runtime enum,
    # parser and direct-entry assumptions are inspected in the owning account;
    # executing those unchanged product suites is outside this harness.
    for guidance in binding["guidance"]:
        content = (instructions / guidance["path"]).read_bytes()
        assert hashlib.sha256(content).hexdigest() == guidance["sha256"], guidance["path"]
    assert all(row["default_for_new_chat"] is False for row in json.loads(raw)["roles"])
