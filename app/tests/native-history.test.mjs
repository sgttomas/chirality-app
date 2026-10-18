import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {continuationFixture} from './support/continuation-fixture.mjs';

const {historyPageBinding, StoredItemPage, StoredTurnPage, ContinuationContext, continuationContextBinding, continuationPageBinding} = loadSrc('NativeHistory');
const {NativeActivityView, NativeItemCard, historyItemRow} = loadSrc('NativeActivity');
const generation = {appSession: 'history-session', home: 'history-home', spawnCounter: 2};
const clone = value => structuredClone(value);
const item = (id, type, fields = {}) => ({id, type, ...fields});
const entry = native => ({turnId: 'turn-source', item: native, startedAtMs: 10, completedAtMs: 20, entryExtra: 'kept'});
const nativeItems = () => [
  item('agent', 'agentMessage', {text: 'Stored final <answer>', phase: 'final_answer'}),
  item('user', 'userMessage', {content: [{type: 'text', text: 'Stored input <script>unsafe()</script>', text_elements: []}]}),
  item('reason', 'reasoning', {summary: ['Stored reasoning summary'], content: []}),
  item('plan', 'plan', {text: 'Stored plan: inspect, then repair'}),
  item('cmd', 'commandExecution', {command: 'inspect sample', cwd: '/invented', source: 'agent', status: 'completed', exitCode: 0, durationMs: 12, aggregatedOutput: 'Stored command output'}),
  item('file', 'fileChange', {status: 'failed', changes: [{path: 'sample.txt', kind: {type: 'update'}, diff: '+stored change'}]}),
  item('mcp', 'mcpToolCall', {server: 'sample', tool: 'read', status: 'completed', arguments: {path: 'sample'}, result: {content: [{type: 'text', text: 'Stored MCP text'}, {type: 'resource', resource: {text: 'Stored resource text', uri: 'invented://resource'}}], structuredContent: {kept: 1}}, error: null}),
  item('dynamic', 'dynamicToolCall', {tool: 'inspect', arguments: {}, status: 'completed', success: true, contentItems: [{type: 'inputText', text: 'Stored App tool text'}, {type: 'inputImage', imageUrl: 'https://example.invalid/never-load'}]}),
  item('function', 'functionCallOutput', {name: 'evaluate', output: 'Stored function result'}),
  item('spawn', 'collabAgentToolCall', {tool: 'spawnAgent', status: 'completed', senderThreadId: 'stored', receiverThreadIds: ['child'], agentsStates: {child: {status: 'running', message: 'Still working at the read'}}, prompt: 'Inspect a bounded assignment'}),
  item('child-reference', 'subAgentActivity', {kind: 'started', agentPath: '/root/child', agentThreadId: 'child'}),
  item('unknown', 'futureNativeKind', {status: 'futureStatus', nativeExtra: {unchanged: true}}),
];
function query(kind, id = kind === 'items' ? 22 : 21) {
  return {factory_id: 7, query_id: id, home: generation.home, generation: clone(generation), method: `thread/${kind}/list`, params: {threadId: 'stored', ...(kind === 'items' ? {turnId: 'turn-source'} : {itemsView: 'summary'}), sortDirection: kind === 'items' ? 'desc' : 'asc'}};
}
function fixture() {
  return {state: 'ready', generation: clone(generation), nativeItems: {items: [{native: item('outside', 'agentMessage', {text: 'Must not hydrate this live projection'})}]}, nativeHistory: {
    home: generation.home, generation: clone(generation), state: 'history-receiving', selectionEpoch: 3,
    threads: [{native: {id: 'stored', status: {type: 'notLoaded'}, preview: 'Stored conversation'}}], dispatches: [],
    selected: {threadId: 'stored', state: 'indexed-read-only', appRole: {standing: 'unknown'},
      // Deliberately contradictory mutable fields: accepted queries own identity.
      itemTurnId: 'wrong-intent-turn', itemDirection: 'asc', turnDirection: 'desc',
      turnsPage: {data: [{id: 'turn-source', status: 'completed', itemsView: 'summary', startedAt: 1, durationMs: 12, items: [nativeItems()[1], nativeItems()[0]]}], nextCursor: 'turn-next', backwardsCursor: 'turn-back'},
      itemsPage: {data: nativeItems().map(entry), nextCursor: 'item-next', backwardsCursor: 'item-back', pageExtra: 'preserved page'},
      streamResolutions: {'turn-pages': {query: query('turns'), revision: 1, outcome: 'native-result-observed'}, 'item-pages': {query: query('items'), revision: 2, outcome: 'native-result-observed'}},
      errorsByStream: {}, knownChildren: [], checklists: 'not kept in supplier history',
    },
  }};
}
const renderItems = host => renderToStaticMarkup(React.createElement(StoredItemPage, {binding: historyPageBinding(host, 'items')}));
const renderTurns = host => renderToStaticMarkup(React.createElement(StoredTurnPage, {binding: historyPageBinding(host, 'turns'), canRead: true, readItems: () => {throw Error('render must not read');}}));

