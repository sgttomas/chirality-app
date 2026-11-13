// Scratch only, never committed: serves the App's web view with a page probe
// so a development walk can read the rendered view and press its web controls.
// It operates no native dialog and establishes no act of a person.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { appendFileSync, readdirSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const WALK = process.env.WALK_DIR;
const PORT = Number(process.env.WALK_PORT ?? 1437);

const PROBE = `
(() => {
  const visible = el => { const s = getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden'; };
  const hiddenBy = el => { for (let n = el; n && n.nodeType === 1; n = n.parentElement) { if (n.hidden) return true; if (n.tagName === 'DETAILS' && !n.open && el !== n && !(el.tagName === 'SUMMARY' && el.parentElement === n) && !n.querySelector(':scope > summary')?.contains(el)) return true; } return false; };
  const label = el => (el.getAttribute('aria-label') || (el.labels && el.labels[0] && el.labels[0].innerText) || el.closest('label')?.innerText || el.placeholder || '').replace(/\\s+/g, ' ').trim();
  window.__walk = {
    // The view as a person reads it: visible text with controls marked.
    dump(root = document.body) {
      const out = [];
      const walk = (node, depth) => {
        if (node.nodeType === 3) { const t = node.textContent.replace(/\\s+/g, ' '); if (t.trim()) out.push(t); return; }
        if (node.nodeType !== 1) return;
        const el = node, tag = el.tagName;
        if (tag === 'STYLE' || tag === 'SCRIPT') return;
        if (el.hidden || !visible(el)) return;
        if (tag === 'DETAILS' && !el.open) { const s = el.querySelector(':scope > summary'); out.push('\\n[closed: ' + (s ? s.innerText.replace(/\\s+/g, ' ').trim() : 'details') + ']\\n'); return; }
        if (/^H[1-6]$/.test(tag)) { out.push('\\n' + '#'.repeat(Number(tag[1])) + ' ' + el.innerText.replace(/\\s+/g, ' ').trim() + '\\n'); return; }
        if (tag === 'BUTTON') { out.push(' [' + (el.disabled ? 'button, disabled: ' : 'button: ') + el.innerText.replace(/\\s+/g, ' ').trim() + '] '); return; }
        if (tag === 'A') { out.push(' <link: ' + el.innerText.replace(/\\s+/g, ' ').trim() + ' -> ' + el.getAttribute('href') + '> '); return; }
        if (tag === 'SELECT') { out.push(' {select' + (el.disabled ? ', disabled' : '') + ' "' + label(el) + '" = "' + (el.selectedOptions[0]?.innerText ?? '') + '" of [' + Array.from(el.options).map(o => o.innerText).join(' | ') + ']} '); return; }
        if (tag === 'INPUT') { out.push(' {' + (el.type || 'text') + (el.disabled ? ', disabled' : '') + ' "' + label(el) + '" = ' + (el.type === 'checkbox' || el.type === 'radio' ? el.checked : JSON.stringify(el.value)) + '} '); return; }
        if (tag === 'TEXTAREA') { out.push(' {textarea' + (el.disabled ? ', disabled' : '') + ' "' + label(el) + '" = ' + JSON.stringify(el.value) + '} '); return; }
        if (tag === 'SUMMARY') { out.push('\\n[open: ' + el.innerText.replace(/\\s+/g, ' ').trim() + ']\\n'); return; }
        const block = /^(P|DIV|LI|SECTION|ARTICLE|UL|OL|PRE|ASIDE|MAIN|NAV|FIELDSET|DL|DT|DD|TABLE|TR|HEADER|FOOTER|BR|DETAILS|LEGEND|LABEL)$/.test(tag);
        if (block) out.push('\\n');
        if (tag === 'LI') out.push('- ');
        for (const child of el.childNodes) walk(child, depth + 1);
        if (block) out.push('\\n');
      };
      walk(root, 0);
      return out.join('').replace(/[ \\t]+/g, ' ').replace(/\\n\\s*\\n+/g, '\\n').trim();
    },
    find(kind, name, nth = 0) {
      const sel = kind === 'button' ? 'button' : kind === 'link' ? 'a' : kind === 'summary' ? 'summary' : kind;
      const norm = s => s.replace(/\\s+/g, ' ').trim();
      const all = Array.from(document.querySelectorAll(sel)).filter(el => !hiddenBy(el) && (kind === 'input' || kind === 'select' || kind === 'textarea' ? label(el).includes(name) : norm(el.innerText).includes(name)));
      return all[nth];
    },
    click(kind, name, nth = 0) { const el = this.find(kind, name, nth); if (!el) return 'not found: ' + kind + ' ' + name; if (el.disabled) return 'disabled: ' + name; el.click(); return 'clicked: ' + (el.innerText || '').replace(/\\s+/g, ' ').trim(); },
    fill(kind, name, value, nth = 0) {
      const el = this.find(kind, name, nth); if (!el) return 'not found: ' + kind + ' ' + name; if (el.disabled) return 'disabled: ' + name;
      const proto = kind === 'textarea' ? HTMLTextAreaElement.prototype : kind === 'select' ? HTMLSelectElement.prototype : HTMLInputElement.prototype;
      Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, value);
      el.dispatchEvent(new Event(kind === 'select' ? 'change' : 'input', { bubbles: true }));
      return 'filled: ' + name;
    },
    check(name, nth = 0) { const el = this.find('input', name, nth); if (!el) return 'not found: ' + name; el.click(); return 'checked: ' + el.checked; },
  };
  const errors = [];
  window.addEventListener('error', e => errors.push(String(e.message)));
  window.addEventListener('unhandledrejection', e => errors.push('rejection: ' + String(e.reason)));
  const loop = async () => {
    try {
      const reply = await fetch('/__walk/next');
      const cmd = await reply.json();
      if (cmd && cmd.id) {
        let result;
        try { result = await (0, eval)('(async () => { ' + cmd.code + ' })()'); } catch (error) { result = 'THROWN: ' + String(error && error.stack || error); }
        await fetch('/__walk/report', { method: 'POST', body: JSON.stringify({ id: cmd.id, result: result === undefined ? null : result, errors: errors.splice(0) }) });
      }
    } catch (error) { /* dev server not reachable; try again */ }
    setTimeout(loop, 250);
  };
  loop();
})();
`;

