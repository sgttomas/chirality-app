#!/usr/bin/env python3
"""Author and validate Root workflow metadata; never used as a runtime parser."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

CATALOG_SCHEMA = "chirality-workflow-catalog/v1"
INDEX_SCHEMA = "chirality-method-index/v1"
LEGACY_SCHEMA = "chirality-legacy-methods/v1"
NAME_RE = re.compile(r"^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCES = ("project", "user", "bundled")
ROLES = ("HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK")
CENTRAL = (
    "create-workflow",
    "project-setup",
    "project-decomp",
    "software-decomp",
    "domain-decomp",
    "research-orchestration",
    "scope-change",
)
# Ordered core navigation set: the central workflows plus the
# three everyday project workflows the App shows at first glance.
CORE = CENTRAL + ("task-management", "review", "reconciliation")
CORE_DISPLAY_NAMES = {
    "task-management": "Manage tasks",
    "review": "Review results",
    "reconciliation": "Check project status",
}
NAVIGATION_CATEGORIES = ("core", "specialist", "superseded")
NAVIGATION_TIERS = ("primary", "supporting")


def _contained_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"invalid resource path: {relative!r}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing or escaping resource: {relative}")
    return path


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain an object")
    return value


def _load_catalog(path: Path) -> dict:
    # JSON is a YAML 1.2 subset. Root emits that strict subset so authoring and
    # validation require no second YAML parser implementation.
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("catalog must contain a mapping")
    return value


def _descriptor(entry: dict, library: dict, central: bool, navigation: dict | None) -> dict:
    descriptor = {
        "kind": entry["kind"],
        "name": entry["name"],
        "source": library["source"],
        "sourceRootId": library["sourceRootId"],
        "description": entry["description"],
        "central": central,
        "compatibility": entry["compatibility"],
        "executionRoleIds": entry["executionRoleIds"],
        "resources": entry["resources"],
    }
    if navigation is not None:
        descriptor["navigation"] = navigation
    if entry.get("execution") is not None:
        descriptor["execution"] = entry["execution"]
    if entry.get("metadata") is not None:
        descriptor["metadata"] = entry["metadata"]
    return descriptor


def _navigation_name(value: object, where: str) -> str:
    if not isinstance(value, str) or not NAME_RE.fullmatch(value):
        raise ValueError(f"navigation {where}: invalid workflow name {value!r}")
    return value


def parse_navigation(navigation: object) -> dict[str, dict]:
    """Validate the catalog navigation partition and return per-workflow descriptors.

    Every bundled workflow must appear exactly once across core, the specialist
    groups, and superseded. The caller compares the returned names against the
    discovered packages so missing and extra names are reported precisely.
    """
    if not isinstance(navigation, dict) or set(navigation) != set(NAVIGATION_CATEGORIES):
        raise ValueError("navigation must contain exactly core, specialist and superseded")
    core, specialist, superseded = (navigation[key] for key in NAVIGATION_CATEGORIES)
    if not isinstance(core, list) or not isinstance(specialist, list) or not isinstance(superseded, list):
        raise ValueError("navigation categories must be lists")
    placements: dict[str, dict] = {}

    def place(name: str, descriptor: dict) -> None:
        if name in placements:
            raise ValueError(f"navigation places workflow more than once: {name}")
        placements[name] = descriptor

    core_names = []
    for order, item in enumerate(core):
        if not isinstance(item, dict) or not {"name"} <= set(item) <= {"name", "displayName"}:
            raise ValueError("navigation core entries must contain name and optional displayName only")
        name = _navigation_name(item.get("name"), "core")
        core_names.append(name)
        expected_display = CORE_DISPLAY_NAMES.get(name)
        if item.get("displayName") != expected_display:
            raise ValueError(f"navigation core displayName for {name} must be {expected_display!r}")
        descriptor = {"category": "core", "tier": "primary", "order": order}
        if expected_display is not None:
            descriptor["displayName"] = expected_display
        place(name, descriptor)
    if tuple(core_names) != CORE:
        raise ValueError(f"navigation core must be exactly {list(CORE)} in order; got {core_names}")

    group_keys = set()
    for group_order, group in enumerate(specialist):
        if not isinstance(group, dict) or set(group) != {"key", "label", "workflows"}:
            raise ValueError("navigation specialist groups must contain key, label and workflows only")
        key = _navigation_name(group.get("key"), "specialist group key")
        if key in group_keys:
            raise ValueError(f"navigation specialist group key is not unique: {key}")
        group_keys.add(key)
        label = group.get("label")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"navigation specialist group {key} requires a non-empty label")
        workflows = group.get("workflows")
        if not isinstance(workflows, list) or not workflows:
            raise ValueError(f"navigation specialist group {key} requires a non-empty workflow list")
        for order, item in enumerate(workflows):
            if not isinstance(item, dict) or not {"name"} <= set(item) <= {"name", "tier"}:
                raise ValueError(f"navigation specialist group {key} entries must contain name and optional tier only")
            name = _navigation_name(item.get("name"), f"specialist group {key}")
            tier = item.get("tier", "primary")
            if tier not in NAVIGATION_TIERS:
                raise ValueError(f"navigation tier for {name} must be one of {list(NAVIGATION_TIERS)}")
            place(name, {
                "category": "specialist", "tier": tier, "order": order,
                "group": {"key": key, "label": label, "order": group_order},
            })

    superseded_names = []
    for order, item in enumerate(superseded):
        if not isinstance(item, dict) or set(item) != {"name", "replacedBy"}:
            raise ValueError("navigation superseded entries must contain name and replacedBy only")
        name = _navigation_name(item.get("name"), "superseded")
        replaced_by = _navigation_name(item.get("replacedBy"), f"superseded {name} replacedBy")
        superseded_names.append((name, replaced_by))
        place(name, {"category": "superseded", "tier": "primary", "order": order, "supersededBy": replaced_by})
    for name, replaced_by in superseded_names:
        target = placements.get(replaced_by)
        if target is None or target["category"] == "superseded":
            raise ValueError(f"navigation superseded {name} replacedBy must name an existing non-superseded workflow: {replaced_by}")
    return placements


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"found duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def parse_yaml_mapping(raw: str, label: str) -> dict:
    value = yaml.load(raw, Loader=_UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{label}: YAML metadata must be a mapping")
    return value


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: WORKFLOW.md must start with YAML frontmatter")
    try:
        delimiter = lines.index("---", 1)
    except ValueError:
        raise ValueError(f"{path}: unclosed YAML frontmatter")
    values = parse_yaml_mapping("\n".join(lines[1:delimiter]), str(path))
    if not isinstance(values.get("name"), str) or not values["name"]:
        raise ValueError(f"{path}: frontmatter requires a non-empty name")
    if not isinstance(values.get("description"), str) or not values["description"].strip():
        raise ValueError(f"{path}: frontmatter requires a non-empty description")
    return values


def parse_execution(package_root: Path, repo_root: Path, required: bool) -> dict | None:
    path = package_root / "execution.json"
    if not path.is_file():
        if required:
            raise ValueError(f"missing execution.json: {package_root.name}")
        return None
    execution = _load_json(_contained_file(package_root, "execution.json"))
    if set(execution) - {"schema_version", "compatible_roles", "tools"}:
        raise ValueError(f"unknown execution.json fields: {package_root.name}")
    roles = execution.get("compatible_roles")
    if execution.get("schema_version") != 1 or not isinstance(roles, list):
        raise ValueError(f"malformed execution.json: {package_root.name}")
    if any(not isinstance(role, str) or role not in ROLES for role in roles) or len(roles) != len(set(roles)):
        raise ValueError(f"malformed compatible_roles: {package_root.name}")
    tools = execution.get("tools")
    if tools is not None:
        if not isinstance(tools, dict) or set(tools) - {"capabilities", "commands"}:
            raise ValueError(f"malformed execution tools: {package_root.name}")
        if any(not isinstance(values, list) or any(not isinstance(item, str) for item in values) for values in tools.values()):
            raise ValueError(f"malformed execution tool lists: {package_root.name}")
        for expression in tools.get("commands", []):
            parts = expression.rsplit(":", 1)
            if len(parts) != 2 or not parts[1] or len(parts[0].split()) != 2:
                raise ValueError(f"malformed command restriction: {package_root.name}")
            tool = parts[0].split()[1]
            resolved = (repo_root / tool).resolve()
            if not tool.startswith("tools/") or not resolved.is_relative_to((repo_root / "tools").resolve()) or not resolved.is_file():
                raise ValueError(f"command tool is missing or escaping: {tool}")
    normalized = {"schemaVersion": 1, "compatibleRoles": roles}
    if tools is not None:
        normalized["tools"] = tools
    return normalized


def validate_and_build(root: Path, public_export: bool = False) -> dict:
    root = root.resolve()
    workflows = root / "workflows"
    catalog = _load_catalog(workflows / "catalog.yaml")
    if catalog.get("schema") != CATALOG_SCHEMA:
        raise ValueError(f"catalog schema must be {CATALOG_SCHEMA}")
    if set(catalog) != {"schema", "library", "centralWorkflowNames", "navigation"}:
        raise ValueError("catalog has missing or unknown top-level fields")
    library = catalog["library"]
    if not isinstance(library, dict) or set(library) != {"source", "sourceRootId"}:
        raise ValueError("library must contain only source and sourceRootId")
    if library["source"] not in SOURCES or not isinstance(library["sourceRootId"], str) or not library["sourceRootId"]:
        raise ValueError("invalid library identity")
    central_names = catalog["centralWorkflowNames"]
    if not isinstance(central_names, list) or tuple(central_names) != CENTRAL:
        raise ValueError("centralWorkflowNames must equal the ordered central workflows")
    navigation = parse_navigation(catalog["navigation"])
    methods = _load_json(workflows / "legacy-methods.json")
    required_method_keys = {"schema", "convertedWorkflowAliases", "historicalOnly", "unknownLegacyBehavior"}
    if methods.get("schema") != LEGACY_SCHEMA or set(methods) != required_method_keys:
        raise ValueError("invalid legacy-method ledger")
    descriptors = []
    seen = set()
    package_dirs = [p for p in workflows.iterdir() if p.is_dir() and not p.name.startswith(".") and p.name != "chirality-change"]
    missing_entrypoints = [p.name for p in package_dirs if not (p / "WORKFLOW.md").is_file()]
    if missing_entrypoints:
        raise ValueError(f"workflow package directories missing WORKFLOW.md: {sorted(missing_entrypoints)}")
    folders = package_dirs
    for folder in sorted(folders):
        metadata = _frontmatter(folder / "WORKFLOW.md")
        execution = parse_execution(folder, root, required=False)
        resources = sorted(path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file())
        placement = navigation.get(folder.name)
        entry = {
            "kind": "workflow",
            "name": metadata["name"],
            "description": metadata["description"],
            "compatibility": "legacy" if placement is not None and placement["category"] == "superseded" else "canonical",
            "executionRoleIds": execution["compatibleRoles"] if execution is not None else list(ROLES),
            "resources": resources,
        }
        package_metadata = metadata.get("metadata")
        if package_metadata is not None:
            if not isinstance(package_metadata, dict):
                raise ValueError(f"frontmatter metadata must be a mapping: {folder.name}")
            entry["metadata"] = package_metadata
        if execution is not None:
            entry["execution"] = execution
        name = entry["name"]
        identity = (entry["kind"], name)
        if identity in seen:
            raise ValueError(f"duplicate package identity: {identity}")
        seen.add(identity)
        if entry["kind"] != "workflow" or not isinstance(name, str) or not NAME_RE.fullmatch(name):
            raise ValueError(f"invalid bundled workflow identity: {identity}")
        if name != folder.name:
            raise ValueError(f"package name must match folder: {name}")
        if not isinstance(entry["description"], str) or not entry["description"].strip():
            raise ValueError(f"empty description: {name}")
        if entry["compatibility"] not in ("canonical", "legacy"):
            raise ValueError(f"invalid compatibility: {name}")
        roles = entry["executionRoleIds"]
        resources = entry["resources"]
        if not isinstance(roles, list) or any(not isinstance(x, str) for x in roles) or len(roles) != len(set(roles)):
            raise ValueError(f"invalid executionRoleIds: {name}")
        if not isinstance(resources, list) or "WORKFLOW.md" not in resources or any(not isinstance(x, str) for x in resources) or len(resources) != len(set(resources)):
            raise ValueError(f"invalid resources: {name}")
        package_root = folder.resolve()
        if not package_root.is_relative_to(workflows.resolve()) or not package_root.is_dir():
            raise ValueError(f"missing or escaping workflow package: {name}")
        for resource in resources:
            _contained_file(package_root, resource)
        descriptors.append(_descriptor(entry, library, name in central_names, placement))
    folders = {p.name for p in workflows.iterdir() if p.is_dir() and (p / "WORKFLOW.md").is_file() and p.name != "chirality-change"}
    names = {item["name"] for item in descriptors}
    if names != folders:
        raise ValueError(f"catalog/folder disagreement: missing={sorted(folders-names)}, extra={sorted(names-folders)}")
    if set(navigation) != names:
        raise ValueError(
            "navigation/package disagreement: "
            f"missing={sorted(names - set(navigation))}, extra={sorted(set(navigation) - names)}"
        )
    actual_central = {item["name"] for item in descriptors if item["central"]}
    if actual_central != set(CENTRAL):
        raise ValueError("central workflow set must match the central workflows")
    actual_legacy = {item["name"] for item in descriptors if item["compatibility"] == "legacy"}
    if actual_legacy != {name for name, placement in navigation.items() if placement["category"] == "superseded"}:
        raise ValueError("legacy compatibility must be reserved for superseded workflows")

    skills_root = root / ".agents" / "skills"
    skill_names = set()
    if skills_root.is_dir():
        if not skills_root.resolve().is_relative_to(root):
            raise ValueError("skill collection escapes declared library root")
        skill_dirs = [p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith(".")]
        missing_skills = [p.name for p in skill_dirs if not (p / "SKILL.md").is_file()]
        if missing_skills:
            raise ValueError(f"skill package directories missing SKILL.md: {sorted(missing_skills)}")
        for folder in sorted(skill_dirs):
            package_root = folder.resolve()
            if not package_root.is_relative_to(skills_root.resolve()) or not package_root.is_dir():
                raise ValueError(f"missing or escaping skill package: {folder.name}")
            metadata = _frontmatter(folder / "SKILL.md")
            if metadata["name"] != folder.name or not NAME_RE.fullmatch(folder.name):
                raise ValueError(f"invalid bundled skill identity: {folder.name}")
            resources = sorted(path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file())
            for resource in resources:
                _contained_file(package_root, resource)
            execution = parse_execution(package_root, root, required=False)
            skill_names.add(folder.name)
            method_source = "project" if folder.name == "chirality-change" else library["source"]
            method_root = "chirality-root-project" if folder.name == "chirality-change" else library["sourceRootId"]
            descriptor = {
                "kind": "skill", "name": folder.name,
                "source": method_source, "sourceRootId": method_root,
                "description": metadata["description"], "central": False,
                "compatibility": "canonical",
                "executionRoleIds": execution["compatibleRoles"] if execution is not None else list(ROLES),
                "resources": resources,
            }
            if execution is not None:
                descriptor["execution"] = execution
            descriptors.append(descriptor)

    retired = _load_json(workflows / "legacy-agents.json")
    if retired.get("schema_version") != 1 or not isinstance(retired.get("aliases"), dict):
        raise ValueError("invalid retired-role ledger")
    for alias, mapping in retired["aliases"].items():
        if not isinstance(mapping, dict) or not isinstance(mapping.get("role"), str):
            raise ValueError(f"malformed retired-role mapping: {alias}")
        successor = mapping.get("canonical_successor")
        if successor is not None:
            if not isinstance(successor, dict) or successor.get("kind") not in ("workflow", "skill") or not isinstance(successor.get("name"), str):
                raise ValueError(f"malformed canonical successor: {alias}")
            if successor["kind"] == "workflow" and successor["name"] not in names:
                raise ValueError(f"unknown workflow successor: {alias}")
            if successor["kind"] == "skill" and successor["name"] not in skill_names:
                raise ValueError(f"unknown skill successor: {alias}")
    if methods["unknownLegacyBehavior"] != "error" or not isinstance(methods["historicalOnly"], list):
        raise ValueError("unconverted legacy methods must remain historical and unknown selection must error")
    converted = methods["convertedWorkflowAliases"]
    if not isinstance(converted, dict) or any(
        not isinstance(k, str) or not isinstance(v, dict)
        or set(v) != {"kind", "name"} or v["kind"] not in ("workflow", "skill")
        or (v["kind"] == "workflow" and v["name"] not in names)
        or (v["kind"] == "skill" and v["name"] not in skill_names)
        for k, v in converted.items()
    ):
        raise ValueError("converted TaskSkill mapping targets unknown workflows")
    if set(converted) & set(methods["historicalOnly"]):
        raise ValueError("legacy methods cannot be both converted and historical-only")
    converted_refs = dict(sorted(converted.items()))
    if public_export:
        descriptors = [item for item in descriptors if not (item["kind"] == "skill" and item["name"] == "chirality-change")]
    return {
        "schema": INDEX_SCHEMA,
        "library": library,
        "precedence": list(SOURCES),
        "centralWorkflowNames": list(CENTRAL),
        "methods": sorted(descriptors, key=lambda item: (item["kind"], item["name"])),
        "legacy": {
            "retiredRoles": retired["aliases"],
            "convertedWorkflowAliases": converted_refs,
            "historicalOnly": methods["historicalOnly"],
            "unknownLegacyBehavior": "error",
        },
        "discoveryContract": {
            "packageMetadata": "<package>/WORKFLOW.md#yaml-frontmatter",
            "executionCompanion": "execution.json",
            "flatProjectMarkdown": "document-only",
            "malformedHigherPrecedence": "block-identity",
            "collisionHandling": "expose-all-qualified-candidates",
            "resourceContainment": "realpath-within-package-root",
            "publicExportExclusions": [{"kind": "skill", "name": "chirality-change"}],
        },
    }


def bootstrap(root: Path) -> None:
    workflows = root.resolve() / "workflows"
    existing = workflows / "catalog.yaml"
    navigation = None
    if existing.is_file():
        try:
            navigation = _load_catalog(existing).get("navigation")
        except (OSError, ValueError, json.JSONDecodeError):
            navigation = None
    value = {
        "schema": CATALOG_SCHEMA,
        "library": {"source": "bundled", "sourceRootId": "chirality-root"},
        "centralWorkflowNames": list(CENTRAL),
        "navigation": navigation if isinstance(navigation, dict) else {
            "core": [
                {"name": name, **({"displayName": CORE_DISPLAY_NAMES[name]} if name in CORE_DISPLAY_NAMES else {})}
                for name in CORE
            ],
            "specialist": [],
            "superseded": [],
        },
    }
    (workflows / "catalog.yaml").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--bootstrap", action="store_true", help="one-time migration from legacy WORKFLOW.md frontmatter")
    parser.add_argument("--check", action="store_true", help="fail if generated index is stale")
    parser.add_argument("--public-export", action="store_true", help="omit project-only methods from public bundle output")
    args = parser.parse_args()
    try:
        if args.bootstrap:
            bootstrap(args.root)
        index = validate_and_build(args.root, public_export=args.public_export)
        destination = args.root.resolve() / "workflows" / "index.json"
        rendered = json.dumps(index, indent=2, sort_keys=False) + "\n"
        if args.check:
            if not destination.is_file() or destination.read_text(encoding="utf-8") != rendered:
                raise ValueError("workflows/index.json is stale; regenerate with build_workflow_index.py")
        else:
            destination.write_text(rendered, encoding="utf-8")
        print(json.dumps({"status": "PASS", "methods": len(index["methods"]), "index": str(destination)}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, yaml.YAMLError) as error:
        parser.exit(1, f"workflow catalog error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
