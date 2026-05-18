#!/usr/bin/env python3
"""
build_page_assets_brief.py
Render an INIT-TASK brief for one pdf2md-page-assets dispatch.

Usage:
    python3 build_page_assets_brief.py --work-dir WORK_DIR --doc-stem DOC --page 3 --total-pages 42

Inputs:
    --work-dir       PDF2MD work directory containing page rasters and page Markdown
    --doc-stem       PDF/document stem used for stable asset IDs
    --page           1-indexed page number
    --total-pages    total page count from manifest.json
    --page-md        optional page Markdown path (default: WORK_DIR/page_NNNN.md)
    --output-json    optional asset JSON path (default: WORK_DIR/page_NNNN_assets.json)
    --asset-policy   extraction policy label (default: prose-document-assets-v1)

Outputs:
    INIT-TASK brief on stdout. The brief is consumed by TASK with
    TaskSkill: pdf2md-page-assets.

Example:
    python3 tools/pdf2md/build_page_assets_brief.py \
      --work-dir ./MWK_1956_pdf2md_work --doc-stem MWK_1956 --page 3 --total-pages 386
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a pdf2md-page-assets INIT-TASK brief.")
    parser.add_argument("--work-dir", required=True, help="PDF2MD work directory")
    parser.add_argument("--doc-stem", required=True, help="Document stem for stable asset IDs")
    parser.add_argument("--page", required=True, type=int, help="1-indexed page number")
    parser.add_argument("--total-pages", required=True, type=int, help="Total page count")
    parser.add_argument("--page-md", help="Clean per-page Markdown path")
    parser.add_argument("--output-json", help="Per-page asset JSON output path")
    parser.add_argument("--asset-policy", default="prose-document-assets-v1", help="Asset extraction policy label")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.page < 1:
        raise SystemExit("ERROR: --page must be >= 1")
    if args.total_pages < args.page:
        raise SystemExit("ERROR: --total-pages must be >= --page")

    work_dir = Path(args.work_dir).resolve()
    image_path = work_dir / f"page_{args.page:04d}.png"
    page_md = Path(args.page_md).resolve() if args.page_md else work_dir / f"page_{args.page:04d}.md"
    output_json = Path(args.output_json).resolve() if args.output_json else work_dir / f"page_{args.page:04d}_assets.json"

    if not work_dir.is_dir():
        raise SystemExit(f"ERROR: --work-dir is not a directory: {work_dir}")
    if not image_path.is_file():
        raise SystemExit(f"ERROR: page image not found: {image_path}")
    if image_path.suffix.lower() != ".png":
        raise SystemExit(f"ERROR: page image must be a .png file: {image_path}")
    if not page_md.is_file():
        raise SystemExit(f"ERROR: page Markdown not found: {page_md}")
    if page_md.suffix.lower() != ".md":
        raise SystemExit(f"ERROR: page Markdown must be a .md file: {page_md}")
    if not output_json.parent.is_dir():
        raise SystemExit(f"ERROR: output parent directory does not exist: {output_json.parent}")

    brief = f"""PURPOSE: Identify extractable prose-document assets on one PDF page
RequestedBy: PDF2MD

ScopePath: {work_dir}
TaskSkill: pdf2md-page-assets

Tasks:
  - Read one page raster and its clean Markdown context
  - Identify visible figures, tables, and other meaningful images
  - Emit bbox-normalized asset candidates and, for tables, a structured
    `table_data` block (pdf2md-table/v1) per the skill contract

ApplyEdits: true

AllowedWriteTargets:
  - "{output_json}"

RuntimeOverrides:
  IMAGE_PATH: {image_path}
  PAGE_MD_PATH: {page_md}
  OUTPUT_PATH: {output_json}
  DOC_STEM: {args.doc_stem}
  PAGE_NUM: {args.page}
  TOTAL_PAGES: {args.total_pages}
  ASSET_POLICY: {args.asset_policy}

CustomInstructions:
  - The output JSON contract is strict. Use these EXACT field names and string literals;
    do not substitute synonyms or restructure:
    * Top-level fields: schema_version, run_status, doc_stem, page, total_pages,
      asset_policy, assets, issues. The page-number field is page (NOT page_num).
    * schema_version MUST be the literal "pdf2md-page-assets/v1".
    * run_status MUST be one of the four uppercase literals: SUCCESS, NO_ASSETS, FAILED,
      FAILED_INPUTS. Do not use lowercase "ok" or any other value.
    * assets is a flat array. Do NOT add a sibling tables/figures/images array; tables
      are entries inside assets with kind="tbl".
    * Per-asset kind MUST be one of three 3-letter literals: "fig", "tbl", "img". Do NOT
      use "figure", "image", "table", "diagram", "plot", "chart", "logo", "photo", etc.
    * Per-asset bbox_norm MUST be a 4-element JSON array [x0, y0, x1, y1]. Do NOT emit
      an object {{"x0": ..., "y0": ..., "x1": ..., "y1": ...}}.
    * Captions go in the "caption" field (NOT "label", "title", or "name").
    * For kind="tbl" entries: do NOT emit the legacy "csv_text" field. The canonical
      table representation is a structured "table_data" object conforming to
      "pdf2md-table/v1" — see skills/pdf2md-page-assets/SKILL.md for the schema,
      field rules, and worked example (rows/cells with row_span/col_span/is_header,
      cell `type` of text|number|fraction|missing|formula|boolean, optional `unit`
      and `raw`, table-level `header_rows`, `section_dividers`, `footnotes`,
      `continuation_of`). If a table is visible but cannot be safely transcribed,
      OMIT `table_data` and set `needs_extraction: true` plus an issue.
  - bbox_norm MUST generously include the full asset, the visible caption, AND ~3-5% of
    surrounding page whitespace. Clipped figures or truncated captions are defects; a
    little extra whitespace around the asset is preferable.

ExpectedOutputs:
  - {output_json}
"""
    print(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
