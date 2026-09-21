"""Fixture tests for validate_decomposition_registers.py.

Fixtures are built in tmp_path so the tests never read a live project corpus.
Coverage targets, per the OI-013 closure contract:
  * both named evidence sub-classes, reported distinctly;
  * ANCHOR-row cleanliness under the same rules;
  * a clean synthetic register that produces zero findings;
  * cross-register (XRG) and dependency-binding (DRB) families;
  * report-only posture and the three exit codes.
"""

from __future__ import annotations

import csv
import os
import subprocess
import sys
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parent

import validate_decomposition_registers as vdr  # noqa: E402
from validate_dependencies_schema import REQUIRED_COLUMNS  # noqa: E402

TOOL = VALIDATION_DIR / "validate_decomposition_registers.py"

DELIVERABLE_COLUMNS = [
    "DeliverableID", "PackageID", "Name", "Description", "Type", "ResponsibleParty",
    "AnticipatedArtifacts", "CoversScopeItems", "SupportsObjectives",
    "ContextEnvelope", "ContextEnvelopeNotes", "PhaseHint",
]
LEDGER_COLUMNS = [
    "ScopeItemID", "InOutStatus", "ScopeItemStatement", "SourceRef", "PackageID",
    "DeliverableIDs", "ObjectiveIDs", "DecisionRef", "OpenIssue", "Notes",
]
CONTEXT_QA_COLUMNS = [
    "DeliverableID", "PackageID", "ContextEnvelope", "Risk", "RecommendedAction", "Notes",
]


# --------------------------------------------------------------------------
# Fixture construction
# --------------------------------------------------------------------------

def write_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def anchor_row(seq: str = "001", **overrides: str) -> dict[str, str]:
    """A well-formed ANCHOR row: SourceRef is a locus, EvidenceQuote is source text."""
    row = {column: "" for column in REQUIRED_COLUMNS}
    row.update(
        {
            "RegisterSchemaVersion": "v3.1",
            "DependencyID": f"DEP-01-01-{seq}",
            "FromPackageID": "PKG-01",
            "FromDeliverableID": "DEL-01-01",
            "FromDeliverableName": "Record tier schema",
            "DependencyClass": "ANCHOR",
            "AnchorType": "TRACES_TO_REQUIREMENT",
            "Direction": "UPSTREAM",
            "DependencyType": "OTHER",
            "TargetType": "REQUIREMENT",
            "TargetPackageID": "",
            "TargetDeliverableID": "",
            "TargetRefID": "SOW-001",
            "TargetName": "Record tier entity model",
            "TargetLocation": "execution/_Decomposition/ScopeLedger.csv",
            "Statement": "DEL-01-01 covers scope item SOW-001.",
            "EvidenceFile": "execution/_Decomposition/ScopeLedger.csv",
            "SourceRef": "ScopeLedger.csv row SOW-001",
            "EvidenceQuote": "DeliverableIDs include DEL-01-01",
            "Explicitness": "EXPLICIT",
            "RequiredMaturity": "SEMANTIC_READY",
            "ProposedMaturity": "SEMANTIC_READY",
            "SatisfactionStatus": "TBD",
            "Confidence": "HIGH",
            "Origin": "DECLARED",
            "FirstSeen": "2026-07-25",
            "LastSeen": "2026-07-25",
            "Status": "ACTIVE",
            "Notes": "",
        }
    )
    row.update(overrides)
    return row


def execution_row(seq: str = "003", **overrides: str) -> dict[str, str]:
    """A well-formed EXECUTION row."""
    row = anchor_row(seq)
    row.update(
        {
            "DependencyClass": "EXECUTION",
            "AnchorType": "NOT_APPLICABLE",
            "DependencyType": "PREREQUISITE",
            "TargetType": "DELIVERABLE",
            "TargetPackageID": "PKG-02",
            "TargetDeliverableID": "DEL-02-01",
            "TargetRefID": "DEL-02-01",
            "TargetName": "Status parser",
            "Statement": "DEL-01-01 must precede DEL-02-01.",
            "EvidenceFile": "execution/_Decomposition/ScopeLedger.csv",
            "SourceRef": "PLAN dag gate exhibit, row E-A01",
            "EvidenceQuote": "the record tier underlies the parser items",
            "Origin": "EXTRACTED",
        }
    )
    row.update(overrides)
    return row


