// The presentation boundary on the three covered views (RequestCards, NativeActivity, NativeHistory): every value
// from Codex, an agent or a record reaches the page only through an approved presentation (AgentText, SuppliedId,
// Word, Num, Flag, or the functions plainId, idWords, wordOf, numberWords, isoSeconds), and a control or heading
// holds only the App's words. Two kinds of evidence: the guard's verdict on the source, and the rendered page with
// every supplied string poisoned. Invented material only.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';
import {guardFailures, sourceFailures, wordTableFailures, GUARDED_VIEWS} from './support/presentation-guard.mjs';

const SRC = new URL('../src/', import.meta.url);
const exceptions = JSON.parse(readFileSync(new URL('./support/presentation-guard-exceptions.json', import.meta.url), 'utf8'));

test('presentation guard: every drawn expression on the four covered views takes an approved form, and each listed exception gives its reason', () => {
  assert.deepEqual([...GUARDED_VIEWS].sort(), ['NativeActivity.tsx', 'NativeHistory.tsx', 'RequestCards.tsx', 'RunOffers.tsx']);
  assert.deepEqual(guardFailures(SRC, exceptions), []);
  assert.deepEqual(wordTableFailures(SRC), [], 'the vocabulary module holds only tables of literal words');
  for (const e of exceptions) assert.ok(typeof e.reason === 'string' && e.reason.length > 40, `${e.file} ${e.expr}: a reason that says why`);
});

// The guard on invented views: each attempt to bypass the boundary fails; the approved forms pass.
const judge = (source, name = 'Invented.tsx', listed = []) => sourceFailures(name, source, listed).failures;
const fails = (source, why, name) => assert.notDeepEqual(judge(source, name), [], why);
const passes = (source, why, name) => assert.deepEqual(judge(source, name), [], why);
const IMPORTS = 'import { AgentText, SuppliedId, Word, Num, Flag, idWords, plainId, wordOf, numberWords } from "./AgentText";\n';

