#!/usr/bin/env python3
"""`coord-check` - report-only checks for coordination/control artifacts.

This command is the coordination-artifact analogue to the brief-fenced Phase 4
checks: it reads the tracked paths changed by a git diff range, selects the
coordination/control subset, and reports mechanical findings only. It never
selects work, never validates an outcome, and never changes lifecycle state.
"""

from __future__ import annotations

import re
from pathlib import Path

from cmd_scope_check import _changed_paths, _run_git, _validate_diff_range
from cmd_self_check import (
    ABS_PATH_RE,
    _candidate_refs,
    _is_declared_generated_root_ref,
    _resolve_ref_path,
)
from surface_roles import (
    SurfaceRole,
    effective_role,
    has_control_exception,
    load_project_policy,
)
from harness_common import (
    HarnessOperationalError,
    Report,
    Severity,
    make_finding,
)

COORD_NOTE = (
    "coord-check inspects changed coordination/control artifacts in a git diff "
    "range. It reports citation resolution, same-directory decision-register "
    "coverage for changed decision records, named-precedent presence for "
    "packet-shaped records, and machine-absolute paths on lines the diff "
    "range ADDS; it is never approval, selection, or lifecycle judgment.")

DIFF_NOTE = (
    "Only current file content and diff-added lines for tracked changed paths "
    "are inspected; deleted files, reverted intermediate edits, untracked "
    "files, gitignored files, and files outside this repository are blind "
    "spots.")

TEMPLATES = [COORD_NOTE, DIFF_NOTE]

COORD_PREFIXES = (
    "_DomainEngines/bridge/",
    "_DomainEngines/_DECISIONS/",
    "_DomainEngines/proposals/",
    "docs/governance_harness/_DECISIONS/",
)
DECISION_ID_RE = re.compile(r"^(D(?:-[A-Z0-9]+)*-\d+[A-Za-z]?)")
PRECEDENT_RE = re.compile(
    r"\b(precedent|pattern|skeleton|modeled on|convention)\b", re.IGNORECASE)

# HB-10 diff-added machine-absolute-path check (SPEC §0.2.4). The D-05b
# packet (2026-07-04) quoted a machine-absolute path verbatim; the GEN-8
# self-check lint caught it only at full-audit/CI time, after the closeout
# checks had already been recorded. This check closes the pre-commit seam:
# it flags machine-absolute paths on lines the diff range ADDS to changed
# coordination artifacts, reusing self-check's ABS_PATH_RE machine-root
# pattern and EVIDENCE_PATH_MARKERS exemption (imported, never duplicated;
# run-record/evidence artifacts lawfully carry absolute paths per SPEC
# §0.2.4). Detect, never rewrite.
HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def _is_coordination_artifact(relpath: str) -> bool:
    if relpath.startswith(COORD_PREFIXES):
        return relpath.endswith(".md")
    return "/execution/_Coordination/" in relpath and relpath.endswith(".md")


def _decision_id_from_record(relpath: str) -> str:
    path = Path(relpath)
    if path.name == "_REGISTER.md" or path.suffix != ".md":
        return ""
    if path.parent.name != "_DECISIONS":
        return ""
    m = DECISION_ID_RE.match(path.name)
    return m.group(1) if m else ""


def _register_contains_decision(register_text: str, decision_id: str) -> bool:
    return re.search(
        rf"\|\s*`?{re.escape(decision_id)}`?\s*\|", register_text) is not None


def _requires_named_precedent(relpath: str) -> bool:
    path = Path(relpath)
    lower = path.name.lower()
    if _decision_id_from_record(relpath):
        return True
    return (
        "change_prep" in lower
        or "decision_packet" in lower
        or "design" in lower
    )