def build_workspace(
    root: Path,
    registers: dict[str, list[dict[str, str]]] | None = None,
    deliverables: list[dict[str, str]] | None = None,
    ledger: list[dict[str, str]] | None = None,
    context_qa: list[dict[str, str]] | None = None,
) -> Path:
    """Build a minimal, internally consistent two-deliverable execution root."""
    execution_root = root / "execution"
    decomposition = execution_root / "_Decomposition"

    deliverables = deliverables if deliverables is not None else [
        {
            "DeliverableID": "DEL-01-01", "PackageID": "PKG-01",
            "Name": "Record tier schema", "Description": "d", "Type": "CODE",
            "ResponsibleParty": "TBD", "AnticipatedArtifacts": "a",
            "CoversScopeItems": "SOW-001", "SupportsObjectives": "OBJ-001",
            "ContextEnvelope": "S", "ContextEnvelopeNotes": "", "PhaseHint": "P1",
        },
        {
            "DeliverableID": "DEL-02-01", "PackageID": "PKG-02",
            "Name": "Status parser", "Description": "d", "Type": "CODE",
            "ResponsibleParty": "TBD", "AnticipatedArtifacts": "a",
            "CoversScopeItems": "SOW-002", "SupportsObjectives": "OBJ-001",
            "ContextEnvelope": "M", "ContextEnvelopeNotes": "", "PhaseHint": "P1",
        },
    ]
    ledger = ledger if ledger is not None else [
        {
            "ScopeItemID": "SOW-001", "InOutStatus": "IN", "ScopeItemStatement": "s",
            "SourceRef": "§7.1", "PackageID": "PKG-01", "DeliverableIDs": "DEL-01-01",
            "ObjectiveIDs": "OBJ-001", "DecisionRef": "", "OpenIssue": "FALSE", "Notes": "",
        },
        {
            "ScopeItemID": "SOW-002", "InOutStatus": "IN", "ScopeItemStatement": "s",
            "SourceRef": "§7.2", "PackageID": "PKG-02", "DeliverableIDs": "DEL-02-01",
            "ObjectiveIDs": "OBJ-001", "DecisionRef": "", "OpenIssue": "FALSE", "Notes": "",
        },
    ]
    context_qa = context_qa if context_qa is not None else [
        {"DeliverableID": "DEL-01-01", "PackageID": "PKG-01", "ContextEnvelope": "S",
         "Risk": "LOW", "RecommendedAction": "None", "Notes": ""},
        {"DeliverableID": "DEL-02-01", "PackageID": "PKG-02", "ContextEnvelope": "M",
         "Risk": "LOW", "RecommendedAction": "None", "Notes": ""},
    ]

    write_csv(decomposition / "Deliverables.csv", DELIVERABLE_COLUMNS, deliverables)
    write_csv(decomposition / "ScopeLedger.csv", LEDGER_COLUMNS, ledger)
    write_csv(decomposition / "ContextBudgetQA.csv", CONTEXT_QA_COLUMNS, context_qa)

    if registers is None:
        registers = {
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [anchor_row(), execution_row()],
            "PKG-02_Parsers/1_Working/DEL-02-01_Status_parser": [
                anchor_row(
                    "001", DependencyID="DEP-02-01-001", FromPackageID="PKG-02",
                    FromDeliverableID="DEL-02-01", FromDeliverableName="Status parser",
                    TargetRefID="SOW-002", Statement="DEL-02-01 covers SOW-002.",
                )
            ],
        }
    for relative, rows in registers.items():
        write_csv(execution_root / relative / "Dependencies.csv", REQUIRED_COLUMNS, rows)
    return execution_root


