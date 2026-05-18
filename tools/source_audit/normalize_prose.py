"""Deterministic prose normalization for the Gate 1.5-P comparator.

Two VLM extractions of the same page will agree semantically while
disagreeing on a parade of cosmetic differences (smart vs. straight
quotes, ligatures, soft hyphens, multi-space, line-break hyphenation).
This module collapses those differences so the comparator can call out
genuine prose divergences without drowning in noise.

The normalization is intentionally lossy: it strips information the
comparator does not care about (typography, layout-induced whitespace,
case-only differences are NOT collapsed — those can be real). Use only
on prose-class text.
"""
from __future__ import annotations

import re
import unicodedata


# Ligatures that NFKC doesn't always decompose (FB00-FB06 region).
_LIGATURES: dict[str, str] = {
    "ﬀ": "ff",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬅ": "ft",
    "ﬆ": "st",
}

# Smart quotes / dashes → ASCII equivalents.
_TYPOGRAPHY: dict[str, str] = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-",  # en dash
    "—": "-",  # em dash
    "−": "-",  # minus sign
    " ": " ",  # nbsp
    " ": " ",  # thin space
    "​": "",   # zero-width space
    "…": "...",
}

_SOFT_HYPHEN_RE = re.compile(r"­")
_LINEBREAK_HYPHEN_RE = re.compile(r"(\w+)-\s*\n\s*(\w+)")
_MULTISPACE_RE = re.compile(r"[ \t]+")


def _apply_charmap(text: str, charmap: dict[str, str]) -> str:
    if not any(c in text for c in charmap):
        return text
    return "".join(charmap.get(c, c) for c in text)


def normalize_prose(text: str) -> str:
    """Return a normalized form of `text` suitable for prose comparison.

    Pipeline:
      1. NFKC Unicode normalization.
      2. Strip soft hyphens (U+00AD).
      3. De-hyphenate line-break hyphenations (`prog-\\nress` → `progress`).
      4. Map ligatures (`ﬁ` → `fi`, etc.).
      5. Map smart quotes / dashes / ellipsis / nbsp / thin spaces.
      6. Collapse runs of spaces/tabs to a single space.
      7. Strip leading/trailing whitespace on each line.
      8. Strip trailing whitespace from the final result.
    """
    out = unicodedata.normalize("NFKC", text)
    out = _SOFT_HYPHEN_RE.sub("", out)
    out = _LINEBREAK_HYPHEN_RE.sub(r"\1\2", out)
    out = _apply_charmap(out, _LIGATURES)
    out = _apply_charmap(out, _TYPOGRAPHY)
    out = _MULTISPACE_RE.sub(" ", out)
    lines = [ln.strip() for ln in out.split("\n")]
    return "\n".join(lines).strip()


def normalize_for_diff(text: str) -> str:
    """Stronger normalization for the inner equality test of two prose lines.

    Adds on top of `normalize_prose`:
      - All whitespace (including newlines) collapsed to single spaces.
      - Trailing punctuation stripped from the end of the comparison
        (commas, periods, semicolons) so a line that one extract terminates
        with a period and another doesn't doesn't show up as a diff.
    """
    out = normalize_prose(text)
    out = re.sub(r"\s+", " ", out).strip()
    out = out.rstrip(".,;:")
    return out
