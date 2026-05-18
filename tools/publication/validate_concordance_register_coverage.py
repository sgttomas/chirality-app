#!/usr/bin/env python3
"""
validate_concordance_register_coverage.py - Gate 4 concordance coverage validator.

Purpose:
  Validate that the human-reviewable concordance register covers or explicitly
  resolves every mechanical risk inventory row before section synthesis begins.

Inputs:
  --risk-inventory   Publication_Concordance_Risk_Inventory.csv
  --register         Publication_Concordance_Register.csv
  --section-map      Section_Map.csv
  --manifest         Publication_Input_Manifest.md
  --supersession-map Optional Supersession_Map.csv
  --output-report    Markdown coverage report
  --output-findings  CSV findings

Exit codes:
  0 = all covered
  1 = fatal input / parsing error
  2 = uncovered or blocking risks
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import parse_list_cell, parse_manifest, read_csv_rows, require_within, write_csv  # type: ignore

FINDING_COLUMNS = [
    "FindingID",
    "FindingType",
    "RiskID",
    "AssertionKey",
    "SourceArtifact",
    "SectionID",
    "Blocking",
    "Notes",
]

REQUIRED_REGISTER_COLUMNS = [
    "AssertionKey",
    "AssertionLabel",
    "AssertionDomain",
    "AssertionType",
    "CanonicalTerm",
    "Unit",
    "ComparisonRule",
    "ComparisonParameter",
    "AuthoritySectionID",
    "RequiredSectionIDs",
    "FacilityScope",
    "CurrentStateBasis",
    "DecisionRefs",
    "DiscoverySource",
    "NormalizationHint",
    "NormalizationContract",
    "Criticality",
    "SourceFidelityCritical",
    "SourceExpectedValue",
    "Notes",
]

ALLOWED_RISK_RESOLUTION = {"COVERED_BY_REGISTER", "WAIVED_WITH_RATIONALE", "DEFERRED_BLOCKING", "OUT_OF_SCOPE"}
ALLOWED_SOURCE_FIDELITY = {"YES", "NO", ""}


def fatal(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def finding(
    finding_type: str,
    risk_id: str = "",
    assertion_key: str = "",
    source_artifact: str = "",
    section_id: str = "",
    blocking: bool = True,
    notes: str = "",
) -> Dict[str, str]:
    basis = "|".join([finding_type, risk_id, assertion_key, source_artifact, section_id])
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:10].upper()
    return {
        "FindingID": f"CCOV-{digest}",
        "FindingType": finding_type,
        "RiskID": risk_id,
        "AssertionKey": assertion_key,
        "SourceArtifact": source_artifact,
        "SectionID": section_id,
        "Blocking": "TRUE" if blocking else "FALSE",
        "Notes": notes,
    }


def csv_header(path: Path) -> List[str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            return [col.strip() for col in next(reader)]
    except FileNotFoundError:
        fatal(f"File not found: {path}")
    except StopIteration:
        return []


def section_ids(section_map_rows: Sequence[Dict[str, str]]) -> set:
    return {row.get("SectionID", "") for row in section_map_rows if row.get("SectionID", "")}


def build_report(findings: Sequence[Dict[str, str]], risk_rows: Sequence[Dict[str, str]], register_rows: Sequence[Dict[str, str]]) -> str:
    blocking = [row for row in findings if row.get("Blocking") == "TRUE"]
    lines = [
        "# Concordance Register Coverage Report",
        "",
        "## Summary",
        "",
        f"- Risk inventory rows: {len(risk_rows)}",
        f"- Register rows: {len(register_rows)}",
        f"- Findings: {len(findings)}",
        f"- Blocking findings: {len(blocking)}",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.append("| FindingType | RiskID | AssertionKey | SectionID | Blocking | Notes |")
        lines.append("|---|---|---|---|---|---|")
        for row in findings:
            lines.append(
                "| {FindingType} | {RiskID} | {AssertionKey} | {SectionID} | {Blocking} | {Notes} |".format(
                    **{key: value.replace("|", "\\|") for key, value in row.items()}
                )
            )
    else:
        lines.append("- None")
    return "\n".join(lines).rstrip() + "\n"


def validate(
    risk_rows: List[Dict[str, str]],
    register_rows: List[Dict[str, str]],
    register_header: List[str],
    section_map_rows: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    section_set = section_ids(section_map_rows)
    register_by_key = {row.get("AssertionKey", ""): row for row in register_rows if row.get("AssertionKey", "")}

    missing_columns = [col for col in REQUIRED_REGISTER_COLUMNS if col not in register_header]
    for column in missing_columns:
        findings.append(finding("REGISTER_MISSING_REQUIRED_COLUMN", assertion_key=column, notes=f"Missing required register column: {column}"))

    for risk in risk_rows:
        status = risk.get("CoverageStatus", "").strip().upper()
        risk_id = risk.get("RiskID", "")
        key = risk.get("RegisterAssertionKey", "").strip()
        if status not in ALLOWED_RISK_RESOLUTION:
            findings.append(
                finding(
                    "UNCOVERED_HIGH_RISK",
                    risk_id=risk_id,
                    assertion_key=key,
                    source_artifact=risk.get("SourceArtifact", ""),
                    section_id=risk.get("AffectedSectionIDs", ""),
                    notes="Every risk inventory row must be covered, waived, deferred as blocking, or out of scope.",
                )
            )
            continue
        if status == "COVERED_BY_REGISTER" and key not in register_by_key:
            findings.append(
                finding(
                    "RISK_COVERAGE_KEY_NOT_IN_REGISTER",
                    risk_id=risk_id,
                    assertion_key=key,
                    source_artifact=risk.get("SourceArtifact", ""),
                    notes="Risk row claims register coverage but RegisterAssertionKey is absent from the register.",
                )
            )
        if status == "WAIVED_WITH_RATIONALE" and not risk.get("WaiverReason", "").strip():
            findings.append(
                finding(
                    "WAIVER_MISSING_RATIONALE",
                    risk_id=risk_id,
                    assertion_key=key,
                    source_artifact=risk.get("SourceArtifact", ""),
                    notes="WAIVED_WITH_RATIONALE requires WaiverReason.",
                )
            )

    for row in register_rows:
        key = row.get("AssertionKey", "")
        authority = row.get("AuthoritySectionID", "")
        if authority and authority not in section_set:
            findings.append(finding("UNKNOWN_AUTHORITY_SECTION", assertion_key=key, section_id=authority, notes="AuthoritySectionID is not present in Section_Map.csv."))
        for section_id in parse_list_cell(row.get("RequiredSectionIDs", "")):
            if section_id not in section_set:
                findings.append(finding("UNKNOWN_REQUIRED_SECTION", assertion_key=key, section_id=section_id, notes="RequiredSectionIDs contains a section absent from Section_Map.csv."))
        sf = row.get("SourceFidelityCritical", "").strip().upper()
        if sf not in ALLOWED_SOURCE_FIDELITY:
            findings.append(finding("INVALID_SOURCE_FIDELITY_FLAG", assertion_key=key, notes="SourceFidelityCritical must be YES or NO."))
        if sf == "YES" and not row.get("SourceExpectedValue", "").strip():
            rationale = row.get("SourceFidelityRationale", "") or row.get("Notes", "")
            if not rationale.strip():
                findings.append(finding("SOURCE_FIDELITY_EXPECTED_VALUE_MISSING", assertion_key=key, notes="SourceFidelityCritical=YES requires SourceExpectedValue or explicit rationale."))
        if "NormalizationContract" in register_header and not row.get("NormalizationContract", "").strip():
            findings.append(finding("NORMALIZATION_CONTRACT_MISSING", assertion_key=key, blocking=False, notes="Register row lacks NormalizationContract."))

    primary_artifacts = {
        row.get("ArtifactPath", "")
        for row in section_map_rows
        if row.get("MappingRole", "").upper() == "PRIMARY"
    }
    for risk in risk_rows:
        if risk.get("RiskClass", "") == "RETIRED_CONTENT_REFERENCE" and risk.get("SourceArtifact", "") in primary_artifacts:
            findings.append(
                finding(
                    "RETIRED_ARTIFACT_MAPPED_AS_PRIMARY",
                    risk_id=risk.get("RiskID", ""),
                    source_artifact=risk.get("SourceArtifact", ""),
                    section_id=risk.get("AffectedSectionIDs", ""),
                    notes="Retired/tombstoned content must not be mapped as PRIMARY authority.",
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate concordance register coverage against risk inventory.")
    parser.add_argument("--risk-inventory", required=True)
    parser.add_argument("--register", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--supersession-map", default="")
    parser.add_argument("--output-report", required=True)
    parser.add_argument("--output-findings", required=True)
    args = parser.parse_args()

    risk_path = Path(args.risk_inventory).resolve()
    register_path = Path(args.register).resolve()
    section_map_path = Path(args.section_map).resolve()
    manifest_path = Path(args.manifest).resolve()
    report_path = Path(args.output_report).resolve()
    findings_path = Path(args.output_findings).resolve()
    for path in [risk_path, register_path, section_map_path, manifest_path]:
        if not path.exists():
            fatal(f"Required input does not exist: {path}")

    manifest = parse_manifest(manifest_path)
    publication_root = manifest["publication_root"]
    if not isinstance(publication_root, Path):
        fatal("Publication root could not be resolved from manifest.")
    require_within(report_path, publication_root, "--output-report")
    require_within(findings_path, publication_root, "--output-findings")

    risk_rows = read_csv_rows(risk_path)
    register_rows = read_csv_rows(register_path)
    section_map_rows = read_csv_rows(section_map_path)
    findings = validate(risk_rows, register_rows, csv_header(register_path), section_map_rows)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(findings, risk_rows, register_rows), encoding="utf-8")
    write_csv(findings_path, FINDING_COLUMNS, findings)
    print(f"Wrote coverage report: {report_path}")
    print(f"Wrote coverage findings: {findings_path}")
    print(f"Findings: {len(findings)}")
    return 2 if any(row.get("Blocking") == "TRUE" for row in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
