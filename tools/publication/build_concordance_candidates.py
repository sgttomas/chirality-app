#!/usr/bin/env python3
"""
build_concordance_candidates.py — ARCHIVED typed concordance candidate builder for DBM publication.

Deprecated:
  Superseded for active DBM_PUBLISHER runs by
  tools/publication/extract_concordance_evidence.py. This file remains in
  place so old publication run documentation that references it stays
  readable. New runs must use evidence atoms + dbm-concordance-seed instead
  of this heuristic candidate builder.

Purpose:
  Read the frozen publication planning artifacts, harvest concordance candidates
  from structured publication inputs, and write an agent-seedable candidate set
  plus a coverage summary before the blocking concordance register is frozen.

Inputs:
  --manifest     Frozen Publication_Input_Manifest.md
  --schema       Approved Publication_Schema.md
  --section-map  Approved Section_Map.csv
  --output-csv   Publication_Concordance_Candidates.csv
  --coverage-md  Publication_Concordance_Coverage.md

Writes:
  - Publication_Concordance_Candidates.csv
  - Publication_Concordance_Coverage.md

Optional hypergraph inputs (AUXILIARY_STRUCTURE_EVIDENCE):
  When the frozen manifest admits a hypergraph snapshot with a planning-
  compatible use mode (AUXILIARY_PLANNING or AUXILIARY_PLANNING_AND_QA),
  the tool reads nodes, hyperedges, and evidence CSVs to suggest additional
  concordance candidates tagged DiscoverySource = HYPERGRAPH_AUXILIARY.
  Hypergraph evidence must NOT generate canonical assertion values from
  graph topology or override candidates already grounded in mapped source
  content.  The tool works identically when no hypergraph inputs are present.

Scope boundary:
  Reads: manifest, schema, section map, mapped KA markdown, open-issues CSVs,
  decision-log CSVs, active SCA amendment CSVs named by the manifest, and
  optionally admitted hypergraph evidence files
  Writes: only --output-csv and --coverage-md
  Does not mutate section outputs, package snapshots, or KTY-local truth

Exit codes:
  0 = success
  1 = fatal input / parsing error
  2 = outputs written, but coverage gaps or unresolved candidate issues remain

Example:
  python3 tools/publication/build_concordance_candidates.py \
    --manifest /repo/.../_Planning/Publication_Input_Manifest.md \
    --schema /repo/.../_Planning/Publication_Schema.md \
    --section-map /repo/.../_Planning/Section_Map.csv \
    --output-csv /repo/.../_Planning/Publication_Concordance_Candidates.csv \
    --coverage-md /repo/.../_Planning/Publication_Concordance_Coverage.md
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import (  # type: ignore
    classify_manifest_csvs,
    parse_list_cell,
    parse_manifest,
    parse_schema,
    read_csv_rows,
    write_csv,
)

CANDIDATE_COLUMNS = [
    "AssertionKey",
    "AssertionLabel",
    "AssertionDomain",
    "AssertionType",
    "CanonicalTerm",
    "Unit",
    "ComparisonRule",
    "ComparisonParameter",
    "AuthoritySectionID",
    "RequiredSectionIDs",
    "FacilityScope",
    "CurrentStateBasis",
    "DecisionRefs",
    "DiscoverySource",
    "SourceKTYIDs",
    "SourceSectionIDs",
    "NormalizationHint",
    "Criticality",
    "CandidateValueExample",
    "SourceArtifact",
    "SourceRef",
    "Notes",
    "ResolutionStatus",
]

ALLOWED_ASSERTION_DOMAINS = {
    "PROCESS_CONDITION",
    "UTILITY_CONDITION",
    "PRODUCT_SPEC",
    "EQUIPMENT_LIMIT",
    "OPERATING_TARGET",
    "SCOPE_STATE",
    "LOCATION_STATE",
    "REGULATORY_STATE",
    "CONTROL_LOGIC",
}

ALLOWED_DISCOVERY_SOURCES = {
    "STRUCTURED_TABLE",
    "METADATA_FIELD",
    "PROSE_EXTRACTION",
    "OPEN_ISSUE",
    "DECISION_LOG",
    "SCOPE_CHANGE",
    "HUMAN_ADDED",
    "SECTION_DISCOVERY",
    "HYPERGRAPH_AUXILIARY",
}

# ---------------------------------------------------------------------------
# Hypergraph use-mode constants.
#
# Hypergraph evidence is AUXILIARY ONLY.  It must never generate canonical
# assertion values from graph topology or override candidates already
# grounded in mapped source content.  See the plan section
# "Core Policy / Hypergraphs become auxiliary structure evidence".
# ---------------------------------------------------------------------------
HYPERGRAPH_PLANNING_MODES = {
    "AUXILIARY_PLANNING",
    "AUXILIARY_PLANNING_AND_QA",
}

ALLOWED_CRITICALITY = {"HIGH", "NORMAL", "LOW"}
ALLOWED_RESOLUTION_STATUS = {"READY_FOR_FREEZE", "NEEDS_REVIEW", "DUPLICATE_CANDIDATE", "OUT_OF_SCOPE"}

IGNORED_ARTIFACT_NAMES = {"Scoping.md", "_STATUS.md", "_CONTEXT.md", "_REFERENCES.md", "_DEPENDENCIES.md"}
GENERIC_VALUE_HEADERS = {"VALUE", "DESIGN", "LOW", "HIGH", "MIN", "MAX", "CASE", "STATUS"}
SECTION_TYPE_AUTHORITY_PREFERENCE = {
    "PROCESS_CONDITION": ["DATA_REFERENCE", "PROCESS_BASIS", "DISCIPLINE_BASIS", "OVERVIEW", "PHILOSOPHY", "REGULATORY"],
    "UTILITY_CONDITION": ["DATA_REFERENCE", "DISCIPLINE_BASIS", "PROCESS_BASIS", "OVERVIEW", "PHILOSOPHY", "REGULATORY"],
    "PRODUCT_SPEC": ["DATA_REFERENCE", "PROCESS_BASIS", "OVERVIEW", "DISCIPLINE_BASIS", "PHILOSOPHY", "REGULATORY"],
    "EQUIPMENT_LIMIT": ["DATA_REFERENCE", "DISCIPLINE_BASIS", "PROCESS_BASIS", "OVERVIEW", "PHILOSOPHY", "REGULATORY"],
    "OPERATING_TARGET": ["DATA_REFERENCE", "PROCESS_BASIS", "DISCIPLINE_BASIS", "OVERVIEW", "PHILOSOPHY", "REGULATORY"],
    "SCOPE_STATE": ["OVERVIEW", "REGULATORY", "PHILOSOPHY", "PROCESS_BASIS", "DISCIPLINE_BASIS", "DATA_REFERENCE"],
    "LOCATION_STATE": ["OVERVIEW", "PROCESS_BASIS", "DISCIPLINE_BASIS", "DATA_REFERENCE", "REGULATORY", "PHILOSOPHY"],
    "REGULATORY_STATE": ["REGULATORY", "OVERVIEW", "PHILOSOPHY", "PROCESS_BASIS", "DISCIPLINE_BASIS", "DATA_REFERENCE"],
    "CONTROL_LOGIC": ["PHILOSOPHY", "PROCESS_BASIS", "DISCIPLINE_BASIS", "DATA_REFERENCE", "OVERVIEW", "REGULATORY"],
}


@dataclass
class TableBlock:
    heading_path: Tuple[str, ...]
    caption: str
    rows: List[Dict[str, str]]


def fatal(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def require_within(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fatal(f"{label} must resolve under publication root {root}: {path}")


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def normalize_key_token(value: str) -> str:
    tokens = re.findall(r"[A-Z0-9]+", value.upper().replace("°", " DEG "))
    return "_".join(tokens)


def canonicalize_label(value: str) -> str:
    value = normalize_space(value)
    value = value.replace("**", "").replace("*", "").replace("`", "")
    value = value.strip(" -*_")
    value = re.sub(r"\s*\(Source:.*?\)\s*$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^Table\s+[A-Za-z0-9.-]+:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^#+\s*", "", value)
    return normalize_space(value)


def dedupe_preserve_order(values: Iterable[str]) -> List[str]:
    result: List[str] = []
    seen = set()
    for value in values:
        item = normalize_space(value)
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def first_nonempty(*values: str) -> str:
    for value in values:
        if normalize_space(value):
            return normalize_space(value)
    return ""


def parse_markdown_tables_with_context(text: str) -> List[TableBlock]:
    headings: List[str] = []
    blocks: List[TableBlock] = []
    current_table_lines: List[str] = []
    recent_nonempty: List[str] = []

    def flush_table() -> None:
        nonlocal current_table_lines
        if not current_table_lines:
            return
        rows = _parse_table_block(current_table_lines)
        if rows:
            caption = ""
            for line in reversed(recent_nonempty):
                cleaned = line.strip()
                if cleaned.startswith("|"):
                    continue
                if cleaned.startswith("*Table") or cleaned.startswith("Table ") or cleaned.startswith("*") or cleaned.startswith(">"):
                    caption = cleaned.strip("*").strip()
                    break
            blocks.append(TableBlock(tuple(headings), canonicalize_label(caption), rows))
        current_table_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if heading_match:
            flush_table()
            level = len(heading_match.group(1))
            title = canonicalize_label(heading_match.group(2))
            while len(headings) >= level:
                headings.pop()
            headings.append(title)
            recent_nonempty.append(line.strip())
            recent_nonempty = recent_nonempty[-5:]
            continue
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current_table_lines.append(line)
            continue
        flush_table()
        if stripped:
            recent_nonempty.append(stripped)
            recent_nonempty = recent_nonempty[-5:]
    flush_table()
    return blocks


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


def parse_section_map(path: Path) -> List[Dict[str, str]]:
    rows = read_csv_rows(path)
    required = {"SectionID", "SectionTitle", "SectionType", "ArtifactPath", "KnowledgeTypeID", "DecisionRefs", "SCARefs", "CurrentStateBasis"}
    if rows and not required.issubset(set(rows[0].keys())):
        missing = sorted(required - set(rows[0].keys()))
        fatal(f"Section map missing required columns: {', '.join(missing)}")
    return rows


def extract_unit(*values: str) -> str:
    text = " ".join(value for value in values if value)
    paren_matches = re.findall(r"\(([^()]{1,40})\)", text)
    for match in reversed(paren_matches):
        if re.search(r"[A-Za-z%°/]", match):
            return normalize_space(match)
    unit_match = re.search(r"\b(ppmv|ppmw(?:\s+as\s+S)?|wt%|mol%|mole fraction|psig|kpag|psia|bbl/day|mmscfd|deg f|deg c|°c|°f|hp|kw|minutes?|hrs?|hours?)\b", text, flags=re.IGNORECASE)
    return normalize_space(unit_match.group(1)) if unit_match else ""


def infer_assertion_type(label: str, value: str) -> str:
    normalized_value = value.strip().upper()
    if re.search(r"\bYES\b|\bNO\b|\bTRUE\b|\bFALSE\b", normalized_value):
        return "BOOLEAN"
    if " to " in value.lower() and re.search(r"\d", value):
        return "RANGE"
    if re.search(r"\d", value):
        if "composition" in label.lower() or "mole fraction" in label.lower():
            return "COMPOSITION"
        return "NUMERIC"
    if any(token in normalized_value for token in ["TBD", "TBC", "OPEN", "CLOSED", "IN", "OUT", "ACTIVE", "RETIRED", "MOVED"]):
        if "location" in label.lower():
            return "LOCATION"
        return "STATE"
    if "location" in label.lower() or "facility" in label.lower():
        return "LOCATION"
    if any(token in label.lower() for token in ["state", "scope", "status", "responsibility", "compliance"]):
        return "STATE"
    return "ENUM"


def infer_assertion_domain(label: str, value: str, discovery_source: str) -> str:
    text = f"{label} {value}".lower()
    if discovery_source == "DECISION_LOG":
        if any(token in text for token in ["scope", "boundary", "in-scope", "out ", "retired", "cancelled", "future"]):
            return "SCOPE_STATE"
        if any(token in text for token in ["move", "location", "to 4-25", "to 3-25", "shared"]):
            return "LOCATION_STATE"
        if "compliance" in text or "obligation" in text:
            return "REGULATORY_STATE"
        return "PROCESS_CONDITION"
    if discovery_source == "SCOPE_CHANGE":
        if any(token in text for token in ["location", "move", "shared", "facility", "3-25", "4-25"]):
            return "LOCATION_STATE"
        if any(token in text for token in ["scope", "retire", "remove", "add", "future"]):
            return "SCOPE_STATE"
        return "PROCESS_CONDITION"
    if discovery_source == "OPEN_ISSUE":
        if any(token in text for token in ["boundary", "scope", "responsibility"]):
            return "SCOPE_STATE"
        if any(token in text for token in ["regulatory", "compliance"]):
            return "REGULATORY_STATE"
        return "PROCESS_CONDITION"
    if any(token in text for token in ["pressure", "temperature", "flow", "composition", "sulphur", "sulfur", "spec", "h2s", "co2"]):
        if any(token in text for token in ["spec", "sulphur", "sulfur", "product", "sales gas"]):
            return "PRODUCT_SPEC"
        return "PROCESS_CONDITION"
    if any(token in text for token in ["fuel gas", "instrument air", "utility", "power", "steam", "hot oil", "heat medium"]):
        return "UTILITY_CONDITION"
    if any(token in text for token in ["mawp", "design limit", "capacity", "design pressure", "design temperature", "hp", "kw"]):
        return "EQUIPMENT_LIMIT"
    if any(token in text for token in ["target", "performance", "yield", "recovery", "retention time"]):
        return "OPERATING_TARGET"
    if any(token in text for token in ["scope", "include", "exclude", "responsibility", "ownership"]):
        return "SCOPE_STATE"
    if any(token in text for token in ["location", "facility", "shared", "moved"]):
        return "LOCATION_STATE"
    if any(token in text for token in ["regulatory", "compliance", "obligation"]):
        return "REGULATORY_STATE"
    if any(token in text for token in ["control", "interlock", "logic", "protection"]):
        return "CONTROL_LOGIC"
    return "PROCESS_CONDITION"


def infer_criticality(domain: str, label: str, value: str) -> str:
    text = f"{label} {value}".lower()
    if domain in {"PRODUCT_SPEC", "EQUIPMENT_LIMIT", "SCOPE_STATE", "LOCATION_STATE", "REGULATORY_STATE"}:
        return "HIGH"
    if any(token in text for token in ["pressure", "temperature", "flow", "composition", "spec", "capacity", "mawp", "flare"]):
        return "HIGH"
    if domain in {"PROCESS_CONDITION", "UTILITY_CONDITION", "CONTROL_LOGIC"}:
        return "NORMAL"
    return "LOW"


def infer_comparison(type_name: str, value: str) -> Tuple[str, str]:
    if type_name == "BOOLEAN":
        return ("EXACT", "")
    if type_name in {"STATE", "ENUM", "LOCATION"}:
        return ("TOKEN_MATCH", "")
    if type_name == "RANGE":
        return ("RANGE_MATCH", "")
    if type_name in {"NUMERIC", "COMPOSITION"}:
        match = re.search(r"\.(\d+)", value.replace(",", ""))
        digits = len(match.group(1)) if match else 0
        return ("ROUND_N", str(min(digits, 6)))
    return ("EXACT", "")


def make_assertion_key(parts: Sequence[str], unit: str = "") -> str:
    cleaned = [normalize_key_token(part) for part in parts if normalize_key_token(part)]
    unit_token = normalize_key_token(unit)
    if unit_token and all(unit_token not in part for part in cleaned):
        cleaned.append(unit_token)
    key = "__".join(cleaned[:4])
    key = re.sub(r"_+", "_", key).strip("_")
    return key[:180]


def build_normalization_hint(assertion_type: str, unit: str, comparison_rule: str, comparison_parameter: str) -> str:
    if assertion_type in {"NUMERIC", "COMPOSITION", "RANGE"}:
        unit_hint = f" in {unit}" if unit else ""
        if comparison_rule == "ROUND_N" and comparison_parameter:
            return f"Normalize numeric value{unit_hint} and round to {comparison_parameter} decimal place(s)."
        return f"Normalize numeric value{unit_hint} without prose qualifiers."
    if assertion_type in {"STATE", "ENUM", "LOCATION"}:
        return "Normalize to canonical uppercase tokens with stable terminology."
    if assertion_type == "BOOLEAN":
        return "Normalize to TRUE or FALSE."
    return "Normalize to a stable canonical token."


def extract_decimal_example(value: str) -> str:
    value = normalize_space(value)
    value = re.sub(r"\*\*", "", value)
    return value[:200]


def choose_authority(section_ids: Sequence[str], schema_index: Dict[str, Dict[str, str]], domain: str) -> Tuple[str, str]:
    deduped = dedupe_preserve_order(section_ids)
    if not deduped:
        return ("", "NEEDS_REVIEW")
    if len(deduped) == 1:
        return (deduped[0], "READY_FOR_FREEZE")
    preference = SECTION_TYPE_AUTHORITY_PREFERENCE.get(domain, [])
    for preferred_type in preference:
        matches = [section_id for section_id in deduped if schema_index.get(section_id, {}).get("SectionType", "") == preferred_type]
        if len(matches) == 1:
            return (matches[0], "READY_FOR_FREEZE")
    ordered = sorted(deduped, key=lambda section_id: (_safe_int(schema_index.get(section_id, {}).get("SectionOrder", "999999")), section_id))
    return (ordered[0], "NEEDS_REVIEW")


def _safe_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 999999


def is_relevant_table(block: TableBlock) -> bool:
    if not block.rows:
        return False
    headers = [normalize_space(header) for header in block.rows[0].keys()]
    lower_headers = {header.lower() for header in headers}
    heading_text = " ".join(block.heading_path).lower()
    caption_text = block.caption.lower()
    if lower_headers == {"field", "value"} and "artifact metadata" in heading_text:
        return False
    if "references" in heading_text or lower_headers == {"ref", "description"}:
        return False
    if "coverage" in heading_text or "artifact plan" in heading_text:
        return False
    if caption_text.startswith("table ") or any(re.search(r"\d", cell or "") for row in block.rows for cell in row.values()):
        return True
    if any(token in caption_text for token in ["pressure", "temperature", "flow", "composition", "performance", "spec", "capacity"]):
        return True
    return False


def build_label_parts(block: TableBlock, row_label: str, column_name: str) -> List[str]:
    heading = canonicalize_label(" / ".join(part for part in block.heading_path if part))
    caption = canonicalize_label(block.caption)
    label_parts = []
    if caption:
        label_parts.append(caption)
    elif heading:
        label_parts.append(heading)
    if row_label and row_label.upper() not in {"TOTAL", "TOTALS"}:
        label_parts.append(canonicalize_label(row_label))
    if column_name and normalize_key_token(column_name) not in GENERIC_VALUE_HEADERS:
        label_parts.append(canonicalize_label(column_name))
    return label_parts


def generate_table_candidates(
    artifact_path: Path,
    artifact_context: Dict[str, object],
    text: str,
    schema_index: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for block in parse_markdown_tables_with_context(text):
        if not is_relevant_table(block):
            continue
        headers = list(block.rows[0].keys()) if block.rows else []
        if len(headers) < 2:
            continue
        row_key_header = headers[0]
        for table_row in block.rows:
            row_label = normalize_space(table_row.get(row_key_header, ""))
            for column_name, raw_value in table_row.items():
                if column_name == row_key_header:
                    continue
                value = normalize_space(raw_value)
                if not value or value in {"—", "-"}:
                    continue
                label_parts = build_label_parts(block, row_label, column_name)
                if not label_parts:
                    continue
                label = canonicalize_label(" — ".join(label_parts))
                unit = extract_unit(row_label, column_name, block.caption)
                assertion_type = infer_assertion_type(label, value)
                discovery_source = "STRUCTURED_TABLE"
                domain = infer_assertion_domain(label, value, discovery_source)
                comparison_rule, comparison_parameter = infer_comparison(assertion_type, value)
                source_section_ids = dedupe_preserve_order(artifact_context["section_ids"])
                authority_section_id, resolution_status = choose_authority(source_section_ids, schema_index, domain)
                if len(source_section_ids) > 1 and resolution_status == "READY_FOR_FREEZE":
                    resolution_status = "NEEDS_REVIEW"
                rows.append(
                    {
                        "AssertionKey": make_assertion_key(label_parts, unit),
                        "AssertionLabel": label,
                        "AssertionDomain": domain,
                        "AssertionType": assertion_type,
                        "CanonicalTerm": label,
                        "Unit": unit,
                        "ComparisonRule": comparison_rule,
                        "ComparisonParameter": comparison_parameter,
                        "AuthoritySectionID": authority_section_id,
                        "RequiredSectionIDs": "; ".join(source_section_ids),
                        "FacilityScope": normalize_space(str(artifact_context["source_domain"])),
                        "CurrentStateBasis": normalize_space(str(artifact_context["current_state_basis"])),
                        "DecisionRefs": "; ".join(dedupe_preserve_order(artifact_context["decision_refs"])),
                        "DiscoverySource": discovery_source,
                        "SourceKTYIDs": "; ".join(dedupe_preserve_order([str(artifact_context["kty_id"])])),
                        "SourceSectionIDs": "; ".join(source_section_ids),
                        "NormalizationHint": build_normalization_hint(assertion_type, unit, comparison_rule, comparison_parameter),
                        "Criticality": infer_criticality(domain, label, value),
                        "CandidateValueExample": extract_decimal_example(value),
                        "SourceArtifact": str(artifact_path.resolve()),
                        "SourceRef": first_nonempty(block.caption, " / ".join(block.heading_path)),
                        "Notes": f"Structured table extraction from {artifact_path.name}.",
                        "ResolutionStatus": resolution_status,
                    }
                )
    return rows


def build_artifact_contexts(section_map_rows: Sequence[Dict[str, str]]) -> Tuple[Dict[Path, Dict[str, object]], Dict[str, set], Dict[str, set]]:
    artifact_contexts: Dict[Path, Dict[str, object]] = {}
    decision_to_sections: Dict[str, set] = defaultdict(set)
    sca_to_sections: Dict[str, set] = defaultdict(set)
    for row in section_map_rows:
        artifact_path = Path(row.get("ArtifactPath", "")).resolve()
        if not artifact_path.exists():
            continue
        if artifact_path.name in IGNORED_ARTIFACT_NAMES or not artifact_path.name.startswith("KA-"):
            continue
        context = artifact_contexts.setdefault(
            artifact_path,
            {
                "section_ids": [],
                "kty_id": row.get("KnowledgeTypeID", ""),
                "source_domain": row.get("SourceDomain", ""),
                "current_state_basis": row.get("CurrentStateBasis", ""),
                "decision_refs": [],
                "sca_refs": [],
            },
        )
        context["section_ids"] = dedupe_preserve_order(list(context["section_ids"]) + [row.get("SectionID", "")])
        context["decision_refs"] = dedupe_preserve_order(list(context["decision_refs"]) + parse_list_cell(row.get("DecisionRefs", "")))
        context["sca_refs"] = dedupe_preserve_order(list(context["sca_refs"]) + parse_list_cell(row.get("SCARefs", "")))
        for decision_ref in parse_list_cell(row.get("DecisionRefs", "")):
            decision_to_sections[decision_ref].add(row.get("SectionID", ""))
        for sca_ref in parse_list_cell(row.get("SCARefs", "")):
            sca_to_sections[sca_ref].add(row.get("SectionID", ""))
    return artifact_contexts, decision_to_sections, sca_to_sections


def merge_candidate_rows(rows: Sequence[Dict[str, str]], schema_index: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
    grouped: Dict[str, Dict[str, str]] = {}
    key_counts: Counter[str] = Counter()
    for row in rows:
        key = row["AssertionKey"]
        key_counts[key] += 1
        if key not in grouped:
            grouped[key] = dict(row)
            continue
        current = grouped[key]
        for list_field in ["RequiredSectionIDs", "DecisionRefs", "SourceKTYIDs", "SourceSectionIDs", "SourceArtifact", "SourceRef"]:
            current[list_field] = "; ".join(
                dedupe_preserve_order(parse_list_cell(current.get(list_field, "")) + parse_list_cell(row.get(list_field, "")))
            )
        for text_field in ["Notes", "CandidateValueExample"]:
            current[text_field] = " | ".join(dedupe_preserve_order([current.get(text_field, ""), row.get(text_field, "")]))
        if any(current.get(field, "") != row.get(field, "") for field in ["AssertionLabel", "AssertionDomain", "AssertionType", "Unit", "ComparisonRule", "ComparisonParameter", "Criticality"]):
            current["ResolutionStatus"] = "NEEDS_REVIEW"
            current["Notes"] = " | ".join(
                dedupe_preserve_order([current.get("Notes", ""), "Merged heterogeneous structured candidates under one semantic key."])
            )
        merged_sections = dedupe_preserve_order(parse_list_cell(current.get("SourceSectionIDs", "")))
        authority, status = choose_authority(merged_sections, schema_index, current.get("AssertionDomain", "PROCESS_CONDITION"))
        current["AuthoritySectionID"] = authority
        if current.get("ResolutionStatus", "") != "NEEDS_REVIEW":
            current["ResolutionStatus"] = status
    merged = []
    for key in sorted(grouped):
        row = grouped[key]
        if key_counts[key] > 1 and row.get("ResolutionStatus", "") == "READY_FOR_FREEZE":
            row["ResolutionStatus"] = "NEEDS_REVIEW"
        merged.append({column: row.get(column, "") for column in CANDIDATE_COLUMNS})
    return merged


def load_open_issue_candidates(
    open_issues_path: Optional[Path],
    section_map_rows: Sequence[Dict[str, str]],
    schema_index: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    if not open_issues_path or not open_issues_path.exists():
        return []
    rows = read_csv_rows(open_issues_path)
    by_kty: Dict[str, set] = defaultdict(set)
    for row in section_map_rows:
        if row.get("KnowledgeTypeID", ""):
            by_kty[row["KnowledgeTypeID"]].add(row.get("SectionID", ""))
    result: List[Dict[str, str]] = []
    for row in rows:
        sections: List[str] = []
        notes: List[str] = []
        description = first_nonempty(row.get("Description", ""), row.get("Statement", ""), row.get("RecommendedResolution", ""))
        if not description:
            continue
        if row.get("RefersTo", "").startswith("KTY-"):
            sections = sorted(by_kty.get(row["RefersTo"], set()))
            notes.append(f"Open issue refers to {row['RefersTo']}.")
        if row.get("DecisionRef", ""):
            for map_row in section_map_rows:
                if row["DecisionRef"] in parse_list_cell(map_row.get("DecisionRefs", "")):
                    sections.append(map_row.get("SectionID", ""))
        sections = dedupe_preserve_order(sections)
        if not sections:
            continue
        issue_label = first_nonempty(row.get("IssueType", ""), row.get("CurrentStatus", ""), row.get("Description", ""), row.get("Statement", ""))
        label = canonicalize_label(f"{issue_label} — {description[:120]}")
        domain = infer_assertion_domain(label, description, "OPEN_ISSUE")
        assertion_type = infer_assertion_type(label, row.get("CurrentStatus", "") or description)
        comparison_rule, comparison_parameter = infer_comparison(assertion_type, row.get("CurrentStatus", "") or description)
        authority, status = choose_authority(sections, schema_index, domain)
        result.append(
            {
                "AssertionKey": make_assertion_key([issue_label or "OPEN_ISSUE", description[:80]], ""),
                "AssertionLabel": label,
                "AssertionDomain": domain,
                "AssertionType": assertion_type,
                "CanonicalTerm": label,
                "Unit": "",
                "ComparisonRule": comparison_rule,
                "ComparisonParameter": comparison_parameter,
                "AuthoritySectionID": authority,
                "RequiredSectionIDs": "; ".join(sections),
                "FacilityScope": "",
                "CurrentStateBasis": "Open issue state",
                "DecisionRefs": row.get("DecisionRef", ""),
                "DiscoverySource": "OPEN_ISSUE",
                "SourceKTYIDs": row.get("RefersTo", "") if row.get("RefersTo", "").startswith("KTY-") else "",
                "SourceSectionIDs": "; ".join(sections),
                "NormalizationHint": build_normalization_hint(assertion_type, "", comparison_rule, comparison_parameter),
                "Criticality": infer_criticality(domain, label, description),
                "CandidateValueExample": extract_decimal_example(first_nonempty(row.get("CurrentStatus", ""), description)),
                "SourceArtifact": str(open_issues_path.resolve()),
                "SourceRef": first_nonempty(row.get("OpenIssueID", ""), row.get("Anchor", "")),
                "Notes": " | ".join(dedupe_preserve_order(notes + ["Open issue candidate."])),
                "ResolutionStatus": status,
            }
        )
    return result


def load_decision_candidates(
    decision_log_path: Optional[Path],
    decision_to_sections: Dict[str, set],
    schema_index: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    if not decision_log_path or not decision_log_path.exists():
        return []
    rows = read_csv_rows(decision_log_path)
    result: List[Dict[str, str]] = []
    for row in rows:
        decision_ref = first_nonempty(row.get("DecisionRef", ""), row.get("DecisionID", ""))
        sections = dedupe_preserve_order(sorted(decision_to_sections.get(decision_ref, set())))
        if not decision_ref or not sections:
            continue
        topic = first_nonempty(row.get("Topic", ""), row.get("Decision", ""), decision_ref)
        value_example = first_nonempty(row.get("Status", ""), row.get("Decision", ""))
        domain = infer_assertion_domain(topic, value_example, "DECISION_LOG")
        assertion_type = infer_assertion_type(topic, value_example)
        comparison_rule, comparison_parameter = infer_comparison(assertion_type, value_example)
        authority, status = choose_authority(sections, schema_index, domain)
        result.append(
            {
                "AssertionKey": make_assertion_key([topic, "DECISION_STATE"]),
                "AssertionLabel": canonicalize_label(topic),
                "AssertionDomain": domain,
                "AssertionType": assertion_type,
                "CanonicalTerm": canonicalize_label(topic),
                "Unit": "",
                "ComparisonRule": comparison_rule,
                "ComparisonParameter": comparison_parameter,
                "AuthoritySectionID": authority,
                "RequiredSectionIDs": "; ".join(sections),
                "FacilityScope": "",
                "CurrentStateBasis": first_nonempty(row.get("Status", ""), "Decision log"),
                "DecisionRefs": decision_ref,
                "DiscoverySource": "DECISION_LOG",
                "SourceKTYIDs": "",
                "SourceSectionIDs": "; ".join(sections),
                "NormalizationHint": build_normalization_hint(assertion_type, "", comparison_rule, comparison_parameter),
                "Criticality": infer_criticality(domain, topic, value_example),
                "CandidateValueExample": extract_decimal_example(value_example),
                "SourceArtifact": str(decision_log_path.resolve()),
                "SourceRef": decision_ref,
                "Notes": "Decision-log-derived current-state candidate.",
                "ResolutionStatus": status,
            }
        )
    return result


def load_sca_candidates(
    sca_dirs: Sequence[Path],
    sca_to_sections: Dict[str, set],
    schema_index: Dict[str, Dict[str, str]],
) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for sca_dir in sca_dirs:
        amendment_csv = sca_dir / "Amendment_Actions.csv"
        if not amendment_csv.exists():
            continue
        rows = read_csv_rows(amendment_csv)
        sca_ref = sca_dir.name.split("_", 1)[0]
        sections = dedupe_preserve_order(sorted(sca_to_sections.get(sca_ref, set())))
        for row in rows:
            row_sections = list(sections)
            if not row_sections:
                continue
            description = first_nonempty(row.get("Description", ""), row.get("EntityID", ""))
            domain = infer_assertion_domain(description, row.get("ActionType", ""), "SCOPE_CHANGE")
            assertion_type = infer_assertion_type(description, row.get("Description", ""))
            comparison_rule, comparison_parameter = infer_comparison(assertion_type, row.get("Description", ""))
            authority, status = choose_authority(row_sections, schema_index, domain)
            result.append(
                {
                    "AssertionKey": make_assertion_key([row.get("EntityID", ""), description, sca_ref]),
                    "AssertionLabel": canonicalize_label(description),
                    "AssertionDomain": domain,
                    "AssertionType": assertion_type,
                    "CanonicalTerm": canonicalize_label(description),
                    "Unit": "",
                    "ComparisonRule": comparison_rule,
                    "ComparisonParameter": comparison_parameter,
                    "AuthoritySectionID": authority,
                    "RequiredSectionIDs": "; ".join(row_sections),
                    "FacilityScope": "",
                    "CurrentStateBasis": sca_ref,
                    "DecisionRefs": "",
                    "DiscoverySource": "SCOPE_CHANGE",
                    "SourceKTYIDs": "",
                    "SourceSectionIDs": "; ".join(row_sections),
                    "NormalizationHint": build_normalization_hint(assertion_type, "", comparison_rule, comparison_parameter),
                    "Criticality": infer_criticality(domain, description, row.get("ActionType", "")),
                    "CandidateValueExample": extract_decimal_example(first_nonempty(row.get("ActionType", ""), description)),
                    "SourceArtifact": str(amendment_csv.resolve()),
                    "SourceRef": first_nonempty(row.get("AmendmentID", ""), row.get("ActionSeq", "")),
                    "Notes": f"SCA amendment action for {row.get('EntityType', '')} {row.get('EntityID', '')}.",
                    "ResolutionStatus": status,
                }
            )
    return result


def _read_hypergraph_manifest_fields(manifest: Dict[str, object]) -> Dict[str, str]:
    """Extract hypergraph-related fields from the parsed manifest explicit dict.

    Returns a dict with normalised keys.  Missing keys map to empty strings.
    """
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
    """Return True only when the manifest explicitly admits hypergraph evidence
    for planning-stage use (Gate 2 / Gate 4).

    The tool must work identically when this returns False — all hypergraph
    code paths are gated behind this check.
    """
    mode = hg_fields.get("use_mode", "").strip().upper()
    if mode not in HYPERGRAPH_PLANNING_MODES:
        return False
    # Even when the mode permits planning use, a BLOCKED QA verdict limits
    # the evidence to non-authoritative clustering only.  The candidate
    # builder still emits suggestions, but the caller must treat them as
    # advisory.
    return True


def _load_hypergraph_evidence(hg_fields: Dict[str, str], manifest_dir: Path) -> Dict[str, object]:
    """Load hypergraph nodes, hyperedges, and evidence CSVs when available.

    All loading is best-effort: missing files are silently skipped and the
    caller receives an empty collection for that evidence type.

    Returns a dict with keys:
      nodes            List[Dict[str, str]]
      hyperedges       List[Dict[str, str]]
      discovered_ktys  List[Dict[str, str]]
      subjects         List[Dict[str, str]]
      objectives       List[Dict[str, str]]
      artifact_map     List[Dict[str, str]]
    """
    result: Dict[str, object] = {
        "nodes": [],
        "hyperedges": [],
        "discovered_ktys": [],
        "subjects": [],
        "objectives": [],
        "artifact_map": [],
    }

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

    evidence_root = _resolve(hg_fields.get("evidence_root", ""))
    if evidence_root and evidence_root.is_dir():
        for csv_path in sorted(evidence_root.glob("*.csv")):
            rows = read_csv_rows(csv_path)
            name_lower = csv_path.stem.lower()
            if "kty" in name_lower or "knowledge_type" in name_lower:
                result["discovered_ktys"] = rows
            elif "subject" in name_lower:
                result["subjects"] = rows
            elif "objective" in name_lower:
                result["objectives"] = rows
            elif "artifact" in name_lower:
                result["artifact_map"] = rows

    return result


def _identify_repeated_patterns(
    hg_evidence: Dict[str, object],
    section_map_rows: Sequence[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Identify repeated structural patterns across mapped sections using
    hypergraph evidence.

    This is an AUXILIARY discovery step only.  The returned candidate rows
    are tagged with DiscoverySource = HYPERGRAPH_AUXILIARY and must be
    reviewed before freeze.
    """
    candidates: List[Dict[str, str]] = []

    # Build a set of KTY IDs already present in the section map so we
    # can detect objective / subject participation that spans multiple KTYs.
    mapped_kty_ids = {row.get("KnowledgeTypeID", "") for row in section_map_rows if row.get("KnowledgeTypeID", "")}

    # --- Repeated objective participation ---------------------------------
    # If two or more mapped KTYs share the same objective in the hypergraph,
    # that objective is a candidate for a cross-section concordance assertion.
    objectives: List[Dict[str, str]] = list(hg_evidence.get("objectives", []))
    hyperedges: List[Dict[str, str]] = list(hg_evidence.get("hyperedges", []))

    # Build objective -> set of supporting KTY IDs from hyperedges
    obj_to_ktys: Dict[str, set] = defaultdict(set)
    for edge in hyperedges:
        edge_type = edge.get("EdgeType", "") or edge.get("Type", "")
        if edge_type != "KTY_SUPPORTS_OBJ":
            continue
        source = edge.get("Source", "") or edge.get("SourceID", "")
        target = edge.get("Target", "") or edge.get("TargetID", "")
        if source in mapped_kty_ids:
            obj_to_ktys[target].add(source)

    for obj_id, supporting_ktys in obj_to_ktys.items():
        if len(supporting_ktys) < 2:
            continue
        # Look up objective label
        obj_label = obj_id
        for obj_row in objectives:
            if obj_row.get("ObjectiveID", "") == obj_id or obj_row.get("ID", "") == obj_id:
                obj_label = obj_row.get("Name", "") or obj_row.get("ObjectiveName", "") or obj_id
                break
        label = canonicalize_label(f"Cross-KTY objective — {obj_label}")
        candidates.append({
            "AssertionKey": make_assertion_key(["XOBJ", obj_id]),
            "AssertionLabel": label,
            "AssertionDomain": "PROCESS_CONDITION",
            "AssertionType": "STATE",
            "CanonicalTerm": label,
            "Unit": "",
            "ComparisonRule": "TOKEN_MATCH",
            "ComparisonParameter": "",
            "AuthoritySectionID": "",
            "RequiredSectionIDs": "",
            "FacilityScope": "",
            "CurrentStateBasis": "",
            "DecisionRefs": "",
            "DiscoverySource": "HYPERGRAPH_AUXILIARY",
            "SourceKTYIDs": "; ".join(sorted(supporting_ktys)),
            "SourceSectionIDs": "",
            "NormalizationHint": "Normalize to canonical uppercase tokens with stable terminology.",
            "Criticality": "NORMAL",
            "CandidateValueExample": "",
            "SourceArtifact": "HYPERGRAPH_SNAPSHOT",
            "SourceRef": obj_id,
            "Notes": f"Hypergraph auxiliary: objective {obj_id} is supported by {len(supporting_ktys)} mapped KTYs; likely cross-section concordance candidate.",
            "ResolutionStatus": "NEEDS_REVIEW",
        })

    return candidates


