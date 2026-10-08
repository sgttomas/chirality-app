import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const here = new URL('.', import.meta.url);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export function classify(count, actual, expected) {
  if (count !== 1) return { status: 'blocked', cause: 'Target must resolve to exactly one element' };
  return { status: actual === expected ? 'pass' : 'fail', actual, expected };
}
export function allowed(url, origin) {
  try { return new URL(url).origin === origin; } catch { return false; }
}
export async function verifyCaptures(root, report) {
  for (const project of report.projects) for (const capture of project.captures) {
    if (!/^[a-z0-9-]+\.(json|png)$/.test(capture.path)) throw Error('Unsafe capture path');
    if (hash(await readFile(join(root, capture.path))) !== capture.sha256) throw Error('Capture digest mismatch');
  }
  return true;
}

// This is a support report, not an EXP admission record. Page request observation
// does not establish whole-process network isolation, so DC-R5 cannot pass here.
export async function run({ output, modulePath, executables = {} }) {
  await mkdir(output, { recursive: false }); // refuse accidental evidence overwrite
  const fixture = await readFile(new URL('fixture.html', here));
  const report = {
    format: 'chirality-runner-support-v1', run_basis: 'definition_check',
    subject: 'offline-interface-runner', runner_sha256: hash(await readFile(new URL('runner.mjs', here))),
    fixture_sha256: hash(fixture), date: new Date().toISOString(),
    admitted: false, qualification: 'unestablished',
    limits: ['Invented seam fixture; no App candidate or native witness',
      'DC-R5 whole-process traffic observation is not supplied',
      'A canonical EXP result and independent review remain required'], projects: [],
  };
  let pw;
  try {
    const require = createRequire(import.meta.url);
    pw = require(resolve(modulePath));
    report.playwright_version = require(join(resolve(modulePath), 'package.json')).version;
    report.playwright_package_sha256 = hash(await readFile(join(resolve(modulePath), 'package.json')));
  } catch { report.playwright_version = null; }
  const server = createServer((req, res) => {
    if (req.url !== '/') { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-store' }); res.end(fixture);
  });
  await new Promise((ok, fail) => { server.once('error', fail); server.listen(0, '127.0.0.1', ok); });
  const origin = `http://127.0.0.1:${server.address().port}`;
  try {
    for (const engine of ['chromium', 'webkit']) {
      const p = { engine, version: null, checks: {}, probes: [], captures: [], requests: [] };
      report.projects.push(p);
      async function capture(name, bytes) {
        const path = `${engine}-${name}`;
        await writeFile(join(output, path), bytes, { flag: 'wx' });
        p.captures.push({ path, sha256: hash(bytes) });
      }
      let browser;
      try {
        if (!pw?.[engine]) throw Error('Module unavailable');
        const selectedExecutable = executables[engine] || pw[engine].executablePath();
        p.launch_entry_sha256 = hash(await readFile(selectedExecutable));
        p.launch_entry_limit = 'Hash binds launch entry only; WebKit entry can be a wrapper, not whole engine';
        browser = await pw[engine].launch({ headless: true,
          ...(executables[engine] ? { executablePath: executables[engine] } : {}) });
        p.version = browser.version();
        p.version_source = engine === 'webkit' ? 'Playwright module version label; actual engine version unestablished' : 'Chromium Browser.getVersion via Playwright';
        p.executable_selection = executables[engine] ? 'explicit-cache-override' : 'module-default';
        const context = await browser.newContext({ serviceWorkers: 'block' });
        await context.route('**/*', async route => {
          const local = allowed(route.request().url(), origin);
          p.requests.push({ destination: local ? 'local-fixture' : 'outside-fixture', action: local ? 'continue' : 'abort' });
          if (local) await route.continue(); else await route.abort('blockedbyclient');
        });
        // Newer Playwright supports explicit websocket interception. Unsupported
        // versions are recorded; neither case upgrades DC-R5 to pass.
        p.websocket_guard = typeof context.routeWebSocket === 'function';
        if (p.websocket_guard) await context.routeWebSocket('**/*', ws => {
          p.requests.push({ destination: 'websocket', action: 'close' }); ws.close();
        });
        const page = await context.newPage();
        await page.goto(origin, { waitUntil: 'load', timeout: 10000 });
        for (const [id, selector, expected] of [
          ['known-pass', '#reply', 'Invented supplier reply'],
          ['known-fail', '#reply', 'Deliberately wrong expectation'],
          ['missing-target', '#absent', 'anything'],
        ]) {
          const target = page.locator(selector); const count = await target.count();
          const result = classify(count, count === 1 ? await target.textContent() : null, expected);
          p.probes.push({ id, ...result });
          await capture(`${id}.png`, await page.screenshot());
        }
        // Exercise the actual interceptor without permitting an external request.
        // The reserved invalid domain must be aborted before any transport.
        await page.evaluate(async () => {
          try { await fetch('https://runner-isolation.invalid/probe'); } catch {}
        });
        p.checks['DC-R1'] = engine === 'webkit' ? 'inconclusive' : (p.version ? 'pass' : 'fail');
        p.checks['DC-R2'] = p.probes[0].status === 'pass' && p.probes[1].status === 'fail' ? 'pass' : 'fail';
        p.checks['DC-R3'] = p.probes[2].status === 'blocked' && !!p.probes[2].cause ? 'pass' : 'fail';
        p.page_isolation_guard = p.requests.some(r => r.destination === 'outside-fixture' && r.action === 'abort') ? 'pass' : 'fail';
      } catch (error) {
        // Avoid persisting browser diagnostics containing local paths/host names.
        p.cause = browser ? 'Browser probe failed; inspect locally without committing raw diagnostics' : 'Browser engine or compatible module unavailable or launch refused';
        p.error_type = error.name;
        for (const id of ['DC-R1', 'DC-R2', 'DC-R3']) p.checks[id] ??= 'blocked';
      } finally {
        if (browser) await browser.close();
      }
      p.checks['DC-R5'] = 'inconclusive';
      await capture('observation.json', Buffer.from(JSON.stringify({ version: p.version, version_source: p.version_source, probes: p.probes, requests: p.requests, cause: p.cause }, null, 2) + '\n'));
      p.checks['DC-R4'] = 'pass';
    }
  } finally { await new Promise(ok => server.close(ok)); }
  await verifyCaptures(output, report);
  await writeFile(join(output, 'report.json'), JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
  return report;
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const [output, modulePath, chromium, webkit] = process.argv.slice(2);
  if (!output || !modulePath) {
    console.error('Usage: node runner.mjs NEW_OUTPUT_DIR INSTALLED_PLAYWRIGHT_DIR [CHROMIUM_EXECUTABLE WEBKIT_EXECUTABLE]'); process.exitCode = 2;
  } else {
    try {
      const report = await run({ output, modulePath, executables: { chromium, webkit } });
      console.log(JSON.stringify(report));
      process.exitCode = report.projects.some(p => Object.values(p.checks).some(s => s === 'blocked' || s === 'fail')) ? 2 : 1;
    } catch { console.error('Runner failed; no admission established'); process.exitCode = 2; }
  }
}
