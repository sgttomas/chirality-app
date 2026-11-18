#!/usr/bin/env python3
"""Keep the repository's own crates out of the CI Rust dependency cache.

Cargo treats a unit as fresh only when its fingerprint directory says so. A
crate with no fingerprint must be compiled from the checked-out source, whatever
the file times are. Removing the repository's own units therefore leaves cargo
nothing it could wrongly reuse; third-party units stay, bound to Cargo.lock by
the cache key.

Cargo's output layout is not a stable interface. Two are known here. Before
Cargo 1.100: `.fingerprint/<package>-<hash>/`, `build/<package>-<hash>/` and
flat files in `deps/`, where a local library built as a dynamic or static
library carries no hash in its file names. From 1.100: every unit of a package
under `build/<package>/<hash>/`, at least one of them with a `fingerprint`
folder. Every entry of the cached folders is sorted into one of these by its structure, and an entry
that fits neither is refused, never passed as clean. A shape check has a limit:
a future layout that looks like one of these cannot be told apart.
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


HASH = "[0-9a-f]{16}"
LEGACY_UNIT = re.compile(rf"(.+)-{HASH}")
UNIT = re.compile(HASH)


def real_directory(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def entries(directory: Path) -> list[Path]:
    return sorted(directory.iterdir()) if real_directory(directory) else []


def package_folder(entry: Path) -> bool:
    """A `build` entry in the layout of Cargo 1.100: only unit folders inside, or nothing.

    The older layout's `build/<package>-<hash>/` holds a build script or its run
    output directly, never a folder per unit, so the two cannot be confused even
    when a package's own name ends in something that looks like a hash.
    """
    if not real_directory(entry):
        return False
    inside = entries(entry)
    if not inside:
        return not LEGACY_UNIT.fullmatch(entry.name)
    return all(real_directory(unit) and UNIT.fullmatch(unit.name) for unit in inside)


def own_artifacts(profile: Path, packages: set[str], crates: set[str]) -> list[Path]:
    """List output belonging to repository crates; dependencies never match."""
    crate = re.compile("(?:lib)?(?:" + "|".join(map(re.escape, sorted(crates))) + r")(?:-[0-9a-f]+)?(?:\..*)?")

    def legacy_owner(entry: Path) -> bool:
        named = LEGACY_UNIT.fullmatch(entry.name)
        return bool(named) and named.group(1) in packages

    found = [entry for entry in entries(profile / ".fingerprint") if legacy_owner(entry)]
    for entry in entries(profile / "build"):
        # The name is read as the layout the entry is in reads it.
        if entry.name in packages if package_folder(entry) else legacy_owner(entry):
            found.append(entry)
    # A local library built as a dynamic or static library has no hash in its file names.
    found += [entry for entry in entries(profile / "deps") if crate.fullmatch(entry.name)]
    return found


def compiled_units(profile: Path) -> list[Path]:
    """Every compiled unit's fingerprint folder, under either known layout."""
    found = [entry for entry in entries(profile / ".fingerprint")
             if real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name)]
    for entry in entries(profile / "build"):
        if package_folder(entry):
            found += [unit / "fingerprint" for unit in entries(entry) if real_directory(unit / "fingerprint")]
    return found


def unrecognised_output(profile: Path) -> list[Path]:
    """Entries of the cached folders that fit neither known layout, known units beside them or not."""
    unknown = [profile / name for name in CACHED_FOLDERS
               if (profile / name).exists() and not real_directory(profile / name)]
    unknown += [entry for entry in entries(profile / ".fingerprint")
                if not (real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name))]
    payload = []
    for entry in entries(profile / "build"):
        if package_folder(entry):
            # Cargo gives a build script's output a unit folder with no fingerprint
            # of its own, so one unit without one is ordinary. A package with output
            # and no fingerprint in any unit has no freshness record to remove.
            units = entries(entry)
            if units and not any(real_directory(unit / "fingerprint") for unit in units):
                unknown.append(entry)
        elif real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name):
            payload.append(entry)
        else:
            unknown.append(entry)
    for entry in entries(profile / "deps"):
        if entry.is_file() or (real_directory(entry) and entry.name.endswith(".dSYM")):
            payload.append(entry)
        else:
            unknown.append(entry)
    if payload and not entries(profile / ".fingerprint"):
        # The older layout's output with no fingerprint beside it.
        unknown += payload
    return unknown


def shared_names(manifest: Path, packages: set[str]) -> list[str]:
    """Repository package names that Cargo.lock also gives to another package.

    Both layouts file a package's units under its name alone, so the two
    packages' units could not be told apart.
    """
    for folder in (manifest.resolve().parent, *manifest.resolve().parent.parents):
        lock = folder / "Cargo.lock"
        if lock.is_file():
            names = re.findall(r'^\[\[package\]\]\nname = "([^"]+)"', lock.read_text(), re.MULTILINE)
            return sorted(name for name in packages if names.count(name) > 1)
    return []


def remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def prune(manifest: Path, target: Path) -> int:
    """Remove repository crates from target and prove none remain."""
    packages, crates = own_units(manifest)
    shared = shared_names(manifest, packages)
    if shared:
        raise ValueError(f"Cargo.lock gives the repository package name {shared} to another package "
                         "too; their compiled units cannot be told apart")
    profile = target / PROFILE
    unknown = unrecognised_output(profile)
    if unknown:
        raise ValueError(f"Rust output under {profile} is not in a layout this tool knows "
                         f"({len(unknown)} entries, first {unknown[0]}); repository crates in it "
                         "cannot be found")
    found = own_artifacts(profile, packages, crates)
    for path in found:
        remove(path)
    left = own_artifacts(profile, packages, crates)
    if left:
        raise ValueError(f"Repository crates remain in the Rust output: {left}")
    return len(found)


def prune_after_build(manifest: Path, target: Path) -> int:
    """Prune before a save. A build that left nothing of the repository's is an error.

    A job that compiled has the repository's crates in its output, so compiled
    output with none of them recognised could hold them unrecognised. A job that
    restored dependencies and failed before compiling is refused as well; it has
    nothing new to save.
    """
    built = bool(compiled_units(target / PROFILE))
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
