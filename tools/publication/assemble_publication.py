#!/usr/bin/env python3
"""
assemble_publication.py — Deterministic package assembler for DBM publication.

Writes:
  - Rewritten_DBM.md
  - Trace_Appendix.md
  - Publication_Manifest.md
  - Publication_QA.md

Optional hypergraph metadata (AUXILIARY_STRUCTURE_EVIDENCE):
  When the frozen input manifest declares a non-NONE hypergraph use mode,
  the publication manifest includes a supplementary metadata section
  recording: whether hypergraph evidence was used, which snapshot was
  admitted, and whether hypergraph QA was binding or advisory.  No
  authority change is implied — the assembler's write scope is unchanged.

Scope boundary:
  Reads: publication-root, input-manifest, schema, section-map, rules, sections-root
  Writes: only files under --output-dir, plus optional _LATEST.md when explicitly requested
  Does not: modify section outputs, planning artifacts, or inputs

Inputs:
  --publication-root  Publication tool root (_Publication/DBM)
  --input-manifest    Frozen Publication_Input_Manifest.md
  --schema            Approved Publication_Schema.md
  --section-map       Approved Section_Map.csv
  --rules             Approved Publication_Rules.md
  --sections-root     Root containing per-section output folders
  --output-dir        Immutable package snapshot folder to write into
  [--latest-pointer]  Optional _LATEST.md path to overwrite (disabled by default)

Exit codes:
  0 = success, no blocking completeness findings
  1 = fatal input / parsing error
  2 = outputs written, but blocking completeness / trace findings remain

Example:
  python3 tools/publication/assemble_publication.py \
    --publication-root /repo/.../_Publication/DBM \
    --input-manifest /repo/.../_Planning/Publication_Input_Manifest.md \
    --schema /repo/.../_Planning/Publication_Schema.md \
    --section-map /repo/.../_Planning/Section_Map.csv \
    --rules /repo/.../_Planning/Publication_Rules.md \
    --sections-root /repo/.../_Publication/DBM/sections \
    --output-dir /repo/.../_Publication/DBM/package/RUN-20260418-120000
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import parse_manifest, parse_schema, read_csv_rows  # type: ignore


TOP_SOURCE_RE = re.compile(r"^\s*(?:\*\*Source:\*\*|Source:)\s*(.+?)\s*$")
REFERENCES_HEADING_RE = re.compile(r"^\s*##\s+References\b", re.IGNORECASE)
HEADING_RE = re.compile(r"^\s*#{2,6}\s+")
REFERENCE_BULLET_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")
METADATA_BULLET_RE = re.compile(r"^\s*[-*]\s+\*\*([^*]+?)\*\*\s*:?\s*(.+?)\s*$")
SOURCE_REF_RE = re.compile(r"(?:\*\*Source\s*Ref\*\*\s*\|\s*|Source\s*Ref\s*[:|-]\s*|SourceRef\s*[:|-]\s*)([^|\n]+)")
HBK_RE = re.compile(r"\bHBK-\d+\b")
LINE_REF_ONLY_RE = re.compile(r"^L\d+(?:[–-]L?\d+)?$", re.IGNORECASE)
STRONG_REFERENCE_HINT_RE = re.compile(r"(?:\.md\b|DBM/TOC|_Sources/|§|Section\b|Lines?\b|Line\b|W\d{6}-)", re.IGNORECASE)

PACKAGE_OUTPUT_NAMES = [
    "Rewritten_DBM.md",
    "Trace_Appendix.md",
    "Publication_Manifest.md",
    "Publication_QA.md",
    "Publication_Concordance_Report.md",
    "Publication_Concordance_Findings.csv",
    "Publication_Concordance_Expansion_Candidates.csv",
    "Publication_Readiness.md",
    "Rerun_Recommendations.csv",
]

ASSEMBLY_OUTPUT_NAMES = [
    "Rewritten_DBM.md",
    "Trace_Appendix.md",
    "Publication_Manifest.md",
    "Publication_QA.md",
]


def fatal(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_within(path: Path, root: Path, label: str) -> None:
    """Fail fast if a requested output path escapes the publication tool root."""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fatal(f"{label} must resolve under publication root {root}: {path}")


def fail_if_snapshot_contains_outputs(output_dir: Path) -> None:
    """Preserve immutable package snapshots by refusing to overwrite known outputs."""
    existing = [name for name in PACKAGE_OUTPUT_NAMES if (output_dir / name).exists()]
    if existing:
        fatal(
            "Package snapshot already contains publication outputs; choose a new "
            f"RUN-* output directory. Existing outputs: {', '.join(existing)}"
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fatal(f"File not found: {path}")


def dedupe_preserve_order(items: Sequence[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def clean_provenance_token(token: str) -> str:
    return token.strip().replace("`", "").rstrip(".,;")


def split_pre_references_and_references(lines: Sequence[str]) -> Tuple[List[str], List[str]]:
    pre_references: List[str] = []
    references: List[str] = []
    in_references_block = False

    for line in lines:
        if REFERENCES_HEADING_RE.match(line):
            in_references_block = True
            continue
        if in_references_block:
            if HEADING_RE.match(line):
                break
            references.append(line)
            continue
        pre_references.append(line)
    return pre_references, references


def normalize_metadata_key(raw_key: str) -> str:
    key = raw_key.replace("`", "").replace("*", "").strip().lower()
    key = re.sub(r"\s+", " ", key)
    return key.rstrip(":")


def parse_metadata_fields(lines: Sequence[str]) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        bullet_match = METADATA_BULLET_RE.match(line)
        if bullet_match:
            key = normalize_metadata_key(bullet_match.group(1))
            value = clean_provenance_token(bullet_match.group(2))
            if key and value and key not in fields:
                fields[key] = value
            continue

        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        first_cell = cells[0].replace("-", "").replace(":", "").strip()
        if not first_cell or first_cell.lower() in {"field", "value"}:
            continue
        key = normalize_metadata_key(cells[0])
        value = clean_provenance_token(cells[1])
        if key and value and key not in fields:
            fields[key] = value
    return fields


def is_line_ref_only(token: str) -> bool:
    return bool(LINE_REF_ONLY_RE.fullmatch(token.strip()))


def is_strong_reference(candidate: str) -> bool:
    return bool(STRONG_REFERENCE_HINT_RE.search(candidate))


def combine_source_parts(parts: Sequence[str]) -> str:
    cleaned = [clean_provenance_token(part) for part in parts if part]
    unique = dedupe_preserve_order(cleaned)
    return "; ".join(unique)


def extract_top_level_source(pre_reference_lines: Sequence[str]) -> str:
    for line in pre_reference_lines:
        source_match = TOP_SOURCE_RE.match(line)
        if not source_match:
            continue
        candidate = clean_provenance_token(source_match.group(1))
        if candidate and not is_line_ref_only(candidate):
            return candidate
    return ""


def extract_source_from_metadata(fields: Dict[str, str]) -> str:
    source = fields.get("source")
    if source and not is_line_ref_only(source):
        return source

    source_file = fields.get("source file")
    source_ref = fields.get("source ref") or fields.get("sourceref")
    if source_file and source_ref:
        return combine_source_parts([source_file, source_ref])
    if source_file:
        return source_file
    if source_ref and not is_line_ref_only(source_ref):
        return source_ref

    document = fields.get("document")
    section = fields.get("section")
    source_span = fields.get("source span")
    identification = combine_source_parts([document, section, source_span])
    if identification and not is_line_ref_only(identification):
        return identification
    return ""


def extract_source_from_references(reference_lines: Sequence[str]) -> str:
    candidates: List[str] = []
    for line in reference_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("|"):
            continue
        reference_match = REFERENCE_BULLET_RE.match(line)
        candidate = clean_provenance_token(reference_match.group(1) if reference_match else stripped)
        if candidate:
            candidates.append(candidate)
    for candidate in candidates:
        if is_strong_reference(candidate) and not is_line_ref_only(candidate):
            return candidate
    for candidate in candidates:
        if not is_line_ref_only(candidate):
            return candidate
    return ""


def build_evidence_summary(text: str, canonical_source: str) -> str:
    canonical_upper = canonical_source.upper()
    source_ref_tokens: List[str] = []
    for match in SOURCE_REF_RE.findall(text):
        cleaned = clean_provenance_token(match).rstrip(")")
        if not cleaned:
            continue
        if canonical_upper and cleaned.upper() in canonical_upper:
            continue
        if is_line_ref_only(cleaned):
            source_ref_tokens.append(f"SourceRef: {cleaned}")
        else:
            source_ref_tokens.append(cleaned)

    evidence_bits: List[str] = []
    source_ref_tokens = dedupe_preserve_order(source_ref_tokens)
    if source_ref_tokens:
        preview = ", ".join(source_ref_tokens[:5])
        evidence_bits.append(preview if len(source_ref_tokens) <= 5 else f"{preview}, ...")

    hbk_tokens = [token for token in dedupe_preserve_order(HBK_RE.findall(text)) if token.upper() not in canonical_upper]
    if hbk_tokens:
        preview = ", ".join(hbk_tokens[:5])
        evidence_bits.append(f"HBK: {preview}" if len(hbk_tokens) <= 5 else f"HBK: {preview}, ...")

    return "; ".join(evidence_bits)


def parse_artifact_source_and_evidence(text: str) -> Tuple[str, str]:
    lines = text.splitlines()
    pre_reference_lines, reference_lines = split_pre_references_and_references(lines)
    metadata_fields = parse_metadata_fields(pre_reference_lines)

    canonical_source = extract_top_level_source(pre_reference_lines)
    if not canonical_source:
        canonical_source = extract_source_from_metadata(metadata_fields)
    if not canonical_source:
        canonical_source = extract_source_from_references(reference_lines)

    evidence = build_evidence_summary(text, canonical_source)
    return canonical_source, evidence


def format_source_evidence(source: str, evidence: str) -> str:
    if source and evidence:
        return f"Source: {source}; Evidence: {evidence}"
    if source:
        return f"Source: {source}"
    if evidence:
        return f"Evidence: {evidence}"
    return ""


def load_section_map(path: Path) -> Dict[str, List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(path):
        section_id = row.get("SectionID", "")
        if section_id:
            grouped[section_id].append(row)
    return grouped


def expected_section_files(section_id: str, sections_root: Path) -> Dict[str, Path]:
    section_dir = sections_root / section_id
    return {
        "dir": section_dir,
        "body": section_dir / f"{section_id}.md",
        "qa": section_dir / f"{section_id}_QA.md",
        "assertions": section_dir / f"{section_id}_ASSERTIONS.csv",
    }


def extract_artifact_source_ref(path: Path) -> str:
    if not path.exists() or not path.is_file() or path.suffix.lower() != ".md":
        return ""
    text = read_text(path)
    source, evidence = parse_artifact_source_and_evidence(text)
    return format_source_evidence(source, evidence)


def count_conflicts_in_qa(path: Path) -> int:
    if not path.exists():
        return 0
    text = read_text(path)
    lines = text.splitlines()
    in_conflict_block = False
    count = 0
    header_seen = False
    for line in lines:
        if line.strip().lower().startswith("## "):
            heading = line.strip().lower()
            in_conflict_block = heading == "## conflict register"
            header_seen = False
            continue
        if not in_conflict_block:
            continue
        if line.strip().startswith("|"):
            if "---" in line:
                header_seen = True
                continue
            if header_seen:
                count += 1
    return count


def build_rewritten_dbm(schema_rows: List[Dict[str, str]], sections_root: Path) -> Tuple[str, List[str]]:
    missing_sections: List[str] = []
    parts: List[str] = []
    for section in schema_rows:
        expected = expected_section_files(section["SectionID"], sections_root)
        body_path = expected["body"]
        if not body_path.exists():
            missing_sections.append(section["SectionID"])
            parts.append(
                f"> MISSING SECTION OUTPUT: {section['SectionID']} — {section['SectionTitle']}\n> Expected file: `{body_path}`"
            )
            continue
        parts.append(read_text(body_path).strip())
    document = "\n\n".join(part for part in parts if part).rstrip() + "\n"
    return document, missing_sections


def build_trace_appendix(
    schema_rows: List[Dict[str, str]],
    section_map: Dict[str, List[Dict[str, str]]],
    sections_root: Path,
) -> str:
    summary_lines = [
        "# Trace Appendix",
        "",
        "## Section Summary",
        "",
        "| SectionID | SectionTitle | Mapped KTY Count | Mapped KA Count | Evidence / SourceRef Count | Conflict Count |",
        "|---|---|---:|---:|---:|---:|",
    ]
    detail_lines: List[str] = ["", "## Section Trace Blocks", ""]

    for section in schema_rows:
        section_id = section["SectionID"]
        rows = section_map.get(section_id, [])
        kty_count = len({row.get("KnowledgeTypeID", "") for row in rows if row.get("KnowledgeTypeID", "")})
        ka_rows = [row for row in rows if Path(row.get("ArtifactPath", "")).name.startswith("KA-")]
        source_ref_count = 0
        trace_rows: List[List[str]] = []
        for row in rows:
            artifact_path = Path(row.get("ArtifactPath", ""))
            source_ref = extract_artifact_source_ref(artifact_path)
            if source_ref:
                source_ref_count += 1
            trace_rows.append(
                [
                    row.get("SectionID", ""),
                    row.get("SectionTitle", ""),
                    row.get("KnowledgeTypeID", ""),
                    row.get("SubjectID", ""),
                    row.get("ArtifactPath", ""),
                    row.get("MappingRole", ""),
                    row.get("ContributionScope", ""),
                    source_ref,
                    row.get("SCARefs", ""),
                    row.get("CurrentStateBasis", ""),
                ]
            )
        conflict_count = count_conflicts_in_qa(expected_section_files(section_id, sections_root)["qa"])
        safe_section_title = section["SectionTitle"].replace("|", "\\|")
        summary_lines.append(
            f"| {section_id} | {safe_section_title} | {kty_count} | {len(ka_rows)} | {source_ref_count} | {conflict_count} |"
        )

        detail_lines.extend(
            [
                f"### {section_id} — {section['SectionTitle']}",
                "",
                "| SectionID | SectionTitle | KnowledgeTypeID | SubjectID | ArtifactPath | MappingRole | ContributionScope | SourceRef / Evidence | SCARefs | CurrentStateBasis |",
                "|---|---|---|---|---|---|---|---|---|---|",
            ]
        )
        if trace_rows:
            for values in trace_rows:
                escaped = [value.replace("|", "\\|") if isinstance(value, str) else "" for value in values]
                detail_lines.append("| " + " | ".join(escaped) + " |")
        else:
            safe_section_title = section["SectionTitle"].replace("|", "\\|")
            detail_lines.append(f"| {section_id} | {safe_section_title} | — | — | — | — | — | — | — | — |")
        detail_lines.append("")

    return "\n".join(summary_lines + detail_lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Hypergraph metadata helpers.
#
# The assembler does not change authority — it only records whether
# hypergraph evidence was used, which snapshot was admitted, and whether
# the QA was binding or advisory.  See plan section "Publication Tooling
# Changes / Tool 4".
# ---------------------------------------------------------------------------


def _read_hypergraph_manifest_fields(input_manifest: Path) -> Dict[str, str]:
    """Extract hypergraph-related fields from the frozen input manifest.

    Uses the manifest parser from build_section_map and pulls the explicit
    key-value fields.
    """
    manifest = parse_manifest(input_manifest)
    explicit = manifest.get("explicit", {})
    if not isinstance(explicit, dict):
        return {}
    return {
        "use_mode": explicit.get("HYPERGRAPH_USE_MODE", "NONE"),
        "snapshot_path": explicit.get("HYPERGRAPH_SNAPSHOT_PATH", ""),
        "binding_policy": explicit.get("HYPERGRAPH_QA_BINDING_POLICY", "ADVISORY_ONLY"),
        "qa_verdict": explicit.get("HYPERGRAPH_QA_VERDICT", ""),
        "limitations": explicit.get("HYPERGRAPH_LIMITATIONS", ""),
    }


def _hypergraph_was_used(hg_fields: Dict[str, str]) -> bool:
    """Return True if the manifest declares any non-NONE hypergraph use mode."""
    mode = hg_fields.get("use_mode", "NONE").strip().upper()
    return mode != "" and mode != "NONE"


def _hypergraph_qa_is_binding(hg_fields: Dict[str, str]) -> bool:
    """Return True if hypergraph QA is configured as binding for this run."""
    return hg_fields.get("binding_policy", "").strip().upper() == "BLOCK_ON_BINDING_FAILURE"


def build_publication_manifest(
    publication_root: Path,
    input_manifest: Path,
    schema_path: Path,
    section_map_path: Path,
    rules_path: Path,
    sections_root: Path,
    output_dir: Path,
    hg_fields: Optional[Dict[str, str]] = None,
) -> str:
    files_to_hash = [input_manifest, schema_path, section_map_path, rules_path]
    lines = [
        "# Publication Manifest",
        "",
        f"- PublicationRoot: `{publication_root.resolve()}`",
        f"- InputManifest: `{input_manifest.resolve()}`",
        f"- PublicationSchema: `{schema_path.resolve()}`",
        f"- SectionMap: `{section_map_path.resolve()}`",
        f"- PublicationRules: `{rules_path.resolve()}`",
        f"- SectionsRoot: `{sections_root.resolve()}`",
        f"- PackageOutputDir: `{output_dir.resolve()}`",
        "",
        "## Planning Artifact Hashes",
        "",
        "| Artifact | SHA256 |",
        "|---|---|",
    ]
    for path in files_to_hash:
        lines.append(f"| `{path.name}` | `{sha256_file(path)}` |")
    lines.append("")
    lines.append("## Package Outputs")
    lines.append("")
    for name in PACKAGE_OUTPUT_NAMES:
        lines.append(f"- `{(output_dir / name).resolve()}`")
    lines.append("")

    # --- Hypergraph evidence metadata (AUXILIARY_STRUCTURE_EVIDENCE) -------
    # Records whether hypergraph evidence was used, which snapshot was
    # admitted, and whether QA was binding or advisory.  No authority
    # change is implied.
    if hg_fields is not None and _hypergraph_was_used(hg_fields):
        lines.append("## Auxiliary Structure Evidence — Hypergraph")
        lines.append("")
        lines.append(f"- HypergraphEvidenceUsed: YES")
        lines.append(f"- HypergraphUseMode: {hg_fields.get('use_mode', 'NONE')}")
        lines.append(f"- HypergraphSnapshotPath: `{hg_fields.get('snapshot_path', '')}`")
        lines.append(f"- HypergraphQAVerdict: {hg_fields.get('qa_verdict', '')}")
        binding = "BINDING" if _hypergraph_qa_is_binding(hg_fields) else "ADVISORY_ONLY"
        lines.append(f"- HypergraphQABindingPolicy: {binding}")
        limitations = hg_fields.get("limitations", "")
        lines.append(f"- HypergraphLimitations: {limitations if limitations else 'None disclosed'}")
        lines.append("")
    else:
        lines.append("## Auxiliary Structure Evidence — Hypergraph")
        lines.append("")
        lines.append("- HypergraphEvidenceUsed: NO")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_publication_qa(
    schema_rows: List[Dict[str, str]],
    section_map: Dict[str, List[Dict[str, str]]],
    sections_root: Path,
    missing_sections: List[str],
) -> Tuple[str, List[str]]:
    findings: List[str] = []
    lines = [
        "# Publication QA",
        "",
        "## Deterministic Completeness",
        "",
        "| SectionID | Body | QA | Assertions | Map Rows | Status |",
        "|---|---|---|---|---:|---|",
    ]

    for section in schema_rows:
        section_id = section["SectionID"]
        expected = expected_section_files(section_id, sections_root)
        body_ok = expected["body"].exists()
        qa_ok = expected["qa"].exists()
        assertions_ok = expected["assertions"].exists()
        map_count = len(section_map.get(section_id, []))
        status = "PASS"
        if map_count == 0:
            status = "BLOCK"
            findings.append(f"[{section_id}] Section has no Section_Map.csv rows.")
        if not body_ok or not qa_ok or not assertions_ok:
            status = "BLOCK"
            findings.append(f"[{section_id}] Missing required section outputs (body={body_ok}, qa={qa_ok}, assertions={assertions_ok}).")
        lines.append(
            f"| {section_id} | {'YES' if body_ok else 'NO'} | {'YES' if qa_ok else 'NO'} | {'YES' if assertions_ok else 'NO'} | {map_count} | {status} |"
        )

    lines.extend([
        "",
        "## Trace Coverage",
        "",
        f"- Missing required section bodies: {', '.join(missing_sections) if missing_sections else 'None'}",
        f"- Sections with Section_Map rows: {sum(1 for section_id in [row['SectionID'] for row in schema_rows] if section_map.get(section_id))}",
        "",
        "## Findings",
        "",
    ])
    if findings:
        for finding in findings:
            lines.append(f"- {finding}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n", findings


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_latest_pointer(latest_path: Path, snapshot_dir: Path) -> None:
    content = "\n".join(
        [
            "# Latest Publication Snapshot",
            "",
            f"- Snapshot: `{snapshot_dir.name}/`",
            f"- Path: `{snapshot_dir.resolve()}`",
            "",
        ]
    )
    write_text(latest_path, content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble publication package from approved section outputs.")
    parser.add_argument("--publication-root", required=True)
    parser.add_argument("--input-manifest", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--sections-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--latest-pointer", default="")
    args = parser.parse_args()

    publication_root = Path(args.publication_root).resolve()
    input_manifest = Path(args.input_manifest).resolve()
    schema_path = Path(args.schema).resolve()
    section_map_path = Path(args.section_map).resolve()
    rules_path = Path(args.rules).resolve()
    sections_root = Path(args.sections_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    latest_pointer = Path(args.latest_pointer).resolve() if args.latest_pointer else None

    for path in [publication_root, input_manifest, schema_path, section_map_path, rules_path, sections_root]:
        if not path.exists():
            fatal(f"Required path does not exist: {path}")

    require_within(output_dir, publication_root, "--output-dir")
    if latest_pointer:
        require_within(latest_pointer, publication_root, "--latest-pointer")
    fail_if_snapshot_contains_outputs(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    schema_rows = parse_schema(schema_path)
    section_map = load_section_map(section_map_path)

    # ------------------------------------------------------------------
    # Read optional hypergraph metadata from the input manifest.
    # This is used only to record package-level metadata about whether
    # hypergraph evidence was used.  No authority change.
    # ------------------------------------------------------------------
    hg_fields = _read_hypergraph_manifest_fields(input_manifest)

    rewritten_dbm, missing_sections = build_rewritten_dbm(schema_rows, sections_root)
    trace_appendix = build_trace_appendix(schema_rows, section_map, sections_root)
    publication_manifest = build_publication_manifest(
        publication_root=publication_root,
        input_manifest=input_manifest,
        schema_path=schema_path,
        section_map_path=section_map_path,
        rules_path=rules_path,
        sections_root=sections_root,
        output_dir=output_dir,
        hg_fields=hg_fields,
    )
    publication_qa, findings = build_publication_qa(schema_rows, section_map, sections_root, missing_sections)

    write_text(output_dir / "Rewritten_DBM.md", rewritten_dbm)
    write_text(output_dir / "Trace_Appendix.md", trace_appendix)
    write_text(output_dir / "Publication_Manifest.md", publication_manifest)
    write_text(output_dir / "Publication_QA.md", publication_qa)
    if latest_pointer:
        write_latest_pointer(latest_pointer, output_dir)

    print(f"Wrote package outputs under: {output_dir}")
    print(f"Blocking completeness findings: {len(findings)}")
    if findings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
