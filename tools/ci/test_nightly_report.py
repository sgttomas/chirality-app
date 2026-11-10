from __future__ import annotations

import json
import subprocess

import pytest

from tools.ci import nightly_gate, nightly_report as subject


HEAD = "d" * 40
BASE = "b" * 40
SUBJECT = "Merge pull request #211 from sgttomas/app/x"
ZWSP = "​"


def jobs_for(conclusion):
    if conclusion is None:
        return {"jobs": [{"name": "changed", "status": "completed", "conclusion": "success"}]}
    return {"jobs": [{"name": "full-suite / App v4 product", "status": "completed", "conclusion": conclusion}]}


def install_history(monkeypatch, runs, unreadable=()):
    """runs: newest first as (id, product conclusion, overall conclusion)."""
    reads = []

    def fake(path):
        reads.append(path)
        if "/jobs" in path:
            run_id = int(path.split("/runs/")[1].split("/")[0])
            return None if run_id in unreadable else jobs_for(next(r[1] for r in runs if r[0] == run_id))
        if "listing" in unreadable:
            return None
        page = int(path.rsplit("page=", 1)[1])
        chunk = runs[(page - 1) * 100:page * 100]
        return {"workflow_runs": [{"id": r[0], "head_sha": f"sha{r[0]}", "conclusion": r[2]} for r in chunk]}

    monkeypatch.setattr(nightly_gate, "gh_api", fake)
    return reads


@pytest.mark.parametrize("runs, expected", [
    ([], None),
    ([(8, "failure", "failure"), (7, "cancelled", "cancelled")], None),
    ([(8, "failure", "failure"), (7, "success", "success")], 7),
    # This run is never its own last pass.
    ([(9, "success", "success"), (8, "success", "success")], 8),
    # A scheduled skip concludes success but has no product job, even many times over.
    ([*((n, None, "success") for n in range(60, 10, -1)), (8, "failure", "failure"), (7, "success", "success")], 7),
    # The workflow's own conclusion decides nothing.
    ([(8, "failure", "success"), (7, "success", "failure")], 7),
    ([(8, None, "failure"), (7, "success", "success")], 7),
])
def test_last_pass_is_decided_by_the_product_job(monkeypatch, runs, expected):
    install_history(monkeypatch, runs)
    found = subject.last_pass("o/r", 9)
    assert (found["id"] if found else None) == expected


def test_last_pass_pages_through_history(monkeypatch):
    runs = [*((n, "failure", "failure") for n in range(1000, 900, -1)), (900, "success", "success")]
    reads = install_history(monkeypatch, runs)
    assert subject.last_pass("o/r", 9)["id"] == 900
    assert sum("page=2" in path for path in reads) == 1


def test_last_pass_is_unknown_at_the_bound_and_examines_no_more(monkeypatch):
    runs = [*((n, "failure", "failure") for n in range(2000, 1800, -1)), (1800, "success", "success")]
    reads = install_history(monkeypatch, runs)
    assert subject.last_pass("o/r", 9) is None
    assert sum("/jobs" in path for path in reads) == subject.MAX_RUNS


@pytest.mark.parametrize("unreadable", [("listing",), (8,)])
def test_last_pass_is_unknown_when_history_cannot_be_read(monkeypatch, unreadable):
    install_history(monkeypatch, [(8, "failure", "failure"), (7, "success", "success")], unreadable)
    assert subject.last_pass("o/r", 9) is None


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


@pytest.mark.parametrize("raw, inert", [
    ("ping @octocat now", f"ping @{ZWSP}octocat now"),
    ("@org/team", f"@{ZWSP}org/team"),
    ("use `code` here", r"use \`code\` here"),
    ("[click](https://evil.example)", r"\[click\]\(https://evil.example\)"),
    ("![img](x)", r"!\[img\]\(x\)"),
    ("<img src=x>", r"\<img src=x\>"),
    ("**bold** _it_", r"\*\*bold\*\* \_it\_"),
    ("closes #12", f"closes \\#{ZWSP}12"),
    ("&#64;octocat", f"\\&\\#{ZWSP}64;octocat"),
    (r"already \@escaped", f"already \\\\@{ZWSP}escaped"),
    ("line one\nhttps://github.example/fake\r\n" + "f" * 40, "line one https://github.example/fake " + "f" * 40),
])
def test_display_makes_supplied_text_inert(raw, inert):
    assert subject.display(raw) == inert


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
    assert f"- `{HEAD[:12]}` PR #211: {subject.display(SUBJECT)}" in text
    assert f"- `{'c' * 12}` no PR: Direct commit" in text


def test_report_neutralises_hostile_subjects_branches_and_job_names():
    hostile = "Merge pull request #7 from evil/@octocat-`x`-[click](https://evil.example)"
    jobs = subject.failing_jobs({"jobs": [{"name": "@octocat [click](https://evil.example) `x`",
                                           "conclusion": "failure"}]}, "success", "failure")
    text = body(subject=hostile, commits=[(HEAD, hostile)], jobs=jobs)
    assert "after PR #7 " in text
    assert "@octocat" not in text
    assert "[click](" not in text
    assert "`x`" not in text.replace(r"\`x\`", "")


