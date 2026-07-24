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

import argparse
import csv
import importlib.util
import glob
import os
import sys
from pathlib import Path

SOW_COMMON_PATH = Path(__file__).resolve().parents[1] / "scope_of_work" / "common.py"
_spec = importlib.util.spec_from_file_location("chirality_scope_of_work_common", SOW_COMMON_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load Scope-of-Work common module: {SOW_COMMON_PATH}")
_common = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _common
_spec.loader.exec_module(_common)
resolve_production_format = _common.resolve_production_format

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

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execution_root")
    parser.add_argument("output_csv")
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    return parser.parse_args()


def main():
    args = parse_args()
    execution_root = args.execution_root
    output_path = args.output_csv

    deliverables = find_deliverables(execution_root)

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'DeliverableID', 'Package', 'HasDependenciesCsv', 'HasSemantic',
            'HasEstimate', 'EstimateCount', 'HasDatasheet', 'HasSpecification',
            'HasGuidance', 'HasProcedure', 'HasScopeOfWork', 'ProductionFormatState'
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
            has_sow = check_artifact(d['path'], 'ScopeOfWork.md')
            format_state = resolve_production_format(
                Path(d['path']),
                isolated_migration=args.isolated_migration,
                migration_authority=args.migration_authority,
            ).state

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
                'Y' if has_sow else 'N',
                format_state,
            ])

    t = stats['total']
    print(f"Coverage: {t} deliverables")
    print(f"  Dependencies.csv: {stats['has_deps']}/{t}")
    print(f"  _SEMANTIC.md: {stats['has_sem']}/{t}")
    print(f"  Estimates: {stats['has_est']}/{t}")
    print(f"  Doc kit complete: {stats['has_kit']}/{t}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
