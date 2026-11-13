#!/usr/bin/env python3
"""Check that every App web test file is run by a pull-request job or excluded.

Every ``*.test.mjs`` under ``app/tests`` must be named on a ``node --test``
line of a pull-request job in ``.github/workflows/app-v4.yml``, or in the one
exclusion list ``tools/ci/web_test_exclusions.txt`` with its reason. The check
fails, naming the file, when a test file is in neither, when a file named on a
line or in the list does not exist, when a file is in both, and when it finds
no test files or no pull-request ``node --test`` line at all.

A pull-request job is one whose ``if`` is exactly the focused-route condition
below; the full route (``product``, run on dispatch and nightly) does not
count, whatever its lines name. Lines of every job are checked for files that
do not exist.

Limit: this checks spelling in a workflow file. It does not show that a listed
test executes or passes, it does not read app/package.json's test script, and
it does not see a web test file under another name pattern (for example
``group_b_runner_test.mjs``) or a file reached only through a shell variable.
"""
from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(".github/workflows/app-v4.yml")
EXCLUSIONS = Path("tools/ci/web_test_exclusions.txt")
TESTS = PurePosixPath("app/tests")
PATTERN = "*.test.mjs"
PULL_REQUEST_CONDITION = "github.event_name != 'workflow_dispatch' && !inputs.full_suite"
OPERATORS = {"&&", "||", ";", "|", "&", ";;", "(", ")"}


def node_test_arguments(run: str) -> list[list[str]]:
    """Return the arguments of each ``node --test`` command in a step's script."""
    commands = []
    for line in run.replace("\\\n", " ").splitlines():
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        tokens = list(lexer)
        for i in range(len(tokens) - 1):
            if tokens[i] == "node" and tokens[i + 1] == "--test" and (i == 0 or tokens[i - 1] in OPERATORS):
                arguments = []
                for token in tokens[i + 2:]:
                    if token in OPERATORS:
                        break
                    arguments.append(token)
                commands.append(arguments)
    return commands


def _working_directory(workflow: dict, job: dict, step: dict) -> PurePosixPath:
    for scope in (step, (job.get("defaults") or {}).get("run") or {}, (workflow.get("defaults") or {}).get("run") or {}):
        if scope.get("working-directory"):
            return PurePosixPath(scope["working-directory"])
    return PurePosixPath(".")


def _normalise(path: PurePosixPath) -> PurePosixPath:
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if parts:
                parts.pop()
            else:
                parts.append(part)
        elif part != ".":
            parts.append(part)
    return PurePosixPath(*parts)


def workflow_listing(workflow: dict) -> tuple[dict[str, list[str]], list[str], dict[str, list[str]]]:
    """Read the node --test lines of every job.

    Returns the repository paths named by pull-request jobs, with where; the
    problems found (an argument that is not a test file under app/tests, or no pull-request line at all); and the paths named by any job,
    whose existence the caller checks.
    """
    listing: dict[str, list[str]] = {}
    named_anywhere: dict[str, list[str]] = {}
    problems: list[str] = []
    lines = 0
    for job_id, job in (workflow.get("jobs") or {}).items():
        pull_request = job.get("if") == PULL_REQUEST_CONDITION
        for step in job.get("steps") or []:
            run = step.get("run")
            if not isinstance(run, str):
                continue
            for arguments in node_test_arguments(run):
                where = f"{job_id} / {step.get('name', '(unnamed step)')}"
                if pull_request:
                    lines += 1
                base = _working_directory(workflow, job, step)
                for argument in arguments:
                    if argument.startswith("-"):
                        continue
                    path = _normalise(base / argument)
                    if TESTS not in path.parents or not path.match(PATTERN):
                        problems.append(f"{argument} on {where} is not a {PATTERN} file under {TESTS}")
                        continue
                    named_anywhere.setdefault(str(path), []).append(where)
                    if pull_request:
                        listing.setdefault(str(path), []).append(where)
    if lines == 0:
        problems.append(f"no node --test line found in a pull-request job (if: {PULL_REQUEST_CONDITION})")
    return listing, problems, named_anywhere


def parse_exclusions(text: str) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    problems: list[str] = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, colon, reason = line.partition(":")
        name, reason = name.strip(), reason.strip()
        if not colon or not reason:
            problems.append(f"exclusion line {number} gives no reason: {line}")
            continue
        path = str(TESTS / name)
        if path in entries:
            problems.append(f"{name} is excluded twice")
        entries[path] = reason
    return entries, problems


def check(root: Path, workflow_text: str, exclusions_text: str) -> list[str]:
    workflow = yaml.safe_load(workflow_text) or {}
    listing, problems, named_anywhere = workflow_listing(workflow)
    excluded, exclusion_problems = parse_exclusions(exclusions_text)
    problems += exclusion_problems
    tests_dir = root / TESTS
    found = sorted(str(TESTS / p.relative_to(tests_dir).as_posix()) for p in tests_dir.rglob(PATTERN)) if tests_dir.is_dir() else []
    if not found:
        problems.append(f"no {PATTERN} file found under {TESTS}")
    for path in found:
        if path not in listing and path not in excluded:
            problems.append(f"{path} is run by no pull-request job and is not in {EXCLUSIONS}")
        if path in listing and path in excluded:
            problems.append(f"{path} is both run by a pull-request job ({'; '.join(listing[path])}) and in {EXCLUSIONS}")
    for path, where in sorted(named_anywhere.items()):
        if not (root / path).is_file():
            problems.append(f"{path} named on {'; '.join(where)} does not exist")
    for path in sorted(excluded):
        if not (root / path).is_file():
            problems.append(f"{path} in {EXCLUSIONS} does not exist")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--workflow", type=Path, help="workflow file to read (default: the root's app-v4.yml)")
    parser.add_argument("--exclusions", type=Path, help="exclusion list to read (default: the root's list)")
    args = parser.parse_args(argv)
    workflow = (args.workflow or args.root / WORKFLOW).read_text(encoding="utf-8")
    exclusions_path = args.exclusions or args.root / EXCLUSIONS
    exclusions = exclusions_path.read_text(encoding="utf-8") if exclusions_path.exists() else ""
    problems = check(args.root, workflow, exclusions)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"web test listing: {len(problems)} problem(s)", file=sys.stderr)
        return 1
    print("web test listing: every web test file is run by a pull-request job or excluded with a reason")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