test('a selected native page reads messages, plans, substantive tool results and delegation in supplier order', () => {
  const host = fixture(), before = clone(host);
  const html = renderItems(host);
  for (const value of ['Stored final &lt;answer&gt;', 'Stored input &lt;script&gt;unsafe()&lt;/script&gt;', 'Stored reasoning summary', 'Stored plan: inspect, then repair', 'Stored command output', 'exit code: 0', '+stored change', 'Stored MCP text', 'Stored resource text', 'Stored App tool text', 'Stored function result', 'agent child: Codex status running', 'unfamiliar item <code>futureNativeKind</code>']) assert.ok(html.includes(value), value);
  assert.ok(html.indexOf('Stored final') < html.indexOf('Stored input'), 'the selected native page order is retained even newest first');
  assert.ok(html.includes('Source home history-home · conversation stored · turn turn-source') && html.includes('Newest first · first page request'));
  assert.ok(html.includes('&quot;factory_id&quot;: 7') && html.includes('&quot;query_id&quot;: 22') && html.includes('&quot;revision&quot;: 2'), 'exact query identity remains in source details');
  assert.ok(html.includes('Original native item page') && html.includes('&quot;entryExtra&quot;: &quot;kept&quot;') && html.includes('&quot;pageExtra&quot;: &quot;preserved page&quot;'));
  assert.ok(html.includes('&quot;unchanged&quot;: true'));
  assert.ok(!html.includes('Must not hydrate this live projection'));
  assert.doesNotMatch(html, /<button|<a |<img|<audio|<script| id="item-/);
  assert.doesNotMatch(html, /Plan<\/b> · revision \d|observed live|wrong-intent-turn/);
  assert.ok(html.includes('not recoverable after restart or relaunch') && html.includes('current execution status is not established'));
  assert.ok(html.includes('Parent completion does not establish descendant return, review or integration'));
  assert.deepEqual(host, before, 'presentation does not alter native page values');
});

test('history state keeps unknown or inProgress outcomes unknown and preserves unavailable results', () => {
  const host = fixture();
  host.nativeHistory.selected.itemsPage.data = [
    entry(item('running', 'commandExecution', {command: 'still running at read', status: 'inProgress', aggregatedOutput: 'partial', exitCode: null})),
    entry(item('image', 'imageGeneration', {status: 'future-valid-native-status'})),
    entry(item('missing', 'mcpToolCall', {tool: 'missing', status: 'completed', result: null, error: null})),
    entry(item('no-status', 'futureNativeKind')),
    entry(item('invalid-status', 'commandExecution', {status: null})),
  ];
  const html = renderItems(host);
  assert.ok(html.includes('unknown — no completion observed'));
  assert.ok(html.includes('native status inProgress') && html.includes('in progress at the read'));
  assert.ok(html.includes('native status future-valid-native-status'));
  assert.equal((html.match(/result not supplied by Codex/g) ?? []).length, 1);
  assert.equal(historyItemRow({type: 'futureNativeKind'}, 'T', 'U').displayState, 'unknown');
  assert.equal(historyItemRow({type: 'imageGeneration', status: 'future-valid-native-status'}, 'T', 'U').displayState, 'unknown');
  assert.equal(historyItemRow({type: 'plan', text: 'p'}, 'T', 'U').displayState, 'completed');
  assert.equal(historyItemRow({type: 'commandExecution', status: null}, 'T', 'U').displayState, 'unknown');
  assert.doesNotMatch(html, /in progress<\/b>|not completed \(turn ended\)|succeeded/);
});

test('read-only reuse cannot inherit live request links, anchors, preview, revision ordinals or controls', () => {
  const native = item('same-item', 'plan', {text: 'History plan text'});
  const row = {threadId: 'stored', turnId: 'turn-source', native, displayState: 'waiting-on-request', standing: 'live-observed', requestRef: {generation, requestIdentity: 4}, preview: 'Leaked live preview'};
  const plans = [{itemId: native.id, turnId: row.turnId, standing: 'live-observed', ordinal: 99}];
  const historical = React.createElement(NativeItemCard, {row, plans, history: true, children: React.createElement('button', null, 'Act now')});
  const live = React.createElement(NativeActivityView, {threadId: 'stored', view: {items: [row], revisions: plans}});
  const html = renderToStaticMarkup(React.createElement(React.Fragment, null, live, historical));
  assert.equal((html.match(/ id="item-/g) ?? []).length, 1, 'concurrent live and stored views have only the live anchor');
  const historyHtml = renderToStaticMarkup(historical);
  assert.ok(historyHtml.includes('History plan text'));
  assert.doesNotMatch(historyHtml, /href=| id=|<button|Leaked live preview|revision 99|request card|Act now/);
});

test('pending, failed, foreign and malformed page sources retain raw evidence without readable rows or pagination authority', () => {
  const cases = [
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].outcome = 'pending';},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].outcome = 'native-error-observed';},
    h => {h.nativeHistory.selected.errorsByStream['item-pages'] = {message: 'unavailable'};},
    h => {h.generation.home = 'other-home';},
    h => {h.generation.appSession = 'other-session';},
    h => {h.generation.spawnCounter++;},
    h => {h.nativeHistory.state = 'observation-ended';},
    h => {h.nativeHistory.home = 'other-home';},
    h => {h.nativeHistory.selectionEpoch = 0;},
    h => {h.nativeHistory.selected.threadId = 'other-thread';},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].query.params.turnId = null;},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].query.params.sortDirection = 'sideways';},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].query.home = 'other-home';},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].query.generation.spawnCounter++;},
    h => {h.nativeHistory.selected.streamResolutions['item-pages'].query.method = 'thread/resume';},
    h => {delete h.nativeHistory.selected.streamResolutions['item-pages'];},
    h => {h.nativeHistory.selected.itemsPage.data = 'malformed';},
  ];
  for (const mutate of cases) {
    const host = fixture(); mutate(host);
    const bound = historyPageBinding(host, 'items');
    assert.equal(bound.accepted, false, mutate.toString());
    assert.equal(bound.page, null, 'unavailable binding exposes no page cursors');
    const html = renderItems(host);
    assert.doesNotMatch(html, /<b>Agent<\/b>|Native item agent ·|<button| id="item-/);
    assert.ok(html.includes('Original native item page') && html.includes('preserved page'), 'raw native page retained');
  }
});

