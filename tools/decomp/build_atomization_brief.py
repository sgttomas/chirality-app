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
        "  - Read ONLY lines LINE_START..LINE_END of MD_PATH. Atoms whose SourceRef line falls outside that range MUST NOT be emitted.",
        "  - Every emitted atom MUST map to one of the TARGET_SECTION_IDS (its SectionID column).",
        "  - LocalSeq is monotonic across atoms in the same dispatch unit. Final stable IDs are NOT assigned here — that is the merge step's responsibility.",
        "  - ContentHash MUST be sha1(UnitStatement)[:12]; this column is load-bearing for dedup and HTML cross-reference.",
        "  - SourceRef is dual: `<book>.md:L####` (the line in the assembled markdown) and `<book>.html#anchor` (the rendered HTML anchor; the SectionID anchor when no finer-grained anchor applies).",
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
