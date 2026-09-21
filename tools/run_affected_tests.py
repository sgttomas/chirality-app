#!/usr/bin/env python3
"""Run the tools/ test suites affected by a change set.

Selection is delegated to the ratified selector
(tools/software_workflow/select_affected_checks.py) driven by the routing
profile tools/tools-test-routing.json: live-tree gate suites
(always_checks) run on any change; per-tool suites run only when their
own paths changed. The selection JSON (checks + per-check matched paths)
is printed before the run so every invocation records why each suite ran.

Change set = committed diff against --base (three-dot merge-base diff)
plus working-tree changes (staged, unstaged, untracked). If the base ref
cannot be resolved the script falls back to running everything — routing
must fail open, never silently skip.

Usage:
  python3 tools/run_affected_tests.py                 # vs origin/main
  python3 tools/run_affected_tests.py --base <ref>    # vs another ref
  python3 tools/run_affected_tests.py --all           # full estate
  python3 tools/run_affected_tests.py --dry-run       # selection only
  python3 tools/run_affected_tests.py --paths P [P..] # explicit change set
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from importlib.util import find_spec
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "tools" / "tools-test-routing.json"
SELECTOR = REPO_ROOT / "tools" / "software_workflow" / "select_affected_checks.py"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True, text=True, check=True,
    ).stdout


def changed_paths(base: str) -> list[str] | None:
    """Committed + working-tree changed paths, or None if base is unusable."""
    try:
        committed = _git("diff", "--name-only", f"{base}...HEAD")
    except subprocess.CalledProcessError:
        return None
    paths = {line for line in committed.splitlines() if line}
    for line in _git("status", "--porcelain=v1", "-uall").splitlines():
        entry = line[3:]
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        if entry:
            paths.add(entry)
    return sorted(paths)


def load_profile() -> dict:
    return json.loads(PROFILE.read_text(encoding="utf-8"))


def select_checks(paths: list[str]) -> dict:
    profile = load_profile()
    if not paths:
        return {
            "schema": "chirality-affected-checks/v1",
            "paths": [],
            "checks": sorted(profile["always_checks"]),
            "reasons": {},
        }
    result = subprocess.run(
        [sys.executable, str(SELECTOR), str(PROFILE), "--paths-json-stdin"],
        input=json.dumps(paths), capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def pytest_dirs(check_ids: list[str]) -> list[str]:
    checks = load_profile()["checks"]
    dirs: list[str] = []
    for check_id in check_ids:
        dirs.extend(checks[check_id]["pytest_paths"])
    return sorted(set(dirs))


def run_pytest(dirs: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", "-q"]
    if find_spec("xdist") is not None:
        cmd += ["-n", "auto", "--dist", "loadscope"]
    cmd += dirs
    print(f"[run-affected] {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=REPO_ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/main",
                        help="ref to diff against (default: origin/main)")
    parser.add_argument("--all", action="store_true",
                        help="run the full tools/ estate")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the selection and exit without running")
    parser.add_argument("--paths", nargs="+", default=None,
                        help="explicit changed-path list (overrides git)")
    args = parser.parse_args()

    if args.all:
        selection = {"checks": sorted(load_profile()["checks"]),
                     "reasons": {"*": ["--all"]}, "paths": ["--all"]}
    else:
        paths = args.paths if args.paths is not None else changed_paths(args.base)
        if paths is None:
            print(f"[run-affected] base {args.base!r} not resolvable; "
                  "failing open to the full estate", flush=True)
            selection = {"checks": sorted(load_profile()["checks"]),
                         "reasons": {"*": ["base-unresolvable"]},
                         "paths": []}
        else:
            selection = select_checks(paths)

    print(json.dumps(selection, indent=2, sort_keys=True), flush=True)
    dirs = pytest_dirs(selection["checks"])
    skipped = sorted(set(load_profile()["checks"]) - set(selection["checks"]))
    print(f"[run-affected] running {len(selection['checks'])} suite(s); "
          f"skipping {len(skipped)}: {', '.join(skipped) or '(none)'}", flush=True)
    if args.dry_run:
        return 0
    return run_pytest(dirs)


if __name__ == "__main__":
    raise SystemExit(main())
