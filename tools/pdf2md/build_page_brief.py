#!/usr/bin/env python3
"""
build_page_brief.py
Render an INIT-TASK brief for one pdf2md-page dispatch.

Usage:
    python3 build_page_brief.py --work-dir WORK_DIR --page 3 --total-pages 42

Inputs:
    --work-dir       PDF2MD work directory containing page rasters
    --page           1-indexed page number
    --total-pages    total page count from manifest.json
    --output-md      optional per-page Markdown output path
                     (default: WORK_DIR/page_NNNN.md)

Outputs:
    INIT-TASK brief on stdout. The brief is consumed by TASK with
    TaskSkill: pdf2md-page.

Example:
    python3 tools/pdf2md/build_page_brief.py \\
        --work-dir ./MWK_1956_pdf2md_work --page 3 --total-pages 386
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--work-dir", required=True, help="PDF2MD work directory")
    p.add_argument("--page", required=True, type=int, help="1-indexed page number")
    p.add_argument("--total-pages", required=True, type=int, help="Total page count")
    p.add_argument("--output-md", help="Per-page Markdown output path")
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
        print(f"ERROR: output parent directory does not exist: {output_md.parent}", file=sys.stderr)
        return 2

    brief = f"""PURPOSE: Convert one PDF page image to raw Markdown via multimodal vision
RequestedBy: PDF2MD
ActingSurface: TASK+pdf2md-page

ScopePath: {work_dir}
TaskSkill: pdf2md-page

Tasks:
  - Read the page image and transcribe its contents to Markdown per the 8 conversion rules in skills/pdf2md-page/SKILL.md

ApplyEdits: true

AllowedWriteTargets:
  - "{output_md}"

RuntimeOverrides:
  IMAGE_PATH: {image_path}
  OUTPUT_PATH: {output_md}
  PAGE_NUM: {args.page}
  TOTAL_PAGES: {args.total_pages}

ExpectedOutputs:
  - {output_md}
"""
    print(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
