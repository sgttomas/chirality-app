#!/usr/bin/env python3
"""
merge_equipment_detailed.py
Deterministic side-by-side merge of two combined equipment CSVs on
`equipment_number` (PFD-equipment-repertoire-scoped; see design decision #12).

Inputs:
  --extracted : combined CSV from a DRAWING_EXTRACT run (Deliverable 10 schema)
  --existing  : baseline/existing CSV to compare against (same schema or subset)

Output (one merge_result CSV + two unmatched auxiliary CSVs) is placed in
--output-dir using the canonical naming:
  {pdf_stem}_combined_pages_{start:04d}_{end:04d}_merge_result.csv
  {pdf_stem}_combined_pages_{start:04d}_{end:04d}_merge_unmatched_extracted.csv
  {pdf_stem}_combined_pages_{start:04d}_{end:04d}_merge_unmatched_existing.csv

For each equipment_number present in EITHER input a row is emitted in the merge
result. For every column in the union of input columns, two cells are written:
  {col}_extracted  — value from extracted CSV (empty if not present)
  {col}_existing   — value from existing CSV (empty if not present)

No auto-resolution is performed; all cells are preserved verbatim for human
review. Conflicts are reported separately by flag_merge_conflicts.py.

Usage:
    python3 merge_equipment_detailed.py \
        --extracted CSV1 --existing CSV2 \
        --output-dir DIR --pdf-stem STEM \
        --start-page N --end-page M \
        --merge-key equipment_number
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


MERGE_KEY_SUPPORTED = "equipment_number"


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return fieldnames, rows


def _index_by_key(
    rows: list[dict[str, str]],
    key: str,
) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        key_value = (row.get(key) or "").strip()
        if not key_value:
            continue
        # First occurrence wins deterministically; within-file duplicates are
        # expected to be flagged by flag_duplicate_equipment_csv.py upstream.
        if key_value not in indexed:
            indexed[key_value] = row
    return indexed


def _union_columns(
    extracted_cols: list[str],
    existing_cols: list[str],
) -> list[str]:
    """Stable union: extracted order first, then any new existing columns."""
    seen: set[str] = set()
    union: list[str] = []
    for col in extracted_cols:
        if col not in seen:
            seen.add(col)
            union.append(col)
    for col in existing_cols:
        if col not in seen:
            seen.add(col)
            union.append(col)
    return union


def _build_sidebyside_fieldnames(
    merge_key: str,
    union_cols: list[str],
) -> list[str]:
    """merge_key first (plain), then every non-key column as (_extracted, _existing) pair."""
    fieldnames: list[str] = [merge_key]
    for col in union_cols:
        if col == merge_key:
            continue
        fieldnames.append(f"{col}_extracted")
        fieldnames.append(f"{col}_existing")
    return fieldnames


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Side-by-side merge of two combined equipment CSVs on equipment_number."
    )
    parser.add_argument("--extracted", required=True)
    parser.add_argument("--existing", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--merge-key", default=MERGE_KEY_SUPPORTED)
    args = parser.parse_args()

    if args.merge_key != MERGE_KEY_SUPPORTED:
        print(
            f"ERROR: only '{MERGE_KEY_SUPPORTED}' supported in v1; other keys deferred",
            file=sys.stderr,
        )
        return 2

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    extracted_path = Path(args.extracted).resolve()
    existing_path = Path(args.existing).resolve()

    if not extracted_path.is_file():
        print(f"ERROR: extracted CSV not found: {extracted_path}", file=sys.stderr)
        return 2
    if not existing_path.is_file():
        print(f"ERROR: existing CSV not found: {existing_path}", file=sys.stderr)
        return 2

    extracted_cols, extracted_rows = _read_csv(extracted_path)
    existing_cols, existing_rows = _read_csv(existing_path)

    if args.merge_key not in extracted_cols:
        print(
            f"ERROR: missing merge key '{args.merge_key}' in {extracted_path}",
            file=sys.stderr,
        )
        return 1
    if args.merge_key not in existing_cols:
        print(
            f"ERROR: missing merge key '{args.merge_key}' in {existing_path}",
            file=sys.stderr,
        )
        return 1

    extracted_index = _index_by_key(extracted_rows, args.merge_key)
    existing_index = _index_by_key(existing_rows, args.merge_key)

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    prefix = (
        f"{args.pdf_stem}_combined_pages_"
        f"{args.start_page:04d}_{args.end_page:04d}"
    )
    merge_result_path = output_dir / f"{prefix}_merge_result.csv"
    unmatched_extracted_path = output_dir / f"{prefix}_merge_unmatched_extracted.csv"
    unmatched_existing_path = output_dir / f"{prefix}_merge_unmatched_existing.csv"

    union_cols = _union_columns(extracted_cols, existing_cols)
    sbs_fieldnames = _build_sidebyside_fieldnames(args.merge_key, union_cols)

    # Deterministic row order: keys in extracted order first (matched + extracted-only),
    # then existing-only keys in existing order.
    ordered_keys: list[str] = []
    seen_keys: set[str] = set()
    for row in extracted_rows:
        key_value = (row.get(args.merge_key) or "").strip()
        if key_value and key_value not in seen_keys:
            seen_keys.add(key_value)
            ordered_keys.append(key_value)
    for row in existing_rows:
        key_value = (row.get(args.merge_key) or "").strip()
        if key_value and key_value not in seen_keys:
            seen_keys.add(key_value)
            ordered_keys.append(key_value)

    matched = 0
    unmatched_extracted = 0
    unmatched_existing = 0

    with merge_result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=sbs_fieldnames)
        writer.writeheader()
        for key_value in ordered_keys:
            in_extracted = key_value in extracted_index
            in_existing = key_value in existing_index
            if in_extracted and in_existing:
                matched += 1
            elif in_extracted:
                unmatched_extracted += 1
            else:
                unmatched_existing += 1

            e_row = extracted_index.get(key_value, {})
            x_row = existing_index.get(key_value, {})
            record: dict[str, str] = {args.merge_key: key_value}
            for col in union_cols:
                if col == args.merge_key:
                    continue
                record[f"{col}_extracted"] = (e_row.get(col) or "") if in_extracted else ""
                record[f"{col}_existing"] = (x_row.get(col) or "") if in_existing else ""
            writer.writerow(record)

    # Aux report: unmatched_extracted — rows only in extracted, emitted with
    # the extracted CSV's own columns (full fidelity, not the side-by-side view).
    with unmatched_extracted_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=extracted_cols)
        writer.writeheader()
        for row in extracted_rows:
            key_value = (row.get(args.merge_key) or "").strip()
            if not key_value:
                continue
            if key_value not in existing_index:
                writer.writerow({col: (row.get(col) or "") for col in extracted_cols})

    # Aux report: unmatched_existing — symmetric counterpart.
    with unmatched_existing_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=existing_cols)
        writer.writeheader()
        for row in existing_rows:
            key_value = (row.get(args.merge_key) or "").strip()
            if not key_value:
                continue
            if key_value not in extracted_index:
                writer.writerow({col: (row.get(col) or "") for col in existing_cols})

    print(f"matched={matched}")
    print(f"unmatched_extracted={unmatched_extracted}")
    print(f"unmatched_existing={unmatched_existing}")
    print(f"output_dir={output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
