#!/usr/bin/env python3
"""Validate a PKG-00 Scope Change Consumable Packet."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_FILES = [
    "Packet_Contract.md",
    "Packet_Datasheet.md",
    "Packet_Specification.md",
    "Packet_Procedure.md",
    "Packet_Rationale.md",
    "SCOPE_CHANGE_INIT.md",
    "Proposed_SCA_Actions.csv",
    "Affected_Surfaces.csv",
    "Evidence_Index.csv",
    "Packet_QA.md",
]

ACTION_COLUMNS = [
    "PacketID",
    "ActionSeq",
    "ActionType",
    "EntityType",
    "EntityID",
    "Description",
    "AffectedDeliverables",
    "AffectedFiles",
    "EvidenceRefs",
    "SCOPE_CHANGE_Gate",
    "Status",
]

SURFACE_COLUMNS = [
    "PacketID",
    "SurfaceType",
    "SurfacePath",
    "PackageRole",
    "ChangeClass",
    "OwnerWorkflow",
    "RequiredAction",
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

VALID_ACTION_TYPES = {"ADD", "REMOVE", "MODIFY", "RECLASSIFY", "MERGE", "SPLIT", "TBD"}

FORBIDDEN_CLAIMS = [
    "SCC closure achieved",
    "strict graph is acyclic",
    "project-wide BLOCKED/UNBLOCKED is reportable",
    "SCOPE_CHANGE initiated",
    "dependency rows updated",
    "dependency rows changed",
    "Dependencies.csv updated",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def split_ids(value: str) -> list[str]:
    out: list[str] = []
    for chunk in value.replace(",", ";").split(";"):
        token = chunk.strip()
        if token and token != "TBD":
            out.append(token)
    return out


def find_execution_root(packet_path: Path) -> Path | None:
    for parent in [packet_path, *packet_path.parents]:
        if parent.name == "execution":
            return parent
    return None


def load_decomposition_text(execution_root: Path | None, explicit: str | None) -> str:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if execution_root:
        decomp_root = execution_root / "_Decomposition"
        candidates.extend(sorted(decomp_root.glob("*.md")))
    texts: list[str] = []
    for candidate in candidates:
        if candidate.exists():
            texts.append(candidate.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(texts)


def validate_packet(packet_path: Path, decomposition_path: str | None = None) -> list[str]:
    errors: list[str] = []
    packet_path = packet_path.resolve()

    if not packet_path.is_dir():
        return [f"packet path is not a directory: {packet_path}"]

    for filename in REQUIRED_FILES:
        if not (packet_path / filename).is_file():
            errors.append(f"missing required file: {filename}")

    if errors:
        return errors

    action_fields, actions = read_csv(packet_path / "Proposed_SCA_Actions.csv")
    surface_fields, surfaces = read_csv(packet_path / "Affected_Surfaces.csv")
    evidence_fields, evidence = read_csv(packet_path / "Evidence_Index.csv")

    for expected, actual, name in [
        (ACTION_COLUMNS, action_fields, "Proposed_SCA_Actions.csv"),
        (SURFACE_COLUMNS, surface_fields, "Affected_Surfaces.csv"),
        (EVIDENCE_COLUMNS, evidence_fields, "Evidence_Index.csv"),
    ]:
        missing = [col for col in expected if col not in actual]
        if missing:
            errors.append(f"{name} missing columns: {', '.join(missing)}")

    evidence_ids = {row.get("EvidenceID", "").strip() for row in evidence}
    evidence_ids.discard("")
    if not evidence_ids:
        errors.append("Evidence_Index.csv has no evidence rows")

    affected_ids: set[str] = set()
    for idx, row in enumerate(actions, start=2):
        action_type = row.get("ActionType", "").strip()
        if action_type not in VALID_ACTION_TYPES:
            errors.append(f"Proposed_SCA_Actions.csv row {idx} invalid ActionType={action_type!r}")
        refs = split_ids(row.get("EvidenceRefs", ""))
        if not refs:
            errors.append(f"Proposed_SCA_Actions.csv row {idx} missing EvidenceRefs")
        for ref in refs:
            if ref not in evidence_ids:
                errors.append(f"Proposed_SCA_Actions.csv row {idx} unknown EvidenceRef={ref}")
        affected_ids.update(split_ids(row.get("AffectedDeliverables", "")))

    for idx, row in enumerate(surfaces, start=2):
        for ref in split_ids(row.get("EvidenceRefs", "")):
            if ref not in evidence_ids:
                errors.append(f"Affected_Surfaces.csv row {idx} unknown EvidenceRef={ref}")

    execution_root = find_execution_root(packet_path)
    decomp_text = load_decomposition_text(execution_root, decomposition_path)
    if decomp_text:
        for deliverable_id in sorted(affected_ids):
            if deliverable_id.startswith("DEL-") and deliverable_id not in decomp_text:
                errors.append(f"affected deliverable not found in decomposition: {deliverable_id}")
    elif affected_ids:
        errors.append("could not locate decomposition text to validate affected deliverables")

    combined_text = "\n".join(
        (packet_path / filename).read_text(encoding="utf-8", errors="replace")
        for filename in REQUIRED_FILES
        if filename.endswith(".md")
    )
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in combined_text:
            errors.append(f"forbidden positive closure/mutation claim found: {phrase}")

    init_text = (packet_path / "SCOPE_CHANGE_INIT.md").read_text(encoding="utf-8", errors="replace")
    if "human" not in init_text.lower() or "initiat" not in init_text.lower():
        errors.append("SCOPE_CHANGE_INIT.md must state that human initiation is required")

    if execution_root:
        pkg00 = execution_root / "PKG-00_DAG_Closure_and_Project_Control"
        if pkg00.exists() and any(pkg00.rglob("Dependencies.csv")):
            errors.append("PKG-00 contains Dependencies.csv; control packets must not add dependency registers")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet_path", help="Path to a scope-change packet folder")
    parser.add_argument("--decomposition-path", help="Optional explicit decomposition markdown path")
    args = parser.parse_args()

    errors = validate_packet(Path(args.packet_path), args.decomposition_path)
    if errors:
        print("FAIL: scope-change packet validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: scope-change packet validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