def codes(report: dict) -> dict[str, int]:
    return report["findings_by_code"]


def ids_for(report: dict, code: str) -> list[str]:
    return [f["row_id"] for f in report["findings"] if f["code"] == code]


# --------------------------------------------------------------------------
# Clean baseline
# --------------------------------------------------------------------------

def test_clean_synthetic_workspace_is_finding_free(tmp_path: Path) -> None:
    execution_root = build_workspace(tmp_path)
    report = vdr.run(execution_root)

    assert report["findings"] == []
    assert report["registers_scanned"] == 2
    assert report["dependency_rows"] == 3
    assert report["deliverables_declared"] == 2
    assert report["error_count"] == 0
    assert report["warning_count"] == 0
    metrics = report["row_class_metrics"]
    assert metrics["ANCHOR"]["rows"] == 2
    assert metrics["ANCHOR"]["well_formed_evidence"] == 2
    assert metrics["EXECUTION"]["well_formed_evidence"] == 1


# --------------------------------------------------------------------------
# OI-013 sub-class (a): locus/quote confusion
# --------------------------------------------------------------------------

def test_locus_quote_duplication_is_detected_as_its_own_subclass(tmp_path: Path) -> None:
    pasted = 'OI-012 basis: "driving edges: PKG-07/08/09"'
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row(),
                execution_row(SourceRef=pasted, EvidenceQuote=pasted),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report)["EVQ-001"] == 1
    assert ids_for(report, "EVQ-001") == ["DEP-01-01-003"]
    # Reported distinctly: duplication is not also counted as empty-evidence.
    assert "EVQ-003" not in codes(report)
    assert "EVQ-004" not in codes(report)
    metrics = report["row_class_metrics"]
    assert metrics["EXECUTION"]["locus_quote_duplication"] == 1
    assert metrics["EXECUTION"]["well_formed_evidence"] == 0
    assert metrics["ANCHOR"]["well_formed_evidence"] == 1


def test_quote_shaped_locus_is_a_separate_warning(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row(),
                execution_row(
                    SourceRef='§3 mapping notes: "parser items underlie OBJ-001"',
                    EvidenceQuote="parser items underlie OBJ-001",
                ),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report) == {"EVQ-002": 1}
    assert report["error_count"] == 0
    assert report["warning_count"] == 1
    assert report["row_class_metrics"]["EXECUTION"]["quote_shaped_locus"] == 1


# --------------------------------------------------------------------------
# OI-013 sub-class (b): empty-evidence rows
# --------------------------------------------------------------------------

def test_empty_evidence_row_reports_both_cells_distinctly(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row(),
                execution_row(SourceRef="location TBD", EvidenceQuote=""),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report) == {"EVQ-003": 1, "EVQ-004": 1}
    assert ids_for(report, "EVQ-003") == ["DEP-01-01-003"]
    assert ids_for(report, "EVQ-004") == ["DEP-01-01-003"]
    # The empty-evidence class must NOT be reported as locus/quote duplication,
    # even though both cells are "equal" when both are blank.
    assert "EVQ-001" not in codes(report)
    metrics = report["row_class_metrics"]["EXECUTION"]
    assert metrics["empty_evidence_quote"] == 1
    assert metrics["placeholder_locus"] == 1
    assert metrics["locus_quote_duplication"] == 0


