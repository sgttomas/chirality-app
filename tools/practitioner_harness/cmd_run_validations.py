#!/usr/bin/env python3
"""`run-validations` — execute the manifest-declared validation commands for
the project a brief fences, under the plan v3 mutation-control contract:

    1. record pre-run  `git status --porcelain` plus a content fingerprint
       (`git hash-object` over worktree bytes) of every tracked porcelain
       entry — status-code diffing alone cannot see a command mutating a
       file that was ALREADY dirty before the run (" M" stays " M")
    2. run only declared commands (adapter manifest — the governed
       configuration authority; the brief's validations text is cross-checked
       and drift is surfaced, the manifest governs)
    3. capture stdout/stderr, exit code, duration, tool versions where cheap
    4. record post-run `git status --porcelain` and re-fingerprint the union
       of pre/post tracked entries; a content change with an unchanged
       status code is a changed path like any other
    5. classify changed paths: expected_evidence_output | ignored_cache |
       unexpected_tracked_change | review_required_untracked
    6. BLOCK if a validation command modified governed files outside the
       declared evidence/output paths — the generated root ALWAYS, plus the
       brief's evidence_targets ONLY when the fence is active
       (VALIDATION_MUTATED_GOVERNED_FILES, K-WRITE-2 — UNCONDITIONAL: this
       protects the substrate, not the fence, so the D-GOV-04 adoption cap
       never applies)

Known boundary, stated rather than papered over (K-INVENT-1): appends to a
PRE-EXISTING untracked file are invisible to porcelain diffing — the entry
is `??` before and after, and untracked files are not fingerprinted.

Porcelain snapshots are taken with `--ignored` so ignored-cache writes are
observable at all; `git check-ignore` then classifies them. Every command
gets an evidence record (evidence_records.py, json + md) regardless of
outcome; a timed-out command is recorded TIMED_OUT with exit_code null —
never an inferred outcome (K-INVENT-1). Exit codes are recorded facts, never
judgments; a completed run with exit 0 is structural evidence only, never
approval (K-DOMAIN-4 analogue). An unadopted/candidate brief does not stop
the run (the commands are manifest-declared) but caps it: REVIEW
`VALIDATION_RUN_WITHOUT_ACTIVE_FENCE` with the fence's cap_reason, and every
record carries fence_active=False. Identity refusals (D-GOV-04) execute
nothing and write nothing (exit 2).
"""

from __future__ import annotations

import os
import shlex
import signal
import subprocess
import time
from collections import Counter
from pathlib import Path

import brief_adoption
import evidence_records
from adapter_loader import AdapterManifest, load_adapter
from evidence_records import (
    CLASS_EXPECTED,
    CLASS_IGNORED,
    CLASS_TRACKED,
    CLASS_UNTRACKED,
    STRUCTURAL_EVIDENCE_NOTE,
)
from harness_common import (
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Report,
    Severity,
    SourcedFact,
    make_finding,
)

SCOPE_NOTE = (
    "run-validations executes ONLY validation commands declared in the "
    "adapter manifest (harness configuration authority — governed, "
    "committed, human-reviewed; never lifecycle or project truth) for the "
    "project the brief fences, under the mutation-control contract: pre/post "
    "`git status --porcelain --ignored` snapshots, one evidence record per "
    "command, changed-path classification.")

LIST_MODE_NOTE = (
    "--list mode: the resolved command list above is the whole action — "
    "nothing was executed and nothing was written (no evidence records, no "
    "working-tree side effects).")

REFUSAL_NOTE = (
    "Identity refusal (D-GOV-04): nothing was executed and no evidence "
    "record was written.")

MSG_RUN_WITHOUT_FENCE = (
    "Validation commands executed without an active fence: the brief "
    "declares state {state} and is not a verified HUMAN_ADOPTED+committed "
    "fence (D-GOV-04). The commands are manifest-declared (the governed "
    "configuration authority), so execution proceeds; every evidence record "
    "for this run carries fence_active=False.")

MSG_MUTATED = (
    "Validation command `{command}` modified governed file(s) outside the "
    "declared evidence/output paths: {paths}. A validation command is not a "
    "write tool (K-WRITE-2 mutation-control contract); this BLOCK protects "
    "the substrate, not the fence — it is unconditional and the D-GOV-04 "
    "adoption cap does not apply.")

