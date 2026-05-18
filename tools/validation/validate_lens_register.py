#!/usr/bin/env python3
"""Validate Chirality semantic lensing register artifacts for one deliverable."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


EXPECTED_COVERAGE = {"A": 12, "B": 16, "C": 12, "F": 12, "D": 12, "X": 16, "E": 16}
VALID_STATUS = {"NO_ITEMS", "HAS_ITEMS", "MATRIX_ERROR"}
VALID_TYPES = {
    "MissingSlot",
    "WeakStatement",
    "Conflict",
    "VerificationGap",
    "RationaleGap",
    "Normalization",
    "TBD_Question",
    "MatrixError",
}
REQUIRED_ITEM_COLUMNS = [
    "ItemID",
    "LensKey",
    "Type",
    "AppliesToDoc",
    "SuggestedEditDoc",
    "CandidateInfo",
    "WhyWarranted",
    "SourcePath",
    "SectionRef",
    "Contenders",
    "ProposedAuthority (PROPOSAL)",
    "HumanRuling",
]
GENERIC_NO_ITEM_PATTERNS = [
    re.compile(r"no incremental warranted edit", re.IGNORECASE),
    re.compile(r"no warranted items?", re.IGNORECASE),
    re.compile(r"already covered", re.IGNORECASE),
    re.compile(r"existing .* controls", re.IGNORECASE),
]


@dataclass(frozen=True)
class Finding:
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one deliverable _SEMANTIC_LENSING.md file.")
    parser.add_argument("deliverable_path", help="Path to a deliverable folder")
    return parser.parse_args()


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def iter_tables(section: str) -> list[tuple[list[str], list[list[str]]]]:
    lines = section.splitlines()
    tables: list[tuple[list[str], list[list[str]]]] = []
    idx = 0
    while idx < len(lines):
        if not lines[idx].strip().startswith("|"):
            idx += 1
            continue
        header = split_table_row(lines[idx])
        if idx + 1 >= len(lines) or not is_separator_row(split_table_row(lines[idx + 1])):
            idx += 1
            continue
        idx += 2
        rows: list[list[str]] = []
        while idx < len(lines) and lines[idx].strip().startswith("|"):
            cells = split_table_row(lines[idx])
            if cells and not is_separator_row(cells):
                rows.append(cells)
            idx += 1
        tables.append((header, rows))
    return tables


def extract_matrix_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## Matrix ([A-Z])\b.*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        key = match.group(1)
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[key] = text[start:end]
    return sections


def parse_summary_counts(text: str) -> dict[str, int]:
    summary = text.split("## Summary", 1)[1].split("## Matrix", 1)[0] if "## Summary" in text else ""
    counts: dict[str, int] = {}
    total = re.search(r"Total warranted items:\s*(\d+)", summary)
    if total:
        counts["TOTAL"] = int(total.group(1))
    for name in EXPECTED_COVERAGE:
        match = re.search(rf"\b{name}:\s*(\d+)", summary)
        if match:
            counts[name] = int(match.group(1))
    for item_type in VALID_TYPES:
        match = re.search(rf"\b{re.escape(item_type)}:\s*(\d+)", summary)
        if match:
            counts[item_type] = int(match.group(1))
    return counts


def validate_lens_register(deliverable_path: Path) -> list[Finding]:
    lens_path = deliverable_path / "_SEMANTIC_LENSING.md"
    if not lens_path.is_file():
        return [Finding("MISSING_FILE", f"{lens_path} does not exist")]

    text = lens_path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []

    if "**Inputs Read:**" not in text:
        findings.append(Finding("MISSING_INPUTS_READ", "_SEMANTIC_LENSING.md lacks Inputs Read"))
    if "## Summary" not in text:
        findings.append(Finding("MISSING_SUMMARY", "_SEMANTIC_LENSING.md lacks Summary"))

    sections = extract_matrix_sections(text)
    item_rows: list[dict[str, str]] = []
    matrix_item_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    repeated_no_item_notes: Counter[str] = Counter()

    for matrix, expected_count in EXPECTED_COVERAGE.items():
        section = sections.get(matrix)
        if not section:
            findings.append(Finding(f"MISSING_MATRIX_{matrix}", f"Matrix {matrix} section is missing"))
            continue

        tables = iter_tables(section)
        coverage_table = None
        warranted_table = None
        for header, rows in tables:
            if header[:7] == ["LensKey", "RowLabel", "ColLabel", "LensValue", "ItemCount", "CoverageStatus", "Notes"]:
                coverage_table = rows
            elif header == REQUIRED_ITEM_COLUMNS:
                warranted_table = rows

        if coverage_table is None:
            findings.append(Finding(f"MISSING_{matrix}_COVERAGE", f"Matrix {matrix} lacks Lens Coverage table"))
            continue

        if len(coverage_table) != expected_count:
            findings.append(
                Finding(
                    f"BAD_{matrix}_COVERAGE_COUNT",
                    f"Matrix {matrix} has {len(coverage_table)} coverage rows, expected {expected_count}",
                )
            )

        for row in coverage_table:
            if len(row) != 7:
                findings.append(Finding(f"BAD_{matrix}_COVERAGE_ROW", f"Matrix {matrix} has malformed coverage row"))
                continue
            lens_key, row_label, col_label, lens_value, item_count, status, notes = row
            if not lens_key.startswith(f"{matrix}:["):
                findings.append(Finding(f"BAD_{matrix}_LENSKEY", f"LensKey does not start with {matrix}: {lens_key}"))
            if not row_label or not col_label or not lens_value:
                findings.append(Finding(f"BAD_{matrix}_COVERAGE_VALUE", f"Coverage row has empty row/col/value: {lens_key}"))
            if status not in VALID_STATUS:
                findings.append(Finding(f"BAD_{matrix}_STATUS", f"{lens_key} has invalid CoverageStatus {status}"))
            if not item_count.isdigit():
                findings.append(Finding(f"BAD_{matrix}_ITEMCOUNT", f"{lens_key} ItemCount is not an integer"))
            elif status == "HAS_ITEMS":
                matrix_item_counts[matrix] += int(item_count)
            if status == "NO_ITEMS":
                note_key = notes.strip().lower()
                if note_key:
                    repeated_no_item_notes[note_key] += 1
                if any(pattern.search(notes) for pattern in GENERIC_NO_ITEM_PATTERNS):
                    findings.append(Finding("GENERIC_NO_ITEMS_NOTE", f"{lens_key} uses generic NO_ITEMS note: {notes}"))

        if warranted_table:
            for row in warranted_table:
                if len(row) != len(REQUIRED_ITEM_COLUMNS):
                    findings.append(Finding(f"BAD_{matrix}_ITEM_ROW", f"Matrix {matrix} has malformed warranted item row"))
                    continue
                item = dict(zip(REQUIRED_ITEM_COLUMNS, row))
                item_rows.append(item)
                item_matrix = item["ItemID"].split("-", 1)[0]
                matrix_item_counts[item_matrix] += 0 if matrix_item_counts[item_matrix] else 0
                type_counts[item["Type"]] += 1

                if item["Type"] not in VALID_TYPES:
                    findings.append(Finding("BAD_ITEM_TYPE", f"{item['ItemID']} has invalid Type {item['Type']}"))
                if not item["SourcePath"] or item["SourcePath"] == "NA":
                    findings.append(Finding("MISSING_ITEM_SOURCE", f"{item['ItemID']} lacks SourcePath"))
                if not item["SectionRef"] or item["SectionRef"] == "NA":
                    findings.append(Finding("MISSING_ITEM_SECTION", f"{item['ItemID']} lacks SectionRef"))
                if item["Type"] == "Conflict" and (item["Contenders"] in {"", "NA"} or item["HumanRuling"] != "TBD"):
                    findings.append(Finding("BAD_CONFLICT_ITEM", f"{item['ItemID']} conflict item lacks contenders or TBD ruling"))
                if not item["CandidateInfo"] or not item["WhyWarranted"]:
                    findings.append(Finding("EMPTY_ITEM_CONTENT", f"{item['ItemID']} lacks CandidateInfo or WhyWarranted"))

    for note, count in repeated_no_item_notes.items():
        if count >= 8:
            findings.append(Finding("REPEATED_NO_ITEMS_NOTE", f"NO_ITEMS note repeats {count} times: {note[:120]}"))

    summary_counts = parse_summary_counts(text)
    if summary_counts.get("TOTAL") != len(item_rows):
        findings.append(
            Finding(
                "BAD_SUMMARY_TOTAL",
                f"Summary total is {summary_counts.get('TOTAL')}, actual warranted rows {len(item_rows)}",
            )
        )
    actual_by_matrix = Counter(item["ItemID"].split("-", 1)[0] for item in item_rows)
    for matrix in EXPECTED_COVERAGE:
        if summary_counts.get(matrix, 0) != actual_by_matrix.get(matrix, 0):
            findings.append(
                Finding(
                    "BAD_SUMMARY_MATRIX_COUNT",
                    f"Summary {matrix} count is {summary_counts.get(matrix, 0)}, actual {actual_by_matrix.get(matrix, 0)}",
                )
            )
    for item_type in VALID_TYPES:
        if summary_counts.get(item_type, 0) != type_counts.get(item_type, 0):
            findings.append(
                Finding(
                    "BAD_SUMMARY_TYPE_COUNT",
                    f"Summary {item_type} count is {summary_counts.get(item_type, 0)}, actual {type_counts.get(item_type, 0)}",
                )
            )

    return findings


def main() -> int:
    args = parse_args()
    deliverable_path = Path(args.deliverable_path)
    findings = validate_lens_register(deliverable_path)
    if findings:
        print(f"INVALID: {deliverable_path / '_SEMANTIC_LENSING.md'}")
        for finding in findings:
            print(f"  [{finding.category}] {finding.message}")
        return 1

    print(f"VALID: {deliverable_path / '_SEMANTIC_LENSING.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
