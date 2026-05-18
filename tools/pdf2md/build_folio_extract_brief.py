#!/usr/bin/env python3
"""
build_folio_extract_brief.py
Render an INIT-TASK brief for one `pdf2md-folio-extract` dispatch.

Usage:
    python3 tools/pdf2md/build_folio_extract_brief.py \\
        --work-dir <_Sources/<book>_pdf2md_work> \\
        --page <N>

Outputs the brief on stdout. The brief instructs the TASK agent to read
one page raster and emit a single JSON file at
`<work_dir>/page_folios/<page>.json` containing the printed-folio
extraction result per `skills/pdf2md-folio-extract/BRIEF_SCHEMA.md`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--work-dir", required=True)
    p.add_argument("--page", required=True, type=int)
    p.add_argument("--output-path", default=None,
                   help="Where the skill writes its JSON output. "
                        "Default: <work_dir>/page_folios/page_NNNN.json")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.page < 1:
        print("ERROR: --page must be >= 1", file=sys.stderr)
        return 2
    work_dir = Path(args.work_dir).resolve()
    if not work_dir.is_dir():
        print(f"ERROR: --work-dir is not a directory: {work_dir}", file=sys.stderr)
        return 2

    image_path = work_dir / f"page_{args.page:04d}.png"
    if not image_path.is_file():
        print(f"ERROR: page image not found: {image_path}", file=sys.stderr)
        return 2

    output_path = (
        Path(args.output_path).resolve()
        if args.output_path
        else work_dir / "page_folios" / f"page_{args.page:04d}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    brief = f"""PURPOSE: Extract the printed folio label visible on one PDF page
RequestedBy: PDF2MD
ActingSurface: TASK+pdf2md-folio-extract

ScopePath: {work_dir}
TaskSkill: pdf2md-folio-extract

RuntimeOverrides:
  IMAGE_PATH: {image_path}
  OUTPUT_PATH: {output_path}
  PAGE_NUM: {args.page}

AllowedWriteTargets:
  - {output_path}

ExpectedOutputs:
  - One JSON file at OUTPUT_PATH matching `pdf2md-folio-extract/v1`.

AcceptanceCriteria:
  1. JSON parses and carries the schema_version literal `pdf2md-folio-extract/v1`.
  2. `page` equals {args.page}.
  3. `run_status` is one of SUCCESS / NO_FOLIO / FAILED / FAILED_INPUTS.
  4. `page_label` is a string or null. NEVER invented from the sequence.
"""
    sys.stdout.write(brief)
    return 0


if __name__ == "__main__":
    sys.exit(main())
