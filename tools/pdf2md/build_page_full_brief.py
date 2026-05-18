#!/usr/bin/env python3
"""
build_page_full_brief.py
Render an INIT-TASK brief for one pdf2md-page-full dispatch.

The merged skill produces BOTH the per-page Markdown and the per-page asset
JSON from a single vision read of the page image, replacing the prior
two-skill split (pdf2md-page + pdf2md-page-assets).

Usage:
    python3 build_page_full_brief.py --work-dir WORK_DIR --doc-stem DOC \\
        --page 3 --total-pages 42

Inputs:
    --work-dir       PDF2MD work directory containing page rasters
    --doc-stem       Document stem used for stable asset IDs
    --page           1-indexed page number
    --total-pages    Total page count from manifest.json
    --output-md      Optional per-page Markdown output path
                     (default: WORK_DIR/page_NNNN.md)
    --output-json    Optional per-page asset JSON output path
                     (default: WORK_DIR/page_NNNN_assets.json)
    --asset-policy   Asset extraction policy label
                     (default: prose-document-assets-v1)

Outputs:
    INIT-TASK brief on stdout. The brief is consumed by TASK with
    TaskSkill: pdf2md-page-full.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a pdf2md-page-full INIT-TASK brief.")
    p.add_argument("--work-dir", required=True, help="PDF2MD work directory")
    p.add_argument("--doc-stem", required=True, help="Document stem for stable asset IDs")
    p.add_argument("--page", required=True, type=int, help="1-indexed page number")
    p.add_argument("--total-pages", required=True, type=int, help="Total page count")
    p.add_argument("--output-md", help="Per-page Markdown output path")
    p.add_argument("--output-json", help="Per-page asset JSON output path")
    p.add_argument(
        "--asset-policy",
        default="prose-document-assets-v1",
        help="Asset extraction policy label",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.page < 1:
        print("ERROR: --page must be >= 1", file=sys.stderr)
        return 2
    if args.total_pages < args.page:
        print("ERROR: --total-pages must be >= --page", file=sys.stderr)
        return 2

    work_dir = Path(args.work_dir).resolve()
    image_path = work_dir / f"page_{args.page:04d}.png"
    output_md = (
        Path(args.output_md).resolve()
        if args.output_md
        else work_dir / f"page_{args.page:04d}.md"
    )
    output_json = (
        Path(args.output_json).resolve()
        if args.output_json
        else work_dir / f"page_{args.page:04d}_assets.json"
    )

    if not work_dir.is_dir():
        print(f"ERROR: --work-dir is not a directory: {work_dir}", file=sys.stderr)
        return 2
    if not image_path.is_file():
        print(f"ERROR: page image not found: {image_path}", file=sys.stderr)
        return 2
    if image_path.suffix.lower() != ".png":
        print(f"ERROR: page image must be a .png file: {image_path}", file=sys.stderr)
        return 2
    if not output_md.parent.is_dir():
        print(f"ERROR: output-md parent not found: {output_md.parent}", file=sys.stderr)
        return 2
    if not output_json.parent.is_dir():
        print(f"ERROR: output-json parent not found: {output_json.parent}", file=sys.stderr)
        return 2

    brief = f"""PURPOSE: Convert one PDF page image to BOTH raw Markdown AND asset JSON from a single multimodal vision read
RequestedBy: PDF2MD
ActingSurface: TASK+pdf2md-page-full

ScopePath: {work_dir}
TaskSkill: pdf2md-page-full

Tasks:
  - Read the page image ONCE via multimodal vision
  - Transcribe its contents to Markdown per the 8 conversion rules in skills/pdf2md-page-full/SKILL.md (including [FIGURE:]/[TABLE:]/[... logo] placeholders in reading order)
  - Identify visible figures, tables, and meaningful images; emit the strict-schema asset JSON (pdf2md-page-assets/v1) with bbox_norm, table_data for legible tables, and one-to-one correspondence with the Markdown placeholders

ApplyEdits: true

AllowedWriteTargets:
  - "{output_md}"
  - "{output_json}"

RuntimeOverrides:
  IMAGE_PATH: {image_path}
  OUTPUT_MD_PATH: {output_md}
  OUTPUT_JSON_PATH: {output_json}
  DOC_STEM: {args.doc_stem}
  PAGE_NUM: {args.page}
  TOTAL_PAGES: {args.total_pages}
  ASSET_POLICY: {args.asset_policy}

CustomInstructions:
  - SINGLE VISION READ: read IMAGE_PATH exactly once and produce both outputs from that one pass. Do not re-read.
  - The Markdown output (OUTPUT_MD_PATH) follows the legacy pdf2md-page contract exactly: 8 rules, raw Markdown only, no fences/commentary, asset placeholders in reading order.
  - The JSON output (OUTPUT_JSON_PATH) follows the legacy pdf2md-page-assets/v1 schema exactly. Use these EXACT field names and literal string values; do not substitute synonyms or restructure:
    * Top-level fields: schema_version, run_status, doc_stem, page (NOT page_num), total_pages, asset_policy, assets, issues.
    * schema_version MUST be the literal "pdf2md-page-assets/v1".
    * run_status MUST be one of: SUCCESS, NO_ASSETS, FAILED, FAILED_INPUTS (uppercase).
    * assets is a flat array; tables are entries with kind="tbl", NOT a sibling array.
    * Per-asset kind MUST be one of three 3-letter literals: "fig", "tbl", "img".
    * Per-asset bbox_norm MUST be a 4-element JSON array [x0, y0, x1, y1], NOT an object.
    * Captions go in "caption" (NOT "label", "title", "name").
    * For kind="tbl": emit a structured "table_data" object conforming to pdf2md-table/v1 (see skills/pdf2md-page-assets/SKILL.md for the schema, row/cell shape, cell types, footnotes, and worked example). If a table is visible but cannot be safely transcribed, OMIT table_data and set "needs_extraction": true plus an issue.
    * Do NOT emit the legacy "csv_text" field anywhere.
  - bbox_norm MUST generously include the full asset, the visible caption, AND ~3-5% of surrounding page whitespace.
  - A/B CONSISTENCY: every [FIGURE:]/[TABLE:]/[... logo|emblem|seal|cover|photograph|photo|image] placeholder in the Markdown must have a corresponding entry in the JSON, in the same reading order, and vice versa.

ExpectedOutputs:
  - {output_md}
  - {output_json}
"""
    print(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
