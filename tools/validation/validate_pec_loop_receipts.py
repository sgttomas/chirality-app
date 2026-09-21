#!/usr/bin/env python3
"""Validate the PEC D-PEC-80 receipt migration and versioned continuation.

The exact pre-migration ledger is accepted unchanged as a legacy-only state.
Any continuation requires the shared contract marker and shared v2 validation.
Exit 0 is structural evidence, never a ruling; 1 is invalid, 2 is input failure.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from loop_receipt_contract import ReceiptContract, ReceiptIssue
from loop_receipt_contract import validate_receipts as validate_contract_receipts

RECEIPTS_RELPATH = Path("projects/pec/loop/LOOP_RECEIPTS.md")
FROZEN_THROUGH = 166
FROZEN_PREFIX_BYTES = 426714
FROZEN_PREFIX_SHA256 = "153732e389a1dd948805dd71150f63d865ef3c70cb8b8f8230a36b836dda0dd7"
MARKER = (
    "<!-- receipt-contract-v2 frozen-through=Receipt-166 "
    "prefix-bytes=426714 "
    f"prefix-sha256={FROZEN_PREFIX_SHA256} -->"
)
CONTRACT = ReceiptContract(
    contract_id="D-PEC-80", receipts_relpath=RECEIPTS_RELPATH,
    frozen_through=FROZEN_THROUGH, frozen_prefix_bytes=FROZEN_PREFIX_BYTES,
    frozen_prefix_sha256=FROZEN_PREFIX_SHA256, marker=MARKER,
)


def validate_receipts(receipts_path: Path, repo_root: Path,
                      validation_commit: str = "HEAD") -> list[ReceiptIssue]:
    raw = receipts_path.read_bytes()
    if (len(raw) == FROZEN_PREFIX_BYTES
            and hashlib.sha256(raw).hexdigest() == FROZEN_PREFIX_SHA256):
        return []
    return validate_contract_receipts(
        receipts_path, repo_root, CONTRACT, validation_commit,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--receipts", type=Path, default=RECEIPTS_RELPATH)
    parser.add_argument("--validation-commit", default="HEAD")
    args = parser.parse_args(argv)
    try:
        root = args.repo_root.resolve()
        path = (root / args.receipts).resolve()
        if path != root and root not in path.parents:
            raise ValueError("receipt path resolves outside repo root")
        issues = validate_receipts(path, root, args.validation_commit)
        legacy_only = path.stat().st_size == FROZEN_PREFIX_BYTES
    except (OSError, ValueError) as exc:
        print(f"OPERATIONAL_ERROR: {exc}", file=sys.stderr)
        return 2
    for issue in issues:
        location = f":{issue.line}" if issue.line is not None else ""
        print(f"INVALID {issue.code} {path}{location}: {issue.message}")
    if issues:
        return 1
    state = "exact legacy-only ledger" if legacy_only else "versioned receipt contract satisfied"
    print(f"VALID {path}: frozen through Receipt-{FROZEN_THROUGH}; {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
