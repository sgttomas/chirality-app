#!/usr/bin/env python3
"""
render_dispatch_briefs.py — Deterministic INIT-TASK brief renderer for DBM publication.

Consumes frozen planning artifacts and emits:
  - one section INIT-TASK brief per approved section,
  - one package INIT-TASK brief for dbm-publish,
  - DISPATCH_INDEX.csv,
  - pre-created section output directories,
  - optional targeted rerender for selected sections.

Inputs:
  --publication-root       Path to {_EXECUTION_ROOT}/_Publication/DBM/
  --input-manifest         Publication_Input_Manifest.md
  --schema                 Publication_Schema.md
  --section-map            Approved Section_Map.csv
  --rules                  Publication_Rules.md
  --concordance-register   Publication_Concordance_Register.csv
  --dispatch-root          dispatch/ output folder
  --sections-root          sections/ output folder
  --package-root           package/ snapshot parent
  --package-snapshot-name  Immutable package snapshot folder name (required for determinism)
  [--skills-root]          Repo skills root (default: {repo}/skills)
  [--section-ids]          Comma/semicolon list of SectionIDs to rerender; default = all
  [--render-package]       yes|no (default yes)

Exit codes:
  0 = success
  1 = fatal input / validation error

Example:
  python3 tools/publication/render_dispatch_briefs.py \
    --publication-root /repo/.../_Publication/DBM \
    --input-manifest /repo/.../_Planning/Publication_Input_Manifest.md \
    --schema /repo/.../_Planning/Publication_Schema.md \
    --section-map /repo/.../_Planning/Section_Map.csv \
    --rules /repo/.../_Planning/Publication_Rules.md \
    --concordance-register /repo/.../_Planning/Publication_Concordance_Register.csv \
    --dispatch-root /repo/.../_Publication/DBM/dispatch \
    --sections-root /repo/.../_Publication/DBM/sections \
    --package-root /repo/.../_Publication/DBM/package \
    --package-snapshot-name RUN-20260418-120000
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_section_map import (  # type: ignore
    find_table_with_columns,
    parse_list_cell,
    parse_manifest,
    parse_markdown_tables,
    parse_schema,
    read_csv_rows,
)

SECTION_BRIEF_NAME_TEMPLATE = "{section_id}_INIT-TASK.md"
PACKAGE_BRIEF_NAME = "DBM_PUBLISH_INIT-TASK.md"
DISPATCH_INDEX_COLUMNS = [
    "DispatchType",
    "RenderMode",
    "SectionID",
    "TaskSkill",
    "BriefPath",
    "ScopePath",
    "PrimaryOutputs",
    "PackageSnapshot",
]


class BriefValidationError(RuntimeError):
    pass


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
    existing = [name for name in PACKAGE_OUTPUT_NAMES if (output_dir / name).exists()]
    if existing:
        fatal(
            "Package snapshot already contains publication outputs; choose a new "
            f"RUN-* snapshot name before rendering the package brief. Existing outputs: {', '.join(existing)}"
        )


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def load_section_map(path: Path) -> Dict[str, List[Dict[str, str]]]:
    rows = read_csv_rows(path)
    grouped: Dict[str, List[Dict[str, str]]] = {}
    for row in rows:
        section_id = row.get("SectionID", "")
        if not section_id:
            continue
        grouped.setdefault(section_id, []).append(row)
    return grouped


def parse_required_brief_fields(brief_schema_path: Path) -> List[str]:
    text = brief_schema_path.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    for table in tables:
        if table and "Field" in table[0] and "Meaning" in table[0]:
            return [row.get("Field", "").strip().strip("`") for row in table if row.get("Field", "").strip()]
    raise BriefValidationError(f"Unable to parse required brief fields from {brief_schema_path}")


def parse_rendered_brief(text: str) -> Dict[str, object]:
    top_level: Dict[str, object] = {}
    runtime: Dict[str, str] = {}
    current_list_name: str | None = None
    in_runtime = False

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        if raw_line.startswith("  ") and in_runtime and ":" in raw_line:
            key, value = raw_line.strip().split(":", 1)
            runtime[key.strip()] = value.strip()
            continue
        if raw_line.startswith("  - ") and current_list_name:
            top_level.setdefault(current_list_name, [])
            top_level[current_list_name].append(raw_line[4:].strip())
            continue
        if raw_line.startswith("- ") and current_list_name:
            top_level.setdefault(current_list_name, [])
            top_level[current_list_name].append(raw_line[2:].strip())
            continue
        if ":" in raw_line:
            key, value = raw_line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "RuntimeOverrides":
                in_runtime = True
                current_list_name = None
                continue
            in_runtime = False
            if value:
                top_level[key] = value
                current_list_name = None
            else:
                top_level[key] = []
                current_list_name = key
            continue
    top_level["RuntimeOverrides"] = runtime
    return top_level


def validate_brief(rendered_text: str, required_fields: Sequence[str]) -> None:
    parsed = parse_rendered_brief(rendered_text)
    for field in required_fields:
        if not field:
            continue
        if field.startswith("RuntimeOverrides."):
            key = field.split(".", 1)[1]
            runtime = parsed.get("RuntimeOverrides", {})
            if not isinstance(runtime, dict) or not runtime.get(key):
                raise BriefValidationError(f"Rendered brief missing required runtime override: {key}")
        else:
            value = parsed.get(field)
            if value is None:
                raise BriefValidationError(f"Rendered brief missing required field: {field}")
            if isinstance(value, list) and not value:
                raise BriefValidationError(f"Rendered brief field '{field}' is empty")
            if isinstance(value, str) and not value.strip():
                raise BriefValidationError(f"Rendered brief field '{field}' is empty")


def render_section_brief(
    section: Dict[str, str],
    section_dir: Path,
    paths: Dict[str, Path],
    source_domain: str,
) -> Tuple[str, Dict[str, str]]:
    section_id = section["SectionID"]
    body_path = section_dir / f"{section_id}.md"
    qa_path = section_dir / f"{section_id}_QA.md"
    assertions_path = section_dir / f"{section_id}_ASSERTIONS.csv"
    max_ka_files = section.get("MaxKAFiles", "") or "0"

    lines = [
        f"PURPOSE: Publish approved rewritten DBM section {section_id}.",
        f"ScopePath: {section_dir.resolve()}/",
        "TaskSkill: dbm-section-publish",
        "AllowedWriteTargets:",
        f"  - {body_path.resolve()}",
        f"  - {qa_path.resolve()}",
        f"  - {assertions_path.resolve()}",
        "RuntimeOverrides:",
        f"  SECTION_ID: {section_id}",
        f"  SECTION_TITLE: {section['SectionTitle']}",
        f"  SECTION_TYPE: {section['SectionType']}",
        f"  SECTION_PURPOSE: {section['SectionPurpose']}",
        f"  SECTION_OUTPUT_PATH: {body_path.resolve()}",
        f"  SECTION_QA_OUTPUT_PATH: {qa_path.resolve()}",
        f"  SECTION_ASSERTIONS_OUTPUT_PATH: {assertions_path.resolve()}",
        f"  PUBLICATION_INPUT_MANIFEST: {paths['input_manifest'].resolve()}",
        f"  PUBLICATION_SCHEMA_PATH: {paths['schema'].resolve()}",
        f"  SECTION_MAP_PATH: {paths['section_map'].resolve()}",
        f"  PUBLICATION_RULES_PATH: {paths['rules'].resolve()}",
        f"  PUBLICATION_CONCORDANCE_REGISTER_PATH: {paths['concordance_register'].resolve()}",
        f"  MAX_KA_FILES: {max_ka_files}",
        f"  SOURCE_DOMAIN: {source_domain}",
        f"  SECTION_ORDER: {section['SectionOrder']}",
        "ExpectedOutputs:",
        f"  - {body_path.resolve()}",
        f"  - {qa_path.resolve()}",
        f"  - {assertions_path.resolve()}",
    ]
    metadata = {
        "body_path": str(body_path.resolve()),
        "qa_path": str(qa_path.resolve()),
        "assertions_path": str(assertions_path.resolve()),
    }
    return "\n".join(lines).rstrip() + "\n", metadata


def render_package_brief(package_snapshot_dir: Path, paths: Dict[str, Path], source_domain: str, run_label: str) -> str:
    outputs = [
        package_snapshot_dir / "Rewritten_DBM.md",
        package_snapshot_dir / "Trace_Appendix.md",
        package_snapshot_dir / "Publication_Manifest.md",
        package_snapshot_dir / "Publication_QA.md",
        package_snapshot_dir / "Publication_Concordance_Report.md",
        package_snapshot_dir / "Publication_Concordance_Findings.csv",
        package_snapshot_dir / "Publication_Readiness.md",
        package_snapshot_dir / "Rerun_Recommendations.csv",
    ]
    lines = [
        "PURPOSE: Assemble the rewritten DBM and classify publication readiness.",
        f"ScopePath: {paths['publication_root'].resolve()}/",
        "TaskSkill: dbm-publish",
        "AllowedWriteTargets:",
    ]
    lines.extend([f"  - {path.resolve()}" for path in outputs])
    lines.extend(
        [
            "RuntimeOverrides:",
            f"  PUBLICATION_ROOT: {paths['publication_root'].resolve()}",
            f"  PUBLICATION_INPUT_MANIFEST: {paths['input_manifest'].resolve()}",
            f"  PUBLICATION_SCHEMA_PATH: {paths['schema'].resolve()}",
            f"  SECTION_MAP_PATH: {paths['section_map'].resolve()}",
            f"  PUBLICATION_RULES_PATH: {paths['rules'].resolve()}",
            f"  PUBLICATION_CONCORDANCE_REGISTER_PATH: {paths['concordance_register'].resolve()}",
            f"  SECTIONS_ROOT: {paths['sections_root'].resolve()}/",
            f"  PACKAGE_OUTPUT_ROOT: {paths['package_root'].resolve()}/",
            f"  RUN_LABEL: {run_label}",
            f"  SOURCE_DOMAIN: {source_domain}",
            "ExpectedOutputs:",
        ]
    )
    lines.extend([f"  - {path.resolve()}" for path in outputs])
    return "\n".join(lines).rstrip() + "\n"


def repo_default_skills_root() -> Path:
    return SCRIPT_DIR.parent.parent / "skills"


def infer_source_domain(section_map_rows: Dict[str, List[Dict[str, str]]], publication_root: Path) -> str:
    for rows in section_map_rows.values():
        for row in rows:
            if row.get("SourceDomain", ""):
                return row["SourceDomain"]
    return publication_root.parent.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deterministic publication INIT-TASK briefs.")
    parser.add_argument("--publication-root", required=True)
    parser.add_argument("--input-manifest", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--section-map", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--concordance-register", required=True)
    parser.add_argument("--dispatch-root", required=True)
    parser.add_argument("--sections-root", required=True)
    parser.add_argument("--package-root", required=True)
    parser.add_argument("--package-snapshot-name", required=True)
    parser.add_argument("--skills-root", default=str(repo_default_skills_root()))
    parser.add_argument("--section-ids", default="")
    parser.add_argument("--render-package", choices=["yes", "no"], default="yes")
    args = parser.parse_args()

    paths = {
        "publication_root": Path(args.publication_root).resolve(),
        "input_manifest": Path(args.input_manifest).resolve(),
        "schema": Path(args.schema).resolve(),
        "section_map": Path(args.section_map).resolve(),
        "rules": Path(args.rules).resolve(),
        "concordance_register": Path(args.concordance_register).resolve(),
        "dispatch_root": Path(args.dispatch_root).resolve(),
        "sections_root": Path(args.sections_root).resolve(),
        "package_root": Path(args.package_root).resolve(),
        "skills_root": Path(args.skills_root).resolve(),
    }

    publication_root = paths["publication_root"]
    for name, path in paths.items():
        if name in {"dispatch_root", "sections_root", "package_root"}:
            continue
        if not path.exists():
            fatal(f"Required path does not exist: {path}")
    for name in ["dispatch_root", "sections_root", "package_root"]:
        argument_name = "--" + name.replace("_", "-")
        require_within(paths[name], publication_root, argument_name)

    schema_rows = parse_schema(paths["schema"])
    section_map_rows = load_section_map(paths["section_map"])
    manifest = parse_manifest(paths["input_manifest"])
    source_domain = infer_source_domain(section_map_rows, paths["publication_root"])

    selected_sections = set(parse_list_cell(args.section_ids)) if args.section_ids else {row["SectionID"] for row in schema_rows}
    missing_from_map = [section["SectionID"] for section in schema_rows if section["SectionID"] in selected_sections and section["SectionID"] not in section_map_rows]
    if missing_from_map:
        fatal(f"Section map has no rows for selected sections: {', '.join(missing_from_map)}")

    section_brief_schema = paths["skills_root"] / "dbm-section-publish" / "BRIEF_SCHEMA.md"
    package_brief_schema = paths["skills_root"] / "dbm-publish" / "BRIEF_SCHEMA.md"
    if not section_brief_schema.exists() or not package_brief_schema.exists():
        fatal("Skill BRIEF_SCHEMA.md files not found under skills root.")
    required_section_fields = parse_required_brief_fields(section_brief_schema)
    required_package_fields = parse_required_brief_fields(package_brief_schema)

    paths["dispatch_root"].mkdir(parents=True, exist_ok=True)
    paths["sections_root"].mkdir(parents=True, exist_ok=True)
    paths["package_root"].mkdir(parents=True, exist_ok=True)
    package_snapshot_dir = paths["package_root"] / args.package_snapshot_name
    require_within(package_snapshot_dir, publication_root, "--package-snapshot-name")
    if args.render_package == "yes":
        fail_if_snapshot_contains_outputs(package_snapshot_dir)
        package_snapshot_dir.mkdir(parents=True, exist_ok=True)

    dispatch_rows: List[Dict[str, str]] = []
    render_mode = "TARGETED" if args.section_ids else "FULL"

    for section in schema_rows:
        section_id = section["SectionID"]
        if section_id not in selected_sections:
            continue
        section_dir = paths["sections_root"] / section_id
        section_dir.mkdir(parents=True, exist_ok=True)
        rendered, metadata = render_section_brief(section, section_dir, paths, source_domain)
        validate_brief(rendered, required_section_fields)
        brief_path = paths["dispatch_root"] / SECTION_BRIEF_NAME_TEMPLATE.format(section_id=section_id)
        brief_path.write_text(rendered, encoding="utf-8")
        dispatch_rows.append(
            {
                "DispatchType": "SECTION",
                "RenderMode": render_mode,
                "SectionID": section_id,
                "TaskSkill": "dbm-section-publish",
                "BriefPath": str(brief_path.resolve()),
                "ScopePath": str(section_dir.resolve()) + "/",
                "PrimaryOutputs": "; ".join([metadata["body_path"], metadata["qa_path"], metadata["assertions_path"]]),
                "PackageSnapshot": args.package_snapshot_name,
            }
        )

    if args.render_package == "yes":
        package_brief = render_package_brief(
            package_snapshot_dir=package_snapshot_dir,
            paths=paths,
            source_domain=source_domain,
            run_label=args.package_snapshot_name,
        )
        validate_brief(package_brief, required_package_fields)
        package_brief_path = paths["dispatch_root"] / PACKAGE_BRIEF_NAME
        package_brief_path.write_text(package_brief, encoding="utf-8")
        dispatch_rows.append(
            {
                "DispatchType": "PACKAGE",
                "RenderMode": render_mode,
                "SectionID": "",
                "TaskSkill": "dbm-publish",
                "BriefPath": str(package_brief_path.resolve()),
                "ScopePath": str(paths["publication_root"].resolve()) + "/",
                "PrimaryOutputs": "; ".join(
                    [
                        str((package_snapshot_dir / "Rewritten_DBM.md").resolve()),
                        str((package_snapshot_dir / "Publication_Readiness.md").resolve()),
                    ]
                ),
                "PackageSnapshot": args.package_snapshot_name,
            }
        )

    index_path = paths["dispatch_root"] / "DISPATCH_INDEX.csv"
    write_csv(index_path, DISPATCH_INDEX_COLUMNS, dispatch_rows)

    print(f"Wrote dispatch index: {index_path}")
    print(f"Rendered dispatch rows: {len(dispatch_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
