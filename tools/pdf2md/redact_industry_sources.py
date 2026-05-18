#!/usr/bin/env python3
"""
redact_industry_sources.py
Deterministic per-page redaction of identifying source-organization names,
issuer-specific document-number prefixes, and issuer-fingerprinting site
names in industry-practices Markdown, using a vocabulary YAML.

Designed to slot into the PDF2MD per-page pipeline as Phase 3c:
    Phase 3a — postprocess_page.py        (10-rule cleanup)
    Phase 3b — clean_pdf2md_output.py     (header/footer strip)
    Phase 3c — redact_industry_sources.py (this tool)
and, when ASSET_MODE=prose, on page_NNNN.anchored.md after the inline
rewriter so both prose flow and the "Unmatched Page Assets" block are
covered.

The redactor is idempotent: pages already containing the replacement IDs
re-run cleanly. This preserves PDF2MD's resume contract.

Replacement scheme
------------------
For each source entry in the vocabulary, three classes of token can be
redacted (longest-match-first, whole-token-boundary, case-insensitive):

  1. aliases                  → "<id>"
  2. document_number_prefixes → "<id> Doc"  (the suffix following the prefix
                                             is preserved so cross-citations
                                             remain traceable as references
                                             without revealing the issuer)
  3. site_names               → "<id> Facility"

`keep_verbatim` entries are recognised first and shielded from any
overlapping alias match; e.g. an alias "PIP" is not applied inside the
string "ASME PIP" if "PIP" appears in keep_verbatim and the keep_verbatim
entry covers the surrounding token range.

Usage
-----
    python3 redact_industry_sources.py PAGE_MD --vocab VOCAB_YAML [--out OUT_MD]
                                       [--dry-run] [--report REPORT_JSON]

Inputs
------
    PAGE_MD      — Markdown file to redact (page or anchored page).
    --vocab      — Path to industry_sources_vocab.yaml.
    --out        — Optional output path. Default: rewrite PAGE_MD in place.
    --dry-run    — Print diff stats; do not write.
    --report     — Optional JSON report of per-rule hit counts.

Exit codes
----------
    0 — completed (may have made zero edits)
    2 — input/setup error
    3 — vocabulary file invalid

Example
-------
    python3 tools/pdf2md/redact_industry_sources.py \\
        {WORK_DIR}/page_0001.anchored.md \\
        --vocab tools/pdf2md/industry_sources_vocab.yaml
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("redact_industry_sources: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)


# Token boundary: alphanumeric or underscore continues a token; everything
# else terminates it. We additionally treat ".", "-", "_" *inside* matched
# vocabulary tokens as literal — boundary is computed only at the outer edges
# of a match.
_BOUNDARY_LEFT_RE  = re.compile(r"(?:^|(?<=[^A-Za-z0-9]))")
_BOUNDARY_RIGHT_RE = re.compile(r"(?=$|[^A-Za-z0-9])")


class Vocab:
    """Parsed vocabulary with compiled regex patterns, sorted longest-first."""

    def __init__(self, raw: dict[str, Any]) -> None:
        if not isinstance(raw, dict) or "sources" not in raw:
            raise ValueError("vocab missing required `sources` list")
        self.case_sensitive: bool = bool(raw.get("case_sensitive", False))
        self.keep_verbatim: list[str] = list(raw.get("keep_verbatim") or [])
        self.sources = []
        for s in raw["sources"]:
            sid = s["id"]
            self.sources.append({
                "id": sid,
                "canonical_name": s["canonical_name"],
                "aliases": list(s.get("aliases") or []),
                "document_number_prefixes": list(s.get("document_number_prefixes") or []),
                "site_names": list(s.get("site_names") or []),
            })

        # Build a single combined alias->id table, including canonical_name as
        # an alias and sorted by length descending so longer phrases match
        # first (avoids "Shell Canada" being clobbered by "Shell" alone).
        alias_rows: list[tuple[str, str, str]] = []  # (token, replacement, rule)
        for s in self.sources:
            sid = s["id"]
            for tok in [s["canonical_name"]] + s["aliases"]:
                if tok:
                    alias_rows.append((tok, sid, "alias"))
            for tok in s["document_number_prefixes"]:
                if tok:
                    alias_rows.append((tok, f"{sid} Doc", "doc_prefix"))
            for tok in s["site_names"]:
                if tok:
                    alias_rows.append((tok, f"{sid} Facility", "site"))

        alias_rows.sort(key=lambda r: (-len(r[0]), r[0]))
        self.rules = alias_rows

        # Pre-compile keep-verbatim guard as a set of lowercased tokens, also
        # sorted longest-first, so we can skip-over those ranges.
        self._keep_lower = sorted({k.lower() for k in self.keep_verbatim}, key=lambda t: (-len(t), t))


def _compile_alt(tokens: list[str], case_sensitive: bool) -> re.Pattern[str] | None:
    if not tokens:
        return None
    # Escape and join, preserving longest-first order.
    alt = "|".join(re.escape(t) for t in tokens)
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(rf"(?<![A-Za-z0-9])(?:{alt})(?![A-Za-z0-9])", flags)


_LINK_TARGET_RE = re.compile(r"\]\(([^)]*)\)")
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def _structural_keep_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for m in _LINK_TARGET_RE.finditer(text):
        spans.append((m.start(1), m.end(1)))
    for m in _INLINE_CODE_RE.finditer(text):
        spans.append((m.start(), m.end()))
    return spans


def _keep_verbatim_spans(text: str, vocab: Vocab) -> list[tuple[int, int]]:
    """Return [(start, end), ...] spans that must be shielded from redaction."""
    spans = _structural_keep_spans(text)
    if vocab.keep_verbatim:
        pat = _compile_alt(vocab.keep_verbatim, vocab.case_sensitive)
        if pat:
            spans.extend((m.start(), m.end()) for m in pat.finditer(text))
    return spans


def _spans_overlap(a_start: int, a_end: int, spans: list[tuple[int, int]]) -> bool:
    for s, e in spans:
        if a_start < e and s < a_end:
            return True
    return False


def redact(text: str, vocab: Vocab) -> tuple[str, dict[str, int]]:
    """Apply all rules to `text`. Returns (redacted_text, per_rule_counts)."""
    counts: dict[str, int] = {"alias": 0, "doc_prefix": 0, "site": 0, "skipped_keep_verbatim": 0}

    # Compute keep-verbatim spans up front; we re-compute after each substitution
    # because indices shift. (Cost is acceptable for page-sized inputs.)
    flags = 0 if vocab.case_sensitive else re.IGNORECASE

    for token, replacement, rule in vocab.rules:
        pat = re.compile(rf"(?<![A-Za-z0-9])({re.escape(token)})(?![A-Za-z0-9])", flags)

        out_chunks: list[str] = []
        pos = 0
        keep_spans = _keep_verbatim_spans(text, vocab)

        # Special handling for doc_prefix: preserve the suffix that follows
        # the matched prefix as a "Doc <suffix>" reference.
        if rule == "doc_prefix":
            # The prefix matches e.g. "STP-" or "DEP " — capture the prefix AND
            # the following identifier token (alphanumerics, dots, dashes,
            # underscores, slashes) so we can emit "<id> Doc <suffix>".
            pat = re.compile(
                rf"(?<![A-Za-z0-9])({re.escape(token)})([A-Za-z0-9][A-Za-z0-9._\-\/]*)?",
                flags,
            )

        for m in pat.finditer(text):
            ms, me = m.start(), m.end()
            if _spans_overlap(ms, me, keep_spans):
                counts["skipped_keep_verbatim"] += 1
                continue
            # Append text before the match
            out_chunks.append(text[pos:ms])
            if rule == "doc_prefix":
                suffix = (m.group(2) or "").strip()
                if suffix:
                    out_chunks.append(f"{replacement} {suffix}")
                else:
                    out_chunks.append(replacement)
            else:
                out_chunks.append(replacement)
            counts[rule] += 1
            pos = me

        out_chunks.append(text[pos:])
        text = "".join(out_chunks)

    return text, counts


def load_vocab(path: Path) -> Vocab:
    try:
        raw = yaml.safe_load(path.read_text())
    except FileNotFoundError:
        print(f"redact_industry_sources: vocab not found: {path}", file=sys.stderr)
        sys.exit(2)
    except yaml.YAMLError as e:
        print(f"redact_industry_sources: invalid YAML in {path}: {e}", file=sys.stderr)
        sys.exit(3)
    try:
        return Vocab(raw)
    except ValueError as e:
        print(f"redact_industry_sources: invalid vocab schema: {e}", file=sys.stderr)
        sys.exit(3)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Redact identifying source-org names in PDF2MD page Markdown.")
    ap.add_argument("page_md", type=Path, help="Markdown page file to redact")
    ap.add_argument("--vocab", type=Path, required=True, help="Path to industry_sources_vocab.yaml")
    ap.add_argument("--out", type=Path, default=None, help="Output path (default: in-place)")
    ap.add_argument("--dry-run", action="store_true", help="Print stats; do not write")
    ap.add_argument("--report", type=Path, default=None, help="Optional JSON report path")
    args = ap.parse_args(argv)

    if not args.page_md.exists():
        print(f"redact_industry_sources: file not found: {args.page_md}", file=sys.stderr)
        return 2

    vocab = load_vocab(args.vocab)
    src = args.page_md.read_text()
    redacted, counts = redact(src, vocab)

    changed = redacted != src
    out_path = args.out if args.out is not None else args.page_md
    if not args.dry_run and changed:
        out_path.write_text(redacted)

    report = {
        "file": str(args.page_md),
        "out": str(out_path),
        "bytes_in": len(src),
        "bytes_out": len(redacted),
        "changed": changed,
        "dry_run": args.dry_run,
        "counts": counts,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2))
    print(f"{args.page_md.name}: redacted "
          f"(alias={counts['alias']}, doc_prefix={counts['doc_prefix']}, "
          f"site={counts['site']}, kept={counts['skipped_keep_verbatim']}, "
          f"changed={changed})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
