from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("generate_coverage_csv.py")
MIGRATION_AUTHORITY = "D-GOV-16@7584718aa32b112e415331736d1a8e68c12ac176"


def write_valid_sow(path: Path, *, migration_authority: str = "") -> None:
    marker = f"\n<!-- migration-authority: {migration_authority} -->\n" if migration_authority else ""
    (path / "ScopeOfWork.md").write_text(
        """---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-02
package_id: PKG-01
decomposition_basis: execution/_Decomposition/SOFTWARE_DECOMP.md@abc123
project_scope_refs: [SOW-001]
package_objective_refs: [OBJ-001]
---

# Scope of Work — DEL-01-02

## Purpose and Objective Traceability

- **OUT-001** — Produce the bounded output.

## Deliverable Definition — Ontology

The output is defined.

## Completion and Reliance Basis — Epistemology

- **AC-001** — The output is complete.

## Production and Verification Method — Praxeology

- **VER-001** — Inspect the output.

## Governing Values and Decisions — Axiology

Preserve accepted authority.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | SOW-001 | | AC-001 | VER-001 | Deterministic evidence |
""" + marker,
        encoding="utf-8",
    )


def test_coverage_preserves_columns_and_reports_resolved_format_states(tmp_path: Path) -> None:
    execution = tmp_path / "execution"
    working = execution / "PKG-01_Test" / "1_Working"
    legacy = working / "DEL-01-01_Legacy"
    sow = working / "DEL-01-02_Sow"
    dual = working / "DEL-01-03_Dual"
    partial = working / "DEL-01-04_Partial"
    for deliverable in (legacy, dual):
        deliverable.mkdir(parents=True)
        for name in ("Datasheet.md", "Specification.md", "Guidance.md", "Procedure.md"):
            (deliverable / name).write_text("# source\n", encoding="utf-8")
    sow.mkdir(parents=True)
    write_valid_sow(sow)
    write_valid_sow(dual, migration_authority=MIGRATION_AUTHORITY)
    partial.mkdir(parents=True)
    (partial / "Datasheet.md").write_text("# partial\n", encoding="utf-8")
    output = tmp_path / "coverage.csv"

    subprocess.run([sys.executable, str(SCRIPT), str(execution), str(output)], check=True)
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert list(rows[0]) == [
        "DeliverableID", "Package", "HasDependenciesCsv", "HasSemantic",
        "HasEstimate", "EstimateCount", "HasDatasheet", "HasSpecification",
        "HasGuidance", "HasProcedure", "HasScopeOfWork", "ProductionFormatState",
    ]
    assert rows[0]["ProductionFormatState"] == "LEGACY_FOUR_DOC"
    assert rows[0]["HasScopeOfWork"] == "N"
    assert rows[1]["ProductionFormatState"] == "SOW_V1"
    assert rows[1]["HasScopeOfWork"] == "Y"
    assert rows[2]["ProductionFormatState"] == "AMBIGUOUS"
    assert rows[3]["ProductionFormatState"] == "INVALID"

    authorized_output = tmp_path / "coverage-authorized.csv"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(execution),
            str(authorized_output),
            "--isolated-migration",
            "--migration-authority",
            MIGRATION_AUTHORITY,
        ],
        check=True,
    )
    with authorized_output.open(newline="", encoding="utf-8") as handle:
        authorized_rows = list(csv.DictReader(handle))
    assert authorized_rows[2]["ProductionFormatState"] == "MIGRATION_DUAL"