MSG_UNTRACKED_OUTPUT = (
    "Validation command `{command}` created new untracked, non-ignored "
    "file(s) outside the declared evidence/output paths: {paths}. Human "
    "review required to disposition them (declare as evidence output, "
    "gitignore, or remove) — not classified further by the harness "
    "(K-INVENT-1).")

MSG_TIMED_OUT = (
    "Validation command `{command}` hit the {timeout}s timeout and was "
    "killed: recorded TIMED_OUT with exit_code null — an unobserved outcome "
    "is never inferred (K-INVENT-1).")

MSG_DRIFT_MANIFEST_ONLY = (
    "Manifest-declared validation command `{command}` does not appear in the "
    "brief's declared validations text. The adapter manifest governs — it is "
    "the harness configuration authority — so the command runs regardless; "
    "reconcile the brief text when it is next touched.")

MSG_DRIFT_BRIEF_ONLY = (
    "Brief-declared validations entry {entry!r} matches no manifest-declared "
    "validation command. The adapter manifest governs — it is the harness "
    "configuration authority — and only manifest-declared commands run.")

NO_CHANGES_NOTE = (
    "No changed paths observed across the run (pre-run and post-run "
    "porcelain snapshots agree per command).")

TEMPLATES: list[str] = [
    SCOPE_NOTE, LIST_MODE_NOTE, REFUSAL_NOTE, MSG_RUN_WITHOUT_FENCE,
    MSG_MUTATED, MSG_UNTRACKED_OUTPUT, MSG_TIMED_OUT,
    MSG_DRIFT_MANIFEST_ONLY, MSG_DRIFT_BRIEF_ONLY, NO_CHANGES_NOTE,
]

# Cheap tool-version probes keyed off the command's first token; anything
# else is skipped (probes stay cheap, never guessed).
VERSION_PROBE_TOOLS = ("python3", "npm", "node")
_PROBE_TIMEOUT_SECONDS = 10


# --- git plumbing for the mutation-control contract ----------------------------

def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True, text=True, check=False)
    except OSError as exc:
        raise HarnessOperationalError(
            f"git unavailable for the mutation-control contract: {exc}") from exc


def _porcelain(repo_root: Path) -> list[str]:
    """Full-repo `git status --porcelain --ignored` snapshot (--ignored so
    ignored-cache writes are observable for classification at all)."""
    proc = _run_git(repo_root, "status", "--porcelain", "--ignored")
    if proc.returncode != 0:
        raise HarnessOperationalError(
            "git status --porcelain failed; the mutation-control contract "
            f"cannot proceed without git truth: {proc.stderr.strip()}")
    return proc.stdout.splitlines()


def _is_ignored(repo_root: Path, path: str) -> bool:
    return _run_git(repo_root, "check-ignore", "-q", "--", path).returncode == 0


def _unquote(path: str) -> str:
    """Undo git's C-style quoting of porcelain paths (spaces, non-ASCII)."""
    if len(path) >= 2 and path.startswith('"') and path.endswith('"'):
        try:
            return (path[1:-1].encode("utf-8").decode("unicode_escape")
                    .encode("latin-1").decode("utf-8"))
        except (UnicodeDecodeError, UnicodeEncodeError):
            return path[1:-1]
    return path


def _parse_porcelain(lines: list[str]) -> dict[str, str]:
    """Porcelain lines -> {path: XY status}. Rename/copy entries yield BOTH
    sides (the old tracked path was mutated too)."""
    entries: dict[str, str] = {}
    for line in lines:
        if len(line) < 4:
            continue
        xy, rest = line[:2], line[3:]
        if xy[0] in "RC" and " -> " in rest:
            old, _, new = rest.partition(" -> ")
            entries[_unquote(old)] = xy
            entries[_unquote(new)] = xy
        else:
            entries[_unquote(rest)] = xy
    return entries


# Labeled fingerprint state for a tracked path that cannot be content-hashed
# at snapshot time (deleted from the worktree, unreadable) — a label, never a
# guess (K-INVENT-1). Two labeled states compare equal, so a file that is
# absent both before and after the run is not reported as a mutation.
FINGERPRINT_UNAVAILABLE = "unreadable_or_absent"


