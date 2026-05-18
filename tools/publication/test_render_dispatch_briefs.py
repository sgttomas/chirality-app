from __future__ import annotations

import sys
from pathlib import Path

import pytest


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from render_dispatch_briefs import (  # noqa: E402
    main,
    render_concordance_verify_brief,
    render_package_brief,
    render_section_brief,
    validate_full_engineering_rules,
)
from build_section_map import parse_manifest  # noqa: E402


def test_section_brief_required_fields(tmp_path):
    context_root = tmp_path / "_Planning" / "section-context"
    context_root.mkdir(parents=True)
    (context_root / "SEC-01_Context.md").write_text("# Section Context\n", encoding="utf-8")
    paths = {
        "input_manifest": tmp_path / "Publication_Input_Manifest.md",
        "schema": tmp_path / "Publication_Schema.md",
        "section_map": tmp_path / "Section_Map.csv",
        "rules": tmp_path / "Publication_Rules.md",
        "concordance_register": tmp_path / "Publication_Concordance_Register.csv",
        "section_context_root": context_root,
    }
    section = {
        "SectionID": "SEC-01",
        "SectionTitle": "Basis",
        "SectionType": "PROCESS_BASIS",
        "SectionPurpose": "Publish basis.",
        "SectionOrder": "1",
        "MaxKAFiles": "12",
    }
    brief, _ = render_section_brief(section, tmp_path / "sections" / "SEC-01", paths, "Root")
    assert "TaskSkill: dbm-section-publish" in brief
    assert "DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM" in brief
    assert "PUBLICATION_CONCORDANCE_REGISTER_PATH:" in brief
    assert "SECTION_CONTEXT_PATH:" in brief


def test_package_brief_supersession_propagation(tmp_path):
    paths = {
        "publication_root": tmp_path,
        "input_manifest": tmp_path / "_Planning" / "Publication_Input_Manifest.md",
        "schema": tmp_path / "_Planning" / "Publication_Schema.md",
        "section_map": tmp_path / "_Planning" / "Section_Map.csv",
        "rules": tmp_path / "_Planning" / "Publication_Rules.md",
        "concordance_register": tmp_path / "_Planning" / "Publication_Concordance_Register.csv",
        "sections_root": tmp_path / "sections",
        "package_root": tmp_path / "package",
    }
    brief = render_package_brief(tmp_path / "package" / "RUN", paths, "Root", "RUN", supersession_map_path="/tmp/Supersession_Map.csv", facility_id="04-25")
    assert "SUPERSESSION_MAP_PATH: /tmp/Supersession_Map.csv" in brief
    assert "FACILITY_ID: 04-25" in brief
    assert "DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM" in brief
    assert "Publication_Knowledge_Coverage.md" in brief
    assert "Publication_Open_Items.md" in brief
    assert "Publication_Content_Adequacy.md" in brief


def test_verify_brief_rendering(tmp_path):
    paths = {
        "sections_root": tmp_path / "sections",
        "concordance_register": tmp_path / "_Planning" / "Publication_Concordance_Register.csv",
        "rules": tmp_path / "_Planning" / "Publication_Rules.md",
        "input_manifest": tmp_path / "_Planning" / "Publication_Input_Manifest.md",
    }
    brief = render_concordance_verify_brief(tmp_path / "package" / "RUN", paths)
    assert "TaskSkill: dbm-concordance-verify" in brief
    assert "Publication_Concordance_Verification_Findings.csv" in brief


