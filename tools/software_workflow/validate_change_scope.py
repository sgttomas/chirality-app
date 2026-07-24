#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path, PurePosixPath


def contained(path: str, allowed: str) -> bool:
    candidate = PurePosixPath(path)
    root = PurePosixPath(allowed.rstrip("/"))
    return candidate == root or root in candidate.parents


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Git changed paths against declared write roots.")
    parser.add_argument("repo")
    parser.add_argument("--allowed", action="append", required=True)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--head")
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    paths = list(args.path)
    if not paths:
        command = ["git", "-C", str(repo), "diff", "--name-only", args.base]
        if args.head:
            command.append(args.head)
        completed = subprocess.run(command, text=True, capture_output=True, shell=False, check=True)
        paths = [line for line in completed.stdout.splitlines() if line]
        untracked = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "--others", "--exclude-standard"],
            text=True,
            capture_output=True,
            shell=False,
            check=True,
        )
        paths = sorted(set(paths + [line for line in untracked.stdout.splitlines() if line]))
    violations = [path for path in paths if not any(contained(path, allowed) for allowed in args.allowed)]
    report = {
        "schema": "chirality-change-scope/v1",
        "allowed": args.allowed,
        "paths": paths,
        "violations": violations,
        "status": "PASS" if not violations else "FAIL",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