def _tracked_fingerprints(
    repo_root: Path, entries: dict[str, str],
) -> dict[str, str]:
    """Content fingerprints (`git hash-object` over worktree bytes) for every
    porcelain entry that is a TRACKED path (any XY except `??` untracked and
    `!!` ignored). Status-code diffing alone misses a command mutating a file
    that was already dirty pre-run — the entry reads " M" before and after —
    so the mutation-control contract compares content for those (K-WRITE-2).
    A path that cannot be hashed is recorded as FINGERPRINT_UNAVAILABLE."""
    fingerprints: dict[str, str] = {}
    for path, xy in entries.items():
        if xy in ("??", "!!"):
            continue
        proc = _run_git(repo_root, "hash-object", "--", path)
        digest = proc.stdout.strip()
        fingerprints[path] = (digest if proc.returncode == 0 and digest
                              else FINGERPRINT_UNAVAILABLE)
    return fingerprints


def _diff_porcelain(
    pre: list[str],
    post: list[str],
    pre_fingerprints: dict[str, str] | None = None,
    post_fingerprints: dict[str, str] | None = None,
) -> list[tuple[str, str]]:
    """NEW or CHANGED entries between the two snapshots (a path whose status
    is unchanged is not a mutation of this command's making) — PLUS, when
    fingerprints are supplied, tracked entries whose status code is unchanged
    but whose worktree CONTENT changed: a file already dirty pre-run stays
    " M" when a command mutates it further, invisible to status-code diffing
    alone. Such a path is included and classified like any other tracked
    change."""
    pre_map = _parse_porcelain(pre)
    post_map = _parse_porcelain(post)
    changed = {path: xy for path, xy in post_map.items()
               if pre_map.get(path) != xy}
    if pre_fingerprints is not None and post_fingerprints is not None:
        for path, xy in post_map.items():
            if path in changed or xy in ("??", "!!"):
                continue
            if pre_fingerprints.get(path) != post_fingerprints.get(path):
                changed[path] = xy
    return sorted(changed.items())


def _evidence_prefixes(evidence_targets: list[str]) -> list[str]:
    prefixes = []
    for target in evidence_targets:
        cleaned = target.strip().rstrip("*").rstrip("/")
        if cleaned:
            prefixes.append(cleaned)
    return prefixes


def _classify(path: str, xy: str, prefixes: list[str], repo_root: Path) -> str:
    """The contract's classification, applied in order."""
    bare = path.rstrip("/")
    if bare == GENERATED_ROOT_NAME or bare.startswith(GENERATED_ROOT_NAME + "/"):
        return CLASS_EXPECTED
    for prefix in prefixes:
        if bare == prefix or bare.startswith(prefix + "/"):
            return CLASS_EXPECTED
    if _is_ignored(repo_root, path):
        return CLASS_IGNORED
    if xy != "??":
        return CLASS_TRACKED
    return CLASS_UNTRACKED


# --- command resolution ---------------------------------------------------------

def _resolve_project_root(
    repo_root: Path, fence: brief_adoption.BriefFence,
    alias_by_root: dict[Path, str],
) -> Path:
    """The pilot project root that is a path prefix of the brief's first
    write_scope entry (roots from harness.py PROJECT_ALIASES, passed in by
    the caller). No match is an operational error, never a guess."""
    if not fence.write_scope:
        raise HarnessOperationalError(
            f"Brief {fence.tranche_id} declares no write_scope entry, so the "
            "project cannot be resolved — operational error, never guessed "
            "(K-INVENT-1).")
    entry = fence.write_scope[0]
    entry_parts = Path(entry).parts
    for root in sorted(alias_by_root, key=lambda r: len(r.parts), reverse=True):
        try:
            rel_parts = root.relative_to(repo_root).parts
        except ValueError:
            continue
        if entry_parts[: len(rel_parts)] == rel_parts:
            if not root.is_dir():
                raise HarnessOperationalError(f"Project root absent: {root}")
            return root
    raise HarnessOperationalError(
        f"The brief's first write_scope entry {entry!r} lies under no "
        "registered pilot project root (harness.py PROJECT_ALIASES); "
        "run-validations refuses rather than guessing the project "
        "(K-INVENT-1).")


