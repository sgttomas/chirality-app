#!/usr/bin/env python3
"""
validate_stub_format.py
Validate that checked v2 per-page stubs are format-safe for downstream QA.

Used by DRAWING_EXTRACT after page-worker batches complete so malformed
SUCCESS stubs are caught before sanitization or assembly can proceed.

Inputs:
    --source-dir SRC
    --drawing-type PFD
    --extraction-target NAME
    --pdf-stem STEM
    --start-page N --end-page M
    [--pages 7-9,12]            optional subset within the declared range

Reads:
    {SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_page_{NNNN}_stub.md

Writes:
    Nothing. Read-only validator.

Exit codes:
    0  format validation OK
    1  one or more checked pages failed validation
    2  setup/argument error
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from normalize_equipment_stub_layout import BASE_COLUMNS, parse_stub, resolve_stub_path


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            pages.update(range(start, end + 1))
        else:
            pages.add(int(token))
    return sorted(pages)


def meaningful_row_count(parsed: dict) -> int:
    base_len = len(BASE_COLUMNS)
    return sum(
        1
        for row in parsed["rows"]
        if len(row) >= base_len and (row[0] or row[1] or row[3])
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that checked v2 per-page stubs are format-safe for downstream QA."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument(
        "--pages",
        help="Optional page subset to validate, e.g. 7-9,12. Must be within the declared range.",
    )
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    pages = list(range(args.start_page, args.end_page + 1))
    if args.pages:
        try:
            pages = parse_pages(args.pages)
        except ValueError as exc:
            print(f"ERROR: invalid --pages spec: {exc}", file=sys.stderr)
            return 2
        out_of_range = [p for p in pages if p < args.start_page or p > args.end_page]
        if out_of_range:
            print(
                "ERROR: --pages entries must fall within "
                f"{args.start_page}-{args.end_page}; got {out_of_range}",
                file=sys.stderr,
            )
            return 2

    failures: list[tuple[int, str]] = []

    for page_num in pages:
        stub_path = resolve_stub_path(
            source_dir,
            args.drawing_type,
            args.extraction_target,
            args.pdf_stem,
            page_num,
        )
        if not stub_path.is_file():
            failures.append((page_num, "stub_missing"))
            continue

        parsed = parse_stub(stub_path, page_num)
        if str(parsed.get("format_version", "")) == "legacy":
            failures.append((page_num, "legacy_stub_at_target_aware_path"))
            continue

        parsed_meaningful = meaningful_row_count(parsed)
        status = str(parsed.get("status", ""))
        finding_count = parsed.get("finding_count")
        if status == "SUCCESS" and finding_count is None:
            failures.append((page_num, "status=SUCCESS but missing finding_count"))
        elif status == "SUCCESS" and parsed_meaningful != finding_count:
            failures.append(
                (page_num, f"row_count_mismatch: finding_count={finding_count} but parsed={parsed_meaningful}")
            )

    if failures:
        for page_num, reason in failures:
            print(f"page {page_num}: {reason}", file=sys.stderr)
        print(f"format_validation_failures={len(failures)}", file=sys.stderr)
        return 1

    print(f"pages_checked={len(pages)}")
    print("format_validation=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
