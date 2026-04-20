#!/usr/bin/env python3
"""
validate_source_supersession.py — Deterministic source-fidelity validator for DBM publication.

Compares source-fidelity-critical assertion values from published sections
against the admitted source authority package.  Divergence is allowed only
when matched by the active Supersession_Map.csv.

Consumes:
  --assertions-root       Path to sections/ directory containing SEC-##_ASSERTIONS.csv
  --source-authority      Path to the cleaned source authority package root
  --supersession-map      Path to the frozen cumulative Supersession_Map.csv
  --concordance-register  Path to the frozen concordance register (source-fidelity keys)
  --output-report         Path to write Source_Supersession_Report.md
  --output-findings       Path to write Source_Supersession_Findings.csv

Determinism:
  Same inputs -> byte-identical outputs.  No probabilistic or model-based
  logic.  String comparison only.

Scope boundary:
  Reads only the admitted inputs.  Writes only to --output-report and
  --output-findings.  Does not modify assertions, source, or supersession map.

Exit codes:
  0 = success, no blocking findings
  1 = fatal input / parsing error
  2 = success with blocking findings requiring human review

Example:
  python3 tools/publication/validate_source_supersession.py \\
    --assertions-root /repo/.../_Publication/DBM/sections/ \\
    --source-authority /repo/.../west_doe_process_design_basis_clean/ \\
    --supersession-map /repo/.../_ScopeChange/SCA-004_.../Supersession_Map.csv \\
    --concordance-register /repo/.../_Planning/Publication_Concordance_Register.csv \\
    --output-report /repo/.../package/Source_Supersession_Report.md \\
    --output-findings /repo/.../package/Source_Supersession_Findings.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fatal(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of row dicts."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def normalize_value(raw: str) -> str:
    """Normalize a value for comparison: strip, lowercase, collapse whitespace."""
    return " ".join(raw.strip().lower().split())


# ---------------------------------------------------------------------------
# Source-fidelity key identification
# ---------------------------------------------------------------------------

SOURCE_FIDELITY_FLAG = "SourceFidelityCritical"


def extract_source_fidelity_keys(register_rows: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """Return register rows flagged as source-fidelity-critical, keyed by AssertionKey."""
    result: Dict[str, Dict[str, str]] = {}
    for row in register_rows:
        flag = row.get(SOURCE_FIDELITY_FLAG, "").strip().upper()
        if flag in ("YES", "TRUE", "1"):
            key = row.get("AssertionKey", "").strip()
            if key:
                result[key] = row
    return result


# ---------------------------------------------------------------------------
# Supersession map loading
# ---------------------------------------------------------------------------


def load_supersession_map(path: Path) -> Dict[str, List[Dict[str, str]]]:
    """Load the supersession map, keyed by SupersededFactKey.

    Multiple rows may share the same fact key (different applicability scopes
    or successive amendments).  Returns all rows per key so the validator can
    filter by applicability before selecting the active binding.
    """
    rows = read_csv_rows(path)
    result: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        key = row.get("SupersededFactKey", "").strip()
        if key:
            result.setdefault(key, []).append(row)
    return result


def _parse_semicolon_list(raw: str) -> List[str]:
    """Split a semicolon-separated field into stripped, non-empty tokens."""
    return [t.strip() for t in raw.split(";") if t.strip()]


def find_applicable_supersession(
    rows: List[Dict[str, str]],
    root_name: str,
    facility_id: str,
    section_id: str,
) -> Optional[Dict[str, str]]:
    """Find the most recent applicable supersession binding for a fact key.

    Filters by AppliesToRoots, AppliesToFacilities, and AppliesToSections when
    those fields are non-empty.  Returns the last matching row (latest
    amendment wins) or None if no row is applicable.
    """
    candidates: List[Dict[str, str]] = []
    for row in rows:
        roots = _parse_semicolon_list(row.get("AppliesToRoots", ""))
        facilities = _parse_semicolon_list(row.get("AppliesToFacilities", ""))
        sections = _parse_semicolon_list(row.get("AppliesToSections", ""))
        if roots and root_name not in roots:
            continue
        if facilities and facility_id not in facilities:
            continue
        if sections and section_id not in sections:
            continue
        candidates.append(row)
    # Latest amendment wins (last in the list, since cumulative map is ordered)
    return candidates[-1] if candidates else None


# ---------------------------------------------------------------------------
# Section assertion loading
# ---------------------------------------------------------------------------


def load_section_assertions(assertions_root: Path) -> Dict[str, List[Dict[str, str]]]:
    """Load all SEC-##_ASSERTIONS.csv files, keyed by SectionID."""
    result: Dict[str, List[Dict[str, str]]] = {}
    if not assertions_root.exists():
        return result
    for section_dir in sorted(assertions_root.iterdir()):
        if not section_dir.is_dir():
            continue
        section_id = section_dir.name
        assertions_file = section_dir / f"{section_id}_ASSERTIONS.csv"
        if assertions_file.exists():
            result[section_id] = read_csv_rows(assertions_file)
    return result


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

