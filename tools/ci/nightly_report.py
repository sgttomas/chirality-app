#!/usr/bin/env python3
"""Report a full-suite run on main that did not pass as one open issue labelled nightly."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

from tools.ci import nightly_gate


LABEL = "nightly"
DID_NOT_FAIL = frozenset({"success", "skipped", "neutral", None})
PR_NUMBER = re.compile(r"^Merge pull request #(\d+)\b|\(#(\d+)\)$")
MARKDOWN_SPECIAL = re.compile(r"([\\`*_~\[\]()<>|&#])")
PER_PAGE = 100
# Runs examined for a verified pass; reaching this leaves the baseline unknown.
MAX_RUNS = 200
PUBLISH_ATTEMPTS = 4
BACKOFF_SECONDS = 5
GH_TIMEOUT_SECONDS = 60
PUBLISH_ERRORS = (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError)
# Placed after @ and #: GitHub then finds no mention or issue reference to act on.
ZERO_WIDTH_SPACE = "​"


def display(text: str) -> str:
    """Make a repository-supplied string inert: one line, no Markdown, no mentions."""
    escaped = MARKDOWN_SPECIAL.sub(r"\\\1", " ".join(text.split()))
    return escaped.replace("@", f"@{ZERO_WIDTH_SPACE}").replace("#", f"#{ZERO_WIDTH_SPACE}")


def last_pass(repository: str, run_id: int) -> dict | None:
    """Newest run on main, other than this one, whose product job concluded success.

    None means the baseline is unknown: no such run within MAX_RUNS, or history unreadable.
    """
    examined = 0
    for page in range(1, MAX_RUNS // PER_PAGE + 2):
        listed = nightly_gate.gh_api(
            f"repos/{repository}/actions/workflows/{nightly_gate.WORKFLOW}/runs"
            f"?branch=main&status=completed&per_page={PER_PAGE}&page={page}")
        if listed is None:
            return None
        items = listed.get("workflow_runs", [])
        for item in items:
            if item.get("id") == run_id:
                continue
            if examined == MAX_RUNS:
                return None
            examined += 1
            jobs = nightly_gate.run_jobs(repository, item["id"])
            if jobs is None:
                return None
            if nightly_gate.suite_conclusion(jobs) == "success":
                return item
        if len(items) < PER_PAGE:
            return None
    return None


def log(*revisions: str) -> list[tuple[str, str]] | None:
    """Main's own line of commits, newest first, as (sha, subject)."""
    result = subprocess.run(["git", "log", "--first-parent", "--format=%H%x09%s", *revisions],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"::warning::git log failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    return [(sha, subject) for sha, _, subject in
            (line.partition("\t") for line in result.stdout.splitlines())]


def pr_number(subject: str) -> str | None:
    match = PR_NUMBER.search(subject)
    return (match.group(1) or match.group(2)) if match else None


def commit_line(sha: str, subject: str) -> str:
    number = pr_number(subject)
    return f"- `{sha[:12]}` {f'PR #{number}' if number else 'no PR'}: {display(subject)}"


def failing_jobs(jobs: dict | None, gate_result: str, suite_result: str) -> list[str]:
    """Jobs that did not pass; the run's own results stand in if they cannot be read."""
    failing = [f"{display(job['name'])} ({job['conclusion']})" for job in (jobs or {}).get("jobs", [])
               if job.get("conclusion") not in DID_NOT_FAIL]
    if failing:
        return failing
    if gate_result != "success":
        return [f"changed ({gate_result})"]
    return [f"full-suite ({suite_result})"]


def merge_name(head: str, subject: str | None) -> str:
    number = pr_number(subject or "")
    return f"PR #{number}" if number else f"commit {head[:12]}"


def title(head: str, subject: str | None) -> str:
    return f"Full suite did not pass on main after {merge_name(head, subject)}"


def report_body(*, head: str, subject: str | None, run_url: str, event: str, jobs: list[str],
                passed: dict | None, commits: list[tuple[str, str]] | None) -> str:
    lines = [f"The full suite did not pass on `main` after {merge_name(head, subject)}"
             f" (trigger: `{event}`).", "", "Failing run and main commit:", "", run_url, head, "",
             "Failing jobs:", *[f"- {job}" for job in jobs], ""]
    if passed is None:
        lines.append(f"The baseline is unknown: no verified pass was found in the last {MAX_RUNS}"
                     " runs, or they could not be read, so no range of commits is listed.")
    elif commits is None:
        lines.append(f"The last verified pass is run {passed['id']} on `{passed['head_sha']}`;"
                     " the commits since could not be listed.")
    elif not commits:
        lines.append(f"The same commit passed in run {passed['id']}; no commits landed since.")
    else:
        lines += [f"Commits since the last verified pass (run {passed['id']} on"
                  f" `{passed['head_sha']}`):", *[commit_line(*commit) for commit in commits]]
    return "\n".join(lines) + "\n"


def gh(*arguments: str) -> str:
    return subprocess.run(["gh", *arguments], stdout=subprocess.PIPE, text=True, check=True,
                          timeout=GH_TIMEOUT_SECONDS).stdout


def publish_once(repository: str, issue_title: str, body: str) -> str:
    """Comment on the open nightly issue if there is one, otherwise open it."""
    listed = gh("issue", "list", "--repo", repository, "--label", LABEL, "--state", "open",
                "--json", "number", "--limit", "100")
    numbers = [item["number"] for item in json.loads(listed)]
    if numbers:
        gh("issue", "comment", str(min(numbers)), "--repo", repository, "--body", body)
        return f"Commented on nightly issue {min(numbers)}."
    gh("issue", "create", "--repo", repository, "--title", issue_title, "--label", LABEL, "--body", body)
    return "Opened a nightly issue."


def publish(repository: str, issue_title: str, body: str) -> str:
    """Publish with bounded retries. Each attempt lists again, so a retry never opens a second issue."""
    for attempt in range(1, PUBLISH_ATTEMPTS + 1):
        try:
            return publish_once(repository, issue_title, body)
        except PUBLISH_ERRORS as error:
            if attempt == PUBLISH_ATTEMPTS:
                raise
            delay = BACKOFF_SECONDS * 2 ** (attempt - 1)
            print(f"::warning::Publishing attempt {attempt} failed, retrying in {delay}s: {error}",
                  file=sys.stderr)
            time.sleep(delay)
    raise AssertionError("unreachable")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("event", "head", "repository", "server-url", "gate-result", "suite-result"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    args = parser.parse_args(argv)
    head_log = log("-1", args.head)
    subject = head_log[0][1] if head_log else None
    passed = last_pass(args.repository, args.run_id)
    commits = log(f"{passed['head_sha']}..{args.head}") if passed else None
    jobs = failing_jobs(nightly_gate.run_jobs(args.repository, args.run_id),
                        args.gate_result, args.suite_result)
    body = report_body(head=args.head, subject=subject, event=args.event, jobs=jobs, passed=passed,
                       commits=commits,
                       run_url=f"{args.server_url}/{args.repository}/actions/runs/{args.run_id}")
    try:
        print(publish(args.repository, title(args.head, subject), body))
    except PUBLISH_ERRORS as error:
        print(f"::error::The nightly issue could not be published: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
