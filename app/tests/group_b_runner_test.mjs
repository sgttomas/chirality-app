import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { run, classify, allowed, verifyCaptures } from '../examination/runner_support/runner.mjs';

test('false expectations and absent/ambiguous targets cannot pass', () => {
  assert.equal(classify(1, 'observed', 'wrong').status, 'fail');
  for (const count of [0, 2]) {
    const result = classify(count, 'observed', 'observed');
    assert.equal(result.status, 'blocked'); assert.ok(result.cause);
  }
});
test('origin guard rejects deceptive origins and non-network schemes', () => {
  const local = 'http://127.0.0.1:1234';
  assert.equal(allowed(`${local}/fixture`, local), true);
  for (const url of ['https://127.0.0.1:1234/', 'http://127.0.0.1:1235/', 'http://127.0.0.1:1234@outside.invalid/', 'file:///tmp/test', 'data:text/html,hi']) assert.equal(allowed(url, local), false);
});
test('actual runner missing-module path writes blocked evidence and detects tampering', async () => {
  const parent = await mkdtemp(join(tmpdir(), 'runner-missing-'));
  try {
    const output = join(parent, 'captures');
    const report = await run({ output, modulePath: join(parent, 'absent-module') });
    assert.equal(report.admitted, false);
    for (const p of report.projects) {
      assert.equal(p.checks['DC-R1'], 'blocked'); assert.ok(p.cause);
      assert.equal(p.checks['DC-R5'], 'inconclusive');
    }
    assert.equal(await verifyCaptures(output, report), true);
    await writeFile(join(output, report.projects[0].captures[0].path), 'changed');
    await assert.rejects(verifyCaptures(output, report), /digest mismatch/);
    await assert.rejects(run({ output, modulePath: '' }), /EEXIST/);
  } finally { await rm(parent, { recursive: true, force: true }); }
});
const live = process.env.RUNNER_PLAYWRIGHT_DIR;
test('cached browsers exercise real false-pass, missing-target, capture and network guard paths', { skip: !live }, async () => {
  const parent = await mkdtemp(join(tmpdir(), 'runner-browser-'));
  try {
    const output = join(parent, 'captures');
    const report = await run({ output, modulePath: live, executables: {
      chromium: process.env.RUNNER_CHROMIUM, webkit: process.env.RUNNER_WEBKIT,
    } });
    for (const p of report.projects) {
      assert.ok(p.version, `${p.engine}: ${p.cause}`);
      assert.equal(p.checks['DC-R1'], p.engine === 'webkit' ? 'inconclusive' : 'pass');
      assert.equal(p.sensitivity_probe, 'pass');
      assert.equal(p.checks['DC-R2'], 'inconclusive');
      for (const id of ['DC-R3', 'DC-R4']) assert.equal(p.checks[id], 'pass');
      assert.deepEqual(p.probes.map(x => x.status), ['pass', 'fail', 'blocked']);
      assert.equal(p.page_isolation_guard, 'pass');
      assert.ok(p.requests.some(r => r.destination === 'local-fixture' && r.action === 'continue'));
      assert.ok(p.requests.every(r => r.destination === 'local-fixture' || r.action !== 'continue'));
      assert.equal(p.checks['DC-R5'], 'inconclusive');
    }
    assert.equal(report.admitted, false);
    await verifyCaptures(output, JSON.parse(await readFile(join(output, 'report.json'))));
  } finally { await rm(parent, { recursive: true, force: true }); }
});