FINDING_TYPES = {
    "PASS": "Assertion matches source authority",
    "PASS_OVERRIDDEN": "Assertion diverges from source but is covered by a supersession binding",
    "UNMATCHED_SOURCE_DIVERGENCE": "Assertion contradicts source authority with no supersession binding (BLOCKING)",
    "SUPERSESSION_VALUE_MISMATCH": "Supersession binding exists but assertion matches neither source nor replacement (BLOCKING)",
    "SOURCE_VALUE_NOT_AVAILABLE": "Source-fidelity key has no extractable source value for comparison (non-blocking)",
    "ASSERTION_NOT_FOUND": "Source-fidelity key has no authority assertion row in any section (BLOCKING)",
}

BLOCKING_TYPES = {"UNMATCHED_SOURCE_DIVERGENCE", "SUPERSESSION_VALUE_MISMATCH", "ASSERTION_NOT_FOUND"}


def make_finding(
    assertion_key: str,
    section_id: str,
    finding_type: str,
    source_value: str,
    assertion_value: str,
    supersession_key: str,
    replacement_value: str,
    notes: str,
) -> Dict[str, str]:
    return {
        "AssertionKey": assertion_key,
        "SectionID": section_id,
        "FindingType": finding_type,
        "Blocking": "TRUE" if finding_type in BLOCKING_TYPES else "FALSE",
        "SourceValue": source_value,
        "AssertionValue": assertion_value,
        "SupersessionKey": supersession_key,
        "ReplacementValue": replacement_value,
        "Notes": notes,
    }


