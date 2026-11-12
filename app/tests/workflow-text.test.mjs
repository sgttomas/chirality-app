import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// Reading a workflow's own text in Run a workflow: under an included entry's
// About, and beside the chosen workflow. Controlled host views and an invented
// workflow_read_text reply that the test settles; no native App, supplier,
// model or person act. Imported by a test file the web suite already lists.
if (!globalThis.document) installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {RunWorkflowGuide} = loadSrc('RunJourney');
const {heldFromReply, identityKey} = loadSrc('WorkflowText');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const ROOT = 'invented-library:library-v9.9.9', METHOD = 'invented.package.sha256/v1';
const REV = 'alpha-revision-0123456789abcdef', REV2 = 'alpha-revision-fedcba9876543210';
const identity = (name, revision, over = {}) => ({kind:'workflow', origin:'bundled', source_root:ROOT, name, revision, revision_method:METHOD, ...over});
const entry = (name, revision = `${name}-revision-0123456789`) => ({name, revision, origin:'bundled', sourceRoot:ROOT, revisionMethod:METHOD, identity:identity(name, revision), runnable:true, runLimit:null,
  description:`Invented description of ${name}.`, roles:[], compatibility:'canonical', libraryPathsNamed:[], navigation:{category:'specialist', tier:'primary', order:1, group:{key:'g', label:'Invented group', order:1}}});
const catalogue = (revision = REV) => ({standing:'invented standing', source:{tag:'library-v9.9.9'},
  entries:[entry('alpha-flow', revision), ...['b', 'c', 'd', 'e', 'f', 'h'].map(n => entry(`${n}-flow`))]});
const PROJECT = identity('resolve-spacing', 'rev-2-abcdef0123456789', {origin:'project', source_root:'/invented/project'});
const selections = (chosen = PROJECT) => [{sourceRef:'src', threadId:'T1', selection:{state:'selected', reference:'sel-1', runnable:true, runLimit:null, currentLimit:null, identity:chosen}}];
function host() {
  return {state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}}, serverRequests:[],
    threads:[{threadId:'T1', generation:g, model:'invented-model', status:{type:'idle'}}]};
}
function data(over = {}) {
  return {context:{sourceRef:'src', generation:g, historyEpoch:3}, projectLibraryAvailable:true, activeLibrary:null, libraries:[],
    productionCatalog:catalogue(), selections:[], runs:[], reviews:[], ...over};
}
// The text as a workflow might write it: markup and Markdown that must be shown, never rendered.
const TEXT = '---\nname: alpha-flow\n---\n# Alpha\n\n<b>not markup</b> **not bold** [not a link](https://example.invalid)\n\tindented line\n';
const readReply = (id, text = TEXT) => ({state:'read', target:{}, identity:id, text, bytes:new TextEncoder().encode(text).length,
  files:[{path:'notes/README.md', bytes:42}, {path:'scripts/run.py', bytes:7}], matched:true, standing:'invented standing'});

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => all(c, 'button').find(node => node.textContent === label);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const ancestors = node => { const out = []; for (let at = node.parentNode; at; at = at.parentNode) out.push(at); return out; };

function heldHost() {
  const pending = [];
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke(command, args) { return new Promise((resolve, reject) => pending.push({command, args, resolve, reject})); }};
  return {pending, of:command => pending.filter(p => p.command === command), restore() { window.__TAURI_INTERNALS__ = previous; }};
}
async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = [];
  const render = () => root.render(React.createElement(RunWorkflowGuide, {data:view.data, host:view.host ?? host(), thread:view.thread ?? '', busy:false, text:'', viewStale:!!view.viewStale,
    chooseThread:() => {}, setText:() => {}, act:async (command, args) => { calls.push({command, args}); }, outcome:null}));
  await React.act(async () => render());
  return {c, calls,
    press:async label => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); },
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); },
    close:async () => React.act(async () => root.unmount())};
}
const settle = async (pending, value, how = 'resolve') => React.act(async () => { pending[how](value); await Promise.resolve(); });
// The App's own words around a text: the region without the text itself.
const ownWords = (c, label) => { const r = region(c, label); const pre = all(r, 'pre')[0]; return r.textContent.replace(pre ? pre.textContent : '', ''); };
const NO_CLAIM = /\b(requires?|required|requirements?|needs?|available|availability|missing|present|ready|works?|working|will run|can run|runnable|compatible|supported|safe|tools?|valid|summary|means)\b/i;

