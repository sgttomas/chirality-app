from __future__ import annotations

import json
import subprocess

import pytest

from tools.ci import nightly_gate, nightly_report as subject


def run(run_id, sha, conclusion, event="push", status="completed"):
    return {"id": run_id, "head_sha": sha, "status": status, "conclusion": conclusion, "event": event}


@pytest.mark.parametrize("items, expected", [
    ([], None),
    ([run(8, "a", "failure"), run(7, "b", "cancelled")], None),
    ([run(8, "a", "failure"), run(7, "b", "success")], 7),
    # This run is never its own last pass.
    ([run(9, "a", "success"), run(8, "b", "success")], 8),
    # A scheduled skip concludes success but ran nothing, whatever the earlier verdict was.
    ([run(8, "a", "success", "schedule"), run(7, "a", "failure"), run(6, "b", "success")], 6),
    ([run(8, "a", "success", "schedule"), run(7, "a", "success")], 7),
    # A scheduled run with no earlier verdict on its commit ran the suite.
    ([run(8, "a", "success", "schedule"), run(7, "b", "failure")], 8),
    # A rerun that passed on a commit that failed earlier is a pass.
    ([run(8, "a", "success", "workflow_dispatch"), run(7, "a", "failure")], 8),
])
def test_last_pass_finds_the_newest_run_that_really_passed(items, expected):
    found = subject.last_pass({"workflow_runs": items}, 9)
    assert (found["id"] if found else None) == expected


def test_last_pass_tolerates_unreadable_runs():
    assert subject.last_pass(None, 9) is None


@pytest.mark.parametrize("line, number", [
    ("Merge pull request #211 from sgttomas/app/x", "211"),
    ("Squashed change (#212)", "212"),
    ("Mentions #5 in passing", None),
])
def test_pr_number_reads_merge_and_squash_subjects(line, number):
    assert subject.pr_number(line) == number


def test_failing_jobs_prefers_the_run_jobs_and_ignores_passes_and_the_running_report():
    jobs = {"jobs": [{"name": "changed", "conclusion": "success"},
                     {"name": "full-suite / App v4 product", "conclusion": "failure"},
                     {"name": "full-suite / sources", "conclusion": "skipped"},
                     {"name": "Report a run that did not pass", "conclusion": None}]}
    assert subject.failing_jobs(jobs, "success", "failure") == ["full-suite / App v4 product (failure)"]


@pytest.mark.parametrize("jobs, gate, suite, expected", [
    (None, "success", "cancelled", ["full-suite (cancelled)"]),
    ({"jobs": []}, "failure", "skipped", ["changed (failure)"]),
])
def test_failing_jobs_falls_back_to_the_workflow_results(jobs, gate, suite, expected):
    assert subject.failing_jobs(jobs, gate, suite) == expected


HEAD = "d" * 40
BASE = "b" * 40
SUBJECT = "Merge pull request #211 from sgttomas/app/x"


def body(**changes):
    values = {"head": HEAD, "subject": SUBJECT, "event": "push", "jobs": ["full-suite / App v4 product (failure)"],
              "run_url": "https://github.example/o/r/actions/runs/9",
              "passed": {"id": 8, "head_sha": BASE}, "commits": [(HEAD, SUBJECT), ("c" * 40, "Direct commit")]}
    return subject.report_body(**{**values, **changes})


def test_report_puts_run_url_and_commit_on_their_own_lines():
    lines = body().splitlines()
    assert "https://github.example/o/r/actions/runs/9" in lines
    assert HEAD in lines


def test_report_names_the_merge_jobs_and_commits_since_the_last_pass():
    text = body()
    assert "after PR #211 (trigger: `push`)" in text
    assert "- full-suite / App v4 product (failure)" in text
    assert f"(run 8 on `{BASE}`):" in text
    assert f"- `{HEAD[:12]}` PR #211: {SUBJECT}" in text
    assert f"- `{'c' * 12}` no PR: Direct commit" in text


@pytest.mark.parametrize("changes, phrase", [
    ({"passed": None, "commits": None}, "No passing verdict was found"),
    ({"commits": None}, "could not be listed"),
    ({"commits": []}, "no commits landed since"),
])
def test_report_says_when_it_cannot_list_the_commits(changes, phrase):
    assert phrase in body(**changes)


def test_title_names_the_merge_or_falls_back_to_the_commit():
    assert subject.title(HEAD, SUBJECT) == "Full suite did not pass on main after PR #211"
    assert subject.title(HEAD, None) == f"Full suite did not pass on main after commit {HEAD[:12]}"


class FakeWorld:
    """Answers the git and gh calls the reporter makes, and records them."""

    def __init__(self, open_issues=(), runs=None):
        self.open_issues, self.calls = list(open_issues), []
        self.runs = runs if runs is not None else {"workflow_runs": [run(8, BASE, "success")]}

    def __call__(self, command, **kwargs):
        self.calls.append(command)
        stdout = ""
        if command[:2] == ["git", "log"]:
            stdout = f"{HEAD}\t{SUBJECT}\n"
        elif command[:2] == ["gh", "api"]:
            payload = self.runs if "/workflows/" in command[2] else {
                "jobs": [{"name": "full-suite / App v4 product", "conclusion": "failure"}]}
            stdout = json.dumps(payload)
        elif command[:3] == ["gh", "issue", "list"]:
            stdout = json.dumps([{"number": number} for number in self.open_issues])
        return subprocess.CompletedProcess(command, 0, stdout, "")

    def issue_writes(self):
        return [command for command in self.calls
                if command[:3] in (["gh", "issue", "create"], ["gh", "issue", "comment"])]


ARGS = ["--event", "push", "--head", HEAD, "--run-id", "9", "--repository", "o/r",
        "--server-url", "https://github.example", "--gate-result", "success", "--suite-result", "failure"]


def test_main_opens_a_labelled_issue_when_none_is_open(monkeypatch):
    world = FakeWorld()
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    [write] = world.issue_writes()
    assert write[:3] == ["gh", "issue", "create"]
    assert write[write.index("--label") + 1] == "nightly"
    assert write[write.index("--title") + 1] == "Full suite did not pass on main after PR #211"
    posted = write[write.index("--body") + 1].splitlines()
    assert "https://github.example/o/r/actions/runs/9" in posted and HEAD in posted
    assert ["git", "log", "--first-parent", "--format=%H%x09%s", f"{BASE}..{HEAD}"] in world.calls


def test_main_comments_on_the_open_issue_instead_of_opening_a_second(monkeypatch):
    world = FakeWorld(open_issues=[14, 12])
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    [write] = world.issue_writes()
    assert write[:4] == ["gh", "issue", "comment", "12"]


def test_main_still_reports_when_earlier_runs_cannot_be_read(monkeypatch):
    world = FakeWorld()
    monkeypatch.setattr(nightly_gate, "fetch", lambda repository: None)
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    [write] = world.issue_writes()
    assert "No passing verdict was found" in write[write.index("--body") + 1]


def test_main_fails_rather_than_risk_a_duplicate_when_issues_cannot_be_listed(monkeypatch):
    def refuse(command, **kwargs):
        if command[:3] == ["gh", "issue", "list"]:
            raise subprocess.CalledProcessError(1, command)
        return FakeWorld()(command, **kwargs)

    monkeypatch.setattr(subprocess, "run", refuse)
    with pytest.raises(subprocess.CalledProcessError):
        subject.main(ARGS)