def _declared_commands(manifest: AdapterManifest) -> list[tuple[str, str]]:
    """The manifest's validation_commands as (command, cwd) pairs, in order.
    A malformed entry is an operational error, never guessed."""
    commands: list[tuple[str, str]] = []
    for idx, vc in enumerate(manifest.validation_commands):
        if not isinstance(vc, dict) or not str(vc.get("command", "") or "").strip():
            raise HarnessOperationalError(
                f"validation_commands[{idx}] in {manifest.manifest_path} "
                "carries no command text; unparseable configuration is an "
                "operational error, never guessed (K-INVENT-1).")
        commands.append((str(vc["command"]).strip(),
                         str(vc.get("cwd", ".") or ".")))
    return commands


def _check_declaration_drift(
    report: Report, fence: brief_adoption.BriefFence,
    commands: list[tuple[str, str]], declared_in: str,
) -> None:
    """Cross-check the brief's declared validations text against the
    manifest list; the manifest governs on any drift."""
    manifest_cmds = [command for command, _cwd in commands]
    for command in manifest_cmds:
        if not any(command in entry for entry in fence.validations):
            report.add_finding(make_finding(
                Severity.WARN, "VALIDATION_DECLARATION_DRIFT", "declaration",
                MSG_DRIFT_MANIFEST_ONLY.format(command=command),
                declared_in, invariant="K-CONFLICT-1"))
    for entry in fence.validations:
        if not any(command in entry for command in manifest_cmds):
            report.add_finding(make_finding(
                Severity.WARN, "VALIDATION_DECLARATION_DRIFT", "declaration",
                MSG_DRIFT_BRIEF_ONLY.format(entry=entry),
                fence.source_path, invariant="K-CONFLICT-1"))


# --- execution -------------------------------------------------------------------

