import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentBlocks, agentBlockText} from './support/agent-text.mjs';

// J1 over the right panel's Run and Workflows tabs and the composer's chip, which hold
// what the Run a workflow guide held. Controlled host views only: no native App,
// supplier, model or person act.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {GuideResult, runReading, runTurnNotices, turnStatusWords, guideResultWords} = loadSrc('RunJourney');
const {RunTab} = loadSrc('RunTab');
const {WorkflowLibrary} = loadSrc('WorkflowLibrary');
const {PickChip, pickIncluded, pickListed} = loadSrc('WorkflowPick');
const UNKNOWN = {state:'native workflow-text send outcome unknown; original source retained', limit:'reply lost'};
const REFUSED = {state:'native workflow-text turn/start refused by Codex; original source retained', limit:'invented refusal'};
const NOT_CONFIRMED = 'start not confirmed (turn refused or outcome unknown); not opened, not live';

const raw = JSON.parse(readFileSync(new URL('../src-tauri/resources/workflow_role/workflow-declaration.valid.example.json', import.meta.url), 'utf8'));
const cats = ['expected_inputs','required_tools','checkpoints','returned_outputs','returned_evidence'];
const declaration = {raw, reading:'recognized', findings:[], categories:Object.fromEntries(cats.map(c=>[c,'recognized'])),
  elements:Object.fromEntries(cats.map(c=>[c,(raw[c]??[]).map(value=>({value,reading:'recognized',findings:[]}))]))};
declaration.elements.returned_outputs.push({value:{name:'report-file',form:'file',path:'reports/spacing.md',meaning:'The written report'},reading:'recognized',findings:[]});
const g = {home:'account', appSession:'s1', spawnCounter:1};
const path = text => ({encoding:'unix_bytes', bytes:[...new TextEncoder().encode(text)]});
const OPEN = "open (live); only the person's explicit end ends it";
const PREPARED = 'prepared; not a run until its start turn is observed';

function host(over = {}) {
  return {state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}},
    currentAppProjectContext:{reference:'/invented/work-project', sourceCaption:'configured App directory', standing:'s'}, currentAppProjectContextLimit:null,
    attachmentSelections:{launchAppProjectObservation:{source:'explicit App launch CHIRALITY_WORKSPACE', nativeRoot:path('/invented/work-project'), associationStanding:'a'}},
    threads:[{threadId:'T1', generation:g, model:'invented-model', status:{type:'idle'}}, {threadId:'T2', generation:g, model:'invented-model', status:{type:'idle'}}],
    serverRequests:[], ...over};
}
function data(over = {}) {
  return {context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib:project',
    libraries:[{reference:'lib:project', origin:'project', root:path('/invented/project'), sourceRoot:'project',
      registered:[{name:'resolve-spacing', sequence:2, revision:'rev-2-abcdef0123456789', label:'registered — selectable in this App session', selectable:true},
                  {name:'old-method', sequence:1, revision:'rev-o', label:'registered — store copy missing', selectable:false}],
      entryListing:{state:'observed', reference:'listing-1', libraryRef:'lib:project', entries:[
        {name:'draft-free-entry', reference:'entry-1', reviewable:true, state:'unregistered'},
        {name:'broken', reference:'entry-2', reviewable:false, state:'malformed'}]}}],
    productionCatalog:{standing:'production bundle candidate; not a published release', entries:[{name:'coordinated-knowledge-work', revision:'r', runnable:false}]},
    selections:[], runs:[], reviews:[], ...over};
}
const selected = (runnable = true) => [{sourceRef:'src', threadId:'T1', selection:{state:'selected', reference:'sel-1', runnable, runLimit:runnable ? null : 'not registered',
  identity:{name:'resolve-spacing', origin:'project', revision:'rev-2-abcdef0123456789'}, declaration}}];

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => all(c, 'button').find(node => node.textContent === label);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];

// The guide's steps now stand in three places, each mounted alone here over the same invented views: the Run tab (the
// open conversation's run), the Workflows tab (this project's workflows) and the composer's chip (the picked workflow).
// The single press that chooses, prepares and starts is the composer's Start run (tests/workflow-pick-run.test.mjs).
async function mountWith(component, view, propsOf) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = []; const shown = [];
  const render = () => root.render(React.createElement(component, propsOf(view, calls, shown)));
  await React.act(async () => render());
  return {c, calls, shown,
    press:async (label, within = c) => { const node = button(within, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); },
    click:async node => React.act(async () => props(node).onClick()),
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); },
    close:async () => React.act(async () => root.unmount())};
}
const mountRun = view => mountWith(RunTab, view, (v, calls, shown) => ({data:v.data, host:v.host, thread:v.thread ?? 'T1', busy:!!v.busy, viewStale:!!v.viewStale,
  readFailure:v.readFailure ?? null, outcome:v.outcome ?? null, showConversation:v.navigate ? (id, target) => shown.push([id, target]) : undefined,
  act:async (command, args) => { calls.push({command, args}); }}));
const mountLibrary = view => mountWith(WorkflowLibrary, view, (v, calls) => ({data:v.data, host:v.host, busy:!!v.busy, pick:v.pick ?? null, outcome:v.outcome ?? null,
  setPick:pick => { calls.push({pick}); }, act:async (command, args) => { calls.push({command, args}); }}));
const mountChip = view => mountWith(PickChip, view, v => ({pick:v.pick, host:{...v.host, workflowRoot:v.data}, thread:v.thread ?? 'T1', disabled:false, remove:() => {}}));
// The chip shows a selection only where it is the pick by its whole source: the project library's source root included.
const selectedHere = () => [{...selected()[0], selection:{...selected()[0].selection, identity:{...selected()[0].selection.identity, source_root:'project'}}}];
const projectPick = () => pickListed(data().libraries[0].registered[0], data().libraries[0], host());
const mountResult = view => mountWith(GuideResult, view, v => ({label:'Last result', outcome:v.outcome ?? null, only:v.only}));

test('run readings keep waiting, working, failed, interrupted-start and finished distinct', () => {
  const h = host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]});
  assert.equal(runReading({conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}}, h).tone, 'waiting');
  assert.equal(runReading({conversation:'T2', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}}, host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}],
    threads:[{threadId:'T2', generation:g, status:{type:'active'}}]})).tone, 'working', 'another conversation\'s request is not this run\'s question');
  assert.equal(runReading({conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}}, host({serverRequests:[{state:'answered', nativeParameters:{threadId:'T1'}}]})).tone, 'idle');
  assert.equal(runReading({conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}}, host({threads:[{threadId:'T1', generation:g, status:{type:'systemError'}}]})).tone, 'failed');
  const refused = runReading({conversation:'T1', lifecycle:{state:NOT_CONFIRMED}, status:REFUSED}, host());
  assert.equal(refused.tone, 'failed'); assert.match(refused.detail, /did not run.*invented refusal.*prepare it again/);
  for (const status of [UNKNOWN, {state:'native workflow-text send not started; original records retained', sent:'not observed', limit:'x'}, {}]) {
    const unknown = runReading({conversation:'T1', lifecycle:{state:NOT_CONFIRMED}, status}, host());
    assert.equal(unknown.tone, 'uncertain', JSON.stringify(status)); assert.match(unknown.detail, /may have run\. The App will not resend it/);
    assert.doesNotMatch(unknown.detail, /did not run|prepare/i, 'an unknown outcome never claims nothing ran or suggests a resend');
  }
  const sent = runReading({conversation:'T1', source:'sent', lifecycle:{state:PREPARED}}, host());
  assert.equal(sent.title, 'Starting', 'a send acknowledgment is not a started or completed run');
  assert.equal(runReading({conversation:'T1', lifecycle:{state:PREPARED}, status:{sent:false, state:'WR pre-send publication failed; nothing sent', limit:'disk full'}}, host()).title, 'Not started');
  assert.equal(runReading({conversation:'T1', lifecycle:{state:PREPARED}, status:{sent:false}}, host()).title, 'Ready to start');
  const done = runReading({conversation:'T1', source:'s', lifecycle:{state:'ended by the person', end:{cause:'completed'}}}, host());
  assert.equal(done.tone, 'done'); assert.equal(done.title, 'Ended as completed'); assert.match(done.detail, /has not checked the work/);
  for (const [cause, title] of [['ended by the person','Ended by you'], ['ended to start other-flow','Ended to start another workflow'], ['invalid','Ended'], [undefined,'Ended']]) {
    const ended = runReading({conversation:'T1', source:'s', lifecycle:{state:'ended by the person', end:cause === undefined ? null : {cause}}}, host());
    assert.equal(ended.tone, 'ended', String(cause)); assert.equal(ended.title, title);
    assert.match(ended.detail, /does not say the work is complete/); assert.doesNotMatch(ended.title, /complete|finish/i, 'a plain end is never completed');
  }
  for (const reading of [sent]) assert.doesNotMatch(reading.title + reading.detail, /finished|completed/i);
});
test('a prepared run whose start record was not admitted says so in the Run tab, which offers no start', async () => {
  const limit='Workflow start record not saved; nothing was sent; start again to record it. Its bytes are held in this App process only and lost on quit; cannot be saved from within the App.';
  const view=await mountRun({host:host(),data:data({selections:selected(),runs:[{reference:'run:unsaved',home:'account',generation:g,conversation:'T1',workflow:{name:'resolve-spacing'},lifecycle:{state:PREPARED},publication:{admissionRefusal:limit},status:{sent:false,limit}}]})});
  try {
    assert.equal(button(view.c,'Start the run'),undefined,'the original start is not offered: the press is the composer\'s Start run, which prepares afresh');
    assert.match(region(view.c,'Run progress').textContent,/not saved.*lost on quit/);
    assert.deepEqual(view.calls,[]);
  } finally {await view.close();}
});

