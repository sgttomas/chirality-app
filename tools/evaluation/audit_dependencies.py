#!/usr/bin/env python3
"""Exhaustive dependency-register audit. Successful observation exits 0, even for FAIL subjects."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from audit_common import inventory, parse_register, report_base, require_root, write_report


def audit(root):
    root = require_root(root)
    result = report_base(root)
    units = inventory(root)
    files = []
    for unit in units:
        path = unit / "Dependencies.csv"
        if path.is_file():
            info, _ = parse_register(path)
            info["production_unit"] = unit.name.split("_")[0]
            files.append(info)
        else:
            result["issues"].append(f"missing register: {path}")
    # Registers of nonstandard production units remain in the CSV census.
    known = {item["path"] for item in files}
    for path in sorted(root.rglob("Dependencies.csv")):
        relative = path.relative_to(root)
        if "1_Working" in relative.parts and "_Archive" not in relative.parts and str(path) not in known:
            info, _ = parse_register(path)
            files.append(info)
    files.sort(key=lambda info: info["path"])
    result["files"] = files
    total = sum(info["rows"] for info in files)
    populated = sum(info["evidence_populated"] for info in files)
    complete = all(info["denominator_complete"] for info in files)
    result["summary"] = {"production_units": len(units), "files": len(files), "rows": total,
        "schema_valid_files": sum(info["schema_valid"] for info in files),
        "malformed_rows": sum(info["malformed_rows"] for info in files),
        "readable_rows": sum(info["readable_rows"] for info in files),
        "files_with_implements_node": sum(info["implements_node_rows"] > 0 for info in files),
        "evidence_populated": populated, "evidence_denominator": total,
        "denominator_complete": complete,
        "evidence_coverage_percent": round(100 * populated / total, 4) if total and complete else None}
    for info in files:
        if not info["implements_node_rows"]:
            info["issues"].append("no ANCHOR row with AnchorType=IMPLEMENTS_NODE")
        if info["evidence_populated"] != info["rows"]:
            info["issues"].append("EvidenceFile is absent or unassessable for one or more records")
    failures = result["issues"] or any(info["issues"] or info["row_findings"] for info in files)
    result["subject_status"] = "FAIL" if failures else "PASS" if files else "NOT_ASSESSED"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, help="JSON report path, or - for stdout")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root)
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