test('presentation guard: each bypass attempt fails, and only a written-down trusted presentation passes a supplied value', () => {
  // The positive control: a supplied value through each approved presentation, and the App's own forms.
  passes(IMPORTS + `const T = { a: "the App's word" } as const;
    export function V({ row }: { row: any }) { return <div><p>Literal {row.count > 1 ? "many" : "one"}</p><SuppliedId value={row.id} /> <Word value={row.kind} words={T} />
      <Num value={row.n} /> <Flag value={row.ok} yes="yes" no="no" /> <AgentText value={row.text} source="codex" />{idWords(row.id)} {wordOf(T, row.kind) ?? "unknown"} {numberWords(row.n)}
      {[1, 2].map((x, i) => <span key={i}>{i + 1}</span>)}<button>{"Read"}</button></div>; }`, 'the approved presentations pass');
  // A supplied value drawn directly, in a sentence, a heading, a button, a link or an attribute.
  fails('export const V = ({ row }: any) => <p>About {row.title}</p>;', 'a supplied value in a sentence');
  fails('export const V = ({ row }: any) => <h3>{`Request ${row.method}`}</h3>;', 'a supplied value in a heading');
  fails('export const V = ({ row }: any) => <div title={row.title} />;', 'a supplied value as a title');
  fails('export const V = ({ row }: any) => <div aria-label={`Run ${row.name}`} />;', 'a supplied value as an accessible name');
  fails('export const V = ({ row }: any) => <p aria-describedby={row.id} />;', 'a supplied value naming a description');
  fails('export const V = ({ row }: any) => <p>{JSON.stringify(row)}</p>;', 'raw JSON drawn as text');
  fails('export const V = ({ row }: any) => <p>{row.length}</p>;', "a supplied object's length field is not a count");
  // A trusted helper's name is not enough: a same-file function returning raw text, a local or renamed "idWords".
  fails('function show(v: any) { return v; }\nexport const V = ({ row }: any) => <p>{show(row.title)}</p>;', 'a helper that returns raw text');
  fails('const idWords = (v: any) => v;\nexport const V = ({ row }: any) => <p>{idWords(row.title)}</p>;', 'a local function named idWords');
  fails('import { text as idWords } from "./AgentText";\nexport const V = ({ row }: any) => <p>{idWords(row.title)}</p>;', 'another function imported as idWords');
  fails('import { idWords } from "./elsewhere";\nexport const V = ({ row }: any) => <p>{idWords(row.title)}</p>;', 'idWords from another module');
  // A child component that draws a supplied prop: exported, or passed one by a caller in this file.
  fails('export function Name({ value }: { value: any }) { return <b>{value}</b>; }', 'an exported component drawing its prop');
  fails('function Name({ value }: { value: string }) { return <b>{value}</b>; }\nexport const V = ({ row }: any) => <Name value={row.title} />;', 'an unexported component passed a supplied value');
  passes('function Name({ value }: { value: string }) { return <b>{value}</b>; }\nexport const V = () => <Name value="the App\'s words" />;', 'an unexported component passed only literals');
  fails('import { Pretty } from "./Pretty";\nexport const V = ({ row }: any) => <Pretty value={row.title} />;', 'a component from outside the boundary, unlisted');
  // An approved presentation's own words must be the App's; its word table must be the App's.
  fails(IMPORTS + 'export const V = ({ row }: any) => <AgentText value={row.text} label={row.title} />;', "a box labelled with supplied text");
  fails(IMPORTS + 'export const V = ({ row }: any) => <Word value={row.kind} words={row.table} />;', 'a supplied word table');
  fails(IMPORTS + 'export const V = ({ row }: any) => { const T = { a: row.word }; return <p>{wordOf(T, row.kind)}</p>; };', 'a table holding a supplied word');
  // Inside a control or a heading, even a box is not allowed.
  fails(IMPORTS + 'export const V = ({ row }: any) => <button>Use <AgentText value={row.name} /></button>;', 'a box inside a button');
  fails(IMPORTS + 'export const V = ({ row }: any) => <summary>Item <SuppliedId value={row.id} /></summary>;', 'an identity presentation inside a summary');
  // Spreads, raw HTML and writes to the page outside React.
  fails('export const V = ({ row }: any) => <div {...{ title: row.title }} />;', 'a spread carrying a supplied title');
  fails('export const V = ({ row }: any) => <div dangerouslySetInnerHTML={{ __html: row.html }} />;', 'raw HTML');
  fails('export function V({ row }: any) { const el = document.getElementById("x")!; el.textContent = row.text; return null; }', 'assigning DOM text');
  fails('export function V({ row }: any) { const r = { current: null as any }; r.current.innerHTML = row.text; return null; }', 'assigning HTML through a ref');
  fails('export function V({ row }: any) { document.body.insertAdjacentHTML("beforeend", row.text); return null; }', 'inserting HTML');
  fails('export function V({ row }: any) { (document as any)["innerHTML"] = row.text; return null; }', 'assigning HTML by name');
  // A text field holds only what the person types: finding 1's form fails, the repaired form passes.
  const field = choose => `import { useState } from "react";
    export function V({ options }: any) { const [draft, setDraft] = useState(""); return <div>{options.map((o: any, i: number) => <button key={i} onClick={() => ${choose}}>Choose option {i + 1}</button>)}
      <input value={draft} onChange={e => setDraft(e.target.value)} /></div>; }`;
  fails(field('setDraft(o.label)'), "choosing an option writes the agent's label into the person's field");
  passes(field('setDraft("")'), 'a field cleared or typed into holds only the App\'s or the person\'s text');
  // A listed exception passes only its exact expression, and a listed exception that no longer fails is stale.
  const listed = [{file: 'Invented.tsx', where: 'drawn', expr: 'row.notice', reason: 'invented'}];
  assert.deepEqual(judge('export const V = ({ row }: any) => <p>{row.notice}</p>;', 'Invented.tsx', listed), []);
  assert.notDeepEqual(judge('export const V = ({ row }: any) => <p>{row.other}</p>;', 'Invented.tsx', listed), []);
  assert.deepEqual(sourceFailures('Invented.tsx', 'export const V = () => <p>words</p>;', listed).used.size, 0, 'an unused listing is not used, and guardFailures reports it stale');
});

