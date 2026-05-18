from __future__ import annotations

import csv
import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

import assemble_publication  # noqa: E402


SCHEMA_TABLE = """# Publication Schema

| SectionID | SectionOrder | SectionTitle | SectionType | SectionPurpose | InclusionRule | ExclusionRule | IncludeCategoryIDs | IncludeKnowledgeTypeIDs | IncludeCanonicalSchemas | ExcludeCategoryIDs | ExcludeKnowledgeTypeIDs | ExpectedInputs | ExpectedOutputShape | MaxKAFiles | MaxEstimatedTokens | ComplexityClass | SplitTrigger | SplitHint |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEC-01 | 1 | Overview | OVERVIEW | Frame the facility basis. | Include process. |  | CAT-001 |  |  |  |  | KTYs | Narrative | 10 | 5000 | NORMAL | ANY_LIMIT |  |
"""


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_package_inputs(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "Root"
    publication_root = root / "_Publication" / "DBM"
    planning = publication_root / "_Planning"
    sections_root = publication_root / "sections"
    output_dir = publication_root / "package" / "RUN"
    planning.mkdir(parents=True)

    schema = planning / "Publication_Schema.md"
    schema.write_text(SCHEMA_TABLE, encoding="utf-8")
    rules = planning / "Publication_Rules.md"
    rules.write_text("# Publication Rules\n", encoding="utf-8")

    category = root / "_Decomposition" / "Category_Register.csv"
    write_csv(category, [{"CategoryID": "CAT-001", "CategoryName": "Process", "ScopeDescription": "Process systems."}])
    kty = root / "_Decomposition" / "KnowledgeType_Register.csv"
    write_csv(
        kty,
        [{"KnowledgeTypeID": "KTY-001", "ParentCategoryID": "CAT-001", "KnowledgeTypeName": "Inlet Stabilizer", "SupportsObjectives": "OBJ-001"}],
    )
    subject = root / "_Decomposition" / "Subject_Register.csv"
    write_csv(subject, [{"SubjectID": "SUB-001", "ParentKnowledgeTypeID": "KTY-001", "SubjectName": "Operating pressure"}])
    objective = root / "_Decomposition" / "Objective_Register.csv"
    write_csv(objective, [{"ObjectiveID": "OBJ-001", "Statement": "Maximize condensate recovery."}])
    ledger = root / "_Decomposition" / "Domain_Ledger.csv"
    write_csv(ledger, [{"UnitID": "HBK-001", "CategoryID": "CAT-001", "KnowledgeTypeID(s)": "KTY-001", "ObjectiveID": "OBJ-001"}])
    open_issues = root / "_Decomposition" / "Open_Issues_Register.csv"
    write_csv(open_issues, [{"OpenIssueID": "OI-001", "OpenIssueType": "TBD", "AffectedEntityID": "KTY-001", "Status": "OPEN"}])

    ka = root / "CAT-001_Process" / "1_Working" / "KTY-001_Inlet" / "KA-01_Reference__Pressure.md"
    ka.parent.mkdir(parents=True)
    ka.write_text("Source: design.md\n", encoding="utf-8")
    section_map = planning / "Section_Map.csv"
    write_csv(
        section_map,
        [
            {
                "SectionID": "SEC-01",
                "SectionTitle": "Overview",
                "KnowledgeTypeID": "KTY-001",
                "SubjectID": "SUB-001",
                "CategoryID": "CAT-001",
                "ArtifactPath": str(ka),
                "MappingRole": "PRIMARY",
                "ContributionScope": "FULL_ARTIFACT",
            }
        ],
    )

    manifest = planning / "Publication_Input_Manifest.md"
    manifest.write_text(
        "\n".join(
            [
                "# Manifest",
                f"- EXECUTION_ROOT: `{root}`",
                f"- PUBLICATION_ROOT: `{publication_root}`",
                f"- `{category}`",
                f"- `{kty}`",
                f"- `{subject}`",
                f"- `{objective}`",
                f"- `{ledger}`",
                f"- `{open_issues}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    sec_dir = sections_root / "SEC-01"
    sec_dir.mkdir(parents=True)
    (sec_dir / "SEC-01.md").write_text("# 1 Overview\n\nThe facility basis is TBD and assumed pending confirmation.\n", encoding="utf-8")
    (sec_dir / "SEC-01_ASSERTIONS.csv").write_text("SectionID,AssertionKey,AssertionStatus\n", encoding="utf-8")
    (sec_dir / "SEC-01_QA.md").write_text(
        """# QA

## Section Summary

## Coverage Table

| ArtifactPath | Status | SkipReason |
|---|---|---|
| none | CONSUMED |  |

## Readiness Observations

## Conflict Register

## Terminology Notes

## Gap / TBD Register

| ItemID | Type | Description | Source | AffectedContent |
|---|---|---|---|---|
| GAP-001 | TBD | Pressure pending confirmation | KA-01 | Overview |

## Amendment Notes

## Assertion Emission Notes
""",
        encoding="utf-8",
    )
    return {
        "publication_root": publication_root,
        "manifest": manifest,
        "schema": schema,
        "section_map": section_map,
        "rules": rules,
        "sections_root": sections_root,
        "output_dir": output_dir,
    }


def test_assemble_writes_knowledge_coverage_and_open_items(tmp_path, monkeypatch):
    paths = make_package_inputs(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "assemble_publication.py",
            "--publication-root",
            str(paths["publication_root"]),
            "--input-manifest",
            str(paths["manifest"]),
            "--schema",
            str(paths["schema"]),
            "--section-map",
            str(paths["section_map"]),
            "--rules",
            str(paths["rules"]),
            "--sections-root",
            str(paths["sections_root"]),
            "--output-dir",
            str(paths["output_dir"]),
        ],
    )
    assert assemble_publication.main() == 0
    coverage = (paths["output_dir"] / "Publication_Knowledge_Coverage.md").read_text(encoding="utf-8")
    open_items = (paths["output_dir"] / "Publication_Open_Items.md").read_text(encoding="utf-8")
    assert "Objective Coverage" in coverage
    assert "OBJ-001" in coverage
    assert "Publication Open Items" in open_items
    assert "GAP-001" in open_items
