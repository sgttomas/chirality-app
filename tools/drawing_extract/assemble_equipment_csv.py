#!/usr/bin/env python3
"""
assemble_equipment_csv.py
Assemble per-page drawing extraction outputs into one combined CSV.

Supports page-level markdown stubs and page-level csv_row outputs.

Usage:
    python3 assemble_equipment_csv.py <source_dir> <output_csv> --pdf-stem STEM --start-page 7 --end-page 61
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def parse_markdown_stub(path: Path, page_num: int) -> tuple[list[list[str]], bool]:
    rows: list[list[str]] = []
    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("| equipment_number | equipment_name | drawing |"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and line.startswith("| "):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 3 and any(parts):
                rows.append([parts[0], parts[1], parts[2], str(page_num)])
            continue
        if in_table and not line.startswith("| "):
            break
    return rows, len(rows) == 0


def parse_csv_rows(path: Path) -> tuple[list[list[str]], bool]:
    rows: list[list[str]] = []
    no_findings = False
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            status = (record.get("status") or "").strip()
            if status == "NO_FINDINGS":
                no_findings = True
                continue
            rows.append([
                (record.get("equipment_number") or "").strip(),
                (record.get("equipment_name") or "").strip(),
                (record.get("drawing") or "").strip(),
                (record.get("source_page") or "").strip(),
            ])
    return rows, no_findings and len(rows) == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble combined equipment CSV from per-page outputs.")
    parser.add_argument("source_dir")
    parser.add_argument("output_csv")
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    output_csv = Path(args.output_csv).resolve()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    combined_rows: list[list[str]] = []
    no_findings_pages: list[int] = []
    missing_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        md_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        csv_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_rows.csv"

        if md_path.is_file():
            page_rows, no_findings = parse_markdown_stub(md_path, page_num)
        elif csv_path.is_file():
            page_rows, no_findings = parse_csv_rows(csv_path)
        else:
            missing_pages.append(page_num)
            continue

        if no_findings:
            no_findings_pages.append(page_num)
        combined_rows.extend(page_rows)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["equipment_number", "equipment_name", "drawing", "source_page"])
        writer.writerows(combined_rows)

    print(f"rows={len(combined_rows)}")
    print(f"no_findings_pages={','.join(str(p) for p in no_findings_pages) or 'none'}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"output={output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
