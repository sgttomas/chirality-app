"""Shared inventory, report and dependency parsing for deterministic audits."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


schema = load_module("evaluation_dependency_schema", TOOLS / "validation/validate_dependencies_schema.py")
sow = load_module("evaluation_sow_contract", TOOLS / "scope_of_work/common.py")


def inventory(root, variant=None):
    """Live immediate production units; never recurse into archived copies."""
    prefixes = (("CAT-", "KTY-"),) if variant == "DOMAIN" else (("PKG-", "DEL-"),)
    if variant is None:
        prefixes = (("PKG-", "DEL-"), ("CAT-", "KTY-"))
    return sorted(path for partition, unit in prefixes for path in root.glob(f"{partition}*/1_Working/{unit}*") if path.is_dir())


def require_root(root):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"execution root is not a directory: {root}")
    return root


def report_base(root):
    return {"schema_version": 1, "root": str(root), "run_status": "COMPLETE", "subject_status": "NOT_ASSESSED", "issues": []}


def write_report(report, output):
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if str(output) == "-":
        print(text, end="")
    else:
        target = Path(output).resolve()
        if target.exists() and not target.is_file():
            raise ValueError(f"report output is not a regular file: {target}")
        # Reports cannot replace inspected workspace content.
        if "1_Working" in target.parts or target.name in {"Dependencies.csv", "_STATUS.md"}:
            raise ValueError("report output must be outside production-unit source paths")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def parse_register(path):
    """Strict CSV shape + canonical row semantics; logical records preserve multiline cells.

    Return a report and shape-readable rows. Invalid rows carry their errors;
    graph consumers must exclude them. A parse error retains preceding records
    and marks the denominator incomplete.
    """
    result = {"path": str(path), "rows": 0, "readable_rows": 0, "malformed_rows": 0,
              "denominator_complete": True, "columns": [], "extensions": [],
              "issues": [], "row_findings": [], "schema_valid": False,
              "enum_validation": {field: {"valid": 0, "invalid": 0} for field in schema.CANONICAL_ENUMS},
              "implements_node_rows": 0, "anchor_rows": 0, "execution_rows": 0,
              "evidence_populated": 0, "evidence_coverage_percent": None}
    rows = []
    try:
        raw = path.read_bytes()
        result["sha256"] = hashlib.sha256(raw).hexdigest()
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, None)
            if not header:
                result["issues"].append("empty file or missing header")
                return result, rows
            header = [name.strip() for name in header]
            result["columns"] = header
            missing = sorted(set(schema.REQUIRED_COLUMNS) - set(header))
            duplicates = sorted({name for name in header if header.count(name) > 1})
            result["extensions"] = [name for name in header if name not in schema.REQUIRED_COLUMNS]
            if missing:
                result["issues"].append("missing columns: " + ", ".join(missing))
            if duplicates or "" in header:
                result["issues"].append("duplicate or empty column names: " + ", ".join(duplicates))
            header_valid = not missing and not duplicates and "" not in header
            for number, values in enumerate(reader, 1):
                result["rows"] += 1
                if len(values) != len(header):
                    result["malformed_rows"] += 1
                    result["row_findings"].append({"record": number, "end_line": reader.line_num,
                        "issues": [f"field count: expected {len(header)}, found {len(values)}"]})
                    continue
                if not header_valid:
                    continue
                row = dict(zip(header, values))
                result["readable_rows"] += 1
                for field, allowed in schema.CANONICAL_ENUMS.items():
                    result["enum_validation"][field]["valid" if row[field].strip() in allowed else "invalid"] += 1
                errors = schema.validate_row_semantics([row])
                # Canonical helper labels its single input as Row 2; report the
                # actual logical record and physical end line outside that text.
                errors = [message.removeprefix("Row 2 ") for message in errors]
                if row["RegisterSchemaVersion"].strip() != "v3.1":
                    errors.append("RegisterSchemaVersion must equal v3.1")
                if not row["DependencyID"].strip():
                    errors.append("DependencyID is empty")
                if errors:
                    result["row_findings"].append({"record": number, "end_line": reader.line_num, "issues": errors})
                row.update(_record=number, _end_line=reader.line_num, _issues=errors, _source_file=str(path))
                rows.append(row)
                anchor = row["DependencyClass"].strip() == "ANCHOR"
                result["anchor_rows"] += int(anchor)
                result["execution_rows"] += int(row["DependencyClass"].strip() == "EXECUTION")
                result["implements_node_rows"] += int(anchor and row["AnchorType"].strip() == "IMPLEMENTS_NODE")
                result["evidence_populated"] += int(bool(row["EvidenceFile"].strip()))
    except (OSError, UnicodeError, csv.Error) as exc:
        result["issues"].append(f"unreadable register: {exc}")
        result["denominator_complete"] = False
    result["schema_valid"] = not result["issues"] and not result["row_findings"]
    if result["rows"] and result["denominator_complete"]:
        result["evidence_coverage_percent"] = round(100 * result["evidence_populated"] / result["rows"], 4)
    return result, rows
