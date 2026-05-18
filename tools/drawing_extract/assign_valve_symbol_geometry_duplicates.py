#!/usr/bin/env python3
"""Flag/supersede duplicate P&ID valve symbol observations by geometry."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


def as_float(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "") or 0)
    except ValueError:
        return 0.0


def center_distance(a: dict[str, str], b: dict[str, str]) -> float:
    return math.hypot(as_float(a, "center_x_px") - as_float(b, "center_x_px"), as_float(a, "center_y_px") - as_float(b, "center_y_px"))


def iou(a: dict[str, str], b: dict[str, str]) -> float:
    ax0, ay0, ax1, ay1 = (as_float(a, key) for key in ("bbox_x0_px", "bbox_y0_px", "bbox_x1_px", "bbox_y1_px"))
    bx0, by0, bx1, by1 = (as_float(b, key) for key in ("bbox_x0_px", "bbox_y0_px", "bbox_x1_px", "bbox_y1_px"))
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    inter = max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
    area_a = max(0.0, ax1 - ax0) * max(0.0, ay1 - ay0)
    area_b = max(0.0, bx1 - bx0) * max(0.0, by1 - by0)
    union = area_a + area_b - inter
    return inter / union if union else 0.0


def compatible_class(a: dict[str, str], b: dict[str, str]) -> bool:
    a_class = a.get("symbol_class", "")
    b_class = b.get("symbol_class", "")
    return a_class == b_class or "unknown" in {a_class, b_class}


def duplicate_reason(a: dict[str, str], b: dict[str, str], center_tol: float, iou_threshold: float) -> str:
    if a.get("source_page") != b.get("source_page"):
        return ""
    if not compatible_class(a, b):
        return ""
    dist = center_distance(a, b)
    overlap = iou(a, b)
    if dist <= center_tol:
        return f"center_distance={dist:.2f}"
    if overlap >= iou_threshold:
        return f"bbox_iou={overlap:.2f}"
    return ""


def merge_flag(existing: str, flag: str) -> str:
    flags = [part.strip() for part in (existing or "").strip("[]").split(",") if part.strip()]
    if flag not in flags:
        flags.append(flag)
    return "[" + ", ".join(flags) + "]" if flags else "[]"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    ap.add_argument("--duplicates-csv", required=True)
    ap.add_argument("--center-tolerance-px", type=float, default=20.0)
    ap.add_argument("--bbox-iou-threshold", type=float, default=0.50)
    args = ap.parse_args()

    input_path = Path(args.input_csv)
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if "review_status" not in fieldnames:
        print("input CSV missing review_status", file=sys.stderr)
        return 2

    duplicate_rows: list[dict[str, str]] = []
    for idx, row in enumerate(rows):
        if row.get("review_status") == "superseded_duplicate":
            continue
        for other in rows[idx + 1 :]:
            if other.get("review_status") == "superseded_duplicate":
                continue
            reason = duplicate_reason(row, other, args.center_tolerance_px, args.bbox_iou_threshold)
            if not reason:
                continue
            other["review_status"] = "superseded_duplicate"
            other["review_reason"] = "geometry_duplicate"
            other["count_include"] = "false"
            other["issue_flags"] = merge_flag(other.get("issue_flags", ""), "GEOMETRY_DUPLICATE_REVIEW")
            duplicate_rows.append(
                {
                    "kept_candidate_id": row.get("candidate_id", ""),
                    "superseded_candidate_id": other.get("candidate_id", ""),
                    "source_page": row.get("source_page", ""),
                    "reason": reason,
                    "kept_tile_id": row.get("tile_id", ""),
                    "superseded_tile_id": other.get("tile_id", ""),
                }
            )

    output = Path(args.output_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    duplicates = Path(args.duplicates_csv)
    duplicates.parent.mkdir(parents=True, exist_ok=True)
    duplicate_cols = ["kept_candidate_id", "superseded_candidate_id", "source_page", "reason", "kept_tile_id", "superseded_tile_id"]
    with duplicates.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=duplicate_cols)
        writer.writeheader()
        writer.writerows(duplicate_rows)

    print(f"geometry_duplicates={len(duplicate_rows)}")
    print(f"output_csv={output}")
    print(f"duplicates_csv={duplicates}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
