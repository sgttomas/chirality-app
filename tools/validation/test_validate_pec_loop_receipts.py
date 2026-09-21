from pathlib import Path

import validate_pec_loop_receipts as validator

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMINED_SHA = "7458e9c1eb9399ed259da464207d9a507acdea2e"


def prefix():
    return (REPO_ROOT / validator.RECEIPTS_RELPATH).read_bytes()[:validator.FROZEN_PREFIX_BYTES]


def receipt(number=167, parent=166, sha=EXAMINED_SHA):
    return (
        f"\n- **2026-09-05 — Receipt {number}** (validator fixture).\n"
        f"  - Receipt-ID: `Receipt-{number}`\n"
        f"  - Examined-Through: `{sha}`\n"
        f"  - Parent-Receipt: `Receipt-{parent}`\n"
        "  - Gate-Outcome: `AWAITING_OWNER` — candidate awaits owner disposition\n"
    ).encode()


def write(tmp_path, raw):
    path = tmp_path / "ledger.md"
    path.write_bytes(raw)
    return path


def codes(path):
    return {x.code for x in validator.validate_receipts(path, REPO_ROOT)}


def continuation():
    return prefix() + validator.MARKER.encode() + b"\n"


def test_exact_legacy_ledger_is_valid(tmp_path):
    assert codes(write(tmp_path, prefix())) == set()


def test_legacy_tamper_and_unversioned_append_fail(tmp_path):
    for raw in (b"X" + prefix()[1:], prefix()[:-1], prefix() + receipt()):
        assert codes(write(tmp_path, raw))


def test_valid_continuation_and_same_branch_chain(tmp_path):
    assert codes(write(tmp_path, continuation() + receipt() + receipt(168, 167))) == set()


def test_prefix_immutable_with_continuation(tmp_path):
    raw = b"X" + continuation()[1:] + receipt()
    assert "FROZEN_PREFIX_HASH" in codes(write(tmp_path, raw))


def test_parent_and_commit_must_resolve(tmp_path):
    assert "PARENT_RECEIPT_NOT_FOUND" in codes(write(tmp_path, continuation() + receipt(parent=999)))
    assert "COMMIT_NOT_FOUND" in codes(write(tmp_path, continuation() + receipt(sha="f" * 40)))


def test_duplicate_marker_and_missing_gate_fail(tmp_path):
    assert "CONTRACT_MARKER_COUNT" in codes(write(tmp_path, continuation() * 2 + receipt()))
    raw = continuation() + receipt().split(b"  - Gate-Outcome:")[0]
    assert "REQUIRED_FIELD_COUNT" in codes(write(tmp_path, raw))


def test_shared_count_and_structure_rules_apply(tmp_path):
    raw = continuation() + receipt() + b"  - Checks: 12 tests passed\n"
    assert "DUPLICATED_MEASUREMENT" in codes(write(tmp_path, raw))
    raw = continuation() + receipt() + b"    - nested record\n"
    assert "NESTED_RECORD" in codes(write(tmp_path, raw))


def test_cli_missing_and_outside_paths_fail(tmp_path):
    assert validator.main(["--repo-root", str(tmp_path), "--receipts", "missing.md"]) == 2
    assert validator.main(["--repo-root", str(tmp_path), "--receipts", "../outside.md"]) == 2


def test_current_ledger_is_valid():
    assert codes(REPO_ROOT / validator.RECEIPTS_RELPATH) == set()
