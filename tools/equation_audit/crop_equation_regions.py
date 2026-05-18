#!/usr/bin/env python3
"""Crop equation regions from page PNGs using per-page bbox JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--work-dir", required=True)
    p.add_argument("--crops-dir", required=True)
    p.add_argument("--padding", type=float, default=0.005)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    work = Path(args.work_dir).resolve()
    crops = Path(args.crops_dir).resolve()
    crops.mkdir(parents=True, exist_ok=True)
    written = 0
    missing = []
    for bbox_json in sorted(work.glob("page_*_eq_bboxes.json")):
        data = json.loads(bbox_json.read_text())
        page = data["page"]
        png = work / f"page_{page:04d}.png"
        if not png.exists():
            missing.append(page)
            continue
        img = Image.open(png)
        W, H = img.size
        for eq in data.get("equations", []):
            x0, y0, x1, y1 = eq["bbox_norm"]
            pad = args.padding
            x0 = max(0.0, x0 - pad); y0 = max(0.0, y0 - pad)
            x1 = min(1.0, x1 + pad); y1 = min(1.0, y1 + pad)
            box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
            crop = img.crop(box)
            out = crops / f"page_{page:04d}_eq_{eq['index']:02d}.png"
            crop.save(out)
            written += 1
    print(f"crops_written={written} missing_pngs={len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
