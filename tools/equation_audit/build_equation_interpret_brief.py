#!/usr/bin/env python3
"""
Render a valid INIT-TASK brief for one `equation-flag-interpret` dispatch.

Called once per flagged-equation entry whose `description` is a natural-
language note. Reads the entry from `--flagged-json` by `--equation-hash`,
embeds the original LaTeX and the human's note in the brief, and tells
TASK where to write the interpreted LaTeX.

Inputs:
  --flagged-json     Path to flagged.json containing the entry
  --equation-hash    12-hex hash identifying the entry (matches the key
                     `<page>:<hash>` in flagged.json)
  --output-path      Where the skill writes its result JSON (one per entry)
  --page-image-path  Optional path to the page PNG (visual context for VLM)

Output (stdout): INIT-TASK brief with the canonical fields
  PURPOSE, RequestedBy, ActingSurface, ScopePath, TaskSkill,
  AllowedWriteTargets, RuntimeOverrides, ExpectedOutputs.

The skill is expected to write a small JSON at OUTPUT_PATH with shape:

  {
    "key": "<page>:<hash>",
    "page": <int>,
    "hash": "<12-hex>",
    "current_latex": "<original>",
    "interpreted_latex": "<corrected LaTeX>",
    "source_note": "<original human note>"
  }

The persona later merges this back into flagged.json's `description` field
for that key.

Exit codes:
  0  brief rendered to stdout
  2  inputs invalid (flagged.json missing, hash not found, etc.)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--flagged-json", required=True)
    p.add_argument("--equation-hash", required=True,
                   help="12-hex hash; tool looks up the unique <page>:<hash> entry")
    p.add_argument("--output-path", required=True,
                   help="Where the skill writes its interpreted-LaTeX JSON")
    p.add_argument("--page-image-path", default="",
                   help="Optional page PNG for visual context")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    flagged_path = Path(args.flagged_json).resolve()
    if not flagged_path.exists():
        print(f"ERROR: flagged.json not found: {flagged_path}", file=sys.stderr)
        return 2

    try:
        flagged = json.loads(flagged_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: flagged.json not valid JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(flagged, dict):
        print(f"ERROR: flagged.json top-level must be object", file=sys.stderr)
        return 2

    # Find the unique entry whose key ends in the given hash
    matches = [(k, v) for k, v in flagged.items() if k.endswith(":" + args.equation_hash)]
    if len(matches) == 0:
        print(f"ERROR: no flagged entry with hash {args.equation_hash!r}", file=sys.stderr)
        return 2
    if len(matches) > 1:
        print(f"ERROR: ambiguous — {len(matches)} flagged entries match hash {args.equation_hash!r}", file=sys.stderr)
        return 2
    key, entry = matches[0]

    page = entry["page"]
    current_latex = entry["current_latex"]
    flag_note = entry["description"]
    output_path = Path(args.output_path).resolve()

    lines = [
        f"PURPOSE: Interpret the human's natural-language correction note for the equation on page {page} (hash {args.equation_hash}) and emit a corrected LaTeX expression",
        "RequestedBy: EQUATION_AUDIT",
        "ActingSurface: TASK+equation-flag-interpret",
        "",
        f"ScopePath: {flagged_path.parent}",
        "TaskSkill: equation-flag-interpret",
        "",
        "AllowedWriteTargets:",
        f'  - "{output_path}"',
        "",
        "RuntimeOverrides:",
        f"  EQUATION_KEY: {key}",
        f"  PAGE_NUM: {page}",
        f"  EQUATION_HASH: {args.equation_hash}",
        f"  CURRENT_LATEX: |-",
    ]
    for line in current_latex.splitlines() or [current_latex]:
        lines.append(f"    {line}")
    lines += [
        f"  FLAG_NOTE: |-",
    ]
    for line in flag_note.splitlines() or [flag_note]:
        lines.append(f"    {line}")
    if args.page_image_path:
        lines.append(f"  PAGE_IMAGE_PATH: {Path(args.page_image_path).resolve()}")
    lines += [
        f"  OUTPUT_PATH: {output_path}",
        "",
        "CustomInstructions:",
        "  - Read CURRENT_LATEX and FLAG_NOTE together; the note describes what is wrong with CURRENT_LATEX or how to correct it.",
        "  - Emit ONE corrected LaTeX expression. Do not invent unrelated content; preserve the equation's structure and only apply the note's correction.",
        "  - If PAGE_IMAGE_PATH is provided, use it only to disambiguate symbols when the note is ambiguous.",
        "  - Write a single JSON object to OUTPUT_PATH with keys: key, page, hash, current_latex, interpreted_latex, source_note.",
        "  - If the note is too ambiguous to interpret unambiguously, set interpreted_latex to the empty string and add a 'reason' field; do not guess.",
        "",
        "ExpectedOutputs:",
        f"  - {output_path}",
        "",
    ]

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
