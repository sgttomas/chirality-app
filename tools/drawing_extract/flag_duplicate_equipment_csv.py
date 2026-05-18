#!/usr/bin/env python3
"""
flag_duplicate_equipment_csv.py
Flag repeated equipment numbers in a combined equipment CSV without collapsing rows.

Usage:
    python3 flag_duplicate_equipment_csv.py <input_csv> <output_csv> [--key equipment_number]
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


def classify_duplicate(records: list[dict[str, str]]) -> str:
    names = {((r.get("equipment_name") or "").strip()) for r in records}
    drawings = {((r.get("drawing") or "").strip()) for r in records}
    if len(names) == 1 and len(drawings) == 1:
        return "EXACT_REPEAT"
    if len(names) > 1 and len(drawings) == 1:
        return "NAME_CONFLICT"
    if len(names) == 1 and len(drawings) > 1:
        return "DRAWING_CONFLICT"
    return "NAME_AND_DRAWING_CONFLICT"


def main() -> int:
    parser = argparse.ArgumentParser(description="Flag duplicate equipment numbers in a combined CSV.")
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    parser.add_argument("--key", default="equipment_number")
    args = parser.parse_args()

    input_csv = Path(args.input_csv).resolve()
    output_csv = Path(args.output_csv).resolve()

    if not input_csv.is_file():
        print(f"ERROR: input CSV not found: {input_csv}", file=sys.stderr)
        return 2

    with input_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        if fieldnames is None or args.key not in fieldnames:
            print(f"ERROR: missing key column: {args.key}", file=sys.stderr)
            return 2
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for record in reader:
            key_value = (record.get(args.key) or "").strip()
            if key_value:
                grouped[key_value].append(record)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "equipment_number",
            "occurrence_count",
            "equipment_names",
            "drawings",
            "source_pages",
            "duplicate_type",
        ])
        flagged = 0
        for equipment_number in sorted(grouped):
            records = grouped[equipment_number]
            if len(records) < 2:
                continue
            flagged += 1
            names = sorted({(r.get("equipment_name") or "").strip() for r in records if (r.get("equipment_name") or "").strip()})
            drawings = sorted({(r.get("drawing") or "").strip() for r in records if (r.get("drawing") or "").strip()})
            pages = sorted(
                {(r.get("source_page") or "").strip() for r in records if (r.get("source_page") or "").strip()},
                key=lambda value: int(value),
            )
            writer.writerow([
                equipment_number,
                len(records),
                " || ".join(names),
                " || ".join(drawings),
                ",".join(pages),
                classify_duplicate(records),
            ])

    print(f"flagged={flagged}")
    print(f"key={args.key}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
