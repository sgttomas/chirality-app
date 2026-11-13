#!/usr/bin/env python3
"""Check that every Rust library test is selected on pull requests or deliberately left out.

Reads the library's test list (the output of
``cargo test --locked --manifest-path src-tauri/Cargo.toml --lib -- --list``),
``.github/workflows/app-v4.yml`` and ``tools/ci/lib_cohort_exclusions.txt``.
A pull-request default-feature filter is a ``LIB_COHORTS`` entry of a
pull-request job, or the test-name filter of a ``cargo test --lib`` command
without ``--features`` in a pull-request job's step (a command at the start of
a shell command, after any ``NAME=value`` words). A filter selects a test as
libtest does: the test's path contains it (equals it under ``--exact``).

Jobs are told apart by their ``if``, the pull-request condition and the
full-route condition below exactly as written. A job with no ``if`` counts as
a pull-request job: the workflow runs it on every event that calls it, the
pull-request call included. A job with a ``cargo test --lib`` line and any
other ``if`` fails the check, naming the job and its condition.

An exclusion line names a test module and covers the tests directly in that
module that no pull-request filter selects, not those of its submodules, so a
new submodule is not excluded by its parent's line. Or it names one test by
its full path; that line takes precedence over its module's line. Each line
gives its reason.

The check fails, naming them, when a test is selected by no pull-request
default-feature filter and covered by no exclusion line; when a filter selects
no test; when an exclusion line covers no test (a module line whose tests are
all selected is stale); when a line naming one test names a selected test;
when an exclusion line has no reason or repeats; and when the list holds no
test or the workflow no filter.

It needs only the Python standard library, because it runs on the macOS job
that has the test list and no YAML library. ``read_workflow`` reads the few
things the check uses (job ids, a job's ``if``, its ``LIB_COHORTS`` and its
steps' ``name`` and ``run``) from the workflow's own layout: a top-level
``jobs:`` mapping, block or quoted scalars, steps as a ``- `` list.
``tools/ci/test_lib_cohorts.py``, run by repository-checks with PyYAML, fails
when this reading and PyYAML's give different filters for the real workflow.

Limit: it shows that each library test is selected on pull requests or left
to the full route on purpose. It does not show that a selected test passes, it
reads only the default-feature list (a test compiled only with a feature is not
in it), and a test left to the full route runs on main nightly and on a product
dispatch, not on the pull request that changes it. A new test in an excluded
module is excluded with it.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(".github/workflows/app-v4.yml")
EXCLUSIONS = Path("tools/ci/lib_cohort_exclusions.txt")
PULL_REQUEST_CONDITION = "github.event_name != 'workflow_dispatch' && !inputs.full_suite"
OPERATORS = {"&&", "||", ";", "|", "&", ";;", "(", ")"}
FULL_ROUTE_CONDITION = "github.event_name == 'workflow_dispatch' || inputs.full_suite"
SHELL_KEYWORDS = {"do", "then", "else", "!", "time", "env"}
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")
VALUE_FLAGS = {
    "--manifest-path", "--features", "-F", "--package", "-p", "--target", "--target-dir", "-j", "--jobs",
    "--profile", "--test", "--bin", "--example", "--bench", "--color", "--message-format", "-Z", "--config",
}


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _scalar(lines: list[str], index: int, key_indent: int, rest: str) -> tuple[str, int]:
    """The value of a key whose text after the colon is rest; returns it and the next line index."""
    rest = rest.strip()
    following = []
    j = index + 1
    while j < len(lines) and (not lines[j].strip() or _indent(lines[j]) > key_indent):
        following.append(lines[j])
        j += 1
    while following and not following[-1].strip():
        following.pop()
        j -= 1
    if rest[:1] in ("|", ">"):
        body = [line for line in following]
        depth = min((_indent(line) for line in body if line.strip()), default=0)
        body = [line[depth:] for line in body]
        return ("\n" if rest[0] == "|" else " ").join(body if rest[0] == "|" else [b for b in body if b]), j
    if rest.startswith("'") and rest.endswith("'") and len(rest) > 1:
        return rest[1:-1].replace("''", "'"), j
    if rest.startswith('"') and rest.endswith('"') and len(rest) > 1:
        return json.loads(rest), j
    return " ".join([rest, *(line.strip() for line in following if line.strip())]).strip(), j


KEY = re.compile(r"(-\s+)?([A-Za-z0-9_-]+):(?:\s+(.*))?$")


def read_workflow(text: str) -> dict:
    """Read job ids, each job's if and LIB_COHORTS, and its steps' name and run."""
    lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
    jobs: dict[str, dict] = {}
    try:
        start = lines.index("jobs:") + 1
    except ValueError:
        return {"jobs": jobs}
    job_indent = job_key_indent = None
    job = step = None
    step_key_indent = None
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        indent = _indent(line)
        if indent == 0:
            break
        match = KEY.match(line.strip())
        if job_indent is None:
            job_indent = indent
        if indent == job_indent and match and not match.group(1):
            job = jobs.setdefault(match.group(2), {"steps": []})
            job_key_indent = step = None
            i += 1
            continue
        if job is None or not match:
            i += 1
            continue
        if job_key_indent is None:
            job_key_indent = indent
        dash, key, rest = match.group(1), match.group(2), match.group(3) or ""
        if dash:
            step = {}
            job["steps"].append(step)
            step_key_indent = indent + len(dash)
        if indent == job_key_indent and not dash and key == "if":
            job["if"], i = _scalar(lines, i, indent, rest)
            continue
        if key == "LIB_COHORTS" and step is None:
            job.setdefault("env", {})["LIB_COHORTS"], i = _scalar(lines, i, indent, rest)
            continue
        if step is not None and key in ("name", "run") and (dash or indent == step_key_indent):
            step[key], i = _scalar(lines, i, step_key_indent, rest)
            continue
        i += 1
    return {"jobs": jobs}


def parse_list(text: str) -> list[str]:
    return [line[: -len(": test")].strip() for line in text.splitlines() if line.rstrip().endswith(": test")]


def _commands(run: str) -> list[list[str]]:
    commands = []
    for line in run.replace("\\\n", " ").splitlines():
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        current: list[str] = []
        for token in lexer:
            if token in OPERATORS:
                if current:
                    commands.append(current)
                current = []
            else:
                current.append(token)
        if current:
            commands.append(current)
    return commands


def cargo_lib_filters(run: str) -> list[tuple[str, bool, bool]]:
    """(filter, exact, with_features) for each `cargo test --lib` command of a script."""
    found = []
    for command in _commands(run):
        while command and (command[0] in SHELL_KEYWORDS or ASSIGNMENT.match(command[0])):
            command = command[1:]
        if command[:2] != ["cargo", "test"]:
            continue
        before, after = command[2:], []
        if "--" in before:
            index = before.index("--")
            before, after = before[:index], before[index + 1:]
        if "--lib" not in before or "--no-run" in before or "--list" in after:
            continue
        features = any(t in ("--features", "-F", "--all-features") or t.startswith("--features=") for t in before)
        positional, skip = [], False
        for token in before:
            if skip:
                skip = False
            elif token in VALUE_FLAGS:
                skip = True
            elif not token.startswith("-"):
                positional.append(token)
        found.append((positional[0] if positional else "", "--exact" in after, features))
    return found


def pull_request_filters(workflow: dict, problems: list[str] | None = None) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Default-feature and feature filters of the pull-request jobs, each with where it is.

    A job with a cargo test --lib line whose if is neither condition is named
    in problems.
    """
    default: dict[str, list[str]] = {}
    featured: dict[str, list[str]] = {}
    for job_id, job in (workflow.get("jobs") or {}).items():
        condition = job.get("if")
        pull_request = condition is None or condition == PULL_REQUEST_CONDITION
        recognised = pull_request or condition == FULL_ROUTE_CONDITION
        cohorts = str((job.get("env") or {}).get("LIB_COHORTS") or "").split()
        for step in job.get("steps") or []:
            run = step.get("run")
            if not isinstance(run, str):
                continue
            where = f"{job_id} / {step.get('name', '(unnamed step)')}"
            filters = cargo_lib_filters(run)
            if filters and not recognised:
                if problems is not None:
                    problems.append(
                        f"job {job_id} has a cargo test --lib line and an if the check does not recognise: {condition!r} "
                        f"(pull request: {PULL_REQUEST_CONDITION!r}; full route: {FULL_ROUTE_CONDITION!r})")
                break
            if not pull_request:
                continue
            for name, exact, features in filters:
                names = cohorts if "LIB_COHORTS" in run and name.startswith("$") else [name]
                for value in names:
                    key = f"={value}" if exact else value
                    (featured if features else default).setdefault(key, []).append(where)
    return default, featured


