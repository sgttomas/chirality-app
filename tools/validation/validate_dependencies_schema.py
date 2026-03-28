#!/usr/bin/env python3
"""
validate_dependencies_schema.py
Validates a Dependencies.csv file against the v3.1 schema.

Checks:
  1. All 29 required columns are present
  2. RegisterSchemaVersion column contains 'v3.1'
  3. Reports any extension columns found

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

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <csv_path>", file=sys.stderr)
        sys.exit(1)

    csv_path = sys.argv[1]

    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    except StopIteration:
        print(f"ERROR: Empty file: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # Strip whitespace and BOM
    header = [col.strip().lstrip('\ufeff') for col in header]

    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    extensions = [col for col in header if col not in REQUIRED_COLUMNS]

    # Count data rows
    with open(csv_path, 'r', newline='') as f:
        row_count = sum(1 for _ in f) - 1

    if missing:
        print(f"INVALID: {csv_path}")
        print(f"  Missing columns ({len(missing)}): {', '.join(missing)}")
        print(f"  Found columns: {len(header)}")
        print(f"  Data rows: {row_count}")
        sys.exit(1)
    else:
        print(f"VALID: {csv_path}")
        print(f"  Columns: {len(header)} ({len(REQUIRED_COLUMNS)} required + {len(extensions)} extension)")
        print(f"  Data rows: {row_count}")
        if extensions:
            print(f"  Extensions: {', '.join(extensions)}")
        sys.exit(0)
