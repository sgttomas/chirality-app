#!/usr/bin/env python3
"""Manifest-backed source catalog coverage."""
from __future__ import annotations

import csv
import hashlib
import sqlite3
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
BUILD = TOOLS_DIR / "build_source_database.py"
VALIDATE = TOOLS_DIR / "validate_source_database.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "SourceDocID",
                "SourceName",
                "RepoRelPath",
                "SourceGroup",
                "AuthorityRole",
                "IncludeInIndex",
                "ArchiveState",
                "ExpectedSha256",
                "Notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def run_cmd(*args: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(arg) for arg in args)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def latest_snapshot(domain_root: Path) -> Path:
    latest = domain_root / "_LocalIndexes" / "_LATEST.md"
    for line in latest.read_text(encoding="utf-8").splitlines():
        if line.startswith("Latest:"):
            return (latest.parent / line.split(":", 1)[1].strip()).resolve()
    raise AssertionError("no Latest pointer found")


def rows_from(snapshot: Path, export_name: str) -> list[dict[str, str]]:
    with (snapshot / export_name).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_manifest_repo_markdown_is_cataloged_chunked_and_validated(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    domain_root = tmp_path / "domain"
    source = repo_root / "docs" / "CONTRACT.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Contract\n\nTASK hard authorization boundary.\n", encoding="utf-8")
    (domain_root / "_Sources").mkdir(parents=True)
    write_manifest(
        domain_root / "_Sources" / "Source_Manifest.csv",
        [
            {
                "SourceDocID": "SRC-CONTRACT",
                "SourceName": "Contract",
                "RepoRelPath": "docs/CONTRACT.md",
                "SourceGroup": "ROOT_GOVERNANCE_DOCS",
                "AuthorityRole": "GOVERNANCE_AUTHORITY",
                "IncludeInIndex": "YES",
                "ArchiveState": "ACTIVE",
                "ExpectedSha256": sha256(source),
                "Notes": "test",
            }
        ],
    )

    result = run_cmd(
        BUILD,
        "--domain-root",
        domain_root,
        "--repo-root",
        repo_root,
        "--source-manifest",
        domain_root / "_Sources" / "Source_Manifest.csv",
    )
    assert result.returncode == 0, result.stderr
    snapshot = latest_snapshot(domain_root)

    artifacts = rows_from(snapshot, "Artifacts.csv")
    chunks = rows_from(snapshot, "Chunks.csv")
    assert [row["rel_path"] for row in artifacts] == ["@repo/docs/CONTRACT.md"]
    assert chunks
    assert chunks[0]["rel_path"] == "@repo/docs/CONTRACT.md"
    assert "TASK hard authorization boundary" in chunks[0]["text"]

    validation = run_cmd(
        VALIDATE,
        "--snapshot",
        domain_root / "_LocalIndexes" / "_LATEST.md",
        "--domain-root",
        domain_root,
        "--repo-root",
        repo_root,
    )
    assert validation.returncode == 0, validation.stdout + validation.stderr
    assert "PASS:" in validation.stdout


def test_manifest_expected_hash_mismatch_is_reported(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    domain_root = tmp_path / "domain"
    source = repo_root / "docs" / "CONTRACT.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Contract\n\nHash mismatch surface.\n", encoding="utf-8")
    (domain_root / "_Sources").mkdir(parents=True)
    write_manifest(
        domain_root / "_Sources" / "Source_Manifest.csv",
        [
            {
                "SourceDocID": "SRC-CONTRACT",
                "SourceName": "Contract",
                "RepoRelPath": "docs/CONTRACT.md",
                "SourceGroup": "ROOT_GOVERNANCE_DOCS",
                "AuthorityRole": "GOVERNANCE_AUTHORITY",
                "IncludeInIndex": "YES",
                "ArchiveState": "ACTIVE",
                "ExpectedSha256": "0" * 64,
                "Notes": "test",
            }
        ],
    )

    result = run_cmd(
        BUILD,
        "--domain-root",
        domain_root,
        "--repo-root",
        repo_root,
        "--source-manifest",
        domain_root / "_Sources" / "Source_Manifest.csv",
    )
    assert result.returncode == 0, result.stderr
    validation = run_cmd(
        VALIDATE,
        "--snapshot",
        domain_root / "_LocalIndexes" / "_LATEST.md",
        "--domain-root",
        domain_root,
        "--repo-root",
        repo_root,
    )
    assert validation.returncode == 1
    assert "HASH_MISMATCH" in validation.stdout


