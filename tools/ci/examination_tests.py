#!/usr/bin/env python3
"""Run the Group B examination tests on their two hosted routes, judged by what ran.

`portable` (Ubuntu repository checks) runs every app/tests/group_b*test.py. A test
may skip there only if its module is named app/tests/group_b_<name>_macos_test.py
or it is the one test in GRANDFATHERED; any other skip, including one at
collection time, fails and is named.

`macos` (the examination-macos job) runs every tracked group_b_*_macos_test.py on
macOS, each module on its own; a module with no test, or any skipped, failed or
erroring test, fails. It also fails when the selector's merge base held such a
module and the head holds none.
"""
from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

TESTS = "app/tests"
PATTERN = "group_b_*_macos_test.py"
PORTABLE_GLOB = "group_b*test.py"
# Present on main before the macOS route existed; it runs only in the nightly
# full suite until it moves into a module matching PATTERN.
GRANDFATHERED = frozenset({
    "app/tests/group_b_launch_home_test.py::OnlyTheIdentifiedCandidate::"
    "test_a_changed_resource_is_refused_and_the_identified_bundle_launches",
})


def is_macos_module(path: str) -> bool:
    pure = PurePosixPath(path)
    return str(pure.parent) == TESTS and fnmatchcase(pure.name, PATTERN)


def tracked_modules(root: Path, revision: str) -> list[str]:
    """Matching modules in a commit's tree, read from Git, not from the checkout."""
    listed = subprocess.run(["git", "-C", str(root), "ls-tree", "--name-only", "-z", revision, "--", TESTS + "/"],
                            capture_output=True, check=True).stdout
    return sorted(name for name in os.fsdecode(listed).split("\0") if name and is_macos_module(name))


def pytest(root: Path, paths: list[str], report: Path) -> int:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-rs", "-p", "no:cacheprovider",
                           "-o", "junit_family=xunit1", f"--junitxml={report}", *paths], cwd=root).returncode


def cases(report: Path) -> list[dict[str, str]]:
    """Every reported test case, with its skip state. A missing report is an error."""
    found = []
    for case in ET.parse(report).getroot().iter("testcase"):
        file = case.get("file")
        if not file:
            raise ValueError("test report lacks the module of a test case")
        module = file[:-3].replace("/", ".") if file.endswith(".py") else file
        classname = case.get("classname", "")
        inner = classname[len(module) + 1:] if classname.startswith(module + ".") else classname
        ident = "::".join(part for part in [file, *inner.split(".")] if part) + "::" + case.get("name", "")
        found.append({"file": file, "id": ident,
                      "skipped": any(child.tag == "skipped" for child in case),
                      "broken": any(child.tag in {"failure", "error"} for child in case)})
    return found


def portable(root: Path) -> tuple[bool, list[str]]:
    paths = sorted(path.relative_to(root).as_posix() for path in (root / TESTS).glob(PORTABLE_GLOB))
    if not paths:
        return False, [f"nothing matches {TESTS}/{PORTABLE_GLOB}"]
    with tempfile.TemporaryDirectory() as scratch:
        report = Path(scratch) / "report.xml"
        code = pytest(root, paths, report)
        try:
            found = cases(report)
        except (OSError, ET.ParseError, ValueError) as exc:
            return False, [f"pytest exit {code}; the test report needed to inspect skips is unavailable: {exc}"]
    refused = [case["id"] for case in found if case["skipped"]
               and not is_macos_module(case["file"]) and case["id"] not in GRANDFATHERED]
    skipped = sum(case["skipped"] for case in found)
    lines = [f"{len(found)} reported, {skipped} skipped, pytest exit {code}"]
    lines += [f"skipped outside a macOS module and not grandfathered: {ident}" for ident in refused]
    return code == 0 and not refused, lines


def run_module(root: Path, module: str) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as scratch:
        report = Path(scratch) / "report.xml"
        code = pytest(root, [module], report)
        try:
            found = cases(report)
        except (OSError, ET.ParseError, ValueError) as exc:
            return False, f"{module}: pytest exit {code}; no usable test report ({exc})"
    skipped, broken = sum(c["skipped"] for c in found), sum(c["broken"] for c in found)
    summary = f"{module}: {len(found)} reported, {skipped} skipped, {broken} failed or errored (pytest exit {code})"
    if not found:
        return False, summary + "; a macOS examination module must hold at least one test"
    if skipped:
        return False, summary + "; a macOS examination test skipped on macOS runs nowhere"
    return code == 0 and not broken, summary


def macos(root: Path, merge_base: str, event: str) -> tuple[bool, list[str]]:
    modules = tracked_modules(root, "HEAD")
    lines, ok = [], True
    if event == "workflow_dispatch":
        lines.append("Manual dispatch has no merge base; the removal check does not apply.")
    elif not merge_base:
        return False, ["The selector's merge base is missing; the removal check cannot be made."]
    else:
        try:
            before = tracked_modules(root, merge_base)
        except subprocess.CalledProcessError as exc:
            return False, [f"The merge base {merge_base} cannot be inspected: {exc.stderr.decode(errors='replace').strip()}"]
        if before and not modules:
            return False, [f"The merge base holds {len(before)} macOS examination module(s) ({', '.join(before)}) "
                           "and the head holds none. Removing the last one needs a deliberate change to "
                           "tools/ci/examination_tests.py."]
    if not modules:
        lines.append(f"No macOS examination tests on this revision: nothing tracked matches {TESTS}/{PATTERN}, "
                     "so nothing ran.")
        print(f"::notice title=macOS examination tests::{lines[-1]}")
        return ok, lines
    results = [run_module(root, module) for module in modules]
    lines += [("passed: " if passed else "FAILED: ") + text for passed, text in results]
    return all(passed for passed, _ in results), lines


def main(argv: list[str] | None = None, platform: str = sys.platform) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route", choices=["portable", "macos"])
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--merge-base", default="")
    parser.add_argument("--event", default="pull_request")
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.route == "macos":
        if platform != "darwin":
            print("macOS examination tests must run on macOS; refusing to report from " + platform, file=sys.stderr)
            return 2
        ok, lines = macos(root, args.merge_base, args.event)
        title = "macOS examination tests"
    else:
        ok, lines = portable(root)
        title = "Group B examination tests (portable route)"
    print("\n".join(lines))
    if args.summary:
        with args.summary.open("a") as stream:
            stream.write(f"## {title}\n\n" + "".join(f"- {line}\n" for line in lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
