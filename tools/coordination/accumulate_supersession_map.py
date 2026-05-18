#!/usr/bin/env python3
"""
accumulate_supersession_map.py

Deterministically accumulates a cumulative Supersession_Map.csv from accepted
prior maps and the current Supersession_Delta.csv.

Usage:
  python3 tools/coordination/accumulate_supersession_map.py \\
    [--prior-map <prior>/Supersession_Map.csv]... \\
    [--delta <snapshot>/Supersession_Delta.csv]... \\
    --output-map <snapshot>/Supersession_Map.csv \\
    [--allow-empty] \\
    [--check-map <snapshot>/Supersession_Map.csv] \\
    [--output-findings <audit>/Supersession_Map_Findings.csv]

Inputs:
  --prior-map: optional accepted prior cumulative maps; repeatable.
  --delta: current SCA Supersession_Delta.csv; repeatable and optional when
    an SCA introduces no new supersession rows.
  --check-map: optional existing cumulative map to compare against generated
    output for audit verification.

Outputs:
  Canonical cumulative CSV at --output-map and optional findings CSV. The tool
  is idempotent and writes only declared output paths.

Scope boundary:
  Reads only the supplied supersession CSV files. Does not modify source
  authorities, decomposition files, KTY folders, or SCA deltas.

Exit codes:
  0 = output written and check passed / no check requested
  1 = fatal input / parsing error
  2 = check completed with blocking findings
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


SUPERSESSION_COLUMNS = [
    "AmendmentID",
    "DecisionID",
    "SupersededAuthorityRole",
    "SupersededAuthorityPath",
    "SupersededAuthorityRef",
    "SupersededFactKey",
    "SupersededFactTextOrValue",
    "OverrideType",
    "ReplacementFactTextOrValue",
    "AppliesToRoots",
    "AppliesToFacilities",
    "AppliesToSections",
    "Notes",
]


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    source: str
    message: str


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        header = [h.strip() for h in reader.fieldnames]
        rows: list[dict[str, str]] = []
        for row in reader:
            cleaned: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                cleaned[key.strip()] = "" if value is None else str(value).strip()
            rows.append(cleaned)
    return header, rows


def validate_header(path: Path, header: list[str]) -> None:
    missing = [column for column in SUPERSESSION_COLUMNS if column not in header]
    if missing:
        raise ValueError(f"{path} missing required columns: {', '.join(missing)}")


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {column: row.get(column, "").strip() for column in SUPERSESSION_COLUMNS}


def row_key(row: dict[str, str]) -> tuple[str, ...]:
    # Full-row key preserves same decision id when applicability or value changes.
    return tuple(row.get(column, "") for column in SUPERSESSION_COLUMNS)


def load_all(prior_maps: list[Path], deltas: list[Path], allow_empty: bool = False) -> list[dict[str, str]]:
    if not prior_maps and not deltas:
        if allow_empty:
            return []
        raise ValueError("At least one --prior-map or --delta input is required")
    merged: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for path in [*prior_maps, *deltas]:
        header, rows = read_csv_rows(path)
        validate_header(path, header)
        for row in rows:
            normalized = normalize_row(row)
            key = row_key(normalized)
            if key in seen:
                continue
            seen.add(key)
            merged.append(normalized)
    return merged


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUPERSESSION_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def compare_maps(generated_rows: list[dict[str, str]], check_map: Path) -> list[Finding]:
    _, existing_rows_raw = read_csv_rows(check_map)
    existing_rows = [normalize_row(row) for row in existing_rows_raw]
    generated_keys = {row_key(row) for row in generated_rows}
    existing_keys = {row_key(row) for row in existing_rows}

    findings: list[Finding] = []
    for key in sorted(generated_keys - existing_keys):
        findings.append(Finding(
            "CRITICAL",
            "MISSING_EXPECTED_ROW",
            str(check_map),
            f"Existing map is missing expected row: {dict(zip(SUPERSESSION_COLUMNS, key))}",
        ))
    for key in sorted(existing_keys - generated_keys):
        findings.append(Finding(
            "MAJOR",
            "UNEXPECTED_ROW",
            str(check_map),
            f"Existing map contains row not generated from supplied prior maps/delta: {dict(zip(SUPERSESSION_COLUMNS, key))}",
        ))
    return findings


def write_findings(path: Path, findings: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Severity", "Category", "Source", "Message"])
        writer.writeheader()
        for finding in findings:
            writer.writerow({
                "Severity": finding.severity,
                "Category": finding.category,
                "Source": finding.source,
                "Message": finding.message,
            })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Accumulate cumulative Supersession_Map.csv")
    parser.add_argument("--prior-map", action="append", type=Path, default=[], help="Prior accepted Supersession_Map.csv. Repeatable.")
    parser.add_argument("--delta", action="append", type=Path, default=[], help="Current Supersession_Delta.csv. Repeatable.")
    parser.add_argument("--output-map", required=True, type=Path, help="Output cumulative Supersession_Map.csv")
    parser.add_argument("--allow-empty", action="store_true", help="Permit header-only output when no prior maps or deltas exist")
    parser.add_argument("--check-map", type=Path, help="Optional existing map to compare against generated output")
    parser.add_argument("--output-findings", type=Path, help="Optional findings CSV")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = load_all(args.prior_map, args.delta, allow_empty=args.allow_empty)
        write_csv(args.output_map, rows)
        findings = compare_maps(rows, args.check_map) if args.check_map else []
        if args.output_findings:
            write_findings(args.output_findings, findings)
    except (FileNotFoundError, ValueError, OSError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    blocking = [f for f in findings if f.severity in {"CRITICAL", "MAJOR"}]
    print(f"Wrote supersession map: {args.output_map}")
    print(f"Rows: {len(rows)}")
    print(f"Findings: {len(findings)} total, {len(blocking)} blocking")
    for finding in findings:
        print(f"{finding.severity}: {finding.category}: {finding.message}")
    return 2 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
