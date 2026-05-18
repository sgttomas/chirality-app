from __future__ import annotations

import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from extract_concordance_evidence import (  # noqa: E402
    ATOM_COLUMNS,
    CLASSIFICATION_FORBIDDEN_COLUMNS,
    build_risk_inventory,
    extract_markdown_atoms,
)


def test_evidence_atom_no_classification_fields(tmp_path):
    artifact = tmp_path / "KA-01_Test.md"
    artifact.write_text("| Parameter | Value |\n|---|---|\n| Pressure | 450 psig |\n", encoding="utf-8")
    atoms = extract_markdown_atoms(
        artifact,
        {
            "sections": {"SEC-01"},
            "ktys": {"KTY-01"},
            "mapping_roles": {"PRIMARY"},
            "contribution_scopes": {"FULL_ARTIFACT"},
            "lifecycle_states": {"ACTIVE"},
        },
    )
    assert atoms
    assert not (CLASSIFICATION_FORBIDDEN_COLUMNS & set(ATOM_COLUMNS))
    assert not (CLASSIFICATION_FORBIDDEN_COLUMNS & set(atoms[0].keys()))


def test_evidence_atom_provenance_complete(tmp_path):
    artifact = tmp_path / "KA-01_Test.md"
    artifact.write_text("# Basis\nIntro line.\n| Parameter | Value |\n|---|---|\n| Pressure | 450 psig |\n", encoding="utf-8")
    atoms = extract_markdown_atoms(
        artifact,
        {
            "sections": {"SEC-01"},
            "ktys": {"KTY-01"},
            "mapping_roles": {"PRIMARY"},
            "contribution_scopes": {"FULL_ARTIFACT"},
            "lifecycle_states": {"ACTIVE"},
        },
    )
    atom = atoms[0]
    assert atom["SourceArtifact"]
    assert atom["HeadingPath"] == "Basis"
    assert atom["NearbyContext"]


def test_source_authority_risk_signal(tmp_path):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    artifact = source_dir / "source.md"
    artifact.write_text("| Parameter | Value |\n|---|---|\n| Pressure | 450 psig |\n", encoding="utf-8")
    atoms = extract_markdown_atoms(
        artifact,
        {
            "sections": {"SEC-01"},
            "ktys": {"KTY-01"},
            "mapping_roles": {"PRIMARY"},
            "contribution_scopes": {"FULL_ARTIFACT"},
            "lifecycle_states": {"ACTIVE"},
        },
    )
    assert "SOURCE_AUTHORITY" in atoms[0]["RiskSignals"]


def test_risk_inventory_emission(tmp_path):
    artifact = tmp_path / "KA-01_Test.md"
    artifact.write_text("| Parameter | Value |\n|---|---|\n| Pressure | TBD |\n", encoding="utf-8")
    atoms = extract_markdown_atoms(
        artifact,
        {
            "sections": {"SEC-01"},
            "ktys": {"KTY-01"},
            "mapping_roles": {"PRIMARY"},
            "contribution_scopes": {"FULL_ARTIFACT"},
            "lifecycle_states": {"ACTIVE"},
        },
    )
    risks = build_risk_inventory(atoms)
    assert any(row["RiskClass"] == "OPEN_TBD" for row in risks)


def test_atom_id_stability(tmp_path):
    artifact = tmp_path / "KA-01_Test.md"
    artifact.write_text("| Parameter | Value |\n|---|---|\n| Pressure | 450 psig |\n", encoding="utf-8")
    meta = {
        "sections": {"SEC-01"},
        "ktys": {"KTY-01"},
        "mapping_roles": {"PRIMARY"},
        "contribution_scopes": {"FULL_ARTIFACT"},
        "lifecycle_states": {"ACTIVE"},
    }
    first = extract_markdown_atoms(artifact, meta)[0]["AtomID"]
    second = extract_markdown_atoms(artifact, meta)[0]["AtomID"]
    assert first == second
