#!/usr/bin/env python3
"""taskmgmt — deterministic Task Management register utilities.

Stage-A step-8 tool (adopted TM PRD §9; D-GOV-32; workplan step 8). Three
subcommands, all deterministic and judgment-free (PRD §9.3: promotion,
prioritization, disposition, closure, and escalation are human acts — this
tool validates form and harvests candidates, never makes the call):

  validate [--register PATH]   Schema and referential conformance of one
                               register CSV (default: the root program
                               register). Exit 0 PASS, 1 BLOCK, 2
                               operational (D-GOV-02 severity semantics).
  scan [--out PATH] [--register PATH]
                               Harvest candidates from the PRD §5.1
                               structured surfaces into a derived,
                               rebuildable candidate inventory (JSON).
                               The output is a gitignored projection
                               (D-GOV-01) and never authority. Exit 0 on
                               a completed scan (candidate count is data,
                               not a verdict), 2 operational.
  federation --register PATH [--out PATH]
                               Read-only federation survey of every tracked,
                               canonical register. Exit 0 COMPLETE, 1 PARTIAL,
                               2 operational.
  archive --register PATH [--dry-run]
                               Relocate rows already CLOSED by an owner-ruled
                               disposition from the live register into its
                               sibling REGISTER_CLOSED.csv archive. Mechanical
                               storage layout only: the tool never closes,
                               edits, reopens, or reorders a row, and refuses
                               to run when either file fails validation. Exit
                               0 on a completed (possibly zero-row) archive
                               pass, 1 refused on validation BLOCK, 2
                               operational.

Scanner precision rules implemented (PRD §9.2): structured surfaces by
filename/schema only — no free-text tree scanning; a declared exclusion
set reported in every output; canonical-vs-copy dedup preferring
`_Coordination/` originals over `_Evaluation/` copies, keyed within one
loop so same-named surfaces routed to different loops never fold together;
`TRACKED_OPEN` presented as open concern, never gating; no silent caps —
whatever the scan skips, it says it skipped.

Archive semantics: each canonical register may have a sibling
`REGISTER_CLOSED.csv` holding relocated CLOSED rows. Archived rows remain
part of the register's federated identity — ID resolution, duplicate
detection, closure comparison, staleness base, and scan dedup memory all
read live + archive — so archiving changes storage layout, never meaning.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

DEFAULT_REGISTER = Path("execution/_Coordination/_TaskManagement/REGISTER.csv")
DEFAULT_SCAN_OUT = Path(
    "execution/_Coordination/_TaskManagement/.candidates/scan.json"
)
ARCHIVE_NAME = "REGISTER_CLOSED.csv"

CANONICAL_COLUMNS = [
    "RegisterSchemaVersion", "ActionItemID", "Title", "Concern", "SourceRef",
    "SourceSha", "CandidateRef", "DomainLenses", "AssociatedWith", "NoticeRef",
    "ScaRef", "Assignment", "Priority", "PriorityBasis", "Status", "Trigger",
    "ElevatedTo", "Disposition", "EvidenceRef", "EvidenceSha", "EvidenceQuote",
    "Opened", "LastReviewed", "Closed", "Notes",
]
VALID_STATUS = ("OPEN", "DEFERRED", "ELEVATED", "CLOSED")
VALID_DISPOSITIONS = (
    "RESOLVED_WITH_CHANGE", "RESOLVED_BY_DECISION", "INFORMATIONAL_NO_ACTION",
    "DUPLICATE", "REJECTED", "SUPERSEDED_BY_SCOPE_CHANGE", "OBE",
)
ID_RE = re.compile(r"^TM-[A-Z0-9]+-\d{3,}$")
ID_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9-])(TM-[A-Z0-9]+-\d{3,})(?![A-Za-z0-9-])")
ID_PARTS_RE = re.compile(r"^TM-([A-Z0-9]+)-(\d{3,})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

FEDERATION_VERSION = "v1"
FEDERATION_AUTHORITY = "derived, rebuildable, gitignored, never authority"
FEDERATION_FINDING_CLASSES = (
    "INBOUND_ELEVATION", "FOREIGN_LINK_TO_LOCAL",
    "LOCAL_LINK_TO_FOREIGN", "OUTBOUND_AWAITING_ACK",
    "REMOTE_CLOSED_LOCAL_OPEN", "LOCAL_CLOSED_REMOTE_OPEN",
    "ORPHANED_LINK", "DUPLICATE_GLOBAL_ID", "MISSING_NOTICE",
    "AMBIGUOUS_REFERENCE", "INVALID_REGISTER", "UNREADABLE_REGISTER",
)
FEDERATION_EXCLUSIONS = (
    "untracked register lookalikes",
    "tracked register paths outside sanctioned coordination shapes",
    "archives, exports, fixtures, evaluation copies, and generated projections",
    "Notes prose and untyped free text",
    "foreign-register writes and automatic receiving rows",
    "promotion, prioritization, elevation, closure, and disposition effects",
)

_CANONICAL_REGISTER_RES = (
    re.compile(r"^execution/_Coordination/_TaskManagement/REGISTER\.csv$"),
    re.compile(
        r"^projects/[^/]+/execution/_Coordination/_TaskManagement/REGISTER\.csv$"),
    re.compile(
        r"^domains/[^/]+/execution/_Coordination/_TaskManagement/REGISTER\.csv$"),
    re.compile(r"^_DomainEngines/[^/]+/_TaskManagement/REGISTER\.csv$"),
)
_CANONICAL_ARCHIVE_RES = (
    re.compile(r"^execution/_Coordination/_TaskManagement/REGISTER_CLOSED\.csv$"),
    re.compile(
        r"^projects/[^/]+/execution/_Coordination/_TaskManagement/REGISTER_CLOSED\.csv$"),
    re.compile(
        r"^domains/[^/]+/execution/_Coordination/_TaskManagement/REGISTER_CLOSED\.csv$"),
    re.compile(r"^_DomainEngines/[^/]+/_TaskManagement/REGISTER_CLOSED\.csv$"),
)

# PRD §9.2 exclusion set — declared in configuration, reported in every output.
EXCLUDED_DIR_PARTS = (
    "dispatch_briefs", "dispatch_outputs", "gate5_coverage",
    "source_review_html", "atom_review_html", "source_section_nodes",
    "_Sources", ".archive", ".git", "node_modules",
)
EXCLUDED_PATH_SUBSTRINGS = (
    "_pdf2md_work", "docs/thesis/", "plans/chirality-task-management/",
)
# tools/** test fixtures are excluded wholesale by excluding tools/ from scan
# roots; the scanner never enumerates tools/.
SCAN_ROOTS = ("execution", "projects", "domains", "_DomainEngines")

# Structured-surface statuses treated as open at source.
OPEN_DECISION_STATUSES = ("AWAITING_RULING", "PROPOSED", "OPEN", "PENDING")
CLOSED_FINDING_STATUSES = ("CLOSED", "RESOLVED", "DONE", "RETIRED")


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    )
    return Path(out.stdout.strip())


def excluded(path: Path) -> bool:
    posix = path.as_posix()
    if any(part in EXCLUDED_DIR_PARTS for part in path.parts):
        return True
    return any(sub in posix for sub in EXCLUDED_PATH_SUBSTRINGS)


# ---------------------------------------------------------------- validate

def validate_register(root: Path, register: Path) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines)."""
    lines: list[str] = []
    reg_path = register if register.is_absolute() else root / register
    if not reg_path.is_file():
        return 2, [f"taskmgmt validate OPERATIONAL (exit 2): no register at "
                   f"{register}"]
    try:
        with open(reg_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            header = reader.fieldnames or []
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        return 2, [f"taskmgmt validate OPERATIONAL (exit 2): unreadable "
                   f"register: {exc}"]

    failures: list[str] = []
    if header != CANONICAL_COLUMNS:
        missing = [c for c in CANONICAL_COLUMNS if c not in header]
        extra = [c for c in header if c not in CANONICAL_COLUMNS]
        detail = []
        if missing:
            detail.append(f"missing {missing}")
        if extra:
            detail.append(f"unknown {extra}")
        if not detail:
            detail.append("column order differs from the schema-1.0 order")
        if header and header[0] != "RegisterSchemaVersion":
            detail.append("RegisterSchemaVersion is not column 1")
        failures.append("header: " + "; ".join(detail))

    seen_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):  # header is line 1
        rid = (row.get("ActionItemID") or "").strip()
        where = f"line {i} ({rid or 'no id'})"
        if not (row.get("RegisterSchemaVersion") or "").strip():
            failures.append(f"{where}: RegisterSchemaVersion empty")
        if not ID_RE.match(rid):
            failures.append(f"{where}: ActionItemID {rid!r} not TM-<LOOP>-<seq>")
        if rid in seen_ids:
            failures.append(f"{where}: duplicate ActionItemID {rid}")
        seen_ids.add(rid)
        status = (row.get("Status") or "").strip()
        if status not in VALID_STATUS:
            failures.append(f"{where}: Status {status!r} not in {VALID_STATUS}")
        disposition = (row.get("Disposition") or "").strip()
        if status == "CLOSED":
            if disposition not in VALID_DISPOSITIONS:
                failures.append(
                    f"{where}: CLOSED without a valid Disposition "
                    f"(got {disposition!r})")
            if not (row.get("EvidenceRef") or "").strip():
                failures.append(f"{where}: CLOSED without EvidenceRef")
            if not (row.get("EvidenceSha") or "").strip():
                failures.append(f"{where}: CLOSED without EvidenceSha")
            if not (row.get("Closed") or "").strip():
                failures.append(f"{where}: CLOSED without Closed date")
        elif disposition:
            failures.append(
                f"{where}: Disposition {disposition!r} on non-CLOSED row")
        if status == "DEFERRED" and not (row.get("Trigger") or "").strip():
            failures.append(f"{where}: DEFERRED without Trigger")
        if status == "ELEVATED" and not (row.get("ElevatedTo") or "").strip():
            failures.append(f"{where}: ELEVATED without ElevatedTo")
        if not (row.get("SourceRef") or "").strip():
            failures.append(f"{where}: SourceRef empty (K-PROV-1)")
        if not (row.get("SourceSha") or "").strip():
            failures.append(f"{where}: SourceSha empty (K-AUTH-2 posture)")
        for col in ("Opened", "LastReviewed", "Closed"):
            value = (row.get(col) or "").strip()
            if col == "Opened" and not value:
                failures.append(f"{where}: Opened empty")
            if value and not DATE_RE.match(value):
                failures.append(f"{where}: {col} {value!r} not YYYY-MM-DD")

    if failures:
        lines.append(f"taskmgmt validate BLOCK: {register} — "
                     f"{len(failures)} finding(s):")
        lines.extend(f"  - {f}" for f in failures)
        return 1, lines
    lines.append(
        f"taskmgmt validate PASS: {register} — {len(rows)} row(s), schema "
        "columns and referential rules conform. Form only; content judgment "
        "stays human (PRD §9.3).")
    return 0, lines


