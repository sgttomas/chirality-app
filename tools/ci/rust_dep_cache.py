#!/usr/bin/env python3
"""Keep the repository's own crates out of the CI Rust dependency cache.

Cargo treats a unit as fresh only when its fingerprint directory says so. A
crate with no fingerprint must be compiled from the checked-out source, whatever
the file times are. Removing the repository's own units therefore leaves cargo
nothing it could wrongly reuse; third-party units stay, bound to Cargo.lock by
the cache key.

Cargo's output layout is not a stable interface. Two are known here: before
Cargo 1.100, `.fingerprint/<package>-<hash>`, `build/<package>-<hash>` and
`deps/<crate>-<hash>*`; from 1.100, everything of a package under
`build/<package>/<hash>/`. Output in any other shape is refused, never passed
as clean.
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
CACHED_FOLDERS = (".fingerprint", "build", "deps")


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
    # Cargo 1.100 and later: one folder per package, named exactly as the package.
    build = profile / "build"
    if build.is_dir():
        found += [entry for entry in build.iterdir() if entry.name in packages]
    return found


def unit_fingerprints(profile: Path) -> list[Path]:
    """Every compiled unit's fingerprint folder, under either known layout."""
    found: list[Path] = []
    before_1_100 = profile / ".fingerprint"
    if before_1_100.is_dir():
        found += list(before_1_100.iterdir())
    build = profile / "build"
    if build.is_dir():
        found += [path for path in build.glob("*/*/fingerprint") if path.is_dir()]
    return found


def unrecognised_output(profile: Path) -> bool:
    """Compiled output is there, and no unit in it is where either layout puts one."""
    holds_output = any(directory.is_dir() and any(directory.iterdir())
                       for directory in (profile / name for name in CACHED_FOLDERS))
    return holds_output and not unit_fingerprints(profile)


def remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def prune(manifest: Path, target: Path) -> int:
    """Remove repository crates from target and prove none remain."""
    packages, crates = own_units(manifest)
    profile = target / PROFILE
    if unrecognised_output(profile):
        raise ValueError(f"Rust output under {profile} is not in a layout this tool knows; "
                         "repository crates in it cannot be found")
    found = own_artifacts(profile, packages, crates)
    for path in found:
        remove(path)
    left = own_artifacts(profile, packages, crates)
    if left:
        raise ValueError(f"Repository crates remain in the Rust output: {left}")
    return len(found)


def prune_after_build(manifest: Path, target: Path) -> int:
    """Prune before a save. A build that left nothing of the repository's is an error.

    Every job that saves has compiled the repository's crates, so compiled
    output with none of them in it means they were not recognised, and what
    would be saved could hold them.
    """
    built = bool(unit_fingerprints(target / PROFILE))
    removed = prune(manifest, target)
    if built and not removed:
        raise ValueError("Compiled Rust output is present and none of it was recognised as the "
                         "repository's; nothing is saved")
    return removed


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
            print(f"Removed {prune_after_build(args.manifest_path, args.target_dir)} repository crate outputs")
        else:
            print(restored(args.manifest_path, args.target_dir, args.matched_key))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(f"::error::Rust dependency cache step failed: {exc}")
        print(f"Rust dependency cache step failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