def _selects(key: str, test: str) -> bool:
    return test == key[1:] if key.startswith("=") else key in test


def parse_exclusions(text: str) -> tuple[dict[str, str], list[str]]:
    entries: dict[str, str] = {}
    problems: list[str] = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name, colon, reason = line.partition(": ")
        name, reason = name.strip(), reason.strip()
        if not colon or not reason or not name:
            problems.append(f"exclusion line {number} gives no reason: {line}")
            continue
        if name in entries:
            problems.append(f"{name} is excluded twice")
        entries[name] = reason
    return entries, problems


def _module(test: str) -> str:
    return test.rsplit("::", 1)[0] if "::" in test else ""


def check(list_text: str, workflow_text: str, exclusions_text: str) -> tuple[list[str], dict[str, int]]:
    problems, counts, _ = _evaluate(list_text, workflow_text, exclusions_text)
    return problems, counts


def prune(list_text: str, workflow_text: str, exclusions_text: str) -> tuple[str, list[str]]:
    """The exclusion file without lines that cover no test or name a selected test, and those lines.

    Every other line, its reason and the comments stay as written. Nothing is
    added: a test that becomes unselected stays a failure until a person gives
    it a cohort or a line.
    """
    _, _, drop = _evaluate(list_text, workflow_text, exclusions_text)
    kept, dropped = [], []
    for raw in exclusions_text.splitlines(keepends=True):
        name = raw.strip().partition(": ")[0].strip()
        if raw.strip() and not raw.lstrip().startswith("#") and name in drop:
            dropped.append(name)
        else:
            kept.append(raw)
    return "".join(kept), dropped


