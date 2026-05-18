#!/usr/bin/env python3
"""Validate DRAWING_SET/titleblock_index stubs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from titleblock_stub_layout import parse, validate


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start, end = token.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(token))
    return sorted(pages)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate titleblock stubs.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--pages")
    ap.add_argument("--run-folder", required=True)
    args = ap.parse_args()
    source = Path(args.source_dir).resolve() / "DRAWING_SET" / "titleblock_index" / args.run_folder
    pages = parse_pages(args.pages) if args.pages else list(range(args.start_page, args.end_page + 1))
    failures: list[str] = []
    for page in pages:
        path = source / f"{args.pdf_stem}_page_{page:04d}_titleblock_stub.md"
        if not path.is_file():
            failures.append(f"page {page}: missing stub")
            continue
        try:
            model = parse(path)
            for error in validate(model):
                failures.append(f"page {page}: {error}")
        except Exception as exc:
            failures.append(f"page {page}: {exc}")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"pages_checked={len(pages)}")
    print("titleblock_format=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
