#!/usr/bin/env python3
"""Keep the repository's own crates out of the CI Rust dependency cache.

Cargo treats a unit as fresh only when its .fingerprint directory says so. A
crate with no fingerprint must be compiled from the checked-out source, whatever
the file times are. Removing the repository's own units therefore leaves cargo
nothing it could wrongly reuse; third-party units stay, bound to Cargo.lock by
the cache key.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

MANIFEST = Path("app/src-tauri/Cargo.toml")
TARGET = Path("app/src-tauri/target")
PROFILE = "debug"


def own_units(manifest: Path) -> tuple[set[str], set[str]]:
    """Return the repository's package names and crate names from Cargo itself."""
    raw = subprocess.check_output(
        ["cargo", "metadata", "--no-deps", "--format-version", "1", "--offline",
         "--manifest-path", str(manifest)])
    packages = json.loads(raw)["packages"]
    names = {package["name"] for package in packages}
    crates = {target["name"].replace("-", "_")
              for package in packages for target in package["targets"]}
    if not names or not crates:
        raise ValueError("Cargo reported no repository package or target")
    return names, crates


def own_artifacts(profile: Path, packages: set[str], crates: set[str]) -> list[Path]:
    """List output belonging to repository crates; dependencies never match."""
    package = re.compile("(?:" + "|".join(map(re.escape, sorted(packages))) + r")-[0-9a-f]+")
    crate = re.compile("(?:lib)?(?:" + "|".join(map(re.escape, sorted(crates))) + r")-[0-9a-f]+(?:\..*)?")
    found: list[Path] = []
    for folder, pattern in ((".fingerprint", package), ("build", package), ("deps", crate)):
        directory = profile / folder
        if directory.is_dir():
            found += [entry for entry in directory.iterdir() if pattern.fullmatch(entry.name)]
    return found


def remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def prune(manifest: Path, target: Path) -> int:
    """Remove repository crates from target and prove none remain."""
    packages, crates = own_units(manifest)
    profile = target / PROFILE
    found = own_artifacts(profile, packages, crates)
    for path in found:
        remove(path)
    left = own_artifacts(profile, packages, crates)
    if left:
        raise ValueError(f"Repository crates remain in the Rust output: {left}")
    return len(found)


def restored(manifest: Path, target: Path, matched_key: str) -> str:
    """Make restored output safe to build on, or discard all of it.

    A miss or failed restore cannot leave reusable output, and a restore that
    cannot be cleaned cannot be trusted; both become a full build.
    """
    if not matched_key:
        if target.exists():
            shutil.rmtree(target)
        return "No compiled dependencies restored; building everything"
    try:
        removed = prune(manifest, target)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"::warning::Discarding restored Rust output: {exc}")
        if target.exists():
            shutil.rmtree(target)
        return "Restored output could not be cleaned; building everything"
    return f"Restored {matched_key}; removed {removed} repository crate outputs"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("prune", "restored"):
        command = commands.add_parser(name)
        command.add_argument("--manifest-path", type=Path, default=MANIFEST)
        command.add_argument("--target-dir", type=Path, default=TARGET)
        if name == "restored":
            command.add_argument("--matched-key", default="")
    args = parser.parse_args()
    try:
        if args.command == "prune":
            print(f"Removed {prune(args.manifest_path, args.target_dir)} repository crate outputs")
        else:
            print(restored(args.manifest_path, args.target_dir, args.matched_key))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"Rust dependency cache step failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
