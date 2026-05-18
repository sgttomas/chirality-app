#!/usr/bin/env python3
"""Render INIT-TASK brief for drawing-titleblock-page."""

from __future__ import annotations

import argparse
from pathlib import Path

from titleblock_stub_layout import render_template_for_brief


def main() -> int:
    ap = argparse.ArgumentParser(description="Build drawing-titleblock-page INIT-TASK brief.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--source-pdf-name", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--page", required=True, type=int)
    ap.add_argument("--total-pages", required=True, type=int)
    ap.add_argument("--output-path", required=True)
    ap.add_argument("--corner-width-ratio", type=float, default=0.25)
    ap.add_argument("--corner-height-ratio", type=float, default=0.25)
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    output_path = Path(args.output_path).resolve()
    page = args.page
    page_s = f"{page:04d}"
    template = render_template_for_brief(args.source_pdf_name, page, args.corner_width_ratio, args.corner_height_ratio)
    lines = [
        f"PURPOSE: Extract drawing sheet titleblock metadata from page {page} of {args.total_pages}",
        "RequestedBy: DRAWING_EXTRACT",
        "ActingSurface: TASK+drawing-titleblock-page",
        "",
        f"ScopePath: {work_dir}",
        "TaskSkill: drawing-titleblock-page",
        "",
        "AllowedWriteTargets:",
        f'  - "{output_path}"',
        "",
        "RuntimeOverrides:",
        f"  SOURCE_PDF_NAME: {args.source_pdf_name}",
        f"  PAGE_NUM: {page}",
        f"  TOTAL_PAGES: {args.total_pages}",
        "  CORNER_CROP_PATHS:",
        f"    tl: {work_dir / f'page_{page_s}_titleblock_tl.png'}",
        f"    tr: {work_dir / f'page_{page_s}_titleblock_tr.png'}",
        f"    bl: {work_dir / f'page_{page_s}_titleblock_bl.png'}",
        f"    br: {work_dir / f'page_{page_s}_titleblock_br.png'}",
        f"  THUMBNAIL_PATH: {work_dir / f'page_{page_s}_thumbnail.png'}",
        f"  OUTPUT_PATH: {output_path}",
        "  CORNER_CROP_GEOMETRY:",
        f"    width_ratio: {args.corner_width_ratio}",
        f"    height_ratio: {args.corner_height_ratio}",
        "",
        "CustomInstructions:",
        "  - Read all four corner crops before deciding titleblock_corner.",
        "  - drawing_family_proposal is a proposal, not final operator scope.",
        "  - Unknown fields are TBD; do not infer from page order.",
        "  - confidence must be high, medium, or low.",
        "",
        "ExpectedOutputs:",
        f"  - {output_path}",
        "",
        "## Dispatch Appendix - Canonical Output Template",
        "",
        "```",
        template.rstrip(),
        "```",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