# -------------------------------------------------------------------- scan

def iter_files(root: Path, pattern: str):
    for scan_root in SCAN_ROOTS:
        base = root / scan_root
        if not base.is_dir():
            continue
        for path in sorted(base.rglob(pattern)):
            if not excluded(path.relative_to(root)):
                yield path


def candidate(source_class: str, path: Path, root: Path, ident: str,
              summary: str) -> dict:
    return {
        "class": source_class,
        "source": path.relative_to(root).as_posix(),
        "id": ident,
        "summary": " ".join(summary.split())[:240],
        "authority": "observed",  # candidates are observations, never authority
    }


def scan_decision_registers(root: Path) -> list[dict]:
    found = []
    for path in iter_files(root, "_REGISTER.md"):
        if "_DECISIONS" not in path.parts:
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            statuses = [c for c in cells if c in OPEN_DECISION_STATUSES]
            if statuses:
                found.append(candidate(
                    "decision-non-ruled", path, root, cells[0],
                    f"{statuses[0]}: {' / '.join(cells[1:2])}"))
    return found


def scan_notice_ledgers(root: Path) -> tuple[list[dict], list[dict]]:
    """Returns (tracked_open, notices_not_in_any_ledger)."""
    tracked, ledgered_names = [], set()
    for path in iter_files(root, "*NOTICE_STATUS*.csv"):
        try:
            rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        except (OSError, csv.Error):
            continue
        for row in rows:
            notice = (row.get("NoticePath") or "").strip()
            if notice:
                ledgered_names.add(PurePosixPath(notice).name)
            if (row.get("AcknowledgementState") or "").strip() == "TRACKED_OPEN":
                tracked.append(candidate(
                    "notice-tracked-open", path, root, notice,
                    "TRACKED_OPEN in ledger; presented as open concern, "
                    "never gating"))
    unregistered = []
    for path in iter_files(root, "NOTICE_*.md"):
        if "_Coordination" in path.parts and path.name not in ledgered_names:
            unregistered.append(candidate(
                "notice-not-in-ledger", path, root, path.name,
                "notice present on a coordination surface but absent from "
                "every notice ledger"))
    return tracked, unregistered


