#!/usr/bin/env python3
"""
Prune accumulated equation-audit artifacts in one `audit/equations/` root.

Three categories accumulate over time and have no value beyond a recent
window for forensics:

  1. `snapshots/EQ_*/` — one immutable directory per Phase 6 closure
  2. `working/*_verified_*.json`, `*_flagged_*.json`, `*_backcheck_*.json` —
     timestamped browser exports from each review session
  3. `working/*.bak` — archived `flagged.json` backups written each time
     `process_flagged.py` runs

For each category this tool keeps the most recent N entries (default 20)
and deletes the rest. File/directory names embed an ISO-style timestamp
so lexicographic sort matches chronological sort.

What this tool will NEVER touch:
  - `_LATEST.md` pointer at the audit root
  - Live canonical state: `equations.html`, `equations.jsonl`,
    `verified.json`, `flagged.json`, `backcheck.json`
  - Anything *inside* a snapshot directory (snapshots are immutable as
    units; we only delete whole snapshot directories that fall out of
    the keep window)
  - `pages/` symlink, `.archive/`, `proposals/`, or any directory at
    the audit root other than `snapshots/` and `working/`

Idempotent: re-running produces the same state.

Usage:
    python3 tools/equation_audit/prune_old_snapshots.py \\
        --audit-root _Sources/<book>/audit/equations [--keep 20] [--dry-run]
    python3 tools/equation_audit/prune_old_snapshots.py \\
        --audit-root _Sources/<book>/audit/equations --snapshots-only
    python3 tools/equation_audit/prune_old_snapshots.py \\
        --audit-root _Sources/<book>/audit/equations --exports-only

Exit codes:
    0  success (or dry-run completed)
    2  --audit-root missing / not a directory
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

DEFAULT_KEEP = 20

EXPORT_GLOBS = (
    "*_verified_*.json",
    "*_flagged_*.json",
    "*_backcheck_*.json",
)
BAK_GLOB = "*.bak"


def _select_for_prune(entries: list[Path], keep: int) -> tuple[list[Path], list[Path]]:
    """Return (kept, prunable) given a list of paths to consider.

    Entries are sorted by name descending; the first `keep` are kept,
    the rest are returned as prunable.
    """
    sorted_desc = sorted(entries, key=lambda p: p.name, reverse=True)
    return sorted_desc[:keep], sorted_desc[keep:]


def survey(audit_root: Path, keep: int) -> dict:
    """Compute prune plan for one audit/equations/ root.

    Returns a structured dict; never modifies the filesystem.
    """
    plan: dict = {
        "audit_root": str(audit_root),
        "keep": keep,
        "snapshots": {"kept": [], "prunable": []},
        "exports": {"kept": [], "prunable": []},
        "baks": {"kept": [], "prunable": []},
    }

    snapshots_dir = audit_root / "snapshots"
    if snapshots_dir.is_dir():
        snapshot_dirs = [p for p in snapshots_dir.iterdir()
                         if p.is_dir() and p.name.startswith("EQ_")]
        kept, prunable = _select_for_prune(snapshot_dirs, keep)
        plan["snapshots"]["kept"] = [str(p) for p in kept]
        plan["snapshots"]["prunable"] = [str(p) for p in prunable]

    working_dir = audit_root / "working"
    if working_dir.is_dir():
        # Each export glob (verified / flagged / backcheck) keeps its own
        # most-recent-N. We do NOT pool all exports into one global keep window:
        # losing all but one kind would be surprising.
        for glob in EXPORT_GLOBS:
            matches = sorted(working_dir.glob(glob))
            kept, prunable = _select_for_prune(matches, keep)
            plan["exports"]["kept"].extend(str(p) for p in kept)
            plan["exports"]["prunable"].extend(str(p) for p in prunable)

        baks = sorted(working_dir.glob(BAK_GLOB))
        kept, prunable = _select_for_prune(baks, keep)
        plan["baks"]["kept"] = [str(p) for p in kept]
        plan["baks"]["prunable"] = [str(p) for p in prunable]

    plan["totals"] = {
        "snapshots_kept": len(plan["snapshots"]["kept"]),
        "snapshots_prunable": len(plan["snapshots"]["prunable"]),
        "exports_kept": len(plan["exports"]["kept"]),
        "exports_prunable": len(plan["exports"]["prunable"]),
        "baks_kept": len(plan["baks"]["kept"]),
        "baks_prunable": len(plan["baks"]["prunable"]),
    }
    return plan


def _delete(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def execute(plan: dict, *, snapshots_only: bool, exports_only: bool) -> dict:
    """Execute the prune plan; return a result dict with `removed` list."""
    removed: list[str] = []
    if not exports_only:
        for p in plan["snapshots"]["prunable"]:
            _delete(Path(p))
            removed.append(p)
    if not snapshots_only:
        for p in plan["exports"]["prunable"]:
            _delete(Path(p))
            removed.append(p)
        for p in plan["baks"]["prunable"]:
            _delete(Path(p))
            removed.append(p)
    return {"removed": removed, "removed_count": len(removed)}


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-root", required=True,
                    help="path to <book>/audit/equations/ (NOT working/ or snapshots/)")
    ap.add_argument("--keep", type=int, default=DEFAULT_KEEP,
                    help=f"how many most-recent entries to keep per category (default {DEFAULT_KEEP})")
    ap.add_argument("--dry-run", action="store_true",
                    help="report the plan without deleting anything")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--snapshots-only", action="store_true",
                   help="only prune snapshots/, leave working/ exports alone")
    g.add_argument("--exports-only", action="store_true",
                   help="only prune working/ exports + .bak files, leave snapshots/ alone")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    audit_root = Path(args.audit_root).resolve()
    if not audit_root.is_dir():
        print(f"ERROR: --audit-root is not a directory: {audit_root}", file=sys.stderr)
        return 2
    if args.keep < 1:
        print("ERROR: --keep must be >= 1", file=sys.stderr)
        return 2

    plan = survey(audit_root, args.keep)

    if args.dry_run:
        plan["status"] = "dry_run"
        # In dry-run the "removed" list is the plan's "prunable" subset that
        # WOULD be removed given the current --snapshots-only / --exports-only flags.
        would_remove: list[str] = []
        if not args.exports_only:
            would_remove.extend(plan["snapshots"]["prunable"])
        if not args.snapshots_only:
            would_remove.extend(plan["exports"]["prunable"])
            would_remove.extend(plan["baks"]["prunable"])
        plan["would_remove"] = would_remove
        plan["would_remove_count"] = len(would_remove)
        print(json.dumps(plan, indent=2))
        return 0

    result = execute(plan, snapshots_only=args.snapshots_only,
                     exports_only=args.exports_only)
    plan["status"] = "pruned"
    plan["removed"] = result["removed"]
    plan["removed_count"] = result["removed_count"]
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
