#!/usr/bin/env python3
"""
validate_pipe_spec_outputs.py
Output validator for the Pipe Spec extractor tool suite.

Walks an output tree produced by extract_pipe_specs_batch.py and asserts
the documented CSV contracts. Emits `_validation_report.csv` at the
output root and a stdout summary.

Usage:
    python3 tools/pipe_specs/validate_pipe_spec_outputs.py \
        --output-dir <OUTPUT_DIR>

Inputs:
    --output-dir DIR    Output root produced by the batch driver (required).

Outputs:
    {output-dir}/_validation_report.csv

Stdout: pass/fail summary lines.
Stderr: input errors.

Exit codes:
    0 — every spec passes validation
    1 — at least one validation failure
    2 — input error

Determinism:
    No LLM calls, no network, no API keys. Pure filesystem reads + schema
    assertions. Output is byte-identical across reruns on an unchanged tree.

Idempotence:
    Overwrites the validation report each run.

Write scope:
    Limited to {output-dir}/_validation_report.csv.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipe_spec_extractor import (  # noqa: E402
    DIAGNOSTICS_COLUMNS,
    HEADER_COLUMNS,
    RAW_ROWS_COLUMNS,
    SECTION_ORDER,
    TABLES_COLUMNS,
)

REPORT_COLUMNS = [
    "spec_id",
    "revision",
    "parse_status",
    "checks_passed",
    "checks_failed",
    "failures",
    "golden_assertions_total",
    "golden_assertions_failed",
    "golden_failures",
    "negative_check_failures",
    "rule_line_fallback_warning",
]

REQUIRED_PROVENANCE = [
    "piping_class",
    "source_pdf",
    "source_revision",
    "source_sha256",
    "section",
    "section_row_id",
]

DATE_RE = re.compile(r"^\d{1,2}[./-]\d{1,2}[./-]\d{2,4}$")

GOLDEN_SPECS = {
    ("MLE-PI-SPC-ASME_AA1", "R4"),
    ("MLE-PI-SPC-ASME_BC1", "R6"),
    ("MLE-PI-SPC-ASME_FA1", "R5"),
}

GOLDEN_ASSERTIONS = {
    ("MLE-PI-SPC-ASME_AA1", "R4"): [
        ("header_eq", "service_description", "Sweet Hydrocarbon Gases & Liquids, Glycol, LP Flare, Clean Oil, Combustion Air, Methanol, Nitrogen, Water", "AA1 service description"),
        ("header_contains", "mawp", "1,960", "AA1 MAWP"),
        ("table_row_eq", ("PIPE", "pipe:001", "item_or_type"), "TRD PIPE", "AA1 pipe:001 item"),
        ("table_row_eq", ("PIPE", "pipe:001", "schedule_or_rating"), "SCH 80", "AA1 pipe:001 schedule"),
        ("table_row_eq", ("PIPE", "pipe:001", "conn_or_ends"), "TE", "AA1 pipe:001 ends"),
        ("table_row_startswith", ("PIPE", "pipe:001", "description"), "ASTM A106 GR. B SMLS", "AA1 pipe:001 description"),
        ("table_row_eq", ("PIPE", "pipe:001", "note_code"), "ASME B36.10M", "AA1 pipe:001 note"),
        ("table_row_eq", ("FLANGES_FITTINGS", "flanges_fittings:004", "item_or_type"), "ORIFICE FLANGES", "AA1 flanges:004 item"),
        ("table_row_eq", ("FLANGES_FITTINGS", "flanges_fittings:004", "note_code"), "ASME B16.36", "AA1 flanges:004 note"),
        ("table_row_eq", ("VALVES", "valves:001", "item_or_type"), "BALL", "AA1 valves:001 item"),
        ("table_row_eq", ("VALVES", "valves:001", "item_filled"), "false", "AA1 valves:001 item_filled"),
        ("table_row_eq", ("VALVES", "valves:001", "schedule_or_rating"), "2000 WOG", "AA1 valves:001 rating"),
        ("table_row_contains", ("VALVES", "valves:001", "tag"), "/J0", "AA1 valves:001 tag"),
        ("table_row_eq", ("VALVES", "valves:001", "trim"), "CHR", "AA1 valves:001 trim"),
        ("table_row_eq", ("VALVES", "valves:008", "item_or_type"), "CHECK", "AA1 valves:008 item"),
        ("table_row_startswith", ("VALVES", "valves:008", "tag"), "CH-", "AA1 valves:008 tag"),
    ],
    ("MLE-PI-SPC-ASME_BC1", "R6"): [
        ("diag_eq", "blank_pages_skipped", "1", "BC1 blank trailing page"),
        ("header_eq", "service_description", "Sour Hydrocarbon Gases & Liquids, Drains, Flare Systems Produced Water", "BC1 service description"),
        ("header_eq", "piping_class", "BC1", "BC1 piping class"),
        ("header_eq", "revision", "6", "BC1 revision"),
    ],
    ("MLE-PI-SPC-ASME_FA1", "R5"): [
        ("table_any_row_eq", ("PIPE", "schedule_or_rating"), "CALCULATE WALL THICKNESS", "FA1 calculate wall thickness"),
        ("header_contains", "mawp", "42,550", "FA1 MAWP"),
        ("header_not_date", "service_description", "", "FA1 service description not date"),
    ],
}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        rows = list(reader)
    return cols, rows


def _diag_status(diag_rows: list[dict[str, str]]) -> str:
    for r in diag_rows:
        if r.get("metric") == "parse_status":
            return r.get("value", "")
    return ""


def _diag_lookup(diag_rows: list[dict[str, str]], metric: str) -> str:
    for r in diag_rows:
        if r.get("metric") == metric:
            return r.get("value", "")
    return ""


def _header_lookup(header_rows: list[dict[str, str]], field: str) -> str:
    for r in header_rows:
        if r.get("field") == field:
            return r.get("value", "")
    return ""


def _table_row_lookup(
    table_rows: list[dict[str, str]], section: str, row_id: str
) -> dict[str, str] | None:
    for r in table_rows:
        if r.get("section") == section and r.get("section_row_id") == row_id:
            return r
    return None


def _run_golden_assertions(
    spec_id: str,
    revision: str,
    header_rows: list[dict[str, str]],
    table_rows: list[dict[str, str]],
    diag_rows: list[dict[str, str]],
) -> tuple[int, list[str]]:
    assertions = GOLDEN_ASSERTIONS.get((spec_id, revision), [])
    failures: list[str] = []
    for kind, location, expected, label in assertions:
        ok = False
        actual = ""
        if kind == "header_eq":
            actual = _header_lookup(header_rows, location)
            ok = actual == expected
        elif kind == "header_contains":
            actual = _header_lookup(header_rows, location)
            ok = expected in actual
        elif kind == "header_not_date":
            actual = _header_lookup(header_rows, location)
            ok = bool(actual) and DATE_RE.match(actual) is None
        elif kind == "diag_eq":
            actual = _diag_lookup(diag_rows, location)
            ok = actual == expected
        elif kind in {"table_row_eq", "table_row_contains", "table_row_startswith"}:
            section, row_id, col = location
            row = _table_row_lookup(table_rows, section, row_id)
            actual = "" if row is None else row.get(col, "")
            if kind == "table_row_eq":
                ok = actual == expected
            elif kind == "table_row_contains":
                ok = expected in actual
            else:
                ok = actual.startswith(expected)
        elif kind == "table_any_row_eq":
            section, col = location
            matches = [
                r.get(col, "")
                for r in table_rows
                if r.get("section") == section and r.get(col, "") == expected
            ]
            actual = "|".join(matches)
            ok = bool(matches)
        if not ok:
            failures.append(f"{label}: expected {expected!r}, got {actual!r}")
    return len(assertions), failures


def _run_negative_checks(
    header_rows: list[dict[str, str]], table_rows: list[dict[str, str]]
) -> list[str]:
    failures: list[str] = []
    service_description = _header_lookup(header_rows, "service_description")
    if DATE_RE.match(service_description or ""):
        failures.append("service_description is date-like")

    for r in table_rows:
        row_label = f"{r.get('section')}:{r.get('section_row_id')}"
        if "ASTM" in r.get("conn_or_ends", ""):
            failures.append(f"{row_label}: conn_or_ends contains ASTM")
        if r.get("section") == "VALVES" and "FTB" in r.get("trim", ""):
            failures.append(f"{row_label}: VALVES trim contains FTB")
    return failures


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_spec_dir(
    spec_id: str, revision: str, rev_dir: Path, source_dir: Path | None
) -> dict[str, str]:
    failures: list[str] = []
    passed = 0
    golden_total = 0
    golden_failures: list[str] = []
    negative_failures: list[str] = []
    rule_line_fallback_warning = "false"

    diag_path = rev_dir / "_diagnostics.csv"
    if not diag_path.is_file():
        failures.append(f"missing:_diagnostics.csv")
        return {
            "spec_id": spec_id,
            "revision": revision,
            "parse_status": "",
            "checks_passed": str(passed),
            "checks_failed": str(len(failures)),
            "failures": ";".join(failures),
            "golden_assertions_total": "0",
            "golden_assertions_failed": "0",
            "golden_failures": "",
            "negative_check_failures": "",
            "rule_line_fallback_warning": "false",
        }
    diag_cols, diag_rows = _read_csv(diag_path)
    if diag_cols != DIAGNOSTICS_COLUMNS:
        failures.append(
            f"_diagnostics.csv columns mismatch: got {diag_cols}"
        )
    else:
        passed += 1

    parse_status = _diag_status(diag_rows)

    tables_path = rev_dir / "tables.csv"
    header_path = rev_dir / "_header.csv"
    raw_path = rev_dir / "_raw_rows.csv"

    if parse_status == "ok":
        # Must have all four files
        for f, label in (
            (tables_path, "tables.csv"),
            (header_path, "_header.csv"),
            (raw_path, "_raw_rows.csv"),
        ):
            if not f.is_file():
                failures.append(f"missing:{label}")
            else:
                passed += 1

        table_rows: list[dict[str, str]] = []
        header_rows: list[dict[str, str]] = []
        if tables_path.is_file():
            cols, table_rows = _read_csv(tables_path)
            if cols != TABLES_COLUMNS:
                failures.append(f"tables.csv columns mismatch: {cols}")
            else:
                passed += 1
            # Required provenance non-empty in every row
            empty_offenders: list[str] = []
            for ridx, r in enumerate(table_rows, start=2):
                for col in REQUIRED_PROVENANCE:
                    if not (r.get(col) or "").strip():
                        empty_offenders.append(f"row{ridx}:{col}")
                        break
            if empty_offenders:
                failures.append(
                    f"tables.csv empty provenance in {len(empty_offenders)} rows"
                )
            else:
                passed += 1
            # Row counts non-zero per section
            counts = {sec: 0 for sec in SECTION_ORDER}
            for r in table_rows:
                sec = r.get("section", "")
                if sec in counts:
                    counts[sec] += 1
            zero_secs = [s for s, c in counts.items() if c == 0]
            if zero_secs:
                failures.append(f"tables.csv zero rows in sections: {zero_secs}")
            else:
                passed += 1

        if header_path.is_file():
            cols, header_rows = _read_csv(header_path)
            if cols != HEADER_COLUMNS:
                failures.append(f"_header.csv columns mismatch: {cols}")
            else:
                passed += 1
        if raw_path.is_file():
            cols, _ = _read_csv(raw_path)
            if cols != RAW_ROWS_COLUMNS:
                failures.append(f"_raw_rows.csv columns mismatch: {cols}")
            else:
                passed += 1

        # SHA256 cross-check against source if locatable
        if source_dir is not None:
            source_pdf_name = _diag_lookup(diag_rows, "source_pdf")
            sha_diag = _diag_lookup(diag_rows, "source_sha256")
            src = source_dir / source_pdf_name
            if src.is_file() and sha_diag:
                if _sha256_of(src) != sha_diag:
                    failures.append("source_sha256 mismatch with source PDF")
                else:
                    passed += 1

        if table_rows and header_rows:
            negative_failures = _run_negative_checks(header_rows, table_rows)
            golden_total, golden_failures = _run_golden_assertions(
                spec_id, revision, header_rows, table_rows, diag_rows
            )

        fallback_count = int(_diag_lookup(diag_rows, "rule_line_fallbacks") or "0")
        if fallback_count > 0:
            rule_line_fallback_warning = "true"
            if (spec_id, revision) in GOLDEN_SPECS:
                golden_failures.append(
                    f"rule_line_fallbacks expected 0 for golden spec, got {fallback_count}"
                )
    elif parse_status == "parse_fail":
        # Must NOT have the three success files
        for f, label in (
            (tables_path, "tables.csv"),
            (header_path, "_header.csv"),
            (raw_path, "_raw_rows.csv"),
        ):
            if f.is_file():
                failures.append(f"unexpected:{label} present on parse_fail")
            else:
                passed += 1
    else:
        failures.append(f"unknown parse_status: {parse_status!r}")

    return {
        "spec_id": spec_id,
        "revision": revision,
        "parse_status": parse_status,
        "checks_passed": str(passed),
        "checks_failed": str(len(failures)),
        "failures": ";".join(failures),
        "golden_assertions_total": str(golden_total),
        "golden_assertions_failed": str(len(golden_failures)),
        "golden_failures": ";".join(golden_failures),
        "negative_check_failures": ";".join(negative_failures),
        "rule_line_fallback_warning": rule_line_fallback_warning,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--source-dir",
        default=None,
        help="Optional: directory of source PDFs for SHA-256 cross-check",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    if not output_dir.is_dir():
        print(f"ERROR: output directory not found: {output_dir}", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve() if args.source_dir else None

    # Walk: each immediate child is a spec_id; each grandchild is a revision.
    rev_dirs: list[tuple[str, str, Path]] = []
    for spec_dir in sorted(p for p in output_dir.iterdir() if p.is_dir()):
        for rev_dir in sorted(p for p in spec_dir.iterdir() if p.is_dir()):
            rev_dirs.append((spec_dir.name, rev_dir.name, rev_dir))

    summary_path = output_dir / "_extraction_summary.csv"
    summary_rows: list[dict[str, str]] = []
    if summary_path.is_file():
        _, summary_rows = _read_csv(summary_path)

    report_rows: list[dict[str, str]] = []
    fail_total = 0
    golden_total = 0
    golden_failed = 0
    negative_failed = 0
    fallback_warning_total = 0
    for spec_id, revision, rev_dir in rev_dirs:
        row = validate_spec_dir(spec_id, revision, rev_dir, source_dir)
        report_rows.append(row)
        if int(row["checks_failed"]) > 0:
            fail_total += 1
        golden_total += int(row.get("golden_assertions_total") or "0")
        golden_failed += int(row.get("golden_assertions_failed") or "0")
        if row.get("negative_check_failures"):
            negative_failed += len(row["negative_check_failures"].split(";"))
        if row.get("rule_line_fallback_warning") == "true":
            fallback_warning_total += 1

    # Cross-check: summary row count matches walked tree
    extra_failures: list[str] = []
    if summary_rows:
        if len(summary_rows) != len(rev_dirs):
            extra_failures.append(
                f"summary_row_count={len(summary_rows)} but tree_count={len(rev_dirs)}"
            )

    report_path = output_dir / "_validation_report.csv"
    with report_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_COLUMNS)
        writer.writeheader()
        for r in report_rows:
            writer.writerow(r)

    print(f"specs_validated={len(report_rows)}")
    print(f"specs_failed={fail_total}")
    print(f"golden_assertions_total={golden_total}")
    print(f"golden_assertions_failed={golden_failed}")
    print(f"negative_check_failures={negative_failed}")
    print(f"rule_line_fallbacks_total={fallback_warning_total}")
    print(f"report_csv={report_path}")
    for f in extra_failures:
        print(f"warning={f}", file=sys.stderr)

    if fail_total > 0 or golden_failed > 0 or negative_failed > 0 or extra_failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