def scan_findings(root: Path) -> list[dict]:
    found = []
    for path in iter_files(root, "FINDINGS.csv"):
        if "_Evaluation" not in path.parts:
            continue
        try:
            rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        except (OSError, csv.Error):
            continue
        for row in rows:
            status = (row.get("Status") or row.get("Disposition") or "").strip()
            if status and status.upper() not in CLOSED_FINDING_STATUSES:
                found.append(candidate(
                    "evaluation-finding-open", path, root,
                    (row.get("FindingID") or "row").strip(),
                    f"{status}: {(row.get('Concern') or '')}"))
    return found


def scan_packet_fields(root: Path) -> list[dict]:
    found = []
    for pattern, id_cols in (
        ("Open_Questions.csv", ("OpenQuestionID", "QuestionID")),
        ("Conflicts.csv", ("ConflictID", "ID")),
        ("Amendment_Candidates.csv", ("AmendmentID", "CandidateID", "ID")),
    ):
        for path in iter_files(root, pattern):
            try:
                rows = list(csv.DictReader(open(path, newline="",
                                                encoding="utf-8")))
            except (OSError, csv.Error):
                continue
            for row in rows:
                status = (row.get("Status") or "").strip().upper()
                ruling = (row.get("HumanRuling") or
                          row.get("HumanDisposition") or "").strip().upper()
                # TBD only in disposition-bearing columns (PRD §5.1); Status
                # open values for question schemas.
                is_open = ruling == "TBD" or (
                    pattern == "Open_Questions.csv"
                    and status in ("OPEN", "PARTIAL", ""))
                if is_open:
                    ident = next((row[c] for c in id_cols if row.get(c)), "row")
                    found.append(candidate(
                        "packet-field-open", path, root, ident,
                        (row.get("Question") or row.get("Description") or
                         row.get("Conflict") or "")))
    return found


def scan_tbd_registers(root: Path) -> list[dict]:
    found = []
    for path in iter_files(root, "*TBD_Register*.csv"):
        try:
            rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        except (OSError, csv.Error):
            continue
        for row in rows:
            found.append(candidate(
                "tbd-register-row", path, root,
                (row.get("TBDID") or "row").strip(),
                (row.get("Question") or "")))
    return found


def scan_handoff_blockers(root: Path) -> list[dict]:
    found = []
    for path in iter_files(root, "HANDOFF_STATE.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            lowered = line.lower()
            if "remaining blockers" in lowered and "none" not in lowered:
                found.append(candidate(
                    "handoff-blocker", path, root, "remaining-blockers",
                    line.strip()))
    return found


def loop_of_source(source: str) -> str:
    """Loop identity of a repo-relative source path.

    `projects/<x>/...`, `domains/<x>/...`, and `_DomainEngines/<x>/...` belong
    to that loop; everything else (`execution/...`) is the root loop.
    """
    parts = PurePosixPath(source).parts
    if len(parts) > 1 and parts[0] in ("projects", "domains", "_DomainEngines"):
        return f"{parts[0]}/{parts[1]}"
    return "ROOT"


def dedup_canonical(cands: list[dict]) -> tuple[list[dict], int]:
    """Canonical-vs-copy: prefer _Coordination/ paths over _Evaluation/ copies
    sharing (loop, source basename, class, id).

    Loop identity is part of the key so same-named surfaces routed to
    different loops (e.g., one NOTICE_*.md delivered to several coordination
    surfaces) are never folded into one candidate; only true intra-loop
    copies are."""
    by_key: dict[tuple, dict] = {}
    dropped = 0
    for cand in cands:
        key = (loop_of_source(cand["source"]),
               PurePosixPath(cand["source"]).name, cand["class"], cand["id"])
        kept = by_key.get(key)
        if kept is None:
            by_key[key] = cand
            continue
        dropped += 1
        if ("/_Coordination/" in "/" + cand["source"]
                and "/_Coordination/" not in "/" + kept["source"]):
            by_key[key] = cand
    return list(by_key.values()), dropped


def load_register_refs(root: Path, register: Path) -> set[str]:
    reg_path = register if register.is_absolute() else root / register
    refs: set[str] = set()
    # Archived CLOSED rows stay part of the register's dedup memory.
    for path in (reg_path, reg_path.parent / ARCHIVE_NAME):
        if not path.is_file():
            continue
        try:
            for row in csv.DictReader(open(path, newline="", encoding="utf-8")):
                refs.add((row.get("SourceRef") or "").strip())
        except (OSError, csv.Error):
            pass
    return refs


def scan(root: Path, register: Path, out: Path) -> tuple[int, list[str]]:
    tracked, unregistered = scan_notice_ledgers(root)
    classes = {
        "decision-non-ruled": scan_decision_registers(root),
        "notice-tracked-open": tracked,
        "notice-not-in-ledger": unregistered,
        "evaluation-finding-open": scan_findings(root),
        "packet-field-open": scan_packet_fields(root),
        "tbd-register-row": scan_tbd_registers(root),
        "handoff-blocker": scan_handoff_blockers(root),
    }
    all_cands = [c for group in classes.values() for c in group]
    deduped, dropped = dedup_canonical(all_cands)

    register_refs = load_register_refs(root, register)
    for cand in deduped:
        cand["known_to_register"] = any(
            cand["source"] in ref for ref in register_refs)

    payload = {
        "generated_by": "tools/taskmgmt/taskmgmt.py scan (v0)",
        "authority": "derived, rebuildable, gitignored projection (D-GOV-01); "
                     "never citable as authority; candidates are observations "
                     "and create no duty anywhere (K-TM-3/K-TM-4)",
        "scan_roots": list(SCAN_ROOTS),
        "exclusions_declared": {
            "dir_parts": list(EXCLUDED_DIR_PARTS),
            "path_substrings": list(EXCLUDED_PATH_SUBSTRINGS),
            "note": "tools/ is never enumerated; free-text token scanning "
                    "is out of scope for v0 (per-document mode only, "
                    "not implemented)",
        },
        "dedup_dropped_copies": dropped,
        "counts": {name: len(group) for name, group in classes.items()},
        "candidates": sorted(
            deduped, key=lambda c: (c["class"], c["source"], str(c["id"]))),
    }
    out_path = out if out.is_absolute() else root / out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"taskmgmt scan COMPLETE: {len(deduped)} candidate(s) "
        f"({dropped} canonical-copy duplicate(s) folded) -> "
        f"{out_path.relative_to(root).as_posix() if not out.is_absolute() else out_path}",
    ]
    for name, group in classes.items():
        lines.append(f"  {name}: {len(group)}")
    known = sum(1 for c in deduped if c.get("known_to_register"))
    lines.append(f"  known_to_register (SourceRef overlap): {known}")
    lines.append("  exclusions declared in output; no silent caps — classes "
                 "not implemented in v0 (run-record markers, review-report "
                 "sections, per-document token mode) are skipped and named "
                 "here.")
    return 0, lines


