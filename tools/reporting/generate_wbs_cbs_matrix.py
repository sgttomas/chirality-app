#!/usr/bin/env python3
"""
generate_wbs_cbs_matrix.py
Pivots a merged Detail.csv into a WBS (Package) x CBS cost matrix.
Produces Project_WBS_CBS_Matrix.csv.

Usage:
    python3 generate_wbs_cbs_matrix.py <input_detail_csv> <output_csv>

Example:
    python3 generate_wbs_cbs_matrix.py ./Project_Detail.csv ./Project_WBS_CBS_Matrix.csv
"""

import csv
import sys
from collections import defaultdict

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_detail_csv> <output_csv>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    pkg_names = ['WBS_PackageID', 'FromPackageID', 'PackageID']
    cbs_names = ['CBS', 'CBS_Code', 'CostCategory']
    amount_names = ['Amount', 'Amount_CAD', 'Amount_USD']

    with open(input_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []

        pkg_col = next((c for c in pkg_names if c in header), None)
        cbs_col = next((c for c in cbs_names if c in header), None)
        amt_col = next((c for c in amount_names if c in header), None)

        if not pkg_col or not cbs_col or not amt_col:
            print(f"ERROR: Could not find required columns. Found: {header}", file=sys.stderr)
            sys.exit(1)

        # Build pivot: matrix[pkg][cbs] = sum
        matrix = defaultdict(lambda: defaultdict(float))
        all_cbs = set()

        for row in reader:
            pkg = row.get(pkg_col, '').strip() or 'UNKNOWN'
            cbs = row.get(cbs_col, '').strip() or 'UNCLASSIFIED'
            try:
                amt = float(row.get(amt_col, '0').strip() or '0')
            except ValueError:
                amt = 0.0
            matrix[pkg][cbs] += amt
            all_cbs.add(cbs)

    cbs_sorted = sorted(all_cbs)
    pkgs_sorted = sorted(matrix.keys())

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([pkg_col] + cbs_sorted + ['RowTotal'])
        for pkg in pkgs_sorted:
            row = [pkg]
            row_total = 0.0
            for cbs in cbs_sorted:
                val = matrix[pkg][cbs]
                row.append(f"{val:.2f}")
                row_total += val
            row.append(f"{row_total:.2f}")
            writer.writerow(row)

        # Column totals
        col_totals = ['TOTAL']
        grand = 0.0
        for cbs in cbs_sorted:
            ct = sum(matrix[p][cbs] for p in pkgs_sorted)
            col_totals.append(f"{ct:.2f}")
            grand += ct
        col_totals.append(f"{grand:.2f}")
        writer.writerow(col_totals)

    print(f"WBS x CBS matrix: {len(pkgs_sorted)} packages x {len(cbs_sorted)} CBS categories. Grand total: {grand:.2f}")
