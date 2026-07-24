#!/usr/bin/env python3
"""Validate a PKG-00 SCC Resolution Case folder."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_FILES = [
    "Case_Contract.md",
    "Case_Datasheet.md",
    "Task_Findings.csv",
    "Evidence_Register.csv",
    "Candidate_Remedies.csv",
    "Ruling_Register.csv",
    "Open_Questions.md",
    "Owner_Workflow_Handoff.md",
    "Case_QA.md",
]

TASK_FINDINGS_COLUMNS = [
    "FindingID",
    "SourceTaskRun",
    "AffectedDeliverables",
    "FindingType",
    "Summary",
    "EvidenceRefs",
    "Status",
]

EVIDENCE_COLUMNS = [
    "EvidenceID",
    "SourcePath",
    "SourceRef",
    "EvidenceType",
    "Supports",
    "Notes",
]

CANDIDATE_REMEDY_COLUMNS = [
    "RemedyID",
    "IssueOrEdge",
    "RemedyType",
    "OwnerWorkflow",
    "AffectedDeliverables",
    "EvidenceRefs",
    "HumanRuling",
    "Status",
    "TBDReason",
]

RULING_COLUMNS = [
    "RulingID",
    "QuestionID",
    "Ruling",
    "RulingBy",
    "Date",
    "EvidenceRefs",
    "Status",
]

HANDOFF_COLUMNS = [
    "HandoffID",
    "OwnerWorkflow",
    "TriggerCondition",
    "PayloadPath",
    "ExpectedOutput",
    "Status",
]

CASE_STATES = {
    "OPEN_FOR_TASK_WORK",
    "EVIDENCE_ACCUMULATING",
    "HUMAN_RULINGS_PENDING",
    "REMEDY_CLASSIFIED",
    "READY_FOR_OWNER_WORKFLOWS",
    "DEP_CLOSURE_PENDING",
    "CLOSED_BY_DEPCLOSURE",
    "BLOCKED_TBD",
}

OWNER_WORKFLOWS = {
    "WORKING_ITEMS",
    "TASK",
    "DEPENDENCY_WORKFLOW",
    "SCOPE_CHANGE",
    "RECONCILIATION",
    "DEPCLOSURE",
    "PROJECT_SETUP",
    # legacy value retained because immutable historical SCC artifacts carry it; new cases use PROJECT_SETUP (D-GOV-18)
    "ORCHESTRATOR",
    "CHANGE",
    "TBD",
}

FORBIDDEN_CLAIMS = [
    "SCC closure achieved",
    "strict graph is acyclic",
    "project-wide BLOCKED/UNBLOCKED is reportable",
    "dependency rows updated",
    "dependency rows changed",
    "Dependencies.csv updated",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def split_refs(value: str) -> list[str]:
    refs: list[str] = []
    for chunk in value.replace(",", ";").split(";"):
        token = chunk.strip()
        if token and token != "TBD":
            refs.append(token)
    return refs


def find_execution_root(case_path: Path) -> Path | None:
    for parent in [case_path, *case_path.parents]:
        if parent.name == "execution":
            return parent
    return None


def require_columns(
    errors: list[str], path: Path, expected: list[str]
) -> tuple[list[str], list[dict[str, str]]]:
    fields, rows = read_csv(path)
    missing = [col for col in expected if col not in fields]
    if missing:
        errors.append(f"{path.name} missing columns: {', '.join(missing)}")
    return fields, rows


def validate_case(case_path: Path) -> list[str]:
    errors: list[str] = []
    case_path = case_path.resolve()
    if not case_path.is_dir():
        return [f"case path is not a directory: {case_path}"]

    for filename in REQUIRED_FILES:
        if not (case_path / filename).is_file():
            errors.append(f"missing required file: {filename}")
    if errors:
        return errors

    _, findings = require_columns(errors, case_path / "Task_Findings.csv", TASK_FINDINGS_COLUMNS)
    _, evidence = require_columns(errors, case_path / "Evidence_Register.csv", EVIDENCE_COLUMNS)
    _, remedies = require_columns(errors, case_path / "Candidate_Remedies.csv", CANDIDATE_REMEDY_COLUMNS)
    _, rulings = require_columns(errors, case_path / "Ruling_Register.csv", RULING_COLUMNS)
    _, handoffs = require_columns(errors, case_path / "Owner_Workflow_Handoff.md", HANDOFF_COLUMNS)

    evidence_ids = {row.get("EvidenceID", "").strip() for row in evidence}
    evidence_ids.discard("")
    if not evidence_ids:
        errors.append("Evidence_Register.csv has no evidence rows")

    for idx, row in enumerate(findings, start=2):
        for ref in split_refs(row.get("EvidenceRefs", "")):
            if ref not in evidence_ids:
                errors.append(f"Task_Findings.csv row {idx} unknown EvidenceRef={ref}")

    for idx, row in enumerate(remedies, start=2):
        refs = split_refs(row.get("EvidenceRefs", ""))
        tbd_reason = row.get("TBDReason", "").strip()
        if not refs and not tbd_reason:
            errors.append(f"Candidate_Remedies.csv row {idx} needs EvidenceRefs or TBDReason")
        for ref in refs:
            if ref not in evidence_ids:
                errors.append(f"Candidate_Remedies.csv row {idx} unknown EvidenceRef={ref}")
        owner = row.get("OwnerWorkflow", "").strip()
        if owner not in OWNER_WORKFLOWS:
            errors.append(f"Candidate_Remedies.csv row {idx} invalid OwnerWorkflow={owner!r}")

    for idx, row in enumerate(rulings, start=2):
        for ref in split_refs(row.get("EvidenceRefs", "")):
            if ref not in evidence_ids:
                errors.append(f"Ruling_Register.csv row {idx} unknown EvidenceRef={ref}")

    for idx, row in enumerate(handoffs, start=2):
        owner = row.get("OwnerWorkflow", "").strip()
        if owner not in OWNER_WORKFLOWS:
            errors.append(f"Owner_Workflow_Handoff.md row {idx} invalid OwnerWorkflow={owner!r}")

    datasheet = read_text(case_path / "Case_Datasheet.md")
    qa = read_text(case_path / "Case_QA.md")
    states_seen = [state for state in CASE_STATES if state in datasheet or state in qa]
    if not states_seen:
        errors.append("case state not found in Case_Datasheet.md or Case_QA.md")
    if "CLOSED_BY_DEPCLOSURE" in states_seen and "DepClosure" not in qa:
        errors.append("CLOSED_BY_DEPCLOSURE requires cited DepClosure evidence in Case_QA.md")

    combined_text = "\n".join(read_text(case_path / filename) for filename in REQUIRED_FILES if filename.endswith(".md"))
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in combined_text:
            errors.append(f"forbidden positive closure/mutation claim found: {phrase}")
    if (case_path / "case-seeds").exists():
        seed_text = combined_text.lower()
        if "seed evidence" not in seed_text:
            errors.append("case-seeds present but case text does not label seeds as evidence")

    execution_root = find_execution_root(case_path)
    if execution_root:
        pkg00 = execution_root / "PKG-00_DAG_Closure_and_Project_Control"
        if pkg00.exists() and any(pkg00.rglob("Dependencies.csv")):
            errors.append("PKG-00 contains Dependencies.csv; SCC cases must not add dependency registers")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_path", help="Path to an SCC resolution case folder")
    args = parser.parse_args()

    errors = validate_case(Path(args.case_path))
    if errors:
        print("FAIL: SCC resolution case validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: SCC resolution case validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
