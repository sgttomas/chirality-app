#!/usr/bin/env python3
"""
Extract every display equation ($$...$$) from per-page Markdown and emit an
HTML audit report rendering each equation next to its source page PNG.

This is a thin CLI wrapper. The rendering logic lives in
`tools/source_audit/equations.py`, which composes the shared base
(`tools/source_audit/{chunk,html_shell,page_strip,sidecar}.py`) with
equations-specific glue (KaTeX preview, backcheck note block,
4-state stat bar, equations JSONL stream).

The HTML report supports per-equation review state (Unreviewed / Verified /
Flagged-for-fix / system-set Backcheck). State lives in browser localStorage
during a session and is exported as two sidecar files alongside the audit HTML:

  - equations_verified.json : map of "page:hash" -> {page, hash, verified_at, ...}
  - equations_flagged.json  : map of "page:hash" -> {page, hash, description, ...}

Legacy bare names (verified.json / flagged.json / backcheck.json) under either
the flat audit/ dir or the nested audit/equations/working/ dir are still read as
a fallback for sources not yet migrated to the kind-prefixed layout.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.source_audit import equations  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--work-dir", required=True)
    p.add_argument("--out-html", required=True)
    p.add_argument("--out-jsonl", required=True)
    p.add_argument("--title", default="Equation audit")
    p.add_argument(
        "--crops-dir",
        default=None,
        help=(
            "Optional directory containing per-equation crops named "
            "page_NNNN_eq_NN.png. Defaults to <out-html-dir>/crops when present."
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    work = Path(args.work_dir).resolve()
    out_html = Path(args.out_html).resolve()
    out_jsonl = Path(args.out_jsonl).resolve()
    out_html.parent.mkdir(parents=True, exist_ok=True)
    audit_dir = out_html.parent

    records = equations.scan_pages(work)
    equations.write_jsonl(records, out_jsonl)

    crops_dir = Path(args.crops_dir).resolve() if args.crops_dir else None
    doc, counts = equations.render_equations_audit_page(
        records, audit_dir, args.title, crops_dir=crops_dir
    )
    out_html.write_text(doc, encoding="utf-8")

    pages = sorted({r["page"] for r in records})
    print(
        f"equations={counts['total']} pages={len(pages)} "
        f"verified={counts['verified']} flagged={counts['flagged']} "
        f"backcheck={counts['backcheck']} "
        f"html={out_html} jsonl={out_jsonl}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
