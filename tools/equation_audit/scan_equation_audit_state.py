#!/usr/bin/env python3
"""
Scan one equation-audit working folder and emit a JSON state summary on
stdout. Used by the EQUATION_AUDIT persona at Gate 0 (resume state) and
Gate 6 (close eligibility).

Inputs:
  --audit-root   Path to <book>/audit/equations/working/ (the post-migration
                 layout). The folder must contain equations.jsonl. Sidecars
                 (verified.json, flagged.json, backcheck.json) are loaded via
                 canonical-else-timestamped-export fallback.

Output (stdout, JSON):
  {
    "total":      <int>,   # equations in equations.jsonl
    "verified":   <int>,   # entries matched against extracted equations
    "flagged":    <int>,
    "backcheck":  <int>,
    "unreviewed": <int>,   # total - (verified ∪ flagged ∪ backcheck)
    "overlaps":   <int>,   # equations that appear in >1 review state
    "per_page": {
       "<page>": {"total": N, "verified": V, "flagged": F,
                  "backcheck": B, "unreviewed": U}
    },
    "audit_root": "<resolved-path>",
    "warnings":  [<str>, ...]   # non-fatal anomalies (orphan sidecar keys, etc.)
  }

Exit codes:
  0  success
  2  --audit-root not a directory
  3  equations.jsonl missing or unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_sidecar(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_sidecar_with_fallback(audit_dir: Path, role: str) -> dict:
    """Read <audit_dir>/<role>.json if non-empty; else fall back to the most
    recent <prefix>_<role>_<timestamp>.json in the same directory."""
    canonical = audit_dir / f"{role}.json"
    data = load_sidecar(canonical)
    if data:
        return data
    candidates = sorted(audit_dir.glob(f"*_{role}_*.json"))
    if candidates:
        return load_sidecar(candidates[-1])
    return {}


def load_equations(jsonl_path: Path) -> list[dict]:
    records = []
    with jsonl_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--audit-root",
        required=True,
        help="Path to <book>/audit/equations/working/",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    audit_root = Path(args.audit_root).resolve()
    if not audit_root.is_dir():
        print(f"ERROR: not a directory: {audit_root}", file=sys.stderr)
        return 2

    jsonl_path = audit_root / "equations.jsonl"
    if not jsonl_path.exists():
        print(f"ERROR: equations.jsonl not found at {jsonl_path}", file=sys.stderr)
        return 3

    equations = load_equations(jsonl_path)
    if not equations:
        print(f"ERROR: equations.jsonl is empty or unparseable at {jsonl_path}", file=sys.stderr)
        return 3

    verified = load_sidecar_with_fallback(audit_root, "verified")
    flagged = load_sidecar_with_fallback(audit_root, "flagged")
    backcheck = load_sidecar_with_fallback(audit_root, "backcheck")

    eq_keys = {f"{e['page']}:{e['hash']}" for e in equations}
    warnings: list[str] = []

    # Orphan keys: sidecar entries whose equation no longer exists in
    # equations.jsonl (typically because the equation was fixed and the
    # hash changed — that key is now stale in the OLD sidecar set).
    for role, sidecar in [("verified", verified), ("flagged", flagged), ("backcheck", backcheck)]:
        orphans = set(sidecar.keys()) - eq_keys
        if orphans:
            warnings.append(
                f"{role}: {len(orphans)} sidecar entries reference equations not in current equations.jsonl "
                f"(stale post-fix or pre-migration drift)"
            )

    # Per-equation classification (intersected with eq_keys)
    v_keys = set(verified) & eq_keys
    f_keys = set(flagged) & eq_keys
    b_keys = set(backcheck) & eq_keys

    overlap_count = 0
    state_per_key: dict[str, set[str]] = {}
    for k in eq_keys:
        states = set()
        if k in v_keys:
            states.add("verified")
        if k in f_keys:
            states.add("flagged")
        if k in b_keys:
            states.add("backcheck")
        if len(states) > 1:
            overlap_count += 1
        state_per_key[k] = states

    unreviewed_count = sum(1 for s in state_per_key.values() if not s)

    per_page = defaultdict(lambda: {"total": 0, "verified": 0, "flagged": 0,
                                    "backcheck": 0, "unreviewed": 0})
    for e in equations:
        page = e["page"]
        key = f"{page}:{e['hash']}"
        bucket = per_page[page]
        bucket["total"] += 1
        states = state_per_key.get(key, set())
        if not states:
            bucket["unreviewed"] += 1
        else:
            for s in states:
                bucket[s] += 1

    summary = {
        "total": len(equations),
        "verified": len(v_keys),
        "flagged": len(f_keys),
        "backcheck": len(b_keys),
        "unreviewed": unreviewed_count,
        "overlaps": overlap_count,
        "per_page": {str(p): per_page[p] for p in sorted(per_page)},
        "audit_root": str(audit_root),
        "warnings": warnings,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