test('before Codex or a project is available, the Workflows tab says what to do and issues nothing', async () => {
  const ui = await mountLibrary({host:host({state:'absent', generation:null}), data:data({projectLibraryAvailable:false, activeLibrary:null})});
  try {
    assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#desktop-setup'), 'no project names Desktop setup');
    assert.equal(button(ui.c, 'Show this project\'s workflows'), undefined);
    assert.match(region(ui.c, 'Workflows').textContent, /No project folder is set for this App yet\. Choose a project in Desktop setup — the choice applies when you next open the App\./);
    await ui.rerender({host:host({state:'absent'}), data:data({activeLibrary:null})});
    assert.equal(props(button(ui.c, 'Show this project\'s workflows')).disabled, true, 'Codex not connected: the project library is not opened');
    await ui.click(button(ui.c, 'Show this project\'s workflows'));
    await ui.rerender({host:host()});
    assert.equal(!!props(button(ui.c, 'Show this project\'s workflows')).disabled, false);
    assert.deepEqual(ui.calls, []);
  } finally { await ui.close(); }
});

test('an existing registered workflow is found in the Workflows tab and picked, the chip says what it needs, and the Run tab reads its run', async () => {
  const lib = await mountLibrary({host:host(), data:data({activeLibrary:null})});
  try {
    await lib.press('Show this project\'s workflows');
    assert.deepEqual(lib.calls.at(-1), {command:'workflow_open_project_library', args:{}});
    await lib.rerender({data:data()});
    const card = region(lib.c, 'Project workflow resolve-spacing');
    assert.equal(!!props(button(card, 'Use in message')).disabled, false, 'a pick needs no conversation: Start run chooses it for the conversation it starts or is in');
    const old = region(lib.c, 'Project workflow old-method');
    assert.equal(props(button(old, 'Use in message')).disabled, true, 'a non-selectable revision cannot be picked');
    assert.match(old.textContent, /store copy missing/);
    await lib.click(button(card, 'Use in message'));
    const {pick} = lib.calls.at(-1);
    assert.deepEqual([pick.kind, pick.libraryRef, pick.name, pick.revision], ['listed', 'lib:project', 'resolve-spacing', 'rev-2-abcdef0123456789'], 'the pick names the library and revision shown');
    assert.equal(lib.calls.filter(call => call.command).length, 1, 'picking issues no command');
  } finally { await lib.close(); }
  const chip = await mountChip({host:host(), data:data({selections:selectedHere()}), pick:projectPick()});
  try {
    const needs = region(chip.c, 'What this workflow needs').textContent;
    for (const name of ['run', 'spacing-limit', 'supports-table']) assert.ok(needs.includes(name), name);
  } finally { await chip.close(); }
  const prepared = {reference:'run-1', conversation:'T1', home:'account', generation:g, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{sent:false}, compatibility:[{preparation:{declaration}}]};
  const run = await mountRun({host:host(), data:data({selections:selected(), runs:[prepared]})});
  try {
    assert.match(region(run.c, 'Run progress').textContent, /Ready to start/);
    assert.equal(button(run.c, 'Prepare this run'), undefined); assert.equal(button(run.c, 'Start the run'), undefined, 'the press is the composer\'s Start run');
    const results = region(run.c, 'Where the results go').textContent;
    assert.match(results, /report-file — declared path reports\/spacing\.md: The written report/);
    const tab = region(run.c, 'Run').textContent;
    assert.match(tab, /the project folder \/invented\/work-project/);
    assert.doesNotMatch(tab, /\/invented\/project/, 'the opened library folder is never presented as the results location');
    assert.match(tab, /hasn't checked that any of them exist/);
    assert.deepEqual(run.calls, []);
  } finally { await run.close(); }
});

test('an open run in the Run tab reports questions, offers End run and the agent\'s finished report; a finished run says so', async () => {
  const open = {reference:'run-1', conversation:'T1', home:'account', generation:g, source:'sent', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}, status:{}};
  const ui = await mountRun({host:host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]}), data:data({selections:selected(), runs:[open]})});
  try {
    assert.match(region(ui.c, 'Run progress').textContent, /Waiting for your answer/);
    assert.ok(all(region(ui.c, 'Run'), 'a').some(a => a.getAttribute('href') === '#conversation'), 'without App navigation, a link to the conversation');
    assert.equal(button(ui.c, 'End run as completed'), undefined, 'no completed end without the host\'s finished offer');
    await ui.press('End run');
    assert.deepEqual(ui.calls.at(-1), {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:null}});
    const message = {threadId:'T1', turnId:'turn-9', itemId:'m'};
    await ui.rerender({data:data({selections:selected(), runs:[open], offers:[{message, finished:{run:'run-1', statement:'Workflow finished: project:resolve-spacing'}}, {message:{threadId:'T1'}, finished:{run:'run-other', statement:'x'}}]})});
    assert.match(region(ui.c, 'Agent finished report').textContent, /The agent wrote Workflow finished: project:resolve-spacing/);
    await ui.press('End run as completed');
    assert.deepEqual(ui.calls.at(-1), {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:message}}, 'the existing completed path carries the host\'s exact report message');
    await ui.rerender({host:host(), data:data({selections:selected(), runs:[{...open, lifecycle:{state:'ended by the person', end:{cause:'completed'}}}]})});
    assert.match(region(ui.c, 'Run progress').textContent, /Ended as completed\./);
    assert.equal(button(ui.c, 'End run'), undefined);
    const other = {...open, reference:'run-x', conversation:'T2'};
    await ui.rerender({data:data({selections:selected(), runs:[other]})});
    assert.ok(region(ui.c, 'Run progress') === undefined, 'another conversation\'s run is not shown as this one');
    assert.match(region(ui.c, 'Run').textContent, /resolve-spacing is chosen for this conversation\. No run has been started\./);
  } finally { await ui.close(); }
});

test('an unregistered library entry is reviewed singly in the Workflows tab; an included workflow the host does not run cannot be picked', async () => {
  const ui = await mountLibrary({host:host(), data:data()});
  try {
    const entry = region(ui.c, 'Project workflow draft-free-entry');
    assert.ok(entry); assert.ok(region(ui.c, 'Project workflow broken') === undefined, 'an entry that cannot be reviewed is not offered');
    await ui.press('Review for first use…', entry);
    assert.deepEqual(ui.calls.at(-1), {command:'workflow_review_library_entries', args:{libraryRef:'lib:project', listingRef:'listing-1', entryRefs:['entry-1']}});
    await ui.press('Look for other workflows in this library');
    assert.deepEqual(ui.calls.at(-1), {command:'workflow_library_entries_refresh', args:{libraryRef:'lib:project'}});
    const included = region(ui.c, 'Included workflow coordinated-knowledge-work');
    assert.match(included.textContent, /Can't be used in this App: production bundle candidate; not a published release\./, 'the host reason is said beside the workflow');
    assert.equal(props(button(included, 'Use in message')).disabled, true);
    await ui.rerender({data:data({productionCatalog:{standing:'released', entries:[{name:'coordinated-knowledge-work', revision:'bundled-rev-0123456789', runnable:true, runLimit:null}]}})});
    await ui.click(button(region(ui.c, 'Included workflow coordinated-knowledge-work'), 'Use in message'));
    assert.deepEqual([ui.calls.at(-1).pick.kind, ui.calls.at(-1).pick.name], ['included', 'coordinated-knowledge-work'], 'a host-runnable included workflow is picked; Start run selects it');
    await ui.rerender({data:data({reviews:[{reference:'rev-ref', status:{presentation:{entries:[]}}}], activeReview:'rev-ref'})});
    assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#workflow-reviews'));
    assert.equal(ui.calls.filter(call => call.command).length, 2, 'only the review and the refresh issued commands');
  } finally { await ui.close(); }
});

test('a stale workflow source disables every command of the Workflows and Run tabs', async () => {
  const stale = host({workflowRoot:{context:{sourceRef:'other', generation:g}}});
  const lib = await mountLibrary({host:stale, data:data({selections:selected()})});
  const clickAll = async (ui, labels) => { for (const label of labels) { const node = button(ui.c, label); assert.ok(node, label); assert.equal(props(node).disabled, true, label);
    await React.act(async () => props(node).onClick()); } };
  try {
    assert.match(region(lib.c, 'Workflows').textContent, /The workflow view is out of date/);
    await clickAll(lib, ['Reload this project\'s workflows', 'Review for first use…', 'Look for other workflows in this library']);
    assert.equal(props(button(region(lib.c, 'Project workflow resolve-spacing'), 'Use in message')).disabled, true, 'picking waits for a current view too');
    assert.deepEqual(lib.calls, [], 'a retained click on a stale control dispatches nothing');
  } finally { await lib.close(); }
  const open = {reference:'run-o', conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}, status:{}};
  const run = await mountRun({host:stale, data:data({selections:selected(), runs:[open], offers:[{message:{threadId:'T1'}, finished:{run:'run-o', statement:'s'}}]})});
  try {
    await clickAll(run, ['End run', 'End run as completed']);
    assert.deepEqual(run.calls, []);
  } finally { await run.close(); }
});