def test_blank_source_ref_and_quote_is_empty_evidence_not_duplication(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                execution_row(SourceRef="", EvidenceQuote=""),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert "EVQ-001" not in codes(report)
    assert codes(report)["EVQ-003"] == 1
    assert codes(report)["EVQ-004"] == 1


def test_placeholder_locus_vocabulary(tmp_path: Path) -> None:
    placeholders = ["location TBD", "TBD", "n/a", "N/A", "none", "?", "--", "  tbd  "]
    citable = ["ScopeLedger.csv row SOW-001", "§7.1", "PLAN §4.2 exhibit row E-A01",
               "Deliverables.csv row DEL-01-01"]
    for value in placeholders:
        assert vdr.PLACEHOLDER_LOCUS.match(value), f"{value!r} should read as a placeholder"
    for value in citable:
        assert not vdr.PLACEHOLDER_LOCUS.match(value), f"{value!r} is a real locus"


# --------------------------------------------------------------------------
# Row-class awareness
# --------------------------------------------------------------------------

def test_anchor_rows_are_checked_and_reported_separately(tmp_path: Path) -> None:
    """ANCHOR rows are subject to the same rules; the summary keeps classes apart."""
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", SourceRef="dup text", EvidenceQuote="dup text"),
                anchor_row("002"),
                execution_row(),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert ids_for(report, "EVQ-001") == ["DEP-01-01-001"]
    assert [f["row_class"] for f in report["findings"]] == ["ANCHOR"]
    metrics = report["row_class_metrics"]
    assert metrics["ANCHOR"]["rows"] == 2
    assert metrics["ANCHOR"]["locus_quote_duplication"] == 1
    assert metrics["ANCHOR"]["well_formed_evidence"] == 1
    assert metrics["EXECUTION"]["well_formed_evidence"] == 1


def test_evidence_file_coverage_and_resolution_are_distinct_metrics(tmp_path: Path) -> None:
    """The analyze_dep_closure.py lesson: populated != resolves != quote quality."""
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", EvidenceFile=""),
                anchor_row("002", EvidenceFile="execution/_Decomposition/NoSuchFile.csv"),
                anchor_row("003"),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report) == {"EVQ-005": 1, "EVQ-006": 1}
    metrics = report["row_class_metrics"]["ANCHOR"]
    assert metrics["rows"] == 3
    assert metrics["evidence_file_populated"] == 2   # coverage
    assert metrics["evidence_file_resolved"] == 1    # resolution
    assert metrics["well_formed_evidence"] == 1


# --------------------------------------------------------------------------
# Cross-register consistency (XRG)
# --------------------------------------------------------------------------

def test_non_reciprocal_scope_coverage_is_reported_from_both_sides(tmp_path: Path) -> None:
    execution_root = build_workspace(tmp_path)
    ledger_path = execution_root / "_Decomposition" / "ScopeLedger.csv"
    rows = list(csv.DictReader(ledger_path.open(encoding="utf-8-sig")))
    rows[0]["DeliverableIDs"] = "DEL-02-01"  # SOW-001 now points at the wrong deliverable
    write_csv(ledger_path, LEDGER_COLUMNS, rows)

    report = vdr.run(execution_root, families=("XRG",))

    assert codes(report)["XRG-003"] == 2  # once from the ledger, once from Deliverables
    assert codes(report)["XRG-004"] == 1  # PackageID PKG-01 vs DEL-02-01 in PKG-02