def test_manifest_mode_indexes_decomposition_ledger_and_section_nodes(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    domain_root = tmp_path / "domain"
    source = repo_root / "docs" / "CONTRACT.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Contract\n\nSource text.\n", encoding="utf-8")
    (domain_root / "_Sources").mkdir(parents=True)
    write_manifest(
        domain_root / "_Sources" / "Source_Manifest.csv",
        [
            {
                "SourceDocID": "SRC-CONTRACT",
                "SourceName": "Contract",
                "RepoRelPath": "docs/CONTRACT.md",
                "SourceGroup": "ROOT_GOVERNANCE_DOCS",
                "AuthorityRole": "GOVERNANCE_AUTHORITY",
                "IncludeInIndex": "YES",
                "ArchiveState": "ACTIVE",
                "ExpectedSha256": sha256(source),
                "Notes": "test",
            }
        ],
    )

    section_dir = domain_root / "_Decomposition" / "source_section_nodes"
    section_dir.mkdir(parents=True)
    with (section_dir / "SRC-CONTRACT_section_nodes.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["SectionID", "SourceDoc", "Title", "Text", "HtmlAnchor"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "SectionID": "SEC-CON-0001",
                "SourceDoc": "SRC-CONTRACT",
                "Title": "Contract Section",
                "Text": "Section-node evidence text.",
                "HtmlAnchor": "SRC-CONTRACT.html#SEC-CON-0001",
            }
        )

    with (domain_root / "_Decomposition" / "Atomic_Domain_Ledger.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "AtomicUnitID",
                "SourceDoc",
                "SourcePrefix",
                "LocalSeq",
                "UnitStatement",
                "SourceRef",
                "ContentHash",
                "InOutStatus",
                "SectionID",
                "DispatchUnitID",
                "Corrects",
                "Notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "AtomicUnitID": "HBA-CON-00001",
                "SourceDoc": "SRC-CONTRACT",
                "SourcePrefix": "CON",
                "LocalSeq": "1",
                "UnitStatement": "Ledger atom evidence text.",
                "SourceRef": "@repo/docs/CONTRACT.md:L0001|domains/test#SEC-CON-0001",
                "ContentHash": "abc123",
                "InOutStatus": "IN",
                "SectionID": "SEC-CON-0001",
                "DispatchUnitID": "UNIT-CON-0001",
                "Corrects": "",
                "Notes": "",
            }
        )

    result = run_cmd(
        BUILD,
        "--domain-root",
        domain_root,
        "--repo-root",
        repo_root,
        "--source-manifest",
        domain_root / "_Sources" / "Source_Manifest.csv",
    )
    assert result.returncode == 0, result.stderr
    snapshot = latest_snapshot(domain_root)

    artifacts = rows_from(snapshot, "Artifacts.csv")
    chunks = rows_from(snapshot, "Chunks.csv")
    source_docs = rows_from(snapshot, "SourceDocs.csv")

    assert {row["artifact_role"] for row in artifacts} == {
        "DECOMPOSITION_LEDGER_CSV",
        "SECTION_NODES_CSV",
        "SOURCE_MARKDOWN",
    }
    chunk_types = {row["chunk_type"] for row in chunks}
    assert {"LEDGER_ATOM", "MARKDOWN_SECTION", "SECTION_NODE"} <= chunk_types
    assert {row["source_doc_id"] for row in chunks} == {"SRC-CONTRACT"}
    [source_doc] = source_docs
    assert source_doc["source_doc_id"] == "SRC-CONTRACT"
    assert source_doc["source_root_rel_path"] == "@repo/docs/CONTRACT.md"
    assert source_doc["section_nodes_artifact_id"]


def test_without_manifest_keeps_piping_design_style_local_source_behavior(tmp_path: Path) -> None:
    domain_root = tmp_path / "domain"
    source = domain_root / "_Sources" / "Handbook" / "Handbook.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Handbook\n\nExisting local source behavior.\n", encoding="utf-8")

    result = run_cmd(BUILD, "--domain-root", domain_root)
    assert result.returncode == 0, result.stderr
    snapshot = latest_snapshot(domain_root)
    artifacts = rows_from(snapshot, "Artifacts.csv")
    chunks = rows_from(snapshot, "Chunks.csv")
    assert [row["rel_path"] for row in artifacts] == ["_Sources/Handbook/Handbook.md"]
    assert chunks
    assert chunks[0]["rel_path"] == "_Sources/Handbook/Handbook.md"

    con = sqlite3.connect(snapshot / "catalog.sqlite")
    try:
        count = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    finally:
        con.close()
    assert count == 1
