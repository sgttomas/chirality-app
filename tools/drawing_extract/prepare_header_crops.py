#!/usr/bin/env python3
"""
prepare_header_crops.py
Create deterministic header/title-region crops from rasterized drawing pages.

This is intended to reduce false positives on drawing sets where the full-page
image contains nearby notes or dense top-of-sheet descriptor text. It also
creates overlapping top-header slices so multiblock header layouts can be
reviewed and extracted without relying on one wide crop alone.

Drawing-type crop-spec registry
-------------------------------
Default crop geometry is dispatched from a drawing-type-keyed registry
(`DRAWING_TYPE_CROP_SPECS`). Only `PFD` is implemented in v1. `P_AND_ID`,
`ISOMETRIC`, and `GA` are registered as stubbed and fail fast with a clear
"registered but not implemented" error. Unknown drawing types also fail
fast. `--drawing-type` is required (no default) so the dispatch decision
is explicit in every invocation.

Per-page crop override workflow
-------------------------------
Default geometry comes from the drawing-type registry. When extraction
fails or under-captures on specific pages (e.g., descriptor band
truncated), operators re-invoke the tool with `--pages N` plus one or
more `--header-*-ratio` / `--titleblock-*-ratio` / `--header-slices` /
`--header-slice-overlap-ratio` CLI overrides to overwrite crops for just
those pages. Other pages are untouched. CLI overrides win over registry
defaults.

Spike evidence (Phase 1 gate, 2026-04-05): West Doe Comp & Liquids page
41 ("T-7100-2 STABILIZER") descriptor band is truncated ~20-30px at the
default `header_height_ratio=0.18`; re-running with
`--header-height-ratio 0.22` for that page restores the missing band.

Usage:
    python3 prepare_header_crops.py <work_dir> --drawing-type PFD --pages 7-61

    # Per-page override (taller header crop for page 41 only):
    python3 prepare_header_crops.py <work_dir> --drawing-type PFD --pages 41 \\
        --header-height-ratio 0.22
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


# ---------------------------------------------------------------------------
# Drawing-type crop-spec registry
# ---------------------------------------------------------------------------

DRAWING_TYPE_CROP_SPECS: dict[str, dict[str, float | int]] = {
    "PFD": {
        "header_height_ratio": 0.18,
        "header_right_exclude_ratio": 0.22,
        "titleblock_width_ratio": 0.22,
        "titleblock_height_ratio": 0.44,
        "header_slices": 4,
        "header_slice_overlap_ratio": 0.03,
    },
    # Stubbed (fail-fast):
    # "P_AND_ID": not implemented
    # "ISOMETRIC": not implemented
    # "GA": not implemented
}

DRAWING_TYPES_STUBBED: frozenset[str] = frozenset({"P_AND_ID", "ISOMETRIC", "GA"})


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create deterministic top-header and titleblock crops.")
    parser.add_argument("work_dir")
    parser.add_argument(
        "--drawing-type",
        required=True,
        help="Drawing type key into the crop-spec registry (e.g. PFD).",
    )
    parser.add_argument("--pages", required=True, help="Page spec, e.g. 7-61 or 7,9,12")
    parser.add_argument("--header-height-ratio", type=float, default=None)
    parser.add_argument("--header-right-exclude-ratio", type=float, default=None)
    parser.add_argument("--titleblock-width-ratio", type=float, default=None)
    parser.add_argument("--titleblock-height-ratio", type=float, default=None)
    parser.add_argument("--header-slices", type=int, default=None, help="Overlapping header slices to write per page.")
    parser.add_argument("--header-slice-overlap-ratio", type=float, default=None)
    args = parser.parse_args()

    drawing_type = args.drawing_type
    known_types = set(DRAWING_TYPE_CROP_SPECS.keys()) | set(DRAWING_TYPES_STUBBED)
    if drawing_type not in known_types:
        valid_sorted = sorted(known_types)
        print(
            f"ERROR: unknown drawing_type '{drawing_type}'; valid: {valid_sorted}",
            file=sys.stderr,
        )
        return 2
    if drawing_type in DRAWING_TYPES_STUBBED:
        print(
            f"ERROR: drawing_type '{drawing_type}' is registered but not implemented; "
            f"see 'How to add a new drawing type' in AGENT_DRAWING_EXTRACT.md",
            file=sys.stderr,
        )
        return 2

    spec = dict(DRAWING_TYPE_CROP_SPECS[drawing_type])
    # CLI overrides win over registry defaults.
    cli_overrides: dict[str, float | int | None] = {
        "header_height_ratio": args.header_height_ratio,
        "header_right_exclude_ratio": args.header_right_exclude_ratio,
        "titleblock_width_ratio": args.titleblock_width_ratio,
        "titleblock_height_ratio": args.titleblock_height_ratio,
        "header_slices": args.header_slices,
        "header_slice_overlap_ratio": args.header_slice_overlap_ratio,
    }
    for key, value in cli_overrides.items():
        if value is not None:
            spec[key] = value

    header_height_ratio = float(spec["header_height_ratio"])
    header_right_exclude_ratio = float(spec["header_right_exclude_ratio"])
    titleblock_width_ratio = float(spec["titleblock_width_ratio"])
    titleblock_height_ratio = float(spec["titleblock_height_ratio"])
    header_slices = int(spec["header_slices"])
    header_slice_overlap_ratio = float(spec["header_slice_overlap_ratio"])

    work_dir = Path(args.work_dir).resolve()
    if not work_dir.is_dir():
        print(f"ERROR: work_dir not found: {work_dir}", file=sys.stderr)
        return 2

    updated = 0
    missing_pages: list[int] = []

    for page_num in parse_pages(args.pages):
        page_path = work_dir / f"page_{page_num:04d}.png"
        if not page_path.is_file():
            missing_pages.append(page_num)
            continue

        with Image.open(page_path) as image:
            width, height = image.size

            header_box = (
                0,
                0,
                int(width * (1.0 - header_right_exclude_ratio)),
                max(1, int(height * header_height_ratio)),
            )
            titleblock_box = (
                int(width * (1.0 - titleblock_width_ratio)),
                int(height * (1.0 - titleblock_height_ratio)),
                width,
                height,
            )

            header_crop = image.crop(header_box)
            titleblock_crop = image.crop(titleblock_box)

            header_out = work_dir / f"page_{page_num:04d}_top_header.png"
            titleblock_out = work_dir / f"page_{page_num:04d}_titleblock.png"
            header_crop.save(header_out)
            titleblock_crop.save(titleblock_out)
            updated += 2

            if header_slices > 0:
                slice_width = max(1, round(header_crop.width / header_slices))
                overlap = max(0, round(header_crop.width * header_slice_overlap_ratio))
                for index in range(header_slices):
                    start_x = max(0, index * slice_width - overlap)
                    end_x = min(header_crop.width, (index + 1) * slice_width + overlap)
                    slice_crop = header_crop.crop((start_x, 0, end_x, header_crop.height))
                    slice_out = work_dir / f"page_{page_num:04d}_top_header_slice_{index + 1}.png"
                    slice_crop.save(slice_out)
                    updated += 1

    print(f"drawing_type={drawing_type}")
    print(f"crops_written={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
