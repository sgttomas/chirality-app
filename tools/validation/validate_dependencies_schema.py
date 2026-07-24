#!/usr/bin/env python3
"""Validate a dependency CSV file against the canonical v3.1 contract."""

import argparse
import csv
import sys

REQUIRED_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement",
    "EvidenceFile", "SourceRef", "EvidenceQuote", "Explicitness",
    "RequiredMaturity", "ProposedMaturity", "SatisfactionStatus", "Confidence",
    "Origin", "FirstSeen", "LastSeen", "Status", "Notes"
]

KNOWN_EXTENSIONS = ["EstimateImpactClass", "ConsumerHint"]

CANONICAL_ENUMS = {
    "DependencyClass": {"ANCHOR", "EXECUTION"},
    "AnchorType": {"IMPLEMENTS_NODE", "TRACES_TO_REQUIREMENT", "NOT_APPLICABLE"},
    "Direction": {"UPSTREAM", "DOWNSTREAM"},
    "DependencyType": {"PREREQUISITE", "INTERFACE", "HANDOVER", "CONSTRAINT", "ENABLES", "OTHER"},
    "TargetType": {"DELIVERABLE", "PACKAGE", "WBS_NODE", "REQUIREMENT", "DOCUMENT", "EQUIPMENT", "EXTERNAL", "UNKNOWN"},
    "Explicitness": {"EXPLICIT", "IMPLICIT"},
    "SatisfactionStatus": {"TBD", "PENDING", "IN_PROGRESS", "SATISFIED", "WAIVED", "NOT_APPLICABLE"},
    "Confidence": {"HIGH", "MEDIUM", "LOW"},
    "Origin": {"DECLARED", "EXTRACTED"},
    "Status": {"ACTIVE", "RETIRED"},
}


def dependency_id(row: dict[str, str], fallback: str = "<missing>") -> str:
    return row.get("DependencyID", "").strip() or fallback


def validate_row_semantics(rows: list[dict[str, str]]) -> list[str]:
    findings: list[str] = []
    for line_number, row in enumerate(rows, start=2):
        dep_id = dependency_id(row)

        for field, allowed in CANONICAL_ENUMS.items():
            value = row.get(field, "").strip()
            if value not in allowed:
                findings.append(
                    f"Row {line_number} invalid {field}: {value!r} "
                    f"(DependencyID={dep_id}; allowed={', '.join(sorted(allowed))})"
                )

        dependency_class = row.get("DependencyClass", "").strip()
        anchor_type = row.get("AnchorType", "").strip()
        dependency_type = row.get("DependencyType", "").strip()
        target_type = row.get("TargetType", "").strip()
        target_deliverable_id = row.get("TargetDeliverableID", "").strip()

        if dependency_class == "ANCHOR":
            if dependency_type != "OTHER":
                findings.append(
                    f"Row {line_number} ANCHOR row must use DependencyType=OTHER "
                    f"(DependencyID={dep_id}; found {dependency_type!r})"
                )
            if anchor_type == "NOT_APPLICABLE":
                findings.append(
                    f"Row {line_number} ANCHOR row must not use AnchorType=NOT_APPLICABLE "
                    f"(DependencyID={dep_id})"
                )

        if dependency_class == "EXECUTION" and anchor_type != "NOT_APPLICABLE":
            findings.append(
                f"Row {line_number} EXECUTION row must use AnchorType=NOT_APPLICABLE "
                f"(DependencyID={dep_id}; found {anchor_type!r})"
            )

        if target_type == "DELIVERABLE" and not target_deliverable_id:
            findings.append(
                f"Row {line_number} TargetType=DELIVERABLE requires TargetDeliverableID "
                f"(DependencyID={dep_id})"
            )
        if target_type and target_type != "DELIVERABLE" and target_deliverable_id:
            findings.append(
                f"Row {line_number} non-deliverable TargetType must leave TargetDeliverableID blank "
                f"(DependencyID={dep_id}; TargetType={target_type!r}; "
                f"TargetDeliverableID={target_deliverable_id!r})"
            )

    return findings


def validate(csv_path, schema_only=False):
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)
            raw_rows = list(reader)
    except FileNotFoundError:
        return False, [f"ERROR: File not found: {csv_path}"], [], 0, []
    except StopIteration:
        return False, [f"ERROR: Empty file: {csv_path}"], [], 0, []
    except csv.Error as exc:
        return False, [f"ERROR: CSV parse error in {csv_path}: {exc}"], [], 0, []

    # Strip whitespace and BOM.
    header = [col.strip().lstrip('\ufeff') for col in header]
    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    extensions = [col for col in header if col not in REQUIRED_COLUMNS]
    row_count = len(raw_rows)
    findings = []
    dict_rows: list[dict[str, str]] = []

    expected_width = len(header)
    for index, row in enumerate(raw_rows, start=2):
        if len(row) != expected_width:
            dependency_id = row[1] if len(row) > 1 else "<missing>"
            findings.append(
                f"Row {index} field count mismatch: expected {expected_width}, "
                f"found {len(row)} (DependencyID={dependency_id})"
            )
        padded = row + [""] * max(0, expected_width - len(row))
        dict_rows.append({name: padded[column_index] for column_index, name in enumerate(header)})

    if "RegisterSchemaVersion" in header:
        version_index = header.index("RegisterSchemaVersion")
        for index, row in enumerate(raw_rows, start=2):
            if len(row) <= version_index:
                continue
            if row[version_index].strip() != "v3.1":
                dependency_id = row[1] if len(row) > 1 else "<missing>"
                findings.append(
                    f"Row {index} invalid RegisterSchemaVersion: "
                    f"{row[version_index]!r} (DependencyID={dependency_id})"
                )

    if missing:
        findings.append(f"Missing columns ({len(missing)}): {', '.join(missing)}")

    if not schema_only and not missing:
        findings.extend(validate_row_semantics(dict_rows))

    return not findings, findings, extensions, row_count, header


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Validate only CSV shape/version. Use only for historical legacy snapshots.",
    )
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    valid, findings, extensions, row_count, header = validate(args.csv_path, schema_only=args.schema_only)

    if not valid:
        print(f"INVALID: {args.csv_path}")
        for finding in findings:
            print(f"  {finding}")
        print(f"  Data rows: {row_count}")
        sys.exit(1)

    print(f"VALID: {args.csv_path}")
    print(f"  Columns: {len(header)} ({len(REQUIRED_COLUMNS)} required + {len(extensions)} extension)")
    print(f"  Data rows: {row_count}")
    if extensions:
        print(f"  Extensions: {', '.join(extensions)}")
    sys.exit(0)
