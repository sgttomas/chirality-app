import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// Source-faithful maintained positive shapes from native-activity/request-cards
// fixtures, with NativeView::snapshot_with_requests' exact full-generation and
// thread/turn/item overlay. These are controlled IPC inputs to the actual App,
// not native producer/provider/GUI qualification or operational admission.
const generation = {appSession: 'request-activity-fixture', home: 'native-fixture-home', spawnCounter: 1};
const rootKey = JSON.stringify([generation, 'parent']);
const parentItem = {threadId: 'parent', turnId: 'parent-turn', itemId: 'parent-command'};
const childItem = {threadId: 'child', turnId: 'child-turn', itemId: 'child-command'};
const request = (at, id) => ({
  recordKind: 'server-request-entry', generation, requestIdentity: id,
  method: 'item/commandExecution/requestApproval', classification: 'known-answerable', originClass: 'a14',
  nativeParameters: {...at, command: 'ls -la', cwd: '/invented', reason: 'List the folder'},
  state: 'outstanding', replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'},
});
const nativeCommand = at => ({id: at.itemId, type: 'commandExecution', command: 'ls -la', cwd: '/invented', source: 'agent', status: 'inProgress', commandActions: []});
const liveRow = (at, order) => ({
  threadId: at.threadId, turnId: at.turnId, native: nativeCommand(at), displayState: 'in-progress',
  standing: 'live-observed', observationEnded: false, observedOrder: order, receipt: {generation, started: order + 1},
});
function fixture() {
  const requests = [request(parentItem, '7'), request(childItem, 7)];
  const spawn = {id: 'spawn-child', type: 'collabAgentToolCall', tool: 'spawnAgent', status: 'completed', senderThreadId: 'parent', receiverThreadIds: ['child'], agentsStates: {child: {status: 'running', message: null}}};
  const view = {home: generation.home, generation, typesPin: '0.160.0', supplierStanding: 'unverified-development',
    limits: ['Parent completion says nothing about children.', 'Child completion, return, review and integration are not inferred.'],
    items: [liveRow(parentItem, 0), liveRow(childItem, 2),
      {threadId: 'parent', turnId: 'parent-turn', native: spawn, displayState: 'completed', observedOrder: 1, standing: 'live-observed'},
      {threadId: 'child', turnId: 'child-turn', native: {id: 'child-message', type: 'agentMessage', text: 'Received child message'}, displayState: 'in-progress', observedOrder: 3, standing: 'live-observed'}],
    turns: [{id: 'parent-turn', status: 'completed', startedAt: 1}, {id: 'child-turn', status: 'inProgress', startedAt: 2}],
    turnRecords: [{threadId: 'parent', turnId: 'parent-turn'}, {threadId: 'child', turnId: 'child-turn'}], revisions: [], goals: {}, checklistGaps: [],
    descendants: [{threadId: 'child', parentThreadId: 'parent', parentSource: 'collabAgentToolCall.senderThreadId', statusSource: 'collabAgentToolCall.agentsStates', lastObservedStatus: spawn.agentsStates.child, lastNativeCall: spawn, guidance: 'not-known', observationEnded: false}],
  };
  for (const item of view.items) {
    const original = requests.findLast(r => JSON.stringify(r.generation) === JSON.stringify(view.generation)
      && r.nativeParameters.threadId === item.threadId && r.nativeParameters.turnId === item.turnId && r.nativeParameters.itemId === item.native.id);
    if (original) {item.requestRef = {generation: original.generation, requestIdentity: original.requestIdentity}; item.displayState = 'waiting-on-request'; item.settlementOrigin = null;}
  }
  return {state: 'ready', generation, threads: [{generation, threadId: 'parent', appRole: {standing: 'app-observed', role: null, supply_ref: 'parent-fixture-role'}, roleRelation: {kind: 'start'}, futureGuidanceNotices: []}],
    nativeView: view, serverRequests: requests, roleLimits: {account: {roles: []}}, homeRouting: {activeModeHomeClass: 'account', entries: [{modeHomeClass: 'account'}]}};
}
const document = installMiniDom();
// MiniDom has no layout/CSS API. Supply only the standard scoped ID lookup
// used by this interaction; its result is still an actual mounted element.
const elementPrototype = Object.getPrototypeOf(document.createElement('div'));
elementPrototype.querySelector = function(selector) {
  assert.match(selector, /^#[a-z0-9-]+$/);
  return this.querySelectorAll(element => element.getAttribute('id') === selector.slice(1))[0] ?? null;
};
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const {requestAnchorId, itemAnchorId} = loadSrc('NativeActivity');
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container, tag) => container.querySelectorAll(element => element.localName === tag);
const itemId = at => itemAnchorId(at.threadId, at.turnId, at.itemId);
const draft = 'Unsent parent text é / 家';
async function mounted(check, prepare = () => {}) {
  const host = fixture(), calls = [], timers = new Map(), scrolls = []; let timer = 0;
  prepare(host);
  const previousScroll = elementPrototype.scrollIntoView;
  elementPrototype.scrollIntoView = function() {scrolls.push(this);};
  const previousTimers = {setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval};
  globalThis.setInterval = (fn, ms) => {timers.set(++timer, {fn, ms}); return timer;};
  globalThis.clearInterval = id => timers.delete(id);
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return structuredClone(host);
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    throw Error(`Unexpected original command: ${command}`);
  });
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const byId = id => c.querySelectorAll(element => element.getAttribute('id') === id);
  const conversation = () => byId('conversation')[0];
  const activity = () => c.querySelectorAll(element => element.getAttribute('aria-label') === 'Native activity')[0];
  const choose = async (element, value) => React.act(() => props(element).onChange({target: {value}}));
  const show = thread => choose(elements(activity(), 'select')[0], thread);
  const read = () => [...timers.values()].find(timer => timer.fn.toString().includes('host_status')).fn();
  const poll = async () => React.act(async () => {read();});
  const card = id => byId(requestAnchorId(generation, id))[0];
  const about = (id, at) => elements(card(id), 'a').find(a => a.getAttribute('href') === `#${itemId(at)}`);
  const clickAbout = async (id, at) => {
    const link = about(id, at); assert.ok(link, 'About offers the original item');
    // A native fragment alone cannot reveal an unmounted thread. Exercise the
    // App handler when present, then assert its actual mounted destination.
    await React.act(async () => {await props(link).onClick?.({preventDefault() {}});});
  };
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await choose(elements(conversation(), 'select')[0], rootKey);
    await choose(elements(conversation(), 'textarea')[0], draft);
    const role = conversation().querySelectorAll(element => element.getAttribute('aria-label') === 'Conversation role')[0].textContent;
    await check({host, c, calls, scrolls, byId, conversation, activity, show, card, about, clickAbout, choose, read, poll});
    assert.equal(props(elements(conversation(), 'select')[0]).value, rootKey, 'read-only activity navigation never selects/adopts the child operationally');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft);
    assert.equal(conversation().querySelectorAll(element => element.getAttribute('aria-label') === 'Conversation role')[0].textContent, role);
    assert.deepEqual(host.threads.map(thread => thread.threadId), ['parent']);
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content'].includes(call.command)), 'no read/start/resume/send/answer/role RPC');
    idle.assertClean(c);
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    assert.equal(timers.size, 0); Object.assign(globalThis, previousTimers); elementPrototype.scrollIntoView = previousScroll;
  }
}