// The third reading's bypasses (review of PR 336, round 3), each closed by one rule of the guard.
test('presentation guard closure: attribute contents are judged as children are (a children attribute, a ref callback, a function in an attribute)', () => {
  const wrap = 'function Wrap({ children }: any) { return <div>{children}</div>; }\n';
  fails(wrap + 'export const V = ({ row }: any) => <Wrap children={<button>{row.text}</button>} />;', 'an element with supplied text in a children attribute');
  fails(wrap + 'export const V = ({ row }: any) => <Wrap children={row.text} />;', 'a supplied value as a children attribute');
  fails('export const V = ({ row }: any) => <p ref={el => { if (el) el.textContent = row.text; }} />;', 'a ref callback writing DOM text');
  fails('export const V = ({ row }: any) => <button onClick={() => { document.body.insertAdjacentHTML("beforeend", row.text); }}>Go</button>;', 'an event handler inserting HTML');
  fails('import { List } from "./List";\nexport const V = ({ rows }: any) => <List render={(r: any) => <b>{r.text}</b>} />;', 'supplied text in an element a render prop returns');
  passes(wrap + 'export const V = () => <Wrap children={<b>The App\'s words</b>} />;', 'an element of the App\'s words in a children attribute');
});
test('presentation guard closure: a spread of attributes carries only listed keys, never raw HTML', () => {
  const raw = 'export const V = ({ row }: any) => <div {...{ dangerouslySetInnerHTML: { __html: row.text } }} />;';
  fails(raw, 'raw HTML in a spread');
  assert.notDeepEqual(judge(raw, 'Invented.tsx', [{file: 'Invented.tsx', where: '{...}', expr: '{ dangerouslySetInnerHTML: { __html: row.text } }', reason: 'invented'}]), [], 'raw HTML in a spread cannot be listed');
  fails('export const V = ({ row }: any) => <div {...(row.on ? { title: "App" } : { dangerouslySetInnerHTML: { __html: row.text } })} />;', 'raw HTML in one branch of a spread');
  fails('export const V = ({ row }: any) => <div {...{ children: row.text }} />;', 'children in a spread');
  fails('import { Pretty } from "./Pretty";\nexport const V = ({ row }: any) => <div {...{ children: <Pretty value={row.text} /> }} />;', 'an outside component hidden in a spread\'s children');
  fails('export const V = () => <div {...{ onClick: () => {} }} />;', 'a key not on the list');
  passes('export const V = () => <div {...{ id: "x", className: "c", title: "The App\'s words" }} />;', 'listed keys with the App\'s values');
});
test('presentation guard closure: a control or heading role holds only the App\'s words, as the tags do', () => {
  fails(IMPORTS + 'export const V = ({ row }: any) => <div role="heading"><AgentText value={row.text} /></div>;', 'a box inside role=heading');
  fails(IMPORTS + 'export const V = ({ row }: any) => <span role="button"><SuppliedId value={row.id} /></span>;', 'an identity presentation inside role=button');
  fails(IMPORTS + 'export const V = ({ row, h }: any) => <div role={h ? "heading" : "note"}><AgentText value={row.text} /></div>;', 'a box inside a role that may be a heading');
  fails('export const V = ({ row }: any) => <div role={row.role}>words</div>;', 'a role not built of literals');
  passes(IMPORTS + 'export const V = ({ row, a }: any) => <div role={a ? "alert" : "status"}><AgentText value={row.text} /></div>;', 'a box inside a status');
});
test('presentation guard closure: a naming or describing reference names only a literal id of an App-only element in the same file', () => {
  fails(IMPORTS + 'export const V = ({ row }: any) => <div><span ref={el => { const v = el?.querySelector(".agent-text-value"); if (v) v.id = "supplied"; }}><AgentText value={row.text} /></span><button aria-labelledby="supplied">App</button></div>;',
    'labelledby a value span given an id through a ref');
  fails(IMPORTS + 'export const V = ({ row }: any) => <div><span id="w"><AgentText value={row.text} /></span><button aria-describedby="w">App</button></div>;', 'describedby a wrapper around a box');
  fails('export const V = ({ row }: any) => <div><button aria-labelledby={`x-${row.id}`}>App</button></div>;', 'a reference that is not a literal');
  fails('export const V = () => <div><button aria-labelledby="nowhere">App</button></div>;', 'a reference naming no element in this file');
  fails('export const V = () => <div><span id="n">One</span><span id="n">Two</span><button aria-labelledby="n">Go</button></div>;', 'a reference naming two elements');
  passes('export const V = () => <div><span id="n">The App\'s words</span><button aria-labelledby="n" aria-describedby="n">Go</button></div>;', 'a reference to an App-only element');
});
test('presentation guard closure: a trusted name is trusted only when it is bound to the import from the trusted module', () => {
  fails(IMPORTS + 'function Probe({ row }: any) { const idWords = (x: any) => x; return <p>{idWords(row.text)}</p>; }\nexport const V = () => <Probe row={1} />;', 'a local shadowing the imported idWords');
  fails(IMPORTS + 'export function V({ row, idWords }: any) { return <p>{idWords(row.text)}</p>; }', 'a parameter shadowing the imported idWords');
  fails(IMPORTS + 'export function V({ row }: any) { const AgentText = ({ value }: any) => <b>{value}</b>; return <AgentText value={row.text} />; }', 'a local component shadowing AgentText');
  fails('import { CHANGE_KIND } from "./nativeWords";\nimport { wordOf } from "./AgentText";\nexport function V({ row, CHANGE_KIND: T }: any) { const CHANGE_KIND = row.table; return <p>{wordOf(CHANGE_KIND, row.kind)}</p>; }', 'a local shadowing an imported word table');
  passes(IMPORTS + 'export const V = ({ row }: any) => <p>{idWords(row.id)}</p>;', 'the imported idWords');
  passes('import { clockWords } from "./AgentText";\nexport const V = ({ at }: any) => <p>{clockWords(at)}</p>;', 'clockWords, an approved presentation');
});