def _identify_omitted_participants(
    hg_evidence: Dict[str, object],
    section_map_rows: Sequence[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Use hypergraph subject/artifact adjacency to identify likely omitted
    participant sections for existing section-map entries.

    Returns advisory candidate rows tagged HYPERGRAPH_AUXILIARY.
    """
    candidates: List[Dict[str, str]] = []
    hyperedges: List[Dict[str, str]] = list(hg_evidence.get("hyperedges", []))
    mapped_kty_ids = {row.get("KnowledgeTypeID", "") for row in section_map_rows if row.get("KnowledgeTypeID", "")}

    # Build subject -> KTY adjacency from HAS_SUBJECT edges
    subject_to_ktys: Dict[str, set] = defaultdict(set)
    for edge in hyperedges:
        edge_type = edge.get("EdgeType", "") or edge.get("Type", "")
        if edge_type != "HAS_SUBJECT":
            continue
        source = edge.get("Source", "") or edge.get("SourceID", "")
        target = edge.get("Target", "") or edge.get("TargetID", "")
        if source.startswith("KTY-"):
            subject_to_ktys[target].add(source)
        elif target.startswith("KTY-"):
            subject_to_ktys[source].add(target)

    for subject_id, adjacent_ktys in subject_to_ktys.items():
        mapped_adjacent = adjacent_ktys & mapped_kty_ids
        unmapped_adjacent = adjacent_ktys - mapped_kty_ids
        if mapped_adjacent and unmapped_adjacent:
            # Subject is partially covered — the unmapped KTYs are potential
            # omitted participants.
            subjects: List[Dict[str, str]] = list(hg_evidence.get("subjects", []))
            subject_label = subject_id
            for subj_row in subjects:
                if subj_row.get("SubjectID", "") == subject_id or subj_row.get("ID", "") == subject_id:
                    subject_label = subj_row.get("Name", "") or subj_row.get("SubjectName", "") or subject_id
                    break
            label = canonicalize_label(f"Omitted participant — {subject_label}")
            candidates.append({
                "AssertionKey": make_assertion_key(["OMIT_PART", subject_id]),
                "AssertionLabel": label,
                "AssertionDomain": "SCOPE_STATE",
                "AssertionType": "STATE",
                "CanonicalTerm": label,
                "Unit": "",
                "ComparisonRule": "TOKEN_MATCH",
                "ComparisonParameter": "",
                "AuthoritySectionID": "",
                "RequiredSectionIDs": "",
                "FacilityScope": "",
                "CurrentStateBasis": "",
                "DecisionRefs": "",
                "DiscoverySource": "HYPERGRAPH_AUXILIARY",
                "SourceKTYIDs": "; ".join(sorted(unmapped_adjacent)),
                "SourceSectionIDs": "",
                "NormalizationHint": "Normalize to canonical uppercase tokens with stable terminology.",
                "Criticality": "NORMAL",
                "CandidateValueExample": "",
                "SourceArtifact": "HYPERGRAPH_SNAPSHOT",
                "SourceRef": subject_id,
                "Notes": (
                    f"Hypergraph auxiliary: subject {subject_id} is adjacent to mapped KTYs "
                    f"({', '.join(sorted(mapped_adjacent))}) but also to unmapped KTYs "
                    f"({', '.join(sorted(unmapped_adjacent))}); likely omitted participant sections."
                ),
                "ResolutionStatus": "NEEDS_REVIEW",
            })

    return candidates


def build_coverage_report(
    coverage_path: Path,
    merged_rows: Sequence[Dict[str, str]],
    artifact_contexts: Dict[Path, Dict[str, object]],
    skipped_artifacts: Sequence[str],
    hypergraph_used: bool = False,
    hypergraph_use_mode: str = "",
    hypergraph_snapshot: str = "",
) -> int:
    by_source = Counter(row.get("DiscoverySource", "") for row in merged_rows)
    by_domain = Counter(row.get("AssertionDomain", "") for row in merged_rows)
    by_criticality = Counter(row.get("Criticality", "") for row in merged_rows)
    by_status = Counter(row.get("ResolutionStatus", "") for row in merged_rows)
    section_counts: Counter[str] = Counter()
    for row in merged_rows:
        for section_id in parse_list_cell(row.get("SourceSectionIDs", "")):
            section_counts[section_id] += 1

    lines: List[str] = []
    lines.append("# Publication Concordance Coverage")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Candidate rows written: {len(merged_rows)}")
    lines.append(f"- Candidate source artifacts scanned: {len(artifact_contexts)}")
    lines.append(f"- Skipped mapped artifacts: {len(skipped_artifacts)}")
    # --- Hypergraph coverage summary (AUXILIARY_STRUCTURE_EVIDENCE) --------
    if hypergraph_used:
        hg_candidate_count = sum(1 for r in merged_rows if r.get("DiscoverySource") == "HYPERGRAPH_AUXILIARY")
        lines.append(f"- Hypergraph evidence used: YES")
        lines.append(f"- Hypergraph use mode: {hypergraph_use_mode}")
        lines.append(f"- Hypergraph snapshot: {hypergraph_snapshot}")
        lines.append(f"- Hypergraph-suggested candidates: {hg_candidate_count}")
    else:
        lines.append(f"- Hypergraph evidence used: NO")
    lines.append("")
    lines.append("## By Discovery Source")
    lines.append("")
    for key, count in sorted(by_source.items()):
        lines.append(f"- {key}: {count}")
    lines.append("")
    lines.append("## By Assertion Domain")
    lines.append("")
    for key, count in sorted(by_domain.items()):
        lines.append(f"- {key}: {count}")
    lines.append("")
    lines.append("## By Criticality")
    lines.append("")
    for key, count in sorted(by_criticality.items()):
        lines.append(f"- {key}: {count}")
    lines.append("")
    lines.append("## Resolution Status")
    lines.append("")
    for key, count in sorted(by_status.items()):
        lines.append(f"- {key}: {count}")
    lines.append("")
    lines.append("## Section Coverage")
    lines.append("")
    for section_id, count in sorted(section_counts.items()):
        lines.append(f"- {section_id}: {count} candidates")
    if skipped_artifacts:
        lines.append("")
        lines.append("## Skipped Artifacts")
        lines.append("")
        for note in skipped_artifacts:
            lines.append(f"- {note}")
    unresolved = by_status.get("NEEDS_REVIEW", 0) + by_status.get("DUPLICATE_CANDIDATE", 0)
    coverage_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return 2 if unresolved or skipped_artifacts else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic typed concordance candidates for DBM publication.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--coverage-md", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    schema_path = Path(args.schema).resolve()
    section_map_path = Path(args.section_map).resolve()
    output_csv = Path(args.output_csv).resolve()
    coverage_md = Path(args.coverage_md).resolve()

    for path in [manifest_path, schema_path, section_map_path]:
        if not path.exists():
            fatal(f"Required path does not exist: {path}")

    manifest = parse_manifest(manifest_path)
    publication_root = Path(manifest["publication_root"]).resolve()
    require_within(output_csv, publication_root, "--output-csv")
    require_within(coverage_md, publication_root, "--coverage-md")

    schema_rows = parse_schema(schema_path)
    schema_index = {row["SectionID"]: row for row in schema_rows}
    section_map_rows = parse_section_map(section_map_path)
    artifact_contexts, decision_to_sections, sca_to_sections = build_artifact_contexts(section_map_rows)
    manifest_csvs = classify_manifest_csvs(manifest["decomposition_files"])
    open_issues_path = manifest_csvs.get("open_issues")
    decision_log_path = manifest_csvs.get("decision_log")
    sca_dirs = [Path(path).resolve() for path in manifest.get("scope_change_dirs", [])]

    candidate_rows: List[Dict[str, str]] = []
    skipped_artifacts: List[str] = []

    for artifact_path, artifact_context in sorted(artifact_contexts.items(), key=lambda item: str(item[0])):
        try:
            text = artifact_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            skipped_artifacts.append(f"{artifact_path.name}: unreadable as UTF-8 markdown.")
            continue
        rows = generate_table_candidates(artifact_path, artifact_context, text, schema_index)
        if not rows:
            skipped_artifacts.append(f"{artifact_path.name}: no structured concordance candidates harvested.")
            continue
        candidate_rows.extend(rows)

    candidate_rows.extend(load_open_issue_candidates(open_issues_path, section_map_rows, schema_index))
    candidate_rows.extend(load_decision_candidates(decision_log_path, decision_to_sections, schema_index))
    candidate_rows.extend(load_sca_candidates(sca_dirs, sca_to_sections, schema_index))

    # ------------------------------------------------------------------
    # Optional hypergraph-assisted candidate enrichment
    # (AUXILIARY_STRUCTURE_EVIDENCE — see plan Phase 2, Tool 1).
    #
    # When the frozen manifest admits a hypergraph snapshot with a
    # planning-compatible use mode, load the graph evidence and generate
    # supplementary candidates tagged DiscoverySource = HYPERGRAPH_AUXILIARY.
    #
    # Constraints enforced here:
    #   - Must NOT generate canonical assertion values from graph topology.
    #   - Must NOT override candidates already grounded in mapped source
    #     content (the merge step handles dedup, so we simply append).
    # ------------------------------------------------------------------
    hg_fields = _read_hypergraph_manifest_fields(manifest)
    hypergraph_used = False
    if _hypergraph_planning_allowed(hg_fields):
        hg_evidence = _load_hypergraph_evidence(hg_fields, manifest_path.parent)
        hg_has_data = any(hg_evidence.get(k) for k in ("nodes", "hyperedges", "discovered_ktys", "subjects", "objectives", "artifact_map"))
        if hg_has_data:
            hypergraph_used = True
            candidate_rows.extend(_identify_repeated_patterns(hg_evidence, section_map_rows))
            candidate_rows.extend(_identify_omitted_participants(hg_evidence, section_map_rows))

    if not candidate_rows:
        fatal("No concordance candidates could be harvested from the structured sources.", code=1)

    merged_rows = merge_candidate_rows(candidate_rows, schema_index)
    for row in merged_rows:
        if row["AssertionDomain"] not in ALLOWED_ASSERTION_DOMAINS:
            fatal(f"Invalid AssertionDomain produced: {row['AssertionDomain']}")
        if row["DiscoverySource"] not in ALLOWED_DISCOVERY_SOURCES:
            fatal(f"Invalid DiscoverySource produced: {row['DiscoverySource']}")
        if row["Criticality"] not in ALLOWED_CRITICALITY:
            fatal(f"Invalid Criticality produced: {row['Criticality']}")
        if row["ResolutionStatus"] not in ALLOWED_RESOLUTION_STATUS:
            fatal(f"Invalid ResolutionStatus produced: {row['ResolutionStatus']}")

    write_csv(output_csv, CANDIDATE_COLUMNS, merged_rows)
    exit_code = build_coverage_report(
        coverage_md, merged_rows, artifact_contexts, skipped_artifacts,
        hypergraph_used=hypergraph_used,
        hypergraph_use_mode=hg_fields.get("use_mode", "NONE"),
        hypergraph_snapshot=hg_fields.get("snapshot_path", ""),
    )
    print(f"Candidate rows written: {len(merged_rows)}")
    print(f"Skipped mapped artifacts: {len(skipped_artifacts)}")
    if hypergraph_used:
        hg_count = sum(1 for r in merged_rows if r.get("DiscoverySource") == "HYPERGRAPH_AUXILIARY")
        print(f"Hypergraph-suggested candidates: {hg_count}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
