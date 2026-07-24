#!/usr/bin/env python3
"""Finalize an evidence-rich migration candidate into a clean production SoW."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    BEGIN_RE,
    END_MARKER,
    SowError,
    parse_sow,
    parse_sow_text,
    sha256_bytes,
    validate_document,
)

REPORT_SCHEMA = "chirality-sow-finalization/v1"
CONTROL_COMMENT_RE = re.compile(
    r"^<!-- (?P<key>migration-authority|pilot-variance|issued-preparation-[a-z0-9-]+): (?P<value>.*?) -->$"
)


def _quoted(lines: list[str]) -> list[str]:
    return [">" if line == "" else f"> {line}" for line in lines]


def finalize_candidate_text(path: Path, text: str) -> tuple[str, dict[str, object]]:
    """Return clean production text and the externalized migration evidence."""
    evidence_doc = parse_sow_text(path, text)
    issues = validate_document(evidence_doc)
    if issues:
        raise SowError("evidence candidate validation failed: " + "; ".join(issues))

    lines = text.splitlines()
    output: list[str] = []
    blocks: list[dict[str, object]] = []
    control: dict[str, object] = {}
    wording_updates = 0
    index = 0
    while index < len(lines):
        begin = BEGIN_RE.match(lines[index])
        if begin:
            try:
                metadata = json.loads(begin.group(1))
            except json.JSONDecodeError as exc:
                raise SowError(f"invalid source marker JSON at line {index + 1}") from exc
            end = index + 1
            while end < len(lines) and lines[end] != END_MARKER:
                end += 1
            if end == len(lines):
                raise SowError(f"unterminated source marker at line {index + 1}")
            source_lines = lines[index + 1 : end]
            output.extend(_quoted(source_lines))
            blocks.append(
                {
                    **metadata,
                    "preserved_text_sha256": sha256_bytes("\n".join(source_lines).encode("utf-8")),
                }
            )
            index = end + 1
            continue

        control_comment = CONTROL_COMMENT_RE.match(lines[index])
        if control_comment:
            key, value = control_comment.group("key"), control_comment.group("value")
            if key in control:
                previous = control[key]
                control[key] = [previous, value] if not isinstance(previous, list) else [*previous, value]
            else:
                control[key] = value
            index += 1
            continue

        finalized_line = re.sub(
            r"\bmigration candidate\b",
            "Scope of Work",
            lines[index],
            flags=re.IGNORECASE,
        )
        if finalized_line != lines[index]:
            wording_updates += 1
        output.append(finalized_line)
        index += 1

    if not blocks:
        raise SowError("evidence candidate contains no source mapping blocks")
    if not ({"migration-authority", "pilot-variance"} & control.keys()):
        raise SowError("evidence candidate does not bind migration authority or pilot variance")

    production = "\n".join(output).rstrip() + "\n"
    forbidden = (
        "sow-source-begin",
        "sow-source-end",
        "migration-authority:",
        "pilot-variance:",
        "issued-preparation-",
    )
    residue = [token for token in forbidden if token in production]
    if residue:
        raise SowError("production output retains migration-control metadata: " + ", ".join(residue))
    if re.search(r"\bmigration candidate\b", production, re.IGNORECASE):
        raise SowError("production output retains migration-candidate language")
    production_doc = parse_sow_text(path, production)
    production_issues = validate_document(production_doc)
    if production_issues:
        raise SowError("finalized production validation failed: " + "; ".join(production_issues))

    report = {
        "schema": REPORT_SCHEMA,
        "evidence_candidate_sha256": evidence_doc.sha256,
        "production_scope_of_work_sha256": production_doc.sha256,
        "migration_control": control,
        "source_blocks": blocks,
        "source_block_count": len(blocks),
        "production_wording_update_count": wording_updates,
    }
    return production, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        evidence = args.evidence_candidate.resolve()
        output = args.output.resolve()
        report_path = args.report.resolve()
        if len({evidence, output, report_path}) != 3:
            raise SowError("evidence candidate, production output, and report must be distinct paths")
        production, report = finalize_candidate_text(evidence, evidence.read_text(encoding="utf-8"))
        output.parent.mkdir(parents=True, exist_ok=True)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(production, encoding="utf-8", newline="\n")
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        # Re-read the durable output before declaring success.
        durable = parse_sow(output)
        if durable.sha256 != report["production_scope_of_work_sha256"]:
            raise SowError("durable production output does not match finalization report")
        print(f"PASS blocks={report['source_block_count']} output={output}")
        return 0
    except (OSError, UnicodeError, SowError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
