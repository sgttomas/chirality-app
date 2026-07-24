#!/usr/bin/env python3
"""Evidence records for `run-validations` (Phase 4) — schema
`practitioner-harness-evidence/v1`.

Authority class: **factual evidence artifact** (plan v3 §Authority Classes) —
never approval, never lifecycle state. Two-class self-exclusion rule: unlike
narrative projections (status/drift/self-check reports, which are NEVER read
back by any harness component), evidence records MAY be read back as facts
for the tranche that produced them — and never promote into lifecycle state,
approval state, plan state, or project status. The writer here is used by
`run-validations`; the reader by `evidence-check`.

Records land at `_harness_generated/evidence/<tranche_id>/NNN_<slug>.json`
(NNN = the 3-digit run ordinal per command; slug from the command text) plus
a sibling `.md` summary carrying the standard generated header. All writes go
through `write_generated_file` (contained to the generated root; D-GOV-01 /
K-WRITE-2).

K-INVENT-1 posture: a timed-out command is recorded as TIMED_OUT with
`exit_code` null — never an inferred outcome; stream truncation carries an
explicit marker; unreadable record files are labeled UNPARSEABLE by the
reader, never guessed and never a crash.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from harness_common import (
    DISCLAIMER_TEMPLATE,
    GENERATED_ROOT_NAME,
    MD_HEADER_TEMPLATE,
    GeneratedScopeError,
    HarnessOperationalError,
    ensure_generated_scope,
    write_generated_file,
)

EVIDENCE_SCHEMA = "practitioner-harness-evidence/v1"
EVIDENCE_DIR_NAME = "evidence"
STREAM_CAP_BYTES = 200_000

# Changed-path classifications (the mutation-control contract vocabulary).
CLASS_EXPECTED = "expected_evidence_output"
CLASS_IGNORED = "ignored_cache"
CLASS_TRACKED = "unexpected_tracked_change"
CLASS_UNTRACKED = "review_required_untracked"
CLASSIFICATIONS = (CLASS_EXPECTED, CLASS_IGNORED, CLASS_TRACKED, CLASS_UNTRACKED)

TRUNCATION_MARKER = (
    "[TRUNCATED — stream exceeded 200000 bytes; the remainder was not "
    "retained. Truncation is explicit, never silent (K-INVENT-1).]")

SELF_EXCLUSION_NOTE = (
    "Evidence record — a factual evidence artifact (two-class self-exclusion "
    "rule): readable as facts for the tranche that produced it; never "
    "promoted to lifecycle state, approval state, plan state, or project "
    "status.")

STRUCTURAL_EVIDENCE_NOTE = (
    "A completed run with exit 0 is structural evidence only, never approval "
    "(K-DOMAIN-4 analogue). Exit codes are recorded facts, never judgments.")

TIMED_OUT_NOTE = (
    "TIMED_OUT: the command hit the configured timeout; its exit code was "
    "not observed and is recorded as null — an unobserved outcome is never "
    "inferred (K-INVENT-1).")

NO_CHANGED_PATHS_NOTE = (
    "none observed (pre-run and post-run porcelain snapshots agree)")

TEMPLATES: list[str] = [
    TRUNCATION_MARKER, SELF_EXCLUSION_NOTE, STRUCTURAL_EVIDENCE_NOTE,
    TIMED_OUT_NOTE, NO_CHANGED_PATHS_NOTE,
]

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_ORDINAL_PREFIX_RE = re.compile(r"^(\d{3})_")


def slug_for_command(command: str, max_len: int = 40) -> str:
    """Filesystem slug from the command text (lowercased, non-alphanumeric
    runs collapsed to `_`, length-capped)."""
    slug = _SLUG_RE.sub("_", command.lower()).strip("_")
    slug = slug[:max_len].rstrip("_")
    return slug or "command"


def truncate_stream(text: str) -> tuple[str, bool]:
    """Cap one captured stream at STREAM_CAP_BYTES (UTF-8 bytes) with an
    explicit truncation marker appended. Returns (text, truncated)."""
    data = text.encode("utf-8", errors="replace")
    if len(data) <= STREAM_CAP_BYTES:
        return text, False
    clipped = data[:STREAM_CAP_BYTES].decode("utf-8", errors="replace")
    return clipped + "\n" + TRUNCATION_MARKER, True


def evidence_dir(out_dir: Path | str, tranche_id: str, repo_root: Path) -> Path:
    """The per-tranche records directory, containment-checked against the
    generated root (D-GOV-01 / K-WRITE-2) but not created."""
    return ensure_generated_scope(
        Path(out_dir) / EVIDENCE_DIR_NAME / tranche_id, repo_root)


def next_ordinal(records_dir: Path, slug: str) -> int:
    """The next 3-digit run ordinal for this command slug: 1 + the highest
    existing NNN among `NNN_<slug>.json` files (1 when none). Earlier runs'
    records are never overwritten."""
    best = 0
    if records_dir.is_dir():
        for path in records_dir.glob(f"[0-9][0-9][0-9]_{slug}.json"):
            m = _ORDINAL_PREFIX_RE.match(path.name)
            if m:
                best = max(best, int(m.group(1)))
    return best + 1


def build_evidence_record(
    *,
    tranche_id: str,
    brief_source_path: str,
    brief_state: str,
    brief_bound_sha: str,
    fence_active: bool,
    command: str,
    cwd: str,
    declared_in: str,
    exit_code: int | None,
    timed_out: bool,
    duration_seconds: float,
    tool_versions: dict,
    stdout: str,
    stderr: str,
    pre_run_porcelain: list[str],
    post_run_porcelain: list[str],
    changed_paths: list[dict],
) -> dict:
    """Assemble one schema-conformant record dict (streams truncated here;
    `captured_at` stamped here from datetime.now(timezone.utc))."""
    stdout, stdout_truncated = truncate_stream(stdout)
    stderr, stderr_truncated = truncate_stream(stderr)
    return {
        "schema": EVIDENCE_SCHEMA,
        # GEN-3 labeling marker (GENERATED_OUTPUT): evidence records live under
        # the generated root and must self-label as generated views, exactly
        # like Report.to_json_dict envelopes (harness_common).
        "authority_class": "generated_view",
        "tranche_id": tranche_id,
        "brief_source_path": brief_source_path,
        "brief_state": brief_state,
        "brief_bound_sha": brief_bound_sha,
        "fence_active": fence_active,
        "command": command,
        "cwd": cwd,
        "declared_in": declared_in,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_seconds": duration_seconds,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "tool_versions": tool_versions,
        "stdout": stdout,
        "stdout_truncated": stdout_truncated,
        "stderr": stderr,
        "stderr_truncated": stderr_truncated,
        "pre_run_porcelain": pre_run_porcelain,
        "post_run_porcelain": post_run_porcelain,
        "changed_paths": changed_paths,
        "disclaimer": DISCLAIMER_TEMPLATE.format(cmd="run-validations"),
    }


def render_record_markdown(record: dict, base_name: str) -> str:
    """The sibling .md summary: standard generated header + the record's
    facts. Exit codes are facts; a timed-out run is labeled TIMED_OUT."""
    out: list[str] = [MD_HEADER_TEMPLATE.format(cmd="run-validations")]
    out.append(f"# Evidence record {base_name} — {record['tranche_id']}")
    out.append("")
    out.append(SELF_EXCLUSION_NOTE)
    out.append("")
    out.append(f"- command: `{record['command']}` (cwd: `{record['cwd']}`)")
    out.append(f"- declared_in: `{record['declared_in']}`")
    exit_label = "TIMED_OUT" if record["timed_out"] else str(record["exit_code"])
    out.append(f"- exit: {exit_label}")
    if record["timed_out"]:
        out.append(f"  - {TIMED_OUT_NOTE}")
    out.append(f"- duration_seconds: {record['duration_seconds']}")
    out.append(f"- captured_at: {record['captured_at']}")
    out.append(f"- brief: `{record['brief_source_path']}` "
               f"(state {record['brief_state']}; "
               f"fence_active {record['fence_active']})")
    if record["brief_bound_sha"]:
        out.append(f"- brief_bound_sha: `{record['brief_bound_sha']}`")
    for tool, version in sorted(record.get("tool_versions", {}).items()):
        out.append(f"- tool version: {tool} = {version}")
    out.append(f"- stdout_truncated: {record['stdout_truncated']}; "
               f"stderr_truncated: {record['stderr_truncated']}")
    if record["changed_paths"]:
        out.append("")
        out.append("## Changed paths (mutation-control classification)")
        out.append("")
        out.append("| Path | Classification |")
        out.append("|---|---|")
        for cp in record["changed_paths"]:
            out.append(f"| `{cp['path']}` | {cp['classification']} |")
    else:
        out.append(f"- changed paths: {NO_CHANGED_PATHS_NOTE}")
    out.append("")
    out.append(STRUCTURAL_EVIDENCE_NOTE)
    out.append("")
    return "\n".join(out)


def write_evidence_record(
    record: dict, out_dir: Path | str, repo_root: Path,
) -> tuple[Path, Path]:
    """Write one record (json + md summary) under
    `<out_dir>/evidence/<tranche_id>/NNN_<slug>.*`, all writes routed through
    `write_generated_file`. Returns (json_path, md_path)."""
    slug = slug_for_command(record["command"])
    records_dir = evidence_dir(out_dir, record["tranche_id"], repo_root)
    base_name = f"{next_ordinal(records_dir, slug):03d}_{slug}"
    json_path = write_generated_file(
        records_dir / f"{base_name}.json",
        json.dumps(record, indent=2) + "\n", repo_root)
    md_path = write_generated_file(
        records_dir / f"{base_name}.md",
        render_record_markdown(record, base_name), repo_root)
    return json_path, md_path


@dataclass
class LoadedEvidenceRecord:
    """One file the reader saw: PARSED with the record dict, or UNPARSEABLE
    with a note — labeled, never guessed, never a crash (K-INVENT-1)."""

    path: str                 # repo-relative when under repo_root
    parse_status: str         # "PARSED" | "UNPARSEABLE"
    record: dict | None = None
    note: str = ""


def load_evidence_records(
    repo_root: Path, out_dir: Path | str, tranche_id: str,
) -> list[LoadedEvidenceRecord]:
    """Read the evidence records for one tranche (the `evidence-check` input
    path). Facts for the tranche that produced them only — never lifecycle,
    approval, or status (two-class self-exclusion). Unreadable, non-JSON,
    wrong-schema, or foreign-tranche files come back labeled UNPARSEABLE with
    a note; a missing directory INSIDE the generated root is an empty list.

    Fail-closed containment (same semantics as the write side): the records
    directory must resolve inside the declared generated root
    (`{repo_root}/_harness_generated`, via `ensure_generated_scope`) — a
    directory outside it (or a symlinked generated root) is a refusal, never
    an empty read: harness-captured evidence provenance exists only under
    the declared generated root (D-GOV-01 / K-WRITE-2)."""
    repo_root = repo_root.resolve()
    try:
        records_dir = evidence_dir(out_dir, tranche_id, repo_root)
    except GeneratedScopeError as exc:
        raise HarnessOperationalError(
            "Refusing to read evidence records from "
            f"{Path(out_dir) / EVIDENCE_DIR_NAME / tranche_id}: "
            "harness-captured evidence provenance exists only under the "
            f"declared generated root {GENERATED_ROOT_NAME}/ "
            "(D-GOV-01 / K-WRITE-2), and this directory does not resolve "
            "inside it. A symlinked generated root also refuses: capture "
            f"provenance cannot be trusted through a relocated boundary. "
            f"({exc})"
        ) from exc
    loaded: list[LoadedEvidenceRecord] = []
    if not records_dir.is_dir():
        return loaded
    for path in sorted(records_dir.glob("*.json")):
        try:
            rel = str(path.resolve().relative_to(repo_root))
        except ValueError:
            rel = str(path)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            loaded.append(LoadedEvidenceRecord(
                rel, "UNPARSEABLE",
                note=f"unreadable or non-JSON: {exc.__class__.__name__}: {exc}"))
            continue
        if not isinstance(data, dict) or data.get("schema") != EVIDENCE_SCHEMA:
            got = data.get("schema") if isinstance(data, dict) else type(data).__name__
            loaded.append(LoadedEvidenceRecord(
                rel, "UNPARSEABLE",
                note=(f"schema is {got!r}, not {EVIDENCE_SCHEMA!r} — labeled, "
                      "never guessed (K-INVENT-1)")))
            continue
        if data.get("tranche_id") != tranche_id:
            loaded.append(LoadedEvidenceRecord(
                rel, "UNPARSEABLE",
                note=(f"record declares tranche_id {data.get('tranche_id')!r} "
                      f"but was loaded for {tranche_id!r} — labeled, never "
                      "guessed (K-INVENT-1)")))
            continue
        loaded.append(LoadedEvidenceRecord(rel, "PARSED", record=data))
    return loaded
