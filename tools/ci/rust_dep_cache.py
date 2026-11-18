#!/usr/bin/env python3
"""Keep the repository's own crates out of the CI Rust dependency cache.

Cargo rebuilds a workspace unit when its freshness fingerprint is missing. This
tool removes cached paths matching current workspace packages and targets. The
remaining dependency artifacts can be reused under the cache key.

Cargo's output layout is subject to change. In the legacy layout the cache
paths are `.fingerprint/<package>-<hash>/`, `build/<package>-<hash>/` and flat
entries in `deps/`. The latter can include unhashed files from a local cdylib
build. In Cargo 1.100's new layout, the tool looks for units under
`build/<package>/<hash>/` and checks for a fingerprint directory in each
populated package. It refuses cache entries that fail its structural checks.
The shape of a path alone cannot establish its ownership.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

MANIFEST = Path("app/src-tauri/Cargo.toml")
TARGET = Path("app/src-tauri/target")
PROFILE = "debug"
CACHED_FOLDERS = (".fingerprint", "build", "deps")


def metadata(manifest: Path) -> dict:
    return json.loads(subprocess.check_output(
        ["cargo", "metadata", "--no-deps", "--format-version", "1", "--offline",
         "--manifest-path", str(manifest)]))


def own_units(manifest: Path) -> tuple[set[str], set[str]]:
    """Return the repository's package names and crate names from Cargo itself."""
    packages = metadata(manifest)["packages"]
    names = {package["name"] for package in packages}
    crates = {target["name"].replace("-", "_")
              for package in packages for target in package["targets"]}
    if not names or not crates:
        raise ValueError("Cargo reported no repository package or target")
    return names, crates


def lockfile(manifest: Path) -> Path | None:
    """The lockfile Cargo uses for this manifest: the one at its workspace root."""
    lock = Path(metadata(manifest)["workspace_root"]) / "Cargo.lock"
    return lock if lock.is_file() else None


HASH = "[0-9a-f]{16}"
LEGACY_UNIT = re.compile(rf"(.+)-{HASH}")
UNIT = re.compile(HASH)
HASHED_FILE = re.compile(rf"(?:lib)?[A-Za-z0-9_]+-{HASH}(?:\..*)?")
# What Cargo 1.100 keeps directly inside a unit folder, and what the older layout
# keeps directly inside a build script's two folders. A build script's own
# output under `out` is not looked into.
UNIT_FOLDERS = ("fingerprint", "out", "run", "artifact")
UNIT_FILES = (".lock",)
RUN_FILES = ("output", "root-output", "stderr", "invoked.timestamp")
BUILD_SCRIPT = ("build-script-", "build_script_")
# The temporary directory rustc links in, beside the output it is making. An
# interrupted link can leave it behind.
COMPILER_SCRATCH = re.compile(r"rustc[A-Za-z0-9]{6}")


def real_directory(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def entries(directory: Path) -> list[Path]:
    return sorted(directory.iterdir()) if real_directory(directory) else []


def only_files(directory: Path) -> bool:
    return all(entry.is_file() for entry in entries(directory))


def package_folder(entry: Path) -> bool:
    """Identify a new-layout package folder by its hashed unit directories.

    For an empty entry, use its name to distinguish it from a legacy
    `<package>-<hash>` folder.
    """
    if not real_directory(entry):
        return False
    inside = entries(entry)
    if not inside:
        return not LEGACY_UNIT.fullmatch(entry.name)
    return all(real_directory(unit) and UNIT.fullmatch(unit.name) for unit in inside)


def unit_as_cargo_1_100_makes_it(unit: Path) -> bool:
    for member in entries(unit):
        if member.name in UNIT_FOLDERS and real_directory(member):
            if member.name in ("fingerprint", "run") and not only_files(member):
                return False
        elif not (member.name in UNIT_FILES and member.is_file()):
            return False
    return True


def build_script_folder_as_the_older_layout_makes_it(entry: Path) -> bool:
    for member in entries(entry):
        if member.name == "out" and real_directory(member):
            continue
        if member.name in RUN_FILES and member.is_file():
            continue
        if member.name.startswith(BUILD_SCRIPT) and (member.is_file() or member.name.endswith(".dSYM")):
            continue
        if COMPILER_SCRATCH.fullmatch(member.name) and real_directory(member):
            continue
        return False
    return True


def own_artifacts(profile: Path, packages: set[str], crates: set[str]) -> list[Path]:
    """List cached paths selected for removal by package name or crate name."""
    crate = re.compile("(?:lib)?(?:" + "|".join(map(re.escape, sorted(crates))) + r")(?:-[0-9a-f]+)?(?:\..*)?")
    # Names that differ only in case share one folder on a case-insensitive disk.
    folded = {package.casefold() for package in packages}

    def legacy_owner(entry: Path) -> bool:
        named = LEGACY_UNIT.fullmatch(entry.name)
        return bool(named) and named.group(1) in packages

    found = [entry for entry in entries(profile / ".fingerprint") if legacy_owner(entry)]
    for entry in entries(profile / "build"):
        # The name is read as the layout the entry is in reads it.
        if entry.name.casefold() in folded if package_folder(entry) else legacy_owner(entry):
            found.append(entry)
    found += [entry for entry in entries(profile / "deps") if crate.fullmatch(entry.name)]
    return found


def unidentified(profile: Path) -> list[Path]:
    """List legacy `deps` entries without a recognized filename hash and rustc
    temporary directories directly inside legacy build-script folders.

    The App's registry dependencies use hashed compiler artifact names in legacy
    `deps`. The first selection includes old App library output, compiler
    scratch, and any other entry with no recognized filename hash. Both
    selections are applied after removing current-name matches.
    """
    found = [entry for entry in entries(profile / "deps") if not HASHED_FILE.fullmatch(entry.name)]
    for entry in entries(profile / "build"):
        if real_directory(entry) and not package_folder(entry):
            found += [member for member in entries(entry)
                      if COMPILER_SCRATCH.fullmatch(member.name) and real_directory(member)]
    return found


def compiled_units(profile: Path) -> list[Path]:
    """Recognized fingerprint directories, under either known layout.

    Cargo can create one during preparation, before compilation succeeds.
    """
    found = [entry for entry in entries(profile / ".fingerprint")
             if real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name)]
    for entry in entries(profile / "build"):
        if package_folder(entry):
            found += [unit / "fingerprint" for unit in entries(entry) if real_directory(unit / "fingerprint")]
    return found


