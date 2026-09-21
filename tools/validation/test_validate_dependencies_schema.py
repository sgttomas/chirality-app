from __future__ import annotations

import csv
from pathlib import Path


from validate_dependencies_schema import REQUIRED_COLUMNS, validate  # noqa: E402


def base_row() -> dict[str, str]:
    row = {column: "" for column in REQUIRED_COLUMNS}
    row.update(
        {
            "RegisterSchemaVersion": "v3.1",
            "DependencyID": "DEP-01-01-001",
            "FromPackageID": "PKG-01",
            "FromDeliverableID": "DEL-01-01",
            "FromDeliverableName": "Governance baseline",
            "DependencyClass": "EXECUTION",
            "AnchorType": "NOT_APPLICABLE",
            "Direction": "UPSTREAM",
            "DependencyType": "PREREQUISITE",
            "TargetType": "DELIVERABLE",
            "TargetPackageID": "PKG-02",
            "TargetDeliverableID": "DEL-02-01",
            "TargetRefID": "DEL-02-01",
            "TargetName": "Canonical model",
            "Statement": "DEL-01-01 depends on DEL-02-01.",
            "EvidenceFile": "_CONTEXT.md",
            "SourceRef": "fixture",
            "EvidenceQuote": "fixture",
            "Explicitness": "EXPLICIT",
            "RequiredMaturity": "SEMANTIC_READY",
            "ProposedMaturity": "SEMANTIC_READY",
            "SatisfactionStatus": "TBD",
            "Confidence": "HIGH",
            "Origin": "EXTRACTED",
            "FirstSeen": "2026-06-16",
            "LastSeen": "2026-06-16",
            "Status": "ACTIVE",
            "Notes": "fixture",
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    fieldnames = fieldnames or REQUIRED_COLUMNS
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def assert_invalid_contains(path: Path, expected: str) -> None:
    valid, findings, _extensions, _row_count, _header = validate(str(path))
    assert valid is False
    assert any(expected in finding for finding in findings)


def test_valid_canonical_row_set(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    write_csv(path, [base_row()])

    valid, findings, extensions, row_count, _header = validate(str(path))

    assert valid is True
    assert findings == []
    assert extensions == []
    assert row_count == 1


def test_extension_columns_are_non_breaking(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    row = base_row()
    row["EstimateImpactClass"] = "TBD"
    row["ConsumerHint"] = "RECONCILIATION"
    fieldnames = REQUIRED_COLUMNS + ["EstimateImpactClass", "ConsumerHint"]
    write_csv(path, [row], fieldnames=fieldnames)

    valid, findings, extensions, _row_count, _header = validate(str(path))

    assert valid is True
    assert findings == []
    assert extensions == ["EstimateImpactClass", "ConsumerHint"]


def test_rejects_legacy_dependency_type(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    row = base_row()
    row["DependencyType"] = "ARCHITECTURE_BASIS"
    write_csv(path, [row])

    assert_invalid_contains(path, "invalid DependencyType")


def test_rejects_candidate_status(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    row = base_row()
    row["Status"] = "CANDIDATE"
    write_csv(path, [row])

    assert_invalid_contains(path, "invalid Status")


def test_rejects_bad_anchor_and_execution_row_rules(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    anchor = base_row()
    anchor.update(
        {
            "DependencyID": "DEP-01-01-A01",
            "DependencyClass": "ANCHOR",
            "AnchorType": "NOT_APPLICABLE",
            "DependencyType": "PREREQUISITE",
            "TargetType": "REQUIREMENT",
            "TargetDeliverableID": "",
            "TargetRefID": "SOW-001",
        }
    )
    execution = base_row()
    execution.update({"DependencyID": "DEP-01-01-E02", "AnchorType": "DELIVERABLE"})
    write_csv(path, [anchor, execution])

    valid, findings, _extensions, _row_count, _header = validate(str(path))

    assert valid is False
    assert any("ANCHOR row must use DependencyType=OTHER" in finding for finding in findings)
    assert any("ANCHOR row must not use AnchorType=NOT_APPLICABLE" in finding for finding in findings)
    assert any("EXECUTION row must use AnchorType=NOT_APPLICABLE" in finding for finding in findings)


def test_rejects_bad_target_deliverable_placement(tmp_path: Path) -> None:
    path = tmp_path / "Dependencies.csv"
    missing_deliverable = base_row()
    missing_deliverable.update({"DependencyID": "DEP-01-01-E02", "TargetDeliverableID": ""})
    non_deliverable = base_row()
    non_deliverable.update(
        {
            "DependencyID": "DEP-01-01-E03",
            "TargetType": "DOCUMENT",
            "TargetDeliverableID": "DEL-02-01",
            "TargetRefID": "DOC-001",
        }
    )
    write_csv(path, [missing_deliverable, non_deliverable])

    valid, findings, _extensions, _row_count, _header = validate(str(path))

    assert valid is False
    assert any("TargetType=DELIVERABLE requires TargetDeliverableID" in finding for finding in findings)
    assert any("non-deliverable TargetType must leave TargetDeliverableID blank" in finding for finding in findings)
