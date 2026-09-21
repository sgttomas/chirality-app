#!/usr/bin/env python3
"""`bridge-status` - generated owner-shaped act pick-list for the bridge loop.

This is an inspection view, like `next`: it cites source records, never
selects a lane, and never changes governed state. Inputs are intentionally
boring and file-backed: the two project decision registers, the tier-0
decision register, the adopted profile's live-binding gate line, governed
brief records verified through the existing committed-adoption machinery,
and the latest bridge loop receipt.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import adapter_git_state
import adapter_project
import brief_adoption
from adapter_loader import load_adapter
from harness_common import Report, Severity, SourcedFact, make_finding

PICKLIST_NOTE = (
    "Sourced pick-list only: the tool never selects work; owner-shaped acts "
    "remain owner-side (K-AUTH-1 / D-GOV-04).")
REGISTER_NOTE = (
    "Open register rows are rows whose parsed state/ruling column does not "
    "start with RULED. State words are quoted from the register; the register "
    "governs on disagreement.")
PROFILE_NOTE = (
    "The profile gate line is a source input, not a gate resolver; source "
    "registers and receipts govern each named gate.")
BRIEF_NOTE = (
    "Brief posture is detected with brief_adoption.verify_adoption; "
    "fence_active is reported only as the verifier's mechanical result.")
RECEIPT_NOTE = (
    "The latest receipt supplies loop handoff context only; it is not a "
    "status surface.")
NO_OPEN_REGISTERS = (
    "No non-RULED register rows were parsed from the configured registers.")
NO_BRIEFS = "No governed brief markdown files found under docs/governance_harness/briefs/."
NO_OWNER_ACTS = "No owner-shaped act rows were derived from the configured inputs."
PARKED_NOTE = (
    "Parked-lane rows are parsed from the latest receipt. `anchored` means the "
    "lane text resolves to a register row, governed brief, PR pointer, or "
    "harness backlog/profile/decision-record item; `receipt-only` means the "
    "latest receipt is the only parsed home.")
GATE_NOTE = (
    "Gate rows are derived from the profile's own live-binding line, not from "
    "a hand-maintained gate list. Register rows and decision records are cited "
    "when the gate token resolves mechanically.")
BLOCKED_ON_NOTE = (
    "Deliverable blocked-on rows quote optional `blocked-on: D-XX[, D-YY]` "
    "tokens from deliverable `_STATUS.md` files. They are a reverse index from "
    "owner-side decisions to deliverable work; they do not change lifecycle "
    "state or resolve the decisions.")

TEMPLATES: list[str] = [
    PICKLIST_NOTE,
    REGISTER_NOTE,
    PROFILE_NOTE,
    BRIEF_NOTE,
    RECEIPT_NOTE,
    NO_OPEN_REGISTERS,
    NO_BRIEFS,
    NO_OWNER_ACTS,
    PARKED_NOTE,
    GATE_NOTE,
    BLOCKED_ON_NOTE,
]

REGISTER_SOURCES = (
    (
        "app-dev register",
        "projects/chirality-app-dev/execution/_Coordination/_DECISIONS/_REGISTER.md",
    ),
    (
        "piping register",
        "projects/chirality-piping/execution/_Coordination/_DECISIONS/_REGISTER.md",
    ),
    ("tier-0 register", "_DomainEngines/_DECISIONS/_REGISTER.md"),
    (
        "pec register",
        "projects/pec/execution/_Coordination/_DECISIONS/_REGISTER.md",
    ),
)

PROFILE_CANDIDATES = (
    "_DomainEngines/profiles/open_pipe_stress.yaml",
    "_DomainEngines/profiles/open_pipe_stress.DRAFT.yaml",
    "_DomainEngines/profiles/pec.yaml",
)

RECEIPTS_RELPATH = "_DomainEngines/bridge/LOOP_RECEIPTS.md"
BRIEFS_RELPATH = "docs/governance_harness/briefs"
PIPING_DECOMP_RELPATH = "projects/chirality-piping/execution/_Decomposition/SOFTWARE_DECOMP.md"
HARNESS_BACKLOG_RELPATH = "tools/practitioner_harness/BACKLOG.md"
BLOCKED_ON_PROJECT_RELPATHS = (
    "projects/chirality-app-dev",
    "projects/chirality-piping",
)

CANONICAL_RECEIPT_LABELS = (
    "Owner direction of record",
    "Gate outcome",
    "Parked lanes",
)
DECISION_ID_RE = re.compile(r"\bD-(?:APP|T0|GOV|PEC)-\d+\b|\bD-\d+[A-Za-z]?\b")
PR_REF_RE = re.compile(r"\bPR\s*#\d+\b", re.IGNORECASE)
HB_REF_RE = re.compile(r"\bHB(?:-[A-Z]+)?-\d+\b")


@dataclass(frozen=True)
class DecisionRow:
    source_label: str
    source_path: str
    line: int
    decision_id: str
    decision: str
    blocks: str
    state: str
    state_column: str


@dataclass(frozen=True)
class ProfileInfo:
    source_path: str
    profile_id: str = ""
    profile_status: str = ""
    profile_status_line: int | None = None
    profile_version: str = ""
    profile_version_line: int | None = None
    integration_level: str = ""
    integration_level_line: int | None = None
    live_binding_line: str = ""
    live_binding_line_no: int | None = None


@dataclass(frozen=True)
class ReceiptBullet:
    label: str
    text: str
    source_path: str
    line: int


@dataclass(frozen=True)
class ReceiptSummary:
    title: str
    source_path: str
    line: int
    bullets: tuple[ReceiptBullet, ...] = ()
    owner_direction: ReceiptBullet | None = None
    gate_outcome: ReceiptBullet | None = None
    parked_lanes: ReceiptBullet | None = None


@dataclass(frozen=True)
class BriefRecord:
    source_path: str
    tranche_id: str
    state: str
    fence_active: bool
    committedness: str
    bound_sha: str
    cap_reason: str


@dataclass(frozen=True)
class OwnerAct:
    source: str
    item: str
    posture: str
    owner_side: str


@dataclass(frozen=True)
class ParkedLaneRecord:
    lane: str
    anchor_status: str
    anchor_kind: str
    anchor_source: str
    source_path: str
    line: int


@dataclass(frozen=True)
class GateObservation:
    gate: str
    observed_state: str
    source_path: str
    line: int | None
    resolved_current: bool = False


@dataclass(frozen=True)
class BlockedOnRecord:
    decision_id: str
    project: str
    deliverable_dir: str
    current_state: str
    source_path: str
    line: int | None


def _source(path: str, line: int | None = None) -> str:
    return f"{path}:{line}" if line else path


def _esc(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _clean_cell(value: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def _split_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def _parse_decision_rows(repo_root: Path, label: str, relpath: str) -> list[DecisionRow]:
    path = repo_root / relpath
    if not path.is_file():
        return []
    rows: list[DecisionRow] = []
    headers: list[str] | None = None
    id_col = decision_col = blocks_col = state_col = None
    state_column_name = "State"
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = _split_table_cells(stripped)
        if headers is None:
            lowered = [_clean_cell(cell).lower() for cell in cells]
            if "id" not in lowered:
                continue
            state_idx = None
            for candidate in ("state", "humanruling"):
                if candidate in lowered:
                    state_idx = lowered.index(candidate)
                    state_column_name = (
                        "HumanRuling" if candidate == "humanruling" else "State")
                    break
            if state_idx is None:
                continue
            headers = lowered
            id_col = lowered.index("id")
            decision_col = lowered.index("decision") if "decision" in lowered else None
            blocks_col = lowered.index("blocks") if "blocks" in lowered else None
            state_col = state_idx
            continue
        if _is_separator(cells):
            continue
        assert id_col is not None and state_col is not None
        decision_id = _clean_cell(cells[id_col]) if id_col < len(cells) else ""
        if not decision_id:
            continue
        decision = (
            _clean_cell(cells[decision_col])
            if decision_col is not None and decision_col < len(cells)
            else ""
        )
        blocks = (
            _clean_cell(cells[blocks_col])
            if blocks_col is not None and blocks_col < len(cells)
            else ""
        )
        state = _clean_cell(cells[state_col]) if state_col < len(cells) else ""
        rows.append(
            DecisionRow(
                source_label=label,
                source_path=relpath,
                line=idx,
                decision_id=decision_id,
                decision=decision,
                blocks=blocks,
                state=state,
                state_column=state_column_name,
            )
        )
    return rows


def _open_register_rows(repo_root: Path) -> tuple[list[DecisionRow], int]:
    all_rows = _all_register_rows(repo_root)
    open_rows = [row for row in all_rows if not row.state.upper().startswith("RULED")]
    return open_rows, len(all_rows)


def _all_register_rows(repo_root: Path) -> list[DecisionRow]:
    all_rows: list[DecisionRow] = []
    for label, relpath in REGISTER_SOURCES:
        all_rows.extend(_parse_decision_rows(repo_root, label, relpath))
    return all_rows


def _field_value(line: str) -> str:
    _, _, raw = line.partition(":")
    value = raw.split("#", 1)[0].strip()
    return value.strip('"').strip("'")


def _load_profile_from_path(repo_root: Path, relpath: str) -> ProfileInfo | None:
    path = repo_root / relpath
    if not path.is_file():
        return None
    kwargs: dict[str, object] = {"source_path": relpath}
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("id:"):
            kwargs["profile_id"] = _field_value(stripped)
        elif stripped.startswith("profile_status:"):
            kwargs["profile_status"] = _field_value(stripped)
            kwargs["profile_status_line"] = idx
        elif stripped.startswith("profile_version:"):
            kwargs["profile_version"] = _field_value(stripped)
            kwargs["profile_version_line"] = idx
        elif stripped.startswith("integration_level:"):
            kwargs["integration_level"] = _field_value(stripped)
            kwargs["integration_level_line"] = idx
        elif "Live binding" in stripped and "gated" in stripped:
            kwargs["live_binding_line"] = stripped.lstrip("- ").strip().strip('"')
            kwargs["live_binding_line_no"] = idx
    if not kwargs.get("profile_id"):
        kwargs["profile_id"] = Path(relpath).stem.removesuffix(".DRAFT")
    return ProfileInfo(**kwargs)


def _load_profiles(repo_root: Path) -> list[ProfileInfo]:
    profiles: list[ProfileInfo] = []
    seen: set[str] = set()
    for relpath in PROFILE_CANDIDATES:
        profile = _load_profile_from_path(repo_root, relpath)
        if profile is None:
            continue
        key = profile.profile_id or profile.source_path
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    return profiles


def _load_profile(repo_root: Path) -> ProfileInfo | None:
    profiles = _load_profiles(repo_root)
    for profile in profiles:
        if profile.profile_id == "open_pipe_stress":
            return profile
    return profiles[0] if profiles else None


def _receipt_bullets(
    lines: list[str], start_idx: int, end_idx: int, source_path: str,
) -> list[ReceiptBullet]:
    bullets: list[ReceiptBullet] = []
    current_text: list[str] = []
    current_line = 0
    for offset in range(start_idx + 1, end_idx):
        line = lines[offset]
        if line.startswith("  - "):
            if current_text:
                bullets.append(_make_receipt_bullet(current_text, source_path, current_line))
            current_text = [line[4:].strip()]
            current_line = offset + 1
        elif current_text and (line.startswith("    ") or not line.strip()):
            continuation = line.strip()
            if continuation:
                current_text.append(continuation)
    if current_text:
        bullets.append(_make_receipt_bullet(current_text, source_path, current_line))
    return bullets


def _make_receipt_bullet(parts: list[str], source_path: str, line: int) -> ReceiptBullet:
    text = re.sub(r"\s+", " ", " ".join(parts)).strip()
    label = text.split(":", 1)[0].strip() if ":" in text else ""
    return ReceiptBullet(label=label, text=text, source_path=source_path, line=line)


def _receipt_summaries(repo_root: Path) -> list[ReceiptSummary]:
    relpath = RECEIPTS_RELPATH
    path = repo_root / relpath
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = re.match(r"^- \*\*(.+?)\*\*", line.strip())
        if match:
            starts.append((idx, _clean_cell(match.group(1))))
    if not starts:
        return []
    summaries: list[ReceiptSummary] = []
    for pos, (start_idx, title) in enumerate(starts):
        end_idx = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        bullets = _receipt_bullets(lines, start_idx, end_idx, relpath)
        by_label = {bullet.label.lower(): bullet for bullet in bullets if bullet.label}
        summaries.append(
            ReceiptSummary(
                title=title,
                source_path=relpath,
                line=start_idx + 1,
                bullets=tuple(bullets),
                owner_direction=by_label.get("owner direction of record"),
                gate_outcome=by_label.get("gate outcome"),
                parked_lanes=by_label.get("parked lanes"),
            )
        )
    return summaries


def _latest_receipt(repo_root: Path) -> ReceiptSummary | None:
    receipts = _receipt_summaries(repo_root)
    return receipts[-1] if receipts else None


def _brief_records(repo_root: Path) -> tuple[list[BriefRecord], str | None]:
    brief_dir = repo_root / BRIEFS_RELPATH
    if not brief_dir.is_dir():
        return [], None
    records: list[BriefRecord] = []
    for path in sorted(brief_dir.glob("*.md")):
        fence, _findings, refusal = brief_adoption.verify_adoption(path, repo_root)
        if refusal is not None:
            return records, refusal
        records.append(
            BriefRecord(
                source_path=fence.source_path,
                tranche_id=fence.tranche_id,
                state=fence.state,
                fence_active=fence.fence_active,
                committedness=fence.committedness or "not_checked",
                bound_sha=fence.bound_sha,
                cap_reason=fence.cap_reason,
            )
        )
    return records, None


def _row_action(row: DecisionRow) -> str:
    state = row.state.upper()
    if "AWAITING_RULING" in state:
        return "owner ruling on the cited packet"
    if "NOT_PREPARED" in state:
        return "owner direction to prepare, or leave held"
    return "owner disposition of the non-RULED register row"


def _owner_acts(
    open_rows: list[DecisionRow],
    profile: ProfileInfo | None,
    receipt: ReceiptSummary | None,
    briefs: list[BriefRecord],
    blocked_on: list[BlockedOnRecord],
) -> list[OwnerAct]:
    acts: list[OwnerAct] = []
    if receipt and receipt.gate_outcome:
        acts.append(
            OwnerAct(
                source=_source(receipt.gate_outcome.source_path, receipt.gate_outcome.line),
                item="latest gate outcome",
                posture=receipt.gate_outcome.text,
                owner_side="owner/environment disposition named by the receipt",
            )
        )
    if receipt and receipt.parked_lanes:
        acts.append(
            OwnerAct(
                source=_source(receipt.parked_lanes.source_path, receipt.parked_lanes.line),
                item="parked lanes",
                posture=receipt.parked_lanes.text,
                owner_side="owner direction after the named prerequisite",
            )
        )
    for row in open_rows:
        acts.append(
            OwnerAct(
                source=_source(row.source_path, row.line),
                item=f"{row.source_label} {row.decision_id}",
                posture=f"{row.state_column}={row.state}",
                owner_side=_row_action(row),
            )
        )
    if profile and profile.live_binding_line:
        acts.append(
            OwnerAct(
                source=_source(profile.source_path, profile.live_binding_line_no),
                item="profile live-binding gate set",
                posture=profile.live_binding_line,
                owner_side="source-specific gate disposition before L2/L3 binding",
            )
        )
    for brief in briefs:
        if brief.fence_active:
            acts.append(
                OwnerAct(
                    source=brief.source_path,
                    item=f"active brief {brief.tranche_id}",
                    posture=f"state={brief.state}; fence_active=True",
                    owner_side="owner review or next-phase direction if continuing this brief",
                )
            )
    open_decision_ids = {row.decision_id for row in open_rows}
    for record in blocked_on:
        if record.decision_id not in open_decision_ids:
            continue
        acts.append(
            OwnerAct(
                source=_source(record.source_path, record.line),
                item=f"{record.decision_id} blocked deliverable {record.project}/{record.deliverable_dir}",
                posture=f"Current State={record.current_state}",
                owner_side=f"owner disposition of {record.decision_id} before tagged deliverable work resumes",
            )
        )
    return acts


def _find_decision_row(repo_root: Path, relpath: str, decision_id: str) -> DecisionRow | None:
    for label, source_relpath in REGISTER_SOURCES:
        if source_relpath != relpath:
            continue
        for row in _parse_decision_rows(repo_root, label, source_relpath):
            if row.decision_id == decision_id:
                return row
    return None


def _row_by_id(rows: list[DecisionRow]) -> dict[str, DecisionRow]:
    return {row.decision_id: row for row in rows}


def _receipt_missing_labels(receipt: ReceiptSummary) -> list[str]:
    labels = {bullet.label.lower() for bullet in receipt.bullets if bullet.label}
    return [label for label in CANONICAL_RECEIPT_LABELS if label.lower() not in labels]


def _parked_lane_parts(bullet: ReceiptBullet | None) -> list[str]:
    if bullet is None:
        return []
    body = bullet.text.split(":", 1)[1] if ":" in bullet.text else bullet.text
    parts: list[str] = []
    for raw in re.split(r";\s*|,\s*", body):
        text = raw.strip().strip(".")
        if text:
            parts.append(text)
    return parts


def _classify_parked_lane(
    repo_root: Path,
    lane: str,
    source_path: str,
    line: int,
    rows_by_id: dict[str, DecisionRow],
    briefs: list[BriefRecord],
) -> ParkedLaneRecord:
    row_hits = [rows_by_id[match.group(0)]
                for match in DECISION_ID_RE.finditer(lane)
                if match.group(0) in rows_by_id]
    if row_hits:
        anchors = ", ".join(
            f"{row.decision_id}@{_source(row.source_path, row.line)}"
            for row in row_hits)
        return ParkedLaneRecord(
            lane=lane,
            anchor_status="anchored",
            anchor_kind="register",
            anchor_source=anchors,
            source_path=source_path,
            line=line,
        )
    for brief in briefs:
        if brief.tranche_id in lane:
            return ParkedLaneRecord(
                lane=lane,
                anchor_status="anchored",
                anchor_kind="governed brief",
                anchor_source=brief.source_path,
                source_path=source_path,
                line=line,
            )
    prs = PR_REF_RE.findall(lane)
    if prs:
        return ParkedLaneRecord(
            lane=lane,
            anchor_status="anchored",
            anchor_kind="PR pointer",
            anchor_source=", ".join(prs),
            source_path=source_path,
            line=line,
        )
    hb_sources = []
    for hb in HB_REF_RE.findall(lane):
        found = _find_backlog_item(repo_root, hb)
        if found is not None:
            hb_sources.append(f"{hb}@{_source(found[0], found[1])}")
    if hb_sources:
        return ParkedLaneRecord(
            lane=lane,
            anchor_status="anchored",
            anchor_kind="harness backlog",
            anchor_source=", ".join(hb_sources),
            source_path=source_path,
            line=line,
        )
    dec_sources = []
    for dec in re.findall(r"\bDEC-\d+\b", lane):
        found = _find_decision_record_line(repo_root, dec)
        if found is not None:
            dec_sources.append(f"{dec}@{_source(found[0], found[1])}")
    if dec_sources:
        return ParkedLaneRecord(
            lane=lane,
            anchor_status="anchored",
            anchor_kind="decision record",
            anchor_source=", ".join(dec_sources),
            source_path=source_path,
            line=line,
        )
    if re.search(r"\blive binding\b", lane, re.IGNORECASE):
        profile = _load_profile(repo_root)
        if profile is not None and profile.live_binding_line:
            return ParkedLaneRecord(
                lane=lane,
                anchor_status="anchored",
                anchor_kind="profile live-binding line",
                anchor_source=_source(profile.source_path, profile.live_binding_line_no),
                source_path=source_path,
                line=line,
            )
    if re.search(r"\bF3\b", lane):
        row = rows_by_id.get("D-T0-08")
        if row is not None:
            return ParkedLaneRecord(
                lane=lane,
                anchor_status="anchored",
                anchor_kind="tier-0 F3 sequence row",
                anchor_source=f"{row.decision_id}@{_source(row.source_path, row.line)}",
                source_path=source_path,
                line=line,
            )
    return ParkedLaneRecord(
        lane=lane,
        anchor_status="receipt-only",
        anchor_kind="-",
        anchor_source="-",
        source_path=source_path,
        line=line,
    )


def _parked_lane_records(
    repo_root: Path,
    receipt: ReceiptSummary | None,
    rows: list[DecisionRow],
    briefs: list[BriefRecord],
) -> list[ParkedLaneRecord]:
    if receipt is None or receipt.parked_lanes is None:
        return []
    rows_by_id = _row_by_id(rows)
    return [
        _classify_parked_lane(
            repo_root,
            part,
            receipt.parked_lanes.source_path,
            receipt.parked_lanes.line,
            rows_by_id,
            briefs,
        )
        for part in _parked_lane_parts(receipt.parked_lanes)
    ]


def _find_backlog_item(repo_root: Path, item_id: str) -> tuple[str, int] | None:
    path = repo_root / HARNESS_BACKLOG_RELPATH
    if not path.is_file():
        return None
    heading = re.compile(rf"^##\s+{re.escape(item_id)}\b")
    table_row = re.compile(rf"^\|\s*{re.escape(item_id)}\s*\|")
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if heading.search(line) or table_row.search(line):
            return HARNESS_BACKLOG_RELPATH, idx
    return None


def _live_binding_gate_tokens(line: str) -> list[str]:
    if not line:
        return []
    _, sep, after = line.partition(":")
    body = after if sep else line
    body = re.sub(r"\s*\([^)]*\)\.?\s*$", "", body).strip().strip(".")
    return [part.strip() for part in body.split(",") if part.strip()]


def _find_decision_record_line(repo_root: Path, decision_id: str) -> tuple[str, int] | None:
    path = repo_root / PIPING_DECOMP_RELPATH
    if not path.is_file():
        return None
    needle = f"|{decision_id}|"
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if needle in line:
            return PIPING_DECOMP_RELPATH, idx
    return None


def _live_binding_gate_observations(
    repo_root: Path,
    profile: ProfileInfo | None,
    rows: list[DecisionRow],
) -> list[GateObservation]:
    if profile is None or not profile.live_binding_line:
        return []
    rows_by_id = _row_by_id(rows)
    observations: list[GateObservation] = []
    for token in _live_binding_gate_tokens(profile.live_binding_line):
        lower = token.lower()
        if "tier-0 adoption" in lower and profile.profile_status:
            observations.append(GateObservation(
                gate=token,
                observed_state=f"profile_status={profile.profile_status}",
                source_path=profile.source_path,
                line=profile.profile_status_line,
                resolved_current=profile.profile_status.upper() == "ADOPTED",
            ))
            continue
        if "app-dev f3" in lower:
            row = rows_by_id.get("D-T0-08")
            if row is not None:
                observations.append(GateObservation(
                    gate=token,
                    observed_state=f"{row.decision_id} {row.state_column}={row.state}",
                    source_path=row.source_path,
                    line=row.line,
                    resolved_current=False,
                ))
            else:
                observations.append(GateObservation(
                    gate=token,
                    observed_state="not mechanically resolved",
                    source_path=profile.source_path,
                    line=profile.live_binding_line_no,
                ))
            continue
        id_match = DECISION_ID_RE.search(token)
        if id_match and id_match.group(0) in rows_by_id:
            row = rows_by_id[id_match.group(0)]
            observations.append(GateObservation(
                gate=token,
                observed_state=f"{row.decision_id} {row.state_column}={row.state}",
                source_path=row.source_path,
                line=row.line,
                resolved_current=row.state.upper().startswith("RULED"),
            ))
            continue
        dec_match = re.search(r"\bDEC-\d+\b", token)
        if dec_match:
            located = _find_decision_record_line(repo_root, dec_match.group(0))
            if located is not None:
                source_path, line = located
                observations.append(GateObservation(
                    gate=token,
                    observed_state=f"{dec_match.group(0)} recorded; condition text governs",
                    source_path=source_path,
                    line=line,
                    resolved_current=False,
                ))
                continue
        observations.append(GateObservation(
            gate=token,
            observed_state="not mechanically resolved",
            source_path=profile.source_path,
            line=profile.live_binding_line_no,
        ))
    return observations


def _add_fact(report: Report, fact_id: str, value: str, source: str, line: int | None = None) -> None:
    report.add_fact(
        SourcedFact(
            fact_id=fact_id,
            value=value,
            source_path=source,
            source_hint=f"line {line}" if line else "",
            authority_status="observed",
            parse_status="PARSED",
        )
    )


def _blocked_on_records(repo_root: Path) -> list[BlockedOnRecord]:
    records: list[BlockedOnRecord] = []
    for relroot in BLOCKED_ON_PROJECT_RELPATHS:
        project_root = repo_root / relroot
        if not project_root.is_dir():
            continue
        manifest = load_adapter(project_root)
        for path in adapter_project.collect_status_files(manifest):
            result = adapter_project.analyze_status_file(path, manifest, repo_root)
            if not result.blocked_on:
                continue
            state = (result.current_state or "UNKNOWN").strip().upper()
            for decision_id in result.blocked_on:
                records.append(
                    BlockedOnRecord(
                        decision_id=decision_id,
                        project=manifest.project,
                        deliverable_dir=path.parent.name,
                        current_state=state,
                        source_path=result.rel_path,
                        line=result.blocked_on_line,
                    )
                )
    return records


def run_bridge_status(repo_root: Path) -> Report:
    report = Report(command="bridge-status")
    rows = _all_register_rows(repo_root)
    open_rows = [row for row in rows if not row.state.upper().startswith("RULED")]
    parsed_register_rows = len(rows)
    profiles = _load_profiles(repo_root)
    profile = _load_profile(repo_root)
    receipt = _latest_receipt(repo_root)
    briefs, refusal = _brief_records(repo_root)
    parked_lanes = _parked_lane_records(repo_root, receipt, rows, briefs)
    gate_observations = _live_binding_gate_observations(repo_root, profile, rows)
    blocked_on = _blocked_on_records(repo_root)
    owner_acts = _owner_acts(open_rows, profile, receipt, briefs, blocked_on)

    report.md("# Bridge status - owner-shaped act pick-list")
    report.md("")
    report.md(PICKLIST_NOTE)
    report.md("")

    report.md("## Git state")
    report.md("")
    for fact in adapter_git_state.git_state_facts(repo_root):
        report.add_fact(fact)
        report.md(f"- {fact.fact_id}: {fact.value}")
    report.md("")

    report.md("## Latest bridge receipt")
    report.md("")
    report.md(RECEIPT_NOTE)
    report.md("")
    if receipt is None:
        report.md(f"- receipt file absent or no receipt headings parsed: `{RECEIPTS_RELPATH}`")
    else:
        report.md(f"- latest: `{receipt.title}` - `{_source(receipt.source_path, receipt.line)}`")
        _add_fact(report, "bridge_status.latest_receipt", receipt.title, receipt.source_path, receipt.line)
        missing = _receipt_missing_labels(receipt)
        if missing:
            report.add_finding(make_finding(
                Severity.WARN,
                "RECEIPT_BULLET_LABEL_DRIFT",
                "staleness",
                "Latest receipt lacks canonical bridge-loop bullet label(s): "
                + ", ".join(missing)
                + ". Exact labels keep generated views from silently dropping "
                  "owner-direction, gate-outcome, or parked-lane handoff data.",
                receipt.source_path,
                receipt.line,
                invariant="K-STALE-2",
            ))
        for label, bullet in (
            ("owner direction", receipt.owner_direction),
            ("gate outcome", receipt.gate_outcome),
            ("parked lanes", receipt.parked_lanes),
        ):
            if bullet is None:
                continue
            report.md(f"- {label}: {bullet.text} - `{_source(bullet.source_path, bullet.line)}`")
            _add_fact(
                report,
                "bridge_status." + label.replace(" ", "_"),
                bullet.text,
                bullet.source_path,
                bullet.line,
            )
    report.md("")

    report.md("## Parked lane classification")
    report.md("")
    report.md(PARKED_NOTE)
    report.md("")
    if not parked_lanes:
        report.md("- no parked-lane bullet parsed from the latest receipt")
    else:
        report.md("| Lane | Classification | Anchor kind | Anchor source | Source |")
        report.md("|---|---|---|---|---|")
        for lane in parked_lanes:
            report.md(
                f"| {_esc(lane.lane)} | {_esc(lane.anchor_status)} | "
                f"{_esc(lane.anchor_kind)} | {_esc(lane.anchor_source)} | "
                f"`{_source(lane.source_path, lane.line)}` |"
            )
    report.md("")

    report.md("## Open decision-register rows")
    report.md("")
    report.md(REGISTER_NOTE)
    report.md("")
    if not open_rows:
        report.md(NO_OPEN_REGISTERS)
    else:
        report.md("| Register | ID | State column | State | Blocks | Source |")
        report.md("|---|---|---|---|---|---|")
        for row in open_rows:
            report.md(
                f"| {_esc(row.source_label)} | `{_esc(row.decision_id)}` | "
                f"{_esc(row.state_column)} | {_esc(row.state)} | "
                f"{_esc(row.blocks or row.decision)} | `{_source(row.source_path, row.line)}` |"
            )
            _add_fact(
                report,
                f"bridge_status.open_register_row.{row.decision_id}",
                row.state,
                row.source_path,
                row.line,
            )
    report.md("")

    report.md("## Deliverable blocked-on links")
    report.md("")
    report.md(BLOCKED_ON_NOTE)
    report.md("")
    if not blocked_on:
        report.md("- no `blocked-on` tokens parsed from configured deliverable `_STATUS.md` files")
    else:
        report.md("| Decision | Project | Deliverable directory | Current State | Source |")
        report.md("|---|---|---|---|---|")
        for record in sorted(blocked_on, key=lambda r: (r.decision_id, r.project, r.deliverable_dir)):
            report.md(
                f"| `{_esc(record.decision_id)}` | {_esc(record.project)} | "
                f"`{_esc(record.deliverable_dir)}` | {_esc(record.current_state)} | "
                f"`{_source(record.source_path, record.line)}` |"
            )
            _add_fact(
                report,
                f"bridge_status.blocked_on.{record.decision_id}.{record.project}.{record.deliverable_dir}",
                record.current_state,
                record.source_path,
                record.line,
            )
    report.md("")

    report.md("## Live-binding gate inputs")
    report.md("")
    report.md(PROFILE_NOTE)
    report.md("")
    if not profiles:
        report.md("- profile absent: no configured profile candidate found")
    else:
        report.md("| Profile | Status | Gate posture | Integration level | Source |")
        report.md("|---|---|---|---|---|")
        for item in profiles:
            gate_posture = (
                "Gate 2 open"
                if item.profile_status.upper() in {"DRAFT", "VALIDATED"}
                else "Gate 2 adopted"
                if item.profile_status.upper() == "ADOPTED"
                else "Gate 2 unknown"
            )
            report.md(
                f"| `{_esc(item.profile_id or '-')}` | `{_esc(item.profile_status or '-')}` | "
                f"{_esc(gate_posture)} | `{_esc(item.integration_level or '-')}` | "
                f"`{_source(item.source_path, item.profile_status_line)}` |"
            )
            _add_fact(
                report,
                f"bridge_status.profile.{item.profile_id}.profile_status",
                item.profile_status,
                item.source_path,
                item.profile_status_line,
            )
            _add_fact(
                report,
                f"bridge_status.profile.{item.profile_id}.gate_posture",
                gate_posture,
                item.source_path,
                item.profile_status_line,
            )
        report.md("")
        if profile is not None and profile.live_binding_line:
            report.md(
                f"- live-binding line: {profile.live_binding_line} - "
                f"`{_source(profile.source_path, profile.live_binding_line_no)}`"
            )
            _add_fact(
                report,
                "bridge_status.live_binding_line",
                profile.live_binding_line,
                profile.source_path,
                profile.live_binding_line_no,
            )
        else:
            report.md("- live-binding line: not found in configured profile")

    report.md("")
    report.md(GATE_NOTE)
    report.md("")
    report.md("| Gate source | Observed state | Source |")
    report.md("|---|---|---|")
    if not gate_observations:
        report.md("| profile live-binding line | not parsed | - |")
    else:
        for gate in gate_observations:
            report.md(
                f"| {_esc(gate.gate)} | {_esc(gate.observed_state)} | "
                f"`{_source(gate.source_path, gate.line)}` |"
            )
    report.md("")

    report.md("## Brief lifecycle records")
    report.md("")
    report.md(BRIEF_NOTE)
    report.md("")
    if not briefs:
        report.md(NO_BRIEFS)
    else:
        report.md("| Brief | State | fence_active | committedness | Bound SHA | Source |")
        report.md("|---|---|---:|---|---|---|")
        for brief in briefs:
            sha = brief.bound_sha[:12] if brief.bound_sha else "-"
            report.md(
                f"| `{_esc(brief.tranche_id)}` | {_esc(brief.state)} | "
                f"{brief.fence_active} | {_esc(brief.committedness)} | "
                f"`{sha}` | `{brief.source_path}` |"
            )
            _add_fact(
                report,
                f"bridge_status.brief.{brief.tranche_id}",
                f"state={brief.state}; fence_active={brief.fence_active}",
                brief.source_path,
            )
    report.md("")

    report.md("## Owner-shaped act rows")
    report.md("")
    if not owner_acts:
        report.md(NO_OWNER_ACTS)
    else:
        report.md("| Source | Item | Posture | Owner-side act |")
        report.md("|---|---|---|---|")
        for act in owner_acts:
            report.md(
                f"| `{_esc(act.source)}` | {_esc(act.item)} | "
                f"{_esc(act.posture)} | {_esc(act.owner_side)} |"
            )
    report.md("")

    report.summary["parsed_register_rows"] = parsed_register_rows
    report.summary["open_register_rows"] = len(open_rows)
    report.summary["brief_records"] = len(briefs)
    report.summary["parked_lane_rows"] = len(parked_lanes)
    report.summary["parked_lane_receipt_only"] = sum(
        1 for lane in parked_lanes if lane.anchor_status == "receipt-only")
    report.summary["live_binding_gate_rows"] = len(gate_observations)
    report.summary["blocked_on_links"] = len(blocked_on)
    report.summary["owner_act_rows"] = len(owner_acts)
    if receipt is not None:
        report.summary["latest_receipt"] = receipt.title
    if refusal is not None:
        report.summary["identity_refusal"] = refusal
    return report
