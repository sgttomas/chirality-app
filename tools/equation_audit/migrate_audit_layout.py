#!/usr/bin/env python3
"""
One-shot migration tool: relocate legacy equation-audit state from the flat
layout

    <book>/audit/{equations.html, equations.jsonl, verified.json, flagged.json,
                  backcheck.json, *_verified_<TS>.json, *_flagged_<TS>.json,
                  .archive/, ...}

to the versioned-snapshot layout owned by the EQUATION_AUDIT persona

    <book>/audit/equations/
        working/   # mutable, holds live review state
        snapshots/ # populated by Phase 6 closures; empty after migration
        _LATEST.md # pointer to the most recent snapshot; stub after migration

Files moved (when present):
  - equations.html
  - equations.jsonl
  - verified.json
  - flagged.json
  - backcheck.json
  - <anything>_verified_<TS>.json (timestamped browser exports)
  - <anything>_flagged_<TS>.json
  - *.bak siblings of any of the above
  - .archive/ (entire subdirectory, verbatim)

Files left in place (never touched):
  - pages (symlink consumed by both the audit HTML and the DOMAIN_DECOMP HTML)
  - proposals/ (different subsystem; PFD / P&ID proposals)
  - .DS_Store (macOS metadata)
  - the new equations/ directory itself

Idempotence:
  - If equations/working/ already exists and no legacy files remain at the
    top level, the tool exits success with status "already_migrated".
  - If both legacy files AND a non-empty equations/working/ exist, the tool
    fails loudly (refuses to silently merge two states).

Usage:

    python3 tools/equation_audit/migrate_audit_layout.py \\
        --source-audit-dir <path>/_Sources/<book>/audit/ \\
        [--dry-run]

Exits 0 on success or already-migrated, non-zero on validation failure.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


# Files whose names match these patterns are part of the equation-audit state
# and get relocated under equations/working/. Everything else is left alone.
LITERAL_NAMES = {
    "equations.html",
    "equations.jsonl",
    "verified.json",
    "flagged.json",
    "backcheck.json",
}

# <prefix>_verified_<TS>.json and <prefix>_flagged_<TS>.json — browser-exported
# review snapshots. <TS> is the export timestamp; <prefix> is typically the
# book name but the migration tool accepts any prefix.
TIMESTAMPED_EXPORT_RE = re.compile(
    r"^.+_(?:verified|flagged)_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\.json$"
)

# Backup siblings that audit_equations.py / process_flagged.py may have
# produced via atomic-write retries.
BAK_SUFFIX_RE = re.compile(r"\.\d{8}T\d{6}\.bak$")

# Subdirectories that are part of the audit state and should be moved verbatim.
LITERAL_SUBDIRS = {".archive"}

# Subdirectory holding the new layout. If this exists, the source may already
# be partly or fully migrated.
NEW_LAYOUT_DIR = "equations"
NEW_WORKING_DIR = "working"
NEW_SNAPSHOTS_DIR = "snapshots"
LATEST_POINTER = "_LATEST.md"


@dataclass
class MigrationPlan:
    """Inventory of what migrate_audit_layout will move."""

    source_audit_dir: Path
    files_to_move: list[Path] = field(default_factory=list)
    dirs_to_move: list[Path] = field(default_factory=list)
    already_present_in_target: list[Path] = field(default_factory=list)
    unrelated_items: list[Path] = field(default_factory=list)

    @property
    def is_noop(self) -> bool:
        return not self.files_to_move and not self.dirs_to_move


def is_audit_state_file(name: str) -> bool:
    if name in LITERAL_NAMES:
        return True
    if TIMESTAMPED_EXPORT_RE.match(name):
        return True
    # *.bak siblings of any of the above
    if BAK_SUFFIX_RE.search(name):
        return True
    return False


def is_unrelated_top_level(name: str) -> bool:
    """Files / dirs at the top level that the migration must NOT move."""
    if name in {"pages", "proposals", NEW_LAYOUT_DIR}:
        return True
    if name == ".DS_Store":
        return True
    return False


def survey(source_audit_dir: Path) -> MigrationPlan:
    """Walk one <book>/audit/ folder and classify its top-level entries."""

    plan = MigrationPlan(source_audit_dir=source_audit_dir)
    target_working = source_audit_dir / NEW_LAYOUT_DIR / NEW_WORKING_DIR

    for entry in sorted(source_audit_dir.iterdir()):
        name = entry.name

        if is_unrelated_top_level(name):
            # NEW_LAYOUT_DIR is the migration target itself; classify it
            # explicitly rather than lumping it with unrelated items.
            if name != NEW_LAYOUT_DIR:
                plan.unrelated_items.append(entry)
            continue

        if entry.is_dir():
            if name in LITERAL_SUBDIRS:
                if (target_working / name).exists():
                    plan.already_present_in_target.append(entry)
                else:
                    plan.dirs_to_move.append(entry)
            else:
                plan.unrelated_items.append(entry)
            continue

        if not is_audit_state_file(name):
            plan.unrelated_items.append(entry)
            continue

        if (target_working / name).exists():
            plan.already_present_in_target.append(entry)
        else:
            plan.files_to_move.append(entry)

    return plan


def write_latest_pointer(equations_dir: Path) -> None:
    """Create the stub _LATEST.md pointer if it doesn't exist."""
    pointer = equations_dir / LATEST_POINTER
    if pointer.exists():
        return
    pointer.write_text(
        "# Latest equation-audit snapshot\n"
        "\n"
        "(no snapshot yet)\n"
        "\n"
        "This pointer is updated by AGENT_EQUATION_AUDIT Phase 6 closure. "
        "Until the first close, the live state lives under `working/` and "
        "this file records 'no snapshot yet'.\n",
        encoding="utf-8",
    )


