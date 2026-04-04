#!/usr/bin/env python3
"""
backfill_stub_system_names.py
Insert or update `- System name:` metadata in page-level drawing extraction stubs
and normalize findings tables to include the `system_name` column.

Usage:
    python3 backfill_stub_system_names.py <source_dir> <system_names_csv> --pdf-stem STEM --start-page 7 --end-page 61
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def load_system_names(path: Path) -> dict[int, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "page" not in reader.fieldnames or "system_name" not in reader.fieldnames:
            raise ValueError("system_names_csv must contain page and system_name columns")

        result: dict[int, str] = {}
        for record in reader:
            page_raw = (record.get("page") or "").strip()
            system_name = (record.get("system_name") or "").strip()
            if not page_raw:
                continue
            result[int(page_raw)] = system_name
        return result


def upsert_system_name(stub_text: str, system_name: str) -> str:
    lines = stub_text.splitlines()
    system_line = f"- System name: `{system_name}`"

    for index, line in enumerate(lines):
        if line.startswith("- System name: "):
            lines[index] = system_line
            return "\n".join(lines) + "\n"

    for index, line in enumerate(lines):
        if line.startswith("- DWG NO.: "):
            lines.insert(index + 1, system_line)
            return "\n".join(lines) + "\n"

    for index, line in enumerate(lines):
        if line.startswith("- Source page: "):
            lines.insert(index + 1, system_line)
            return "\n".join(lines) + "\n"

    lines.append(system_line)
    return "\n".join(lines) + "\n"


def normalize_table(stub_text: str, system_name: str) -> str:
    lines = stub_text.splitlines()
    normalized: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.startswith("| equipment_number | equipment_name | system_name | drawing |"):
            normalized.append(line)
            index += 1
            continue

        if line.startswith("| equipment_number | equipment_name | drawing |"):
            normalized.append("| equipment_number | equipment_name | system_name | drawing |")
            index += 1
            continue

        if line.startswith("| --- | --- | --- | --- |"):
            normalized.append(line)
            index += 1
            continue

        if line.startswith("| --- | --- | --- |"):
            normalized.append("| --- | --- | --- | --- |")
            index += 1
            continue

        if line.startswith("| "):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) == 4:
                normalized.append(line)
                index += 1
                continue
            if len(parts) == 3:
                normalized.append(f"| {parts[0]} | {parts[1]} | {system_name} | {parts[2]} |")
                index += 1
                continue

        normalized.append(line)
        index += 1

    return "\n".join(normalized) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill system-name metadata into page-level equipment stubs.")
    parser.add_argument("source_dir")
    parser.add_argument("system_names_csv")
    parser.add_argument("--pdf-stem", required=True)
    parser.add_argument("--start-page", required=True, type=int)
    parser.add_argument("--end-page", required=True, type=int)
    args = parser.parse_args()

    if args.start_page > args.end_page:
        print("ERROR: --start-page must be <= --end-page", file=sys.stderr)
        return 2

    source_dir = Path(args.source_dir).resolve()
    system_names_csv = Path(args.system_names_csv).resolve()

    if not source_dir.is_dir():
        print(f"ERROR: source directory not found: {source_dir}", file=sys.stderr)
        return 2
    if not system_names_csv.is_file():
        print(f"ERROR: system_names_csv not found: {system_names_csv}", file=sys.stderr)
        return 2

    try:
        system_names = load_system_names(system_names_csv)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    updated = 0
    missing_pages: list[int] = []
    blank_system_pages: list[int] = []

    for page_num in range(args.start_page, args.end_page + 1):
        stub_path = source_dir / f"{args.pdf_stem}_page_{page_num:04d}_equipment_stub.md"
        if not stub_path.is_file():
            missing_pages.append(page_num)
            continue

        system_name = system_names.get(page_num, "").strip()
        if not system_name:
            blank_system_pages.append(page_num)
            continue

        original = stub_path.read_text(encoding="utf-8")
        revised = upsert_system_name(original, system_name)
        revised = normalize_table(revised, system_name)
        if revised != original:
            stub_path.write_text(revised, encoding="utf-8")
            updated += 1

    print(f"updated={updated}")
    print(f"missing_pages={','.join(str(p) for p in missing_pages) or 'none'}")
    print(f"blank_system_pages={','.join(str(p) for p in blank_system_pages) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
