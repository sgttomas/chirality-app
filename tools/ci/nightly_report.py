#!/usr/bin/env python3
"""Report a full-suite run on main that did not pass as one open issue labelled nightly."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

from tools.ci import nightly_gate


LABEL = "nightly"
DID_NOT_FAIL = frozenset({"success", "skipped", "neutral", None})
PR_NUMBER = re.compile(r"^Merge pull request #(\d+)\b|\(#(\d+)\)$")


def last_pass(runs: dict | None, run_id: int) -> dict | None:
    """Newest run, other than this one, whose suite ran and passed.

    A scheduled run that found a verdict on its commit skipped the suite and still
    concludes "success", so it says nothing about that commit.
    """
    verdicts = [item for item in (runs or {}).get("workflow_runs", [])
                if item.get("id") != run_id and item.get("status") == "completed"
                and item.get("conclusion") in nightly_gate.VERDICTS]
    for index, item in enumerate(verdicts):
        skipped = item.get("event") == "schedule" and any(
            older.get("head_sha") == item.get("head_sha") for older in verdicts[index + 1:])
        if item["conclusion"] == "success" and not skipped:
            return item
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
    return f"- `{sha[:12]}` {f'PR #{number}' if number else 'no PR'}: {subject}"


def failing_jobs(jobs: dict | None, gate_result: str, suite_result: str) -> list[str]:
    """Jobs that did not pass; the run's own results stand in if they cannot be read."""
    failing = [f"{job['name']} ({job['conclusion']})" for job in (jobs or {}).get("jobs", [])
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
        lines.append("No passing verdict was found in the recent runs, so the commits it covers"
                     " are not listed.")
    elif commits is None:
        lines.append(f"The last passing verdict is run {passed['id']} on `{passed['head_sha']}`;"
                     " the commits since could not be listed.")
    elif not commits:
        lines.append(f"The same commit passed in run {passed['id']}; no commits landed since.")
    else:
        lines += [f"Commits since the last passing verdict (run {passed['id']} on"
                  f" `{passed['head_sha']}`):", *[commit_line(*commit) for commit in commits]]
    return "\n".join(lines) + "\n"


def publish(repository: str, issue_title: str, body: str) -> str:
    """Comment on the open nightly issue if there is one, otherwise open it."""
    listed = subprocess.run(["gh", "issue", "list", "--repo", repository, "--label", LABEL,
                             "--state", "open", "--json", "number", "--limit", "100"],
                            stdout=subprocess.PIPE, text=True, check=True)
    numbers = [item["number"] for item in json.loads(listed.stdout)]
    if numbers:
        subprocess.run(["gh", "issue", "comment", str(min(numbers)), "--repo", repository,
                        "--body", body], check=True)
        return f"Commented on nightly issue {min(numbers)}."
    subprocess.run(["gh", "issue", "create", "--repo", repository, "--title", issue_title,
                    "--label", LABEL, "--body", body], check=True)
    return "Opened a nightly issue."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("event", "head", "repository", "server-url", "gate-result", "suite-result"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    args = parser.parse_args(argv)
    head_log = log("-1", args.head)
    subject = head_log[0][1] if head_log else None
    passed = last_pass(nightly_gate.fetch(args.repository), args.run_id)
    commits = log(f"{passed['head_sha']}..{args.head}") if passed else None
    jobs = failing_jobs(nightly_gate.gh_api(
        f"repos/{args.repository}/actions/runs/{args.run_id}/jobs?per_page=100"),
        args.gate_result, args.suite_result)
    print(publish(args.repository, title(args.head, subject), report_body(
        head=args.head, subject=subject, event=args.event, jobs=jobs, passed=passed, commits=commits,
        run_url=f"{args.server_url}/{args.repository}/actions/runs/{args.run_id}")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
