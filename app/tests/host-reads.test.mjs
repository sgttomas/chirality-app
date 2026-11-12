import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The order of the web view's host status reads. Controlled replies only: an
// invented host_status that the test resolves in the order it chooses.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {useOrderedHost, shownBeforePress, invoke, READ_COMMANDS} = loadSrc('hostReads');
const {readFileSync, readdirSync} = await import('node:fs');

function controlledHost() {
  const pending = [];
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke(command) { assert.equal(command, 'host_status'); return new Promise((resolve, reject) => pending.push({resolve, reject})); }};
  return {pending, restore() { window.__TAURI_INTERNALS__ = previous; }};
}
async function mount() {
  const api = {}; const c = document.createElement('div'); const root = createRoot(c);
  function Harness() { Object.assign(api, useOrderedHost()); return React.createElement('p', null, JSON.stringify(api.host)); }
  await React.act(async () => root.render(React.createElement(Harness)));
  return {api, text:() => c.textContent, close:() => React.act(async () => root.unmount())};
}

test('a reply is applied only if its read started after the one whose reply is shown', async () => {
  const host = controlledHost(); const ui = await mount();
  try {
    assert.equal(ui.api.hostReads.started(), 0); assert.equal(ui.api.hostReads.applied, 0); assert.equal(ui.api.host, null);
    const first = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')), second = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')), third = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status'));
    assert.equal(ui.api.hostReads.started(), 3, 'a read is numbered when it starts, not when it replies');
    // The second read replies first.
    host.pending[1].resolve({view:'second'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await second), true); });
    assert.equal(ui.text(), '{"view":"second"}'); assert.equal(ui.api.hostReads.applied, 2);
    // The first read's reply arrives late: it is older and is not applied.
    host.pending[0].resolve({view:'first'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await first), false, 'an older read never replaces a newer one'); });
    assert.equal(ui.text(), '{"view":"second"}'); assert.equal(ui.api.hostReads.applied, 2);
    // The same read is not applied twice, and a newer one is.
    await React.act(async () => { assert.equal(ui.api.applyHost(await second), false); });
    host.pending[2].resolve({view:'third'});
    await React.act(async () => { assert.equal(ui.api.applyHost(await third), true); });
    assert.equal(ui.text(), '{"view":"third"}'); assert.equal(ui.api.hostReads.applied, 3);
    // A read that fails is numbered and applies nothing.
    const failed = ui.api.readHost(window.__TAURI_INTERNALS__.invoke('host_status')); host.pending[3].reject(new Error('invented failure'));
    await assert.rejects(failed, /invented failure/);
    assert.equal(ui.api.hostReads.started(), 4); assert.equal(ui.api.hostReads.applied, 3);
  } finally { await ui.close(); host.restore(); }
});

// A host whose every command is held until the test settles it, in the order the test chooses.
function heldHost() {
  const pending = [];
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke(command) { return new Promise((resolve, reject) => pending.push({command, resolve, reject})); }};
  return {pending, of:command => pending.filter(entry => entry.command === command), restore() { window.__TAURI_INTERNALS__ = previous; }};
}
const statusRead = api => api.readHost(invoke('host_status'));