test('malformed entries are isolated, identity mismatches cannot enter a different turn, and unknown nested fields remain safe', () => {
  const host = fixture();
  host.nativeHistory.selected.itemsPage.data = [null, {turnId: 'other-turn', item: item('wrong', 'agentMessage', {text: 'Wrong turn body'})}, {turnId: 'turn-source', item: 'bad-item'}, entry(item('nested', 'fileChange', {status: {odd: true}, changes: [null, {path: {p: 1}, kind: {type: {k: 1}}, diff: {d: 1}}]})), entry(item('valid', 'agentMessage', {text: 'Neighbor still readable'}))];
  const html = renderItems(host);
  assert.equal((html.match(/readable body is withheld/g) ?? []).length, 3);
  assert.ok(html.includes('Neighbor still readable') && html.includes('{&quot;p&quot;:1}'));
  assert.ok(html.includes('native status {&quot;odd&quot;:true}'));
  assert.ok(!html.includes('Native item wrong ·'));
  assert.ok(html.includes('&quot;Wrong turn body&quot;'), 'the mismatched source remains raw');
  assert.ok(html.includes('&quot;item&quot;: &quot;bad-item&quot;'));
});

test('turn summaries distinguish summary, unloaded, full-default, empty and unreported fields without rendering their embedded tool bodies', () => {
  const host = fixture();
  host.nativeHistory.selected.turnsPage.data.push(
    {id: 'unloaded', status: 'inProgress', itemsView: 'notLoaded', items: []},
    {id: 'full-default', status: 'interrupted', items: [], error: {message: 'Native error beside interrupted status'}},
    {id: 'null-view', status: 'unknown-status', itemsView: null, items: []},
    {id: 'missing-items', status: 'failed'},
    {id: null, status: {odd: true}, items: []},
  );
  host.nativeHistory.selected.turnsPage.data[0].items.push(item('embedded-command', 'commandExecution', {command: 'Embedded command is not a selected item body'}));
  const html = renderTurns(host);
  assert.ok(html.includes('Input preview:') && html.includes('Agent preview:'));
  assert.ok(html.includes('Items view: summary · 3 embedded items') && html.includes('Summary items can omit substantive activity'));
  assert.ok(html.includes('Items view: notLoaded · 0 embedded items') && html.includes('Items have not been loaded'));
  assert.ok(html.includes('Items view: full (native default) · 0 embedded items'));
  assert.ok(html.includes('Items view: null (as supplied) · 0 embedded items'), 'native null does not become the default or unreported');
  assert.ok(html.includes('items malformed or not reported') && html.includes('Malformed native turn identity'));
  assert.ok(html.includes('cause not established by this page') && html.includes('Native error beside interrupted status'));
  assert.ok(html.includes('in progress at the read; current outcome unknown'));
  assert.doesNotMatch(html, /<b>Command<\/b>|id="item-/);
  host.nativeHistory.selected.turnsPage.data = [];
  assert.ok(renderTurns(host).includes('empty turn page'));
  host.nativeHistory.selected.itemsPage.data = [];
  assert.ok(renderItems(host).includes('empty item page for turn turn-source'));
  host.nativeHistory.selected.itemsPage = null;
  assert.ok(renderItems(host).includes('This page has not been read'));
});

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {HistoryPanel} = loadSrc('App');
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const buttons = container => container.querySelectorAll(e => e.localName === 'button');
const button = (container, label) => buttons(container).find(e => e.textContent === label);
const click = element => React.act(async () => {await props(element).onClick();});

function continued({source = generation, threadId = 'stored', resumeRequestRef = 'req:resume', state = 'partial'} = {}) {
  const thread = {generation: clone(source), threadId, nativeResumeObserved: true, resumeRequestRef};
  const context = continuationFixture({generation: source, threadId, resumeRequestRef, state, items: nativeItems()});
  const host = fixture();host.generation = clone(source);host.continuationContexts = [context];
  return {host, thread, context};
}
const renderContext = ({host, thread}) => renderToStaticMarkup(React.createElement(ContinuationContext, {host, thread}));

test('admitted continuation renders only its independently accepted bounded prior-work pages', () => {
  const current = continued(), before = clone(current);
  current.host.nativeHistory.selected.threadId = 'browser-other-chat';
  current.host.nativeHistory.selectionEpoch++;
  const html = renderContext(current);
  for (const text of ['Stored final &lt;answer&gt;', 'Stored plan: inspect, then repair', 'Stored command output', 'Stored MCP text']) assert.ok(html.includes(text), text);
  assert.ok(html.includes('admitted resume req:resume') && html.includes('bounded partial snapshot'));
  assert.ok(html.includes('at most 20 turn summaries and 50 items in each page'));
  assert.ok(html.includes('not a complete transcript or a rebuild of live state'));
  assert.ok(html.includes('checklist revisions are not restored') && html.includes('Recovered plans have no live revision number'));
  assert.doesNotMatch(html, /id="item-|href="#request|Must not hydrate this live projection/);
  assert.deepEqual(current.context, before.context, 'render leaves the accepted context untouched');
});

test('prior-work and live views with the same native identity keep a single live anchor and no historical controls', () => {
  const current = continued();
  const native = item('shared-plan', 'plan', {text: 'Same native plan identity'});
  current.context.history.selected.itemsPage.data = [{turnId: 'prior-turn', item: native}];
  const live = React.createElement(NativeActivityView, {threadId: 'stored', view: {items: [{threadId: 'stored', turnId: 'prior-turn', native, standing: 'live-observed', requestRef: {generation, requestIdentity: 4}}], revisions: [{kind: 'plan', itemId: native.id, turnId: 'prior-turn', standing: 'live-observed', ordinal: 99}]}});
  const history = React.createElement(ContinuationContext, {host: current.host, thread: current.thread});
  const combined = renderToStaticMarkup(React.createElement(React.Fragment, null, live, history));
  assert.equal((combined.match(/ id="item-/g) ?? []).length, 1, 'only the live timeline owns an anchor');
  const historical = renderToStaticMarkup(history);
  assert.ok(historical.includes('Same native plan identity'));
  assert.doesNotMatch(historical, / id="item-|href="#request|revision 99|End run|Register|Accept proposal/);
});

test('foreign or incomplete continuation ownership withholds readable pages and controls', () => {
  const changes = [
    c => {c.thread.nativeResumeObserved = false;}, c => {delete c.thread.resumeRequestRef;},
    c => {c.host.state = 'stopped';}, c => {c.host.generation.appSession += '-later';}, c => {c.host.generation.spawnCounter++;}, c => {c.host.generation.home += '-other';},
    c => {c.context.resumeRequestRef += '-other';}, c => {c.context.threadId += '-other';}, c => {c.context.home += '-other';}, c => {c.context.generation.spawnCounter++;},
    c => {c.host.continuationContexts.push(clone(c.context));}, c => {c.context.sourceCurrent = false;}, c => {c.context.admissionSelectionEpoch = 0;}, c => {c.context.revision = 0;},
    c => {c.context.partial = false;}, c => {c.context.fullHistoryRebuilt = true;}, c => {c.context.durableNativeData = true;}, c => {c.context.pageLimits.items = 500;},
    c => {c.context.history.selected.threadId += '-other';}, c => {c.context.history.home += '-other';}, c => {c.context.history.generation.appSession += '-other';}, c => {c.context.state = 'observation-ended';},
  ];
  for (const change of changes) {
    const current = continued();change(current);
    assert.equal(continuationContextBinding(current.host, current.thread).accepted, false, change.toString());
    const html = renderContext(current);
    assert.doesNotMatch(html, /Native item agent ·|<b>Agent<\/b>|<button/, change.toString());
  }
  const current = continued();current.context.history.selected.streamResolutions['item-pages'].query.params.limit = 500;
  assert.equal(continuationPageBinding(current.host, current.thread, 'items').accepted, false);
  assert.ok(renderContext(current).includes('bounded prior-work query limit is not established'));
  const oversized = continued();oversized.context.history.selected.itemsPage.data = Array.from({length: 51}, () => ({turnId: 'prior-turn', item: nativeItems()[0]}));
  assert.equal(continuationPageBinding(oversized.host, oversized.thread, 'items').accepted, false, 'supplier output cannot exceed the presented page bound');
});

test('continuation page acceptance requires the exact original native read receipt', () => {
  for (const change of [
    c => {c.context.receipts = [];}, c => {c.context.receipts[1].sourceCurrent = false;},
    c => {c.context.receipts[1].home += '-other';}, c => {c.context.receipts[1].generation.spawnCounter++;},
    c => {c.context.receipts[1].query = {...c.context.receipts[1].query, query_id: 999};},
    c => {c.context.receipts[1].writeResult = 'write-failed';}, c => {c.context.receipts[1].outcome = 'response-observed-error';},
    c => {delete c.context.receipts[1].requestRef;}, c => {delete c.context.receipts[1].requestIdentity;},
    ...[null, 0, -1, Number.MAX_SAFE_INTEGER + 1].map(position => c => {c.context.receipts[1].receiptPosition = position;}),
  ]) {
    const current = continued();change(current);
    assert.equal(continuationPageBinding(current.host, current.thread, 'items').accepted, false, change.toString());
    assert.doesNotMatch(renderContext(current), /Native item agent ·|<b>Agent<\/b>/);
  }
});

test('queued, partial and unavailable prior work remains separate from resume admission and current activity', () => {
  for (const state of ['queued', 'reading']) {
    const html = renderContext(continued({state}));
    assert.ok(html.includes('Prior work is loading. The conversation is open'));
    assert.doesNotMatch(html, /Native item agent ·|<b>Agent<\/b>/);
  }
  const current = continued();
  current.context.state = 'unavailable';current.context.error = 'Selected item read failed';
  current.context.history.selected.state = 'unavailable';
  current.context.history.selected.streamResolutions['item-pages'].outcome = 'native-error-observed';
  current.context.history.selected.errorsByStream['item-pages'] = {message: 'Selected item read failed'};
  const html = renderContext(current);
  assert.ok(html.includes('Some prior work could not be read') && html.includes('<b>Turn prior-turn</b>'));
  assert.ok(html.includes('Selected item read failed') && html.includes('Retry prior-work read'));
  assert.doesNotMatch(html, /Native item agent ·|<b>Agent<\/b>/);
  assert.equal(current.thread.nativeResumeObserved, true, 'failed context is not a failed resume');
});

test('prior-work controls queue only exact context reads and never drain cursors or resume again', async () => {
  const container = document.createElement('div');document.body.appendChild(container);
  const root = createRoot(container), calls = [];
  let current = continued();
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {calls.push({command, args});return {...current.context, revision: current.context.revision + 1, state: 'queued'};}};
  const show = () => React.act(() => root.render(React.createElement(ContinuationContext, {host: current.host, thread: current.thread})));
  const publish = () => {current.context.revision++;};
  try {
    await show();assert.deepEqual(calls, [], 'mount/render never initiates native reads');
    await click(button(container, 'Read more items'));
    assert.ok(container.textContent.includes('Prior-work read requested'));
    assert.equal(props(button(container, 'Read more items')).disabled, true, 'waits for current host revision, not the returned payload');
    publish();await show();
    await click(button(container, 'Read previous turns page'));
    publish();await show();
    await click(button(container, 'Read items for this turn'));
    publish();current.context.state = 'unavailable';current.context.error = 'Failed native read';await show();
    await click(button(container, 'Retry prior-work read'));
    assert.deepEqual(calls, [
      {command: 'continuation_context_action', args: {generation, threadId: 'stored', resumeRequestRef: 'req:resume', revision: 1, action: 'items', cursor: 'older-items', direction: 'desc', turnId: 'prior-turn'}},
      {command: 'continuation_context_action', args: {generation, threadId: 'stored', resumeRequestRef: 'req:resume', revision: 2, action: 'turns', cursor: 'newer-turns', direction: 'asc', turnId: null}},
      {command: 'continuation_context_action', args: {generation, threadId: 'stored', resumeRequestRef: 'req:resume', revision: 3, action: 'items', cursor: null, direction: 'desc', turnId: 'prior-turn'}},
      {command: 'continuation_context_action', args: {generation, threadId: 'stored', resumeRequestRef: 'req:resume', revision: 4, action: 'retry', cursor: null, direction: 'desc', turnId: null}},
    ]);
    assert.equal(calls.length, 4, 'one native read per click, no follow-up traversal');
  } finally {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}
});

test('late context action failures cannot populate a changed chat, source, resume or newer context revision', async () => {
  for (const replacement of [
    () => continued({threadId: 'new-chat'}),
    () => continued({source: {...generation, home: 'new-home'}}),
    () => continued({source: {...generation, appSession: 'new-session'}}),
    () => continued({source: {...generation, spawnCounter: generation.spawnCounter + 1}}),
    () => continued({resumeRequestRef: 'req:new-resume'}),
    () => {const next = continued();next.context.revision++;return next;},
  ]) {
    const container = document.createElement('div');document.body.appendChild(container);
    const root = createRoot(container);
    let current = continued(), reject, request;
    const held = new Promise((_, fail) => {reject = fail;});
    const previous = window.__TAURI_INTERNALS__;
    window.__TAURI_INTERNALS__ = {invoke: () => held};
    const show = () => React.act(() => root.render(React.createElement(ContinuationContext, {host: current.host, thread: current.thread})));
    try {
      await show();
      await React.act(() => {request = props(button(container, 'Read more items')).onClick();});
      current = replacement();await show();
      await React.act(async () => {reject(Error('Old context action refused'));await held.catch(() => {});await request;});
      assert.ok(!container.textContent.includes('Old context action refused'), replacement.toString());
      assert.equal(props(button(container, 'Read more items')).disabled, false, 'late response cannot disable the new owner');
    } finally {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}
  }
});

test('HistoryPanel pages the exact accepted query turn, cursor and direction, and reading never admits a conversation', async () => {
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container), calls = [], admissions = [];
  let host = fixture();
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {calls.push({command, args}); return host.nativeHistory;}};
  const show = () => React.act(() => root.render(React.createElement(HistoryPanel, {host, refresh: async () => host, threadKey: 'existing-chat', setThreadKey: key => admissions.push(key)})));
  try {
    await show();
    assert.deepEqual(calls, [], 'rendering issues no native reads or resume');
    const next = buttons(container).filter(e => e.textContent === 'Next page');
    const back = buttons(container).filter(e => e.textContent === 'Previous page');
    await click(next[1]); await click(back[1]);
    await click(buttons(container).filter(e => e.textContent === 'Next page')[0]);
    await click(buttons(container).filter(e => e.textContent === 'Previous page')[0]);
    await click(button(container, 'Read items for this turn'));
    assert.deepEqual(calls, [
      {command: 'history_action', args: {generation, selectionEpoch: 3, action: 'items', cursor: 'item-next', direction: 'desc', reference: 'turn-source'}},
      {command: 'history_action', args: {generation, selectionEpoch: 3, action: 'items', cursor: 'item-back', direction: 'asc', reference: 'turn-source'}},
      {command: 'history_action', args: {generation, selectionEpoch: 3, action: 'turns', cursor: 'turn-next', direction: 'asc', reference: null}},
      {command: 'history_action', args: {generation, selectionEpoch: 3, action: 'turns', cursor: 'turn-back', direction: 'desc', reference: null}},
      {command: 'history_action', args: {generation, selectionEpoch: 3, action: 'items', cursor: null, direction: 'desc', reference: 'turn-source'}},
    ]);
    assert.deepEqual(admissions, []);
    assert.equal(buttons(container).filter(e => e.textContent === 'Continue selected conversation').length, 1, 'existing explicit Continue is retained');
  } finally {await React.act(() => root.unmount()); window.__TAURI_INTERNALS__ = previous;}
});

test('HistoryPanel withholds retained-page buttons during pending/error/source changes and replaces views across selection/restart', async () => {
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container), calls = [];
  let host = fixture();
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (...args) => {calls.push(args);}};
  const show = () => React.act(() => root.render(React.createElement(HistoryPanel, {host, refresh: async () => host, threadKey: '', setThreadKey: () => {throw Error('history must not admit');}})));
  const readableItems = () => container.querySelectorAll(e => e.localName === 'small' && e.textContent.startsWith('Native item '));
  try {
    await show(); assert.equal(readableItems().length, nativeItems().length);
    host = clone(host);
    for (const stream of ['turn-pages', 'item-pages']) host.nativeHistory.selected.streamResolutions[stream].outcome = 'pending';
    host.nativeHistory.selected.streamResolutions['item-pages'].query.params.turnId = 'newly-requested-turn';
    await show();
    assert.equal(readableItems().length, 0);
    assert.ok(container.textContent.includes('requested page is pending') && container.textContent.includes('preserved page'));
    assert.ok(!button(container, 'Next page') && !button(container, 'Previous page') && !button(container, 'Read items for this turn'));
    host.nativeHistory.selected.streamResolutions['item-pages'].outcome = 'native-error-observed';
    await show(); assert.equal(readableItems().length, 0); assert.ok(!button(container, 'Next page'));
    host = fixture(); host.generation.spawnCounter++;
    await show(); assert.equal(readableItems().length, 0); assert.ok(!button(container, 'Next page'));
    host = fixture(); host.nativeHistory.selectionEpoch++;
    host.nativeHistory.selected.threadId = 'new-selection';
    await show(); assert.equal(readableItems().length, 0); assert.ok(!button(container, 'Next page'));
    host = fixture();
    host.generation = {...generation, appSession: 'restarted-app', spawnCounter: 1};
    host.nativeHistory.generation = clone(host.generation);
    for (const resolution of Object.values(host.nativeHistory.selected.streamResolutions)) resolution.query.generation = clone(host.generation);
    host.nativeHistory.selected.itemsPage.data = [entry(item('after-restart', 'agentMessage', {text: 'Recovered native page after App restart'}))];
    await show();
    assert.equal(readableItems().length, 1);
    assert.ok(container.textContent.includes('Recovered native page after App restart'));
    assert.ok(!container.textContent.includes('Stored command output'), 'no accumulated prior-page or live projection content');
    assert.deepEqual(calls, [], 'source/selection changes and restart never trigger automatic reads or resume');
  } finally {await React.act(() => root.unmount()); window.__TAURI_INTERNALS__ = previous;}
});
