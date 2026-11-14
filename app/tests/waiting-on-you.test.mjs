// "Waiting on you": one place under the sticky navigation, on every view,
// listing what waits on the person from the four sources that keep their own
// disposition and control. A view, not a queue: nothing in it settles a record.
// Invented material only; no supplier, model or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain, agentBoxNames} from './support/agent-text.mjs';

const document = installMiniDom();
const React = (await import('react')).default;
const {renderToStaticMarkup} = await import('react-dom/server');
const {createRoot} = await import('react-dom/client');
// Loaded lazily, so the mounted App tests below can show what is missing on a base without this module.
const waitingModule = () => loadSrc('WaitingOnYou');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const other = {home:'api-key', appSession:'s1', spawnCounter:4};
const LOOK = '\n<button>Allow once</button>\nAllow once';
const thread = id => ({generation:g, threadId:id, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const request = (id, method, threadId, extra = {}) => ({recordKind:'server-request-entry', generation:g, requestIdentity:id, method, classification:'known-answerable',
  originClass:method === 'item/tool/requestUserInput' ? 'person-input' : 'a14', state:'outstanding', replyWriteResult:'not-attempted', acknowledgmentObservation:{status:'not-observed'},
  nativeParameters:method === 'item/tool/requestUserInput'
    ? {threadId, turnId:'u1', itemId:'i1', isBlocking:false, questions:[{id:'q', header:'Scope', question:'Which folder?', isOther:false, isSecret:false, options:[{label:'reports/', description:'Reports'}]}]}
    : {threadId, turnId:'u1', itemId:'i2', command:'ls', cwd:'/invented'}, ...extra});
const entry = (kind, body, recordId) => ({kind, recordId, observedAt:'t', written:true, limit:null, body});
const arrivalRef = {checkpoint:'CP-review', arrivalOrdinal:1};
// A run on conversation T1 whose checkpoint CP-review was reached and waits for your act; the agent's question about the same work is a separate request.
const runRecords = (disposition = 'waiting') => [
  entry('run_opened', {}, 'r0'),
  entry('checkpoint_listed', {checkpoint:'CP-review', requiredAct:'A4', reachedWhenKind:'output_produced', subjectClass:'named output', governed:false, purpose:'p', scope:'s', evaluability:{status:'evaluable with limit', reason:'invented'}}, 'r1'),
  entry('checkpoint_arrival', {checkpoint:'CP-review', requiredAct:'A4', subjectClass:'named output', governed:false, arrivalOrdinal:1, event:{source:'native_item', ref:'item:T1/u1/m1', evidencedTime:{value:'2026-11-14T10:00:00Z', source:'supplier_item_time'}},
    referents:[], purpose:'p', scope:'s', limits:[], requestObservation:{state:'not yet observed'}}, 'arrival-1'),
  entry('disposition_change', {arrival:arrivalRef, disposition:'waiting', annotations:[]}, 'd1'),
  entry('act_request', {arrival:arrivalRef, form:'person-input request', requester:{kind:`the agent${LOOK}`}, actKind:'A4'}, 'q1'),
  ...(disposition === 'waiting' ? [] : [entry('disposition_change', {arrival:arrivalRef, disposition, annotations:[]}, 'd2')]),
];
const declaration = {reading:'recognized', categories:{checkpoints:'recognized'}, elements:{checkpoints:[{reading:'recognized', value:{name:'CP-review', required_act:'A4', actor:'the_person', subject:{class:'named_output'}, reached_when:{kind:'output_produced', output:'report'}}}]}};
const run = (disposition, over = {}) => ({reference:'run-1', conversation:'T1', home:'account', generation:g, source:'sent', workflow:{name:'invented-flow', origin:'project', revision:'r'},
  lifecycle:{state:"open (live); only the person's explicit end ends it", records:runRecords(disposition)}, compatibility:[{preparation:{declaration}}], status:{}, ...over});
const view = {home:'account', generation:g, items:[], turns:[], turnRecords:[], revisions:[], descendants:[
  {threadId:'C1', parentThreadId:'T1', parentSource:'collabAgentToolCall.senderThreadId', guidance:'not-known', nativeThread:{id:'C1', agentRole:`reviewer${LOOK}`, agentNickname:`Ada${LOOK}`}}]};
const hostView = (over = {}) => ({state:'ready', generation:g, threads:[thread('T1'), thread('T2')], roleLimits:{account:{roles:[]}}, homeRouting:{activeModeHomeClass:'account'}, nativeView:view,
  serverRequests:[
    request('q1', 'item/tool/requestUserInput', 'T1'),
    request('cmd1', 'item/commandExecution/requestApproval', 'C1'),
    // The App answers its own records capability by rule: nothing waits on you.
    {...request('rule1', 'item/tool/call', 'T1'), originClass:'named-service', nativeParameters:{threadId:'T1', turnId:'u1', callId:'c', tool:'chirality_records_read_v1', arguments:{}}},
    // Already answered: settled at its source.
    {...request('done1', 'item/tool/requestUserInput', 'T2'), state:'answered', replyWriteResult:'written'},
  ],
  waitingRequests:{groups:[{modeHomeClass:'account', generation:g, threadId:'T1', count:2}, {modeHomeClass:'api-key', generation:other, threadId:'K1', count:3}], sources:[{modeHomeClass:'account', state:'ready'}, {modeHomeClass:'api-key', state:'ready'}], coverage:'Invented overview.'},
  // An established empty census of runs reopened after a restart (record_supply.rs RunsReading::view with the history notices read_reopened_history attaches).
  workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[run('waiting')], drafts:{drafts:[]}, reopened:emptyCensus()},
  ...over});
function emptyCensus() { return {runs:[], limits:[], historyNotices:[], standing:'invented'}; }
const fleet = (state = 'awaiting review') => ({format:'f', formatVersion:'0', standing:'invented', project:{canonicalRoot:'/invented/project'}, briefs:[], graphs:[], limits:[], nativeRecording:'invented',
  coordination:{project:{source:{path:'fleet/coordination.fleet.jsonl'}, status:'read', complete:true}, projectRecords:[], governingStoreRecords:[], appObservations:[], protected:{state:'invented'}},
  workspace:{standing:'invented', graphIdentityMethod:'m', limits:[], undertakings:[{undertaking:`U-pumps${LOOK}`, graph:'g1', revision:'r1', currentGraphEstablished:true, queueComplete:true, notes:[], waiting:[], queue:[
    {item:`I-7${LOOK}`, outcome:'o', inCurrentGraph:true, returnRef:'ret-1', state, returnedBy:`worker agent${LOOK}`, recordedBy:'App', examines:`lead examiner${LOOK} (prepared the brief)`, examiner:null, examinesProvenance:null, returned:[], evidence:[], sources:[]},
    {item:'I-8', outcome:'o', inCurrentGraph:true, returnRef:'ret-2', state:'reviewed — awaiting integration', returnedBy:'w2', recordedBy:'App', examines:'p', examiner:'r', examinesProvenance:null, returned:[], evidence:[], sources:[]},
  ]}]}});
const decisionRow = (pkg, state, extra = {}) => ({package:pkg, packageFile:`${pkg}.json`, actRequested:'A6', subject:['s'], purpose:'p', scope:'s', alternatives:[], state, requestResolution:'unique claim', requestSources:[`${pkg}-src`], limits:[], ...extra});
const decisions = (pending = true) => ({rows:[
  ...(pending ? [decisionRow('pkg-1', "pending — awaiting the person's decision", {requestedBy:`lead agent${LOOK}`})] : []),
  decisionRow('pkg-2', 'decided', {requestedBy:'x', decision:{alternativeChosen:'a', statement:'s', decidedBy:'p', recordedBy:'p', recordingMode:'m', act:'r', lapse:'l', captureProvenance:'c'}}),
  decisionRow('pkg-3', "pending — awaiting the person's decision", {requestedBy:'requester identity not established'}),
], limits:[], historyNotices:[], unresolvedRecords:[]});
const READ_AT = Date.UTC(2026, 10, 14, 9, 5, 7);
const clock = at => { const d = new Date(at), p = n => String(n).padStart(2, '0'); return `as of ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`; };
const allSources = (over = {}) => ({host:hostView(), hostReadAt:READ_AT - 1000, fleet:fleet(), fleetReadAt:READ_AT, decisions:decisions(), decisionsReadAt:READ_AT + 1000, ...over});
const allEntries = (over = {}) => waitingModule().waitingEntries(allSources(over));
const allReadings = (over = {}) => waitingModule().waitingReadings(allSources(over));
const renderPlace = (readings = allReadings(), extra = {}) => renderToStaticMarkup(React.createElement(waitingModule().WaitingOnYou, {readings, view, openGroup:() => {}, go:() => {}, ...extra}));
const rows = html => [...agentPlain(html).matchAll(/<div class="waiting-on-you-entry" data-waiting-key="[^"]*" data-waiting-source="([^"]*)">([\s\S]*?)<\/div>/g)].map(m => ({source:m[1], text:m[2].replace(/<[^>]+>/g, '')}));

test('the list joins all four sources, one entry per record, grouped by assignment where one exists, otherwise by conversation', () => {
  const entries = allEntries();
  assert.deepEqual(entries.map(e => [e.source, e.kind]), [
    ['supplier-request', 'question'], ['supplier-request', 'tool-permission'],
    ['checkpoint-arrival', 'checkpoint-reached'],
    ['waiting-overview', 'requests-in-another-home'],
    ['return-review', 'return'],
    ['decision-package', 'decision'], ['decision-package', 'decision'],
  ], 'one entry per record; the answered request, the request the App answers by rule, the reviewed return and the decided package are not listed');
  assert.equal(new Set(entries.map(e => e.key)).size, entries.length, 'each entry is keyed by its own record');
  const {waitingGroups, waitingTotal} = waitingModule();
  assert.equal(waitingTotal(entries), 9, 'two requests, one arrival, three requests in another home, one return, two decisions');
  const groups = waitingGroups(entries).map(({group, entries}) => [group.label.kind, group.label.threadId ?? group.label.undertaking ?? null, entries.map(e => e.source)]);
  assert.deepEqual(groups, [
    ['conversation', 'T1', ['supplier-request', 'supplier-request', 'checkpoint-arrival']],
    ['conversation', 'K1', ['waiting-overview']],
    ['assignment', `U-pumps${LOOK}`, ['return-review']],
    ['none', null, ['decision-package', 'decision-package']],
  ], 'the delegated agent\'s request joins the conversation it was delegated from; the return goes under its undertaking and item');
  const html = renderPlace();
  assert.match(html, /<summary><span role="status" aria-live="polite">Waiting on you: 9 \(5 requests from Codex\)<\/span><\/summary>/, 'one count, with the requests from Codex as part of it');
  assert.match(agentPlain(html), /Conversation <code>K1<\/code> in the api-key home/);
  assert.match(agentPlain(html), /Assignment: undertaking ⟦Undertaking: U-pumps⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧, item ⟦Item: I-7⏎/);
  assert.match(html, /No conversation or assignment recorded/);
});

test('each entry says what waits, who asks, who must respond, what it concerns, that the integrator is not recorded, and "as of" where its source can be stale', () => {
  const found = rows(renderPlace());
  const [question, permission, pause, otherHome, ret, decision, unnamed] = found;
  assert.equal(question.text, 'a question is waiting · Asked by the conversation’s own agent · Who must respond: you · Concerns: the conversation T1 · Who integrates the result: not recorded Go to it');
  assert.equal(permission.text, 'a tool permission is waiting · Asked by the delegated agent ⟦Name: Ada⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧, role ⟦Role: reviewer⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧, as Codex reports them · Who must respond: you · Concerns: the conversation C1 · Who integrates the result: not recorded Go to it');
  assert.equal(pause.text, 'a checkpoint was reached; your act is not yet recorded · Asked at the workflow&#x27;s checkpoint ⟦Checkpoint: CP-review⟧; a request for the act was observed from ⟦Requester: the agent⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧ · Who must respond: you · Concerns: the run run-1 in the conversation T1 · Who integrates the result: not recorded Go to it');
  assert.match(otherHome.text, /^questions or tool permissions are waiting in another home \(3\) · Who asked is not established.* · Who must respond: you · Concerns: the conversation K1 · Who integrates the result: not recorded Go to it$/);
  assert.equal(ret.text, `a return is waiting for review · Returned by ⟦Returned by: worker agent⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧ · Who must respond: ⟦Examiner: lead examiner⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧, who prepared the brief, as recorded · Concerns: undertaking ⟦Undertaking: U-pumps⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧, item ⟦Item: I-7⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧ · Who integrates the result: not recorded · ${clock(READ_AT)} Go to it`);
  assert.equal(decision.text, `a decision is waiting · Requested by ⟦Requested by: lead agent⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⟧ · Who must respond: you · Concerns: the decision package ⟦Package: pkg-1⟧ · Who integrates the result: not recorded · ${clock(READ_AT + 1000)} Go to it`);
  assert.match(unnamed.text, /^a decision is waiting · Requested by: not established · /, 'the host\'s own "not established" is the App\'s words, not a requester');
  for (const row of [question, permission, pause]) assert.doesNotMatch(row.text, /as of/, 'requests and run records come with every status read');
  const {WAITING_WORDS} = waitingModule();
  assert.deepEqual(Object.values(WAITING_WORDS).filter(words => /\bheld\b/i.test(words)), [], 'never the word "held"');
  assert.doesNotMatch(renderPlace().replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, ''), /\bheld\b/i);
});

test('the place for a call not answered before Codex stopped is named and drawn, and nothing feeds it', () => {
  const {WAITING_WORDS, WaitingEntryRow} = waitingModule();
  assert.equal(WAITING_WORDS['app-call-unanswered-at-codex-stop'], 'the call was not answered before Codex stopped; it will not be asked again');
  assert.equal(WAITING_WORDS['turn-completed'], 'a turn completed');
  assert.ok(!allEntries().some(e => e.kind === 'app-call-unanswered-at-codex-stop' || e.kind === 'turn-completed'), 'no source records either yet; nothing is made up');
  const shaped = {...allEntries()[0], kind:'app-call-unanswered-at-codex-stop', key:'k'};
  assert.match(renderToStaticMarkup(React.createElement(WaitingEntryRow, {entry:shaped, go:() => {}})), /<strong>the call was not answered before Codex stopped; it will not be asked again<\/strong>/);
});

test('"Go to it" leads to the source\'s own control or record, and the list holds no answer or dismiss control', async () => {
  const entries = allEntries();
  const html = renderPlace();
  const links = [...html.matchAll(/<a href="([^"]*)">Go to it<\/a>/g)].map(m => m[1]);
  const {requestAnchorId} = loadSrc('NativeActivity');
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const {returnReviewAnchor, decisionPackageAnchor} = waitingModule();
  assert.deepEqual(links, [`#${requestAnchorId(g, 'q1')}`, `#${requestAnchorId(g, 'cmd1')}`, `#${runEvidenceAnchor('run-1')}`, '#other-requests', `#${returnReviewAnchor('ret-1')}`, `#${decisionPackageAnchor('pkg-1')}`, `#${decisionPackageAnchor('pkg-3')}`]);
  // The card's own anchor is the same id the card carries.
  const {NativeRequestCard} = loadSrc('RequestCards');
  const card = renderToStaticMarkup(React.createElement(NativeRequestCard, {request:hostView().serverRequests[0], view, answer:async () => {}}));
  assert.ok(card.includes(`id="${requestAnchorId(g, 'q1')}"`));
  // The decision panel's package and the fleet panel's return carry the ids the links name.
  const {DecisionPackagesPanel} = loadSrc('App');
  assert.ok(renderToStaticMarkup(React.createElement(DecisionPackagesPanel, {view:decisions(), name:'', setName:() => {}, recordName:() => {}, refresh:async () => {}, continueRecording:async () => {}, openControl:async () => {}})).includes(`id="${decisionPackageAnchor('pkg-1')}"`));
  const {FleetRecordsPanel} = loadSrc('FleetRecordsPanel');
  assert.ok(renderToStaticMarkup(React.createElement(FleetRecordsPanel, {packet:fleet(), error:'', busy:false, refresh:() => {}})).includes(`id="${returnReviewAnchor('ret-1')}"`));
  // Within the list, every button is the overview's open-the-conversation navigation; nothing answers, dismisses or hides.
  const list = html.split('<section aria-label="Requests waiting for your answer"')[0];
  assert.doesNotMatch(list, /<button|<input|<select|<textarea/, 'no control in the entries but the links');
  assert.deepEqual([...list.matchAll(/<a [^>]*>([^<]*)<\/a>/g)].map(m => m[1]), Array(7).fill('Go to it'), 'the only links are Go to it');
  // Clicking calls the App's navigation with the entry, and nothing else.
  const went = [];
  const {WaitingEntryRow} = waitingModule();
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  await React.act(async () => root.render(React.createElement(WaitingEntryRow, {entry:entries[4], go:e => went.push(e)})));
  {
    const link = container.querySelectorAll(n => n.localName === 'a')[0];
    const props = link[Object.keys(link).find(k => k.startsWith('__reactProps$'))];
    let prevented = false;
    props.onClick({preventDefault:() => { prevented = true; }, stopPropagation:() => {}});
    assert.ok(prevented);
    assert.deepEqual(went.map(e => e.target), [{kind:'return', anchor:returnReviewAnchor('ret-1')}]);
    await React.act(() => root.unmount()); document.body.removeChild(container);
  }
});

test('answering at the source removes the entry: each entry is the source\'s record as read now', () => {
  const before = allEntries();
  const answered = hostView();
  answered.serverRequests = answered.serverRequests.map(r => r.requestIdentity === 'q1' ? {...r, state:'answered', replyWriteResult:'written'} : r);
  answered.workflowRoot.runs = [run('performed')];
  const after = waitingModule().waitingEntries({host:answered, fleet:fleet('reviewed — findings to repair'), fleetReadAt:READ_AT, decisions:decisions(false), decisionsReadAt:READ_AT});
  assert.deepEqual(before.filter(e => !after.some(a => a.key === e.key)).map(e => e.source), ['supplier-request', 'checkpoint-arrival', 'return-review', 'decision-package'], 'each settled record leaves the list');
  assert.deepEqual(after.map(e => e.source), ['supplier-request', 'waiting-overview', 'decision-package'], 'what is still waiting stays');
  // A run that has ended no longer lists its arrival (an act no longer changes it).
  const ended = hostView(); ended.workflowRoot.runs = [run('waiting', {lifecycle:{state:'ended', end:{cause:'ended by the person'}, records:runRecords('waiting')}})];
  assert.ok(!waitingModule().waitingEntries({host:ended}).some(e => e.source === 'checkpoint-arrival'));
  // A newer revision of the same record is a new key: a stale entry cannot stand for it.
  const revised = hostView(); revised.serverRequests = revised.serverRequests.map(r => r.requestIdentity === 'cmd1' ? {...r, generation:{...g, spawnCounter:2}} : r);
  assert.ok(!waitingModule().waitingEntries({host:revised}).some(e => e.target.anchor === before[1].target.anchor), 'a request from a replaced Codex process is not this view\'s record');
});

test('a supplier question and a reserved act on the same subject stay two entries', () => {
  const entries = allEntries().filter(e => e.group.label.threadId === 'T1');
  assert.deepEqual(entries.map(e => WAITING_WORDS_OF(e)), ['a question is waiting', 'a tool permission is waiting', 'a checkpoint was reached; your act is not yet recorded']);
  assert.notEqual(entries[0].key, entries[2].key);
});
const WAITING_WORDS_OF = e => waitingModule().WAITING_WORDS[e.kind];

test('a request waiting on an agent is not listed: the App answers its own records capability by rule', () => {
  const entries = allEntries();
  assert.ok(!entries.some(e => e.target.anchor?.includes?.('rule1')) && !JSON.stringify(entries).includes('rule1'));
  const onlyRule = hostView({serverRequests:[hostView().serverRequests[2]], waitingRequests:{groups:[], sources:[{modeHomeClass:'account', state:'ready'}], coverage:''}, workflowRoot:{runs:[], reopened:emptyCensus()}});
  assert.deepEqual(waitingModule().waitingEntries({host:onlyRule}), []);
  assert.match(renderPlace(allReadings({host:onlyRule, fleet:emptyFleet(), decisions:emptyDecisions()})), /Waiting on you: 0<[\s\S]*Nothing recorded is waiting on you\./);
});

test('agent text in entries is inside AgentText, and nothing an agent wrote reads as a control', async () => {
  const html = renderPlace();
  assert.ok(agentBoxNames(html).length >= 8);
  for (const [, inner] of html.matchAll(/<(button|a|summary)[^>]*>([\s\S]*?)<\/\1>/g)) assert.doesNotMatch(inner, /agent-text|Ada|reviewer|worker|lead agent|U-pumps|I-7/, `no agent text in a control: ${inner}`);
  assert.doesNotMatch(html, /<h[1-6][\s>]/, 'the list adds no heading an agent\'s text could sit in');
  const CONTROL_TAGS = new Set(['button', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'summary', 'li', 'option', 'select', 'input', 'textarea']);
  const CONTROL_ROLES = /^(button|link|heading|listitem|menuitem|checkbox|radio|tab|option|switch|textbox|dialog|article)$/;
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  await React.act(() => root.render(React.createElement(waitingModule().WaitingOnYou, {readings:allReadings(), view, openGroup:() => {}, go:() => {}})));
  for (const el of container.querySelectorAll(() => true)) {
    const role = el.getAttribute?.('role'); if (role) assert.doesNotMatch(role, CONTROL_ROLES, role);
    const name = el.getAttribute?.('aria-label'); if (name) assert.doesNotMatch(name, /Allow once|<button>|Ada|worker|U-pumps/, name);
  }
  const texts = []; const walk = node => { for (const child of node.childNodes) { if (child.nodeType === 3) texts.push(child); else walk(child); } }; walk(container);
  const agentTexts = texts.filter(t => /<button>|Ada|reviewer|worker agent|lead agent|U-pumps|I-7|the agent$/.test(t.nodeValue));
  assert.ok(agentTexts.length >= 8);
  for (const t of agentTexts) {
    let box = null;
    for (let n = t.parentNode; n && n !== container; n = n.parentNode) {
      assert.ok(!CONTROL_TAGS.has(n.localName), `"${t.nodeValue}" is inside a ${n.localName}`);
      if (!box && n.getAttribute('role') === 'group' && /\bagent-text\b/.test(n.getAttribute('class') ?? '')) box = n;
    }
    assert.ok(box, `"${t.nodeValue}" is outside an agent box`);
    assert.match(box.getAttribute('aria-label'), /not the App's words/);
    assert.doesNotMatch(t.nodeValue, /\n/);
  }
  await React.act(() => root.unmount()); document.body.removeChild(container);
});

// ---- The mounted App ----
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
async function mountApp(check, {host = hostView, fleetPacket = fleet, decisionView = decisions} = {}) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  const timers = new Map(); let timer = 0; const revealed = [];
  const previous = {setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval, getElementById:document.getElementById};
  globalThis.setInterval = (fn, ms) => { timers.set(++timer, {fn, ms}); return timer; }; globalThis.clearInterval = id => timers.delete(id);
  document.getElementById = id => { revealed.push(id); return c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null; };
  let snapshot = host();
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    // The status read may be held (a promise the test settles) or rejected (an Error).
    if (command === 'host_status') return snapshot instanceof Error ? Promise.reject(snapshot) : snapshot instanceof Promise ? snapshot.then(v => structuredClone(v)) : structuredClone(snapshot);
    // A source may answer later (a promise the test settles) or fail.
    const reply = value => value instanceof Promise ? value.then(v => structuredClone(v)) : structuredClone(value);
    if (command === 'decision_view') return reply(decisionView());
    if (command === 'read_fleet_records') return reply(fleetPacket());
    if (command === 'native_confirmation_content') return [];
    if (command === 'host_observe') return {sourceUnavailable:true, error:'Invented fixture replays no observer frames', frames:[]};
    if (command === 'open_waiting_requests') return {modeHomeClass:args.modeHomeClass, generation:args.generation, threadId:args.threadId, threadLoaded:true, standing:'invented'};
    assert.fail(`Unexpected IPC: ${command}`);
  });
  const run = async filter => React.act(async () => { for (const {fn, ms} of [...timers.values()]) if (filter(ms)) await fn(); for (let i = 0; i < 8; i++) await Promise.resolve(); });
  // Starts the timers' reads without waiting for their replies (a held status read would otherwise hold the test).
  const fire = async filter => React.act(async () => { for (const {fn, ms} of [...timers.values()]) if (filter(ms)) void fn(); for (let i = 0; i < 8; i++) await Promise.resolve(); });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await check({c, calls, timers, revealed, run, fire, setSnapshot:value => { snapshot = value; }});
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    assert.equal([...timers.values()].length, 0, 'every timer stops on unmount');
    Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById;
  }
}
const {App} = loadSrc('App');
const place = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'Waiting on you')[0];
const shownIn = (el, c) => { for (let n = el; n && n !== c; n = n.parentNode) if (props(n)?.hidden) return false; return true; };

