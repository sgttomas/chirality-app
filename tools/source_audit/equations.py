"""Equations-specific glue for the shared per-kind audit-surface base.

Hosts the logic that's unique to `equations.html`:
  - scanning `page_NNNN.md` for `$$...$$` display blocks
  - hashing each block (`eqhash`) to derive the stable per-equation key
  - rendering one chunk per equation with a KaTeX preview pane, raw-LaTeX
    block, optional backcheck-note block, and a flag textarea with a
    live KaTeX preview
  - composing the surface via `html_shell.render_audit_page` with the
    `extra_states=["backcheck"]` 4-state variant, KaTeX head injections,
    and the preview-render JS extension
  - writing the equations JSONL stream that EQUATION_AUDIT Phase 3a
    consumes downstream

This module is consumed by `tools/equation_audit/audit_equations.py`,
which is a thin CLI wrapper.
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

from tools.source_audit import chunk as sa_chunk
from tools.source_audit import html_shell, page_strip, sidecar


DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
PAGE_RE = re.compile(r"^page_(\d{4})\.md$")


def eqhash(latex: str) -> str:
    """12-char content hash of stripped LaTeX. Stable per-equation key."""
    return sidecar.content_hash(latex)


def scan_pages(work_dir: Path) -> list[dict]:
    """Walk `page_NNNN.md` in `work_dir`, return one record per `$$...$$`.

    Each record: `{page, index, latex, hash, key, png}`. `key` is
    `<page>:<hash>`.
    """
    records: list[dict] = []
    for md in sorted(work_dir.glob("page_*.md")):
        m = PAGE_RE.match(md.name)
        if not m:
            continue
        page = int(m.group(1))
        text = md.read_text(encoding="utf-8")
        for idx, match in enumerate(DISPLAY_RE.finditer(text), 1):
            latex = match.group(1).strip()
            h = eqhash(latex)
            records.append({
                "page": page,
                "index": idx,
                "latex": latex,
                "hash": h,
                "key": f"{page}:{h}",
                "png": f"page_{page:04d}.png",
            })
    return records


def write_jsonl(records: list[dict], out_jsonl: Path) -> None:
    """Stream every equation record (sans the in-memory `key` field) to JSONL."""
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_jsonl.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps({k: v for k, v in r.items() if k != "key"}) + "\n")


def load_sidecars_with_legacy(audit_dir: Path) -> tuple[dict, dict, dict, dict]:
    """Load equations_verified/flagged/backcheck/rejected with the
    equation-specific legacy fallback paths preserved.

    The shared `sidecar.load_sidecar_with_fallback` already walks the
    flat audit dir and the nested `<kind>/working/` dir, including the
    bare role names. This wrapper keeps that surface explicit for the
    equations CLI's diagnostic messages.

    `equations_rejected.json` carries `(equation_hash, proposal_hash)`
    entries the reviewer has rejected from 1.5-P-emitted Backcheck
    proposals. It is a 1.5-P-era addition; no legacy fallback exists.
    """
    verified = sidecar.load_sidecar_with_fallback(audit_dir, "equations_verified")
    if not verified:
        verified = sidecar.load_sidecar_with_fallback(audit_dir, "verified")
    flagged = sidecar.load_sidecar_with_fallback(audit_dir, "equations_flagged")
    if not flagged:
        flagged = sidecar.load_sidecar_with_fallback(audit_dir, "flagged")
    backcheck = sidecar.load_sidecar_with_fallback(audit_dir, "equations_backcheck")
    if not backcheck:
        backcheck = sidecar.load_sidecar_with_fallback(audit_dir, "backcheck")
    rejected = sidecar.load_sidecar_with_fallback(audit_dir, "equations_rejected")
    return verified, flagged, backcheck, rejected


def _is_rejected(bc_entry: dict, rejected: dict) -> bool:
    """A 1.5-P backcheck proposal is suppressed iff its
    `(equation_hash, proposal_hash)` pair is in `equations_rejected.json`.

    Key encoding: `<equation_hash>:<proposal_hash>`. Entries that have no
    `proposal_hash` (legacy backcheck written by EQUATION_AUDIT-phase3)
    are never suppressed since there's nothing reviewer-rejected about
    a deterministic phase-3 fix.
    """
    eq_hash = bc_entry.get("hash") or bc_entry.get("equation_hash")
    prop_hash = bc_entry.get("proposal_hash")
    if not eq_hash or not prop_hash:
        return False
    return f"{eq_hash}:{prop_hash}" in rejected


KATEX_HEAD = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true}],throwOnError:false});window.__katexReady=true;document.dispatchEvent(new Event('katex-ready'));"></script>
<style>
.chunk.eq .eqhead{display:flex;align-items:center;gap:.5rem;font-size:.75rem;color:#666;margin-bottom:.25rem;flex-wrap:wrap}
.chunk.eq .eqnum{margin-right:.25rem}
.chunk.eq .hash{color:#aaa;font-size:.7rem}
.chunk.eq .sourcecrop{margin:.45rem 0 .6rem;padding:.45rem;background:#fff;border:1px solid #ccc;border-radius:3px}
.chunk.eq .sourcecrop img{display:block;max-width:100%;max-height:16rem;margin:0 auto;background:#fff;object-fit:contain}
.chunk.eq .sourcecrop figcaption{margin-top:.3rem;font-size:.68rem;color:#555;text-align:center}
.chunk.eq .auditpair{display:grid;grid-template-columns:minmax(0,1fr);gap:.4rem}
.chunk.eq .eqview{margin:.45rem 0 0;clear:both}
.chunk.eq .eqview-label{font-size:.68rem;font-weight:bold;color:#555;text-transform:uppercase;letter-spacing:.03em;margin:0 0 .2rem}
.chunk.eq .rendered{display:block;position:relative;min-height:2.6rem;margin:0 0 .55rem;padding:.55rem;background:#f5f5f5;border:1px solid #e2e2e2;border-radius:3px;overflow-x:auto}
.chunk.eq .rendered .katex-display{margin:.25rem 0}
.chunk.eq pre.src{display:block;position:relative;margin:0;padding:.55rem;background:#272822;color:#f8f8f2;border-radius:3px;font-size:.75rem;line-height:1.35;overflow-x:auto;white-space:pre-wrap}
.chunk.eq textarea.flagnote{min-height:3rem}
.chunk.eq .flagpreview{display:none;margin-top:.3rem;padding:.4rem .5rem;background:#fff;border:1px dashed #c88a3a;border-radius:3px;font-size:.85rem;overflow-x:auto}
.chunk.eq[data-status="flagged"] .flagpreview{display:block}
.chunk.eq .flagpreview .pvlabel{font-size:.7rem;color:#a06020;font-weight:bold;margin-bottom:.2rem}
.chunk.eq .flagpreview .pverror{color:#c30;font-style:italic;font-size:.8rem}
.chunk.eq .bcnote{margin:.3rem 0;padding:.4rem .5rem;background:#d4e4fa;border-left:3px solid #5a8fd0;border-radius:2px;font-size:.8rem}
.chunk.eq .bclabel{font-weight:bold;color:#0055aa;margin-bottom:.2rem}
.chunk.eq .bcdesc{color:#234;margin:.1rem 0}
.chunk.eq .bcdesc code{background:#fff;padding:.05rem .25rem;border-radius:2px;font-size:.85em}
.chunk.eq .bcsource{display:inline-block;margin-left:.5rem;padding:.05rem .35rem;border-radius:3px;font-size:.7em;font-weight:bold;letter-spacing:.02em}
.chunk.eq .bcsource-prefilter{background:#dde8ff;color:#0a3d8a;border:1px solid #5a8fd0}
.chunk.eq .bcsource-phase3{background:#e0f5e0;color:#0a5a0a;border:1px solid #6ab16a}
.chunk.eq .bcreject{margin-top:.2rem;padding:.2rem .5rem;font-size:.75rem;border:1px solid #c60;background:#fff5e6;color:#c60;cursor:pointer;border-radius:3px}
.chunk.eq .bcreject:hover{background:#ffe0c0}
</style>"""


