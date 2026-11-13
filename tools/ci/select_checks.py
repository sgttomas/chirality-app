#!/usr/bin/env python3
"""Select PR verification from committed changes; validate the aggregate gate."""
# Narrowing what a change runs (a new documentary path, a skipped job, a looser
# rule) needs independent review, using the model set by current session
# steering, before merge. Unknown paths keep full coverage; the selector's tests
# and completeness check enforce the rest.
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
import unicodedata


# Exact documentary paths plus the guarded declarative execution tree.
# Operational inputs live under app/ or tools/; unknown domains retain product checks.
PROSE_PATHS = frozenset({
    "AGENTS.md",
    "README.md",
    "init-prompt.md",
    "docs/CI_SELECTION.md",
    "docs/OPERATING_METHOD.md",
    "docs/user-manual/README.md",
    "tools/deliverables/README.md",
})
# Inputs no macOS product job consumes; their readers run in repository checks.
# docs/CI_SELECTION.md maps each class to its readers and the search behind it.
# Class A, governing text: Markdown under docs/ (execution/ is documentary above).
GOVERNING_TEXT = "docs/"
# Class B, examination tooling: the standalone examination and its Group B tests.
EXAMINATION_ROOTS = ("app/examination/standalone/", "app/tests/group_b_")
EXAMINATION_SUFFIXES = (".py", ".mjs", ".cjs", ".js", ".json", ".md")
# Inside those roots, read by a macOS product job: the Rust lib compiles the
# consumer and its tests read standalone/fixtures; sources-packaging reads the
# two fixture trees. These stay product inputs.
MACOS_INPUTS_IN_CLASS_ROOTS = (
    "app/examination/standalone/fixtures/", "app/tests/group_b_fixture_consumer.rs",
    "app/tests/group_b_fixtures/", "app/tests/group_b_sq_receiving_fixtures/",
)
# The macOS examination job runs app/tests/group_b_*_macos_test.py (tests that
# need macOS itself) without the frontend, Rust or supplier. Any change under
# these roots, to the job's definition, or to an unmatched path selects it.
EXAMINATION_MACOS_ROOTS = ("app/examination/", "app/tests/group_b_")
EXAMINATION_MACOS_DEFINITION = frozenset({
    "tools/ci/examination_tests.py", "tools/ci/select_checks.py",
    ".github/workflows/governance-harness.yml",
})
# These domains contain code, contracts, fixtures or retained source inputs.
# Documentary exceptions above take precedence; unfamiliar domains stay unmatched.
PRODUCT_DOMAINS = (
    ".github/actions/", ".github/workflows/", "app/", "docs/", "reference/",
    "tools/", "workflows/",
)
PRODUCT_FILES = frozenset({".gitattributes", ".gitignore", "CLAUDE.md", "LICENSE.md"})
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


def plain(path: str) -> bool:
    # Only printable ASCII can be narrowed: a checkout may fold other spellings
    # onto a protected file (case, Unicode normalization and compatibility forms).
    return all(0x20 <= ord(character) < 0x7f for character in path)


def path_rule(path: str) -> str:
    if plain(path):
        if path in PROSE_PATHS or path.startswith("execution/"):
            return "documentary"
        if path.startswith(GOVERNING_TEXT) and path.endswith(".md"):
            return "governing-text"
        # Protected prefixes compare without regard to case, as macOS checkouts do.
        if (path.startswith(EXAMINATION_ROOTS) and path.endswith(EXAMINATION_SUFFIXES)
                and not path.lower().startswith(tuple(item.lower() for item in MACOS_INPUTS_IN_CLASS_ROOTS))):
            return "examination"
    if path in PRODUCT_FILES:
        return "product-file"
    if path.startswith(PRODUCT_DOMAINS):
        return "product-domain"
    return "unmatched"


def fold(text: str) -> str:
    """A conservative key for names a checkout may treat as one: Unicode
    compatibility normalization, case folding, and dropped format characters.
    It folds at least what a case- and normalization-insensitive macOS volume
    folds; it does not claim to model any file system exactly."""
    text = unicodedata.normalize("NFKC", unicodedata.normalize("NFKC", text).casefold())
    return "".join(character for character in text if unicodedata.category(character) != "Cf")


def tree(repo: Path, revision: str = "HEAD") -> list[tuple[str, str, str]]:
    """Tracked entries (mode, object, path) read from the commit's tree, not a checkout."""
    entries = []
    for record in git(repo, "ls-tree", "-r", "-z", "--full-tree", revision).split(b"\0"):
        if record:
            header, path = record.split(b"\t", 1)
            mode, _, oid = header.decode().split(" ")
            entries.append((mode, oid, os.fsdecode(path)))
    return entries


def collisions(paths: list[str]) -> list[list[str]]:
    """Distinct tracked paths or directories that fold to the same name."""
    groups: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        parts = path.split("/")
        for end in range(1, len(parts) + 1):
            prefix = "/".join(parts[:end])
            groups[fold(prefix)].add(prefix)
    return sorted(sorted(group) for group in groups.values() if len(group) > 1)


