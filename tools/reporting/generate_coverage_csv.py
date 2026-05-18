#!/usr/bin/env python3
"""
generate_coverage_csv.py
Cross-references a deliverable list against found artifacts to produce Coverage.csv.
Reports which deliverables have estimates, dependencies, or other expected artifacts.

Usage:
    python3 generate_coverage_csv.py <EXECUTION_ROOT> <output_csv> [--artifact <pattern>]

Artifacts checked by default:
    - Dependencies.csv (in deliverable folder)
    - _SEMANTIC.md (in deliverable folder)
    - Estimate snapshot (EST_{DEL_ID}_* in _Estimates/)

Example:
    python3 generate_coverage_csv.py ./execution ./Coverage.csv
    python3 generate_coverage_csv.py ./execution ./Coverage.csv --artifact "Detail.csv"
"""

import csv
import glob
import os
import sys

def find_deliverables(execution_root):
    """Find all DEL-* folders under PKG-*/1_Working/."""
    pattern = os.path.join(execution_root, "PKG-*", "1_Working", "DEL-*")
    results = []
    for path in sorted(glob.glob(pattern)):
        if os.path.isdir(path):
            folder_name = os.path.basename(path)
            del_id = folder_name.split('_')[0]
            pkg_folder = os.path.basename(os.path.dirname(os.path.dirname(path)))
            results.append({
                'del_id': del_id,
                'folder_name': folder_name,
                'path': path,
                'pkg': pkg_folder,
            })
    return results

def check_artifact(del_path, filename):
    """Check if an artifact exists in the deliverable folder."""
    return os.path.isfile(os.path.join(del_path, filename))

def check_estimate(execution_root, del_id):
    """Check if an estimate snapshot exists for this deliverable."""
    pattern = os.path.join(execution_root, "_Estimates", f"EST_{del_id}_*")
    matches = glob.glob(pattern)
    return len(matches) > 0, len(matches)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <EXECUTION_ROOT> <output_csv>", file=sys.stderr)
        sys.exit(1)

    execution_root = sys.argv[1]
    output_path = sys.argv[2]

    deliverables = find_deliverables(execution_root)

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'DeliverableID', 'Package', 'HasDependenciesCsv', 'HasSemantic',
            'HasEstimate', 'EstimateCount', 'HasDatasheet', 'HasSpecification',
            'HasGuidance', 'HasProcedure'
        ])

        stats = {'total': 0, 'has_deps': 0, 'has_sem': 0, 'has_est': 0, 'has_kit': 0}

        for d in deliverables:
            stats['total'] += 1
            has_deps = check_artifact(d['path'], 'Dependencies.csv')
            has_sem = check_artifact(d['path'], '_SEMANTIC.md')
            has_est, est_count = check_estimate(execution_root, d['del_id'])
            has_ds = check_artifact(d['path'], 'Datasheet.md')
            has_sp = check_artifact(d['path'], 'Specification.md')
            has_gu = check_artifact(d['path'], 'Guidance.md')
            has_pr = check_artifact(d['path'], 'Procedure.md')

            if has_deps: stats['has_deps'] += 1
            if has_sem: stats['has_sem'] += 1
            if has_est: stats['has_est'] += 1
            if has_ds and has_sp and has_gu and has_pr: stats['has_kit'] += 1

            writer.writerow([
                d['del_id'], d['pkg'],
                'Y' if has_deps else 'N',
                'Y' if has_sem else 'N',
                'Y' if has_est else 'N',
                est_count,
                'Y' if has_ds else 'N',
                'Y' if has_sp else 'N',
                'Y' if has_gu else 'N',
                'Y' if has_pr else 'N',
            ])

    t = stats['total']
    print(f"Coverage: {t} deliverables")
    print(f"  Dependencies.csv: {stats['has_deps']}/{t}")
    print(f"  _SEMANTIC.md: {stats['has_sem']}/{t}")
    print(f"  Estimates: {stats['has_est']}/{t}")
    print(f"  Doc kit complete: {stats['has_kit']}/{t}")
