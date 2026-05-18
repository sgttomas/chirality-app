#!/usr/bin/env python3
"""
prepare_titleblock_crops.py
Create four corner titleblock crops plus a full-page thumbnail.

Usage:
    python3 tools/drawing_extract/prepare_titleblock_crops.py WORK_DIR --pages 1-94

Inputs:
    WORK_DIR contains page_NNNN.png files from rasterize_pdf.py.

Outputs:
    page_NNNN_titleblock_tl.png, _tr.png, _bl.png, _br.png
    page_NNNN_thumbnail.png

Exit codes: 0 success, 2 setup error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            pages.update(range(int(start_s), int(end_s) + 1))
        else:
            pages.add(int(token))
    return sorted(pages)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Create titleblock corner crops.")
    ap.add_argument("work_dir")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--corner-width-ratio", type=float, default=0.25)
    ap.add_argument("--corner-height-ratio", type=float, default=0.25)
    ap.add_argument("--thumbnail-width-px", type=int, default=1600)
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    if not work_dir.is_dir():
        print(f"ERROR: work_dir not found: {work_dir}", file=sys.stderr)
        return 2

    crop_manifest: dict[str, object] = {
        "tool": "prepare_titleblock_crops.py",
        "corner_width_ratio": args.corner_width_ratio,
        "corner_height_ratio": args.corner_height_ratio,
        "thumbnail_width_px": args.thumbnail_width_px,
        "pages": {},
    }
    written = 0
    missing: list[int] = []

    for page in parse_pages(args.pages):
        page_path = work_dir / f"page_{page:04d}.png"
        if not page_path.is_file():
            missing.append(page)
            continue
        with Image.open(page_path) as image:
            width, height = image.size
            crop_w = max(1, int(width * args.corner_width_ratio))
            crop_h = max(1, int(height * args.corner_height_ratio))
            boxes = {
                "tl": (0, 0, crop_w, crop_h),
                "tr": (width - crop_w, 0, width, crop_h),
                "bl": (0, height - crop_h, crop_w, height),
                "br": (width - crop_w, height - crop_h, width, height),
            }
            page_entries: dict[str, object] = {
                "source": page_path.name,
                "source_sha256": sha256(page_path),
                "width": width,
                "height": height,
                "corner_crop_geometry": {
                    "width_ratio": args.corner_width_ratio,
                    "height_ratio": args.corner_height_ratio,
                },
                "crops": {},
            }
            for key, box in boxes.items():
                out = work_dir / f"page_{page:04d}_titleblock_{key}.png"
                image.crop(box).save(out)
                page_entries["crops"][key] = {"path": out.name, "box_px": list(box), "sha256": sha256(out)}
                written += 1
            thumb = image.copy()
            if thumb.width > args.thumbnail_width_px:
                ratio = args.thumbnail_width_px / thumb.width
                thumb = thumb.resize((args.thumbnail_width_px, max(1, int(thumb.height * ratio))))
            thumb_out = work_dir / f"page_{page:04d}_thumbnail.png"
            thumb.save(thumb_out)
            page_entries["thumbnail"] = {"path": thumb_out.name, "sha256": sha256(thumb_out)}
            written += 1
            crop_manifest["pages"][str(page)] = page_entries

    (work_dir / "titleblock_crop_manifest.json").write_text(
        json.dumps(crop_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"crops_written={written}")
    print(f"missing_pages={','.join(str(p) for p in missing) or 'none'}")
    print(f"manifest={work_dir / 'titleblock_crop_manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
