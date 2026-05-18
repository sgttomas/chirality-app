#!/usr/bin/env python3
"""
redispatch_csv_text_tables.py

Phase 4a orchestration helper for the table-handling rework. Identifies
every page in a `_Sources/*_pdf2md_work/` tree whose existing
`page_NNNN_assets.json` still carries one or more legacy `csv_text`
table entries, and renders the per-page `pdf2md-page-assets` brief
needed to re-dispatch that page through the skill under the new
`table_data` contract.

The actual VLM fan-out is performed by the calling persona / orchestrator
(Opus spawning Sonnet subagents, one per brief, per the doctrine in the
plan file). This tool stays in its deterministic lane: enumeration,
brief rendering, and status reporting.

Usage:
    python3 redispatch_csv_text_tables.py \
        --sources-root domains/piping-design/_Sources \
        [--briefs-dir /tmp/pdf2md-redispatch-briefs] \
        [--source MWK_1956_pdf2md_work] \
        [--limit N]

Outputs:
    A JSON queue file at {briefs-dir}/_queue.json listing each pending
    dispatch: (work_dir, doc_stem, page, total_pages, brief_path,
    output_path). The orchestrator iterates this queue and spawns one
    Sonnet TASK subagent per entry, then drops the produced JSON at the
    `output_path`. Each brief file is also written under {briefs-dir}/.

Exit codes:
    0  Queue rendered (or no work to do).
    2  Bad input.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enumerate pages with csv_text and render redispatch briefs.")
    parser.add_argument("--sources-root", required=True)
    parser.add_argument("--briefs-dir", default="/tmp/pdf2md-redispatch-briefs")
    parser.add_argument("--source", help="Limit to one work_dir name (e.g. MWK_1956_pdf2md_work)")
    parser.add_argument("--limit", type=int, default=0, help="Cap the queue at N entries (0 = no cap)")
    return parser.parse_args()


def page_has_csv_text(json_path: Path) -> bool:
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    for asset in data.get("assets", []):
        if not isinstance(asset, dict):
            continue
        if asset.get("kind") != "tbl":
            continue
        if (asset.get("csv_text") or "").strip():
            return True
    return False


def total_pages_for_work_dir(work_dir: Path) -> int:
    manifest = work_dir / "manifest.json"
    if not manifest.is_file():
        return 0
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return 0
    pages = data.get("pages_rendered") or []
    return len(pages) if isinstance(pages, list) else 0


def render_brief(work_dir: Path, doc_stem: str, page: int, total_pages: int, brief_path: Path) -> bool:
    cmd = [
        sys.executable,
        "tools/pdf2md/build_page_assets_brief.py",
        "--work-dir", str(work_dir),
        "--doc-stem", doc_stem,
        "--page", str(page),
        "--total-pages", str(total_pages),
        "--output-json", str(work_dir / f"page_{page:04d}_assets.json"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(f"build_page_assets_brief failed for {doc_stem} p{page}: {proc.stderr}\n")
        return False
    brief_path.write_text(proc.stdout, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    sources_root = Path(args.sources_root).resolve()
    if not sources_root.is_dir():
        sys.stderr.write(f"ERROR: sources-root is not a directory: {sources_root}\n")
        return 2

    briefs_dir = Path(args.briefs_dir).resolve()
    briefs_dir.mkdir(parents=True, exist_ok=True)

    queue: list[dict] = []
    for work_dir in sorted(sources_root.iterdir()):
        if not work_dir.is_dir() or not work_dir.name.endswith("_pdf2md_work"):
            continue
        if args.source and work_dir.name != args.source:
            continue
        doc_stem = work_dir.name.removesuffix("_pdf2md_work")
        total_pages = total_pages_for_work_dir(work_dir)
        if not total_pages:
            sys.stderr.write(f"WARN: {work_dir.name} has no manifest.pages_rendered; skipping\n")
            continue

        for jp in sorted(work_dir.glob("page_*_assets.json")):
            if not page_has_csv_text(jp):
                continue
            try:
                page = int(jp.name.removeprefix("page_").removesuffix("_assets.json"))
            except ValueError:
                continue
            brief_path = briefs_dir / f"{doc_stem}_p{page:04d}.brief.md"
            if not render_brief(work_dir, doc_stem, page, total_pages, brief_path):
                continue
            queue.append({
                "doc_stem": doc_stem,
                "work_dir": str(work_dir),
                "page": page,
                "total_pages": total_pages,
                "brief_path": str(brief_path),
                "output_path": str(work_dir / f"page_{page:04d}_assets.json"),
            })
            if args.limit and len(queue) >= args.limit:
                break
        if args.limit and len(queue) >= args.limit:
            break

    queue_path = briefs_dir / "_queue.json"
    queue_path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    print(f"queue_size={len(queue)} queue_path={queue_path} briefs_dir={briefs_dir}")
    print("Next: the orchestrator (Opus) spawns one TASK+pdf2md-page-assets subagent per")
    print("queue entry, using model='sonnet'. Each subagent reads brief_path, executes,")
    print("and writes structured JSON to output_path. After all complete, run Phase 4c.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
