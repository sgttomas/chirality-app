#!/usr/bin/env python3
"""
validate_kty_remediation_manifest.py

Deterministically validates a SCOPE_CHANGE KTY_Remediation_Manifest.csv.

Usage:
  python3 tools/validation/validate_kty_remediation_manifest.py \
    --manifest <snapshot>/KTY_Remediation_Manifest.csv \
    [--amendment-actions <snapshot>/Amendment_Actions.csv] \
    [--downstream-input <path>]... \
    [--workspace-root <package-root>] \
    [--output-findings <snapshot>/KTY_Remediation_Findings.csv]

Inputs:
  --manifest: required per-SCA KTY content action/evidence ledger.
  --amendment-actions: optional approved Amendment_Actions.csv for
    ContentAction assignment validation. Foreign-key SourceActionRef of
    the form `<AmendmentID>:<ActionSeq>` (e.g. `SCA-004:1`) is resolved
    against this register in addition to bare `ActionSeq`/`D-NNN` forms.
  --downstream-input: optional downstream allowlist/section-map/publication
    input file scanned for .Archive/ leakage; repeatable.
  --workspace-root: optional package-root override. EvidencePaths and
    ArchivePath that don't resolve under the manifest's snapshot folder
    are retried under this root. Defaults to the nearest ancestor of the
    manifest containing `_Sources/` or `_Decomposition/`.

Outputs:
  PASS/finding summary to stdout and optional findings CSV. The tool is
  idempotent and writes only --output-findings when provided.

Scope boundary:
  Reads only the supplied manifest, optional Amendment_Actions.csv, evidence
  paths referenced by the manifest, and optional downstream input files.
  Does not modify KTY folders, archives, manifests, or downstream inputs.

Exit codes:
  0 = valid, no blocking findings
  1 = fatal input / parsing error
  2 = validation completed with blocking findings
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = [
    "AmendmentID",
    "ManifestRowID",
    "SourceActionRef",
    "EntityType",
    "EntityID",
    "KTYID",
    "KTYPath",
    "AffectedSubjects",
    "AffectedHBK",
    "CanonicalRootName",
    "FacilityID",
    "ContentAction",
    "TaskSkill",
    "TaskMode",
    "CONTENT_DISPOSITION_STATE",
    "FACTUAL_USE_GATE",
    "AUTHORITY_BASIS",
    "SOURCE_ACTION_REF",
    "RequiredEvidence",
    "EvidencePaths",
    "ArchivePath",
    "LAST_VERIFIED_AT",
    "BlockerNotes",
]

MANIFEST_ENTITY_TYPES = {
    "KNOWLEDGE_TYPE",
    "KNOWLEDGE_SUBJECT",
    "HANDBOOK_UNIT",
    "CATEGORY",
    "VOCAB_TERM",
    "OTHER",
}

CONTENT_ACTIONS = {
    "ARCHIVE_AND_STUB",
    "REGENERATE_CONTENT",
    "MODIFY",
    "VERIFY_ONLY",
    "NO_ACTION",
}

TASK_SKILLS = {
    "kty-content-remediate",
    "domain-documents",
    "NONE",
}

TASK_MODES = {
    "RETIRE_KTY",
    "VERIFY_KTY",
    "EMIT_DISPOSITION",
    "SCA_DRIVEN",
    "MODIFY_KTY_REBIND",
    "",
}

DISPOSITION_STATES = {
    "PENDING",
    "ARCHIVED_STUBBED",
    "REGENERATED",
    "VERIFIED",
    "DEFERRED",
    "BLOCKED",
    "NOT_REQUIRED",
}

FACTUAL_USE_GATES = {
    "ALLOW_FACTUAL_USE",
    "REGEN_ONLY",
    "BLOCK_FACTUAL_USE",
    "RETIRED_NO_FACTUAL_USE",
    "NOT_APPLICABLE",
}

REQUIRES_EVIDENCE = {
    "ARCHIVE_AND_STUB",
    "REGENERATE_CONTENT",
    "MODIFY",
    "VERIFY_ONLY",
}

BLOCKING_SEVERITIES = {"CRITICAL", "MAJOR"}


@dataclass(frozen=True)
class Finding:
    severity: str
    row_id: str
    category: str
    message: str


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        header = [h.strip() for h in reader.fieldnames]
        rows: list[dict[str, str]] = []
        for row in reader:
            rows.append({(k or "").strip(): (v or "").strip() for k, v in row.items()})
        return header, rows


def split_semicolon(raw: str) -> list[str]:
    return [token.strip() for token in raw.split(";") if token.strip()]


def is_location_tbd(raw: str) -> bool:
    return raw.strip().lower() == "location tbd"


def resolve_path(raw: str, base_dir: Path, workspace_root: Path | None = None) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    primary = (base_dir / path).resolve()
    if primary.exists() or workspace_root is None:
        return primary
    fallback = (workspace_root / path).resolve()
    if fallback.exists():
        return fallback
    return primary


def find_workspace_root(manifest_path: Path) -> Path | None:
    """Walk up from the manifest folder to find the DOMAIN package root.

    Manifest files live inside `<package_root>/_ScopeChange/<SCA-snapshot>/`.
    Evidence paths (e.g. `_Sources/Piping_Manual/`) are workspace-relative
    to the package root, not to the snapshot folder. Returns the first
    ancestor that contains a `_Sources/` or `_Decomposition/` sibling, or
    None when no convention-matching ancestor is found.
    """
    candidates = [manifest_path.parent, *manifest_path.parent.parents]
    for ancestor in candidates:
        if (ancestor / "_Sources").is_dir() or (ancestor / "_Decomposition").is_dir():
            return ancestor
    return None


def path_has_archive_part(path_text: str) -> bool:
    return ".Archive" in Path(path_text).parts or "/.Archive/" in path_text or "\\.Archive\\" in path_text


def source_ref_keys(row: dict[str, str]) -> set[str]:
    raw = row.get("ActionSeq", "").strip()
    keys: set[str] = set()
    if raw:
        keys.add(raw)
        try:
            num = int(raw)
            keys.add(f"D-{num}")
            keys.add(f"D-{num:03d}")
        except ValueError:
            pass
    for candidate in ("SOURCE_ACTION_REF", "SourceActionRef", "DecisionID"):
        value = row.get(candidate, "").strip()
        if value:
            keys.add(value)
    return keys


def index_actions(action_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in action_rows:
        amendment_id = row.get("AmendmentID", "").strip()
        for key in source_ref_keys(row):
            indexed[key] = row
            if amendment_id:
                indexed[f"{amendment_id}:{key}"] = row
    return indexed


def truthy_yes(raw: str) -> bool:
    return raw.strip().upper() in {"YES", "TRUE", "1"}


def has_manifest_membership_context(manifest_row: dict[str, str]) -> bool:
    """Return true when manifest fields show subject/unit membership impact."""
    entity_type = manifest_row.get("EntityType", "").strip().upper()
    if entity_type in {"KNOWLEDGE_SUBJECT", "HANDBOOK_UNIT"}:
        return True
    return bool(split_semicolon(manifest_row.get("AffectedSubjects", "")) or split_semicolon(manifest_row.get("AffectedHBK", "")))


def expected_content_actions(
    action_row: dict[str, str] | None,
    manifest_row: dict[str, str],
) -> set[str]:
    if action_row is None:
        return set()

    action_type = action_row.get("ActionType", "").strip().upper()
    entity_type = (manifest_row.get("EntityType") or action_row.get("EntityType", "")).strip().upper()
    has_supersession = truthy_yes(action_row.get("SupersessionBindingPresent", ""))

    if action_type == "REMOVE":
        if entity_type == "KNOWLEDGE_TYPE":
            return {"ARCHIVE_AND_STUB"}
        if entity_type in {"KNOWLEDGE_SUBJECT", "HANDBOOK_UNIT"}:
            return {"REGENERATE_CONTENT"}
        return {"VERIFY_ONLY"}

    if action_type == "MODIFY":
        if has_supersession:
            return {"REGENERATE_CONTENT"}
        # Without supersession, MODIFY ActionType can disposition as:
        # - MODIFY (β rebind: atom SubjectID rebinding under partition change, prose preserved)
        # - REGENERATE_CONTENT (α regenerate: full prose authoring under partition explosion)
        # - VERIFY_ONLY (HOLD: no partition change; parent-closure traceability)
        # The disposition class is determined by AOP-09 density tier + Subject_Repartition_Map,
        # not by ActionType alone. All three are valid here.
        return {"MODIFY", "REGENERATE_CONTENT", "VERIFY_ONLY"}

    if action_type == "ADD":
        if entity_type == "KNOWLEDGE_TYPE":
            return {"NO_ACTION"}
        if entity_type in {"KNOWLEDGE_SUBJECT", "HANDBOOK_UNIT"}:
            return {"REGENERATE_CONTENT"}
        return {"VERIFY_ONLY"}

    if action_type == "RECLASSIFY":
        if has_supersession or has_manifest_membership_context(manifest_row):
            return {"REGENERATE_CONTENT"}
        return {"VERIFY_ONLY"}

    if action_type == "MERGE":
        return {"ARCHIVE_AND_STUB", "REGENERATE_CONTENT"}

    if action_type == "SPLIT":
        return {"REGENERATE_CONTENT"}

    return set()


def validate_header(header: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    missing = [col for col in REQUIRED_COLUMNS if col not in header]
    if missing:
        findings.append(Finding(
            "CRITICAL",
            "HEADER",
            "MISSING_COLUMNS",
            f"Missing required columns: {', '.join(missing)}",
        ))
    return findings


def validate_enums(row: dict[str, str], row_id: str) -> list[Finding]:
    findings: list[Finding] = []
    enum_checks = [
        ("EntityType", MANIFEST_ENTITY_TYPES),
        ("ContentAction", CONTENT_ACTIONS),
        ("TaskSkill", TASK_SKILLS),
        ("TaskMode", TASK_MODES),
        ("CONTENT_DISPOSITION_STATE", DISPOSITION_STATES),
        ("FACTUAL_USE_GATE", FACTUAL_USE_GATES),
    ]
    for column, allowed in enum_checks:
        value = row.get(column, "").strip()
        if value not in allowed:
            findings.append(Finding(
                "CRITICAL",
                row_id,
                "INVALID_ENUM",
                f"{column} has invalid value {value!r}",
            ))
    return findings


def validate_dispatch_mapping(row: dict[str, str], row_id: str) -> list[Finding]:
    action = row.get("ContentAction", "").strip()
    skill = row.get("TaskSkill", "").strip()
    mode = row.get("TaskMode", "").strip()
    expected = {
        "ARCHIVE_AND_STUB": ("kty-content-remediate", "RETIRE_KTY"),
        "REGENERATE_CONTENT": ("domain-documents", "SCA_DRIVEN"),
        "MODIFY": ("domain-documents", "MODIFY_KTY_REBIND"),
        "VERIFY_ONLY": ("kty-content-remediate", "VERIFY_KTY"),
        "NO_ACTION": ("NONE", ""),
    }
    if action not in expected:
        return []
    expected_skill, expected_mode = expected[action]
    findings: list[Finding] = []
    if skill != expected_skill or mode != expected_mode:
        findings.append(Finding(
            "CRITICAL",
            row_id,
            "DISPATCH_MISMATCH",
            f"{action} must use TaskSkill={expected_skill} and TaskMode={expected_mode or '<blank>'}",
        ))
    return findings


def validate_source_action_ref(row: dict[str, str], row_id: str) -> list[Finding]:
    source_ref = row.get("SourceActionRef", "").strip()
    mirror_ref = row.get("SOURCE_ACTION_REF", "").strip()
    if not source_ref or not mirror_ref:
        return [Finding("CRITICAL", row_id, "MISSING_SOURCE_ACTION_REF", "SourceActionRef and SOURCE_ACTION_REF are required")]
    if source_ref != mirror_ref:
        return [Finding("MAJOR", row_id, "SOURCE_ACTION_REF_MISMATCH", "SourceActionRef and SOURCE_ACTION_REF must match")]
    return []


def validate_assignment_rule(
    row: dict[str, str],
    row_id: str,
    action_index: dict[str, dict[str, str]] | None,
) -> list[Finding]:
    if action_index is None:
        return []
    source_ref = row.get("SourceActionRef", "").strip()
    action_row = action_index.get(source_ref)
    if action_row is None:
        return [Finding("MAJOR", row_id, "ACTION_NOT_FOUND", f"No Amendment_Actions row matched SourceActionRef={source_ref!r}")]
    expected = expected_content_actions(action_row, row)
    if expected and row.get("ContentAction", "").strip() not in expected:
        return [Finding(
            "MAJOR",
            row_id,
            "CONTENT_ACTION_MISMATCH",
            f"ContentAction={row.get('ContentAction', '')!r} does not match expected {sorted(expected)}",
        )]
    return []


def validate_evidence_paths(
    row: dict[str, str],
    row_id: str,
    base_dir: Path,
    workspace_root: Path | None = None,
) -> list[Finding]:
    action = row.get("ContentAction", "").strip()
    evidence_raw = row.get("EvidencePaths", "").strip()
    blocker_notes = row.get("BlockerNotes", "").strip()
    findings: list[Finding] = []

    if action in REQUIRES_EVIDENCE:
        evidence_paths = split_semicolon(evidence_raw)
        if not evidence_paths:
            findings.append(Finding("MAJOR", row_id, "MISSING_EVIDENCE", f"{action} requires EvidencePaths"))
        for token in evidence_paths:
            if is_location_tbd(token):
                if not blocker_notes:
                    findings.append(Finding("MAJOR", row_id, "EVIDENCE_TBD_WITHOUT_BLOCKER", "location TBD evidence requires BlockerNotes"))
                continue
            path = resolve_path(token, base_dir, workspace_root)
            if not path.exists():
                findings.append(Finding("MAJOR", row_id, "EVIDENCE_PATH_MISSING", f"Evidence path does not exist: {token}"))

    archive_raw = row.get("ArchivePath", "").strip()
    if action == "ARCHIVE_AND_STUB":
        if not archive_raw:
            findings.append(Finding("MAJOR", row_id, "MISSING_ARCHIVE_PATH", "ARCHIVE_AND_STUB requires ArchivePath"))
        elif is_location_tbd(archive_raw):
            if not blocker_notes:
                findings.append(Finding("MAJOR", row_id, "ARCHIVE_TBD_WITHOUT_BLOCKER", "location TBD ArchivePath requires BlockerNotes"))
        else:
            archive_path = resolve_path(archive_raw, base_dir, workspace_root)
            if not path_has_archive_part(archive_raw):
                findings.append(Finding("MAJOR", row_id, "ARCHIVE_PATH_NOT_ARCHIVE", "ArchivePath must contain .Archive/"))
            if not archive_path.exists():
                findings.append(Finding("MAJOR", row_id, "ARCHIVE_PATH_MISSING", f"ArchivePath does not exist: {archive_raw}"))
    elif archive_raw and not is_location_tbd(archive_raw):
        findings.append(Finding("MINOR", row_id, "UNEXPECTED_ARCHIVE_PATH", "ArchivePath should be blank unless ContentAction is ARCHIVE_AND_STUB"))

    return findings


def validate_state_gate(row: dict[str, str], row_id: str) -> list[Finding]:
    state = row.get("CONTENT_DISPOSITION_STATE", "").strip()
    gate = row.get("FACTUAL_USE_GATE", "").strip()
    findings: list[Finding] = []

    if state == "PENDING":
        findings.append(Finding("CRITICAL", row_id, "PENDING_ROW", "PENDING rows block closure"))
    if state in {"DEFERRED", "BLOCKED"} and not row.get("BlockerNotes", "").strip():
        findings.append(Finding("MAJOR", row_id, "BLOCKER_NOTES_REQUIRED", f"{state} requires substantive BlockerNotes"))
    if gate == "ALLOW_FACTUAL_USE" and state not in {"REGENERATED", "VERIFIED", "NOT_REQUIRED"}:
        findings.append(Finding("MAJOR", row_id, "FACTUAL_GATE_MISMATCH", "ALLOW_FACTUAL_USE requires REGENERATED, VERIFIED, or NOT_REQUIRED state"))
    if gate == "RETIRED_NO_FACTUAL_USE" and state != "ARCHIVED_STUBBED":
        findings.append(Finding("MAJOR", row_id, "FACTUAL_GATE_MISMATCH", "RETIRED_NO_FACTUAL_USE requires ARCHIVED_STUBBED state"))
    if gate == "NOT_APPLICABLE" and row.get("ContentAction", "").strip() != "NO_ACTION":
        findings.append(Finding("MINOR", row_id, "FACTUAL_GATE_MISMATCH", "NOT_APPLICABLE should be used only with NO_ACTION"))
    return findings


def validate_manifest(
    manifest_path: Path,
    action_rows: list[dict[str, str]] | None = None,
    workspace_root: Path | None = None,
) -> list[Finding]:
    header, rows = read_csv_rows(manifest_path)
    findings = validate_header(header)
    if findings:
        return findings

    action_index = index_actions(action_rows) if action_rows is not None else None
    base_dir = manifest_path.parent
    if workspace_root is None:
        workspace_root = find_workspace_root(manifest_path)

    for idx, row in enumerate(rows, start=1):
        row_id = row.get("ManifestRowID", "").strip() or f"ROW-{idx}"
        findings.extend(validate_enums(row, row_id))
        findings.extend(validate_source_action_ref(row, row_id))
        findings.extend(validate_dispatch_mapping(row, row_id))
        findings.extend(validate_assignment_rule(row, row_id, action_index))
        findings.extend(validate_evidence_paths(row, row_id, base_dir, workspace_root))
        findings.extend(validate_state_gate(row, row_id))

    return findings


def validate_archive_exclusion(paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in paths:
        if not path.exists():
            findings.append(Finding("MAJOR", str(path), "DOWNSTREAM_INPUT_MISSING", "Downstream input file does not exist"))
            continue
        if path.is_dir():
            findings.append(Finding("MAJOR", str(path), "DOWNSTREAM_INPUT_IS_DIR", "Expected downstream input file, got directory"))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if ".Archive/" in text or "/.Archive" in text or "\\.Archive\\" in text:
            findings.append(Finding("MAJOR", str(path), "ARCHIVE_SCANNER_LEAK", "Downstream input references .Archive/ as current input"))
    return findings


def write_findings_csv(path: Path, findings: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Severity", "RowID", "Category", "Message"])
        writer.writeheader()
        for finding in findings:
            writer.writerow({
                "Severity": finding.severity,
                "RowID": finding.row_id,
                "Category": finding.category,
                "Message": finding.message,
            })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate KTY_Remediation_Manifest.csv")
    parser.add_argument("--manifest", required=True, type=Path, help="Path to KTY_Remediation_Manifest.csv")
    parser.add_argument("--amendment-actions", type=Path, help="Optional Amendment_Actions.csv for ContentAction assignment validation")
    parser.add_argument(
        "--downstream-input",
        action="append",
        type=Path,
        default=[],
        help="Optional downstream allowlist/section-map/publication input file to scan for .Archive/ leakage. Repeatable.",
    )
    parser.add_argument("--output-findings", type=Path, help="Optional findings CSV output")
    parser.add_argument(
        "--workspace-root",
        type=Path,
        help="Optional workspace root for resolving manifest-relative EvidencePaths/ArchivePath. Defaults to the nearest ancestor of the manifest containing _Sources/ or _Decomposition/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        action_rows = None
        if args.amendment_actions:
            _, action_rows = read_csv_rows(args.amendment_actions)
        findings = validate_manifest(
            args.manifest,
            action_rows=action_rows,
            workspace_root=args.workspace_root,
        )
        findings.extend(validate_archive_exclusion(args.downstream_input))
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output_findings:
        write_findings_csv(args.output_findings, findings)

    blocking = [f for f in findings if f.severity in BLOCKING_SEVERITIES]
    print(f"Checked manifest: {args.manifest}")
    print(f"Findings: {len(findings)} total, {len(blocking)} blocking")
    for finding in findings:
        print(f"{finding.severity}: {finding.row_id}: {finding.category}: {finding.message}")

    return 2 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
