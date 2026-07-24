#!/usr/bin/env python3
"""`evidence-check` — evidence completeness for the brief's declared
validations per the provenance ladder (plan v3; D-GOV-08 Option B: the
warrant ladder is an audit-time diagnostic computed over content, never a
producer-emitted state).

The declaration source is the adapter manifest (resolved from the brief's
first write_scope entry exactly like `run-validations`); harness-captured
evidence records for the tranche are read back via `evidence_records`
(two-class self-exclusion: readable as FACTS for the tranche that produced
them, never promoted to lifecycle/approval/plan/project status).

NOTHING here BLOCKs — completeness is never sufficiency, and no BLOCK ever
attaches to a lifecycle judgment (K-GATE-1). Findings are REVIEW at most:
`EVIDENCE_MISSING` (absent record — absence is reported, never accepted on
narrative), `EVIDENCE_RECORD_FLAGGED` (the captured run mutated governed
files), `EVIDENCE_UNPARSEABLE` (labeled, never guessed — K-INVENT-1),
`EVIDENCE_STALE` (evidence older than the newest commit touching the write
scope), `EVIDENCE_EXTERNAL_ARTIFACT` (ladder rung 2). Identity refusals
(D-GOV-04) verify nothing (exit 2).
"""

from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

import brief_adoption
import evidence_records
from adapter_loader import load_adapter
from cmd_run_validations import (
    _declared_commands,
    _resolve_project_root,
)
from evidence_records import CLASS_TRACKED, SELF_EXCLUSION_NOTE
from harness_common import (
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Report,
    Severity,
    SourcedFact,
    make_finding,
)

COMMAND_NOTE = (
    "evidence-check verifies evidence COMPLETENESS for the validation "
    "commands declared in the adapter manifest (the governed declaration "
    "source, resolved from the brief's first write_scope entry): are "
    "harness-captured evidence records on file for this tranche, are they "
    "newer than the newest write-scope commit, and do declared external "
    "evidence targets exist. It never judges sufficiency and never BLOCKs.")

PROVENANCE_LADDER_STATEMENT = (
    "Provenance ladder (plan v3; D-GOV-08 Option B — the warrant ladder is "
    "an audit-time diagnostic computed over content, never a producer-"
    "emitted state): (1) harness-captured evidence records satisfy "
    "completeness; (2) timestamp-consistent external artifacts at declared "
    "evidence_target paths outside the generated root satisfy at REVIEW; "
    "(3) bare prose attestations never pass silently — an absent artifact "
    "is reported as EVIDENCE_MISSING, never accepted on narrative.")

COMPLETENESS_NOTE = (
    "Completeness, never sufficiency: a present record is a recorded fact "
    "about evidence capture, not a judgment that the evidence suffices — "
    "sufficiency is a human call (K-GATE-1).")

REFUSAL_NOTE = (
    "Identity refusal (D-GOV-04): no evidence was examined and nothing was "
    "verified.")

FACT_CAVEAT = (
    "Factual evidence artifact read back under the two-class self-exclusion "
    "rule: a fact for the tranche that produced it, never lifecycle, "
    "approval, plan, or project status.")

MSG_MISSING = (
    "No harness-captured evidence record exists for declared validation "
    "command `{command}` (tranche {tid}). Absence is reported, never "
    "accepted on narrative — bare prose attestations never pass silently "
    "(provenance ladder; D-GOV-08).")

MSG_FLAGGED = (
    "Evidence record `{path}` for command `{command}` classifies changed "
    "path(s) as unexpected_tracked_change — the captured run mutated "
    "governed files (K-WRITE-2); human review required before relying on "
    "this record.")

MSG_UNPARSEABLE = (
    "Evidence record file `{path}` is UNPARSEABLE ({note}) — labeled, never "
    "guessed (K-INVENT-1).")

MSG_BAD_TIMESTAMP = (
    "Evidence record `{path}` carries captured_at {value!r}, which is not a "
    "timezone-aware ISO-8601 timestamp — staleness cannot be computed for "
    "it; labeled, never guessed (K-INVENT-1).")