def test_unknown_ids_objectives_and_context_budget_drift(tmp_path: Path) -> None:
    execution_root = build_workspace(tmp_path)
    decomposition = execution_root / "_Decomposition"

    ledger = list(csv.DictReader((decomposition / "ScopeLedger.csv").open(encoding="utf-8-sig")))
    ledger[0]["DeliverableIDs"] = "DEL-09-09"       # XRG-001
    ledger[1]["ObjectiveIDs"] = "OBJ-001;OBJ-007"   # XRG-005
    ledger.append({
        "ScopeItemID": "SOW-003", "InOutStatus": "IN", "ScopeItemStatement": "s",
        "SourceRef": "§7.3", "PackageID": "PKG-01", "DeliverableIDs": "",
        "ObjectiveIDs": "OBJ-001", "DecisionRef": "", "OpenIssue": "FALSE", "Notes": "",
    })                                              # XRG-006
    ledger.append({
        "ScopeItemID": "SOW-004", "InOutStatus": "OUT", "ScopeItemStatement": "s",
        "SourceRef": "§7.4", "PackageID": "PKG-01", "DeliverableIDs": "DEL-01-01",
        "ObjectiveIDs": "", "DecisionRef": "", "OpenIssue": "FALSE", "Notes": "",
    })                                              # XRG-007
    write_csv(decomposition / "ScopeLedger.csv", LEDGER_COLUMNS, ledger)

    deliverables = list(csv.DictReader((decomposition / "Deliverables.csv").open(encoding="utf-8-sig")))
    deliverables[0]["CoversScopeItems"] = "SOW-001;SOW-999"  # XRG-002
    deliverables[1]["PhaseHint"] = ""                        # XRG-008
    write_csv(decomposition / "Deliverables.csv", DELIVERABLE_COLUMNS, deliverables)

    context_qa = list(csv.DictReader((decomposition / "ContextBudgetQA.csv").open(encoding="utf-8-sig")))
    context_qa[0]["ContextEnvelope"] = "XL"                  # XRG-010
    context_qa.pop(1)                                        # XRG-009
    write_csv(decomposition / "ContextBudgetQA.csv", CONTEXT_QA_COLUMNS, context_qa)

    report = vdr.run(execution_root, families=("XRG",))
    found = codes(report)

    assert found["XRG-001"] == 1
    assert found["XRG-002"] == 1
    assert found["XRG-005"] == 1
    assert found["XRG-006"] == 1
    assert found["XRG-007"] == 1
    assert found["XRG-008"] == 1
    assert found["XRG-009"] == 1
    assert found["XRG-010"] == 1


def test_missing_companion_registers_are_skipped_not_errors(tmp_path: Path) -> None:
    execution_root = build_workspace(tmp_path)
    (execution_root / "_Decomposition" / "ScopeLedger.csv").unlink()

    report = vdr.run(execution_root, families=("XRG",))

    assert report["findings"] == []
    assert report["skipped"] == ["XRG family (Deliverables.csv and/or ScopeLedger.csv absent)"]


# --------------------------------------------------------------------------
# Dependency-register binding (DRB)
# --------------------------------------------------------------------------

def test_dependency_binding_defects(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001"),
                anchor_row("002", FromPackageID="PKG-09"),                  # DRB-003
                anchor_row("003", FromDeliverableName="Stale old name"),    # DRB-004
                execution_row("004", TargetDeliverableID="DEL-09-09"),      # DRB-005
                execution_row("001"),                                       # DRB-007 duplicate
            ],
            "PKG-02_Parsers/1_Working/DEL-02-01_Status_parser": [
                anchor_row("005"),  # FromDeliverableID DEL-01-01 in a DEL-02-01 folder
            ],
        },
    )
    report = vdr.run(execution_root, families=("DRB",))
    found = codes(report)

    assert found["DRB-001"] == 1
    assert found["DRB-003"] == 1
    assert found["DRB-004"] == 1
    assert found["DRB-005"] == 1
    assert found["DRB-007"] == 1


def test_unknown_from_deliverable_and_id_prefix(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", DependencyID="DEP-07-07-001"),  # DRB-006
            ],
            "PKG-09_Ghost/1_Working/DEL-09-09_Ghost": [
                anchor_row("001", DependencyID="DEP-09-09-001", FromDeliverableID="DEL-09-09",
                           FromPackageID="PKG-09", FromDeliverableName="Ghost"),  # DRB-002
            ],
        },
    )
    report = vdr.run(execution_root, families=("DRB",))
    found = codes(report)

    assert found["DRB-006"] == 1
    assert found["DRB-002"] == 1
    assert found["DRB-008"] == 1  # DEL-02-01 declared but has no register


# --------------------------------------------------------------------------
# Schema delegation, posture, and CLI contract
# --------------------------------------------------------------------------

def test_schema_family_delegates_to_validate_dependencies_schema(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", DependencyType="ARCHITECTURE_BASIS"),
            ]
        },
    )
    report = vdr.run(execution_root, families=("SCH",))

    assert codes(report)["SCH-001"] >= 1
    assert any("invalid DependencyType" in f["detail"] for f in report["findings"])


