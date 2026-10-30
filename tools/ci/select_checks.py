#!/usr/bin/env python3
"""Select PR verification from committed changes; validate the aggregate gate."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


# Exact documentary paths, not extension or directory-wide exemptions. Packaged
# guidance, Design sources, fixtures and unfamiliar paths retain product checks.
PROSE_PATHS = frozenset({
    "AGENTS.md",
    "README.md",
    "init/README.md",
    "init/init-prompt.md",
    "loop/LOOP_INIT.md",
    "docs/CI_SELECTION.md",
    "execution/_Coordination/CURRENT_EXECUTION_BASIS.md",
    "execution/_Coordination/WINDOWS_UNDERTAKING.md",
})
OID = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
RAW_HEADER = re.compile(
    rb":([0-7]{6}) ([0-7]{6}) ([0-9a-f]{40}|[0-9a-f]{64}) "
    rb"([0-9a-f]{40}|[0-9a-f]{64}) ([AMDT])\Z"
)


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def commit(repo: Path, revision: str) -> str:
    # Workflow inputs are full commit identities, never branch names or options.
    if not OID.fullmatch(revision):
        raise ValueError("Expected a full commit SHA")
    resolved = git(repo, "rev-parse", "--verify", revision + "^{commit}").decode().strip()
    if resolved != revision:
        raise ValueError("Commit identity did not resolve exactly")
    return resolved


def parse_changes(raw: bytes) -> list[dict[str, str]]:
    if not raw:
        return []
    fields = raw.split(b"\0")
    if fields.pop() != b"" or len(fields) % 2:
        raise ValueError("Malformed NUL-delimited Git diff")
    changes = []
    for header, path in zip(fields[::2], fields[1::2]):
        match = RAW_HEADER.fullmatch(header)
        if match is None or not path:
            raise ValueError("Malformed Git change record")
        old_mode, new_mode, _, _, status = match.groups()
        changes.append({
            "path": os.fsdecode(path),
            "status": status.decode(),
            "old_mode": old_mode.decode(),
            "new_mode": new_mode.decode(),
        })
    return changes


def classify(change: dict[str, str]) -> dict[str, str]:
    reason = "Path is not in the documentary allowlist"
    if change["status"] not in {"A", "M"}:
        reason = "Deletion or file-type change requires product verification"
    elif change["new_mode"] != "100644" or change["old_mode"] not in {"000000", "100644"}:
        reason = "Only ordinary non-executable documentary files qualify"
    elif change["path"] in PROSE_PATHS:
        return {**change, "checks": "repository", "reason": "Allowlisted documentary file"}
    return {**change, "checks": "product", "reason": reason}


def select(repo: Path, event: str, base: str, head: str) -> dict:
    head = commit(repo, head)
    if event == "workflow_dispatch":
        return {"head": head, "mode": "product", "run_product": True,
                "reason": "Manual dispatch retains product verification", "changes": []}
    if event != "pull_request":
        raise ValueError("Unsupported CI event")
    base = commit(repo, base)
    bases = git(repo, "merge-base", "--all", base, head).decode().splitlines()
    if len(bases) != 1 or not OID.fullmatch(bases[0]):
        raise ValueError("Expected one unambiguous PR merge base")
    # Disable rename detection: a rename is a deletion plus an addition, so both
    # paths participate. Raw records also retain modes, deletions and odd names.
    changes = [classify(change) for change in parse_changes(git(
        repo, "diff", "--raw", "--no-abbrev", "--no-renames", "--no-ext-diff",
        "--no-textconv", "-z", bases[0], head, "--",
    ))]
    run_product = not changes or any(change["checks"] == "product" for change in changes)
    return {"base": base, "merge_base": bases[0], "head": head,
            "mode": "product" if run_product else "prose", "run_product": run_product,
            "reason": "Empty change set retains product verification" if not changes else
                      "Union of checks required by all changed paths", "changes": changes}


def require_success(needs: dict) -> None:
    if not isinstance(needs, dict) or set(needs) != {"repository-checks", "app-v4"}:
        raise ValueError("Aggregate requires exactly the declared verification jobs")
    repository = needs["repository-checks"]
    if repository.get("result") != "success":
        raise ValueError("Repository checks and change selection must succeed")
    outputs = repository.get("outputs", {})
    mode, product = outputs.get("selection_mode"), outputs.get("run_product")
    if (mode, product) not in {("prose", "false"), ("product", "true")}:
        raise ValueError("Missing or inconsistent change-selection outputs")
    expected = "skipped" if product == "false" else "success"
    if needs["app-v4"].get("result") != expected:
        raise ValueError(f"Selected verification did not complete as required: app-v4 expected {expected}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    selection = commands.add_parser("select")
    selection.add_argument("--event", required=True)
    selection.add_argument("--base", default="")
    selection.add_argument("--head", required=True)
    selection.add_argument("--repo", type=Path, default=Path("."))
    selection.add_argument("--github-output", type=Path)
    selection.add_argument("--summary", type=Path)
    commands.add_parser("gate")
    args = parser.parse_args()
    try:
        if args.command == "gate":
            require_success(json.loads(os.environ["RESULTS"]))
            print("All selected verification succeeded")
        else:
            result = select(args.repo, args.event, args.base, args.head)
            rendered = json.dumps(result, indent=2, ensure_ascii=True) + "\n"
            print(rendered, end="")
            if args.summary:
                with args.summary.open("a") as stream:
                    stream.write("## CI change selection\n\n```json\n" + rendered + "```\n")
            # Publish outputs only after successful Git selection/reporting.
            if args.github_output:
                with args.github_output.open("a") as stream:
                    stream.write(f"selection_mode={result['mode']}\n")
                    stream.write(f"run_product={str(result['run_product']).lower()}\n")
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"CI selection/gate failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
