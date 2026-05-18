#!/usr/bin/env python3
"""Render one source book to a section+atom audit-pattern HTML surface.

The output HTML is the human-review surface for DOMAIN_DECOMP Gate 1.5-S
(skeleton review), Gate 2 (atom-binding review), and Gate 5 (coverage
attestation). It carries only the section outline + atom lists — the
per-kind asset surfaces (`equations.html`, `figures.html`, `tables.html`,
`images.html`) own per-asset review under their own sub-gates.

Mode behavior:
  structure       — sections + page-image strip + section-status controls
                    (Gate 1.5-S skeleton review).
  atom-review     — same as structure, plus per-section lists of atoms
                    read from `--atomic-units-csv` (Gate 2).
  coverage-review — same as structure, plus per-section CSS classes
                    derived from atom-coverage density (Gate 5).

Existing section/atom review state (verified.json / flagged.json under
--audit-dir) is read via `load_sidecar_with_fallback` semantics and
embedded into the new render so prior review is preserved across
regeneration. Inline `Fig./Table` cross-references in section bodies are
rewritten to anchors into the per-kind surfaces
(`figures.html#asset-{id}` / `tables.html#asset-{id}`).

A companion CSV (`<book>_section_nodes.csv`) is emitted for downstream
section-level retrieval indexing.

Usage:
  python3 tools/decomp/render_source_html.py \\
      --md <book>.md \\
      --asset-manifest <book>_assets_manifest.json \\
      --skeleton <book>_skeleton.json \\
      --audit-dir <book>/audit \\
      --output-html <book>/audit/<book>.html \\
      --output-section-nodes <book>_section_nodes.csv \\
      [--mode structure|atom-review|coverage-review] \\
      [--atomic-units-csv <book>_atomic_units.csv] \\
      [--pages-dir-rel pages] \\
      [--title "..."]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

INLINE_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
INLINE_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
FIG_REF_RE = re.compile(r"\b(?:Fig|Figure|FIG)\.?\s*(\d+(?:[.\-]\d+)+[A-Za-z]?)")
TABLE_REF_RE = re.compile(r"\bTable\s*(\d+(?:[.\-]\d+)+[A-Za-z]?)")
SECTION_REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)+)")
EQ_REF_RE = re.compile(r"\b(?:Eq|Equation|EQ)\.?\s*\(?(\d+(?:[.\-]\d+)+[a-z]?)\)?")
PAGE_MARKER_RE = re.compile(r"<!--\s*PDF2MD-ASSETS:(?:START|END)\s+page=(\d+)\s*-->")
FIG_CAPTION_RE = re.compile(r"(?:FIG|Figure|Fig)\.?\s*(\d+(?:\.\d+)+[A-Za-z]?)")
TABLE_CAPTION_RE = re.compile(r"Table\s*(\d+(?:\.\d+)+[A-Za-z]?)")
EQ_TAG_RE = re.compile(r"\\(?:tag|label)\s*\{\s*([0-9][^}]*?)\s*\}")
PARAGRAPH_BREAK_RE = re.compile(r"\n\s*\n+")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--md", required=True, type=Path)
    p.add_argument("--asset-manifest", required=True, type=Path)
    p.add_argument("--skeleton", required=True, type=Path)
    p.add_argument("--audit-dir", required=True, type=Path,
                   help="Source's audit/ folder (also where sidecar exports land)")
    p.add_argument("--output-html", required=True, type=Path)
    p.add_argument("--output-section-nodes", required=True, type=Path)
    p.add_argument("--mode", choices=("structure", "atom-review", "coverage-review"),
                   default="structure")
    p.add_argument("--atomic-units-csv", type=Path, default=None)
    p.add_argument("--pages-dir-rel", default="pages",
                   help="Path (HTML-relative) to the page-image directory. "
                        "By convention this is the existing `audit/pages` symlink.")
    p.add_argument("--title", default=None)
    return p.parse_args()


def sha1_12(text: str) -> str:
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:12]


def load_sidecar(path: Path) -> dict:
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data:
                return data
        except Exception:
            pass
    return {}


def load_sidecar_with_fallback(audit_dir: Path, role: str) -> dict:
    """Load a sidecar JSON for the given role, walking through both the legacy
    flat layout (`<audit_dir>/<role>.json` + `<audit_dir>/*_<role>_*.json`) and
    the post-migration EQUATION_AUDIT layout
    (`<audit_dir>/equations/working/<role>.json` + ...) when it exists.

    Equation-state roles (`verified` / `flagged` / `backcheck`) live under the
    nested layout after a `migrate_audit_layout.py` run; other roles
    (`atoms_verified`, `sections_verified`, etc.) continue to live flat in the
    audit folder. Returning the first non-empty match in priority order:
    canonical-legacy → export-legacy → canonical-new → export-new."""
    search_dirs: list[Path] = [audit_dir]
    nested = audit_dir / "equations" / "working"
    if nested.is_dir():
        search_dirs.append(nested)

    for d in search_dirs:
        data = load_sidecar(d / f"{role}.json")
        if data:
            return data

    for d in search_dirs:
        candidates = sorted(d.glob(f"*_{role}_*.json"))
        if candidates:
            latest = candidates[-1]
            print(f"  using latest exported {role}: {latest.relative_to(audit_dir)}", file=sys.stderr)
            return load_sidecar(latest)

    return {}


def load_skeleton(skeleton_path: Path) -> dict:
    return json.loads(skeleton_path.read_text(encoding="utf-8"))


def load_atoms(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def build_asset_index(manifest: dict) -> dict[str, dict]:
    by_name: dict[str, dict] = {}
    for a in manifest.get("assets", []):
        png = a.get("png_path") or ""
        if png:
            by_name[Path(png).name] = a
            by_name[png] = a
    return by_name


def build_page_line_index(lines: list[str]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for i, raw in enumerate(lines, start=1):
        m = PAGE_MARKER_RE.search(raw)
        if m:
            out.append((i, int(m.group(1))))
    return out


def build_dense_page_anchors(
    lines: list[str],
    asset_index: dict[str, dict],
) -> list[tuple[int, int]]:
    """Return [(line_no, page)] anchors derived from page markers PLUS the
    first appearance of each manifested asset (since assets carry their page
    number explicitly). Sparse page markers alone miss most lines."""
    anchors: list[tuple[int, int]] = []
    for i, raw in enumerate(lines, start=1):
        m = PAGE_MARKER_RE.search(raw)
        if m:
            anchors.append((i, int(m.group(1))))
        for m in INLINE_IMAGE_RE.finditer(raw):
            asset = asset_index.get(Path(m.group(2)).name)
            if asset and isinstance(asset.get("page"), int):
                anchors.append((i, asset["page"]))
        for m in INLINE_LINK_RE.finditer(raw):
            src = m.group(2)
            if not src.endswith((".png", ".xlsx")):
                continue
            asset = asset_index.get(Path(src).name)
            if not asset:
                stem = Path(src).stem
                asset = asset_index.get(stem + ".png")
            if asset and isinstance(asset.get("page"), int):
                anchors.append((i, asset["page"]))
    anchors.sort(key=lambda t: t[0])
    # Deduplicate consecutive entries with the same page
    dedup: list[tuple[int, int]] = []
    for entry in anchors:
        if dedup and dedup[-1][1] == entry[1]:
            continue
        dedup.append(entry)
    return dedup


def page_for_line(line_no: int, anchors: list[tuple[int, int]]) -> int | None:
    page = None
    for lno, pg in anchors:
        if lno <= line_no:
            page = pg
        else:
            break
    return page


def build_cross_ref_indexes(
    sections: list[dict],
    md_lines: list[str],
    asset_index: dict[str, dict],
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    """Return four maps: figure label → cross-surface anchor, table label →
    cross-surface anchor, equation label → anchor (empty in the reduced
    surface), section number → in-page anchor.

    Per-asset review now lives in the per-kind audit surfaces
    (`figures.html`, `tables.html`, `images.html`), so `Fig 3.1` and
    `Table 2.7` references in section bodies link out to those surfaces.
    Equation cross-refs are not rewritten here (the equation audit lives
    in `equations.html` with its own internal anchor scheme)."""
    fig_map: dict[str, str] = {}
    tbl_map: dict[str, str] = {}
    eq_map: dict[str, str] = {}
    sec_map: dict[str, str] = {}

    for s in sections:
        if s.get("section_number"):
            sec_map[s["section_number"]] = f"#{s['section_id']}"

    # Scan all asset references inline in the markdown to build label → anchor.
    for raw in md_lines:
        for m in INLINE_IMAGE_RE.finditer(raw):
            alt_text, src = m.group(1), m.group(2)
            asset = asset_index.get(Path(src).name) or asset_index.get(src)
            if not asset:
                continue
            asset_id = asset.get("asset_id")
            if not asset_id:
                continue
            for cap in FIG_CAPTION_RE.findall(alt_text):
                fig_map.setdefault(cap, f"figures.html#asset-{asset_id}")
            for cap in TABLE_CAPTION_RE.findall(alt_text):
                tbl_map.setdefault(cap, f"tables.html#asset-{asset_id}")
        for m in INLINE_LINK_RE.finditer(raw):
            link_text, src = m.group(1), m.group(2)
            if not src.endswith(".png") and not src.endswith(".xlsx"):
                continue
            stem = Path(src).stem
            png_name = stem + ".png"
            asset = asset_index.get(png_name) or asset_index.get(Path(src).name)
            if not asset:
                continue
            asset_id = asset.get("asset_id")
            if not asset_id:
                continue
            for cap in TABLE_CAPTION_RE.findall(link_text):
                tbl_map.setdefault(cap, f"tables.html#asset-{asset_id}")
            for cap in FIG_CAPTION_RE.findall(link_text):
                fig_map.setdefault(cap, f"figures.html#asset-{asset_id}")

    return fig_map, tbl_map, eq_map, sec_map


def rewrite_cross_refs(
    text: str,
    fig_map: dict[str, str],
    tbl_map: dict[str, str],
    eq_map: dict[str, str],
    sec_map: dict[str, str],
) -> str:
    """Rewrite Fig./Table/§/Eq. references to <a href="...">."""
    def sub_fig(m: re.Match) -> str:
        label = m.group(1)
        anchor = fig_map.get(label)
        return f'<a class="xref" href="{anchor}">{m.group(0)}</a>' if anchor else m.group(0)

    def sub_tbl(m: re.Match) -> str:
        label = m.group(1)
        anchor = tbl_map.get(label)
        return f'<a class="xref" href="{anchor}">{m.group(0)}</a>' if anchor else m.group(0)

    def sub_eq(m: re.Match) -> str:
        label = m.group(1)
        anchor = eq_map.get(label)
        return f'<a class="xref" href="{anchor}">{m.group(0)}</a>' if anchor else m.group(0)

    def sub_sec(m: re.Match) -> str:
        label = m.group(1)
        anchor = sec_map.get(label)
        return f'<a class="xref" href="{anchor}">{m.group(0)}</a>' if anchor else m.group(0)

    text = FIG_REF_RE.sub(sub_fig, text)
    text = TABLE_REF_RE.sub(sub_tbl, text)
    text = EQ_REF_RE.sub(sub_eq, text)
    text = SECTION_REF_RE.sub(sub_sec, text)
    return text


def split_paragraphs(text: str) -> list[str]:
    return [p for p in PARAGRAPH_BREAK_RE.split(text) if p.strip()]


def render_inline_text(
    text: str,
    cross_refs: tuple[dict, dict, dict, dict],
) -> str:
    """Render one logical inline string: escape HTML but leave $$/$ math alone,
    convert inline images/links, then rewrite cross-references."""
    # Protect display and inline math using sentinels so html.escape doesn't
    # mangle the delimiters or contents.
    placeholders: list[str] = []

    def stash(m: re.Match) -> str:
        placeholders.append(m.group(0))
        return f"\x00MATH{len(placeholders) - 1}\x00"

    text = DISPLAY_MATH_RE.sub(stash, text)
    text = re.sub(r"(?<!\\)\$([^$\n]+?)(?<!\\)\$", lambda m: stash(m), text)

    images: list[str] = []
    links: list[str] = []

    def stash_img(m: re.Match) -> str:
        alt, src = m.group(1), m.group(2)
        images.append(
            f'<img class="inline-img" loading="lazy" alt="{html.escape(alt)}" src="{html.escape(src)}">'
        )
        return f"\x00IMG{len(images) - 1}\x00"

    def stash_link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        links.append(
            f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(label)}</a>'
        )
        return f"\x00LINK{len(links) - 1}\x00"

    text = INLINE_IMAGE_RE.sub(stash_img, text)
    text = INLINE_LINK_RE.sub(stash_link, text)

    text = html.escape(text)

    text = rewrite_cross_refs(text, *cross_refs)

    for i, ph in enumerate(placeholders):
        text = text.replace(f"\x00MATH{i}\x00", ph)
    for i, img in enumerate(images):
        text = text.replace(f"\x00IMG{i}\x00", img)
    for i, lk in enumerate(links):
        text = text.replace(f"\x00LINK{i}\x00", lk)
    return text


def render_section_body(
    body_text: str,
    cross_refs: tuple[dict, dict, dict, dict],
) -> str:
    """Render a section's MD body to HTML paragraphs (plus pass-through math)."""
    paragraphs = split_paragraphs(body_text)
    out: list[str] = []
    for p in paragraphs:
        # Heading lines inside the body (from sub-section nesting) are
        # rendered as their own <h*> for visual hierarchy. The heading text
        # itself is not a reviewable chunk here — the sub-section block,
        # rendered separately, owns that.
        m = HEADING_RE.match(p.strip())
        if m:
            hashes, title = m.group(1), m.group(2).strip()
            depth = len(hashes)
            rendered = render_inline_text(title, cross_refs)
            out.append(f'<h{depth} class="inline-heading">{rendered}</h{depth}>')
            continue
        rendered = render_inline_text(p, cross_refs)
        out.append(f"<p>{rendered}</p>")
    return "\n".join(out)


