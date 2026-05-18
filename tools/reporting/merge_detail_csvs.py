#!/usr/bin/env python3
"""
merge_detail_csvs.py
Merges multiple Detail.csv files into a single Project_Detail.csv,
injecting a SourcePath provenance column.

Usage:
    python3 merge_detail_csvs.py <output_path> <detail_csv_1> [detail_csv_2] ...
    python3 merge_detail_csvs.py <output_path> --glob <pattern>

Example:
    python3 merge_detail_csvs.py ./Project_Detail.csv ./_Estimates/EST_*/Detail.csv
    python3 merge_detail_csvs.py ./Project_Detail.csv --glob "./_Estimates/EST_*/Detail.csv"
"""

import csv
import glob
import os
import sys

def merge_csvs(output_path, csv_paths):
    all_rows = []
    header = None

    for path in sorted(csv_paths):
        if not os.path.isfile(path):
            print(f"WARNING: Skipping non-file: {path}", file=sys.stderr)
            continue

        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            try:
                file_header = next(reader)
            except StopIteration:
                print(f"WARNING: Empty file: {path}", file=sys.stderr)
                continue

            # Strip whitespace
            file_header = [col.strip() for col in file_header]

            if header is None:
                header = file_header
            else:
                # Verify compatible schema
                if file_header != header:
                    # Allow if all required columns present (order may differ)
                    if set(header) != set(file_header):
                        print(f"WARNING: Schema mismatch in {path}", file=sys.stderr)

            for row in reader:
                all_rows.append((path, row))

    if header is None:
        print("ERROR: No valid CSV files found", file=sys.stderr)
        sys.exit(1)

    # Write merged output with SourcePath column
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header + ["SourcePath"])
        for source_path, row in all_rows:
            writer.writerow(row + [source_path])

    print(f"Merged {len(all_rows)} rows from {len(csv_paths)} files → {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <output_path> <csv_1> [csv_2] ...", file=sys.stderr)
        print(f"       {sys.argv[0]} <output_path> --glob <pattern>", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[1]

    if sys.argv[2] == '--glob':
        pattern = sys.argv[3]
        csv_paths = glob.glob(pattern)
    else:
        csv_paths = sys.argv[2:]

    if not csv_paths:
        print("ERROR: No input files specified or matched", file=sys.stderr)
        sys.exit(1)

    merge_csvs(output_path, csv_paths)
