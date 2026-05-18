#!/usr/bin/env python3
"""
Schema-validate a flagged.json before process_flagged.py applies its fixes.

The EQUATION_AUDIT persona runs this at Gate 3b: every entry must already
carry LaTeX-shaped corrections, never natural-language notes. Natural-
language notes are converted to LaTeX in Phase 3a by the
`equation-flag-interpret` skill; this validator fails fast if Phase 3a was
skipped or any entry remains as prose.

Inputs:
  --flagged-json  Path to flagged.json (canonical, or a timestamped export)

Output (stdout):
  PASS / FAIL summary with per-entry diagnostics.

Exit codes:
  0  PASS
  1  FAIL (one or more entries failed validation)
  2  Input file missing or not parseable as JSON

Schema (per entry):
  - key:           "<page>:<hash>" where <hash> is 12 hex chars
  - value.page:    int >= 1
  - value.hash:    12 hex chars, matches the key
  - value.current_latex: non-empty str
  - value.description:   non-empty str, must "look like LaTeX" — heuristic
                          described in `is_prose_like`
  - value.flagged_at:    non-empty str (date or timestamp; not format-checked)

Heuristic for "prose-like" descriptions:
  A description is prose-like (and therefore invalid here) iff it contains
  NO backslash commands (`\\<name>`) AND contains >= 3 distinct English
  stop-words. This catches "should be ell not e" while accepting pure
  math expressions like "x = 2 y + 3" or single-symbol corrections.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


KEY_RE = re.compile(r"^(\d+):([0-9a-f]{12})$")
HASH_RE = re.compile(r"^[0-9a-f]{12}$")
LATEX_CMD_RE = re.compile(r"\\[A-Za-z]+")

REQUIRED_KEYS = ("page", "hash", "current_latex", "description", "flagged_at")

ENGLISH_STOP_WORDS = frozenset({
    "the", "is", "of", "and", "a", "to", "in", "that", "with", "by",
    "this", "should", "not", "be", "but", "or", "instead", "for",
    "on", "as", "are", "was", "were", "has", "have", "had", "an",
    "from", "at", "it", "its", "if", "which", "when", "where", "why",
    "wrong", "correct", "needs", "missing", "extra",
})


def is_prose_like(s: str) -> bool:
    """Heuristic prose detection (see module docstring)."""
    if not s.strip():
        return False  # empty is its own failure mode, not prose
    if LATEX_CMD_RE.search(s):
        return False
    words = re.findall(r"[A-Za-z]+", s.lower())
    distinct_stops = {w for w in words if w in ENGLISH_STOP_WORDS}
    return len(distinct_stops) >= 3


def validate_entry(key: str, val: object) -> list[str]:
    errors: list[str] = []

    m = KEY_RE.match(key)
    if not m:
        errors.append(f"key {key!r}: must match '<page>:<12-hex-hash>'")

    if not isinstance(val, dict):
        errors.append(f"key {key!r}: value must be a JSON object, got {type(val).__name__}")
        return errors

    for k in REQUIRED_KEYS:
        if k not in val:
            errors.append(f"key {key!r}: missing required field {k!r}")

    if "page" in val and not (isinstance(val["page"], int) and val["page"] >= 1):
        errors.append(f"key {key!r}: page must be a positive int, got {val['page']!r}")

    if "hash" in val:
        h = val["hash"]
        if not (isinstance(h, str) and HASH_RE.match(h)):
            errors.append(f"key {key!r}: hash must be 12 hex chars, got {h!r}")
        elif m and m.group(2) != h:
            errors.append(f"key {key!r}: hash field {h!r} != hash in key {m.group(2)!r}")

    if "current_latex" in val:
        cl = val["current_latex"]
        if not (isinstance(cl, str) and cl.strip()):
            errors.append(f"key {key!r}: current_latex must be a non-empty str")

    if "description" in val:
        d = val["description"]
        if not isinstance(d, str):
            errors.append(f"key {key!r}: description must be a str, got {type(d).__name__}")
        elif not d.strip():
            errors.append(f"key {key!r}: description must be non-empty")
        elif is_prose_like(d):
            errors.append(
                f"key {key!r}: description appears to be a natural-language note "
                f"({d.strip()[:60]!r}). Run `equation-flag-interpret` skill via TASK "
                f"to convert it to LaTeX before applying fixes."
            )

    if "flagged_at" in val:
        fa = val["flagged_at"]
        if not (isinstance(fa, str) and fa.strip()):
            errors.append(f"key {key!r}: flagged_at must be a non-empty str")

    return errors


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--flagged-json", required=True, help="Path to flagged.json")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.flagged_json).resolve()

    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: not valid JSON: {path}\n  {e}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print(f"ERROR: top-level must be a JSON object, got {type(data).__name__}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for key, val in data.items():
        all_errors.extend(validate_entry(key, val))

    print(f"flagged.json : {path}")
    print(f"entries      : {len(data)}")
    if not all_errors:
        print("status       : PASS")
        return 0

    print(f"status       : FAIL ({len(all_errors)} errors)")
    for err in all_errors:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