test('a start of unknown outcome and a refused start are said in the Run tab', async () => {
  const unknown = {reference:'run-u', conversation:'T1', home:'account', generation:g, source:'src', lifecycle:{state:NOT_CONFIRMED}, status:UNKNOWN};
  const ui = await mountRun({host:host(), data:data({selections:selected(), runs:[unknown]})});
  try {
    assert.match(region(ui.c, 'Run progress').textContent, /Start not confirmed — outcome unknown/);
    assert.ok(all(region(ui.c, 'Run'), 'a').some(a => a.getAttribute('href') === '#conversation'));
    assert.equal(button(ui.c, 'Prepare this run'), undefined, 'the acknowledgement and a new run are the composer\'s Start run\'s');
    await ui.rerender({data:data({selections:selected(), runs:[{...unknown, status:REFUSED}]})});
    assert.match(region(ui.c, 'Run progress').textContent, /Codex refused to start the run/);
    assert.deepEqual(ui.calls, []);
  } finally { await ui.close(); }
});

test("with App navigation, the Run tab shows the run's conversation — its requests when Codex is waiting — and nothing is sent", async () => {
  const open = {reference:'run-1', conversation:'T2', home:'account', generation:g, source:'sent', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}, status:{}};
  const ui = await mountRun({navigate:true, thread:'T2', host:host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T2'}}]}), data:data({selections:selected(), runs:[open]})});
  try {
    assert.equal(all(region(ui.c, 'Run'), 'a').filter(a => a.getAttribute('href') === '#conversation').length, 0, 'no bare scroll link that could show another conversation');
    await ui.press('Answer in the conversation');
    assert.deepEqual(ui.shown, [['T2', 'conversation-requests']]);
    // Codex reports the conversation active: the tab offers to show it.
    await ui.rerender({host:host({threads:[{threadId:'T1', generation:g, model:'invented-model', status:{type:'idle'}}, {threadId:'T2', generation:g, model:'invented-model', status:{type:'active', activeFlags:[]}}]})});
    await ui.press('Show the conversation');
    assert.deepEqual(ui.shown.at(-1), ['T2', 'conversation']);
    // Its turn ended: Reply shows the conversation too.
    await ui.rerender({host:host()});
    await ui.press('Reply');
    assert.deepEqual(ui.shown.at(-1), ['T2', 'conversation']);
    assert.deepEqual(ui.calls, [], 'navigation issues no host command');
  } finally { await ui.close(); }
});

test('conversation labels use a supplied title or preview, otherwise a session-local ordinal, never an invented title', () => {
  const {conversationLabel} = loadSrc('presentation');
  const other = {...g, spawnCounter:2};
  const view = {threads:[{threadId:'T1', generation:g, model:'m'}, {threadId:'old', generation:other, model:'m'}, {threadId:'T2', generation:g, model:'m2', preview:'Summarise the spacing notes'}, {threadId:'T3', generation:g, name:'Spacing review', preview:'ignored'}]};
  assert.equal(conversationLabel(view, view.threads[0]), 'Conversation 1 · m');
  assert.equal(conversationLabel(view, view.threads[2]), 'Summarise the spacing notes · m2');
  assert.equal(conversationLabel(view, view.threads[3]), 'Spacing review · model not reported');
  assert.equal(conversationLabel(view, {threadId:'T9', generation:g}), 'Conversation · model not reported', 'an unknown row gets no fabricated number');
  assert.match(conversationLabel(view, {...view.threads[2], preview:'x'.repeat(80)}), /^x{47}… · m2$/);
});

// Native J1 baseline facts (main 9248a36e): the last-result line showed raw
// host JSON, a newer registered revision was noted only in the studio, and Use
// labels hid the revision. The result line is each tab's GuideResult; the newer
// revision is the chip's (tests/workflow-pick-run.test.mjs).
test('the last result is in words with the reply under details, and same-name revisions are told apart in the Workflows tab', async () => {
  const ui = await mountResult({outcome:{command:'workflow_select_listed', message:'{"state":"selected","reference":"sel-1"}', failed:false, settled:true}});
  try {
    const last = region(ui.c, 'Last result');
    assert.match(last.textContent, /^Chose the workflow for this conversation\.What the App reported/, 'words first; the exact reply under details');
    assert.equal(agentBlockText(agentBlocks(last)[0]), '{"state":"selected","reference":"sel-1"}', 'the exact reply, in a marked box');
    assert.equal(all(last, 'p')[0].textContent, 'Chose the workflow for this conversation.');
    await ui.rerender({outcome:{command:'workflow_send_run', message:'Error: invented refusal text', failed:true, settled:true}});
    assert.equal(region(ui.c, 'Last result').textContent, "Couldn't start the run: invented refusal text", 'an unrecognised refusal stays in the App\'s words');
    await ui.rerender({outcome:{command:'workflow_send_run', message:'', failed:false, settled:false}});
    assert.ok(region(ui.c, 'Last result') === undefined, 'nothing is claimed before the result arrives');
  } finally { await ui.close(); }
  const twoRevisions = data({libraries:[{...data().libraries[0], registered:[
    {name:'resolve-spacing', sequence:2, revision:'rev-2-abcdef0123456789', label:'registered — selectable', selectable:true},
    {name:'resolve-spacing', sequence:3, revision:'rev-3-abcdef0123456789', label:'registered — selectable', selectable:true}]}]});
  const lib = await mountLibrary({host:host(), data:twoRevisions});
  try {
    const cards = lib.c.querySelectorAll(node => node.getAttribute('aria-label') === 'Project workflow resolve-spacing');
    assert.equal(cards.length, 2);
    const metas = cards.map(card => all(card, 'small')[0].textContent);
    assert.ok(metas.every(meta => /another revision has the same name/.test(meta)), 'same-name cards say so');
    assert.notEqual(metas[0], metas[1], 'and name their revision');
  } finally { await lib.close(); }
});

// Rows as runtime_session's run view gives them (generation, home, conversation,
// workflow{origin,name,revision,sourceRoot}); the host's runs are a map, so the
// array order is scrambled here on purpose, and order comes only from
// preparationOrder (local to one home and conversation).
const runRow = over => ({reference:'run', conversation:'T1', home:'account', generation:g, source:'s', turn:'t', compatibility:[{preparation:{declaration}}],
  workflow:{name:'resolve-spacing', origin:'project', revision:'rev-1-0123456789ab', sourceRoot:'project'}, lifecycle:{state:'ended', end:{cause:'completed'}}, ...over});
test('the Run tab orders this conversation\'s runs only by the host\'s preparationOrder, never by array position, and says when order is not known', async () => {
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const ordered = [runRow({reference:'run-b', preparationOrder:1, lifecycle:{state:'ended', end:{cause:'ended by the person'}}}), runRow({reference:'run-c', preparationOrder:2, lifecycle:{state:'ended', end:{cause:'completed'}}}),
    runRow({reference:'run-a', preparationOrder:0}), runRow({reference:'run-other', conversation:'T2', preparationOrder:5}), runRow({reference:'run-prep', preparationOrder:3, source:undefined, lifecycle:{state:PREPARED}})];
  const ui = await mountRun({host:host(), data:data({selections:selected(), runs:ordered}), navigate:true});
  try {
    const labels = () => region(ui.c, 'Runs in this conversation').querySelectorAll(node => node.localName === 'li' && (node.getAttribute('aria-label') ?? '').startsWith('Run ')).map(node => node.getAttribute('aria-label'));
    assert.deepEqual(labels(), ['Run run-c', 'Run run-b', 'Run run-a'], 'highest preparationOrder first, whatever the array order');
    assert.match(region(ui.c, 'Run progress').textContent, /Ready to start/, 'the current run is the highest order (the prepared one), not the last array row');
    assert.match(region(ui.c, 'Run run-c').textContent, /resolve-spacing \(rev-1-012345…\) · Ended as completed\..*It declares: .*report-file \(reports\/spacing\.md\)\..*the App hasn't checked them/);
    assert.equal(all(region(ui.c, 'Run run-c'), 'a').find(node => node.textContent.startsWith('Open this run\'s recorded evidence')).getAttribute('href'), `#${runEvidenceAnchor('run-c')}`);
    await React.act(async () => props(button(region(ui.c, 'Run run-c'), 'Show the conversation')).onClick());
    assert.deepEqual(ui.shown.at(-1), ['T1', undefined]);
    // Without the field, nothing is sorted and no latest run is chosen.
    await ui.rerender({data:data({selections:selected(), runs:[runRow({reference:'run-y'}), runRow({reference:'run-x', lifecycle:{state:OPEN}})]})});
    assert.deepEqual(labels(), ['Run run-y', 'Run run-x'], 'the host\'s order is kept, unsorted');
    assert.match(region(ui.c, 'Runs in this conversation').textContent, /The App doesn't know these runs' order/);
    assert.match(region(ui.c, 'Run').textContent, /several runs, and the App can't tell which one is the latest/);
    assert.ok(region(ui.c, 'Run progress') === undefined, 'no run is read as the current one');
    assert.equal(ui.calls.length, 0, 'finding results issues nothing');
  } finally { await ui.close(); }
});

test('a run from an earlier Codex session with the same thread ID is never current in the Run tab, and says where to find it', async () => {
  const g1 = g, g2 = {...g, spawnCounter:2};
  const restarted = host({generation:g2, workflowRoot:{context:{sourceRef:'src', generation:g2}}, threads:[{threadId:'T1', generation:g2, model:'invented-model', status:{type:'idle'}}]});
  const runs = [runRow({reference:'run-old', generation:g1, preparationOrder:0}), runRow({reference:'run-new', generation:g2, preparationOrder:1}), runRow({reference:'run-key-home', home:'api-key', generation:{...g2, home:'api-key'}})];
  const ui = await mountRun({host:restarted, data:data({context:{sourceRef:'src', generation:g2}, selections:selected(), runs}), navigate:true});
  try {
    assert.match(region(ui.c, 'Run').textContent, /Ended as completed/, 'the current-session run is current');
    assert.ok(region(ui.c, 'Run run-old') === undefined, 'the earlier session\'s run is not current, nor listed as this conversation\'s');
    assert.ok(region(ui.c, 'Run run-key-home') === undefined, 'another home\'s run is not listed');
    assert.ok(region(ui.c, 'Runs in this conversation') === undefined);
  } finally { await ui.close(); }
  // Its reading says where to find its conversation; the workflow studio, under More, lists it at its evidence.
  const open = runReading(runRow({reference:'run-old', generation:g1, lifecycle:{state:OPEN}}), restarted);
  assert.equal(open.title, 'Open in an earlier Codex session');
  assert.match(open.detail, /Find its conversation in History, under More\./);
});

test('after Codex restarts and the run\'s conversation is not loaded, its runs stay findable in the workflow studio', async () => {
  const {WorkflowRootPanel} = loadSrc('App');
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const g2 = {...g, spawnCounter:2};
  const runs = [{reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', workflow:{name:'resolve-spacing', origin:'project', revision:'rev-1-0123456789ab'}, lifecycle:{state:'ended', end:{cause:'completed'}}}];
  const restarted = host({generation:g2, workflowRoot:{context:{sourceRef:'src', generation:g2}}, threads:[{threadId:'T5', generation:g2, model:'invented-model', status:{type:'idle'}}]});
  const view = data({context:{sourceRef:'src', generation:g2}, runs, drafts:{drafts:[]}});
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(WorkflowRootPanel, {data:view, host:restarted, view:'make', act:async () => { throw Error('no command'); }})));
  assert.ok(c.querySelectorAll(node => node.getAttribute('id') === runEvidenceAnchor('run-1'))[0], 'the earlier run is still listed, at its evidence');
  await React.act(async () => root.unmount());
  const run = await mountRun({host:restarted, thread:'T5', data:view});
  try { assert.ok(region(run.c, 'Run progress') === undefined, 'another conversation\'s run, of an earlier session, is not the open conversation\'s'); }
  finally { await run.close(); }
});

test('an open run from an earlier Codex session never takes a same-ID conversation\'s current activity', () => {
  const g2 = {...g, spawnCounter:2};
  const oldOpen = {reference:'run-old', conversation:'same-id', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}};
  const working = host({generation:g2, threads:[{threadId:'same-id', generation:g2, status:{type:'active'}}]});
  const reading = runReading(oldOpen, working);
  assert.equal(reading.title, 'Open in an earlier Codex session');
  assert.doesNotMatch(reading.detail, /Codex is working on this run/, 'G2\'s active same-ID thread is not this run\'s work');
  const waiting = host({generation:g2, threads:[{threadId:'same-id', generation:g2, status:{type:'idle'}}], serverRequests:[{generation:g2, state:'outstanding', nativeParameters:{threadId:'same-id'}}]});
  assert.equal(runReading(oldOpen, waiting).title, 'Open in an earlier Codex session', 'G2\'s waiting request is not this run\'s question');
  assert.equal(runReading({...oldOpen, home:'api-key'}, host({threads:[{threadId:'same-id', generation:g, status:{type:'active'}}]})).title, 'Open in an earlier Codex session', 'another home\'s run is not current either');
  assert.equal(runReading({...oldOpen, generation:g2}, working).tone, 'working', 'the exact current source still reads its activity');
  const ended = runReading({...oldOpen, lifecycle:{state:'ended', end:{cause:'completed'}}}, working);
  assert.equal(ended.title, 'Ended as completed', 'historical lifecycle stays readable');
});

// Constructed source replacements over the retained host/runRow shapes above.
// Mount the Run tab: these are DOM readings/navigation boundaries, not
// direct runReading calls, native history, or a newly executed producer.
for (const [replacement, currentGeneration] of [
  ['spawn', {...g, spawnCounter:2}],
  ['App session', {...g, appSession:'constructed-new-session'}],
  ['home', {...g, home:'constructed-other-home'}],
]) test(`an open run survives ${replacement} replacement without borrowing same-ID live activity in the Run tab`, async () => {
  const original = runRow({reference:'open-original', lifecycle:{state:OPEN}, preparationOrder:0});
  const originalBytes = JSON.stringify(original);
  const snapshot = (generation, state, requests = []) => host({generation,
    workflowRoot:{context:{sourceRef:'src', generation}},
    threads:[{threadId:'T1', generation, model:'invented-model', status:{type:state}}],
    serverRequests:requests});
  const projection = (generation, runs) => data({context:{sourceRef:'src', generation}, selections:selected(), runs});
  const ui = await mountRun({navigate:true, host:snapshot(g, 'active'), data:projection(g, [original])});
  try {
    assert.match(region(ui.c, 'Run progress').textContent, /Codex reports this conversation active/);
    const replacementQuestion = {generation:currentGeneration, state:'outstanding', nativeParameters:{threadId:'T1'}};
    // The open row is unchanged while both the current source and its same-ID
    // activity are replaced. No ended result or new-run order is fabricated.
    await ui.rerender({host:snapshot(currentGeneration, 'active', [replacementQuestion]), data:projection(currentGeneration, [original])});
    assert.ok(region(ui.c, 'Run progress') === undefined, 'the old open row is not current progress');
    assert.ok(region(ui.c, 'Run open-original') === undefined, 'nor listed as the open conversation\'s run');
    assert.doesNotMatch(region(ui.c, 'Run').textContent, /Waiting for your answer|Needs answer|Working/);
    assert.equal(button(ui.c, 'Answer in the conversation'), undefined, 'cannot navigate into the replacement same-ID chat on the old run\'s account');
    assert.deepEqual(ui.calls, []); assert.deepEqual(ui.shown, [], 'replacement alone never opens or answers a conversation');
    // Positive control: a separately constructed run of the exact new source
    // can read that source's waiting/working states; it does not rebind old.
    const current = runRow({reference:'open-current', generation:currentGeneration, home:currentGeneration.home, lifecycle:{state:OPEN}, preparationOrder:1});
    await ui.rerender({data:projection(currentGeneration, [original, current])});
    assert.match(region(ui.c, 'Run progress').textContent, /Waiting for your answer/);
    assert.ok(region(ui.c, 'Run open-original') === undefined, 'the old row is still not this source\'s');
    await ui.press('Answer in the conversation');
    assert.deepEqual(ui.shown, [['T1', 'conversation-requests']]);
    await ui.rerender({host:snapshot(currentGeneration, 'active')});
    assert.match(region(ui.c, 'Run progress').textContent, /Codex reports this conversation active/);
    assert.equal(JSON.stringify(original), originalBytes, 'the retained open run was never ended or rewritten');
    assert.deepEqual(ui.calls, [], 'all these readings and navigation issue no host command');
  } finally { await ui.close(); }
});

test('project and library locations stay distinct without a matching project folder', async () => {
  const {appProjectFolder, ProjectLibraryContext} = loadSrc('WorkflowContext');
  const opaque = host({currentAppProjectContext:{reference:'opaque-project', sourceCaption:'configured App directory', standing:'s'}, workflowRoot:data()});
  assert.equal(appProjectFolder(opaque), null, 'an opaque project reference gives no folder');
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(ProjectLibraryContext, {host:opaque})));
  const shown = region(c, 'Project and opened library');
  assert.match(region(shown, 'Fixed App project display').textContent, /configured App directory; folder display unavailable/);
  assert.doesNotMatch(region(shown, 'Fixed App project display').textContent, /invented/);
  assert.match(shown.textContent, /project library · \/invented\/project/, 'the opened library is said apart from the project');
  assert.ok(all(shown, 'details').every(n => !props(n).open));
  await React.act(async () => root.render(React.createElement(ProjectLibraryContext, {host:host({currentAppProjectContext:null, workflowRoot:data()})})));
  assert.match(region(c, 'Fixed App project display').textContent, /^Unavailable — explicit App project reference not established\./, 'no project: said, and no library folder offered in its place');
  await React.act(async () => root.unmount());
  // The Run tab says only that the library location does not establish where results go.
  const run = await mountRun({host:host({currentAppProjectContext:{reference:'opaque-project'}}), data:data({selections:selected(), runs:[runRow({reference:'run-1', preparationOrder:0})]})});
  try {
    assert.match(region(run.c, 'Run').textContent, /The App has not reported a matching project folder; the library location alone does not establish output locations\./);
    assert.doesNotMatch(region(run.c, 'Run').textContent, /\/invented\/project/);
    assert.deepEqual(run.calls, []);
  } finally { await run.close(); }
});