MSG_STALE = (
    "Newest evidence for command `{command}` was captured at {captured_at}, "
    "OLDER than the newest commit touching the brief's write scope "
    "({commit_iso}, commit {sha}). Evidence older than changed files is "
    "flagged for human review — never silently relied on.")

MSG_EXTERNAL_STALE = (
    "External artifact at `{target}` was last modified {mtime}, OLDER than "
    "the newest commit touching the brief's write scope ({commit_iso}, "
    "commit {sha}) — not timestamp-consistent; flagged for human review.")

MSG_STALENESS_NA = (
    "No commits touch any write_scope path of this brief, so evidence "
    "staleness is NOT_APPLICABLE — there is no newer scope change to "
    "compare captured_at against.")

MSG_SCOPE_WHOLE_REPO = (
    "The brief's write_scope reduces to no literal directory prefix (an "
    "all-wildcard entry such as `**` covers the whole repository), so "
    "evidence staleness is computed against the newest commit in the WHOLE "
    "repository (git pathspec `.`) — labeled here, never silently skipped "
    "(K-INVENT-1).")

MSG_NOT_APPLICABLE = (
    "No validation commands are declared for this brief's project (adapter "
    "manifest `{declared_in}`, the governed declaration source; the brief's "
    "validations section is a projection of it) — evidence completeness has "
    "nothing to verify (NOT_APPLICABLE).")

MSG_EXTERNAL_PRESENT = (
    "Declared evidence target `{target}` lies outside the generated root "
    "and an artifact exists there (filesystem mtime {mtime}). Per the "
    "provenance ladder an external artifact satisfies at REVIEW — its "
    "consistency is a human call, never the harness's.")

MSG_EXTERNAL_ABSENT = (
    "Declared evidence target `{target}` lies outside the generated root "
    "and no artifact exists there — reported as missing, never accepted on "
    "narrative (provenance ladder; D-GOV-08).")

COVERAGE_TEMPLATE = (
    "{with_records} of {total} declared validation commands have "
    "harness-captured evidence records")

TEMPLATES: list[str] = [
    COMMAND_NOTE, PROVENANCE_LADDER_STATEMENT, COMPLETENESS_NOTE,
    REFUSAL_NOTE, FACT_CAVEAT, MSG_MISSING, MSG_FLAGGED, MSG_UNPARSEABLE,
    MSG_BAD_TIMESTAMP, MSG_STALE, MSG_EXTERNAL_STALE, MSG_STALENESS_NA,
    MSG_SCOPE_WHOLE_REPO, MSG_NOT_APPLICABLE, MSG_EXTERNAL_PRESENT,
    MSG_EXTERNAL_ABSENT, COVERAGE_TEMPLATE,
]


# --- git + timestamp plumbing -----------------------------------------------------

def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True, text=True, check=False)
    except OSError as exc:
        raise HarnessOperationalError(
            f"git unavailable for evidence-check: {exc}") from exc


def _scope_pathspecs(write_scope: list[str]) -> tuple[list[str], bool]:
    """Git pathspecs for dating the write scope: each entry's LITERAL
    directory prefix up to (excluding) its first wildcard-bearing component
    ("a/b/**" -> "a/b", "docs/*.md" -> "docs"). Fence glob entries are NEVER
    passed verbatim as git pathspecs — git pathspec `*` semantics differ
    from the fence matcher's (scope_fence.py) and would date the wrong set
    of paths. Any all-wildcard entry (e.g. a bare `**`) covers the whole
    repository, so the pathspec becomes `.` and the second return value is
    True — callers LABEL that rather than silently skipping staleness
    (K-INVENT-1). An empty write_scope returns ([], False): nothing to
    date."""
    prefixes: list[str] = []
    whole_repo = False
    for entry in write_scope:
        cleaned = entry.strip().strip("/")
        if not cleaned:
            continue
        parts: list[str] = []
        for component in cleaned.split("/"):
            if any(ch in component for ch in "*?["):
                break
            parts.append(component)
        prefix = "/".join(parts)
        if not prefix:
            whole_repo = True
        elif prefix not in prefixes:
            prefixes.append(prefix)
    if whole_repo:
        return ["."], True
    return prefixes, False


