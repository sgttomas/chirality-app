import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The order of the web view's host status reads. Controlled replies only: an
// invented host_status that the test resolves in the order it chooses.
// Run alone it installs the test DOM; imported by a listed test file it uses that file's, so one document serves both.
if (!globalThis.document) installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {useOrderedHost, shownBeforePress, invoke, SELF_ISSUED_QUIET, POLL_MS} = loadSrc('hostReads');
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

test('after a command settles, the view is from before it until a read started afterwards is applied; only the self-issued commands listed mark nothing', async () => {
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
    // The status read and every listed self-issued command mark nothing, resolved or rejected.
    for (const command of ['host_status', ...Object.keys(SELF_ISSUED_QUIET)]) for (const settle of ['resolve', 'reject']) {
      const issued = invoke(command, {});
      await React.act(async () => { host.of(command).at(-1)[settle](settle === 'reject' ? new Error('x') : {}); await issued.catch(() => undefined); });
      assert.equal(stale(), false, `${command} ${settle}: marks nothing`);
    }
  } finally { await ui.close(); host.restore(); }
});

test('the commands that mark nothing are a closed table of self-issued commands, and every command goes through the one function', () => {
  // Closed. A command is added only when the web view issues it by itself (a timer, or an effect that re-runs with
  // nothing pressed) and its host function has been read: the value is that function's own effect. A command a
  // person presses is never listed, whatever it does. Review of the first list found ten pressed commands on it and
  // five that change other reported state; none of them is here.
  assert.deepEqual(SELF_ISSUED_QUIET, {
    checkpoint_native_waiting_ui:'the waiting-navigation registry only, which neither guide shows',
    claim_native_waiting_intent:'claim ownership in the waiting-navigation registry; reconciliation only',
    decision_view:"reads the decision projection; where the records store was not opened at startup, opening it can create the store's folder and store.json; neither guide shows either",
    finish_native_waiting_intent:'the waiting-navigation registry only, which neither guide shows',
    host_observe:'queues an observer reconstruction kept apart from live activity; reconciliation only',
    native_confirmation_content:'none',
    workflow_review_digest:'none',
  });
  for (const pressed of ['collaboration_modes_read', 'read_available_models', 'read_configured_providers', 'read_connector_routes', 'read_effective_access_settings', 'read_fleet_records',
    'read_home_access', 'read_recovery_custody', 'read_recovery_request_history', 'role_supply_history'])
    assert.equal(Object.hasOwn(SELF_ISSUED_QUIET, pressed), false, `${pressed} is pressed (read_home_access also follows a sign-in): it marks`);
  assert.equal(POLL_MS, 1000, 'the stated bound on how far the view is behind what the host learns by itself');
  // One route: no module but hostReads.ts takes the platform's command function, in any import form.
  const src = new URL('../src/', import.meta.url);
  const takesPlatform = [];
  for (const name of readdirSync(src).filter(name => /\.tsx?$/.test(name))) {
    const text = readFileSync(new URL(name, src), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
    if (/@tauri-apps\/api\/core/.test(text) || /__TAURI_INTERNALS__/.test(text)) takesPlatform.push(name);
  }
  assert.deepEqual(takesPlatform, ['hostReads.ts']);
  const shell = readFileSync(new URL('App.tsx', src), 'utf8');
  assert.match(shell, /import \{ invoke, useOrderedHost, shownBeforePress, POLL_MS \} from "\.\/hostReads";/, 'the shell issues every command through the marking function');
  assert.match(shell, /readHost\(invoke<Json>\("host_status"\)\)\.then\(applyHost\)[^\n]*, POLL_MS\);/, 'the poll runs at the stated interval');
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
  const issued = new Set();
  const idle = installIdleNativeWaiting(async command => {
    issued.add(command);
    if (command === 'host_status') { if (failStatus) throw new Error('invented status failure'); const snapshot = structuredClone(view(runs)); if (hold) await hold; return snapshot; }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === 'workflow_end_run') { runs = [run('ended by the person')]; return {state:'ended'}; }
    if (command === 'workflow_open_project_library') return {state:'opened'};
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
    // With nothing pressed (mount, a choice in the guide that issues no command, every timer fired once), the App
    // issues only the status read and listed self-issued commands, and the guide is shown, not withheld.
    await React.act(async () => { for (const fire of timers) fire(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.deepEqual([...issued].filter(command => command !== 'host_status' && !Object.hasOwn(SELF_ISSUED_QUIET, command)), [], 'a self-issued command that is not classified');
    assert.doesNotMatch(guide().textContent, /may be from before the App's last operation finished/);
    // The invariant's one exception, and its end, for a press made in the panel (Agent 0's decision on round 3).
    const settle = () => React.act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
    const press = label => React.act(async () => { props(nodes('button').find(b => b.textContent === label)).onClick(); await new Promise(resolve => setTimeout(resolve, 0)); });
    const result = () => c.querySelectorAll(node => node.getAttribute('aria-label') === 'Run a workflow — last result')[0];
    const WITHHELD = /may be from before the App's last operation finished/;
    // (1) While the press is in progress (its command settled, the refresh that follows held): the steps from
    // before it stay, every control that could change the host is disabled, and its result is not yet said.
    let free; hold = new Promise(resolve => { free = resolve; });
    await press("Show this project's workflows");
    assert.doesNotMatch(guide().textContent, WITHHELD, 'in progress: the steps stay');
    assert.equal(result(), undefined, 'in progress: the result is not yet said');
    for (const label of ["Show this project's workflows", 'End this run']) assert.equal(props(nodes('button').find(b => b.textContent === label)).disabled, true, `in progress: ${label} is disabled`);
    // The refresh resolves: no longer in progress, and the read that followed the command is applied.
    hold = null; free(); await settle();
    assert.doesNotMatch(guide().textContent, WITHHELD); assert.match(result().textContent, /^Opened this project's workflow library\./);
    // (2) The refresh after a press rejects: the press is no longer in progress (not busy for ever), and the
    // guide is withheld, with the failed read said in it.
    failStatus = true;
    await press("Show this project's workflows");
    assert.match(guide().textContent, WITHHELD, 'a rejected refresh ends the press; the guide is withheld, which it is only when the panel is not busy');
    assert.match(guide().textContent, /The last read failed: Error: invented status failure/);
    assert.ok(!nodes('button').some(b => b.textContent === 'End this run'));
    failStatus = false;
    await React.act(async () => { poll(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.doesNotMatch(guide().textContent, WITHHELD, 'a read started after the command, applied: the steps return');
    assert.doesNotMatch(guide().textContent, /read failed|read of its state failed/, 'and the failure is behind it');
    // A status read that fails with no command outstanding withholds nothing, and the guide says so above its steps:
    // one second is the poll's schedule, not a bound on how old the view is.
    failStatus = true;
    await React.act(async () => { poll(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.doesNotMatch(guide().textContent, WITHHELD);
    assert.match(guide().textContent, /The App's last read of its state failed \(Error: invented status failure\)\. What is shown here was read before that\./);
    assert.ok(nodes('button').some(b => b.textContent === 'End this run'), 'the steps stay: nothing says they are wrong');
    failStatus = false;
    await React.act(async () => { poll(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.doesNotMatch(guide().textContent, /read of its state failed/);
    // (3) A command issued outside the panel withholds at once. The shell's command function, as the conversation's
    // own End run uses it; the status read that follows is held.
    let release; hold = new Promise(resolve => { release = resolve; });
    await React.act(async () => { await invoke('workflow_end_run', {runRef:'run-1', finishedReport:null}); poll(); });
    assert.match(guide().textContent, /^Run a workflowNext: What this view showed may be from before the App's last operation finished\./);
    assert.ok(!nodes('button').some(b => b.textContent === 'End this run'), 'nothing from before the command is offered');
    // A status read that fails leaves it withheld, with the failure said in the guide.
    hold = null; failStatus = true;
    await React.act(async () => { poll(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.match(guide().textContent, /What this view showed may be from before the App's last operation finished\..*The last read failed: Error: invented status failure/);
    // The held reply, from a read started after the command, arrives: the guide returns with the state after it.
    failStatus = false;
    await React.act(async () => { release(); await new Promise(resolve => setTimeout(resolve, 0)); });
    assert.doesNotMatch(guide().textContent, /may be from before the App's last operation finished|The last read failed/);
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
