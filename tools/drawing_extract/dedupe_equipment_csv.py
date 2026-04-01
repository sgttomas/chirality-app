#!/usr/bin/env python3
"""
dedupe_equipment_csv.py
Deduplicate a combined equipment CSV by a chosen key, keeping first occurrence.

Usage:
    python3 dedupe_equipment_csv.py <input_csv> <output_csv> [--key equipment_number]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplicate equipment CSV by key.")
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

        seen: set[str] = set()
        rows: list[dict[str, str]] = []
        for record in reader:
            key_value = (record.get(args.key) or "").strip()
            if not key_value or key_value in seen:
                continue
            seen.add(key_value)
            rows.append(record)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"rows={len(rows)}")
    print(f"key={args.key}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
