#!/usr/bin/env python3
"""
scan_deliverable_consistency.py
Scan one deliverable for lightweight, deterministic consistency issues.

Checks:
  1. Missing core metadata files
  2. Missing four-document kit files
  3. Unresolved markers such as TBD / ASSUMPTION / CONFLICT:
  4. Simple identity mismatches against the deliverable folder ID
  5. Candidate unsourced numeric lines for human review

Usage:
    python3 scan_deliverable_consistency.py <deliverable_path>
    python3 scan_deliverable_consistency.py <deliverable_path> --output-json report.json
    python3 scan_deliverable_consistency.py <deliverable_path> --focus-doc Specification.md

Outputs:
    JSON report to stdout or a file path passed via --output-json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CORE_FILES = [
    "_STATUS.md",
    "_CONTEXT.md",
    "_DEPENDENCIES.md",
    "_REFERENCES.md",
    "_SEMANTIC.md",
]

FOUR_DOCS = [
    "Datasheet.md",
    "Guidance.md",
    "Procedure.md",
    "Specification.md",
]

MARKER_PATTERNS = {
    "TBD": re.compile(r"\bTBD\b", re.IGNORECASE),
    "ASSUMPTION": re.compile(r"\bASSUMPTION\b", re.IGNORECASE),
    "CONFLICT": re.compile(r"\bCONFLICT\s*:", re.IGNORECASE),
}

DELIVERABLE_ID_RE = re.compile(r"(?<![A-Za-z0-9])DEL-\d{3}-\d{2}(?![0-9])")
PACKAGE_ID_RE = re.compile(r"(?<![A-Za-z0-9])PKG-\d{3}(?![0-9])")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)$")
IDENTITY_HINT_RE = re.compile(
    r"\b(deliverable id|package id|document id|document number|deliverable number|package number|unit id)\b",
    re.IGNORECASE,
)
NUMERIC_TOKEN_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|psi|kpa|mpa|pa|bar|kw|w|v|a|amp|amps|hz|rpm|mm|cm|m|km|in|ft|gpm|l/s|lpm|kg|lb|lbs|n|kn|c|f|°c|°f|days?|hours?|hrs?|minutes?|min)\b",
    re.IGNORECASE,
)
PLAIN_NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
SOURCE_HINT_RE = re.compile(
    r"\b(source|reference|references|ref\.?|per|basis)\b|"
    r"\[[^\]]+\]\([^)]+\)|"
    r"\[[0-9]+\]",
    re.IGNORECASE,
)


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan one deliverable for consistency issues.")
    parser.add_argument("deliverable_path", help="Path to the deliverable folder")
    parser.add_argument("--output-json", help="Write JSON report to this path instead of stdout")
    parser.add_argument(
        "--focus-doc",
        dest="focus_docs",
        action="append",
        default=[],
        help="Restrict scanning to specific production docs (repeatable)",
    )
    parser.add_argument(
        "--strictness",
        choices=["conservative", "aggressive"],
        default="conservative",
        help="How readily to flag candidate unsourced numeric lines",
    )
    parser.add_argument(
        "--max-findings",
        type=int,
        default=10,
        help="Soft cap per finding category",
    )
    parser.add_argument(
        "--check-identity",
        type=parse_bool,
        default=True,
        help="Whether to flag simple DEL/PKG identity mismatches (default: true)",
    )
    parser.add_argument(
        "--check-unsourced-numerics",
        type=parse_bool,
        default=True,
        help="Whether to flag candidate unsourced numeric lines (default: true)",
    )
    return parser.parse_args()


def infer_unit_id(deliverable_dir: Path) -> tuple[str | None, str | None]:
    deliverable_match = DELIVERABLE_ID_RE.search(deliverable_dir.name)
    deliverable_id = deliverable_match.group(0) if deliverable_match else None
    package_id = None
    if deliverable_id:
        package_id = f"PKG-{deliverable_id.split('-')[1]}"
    return deliverable_id, package_id


def find_production_docs(deliverable_dir: Path, focus_docs: list[str]) -> list[Path]:
    if focus_docs:
        requested = [deliverable_dir / name for name in focus_docs]
        return [path for path in requested if path.is_file()]

    standard_docs = [deliverable_dir / name for name in FOUR_DOCS if (deliverable_dir / name).is_file()]
    if standard_docs:
        return standard_docs

    return [
        path
        for path in sorted(deliverable_dir.glob("*.md"))
        if path.is_file() and not path.name.startswith("_")
    ]


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def cap(items: list[dict], max_findings: int) -> tuple[list[dict], int]:
    if max_findings < 1:
        return [], len(items)
    return items[:max_findings], max(0, len(items) - max_findings)


def iter_lines(text: str) -> list[tuple[int, str]]:
    return [(idx, line.rstrip("\n")) for idx, line in enumerate(text.splitlines(), start=1)]


def detect_markers(doc_path: Path, text: str) -> list[dict]:
    findings = []
    for line_number, line in iter_lines(text):
        stripped = line.strip()
        if not stripped:
            continue
        for marker_type, pattern in MARKER_PATTERNS.items():
            if pattern.search(stripped):
                findings.append(
                    {
                        "type": marker_type,
                        "file": doc_path.name,
                        "line": line_number,
                        "excerpt": stripped[:240],
                    }
                )
    return findings


def detect_identity_mismatches(
    doc_path: Path,
    text: str,
    expected_deliverable_id: str | None,
    expected_package_id: str | None,
) -> list[dict]:
    findings = []
    if not expected_deliverable_id and not expected_package_id:
        return findings

    for line_number, line in iter_lines(text):
        stripped = line.strip()
        if not stripped or stripped.startswith("```"):
            continue
        if not IDENTITY_HINT_RE.search(stripped):
            continue

        seen_deliverables = sorted(set(DELIVERABLE_ID_RE.findall(stripped)))
        seen_packages = sorted(set(PACKAGE_ID_RE.findall(stripped)))

        mismatched_deliverables = []
        mismatched_packages = []

        if expected_deliverable_id:
            mismatched_deliverables = [value for value in seen_deliverables if value != expected_deliverable_id]
        if expected_package_id:
            mismatched_packages = [value for value in seen_packages if value != expected_package_id]

        if mismatched_deliverables or mismatched_packages:
            findings.append(
                {
                    "file": doc_path.name,
                    "line": line_number,
                    "expected_deliverable_id": expected_deliverable_id,
                    "expected_package_id": expected_package_id,
                    "found_other_deliverable_ids": mismatched_deliverables,
                    "found_other_package_ids": mismatched_packages,
                    "excerpt": stripped[:240],
                }
            )
    return findings


def likely_unsourced_numeric_line(line: str, strictness: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("#", "|", ">")):
        return False
    if stripped.startswith("```") or set(stripped) <= {"-", ":", "|"}:
        return False
    if DELIVERABLE_ID_RE.search(stripped) or PACKAGE_ID_RE.search(stripped):
        return False
    if SOURCE_HINT_RE.search(stripped):
        return False

    heading_match = HEADING_RE.match(stripped)
    heading_text = heading_match.group(1) if heading_match else stripped
    if re.fullmatch(r"\d+(?:\.\d+)*", heading_text):
        return False

    if NUMERIC_TOKEN_RE.search(stripped):
        return True

    if strictness == "aggressive" and len(stripped) <= 220 and PLAIN_NUMBER_RE.search(stripped):
        return True

    return False


def detect_unsourced_numerics(doc_path: Path, text: str, strictness: str) -> list[dict]:
    findings = []
    for line_number, line in iter_lines(text):
        if likely_unsourced_numeric_line(line, strictness):
            findings.append(
                {
                    "file": doc_path.name,
                    "line": line_number,
                    "excerpt": line.strip()[:240],
                }
            )
    return findings


def main() -> int:
    args = parse_args()
    deliverable_dir = Path(args.deliverable_path).expanduser().resolve()

    if not deliverable_dir.exists():
        print(f"ERROR: Deliverable path does not exist: {deliverable_dir}", file=sys.stderr)
        return 1
    if not deliverable_dir.is_dir():
        print(f"ERROR: Deliverable path is not a directory: {deliverable_dir}", file=sys.stderr)
        return 1

    expected_deliverable_id, expected_package_id = infer_unit_id(deliverable_dir)
    missing_core_files = [name for name in CORE_FILES if not (deliverable_dir / name).is_file()]
    missing_four_documents = [name for name in FOUR_DOCS if not (deliverable_dir / name).is_file()]
    scanned_docs = find_production_docs(deliverable_dir, args.focus_docs)

    marker_findings = []
    identity_mismatches = []
    candidate_unsourced_numerics = []

    for doc_path in scanned_docs:
        text = safe_read(doc_path)
        marker_findings.extend(detect_markers(doc_path, text))
        if args.check_identity:
            identity_mismatches.extend(
                detect_identity_mismatches(doc_path, text, expected_deliverable_id, expected_package_id)
            )
        if args.check_unsourced_numerics:
            candidate_unsourced_numerics.extend(detect_unsourced_numerics(doc_path, text, args.strictness))

    total_marker_findings = len(marker_findings)
    total_identity_mismatches = len(identity_mismatches)
    total_candidate_unsourced_numerics = len(candidate_unsourced_numerics)

    marker_findings, marker_truncated = cap(marker_findings, args.max_findings)
    identity_mismatches, identity_truncated = cap(identity_mismatches, args.max_findings)
    candidate_unsourced_numerics, numeric_truncated = cap(candidate_unsourced_numerics, args.max_findings)

    report = {
        "deliverable_path": str(deliverable_dir),
        "folder_name": deliverable_dir.name,
        "production_unit_id": expected_deliverable_id,
        "package_id": expected_package_id,
        "strictness": args.strictness,
        "scanned_docs": [path.name for path in scanned_docs],
        "missing_core_files": missing_core_files,
        "missing_four_documents": missing_four_documents,
        "marker_findings": marker_findings,
        "identity_mismatches": identity_mismatches,
        "candidate_unsourced_numerics": candidate_unsourced_numerics,
        "summary": {
            "scanned_doc_count": len(scanned_docs),
            "missing_core_file_count": len(missing_core_files),
            "missing_four_document_count": len(missing_four_documents),
            "marker_finding_count": total_marker_findings,
            "identity_mismatch_count": total_identity_mismatches,
            "candidate_unsourced_numeric_count": total_candidate_unsourced_numerics,
            "truncated": {
                "marker_findings": marker_truncated,
                "identity_mismatches": identity_truncated,
                "candidate_unsourced_numerics": numeric_truncated,
            },
        },
    }

    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output_json:
        output_path = Path(args.output_json).expanduser().resolve()
        output_path.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)

    return 0


if __name__ == "__main__":
    sys.exit(main())
