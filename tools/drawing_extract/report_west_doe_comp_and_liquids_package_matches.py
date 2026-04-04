#!/usr/bin/env python3
"""
Generate package-match provenance reports for the West Doe compression/liquids extract.

Outputs:
1. per-final-row package driver report
2. per-master-row disposition report
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from reconcile_west_doe_comp_and_liquids_packages import (
    CONDENSATE_MERCAPTAN_PACKAGE,
    HEAT_MEDIUM_MODULE,
    INLET_COMPRESSOR_PACKAGE,
    INLET_SEPARATOR_PACKAGE,
    INLET_STABILIZER_PACKAGE,
    MANUAL_ADDITIONS,
    STAB_OVERHEAD_COMPRESSOR_PACKAGE,
    TANK_FARM_PUMP_MODULE,
    TEG_MODULE,
    VRU_PACKAGE,
)


PACKAGE_CANDIDATE_ROWS = {
    INLET_SEPARATOR_PACKAGE: {4, 5, 6, 7, 8},
    INLET_COMPRESSOR_PACKAGE: set(range(38, 52)),
    VRU_PACKAGE: set(range(123, 134)),
    HEAT_MEDIUM_MODULE: set(range(146, 152)),
    TEG_MODULE: set(range(52, 72)),
    CONDENSATE_MERCAPTAN_PACKAGE: set(range(79, 91)),
    INLET_STABILIZER_PACKAGE: set(range(9, 22)) | {207, 214, 215, 224, 234, 235, 236, 248},
    STAB_OVERHEAD_COMPRESSOR_PACKAGE: set(range(22, 38)),
    TANK_FARM_PUMP_MODULE: set(range(101, 108)),
    "Inlet Condensate Product Analyzer System (indicated)": {188, 189},
    "Electrical Building Module": set(range(304, 315)),
    "Unit Control System (UCS) - Compression": {351, 352},
    "Modbus Integration - Packaged Equipment": {354},
    "Metering System": {355},
    "Vendor buyout package": {264, 265, 268, 273, 274},
}


TOKEN_RE = re.compile(r"[a-z0-9]+")
AREA_ID_RE = re.compile(r"^\d{3,4}-\d+$")
EQUIPMENT_CLASS_TOKENS = {
    "compressor",
    "scrubber",
    "separator",
    "heater",
    "pump",
    "cooler",
    "condenser",
    "preheater",
    "reboiler",
    "exchanger",
    "tank",
    "column",
    "receiver",
    "coalescer",
    "filter",
    "strainer",
    "drum",
    "valve",
    "motor",
    "driver",
    "cylinder",
    "analyzer",
    "panel",
    "mixer",
    "blower",
    "contactor",
    "reactor",
    "pot",
    "frame",
}
PREFIX_CLASS_HINTS = {
    "K": {"compressor"},
    "KM": {"motor", "driver"},
    "AC": {"cooler"},
    "ACF": {"cooler", "frame"},
    "V": {"separator", "scrubber", "drum", "receiver", "pot", "reactor", "tank", "vessel"},
    "P": {"pump"},
    "E": {"exchanger", "reboiler", "condenser", "preheater", "heater"},
    "H": {"heater"},
    "TK": {"tank"},
    "ST": {"strainer"},
    "AE": {"analyzer"},
    "ASP": {"analyzer", "panel"},
    "MX": {"mixer"},
    "C": {"cylinder"},
    "B": {"blower"},
    "TC": {"coalescer", "filter"},
    "FC": {"contactor"},
    "F": {"filter"},
}


def normalize(text: str) -> str:
    text = text.replace("—", "-")
    text = text.replace("–", "-")
    text = text.replace("/", " ")
    text = text.replace("_", " ")
    return " ".join(TOKEN_RE.findall(text.lower()))


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(normalize(text)))


def split_equipment_number(equipment_number: str) -> set[str]:
    raw = (equipment_number or "").strip()
    if not raw or raw in {"No tag", "—", "N/A"}:
        return set()
    parts = []
    for chunk in raw.split("/"):
        part = chunk.strip()
        if not part:
            continue
        part = re.sub(r"\s+[A-Z]+$", "", part)
        parts.append(part)
    return set(parts) if parts else {raw}


def equipment_prefix(equipment_number: str) -> str:
    raw = (equipment_number or "").strip()
    if not raw or raw in {"No tag", "—", "N/A"}:
        return ""
    first = raw.split("-")[0].strip()
    return first


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_master_rows(path: Path) -> list[dict[str, str]]:
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for line_no, row in enumerate(reader, start=2):
            row = dict(row)
            row["master_row"] = str(line_no)
            rows.append(row)
    return rows


def score_row(final_row: dict[str, str], master_row: dict[str, str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    final_num = (final_row.get("equipment_number") or "").strip()
    master_num = (master_row.get("Equipment Number") or "").strip()
    final_parts = split_equipment_number(final_num)
    master_parts = split_equipment_number(master_num)
    if final_num and master_num and final_num == master_num:
        score += 140
        reasons.append("exact equipment_number")
    elif final_parts and master_parts and final_parts == master_parts:
        score += 120
        reasons.append("equivalent grouped equipment_number")
    elif final_parts and master_parts and final_parts.intersection(master_parts):
        score += 90
        reasons.append("partial grouped equipment_number overlap")

    final_name = (final_row.get("equipment_name") or "").strip()
    master_name = (master_row.get("Equipment Name") or "").strip()
    if final_name and master_name:
        ratio = SequenceMatcher(None, normalize(final_name), normalize(master_name)).ratio()
        score += int(ratio * 55)
        if ratio >= 0.65:
            reasons.append(f"name similarity {ratio:.2f}")

    final_name_tokens = tokens(final_name)
    master_name_tokens = tokens(master_name)
    if final_name_tokens and master_name_tokens:
        overlap = final_name_tokens.intersection(master_name_tokens)
        if overlap:
            score += min(len(overlap) * 8, 32)
            reasons.append(f"name token overlap: {' '.join(sorted(overlap))}")

    final_classes = final_name_tokens.intersection(EQUIPMENT_CLASS_TOKENS)
    if not final_classes:
        final_classes = PREFIX_CLASS_HINTS.get(equipment_prefix(final_num), set())
    master_classes = master_name_tokens.intersection(EQUIPMENT_CLASS_TOKENS)
    if not master_classes:
        master_classes = PREFIX_CLASS_HINTS.get(equipment_prefix(master_num), set())
    class_overlap = final_classes.intersection(master_classes)
    if class_overlap:
        score += min(len(class_overlap) * 16, 48)
        reasons.append(f"equipment class overlap: {' '.join(sorted(class_overlap))}")

    final_package = (final_row.get("package_name") or "").strip()
    master_package = (master_row.get("Package Name") or "").strip()
    if final_package and final_package != "None" and master_package == final_package:
        score += 45
        reasons.append("exact package_name")
    elif final_package and final_package != "None":
        overlap = tokens(final_package).intersection(tokens(master_package))
        if overlap:
            score += min(len(overlap) * 5, 20)
            reasons.append(f"package token overlap: {' '.join(sorted(overlap))}")

    final_context = " ".join(
        [
            final_row.get("system_name") or "",
            final_row.get("drawing") or "",
        ]
    )
    master_context = " ".join(
        [
            master_row.get("Package Name") or "",
            master_row.get("Notes") or "",
            master_row.get("Source KTY") or "",
            master_row.get("Source KA") or "",
        ]
    )
    overlap = tokens(final_context).intersection(tokens(master_context))
    if overlap:
        score += min(len(overlap) * 3, 12)
        reasons.append(f"context overlap: {' '.join(sorted(overlap))}")

    return score, reasons


def candidate_rows_for(final_row: dict[str, str], master_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    package_name = (final_row.get("package_name") or "").strip()
    equipment_number = (final_row.get("equipment_number") or "").strip()
    grouped_parts = split_equipment_number(equipment_number)

    if (final_row.get("drawing") or "").startswith("KTY-"):
        source_kty = final_row.get("drawing") or ""
        source_ka = final_row.get("source_page") or ""
        equipment_name = final_row.get("equipment_name") or ""
        return [
            row
            for row in master_rows
            if (row.get("Source KTY") or "").strip() == source_kty
            and (row.get("Source KA") or "").strip() == source_ka
            and (
                (row.get("Equipment Number") or "").strip() == equipment_number
                or normalize((row.get("Equipment Name") or "").strip()) == normalize(equipment_name)
            )
        ]

    exact_candidates = []
    for row in master_rows:
        master_num = (row.get("Equipment Number") or "").strip()
        master_parts = split_equipment_number(master_num)
        if equipment_number and master_num and (
            master_num == equipment_number or (grouped_parts and master_parts and grouped_parts.intersection(master_parts))
        ):
            exact_candidates.append(row)
    if exact_candidates:
        return exact_candidates

    candidate_ids = PACKAGE_CANDIDATE_ROWS.get(package_name)
    if candidate_ids:
        return [row for row in master_rows if int(row["master_row"]) in candidate_ids]

    return master_rows


def choose_driver(final_row: dict[str, str], master_rows: list[dict[str, str]]) -> tuple[dict[str, str] | None, str, str]:
    candidates = candidate_rows_for(final_row, master_rows)
    if not candidates:
        return None, "no_driver", "No credible master row candidate found."

    scored = []
    for candidate in candidates:
        score, reasons = score_row(final_row, candidate)
        scored.append((score, candidate, reasons))
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_row, reasons = scored[0]

    exact_added = (final_row.get("drawing") or "").startswith("KTY-")
    if exact_added and best_score >= 40:
        return best_row, "exact_master_addition", "; ".join(reasons)

    if (final_row.get("package_name") or "").strip() == "None":
        if best_score >= 35:
            return best_row, "none_supported_by_master", "; ".join(reasons)
        return None, "none_no_package_evidence", "No sufficiently strong master package evidence; kept package_name=None."

    if best_score >= 55:
        return best_row, "semantic_match", "; ".join(reasons)

    if best_score >= 40:
        return best_row, "package_basis_match", "; ".join(reasons)

    return None, "package_inference_without_single_driver", "Package assignment came from broader master context, but no single row was strong enough to cite as primary driver."


def classify_master_row(
    master_row: dict[str, str],
    used_driver_rows: set[int],
    appended_row_ids: set[int],
    supporting_context_rows: set[int],
) -> tuple[str, str]:
    row_id = int(master_row["master_row"])
    equipment_number = (master_row.get("Equipment Number") or "").strip()
    equipment_name = (master_row.get("Equipment Name") or "").strip()
    package_name = (master_row.get("Package Name") or "").strip()

    if row_id in appended_row_ids:
        return "appended_to_final_csv", "Master row was appended directly into the final CSV."
    if row_id in used_driver_rows:
        return "used_as_primary_driver", "Master row was cited as the primary driver for at least one final package decision."
    if row_id in supporting_context_rows:
        return "supporting_package_context_only", "Master row informed package context but was not selected as the primary row-level driver."

    if equipment_number == "—" or equipment_name == "—":
        return "excluded_placeholder", "Placeholder row with no usable equipment content."
    if equipment_number == "No tag" and package_name not in {"", "N/A", "—"}:
        return "excluded_generic_packaged_context", "Packaged context row was too generic or duplicate to append as its own equipment row."
    if equipment_number == "No tag":
        return "excluded_generic_untagged_context", "Generic untagged DBM row; not strong enough to append over PFD-primary data."
    if AREA_ID_RE.match(equipment_number):
        return "excluded_normalized_area_or_building_id", "Normalized area/building identifier, not a preferred equipment-row key for the final CSV."
    if package_name in {"Pembina Scope", "NorthRiver Midstream Scope"}:
        return "excluded_scope_marker", "Scope marker rather than package evidence."
    return "excluded_secondary_source_row", "Secondary-source row was not selected for direct use or append."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("final_csv")
    parser.add_argument("master_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    final_csv = Path(args.final_csv).resolve()
    master_csv = Path(args.master_csv).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    final_rows = load_csv_rows(final_csv)
    master_rows = load_master_rows(master_csv)

    package_match_report = output_dir / f"{final_csv.stem}_package_match_report.csv"
    master_disposition_report = output_dir / f"{final_csv.stem}_master_row_disposition.csv"

    row_reports: list[dict[str, str]] = []
    used_driver_rows: set[int] = set()
    supporting_context_rows: set[int] = set()
    appended_row_ids: set[int] = set()
    master_to_final_rows: dict[int, list[str]] = defaultdict(list)

    manual_addition_index = {
        (
            addition["equipment_number"],
            addition["equipment_name"],
            addition["drawing"],
            addition["source_page"],
        )
        for addition in MANUAL_ADDITIONS
    }

    for final_index, final_row in enumerate(final_rows, start=2):
        driver, match_type, rationale = choose_driver(final_row, master_rows)
        package_name = (final_row.get("package_name") or "").strip()
        package_pool = PACKAGE_CANDIDATE_ROWS.get(package_name, set())
        supporting_context_rows.update(package_pool)

        final_key = (
            (final_row.get("equipment_number") or "").strip(),
            (final_row.get("equipment_name") or "").strip(),
            (final_row.get("drawing") or "").strip(),
            (final_row.get("source_page") or "").strip(),
        )
        row_origin = "master_addition" if final_key in manual_addition_index else "pfd_primary"

        report_row = {
            "final_row": str(final_index),
            "row_origin": row_origin,
            "equipment_number": (final_row.get("equipment_number") or "").strip(),
            "equipment_name": (final_row.get("equipment_name") or "").strip(),
            "system_name": (final_row.get("system_name") or "").strip(),
            "drawing": (final_row.get("drawing") or "").strip(),
            "source_page": (final_row.get("source_page") or "").strip(),
            "package_name": package_name,
            "match_type": match_type,
            "decision_rationale": rationale,
            "master_row": "",
            "master_source_kty": "",
            "master_source_ka": "",
            "master_equipment_number": "",
            "master_equipment_name": "",
            "master_package_name": "",
        }

        if driver is not None:
            master_row_id = int(driver["master_row"])
            report_row.update(
                {
                    "master_row": driver["master_row"],
                    "master_source_kty": (driver.get("Source KTY") or "").strip(),
                    "master_source_ka": (driver.get("Source KA") or "").strip(),
                    "master_equipment_number": (driver.get("Equipment Number") or "").strip(),
                    "master_equipment_name": (driver.get("Equipment Name") or "").strip(),
                    "master_package_name": (driver.get("Package Name") or "").strip(),
                }
            )
            used_driver_rows.add(master_row_id)
            master_to_final_rows[master_row_id].append(str(final_index))
            if row_origin == "master_addition":
                appended_row_ids.add(master_row_id)
        row_reports.append(report_row)

    with package_match_report.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "final_row",
                "row_origin",
                "equipment_number",
                "equipment_name",
                "system_name",
                "drawing",
                "source_page",
                "package_name",
                "match_type",
                "master_row",
                "master_source_kty",
                "master_source_ka",
                "master_equipment_number",
                "master_equipment_name",
                "master_package_name",
                "decision_rationale",
            ],
        )
        writer.writeheader()
        writer.writerows(row_reports)

    disposition_rows = []
    for master_row in master_rows:
        disposition, reason = classify_master_row(
            master_row,
            used_driver_rows=used_driver_rows,
            appended_row_ids=appended_row_ids,
            supporting_context_rows=supporting_context_rows,
        )
        row_id = int(master_row["master_row"])
        disposition_rows.append(
            {
                "master_row": master_row["master_row"],
                "disposition": disposition,
                "linked_final_rows": ",".join(master_to_final_rows.get(row_id, [])),
                "reason": reason,
                "source_kty": (master_row.get("Source KTY") or "").strip(),
                "source_ka": (master_row.get("Source KA") or "").strip(),
                "equipment_number": (master_row.get("Equipment Number") or "").strip(),
                "equipment_name": (master_row.get("Equipment Name") or "").strip(),
                "package_name": (master_row.get("Package Name") or "").strip(),
                "notes": (master_row.get("Notes") or "").strip(),
            }
        )

    with master_disposition_report.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "master_row",
                "disposition",
                "linked_final_rows",
                "reason",
                "source_kty",
                "source_ka",
                "equipment_number",
                "equipment_name",
                "package_name",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(disposition_rows)

    print(f"package_match_report={package_match_report}")
    print(f"master_disposition_report={master_disposition_report}")
    print(f"final_rows_reported={len(row_reports)}")
    print(f"master_rows_reported={len(disposition_rows)}")
    print(f"primary_driver_rows={len(used_driver_rows)}")
    print(f"appended_master_rows={len(appended_row_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
