#!/usr/bin/env python3
"""Check that every Rust library test in the supplied listing is selected on pull requests or left out on purpose.

Reads the library's default-feature test listing (``cargo test --locked
--manifest-path src-tauri/Cargo.toml --lib -- --list``), the listing of its
ignored tests from the same build (``... -- --list --ignored``),
``.github/workflows/app-v4.yml`` and ``tools/ci/lib_cohort_exclusions.txt``.

A pull-request default-feature filter is a ``LIB_COHORTS`` entry of a
pull-request job, or the one test-name filter of a ``cargo test --lib``
command without ``--features`` in a pull-request job's step (a command at the
start of a shell command, after any ``NAME=value`` words). "Selected" means a
filter's name matches the test as libtest matches (the path contains the
filter; equals it under ``--exact``). It is a name match: it does not show
that the test's body executes.

An ignored (``#[ignore]``) test is its own category. No filter's name match
counts as selecting it, and it must be covered by a line whose reason begins
``ignored (#[ignore])``; a test that is not ignored may not be covered by
such a line.

An exclusion line names a test module and covers the tests directly in that
module that no filter selects, not those of its submodules; or it names one
test, and that line takes precedence over its module's line. Each line gives
its reason.

Jobs are told apart by their ``if``: the pull-request condition and the
full-route condition below, exactly as written. A job with no ``if`` counts as
a pull-request job, because the workflow runs it on every event that calls it,
the pull-request call included. A job with a ``cargo test --lib`` line and any
other ``if`` fails the check.

The check fails, naming them, when: a test that is not ignored is selected by
no pull-request default-feature filter and covered by no line; an ignored test
is covered by no line, or by a line that does not say it is ignored; a line
that says ignored covers a test that is not; a default-feature pull-request
filter selects no test that is not ignored; an exclusion line covers no test;
a line naming one test names a selected test; a line has no reason or
repeats; the ignored listing names a test the listing does not; or the
listing holds no test or the workflow no filter.

It refuses, rather than guesses, what its reader does not read, naming the job
and step: more than one test filter, ``--skip``, ``--ignored`` or
``--include-ignored`` on a library test command; a step-level ``LIB_COHORTS``;
a step-level ``if`` on a step with a library test command (it does not
evaluate step conditions); a ``${{ }}`` expression in a filter; and, in a
value it reads, a folded block with blank lines, a quoted scalar followed by
other text such as a comment, or an anchor, alias or merge key.

It needs only the Python standard library, because it runs on the macOS job
that has the listings and no YAML library. ``read_workflow`` reads the few
things the check uses from the workflow's own layout. ``tools/ci/test_lib_cohorts.py``,
run by repository-checks with PyYAML, fails when this reading and PyYAML's give
different jobs, conditions or cohorts; both readings then pass through the same
extraction, so that test cannot catch a misreading the extraction itself makes.
The refusals above are the answer to that.

What it establishes: every test in the supplied default-feature listing is
matched by name by a pull-request default-feature filter, or is ignored, or is
covered by a line with a reason. What it does not establish: that a selected
test passes or that its body runs; anything about a test compiled only with a
feature (it is not in the listing); anything about a reason's text beyond the
ignored marker, such as the named feature step, web fixture, parent test or the
full route's command. A test left to the full route runs on main nightly and on
a product dispatch, not on the pull request that changes it. A new direct test
in an already excluded module is covered by the module line without notice (a
new submodule is not). Removing a filter that selected a direct test of an
excluded module is absorbed the same way: the module line covers that test
and the check still passes.
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


class Unreadable(Exception):
    """A value the reader does not understand; the check refuses it rather than guess."""


def _scalar(lines: list[str], index: int, key_indent: int, rest: str) -> tuple[str, int]:
    """The value of a key whose text after the colon is rest; returns it and the next line index."""
    rest = rest.strip()
    if rest[:1] in ("&", "*"):
        raise Unreadable("an anchor or alias")
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
        if rest[0] == ">" and any(not line.strip() for line in body):
            raise Unreadable("a folded block with blank lines")
        depth = min((_indent(line) for line in body if line.strip()), default=0)
        body = [line[depth:] for line in body]
        return ("\n" if rest[0] == "|" else " ").join(body if rest[0] == "|" else [b for b in body if b]), j
    if rest.startswith("'") and rest.endswith("'") and len(rest) > 1:
        return rest[1:-1].replace("''", "'"), j
    if rest.startswith('"') and rest.endswith('"') and len(rest) > 1:
        return json.loads(rest), j
    if rest[:1] in ("'", '"'):
        raise Unreadable("a quoted scalar followed by other text (such as a comment)")
    return " ".join([rest, *(line.strip() for line in following if line.strip())]).strip(), j


KEY = re.compile(r"(-\s+)?([A-Za-z0-9_-]+):(?:\s+(.*))?$")


def read_workflow(text: str) -> dict:
    """Read job ids, each job's if and LIB_COHORTS, and its steps' name, if, env LIB_COHORTS and run.

    What it cannot read is recorded under "unreadable" on the job or step,
    and the check refuses it.
    """
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
        if indent == job_key_indent and not dash:
            step = None
        if dash:
            step = {}
            job["steps"].append(step)
            step_key_indent = indent + len(dash)
        owner = step if step is not None else job
        if key == "<<" or (rest.strip()[:1] in ("&", "*")):
            owner.setdefault("unreadable", []).append(f"{key}: an anchor, alias or merge key")
            i += 1
            continue
        try:
            if step is None and indent == job_key_indent and key == "if":
                job["if"], i = _scalar(lines, i, indent, rest)
                continue
            if key == "LIB_COHORTS":
                owner.setdefault("env", {})["LIB_COHORTS"], i = _scalar(lines, i, indent, rest)
                continue
            if step is not None and key in ("name", "run", "if") and (dash or indent == step_key_indent):
                step[key], i = _scalar(lines, i, step_key_indent, rest)
                continue
        except Unreadable as error:
            owner.setdefault("unreadable", []).append(f"{key}: {error}")
            if key == "run":
                step[key] = ""
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


TEST_VALUE_FLAGS = {"--skip", "--test-threads", "--format", "--color", "--logfile", "-Z", "--shuffle-seed", "--report-time"}


def cargo_lib_filters(run: str) -> list[tuple[str, bool, bool, list[str]]]:
    """(filter, exact, with_features, refusals) for each `cargo test --lib` command of a script.

    A refusal names what the check does not read in that command.
    """
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
        later, skip = [], False
        for token in after:
            if skip:
                skip = False
            elif token in TEST_VALUE_FLAGS:
                skip = True
            elif not token.startswith("-"):
                later.append(token)
        refusals = []
        if len(positional) + len(later) > 1:
            refusals.append("more than one test filter (the check reads one)")
        if any(t == "--skip" or t.startswith("--skip=") for t in after):
            refusals.append("--skip (the check does not read it)")
        if any(t in ("--ignored", "--include-ignored") for t in after):
            refusals.append("--ignored or --include-ignored (the check does not count runs of ignored tests)")
        name = (positional or later or [""])[0]
        found.append((name, "--exact" in after, features, refusals))
    return found


def pull_request_filters(workflow: dict, problems: list[str] | None = None) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Default-feature and feature filters of the pull-request jobs, each with where it is.

    A job with a cargo test --lib line whose if is neither condition is named
    in problems.
    """
    default: dict[str, list[str]] = {}
    featured: dict[str, list[str]] = {}
    for job_id, job in (workflow.get("jobs") or {}).items():
        if job.get("unreadable") and problems is not None:
            for refusal in job["unreadable"]:
                problems.append(f"{job_id}: the check cannot read {refusal}")
        condition = job.get("if")
        pull_request = condition is None or condition == PULL_REQUEST_CONDITION
        recognised = pull_request or condition == FULL_ROUTE_CONDITION
        cohorts = str((job.get("env") or {}).get("LIB_COHORTS") or "").split()
        for step in job.get("steps") or []:
            run = step.get("run")
            where = f"{job_id} / {step.get('name', '(unnamed step)')}"
            if not isinstance(run, str):
                for refusal in step.get("unreadable") or []:
                    if problems is not None:
                        problems.append(f"{where}: the check cannot read {refusal}")
                continue
            filters = cargo_lib_filters(run)
            refusals = list(step.get("unreadable") or [])
            if (step.get("env") or {}).get("LIB_COHORTS") is not None:
                refusals.append("a step-level LIB_COHORTS (the check reads only the job's)")
            if filters and "if" in step:
                refusals.append("a step-level if on a library test command (the check does not evaluate step conditions)")
            for name, _exact, _features, command_refusals in filters:
                refusals += command_refusals
                values = cohorts if "LIB_COHORTS" in run and name.startswith("$") else [name]
                if any("${{" in value for value in values):
                    refusals.append("a ${{ }} expression in a filter")
            if refusals and problems is not None:
                for refusal in dict.fromkeys(refusals):
                    problems.append(f"{where}: the check cannot read {refusal}")
            if filters and not recognised:
                if problems is not None:
                    problems.append(
                        f"job {job_id} has a cargo test --lib line and an if the check does not recognise: {condition!r} "
                        f"(pull request: {PULL_REQUEST_CONDITION!r}; full route: {FULL_ROUTE_CONDITION!r})")
                break
            if not pull_request:
                continue
            for name, exact, features, _refusals in filters:
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