PREVIEW_JS = """
function rejectProposal(btn) {
  const eq = btn.closest(".chunk.eq");
  if (!eq) return;
  const eqHash = btn.dataset.eqhash;
  const proposalHash = btn.dataset.proposalhash;
  const key = eq.dataset.key;
  if (!eqHash || !proposalHash) return;
  state.rejected = state.rejected || {};
  state.rejected[eqHash + ":" + proposalHash] = {
    equation_hash: eqHash,
    proposal_hash: proposalHash,
    rejected_at: new Date().toISOString().slice(0,10)
  };
  if (state.backcheck) delete state.backcheck[key];
  // Move chunk back to its non-backcheck baseline state.
  if (state.verified && state.verified[key]) { eq.dataset.status = "verified"; }
  else if (state.flagged && state.flagged[key]) { eq.dataset.status = "flagged"; }
  else { eq.dataset.status = "unreviewed"; }
  const bc = eq.querySelector(".bcnote"); if (bc) bc.remove();
  saveState();
}

const _origExportSidecars = exportSidecars;
exportSidecars = function() {
  _origExportSidecars();
  if (state.rejected && Object.keys(state.rejected).length > 0) {
    const slug = sourceSlug();
    const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g,"-");
    download(`${slug}_equations_rejected_${ts}.json`, state.rejected);
  }
};

function renderPreview(eq) {
  const ta = eq.querySelector("textarea.flagnote");
  const body = eq.querySelector(".flagpreview .pvbody");
  if (!ta || !body) return;
  const src = ta.value.trim();
  if (!window.katex) { body.textContent = src ? "(KaTeX loading...)" : ""; return; }
  if (!src) { body.innerHTML = '<span class="pverror">(empty — type LaTeX or a note above)</span>'; return; }
  try {
    katex.render(src, body, {throwOnError: true, displayMode: true, strict: "ignore"});
  } catch (err) {
    body.innerHTML = '<span class="pverror">(invalid LaTeX: ' + (err.message || err).replace(/&/g,'&amp;').replace(/</g,'&lt;') + ')</span>';
  }
}
function renderAllPreviews() {
  document.querySelectorAll('.chunk.eq[data-status="flagged"]').forEach(renderPreview);
}
document.addEventListener("katex-ready", renderAllPreviews);
if (window.__katexReady) renderAllPreviews();
document.addEventListener("input", e => {
  if (e.target.matches("textarea.flagnote")) {
    const eq = e.target.closest(".chunk.eq");
    if (eq) renderPreview(eq);
  }
});
document.addEventListener("change", e => {
  if (e.target.matches('input[type=radio][value="flagged"]')) {
    const eq = e.target.closest(".chunk.eq");
    if (eq) renderPreview(eq);
  }
});
"""