def _newest_scope_commit(
    repo_root: Path, pathspecs: list[str],
) -> tuple[str, datetime] | None:
    """(sha, committer datetime UTC) of the newest commit touching any of
    the given pathspecs (from `_scope_pathspecs`), or None when there are no
    pathspecs or no commit touches them."""
    if not pathspecs:
        return None
    proc = _run_git(repo_root, "log", "-1", "--format=%H %ct", "--", *pathspecs)
    if proc.returncode != 0:
        raise HarnessOperationalError(
            "git log failed while dating the brief's write scope: "
            f"{proc.stderr.strip()} (operational error, never guessed — "
            "K-INVENT-1).")
    line = proc.stdout.strip()
    if not line:
        return None
    sha, _, ts = line.partition(" ")
    try:
        commit_dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
    except (TypeError, ValueError) as exc:
        raise HarnessOperationalError(
            f"git log returned an unreadable commit timestamp {ts!r}; "
            "operational error, never guessed (K-INVENT-1).") from exc
    return sha, commit_dt


def _parse_captured_at(value: str) -> datetime | None:
    """Timezone-aware datetime, or None when the value is not comparable
    (the caller labels it; nothing is guessed — K-INVENT-1)."""
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return dt if dt.tzinfo is not None else None


def _manifest_line(manifest_path: Path, command: str) -> int | None:
    """First manifest line carrying the command text (finding anchor)."""
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except OSError:
        return None
    for idx, line in enumerate(text.splitlines(), start=1):
        if command in line:
            return idx
    return None


# --- the command -----------------------------------------------------------------