test('an included entry\'s text is read when pressed, shown literally with its identity, and the words claim nothing of fitness', async () => {
  const h = heldHost(); const ui = await mount({data:data()});
  try {
    assert.equal(h.pending.length, 0, 'nothing is read before the person asks');
    await ui.press("Read alpha-flow's text");
    const [read] = h.of('workflow_read_text');
    assert.deepEqual(read.args.target, {kind:'included', name:'alpha-flow', revision:REV});
    assert.equal(read.args.context.sourceRef, 'src'); assert.equal(read.args.context.threadId, null);
    assert.equal(ui.calls.length, 0, 'the guide\'s own act (selection, preparation) is not used');
    assert.ok(button(ui.c, "Reading alpha-flow's text…") && props(button(ui.c, "Reading alpha-flow's text…")).disabled);
    await settle(read, readReply(identity('alpha-flow', REV)));
    const shown = region(ui.c, 'Text of alpha-flow');
    const pre = all(shown, 'pre')[0];
    assert.equal(pre.textContent, TEXT, 'exactly as read');
    assert.equal(all(pre, 'b').length + all(pre, 'strong').length + all(pre, 'a').length + all(pre, 'h1').length, 0, 'nothing in the text is rendered');
    const words = ownWords(ui.c, 'Text of alpha-flow');
    assert.match(words, /The WORKFLOW\.md of alpha-flow — included with the App, from Chirality Library 9\.9\.9, revision alpha-revisi…, as the App read it when you asked \(\d+ bytes\)\. Its files matched this revision when they were read\. Shown exactly as read\./);
    assert.match(words, /This revision's other 2 files/); assert.match(words, /notes\/README\.md \(42 bytes\)/); assert.match(words, /scripts\/run\.py \(7 bytes\)/);
    assert.doesNotMatch(words, NO_CLAIM, `the App's words make no claim about requirements or fitness: ${words}`);
    // Hidden, it is gone; read again, it asks the host again.
    await ui.press("Hide alpha-flow's text");
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'pre').length, 0);
    await ui.press("Read alpha-flow's text");
    assert.equal(h.of('workflow_read_text').length, 2);
  } finally { await ui.close(); h.restore(); }
});

test('a refusal is said with the host\'s reason and never as an empty workflow', async () => {
  const h = heldHost(); const ui = await mount({data:data()});
  try {
    await ui.press("Read alpha-flow's text");
    await settle(h.of('workflow_read_text')[0], {state:'refused', target:{}, identity:identity('alpha-flow', REV),
      reason:'the App could not read this revision\'s files and tie them to its identity', cause:'revision not verified', standing:'no text was returned'});
    const shown = region(ui.c, 'Text of alpha-flow');
    assert.equal(all(shown, 'pre').filter(p => !ancestors(p).some(a => a.localName === 'details')).length, 0, 'no text block');
    const alert = all(shown, 'p').find(p => p.getAttribute('role') === 'alert');
    assert.equal(alert.textContent, "The App did not show alpha-flow's text: the App could not read this revision's files and tie them to its identity.");
    assert.match(shown.textContent, /What the App reported.*revision not verified/s);
    assert.doesNotMatch(shown.textContent, /empty|no instructions|nothing to read/i);
    // A command refused outright is said with its own words.
    await ui.press("Read alpha-flow's text again");
    await settle(h.of('workflow_read_text')[1], new Error('Workflow native generation changed; refresh the displayed choice'), 'reject');
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'p').find(p => p.getAttribute('role') === 'alert').textContent,
      "The App did not show alpha-flow's text: Workflow native generation changed; refresh the displayed choice.");
    // An empty text that the host read and matched is shown as an empty text, never confused with a refusal.
    await ui.press("Read alpha-flow's text again");
    await settle(h.of('workflow_read_text')[2], readReply(identity('alpha-flow', REV), ''));
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'pre')[0].textContent, '');
    assert.match(region(ui.c, 'Text of alpha-flow').textContent, /\(0 bytes\)/);
  } finally { await ui.close(); h.restore(); }
});

test('a reply is shown only as the text of the identity it was read for', () => {
  const key = identityKey(identity('alpha-flow', REV));
  assert.equal(identityKey({...identity('alpha-flow', REV), revision_method:undefined}), null, 'an incomplete identity holds nothing');
  assert.equal(heldFromReply(key, readReply(identity('alpha-flow', REV))).state, 'read');
  for (const reply of [readReply(identity('alpha-flow', REV2)), readReply(identity('alpha-flow', REV, {origin:'project'})),
    {...readReply(identity('alpha-flow', REV)), matched:false}, {...readReply(identity('alpha-flow', REV)), matched:undefined},
    {...readReply(identity('alpha-flow', REV)), text:undefined}, null, 'text', {state:'refused'}]) {
    const held = heldFromReply(key, reply);
    assert.equal(held.state, 'refused', JSON.stringify(reply)); assert.equal(held.text, undefined); assert.ok(held.reason);
  }
});