INSTRUCTIONS_HTML = """<details class="instructions" open>
<summary>How to use this audit</summary>
<p>Each display equation extracted from the source is shown rendered (via KaTeX) and as raw LaTeX, paired with the source page PNG on the left. When available, a clipped source image is shown inside the equation card above the rendered/transcribed text. Compare the transcription to the crop first, then use the full page for context.</p>
<p><b>Statuses</b> (four possible):</p>
<ul>
  <li><code>Unreviewed</code> — default; not yet looked at.</li>
  <li><code>✓ Verified</code> — transcription matches the printed equation; done.</li>
  <li><code>⚠ Flag</code> — transcription has an error. A text box opens for you to describe the correction needed.</li>
  <li><code>↻ Backcheck</code> — <i>automatically set by the system</i> after a fix is applied to a previously-flagged equation. Means "fix applied, please verify." You don't pick this status yourself; you respond to it by picking ✓ Verified (accept the fix) or ⚠ Flag (the fix is still wrong, describe further correction).</li>
</ul>
<p><b>Identity:</b> equations are keyed by a 12-char hash of the LaTeX string. If an equation's LaTeX changes (e.g. via a fix), its hash changes too — that's how Backcheck distinguishes "the equation Claude fixed" from "the original flagged one."</p>
</details>"""


def render_eq_chunk(
    record: dict,
    status: str,
    flag_note: str,
    backcheck_entry: dict,
    crop_rel: str | None = None,
) -> str:
    """Render one equation chunk: head + (optional backcheck note) +
    rendered preview + raw LaTeX + flag textarea + live KaTeX preview.

    When the backcheck entry carries `source: "1.5-P-machine"`, the note
    renders a source-provenance badge and a per-proposal Reject button
    that writes `(equation_hash, proposal_hash)` to a local rejected
    map (exported as `equations_rejected.json`).
    """
    key = record["key"]
    page = record["page"]
    h = record["hash"]
    latex = record["latex"]
    idx = record["index"]

    bc_block = ""
    if status == "backcheck" and backcheck_entry:
        bc_desc = html.escape(backcheck_entry.get("description", ""))
        bc_prev = html.escape(backcheck_entry.get("prev_latex", ""))
        bc_source = backcheck_entry.get("source", "EQUATION_AUDIT-phase3")
        bc_proposal_hash = html.escape(backcheck_entry.get("proposal_hash", ""))
        if bc_source == "1.5-P-machine":
            badge_html = '<span class="bcsource bcsource-prefilter">1.5-P-machine</span>'
        else:
            badge_html = '<span class="bcsource bcsource-phase3">EQUATION_AUDIT-phase3</span>'
        reject_btn = ""
        if bc_source == "1.5-P-machine" and bc_proposal_hash:
            reject_btn = (
                f'<button class="bcreject" type="button" '
                f'data-eqhash="{h}" data-proposalhash="{bc_proposal_hash}" '
                f'onclick="rejectProposal(this)">Reject proposal</button>'
            )
        bc_block = (
            f'<div class="bcnote">'
            f'<div class="bclabel">Fix applied — please backcheck {badge_html}</div>'
            + (f'<div class="bcdesc"><b>Original note:</b> {bc_desc}</div>' if bc_desc else "")
            + (f'<div class="bcdesc"><b>Previous LaTeX:</b> <code>{bc_prev}</code></div>' if bc_prev else "")
            + (f'<div class="bcdesc">{reject_btn}</div>' if reject_btn else "")
            + f'</div>'
        )

    crop_block = ""
    if crop_rel:
        crop_src = html.escape(crop_rel)
        crop_alt = html.escape(f"Source crop for page {page} equation {idx}")
        crop_block = (
            f'<figure class="sourcecrop">'
            f'<img class="crop" loading="lazy" src="{crop_src}" alt="{crop_alt}">'
            f'<figcaption>source crop · p. {page} · eq {idx}</figcaption>'
            f'</figure>'
        )

    return (
        f'<div class="chunk eq" data-kind="equation" data-key="{key}" '
        f'data-page="{page}" data-hash="{h}" data-status="{status}">'
        f'<div class="eqhead">'
        f'<span class="eqnum">eq {idx} <code class="hash">{h}</code></span>'
        f'<span class="badge"></span>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="unreviewed">Unreviewed</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="verified">✓ Verified</label>'
        f'<label class="rb"><input type="radio" name="s_{key}" value="flagged">⚠ Flag</label>'
        f'</div>'
        f'{bc_block}'
        f'{crop_block}'
        f'<div class="eqview"><div class="eqview-label">Rendered KaTeX</div>'
        f'<div class="rendered">$$ {html.escape(latex)} $$</div>'
        f'<div class="eqview-label">Raw LaTeX</div>'
        f'<pre class="src">{html.escape(latex)}</pre>'
        f'</div>'
        f'<textarea class="flagnote" placeholder="Type the corrected LaTeX, or a natural-language note (EQUATION_AUDIT Phase 3a will interpret prose notes to LaTeX before applying fixes)...">{html.escape(flag_note)}</textarea>'
        f'<div class="flagpreview"><div class="pvlabel">Preview (rendered from textarea)</div><div class="pvbody"></div></div>'
        f'</div>'
    )


