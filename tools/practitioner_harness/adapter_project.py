#!/usr/bin/env python3
"""Project adapter — read-only observation of a governed project tree.

Walks the manifest `status_glob`, parses each `_STATUS.md` via the versioned
prose-bullet-v1 dialect, and emits SourcedFacts plus per-file drift
comparisons. Also reads the decision register, DAG pointer surfaces, the plan
and coordination Status posture, and manifest-declared approval-SHA fields
(reachability verified via `git cat-file -e <sha>^{commit}`).

Everything here is observation; the cited source files govern.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import adapter_git_state
import prose_bullet_v1
from adapter_loader import AdapterManifest
from harness_common import SourcedFact

SHA_FIELD_RE = re.compile(r"\b([0-9a-f]{7,64})\b")
DECISION_ID_RE = re.compile(r"\bD-(?:APP|T0|GOV)-\d+\b|\bD-\d+[A-Za-z]?\b")
BLOCKED_ON_FIELD_RE = re.compile(
    r"^\s*(?:\*\*blocked-on:\*\*|blocked-on:)\s*(.*?)\s*$",
    re.IGNORECASE,
)


@dataclass
class StatusFileResult:
    path: Path
    rel_path: str
    doc: prose_bullet_v1.ParsedStatusDoc
    current_state: str | None
    current_state_line: int | None
    assertion: prose_bullet_v1.HistoryEntry | None
    trailing_unparseable: int
    mismatch: bool
    unparseable_doc: bool
    empty_history: bool
    approval_sha: str | None = None
    blocked_on: tuple[str, ...] = ()
    blocked_on_line: int | None = None


@dataclass
class ProjectObservation:
    manifest: AdapterManifest
    files: list[StatusFileResult] = field(default_factory=list)
    facts: list[SourcedFact] = field(default_factory=list)
    register_counts: dict[str, int] = field(default_factory=dict)
    sha_reachability: dict[str, bool | None] = field(default_factory=dict)

    @property
    def mismatches(self) -> list[StatusFileResult]:
        return [f for f in self.files if f.mismatch]


def _excluded(rel: PurePosixPath, exclude_globs: list[str]) -> bool:
    parts = set(rel.parts)
    for pattern in exclude_globs:
        if pattern.endswith("/**"):
            if pattern[:-3] in parts:
                return True
        elif rel.match(pattern):
            return True
    return False


def collect_status_files(manifest: AdapterManifest) -> list[Path]:
    root = manifest.project_root
    assert root is not None
    out: list[Path] = []
    for path in sorted(root.glob(manifest.status_glob)):
        rel = PurePosixPath(path.relative_to(root).as_posix())
        if _excluded(rel, manifest.exclude_globs):
            continue
        out.append(path)
    return out


def _field_line_number(text: str, key: str) -> int | None:
    pattern = re.compile(r"^\*\*" + re.escape(key) + r":\*\*", )
    for idx, line in enumerate(text.splitlines(), start=1):
        if pattern.match(line):
            return idx
    return None


def _blocked_on_tokens(text: str) -> tuple[tuple[str, ...], int | None]:
    for idx, line in enumerate(text.splitlines(), start=1):
        match = BLOCKED_ON_FIELD_RE.match(line)
        if not match:
            continue
        seen: set[str] = set()
        tokens: list[str] = []
        for token in DECISION_ID_RE.findall(match.group(1)):
            normalized = token.upper()
            if normalized in seen:
                continue
            seen.add(normalized)
            tokens.append(normalized)
        return tuple(tokens), idx
    return (), None


def analyze_status_file(path: Path, manifest: AdapterManifest, repo_root: Path) -> StatusFileResult:
    text = path.read_text(encoding="utf-8")
    doc = prose_bullet_v1.parse_status_document(text)
    assertion, trailing = prose_bullet_v1.last_state_assertion(doc.history, manifest.states)
    current = doc.current_state
    unparseable_doc = doc.doc_caveat_class == prose_bullet_v1.UNPARSEABLE
    mismatch = False
    if not unparseable_doc and current is not None and assertion is not None:
        mismatch = current.strip().upper() != (assertion.state or "").upper()
    approval_sha = None
    if manifest.guard_approval_sha_field:
        value = doc.fields.get(manifest.guard_approval_sha_field, "")
        m = SHA_FIELD_RE.search(value)
        if m:
            approval_sha = m.group(1)
    blocked_on, blocked_on_line = _blocked_on_tokens(text)
    return StatusFileResult(
        path=path,
        rel_path=str(path.relative_to(repo_root)),
        doc=doc,
        current_state=current,
        current_state_line=_field_line_number(text, "Current State"),
        assertion=assertion,
        trailing_unparseable=trailing,
        mismatch=mismatch,
        unparseable_doc=unparseable_doc,
        empty_history=len(doc.history) == 0,
        approval_sha=approval_sha,
        blocked_on=blocked_on,
        blocked_on_line=blocked_on_line,
    )


def _first_status_line(path: Path) -> tuple[str, int] | None:
    """Find the first self-declared Status posture line in a plan/coordination
    surface: `**Status:** ...`, `Status: ...`, or YAML-frontmatter `status: ...`."""
    if not path.is_file():
        return None
    patterns = (
        re.compile(r"^\*\*Status:?\*\*:?\s*(.+)$"),
        re.compile(r"^Status:\s*(.+)$"),
        re.compile(r"^status:\s*(.+)$"),
        re.compile(r"^>\s*\*\*Status:?\s*(.+)$"),
    )
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for pat in patterns:
            m = pat.match(line.strip())
            if m:
                return line.strip(), idx
    return None


def parse_decision_register(path: Path) -> dict[str, int]:
    """Parse `| ID | ... | State | ... |` markdown table rows; count by state."""
    counts: dict[str, int] = {}
    if not path.is_file():
        return counts
    state_col: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if state_col is None:
            lowered = [c.lower() for c in cells]
            if "state" in lowered and "id" in lowered:
                state_col = lowered.index("state")
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if state_col < len(cells):
            state = cells[state_col].strip("*` ").strip()
            if state:
                counts[state] = counts.get(state, 0) + 1
    return counts


def dag_pointer_facts(manifest: AdapterManifest, repo_root: Path) -> list[SourcedFact]:
    root = manifest.project_root
    assert root is not None
    path = root / manifest.dag_pointer
    rel = str(path.relative_to(repo_root)) if path.is_file() else manifest.dag_pointer
    facts: list[SourcedFact] = []
    if not path.is_file():
        facts.append(SourcedFact(
            fact_id="dag.pointer", value="artifact absent",
            source_path=rel, authority_status="declared-in-manifest",
            parse_status="NOT_APPLICABLE"))
        return facts
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Control-table lines (app-dev DAG_CLOSURE_CONTROL.md shape): | Field | Value |
    control_fields = (
        "CurrentClosureSnapshot", "StrictFullGraphStatus", "StrictSCCCount",
        "BlockerSubsetStatus", "ProjectBlockedAvailableReportable",
    )
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] in control_fields:
                facts.append(SourcedFact(
                    fact_id=f"dag.{cells[0]}", value=cells[1].strip("`"),
                    source_path=rel, source_hint=f"line {idx}",
                    authority_status="governed_committed", parse_status="PARSED"))
        # Piping _LATEST.md pointer shape.
        m = re.match(r"^-\s*Approved graph authority:\s*(.+)$", stripped)
        if m:
            facts.append(SourcedFact(
                fact_id="dag.approved_graph_authority", value=m.group(1).strip("` "),
                source_path=rel, source_hint=f"line {idx}",
                authority_status="governed_committed", parse_status="PARSED",
                caveat="Quoted from the pointer surface; the pointed-at record governs."))
    if not facts:
        facts.append(SourcedFact(
            fact_id="dag.pointer", value="artifact present; no recognized pointer lines",
            source_path=rel, authority_status="governed_committed",
            parse_status="UNPARSEABLE"))
    return facts


def plan_and_coordination_facts(manifest: AdapterManifest, repo_root: Path) -> list[SourcedFact]:
    root = manifest.project_root
    assert root is not None
    facts: list[SourcedFact] = []
    for fact_id, relpath in (
        ("plan", manifest.plan),
        ("coordination", manifest.coordination),
        ("coordination_pointer", manifest.coordination_pointer),
    ):
        if not relpath:
            continue
        path = root / relpath
        rel = str((root / relpath).relative_to(repo_root))
        if not path.is_file():
            facts.append(SourcedFact(
                fact_id=f"{fact_id}.exists", value="artifact absent",
                source_path=rel, authority_status="declared-in-manifest",
                parse_status="NOT_APPLICABLE"))
            continue
        facts.append(SourcedFact(
            fact_id=f"{fact_id}.exists", value="artifact present",
            source_path=rel, authority_status="governed_committed",
            parse_status="PARSED"))
        status = _first_status_line(path)
        if status is not None:
            line_text, line_no = status
            facts.append(SourcedFact(
                fact_id=f"{fact_id}.status_line", value=line_text,
                source_path=rel, source_hint=f"line {line_no}",
                authority_status="self-declared", parse_status="PARSED",
                caveat="Quoted verbatim; the source file governs."))
    return facts


def observe_project(manifest: AdapterManifest, repo_root: Path) -> ProjectObservation:
    obs = ProjectObservation(manifest=manifest)
    root = manifest.project_root
    assert root is not None
    for path in collect_status_files(manifest):
        obs.files.append(analyze_status_file(path, manifest, repo_root))
    obs.facts.extend(plan_and_coordination_facts(manifest, repo_root))
    obs.facts.extend(dag_pointer_facts(manifest, repo_root))
    register_path = root / manifest.decision_register
    obs.register_counts = parse_decision_register(register_path)
    if register_path.is_file():
        obs.facts.append(SourcedFact(
            fact_id="decision_register.counts",
            value=", ".join(f"{k}={v}" for k, v in sorted(obs.register_counts.items())) or "no rows parsed",
            source_path=str(register_path.relative_to(repo_root)),
            authority_status="governed_committed", parse_status="PARSED"))
    else:
        obs.facts.append(SourcedFact(
            fact_id="decision_register.counts", value="artifact absent",
            source_path=manifest.decision_register,
            authority_status="declared-in-manifest", parse_status="NOT_APPLICABLE"))
    # Approval-SHA reachability (only where the manifest declares the field).
    if manifest.guard_approval_sha_field:
        unique_shas = sorted({f.approval_sha for f in obs.files if f.approval_sha})
        for sha in unique_shas:
            obs.sha_reachability[sha] = adapter_git_state.sha_reachable(repo_root, sha)
    obs.facts.extend(adapter_git_state.git_state_facts(repo_root, scope=root))
    return obs
