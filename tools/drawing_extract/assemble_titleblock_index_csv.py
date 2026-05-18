#!/usr/bin/env python3
"""Assemble DRAWING_SET/titleblock_index stubs into CSV/Markdown and a scope proposal."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from titleblock_stub_layout import BODY_COLUMNS, parse


def pages_slug(start: int, end: int) -> str:
    return f"{start:04d}-{end:04d}"


def write_latest(target_dir: Path, run_folder: Path, pages: str, status: str) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    text = f"""---
target: DRAWING_SET/titleblock_index
run_folder: {run_folder.name}
written_by: assemble_titleblock_index_csv.py
written_at: {now}
---

# Latest run pointer - DRAWING_SET/titleblock_index

**Run folder:** [`{run_folder.name}`](./{run_folder.name}/)
**Pages:** {pages}
**Status:** {status}
"""
    (target_dir / "_LATEST.md").write_text(text, encoding="utf-8")


def write_scope_proposal(run_folder: Path, csv_path: Path, rows: list[dict[str, str]]) -> None:
    ranges: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        ranges[row.get("drawing_family_proposal", "TBD")].append(int(row["page"]))

    def compress(nums: list[int]) -> str:
        if not nums:
            return ""
        nums = sorted(nums)
        groups = []
        start = prev = nums[0]
        for n in nums[1:]:
            if n == prev + 1:
                prev = n
            else:
                groups.append(f"{start}-{prev}" if start != prev else str(start))
                start = prev = n
        groups.append(f"{start}-{prev}" if start != prev else str(start))
        return ", ".join(groups)

    scope_lines = [
        "# Scope Proposal - DRAWING_SET/titleblock_index",
        "",
        "This file is a proposal emitted by the inventory pass. For a P&ID valve run, copy or edit this into a scope file and pass it explicitly as the run's scope input.",
        "",
        f"- inventory_csv: {csv_path.name}",
        "",
        "## Proposed Page Ranges",
        "",
    ]
    for family, nums in sorted(ranges.items()):
        scope_lines.append(f"- {family}: {compress(nums)}  # proposal")
    scope_lines += ["", "## Operator Scope", "", "- P_AND_ID: TBD"]
    (run_folder / "scope_proposal.md").write_text("\n".join(scope_lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble titleblock index CSV/Markdown.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--output-csv", required=True)
    ap.add_argument("--output-md", required=True)
    ap.add_argument("--run-folder")
    args = ap.parse_args()

    source_dir = Path(args.source_dir).resolve()
    target_dir = source_dir / "DRAWING_SET" / "titleblock_index"
    run_folder = Path(args.output_csv).resolve().parent
    run_folder.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    missing: list[int] = []
    for page in range(args.start_page, args.end_page + 1):
        stub = run_folder / f"{args.pdf_stem}_page_{page:04d}_titleblock_stub.md"
        if not stub.is_file():
            missing.append(page)
            rows.append({"page": str(page), **{col: "" for col in BODY_COLUMNS}, "run_status": "MISSING"})
            continue
        model = parse(stub)
        row = {"page": str(page)}
        row.update({col: model.row.get(col, "") for col in BODY_COLUMNS})
        row["run_status"] = model.status
        rows.append(row)

    csv_path = Path(args.output_csv).resolve()
    md_path = Path(args.output_md).resolve()
    fieldnames = ["page"] + list(BODY_COLUMNS) + ["run_status"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Titleblock Index\n\n")
        handle.write("| " + " | ".join(fieldnames) + " |\n")
        handle.write("| " + " | ".join(["---"] * len(fieldnames)) + " |\n")
        for row in rows:
            handle.write("| " + " | ".join(row.get(col, "") for col in fieldnames) + " |\n")
    write_scope_proposal(run_folder, csv_path, rows)
    target_dir.mkdir(parents=True, exist_ok=True)
    write_latest(target_dir, run_folder, pages_slug(args.start_page, args.end_page), f"rows={len(rows)}, missing={len(missing)}")
    print(f"rows={len(rows)}")
    print(f"missing_pages={','.join(str(p) for p in missing) or 'none'}")
    print(f"output_csv={csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
