"""Regressions for check_web_test_listing.py, and the check on this repository."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_web_test_listing as listing  # noqa: E402

FOCUSED = f'"{listing.PULL_REQUEST_CONDITION}"'
FULL = "\"github.event_name == 'workflow_dispatch' || inputs.full_suite\""


def workflow(focused_runs: list[str], full_runs: list[str] = ()) -> str:
    def steps(runs):
        return "".join(f"      - name: step {i}\n        run: {run}\n" for i, run in enumerate(runs))
    return (
        "defaults:\n  run:\n    working-directory: app\n"
        "jobs:\n"
        f"  focused:\n    if: {FOCUSED}\n    steps:\n{steps(focused_runs) or '      []\n'}"
        f"  product:\n    if: {FULL}\n    steps:\n{steps(full_runs) or '      []\n'}"
    )


@pytest.fixture
def root(tmp_path):
    tests = tmp_path / "app" / "tests"
    tests.mkdir(parents=True)
    for name in ("a.test.mjs", "b.test.mjs", "c.test.mjs"):
        (tests / name).write_text("")
    (tests / "helper.mjs").write_text("")
    return tmp_path


def test_every_file_listed_or_excluded_passes(root):
    text = workflow(["node --test tests/a.test.mjs tests/b.test.mjs"])
    assert listing.check(root, text, "c.test.mjs: needs the supplier; runs in the full route's npm test\n") == []


def test_unlisted_file_is_named(root):
    problems = listing.check(root, workflow(["node --test tests/a.test.mjs tests/b.test.mjs"]), "")
    assert problems == ["app/tests/c.test.mjs is run by no pull-request job and is not in tools/ci/web_test_exclusions.txt"]


def test_full_route_lines_do_not_count(root):
    text = workflow(["node --test tests/a.test.mjs tests/b.test.mjs"], ["node --test tests/c.test.mjs"])
    assert listing.check(root, text, "") == [
        "app/tests/c.test.mjs is run by no pull-request job and is not in tools/ci/web_test_exclusions.txt"]


def test_jobs_are_told_apart_by_condition_not_position(root):
    # The full route first and the focused job second: still only the focused job counts.
    text = (
        "defaults:\n  run:\n    working-directory: app\njobs:\n"
        f"  product:\n    if: {FULL}\n    steps:\n      - run: node --test tests/c.test.mjs\n"
        f"  focused:\n    if: {FOCUSED}\n    steps:\n      - run: node --test tests/a.test.mjs tests/b.test.mjs\n"
    )
    assert [p for p in listing.check(root, text, "") if "c.test.mjs" in p]


def test_missing_file_on_a_line_or_in_the_list_is_named(root):
    text = workflow(["node --test tests/a.test.mjs tests/b.test.mjs tests/gone.test.mjs"], ["node --test tests/lost.test.mjs"])
    problems = listing.check(root, text, "c.test.mjs: reason\nvanished.test.mjs: reason\n")
    assert "app/tests/gone.test.mjs named on focused / step 0 does not exist" in problems
    assert "app/tests/lost.test.mjs named on product / step 0 does not exist" in problems
    assert "app/tests/vanished.test.mjs in tools/ci/web_test_exclusions.txt does not exist" in problems
    assert len(problems) == 3


def test_file_in_both_is_named(root):
    problems = listing.check(root, workflow(["node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs"]), "c.test.mjs: reason\n")
    assert problems == ["app/tests/c.test.mjs is both run by a pull-request job (focused / step 0) and in tools/ci/web_test_exclusions.txt"]


def test_no_test_files_is_not_a_pass(tmp_path):
    (tmp_path / "app" / "tests").mkdir(parents=True)
    assert "no *.test.mjs file found under app/tests" in listing.check(tmp_path, workflow(["node --test --version"]), "")


def test_no_pull_request_line_is_not_a_pass(root):
    problems = listing.check(root, workflow(["npm run build"], ["node --test tests/a.test.mjs"]), "a.test.mjs: r\nb.test.mjs: r\nc.test.mjs: r\n")
    assert problems == [f"no node --test line found in a pull-request job (if: {listing.PULL_REQUEST_CONDITION})"]


def test_exclusion_without_reason_or_twice_fails(root):
    text = workflow(["node --test tests/a.test.mjs"])
    problems = listing.check(root, text, "b.test.mjs\nc.test.mjs: r\nc.test.mjs: again\n")
    assert "exclusion line 1 gives no reason: b.test.mjs" in problems
    assert "c.test.mjs is excluded twice" in problems


def test_commands_are_split_at_shell_operators_and_continuations(root):
    text = workflow(['|\n          node --test tests/a.test.mjs \\\n            tests/b.test.mjs && echo tests/c.test.mjs'])
    assert listing.check(root, text, "") == [
        "app/tests/c.test.mjs is run by no pull-request job and is not in tools/ci/web_test_exclusions.txt"]


def test_an_argument_that_is_not_a_listed_test_file_fails(root):
    problems = listing.check(root, workflow(["node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs tests/ tests/helper.mjs"]), "")
    assert problems == [
        "tests/ on focused / step 0 is not a *.test.mjs file under app/tests",
        "tests/helper.mjs on focused / step 0 is not a *.test.mjs file under app/tests",
    ]


def test_this_repository_lists_every_web_test_file():
    root = listing.ROOT
    problems = listing.check(
        root,
        (root / listing.WORKFLOW).read_text(encoding="utf-8"),
        (root / listing.EXCLUSIONS).read_text(encoding="utf-8"),
    )
    assert problems == []


def test_an_environment_prefixed_line_naming_a_missing_file_fails(root):
    text = workflow(["node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs",
                     "REVIEW=1 node --test tests/review-env-missing.test.mjs"])
    assert listing.check(root, text, "") == [
        "app/tests/review-env-missing.test.mjs named on focused / step 1 does not exist"]


def test_an_environment_prefixed_line_is_a_files_listing(root):
    text = workflow(["node --test tests/a.test.mjs tests/b.test.mjs",
                     "A=1 B='two words' env C=3 node --test tests/c.test.mjs && echo done"])
    assert listing.check(root, text, "") == []


def _jobs(*jobs: tuple[str, str | None, str]) -> str:
    text = "defaults:\n  run:\n    working-directory: app\njobs:\n"
    for name, condition, run in jobs:
        text += f"  {name}:\n" + (f"    if: {condition}\n" if condition is not None else "")
        text += f"    steps:\n      - name: s\n        run: {run}\n"
    return text


def test_a_job_with_an_unrecognised_condition_and_a_node_line_fails(root):
    text = _jobs(("focused", FOCUSED, "node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs"),
                 ("reworded", "\"github.event_name == 'pull_request'\"", "node --test tests/a.test.mjs"))
    assert listing.check(root, text, "") == [
        "job reworded has a node --test line and an if the check does not recognise: \"github.event_name == 'pull_request'\" "
        f"(pull request: {listing.PULL_REQUEST_CONDITION!r}; full route: {listing.FULL_ROUTE_CONDITION!r})"]


def test_a_job_with_an_unrecognised_condition_and_no_node_line_is_not_a_finding(root):
    text = _jobs(("focused", FOCUSED, "node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs"),
                 ("result", "always()", "test success = success"))
    assert listing.check(root, text, "") == []


def test_a_job_with_no_condition_counts_as_a_pull_request_job(root):
    text = _jobs(("focused", FOCUSED, "node --test tests/a.test.mjs tests/b.test.mjs"),
                 ("unconditioned", None, "node --test tests/c.test.mjs"))
    assert listing.check(root, text, "") == []
    # And it alone is enough to be a pull-request node --test line.
    assert listing.check(root, _jobs(("unconditioned", None, "node --test tests/a.test.mjs tests/b.test.mjs tests/c.test.mjs")), "") == []
