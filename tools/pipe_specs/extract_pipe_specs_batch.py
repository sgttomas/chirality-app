#!/usr/bin/env python3
"""
extract_pipe_specs_batch.py
Batch driver for Pipe Spec PDF extraction.

Iterates *.pdf in --input-dir (skipping any `Superceded/` subfolder if
present), imports `pipe_spec_extractor.extract_pipe_spec()` directly
(no subprocess), and writes per-spec outputs plus a top-level
`_extraction_summary.csv` covering both `ok` and `parse_fail` runs.

Usage:
    python3 tools/pipe_specs/extract_pipe_specs_batch.py \
        --input-dir <DIR> \
        --output-dir <OUTPUT_DIR>

Inputs:
    --input-dir DIR     Directory of Pipe Spec PDFs (required).
    --output-dir DIR    Output root directory (required).

Outputs:
    {output-dir}/{spec_id}/{revision}/...        (per-spec artifacts)
    {output-dir}/_extraction_summary.csv         (always written)

Stdout: aggregate counts and the path to the summary CSV.
Stderr: input errors and per-spec parse_fail diagnostics.

Exit codes:
    0 — all specs ok
    1 — at least one parse_fail (run otherwise complete)
    2 — input error

Determinism:
    No LLM calls, no network, no API keys. Outputs are byte-identical
    across reruns. PDFs are processed in alphabetical order.

Idempotence:
    Per-spec outputs and the summary CSV are overwritten cleanly.
    Re-running on an unchanged input directory produces identical bytes.

Write scope:
    Limited to --output-dir.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_pipe_spec import write_outputs  # noqa: E402
from pipe_spec_extractor import extract_pipe_spec  # noqa: E402

SUMMARY_COLUMNS = [
    "spec_id",
    "source_pdf",
    "source_revision",
    "source_sha256",
    "page_count",
    "blank_pages",
    "rows_pipe",
    "rows_flanges_fittings",
    "rows_bolting_gaskets",
    "rows_tubing",
    "rows_valves",
    "parse_status",
    "failure_reason",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    if not input_dir.is_dir():
        print(f"ERROR: input directory not found: {input_dir}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(p for p in input_dir.glob("*.pdf") if p.is_file())
    if not pdfs:
        print(f"ERROR: no *.pdf files found in {input_dir}", file=sys.stderr)
        return 2

    summary_rows: list[dict[str, str]] = []
    ok_count = 0
    fail_count = 0

    for pdf in pdfs:
        result = extract_pipe_spec(pdf)
        write_outputs(result, output_dir)
        counts = result.section_counts()
        summary_rows.append(
            {
                "spec_id": result.spec_id,
                "source_pdf": result.source_pdf,
                "source_revision": result.revision,
                "source_sha256": result.source_sha256,
                "page_count": str(result.page_count),
                "blank_pages": str(result.blank_pages),
                "rows_pipe": str(counts["PIPE"]),
                "rows_flanges_fittings": str(counts["FLANGES_FITTINGS"]),
                "rows_bolting_gaskets": str(counts["BOLTING_GASKETS"]),
                "rows_tubing": str(counts["TUBING"]),
                "rows_valves": str(counts["VALVES"]),
                "parse_status": result.status,
                "failure_reason": result.failure_reason,
            }
        )
        if result.status == "ok":
            ok_count += 1
        else:
            fail_count += 1
            print(
                f"parse_fail: {result.source_pdf}: {result.failure_reason}",
                file=sys.stderr,
            )

    # Stable order: by source_pdf
    summary_rows.sort(key=lambda r: r["source_pdf"])

    summary_path = output_dir / "_extraction_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"specs_total={len(pdfs)}")
    print(f"specs_ok={ok_count}")
    print(f"specs_parse_fail={fail_count}")
    print(f"summary_csv={summary_path}")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
