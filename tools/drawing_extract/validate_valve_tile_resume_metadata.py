#!/usr/bin/env python3
"""Validate valve tile stub resume metadata against tile_manifest.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from valve_stub_layout import VALVE_SCHEMA_VERSION, parse


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate valve tile resume metadata.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--source-pdf", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--run-folder", required=True)
    ap.add_argument("--tile-manifest", required=True)
    args = ap.parse_args()

    root = Path(args.source_dir).resolve() / "P_AND_ID" / args.target / args.run_folder
    manifest = json.loads(Path(args.tile_manifest).read_text(encoding="utf-8"))
    expected_by_tile = {entry["tile_id"]: entry for entry in manifest.get("tiles", [])}
    mismatches: list[str] = []
    checked = 0
    for path in sorted(root.glob(f"{args.pdf_stem}_page_*_tile_*_{args.mode}_stub.md")):
        model = parse(path)
        if not (args.start_page <= model.source_page <= args.end_page):
            continue
        checked += 1
        expected = expected_by_tile.get(model.tile_id)
        if not expected:
            mismatches.append(f"{path.name}: tile_id not present in manifest")
            continue
        comparisons = {
            "valve_schema_version": (model.valve_schema_version, VALVE_SCHEMA_VERSION),
            "target": (model.extraction_target, args.target),
            "mode": (model.mode, args.mode),
            "source_pdf": (model.source_pdf, args.source_pdf),
            "source_page": (model.source_page, expected["source_page"]),
            "source_raster_path": (model.source_raster_path, str(Path(args.tile_manifest).parent / f"page_{model.source_page:04d}.png")),
            "tile_image_path": (model.tile_image_path, str(Path(args.tile_manifest).parent / expected["image_path"])),
            "tile_grid": (model.tile_grid, expected["tile_grid"]),
            "body_box_px": (model.body_box_px, expected["body_box_px"]),
            "body_exclusions": (model.body_exclusions, expected["body_exclusions"]),
            "read_box_px": (model.read_box_px, expected["read_box_px"]),
            "emit_box_px": (model.emit_box_px, expected["emit_box_px"]),
            "overlap_px": (model.overlap_px, expected["overlap_px"]),
            "mini_grid": (model.mini_grid, expected["mini_grid"]),
        }
        for key, (actual, expected_value) in comparisons.items():
            if actual != expected_value:
                mismatches.append(f"{path.name}: {key} expected {expected_value!r} got {actual!r}")
    if mismatches:
        for mismatch in mismatches:
            print(mismatch, file=sys.stderr)
        return 1
    print(f"stubs_checked={checked}")
    print("resume_safety=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
