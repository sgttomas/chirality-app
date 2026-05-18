#!/usr/bin/env python3
"""
validate_resume_stub_metadata.py
Validate that every existing v2 per-page stub in a target-aware subtree
matches the current run's schema tuple. Fail-fast on any mismatch.

Used by DRAWING_EXTRACT Phase 2 (resume-safety validation) before dispatching
page workers. Prevents silent reuse of stubs written under a different
drawing_type, extraction_target, source_pdf, source_page, or requested-field
tuple.

Inputs (current-run tuple):
    --source-dir SRC                 base SOURCE_DIR
    --drawing-type PFD               e.g. PFD
    --extraction-target NAME         e.g. top_equipment_header_basic
    --pdf-stem STEM                  PDF filename without extension
    --source-pdf PDF_BASENAME        PDF filename with extension
    --start-page N --end-page M      inclusive page range
    --requested-known-fields a,b,c   comma-separated catalog names (detailed only; default empty)
    --extra-fields-json '[...]'      JSON array of {"name","description"} (detailed only; default "[]")
    --required-fields x,y            comma-separated required subset (detailed only; default empty)

Reads:
    {SOURCE_DIR}/{DRAWING_TYPE}/{EXTRACTION_TARGET}/{PDF_STEM}_page_{NNNN}_stub.md
    for each page in [start_page, end_page] that exists. Missing pages are
    skipped (Phase 2 will queue them for extraction).

Writes:
    Nothing. Read-only validator.

Exit codes:
    0  resume-safety OK; all existing stubs match the current-run tuple
    1  one or more stubs mismatch the current-run tuple
    2  setup/argument error

Stdout on success (key=value per repo convention):
    stubs_checked=<N>
    resume_safety=OK

Stderr on failure: per-stub mismatch listing + remediation options.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from normalize_equipment_stub_layout import parse_stub, resolve_stub_path


def _normalize_extras(extras) -> list[tuple[str, str]]:
    """Reduce requested_extra_fields to a list of (name, description) tuples."""
    result: list[tuple[str, str]] = []
    for entry in extras or []:
        if isinstance(entry, dict):
            name = str(entry.get("name", ""))
            description = str(entry.get("description", ""))
        else:
            name = str(entry)
            description = ""
        result.append((name, description))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that existing v2 per-page stubs match the current-run schema tuple."
    )
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--source-pdf", required=True, help="PDF filename with extension")
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument(
        "--requested-known-fields",
        default="",
        help="Comma-separated catalog field names (detailed only; default empty)",
    )
    parser.add_argument(
        "--extra-fields-json",
        default="[]",
        help='JSON array of {"name": ..., "description": ...} pairs (detailed only; default "[]")',
    )
    parser.add_argument(
        "--required-fields",
        default="",
        help="Comma-separated required field names (detailed only; default empty)",
    )
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    requested_known = [x.strip() for x in args.requested_known_fields.split(",") if x.strip()]
    try:
        extras_raw = json.loads(args.extra_fields_json)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --extra-fields-json is not valid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(extras_raw, list):
        print("ERROR: --extra-fields-json must be a JSON array", file=sys.stderr)
        return 2
    want_extras = _normalize_extras(extras_raw)
    required_fields = [x.strip() for x in args.required_fields.split(",") if x.strip()]

    detailed = args.extraction_target == "top_equipment_header_detailed"

    mismatches: list[tuple[Path, list[tuple[str, object, object]]]] = []
    checked = 0

    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = resolve_stub_path(
            source_dir,
            args.drawing_type,
            args.extraction_target,
            args.pdf_stem,
            page_num,
        )
        if not stub_path.is_file():
            continue
        checked += 1
        fm = parse_stub(stub_path, page_num)
        problems: list[tuple[str, object, object]] = []

        if str(fm.get("format_version", "")) == "legacy":
            problems.append(("format_version", "legacy", "v2 (stub at target-aware path must be v2 format)"))

        if str(fm.get("drawing_type", "")) != args.drawing_type:
            problems.append(("drawing_type", fm.get("drawing_type"), args.drawing_type))
        if str(fm.get("extraction_target", "")) != args.extraction_target:
            problems.append(
                ("extraction_target", fm.get("extraction_target"), args.extraction_target)
            )
        if str(fm.get("source_pdf", "")) != args.source_pdf:
            problems.append(("source_pdf", fm.get("source_pdf"), args.source_pdf))
        try:
            stub_page = int(fm.get("source_page", 0) or 0)
        except (TypeError, ValueError):
            stub_page = 0
        if stub_page != page_num:
            problems.append(("source_page", fm.get("source_page"), page_num))

        if detailed:
            got_known = [str(x) for x in (fm.get("requested_known_fields") or [])]
            if got_known != requested_known:
                problems.append(("requested_known_fields", got_known, requested_known))
            got_extras = _normalize_extras(fm.get("requested_extra_fields"))
            if got_extras != want_extras:
                problems.append(("requested_extra_fields", got_extras, want_extras))
            got_required = [str(x) for x in (fm.get("required_fields") or [])]
            if got_required != required_fields:
                problems.append(("required_fields", got_required, required_fields))

        if problems:
            mismatches.append((stub_path, problems))

    if mismatches:
        print(
            f"ERROR: resume-safety mismatch on {len(mismatches)} stub(s)",
            file=sys.stderr,
        )
        for stub_path, probs in mismatches[:20]:
            print(f"  - {stub_path}", file=sys.stderr)
            for field, got, want in probs:
                print(f"      {field}: got={got!r} want={want!r}", file=sys.stderr)
        if len(mismatches) > 20:
            print(f"  ... plus {len(mismatches) - 20} more", file=sys.stderr)
        print(
            "Remediation: (1) clear stubs in target subdirectory, "
            "(2) dispatch to a new SOURCE_DIR, or "
            "(3) rerun with matching parameters",
            file=sys.stderr,
        )
        return 1

    print(f"stubs_checked={checked}")
    print("resume_safety=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
