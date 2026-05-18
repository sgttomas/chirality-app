#!/usr/bin/env python3
"""
run_prose_validation.py
Gate 1.5-P orchestration helper: after the `domain-prose-validate` TASK
fan-out has populated `<audit-dir>/prose_validation_extracts/page_NNNN.reextract.md`
for every page, this script runs `validate_prose.py` to populate
`prose_validation.json`, then prints a summary suitable for the agent's
Stage 3 consolidation.

This script does NOT dispatch the TASK agents itself — that's the
orchestrating persona's responsibility (see AGENT_DOMAIN_DECOMP.md
Gate 1.5-P stages). This is the post-fanout aggregation step,
mirroring `tools/pdf2md/run_folio_extraction.py`.

Usage:
    python3 tools/source_audit/run_prose_validation.py \\
        --work-dir <_Sources/<book>_pdf2md_work> \\
        --audit-dir <_Sources/<book>/audit>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--work-dir", required=True)
    p.add_argument("--audit-dir", required=True)
    p.add_argument("--reextract-dir", default=None,
                   help="Default: <audit-dir>/prose_validation_extracts")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    audit_dir = Path(args.audit_dir).resolve()
    reext_dir = (
        Path(args.reextract_dir).resolve()
        if args.reextract_dir
        else audit_dir / "prose_validation_extracts"
    )
    if not reext_dir.is_dir():
        print(f"ERROR: reextract dir not found: {reext_dir}", file=sys.stderr)
        return 2

    validator = Path(__file__).resolve().parent / "validate_prose.py"
    proc = subprocess.run(
        [sys.executable, str(validator),
         "--work-dir", str(work_dir),
         "--reextract-dir", str(reext_dir),
         "--audit-dir", str(audit_dir)],
        text=True,
    )
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
