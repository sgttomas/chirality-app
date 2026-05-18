#!/usr/bin/env python3
"""Assemble P&ID valve tile stubs into a combined candidate CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from valve_stub_layout import CANDIDATE_COLUMNS, VALVE_SCHEMA_VERSION, parse, validate


def page_numbers(start: int, end: int, pages: str | None) -> list[int]:
    if pages:
        out: list[int] = []
        for part in pages.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                out.extend(range(int(a), int(b) + 1))
            else:
                out.append(int(part))
        return sorted(dict.fromkeys(out))
    return list(range(start, end + 1))


def write_latest_pointer(source_dir: Path, target: str, run_folder: Path, output_csv: Path) -> None:
    pointer = source_dir / "P_AND_ID" / target / "_LATEST.md"
    pointer.parent.mkdir(parents=True, exist_ok=True)
    pointer.write_text(
        "\n".join(
            [
                "# Latest P&ID Valve Candidate Run",
                "",
                f"run_folder: {run_folder}",
                f"combined_csv: {output_csv}",
                f"valve_schema_version: {VALVE_SCHEMA_VERSION}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir", required=True)
    ap.add_argument("--target", choices=["valve_count_basic", "valve_count_detailed"], required=True)
    ap.add_argument("--mode", choices=["basic", "detailed"], required=True)
    ap.add_argument("--pdf-stem", required=True)
    ap.add_argument("--start-page", type=int, required=True)
    ap.add_argument("--end-page", type=int, required=True)
    ap.add_argument("--output-csv", required=True)
    ap.add_argument("--output-md", required=True)
    ap.add_argument("--pages")
    ap.add_argument("--run-folder")
    args = ap.parse_args()

    source_dir = Path(args.source_dir)
    output_csv = Path(args.output_csv)
    output_md = Path(args.output_md)
    run_folder = Path(args.run_folder) if args.run_folder else output_csv.parent
    csv_columns = [
        "valve_schema_version",
        "tile_id",
        "tile_grid",
        "run_status",
        "mode",
        "tag_profile_version",
    ] + list(CANDIDATE_COLUMNS)

    rows: list[dict[str, str]] = []
    missing: list[str] = []
    failures: list[str] = []
    no_findings_reference: list[int] = []
    for page in page_numbers(args.start_page, args.end_page, args.pages):
        pattern = f"{args.pdf_stem}_page_{page:04d}_tile_*_{args.mode}_stub.md"
        stubs = sorted(run_folder.glob(pattern))
        if not stubs:
            missing.append(f"page_{page:04d}")
            continue
        for stub_path in stubs:
            stub = parse(stub_path)
            errors, _warnings = validate(stub)
            if errors:
                failures.extend(f"{stub_path.name}: {error}" for error in errors)
                continue
            if stub.status == "NO_FINDINGS_REFERENCE":
                no_findings_reference.append(page)
            for body_row in stub.rows:
                row = {key: "" for key in csv_columns}
                row.update(
                    {
                        "valve_schema_version": stub.valve_schema_version,
                        "tile_id": stub.tile_id,
                        "tile_grid": stub.tile_grid,
                        "run_status": stub.status,
                        "mode": stub.mode,
                        "tag_profile_version": stub.tag_profile_version,
                    }
                )
                row.update(body_row)
                row["source_page"] = row.get("source_page") or str(stub.source_page)
                row["source_raster_path"] = row.get("source_raster_path") or stub.source_raster_path
                row["tile_id"] = row.get("tile_id") or stub.tile_id
                row["tile_image_path"] = row.get("tile_image_path") or stub.tile_image_path
                row["dwg_no"] = row.get("dwg_no") or stub.dwg_no or "TBD"
                row["system_name"] = row.get("system_name") or stub.system_name or "TBD"
                rows.append(row)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(rows)

    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_md.open("w", encoding="utf-8") as f:
        f.write(f"# P&ID Valve Candidates ({args.mode})\n\n")
        f.write(f"- target: `{args.target}`\n")
        f.write(f"- rows: `{len(rows)}`\n")
        if missing:
            f.write(f"- missing_pages: `{', '.join(missing)}`\n")
        if no_findings_reference:
            pages = ", ".join(str(p) for p in sorted(set(no_findings_reference)))
            f.write(f"- no_findings_reference_pages: `{pages}`\n")
        f.write("\n")
        f.write("| " + " | ".join(csv_columns) + " |\n")
        f.write("| " + " | ".join(["---"] * len(csv_columns)) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(row.get(col, "") for col in csv_columns) + " |\n")

    write_latest_pointer(source_dir, args.target, run_folder, output_csv)
    print(f"rows={len(rows)}")
    print(f"missing_pages={len(missing)}")
    print(f"output_csv={output_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
