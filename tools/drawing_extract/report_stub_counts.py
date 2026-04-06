#!/usr/bin/env python3
"""
report_stub_counts.py
Produce a deterministic per-page coverage report from page-level equipment stubs.

This is intended as a QA gate before combined assembly so low-row pages,
NO_FINDINGS pages, and blank-tag contamination are explicitly visible.

Reads v2 target-aware stubs at
``{source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md``
via the frozen W1 API (``parse_stub`` / ``resolve_stub_path``).

Basic target CSV schema:
    page, status, row_count, blank_tag_count, drawing, system_name, note

Detailed target adds per-field count columns plus QA heuristic columns:
    {field}_populated_count, {field}_total_count
    missing_required_fields
    identical_value_flags

See skills/drawing-extract-page/QA_CHECKS.md sections
"Required-fields warnings" and "Detail capture rate" for metric semantics.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    BASE_COLUMNS,
    parse_stub,
    resolve_stub_path,
)


def _detail_columns_for_run(
    extraction_target: str,
    requested_known_fields: list[str],
    requested_extra_fields: list[dict[str, str]],
) -> list[str]:
    """Return the detail column names in canonical stub order (non-base cols)."""
    if extraction_target != "top_equipment_header_detailed":
        return []
    cols: list[str] = []
    cols.extend([str(f) for f in requested_known_fields])
    for extra in requested_extra_fields:
        name = str(extra.get("name", "") or "")
        if name:
            cols.append(name)
    return cols


def main() -> int:
    parser = argparse.ArgumentParser(description="Report per-page equipment stub coverage counts.")
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

    is_detailed = args.extraction_target == "top_equipment_header_detailed"

    # First pass: parse all stubs and discover detail column set from the first
    # available stub so the CSV header is stable across pages. If stubs disagree
    # on detail columns across pages, we prefer the first available (reported as
    # run-configured) and ignore variance beyond it. The schema validator
    # (W2 deliverable) handles cross-page schema drift detection.
    parsed_pages: list[tuple[int, Path, dict | None]] = []
    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = resolve_stub_path(
            source_dir,
            args.drawing_type,
            args.extraction_target,
            args.pdf_stem,
            page_num,
        )
        if not stub_path.is_file():
            parsed_pages.append((page_num, stub_path, None))
            continue
        parsed = parse_stub(stub_path, page_num)
        parsed_pages.append((page_num, stub_path, parsed))

    detail_columns: list[str] = []
    required_fields: list[str] = []
    if is_detailed:
        for _, _, parsed in parsed_pages:
            if parsed is None:
                continue
            detail_columns = _detail_columns_for_run(
                args.extraction_target,
                list(parsed.get("requested_known_fields") or []),
                list(parsed.get("requested_extra_fields") or []),
            )
            required_fields = [str(x) for x in (parsed.get("required_fields") or [])]
            break

    # Build CSV fieldnames
    base_fields = ["page", "status", "row_count", "blank_tag_count", "drawing", "system_name", "note"]
    detail_field_list: list[str] = []
    for field in detail_columns:
        detail_field_list.append(f"{field}_populated_count")
        detail_field_list.append(f"{field}_total_count")
    heuristic_fields: list[str] = []
    if is_detailed:
        heuristic_fields = ["missing_required_fields", "identical_value_flags"]
    fieldnames = base_fields + detail_field_list + heuristic_fields

    rows: list[dict[str, str]] = []
    missing_pages: list[int] = []
    required_field_warnings: list[str] = []  # "page:field" entries
    identical_value_flag_entries: list[str] = []  # "page:field" entries

    base_len = len(BASE_COLUMNS)

    for page_num, _, parsed in parsed_pages:
        if parsed is None:
            missing_pages.append(page_num)
            entry: dict[str, str] = {
                "page": str(page_num),
                "status": "MISSING",
                "row_count": "0",
                "blank_tag_count": "0",
                "drawing": "",
                "system_name": "",
                "note": "stub_missing",
            }
            for field in detail_columns:
                entry[f"{field}_populated_count"] = "0"
                entry[f"{field}_total_count"] = "0"
            if is_detailed:
                entry["missing_required_fields"] = ""
                entry["identical_value_flags"] = ""
            rows.append(entry)
            continue

        data_rows = parsed["rows"]
        meaningful_rows = [
            row for row in data_rows
            if (len(row) >= base_len and (row[0] or row[1] or row[3]))
        ]
        row_count = len(meaningful_rows)
        blank_tag_count = sum(1 for row in meaningful_rows if not str(row[0]).strip())

        entry = {
            "page": str(page_num),
            "status": str(parsed["status"]),
            "row_count": str(row_count),
            "blank_tag_count": str(blank_tag_count),
            "drawing": str(parsed["drawing"]),
            "system_name": str(parsed["system_name"]),
            "note": str(parsed["note"]),
        }

        # Per-field counts (detailed only)
        page_missing_required: list[str] = []
        page_identical_flags: list[str] = []
        for field_idx, field in enumerate(detail_columns):
            col_idx = base_len + field_idx
            values: list[str] = []
            for row in meaningful_rows:
                if len(row) > col_idx:
                    values.append(str(row[col_idx]).strip())
                else:
                    values.append("")
            populated = sum(1 for v in values if v)
            entry[f"{field}_populated_count"] = str(populated)
            entry[f"{field}_total_count"] = str(row_count)

            if field in required_fields:
                has_blank = any(not v for v in values)
                if has_blank and row_count > 0:
                    page_missing_required.append(field)
                    required_field_warnings.append(f"{page_num}:{field}")

            if row_count >= 2:
                non_blank = [v for v in values if v]
                if len(non_blank) == row_count and len(set(non_blank)) == 1:
                    page_identical_flags.append(field)
                    identical_value_flag_entries.append(f"{page_num}:{field}")

        if is_detailed:
            entry["missing_required_fields"] = ",".join(page_missing_required)
            entry["identical_value_flags"] = ",".join(page_identical_flags)

        rows.append(entry)

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"rows_written={len(rows)}")
    print(f"missing_pages={','.join(str(page) for page in missing_pages) or 'none'}")
    print(f"report={output_csv}")
    if is_detailed:
        print(f"required_field_warnings={','.join(required_field_warnings) or 'none'}")
        print(f"identical_value_flags={','.join(identical_value_flag_entries) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
