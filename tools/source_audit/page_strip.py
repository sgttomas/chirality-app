"""Page-grouping wrapper: source-page image on the left, chunks on the right.

Generalized from `audit_equations.py` lines 157–162. Each page-section
gets an anchor `#pN`, an `<h2>Page N (count)</h2>` heading, and a
two-column grid with the page raster sticky on the left and the
reviewable chunks stacked on the right.
"""
from __future__ import annotations


def render_page_section(
    page: int,
    png_rel: str,
    chunks_html: str,
    count: int,
    page_label: str | None = None,
) -> str:
    """Build one `<section class="page">` wrapping a sticky page image and
    a stack of reviewable chunks.

    Args:
        page:        1-indexed PDF page number.
        png_rel:     HTML-relative URL of the page raster.
        chunks_html: concatenated chunk HTML for this page.
        count:       number of chunks (rendered in the heading).
        page_label:  optional printed folio (e.g. "47", "xiv", "B-3"). When
                     supplied and different from `str(page)`, the heading
                     reads "Page <label> (PDF page <N>)". Default heading
                     ("Page N") is preserved when omitted or equal.
    """
    if page_label and page_label != str(page):
        heading_text = f'Page {page_label} <span class="count">(PDF page {page}, {count})</span>'
    else:
        heading_text = f'Page {page} <span class="count">({count})</span>'
    return (
        f'<section class="page" id="p{page}">'
        f'<h2>{heading_text}</h2>'
        f'<div class="row">'
        f'<div class="img"><img loading="lazy" src="{png_rel}"></div>'
        f'<div class="chunks">{chunks_html}</div>'
        f'</div></section>'
    )


def render_nav(pages: list[int]) -> str:
    """Top-of-page anchor nav listing every page section."""
    return " ".join(f'<a href="#p{p}">p{p}</a>' for p in pages)
