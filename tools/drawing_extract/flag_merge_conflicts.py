#!/usr/bin/env python3
"""
flag_merge_conflicts.py
Post-merge conflict reporter. Consumes the side-by-side merge_result CSV
produced by merge_equipment_detailed.py and emits one row per
equipment_number whose `{col}_extracted` and `{col}_existing` cells
disagree (both non-empty, values differ).

Absence is NOT disagreement: if one side is blank, no conflict is
recorded for that column. Cells where both sides are blank are also
ignored.

Output columns:
  equipment_number
  conflict_count
  conflicting_columns   — ' || '-joined sorted column names
  conflict_detail       — readable 'col=extracted="X"|existing="Y"; ...'

Usage:
    python3 flag_merge_conflicts.py --merge-result CSV --output-csv PATH
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


EXTRACTED_SUFFIX = "_extracted"
EXISTING_SUFFIX = "_existing"


def _discover_paired_columns(fieldnames: list[str]) -> list[str]:
    """Return the sorted set of base column names that have both
    {col}_extracted and {col}_existing variants in fieldnames."""
    extracted_bases = {
        name[: -len(EXTRACTED_SUFFIX)]
        for name in fieldnames
        if name.endswith(EXTRACTED_SUFFIX)
    }
    existing_bases = {
        name[: -len(EXISTING_SUFFIX)]
        for name in fieldnames
        if name.endswith(EXISTING_SUFFIX)
    }
    return sorted(extracted_bases & existing_bases)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag disagreements in a side-by-side merge_result CSV."
    )
    parser.add_argument("--merge-result", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    merge_result_path = Path(args.merge_result).resolve()
    output_csv = Path(args.output_csv).resolve()

    if not merge_result_path.is_file():
        print(f"ERROR: merge_result CSV not found: {merge_result_path}", file=sys.stderr)
        return 2

    with merge_result_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        if "equipment_number" not in fieldnames:
            print(
                "ERROR: missing 'equipment_number' column in merge_result",
                file=sys.stderr,
            )
            return 1
        paired_bases = _discover_paired_columns(fieldnames)
        rows = [dict(row) for row in reader]

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    conflicts = 0
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "equipment_number",
                "conflict_count",
                "conflicting_columns",
                "conflict_detail",
            ]
        )
        for row in rows:
            equipment_number = (row.get("equipment_number") or "").strip()
            if not equipment_number:
                continue
            conflicting_cols: list[str] = []
            detail_parts: list[str] = []
            for base in paired_bases:
                e_value = (row.get(f"{base}{EXTRACTED_SUFFIX}") or "").strip()
                x_value = (row.get(f"{base}{EXISTING_SUFFIX}") or "").strip()
                # Blank on either side -> absence, not disagreement.
                if not e_value or not x_value:
                    continue
                if e_value != x_value:
                    conflicting_cols.append(base)
                    detail_parts.append(
                        f'{base}=extracted="{e_value}"|existing="{x_value}"'
                    )
            if conflicting_cols:
                conflicts += 1
                writer.writerow(
                    [
                        equipment_number,
                        len(conflicting_cols),
                        " || ".join(conflicting_cols),
                        "; ".join(detail_parts),
                    ]
                )

    print(f"conflicts={conflicts}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