def test_validator_never_mutates_inputs(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                execution_row(SourceRef="location TBD", EvidenceQuote=""),
            ]
        },
    )
    before = {
        path: path.read_bytes()
        for path in sorted(execution_root.rglob("*.csv"))
    }

    vdr.run(execution_root)

    after = {path: path.read_bytes() for path in sorted(execution_root.rglob("*.csv"))}
    assert before == after


def test_run_is_deterministic(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", SourceRef="dup", EvidenceQuote="dup"),
                execution_row(SourceRef="location TBD", EvidenceQuote=""),
            ]
        },
    )
    first = vdr.run(execution_root)
    second = vdr.run(execution_root)
    assert first == second


def test_cli_exit_codes_and_json_report(tmp_path: Path) -> None:
    execution_root = build_workspace(tmp_path)
    json_out = tmp_path / "report.json"

    clean = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root), "--json", str(json_out)],
        capture_output=True, text=True,
    )
    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert json_out.is_file()
    assert "Evidence-cell metrics by row class" in clean.stdout

    # Findings -> exit 1.
    register = execution_root / "PKG-01_Core/1_Working/DEL-01-01_Record_tier/Dependencies.csv"
    rows = list(csv.DictReader(register.open(encoding="utf-8-sig")))
    rows[1]["EvidenceQuote"] = ""
    write_csv(register, REQUIRED_COLUMNS, rows)
    findings = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root)], capture_output=True, text=True
    )
    assert findings.returncode == 1
    assert "EVQ-003" in findings.stdout

    # Operational error -> exit 2.
    missing = subprocess.run(
        [sys.executable, str(TOOL), str(tmp_path / "nope")], capture_output=True, text=True
    )
    assert missing.returncode == 2

    unknown_family = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root), "--families", "NOPE"],
        capture_output=True, text=True,
    )
    assert unknown_family.returncode == 2

    listing = subprocess.run(
        [sys.executable, str(TOOL), "--list-checks"], capture_output=True, text=True
    )
    assert listing.returncode == 0
    assert "EVQ-001" in listing.stdout


def test_os_level_read_failures_are_operational_not_findings(tmp_path: Path) -> None:
    """R-05: PermissionError/IsADirectoryError must exit 2, not 1."""
    execution_root = build_workspace(tmp_path)
    register = execution_root / "PKG-01_Core/1_Working/DEL-01-01_Record_tier/Dependencies.csv"

    # IsADirectoryError: replace the register with a directory of the same name.
    register.unlink()
    register.mkdir()
    try:
        vdr.read_register(register)
    except vdr.OperationalError as exc:
        assert "unreadable" in str(exc)
    else:
        raise AssertionError("a directory in place of a register must raise OperationalError")
    register.rmdir()

    # PermissionError via an unreadable file.
    write_csv(register, REQUIRED_COLUMNS, [anchor_row()])
    register.chmod(0o000)
    try:
        vdr.read_register(register)
    except vdr.OperationalError as exc:
        assert "unreadable" in str(exc)
    except PermissionError:  # pragma: no cover - only if run as root
        pass
    else:
        if not os.access(register, os.R_OK):  # pragma: no cover
            raise AssertionError("an unreadable register must raise OperationalError")
    finally:
        register.chmod(0o644)


def test_registers_in_later_lifecycle_folders_are_scanned(tmp_path: Path) -> None:
    """R-10a: a promoted deliverable's register must not drop out of the corpus."""
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/2_Checking/DEL-01-01_Record_tier": [anchor_row(), execution_row()],
            "PKG-02_Parsers/3_Issued/DEL-02-01_Status_parser": [
                anchor_row("001", DependencyID="DEP-02-01-001", FromPackageID="PKG-02",
                           FromDeliverableID="DEL-02-01", FromDeliverableName="Status parser"),
            ],
        },
    )
    report = vdr.run(execution_root)

    assert report["registers_scanned"] == 2
    assert report["dependency_rows"] == 3
    assert report["findings"] == []  # in particular, no DRB-008


