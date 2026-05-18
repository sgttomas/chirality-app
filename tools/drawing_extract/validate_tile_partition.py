#!/usr/bin/env python3
"""
validate_tile_partition.py
Validate P&ID tile geometry invariants.

Usage:
    python3 tools/drawing_extract/validate_tile_partition.py --tile-manifest WORK_DIR/tile_manifest.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def area(box: list[int]) -> int:
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def overlap(a: list[int], b: list[int]) -> int:
    x0 = max(a[0], b[0])
    y0 = max(a[1], b[1])
    x1 = min(a[2], b[2])
    y1 = min(a[3], b[3])
    return max(0, x1 - x0) * max(0, y1 - y0)


def contains(outer: list[int], inner: list[int]) -> bool:
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate P&ID tile partition invariants.")
    ap.add_argument("--tile-manifest", required=True)
    args = ap.parse_args()

    path = Path(args.tile_manifest).resolve()
    if not path.is_file():
        print(f"ERROR: tile manifest not found: {path}", file=sys.stderr)
        return 2
    manifest = json.loads(path.read_text(encoding="utf-8"))
    failures: list[str] = []

    by_page: dict[str, list[dict]] = {}
    for entry in manifest.get("tiles", []):
        by_page.setdefault(str(entry["source_page"]), []).append(entry)

    for page, entries in sorted(by_page.items(), key=lambda item: int(item[0])):
        if not entries:
            continue
        body_box = entries[0]["body_box_px"]
        total_emit_area = sum(area(e["emit_box_px"]) for e in entries)
        if total_emit_area != area(body_box):
            failures.append(f"page {page}: emit area {total_emit_area} != body area {area(body_box)}")
        for idx, first in enumerate(entries):
            if not contains(first["read_box_px"], first["emit_box_px"]):
                failures.append(f"page {page} {first['tile_id']}: read_box does not contain emit_box")
            for second in entries[idx + 1 :]:
                ov = overlap(first["emit_box_px"], second["emit_box_px"])
                if ov:
                    failures.append(f"page {page}: emit boxes overlap {first['tile_id']} {second['tile_id']} area={ov}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"pages_checked={len(by_page)}")
    print("tile_partition=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
