from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]

import validate_piping_loop_receipts as validator


EXAMINED_SHA = "09dd651421fce167c6ad7dd850ecc4f3ff4fe68f"
LIVE_RECEIPTS = REPO_ROOT / validator.RECEIPTS_RELPATH
pytestmark = pytest.mark.skipif(
    not LIVE_RECEIPTS.is_file(),
    reason="public export intentionally excludes private piping loop receipts",
)


def _contract_prelude() -> bytes:
    raw = LIVE_RECEIPTS.read_bytes()
    marker = validator.MARKER.encode("utf-8")
    start = raw.index(marker)
    end = raw.index(b"\n", start) + 1
    return raw[:end]


def _receipt(
    receipt_id: int = 45,
    parent_id: int = 44,
    examined_sha: str = EXAMINED_SHA,
    extra_records: str = "",
    include_gate: bool = True,
    receipt_id_value: int | None = None,
) -> str:
    gate = (
        "  - Gate-Outcome: `EXECUTED` — candidate validated and pointed to its artifacts\n"
        if include_gate
        else ""
    )
    extra = extra_records
    if extra and not extra.endswith("\n"):
        extra += "\n"
    record_id = receipt_id if receipt_id_value is None else receipt_id_value
    return (
        f"\n- **2026-07-15 — Receipt {receipt_id}** (validator fixture).\n"
        f"  - Receipt-ID: `Receipt-{record_id}`\n"
        f"  - Examined-Through: `{examined_sha}`\n"
        f"  - Parent-Receipt: `Receipt-{parent_id}`\n"
        f"{extra}"
        f"{gate}"
    )


def _write(tmp_path: Path, versioned: str, mutate_prefix: bool = False) -> Path:
    raw = _contract_prelude() + versioned.encode("utf-8")
    if mutate_prefix:
        raw = b"X" + raw[1:]
    path = tmp_path / "LOOP_RECEIPTS.md"
    path.write_bytes(raw)
    return path


def _codes(path: Path) -> set[str]:
    return {
        issue.code
        for issue in validator.validate_receipts(path, REPO_ROOT)
    }


def test_valid_minimal_receipt(tmp_path):
    path = _write(tmp_path, _receipt())
    assert validator.validate_receipts(path, REPO_ROOT) == []


def test_valid_gate_stop_and_owner_transcription(tmp_path):
    records = (
        "  - Owner-Direction: CHAT_TRANSCRIPTION — EVIDENCE, NOT RULING — "
        '"Run 264 tests and leave IN_PROGRESS unchanged."\n'
        "  - Pointers: `D-44_RULING_2026-07-15.md`\n"
    )
    receipt = _receipt(extra_records=records).replace(
        "`EXECUTED` — candidate validated and pointed to its artifacts",
        "`AWAITING_OWNER` — method choice requires the named owner ruling",
    )
    path = _write(tmp_path, receipt)
    assert validator.validate_receipts(path, REPO_ROOT) == []


def test_valid_concurrent_sibling_cursors(tmp_path):
    path = _write(
        tmp_path,
        _receipt(receipt_id=45, parent_id=44)
        + _receipt(receipt_id=46, parent_id=44),
    )
    assert validator.validate_receipts(path, REPO_ROOT) == []


def test_missing_or_invalid_cursor_fields_fail(tmp_path):
    missing_parent = _receipt().replace("  - Parent-Receipt: `Receipt-44`\n", "")
    assert "REQUIRED_FIELD_COUNT" in _codes(_write(tmp_path, missing_parent))

    invalid_sha = _receipt(examined_sha="abc")
    assert "INVALID_EXAMINED_THROUGH" in _codes(_write(tmp_path, invalid_sha))

    unresolved_sha = _receipt(examined_sha="f" * 40)
    assert "COMMIT_NOT_FOUND" in _codes(_write(tmp_path, unresolved_sha))


def test_missing_parent_duplicate_id_and_missing_gate_fail(tmp_path):
    assert "PARENT_RECEIPT_NOT_FOUND" in _codes(
        _write(tmp_path, _receipt(parent_id=999))
    )

    duplicate = _receipt() + _receipt(receipt_id=46, receipt_id_value=45)
    codes = _codes(_write(tmp_path, duplicate))
    assert "DUPLICATE_RECEIPT_ID" in codes
    assert "RECEIPT_ID_MISMATCH" in codes

    assert "REQUIRED_FIELD_COUNT" in _codes(
        _write(tmp_path, _receipt(include_gate=False))
    )


def test_oversized_and_measurement_receipts_fail(tmp_path):
    oversized = _receipt(extra_records=f"  - Pointers: `{'x' * 5000}`\n")
    assert "RECEIPT_BYTE_LIMIT" in _codes(_write(tmp_path, oversized))

    measured = _receipt(extra_records="  - Checks: pytest 264 passed; 264/264\n")
    assert "DUPLICATED_MEASUREMENT" in _codes(_write(tmp_path, measured))


def test_ambiguous_boundary_and_altered_prefix_fail(tmp_path):
    nonblank = "unexpected content\n" + _receipt()
    assert "CONTENT_BEFORE_FIRST_RECEIPT" in _codes(_write(tmp_path, nonblank))

    duplicated_marker = _receipt() + validator.MARKER + "\n"
    assert "CONTRACT_MARKER_COUNT" in _codes(
        _write(tmp_path, duplicated_marker)
    )

    assert "FROZEN_PREFIX_HASH" in _codes(
        _write(tmp_path, _receipt(), mutate_prefix=True)
    )


def test_nested_structures_and_unknown_fields_fail(tmp_path):
    nested = _receipt(extra_records=(
        "  - Pointers: `D-44_RULING_2026-07-15.md`\n"
        "    - nested detail\n"
        "  - Evidence-Table: forbidden\n"
    ))
    codes = _codes(_write(tmp_path, nested))
    assert "NESTED_RECORD" in codes
    assert "UNKNOWN_RECORD_FIELD" in codes
