#!/usr/bin/env python3
"""Validate the D-44 / DEC-075 chirality-piping receipt contract.

The tool is read-only. Exit 0 means structural conformance, exit 1 means one
or more contract violations, and exit 2 means an operational/input failure.
Structural conformance is evidence only; it does not authenticate owner
directions or decide whether prose is semantically non-reconstructible.
"""

from __future__ import annotations

from pathlib import Path

from loop_receipt_contract import (
    ReceiptContract,
    ReceiptIssue,
    run_cli,
    validate_receipts as validate_contract_receipts,
)


RECEIPTS_RELPATH = Path("projects/chirality-piping/loop/LOOP_RECEIPTS.md")
FROZEN_THROUGH = 44
FROZEN_PREFIX_BYTES = 74168
FROZEN_PREFIX_SHA256 = (
    "671a1f722a56d98bbc52bb5a3062d0bf7c25bc37312384fc63526bc43c2ca59f"
)
MARKER = (
    "<!-- receipt-contract-v2 frozen-through=Receipt-44 "
    "prefix-bytes=74168 "
    "prefix-sha256=671a1f722a56d98bbc52bb5a3062d0bf7c25bc37312384fc63526bc43c2ca59f -->"
)

CONTRACT = ReceiptContract(
    contract_id="D-44",
    receipts_relpath=RECEIPTS_RELPATH,
    frozen_through=FROZEN_THROUGH,
    frozen_prefix_bytes=FROZEN_PREFIX_BYTES,
    frozen_prefix_sha256=FROZEN_PREFIX_SHA256,
    marker=MARKER,
)


def validate_receipts(
    receipts_path: Path,
    repo_root: Path,
    validation_commit: str = "HEAD",
) -> list[ReceiptIssue]:
    """Preserve the original project-wrapper API for callers and tests."""
    return validate_contract_receipts(
        receipts_path=receipts_path,
        repo_root=repo_root,
        contract=CONTRACT,
        validation_commit=validation_commit,
    )


def main(argv: list[str] | None = None) -> int:
    return run_cli(CONTRACT, __doc__ or "", argv)


if __name__ == "__main__":
    raise SystemExit(main())