def test_reference_folder_registers_are_not_scanned(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={"PKG-01_Core/0_References/DEL-01-01_Record_tier": [anchor_row()]},
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert report["registers_scanned"] == 0


def test_evidence_file_must_be_a_relative_regular_file(tmp_path: Path) -> None:
    """R-10b: a directory is not evidence, and an absolute path escapes the root."""
    absolute = str(tmp_path / "execution" / "_Decomposition" / "ScopeLedger.csv")
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                anchor_row("001", EvidenceFile="execution/_Decomposition"),  # a directory
                anchor_row("002", EvidenceFile=absolute),                    # absolute
                anchor_row("003"),                                           # good
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report) == {"EVQ-006": 2}
    details = " ".join(f["detail"] for f in report["findings"])
    assert "is a directory, not a file" in details
    assert "absolute path" in details
    assert report["row_class_metrics"]["ANCHOR"]["evidence_file_resolved"] == 1


def test_locus_quote_duplication_detail_is_direction_neutral(tmp_path: Path) -> None:
    """R-09: live hits run both ways; the message must not assert one direction."""
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                # A locus duplicated into the quote column (the reverse of the
                # 'quote pasted into the locus column' case).
                execution_row(SourceRef="PEC-RCN-002 feed list (DL-4)",
                              EvidenceQuote="PEC-RCN-002 feed list (DL-4)"),
            ]
        },
    )
    report = vdr.run(execution_root, families=("EVQ",))

    detail = report["findings"][0]["detail"]
    assert "byte-identical" in detail
    assert "one column is carrying the other's content" in detail
    # Must not name a single causal direction.
    assert "locus column is carrying quote text" not in detail


WAIVER_COLUMNS = list(vdr.WAIVER_COLUMNS)

GOOD_RATIONALE = (
    "Relation derived from register truth; the dag-gate exhibit records no "
    "prose statement of it, so there is no source text to quote."
)


def write_waivers(execution_root: Path, relative: str, rows: list[dict[str, str]],
                  columns: list[str] | None = None) -> None:
    write_csv(execution_root / relative / vdr.WAIVER_FILENAME,
              columns or WAIVER_COLUMNS, rows)


def waiver(dep_id: str = "DEP-01-01-003", check: str = "EVQ-003",
           rationale: str = GOOD_RATIONALE, **overrides: str) -> dict[str, str]:
    row = {
        "DependencyID": dep_id, "WaivedCheck": check, "Rationale": rationale,
        "DeclaredBy": "PEC PROJECT_SETUP", "DeclaredOn": "2026-07-25",
    }
    row.update(overrides)
    return row


def test_valid_waiver_downgrades_to_warning_and_permits_exit_zero(tmp_path: Path) -> None:
    """R-04: an honest-empty row must be declarable without inventing a quote."""
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row(SourceRef="location TBD", EvidenceQuote="")]},
    )
    write_waivers(execution_root, relative, [
        waiver(check="EVQ-003"),
        waiver(check="EVQ-004"),
    ])

    report = vdr.run(execution_root, families=("EVQ",))

    assert report["error_count"] == 0
    assert report["warning_count"] == 2
    assert codes(report) == {"EVQ-003": 1, "EVQ-004": 1}
    # The row is downgraded, never hidden.
    assert all(f["severity"] == "WARNING" for f in report["findings"])
    assert all("WAIVED:" in f["detail"] for f in report["findings"])
    assert report["row_class_metrics"]["EXECUTION"]["waived_rows"] == 1
    assert report["row_class_metrics"]["EXECUTION"]["empty_evidence_quote"] == 1

    result = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root), "--families", "EVQ"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "waived" in result.stdout
    # --strict still surfaces them.
    strict = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root), "--families", "EVQ", "--strict"],
        capture_output=True, text=True,
    )
    assert strict.returncode == 1