def render_equations_audit_page(
    records: list[dict],
    audit_dir: Path,
    title: str,
    pages_dir_rel: str = "pages",
    crops_dir: Path | None = None,
) -> tuple[str, dict]:
    """Compose the full equations.html document.

    Returns `(html_doc, counts)` where counts is
    `{"total", "verified", "flagged", "backcheck"}`.
    """
    verified, flagged, backcheck, rejected = load_sidecars_with_legacy(audit_dir)
    crops_dir = crops_dir or (audit_dir / "crops")
    crops_dir = crops_dir.resolve() if crops_dir and crops_dir.exists() else None

    # Filter rejected 1.5-P proposals from the in-memory backcheck map
    # before passing it to the status resolver. This keeps re-renders
    # consistent with reviewer intent even when equations_backcheck.json
    # still contains the rejected entry.
    suppressed_backcheck: dict = {
        k: v for k, v in backcheck.items() if not _is_rejected(v, rejected)
    }

    pages = sorted({r["page"] for r in records})
    page_sections: list[str] = []
    v_count = f_count = b_count = 0

    for pg in pages:
        page_recs = [r for r in records if r["page"] == pg]
        png_rel = f"{pages_dir_rel}/page_{pg:04d}.png"
        eq_blocks: list[str] = []
        for r in page_recs:
            status, note = sa_chunk.initial_status_for_key(
                r["key"], verified, flagged, backcheck=suppressed_backcheck
            )
            bc_entry = suppressed_backcheck.get(r["key"], {}) if status == "backcheck" else {}
            crop_rel = None
            if crops_dir:
                crop_path = crops_dir / f'page_{r["page"]:04d}_eq_{r["index"]:02d}.png'
                if crop_path.exists():
                    crop_rel = os.path.relpath(crop_path, audit_dir)
            eq_blocks.append(render_eq_chunk(r, status, note, bc_entry, crop_rel))
            if status == "verified":
                v_count += 1
            elif status == "flagged":
                f_count += 1
            elif status == "backcheck":
                b_count += 1
        page_sections.append(
            page_strip.render_page_section(pg, png_rel, "".join(eq_blocks), len(page_recs))
        )

    counts = {
        "total": len(records),
        "verified": v_count,
        "flagged": f_count,
        "backcheck": b_count,
    }
    initial_state = {
        "verified": verified,
        "flagged": flagged,
        "backcheck": suppressed_backcheck,
        "rejected": rejected,
    }

    full_title = f"{title} ({len(records)} display equations across {len(pages)} pages)"
    doc = html_shell.render_audit_page(
        title=full_title,
        kind="equations",
        page_sections_html="".join(page_sections),
        nav_html=page_strip.render_nav(pages),
        initial_state=initial_state,
        counts=counts,
        instructions_html=INSTRUCTIONS_HTML,
        extra_states=["backcheck"],
        head_extras=KATEX_HEAD,
        js_extensions=PREVIEW_JS,
    )
    return doc, counts
