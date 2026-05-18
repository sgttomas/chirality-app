#!/usr/bin/env python3
"""Render INIT-TASK brief for P&ID valve symbol-instance extraction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from valve_stub_layout import render_template_for_brief


def main() -> int:
    ap = argparse.ArgumentParser(description="Build pandid-valve-symbol-instance INIT-TASK brief.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--source-pdf-name", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--page", required=True, type=int)
    ap.add_argument("--tile-id", required=True)
    ap.add_argument("--mode", required=True, choices=["basic", "detailed"])
    ap.add_argument("--output-path", required=True)
    ap.add_argument("--allow-reference-sheets", action="store_true")
    ap.add_argument("--scope-file", default="")
    ap.add_argument("--basic-reference-run", default="")
    ap.add_argument("--basic-counts-csv", default="")
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    output_path = Path(args.output_path).resolve()
    manifest_path = work_dir / "tile_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    tile = next((entry for entry in manifest.get("tiles", []) if entry.get("tile_id") == args.tile_id), None)
    if not tile:
        raise SystemExit(f"tile_id not found in manifest: {args.tile_id}")
    tile_image_path = work_dir / tile["image_path"]
    source_raster_path = work_dir / f"page_{args.page:04d}.png"
    template = render_template_for_brief(
        {
            "source_pdf": args.source_pdf_name,
            "source_page": args.page,
            "source_raster_path": source_raster_path,
            "tile_id": args.tile_id,
            "tile_image_path": tile_image_path,
            "tile_grid": tile["tile_grid"],
            "body_box_px": tile["body_box_px"],
            "body_exclusions": tile["body_exclusions"],
            "read_box_px": tile["read_box_px"],
            "emit_box_px": tile["emit_box_px"],
            "overlap_px": tile["overlap_px"],
            "mini_grid": tile["mini_grid"],
        },
        args.mode,
    )
    lines = [
        f"PURPOSE: Extract pixel-anchored P&ID valve symbol instances from page {args.page} tile {args.tile_id}",
        "RequestedBy: DRAWING_EXTRACT",
        "ActingSurface: TASK+pandid-valve-symbol-instance",
        "",
        f"ScopePath: {work_dir}",
        "TaskSkill: pandid-valve-symbol-instance",
        "",
        "AllowedWriteTargets:",
        f'  - "{output_path}"',
        "",
        "RuntimeOverrides:",
        f"  SOURCE_PDF_NAME: {args.source_pdf_name}",
        f"  PAGE_NUM: {args.page}",
        f"  TILE_ID: {args.tile_id}",
        f"  SOURCE_RASTER_PATH: {source_raster_path}",
        f"  TILE_IMAGE_PATH: {tile_image_path}",
        f"  OUTPUT_PATH: {output_path}",
        f"  MODE: {args.mode}",
        f"  ALLOW_REFERENCE_SHEETS: {'true' if args.allow_reference_sheets else 'false'}",
        "  TILE_GEOMETRY:",
        f"    tile_grid: {tile['tile_grid']}",
        f"    body_box_px: {tile['body_box_px']}",
        f"    body_exclusions: {tile['body_exclusions']}",
        f"    read_box_px: {tile['read_box_px']}",
        f"    emit_box_px: {tile['emit_box_px']}",
        f"    overlap_px: {tile['overlap_px']}",
        f"    mini_grid: {tile['mini_grid']}",
    ]
    if args.scope_file:
        lines.append(f"  SCOPE_FILE: {args.scope_file}")
    if args.basic_reference_run:
        lines.append(f"  BASIC_REFERENCE_RUN: {args.basic_reference_run}")
    if args.basic_counts_csv:
        lines.append(f"  BASIC_COUNTS_CSV: {args.basic_counts_csv}")
    lines += [
        "",
        "CustomInstructions:",
        "  - Critical guardrail: emit a row only for an isolated symbol crop classified as a valve class.",
        "  - Text never produces rows. Line/spec/service text may only populate nearby_line_text after a valve symbol exists.",
        "  - Tag profiles never delete rows and never decide countability.",
        "  - Use the whole tile image for detection context, then classify each candidate from a tight symbol crop.",
        "  - The classifier crop must exclude surrounding line/spec/tag text as much as practical.",
        "  - Emit rows only for valve symbols whose page-global visual center is inside the tile emit box.",
        "  - Visible-but-outside candidates go in notes only, never as rows.",
        "  - Emit page-global integer pixel coordinates for center_x_px/center_y_px and bbox_*.",
        "  - count_include=true is allowed only for valve symbol_class values at medium or high symbol_confidence.",
        "  - Put probable line/spec labels such as 27GA-A or 60BA-S in nearby_line_text with tag_status=line_spec_only or ambiguous.",
        "  - Do not put line/spec/service text in visible_tag_text as a true tag.",
        "  - issue_flags is [] or [FLAG_A, FLAG_B]. Include TAG_PROFILE_REVIEW only as a review signal.",
        "  - Unknown fields are TBD.",
        "  - Reference/legend pages return NO_FINDINGS_REFERENCE unless ALLOW_REFERENCE_SHEETS=true.",
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
