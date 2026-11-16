#!/usr/bin/env python3
"""Check that every Rust library test in the supplied listing is selected on pull requests or left out on purpose.

Reads the library's default-feature test listing (``cargo test --locked
--manifest-path src-tauri/Cargo.toml --lib -- --list``), the listing of its
ignored tests from the same build (``... -- --list --ignored``),
``.github/workflows/app-v4.yml`` and ``tools/ci/lib_cohort_exclusions.txt``.

A pull-request default-feature filter is a ``LIB_COHORTS`` entry of a
pull-request job that has a step whose run text is exactly ``COHORT_LOOP``
(compared by equality: no loop is recognised from text), or the one literal
test-name filter of a ``cargo test --lib`` command without ``--features`` in a
pull-request job's step (a command at the start of a shell command, after any
``NAME=value`` words). "Selected" means a
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

It refuses, rather than guesses, what it does not read, naming the job and
step and giving the line: more than one test filter, ``--skip``, ``--ignored``
or ``--include-ignored`` on a library test command; a step-level
``LIB_COHORTS``; a step-level ``if`` on a step that has a library test command
(it does not evaluate step conditions; a step-level ``if`` elsewhere is not
refused); a filter containing ``$`` in any run text that is not exactly
``COHORT_LOOP``; a job with ``LIB_COHORTS`` and no step that is exactly
``COHORT_LOOP``, and a job with that step and no ``LIB_COHORTS``; a cohort
containing ``$``; an anchor, alias or merge key (``<<``) anywhere
in the jobs section; a structural line it does not recognise, which includes a
value it reads placed on the next line; a flow form (``{...}``, ``[...]``) on
a key under which it reads something; and, in a value it reads, a form it does
not read exactly (a folded block with blank or more-indented lines, a quoted
scalar followed by other text such as a comment or spread over lines, a block
header other than ``|``, ``|-``, ``>`` or ``>-``).

It needs only the Python standard library, because it runs on the macOS job
that has the listings and no YAML library. A hand-written reader cannot promise
to recognise every YAML form, so its reading is also checked whole:
``tools/ci/test_lib_cohorts.py``, run by repository-checks with PyYAML on every
pull request, compares the reader's reading of the committed workflow with
PyYAML's, job by job (job ids, each job's ``if`` and ``LIB_COHORTS``, and each
step's ``name``, ``if``, ``LIB_COHORTS`` and ``run`` text, exactly), and fails
on any difference or on any refusal. That compares the reading itself, not
filters a shared extraction derives from it.

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


class Anchored(Unreadable):
    """An anchor, alias or merge key: refused wherever it is, read or not."""


ANCHOR_TOKEN = re.compile(r"(?:^|[\[{,\s])[&*][A-Za-z0-9_.-]")


def _scalar(lines: list[str], index: int, key_indent: int, rest: str) -> tuple[str, int]:
    """The value of a key whose text after the colon is rest, as YAML reads it; and the next line index.

    Raises Unreadable for a form the reader does not read exactly.
    """
    rest = rest.strip()
    following = []
    j = index + 1
    while j < len(lines) and (not lines[j].strip() or _indent(lines[j]) > key_indent):
        following.append(lines[j])
        j += 1
    while following and not following[-1].strip():
        following.pop()
        j -= 1
    if rest[:1] in ("&", "*"):
        raise Anchored("an anchor or alias")
    if rest[:1] in ("|", ">"):
        if rest not in ("|", "|-", ">", ">-"):
            raise Unreadable(f"a block scalar header {rest!r}")
        if not following:
            return ("" if rest.endswith("-") else ""), j
        depth = _indent(next(line for line in following if line.strip()))
        if any(line.strip() and _indent(line) < depth for line in following):
            raise Unreadable("a block scalar whose lines are less indented than its first")
        body = [line[depth:] if line.strip() else "" for line in following]
        if rest[0] == ">":
            if any(not line for line in body):
                raise Unreadable("a folded block with blank lines")
            if any(line.startswith(" ") for line in body):
                raise Unreadable("a folded block with more-indented lines")
            value = " ".join(body)
        else:
            value = "\n".join(body)
        return value + ("" if rest.endswith("-") else "\n"), j
    if rest[:1] in ("'", '"'):
        if following:
            raise Unreadable("a quoted scalar over several lines")
        if len(rest) > 1 and rest.endswith(rest[0]):
            if rest[0] == "'":
                inner = rest[1:-1]
                if "'" in inner.replace("''", ""):
                    raise Unreadable("a quoted scalar followed by other text (such as a comment); move the comment onto its own line")
                return inner.replace("''", "'"), j
            try:
                return json.loads(rest), j
            except ValueError:
                raise Unreadable("a double-quoted scalar with escapes it does not read") from None
        raise Unreadable("a quoted scalar followed by other text (such as a comment); move the comment onto its own line")
    if rest[:1] in ("[", "{"):
        if ANCHOR_TOKEN.search(rest) or any(ANCHOR_TOKEN.search(line) for line in following):
            raise Anchored("an anchor or alias in a flow collection")
        raise Unreadable("a flow collection")
    if rest[:1] in ("!", "%", "@", "`", "?"):
        raise Unreadable(f"a value beginning {rest[:1]!r}")
    parts = [rest, *(line.strip() for line in following)]
    if any(not part for part in parts[1:]):
        raise Unreadable("a plain scalar over several lines with blank lines")
    if any(" #" in part or part.startswith("#") for part in parts[1:]) or (" #" in rest and following):
        raise Unreadable("a plain scalar over several lines with a comment")
    if " #" in rest:
        rest = rest[: rest.index(" #")].rstrip()
        parts[0] = rest
    return " ".join(part for part in parts if part).strip(), j


KEY = re.compile(r"(<<|[A-Za-z0-9_.-]+):(?:[ \t]+(.*))?$")
READ_JOB_KEYS = {("if",), ("env", "LIB_COHORTS"), ("steps",)}
READ_STEP_KEYS = {("name",), ("run",), ("if",), ("env", "LIB_COHORTS")}


def _skip(lines: list[str], index: int, indent: int) -> tuple[None, int]:
    """Step past a line and the lines more indented than indent that follow it."""
    j = index + 1
    while j < len(lines) and (not lines[j].strip() or _indent(lines[j]) > indent):
        j += 1
    return None, j


def read_workflow(text: str) -> dict:
    """Read job ids, each job's if and LIB_COHORTS, and its steps' name, if, env LIB_COHORTS and run.

    It parses each structural line of the jobs section and tracks where it
    sits. What it cannot read exactly is recorded under "unreadable" on the
    job or step, and the check refuses it: an anchor, alias or merge key
    anywhere; a structural line it does not recognise (which includes a read
    key's value placed on the next line); and, in a value it reads, any form it
    does not read exactly.
    """
    lines = text.splitlines()
    jobs: dict[str, dict] = {}
    try:
        i = lines.index("jobs:") + 1
    except ValueError:
        return {"jobs": jobs}
    stack: list[tuple[int, str]] = []  # (indent, key or "-") of open mappings and items below jobs:
    job = step = None

    def owner() -> dict:
        return step if step is not None else job

    def refuse(reason: str) -> None:
        # Attributed to the job and step the line is in, with its line number.
        entry = (i + 1, reason)
        if job is not None:
            owner().setdefault("unreadable", []).append(entry)
        else:
            jobs.setdefault("(jobs)", {"steps": []}).setdefault("unreadable", []).append(entry)

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        indent = _indent(line)
        if indent == 0:
            break
        while stack and stack[-1][0] >= indent:
            stack.pop()
        if not stack:
            # A line at the level of the job ids belongs to no job opened before it.
            job = step = None
        key_indent = indent
        if stripped == "-" or stripped.startswith("- "):
            path = [label for _, label in stack]
            stack.append((indent, "-"))
            if len(path) == 2 and path[1] == "steps" and job is not None:
                step = {"_line": i + 1}
                job["steps"].append(step)
            stripped = stripped[1:].lstrip()
            key_indent = indent + (len(line.lstrip()) - len(stripped))
            if not stripped:
                i += 1
                continue
            if not KEY.match(stripped):
                if step is not None and len(path) == 2:
                    refuse(f"a step it does not read: {stripped[:60]!r}")
                    _, i = _skip(lines, i, indent)
                    continue
                try:
                    _, i = _scalar(lines, i, indent, stripped)
                except Anchored as error:
                    refuse(f"a list item: {error}")
                    i += 1
                except Unreadable:
                    i += 1
                continue
        match = KEY.match(stripped)
        if not match:
            refuse(f"a line it does not recognise: {stripped[:60]!r}")
            i += 1
            continue
        key, rest = match.group(1), (match.group(2) or "").strip()
        path = [label for _, label in stack if label != "-"]
        depth = len(path)
        if key == "<<":
            refuse("<<: a merge key")
            i += 1
            continue
        if depth == 0:
            job = jobs.setdefault(key, {"steps": [], "_line": i + 1})
            step = None
            if rest:
                refuse(f"{key}: a job given as a value ({rest[:40]!r})")
                _, i = _skip(lines, i, key_indent)
                continue
            stack.append((key_indent, key))
            i += 1
            continue
        if depth == 1:
            step = None
        relative = tuple(path[1:] + [key])
        in_step = len(path) >= 2 and path[1] == "steps" and step is not None
        if in_step:
            relative = tuple(path[2:] + [key])
            read_paths = READ_STEP_KEYS
        else:
            read_paths = READ_JOB_KEYS
        read = relative in read_paths and relative != ("steps",)
        leads_to_read = any(len(r) > len(relative) and r[:len(relative)] == relative for r in read_paths) or relative == ("steps",)
        if rest[:1] in ("&", "*") or ANCHOR_TOKEN.search(rest) and rest[:1] in ("[", "{"):
            refuse(f"{key}: an anchor or alias")
            _, i = _skip(lines, i, key_indent)
            continue
        if rest and leads_to_read and not (relative == ("steps",) and rest == "[]"):
            refuse(f"{key}: a value it does not read ({rest[:40]!r}) where the check reads what lies below")
            _, i = _skip(lines, i, key_indent)
            continue
        if not rest:
            if rest == "" and read:
                refuse(f"{key}: a value it does not read (empty, or on the next line)")
            stack.append((key_indent, key))
            i += 1
            continue
        value_line = i + 1
        try:
            value, i = _scalar(lines, i, key_indent, rest)
        except Anchored as error:
            refuse(f"{key}: {error}")
            i += 1
            continue
        except Unreadable as error:
            if read:
                refuse(f"{key}: {error}")
                if in_step and relative == ("run",):
                    step["run"] = ""
            i += 1
            while i < len(lines) and (not lines[i].strip() or _indent(lines[i]) > key_indent):
                i += 1
            continue
        if read:
            target = step if in_step else job
            target[f"_line_{relative[-1]}"] = value_line
            if relative[0] == "env":
                target.setdefault("env", {})["LIB_COHORTS"] = value
            else:
                target[relative[0]] = value
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


# The one script that runs every cohort of its job's LIB_COHORTS, one filter each: the run text of the
# two shard steps, after removing the block's common indentation and one trailing newline. A step counts
# as running the cohorts only if its run text is exactly this; no loop is recognised from text.
COHORT_LOOP = (
    "set -f\n"
    "for cohort in $LIB_COHORTS; do\n"
    '  cargo test --locked --manifest-path src-tauri/Cargo.toml --lib "$cohort" -- --test-threads=1\n'
    "done"
)
NOT_THE_LOOP = (
    "a filter containing $: this step's script is not the cohort loop the check knows "
    "(tools/ci/check_lib_cohorts.py, COHORT_LOOP); either restore that script or change the constant with it "
    "and say why in the pull request"
)


def is_the_cohort_loop(run: str) -> bool:
    """Whether a step's run text is exactly COHORT_LOOP (one trailing newline allowed)."""
    return (run[:-1] if run.endswith("\n") else run) == COHORT_LOOP


def pull_request_filters(workflow: dict, problems: list[str] | None = None) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Default-feature and feature filters of the pull-request jobs, each with where it is.

    Refusals, unrecognised job conditions and cohorts declared but never run
    (or run but never declared) are added to problems.
    """
    default: dict[str, list[str]] = {}
    featured: dict[str, list[str]] = {}

    def report(where: str, text: str, line: int | None) -> None:
        if problems is not None:
            problems.append(f"{where}: the check cannot read {text}" + (f" (line {line})" if line else ""))

    for job_id, job in (workflow.get("jobs") or {}).items():
        for line, text in job.get("unreadable") or []:
            report(job_id, text, line)
        condition = job.get("if")
        pull_request = condition is None or condition == PULL_REQUEST_CONDITION
        recognised = pull_request or condition == FULL_ROUTE_CONDITION
        declared = (job.get("env") or {}).get("LIB_COHORTS")
        cohorts = str(declared or "").split()
        loops = 0
        for step in job.get("steps") or []:
            run = step.get("run")
            where = f"{job_id} / {step.get('name', '(unnamed step)')}"
            run_line = step.get("_line_run", step.get("_line"))
            for line, text in step.get("unreadable") or []:
                report(where, text, line)
            if not isinstance(run, str):
                continue
            loop = is_the_cohort_loop(run)
            filters = [] if loop else cargo_lib_filters(run)
            if (step.get("env") or {}).get("LIB_COHORTS") is not None:
                report(where, "a step-level LIB_COHORTS (the check reads only the job's)", step.get("_line_LIB_COHORTS"))
            if (loop or filters) and "if" in step:
                report(where, "a step-level if on a step with a library test command "
                              "(the check does not evaluate step conditions)", step.get("_line_if"))
            for name, _exact, _features, command_refusals in filters:
                for text in command_refusals:
                    report(where, text, run_line)
                if "$" in name:
                    report(where, NOT_THE_LOOP, run_line)
            if (loop or filters) and not recognised:
                if problems is not None:
                    problems.append(
                        f"job {job_id} has a cargo test --lib line and an if the check does not recognise: {condition!r} "
                        f"(pull request: {PULL_REQUEST_CONDITION!r}; full route: {FULL_ROUTE_CONDITION!r})")
                break
            if loop:
                loops += 1
                for value in cohorts:
                    if "$" in value:
                        report(job_id, f"a cohort containing $ ({value!r}) in LIB_COHORTS", job.get("_line_LIB_COHORTS"))
                    elif pull_request:
                        default.setdefault(value, []).append(where)
                continue
            if not pull_request:
                continue
            for name, exact, features, _refusals in filters:
                if "$" in name:
                    continue
                key = f"={name}" if exact else name
                (featured if features else default).setdefault(key, []).append(where)
        if declared is not None and not loops:
            report(job_id, "LIB_COHORTS declared but no step whose run text is exactly the cohort loop "
                           "(tools/ci/check_lib_cohorts.py, COHORT_LOOP), so the cohorts are never run",
                   job.get("_line_LIB_COHORTS"))
        if loops and declared is None:
            report(job_id, "a step running the cohort loop in a job with no LIB_COHORTS", job.get("_line"))
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
    added. A test that becomes unselected is a failure until a person gives it
    a cohort or a line, unless a module line already covers it: a test directly
    in an excluded module is absorbed by that module's line without notice.
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
