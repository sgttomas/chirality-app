"""Generic HTML shell for a per-kind audit surface.

Wraps a pre-rendered list of page sections in:
  - sticky toolbar with stat counters + filter chips + export/reload/clear buttons
  - sticky nav strip of page anchors
  - localStorage state machine (radio change → save; textarea input → save)
  - timestamped sidecar export (`<source>_<kind>_verified_<TS>.json` etc.)

Kind-agnostic: the caller passes `kind` (e.g. `"figures"`) which scopes
the export filenames and the verified/flagged role keys.

Optional 4-state variant: when `extra_states` includes `"backcheck"`, the
shell renders an extra stat counter, filter chip, and CSS badge for the
backcheck state; the JS state machine reads `state.backcheck` from the
initial state and resolves it as the lowest-priority status (after
verified/flagged). The Backcheck state is *system-set* — there is no
radio chip for it. Reviewers leave Backcheck by picking Verified or Flag.
"""
from __future__ import annotations

import html
import json


def render_audit_page(
    title: str,
    kind: str,
    page_sections_html: str,
    nav_html: str,
    initial_state: dict,
    counts: dict,
    instructions_html: str = "",
    extra_states: list[str] | None = None,
    head_extras: str = "",
    js_extensions: str = "",
) -> str:
    """Compose the full audit HTML document.

    Args:
        title:               <title> + <h1> text.
        kind:                lowercase role slug (`figures` / `tables` / `images`
                             / `equations`). Drives the verified/flagged sidecar
                             filenames in the export buttons.
        page_sections_html:  concatenated output of `render_page_section()`.
        nav_html:            output of `render_nav()`.
        initial_state:       `{"verified": {...}, "flagged": {...}}` (plus
                             `"backcheck": {...}` for the 4-state variant).
        counts:              `{"total": N, "verified": V, "flagged": F}` (plus
                             `"backcheck": B` for the 4-state variant).
        instructions_html:   optional <details> block describing the surface.
        extra_states:        optional list of additional reviewer states beyond
                             unreviewed/verified/flagged. Only `"backcheck"` is
                             supported today.
        head_extras:         raw HTML injected into <head> after the base
                             <style> block (KaTeX <link>/<script>, extra
                             <style> for kind-specific chunk visuals, etc.).
        js_extensions:       raw JS injected at the end of the main <script>
                             block (KaTeX preview hooks, etc.).
    """
    extra_states = list(extra_states or [])
    has_backcheck = "backcheck" in extra_states

    initial_state_json = json.dumps(initial_state)
    total = counts.get("total", 0)
    verified_count = counts.get("verified", 0)
    flagged_count = counts.get("flagged", 0)
    backcheck_count = counts.get("backcheck", 0)
    unreviewed_count = total - verified_count - flagged_count - (backcheck_count if has_backcheck else 0)

    backcheck_css = """
.chunk[data-status="backcheck"]{background:#e6f0ff;border-color:#5a8fd0;opacity:1}
.chunk[data-status="backcheck"] .badge::before{content:"↻ backcheck";color:#0055aa;font-weight:bold}
body.only-backcheck .chunk:not([data-status="backcheck"]){display:none}
""" if has_backcheck else ""

    backcheck_stat = (
        f'  <span class="stat">↻ <b id="stat-backcheck">{backcheck_count}</b></span>\n'
        if has_backcheck else ""
    )
    backcheck_filter = (
        '    <label><input type="checkbox" id="only-backcheck"> Only backcheck</label>\n'
        if has_backcheck else ""
    )

    backcheck_js_apply = """
    else if (state.backcheck && state.backcheck[key]) status = "backcheck";""" if has_backcheck else ""

    backcheck_js_stats = """
  let b = 0;
  document.querySelectorAll(".chunk").forEach(el => {
    if (el.dataset.status === "backcheck") b++;
  });
  document.getElementById("stat-backcheck").textContent = b;""" if has_backcheck else ""

    backcheck_js_filter = """
document.getElementById("only-backcheck").addEventListener("change", e => {
  document.body.classList.toggle("only-backcheck", e.target.checked);
});""" if has_backcheck else ""

    # Unreviewed-count expression: 4-state subtracts backcheck too.
    unreviewed_expr = (
        "total - v - f - b" if has_backcheck else "total - v - f"
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:-apple-system,sans-serif;margin:0;padding:1rem;background:#fafafa}}
.toolbar{{position:sticky;top:0;background:#fff;padding:.5rem;border-bottom:1px solid #ddd;z-index:20;display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;font-size:.85rem}}
.toolbar button{{padding:.35rem .7rem;border:1px solid #888;background:#f5f5f5;border-radius:3px;cursor:pointer;font-size:.85rem}}
.toolbar button.primary{{background:#06c;color:#fff;border-color:#06c}}
.toolbar .stat{{margin-right:.5rem;color:#444}}
.toolbar .dirty{{color:#c60;font-weight:bold}}
.toolbar .filter label{{margin-right:.5rem;cursor:pointer}}
nav{{position:sticky;top:3rem;background:#fff;padding:.4rem .5rem;border-bottom:1px solid #ddd;font-size:.7rem;max-height:3.5rem;overflow-y:auto;z-index:15}}
nav a{{margin-right:.4rem;color:#06c;text-decoration:none}}
.page{{margin:1.5rem 0;border-top:2px solid #333;padding-top:1rem}}
.count{{color:#888;font-weight:normal;font-size:.8em}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;align-items:start}}
.img img{{width:100%;border:1px solid #ccc;background:#fff;position:sticky;top:7rem}}
.chunk{{margin-bottom:1rem;padding:.5rem;background:#fff;border:1px solid #ddd;border-radius:4px;transition:background .15s,opacity .15s}}
.chunk[data-status="verified"]{{background:#eef9ee;border-color:#9c9;opacity:.55}}
.chunk[data-status="flagged"]{{background:#fff4e6;border-color:#e8a04a;opacity:1}}
.chunk img.crop{{max-width:100%;border:1px solid #ccc;background:#fff;display:block;margin-bottom:.3rem}}
.chunk .caption{{font-size:.8em;color:#333;margin-bottom:.3rem}}
.chunk .ctrl{{display:flex;align-items:center;gap:.5rem;font-size:.75rem;color:#666;flex-wrap:wrap;margin-top:.3rem}}
.chunk .badge{{display:inline-block;min-width:1.5rem}}
.chunk[data-status="verified"] .badge::before{{content:"✓ verified";color:#080;font-weight:bold}}
.chunk[data-status="flagged"] .badge::before{{content:"⚠ flagged";color:#c60;font-weight:bold}}
.chunk .rb{{font-size:.75rem;color:#555;cursor:pointer}}
.chunk .rb input{{vertical-align:middle}}
.chunk textarea.flagnote{{display:none;width:100%;box-sizing:border-box;margin-top:.3rem;padding:.4rem;font-family:monospace;font-size:.85rem;border:1px solid #e8a04a;border-radius:3px;min-height:2rem;resize:vertical}}
.chunk[data-status="flagged"] textarea.flagnote{{display:block}}
.chunk .meta{{font-size:.7em;color:#888;font-family:monospace;margin-bottom:.2rem}}
.chunk .links a{{font-family:monospace;font-size:.75em;color:#06c;margin-right:.5rem}}
.chunk .needs-extraction{{color:#a00;font-weight:bold;font-size:.75em}}
body.hide-verified .chunk[data-status="verified"]{{display:none}}
body.only-flagged .chunk:not([data-status="flagged"]){{display:none}}
{backcheck_css}details.instructions{{margin:.75rem 0;padding:.5rem .75rem;background:#fffbe6;border:1px solid #e8d77a;border-radius:4px;font-size:.85rem}}
details.instructions summary{{cursor:pointer;font-weight:bold;color:#6a5a00}}
</style>
{head_extras}</head><body>
<div class="toolbar">
  <span class="stat">Kind: <b>{html.escape(kind)}</b></span>
  <span class="stat">Total: <b id="stat-total">{total}</b></span>
  <span class="stat">✓ <b id="stat-verified">{verified_count}</b></span>
  <span class="stat">⚠ <b id="stat-flagged">{flagged_count}</b></span>
{backcheck_stat}  <span class="stat">Unreviewed: <b id="stat-unreviewed">{unreviewed_count}</b></span>
  <span class="stat dirty" id="dirty-flag"></span>
  <span class="filter">
    <label><input type="checkbox" id="hide-verified"> Hide verified</label>
    <label><input type="checkbox" id="only-flagged"> Only flagged</label>
{backcheck_filter}  </span>
  <button onclick="exportSidecars()" class="primary">Export {kind}_verified.json + {kind}_flagged.json</button>
  <button onclick="reloadFromDisk()">Reload from disk</button>
  <button onclick="clearLocal()">Clear localStorage</button>
</div>
<nav>{nav_html}</nav>
<h1>{html.escape(title)}</h1>
{instructions_html}
{page_sections_html}
<script>
const KIND = {json.dumps(kind)};
const STORAGE_KEY = "audit:" + location.pathname;
const INITIAL = {initial_state_json};
let state = loadState();

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

let dirty = false;
function markDirty(d) {{
  dirty = d;
  document.getElementById("dirty-flag").textContent = d ? "● unsaved changes (Export to persist)" : "";
}}

function updateStats() {{
  const total = document.querySelectorAll(".chunk").length;
  let v=0, f=0;
  document.querySelectorAll(".chunk").forEach(el => {{
    const s = el.dataset.status;
    if (s === "verified") v++;
    else if (s === "flagged") f++;
  }});
  document.getElementById("stat-verified").textContent = v;
  document.getElementById("stat-flagged").textContent = f;{backcheck_js_stats}
  document.getElementById("stat-unreviewed").textContent = {unreviewed_expr};
}}

function applyStateToDOM() {{
  document.querySelectorAll(".chunk").forEach(el => {{
    const key = el.dataset.key;
    let status = "unreviewed";
    let note = "";
    if (state.verified && state.verified[key]) status = "verified";
    else if (state.flagged && state.flagged[key]) {{
      status = "flagged";
      note = state.flagged[key].description || "";
    }}{backcheck_js_apply}
    el.dataset.status = status;
    el.querySelectorAll('input[type=radio]').forEach(r => {{
      r.checked = (r.value === status);
    }});
    const ta = el.querySelector("textarea.flagnote");
    if (ta) ta.value = note;
  }});
  updateStats();
}}

document.addEventListener("change", e => {{
  if (e.target.matches('input[type=radio]')) {{
    const chunk = e.target.closest(".chunk");
    if (!chunk) return;
    const key = chunk.dataset.key;
    const status = e.target.value;
    chunk.dataset.status = status;
    if (status === "verified") {{
      state.verified = state.verified || {{}};
      state.verified[key] = {{
        asset_id: chunk.dataset.assetId || "",
        page: parseInt(chunk.dataset.page) || null,
        kind: chunk.dataset.kind || KIND,
        verified_at: new Date().toISOString().slice(0,10)
      }};
      if (state.flagged) delete state.flagged[key];
    }} else if (status === "flagged") {{
      const ta = chunk.querySelector("textarea.flagnote");
      const note = ta ? ta.value : "";
      state.flagged = state.flagged || {{}};
      state.flagged[key] = {{
        asset_id: chunk.dataset.assetId || "",
        page: parseInt(chunk.dataset.page) || null,
        kind: chunk.dataset.kind || KIND,
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
    const chunk = e.target.closest(".chunk");
    if (!chunk) return;
    const key = chunk.dataset.key;
    if (chunk.dataset.status === "flagged") {{
      state.flagged = state.flagged || {{}};
      state.flagged[key] = state.flagged[key] || {{
        asset_id: chunk.dataset.assetId || "",
        page: parseInt(chunk.dataset.page) || null,
        kind: chunk.dataset.kind || KIND,
        flagged_at: new Date().toISOString().slice(0,10)
      }};
      state.flagged[key].description = e.target.value;
      saveState();
    }}
  }}
}});

document.getElementById("hide-verified").addEventListener("change", e => {{
  document.body.classList.toggle("hide-verified", e.target.checked);
}});
document.getElementById("only-flagged").addEventListener("change", e => {{
  document.body.classList.toggle("only-flagged", e.target.checked);
}});{backcheck_js_filter}

function download(filename, data) {{
  const blob = new Blob([JSON.stringify(data, null, 2)], {{type:"application/json"}});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}}

function sourceSlug() {{
  const parts = location.pathname.split("/").filter(Boolean);
  const auditIdx = parts.lastIndexOf("audit");
  return (auditIdx > 0 ? parts[auditIdx - 1] : "audit").replace(/[^A-Za-z0-9._-]+/g, "_");
}}

function exportSidecars() {{
  const slug = sourceSlug();
  const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g,"-");
  download(`${{slug}}_${{KIND}}_verified_${{ts}}.json`, state.verified || {{}});
  download(`${{slug}}_${{KIND}}_flagged_${{ts}}.json`, state.flagged || {{}});
  markDirty(false);
}}

function reloadFromDisk() {{
  if (!confirm("Discard unsaved browser changes and reload state from the disk sidecars baked into this HTML?")) return;
  localStorage.removeItem(STORAGE_KEY);
  state = JSON.parse(JSON.stringify(INITIAL));
  applyStateToDOM();
  markDirty(false);
}}

function clearLocal() {{
  if (!confirm("Wipe all in-browser review state? (Does not touch the on-disk sidecars.)")) return;
  localStorage.removeItem(STORAGE_KEY);
  state = {{ verified: {{}}, flagged: {{}} }};
  applyStateToDOM();
  markDirty(false);
}}

applyStateToDOM();
{js_extensions}
</script>
</body></html>
"""
