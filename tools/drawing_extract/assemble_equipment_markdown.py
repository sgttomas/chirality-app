#!/usr/bin/env python3
"""
assemble_equipment_markdown.py
Assemble per-page drawing extraction outputs into one combined Markdown table.

Usage:
    python3 assemble_equipment_markdown.py <source_dir> <output_md> --pdf-stem STEM --start-page 7 --end-page 61 [--source-pdf-name FILE.pdf]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def parse_markdown_stub(path: Path, page_num: int) -> tuple[list[list[str]], bool, str]:
    rows: list[list[str]] = []
    drawing = ""
    in_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("- DWG NO.: "):
            parts = line.split("`")
            if len(parts) >= 2:
                drawing = parts[1].strip()
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
    return rows, len(rows) == 0, drawing


def parse_csv_rows(path: Path) -> tuple[list[list[str]], bool, str]:
    rows: list[list[str]] = []
    no_findings = False
    drawing = ""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            drawing = (record.get("drawing") or drawing).strip()
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
    return rows, no_findings and len(rows) == 0, drawing


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble combined equipment Markdown from per-page outputs.")
    parser.add_argument("source_dir")
    parser.add_argument("output_md")
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--source-pdf-name")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).resolve()
    output_md = Path(args.output_md).resolve()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    output_md.parent.mkdir(parents=True, exist_ok=True)

    combined_rows: list[list[str]] = []
    no_findings_pages: list[tuple[int, str]] = []
    missing_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        md_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        csv_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_rows.csv"

        if md_path.is_file():
            page_rows, no_findings, drawing = parse_markdown_stub(md_path, page_num)
        elif csv_path.is_file():
            page_rows, no_findings, drawing = parse_csv_rows(csv_path)
        else:
            missing_pages.append(page_num)
            continue

        if no_findings:
            no_findings_pages.append((page_num, drawing))
        combined_rows.extend(page_rows)

    lines = ["# Combined Equipment Table", ""]
    if args.source_pdf_name:
        lines.append(f"- Source PDF: `{args.source_pdf_name}`")
    lines.extend([
        f"- Page scope: `{args.start_page}-{args.end_page}`",
        f"- Equipment rows extracted: `{len(combined_rows)}`",
        f"- Pages without separated top-of-sheet equipment headers: `{len(no_findings_pages)}`",
        "",
        "| equipment_number | equipment_name | drawing |",
        "| --- | --- | --- |",
    ])
    for equipment_number, equipment_name, drawing, _source_page in combined_rows:
        lines.append(f"| {equipment_number} | {equipment_name} | {drawing} |")

    lines.extend([
        "",
        "## Pages Without Top Equipment Headers",
        "",
        "| page | drawing |",
        "| --- | --- |",
    ])
    for page_num, drawing in no_findings_pages:
        lines.append(f"| {page_num} | {drawing} |")

    if missing_pages:
        lines.extend([
            "",
            "## Missing Page Outputs",
            "",
            "| page |",
            "| --- |",
        ])
        for page_num in missing_pages:
            lines.append(f"| {page_num} |")

    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"rows={len(combined_rows)}")
    print(f"no_findings_pages={','.join(str(p) for p, _ in no_findings_pages) or 'none'}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"output={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
