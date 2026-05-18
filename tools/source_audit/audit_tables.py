#!/usr/bin/env python3
"""
audit_tables.py — render one source's tables.html review surface.

The Gate 1.5-T surface for DOMAIN_DECOMP. Each table asset becomes a
reviewable chunk with its bbox crop image, caption, and (when the table
was successfully transcribed under the pdf2md-table/v1 contract) two
links: the rendered XLSX workbook and the canonical table_data JSON
sidecar. Tables flagged `needs_extraction: true` render with a distinct
chip and no XLSX/JSON links — they signal "table visible but not yet
structurally extracted" and stay in the queue for future re-dispatch.

Sidecar files: <source>_tables_verified_<TS>.json /
<source>_tables_flagged_<TS>.json under the source's audit/ folder.

Usage:
  python3 tools/source_audit/audit_tables.py \\
      --asset-manifest <src>/<src>_assets_manifest.json \\
      --audit-dir <src>/audit \\
      --output-html <src>/audit/tables.html \\
      [--pages-dir-rel pages] [--title "..."]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.source_audit import chunk as sa_chunk  # noqa: E402
from tools.source_audit import html_shell, page_strip, sidecar  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render tables.html (Gate 1.5-T surface).")
    p.add_argument("--asset-manifest", required=True)
    p.add_argument("--audit-dir", required=True)
    p.add_argument("--output-html", required=True)
    p.add_argument("--pages-dir-rel", default="pages")
    p.add_argument("--title", default=None)
    return p.parse_args()


def relpath_for_html(p: str, audit_dir: Path, html_dir: Path) -> str:
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


def render_table_chunk(asset: dict, audit_dir: Path, output_html_dir: Path,
                       verified: dict, flagged: dict) -> tuple[str, str, str]:
    import html as html_mod
    asset_id = asset["asset_id"]
    key = f"table:{asset_id}"
    status, note = sa_chunk.initial_status_for_key(key, verified, flagged)
    caption = asset.get("caption", "") or ""
    page = asset.get("page", "")
    png_path = asset.get("png_path", "") or ""
    xlsx_path = asset.get("xlsx_path", "") or ""
    json_path = asset.get("table_data_json_path", "") or ""
    needs_extraction = bool(asset.get("needs_extraction"))

    rel_png = relpath_for_html(png_path, audit_dir, output_html_dir)
    img_html = (f'<img class="crop" loading="lazy" alt="{html_mod.escape(caption)}" '
                f'src="{rel_png}">') if rel_png else ""

    links_html = ""
    if needs_extraction:
        links_html = '<div class="links"><span class="needs-extraction">needs_extraction</span></div>'
    else:
        rel_xlsx = relpath_for_html(xlsx_path, audit_dir, output_html_dir)
        rel_json = relpath_for_html(json_path, audit_dir, output_html_dir)
        link_parts = []
        if rel_xlsx:
            link_parts.append(f'<a class="xlsxlink" href="{rel_xlsx}">XLSX</a>')
        if rel_json:
            link_parts.append(f'<a class="jsonlink" href="{rel_json}">JSON</a>')
        if link_parts:
            links_html = f'<div class="links">{"".join(link_parts)}</div>'

    block = (
        f'<div id="asset-{asset_id}" class="chunk tbl" '
        f'data-kind="table" data-key="{key}" data-status="{status}" '
        f'data-asset-id="{asset_id}" data-page="{page}" '
        f'data-needs-extraction="{str(needs_extraction).lower()}">'
        f'<div class="meta">{asset_id} · p. {page}</div>'
        f'{img_html}'
        f'<div class="caption">{html_mod.escape(caption)}</div>'
        f'{links_html}'
        f'{sa_chunk.render_chunk_controls(key, status, note)}'
        f'</div>'
    )
    return block, key, status


INSTRUCTIONS_HTML = """<details class="instructions" open>
<summary>How to use this audit</summary>
<p>One reviewable chunk per table asset. The bbox crop and caption are shown
alongside the source page raster on the left. For successfully-transcribed
tables, the <code>XLSX</code> link opens the rendered workbook and the
<code>JSON</code> link opens the canonical <code>table_data</code> sidecar.
Tables flagged <code>needs_extraction</code> show that chip in place of the
links — those are visible-but-not-structurally-transcribed and stay in the
re-dispatch queue.</p>
<ul>
  <li><code>✓ Verified</code> — bbox + caption + (when present) structure/values match the printed table.</li>
  <li><code>⚠ Flag</code> — describe what's wrong in the note (bbox clipped, caption mis-bound, structure error, value error, header/section drift, etc.).</li>
</ul>
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
    verified = sidecar.load_sidecar_with_fallback(audit_dir, "tables_verified")
    flagged = sidecar.load_sidecar_with_fallback(audit_dir, "tables_flagged")

    tbls = [a for a in manifest.get("assets", []) if a.get("kind") == "tbl"]
    by_page: dict[int, list[dict]] = {}
    for a in tbls:
        pg = a.get("page")
        if not isinstance(pg, int):
            continue
        by_page.setdefault(pg, []).append(a)

    page_sections: list[str] = []
    v_count = f_count = needs_ext_count = 0
    for pg in sorted(by_page):
        chunks_html: list[str] = []
        for asset in by_page[pg]:
            block, _, status = render_table_chunk(
                asset, audit_dir, output_html.parent, verified, flagged
            )
            chunks_html.append(block)
            if status == "verified":
                v_count += 1
            elif status == "flagged":
                f_count += 1
            if asset.get("needs_extraction"):
                needs_ext_count += 1
        png_rel = f"{args.pages_dir_rel}/page_{pg:04d}.png"
        page_sections.append(
            page_strip.render_page_section(pg, png_rel, "".join(chunks_html), len(by_page[pg]))
        )

    title = args.title or f"Tables audit — {manifest_path.parent.name}"
    doc = html_shell.render_audit_page(
        title=title,
        kind="tables",
        page_sections_html="".join(page_sections),
        nav_html=page_strip.render_nav(sorted(by_page)),
        initial_state={"verified": verified, "flagged": flagged},
        counts={"total": len(tbls), "verified": v_count, "flagged": f_count},
        instructions_html=INSTRUCTIONS_HTML,
    )
    output_html.write_text(doc, encoding="utf-8")
    print(f"source={manifest_path.parent.name} kind=tables tables={len(tbls)} "
          f"needs_extraction={needs_ext_count} pages={len(by_page)} "
          f"verified={v_count} flagged={f_count} html={output_html.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
