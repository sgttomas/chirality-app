#!/usr/bin/env python3
"""Derive a stable REVIEW acceptance checklist from validated ScopeOfWork AC records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    SCHEMA,
    SowDocument,
    SowError,
    load_catalog,
    parse_sow,
    resolve_production_format,
    section_text,
    validate_document,
)

CHECKLIST_SCHEMA = "chirality-review-checklist/v1"
TOOL_VERSION = "1"


def definition_records(doc: SowDocument, prefixes: tuple[str, ...], width: int) -> dict[str, dict[str, object]]:
    prefix_pattern = "|".join(re.escape(prefix) for prefix in prefixes)
    pattern = re.compile(
        rf"^(?:[-*]\s+\*\*|#{{3,6}}\s+)(?P<id>(?:{prefix_pattern})-\d{{{width}}})(?:\*\*)?\s+[—-]\s+(?P<text>\S(?:.*\S)?)\s*$"
    )
    records: dict[str, dict[str, object]] = {}
    current_section = ""
    in_source_block = False
    for line_number, line in enumerate(doc.raw.splitlines(), 1):
        if line.startswith("<!-- sow-source-begin "):
            in_source_block = True
            continue
        if line == "<!-- sow-source-end -->":
            in_source_block = False
            continue
        if in_source_block:
            continue
        if re.match(r"^ {0,3}>", line):
            continue
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current_section = heading.group(1).strip()
        match = pattern.match(line)
        if match:
            records[match.group("id")] = {
                "id": match.group("id"),
                "text": match.group("text"),
                "section": current_section,
                "line": line_number,
            }
    return records


def matrix_links(doc: SowDocument, width: int) -> dict[str, dict[str, list[str]]]:
    ac_re = re.compile(rf"\bAC-\d{{{width}}}\b")
    ver_re = re.compile(rf"\bVER-\d{{{width}}}\b")
    out_re = re.compile(rf"\bOUT-\d{{{width}}}\b")
    links: dict[str, dict[str, list[str]]] = {}
    matrix = section_text(doc.body, "Output and Evaluation Matrix")
    for line in matrix.splitlines():
        if not line.strip().startswith("|") or re.match(r"^\s*\|?\s*:?-", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6 or not out_re.fullmatch(cells[0]):
            continue
        acceptance_refs = ac_re.findall(cells[3])
        verification_refs = ver_re.findall(cells[4])
        human_review = re.fullmatch(r"HUMAN_REVIEW:\s*(\S(?:.*\S)?)", cells[4])
        for ac_id in acceptance_refs:
            item = links.setdefault(ac_id, {"outputs": [], "verifications": [], "human_reviews": []})
            if cells[0] not in item["outputs"]:
                item["outputs"].append(cells[0])
            for ver_id in verification_refs:
                if ver_id not in item["verifications"]:
                    item["verifications"].append(ver_id)
            if human_review and human_review.group(1) not in item["human_reviews"]:
                item["human_reviews"].append(human_review.group(1))
    return links


def derive(doc: SowDocument, format_state: str, migration_authority: str) -> dict[str, object]:
    catalog = load_catalog()
    definitions = definition_records(doc, ("AC", "VER"), catalog.width)
    links = matrix_links(doc, catalog.width)
    deliverable_id = str(doc.frontmatter["deliverable_id"])
    ac_ids = [item for item in doc.definitions if item.startswith("AC-")]
    items: list[dict[str, object]] = []

    for ac_id in ac_ids:
        criterion = definitions.get(ac_id)
        if criterion is None:
            raise SowError(f"acceptance criterion has no extractable one-line definition: {ac_id}")
        linkage = links.get(ac_id)
        if linkage is None:
            raise SowError(f"acceptance criterion is not linked by the output/evaluation matrix: {ac_id}")
        verification: list[dict[str, object]] = []
        for ver_id in linkage["verifications"]:
            record = definitions.get(ver_id)
            if record is None:
                raise SowError(f"linked verification has no extractable one-line definition: {ver_id}")
            verification.append(
                {
                    "kind": "VER",
                    "id": ver_id,
                    "qualified_id": f"{deliverable_id}-{ver_id}",
                    "text": record["text"],
                    "source_line": record["line"],
                    "source_section": record["section"],
                }
            )
        for method in linkage["human_reviews"]:
            verification.append({"kind": "HUMAN_REVIEW", "method": method})
        if not verification:
            raise SowError(f"acceptance criterion has no linked VER or HUMAN_REVIEW method: {ac_id}")
        items.append(
            {
                "id": ac_id,
                "qualified_id": f"{deliverable_id}-{ac_id}",
                "text": criterion["text"],
                "source_identity": {
                    "document": "ScopeOfWork.md",
                    "sha256": doc.sha256,
                    "section": criterion["section"],
                    "line": criterion["line"],
                },
                "output_refs": linkage["outputs"],
                "verification": verification,
                "review_status": None,
            }
        )

    return {
        "schema": CHECKLIST_SCHEMA,
        "tool_version": TOOL_VERSION,
        "source": {
            "document": "ScopeOfWork.md",
            "sha256": doc.sha256,
            "schema": SCHEMA,
            "deliverable_id": deliverable_id,
            "package_id": str(doc.frontmatter["package_id"]),
            "format": format_state,
            "migration_authority": migration_authority or None,
        },
        "item_count": len(items),
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="ScopeOfWork.md or its deliverable directory")
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    parser.add_argument("--output", type=Path, help="Write checklist JSON here instead of stdout")
    args = parser.parse_args()

    deliverable = args.target if args.target.is_dir() else args.target.parent
    sow_path = deliverable / "ScopeOfWork.md" if args.target.is_dir() else args.target
    migration_authority = args.migration_authority
    try:
        resolution = resolve_production_format(
            deliverable,
            isolated_migration=args.isolated_migration,
            migration_authority=migration_authority,
        )
        if resolution.state not in {"SOW_V1", "MIGRATION_DUAL"} or not resolution.valid:
            detail = "; ".join(resolution.issues)
            raise SowError(
                f"format state is {resolution.state}; validated ScopeOfWork.md is required"
                + (f": {detail}" if detail else "")
            )
        if not sow_path.is_file():
            raise SowError(f"missing ScopeOfWork.md: {sow_path}")
        doc = parse_sow(sow_path)
        issues = validate_document(doc)
        if issues:
            raise SowError("invalid ScopeOfWork.md: " + "; ".join(issues))
        report = derive(doc, resolution.state, migration_authority)
        rendered = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, UnicodeError, SowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
