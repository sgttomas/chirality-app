#!/usr/bin/env python3
"""
assemble_equipment_csv.py
Assemble per-page v2 drawing-extract stubs into one combined CSV.

Reads target-aware v2 stubs at
  {source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md
and emits a combined CSV with target-driven columns plus `source_page`
(per DRAWING_EXTRACT Deliverables 4, 6, 10).

- Basic target:    equipment_number, equipment_name, system_name, drawing, source_page
- Detailed target: base 4 + requested_known_fields (canonical catalog order) +
                   requested_extra_fields (request order) + source_page

Rows whose equipment_number, equipment_name, and drawing are ALL blank
(NO_FINDINGS placeholder rows) are skipped. All other rows are emitted.

Usage:
    python3 assemble_equipment_csv.py \
        --source-dir SRC --drawing-type PFD --extraction-target top_equipment_header_basic \
        --pdf-stem STEM --start-page 7 --end-page 106 --output-csv PATH
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    BASE_COLUMNS,
    build_column_order,
    parse_stub,
    resolve_stub_path,
)


def _row_is_no_findings_placeholder(row: dict[str, str]) -> bool:
    """Skip row if equipment_number, equipment_name, and drawing are all blank."""
    eq_number = (row.get("equipment_number") or "").strip()
    eq_name = (row.get("equipment_name") or "").strip()
    drawing = (row.get("drawing") or "").strip()
    return not eq_number and not eq_name and not drawing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble combined equipment CSV from v2 per-page stubs."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    output_csv = Path(args.output_csv).resolve()
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    columns: list[str] | None = None
    combined_rows: list[dict[str, str]] = []
    no_findings_pages: list[int] = []
    failed_pages: list[int] = []
    missing_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = resolve_stub_path(
            source_dir,
            args.drawing_type,
            args.extraction_target,
            args.pdf_stem,
            page_num,
        )
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue

        parsed = parse_stub(stub_path, page_num)
        stub_status = str(parsed.get("status", ""))
        if stub_status in ("FAILED", "FAILED_INPUTS"):
            failed_pages.append(page_num)
            continue

        if columns is None:
            columns = build_column_order(
                args.extraction_target,
                parsed.get("requested_known_fields"),
                parsed.get("requested_extra_fields"),
            )

        page_columns = list(parsed.get("columns") or BASE_COLUMNS)
        page_rows = list(parsed.get("rows") or [])

        kept_rows = 0
        for row in page_rows:
            record: dict[str, str] = {}
            for col_idx, col in enumerate(page_columns):
                value = row[col_idx] if col_idx < len(row) else ""
                record[col] = value
            if _row_is_no_findings_placeholder(record):
                continue
            record["source_page"] = str(page_num)
            combined_rows.append(record)
            kept_rows += 1

        if kept_rows == 0:
            no_findings_pages.append(page_num)

    if columns is None:
        # No stubs found at all — still write a header-only CSV derived from target.
        columns = build_column_order(args.extraction_target, [], [])

    fieldnames = list(columns) + ["source_page"]

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in combined_rows:
            # DictWriter will emit empty strings for missing keys when restval set.
            writer.writerow({key: record.get(key, "") for key in fieldnames})

    print(f"rows={len(combined_rows)}")
    print(f"no_findings_pages={','.join(str(p) for p in no_findings_pages) or 'none'}")
    print(f"failed_pages={','.join(str(p) for p in failed_pages) or 'none'}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
