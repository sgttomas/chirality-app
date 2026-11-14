// The presentation boundary on the four covered views (RequestCards, NativeActivity, NativeHistory, RunOffers): the
// aim is that every value from Codex, an agent or a record reaches the page only through an approved presentation
// (AgentText, SuppliedId, Word, Num, Flag, or the functions plainId, idWords, wordOf, numberWords, isoSeconds,
// clockWords), and that a control or heading holds only the App's words. Two kinds of evidence: the guard's verdict on
// the source (a syntactic check of listed forms, with known limitations), and the rendered page on valid fixtures,
// which first asserts each surface's readable body is drawn and then poisons each enumerated leaf and key in turn.
// Invented material only.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';
import {guardFailures, sourceFailures, wordTableFailures, GUARDED_VIEWS, APP_ONLY, APP_ONLY_ROLES} from './support/presentation-guard.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {continuationFixture} from './support/continuation-fixture.mjs';

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
  // Under a computed string-literal key, raw HTML is still raw HTML: it fails and cannot be listed.
  const computed = '{ ["dangerouslySetInnerHTML"]: { __html: row.text } }';
  const computedRaw = `export const V = ({ row }: any) => <div {...${computed}} />;`;
  fails(computedRaw, 'raw HTML under a computed literal key');
  assert.notDeepEqual(judge(computedRaw, 'Invented.tsx', [{file: 'Invented.tsx', where: '{...}', expr: computed, reason: 'invented'}]), [], 'raw HTML under a computed literal key cannot be listed');
  fails('export const V = ({ row }: any) => <div {...{ children: row.text }} />;', 'children in a spread');
  fails('import { Pretty } from "./Pretty";\nexport const V = ({ row }: any) => <div {...{ children: <Pretty value={row.text} /> }} />;', 'an outside component hidden in a spread\'s children');
  fails('export const V = () => <div {...{ onClick: () => {} }} />;', 'a key not on the list');
  passes('export const V = () => <div {...{ id: "x", className: "c", title: "The App\'s words" }} />;', 'listed keys with the App\'s values');
});
test('presentation guard closure: a control or heading role holds only the App\'s words, as the tags do', () => {
  fails(IMPORTS + 'export const V = ({ row }: any) => <div role="heading"><AgentText value={row.text} /></div>;', 'a box inside role=heading');
  fails(IMPORTS + 'export const V = ({ row }: any) => <span role="button"><SuppliedId value={row.id} /></span>;', 'an identity presentation inside role=button');
  fails(IMPORTS + 'export const V = ({ row, h }: any) => <div role={h ? "heading" : "note"}><AgentText value={row.text} /></div>;', 'a box inside a role that may be a heading');
  fails(IMPORTS + 'export const V = ({ row }: any) => <div role="heading note"><AgentText value={row.text} /></div>;', 'a box inside a role token list that holds heading');
  fails(IMPORTS + 'export const V = ({ row }: any) => <div role="note  button"><AgentText value={row.text} /></div>;', 'a box inside a role token list that holds a control role later');
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

// The rendered page, on valid fixtures: each surface is first drawn as it is, with a check that what it is meant to
// show is shown; then every leaf of its data (each string, number, boolean and null, and each object key) is
// replaced in turn by P, the rest left as it was, and the page drawn again, statically and mounted. P may appear
// only inside a box (AgentText, or the box an approved presentation falls back to); never in a control, a heading,
// an element whose role is one, a naming or describing attribute or its target, or a text field's value. A value
// may also be withheld (not drawn at all).
const MARK = 'UNTRUSTED';
const RLO = '‮';
const P = `${MARK}\n${RLO}Allow once`;

/** The page with every box read as ⟦label value⟧ and then removed: what remains is the App's own words. */
const outsideBoxes = raw => agentPlain(raw).replace(/⟦[^⟧]*⟧/g, '');
const APP_ONLY_ELEMENTS = new RegExp(`<(${[...APP_ONLY].join('|')})\\b[^>]*>([\\s\\S]*?)</\\1>`, 'g');
const NAMING_ATTRIBUTES = /\s(aria-[a-z]+|title|alt|placeholder|value|label)="([^"]*)"/g;
// A box is what AgentText draws: a group with a non-empty accessibility name and a visible border, whose first child is
// a non-empty source label, then the value. The box's classes on anything less are not a box, and fail.
const BOX = /<(?:span|div) role="group" aria-label="([^"]*)" class="agent-text(?: agent-text-block)?" style="([^"]*)"><(?:span|div) class="agent-text-label" style="[^"]*">([^<]*)<\/(?:span|div)> ?<(?:span|div) class="agent-text-value"/g;
// Elements whose role, a space-separated token list, holds a control or heading role, with what they enclose.
const ROLE_OPEN = /<([a-z][a-z0-9]*)\b[^>]*?\srole="([^"]*)"[^>]*>/g;
function roleElements(raw) {
  const out = [];
  for (const m of raw.matchAll(ROLE_OPEN)) {
    const role = m[2].trim().split(/\s+/).find(r => APP_ONLY_ROLES.has(r));
    if (!role || m[0].endsWith('/>')) continue;
    const close = new RegExp(`<${m[1]}\\b[^>]*?(/?)>|</${m[1]}>`, 'g');
    close.lastIndex = m.index + m[0].length;
    let depth = 1, end = raw.length, x;
    while (depth > 0 && (x = close.exec(raw))) { if (x[0].startsWith('</')) depth--; else if (!x[1]) depth++; if (depth === 0) end = x.index; }
    out.push({role, inner: raw.slice(m.index + m[0].length, end)});
  }
  return out;
}
function assertBoundary(markup, what) {
  // An option's value is the selector's opaque target, never drawn; its displayed text is checked.
  const raw = markup.replace(/(<option\b[^>]*?\svalue=")[^"]*(")/g, '$1$2');
  const boxes = [...raw.matchAll(BOX)];
  assert.equal((raw.match(/class="agent-text(?: agent-text-block)?"/g) ?? []).length, boxes.length, `${what}: the box's class on something that is not a box`);
  assert.equal((raw.match(/class="agent-text-value"/g) ?? []).length, boxes.length, `${what}: a value with the box's class outside a box`);
  for (const [, name, style, label] of boxes) assert.ok(name.trim() !== '' && label.trim() !== '' && /(^|;)border:/.test(style), `${what}: a box without its source label, its accessibility name or its border`);
  const outside = outsideBoxes(raw);
  assert.ok(!outside.includes(MARK), `${what}: supplied text outside a box: …${outside.slice(Math.max(0, outside.indexOf(MARK) - 160), outside.indexOf(MARK) + 80)}…`);
  assert.ok(!raw.includes(RLO), `${what}: a direction override drawn as it is`);
  for (const [, tag, inner] of raw.matchAll(APP_ONLY_ELEMENTS)) {
    assert.ok(!inner.includes(MARK), `${what}: supplied text inside a ${tag}: ${inner.slice(0, 200)}`);
    assert.ok(!/agent-text/.test(inner), `${what}: a box inside a ${tag}: ${inner.slice(0, 200)}`);
  }
  for (const {role, inner} of roleElements(raw)) {
    assert.ok(!inner.includes(MARK), `${what}: supplied text inside role="${role}": ${inner.slice(0, 200)}`);
    assert.ok(!/agent-text/.test(inner), `${what}: a box inside role="${role}": ${inner.slice(0, 200)}`);
  }
  for (const [, name, value] of raw.matchAll(NAMING_ATTRIBUTES)) {
    assert.ok(!value.includes(MARK), `${what}: supplied text in ${name}="${value.slice(0, 120)}"`);
  }
}

// The mounted page, read node by node.
const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const classes = node => (node.getAttribute?.('class') ?? '').split(/\s+/);
// The value of a box as AgentText draws it: its group has a non-empty name and a border, and a non-empty source label.
const wellFormedBox = node => {
  const group = node.parentNode;
  return !!group && group.getAttribute?.('role') === 'group' && classes(group).includes('agent-text') && (group.getAttribute('aria-label') ?? '').trim() !== ''
    && String(group.style?.border ?? '').trim() !== '' && group.childNodes.some(c => classes(c).includes('agent-text-label') && (c.textContent ?? '').trim() !== '');
};
const SHOWN_ATTRIBUTES = name => name.startsWith('aria-') || ['title', 'alt', 'placeholder', 'label'].includes(name);
function assertMounted(container, what) {
  const byId = new Map();
  container.querySelectorAll(n => n.hasAttribute('id')).forEach(n => byId.set(n.getAttribute('id'), n));
  const walk = (node, ctx) => {
    if (node.nodeType === 3) {
      const t = node.nodeValue ?? '';
      assert.ok(!t.includes(RLO), `${what}: a direction override drawn as it is`);
      if (t.includes(MARK)) {
        assert.ok(ctx.box, `${what}: supplied text outside a box, in <${ctx.tag}>: ${t.slice(0, 80)}`);
        assert.ok(!ctx.control, `${what}: supplied text inside ${ctx.control}`);
      }
      return;
    }
    if (node.nodeType !== 1) return;
    const tag = node.localName, role = node.getAttribute('role');
    for (const [name, value] of node.attributes) {
      if (name === 'value' && tag === 'option') continue;
      assert.ok(!value.includes(RLO), `${what}: a direction override in ${name}`);
      if (SHOWN_ATTRIBUTES(name) || (name === 'value' && ['input', 'textarea'].includes(tag))) assert.ok(!value.includes(MARK), `${what}: supplied text in <${tag} ${name}>`);
      if (['aria-labelledby', 'aria-describedby', 'aria-details', 'aria-errormessage'].includes(name)) for (const id of value.split(/\s+/)) {
        const target = byId.get(id);
        assert.ok(!target || (!target.textContent.includes(MARK) && target.querySelectorAll(n => classes(n).includes('agent-text')).length === 0), `${what}: <${tag} ${name}> names supplied text`);
      }
    }
    for (const field of ['value', 'defaultValue']) if (['input', 'textarea'].includes(tag) && typeof node[field] === 'string') assert.ok(!node[field].includes(MARK), `${what}: supplied text in a field's ${field}`);
    const appRole = (role ?? '').trim().split(/\s+/).find(r => APP_ONLY_ROLES.has(r));
    const control = ctx.control || (APP_ONLY.has(tag) ? `<${tag}>` : appRole ? `role="${role}"` : null);
    if (control) assert.ok(!classes(node).includes('agent-text'), `${what}: a box inside ${control}`);
    if (classes(node).includes('agent-text-value')) assert.ok(wellFormedBox(node), `${what}: a value with the box's class outside a box with its name, border and source label`);
    const box = ctx.box || (classes(node).includes('agent-text-value') && wellFormedBox(node));
    for (const child of node.childNodes) walk(child, {box, control, tag});
  };
  walk(container, {box: false, control: null, tag: 'div'});
}

// Every leaf of a fixture, and the fixture with one leaf replaced by P. A surface's own top-level keys name the props
// the test passes (request, view, host…), not supplied data, so they are not renamed; everything under them is. The
// App's own structures beside a request (its place and a reply observation: RequestPlace, RequestReplyObservation)
// keep their keys too; their values are poisoned.
const APP_SHAPED = new Set(['place', 'command', 'custody']);
function leaves(value, path = [], out = []) {
  if (Array.isArray(value)) value.forEach((v, i) => leaves(v, [...path, i], out));
  else if (value && typeof value === 'object') for (const key of Object.keys(value)) { if (path.length > 0 && !APP_SHAPED.has(path[0])) out.push({path, key}); leaves(value[key], [...path, key], out); }
  else out.push({path});
  return out;
}
function poisonedAt(data, {path, key}) {
  // A JSON copy, so an object the fixture shares in two places (a generation) is two objects: one leaf changes.
  const copy = JSON.parse(JSON.stringify(data));
  const at = path.reduce((v, k) => v[k], copy);
  if (key === undefined) {
    if (path.length === 0) return P;
    path.slice(0, -1).reduce((v, k) => v[k], copy)[path.at(-1)] = P;
    return copy;
  }
  const renamed = Object.fromEntries(Object.entries(at).map(([k, v]) => [k === key ? P : k, v]));
  if (path.length === 0) return renamed;
  path.slice(0, -1).reduce((v, k) => v[k], copy)[path.at(-1)] = renamed;
  return copy;
}
const where = ({path, key}) => `${path.join('.')}${key === undefined ? '' : ` key ${key}`}`;

// The fixtures. g is a valid generation; T the conversation; every supplied text is distinctive so a positive check
// can find it.
const {NativeRequestCard, WaitingRequestsIndicator, requestScopeKey} = loadSrc('RequestCards');
const {NativeActivityView, RunStartMarker, RunEndMarker, RunLabel, StopLabel} = loadSrc('NativeActivity');
const {StoredTurnPage, StoredItemPage, historyPageBinding, ContinuationContext} = loadSrc('NativeHistory');
const {RunOffer} = loadSrc('RunOffers');
const {AgentText} = loadSrc('AgentText');
const g = {appSession: 's', home: 'h', spawnCounter: 1};
const descendant = {threadId: 'C', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', statusSource: 'collabAgentToolCall.agentsStates', lastObservedStatus: {status: 'running', message: 'child-status-message'},
  guidance: 'child-guidance', observationEnded: false, nativeThread: {id: 'C', agentRole: 'child-role', agentNickname: 'child-nickname'}};
const request = (method, nativeParameters, extra = {}) => ({recordKind: 'server-request-entry', requestIdentity: 7, generation: g, method, classification: 'known-answerable',
  originClass: ['item/tool/requestUserInput', 'mcpServer/elicitation/request'].includes(method) ? 'person-input' : 'a14', nativeParameters, state: 'outstanding',
  replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'}, ...extra});
const requestView = items => ({generation: g, home: 'h', items, descendants: [descendant]});
const fileRow = {threadId: 'C', turnId: 'u', native: {id: 'f', type: 'fileChange', status: 'inProgress', changes: [{path: 'rel/changed.txt', kind: {type: 'update', move_path: '/outside/moved.txt'}, diff: '+diff-line'}]}, displayState: 'waiting-on-request', standing: 'live-observed'};
const commandRow = {threadId: 'T', turnId: 'u', native: {id: 'i', type: 'commandExecution', command: 'ls'}, displayState: 'waiting-on-request', standing: 'live-observed'};
const COMMAND = request('item/commandExecution/requestApproval', {threadId: 'T', turnId: 'u', itemId: 'i', command: 'cmd-text', cwd: '/cmd-folder', reason: 'cmd-reason', kind: 'cmd-kind',
  proposedExecpolicyAmendment: ['rule-word'], proposedNetworkPolicyAmendments: [{host: 'net-host'}], additionalPermissions: {network: true},
  availableDecisions: ['accept', 'acceptForSession', {acceptWithExecpolicyAmendment: {execpolicy_amendment: ['amend-word']}}, 'decline', 'cancel', 'future-decision']});
const QUESTION = request('item/tool/requestUserInput', {threadId: 'C', turnId: 'u', itemId: 'q', isBlocking: false, questions: [{id: 'q1', header: 'question-header', question: 'question-words', isOther: true, isSecret: false,
  options: [{label: 'option-label', description: 'option-description'}]}]});
const PLACE = {project: {kind: 'folder', folder: '/project'}, conversationFolder: '/conversation', permissionProfile: ':workspace'};
const requestSurface = (name, req, view, expect, extra = {}) => ({name, data: {request: req, view, place: PLACE, refusal: 'refusal-words already-resolved', ...extra},
  draw: d => React.createElement(NativeRequestCard, {request: d.request, view: d.view, place: d.place, activityLink: () => ({open() {}}),
    answer: async () => { throw new Error(d.refusal); }, ...(d.command ? {observation: {scope: requestScopeKey(d.request), command: d.command, custody: {...d.custody, scope: requestScopeKey(d.request)}}} : {})}),
  expect, interact: true});

const offerWorkflow = {kind: 'workflow', origin: 'project', source_root: '/offer-library', name: 'load-check', revision: 'abcdef0123456789', revision_method: 'm'};
const compatibility = {occasionLabel: 'CK-1 offered candidate', statement: 'compat-statement', advisory: true, notCurrent: true,
  preparation: {check: {result: 'unsupported', findings: ['compat-finding']}, role: {standing: 'app-observed', role: 'role-in-force'}, declaration: {raw: {compatible_roles: ['declared-role']}},
    requirements: [{name: 'requirement-name', purpose: 'requirement-purpose', reason: 'requirement-reason', fallback: 'requirement-fallback', outcome: 'missing'}],
    basis: {surface: 'basis-surface', acting_pin: 'basis-pin', catalog_edition: 'basis-catalog', environment_observation: 'basis-environment', conversation: 'T', home: 'h', generation: g}, evaluated_at: 'evaluated-at-time'},
  inventoryOrigin: {kind: 'inventory-kind', source: 'inventory-source'}, publication: {state: 'not published', factsNotSupplied: ['publication-limit']}, r14: 'r14-words'};
const finishedOffer = {message: {threadId: 'T', turnId: 'turn-1', itemId: 'm'}, finished: {run: 'run:workflow:a', statement: 'Workflow finished: project:finished-flow', standing: 'finished-standing'},
  proposal: {proposed: 'project:proposed-flow', resolution: {workflow: offerWorkflow, standing: 'registered — selectable in this App session', notice: null},
    runInForce: {run: 'run:workflow:a', workflow: 'pump-skid', endCause: 'completed'}, compatibility, context: {sourceRef: 'source:original'}, standing: 'proposal-standing'}};
const unresolvedOffer = {message: {threadId: 'T', turnId: 'turn-2', itemId: 'm2'}, finished: null,
  proposal: {proposed: 'project:unknown-flow', resolution: {workflow: null, notice: 'resolution-notice-words'}, runInForce: null, standing: 'proposal-standing'}};
const run = {reference: 'run:workflow:a', workflow: {name: 'pump-skid', revision: 'abc123'}, conversation: 'T', turn: 'turn-1', lifecycle: {state: 'ended by the person', end: {cause: 'ended to start next-flow'}}, endedAfterTurn: 'turn-2', finishedReport: {run: 'run:workflow:a'}};
const unplacedRun = {reference: 'run:workflow:b', workflow: {name: 'Unsafe Name', revision: 'not-hex-revision'}, conversation: 'T', turn: 'gone', lifecycle: {state: 'open (live)'}, endedAfterTurn: null};
const item = (turnId, order, native, extra = {}) => ({threadId: 'T', turnId, native, displayState: 'completed', standing: 'live-observed', observationEnded: false, observedOrder: order, ...extra});
const RUN_TEXT = '[Chirality] Workflow run start: pump-skid from the project library "/lib", revision abc123, run run:workflow:a.\nrun-text-body';
const ACTIVITY = {
  generation: g, home: 'h', typesPin: '0.167.0', supplierStanding: 'supplier-standing', limits: ['activity-limit'], observationEnded: false,
  items: [
    item('turn-1', 0, {id: 'u', type: 'userMessage', content: [{type: 'text', text: RUN_TEXT}, {type: 'text', text: 'user-message-words'}, {type: 'image', url: 'image-url'}]}),
    item('turn-1', 1, {id: 'm', type: 'agentMessage', text: 'agent-message-words', phase: 'final_answer'}),
    item('turn-1', 2, {id: 'r', type: 'reasoning', summary: ['reasoning-words'], content: []}, {displayState: 'unknown', endReason: 'turn ended without item completion', summaryPreview: ['reasoning-preview']}),
    item('turn-1', 3, {id: 'p', type: 'plan', text: 'plan-words'}, {displayState: 'in-progress', preview: 'plan-preview', previewStanding: 'in progress; may differ from completed plan'}),
    item('turn-1', 4, {id: 'c', type: 'commandExecution', command: 'command-words', cwd: '/command-folder', source: 'userShell', status: 'failed', exitCode: 2, durationMs: 5, aggregatedOutput: 'command-output', commandActions: []},
      {displayState: 'failed', startNative: {source: 'agent'}, settlementOrigin: {origin: 'settlement-origin'}, requestRef: {generation: g, requestIdentity: 7}}),
    item('turn-1', 5, {id: 'f', type: 'fileChange', status: 'declined', changes: [{path: 'change-path', kind: {type: 'update', move_path: 'moved-path'}, diff: 'diff-words'}]}, {displayState: 'declined'}),
    item('turn-1', 6, {id: 't', type: 'mcpToolCall', server: 'mcp-server', tool: 'mcp-tool', arguments: {argument: 'mcp-argument'}, readOnlyHint: true, durationMs: 3, status: 'completed',
      result: {content: [{type: 'text', text: 'mcp-result-text'}, {type: 'resource', resource: {text: 'mcp-resource-text'}}, {type: 'image', data: 'image-data'}]}, error: {message: 'mcp-error'}}),
    item('turn-1', 7, {id: 'd', type: 'dynamicToolCall', namespace: 'dyn-namespace', tool: 'dyn-tool', arguments: {}, success: false, status: 'completed', contentItems: [{type: 'inputText', text: 'dyn-text'}]}),
    item('turn-1', 8, {id: 'o', type: 'functionCallOutput', namespace: 'fn-namespace', name: 'fn-name', output: 'fn-output'}),
    item('turn-1', 9, {id: 'g', type: 'collabAgentToolCall', tool: 'spawnAgent', status: 'completed', senderThreadId: 'T', receiverThreadIds: ['C'], model: 'requested-model', reasoningEffort: 'high', prompt: 'delegation-prompt',
      agentsStates: {C: {status: 'running', message: 'agent-state-message'}}}),
    item('turn-1', 10, {id: 's', type: 'subAgentActivity', kind: 'started', agentPath: 'agent-path', agentThreadId: 'C'}),
    item('turn-1', 11, {id: 'w', type: 'webSearch', query: 'search-query'}),
    item('turn-1', 12, {id: 'i', type: 'imageView', path: 'image-path'}),
    item('turn-1', 13, {id: 'k', type: 'contextCompaction'}),
    item('turn-1', 14, {id: 'x', type: 'future-item-kind', raw: 'future-raw'}),
    item('turn-2', 15, {id: 'm2', type: 'agentMessage', text: 'second-turn-words'}),
  ],
  turns: [{id: 'turn-1', status: 'inProgress', startedAt: 100, durationMs: 9, error: {message: 'native-turn-error'}, items: []}, {id: 'turn-2', status: 'completed', startedAt: 200, items: []}],
  turnRecords: [{threadId: 'T', turnId: 'turn-1'}, {threadId: 'T', turnId: 'turn-2'}],
  turnErrors: [{threadId: 'T', turnId: 'turn-1', error: {message: 'error-notice-message', additionalDetails: 'error-notice-details'}, willRetry: true, receiptPosition: 4, ordinalInTurn: 2}],
  unreadableTurnErrors: [{threadId: 'T', turnId: 'turn-1', kind: 'server-request-named-error', receiptPosition: 5, ordinalInTurn: 1}],
  revisions: [{kind: 'checklist', revisionId: 'k1', threadId: 'T', turnId: 'turn-1', ordinal: 1, content: {explanation: 'checklist-explanation', steps: [{step: 'earlier-step', status: 'inProgress'}]}},
    {kind: 'checklist', revisionId: 'k2', threadId: 'T', turnId: 'turn-1', ordinal: 2, content: {explanation: 'checklist-explanation', steps: [{step: 'checklist-step', status: 'completed'}]}},
    {kind: 'plan-item', threadId: 'T', turnId: 'turn-1', itemId: 'p', ordinal: 3, standing: 'live-observed'}],
  descendants: [descendant],
  goals: {T: {native: {objective: 'goal-objective'}, source: 'goal-source'}},
  checklistGaps: [{threadId: 'T', turnId: 'turn-0', reason: 'gap-reason'}],
};
const stop = {stopRequestId: 's1', label: 'interrupted by the person', reading: 'stop-reading', codexReported: 'interrupted', persistence: 'stop-persistence', earlierSession: true};
const historyItems = [
  {id: 'h-user', type: 'userMessage', content: [{type: 'text', text: 'history-user-words'}]},
  {id: 'h-plan', type: 'plan', text: 'history-plan-words'},
  {id: 'h-command', type: 'commandExecution', command: 'history-command', status: 'completed', exitCode: 0, aggregatedOutput: 'history-output'},
  {id: 'h-tool', type: 'mcpToolCall', server: 'history-server', tool: 'history-tool', status: 'inProgress', result: null, error: null},
  {id: 'h-agent', type: 'agentMessage', text: 'history-agent-words'},
  {id: 'h-future', type: 'history-future-kind'},
];
const historyHost = () => {
  const context = continuationFixture({generation: g, items: historyItems});
  context.history.selected.turnsPage.data[0] = {...context.history.selected.turnsPage.data[0], startedAt: 100, completedAt: 'not-a-time', durationMs: 9, error: {message: 'history-turn-error'}};
  return {state: 'ready', generation: g, nativeHistory: context.history};
};
const continuation = () => ({host: {state: 'ready', generation: g, continuationContexts: [continuationFixture({generation: g, items: historyItems})]},
  thread: {nativeResumeObserved: true, resumeRequestRef: 'req:resume', generation: g, threadId: 'stored'}});
const noop = async () => {};

const SURFACES = [
  requestSurface('command card', COMMAND, requestView([commandRow]), ['cmd-text', '/cmd-folder', 'cmd-reason', 'cmd-kind', 'rule-word', 'net-host', 'amend-word', 'future-decision']),
  requestSurface('file change card', request('item/fileChange/requestApproval', {threadId: 'C', turnId: 'u', itemId: 'f', reason: 'file-reason', grantRoot: '/grant-root', cwd: '/cwd'}), requestView([fileRow]),
    ['file-reason', '/grant-root', '/cwd/rel/changed.txt', '/outside/moved.txt', '+diff-line', 'child-role']),
  requestSurface('permissions card', request('item/permissions/requestApproval', {threadId: 'T', turnId: 'u', itemId: 'p', cwd: '/perm-folder', reason: 'perm-reason', permissions: {network: 'perm-value'}}), null, ['/perm-folder', 'perm-reason', 'perm-value']),
  requestSurface('legacy command card', request('execCommandApproval', {conversationId: 'T', callId: 'c', command: ['legacy-cmd'], cwd: '/legacy-folder', reason: 'legacy-reason'}), null, ['legacy-cmd', '/legacy-folder', 'legacy-reason']),
  requestSurface('legacy patch card', request('applyPatchApproval', {conversationId: 'T', callId: 'c', reason: 'patch-reason', fileChanges: {'patch-file.txt': {}}, grantRoot: '/patch-root'}), null, ['patch-reason', 'patch-file.txt', '/patch-root']),
  requestSurface('question card', QUESTION, requestView([]), ['question-header', 'question-words', 'option-label', 'option-description', 'child-role', 'child-nickname']),
  requestSurface('input request card', request('mcpServer/elicitation/request', {threadId: 'T', turnId: 'u', serverName: 'server-name', mode: 'url', message: 'elicitation-message', url: 'https://elicitation.invalid', requestedSchema: {field: 'schema-field'}}), null,
    ['server-name', 'elicitation-message', 'https://elicitation.invalid', 'schema-field']),
  // An unknown request's parameters are shown only as received, in its source dump: its readable body is the App's words and the method.
  requestSurface('unknown request card', request('future/method', {threadId: 'T', detail: 'future-detail'}), null, ['future/method', 'Codex named the request']),
  requestSurface('errored by rule', {...COMMAND, state: 'errored', settlement: {origin: {class: 'app-rule', ruleName: 'rule-name'}, kind: 'error'}}, null, ['rule-name']),
  requestSurface('resolved by Codex', {...COMMAND, state: 'resolved-by-supplier', supplierResolution: {cause: 'supplier-cause'}}, null, ['supplier-cause']),
  requestSurface('retained reply', {...COMMAND, state: 'declined', closedGeneration: true, replyWriteResult: 'written', settlement: {origin: {class: 'person'}, kind: 'decline', nativeContent: {answer: 'retained-answer'}, redaction: true}}, null, ['retained-answer']),
  requestSurface('reply rejected', COMMAND, null, ['rejected-reason', 'custody-reason'], {command: {kind: 'rejected', reason: 'rejected-reason'}, custody: {available: false, reason: 'custody-reason'}}),
  requestSurface('reply unconfirmed', QUESTION, null, ['write-result-value'], {command: {kind: 'unconfirmed', writeResult: 'write-result-value'}, custody: {available: true, state: 'outstanding'}}),
  {name: 'waiting requests', data: {overview: {groups: [{modeHomeClass: 'account', generation: g, threadId: 'C', count: 2}, {modeHomeClass: 'project', generation: g, threadId: 'thread with spaces', count: 1}],
    sources: [{modeHomeClass: 'source-home', state: 'source-state'}], coverage: 'coverage-words'}, view: requestView([])},
  draw: d => React.createElement(WaitingRequestsIndicator, {overview: d.overview, view: d.view, open: () => {}}), expect: ['thread with spaces', 'coverage-words', 'source-home', 'source-state', 'child-nickname']},
  {name: 'activity', data: {view: ACTIVITY, threadId: 'T', runs: [run, unplacedRun], offers: [finishedOffer, unresolvedOffer], stop, trialTurns: [{threadId: 'T', turnId: 'turn-1', label: 'trial-turn-label'}],
    trialChildren: [{threadId: 'C', label: 'trial-child-label'}], delegation: {reading: 'missing', reason: 'delegation-reason', readAt: 'delegation-read-at'}},
  draw: d => React.createElement(NativeActivityView, {view: d.view, threadId: d.threadId, runs: d.runs, offers: d.offers, offerControls: {generation: g, ready: true, busy: false, act: noop},
    stopLabelFor: () => d.stop, trialTurns: d.trialTurns, trialChildren: d.trialChildren, delegation: d.delegation}),
  expect: ['run-text-body', 'user-message-words', 'agent-message-words', 'reasoning-preview', 'plan-preview', 'command-words', '/command-folder', 'command-output', 'change-path', 'moved-path', 'diff-words',
    'mcp-server', 'mcp-tool', 'mcp-argument', 'mcp-result-text', 'mcp-resource-text', 'mcp-error', 'dyn-namespace / dyn-tool', 'dyn-text', 'fn-namespace / fn-name', 'fn-output', 'requested-model', 'delegation-prompt',
    'agent-state-message', 'agent-path', 'search-query', 'future-item-kind', 'second-turn-words', 'native-turn-error', 'error-notice-message — error-notice-details', 'checklist-explanation', 'checklist-step', 'earlier-step',
    'goal-objective', 'goal-source', 'gap-reason', 'supplier-standing', 'activity-limit', 'child-status-message', 'child-guidance', 'child-role', 'child-nickname', 'trial-turn-label', 'trial-child-label',
    'delegation-reason', 'delegation-read-at', 'stop-reading', 'stop-persistence', 'settlement-origin', 'revision 3 in this conversation', 'Unsafe Name not-hex-revi', 'ended to start next-flow',
    'Workflow finished: project:finished-flow', 'project:proposed-flow', 'compat-statement', 'compat-finding', 'role-in-force', 'declared-role', 'requirement-name', 'requirement-purpose', 'requirement-reason',
    'requirement-fallback', 'basis-surface', 'basis-pin', 'basis-catalog', 'basis-environment', 'evaluated-at-time', 'inventory-kind', 'inventory-source', 'publication-limit', 'r14-words', '/offer-library',
    'End pump-skid and start load-check', 'project:unknown-flow', 'resolution-notice-words']},
  {name: 'run offer, plain start', data: {offer: {message: {threadId: 'T', turnId: 'turn-1', itemId: 'm'}, finished: null,
    proposal: {proposed: 'project:Unsafe Flow', resolution: {workflow: {...offerWorkflow, name: 'Unsafe Flow', origin: 'bundled', revision: 'not-hex'}, standing: 'registered — selectable in this App session', notice: null},
      runInForce: null, compatibility: {occasionLabel: 'occasion-label', limit: 'compat-limit', advisory: true}, context: {}}}},
  draw: d => React.createElement(RunOffer, {offer: d.offer, generation: g, ready: true, busy: false, act: noop}), expect: ['Start the proposed workflow (proposed by the agent)', 'Unsafe Flow', 'occasion-label', 'compat-limit', 'not-hex']},
  {name: 'run offer, unsafe run in force', data: {offer: {message: {}, finished: {run: 'run with spaces', statement: 'finished-statement'},
    proposal: {proposed: 'p', resolution: {workflow: offerWorkflow, standing: 'unknown-standing'}, runInForce: {run: 'run with spaces', workflow: 'Unsafe Current', endCause: 'unknown-cause'}, compatibility: {preparation: {role: {standing: 'unknown', reason: 'role-reason'}}}}}},
  draw: d => React.createElement(RunOffer, {offer: d.offer, generation: g, ready: true, busy: false, act: noop}),
  expect: ['End the current run and start load-check', 'Unsafe Current', 'unknown-cause', 'run with spaces', 'finished-statement', 'unknown-standing', 'role-reason']},
  {name: 'run markers and stop labels', data: {run: {...run, lifecycle: {state: 'ended', end: {cause: 'end-cause-words'}}}, unsafe: unplacedRun, stop, stopNoRequest: {label: 'stop-label-words', codexReported: 'turn-status-words'}},
  draw: d => React.createElement('div', null, React.createElement(RunStartMarker, {run: d.run}), React.createElement(RunEndMarker, {run: d.run}), React.createElement(RunLabel, {run: d.unsafe}),
    React.createElement(StopLabel, {stop: d.stop}), React.createElement(StopLabel, {stop: d.stopNoRequest})),
  expect: ['pump-skid', 'run:workflow:a', 'end-cause-words', 'Unsafe Name', 'stop-reading', 'stop-persistence', 'stop-label-words', 'turn-status-words']},
  {name: 'history turns', data: {host: historyHost()}, draw: d => React.createElement(StoredTurnPage, {binding: historyPageBinding(d.host, 'turns'), canRead: true, readItems: () => {}}),
    expect: ['Recorded as your message:', 'prior-turn', '1970-01-01T00:01:40.000Z', 'not-a-time', 'history-user-words', 'history-future-kind', 'history-turn-error', 'Latest accepted page for this selection']},
  {name: 'history items', data: {host: historyHost()}, draw: d => React.createElement(StoredItemPage, {binding: historyPageBinding(d.host, 'items')}),
    expect: ['Recorded as your message:', 'The agent wrote:', 'history-user-words', 'history-plan-words', 'history-command', 'history-output', 'history-server', 'history-tool', 'history-agent-words', 'history-future-kind', 'h-command']},
  {name: 'continuation context', data: continuation(), draw: d => React.createElement(ContinuationContext, {host: d.host, thread: d.thread}),
    expect: ['Recorded as your message:', 'The agent wrote:', 'Prior work: bounded partial snapshot', 'req:resume', 'history-user-words', 'history-plan-words', 'history-command', 'history-agent-words', 'Read more turns']},
];

// The source dumps: boxes that hold the received JSON as it was sent. Every value of a fixture is in one, so a positive
// assertion that counted them would hold even when the readable body was withheld. Positives read the page without them.
const DUMP_LABELS = new Set(['As Codex sent it:', 'Codex sent (native JSON):', "The App's record of this read, with Codex's identities (JSON):", 'The read, with the pages Codex sent (JSON):']);
// The dumps are block boxes, read as ⟦label⏎lines⟧: the label is everything before the first line break.
const readableMarkup = raw => agentPlain(raw).replace(/⟦([^\n⟧]*)\n[^⟧]*⟧/g, (box, label) => DUMP_LABELS.has(label) ? '' : box);
const readableText = node => node.nodeType === 3 ? node.nodeValue ?? ''
  : node.nodeType !== 1 ? ''
  : classes(node).includes('agent-text') && node.childNodes.some(c => classes(c).includes('agent-text-label') && DUMP_LABELS.has((c.textContent ?? '').trim())) ? ''
  : node.childNodes.map(readableText).join('');

// One surface drawn statically and mounted; the question and command cards are also answered, so the chosen option
// and a refused answer are drawn.
async function drawn(surface, data, what) {
  const raw = renderToStaticMarkup(surface.draw(data));
  assertBoundary(raw, `${what} (static)`);
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  try {
    await React.act(() => root.render(surface.draw(data)));
    assertMounted(container, `${what} (mounted)`);
    let text = container.textContent;
    let readable = readableMarkup(raw) + '\n' + readableText(container);
    if (surface.interact) {
      const button = words => container.querySelectorAll(n => n.localName === 'button' && n.textContent === words)[0];
      for (const words of ['Choose option 1', 'Allow once']) if (button(words)) {
        await React.act(async () => { await props(button(words)).onClick(); });
        assertMounted(container, `${what} (mounted, after ${words})`);
        text += container.textContent;
        readable += '\n' + readableText(container);
      }
    }
    return {raw, text, readable};
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}

test('rendered: each surface, drawn on valid fixtures, shows what it is meant to show, and stays within the boundary', async t => {
  let positive = 0;
  for (const surface of SURFACES) {
    const {readable} = await drawn(surface, surface.data, surface.name);
    // Each expected value must be drawn outside the source dumps, in the surface's readable body.
    for (const value of surface.expect) { assert.ok(readable.includes(value), `${surface.name}: ${value} is drawn in the readable body`); positive++; }
  }
  // The interactions draw what they are for.
  const answered = await drawn(SURFACES.find(s => s.name === 'question card'), SURFACES.find(s => s.name === 'question card').data, 'question card');
  assert.ok(answered.text.includes('Its label: option-label'), 'the chosen option is drawn, boxed');
  const refused = await drawn(SURFACES[0], SURFACES[0].data, 'command card');
  assert.ok(refused.text.includes('Last answer not taken: Codex already resolved it.') && refused.text.includes('refusal-words'), 'a refused answer is drawn, its report boxed');
  positive += 2;
  t.diagnostic(`${SURFACES.length} surfaces; ${positive} positive assertions`);
  assert.ok(positive > 150);
});

test('rendered: each leaf of every surface poisoned in turn (strings, numbers, booleans, null and object keys) reaches the page only inside a box', async t => {
  let renders = 0, boxed = 0, withheld = 0;
  for (const surface of SURFACES) {
    for (const leaf of leaves(surface.data)) {
      const what = `${surface.name} @ ${where(leaf)}`;
      // A render that throws fails the test as well.
      const {raw, text} = await drawn(surface, poisonedAt(surface.data, leaf), what);
      renders += 2;
      if (raw.includes(MARK) || text.includes(MARK)) boxed++; else withheld++;
    }
  }
  t.diagnostic(`${renders} renders (${renders / 2} static, ${renders / 2} mounted): ${boxed} poisoned variants drew the value boxed, ${withheld} withheld it`);
  assert.ok(boxed > 500 && renders > 1500);
});

test('rendered: the detectors take a box only as AgentText draws it, and a role token list as its roles', async () => {
  const shownValue = 'UNTRUSTED⏎‹U+202E›Allow once';
  // The fourth reading's counterexample: the box's classes with no source label, no accessibility name and no border.
  const stripped = `<span role="group" aria-label="" class="agent-text" style=""><span class="agent-text-label" style=""></span> <span class="agent-text-value" style="">${shownValue}</span></span>`;
  assert.throws(() => assertBoundary(stripped, 'stripped'), /without its source label/, 'an unmarked box fails the static check');
  const strippedNodes = () => {
    const root = document.createElement('div'), group = document.createElement('span');
    group.setAttribute('role', 'group'); group.setAttribute('aria-label', ''); group.setAttribute('class', 'agent-text');
    const label = document.createElement('span'); label.setAttribute('class', 'agent-text-label');
    const value = document.createElement('span'); value.setAttribute('class', 'agent-text-value'); value.textContent = shownValue;
    group.appendChild(label); group.appendChild(value); root.appendChild(group);
    return {root, group, label};
  };
  assert.throws(() => assertMounted(strippedNodes().root, 'stripped'), /outside a box/, 'an unmarked box fails the mounted check');
  const named = strippedNodes(); named.group.setAttribute('aria-label', 'Text Codex sent'); named.label.textContent = 'Codex sent:';
  assert.throws(() => assertMounted(named.root, 'no border'), /outside a box/, 'a box without its border fails the mounted check');
  // A heading given as a role token list.
  const real = renderToStaticMarkup(React.createElement(AgentText, {value: P, source: 'codex'}));
  assertBoundary(real, 'a real box');
  assert.throws(() => assertBoundary(`<div role="heading note">${real}</div>`, 'role list'), /inside role="heading"/, 'a box inside role="heading note" fails the static check');
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  try {
    await React.act(() => root.render(React.createElement('div', null, React.createElement(AgentText, {value: P, source: 'codex'}))));
    assertMounted(container, 'a real box, mounted');
    await React.act(() => root.render(React.createElement('div', {role: 'heading note'}, React.createElement(AgentText, {value: P, source: 'codex'}))));
    assert.throws(() => assertMounted(container, 'role list'), /inside role="heading note"/, 'a box inside role="heading note" fails the mounted check');
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
});

test('rendered: the positives read the readable body: history entries without their {turnId,item} wrapper fail them, though every value is still in the source dumps', async () => {
  const surface = SURFACES.find(s => s.name === 'history items');
  const bare = JSON.parse(JSON.stringify(surface.data));
  const page = bare.host.nativeHistory.selected.itemsPage;
  page.data = page.data.map(entry => entry.item);
  const {raw, readable} = await drawn(surface, bare, 'history items without wrappers');
  const missing = surface.expect.filter(value => !readable.includes(value));
  assert.ok(missing.includes('The agent wrote:') && missing.includes('history-agent-words'), `the withheld bodies fail the positives (missing: ${missing.join(', ')})`);
  assert.ok(agentPlain(raw).includes('history-agent-words'), 'the value is still in a source dump, which the positives do not count');
  // An unknown request's parameters are shown only in its source dump: there, not in its readable body.
  const unknown = await drawn(SURFACES.find(s => s.name === 'unknown request card'), SURFACES.find(s => s.name === 'unknown request card').data, 'unknown request card');
  assert.ok(!unknown.readable.includes('future-detail') && agentPlain(unknown.raw).includes('future-detail'), 'an unknown request\'s parameters are in its source dump only');
});

test('rendered: a removed boundary is caught: a supplied value drawn raw fails the rendered checks', async () => {
  // The static check, on a page that breaks the rule in each place it looks.
  for (const [raw, where] of [[`<p>About ${MARK}</p>`, 'a sentence'], [`<button>${MARK}</button>`, 'a button'], [`<h3>x</h3><p title="${MARK}"></p>`, 'an attribute'], [`<p>${RLO}</p>`, 'a direction override'],
    [`<summary>x <span role="group" aria-label="n" class="agent-text"><span class="agent-text-label">L</span> <span class="agent-text-value">${MARK}</span></span></summary>`, 'a box inside a summary']])
    assert.throws(() => assertBoundary(raw, where), undefined, where);
  // The mounted check: raw text, text inside a control role, a box inside a heading role, a reference to supplied text, a field's value.
  const box = React.createElement('span', {className: 'agent-text'}, React.createElement('span', {className: 'agent-text-value'}, MARK));
  for (const [element, where] of [[React.createElement('p', null, MARK), 'raw text'], [React.createElement('div', {role: 'button'}, box), 'a box inside role=button'],
    [React.createElement('div', {role: 'heading'}, box), 'a box inside role=heading'], [React.createElement('div', null, React.createElement('span', {id: 'x'}, box), React.createElement('button', {'aria-labelledby': 'x'}, 'App')), 'a reference to a box'],
    [React.createElement('input', {value: MARK, readOnly: true}), 'a field value'], [React.createElement('p', {'aria-label': MARK}), 'an accessible name']]) {
    const surface = {draw: () => element};
    await assert.rejects(drawnMountedOnly(surface), undefined, where);
  }
});
async function drawnMountedOnly(surface) {
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  try { await React.act(() => root.render(surface.draw())); assertMounted(container, 'self-check'); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}
