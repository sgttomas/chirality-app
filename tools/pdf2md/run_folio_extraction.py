#!/usr/bin/env python3
"""
run_folio_extraction.py
Aggregate per-page folio JSONs into a single `page_folios.json` keyed by
physical page number. Intended to be invoked AFTER the
`pdf2md-folio-extract` TASK fan-out has populated
`<work_dir>/page_folios/page_NNNN.json` for every page.

This script is the collection/aggregation step; the per-page TASK
dispatch itself is handled by an orchestrating agent (see
AGENT_PDF2MD.md Phase 1.5). Keeping dispatch separate from collection
mirrors the pattern in rasterize_pdf.py + aggregate_asset_manifest.py.

Usage:
    python3 tools/pdf2md/run_folio_extraction.py \\
        --work-dir <_Sources/<book>_pdf2md_work> \\
        [--output page_folios.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PER_PAGE_RE = re.compile(r"^page_(\d{4})\.json$")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--work-dir", required=True)
    p.add_argument("--output", default="page_folios.json")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    folios_dir = work_dir / "page_folios"
    output = work_dir / args.output

    if not folios_dir.is_dir():
        print(f"ERROR: folios dir not found: {folios_dir}", file=sys.stderr)
        return 2

    out: dict[str, dict] = {}
    missing: list[str] = []
    for path in sorted(folios_dir.glob("page_*.json")):
        m = PER_PAGE_RE.match(path.name)
        if not m:
            continue
        page = int(m.group(1))
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            missing.append(f"{path.name}: invalid JSON ({exc})")
            continue
        out[str(page)] = data

    output.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"folios={len(out)} output={output}" + (
        f" issues={len(missing)}" if missing else ""
    ))
    if missing:
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
