#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from software_workflow_common import contained_path, sha256


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify generated files against recorded SHA-256 digests.")
    parser.add_argument("root")
    parser.add_argument("manifest")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    findings = []
    for relative, expected in sorted(manifest.get("files", {}).items()):
        path = contained_path(root, relative)
        actual = sha256(path) if path.is_file() else None
        if actual != expected:
            findings.append({"path": relative, "expected": expected, "actual": actual})
    report = {
        "schema": "chirality-generated-drift/v1",
        "status": "PASS" if not findings else "FAIL",
        "findings": findings,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
