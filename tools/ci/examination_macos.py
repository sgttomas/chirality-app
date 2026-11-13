#!/usr/bin/env python3
"""Run the examination tests that need macOS itself, on macOS, with no skips.

A test that needs macOS (libproc, live bundle metadata, macOS process behaviour)
lives in a module named app/tests/group_b_<name>_macos_test.py and skips on other
platforms by an explicit platform condition, so the Ubuntu repository checks
collect and skip it. Here every such module runs on its own; each must collect at
least one test, skip none and pass. When none exists, the job says so plainly.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

PATTERN = "group_b_*_macos_test.py"
TESTS = Path("app/tests")


def discover(root: Path) -> list[Path]:
    return sorted((root / TESTS).glob(PATTERN))


def counts(report: Path) -> dict[str, int]:
    tree = ET.parse(report).getroot()
    suites = [tree] if tree.tag == "testsuite" else tree.findall("testsuite")
    total = {"tests": 0, "skipped": 0, "failures": 0, "errors": 0}
    for suite in suites:
        for key in total:
            total[key] += int(suite.get(key, 0))
    return total


def run_module(root: Path, module: Path) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as scratch:
        report = Path(scratch) / "report.xml"
        done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rs", "-p", "no:cacheprovider",
                               f"--junitxml={report}", str(module.relative_to(root))], cwd=root)
        found = counts(report) if report.exists() else None
    name = module.relative_to(root).as_posix()
    if found is None:
        return False, f"{name}: no test report (pytest exit {done.returncode})"
    summary = (f"{name}: {found['tests']} collected, {found['skipped']} skipped, "
               f"{found['failures']} failed, {found['errors']} errors (pytest exit {done.returncode})")
    if found["tests"] == 0:
        return False, summary + "; a macOS examination module must hold at least one test"
    if found["skipped"]:
        return False, summary + "; a macOS examination test skipped on macOS runs nowhere"
    return done.returncode == 0 and not found["failures"] and not found["errors"], summary


def main(argv: list[str] | None = None, platform: str = sys.platform) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    if platform != "darwin":
        print("macOS examination tests must run on macOS; refusing to report from " + platform, file=sys.stderr)
        return 2
    root = args.root.resolve()
    modules = discover(root)
    if not modules:
        lines = [f"No macOS examination tests on this revision: nothing matches {TESTS.as_posix()}/{PATTERN}, "
                 "so nothing ran."]
        print(f"::notice title=macOS examination tests::{lines[0]}")
        ok = True
    else:
        results = [run_module(root, module) for module in modules]
        lines = [("passed: " if passed else "FAILED: ") + text for passed, text in results]
        ok = all(passed for passed, _ in results)
    print("\n".join(lines))
    if args.summary:
        with args.summary.open("a") as stream:
            stream.write("## macOS examination tests\n\n" + "".join(f"- {line}\n" for line in lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