test('the place is present on every view, directly under the navigation, inside the part that stays in view', async () => {
  const {WORKSPACE_VIEWS} = loadSrc('DailyWorkspace');
  await mountApp(async ({c}) => {
    const main = nodes(c, 'main')[0];
    for (const item of WORKSPACE_VIEWS) {
      const link = nodes(c, 'a').find(a => a.textContent === item.label && a.parentNode.localName === 'nav');
      await React.act(async () => props(main).onClick({target:link, currentTarget:main, preventDefault:() => {}}));
      assert.equal(link.getAttribute('aria-current'), 'page', item.label);
      const here = place(c);
      assert.ok(here, `${item.label}: the place is in the document`);
      assert.ok(shownIn(here, c), `${item.label}: the place is shown`);
      assert.match(nodes(here, 'summary')[0].textContent, /^Waiting on you: \d+( observed now)?( \(\d+ requests? from Codex\))?(; status incomplete)?$/);
      const sticky = here.parentNode;
      assert.equal(sticky.getAttribute('class'), 'workspace-sticky', 'it stays in view with the navigation');
      assert.equal(sticky.parentNode, main, 'a direct child of the workspace that holds every view, so it sticks while any of them scrolls');
      assert.equal(sticky.childNodes[0].localName, 'nav'); assert.equal(sticky.childNodes[1], here, 'directly under the navigation');
    }
    assert.equal(c.querySelectorAll(n => n.getAttribute('aria-label') === 'Requests waiting for your answer').length, 1, 'the waiting count is inside the place, once');
    assert.ok(place(c).contains(c.querySelectorAll(n => n.getAttribute('aria-label') === 'Requests waiting for your answer')[0]));
  });
});

