#!/usr/bin/env python3
"""Create a lossless migration ScopeOfWork.md from one legacy four-document kit."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import (
    LEGACY_FILES,
    MIGRATION_AUTHORITY,
    SCHEMA,
    SowError,
    demote_headings,
    load_catalog,
    parse_sow_text,
    read_lifecycle_state,
    resolve_production_format,
    sha256_file,
    split_source_sections,
    validate_document,
)

ISSUED_ACCEPTED_BASIS_MAX_LENGTH = 512

SECTION_CONFIG = (
    ("Datasheet.md", "Deliverable Definition — Ontology", "CLM"),
    ("Specification.md", "Completion and Reliance Basis — Epistemology", "CLM"),
    ("Procedure.md", "Production and Verification Method — Praxeology", "CLM"),
    ("Guidance.md", "Governing Values and Decisions — Axiology", "CLM"),
)


def inline_list(values: list[str]) -> str:
    return "[" + ", ".join(values) + "]"


def validate_issued_accepted_basis(value: str) -> str:
    if (
        not value
        or value != value.strip()
        or len(value) > ISSUED_ACCEPTED_BASIS_MAX_LENGTH
        or any(character in "\r\n" or ord(character) < 32 or ord(character) == 127 for character in value)
        or "-->" in value
    ):
        raise SowError(
            "ISSUED preparation requires --issued-accepted-basis as an unpadded "
            f"single-line value of 1-{ISSUED_ACCEPTED_BASIS_MAX_LENGTH} safe characters"
        )
    return value


def convert(args: argparse.Namespace) -> str:
    deliverable = args.deliverable.resolve()
    migration_authority = args.migration_authority
    if not args.isolated_migration or migration_authority != MIGRATION_AUTHORITY:
        raise SowError(
            "dual-format conversion requires --isolated-migration and "
            f"--migration-authority {MIGRATION_AUTHORITY}"
        )
    initial = resolve_production_format(deliverable)
    if initial.state != "LEGACY_FOUR_DOC":
        if not (args.force and initial.state == "AMBIGUOUS"):
            raise SowError(f"conversion source must resolve as LEGACY_FOUR_DOC, found {initial.state}")
    state = read_lifecycle_state(deliverable)
    if state == "ISSUED":
        issued_accepted_basis = validate_issued_accepted_basis(args.issued_accepted_basis)
        if not re.fullmatch(r"[0-9a-f]{7,64}", args.issued_source_commit.strip()):
            raise SowError("ISSUED preparation requires --issued-source-commit <git-sha>")
        if args.issued_status_sha256.strip() != sha256_file(deliverable / "_STATUS.md"):
            raise SowError("ISSUED preparation status hash does not match _STATUS.md")
        try:
            source_bindings = dict(item.split("=", 1) for item in args.issued_source_sha256)
        except ValueError as exc:
            raise SowError("--issued-source-sha256 entries must be NAME=SHA256") from exc
        for name in LEGACY_FILES:
            if source_bindings.get(name) != sha256_file(deliverable / name):
                raise SowError(f"ISSUED preparation source hash mismatch or missing: {name}")
    elif state not in {"INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING"}:
        raise SowError(f"converter requires INITIALIZED or later pre-ISSUED lifecycle, found {state or 'UNKNOWN'}")
    target = deliverable / "ScopeOfWork.md"
    if target.exists() and not args.force:
        raise SowError(f"target exists; refuse overwrite without --force: {target}")
    if target.exists() and args.force:
        existing = target.read_text(encoding="utf-8")
        if f"<!-- migration-authority: {migration_authority} -->" not in existing:
            raise SowError("--force may overwrite only a candidate bound to the same migration authority")
    status = deliverable / "_STATUS.md"
    status_before = sha256_file(status)

    catalog = load_catalog()
    counters = {prefix: 1 for prefix in catalog.definitions}
    source_sections: dict[str, list[str]] = {}
    defined: dict[str, list[str]] = {}
    for filename, heading, prefix in SECTION_CONFIG:
        path = deliverable / filename
        source_sha = sha256_file(path)
        rendered: list[str] = []
        defined[filename] = []
        for line_start, line_end, source_heading, source_text in split_source_sections(
            path.read_text(encoding="utf-8")
        ):
            local_id = f"{prefix}-{counters[prefix]:03d}"
            counters[prefix] += 1
            defined[filename].append(local_id)
            marker = {
                "disposition": "PRESERVED",
                "file": filename,
                "line_end": line_end,
                "line_start": line_start,
                "source_sha256": source_sha,
                "target_id": local_id,
            }
            rendered.extend(
                [
                    f"### {local_id} — {source_heading}",
                    "",
                    "<!-- sow-source-begin " + json.dumps(marker, sort_keys=True, separators=(",", ":")) + " -->",
                    demote_headings(source_text),
                    "<!-- sow-source-end -->",
                    "",
                ]
            )
        source_sections[heading] = rendered

    out_id, ac_id, ver_id = "OUT-001", "AC-001", "VER-001"
    project_refs = args.project_scope_ref
    package_refs = args.package_objective_ref
    matrix_objectives = " ".join(project_refs + package_refs)
    lines = [
        "---",
        f"schema: {SCHEMA}",
        f"deliverable_id: {args.deliverable_id}",
        f"package_id: {args.package_id}",
        f"decomposition_basis: {args.decomposition_basis}",
        f"project_scope_refs: {inline_list(project_refs)}",
        f"package_objective_refs: {inline_list(package_refs)}",
        "---",
        "",
        f"# Scope of Work — {args.deliverable_id}",
        "",
        "## Purpose and Objective Traceability",
        "",
        f"This migration candidate defines `{args.deliverable_id}` in service of project scope {inline_list(project_refs)} and package objectives {inline_list(package_refs)}.",
        "",
        f"- **{out_id}** — {args.output_description}",
        "",
    ]
    for _, heading, _ in SECTION_CONFIG:
        lines.extend([f"## {heading}", ""])
        lines.extend(source_sections[heading])
        if heading == "Completion and Reliance Basis — Epistemology":
            lines.extend([f"- **{ac_id}** — {args.acceptance_criterion}", ""])
        if heading == "Production and Verification Method — Praxeology":
            lines.extend([f"- **{ver_id}** — {args.verification_method}", ""])
    first_req = defined["Specification.md"][0]
    lines.extend(
        [
            "## Output and Evaluation Matrix",
            "",
            "| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |",
            "|---|---|---|---|---|---|",
            f"| {out_id} | {matrix_objectives} | {first_req} | {ac_id} | {ver_id} | Claim map, parity report, and applicable verification evidence |",
            "",
            f"<!-- migration-authority: {migration_authority} -->",
            *(
                [
                    f"<!-- issued-preparation-accepted-basis: {issued_accepted_basis} -->",
                    f"<!-- issued-preparation-source-commit: {args.issued_source_commit.strip()} -->",
                    f"<!-- issued-preparation-status-sha256: {args.issued_status_sha256.strip()} -->",
                    *(f"<!-- issued-preparation-source-sha256: {name}={source_bindings[name]} -->" for name in LEGACY_FILES),
                ]
                if state == "ISSUED" else []
            ),
            "",
        ]
    )
    output = "\n".join(lines)
    issues = validate_document(parse_sow_from_text(target, output))
    if issues:
        raise SowError("generated migration candidate failed validation: " + "; ".join(issues))
    if sha256_file(status) != status_before:
        raise SowError("_STATUS.md changed during conversion; refusing output")
    return output


def parse_sow_from_text(target: Path, text: str):
    """Validate generated text using the production parser without writing the target."""
    return parse_sow_text(target, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deliverable", type=Path, required=True)
    parser.add_argument("--deliverable-id", required=True)
    parser.add_argument("--package-id", required=True)
    parser.add_argument("--decomposition-basis", required=True)
    parser.add_argument("--project-scope-ref", action="append", required=True)
    parser.add_argument("--package-objective-ref", action="append", required=True)
    parser.add_argument("--output-description", required=True)
    parser.add_argument("--acceptance-criterion", required=True)
    parser.add_argument("--verification-method", required=True)
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    parser.add_argument("--issued-source-commit", default="")
    parser.add_argument("--issued-accepted-basis", default="")
    parser.add_argument("--issued-status-sha256", default="")
    parser.add_argument("--issued-source-sha256", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        output = convert(args)
        target = args.deliverable / "ScopeOfWork.md"
        target.write_text(output, encoding="utf-8", newline="\n")
        print(target)
        return 0
    except (OSError, UnicodeError, SowError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
