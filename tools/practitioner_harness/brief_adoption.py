#!/usr/bin/env python3
"""Brief parsing + committed-adoption verification (Phase 3, D-GOV-04).

Adoption is a HUMAN act: a brief becomes an enforceable fence only when a
human sets its state to HUMAN_ADOPTED, attributes themselves against the
owner-curated allowlist, and the brief is COMMITTED to the governed record.
"An adoption existing only in a scratch directory does not exist" (D-GOV-04).
This module DETECTS that posture; it never performs any lifecycle transition
and never rewrites a brief.

Verification semantics (`verify_adoption`):
- CANDIDATE            -> fence inactive; INFO `BRIEF_NOT_ADOPTED`.
- adoption claimed (HUMAN_ADOPTED/EXECUTED/CHECKED/HUMAN_REVIEWED):
  identity first (refuse per D-GOV-04 when the allowlist is absent or the
  attributed actor does not match — refusals are exit-2 conditions, never
  severity findings), then committed-ness:
    under `_harness_generated/` (matched case-insensitively)
                                -> REVIEW `ADOPTION_IN_SCRATCH_DIR`;
    untracked                   -> REVIEW `ADOPTION_NOT_COMMITTED`;
    tracked but dirty           -> REVIEW `ADOPTION_UNCOMMITTED_EDITS`;
    clean                       -> fence_active, bound_sha = the publication
                                   commit (K-AUTH-2 binds adoption to content).
- CLOSED/SUPERSEDED    -> same identity + committed checks (a terminal brief
  still claims adoption), but fence inactive; INFO `BRIEF_LIFECYCLE_TERMINAL`.

Nothing here BLOCKs — by this module's own severity design (Phase 3
introduces no BLOCK findings; adoption posture is surfaced for humans,
never gated mechanically). The
capping hook Phase 4 applies against anything that is not a verified fence is
`harness_common.cap_severity_for_unadopted_brief` (re-exported here, not
duplicated): findings referencing a brief whose fence_active is False cap at
REVIEW, with `BriefFence.cap_reason` as the recorded reason. Unknown brief
state or missing identity fields are operational errors (exit 2), never
guesses (K-INVENT-1) — as are brief paths carrying a `..` component or
passing through a symlink: committed-adoption verification requires the real
committed path, never a redirected one.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from harness_common import (
    GENERATED_ROOT_NAME,
    HUMAN_ACTORS_RELPATH,
    Finding,
    HarnessOperationalError,
    Severity,
    SourcedFact,
    cap_severity_for_unadopted_brief,  # noqa: F401 - the Phase 4 capping hook, re-exported
    identity_refusal_message,
    load_human_actors,
    make_finding,
)

# Brief lifecycle states (metadata on harness artifacts only — never the
# deliverable lifecycle). Anything else is an operational error, never a guess.
BRIEF_STATES = (
    "CANDIDATE",
    "HUMAN_ADOPTED",
    "EXECUTED",
    "CHECKED",
    "HUMAN_REVIEWED",
    "CLOSED",
    "SUPERSEDED",
)
ADOPTION_CLAIMED_STATES = ("HUMAN_ADOPTED", "EXECUTED", "CHECKED", "HUMAN_REVIEWED")
TERMINAL_STATES = ("CLOSED", "SUPERSEDED")

# Header bullets and H2 sections `cmd_brief.run_brief` emits. Section headings
# are matched on the token before any parenthetical (so "validations
# (declared, not run)" keys as "validations"); top-level "- " bullets are the
# entries; indented sub-bullets (e.g. "  - source: ...") are annotations, not
# entries.
HEADER_KEYS = ("tranche_id", "state", "objective", "adopted_by", "adopted_on")
SECTION_KEYS = (
    "read_scope",
    "write_scope",
    "prohibited_paths",
    "validations",
    "evidence_targets",
    "stop_conditions",
    "human_decision_points",
)
# The placeholder entry cmd_brief emits for an empty section — not an entry.
EMPTY_SECTION_ENTRY = "none declared"

# An adoption field is a placeholder only when it is the TBD token itself
# ("TBD", "TBD — …", "TBD:"), never a real value that merely starts with the
# letters ("TBDenson" is an actor, matched or not — K-INVENT-1).
TBD_PLACEHOLDER_RE = re.compile(r"TBD\b")

MSG_NOT_ADOPTED = (
    "Brief state is CANDIDATE — a candidate projection; it fences nothing, and "
    "findings referencing it cap at REVIEW until a human adopts it and it is "
    "committed to the governed record (D-GOV-04)."
)
MSG_SCRATCH = (
    "Brief declares state {state} but resolves under the generated root "
    "_harness_generated/ — an adoption existing only in a scratch directory "
    "does not exist for reliance (D-GOV-04). Fence not active."
)
MSG_NOT_COMMITTED = (
    "Brief declares state {state} but the file is untracked by git; adoption "
    "binds to committed content (K-AUTH-2), and an adoption not committed to "
    "the governed record does not exist for reliance (D-GOV-04). Fence not active."
)
MSG_UNCOMMITTED_EDITS = (
    "Brief is tracked but the working copy differs from HEAD; K-AUTH-2 binds "
    "adoption to committed content — the uncommitted edit is not part of the "
    "adopted fence (D-GOV-04). Fence not active."
)
MSG_TERMINAL = (
    "Brief state is {state} — a terminal-state brief no longer fences new "
    "work; fence not active."
)

CAP_CANDIDATE = (
    "brief state is CANDIDATE — not HUMAN_ADOPTED+committed; findings "
    "referencing this brief cap at REVIEW (D-GOV-04)"
)
CAP_SCRATCH = (
    "adoption exists only under the generated scratch root — not part of the "
    "governed record (D-GOV-04); findings referencing this brief cap at REVIEW"
)
CAP_NOT_COMMITTED = (
    "brief file is untracked — adoption is not committed to the governed "
    "record (D-GOV-04 / K-AUTH-2); findings referencing this brief cap at REVIEW"
)
CAP_UNCOMMITTED_EDITS = (
    "working copy differs from HEAD — K-AUTH-2 binds adoption to committed "
    "content; findings referencing this brief cap at REVIEW"
)
CAP_TERMINAL = (
    "brief state is {state} — a terminal-state brief no longer fences new work"
)
CAP_REFUSAL = (
    "identity refusal — committed-adoption verification refused rather than "
    "guessed (D-GOV-04)"
)

CAVEAT_BOUND_SHA = (
    "Publication commit binding the adoption to content (K-AUTH-2)."
)
CAVEAT_TERMINAL_BOUND_SHA = (
    "Terminal-state brief — the SHA binds the committed adoption record; "
    "fence_active is False and this is not an active fence."
)

TEMPLATES: list[str] = [
    MSG_NOT_ADOPTED, MSG_SCRATCH, MSG_NOT_COMMITTED, MSG_UNCOMMITTED_EDITS,
    MSG_TERMINAL, CAP_CANDIDATE, CAP_SCRATCH, CAP_NOT_COMMITTED,
    CAP_UNCOMMITTED_EDITS, CAP_TERMINAL, CAP_REFUSAL,
    CAVEAT_BOUND_SHA, CAVEAT_TERMINAL_BOUND_SHA,
]


@dataclass
class BriefFence:
    """One parsed brief plus its verified-adoption posture.

    `fence_active` is True only for a HUMAN_ADOPTED-track brief whose identity
    matched the allowlist and whose file is committed clean to the governed
    record; `cap_reason` records why it is not (empty when active).
    `bound_sha` is the publication commit of a verified committed adoption,
    active or terminal (K-AUTH-2 binds adoption to content); empty unless
    verified. `fence_active` alone gates enforcement — a terminal brief's
    bound_sha binds the committed adoption record, not an active fence.
    """

    tranche_id: str
    state: str
    adopted_by: str = ""       # raw attributed value; "" when absent/TBD
    adopted_on: str = ""       # raw value; "" when absent/TBD
    objective: str = ""
    source_path: str = ""      # repo-relative; filled by verify_adoption
    read_scope: list[str] = field(default_factory=list)
    write_scope: list[str] = field(default_factory=list)
    prohibited_paths: list[str] = field(default_factory=list)
    validations: list[str] = field(default_factory=list)
    evidence_targets: list[str] = field(default_factory=list)
    stop_conditions: list[str] = field(default_factory=list)
    human_decision_points: list[str] = field(default_factory=list)
    fence_active: bool = False
    cap_reason: str = ""
    bound_sha: str = ""
    # Bookkeeping (not part of the fence contract):
    adopted_by_canonical: str = ""   # allowlist canonical name when matched
    committedness: str = ""          # scratch_dir|untracked|uncommitted_edits|committed_clean|not_checked
    facts: list[SourcedFact] = field(default_factory=list)


def _strip_ticks(value: str) -> str:
    return value.strip().strip("`").strip()


def _parse_entry(body: str) -> str:
    """One top-level '- ' bullet body -> entry text. Enclosing backticks are
    stripped; a trailing annotation after the closing backtick (e.g.
    "(under the declared generated root; D-GOV-01)") is tolerated and dropped."""
    body = body.strip()
    if body.startswith("`"):
        closing = body.find("`", 1)
        if closing > 0:
            return body[1:closing].strip()
    return body


def parse_brief_markdown(text: str) -> BriefFence:
    """Parse the Markdown a brief file carries (the `cmd_brief` emission
    format) into a BriefFence with fence_active=False (verification is
    `verify_adoption`'s job).

    Header bullets ("- tranche_id: ...", "- state: ...", "- objective: ...",
    "- adopted_by: ...", "- adopted_on: ...") are read before the first H2
    heading; adoption fields whose value is the TBD placeholder token
    (TBD_PLACEHOLDER_RE: "TBD" at a word boundary, so "TBDenson" is a real
    value) are treated as absent. Missing tranche_id/state or an unknown
    state value is a HarnessOperationalError — never guessed (K-INVENT-1).
    """
    header: dict[str, str] = {}
    sections: dict[str, list[str]] = {k: [] for k in SECTION_KEYS}
    current: str | None = None
    seen_heading = False
    for line in text.splitlines():
        if line.startswith("## "):
            seen_heading = True
            name = line[3:].strip()
            key = name.split(" (", 1)[0].strip()
            current = key if key in sections else None
            continue
        if line.startswith("#"):
            current = None
            continue
        if not line.startswith("- "):
            continue  # indented sub-bullets, prose, blockquote header: ignored
        body = line[2:]
        if not seen_heading:
            head, sep, value = body.partition(":")
            key = head.strip()
            if sep and key in HEADER_KEYS and key not in header:
                header[key] = value.strip()
            continue
        if current is not None:
            entry = _parse_entry(body)
            if entry and entry != EMPTY_SECTION_ENTRY:
                sections[current].append(entry)

    tranche_id = _strip_ticks(header.get("tranche_id", ""))
    if not tranche_id:
        raise HarnessOperationalError(
            "Brief carries no '- tranche_id:' header bullet; an unidentified "
            "brief is an operational error, never guessed (K-INVENT-1).")
    state = _strip_ticks(header.get("state", ""))
    if not state:
        raise HarnessOperationalError(
            f"Brief {tranche_id} carries no '- state:' header bullet; unknown "
            "brief state is an operational error, never guessed (K-INVENT-1).")
    if state not in BRIEF_STATES:
        raise HarnessOperationalError(
            f"Brief {tranche_id} declares unknown state {state!r}; expected "
            f"one of {', '.join(BRIEF_STATES)} — never guessed (K-INVENT-1).")
    adopted_by = header.get("adopted_by", "").strip()
    if TBD_PLACEHOLDER_RE.match(adopted_by):
        adopted_by = ""
    adopted_on = header.get("adopted_on", "").strip()
    if TBD_PLACEHOLDER_RE.match(adopted_on):
        adopted_on = ""
    return BriefFence(
        tranche_id=tranche_id,
        state=state,
        adopted_by=adopted_by,
        adopted_on=adopted_on,
        objective=header.get("objective", "").strip(),
        **{k: sections[k] for k in SECTION_KEYS},
    )


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git for the committed-ness checks. A missing git binary or a git
    hard failure (exit >1, e.g. 'not a git repository') is an operational
    error — committed-adoption verification cannot proceed without git truth."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True, text=True, check=False)
    except OSError as exc:
        raise HarnessOperationalError(
            f"git unavailable for committed-adoption verification: {exc}") from exc
    if proc.returncode not in (0, 1):
        raise HarnessOperationalError(
            "git failed during committed-adoption verification (git "
            f"{' '.join(args)} -> exit {proc.returncode}): {proc.stderr.strip()}")
    return proc


def _check_committedness(
    fence: BriefFence, resolved: Path, repo_root: Path, findings: list[Finding],
) -> bool:
    """Committed-ness of the brief file (git -C repo_root). Returns True when
    committed clean, filling bound_sha; else appends the one REVIEW finding
    for the first (most severe) failure mode and sets cap_reason."""
    # Scratch classification: LEXICAL prefix, CASE-INSENSITIVE components.
    # Deliberate asymmetry with the write guard: ensure_generated_scope
    # compares resolved parts case-SENSITIVELY so a case-variant prefix cannot
    # spoof containment — it fails CLOSED for writes; this classifier
    # casefolds each component so a case-variant spelling of the scratch root
    # (macOS filesystems are case-insensitive by default) cannot smuggle an
    # adoption out of scratch — it fails CLOSED for adoption. Both err toward
    # refusing/deactivating. The prefix is computed lexically from the
    # already-resolved repo_root — deliberately NOT generated_root(), whose
    # symlink refusal is a write-guard concern: a symlinked
    # _harness_generated/ must not break verification of an unrelated,
    # correctly committed brief (this read path is decoupled from the write
    # guard).
    scratch_prefix = repo_root / GENERATED_ROOT_NAME
    scratch_parts = tuple(p.casefold() for p in scratch_prefix.parts)
    resolved_folded = tuple(p.casefold() for p in resolved.parts)
    if resolved_folded[: len(scratch_parts)] == scratch_parts:
        fence.committedness = "scratch_dir"
        fence.cap_reason = CAP_SCRATCH
        findings.append(make_finding(
            Severity.REVIEW, "ADOPTION_IN_SCRATCH_DIR", "adoption",
            MSG_SCRATCH.format(state=fence.state), fence.source_path,
            invariant="K-AUTH-2"))
        return False
    tracked = _run_git(
        repo_root, "ls-files", "--error-unmatch", "--", fence.source_path
    ).returncode == 0
    if not tracked:
        fence.committedness = "untracked"
        fence.cap_reason = CAP_NOT_COMMITTED
        findings.append(make_finding(
            Severity.REVIEW, "ADOPTION_NOT_COMMITTED", "adoption",
            MSG_NOT_COMMITTED.format(state=fence.state), fence.source_path,
            invariant="K-AUTH-2"))
        return False
    porcelain = _run_git(
        repo_root, "status", "--porcelain", "--", fence.source_path
    ).stdout.strip()
    if porcelain:
        fence.committedness = "uncommitted_edits"
        fence.cap_reason = CAP_UNCOMMITTED_EDITS
        findings.append(make_finding(
            Severity.REVIEW, "ADOPTION_UNCOMMITTED_EDITS", "adoption",
            MSG_UNCOMMITTED_EDITS, fence.source_path, invariant="K-AUTH-2"))
        return False
    sha = _run_git(
        repo_root, "log", "-1", "--format=%H", "--", fence.source_path
    ).stdout.strip()
    if not sha:
        raise HarnessOperationalError(
            f"Cannot determine the publication commit for {fence.source_path} "
            "(git log returned nothing for a tracked, clean file); refusing "
            "rather than guessing (K-INVENT-1 / K-AUTH-2).")
    fence.committedness = "committed_clean"
    fence.bound_sha = sha
    caveat = CAVEAT_BOUND_SHA
    if fence.state in TERMINAL_STATES:
        caveat += " " + CAVEAT_TERMINAL_BOUND_SHA
    fence.facts.append(SourcedFact(
        fact_id="brief.adoption_bound_sha",
        value=sha,
        source_path=fence.source_path,
        source_hint="git log -1 --format=%H -- <path>",
        authority_status="governed_committed",
        parse_status="PARSED",
        caveat=caveat))
    return True


def verify_adoption(
    brief_path: Path, repo_root: Path,
) -> tuple[BriefFence, list[Finding], str | None]:
    """Committed-adoption verification of one brief file (detect, never
    rewrite). Returns (fence, findings, refusal); a non-None refusal is a
    D-GOV-04 exit-2 condition the caller must honor. Nothing here BLOCKs."""
    repo_root = repo_root.resolve()
    given = Path(brief_path)
    if ".." in given.parts:
        raise HarnessOperationalError(
            f"Brief path {brief_path} carries a '..' component; committed-"
            "adoption verification refuses lexical escapes — pass a path "
            "without .. components.")
    candidate = given if given.is_absolute() else repo_root / given
    # Refuse symlinks anywhere on the unresolved path BEFORE resolving:
    # resolve() silently follows links, so an untracked symlink could verify
    # a DIFFERENT (committed, adopted) file than the caller named and report
    # a redirected source_path. The write-side machinery (generated_root /
    # ensure_generated_scope) refuses symlinks for the same fail-closed
    # reason; committed-adoption verification requires the real committed
    # path. repo_root is already resolved, so only the caller-supplied tail
    # can trip this.
    prefix = Path(candidate.parts[0])
    for part in candidate.parts[1:]:
        prefix = prefix / part
        if prefix.is_symlink():
            raise HarnessOperationalError(
                f"Brief path {brief_path} passes through a symlink at "
                f"{prefix}; committed-adoption verification requires the "
                "real committed path — symlinks are refused fail-closed, as "
                "on the write side (D-GOV-04 / K-AUTH-2).")
    resolved = candidate.resolve()
    # Component-wise containment under the resolved repo root (the
    # ensure_generated_scope idiom): committed-adoption verification is
    # meaningless for a path outside the repository.
    root_parts = repo_root.parts
    if resolved.parts[: len(root_parts)] != root_parts:
        raise HarnessOperationalError(
            f"Brief path {brief_path} resolves outside the repo root "
            f"({resolved}); committed-adoption verification requires an "
            "in-repo path.")
    if not resolved.is_file():
        raise HarnessOperationalError(
            f"Brief file absent: {resolved} (operational error, exit 2).")

    fence = parse_brief_markdown(resolved.read_text(encoding="utf-8"))
    fence.source_path = str(resolved.relative_to(repo_root))
    findings: list[Finding] = []

    if fence.state == "CANDIDATE":
        # No identity check: no human is attributed on a candidate.
        fence.committedness = "not_checked"
        fence.cap_reason = CAP_CANDIDATE
        findings.append(make_finding(
            Severity.INFO, "BRIEF_NOT_ADOPTED", "adoption",
            MSG_NOT_ADOPTED, fence.source_path, invariant="K-AUTH-1"))
        return fence, findings, None

    # Adoption claimed (including terminal states — a terminal brief still
    # claims adoption): identity first, per D-GOV-04. Refusals produce NO
    # severity findings — they are exit-2 conditions.
    allowlist = load_human_actors(repo_root)
    if allowlist is None:
        fence.cap_reason = CAP_REFUSAL
        return fence, [], identity_refusal_message(
            f"Allowlist file absent ({HUMAN_ACTORS_RELPATH}); committed-"
            f"adoption verification of {fence.source_path} cannot attribute "
            "adopted_by.")
    if not fence.adopted_by:
        fence.cap_reason = CAP_REFUSAL
        return fence, [], identity_refusal_message(
            f"Brief {fence.source_path} declares state {fence.state} but "
            "carries no adopted_by actor.")
    matched = allowlist.match(fence.adopted_by)
    if matched is None:
        fence.cap_reason = CAP_REFUSAL
        return fence, [], identity_refusal_message(
            f"Attributed actor {fence.adopted_by!r} in {fence.source_path} "
            "matches no allowlist entry.")
    fence.adopted_by_canonical = matched

    clean = _check_committedness(fence, resolved, repo_root, findings)

    if fence.state in TERMINAL_STATES:
        fence.fence_active = False
        terminal_note = CAP_TERMINAL.format(state=fence.state)
        # A committedness cap_reason (e.g. untracked) must survive alongside
        # the terminal note — both reasons cap this brief.
        fence.cap_reason = (f"{fence.cap_reason}; {terminal_note}"
                            if fence.cap_reason else terminal_note)
        findings.append(make_finding(
            Severity.INFO, "BRIEF_LIFECYCLE_TERMINAL", "adoption",
            MSG_TERMINAL.format(state=fence.state), fence.source_path,
            invariant="K-AUTH-1"))
    elif clean:
        fence.fence_active = True
        fence.cap_reason = ""
    return fence, findings, None
