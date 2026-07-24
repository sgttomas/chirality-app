#!/usr/bin/env python3
"""Recover per-equation bboxes by matching crop PNGs back onto page PNGs.

The Phase-1 crop step (`crop_equation_regions.py`) consumes per-page
`page_NNNN_eq_bboxes.json` files that live in a scratch working dir and
are discarded after the crops are written. When only the crops survive,
this tool reconstructs the bbox of every `page_NNNN_eq_NN.png` in
`--crops-dir` by exact template matching against the corresponding
`--pages-dir/page_NNNN.png`, and writes a single `eq_bboxes.json`:

    {"3": [{"index": 1, "bbox_norm": [x0, y0, x1, y1], "score": 0.999}], ...}

Coordinates are normalized to page width/height and include whatever
padding the original crop step applied. Matches score via
TM_CCOEFF_NORMED at 1/4 scale then refine at full resolution; anything
scoring below --min-score is reported and still written (best guess).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

CROP_RE = re.compile(r"^page_(\d{4})_eq_(\d+)\.png$")
COARSE_SCALE = 4


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--crops-dir", required=True)
    p.add_argument("--pages-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--min-score", type=float, default=0.98)
    return p.parse_args()


def _gray(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise IOError(f"unreadable PNG: {path}")
    return img


def match_crop(page: np.ndarray, crop: np.ndarray) -> tuple[int, int, float]:
    """Return (x, y, score) of the best placement of `crop` inside `page`."""
    ph, pw = page.shape
    ch, cw = crop.shape
    if ch > ph or cw > pw:
        return 0, 0, -1.0
    # Coarse pass at 1/4 scale.
    small_page = cv2.resize(page, (max(1, pw // COARSE_SCALE), max(1, ph // COARSE_SCALE)))
    small_crop = cv2.resize(crop, (max(1, cw // COARSE_SCALE), max(1, ch // COARSE_SCALE)))
    res = cv2.matchTemplate(small_page, small_crop, cv2.TM_CCOEFF_NORMED)
    _, _, _, loc = cv2.minMaxLoc(res)
    cx, cy = loc[0] * COARSE_SCALE, loc[1] * COARSE_SCALE
    # Refine at full resolution in a window around the coarse hit.
    margin = 2 * COARSE_SCALE + 4
    x0 = max(0, cx - margin)
    y0 = max(0, cy - margin)
    x1 = min(pw, cx + cw + margin)
    y1 = min(ph, cy + ch + margin)
    window = page[y0:y1, x0:x1]
    if window.shape[0] < ch or window.shape[1] < cw:
        window = page
        x0 = y0 = 0
    res = cv2.matchTemplate(window, crop, cv2.TM_CCOEFF_NORMED)
    _, score, _, loc = cv2.minMaxLoc(res)
    return x0 + loc[0], y0 + loc[1], float(score)


def main() -> int:
    args = parse_args()
    crops_dir = Path(args.crops_dir).resolve()
    pages_dir = Path(args.pages_dir).resolve()
    out_path = Path(args.out).resolve()

    by_page: dict[int, list[Path]] = {}
    for f in sorted(crops_dir.iterdir()):
        m = CROP_RE.match(f.name)
        if m:
            by_page.setdefault(int(m.group(1)), []).append(f)

    result: dict[str, list[dict]] = {}
    low, missing_pages, matched = [], [], 0
    for page_no, crop_files in sorted(by_page.items()):
        page_png = pages_dir / f"page_{page_no:04d}.png"
        if not page_png.exists():
            missing_pages.append(page_no)
            continue
        page = _gray(page_png)
        ph, pw = page.shape
        entries = []
        for f in crop_files:
            idx = int(CROP_RE.match(f.name).group(2))
            crop = _gray(f)
            x, y, score = match_crop(page, crop)
            ch, cw = crop.shape
            bbox = [
                round(x / pw, 6),
                round(y / ph, 6),
                round((x + cw) / pw, 6),
                round((y + ch) / ph, 6),
            ]
            entries.append({"index": idx, "bbox_norm": bbox, "score": round(score, 4)})
            matched += 1
            if score < args.min_score:
                low.append((page_no, idx, score))
        result[str(page_no)] = entries

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")

    print(f"matched={matched} pages={len(result)} low_score={len(low)} "
          f"missing_page_pngs={len(missing_pages)} out={out_path}")
    for page_no, idx, score in low:
        print(f"  LOW page {page_no} eq {idx}: score={score:.4f}", file=sys.stderr)
    for page_no in missing_pages:
        print(f"  MISSING page PNG: page_{page_no:04d}.png", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
