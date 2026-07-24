#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


MANIFESTS = {
    "package.json": "node",
    "pyproject.toml": "python",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "pom.xml": "java-maven",
    "build.gradle": "java-gradle",
    "build.gradle.kts": "java-gradle",
}
TEST_PATTERNS = ("test_*.py", "*_test.py", "*.test.ts", "*.test.tsx", "*.spec.ts", "*.spec.tsx")
SKIP_PARTS = {".git", "node_modules", "dist", "build", ".next", "target", ".venv", "venv"}


def visible(path: Path) -> bool:
    return not any(part in SKIP_PARTS for part in path.parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover software manifests and test surfaces.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifests = []
    for name, family in MANIFESTS.items():
        for path in root.rglob(name):
            if path.is_file() and visible(path.relative_to(root)):
                manifests.append({"path": path.relative_to(root).as_posix(), "family": family})
    tests: set[str] = set()
    for pattern in TEST_PATTERNS:
        tests.update(
            path.relative_to(root).as_posix()
            for path in root.rglob(pattern)
            if path.is_file() and visible(path.relative_to(root))
        )
    report = {
        "schema": "chirality-software-discovery/v1",
        "root": str(root),
        "manifests": sorted(manifests, key=lambda item: item["path"]),
        "tests": sorted(tests),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
