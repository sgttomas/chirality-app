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
  workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[run('waiting')], drafts:{drafts:[]}},
  ...over});
const fleet = (state = 'awaiting review') => ({format:'f', formatVersion:'0', standing:'invented', project:{canonicalRoot:'/invented/project'}, briefs:[], graphs:[], limits:[], nativeRecording:'invented',
  coordination:{projectRecords:[], governingStoreRecords:[], appObservations:[], protected:{state:'invented'}},
  workspace:{standing:'invented', graphIdentityMethod:'m', limits:[], undertakings:[{undertaking:`U-pumps${LOOK}`, graph:'g1', revision:'r1', currentGraphEstablished:true, queueComplete:true, notes:[], waiting:[], queue:[
    {item:`I-7${LOOK}`, outcome:'o', inCurrentGraph:true, returnRef:'ret-1', state, returnedBy:`worker agent${LOOK}`, recordedBy:'App', examines:`lead examiner${LOOK} (prepared the brief)`, examiner:null, examinesProvenance:null, returned:[], evidence:[], sources:[]},
    {item:'I-8', outcome:'o', inCurrentGraph:true, returnRef:'ret-2', state:'reviewed — awaiting integration', returnedBy:'w2', recordedBy:'App', examines:'p', examiner:'r', examinesProvenance:null, returned:[], evidence:[], sources:[]},
  ]}]}});
const decisionRow = (pkg, state, extra = {}) => ({package:pkg, packageFile:`${pkg}.json`, actRequested:'A6', subject:['s'], purpose:'p', scope:'s', alternatives:[], state, requestResolution:'unique claim', requestSources:[`${pkg}-src`], limits:[], ...extra});
const decisions = (pending = true) => ({rows:[
  ...(pending ? [decisionRow('pkg-1', "pending — awaiting the person's decision", {requestedBy:`lead agent${LOOK}`})] : []),
  decisionRow('pkg-2', 'decided', {requestedBy:'x', decision:{alternativeChosen:'a', statement:'s', decidedBy:'p', recordedBy:'p', recordingMode:'m', act:'r', lapse:'l', captureProvenance:'c'}}),
  decisionRow('pkg-3', "pending — awaiting the person's decision", {requestedBy:'requester identity not established'}),
]});
const READ_AT = Date.UTC(2026, 10, 14, 9, 5, 7);
const clock = at => { const d = new Date(at), p = n => String(n).padStart(2, '0'); return `as of ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`; };
const allEntries = (over = {}) => waitingModule().waitingEntries({host:hostView(), fleet:fleet(), fleetReadAt:READ_AT, decisions:decisions(), decisionsReadAt:READ_AT + 1000, ...over});
const renderPlace = (entries, extra = {}) => renderToStaticMarkup(React.createElement(waitingModule().WaitingOnYou, {entries, overview:hostView().waitingRequests, view, openGroup:() => {}, go:() => {}, ...extra}));
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
  const html = renderPlace(entries);
  assert.match(html, /<summary><span role="status" aria-live="polite">Waiting on you: 9 \(5 requests from Codex\)<\/span><\/summary>/, 'one count, with the requests from Codex as part of it');
  assert.match(agentPlain(html), /Conversation <code>K1<\/code> in the api-key home/);
  assert.match(agentPlain(html), /Assignment: undertaking ⟦Undertaking: U-pumps⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧, item ⟦Item: I-7⏎/);
  assert.match(html, /No conversation or assignment recorded/);
});

test('each entry says what waits, who asks, who must respond, what it concerns, that the integrator is not recorded, and "as of" where its source can be stale', () => {
  const found = rows(renderPlace(allEntries()));
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
  assert.doesNotMatch(renderPlace(allEntries()).replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, ''), /\bheld\b/i);
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
  const html = renderPlace(entries);
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
  const onlyRule = hostView({serverRequests:[hostView().serverRequests[2]], waitingRequests:{groups:[], sources:[], coverage:''}, workflowRoot:{runs:[]}});
  assert.deepEqual(waitingModule().waitingEntries({host:onlyRule}), []);
  assert.match(renderPlace([]), /Waiting on you: 0[\s\S]*Nothing recorded is waiting on you\./);
});