test('the decision packages and the returns are read on a timer, the returns also each time the list is opened, the entries show "as of", and the timer stops on unmount', async () => {
  await mountApp(async ({c, calls, timers, run}) => {
    // Before any read of the fleet packet, no return is listed; decisions were read at launch.
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 8 observed now \(5 requests from Codex\); status incomplete$/, 'two requests, the arrival, three in another home and two decisions; returns not read yet, so no definite count');
    const reads = () => calls.filter(call => ['read_fleet_records', 'decision_view'].includes(call.command)).map(call => call.command);
    let before = reads().length;
    const sourceTimers = [...timers.values()].filter(({ms}) => ms > 1000);
    assert.equal(sourceTimers.length, 1, 'one timer of its own, apart from the status poll');
    await run(ms => ms > 1000);
    for (let i = 0; i < 8; i++) await React.act(async () => { await Promise.resolve(); });
    assert.deepEqual(reads().slice(before), ['decision_view', 'read_fleet_records'], 'the timer reads the decision packages through the command their panel calls, and the return queue through the timed-read route (hostReads.ts)');
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 9 \(5 requests from Codex\)$/, 'the return awaiting review is listed without the list being opened');
    // Opening the list reads the return-review queue again.
    before = reads().length;
    const details = c.querySelectorAll(n => n.getAttribute('id') === 'waiting-on-you')[0];
    await React.act(async () => { details.open = true; props(details).onToggle({currentTarget:details}); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.deepEqual(reads().slice(before), ['read_fleet_records']);
    // Closing reads nothing.
    before = reads().length;
    await React.act(async () => { details.open = false; props(details).onToggle({currentTarget:details}); });
    assert.equal(reads().length, before);
    const entriesText = place(c).textContent;
    assert.match(entriesText, /a return is waiting for review.*as of \d\d:\d\d:\d\d/);
    assert.match(entriesText, /a decision is waiting.*as of \d\d:\d\d:\d\d/);
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'read_fleet_records', 'native_confirmation_content', 'host_observe'].includes(call.command)), 'reads only');
  });
});