IGNORED_MARK = "ignored (#[ignore])"


def check(list_text: str, workflow_text: str, exclusions_text: str, ignored_text: str = "") -> tuple[list[str], dict[str, int]]:
    problems, counts, _ = _evaluate(list_text, workflow_text, exclusions_text, ignored_text)
    return problems, counts


def prune(list_text: str, workflow_text: str, exclusions_text: str, ignored_text: str = "") -> tuple[str, list[str]]:
    """The exclusion file without lines that cover no test or name a selected test, and those lines.

    Every other line, its reason and the comments stay as written. Nothing is
    added: a test that becomes unselected stays a failure until a person gives
    it a cohort or a line.
    """
    _, _, drop = _evaluate(list_text, workflow_text, exclusions_text, ignored_text)
    kept, dropped = [], []
    for raw in exclusions_text.splitlines(keepends=True):
        name = raw.strip().partition(": ")[0].strip()
        if raw.strip() and not raw.lstrip().startswith("#") and name in drop:
            dropped.append(name)
        else:
            kept.append(raw)
    return "".join(kept), dropped


def _evaluate(list_text: str, workflow_text: str, exclusions_text: str,
              ignored_text: str) -> tuple[list[str], dict[str, int], set[str]]:
    tests = parse_list(list_text)
    ignored = set(parse_list(ignored_text))
    excluded, problems = parse_exclusions(exclusions_text)
    for test in sorted(ignored - set(tests)):
        problems.append(f"{test} is in the ignored list but not in the test list (were both listed from one build?)")
    default, _featured = pull_request_filters(read_workflow(workflow_text), problems)
    if not tests:
        problems.append("the test list holds no test")
    if not default:
        problems.append(f"no pull-request default-feature cargo test --lib filter found (if: {PULL_REQUEST_CONDITION})")
    used_filters: set[str] = set()
    used_exclusions: set[str] = set()
    drop: set[str] = set()
    counts = {"tests": len(tests), "selected": 0, "excluded": 0, "ignored": 0}
    for test in tests:
        selected = [key for key in default if _selects(key, test)]
        if test in ignored:
            # An ignored test is not run by a filter, so a filter's name match is not a selection.
            covering = test if test in excluded else _module(test) if _module(test) in excluded else None
            if covering is None:
                problems.append(f"{test} is ignored (#[ignore]) and covered by no line of {EXCLUSIONS}")
            else:
                used_exclusions.add(covering)
                if not excluded[covering].startswith(IGNORED_MARK):
                    problems.append(f"{test} is ignored (#[ignore]) but its line {covering} does not say so "
                                    f"(its reason must begin {IGNORED_MARK!r})")
            counts["ignored"] += 1
            continue
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
            if excluded[covering].startswith(IGNORED_MARK):
                problems.append(f"{test} is not ignored but its line {covering} says it is")
        else:
            problems.append(f"{test} is selected by no pull-request cohort and covered by no line of {EXCLUSIONS}")
    for key in sorted(set(default) - used_filters):
        problems.append(f"default-feature filter {key.lstrip('=')} on {'; '.join(default[key])} selects no test that is not ignored")
    for entry in sorted(set(excluded) - used_exclusions):
        drop.add(entry)
        problems.append(f"exclusion line {entry} covers no test")
    return problems, counts, drop


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", type=Path, required=True, help="output of cargo test --lib -- --list")
    parser.add_argument("--ignored-list", type=Path, required=True,
                        help="output of cargo test --lib -- --list --ignored, from the same build")
    parser.add_argument("--workflow", type=Path, default=ROOT / WORKFLOW)
    parser.add_argument("--exclusions", type=Path, default=ROOT / EXCLUSIONS)
    parser.add_argument("--prune", action="store_true",
                        help="rewrite the exclusion file without lines that cover no test or name a selected test, then check")
    args = parser.parse_args(argv)
    exclusions = args.exclusions.read_text(encoding="utf-8") if args.exclusions.exists() else ""
    if args.prune:
        exclusions, dropped = prune(args.list.read_text(encoding="utf-8"), args.workflow.read_text(encoding="utf-8"),
                                    exclusions, args.ignored_list.read_text(encoding="utf-8"))
        args.exclusions.write_text(exclusions, encoding="utf-8")
        for name in dropped:
            print(f"removed exclusion line {name}")
    problems, counts = check(
        args.list.read_text(encoding="utf-8"), args.workflow.read_text(encoding="utf-8"), exclusions,
        args.ignored_list.read_text(encoding="utf-8"))
    for problem in problems:
        print(problem, file=sys.stderr)
    summary = (f"{counts['tests']} library tests (default features): {counts['selected']} selected by name on pull requests, "
               f"{counts['excluded']} left out by a line, {counts['ignored']} ignored and counted in neither")
    if problems:
        print(f"lib cohort listing: {len(problems)} problem(s); {summary}", file=sys.stderr)
        return 1
    print(f"lib cohort listing: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