def validate(
    source_fidelity_keys: Dict[str, Dict[str, str]],
    section_assertions: Dict[str, List[Dict[str, str]]],
    supersession_map: Dict[str, List[Dict[str, str]]],
    root_name: str,
    facility_id: str,
) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    """Run the validation and return (findings, metrics)."""
    findings: List[Dict[str, str]] = []
    metrics = {
        "total_checked": 0,
        "pass": 0,
        "pass_overridden": 0,
        "unmatched_divergence": 0,
        "supersession_mismatch": 0,
        "source_not_available": 0,
        "assertion_not_found": 0,
    }

    # Build a lookup: assertion_key -> list of (section_id, row)
    assertion_index: Dict[str, List[Tuple[str, Dict[str, str]]]] = {}
    for section_id, rows in section_assertions.items():
        for row in rows:
            key = row.get("AssertionKey", "").strip()
            status = row.get("AssertionStatus", "").strip()
            if key and status == "ASSERTED":
                assertion_index.setdefault(key, []).append((section_id, row))

    for fidelity_key, register_row in sorted(source_fidelity_keys.items()):
        metrics["total_checked"] += 1
        source_value = normalize_value(register_row.get("SourceExpectedValue", ""))
        authority_section = register_row.get("AuthoritySectionID", "").strip()

        # Find the authority assertion
        authority_assertions = assertion_index.get(fidelity_key, [])
        if not authority_assertions:
            metrics["assertion_not_found"] += 1
            findings.append(make_finding(
                fidelity_key, authority_section, "ASSERTION_NOT_FOUND",
                source_value, "", "", "",
                "No ASSERTED row found for this source-fidelity key in any section.",
            ))
            continue

        # Use the first authority assertion (should be unique per key)
        section_id, assertion_row = authority_assertions[0]
        assertion_value = normalize_value(assertion_row.get("NormalizedValue", ""))

        if not source_value:
            metrics["source_not_available"] += 1
            findings.append(make_finding(
                fidelity_key, section_id, "SOURCE_VALUE_NOT_AVAILABLE",
                "", assertion_value, "", "",
                "Source-fidelity key has no SourceExpectedValue in the register for comparison.",
            ))
            continue

        # Compare assertion against source
        if assertion_value == source_value:
            metrics["pass"] += 1
            findings.append(make_finding(
                fidelity_key, section_id, "PASS",
                source_value, assertion_value, "", "",
                "Assertion matches source authority.",
            ))
            continue

        # Divergence detected — check supersession map with applicability filtering
        supersession_rows = supersession_map.get(fidelity_key, [])
        supersession_row = find_applicable_supersession(
            supersession_rows, root_name, facility_id, section_id,
        )
        if supersession_row and supersession_row.get("OverrideType", "").strip().upper() == "SUPERSESSION":
            replacement = normalize_value(supersession_row.get("ReplacementFactTextOrValue", ""))
            supersession_key = supersession_row.get("SupersededFactKey", "")
            if assertion_value == replacement:
                metrics["pass_overridden"] += 1
                findings.append(make_finding(
                    fidelity_key, section_id, "PASS_OVERRIDDEN",
                    source_value, assertion_value, supersession_key, replacement,
                    f"Covered by {supersession_row.get('AmendmentID', '')} {supersession_row.get('DecisionID', '')}.",
                ))
            else:
                metrics["supersession_mismatch"] += 1
                findings.append(make_finding(
                    fidelity_key, section_id, "SUPERSESSION_VALUE_MISMATCH",
                    source_value, assertion_value, supersession_key, replacement,
                    f"Binding exists ({supersession_row.get('AmendmentID', '')}) but assertion matches neither source nor replacement.",
                ))
        else:
            metrics["unmatched_divergence"] += 1
            findings.append(make_finding(
                fidelity_key, section_id, "UNMATCHED_SOURCE_DIVERGENCE",
                source_value, assertion_value, "", "",
                "Assertion contradicts source authority with no supersession binding.",
            ))

    return findings, metrics


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def write_findings_csv(findings: List[Dict[str, str]], path: Path) -> None:
    columns = [
        "AssertionKey", "SectionID", "FindingType", "Blocking",
        "SourceValue", "AssertionValue", "SupersessionKey", "ReplacementValue", "Notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(findings)


def write_report(findings: List[Dict[str, str]], metrics: Dict[str, int], path: Path) -> None:
    blocking_count = sum(1 for f in findings if f.get("Blocking") == "TRUE")
    lines = [
        "# Source Supersession Validation Report",
        "",
        f"**Total source-fidelity keys checked:** {metrics['total_checked']}",
        f"**PASS (matches source):** {metrics['pass']}",
        f"**PASS_OVERRIDDEN (covered by supersession):** {metrics['pass_overridden']}",
        f"**UNMATCHED_SOURCE_DIVERGENCE (blocking):** {metrics['unmatched_divergence']}",
        f"**SUPERSESSION_VALUE_MISMATCH (blocking):** {metrics['supersession_mismatch']}",
        f"**ASSERTION_NOT_FOUND (blocking):** {metrics['assertion_not_found']}",
        f"**SOURCE_VALUE_NOT_AVAILABLE (non-blocking):** {metrics['source_not_available']}",
        "",
        f"**Total blocking findings:** {blocking_count}",
        f"**Verdict:** {'BLOCKED' if blocking_count > 0 else 'PASS'}",
        "",
    ]

    if blocking_count > 0:
        lines.append("## Blocking Findings")
        lines.append("")
        lines.append("| Key | Section | Type | Source | Assertion | Notes |")
        lines.append("|---|---|---|---|---|---|")
        for f in findings:
            if f.get("Blocking") == "TRUE":
                lines.append(
                    f"| {f['AssertionKey']} | {f['SectionID']} | {f['FindingType']} "
                    f"| {f['SourceValue']} | {f['AssertionValue']} | {f['Notes']} |"
                )
        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate source fidelity with supersession-map allowance.")
    parser.add_argument("--assertions-root", required=True, help="Path to sections/ directory")
    parser.add_argument("--source-authority", default="", help="Path to cleaned source authority package root (informational — source values come from the register's SourceExpectedValue column)")
    parser.add_argument("--supersession-map", required=True, help="Path to Supersession_Map.csv")
    parser.add_argument("--concordance-register", required=True, help="Path to concordance register CSV")
    parser.add_argument("--root-name", default="", help="Root name for applicability filtering (e.g., West_Doe_Deepcut_DBM)")
    parser.add_argument("--facility-id", default="", help="Facility ID for applicability filtering (e.g., 04-25)")
    parser.add_argument("--output-report", required=True, help="Path to write report markdown")
    parser.add_argument("--output-findings", required=True, help="Path to write findings CSV")
    args = parser.parse_args()

    assertions_root = Path(args.assertions_root).resolve()
    supersession_map_path = Path(args.supersession_map).resolve()
    register_path = Path(args.concordance_register).resolve()
    report_path = Path(args.output_report).resolve()
    findings_path = Path(args.output_findings).resolve()

    if not assertions_root.exists():
        fatal(f"Assertions root does not exist: {assertions_root}")
    if not register_path.exists():
        fatal(f"Concordance register does not exist: {register_path}")

    # Load inputs
    register_rows = read_csv_rows(register_path)
    source_fidelity_keys = extract_source_fidelity_keys(register_rows)

    if not source_fidelity_keys:
        print("No source-fidelity-critical keys found in the concordance register. Nothing to validate.")
        write_report([], {"total_checked": 0, "pass": 0, "pass_overridden": 0,
                          "unmatched_divergence": 0, "supersession_mismatch": 0,
                          "source_not_available": 0, "assertion_not_found": 0}, report_path)
        write_findings_csv([], findings_path)
        return 0

    supersession_map = load_supersession_map(supersession_map_path) if supersession_map_path.exists() else {}
    section_assertions = load_section_assertions(assertions_root)

    # Run validation
    findings, metrics = validate(
        source_fidelity_keys, section_assertions, supersession_map,
        root_name=args.root_name, facility_id=args.facility_id,
    )

    # Write outputs
    write_findings_csv(findings, findings_path)
    write_report(findings, metrics, report_path)

    blocking_count = sum(1 for f in findings if f.get("Blocking") == "TRUE")
    total = metrics["total_checked"]
    passed = metrics["pass"] + metrics["pass_overridden"]

    print(f"Source-supersession validation: {total} checked, {passed} passed, {blocking_count} blocking.")

    if blocking_count > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