test('after any command that is not a listed read settles, the view is from before it until a read started afterwards is applied', async () => {
  const host = heldHost(); const ui = await mount();
  const stale = () => shownBeforePress(ui.api.hostReads);
  try {
    assert.equal(stale(), false, 'no command has settled');
    const during = [];
    for (const [outcome, settle] of [['resolved', entry => entry.resolve({state:'ok'})], ['rejected', entry => entry.reject(new Error('invented refusal'))]]) {
      const before = statusRead(ui.api);                       // started before the command settles
      const command = invoke('invented_host_command', {});      // not a listed read: unknown commands mark
      const whileIssued = statusRead(ui.api);                  // started while the command is in flight
      assert.equal(stale(), false, `${outcome}: a command in flight marks nothing`);
      await React.act(async () => { settle(host.of('invented_host_command').at(-1)); await command.catch(() => undefined); });
      assert.equal(ui.api.hostReads.settledAt, ui.api.hostReads.started(), `${outcome}: the mark is the number of reads started when the command settled`);
      assert.equal(stale(), true, `${outcome}: settled either way, the view is from before it`);
      // Replies to reads started before the settle are applied in their order and do not clear the mark.
      const held = host.of('host_status').slice(-2);
      held[1].resolve({view:`${outcome}: read during the command`});
      await React.act(async () => { assert.equal(ui.api.applyHost(await whileIssued), true); });
      assert.equal(stale(), true, `${outcome}: a read started during the command cannot follow it`);
      held[0].resolve({view:'older'});
      await React.act(async () => { assert.equal(ui.api.applyHost(await before), false); });
      assert.equal(stale(), true);
      // A read started after the settle that fails applies nothing; its message is kept beside the mark.
      const failed = statusRead(ui.api); host.of('host_status').at(-1).reject(new Error('invented read failure'));
      await React.act(async () => { await failed.catch(() => undefined); });
      assert.equal(stale(), true); assert.equal(ui.api.hostReads.failure, 'Error: invented read failure');
      // A read started after the settle, applied: the view follows the command, and the failure is behind it.
      const after = statusRead(ui.api); host.of('host_status').at(-1).resolve({view:`${outcome}: read after the command`});
      await React.act(async () => { assert.equal(ui.api.applyHost(await after), true); });
      assert.equal(stale(), false, `${outcome}: a read started after the settle has been applied`);
      assert.equal(ui.api.hostReads.failure, null);
      during.push(ui.text());
    }
    assert.deepEqual(during, ['{"view":"resolved: read after the command"}', '{"view":"rejected: read after the command"}']);
    // The status read and every listed read mark nothing, resolved or rejected.
    for (const command of ['host_status', ...READ_COMMANDS]) for (const settle of ['resolve', 'reject']) {
      const issued = invoke(command, {});
      await React.act(async () => { host.of(command).at(-1)[settle](settle === 'reject' ? new Error('x') : {}); await issued.catch(() => undefined); });
      assert.equal(stale(), false, `${command} ${settle}: a read marks nothing`);
    }
  } finally { await ui.close(); host.restore(); }
});

