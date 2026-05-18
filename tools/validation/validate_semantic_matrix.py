#!/usr/bin/env python3
"""Validate Chirality semantic matrix artifacts for one deliverable."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CANONICAL_A = {
    "normative": ["prescriptive direction", "mandatory practice", "compliance determination", "regulatory audit"],
    "operative": ["procedural direction", "practical execution", "performance assessment", "process audit"],
    "evaluative": ["value orientation", "merit application", "worth determination", "quality appraisal"],
}

CANONICAL_B = {
    "data": ["essential fact", "adequate evidence", "comprehensive record", "reliable measurement"],
    "information": ["essential signal", "adequate context", "comprehensive account", "coherent message"],
    "knowledge": ["fundamental understanding", "competent expertise", "thorough mastery", "coherent understanding"],
    "wisdom": ["essential discernment", "adequate judgment", "holistic insight", "principled reasoning"],
}

EXPECTED_DIMS = {
    "C": (3, 4),
    "F": (3, 4),
    "D": (3, 4),
    "K": (4, 3),
    "G": (3, 4),
    "X": (4, 4),
    "T": (4, 4),
    "E": (4, 4),
}

WORK_REQUIRED = {"C", "F", "D", "X", "E"}
MATRIX_ORDER = ["A", "B", "C", "F", "D", "K", "G", "X", "T", "E"]
SUMMARY_ORDER = ["C", "F", "D", "K", "G", "X", "T", "E"]


@dataclass(frozen=True)
class Finding:
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one deliverable _SEMANTIC.md file.")
    parser.add_argument("deliverable_path", help="Path to a deliverable folder")
    parser.add_argument("--json", action="store_true", help="Reserved for future machine-readable output")
    return parser.parse_args()


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def extract_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## Matrix ([A-Z])\b.*$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        key = match.group(1)
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[key] = text[start:end]
    return sections


def extract_result_table(section: str) -> tuple[list[str], dict[str, list[str]]] | None:
    marker = re.search(r"^### Result\s*$", section, flags=re.MULTILINE)
    if not marker:
        return None
    lines = section[marker.end():].splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return None

    header = split_table_row(table_lines[0])
    separator = split_table_row(table_lines[1])
    if len(header) < 2 or not is_separator_row(separator):
        return None

    columns = [cell.strip("* ") for cell in header[1:]]
    rows: dict[str, list[str]] = {}
    for line in table_lines[2:]:
        cells = split_table_row(line)
        if not cells or is_separator_row(cells):
            continue
        row_label = cells[0].strip("* ")
        rows[row_label] = cells[1:]
    return columns, rows


def extract_first_table(section: str) -> tuple[list[str], dict[str, list[str]]] | None:
    table_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return None
    header = split_table_row(table_lines[0])
    separator = split_table_row(table_lines[1])
    if len(header) < 2 or not is_separator_row(separator):
        return None
    columns = [cell.strip("* ") for cell in header[1:]]
    rows: dict[str, list[str]] = {}
    for line in table_lines[2:]:
        cells = split_table_row(line)
        if not cells or is_separator_row(cells):
            continue
        row_label = cells[0].strip("* ")
        rows[row_label] = cells[1:]
    return columns, rows


def validate_canonical_matrix(name: str, table: tuple[list[str], dict[str, list[str]]] | None) -> list[Finding]:
    expected = CANONICAL_A if name == "A" else CANONICAL_B
    expected_cols = (
        ["guiding", "applying", "judging", "reviewing"]
        if name == "A"
        else ["necessity", "sufficiency", "completeness", "consistency"]
    )
    findings: list[Finding] = []
    if table is None:
        return [Finding(f"MISSING_MATRIX_{name}", f"Matrix {name} result table is missing")]
    cols, rows = table
    if cols != expected_cols:
        findings.append(Finding(f"BAD_MATRIX_{name}_COLUMNS", f"Matrix {name} columns do not match canonical values"))
    if rows != expected:
        findings.append(Finding(f"BAD_MATRIX_{name}_VALUES", f"Matrix {name} values do not match canonical values"))
    return findings


def validate_result_table(name: str, table: tuple[list[str], dict[str, list[str]]] | None) -> list[Finding]:
    findings: list[Finding] = []
    if table is None:
        return [Finding(f"MISSING_MATRIX_{name}_RESULT", f"Matrix {name} result table is missing")]

    cols, rows = table
    expected_rows, expected_cols = EXPECTED_DIMS[name]
    if len(rows) != expected_rows or len(cols) != expected_cols:
        findings.append(
            Finding(
                f"BAD_MATRIX_{name}_DIMENSIONS",
                f"Matrix {name} dimensions are {len(rows)}x{len(cols)}, expected {expected_rows}x{expected_cols}",
            )
        )

    for row_label, values in rows.items():
        if len(values) != len(cols):
            findings.append(Finding(f"BAD_MATRIX_{name}_ROW_WIDTH", f"{name}[{row_label}] has wrong width"))
        for col, value in zip(cols, values):
            normalized = value.strip()
            if not normalized:
                findings.append(Finding(f"EMPTY_MATRIX_{name}_CELL", f"{name}[{row_label},{col}] is empty"))
            if "∩" in normalized or "Σ" in normalized:
                findings.append(Finding(f"ALGEBRA_LEAK_{name}", f"{name}[{row_label},{col}] contains algebra notation"))
            if re.search(r"\w\s+\+\s+\w", normalized):
                findings.append(Finding(f"OPERATOR_LEAK_{name}", f"{name}[{row_label},{col}] contains leaked + operator"))
            if len(normalized) > 80:
                findings.append(Finding(f"LONG_CELL_{name}", f"{name}[{row_label},{col}] exceeds 80 characters"))
            if len(normalized.split()) > 5:
                findings.append(Finding(f"VERBOSE_CELL_{name}", f"{name}[{row_label},{col}] is not a 2-5 word phrase"))
            if row_label.lower() in normalized.lower().split() or col.lower() in normalized.lower().split():
                findings.append(Finding(f"AXIS_TOKEN_LEAK_{name}", f"{name}[{row_label},{col}] repeats an axis token"))
    return findings


def validate_work_section(name: str, section: str) -> list[Finding]:
    if name not in WORK_REQUIRED:
        return []
    required = [
        "Intermediate collection",
        "Step 1 - Axis anchor",
        "Step 2 - Projected contributors",
        "Step 3 - Centroid attractor",
    ]
    findings: list[Finding] = []
    for marker in required:
        if marker not in section:
            findings.append(Finding(f"MISSING_{name}_WORK", f"Matrix {name} lacks {marker} work"))
    result = extract_result_table(section)
    if result:
        _, rows = result
        expected_cells = sum(len(values) for values in rows.values())
        explicit_cells = len(re.findall(rf"\| {re.escape(name)}\[", section))
        if explicit_cells < expected_cells:
            findings.append(
                Finding(
                    f"INCOMPLETE_{name}_WORK",
                    f"Matrix {name} has work for {explicit_cells} cells, expected at least {expected_cells}",
                )
            )

        work_rows = [
            split_table_row(line)
            for line in section.splitlines()
            if line.strip().startswith(f"| {name}[")
        ]
        for row in work_rows:
            if len(row) < 5:
                findings.append(Finding(f"MALFORMED_{name}_WORK_ROW", f"Matrix {name} has malformed interpretation row"))
                continue
            cell, intermediate, anchor, projections, centroid = row[:5]
            if " * " not in intermediate:
                findings.append(Finding(f"MISSING_{name}_INTERMEDIATE_PRODUCTS", f"{cell} lacks explicit * products"))
            if " * " not in anchor:
                findings.append(Finding(f"MISSING_{name}_ANCHOR_PRODUCT", f"{cell} lacks explicit axis-anchor product"))
            if " * " not in projections:
                findings.append(Finding(f"MISSING_{name}_PROJECTIONS", f"{cell} lacks explicit projected contributor products"))
            if not re.search(r"centroid", centroid, flags=re.IGNORECASE):
                findings.append(Finding(f"MISSING_{name}_CENTROID", f"{cell} lacks centroid selection wording"))
    return findings


def validate_semantic_file(deliverable_path: Path) -> list[Finding]:
    semantic_path = deliverable_path / "_SEMANTIC.md"
    if not semantic_path.is_file():
        return [Finding("MISSING_FILE", f"{semantic_path} does not exist")]

    text = semantic_path.read_text(encoding="utf-8", errors="replace")
    findings: list[Finding] = []

    if "**Inputs Read:**" not in text:
        findings.append(Finding("MISSING_INPUTS_READ", "_SEMANTIC.md lacks Inputs Read provenance"))
    for filename in ["_CONTEXT.md", "_STATUS.md", "Datasheet.md", "Specification.md", "Guidance.md", "Procedure.md"]:
        if filename not in text:
            findings.append(Finding("MISSING_INPUT_REF", f"Inputs Read does not list {filename}"))
    if "**Audit:** PASS" not in text and "Audit: PASS" not in text:
        findings.append(Finding("MISSING_AUDIT_PASS", "_SEMANTIC.md lacks audit PASS"))
    if "## Matrix Summary" not in text:
        findings.append(Finding("MISSING_MATRIX_SUMMARY", "_SEMANTIC.md lacks Matrix Summary"))

    section_keys = [match.group(1) for match in re.finditer(r"^## Matrix ([A-Z])\b", text, flags=re.MULTILINE)]
    if section_keys[: len(MATRIX_ORDER)] != MATRIX_ORDER:
        findings.append(Finding("BAD_MATRIX_ORDER", f"Matrix order is {section_keys}, expected prefix {MATRIX_ORDER}"))

    sections = extract_sections(text)
    for name in MATRIX_ORDER:
        if name not in sections:
            findings.append(Finding(f"MISSING_MATRIX_{name}", f"Matrix {name} section is missing"))

    findings.extend(validate_canonical_matrix("A", extract_first_table(sections.get("A", ""))))
    findings.extend(validate_canonical_matrix("B", extract_first_table(sections.get("B", ""))))
    for name in SUMMARY_ORDER:
        section = sections.get(name, "")
        table = extract_result_table(section)
        findings.extend(validate_result_table(name, table))
        findings.extend(validate_work_section(name, section))

    summary = text.split("## Matrix Summary", 1)[1] if "## Matrix Summary" in text else ""
    for name in SUMMARY_ORDER:
        if f"### {name} -" not in summary:
            findings.append(Finding("MISSING_SUMMARY_MATRIX", f"Matrix Summary lacks {name}"))

    return findings


def main() -> int:
    args = parse_args()
    if args.json:
        print("ERROR: --json is not implemented for this validator", file=sys.stderr)
        return 2

    deliverable_path = Path(args.deliverable_path)
    findings = validate_semantic_file(deliverable_path)
    if findings:
        print(f"INVALID: {deliverable_path / '_SEMANTIC.md'}")
        for finding in findings:
            print(f"  [{finding.category}] {finding.message}")
        return 1

    print(f"VALID: {deliverable_path / '_SEMANTIC.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