def test_full_engineering_rules_reject_stale_compression(tmp_path):
    rules = tmp_path / "Publication_Rules.md"
    rules.write_text(
        "\n".join(
            [
                "# Publication Rules",
                "",
                "- DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM",
                "- BodyCompletenessStandard: body completeness is required.",
                "- TabularDataPolicy: design-basis tables are required.",
                "- BodyVsQAArtifactBoundaryRule: QA scaffolds must not define the main body.",
                "- A section with high KTY count must summarize stable system-level design basis in body prose.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(SystemExit):
        validate_full_engineering_rules(rules)


def test_renderer_scratch_full_engineering_dispatch(monkeypatch, tmp_path):
    execution_root = tmp_path / "Root"
    publication_root = execution_root / "_Publication" / "DBM"
    planning_root = publication_root / "_Planning"
    dispatch_root = publication_root / "dispatch"
    sections_root = publication_root / "sections"
    package_root = publication_root / "package"
    planning_root.mkdir(parents=True)
    supersession_map = planning_root / "Supersession_Map.csv"
    supersession_map.write_text(
        "AmendmentID,DecisionID,SupersededFactKey,OverrideType,ReplacementFactTextOrValue,AppliesToRoots,AppliesToFacilities,AppliesToSections\n",
        encoding="utf-8",
    )

    manifest = planning_root / "Publication_Input_Manifest.md"
    manifest.write_text(
        "\n".join(
            [
                "# Manifest",
                "",
                f"- `EXECUTION_ROOT`: `{execution_root}`",
                f"- `PUBLICATION_ROOT`: `{publication_root}`",
                "- `DBM_OUTPUT_MODE`: `FULL_ENGINEERING_DBM`",
                f"- `SUPERSESSION_MAP_PATH`: `{supersession_map}`",
                "- `FACILITY_ID`: `04-25`",
                "- `HYPERGRAPH_USE_MODE`: `AUXILIARY_PLANNING_AND_QA` if this Gate 1 manifest is approved",
                "",
            ]
        ),
        encoding="utf-8",
    )
    parsed_manifest = parse_manifest(manifest)
    explicit = parsed_manifest["explicit"]
    assert explicit["SUPERSESSION_MAP_PATH"] == str(supersession_map)
    assert explicit["HYPERGRAPH_USE_MODE"] == "AUXILIARY_PLANNING_AND_QA"

    schema = planning_root / "Publication_Schema.md"
    schema.write_text(
        "\n".join(
            [
                "# Schema",
                "",
                "| SectionID | SectionOrder | SectionTitle | SectionType | SectionPurpose | InclusionRule | ExclusionRule | IncludeCategoryIDs | IncludeKnowledgeTypeIDs | IncludeCanonicalSchemas | ExcludeCategoryIDs | ExcludeKnowledgeTypeIDs | ExpectedInputs | ExpectedOutputShape | MaxKAFiles | SplitHint |",
                "|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|",
                "| SEC-01 | 1 | Basis | PROCESS_BASIS | Publish basis. | Include KTY. | None. | CAT-001 | KTY-001 |  |  |  | KTY files | Full section | 12 | None |",
                "",
            ]
        ),
        encoding="utf-8",
    )

    section_map = planning_root / "Section_Map.csv"
    section_map.write_text(
        "\n".join(
            [
                "SectionID,SectionTitle,SectionType,SourceDomain,CategoryID,KnowledgeTypeID,SubjectID,ArtifactPath,MappingRole,ContributionScope,SCARefs,DecisionRefs,CurrentStateBasis,LifecycleState,LifecycleSource,Notes",
                "SEC-01,Basis,PROCESS_BASIS,Root,CAT-001,KTY-001,,/tmp/input.md,PRIMARY,FULL_ARTIFACT,,,APPROVED,ACTIVE,_STATUS.md,fixture",
                "",
            ]
        ),
        encoding="utf-8",
    )

    rules = planning_root / "Publication_Rules.md"
    rules.write_text(
        "\n".join(
            [
                "# Publication Rules",
                "",
                "- DBM_OUTPUT_MODE = FULL_ENGINEERING_DBM",
                "- BodyCompletenessStandard: body completeness requires applicable design criteria, capacities, interfaces, TBDs, and design-basis tables.",
                "- TabularDataPolicy: tabular data and design-basis tables must be included, consolidated, split, or explicitly omitted with rationale.",
                "- BodyVsQAArtifactBoundaryRule: QA assertions, path inventories, and trace scaffolds must not define the main body.",
                "- High-KTY sections may summarize stable system-level design basis only when they do not omit engineering detail.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    register = planning_root / "Publication_Concordance_Register.csv"
    register.write_text(
        "AssertionKey,AssertionLabel,AuthoritySectionID,RequiredSectionIDs,ComparisonRule,ComparisonParameter\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "render_dispatch_briefs.py",
            "--publication-root",
            str(publication_root),
            "--input-manifest",
            str(manifest),
            "--schema",
            str(schema),
            "--section-map",
            str(section_map),
            "--rules",
            str(rules),
            "--concordance-register",
            str(register),
            "--dispatch-root",
            str(dispatch_root),
            "--sections-root",
            str(sections_root),
            "--package-root",
            str(package_root),
            "--package-snapshot-name",
            "RUN-SCRATCH",
        ],
    )

    assert main() == 0

    section_brief = (dispatch_root / "SEC-01_INIT-TASK.md").read_text(encoding="utf-8")
    package_brief = (dispatch_root / "DBM_PUBLISH_INIT-TASK.md").read_text(encoding="utf-8")
    assert "DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM" in section_brief
    assert "DBM_OUTPUT_MODE: FULL_ENGINEERING_DBM" in package_brief
    assert f"SUPERSESSION_MAP_PATH: {supersession_map}" in section_brief
    assert f"SUPERSESSION_MAP_PATH: {supersession_map}" in package_brief
    assert "HYPERGRAPH_USE_MODE: AUXILIARY_PLANNING_AND_QA" in package_brief
    allowed_block = package_brief.split("RuntimeOverrides:", 1)[0]
    expected_block = package_brief.split("ExpectedOutputs:", 1)[1]
    assert "AllowedWriteTargets:" in allowed_block
    assert "Publication_Content_Adequacy.md" in allowed_block
    assert "Publication_Content_Adequacy.md" in expected_block
    assert package_brief.count("Publication_Content_Adequacy.md") == 2
    assert (package_root / "RUN-SCRATCH").is_dir()
