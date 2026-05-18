#!/usr/bin/env python3
"""
check_body_thinness.py — Smoke test for section body underdevelopment signals.

Purpose:
    Structural indicator scan for draft DBM sections.  NOT an adequacy judgment:
    computes factual line counts, table counts, heading counts, and mapped
    artifact density, then flags deterministic structural signals.

Inputs:
    --draft        (required) Path to draft DBM markdown file.
    --section-map  (optional) Path to Section_Map.csv for mapped artifact counts.
    --schema       (optional) Path to Publication_Schema.md for expected table classes.
    --output       (optional) CSV output path; default stdout.

Output CSV columns:
    SectionID, SectionHeading, DraftLineNumber, TotalLines, NonBlankLines,
    TableRows, HeadingCount, MappedPrimaryKAs, MappedSupportingKAs,
    DensityRatio, ExpectedTableClasses, FoundTableCount, Signals

Exit codes:
    0 = success (signals encoded in output rows)
    1 = fatal input error

Example:
    python3 tools/review/check_body_thinness.py \
        --draft package/Rewritten_DBM.md \
        --section-map _Planning/Section_Map.csv \
        --schema _Planning/Publication_Schema.md \
        --output thinness.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
SECTION_ID_RE = re.compile(r"\b(SEC-\d+)\b")

OUTPUT_COLUMNS = [
    "SectionID",
    "SectionHeading",
    "DraftLineNumber",
    "TotalLines",
    "NonBlankLines",
    "TableRows",
    "HeadingCount",
    "MappedPrimaryKAs",
    "MappedSupportingKAs",
    "DensityRatio",
    "ExpectedTableClasses",
    "FoundTableCount",
    "Signals",
]

REQUIRED_SCHEMA_COLUMNS = ["SectionID", "SectionOrder", "SectionTitle", "SectionType"]


def fatal(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        fatal(f"File not found: {path}")
    except PermissionError:
        fatal(f"Permission denied: {path}")


def parse_markdown_tables(text: str) -> List[List[Dict[str, str]]]:
    """Parse all pipe-delimited markdown tables from text."""
    tables: List[List[Dict[str, str]]] = []
    block: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("|") and line.strip().endswith("|"):
            block.append(line)
            continue
        if block:
            table = _parse_table_block(block)
            if table:
                tables.append(table)
            block = []
    if block:
        table = _parse_table_block(block)
        if table:
            tables.append(table)
    return tables


def _parse_table_block(lines: Sequence[str]) -> List[Dict[str, str]]:
    if len(lines) < 2:
        return []
    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(header) != len(separator):
        return []
    if not all(re.fullmatch(r":?-{1,}:?", cell or "") for cell in separator):
        return []
    rows: List[Dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < len(header):
            cells.extend([""] * (len(header) - len(cells)))
        if len(cells) > len(header):
            cells = cells[: len(header)]
        rows.append({header[idx]: cells[idx] for idx in range(len(header))})
    return rows


def find_table_with_columns(text: str, required_columns: Sequence[str]) -> Optional[List[Dict[str, str]]]:
    for table in parse_markdown_tables(text):
        if not table:
            continue
        keys = set(table[0].keys())
        if all(col in keys for col in required_columns):
            return table
    return None


def parse_sections(draft_path: Path) -> List[Dict]:
    """Parse draft into top-level sections by heading hierarchy.

    Returns a list of section dicts with keys:
      section_id, heading, line_number, level, body_lines (list of (line_no, text))
    """
    text = read_text(draft_path)
    lines = text.splitlines()

    sections = []
    current = None

    for idx, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            # Extract SectionID if present
            sid_match = SECTION_ID_RE.search(heading_text)
            section_id = sid_match.group(1) if sid_match else ""

            if level == 1:
                # New top-level section
                if current is not None:
                    sections.append(current)
                current = {
                    "section_id": section_id,
                    "heading": heading_text,
                    "line_number": idx,
                    "level": level,
                    "body_lines": [],
                    "sub_headings": 0,
                }
            elif current is not None:
                # Sub-heading within current section
                current["sub_headings"] += 1
                current["body_lines"].append((idx, line))
            else:
                # Heading before any top-level section
                if current is None:
                    current = {
                        "section_id": section_id,
                        "heading": heading_text,
                        "line_number": idx,
                        "level": level,
                        "body_lines": [],
                        "sub_headings": 0,
                    }
        elif current is not None:
            current["body_lines"].append((idx, line))

    if current is not None:
        sections.append(current)

    return sections


def count_tables_in_body(body_lines: List[Tuple[int, str]]) -> int:
    """Count discrete markdown tables in section body lines.

    A table is a contiguous block of pipe-delimited rows with a valid
    header + separator.
    """
    table_count = 0
    in_table = False

    for line_no, line in body_lines:
        is_table_line = TABLE_ROW_RE.match(line) is not None
        if is_table_line and not in_table:
            in_table = True
            table_count += 1
        elif not is_table_line:
            in_table = False

    return table_count


def parse_section_map_counts(section_map_path: Path) -> Dict[str, Tuple[int, int]]:
    """Parse Section_Map.csv and return per-section (primary_count, supporting_count)."""
    counts: Dict[str, Tuple[int, int]] = defaultdict(lambda: (0, 0))

    try:
        with section_map_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = (row.get("SectionID") or "").strip()
                role = (row.get("MappingRole") or "").strip().upper()
                if not sid:
                    continue
                primary, supporting = counts[sid]
                if role == "PRIMARY":
                    counts[sid] = (primary + 1, supporting)
                elif role == "SUPPORTING":
                    counts[sid] = (primary, supporting + 1)
    except FileNotFoundError:
        fatal(f"Section map not found: {section_map_path}")
    except PermissionError:
        fatal(f"Permission denied: {section_map_path}")

    return dict(counts)


def parse_schema_tables(schema_path: Path) -> Dict[str, str]:
    """Parse Publication_Schema.md for ExpectedDesignBasisTables per section.

    Returns dict of SectionID -> expected table classes string.
    """
    text = read_text(schema_path)
    table = find_table_with_columns(text, REQUIRED_SCHEMA_COLUMNS)
    if not table:
        return {}

    result = {}
    for row in table:
        sid = (row.get("SectionID") or "").strip()
        # Look for ExpectedDesignBasisTables column or similar
        expected = (row.get("ExpectedDesignBasisTables") or "").strip()
        if not expected:
            expected = (row.get("ExpectedOutputShape") or "").strip()
        if sid:
            result[sid] = expected if expected else "NONE_EXPECTED"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke test for section body underdevelopment signals."
    )
    parser.add_argument("--draft", required=True, help="Path to draft DBM markdown file")
    parser.add_argument("--section-map", help="Path to Section_Map.csv for mapped artifact counts")
    parser.add_argument("--schema", help="Path to Publication_Schema.md for expected table classes")
    parser.add_argument("--output", help="CSV output path; default stdout")
    args = parser.parse_args()

    draft_path = Path(args.draft).expanduser().resolve()
    if not draft_path.is_file():
        fatal(f"Draft file not found: {draft_path}")

    # Parse optional inputs
    section_map_counts: Optional[Dict[str, Tuple[int, int]]] = None
    if args.section_map:
        sm_path = Path(args.section_map).expanduser().resolve()
        if not sm_path.is_file():
            fatal(f"Section map not found: {sm_path}")
        section_map_counts = parse_section_map_counts(sm_path)

    schema_tables: Optional[Dict[str, str]] = None
    if args.schema:
        schema_path = Path(args.schema).expanduser().resolve()
        if not schema_path.is_file():
            fatal(f"Schema file not found: {schema_path}")
        schema_tables = parse_schema_tables(schema_path)

    # Parse draft into sections
    sections = parse_sections(draft_path)

    output_rows = []
    for section in sections:
        sid = section["section_id"]
        heading = section["heading"]
        line_number = section["line_number"]
        body_lines = section["body_lines"]

        total_lines = len(body_lines) + 1  # +1 for the heading itself
        non_blank = sum(1 for _, l in body_lines if l.strip()) + 1  # heading is non-blank
        table_rows = sum(1 for _, l in body_lines if TABLE_ROW_RE.match(l))
        heading_count = section["sub_headings"]
        found_table_count = count_tables_in_body(body_lines)

        # Mapped KA counts
        mapped_primary = ""
        mapped_supporting = ""
        density_ratio = ""
        if section_map_counts is not None and sid:
            primary, supporting = section_map_counts.get(sid, (0, 0))
            mapped_primary = str(primary)
            mapped_supporting = str(supporting)
            if primary > 0:
                density_ratio = f"{non_blank / primary:.1f}"

        # Expected table classes
        expected_table_classes = ""
        if schema_tables is not None and sid:
            expected_table_classes = schema_tables.get(sid, "NONE_EXPECTED")

        # Compute signals
        signals = []
        if (
            density_ratio
            and mapped_primary
            and float(density_ratio) < 3.0
            and int(mapped_primary) > 5
        ):
            signals.append("LOW_DENSITY")

        if (
            schema_tables is not None
            and sid
            and expected_table_classes
            and expected_table_classes != "NONE_EXPECTED"
            and found_table_count == 0
        ):
            signals.append("NO_TABLES_WHERE_EXPECTED")

        if non_blank < 5:
            signals.append("FEWER_THAN_5_BODY_LINES")

        if (
            mapped_primary
            and int(mapped_primary) > 20
            and non_blank < 50
        ):
            signals.append("HIGH_KA_COUNT_LOW_BODY")

        output_rows.append({
            "SectionID": sid,
            "SectionHeading": heading,
            "DraftLineNumber": str(line_number),
            "TotalLines": str(total_lines),
            "NonBlankLines": str(non_blank),
            "TableRows": str(table_rows),
            "HeadingCount": str(heading_count),
            "MappedPrimaryKAs": mapped_primary,
            "MappedSupportingKAs": mapped_supporting,
            "DensityRatio": density_ratio,
            "ExpectedTableClasses": expected_table_classes,
            "FoundTableCount": str(found_table_count),
            "Signals": ";".join(signals),
        })

    # Write output
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
            writer.writeheader()
            for row in output_rows:
                writer.writerow(row)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)

    return 0


if __name__ == "__main__":
    sys.exit(main())
