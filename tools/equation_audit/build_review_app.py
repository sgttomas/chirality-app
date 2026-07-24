#!/usr/bin/env python3
"""Build the equation review app: a single-file equations.html audit surface.

Replaces the page-strip chunk-list layout with a focused review app
designed for non-expert reviewers:

  - Left pane: the source page PNG, kept clean (no machine-drawn
    boxes), with a pen/highlighter/eraser toolbar. Marks are freehand
    SVG strokes stored in normalized page coordinates, so they stay
    glued to the page content, scale with it, and persist in
    localStorage (`ink:<pathname>`, keyed per page) — like marking a
    paper copy while working through the audit.
  - Right pane (width adjustable by dragging the splitter): ONE
    equation at a time — big KaTeX render, "It matches" / "Something's
    wrong" buttons, note box with live preview, skip, and auto-advance
    to the next unreviewed equation.

State model is bit-compatible with the classic surface: same
localStorage key (`audit:<pathname>`), same INITIAL baking from the
disk sidecars, same export filenames and JSON schemas
(`<slug>_equations_{verified,flagged}_<ts>.json`, plus
`_rejected` when 1.5-P proposals were rejected), so EQUATION_AUDIT
phases and browser state from the previous layout carry over unchanged.

Inputs (all under --audit-dir):
  equations.jsonl   one record per display equation (page, index, latex, hash)
  eq_bboxes.json    optional; page -> [{index, bbox_norm}] from
                    recover_eq_bboxes.py (equations without a bbox get
                    no highlight but remain reviewable)
  sidecars          equations_{verified,flagged,backcheck,rejected}.json
                    with the usual legacy fallbacks
  pages/            page_NNNN.png renders
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.source_audit import equations as eq_mod  # noqa: E402
from tools.source_audit import chunk as sa_chunk  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--audit-dir", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--out", default=None, help="default: <audit-dir>/equations.html")
    p.add_argument("--pages-dir-rel", default="pages")
    p.add_argument(
        "--state-epoch",
        default="",
        help=(
            "Optional salt appended to the browser-storage key. Bumping it "
            "makes the app ignore all previously saved in-browser answers — "
            "use when deliberately resetting the audit to a clean slate."
        ),
    )
    return p.parse_args()


def load_records(audit_dir: Path) -> list[dict]:
    records = []
    with (audit_dir / "equations.jsonl").open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r["key"] = f'{r["page"]}:{r["hash"]}'
            records.append(r)
    records.sort(key=lambda r: (r["page"], r["index"]))
    return records


def load_bboxes(audit_dir: Path) -> dict[tuple[int, int], list[float]]:
    path = audit_dir / "eq_bboxes.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for page_str, entries in data.items():
        for e in entries:
            out[(int(page_str), int(e["index"]))] = e["bbox_norm"]
    return out


def build_payload(records, bboxes, verified, flagged, backcheck) -> list[dict]:
    payload = []
    for r in records:
        status, note = sa_chunk.initial_status_for_key(
            r["key"], verified, flagged, backcheck=backcheck
        )
        entry = {
            "key": r["key"],
            "page": r["page"],
            "index": r["index"],
            "hash": r["hash"],
            "latex": r["latex"],
            "bbox": bboxes.get((r["page"], r["index"])),
        }
        bc = backcheck.get(r["key"]) if status == "backcheck" else None
        if bc:
            entry["bc"] = {
                "description": bc.get("description", ""),
                "prev_latex": bc.get("prev_latex", ""),
                "source": bc.get("source", "EQUATION_AUDIT-phase3"),
                "proposal_hash": bc.get("proposal_hash", ""),
            }
        payload.append(entry)
    return payload


def json_for_script(obj) -> str:
    """JSON safe to embed inside a <script> block."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def render_app(title: str, payload: list[dict], initial_state: dict,
               pages_dir_rel: str, state_epoch: str = "") -> str:
    pages = sorted({e["page"] for e in payload})
    return (
        APP_TEMPLATE
        .replace("__TITLE__", title)
        .replace("__EQS_JSON__", json_for_script(payload))
        .replace("__INITIAL_JSON__", json_for_script(initial_state))
        .replace("__PAGES_JSON__", json_for_script(pages))
        .replace("__PAGES_DIR__", pages_dir_rel)
        .replace("__STATE_EPOCH__", state_epoch)
    )


def main() -> int:
    args = parse_args()
    audit_dir = Path(args.audit_dir).resolve()
    out_html = Path(args.out).resolve() if args.out else audit_dir / "equations.html"

    records = load_records(audit_dir)
    bboxes = load_bboxes(audit_dir)
    verified, flagged, backcheck, rejected = eq_mod.load_sidecars_with_legacy(audit_dir)
    suppressed_bc = {k: v for k, v in backcheck.items()
                     if not eq_mod._is_rejected(v, rejected)}

    payload = build_payload(records, bboxes, verified, flagged, suppressed_bc)
    initial_state = {
        "verified": verified,
        "flagged": flagged,
        "backcheck": suppressed_bc,
        "rejected": rejected,
    }
    doc = render_app(args.title, payload, initial_state, args.pages_dir_rel,
                     state_epoch=args.state_epoch)
    out_html.write_text(doc, encoding="utf-8")

    with_bbox = sum(1 for e in payload if e["bbox"])
    print(f"equations={len(payload)} pages={len({e['page'] for e in payload})} "
          f"with_bbox={with_bbox} html={out_html}")
    return 0


