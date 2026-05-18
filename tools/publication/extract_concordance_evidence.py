#!/usr/bin/env python3
"""
extract_concordance_evidence.py - Raw concordance evidence atom extractor.

Purpose:
  Read frozen DBM publication planning artifacts and emit raw evidence atoms
  plus a mechanical risk inventory. This tool does not classify typed
  concordance assertions; semantic targeting belongs to TASK +
  dbm-concordance-seed.

Inputs:
  --manifest            Frozen Publication_Input_Manifest.md
  --schema              Approved Publication_Schema.md
  --section-map         Approved Section_Map.csv
  --output-atoms-csv    Publication_Concordance_Evidence_Atoms.csv
  --risk-inventory-csv  Publication_Concordance_Risk_Inventory.csv
  --coverage-md         Evidence extraction coverage report

Writes only the three output paths above, all under the publication root.

Exit codes:
  0 = success
  1 = fatal input / parsing error
  2 = success with mechanical risk inventory rows requiring review
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import (  # type: ignore
    classify_manifest_csvs,
    parse_manifest,
    read_csv_rows,
    require_within,
    write_csv,
)

ATOM_COLUMNS = [
    "AtomID",
    "SourceArtifact",
    "SourceKTYID",
    "MappedSectionIDs",
    "HeadingPath",
    "BlockType",
    "TableCaption",
    "RowLabel",
    "ColumnName",
    "RawText",
    "RawValue",
    "UnitText",
    "SourceRef",
    "NearbyContext",
    "ExtractionReason",
    "RiskSignals",
    "MappingRole",
    "ContributionScope",
]

RISK_COLUMNS = [
    "RiskID",
    "RiskClass",
    "SourceArtifact",
    "SourceKTYID",
    "AffectedSectionIDs",
    "CurrentStateBasis",
    "WhyItMatters",
    "ExpectedConcordanceTreatment",
    "RegisterAssertionKey",
    "CoverageStatus",
    "WaiverReason",
]

CLASSIFICATION_FORBIDDEN_COLUMNS = {
    "AssertionDomain",
    "AssertionType",
    "Criticality",
    "AuthoritySectionID",
    "ComparisonRule",
    "NormalizationContract",
    "SourceFidelityCritical",
}


def fatal(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def strip_markdown(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = value.replace("**", "").replace("*", "")
    value = re.sub(r"<[^>]+>", "", value)
    return normalize_space(value)


def stable_id(prefix: str, *parts: str) -> str:
    payload = "\n".join(parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha1(payload).hexdigest()[:12].upper()}"


def parse_table_block(lines: Sequence[str]) -> List[Dict[str, str]]:
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


def markdown_tables_with_context(text: str) -> List[Tuple[int, Tuple[str, ...], str, List[Dict[str, str]], List[str]]]:
    headings: List[str] = []
    recent: List[str] = []
    table_lines: List[str] = []
    table_start = 0
    results: List[Tuple[int, Tuple[str, ...], str, List[Dict[str, str]], List[str]]] = []

    def flush() -> None:
        nonlocal table_lines, table_start
        if not table_lines:
            return
        rows = parse_table_block(table_lines)
        if rows:
            caption = ""
            for candidate in reversed(recent):
                if not candidate.startswith("|"):
                    caption = strip_markdown(candidate)
                    break
            results.append((table_start, tuple(headings), caption, rows, list(recent[-5:])))
        table_lines = []
        table_start = 0

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.rstrip()
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if heading_match:
            flush()
            level = len(heading_match.group(1))
            while len(headings) >= level:
                headings.pop()
            headings.append(strip_markdown(heading_match.group(2)))
            recent.append(line.strip())
            recent = recent[-5:]
            continue
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            if not table_lines:
                table_start = line_no
            table_lines.append(line)
            continue
        flush()
        if stripped:
            recent.append(stripped)
            recent = recent[-5:]
    flush()
    return results


def unit_text(value: str) -> str:
    units = re.findall(
        r"\b(psig|psia|kpag|degf|degc|f|c|mmscfd|scfd|bpd|gpm|hp|kw|mw|ppm|mol%|wt%|ft|in|mm|m)\b",
        value.lower(),
    )
    if units:
        return ";".join(dict.fromkeys(units))
    paren = re.findall(r"\(([^)]{1,20})\)", value)
    return ";".join(dict.fromkeys(paren[:2]))


def source_ref(path: Path, line_no: int) -> str:
    return f"{path.name}:{line_no}"


def risk_signals_for_text(path: Path, text: str, mapped_sections: Sequence[str], lifecycle_state: str = "") -> List[str]:
    signals: List[str] = []
    upper = text.upper()
    if "_Sources" in path.parts:
        signals.append("SOURCE_AUTHORITY")
    if re.search(r"\bSCA-\d{3}\b", text, flags=re.IGNORECASE):
        signals.append("SCA_REFERENCED")
    if "TBD" in upper or "TBC" in upper or "OPEN ISSUE" in upper:
        signals.append("OPEN_TBD")
    if lifecycle_state.upper().startswith("RETIRED") or "RETIRED_NO_FACTUAL_USE" in upper or "TOMBSTONE" in upper:
        signals.append("RETIRED_KTY")
    if len(set(mapped_sections)) > 1:
        signals.append("CROSS_SECTION_DUPLICATE")
    return sorted(set(signals))


def section_map_index(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, object]]:
    index: Dict[str, Dict[str, object]] = {}
    for row in rows:
        artifact = row.get("ArtifactPath", "")
        if not artifact:
            continue
        entry = index.setdefault(
            artifact,
            {
                "sections": set(),
                "ktys": set(),
                "mapping_roles": set(),
                "contribution_scopes": set(),
                "lifecycle_states": set(),
                "current_state_basis": set(),
            },
        )
        entry["sections"].add(row.get("SectionID", ""))
        entry["ktys"].add(row.get("KnowledgeTypeID", ""))
        entry["mapping_roles"].add(row.get("MappingRole", ""))
        entry["contribution_scopes"].add(row.get("ContributionScope", ""))
        entry["lifecycle_states"].add(row.get("LifecycleState", ""))
        entry["current_state_basis"].add(row.get("CurrentStateBasis", ""))
    return index


def mapped_artifacts(section_map_rows: List[Dict[str, str]]) -> List[Path]:
    artifacts = []
    seen = set()
    for row in section_map_rows:
        raw = row.get("ArtifactPath", "")
        if not raw or raw in seen:
            continue
        seen.add(raw)
        path = Path(raw)
        if path.exists() and path.is_file():
            artifacts.append(path)
    return sorted(artifacts, key=lambda p: str(p))


def extract_markdown_atoms(path: Path, meta: Dict[str, object]) -> List[Dict[str, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    atoms: List[Dict[str, str]] = []
    sections = sorted(s for s in meta.get("sections", set()) if s)
    ktys = sorted(k for k in meta.get("ktys", set()) if k)
    mapping_roles = sorted(r for r in meta.get("mapping_roles", set()) if r)
    contribution_scopes = sorted(s for s in meta.get("contribution_scopes", set()) if s)
    lifecycle_state = ";".join(sorted(s for s in meta.get("lifecycle_states", set()) if s))
    for line_no, headings, caption, rows, nearby in markdown_tables_with_context(text):
        if not rows:
            continue
        headers = list(rows[0].keys())
        row_label_header = headers[0] if headers else ""
        for row_index, row in enumerate(rows, start=1):
            row_label = strip_markdown(row.get(row_label_header, "")) if row_label_header else ""
            for column_name, raw in row.items():
                cleaned = strip_markdown(raw)
                if not cleaned or re.fullmatch(r"[-: ]*", cleaned):
                    continue
                signals = risk_signals_for_text(path, cleaned, sections, lifecycle_state)
                atoms.append(
                    {
                        "AtomID": stable_id("ATOM", str(path.resolve()), str(line_no), str(row_index), column_name, cleaned),
                        "SourceArtifact": str(path.resolve()),
                        "SourceKTYID": ";".join(ktys),
                        "MappedSectionIDs": ";".join(sections),
                        "HeadingPath": " > ".join(headings),
                        "BlockType": "TABLE_CELL",
                        "TableCaption": caption,
                        "RowLabel": row_label,
                        "ColumnName": column_name,
                        "RawText": raw,
                        "RawValue": cleaned,
                        "UnitText": unit_text(cleaned),
                        "SourceRef": source_ref(path, line_no),
                        "NearbyContext": " / ".join(strip_markdown(item) for item in nearby),
                        "ExtractionReason": "STRUCTURED_TABLE",
                        "RiskSignals": ";".join(signals),
                        "MappingRole": ";".join(mapping_roles),
                        "ContributionScope": ";".join(contribution_scopes),
                    }
                )
    return atoms


def csv_row_atoms(path: Path, rows: List[Dict[str, str]], block_type: str, reason: str) -> List[Dict[str, str]]:
    atoms: List[Dict[str, str]] = []
    for row_index, row in enumerate(rows, start=1):
        row_text = " | ".join(f"{key}={value}" for key, value in row.items() if value)
        cleaned = strip_markdown(row_text)
        if not cleaned:
            continue
        signals = risk_signals_for_text(path, cleaned, [])
        atoms.append(
            {
                "AtomID": stable_id("ATOM", str(path.resolve()), str(row_index), cleaned),
                "SourceArtifact": str(path.resolve()),
                "SourceKTYID": "",
                "MappedSectionIDs": "",
                "HeadingPath": "",
                "BlockType": block_type,
                "TableCaption": "",
                "RowLabel": str(row_index),
                "ColumnName": "",
                "RawText": row_text,
                "RawValue": cleaned,
                "UnitText": unit_text(cleaned),
                "SourceRef": source_ref(path, row_index + 1),
                "NearbyContext": cleaned,
                "ExtractionReason": reason,
                "RiskSignals": ";".join(signals),
                "MappingRole": "",
                "ContributionScope": "",
            }
        )
    return atoms


def derive_risk_class(atom: Dict[str, str]) -> List[str]:
    text = " ".join([atom.get("RawValue", ""), atom.get("HeadingPath", ""), atom.get("TableCaption", "")]).upper()
    signals = set(filter(None, atom.get("RiskSignals", "").split(";")))
    classes: List[str] = []
    if "RETIRED_KTY" in signals:
        classes.append("RETIRED_CONTENT_REFERENCE")
    if "SCA_REFERENCED" in signals:
        classes.append("SCA_SUPERSEDED_VALUE")
    if "SOURCE_AUTHORITY" in signals:
        classes.append("SOURCE_FIDELITY_CRITICAL")
    if "OPEN_TBD" in signals:
        classes.append("OPEN_TBD")
    if "CROSS_SECTION_DUPLICATE" in signals:
        classes.append("SECTION_AUTHORITY_AMBIGUITY")
    if any(token in text for token in ["SHARED", "COMMON", "FACILITY"]):
        classes.append("SHARED_FACILITY_SYSTEM")
    if any(token in text for token in ["LOCATION", "LOCATED", "04-25", "03-25"]):
        classes.append("FACILITY_LOCATION_STATE")
    if any(token in text for token in ["UTILITY", "FUEL GAS", "INSTRUMENT AIR", "HEAT MEDIUM", "POWER"]):
        classes.append("UTILITY_INTERFACE")
    if any(token in text for token in ["MAWP", "PRESSURE", "TEMPERATURE", "DESIGN", "CAPACITY", "LIMIT"]):
        classes.append("DESIGN_LIMIT")
    if any(token in text for token in ["SPEC", "PRODUCT", "COMPOSITION", "PPM", "WT%", "MOL%"]):
        classes.append("PRODUCT_SPEC")
    if any(token in text for token in ["FLOW", "MMSCFD", "BPD", "GPM", "RATE"]):
        classes.append("FLOW_OR_CAPACITY")
    return sorted(set(classes))


def build_risk_inventory(atoms: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    seen = set()
    for atom in atoms:
        for risk_class in derive_risk_class(atom):
            key = (risk_class, atom.get("SourceArtifact", ""), atom.get("SourceKTYID", ""), atom.get("MappedSectionIDs", ""))
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "RiskID": stable_id("RISK", *key),
                    "RiskClass": risk_class,
                    "SourceArtifact": atom.get("SourceArtifact", ""),
                    "SourceKTYID": atom.get("SourceKTYID", ""),
                    "AffectedSectionIDs": atom.get("MappedSectionIDs", ""),
                    "CurrentStateBasis": atom.get("RiskSignals", ""),
                    "WhyItMatters": f"Mechanical signal indicates {risk_class} may require concordance control.",
                    "ExpectedConcordanceTreatment": "COVER_OR_WAIVE_BEFORE_REGISTER_FREEZE",
                    "RegisterAssertionKey": "",
                    "CoverageStatus": "",
                    "WaiverReason": "",
                }
            )
    return rows


def build_report(path: Path, atoms: Sequence[Dict[str, str]], risks: Sequence[Dict[str, str]], skipped: Sequence[str]) -> None:
    by_block = Counter(atom.get("BlockType", "") for atom in atoms)
    by_signal: Counter[str] = Counter()
    by_section: Counter[str] = Counter()
    for atom in atoms:
        for signal in filter(None, atom.get("RiskSignals", "").split(";")):
            by_signal[signal] += 1
        for section in filter(None, atom.get("MappedSectionIDs", "").split(";")):
            by_section[section] += 1
    lines = [
        "# Concordance Evidence Extraction Coverage",
        "",
        "## Summary",
        "",
        f"- Evidence atoms: {len(atoms)}",
        f"- Risk inventory rows: {len(risks)}",
        f"- Skipped artifacts: {len(skipped)}",
        "",
        "## Atoms By Block Type",
        "",
    ]
    for key, count in sorted(by_block.items()):
        lines.append(f"- {key or 'UNKNOWN'}: {count}")
    lines.extend(["", "## Risk Signal Distribution", ""])
    if by_signal:
        for key, count in sorted(by_signal.items()):
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- None")
    lines.extend(["", "## Section Coverage", ""])
    if by_section:
        for key, count in sorted(by_section.items()):
            lines.append(f"- {key}: {count} atoms")
    else:
        lines.append("- No section-mapped atoms")
    lines.extend(["", "## Skipped Artifacts", ""])
    if skipped:
        for item in skipped:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract raw concordance evidence atoms.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--output-atoms-csv", required=True)
    parser.add_argument("--risk-inventory-csv", required=True)
    parser.add_argument("--coverage-md", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    schema_path = Path(args.schema).resolve()
    section_map_path = Path(args.section_map).resolve()
    atoms_path = Path(args.output_atoms_csv).resolve()
    risks_path = Path(args.risk_inventory_csv).resolve()
    coverage_path = Path(args.coverage_md).resolve()

    if not manifest_path.exists() or not schema_path.exists() or not section_map_path.exists():
        fatal("Manifest, schema, and section map paths must exist.")
    manifest = parse_manifest(manifest_path)
    publication_root = manifest["publication_root"]
    if not isinstance(publication_root, Path):
        fatal("Publication root could not be resolved from manifest.")
    require_within(atoms_path, publication_root, "--output-atoms-csv")
    require_within(risks_path, publication_root, "--risk-inventory-csv")
    require_within(coverage_path, publication_root, "--coverage-md")

    section_map_rows = read_csv_rows(section_map_path)
    forbidden = CLASSIFICATION_FORBIDDEN_COLUMNS & set(section_map_rows[0].keys() if section_map_rows else [])
    if forbidden:
        fatal(f"Section map unexpectedly contains classification-only columns: {', '.join(sorted(forbidden))}")

    meta_by_artifact = section_map_index(section_map_rows)
    atoms: List[Dict[str, str]] = []
    skipped: List[str] = []
    for artifact in mapped_artifacts(section_map_rows):
        if artifact.suffix.lower() != ".md":
            skipped.append(f"{artifact}: non-markdown mapped artifact")
            continue
        extracted = extract_markdown_atoms(artifact, meta_by_artifact.get(str(artifact.resolve()), {}))
        if extracted:
            atoms.extend(extracted)
        else:
            skipped.append(f"{artifact}: no structured table atoms")

    for source_file in sorted(manifest["source_files"]):
        if source_file.suffix.lower() == ".md" and source_file.exists():
            extracted = extract_markdown_atoms(
                source_file,
                {
                    "sections": set(),
                    "ktys": set(),
                    "mapping_roles": {"SOURCE_AUTHORITY"},
                    "contribution_scopes": {"VALUES_ONLY"},
                    "lifecycle_states": set(),
                },
            )
            if extracted:
                atoms.extend(extracted)

    classified = classify_manifest_csvs(manifest["decomposition_files"])
    for key, block_type, reason in [
        ("open_issues", "OPEN_ISSUE", "OPEN_ISSUE_ROW"),
        ("decision_log", "DECISION_LOG", "DECISION_LOG_ROW"),
    ]:
        if key in classified:
            atoms.extend(csv_row_atoms(classified[key], read_csv_rows(classified[key]), block_type, reason))

    for path in sorted(manifest["scope_change_files"]):
        if path.suffix.lower() == ".csv" and path.exists() and path.name in {"Amendment_Actions.csv", "Supersession_Map.csv"}:
            atoms.extend(csv_row_atoms(path, read_csv_rows(path), "SCA_AMENDMENT", "SCA_AMENDMENT_ROW"))

    risks = build_risk_inventory(atoms)
    write_csv(atoms_path, ATOM_COLUMNS, atoms)
    write_csv(risks_path, RISK_COLUMNS, risks)
    build_report(coverage_path, atoms, risks, skipped)

    print(f"Wrote evidence atoms: {atoms_path}")
    print(f"Wrote risk inventory: {risks_path}")
    print(f"Wrote coverage report: {coverage_path}")
    print(f"Atoms: {len(atoms)}")
    print(f"Risk rows: {len(risks)}")
    return 2 if risks else 0


if __name__ == "__main__":
    raise SystemExit(main())
