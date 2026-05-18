#!/usr/bin/env python3
"""
scan_tbd_markers.py — Locate TBD/TBC/ASSUMPTION markers with line numbers and
optional KB cross-reference.

Purpose:
    Deterministic scan for TBD, TBC, and ASSUMPTION markers in a draft DBM
    markdown file.  When a Section_Map.csv is provided, attempts fuzzy
    cross-referencing against Scoping.md Open Questions / TBD sections to
    report KB resolution status.  Factual and non-judgmental.

Inputs:
    --draft        (required) Path to draft DBM markdown file.
    --section-map  (optional) Path to Section_Map.csv for Scoping.md discovery.
    --domain-root  (optional) Domain root path for rebasing artifact paths.
    --output       (optional) CSV output path; default stdout.

Output CSV columns:
    MarkerID, MarkerType, DraftLineNumber, DraftContext, NearestSectionID,
    KBResolutionStatus, KBResolutionRef, Notes

Exit codes:
    0 = success (signals encoded in output rows)
    1 = fatal input error

Example:
    python3 tools/review/scan_tbd_markers.py \
        --draft package/Rewritten_DBM.md \
        --section-map _Planning/Section_Map.csv \
        --output tbd_markers.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

MARKER_PATTERNS = [
    ("TBD", re.compile(r"\bTBD\b", re.IGNORECASE)),
    ("TBC", re.compile(r"\bTBC\b", re.IGNORECASE)),
    ("TBD", re.compile(r"\bto be determined\b", re.IGNORECASE)),
    ("TBC", re.compile(r"\bto be confirmed\b", re.IGNORECASE)),
    ("ASSUMPTION", re.compile(r"\bASSUMPTION\b", re.IGNORECASE)),
    ("ASSUMPTION", re.compile(r"\bassumed\b", re.IGNORECASE)),
]

SECTION_ID_RE = re.compile(r"\b(SEC-\d+)\b")

OUTPUT_COLUMNS = [
    "MarkerID",
    "MarkerType",
    "DraftLineNumber",
    "DraftContext",
    "NearestSectionID",
    "KBResolutionStatus",
    "KBResolutionRef",
    "Notes",
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


def tokenize(s: str) -> set:
    """Tokenize a string into lowercase alphanumeric words."""
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def extract_kty_folders(section_map_path: Path) -> List[str]:
    """Extract unique KTY folder paths from Section_Map.csv ArtifactPath column."""
    folders = set()
    try:
        with section_map_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                artifact_path = (row.get("ArtifactPath") or "").strip()
                if artifact_path:
                    # Get the parent directory of the artifact (KTY folder)
                    p = Path(artifact_path)
                    parent = str(p.parent)
                    if parent and parent != ".":
                        folders.add(parent)
    except FileNotFoundError:
        fatal(f"Section map not found: {section_map_path}")
    except PermissionError:
        fatal(f"Permission denied: {section_map_path}")
    return sorted(folders)


def build_kb_registry(
    kty_folders: List[str], domain_root: Optional[Path]
) -> List[Tuple[str, str, str]]:
    """Build KB registry from Scoping.md files in KTY folders.

    Returns list of (kty_id, issue_text, resolution_status).
    """
    registry: List[Tuple[str, str, str]] = []
    seen_folders = set()

    for folder_path_str in kty_folders:
        folder_path = Path(folder_path_str)

        # Skip duplicates
        folder_key = str(folder_path)
        if folder_key in seen_folders:
            continue
        seen_folders.add(folder_key)

        scoping_path = folder_path / "Scoping.md"

        if not scoping_path.is_file():
            continue

        try:
            text = scoping_path.read_text(encoding="utf-8", errors="replace")
        except (PermissionError, OSError):
            continue

        kty_id = folder_path.name

        # Parse Open Questions / TBD section
        in_tbd_section = False
        for line in text.splitlines():
            stripped = line.strip()

            # Look for the Open Questions / TBD heading
            heading_match = HEADING_RE.match(line)
            if heading_match:
                heading_text = heading_match.group(2).strip().lower()
                if "open questions" in heading_text and ("tbd" in heading_text or "tbds" in heading_text):
                    in_tbd_section = True
                    continue
                elif in_tbd_section:
                    # A new heading ends the TBD section
                    in_tbd_section = False
                continue

            if not in_tbd_section:
                continue

            if not stripped or stripped.startswith("---"):
                continue

            # Determine resolution status
            if "~~" in stripped or "**RESOLVED**" in stripped:
                status = "RESOLVED"
            else:
                status = "UNRESOLVED"

            # Clean up the issue text for matching
            issue_text = re.sub(r"^[-*]\s*", "", stripped)
            issue_text = re.sub(r"~~(.+?)~~", r"\1", issue_text)  # Remove strikethrough markers
            issue_text = issue_text.strip()

            if issue_text:
                registry.append((kty_id, issue_text, status))

    return registry


def match_marker_to_kb(
    marker_text: str,
    kb_registry: List[Tuple[str, str, str]],
) -> Tuple[str, str]:
    """Match a draft marker against KB issues.

    Returns (resolution_status, resolution_ref).
    """
    if not kb_registry:
        return "NOT_IN_KB", ""

    marker_tokens = tokenize(marker_text)
    if not marker_tokens:
        return "NOT_IN_KB", ""

    best_score = 0.0
    best_kty = ""
    best_status = ""

    for kty_id, issue_text, status in kb_registry:
        issue_tokens = tokenize(issue_text)
        score = jaccard_similarity(marker_tokens, issue_tokens)
        if score > best_score:
            best_score = score
            best_kty = kty_id
            best_status = status

    if best_score >= 0.3:
        return best_status, best_kty

    return "NOT_IN_KB", ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Locate TBD/TBC/ASSUMPTION markers with line numbers and optional KB cross-reference."
    )
    parser.add_argument("--draft", required=True, help="Path to draft DBM markdown file")
    parser.add_argument("--section-map", help="Path to Section_Map.csv for Scoping.md discovery")
    parser.add_argument("--domain-root", help="Domain root path for rebasing artifact paths")
    parser.add_argument("--output", help="CSV output path; default stdout")
    args = parser.parse_args()

    draft_path = Path(args.draft).expanduser().resolve()
    if not draft_path.is_file():
        fatal(f"Draft file not found: {draft_path}")

    domain_root = None
    if args.domain_root:
        domain_root = Path(args.domain_root).expanduser().resolve()
        if not domain_root.is_dir():
            fatal(f"Domain root not found: {domain_root}")

    # Build KB registry if section map provided
    kb_registry: List[Tuple[str, str, str]] = []
    has_kb = False
    if args.section_map:
        sm_path = Path(args.section_map).expanduser().resolve()
        if not sm_path.is_file():
            fatal(f"Section map not found: {sm_path}")
        kty_folders = extract_kty_folders(sm_path)
        kb_registry = build_kb_registry(kty_folders, domain_root)
        has_kb = True

    # Read draft and scan for markers
    text = read_text(draft_path)
    lines = text.splitlines()

    current_section_heading = ""
    current_section_id = ""
    markers: List[Dict[str, str]] = []
    seen_markers: set = set()  # Deduplicate: (line_no, marker_type)

    for idx, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading_text = heading_match.group(2).strip()
            current_section_heading = heading_text
            # Try to extract SectionID from heading
            sid_match = SECTION_ID_RE.search(heading_text)
            if sid_match:
                current_section_id = sid_match.group(1)
            continue

        stripped = line.strip()
        if not stripped:
            continue

        for marker_type, pattern in MARKER_PATTERNS:
            if pattern.search(stripped):
                dedup_key = (idx, marker_type)
                if dedup_key in seen_markers:
                    continue
                seen_markers.add(dedup_key)

                # KB cross-reference
                if has_kb:
                    kb_status, kb_ref = match_marker_to_kb(stripped, kb_registry)
                else:
                    kb_status = "NO_KB_PROVIDED"
                    kb_ref = ""

                markers.append({
                    "MarkerType": marker_type,
                    "DraftLineNumber": str(idx),
                    "DraftContext": stripped[:200],
                    "NearestSectionID": current_section_id,
                    "KBResolutionStatus": kb_status,
                    "KBResolutionRef": kb_ref,
                    "Notes": "",
                })

    # Assign sequential MarkerIDs
    output_rows = []
    for i, marker in enumerate(markers, start=1):
        row = {"MarkerID": f"M-{i:03d}"}
        row.update(marker)
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
