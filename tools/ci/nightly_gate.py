#!/usr/bin/env python3
"""Decide whether the full suite runs: a scheduled run skips a commit that already has a verdict."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


WORKFLOW = "nightly-full-suite.yml"
# Runs that reached a verdict. A run that skipped the suite concludes "success"
# only because an earlier run already gave a verdict on the same SHA.
VERDICTS = frozenset({"success", "failure"})


def verdict_on(head: str, runs: dict, run_id: int) -> dict | None:
    """Newest completed run on head, from any trigger and other than this one, with a verdict."""
    for item in runs.get("workflow_runs", []):
        if (item.get("id") != run_id and item.get("head_sha") == head
                and item.get("status") == "completed" and item.get("conclusion") in VERDICTS):
            return item
    return None


def decide(event: str, head: str, run_id: int, runs: dict | None) -> tuple[bool, str]:
    if event != "schedule":
        return True, f"`{event}`: the full suite always runs on `{head}`."
    if runs is None:
        return True, "Earlier runs could not be read, so the full suite runs."
    previous = verdict_on(head, runs, run_id)
    if previous is None:
        return True, f"No completed verdict on `{head}` yet, so the full suite runs."
    return False, (f"`{head}` already has a verdict from {previous.get('event')} run"
                   f" {previous['id']} ({previous['conclusion']}); the full suite is skipped.")


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


def fetch(repository: str) -> dict | None:
    # Newest first, every trigger. Fifty runs leave room for cancelled ones between verdicts.
    return gh_api(f"repos/{repository}/actions/workflows/{WORKFLOW}/runs"
                  "?branch=main&status=completed&per_page=50")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--runs-json", type=Path, help="Recorded runs response (tests only).")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args(argv)
    runs = None
    if args.event == "schedule":
        runs = json.loads(args.runs_json.read_text()) if args.runs_json else fetch(args.repository)
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
