#!/usr/bin/env python3
"""Emit the deterministic source-range-to-target-ID map embedded in a candidate SoW."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from common import SowError, iter_source_blocks, load_catalog, parse_sow, sha256_file, validate_document
from finalize_scope_of_work import finalize_candidate_text

FIELDS = (
    "SourceFile",
    "SourceLineStart",
    "SourceLineEnd",
    "SourceSHA256",
    "TargetID",
    "TargetSHA256",
    "Disposition",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope-of-work", type=Path, required=True)
    parser.add_argument("--production-scope-of-work", type=Path)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()
    try:
        catalog = load_catalog()
        doc = parse_sow(args.scope_of_work, catalog)
        issues = validate_document(doc, catalog)
        if issues:
            raise SowError("candidate validation failed: " + "; ".join(issues))
        target_doc = doc
        if args.production_scope_of_work:
            expected, _ = finalize_candidate_text(args.scope_of_work, doc.raw)
            production_text = args.production_scope_of_work.read_text(encoding="utf-8")
            if production_text != expected:
                raise SowError("production ScopeOfWork.md is not the deterministic finalization of the evidence candidate")
            target_doc = parse_sow(args.production_scope_of_work, catalog)
            production_issues = validate_document(target_doc, catalog)
            if production_issues:
                raise SowError("production validation failed: " + "; ".join(production_issues))
        rows = []
        for metadata, _ in iter_source_blocks(doc.body):
            required = {"file", "line_start", "line_end", "source_sha256", "target_id", "disposition"}
            missing = required - metadata.keys()
            if missing:
                raise SowError("source marker missing: " + ", ".join(sorted(missing)))
            source = args.source_dir / str(metadata["file"])
            if not source.is_file():
                raise SowError(f"source file is missing: {source}")
            actual_sha = sha256_file(source)
            if actual_sha != metadata["source_sha256"]:
                raise SowError(f"source hash mismatch: {source}")
            if metadata["disposition"] not in catalog.dispositions:
                raise SowError(f"unknown migration disposition: {metadata['disposition']}")
            if metadata["target_id"] not in target_doc.definitions:
                raise SowError(f"target ID is not defined: {metadata['target_id']}")
            rows.append(
                {
                    "SourceFile": metadata["file"],
                    "SourceLineStart": metadata["line_start"],
                    "SourceLineEnd": metadata["line_end"],
                    "SourceSHA256": metadata["source_sha256"],
                    "TargetID": metadata["target_id"],
                    "TargetSHA256": target_doc.sha256,
                    "Disposition": metadata["disposition"],
                }
            )
        if not rows:
            raise SowError("candidate contains no source mapping markers")
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print(f"PASS rows={len(rows)} output={args.output_csv}")
        return 0
    except (OSError, UnicodeError, SowError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
