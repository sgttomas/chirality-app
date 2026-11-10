#!/usr/bin/env python3
"""Decide whether the nightly full suite runs: only when main moved since the last verdict."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


WORKFLOW = "nightly-full-suite.yml"
# Runs that reached a verdict. A run that skipped the suite concludes "success"
# only because an earlier scheduled run already gave a verdict on the same SHA.
VERDICTS = frozenset({"success", "failure"})


def last_verdict(runs: dict, run_id: int) -> dict | None:
    """Newest completed scheduled run, other than this one, that reached a verdict."""
    for item in runs.get("workflow_runs", []):
        if (item.get("id") != run_id and item.get("status") == "completed"
                and item.get("conclusion") in VERDICTS):
            return item
    return None


def decide(event: str, head: str, run_id: int, runs: dict | None) -> tuple[bool, str]:
    if event != "schedule":
        return True, f"`{event}`: the full suite always runs on `{head}`."
    if runs is None:
        return True, "Earlier nightly runs could not be read, so the full suite runs."
    previous = last_verdict(runs, run_id)
    if previous is None:
        return True, "No earlier scheduled nightly verdict, so the full suite runs."
    if previous.get("head_sha") == head:
        return False, (f"Main is unchanged at `{head}` since scheduled run {previous['id']}"
                       f" ({previous['conclusion']}); the full suite is skipped.")
    return True, (f"Main moved from `{previous.get('head_sha')}` (scheduled run {previous['id']},"
                  f" {previous['conclusion']}) to `{head}`.")


def fetch(repository: str) -> dict | None:
    # Newest first. Fifty runs leave room for cancelled ones between verdicts.
    path = (f"repos/{repository}/actions/workflows/{WORKFLOW}/runs"
            "?event=schedule&branch=main&status=completed&per_page=50")
    result = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"::warning::gh api failed: {result.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print("::warning::gh api returned malformed JSON", file=sys.stderr)
        return None


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