test('raw action responses are optional while an exception stays directly readable', async () => {
  const {ActionFeedback}=loadSrc('ActionFeedback');const c=document.createElement('div');const root=createRoot(c);
  await React.act(async()=>root.render(React.createElement(ActionFeedback,{message:'workflow_send_run: {"state":"outcome unknown","request":"original"}'})));
  const details=all(c,'details')[0];assert.ok(details);assert.equal(!!props(details).open,false);
  assert.match(details.textContent,/outcome unknown.*original/);
  assert.doesNotMatch(all(c,'p')[0].textContent,/original|completed|successful/);
  await React.act(async()=>root.render(React.createElement(ActionFeedback,{message:'Could not read the current workflow source.'})));
  assert.equal(all(c,'details').length,0);assert.match(all(c,'p')[0].textContent,/Could not read/);
  await React.act(async()=>root.unmount());
});

// desktop_startup.rs DesktopSetup::adopt names this source; lib.rs host_status
// replaces the launch observation source with it after a saved desktop setup.
const SAVED = 'explicit saved desktop request, revalidated this launch';
const launchFrom = (source, root = '/invented/work-project') => ({launchAppProjectObservation:{source, nativeRoot:path(root), associationStanding:'a'}});
test('a saved desktop setup gives the project folder only when its projection matches the frozen reference', async () => {
  const {appProjectFolder} = loadSrc('WorkflowContext');
  assert.equal(appProjectFolder(host({attachmentSelections:launchFrom(SAVED)})), '/invented/work-project');
  assert.equal(appProjectFolder(host({attachmentSelections:launchFrom(SAVED, '/invented/other-project')})), null, 'a mismatched saved-desktop projection supplies no folder');
  for (const source of ['explicit saved desktop request', 'another producer', undefined])
    assert.equal(appProjectFolder(host({attachmentSelections:launchFrom(source)})), null, `unknown source ${source} supplies no folder`);
  // Where it is said: the Run tab's Details, beside what the workflow declares.
  const run = await mountRun({host:host({attachmentSelections:launchFrom(SAVED)}), data:data({selections:selected(), runs:[runRow({reference:'run-1', preparationOrder:0})]})});
  try {
    assert.match(region(run.c, 'Run').textContent, /inside the project folder \/invented\/work-project/);
    await run.rerender({host:host({attachmentSelections:launchFrom(SAVED, '/invented/other-project')})});
    assert.doesNotMatch(region(run.c, 'Run').textContent, /other-project/);
    assert.match(region(run.c, 'Run').textContent, /The App has not reported a matching project folder/);
    assert.deepEqual(run.calls, []);
  } finally { await run.close(); }
});

