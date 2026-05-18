#!/usr/bin/env python3
"""
validate_dependencies_schema.py
Validates a Dependencies.csv file against the v3.1 schema.

Checks:
  1. All 29 required columns are present
  2. RegisterSchemaVersion column contains 'v3.1'
  3. Every data row has the same field count as the header
  4. Reports any extension columns found

Usage:
    python3 validate_dependencies_schema.py <csv_path>

Exit codes:
    0 = valid schema
    1 = invalid schema or file error
"""

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

def validate(csv_path):
    try:
        with open(csv_path, 'r', newline='') as f:
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

    expected_width = len(header)
    for index, row in enumerate(raw_rows, start=2):
        if len(row) != expected_width:
            dependency_id = row[1] if len(row) > 1 else "<missing>"
            findings.append(
                f"Row {index} field count mismatch: expected {expected_width}, "
                f"found {len(row)} (DependencyID={dependency_id})"
            )

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

    return not findings, findings, extensions, row_count, header


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]
    valid, findings, extensions, row_count, header = validate(csv_path)

    if not valid:
        print(f"INVALID: {csv_path}")
        for finding in findings:
            print(f"  {finding}")
        print(f"  Data rows: {row_count}")
        sys.exit(1)

    print(f"VALID: {csv_path}")
    print(f"  Columns: {len(header)} ({len(REQUIRED_COLUMNS)} required + {len(extensions)} extension)")
    print(f"  Data rows: {row_count}")
    if extensions:
        print(f"  Extensions: {', '.join(extensions)}")
    sys.exit(0)
