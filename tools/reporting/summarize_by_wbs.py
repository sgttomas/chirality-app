#!/usr/bin/env python3
"""
summarize_by_wbs.py
Groups and sums Amount by WBS fields (PackageID, DeliverableID) from a merged Detail.csv.
Produces Project_Summary_WBS.csv.

Usage:
    python3 summarize_by_wbs.py <input_detail_csv> <output_csv>

Example:
    python3 summarize_by_wbs.py ./Project_Detail.csv ./Project_Summary_WBS.csv
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

    # Detect WBS column names (handle common variants)
    wbs_pkg_names = ['WBS_PackageID', 'FromPackageID', 'PackageID']
    wbs_del_names = ['WBS_DeliverableID', 'FromDeliverableID', 'DeliverableID']
    amount_names = ['Amount', 'Amount_CAD', 'Amount_USD']

    with open(input_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []

        pkg_col = next((c for c in wbs_pkg_names if c in header), None)
        del_col = next((c for c in wbs_del_names if c in header), None)
        amt_col = next((c for c in amount_names if c in header), None)

        if not pkg_col or not del_col or not amt_col:
            print(f"ERROR: Could not find required columns. Found: {header}", file=sys.stderr)
            print(f"  Need one of: {wbs_pkg_names} + {wbs_del_names} + {amount_names}", file=sys.stderr)
            sys.exit(1)

        # Aggregate
        totals = defaultdict(float)  # (pkg, del) -> sum
        pkg_totals = defaultdict(float)  # pkg -> sum

        for row in reader:
            pkg = row.get(pkg_col, '').strip()
            del_id = row.get(del_col, '').strip()
            try:
                amt = float(row.get(amt_col, '0').strip() or '0')
            except ValueError:
                amt = 0.0

            if pkg and del_id:
                totals[(pkg, del_id)] += amt
                pkg_totals[pkg] += amt

    # Write output
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([pkg_col, del_col, amt_col, 'PackageTotal_' + amt_col.split('_')[-1] if '_' in amt_col else 'PackageTotal'])

        for (pkg, del_id) in sorted(totals.keys()):
            writer.writerow([pkg, del_id, f"{totals[(pkg, del_id)]:.2f}", f"{pkg_totals[pkg]:.2f}"])

    total = sum(pkg_totals.values())
    print(f"WBS summary: {len(totals)} deliverables across {len(pkg_totals)} packages. Grand total: {total:.2f}")