// The rendered page: every supplied string poisoned with a marker and a direction override. Outside the boxes, and
// in every control, heading and attribute that names or holds text, the marker never appears.
const MARK = 'UNTRUSTED';
const RLO = '‮';
const poison = (value, keep = new Set()) => {
  if (typeof value === 'string') return `${MARK}${RLO}${value}`;
  if (Array.isArray(value)) return value.map(v => poison(v, keep));
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, keep.has(k) ? v : poison(v, keep)]));
  return value;
};
/** The page with every box read as ⟦label value⟧ and then removed: what remains is the App's own words. */
const outsideBoxes = raw => agentPlain(raw).replace(/⟦[^⟧]*⟧/g, '');
const APP_ONLY_ELEMENTS = /<(button|a|summary|label|legend|option|h[1-6])\b[^>]*>([\s\S]*?)<\/\1>/g;
const NAMING_ATTRIBUTES = /\s(aria-[a-z]+|title|alt|placeholder|value)="([^"]*)"/g;
function assertBoundary(raw, what) {
  const outside = outsideBoxes(raw);
  assert.ok(!outside.includes(MARK), `${what}: supplied text outside a box: …${outside.slice(Math.max(0, outside.indexOf(MARK) - 160), outside.indexOf(MARK) + 80)}…`);
  assert.ok(!outside.includes(RLO), `${what}: a direction override outside a box`);
  for (const [, tag, inner] of raw.matchAll(APP_ONLY_ELEMENTS)) {
    assert.ok(!inner.includes(MARK), `${what}: supplied text inside a ${tag}: ${inner.slice(0, 200)}`);
    assert.ok(!/agent-text/.test(inner), `${what}: a box inside a ${tag}: ${inner.slice(0, 200)}`);
  }
  for (const [, name, value] of raw.matchAll(NAMING_ATTRIBUTES)) assert.ok(!value.includes(MARK) && !value.includes(RLO), `${what}: supplied text in ${name}="${value.slice(0, 120)}"`);
}

