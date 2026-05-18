#!/usr/bin/env python3
"""Validate P_AND_ID valve tile stubs."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from valve_stub_layout import parse, validate


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate valve tile stubs.")
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--target", required=True, choices=["valve_count_basic", "valve_count_detailed"])
    ap.add_argument("--mode", required=True, choices=["basic", "detailed"])
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--run-folder", required=True)
    ap.add_argument("--warnings-csv", required=True)
    args = ap.parse_args()

    root = Path(args.source_dir).resolve() / "P_AND_ID" / args.target / args.run_folder
    failures: list[str] = []
    warnings: list[dict[str, str]] = []
    checked = 0
    for path in sorted(root.glob(f"{args.pdf_stem}_page_*_tile_*_{args.mode}_stub.md")):
        try:
            model = parse(path)
            if not (args.start_page <= model.source_page <= args.end_page):
                continue
            checked += 1
            errors, warns = validate(model)
            for error in errors:
                failures.append(f"{path.name}: {error}")
            for warning in warns:
                warnings.append({"stub": path.name, "warning": warning})
        except Exception as exc:
            failures.append(f"{path.name}: {exc}")

    warnings_csv = Path(args.warnings_csv).resolve()
    warnings_csv.parent.mkdir(parents=True, exist_ok=True)
    with warnings_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["stub", "warning"])
        writer.writeheader()
        writer.writerows(warnings)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"stubs_checked={checked}")
    print(f"warnings={len(warnings)}")
    print("valve_tile_format=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