test('received descendant viewing and waiting-item forward links preserve original source and operational selection', async () => {
  await mounted(async ui => {
    assert.notEqual(requestAnchorId(generation, '7'), requestAnchorId(generation, 7));
    for (const foreign of [{...generation, home: 'other-home'}, {...generation, appSession: 'other-app'}, {...generation, spawnCounter: 2}]) assert.notEqual(requestAnchorId(generation, 7), requestAnchorId(foreign, 7));
    const parent = ui.byId(itemId(parentItem))[0];
    assert.ok(elements(parent, 'a').some(a => a.getAttribute('href') === `#${requestAnchorId(generation, '7')}`));
    assert.equal(ui.byId(requestAnchorId(generation, '7')).length, 1);
    assert.match(ui.activity().textContent, /child · last observed Codex status running/);
    assert.match(ui.activity().textContent, /guidance not known/);
    await ui.show('child');
    assert.match(ui.activity().textContent, /Received child message/);
    assert.match(ui.activity().textContent, /Descendant of parent/);
    const child = ui.byId(itemId(childItem))[0];
    assert.ok(elements(child, 'a').some(a => a.getAttribute('href') === `#${requestAnchorId(generation, 7)}`));
    assert.equal(ui.byId('other-requests')[0].querySelectorAll(element => element.getAttribute('id') === requestAnchorId(generation, 7)).length, 1);
    assert.ok(ui.about(7, childItem));
  });
});
test('About reveals the original parent item after Show descendant hides it', async () => {
  await mounted(async ui => {
    await ui.show('child'); assert.equal(ui.byId(itemId(parentItem)).length, 0);
    await ui.clickAbout('7', parentItem);
    assert.equal(ui.byId(itemId(parentItem)).length, 1, 'the reciprocal About target must be mounted after its explicit click');
    assert.equal(props(elements(ui.activity(), 'select')[0]).value, 'parent');
    assert.equal(ui.scrolls.at(-1), ui.byId(itemId(parentItem))[0], 'anchor the real activity row after render');
  });
});
test('outside-selected descendant About reveals its received item while keeping the parent conversation', async () => {
  await mounted(async ui => {
    assert.equal(ui.byId(itemId(childItem)).length, 0);
    await ui.clickAbout(7, childItem);
    assert.equal(ui.byId(itemId(childItem)).length, 1, 'the original descendant item is the reciprocal destination');
    assert.equal(props(elements(ui.activity(), 'select')[0]).value, 'child');
    assert.equal(ui.scrolls.at(-1), ui.byId(itemId(childItem))[0]);
    await ui.show('parent'); assert.equal(ui.byId(itemId(parentItem)).length, 1, 'ordinary Show control remains usable');
  });
});
test('About on an already displayed item preserves its original matching destination', async () => {
  await mounted(async ui => {
    await ui.clickAbout('7', parentItem);
    assert.equal(ui.byId(itemId(parentItem)).length, 1);
    assert.equal(ui.byId(requestAnchorId(generation, '7')).length, 1);
  });
});