def run_evidence_check(
    repo_root: Path,
    brief_path: Path,
    out_dir: Path,
    alias_by_root: dict[Path, str],
) -> Report:
    """See the module docstring for the contract. `alias_by_root` is built by
    the caller from harness.py PROJECT_ALIASES (the run-validations idiom; no
    circular import)."""
    repo_root = repo_root.resolve()
    fence, adoption_findings, refusal = brief_adoption.verify_adoption(
        brief_path, repo_root)
    report = Report(command="evidence-check")
    report.md(f"# evidence-check — {fence.tranche_id}")
    report.md("")
    report.md(COMMAND_NOTE)
    report.md("")
    report.md(PROVENANCE_LADDER_STATEMENT)
    report.md("")
    report.md(SELF_EXCLUSION_NOTE)
    report.md("")
    report.md(f"- brief: `{fence.source_path}`")
    report.md(f"- brief state: {fence.state}")
    report.md(f"- fence_active: {fence.fence_active}")
    if fence.cap_reason:
        report.md(f"  - cap_reason: {fence.cap_reason}")
    if fence.bound_sha:
        report.md(f"- bound SHA (K-AUTH-2): `{fence.bound_sha}`")
    report.summary["tranche_id"] = fence.tranche_id
    report.summary["brief_state"] = fence.state
    report.summary["fence_active"] = fence.fence_active

    if refusal is not None:
        report.md("")
        report.md(REFUSAL_NOTE)
        report.summary["identity_refusal"] = refusal
        return report
    for finding in adoption_findings:
        report.add_finding(finding)
    for fact in fence.facts:
        report.add_fact(fact)

    project_root = _resolve_project_root(repo_root, fence, alias_by_root)
    manifest = load_adapter(project_root)
    declared_in = str(manifest.manifest_path.relative_to(repo_root))
    commands = _declared_commands(manifest)
    report.summary["project"] = manifest.project
    report.summary["declared_in"] = declared_in
    report.md(f"- project: {manifest.project} "
              f"(root `{project_root.relative_to(repo_root)}`, resolved from "
              "the brief's first write_scope entry)")
    report.md(f"- declared_in: `{declared_in}`")
    report.md("")

    loaded = evidence_records.load_evidence_records(
        repo_root, out_dir, fence.tranche_id)
    parsed = [rec for rec in loaded if rec.parse_status == "PARSED"]
    for rec in loaded:
        if rec.parse_status == "UNPARSEABLE":
            report.add_finding(make_finding(
                Severity.REVIEW, "EVIDENCE_UNPARSEABLE", "evidence",
                MSG_UNPARSEABLE.format(path=rec.path, note=rec.note),
                rec.path, invariant="K-INVENT-1"))

    scope_pathspecs, scope_is_whole_repo = _scope_pathspecs(fence.write_scope)
    newest_scope = _newest_scope_commit(repo_root, scope_pathspecs)
    # Whole-repo staleness scope is stated in the rendered output, never
    # silent: the reader must see WHAT the captured_at timestamps were dated
    # against (K-INVENT-1).
    staleness_caveat = MSG_SCOPE_WHOLE_REPO if scope_is_whole_repo else ""
    if newest_scope is None:
        report.add_finding(make_finding(
            Severity.NOT_APPLICABLE, "EVIDENCE_STALENESS_NOT_APPLICABLE",
            "evidence", MSG_STALENESS_NA, fence.source_path,
            invariant="K-STALE-2"))
    else:
        report.add_fact(SourcedFact(
            fact_id="evidence_check.newest_scope_commit",
            value=f"{newest_scope[0]} @ {newest_scope[1].isoformat()}",
            source_path=fence.source_path,
            source_hint=("git log -1 --format='%H %ct' -- "
                         + " ".join(scope_pathspecs)),
            authority_status="governed_committed", parse_status="PARSED",
            caveat=staleness_caveat))
        if scope_is_whole_repo:
            report.md(f"- staleness scope: {MSG_SCOPE_WHOLE_REPO}")
            report.md("")

    if not commands:
        report.add_finding(make_finding(
            Severity.NOT_APPLICABLE, "EVIDENCE_CHECK_NOT_APPLICABLE",
            "evidence", MSG_NOT_APPLICABLE.format(declared_in=declared_in),
            declared_in, invariant="K-PROV-1"))

    per_command: list[dict] = []
    with_records = 0
    for idx, (command, _cwd) in enumerate(commands, start=1):
        anchor_line = _manifest_line(manifest.manifest_path, command)
        matching = [rec for rec in parsed
                    if rec.record.get("command") == command]
        if not matching:
            report.add_finding(make_finding(
                Severity.REVIEW, "EVIDENCE_MISSING", "evidence",
                MSG_MISSING.format(command=command, tid=fence.tranche_id),
                declared_in, source_line=anchor_line, invariant="K-PROV-1"))
            per_command.append(
                {"command": command, "records": [], "status": "record_missing"})
            continue
        with_records += 1
        records_meta: list[dict] = []
        newest_dt: datetime | None = None
        newest_rec = matching[0]
        for rec in matching:
            data = rec.record
            exit_label = ("TIMED_OUT" if data.get("timed_out")
                          else str(data.get("exit_code")))
            captured = str(data.get("captured_at", ""))
            report.add_fact(SourcedFact(
                fact_id=f"evidence_check.{idx:02d}.record",
                value=f"exit {exit_label}; captured_at {captured}",
                source_path=rec.path,
                source_hint=command,
                authority_status="harness_captured",
                parse_status="PARSED",
                caveat=FACT_CAVEAT))
            flagged = any(cp.get("classification") == CLASS_TRACKED
                          for cp in data.get("changed_paths", []))
            if flagged:
                report.add_finding(make_finding(
                    Severity.REVIEW, "EVIDENCE_RECORD_FLAGGED", "evidence",
                    MSG_FLAGGED.format(path=rec.path, command=command),
                    rec.path, invariant="K-WRITE-2"))
            captured_dt = _parse_captured_at(captured)
            if captured_dt is None:
                report.add_finding(make_finding(
                    Severity.REVIEW, "EVIDENCE_UNPARSEABLE", "evidence",
                    MSG_BAD_TIMESTAMP.format(path=rec.path, value=captured),
                    rec.path, invariant="K-INVENT-1"))
            elif newest_dt is None or captured_dt > newest_dt:
                newest_dt, newest_rec = captured_dt, rec
            records_meta.append({"path": rec.path, "exit": exit_label,
                                 "captured_at": captured, "flagged": flagged})
        if newest_scope is not None and newest_dt is not None:
            sha, commit_dt = newest_scope
            if newest_dt < commit_dt:
                report.add_finding(make_finding(
                    Severity.REVIEW, "EVIDENCE_STALE", "evidence",
                    MSG_STALE.format(command=command,
                                     captured_at=newest_dt.isoformat(),
                                     commit_iso=commit_dt.isoformat(),
                                     sha=sha[:12]),
                    newest_rec.path, invariant="K-STALE-2",
                    caveat=staleness_caveat))
        per_command.append({"command": command, "records": records_meta,
                            "status": "records_present"})

    # Ladder rung 2: declared evidence targets OUTSIDE the generated root.
    external_rows: list[dict] = []
    for target in fence.evidence_targets:
        cleaned = target.strip().rstrip("*").rstrip("/")
        if not cleaned:
            continue
        if (cleaned == GENERATED_ROOT_NAME
                or cleaned.startswith(GENERATED_ROOT_NAME + "/")):
            continue  # rung 1 territory: harness-captured records
        artifact = repo_root / cleaned
        if artifact.exists():
            mtime = datetime.fromtimestamp(
                artifact.stat().st_mtime, tz=timezone.utc)
            external_rows.append({"target": cleaned, "present": True,
                                  "mtime": mtime.isoformat()})
            report.add_finding(make_finding(
                Severity.REVIEW, "EVIDENCE_EXTERNAL_ARTIFACT", "evidence",
                MSG_EXTERNAL_PRESENT.format(target=cleaned,
                                            mtime=mtime.isoformat()),
                cleaned, invariant="K-PROV-1"))
            if newest_scope is not None and mtime < newest_scope[1]:
                sha, commit_dt = newest_scope
                report.add_finding(make_finding(
                    Severity.REVIEW, "EVIDENCE_STALE", "evidence",
                    MSG_EXTERNAL_STALE.format(target=cleaned,
                                              mtime=mtime.isoformat(),
                                              commit_iso=commit_dt.isoformat(),
                                              sha=sha[:12]),
                    cleaned, invariant="K-STALE-2",
                    caveat=staleness_caveat))
        else:
            external_rows.append({"target": cleaned, "present": False})
            report.add_finding(make_finding(
                Severity.REVIEW, "EVIDENCE_MISSING", "evidence",
                MSG_EXTERNAL_ABSENT.format(target=cleaned),
                cleaned, invariant="K-PROV-1"))

    report.md(f"## Declared validations vs captured evidence ({len(commands)})")
    report.md("")
    if commands:
        report.md("| # | command | records | exits | newest captured_at |")
        report.md("|---|---|---|---|---|")
        for idx, entry in enumerate(per_command, start=1):
            recs = entry["records"]
            exits = ", ".join(r["exit"] for r in recs) if recs else "-"
            newest = max((r["captured_at"] for r in recs), default="-")
            report.md(f"| {idx} | `{entry['command']}` | {len(recs)} "
                      f"| {exits} | {newest} |")
    else:
        report.md("- none declared")
    report.md("")
    coverage = COVERAGE_TEMPLATE.format(
        with_records=with_records, total=len(commands))
    report.md(f"- coverage: {coverage}")
    report.md("")
    report.md(COMPLETENESS_NOTE)

    report.extras["evidence_check"] = {
        "declared_in": declared_in,
        "coverage": {"total": len(commands), "with_records": with_records},
        "per_command": per_command,
        "unparseable": [rec.path for rec in loaded
                        if rec.parse_status == "UNPARSEABLE"],
        "external_targets": external_rows,
    }
    report.summary["coverage"] = coverage
    report.summary["completeness_note"] = COMPLETENESS_NOTE
    return report
