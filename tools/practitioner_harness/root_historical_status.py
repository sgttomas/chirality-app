"""Isolated Root historical reader; never extends prose-bullet-v1 lifecycle."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys

import prose_bullet_v1
from harness_common import HarnessOperationalError

# Validation helpers are repository tools, independent of the selected fixture root.
VALIDATION = Path(__file__).resolve().parents[1] / "validation"
if str(VALIDATION) not in sys.path:
    sys.path.insert(0, str(VALIDATION))

RETIREMENT = re.compile(
    r"^## SCA-005 retirement record\s*\n+"
    r"\[RETIRED — SCA-005\] Historical source carrier;[^\n]+Successor: ([^\s]+)\.[^\n]*$",
    re.MULTILINE,
)


def resolve_state(root: Path, config: dict) -> dict:
    try:
        from root_governance_state import load_governance_state, GovernanceError
    except ImportError as exc:
        raise HarnessOperationalError("Root governance state validator is unavailable.") from exc
    try:
        return load_governance_state(root, config, require_effective=False)
    except (GovernanceError, OSError, ValueError, KeyError) as exc:
        raise HarnessOperationalError(f"Root governance state refused: {exc}") from exc


def parse_historical_status(path: Path, root: Path, state: dict):
    rel = path.relative_to(root).as_posix()
    rows = [row for row in state["source_statuses"] if row["path"] == rel]
    if len(rows) != 1 or not path.resolve().is_relative_to(root.resolve()):
        raise HarnessOperationalError(f"Historical source outside exact accepted census: {rel}")
    row = rows[0]
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    stage = state.get("stage")
    if stage == "prepared":
        if digest != row["preimage_sha256"]:
            raise HarnessOperationalError(f"Prepared historical source preimage mismatch: {rel}")
        doc = prose_bullet_v1.parse_status_document(raw.decode("utf-8"))
        if doc.current_state == "RETIRED":
            raise HarnessOperationalError("Prepared source cannot assert retirement before application.")
        return doc
    if stage not in ("applied_pending_confirmation", "effective"):
        raise HarnessOperationalError(f"Unknown historical application stage: {stage!r}")
    if digest != row["postimage_sha256"]:
        raise HarnessOperationalError(f"Historical source postimage mismatch: {rel}")
    doc = prose_bullet_v1.parse_status_document(raw.decode("utf-8"))
    # The accepted postimage appends a separate, final retirement record. It
    # intentionally preserves the original lifecycle History bytes. This is a
    # Root-only assertion, never a new rule in the frozen ordinary parser.
    matches = list(RETIREMENT.finditer(raw.decode("utf-8")))
    if doc.current_state != "RETIRED" or len(matches) != 1:
        raise HarnessOperationalError(f"Historical retirement current/record assertion mismatch: {rel}")
    match = matches[0]
    if raw.decode("utf-8")[match.end():].strip():
        raise HarnessOperationalError(f"Historical retirement record is not the final assertion: {rel}")
    doc.history.append(prose_bullet_v1.HistoryEntry(
        date=None, raw=match.group(0), state="RETIRED", actor="SCA-005",
        rule="root_historical_retirement", caveat_class=prose_bullet_v1.PARSED))
    return doc