function walkProbe() {
  return {
    name: "walk-probe",
    transformIndexHtml(html) { return html.replace("</body>", `<script>${PROBE}</script></body>`); },
    configureServer(server) {
      server.middlewares.use((req, _res, next) => { try { appendFileSync(join(WALK, "hits.log"), `${new Date().toISOString()} ${req.method} ${req.url} ${req.headers["user-agent"] ?? ""}\n`); } catch {} next(); });
      server.middlewares.use("/__walk/next", (_req, res) => {
        res.setHeader("content-type", "application/json");
        const names = readdirSync(join(WALK, "q")).filter(n => n.endsWith(".js")).sort();
        if (!names.length) { res.end("null"); return; }
        const file = join(WALK, "q", names[0]);
        const code = readFileSync(file, "utf8");
        unlinkSync(file);
        res.end(JSON.stringify({ id: names[0].replace(/\.js$/, ""), code }));
      });
      server.middlewares.use("/__walk/report", (req, res) => {
        let body = "";
        req.on("data", chunk => { body += chunk; });
        req.on("end", () => {
          const report = JSON.parse(body);
          const text = typeof report.result === "string" ? report.result : JSON.stringify(report.result, null, 2);
          writeFileSync(join(WALK, "out", `${report.id}.txt`), text + (report.errors.length ? `\n\nPAGE ERRORS:\n${report.errors.join("\n")}` : ""));
          res.end("ok");
        });
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), walkProbe()],
  clearScreen: false,
  resolve: { alias: [{ find: /^@tauri-apps\/api\/core$/, replacement: join(WALK, "core-shim.mjs") }] },
  server: { host: "127.0.0.1", port: PORT, strictPort: true, fs: { allow: [".", WALK] } },
});
