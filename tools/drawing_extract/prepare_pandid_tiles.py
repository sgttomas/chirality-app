#!/usr/bin/env python3
"""
prepare_pandid_tiles.py
Prepare P&ID read-zone tiles with emit-zone overlays.

Usage:
    python3 tools/drawing_extract/prepare_pandid_tiles.py WORK_DIR --pages 11-12

Writes page_NNNN_tile_rRR_cCC.png, per-page manifests, and tile_manifest.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


def parse_grid(spec: str) -> tuple[int, int]:
    if "x" not in spec:
        raise ValueError("tile grid must be COLSxROWS, e.g. 5x4")
    cols_s, rows_s = spec.lower().split("x", 1)
    cols, rows = int(cols_s), int(rows_s)
    if cols < 1 or rows < 1:
        raise ValueError("tile grid dimensions must be positive")
    return cols, rows


def parse_exclusions(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_body_box(width: int, height: int, exclusions: list[str]) -> list[int]:
    # Conservative defaults: remove border and right-side titleblock strip only.
    margin_x = int(width * 0.02) if "border" in exclusions else 0
    margin_y = int(height * 0.02) if "border" in exclusions else 0
    titleblock_w = int(width * 0.22) if "titleblock" in exclusions else 0
    return [margin_x, margin_y, width - margin_x - titleblock_w, height - margin_y]


def partition_emit_boxes(body: list[int], cols: int, rows: int) -> list[tuple[int, int, list[int]]]:
    x0, y0, x1, y1 = body
    width = x1 - x0
    height = y1 - y0
    boxes: list[tuple[int, int, list[int]]] = []
    for row in range(rows):
        ey0 = y0 + (height * row) // rows
        ey1 = y0 + (height * (row + 1)) // rows
        for col in range(cols):
            ex0 = x0 + (width * col) // cols
            ex1 = x0 + (width * (col + 1)) // cols
            boxes.append((row + 1, col + 1, [ex0, ey0, ex1, ey1]))
    return boxes


def expand_read_box(emit: list[int], body: list[int], overlap: int) -> list[int]:
    return [
        max(body[0], emit[0] - overlap),
        max(body[1], emit[1] - overlap),
        min(body[2], emit[2] + overlap),
        min(body[3], emit[3] + overlap),
    ]


def draw_overlay(tile: Image.Image, emit: list[int], read: list[int], mini_grid: str) -> None:
    draw = ImageDraw.Draw(tile)
    local = [emit[0] - read[0], emit[1] - read[1], emit[2] - read[0], emit[3] - read[1]]
    draw.rectangle(local, outline=(255, 0, 0), width=5)
    cols, rows = parse_grid(mini_grid)
    for i in range(1, cols):
        x = local[0] + (local[2] - local[0]) * i // cols
        draw.line([(x, local[1]), (x, local[3])], fill=(255, 0, 0), width=1)
    for i in range(1, rows):
        y = local[1] + (local[3] - local[1]) * i // rows
        draw.line([(local[0], y), (local[2], y)], fill=(255, 0, 0), width=1)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    labels_x = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for c in range(cols):
        for r in range(rows):
            label = f"{labels_x[c]}{r + 1}"
            tx = local[0] + (local[2] - local[0]) * c // cols + 6
            ty = local[1] + (local[3] - local[1]) * r // rows + 6
            draw.text((tx, ty), label, fill=(255, 0, 0), font=font)


def load_reference(path: Path) -> dict | None:
    if not path:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def comparable_manifest(manifest: dict) -> list[dict]:
    keys = ["source_page", "tile_id", "tile_grid", "body_box_px", "body_exclusions", "read_box_px", "emit_box_px", "overlap_px", "mini_grid"]
    return [{key: tile.get(key) for key in keys} for tile in manifest.get("tiles", [])]


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare P&ID tiles with emit-zone overlays.")
    ap.add_argument("work_dir")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--tile-grid", default="5x4")
    ap.add_argument("--overlap-px", type=int, default=200)
    ap.add_argument("--body-exclusions", default="border,titleblock")
    ap.add_argument("--mini-grid", default="5x5")
    ap.add_argument("--tile-manifest-reference")
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    if not work_dir.is_dir():
        print(f"ERROR: work_dir not found: {work_dir}", file=sys.stderr)
        return 2
    try:
        cols, rows = parse_grid(args.tile_grid)
        parse_grid(args.mini_grid)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    exclusions = parse_exclusions(args.body_exclusions)

    manifest = {
        "tool": "prepare_pandid_tiles.py",
        "tile_grid": args.tile_grid,
        "overlap_px": args.overlap_px,
        "body_exclusions": exclusions,
        "mini_grid": args.mini_grid,
        "tiles": [],
    }

    written = 0
    for page in parse_pages(args.pages):
        page_path = work_dir / f"page_{page:04d}.png"
        if not page_path.is_file():
            print(f"ERROR: missing page image: {page_path}", file=sys.stderr)
            return 2
        with Image.open(page_path) as image:
            width, height = image.size
            body = compute_body_box(width, height, exclusions)
            page_tiles = []
            for row, col, emit in partition_emit_boxes(body, cols, rows):
                read = expand_read_box(emit, body, args.overlap_px)
                tile_id = f"page_{page:04d}_r{row:02d}_c{col:02d}"
                out = work_dir / f"page_{page:04d}_tile_r{row:02d}_c{col:02d}.png"
                tile = image.crop(tuple(read))
                draw_overlay(tile, emit, read, args.mini_grid)
                tile.save(out)
                entry = {
                    "tile_id": tile_id,
                    "source_page": page,
                    "tile_grid": args.tile_grid,
                    "body_box_px": body,
                    "body_exclusions": exclusions,
                    "read_box_px": read,
                    "emit_box_px": emit,
                    "overlap_px": args.overlap_px,
                    "mini_grid": args.mini_grid,
                    "image_path": out.name,
                    "image_sha256": sha256(out),
                }
                page_tiles.append(entry)
                manifest["tiles"].append(entry)
                written += 1
            (work_dir / f"page_{page:04d}_tile_manifest.json").write_text(
                json.dumps({"tiles": page_tiles}, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

    manifest_path = work_dir / "tile_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.tile_manifest_reference:
        ref = json.loads(Path(args.tile_manifest_reference).read_text(encoding="utf-8"))
        if comparable_manifest(ref) != comparable_manifest(manifest):
            print("ERROR: regenerated tile geometry differs from --tile-manifest-reference", file=sys.stderr)
            return 1

    validator = Path(__file__).with_name("validate_tile_partition.py")
    result = subprocess.run([sys.executable, str(validator), "--tile-manifest", str(manifest_path)], text=True)
    if result.returncode != 0:
        return result.returncode

    print(f"tiles_written={written}")
    print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
