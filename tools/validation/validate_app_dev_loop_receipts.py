#!/usr/bin/env python3
"""Validate the D-APP-57 chirality-app-dev receipt contract.

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


RECEIPTS_RELPATH = Path("projects/chirality-app-dev/loop/LOOP_RECEIPTS.md")
FROZEN_THROUGH = 52
FROZEN_PREFIX_BYTES = 114344
FROZEN_PREFIX_SHA256 = (
    "d67fbb7e5c58427eb22af95c81ae7be7e0b9d86f2ceb07b10ed8dbf08b0be0a7"
)
MARKER = (
    "<!-- receipt-contract-v2 project=chirality-app-dev "
    "frozen-through=Receipt-52 prefix-bytes=114344 "
    "prefix-sha256=d67fbb7e5c58427eb22af95c81ae7be7e0b9d86f2ceb07b10ed8dbf08b0be0a7 -->"
)

CONTRACT = ReceiptContract(
    contract_id="D-APP-57",
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
