#!/usr/bin/env python3
"""
audit_figures.py — render one source's figures.html review surface.

The Gate 1.5-F surface for DOMAIN_DECOMP. Each figure asset becomes a
reviewable chunk with its bbox crop image, caption, and accept/flag
radio controls. Chunks are grouped per source page so the page raster
appears once on the left and its figures stack on the right.

Reviewer state persists in browser localStorage and exports as two
sidecars under the source's audit/ folder:
  - <source>_figures_verified_<TS>.json
  - <source>_figures_flagged_<TS>.json
Drop the latest export under audit/ (canonical name
`figures_verified.json` / `figures_flagged.json`) to bake it into the
next render.

Usage:
  python3 tools/source_audit/audit_figures.py \\
      --asset-manifest <src>/<src>_assets_manifest.json \\
      --audit-dir <src>/audit \\
      --output-html <src>/audit/figures.html \\
      [--pages-dir-rel pages] [--title "..."]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow invocation as both `python3 -m tools.source_audit.audit_figures`
# and `python3 tools/source_audit/audit_figures.py`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.source_audit import chunk as sa_chunk  # noqa: E402
from tools.source_audit import html_shell, page_strip, sidecar  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render figures.html (Gate 1.5-F surface).")
    p.add_argument("--asset-manifest", required=True)
    p.add_argument("--audit-dir", required=True)
    p.add_argument("--output-html", required=True)
    p.add_argument("--pages-dir-rel", default="pages",
                   help="HTML-relative path to the page-image directory.")
    p.add_argument("--title", default=None)
    return p.parse_args()


def render_figure_chunk(asset: dict, audit_dir: Path, output_html_dir: Path,
                        verified: dict, flagged: dict) -> tuple[str, str, str]:
    """Return (chunk_html, key, status) for one figure asset."""
    asset_id = asset["asset_id"]
    key = f"figure:{asset_id}"
    status, note = sa_chunk.initial_status_for_key(key, verified, flagged)
    caption = asset.get("caption", "") or ""
    page = asset.get("page", "")
    png_path = asset.get("png_path", "") or ""
    rel_src = relpath_for_html(png_path, audit_dir, output_html_dir)
    import html as html_mod
    img_html = (f'<img class="crop" loading="lazy" alt="{html_mod.escape(caption)}" '
                f'src="{rel_src}">') if rel_src else ""
    block = (
        f'<figure id="asset-{asset_id}" class="chunk fig" '
        f'data-kind="figure" data-key="{key}" data-status="{status}" '
        f'data-asset-id="{asset_id}" data-page="{page}">'
        f'<div class="meta">{asset_id} · p. {page}</div>'
        f'{img_html}'
        f'<div class="caption">{html_mod.escape(caption)}</div>'
        f'{sa_chunk.render_chunk_controls(key, status, note)}'
        f'</figure>'
    )
    return block, key, status


def relpath_for_html(p: str, audit_dir: Path, html_dir: Path) -> str:
    """Same convention as render_source_html.py.relpath_for_html: asset
    paths in the manifest are stored relative to the source root
    (sibling of audit/). HTML lives in audit/, so go up one then in."""
    if not p:
        return ""
    pp = Path(p)
    if pp.is_absolute():
        target = pp
    else:
        target = audit_dir.parent / p
    try:
        return str(target.resolve().relative_to(html_dir.resolve()))
    except ValueError:
        import os
        return os.path.relpath(target, html_dir)


INSTRUCTIONS_HTML = """<details class="instructions" open>
<summary>How to use this audit</summary>
<p>One reviewable chunk per figure asset. The bbox crop and caption are
shown alongside the source page raster on the left.</p>
<ul>
  <li><code>Unreviewed</code> — default; not yet looked at.</li>
  <li><code>✓ Verified</code> — bbox crop and caption are correct for this figure.</li>
  <li><code>⚠ Flag</code> — bbox is wrong (clipped, mis-bound, false positive)
     or caption mis-bound. Describe the correction in the note field.</li>
</ul>
<p><b>Saving</b>: state saves to browser localStorage automatically.
The orange "unsaved" indicator stays on until you Export. Drop the
exported <code>*_figures_verified_*.json</code> /
<code>*_figures_flagged_*.json</code> back into the
<code>audit/</code> folder (or rename to the canonical
<code>figures_verified.json</code> / <code>figures_flagged.json</code>)
to make it active for the next regeneration.</p>
</details>"""


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.asset_manifest).resolve()
    audit_dir = Path(args.audit_dir).resolve()
    output_html = Path(args.output_html).resolve()
    output_html.parent.mkdir(parents=True, exist_ok=True)

    if not manifest_path.is_file():
        print(f"ERROR: asset manifest not found: {manifest_path}", file=sys.stderr)
        return 2
    if not audit_dir.is_dir():
        print(f"ERROR: audit dir not found: {audit_dir}", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verified = sidecar.load_sidecar_with_fallback(audit_dir, "figures_verified")
    flagged = sidecar.load_sidecar_with_fallback(audit_dir, "figures_flagged")

    figs = [a for a in manifest.get("assets", []) if a.get("kind") == "fig"]
    by_page: dict[int, list[dict]] = {}
    for a in figs:
        pg = a.get("page")
        if not isinstance(pg, int):
            continue
        by_page.setdefault(pg, []).append(a)

    page_sections: list[str] = []
    verified_count = flagged_count = 0
    for pg in sorted(by_page):
        chunks_html: list[str] = []
        for asset in by_page[pg]:
            block, _, status = render_figure_chunk(
                asset, audit_dir, output_html.parent, verified, flagged
            )
            chunks_html.append(block)
            if status == "verified":
                verified_count += 1
            elif status == "flagged":
                flagged_count += 1
        png_rel = f"{args.pages_dir_rel}/page_{pg:04d}.png"
        page_sections.append(
            page_strip.render_page_section(pg, png_rel, "".join(chunks_html), len(by_page[pg]))
        )

    title = args.title or f"Figures audit — {manifest_path.parent.name}"
    doc = html_shell.render_audit_page(
        title=title,
        kind="figures",
        page_sections_html="".join(page_sections),
        nav_html=page_strip.render_nav(sorted(by_page)),
        initial_state={"verified": verified, "flagged": flagged},
        counts={"total": len(figs), "verified": verified_count, "flagged": flagged_count},
        instructions_html=INSTRUCTIONS_HTML,
    )
    output_html.write_text(doc, encoding="utf-8")
    print(f"source={manifest_path.parent.name} kind=figures figures={len(figs)} pages={len(by_page)} "
          f"verified={verified_count} flagged={flagged_count} html={output_html.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
