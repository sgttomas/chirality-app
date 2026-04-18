#!/usr/bin/env python3
# merge_equipment_costing_csv.py
# Merge per-KTY Equipment_Costing_Extract CSV files into a single consolidated CSV.
#
# Usage:
#   python3 tools/reporting/merge_equipment_costing_csv.py OUTPUT_CSV INPUT_DIR [--sort-by COLUMN]
#
# Inputs:
#   OUTPUT_CSV  — path to the consolidated output CSV file
#   INPUT_DIR   — directory containing *_Equipment_Costing_Extract.csv files
#   --sort-by   — optional column name to sort by (default: Equipment_Module_Type)
#
# Outputs:
#   A single CSV file with header row + all data rows from all per-KTY input CSVs,
#   sorted by the specified column. Duplicate headers are removed.
#
# Example:
#   python3 tools/reporting/merge_equipment_costing_csv.py \
#     /path/to/_Aggregation/Equipment_Extract/Equipment_Costing_Extract.csv \
#     /path/to/_Aggregation/Equipment_Extract/ \
#     --sort-by Equipment_Module_Type

import csv
import glob
import os
import sys

EXPECTED_COLUMNS = [
    "Equipment_Module_Type",
    "Match_Quality",
    "Equipment_Instance",
    "Equipment_Tag",
    "Quantity_and_Sparing",
    "Description",
    "Capacity_Throughput",
    "Power_Duty",
    "Size_Dimensions",
    "Design_Pressure",
    "Design_Temperature",
    "Fluid_Process_Service",
    "Subcomponents",
    "Key_Costing_Parameters",
    "Source_KTY",
    "Source_KA_Files",
    "Notes",
]


def main():
    if len(sys.argv) < 3:
        print(
            f"Usage: {sys.argv[0]} OUTPUT_CSV INPUT_DIR [--sort-by COLUMN]",
            file=sys.stderr,
        )
        sys.exit(1)

    output_csv = sys.argv[1]
    input_dir = sys.argv[2]

    sort_by = "Equipment_Module_Type"
    if "--sort-by" in sys.argv:
        idx = sys.argv.index("--sort-by")
        if idx + 1 < len(sys.argv):
            sort_by = sys.argv[idx + 1]

    if not os.path.isdir(input_dir):
        print(f"ERROR: INPUT_DIR does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)

    pattern = os.path.join(input_dir, "*_Equipment_Costing_Extract.csv")
    input_files = sorted(glob.glob(pattern))

    if not input_files:
        print(f"ERROR: No *_Equipment_Costing_Extract.csv files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    all_rows = []
    files_read = 0
    schema_errors = []

    for filepath in input_files:
        basename = os.path.basename(filepath)
        try:
            with open(filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    schema_errors.append(f"{basename}: empty or unreadable")
                    continue

                missing = [c for c in EXPECTED_COLUMNS if c not in reader.fieldnames]
                if missing:
                    schema_errors.append(f"{basename}: missing columns {missing}")
                    continue

                row_count = 0
                for row in reader:
                    all_rows.append(row)
                    row_count += 1

                files_read += 1
                print(f"  {basename}: {row_count} rows", file=sys.stderr)

        except Exception as e:
            schema_errors.append(f"{basename}: read error: {e}")

    if schema_errors:
        print(f"\nSchema errors ({len(schema_errors)}):", file=sys.stderr)
        for err in schema_errors:
            print(f"  {err}", file=sys.stderr)

    if sort_by in EXPECTED_COLUMNS:
        all_rows.sort(key=lambda r: r.get(sort_by, ""))

    output_dir = os.path.dirname(output_csv)
    if output_dir and not os.path.isdir(output_dir):
        print(f"ERROR: Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(
        f"\nMerged {len(all_rows)} rows from {files_read} files into {output_csv}",
        file=sys.stderr,
    )

    if schema_errors:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