def extract_section_md(
    md_lines: list[str],
    line_start: int,
    line_end: int,
    skip_heading: bool = True,
) -> str:
    body = md_lines[line_start - 1:line_end]
    if skip_heading and body and HEADING_RE.match(body[0]):
        body = body[1:]
    return "\n".join(body)


def render_chunk_controls(key: str, status: str, note: str) -> str:
    """Toolbar inside a reviewable chunk: radio chips + flag note textarea."""
    return (
        f'<div class="ctrl">'
        f'<span class="badge"></span>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="unreviewed">Unreviewed</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="verified">✓ Verified</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="flagged">⚠ Flag</label>'
        f'<textarea class="flagnote" placeholder="Flag note...">{html.escape(note)}</textarea>'
        f'</div>'
    )


def initial_status_for_key(key: str, verified: dict, flagged: dict) -> tuple[str, str]:
    if key in verified:
        return "verified", ""
    if key in flagged:
        return "flagged", flagged[key].get("description", "") or flagged[key].get("note", "")
    return "unreviewed", ""



def render_atom_list(
    section_id: str,
    atoms_by_section: dict[str, list[dict]],
    state_verified: dict,
    state_flagged: dict,
) -> tuple[str, list[str]]:
    """Render the per-section atoms list (atom-review mode only)."""
    atoms = atoms_by_section.get(section_id, [])
    if not atoms:
        return "", []
    items: list[str] = []
    keys: list[str] = []
    for a in atoms:
        atom_id = a.get("AtomicUnitID") or a.get("UnitID") or ""
        statement = a.get("UnitStatement") or ""
        h = a.get("ContentHash") or sha1_12(statement)
        key = f"atom:{h}"
        keys.append(key)
        status, note = initial_status_for_key(key, state_verified, state_flagged)
        inout = a.get("InOutStatus") or a.get("InOut") or "TBD"
        provenance = html.escape(a.get("SourceRef") or "")
        items.append(
            f'<li class="chunk atom" data-kind="atom" data-key="{key}" '
            f'data-status="{status}" data-inout="{inout}" data-atom-id="{atom_id}">'
            f'<span class="prov">{provenance}</span>'
            f'<span class="inout">{inout}</span>'
            f'<span class="stmt">{html.escape(statement)}</span>'
            f'{render_chunk_controls(key, status, note)}'
            f'</li>'
        )
    return f'<ul class="atoms">{"".join(items)}</ul>', keys


