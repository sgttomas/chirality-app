#!/usr/bin/env python3
"""Aggregate P&ID valve candidate rows into deterministic page counts."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def parse_issue_flags(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if not raw or raw == "[]":
        return []
    if raw.startswith("[") and raw.endswith("]"):
        try:
            value = ast.literal_eval(raw)
            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]
        except Exception:
            return [part.strip() for part in raw[1:-1].split(",") if part.strip()]
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def page_numbers(start: int, end: int, pages: str | None) -> list[int]:
    if not pages:
        return list(range(start, end + 1))
    out: list[int] = []
    for part in pages.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(dict.fromkeys(out))


def load_reference_pages(path: Path | None) -> dict[int, str]:
    if not path:
        return {}
    out: dict[int, str] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            page_raw = row.get("source_page") or row.get("page")
            status = row.get("run_status") or row.get("status")
            if page_raw and status == "NO_FINDINGS_REFERENCE":
                out[int(page_raw)] = "legend_or_reference_sheet"
    return out


def write_latest_pointer(output_csv: Path, rows: list[dict[str, str]]) -> None:
    run_folder = output_csv.parent
    target_dir = run_folder.parent if run_folder.name.startswith("RUN-") else run_folder
    total = sum(int(row["accepted_plus_manual_review_count"]) for row in rows)
    pointer = target_dir / "_LATEST.md"
    pointer.write_text(
        "\n".join(
            [
                "---",
                "target: P_AND_ID/valve_count",
                f"run_folder: {run_folder.name}",
                "written_by: aggregate_valve_counts.py",
                f"written_at: {datetime.now().isoformat(timespec='seconds')}",
                "---",
                "",
                "# Latest P&ID Valve Count Aggregation",
                "",
                f"**Run folder:** `{run_folder}`",
                f"**Counts CSV:** `{output_csv}`",
                f"**Pages:** {len(rows)}",
                f"**Total accepted plus manual-review valves:** {total}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidates-csv", required=True)
    ap.add_argument("--output-csv", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--pages")
    ap.add_argument("--reference-status-csv", help="Optional CSV containing NO_FINDINGS_REFERENCE page statuses.")
    args = ap.parse_args()

    pages = page_numbers(args.start_page, args.end_page, args.pages)
    by_page: dict[int, list[dict[str, str]]] = defaultdict(list)
    with Path(args.candidates_csv).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            page = int(row["source_page"])
            by_page[page].append(row)

    reference_pages = load_reference_pages(Path(args.reference_status_csv) if args.reference_status_csv else None)
    out_cols = [
        "page",
        "drawing",
        "accepted_count",
        "accepted_plus_manual_review_count",
        "total_count",
        "auto_accept_count",
        "human_accept_count",
        "manual_review_count",
        "human_reject_count",
        "superseded_duplicate_count",
        "tagless_count",
        "line_spec_only_tag_count",
        "ambiguous_tag_count",
        "by_symbol_class_counts_json",
        "issue_flag_counts_json",
        "reference_reason",
    ]
    out_rows: list[dict[str, str]] = []
    for page in pages:
        rows = by_page.get(page, [])
        countable_rows = [row for row in rows if row.get("count_include") == "true" and row.get("review_status") != "superseded_duplicate"]
        accepted_rows = [row for row in countable_rows if row.get("review_status") in {"auto_accept", "human_accept"}]
        accepted_plus_manual = [row for row in countable_rows if row.get("review_status") in {"auto_accept", "human_accept", "manual_review"}]
        classes = Counter(row.get("symbol_class", "unknown") or "unknown" for row in rows)
        flags = Counter(flag for row in rows for flag in parse_issue_flags(row.get("issue_flags", "")))
        drawing = next((row.get("dwg_no", "") for row in rows if row.get("dwg_no")), "")
        out_rows.append(
            {
                "page": str(page),
                "drawing": drawing or "TBD",
                "accepted_count": str(len(accepted_rows)),
                "accepted_plus_manual_review_count": str(len(accepted_plus_manual)),
                "total_count": str(len(accepted_plus_manual)),
                "auto_accept_count": str(sum(1 for row in countable_rows if row.get("review_status") == "auto_accept")),
                "human_accept_count": str(sum(1 for row in countable_rows if row.get("review_status") == "human_accept")),
                "manual_review_count": str(sum(1 for row in countable_rows if row.get("review_status") == "manual_review")),
                "human_reject_count": str(sum(1 for row in rows if row.get("review_status") == "human_reject")),
                "superseded_duplicate_count": str(sum(1 for row in rows if row.get("review_status") == "superseded_duplicate")),
                "tagless_count": str(sum(1 for row in countable_rows if row.get("tag_status") in {"none", "unreadable"})),
                "line_spec_only_tag_count": str(sum(1 for row in rows if row.get("tag_status") == "line_spec_only")),
                "ambiguous_tag_count": str(sum(1 for row in rows if row.get("tag_status") == "ambiguous")),
                "by_symbol_class_counts_json": json.dumps(dict(sorted(classes.items())), sort_keys=True),
                "issue_flag_counts_json": json.dumps(dict(sorted(flags.items())), sort_keys=True),
                "reference_reason": reference_pages.get(page, ""),
            }
        )

    output = Path(args.output_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        writer.writeheader()
        writer.writerows(out_rows)
    write_latest_pointer(output, out_rows)
    print(f"pages={len(out_rows)}")
    print(f"output_csv={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