def test_thin_or_placeholder_rationale_is_rejected(tmp_path: Path) -> None:
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row(SourceRef="location TBD", EvidenceQuote="")]},
    )
    write_waivers(execution_root, relative, [
        waiver(check="EVQ-003", rationale="n/a"),
        waiver(check="EVQ-004", rationale="no source"),
    ])

    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report)["EVQ-008"] == 2
    # The underlying findings stay ERROR — a bad waiver softens nothing.
    assert codes(report)["EVQ-003"] == 1
    assert codes(report)["EVQ-004"] == 1
    assert report["error_count"] == 4
    assert report["row_class_metrics"]["EXECUTION"]["waived_rows"] == 0


def test_stale_waiver_is_an_error(tmp_path: Path) -> None:
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row()]},  # well-formed row
    )
    write_waivers(execution_root, relative, [waiver(check="EVQ-003")])

    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report) == {"EVQ-007": 1}
    assert report["error_count"] == 1


def test_malformed_waivers_are_rejected(tmp_path: Path) -> None:
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row(SourceRef="location TBD", EvidenceQuote="")]},
    )
    write_waivers(execution_root, relative, [
        waiver(dep_id="DEP-99-99-999"),                 # unknown DependencyID
        waiver(check="EVQ-001"),                        # unwaivable check
        waiver(check="EVQ-004", DeclaredBy=""),         # unattributed
    ])

    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report)["EVQ-009"] == 3
    assert codes(report)["EVQ-003"] == 1
    assert codes(report)["EVQ-004"] == 1
    assert report["row_class_metrics"]["EXECUTION"]["waived_rows"] == 0


def test_waiver_sidecar_missing_columns_is_rejected(tmp_path: Path) -> None:
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row(SourceRef="location TBD", EvidenceQuote="")]},
    )
    write_waivers(
        execution_root, relative,
        [{"DependencyID": "DEP-01-01-003", "WaivedCheck": "EVQ-003"}],
        columns=["DependencyID", "WaivedCheck"],
    )

    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report)["EVQ-009"] == 1
    assert any("missing required column" in f["detail"] for f in report["findings"])


def test_waiver_cannot_soften_locus_quote_duplication(tmp_path: Path) -> None:
    """EVQ-001 is never waivable: duplication is a defect, not a missing source."""
    relative = "PKG-01_Core/1_Working/DEL-01-01_Record_tier"
    execution_root = build_workspace(
        tmp_path,
        registers={relative: [execution_row(SourceRef="same text", EvidenceQuote="same text")]},
    )
    write_waivers(execution_root, relative, [waiver(check="EVQ-001")])

    report = vdr.run(execution_root, families=("EVQ",))

    assert codes(report)["EVQ-001"] == 1
    assert next(f for f in report["findings"] if f["code"] == "EVQ-001")["severity"] == "ERROR"
    assert codes(report)["EVQ-009"] == 1


def test_strict_promotes_warnings_to_a_failing_exit(tmp_path: Path) -> None:
    execution_root = build_workspace(
        tmp_path,
        registers={
            "PKG-01_Core/1_Working/DEL-01-01_Record_tier": [
                execution_row(SourceRef='§3 notes: "quoted span here"'),
            ],
            "PKG-02_Parsers/1_Working/DEL-02-01_Status_parser": [
                anchor_row("001", DependencyID="DEP-02-01-001", FromPackageID="PKG-02",
                           FromDeliverableID="DEL-02-01", FromDeliverableName="Status parser"),
            ],
        },
    )
    lenient = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root)], capture_output=True, text=True
    )
    assert lenient.returncode == 0
    assert "WARNING EVQ-002" in lenient.stdout

    strict = subprocess.run(
        [sys.executable, str(TOOL), str(execution_root), "--strict"],
        capture_output=True, text=True,
    )
    assert strict.returncode == 1
