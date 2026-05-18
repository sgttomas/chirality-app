#!/usr/bin/env python3
"""
Render a valid INIT-TASK brief for one `equation-bbox-detect` dispatch.

Called once per page that contains display equations the persona wants to
crop. The skill reads the page raster and the per-page Markdown (so it knows
which equations to look for), then emits `page_NNNN_eq_bboxes.json` matching
the schema `crop_equation_regions.py` consumes:

    {"page": <int>,
     "equations": [
        {"index": <int>, "bbox_norm": [x0, y0, x1, y1],
         "latex_excerpt": "<first ~20 chars>"},
        ...]}

Inputs:
  --image-path     Path to page_NNNN.png
  --page-md-path   Path to the per-page Markdown
  --page-num       Page number (1-based, matches the NNNN in image_path)
  --output-path    Where the skill writes page_NNNN_eq_bboxes.json
  --expected-equation-hashes
                   Optional comma-separated list of 12-hex hashes the persona
                   expects to find on this page (for cross-check)

Output (stdout): INIT-TASK brief.

Exit codes:
  0  brief rendered to stdout
  2  inputs invalid
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--image-path", required=True)
    p.add_argument("--page-md-path", required=True)
    p.add_argument("--page-num", required=True, type=int)
    p.add_argument("--output-path", required=True)
    p.add_argument("--expected-equation-hashes", default="",
                   help="Optional comma-separated 12-hex hashes for cross-check")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    image_path = Path(args.image_path).resolve()
    page_md = Path(args.page_md_path).resolve()
    output_path = Path(args.output_path).resolve()

    if not image_path.exists():
        print(f"ERROR: image not found: {image_path}", file=sys.stderr)
        return 2
    if not page_md.exists():
        print(f"ERROR: page Markdown not found: {page_md}", file=sys.stderr)
        return 2

    expected = [h.strip() for h in args.expected_equation_hashes.split(",") if h.strip()]

    lines = [
        f"PURPOSE: Detect display-equation bounding boxes on page {args.page_num} and emit normalized coordinates for downstream cropping",
        "RequestedBy: EQUATION_AUDIT",
        "ActingSurface: TASK+equation-bbox-detect",
        "",
        f"ScopePath: {image_path.parent}",
        "TaskSkill: equation-bbox-detect",
        "",
        "AllowedWriteTargets:",
        f'  - "{output_path}"',
        "",
        "RuntimeOverrides:",
        f"  IMAGE_PATH: {image_path}",
        f"  PAGE_MD_PATH: {page_md}",
        f"  PAGE_NUM: {args.page_num}",
        f"  OUTPUT_PATH: {output_path}",
    ]
    if expected:
        lines.append("  EXPECTED_EQUATION_HASHES:")
        for h in expected:
            lines.append(f"    - {h}")
    else:
        lines.append("  EXPECTED_EQUATION_HASHES: []")

    lines += [
        "",
        "CustomInstructions:",
        "  - Identify each DISPLAY equation visible on the page raster (block-level math, typically set off from running prose).",
        "  - Do NOT box inline equations or symbols inside running text.",
        "  - Emit normalized coordinates [x0,y0,x1,y1] in [0,1] relative to the page raster's width/height.",
        "  - Boxes should tightly enclose the display equation without including the surrounding paragraph text.",
        "  - The 'index' field is 1-based, ordered top-to-bottom on the page.",
        "  - Include a 'latex_excerpt' field with the first ~20 characters of the visible LaTeX/symbolic content for cross-check against expected hashes.",
        "  - If a page has no display equations, write {\"page\": <num>, \"equations\": []} and return RUN_STATUS=NO_FINDINGS.",
        "",
        "ExpectedOutputs:",
        f"  - {output_path}",
        "",
    ]

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
