#!/usr/bin/env python3
"""
sanitize_equipment_stubs.py
Apply deterministic post-extraction QC to page-level equipment stubs.

Designed primarily for drawing sets like the Deepcut PFDs where the page worker
can misread notes/spec text as top-of-sheet equipment findings.

Reads/writes v2 target-aware stubs at
``{source_dir}/{drawing_type}/{extraction_target}/{pdf_stem}_page_{NNNN}_stub.md``
via the frozen W1 API (``parse_stub`` / ``render_stub`` / ``resolve_stub_path``).

Sanitization rules operate on the BASE 4 columns (equipment_number,
equipment_name, system_name, drawing). For the detailed target, any detail
columns present on kept rows are preserved verbatim. Detail columns do NOT
influence filtering decisions; rows that fail the base-column filter are
dropped regardless of detail values.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from normalize_equipment_stub_layout import (
    BASE_COLUMNS,
    parse_stub,
    render_stub,
    resolve_stub_path,
)


INSTRUMENT_PREFIXES = {
    "AI", "AIC", "API", "BOV", "FCV", "FIC", "FIT", "FV", "HIPPS", "HPPS",
    "HIC", "HMI", "LIC", "LIT", "LSS", "PCV", "PIC", "PIT", "PI", "PRV",
    "PSV", "PSH", "PSL", "PT", "PV", "SDV", "TE", "TI", "TIC", "TSH", "XV",
}

EQUIPMENT_PREFIX_STOP_WORDS = {
    "P": ["PUMP", "PUMPS"],
    "AC": ["INTERCOOLER", "AFTERCOOLER", "COOLER"],
    "ACF": ["FRAME", "COOLER"],
    "K": ["COMPRESSOR"],
    "KD": ["DRIVER"],
    "KM": ["MOTOR", "DRIVER"],
    "C": ["CYLINDER"],
    "TK": ["POT", "TANK", "TANKS", "BULLETS", "BULLET"],
    "V": ["SCRUBBER", "SEPARATOR", "DRUM", "VESSEL", "REACTOR", "BULLETS", "BULLET"],
    "E": ["PREHEATER", "EXCHANGER", "EXCH", "REBOILER", "HEATER", "CONDENSER", "COOLER"],
    "ST": ["STRAINER"],
    "F": ["COALESCER", "FILTER", "FILTERS"],
    "H": ["HEATER"],
    "T": ["COLUMN", "TOWER", "CONTACTOR", "STABILIZER"],
    "L": ["COLUMN", "STILL", "DEHYDRATOR"],
    "FC": ["CONTACTOR"],
    "TC": ["COALESCER", "FILTER"],
    "MX": ["MIXER"],
    "B": ["BLOWER"],
    "AE": ["ANALYZER"],
    "ASP": ["PANEL", "ANALYZER"],
    "PR": ["RECEIVER"],
}

NOTE_NAME_STARTS = {
    "CONNECTIONS", "DUTY", "INSTALLED", "MAINTAIN", "ONLY", "PLAN",
    "PROCESS TRAIN", "TYPE", "VALVES", "WITH COMMON FRAME", "BAYS FAN/BAY",
    "COMMON", "MANUAL", "WITH ",
}

NOTE_NAME_CONTAINS = {
    "CSA B149.2", "INSTALLED SPARE", "PRIORITY", "SET ", " PSIG", " MMBTU",
    "PARALLEL STAGGERED", "GENERATOR FUEL SYSTEM", "API-661", "TEMA",
    "MODEL ", "POLE", "INDUCTION", "MODIFIED", "MICRON", "X RATED",
    "SIL 1X", "PIPELINE ALLOCATION", "EXCESS FLOW VALVES", "LOUVERS",
    "COMMON FRAME", "FRAME COMMON", " AERIAL COOLER WITH",
}

TOKEN_RE = re.compile(r"[A-Z0-9/.\-+]+")


def tag_prefix(equipment_number: str) -> str:
    raw = equipment_number.strip().upper()
    if not raw:
        return ""
    return raw.split("-", 1)[0]


def looks_like_equipment_tag(equipment_number: str) -> bool:
    raw = equipment_number.strip().upper()
    if not raw:
        return False
    if raw == "API-661":
        return False
    prefix = tag_prefix(raw)
    if prefix in INSTRUMENT_PREFIXES:
        return False
    return "-" in raw and any(ch.isdigit() for ch in raw)


def clean_name_for_tag(equipment_number: str, equipment_name: str) -> str:
    name = " ".join((equipment_name or "").upper().replace(",", " ").split())
    if not name:
        return ""

    prefix = tag_prefix(equipment_number)
    stop_words = EQUIPMENT_PREFIX_STOP_WORDS.get(prefix, [])
    if stop_words:
        tokens = name.split()
        for index, token in enumerate(tokens):
            normalized = token.rstrip("S")
            if token in stop_words or normalized in [word.rstrip("S") for word in stop_words]:
                return " ".join(tokens[: index + 1]).strip()
    return name


def has_expected_class(prefix: str, name: str) -> bool:
    stop_words = EQUIPMENT_PREFIX_STOP_WORDS.get(prefix, [])
    upper_name = name.upper()
    return any(f" {word} " in f" {upper_name} " for word in stop_words)


def is_note_like_name(name: str) -> bool:
    if not name:
        return True
    upper = name.upper().strip()
    if any(upper.startswith(prefix) for prefix in NOTE_NAME_STARTS):
        return True
    if any(fragment in upper for fragment in NOTE_NAME_CONTAINS):
        return True
    if upper in {"PV", "DP", "X S/S", "I.D X S/S X S/S", "UEL SCRUBBER", "LP FLASH"}:
        return True
    return False


def sanitize_rows(rows: list[list[str]]) -> tuple[list[list[str]], list[dict[str, str]]]:
    """Sanitize findings rows using the base-column filters.

    Rows may carry extra detail columns after the base 4; those are preserved
    verbatim on kept rows and ignored for filtering decisions. Filter rules
    operate solely on ``equipment_number`` (idx 0) and ``equipment_name``
    (idx 1); ``system_name`` (idx 2) and ``drawing`` (idx 3) pass through.
    """
    kept: list[list[str]] = []
    actions: list[dict[str, str]] = []
    base_len = len(BASE_COLUMNS)
    for row in rows:
        padded = list(row) + [""] * max(0, base_len - len(row))
        equipment_number = padded[0]
        equipment_name = padded[1]
        system_name = padded[2]
        drawing = padded[3]
        detail_tail = padded[base_len:]

        original_tag = (equipment_number or "").strip()
        original_name = " ".join((equipment_name or "").split())

        if not looks_like_equipment_tag(original_tag):
            actions.append(
                {
                    "action": "dropped",
                    "equipment_number": original_tag,
                    "equipment_name": original_name,
                    "reason": "invalid_or_instrument_tag",
                }
            )
            continue

        cleaned_name = clean_name_for_tag(original_tag, original_name)
        prefix = tag_prefix(original_tag)
        if prefix in EQUIPMENT_PREFIX_STOP_WORDS and not has_expected_class(prefix, cleaned_name):
            actions.append(
                {
                    "action": "dropped",
                    "equipment_number": original_tag,
                    "equipment_name": original_name,
                    "reason": "name_missing_expected_equipment_class",
                }
            )
            continue
        if is_note_like_name(cleaned_name):
            actions.append(
                {
                    "action": "dropped",
                    "equipment_number": original_tag,
                    "equipment_name": original_name,
                    "reason": "note_like_or_descriptor_text",
                }
            )
            continue

        if cleaned_name != original_name.upper():
            actions.append(
                {
                    "action": "trimmed_name",
                    "equipment_number": original_tag,
                    "equipment_name": original_name,
                    "reason": cleaned_name,
                }
            )

        kept.append([original_tag, cleaned_name, system_name, drawing] + detail_tail)

    return kept, actions


def main() -> int:
    parser = argparse.ArgumentParser(description="Sanitize page-level equipment stubs.")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--drawing-type", required=True)
    parser.add_argument("--extraction-target", required=True)
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    parser.add_argument("--report-csv")
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2

    report_csv = Path(args.report_csv).resolve() if args.report_csv else None

    report_rows: list[dict[str, str]] = []
    updated = 0
    pages_no_findings: list[int] = []
    missing_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = resolve_stub_path(
            source_dir,
            args.drawing_type,
            args.extraction_target,
            args.pdf_stem,
            page_num,
        )
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue

        parsed = parse_stub(stub_path, page_num)
        original_status = str(parsed.get("status", ""))
        if original_status in ("FAILED", "FAILED_INPUTS"):
            # Preserve failure status — sanitization does not apply to failed pages.
            continue
        meaningful_rows = [
            row for row in parsed["rows"]
            if (len(row) >= 4 and (row[0] or row[1] or row[3]))
        ]
        sanitized_rows, actions = sanitize_rows(meaningful_rows)

        for action in actions:
            report_rows.append(
                {
                    "page": str(page_num),
                    "action": action["action"],
                    "equipment_number": action["equipment_number"],
                    "equipment_name": action["equipment_name"],
                    "detail": action["reason"],
                }
            )

        columns = list(parsed.get("columns") or list(BASE_COLUMNS))
        if sanitized_rows:
            parsed["rows"] = sanitized_rows
            parsed["status"] = "SUCCESS"
            parsed["note"] = "Top-of-sheet equipment header present after deterministic QC."
        else:
            empty_row = [""] * len(columns)
            if len(empty_row) >= 3:
                empty_row[2] = parsed.get("system_name", "")
            parsed["rows"] = [empty_row]
            parsed["status"] = "NO_FINDINGS"
            parsed["note"] = "No valid tagged top-of-sheet equipment header remained after deterministic QC."
            pages_no_findings.append(page_num)

        rendered = render_stub(page_num, parsed)
        original = stub_path.read_text(encoding="utf-8")
        if rendered != original:
            stub_path.write_text(rendered, encoding="utf-8")
            updated += 1

    if report_csv:
        report_csv.parent.mkdir(parents=True, exist_ok=True)
        with report_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["page", "action", "equipment_number", "equipment_name", "detail"],
            )
            writer.writeheader()
            writer.writerows(report_rows)

    print(f"updated={updated}")
    print(f"qc_no_findings_pages={','.join(str(p) for p in pages_no_findings) or 'none'}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    if report_csv:
        print(f"report={report_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
