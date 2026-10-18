import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {RecoveryCustodyPanel} = loadSrc('RecoveryCustodyPanel');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
let output;
if (process.env.CHIRALITY_REQUEST_HISTORY_DTO_LOG) {
  output = readFileSync(process.env.CHIRALITY_REQUEST_HISTORY_DTO_LOG, 'utf8');
  assert.match(output, /test result: ok/);
  assert.doesNotMatch(output, /test result: FAILED/);
} else {
  const result = spawnSync('cargo', ['test','--offline','--locked','--lib','recovery_root_cold_','--','--nocapture','--test-threads=1'], {
    cwd: fileURLToPath(new URL('../src-tauri/', import.meta.url)), encoding: 'utf8', timeout: 180000, maxBuffer: 8*1024*1024,
    env: {...process.env, CHIRALITY_SKIP_CODEX:'1', CARGO_NET_OFFLINE:'true'},
  });
  assert.equal(result.status, 0, result.error?.message ?? result.stdout+result.stderr);
  output = result.stdout;
}
const actual = new Map(output.split(/\r?\n/).filter(line => line.includes('REQUEST_HISTORY_DTO '))
  .map(line => JSON.parse(line.slice(line.indexOf('REQUEST_HISTORY_DTO ') + 'REQUEST_HISTORY_DTO '.length))).map(value => [value.scenario, value.view]));
for (const scenario of ['app-quit','supplier-stop','app-ended-without-record']) assert.ok(actual.has(scenario), scenario);
const original = actual.get('app-quit');
function mounted(readRequests, initial = original.source) {
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  let source = initial;
  return {container,
    show: next => { source = next ?? source; return React.act(() => root.render(React.createElement(RecoveryCustodyPanel, {
      modeHomeClass:source.modeHomeClass, generation:source.generation, nativeHistoryGeneration:null,
      read:async () => { throw new Error('cached custody was not requested'); }, readRequests,
    }))); },
    button: label => container.querySelectorAll(node => node.localName === 'button' && node.textContent === label)[0],
    async press(label) { const button = this.button(label); assert.ok(button, label); assert.equal(props(button).disabled,false); await React.act(async () => props(button).onClick()); },
    close: () => React.act(() => root.unmount()),
  };
}

test('actual cold RQ04 and RQ06 DTOs stay historical and require an explicit bounded read', async () => {
  for (const [scenario, dto] of actual) {
    const calls = [];
    const view = mounted(async cursor => {calls.push(cursor);return dto;}, dto.source);
    try {
      await view.show(); assert.deepEqual(calls, [], 'mount and ordinary metadata presentation do not query the ledger');
      await view.press('Read latest request summaries');
      assert.deepEqual(calls, [null]);
      assert.match(view.container.textContent, /ended-unanswered\(process-exit\)/, scenario);
      assert.match(view.container.textContent, /original-request-home/);
      assert.match(view.container.textContent, /old-request-session/);
      assert.match(view.container.textContent, /cannot be answered here/);
      assert.match(view.container.textContent, /reply write: not-attempted; acknowledgment: not-observed/);
      const history = view.container.querySelectorAll(node => node.getAttribute('aria-label') === 'Persisted terminal request summaries')[0];
      assert.deepEqual(history.querySelectorAll(node => node.localName === 'button').map(node => node.textContent), ['Read latest request summaries']);
    } finally {await view.close();}
  }
});

test('earlier pages use only the received cursor and failed reads do not reuse cached success', async () => {
  const cursor = {source:'opaque-original-ledger',throughSequence:'9007199254740993',beforeSequence:'12'};
  const first = structuredClone(original); first.page.nextCursor = cursor; first.page.hasMore = true;
  const calls = [];
  const view = mounted(async next => {calls.push(next);if (next) throw new Error('original ledger unavailable');return first;});
  try {
    await view.show(); await view.press('Read latest request summaries');
    await view.press('Read earlier request summaries');
    assert.deepEqual(calls,[null,cursor]);
    assert.match(view.container.textContent,/original ledger unavailable/);
    assert.doesNotMatch(view.container.textContent,/old-question/,'a failed current read cannot be masked by the prior successful page');
  } finally {await view.close();}
});

test('foreign replies and completion after home selection changes do not populate the new source', async () => {
  let resolve;
  let returned = original;
  const view = mounted(() => new Promise(done => {resolve = done;}));
  try {
    await view.show();
    React.act(() => {props(view.button('Read latest request summaries')).onClick();});
    const other = {modeHomeClass:'api-key',generation:{appSession:'new-session',home:'new-home',spawnCounter:1}};
    await view.show(other);
    await React.act(async () => resolve(returned));
    assert.doesNotMatch(view.container.textContent,/old-question/);
    React.act(() => {props(view.button('Read latest request summaries')).onClick();});
    await React.act(async () => resolve(returned));
    assert.match(view.container.textContent,/different source/);
    assert.doesNotMatch(view.container.textContent,/old-question/);
  } finally {await view.close();}
});

test('terminal outcome and typed identities are displayed without relabeling them unanswered', async () => {
  const dto = structuredClone(original);
  dto.page.entries = ['answered','declined','reply-outcome-unknown','errored','resolved-by-supplier'].map((endedAs,index) => ({
    ...structuredClone(original.page.entries[0]), requestIdentityType:index % 2 ? 'string' : 'integer',
    summary:{...original.page.entries[0].summary, endedAs, requestIdentity:index % 2 ? '"1"' : '1', transition:endedAs === 'reply-outcome-unknown' ? 'RQ-10' : 'RQ-03', replyWrite:endedAs === 'reply-outcome-unknown' ? 'unknown' : 'written', acknowledgment:'not-observed'},
  }));
  const view = mounted(async () => dto);
  try {
    await view.show(); await view.press('Read latest request summaries');
    const summaries = view.container.querySelectorAll(node => node.localName === 'summary').map(node => node.textContent);
    for (const endedAs of ['answered','declined','reply-outcome-unknown','errored','resolved-by-supplier']) assert.ok(summaries.some(text => text.startsWith(endedAs+':')), endedAs);
    assert.ok(summaries.some(text => text.includes('request 1 ·')));
    assert.ok(summaries.some(text => text.includes('request "1" ·')));
    assert.ok(summaries.every(text => !text.startsWith('Ended unanswered:')));
    assert.match(view.container.textContent,/reply write: unknown; acknowledgment: not-observed/);
  } finally {await view.close();}
});

test('serialized numeric and string IDs remain exact across the JSON transport boundary', async () => {
  const dto = structuredClone(original);
  dto.page.entries = ['9007199254740993','"9007199254740993"'].map(requestIdentity => ({
    ...structuredClone(original.page.entries[0]), requestIdentityType:requestIdentity.startsWith('"') ? 'string' : 'integer',
    summary:{...original.page.entries[0].summary,requestIdentity},
  }));
  const view = mounted(async () => JSON.parse(JSON.stringify(dto)));
  try {
    await view.show(); await view.press('Read latest request summaries');
    const summaries = view.container.querySelectorAll(node => node.localName === 'summary').map(node => node.textContent);
    assert.ok(summaries.some(text => text.includes('request 9007199254740993 ·')));
    assert.ok(summaries.some(text => text.includes('request "9007199254740993" ·')));
  } finally {await view.close();}
});
