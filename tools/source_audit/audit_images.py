#!/usr/bin/env python3
"""
audit_images.py — render one source's images.html review surface.

The Gate 1.5-I surface for DOMAIN_DECOMP. Each kind=img asset becomes a
reviewable chunk with its bbox crop, caption, and accept/flag controls.
The images bucket is the catch-all for non-figure, non-table raster
assets the VLM identified on a page (e.g. mastheads, logos, decorative
ornaments, photographs that aren't figures). The review motion is
mostly false-positive triage: is this actually a meaningful asset, or
should it be flagged out?

Sidecar files: <source>_images_verified_<TS>.json /
<source>_images_flagged_<TS>.json.

Usage:
  python3 tools/source_audit/audit_images.py \\
      --asset-manifest <src>/<src>_assets_manifest.json \\
      --audit-dir <src>/audit \\
      --output-html <src>/audit/images.html \\
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
    p = argparse.ArgumentParser(description="Render images.html (Gate 1.5-I surface).")
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


def render_image_chunk(asset: dict, audit_dir: Path, output_html_dir: Path,
                       verified: dict, flagged: dict) -> tuple[str, str, str]:
    import html as html_mod
    asset_id = asset["asset_id"]
    key = f"image:{asset_id}"
    status, note = sa_chunk.initial_status_for_key(key, verified, flagged)
    caption = asset.get("caption", "") or ""
    page = asset.get("page", "")
    png_path = asset.get("png_path", "") or ""
    rel_src = relpath_for_html(png_path, audit_dir, output_html_dir)
    img_html = (f'<img class="crop" loading="lazy" alt="{html_mod.escape(caption)}" '
                f'src="{rel_src}">') if rel_src else ""
    block = (
        f'<div id="asset-{asset_id}" class="chunk img" '
        f'data-kind="image" data-key="{key}" data-status="{status}" '
        f'data-asset-id="{asset_id}" data-page="{page}">'
        f'<div class="meta">{asset_id} · p. {page}</div>'
        f'{img_html}'
        f'<div class="caption">{html_mod.escape(caption)}</div>'
        f'{sa_chunk.render_chunk_controls(key, status, note)}'
        f'</div>'
    )
    return block, key, status


INSTRUCTIONS_HTML = """<details class="instructions" open>
<summary>How to use this audit</summary>
<p>One reviewable chunk per non-figure / non-table image asset detected on a
source page (mastheads, logos, decorative ornaments, photographs). The review
motion is mostly false-positive triage.</p>
<ul>
  <li><code>✓ Verified</code> — this is a meaningful asset (e.g. a real photograph or schematic the corpus should retain).</li>
  <li><code>⚠ Flag</code> — false positive (page header decoration, footer logo, etc.) or bbox mis-bound. Describe in the note.</li>
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
    verified = sidecar.load_sidecar_with_fallback(audit_dir, "images_verified")
    flagged = sidecar.load_sidecar_with_fallback(audit_dir, "images_flagged")

    imgs = [a for a in manifest.get("assets", []) if a.get("kind") == "img"]
    by_page: dict[int, list[dict]] = {}
    for a in imgs:
        pg = a.get("page")
        if not isinstance(pg, int):
            continue
        by_page.setdefault(pg, []).append(a)

    page_sections: list[str] = []
    v_count = f_count = 0
    for pg in sorted(by_page):
        chunks_html: list[str] = []
        for asset in by_page[pg]:
            block, _, status = render_image_chunk(
                asset, audit_dir, output_html.parent, verified, flagged
            )
            chunks_html.append(block)
            if status == "verified":
                v_count += 1
            elif status == "flagged":
                f_count += 1
        png_rel = f"{args.pages_dir_rel}/page_{pg:04d}.png"
        page_sections.append(
            page_strip.render_page_section(pg, png_rel, "".join(chunks_html), len(by_page[pg]))
        )

    title = args.title or f"Images audit — {manifest_path.parent.name}"
    doc = html_shell.render_audit_page(
        title=title,
        kind="images",
        page_sections_html="".join(page_sections),
        nav_html=page_strip.render_nav(sorted(by_page)),
        initial_state={"verified": verified, "flagged": flagged},
        counts={"total": len(imgs), "verified": v_count, "flagged": f_count},
        instructions_html=INSTRUCTIONS_HTML,
    )
    output_html.write_text(doc, encoding="utf-8")
    print(f"source={manifest_path.parent.name} kind=images images={len(imgs)} pages={len(by_page)} "
          f"verified={v_count} flagged={f_count} html={output_html.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