def _check_citations(
        report: Report, repo_root: Path, relpath: str, text: str) -> int:
    file_path = repo_root / relpath
    de_root = repo_root / "_DomainEngines"
    finding_count = 0
    for idx, line in enumerate(text.splitlines(), start=1):
        for ref in _candidate_refs(line):
            if _resolve_ref_path(ref, repo_root, file_path.parent, de_root) is not None:
                continue
            if _is_declared_generated_root_ref(ref):
                report.add_finding(make_finding(
                    Severity.INFO, "COORD_GENERATED_REF_ABSENT", "coordination",
                    f"Reference `{ref}` is under the declared generated root; "
                    "generated artifacts are rebuildable and may be absent in "
                    "fresh checkouts/worktrees.",
                    relpath, idx, invariant="K-PROV-1"))
            else:
                report.add_finding(make_finding(
                    Severity.REVIEW, "COORD_UNRESOLVED_REF", "coordination",
                    f"Reference `{ref}` does not resolve to an existing repo path "
                    "(checked repo-root-relative and file-relative).",
                    relpath, idx, invariant="K-PROV-1"))
            finding_count += 1
    return finding_count


def _check_register_row(report: Report, repo_root: Path, relpath: str) -> int:
    decision_id = _decision_id_from_record(relpath)
    if not decision_id:
        return 0
    register = repo_root / Path(relpath).parent / "_REGISTER.md"
    if not register.is_file():
        report.add_finding(make_finding(
            Severity.REVIEW, "COORD_REGISTER_ABSENT", "coordination",
            f"Decision record `{relpath}` has parsed id `{decision_id}`, but "
            "the same-directory `_REGISTER.md` file is absent.",
            relpath, invariant="K-PROV-1"))
        return 1
    text = register.read_text(encoding="utf-8")
    if _register_contains_decision(text, decision_id):
        return 0
    report.add_finding(make_finding(
        Severity.REVIEW, "COORD_REGISTER_ROW_MISSING", "coordination",
        f"Decision record `{relpath}` has parsed id `{decision_id}`, but that "
        "id is not present as a table cell in the same-directory `_REGISTER.md`.",
        relpath, invariant="K-PROV-1"))
    return 1


def _parse_added_lines(diff_text: str) -> list[tuple[int, str]]:
    """Unified-diff ADDED lines as (new-file line number, content).

    Removed lines and `\\ No newline` markers never advance the new-file
    counter; context lines do. Text before the first hunk header (or after
    a `diff ` file header) is never treated as hunk content, so `+++` file
    headers cannot yield phantom added lines.
    """
    added: list[tuple[int, str]] = []
    new_line = 0
    in_hunk = False
    for raw in diff_text.splitlines():
        if raw.startswith("diff "):
            in_hunk = False
            continue
        m = HUNK_HEADER_RE.match(raw)
        if m:
            new_line = int(m.group(1))
            in_hunk = True
            continue
        if not in_hunk:
            continue
        if raw.startswith("+"):
            added.append((new_line, raw[1:]))
            new_line += 1
        elif raw.startswith(("-", "\\")):
            continue
        else:
            new_line += 1
    return added


def _added_lines(
        repo_root: Path, diff_range: str, relpath: str) -> list[tuple[int, str]]:
    proc = _run_git(
        repo_root, "diff", "--unified=0", diff_range, "--", relpath)
    if proc.returncode != 0:
        raise HarnessOperationalError(
            f"git diff --unified=0 failed for range {diff_range!r} path "
            f"{relpath!r}: {proc.stderr.strip()} (operational error).")
    return _parse_added_lines(proc.stdout)


def _check_added_abs_paths(
        report: Report, repo_root: Path, relpath: str,
        added_lines: list[tuple[int, str]]) -> int:
    parts = Path(relpath).parts
    if len(parts) >= 2 and parts[0] in {"projects", "domains"}:
        project_root = repo_root / parts[0] / parts[1]
        policy = load_project_policy(repo_root, project_root)
    else:
        policy = load_project_policy(repo_root, repo_root)
    classification = effective_role(relpath, policy)
    if classification.role is SurfaceRole.UNCLASSIFIED and not classification.active:
        # Every changed coordination artifact is an active control even when
        # it is outside the managed AgentRuns structural vocabulary.
        from surface_roles import classify_surface
        classification = classify_surface(relpath, live_entry=True)
    if classification.role is SurfaceRole.EVIDENCE:
        return 0
    if has_control_exception(relpath, policy):
        return 0
    finding_count = 0
    for line_no, line in added_lines:
        if not ABS_PATH_RE.search(line):
            continue
        report.add_finding(make_finding(
            Severity.REVIEW, "COORD_ABS_PATH_ADDED", "coordination",
            "Line added by this diff range embeds a machine-absolute path "
            f"on an active {classification.role.value} coordination artifact "
            f"({classification.reason}); SPEC §0.2.4 requires repo-relative "
            "anchoring on controls; unknown active artifacts are actionable "
            "by default. "
            "Relativize before commit or add an explicit hash-bound historical "
            "disposition under governing authority.",
            relpath, line_no, invariant="SPEC-0.2.4"))
        finding_count += 1
    return finding_count