test('"Go to it" on a request opens its conversation through the existing navigation and lands on its card; answering at the source removes the entry', async () => {
  await mountApp(async ({c, calls, revealed, run, setSnapshot}) => {
    const {requestAnchorId} = loadSrc('NativeActivity');
    const link = nodes(place(c), 'a').find(a => a.getAttribute('href') === `#${requestAnchorId(g, 'q1')}`);
    const before = calls.length;
    await React.act(async () => { props(link).onClick({preventDefault:() => {}, stopPropagation:() => {}}); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.deepEqual(calls.slice(before).map(call => call.command).filter(cmd => !['host_status', 'decision_view'].includes(cmd)), ['open_waiting_requests'], 'the existing navigation, which revalidates the source; nothing answers');
    assert.deepEqual(calls.slice(before).find(call => call.command === 'open_waiting_requests').args, {modeHomeClass:'account', generation:g, threadId:'T1'});
    assert.ok(revealed.includes(requestAnchorId(g, 'q1')), 'it lands on that request\'s card');
    const card = c.querySelectorAll(n => n.getAttribute('id') === requestAnchorId(g, 'q1'))[0];
    assert.ok(card && card.localName === 'article', 'the card, with its own answer controls, is there');
    // The card is answered (the host's register settles it): the next status read removes the entry.
    const answered = hostView(); answered.serverRequests = answered.serverRequests.map(r => r.requestIdentity === 'q1' ? {...r, state:'answered', replyWriteResult:'written'} : r);
    setSnapshot(answered); await run(ms => ms <= 1000);
    assert.ok(!nodes(place(c), 'a').some(a => a.getAttribute('href') === `#${requestAnchorId(g, 'q1')}`), 'the answered request has left the list');
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 7 observed now \(4 requests from Codex\); status incomplete$/);
  });
});

test('"held" is gone from the two notices beside the cards', () => {
  const source = readFileSync(new URL('../src/App.tsx', import.meta.url), 'utf8');
  for (const old of ["Bringing it back there again is held until you've checked.", 'so bringing these results back to it is held too', "Sending to that conversation again is held until you've read it.", 'so sending to it is held too'])
    assert.ok(!source.includes(old), old);
  for (const now of ["The App won't bring it back there again until you've said you checked.", "so the App won't bring these results back to it either until then", "The App won't send to that conversation again until you've said you read it.", "so the App won't send to it either until then"])
    assert.ok(source.includes(now), now);
  // And beside the trial and run controls.
  const make = readFileSync(new URL('../src/MakeJourney.tsx', import.meta.url), 'utf8'), runPanel = readFileSync(new URL('../src/RunPanel.tsx', import.meta.url), 'utf8');
  for (const old of ['"is held until you\'ve checked"', "prepared for this conversation but held"]) assert.ok(!make.includes(old), old);
  assert.ok(make.includes("the App won't bring trial {n} back to it until you've said you checked"));
  assert.ok(make.includes("the App won't send them again yet, and the results line below says why"));
  assert.ok(!runPanel.includes("bringing it back there again is held"));
  assert.ok(runPanel.includes("Read that conversation first; the App won't bring it back there again until you've said you checked."));
});

test('who must respond to a return is who prepared its brief, as recorded, never "you" by default; an arrival is never said to be a pause', () => {
  const {waitingEntries} = waitingModule();
  const returns = packet => waitingEntries({host:hostView(), fleet:packet, fleetReadAt:READ_AT}).filter(e => e.source === 'return-review');
  assert.deepEqual(returns(fleet()).map(e => e.responder), [{kind:'brief-preparer', who:`lead examiner${LOOK}`}]);
  const unmatched = fleet(); unmatched.workspace.undertakings[0].queue[0].examines = 'examiner not established';
  const [row] = returns(unmatched);
  assert.deepEqual(row.responder, {kind:'brief-preparer', who:null});
  const html = renderToStaticMarkup(React.createElement(waitingModule().WaitingEntryRow, {entry:row, go:() => {}}));
  assert.match(html, /Who must respond: not established/);
  assert.doesNotMatch(html, /Who must respond: you/);
  // Nothing feeds the point call's words yet: no source produces "the agent was asked to pause" or "a turn completed".
  const kinds = allEntries().map(e => e.kind);
  assert.ok(!kinds.includes('pause') && !kinds.includes('turn-completed'));
});

// ---- Second round (the reader's findings on 337) ----
const deferred = () => { let resolve, reject; const promise = new Promise((yes, no) => { resolve = yes; reject = no; }); return {promise, resolve, reject}; };

test('decision reads are ordered: an older reply never restores a package a newer read showed decided', async () => {
  const replies = []; let call = 0;
  const decisionView = () => { call++; if (call === 1) return decisions(); const d = deferred(); replies.push(d); return d.promise; };
  await mountApp(async ({c, run}) => {
    const shown = () => place(c).textContent;
    assert.match(shown(), /Package: pkg-1/, 'the pending package is listed after launch');
    await run(ms => ms > 1000);   // read A starts and is held
    await run(ms => ms > 1000);   // read B starts
    assert.equal(replies.length, 2);
    await React.act(async () => { replies[1].resolve(decisions(false)); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.doesNotMatch(shown(), /Package: pkg-1/, 'B shows it decided');
    await React.act(async () => { replies[0].resolve(decisions()); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.doesNotMatch(shown(), /Package: pkg-1/, 'the late reply A does not restore the decided package');
  }, {decisionView});
  // Every path reads the decision view through the one ordered function.
  const source = readFileSync(new URL('../src/App.tsx', import.meta.url), 'utf8');
  assert.equal(source.match(/invoke(<[^>]*>)?\("decision_view"\)/g).length, 1, 'one place reads decision_view');
});

test('a failed manual refresh of the fleet records shows its last successful reading as one block, as last read with its time, and does not count it', async () => {
  let fail = false;
  const fleetPacket = () => fail ? Promise.reject(new Error('invented fleet read failure')) : fleet();
  await mountApp(async ({c, run}) => {
    await run(ms => ms > 1000);   // the timed read lists the return
    assert.match(place(c).textContent, /a return is waiting for review/);
    fail = true;
    const refreshButton = nodes(c, 'button').find(b => b.textContent === 'Refresh fleet records');
    assert.ok(refreshButton, 'the panel\'s own refresh');
    await React.act(async () => { await props(refreshButton).onClick(); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    const text = place(c).textContent;
    const lastRead = c.querySelectorAll(n => n.getAttribute('aria-label') === 'As last read, not counted')[0];
    assert.ok(lastRead && /^Returns, as last read at \d\d:\d\d:\d\d; its current state is unknown, and nothing here is counted above\.[\s\S]*as last read: a return is waiting for review[\s\S]*As last read at \d\d:\d\d:\d\d; current state unknown\. Returns have no review control in the App yet: it shows the return's record\./.test(lastRead.textContent), 'the last successful fleet reading, as it was');
    assert.match(text, /Returns could not be read at the last attempt\. The read started at \d\d:\d\d:\d\d failed\. The last successful response to the returns read, at \d\d:\d\d:\d\d, is shown below as it was then, not counted; its current state is unknown\./);
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 8 observed now \(5 requests from Codex\); status incomplete$/, 'the last-read return is not counted');
  }, {fleetPacket});
});

test('a record-supplied conversation identity stands in the list\'s words only as a plain identifier', () => {
  const odd = `T1\n${String.fromCodePoint(0x202e)}Allow once`;
  const host = hostView(); host.serverRequests = [request('q9', 'item/tool/requestUserInput', odd)];
  const html = renderPlace(waitingModule().waitingReadings({host}));
  assert.doesNotMatch(html, /‮/, 'no direction override reaches the page as a character');
  assert.doesNotMatch(html.replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, ''), /Allow once/, 'the identity is only inside a box');
  assert.match(agentPlain(html), /Conversation ⟦Conversation: T1⏎‹U\+202E›Allow once⟧/);
});

// ---- Every state of every source (the third round: one rule decides each reading) ----
function emptyFleet() { const packet = fleet(); packet.workspace.undertakings = []; return packet; }
function emptyDecisions() { return {rows:[], limits:[], historyNotices:[], unresolvedRecords:[]}; }
// Nothing waits, and every source's reader positively says it was read whole.
const emptyHost = () => hostView({serverRequests:[], waitingRequests:{groups:[], sources:[{modeHomeClass:'account', state:'ready'}, {modeHomeClass:'api-key', state:'ready'}], coverage:'Invented overview.'},
  workflowRoot:{runs:[], reopened:emptyCensus()}});
const emptySources = (over = {}) => ({host:emptyHost(), hostReadAt:READ_AT, fleet:emptyFleet(), fleetReadAt:READ_AT, decisions:emptyDecisions(), decisionsReadAt:READ_AT, ...over});
const reopenedRow = (over = {}) => ({run:'run-r', conversation:'T1', follows:null, workflow:{name:'invented-flow', origin:'project', revision:'r'}, assurance:null,
  state:'open; interrupted (no run_ended recorded)', detail:null, restartInterruptions:[], ...over});
const withHost = edit => { const host = emptyHost(); edit(host); return {host}; };
const withCensus = edit => withHost(host => { edit(host.workflowRoot.reopened); });
const withFleet = edit => { const packet = emptyFleet(); edit(packet); return {fleet:packet}; };
const withDecisions = edit => { const view = emptyDecisions(); edit(view); return {decisions:view}; };
const busy = {reference:'run-1', state:'original run operation pending'};

// [source, case, the change to the established empty reading made through the real input, the reading expected, entries observed in it]
const STATES = [
  ['requests:account', 'Codex not running', withHost(h => { h.state = 'stopped'; }), 'not-read'],
  ['requests:account', 'register not given', withHost(h => { delete h.serverRequests; }), 'not-read'],
  ['requests:account', 'no generation', withHost(h => { delete h.generation; }), 'not-read'],
  // The third reader's finding 5: a generation that is not of the generation's shape is no identity for the register.
  ['requests:account', 'a wrong-type generation', withHost(h => { h.generation = true; }), 'not-read'],
  ['requests:account', 'a generation missing a field', withHost(h => { h.generation = {home:'account', appSession:'s1'}; }), 'not-read'],
  ['requests:account', 'the status read was rejected', {hostFailure:'Chirality could not refresh', hostFailedAt:READ_AT + 5000}, 'failed'],
  ['requests', 'no status read yet', {host:null, hostReadAt:null}, 'not-read'],
  ['other-homes', 'overview not given', withHost(h => { delete h.waitingRequests; }), 'not-read'],
  ['other-homes', 'overview without the active home', withHost(h => { h.waitingRequests.sources = [{modeHomeClass:'api-key', state:'ready'}]; }), 'not-read'],
  ['home:api-key', 'that home not ready', withHost(h => { h.waitingRequests.sources[1].state = 'stopped'; }), 'not-read'],
  ['home:api-key', 'that home with no state', withHost(h => { delete h.waitingRequests.sources[1].state; }), 'not-read'],
  ['hot-runs', 'no workflow root', withHost(h => { delete h.workflowRoot; }), 'not-read'],
  ['hot-runs', 'no run table', withHost(h => { delete h.workflowRoot.runs; }), 'not-read'],
  ['run:run-1', 'read whole: its records', withHost(h => { h.workflowRoot.runs = [run('waiting')]; }), 'whole', 1],
  ['run:run-1', 'busy: the host\'s placeholder', withHost(h => { h.workflowRoot.runs = [busy]; }), 'not-read'],
  ['run:run-1', 'a lifecycle without records', withHost(h => { h.workflowRoot.runs = [run('waiting', {lifecycle:{state:'open (live)'}})]; }), 'not-read'],
  ['reopened', 'not read yet: null', withHost(h => { h.workflowRoot.reopened = null; }), 'not-read'],
  ['reopened', 'not given', withHost(h => { delete h.workflowRoot.reopened; }), 'not-read'],
  ['reopened', 'runs:[] with read limits', withCensus(r => { r.limits = ['WR records unreadable: invented']; }), 'limited'],
  ['reopened', 'a history notice', withCensus(r => { r.historyNotices = ['History notice unavailable: invented; whether project-folder records are omitted is not known.']; }), 'limited'],
  ['reopened', 'limits not given', withCensus(r => { delete r.limits; }), 'limited'],
  ['reopened', 'history notices not given', withCensus(r => { delete r.historyNotices; }), 'limited'],
  ['reopened-run:run-r', 'unknown lifecycle', withCensus(r => { r.runs = [reopenedRow({state:'unknown', detail:'run_opened recorded; the record set is incomplete, so a run_ended may be unreadable'})]; }), 'not-read'],
  ['reopened-run:run-r', 'open, interrupted', withCensus(r => { r.runs = [reopenedRow()]; }), 'not-read'],
  ['reopened-run:run-r', 'a state the App does not know', withCensus(r => { r.runs = [reopenedRow({state:'invented'})]; }), 'not-read'],
  ['reopened-run:run-r', 'ended in its records', withCensus(r => { r.runs = [reopenedRow({state:'ended', detail:{stoppedBy:'person', cause:'c'}})]; }), 'whole'],
  ['reopened-run:run-r', 'start not confirmed in a complete record', withCensus(r => { r.runs = [reopenedRow({state:'start not confirmed in record'})]; }), 'whole'],
  ['reopened-run:run-r', 'the coming host read: records, no limits', withCensus(r => { r.runs = [{reference:'run-r', conversation:'T1', lifecycle:{state:'open; interrupted', end:null, records:runRecords('waiting')}, limits:[]}]; }), 'whole', 1],
  ['reopened-run:run-r', 'the coming host read: records with limits', withCensus(r => { r.runs = [{reference:'run-r', conversation:'T1', lifecycle:{state:'open; interrupted', end:null, records:runRecords('waiting')}, limits:['at most 2,000 records']}]; }), 'limited', 1],
  ['reopened-run:run-r', 'the coming host read: limits not given', withCensus(r => { r.runs = [{reference:'run-r', conversation:'T1', lifecycle:{state:'open; interrupted', end:null, records:runRecords('waiting')}}]; }), 'limited', 1],
  ['returns', 'not read yet', {fleet:null, fleetReadAt:null}, 'not-read'],
  ['returns', 'the read was rejected', {fleetFailure:'invented', fleetFailedAt:READ_AT + 5000}, 'failed'],
  ['returns', 'incomplete discovery: unreadable log, limits, no undertakings', withFleet(p => { p.limits = [{source:{path:'fleet/coordination.fleet.jsonl'}, reason:'source unreadable: invented'}]; p.coordination.project = {status:'unreadable', complete:false}; }), 'limited'],
  ['returns', 'project log not complete', withFleet(p => { p.coordination.project.complete = false; }), 'limited'],
  ['returns', 'project log completeness not given', withFleet(p => { delete p.coordination.project; }), 'limited'],
  ['returns', 'an undertaking\'s queue not complete', withFleet(p => { p.workspace.undertakings = fleet().workspace.undertakings; p.workspace.undertakings[0].queueComplete = false; }), 'limited', 1],
  ['returns', 'no workspace', withFleet(p => { delete p.workspace; }), 'limited'],
  ['returns', 'limits not given', withFleet(p => { delete p.limits; }), 'limited'],
  ['decisions', 'not read yet', {decisions:null, decisionsReadAt:null}, 'not-read'],
  ['decisions', 'the read was rejected', {decisionsFailure:'invented', decisionsFailedAt:READ_AT + 5000}, 'failed'],
  ['decisions', 'incomplete discovery: rows:[] with limits', withDecisions(d => { d.limits = ['records log discovery failed: invented']; }), 'limited'],
  ['decisions', 'a history notice', withDecisions(d => { d.historyNotices = ['invented notice']; }), 'limited'],
  ['decisions', 'an unresolved record', withDecisions(d => { d.unresolvedRecords = [{recordId:'x'}]; }), 'limited'],
  ['decisions', 'a package whose standing is ambiguous', withDecisions(d => { d.rows = [decisionRow('pkg-9', 'ambiguous current standing')]; }), 'limited'],
  ['decisions', 'limits not given', withDecisions(d => { delete d.limits; }), 'limited'],
];

test('the one rule: a reading is whole only on its reader\'s positive word with no limit', () => {
  const {decideReading} = waitingModule();
  for (const call of ['answered', 'rejected', 'not-made']) for (const read of [true, false]) for (const affirmedWhole of [true, false]) for (const limits of [[], ['x']]) {
    const expected = call === 'not-made' ? 'not-read' : call === 'rejected' ? 'failed' : !read ? 'not-read' : affirmedWhole && limits.length === 0 ? 'whole' : 'limited';
    assert.equal(decideReading({call, read, affirmedWhole, limits}), expected, JSON.stringify({call, read, affirmedWhole, limits}));
  }
});

test('every state of every source, through the real adapters: no definite count and no "nothing is waiting" unless every reading is positively whole', () => {
  const {waitingReadings, waitingView, waitingLine, WaitingOnYou} = waitingModule();
  const claims = sources => {
    const readings = waitingReadings(sources);
    const shown = waitingView(readings);
    const html = renderToStaticMarkup(React.createElement(WaitingOnYou, {readings, openGroup:() => {}, go:() => {}}));
    return {readings, shown, line:waitingLine(shown.observed, shown.complete), html};
  };
  // The positive control: an established empty reading of every source (the reader's established empty census among them).
  const base = claims(emptySources());
  assert.deepEqual(base.readings.map(r => [r.key, r.state]), [['requests:account', 'whole'], ['hot-runs', 'whole'], ['other-homes', 'whole'], ['home:api-key', 'whole'], ['reopened', 'whole'], ['returns', 'whole'], ['decisions', 'whole']]);
  assert.equal(base.shown.complete, true);
  assert.equal(base.line, 'Waiting on you: 0');
  assert.match(base.html, /Nothing recorded is waiting on you\./);
  assert.doesNotMatch(base.html, /What this list could not read whole/);
  // Each case removes or invalidates the positive word through the real input; the affirmative claims disappear.
  const sources = new Set();
  for (const [key, name, change, expected, observed = 0] of STATES) {
    sources.add(key.split(':')[0]);
    const {readings, shown, line, html} = claims(emptySources(change));
    const reading = readings.find(r => r.key === key);
    assert.ok(reading, `${key} / ${name}: the reading is there`);
    assert.equal(reading.state, expected, `${key} / ${name}`);
    assert.equal(reading.state === 'whole' || reading.state === 'limited' ? reading.entries.length : 0, observed, `${key} / ${name}: entries observed`);
    if (readings.every(r => r.state === 'whole')) {
      assert.equal(shown.complete, true, `${key} / ${name}: whole everywhere`);
      assert.match(line, /^Waiting on you: \d+( \(\d+ requests? from Codex\))?$/);
      continue;
    }
    assert.equal(shown.complete, false, `${key} / ${name}: not complete`);
    assert.match(line, /^Waiting on you: \d+ observed now( \(\d+ requests? from Codex\))?; status incomplete$/, `${key} / ${name}: ${line}`);
    assert.doesNotMatch(html, /Nothing recorded is waiting on you/, `${key} / ${name}: never "nothing is waiting"`);
    assert.match(html, /status is incomplete:/, `${key} / ${name}`);
    assert.ok(shown.notes.length > 0, `${key} / ${name}: what is not read whole is named`);
    if (reading.state !== 'whole' && !(reading.state === 'not-read' && key.startsWith('reopened-run:'))) assert.ok(shown.notes.includes(reading.note), `${key} / ${name}: its own row names it`);
    if (reading.state === 'failed') assert.deepEqual(reading.entries, [], `${key} / ${name}: a failed reading observes nothing now`);
  }
  assert.deepEqual([...sources].sort(), ['decisions', 'home', 'hot-runs', 'other-homes', 'reopened', 'reopened-run', 'requests', 'returns', 'run'], 'every source is walked');
});

test('the reopened census: an established empty census is whole; null, an unknown lifecycle and runs:[] with limits are not, and the note naming unread reopened runs stays', () => {
  const {waitingReadings, waitingView} = waitingModule();
  const notes = change => waitingView(waitingReadings(emptySources(change))).notes;
  assert.deepEqual(notes({}), []);
  assert.deepEqual(notes(withHost(h => { h.workflowRoot.reopened = null; })), ['Runs recorded before the App restarted have not been read, so whether one of their checkpoints waits for your act is not known. Reopen recorded workflow runs reads them.']);
  assert.deepEqual(notes(withCensus(r => { r.limits = ['WR records unreadable: invented']; })), ['Runs recorded before the App restarted were read with limits: some may not be shown, and whether one of their checkpoints waits for your act is not known.']);
  assert.deepEqual(notes(withCensus(r => { r.runs = [reopenedRow(), reopenedRow({run:'run-u', state:'unknown'}), reopenedRow({run:'run-e', state:'ended'})]; })),
    ['2 runs reopened after the App restarted are not known to have ended: the App does not show their checkpoints, so whether one waits for your act is not shown here or anywhere else in the App yet.'], 'the open and the unknown run are counted; the ended one is not');
  // A reopened run that is also a hot run is covered by the hot run's own reading.
  const both = withHost(h => { h.workflowRoot.runs = [run('waiting', {reference:'run-r'})]; h.workflowRoot.reopened.runs = [reopenedRow()]; });
  assert.deepEqual(notes(both), []);
  // Evidence for the finding against release criterion 4: the reopened run as the host gives it now carries no checkpoint, so no view can show one.
  // This assertion changes when the host exposes a reopened run's checkpoint entries.
  assert.deepEqual(Object.keys(reopenedRow()).filter(key => /checkpoint|disposition|records|lifecycle/i.test(key)), []);
  assert.ok(!waitingModule().waitingEntries(emptySources(withCensus(r => { r.runs = [reopenedRow()]; }))).length, 'no arrival of a reopened run can be listed: the host gives none');
  // And as the App draws it: the recorded runs list shows the run's state and nothing of its checkpoints.
  const {WorkflowRootPanel} = loadSrc('App');
  const host = hostView(); const data = {...host.workflowRoot, runs:[], reopened:{...emptyCensus(), runs:[reopenedRow()]}};
  const drawn = renderToStaticMarkup(React.createElement(WorkflowRootPanel, {data, host:{...host, workflowRoot:data}, act:async () => {}}));
  const item = drawn.match(/<li[^>]*>run-r · conversation T1 · open; interrupted \(no run_ended recorded\)[\s\S]*?<\/li>/);
  assert.ok(item, 'the reopened run is drawn with its state');
  assert.doesNotMatch(item[0], /checkpoint|CP-|disposition|waiting for your act/i, 'nothing of its checkpoints is drawn: the host gives none');
});

test('the list keeps no memory: each reading replaces the one before, and what a limited reading leaves out simply is not shown', () => {
  const {waitingReadings, waitingView} = waitingModule();
  const items = list => list.map(e => e.source + ':' + (e.concerns.package ?? e.concerns.item ?? e.concerns.run ?? e.concerns.threadId));
  const twoReturns = () => { const p = fleet(); p.workspace.undertakings[0].queue[1] = {...p.workspace.undertakings[0].queue[0], item:'I-9', returnRef:'ret-9'}; return p; };
  const first = waitingView(waitingReadings(allSources({fleet:twoReturns(), fleetReadAt:READ_AT})));
  assert.equal(first.complete, true);
  assert.deepEqual(items(first.observed).filter(i => i.startsWith('return')), [`return-review:I-7${LOOK}`, 'return-review:I-9']);
  // A limited fleet read that lists only ret-1, reviewed; a limited decision read that lists only pkg-1, decided.
  const limitedFleet = twoReturns(); limitedFleet.limits = [{source:{}, reason:'invented'}];
  limitedFleet.workspace.undertakings[0].queue = [{...limitedFleet.workspace.undertakings[0].queue[0], state:'reviewed — awaiting integration'}];
  const limitedDecisions = decisions(false); limitedDecisions.limits = ['invented']; limitedDecisions.rows = [decisionRow('pkg-1', 'decided')];
  const next = waitingView(waitingReadings(allSources({fleet:limitedFleet, fleetReadAt:READ_AT + 10000, decisions:limitedDecisions, decisionsReadAt:READ_AT + 10000})));
  assert.equal(next.complete, false);
  assert.deepEqual(items(next.observed).filter(i => /^(return|decision)/.test(i)), [], 'nothing of either source is observed now, and nothing from the earlier reading is carried');
  assert.equal(Object.hasOwn(next, 'lastSeen'), false, 'there is no store of entries seen earlier');
  assert.deepEqual(next.lastReads, [], 'no source failed, so no last-read block');
  assert.deepEqual(next.coverage.map(row => [row.reading.key, row.reading.state]), [['returns', 'limited'], ['decisions', 'limited']], 'each limited source keeps its row');
  // The module offers nothing that folds readings over time.
  const module = waitingModule();
  for (const gone of ['foldWaiting', 'WaitingMemory']) assert.equal(module[gone], undefined, `${gone} is gone`);
  const source = readFileSync(new URL('../src/WaitingOnYou.tsx', import.meta.url), 'utf8');
  for (const gone of ['lastWhole', 'lastSeen', 'settled: string', 'settled: []', 'settled.push', '.settled)', 'useRef', 'WaitingMemory', 'foldWaiting']) assert.ok(!source.includes(gone), `${gone} is gone from the source`);
});

test('a waiting arrival whose run turns busy is not shown while the run is not read; the run keeps its row (the mounted App)', async () => {
  await mountApp(async ({c, run:timers, setSnapshot}) => {
    await timers(ms => ms > 1000);   // the fleet is read
    const line = () => nodes(place(c), 'summary')[0].textContent;
    assert.equal(line(), 'Waiting on you: 9 (5 requests from Codex)');
    // The run's lock is busy: the host gives its placeholder.
    setSnapshot(hostView({workflowRoot:{...hostView().workflowRoot, runs:[busy]}})); await timers(ms => ms <= 1000);
    assert.equal(line(), 'Waiting on you: 8 observed now (5 requests from Codex); status incomplete', 'the arrival is not counted, and the count is not definite');
    assert.doesNotMatch(place(c).textContent, /Nothing recorded is waiting on you/);
    assert.match(place(c).textContent, /The run run-1 could not be read \(an operation on it was in progress\), so whether one of its checkpoints waits for your act is not known\. Checked at \d\d:\d\d:\d\d\./);
    assert.doesNotMatch(place(c).textContent, /a checkpoint was reached/, 'the arrival is not shown: the run\'s reading that showed it has been replaced');
    assert.equal(c.querySelectorAll(n => n.getAttribute('aria-label') === 'As last read, not counted').length, 0, 'not read is not a failed read: no last-read block');
    // The run is read again and its record shows the act performed: the count is definite again.
    setSnapshot(hostView({workflowRoot:{...hostView().workflowRoot, runs:[run('performed')]}})); await timers(ms => ms <= 1000);
    assert.equal(line(), 'Waiting on you: 8 (5 requests from Codex)');
  });
});

const lastReadBlocks = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'As last read, not counted');
const coverageRow = (c, key) => c.querySelectorAll(n => n.getAttribute('data-waiting-source-key') === key && n.localName === 'p')[0];

test('the third reader\'s first finding: after a failed status read, the nested request overview is drawn as last read, never as waiting now (the mounted App)', async () => {
  await mountApp(async ({c, calls, run, fire, setSnapshot}) => {
    await run(ms => ms > 1000);
    const line = () => nodes(place(c), 'summary')[0].textContent;
    assert.equal(line(), 'Waiting on you: 9 (5 requests from Codex)');
    const overviewNow = () => c.querySelectorAll(n => n.getAttribute('aria-label') === 'Requests waiting for your answer')[0];
    assert.match(overviewNow().textContent, /Requests from Codex waiting for your answer/, 'read whole: as now');
    setSnapshot(new Error('invented status failure')); await run(ms => ms <= 1000);
    assert.equal(line(), 'Waiting on you: 3 observed now; status incomplete', 'only the return and the two decisions, read since, are observed now');
    assert.equal(overviewNow(), undefined, 'nothing in the list says requests are waiting for your answer now');
    const past = c.querySelectorAll(n => n.getAttribute('aria-label') === 'Requests from Codex as last read')[0];
    assert.ok(past && place(c).contains(past));
    assert.match(past.textContent, /^Requests from Codex by home and conversation, as last read at \d\d:\d\d:\d\d; the current state is unknown, and these counts may be out of date\./);
    assert.doesNotMatch(past.textContent, /waiting for your answer|current waiting/);
    const buttons = nodes(past, 'button').map(b => b.textContent);
    assert.deepEqual(buttons, ['account · thread T1: 2 at that read', 'api-key · thread K1: 3 at that read'], 'its offers say the counts are from that read');
    assert.match(past.textContent, /At that read: Coverage: Invented overview\./);
    assert.match(past.textContent, /Opening checks that home and conversation again and shows the original home's request cards as they are now/);
    // Its buttons still revalidate on opening, through the existing navigation.
    const before = calls.length;
    await React.act(async () => { props(nodes(past, 'button')[0]).onClick(); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.deepEqual(calls.slice(before).filter(call => call.command === 'open_waiting_requests').map(call => call.args), [{modeHomeClass:'account', generation:g, threadId:'T1'}], 'opening goes through the navigation that checks the source again');
    // The requests themselves are one block, as last read, uncounted, bound to the account home.
    const block = [...lastReadBlocks(c)].find(b => b.getAttribute('data-waiting-source-key') === 'requests:account');
    assert.ok(block, 'the active home\'s requests, as last read');
    assert.match(block.textContent, /^Requests from Codex in the account home, as last read at \d\d:\d\d:\d\d; its current state is unknown, and nothing here is counted above\./);
    assert.match(block.textContent, /as last read: a question is waiting[\s\S]*Its request card takes an answer only while the request is still outstanding\./);
    assert.match(coverageRow(c, 'requests:account').textContent, /^Requests from Codex in the account home could not be read at the last attempt: the App's last read of its own status failed\. The read started at \d\d:\d\d:\d\d failed\. The last successful status response, at \d\d:\d\d:\d\d, is shown below/);
    const runBlock = [...lastReadBlocks(c)].find(b => b.getAttribute('data-waiting-source-key') === 'run:run-1');
    assert.match(runBlock.textContent, /as last read: a checkpoint was reached[\s\S]*It may already be settled: the checkpoint act there does not yet refuse an arrival that is no longer waiting\./);
    const homeBlock = [...lastReadBlocks(c)].find(b => b.getAttribute('data-waiting-source-key') === 'home:api-key');
    assert.match(homeBlock.textContent, /in another home \(3\)[\s\S]*Opening checks that home again/);
    // Order: a read started earlier and answered after a later read failed does not stand over the failure.
    const held = deferred();
    setSnapshot(held.promise); await fire(ms => ms <= 1000);   // read 1 starts and is held
    setSnapshot(new Error('invented status failure')); await run(ms => ms <= 1000);   // read 2 fails
    await React.act(async () => { held.resolve(hostView()); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    assert.match(line(), /status incomplete$/, 'the older reply does not make the status whole');
    // A later read succeeds, with the question answered at its source: the count is definite again, and the overview is current.
    const answered = hostView(); answered.serverRequests = answered.serverRequests.map(r => r.requestIdentity === 'q1' ? {...r, state:'answered', replyWriteResult:'written'} : r);
    setSnapshot(answered); await run(ms => ms <= 1000);
    assert.equal(line(), 'Waiting on you: 8 (4 requests from Codex)');
    assert.equal(lastReadBlocks(c).length, 0);
    assert.ok(overviewNow());
  });
});

test('fleet and decision reads: an older whole reply never replaces a newer failed read (the mounted App)', async () => {
  const fleetReplies = [], decisionReplies = []; let decisionCalls = 0;
  const fleetPacket = () => { const d = deferred(); fleetReplies.push(d); return d.promise; };
  const decisionView = () => { if (++decisionCalls === 1) return decisions(); const d = deferred(); decisionReplies.push(d); return d.promise; };
  await mountApp(async ({c, run}) => {
    const settle = async fn => React.act(async () => { fn(); for (let i = 0; i < 8; i++) await Promise.resolve(); });
    const line = () => nodes(place(c), 'summary')[0].textContent;
    await run(ms => ms > 1000); await settle(() => { fleetReplies[0].resolve(fleet()); decisionReplies[0].resolve(decisions()); });
    assert.equal(line(), 'Waiting on you: 9 (5 requests from Codex)');
    await run(ms => ms > 1000);   // reads A start and are held
    await run(ms => ms > 1000);   // reads B start
    await settle(() => { fleetReplies[2].reject(new Error('invented')); decisionReplies[2].reject(new Error('invented')); });
    assert.equal(line(), 'Waiting on you: 6 observed now (5 requests from Codex); status incomplete');
    await settle(() => { fleetReplies[1].resolve(fleet()); decisionReplies[1].resolve(decisions()); });
    assert.equal(line(), 'Waiting on you: 6 observed now (5 requests from Codex); status incomplete', 'the late whole replies A are not taken');
    assert.match(place(c).textContent, /Returns could not be read at the last attempt\.[\s\S]*Decisions could not be read at the last attempt\./);
  }, {fleetPacket, decisionView});
});

// ---- The third reader's other transitions, under the decided rule: no memory of entries ----
const limitedFleetWith = (rows, over = {}) => { const p = fleet(); p.limits = [{source:{path:'fleet/protected'}, reason:'protected source unavailable: invented'}]; p.workspace.undertakings[0].queueComplete = false; p.workspace.undertakings[0].queue = rows; Object.assign(p, over); return p; };
const unreadableFleet = () => { const p = fleet(); p.limits = [{source:{path:'fleet/coordination.fleet.jsonl'}, reason:'source unreadable: invented'}]; p.coordination.project = {status:'unreadable', complete:false}; p.workspace.undertakings = []; return p; };
const returnsRow = c => coverageRow(c, 'returns');

test('the third reader\'s second finding: a return first seen in a limited reading is counted as observed now, and leaves when the next limited reading does not hold it; the returns row stays and says the reading may omit items (the mounted App)', async () => {
  const packets = [limitedFleetWith([fleet().workspace.undertakings[0].queue[0]]), unreadableFleet()]; let n = 0;
  const fleetPacket = () => packets[Math.min(n++, packets.length - 1)];
  await mountApp(async ({c, run}) => {
    const line = () => nodes(place(c), 'summary')[0].textContent;
    await run(ms => ms > 1000);   // the first, limited, fleet reading
    assert.equal(line(), 'Waiting on you: 9 observed now (5 requests from Codex); status incomplete', 'the return observed in a limited reading is counted as observed now; the count is not definite');
    assert.match(place(c).textContent, /a return is waiting for review/);
    assert.match(returnsRow(c).textContent, /^Returns were read with limits, so more may be waiting for review\. Read at \d\d:\d\d:\d\d with limits: this reading may omit waiting items; what it shows is counted as observed now\. What its reader said it could not read: /);
    assert.match(returnsRow(c).textContent, /protected source unavailable: invented/, 'the reader\'s limit is shown in the row');
    await run(ms => ms > 1000);   // the next limited reading holds no rows
    assert.equal(line(), 'Waiting on you: 8 observed now (5 requests from Codex); status incomplete');
    assert.doesNotMatch(place(c).textContent, /a return is waiting for review/, 'nothing from the earlier reading is kept: the return has dropped from view');
    assert.ok(returnsRow(c), 'the returns row stays when its entries disappear');
    assert.match(returnsRow(c).textContent, /this reading may omit waiting items/);
    assert.equal(lastReadBlocks(c).length, 0, 'a limited reading is not a failed one');
  }, {fleetPacket});
});

test('the third reader\'s third finding: after a change of active home, the old home\'s register is never shown as the new home\'s, and the new home\'s requests are not read until they are (the mounted App)', async () => {
  const switched = (state = 'ready') => hostView({state, generation:state === 'ready' ? other : null, homeRouting:{activeModeHomeClass:'api-key'}, serverRequests:[],
    waitingRequests:{groups:[], sources:[{modeHomeClass:'account', state:'stopped'}, {modeHomeClass:'api-key', state:'ready'}], coverage:'Invented overview.'}});
  await mountApp(async ({c, run, setSnapshot}) => {
    await run(ms => ms > 1000);
    const line = () => nodes(place(c), 'summary')[0].textContent;
    const question = () => /a question is waiting/.test(place(c).textContent);
    assert.ok(question(), 'the account home\'s question, read whole');
    // The api-key home is now active and its Codex is not ready yet: its requests are not read, and account's register is not shown under it.
    setSnapshot(switched('starting')); await run(ms => ms <= 1000);
    assert.ok(!question(), 'the account home\'s question is not relabelled as the api-key home\'s');
    assert.match(coverageRow(c, 'requests:api-key').textContent, /^Requests from Codex in the api-key home are not read while Codex is not running\. Checked at \d\d:\d\d:\d\d\./);
    assert.match(coverageRow(c, 'home:account').textContent, /^Requests in the account home are not read \(stopped\)\./, 'the home left is named as not read');
    assert.match(place(c).textContent, /The overview of requests from Codex by home is not shown: requests from Codex in the api-key home are not read while Codex is not running\./, 'the nested overview is withheld, with the reason');
    assert.match(line(), /observed now.*; status incomplete$/);
    // The api-key home is read whole: empty. Still nothing of account's register.
    setSnapshot(switched()); await run(ms => ms <= 1000);
    assert.ok(!question());
    assert.equal(coverageRow(c, 'requests:api-key'), undefined, 'the api-key home\'s requests are read whole');
    assert.match(line(), /; status incomplete$/, 'the account home is not read, so no definite count');
    // The next status read fails: the retained reading is the api-key home's own, which showed nothing; account's question is never shown relabelled.
    setSnapshot(new Error('invented status failure')); await run(ms => ms <= 1000);
    assert.ok(!question());
    assert.match(coverageRow(c, 'requests:api-key').textContent, /The last successful status response, at \d\d:\d\d:\d\d, showed nothing waiting from it; its current state is unknown\./);
    assert.equal([...lastReadBlocks(c)].filter(b => /^requests/.test(b.getAttribute('data-waiting-source-key'))).length, 0);
    assert.match(c.querySelectorAll(n => n.getAttribute('aria-label') === 'Requests from Codex as last read')[0].textContent, /as last read at \d\d:\d\d:\d\d: no requests were observed then in configured homes; the current state is unknown\.[\s\S]*account: stopped at that read; no groups shown for it\./);
  });
});

test('the third reader\'s fourth finding: a return a limited reading shows reviewed does not come back on the next limited reading (the mounted App)', async () => {
  const reviewed = {...fleet().workspace.undertakings[0].queue[0], state:'reviewed — awaiting integration'};
  const packets = [fleet(), limitedFleetWith([reviewed]), unreadableFleet()]; let n = 0;
  const fleetPacket = () => packets[Math.min(n++, packets.length - 1)];
  await mountApp(async ({c, run}) => {
    const line = () => nodes(place(c), 'summary')[0].textContent;
    const shown = () => /a return is waiting for review/.test(place(c).textContent);
    await run(ms => ms > 1000);
    assert.equal(line(), 'Waiting on you: 9 (5 requests from Codex)'); assert.ok(shown());
    await run(ms => ms > 1000);   // limited: the return is recorded reviewed
    assert.ok(!shown()); assert.equal(line(), 'Waiting on you: 8 observed now (5 requests from Codex); status incomplete');
    await run(ms => ms > 1000);   // limited again, with no rows
    assert.ok(!shown(), 'the reviewed return does not reappear: nothing is carried from an earlier reading');
    assert.equal(lastReadBlocks(c).length, 0);
    assert.equal(line(), 'Waiting on you: 8 observed now (5 requests from Codex); status incomplete');
  }, {fleetPacket});
});

test('the third reader\'s fifth finding: a wrong-type generation makes the requests not read, and no definite count or "nothing is waiting" follows (the mounted App)', async () => {
  const quiet = (generation) => hostView({generation, serverRequests:[request('q1', 'item/tool/requestUserInput', 'T1')], waitingRequests:{groups:[], sources:[{modeHomeClass:'account', state:'ready'}, {modeHomeClass:'api-key', state:'ready'}], coverage:'Invented overview.'},
    workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[], drafts:{drafts:[]}, reopened:emptyCensus()}});
  let generation = g;
  await mountApp(async ({c, run, setSnapshot}) => {
    await run(ms => ms > 1000);
    const line = () => nodes(place(c), 'summary')[0].textContent;
    // The permitted case: a valid generation, every source whole: a definite count with the question in it.
    assert.equal(line(), 'Waiting on you: 1 (1 request from Codex)');
    // The same register with the generation replaced by `true`, through the status read.
    generation = true; setSnapshot(quiet(generation)); await run(ms => ms <= 1000);
    assert.equal(line(), 'Waiting on you: 0 observed now; status incomplete', 'no definite count');
    assert.doesNotMatch(place(c).textContent, /Nothing recorded is waiting on you/);
    assert.match(coverageRow(c, 'requests:account').textContent, /^Requests from Codex in the account home are not read: the App's status gave no register with a generation it can use\./);
  }, {host:() => quiet(generation), fleetPacket:emptyFleet, decisionView:emptyDecisions});
});

test('a failed read whose last successful reading had limits: one block, uncounted, dated, with its limits, and its entries boxed (the mounted App)', async () => {
  const packets = [limitedFleetWith([fleet().workspace.undertakings[0].queue[0]]), new Error('invented fleet read failure')]; let n = 0;
  const fleetPacket = () => { const p = packets[Math.min(n++, packets.length - 1)]; return p instanceof Error ? Promise.reject(p) : p; };
  await mountApp(async ({c, run}) => {
    const line = () => nodes(place(c), 'summary')[0].textContent;
    await run(ms => ms > 1000);
    assert.equal(line(), 'Waiting on you: 9 observed now (5 requests from Codex); status incomplete');
    await run(ms => ms > 1000);   // the read fails
    assert.equal(line(), 'Waiting on you: 8 observed now (5 requests from Codex); status incomplete', 'the last-read return is not counted');
    const [block] = lastReadBlocks(c);
    assert.ok(block && block.getAttribute('data-waiting-source-key') === 'returns');
    assert.match(block.textContent, /^Returns, as last read at \d\d:\d\d:\d\d; its current state is unknown, and nothing here is counted above\. That reading had limits and may have omitted waiting items\./);
    assert.match(returnsRow(c).textContent, /Returns could not be read at the last attempt\. The read started at \d\d:\d\d:\d\d failed\. The last successful response to the returns read, at \d\d:\d\d:\d\d, is shown below as it was then, not counted; its current state is unknown\. That reading had limits and may have omitted waiting items\. What its reader said it could not read: /);
    // What a reader or a record supplied stays inside a box, never in a control.
    for (const el of [block, returnsRow(c)]) for (const control of el.querySelectorAll(n => ['a', 'button', 'li', 'summary'].includes(n.localName)))
      assert.doesNotMatch(control.textContent, /worker agent|U-pumps|protected source/, control.textContent);
    const boxed = returnsRow(c).querySelectorAll(n => n.getAttribute('role') === 'group' && /agent-text/.test(n.getAttribute('class') ?? ''));
    assert.ok(boxed.some(box => /protected source unavailable: invented/.test(box.textContent)), 'the limit is in a box');
  }, {fleetPacket});
});

// ---- The fourth reader's counterexamples ----
const statusBlock = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'The last successful status response')[0];

test('the fourth reader\'s first finding: what is retained is the last successful read of each kind of call; a run that read had not read is named as not read in it, never as having no earlier reading (the mounted App)', async () => {
  await mountApp(async ({c, run, setSnapshot}) => {
    await run(ms => ms > 1000);
    const line = () => nodes(place(c), 'summary')[0].textContent;
    assert.equal(line(), 'Waiting on you: 9 (5 requests from Codex)', 'run-1 read whole, its arrival waiting');
    setSnapshot(hostView({workflowRoot:{...hostView().workflowRoot, runs:[busy]}})); await run(ms => ms <= 1000);   // its lock is taken: the busy placeholder
    setSnapshot(new Error('invented status failure')); await run(ms => ms <= 1000);   // the status poll fails
    assert.match(line(), /; status incomplete$/);
    const row = coverageRow(c, 'run:run-1');
    assert.doesNotMatch(row.textContent, /There is no earlier successful reading of it to show/);
    assert.match(row.textContent, /The read started at \d\d:\d\d:\d\d failed\. The last successful status response, at \d\d:\d\d:\d\d, had not read it\. At that read: The run run-1 could not be read \(an operation on it was in progress\)/);
    const block = statusBlock(c);
    assert.ok(block && place(c).contains(block), 'the last successful status read is shown as one block');
    assert.match(block.textContent, /^The last successful status response, at \d\d:\d\d:\d\d; its current state is unknown, and nothing here is counted above\./);
    assert.match(block.textContent, /Not read in that response: The run run-1\. The run run-1 could not be read \(an operation on it was in progress\)/, 'the run is named as not read in it');
    assert.doesNotMatch(place(c).textContent, /a checkpoint was reached/, 'the arrival of the earlier whole reading is not brought back');
    assert.ok([...lastReadBlocks(c)].some(b => b.getAttribute('data-waiting-source-key') === 'requests:account' && block.contains(b)), 'its requests, as last read, inside it');
  });
});

test('the fourth reader\'s second finding: each unread reopened run is named, with its reason, under the aggregate line; with no readAt only the carrying status response is dated', () => {
  const change = withCensus(r => { r.runs = [reopenedRow({run:'missing-run-alpha'}), reopenedRow({run:'missing-run-beta', state:'unknown', detail:'invented'}), reopenedRow({run:`odd run${LOOK}`, state:'invented'})]; });
  const readings = waitingModule().waitingReadings(emptySources({...change, hostReadAt:READ_AT}));
  const html = renderPlace(readings);
  const time = clock(READ_AT).slice('as of '.length);
  const text = agentPlain(html).replace(/<[^>]+>/g, '');
  assert.match(text, /3 runs reopened after the App restarted are not known to have ended: the App does not show their checkpoints/, 'the aggregate line is read first');
  assert.ok(text.indexOf('3 runs reopened') < text.indexOf('missing-run-alpha'));
  const disclosure = html.match(/<details class="waiting-reopened-runs">[\s\S]*?<\/details>/);
  assert.ok(disclosure, 'the runs are in a disclosure under the line');
  const listed = agentPlain(disclosure[0]).replace(/<[^>]+>/g, '');
  assert.match(listed, new RegExp(`The run missing-run-alpha: its records show it opened and record no end\\. Carried in the status response read at ${time}\\. When the records were last read for it is not given\\.`));
  assert.match(listed, new RegExp(`The run missing-run-beta: its records do not establish whether it ended\\. Carried in the status response read at ${time}\\. When the records were last read for it is not given\\.`));
  assert.match(listed, new RegExp(`The run ⟦Run: odd run[\\s\\S]*?⟧: its state is one the App does not recognise\\. Carried in the status response read at ${time}\\. When the records were last read for it is not given\\.`));
  assert.doesNotMatch(listed, /Read at|checkpoints were read|census at|records were last read for it at/, 'the status response\'s time is never presented as when the records were read');
  assert.ok(agentBoxNames(disclosure[0]).length > 0, 'a reference that is not a plain identifier is boxed');
  assert.doesNotMatch(html.replace(/<span class="agent-text[\s\S]*?<\/span><\/span>/g, ''), /<button>Allow once<\/button>/);
});

test('a reopened run is dated by the records read only where the reopened view states readAt, strictly RFC 3339 UTC; never by the status response that carries it', () => {
  const recordsAt = '2026-11-14T08:15:30Z';
  const recordsMs = Date.parse(recordsAt);
  assert.notEqual(clock(recordsMs), clock(READ_AT), 'the two times differ, so the test tells them apart');
  const listedFor = readAt => {
    const change = withCensus(r => { r.runs = [reopenedRow({run:'missing-run-alpha'})]; if (readAt !== undefined) r.readAt = readAt; });
    const html = renderPlace(waitingModule().waitingReadings(emptySources({...change, hostReadAt:READ_AT})));
    return agentPlain(html).replace(/<[^>]+>/g, '');
  };
  const statusTime = clock(READ_AT).slice('as of '.length);
  const recordsTime = clock(recordsMs).slice('as of '.length);
  const valid = listedFor(recordsAt);
  assert.match(valid, new RegExp(`The run missing-run-alpha: its records show it opened and record no end\\. The records were last read for it at ${recordsTime}\\.`));
  assert.ok(!valid.includes(`at ${statusTime}.`) || statusTime === recordsTime, 'the status response time is not given as the records time');
  assert.doesNotMatch(valid, /Carried in the status response/);
  for (const [why, readAt] of [['removed', undefined], ['an offset, not UTC', '2026-11-14T08:15:30+00:00'], ['a date that does not exist', '2026-02-30T08:15:30Z'], ['no seconds', '2026-11-14T08:15Z'], ['a number', recordsMs], ['trailing text', recordsAt + ' ']]) {
    const listed = listedFor(readAt);
    assert.match(listed, new RegExp(`Carried in the status response read at ${statusTime}\\. When the records were last read for it is not given\\.`), why);
    assert.doesNotMatch(listed, /records were last read for it at|census at/, why);
  }
  const {hostUtcTime} = waitingModule();
  assert.equal(hostUtcTime('2026-11-14T08:15:30.123456789Z'), Date.parse('2026-11-14T08:15:30.123Z'), 'a fraction is accepted');
});

test('the fourth reader\'s third finding: another home\'s group whose generation is not of the generation\'s shape makes that home not read and gives no count', () => {
  const {waitingReadings, waitingView, waitingLine} = waitingModule();
  const change = withHost(h => { h.waitingRequests.groups = [{modeHomeClass:'api-key', generation:true, threadId:'K1', count:2}]; });
  const readings = waitingReadings(emptySources(change));
  assert.equal(readings.find(r => r.key === 'home:api-key').state, 'not-read');
  const shown = waitingView(readings);
  assert.equal(shown.observed.length, 0, 'the malformed group contributes nothing');
  assert.equal(waitingLine(shown.observed, shown.complete), 'Waiting on you: 0 observed now; status incomplete');
  assert.ok(shown.notes.includes('Requests in the api-key home are not read: the overview gave a group without a generation the App can use.'));
  // The positive control: the same group with a generation of the shape is counted, and the count is definite.
  const good = waitingView(waitingReadings(emptySources(withHost(h => { h.waitingRequests.groups = [{modeHomeClass:'api-key', generation:other, threadId:'K1', count:2}]; }))));
  assert.equal(waitingLine(good.observed, good.complete), 'Waiting on you: 2 (2 requests from Codex)');
});
