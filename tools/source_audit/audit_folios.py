#!/usr/bin/env python3
"""
audit_folios.py — render one source's folios.html review surface.

The Gate 1.5-Fo surface for DOMAIN_DECOMP. Each physical page becomes one
reviewable chunk presenting the VLM-extracted printed folio label
(`page_label`) alongside the page raster. The review motion is: verify
the printed folio in the corner of the raster matches the emitted label;
flag (with the correct value) when wrong.

Sidecar files: <source>_folios_verified_<TS>.json /
<source>_folios_flagged_<TS>.json.

Usage:
  python3 tools/source_audit/audit_folios.py \\
      --page-folios-json <src>/<src>_pdf2md_work/page_folios.json \\
      --audit-dir <src>/audit \\
      --output-html <src>/audit/folios.html \\
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
    p = argparse.ArgumentParser(description="Render folios.html (Gate 1.5-Fo surface).")
    p.add_argument("--page-folios-json", required=True)
    p.add_argument("--audit-dir", required=True)
    p.add_argument("--output-html", required=True)
    p.add_argument("--pages-dir-rel", default="pages")
    p.add_argument("--title", default=None)
    return p.parse_args()


def render_folio_chunk(page: int, record: dict, verified: dict, flagged: dict) -> tuple[str, str, str]:
    import html as html_mod
    key = f"folio:p{page}"
    status, note = sa_chunk.initial_status_for_key(key, verified, flagged)

    run_status = record.get("run_status", "SUCCESS") or "SUCCESS"
    page_label = record.get("page_label")
    label_display = page_label if page_label else "(no folio)"
    label_attr = page_label if page_label else ""
    confidence = record.get("confidence", "") or ""
    location = record.get("location", "") or ""
    rationale = record.get("rationale", "") or ""

    fail_html = ""
    if run_status != "SUCCESS":
        fail_html = (
            f'<div class="fail-status">⚠ extractor {html_mod.escape(run_status)}</div>'
        )

    chips: list[str] = []
    if confidence:
        chips.append(f'<span class="chip confidence">conf: {html_mod.escape(confidence)}</span>')
    if location:
        chips.append(f'<span class="chip location">{html_mod.escape(location)}</span>')
    chips_html = " ".join(chips)

    meta = (
        f'p. {page} · folio: <b>{html_mod.escape(label_display)}</b> {chips_html}'
    )

    block = (
        f'<div id="folio-p{page}" class="chunk folio" '
        f'data-kind="folio" data-key="{key}" data-status="{status}" '
        f'data-page="{page}" data-page-label="{html_mod.escape(label_attr)}">'
        f'{fail_html}'
        f'<div class="meta">{meta}</div>'
        f'<div class="caption">{html_mod.escape(rationale)}</div>'
        f'{sa_chunk.render_chunk_controls(key, status, note)}'
        f'</div>'
    )
    return block, key, status


INSTRUCTIONS_HTML = """<details class="instructions" open>
<summary>How to use this audit</summary>
<p>One reviewable chunk per physical page. The VLM extracted the printed
folio label (e.g. Roman numerals for front-matter, Arabic numerals for
the body) from the page corner/footer.</p>
<ul>
  <li><code>✓ Verified</code> — the displayed <code>page_label</code> matches the printed folio visible in the corner of the page raster (or <code>(no folio)</code> is correct because no printed folio appears).</li>
  <li><code>⚠ Flag</code> — the label is wrong or missing. Put the correct value in the note (e.g. <code>correct: xii</code>).</li>
</ul>
</details>"""


FOLIO_HEAD_EXTRAS = """<style>
.chunk.folio .meta b{color:#06c;font-family:monospace;font-size:1.05em}
.chunk.folio .chip{display:inline-block;font-size:.7em;padding:.05rem .35rem;margin-left:.3rem;border-radius:3px;background:#eef;border:1px solid #ccd;color:#446;font-family:monospace}
.chunk.folio .chip.confidence{background:#efe;border-color:#cdc;color:#464}
.chunk.folio .fail-status{color:#a00;font-weight:bold;font-size:.8em;margin-bottom:.3rem;font-family:monospace}
</style>"""


def main() -> int:
    args = parse_args()
    page_folios_path = Path(args.page_folios_json).resolve()
    audit_dir = Path(args.audit_dir).resolve()
    output_html = Path(args.output_html).resolve()
    output_html.parent.mkdir(parents=True, exist_ok=True)

    if not page_folios_path.is_file():
        print(f"ERROR: page_folios.json not found: {page_folios_path}", file=sys.stderr)
        return 2
    if not audit_dir.is_dir():
        print(f"ERROR: audit dir not found: {audit_dir}", file=sys.stderr)
        return 2

    raw = json.loads(page_folios_path.read_text(encoding="utf-8"))
    verified = sidecar.load_sidecar_with_fallback(audit_dir, "folios_verified")
    flagged = sidecar.load_sidecar_with_fallback(audit_dir, "folios_flagged")

    # Normalize keys to ints; JSON keys are strings.
    records: dict[int, dict] = {}
    for k, v in raw.items():
        try:
            pg = int(k)
        except (TypeError, ValueError):
            continue
        if isinstance(v, dict):
            records[pg] = v

    page_sections: list[str] = []
    v_count = f_count = 0
    for pg in sorted(records):
        block, _, status = render_folio_chunk(pg, records[pg], verified, flagged)
        if status == "verified":
            v_count += 1
        elif status == "flagged":
            f_count += 1
        png_rel = f"{args.pages_dir_rel}/page_{pg:04d}.png"
        page_sections.append(
            page_strip.render_page_section(pg, png_rel, block, 1)
        )

    title = args.title or f"Folios audit — {page_folios_path.parent.parent.name}"
    doc = html_shell.render_audit_page(
        title=title,
        kind="folios",
        page_sections_html="".join(page_sections),
        nav_html=page_strip.render_nav(sorted(records)),
        initial_state={"verified": verified, "flagged": flagged},
        counts={"total": len(records), "verified": v_count, "flagged": f_count},
        instructions_html=INSTRUCTIONS_HTML,
        head_extras=FOLIO_HEAD_EXTRAS,
    )
    output_html.write_text(doc, encoding="utf-8")
    print(f"source={page_folios_path.parent.parent.name} kind=folios pages={len(records)} "
          f"verified={v_count} flagged={f_count} html={output_html.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
