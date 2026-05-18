#!/usr/bin/env python3
"""Compare basic P&ID valve counts to detailed valve counts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_counts(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return {int(row["page"]): row for row in csv.DictReader(f)}


def pct(delta: int, basic_count: int) -> float:
    if basic_count == 0:
        return 0.0 if delta == 0 else 100.0
    return abs(delta) / basic_count * 100.0


def write_report(output_dir: Path, basic_counts: Path, detailed_counts: Path, delta_csv: Path, rows: list[dict[str, str]], flagged: int) -> None:
    total_delta = sum(int(row["delta"]) for row in rows)
    report = output_dir / "RECONCILIATION_REPORT.md"
    report.write_text(
        "\n".join(
            [
                "# P&ID Valve Basic-vs-Detailed Reconciliation Report",
                "",
                f"basic_counts_csv: {basic_counts}",
                f"detailed_counts_csv: {detailed_counts}",
                f"delta_csv: {delta_csv}",
                f"pages_compared: {len(rows)}",
                f"reconcile_review_pages: {flagged}",
                f"net_delta: {total_delta}",
                "",
                "Pages flagged `RECONCILE_REVIEW` should be inspected by the operator. This report is advisory; it does not accept or reject either run.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--basic-counts-csv", required=True)
    ap.add_argument("--detailed-counts-csv", required=True)
    ap.add_argument("--output-csv", required=True)
    ap.add_argument("--absolute-threshold", type=int, default=2)
    ap.add_argument("--percent-threshold", type=float, default=10.0)
    args = ap.parse_args()

    basic_path = Path(args.basic_counts_csv)
    detailed_path = Path(args.detailed_counts_csv)
    basic = load_counts(basic_path)
    detailed = load_counts(detailed_path)
    pages = sorted(set(basic) | set(detailed))
    out_cols = ["page", "basic_count", "detailed_count", "delta", "abs_delta_pct", "flag"]
    out_rows: list[dict[str, str]] = []
    flagged = 0
    for page in pages:
        b_row = basic.get(page, {})
        d_row = detailed.get(page, {})
        if b_row.get("reference_reason") or d_row.get("reference_reason"):
            continue
        b_count = int(b_row.get("total_count") or 0)
        d_count = int(d_row.get("total_count") or 0)
        delta = d_count - b_count
        abs_pct = pct(delta, b_count)
        flag = "RECONCILE_REVIEW" if abs(delta) > args.absolute_threshold and abs_pct > args.percent_threshold else "OK"
        if flag != "OK":
            flagged += 1
        out_rows.append(
            {
                "page": str(page),
                "basic_count": str(b_count),
                "detailed_count": str(d_count),
                "delta": str(delta),
                "abs_delta_pct": f"{abs_pct:.2f}",
                "flag": flag,
            }
        )

    output = Path(args.output_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        writer.writeheader()
        writer.writerows(out_rows)
    write_report(output.parent, basic_path, detailed_path, output, out_rows, flagged)
    print(f"pages={len(out_rows)}")
    print(f"reconcile_review_pages={flagged}")
    print(f"output_csv={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
