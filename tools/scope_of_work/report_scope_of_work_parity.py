#!/usr/bin/env python3
"""Verify source-range coverage and text parity for a candidate ScopeOfWork.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    LEGACY_FILES,
    SowError,
    demote_headings,
    iter_source_blocks,
    parse_sow,
    resolve_production_format,
    sha256_file,
    validate_document,
)
from finalize_scope_of_work import finalize_candidate_text


def normalized(text: str) -> str:
    return text.replace("\r\n", "\n").rstrip("\n")


def build_report(sow: Path, source_dir: Path, production_sow: Path | None = None) -> dict[str, object]:
    doc = parse_sow(sow)
    issues = validate_document(doc)
    checks: list[dict[str, object]] = []
    coverage: dict[str, set[int]] = {name: set() for name in LEGACY_FILES}
    if issues:
        return {"schema": "chirality-sow-parity/v1", "pass": False, "issues": issues, "checks": checks}
    for metadata, target_text in iter_source_blocks(doc.body):
        filename = str(metadata.get("file", ""))
        source = source_dir / filename
        start = int(metadata.get("line_start", 0))
        end = int(metadata.get("line_end", 0))
        check_issues: list[str] = []
        if filename not in coverage:
            check_issues.append("unexpected source file")
        elif not source.is_file():
            check_issues.append("source missing")
        else:
            source_lines = source.read_text(encoding="utf-8").splitlines()
            if start < 1 or end < start or end > len(source_lines):
                check_issues.append("invalid source line range")
            else:
                expected = "\n".join(source_lines[start - 1 : end])
                if normalized(target_text) != normalized(demote_headings(expected)):
                    check_issues.append("target text differs from source range")
                coverage[filename].update(range(start, end + 1))
            if sha256_file(source) != metadata.get("source_sha256"):
                check_issues.append("source hash mismatch")
        checks.append(
            {
                "source_file": filename,
                "line_start": start,
                "line_end": end,
                "target_id": metadata.get("target_id"),
                "disposition": metadata.get("disposition"),
                "pass": not check_issues,
                "issues": check_issues,
            }
        )
    for filename in LEGACY_FILES:
        source = source_dir / filename
        if not source.is_file():
            issues.append(f"missing source: {filename}")
            continue
        expected_lines = set(range(1, len(source.read_text(encoding="utf-8").splitlines()) + 1))
        missing = sorted(expected_lines - coverage[filename])
        if missing:
            issues.append(f"unmapped source lines in {filename}: {missing[:10]}" + ("..." if len(missing) > 10 else ""))
    if not checks:
        issues.append("no source mappings found")
    if any(not check["pass"] for check in checks):
        issues.append("one or more source mapping checks failed")
    production_sha = doc.sha256
    schema = "chirality-sow-parity/v1"
    if production_sow is not None:
        schema = "chirality-sow-parity/v2"
        try:
            expected, finalization = finalize_candidate_text(sow, doc.raw)
            actual = production_sow.read_text(encoding="utf-8")
            if actual != expected:
                issues.append("production ScopeOfWork.md is not the deterministic finalization of the evidence candidate")
            production_doc = parse_sow(production_sow)
            production_issues = validate_document(production_doc)
            issues.extend(f"production: {issue}" for issue in production_issues)
            production_sha = production_doc.sha256
            if production_sha != finalization["production_scope_of_work_sha256"]:
                issues.append("production hash differs from finalization report basis")
        except (OSError, UnicodeError, SowError, ValueError) as exc:
            issues.append(f"production finalization check failed: {exc}")
    return {
        "schema": schema,
        "evidence_candidate": sow.name,
        "evidence_candidate_sha256": doc.sha256,
        "production_scope_of_work": production_sow.name if production_sow else sow.name,
        "production_scope_of_work_sha256": production_sha,
        "pass": not issues,
        "issues": issues,
        "checks": checks,
        "source_files": {name: sha256_file(source_dir / name) for name in LEGACY_FILES if (source_dir / name).is_file()},
    }


def markdown(report: dict[str, object]) -> str:
    rows = [
        "# Scope-of-Work Parity Report",
        "",
        f"- Verdict: **{'PASS' if report['pass'] else 'FAIL'}**",
        f"- Production Scope-of-Work SHA-256: `{report.get('production_scope_of_work_sha256', 'unavailable')}`",
        f"- Evidence-candidate SHA-256: `{report.get('evidence_candidate_sha256', 'unavailable')}`",
        f"- Mapping checks: {len(report.get('checks', []))}",
        "",
        "## Issues",
        "",
    ]
    issues = report.get("issues", [])
    rows.extend([f"- {issue}" for issue in issues] if issues else ["- none"])
    rows.append("")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope-of-work", type=Path, required=True)
    parser.add_argument("--production-scope-of-work", type=Path)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    args = parser.parse_args()
    try:
        resolution = resolve_production_format(
            args.scope_of_work.parent,
            isolated_migration=args.isolated_migration,
            migration_authority=args.migration_authority,
        )
        if resolution.state not in {"SOW_V1", "MIGRATION_DUAL"} or not resolution.valid:
            raise SowError(f"format state is {resolution.state}: {'; '.join(resolution.issues)}")
        report = build_report(args.scope_of_work, args.source_dir, args.production_scope_of_work)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.output_md:
            args.output_md.parent.mkdir(parents=True, exist_ok=True)
            args.output_md.write_text(markdown(report), encoding="utf-8", newline="\n")
        print(("PASS" if report["pass"] else "FAIL") + f" checks={len(report['checks'])}")
        return 0 if report["pass"] else 1
    except (OSError, UnicodeError, SowError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