def coverage_class_for_density(density: float) -> str:
    if density == 0:
        return "cov-empty"
    if density < 0.5:
        return "cov-low"
    if density < 2.0:
        return "cov-mid"
    return "cov-high"


def main() -> int:
    args = parse_args()

    if not args.md.exists():
        return fail(f"--md not found: {args.md}")
    if not args.skeleton.exists():
        return fail(f"--skeleton not found: {args.skeleton}")
    if args.mode in ("atom-review", "coverage-review") and not args.atomic_units_csv:
        return fail(f"--atomic-units-csv required for mode {args.mode}")
    if args.atomic_units_csv and not args.atomic_units_csv.exists():
        return fail(f"--atomic-units-csv not found: {args.atomic_units_csv}")

    md_lines = args.md.read_text(encoding="utf-8").splitlines()
    skeleton = load_skeleton(args.skeleton)
    sections = skeleton["sections"]
    source_name = skeleton["source"]
    source_prefix = skeleton["source_prefix"]
    manifest = json.loads(args.asset_manifest.read_text(encoding="utf-8"))
    asset_index = build_asset_index(manifest)
    # Printed-folio map (schema v3+). Empty when the manifest predates v3
    # or when folio extraction was skipped on the source.
    page_labels: dict[int, str | None] = {}
    for pg_rec in manifest.get("pages", []):
        if isinstance(pg_rec, dict) and isinstance(pg_rec.get("page"), int):
            page_labels[pg_rec["page"]] = pg_rec.get("page_label")
    page_anchors = build_dense_page_anchors(md_lines, asset_index)

    # Sidecar load — only section + atom state (per-kind asset state lives
    # under the per-kind audit surfaces' own sidecars now).
    state_verified = load_sidecar_with_fallback(args.audit_dir, "verified")
    state_flagged = load_sidecar_with_fallback(args.audit_dir, "flagged")
    for kind in ("atoms", "sections"):
        for role in ("verified", "flagged"):
            extra = load_sidecar_with_fallback(args.audit_dir, f"{kind}_{role}")
            target = state_verified if role == "verified" else state_flagged
            for k, v in extra.items():
                target.setdefault(k, v)

    # Atoms (optional)
    atoms_by_section: dict[str, list[dict]] = {}
    if args.atomic_units_csv:
        for a in load_atoms(args.atomic_units_csv):
            sid = a.get("SectionID") or a.get("TargetSection") or a.get("PartitionID")
            if sid:
                atoms_by_section.setdefault(sid, []).append(a)

    cross_refs = build_cross_ref_indexes(sections, md_lines, asset_index)
    fig_map, tbl_map, eq_map, sec_map = cross_refs

    output_html_dir = args.output_html.parent
    pages_rel = args.pages_dir_rel.rstrip("/")

    # Section index → assets-by-section for figure/table rendering
    sections_by_id = {s["section_id"]: s for s in sections}

    body_html_parts: list[str] = []
    section_node_rows: list[dict] = []
    section_chunk_keys: list[str] = []
    atom_chunk_keys: list[str] = []

    for s in sections:
        section_id = s["section_id"]
        depth = s["depth"]
        title = s["title"]
        line_start = s["line_start"]
        line_end = s["line_end"]
        page_first = s.get("page_first")
        page_last = s.get("page_last")
        is_front = s.get("is_front_matter", False)
        is_back = s.get("is_back_matter", False)
        in_scope = s.get("in_scope_default", True)

        body_md = extract_section_md(md_lines, line_start, line_end, skip_heading=True)
        content_hash = sha1_12(title + "\n" + body_md)
        sec_key = f"section:{content_hash}"
        sec_status, sec_note = initial_status_for_key(sec_key, state_verified, state_flagged)
        section_chunk_keys.append(sec_key)

        # Coverage density
        atoms_in_sec = atoms_by_section.get(section_id, [])
        density = (
            len(atoms_in_sec) / max(1, (line_end - line_start + 1) / 50)
        )
        cov_class = coverage_class_for_density(density) if args.mode == "coverage-review" else ""

        # Section body markdown (display equations stripped — equation review
        # lives in equations.html; prose review is what this surface owns).
        body_without_eqs = DISPLAY_MATH_RE.sub("", body_md)
        body_html = render_section_body(body_without_eqs, cross_refs)

        # Atom list (only in atom-review mode)
        atoms_html = ""
        if args.mode == "atom-review":
            atoms_html, akeys = render_atom_list(
                section_id, atoms_by_section, state_verified, state_flagged,
            )
            atom_chunk_keys.extend(akeys)

        # Page-image strip (cover the section's page range)
        pages_strip = ""
        if page_first is not None:
            pages_strip_imgs: list[str] = []
            page_end = page_last if page_last is not None else page_first
            for p in range(page_first, min(page_end, page_first + 4) + 1):
                pages_strip_imgs.append(
                    f'<img loading="lazy" alt="page {p}" '
                    f'src="{pages_rel}/page_{p:04d}.png">'
                )
            pages_strip = "".join(pages_strip_imgs)

        classes = ["chunk", "sec", f"depth-{depth}"]
        if is_front:
            classes.append("front-matter")
        if is_back:
            classes.append("back-matter")
        if not in_scope:
            classes.append("out-of-scope")
        if cov_class:
            classes.append(cov_class)
        cls_attr = " ".join(classes)

        if page_first is not None:
            label_first = page_labels.get(page_first)
            if page_last is not None and page_last != page_first:
                label_last = page_labels.get(page_last)
                if label_first and label_last and (label_first != str(page_first) or label_last != str(page_last)):
                    page_badge = (
                        f'<span class="page-badge">pp. {html.escape(label_first)}–{html.escape(label_last)} '
                        f'(PDF pp. {page_first}–{page_last})</span>'
                    )
                else:
                    page_badge = f'<span class="page-badge">pp. {page_first}–{page_last}</span>'
            else:
                if label_first and label_first != str(page_first):
                    page_badge = (
                        f'<span class="page-badge">p. {html.escape(label_first)} '
                        f'(PDF p. {page_first})</span>'
                    )
                else:
                    page_badge = f'<span class="page-badge">p. {page_first}</span>'
        else:
            page_badge = ""
        heading_html = (
            f'<h{depth + 1} class="sec-title">'
            f'<span class="sid">{section_id}</span> '
            f'{html.escape(title)}{page_badge}</h{depth + 1}>'
        )

        section_html = (
            f'<section id="{section_id}" class="{cls_attr}" '
            f'data-kind="section" data-key="{sec_key}" data-status="{sec_status}" '
            f'data-depth="{depth}" data-page="{page_first or ""}" '
            f'data-in-scope="{"true" if in_scope else "false"}">'
            f'<header class="sec-head">{heading_html}'
            f'{render_chunk_controls(sec_key, sec_status, sec_note)}</header>'
            f'<div class="row">'
            f'<div class="img">{pages_strip}</div>'
            f'<div class="body">{body_html}'
            f'{atoms_html}'
            f'</div></div>'
            f'</section>'
        )
        body_html_parts.append(section_html)

        # section_nodes.csv row
        cleaned_text = body_md.strip().replace("\n", " ")[:8000]
        section_node_rows.append({
            "SectionID": section_id,
            "SourceDoc": source_name,
            "SourcePrefix": source_prefix,
            "Path": title,
            "Depth": depth,
            "Title": title,
            "LineStart": line_start,
            "LineEnd": line_end,
            "PageFirst": page_first or "",
            "PageLast": page_last or "",
            "HtmlAnchor": f"{args.output_html.name}#{section_id}",
            "ContentHash": content_hash,
            "InScope": in_scope,
            "IsFrontMatter": is_front,
            "IsBackMatter": is_back,
            "FigureRefs": ";".join(s.get("figure_refs", [])),
            "TableRefs": ";".join(s.get("table_refs", [])),
            "EquationRefs": ";".join(s.get("equation_refs", [])),
            "AssetIDs": ";".join(s.get("asset_ids", [])),
            "Text": cleaned_text,
        })

    # Stat counts (section + atom only; per-kind asset counts live in their
    # own audit surfaces)
    counts = {
        "sections": len(section_chunk_keys),
        "atoms": len(atom_chunk_keys),
    }

    title = args.title or f"{source_name} — review"
    initial_state = {
        "verified": state_verified,
        "flagged": state_flagged,
    }

    nav_items = []
    for s in sections:
        if s["depth"] <= 2 and not s.get("is_front_matter") and not s.get("is_back_matter"):
            nav_items.append(
                f'<a href="#{s["section_id"]}">{html.escape(s["title"][:60])}</a>'
            )
    nav_html = " ".join(nav_items)

    doc = build_html(
        title=title,
        nav_html=nav_html,
        body_html="\n".join(body_html_parts),
        counts=counts,
        initial_state_json=json.dumps(initial_state),
        source_prefix=source_prefix,
        mode=args.mode,
    )

    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(doc, encoding="utf-8")

    args.output_section_nodes.parent.mkdir(parents=True, exist_ok=True)
    if section_node_rows:
        with args.output_section_nodes.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(section_node_rows[0].keys()))
            writer.writeheader()
            for row in section_node_rows:
                writer.writerow(row)

    print(
        f"source={source_name} mode={args.mode} "
        f"sections={counts['sections']} atoms={counts['atoms']} "
        f"html={args.output_html.name} nodes={args.output_section_nodes.name}"
    )
    return 0


