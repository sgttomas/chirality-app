import { afterAll, beforeAll, expect, it } from "vitest";
import { build } from "esbuild";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { mkdtemp, mkdir, realpath, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const exec = promisify(execFile);
const runtimeRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
let scratch: string;
// Exercise public barrel consumption using the App's node24/CJS external policy:
// coding-agent is external; pi-ai is deliberately not in that list.
beforeAll(async () => {
  scratch = await realpath(await mkdtemp(join(tmpdir(), "runtime-pi-packaging-")));
  await mkdir(join(scratch, "project"));
  await mkdir(join(scratch, "control"));
  await mkdir(join(scratch, "home"));
  await symlink(join(runtimeRoot, "node_modules"), join(scratch, "node_modules"), "dir");
  for (const format of ["cjs", "esm"] as const) {
    await build({
      stdin: { contents: fixture, loader: "ts", resolveDir: runtimeRoot },
      outfile: join(scratch, format === "cjs" ? "consumer.cjs" : "consumer.mjs"),
      bundle: true, platform: "node", target: "node24", format,
      external: ["@earendil-works/pi-coding-agent", "@earendil-works/pi-coding-agent/*"],
      logLevel: "silent"
    });
  }
  // Instrument native SDK evaluation with barriers/markers; retain the real
  // module bodies and exports instead of substituting a mock SDK.
  await writeFile(join(scratch, "loader.mjs"), `
    const sdkUrls = new Set();
    export async function resolve(specifier, context, next) {
      const result = await next(specifier, context);
      if (context.parentURL?.includes('/consumer.') && ['@earendil-works/pi-coding-agent', '@earendil-works/pi-ai'].includes(specifier)) sdkUrls.add(result.url);
      return result;
    }
    export async function load(url, context, next) {
      const result = await next(url, context);
      if (!sdkUrls.has(url)) return result;
      const mode = process.env.PI_FIXTURE_MODE;
      const gate = JSON.stringify(process.env.PI_FIXTURE_GATE);
      const prefix = mode === 'load-error' ? "throw new Error('synthetic loader failure');" :
        ['interrupt', 'close', 'release', 'deadline'].includes(mode) ?
        "for (;;) { try { await (await import('node:fs/promises')).access(" + gate + "); break; } catch { await new Promise(r => setTimeout(r, 10)); } }" :
        mode === 'success' ? '' : "await new Promise(r => setTimeout(r, 350));";
      const loaded = JSON.stringify(process.env.PI_FIXTURE_GATE + (url.includes('pi-coding-agent') ? '.agent-loaded' : '.ai-loaded'));
      return { ...result, source: prefix + String(result.source) + "\\nawait (await import('node:fs/promises')).writeFile(" + loaded + ", 'loaded');" };
    }
  `);
  await writeFile(join(scratch, "register.mjs"), `import { register } from 'node:module'; register(new URL('./loader.mjs', import.meta.url));`);
});
afterAll(async () => { if (scratch) await rm(scratch, { recursive: true, force: true }); });

for (const format of ["cjs", "esm"] as const) {
  for (const mode of ["success", "interrupt", "close", "release", "deadline", "capacity", "snapshot", "load-error"]) {
    it(`${format} consumer: real SDK offline ${mode}`, async () => {
      const { stdout } = await exec(process.execPath, ["--import", join(scratch, "register.mjs"), join(scratch, format === "cjs" ? "consumer.cjs" : "consumer.mjs")], {
        cwd: scratch, timeout: 15000,
        env: { ...process.env, HOME: join(scratch, "home"), XDG_CONFIG_HOME: join(scratch, "home"), PI_CODING_AGENT_DIR: join(scratch, "home"), PI_FIXTURE_MODE: mode, PI_FIXTURE_GATE: join(scratch, `${format}-${mode}.gate`) }
      });
      expect(JSON.parse(stdout.trim())).toMatchObject({ ok: true, mode });
    }, 20000);
  }
}

const fixture = `
import assert from 'node:assert/strict';
import { join } from 'node:path';
import { access, writeFile } from 'node:fs/promises';
import { setTimeout as delay } from 'node:timers/promises';
import { createPiTurnRuntime } from './packages/engine-pi-omlx/src/index.ts';
async function main() {
  const root = join(process.cwd(), 'project'), transcriptRoot = join(process.cwd(), 'control');
  const mode = process.env.PI_FIXTURE_MODE;
  let calls = 0;
  globalThis.fetch = async () => { throw new Error('Unexpected network access'); };
  const input = { session: { sessionId: 'packaging-session', projectRoot: root, persona: 'TASK', mode: 'WORK', agentType: 2, createdAt: 'fixture', updatedAt: 'fixture' }, message: 'FIRST_USER', opts: { model: 'fixture-model', tools: ['read_file'], maxTurns: 4, persona: 'TASK', mode: 'WORK' }, turnId: 'first-turn' };
  const execution = { credential: 'synthetic-packaging-key', disableBuiltIns: true, disableAmbientResources: true, transcriptRoot };
  const port = createPiTurnRuntime({ canonicalRoot: root, baseUrl: 'http://127.0.0.1:12345/v1', model: { id: 'fixture-model', contextWindow: 8192, maxTokens: 64 }, maxSessions: 1, turnTimeoutMs: mode === 'deadline' ? 30 : 5000,
    fetchImpl: async (url, init) => {
      calls++;
      assert.equal(url, 'http://127.0.0.1:12345/v1/chat/completions');
      assert.equal(init.headers.authorization, 'Bearer synthetic-packaging-key');
      const body = JSON.parse(init.body);
      assert.equal(body.model, 'fixture-model');
      assert.deepEqual(body.tools.map(tool => tool.function.name), ['read_file']);
      if (calls === 2) {
        assert.match(JSON.stringify(body.messages), /FIRST_USER/);
        assert.match(JSON.stringify(body.messages), /OFFLINE_REAL_PI/);
        assert.match(JSON.stringify(body.messages), /SECOND_USER/);
      }
      return new Response(JSON.stringify({ model: 'fixture-model', choices: [{ message: { role: 'assistant', content: 'OFFLINE_REAL_PI' }, finish_reason: 'stop' }], usage: { prompt_tokens: 2, completion_tokens: 2 } }));
    }
  });
  assert.equal(typeof port.startTurn, 'function'); // Factory remains synchronous.
  let release;
  if (mode === 'release') {
    const file = join(root, 'selected.txt'); await writeFile(file, 'fixture');
    input.session.parentSessionId = 'manager';
    release = await port.toolBindings.bind(input.session.sessionId, [{ name: 'read_file', description: 'bound', inputSchema: { type: 'object', properties: {}, additionalProperties: false }, permission: { effect: 'allow', operation: 'read', roots: [file] }, async execute() { throw new Error('revoked callback executed'); } }]);
  }
  const original = structuredClone(input), originalExecution = { ...execution };
  const turn = port.startTurn(input, execution);
  const first = await turn.next(); assert.equal(first.value.type, 'session:init');
  if (mode === 'interrupt') await port.interrupt(original.session.sessionId);
  if (mode === 'close') await port.close();
  if (mode === 'release') await release();
  if (mode === 'capacity') {
    await assert.rejects(async () => { for await (const _ of port.startTurn(original, originalExecution)) {} }, error => error.type === 'TURN_IN_PROGRESS');
    const other = structuredClone(original); other.session.sessionId = 'different-session';
    await assert.rejects(async () => { for await (const _ of port.startTurn(other, originalExecution)) {} }, /capacity/);
    await assert.rejects(port.toolBindings.bind(original.session.sessionId, []));
  }
  if (mode === 'snapshot') {
    input.session.projectRoot = '/unapproved'; input.session.sessionId = 'mutated'; input.opts.tools = ['bash']; input.opts.model = 'wrong'; execution.credential = 'wrong-account';
  }
  const events = [first.value]; for await (const event of turn) events.push(event);
  assert.equal(events.filter(event => event.type === 'process:exit').length, 1);
  const terminal = events.at(-1);
  if (['interrupt', 'close', 'release'].includes(mode)) {
    assert.deepEqual(terminal, { type: 'process:exit', data: { exitCode: 0, interrupted: true } });
  } else if (mode === 'deadline' || mode === 'load-error') {
    assert.equal(terminal.data.exitCode, 1);
    assert.equal(terminal.data.errorType, 'PROVIDER_PROTOCOL_FAILURE');
    if (mode === 'deadline') { assert.match(terminal.data.error, /deadline exceeded/); }
  } else {
    assert.equal(terminal.data.exitCode, 0);
    assert.ok(events.some(event => event.type === 'chat:delta' && event.data.text === 'OFFLINE_REAL_PI'));
    const second = structuredClone(original); second.message = 'SECOND_USER'; second.turnId = 'second-turn';
    const continued = []; for await (const event of port.startTurn(second, originalExecution)) continued.push(event);
    assert.equal(continued.at(-1).data.exitCode, 0);
    assert.equal(calls, 2);
    await assert.rejects(port.preflight(second, 'changed-account'), /context changed/);
    second.session.briefHash = 'changed-scope'; await assert.rejects(port.preflight(second, originalExecution.credential), /context changed/);
  }
  if (['interrupt', 'close', 'release', 'deadline', 'load-error'].includes(mode)) {
    // Native loading cannot complete until after the terminal has arrived.
    await writeFile(process.env.PI_FIXTURE_GATE, 'release');
    if (mode !== 'load-error') {
      for (const suffix of ['.agent-loaded', '.ai-loaded']) {
        for (;;) { try { await access(process.env.PI_FIXTURE_GATE + suffix); break; } catch { await delay(10); } }
      }
    }
    assert.equal(calls, 0);
    await assert.rejects(port.preflight(original, originalExecution.credential));
    assert.ok(!events.some(event => event.type === 'session:complete'));
  }
  await port.close();
  console.log(JSON.stringify({ ok: true, mode, calls }));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
`;
