#!/usr/bin/env python3
"""Flag repeated true valve tags in a P&ID valve candidate CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

from valve_stub_layout import DEFAULT_LINE_SPEC_RES, DEFAULT_TRUE_TAG_RE


EMPTY_TAGS = {"", "TBD", "N/A", "NA", "-"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    args = ap.parse_args()

    with Path(args.input_csv).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_tag: dict[str, list[dict[str, str]]] = defaultdict(list)
    profile_conflicts: list[dict[str, str]] = []
    for row in rows:
        tag = (row.get("visible_tag_text") or "").strip()
        if row.get("tag_status") == "true_tag" and tag.upper() not in EMPTY_TAGS:
            by_tag[tag].append(row)
            conflict_reasons: list[str] = []
            if not DEFAULT_TRUE_TAG_RE.fullmatch(tag):
                conflict_reasons.append("true_tag_grammar_mismatch")
            if any(pattern.fullmatch(tag) for pattern in DEFAULT_LINE_SPEC_RES):
                conflict_reasons.append("line_spec_heuristic_match")
            if conflict_reasons:
                profile_conflicts.append(
                    {
                        "visible_tag_text": tag,
                        "candidate_id": row.get("candidate_id", ""),
                        "source_page": row.get("source_page", ""),
                        "tile_id": row.get("tile_id", ""),
                        "review_reason": ";".join(conflict_reasons),
                    }
                )

    out_cols = [
        "visible_tag_text",
        "occurrence_count",
        "pages",
        "tile_ids",
        "candidate_ids",
        "review_reason",
    ]
    out_rows: list[dict[str, str]] = []
    for tag, tag_rows in sorted(by_tag.items()):
        if len(tag_rows) <= 1:
            continue
        pages = sorted({row.get("source_page", "") for row in tag_rows})
        tiles = sorted({row.get("tile_id", "") for row in tag_rows})
        out_rows.append(
            {
                "visible_tag_text": tag,
                "occurrence_count": str(len(tag_rows)),
                "pages": ";".join(pages),
                "tile_ids": ";".join(tiles),
                "candidate_ids": ";".join(sorted({row.get("candidate_id", "") for row in tag_rows})),
                "review_reason": "duplicate_true_tag_review",
            }
        )

    output = Path(args.output_csv)
    profile_cols = ["visible_tag_text", "candidate_id", "source_page", "tile_id", "review_reason"]
    profile_output = output.with_name(output.stem + "_tag_profile_review.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_cols)
        writer.writeheader()
        writer.writerows(out_rows)
    with profile_output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=profile_cols)
        writer.writeheader()
        writer.writerows(profile_conflicts)

    print(f"duplicate_tags={len(out_rows)}")
    print(f"tag_profile_conflicts={len(profile_conflicts)}")
    print(f"output_csv={output}")
    print(f"tag_profile_review_csv={profile_output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
