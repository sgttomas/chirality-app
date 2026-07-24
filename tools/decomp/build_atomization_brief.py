#!/usr/bin/env python3
"""Render an INIT-TASK brief for one `domain-source-atomize` dispatch unit.

Mirror of `tools/drawing_extract/build_page_worker_brief.py`. The orchestrator
(DOMAIN_DECOMP at Phase 2) iterates a source's `<book>_dispatch_plan.json` and
calls this tool once per unit_id to render the brief that TASK consumes.

The brief is intentionally narrow: the rich method-level guidance lives in
`skills/domain-source-atomize/{SKILL.md, BRIEF_SCHEMA.md, TOOL_POLICY.md,
QA_CHECKS.md}` (loaded by TASK at dispatch time via the skill-hydration
contract). This tool emits only the runtime parameters (paths, ID ranges,
target sections) and a short defensive CustomInstructions block.

Usage:
  python3 tools/decomp/build_atomization_brief.py \\
      --dispatch-plan <book>_dispatch_plan.json \\
      --unit-id UNIT-PSE-0007 \\
      --md <book>.md \\
      --skeleton <book>_skeleton.json \\
      --asset-manifest <book>_assets_manifest.json \\
      --output-ledger-path /path/to/<book>_dispatch_<unit_id>_atoms.csv \\
      --output-vocab-seed-path /path/to/<book>_dispatch_<unit_id>_vocab.csv \\
      [--scope-path /repo/path/to/quarantined/working/dir] \\
      [--max-atoms N]                  # optional smoke-test bound

The brief is written to stdout.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dispatch-plan", required=True, type=Path)
    p.add_argument("--unit-id", required=True)
    p.add_argument("--md", required=True, type=Path)
    p.add_argument("--skeleton", required=True, type=Path)
    p.add_argument("--asset-manifest", required=True, type=Path)
    p.add_argument("--output-ledger-path", required=True, type=Path)
    p.add_argument("--output-vocab-seed-path", required=True, type=Path)
    p.add_argument("--scope-path", default=None, type=Path,
                   help="Quarantined work folder used as ScopePath in the brief. "
                        "Defaults to the parent of --output-ledger-path.")
    p.add_argument("--source-prefix-map", default=None, type=Path,
                   help="Optional Source_Decomp_Prefix_Map.csv. Defaults to the "
                        "sibling map when --dispatch-plan lives under "
                        "_Decomposition/source_dispatch_plans/.")
    p.add_argument("--max-atoms", type=int, default=None,
                   help="Optional bound for smoke testing")
    return p.parse_args()


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def find_unit(plan: dict, unit_id: str) -> dict | None:
    for u in plan.get("units", []):
        if u.get("unit_id") == unit_id:
            return u
    return None


def infer_source_prefix_map(dispatch_plan: Path) -> Path | None:
    if dispatch_plan.parent.name == "source_dispatch_plans":
        candidate = dispatch_plan.parent.parent / "Source_Decomp_Prefix_Map.csv"
        if candidate.exists():
            return candidate
    return None


def load_source_ref_base(map_path: Path | None, source_name: str) -> tuple[str, str]:
    if map_path is None or not map_path.exists():
        return "", ""
    with map_path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("SourceDocID") == source_name or row.get("SourceName") == source_name:
                return row.get("SourceRefBase", ""), row.get("ReviewHtmlPath", "")
    return "", ""


def load_asset_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()

    for p in (args.dispatch_plan, args.md, args.skeleton, args.asset_manifest):
        if not p.exists():
            return fail(f"missing input: {p}")

    plan = json.loads(args.dispatch_plan.read_text(encoding="utf-8"))
    unit = find_unit(plan, args.unit_id)
    if unit is None:
        return fail(f"unit_id {args.unit_id} not in {args.dispatch_plan}")

    source_name = plan.get("source", args.md.stem)
    source_prefix = plan.get("source_prefix", "")
    target_section_ids = unit.get("target_section_ids", [])
    line_start = unit["line_start"]
    line_end = unit["line_end"]
    est_tokens = unit.get("estimated_md_tokens", 0)
    oversized = unit.get("contains_oversized_section", False)

    scope_path = args.scope_path or args.output_ledger_path.parent
    source_prefix_map = args.source_prefix_map or infer_source_prefix_map(args.dispatch_plan)
    source_ref_base, source_html_path = load_source_ref_base(source_prefix_map, source_name)
    asset_manifest = load_asset_manifest(args.asset_manifest)
    source_components = asset_manifest.get("source_components") or []
    if source_components and not source_html_path:
        source_html_path = asset_manifest.get("source_html_path", "")

    lines = [
        f"PURPOSE: Atomize lines {line_start}..{line_end} of {source_name} "
        f"(dispatch unit {args.unit_id}; ~{est_tokens} estimated MD tokens; "
        f"{len(target_section_ids)} target section{'s' if len(target_section_ids) != 1 else ''})"
        f"{' [oversized — single-section dispatch]' if oversized else ''}",
        "RequestedBy: DOMAIN_DECOMP",
        "ActingSurface: TASK+domain-source-atomize",
        "",
        f"ScopePath: {scope_path}",
        "TaskSkill: domain-source-atomize",
        "",
        "AllowedWriteTargets:",
        f'  - "{args.output_ledger_path}"',
        f'  - "{args.output_vocab_seed_path}"',
        "",
        "RuntimeOverrides:",
        f"  SOURCE_NAME: {source_name}",
        f"  SOURCE_PREFIX: {source_prefix}",
        f"  DISPATCH_UNIT_ID: {args.unit_id}",
        f"  MD_PATH: {args.md.resolve()}",
        f"  LINE_START: {line_start}",
        f"  LINE_END: {line_end}",
        f"  SKELETON_PATH: {args.skeleton.resolve()}",
        f"  ASSET_MANIFEST_PATH: {args.asset_manifest.resolve()}",
    ]
    if source_ref_base:
        lines.append(f"  SOURCE_REF_BASE: {source_ref_base}")
    if source_components:
        lines.append("  SOURCE_REF_MODE: COMPONENT_MAP")
    if source_html_path:
        lines.append(f"  SOURCE_HTML_PATH: {source_html_path}")
    lines += [
        f"  OUTPUT_LEDGER_PATH: {args.output_ledger_path}",
        f"  OUTPUT_VOCAB_SEED_PATH: {args.output_vocab_seed_path}",
        "  TARGET_SECTION_IDS:",
    ]
    for sid in target_section_ids:
        lines.append(f"    - {sid}")
    if args.max_atoms is not None:
        lines.append(f"  MAX_ATOMS: {args.max_atoms}")
    lines += [
        "",
        "CustomInstructions:",
        "  - Read ONLY lines LINE_START..LINE_END of MD_PATH. Atoms whose generated MD evidence line falls outside that range MUST NOT be emitted.",
        "  - Every emitted atom MUST map to one of the TARGET_SECTION_IDS (its SectionID column).",
        "  - LocalSeq is monotonic across atoms in the same dispatch unit. Final stable IDs are NOT assigned here — that is the merge step's responsibility.",
        "  - ContentHash MUST be sha1(UnitStatement)[:12]; this column is load-bearing for dedup and HTML cross-reference.",
        "  - SourceRef is dual. If SOURCE_REF_MODE is COMPONENT_MAP, use ASSET_MANIFEST_PATH source_components to map the generated MD source line back to its original @repo component file line, then cite `@repo/<component_repo_rel_path>:L####|SOURCE_HTML_PATH#<SectionID>`.",
        "  - If SOURCE_REF_BASE is present, use that template by replacing L#### with the source line and <SectionID> with the mapped section. Otherwise use `<book>.md:L####|<book>.html#anchor`.",
        "  - InOutStatus ∈ {IN, OUT, TBD}. Default IN for substantive technical statements; OUT for boilerplate (page-numbers-only, headers-only, copyright matter); TBD for ambiguous content the persona must rule on.",
        "  - Do not invent (AOP-08). If a fact is not in the assigned line range, mark TBD and surface the gap.",
        "  - Vocabulary seeds: append candidate canonical terms with source attribution to OUTPUT_VOCAB_SEED_PATH.",
        "  - Write ONLY to OUTPUT_LEDGER_PATH and OUTPUT_VOCAB_SEED_PATH. No other writes are authorized.",
        "",
        "ExpectedOutputs:",
        f"  - {args.output_ledger_path}",
        f"  - {args.output_vocab_seed_path}",
        "",
    ]

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
