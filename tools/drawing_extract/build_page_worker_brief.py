#!/usr/bin/env python3
"""
build_page_worker_brief.py
Render a valid INIT-TASK brief for a drawing-extract-page dispatch.

Emits the documented INIT-TASK shape (PURPOSE, ScopePath, TaskSkill,
AllowedWriteTargets, RuntimeOverrides, CustomInstructions, ExpectedOutputs)
with format-critical CustomInstructions derived from render_stub().

The orchestrator passes the tool's stdout as the page-worker brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from normalize_equipment_stub_layout import render_stub, build_column_order


def _build_canonical_templates(
    drawing_type: str,
    extraction_target: str,
    source_pdf_name: str,
    page_num: int,
    requested_known_fields: list[str],
    extra_fields: list[dict[str, str]],
    required_fields: list[str],
) -> tuple[str, str]:
    """Generate SUCCESS and NO_FINDINGS templates from render_stub()."""
    columns = build_column_order(extraction_target, requested_known_fields, extra_fields)
    placeholder_row = ["<TAG>", "<NAME>", "<SYSTEM_NAME>", "<DWG_NO>"]
    placeholder_row += ["" for _ in range(len(columns) - 4)]

    success_data = {
        "format_version": "v2",
        "drawing_type": drawing_type,
        "extraction_target": extraction_target,
        "source_pdf": source_pdf_name,
        "source_page": str(page_num),
        "drawing": "<DWG_NO>",
        "system_name": "<SYSTEM_NAME>",
        "status": "SUCCESS",
        "note": "",
        "columns": columns,
        "rows": [placeholder_row],
        "requested_known_fields": requested_known_fields,
        "requested_extra_fields": extra_fields,
        "required_fields": required_fields,
        "extraction_mode": "",
    }
    success_tpl = render_stub(page_num, success_data)

    no_findings_data = dict(success_data)
    no_findings_data["status"] = "NO_FINDINGS"
    no_findings_data["rows"] = [[""] * len(columns)]
    no_findings_data["note"] = "No separated top-of-sheet equipment header was identified."
    no_findings_tpl = render_stub(page_num, no_findings_data)

    return success_tpl, no_findings_tpl


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Render a valid INIT-TASK brief for drawing-extract-page."
    )
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--drawing-type", required=True)
    ap.add_argument("--extraction-target", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--page", required=True, type=int)
    ap.add_argument("--total-pages", required=True, type=int)
    ap.add_argument("--source-pdf-name", required=True)
    ap.add_argument("--requested-known-fields", default="")
    ap.add_argument("--extra-fields-json", default="[]")
    ap.add_argument("--required-fields", default="")
    args = ap.parse_args()

    page = args.page
    work_dir = Path(args.work_dir).resolve()
    source_dir = Path(args.source_dir).resolve()

    rkf = [f.strip() for f in args.requested_known_fields.split(",") if f.strip()]
    extra = json.loads(args.extra_fields_json)
    req = [f.strip() for f in args.required_fields.split(",") if f.strip()]
    is_detailed = args.extraction_target == "top_equipment_header_detailed"

    page_str = f"{page:04d}"
    image_path = work_dir / f"page_{page_str}.png"
    header_path = work_dir / f"page_{page_str}_top_header.png"
    titleblock_path = work_dir / f"page_{page_str}_titleblock.png"
    slice_paths = sorted(work_dir.glob(f"page_{page_str}_top_header_slice_*.png"))
    output_path = (
        source_dir / args.drawing_type / args.extraction_target
        / f"{args.pdf_stem}_page_{page_str}_stub.md"
    )

    success_tpl, no_findings_tpl = _build_canonical_templates(
        args.drawing_type, args.extraction_target, args.source_pdf_name,
        page, rkf, extra, req,
    )

    # --- Emit INIT-TASK brief ---
    lines = [
        f"PURPOSE: Extract top-of-sheet equipment header from drawing page {page} of {args.total_pages}",
        "RequestedBy: DRAWING_EXTRACT",
        "ActingSurface: TASK+drawing-extract-page",
        "",
        f"ScopePath: {work_dir}",
        "TaskSkill: drawing-extract-page",
        "",
        "AllowedWriteTargets:",
        f'  - "{output_path}"',
        "",
        "RuntimeOverrides:",
        f"  IMAGE_PATH: {image_path}",
        f"  HEADER_IMAGE_PATH: {header_path}",
        f"  TITLEBLOCK_IMAGE_PATH: {titleblock_path}",
    ]
    if slice_paths:
        lines.append("  HEADER_SLICE_PATHS:")
        for sp in slice_paths:
            lines.append(f"    - {sp}")
    lines += [
        f"  OUTPUT_PATH: {output_path}",
        f"  PAGE_NUM: {page}",
        f"  TOTAL_PAGES: {args.total_pages}",
        f"  DRAWING_TYPE: {args.drawing_type}",
        f"  EXTRACTION_TARGET: {args.extraction_target}",
    ]
    if is_detailed:
        if rkf:
            lines.append("  REQUESTED_KNOWN_FIELDS:")
            for f in rkf:
                lines.append(f"    - {f}")
        else:
            lines.append("  REQUESTED_KNOWN_FIELDS: []")
        if extra:
            lines.append("  EXTRA_FIELDS:")
            for entry in extra:
                lines.append(f"    - name: {entry['name']}")
                lines.append(f"      description: {entry['description']}")
        else:
            lines.append("  EXTRA_FIELDS: []")
        if req:
            lines.append("  REQUIRED_FIELDS:")
            for f in req:
                lines.append(f"    - {f}")
        else:
            lines.append("  REQUIRED_FIELDS: []")
    lines.append(f"  SOURCE_PDF_NAME: {args.source_pdf_name}")

    # CustomInstructions: format reminders + canonical templates
    lines += [
        "",
        "CustomInstructions:",
        "  - YAML lists use block style for multi-element lists; empty lists use inline [].",
        "  - Table separator MUST be spaced: | --- | --- | ... |",
        "  - status MUST be exactly SUCCESS, NO_FINDINGS, FAILED, or FAILED_INPUTS.",
        "  - finding_count MUST equal the number of meaningful equipment rows.",
        "  - Data rows MUST match the column count of the header.",
        "  - Detail fields from crops only. Not visible = blank. Do not invent.",
        "  - No instrument tags (PSV, PCV, FIC, etc.) in findings.",
        "",
    ]

    # Append canonical templates as a dispatch appendix
    lines += [
        "## Dispatch Appendix — Canonical Output Templates",
        "",
        "### SUCCESS",
        "",
        "```",
    ]
    lines += success_tpl.strip().splitlines()
    lines += [
        "```",
        "",
        "### NO_FINDINGS",
        "",
        "```",
    ]
    lines += no_findings_tpl.strip().splitlines()
    lines += [
        "```",
        "",
        "ExpectedOutputs:",
        f"  - {output_path}",
        "",
    ]

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
