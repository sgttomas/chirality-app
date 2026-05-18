#!/usr/bin/env python3
"""
build_section_map.py — Deterministic candidate Section_Map.csv generator for DBM publication.

Consumes:
  --schema        Approved Publication_Schema.md (markdown table with selector fields)
  --manifest      Frozen Publication_Input_Manifest.md (exact paths only)
  --output-csv    Candidate Section_Map.csv output path (omitted in --dry-run mode)
  --report-md     Coverage / validation report output path
  --dry-run       Governed Gate 3 sizing mode; writes report only

Writes:
  Candidate Section_Map.csv with explicit artifact-path rows.
  Coverage / validation report describing selector results, duplicates, and load findings.

Optional hypergraph diagnostics (AUXILIARY_STRUCTURE_EVIDENCE):
  When the frozen manifest admits a hypergraph snapshot with a planning-
  compatible use mode (AUXILIARY_PLANNING or AUXILIARY_PLANNING_AND_QA),
  the tool emits advisory diagnostics in the coverage report covering:
    - likely overloaded section clusters
    - likely omitted supporting KTYs
    - likely cross-section adjacency hotspots
  These diagnostics remain advisory until the human approves the final
  section map.  They do NOT modify the deterministic selector-based
  mapping or the candidate CSV output.

Determinism:
  Same schema + manifest + execution-root contents -> byte-identical CSV/report output.
  Free-text InclusionRule / ExclusionRule prose is NEVER interpreted by this tool.
  Only machine-readable selector columns drive mapping.

Scope boundary:
  Writes only to --output-csv and --report-md.
  Reads only paths named in the frozen manifest plus the KTY folders under EXECUTION_ROOT.
  Dry-run mode still requires the frozen manifest so sizing uses the same admitted
  input set as the final Gate 4 mapping run.

Exit codes:
  0 = success, no validation findings
  1 = fatal input / parsing error
  2 = success with validation findings requiring human review

Example:
  python3 tools/publication/build_section_map.py \
    --schema /repo/.../_Planning/Publication_Schema.md \
    --manifest /repo/.../_Planning/Publication_Input_Manifest.md \
    --output-csv /repo/.../_Planning/Section_Map.csv \
    --report-md /repo/.../_Planning/Section_Map_Coverage.md
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

ALLOWED_SECTION_TYPES = {
    "OVERVIEW",
    "PROCESS_BASIS",
    "PHILOSOPHY",
    "DATA_REFERENCE",
    "DISCIPLINE_BASIS",
    "REGULATORY",
}

SECTION_MAP_COLUMNS = [
    "SectionID",
    "SectionTitle",
    "SectionType",
    "SourceDomain",
    "CategoryID",
    "KnowledgeTypeID",
    "SubjectID",
    "ArtifactPath",
    "MappingRole",
    "ContributionScope",
    "SCARefs",
    "DecisionRefs",
    "CurrentStateBasis",
    "LifecycleState",
    "LifecycleSource",
    "Notes",
]

REQUIRED_SCHEMA_COLUMNS = [
    "SectionID",
    "SectionOrder",
    "SectionTitle",
    "SectionType",
    "SectionPurpose",
    "InclusionRule",
    "ExclusionRule",
    "IncludeCategoryIDs",
    "IncludeKnowledgeTypeIDs",
    "IncludeCanonicalSchemas",
    "ExcludeCategoryIDs",
    "ExcludeKnowledgeTypeIDs",
    "ExpectedInputs",
    "ExpectedOutputShape",
    "MaxKAFiles",
    "SplitHint",
]

OPTIONAL_SCHEMA_COLUMNS = [
    "MaxEstimatedTokens",
    "ComplexityClass",
    "SplitTrigger",
]

KTY_ARTIFACT_ORDER = {
    "Scoping.md": 10,
    "_STATUS.md": 20,
    "_MEMORY.md": 25,
    "_CONTEXT.md": 30,
    "_REFERENCES.md": 40,
    "_DEPENDENCIES.md": 50,
}

RETIRED_STATE_VALUES = {"RETIRED", "ARCHIVED", "TOMBSTONE", "RETIRED_NO_FACTUAL_USE", "NO_FACTUAL_USE"}


def fatal(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def require_within(path: Path, root: Path, label: str) -> None:
    """Fail fast if a requested output path escapes the publication tool root."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fatal(f"{label} must resolve under publication root {root}: {path}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fatal(f"File not found: {path}")


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            normalized_rows: List[Dict[str, str]] = []
            for row in reader:
                normalized: Dict[str, str] = {}
                for key, value in row.items():
                    normalized_key = (key or "").strip()
                    if isinstance(value, list):
                        normalized_value = "; ".join((item or "").strip() for item in value if (item or "").strip())
                    else:
                        normalized_value = (value or "").strip()
                    normalized[normalized_key] = normalized_value
                normalized_rows.append(normalized)
            return normalized_rows
    except FileNotFoundError:
        fatal(f"CSV file not found: {path}")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def normalize_token(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", " ", value.upper()).strip()


def parse_list_cell(value: str) -> List[str]:
    if not value:
        return []
    normalized = value.replace("\n", ";")
    parts = re.split(r"[;,]", normalized)
    cleaned: List[str] = []
    seen = set()
    for part in parts:
        token = part.strip().strip("`")
        if not token:
            continue
        if token not in seen:
            cleaned.append(token)
            seen.add(token)
    return cleaned


def parse_markdown_tables(text: str) -> List[List[Dict[str, str]]]:
    tables: List[List[Dict[str, str]]] = []
    block: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("|") and line.strip().endswith("|"):
            block.append(line)
            continue
        if block:
            table = _parse_table_block(block)
            if table:
                tables.append(table)
            block = []
    if block:
        table = _parse_table_block(block)
        if table:
            tables.append(table)
    return tables


def _parse_table_block(lines: Sequence[str]) -> List[Dict[str, str]]:
    if len(lines) < 2:
        return []
    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(header) != len(separator):
        return []
    if not all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in separator):
        return []
    rows: List[Dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < len(header):
            cells.extend([""] * (len(header) - len(cells)))
        if len(cells) > len(header):
            cells = cells[: len(header)]
        rows.append({header[idx]: cells[idx] for idx in range(len(header))})
    return rows


def find_table_with_columns(text: str, required_columns: Sequence[str]) -> List[Dict[str, str]]:
    for table in parse_markdown_tables(text):
        if not table:
            continue
        keys = set(table[0].keys())
        if all(column in keys for column in required_columns):
            return table
    fatal(f"Unable to find markdown table with required columns: {', '.join(required_columns)}")


def parse_manifest(markdown_path: Path) -> Dict[str, object]:
    text = read_text(markdown_path)
    current_heading = "ROOT"
    headings: Dict[str, List[Path]] = defaultdict(list)
    explicit: Dict[str, str] = {}

    code_span_re = re.compile(r"`([^`]+)`")
    kv_bold_colon_inside_re = re.compile(r"^\s*(?:-\s*)?\*\*`?([A-Za-z0-9_ /-]+?)`?:\*\*\s*(.+?)\s*$")
    kv_re = re.compile(r"^\s*(?:-\s*)?(?:\*\*)?`?([A-Za-z0-9_ /-]+?)`?(?:\*\*)?\s*:\s*(.+?)\s*$")

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading_match = re.match(r"^(#+)\s+(.*)$", line.strip())
        if heading_match:
            current_heading = heading_match.group(2).strip()
            continue
        kv_match = kv_bold_colon_inside_re.match(line) or kv_re.match(line)
        if kv_match:
            key = normalize_space(kv_match.group(1)).rstrip(":").upper().replace(" ", "_").replace("/", "_")
            value = kv_match.group(2).strip()
            code_value_match = re.match(r"`([^`]+)`(?:\s+.*)?$", value)
            if code_value_match:
                value = code_value_match.group(1)
            explicit[key] = value
        for code_span in code_span_re.findall(line):
            if _looks_like_path(code_span):
                headings[current_heading].append(_resolve_manifest_path(markdown_path.parent, code_span))
        stripped = line.strip().lstrip("- ").strip()
        if stripped and "`" not in stripped and _looks_like_path(stripped):
            headings[current_heading].append(_resolve_manifest_path(markdown_path.parent, stripped))

    all_paths: List[Path] = []
    seen = set()
    for items in headings.values():
        for path in items:
            key = str(path)
            if key not in seen:
                all_paths.append(path)
                seen.add(key)

    execution_root: Optional[Path] = None
    publication_root: Optional[Path] = None
    if "EXECUTION_ROOT" in explicit:
        execution_root = _resolve_manifest_path(markdown_path.parent, explicit["EXECUTION_ROOT"])
    if "PUBLICATION_ROOT" in explicit:
        publication_root = _resolve_manifest_path(markdown_path.parent, explicit["PUBLICATION_ROOT"])
    if execution_root is None and publication_root is not None:
        execution_root = publication_root.parent
    if publication_root is None and execution_root is not None:
        publication_root = execution_root / "_Publication" / "DBM"

    if execution_root is None:
        for path in all_paths:
            parts = path.parts
            if "_Decomposition" in parts or "_Sources" in parts or "_ScopeChange" in parts:
                idx = parts.index("_Decomposition") if "_Decomposition" in parts else parts.index("_Sources") if "_Sources" in parts else parts.index("_ScopeChange")
                execution_root = Path(*parts[:idx])
                break
    if execution_root is None:
        fatal("Manifest does not expose EXECUTION_ROOT and execution root could not be inferred from listed paths.")
    if publication_root is None:
        publication_root = execution_root / "_Publication" / "DBM"

    grouped = {
        "decomposition_files": [p for p in all_paths if "_Decomposition" in p.parts and p.is_file()],
        "source_files": [p for p in all_paths if "_Sources" in p.parts and p.is_file()],
        "scope_change_files": [p for p in all_paths if "_ScopeChange" in p.parts and p.is_file()],
        "scope_change_dirs": [p for p in all_paths if "_ScopeChange" in p.parts and p.exists() and p.is_dir()],
        "all_paths": all_paths,
        "explicit": explicit,
        "execution_root": execution_root,
        "publication_root": publication_root,
    }
    return grouped


def _looks_like_path(value: str) -> bool:
    value = value.strip()
    if not value:
        return False
    return any(
        [
            "/" in value,
            value.endswith((".md", ".csv", ".json", ".txt", ".py")),
            value.startswith("."),
        ]
    )


def _resolve_manifest_path(base_dir: Path, raw_value: str) -> Path:
    value = raw_value.strip().strip("`").strip()
    candidate = Path(value)
    return candidate if candidate.is_absolute() else (base_dir / candidate).resolve()


def classify_manifest_csvs(paths: Iterable[Path]) -> Dict[str, Path]:
    classified: Dict[str, Path] = {}
    for path in sorted(paths):
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            try:
                header = next(reader)
            except StopIteration:
                continue
        columns = {col.strip() for col in header}
        if {"KnowledgeTypeID", "ParentCategoryID"}.issubset(columns):
            classified.setdefault("kty_register", path)
        elif {"SubjectID", "ParentKnowledgeTypeID"}.issubset(columns):
            classified.setdefault("subject_register", path)
        elif {"UnitID", "CategoryID"}.issubset(columns) and ("KnowledgeTypeID" in columns or "KnowledgeTypeID(s)" in columns):
            classified.setdefault("ledger", path)
        elif "CategoryID" in columns and ("ScopeDescription" in columns or "BoundaryRule" in columns):
            classified.setdefault("category_register", path)
        elif "DecisionID" in columns or "DecisionRef" in columns:
            classified.setdefault("decision_log", path)
        elif "OpenIssueID" in columns or ("OpenIssueType" in columns and "Status" in columns):
            classified.setdefault("open_issues", path)
        elif "CanonicalTerm" in columns or "PreferredTerm" in columns:
            classified.setdefault("vocabulary_map", path)
    missing = [name for name in ("category_register", "kty_register", "subject_register", "ledger") if name not in classified]
    if missing:
        fatal(f"Manifest is missing required CSV inputs or they could not be classified: {', '.join(missing)}")
    return classified


def load_categories(path: Path) -> Dict[str, Dict[str, str]]:
    rows = read_csv_rows(path)
    categories: Dict[str, Dict[str, str]] = {}
    for row in rows:
        category_id = row.get("CategoryID", "")
        if not category_id:
            continue
        categories[category_id] = {
            "CategoryID": category_id,
            "Name": row.get("Name") or row.get("Category") or row.get("CategoryName") or category_id,
        }
    return categories


def load_ktys(path: Path) -> Dict[str, Dict[str, str]]:
    rows = read_csv_rows(path)
    records: Dict[str, Dict[str, str]] = {}
    for row in rows:
        kty_id = row.get("KnowledgeTypeID", "")
        if not kty_id:
            continue
        canonical_schema = row.get("CanonicalSchema", "") or row.get("CanonicalSchemaType", "")
        records[kty_id] = {
            "KnowledgeTypeID": kty_id,
            "Name": row.get("Name", "") or kty_id,
            "ParentCategoryID": row.get("ParentCategoryID", ""),
            "CanonicalSchema": canonical_schema,
            "CanonicalSchemaNormalized": normalize_token(canonical_schema),
        }
    return records


def load_subjects(path: Path) -> Dict[str, Dict[str, str]]:
    rows = read_csv_rows(path)
    records: Dict[str, Dict[str, str]] = {}
    for row in rows:
        subject_id = row.get("SubjectID", "")
        if not subject_id:
            continue
        records[subject_id] = {
            "SubjectID": subject_id,
            "ParentKnowledgeTypeID": row.get("ParentKnowledgeTypeID", ""),
            "Name": row.get("Name", "") or row.get("SubjectName", "") or subject_id,
        }
    return records


def load_ledger_index(path: Path) -> Dict[str, Dict[str, object]]:
    rows = read_csv_rows(path)
    by_kty: Dict[str, Dict[str, object]] = defaultdict(lambda: {"decision_refs": set(), "unit_ids": set()})
    by_subject: Dict[str, Dict[str, object]] = defaultdict(lambda: {"decision_refs": set(), "unit_ids": set()})
    by_unit: Dict[str, Dict[str, object]] = defaultdict(lambda: {"kty_ids": set(), "subject_ids": set()})

    for row in rows:
        unit_id = row.get("UnitID", "") or row.get("AtomicUnitID", "")
        kty_ids = parse_list_cell(row.get("KnowledgeTypeID", "") or row.get("KnowledgeTypeID(s)", ""))
        subject_ids = parse_list_cell(row.get("SubjectID", "") or row.get("SubjectID(s)", ""))
        decision_refs = parse_list_cell(row.get("DecisionRef", ""))

        for kty_id in kty_ids:
            by_kty[kty_id]["decision_refs"].update(decision_refs)
            if unit_id:
                by_kty[kty_id]["unit_ids"].add(unit_id)
        for subject_id in subject_ids:
            by_subject[subject_id]["decision_refs"].update(decision_refs)
            if unit_id:
                by_subject[subject_id]["unit_ids"].add(unit_id)
        if unit_id:
            by_unit[unit_id]["kty_ids"].update(kty_ids)
            by_unit[unit_id]["subject_ids"].update(subject_ids)

    return {"by_kty": by_kty, "by_subject": by_subject, "by_unit": by_unit}


def load_active_sca_refs(manifest: Dict[str, object], ledger_index: Dict[str, Dict[str, object]]) -> Tuple[Dict[str, set], Dict[str, set], str]:
    scope_dirs: List[Path] = list(manifest["scope_change_dirs"])
    scope_files: List[Path] = list(manifest["scope_change_files"])
    active_snapshot: Optional[Path] = None
    latest_pointer = next((p for p in scope_files if p.name == "_LATEST.md"), None)

    if latest_pointer and latest_pointer.exists():
        latest_text = read_text(latest_pointer)
        snapshot_match = re.search(r"Snapshot\s*[:|-]\s*`?([^`\n]+/)`?", latest_text)
        if snapshot_match:
            candidate = (latest_pointer.parent / snapshot_match.group(1).strip().rstrip("/")).resolve()
            if candidate.exists() and candidate.is_dir():
                active_snapshot = candidate

    if active_snapshot is None:
        active_snapshot = sorted(scope_dirs, key=lambda item: item.name)[-1] if scope_dirs else None

    current_state_basis = active_snapshot.name if active_snapshot else "APPROVED_DECOMPOSITION"
    kty_to_sca: Dict[str, set] = defaultdict(set)
    subject_to_sca: Dict[str, set] = defaultdict(set)
    if not active_snapshot:
        return kty_to_sca, subject_to_sca, current_state_basis

    amendment_id = active_snapshot.name.split("_")[0]
    actions_csv = active_snapshot / "Amendment_Actions.csv"
    if actions_csv.exists():
        for row in read_csv_rows(actions_csv):
            action_id = row.get("AmendmentID", "") or amendment_id
            entity_type = row.get("EntityType", "")
            entity_id = row.get("EntityID", "")
            if not entity_id:
                continue
            if entity_type in {"KNOWLEDGE_TYPE", "KTY"} or entity_id.startswith("KTY-"):
                kty_to_sca[entity_id].add(action_id)
            elif entity_type in {"SUBJECT", "KNOWLEDGE_SUBJECT", "SUB"} or entity_id.startswith("SUB-"):
                subject_to_sca[entity_id].add(action_id)
            elif entity_type in {"HANDBOOK_UNIT", "ATOMIC_UNIT", "UNIT"} or entity_id.startswith("HBK-"):
                unit_mapping = ledger_index["by_unit"].get(entity_id, {})
                for kty_id in unit_mapping.get("kty_ids", set()):
                    kty_to_sca[kty_id].add(action_id)
                for subject_id in unit_mapping.get("subject_ids", set()):
                    subject_to_sca[subject_id].add(action_id)
        return kty_to_sca, subject_to_sca, current_state_basis

    run_summary = active_snapshot / "RUN_SUMMARY.md"
    if run_summary.exists():
        text = read_text(run_summary)
        for entity_id in sorted(set(re.findall(r"\b(KTY-[A-Za-z0-9_-]+|SUB-[A-Za-z0-9_-]+)\b", text))):
            if entity_id.startswith("KTY-"):
                kty_to_sca[entity_id].add(amendment_id)
            else:
                subject_to_sca[entity_id].add(amendment_id)
    return kty_to_sca, subject_to_sca, current_state_basis


def _active_scope_snapshot(manifest: Dict[str, object]) -> Optional[Path]:
    scope_dirs: List[Path] = list(manifest["scope_change_dirs"])
    scope_files: List[Path] = list(manifest["scope_change_files"])
    latest_pointer = next((p for p in scope_files if p.name == "_LATEST.md"), None)
    if latest_pointer and latest_pointer.exists():
        latest_text = read_text(latest_pointer)
        snapshot_match = re.search(r"Snapshot\s*[:|-]\s*`?([^`\n]+/)`?", latest_text)
        if snapshot_match:
            candidate = (latest_pointer.parent / snapshot_match.group(1).strip().rstrip("/")).resolve()
            if candidate.exists() and candidate.is_dir():
                return candidate
    return sorted(scope_dirs, key=lambda item: item.name)[-1] if scope_dirs else None


def _matches_kty_id(candidate: str, kty_id: str) -> bool:
    if not candidate:
        return False
    short_id = kty_id.split("_", 1)[0]
    return candidate == kty_id or candidate == short_id or candidate.startswith(f"{short_id}_")


def load_sca_lifecycle_states(manifest: Dict[str, object]) -> Dict[str, Tuple[str, str]]:
    states: Dict[str, Tuple[str, str]] = {}
    active_snapshot = _active_scope_snapshot(manifest)
    if not active_snapshot:
        return states

    actions_csv = active_snapshot / "Amendment_Actions.csv"
    if actions_csv.exists():
        for row in read_csv_rows(actions_csv):
            entity_id = row.get("EntityID", "")
            action_type = row.get("ActionType", "").strip().upper()
            entity_type = row.get("EntityType", "").strip().upper()
            if not entity_id or not (entity_id.startswith("KTY-") or entity_type in {"KTY", "KNOWLEDGE_TYPE"}):
                continue
            if action_type == "REMOVE":
                states[entity_id] = ("RETIRED", "SCA_ACTION")

    manifest_csv = active_snapshot / "KTY_Remediation_Manifest.csv"
    if manifest_csv.exists():
        for row in read_csv_rows(manifest_csv):
            kty_id = row.get("KTYID", "") or row.get("EntityID", "")
            if not kty_id:
                continue
            state_blob = " ".join(
                [
                    row.get("ContentAction", ""),
                    row.get("CONTENT_DISPOSITION_STATE", ""),
                    row.get("FACTUAL_USE_GATE", ""),
                ]
            ).upper()
            if any(token in state_blob for token in ["ARCHIVE_AND_STUB", "RETIRED_NO_FACTUAL_USE", "ARCHIVED", "RETIRED"]):
                states[kty_id] = ("RETIRED", "SCA_KTY_REMEDIATION")
    return states


def parse_status_lifecycle(status_path: Path) -> str:
    if not status_path.exists():
        return "UNKNOWN"
    text = read_text(status_path)
    upper = text.upper()

    explicit_state_patterns = [
        r"\*\*CURRENT STATE:\*\*\s*([A-Z0-9_\- ]+)",
        r"CURRENT STATE\s*[:|]\s*([A-Z0-9_\- ]+)",
        r"LIFECYCLESTATE\s*[:|]\s*([A-Z0-9_\- ]+)",
        r"LIFECYCLE STATE\s*[:|]\s*([A-Z0-9_\- ]+)",
        r"STATUS\s*[:|]\s*([A-Z0-9_\- ]+)",
    ]
    for pattern in explicit_state_patterns:
        match = re.search(pattern, upper)
        if not match:
            continue
        state = normalize_space(match.group(1)).upper()
        if any(token in state for token in RETIRED_STATE_VALUES):
            return "RETIRED"
        if any(token in state for token in ["INITIALIZED", "COMPLETE", "CURRENT", "ACTIVE", "READY"]):
            return "ACTIVE"

    head = "\n".join(upper.splitlines()[:20])
    if (
        "[RETIRED]" in head
        or "NON-FACTUAL TOMBSTONE STUB" in head
        or "FACTUAL USE GATE | RETIRED_NO_FACTUAL_USE" in head
        or "RETIRED_NO_FACTUAL_USE" in head
    ):
        return "RETIRED"
    if re.search(r"STATE SET TO\s+(INITIALIZED|COMPLETE|CURRENT|ACTIVE|READY)", upper):
        return "ACTIVE"
    if "OPEN" in upper or "DRAFT" in upper:
        return "OPEN"
    return "UNKNOWN"


def detect_tombstone_state(artifact_path: Path) -> str:
    if not artifact_path.exists() or not artifact_path.is_file():
        return "UNKNOWN"
    try:
        text = artifact_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return "UNKNOWN"
    head = "\n".join(text.upper().splitlines()[:10])
    if (
        "[RETIRED]" in head
        or "NON-FACTUAL TOMBSTONE STUB" in head
        or "FACTUAL USE GATE | RETIRED_NO_FACTUAL_USE" in head
        or "FACTUAL USE GATE | NO_FACTUAL_USE" in head
        or "RETIRED_NO_FACTUAL_USE" in head
    ):
        return "RETIRED"
    return "UNKNOWN"


def resolve_lifecycle_state(
    manifest_admitted: bool,
    sca_lifecycle: Tuple[str, str],
    status_path: Path,
    artifact_path: Path,
) -> Tuple[str, str]:
    if not manifest_admitted:
        return ("NOT_ADMITTED", "MANIFEST")
    if sca_lifecycle and sca_lifecycle[0] in RETIRED_STATE_VALUES:
        return sca_lifecycle
    status_state = parse_status_lifecycle(status_path)
    if status_state in RETIRED_STATE_VALUES:
        return (status_state, "_STATUS.md")
    tombstone_state = detect_tombstone_state(artifact_path)
    if tombstone_state in RETIRED_STATE_VALUES:
        return (tombstone_state, "TOMBSTONE_HEADER")
    if status_state != "UNKNOWN":
        return (status_state, "_STATUS.md")
    return ("ACTIVE", "MANIFEST")


def count_open_issues_for_kty(open_issue_rows: Sequence[Dict[str, str]], kty_id: str, subject_ids: Iterable[str]) -> int:
    if not open_issue_rows:
        return 0
    needles = {kty_id, kty_id.split("_", 1)[0], *[sid for sid in subject_ids if sid]}
    count = 0
    for row in open_issue_rows:
        blob = " ".join(row.values())
        if any(needle and needle in blob for needle in needles):
            count += 1
    return count


def locate_kty_dir(execution_root: Path, kty_id: str) -> Optional[Path]:
    candidates = sorted(
        execution_root.glob(f"CAT-*/1_Working/{kty_id}*"),
        key=lambda path: str(path),
    )
    directories = [path.resolve() for path in candidates if path.is_dir()]
    if not directories:
        return None
    return directories[0]


def parse_scoping_artifact_plan(scoping_path: Path) -> List[Dict[str, str]]:
    if not scoping_path.exists():
        return []
    text = read_text(scoping_path)
    table: List[Dict[str, str]] = []
    for candidate in parse_markdown_tables(text):
        if candidate and all(column in candidate[0] for column in ["ArtifactID", "SubjectID", "Filename"]):
            table = candidate
            break
    if not table:
        return []
    normalized_rows: List[Dict[str, str]] = []
    for row in table:
        filename = row.get("Filename", "").strip().strip("`")
        if not filename:
            continue
        normalized_rows.append(
            {
                "ArtifactID": row.get("ArtifactID", ""),
                "SubjectID": row.get("SubjectID", ""),
                "SubjectName": row.get("Subject Name", "") or row.get("Subject Name", "") or row.get("Subject", ""),
                "Filename": filename,
            }
        )
    return normalized_rows


def parse_schema(path: Path) -> List[Dict[str, str]]:
    rows = find_table_with_columns(read_text(path), REQUIRED_SCHEMA_COLUMNS)
    normalized: List[Dict[str, str]] = []
    for row in rows:
        section_id = normalize_space(row.get("SectionID", ""))
        if not section_id:
            continue
        section_type = normalize_space(row.get("SectionType", "")).upper()
        if section_type not in ALLOWED_SECTION_TYPES:
            fatal(f"Unsupported SectionType '{section_type}' in schema row {section_id}")
        normalized.append({key: normalize_space(row.get(key, "")) for key in REQUIRED_SCHEMA_COLUMNS + OPTIONAL_SCHEMA_COLUMNS})
        normalized[-1]["SectionType"] = section_type
    normalized.sort(key=lambda row: (_safe_int(row.get("SectionOrder", "999999")), row["SectionID"]))
    if not normalized:
        fatal("Publication schema contains no usable section rows.")
    return normalized


def _safe_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 999999


def select_ktys_for_section(section: Dict[str, str], ktys: Dict[str, Dict[str, str]]) -> List[str]:
    include_categories = set(parse_list_cell(section.get("IncludeCategoryIDs", "")))
    include_ktys = set(parse_list_cell(section.get("IncludeKnowledgeTypeIDs", "")))
    include_schemas = {normalize_token(v) for v in parse_list_cell(section.get("IncludeCanonicalSchemas", ""))}
    exclude_categories = set(parse_list_cell(section.get("ExcludeCategoryIDs", "")))
    exclude_ktys = set(parse_list_cell(section.get("ExcludeKnowledgeTypeIDs", "")))

    selected = set()
    for kty_id, record in ktys.items():
        if include_categories and record.get("ParentCategoryID", "") in include_categories:
            selected.add(kty_id)
        if include_ktys and kty_id in include_ktys:
            selected.add(kty_id)
        if include_schemas and record.get("CanonicalSchemaNormalized", "") in include_schemas:
            selected.add(kty_id)

    selected = {
        kty_id
        for kty_id in selected
        if kty_id not in exclude_ktys and ktys[kty_id].get("ParentCategoryID", "") not in exclude_categories
    }
    return sorted(selected)


def build_candidate_rows(
    schema_rows: List[Dict[str, str]],
    execution_root: Path,
    categories: Dict[str, Dict[str, str]],
    ktys: Dict[str, Dict[str, str]],
    subjects: Dict[str, Dict[str, str]],
    ledger_index: Dict[str, Dict[str, object]],
    kty_to_sca: Dict[str, set],
    subject_to_sca: Dict[str, set],
    sca_lifecycle_states: Dict[str, Tuple[str, str]],
    open_issue_rows: Sequence[Dict[str, str]],
    current_state_basis: str,
) -> Tuple[List[Dict[str, str]], List[str], Dict[str, Dict[str, object]]]:
    findings: List[str] = []
    rows: List[Dict[str, str]] = []
    section_stats: Dict[str, Dict[str, object]] = {}
    source_domain = execution_root.name

    for section in schema_rows:
        section_id = section["SectionID"]
        selected_ktys = select_ktys_for_section(section, ktys)
        section_findings: List[str] = []
        prose_note = ""
        if (section.get("InclusionRule") or section.get("ExclusionRule")) and not (
            section.get("IncludeCategoryIDs") or section.get("IncludeKnowledgeTypeIDs") or section.get("IncludeCanonicalSchemas")
        ):
            section_findings.append("Section has prose intent but no machine-readable include selectors.")
        if not selected_ktys:
            section_findings.append("No KTYs matched the machine-readable selectors.")

        section_ka_count = 0
        section_artifact_count = 0
        section_kty_dirs_missing = 0
        section_estimated_tokens = 0
        section_sca_refs: set = set()
        section_open_issue_count = 0
        section_lifecycle_findings = 0
        unique_categories = set()
        resolved_kty_count = 0

        for kty_id in selected_ktys:
            kty_record = ktys[kty_id]
            category_id = kty_record.get("ParentCategoryID", "")
            unique_categories.add(category_id)
            kty_dir = locate_kty_dir(execution_root, kty_id)
            if kty_dir is None:
                section_kty_dirs_missing += 1
                section_findings.append(f"KTY directory not found for {kty_id} under execution root.")
                continue
            resolved_kty_count += 1

            scoping_path = kty_dir / "Scoping.md"
            context_path = kty_dir / "_CONTEXT.md"
            references_path = kty_dir / "_REFERENCES.md"
            status_path = kty_dir / "_STATUS.md"
            memory_path = kty_dir / "_MEMORY.md"
            artifact_plan = parse_scoping_artifact_plan(scoping_path) if scoping_path.exists() else []
            if not scoping_path.exists():
                section_findings.append(f"Scoping.md missing for {kty_id}.")
            if not artifact_plan:
                available_kas = sorted(kty_dir.glob("KA-*.md"))
                for ka_path in available_kas:
                    artifact_plan.append({
                        "ArtifactID": ka_path.stem.split("_")[0],
                        "SubjectID": "",
                        "SubjectName": "",
                        "Filename": ka_path.name,
                    })
                if available_kas:
                    section_findings.append(f"Artifact Plan table missing or unreadable in {scoping_path.name}; fell back to KA file enumeration for {kty_id}.")

            subject_ids_for_kty = [artifact.get("SubjectID", "") for artifact in artifact_plan]
            section_open_issue_count += count_open_issues_for_kty(open_issue_rows, kty_id, subject_ids_for_kty)
            sca_lifecycle = next(
                (state for state_id, state in sca_lifecycle_states.items() if _matches_kty_id(state_id, kty_id)),
                ("", ""),
            )

            support_artifacts = [
                (scoping_path, "SUPPORTING", "BACKGROUND_ONLY", "KTY scoping artifact."),
                (status_path, "SUPPORTING", "VALUES_ONLY", "KTY readiness gate artifact."),
                (memory_path, "CONTEXT_ONLY", "BACKGROUND_ONLY", "KTY memory artifact; read only as non-authoritative context paired with _STATUS.md."),
                (context_path, "CONTEXT_ONLY", "BACKGROUND_ONLY", "KTY context artifact."),
                (references_path, "SUPPORTING", "BACKGROUND_ONLY", "KTY references artifact."),
            ]
            for artifact_path, mapping_role, contribution_scope, notes in support_artifacts:
                if artifact_path.exists():
                    lifecycle_state, lifecycle_source = resolve_lifecycle_state(
                        manifest_admitted=True,
                        sca_lifecycle=sca_lifecycle,
                        status_path=status_path,
                        artifact_path=artifact_path,
                    )
                    if lifecycle_state in RETIRED_STATE_VALUES:
                        section_lifecycle_findings += 1
                        section_findings.append(
                            f"RETIRED_KTY_MAPPED: {kty_id} support artifact {artifact_path.name} resolved {lifecycle_state} via {lifecycle_source}."
                        )
                    rows.append(
                        {
                            "SectionID": section_id,
                            "SectionTitle": section["SectionTitle"],
                            "SectionType": section["SectionType"],
                            "SourceDomain": source_domain,
                            "CategoryID": category_id,
                            "KnowledgeTypeID": kty_id,
                            "SubjectID": "",
                            "ArtifactPath": str(artifact_path.resolve()),
                            "MappingRole": mapping_role,
                            "ContributionScope": contribution_scope,
                            "SCARefs": "; ".join(sorted(kty_to_sca.get(kty_id, set()))),
                            "DecisionRefs": "; ".join(sorted(ledger_index["by_kty"].get(kty_id, {}).get("decision_refs", set()))),
                            "CurrentStateBasis": current_state_basis,
                            "LifecycleState": lifecycle_state,
                            "LifecycleSource": lifecycle_source,
                            "Notes": notes,
                        }
                    )
                    section_artifact_count += 1
                else:
                    section_findings.append(f"Expected support artifact missing for {kty_id}: {artifact_path.name}")

            for artifact in artifact_plan:
                artifact_file = kty_dir / artifact["Filename"]
                if not artifact_file.exists():
                    section_findings.append(f"Artifact listed in Scoping.md but file missing: {artifact_file.name} for {kty_id}")
                    continue
                subject_id = artifact.get("SubjectID", "")
                decision_refs = set(ledger_index["by_kty"].get(kty_id, {}).get("decision_refs", set()))
                if subject_id:
                    decision_refs.update(ledger_index["by_subject"].get(subject_id, {}).get("decision_refs", set()))
                sca_refs = set(kty_to_sca.get(kty_id, set()))
                if subject_id:
                    sca_refs.update(subject_to_sca.get(subject_id, set()))
                section_sca_refs.update(sca_refs)
                notes = artifact.get("SubjectName", "") or subjects.get(subject_id, {}).get("Name", "")
                note_text = f"Artifact Plan row {artifact.get('ArtifactID', '').strip()}"
                if notes:
                    note_text += f" — {notes}"
                lifecycle_state, lifecycle_source = resolve_lifecycle_state(
                    manifest_admitted=True,
                    sca_lifecycle=sca_lifecycle,
                    status_path=status_path,
                    artifact_path=artifact_file,
                )
                mapping_role = "PRIMARY"
                contribution_scope = "FULL_ARTIFACT"
                if lifecycle_state in RETIRED_STATE_VALUES:
                    mapping_role = "CONTEXT_ONLY"
                    contribution_scope = "BACKGROUND_ONLY"
                    section_lifecycle_findings += 1
                    section_findings.append(
                        f"RETIRED_KTY_MAPPED: {kty_id} artifact {artifact_file.name} resolved {lifecycle_state} via {lifecycle_source}; not mapped as PRIMARY."
                    )
                try:
                    section_estimated_tokens += max(1, artifact_file.stat().st_size // 4)
                except OSError:
                    pass
                rows.append(
                    {
                        "SectionID": section_id,
                        "SectionTitle": section["SectionTitle"],
                        "SectionType": section["SectionType"],
                        "SourceDomain": source_domain,
                        "CategoryID": category_id,
                        "KnowledgeTypeID": kty_id,
                        "SubjectID": subject_id,
                        "ArtifactPath": str(artifact_file.resolve()),
                        "MappingRole": mapping_role,
                        "ContributionScope": contribution_scope,
                        "SCARefs": "; ".join(sorted(sca_refs)),
                        "DecisionRefs": "; ".join(sorted(decision_refs)),
                        "CurrentStateBasis": current_state_basis,
                        "LifecycleState": lifecycle_state,
                        "LifecycleSource": lifecycle_source,
                        "Notes": note_text,
                    }
                )
                section_ka_count += 1
                section_artifact_count += 1

        max_ka_files = _safe_int(section.get("MaxKAFiles", ""))
        if section_ka_count > max_ka_files:
            section_findings.append(
                f"Section matched {section_ka_count} KA files which exceeds MaxKAFiles={max_ka_files}."
            )
        max_estimated_tokens = _safe_int(section.get("MaxEstimatedTokens", ""))
        split_pressure_reasons: List[str] = []
        if section_ka_count > max_ka_files:
            split_pressure_reasons.append("KAFileCount>MaxKAFiles")
        if max_estimated_tokens != 999999 and section_estimated_tokens > max_estimated_tokens:
            split_pressure_reasons.append("EstimatedTokens>MaxEstimatedTokens")
        split_pressure = "YES" if split_pressure_reasons else "NO"

        section_stats[section_id] = {
            "section": section,
            "selected_ktys": selected_ktys,
            "resolved_kty_count": resolved_kty_count,
            "section_ka_count": section_ka_count,
            "section_artifact_count": section_artifact_count,
            "estimated_tokens": section_estimated_tokens,
            "sca_ref_count": len(section_sca_refs),
            "open_issue_count": section_open_issue_count,
            "lifecycle_findings": section_lifecycle_findings,
            "max_ka_files": max_ka_files,
            "max_estimated_tokens": "" if max_estimated_tokens == 999999 else max_estimated_tokens,
            "split_pressure": split_pressure,
            "split_pressure_reasons": split_pressure_reasons,
            "unique_categories": sorted(unique_categories),
            "findings": section_findings,
            "kty_dirs_missing": section_kty_dirs_missing,
            "prose_note": prose_note,
        }
        findings.extend([f"[{section_id}] {finding}" for finding in section_findings])

    rows.sort(key=_row_sort_key)
    return rows, findings, section_stats


def _row_sort_key(row: Dict[str, str]) -> Tuple[str, int, str, str]:
    artifact_name = Path(row["ArtifactPath"]).name
    if artifact_name.startswith("KA-"):
        artifact_order = 100 + _safe_int(artifact_name.split("_")[0].replace("KA-", ""))
    else:
        artifact_order = KTY_ARTIFACT_ORDER.get(artifact_name, 999)
    return (row["SectionID"], artifact_order, row["KnowledgeTypeID"], row["ArtifactPath"])


# ---------------------------------------------------------------------------
# Hypergraph use-mode constants and advisory diagnostic helpers.
#
# Hypergraph evidence is AUXILIARY ONLY for section-map generation.  The
# diagnostics emitted here are advisory until the human approves the final
# section map.  They must never override the deterministic selector-based
# mapping.  See plan section "Publication Tooling Changes / Tool 3".
# ---------------------------------------------------------------------------
HYPERGRAPH_PLANNING_MODES = {
    "AUXILIARY_PLANNING",
    "AUXILIARY_PLANNING_AND_QA",
}


def _read_hypergraph_manifest_fields(manifest: Dict[str, object]) -> Dict[str, str]:
    """Extract hypergraph-related fields from the parsed manifest explicit dict."""
    explicit = manifest.get("explicit", {})
    if not isinstance(explicit, dict):
        return {}
    return {
        "use_mode": explicit.get("HYPERGRAPH_USE_MODE", ""),
        "snapshot_path": explicit.get("HYPERGRAPH_SNAPSHOT_PATH", ""),
        "evidence_root": explicit.get("HYPERGRAPH_EVIDENCE_ROOT", ""),
        "nodes_path": explicit.get("HYPERGRAPH_NODES_PATH", ""),
        "hyperedges_path": explicit.get("HYPERGRAPH_HYPEREDGES_PATH", ""),
        "qa_verdict": explicit.get("HYPERGRAPH_QA_VERDICT", ""),
    }


def _hypergraph_planning_allowed(hg_fields: Dict[str, str]) -> bool:
    """Return True only when the manifest admits hypergraph evidence for
    planning-stage use."""
    return hg_fields.get("use_mode", "").strip().upper() in HYPERGRAPH_PLANNING_MODES


def _load_hypergraph_evidence_for_diagnostics(
    hg_fields: Dict[str, str], manifest_dir: Path
) -> Dict[str, object]:
    """Load minimal hypergraph evidence for advisory diagnostics.

    Returns a dict with keys: nodes, hyperedges (lists of dicts).
    Missing / unreadable files yield empty lists.
    """
    result: Dict[str, object] = {"nodes": [], "hyperedges": []}

    def _resolve(raw: str) -> Optional[Path]:
        if not raw:
            return None
        p = Path(raw.strip())
        if not p.is_absolute():
            p = (manifest_dir / p).resolve()
        return p if p.exists() else None

    nodes_path = _resolve(hg_fields.get("nodes_path", ""))
    if nodes_path:
        result["nodes"] = read_csv_rows(nodes_path)

    hyperedges_path = _resolve(hg_fields.get("hyperedges_path", ""))
    if hyperedges_path:
        result["hyperedges"] = read_csv_rows(hyperedges_path)

    return result


def build_hypergraph_advisory_diagnostics(
    hg_evidence: Dict[str, object],
    csv_rows: List[Dict[str, str]],
    section_stats: Dict[str, Dict[str, object]],
) -> List[str]:
    """Emit advisory diagnostics using hypergraph structural evidence.

    Diagnostics are informational only — they remain advisory until the
    human approves the final section map.

    Three diagnostic types:
      1. Likely overloaded section clusters — sections whose mapped KTYs
         form dense subgraphs in the hypergraph.
      2. Likely omitted supporting KTYs — KTYs that appear in hyperedges
         adjacent to mapped KTYs but are not mapped themselves.
      3. Likely cross-section adjacency hotspots — KTY pairs that share
         multiple hyperedges and land in different sections.
    """
    diagnostics: List[str] = []
    hyperedges: List[Dict[str, str]] = list(hg_evidence.get("hyperedges", []))
    if not hyperedges:
        return diagnostics

    # Collect all mapped KTY IDs and their section assignments
    kty_to_sections: Dict[str, set] = defaultdict(set)
    all_mapped_ktys: set = set()
    for row in csv_rows:
        kty_id = row.get("KnowledgeTypeID", "")
        section_id = row.get("SectionID", "")
        if kty_id and section_id:
            kty_to_sections[kty_id].add(section_id)
            all_mapped_ktys.add(kty_id)

    # Build KTY adjacency from hyperedges
    kty_adjacency: Dict[str, set] = defaultdict(set)
    for edge in hyperedges:
        source = edge.get("Source", "") or edge.get("SourceID", "")
        target = edge.get("Target", "") or edge.get("TargetID", "")
        if source.startswith("KTY-") and target.startswith("KTY-"):
            kty_adjacency[source].add(target)
            kty_adjacency[target].add(source)

    # 1. Overloaded section clusters
    for section_id, stats in section_stats.items():
        selected_ktys = set(stats.get("selected_ktys", []))
        if len(selected_ktys) < 2:
            continue
        # Count intra-section edges
        intra_edges = 0
        for kty_id in selected_ktys:
            for neighbor in kty_adjacency.get(kty_id, set()):
                if neighbor in selected_ktys:
                    intra_edges += 1
        intra_edges //= 2  # undirected
        max_edges = len(selected_ktys) * (len(selected_ktys) - 1) // 2
        if max_edges > 0 and intra_edges > 0:
            density = intra_edges / max_edges
            if density > 0.5 and len(selected_ktys) >= 3:
                diagnostics.append(
                    f"[ADVISORY:HYPERGRAPH] [{section_id}] Likely overloaded section cluster: "
                    f"{len(selected_ktys)} KTYs with {intra_edges}/{max_edges} intra-section edges "
                    f"(density {density:.2f}).  Consider splitting."
                )

    # 2. Omitted supporting KTYs
    omitted: Dict[str, set] = defaultdict(set)
    for kty_id in all_mapped_ktys:
        for neighbor in kty_adjacency.get(kty_id, set()):
            if neighbor not in all_mapped_ktys:
                omitted[neighbor].add(kty_id)
    for unmapped_kty, adjacent_mapped in sorted(omitted.items()):
        if len(adjacent_mapped) >= 2:
            diagnostics.append(
                f"[ADVISORY:HYPERGRAPH] Likely omitted supporting KTY: {unmapped_kty} "
                f"is adjacent to {len(adjacent_mapped)} mapped KTYs "
                f"({', '.join(sorted(adjacent_mapped))}) but is not mapped to any section."
            )

    # 3. Cross-section adjacency hotspots
    hotspot_pairs: List[str] = []
    seen_pairs: set = set()
    for kty_a in all_mapped_ktys:
        for kty_b in kty_adjacency.get(kty_a, set()):
            if kty_b not in all_mapped_ktys:
                continue
            pair_key = tuple(sorted((kty_a, kty_b)))
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)
            sections_a = kty_to_sections.get(kty_a, set())
            sections_b = kty_to_sections.get(kty_b, set())
            if sections_a and sections_b and not sections_a & sections_b:
                hotspot_pairs.append(
                    f"{kty_a} ({', '.join(sorted(sections_a))}) <-> {kty_b} ({', '.join(sorted(sections_b))})"
                )
    if hotspot_pairs:
        diagnostics.append(
            f"[ADVISORY:HYPERGRAPH] Cross-section adjacency hotspots ({len(hotspot_pairs)} pairs): "
            + "; ".join(hotspot_pairs[:10])
            + ("..." if len(hotspot_pairs) > 10 else "")
        )

    return diagnostics


def build_report(
    report_path: Path,
    schema_rows: List[Dict[str, str]],
    csv_rows: List[Dict[str, str]],
    findings: List[str],
    section_stats: Dict[str, Dict[str, object]],
    hypergraph_diagnostics: Optional[List[str]] = None,
) -> None:
    artifact_to_sections: Dict[str, set] = defaultdict(set)
    for row in csv_rows:
        artifact_to_sections[row["ArtifactPath"]].add(row["SectionID"])
    duplicate_artifacts = {
        artifact: sorted(section_ids)
        for artifact, section_ids in artifact_to_sections.items()
        if len(section_ids) > 1
    }
    if duplicate_artifacts:
        findings.extend(
            [
                f"[DUPLICATE] Artifact mapped to multiple sections: {artifact} -> {', '.join(section_ids)}"
                for artifact, section_ids in sorted(duplicate_artifacts.items())
            ]
        )

    total_ka_rows = sum(1 for row in csv_rows if Path(row["ArtifactPath"]).name.startswith("KA-"))
    total_ktys = len({row["KnowledgeTypeID"] for row in csv_rows if row["KnowledgeTypeID"]})
    total_sections = len(schema_rows)

    lines: List[str] = []
    lines.append("# Section Map Coverage Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Sections in schema: {total_sections}")
    lines.append(f"- Candidate mapping rows: {len(csv_rows)}")
    lines.append(f"- Distinct KTYs matched: {total_ktys}")
    lines.append(f"- Candidate KA rows: {total_ka_rows}")
    lines.append(f"- Validation findings: {len(findings)}")
    lines.append("")
    lines.append("## Section Summary")
    lines.append("")
    lines.append("| SectionID | Title | Type | Matched KTYs | KA Rows | EstimatedTokens | SCARefs | OpenIssues | SplitPressure | Total Rows | Findings |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|")
    for section in schema_rows:
        stats = section_stats[section["SectionID"]]
        lines.append(
            "| {sid} | {title} | {stype} | {kty_count} | {ka_count} | {estimated_tokens} | {sca_refs} | {open_issues} | {split_pressure} | {row_count} | {finding_count} |".format(
                sid=section["SectionID"],
                title=section["SectionTitle"].replace("|", "\\|"),
                stype=section["SectionType"],
                kty_count=stats.get("resolved_kty_count", len(stats["selected_ktys"])),
                ka_count=stats["section_ka_count"],
                estimated_tokens=stats.get("estimated_tokens", 0),
                sca_refs=stats.get("sca_ref_count", 0),
                open_issues=stats.get("open_issue_count", 0),
                split_pressure=stats.get("split_pressure", "NO"),
                row_count=stats["section_artifact_count"],
                finding_count=len(stats["findings"]),
            )
        )
    lines.append("")
    lines.append("## Section Sizing Profile")
    lines.append("")
    lines.append("| SectionID | KAFileCount | MaxKAFiles | EstimatedTokens | MaxEstimatedTokens | KTYCount | SCARefCount | OpenIssueCount | LifecycleFindings | SplitPressure | SplitReasons |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for section in schema_rows:
        stats = section_stats[section["SectionID"]]
        lines.append(
            "| {sid} | {ka_count} | {max_ka} | {estimated_tokens} | {max_tokens} | {kty_count} | {sca_refs} | {open_issues} | {lifecycle_findings} | {split_pressure} | {reasons} |".format(
                sid=section["SectionID"],
                ka_count=stats.get("section_ka_count", 0),
                max_ka=stats.get("max_ka_files", ""),
                estimated_tokens=stats.get("estimated_tokens", 0),
                max_tokens=stats.get("max_estimated_tokens", "") or "—",
                kty_count=stats.get("resolved_kty_count", len(stats.get("selected_ktys", []))),
                sca_refs=stats.get("sca_ref_count", 0),
                open_issues=stats.get("open_issue_count", 0),
                lifecycle_findings=stats.get("lifecycle_findings", 0),
                split_pressure=stats.get("split_pressure", "NO"),
                reasons=", ".join(stats.get("split_pressure_reasons", [])) or "—",
            )
        )
    lines.append("")
    lines.append("## Selector Rules")
    lines.append("")
    for section in schema_rows:
        stats = section_stats[section["SectionID"]]
        lines.append(f"### {section['SectionID']} — {section['SectionTitle']}")
        lines.append("")
        lines.append(f"- IncludeCategoryIDs: {section.get('IncludeCategoryIDs') or '—'}")
        lines.append(f"- IncludeKnowledgeTypeIDs: {section.get('IncludeKnowledgeTypeIDs') or '—'}")
        lines.append(f"- IncludeCanonicalSchemas: {section.get('IncludeCanonicalSchemas') or '—'}")
        lines.append(f"- ExcludeCategoryIDs: {section.get('ExcludeCategoryIDs') or '—'}")
        lines.append(f"- ExcludeKnowledgeTypeIDs: {section.get('ExcludeKnowledgeTypeIDs') or '—'}")
        lines.append(f"- InclusionRule (ignored by tool): {section.get('InclusionRule') or '—'}")
        lines.append(f"- ExclusionRule (ignored by tool): {section.get('ExclusionRule') or '—'}")
        lines.append(f"- Matched KTY IDs: {', '.join(stats['selected_ktys']) or '—'}")
        if stats["findings"]:
            lines.append("- Findings:")
            for finding in stats["findings"]:
                lines.append(f"  - {finding}")
        else:
            lines.append("- Findings: none")
        lines.append("")

    lines.append("## Duplicate Artifact Rows Across Sections")
    lines.append("")
    if duplicate_artifacts:
        for artifact, section_ids in sorted(duplicate_artifacts.items()):
            lines.append(f"- `{artifact}` -> {', '.join(section_ids)}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Validation Findings")
    lines.append("")
    if findings:
        for finding in sorted(findings):
            lines.append(f"- {finding}")
    else:
        lines.append("- None")
    lines.append("")

    # --- Advisory hypergraph diagnostics (AUXILIARY_STRUCTURE_EVIDENCE) ----
    # These diagnostics are advisory only and remain non-authoritative until
    # the human approves the final section map.
    if hypergraph_diagnostics is not None:
        lines.append("## Hypergraph Advisory Diagnostics (AUXILIARY_STRUCTURE_EVIDENCE)")
        lines.append("")
        if hypergraph_diagnostics:
            for diag in hypergraph_diagnostics:
                lines.append(f"- {diag}")
        else:
            lines.append("- No advisory diagnostics from hypergraph evidence.")
        lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate candidate Section_Map.csv from Publication_Schema.md selectors.")
    parser.add_argument("--schema", required=True, help="Path to Publication_Schema.md")
    parser.add_argument("--manifest", required=True, help="Path to Publication_Input_Manifest.md")
    parser.add_argument("--output-csv", required=False, help="Output path for candidate Section_Map.csv")
    parser.add_argument("--report-md", required=True, help="Output path for mapping coverage report markdown")
    parser.add_argument("--dry-run", action="store_true", help="Gate 3 governed sizing mode; write report only")
    args = parser.parse_args()

    schema_path = Path(args.schema).resolve()
    manifest_path = Path(args.manifest).resolve()
    output_csv = Path(args.output_csv).resolve() if args.output_csv else None
    report_md = Path(args.report_md).resolve()
    if not args.dry_run and output_csv is None:
        fatal("--output-csv is required unless --dry-run is set")

    schema_rows = parse_schema(schema_path)
    manifest = parse_manifest(manifest_path)
    execution_root = manifest["execution_root"]
    publication_root = manifest["publication_root"]
    if not isinstance(execution_root, Path):
        fatal("Execution root could not be resolved from manifest.")
    if not isinstance(publication_root, Path):
        fatal("Publication root could not be resolved from manifest.")
    if not execution_root.exists():
        fatal(f"Execution root does not exist: {execution_root}")
    if output_csv is not None:
        require_within(output_csv, publication_root, "--output-csv")
    require_within(report_md, publication_root, "--report-md")

    classified = classify_manifest_csvs(manifest["decomposition_files"])
    categories = load_categories(classified["category_register"])
    ktys = load_ktys(classified["kty_register"])
    subjects = load_subjects(classified["subject_register"])
    ledger_index = load_ledger_index(classified["ledger"])
    kty_to_sca, subject_to_sca, current_state_basis = load_active_sca_refs(manifest, ledger_index)
    sca_lifecycle_states = load_sca_lifecycle_states(manifest)
    open_issue_rows = read_csv_rows(classified["open_issues"]) if "open_issues" in classified else []

    csv_rows, findings, section_stats = build_candidate_rows(
        schema_rows=schema_rows,
        execution_root=execution_root,
        categories=categories,
        ktys=ktys,
        subjects=subjects,
        ledger_index=ledger_index,
        kty_to_sca=kty_to_sca,
        subject_to_sca=subject_to_sca,
        sca_lifecycle_states=sca_lifecycle_states,
        open_issue_rows=open_issue_rows,
        current_state_basis=current_state_basis,
    )

    # ------------------------------------------------------------------
    # Optional hypergraph-assisted advisory diagnostics
    # (AUXILIARY_STRUCTURE_EVIDENCE — see plan Phase 2, Tool 3).
    #
    # When the manifest admits a hypergraph snapshot for planning, emit
    # advisory diagnostics covering:
    #   - likely overloaded section clusters
    #   - likely omitted supporting KTYs
    #   - likely cross-section adjacency hotspots
    #
    # These diagnostics remain advisory until the human approves the
    # final section map.  They do NOT modify the deterministic
    # selector-based mapping.
    # ------------------------------------------------------------------
    hg_fields = _read_hypergraph_manifest_fields(manifest)
    hypergraph_diagnostics: Optional[List[str]] = None
    if _hypergraph_planning_allowed(hg_fields):
        hg_evidence = _load_hypergraph_evidence_for_diagnostics(hg_fields, manifest_path.parent)
        if hg_evidence.get("hyperedges"):
            hypergraph_diagnostics = build_hypergraph_advisory_diagnostics(
                hg_evidence, csv_rows, section_stats,
            )

    if output_csv is not None:
        write_csv(output_csv, SECTION_MAP_COLUMNS, csv_rows)
    build_report(report_md, schema_rows, csv_rows, findings, section_stats, hypergraph_diagnostics)

    if output_csv is not None:
        print(f"Wrote candidate section map: {output_csv}")
    else:
        print("Dry run: no candidate section map written")
    print(f"Wrote coverage report: {report_md}")
    print(f"Rows: {len(csv_rows)}")
    if hypergraph_diagnostics:
        print(f"Hypergraph advisory diagnostics: {len(hypergraph_diagnostics)}")
    if findings:
        print(f"Validation findings: {len(findings)}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
