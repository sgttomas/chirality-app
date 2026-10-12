#!/usr/bin/env python3
"""Check the public release projection without importing private project state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "validation"))

from build_workflow_index import validate_and_build

REQUIRED_FILES = (
    "README.md",
    "LICENSE.md",
    "agents/registry.json",
    "workflows/catalog.yaml",
    "workflows/index.json",
    "desktop/package.json",
    "desktop/package-lock.json",
    "desktop/electron/main.ts",
    "desktop/src/app/page.tsx",
    "runtime/package.json",
    "runtime/package-lock.json",
    "runtime/packages/core/src/runtime-service.ts",
)
PRIVATE_PATHS = (
    "projects",
    "execution",
    "domains",
    "exports",
    ".agents/skills/chirality-change",
)


def validate_projection(root: Path) -> dict:
    root = root.resolve()
    for relative in PRIVATE_PATHS:
        path = root / relative
        if path.exists() or path.is_symlink():
            raise ValueError(f"private monorepo path in release projection: {relative}")
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"missing or escaping release-projection file: {relative}")

    index = validate_and_build(root, public_export=True)
    expected = json.dumps(index, indent=2, sort_keys=False) + "\n"
    if (root / "workflows/index.json").read_text(encoding="utf-8") != expected:
        raise ValueError("published workflow index is stale")

    versions = {}
    for workspace in ("desktop", "runtime"):
        package = json.loads((root / workspace / "package.json").read_text())
        lock = json.loads((root / workspace / "package-lock.json").read_text())
        if lock.get("lockfileVersion") != 3 or not isinstance(lock.get("packages"), dict):
            raise ValueError(f"invalid package lock: {workspace}")
        entry = lock["packages"].get("")
        if not isinstance(entry, dict):
            raise ValueError(f"missing root package in lock: {workspace}")
        for key in ("name", "version"):
            if not isinstance(package.get(key), str) or package[key] != lock.get(key) or package[key] != entry.get(key):
                raise ValueError(f"package/lock {key} mismatch: {workspace}")
        for key in ("dependencies", "devDependencies", "optionalDependencies", "workspaces"):
            if package.get(key) != entry.get(key):
                raise ValueError(f"package/lock {key} mismatch: {workspace}")
        versions[workspace] = package["version"]
    return {"status": "PASS", "methods": len(index["methods"]), "sourceVersions": versions}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        print(json.dumps(validate_projection(args.root)))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"release projection error: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
