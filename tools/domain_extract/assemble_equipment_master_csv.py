#!/usr/bin/env python3
"""assemble_equipment_master_csv.py

Assemble per-KTY Equipment Extract markdown files into a single
Equipment_Master_List.csv.

Reads all *_Equipment_Extract.md files from a source directory, parses
the markdown equipment tables, and outputs a consolidated CSV.

Usage:
    python3 assemble_equipment_master_csv.py <source_dir> <output_csv>

Inputs:
    source_dir  — directory containing KTY-*_Equipment_Extract.md files
    output_csv  — path to write the consolidated CSV

Outputs:
    CSV with columns: Source_KTY, Source_KA, Equipment_Tag, Equipment_Name,
                      Package_Name, Notes

Rows are ordered by source file name (KTY ID sort), then by row number
within each file. KTYs with zero equipment (empty tables) are silently
skipped — they produce no CSV rows.
"""

import csv
import os
import re
import sys


def parse_equipment_table(filepath):
    """Parse the Equipment Table from a markdown extract file.

    Returns a list of dicts with keys matching the CSV columns.
    """
    rows = []
    in_table = False
    header_seen = False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # Detect start of Equipment Table section
            if stripped.startswith("## Equipment Table"):
                in_table = True
                header_seen = False
                continue

            # Detect end of table (next section or end of file)
            if in_table and stripped.startswith("## ") and not stripped.startswith("## Equipment Table"):
                break

            if not in_table:
                continue

            # Skip non-table lines
            if not stripped.startswith("|"):
                continue

            # Parse table row
            cells = [c.strip() for c in stripped.split("|")]
            # split on | gives empty strings at start/end
            cells = [c for c in cells if c != "" or c == ""]
            # Remove empty leading/trailing from split
            if stripped.startswith("|"):
                cells = stripped.split("|")[1:-1]
                cells = [c.strip() for c in cells]

            if not cells:
                continue

            # Skip separator rows (|---|---|...)
            if all(re.match(r"^-+$", c.strip()) for c in cells if c.strip()):
                header_seen = True
                continue

            # Skip header row (first row with text before separator)
            if not header_seen:
                # This is the header row
                continue

            # Skip explanatory rows (e.g., "— | — | — | —")
            if cells and cells[0].strip() in ("—", "-", ""):
                continue

            # We expect 8 columns: #, CAT, KTY, KA Source, Equipment Tag, Equipment Name, Package Name, Notes
            if len(cells) >= 7:
                row = {
                    "Source_KTY": cells[2].strip() if len(cells) > 2 else "",
                    "Source_KA": cells[3].strip() if len(cells) > 3 else "",
                    "Equipment_Tag": cells[4].strip() if len(cells) > 4 else "",
                    "Equipment_Name": cells[5].strip() if len(cells) > 5 else "",
                    "Package_Name": cells[6].strip() if len(cells) > 6 else "",
                    "Notes": cells[7].strip() if len(cells) > 7 else "",
                }
                # Skip rows where equipment name is empty or placeholder
                if row["Equipment_Name"] and row["Equipment_Name"] not in ("—", "-"):
                    rows.append(row)

    return rows


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_csv>", file=sys.stderr)
        sys.exit(1)

    source_dir = sys.argv[1]
    output_csv = sys.argv[2]

    if not os.path.isdir(source_dir):
        print(f"ERROR: Source directory not found: {source_dir}", file=sys.stderr)
        sys.exit(1)

    # Find all equipment extract files, sorted by name
    extract_files = sorted(
        f for f in os.listdir(source_dir)
        if f.endswith("_Equipment_Extract.md")
    )

    if not extract_files:
        print(f"WARNING: No *_Equipment_Extract.md files found in {source_dir}", file=sys.stderr)

    all_rows = []
    files_parsed = 0
    files_with_equipment = 0

    for filename in extract_files:
        filepath = os.path.join(source_dir, filename)
        rows = parse_equipment_table(filepath)
        files_parsed += 1
        if rows:
            files_with_equipment += 1
            all_rows.extend(rows)

    # Write CSV
    fieldnames = ["Source_KTY", "Source_KA", "Equipment_Tag", "Equipment_Name", "Package_Name", "Notes"]

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Files parsed: {files_parsed}")
    print(f"Files with equipment: {files_with_equipment}")
    print(f"Total equipment rows: {len(all_rows)}")
    print(f"Output: {output_csv}")


if __name__ == "__main__":
    main()