test('the list of read commands is closed, and every command the web view issues goes through the marking function or is a named exception', () => {
  // Closed: a command is added here only after its host function has been read and found to change nothing.
  assert.deepEqual([...READ_COMMANDS], ['collaboration_modes_read', 'decision_view', 'native_confirmation_content', 'read_available_models', 'read_configured_providers', 'read_connector_routes',
    'read_effective_access_settings', 'read_fleet_records', 'read_home_access', 'read_recovery_custody', 'read_recovery_request_history', 'role_supply_history', 'workflow_review_digest']);
  const src = new URL('../src/', import.meta.url);
  const platform = /from "@tauri-apps\/api\/core"/;
  const direct = {};
  for (const name of readdirSync(src).filter(name => /\.tsx?$/.test(name))) {
    const text = readFileSync(new URL(name, src), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
    if (!platform.test(text) || !/\binvoke\b/.test(text.split('\n').find(line => platform.test(line)))) continue;
    direct[name] = [...new Set([...text.matchAll(/invoke(?:<[^(]*>)?\(\s*"([a-z_]+)"/g)].map(match => match[1]))].sort();
  }
  // The modules that call the platform directly, with exactly the commands they issue there. hostReads.ts is the
  // marking function itself. The other three issue no press: the waiting bridge is pumped by a timer and an event,
  // the observer attachment by the host's own retention, and the model choice issues one listed read.
  assert.deepEqual(direct, {
    'ModelChoice.tsx':['read_available_models'],
    'NativeWaitingBridge.tsx':['checkpoint_native_waiting_ui', 'claim_native_waiting_intent', 'finish_native_waiting_intent'],
    'ObserverAttachment.tsx':['host_observe'],
    'hostReads.ts':[],
  });
  assert.ok(READ_COMMANDS.includes('read_available_models'));
  const shell = readFileSync(new URL('App.tsx', src), 'utf8');
  assert.match(shell, /import \{ invoke, useOrderedHost, shownBeforePress \} from "\.\/hostReads";/, 'the shell issues every command through the marking function');
  assert.doesNotMatch(shell, /setHost\(/);
});

test('mounted App: a command issued outside the workflow panel withholds the Run guide until a later status read is applied', async () => {
  // Review finding: End run pressed in the conversation goes through the shell's command function, not the
  // workflow panel. With the following status reply held the Run guide went on offering "End this run".
  const {installIdleNativeWaiting} = await import('./support/idle-native-waiting.mjs');
  const {App} = loadSrc('App');
  const g = {home:'account', appSession:'s1', spawnCounter:1};
  const thread = id => ({generation:g, threadId:id, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
  const run = state => ({reference:'run-1', conversation:'T2', home:'account', generation:g, source:'sent', workflow:{name:'invented-flow', origin:'project', revision:'r'}, lifecycle:{state}, status:{}});
  const view = runs => ({state:'ready', generation:g, threads:[thread('T1'), thread('T2')], roleLimits:{account:{roles:[]}}, homeRouting:{activeModeHomeClass:'account'}, serverRequests:[],
    workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs, drafts:{drafts:[]}}});
  const OPEN = "open (live); only the person's explicit end ends it";
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  const timers = []; globalThis.setInterval = fn => { timers.push(fn); return timers.length; }; globalThis.clearInterval = () => {};
  let runs = [run(OPEN)], hold = null, failStatus = false;
  const idle = installIdleNativeWaiting(async command => {
    if (command === 'host_status') { if (failStatus) throw new Error('invented status failure'); const snapshot = structuredClone(view(runs)); if (hold) await hold; return snapshot; }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'workflow_end_run') { runs = [run('ended by the person')]; return {state:'ended'}; }
    assert.fail(`Unexpected IPC: ${command}`);
  });
  const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
  const nodes = tag => c.querySelectorAll(node => node.localName === tag);
  const guide = () => c.querySelectorAll(node => node.getAttribute('id') === 'run-workflow')[0];
  const poll = () => timers.find(fn => fn.toString().includes('host_status'))();
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const guideSelect = nodes('select').find(n => n.parentNode.textContent.startsWith('Conversation to run it in'));
    await React.act(async () => props(guideSelect).onChange({target:{value:'T2'}}));
    assert.ok(nodes('button').some(b => b.textContent === 'End this run' && !props(b).disabled), 'the open run offers End this run');
    // The shell's command function, as the conversation's own End run uses it; the status read that follows is held.
    let release; hold = new Promise(resolve => { release = resolve; });
    await React.act(async () => { await invoke('workflow_end_run', {runRef:'run-1', finishedReport:null}); poll(); });
    assert.match(guide().textContent, /^Run a workflowNext: What this view showed may be from before your last press\./);
    assert.ok(!nodes('button').some(b => b.textContent === 'End this run'), 'nothing from before the command is offered');
    // A status read that fails leaves it withheld, with the failure said in the guide.
    hold = null; failStatus = true;
    await React.act(async () => { poll(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.match(guide().textContent, /What this view showed may be from before your last press\..*The last read failed: Error: invented status failure/);
    // The held reply, from a read started after the command, arrives: the guide returns with the state after it.
    failStatus = false;
    await React.act(async () => { release(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.doesNotMatch(guide().textContent, /may be from before your last press|The last read failed/);
    assert.ok(!nodes('button').some(b => b.textContent === 'End this run'), 'the ended run no longer offers End this run');
    idle.assertClean(c);
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, previous); }
});

test('whether a view is from before the last command is read from the reads\' order alone', () => {
  const reads = (applied, settledAt) => ({started:() => 0, applied, settledAt, failure:null});
  assert.equal(shownBeforePress(reads(5, null)), false, 'no command has settled');
  assert.equal(shownBeforePress(undefined), false, 'without the reads\' order nothing is claimed either way');
  assert.equal(shownBeforePress(reads(2, 3)), true, 'the read shown started before the command settled');
  assert.equal(shownBeforePress(reads(3, 3)), true, 'the last read started before the settle is still from before it');
  assert.equal(shownBeforePress(reads(4, 3)), false, 'a read started after the settle');
});
