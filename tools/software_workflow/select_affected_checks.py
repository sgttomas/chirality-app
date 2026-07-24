#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import load_profile, matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Select registered checks from changed paths.")
    parser.add_argument("profile")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    _, profile = load_profile(Path(args.profile))
    selected: set[str] = set(profile.get("always_checks", []))
    reasons: dict[str, list[str]] = {}
    for rule in profile.get("path_rules", []):
        patterns = rule.get("paths", [])
        matched = [path for path in args.paths if matches(path, patterns)]
        if matched:
            for check_id in rule.get("checks", []):
                selected.add(check_id)
                reasons.setdefault(check_id, []).extend(matched)
    unknown = sorted(selected - set(profile.get("checks", {})))
    if unknown:
        raise ValueError(f"profile rules reference unknown checks: {', '.join(unknown)}")
    print(json.dumps({
        "schema": "chirality-affected-checks/v1",
        "paths": args.paths,
        "checks": sorted(selected),
        "reasons": {key: sorted(set(value)) for key, value in sorted(reasons.items())},
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