const {NativeRequestCard, WaitingRequestsIndicator} = loadSrc('RequestCards');
const {NativeActivityView, RunStartMarker, RunEndMarker, RunLabel, StopLabel} = loadSrc('NativeActivity');
const {StoredTurnPage, StoredItemPage, HistoryPageSource} = loadSrc('NativeHistory');
const g = {appSession: 's', home: 'h', spawnCounter: 1};
const request = (method, nativeParameters, extra = {}) => ({recordKind: 'server-request-entry', requestIdentity: method, generation: g, method, classification: 'known-answerable',
  originClass: ['item/tool/requestUserInput', 'mcpServer/elicitation/request'].includes(method) ? 'person-input' : 'a14', nativeParameters, state: 'outstanding',
  replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'}, ...extra});
const REQUESTS = [
  request('item/commandExecution/requestApproval', {threadId: 'T', turnId: 'u', itemId: 'i', command: 'ls', cwd: '/w', reason: 'list', kind: 'shell', proposedExecpolicyAmendment: ['ls'],
    availableDecisions: ['accept', 'acceptForSession', {acceptWithExecpolicyAmendment: {execpolicy_amendment: ['ls']}}, 'decline', 'cancel', 'a future decision']}),
  request('item/fileChange/requestApproval', {threadId: 'T', turnId: 'u', itemId: 'f', reason: 'edit', grantRoot: '/w'}),
  request('item/permissions/requestApproval', {threadId: 'T', turnId: 'u', itemId: 'p', cwd: '/w', reason: 'more', permissions: {network: true}}),
  request('execCommandApproval', {conversationId: 'T', callId: 'c', command: ['ls'], cwd: '/w', reason: 'legacy'}),
  request('applyPatchApproval', {conversationId: 'T', callId: 'c', reason: 'legacy patch', fileChanges: {'a.txt': {}}, grantRoot: '/w'}),
  request('item/tool/requestUserInput', {threadId: 'T', turnId: 'u', itemId: 'q', questions: [{id: 'q1', header: 'Pick', question: 'Which?', isOther: true, isSecret: false,
    options: [{label: 'Allow once', description: 'first'}]}]}),
  request('mcpServer/elicitation/request', {threadId: 'T', turnId: 'u', serverName: 'srv', mode: 'form', message: 'Fill in', requestedSchema: {type: 'object'}}),
  request('a/future/method', {threadId: 'T'}),
];
// Request states and reply observations that put the register's values into the App's sentences.
const REQUEST_STATES = [
  {state: 'errored', settlement: {origin: {class: 'app-rule', ruleName: 'no-tools'}, kind: 'error'}},
  {state: 'declined', settlement: {origin: {class: 'app-rule', ruleName: 'on-stop'}, kind: 'decline'}},
  {state: 'resolved-by-supplier', supplierResolution: {cause: 'turn ended'}},
  {state: 'a future state'},
];
const activityItem = (id, native, extra = {}) => ({threadId: 'T', turnId: 'turn-1', native: {id, ...native}, displayState: 'completed', standing: 'live-observed', observationEnded: false, observedOrder: 0, ...extra});
const ACTIVITY = {
  typesPin: '0.167.0', supplierStanding: 'verified-pin', limits: ['a limit'],
  items: [
    activityItem('m', {type: 'agentMessage', text: 'answer', phase: 'final_answer'}, {displayState: 'in-progress', previewStanding: 'streamed so far; may differ from the completed item', preview: 'ans'}),
    activityItem('r', {type: 'reasoning', summary: ['think'], content: []}, {displayState: 'unknown', endReason: 'turn ended without item completion'}),
    activityItem('c', {type: 'commandExecution', command: 'ls', cwd: '/w', source: 'userShell', status: 'failed', exitCode: 2, durationMs: 5, aggregatedOutput: 'out', commandActions: []}, {startNative: {source: 'agent'}, settlementOrigin: {origin: 'person'}}),
    activityItem('f', {type: 'fileChange', status: 'declined', changes: [{path: 'a.txt', kind: {type: 'update', move_path: 'b.txt'}, diff: '+x'}]}),
    activityItem('t', {type: 'mcpToolCall', server: 'srv', tool: 'read', arguments: {a: 1}, readOnlyHint: true, durationMs: 3, status: 'completed', result: {content: [{type: 'text', text: 'tool text'}]}, error: null}),
    activityItem('d', {type: 'dynamicToolCall', namespace: 'ns', tool: 'tool', arguments: {}, success: false, status: 'completed', contentItems: [{type: 'inputText', text: 'dyn'}]}),
    activityItem('o', {type: 'functionCallOutput', namespace: 'ns', name: 'fn', output: 'result'}),
    activityItem('g', {type: 'collabAgentToolCall', tool: 'spawnAgent', status: 'completed', senderThreadId: 'T', receiverThreadIds: ['C'], model: 'm', reasoningEffort: 'high', prompt: 'help',
      agentsStates: {C: {status: 'running', message: 'busy'}}}),
    activityItem('s', {type: 'subAgentActivity', kind: 'started', agentPath: 'reviewer', agentThreadId: 'C'}),
    activityItem('w', {type: 'webSearch', query: 'q'}),
    activityItem('i', {type: 'imageView', path: 'p.png'}),
    activityItem('x', {type: 'a future item', raw: 'r'}),
  ],
  turns: [{id: 'turn-1', status: 'inProgress', startedAt: 100, durationMs: 9, error: {message: 'turn error'}, items: []}],
  turnRecords: [{threadId: 'T', turnId: 'turn-1', errors: [{error: {message: 'err', additionalDetails: 'more'}, willRetry: true, receiptPosition: 4, ordinalInTurn: 1}],
    unreadableErrors: [{kind: 'server-request-named-error', receiptPosition: 5, ordinalInTurn: 1}]}],
  revisions: [{kind: 'checklist', revisionId: 'k1', threadId: 'T', turnId: 'turn-1', ordinal: 1, content: {explanation: 'plan', steps: [{step: 'Read', status: 'inProgress'}]}},
    {kind: 'checklist', revisionId: 'k2', threadId: 'T', turnId: 'turn-1', ordinal: 2, content: {explanation: 'plan', steps: [{step: 'Read', status: 'completed'}]}}],
  descendants: [{threadId: 'C', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', statusSource: 'collabAgentToolCall.agentsStates', lastObservedStatus: {status: 'running', message: 'm'},
    guidance: 'a reading', observationEnded: false, nativeThread: {id: 'C', agentRole: 'reviewer', agentNickname: 'Ada'}}],
  goals: {T: {native: {objective: 'goal'}, source: 'thread/goal/updated'}},
  checklistGaps: [{threadId: 'T', turnId: 'turn-0', reason: 'not kept'}],
};
const run = {reference: 'run:1', workflow: {name: 'pump-skid', revision: 'abc123'}, conversation: 'T', turn: 'turn-1', lifecycle: {state: 'ended', end: {cause: 'you ended it'}}, endedAfterTurn: 'turn-1'};
const stop = {stopRequestId: 's1', label: 'interrupted by the person', reading: 'Final status observed when the turn ended.', codexReported: 'interrupted', persistence: 'recorded in the App ledger', earlierSession: true};
const binding = (page, kind) => ({accepted: true, notice: 'Latest accepted page for this selection.', page, rawPage: page, home: 'h', generation: g, epoch: 1, threadId: 'T', resolution: {outcome: 'matched'},
  query: {params: {turnId: kind === 'items' ? 'turn-1' : undefined, sortDirection: 'desc'}}});
const turnPage = {data: [{id: 'turn-1', status: 'interrupted', itemsView: 'summary', startedAt: 100, completedAt: 200, durationMs: 9, error: {message: 'e'},
  items: [{type: 'userMessage', content: [{type: 'text', text: 'hi'}]}, {type: 'agentMessage', text: 'there'}, {type: 'a future item'}]}]};
const itemPage = {data: ACTIVITY.items.map(row => row.native)};

function renders(keep) {
  const p = value => poison(value, keep);
  const out = [];
  for (const r of REQUESTS) {
    const poisoned = p(r);
    out.push([`card ${r.method}`, renderToStaticMarkup(React.createElement(NativeRequestCard, {request: poisoned, view: null, answer: async () => {}}))]);
    for (const extra of REQUEST_STATES) out.push([`card ${r.method} ${extra.state}`, renderToStaticMarkup(React.createElement(NativeRequestCard, {request: {...poisoned, ...p(extra)}, view: null, answer: async () => {}}))]);
    for (const command of [{kind: 'rejected', reason: 'already-resolved'}, {kind: 'unconfirmed', writeResult: 'unknown'}]) {
      const scope = JSON.stringify([poisoned.generation, poisoned.requestIdentity]);
      out.push([`card ${r.method} reply ${command.kind}`, renderToStaticMarkup(React.createElement(NativeRequestCard, {request: poisoned, view: null, answer: async () => {},
        observation: {scope, command: p(command), custody: {scope, available: false, reason: p('custody unavailable')}}}))]);
    }
  }
  out.push(['waiting count', renderToStaticMarkup(React.createElement(WaitingRequestsIndicator, {overview: p({groups: [{modeHomeClass: 'account', generation: g, threadId: 'T', count: 2}],
    sources: [{modeHomeClass: 'account', state: 'stopped'}], coverage: 'coverage words'}), open: () => {}}))]);
  const view = p(ACTIVITY);
  out.push(['activity', renderToStaticMarkup(React.createElement(NativeActivityView, {view, threadId: keep.has('threadId') ? 'T' : p('T'), runs: [p(run)],
    stopLabelFor: () => p(stop), trialTurns: [p({threadId: 'T', turnId: 'turn-1', label: 'trial 1'})], trialChildren: [p({threadId: 'C', label: 'trial child'})], delegation: p({reading: 'missing', reason: 'off', readAt: 'now'})}))]);
  out.push(['run markers', renderToStaticMarkup(React.createElement('div', null, React.createElement(RunStartMarker, {run: p(run)}), React.createElement(RunEndMarker, {run: p(run)}), React.createElement(RunLabel, {run: p(run)})))]);
  out.push(['stop label', renderToStaticMarkup(React.createElement(StopLabel, {stop: p(stop)}))]);
  out.push(['stop label, no request', renderToStaticMarkup(React.createElement(StopLabel, {stop: p({label: 'interrupted by Stop Codex', codexReported: 'completed'})}))]);
  out.push(['history source', renderToStaticMarkup(React.createElement(HistoryPageSource, {binding: p(binding(turnPage, 'turns'))}))]);
  out.push(['history turns', renderToStaticMarkup(React.createElement(StoredTurnPage, {binding: p(binding(turnPage, 'turns')), canRead: true, readItems: () => {}}))]);
  out.push(['history items', renderToStaticMarkup(React.createElement(StoredItemPage, {binding: p(binding(itemPage, 'items'))}))]);
  return out;
}

test('rendered: with every supplied string poisoned (the routing fields kept), no supplied text reaches a control, heading, attribute or the App\'s sentences', () => {
  // The routing fields keep their values so each kind of card, item and state is drawn by its own code.
  const keep = new Set(['method', 'type', 'state', 'displayState', 'originClass', 'classification', 'recordKind', 'mode', 'isOther', 'isSecret', 'reading', 'kind', 'threadId', 'turnId', 'conversation', 'turn', 'endedAfterTurn',
    'generation', 'appSession', 'home', 'requestIdentity', 'class', 'standing', 'sortDirection', 'outcome', 'accepted',
    // A history binding's notice is the App's: historyPageBinding sets it from literals (the listed exception).
    'notice']);
  const pages = renders(keep);
  assert.ok(pages.length > 40, 'every surface drawn');
  for (const [what, raw] of pages) {
    // The source line draws only the identities kept for routing in this run; the second run poisons those too.
    if (what !== 'history source') assert.ok(raw.includes(MARK), `${what}: the poisoned values are drawn somewhere (inside boxes)`);
    assertBoundary(raw, what);
  }
});

test('rendered: with every string poisoned, routing fields too, every kind and state is drawn as one the App does not recognise, and still nothing escapes', () => {
  // Only what links rows together keeps its value; every kind, method, state and status is a value the App does not know.
  for (const [what, raw] of renders(new Set(['threadId', 'turnId', 'generation', 'appSession', 'home', 'requestIdentity', 'conversation', 'turn', 'endedAfterTurn', 'accepted', 'notice']))) assertBoundary(raw, `${what} (unfamiliar)`);
});

test('rendered: a removed boundary is caught: a supplied value drawn raw fails the rendered check', () => {
  // The check itself, on a page that breaks the rule in each place it looks.
  for (const [raw, where] of [[`<p>About ${MARK}</p>`, 'a sentence'], [`<button>${MARK}</button>`, 'a button'], [`<h3>x</h3><p title="${MARK}"></p>`, 'an attribute'],
    [`<summary>x <span role="group" aria-label="n" class="agent-text"><span class="agent-text-label">L</span> <span class="agent-text-value">${MARK}</span></span></summary>`, 'a box inside a summary']])
    assert.throws(() => assertBoundary(raw, where), undefined, where);
});
