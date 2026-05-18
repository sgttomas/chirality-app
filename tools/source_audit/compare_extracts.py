"""Deterministic three-class compare for the Gate 1.5-P prefilter.

Takes two Markdown extracts of the same page (the original from
`pdf2md-page-assets`, and the 1.5-P re-extract from
`domain-prose-validate`) and emits a structured diff covering:

  - **prose** — line-level divergences after `normalize_prose`.
                Strict equality after normalization is required;
                anything else is a `prose_hunk` finding.
  - **equations** — first a structural compare (count + position),
                then for matched pairs a canonicalize-then-content compare.
                Structural divergence → `equation_structural_fail`.
                Content divergence under canonicalization →
                `equation_content_proposal` (an edit proposal to surface
                at 1.5-E for human adjudication, never silently applied).
  - **assets** — structural compare of asset references and placeholders
                (one-to-one positional match by kind: fig/tbl/img).
                Structural divergence → `asset_structural_fail`.
                Caption divergence → `caption_note` (informational).

**1.5-P is purely additive.** This module NEVER writes a verification
or exemption signal; it only routes attention TO content. A match in
any class is silent — both extracts can be wrong about the same
printed content. See `agents/AGENT_DOMAIN_DECOMP.md` Gate 1.5-P for the
full doctrine.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from tools.source_audit.canonicalize_latex import canonicalize_latex_v1
from tools.source_audit.normalize_prose import normalize_for_diff
from tools.source_audit.sidecar import content_hash
from tools.source_audit.tokenize_md import (
    AssetRef,
    Blank,
    EquationBlock,
    Placeholder,
    ProseLine,
    Token,
    tokenize,
)


@dataclass(frozen=True)
class ProseHunk:
    page: int
    position: int           # index in the original token stream
    original: str
    reextract: str


@dataclass(frozen=True)
class EquationStructuralFail:
    page: int
    reason: str             # "count_mismatch" | "position_mismatch"
    original_count: int
    reextract_count: int


@dataclass(frozen=True)
class EquationContentProposal:
    page: int
    position: int           # ordinal among display equations on this page
    equation_hash: str      # content_hash of the *original* LaTeX (matches
                            # the equation_audit per-equation key suffix)
    proposal_hash: str      # content_hash of the canonicalized re-extract
    original_latex: str
    proposed_latex: str
    canonical_original: str
    canonical_proposed: str


@dataclass(frozen=True)
class AssetStructuralFail:
    page: int
    kind: str               # "fig" | "tbl" | "img"
    reason: str             # "count_mismatch" | "position_mismatch"
    original_count: int
    reextract_count: int


@dataclass(frozen=True)
class CaptionNote:
    page: int
    kind: str
    position: int           # ordinal among assets of this kind on the page
    original_caption: str
    reextract_caption: str


@dataclass
class PageComparison:
    page: int
    prose_hunks: list[ProseHunk] = field(default_factory=list)
    equation_structural_fails: list[EquationStructuralFail] = field(default_factory=list)
    equation_content_proposals: list[EquationContentProposal] = field(default_factory=list)
    asset_structural_fails: list[AssetStructuralFail] = field(default_factory=list)
    caption_notes: list[CaptionNote] = field(default_factory=list)

    @property
    def has_structural_fails(self) -> bool:
        return bool(self.equation_structural_fails or self.asset_structural_fails)

    def to_dict(self) -> dict:
        def _asdict_list(items):
            return [_dc_to_dict(i) for i in items]
        return {
            "page": self.page,
            "prose_hunks": _asdict_list(self.prose_hunks),
            "equation_structural_fails": _asdict_list(self.equation_structural_fails),
            "equation_content_proposals": _asdict_list(self.equation_content_proposals),
            "asset_structural_fails": _asdict_list(self.asset_structural_fails),
            "caption_notes": _asdict_list(self.caption_notes),
            "has_structural_fails": self.has_structural_fails,
        }


def _dc_to_dict(obj) -> dict:
    return {k: getattr(obj, k) for k in obj.__dataclass_fields__}


def _prose_tokens(toks: list[Token]) -> list[ProseLine]:
    return [t for t in toks if isinstance(t, ProseLine)]


def _equation_tokens(toks: list[Token]) -> list[EquationBlock]:
    return [t for t in toks if isinstance(t, EquationBlock)]


def _asset_tokens(toks: list[Token]) -> list[tuple[str, str]]:
    """Return (kind, caption_or_target) for every asset-like token in order."""
    out: list[tuple[str, str]] = []
    for t in toks:
        if isinstance(t, AssetRef):
            out.append((t.kind, t.target))
        elif isinstance(t, Placeholder):
            out.append((t.kind, t.caption))
    return out


def compare_page(
    original_md: str,
    reextract_md: str,
    page_num: int,
    latex_canonicalizer: Callable[[str], str] = canonicalize_latex_v1,
) -> PageComparison:
    """Run the three-class compare on one `(original, reextract)` pair.

    The original side is treated as the anchor for keys (equation hashes,
    asset positions). The re-extract supplies the proposal content.
    """
    cmp = PageComparison(page=page_num)
    orig_toks = tokenize(original_md)
    re_toks = tokenize(reextract_md)

    # --- prose -------------------------------------------------------------
    op = _prose_tokens(orig_toks)
    rp = _prose_tokens(re_toks)
    # zip pairwise; flag length mismatches by adding hunks for the tail.
    for idx in range(max(len(op), len(rp))):
        o_text = op[idx].text if idx < len(op) else ""
        r_text = rp[idx].text if idx < len(rp) else ""
        if normalize_for_diff(o_text) != normalize_for_diff(r_text):
            cmp.prose_hunks.append(ProseHunk(
                page=page_num, position=idx,
                original=o_text, reextract=r_text,
            ))

    # --- equations: structural first, then content proposals --------------
    oe = _equation_tokens(orig_toks)
    re_ = _equation_tokens(re_toks)
    if len(oe) != len(re_):
        cmp.equation_structural_fails.append(EquationStructuralFail(
            page=page_num, reason="count_mismatch",
            original_count=len(oe), reextract_count=len(re_),
        ))
    else:
        for idx, (o, r) in enumerate(zip(oe, re_)):
            canon_o = latex_canonicalizer(o.latex)
            canon_r = latex_canonicalizer(r.latex)
            if canon_o != canon_r:
                cmp.equation_content_proposals.append(EquationContentProposal(
                    page=page_num, position=idx,
                    equation_hash=content_hash(o.latex),
                    proposal_hash=content_hash(canon_r),
                    original_latex=o.latex,
                    proposed_latex=r.latex,
                    canonical_original=canon_o,
                    canonical_proposed=canon_r,
                ))

    # --- assets: structural (per kind), then caption notes -----------------
    oa = _asset_tokens(orig_toks)
    ra = _asset_tokens(re_toks)
    for kind in ("fig", "tbl", "img"):
        o_kind = [(p, c) for p, (k, c) in enumerate(oa) if k == kind]
        r_kind = [(p, c) for p, (k, c) in enumerate(ra) if k == kind]
        if len(o_kind) != len(r_kind):
            cmp.asset_structural_fails.append(AssetStructuralFail(
                page=page_num, kind=kind, reason="count_mismatch",
                original_count=len(o_kind), reextract_count=len(r_kind),
            ))
            continue
        for idx, ((_, o_cap), (_, r_cap)) in enumerate(zip(o_kind, r_kind)):
            if normalize_for_diff(o_cap) != normalize_for_diff(r_cap):
                cmp.caption_notes.append(CaptionNote(
                    page=page_num, kind=kind, position=idx,
                    original_caption=o_cap, reextract_caption=r_cap,
                ))

    return cmp
