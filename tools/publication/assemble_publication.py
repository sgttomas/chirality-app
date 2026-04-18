#!/usr/bin/env python3
"""
assemble_publication.py — Deterministic package assembler for DBM publication.

Consumes approved section outputs plus frozen planning artifacts and writes:
  - Rewritten_DBM.md
  - Trace_Appendix.md
  - Publication_Manifest.md
  - Publication_QA.md
  - optional _LATEST.md pointer preview when explicitly requested

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
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import parse_schema, read_csv_rows  # type: ignore


SECTION_QA_BLOCK_RE = re.compile(r"^##\s+(.*)$", re.MULTILINE)
SOURCE_REF_RE = re.compile(r"(?:\*\*SourceRef\*\*\s*\|\s*|SourceRef\s*[:|-]\s*)([^|\n]+)")
HBK_RE = re.compile(r"\bHBK-\d+\b")

PACKAGE_OUTPUT_NAMES = [
    "Rewritten_DBM.md",
    "Trace_Appendix.md",
    "Publication_Manifest.md",
    "Publication_QA.md",
    "Publication_Concordance_Report.md",
    "Publication_Concordance_Findings.csv",
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
    match = SOURCE_REF_RE.search(text)
    if match:
        return match.group(1).strip()
    evidence = sorted(set(HBK_RE.findall(text[:8000])))
    if evidence:
        preview = ", ".join(evidence[:5])
        return f"Evidence: {preview}" if len(evidence) <= 5 else f"Evidence: {preview}, ..."
    return ""


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


def build_publication_manifest(
    publication_root: Path,
    input_manifest: Path,
    schema_path: Path,
    section_map_path: Path,
    rules_path: Path,
    sections_root: Path,
    output_dir: Path,
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
    for name in ASSEMBLY_OUTPUT_NAMES:
        lines.append(f"- `{(output_dir / name).resolve()}`")
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