def unrecognised_output(profile: Path) -> list[Path]:
    """List entries that fail the cache structure checks.

    The separate legacy removal rule handles `deps` entries without a recognized
    filename hash.
    """
    unknown = [profile / name for name in CACHED_FOLDERS
               if (profile / name).exists() and not real_directory(profile / name)]
    unknown += [entry for entry in entries(profile / ".fingerprint")
                if not (real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name) and only_files(entry))]
    payload = []
    for entry in entries(profile / "build"):
        if package_folder(entry):
            units = entries(entry)
            unknown += [unit for unit in units if not unit_as_cargo_1_100_makes_it(unit)]
            # Cargo makes a build script's output folder before that run's
            # fingerprint, so one unit without a fingerprint is ordinary. A
            # package with output and no fingerprint in any unit has no freshness
            # record to remove.
            if units and not any(real_directory(unit / "fingerprint") for unit in units):
                unknown.append(entry)
        elif (real_directory(entry) and LEGACY_UNIT.fullmatch(entry.name)
              and build_script_folder_as_the_older_layout_makes_it(entry)):
            payload.append(entry)
        else:
            unknown.append(entry)
    for entry in entries(profile / "deps"):
        if not HASHED_FILE.fullmatch(entry.name):
            continue  # No recognized hash: removed by the unhashed-entry rule.
        if entry.is_file() or (real_directory(entry) and entry.name.endswith(".dSYM")):
            payload.append(entry)
        else:
            unknown.append(entry)
    if payload and not entries(profile / ".fingerprint"):
        # The older layout's output with no fingerprint beside it.
        unknown += payload
    return unknown


def shared_names(manifest: Path, packages: set[str]) -> list[str]:
    """Return current workspace package names that occur more than once in the
    workspace lockfile after case folding.

    The pruner refuses these names because package-name matching alone cannot
    distinguish the units.
    """
    lock = lockfile(manifest)
    if lock is None:
        return []
    names = [str(package.get("name", "")).casefold()
             for package in tomllib.loads(lock.read_text()).get("package", [])]
    return sorted(name for name in packages if names.count(name.casefold()) > 1)


def remove(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def prune(manifest: Path, target: Path) -> int:
    """Remove current-name matches first and remaining unidentified entries next.

    Check both selections again before returning the number of current-name
    matches.
    """
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
    # Listed after the matches are gone: a match can hold or be one of these.
    for path in unidentified(profile):
        remove(path)
    left = own_artifacts(profile, packages, crates) + unidentified(profile)
    if left:
        raise ValueError(f"Entries selected for removal remain in the Rust output: {left}")
    return len(found)


def prune_after_build(manifest: Path, target: Path) -> int:
    """Require at least one current workspace package or target match before saving."""
    built = bool(compiled_units(target / PROFILE))
    removed = prune(manifest, target)
    if not removed:
        raise ValueError("Compiled Rust output is present and none of it was recognised as the "
                         "repository's; nothing is saved" if built else
                         "No Rust output matched a current workspace package or target; nothing is saved")
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