test('text read for one identity is not shown under another', async () => {
  const h = heldHost(); const ui = await mount({data:data()});
  try {
    await ui.press("Read alpha-flow's text");
    await settle(h.of('workflow_read_text')[0], readReply(identity('alpha-flow', REV)));
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'pre')[0].textContent, TEXT);
    // The entry's revision changes: the earlier text is not shown under the new one.
    await ui.rerender({data:data({productionCatalog:catalogue(REV2)})});
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'pre').length, 0);
    assert.match(region(ui.c, 'Text of alpha-flow').textContent, /The text read earlier here was of another workflow or revision; it is not shown\./);
    assert.ok(button(ui.c, "Read alpha-flow's text"));
    // A reply that arrives for a superseded read is not applied.
    await ui.press("Read alpha-flow's text");
    const late = h.of('workflow_read_text')[1];
    assert.deepEqual(late.args.target, {kind:'included', name:'alpha-flow', revision:REV2});
    await ui.rerender({data:data()});
    await ui.press("Read alpha-flow's text");
    await settle(late, readReply(identity('alpha-flow', REV2), 'late text'));
    assert.ok(button(ui.c, "Reading alpha-flow's text…"), 'the later read is still the one awaited');
    await settle(h.of('workflow_read_text')[2], readReply(identity('alpha-flow', REV)));
    assert.equal(all(region(ui.c, 'Text of alpha-flow'), 'pre')[0].textContent, TEXT);
  } finally { await ui.close(); h.restore(); }
});

test('the chosen workflow\'s text is read as the conversation\'s selection and follows that selection', async () => {
  const h = heldHost(); const ui = await mount({data:data({selections:selections()}), thread:'T1'});
  try {
    await ui.press("Read resolve-spacing's text");
    const [read] = h.of('workflow_read_text');
    assert.deepEqual(read.args.target, {kind:'selection', revision:PROJECT.revision});
    assert.equal(read.args.context.threadId, 'T1'); assert.equal(read.args.context.selectionRef, 'sel-1');
    await settle(read, readReply(PROJECT, 'project text\n'));
    assert.equal(all(region(ui.c, 'Text of resolve-spacing'), 'pre')[0].textContent, 'project text\n');
    const words = ownWords(ui.c, 'Text of resolve-spacing');
    assert.match(words, /The WORKFLOW\.md of resolve-spacing — project library, revision rev-2-abcdef…/);
    assert.doesNotMatch(words, NO_CLAIM, words);
    // Another revision chosen for the conversation: the earlier text is not shown under it.
    const newer = {...PROJECT, revision:'rev-3-0123456789abcdef'};
    await ui.rerender({data:data({selections:[{...selections(newer)[0], selection:{...selections(newer)[0].selection, reference:'sel-2'}}]})});
    assert.equal(all(region(ui.c, 'Text of resolve-spacing'), 'pre').length, 0);
    assert.ok(button(ui.c, "Read resolve-spacing's text"));
    // No conversation chosen: no chosen workflow, so no control.
    await ui.rerender({thread:''});
    assert.equal(region(ui.c, 'Text of resolve-spacing'), undefined);
  } finally { await ui.close(); h.restore(); }
});

test('a text asked for is still shown, its entry open, when the withheld steps come back', async () => {
  const h = heldHost(); const ui = await mount({data:data()});
  try {
    await ui.press("Read alpha-flow's text");
    await settle(h.of('workflow_read_text')[0], readReply(identity('alpha-flow', REV)));
    // The read is a press: the guide is withheld until the next status read is applied.
    await ui.rerender({viewStale:true});
    assert.equal(region(ui.c, 'Text of alpha-flow'), undefined, 'no step is shown while withheld');
    await ui.rerender({viewStale:false});
    const shown = region(ui.c, 'Text of alpha-flow');
    assert.equal(all(shown, 'pre')[0].textContent, TEXT, 'the text is there when the steps come back');
    const open = ancestors(shown).filter(a => a.localName === 'details');
    assert.equal(open.length, 2, 'inside its About and its group');
    assert.ok(open.every(d => props(d).open === true), 'both are drawn open');
    // Another entry's About stays as it was drawn.
    const other = region(ui.c, 'Text of b-flow');
    assert.ok(ancestors(other).filter(a => a.localName === 'details').some(d => props(d).open !== true));
  } finally { await ui.close(); h.restore(); }
});

test('the read is issued through the web view\'s one command function', async () => {
  const {readFileSync} = await import('node:fs');
  const src = readFileSync(new URL('../src/WorkflowText.tsx', import.meta.url), 'utf8');
  assert.match(src, /import \{ invoke \} from "\.\/hostReads";/);
  assert.doesNotMatch(src, /@tauri-apps\/api\/core|__TAURI_INTERNALS__/);
  const {SELF_ISSUED_QUIET} = loadSrc('hostReads');
  assert.equal(Object.hasOwn(SELF_ISSUED_QUIET, 'workflow_read_text'), false, 'a pressed read marks');
});