def _check_precedent(report: Report, relpath: str, text: str) -> int:
    if not _requires_named_precedent(relpath) or PRECEDENT_RE.search(text):
        return 0
    report.add_finding(make_finding(
        Severity.REVIEW, "COORD_PRECEDENT_NOT_NAMED", "coordination",
        f"Coordination packet-shaped artifact `{relpath}` does not name a "
        "precedent, pattern, skeleton, or convention for its structure.",
        relpath, invariant="K-INVENT-1"))
    return 1


def run_coord_check(repo_root: Path, diff_range: str) -> Report:
    repo_root = repo_root.resolve()
    report = Report(command="coord-check")
    report.md("# coord-check - coordination/control artifact checks")
    report.md("")
    report.md(COORD_NOTE)
    report.md("")
    report.md(f"- diff range: `{diff_range}`")
    report.summary["diff_range"] = diff_range

    _validate_diff_range(repo_root, diff_range)
    changed = _changed_paths(repo_root, diff_range)
    coord_rows: list[dict] = []
    skipped_rows: list[dict] = []

    for relpath, status in changed:
        if not _is_coordination_artifact(relpath):
            skipped_rows.append({"path": relpath, "git_status": status})
            continue
        path = repo_root / relpath
        row = {
            "path": relpath,
            "git_status": status,
            "inspectable": path.is_file(),
            "citation_findings": 0,
            "register_findings": 0,
            "precedent_findings": 0,
            "abs_path_findings": 0,
        }
        coord_rows.append(row)
        # Diff-added lines are judged from the diff itself, so deletions and
        # renames-away (no current file) are still inspected — they simply
        # contribute no added lines.
        row["abs_path_findings"] = _check_added_abs_paths(
            report, repo_root, relpath,
            _added_lines(repo_root, diff_range, relpath))
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        row["citation_findings"] = _check_citations(
            report, repo_root, relpath, text)
        row["register_findings"] = _check_register_row(
            report, repo_root, relpath)
        row["precedent_findings"] = _check_precedent(report, relpath, text)

    report.md("")
    report.md(f"## Coordination/control paths ({len(coord_rows)})")
    report.md("")
    if coord_rows:
        report.md("| path | git status | inspectable | citation | register | precedent | abs-path |")
        report.md("|---|---|---:|---:|---:|---:|---:|")
        for row in coord_rows:
            report.md(
                f"| `{row['path']}` | {row['git_status']} | "
                f"{row['inspectable']} | {row['citation_findings']} | "
                f"{row['register_findings']} | {row['precedent_findings']} | "
                f"{row['abs_path_findings']} |")
    else:
        report.md("- none in this diff range")

    report.md("")
    report.md(f"## Other changed paths ({len(skipped_rows)})")
    report.md("")
    if skipped_rows:
        report.md("| path | git status |")
        report.md("|---|---|")
        for row in skipped_rows:
            report.md(f"| `{row['path']}` | {row['git_status']} |")
    else:
        report.md("- none")

    report.md("")
    report.md(DIFF_NOTE)
    report.extras["coord_check"] = {
        "diff_range": diff_range,
        "coordination_paths": coord_rows,
        "other_changed_paths": skipped_rows,
    }
    report.summary["changed_paths"] = len(changed)
    report.summary["coordination_paths"] = len(coord_rows)
    report.summary["other_changed_paths"] = len(skipped_rows)
    report.summary["blind_spots"] = DIFF_NOTE
    return report
