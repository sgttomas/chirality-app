from __future__ import annotations

import csv
import sys
from pathlib import Path


VALIDATION_DIR = Path(__file__).resolve().parent
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

from validate_kty_remediation_manifest import (  # noqa: E402
    REQUIRED_COLUMNS,
    find_workspace_root,
    validate_archive_exclusion,
    validate_manifest,
)


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def base_manifest_row(tmp_path: Path) -> dict[str, str]:
    evidence = tmp_path / "Evidence" / "KTY-01_Content.md"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text("ok\n", encoding="utf-8")
    archive = tmp_path / "KTY-01" / ".Archive" / "SCA-001_2026-04-21_1200"
    archive.mkdir(parents=True, exist_ok=True)

    return {
        "AmendmentID": "SCA-001",
        "ManifestRowID": "KRM-001",
        "SourceActionRef": "D-001",
        "EntityType": "KNOWLEDGE_TYPE",
        "EntityID": "KTY-01",
        "KTYID": "KTY-01",
        "KTYPath": str(tmp_path / "KTY-01"),
        "AffectedSubjects": "",
        "AffectedHBK": "",
        "CanonicalRootName": "Example_Root",
        "FacilityID": "03-25",
        "ContentAction": "ARCHIVE_AND_STUB",
        "TaskSkill": "kty-content-remediate",
        "TaskMode": "RETIRE_KTY",
        "CONTENT_DISPOSITION_STATE": "ARCHIVED_STUBBED",
        "FACTUAL_USE_GATE": "RETIRED_NO_FACTUAL_USE",
        "AUTHORITY_BASIS": "SCA-001",
        "SOURCE_ACTION_REF": "D-001",
        "RequiredEvidence": "REPORT;ARCHIVE_PATH",
        "EvidencePaths": str(evidence),
        "ArchivePath": str(archive),
        "LAST_VERIFIED_AT": "2026-04-21T12:00:00",
        "BlockerNotes": "",
    }


def test_valid_manifest_passes_assignment_and_evidence_checks(tmp_path: Path) -> None:
    manifest = tmp_path / "KTY_Remediation_Manifest.csv"
    actions = tmp_path / "Amendment_Actions.csv"
    write_csv(manifest, [base_manifest_row(tmp_path)], REQUIRED_COLUMNS)
    write_csv(actions, [{
        "AmendmentID": "SCA-001",
        "ActionSeq": "1",
        "ActionType": "REMOVE",
        "EntityType": "KNOWLEDGE_TYPE",
        "EntityID": "KTY-01",
        "Description": "retire KTY",
        "AffectedFiles": "",
        "DownstreamReruns": "",
        "SupersessionBindingPresent": "NO",
    }])

    with actions.open(encoding="utf-8", newline="") as f:
        action_rows = list(csv.DictReader(f))
    findings = validate_manifest(manifest, action_rows=action_rows)

    assert findings == []


def test_assignment_rule_blocks_wrong_content_action(tmp_path: Path) -> None:
    row = base_manifest_row(tmp_path)
    row["ContentAction"] = "VERIFY_ONLY"
    row["TaskSkill"] = "kty-content-remediate"
    row["TaskMode"] = "VERIFY_KTY"
    row["CONTENT_DISPOSITION_STATE"] = "VERIFIED"
    row["FACTUAL_USE_GATE"] = "ALLOW_FACTUAL_USE"
    row["ArchivePath"] = ""
    manifest = tmp_path / "KTY_Remediation_Manifest.csv"
    write_csv(manifest, [row], REQUIRED_COLUMNS)
    action_rows = [{
        "ActionSeq": "1",
        "ActionType": "REMOVE",
        "EntityType": "KNOWLEDGE_TYPE",
        "SupersessionBindingPresent": "NO",
    }]

    findings = validate_manifest(manifest, action_rows=action_rows)

    assert any(f.category == "CONTENT_ACTION_MISMATCH" for f in findings)


def test_archive_and_stub_requires_explicit_archive_path(tmp_path: Path) -> None:
    row = base_manifest_row(tmp_path)
    row["ArchivePath"] = ""
    manifest = tmp_path / "KTY_Remediation_Manifest.csv"
    write_csv(manifest, [row], REQUIRED_COLUMNS)

    findings = validate_manifest(manifest)

    assert any(f.category == "MISSING_ARCHIVE_PATH" for f in findings)


def test_archive_scanner_leak_is_reported(tmp_path: Path) -> None:
    downstream = tmp_path / "Section_Map.csv"
    downstream.write_text("InputPath\nKTY-01/.Archive/SCA-001/KA-01.md\n", encoding="utf-8")

    findings = validate_archive_exclusion([downstream])

    assert len(findings) == 1
    assert findings[0].category == "ARCHIVE_SCANNER_LEAK"


