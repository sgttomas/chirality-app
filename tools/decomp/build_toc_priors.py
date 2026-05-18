#!/usr/bin/env python3
"""Build cross-source TOC reconciliation priors for DOMAIN_DECOMP Phase 3.

Read each source's `<book>_skeleton.json` (or `.reviewed.json` if Gate 1.5
overrides are applied) and emit two artifacts:

  cross_source_toc_matrix.md
    Human-readable per-source TOC trees printed side by side with depth-2
    (chapter) and depth-3 (section) granularity, followed by a candidate
    alignment table that lists section pairs across sources whose titles
    share two or more content keywords. This is the prior input that
    DOMAIN_DECOMP's Phase-3 persona uses when proposing flat categories
    as a reconciliation of author structures.

  cross_source_toc_matrix.csv
    Machine-readable alignment candidates: one row per section pair from
    different sources with shared_keywords (semicolon-separated), shared
    count, and Jaccard similarity. Sortable / filterable downstream.

The tool is fully deterministic — no semantic alignment, no NLP. It is a
keyword-overlap prior, not a clustering decision.

Usage:
  python3 tools/decomp/build_toc_priors.py \\
      --skeleton <book1>_skeleton.json \\
      --skeleton <book2>_skeleton.json \\
      --skeleton <book3>_skeleton.json \\
      --output-md cross_source_toc_matrix.md \\
      --output-csv cross_source_toc_matrix.csv \\
      [--min-shared 2] \\
      [--max-depth 3]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "in", "on", "for", "to", "with",
    "from", "by", "at", "is", "are", "be", "as", "into", "due", "over",
    "under", "between", "this", "that", "these", "those", "section",
    "chapter", "part", "appendix", "introduction", "preface", "references",
    "table", "figure", "fig", "eq", "equation", "summary", "general",
    "basic", "other", "various", "single", "small", "large", "long",
    "short", "low", "high", "many", "more", "less", "such", "their",
    "they", "them", "its", "it", "we", "i", "you", "your", "our", "us",
}
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z\-]*[A-Za-z]|[A-Za-z]")


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skeleton", action="append", required=True, type=Path,
                   help="Per-source skeleton JSON (repeat per source)")
    p.add_argument("--output-md", required=True, type=Path)
    p.add_argument("--output-csv", required=True, type=Path)
    p.add_argument("--min-shared", type=int, default=2,
                   help="Minimum shared keyword count to emit a pair (default 2)")
    p.add_argument("--max-depth", type=int, default=3,
                   help="Maximum section depth to include (default 3)")
    return p.parse_args()


def tokenize(title: str) -> set[str]:
    tokens = TOKEN_RE.findall(title.lower())
    return {t for t in tokens if t not in STOPWORDS and len(t) > 2}


def load_skeleton(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def in_scope_section(s: dict, max_depth: int) -> bool:
    if s["depth"] > max_depth:
        return False
    if s.get("is_front_matter") or s.get("is_back_matter"):
        return False
    if not s.get("in_scope_default", True):
        return False
    return True


def render_toc_md(skeletons: list[dict], max_depth: int) -> str:
    out: list[str] = ["# Cross-Source TOC Matrix\n"]
    for sk in skeletons:
        out.append(f"## {sk['source']}\n")
        out.append(f"_Prefix: `{sk['source_prefix']}` · {len(sk['sections'])} sections · "
                   f"{sum(1 for s in sk['sections'] if s.get('in_scope_default', True))} in scope_\n")
        out.append("")
        for s in sk["sections"]:
            if not in_scope_section(s, max_depth):
                continue
            indent = "  " * (s["depth"] - 1)
            pages = ""
            if s.get("page_first") and s.get("page_last"):
                pages = f" _(pp. {s['page_first']}–{s['page_last']})_"
            tokens = sum(s.get("estimated_md_tokens", 0) for s in [s])
            out.append(
                f"{indent}- **{s['section_id']}** {s['title']}{pages} — "
                f"~{tokens} MD tokens"
            )
        out.append("")
    return "\n".join(out)


def alignment_pairs(
    skeletons: list[dict],
    min_shared: int,
    max_depth: int,
) -> list[dict]:
    """Compute keyword-overlap-based alignment pairs across distinct sources."""
    # Build per-section token sets
    section_meta: list[dict] = []
    for sk in skeletons:
        for s in sk["sections"]:
            if not in_scope_section(s, max_depth):
                continue
            tokens = tokenize(s["title"])
            if not tokens:
                continue
            section_meta.append({
                "source": sk["source"],
                "source_prefix": sk["source_prefix"],
                "section_id": s["section_id"],
                "title": s["title"],
                "depth": s["depth"],
                "tokens": tokens,
            })
    pairs: list[dict] = []
    n = len(section_meta)
    for i in range(n):
        a = section_meta[i]
        for j in range(i + 1, n):
            b = section_meta[j]
            if a["source"] == b["source"]:
                continue
            shared = a["tokens"] & b["tokens"]
            if len(shared) < min_shared:
                continue
            union = a["tokens"] | b["tokens"]
            jaccard = len(shared) / len(union) if union else 0.0
            pairs.append({
                "source_a": a["source"],
                "section_a_id": a["section_id"],
                "title_a": a["title"],
                "source_b": b["source"],
                "section_b_id": b["section_id"],
                "title_b": b["title"],
                "shared_keywords": ";".join(sorted(shared)),
                "shared_count": len(shared),
                "jaccard": round(jaccard, 4),
            })
    pairs.sort(key=lambda r: (-r["shared_count"], -r["jaccard"], r["source_a"], r["section_a_id"]))
    return pairs


def main() -> int:
    args = parse_args()
    skeletons: list[dict] = []
    for sk_path in args.skeleton:
        if not sk_path.exists():
            return fail(f"missing skeleton: {sk_path}")
        skeletons.append(load_skeleton(sk_path))

    toc_md = render_toc_md(skeletons, args.max_depth)
    pairs = alignment_pairs(skeletons, args.min_shared, args.max_depth)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(toc_md, encoding="utf-8")

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    if pairs:
        with args.output_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(pairs[0].keys()))
            writer.writeheader()
            for row in pairs:
                writer.writerow(row)
    else:
        # Still write a header-only CSV
        args.output_csv.write_text(
            "source_a,section_a_id,title_a,source_b,section_b_id,title_b,"
            "shared_keywords,shared_count,jaccard\n",
            encoding="utf-8",
        )

    print(
        f"sources={len(skeletons)} pairs={len(pairs)} "
        f"md={args.output_md.name} csv={args.output_csv.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
