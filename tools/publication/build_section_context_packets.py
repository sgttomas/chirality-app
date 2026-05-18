#!/usr/bin/env python3
"""
build_section_context_packets.py - Deterministic section context packet builder.

Purpose:
  Generate one read-only structural context packet per approved DBM
  publication section. Packets summarize decomposition/register context that
  helps section workers frame, complete, and QA their work. The packets are
  not body-authoring authority and perform no semantic classification.

Inputs:
  --manifest                Frozen Publication_Input_Manifest.md
  --schema                  Approved Publication_Schema.md
  --section-map             Approved Section_Map.csv
  [--concordance-register]  (LEGACY — accepted but ignored; concordance moved to post-authoring)
  [--risk-inventory]        (LEGACY — accepted but ignored; concordance moved to post-authoring)
  [--supersession-map]      Frozen cumulative Supersession_Map.csv
  [--open-issues]           Open_Issues_Register.csv
  [--hypergraph-use-mode]   NONE | AUXILIARY_PLANNING | AUXILIARY_QA |
                            AUXILIARY_PLANNING_AND_QA
  --output-dir              _Publication/DBM/_Planning/section-context/

Writes:
  SEC-##_Context.md files under --output-dir only.

Exit codes:
  0 = all packets generated without context warnings
  1 = fatal input / parsing error
  2 = packets generated, but some optional context could not be populated

Scope boundary:
  Reads only frozen publication planning artifacts and exact files named in
  the frozen manifest / CLI arguments. Writes only under --output-dir.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import (  # type: ignore
    parse_list_cell,
    parse_manifest,
    parse_schema,
    read_csv_rows,
    require_within,
)


ALLOWED_HYPERGRAPH_MODES = {
    "NONE",
    "AUXILIARY_PLANNING",
    "AUXILIARY_QA",
    "AUXILIARY_PLANNING_AND_QA",
}


def fatal(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def first_value(row: Dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key, "")
        if value:
            return value
    return ""


def split_ids(value: str) -> List[str]:
    parts = parse_list_cell(value)
    if parts:
        return parts
    return [token for token in re.findall(r"\b(?:KTY|SUB|OBJ|CAT|SEC)-[A-Za-z0-9_-]+\b", value or "")]


def stable_rows(rows: Iterable[Dict[str, str]], *keys: str) -> List[Dict[str, str]]:
    return sorted(rows, key=lambda row: tuple(row.get(key, "") for key in keys) or tuple(sorted(row.items())))


def table(lines: List[str], headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    if rows:
        for row in rows:
            padded = list(row[: len(headers)]) + [""] * max(0, len(headers) - len(row))
            lines.append("| " + " | ".join(md_escape(value) for value in padded) + " |")
    else:
        lines.append("| " + " | ".join("None" if idx == 0 else "" for idx, _ in enumerate(headers)) + " |")


def detect_csv(path: Path) -> str:
    if not path.exists() or path.suffix.lower() != ".csv":
        return ""
    try:
        rows = read_csv_rows(path)
    except SystemExit:
        return ""
    if not rows:
        return ""
    columns = set(rows[0].keys())
    name = path.name.lower()
    if {"KnowledgeTypeID", "ParentCategoryID"}.issubset(columns):
        return "kty_register"
    if {"SubjectID", "ParentKnowledgeTypeID"}.issubset(columns):
        return "subject_register"
    if "CategoryID" in columns and ("ScopeDescription" in columns or "BoundaryRule" in columns or "CategoryName" in columns or "Name" in columns):
        return "category_register"
    if "CanonicalTerm" in columns or "PreferredTerm" in columns:
        return "vocabulary_map"
    if "OpenIssueID" in columns or ("OpenIssueType" in columns and "Status" in columns):
        return "open_issues"
    if "KTYID" in columns and ("FACTUAL_USE_GATE" in columns or "CONTENT_DISPOSITION_STATE" in columns):
        return "remediation_manifest"
    if {"UnitID", "CategoryID"}.issubset(columns) and any(column.startswith("KnowledgeTypeID") for column in columns):
        return "ledger"
    if "ObjectiveID" in columns or name.find("objective") >= 0:
        return "objective_register"
    return ""


def resolve_optional_path(raw: str, base_dir: Path) -> Optional[Path]:
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path if path.exists() else None


def classify_manifest_paths(manifest: Dict[str, object]) -> Dict[str, Path]:
    classified: Dict[str, Path] = {}
    all_paths: Sequence[Path] = list(manifest.get("all_paths", []))  # type: ignore[arg-type]
    for path in sorted(all_paths, key=lambda item: str(item)):
        kind = detect_csv(path)
        if kind:
            classified.setdefault(kind, path)
    return classified


def load_rows(path: Optional[Path]) -> List[Dict[str, str]]:
    if not path:
        return []
    return read_csv_rows(path) if path.exists() else []


def index_by(rows: Sequence[Dict[str, str]], key: str) -> Dict[str, Dict[str, str]]:
    indexed: Dict[str, Dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if value:
            indexed[value] = row
    return indexed


def section_map_by_section(rows: Sequence[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        section_id = row.get("SectionID", "")
        if section_id:
            grouped[section_id].append(row)
    return grouped


def subjects_by_kty(rows: Sequence[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        kty_id = row.get("ParentKnowledgeTypeID", "")
        if kty_id:
            grouped[kty_id].append(row)
    return grouped


def kty_name(row: Dict[str, str], fallback: str) -> str:
    return first_value(row, "KnowledgeTypeName", "KTYName", "Name", "Title") or fallback


def category_name(row: Dict[str, str], fallback: str) -> str:
    return first_value(row, "CategoryName", "Name", "Title", "Category") or fallback


def objective_id(row: Dict[str, str]) -> str:
    return first_value(row, "ObjectiveID", "ID", "ObjectiveId")


def objective_statement(row: Dict[str, str]) -> str:
    return first_value(row, "Statement", "ObjectiveStatement", "Description", "Name", "ObjectiveName", "Title")


def extract_objective_ids(row: Dict[str, str]) -> List[str]:
    values: List[str] = []
    for key, value in row.items():
        if "objective" in key.lower() and value:
            values.extend(split_ids(value))
    blob = " ".join(row.values())
    values.extend(re.findall(r"\bOBJ-[A-Za-z0-9_-]+\b", blob))
    seen = set()
    ordered: List[str] = []
    for value in values:
        if value and value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def build_kty_objective_index(
    kty_rows: Sequence[Dict[str, str]],
    ledger_rows: Sequence[Dict[str, str]],
) -> Dict[str, List[str]]:
    by_kty: Dict[str, List[str]] = defaultdict(list)
    seen: Dict[str, set] = defaultdict(set)

    def add(kty_id: str, obj_id: str) -> None:
        if kty_id and obj_id and obj_id not in seen[kty_id]:
            by_kty[kty_id].append(obj_id)
            seen[kty_id].add(obj_id)

    for row in kty_rows:
        kty_id = row.get("KnowledgeTypeID", "")
        for obj in extract_objective_ids(row):
            add(kty_id, obj)

    for row in ledger_rows:
        kty_ids = split_ids(first_value(row, "KnowledgeTypeID", "KnowledgeTypeID(s)", "KTYID"))
        objectives = extract_objective_ids(row)
        for kty_id in kty_ids:
            for obj in objectives:
                add(kty_id, obj)
    return by_kty


def row_matches_entities(row: Dict[str, str], entities: Sequence[str]) -> bool:
    blob = " ".join(row.values())
    return any(entity and entity in blob for entity in entities)


def row_applies_to_section(row: Dict[str, str], section_id: str, entities: Sequence[str]) -> bool:
    applies = first_value(row, "AppliesToSections", "RequiredSectionIDs", "SectionIDs", "SectionID")
    if applies and section_id in split_ids(applies):
        return True
    if row_matches_entities(row, entities):
        return True
    return False


def concordance_keys_for_section(register_rows: Sequence[Dict[str, str]], section_id: str) -> Tuple[List[str], List[str]]:
    authority: List[str] = []
    required: List[str] = []
    for row in register_rows:
        key = row.get("AssertionKey", "")
        if not key:
            continue
        if row.get("AuthoritySectionID", "") == section_id:
            authority.append(key)
        required_ids = split_ids(row.get("RequiredSectionIDs", ""))
        if section_id in required_ids:
            required.append(key)
    return sorted(set(authority)), sorted(set(required))


def relevant_vocabulary_rows(
    rows: Sequence[Dict[str, str]],
    entities: Sequence[str],
    context_blob: str,
) -> List[Dict[str, str]]:
    relevant: List[Dict[str, str]] = []
    context_upper = context_blob.upper()
    for row in rows:
        blob = " ".join(row.values())
        term = first_value(row, "CanonicalTerm", "PreferredTerm", "Term")
        if row_matches_entities(row, entities) or (term and term.upper() in context_upper):
            relevant.append(row)
    return stable_rows(relevant, "CanonicalTerm", "PreferredTerm", "Term")


def build_packet(
    section: Dict[str, str],
    section_rows: Sequence[Dict[str, str]],
    categories: Dict[str, Dict[str, str]],
    ktys: Dict[str, Dict[str, str]],
    subjects_index: Dict[str, List[Dict[str, str]]],
    objectives: Dict[str, Dict[str, str]],
    kty_objectives: Dict[str, List[str]],
    supersession_rows: Sequence[Dict[str, str]],
    open_issue_rows: Sequence[Dict[str, str]],
    remediation_rows: Sequence[Dict[str, str]],
    vocabulary_rows: Sequence[Dict[str, str]],
    warnings: List[str],
) -> str:
    section_id = section["SectionID"]
    mapped_ktys = sorted({row.get("KnowledgeTypeID", "") for row in section_rows if row.get("KnowledgeTypeID", "")})
    mapped_subjects = sorted({row.get("SubjectID", "") for row in section_rows if row.get("SubjectID", "")})
    mapped_categories = sorted({row.get("CategoryID", "") for row in section_rows if row.get("CategoryID", "")})
    entities = [section_id, *mapped_ktys, *mapped_subjects, *mapped_categories]

    context_blob_parts: List[str] = []
    for kty_id in mapped_ktys:
        kty = ktys.get(kty_id, {})
        context_blob_parts.extend([kty_id, kty_name(kty, kty_id), first_value(kty, "Description", "ScopeDescription", "WhenUsed")])
    context_blob = " ".join(context_blob_parts)

    lines = [
        f"# Section Context - {section_id}: {section.get('SectionTitle', '')}",
        "",
        "> Deterministic structural context packet. Use for framing, completeness checks, and QA. This packet is not a substitute for mapped KA content as body-authoring authority.",
        "",
        "## Mapped KTYs and Subjects",
        "",
    ]

    kty_rows_out: List[List[str]] = []
    for kty_id in mapped_ktys:
        kty = ktys.get(kty_id, {})
        cat_id = first_value(kty, "ParentCategoryID", "CategoryID") or next((row.get("CategoryID", "") for row in section_rows if row.get("KnowledgeTypeID", "") == kty_id), "")
        cat = categories.get(cat_id, {})
        roles = sorted({row.get("MappingRole", "") for row in section_rows if row.get("KnowledgeTypeID", "") == kty_id and row.get("MappingRole", "")})
        ka_count = sum(1 for row in section_rows if row.get("KnowledgeTypeID", "") == kty_id and Path(row.get("ArtifactPath", "")).name.startswith("KA-"))
        kty_rows_out.append(
            [
                kty_id,
                kty_name(kty, kty_id),
                cat_id,
                category_name(cat, cat_id),
                "; ".join(roles),
                str(len(subjects_index.get(kty_id, []))),
                str(ka_count),
            ]
        )
    table(lines, ["KTYId", "KTYName", "CategoryID", "CategoryName", "MappingRole", "SubjectCount", "KAFileCount"], kty_rows_out)

    lines.extend(["", "## Objectives Served", ""])
    objective_rows: List[List[str]] = []
    for obj_id in sorted({obj_id for kty_id in mapped_ktys for obj_id in kty_objectives.get(kty_id, [])}):
        supporting = sorted(kty_id for kty_id in mapped_ktys if obj_id in kty_objectives.get(kty_id, []))
        obj = objectives.get(obj_id, {})
        objective_rows.append([obj_id, objective_statement(obj) or obj_id, "; ".join(supporting)])
    if not objective_rows:
        warnings.append(f"{section_id}: no objective context found for mapped KTYs.")
    table(lines, ["ObjectiveID", "Statement", "KTYs Supporting"], objective_rows)

    lines.extend(["", "## Category and KTY Descriptions", ""])
    if mapped_ktys:
        for kty_id in mapped_ktys:
            kty = ktys.get(kty_id, {})
            cat_id = first_value(kty, "ParentCategoryID", "CategoryID")
            cat = categories.get(cat_id, {})
            description = first_value(kty, "Description", "ScopeDescription", "WhenUsed", "Purpose") or "No register description available."
            lines.append(f"- **{kty_id} - {md_escape(kty_name(kty, kty_id))}** ({md_escape(category_name(cat, cat_id))}): {md_escape(description)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Applicable Supersession Bindings", ""])
    supersession_out: List[List[str]] = []
    for row in supersession_rows:
        if row_applies_to_section(row, section_id, entities):
            supersession_out.append(
                [
                    first_value(row, "SupersededFactKey", "FactKey", "AssertionKey"),
                    first_value(row, "OverrideType", "SupersessionType"),
                    first_value(row, "ReplacementValue", "NewValue", "CurrentValue"),
                    first_value(row, "AmendmentID", "SCAID", "SCA_ID"),
                    first_value(row, "AppliesToSections", "SectionID", "SectionIDs"),
                ]
            )
    table(lines, ["SupersededFactKey", "OverrideType", "ReplacementValue", "AmendmentID", "AppliesToSections"], supersession_out)

    lines.extend(["", "## Open Issues Affecting This Section", ""])
    open_out: List[List[str]] = []
    for row in open_issue_rows:
        if row_applies_to_section(row, section_id, entities):
            open_out.append(
                [
                    first_value(row, "OpenIssueID", "IssueID", "ID"),
                    first_value(row, "OpenIssueType", "IssueType", "Type"),
                    first_value(row, "AffectedEntityID", "EntityID", "AffectedEntities", "AffectedEntity"),
                    first_value(row, "Summary", "Description", "Issue", "Title"),
                ]
            )
    table(lines, ["IssueID", "IssueType", "AffectedEntityID", "Summary"], open_out)

    lines.extend(["", "## Factual-Use Eligibility", ""])
    remediation_by_kty = {
        first_value(row, "KTYID", "KnowledgeTypeID", "EntityID"): row
        for row in remediation_rows
        if first_value(row, "KTYID", "KnowledgeTypeID", "EntityID")
    }
    eligibility_rows: List[List[str]] = []
    for kty_id in mapped_ktys:
        row = remediation_by_kty.get(kty_id, {})
        eligibility_rows.append(
            [
                kty_id,
                first_value(row, "FACTUAL_USE_GATE", "FactualUseGate") or "NOT_REPORTED",
                first_value(row, "CONTENT_DISPOSITION_STATE", "ContentDispositionState", "ContentRemediationState") or "NOT_REPORTED",
                first_value(row, "Notes", "Rationale", "Reason"),
            ]
        )
    if not remediation_rows:
        warnings.append(f"{section_id}: no KTY remediation manifest context found.")
    table(lines, ["KTYID", "FACTUAL_USE_GATE", "CONTENT_DISPOSITION_STATE", "Notes"], eligibility_rows)

    lines.extend(["", "## Vocabulary Terms", ""])
    vocab_out: List[List[str]] = []
    for row in relevant_vocabulary_rows(vocabulary_rows, entities, context_blob):
        vocab_out.append(
            [
                first_value(row, "CanonicalTerm", "PreferredTerm", "Term"),
                first_value(row, "Synonyms", "Aliases", "Alias"),
            ]
        )
    table(lines, ["CanonicalTerm", "Synonyms"], vocab_out)

    primary = sorted({row.get("KnowledgeTypeID", "") for row in section_rows if row.get("MappingRole", "") == "PRIMARY"})
    supporting = sorted({row.get("KnowledgeTypeID", "") for row in section_rows if row.get("MappingRole", "") == "SUPPORTING"})
    context_only = sorted({row.get("KnowledgeTypeID", "") for row in section_rows if row.get("MappingRole", "") == "CONTEXT_ONLY"})
    lines.extend(
        [
            "",
            "## Section-Map Role Expectations",
            "",
            f"- Section type: {section.get('SectionType', '')}",
            f"- Section purpose: {section.get('SectionPurpose', '')}",
            f"- Expected output shape: {section.get('ExpectedOutputShape', '')}",
            f"- PRIMARY KTYs: {', '.join(primary) if primary else 'None'}",
            f"- SUPPORTING KTYs: {', '.join(supporting) if supporting else 'None'}",
            f"- CONTEXT_ONLY KTYs: {', '.join(context_only) if context_only else 'None'}",
        ]
    )

    lines.append("")
    return "\n".join(lines)


def generate_packets(
    manifest_path: Path,
    schema_path: Path,
    section_map_path: Path,
    concordance_register_path: Optional[Path] = None,
    risk_inventory_path: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    supersession_map_path: Optional[Path] = None,
    open_issues_path: Optional[Path] = None,
    hypergraph_use_mode: str = "NONE",
) -> Tuple[List[Path], List[str]]:
    if hypergraph_use_mode.upper() not in ALLOWED_HYPERGRAPH_MODES:
        fatal(f"Unsupported hypergraph use mode: {hypergraph_use_mode}")
    for path in [manifest_path, schema_path, section_map_path]:
        if not path.exists():
            fatal(f"Required input does not exist: {path}")

    manifest = parse_manifest(manifest_path)
    publication_root = manifest.get("publication_root")
    if not isinstance(publication_root, Path):
        fatal("Publication root could not be resolved from manifest.")
    require_within(output_dir, publication_root, "--output-dir")

    classified = classify_manifest_paths(manifest)
    if supersession_map_path is None:
        explicit = manifest.get("explicit", {})
        if isinstance(explicit, dict):
            supersession_map_path = resolve_optional_path(explicit.get("SUPERSESSION_MAP_PATH", ""), manifest_path.parent)
    if open_issues_path is None:
        open_issues_path = classified.get("open_issues")

    warnings: List[str] = []
    for required_kind in ["category_register", "kty_register", "subject_register"]:
        if required_kind not in classified:
            warnings.append(f"Manifest did not expose {required_kind}.")
    if "objective_register" not in classified:
        warnings.append("Manifest did not expose objective_register.")
    if "ledger" not in classified:
        warnings.append("Manifest did not expose ledger.")
    if "vocabulary_map" not in classified:
        warnings.append("Manifest did not expose vocabulary_map.")
    if "remediation_manifest" not in classified:
        warnings.append("Manifest did not expose remediation_manifest.")
    if open_issues_path is None:
        warnings.append("No open issues register provided or discovered.")

    schema_rows = parse_schema(schema_path)
    section_map_rows = read_csv_rows(section_map_path)
    category_rows = load_rows(classified.get("category_register"))
    kty_rows = load_rows(classified.get("kty_register"))
    subject_rows = load_rows(classified.get("subject_register"))
    objective_rows = load_rows(classified.get("objective_register"))
    ledger_rows = load_rows(classified.get("ledger"))
    vocabulary_rows = load_rows(classified.get("vocabulary_map"))
    remediation_rows = load_rows(classified.get("remediation_manifest"))
    open_issue_rows = load_rows(open_issues_path)
    supersession_rows = load_rows(supersession_map_path)

    categories = index_by(category_rows, "CategoryID")
    ktys = index_by(kty_rows, "KnowledgeTypeID")
    subjects = subjects_by_kty(subject_rows)
    objectives = {objective_id(row): row for row in objective_rows if objective_id(row)}
    kty_objectives = build_kty_objective_index(kty_rows, ledger_rows)
    by_section = section_map_by_section(section_map_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    for section in schema_rows:
        section_id = section["SectionID"]
        packet = build_packet(
            section=section,
            section_rows=by_section.get(section_id, []),
            categories=categories,
            ktys=ktys,
            subjects_index=subjects,
            objectives=objectives,
            kty_objectives=kty_objectives,
            supersession_rows=supersession_rows,
            open_issue_rows=open_issue_rows,
            remediation_rows=remediation_rows,
            vocabulary_rows=vocabulary_rows,
            warnings=warnings,
        )
        packet_path = output_dir / f"{section_id}_Context.md"
        packet_path.write_text(packet, encoding="utf-8")
        written.append(packet_path)
    return written, sorted(set(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic DBM section context packets.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--concordance-register", default="", help="LEGACY — accepted but ignored")
    parser.add_argument("--risk-inventory", default="", help="LEGACY — accepted but ignored")
    parser.add_argument("--supersession-map", default="")
    parser.add_argument("--open-issues", default="")
    parser.add_argument("--hypergraph-use-mode", default="NONE")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    written, warnings = generate_packets(
        manifest_path=Path(args.manifest).resolve(),
        schema_path=Path(args.schema).resolve(),
        section_map_path=Path(args.section_map).resolve(),
        output_dir=Path(args.output_dir).resolve(),
        supersession_map_path=Path(args.supersession_map).resolve() if args.supersession_map else None,
        open_issues_path=Path(args.open_issues).resolve() if args.open_issues else None,
        hypergraph_use_mode=args.hypergraph_use_mode,
    )
    print(f"Wrote section context packets: {len(written)}")
    for path in written:
        print(f"- {path}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