def apply_plan(plan: MigrationPlan, dry_run: bool) -> None:
    audit_dir = plan.source_audit_dir
    equations_dir = audit_dir / NEW_LAYOUT_DIR
    working_dir = equations_dir / NEW_WORKING_DIR
    snapshots_dir = equations_dir / NEW_SNAPSHOTS_DIR

    if not dry_run:
        working_dir.mkdir(parents=True, exist_ok=True)
        snapshots_dir.mkdir(parents=True, exist_ok=True)

    for f in plan.files_to_move:
        dest = working_dir / f.name
        if dry_run:
            print(f"  [dry-run] move file: {f} -> {dest}")
            continue
        shutil.move(str(f), str(dest))
        print(f"  moved: {f.name}")

    for d in plan.dirs_to_move:
        dest = working_dir / d.name
        if dry_run:
            print(f"  [dry-run] move dir : {d} -> {dest}")
            continue
        shutil.move(str(d), str(dest))
        print(f"  moved: {d.name}/")

    if not dry_run:
        write_latest_pointer(equations_dir)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--source-audit-dir",
        required=True,
        help="Path to <book>/audit/ (the legacy flat layout root)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without touching the filesystem",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    audit_dir = Path(args.source_audit_dir).resolve()

    if not audit_dir.is_dir():
        print(f"ERROR: not a directory: {audit_dir}", file=sys.stderr)
        return 2

    plan = survey(audit_dir)

    print(f"Source audit dir: {audit_dir}")
    print(f"  files to move : {len(plan.files_to_move)}")
    print(f"  dirs to move  : {len(plan.dirs_to_move)}")
    print(f"  already in target: {len(plan.already_present_in_target)}")
    print(f"  unrelated items (left alone): {len(plan.unrelated_items)}")

    if plan.already_present_in_target:
        # Any name collision between a top-level audit file and one already
        # present under equations/working/ is a data-integrity problem the
        # tool refuses to silently resolve. The two copies may differ and
        # losing either could destroy review state.
        print(
            "\nERROR: collision — these audit-state files exist BOTH at the "
            "top level AND under equations/working/:",
            file=sys.stderr,
        )
        for entry in plan.already_present_in_target:
            print(f"  collision: {entry.name}", file=sys.stderr)
        if plan.files_to_move or plan.dirs_to_move:
            for entry in plan.files_to_move + plan.dirs_to_move:
                print(f"  pending  : {entry.name}", file=sys.stderr)
        print(
            "\nRefusing to overwrite or merge silently. Compare the two copies "
            "manually, delete the obsolete one, then rerun.",
            file=sys.stderr,
        )
        return 3

    if plan.is_noop:
        print("\nNothing to migrate.")
        if (audit_dir / NEW_LAYOUT_DIR / NEW_WORKING_DIR).exists():
            print("status: already_migrated")
            if not args.dry_run:
                write_latest_pointer(audit_dir / NEW_LAYOUT_DIR)
        else:
            print("status: no_legacy_state")
        return 0

    print("\nApplying migration:" if not args.dry_run else "\nDry-run plan:")
    apply_plan(plan, dry_run=args.dry_run)

    if args.dry_run:
        print("\nstatus: dry_run")
    else:
        print("\nstatus: migrated")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
