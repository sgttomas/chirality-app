#!/usr/bin/env python3
"""Validate exact Rev 6 PRD transcriptions against Git-pinned source blobs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


PACKAGE_REL = Path(
    "docs/governance_harness/_PROPOSALS/"
    "D-GOV-28_root_runtime_stewardship"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument(
        "--spec",
        type=Path,
        default=PACKAGE_REL / "TRANSCRIPTION_SPEC.json",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def resolve_under(root: Path, path: Path) -> Path:
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes repo root: {path}") from exc
    return resolved


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    spec_path = resolve_under(root, args.spec)
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))

    candidate_path = resolve_under(root, Path(spec["candidate_path"]))
    open_path = resolve_under(root, Path(spec["open_items_path"]))
    candidate_bytes = candidate_path.read_bytes()
    open_bytes = open_path.read_bytes()

    checks: list[dict[str, object]] = []
    errors: list[str] = []

    source_bytes_by_path: dict[str, bytes] = {}
    source_file_checks: list[dict[str, object]] = []
    for source_file in spec["source_files"]:
        source_rel = source_file["path"]
        result = subprocess.run(
            ["git", "show", f"{spec['basis_commit']}:{source_rel}"],
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            errors.append(
                f"unable to read pinned source {source_rel}: "
                f"{result.stderr.decode('utf-8', errors='replace').strip()}"
            )
            source_bytes = b""
        else:
            source_bytes = result.stdout
        actual_sha = sha256(source_bytes)
        expected_sha = source_file["blob_sha256"]
        passed = result.returncode == 0 and actual_sha == expected_sha
        if not passed:
            errors.append(
                f"source blob hash mismatch {source_rel}: "
                f"expected={expected_sha}, actual={actual_sha}"
            )
        source_bytes_by_path[source_rel] = source_bytes
        source_file_checks.append(
            {
                "path": source_rel,
                "basis_commit": spec["basis_commit"],
                "expected_blob_sha256": expected_sha,
                "actual_blob_sha256": actual_sha,
                "status": "PASS" if passed else "FAIL",
            }
        )

    for item in spec["transcriptions"]:
        source_rel = item["source_path"]
        if source_rel not in source_bytes_by_path:
            errors.append(f"undeclared source file for {item['id']}: {source_rel}")
            source_bytes = b""
        else:
            source_bytes = source_bytes_by_path[source_rel]
        exact = item["text"].encode("utf-8")
        source_count = source_bytes.count(exact)
        candidate_count = candidate_bytes.count(exact)
        passed = source_count == 1 and candidate_count == 1
        checks.append(
            {
                "id": item["id"],
                "source_path": source_rel,
                "source_anchor": item["source_anchor"],
                "source_count": source_count,
                "candidate_count": candidate_count,
                "exact_utf8_sha256": sha256(exact),
                "status": "PASS" if passed else "FAIL",
            }
        )
        if not passed:
            errors.append(
                f"{item['id']}: source_count={source_count}, "
                f"candidate_count={candidate_count}"
            )

    candidate_text = candidate_bytes.decode("utf-8")
    marker_checks: list[dict[str, object]] = []
    for marker in spec["required_candidate_markers"]:
        count = candidate_text.count(marker)
        passed = count == 1
        marker_checks.append(
            {"marker": marker, "count": count, "status": "PASS" if passed else "FAIL"}
        )
        if not passed:
            errors.append(f"candidate marker count={count}: {marker}")

    open_text = open_bytes.decode("utf-8")
    rows = list(csv.DictReader(open_text.splitlines()))
    ids = [row.get("OpenItemID", "") for row in rows]
    statuses = [row.get("Status", "") for row in rows]
    expected_ids = spec["required_open_item_ids"]
    allowed_statuses = set(spec["allowed_open_statuses"])

    if len(ids) != len(set(ids)):
        errors.append("duplicate OpenItemID")
    if sorted(ids) != sorted(expected_ids):
        errors.append(
            "open-item membership mismatch: "
            f"expected={sorted(expected_ids)}, actual={sorted(ids)}"
        )
    invalid_statuses = sorted(set(statuses) - allowed_statuses)
    if invalid_statuses:
        errors.append(f"invalid open-item statuses: {invalid_statuses}")
    if "TBD" in open_text:
        errors.append("literal TBD is prohibited in OPEN_ITEMS.csv")

    report = {
        "schema": "chirality.prd-transcription-concordance-report/v1",
        "scope": spec["scope"],
        "basis_commit": spec["basis_commit"],
        "spec_path": str(spec_path.relative_to(root)),
        "spec_sha256": sha256(spec_bytes),
        "candidate_path": str(candidate_path.relative_to(root)),
        "candidate_sha256": sha256(candidate_bytes),
        "open_items_path": str(open_path.relative_to(root)),
        "open_items_sha256": sha256(open_bytes),
        "source_file_checks": source_file_checks,
        "transcription_checks": checks,
        "marker_checks": marker_checks,
        "open_item_check": {
            "expected_count": len(expected_ids),
            "actual_count": len(rows),
            "allowed_statuses": sorted(allowed_statuses),
            "actual_statuses": sorted(set(statuses)),
            "status": "PASS"
            if not any(
                error.startswith(("duplicate OpenItemID", "open-item", "invalid open-item", "literal TBD"))
                for error in errors
            )
            else "FAIL",
        },
        "result": "PASS" if not errors else "FAIL",
        "errors": errors,
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        output_path = resolve_under(root, args.output)
        package_root = (root / PACKAGE_REL).resolve()
        try:
            output_path.relative_to(package_root)
        except ValueError as exc:
            raise ValueError(
                f"output must remain inside proposal package: {args.output}"
            ) from exc
        output_path.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