def test_foreign_key_source_action_ref_resolves_against_amendment_actions(tmp_path: Path) -> None:
    package_root = tmp_path / "pkg"
    snapshot = package_root / "_ScopeChange" / "SCA-009_2026-05-04_1200"
    snapshot.mkdir(parents=True)
    (package_root / "_Sources").mkdir()
    (package_root / "_Decomposition").mkdir()

    evidence = package_root / "_Sources" / "Handbook"
    evidence.mkdir()

    row = base_manifest_row(tmp_path)
    row.update({
        "AmendmentID": "SCA-009",
        "SourceActionRef": "SCA-009:1",
        "SOURCE_ACTION_REF": "SCA-009:1",
        "AUTHORITY_BASIS": "SCA-009",
        "EntityType": "KNOWLEDGE_TYPE",
        "ContentAction": "REGENERATE_CONTENT",
        "TaskSkill": "domain-documents",
        "TaskMode": "SCA_DRIVEN",
        "CONTENT_DISPOSITION_STATE": "VERIFIED",
        "FACTUAL_USE_GATE": "ALLOW_FACTUAL_USE",
        "ArchivePath": "",
        "EvidencePaths": "_Sources/Handbook",
    })
    manifest = snapshot / "KTY_Remediation_Manifest.csv"
    write_csv(manifest, [row], REQUIRED_COLUMNS)
    action_rows = [{
        "AmendmentID": "SCA-009",
        "ActionSeq": "1",
        "ActionType": "MODIFY",
        "EntityType": "KNOWLEDGE_TYPE",
        "SupersessionBindingPresent": "YES",
    }]

    findings = validate_manifest(manifest, action_rows=action_rows)

    assert not any(f.category == "ACTION_NOT_FOUND" for f in findings)
    assert not any(f.category == "EVIDENCE_PATH_MISSING" for f in findings)


def test_workspace_root_fallback_resolves_evidence_outside_snapshot(tmp_path: Path) -> None:
    package_root = tmp_path / "pkg"
    snapshot = package_root / "_ScopeChange" / "SCA-010_2026-05-04_1200"
    snapshot.mkdir(parents=True)
    (package_root / "_Sources").mkdir()
    (package_root / "_Decomposition").mkdir()
    evidence_dir = package_root / "_Sources" / "Manual"
    evidence_dir.mkdir()

    row = base_manifest_row(tmp_path)
    row.update({
        "AmendmentID": "SCA-010",
        "SourceActionRef": "SCA-010:1",
        "SOURCE_ACTION_REF": "SCA-010:1",
        "AUTHORITY_BASIS": "SCA-010",
        "EntityType": "KNOWLEDGE_TYPE",
        "ContentAction": "REGENERATE_CONTENT",
        "TaskSkill": "domain-documents",
        "TaskMode": "SCA_DRIVEN",
        "CONTENT_DISPOSITION_STATE": "VERIFIED",
        "FACTUAL_USE_GATE": "ALLOW_FACTUAL_USE",
        "ArchivePath": "",
        "EvidencePaths": "_Sources/Manual",
    })
    manifest = snapshot / "KTY_Remediation_Manifest.csv"
    write_csv(manifest, [row], REQUIRED_COLUMNS)
    action_rows = [{
        "AmendmentID": "SCA-010",
        "ActionSeq": "1",
        "ActionType": "MODIFY",
        "EntityType": "KNOWLEDGE_TYPE",
        "SupersessionBindingPresent": "YES",
    }]

    auto_findings = validate_manifest(manifest, action_rows=action_rows)
    assert not any(f.category == "EVIDENCE_PATH_MISSING" for f in auto_findings)

    explicit_findings = validate_manifest(manifest, action_rows=action_rows, workspace_root=package_root)
    assert not any(f.category == "EVIDENCE_PATH_MISSING" for f in explicit_findings)


def test_workspace_root_auto_detected_via_sibling_markers(tmp_path: Path) -> None:
    package_root = tmp_path / "pkg"
    snapshot = package_root / "_ScopeChange" / "SCA-011_2026-05-04_1200"
    snapshot.mkdir(parents=True)
    (package_root / "_Sources").mkdir()

    detected = find_workspace_root(snapshot / "KTY_Remediation_Manifest.csv")
    assert detected == package_root

    bare = tmp_path / "loose" / "manifest.csv"
    bare.parent.mkdir()
    assert find_workspace_root(bare) is None


def test_reclassify_with_subject_membership_context_requires_regeneration(tmp_path: Path) -> None:
    row = base_manifest_row(tmp_path)
    row.update({
        "EntityType": "KNOWLEDGE_SUBJECT",
        "EntityID": "SUB-01-01-01",
        "AffectedSubjects": "SUB-01-01-01",
        "ContentAction": "VERIFY_ONLY",
        "TaskSkill": "kty-content-remediate",
        "TaskMode": "VERIFY_KTY",
        "CONTENT_DISPOSITION_STATE": "VERIFIED",
        "FACTUAL_USE_GATE": "ALLOW_FACTUAL_USE",
        "ArchivePath": "",
    })
    manifest = tmp_path / "KTY_Remediation_Manifest.csv"
    write_csv(manifest, [row], REQUIRED_COLUMNS)
    action_rows = [{
        "ActionSeq": "1",
        "ActionType": "RECLASSIFY",
        "EntityType": "KNOWLEDGE_SUBJECT",
        "SupersessionBindingPresent": "NO",
    }]

    findings = validate_manifest(manifest, action_rows=action_rows)

    assert any(f.category == "CONTENT_ACTION_MISMATCH" for f in findings)