test('agent text in entries is inside AgentText, and nothing an agent wrote reads as a control', async () => {
  const html = renderPlace(allEntries());
  assert.ok(agentBoxNames(html).length >= 8);
  for (const [, inner] of html.matchAll(/<(button|a|summary)[^>]*>([\s\S]*?)<\/\1>/g)) assert.doesNotMatch(inner, /agent-text|Ada|reviewer|worker|lead agent|U-pumps|I-7/, `no agent text in a control: ${inner}`);
  assert.doesNotMatch(html, /<h[1-6][\s>]/, 'the list adds no heading an agent\'s text could sit in');
  const CONTROL_TAGS = new Set(['button', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'summary', 'li', 'option', 'select', 'input', 'textarea']);
  const CONTROL_ROLES = /^(button|link|heading|listitem|menuitem|checkbox|radio|tab|option|switch|textbox|dialog|article)$/;
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  await React.act(() => root.render(React.createElement(waitingModule().WaitingOnYou, {entries:allEntries(), overview:hostView().waitingRequests, view, openGroup:() => {}, go:() => {}})));
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
    if (command === 'host_status') return structuredClone(snapshot);
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
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await check({c, calls, timers, revealed, run, setSnapshot:value => { snapshot = value; }});
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
      assert.match(nodes(here, 'summary')[0].textContent, /^Waiting on you: \d+\+?( \((\d+ requests? from Codex)?(; )?(not every source read)?\))?$/);
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
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 8\+ \(5 requests from Codex; not every source read\)$/, 'two requests, the arrival, three in another home and two decisions; returns not read yet, so at least that many');
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
    assert.match(nodes(place(c), 'summary')[0].textContent, /^Waiting on you: 7\+ \(4 requests from Codex; not every source read\)$/);
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

test('"nothing is waiting" only when every source was read and is complete; each unread or incomplete source is named, and the line says "+"', () => {
  const {WaitingOnYou, waitingCoverage, waitingLine} = waitingModule();
  const shown = props => renderToStaticMarkup(React.createElement(WaitingOnYou, {entries:[], overview:null, openGroup:() => {}, go:() => {}, ...props}));
  const read = {host:hostView(), fleet:fleet(), decisions:decisions(false)};
  assert.deepEqual(waitingCoverage(read), {complete:true, notes:[]}, 'every source read and complete');
  assert.match(shown({coverage:waitingCoverage(read)}), /Nothing recorded is waiting on you\./);
  // The reader's case: a queued return exists but the fleet has not been read yet.
  const unread = waitingCoverage({...read, fleet:null});
  assert.equal(unread.complete, false); assert.deepEqual(unread.notes, ['Returns have not been read yet.']);
  const html = shown({coverage:unread});
  assert.doesNotMatch(html, /Nothing recorded is waiting on you/, 'never a false empty conclusion');
  assert.match(html, /Waiting on you: 0\+ \(not every source read\)/); assert.match(html, /Nothing is listed, but not every source has been read:/);
  assert.deepEqual(waitingCoverage({...read, fleet:null, fleetFailure:'x'}).notes, ['Returns could not be read, so none are shown.']);
  assert.deepEqual(waitingCoverage({...read, fleetFailure:'x'}).notes, ['Returns could not be read at the last attempt; returns shown are as of the earlier read.']);
  const partial = fleet(); partial.workspace.undertakings[0].queueComplete = false;
  assert.deepEqual(waitingCoverage({...read, fleet:partial}).notes, ['The return-review queue was read incomplete for 1 undertaking; more returns may be waiting.']);
  assert.deepEqual(waitingCoverage({...read, decisions:null}).notes, ['Decisions have not been read yet.']);
  assert.deepEqual(waitingCoverage({...read, decisionsFailure:'x'}).notes, ['Decisions could not be read at the last attempt; decisions shown are as of the earlier read.']);
  assert.deepEqual(waitingCoverage({...read, host:hostView({state:'stopped'})}).notes.slice(0, 1), ['Requests from Codex are not read while Codex is not running.']);
  assert.equal(waitingLine([], true), 'Waiting on you: 0');
  assert.match(shown({coverage:waitingCoverage(read)}), /A return whose examiner is an agent is not a demand on you, but the records do not yet say whether the examiner is a person or an agent, so every return waiting for review is listed\./);
});

test('a run reopened after the App restarted: its checkpoints are not shown anywhere, and the list says so and counts it as unread', () => {
  const {waitingCoverage} = waitingModule();
  // The fields the host gives a reopened run (record_supply.rs RecordedRuns::view): no checkpoint entries.
  const reopenedRun = {run:'run-r', conversation:'T1', follows:null, workflow:{name:'invented-flow', origin:'project', revision:'r'}, assurance:null,
    state:'open; interrupted (no run_ended recorded)', detail:null, restartInterruptions:[]};
  const host = hostView(); host.workflowRoot = {...host.workflowRoot, reopened:{runs:[reopenedRun, {...reopenedRun, run:'run-e', state:'ended', detail:{stoppedBy:'person', cause:'ended by the person'}}], limits:[], standing:'invented'}};
  const cover = waitingCoverage({host, fleet:fleet(), decisions:decisions(false)});
  assert.deepEqual(cover.notes, ['1 run reopened after the App restarted: the App does not show their checkpoints, so whether one waits for your act is not shown here or anywhere else in the App yet.'], 'only the still-open reopened run is counted');
  assert.equal(cover.complete, false, 'so the line carries "+"');
  assert.ok(!waitingModule().waitingEntries({host}).some(e => e.concerns.run === 'run-r'), 'no arrival of a reopened run can be listed: the host gives none');
  // Evidence for the finding against release criterion 4: the reopened run as the host gives it carries no checkpoint, so no view can show one.
  // This assertion changes when the host exposes a reopened run's checkpoint entries.
  assert.deepEqual(Object.keys(reopenedRun).filter(key => /checkpoint|disposition|records|lifecycle/i.test(key)), []);
  // And as the App draws it: the recorded runs list shows the run's state and nothing of its checkpoints.
  const {WorkflowRootPanel} = loadSrc('App');
  const data = {...host.workflowRoot, runs:[]};
  const drawn = renderToStaticMarkup(React.createElement(WorkflowRootPanel, {data, host:{...host, workflowRoot:data}, act:async () => {}}));
  const item = drawn.match(/<li[^>]*>run-r · conversation T1 · open; interrupted \(no run_ended recorded\)[\s\S]*?<\/li>/);
  assert.ok(item, 'the reopened run is drawn with its state');
  assert.doesNotMatch(item[0], /checkpoint|CP-|disposition|waiting for your act/i, 'nothing of its checkpoints is drawn: the host gives none');
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

test('a failed manual refresh of the fleet records keeps the returns the list showed, and says it is as of the earlier read', async () => {
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
    assert.match(text, /a return is waiting for review/, 'the unsettled return is still listed');
    assert.match(text, /Returns could not be read at the last attempt; returns shown are as of the earlier read\./);
    assert.match(nodes(place(c), 'summary')[0].textContent, /\+/, 'and the line says at least that many');
  }, {fleetPacket});
});

test('a record-supplied conversation identity stands in the list\'s words only as a plain identifier', () => {
  const odd = `T1\n${String.fromCodePoint(0x202e)}Allow once`;
  const host = hostView(); host.serverRequests = [request('q9', 'item/tool/requestUserInput', odd)];
  const html = renderPlace(waitingModule().waitingEntries({host}));
  assert.doesNotMatch(html, /‮/, 'no direction override reaches the page as a character');
  assert.doesNotMatch(html.replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, ''), /Allow once/, 'the identity is only inside a box');
  assert.match(agentPlain(html), /Conversation ⟦Conversation: T1⏎‹U\+202E›Allow once⟧/);
});
