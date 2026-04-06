#!/usr/bin/env python3
"""
backfill_stub_system_names.py
Update the ``system_name`` metadata field in v2 target-aware equipment stubs
and propagate the value to the ``system_name`` cell of every finding row so
every row's system_name matches the title-block system_name.

Reads/writes v2 target-aware stubs at
``{source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md``
via the frozen W1 API (``parse_stub`` / ``render_stub`` / ``resolve_stub_path``).

Uses a full parse -> mutate -> render round-trip; no text-level editing.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    BASE_COLUMNS,
    parse_stub,
    render_stub,
    resolve_stub_path,
)


# system_name is the 3rd base column (index 2)
_SYSTEM_NAME_COL_IDX = BASE_COLUMNS.index("system_name")


def load_system_names(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "page" not in reader.fieldnames or "system_name" not in reader.fieldnames:
            raise ValueError("system_names_csv must contain page and system_name columns")

        result: dict[int, str] = {}
        for record in reader:
            page_raw = (record.get("page") or "").strip()
            system_name = (record.get("system_name") or "").strip()
            if not page_raw:
                continue
            result[int(page_raw)] = system_name
        return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Backfill system-name metadata into v2 equipment stubs."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--system-names-csv", required=True)
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    system_names_csv = Path(args.system_names_csv).resolve()

    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2
    if not system_names_csv.is_file():
        print(f"ERROR: system_names_csv not found: {system_names_csv}", file=sys.stderr)
        return 2

    try:
        system_names = load_system_names(system_names_csv)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    updated = 0
    missing_pages: list[int] = []
    blank_system_pages: list[int] = []

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

        system_name = system_names.get(page_num, "").strip()
        if not system_name:
            blank_system_pages.append(page_num)
            continue

        parsed = parse_stub(stub_path, page_num)
        parsed["system_name"] = system_name
        updated_rows: list[list[str]] = []
        for row in parsed.get("rows", []):
            padded = list(row)
            while len(padded) <= _SYSTEM_NAME_COL_IDX:
                padded.append("")
            padded[_SYSTEM_NAME_COL_IDX] = system_name
            updated_rows.append(padded)
        parsed["rows"] = updated_rows

        rendered = render_stub(page_num, parsed)
        original = stub_path.read_text(encoding="utf-8")
        if rendered != original:
            stub_path.write_text(rendered, encoding="utf-8")
            updated += 1

    print(f"updated={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"blank_system_pages={','.join(str(p) for p in blank_system_pages) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
