from __future__ import annotations

import sys
from pathlib import Path


from validate_lens_register import validate_lens_register  # noqa: E402
from scan_deliverable_consistency import main as consistency_main  # noqa: E402
from validate_p3_disposition import main as p3_main, validate_p3_disposition  # noqa: E402
from validate_semantic_matrix import main as semantic_main, validate_semantic_file  # noqa: E402
from validate_semantic_pipeline_scope import (  # noqa: E402
    init_blocked_by_existing_contract,
    validate_changed_paths,
)


def write_semantic(path: Path, *, omit_matrix: str | None = None, use_sow: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=True)
    sections = [
        "# Deliverable: DEL-17-99 Example",
        "**Inputs Read:**",
        "- `_CONTEXT.md` - x",
        "- `_STATUS.md` - x",
        *(
            ["- `ScopeOfWork.md` - x"]
            if use_sow
            else [
                "- `Datasheet.md` - x",
                "- `Specification.md` - x",
                "- `Guidance.md` - x",
                "- `Procedure.md` - x",
            ]
        ),
        "**Audit:** PASS",
        "## Matrix A - Orientation (3x4) - Canonical",
        "",
        "| | **guiding** | **applying** | **judging** | **reviewing** |",
        "|---|---|---|---|---|",
        "| **normative** | prescriptive direction | mandatory practice | compliance determination | regulatory audit |",
        "| **operative** | procedural direction | practical execution | performance assessment | process audit |",
        "| **evaluative** | value orientation | merit application | worth determination | quality appraisal |",
        "## Matrix B - Conceptualization (4x4) - Canonical",
        "",
        "| | **necessity** | **sufficiency** | **completeness** | **consistency** |",
        "|---|---|---|---|---|",
        "| **data** | essential fact | adequate evidence | comprehensive record | reliable measurement |",
        "| **information** | essential signal | adequate context | comprehensive account | coherent message |",
        "| **knowledge** | fundamental understanding | competent expertise | thorough mastery | coherent understanding |",
        "| **wisdom** | essential discernment | adequate judgment | holistic insight | principled reasoning |",
    ]
    matrix_shapes = {
        "C": (["necessity", "sufficiency", "completeness", "consistency"], ["normative", "operative", "evaluative"]),
        "F": (["necessity", "sufficiency", "completeness", "consistency"], ["normative", "operative", "evaluative"]),
        "D": (["guiding", "applying", "judging", "reviewing"], ["normative", "operative", "evaluative"]),
        "K": (["normative", "operative", "evaluative"], ["guiding", "applying", "judging", "reviewing"]),
        "G": (["necessity", "sufficiency", "completeness", "consistency"], ["data", "information", "knowledge"]),
        "X": (["necessity", "sufficiency", "completeness", "consistency"], ["guiding", "applying", "judging", "reviewing"]),
        "T": (["data", "information", "knowledge", "wisdom"], ["necessity", "sufficiency", "completeness", "consistency"]),
        "E": (["data", "information", "knowledge", "wisdom"], ["guiding", "applying", "judging", "reviewing"]),
    }
    for matrix, (cols, rows) in matrix_shapes.items():
        if matrix == omit_matrix:
            continue
        sections.append(f"## Matrix {matrix} - Example")
        if matrix in {"C", "F", "D", "X", "E"}:
            sections.extend([
                "| Cell | Intermediate collection | Step 1 - Axis anchor | Step 2 - Projected contributors | Step 3 - Centroid attractor |",
                "|---|---|---|---|---|",
            ])
            for row in rows:
                for col in cols:
                    sections.append(
                        f"| {matrix}[{row}, {col}] | `L = {{a * b = test value}}` | "
                        f"`a = {row} * {col} = latent frame` | `p1 = a * test value = projected signal` | "
                        f"Centroid selects `clear signal` for test. |"
                    )
        sections.extend([
            "### Result",
            "",
            "| | " + " | ".join(f"**{col}**" for col in cols) + " |",
            "|---" + "|---" * len(cols) + "|",
        ])
        for row in rows:
            sections.append(f"| **{row}** | " + " | ".join(["clear signal"] * len(cols)) + " |")
    sections.append("## Matrix Summary")
    for matrix in ["C", "F", "D", "K", "G", "X", "T", "E"]:
        if matrix != omit_matrix:
            sections.append(f"### {matrix} - Example")
    (path / "_SEMANTIC.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def write_valid_sow(path: Path, *, extra: str = "") -> None:
    path.mkdir(parents=True, exist_ok=True)
    text = """---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-17-99
package_id: PKG-17
decomposition_basis: execution/_Decomposition/SOFTWARE_DECOMP.md@abc123
project_scope_refs: [SOW-001]
package_objective_refs: [OBJ-001]
---

# Scope of Work — DEL-17-99

## Purpose and Objective Traceability

- **OUT-001** — Produce the bounded output.

## Deliverable Definition — Ontology

The output is defined by the accepted decomposition.

## Completion and Reliance Basis — Epistemology

- **AC-001** — The bounded output is complete.

## Production and Verification Method — Praxeology

- **VER-001** — Inspect the output deterministically.

## Governing Values and Decisions — Axiology

Preserve accepted authority.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | SOW-001 | | AC-001 | VER-001 | Deterministic evidence |
"""
    (path / "ScopeOfWork.md").write_text(text + extra, encoding="utf-8")


def write_lens(path: Path, *, generic_notes: bool = False, bad_total: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=True)
    counts = {"A": 12, "B": 16, "C": 12, "F": 12, "D": 12, "X": 16, "E": 16}
    text = [
        "# Semantic Lensing Register: DEL-17-99 Example",
        "**Inputs Read:**",
        "- _CONTEXT.md - x",
        "- _STATUS.md - x",
        "- _SEMANTIC.md - x",
        "## Summary",
        f"- Total warranted items: {2 if bad_total else 1}",
        "- By matrix:",
        "- A: 1  B: 0  C: 0  F: 0  D: 0  X: 0  E: 0",
        "- By type:",
        "- Conflict: 0",
        "- VerificationGap: 1",
        "- MissingSlot: 0",
        "- WeakStatement: 0",
        "- RationaleGap: 0",
        "- Normalization: 0",
        "- TBD_Question: 0",
        "- MatrixError: 0",
    ]
    for matrix, count in counts.items():
        text.extend([
            f"## Matrix {matrix} - Example",
            "### Lens Coverage",
            "| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |",
            "|---|---|---|---|---:|---|---|",
        ])
        for idx in range(count):
            status = "HAS_ITEMS" if matrix == "A" and idx == 0 else "NO_ITEMS"
            item_count = 1 if status == "HAS_ITEMS" else 0
            note = "No incremental warranted edit beyond existing controls." if generic_notes else f"Lens-specific note {matrix}-{idx}."
            text.append(f"| {matrix}:[r{idx}]:[c{idx}] | r{idx} | c{idx} | clear signal | {item_count} | {status} | {note} |")
        if matrix == "A":
            text.extend([
                "### Warranted Items",
                "| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|",
                "| A-001 | A:[r0]:[c0] | VerificationGap | Specification | Specification | Add check. | Requirement lacks verification. | Specification.md | Requirements | NA | PROPOSAL | TBD |",
            ])
    (path / "_SEMANTIC_LENSING.md").write_text("\n".join(text) + "\n", encoding="utf-8")


def test_semantic_validator_accepts_required_shape(tmp_path: Path) -> None:
    write_semantic(tmp_path)
    assert validate_semantic_file(tmp_path) == []


def test_semantic_validator_rejects_missing_matrix(tmp_path: Path) -> None:
    write_semantic(tmp_path, omit_matrix="K")
    findings = validate_semantic_file(tmp_path)
    assert any(f.category == "MISSING_MATRIX_K" for f in findings)


def test_lens_validator_accepts_required_shape(tmp_path: Path) -> None:
    write_lens(tmp_path)
    assert validate_lens_register(tmp_path) == []


def test_lens_validator_rejects_generic_no_items_notes(tmp_path: Path) -> None:
    write_lens(tmp_path, generic_notes=True)
    findings = validate_lens_register(tmp_path)
    assert any(f.category == "GENERIC_NO_ITEMS_NOTE" for f in findings)


def test_lens_validator_rejects_bad_summary_total(tmp_path: Path) -> None:
    write_lens(tmp_path, bad_total=True)
    findings = validate_lens_register(tmp_path)
    assert any(f.category == "BAD_SUMMARY_TOTAL" for f in findings)


def test_p3_disposition_accepts_item_accounting(tmp_path: Path) -> None:
    write_lens(tmp_path)
    (tmp_path / "Procedure.md").write_text("Applied A-001 with source reread evidence.\n", encoding="utf-8")
    assert validate_p3_disposition(tmp_path) == []


def test_p3_disposition_rejects_stale_item_reference(tmp_path: Path) -> None:
    write_lens(tmp_path)
    (tmp_path / "Procedure.md").write_text("Applied A-002 with source reread evidence.\n", encoding="utf-8")
    findings = validate_p3_disposition(tmp_path)
    assert any(f.category == "MISSING_ITEM_DISPOSITION" for f in findings)
    assert any(f.category == "UNKNOWN_ITEM_REFERENCE" for f in findings)


def test_scope_validator_accepts_init_step_scope() -> None:
    findings = validate_changed_paths(
        [
            "execution/PKG/DEL/ScopeOfWork.md",
            "execution/PKG/DEL/_STATUS.md",
            "execution/PKG/DEL/_run_records/TASK_RUN.md",
        ],
        "execution/PKG/DEL",
        "init",
    )
    assert findings == []


def test_scope_validator_rejects_semantic_file_under_init_step() -> None:
    findings = validate_changed_paths(
        ["execution/PKG/DEL/_SEMANTIC.md"],
        "execution/PKG/DEL",
        "init",
    )
    assert any(f.category == "OUT_OF_SCOPE_PATH" for f in findings)


def test_init_step_fails_closed_when_production_contract_exists() -> None:
    assert init_blocked_by_existing_contract("SOW_V1") is True
    assert init_blocked_by_existing_contract("MIGRATION_DUAL") is True


def test_init_step_allows_the_genuine_pre_init_states() -> None:
    # A pre-INIT deliverable resolves INVALID ("missing production contract").
    # Blocking that would reject exactly the runs INIT exists to perform.
    assert init_blocked_by_existing_contract("INVALID") is False
    assert init_blocked_by_existing_contract("LEGACY_FOUR_DOC") is False
    assert init_blocked_by_existing_contract("AMBIGUOUS") is False


def test_scope_validator_accepts_semantic_step_scope() -> None:
    findings = validate_changed_paths(
        [
            "execution/PKG/DEL/_SEMANTIC.md",
            "execution/PKG/DEL/_STATUS.md",
            "execution/PKG/DEL/_run_records/TASK_RUN.md",
        ],
        "execution/PKG/DEL",
        "semantic",
    )
    assert findings == []


def test_scope_validator_rejects_wrong_step_file() -> None:
    findings = validate_changed_paths(
        ["execution/PKG/DEL/_SEMANTIC_LENSING.md"],
        "execution/PKG/DEL",
        "semantic",
    )
    assert any(f.category == "OUT_OF_SCOPE_PATH" for f in findings)


def test_scope_validator_rejects_dirty_outside_when_strict() -> None:
    findings = validate_changed_paths(
        ["execution/PKG/OTHER/Procedure.md"],
        "execution/PKG/DEL",
        "p3",
        strict_repo=True,
    )
    assert any(f.category == "DIRTY_OUTSIDE_DELIVERABLE" for f in findings)


def test_scope_validator_selects_sow_p3_write_surface() -> None:
    findings = validate_changed_paths(
        ["execution/PKG/DEL/ScopeOfWork.md"],
        "execution/PKG/DEL",
        "p3",
        production_format="SOW_V1",
    )
    assert findings == []
    denied = validate_changed_paths(
        ["execution/PKG/DEL/Specification.md"],
        "execution/PKG/DEL",
        "p3",
        production_format="SOW_V1",
    )
    assert any(f.category == "OUT_OF_SCOPE_PATH" for f in denied)


def test_semantic_cli_rejects_declared_sow_when_format_is_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate_semantic_matrix.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert semantic_main() == 2


def test_p3_cli_rejects_declared_sow_when_format_is_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["validate_p3_disposition.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert p3_main() == 2


def test_consistency_cli_rejects_declared_sow_when_format_is_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_deliverable_consistency.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert consistency_main() == 2


def test_semantic_p3_and_consistency_clis_accept_resolved_sow(tmp_path: Path, monkeypatch) -> None:
    write_valid_sow(tmp_path, extra="\nA-001 disposition evidence.\n")
    write_semantic(tmp_path, use_sow=True)
    write_lens(tmp_path)

    monkeypatch.setattr(
        sys,
        "argv",
        ["validate_semantic_matrix.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert semantic_main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        ["validate_p3_disposition.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert p3_main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_deliverable_consistency.py", str(tmp_path), "--production-format", "SOW_V1"],
    )
    assert consistency_main() == 0
