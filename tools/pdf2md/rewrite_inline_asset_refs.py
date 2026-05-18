#!/usr/bin/env python3
"""
rewrite_inline_asset_refs.py
Rewrite inline figure/table/image references in a per-page Markdown so they
point at materialized PDF2MD assets, replacing the prior dead-link
"[FIGURE: ...]" / "![FIG. ...]" / "[NAME logo]" placeholders that the
pdf2md-page skill emits.

Usage:
    python3 rewrite_inline_asset_refs.py \\
      --page-md page_0003.md \\
      --materialized-manifest page_0003_assets_materialized.json \\
      --output-md page_0003.anchored.md

Inputs:
    --page-md                Cleaned per-page Markdown produced by Phase 3.
    --materialized-manifest  Per-page materialization manifest written by
                             materialize_page_assets.py (contains kind,
                             ordinal, png_path, csv_path, caption per asset).
    --output-md              Anchored per-page Markdown to write.

Outputs:
    Anchored Markdown in which the inline placeholders for figures, tables,
    and oddball images are rewritten in-place to use the materialized asset
    paths. Any materialized assets that did not match an inline placeholder
    are emitted in a trailing "Unmatched Page Assets" block bounded by
    PDF2MD-ASSETS:BEGIN/END comments. If every materialized asset is matched
    inline, no trailing block is emitted.

Behavior:
    - Inline placeholders are detected per (page, kind) in document reading
      order. The Nth match for a given kind is bound to ordinal N from the
      materialization manifest (kind in {fig, tbl, img}).
    - If there are more inline placeholders than materialized assets for a
      given kind, surplus placeholders are left untouched and a per-page
      issue is reported on stderr.
    - If there are more materialized assets than inline placeholders, the
      surplus assets land in the trailing "Unmatched Page Assets" block.
    - Existing PDF2MD-ASSETS:BEGIN..END blocks in the input are stripped
      before rewriting.

Example:
    python3 tools/pdf2md/rewrite_inline_asset_refs.py \\
      --page-md work/page_0003.md \\
      --materialized-manifest work/page_0003_assets_materialized.json \\
      --output-md work/page_0003.anchored.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ASSET_BLOCK_RE = re.compile(
    r"\n*<!-- PDF2MD-ASSETS:BEGIN page=\d+ -->.*?<!-- PDF2MD-ASSETS:END page=\d+ -->\n*",
    re.DOTALL,
)

# Body matcher that allows one level of nested [..] (e.g. citation [1]) inside
# the placeholder marker. Without this, "[FIGURE: ... [1].]" stops at the
# citation's "]" and breaks the rewrite.
_BAL = r"(?:[^\[\]\n]|\[[^\[\]\n]*\])"
_BODY = rf"{_BAL}+"

# CANONICAL placeholder patterns — exactly what skills/pdf2md-page/SKILL.md
# RULE 8 specifies the pdf2md-page skill must emit. Drift patterns (e.g.
# `![Fig. ...](...)` markdown-image syntax, bare-bracketed `[Fig. 1.1 ...]`
# without the FIGURE: prefix) are NOT matched here — surfacing those as
# warnings via DRIFT_PATTERNS forces the skill back to the contract instead
# of silently rewriting non-compliant placeholders.
INLINE_PATTERNS = [
    # [FIGURE: Fig. 1.1 caption with [1] citation.]
    ("fig", re.compile(rf"\[FIGURE:\s*(?P<body>{_BODY})\]")),
    # [TABLE: Table 1 caption.] — immediately above GFM/HTML transcription per RULE 3.
    ("tbl", re.compile(rf"\[TABLE:\s*(?P<body>{_BODY})\]")),
    # [<descriptor> <suffix>] where suffix is one of the RULE 8 oddball keywords.
    ("img", re.compile(r"\[(?P<body>[A-Za-z][\w\s&.\-']*?\s+(?:logo|emblem|seal|cover|photograph|photo|image))\]")),
]

# Drift patterns: shapes the pdf2md-page skill is forbidden from emitting per
# RULE 8 in skills/pdf2md-page/SKILL.md. When detected, the rewriter emits
# a warning to stderr (it does NOT rewrite them — that would mask the skill
# defect). Listed here so the patrol surfaces drift instead of swallowing it.
# Body matches the same nested-bracket-aware shape as canonical placeholders.
_FIG_PREFIX = r"(?:fig\.?|figure)"
_TBL_PREFIX = r"(?:tbl\.?|table)"
DRIFT_PATTERNS = [
    ("fig (markdown-image syntax — should be `[FIGURE: ...]`)",
     re.compile(rf"!\[(?:{_FIG_PREFIX})\b{_BAL}*\](?:\([^\)]*\))?", re.IGNORECASE)),
    ("fig (bare bracketed without FIGURE: prefix or lowercase prefix)",
     re.compile(rf"(?<!!)\[(?:{_FIG_PREFIX})\s+[\d\.\-]{_BAL}*\]", re.IGNORECASE)),
    ("tbl (markdown-image syntax — should be `[TABLE: ...]`)",
     re.compile(rf"!\[(?:{_TBL_PREFIX})\b{_BAL}*\](?:\([^\)]*\))?", re.IGNORECASE)),
    ("tbl (bare bracketed without TABLE: prefix or lowercase prefix)",
     re.compile(rf"(?<!!)\[(?:{_TBL_PREFIX})\s+[\d\.\-]{_BAL}*\]", re.IGNORECASE)),
    ("tbl (legacy `[CSV](...)` link — tables now render as `[XLSX](...)`)",
     re.compile(r"\[CSV\]\([^)]*\)")),
]


def detect_drift(text: str) -> list[tuple[str, str]]:
    """Return list of (label, snippet) for any non-canonical placeholders detected."""
    hits: list[tuple[str, str]] = []
    for label, pattern in DRIFT_PATTERNS:
        for m in pattern.finditer(text):
            snippet = m.group(0)
            if len(snippet) > 80:
                snippet = snippet[:77] + "..."
            hits.append((label, snippet))
    return hits


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite inline asset placeholders to materialized asset paths.")
    parser.add_argument("--page-md", required=True)
    parser.add_argument("--materialized-manifest", required=True)
    parser.add_argument("--output-md", required=True)
    return parser.parse_args()


def escape_markdown_label(value: str) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def escape_bold_text(value: str) -> str:
    text = escape_markdown_label(value)
    return text.replace("*", "\\*").replace("_", "\\_")


def strip_existing_asset_block(text: str) -> str:
    return ASSET_BLOCK_RE.sub("\n\n", text).rstrip()


def load_materialized(path: Path) -> tuple[int, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    page = int(data.get("page", 0))
    raw_assets = data.get("assets", [])
    if not isinstance(raw_assets, list):
        raise SystemExit(f"ERROR: materialized manifest has no assets list: {path}")
    valid = [
        asset for asset in raw_assets
        if isinstance(asset, dict)
        and asset.get("status") in {"materialized", "degraded"}
        and asset.get("kind") in {"fig", "tbl", "img"}
    ]
    valid.sort(key=lambda asset: (asset.get("kind", ""), int(asset.get("ordinal") or 0)))
    return page, valid


def find_inline_matches(text: str) -> list[tuple[int, int, str, str]]:
    """Return list of (start, end, kind, body) for every inline placeholder, sorted by position."""
    matches: list[tuple[int, int, str, str]] = []
    occupied: list[tuple[int, int]] = []
    for kind, pattern in INLINE_PATTERNS:
        for match in pattern.finditer(text):
            span = match.span()
            if any(not (span[1] <= s or span[0] >= e) for s, e in occupied):
                continue
            body = match.group("body").strip()
            matches.append((span[0], span[1], kind, body))
            occupied.append(span)
    matches.sort()
    return matches


def build_inline_replacement(asset: dict, body_text: str) -> str:
    caption = body_text or str(asset.get("caption") or asset.get("asset_id") or "asset")
    label = escape_markdown_label(caption)
    if asset["kind"] == "tbl":
        png_path = asset.get("png_path") or ""
        xlsx_path = asset.get("xlsx_path") or ""
        bold = escape_bold_text(caption)
        links = []
        if xlsx_path:
            links.append(f"[XLSX]({xlsx_path})")
        if png_path:
            links.append(f"[source crop]({png_path})")
        if asset.get("needs_extraction"):
            links.append("needs_extraction")
        suffix = " and ".join(links) if links else "asset pending"
        return f"> **Table - {bold}** - see {suffix}"
    target = asset.get("png_path") or ""
    return f"![{label}]({target})"


def build_unmatched_block(page: int, unmatched: list[dict]) -> str:
    if not unmatched:
        return ""
    lines = [
        f"<!-- PDF2MD-ASSETS:BEGIN page={page} -->",
        "",
        "#### Unmatched Page Assets",
        "",
    ]
    for asset in unmatched:
        caption = asset.get("caption") or asset.get("asset_id") or "asset"
        if asset.get("kind") == "tbl":
            bold = escape_bold_text(caption)
            png_path = asset.get("png_path") or ""
            xlsx_path = asset.get("xlsx_path") or ""
            parts = []
            if xlsx_path:
                parts.append(f"[XLSX]({xlsx_path})")
            if png_path:
                parts.append(f"[source crop]({png_path})")
            if asset.get("needs_extraction"):
                parts.append("needs_extraction")
            suffix = " and ".join(parts) if parts else "asset pending"
            lines.append(f"> **Table - {bold}** - see {suffix}")
        else:
            label = escape_markdown_label(caption)
            target = asset.get("png_path") or ""
            lines.append(f"![{label}]({target})")
        lines.append("")
    lines.append(f"<!-- PDF2MD-ASSETS:END page={page} -->")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    page_md_path = Path(args.page_md).resolve()
    manifest_path = Path(args.materialized_manifest).resolve()
    output_md_path = Path(args.output_md).resolve()

    for path in (page_md_path, manifest_path):
        if not path.is_file():
            print(f"ERROR: missing input: {path}", file=sys.stderr)
            return 2

    page, assets = load_materialized(manifest_path)
    text = strip_existing_asset_block(page_md_path.read_text(encoding="utf-8"))

    # Patrol for drift: non-canonical placeholders the skill is forbidden from
    # emitting per RULE 8. Surface to stderr but do NOT rewrite — that would
    # mask the skill defect and let drift accumulate silently.
    drift = detect_drift(text)
    if drift:
        print(
            f"WARNING: page={page} has {len(drift)} non-canonical placeholder(s) "
            f"the rewriter is not configured to handle. The pdf2md-page skill is "
            f"emitting drift from skills/pdf2md-page/SKILL.md RULE 8. Examples:",
            file=sys.stderr,
        )
        for label, snippet in drift[:5]:
            print(f"  {label}: {snippet!r}", file=sys.stderr)

    inline_matches = find_inline_matches(text)

    by_kind: dict[str, list[dict]] = {"fig": [], "tbl": [], "img": []}
    for asset in assets:
        by_kind[asset["kind"]].append(asset)

    consumed_indices: dict[str, int] = {"fig": 0, "tbl": 0, "img": 0}
    matched_assets: list[dict] = []
    surplus_inline: list[tuple[str, str]] = []

    rewritten_segments: list[tuple[int, int, str]] = []
    for start, end, kind, body in inline_matches:
        idx = consumed_indices[kind]
        if idx >= len(by_kind[kind]):
            surplus_inline.append((kind, body))
            continue
        asset = by_kind[kind][idx]
        consumed_indices[kind] = idx + 1
        matched_assets.append(asset)
        rewritten_segments.append((start, end, build_inline_replacement(asset, body)))

    rewritten_segments.sort(reverse=True)
    output_text = text
    for start, end, replacement in rewritten_segments:
        output_text = output_text[:start] + replacement + output_text[end:]

    matched_ids = {(a["kind"], a.get("ordinal")) for a in matched_assets}
    unmatched_assets = [
        a for a in assets if (a["kind"], a.get("ordinal")) not in matched_ids
    ]

    output_text = output_text.rstrip() + "\n"
    block = build_unmatched_block(page, unmatched_assets)
    if block:
        output_text = output_text + "\n" + block + "\n"

    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    output_md_path.write_text(output_text, encoding="utf-8")

    print(f"page={page}")
    print(f"materialized_assets={len(assets)}")
    print(f"inline_matches={len(inline_matches)}")
    print(f"rewritten_inline={len(matched_assets)}")
    print(f"unmatched_assets={len(unmatched_assets)}")
    print(f"surplus_inline_placeholders={len(surplus_inline)}")
    if surplus_inline:
        print("surplus_inline:")
        for kind, body in surplus_inline[:10]:
            print(f"  - kind={kind} body={body[:80]!r}")
    print(f"output={output_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