def _tool_versions(command: str) -> dict[str, str]:
    """Cheap version probes only, keyed off the command's first token."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    first = tokens[0] if tokens else ""
    if first not in VERSION_PROBE_TOOLS:
        return {}
    try:
        proc = subprocess.run(
            [first, "--version"], capture_output=True, text=True,
            timeout=_PROBE_TIMEOUT_SECONDS, check=False)
        lines = (proc.stdout or proc.stderr).strip().splitlines()
        return {first: lines[0] if lines else ""}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {first: f"probe unavailable: {exc.__class__.__name__}"}


def _execute(command: str, run_cwd: Path, timeout_seconds: int,
             ) -> tuple[int | None, bool, str, str, float]:
    """Run one declared command (shell=True in its own session). On timeout
    the whole process group is killed (the closest a subprocess caller gets
    to killing the process tree) and the outcome is TIMED_OUT/exit None."""
    start = time.monotonic()
    try:
        proc = subprocess.Popen(
            command, shell=True, cwd=str(run_cwd),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            start_new_session=hasattr(os, "setsid"))
    except OSError as exc:
        raise HarnessOperationalError(
            f"Cannot launch validation command {command!r} in {run_cwd}: "
            f"{exc}") from exc
    timed_out = False
    exit_code: int | None
    try:
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        exit_code = None
        try:
            if hasattr(os, "killpg"):
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            else:  # pragma: no cover - non-POSIX fallback
                proc.kill()
        except OSError:
            proc.kill()
        try:
            stdout, stderr = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover - kill raced
            stdout, stderr = "", ""
    duration = round(time.monotonic() - start, 3)
    return exit_code, timed_out, stdout or "", stderr or "", duration


# --- the command -----------------------------------------------------------------

def run_run_validations(
    repo_root: Path,
    brief_path: Path,
    out_dir: Path,
    timeout_seconds: int,
    list_only: bool,
    alias_by_root: dict[Path, str],
) -> Report:
    """See the module docstring for the contract. `alias_by_root` maps
    resolved pilot project root -> CLI alias, built by the caller from
    harness.py PROJECT_ALIASES (the cmd_next idiom; no circular imports)."""
    repo_root = repo_root.resolve()
    if timeout_seconds is None or timeout_seconds <= 0:
        raise HarnessOperationalError(
            f"--timeout-seconds must be a positive integer "
            f"(got {timeout_seconds!r}).")

    fence, adoption_findings, refusal = brief_adoption.verify_adoption(
        brief_path, repo_root)
    report = Report(command="run-validations")
    report.md(f"# run-validations — {fence.tranche_id}")
    report.md("")
    report.md(SCOPE_NOTE)
    report.md("")
    report.md(STRUCTURAL_EVIDENCE_NOTE)
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
        # D-GOV-04: nothing executed, nothing written; harness.py maps the
        # summary key to stderr + exit 2.
        report.md("")
        report.md(REFUSAL_NOTE)
        report.summary["identity_refusal"] = refusal
        return report
    for finding in adoption_findings:
        report.add_finding(finding)

    project_root = _resolve_project_root(repo_root, fence, alias_by_root)
    manifest = load_adapter(project_root)
    declared_in = str(manifest.manifest_path.relative_to(repo_root))
    commands = _declared_commands(manifest)
    report.summary["project"] = manifest.project
    report.summary["declared_in"] = declared_in
    report.md(f"- project: {manifest.project} "
              f"(root `{project_root.relative_to(repo_root)}`, resolved from "
              "the brief's first write_scope entry)")
    report.md(f"- timeout per command: {timeout_seconds}s")
    report.md("")

    _check_declaration_drift(report, fence, commands, declared_in)

    report.md(f"## Declared validation commands ({len(commands)})")
    report.md("")
    if commands:
        report.md("| # | command | cwd | declared_in |")
        report.md("|---|---|---|---|")
        for idx, (command, cwd) in enumerate(commands, start=1):
            report.md(f"| {idx} | `{command}` | `{cwd}` | `{declared_in}` |")
    else:
        report.md("- none declared")
    report.md("")

    if list_only:
        report.md(LIST_MODE_NOTE)
        report.summary["list_only"] = True
        report.summary["executed"] = 0
        return report

    if not fence.fence_active:
        report.add_finding(make_finding(
            Severity.REVIEW, "VALIDATION_RUN_WITHOUT_ACTIVE_FENCE", "adoption",
            MSG_RUN_WITHOUT_FENCE.format(state=fence.state),
            fence.source_path, invariant="K-AUTH-1", caveat=fence.cap_reason))

    # K-WRITE-2 (RATIFIED): the mutation BLOCK protects the substrate and
    # must not be suppressible by anything agent-authored. run-validations
    # deliberately runs on CANDIDATE/unadopted briefs, and a brief's
    # evidence_targets are agent-authorable text until a human adopts the
    # brief (D-GOV-04) — so brief-declared evidence_targets exempt changed
    # paths as expected_evidence_output ONLY when fence_active is True.
    # An unadopted brief's targets exempt NOTHING; otherwise a candidate
    # brief could declare a broad governed path as an evidence_target and
    # swallow governed-file mutations. The generated root
    # (_harness_generated/) is ALWAYS exempt — it is harness-owned,
    # gitignored scratch (D-GOV-01); that exemption lives in _classify,
    # independent of the fence.
    prefixes = (_evidence_prefixes(fence.evidence_targets)
                if fence.fence_active else [])
    class_counts: Counter[str] = Counter()
    run_rows: list[tuple[int, str, str, float, str]] = []
    record_rels: list[str] = []

    for idx, (command, cwd) in enumerate(commands, start=1):
        run_cwd = (project_root / cwd).resolve()
        if not run_cwd.is_dir():
            raise HarnessOperationalError(
                f"Declared cwd {cwd!r} for validation command {command!r} is "
                f"not a directory ({run_cwd}); operational error, never "
                "guessed (K-INVENT-1).")
        pre = _porcelain(repo_root)
        # Fingerprint tracked pre-run entries: an already-dirty tracked file
        # the command mutates further keeps its status code, so content
        # comparison is the only way to see that mutation (K-WRITE-2).
        pre_entries = _parse_porcelain(pre)
        pre_fingerprints = _tracked_fingerprints(repo_root, pre_entries)
        exit_code, timed_out, stdout, stderr, duration = _execute(
            command, run_cwd, timeout_seconds)
        tool_versions = _tool_versions(command)
        post = _porcelain(repo_root)
        # Re-fingerprint over the UNION of pre/post tracked entries; a path
        # gone from the post snapshot hashes to the labeled unavailable
        # state, never a guess (K-INVENT-1).
        post_fingerprints = _tracked_fingerprints(
            repo_root, {**pre_entries, **_parse_porcelain(post)})
        changed_paths = [
            {"path": path, "classification": _classify(path, xy, prefixes, repo_root)}
            for path, xy in _diff_porcelain(
                pre, post, pre_fingerprints, post_fingerprints)
        ]
        record = evidence_records.build_evidence_record(
            tranche_id=fence.tranche_id,
            brief_source_path=fence.source_path,
            brief_state=fence.state,
            brief_bound_sha=fence.bound_sha,
            fence_active=fence.fence_active,
            command=command,
            cwd=cwd,
            declared_in=declared_in,
            exit_code=exit_code,
            timed_out=timed_out,
            duration_seconds=duration,
            tool_versions=tool_versions,
            stdout=stdout,
            stderr=stderr,
            pre_run_porcelain=pre,
            post_run_porcelain=post,
            changed_paths=changed_paths,
        )
        json_path, _md_path = evidence_records.write_evidence_record(
            record, out_dir, repo_root)
        record_rel = str(json_path.relative_to(repo_root))
        record_rels.append(record_rel)

        by_class: dict[str, list[str]] = {}
        for cp in changed_paths:
            by_class.setdefault(cp["classification"], []).append(cp["path"])
            class_counts[cp["classification"]] += 1
        mutated = by_class.get(CLASS_TRACKED, [])
        if mutated:
            # UNCONDITIONAL BLOCK (K-WRITE-2, local technical): protects the
            # substrate, not the fence — no D-GOV-04 adoption cap.
            report.add_finding(make_finding(
                Severity.BLOCK, "VALIDATION_MUTATED_GOVERNED_FILES",
                "mutation-control",
                MSG_MUTATED.format(command=command,
                                   paths=", ".join(sorted(mutated))),
                record_rel, invariant="K-WRITE-2", local_technical=True))
        untracked = by_class.get(CLASS_UNTRACKED, [])
        if untracked:
            report.add_finding(make_finding(
                Severity.REVIEW, "VALIDATION_UNTRACKED_OUTPUT",
                "mutation-control",
                MSG_UNTRACKED_OUTPUT.format(command=command,
                                            paths=", ".join(sorted(untracked))),
                record_rel, invariant="K-WRITE-2"))
        for path in by_class.get(CLASS_IGNORED, []):
            report.add_fact(SourcedFact(
                fact_id="run_validations.ignored_cache",
                value=path, source_path=record_rel, source_hint=command,
                authority_status="observed", parse_status="PARSED"))
        if timed_out:
            report.add_finding(make_finding(
                Severity.WARN, "VALIDATION_COMMAND_TIMED_OUT", "evidence",
                MSG_TIMED_OUT.format(command=command, timeout=timeout_seconds),
                record_rel, invariant="K-INVENT-1"))
        report.add_fact(SourcedFact(
            fact_id=f"run_validations.run_{idx:02d}.exit",
            value="TIMED_OUT" if timed_out else str(exit_code),
            source_path=record_rel, source_hint=command,
            authority_status="harness_captured", parse_status="PARSED"))
        run_rows.append((
            idx, command, "TIMED_OUT" if timed_out else str(exit_code),
            duration, record_rel))

    report.md("## Runs")
    report.md("")
    if run_rows:
        report.md("| # | command | exit | duration (s) | evidence record |")
        report.md("|---|---|---|---|---|")
        for idx, command, exit_label, duration, record_rel in run_rows:
            report.md(f"| {idx} | `{command}` | {exit_label} | {duration} "
                      f"| `{record_rel}` |")
    else:
        report.md("- no commands declared; nothing executed")
    report.md("")
    report.md("## Changed-path classification summary")
    report.md("")
    if class_counts:
        for name in evidence_records.CLASSIFICATIONS:
            if class_counts.get(name):
                report.md(f"- {name}: {class_counts[name]}")
    else:
        report.md(f"- {NO_CHANGES_NOTE}")
    report.md("")

    report.summary["executed"] = len(run_rows)
    report.summary["records"] = record_rels
    report.summary["classification_counts"] = dict(class_counts)
    return report
