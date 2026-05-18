"""Markdown tokenizer for the Gate 1.5-P extraction comparator.

Splits per-page Markdown into a typed stream of tokens that the
comparator (`compare_extracts.py`) can align structurally:

  - `ProseLine(text)`            — a non-empty prose paragraph line.
  - `EquationBlock(latex)`       — a `$$...$$` display equation block
                                   (stripped LaTeX content, no fences).
  - `AssetRef(kind, target)`     — a Markdown image/link reference to an
                                   embedded asset (e.g. `![](figures/...)`).
  - `Placeholder(kind, caption)` — a 1.5-P-style placeholder produced by
                                   `domain-prose-validate`: `[FIGURE: caption]`,
                                   `[TABLE: caption]`, `[IMAGE: caption]`.
  - `Blank()`                    — explicit blank-line separator.

Display equation blocks are recognized first (they may span lines).
Asset references and placeholders are recognized on their own line.
Everything else becomes a `ProseLine` after surrounding whitespace is
trimmed. Markdown headings, lists, and other structural prefixes are
preserved verbatim inside the `ProseLine` text — the comparator's prose
normalizer is responsible for downstream cleanup.

The tokenizer is intentionally line-oriented and conservative: when in
doubt, classify as `ProseLine`. The downstream comparator handles the
fuzz of whether two ProseLines match modulo whitespace.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ProseLine:
    text: str


@dataclass(frozen=True)
class EquationBlock:
    latex: str


@dataclass(frozen=True)
class AssetRef:
    kind: str       # "fig" | "tbl" | "img" | "unknown"
    target: str     # the link target as written


@dataclass(frozen=True)
class Placeholder:
    kind: str       # "fig" | "tbl" | "img"
    caption: str


@dataclass(frozen=True)
class Blank:
    pass


Token = ProseLine | EquationBlock | AssetRef | Placeholder | Blank


_DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_PLACEHOLDER_RE = re.compile(
    r"^\s*\[(FIGURE|TABLE|IMAGE)\s*:\s*(.*?)\s*\]\s*$",
    re.IGNORECASE,
)
_MD_IMAGE_RE = re.compile(r"^\s*!\[[^\]]*\]\(([^)]+)\)\s*$")
_MD_LINK_RE = re.compile(r"^\s*\[[^\]]+\]\(([^)]+)\)\s*$")


_PLACEHOLDER_KIND_MAP = {
    "FIGURE": "fig",
    "TABLE": "tbl",
    "IMAGE": "img",
}


def _classify_asset_target(target: str) -> str:
    """Best-effort kind from a link/image target path."""
    t = target.lower()
    if "/figures/" in t or t.startswith("figures/") or t.endswith(".fig"):
        return "fig"
    if "/tables/" in t or t.startswith("tables/") or t.endswith(".xlsx") or t.endswith(".csv"):
        return "tbl"
    if "/images/" in t or t.startswith("images/"):
        return "img"
    return "unknown"


def tokenize(md_text: str) -> list[Token]:
    """Split `md_text` into a flat token stream.

    Display equations (`$$...$$`) are pulled out first regardless of
    line position. The remaining text is processed line by line.
    """
    tokens: list[Token] = []
    cursor = 0
    for m in _DISPLAY_RE.finditer(md_text):
        if m.start() > cursor:
            _tokenize_lines(md_text[cursor:m.start()], tokens)
        tokens.append(EquationBlock(latex=m.group(1).strip()))
        cursor = m.end()
    if cursor < len(md_text):
        _tokenize_lines(md_text[cursor:], tokens)
    return tokens


def _tokenize_lines(chunk: str, out: list[Token]) -> None:
    for raw in chunk.splitlines():
        stripped = raw.strip()
        if not stripped:
            if out and not isinstance(out[-1], Blank):
                out.append(Blank())
            continue
        m = _PLACEHOLDER_RE.match(raw)
        if m:
            kind = _PLACEHOLDER_KIND_MAP[m.group(1).upper()]
            out.append(Placeholder(kind=kind, caption=m.group(2).strip()))
            continue
        m = _MD_IMAGE_RE.match(raw)
        if m:
            tgt = m.group(1).strip()
            out.append(AssetRef(kind=_classify_asset_target(tgt), target=tgt))
            continue
        m = _MD_LINK_RE.match(raw)
        if m:
            tgt = m.group(1).strip()
            kind = _classify_asset_target(tgt)
            if kind != "unknown":
                out.append(AssetRef(kind=kind, target=tgt))
                continue
        out.append(ProseLine(text=stripped))
