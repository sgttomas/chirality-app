#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def flatten(value: Any, prefix: str = "$") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            result.update(flatten(value[key], f"{prefix}.{key}"))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(value):
            result.update(flatten(item, f"{prefix}[{index}]"))
        return result
    return {prefix: value}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare JSON API, schema, or migration artifacts.")
    parser.add_argument("before")
    parser.add_argument("after")
    args = parser.parse_args()
    before = flatten(json.loads(Path(args.before).read_text(encoding="utf-8")))
    after = flatten(json.loads(Path(args.after).read_text(encoding="utf-8")))
    report = {
        "schema": "chirality-structured-comparison/v1",
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "changed": [
            {"path": key, "before": before[key], "after": after[key]}
            for key in sorted(set(before) & set(after)) if before[key] != after[key]
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
