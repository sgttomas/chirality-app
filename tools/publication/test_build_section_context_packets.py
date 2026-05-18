from __future__ import annotations

import csv
import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from build_section_context_packets import generate_packets  # noqa: E402


SCHEMA_TABLE = """# Publication Schema

| SectionID | SectionOrder | SectionTitle | SectionType | SectionPurpose | InclusionRule | ExclusionRule | IncludeCategoryIDs | IncludeKnowledgeTypeIDs | IncludeCanonicalSchemas | ExcludeCategoryIDs | ExcludeKnowledgeTypeIDs | ExpectedInputs | ExpectedOutputShape | MaxKAFiles | MaxEstimatedTokens | ComplexityClass | SplitTrigger | SplitHint |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SEC-01 | 1 | Overview | OVERVIEW | Frame the facility basis. | Include process. |  | CAT-001 |  |  |  |  | KTYs | Narrative | 10 | 5000 | NORMAL | ANY_LIMIT |  |
| SEC-02 | 2 | Process Basis | PROCESS_BASIS | Publish process basis. | Include process. |  | CAT-001 |  |  |  |  | KTYs | Narrative | 10 | 5000 | NORMAL | ANY_LIMIT |  |
"""


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_inputs(tmp_path: Path) -> dict[str, Path]:
    root = tmp_path / "Root"
    planning = root / "_Publication" / "DBM" / "_Planning"
    planning.mkdir(parents=True)

    schema = planning / "Publication_Schema.md"
    schema.write_text(SCHEMA_TABLE, encoding="utf-8")

    category = root / "_Decomposition" / "Category_Register.csv"
    write_csv(
        category,
        [{"CategoryID": "CAT-001", "CategoryName": "Process", "ScopeDescription": "Process systems."}],
    )
    kty = root / "_Decomposition" / "KnowledgeType_Register.csv"
    write_csv(
        kty,
        [
            {
                "KnowledgeTypeID": "KTY-001",
                "ParentCategoryID": "CAT-001",
                "KnowledgeTypeName": "Inlet Stabilizer",
                "Description": "Stabilizer design basis.",
                "SupportsObjectives": "OBJ-001",
            }
        ],
    )
    subject = root / "_Decomposition" / "Subject_Register.csv"
    write_csv(
        subject,
        [{"SubjectID": "SUB-001", "ParentKnowledgeTypeID": "KTY-001", "SubjectName": "Operating pressure"}],
    )
    objective = root / "_Decomposition" / "Objective_Register.csv"
    write_csv(objective, [{"ObjectiveID": "OBJ-001", "Statement": "Maximize condensate recovery."}])
    ledger = root / "_Decomposition" / "Domain_Ledger.csv"
    write_csv(
        ledger,
        [{"UnitID": "HBK-001", "CategoryID": "CAT-001", "KnowledgeTypeID(s)": "KTY-001", "ObjectiveID": "OBJ-001"}],
    )
    vocab = root / "_Decomposition" / "Vocabulary_Map.csv"
    write_csv(vocab, [{"CanonicalTerm": "Inlet Stabilizer", "Synonyms": "Stabilizer"}])
    open_issues = root / "_Decomposition" / "Open_Issues_Register.csv"
    write_csv(
        open_issues,
        [{"OpenIssueID": "OI-001", "OpenIssueType": "TBD", "AffectedEntityID": "KTY-001", "Summary": "Pressure to be confirmed"}],
    )

    sca = root / "_ScopeChange" / "SCA-001"
    remediation = sca / "KTY_Remediation_Manifest.csv"
    write_csv(
        remediation,
        [{"KTYID": "KTY-001", "FACTUAL_USE_GATE": "ALLOW_FACTUAL_USE", "CONTENT_DISPOSITION_STATE": "CURRENT", "Notes": "Ready"}],
    )
    supersession = sca / "Supersession_Map.csv"
    write_csv(
        supersession,
        [
            {
                "SupersededFactKey": "PRESSURE",
                "OverrideType": "SUPERSESSION",
                "ReplacementValue": "150 psig",
                "AmendmentID": "SCA-001",
                "AppliesToSections": "SEC-01",
            }
        ],
    )

    section_map = planning / "Section_Map.csv"
    ka_path = root / "CAT-001_Process" / "1_Working" / "KTY-001_Inlet" / "KA-01_Reference__Pressure.md"
    ka_path.parent.mkdir(parents=True)
    ka_path.write_text("# Pressure\n", encoding="utf-8")
    write_csv(
        section_map,
        [
            {
                "SectionID": "SEC-01",
                "SectionTitle": "Overview",
                "SectionType": "OVERVIEW",
                "SourceDomain": "Root",
                "CategoryID": "CAT-001",
                "KnowledgeTypeID": "KTY-001",
                "SubjectID": "SUB-001",
                "ArtifactPath": str(ka_path),
                "MappingRole": "PRIMARY",
                "ContributionScope": "FULL_ARTIFACT",
                "SCARefs": "SCA-001",
                "DecisionRefs": "",
                "CurrentStateBasis": "SCA-001",
                "LifecycleState": "ACTIVE",
                "LifecycleSource": "MANIFEST",
                "Notes": "Artifact Plan row KA-01",
            }
        ],
    )
    register = planning / "Publication_Concordance_Register.csv"
    write_csv(
        register,
        [
            {
                "AssertionKey": "PRESSURE",
                "AuthoritySectionID": "SEC-01",
                "RequiredSectionIDs": "SEC-01; SEC-02",
                "SourceFidelityCritical": "YES",
                "SourceExpectedValue": "150",
            }
        ],
    )
    risk = planning / "Publication_Concordance_Risk_Inventory.csv"
    write_csv(
        risk,
        [
            {
                "RiskID": "RISK-001",
                "RiskClass": "DESIGN_LIMIT",
                "SourceArtifact": str(ka_path),
                "SourceKTYID": "KTY-001",
                "AffectedSectionIDs": "SEC-01",
                "CurrentStateBasis": "SCA-001",
                "WhyItMatters": "Pressure risk.",
                "ExpectedConcordanceTreatment": "COVER",
                "RegisterAssertionKey": "PRESSURE",
                "CoverageStatus": "COVERED_BY_REGISTER",
                "WaiverReason": "",
            }
        ],
    )

    manifest = planning / "Publication_Input_Manifest.md"
    manifest.write_text(
        "\n".join(
            [
                "# Manifest",
                f"- EXECUTION_ROOT: `{root}`",
                f"- PUBLICATION_ROOT: `{root / '_Publication' / 'DBM'}`",
                f"- SUPERSESSION_MAP_PATH: `{supersession}`",
                f"- `{category}`",
                f"- `{kty}`",
                f"- `{subject}`",
                f"- `{objective}`",
                f"- `{ledger}`",
                f"- `{vocab}`",
                f"- `{open_issues}`",
                f"- `{remediation}`",
                f"- `{supersession}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "manifest": manifest,
        "schema": schema,
        "section_map": section_map,
        "register": register,
        "risk": risk,
        "supersession": supersession,
        "open_issues": open_issues,
        "output": planning / "section-context",
    }


def render(tmp_path: Path) -> tuple[list[Path], list[str]]:
    paths = make_inputs(tmp_path)
    return generate_packets(
        manifest_path=paths["manifest"],
        schema_path=paths["schema"],
        section_map_path=paths["section_map"],
        concordance_register_path=paths["register"],
        risk_inventory_path=paths["risk"],
        output_dir=paths["output"],
        supersession_map_path=paths["supersession"],
        open_issues_path=paths["open_issues"],
    )


def test_packet_generated_per_section(tmp_path):
    written, _ = render(tmp_path)
    assert [path.name for path in written] == ["SEC-01_Context.md", "SEC-02_Context.md"]


def test_objectives_filtered_to_mapped_ktys(tmp_path):
    written, _ = render(tmp_path)
    text = written[0].read_text(encoding="utf-8")
    assert "OBJ-001" in text
    assert "Maximize condensate recovery." in text


def test_supersession_filtered_to_section(tmp_path):
    written, _ = render(tmp_path)
    assert "150 psig" in written[0].read_text(encoding="utf-8")
    assert "150 psig" not in written[1].read_text(encoding="utf-8")


def test_open_issues_filtered_to_section(tmp_path):
    written, _ = render(tmp_path)
    assert "Pressure to be confirmed" in written[0].read_text(encoding="utf-8")


def test_factual_use_gate_populated(tmp_path):
    written, _ = render(tmp_path)
    assert "ALLOW_FACTUAL_USE" in written[0].read_text(encoding="utf-8")


def test_vocabulary_filtered_to_section(tmp_path):
    written, _ = render(tmp_path)
    assert "Inlet Stabilizer" in written[0].read_text(encoding="utf-8")


def test_concordance_risk_coverage_populated(tmp_path):
    written, _ = render(tmp_path)
    text = written[0].read_text(encoding="utf-8")
    assert "RISK-001" in text
    assert "COVERED_BY_REGISTER" in text


def test_missing_register_produces_exit_2_style_warning(tmp_path):
    paths = make_inputs(tmp_path)
    # Remove optional objective/register context from the manifest. Packets still
    # generate, but the caller should treat warnings as exit-code 2 in CLI mode.
    paths["manifest"].write_text(
        "\n".join(
            [
                "# Manifest",
                f"- EXECUTION_ROOT: `{tmp_path / 'Root'}`",
                f"- PUBLICATION_ROOT: `{tmp_path / 'Root' / '_Publication' / 'DBM'}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    written, warnings = generate_packets(
        manifest_path=paths["manifest"],
        schema_path=paths["schema"],
        section_map_path=paths["section_map"],
        concordance_register_path=paths["register"],
        risk_inventory_path=paths["risk"],
        output_dir=paths["output"],
    )
    assert written
    assert any("objective_register" in warning for warning in warnings)
