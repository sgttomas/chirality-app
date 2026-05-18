#!/usr/bin/env python3
"""
validate_prose.py — Gate 1.5-P Stage 2 CLI (deterministic comparator).

Walks every page of a source whose 1.5-P re-extracts have been produced,
runs `compare_page` per page, and aggregates results into
`<audit-dir>/prose_validation.json` (schema `pdf2md-prose-validate/v1`).

This is the deterministic middle stage of the 1.5-P pipeline. The skill
(Stage 1, `domain-prose-validate`) produces the re-extracts; this CLI
runs the strict compare; then the agent (Stage 3, persona section in
AGENT_DOMAIN_DECOMP.md) consolidates findings, dispatches re-extracts
for structural fails, and writes survivor equation proposals to
`equations_backcheck.json`.

**1.5-P is purely additive.** This CLI never writes to any
`*_verified.json` or `*_flagged.json` sidecar. Its sole on-disk output
is `prose_validation.json`.

Usage:
  python3 tools/source_audit/validate_prose.py \\
      --work-dir <_Sources/<book>_pdf2md_work> \\
      --reextract-dir <_Sources/<book>/audit/prose_validation_extracts> \\
      --audit-dir <_Sources/<book>/audit> \\
      [--output prose_validation.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.source_audit.compare_extracts import compare_page  # noqa: E402


PAGE_MD_RE = re.compile(r"^page_(\d{4})\.md$")
PAGE_REEXTRACT_RE = re.compile(r"^page_(\d{4})\.reextract\.md$")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Gate 1.5-P deterministic comparator.")
    p.add_argument("--work-dir", required=True,
                   help="pdf2md work dir containing page_NNNN.md (the original extracts).")
    p.add_argument("--reextract-dir", required=True,
                   help="Dir containing page_NNNN.reextract.md (Stage 1 outputs).")
    p.add_argument("--audit-dir", required=True,
                   help="Source audit dir; prose_validation.json is written here.")
    p.add_argument("--output", default="prose_validation.json")
    return p.parse_args()


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main() -> int:
    args = parse_args()
    work_dir = Path(args.work_dir).resolve()
    reext_dir = Path(args.reextract_dir).resolve()
    audit_dir = Path(args.audit_dir).resolve()
    output = audit_dir / args.output
    audit_dir.mkdir(parents=True, exist_ok=True)

    # Collect every page that has BOTH an original extract and a re-extract.
    originals = {}
    for md in sorted(work_dir.glob("page_*.md")):
        m = PAGE_MD_RE.match(md.name)
        if m:
            originals[int(m.group(1))] = md

    reextracts = {}
    for md in sorted(reext_dir.glob("page_*.reextract.md")):
        m = PAGE_REEXTRACT_RE.match(md.name)
        if m:
            reextracts[int(m.group(1))] = md

    common = sorted(set(originals) & set(reextracts))
    missing_reextract = sorted(set(originals) - set(reextracts))

    pages_out: list[dict] = []
    counts = {
        "pages_compared": 0,
        "pages_with_structural_fails": 0,
        "prose_hunks": 0,
        "equation_structural_fails": 0,
        "equation_content_proposals": 0,
        "asset_structural_fails": 0,
        "caption_notes": 0,
    }
    for page in common:
        orig = _read_text(originals[page])
        reext = _read_text(reextracts[page])
        cmp = compare_page(orig, reext, page_num=page)
        d = cmp.to_dict()
        pages_out.append(d)
        counts["pages_compared"] += 1
        if cmp.has_structural_fails:
            counts["pages_with_structural_fails"] += 1
        counts["prose_hunks"] += len(cmp.prose_hunks)
        counts["equation_structural_fails"] += len(cmp.equation_structural_fails)
        counts["equation_content_proposals"] += len(cmp.equation_content_proposals)
        counts["asset_structural_fails"] += len(cmp.asset_structural_fails)
        counts["caption_notes"] += len(cmp.caption_notes)

    out = {
        "schema_version": "pdf2md-prose-validate/v1",
        "work_dir": str(work_dir),
        "reextract_dir": str(reext_dir),
        "audit_dir": str(audit_dir),
        "missing_reextract": missing_reextract,
        "counts": counts,
        "pages": pages_out,
    }
    output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"pages_compared={counts['pages_compared']} "
        f"struct_fails={counts['pages_with_structural_fails']} "
        f"prose_hunks={counts['prose_hunks']} "
        f"eq_proposals={counts['equation_content_proposals']} "
        f"missing_reextract={len(missing_reextract)} "
        f"output={output}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
