#!/usr/bin/env python3
"""Validate Pass 3 disposition evidence for semantic-lensing warranted items."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SOW_COMMON_PATH = Path(__file__).resolve().parents[1] / "scope_of_work" / "common.py"
_spec = importlib.util.spec_from_file_location("chirality_scope_of_work_common", SOW_COMMON_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load Scope-of-Work common module: {SOW_COMMON_PATH}")
_common = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _common
_spec.loader.exec_module(_common)
PRODUCTION_FORMATS = _common.PRODUCTION_FORMATS
SowError = _common.SowError
require_requested_format = _common.require_requested_format
resolve_production_format = _common.resolve_production_format


ITEM_ID_RE = re.compile(r"\b([A-Z]-\d{3})\b")
LENS_ITEM_ROW_RE = re.compile(r"^\|\s*([A-Z]-\d{3})\s*\|")
FOUR_DOCS = ["Datasheet.md", "Specification.md", "Guidance.md", "Procedure.md"]
EVIDENCE_FILES = FOUR_DOCS + ["MEMORY.md", "_STATUS.md"]


@dataclass(frozen=True)
class Finding:
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate P3 disposition evidence for one deliverable.")
    parser.add_argument("deliverable_path", help="Path to a deliverable folder")
    parser.add_argument(
        "--production-format",
        choices=["AUTO", *PRODUCTION_FORMATS],
        default="AUTO",
    )
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    return parser.parse_args()


def parse_warranted_item_ids(lens_path: Path) -> list[str]:
    text = lens_path.read_text(encoding="utf-8", errors="replace")
    item_ids: list[str] = []
    for line in text.splitlines():
        match = LENS_ITEM_ROW_RE.match(line)
        if match:
            item_ids.append(match.group(1))
    return item_ids


def disposition_files(deliverable_path: Path, *, production_format: str = "LEGACY_FOUR_DOC") -> list[Path]:
    names = (["ScopeOfWork.md"] if production_format in {"SOW_V1", "MIGRATION_DUAL"} else FOUR_DOCS) + ["MEMORY.md", "_STATUS.md"]
    files = [deliverable_path / name for name in names if (deliverable_path / name).is_file()]
    run_records = deliverable_path / "_run_records"
    if run_records.is_dir():
        files.extend(sorted(run_records.glob("*.md")))
    return files


def item_ids_in_files(files: list[Path]) -> dict[str, set[Path]]:
    locations: dict[str, set[Path]] = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for item_id in ITEM_ID_RE.findall(text):
            locations.setdefault(item_id, set()).add(path)
    return locations


def validate_p3_disposition(deliverable_path: Path, *, production_format: str = "LEGACY_FOUR_DOC") -> list[Finding]:
    lens_path = deliverable_path / "_SEMANTIC_LENSING.md"
    if not lens_path.is_file():
        return [Finding("MISSING_LENS_REGISTER", f"{lens_path} does not exist")]

    warranted_ids = parse_warranted_item_ids(lens_path)
    findings: list[Finding] = []
    if not warranted_ids:
        return findings

    if len(warranted_ids) != len(set(warranted_ids)):
        findings.append(Finding("DUPLICATE_WARRANTED_ITEM", "Duplicate warranted item IDs found in _SEMANTIC_LENSING.md"))

    evidence_files = disposition_files(deliverable_path, production_format=production_format)
    if not evidence_files:
        findings.append(Finding("MISSING_DISPOSITION_EVIDENCE", "No production, MEMORY, STATUS, or run-record files found"))
        return findings

    evidence_ids = item_ids_in_files(evidence_files)
    expected = set(warranted_ids)
    for item_id in sorted(expected):
        if item_id not in evidence_ids:
            findings.append(Finding("MISSING_ITEM_DISPOSITION", f"{item_id} is not mentioned in P3 disposition evidence"))

    extras = sorted(item_id for item_id in evidence_ids if item_id not in expected)
    for item_id in extras:
        paths = ", ".join(str(path.relative_to(deliverable_path)) for path in sorted(evidence_ids[item_id]))
        findings.append(Finding("UNKNOWN_ITEM_REFERENCE", f"{item_id} is mentioned but is not a warranted item ({paths})"))

    return findings


def main() -> int:
    args = parse_args()
    deliverable_path = Path(args.deliverable_path)
    resolution = resolve_production_format(
        deliverable_path,
        isolated_migration=args.isolated_migration,
        migration_authority=args.migration_authority,
    )
    try:
        require_requested_format(resolution, args.production_format)
    except SowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not resolution.valid:
        print(f"ERROR: format state is {resolution.state}: {'; '.join(resolution.issues)}", file=sys.stderr)
        return 2
    findings = validate_p3_disposition(deliverable_path, production_format=resolution.state)
    if findings:
        print(f"INVALID: {deliverable_path}")
        for finding in findings:
            print(f"  [{finding.category}] {finding.message}")
        return 1

    print(f"VALID: {deliverable_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
