#!/usr/bin/env python3
"""
extract_claims.py — Locate engineering values, design parameters, configuration
statements, and controlled terms in completed DBM text.

Purpose:
    Deterministic extraction of numeric engineering claims, table-cell values,
    configuration statements, and TBD-adjacent values from a draft DBM markdown
    file.  Factual and non-judgmental: extracts and classifies but does not
    judge materiality, adequacy, or engineering obligation.

Inputs:
    --draft        (required) Path to draft DBM markdown file.
    --section-map  (optional) Path to Section_Map.csv for section boundary hints.
    --output       (optional) CSV output path; default stdout.

Output CSV columns:
    ClaimID, SectionHeading, DraftLineNumber, RawText, ExtractedValue,
    Unit, ContextType, NearestTerm

Exit codes:
    0 = success (signals encoded in output rows)
    1 = fatal input error

Example:
    python3 tools/review/extract_claims.py \
        --draft package/Rewritten_DBM.md \
        --output claims.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

# Engineering value with unit (case-insensitive)
UNIT_VALUE_RE = re.compile(
    r"\b(\d+(?:[,.]?\d+)*)\s*"
    r"(kPag|psig|kPad|SCFM|SCM/H|MMSCFD|degC|degF|°C|°F|m|mm|ft|in|%|kW|hp|MW|BTU|MMBTU|psi|bar|barg)\b",
    re.IGNORECASE,
)

# Configuration statements: NxM% patterns
CONFIG_NXM_RE = re.compile(r"(\d+)\s*[x\u00d7]\s*(\d+)\s*%", re.IGNORECASE)

# Named configuration terms
CONFIG_TERMS_RE = re.compile(
    r"\b(lead[\s-]?lag|forced[\s-]?draft|induced[\s-]?draft)\b",
    re.IGNORECASE,
)

# Pipe-delimited table row
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")

# Table separator row
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")

# TBD/TBC pattern
TBD_RE = re.compile(r"\b(TBD|TBC|to be determined|to be confirmed)\b", re.IGNORECASE)

# Numeric value (for table cell scanning)
NUMERIC_RE = re.compile(r"\b\d+(?:[,.]?\d+)*\b")

OUTPUT_COLUMNS = [
    "ClaimID",
    "SectionHeading",
    "DraftLineNumber",
    "RawText",
    "ExtractedValue",
    "Unit",
    "ContextType",
    "NearestTerm",
]


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


def find_nearest_term(text: str, match_start: int, match_end: int) -> str:
    """Find the nearest non-numeric, non-unit word cluster in the same text.

    Looks for the closest meaningful word(s) near the matched value.
    """
    # Strip units and numeric tokens, look for the nearest word cluster
    # Search in a window around the match
    window_start = max(0, match_start - 80)
    window_end = min(len(text), match_end + 80)
    context = text[window_start:window_end]

    # Remove the matched portion conceptually; find word clusters
    words_before = text[window_start:match_start].strip()
    words_after = text[match_end:window_end].strip()

    # Clean up pipe chars for table contexts
    words_before = words_before.replace("|", " ").strip()
    words_after = words_after.replace("|", " ").strip()

    # Extract meaningful words (not numbers, not units, not punctuation)
    unit_set = {
        "kpag", "psig", "kpad", "scfm", "scm/h", "mmscfd", "degc", "degf",
        "m", "mm", "ft", "in", "kw", "hp", "mw", "btu", "mmbtu", "psi",
        "bar", "barg", "x", "tbd", "tbc",
    }

    def extract_words(s: str) -> List[str]:
        tokens = re.findall(r"[A-Za-z][\w/-]*", s)
        return [t for t in tokens if t.lower() not in unit_set and not t.isdigit()]

    # Prefer words before the value (typically the parameter name)
    before_words = extract_words(words_before)
    if before_words:
        # Take last 1-4 words before the value
        return " ".join(before_words[-4:])

    after_words = extract_words(words_after)
    if after_words:
        return " ".join(after_words[:4])

    return ""


def extract_table_cell_claims(
    line_no: int, line: str, section_heading: str
) -> List[Dict[str, str]]:
    """Extract claims from pipe-delimited table cells."""
    claims = []
    if TABLE_SEP_RE.match(line):
        return claims

    cells = line.strip().strip("|").split("|")
    for cell in cells:
        cell_text = cell.strip()
        if not cell_text:
            continue

        # Look for unit values in table cells
        for m in UNIT_VALUE_RE.finditer(cell_text):
            nearest = find_nearest_term(line, m.start() + (len(line) - len(line.lstrip())), m.end())
            claims.append({
                "SectionHeading": section_heading,
                "DraftLineNumber": str(line_no),
                "RawText": cell_text[:200],
                "ExtractedValue": m.group(1),
                "Unit": m.group(2),
                "ContextType": "TABLE_CELL",
                "NearestTerm": nearest,
            })

    return claims


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locate engineering values, design parameters, and configuration statements in DBM text."
    )
    parser.add_argument("--draft", required=True, help="Path to draft DBM markdown file")
    parser.add_argument("--section-map", help="Path to Section_Map.csv for section boundary hints")
    parser.add_argument("--output", help="CSV output path; default stdout")
    args = parser.parse_args()

    draft_path = Path(args.draft).expanduser().resolve()
    if not draft_path.is_file():
        fatal(f"Draft file not found: {draft_path}")

    text = read_text(draft_path)
    lines = text.splitlines()

    # Parse into sections by heading hierarchy
    current_heading = "(preamble)"
    claims: List[Dict[str, str]] = []

    for idx, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            current_heading = heading_match.group(2).strip()
            continue

        stripped = line.strip()
        if not stripped:
            continue

        # Check if this is a table row
        is_table_row = TABLE_ROW_RE.match(line) is not None

        if is_table_row:
            table_claims = extract_table_cell_claims(idx, line, current_heading)
            claims.extend(table_claims)
            # Also check for config patterns in table rows
            for cm in CONFIG_NXM_RE.finditer(stripped):
                nearest = find_nearest_term(stripped, cm.start(), cm.end())
                claims.append({
                    "SectionHeading": current_heading,
                    "DraftLineNumber": str(idx),
                    "RawText": stripped[:200],
                    "ExtractedValue": cm.group(0),
                    "Unit": "",
                    "ContextType": "CONFIGURATION",
                    "NearestTerm": nearest,
                })
            continue

        # Prose scanning: engineering values with units
        for m in UNIT_VALUE_RE.finditer(stripped):
            # Check if this is TBD-adjacent
            context_type = "PROSE_VALUE"
            if TBD_RE.search(stripped):
                # Check proximity: TBD within 100 chars of numeric value
                tbd_match = TBD_RE.search(stripped)
                if tbd_match and abs(tbd_match.start() - m.start()) < 100:
                    context_type = "TBD_VALUE"

            nearest = find_nearest_term(stripped, m.start(), m.end())
            claims.append({
                "SectionHeading": current_heading,
                "DraftLineNumber": str(idx),
                "RawText": stripped[:200],
                "ExtractedValue": m.group(1),
                "Unit": m.group(2),
                "ContextType": context_type,
                "NearestTerm": nearest,
            })

        # Configuration statements: NxM%
        for cm in CONFIG_NXM_RE.finditer(stripped):
            nearest = find_nearest_term(stripped, cm.start(), cm.end())
            claims.append({
                "SectionHeading": current_heading,
                "DraftLineNumber": str(idx),
                "RawText": stripped[:200],
                "ExtractedValue": cm.group(0),
                "Unit": "",
                "ContextType": "CONFIGURATION",
                "NearestTerm": nearest,
            })

        # Configuration terms: lead-lag, forced draft, induced draft
        for ct in CONFIG_TERMS_RE.finditer(stripped):
            nearest = find_nearest_term(stripped, ct.start(), ct.end())
            claims.append({
                "SectionHeading": current_heading,
                "DraftLineNumber": str(idx),
                "RawText": stripped[:200],
                "ExtractedValue": ct.group(0),
                "Unit": "",
                "ContextType": "CONFIGURATION",
                "NearestTerm": nearest,
            })

        # TBD-adjacent values: line has both numeric + TBD/TBC within 100 chars
        # (only if not already captured as PROSE_VALUE with TBD)
        if TBD_RE.search(stripped) and NUMERIC_RE.search(stripped):
            tbd_m = TBD_RE.search(stripped)
            num_m = NUMERIC_RE.search(stripped)
            if tbd_m and num_m and abs(tbd_m.start() - num_m.start()) < 100:
                # Check if we already have a unit-value claim for this line as TBD_VALUE
                already_captured = any(
                    c["DraftLineNumber"] == str(idx) and c["ContextType"] == "TBD_VALUE"
                    for c in claims
                )
                if not already_captured:
                    nearest = find_nearest_term(stripped, num_m.start(), num_m.end())
                    claims.append({
                        "SectionHeading": current_heading,
                        "DraftLineNumber": str(idx),
                        "RawText": stripped[:200],
                        "ExtractedValue": num_m.group(0),
                        "Unit": "",
                        "ContextType": "TBD_VALUE",
                        "NearestTerm": nearest,
                    })

    # Assign sequential ClaimIDs
    output_rows = []
    for i, claim in enumerate(claims, start=1):
        row = {"ClaimID": f"C-{i:03d}"}
        row.update(claim)
        output_rows.append(row)

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