# ---------------------------------------------------------------- archive

def status_counts(rows: list[dict]) -> dict[str, int]:
    counts = {status: 0 for status in VALID_STATUS}
    for row in rows:
        status = (row.get("Status") or "").strip()
        if status in counts:
            counts[status] += 1
    return counts


def _status_counts_line(rows: list[dict]) -> str:
    counts = status_counts(rows)
    return " ".join(f"{status}={counts[status]}" for status in VALID_STATUS)


def _write_rows(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=CANONICAL_COLUMNS, quoting=csv.QUOTE_ALL,
            lineterminator="\n", extrasaction="ignore", restval="")
        writer.writeheader()
        writer.writerows(rows)


def archive_register(root: Path, register: Path,
                     dry_run: bool = False) -> tuple[int, list[str]]:
    """Relocate CLOSED rows into the sibling REGISTER_CLOSED.csv archive.

    Deterministic and judgment-free (PRD §9.3): a row moves only if it is
    already CLOSED by an owner-ruled disposition recorded in the register.
    The tool never closes, edits, reopens, or reorders rows, and fails
    closed when the live register or the existing archive does not validate.
    """
    display = register.as_posix()
    reg_path = register if register.is_absolute() else root / register
    if not reg_path.is_file():
        return 2, [f"taskmgmt archive OPERATIONAL (exit 2): no register at "
                   f"{display}"]

    code, val_lines = validate_register(root, register)
    if code != 0:
        return code, [f"taskmgmt archive REFUSED: live register {display} "
                      "does not validate; nothing moved:"] + val_lines

    _, live_rows = _read_register(reg_path)
    archive_reg = register.parent / ARCHIVE_NAME
    arch_path = reg_path.parent / ARCHIVE_NAME
    archived_rows: list[dict] = []
    if arch_path.is_file():
        arch_code, arch_lines = validate_register(root, archive_reg)
        if arch_code != 0:
            return (arch_code if arch_code in (1, 2) else 2), [
                f"taskmgmt archive REFUSED: existing archive "
                f"{archive_reg.as_posix()} does not validate; nothing moved:",
            ] + arch_lines
        _, archived_rows = _read_register(arch_path)
        not_closed = [
            (row.get("ActionItemID") or "?").strip() for row in archived_rows
            if (row.get("Status") or "").strip() != "CLOSED"
        ]
        if not_closed:
            return 1, [
                f"taskmgmt archive REFUSED: archive {archive_reg.as_posix()} "
                f"contains non-CLOSED row(s) {not_closed}; an archive may "
                "hold only owner-closed rows; nothing moved",
            ]
        overlap = ({(row.get("ActionItemID") or "").strip()
                    for row in archived_rows}
                   & {(row.get("ActionItemID") or "").strip()
                      for row in live_rows})
        if overlap:
            return 1, [
                "taskmgmt archive REFUSED: ActionItemID(s) present in both "
                f"live register and archive: {sorted(overlap)}; resolve the "
                "duplicate identity first; nothing moved",
            ]

    to_move = [row for row in live_rows
               if (row.get("Status") or "").strip() == "CLOSED"]
    remaining = [row for row in live_rows
                 if (row.get("Status") or "").strip() != "CLOSED"]

    action = "would move" if dry_run else "moved"
    lines = [
        f"taskmgmt archive {'DRY-RUN' if dry_run else 'COMPLETE'}: "
        f"{len(to_move)} CLOSED row(s) {action} "
        f"{display} -> {archive_reg.as_posix()}",
        f"  live after: {_status_counts_line(remaining)} "
        f"({len(remaining)} row(s)); archive total: "
        f"{len(archived_rows) + len(to_move)}",
        "  mechanical relocation only; closure itself remains the owner's "
        "recorded act (K-TM-3), and archived rows stay part of the "
        "register's federated identity",
    ]
    if dry_run or not to_move:
        return 0, lines
    _write_rows(arch_path, archived_rows + to_move)
    _write_rows(reg_path, remaining)
    return 0, lines


# ------------------------------------------------------------- federation

def _repo_relative(root: Path, path: Path) -> str:
    resolved = path if path.is_absolute() else root / path
    return resolved.resolve().relative_to(root.resolve()).as_posix()


def _is_canonical_register(path: str) -> bool:
    return any(pattern.fullmatch(path) for pattern in _CANONICAL_REGISTER_RES)


def _is_register_lookalike(path: str) -> bool:
    return path == "_TaskManagement/REGISTER.csv" or path.endswith(
        "/_TaskManagement/REGISTER.csv")


def _is_canonical_archive(path: str) -> bool:
    return any(pattern.fullmatch(path) for pattern in _CANONICAL_ARCHIVE_RES)


def _is_archive_lookalike(path: str) -> bool:
    return path == f"_TaskManagement/{ARCHIVE_NAME}" or path.endswith(
        f"/_TaskManagement/{ARCHIVE_NAME}")


def classify_register_paths(tracked: list[str], untracked: list[str]) -> tuple[list[str], list[dict]]:
    """Classify Git-reported paths without consulting filesystem existence."""
    canonical = sorted({p for p in tracked if _is_canonical_register(p)})
    exclusions = [
        {"path": p, "reason": "tracked path is outside sanctioned register shapes"}
        for p in sorted(set(tracked))
        if _is_register_lookalike(p) and not _is_canonical_register(p)
    ]
    exclusions.extend(
        {"path": p, "reason": "untracked register lookalike"}
        for p in sorted(set(untracked))
        if _is_register_lookalike(p)
    )
    return canonical, exclusions


def _git_paths(root: Path, *args: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", *args],
        capture_output=True, check=True,
    )
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in completed.stdout.split(b"\0") if item
    ]


