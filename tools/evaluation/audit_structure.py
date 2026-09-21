#!/usr/bin/env python3
"""Audit an explicit workspace variant and live or supplied production-unit inventory."""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from audit_common import inventory, report_base, require_root, sow, write_report

MUST_FILES = ("_STATUS.md", "_CONTEXT.md", "_DEPENDENCIES.md", "_REFERENCES.md")
OPTIONAL_FILES = ("Dependencies.csv", "_MEMORY.md", "_SEMANTIC.md", "_SEMANTIC_LENSING.md")
LIFECYCLE = {"OPEN", "INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING", "ISSUED", "RETIRED"}
CONTRACT = {"version": "structure-audit/v1", "basis": "docs/SPEC.md sections 1-2; production format via tools/scope_of_work/common.py",
    "tool_roots": ["_Aggregation", "_Coordination", "_Decomposition", "_Estimates", "_Reconciliation", "_Sources"],
    "partition_directories": ["0_References", "1_Working", "2_Checking", "3_Issued"]}


def current_state(path):
    if not path.is_file():
        return None, "missing _STATUS.md"
    text = path.read_text(encoding="utf-8")
    # Read explicit fields, never state words in history or commentary.
    matches = []
    for line in text.splitlines():
        clean = line.strip().replace("**", "").replace("`", "")
        match = re.fullmatch(r"(?:-\s*)?Current State\s*:\s*(.*?)\s*", clean, re.I)
        table = re.fullmatch(r"\|\s*Current State\s*\|\s*([^|]*)\|", clean, re.I)
        if match or table:
            matches.append((match or table).group(1).strip())
    if not matches:
        # Historical explicit State fields remain a supported input format.
        for line in text.splitlines():
            clean = line.strip().replace("**", "").replace("`", "")
            match = re.fullmatch(r"(?:-\s*)?(?:Lifecycle\s+)?State\s*:\s*(.*?)\s*", clean, re.I)
            if match:
                matches.append(match.group(1).strip())
    if len(matches) != 1:
        return None, f"expected one current-state field, found {len(matches)}"
    state = matches[0]
    return state, None if state in LIFECYCLE else f"invalid current lifecycle state: {state!r}"


def selected_units(root, variant, inventory_path):
    if not inventory_path:
        return [(path, []) for path in inventory(root, variant)]
    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("units"), list):
        raise ValueError("inventory must be {schema_version: 1, units: [{path: relative-path, required_files: [...]}]}")
    selected = []
    for entry in data["units"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("each inventory unit requires a string path")
        path = (root / entry["path"]).resolve()
        if not path.is_relative_to(root) or path == root:
            raise ValueError(f"inventory path must be contained within root: {entry['path']}")
        required = entry.get("required_files", [])
        if not isinstance(required, list) or any(not isinstance(name, str) or Path(name).is_absolute() or ".." in Path(name).parts for name in required):
            raise ValueError("required_files must contain relative paths within the unit")
        selected.append((path, required))
    if len({path for path, _ in selected}) != len(selected):
        raise ValueError("inventory contains duplicate unit paths")
    return sorted(selected)


def audit(root, variant, inventory_path=None, isolated_migration=False, migration_authority=""):
    root = require_root(root)
    result = report_base(root)
    result.update(variant=variant, contract=CONTRACT, inventory_source=str(inventory_path) if inventory_path else "live variant discovery")
    selection = selected_units(root, variant, inventory_path)
    units = []
    for path, additional in selection:
        issues = []
        if not path.is_dir():
            issues.append("declared production-unit directory is missing")
        files = {name: (path / name).is_file() for name in (*MUST_FILES, *OPTIONAL_FILES, *sow.LEGACY_FILES, "ScopeOfWork.md", *additional)}
        issues.extend(f"missing required file: {name}" for name in (*MUST_FILES, *additional) if not files[name])
        state, state_issue = current_state(path / "_STATUS.md")
        if state_issue:
            issues.append(state_issue)
        if variant in {"PROJECT", "SOFTWARE"}:
            format_result = sow.resolve_production_format(path, isolated_migration=isolated_migration, migration_authority=migration_authority)
            format_info = {"state": format_result.state, "valid": format_result.valid,
                "accepted_baseline": format_result.state in sow.ACCEPTED_FORMATS and format_result.valid,
                "issues": list(format_result.issues)}
            has_production = format_result.has_scope_of_work or bool(format_result.legacy_files)
            if state in LIFECYCLE - {"OPEN", "RETIRED"} or has_production:
                issues.extend(format_result.issues)
            # RETIRED units remain in the census but do not require active production content.
        else:
            format_info = {"state": "NOT_APPLICABLE", "valid": None, "accepted_baseline": None,
                "issues": [], "reason": "SOW transition applies to PROJECT/SOFTWARE; DOMAIN content comes from inventory required_files"}
        units.append({"path": str(path), "id": path.name.split("_")[0], "current_state": state,
            "files": files, "production_format": format_info, "issues": issues, "subject_status": "FAIL" if issues else "PASS"})
    prefixes = "CAT-*" if variant == "DOMAIN" else "PKG-*"
    partitions = sorted(path for path in root.glob(prefixes) if path.is_dir())
    result["partitions"] = [{"path": str(path), "missing_directories": [name for name in CONTRACT["partition_directories"] if not (path / name).is_dir()]} for path in partitions]
    result["tool_roots"] = {name: (root / name).is_dir() for name in CONTRACT["tool_roots"]}
    result["units"] = units
    result["summary"] = {"units": len(units), "pass": sum(unit["subject_status"] == "PASS" for unit in units),
        "fail": sum(unit["subject_status"] == "FAIL" for unit in units), "partitions": len(partitions),
        "lifecycle_states": dict(sorted(Counter(unit["current_state"] or "UNKNOWN" for unit in units).items())),
        "production_formats": dict(sorted(Counter(unit["production_format"]["state"] for unit in units).items()))}
    if any(item["missing_directories"] for item in result["partitions"]):
        result["issues"].append("partition directory contract is incomplete")
    if not all(result["tool_roots"].values()):
        result["issues"].append("required tool roots are missing")
    result["subject_status"] = "FAIL" if result["issues"] or result["summary"]["fail"] else "PASS" if units else "NOT_ASSESSED"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True)
    parser.add_argument("--variant", required=True, choices=["PROJECT", "SOFTWARE", "DOMAIN"])
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root, args.variant, args.inventory, args.isolated_migration, args.migration_authority)
    except (OSError, ValueError) as exc:
        report = report_base(args.root)
        report.update(run_status="FAILED_INPUTS", issues=[str(exc)])
    try:
        write_report(report, args.output)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0 if report["run_status"] == "COMPLETE" else 2


if __name__ == "__main__":
    sys.exit(main())
