#!/usr/bin/env python3
"""
filter_logo_assets.py
Drop logo-like `img` assets from PDF2MD per-page assets JSON.

Header logos fingerprint the issuing organization and add no design-judgment
content; this filter removes them in-place before materialization. The filter
is idempotent and safe to re-run.

Rule: remove asset where kind == "img" AND caption matches /logo/i.

Usage:
    python3 filter_logo_assets.py WORK_DIR [--report REPORT_JSON]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LOGO_RE = re.compile(r"logo", re.IGNORECASE)


def filter_file(p: Path) -> int:
    data = json.loads(p.read_text())
    assets = data.get("assets") or []
    kept = [a for a in assets if not (a.get("kind") == "img" and LOGO_RE.search(a.get("caption") or ""))]
    removed = len(assets) - len(kept)
    if removed:
        data["assets"] = kept
        p.write_text(json.dumps(data, indent=2))
    return removed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Drop logo img assets from per-page assets JSONs.")
    ap.add_argument("work_dir", type=Path)
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args(argv)

    if not args.work_dir.is_dir():
        print(f"filter_logo_assets: not a directory: {args.work_dir}", file=sys.stderr)
        return 2

    total_removed = 0
    files_touched = 0
    for p in sorted(args.work_dir.glob("page_*_assets.json")):
        r = filter_file(p)
        total_removed += r
        if r:
            files_touched += 1

    report = {"work_dir": str(args.work_dir), "files_touched": files_touched, "removed": total_removed}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2))
    print(f"filter_logo_assets: removed={total_removed} files_touched={files_touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