def fail(msg: str, code: int = 2) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return code


def build_html(
    title: str,
    nav_html: str,
    body_html: str,
    counts: dict[str, int],
    initial_state_json: str,
    source_prefix: str,
    mode: str,
) -> str:
    title_e = html.escape(title)
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title_e}</title>
<style>
body{{font-family:-apple-system,sans-serif;margin:0;padding:0;background:#fafafa;color:#222}}
.toolbar{{position:sticky;top:0;background:#fff;padding:.5rem 1rem;border-bottom:1px solid #ddd;z-index:30;display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;font-size:.85rem}}
.toolbar button{{padding:.35rem .7rem;border:1px solid #888;background:#f5f5f5;border-radius:3px;cursor:pointer;font-size:.85rem}}
.toolbar button.primary{{background:#06c;color:#fff;border-color:#06c}}
.toolbar .stat{{margin-right:.5rem;color:#444}}
.toolbar .stat b{{color:#000}}
.toolbar .dirty{{color:#c60;font-weight:bold}}
.toolbar .filter label{{margin-right:.4rem;cursor:pointer}}
.toolbar .mode-pill{{background:#06c;color:#fff;padding:.15rem .5rem;border-radius:3px;font-size:.75rem;text-transform:uppercase}}
nav.toc{{position:sticky;top:2.6rem;background:#fff;padding:.4rem .75rem;border-bottom:1px solid #ddd;font-size:.7rem;max-height:4rem;overflow-y:auto;z-index:25}}
nav.toc a{{margin-right:.5rem;color:#06c;text-decoration:none}}
main{{padding:0 1rem}}
section.sec{{margin:1.25rem 0;border-top:2px solid #333;padding-top:.5rem}}
section.sec.depth-3{{border-top:1px solid #888;padding-top:.4rem}}
section.sec.depth-4{{border-top:1px dashed #aaa}}
section.sec.front-matter{{background:#f6f0ff}}
section.sec.back-matter{{background:#fff4ec}}
section.sec.out-of-scope{{opacity:.55}}
section.sec.cov-empty{{outline:3px solid #d22}}
section.sec.cov-low{{outline:2px solid #e8a04a}}
section.sec.cov-mid{{outline:2px solid #5a8fd0}}
section.sec.cov-high{{outline:2px solid #2a8a3a}}
.sec-head{{display:flex;align-items:flex-start;gap:.75rem;justify-content:space-between;flex-wrap:wrap}}
.sec-title{{margin:.25rem 0;flex:1}}
.sid{{font-family:monospace;color:#888;font-size:.75em;margin-right:.4em}}
.row{{display:grid;grid-template-columns:1fr 2fr;gap:1rem;align-items:start;margin-top:.5rem}}
.row .img img{{width:100%;border:1px solid #ccc;background:#fff;margin-bottom:.25rem;position:relative}}
.body p{{margin:.5rem 0}}
.body h1,.body h2,.body h3,.body h4,.body h5,.body h6{{margin:.6rem 0 .25rem;color:#234}}
.body .inline-img{{max-width:100%;display:block;margin:.5rem 0}}
.chunk{{padding:.5rem;margin:.4rem 0;border:1px solid #ddd;background:#fff;border-radius:4px;transition:background .15s,opacity .15s}}
.chunk[data-status="verified"]{{background:#eef9ee;border-color:#9c9;opacity:.65}}
.chunk[data-status="flagged"]{{background:#fff4e6;border-color:#e8a04a}}
.chunk.atom{{display:flex;flex-wrap:wrap;align-items:flex-start;gap:.5rem;padding:.4rem .5rem}}
.atom .prov{{font-family:monospace;color:#888;font-size:.7em}}
.atom .inout{{font-size:.65em;background:#eef;padding:.05em .3em;border-radius:2px}}
.atom .stmt{{flex:1}}
ul.atoms{{padding:0;list-style:none;margin:.5rem 0}}
.page-badge{{font-size:.85em;color:#666;font-weight:normal;margin-left:.5em;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
.ctrl{{margin-top:.3rem;display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;font-size:.75rem;color:#555}}
.ctrl .badge{{display:inline-block;min-width:1.5rem}}
.chunk[data-status="verified"] .badge::before{{content:"✓ verified";color:#080;font-weight:bold}}
.chunk[data-status="flagged"] .badge::before{{content:"⚠ flagged";color:#c60;font-weight:bold}}
.rb{{cursor:pointer}}
textarea.flagnote{{display:none;width:100%;box-sizing:border-box;padding:.3rem;font-family:monospace;font-size:.8rem;border:1px solid #e8a04a;border-radius:3px;min-height:2rem;resize:vertical}}
.chunk[data-status="flagged"] textarea.flagnote{{display:block}}
.xref{{color:#06c;text-decoration:none}}
.xref:hover{{text-decoration:underline}}
body.hide-verified .chunk[data-status="verified"]{{display:none}}
body.only-flagged .chunk:not([data-status="flagged"]){{display:none}}
body.only-out .chunk:not([data-inout="OUT"]){{display:none}}
body.only-tbd .chunk:not([data-inout="TBD"]){{display:none}}
body.only-in  .chunk:not([data-inout="IN"]){{display:none}}
body.only-atoms .chunk:not(.atom){{display:none}}
body.only-sections .chunk:not(.sec){{display:none}}
</style></head><body>
<div class="toolbar">
  <span class="mode-pill">{mode}</span>
  <span class="stat">Sections: <b>{counts['sections']}</b></span>
  <span class="stat">Atoms: <b>{counts['atoms']}</b></span>
  <span class="stat">✓ <b id="stat-verified">0</b></span>
  <span class="stat">⚠ <b id="stat-flagged">0</b></span>
  <span class="stat dirty" id="dirty-flag"></span>
  <span class="filter">
    <label><input type="checkbox" id="hide-verified"> Hide verified</label>
    <label><input type="checkbox" id="only-flagged"> Only flagged</label>
    <label><input type="checkbox" id="only-in"> IN</label>
    <label><input type="checkbox" id="only-out"> OUT</label>
    <label><input type="checkbox" id="only-tbd"> TBD</label>
    <select id="kind-filter">
      <option value="">All kinds</option>
      <option value="only-sections">Sections only</option>
      <option value="only-atoms">Atoms only</option>
    </select>
  </span>
  <button onclick="exportSidecars()" class="primary">Export sidecars</button>
  <button onclick="reloadFromDisk()">Reload from disk</button>
  <button onclick="clearLocal()">Clear localStorage</button>
</div>
<nav class="toc">{nav_html}</nav>
<main>
{body_html}
</main>
<script>
const STORAGE_KEY = "decomp-audit:" + location.pathname;
const SOURCE_PREFIX = {json.dumps(source_prefix)};
const INITIAL = {initial_state_json};
let state = loadState();
let dirty = false;

function loadState() {{
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {{
    try {{ return JSON.parse(raw); }} catch(e) {{}}
  }}
  return JSON.parse(JSON.stringify(INITIAL));
}}

function saveState() {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  markDirty(true);
  updateStats();
}}

function markDirty(d) {{
  dirty = d;
  document.getElementById("dirty-flag").textContent = d ? "● unsaved changes (Export to persist)" : "";
}}

function updateStats() {{
  let v=0,f=0;
  document.querySelectorAll(".chunk").forEach(el => {{
    const s = el.dataset.status;
    if (s === "verified") v++;
    else if (s === "flagged") f++;
  }});
  document.getElementById("stat-verified").textContent = v;
  document.getElementById("stat-flagged").textContent = f;
}}

function applyStateToDOM() {{
  document.querySelectorAll(".chunk").forEach(el => {{
    const key = el.dataset.key;
    const legacy = el.dataset.legacyKey;
    let status = "unreviewed";
    let note = "";
    if ((state.verified && state.verified[key]) || (legacy && state.verified && state.verified[legacy])) {{
      status = "verified";
    }} else if ((state.flagged && state.flagged[key]) || (legacy && state.flagged && state.flagged[legacy])) {{
      status = "flagged";
      const entry = (state.flagged && (state.flagged[key] || state.flagged[legacy])) || {{}};
      note = entry.description || entry.note || "";
    }}
    el.dataset.status = status;
    el.querySelectorAll('input[type=radio]').forEach(r => {{ r.checked = (r.value === status); }});
    const ta = el.querySelector("textarea.flagnote");
    if (ta) ta.value = note;
  }});
  updateStats();
}}

document.addEventListener("change", e => {{
  if (e.target.matches('input[type=radio]')) {{
    const ck = e.target.closest(".chunk");
    if (!ck) return;
    const key = ck.dataset.key;
    const status = e.target.value;
    ck.dataset.status = status;
    if (status === "verified") {{
      state.verified = state.verified || {{}};
      state.verified[key] = {{
        kind: ck.dataset.kind,
        page: ck.dataset.page || null,
        verified_at: new Date().toISOString().slice(0,10)
      }};
      if (state.flagged) delete state.flagged[key];
    }} else if (status === "flagged") {{
      const note = (ck.querySelector("textarea.flagnote") || {{}}).value || "";
      state.flagged = state.flagged || {{}};
      state.flagged[key] = {{
        kind: ck.dataset.kind,
        page: ck.dataset.page || null,
        description: note,
        flagged_at: new Date().toISOString().slice(0,10)
      }};
      if (state.verified) delete state.verified[key];
    }} else {{
      if (state.verified) delete state.verified[key];
      if (state.flagged) delete state.flagged[key];
    }}
    saveState();
  }}
}});

document.addEventListener("input", e => {{
  if (e.target.matches("textarea.flagnote")) {{
    const ck = e.target.closest(".chunk");
    if (!ck || ck.dataset.status !== "flagged") return;
    const key = ck.dataset.key;
    state.flagged = state.flagged || {{}};
    state.flagged[key] = state.flagged[key] || {{
      kind: ck.dataset.kind,
      page: ck.dataset.page || null,
      flagged_at: new Date().toISOString().slice(0,10)
    }};
    state.flagged[key].description = e.target.value;
    saveState();
  }}
}});

function download(filename, data) {{
  const blob = new Blob([JSON.stringify(data, null, 2)], {{type:"application/json"}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}}

function bucketByKind(map) {{
  const buckets = {{atom:{{}}, section:{{}}}};
  for (const [k, v] of Object.entries(map || {{}})) {{
    const idx = k.indexOf(":");
    const kind = idx > 0 ? k.slice(0, idx) : "other";
    if (buckets[kind]) buckets[kind][k] = v;
    else (buckets.other = buckets.other || {{}})[k] = v;
  }}
  return buckets;
}}

function exportSidecars() {{
  const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g,"-");
  const slug = SOURCE_PREFIX || "source";
  const vbuckets = bucketByKind(state.verified);
  const fbuckets = bucketByKind(state.flagged);
  for (const kind of ["atom","section"]) {{
    const v = vbuckets[kind] || {{}};
    const f = fbuckets[kind] || {{}};
    if (Object.keys(v).length) download(`${{slug}}_${{kind}}s_verified_${{ts}}.json`, v);
    if (Object.keys(f).length) download(`${{slug}}_${{kind}}s_flagged_${{ts}}.json`, f);
  }}
  markDirty(false);
}}

function reloadFromDisk() {{
  if (!confirm("Discard browser edits and reload state from on-disk sidecars baked into this HTML?")) return;
  localStorage.removeItem(STORAGE_KEY);
  state = JSON.parse(JSON.stringify(INITIAL));
  applyStateToDOM();
  markDirty(false);
}}

function clearLocal() {{
  if (!confirm("Wipe ALL review state from localStorage? Does not touch on-disk sidecars until you re-export.")) return;
  state = {{verified: {{}}, flagged: {{}}}};
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  applyStateToDOM();
  markDirty(true);
}}

document.getElementById("hide-verified").addEventListener("change", e => {{
  document.body.classList.toggle("hide-verified", e.target.checked);
}});
document.getElementById("only-flagged").addEventListener("change", e => {{
  document.body.classList.toggle("only-flagged", e.target.checked);
}});
document.getElementById("only-in").addEventListener("change", e => {{
  document.body.classList.toggle("only-in", e.target.checked);
}});
document.getElementById("only-out").addEventListener("change", e => {{
  document.body.classList.toggle("only-out", e.target.checked);
}});
document.getElementById("only-tbd").addEventListener("change", e => {{
  document.body.classList.toggle("only-tbd", e.target.checked);
}});
document.getElementById("kind-filter").addEventListener("change", e => {{
  ["only-sections","only-atoms"].forEach(c => document.body.classList.remove(c));
  if (e.target.value) document.body.classList.add(e.target.value);
}});

applyStateToDOM();
window.addEventListener("beforeunload", e => {{
  if (dirty) {{ e.preventDefault(); e.returnValue = ""; }}
}});
</script>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
