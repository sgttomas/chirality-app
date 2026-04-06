#!/usr/bin/env python3
"""
validate_detailed_schema.py
Validate that every v2 per-page stub in a page range shares identical schema
metadata (drawing_type, extraction_target, requested_known_fields,
requested_extra_fields, required_fields).

Used as the core-phase schema-consistency validator (Phase 2.7b) before
combined-CSV assembly. For basic targets the requested_* lists are empty,
but the validator still enforces drawing_type + extraction_target consistency.

Usage:
    python3 validate_detailed_schema.py \
        --source-dir SRC --drawing-type PFD --extraction-target top_equipment_header_detailed \
        --pdf-stem STEM --start-page 7 --end-page 106

Exit codes:
    0 — schema consistent across all parsed stubs
    1 — mismatch or missing stub detected
    2 — setup error
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    build_column_order,
    parse_stub,
    resolve_stub_path,
)


def _normalize_extras(extras) -> tuple[tuple[str, str], ...]:
    """Reduce requested_extra_fields to a hashable normalized form."""
    result: list[tuple[str, str]] = []
    for entry in extras or []:
        if isinstance(entry, dict):
            name = str(entry.get("name", ""))
            description = str(entry.get("description", ""))
        else:
            name = str(entry)
            description = ""
        result.append((name, description))
    return tuple(result)


def _schema_tuple(parsed: dict) -> tuple:
    return (
        str(parsed.get("drawing_type", "") or ""),
        str(parsed.get("extraction_target", "") or ""),
        tuple(str(x) for x in (parsed.get("requested_known_fields") or [])),
        _normalize_extras(parsed.get("requested_extra_fields")),
        tuple(str(x) for x in (parsed.get("required_fields") or [])),
    )


def _format_schema(schema: tuple) -> str:
    drawing_type, extraction_target, known, extras, required = schema
    extras_str = ";".join(f"{n}={d}" for n, d in extras) or "none"
    known_str = ",".join(known) or "none"
    required_str = ",".join(required) or "none"
    return (
        f"drawing_type={drawing_type} extraction_target={extraction_target} "
        f"known=[{known_str}] extras=[{extras_str}] required=[{required_str}]"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate identical schema metadata across v2 per-page stubs."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
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

    reference_schema: tuple | None = None
    reference_page: int | None = None
    mismatches: list[tuple[int, tuple]] = []
    missing_pages: list[int] = []
    pages_checked = 0

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
        schema = _schema_tuple(parsed)
        pages_checked += 1

        if reference_schema is None:
            reference_schema = schema
            reference_page = page_num
            continue

        if schema != reference_schema:
            mismatches.append((page_num, schema))

    if missing_pages:
        print(f"ERROR: missing stubs at pages {','.join(str(p) for p in missing_pages)}", file=sys.stderr)
        # Still print reference for debugging if available.
        if reference_schema is not None:
            print(f"reference_page={reference_page}", file=sys.stderr)
            print(f"reference_schema={_format_schema(reference_schema)}", file=sys.stderr)
        return 1

    if reference_schema is None:
        print("ERROR: no stubs parsed; nothing to validate", file=sys.stderr)
        return 1

    if mismatches:
        print(
            f"ERROR: schema mismatch on {len(mismatches)} page(s) vs reference page {reference_page}",
            file=sys.stderr,
        )
        print(f"reference_page={reference_page}", file=sys.stderr)
        print(f"reference_schema={_format_schema(reference_schema)}", file=sys.stderr)
        for page_num, schema in mismatches:
            print(f"  - page {page_num}: {_format_schema(schema)}", file=sys.stderr)
        return 1

    drawing_type, extraction_target, known, extras, _ = reference_schema
    columns = build_column_order(
        extraction_target,
        list(known),
        [{"name": n, "description": d} for n, d in extras],
    )
    print(f"pages_checked={pages_checked}")
    print("schema_consistent=true")
    print(f"columns={','.join(columns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
