#!/usr/bin/env python3
"""
migrate_csv_assets_to_archive.py

Cleanup utility for the PDF2MD table-handling rework. Walks one source's
public `tables/` directory; for each legacy `.csv` artifact whose paired
`.xlsx` exists, moves the `.csv` into `tables/.archive/`. Refuses to
archive a `.csv` whose `.xlsx` is missing (exit 3) — that gap is a
diagnostic signal the operator must resolve before the migration is safe.

Usage:
    python3 migrate_csv_assets_to_archive.py --tables-dir {ASSETS_ROOT}/tables \
        [--dry-run]

Inputs:
    --tables-dir   Path to the public `tables/` directory containing the
                   legacy `.csv` files and the new `.xlsx` files.
    --dry-run      Optional. Print the plan but do not move anything.

Exit codes:
    0  Migration succeeded (or no work to do); per-file actions reported.
    2  Bad input (directory missing, not a directory, etc.).
    3  Refusal: one or more `.csv` files have no paired `.xlsx`.

Idempotence:
    A second run after a successful first run is a no-op (no `.csv`
    remains outside `.archive/`).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ARCHIVE_DIRNAME = ".archive"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive legacy table CSVs after XLSX migration.")
    parser.add_argument("--tables-dir", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def plan_migration(tables_dir: Path) -> tuple[list[Path], list[Path]]:
    """Return (csvs_to_archive, csvs_missing_xlsx)."""
    csvs_to_archive: list[Path] = []
    csvs_missing_xlsx: list[Path] = []
    for csv_path in sorted(tables_dir.glob("*.csv")):
        xlsx_path = csv_path.with_suffix(".xlsx")
        if xlsx_path.is_file():
            csvs_to_archive.append(csv_path)
        else:
            csvs_missing_xlsx.append(csv_path)
    return csvs_to_archive, csvs_missing_xlsx


def main() -> int:
    args = parse_args()
    tables_dir = Path(args.tables_dir).resolve()
    if not tables_dir.is_dir():
        print(f"ERROR: tables-dir is not a directory: {tables_dir}", file=sys.stderr)
        return 2

    to_archive, missing_xlsx = plan_migration(tables_dir)

    if missing_xlsx:
        print(f"REFUSED: {len(missing_xlsx)} legacy .csv files have no paired .xlsx:")
        for path in missing_xlsx[:50]:
            print(f"  - {path.name}")
        if len(missing_xlsx) > 50:
            print(f"  ... {len(missing_xlsx) - 50} more")
        print("Resolve by re-dispatching the affected tables through the pdf2md-page-assets skill so render_table_xlsx produces the missing .xlsx files, then re-run.")
        return 3

    if not to_archive:
        print(f"no_csvs_to_archive tables_dir={tables_dir}")
        return 0

    archive_dir = tables_dir / ARCHIVE_DIRNAME
    if not args.dry_run:
        archive_dir.mkdir(exist_ok=True)

    for csv_path in to_archive:
        dest = archive_dir / csv_path.name
        if args.dry_run:
            print(f"would_archive {csv_path.name} -> {ARCHIVE_DIRNAME}/{csv_path.name}")
        else:
            shutil.move(str(csv_path), str(dest))
            print(f"archived {csv_path.name} -> {ARCHIVE_DIRNAME}/{csv_path.name}")

    print(f"archived_count={len(to_archive)} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
