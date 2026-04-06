#!/usr/bin/env python3
"""
assemble_equipment_markdown.py
Assemble per-page v2 drawing-extract stubs into one combined Markdown table.

Reads target-aware v2 stubs at
  {source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md
and emits a combined Markdown document with the same target-driven columns
as the combined CSV (per DRAWING_EXTRACT Deliverables 4, 6, 10).

Sections:
- header + summary
- findings table (target-driven columns)
- "Pages Without Top Equipment Headers" (NO_FINDINGS pages)
- "Missing Page Outputs" (pages with no stub on disk)

Usage:
    python3 assemble_equipment_markdown.py \
        --source-dir SRC --drawing-type PFD --extraction-target top_equipment_header_basic \
        --pdf-stem STEM --start-page 7 --end-page 106 --output-md PATH [--source-pdf-name FILE.pdf]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    BASE_COLUMNS,
    build_column_order,
    parse_stub,
    resolve_stub_path,
)


def _row_is_no_findings_placeholder(record: dict[str, str]) -> bool:
    eq_number = (record.get("equipment_number") or "").strip()
    eq_name = (record.get("equipment_name") or "").strip()
    drawing = (record.get("drawing") or "").strip()
    return not eq_number and not eq_name and not drawing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble combined equipment Markdown from v2 per-page stubs."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--source-pdf-name")
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    output_md = Path(args.output_md).resolve()
    output_md.parent.mkdir(parents=True, exist_ok=True)

    columns: list[str] | None = None
    combined_records: list[dict[str, str]] = []
    no_findings_pages: list[tuple[int, str, str]] = []
    failed_pages: list[tuple[int, str, str]] = []
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
            failed_pages.append((page_num, str(parsed.get("system_name") or ""), str(parsed.get("drawing") or "")))
            continue

        if columns is None:
            columns = build_column_order(
                args.extraction_target,
                parsed.get("requested_known_fields"),
                parsed.get("requested_extra_fields"),
            )

        page_columns = list(parsed.get("columns") or BASE_COLUMNS)
        page_rows = list(parsed.get("rows") or [])
        drawing = str(parsed.get("drawing") or "")
        system_name = str(parsed.get("system_name") or "")

        kept_rows = 0
        for row in page_rows:
            record: dict[str, str] = {}
            for col_idx, col in enumerate(page_columns):
                value = row[col_idx] if col_idx < len(row) else ""
                record[col] = value
            if _row_is_no_findings_placeholder(record):
                continue
            record["source_page"] = str(page_num)
            combined_records.append(record)
            kept_rows += 1

        if kept_rows == 0:
            no_findings_pages.append((page_num, system_name, drawing))

    if columns is None:
        columns = build_column_order(args.extraction_target, [], [])

    header_cols = list(columns)

    lines = ["# Combined Equipment Table", ""]
    if args.source_pdf_name:
        lines.append(f"- Source PDF: `{args.source_pdf_name}`")
    lines.extend([
        f"- Drawing type: `{args.drawing_type}`",
        f"- Extraction target: `{args.extraction_target}`",
        f"- Page scope: `{args.start_page}-{args.end_page}`",
        f"- Equipment rows extracted: `{len(combined_records)}`",
        f"- Pages without separated top-of-sheet equipment headers: `{len(no_findings_pages)}`",
        "",
        "| " + " | ".join(header_cols) + " |",
        "| " + " | ".join("---" for _ in header_cols) + " |",
    ])
    for record in combined_records:
        row_cells = [record.get(col, "") for col in header_cols]
        lines.append("| " + " | ".join(row_cells) + " |")

    lines.extend([
        "",
        "## Pages Without Top Equipment Headers",
        "",
        "| page | system_name | drawing |",
        "| --- | --- | --- |",
    ])
    for page_num, system_name, drawing in no_findings_pages:
        lines.append(f"| {page_num} | {system_name} | {drawing} |")

    if failed_pages:
        lines.extend([
            "",
            "## Failed Pages",
            "",
            "| page | system_name | drawing |",
            "| --- | --- | --- |",
        ])
        for page_num, system_name, drawing in failed_pages:
            lines.append(f"| {page_num} | {system_name} | {drawing} |")

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

    print(f"rows={len(combined_records)}")
    print(f"no_findings_pages={','.join(str(p) for p, _, _ in no_findings_pages) or 'none'}")
    print(f"failed_pages={','.join(str(p) for p, _, _ in failed_pages) or 'none'}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"output={output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