@pytest.mark.parametrize("changes, phrase", [
    ({"passed": None, "commits": None}, "The baseline is unknown"),
    ({"commits": None}, "could not be listed"),
    ({"commits": []}, "no commits landed since"),
])
def test_report_says_when_it_cannot_list_the_commits(changes, phrase):
    assert phrase in body(**changes)


def test_unknown_baseline_lists_no_range():
    text = body(passed=None, commits=None)
    assert "Commits since" not in text and f"last {subject.MAX_RUNS} runs" in text


def test_title_names_the_merge_or_falls_back_to_the_commit():
    assert subject.title(HEAD, SUBJECT) == "Full suite did not pass on main after PR #211"
    assert subject.title(HEAD, None) == f"Full suite did not pass on main after commit {HEAD[:12]}"


class FakeWorld:
    """Answers the git and gh calls the reporter makes, and records them."""

    def __init__(self, open_issues=(), history=((8, "success"),), refuse=lambda command: False):
        self.open_issues, self.history, self.refuse, self.calls = list(open_issues), history, refuse, []

    def api(self, path):
        if "/jobs" in path:
            run_id = int(path.split("/runs/")[1].split("/")[0])
            return jobs_for(dict(self.history).get(run_id, "failure"))
        return {"workflow_runs": [{"id": run_id, "head_sha": BASE} for run_id, _ in self.history]}

    def __call__(self, command, **kwargs):
        self.calls.append(command)
        if self.refuse(command):
            raise subprocess.CalledProcessError(1, command)
        stdout = ""
        if command[:2] == ["git", "log"]:
            stdout = f"{HEAD}\t{SUBJECT}\n"
        elif command[:2] == ["gh", "api"]:
            stdout = json.dumps(self.api(command[2]))
        elif command[:3] == ["gh", "issue", "list"]:
            stdout = json.dumps([{"number": number} for number in self.open_issues])
        return subprocess.CompletedProcess(command, 0, stdout, "")

    def count(self, verb):
        return sum(command[:3] == ["gh", "issue", verb] for command in self.calls)

    def issue_writes(self):
        return [command for command in self.calls
                if command[:3] in (["gh", "issue", "create"], ["gh", "issue", "comment"])]


ARGS = ["--event", "push", "--head", HEAD, "--run-id", "9", "--repository", "o/r",
        "--server-url", "https://github.example", "--gate-result", "success", "--suite-result", "failure"]


@pytest.fixture
def sleeps(monkeypatch):
    recorded = []
    monkeypatch.setattr(subject.time, "sleep", recorded.append)
    return recorded


def test_main_opens_a_labelled_issue_when_none_is_open(monkeypatch, sleeps):
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
    assert sleeps == []


def test_main_comments_on_the_open_issue_instead_of_opening_a_second(monkeypatch, sleeps):
    world = FakeWorld(open_issues=[14, 12])
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    [write] = world.issue_writes()
    assert write[:4] == ["gh", "issue", "comment", "12"]


def test_main_still_reports_with_an_unknown_baseline_when_runs_cannot_be_read(monkeypatch, sleeps):
    world = FakeWorld()
    monkeypatch.setattr(nightly_gate, "gh_api", lambda path: None)
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    [write] = world.issue_writes()
    assert "The baseline is unknown" in write[write.index("--body") + 1]


def failing_times(times, verb):
    remaining = [times]

    def refuse(command):
        if command[:3] == ["gh", "issue", verb] and remaining[0] > 0:
            remaining[0] -= 1
            return True
        return False

    return refuse


@pytest.mark.parametrize("verb", ["list", "create"])
def test_publish_retries_with_backoff_and_then_succeeds(monkeypatch, sleeps, verb):
    world = FakeWorld(refuse=failing_times(2, verb))
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    assert sleeps == [5, 10]
    assert world.count("create") == (3 if verb == "create" else 1)


def test_a_retry_after_a_create_that_landed_comments_instead_of_duplicating(monkeypatch, sleeps):
    world = FakeWorld()

    def lands_then_errors(command):
        if command[:3] == ["gh", "issue", "create"]:
            world.open_issues.append(30)
            return True
        return False

    world.refuse = lands_then_errors
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 0
    assert world.count("create") == 1 and world.count("comment") == 1


def test_a_gh_call_that_hangs_is_retried(monkeypatch, sleeps):
    world = FakeWorld()
    hung = []

    def hang_once(command, **kwargs):
        assert command[0] == "git" or command[1] == "api" or kwargs["timeout"] == subject.GH_TIMEOUT_SECONDS
        if command[:3] == ["gh", "issue", "list"] and not hung:
            hung.append(command)
            raise subprocess.TimeoutExpired(command, subject.GH_TIMEOUT_SECONDS)
        return world(command, **kwargs)

    monkeypatch.setattr(subprocess, "run", hang_once)
    assert subject.main(ARGS) == 0
    assert sleeps == [5]


@pytest.mark.parametrize("verb", ["list", "create"])
def test_main_fails_visibly_once_the_retries_are_spent(monkeypatch, sleeps, capsys, verb):
    world = FakeWorld(refuse=lambda command: command[:3] == ["gh", "issue", verb])
    monkeypatch.setattr(subprocess, "run", world)
    assert subject.main(ARGS) == 1
    assert world.count(verb) == subject.PUBLISH_ATTEMPTS
    assert sleeps == [5, 10, 20]
    assert "::error::" in capsys.readouterr().err