def _evaluate(list_text: str, workflow_text: str, exclusions_text: str) -> tuple[list[str], dict[str, int], set[str]]:
    tests = parse_list(list_text)
    excluded, problems = parse_exclusions(exclusions_text)
    default, _featured = pull_request_filters(read_workflow(workflow_text), problems)
    if not tests:
        problems.append("the test list holds no test")
    if not default:
        problems.append(f"no pull-request default-feature cargo test --lib filter found (if: {PULL_REQUEST_CONDITION})")
    used_filters: set[str] = set()
    used_exclusions: set[str] = set()
    drop: set[str] = set()
    counts = {"tests": len(tests), "selected": 0, "excluded": 0}
    for test in tests:
        selected = [key for key in default if _selects(key, test)]
        used_filters.update(selected)
        if selected:
            counts["selected"] += 1
            if test in excluded:
                used_exclusions.add(test)
                drop.add(test)
                problems.append(f"{test} is selected by {', '.join(selected)} and excluded by its own line")
            continue
        covering = test if test in excluded else _module(test) if _module(test) in excluded else None
        if covering is not None:
            used_exclusions.add(covering)
            counts["excluded"] += 1
        else:
            problems.append(f"{test} is selected by no pull-request cohort and covered by no line of {EXCLUSIONS}")
    for key in sorted(set(default) - used_filters):
        problems.append(f"filter {key.lstrip('=')} on {'; '.join(default[key])} selects no test")
    for entry in sorted(set(excluded) - used_exclusions):
        drop.add(entry)
        problems.append(f"exclusion line {entry} covers no test")
    return problems, counts, drop


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", type=Path, required=True, help="output of cargo test --lib -- --list")
    parser.add_argument("--workflow", type=Path, default=ROOT / WORKFLOW)
    parser.add_argument("--exclusions", type=Path, default=ROOT / EXCLUSIONS)
    parser.add_argument("--prune", action="store_true",
                        help="rewrite the exclusion file without lines that cover no test or name a selected test, then check")
    args = parser.parse_args(argv)
    exclusions = args.exclusions.read_text(encoding="utf-8") if args.exclusions.exists() else ""
    if args.prune:
        exclusions, dropped = prune(args.list.read_text(encoding="utf-8"), args.workflow.read_text(encoding="utf-8"), exclusions)
        args.exclusions.write_text(exclusions, encoding="utf-8")
        for name in dropped:
            print(f"removed exclusion line {name}")
    problems, counts = check(
        args.list.read_text(encoding="utf-8"), args.workflow.read_text(encoding="utf-8"), exclusions)
    for problem in problems:
        print(problem, file=sys.stderr)
    summary = f"{counts['tests']} library tests: {counts['selected']} selected on pull requests, {counts['excluded']} left to the full route"
    if problems:
        print(f"lib cohort listing: {len(problems)} problem(s); {summary}", file=sys.stderr)
        return 1
    print(f"lib cohort listing: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
