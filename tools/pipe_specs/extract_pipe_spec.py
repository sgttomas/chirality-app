#!/usr/bin/env python3
"""
extract_pipe_spec.py
Single-PDF CLI for Millenia Engineering Piping Class spec extraction.

Thin wrapper around `pipe_spec_extractor.extract_pipe_spec()`.

Usage:
    python3 tools/pipe_specs/extract_pipe_spec.py \
        --pdf <PDF_PATH> \
        --output-dir <OUTPUT_DIR>

Inputs:
    --pdf PATH          Path to a Pipe Spec PDF file (required).
    --output-dir DIR    Output root directory (required).

Outputs (on parse_status=ok):
    {output-dir}/{spec_id}/{revision}/tables.csv
    {output-dir}/{spec_id}/{revision}/_header.csv
    {output-dir}/{spec_id}/{revision}/_raw_rows.csv
    {output-dir}/{spec_id}/{revision}/_diagnostics.csv

Outputs (on parse_status=parse_fail):
    {output-dir}/{spec_id}/{revision}/_diagnostics.csv      (only)

Stdout: structured key=value summary lines.
Stderr: input errors, parse_fail diagnostics.

Exit codes:
    0 — extraction ok
    1 — parse_fail (per-spec contract; outputs limited to _diagnostics.csv)
    2 — input error (missing/invalid arguments, file not found)

Determinism:
    No LLM calls, no network, no API keys. Output is byte-identical
    across reruns on the same input.

Idempotence:
    Overwrites the per-spec/revision output files cleanly. Repeat runs
    produce identical bytes.

Write scope:
    Limited to {output-dir}/{spec_id}/{revision}/ for the parsed file.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Allow running as a script without package install
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipe_spec_extractor import (  # noqa: E402
    DIAGNOSTICS_COLUMNS,
    HEADER_COLUMNS,
    RAW_ROWS_COLUMNS,
    TABLES_COLUMNS,
    ExtractionResult,
    extract_pipe_spec,
)


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in columns})


def write_outputs(result: ExtractionResult, output_dir: Path) -> dict[str, Path]:
    """Write outputs per parse-fail artifact contract; return paths written."""
    spec_dir = output_dir / result.spec_id / result.revision
    spec_dir.mkdir(parents=True, exist_ok=True)

    for stale_name in (
        "tables.csv",
        "_header.csv",
        "_raw_rows.csv",
        "_diagnostics_words.csv",
    ):
        (spec_dir / stale_name).unlink(missing_ok=True)

    diag_path = spec_dir / "_diagnostics.csv"
    _write_csv(diag_path, DIAGNOSTICS_COLUMNS, result.diagnostics)

    written: dict[str, Path] = {"_diagnostics.csv": diag_path}

    if result.status == "ok":
        tables_path = spec_dir / "tables.csv"
        header_path = spec_dir / "_header.csv"
        raw_path = spec_dir / "_raw_rows.csv"
        _write_csv(tables_path, TABLES_COLUMNS, result.table_rows)
        _write_csv(header_path, HEADER_COLUMNS, result.header_rows)
        _write_csv(raw_path, RAW_ROWS_COLUMNS, result.raw_rows)
        written.update(
            {
                "tables.csv": tables_path,
                "_header.csv": header_path,
                "_raw_rows.csv": raw_path,
            }
        )
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--pdf", required=True, help="Path to Pipe Spec PDF")
    parser.add_argument("--output-dir", required=True, help="Output root directory")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    result = extract_pipe_spec(pdf_path)
    written = write_outputs(result, output_dir)

    counts = result.section_counts()
    print(f"spec_id={result.spec_id}")
    print(f"revision={result.revision}")
    print(f"source_pdf={result.source_pdf}")
    print(f"source_sha256={result.source_sha256}")
    print(f"parse_status={result.status}")
    print(f"page_count={result.page_count}")
    print(f"blank_pages={result.blank_pages}")
    print(f"rows_pipe={counts['PIPE']}")
    print(f"rows_flanges_fittings={counts['FLANGES_FITTINGS']}")
    print(f"rows_bolting_gaskets={counts['BOLTING_GASKETS']}")
    print(f"rows_tubing={counts['TUBING']}")
    print(f"rows_valves={counts['VALVES']}")
    print(f"output_dir={output_dir / result.spec_id / result.revision}")
    for name, path in sorted(written.items()):
        print(f"wrote.{name}={path}")

    if result.status != "ok":
        print(
            f"ERROR: parse_fail: {result.failure_reason}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
