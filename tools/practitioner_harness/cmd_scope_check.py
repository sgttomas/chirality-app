#!/usr/bin/env python3
"""`scope-check` — compare the changed paths of a git diff range to the
brief's fence (D-GOV-04). Findings report only; nothing here writes.

BLOCK discipline (D-GOV-02 / D-GOV-04): the only BLOCK-capable findings here
are objective tracked-path fence violations (`PROHIBITED_PATH_TOUCHED`,
`SCOPE_VIOLATION`) judged against an ACTIVE fence — a verified
HUMAN_ADOPTED+committed brief. Against anything else the finding is created
at BLOCK and immediately capped at REVIEW via
`cap_severity_for_unadopted_brief` with the fence's `cap_reason`. Observed
untracked files are judged the same way but sit OUTSIDE the objective
tracked-path observation boundary, so they cap at REVIEW always (stated in
the finding caveat). Path judgment is never lifecycle judgment (K-GATE-1),
and every output ends with the fixed blind-spot statement. An unresolvable
`--diff` range is an operational error (exit 2), never guessed (K-INVENT-1).
Identity refusals (D-GOV-04) examine no diff and judge no path (exit 2).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import brief_adoption
import scope_fence
from cmd_run_validations import _unquote
from harness_common import (
    HarnessOperationalError,
    Report,
    Severity,
    cap_severity_for_unadopted_brief,
    make_finding,
)

SCOPE_NOTE = (
    "scope-check compares the tracked paths changed in a git diff range, "
    "plus the currently observed untracked non-ignored files, to the brief's "
    "declared fence (write_scope / prohibited_paths; deny wins over allow). "
    "It reports findings only — it judges paths, never work.")

PATH_NOT_LIFECYCLE_NOTE = (
    "Path judgment is never lifecycle judgment: this check compares paths to "
    "the adopted fence and judges nothing about the work itself — no BLOCK "
    "ever attaches to a lifecycle judgment (K-GATE-1).")

BLIND_SPOT_STATEMENT = (
    "Blind spots — this output cannot see: untracked files beyond those "
    "listed here; writes outside this repository; changes made and reverted "
    "inside the diff range (revert games); gitignored paths.")

REFUSAL_NOTE = (
    "Identity refusal (D-GOV-04): no diff was examined and no path was "
    "judged.")

MSG_PROHIBITED = (
    "Tracked path `{path}` changed in `{range}` matches prohibited_paths "
    "entry `{pattern}` of brief {tid} — an objective tracked-path violation "
    "within the declared observation boundary (D-GOV-04 fence; D-GOV-02).")

MSG_OUT_OF_SCOPE = (
    "Tracked path `{path}` changed in `{range}` matches no write_scope "
    "entry of brief {tid} — an objective tracked-path violation within the "
    "declared observation boundary (D-GOV-04 fence; D-GOV-02).")

MSG_UNTRACKED_PROHIBITED = (
    "Untracked file `{path}` (observed now; not part of the diff range) "
    "matches prohibited_paths entry `{pattern}` of brief {tid}.")

MSG_UNTRACKED_OUT_OF_SCOPE = (
    "Untracked file `{path}` (observed now; not part of the diff range) "
    "matches no write_scope entry of brief {tid}.")

CAVEAT_UNTRACKED_OBSERVED = (
    "Observed-untracked path — outside the objective tracked-path "
    "observation boundary (not a committed change in the diff range), so "
    "severity caps at REVIEW, never BLOCK; human disposition required.")

TEMPLATES: list[str] = [
    SCOPE_NOTE, PATH_NOT_LIFECYCLE_NOTE, BLIND_SPOT_STATEMENT, REFUSAL_NOTE,
    MSG_PROHIBITED, MSG_OUT_OF_SCOPE, MSG_UNTRACKED_PROHIBITED,
    MSG_UNTRACKED_OUT_OF_SCOPE, CAVEAT_UNTRACKED_OBSERVED,
]


# --- git plumbing ---------------------------------------------------------------

def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True, text=True, check=False)
    except OSError as exc:
        raise HarnessOperationalError(
            f"git unavailable for scope-check: {exc}") from exc


def _validate_diff_range(repo_root: Path, diff_range: str) -> None:
    """Validate the range with git rev-parse FIRST; an unresolvable range is
    an operational error, never guessed (K-INVENT-1)."""
    if not diff_range or diff_range.startswith("-"):
        raise HarnessOperationalError(
            f"--diff range {diff_range!r} is empty or option-shaped; "
            "scope-check requires a plain git rev or A..B range "
            "(operational error, never guessed — K-INVENT-1).")
    proc = _run_git(repo_root, "rev-parse", diff_range)
    if proc.returncode != 0:
        raise HarnessOperationalError(
            f"--diff range {diff_range!r} does not resolve (git rev-parse: "
            f"{proc.stderr.strip()}); an unresolvable git range is an "
            "operational error, never guessed (K-INVENT-1).")


def _changed_paths(repo_root: Path, diff_range: str) -> list[tuple[str, str]]:
    """`git diff --name-status -z <range>` -> [(path, status)]. Rename/copy
    entries contribute BOTH sides (the old tracked path was touched too)."""
    proc = _run_git(repo_root, "diff", "--name-status", "-z", diff_range)
    if proc.returncode != 0:
        raise HarnessOperationalError(
            f"git diff --name-status failed for range {diff_range!r}: "
            f"{proc.stderr.strip()} (operational error).")
    tokens = proc.stdout.split("\0")
    entries: list[tuple[str, str]] = []
    i = 0
    while i < len(tokens):
        status = tokens[i]
        if not status:
            i += 1
            continue
        if status[0] in "RC":
            if i + 2 >= len(tokens):
                break  # truncated trailer; nothing left to parse
            entries.append((tokens[i + 1], status))
            entries.append((tokens[i + 2], status))
            i += 3
        else:
            if i + 1 >= len(tokens):
                break
            entries.append((tokens[i + 1], status))
            i += 2
    return entries


def _untracked_paths(repo_root: Path) -> list[str]:
    """Currently untracked, non-ignored files (git status porcelain `??`,
    with --untracked-files=all so directories are expanded to files)."""
    proc = _run_git(repo_root, "status", "--porcelain", "--untracked-files=all")
    if proc.returncode != 0:
        raise HarnessOperationalError(
            "git status --porcelain failed during scope-check: "
            f"{proc.stderr.strip()} (operational error).")
    out: list[str] = []
    for line in proc.stdout.splitlines():
        if line.startswith("?? "):
            out.append(_unquote(line[3:]))
    return out


# --- the command -----------------------------------------------------------------

def run_scope_check(repo_root: Path, brief_path: Path, diff_range: str) -> Report:
    """See the module docstring for the contract."""
    repo_root = repo_root.resolve()
    fence, adoption_findings, refusal = brief_adoption.verify_adoption(
        brief_path, repo_root)
    report = Report(command="scope-check")
    report.md(f"# scope-check — {fence.tranche_id}")
    report.md("")
    report.md(SCOPE_NOTE)
    report.md("")
    report.md(PATH_NOT_LIFECYCLE_NOTE)
    report.md("")
    report.md(f"- brief: `{fence.source_path}`")
    report.md(f"- brief state: {fence.state}")
    report.md(f"- fence_active: {fence.fence_active}")
    if fence.cap_reason:
        report.md(f"  - cap_reason: {fence.cap_reason}")
    if fence.bound_sha:
        report.md(f"- bound SHA (K-AUTH-2): `{fence.bound_sha}`")
    report.md(f"- diff range: `{diff_range}`")
    report.summary["tranche_id"] = fence.tranche_id
    report.summary["brief_state"] = fence.state
    report.summary["fence_active"] = fence.fence_active
    report.summary["diff_range"] = diff_range

    if refusal is not None:
        # D-GOV-04: no diff examined, no path judged; harness.py maps the
        # summary key to stderr + exit 2. Blind spots stated even here.
        report.md("")
        report.md(REFUSAL_NOTE)
        report.md("")
        report.md(BLIND_SPOT_STATEMENT)
        report.summary["identity_refusal"] = refusal
        report.summary["blind_spots"] = BLIND_SPOT_STATEMENT
        return report

    for finding in adoption_findings:
        report.add_finding(finding)
    for fact in fence.facts:
        report.add_fact(fact)

    _validate_diff_range(repo_root, diff_range)
    changed = _changed_paths(repo_root, diff_range)
    untracked = _untracked_paths(repo_root)

    changed_rows: list[dict] = []
    counts = {scope_fence.JUDGMENT_IN_WRITE_SCOPE: 0,
              scope_fence.JUDGMENT_PROHIBITED: 0,
              scope_fence.JUDGMENT_OUTSIDE_WRITE_SCOPE: 0}
    for path, status in changed:
        judged = scope_fence.judge_path(
            path, fence.write_scope, fence.prohibited_paths)
        counts[judged.judgment] += 1
        changed_rows.append({
            "path": path, "git_status": status,
            "judgment": judged.judgment,
            "matched_pattern": judged.matched_pattern})
        if judged.judgment == scope_fence.JUDGMENT_PROHIBITED:
            finding = make_finding(
                Severity.BLOCK, "PROHIBITED_PATH_TOUCHED", "scope",
                MSG_PROHIBITED.format(path=path, range=diff_range,
                                      pattern=judged.matched_pattern,
                                      tid=fence.tranche_id),
                path, invariant="K-WRITE-2")
        elif judged.judgment == scope_fence.JUDGMENT_OUTSIDE_WRITE_SCOPE:
            finding = make_finding(
                Severity.BLOCK, "SCOPE_VIOLATION", "scope",
                MSG_OUT_OF_SCOPE.format(path=path, range=diff_range,
                                        tid=fence.tranche_id),
                path, invariant="K-WRITE-2")
        else:
            continue
        if not fence.fence_active:
            # BLOCK only against a verified fence (D-GOV-04); anything else
            # caps at REVIEW with the fence's cap_reason recorded.
            finding = cap_severity_for_unadopted_brief(finding, fence.cap_reason)
        report.add_finding(finding)

    untracked_rows: list[dict] = []
    for path in untracked:
        judged = scope_fence.judge_path(
            path, fence.write_scope, fence.prohibited_paths)
        untracked_rows.append({
            "path": path, "judgment": judged.judgment,
            "matched_pattern": judged.matched_pattern})
        if judged.judgment == scope_fence.JUDGMENT_PROHIBITED:
            report.add_finding(make_finding(
                Severity.REVIEW, "PROHIBITED_PATH_TOUCHED", "scope",
                MSG_UNTRACKED_PROHIBITED.format(
                    path=path, pattern=judged.matched_pattern,
                    tid=fence.tranche_id),
                path, invariant="K-WRITE-2", caveat=CAVEAT_UNTRACKED_OBSERVED))
        elif judged.judgment == scope_fence.JUDGMENT_OUTSIDE_WRITE_SCOPE:
            report.add_finding(make_finding(
                Severity.REVIEW, "SCOPE_VIOLATION", "scope",
                MSG_UNTRACKED_OUT_OF_SCOPE.format(
                    path=path, tid=fence.tranche_id),
                path, invariant="K-WRITE-2", caveat=CAVEAT_UNTRACKED_OBSERVED))

    report.md("")
    report.md(f"## Changed paths in range ({len(changed_rows)})")
    report.md("")
    if changed_rows:
        report.md("| path | git status | fence judgment | matched fence entry |")
        report.md("|---|---|---|---|")
        for row in changed_rows:
            pattern = f"`{row['matched_pattern']}`" if row["matched_pattern"] else "-"
            report.md(f"| `{row['path']}` | {row['git_status']} "
                      f"| {row['judgment']} | {pattern} |")
    else:
        report.md("- none — the diff range contains no changed paths")
    report.md("")
    report.md(f"## Observed untracked non-ignored files ({len(untracked_rows)})")
    report.md("")
    if untracked_rows:
        report.md("| path | fence judgment | matched fence entry |")
        report.md("|---|---|---|")
        for row in untracked_rows:
            pattern = f"`{row['matched_pattern']}`" if row["matched_pattern"] else "-"
            report.md(f"| `{row['path']}` | {row['judgment']} | {pattern} |")
    else:
        report.md("- none observed")
    report.md("")
    report.md(BLIND_SPOT_STATEMENT)

    report.extras["scope_check"] = {
        "diff_range": diff_range,
        "changed": changed_rows,
        "untracked": untracked_rows,
    }
    report.summary["changed_paths"] = len(changed_rows)
    for name, count in counts.items():
        report.summary[f"changed_{name}"] = count
    report.summary["untracked_observed"] = len(untracked_rows)
    report.summary["blind_spots"] = BLIND_SPOT_STATEMENT
    report.summary["path_judgment_note"] = PATH_NOT_LIFECYCLE_NOTE
    return report
