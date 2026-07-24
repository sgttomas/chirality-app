#!/usr/bin/env python3
"""Validate candidate ScopeOfWork.md documents and resolve deliverable format."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import resolve_production_format


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="ScopeOfWork.md or its deliverable directory")
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    deliverable = args.target if args.target.is_dir() else args.target.parent
    resolution = resolve_production_format(
        deliverable,
        isolated_migration=args.isolated_migration,
        migration_authority=args.migration_authority,
    )
    issues = list(resolution.issues)
    if not resolution.valid:
        issues.insert(0, f"format state is {resolution.state}")

    report = {"target": str(args.target), "format": resolution.state, "valid": not issues, "issues": issues}
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(("PASS" if not issues else "FAIL") + f" format={resolution.state} target={args.target}")
        for issue in issues:
            print(f"- {issue}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