for (const field of ['appSession', 'home', 'spawnCounter']) test(`retained older ${field} request cannot navigate to same-named current items`, async () => {
  let older;
  await mounted(async ui => {
    const oldCard = ui.byId(requestAnchorId(older.generation, older.requestIdentity))[0];
    assert.ok(oldCard);
    assert.equal(elements(oldCard, 'a').filter(a => a.getAttribute('href')?.startsWith('#item-')).length, 0);
    assert.match(oldCard.textContent, /About: Codex item/);
    await ui.clickAbout('7', parentItem); assert.equal(ui.scrolls.length, 1, 'the genuine current source remains reachable');
  }, host => {
    older = structuredClone(host.serverRequests[0]);
    older.generation[field] = field === 'spawnCounter' ? 2 : `foreign-${field}`;
    host.serverRequests.push(older);
  });
});
for (const mismatch of ['view-generation', 'view-home', 'subtree', 'missing-row']) test(`About uses identity fallback when ${mismatch} makes its target unavailable`, async () => {
  await mounted(async ui => {
    assert.equal(ui.about(7, childItem), undefined);
    assert.match(ui.card(7).textContent, /About: Codex item/);
    assert.equal(ui.scrolls.length, 0);
  }, host => {
    if (mismatch === 'view-generation') host.nativeView.generation = {...generation, spawnCounter: 2};
    if (mismatch === 'view-home') host.nativeView.home = 'foreign-native-home';
    if (mismatch === 'subtree') host.nativeView.descendants = [];
    if (mismatch === 'missing-row') host.nativeView.items = host.nativeView.items.filter(row => row.native.id !== childItem.itemId);
  });
});
test('source-qualified file-change details survive navigation outside the selected root subtree', async () => {
  await mounted(async ui => {
    const card = ui.card('unrelated-change');
    assert.match(card.textContent, /received-file.txt/); assert.match(card.textContent, /distinct received diff/);
    assert.equal(elements(card, 'a').filter(a => a.getAttribute('href')?.startsWith('#item-')).length, 0);
    assert.match(card.textContent, /About: Codex item/);
  }, host => {
    const at = {threadId: 'unrelated', turnId: 'unrelated-turn', itemId: 'file-change'};
    host.serverRequests.push({...request(at, 'unrelated-change'), method: 'item/fileChange/requestApproval', nativeParameters: {...at, reason: 'Synthetic file change'}});
    host.nativeView.items.push({...liveRow(at, 9), native: {id: at.itemId, type: 'fileChange', status: 'inProgress', changes: [{path: 'received-file.txt', kind: {type: 'update'}, diff: '+distinct received diff'}]}});
  });
});
test('settled original cards can reveal their received item without becoming answerable again', async () => {
  await mounted(async ui => {
    await ui.show('child'); await ui.clickAbout('7', parentItem);
    assert.equal(ui.byId(itemId(parentItem)).length, 1); assert.equal(ui.scrolls.length, 1);
    assert.match(ui.card('7').textContent, /Resolved by Codex before you answered/);
  }, host => {
    host.serverRequests[0].state = 'resolved-by-supplier'; host.serverRequests[0].supplierResolution = {cause: 'native notification'};
    host.nativeView.items.find(row => row.native.id === parentItem.itemId).displayState = 'in-progress';
  });
});
test('About preserves the request card permission scope while revealing its original item', async () => {
  await mounted(async ui => {
    const select = () => elements(ui.card('7'), 'select')[0];
    await ui.choose(select(), 'session'); await ui.show('child'); await ui.clickAbout('7', parentItem);
    assert.equal(props(select()).value, 'session'); assert.equal(ui.scrolls.length, 1);
  }, host => {
    host.serverRequests[0].method = 'item/permissions/requestApproval';
    host.serverRequests[0].nativeParameters = {...parentItem, cwd: '/invented', permissions: {network: {enabled: true}}, reason: null};
  });
});
test('About preserves a local question draft without submitting it', async () => {
  await mounted(async ui => {
    const input = () => elements(ui.card('7'), 'input')[0];
    await ui.choose(input(), 'Unsent question answer'); await ui.show('child'); await ui.clickAbout('7', parentItem);
    assert.equal(props(input()).value, 'Unsent question answer'); assert.equal(ui.scrolls.length, 1);
  }, host => {
    host.serverRequests[0].method = 'item/tool/requestUserInput'; host.serverRequests[0].originClass = 'person-input';
    host.serverRequests[0].nativeParameters = {...parentItem, questions: [{id: 'q', header: 'Question', question: 'Which?', isOther: true, isSecret: false, options: []}]};
  });
});
test('a newer explicit Show choice supersedes a reveal before its render and anchor', async () => {
  await mounted(async ui => {
    const open = props(ui.about(7, childItem)).onClick;
    const manual = props(elements(ui.activity(), 'select')[0]).onChange;
    await React.act(() => {React.startTransition(() => open({preventDefault() {}})); manual({target: {value: 'parent'}});});
    assert.equal(props(elements(ui.activity(), 'select')[0]).value, 'parent'); assert.equal(ui.scrolls.length, 0);
    await ui.poll(); assert.equal(ui.byId(itemId(childItem)).length, 0, 'read cannot revive superseded About intent');
  });
});
test('newer operational selection away and back invalidates an older captured About handler', async () => {
  await mounted(async ui => {
    const old = props(ui.about(7, childItem)).onClick;
    const selector = () => elements(ui.conversation(), 'select')[0];
    await ui.choose(selector(), ''); await ui.choose(selector(), rootKey);
    await React.act(() => old({preventDefault() {}}));
    assert.equal(ui.byId(itemId(childItem)).length, 0); assert.equal(ui.scrolls.length, 0);
  });
});
for (const replacement of ['row', 'subtree', 'request', 'source']) test(`pending About is cancelled by ${replacement} replacement and never revived on read`, async () => {
  await mounted(async ui => {
    const original = structuredClone(ui.host), old = props(ui.about(7, childItem)).onClick;
    await React.act(async () => {
      React.startTransition(() => old({preventDefault() {}}));
      if (replacement === 'row') ui.host.nativeView.items = ui.host.nativeView.items.filter(row => row.native.id !== childItem.itemId);
      if (replacement === 'subtree') ui.host.nativeView.descendants = [];
      if (replacement === 'request') ui.host.serverRequests = ui.host.serverRequests.filter(request => request.requestIdentity !== 7);
      if (replacement === 'source') {ui.host.state = 'exited'; ui.host.generationClosed = true;}
      await ui.read();
    });
    assert.equal(ui.scrolls.length, 0);
    Object.assign(ui.host, original); await ui.poll();
    assert.equal(ui.byId(itemId(childItem)).length, 0, 'restoring received data does not revive the cancelled navigation');
    await React.act(() => old({preventDefault() {}})); assert.equal(ui.scrolls.length, 0, 'old callback stays cancelled');
  });
});

test('newer operational choice ABA cancels a deferred About even when its final root is unchanged', async () => {
  await mounted(async ui => {
    const old = props(ui.about(7, childItem)).onClick;
    const select = props(elements(ui.conversation(), 'select')[0]).onChange;
    await React.act(() => {
      React.startTransition(() => old({preventDefault() {}}));
      select({target: {value: ''}}); select({target: {value: rootKey}});
    });
    assert.equal(ui.scrolls.length, 0); assert.equal(ui.byId(itemId(childItem)).length, 0);
    await ui.poll(); assert.equal(ui.scrolls.length, 0);
  });
});