def discover_registers(root: Path) -> tuple[list[str], list[dict]]:
    """Return canonical tracked registers and explicitly excluded lookalikes."""
    tracked = _git_paths(root)
    untracked = _git_paths(root, "--others", "--exclude-standard")
    return classify_register_paths(tracked, untracked)


def classify_archive_paths(tracked: list[str], untracked: list[str]) -> tuple[list[str], list[dict]]:
    """Classify archive paths; canonical archives sit beside canonical registers."""
    canonical = sorted({p for p in tracked if _is_canonical_archive(p)})
    exclusions = [
        {"path": p,
         "reason": "tracked archive path is outside sanctioned register shapes"}
        for p in sorted(set(tracked))
        if _is_archive_lookalike(p) and not _is_canonical_archive(p)
    ]
    exclusions.extend(
        {"path": p,
         "reason": "untracked archive lookalike outside sanctioned register shapes"}
        for p in sorted(set(untracked))
        if _is_archive_lookalike(p) and not _is_canonical_archive(p)
    )
    return canonical, exclusions


def discover_archives(root: Path) -> tuple[list[str], list[dict]]:
    """Return canonical tracked archives and explicitly excluded lookalikes."""
    tracked = _git_paths(root)
    untracked = _git_paths(root, "--others", "--exclude-standard")
    return classify_archive_paths(tracked, untracked)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_register(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames or [], list(reader)


def _path_fallback_namespace(register_path: str) -> str:
    parts = PurePosixPath(register_path).parts
    if register_path == DEFAULT_REGISTER.as_posix():
        return "ROOT"
    if parts[0] in ("projects", "domains", "_DomainEngines"):
        label = parts[1]
    else:  # Defensive only; discovery admits no other shape.
        label = PurePosixPath(register_path).parent.parent.name
    return re.sub(r"[^A-Z0-9]+", "_", label.upper()).strip("_") or "UNKNOWN"


def _infer_namespace(register_path: str, rows: list[dict]) -> tuple[str | None, str]:
    if register_path == DEFAULT_REGISTER.as_posix():
        return "ROOT", "ACTION_ITEM_IDS"
    namespaces = {
        match.group(1)
        for row in rows
        if (match := ID_PARTS_RE.fullmatch((row.get("ActionItemID") or "").strip()))
    }
    if len(namespaces) == 1:
        return next(iter(namespaces)), "ACTION_ITEM_IDS"
    if not rows:
        return _path_fallback_namespace(register_path), "PATH_FALLBACK_HEADER_ONLY"
    return None, "AMBIGUOUS_MIXED_ACTION_ITEM_IDS"


def _working_root(root: Path, register_path: str) -> Path:
    parts = PurePosixPath(register_path).parts
    if register_path == DEFAULT_REGISTER.as_posix():
        return root
    if parts[0] in ("projects", "domains", "_DomainEngines"):
        return root.joinpath(*parts[:2])
    return root


def _finding(finding_class: str, invoking_register: str, *,
             local_id: str = "", remote_id: str = "",
             register_paths: list[str] | None = None, field: str = "",
             evidence: str = "") -> dict:
    if finding_class not in FEDERATION_FINDING_CLASSES:
        raise ValueError(f"unknown federation finding class: {finding_class}")
    return {
        "class": finding_class,
        "invoking_register": invoking_register,
        "local_id": local_id,
        "remote_id": remote_id,
        "register_paths": sorted(set(register_paths or [])),
        "field": field,
        "evidence": evidence,
    }


def _finding_sort_key(item: dict) -> tuple:
    return (
        FEDERATION_FINDING_CLASSES.index(item["class"]),
        item["local_id"], item["remote_id"], tuple(item["register_paths"]),
        item["field"], item["evidence"],
    )


def _strip_notice_wrapper(value: str) -> str:
    value = value.strip()
    for wrapper in ('"', "'", "`"):
        if len(value) >= 2 and value.startswith(wrapper) and value.endswith(wrapper):
            return value[1:-1].strip()
    return value


def _notice_matches(root: Path, register_path: str, reference: str) -> list[str]:
    ref_path = Path(reference)
    candidates = [ref_path] if ref_path.is_absolute() else [
        _working_root(root, register_path) / ref_path,
        root / ref_path,
    ]
    matches: set[str] = set()
    for candidate_path in candidates:
        try:
            if candidate_path.is_file():
                try:
                    matches.add(candidate_path.resolve().relative_to(root.resolve()).as_posix())
                except ValueError:
                    matches.add(candidate_path.resolve().as_posix())
        except OSError:
            continue
    return sorted(matches)


def _public_register(entry: dict) -> dict:
    return {
        "path": entry["path"],
        "namespace": entry["namespace"],
        "namespace_basis": entry["namespace_basis"],
        "schema_version": entry["schema_version"],
        "row_count": entry["row_count"],
        "status_counts": entry["status_counts"],
        "validation": entry["validation"],
        "validation_details": entry["validation_details"],
        "before_sha256": entry["before_sha256"],
        "after_sha256": entry["after_sha256"],
        "archive_path": entry["archive_path"],
        "archive_tracked": entry["archive_tracked"],
        "archive_row_count": entry["archive_row_count"],
        "archive_validation": entry["archive_validation"],
        "archive_before_sha256": entry["archive_before_sha256"],
        "archive_after_sha256": entry["archive_after_sha256"],
    }


def _write_federation_payload(out_path: Path, payload: dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _output_register_collision(root: Path, out_path: Path,
                               canonical_paths: list[str]) -> str | None:
    """Fail closed when a projection target aliases any register surface."""
    resolved_out = out_path.resolve(strict=False)
    for rel_path in canonical_paths:
        register_path = (root / rel_path).resolve(strict=False)
        if resolved_out == register_path:
            return rel_path
        try:
            if out_path.exists() and register_path.exists() and out_path.samefile(
                    register_path):
                return rel_path
        except OSError:
            pass
    try:
        resolved_relative = resolved_out.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    if (_is_register_lookalike(resolved_relative)
            or _is_archive_lookalike(resolved_relative)):
        return resolved_relative
    return None


def federation(root: Path, register: Path, out: Path | None = None) -> tuple[int, list[str]]:
    """Perform the invocation-local, read-only cross-register survey."""
    root = root.resolve()
    try:
        invoking_register = _repo_relative(root, register)
    except (OSError, ValueError) as exc:
        return 2, [f"taskmgmt federation OPERATIONAL (exit 2): invoking register "
                   f"is outside the repository: {exc}"]

    out_path = (
        (out if out.is_absolute() else root / out) if out is not None
        else root / PurePosixPath(invoking_register).parent / ".candidates" /
        "federation.json"
    )
    display_out = (out_path.relative_to(root).as_posix()
                   if out_path.is_relative_to(root) else out_path.as_posix())
    command = ["federation", "--register", invoking_register, "--out", display_out]
    operational_errors: list[dict] = []
    exclusions: list[dict] = []
    entries: list[dict] = []
    findings: list[dict] = []

    try:
        canonical_paths, exclusions = discover_registers(root)
    except (OSError, subprocess.CalledProcessError) as exc:
        canonical_paths = []
        operational_errors.append({"stage": "discovery", "error": str(exc)})

    try:
        canonical_archives, archive_exclusions = discover_archives(root)
    except (OSError, subprocess.CalledProcessError) as exc:
        canonical_archives, archive_exclusions = [], []
        operational_errors.append(
            {"stage": "discovery-archives", "error": str(exc)})
    exclusions = exclusions + archive_exclusions

    collision = _output_register_collision(
        root, out_path, canonical_paths + canonical_archives)
    if collision is not None:
        return 2, [
            "taskmgmt federation OPERATIONAL (exit 2): output path resolves "
            f"to a register surface ({collision}); no output written",
        ]

    if invoking_register not in canonical_paths:
        operational_errors.append({
            "stage": "invocation",
            "error": f"invoking register is not a tracked canonical register: {invoking_register}",
        })

    for rel_path in canonical_paths:
        abs_path = root / rel_path
        entry = {
            "path": rel_path, "namespace": None, "namespace_basis": "UNAVAILABLE",
            "schema_version": None, "row_count": None,
            "status_counts": None,
            "validation": "UNREADABLE", "validation_details": [],
            "before_sha256": None, "after_sha256": None, "_rows": [],
            "archive_path": None, "archive_tracked": False,
            "archive_row_count": None, "archive_validation": None,
            "archive_before_sha256": None, "archive_after_sha256": None,
        }
        try:
            entry["before_sha256"] = _sha256(abs_path)
            header, rows = _read_register(abs_path)
            entry["_rows"] = rows
            entry["row_count"] = len(rows)
            entry["status_counts"] = status_counts(rows)
            versions = sorted({
                (row.get("RegisterSchemaVersion") or "").strip()
                for row in rows if (row.get("RegisterSchemaVersion") or "").strip()
            })
            entry["schema_version"] = (
                versions[0] if len(versions) == 1 else
                "MIXED" if versions else
                ("HEADER_ONLY" if header == CANONICAL_COLUMNS else None)
            )
        except (OSError, UnicodeError, csv.Error) as exc:
            message = f"{type(exc).__name__}: {exc}"
            entry["validation_details"] = [message]
            operational_errors.append({
                "stage": "read", "register": rel_path, "error": message,
            })
            findings.append(_finding(
                "UNREADABLE_REGISTER", invoking_register,
                register_paths=[rel_path], evidence=message))
            entries.append(entry)
            continue

        validation_code, validation_lines = validate_register(root, Path(rel_path))
        entry["validation_details"] = validation_lines
        if validation_code == 2:
            entry["validation"] = "UNREADABLE"
            operational_errors.append({
                "stage": "validation-read", "register": rel_path,
                "error": "validator could not read register",
            })
            findings.append(_finding(
                "UNREADABLE_REGISTER", invoking_register,
                register_paths=[rel_path], evidence="; ".join(validation_lines)))
        elif validation_code == 1:
            entry["validation"] = "BLOCK"
            findings.append(_finding(
                "INVALID_REGISTER", invoking_register,
                register_paths=[rel_path], evidence="; ".join(validation_lines)))
        else:
            entry["validation"] = "PASS"
            archive_rel = (
                PurePosixPath(rel_path).parent / ARCHIVE_NAME).as_posix()
            archive_abs = root / archive_rel
            if archive_abs.is_file():
                entry["archive_path"] = archive_rel
                entry["archive_tracked"] = archive_rel in canonical_archives
                try:
                    entry["archive_before_sha256"] = _sha256(archive_abs)
                    arch_code, arch_lines = validate_register(
                        root, Path(archive_rel))
                    _, arch_rows = _read_register(archive_abs)
                    entry["archive_row_count"] = len(arch_rows)
                    not_closed = [
                        (r.get("ActionItemID") or "?").strip()
                        for r in arch_rows
                        if (r.get("Status") or "").strip() != "CLOSED"
                    ]
                    if arch_code == 2:
                        entry["archive_validation"] = "UNREADABLE"
                        operational_errors.append({
                            "stage": "archive-validation-read",
                            "register": archive_rel,
                            "error": "validator could not read archive",
                        })
                        findings.append(_finding(
                            "UNREADABLE_REGISTER", invoking_register,
                            register_paths=[archive_rel],
                            evidence="; ".join(arch_lines)))
                    elif arch_code == 1 or not_closed:
                        entry["archive_validation"] = "BLOCK"
                        evidence = "; ".join(arch_lines) if arch_code == 1 else (
                            f"archive contains non-CLOSED row(s) {not_closed}; "
                            "an archive may hold only owner-closed rows")
                        findings.append(_finding(
                            "INVALID_REGISTER", invoking_register,
                            register_paths=[archive_rel], evidence=evidence))
                    else:
                        entry["archive_validation"] = "PASS"
                        # Archived rows stay part of the register's federated
                        # identity: ID index, links, closure comparison.
                        entry["_rows"] = entry["_rows"] + arch_rows
                except (OSError, UnicodeError, csv.Error) as exc:
                    message = f"{type(exc).__name__}: {exc}"
                    entry["archive_validation"] = "UNREADABLE"
                    operational_errors.append({
                        "stage": "archive-read", "register": archive_rel,
                        "error": message,
                    })
                    findings.append(_finding(
                        "UNREADABLE_REGISTER", invoking_register,
                        register_paths=[archive_rel], evidence=message))
            namespace, basis = _infer_namespace(rel_path, entry["_rows"])
            entry["namespace"] = namespace
            entry["namespace_basis"] = basis
            if namespace is None:
                findings.append(_finding(
                    "AMBIGUOUS_REFERENCE", invoking_register,
                    register_paths=[rel_path], field="ActionItemID",
                    evidence="mixed ActionItemID namespaces prevent register identity inference"))
        entries.append(entry)

    invoking_entry = next(
        (entry for entry in entries if entry["path"] == invoking_register), None)
    invoking_namespace = invoking_entry["namespace"] if invoking_entry else None

    valid_entries = [entry for entry in entries if entry["validation"] == "PASS"]
    global_index: dict[str, list[tuple[dict, dict]]] = {}
    namespace_entries: dict[str, list[dict]] = {}
    for entry in valid_entries:
        if entry["namespace"] is not None:
            namespace_entries.setdefault(entry["namespace"], []).append(entry)
        for row in entry["_rows"]:
            row_id = (row.get("ActionItemID") or "").strip()
            global_index.setdefault(row_id, []).append((entry, row))

    for item_id, locations in sorted(global_index.items()):
        if len(locations) > 1:
            findings.append(_finding(
                "DUPLICATE_GLOBAL_ID", invoking_register,
                local_id=item_id,
                register_paths=[entry["path"] for entry, _ in locations],
                field="ActionItemID", evidence=item_id))

    resolved_links: list[dict] = []
    for source_entry in valid_entries:
        for source_row in source_entry["_rows"]:
            source_id = (source_row.get("ActionItemID") or "").strip()
            references: list[tuple[str, str]] = []
            source_value = (source_row.get("SourceRef") or "").strip()
            references.extend(("SourceRef", token)
                              for token in sorted(set(ID_TOKEN_RE.findall(source_value))))
            elevated_value = (source_row.get("ElevatedTo") or "").strip()
            if ID_RE.fullmatch(elevated_value):
                references.append(("ElevatedTo", elevated_value))

            for field, target_id in references:
                target_namespace_match = ID_PARTS_RE.fullmatch(target_id)
                target_namespace = (target_namespace_match.group(1)
                                    if target_namespace_match else None)
                targets = global_index.get(target_id, [])
                target_namespace_entries = namespace_entries.get(
                    target_namespace or "", [])
                if (field == "ElevatedTo" and len(target_namespace_entries) == 1
                        and source_entry["path"] != invoking_register
                        and target_namespace == invoking_namespace
                        and target_namespace_entries[0]["path"] ==
                        invoking_register):
                    inbound_entry = target_namespace_entries[0]
                    findings.append(_finding(
                        "INBOUND_ELEVATION", invoking_register,
                        local_id=target_id, remote_id=source_id,
                        register_paths=[source_entry["path"], inbound_entry["path"]],
                        field=field, evidence=elevated_value))
                if not targets:
                    findings.append(_finding(
                        "ORPHANED_LINK", invoking_register,
                        local_id=source_id, remote_id=target_id,
                        register_paths=[source_entry["path"]], field=field,
                        evidence=(source_row.get(field) or "").strip()))
                    is_cross_namespace = target_namespace != source_entry["namespace"]
                    if (source_entry["path"] == invoking_register and (
                            (field == "SourceRef" and is_cross_namespace) or
                            (field == "ElevatedTo" and
                             (source_row.get("Status") or "").strip() == "ELEVATED"))):
                        findings.append(_finding(
                            "OUTBOUND_AWAITING_ACK", invoking_register,
                            local_id=source_id, remote_id=target_id,
                            register_paths=[source_entry["path"]], field=field,
                            evidence=(source_row.get(field) or "").strip()))
                    continue
                if len(targets) > 1:
                    findings.append(_finding(
                        "AMBIGUOUS_REFERENCE", invoking_register,
                        local_id=source_id, remote_id=target_id,
                        register_paths=[source_entry["path"]] +
                                       [entry["path"] for entry, _ in targets],
                        field=field,
                        evidence="target ActionItemID occurs in multiple registers"))
                    continue
                target_entry, target_row = targets[0]
                if target_entry["path"] == source_entry["path"]:
                    continue
                resolved_links.append({
                    "source_entry": source_entry, "source_row": source_row,
                    "target_entry": target_entry, "target_row": target_row,
                    "field": field,
                })
                if (target_entry["path"] == invoking_register
                        and source_entry["path"] != invoking_register):
                    findings.append(_finding(
                        "FOREIGN_LINK_TO_LOCAL", invoking_register,
                        local_id=target_id, remote_id=source_id,
                        register_paths=[source_entry["path"], target_entry["path"]],
                        field=field, evidence=(source_row.get(field) or "").strip()))
                elif (source_entry["path"] == invoking_register
                      and target_entry["path"] != invoking_register):
                    findings.append(_finding(
                        "LOCAL_LINK_TO_FOREIGN", invoking_register,
                        local_id=source_id, remote_id=target_id,
                        register_paths=[source_entry["path"], target_entry["path"]],
                        field=field, evidence=(source_row.get(field) or "").strip()))

            notice_value = (source_row.get("NoticeRef") or "").strip()
            if notice_value and notice_value.upper() != "NONE":
                for raw_ref in notice_value.split(";"):
                    notice_ref = _strip_notice_wrapper(raw_ref)
                    if not notice_ref or notice_ref.upper() == "NONE":
                        continue
                    matches = _notice_matches(root, source_entry["path"], notice_ref)
                    if not matches:
                        findings.append(_finding(
                            "MISSING_NOTICE", invoking_register,
                            local_id=source_id,
                            register_paths=[source_entry["path"]],
                            field="NoticeRef", evidence=notice_ref))
                    elif len(matches) > 1:
                        findings.append(_finding(
                            "AMBIGUOUS_REFERENCE", invoking_register,
                            local_id=source_id,
                            register_paths=[source_entry["path"]] + matches,
                            field="NoticeRef", evidence=notice_ref))

    closure_pairs: set[tuple] = set()
    for link in sorted(resolved_links, key=lambda item: (
            item["source_entry"]["path"],
            (item["source_row"].get("ActionItemID") or ""),
            item["target_entry"]["path"],
            (item["target_row"].get("ActionItemID") or ""), item["field"])):
        source_key = (link["source_entry"]["path"],
                      (link["source_row"].get("ActionItemID") or "").strip())
        target_key = (link["target_entry"]["path"],
                      (link["target_row"].get("ActionItemID") or "").strip())
        pair_key = tuple(sorted((source_key, target_key)))
        if pair_key in closure_pairs:
            continue
        closure_pairs.add(pair_key)
        if source_key[0] == invoking_register:
            local_entry, local_row = link["source_entry"], link["source_row"]
            remote_entry, remote_row = link["target_entry"], link["target_row"]
        elif target_key[0] == invoking_register:
            local_entry, local_row = link["target_entry"], link["target_row"]
            remote_entry, remote_row = link["source_entry"], link["source_row"]
        elif source_key <= target_key:
            local_entry, local_row = link["source_entry"], link["source_row"]
            remote_entry, remote_row = link["target_entry"], link["target_row"]
        else:
            local_entry, local_row = link["target_entry"], link["target_row"]
            remote_entry, remote_row = link["source_entry"], link["source_row"]
        local_closed = (local_row.get("Status") or "").strip() == "CLOSED"
        remote_closed = (remote_row.get("Status") or "").strip() == "CLOSED"
        if local_closed == remote_closed:
            continue
        finding_class = ("LOCAL_CLOSED_REMOTE_OPEN" if local_closed
                         else "REMOTE_CLOSED_LOCAL_OPEN")
        findings.append(_finding(
            finding_class, invoking_register,
            local_id=(local_row.get("ActionItemID") or "").strip(),
            remote_id=(remote_row.get("ActionItemID") or "").strip(),
            register_paths=[local_entry["path"], remote_entry["path"]],
            field=link["field"],
            evidence="linked rows have divergent CLOSED status"))

    changed_hashes = 0
    for entry in entries:
        surfaces = [("path", "before_sha256", "after_sha256")]
        if entry["archive_before_sha256"] is not None:
            surfaces.append(
                ("archive_path", "archive_before_sha256", "archive_after_sha256"))
        for path_key, before_key, after_key in surfaces:
            if entry[before_key] is None:
                continue
            try:
                entry[after_key] = _sha256(root / entry[path_key])
            except OSError as exc:
                operational_errors.append({
                    "stage": "post-survey-hash", "register": entry[path_key],
                    "error": f"{type(exc).__name__}: {exc}",
                })
                continue
            if entry[before_key] != entry[after_key]:
                changed_hashes += 1
                operational_errors.append({
                    "stage": "zero-write-proof", "register": entry[path_key],
                    "error": "register SHA-256 changed during survey",
                })

    coverage_partial = any(
        entry["validation"] != "PASS" or entry["namespace"] is None
        or entry["archive_validation"] not in (None, "PASS")
        for entry in entries
    ) or not canonical_paths
    coverage = "PARTIAL" if coverage_partial else "COMPLETE"
    findings = sorted(findings, key=_finding_sort_key)
    program_classes = {
        "DUPLICATE_GLOBAL_ID", "INVALID_REGISTER", "UNREADABLE_REGISTER",
        "AMBIGUOUS_REFERENCE",
    }
    if invoking_namespace == "ROOT":
        presented = findings
    else:
        presented = [
            item for item in findings
            if item["class"] in program_classes
            or invoking_register in item["register_paths"]
        ]

    payload = {
        "tool": "tools/taskmgmt/taskmgmt.py federation",
        "version": FEDERATION_VERSION,
        "command": command,
        "authority": FEDERATION_AUTHORITY,
        "invocation": {
            "loop": invoking_namespace,
            "register": invoking_register,
        },
        "coverage": coverage,
        "registers": [_public_register(entry) for entry in entries],
        "findings": findings,
        "presented_findings": presented,
        "finding_counts": {
            name: sum(1 for item in findings if item["class"] == name)
            for name in FEDERATION_FINDING_CLASSES
        },
        "exclusions_declared": list(FEDERATION_EXCLUSIONS),
        "excluded_paths": exclusions,
        "unresolved_ambiguities": [
            item for item in findings if item["class"] == "AMBIGUOUS_REFERENCE"
        ],
        "operational_errors": operational_errors,
        "zero_write_proof": {
            "register_writes": changed_hashes,
            "statement": (
                "zero register writes occurred; every readable register hash matched"
                if changed_hashes == 0 and all(
                    entry[before] == entry[after]
                    for entry in entries
                    for before, after in (
                        ("before_sha256", "after_sha256"),
                        ("archive_before_sha256", "archive_after_sha256"))
                    if entry[before] is not None)
                else "zero register writes not proven"
            ),
        },
    }

    try:
        _write_federation_payload(out_path, payload)
    except OSError as exc:
        return 2, [
            f"taskmgmt federation OPERATIONAL (exit 2): output failed: {exc}",
            f"  coverage before output failure: {coverage}",
        ]

    exit_code = 2 if operational_errors else (1 if coverage == "PARTIAL" else 0)
    outcome = "OPERATIONAL" if exit_code == 2 else coverage
    lines = [
        f"taskmgmt federation {outcome}: {len(entries)} register(s), "
        f"{len(findings)} finding(s), {len(presented)} presented -> {display_out}",
        f"  coverage: {coverage}; register_writes: {changed_hashes}",
    ]
    for entry in entries:
        if entry["status_counts"] is None:
            continue
        label = entry["namespace"] or entry["path"]
        counts = entry["status_counts"]
        live = " ".join(f"{status}={counts[status]}" for status in VALID_STATUS)
        archived = (f"; archived={entry['archive_row_count']}"
                    if entry["archive_row_count"] is not None else "")
        lines.append(f"  {label}: {live}{archived}")
    if coverage == "PARTIAL":
        lines.append("  PARTIAL coverage: do not infer global absence or closure.")
    for name in FEDERATION_FINDING_CLASSES:
        count = payload["finding_counts"][name]
        if count:
            lines.append(f"  {name}: {count}")
    if operational_errors:
        lines.append(f"  operational_errors: {len(operational_errors)}")
    return exit_code, lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_val = sub.add_parser("validate", help="validate one register CSV")
    p_val.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    p_scan = sub.add_parser("scan", help="harvest candidates (PRD §5.1)")
    p_scan.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    p_scan.add_argument("--out", type=Path, default=DEFAULT_SCAN_OUT)
    p_fed = sub.add_parser("federation", help="survey canonical registers")
    p_fed.add_argument("--register", type=Path, required=True)
    p_fed.add_argument("--out", type=Path)
    p_arc = sub.add_parser(
        "archive",
        help="relocate owner-closed rows to the REGISTER_CLOSED.csv sibling")
    # The one mutating verb: no default register, so a child-loop session can
    # never archive the root register by omission (K-TM cross-loop rule).
    p_arc.add_argument("--register", type=Path, required=True)
    p_arc.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        root = repo_root()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"taskmgmt OPERATIONAL (exit 2): git unavailable: {exc}")
        return 2

    if args.command == "validate":
        code, lines = validate_register(root, args.register)
    elif args.command == "scan":
        code, lines = scan(root, args.register, args.out)
    elif args.command == "archive":
        code, lines = archive_register(root, args.register, args.dry_run)
    else:
        code, lines = federation(root, args.register, args.out)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
