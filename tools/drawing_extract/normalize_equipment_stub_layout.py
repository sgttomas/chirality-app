#!/usr/bin/env python3
"""
normalize_equipment_stub_layout.py
Rewrite page-level equipment stubs into one canonical Markdown layout.

Usage:
    python3 normalize_equipment_stub_layout.py <source_dir> --pdf-stem STEM --start-page 7 --end-page 61
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def extract_backticked_value(line: str) -> str:
    parts = line.split("`")
    if len(parts) >= 2:
        return parts[1].strip()
    return ""


def parse_stub(path: Path, page_num: int) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    source_pdf = ""
    source_page = f"{page_num}"
    extraction_mode = "top_equipment_header_with_dwg"
    drawing = ""
    system_name = ""
    rows: list[list[str]] = []

    in_table = False
    for line in lines:
        if "Source PDF:" in line:
            source_pdf = extract_backticked_value(line)
        elif "Source page:" in line:
            source_page = extract_backticked_value(line) or f"{page_num}"
        elif "Extraction mode:" in line:
            extraction_mode = extract_backticked_value(line) or extraction_mode
        elif "DWG NO.:" in line:
            drawing = extract_backticked_value(line)
        elif "System name:" in line:
            system_name = extract_backticked_value(line)

    for line in lines:
        if line.startswith("| equipment_number | equipment_name | system_name | drawing |"):
            in_table = True
            continue
        if line.startswith("| equipment_number | equipment_name | drawing |"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and line.startswith("| "):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 4:
                if not parts[2]:
                    parts[2] = system_name
                rows.append(parts)
            elif len(parts) == 3:
                rows.append([parts[0], parts[1], system_name, parts[2]])
            continue
        if in_table and not line.startswith("| "):
            break

    status = "SUCCESS"
    note = "Top-of-sheet equipment header present."
    meaningful_rows = [row for row in rows if row[0] or row[1] or row[3]]
    if not meaningful_rows:
        status = "NO_FINDINGS"
        note = "No separated top-of-sheet equipment header was identified."
        rows = [["", "", system_name, ""]]

    return {
        "source_pdf": source_pdf,
        "source_page": source_page,
        "extraction_mode": extraction_mode,
        "drawing": drawing,
        "system_name": system_name,
        "rows": rows,
        "status": status,
        "note": note,
    }


def render_stub(page_num: int, data: dict[str, object]) -> str:
    lines = [
        f"# Page {page_num} Equipment Extraction",
        "",
        f"- Source PDF: `{data['source_pdf']}`",
        f"- Source page: `{data['source_page']}`",
        f"- Extraction mode: `{data['extraction_mode']}`",
        f"- DWG NO.: `{data['drawing']}`",
        f"- System name: `{data['system_name']}`",
        "",
        "| equipment_number | equipment_name | system_name | drawing |",
        "| --- | --- | --- | --- |",
    ]

    for equipment_number, equipment_name, system_name, drawing in data["rows"]:
        lines.append(f"| {equipment_number} | {equipment_name} | {system_name} | {drawing} |")

    lines.extend(
        [
            "",
            f"- {data['note']}",
            f"- Extraction status: `{data['status']}`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize equipment stub markdown layout.")
    parser.add_argument("source_dir")
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

    updated = 0
    missing_pages: list[int] = []
    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue

        original = stub_path.read_text(encoding="utf-8")
        normalized = render_stub(page_num, parse_stub(stub_path, page_num))
        if normalized != original:
            stub_path.write_text(normalized, encoding="utf-8")
            updated += 1

    print(f"updated={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
