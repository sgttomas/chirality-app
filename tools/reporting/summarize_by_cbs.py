#!/usr/bin/env python3
"""
summarize_by_cbs.py
Groups and sums Amount by CBS (Cost Breakdown Structure) field from a merged Detail.csv.
Produces Project_Summary_CBS.csv.

Usage:
    python3 summarize_by_cbs.py <input_detail_csv> <output_csv>

Example:
    python3 summarize_by_cbs.py ./Project_Detail.csv ./Project_Summary_CBS.csv
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

    cbs_names = ['CBS', 'CBS_Code', 'CostCategory']
    amount_names = ['Amount', 'Amount_CAD', 'Amount_USD']

    with open(input_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []

        cbs_col = next((c for c in cbs_names if c in header), None)
        amt_col = next((c for c in amount_names if c in header), None)

        if not cbs_col or not amt_col:
            print(f"ERROR: Could not find required columns. Found: {header}", file=sys.stderr)
            sys.exit(1)

        totals = defaultdict(float)
        row_counts = defaultdict(int)

        for row in reader:
            cbs = row.get(cbs_col, '').strip() or 'UNCLASSIFIED'
            try:
                amt = float(row.get(amt_col, '0').strip() or '0')
            except ValueError:
                amt = 0.0
            totals[cbs] += amt
            row_counts[cbs] += 1

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([cbs_col, amt_col, 'LineCount'])
        for cbs in sorted(totals.keys()):
            writer.writerow([cbs, f"{totals[cbs]:.2f}", row_counts[cbs]])

    total = sum(totals.values())
    print(f"CBS summary: {len(totals)} categories. Grand total: {total:.2f}")