// Walk of the development App at main 4bb28164: a press that met a passing
// history reader failed with the host's own words under Progress, and an
// included workflow showed a library's "newer revisions can't be checked".
// The result line is each tab's GuideResult; the chosen workflow is the chip's.
test('a refused press is said in plain words only where nothing was done; the chip describes the chosen workflow and its role line', async () => {
  const busy = {command:'workflow_select_production_bundle', message:'Error: Native history context is busy; refresh the workflow choice', failed:true, settled:true};
  const ui = await mountResult({outcome:busy});
  try {
    const last = region(ui.c, 'Last result');
    assert.equal(all(last, 'p')[0].textContent, "Couldn't choose the included workflow: the App was busy reading conversation history, so nothing was done. Press the button again.");
    assert.match(last.textContent, /What the App reported/, 'the exact reply stays under details');
    assert.equal(agentBlockText(agentBlocks(last).at(-1)), 'Native history context is busy; refresh the workflow choice', 'the exact reply, in a marked box');
    assert.equal(last.getAttribute('role'), 'alert');
    // The App's own refusal before any host command is issued.
    await ui.rerender({outcome:{command:'workflow_open_project_library', message:'Error: Workflow source or chat changed; refresh the displayed choice before acting', failed:true, settled:true}});
    assert.match(region(ui.c, 'Last result').textContent, /^Couldn't show this project's workflows: the conversation chosen here is no longer open in this view, so nothing was done\. Choose the conversation again/);
    // Plain words only for the exact message from a command that checks first.
    // A start refused after its records were written is never "nothing was done".
    for (const [command, message] of [
      ['workflow_send_run', 'refused-not-sent: turn/start generation changed before request registration'],
      ['workflow_send_run', 'Workflow native generation changed; refresh the displayed choice'],
      ['workflow_end_run', 'Native history context is busy; refresh the workflow choice'],
      ['workflow_prepare_run', 'Workflow App source changed; nothing selected or prepared'],
      ['workflow_prepare_run', 'the Native history context is busy; refresh the workflow choice, later'],
    ]) {
      await ui.rerender({outcome:{command, message:`Error: ${message}`, failed:true, settled:true}});
      const words = region(ui.c, 'Last result').textContent;
      assert.ok(words.includes(message), `${command}: the App's own words are shown`);
      assert.doesNotMatch(words, /nothing was done|nothing was changed|nothing was sent|Press the button again/, `${command}: ${message}`);
    }
    await ui.rerender({outcome:{command:'workflow_send_run', message:'Error: refused-not-sent: turn/start generation changed before request registration', failed:true, settled:true}, only:['workflow_send_run']});
    assert.equal(region(ui.c, 'Last result').textContent, "Couldn't start the run: refused-not-sent: turn/start generation changed before request registration", 'a failed start points nowhere');
  } finally { await ui.close(); }

  // The chip, for an included workflow chosen for the conversation: its source and revision, and its role line.
  const included = {kind:'workflow', origin:'bundled', source_root:'invented-library:library-v9.9.9', name:'coordinated-knowledge-work', revision:'3730d84debb5aa', revision_method:'invented/v1', derived_from:null};
  const bundled = [{...selected()[0], selection:{...selected()[0].selection, identity:included,
    newerRevision:{limit:"the selection's library is not open in this App session; newer revisions not read"}}}];
  const catalogue = (source, over = {}) => ({standing:'s', ...(source ? {source} : {}), entries:[{name:included.name, revision:included.revision, identity:included, runnable:true, ...over}]});
  const pickOf = view => pickIncluded(view.productionCatalog.entries[0], view.productionCatalog, host());
  const first = data({selections:bundled, productionCatalog:catalogue({tag:'library-v9.9.9'})});
  const chip = await mountChip({host:host(), data:first, pick:pickOf(first)});
  try {
    assert.doesNotMatch(chip.c.textContent, /can't be checked/, 'an included workflow has no library revisions to follow');
    assert.match(region(chip.c, 'Workflow picked').textContent, /^coordinated-knowledge-work.*Chirality Library 9\.9\.9/, 'the source of an included workflow');
    assert.doesNotMatch(region(chip.c, 'Workflow picked').textContent, /3730d84debb5/, 'its digest is not on the chip; Details holds it');
    assert.match(chip.c.textContent, /3730d84debb5/, 'and is still shown, in Details');
    assert.ok(region(chip.c, 'Text of coordinated-knowledge-work'), 'its text can be read from the chip');
    const roleLine = () => region(chip.c, "Role and the workflow's listed roles");
    assert.ok(roleLine() === undefined, 'no roles listed, no role line');
    await chip.rerender({data:data({selections:bundled, productionCatalog:catalogue({tag:'library-v9.9.9'}, {roles:['TASK', 'WORKING_ITEMS']})})});
    assert.equal(roleLine().textContent, "This conversation's role is not known to this App process. The Library lists coordinated-knowledge-work for: TASK, WORKING_ITEMS.", 'a conversation row with no role established by the App');
    await chip.rerender({host:host({threads:[{threadId:'T1', generation:g, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:'HELP_HUMAN', supply_ref:'sup:1'}}, {threadId:'T2', generation:g, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:'TASK'}}]})});
    assert.equal(roleLine().textContent, 'This conversation is in the role HELP_HUMAN. The Library lists coordinated-knowledge-work for: TASK, WORKING_ITEMS.', 'the conversation\'s own role, not another conversation\'s');
    // Review round 1: the development holding copy also has the bundled origin, with another source root. It is not the
    // included workflow picked, so the chip says nothing of it as the pick's selection.
    await chip.rerender({host:host(), data:data({selections:[{...bundled[0], selection:{...bundled[0].selection, identity:{...included, source_root:'chirality-root', revision:'1b1733864cd8aa'}}}], productionCatalog:catalogue({tag:'library-v9.9.9'}, {roles:['TASK']})})});
    assert.ok(roleLine() === undefined, 'a selection that is not the catalogue entry picked gets no role line');
    assert.match(chip.c.textContent, /Press Start run to see the tools it needs/, 'nor any of the selection\'s facts');
  } finally { await chip.close(); }
  // A library workflow still says when newer revisions could not be read.
  const limited = [{...selectedHere()[0], selection:{...selectedHere()[0].selection, newerRevision:{limit:'library busy; newer revisions not read now'}}}];
  const project = await mountChip({host:host(), data:data({selections:limited}), pick:projectPick()});
  try { assert.match(project.c.textContent, /Newer revisions of resolve-spacing can't be checked: library busy; newer revisions not read now/); }
  finally { await project.close(); }
});

test('a prepared run the host did not send says in the Run tab what happened in plain words and then the host\'s own recovery text', async () => {
  const unsent = (state, limit, retry) => ({reference:'run-1', conversation:'T1', home:'account', generation:g, preparationOrder:0, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{sent:false, state, limit, ...(retry ? {retry} : {})}});
  const ui = await mountRun({host:host(), data:data({selections:selected(), runs:[unsent('WR pre-send publication failed; nothing sent', 'nothing written: no records store', 'Retry publishes the same original records; sending stays a separate once-only step')]})});
  try {
    assert.equal(region(ui.c, 'Run progress').textContent.replace(/^Not started\./, '').trim().startsWith("Nothing was sent. The App couldn't finish saving the run's record. What the App says to do: Retry publishes the same original records; sending stays a separate once-only step. The App reported: WR pre-send publication failed; nothing sent: nothing written: no records store"), true);
    for (const [state, what] of [
      ['generated supporting files changed or unavailable; nothing sent', /Nothing was sent\. The App couldn't verify the copy of the workflow's supporting files that this run was prepared with\./],
      ['selected revision source changed or unavailable; nothing sent', /Nothing was sent\. The App couldn't verify the chosen workflow for this run\./],
      ['workflow approval changed since preparation; nothing sent', /Nothing was sent\. The App couldn't apply the same workflow approval it applied when you prepared this run\./],
    ]) {
      await ui.rerender({data:data({selections:selected(), runs:[unsent(state, 'invented cause', 'invented host recovery text')]})});
      const progress = region(ui.c, 'Run progress').textContent;
      assert.match(progress, what, state); assert.match(progress, /What the App says to do: invented host recovery text\. The App reported: /, 'the next action is the host\'s own');
      assert.doesNotMatch(region(ui.c, 'Run').textContent, /Prepare the run again|Start the run again|Choose the workflow again/, 'the tab prescribes nothing the host did not');
    }
    await ui.rerender({data:data({selections:selected(), runs:[unsent('a state the guide does not know', 'invented cause')]})});
    const unknown = region(ui.c, 'Run progress').textContent;
    assert.match(unknown, /^Not started\. The App reports that this run was not sent\. The App reported: a state the guide does not know: invented cause/);
    assert.doesNotMatch(unknown, /Nothing was sent\.|What the App says to do/, 'an unknown state is given no words the host did not establish');
    assert.deepEqual(ui.calls, []);
  } finally { await ui.close(); }
});

// Review rounds 1 and 2 of pull request 241, the question asked of every
// result: can something not observed, or failed, come out as done?
test('a result line says only what the command established', () => {
  assert.equal(guideResultWords({command:'workflow_end_and_start', message:'{"start":{"state":"successor not started"}}', failed:false, settled:true}), null, 'an unnamed command\'s reply is never called done');
  assert.equal(guideResultWords({command:'workflow_prepare_run', message:'', failed:false, settled:false}), null, 'a press whose result has not arrived claims nothing');
  const bundle = message => guideResultWords({command:'workflow_select_production_bundle', message, failed:false, settled:true}).words;
  assert.equal(bundle('{"state":"selected","choiceChat":{"sourceRef":"src","threadId":"T1"}}'), 'Chose the included workflow for this conversation.');
  assert.equal(bundle('{"state":"selected","choiceChat":null}'), 'Opened the included workflow to read. Nothing was chosen for a conversation.', 'the studio\'s inspection with no conversation is not a choice');
  for (const reply of ['{"state":"selected"}', 'not json', '']) assert.equal(bundle(reply), 'The App accepted this. The Workflow step shows what is chosen for the conversation.', `a reply that does not say which: ${reply}`);
  assert.equal(guideResultWords({command:'workflow_open_project_library', message:'{}', failed:false, settled:true}).words, "Opened this project's workflow library.", 'opening the library is not having listed it');
});

// Review rounds 2 and 3 of pull request 241: after a start that succeeded, a
// view from before the press read "Ready to start", "Nothing has been sent
// yet" and offered Start again; with a marker set, other steps still showed
// cached states as current. The Run tab holds the run now.
test('while its view may be from before the last press, the Run tab shows none of the run and offers nothing', async () => {
  const preparedRun = {reference:'run-1', conversation:'T1', home:'account', generation:g, preparationOrder:0, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{}};
  const open = {...preparedRun, source:'s', lifecycle:{state:OPEN}};
  const earlier = {reference:'run-0', conversation:'T1', home:'account', generation:{...g, spawnCounter:0}, source:'s', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}};
  const ended = {command:'workflow_end_run', message:'{"state":"ended by the person"}', failed:false, settled:true};
  const ui = await mountRun({data:data({selections:selected(), runs:[open, earlier]}), host:host(), outcome:ended, navigate:true});
  try {
    assert.ok(button(ui.c, 'End run'), 'the view alone offers End run');
    assert.match(region(ui.c, 'Run progress').textContent, /^Open/);
    await ui.rerender({viewStale:true});
    const section = region(ui.c, 'Run');
    assert.match(section.textContent, /^What this view showed may be from before the App's last operation finished\. The App is not showing its steps until it has read its state again after that; it reads again by itself\./);
    assert.doesNotMatch(section.textContent, /The last read failed/, 'no failure is said when no read failed');
    assert.ok(region(ui.c, 'Run — last result'), 'the press\'s own result stays');
    assert.deepEqual(all(section, 'button').map(node => node.textContent), [], 'no end or other control is offered');
    assert.doesNotMatch(section.textContent, /Ready to start|has not been sent|Nothing has been sent yet|Open —|Working|resolve-spacing/, 'nothing cached is shown as current, earlier runs included');
    // A status read that failed since is said in the tab itself, where the person is looking.
    await ui.rerender({readFailure:'Error: invented status failure'});
    assert.match(region(ui.c, 'Run').textContent, /it reads again by itself\.The last read failed: Error: invented status failure/);
    // While the press is still in progress the run stays, its controls disabled, and its result is not yet said.
    await ui.rerender({readFailure:null, busy:true});
    assert.ok(region(ui.c, 'Run — last result') === undefined, 'no result is claimed beside a run read from before the press');
    for (const node of all(region(ui.c, 'Run'), 'button')) if (!/Show the conversation|Answer|Reply/.test(node.textContent)) assert.equal(props(node).disabled, true, `${node.textContent} is disabled while the press is in progress`);
    await ui.rerender({busy:false, viewStale:false, data:data({selections:selected(), runs:[preparedRun]})});
    assert.match(region(ui.c, 'Run progress').textContent, /Ready to start/, 'once a read started after the press is applied, the run is shown again');
    assert.ok(region(ui.c, 'Run — last result'));
    assert.deepEqual(ui.calls, []);
  } finally { await ui.close(); }
});

test('a library folder the App could not list is said in the Workflows tab where the list would be', async () => {
  const base = data().libraries[0];
  const unavailable = {...base, entryListing:{state:'unavailable', reference:'listing-2', libraryRef:'lib:project', entries:[], limits:['library entry folder unreadable: invented cause']}};
  const ui = await mountLibrary({host:host(), data:data({libraries:[unavailable]})});
  try {
    assert.match(region(ui.c, 'Workflows').textContent, /The App couldn't look in this library's folder for other workflows: library entry folder unreadable: invented cause/);
    assert.ok(region(ui.c, 'Project workflow draft-free-entry') === undefined, 'no entry to review is offered');
  } finally { await ui.close(); }
});

// Each reading of an open run says what Codex reported for this conversation and nothing that would follow from it.
test('an open run is read from what Codex reported for its conversation and no more', () => {
  const run = {conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}};
  const reading = (row, extra = {}) => runReading(run, host({threads:row ? [{threadId:'T1', generation:g, ...row}] : [], ...extra}));
  // Idle is Codex's report for this conversation; it is not a claim that nothing is working (a delegated agent may be).
  const idle = reading({status:{type:'idle'}, statusSource:{method:'thread/status/changed', receiptPosition:9}});
  assert.equal(idle.tone, 'idle'); assert.equal(idle.title, 'Open — Codex reports this conversation idle');
  assert.match(idle.detail, /says nothing about agents it delegated work to/);
  assert.doesNotMatch(idle.title + idle.detail, /not working/);
  assert.equal(reading({status:{type:'idle'}}).title, 'Open — Codex reports this conversation idle', 'the admission reply is Codex\'s report too');
  // A status that was never reported, cannot be read, or is not one the guide knows says nothing.
  for (const row of [{}, {status:null}, {status:{type:'notLoaded'}}, {status:{type:'invented'}}, {status:'idle'}, null]) {
    const unknown = reading(row);
    assert.equal(unknown.tone, 'uncertain', JSON.stringify(row)); assert.equal(unknown.title, 'Open — what Codex is doing is not known');
    assert.doesNotMatch(unknown.title + unknown.detail, /idle|Working|waiting/);
  }
  const limited = reading({status:null, statusSource:{method:'thread/status/changed', receiptPosition:9, limit:'the notification does not match the pinned ThreadStatusChangedNotification; status unknown'}});
  assert.match(limited.detail, /The App cannot establish what Codex is doing in this conversation: the notification does not match the pinned ThreadStatusChangedNotification; status unknown\./);
  // A report that was received but could not be ordered against the admission reply is said as that, not as "nothing readable".
  const unordered = reading({status:null, statusSource:{method:'thread/status/changed', limit:'a status report was received for this conversation and its order relative to the admission reply is not established; status unknown'}});
  assert.match(unordered.detail, /cannot establish what Codex is doing in this conversation: a status report was received for this conversation and its order relative to the admission reply is not established/);
  assert.doesNotMatch(unordered.detail, /no status from Codex|has not reported/);
  assert.match(reading({status:{type:'notLoaded'}}).detail, /: Codex reports the conversation as not loaded\./);
  assert.match(reading({}).detail, /: it holds no status from Codex for it that it can read\./);
  // The end of the App's observation: the last status seen is not a reading, and nothing is claimed about Codex's process.
  for (const [row, extra] of [[{status:null, lastObservedStatus:{type:'active', activeFlags:[]}, statusObservationEnded:true}, {}], [{status:{type:'idle'}}, {generationClosed:true}], [{status:{type:'active', activeFlags:[]}}, {generationClosed:true}], [{status:{type:'idle'}, statusObservationEnded:true}, {}]]) {
    const ended = reading(row, extra);
    assert.equal(ended.tone, 'uncertain', JSON.stringify([row, extra])); assert.equal(ended.title, 'Open — the App is no longer receiving from Codex');
    assert.match(ended.detail, /no longer receiving from the Codex process this run was in/);
    assert.doesNotMatch(ended.title + ended.detail, /Codex has stopped|has ended|exited/);
  }
  // Active is working; active with a waiting flag is Codex's own word that it waits, before any request has reached the App.
  assert.equal(reading({status:{type:'active', activeFlags:[]}}).tone, 'working');
  for (const flag of ['waitingOnApproval', 'waitingOnUserInput']) {
    const waits = reading({status:{type:'active', activeFlags:[flag]}});
    assert.equal(waits.tone, 'waiting', flag); assert.equal(waits.title, 'Codex reports it is waiting for an approval or an answer');
    assert.match(waits.detail, /The request appears in the conversation once the App has received it\./);
    assert.notEqual(waits.title, 'Working');
  }
});

test('a run recorded open in an earlier Codex session carries the uncertain tone its words describe', () => {
  const reading = runReading({reference:'run-old', conversation:'same-id', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}}, host({generation:{...g, spawnCounter:2}, threads:[{threadId:'same-id', generation:{...g, spawnCounter:2}, status:{type:'idle'}}]}));
  assert.equal(reading.title, 'Open in an earlier Codex session'); assert.equal(reading.tone, 'uncertain');
});

// Each reading says what Codex reported for the conversation and nothing that would follow from it.
test('the waiting, active and starting readings claim no more than was reported', () => {
  const open = {conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}};
  const waiting = runReading(open, host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]}));
  assert.equal(waiting.detail, 'Codex is asking a question or approval in the conversation. Answer it there.');
  assert.doesNotMatch(waiting.detail, /Nothing continues/, 'one outstanding request says nothing of other work in progress');
  const active = runReading(open, host({threads:[{threadId:'T1', generation:g, status:{type:'active', activeFlags:[]}}]}));
  assert.deepEqual([active.tone, active.title, active.detail], ['working', 'Open — Codex reports this conversation active', 'Codex last reported this conversation as active. Follow its progress in the conversation.']);
  assert.doesNotMatch(`${active.title} ${active.detail}`, /is working on this run|^Working/, 'a last report of active is not a claim that work is being done on the run');
  const starting = runReading({conversation:'T1', source:'sent', lifecycle:{state:PREPARED}}, host());
  assert.equal(starting.detail, "The App has issued the starting message and is waiting for Codex's reply. The run opens when Codex confirms the starting turn.");
  assert.doesNotMatch(starting.detail, /when that reply is observed/, 'a refusal is also a reply, and it does not open the run');
  assert.doesNotMatch(starting.detail, /was sent/, 'a source is the App issuing the message; Codex receiving it is not established until its reply');
});

