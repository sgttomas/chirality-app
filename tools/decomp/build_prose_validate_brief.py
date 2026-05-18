#!/usr/bin/env python3
"""
build_prose_validate_brief.py
Render an INIT-TASK brief for one `domain-prose-validate` dispatch
(Gate 1.5-P Stage 1).

Builds an asset-bbox-hints JSON for the page from the source's asset
manifest (kind + asset_id + bbox_norm of each asset on the page) so the
skill knows where placeholders are expected. The skill must NOT read
the original `page_NNNN.md` — that's the anti-confirmation-bias clause.

Usage:
    python3 tools/decomp/build_prose_validate_brief.py \\
        --work-dir <_Sources/<book>_pdf2md_work> \\
        --asset-manifest <_Sources/<book>_assets_manifest.json> \\
        --reextract-dir <_Sources/<book>/audit/prose_validation_extracts> \\
        --hints-dir <_Sources/<book>/audit/prose_validation_extracts/.hints> \\
        --page <N>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--work-dir", required=True)
    p.add_argument("--asset-manifest", required=True)
    p.add_argument("--reextract-dir", required=True,
                   help="Destination dir for page_NNNN.reextract.md outputs.")
    p.add_argument("--hints-dir", required=True,
                   help="Destination dir for the per-page asset-bbox hints JSONs.")
    p.add_argument("--page", required=True, type=int)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    manifest_path = Path(args.asset_manifest).resolve()
    reext_dir = Path(args.reextract_dir).resolve()
    hints_dir = Path(args.hints_dir).resolve()
    reext_dir.mkdir(parents=True, exist_ok=True)
    hints_dir.mkdir(parents=True, exist_ok=True)

    image_path = work_dir / f"page_{args.page:04d}.png"
    if not image_path.is_file():
        print(f"ERROR: page image not found: {image_path}", file=sys.stderr)
        return 2
    if not manifest_path.is_file():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    page_assets = [
        {
            "kind": a.get("kind", ""),
            "asset_id": a.get("asset_id", ""),
            "bbox_norm": a.get("bbox_norm", []),
        }
        for a in manifest.get("assets", [])
        if a.get("page") == args.page
    ]
    hints_path = hints_dir / f"page_{args.page:04d}.hints.json"
    hints_path.write_text(
        json.dumps({"page": args.page, "assets": page_assets}, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    output_path = reext_dir / f"page_{args.page:04d}.reextract.md"

    brief = f"""PURPOSE: Independently re-extract one page's prose for Gate 1.5-P Stage 1
RequestedBy: DOMAIN_DECOMP Gate 1.5-P
ActingSurface: TASK+domain-prose-validate

ScopePath: {work_dir.parent}
TaskSkill: domain-prose-validate

RuntimeOverrides:
  IMAGE_PATH: {image_path}
  ASSET_BBOX_HINTS_PATH: {hints_path}
  OUTPUT_PATH: {output_path}
  PAGE_NUM: {args.page}

AllowedWriteTargets:
  - {output_path}

ANTI-CONFIRMATION-BIAS CLAUSE:
  The skill MUST NOT read any pre-existing `page_NNNN.md` or `<book>.md`
  file. The re-extract must be produced from the raster alone. This is
  the cornerstone of 1.5-P — match between two extracts is silent but
  NOT verification.

ExpectedOutputs:
  - One Markdown file at OUTPUT_PATH containing prose, $$..$$ display
    equations, and `[FIGURE: ...]` / `[TABLE: ...]` / `[IMAGE: ...]`
    placeholders in reading order.

AcceptanceCriteria:
  1. The file exists and is non-empty.
  2. The skill has read only IMAGE_PATH and ASSET_BBOX_HINTS_PATH.
"""
    sys.stdout.write(brief)
    return 0


if __name__ == "__main__":
    sys.exit(main())
