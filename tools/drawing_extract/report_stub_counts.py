#!/usr/bin/env python3
"""
report_stub_counts.py
Produce a deterministic per-page coverage report from page-level equipment stubs.

This is intended as a QA gate before combined assembly so low-row pages,
NO_FINDINGS pages, and blank-tag contamination are explicitly visible.

Usage:
    python3 report_stub_counts.py <source_dir> <output_csv> --pdf-stem STEM --start-page 7 --end-page 61
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from normalize_equipment_stub_layout import parse_stub


def main() -> int:
    parser = argparse.ArgumentParser(description="Report per-page equipment stub coverage counts.")
    parser.add_argument("source_dir")
    parser.add_argument("output_csv")
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
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

    rows: list[dict[str, str]] = []
    missing_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        if not stub_path.is_file():
            missing_pages.append(page_num)
            rows.append(
                {
                    "page": str(page_num),
                    "status": "MISSING",
                    "row_count": "0",
                    "blank_tag_count": "0",
                    "drawing": "",
                    "system_name": "",
                    "note": "stub_missing",
                }
            )
            continue

        parsed = parse_stub(stub_path, page_num)
        data_rows = parsed["rows"]  # type: ignore[assignment]
        meaningful_rows = [row for row in data_rows if row[0] or row[1] or row[3]]
        blank_tag_count = sum(1 for row in meaningful_rows if not str(row[0]).strip())

        rows.append(
            {
                "page": str(page_num),
                "status": str(parsed["status"]),
                "row_count": str(len(meaningful_rows)),
                "blank_tag_count": str(blank_tag_count),
                "drawing": str(parsed["drawing"]),
                "system_name": str(parsed["system_name"]),
                "note": str(parsed["note"]),
            }
        )

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["page", "status", "row_count", "blank_tag_count", "drawing", "system_name", "note"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"rows_written={len(rows)}")
    print(f"missing_pages={','.join(str(page) for page in missing_pages) or 'none'}")
    print(f"report={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
