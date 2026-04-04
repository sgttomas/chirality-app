#!/usr/bin/env python3
"""
prepare_header_crops.py
Create deterministic header/title-region crops from rasterized drawing pages.

This is intended to reduce false positives on drawing sets where the full-page
image contains nearby notes or dense top-of-sheet descriptor text. It also
creates overlapping top-header slices so multiblock header layouts can be
reviewed and extracted without relying on one wide crop alone.

Usage:
    python3 prepare_header_crops.py <work_dir> --pages 7-61
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


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
    parser.add_argument("--pages", required=True, help="Page spec, e.g. 7-61 or 7,9,12")
    parser.add_argument("--header-height-ratio", type=float, default=0.18)
    parser.add_argument("--header-right-exclude-ratio", type=float, default=0.22)
    parser.add_argument("--titleblock-width-ratio", type=float, default=0.22)
    parser.add_argument("--titleblock-height-ratio", type=float, default=0.44)
    parser.add_argument("--header-slices", type=int, default=4, help="Overlapping header slices to write per page.")
    parser.add_argument("--header-slice-overlap-ratio", type=float, default=0.03)
    args = parser.parse_args()

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
                int(width * (1.0 - args.header_right_exclude_ratio)),
                max(1, int(height * args.header_height_ratio)),
            )
            titleblock_box = (
                int(width * (1.0 - args.titleblock_width_ratio)),
                int(height * (1.0 - args.titleblock_height_ratio)),
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

            if args.header_slices > 0:
                slice_width = max(1, round(header_crop.width / args.header_slices))
                overlap = max(0, round(header_crop.width * args.header_slice_overlap_ratio))
                for index in range(args.header_slices):
                    start_x = max(0, index * slice_width - overlap)
                    end_x = min(header_crop.width, (index + 1) * slice_width + overlap)
                    slice_crop = header_crop.crop((start_x, 0, end_x, header_crop.height))
                    slice_out = work_dir / f"page_{page_num:04d}_top_header_slice_{index + 1}.png"
                    slice_crop.save(slice_out)
                    updated += 1

    print(f"crops_written={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