APP_TEMPLATE = r"""<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — equation check</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"
  onload="window.__katexReady=true;document.dispatchEvent(new Event('katex-ready'));"></script>
<style>
:root{
  --ok:#2e9e44; --ok-bg:#e7f7ea; --bad:#e07b00; --bad-bg:#fdf1e2;
  --bc:#3572d8; --bc-bg:#e8f0fd; --cur:#2563eb; --ink:#1f2430; --mut:#6b7280;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{font-family:-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:#f3f4f6;
  display:flex;flex-direction:column;overflow:hidden}

/* ---------- header ---------- */
header{background:#fff;border-bottom:2px solid #e5e7eb;padding:.55rem 1rem;
  display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
header h1{font-size:1rem;margin:0;white-space:nowrap}
#home-btn{display:inline-block;background:#fff;border:1px solid #d1d5db;border-radius:8px;
  padding:.4rem .7rem;font-size:.88rem;font-weight:600;color:var(--ink);text-decoration:none;white-space:nowrap}
#home-btn:hover{background:#f3f4f6}
.progress{flex:1;min-width:180px;display:flex;align-items:center;gap:.6rem}
.pbar{flex:1;height:14px;background:#e5e7eb;border-radius:7px;overflow:hidden;display:flex}
.pbar .pv{background:var(--ok);height:100%;transition:width .3s}
.pbar .pf{background:var(--bad);height:100%;transition:width .3s}
.ptext{font-size:.85rem;color:var(--mut);white-space:nowrap}
button{font-family:inherit;cursor:pointer;border-radius:8px;border:1px solid #d1d5db;background:#fff;
  padding:.45rem .8rem;font-size:.9rem}
button:hover{filter:brightness(.97)}
#save-btn{background:#111827;color:#fff;border-color:#111827;font-weight:600}
#dirty-flag{color:var(--bad);font-size:.8rem;min-width:1rem}
.menu{position:relative}
.menu-items{display:none;position:absolute;right:0;top:110%;background:#fff;border:1px solid #d1d5db;
  border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.12);z-index:50;min-width:230px;padding:.3rem}
.menu.open .menu-items{display:block}
.menu-items button{display:block;width:100%;text-align:left;border:none;background:none;padding:.5rem .7rem}
.menu-items button:hover{background:#f3f4f6}

/* ---------- main split ---------- */
main{flex:1;display:flex;min-height:0}
#page-pane{flex:1.15;min-width:0;overflow:auto;background:#565c66;padding:1rem;position:relative}
#page-wrap{position:relative;margin:0 auto;max-width:1100px}
#rot-box{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100%}
#rot-box img{display:block;width:100%;background:#fff;border-radius:4px;box-shadow:0 2px 14px rgba(0,0,0,.35)}
#ink{position:absolute;inset:0;width:100%;height:100%;touch-action:none}
#ink.pen{cursor:crosshair}
#ink.hi{cursor:crosshair}
#ink.eraser{cursor:cell}
#ink.fence{cursor:crosshair}
#pen-bar{position:sticky;top:0;z-index:10;display:flex;gap:.35rem;align-items:center;
  background:rgba(17,24,39,.88);border-radius:10px;padding:.3rem .45rem;width:max-content;
  margin:0 auto .6rem;box-shadow:0 2px 10px rgba(0,0,0,.35)}
#pen-bar button{background:none;border:none;border-radius:7px;font-size:1.05rem;padding:.25rem .45rem;color:#fff}
#pen-bar #zoom-reset{font-size:.78rem;min-width:3.1rem;text-align:center}
#pen-bar button:hover{background:rgba(255,255,255,.14)}
#pen-bar button.active{background:#2563eb}
#pen-bar .sep{width:1px;height:1.2rem;background:rgba(255,255,255,.25)}

/* ---------- review pane ---------- */
#splitter{flex:0 0 7px;cursor:col-resize;background:#e5e7eb;position:relative;z-index:5}
#splitter:hover,#splitter.dragging{background:#93c5fd}
#splitter::after{content:"⋮";position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  color:#6b7280;font-size:.9rem}
#review-pane{flex:0 0 var(--review-w,460px);min-width:300px;max-width:75vw;overflow-y:auto;background:#fff;
  padding:1rem;display:flex;flex-direction:column;gap:.75rem}
.crumb{font-size:.85rem;color:var(--mut)}
.crumb b{color:var(--ink)}
#status-chip{display:inline-block;padding:.15rem .6rem;border-radius:999px;font-size:.78rem;font-weight:700}
#status-chip.unreviewed{background:#eef0f3;color:#4b5563}
#status-chip.verified{background:var(--ok-bg);color:var(--ok)}
#status-chip.flagged{background:var(--bad-bg);color:var(--bad)}
#status-chip.backcheck{background:var(--bc-bg);color:var(--bc)}
#bc-banner{display:none;background:var(--bc-bg);border-left:4px solid var(--bc);border-radius:6px;
  padding:.6rem .8rem;font-size:.85rem}
#bc-banner .bctitle{font-weight:700;color:var(--bc);margin-bottom:.25rem}
#bc-banner code{background:#fff;padding:.05rem .3rem;border-radius:3px}
#bc-banner button{margin-top:.4rem;font-size:.78rem;color:#b45309;border-color:#d97706;background:#fffbeb}
#eq-render{background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:1rem .8rem;
  font-size:1.3rem;overflow-x:auto;min-height:4.4rem;text-align:center}
#eq-render .katex-display{margin:.2rem 0;width:max-content;min-width:100%}
.ask{font-size:1rem;font-weight:600;text-align:center}
.ask .nudge{display:block;font-size:.8rem;font-weight:400;color:var(--mut);margin-top:.15rem}
.answers{display:flex;gap:.6rem}
.answers button{flex:1;font-size:1.02rem;font-weight:700;padding:.85rem .5rem;border-width:2px}
#btn-yes{background:var(--ok-bg);border-color:var(--ok);color:var(--ok)}
#btn-no{background:var(--bad-bg);border-color:var(--bad);color:var(--bad)}
.subrow{display:flex;gap:.6rem;align-items:center;justify-content:center;font-size:.85rem}
.subrow button{border:none;background:none;color:var(--mut);text-decoration:underline;padding:.2rem .4rem}
#flag-panel{display:none;background:var(--bad-bg);border:2px solid var(--bad);border-radius:10px;padding:.7rem}
#flag-panel label{font-size:.85rem;font-weight:600;color:#92400e}
#flag-panel textarea{width:100%;min-height:4.2rem;margin:.4rem 0;border-radius:6px;border:1px solid #d1d5db;
  padding:.5rem;font-size:.92rem;font-family:inherit}
#flag-preview{background:#fff;border:1px dashed var(--bad);border-radius:6px;padding:.45rem .6rem;
  font-size:1rem;min-height:1.6rem;overflow-x:auto}
#flag-preview .pverror{color:var(--mut);font-style:italic;font-size:.8rem}
#flag-panel .actions{display:flex;gap:.5rem;margin-top:.5rem}
#flag-save{background:var(--bad);border-color:var(--bad);color:#fff;font-weight:700}
.latexblock .label{font-size:.72rem;font-weight:700;color:var(--mut);text-transform:uppercase;
  letter-spacing:.04em;margin-bottom:.25rem}
.latexblock pre{margin:0;background:#272822;color:#f8f8f2;padding:.55rem;border-radius:6px;
  white-space:pre-wrap;font-size:.8rem;user-select:all}
.navrow{display:flex;gap:.5rem;align-items:center;justify-content:space-between;margin-top:auto;
  padding-top:.6rem;border-top:1px solid #e5e7eb}
.navrow .keys{font-size:.72rem;color:var(--mut)}
kbd{background:#eef0f3;border:1px solid #d1d5db;border-bottom-width:2px;border-radius:4px;
  padding:0 .32rem;font-size:.72rem}
#done-card{display:none;text-align:center;padding:2rem 1rem;font-size:1.1rem}
#done-card .big{font-size:2.6rem}

/* ---------- page strip ---------- */
#page-strip{display:flex;gap:3px;flex-wrap:wrap;background:#fff;border-top:2px solid #e5e7eb;
  padding:.45rem 1rem;max-height:5.4rem;overflow-y:auto}
.pdot{width:14px;height:14px;border-radius:3px;background:#d1d5db;cursor:pointer;border:2px solid transparent}
.pdot.some{background:linear-gradient(135deg,var(--ok) 50%,#d1d5db 50%)}
.pdot.done{background:var(--ok)}
.pdot.hasflag{background:var(--bad)}
.pdot.current{border-color:var(--cur)}
</style></head>
<body>
<header>
  <a id="home-btn" href="../../index.html" title="back to the list of books">🏠 Home</a>
  <h1>__TITLE__</h1>
  <div class="progress">
    <div class="pbar"><div class="pv" id="pv"></div><div class="pf" id="pf"></div></div>
    <span class="ptext" id="ptext"></span>
  </div>
  <button id="next-unreviewed">Next unchecked ▸</button>
  <span id="dirty-flag"></span>
  <button id="save-btn" title="Writes your answers into the book's audit folder (first time: pick that folder once)">💾 Save my work</button>
  <div class="menu" id="gear-menu">
    <button aria-label="more">⚙</button>
    <div class="menu-items">
      <button id="reload-disk">Reload state from disk sidecars</button>
      <button id="clear-local">Clear in-browser answers</button>
    </div>
  </div>
</header>

<main>
  <div id="page-pane">
    <div id="pen-bar">
      <button id="tool-pen" title="pen — draw thin red lines">🖊️</button>
      <button id="tool-hi" title="highlighter — thick yellow marker">🖍️</button>
      <button id="tool-eraser" title="eraser — rub out marks">🧽</button>
      <button id="tool-fence" title="fence — drag a box to copy that part of the page as a picture (paste it anywhere)">✂️</button>
      <span class="sep"></span>
      <button id="ink-undo" title="undo last mark on this page">↩️</button>
      <button id="ink-clear" title="erase every mark on this page">🗑️</button>
      <span class="sep"></span>
      <button id="page-rotate" title="rotate the page a quarter turn (for upside-down or sideways scans)">🔄</button>
      <span class="sep"></span>
      <button id="zoom-out" title="zoom out (or pinch / ctrl+scroll on the page)">➖</button>
      <button id="zoom-reset" title="back to fit">100%</button>
      <button id="zoom-in" title="zoom in (or pinch / ctrl+scroll on the page)">➕</button>
    </div>
    <div id="page-wrap">
      <div id="rot-box">
        <img id="page-img" alt="source page">
        <svg id="ink" class="pen"></svg>
      </div>
    </div>
  </div>
  <div id="splitter"></div>
  <div id="review-pane">
    <div class="crumb">Page <b id="crumb-page"></b> · equation <b id="crumb-idx"></b> of <b id="crumb-count"></b> on this page
      &nbsp;<span id="status-chip"></span></div>
    <div id="bc-banner"></div>
    <div id="eq-render"></div>
    <div class="ask">Find this equation on the page — does it match what's printed?</div>
    <div class="answers">
      <button id="btn-yes">✓ Yes, it matches</button>
      <button id="btn-no">✗ Something's wrong</button>
    </div>
    <div class="subrow">
      <button id="btn-skip">Skip for now →</button>
      <button id="btn-clear">Clear my answer</button>
    </div>
    <div id="flag-panel">
      <label>What's wrong? Type the correct math (LaTeX) if you can, or just describe it in plain words:</label>
      <textarea id="flag-note" placeholder="e.g. 'the 2 should be a superscript' — plain English is fine!"></textarea>
      <div id="flag-preview"></div>
      <div class="actions">
        <button id="flag-save">⚠ Save flag</button>
        <button id="flag-cancel">Cancel</button>
      </div>
    </div>
    <div class="latexblock"><div class="label">LaTeX text</div><pre id="eq-src"></pre></div>
    <div id="done-card"><div class="big">🎉</div>Every equation has been checked!<br>
      Hit <b>💾 Save my work</b> to keep your answers.</div>
    <div class="navrow">
      <button id="btn-prev">‹ Back</button>
      <span class="keys"><kbd>Y</kbd> yes · <kbd>N</kbd> wrong · <kbd>S</kbd> skip · <kbd>←</kbd><kbd>→</kbd> move</span>
      <button id="btn-next">Next ›</button>
    </div>
  </div>
</main>
<div id="page-strip"></div>

<script>
const KIND = "equations";
const STATE_EPOCH = "__STATE_EPOCH__"; /* bumped on deliberate resets */
const STORAGE_KEY = "audit:" + location.pathname + (STATE_EPOCH ? "#" + STATE_EPOCH : "");
const EQS = __EQS_JSON__;
const INITIAL = __INITIAL_JSON__;
const PAGES = __PAGES_JSON__;
const PAGES_DIR = "__PAGES_DIR__";

let state = loadState();
let cur = 0;

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) { try { return JSON.parse(raw); } catch(e) {} }
  return JSON.parse(JSON.stringify(INITIAL));
}
let dirty = false;
function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  dirty = true;
  document.getElementById("dirty-flag").textContent = "●";
  document.getElementById("save-btn").title = "You have unsaved answers — download them!";
}
function statusOf(eq) {
  if (state.verified && state.verified[eq.key]) return "verified";
  if (state.flagged && state.flagged[eq.key]) return "flagged";
  if (state.backcheck && state.backcheck[eq.key]) return "backcheck";
  return "unreviewed";
}
function noteOf(eq) {
  return (state.flagged && state.flagged[eq.key] && state.flagged[eq.key].description) || "";
}

/* ---------- actions ---------- */
function setVerified(eq) {
  state.verified = state.verified || {};
  state.verified[eq.key] = { page: eq.page, hash: eq.hash, kind: KIND,
    verified_at: new Date().toISOString().slice(0,10) };
  if (state.flagged) delete state.flagged[eq.key];
  if (state.backcheck) delete state.backcheck[eq.key];
  saveState();
}
function setFlagged(eq, note) {
  state.flagged = state.flagged || {};
  state.flagged[eq.key] = { page: eq.page, hash: eq.hash, kind: KIND,
    description: note, flagged_at: new Date().toISOString().slice(0,10) };
  if (state.verified) delete state.verified[eq.key];
  if (state.backcheck) delete state.backcheck[eq.key];
  saveState();
}
function clearAnswer(eq) {
  if (state.verified) delete state.verified[eq.key];
  if (state.flagged) delete state.flagged[eq.key];
  saveState();
}
function rejectProposal(eq) {
  const bc = eq.bc; if (!bc || !bc.proposal_hash) return;
  state.rejected = state.rejected || {};
  state.rejected[eq.hash + ":" + bc.proposal_hash] = {
    equation_hash: eq.hash, proposal_hash: bc.proposal_hash,
    rejected_at: new Date().toISOString().slice(0,10) };
  if (state.backcheck) delete state.backcheck[eq.key];
  saveState();
  render();
}

/* ---------- export / reset ---------- */
function download(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}
function sourceSlug() {
  const parts = location.pathname.split("/").filter(Boolean);
  const i = parts.lastIndexOf("audit");
  return (i > 0 ? parts[i-1] : "audit").replace(/[^A-Za-z0-9._-]+/g, "_");
}
function exportSidecars() {
  const slug = sourceSlug();
  const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g,"-");
  download(`${slug}_${KIND}_verified_${ts}.json`, state.verified || {});
  download(`${slug}_${KIND}_flagged_${ts}.json`, state.flagged || {});
  if (state.rejected && Object.keys(state.rejected).length > 0) {
    download(`${slug}_${KIND}_rejected_${ts}.json`, state.rejected);
  }
  dirty = false;
  document.getElementById("dirty-flag").textContent = "";
}

/* ---------- direct save into the audit folder (File System Access API) ---------- */
function idbOpen() {
  return new Promise((res, rej) => {
    const rq = indexedDB.open("audit-app", 1);
    rq.onupgradeneeded = () => rq.result.createObjectStore("handles");
    rq.onsuccess = () => res(rq.result);
    rq.onerror = () => rej(rq.error);
  });
}
async function idbGet(key) {
  const db = await idbOpen();
  return new Promise((res, rej) => {
    const rq = db.transaction("handles").objectStore("handles").get(key);
    rq.onsuccess = () => res(rq.result); rq.onerror = () => rej(rq.error);
  });
}
async function idbSet(key, val) {
  const db = await idbOpen();
  return new Promise((res, rej) => {
    const tx = db.transaction("handles", "readwrite");
    tx.objectStore("handles").put(val, key);
    tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error);
  });
}
let auditDirHandle = null; /* in-memory cache: one picker prompt per session at most */
async function getAuditDirHandle() {
  let h = auditDirHandle;
  if (!h) { try { h = await idbGet(location.pathname); } catch(e) {} }
  if (h) {
    try {
      if (await h.queryPermission({mode:"readwrite"}) === "granted") { auditDirHandle = h; return h; }
      if (await h.requestPermission({mode:"readwrite"}) === "granted") { auditDirHandle = h; return h; }
    } catch(e) {}
  }
  h = await window.showDirectoryPicker({ id: "audit-dir", mode: "readwrite" });
  h = await resolveAuditDir(h);
  auditDirHandle = h;
  try { await idbSet(location.pathname, h); } catch(e) {}
  return h;
}
async function resolveAuditDir(h) {
  /* accept the audit dir itself, or walk down if they picked a parent
     (the book folder, or _Sources with the book one level up) */
  const looksRight = async d => {
    try { await d.getFileHandle("equations.jsonl"); return true; } catch(e) { return false; }
  };
  if (await looksRight(h)) return h;
  const parts = location.pathname.split("/");
  const book = parts[parts.length - 3]; /* .../<book>/audit/equations.html */
  for (const rel of [["audit"], [book, "audit"]]) {
    try {
      let d = h;
      for (const seg of rel) d = await d.getDirectoryHandle(seg);
      if (await looksRight(d)) return d;
    } catch(e) {}
  }
  if (!confirm("Hmm — that folder doesn't look like this book's audit folder " +
               "(no equations.jsonl inside). Use it anyway?")) {
    const err = new Error("wrong folder"); err.name = "AbortError"; throw err;
  }
  return h;
}
async function forgetAuditDirHandle() {
  auditDirHandle = null;
  try {
    const db = await idbOpen();
    await new Promise((res, rej) => {
      const tx = db.transaction("handles", "readwrite");
      tx.objectStore("handles").delete(location.pathname);
      tx.oncomplete = () => res(); tx.onerror = () => rej(tx.error);
    });
  } catch(e) {}
}
async function writeJSONFile(dir, name, obj) {
  const fh = await dir.getFileHandle(name, { create: true });
  const w = await fh.createWritable();
  await w.write(JSON.stringify(obj, null, 2) + "\n");
  await w.close();
}
function toast(msg, ok) {
  let t = document.getElementById("toast");
  if (!t) {
    t = document.createElement("div"); t.id = "toast";
    t.style.cssText = "position:fixed;bottom:5.5rem;left:50%;transform:translateX(-50%);" +
      "padding:.6rem 1.1rem;border-radius:10px;font-size:.95rem;font-weight:600;z-index:99;" +
      "box-shadow:0 4px 16px rgba(0,0,0,.25);transition:opacity .4s";
    document.body.appendChild(t);
  }
  t.style.background = ok ? "#e7f7ea" : "#fdf1e2";
  t.style.color = ok ? "#166a2b" : "#92400e";
  t.style.border = "2px solid " + (ok ? "#2e9e44" : "#e07b00");
  t.textContent = msg; t.style.opacity = "1";
  clearTimeout(t._h);
  t._h = setTimeout(() => { t.style.opacity = "0"; }, 4000);
}
async function saveWork() {
  if (window.showDirectoryPicker) {
    try {
      const dir = await getAuditDirHandle();
      await writeJSONFile(dir, "equations_verified.json", state.verified || {});
      await writeJSONFile(dir, "equations_flagged.json", state.flagged || {});
      if (state.rejected && Object.keys(state.rejected).length > 0) {
        await writeJSONFile(dir, "equations_rejected.json", state.rejected);
      }
      dirty = false;
      document.getElementById("dirty-flag").textContent = "";
      toast("Saved ✓ — your answers are in the audit folder", true);
      return;
    } catch(e) {
      if (e && e.name === "AbortError") { toast("Save cancelled — nothing was written", false); return; }
      console.warn("direct save failed; falling back to download", e);
    }
  }
  exportSidecars();
  toast("Downloaded your answers — move the files into the audit folder", false);
}

/* ---------- page image ---------- */
let shownPage = null;
function pad4(n){ return String(n).padStart(4,"0"); }
function showPage(page) {
  if (shownPage === page) return;
  shownPage = page;
  document.getElementById("page-img").src = `${PAGES_DIR}/page_${pad4(page)}.png`;
  document.getElementById("page-pane").scrollTo({top:0});
  applyRotation();
  renderInk();
}

/* ---------- page rotation (remembered per page) ---------- */
const ROT_KEY = "rot:" + location.pathname;
let rotMap = (() => { try { return JSON.parse(localStorage.getItem(ROT_KEY)) || {}; } catch(e) { return {}; } })();
function pageRotation() { return rotMap[shownPage] || 0; }
function applyRotation() {
  const img = document.getElementById("page-img");
  const wrap = document.getElementById("page-wrap");
  const box = document.getElementById("rot-box");
  const deg = pageRotation();
  const nw = img.naturalWidth || 1000, nh = img.naturalHeight || 1400;
  if (deg % 180 === 0) {
    wrap.style.aspectRatio = `${nw} / ${nh}`;
    box.style.width = "100%";
  } else {
    wrap.style.aspectRatio = `${nh} / ${nw}`;
    box.style.width = wrap.clientHeight ? wrap.clientHeight + "px" : (wrap.clientWidth * nh / nw) + "px";
  }
  box.style.transform = `translate(-50%,-50%) rotate(${deg}deg)`;
  /* second pass once the aspect-ratio has settled the wrap height */
  if (deg % 180 !== 0) requestAnimationFrame(() => {
    box.style.width = wrap.clientHeight + "px";
  });
}
function rotatePage() {
  rotMap[shownPage] = (pageRotation() + 90) % 360;
  if (!rotMap[shownPage]) delete rotMap[shownPage];
  localStorage.setItem(ROT_KEY, JSON.stringify(rotMap));
  applyRotation();
}

/* ---------- zoom ---------- */
const BASE_MAX_W = 1100;
let zoom = Number(localStorage.getItem("ui:zoom")) || 1;
function applyZoom() {
  const wrap = document.getElementById("page-wrap");
  wrap.style.width = (zoom * 100) + "%";
  wrap.style.maxWidth = (zoom * BASE_MAX_W) + "px";
  document.getElementById("zoom-reset").textContent = Math.round(zoom * 100) + "%";
  applyRotation();
}
function setZoom(z, cx, cy) {
  const pane = document.getElementById("page-pane");
  const wrap = document.getElementById("page-wrap");
  z = Math.max(0.4, Math.min(5, z));
  if (z === zoom) return;
  /* keep the point under (cx, cy) fixed while the page rescales */
  const r = wrap.getBoundingClientRect();
  const px = cx === undefined ? .5 : (cx - r.left) / r.width;
  const py = cy === undefined ? .5 : (cy - r.top) / r.height;
  const factor = z / zoom;
  zoom = z;
  localStorage.setItem("ui:zoom", String(zoom));
  applyZoom();
  const r2 = wrap.getBoundingClientRect();
  pane.scrollLeft += (r2.width * px + r2.left) - (cx === undefined ? r.left + r.width * px : cx);
  pane.scrollTop  += (r2.height * py + r2.top) - (cy === undefined ? r.top + r.height * py : cy);
}

/* ---------- pen & highlighter (marks live in page coordinates) ---------- */
const INK_KEY = "ink:" + location.pathname;
const INK_W = 1000; /* stroke coords are stored in a 1000-wide page space */
let inkAll = loadInk();       /* {"<page>": [ {tool, pts:[[x,y],...]}, ... ]} */
let inkTool = "pen";
let drawing = null;

function loadInk() {
  try { return JSON.parse(localStorage.getItem(INK_KEY)) || {}; } catch(e) { return {}; }
}
function saveInk() { localStorage.setItem(INK_KEY, JSON.stringify(inkAll)); }
function pageStrokes() { return inkAll[shownPage] = inkAll[shownPage] || []; }

function inkSvg() { return document.getElementById("ink"); }
function inkViewH() {
  const img = document.getElementById("page-img");
  return img.naturalWidth ? INK_W * img.naturalHeight / img.naturalWidth : INK_W * 1.4;
}
function strokePath(s) {
  const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
  p.setAttribute("d", "M" + s.pts.map(pt => pt[0].toFixed(1) + " " + pt[1].toFixed(1)).join(" L"));
  p.setAttribute("fill", "none");
  p.setAttribute("stroke-linecap", "round");
  p.setAttribute("stroke-linejoin", "round");
  if (s.tool === "hi") {
    p.setAttribute("stroke", "#ffe24a"); p.setAttribute("stroke-width", "14");
    p.setAttribute("opacity", "0.45");
  } else {
    p.setAttribute("stroke", "#e02020"); p.setAttribute("stroke-width", "2.2");
    p.setAttribute("opacity", "0.9");
  }
  return p;
}
function renderInk() {
  const svg = inkSvg();
  svg.setAttribute("viewBox", `0 0 ${INK_W} ${inkViewH()}`);
  svg.innerHTML = "";
  (inkAll[shownPage] || []).forEach(s => svg.appendChild(strokePath(s)));
}
function inkPoint(e) {
  /* map through the SVG's screen matrix so drawing works at any rotation */
  const svg = inkSvg();
  const ctm = svg.getScreenCTM();
  if (ctm) {
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(ctm.inverse());
    return [p.x, p.y];
  }
  const r = svg.getBoundingClientRect();
  return [ (e.clientX - r.left) / r.width * INK_W,
           (e.clientY - r.top) / r.height * inkViewH() ];
}
function eraseNear(pt) {
  const strokes = pageStrokes();
  const R = 12;
  const hit = strokes.findIndex(s => s.pts.some(p =>
    (p[0]-pt[0])**2 + (p[1]-pt[1])**2 < R*R));
  if (hit >= 0) { strokes.splice(hit, 1); saveInk(); renderInk(); }
}
function setInkTool(t) {
  inkTool = t;
  inkSvg().setAttribute("class", t);
  ["pen","hi","eraser","fence"].forEach(x =>
    document.getElementById("tool-" + x).classList.toggle("active", x === t));
}

/* ---------- fence: copy a region of the page as a PNG ---------- */
function fenceRectEl() {
  let r = document.getElementById("fence-rect");
  if (!r) {
    r = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    r.id = "fence-rect";
    r.setAttribute("fill", "rgba(37,99,235,.12)");
    r.setAttribute("stroke", "#2563eb");
    r.setAttribute("stroke-width", "2.5");
    r.setAttribute("stroke-dasharray", "8 5");
  }
  inkSvg().appendChild(r);
  return r;
}
function setFenceRect(el, a, b) {
  const x = Math.min(a[0], b[0]), y = Math.min(a[1], b[1]);
  el.setAttribute("x", x); el.setAttribute("y", y);
  el.setAttribute("width", Math.abs(a[0]-b[0])); el.setAttribute("height", Math.abs(a[1]-b[1]));
}
function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}
async function copyFenceRegion(a, b) {
  const x0 = Math.min(a[0], b[0]), y0 = Math.min(a[1], b[1]);
  const w = Math.abs(a[0]-b[0]), h = Math.abs(a[1]-b[1]);
  if (w < 8 || h < 8) return; /* accidental click */
  try {
    toast("Copying…", true);
    let file = null;
    for (let attempt = 0; attempt < 2 && !file; attempt++) {
      const dir = await getAuditDirHandle();
      try {
        const pagesDir = await dir.getDirectoryHandle(PAGES_DIR);
        const fh = await pagesDir.getFileHandle(`page_${pad4(shownPage)}.png`);
        file = await fh.getFile();
      } catch(e) {
        /* remembered folder is wrong or stale — forget it and re-prompt once */
        if (attempt === 0) { await forgetAuditDirHandle(); toast("That folder didn't have the page images — pick the book's audit folder", false); }
        else throw e;
      }
    }
    const bmp = await createImageBitmap(file);
    const s = bmp.width / INK_W; /* page-space -> natural pixels (same scale both axes) */
    const sw = Math.max(1, Math.round(w*s)), sh = Math.max(1, Math.round(h*s));
    const deg = pageRotation();
    const c = document.createElement("canvas");
    c.width = deg % 180 ? sh : sw;
    c.height = deg % 180 ? sw : sh;
    const ctx = c.getContext("2d");
    ctx.translate(c.width/2, c.height/2);
    ctx.rotate(deg * Math.PI / 180);
    ctx.drawImage(bmp, Math.round(x0*s), Math.round(y0*s), sw, sh, -sw/2, -sh/2, sw, sh);
    /* toDataURL (sync) — canvas.toBlob's callback can fail to fire inside pointer-event flows */
    const b64 = c.toDataURL("image/png").split(",")[1];
    const bytes = Uint8Array.from(atob(b64), ch => ch.charCodeAt(0));
    const blob = new Blob([bytes], { type: "image/png" });
    try {
      await navigator.clipboard.write([new ClipboardItem({"image/png": blob})]);
      toast("Copied ✓ — paste it anywhere (⌘V / Ctrl+V)", true);
    } catch(e) {
      downloadBlob(`${sourceSlug()}_p${pad4(shownPage)}_clip.png`, blob);
      toast("Clipboard not available — saved the snippet as a PNG download instead", false);
    }
  } catch(e) {
    if (e && e.name === "AbortError") { toast("Copy cancelled", false); return; }
    console.warn("fence copy failed", e);
    toast("Couldn't copy (" + (e && e.name || "error") + ": " + (e && e.message || e) + ")", false);
  }
}
function wireInk() {
  const svg = inkSvg();
  svg.addEventListener("pointerdown", e => {
    e.preventDefault();
    svg.setPointerCapture(e.pointerId);
    const pt = inkPoint(e);
    if (inkTool === "eraser") { eraseNear(pt); drawing = "erase"; return; }
    if (inkTool === "fence") {
      drawing = { fence: true, a: pt, b: pt, el: fenceRectEl() };
      setFenceRect(drawing.el, pt, pt);
      return;
    }
    drawing = { tool: inkTool, pts: [pt] };
    svg.appendChild(strokePath(drawing));
  });
  svg.addEventListener("pointermove", e => {
    if (!drawing) return;
    const pt = inkPoint(e);
    if (drawing === "erase") { eraseNear(pt); return; }
    if (drawing.fence) { drawing.b = pt; setFenceRect(drawing.el, drawing.a, drawing.b); return; }
    drawing.pts.push(pt);
    svg.lastChild.setAttribute("d",
      "M" + drawing.pts.map(p => p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" L"));
  });
  const up = () => {
    if (drawing && drawing.fence) {
      const { a, b } = drawing;
      drawing = null;
      renderInk(); /* clears the fence rect from the overlay */
      copyFenceRegion(a, b);
      return;
    }
    if (drawing && drawing !== "erase" && drawing.pts.length > 1) {
      pageStrokes().push(drawing); saveInk();
    }
    drawing = null;
    renderInk();
  };
  svg.addEventListener("pointerup", up);
  svg.addEventListener("pointercancel", up);
  document.getElementById("tool-pen").addEventListener("click", () => setInkTool("pen"));
  document.getElementById("tool-hi").addEventListener("click", () => setInkTool("hi"));
  document.getElementById("tool-eraser").addEventListener("click", () => setInkTool("eraser"));
  document.getElementById("tool-fence").addEventListener("click", () => setInkTool("fence"));
  document.getElementById("ink-undo").addEventListener("click", () => {
    pageStrokes().pop(); saveInk(); renderInk();
  });
  document.getElementById("ink-clear").addEventListener("click", () => {
    if (!confirm("Erase every mark on this page?")) return;
    inkAll[shownPage] = []; saveInk(); renderInk();
  });
  document.getElementById("page-img").addEventListener("load", () => { applyRotation(); renderInk(); });
  document.getElementById("page-rotate").addEventListener("click", rotatePage);
  document.getElementById("zoom-in").addEventListener("click", () => setZoom(zoom * 1.25));
  document.getElementById("zoom-out").addEventListener("click", () => setZoom(zoom / 1.25));
  document.getElementById("zoom-reset").addEventListener("click", () => setZoom(1));
  document.getElementById("page-pane").addEventListener("wheel", e => {
    if (!e.ctrlKey && !e.metaKey) return; /* pinch gestures arrive as ctrl+wheel */
    e.preventDefault();
    setZoom(zoom * Math.exp(-e.deltaY * 0.005), e.clientX, e.clientY);
  }, { passive: false });
  new ResizeObserver(() => applyRotation()).observe(document.getElementById("page-pane"));
  applyZoom();
  setInkTool("pen");
}

/* ---------- katex ---------- */
function typeset(el, latex) {
  if (window.katex) {
    try { katex.render(latex, el, {throwOnError:true, displayMode:true, strict:"ignore"}); return; }
    catch(e) { el.textContent = latex; return; }
  }
  el.textContent = latex;
  document.addEventListener("katex-ready", () => typeset(el, latex), {once:true});
}

/* ---------- main render ---------- */
function render() {
  const eq = EQS[cur];
  const st = statusOf(eq);
  const onPage = EQS.filter(e => e.page === eq.page);
  document.getElementById("crumb-page").textContent = eq.page;
  document.getElementById("crumb-idx").textContent = eq.index;
  document.getElementById("crumb-count").textContent = onPage.length;
  const chip = document.getElementById("status-chip");
  chip.className = st;
  chip.textContent = {unreviewed:"not checked yet", verified:"✓ checked", flagged:"⚠ flagged",
    backcheck:"↻ check the fix"}[st];
  typeset(document.getElementById("eq-render"), eq.latex);
  document.getElementById("eq-src").textContent = eq.latex;

  const bc = document.getElementById("bc-banner");
  if (st === "backcheck" && eq.bc) {
    let html = '<div class="bctitle">↻ This one was fixed by the computer — does the fix look right now?</div>';
    if (eq.bc.description) html += '<div><b>The original problem:</b> ' + esc(eq.bc.description) + '</div>';
    if (eq.bc.prev_latex) html += '<div><b>Before the fix:</b> <code>' + esc(eq.bc.prev_latex) + '</code></div>';
    if (eq.bc.source === "1.5-P-machine" && eq.bc.proposal_hash) {
      html += '<button onclick="rejectProposal(EQS[cur])">Reject this proposal</button>';
    }
    bc.innerHTML = html; bc.style.display = "block";
  } else { bc.style.display = "none"; }

  document.getElementById("flag-panel").style.display = "none";
  document.getElementById("flag-note").value = noteOf(eq);
  showPage(eq.page);
  updateProgress();
  renderStrip();
}
function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;"); }

function updateProgress() {
  let v=0, f=0;
  EQS.forEach(eq => { const s = statusOf(eq); if (s==="verified") v++; else if (s==="flagged") f++; });
  const total = EQS.length, done = v + f;
  document.getElementById("pv").style.width = (v/total*100)+"%";
  document.getElementById("pf").style.width = (f/total*100)+"%";
  document.getElementById("ptext").textContent = `${done} / ${total} checked` + (f ? ` · ${f} flagged` : "");
  document.getElementById("done-card").style.display =
    EQS.every(eq => statusOf(eq) !== "unreviewed") ? "block" : "none";
}

function renderStrip() {
  const strip = document.getElementById("page-strip");
  if (!strip.childElementCount) {
    PAGES.forEach(p => {
      const d = document.createElement("div");
      d.className = "pdot"; d.dataset.page = p; d.title = "page " + p;
      d.addEventListener("click", () => {
        const i = EQS.findIndex(e => e.page === p);
        if (i >= 0) goto(i);
      });
      strip.appendChild(d);
    });
  }
  strip.querySelectorAll(".pdot").forEach(d => {
    const p = Number(d.dataset.page);
    const eqs = EQS.filter(e => e.page === p);
    const states = eqs.map(statusOf);
    d.className = "pdot";
    if (states.some(s => s === "flagged")) d.classList.add("hasflag");
    else if (states.every(s => s === "verified")) d.classList.add("done");
    else if (states.some(s => s !== "unreviewed")) d.classList.add("some");
    if (p === EQS[cur].page) d.classList.add("current");
    d.title = `page ${p} — ${states.filter(s=>s!=="unreviewed").length}/${eqs.length} checked`;
  });
}

/* ---------- navigation ---------- */
function goto(i) {
  cur = Math.max(0, Math.min(EQS.length - 1, i));
  render();
}
function nextUnreviewed(from) {
  const n = EQS.length;
  for (let d = 1; d <= n; d++) {
    const i = (from + d) % n;
    if (statusOf(EQS[i]) === "unreviewed" || statusOf(EQS[i]) === "backcheck") return i;
  }
  return null;
}
function advance() {
  const i = nextUnreviewed(cur);
  if (i === null) { render(); return; }
  goto(i);
}

/* ---------- wire up ---------- */
document.getElementById("btn-yes").addEventListener("click", () => { setVerified(EQS[cur]); advance(); });
document.getElementById("btn-no").addEventListener("click", () => {
  const p = document.getElementById("flag-panel");
  p.style.display = "block";
  document.getElementById("flag-note").focus();
  renderFlagPreview();
});
document.getElementById("flag-save").addEventListener("click", () => {
  setFlagged(EQS[cur], document.getElementById("flag-note").value);
  advance();
});
document.getElementById("flag-cancel").addEventListener("click", () => {
  document.getElementById("flag-panel").style.display = "none";
});
document.getElementById("btn-skip").addEventListener("click", () => goto(cur + 1));
document.getElementById("btn-clear").addEventListener("click", () => { clearAnswer(EQS[cur]); render(); });
document.getElementById("btn-prev").addEventListener("click", () => goto(cur - 1));
document.getElementById("btn-next").addEventListener("click", () => goto(cur + 1));
document.getElementById("next-unreviewed").addEventListener("click", advance);
document.getElementById("save-btn").addEventListener("click", saveWork);
document.getElementById("gear-menu").querySelector("button").addEventListener("click",
  e => { e.stopPropagation(); document.getElementById("gear-menu").classList.toggle("open"); });
document.addEventListener("click", () => document.getElementById("gear-menu").classList.remove("open"));
document.getElementById("reload-disk").addEventListener("click", () => {
  if (!confirm("Discard unsaved browser changes and reload state from the disk sidecars baked into this HTML?")) return;
  localStorage.removeItem(STORAGE_KEY);
  state = JSON.parse(JSON.stringify(INITIAL));
  dirty = false; document.getElementById("dirty-flag").textContent = "";
  render();
});
document.getElementById("clear-local").addEventListener("click", () => {
  if (!confirm("Wipe all in-browser review state? (Does not touch the on-disk sidecars.)")) return;
  localStorage.removeItem(STORAGE_KEY);
  state = { verified: {}, flagged: {} };
  dirty = false; document.getElementById("dirty-flag").textContent = "";
  render();
});

function renderFlagPreview() {
  const src = document.getElementById("flag-note").value.trim();
  const body = document.getElementById("flag-preview");
  if (!src) { body.innerHTML = '<span class="pverror">Your note will show here.</span>'; return; }
  if (!window.katex) { body.textContent = src; return; }
  try { katex.render(src, body, {throwOnError:true, displayMode:true, strict:"ignore"}); }
  catch(e) { body.innerHTML = '<span class="pverror">Plain-English note (that\'s fine!): </span>' + esc(src); }
}
document.getElementById("flag-note").addEventListener("input", renderFlagPreview);

document.addEventListener("keydown", e => {
  if (e.target.matches("textarea, input")) return;
  const k = e.key.toLowerCase();
  if (k === "y" || k === "v") { setVerified(EQS[cur]); advance(); }
  else if (k === "n" || k === "f") { document.getElementById("btn-no").click(); }
  else if (k === "s") { goto(cur + 1); }
  else if (e.key === "ArrowRight") { goto(cur + 1); }
  else if (e.key === "ArrowLeft") { goto(cur - 1); }
});
window.addEventListener("beforeunload", e => { if (dirty) { e.preventDefault(); e.returnValue = ""; } });

/* ---------- resizable review pane ---------- */
function wireSplitter() {
  const split = document.getElementById("splitter");
  const saved = localStorage.getItem("ui:review-w");
  if (saved) document.documentElement.style.setProperty("--review-w", saved);
  split.addEventListener("pointerdown", e => {
    e.preventDefault();
    split.setPointerCapture(e.pointerId);
    split.classList.add("dragging");
    const onMove = ev => {
      const w = Math.max(300, Math.min(window.innerWidth * 0.75, window.innerWidth - ev.clientX));
      document.documentElement.style.setProperty("--review-w", w + "px");
    };
    const onUp = () => {
      split.classList.remove("dragging");
      localStorage.setItem("ui:review-w",
        getComputedStyle(document.documentElement).getPropertyValue("--review-w").trim());
      split.removeEventListener("pointermove", onMove);
      split.removeEventListener("pointerup", onUp);
    };
    split.addEventListener("pointermove", onMove);
    split.addEventListener("pointerup", onUp);
  });
}

/* start on the first unreviewed equation */
cur = (statusOf(EQS[0]) === "unreviewed") ? 0 : (nextUnreviewed(-1) ?? 0);
wireInk();
wireSplitter();
render();
</script>
</body></html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
