"""Textual LaTeX canonicalization (v1) for Gate 1.5-P equation compare.

Two VLM extractions of the same display equation can canonicalize to the
same LaTeX while differing in cosmetic ways — `\\frac` vs. `\\dfrac`,
`\\mathrm{x}` vs. `{\\rm x}`, brace-around-single-token, optional thin
spaces, redundant `\\left`/`\\right`. This v1 canonicalizer collapses
those equivalences using pure regex/string substitution.

v2 (AST-based) is deferred until empirical proposal-cosmesis rate
demands it. The plan calls for adopting v2 only if a sample of
proposals on the first source shows >30% cosmetic content.

The canonicalizer is intentionally CONSERVATIVE — it never rewrites
LaTeX whose semantic equivalence would require parsing. When in doubt,
leave the original form so a genuine content difference still shows.
"""
from __future__ import annotations

import re


# Order matters: some rules consume tokens others would otherwise rewrite.
_FRAC_DFRAC_RE = re.compile(r"\\dfrac\b")
_TFRAC_FRAC_RE = re.compile(r"\\tfrac\b")
_TAG_RE = re.compile(r"\\tag\s*\{[^{}]*\}")
_MATHRM_BRACE_RE = re.compile(r"\\mathrm\s*\{([^{}]*)\}")
_RM_BRACE_RE = re.compile(r"\{\s*\\rm\s+([^{}]+)\}")
_OPNAME_RE = re.compile(r"\\operatorname\s*\{([^{}]*)\}")
_THIN_SPACE_RE = re.compile(r"\\[,:;!]")
_LEFT_PAREN_RE = re.compile(r"\\left\s*([(\[|])\s*")
_RIGHT_PAREN_RE = re.compile(r"\s*\\right\s*([)\]|])")
_BRACE_SINGLE_TOKEN_RE = re.compile(r"\{([A-Za-z0-9])\}")
_MULTI_WHITESPACE_RE = re.compile(r"\s+")
_WHITESPACE_AROUND_BRACE_RE = re.compile(r"\s*([{}])\s*")
_WHITESPACE_AROUND_OPS_RE = re.compile(r"\s*([=+\-*/^_])\s*")


def canonicalize_latex_v1(latex: str) -> str:
    """Return a canonicalized form of `latex` suitable for equality compare.

    Applies in order:
      1. `\\dfrac` / `\\tfrac` → `\\frac`.
      2. `\\tag{X}` → dropped (LaTeX equation-numbering metadata, not math).
      3. `\\mathrm{X}` → `\\rm X` form (unified single style).
         Specifically: `\\mathrm{X}` and `{\\rm X}` both → `\\mathrm{X}`.
      4. `\\operatorname{X}` → `\\mathrm{X}`.
      5. Thin-space variants `\\,` / `\\:` / `\\;` / `\\!` → dropped.
      6. `\\left(` / `\\right)` (and `[]`, `||`) → bare `(` / `)`.
      7. Brace-around-single-alphanum-token `{x}` → `x` (except inside
         super/sub: `^{x}` / `_{x}` kept because removing braces there is
         non-equivalent).
      8. Whitespace fully collapsed and stripped from around braces and
         binary operators.
    """
    out = latex

    out = _FRAC_DFRAC_RE.sub(r"\\frac", out)
    out = _TFRAC_FRAC_RE.sub(r"\\frac", out)

    # Strip \tag{...} equation-numbering markers; they are LaTeX metadata
    # for the rendered equation number, not part of the math. Two extracts
    # that disagree only on \tag presence are not disagreeing on content.
    out = _TAG_RE.sub("", out)

    # Unify both `\\mathrm{X}` and `{\\rm X}` to `\\mathrm{X}`.
    out = _RM_BRACE_RE.sub(r"\\mathrm{\1}", out)
    # `\\operatorname{X}` → `\\mathrm{X}`.
    out = _OPNAME_RE.sub(r"\\mathrm{\1}", out)

    out = _THIN_SPACE_RE.sub("", out)
    out = _LEFT_PAREN_RE.sub(r"\1", out)
    out = _RIGHT_PAREN_RE.sub(r"\1", out)

    # Brace-around-single-token: strip only when the braces are clearly
    # decorative — preceded by an operator or whitespace, never preceded
    # by a backslash-command (which would make them mandatory arguments
    # like `\frac{a}{b}`) and never preceded by `^`/`_` (which would make
    # them mandatory super/subscript groups).
    out = re.sub(r"(?<=[=+\-*/(\[, ])\{([A-Za-z0-9])\}", r"\1", out)
    out = re.sub(r"^\{([A-Za-z0-9])\}", r"\1", out)

    out = _MULTI_WHITESPACE_RE.sub(" ", out)
    out = _WHITESPACE_AROUND_BRACE_RE.sub(r"\1", out)
    out = _WHITESPACE_AROUND_OPS_RE.sub(r"\1", out)
    return out.strip()


def equation_content_equal(a: str, b: str) -> bool:
    """Compare two LaTeX strings under canonicalization."""
    return canonicalize_latex_v1(a) == canonicalize_latex_v1(b)
