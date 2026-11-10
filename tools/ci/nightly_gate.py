#!/usr/bin/env python3
"""Decide whether the full suite runs: a scheduled run skips a commit that already has a verdict."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


WORKFLOW = "nightly-full-suite.yml"
# A suite verdict is this job's own conclusion. The workflow's overall conclusion
# also covers gate, runner and reporting failures and runs that skipped the suite.
PRODUCT_JOB = "App v4 product"
VERDICTS = frozenset({"success", "failure"})


def suite_conclusion(jobs: dict) -> str | None:
    """The product job's conclusion in one run's jobs, or None if it never completed."""
    for job in jobs.get("jobs", []):
        # A job in a called workflow is named "<caller job> / <job name>".
        if job.get("name", "").split(" / ")[-1] == PRODUCT_JOB and job.get("status") == "completed":
            return job.get("conclusion")
    return None


def verdict_on(head: str, runs: dict, run_id: int) -> dict | None:
    """Newest run on head, from any trigger and other than this one, with a suite verdict."""
    for item in runs.get("workflow_runs", []):
        if item.get("id") != run_id and item.get("head_sha") == head and item.get("suite") in VERDICTS:
            return item
    return None


def decide(event: str, head: str, run_id: int, runs: dict | None) -> tuple[bool, str]:
    if event != "schedule":
        return True, f"`{event}`: the full suite always runs on `{head}`."
    if runs is None:
        return True, "Earlier runs or their jobs could not be read, so the full suite runs."
    previous = verdict_on(head, runs, run_id)
    if previous is None:
        return True, f"No suite verdict on `{head}` yet, so the full suite runs."
    return False, (f"`{head}` already has a suite verdict from {previous.get('event')} run"
                   f" {previous['id']} ({previous['suite']}); the full suite is skipped.")


def gh_api(path: str) -> dict | None:
    result = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"::warning::gh api failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print("::warning::gh api returned malformed JSON", file=sys.stderr)
        return None


def run_jobs(repository: str, run_id: int) -> dict | None:
    return gh_api(f"repos/{repository}/actions/runs/{run_id}/jobs?per_page=100")


def fetch(repository: str, head: str) -> dict | None:
    """Completed runs on head, each with its suite conclusion; None if any cannot be read."""
    # One page: a commit does not reach 100 runs, and finding no verdict runs the suite.
    listed = gh_api(f"repos/{repository}/actions/workflows/{WORKFLOW}/runs"
                    f"?branch=main&head_sha={head}&status=completed&per_page=100")
    if listed is None:
        return None
    items = []
    for item in listed.get("workflow_runs", []):
        jobs = run_jobs(repository, item["id"])
        if jobs is None:
            return None
        items.append({**item, "suite": suite_conclusion(jobs)})
    return {"workflow_runs": items}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--runs-json", type=Path, help="Recorded runs with suite conclusions (tests only).")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    runs = None
    if args.event == "schedule":
        runs = json.loads(args.runs_json.read_text()) if args.runs_json else fetch(args.repository, args.head)
    run, reason = decide(args.event, args.head, args.run_id, runs)
    print(reason)
    if args.github_output:
        with args.github_output.open("a") as stream:
            stream.write(f"run={'true' if run else 'false'}\n")
    if args.summary:
        with args.summary.open("a") as stream:
            stream.write(f"## Nightly full suite\n\n{reason}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
