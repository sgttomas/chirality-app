#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from software_workflow_common import load_profile, matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Select registered checks from changed paths.")
    parser.add_argument("profile")
    parser.add_argument("paths", nargs="*")
    parser.add_argument(
        "--paths-json-stdin",
        action="store_true",
        help="read the changed-path list as a JSON array from standard input",
    )
    args = parser.parse_args()
    paths = list(args.paths)
    if args.paths_json_stdin:
        stdin_paths = json.load(sys.stdin)
        if not isinstance(stdin_paths, list) or not all(
            isinstance(path, str) and path for path in stdin_paths
        ):
            raise ValueError("standard input must be a JSON array of non-empty paths")
        paths.extend(stdin_paths)
    if not paths:
        parser.error("at least one changed path is required")
    _, profile = load_profile(Path(args.profile))
    selected: set[str] = set(profile.get("always_checks", []))
    reasons: dict[str, list[str]] = {}
    for rule in profile.get("path_rules", []):
        patterns = rule.get("paths", [])
        matched = [path for path in paths if matches(path, patterns)]
        if matched:
            for check_id in rule.get("checks", []):
                selected.add(check_id)
                reasons.setdefault(check_id, []).extend(matched)
    unknown = sorted(selected - set(profile.get("checks", {})))
    if unknown:
        raise ValueError(f"profile rules reference unknown checks: {', '.join(unknown)}")
    print(json.dumps({
        "schema": "chirality-affected-checks/v1",
        "paths": paths,
        "checks": sorted(selected),
        "reasons": {key: sorted(set(value)) for key, value in sorted(reasons.items())},
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