NARROWED_ROOTS = ("execution/", GOVERNING_TEXT, *EXAMINATION_ROOTS)


def links_into_narrowed(repo: Path, entries: list[tuple[str, str, str]]) -> list[str]:
    """Tracked symbolic links whose target lies in a narrowed class: a reader of
    the link would read a path whose changes skip the product jobs."""
    found = []
    for mode, oid, path in entries:
        if mode != "120000":
            continue
        target = os.fsdecode(git(repo, "cat-file", "blob", oid))
        resolved = fold(posixpath.normpath(posixpath.join(posixpath.dirname(path), target)))
        if (resolved.startswith(tuple(fold(root) for root in NARROWED_ROOTS))
                or resolved in {fold(item) for item in PROSE_PATHS}):
            found.append(path)
    return sorted(found)


def inventory(repo: Path) -> dict:
    paths = [os.fsdecode(path) for path in git(repo, "ls-files", "-z").split(b"\0") if path]
    unmatched = sorted(path for path in paths if path_rule(path) == "unmatched")
    entries = tree(repo)
    return {"tracked_paths": len(paths), "unmatched": unmatched,
            "collisions": collisions([path for _, _, path in entries]),
            "links_into_narrowed": links_into_narrowed(repo, entries)}


REPOSITORY_RULES = {
    "documentary": "Audited documentary file",
    "governing-text": "Governing text read only by repository checks",
    "examination": "Examination tooling run only by repository checks",
}


def classify(change: dict[str, str]) -> dict[str, str]:
    rule = path_rule(change["path"])
    reason = "Unmatched path requires full product verification" if rule == "unmatched" else \
             "Explicit product input requires product verification"
    if not plain(change["path"]):
        reason = "Only printable ASCII paths can skip product verification"
    if change["status"] not in {"A", "M"}:
        reason = "Deletion or file-type change requires product verification"
    elif change["new_mode"] != "100644" or change["old_mode"] not in {"000000", "100644"}:
        reason = "Only ordinary non-executable documentary files qualify"
    elif rule in REPOSITORY_RULES:
        return {**change, "rule": rule, "checks": "repository", "reason": REPOSITORY_RULES[rule]}
    return {**change, "rule": rule, "checks": "product", "reason": reason}


def examination_macos(changes: list[dict[str, str]]) -> bool:
    return not changes or any(
        change["path"].startswith(EXAMINATION_MACOS_ROOTS) or change["rule"] == "unmatched"
        or change["path"] in EXAMINATION_MACOS_DEFINITION for change in changes)


def select(repo: Path, event: str, base: str, head: str) -> dict:
    head = commit(repo, head)
    if event == "workflow_dispatch":
        return {"head": head, "mode": "product", "run_product": True, "run_examination_macos": True,
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
            "run_examination_macos": examination_macos(changes),
            "reason": "Empty change set retains product verification" if not changes else
                      "Union of checks required by all changed paths", "changes": changes}


def require_success(needs: dict) -> None:
    if not isinstance(needs, dict) or set(needs) != {
            "change-selection", "repository-checks", "app-v4", "examination-macos"}:
        raise ValueError("Aggregate requires exactly the declared verification jobs")
    selected = needs["change-selection"]
    if selected.get("result") != "success":
        raise ValueError("Change selection must succeed")
    if needs["repository-checks"].get("result") != "success":
        raise ValueError("Repository checks must succeed")
    outputs = selected.get("outputs", {})
    mode, product = outputs.get("selection_mode"), outputs.get("run_product")
    if (mode, product) not in {("prose", "false"), ("product", "true")}:
        raise ValueError("Missing or inconsistent change-selection outputs")
    examination = outputs.get("run_examination_macos")
    if examination not in {"true", "false"}:
        raise ValueError("Missing or inconsistent change-selection outputs")
    for job, selected in (("app-v4", product), ("examination-macos", examination)):
        expected = "success" if selected == "true" else "skipped"
        if needs[job].get("result") != expected:
            raise ValueError(f"Selected verification did not complete as required: {job} expected {expected}")


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
    tracked = commands.add_parser("inventory")
    tracked.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        if args.command == "gate":
            require_success(json.loads(os.environ["RESULTS"]))
            print("All selected verification succeeded")
        elif args.command == "inventory":
            result = inventory(args.repo)
            print(json.dumps(result, indent=2, ensure_ascii=True))
            problems = [message for key, message in (
                ("unmatched", "Tracked paths need explicit classification; unmatched paths still select full product verification"),
                ("collisions", "Tracked paths collide when case and Unicode forms are folded; a checkout may merge them"),
                ("links_into_narrowed", "Tracked symbolic links point into a narrowed class; their readers would skip product checks"),
            ) if result[key]]
            if problems:
                raise ValueError("; ".join(problems))
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
                    stream.write(f"run_examination_macos={str(result['run_examination_macos']).lower()}\n")
                    stream.write(f"merge_base={result.get('merge_base', '')}\n")
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"CI selection/gate failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
