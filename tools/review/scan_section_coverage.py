#!/usr/bin/env python3
"""
scan_section_coverage.py — Compare draft section headings against Publication_Schema.md.

Purpose:
    Deterministic coverage comparison between draft DBM headings and the approved
    section schema, optionally enriched by a run-specific Section_Map.csv.

Inputs:
    --draft        (required) Path to draft DBM markdown file.
    --schema       (required) Path to Publication_Schema.md.
    --section-map  (optional) Path to Section_Map.csv (run-specific authority).
    --output       (optional) CSV output path; default stdout.

Output CSV columns:
    SectionID, SectionTitle, SectionType, SectionOrder, CoverageStatus,
    DraftHeading, DraftLineNumber, AuthoritySource

Exit codes:
    0 = success (signals encoded in output rows)
    1 = fatal input error

Example:
    python3 tools/review/scan_section_coverage.py \
        --draft package/Rewritten_DBM.md \
        --schema _Planning/Publication_Schema.md \
        --section-map _Planning/Section_Map.csv \
        --output coverage.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

OUTPUT_COLUMNS = [
    "SectionID",
    "SectionTitle",
    "SectionType",
    "SectionOrder",
    "CoverageStatus",
    "DraftHeading",
    "DraftLineNumber",
    "AuthoritySource",
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


def find_table_with_columns(text: str, required_columns: Sequence[str]) -> List[Dict[str, str]]:
    for table in parse_markdown_tables(text):
        if not table:
            continue
        keys = set(table[0].keys())
        if all(col in keys for col in required_columns):
            return table
    fatal(f"Unable to find markdown table with required columns: {', '.join(required_columns)}")


def parse_schema_sections(schema_path: Path) -> List[Dict[str, str]]:
    """Parse Publication_Schema.md and return section definition rows."""
    text = read_text(schema_path)
    return find_table_with_columns(text, REQUIRED_SCHEMA_COLUMNS)


def parse_section_map_ids(section_map_path: Path) -> set:
    """Extract unique SectionID values from Section_Map.csv."""
    try:
        with section_map_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            ids = set()
            for row in reader:
                sid = (row.get("SectionID") or "").strip()
                if sid:
                    ids.add(sid)
            return ids
    except FileNotFoundError:
        fatal(f"Section map not found: {section_map_path}")
    except PermissionError:
        fatal(f"Permission denied: {section_map_path}")


def parse_draft_headings(draft_path: Path) -> List[Tuple[int, int, str]]:
    """Parse draft headings. Returns list of (line_number, level, heading_text)."""
    text = read_text(draft_path)
    headings = []
    for idx, line in enumerate(text.splitlines(), start=1):
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            headings.append((idx, level, heading_text))
    return headings


def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def tokenize(s: str) -> set:
    """Tokenize a string into lowercase alphanumeric words."""
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def match_section_to_headings(
    section: Dict[str, str],
    headings: List[Tuple[int, int, str]],
) -> Tuple[str, str, str]:
    """Try to match a schema section against draft headings.

    Returns (CoverageStatus, DraftHeading, DraftLineNumber).
    """
    section_id = section.get("SectionID", "").strip()
    section_title = section.get("SectionTitle", "").strip()
    section_order_raw = section.get("SectionOrder", "").strip()

    # Derive section number prefix for numeric matching
    section_number = None
    if section_order_raw:
        try:
            section_number = str(int(section_order_raw))
        except ValueError:
            pass

    best_fuzzy_score = 0.0
    best_fuzzy_heading = None
    best_fuzzy_line = None

    section_title_norm = normalize_whitespace(section_title).lower()
    section_title_tokens = tokenize(section_title)

    for line_no, level, heading_text in headings:
        heading_norm = normalize_whitespace(heading_text).lower()

        # Exact SectionID match: e.g., "SEC-01" appears in heading text
        if section_id and section_id.lower() in heading_norm:
            return "COVERED", heading_text, str(line_no)

        # Exact title match (case-insensitive, whitespace-normalized)
        if section_title_norm and section_title_norm == heading_norm:
            return "COVERED", heading_text, str(line_no)

        # Section-number prefix match (e.g., heading starts with "1.0" or "1.")
        if section_number:
            prefix_patterns = [
                f"{section_number}.0 ",
                f"{section_number}.0\t",
                f"{section_number}. ",
                f"{section_number} ",
                f"{section_number}.",
            ]
            heading_stripped = heading_text.strip()
            for pat in prefix_patterns:
                if heading_stripped.startswith(pat):
                    return "COVERED", heading_text, str(line_no)

        # Fuzzy match
        heading_tokens = tokenize(heading_text)
        score = jaccard_similarity(section_title_tokens, heading_tokens)
        if score > best_fuzzy_score:
            best_fuzzy_score = score
            best_fuzzy_heading = heading_text
            best_fuzzy_line = line_no

    if best_fuzzy_score >= 0.6:
        return "PARTIAL", best_fuzzy_heading, str(best_fuzzy_line)

    return "MISSING", "", ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare draft section headings against Publication_Schema.md."
    )
    parser.add_argument("--draft", required=True, help="Path to draft DBM markdown file")
    parser.add_argument("--schema", required=True, help="Path to Publication_Schema.md")
    parser.add_argument("--section-map", help="Path to Section_Map.csv (run-specific authority)")
    parser.add_argument("--output", help="CSV output path; default stdout")
    args = parser.parse_args()

    draft_path = Path(args.draft).expanduser().resolve()
    schema_path = Path(args.schema).expanduser().resolve()

    if not draft_path.is_file():
        fatal(f"Draft file not found: {draft_path}")
    if not schema_path.is_file():
        fatal(f"Schema file not found: {schema_path}")

    section_map_ids = None
    authority_source = "SCHEMA_ONLY"
    if args.section_map:
        sm_path = Path(args.section_map).expanduser().resolve()
        if not sm_path.is_file():
            fatal(f"Section map file not found: {sm_path}")
        section_map_ids = parse_section_map_ids(sm_path)
        authority_source = "SECTION_MAP"

    # Parse schema sections
    schema_sections = parse_schema_sections(schema_path)

    # Filter to run-specific sections if section map provided
    if section_map_ids is not None:
        expected_sections = [
            s for s in schema_sections
            if s.get("SectionID", "").strip() in section_map_ids
        ]
    else:
        expected_sections = schema_sections

    # Parse draft headings
    headings = parse_draft_headings(draft_path)

    # Track which headings are matched
    matched_heading_lines = set()
    output_rows = []

    for section in expected_sections:
        status, draft_heading, draft_line = match_section_to_headings(section, headings)
        if draft_line:
            matched_heading_lines.add(int(draft_line))
        output_rows.append({
            "SectionID": section.get("SectionID", "").strip(),
            "SectionTitle": section.get("SectionTitle", "").strip(),
            "SectionType": section.get("SectionType", "").strip(),
            "SectionOrder": section.get("SectionOrder", "").strip(),
            "CoverageStatus": status,
            "DraftHeading": draft_heading,
            "DraftLineNumber": draft_line,
            "AuthoritySource": authority_source,
        })

    # Find EXTRA headings (not matched to any expected section)
    for line_no, level, heading_text in headings:
        if line_no not in matched_heading_lines:
            output_rows.append({
                "SectionID": "",
                "SectionTitle": "",
                "SectionType": "",
                "SectionOrder": "",
                "CoverageStatus": "EXTRA",
                "DraftHeading": heading_text,
                "DraftLineNumber": str(line_no),
                "AuthoritySource": authority_source,
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
