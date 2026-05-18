#!/usr/bin/env python3
"""Validate titleblock stub resume metadata."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from titleblock_stub_layout import parse


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate titleblock resume metadata.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--source-pdf", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--run-folder", required=True)
    ap.add_argument("--corner-width-ratio", type=float, default=0.25)
    ap.add_argument("--corner-height-ratio", type=float, default=0.25)
    args = ap.parse_args()
    root = Path(args.source_dir).resolve() / "DRAWING_SET" / "titleblock_index" / args.run_folder
    mismatches: list[str] = []
    checked = 0
    for page in range(args.start_page, args.end_page + 1):
        path = root / f"{args.pdf_stem}_page_{page:04d}_titleblock_stub.md"
        if not path.exists():
            continue
        checked += 1
        try:
            model = parse(path)
        except Exception as exc:
            mismatches.append(f"{path}: parse error: {exc}")
            continue
        expected = {
            "source_pdf": args.source_pdf,
            "source_page": page,
            "width_ratio": args.corner_width_ratio,
            "height_ratio": args.corner_height_ratio,
        }
        actual = {
            "source_pdf": model.source_pdf,
            "source_page": model.source_page,
            "width_ratio": float(model.corner_crop_geometry.get("width_ratio", -1)),
            "height_ratio": float(model.corner_crop_geometry.get("height_ratio", -1)),
        }
        if actual != expected:
            mismatches.append(f"{path}: expected {expected} got {actual}")
    if mismatches:
        for mismatch in mismatches:
            print(mismatch, file=sys.stderr)
        return 1
    print(f"stubs_checked={checked}")
    print("resume_safety=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