test('an open run says each error notice the App holds with its turn and that turn\'s status, and compares no turns', async () => {
  const run = {reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}, workflow:{name:'resolve-spacing', origin:'project', revision:'r'}, status:{}};
  // The case observed against an unreachable model: a conversation Codex reports active whose only news is its retry notice.
  // Every notice has its own words, by its order of receipt, so that saying the wrong notice of a turn fails.
  const words = order => `Reconnecting... ${order} — Connection failed: error sending request`;
  const notice = (turnId, observedOrder, extra = {}) => ({threadId:'T1', turnId, generation:g, error:{message:`Reconnecting... ${observedOrder}`, additionalDetails:'Connection failed: error sending request'},
    willRetry:true, receiptPosition:observedOrder, ordinalInTurn:1, observedOrder, turnFirstObservedOrder:observedOrder, laterFrameForTurn:false, standing:'live-observed', ...extra});
  // The host's view: the notices, the turns it holds (a row with the turn's id, and separately which conversation holds a turn of that id), and its item rows.
  const held = (id, status, startedAt, threadId = 'T1') => ({record:{threadId, turnId:id}, turn:{id, status, startedAt}});
  const item = (turnId, observedOrder, extra = {}) => ({threadId:'T1', turnId, native:{id:`m-${observedOrder}`, type:'agentMessage'}, standing:'live-observed', observedOrder, ...extra});
  const view = (turnErrors, turns = [], items = []) => ({turnErrors, turnRecords:turns.map(t => t.record), turns:turns.map(t => t.turn), items});
  const activeHost = (nativeView, over = {}) => host({threads:[{threadId:'T1', generation:g, status:{type:'active', activeFlags:[]}}], nativeView, ...over});
  const said = (nativeView, over) => runTurnNotices(run, activeHost(nativeView, over));
  const RETRY = 'Codex said it will retry.';
  const one = (turnId, turnStatus, order, over = {}) => ({turnId, words:words(order), retry:RETRY, count:1, turnStatus, ...over});
  assert.deepEqual(said(view([])), []); assert.deepEqual(runTurnNotices(run, host()), [], 'no native view, no notice');

  // One form: the turn's latest notice, with the status the App holds for that same turn, whatever it is.
  assert.deepEqual(said(view([notice('B', 40), notice('B', 41, {ordinalInTurn:2})], [held('B', 'inProgress', 200)])), [one('B', 'inProgress', 41, {count:2})]);
  assert.deepEqual(said(view([notice('B', 41, {ordinalInTurn:2}), notice('B', 40)], [held('B', 'inProgress', 200)])), [one('B', 'inProgress', 41, {count:2})], 'the last received, wherever it stands in the host\'s list');
  for (const status of ['completed', 'failed', 'interrupted'])
    assert.deepEqual(said(view([notice('B', 40)], [held('B', status, 200)])), [one('B', status, 40)], `a turn the App holds as ${status} with no later frame naming it: said with that status, not hidden and not inferred to be over`);
  assert.deepEqual(said(view([notice('A', 40)])), [one('A', null, 40)], 'the App holds no status for the turn, and says none');
  assert.equal(said(view([notice('B', 40, {willRetry:false})]))[0].retry, 'Codex said it will not retry.');
  assert.equal(said(view([notice('B', 40, {willRetry:undefined})]))[0].retry, 'Codex did not say whether it will retry.');
  assert.equal(said(view([notice('B', 90, {ordinalInTurn:33})]))[0].count, 33, 'what the host accepted for that turn, which can exceed the 32 it keeps');
  // The status is what the App holds from Codex's reports, not "the last reported": the host keeps a reported end over a later stale report of progress.
  assert.equal(turnStatusWords(null), ''); assert.equal(turnStatusWords('inProgress'), 'The App holds Codex\'s report of that turn as in progress.');
  assert.equal(turnStatusWords('paused'), 'The App holds Codex\'s report of that turn as “paused”.', 'a status the App does not know is quoted, not interpreted');
  for (const status of ['inProgress', 'completed', 'failed', 'interrupted', 'paused']) assert.doesNotMatch(turnStatusWords(status), /last|latest|now|still/);

  // A status is this conversation's turn's only where the host's report ties it: one record of that id, this conversation's, and one row of that id.
  assert.deepEqual(said(view([notice('A', 40)], [held('A', 'completed', 100, 'T2')])), [one('A', null, 40)], 'another conversation\'s turn of that id is not this turn');
  const shared = {turnErrors:[notice('U', 40)], turnRecords:[{threadId:'T2', turnId:'U'}, {threadId:'T1', turnId:'U'}], turns:[{id:'U', status:'completed', startedAt:100}, {id:'U', status:'inProgress', startedAt:100}], items:[]};
  assert.deepEqual(said(shared), [one('U', null, 40)], 'two conversations hold a turn of that id: the rows cannot be told apart, so no status is said');
  assert.deepEqual(said({...shared, turnRecords:[...shared.turnRecords].reverse()}), [one('U', null, 40)], 'in either order: the lists are not paired by position');
  assert.deepEqual(said({...shared, turns:[shared.turns[0]]}), [one('U', null, 40)], 'two records and one row');
  assert.deepEqual(said({...shared, turnRecords:[shared.turnRecords[1]]}), [one('U', null, 40)], 'one record and two rows');
  assert.deepEqual(said({...shared, turnRecords:[shared.turnRecords[1]], turns:[shared.turns[1]]}), [one('U', 'inProgress', 40)], 'one record, this conversation\'s, and one row');

  // Left out only on evidence about that same turn.
  assert.deepEqual(said(view([notice('B', 40, {laterFrameForTurn:true})], [held('B', 'inProgress', 200)])), []);
  assert.deepEqual(said(view([notice('B', 40, {observationEnded:true})], [held('B', 'inProgress', 200)])), []);
  assert.deepEqual(said(view([notice('B', 40)], [held('B', 'inProgress', 200)]), {generationClosed:true}), []);
  assert.deepEqual(said(view([notice('B', 40), notice('B', 41, {ordinalInTurn:2, laterFrameForTurn:true})])), [], 'the turn\'s latest notice decides, by order of receipt within that one turn');

  // No comparison between turns. Each of the cases the earlier reviews reproduced gives the attributed notice, and nothing about another turn changes it.
  const compared = [
    [view([notice('A', 40)], [held('A', 'inProgress', 100), held('B', 'inProgress', 200)]), [one('A', 'inProgress', 40)], 'another held turn with a later start time'],
    [view([notice('A', 30), notice('A', 41, {ordinalInTurn:2})], [held('A', 'inProgress', 100), held('B', 'inProgress', 200)], [item('B', 35)]), [one('A', 'inProgress', 41, {count:2})], 'a retry received after another turn\'s frame'],
    [view([notice('A', 30), notice('A', 41, {ordinalInTurn:2})], [held('A', 'inProgress', 100)], [item('B', 35)]), [one('A', 'inProgress', 41, {count:2})], 'another turn known only by a live item'],
    [view([notice('B', 40)], [held('A', 'completed', 100), held('B', 'inProgress', 200)], [item('A', 45)]), [one('B', 'inProgress', 40)], 'a late frame for another turn'],
    [view([notice('A', 35)], [], [item('A', 30)]), [one('A', null, 35)], 'a turn known only by its items and its notice'],
    [view([notice('A', 40)], [held('A', 'inProgress', 100)], [item('B', 45, {standing:'recovered-from-supplier'})]), [one('A', 'inProgress', 40)], 'another turn known only from a history read\'s row'],
    [view([notice('A', 40)], [held('A', 'inProgress', null), held('B', 'inProgress', 100)]), [one('A', 'inProgress', 40)], 'start times, present or missing, are not read'],
  ];
  for (const [nativeView, expected, why] of compared) assert.deepEqual(said(nativeView), expected, why);
  // Two turns with a notice each: both are said, each with its own turn, in the order the host lists them. Neither is called the latest.
  assert.deepEqual(said(view([notice('B', 40), notice('A', 50)], [held('A', 'inProgress', 100), held('B', 'inProgress', 200)])), [one('B', 'inProgress', 40), one('A', 'inProgress', 50)]);
  assert.deepEqual(said(view([notice('A', 50), notice('B', 40)], [held('A', 'inProgress', 100), held('B', 'inProgress', 200)])), [one('A', 'inProgress', 50), one('B', 'inProgress', 40)]);

  // Never another conversation's notice, another Codex session's, one naming no session or no turn, or for a run not open in the current source.
  const g2 = {...g, spawnCounter:2};
  assert.deepEqual(said(view([{...notice('A', 40), threadId:'T2'}])), []);
  assert.deepEqual(said(view([{...notice('A', 40), generation:g2}])), []);
  assert.deepEqual(said(view([{...notice('A', 40), generation:undefined}])), []);
  assert.deepEqual(said(view([{...notice('A', 40), turnId:''}])), []);
  assert.deepEqual(runTurnNotices({...run, generation:g2}, activeHost(view([notice('A', 40)]))), [], 'a run of an earlier Codex session');
  assert.deepEqual(runTurnNotices({...run, lifecycle:{state:PREPARED}}, activeHost(view([notice('A', 40)]))), []);

  // In the Run tab, each case asserts what is shown.
  const LABEL = 'Error notices the App holds for this conversation', LAST = 'The conversation\'s activity shows each notice the App has kept, with its turn.';
  const STATUS = {inProgress:'in progress', completed:'completed', failed:'failed', interrupted:'interrupted'};
  const ui = await mountRun({host:activeHost(view([notice('B', 40), notice('B', 41, {ordinalInTurn:2})], [held('A', 'completed', 100), held('B', 'inProgress', 200)])), data:data({selections:selected(), runs:[run]})});
  const notices = () => region(ui.c, LABEL), lines = () => all(notices(), 'p').map(p => p.textContent);
  const line = n => `The App holds an error notice from Codex for turn ${n.turnId} of this conversation${n.count > 1 ? `; it is the latest of ${n.count} for that turn` : ''}: ${n.words} ${n.retry}${n.turnStatus ? ` The App holds Codex's report of that turn as ${STATUS[n.turnStatus]}.` : ''}`;
  assert.deepEqual(lines(), ['The App holds an error notice from Codex for turn B of this conversation; it is the latest of 2 for that turn: Reconnecting... 41 — Connection failed: error sending request Codex said it will retry. The App holds Codex\'s report of that turn as in progress.', LAST]);
  // A held notice with its turn, not an alert on the run: a note, no alert and no live region on it, in it or around it up to the tab, and outside the state box and its marking.
  const noteLike = () => {
    assert.equal(props(notices()).role, 'note'); assert.doesNotMatch(String(props(notices()).className ?? ''), /alert|fail|error|warn/, 'no alert or failure marking');
    const live = node => { const p = props(node) ?? {}; return p.role === 'alert' || p.role === 'status' || p['aria-live'] !== undefined; };
    assert.equal(live(notices()), false); assert.equal(notices().querySelectorAll(live).length, 0, 'nothing inside the note is announced as it changes');
    for (let node = notices().parentNode; node && node !== ui.c; node = node.parentNode) assert.equal(live(node), false, 'no live region around the note');
    assert.equal(ui.c.querySelectorAll(node => props(node)?.role === 'alert').length, 0);
    for (const box of ['Run state', 'Run progress']) {
      assert.ok(region(ui.c, box).querySelectorAll(node => node === notices()).length === 0, `not inside ${box}`);
      assert.doesNotMatch(region(ui.c, box).textContent, /error notice|Reconnecting/, 'the notice is no part of the run\'s state');
    }
  };
  noteLike();
  assert.match(region(ui.c, 'Run progress').textContent, /^Open — Codex reports this conversation active\./, 'the state Codex reported stays as reported');
  // The App's own words conclude nothing about the run, claim no absence and name no turn as current or latest.
  const CLAIMS = /latest turn|current|most recent|last reported|still|now\b|can't reach|stopped|recovered|No later|no other record|does not hold|cannot establish|earlier turn|later turn/i;
  const ownWords = () => lines().join(' ').replace(/Reconnecting\.\.\. \d+ — Connection failed: error sending request/g, '');
  assert.doesNotMatch(ownWords(), CLAIMS);
  // Each reproduced case shows the attributed line, and none claims currency.
  for (const [nativeView, expected, why] of compared) {
    await ui.rerender({host:activeHost(nativeView)});
    assert.deepEqual(lines(), [...expected.map(line), LAST], why);
    assert.doesNotMatch(ownWords(), CLAIMS, why); noteLike();
  }
  // Every status the App can hold for the turn, as shown; an end is said as held, with no alert even where Codex said it will not retry.
  for (const status of ['completed', 'interrupted', 'failed']) {
    await ui.rerender({host:activeHost(view([notice('B', 40, {willRetry:false})], [held('B', status, 200)]))});
    assert.deepEqual(lines(), [`The App holds an error notice from Codex for turn B of this conversation: ${words(40)} Codex said it will not retry. The App holds Codex's report of that turn as ${status}.`, LAST]);
    noteLike();
  }
  // Two conversations hold a turn of that id: no status sentence, and the rest of the line unchanged.
  await ui.rerender({host:activeHost(shared)});
  assert.deepEqual(lines(), [`The App holds an error notice from Codex for turn U of this conversation: ${words(40)} ${RETRY}`, LAST]);
  assert.doesNotMatch(lines().join(' '), /report of that turn|completed|in progress/);
  // Two turns: two lines, each with its turn.
  await ui.rerender({host:activeHost(view([notice('B', 40), notice('A', 50)], [held('B', 'inProgress', 200)]))});
  assert.deepEqual(lines(), [line(one('B', 'inProgress', 40)), line(one('A', null, 50)), LAST]);
  noteLike();
  // Evidence about the turn itself: nothing is shown.
  for (const nativeView of [view([notice('B', 41, {laterFrameForTurn:true})], [held('B', 'inProgress', 200)]), view([notice('B', 41, {observationEnded:true})]), view([])]) {
    await ui.rerender({host:activeHost(nativeView)});
    assert.equal(notices(), undefined);
  }
  await ui.close();
});
