#!/usr/bin/env python3
"""
validate_domain_decomposition_integrity.py

Deterministically validates a DOMAIN decomposition package's machine-checkable
integrity constraints.

Usage:
  python3 tools/validation/validate_domain_decomposition_integrity.py \\
    --decomposition-root <domain-root>/_Decomposition \\
    --output-report <snapshot>/Domain_Integrity_Report.md \\
    --output-findings <snapshot>/Domain_Integrity_Findings.csv \\
    [--scope-change-snapshot <snapshot>] \\
    [--package-subfolder <name>]

Inputs:
  --decomposition-root: directory containing DOMAIN annex CSVs.
  --scope-change-snapshot: optional SCA snapshot used to validate active
    snapshot artifact completeness, _LATEST parity, and KTY manifest rollup.
  --package-subfolder: optional name of a single direct subfolder under
    --decomposition-root from which to resolve annex CSVs (transitional
    dual-layout support). When omitted and the root has no annex matches
    directly, the resolver auto-descends into a single eligible subfolder
    (excluding hidden dirs, `_Archive`, and `__pycache__`). Ambiguous
    layouts (multiple eligible subfolders) require the explicit flag.

Outputs:
  Markdown report and findings CSV. The tool is idempotent and writes only the
  declared output files.

Scope boundary:
  Reads only supplied decomposition annexes, optional _ScopeChange pointer /
  snapshot artifacts, and optional KTY_Remediation_Manifest.csv. It does not
  modify decomposition truth, SCA snapshots, KTY folders, or downstream outputs.

Exit codes:
  0 = valid, no blocking findings
  1 = fatal input / parsing error
  2 = validation completed with blocking findings
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


BLOCKING_SEVERITIES = {"CRITICAL", "MAJOR"}

REQUIRED_FILES = {
    "ledger": "annex_domain_ledger.csv",
    "categories": "annex_categories.csv",
    "ktys": "annex_knowledge_types.csv",
    "subjects": "annex_knowledge_subjects.csv",
    "objectives": "annex_objectives.csv",
    "coverage": "annex_coverage_telemetry.csv",
}

FILE_CANDIDATES = {
    "ledger": ["annex_domain_ledger.csv", "*Domain_Ledger*.csv"],
    "categories": ["annex_categories.csv", "*Category_Register*.csv"],
    "ktys": ["annex_knowledge_types.csv", "*Knowledge_Type_Register*.csv"],
    "subjects": ["annex_knowledge_subjects.csv", "*Knowledge_Subject_Register*.csv"],
    "objectives": ["annex_objectives.csv", "*Objective_Register*.csv"],
    "coverage": ["annex_coverage_telemetry.csv", "*Coverage_Telemetry*.csv", "*Coverage_Telemetry*.json"],
}

REQUIRED_SNAPSHOT_ARTIFACTS = [
    "Brief.md",
    "Impact_Assessment.md",
    "Propagation_Plan.md",
    "Amendment_Actions.csv",
    "Pre_Change_Coverage.json",
    "Post_Change_Coverage.json",
    "Decision_Log.md",
    "Handoff_State.md",
    "RUN_SUMMARY.md",
    "Supersession_Map.csv",
]


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    evidence_file: str
    source_ref: str
    message: str


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(str(path))
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        header = [h.strip() for h in reader.fieldnames]
        rows = []
        for row in reader:
            cleaned: dict[str, str] = {}
            for k, v in row.items():
                if k is None:
                    continue
                cleaned[k.strip()] = "" if v is None else str(v).strip()
            rows.append(cleaned)
    return header, rows


SUBFOLDER_DESCENT_EXCLUDES = {"_Archive", "__pycache__"}


def _resolve_in_dir(directory: Path) -> dict[str, Path]:
    """Resolve FILE_CANDIDATES against a single directory (depth 0).

    Returns a partial map of {logical-name: path} containing only the candidates
    that were actually found. Callers compare result size to FILE_CANDIDATES to
    determine whether descent is needed.
    """
    found: dict[str, Path] = {}
    for name, patterns in FILE_CANDIDATES.items():
        for pattern in patterns:
            exact = directory / pattern
            if exact.exists():
                found[name] = exact
                break
            matches = sorted(directory.glob(pattern))
            if matches:
                found[name] = matches[0]
                break
    return found


def _candidate_subfolders(decomposition_root: Path) -> list[Path]:
    """Return direct subfolders eligible for transitional auto-descent.

    Excludes hidden directories (leading `.`), `_Archive`, and `__pycache__`.
    Order is sorted by name for determinism.
    """
    subs: list[Path] = []
    for child in sorted(decomposition_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name in SUBFOLDER_DESCENT_EXCLUDES:
            continue
        subs.append(child)
    return subs


def resolve_required_paths(
    decomposition_root: Path,
    package_subfolder: str | None = None,
) -> dict[str, Path]:
    """Resolve annex paths under ``decomposition_root``.

    Resolution order:
      1. If ``package_subfolder`` is provided, resolve from
         ``decomposition_root/package_subfolder`` (explicit overrides
         implicit). A nonexistent named subfolder yields fall-through paths
         that surface as MISSING_REQUIRED_FILE findings via the existing
         contract.
      2. Otherwise, resolve directly under ``decomposition_root``.
      3. If no annex matches at root, perform depth-1 auto-descent: if
         exactly one eligible subfolder (excluding hidden, ``_Archive``,
         ``__pycache__``) contains at least one annex match, resolve from
         there. Multiple eligible subfolders that each contain matches are
         treated as ambiguous; resolution falls through and the missing
         files surface as findings.

    Auto-descent is depth-1 only — no further recursion is performed.
    """
    paths: dict[str, Path] = {}

    # Explicit package subfolder takes precedence.
    if package_subfolder:
        explicit_dir = decomposition_root / package_subfolder
        if explicit_dir.is_dir():
            paths.update(_resolve_in_dir(explicit_dir))
        # If the explicit subfolder is missing or empty of candidates, fall
        # through; missing files surface via validate_required_files.
    else:
        # Try root first.
        paths.update(_resolve_in_dir(decomposition_root))

        # If nothing was found at root, attempt depth-1 auto-descent.
        if not paths:
            candidates = _candidate_subfolders(decomposition_root)
            eligible: list[tuple[Path, dict[str, Path]]] = []
            for sub in candidates:
                sub_resolved = _resolve_in_dir(sub)
                if sub_resolved:
                    eligible.append((sub, sub_resolved))
            if len(eligible) == 1:
                paths.update(eligible[0][1])
            # If 0 eligible -> fall through; if >1 eligible -> ambiguous,
            # also fall through (caller must use --package-subfolder).

    # Fill any unresolved logical names with the canonical root-level path so
    # validate_required_files can report MISSING_REQUIRED_FILE against a
    # stable, expected location.
    for name in FILE_CANDIDATES:
        if name not in paths:
            paths[name] = decomposition_root / REQUIRED_FILES[name]
    return paths


def first_value(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key, "").strip()
        if value:
            return value
    return ""


def lifecycle_status(row: dict[str, str]) -> str:
    return first_value(row, "UnitStatus", "InOutStatus", "LifecycleState", "CurrentState", "Current State").upper()


def split_ids(raw: str) -> list[str]:
    if not raw.strip() or raw.strip().upper() == "TBD":
        return []
    normalized = raw.replace(",", ";")
    return [token.strip() for token in normalized.split(";") if token.strip() and token.strip().upper() != "TBD"]


def is_retired_row(row: dict[str, str]) -> bool:
    status = lifecycle_status(row)
    if status in {"RETIRED", "RETIRED_NO_FACTUAL_USE"}:
        return True
    return any("[RETIRED" in value.upper() or value.upper().startswith("RETIRED") for value in row.values())


def is_active_subject_row(row: dict[str, str]) -> bool:
    return lifecycle_status(row) not in {"OUT", "RETIRED", "RETIRED_NO_FACTUAL_USE"} and not is_retired_row(row)


def is_nonretired_subject_row(row: dict[str, str]) -> bool:
    return lifecycle_status(row) not in {"RETIRED", "RETIRED_NO_FACTUAL_USE"} and not is_retired_row(row)


def row_ref(row_num: int, key: str = "") -> str:
    return f"row {row_num}" + (f" ({key})" if key else "")


def load_required(
    decomposition_root: Path,
    package_subfolder: str | None = None,
) -> tuple[dict[str, Path], dict[str, list[dict[str, str]]]]:
    paths = resolve_required_paths(decomposition_root, package_subfolder=package_subfolder)
    rows: dict[str, list[dict[str, str]]] = {}
    for name, path in paths.items():
        if path.suffix.lower() == ".json":
            continue
        _, rows[name] = read_csv_rows(path)
    return paths, rows


def coverage_metrics(path: Path) -> dict[str, object]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    _, rows = read_csv_rows(path)
    return {row.get("Metric", "").strip(): row.get("Value", "").strip() for row in rows if row.get("Metric", "").strip()}


def metric_int(metrics: dict[str, object], key: str) -> int | None:
    raw = str(metrics.get(key, "")).strip()
    try:
        return int(raw)
    except ValueError:
        return None


def validate_required_files(paths: dict[str, Path]) -> list[Finding]:
    findings: list[Finding] = []
    for name, path in paths.items():
        if not path.exists():
            findings.append(Finding("CRITICAL", "MISSING_REQUIRED_FILE", str(path), "file", f"Missing DOMAIN decomposition annex: {name}"))
    return findings


def validate_domain_rows(paths: dict[str, Path], rows: dict[str, list[dict[str, str]]]) -> list[Finding]:
    findings: list[Finding] = []
    ledger = rows["ledger"]
    categories = rows["categories"]
    ktys = rows["ktys"]
    subjects = rows["subjects"]
    objectives = rows["objectives"]

    category_ids = {row.get("CategoryID", "") for row in categories if row.get("CategoryID", "")}
    objective_ids = {row.get("ObjectiveID", "") for row in objectives if row.get("ObjectiveID", "")}
    kty_rows_by_id: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    for idx, row in enumerate(ktys, start=2):
        kty_rows_by_id[row.get("KnowledgeTypeID", "")].append((idx, row))
    kty_ids = {k for k in kty_rows_by_id if k}
    retired_ktys = {k for k, grouped in kty_rows_by_id.items() if any(is_retired_row(row) for _, row in grouped)}
    inactive_subject_rule_ktys = {
        k
        for k, grouped in kty_rows_by_id.items()
        if any(lifecycle_status(row) in {"OUT", "RETIRED", "RETIRED_NO_FACTUAL_USE"} or is_retired_row(row) for _, row in grouped)
    }

    subjects_by_id: dict[str, tuple[int, dict[str, str]]] = {}
    subjects_by_kty: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    for idx, row in enumerate(subjects, start=2):
        subject_id = row.get("SubjectID", "")
        if subject_id:
            subjects_by_id[subject_id] = (idx, row)
        subjects_by_kty[row.get("ParentKnowledgeTypeID", "")].append((idx, row))

    for kty_id, grouped in kty_rows_by_id.items():
        if not kty_id:
            findings.append(Finding("CRITICAL", "MISSING_KTY_ID", str(paths["ktys"]), "row unknown", "KnowledgeTypeID is blank"))
            continue
        if len(grouped) > 1:
            findings.append(Finding("CRITICAL", "DUPLICATE_KTY_ID", str(paths["ktys"]), kty_id, "KnowledgeTypeID appears more than once"))
        for idx, row in grouped:
            cat = row.get("ParentCategoryID", "")
            if not cat:
                findings.append(Finding("CRITICAL", "KTY_WITHOUT_CATEGORY", str(paths["ktys"]), row_ref(idx, kty_id), "Knowledge Type has no ParentCategoryID"))
            elif cat not in category_ids:
                findings.append(Finding("CRITICAL", "KTY_CATEGORY_MISSING", str(paths["ktys"]), row_ref(idx, kty_id), f"ParentCategoryID {cat} does not exist in categories"))
        active_subjects = [row for _, row in subjects_by_kty.get(kty_id, []) if is_nonretired_subject_row(row)]
        if kty_id not in inactive_subject_rule_ktys and not active_subjects:
            findings.append(Finding("CRITICAL", "ACTIVE_KTY_WITHOUT_ACTIVE_SUBJECT", str(paths["subjects"]), kty_id, "Active Knowledge Type has no active Knowledge Subject"))

    for idx, row in enumerate(subjects, start=2):
        subject_id = row.get("SubjectID", "")
        parent = row.get("ParentKnowledgeTypeID", "")
        if not subject_id:
            findings.append(Finding("CRITICAL", "MISSING_SUBJECT_ID", str(paths["subjects"]), row_ref(idx), "SubjectID is blank"))
        if not parent or parent not in kty_ids:
            findings.append(Finding("CRITICAL", "SUBJECT_PARENT_MISSING", str(paths["subjects"]), row_ref(idx, subject_id), f"ParentKnowledgeTypeID {parent!r} does not exist"))
            continue
        parent_cat = kty_rows_by_id[parent][0][1].get("ParentCategoryID", "")
        if row.get("CategoryID", "") and row.get("CategoryID") != parent_cat:
            findings.append(Finding("MAJOR", "SUBJECT_CATEGORY_MISMATCH", str(paths["subjects"]), row_ref(idx, subject_id), f"Subject CategoryID {row.get('CategoryID')} differs from parent KTY category {parent_cat}"))

    for idx, row in enumerate(ledger, start=2):
        unit = row.get("UnitID", "")
        status = lifecycle_status(row)
        if status == "IN":
            if not row.get("CategoryID", ""):
                findings.append(Finding("CRITICAL", "IN_UNIT_WITHOUT_CATEGORY", str(paths["ledger"]), row_ref(idx, unit), "IN unit has no CategoryID"))
            elif row.get("CategoryID") not in category_ids:
                findings.append(Finding("CRITICAL", "IN_UNIT_CATEGORY_MISSING", str(paths["ledger"]), row_ref(idx, unit), f"CategoryID {row.get('CategoryID')} does not exist"))
            kty_refs = split_ids(first_value(row, "KnowledgeTypeID(s)", "KnowledgeTypeID", "KnowledgeTypeIDs"))
            subject_refs = split_ids(first_value(row, "SubjectID(s)", "SubjectID", "SubjectIDs"))
            if not kty_refs:
                findings.append(Finding("CRITICAL", "IN_UNIT_WITHOUT_KTY", str(paths["ledger"]), row_ref(idx, unit), "IN unit has no KnowledgeTypeID(s)"))
            if not subject_refs:
                findings.append(Finding("CRITICAL", "IN_UNIT_WITHOUT_SUBJECT", str(paths["ledger"]), row_ref(idx, unit), "IN unit has no SubjectID(s)"))
            for ref in kty_refs:
                if ref not in kty_ids:
                    findings.append(Finding("CRITICAL", "LEDGER_KTY_REF_MISSING", str(paths["ledger"]), row_ref(idx, unit), f"KnowledgeTypeID reference does not exist: {ref}"))
            for ref in subject_refs:
                if ref not in subjects_by_id:
                    findings.append(Finding("CRITICAL", "LEDGER_SUBJECT_REF_MISSING", str(paths["ledger"]), row_ref(idx, unit), f"SubjectID reference does not exist: {ref}"))
        for obj in split_ids(first_value(row, "ObjectiveID(s)", "ObjectiveIDs", "ObjectiveID")):
            if obj not in objective_ids:
                findings.append(Finding("MAJOR", "LEDGER_OBJECTIVE_REF_MISSING", str(paths["ledger"]), row_ref(idx, unit), f"ObjectiveID reference does not exist: {obj}"))

    for idx, row in enumerate(objectives, start=2):
        objective_id = row.get("ObjectiveID", "")
        mapped_ktys = split_ids(row.get("MappedKnowledgeTypes", ""))
        if mapped_ktys and all(kty in retired_ktys for kty in mapped_ktys):
            findings.append(Finding("CRITICAL", "OBJECTIVE_ONLY_RETIRED_KTYS", str(paths["objectives"]), row_ref(idx, objective_id), "Objective is supported only by retired Knowledge Types"))
        for kty in mapped_ktys:
            if kty not in kty_ids:
                findings.append(Finding("MAJOR", "OBJECTIVE_KTY_REF_MISSING", str(paths["objectives"]), row_ref(idx, objective_id), f"MappedKnowledgeTypes reference does not exist: {kty}"))

    # OBJECTIVE_KTY_PARITY_MISMATCH: verify Objective_Register.MappedKnowledgeTypes matches
    # the inversion of Knowledge_Type_Register.SupportsObjectives.
    kty_inversion: dict[str, set[str]] = defaultdict(set)
    for row in ktys:
        kty_id = row.get("KnowledgeTypeID", "").strip()
        if not kty_id:
            continue
        for obj_id in split_ids(row.get("SupportsObjectives", "")):
            kty_inversion[obj_id].add(kty_id)

    for idx, row in enumerate(objectives, start=2):
        objective_id = row.get("ObjectiveID", "")
        if not objective_id:
            continue
        set_a = set(split_ids(row.get("MappedKnowledgeTypes", "")))
        set_b = kty_inversion.get(objective_id, set())
        diff = set_a.symmetric_difference(set_b)
        if diff:
            findings.append(Finding(
                "MAJOR",
                "OBJECTIVE_KTY_PARITY_MISMATCH",
                str(paths["objectives"]),
                row_ref(idx, objective_id),
                f"MappedKnowledgeTypes does not match KT-register inversion: symmetric difference = {sorted(diff)}",
            ))

    return findings


def parse_knowledge_type_metric(raw: object) -> tuple[int | None, int | None]:
    text = str(raw)
    numbers = [int(match) for match in re.findall(r"\d+", text)]
    if not numbers:
        return None, None
    if "active" in text.lower():
        active = numbers[0]
        total = numbers[-1] if "total" in text.lower() and len(numbers) >= 2 else None
        return active, total
    return numbers[0], None


def validate_coverage(paths: dict[str, Path], rows: dict[str, list[dict[str, str]]]) -> list[Finding]:
    metrics = coverage_metrics(paths["coverage"])
    findings: list[Finding] = []
    ledger = rows["ledger"]
    categories = rows["categories"]
    ktys = rows["ktys"]
    subjects = rows["subjects"]
    objectives = rows["objectives"]

    expected = {
        "UnitCount": sum(1 for row in ledger if lifecycle_status(row) != "RETIRED"),
        "INUnitCount": sum(1 for row in ledger if lifecycle_status(row) == "IN"),
        "TBDUnitCount": sum(1 for row in ledger if lifecycle_status(row) == "TBD"),
        "OUTUnitCount": sum(1 for row in ledger if lifecycle_status(row) == "OUT"),
        "CategoryCount": len(categories),
        "ObjectiveCount": len(objectives),
        "UnassignedINUnits": sum(1 for row in ledger if lifecycle_status(row) == "IN" and not row.get("CategoryID", "")),
        "UnitsWithoutKnowledgeTypeMapping": sum(1 for row in ledger if lifecycle_status(row) == "IN" and not split_ids(first_value(row, "KnowledgeTypeID(s)", "KnowledgeTypeID", "KnowledgeTypeIDs"))),
    }
    mapped_objectives = set()
    for row in ledger:
        mapped_objectives.update(split_ids(first_value(row, "ObjectiveID(s)", "ObjectiveIDs", "ObjectiveID")))
    objective_ids = {row.get("ObjectiveID", "") for row in objectives if row.get("ObjectiveID", "")}
    expected["UnmappedObjectives"] = len(objective_ids - mapped_objectives)

    for key, expected_value in expected.items():
        observed = metric_int(metrics, key)
        if observed is not None and observed != expected_value:
            findings.append(Finding("MAJOR", "COVERAGE_METRIC_MISMATCH", str(paths["coverage"]), key, f"{key}={observed} but computed {expected_value}"))

    observed_subjects = metric_int(metrics, "SubjectCount")
    active_subject_count = sum(1 for row in subjects if is_active_subject_row(row))
    nonretired_subject_count = sum(1 for row in subjects if is_nonretired_subject_row(row))
    if observed_subjects is not None and observed_subjects not in {active_subject_count, nonretired_subject_count}:
        findings.append(Finding(
            "MAJOR",
            "COVERAGE_METRIC_MISMATCH",
            str(paths["coverage"]),
            "SubjectCount",
            f"SubjectCount={observed_subjects} but computed active={active_subject_count} or non-retired={nonretired_subject_count}",
        ))

    retired_ktys = sum(1 for row in ktys if is_retired_row(row))
    active_ktys = len(ktys) - retired_ktys
    observed_active, observed_total = parse_knowledge_type_metric(metrics.get("KnowledgeTypeCount", ""))
    if observed_active is not None and observed_active != active_ktys:
        findings.append(Finding("MAJOR", "COVERAGE_METRIC_MISMATCH", str(paths["coverage"]), "KnowledgeTypeCount", f"active KTY count {observed_active} but computed {active_ktys}"))
    if observed_total is not None and observed_total != len(ktys):
        findings.append(Finding("MAJOR", "COVERAGE_METRIC_MISMATCH", str(paths["coverage"]), "KnowledgeTypeCount", f"total KTY count {observed_total} but computed {len(ktys)}"))

    return findings


def manifest_rollup(rows: list[dict[str, str]]) -> str:
    states = {row.get("CONTENT_DISPOSITION_STATE", "").strip() for row in rows}
    gates = {row.get("FACTUAL_USE_GATE", "").strip() for row in rows}
    if any(not state or state == "PENDING" for state in states):
        return "PENDING"
    if "BLOCKED" in states or "BLOCK_FACTUAL_USE" in gates:
        return "BLOCKED"
    if "DEFERRED" in states:
        return "DEFERRED"
    return "COMPLETE"


def validate_snapshot(snapshot: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not snapshot.exists() or not snapshot.is_dir():
        return [Finding("CRITICAL", "SNAPSHOT_MISSING", str(snapshot), "snapshot", "Scope-change snapshot does not exist")]
    for name in REQUIRED_SNAPSHOT_ARTIFACTS:
        path = snapshot / name
        if not path.exists():
            findings.append(Finding("MAJOR", "SNAPSHOT_ARTIFACT_MISSING", str(path), name, "Required snapshot artifact is missing"))

    actions = snapshot / "Amendment_Actions.csv"
    if actions.exists():
        _, action_rows = read_csv_rows(actions)
        needs_supersession_delta = any(row.get("SupersessionBindingPresent", "").strip().upper() in {"YES", "TRUE", "1"} for row in action_rows)
        delta = snapshot / "Supersession_Delta.csv"
        if needs_supersession_delta and not delta.exists():
            findings.append(Finding("CRITICAL", "SUPERSESSION_DELTA_MISSING", str(delta), "SupersessionBindingPresent", "Supersession_Delta.csv is required because one or more actions declare SupersessionBindingPresent=YES"))

    latest = snapshot.parent / "_LATEST.md"
    if latest.exists():
        text = latest.read_text(encoding="utf-8", errors="replace")
        if snapshot.name not in text and str(snapshot) not in text:
            findings.append(Finding("MAJOR", "LATEST_POINTER_MISMATCH", str(latest), "_LATEST.md", f"_LATEST.md does not point to active snapshot {snapshot.name}"))
    else:
        findings.append(Finding("MAJOR", "LATEST_POINTER_MISSING", str(latest), "_LATEST.md", "_LATEST.md is missing"))

    manifest = snapshot / "KTY_Remediation_Manifest.csv"
    if manifest.exists():
        _, rows = read_csv_rows(manifest)
        rollup = manifest_rollup(rows) if rows else "NOT_REQUIRED"
        pending = sum(1 for row in rows if row.get("CONTENT_DISPOSITION_STATE", "").strip() == "PENDING")
        if pending:
            findings.append(Finding("CRITICAL", "KTY_REMEDIATION_PENDING", str(manifest), "CONTENT_DISPOSITION_STATE", f"{pending} manifest rows are PENDING"))
        for path_name in ("RUN_SUMMARY.md", "Handoff_State.md"):
            path = snapshot / path_name
            if path.exists():
                text = path.read_text(encoding="utf-8", errors="replace")
                if "ContentRemediationState" in text and rollup not in text:
                    findings.append(Finding("MAJOR", "CONTENT_REMEDIATION_ROLLUP_MISMATCH", str(path), "ContentRemediationState", f"Manifest rollup is {rollup}, but {path_name} does not show that state"))
    return findings


def write_findings_csv(path: Path, findings: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Severity", "Category", "EvidenceFile", "SourceRef", "Message"])
        writer.writeheader()
        for finding in findings:
            writer.writerow({
                "Severity": finding.severity,
                "Category": finding.category,
                "EvidenceFile": finding.evidence_file,
                "SourceRef": finding.source_ref,
                "Message": finding.message,
            })


def write_report(path: Path, findings: list[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter(f.severity for f in findings)
    status = "PASS" if not any(f.severity in BLOCKING_SEVERITIES for f in findings) else "BLOCKED"
    lines = [
        "# DOMAIN Decomposition Integrity Report",
        "",
        f"**Status:** {status}",
        "",
        "## Findings Summary",
        "",
        f"- CRITICAL: {counts.get('CRITICAL', 0)}",
        f"- MAJOR: {counts.get('MAJOR', 0)}",
        f"- MINOR: {counts.get('MINOR', 0)}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings.")
    else:
        lines.append("| Severity | Category | Evidence | SourceRef | Message |")
        lines.append("|---|---|---|---|---|")
        for finding in findings:
            lines.append(f"| {finding.severity} | {finding.category} | `{finding.evidence_file}` | {finding.source_ref} | {finding.message} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate DOMAIN decomposition package integrity")
    parser.add_argument("--decomposition-root", required=True, type=Path, help="Path to DOMAIN _Decomposition directory")
    parser.add_argument("--scope-change-snapshot", type=Path, help="Optional active SCA snapshot path")
    parser.add_argument("--output-report", required=True, type=Path, help="Markdown report output")
    parser.add_argument("--output-findings", required=True, type=Path, help="Findings CSV output")
    parser.add_argument(
        "--package-subfolder",
        type=str,
        default=None,
        help=(
            "Optional name of a single direct subfolder under --decomposition-root "
            "from which to resolve annex CSVs (transitional dual-layout support). "
            "When omitted, the resolver auto-descends into a single eligible "
            "subfolder if the root does not contain annexes."
        ),
    )
    return parser.parse_args()


def _log_resolution_source(decomposition_root: Path, package_subfolder: str | None) -> None:
    """Emit a stderr INFO line when resolution did not come from the root."""
    if package_subfolder:
        # Verify the explicit subfolder exists; if not, raise so main()'s
        # error handler returns exit 1 with a clear message.
        explicit_dir = decomposition_root / package_subfolder
        if not explicit_dir.is_dir():
            raise NotADirectoryError(
                f"--package-subfolder does not exist: {explicit_dir}"
            )
        print(
            f"[INFO] Resolved annexes from package subfolder: {package_subfolder}",
            file=sys.stderr,
        )
        return

    # Auto-descent path: detect whether resolution will descend.
    if _resolve_in_dir(decomposition_root):
        return  # root has annexes — no descent
    candidates = _candidate_subfolders(decomposition_root)
    eligible = [sub for sub in candidates if _resolve_in_dir(sub)]
    if len(eligible) == 1:
        print(
            f"[INFO] Resolved annexes from package subfolder: {eligible[0].name}",
            file=sys.stderr,
        )


def main() -> int:
    args = parse_args()
    try:
        if not args.decomposition_root.is_dir():
            raise NotADirectoryError(str(args.decomposition_root))
        _log_resolution_source(args.decomposition_root, args.package_subfolder)
        paths = resolve_required_paths(
            args.decomposition_root,
            package_subfolder=args.package_subfolder,
        )
        findings = validate_required_files(paths)
        if not findings:
            paths, rows = load_required(
                args.decomposition_root,
                package_subfolder=args.package_subfolder,
            )
            findings.extend(validate_domain_rows(paths, rows))
            findings.extend(validate_coverage(paths, rows))
        if args.scope_change_snapshot:
            findings.extend(validate_snapshot(args.scope_change_snapshot))
        write_findings_csv(args.output_findings, findings)
        write_report(args.output_report, findings)
    except (FileNotFoundError, NotADirectoryError, ValueError, OSError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    blocking = [finding for finding in findings if finding.severity in BLOCKING_SEVERITIES]
    print(f"Checked DOMAIN decomposition: {args.decomposition_root}")
    print(f"Findings: {len(findings)} total, {len(blocking)} blocking")
    for finding in findings:
        print(f"{finding.severity}: {finding.category}: {finding.message}")
    return 2 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
