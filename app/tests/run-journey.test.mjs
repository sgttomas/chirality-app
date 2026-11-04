import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// J1 guided path over the workflow studio's existing state and commands.
// Controlled host views only: no native App, supplier, model or person act.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {RunWorkflowGuide, runReading} = loadSrc('RunJourney');
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

async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = []; let thread = view.thread ?? ''; let text = '';
  const shown = [];
  const render = () => root.render(React.createElement(RunWorkflowGuide, {data:view.data, host:view.host, thread, busy:false, text, showConversation:view.navigate ? (id, target) => shown.push([id, target]) : undefined,
    chooseThread:value => { thread = value; calls.push({choose:value}); render(); }, setText:value => { text = value; render(); },
    act:async (command, args) => { calls.push({command, args}); }, outcome:view.outcome ?? null}));
  await React.act(async () => render());
  return {c, calls, shown, press:async label => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); },
    type:async value => { const area = all(c, 'textarea')[0]; await React.act(async () => props(area).onChange({target:{value}})); },
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); }};
}

test('run readings keep waiting, working, failed, interrupted-start and finished distinct', () => {
  const h = host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]});
  assert.equal(runReading({conversation:'T1', source:'s', lifecycle:{state:OPEN}}, h).tone, 'waiting');
  assert.equal(runReading({conversation:'T2', source:'s', lifecycle:{state:OPEN}}, host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}],
    threads:[{threadId:'T2', generation:g, status:{type:'active'}}]})).tone, 'working', 'another conversation\'s request is not this run\'s question');
  assert.equal(runReading({conversation:'T1', source:'s', lifecycle:{state:OPEN}}, host({serverRequests:[{state:'answered', nativeParameters:{threadId:'T1'}}]})).tone, 'idle');
  assert.equal(runReading({conversation:'T1', source:'s', lifecycle:{state:OPEN}}, host({threads:[{threadId:'T1', generation:g, status:{type:'systemError'}}]})).tone, 'failed');
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

test('before Codex or a project is available the next step names a concrete action and issues nothing', async () => {
  const ui = await mount({host:host({state:'absent', generation:null}), data:data({projectLibraryAvailable:false, activeLibrary:null})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: Connect Codex first/);
  assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#desktop-setup'), 'no project names Desktop setup');
  assert.equal(button(ui.c, 'Show this project\'s workflows'), undefined);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true);
  await ui.rerender({host:host(), data:data({projectLibraryAvailable:false, activeLibrary:null})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: No project folder is set\. Choose one in Desktop setup; it applies the next time you open the App\./);
  assert.deepEqual(ui.calls, []);
});

test('an existing registered workflow is found, chosen for a conversation and prepared then started with the person\'s text', async () => {
  const ui = await mount({host:host(), data:data({activeLibrary:null})});
  await ui.press('Show this project\'s workflows');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_open_project_library', args:{}});
  await ui.rerender({data:data()});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: Choose the conversation that will run the workflow/);
  assert.equal(props(button(ui.c, 'Use resolve-spacing')).disabled, true, 'a selection needs the conversation that keeps it');
  assert.equal(button(ui.c, 'Use old-method'), undefined, 'a non-selectable revision offers no Use');
  assert.match(region(ui.c, 'Workflows ready to use').textContent, /store copy missing/);
  const select = all(ui.c, 'select')[0]; await React.act(async () => props(select).onChange({target:{value:'T1'}}));
  await ui.press('Use resolve-spacing');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_select_listed', args:{libraryRef:'lib:project', name:'resolve-spacing', revision:'rev-2-abcdef0123456789'}});
  await ui.rerender({data:data({selections:selected()})});
  assert.match(region(ui.c, 'Workflow chosen for this run').textContent, /resolve-spacing — project library, revision 2 rev-2-abcdef….*Ready to run/);
  const needs = region(ui.c, 'What this workflow needs').textContent;
  for (const name of ['run', 'spacing-limit', 'supports-table']) assert.ok(needs.includes(name), name);
  await ui.type('Use the invented north wing spacing limit of 3 m.');
  await ui.press('Prepare this run');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_prepare_run', args:{generation:g, threadId:'T1', personText:'Use the invented north wing spacing limit of 3 m.'}});
  const prepared = {reference:'run-1', conversation:'T1', home:'account', generation:g, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{sent:false}, compatibility:[{preparation:{declaration}}]};
  await ui.rerender({data:data({selections:selected(), runs:[prepared]})});
  assert.equal(button(ui.c, 'Prepare this run'), undefined);
  assert.match(region(ui.c, 'Run progress').textContent, /Ready to start/);
  await ui.press('Start the run');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_send_run', args:{runRef:'run-1'}});
  const results = region(ui.c, 'Where the results go').textContent;
  assert.match(results, /report-file — declared path reports\/spacing\.md: The written report/);
  const guide = region(ui.c, 'Run a workflow').textContent;
  assert.match(guide, /Project folder: \/invented\/work-project/);
  assert.doesNotMatch(results, /\/invented\/project/, 'the opened library folder is never presented as the results location');
  assert.match(guide, /hasn't checked that any of them exist/);
});

test('an open run reports questions, offers End this run and refuses a second prepare; a finished run says so', async () => {
  const open = {reference:'run-1', conversation:'T1', home:'account', generation:g, source:'sent', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}, status:{}};
  const ui = await mount({thread:'T1', host:host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]}), data:data({selections:selected(), runs:[open]})});
  assert.match(region(ui.c, 'Run progress').textContent, /Waiting for your answer/);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true, 'an open run is not prepared again from the guide');
  assert.ok(all(region(ui.c, 'Run progress'), 'a').some(a => a.getAttribute('href') === '#conversation'));
  assert.equal(button(ui.c, 'End as completed, on the agent\'s report'), undefined, 'no completed end without the host\'s finished offer');
  await ui.press('End this run');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:null}});
  const message = {threadId:'T1', turnId:'turn-9', itemId:'m'};
  await ui.rerender({data:data({selections:selected(), runs:[open], offers:[{message, finished:{run:'run-1', statement:'Workflow finished: project:resolve-spacing'}}, {message:{threadId:'T1'}, finished:{run:'run-other', statement:'x'}}]})});
  assert.match(region(ui.c, 'Agent finished report').textContent, /The agent wrote “Workflow finished: project:resolve-spacing”/);
  await ui.press('End as completed, on the agent\'s report');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:message}}, 'the existing completed path carries the host\'s exact report message');
  await ui.rerender({host:host(), data:data({selections:selected(), runs:[{...open, lifecycle:{state:'ended by the person', end:{cause:'completed'}}}]})});
  assert.match(region(ui.c, 'Run progress').textContent, /Ended as completed\./);
  assert.equal(button(ui.c, 'End this run'), undefined);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, false, 'after the end a new run may be prepared');
  const other = {...open, reference:'run-x', conversation:'T2'};
  await ui.rerender({data:data({selections:selected(), runs:[other]})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /No run in this conversation yet/, 'another conversation\'s run is not shown as this one');
});

test('an unregistered library entry is reviewed singly; the bundled candidate is shown as not runnable without a selecting control', async () => {
  const ui = await mount({thread:'T1', host:host(), data:data()});
  const review = region(ui.c, 'Workflows that need a first review');
  assert.match(review.textContent, /draft-free-entry/); assert.doesNotMatch(review.textContent, /broken/);
  await ui.press('Review draft-free-entry for first use…');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_review_library_entries', args:{libraryRef:'lib:project', listingRef:'listing-1', entryRefs:['entry-1']}});
  await ui.press('Look for other workflows in this library');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_library_entries_refresh', args:{libraryRef:'lib:project'}});
  const guide = region(ui.c, 'Run a workflow');
  assert.match(guide.textContent, /Included with the App: coordinated-knowledge-work\. This build can't run it directly; you can inspect it in the workflow studio\./);
  const why = all(guide, 'details').find(d => d.textContent.startsWith('Why'));
  assert.match(why.textContent, /production bundle candidate; not a published release/, 'the host reason stays available under Why');
  assert.equal(all(guide, 'button').some(b => b.textContent.includes('coordinated-knowledge-work')), false);
  await ui.rerender({data:data({productionCatalog:{standing:'released', entries:[{name:'coordinated-knowledge-work', revision:'bundled-rev-0123456789', runnable:true, runLimit:null}]}})});
  await ui.press('Use coordinated-knowledge-work (included with the App)');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_select_production_bundle', args:{name:'coordinated-knowledge-work'}}, 'a host-runnable bundled entry uses the existing bundled selection');
  await ui.rerender({data:data()});
  await ui.rerender({data:data({selections:selected(false)})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: resolve-spacing can't run: not registered/);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true);
  await ui.rerender({data:data({selections:selected(), reviews:[{reference:'rev-ref', status:{presentation:{entries:[]}}}], activeReview:'rev-ref'})});
  assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#workflow-reviews'));
});

test('a stale workflow source disables every guide command', async () => {
  const ui = await mount({thread:'T1', host:host({workflowRoot:{context:{sourceRef:'other', generation:g}}}), data:data({selections:selected()})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: The workflow view is out of date/);
  assert.match(region(ui.c, 'Workflows ready to use').textContent, /resolve-spacing · revision 2 — chosen/);
  assert.equal(button(ui.c, 'Use resolve-spacing'), undefined, 'the chosen revision is not offered again');
  const labels = ['Reload this project\'s workflows', 'Review draft-free-entry for first use…', 'Look for other workflows in this library', 'Prepare this run'];
  const stale = host({workflowRoot:{context:{sourceRef:'other', generation:g}}});
  const prepared = {reference:'run-p', conversation:'T1', home:'account', generation:g, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{sent:false}};
  const open = {reference:'run-o', conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}, status:{}};
  const clickAll = async list => { for (const label of list) { const node = button(ui.c, label); assert.ok(node, label); assert.equal(props(node).disabled, true, label);
    await React.act(async () => props(node).onClick()); } };
  await clickAll(labels);
  await ui.rerender({host:stale, data:data({selections:selected(), runs:[prepared]})}); await clickAll(['Start the run']);
  await ui.rerender({host:stale, data:data({selections:selected(), runs:[open], offers:[{message:{threadId:'T1'}, finished:{run:'run-o', statement:'s'}}]})}); await clickAll(['End this run', 'End as completed, on the agent\'s report']);
  assert.equal(props(all(ui.c, 'select')[0]).disabled, true, 'the conversation choice follows the same guard');
  assert.deepEqual(ui.calls, [], 'a retained click on a stale control dispatches nothing');
});

test('an unknown start outcome is not resent without the person reading the conversation; a definite refusal may be prepared again', async () => {
  const unknown = {reference:'run-u', conversation:'T1', home:'account', generation:g, source:'src', lifecycle:{state:NOT_CONFIRMED}, status:UNKNOWN};
  const ui = await mount({thread:'T1', host:host(), data:data({selections:selected(), runs:[unknown]})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: Read the conversation: the last start's outcome is unknown and it may have run\./);
  assert.match(region(ui.c, 'Run progress').textContent, /Start not confirmed — outcome unknown/);
  assert.ok(all(region(ui.c, 'Run progress'), 'a').some(a => a.getAttribute('href') === '#conversation'));
  const prepare = button(ui.c, 'Prepare this run'); assert.equal(props(prepare).disabled, true);
  await React.act(async () => props(prepare).onClick()); assert.deepEqual(ui.calls, []);
  const ack = all(ui.c, 'input').find(node => props(node)?.type === 'checkbox');
  await React.act(async () => props(ack).onChange({target:{checked:true}}));
  await ui.press('Prepare this run');
  assert.equal(ui.calls.at(-1).command, 'workflow_prepare_run', 'only after the explicit acknowledgement');
  await ui.rerender({data:data({selections:selected(), runs:[unknown, {...unknown, reference:'run-u2'}]})});
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true, 'the acknowledgement named the earlier run only');
  await ui.rerender({data:data({selections:selected(), runs:[{...unknown, status:REFUSED}]})});
  assert.equal(all(ui.c, 'input').some(node => props(node)?.type === 'checkbox'), false);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, false);
  assert.match(region(ui.c, 'Run progress').textContent, /Codex refused to start the run/);
});

test("with App navigation, the run's conversation is shown — its requests when Codex is waiting — and nothing is sent", async () => {
  const open = {reference:'run-1', conversation:'T2', home:'account', generation:g, source:'sent', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}, status:{}};
  const ui = await mount({navigate:true, thread:'T2', host:host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T2'}}]}), data:data({selections:selected(), runs:[open]})});
  assert.equal(all(region(ui.c, 'Run progress'), 'a').length, 0, 'no bare scroll link that could show another conversation');
  await ui.press('Answer in the conversation');
  assert.deepEqual(ui.shown, [['T2', 'conversation-requests']]);
  await ui.rerender({host:host()});
  await ui.press('Show the conversation');
  assert.deepEqual(ui.shown.at(-1), ['T2', 'conversation']);
  assert.deepEqual(ui.calls, [], 'navigation issues no host command');
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
// host JSON, a newer registered revision was noted only in the studio, Use
// labels hid the revision, and focus fell to the page after Prepare and Start.
test('the last result is in words with the reply under details, a newer revision is offered here, and revisions are told apart', async () => {
  const twoRevisions = data({libraries:[{...data().libraries[0], registered:[
    {name:'resolve-spacing', sequence:2, revision:'rev-2-abcdef0123456789', label:'registered — selectable', selectable:true},
    {name:'resolve-spacing', sequence:3, revision:'rev-3-abcdef0123456789', label:'registered — selectable', selectable:true}]}]});
  const newer = {notice:'Revision 3 of resolve-spacing is registered', revision:'rev-3-abcdef0123456789', selectable:true, offered:'Use revision 3 in this conversation'};
  const view = {host:host(), data:{...twoRevisions, selections:[{...selected()[0], selection:{...selected()[0].selection, newerRevision:newer}}]}, thread:'T1',
    outcome:{command:'workflow_select_listed', message:'{"state":"selected","reference":"sel-1"}', failed:false, settled:true}};
  const ui = await mount(view);
  const last = region(ui.c, 'Run a workflow — last result');
  assert.match(last.textContent, /^Chose the workflow for this conversation\.What the App reported\{"state":"selected"/, 'words first; the exact reply under details');
  assert.equal(all(last, 'p')[0].textContent, 'Chose the workflow for this conversation.');
  await ui.rerender({outcome:{command:'workflow_send_run', message:'Error: invented refusal text', failed:true, settled:true}});
  assert.equal(region(ui.c, 'Run a workflow — last result').textContent, "Couldn't start the run: invented refusal text");
  await ui.rerender({outcome:{command:'workflow_send_run', message:'', failed:false, settled:false}});
  assert.equal(region(ui.c, 'Run a workflow — last result'), undefined, 'nothing is claimed before the result arrives');
  const note = region(ui.c, 'Newer revision for this conversation');
  assert.match(note.textContent, /A newer revision of resolve-spacing is registered \(Revision 3 of resolve-spacing is registered\)\. This conversation keeps using the one shown above until you choose the newer one\./);
  await ui.press('Use revision 3 in this conversation');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_follow_newer_revision', args:{selectionRef:'sel-1', revision:'rev-3-abcdef0123456789'}});
  assert.ok(button(ui.c, 'Use resolve-spacing revision 3'), 'same-name rows name their revision');
});

test('after Prepare the Start button has the focus, and after Start the run progress', async () => {
  const proto = Object.getPrototypeOf(document.createElement('div')); const focused = []; const previous = proto.focus;
  proto.focus = function () { focused.push(this); };
  try {
    const view = {host:host(), data:data({selections:selected()}), thread:'T1'};
    const ui = await mount(view);
    await ui.type('Fix the spacing in reports/');
    await ui.press('Prepare this run');
    await ui.rerender({data:data({selections:selected(), runs:[{reference:'run-1', conversation:'T1', home:'account', generation:g, workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}}]})});
    assert.equal(focused.at(-1)?.textContent, 'Start the run', 'Prepare lands on Start');
    await ui.press('Start the run');
    await ui.rerender({data:data({selections:selected(), runs:[{reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}}]})});
    assert.equal(focused.at(-1)?.getAttribute('aria-label'), 'Run progress', 'Start lands on the run progress');
  } finally { proto.focus = previous; }
});

// Rows as runtime_session's run view gives them (generation, home, conversation,
// workflow{origin,name,revision,sourceRoot}); the host's runs are a map, so the
// array order is scrambled here on purpose, and order comes only from
// preparationOrder (local to one home and conversation).
const runRow = over => ({reference:'run', conversation:'T1', home:'account', generation:g, source:'s', turn:'t', compatibility:[{preparation:{declaration}}],
  workflow:{name:'resolve-spacing', origin:'project', revision:'rev-1-0123456789ab', sourceRoot:'project'}, lifecycle:{state:'ended', end:{cause:'completed'}}, ...over});
test('Results orders this conversation\'s runs only by the host\'s preparationOrder, never by array position, and says when order is not known', async () => {
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const ordered = [runRow({reference:'run-b', preparationOrder:1, lifecycle:{state:'ended', end:{cause:'ended by the person'}}}), runRow({reference:'run-c', preparationOrder:2, lifecycle:{state:'ended', end:{cause:'completed'}}}),
    runRow({reference:'run-a', preparationOrder:0}), runRow({reference:'run-other', conversation:'T2', preparationOrder:5}), runRow({reference:'run-prep', preparationOrder:3, source:undefined, lifecycle:{state:PREPARED}})];
  const ui = await mount({host:host(), data:data({selections:selected(), runs:ordered}), thread:'T1', navigate:true});
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
  assert.match(region(ui.c, 'Run progress')?.textContent ?? region(ui.c, 'Run a workflow').textContent, /several runs, and the App can't tell which one is the latest|several runs whose order the App can't tell/);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true, 'an open run among them still holds a new preparation');
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: A run in this conversation is still open, and the App can't tell which run is latest/, 'Next does not offer a preparation that is held');
  await ui.rerender({data:data({selections:selected(), runs:[runRow({reference:'run-y'}), runRow({reference:'run-u', lifecycle:{state:NOT_CONFIRMED}, status:UNKNOWN})]})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: Read the conversation: a start here has an unknown outcome and may have run; the App can't tell which run is latest\./, 'no "last start" claim without an order');
  assert.equal(ui.calls.filter(call => call.command).length, 0, 'finding results issues nothing');
});

test('a run from an earlier Codex session with the same thread ID is never current; recorded runs match the full workflow source', async () => {
  const g1 = g, g2 = {...g, spawnCounter:2};
  const restarted = host({generation:g2, workflowRoot:{context:{sourceRef:'src', generation:g2}}, threads:[{threadId:'T1', generation:g2, model:'invented-model', status:{type:'idle'}}]});
  const runs = [runRow({reference:'run-old', generation:g1, preparationOrder:0}), runRow({reference:'run-new', generation:g2, preparationOrder:1}), runRow({reference:'run-key-home', home:'api-key', generation:{...g2, home:'api-key'}})];
  const sel = [{sourceRef:'src', threadId:'T1', selection:{...selected()[0].selection, identity:{kind:'registered', name:'resolve-spacing', origin:'project', source_root:'project', revision:'rev-2-abcdef0123456789'}}}];
  const reopened = {standing:'s', runs:[
    {run:'rec-same', conversation:'thread-old', state:'ended', workflow:{kind:'registered', name:'resolve-spacing', origin:'project', source_root:'project', revision:'rev-0-aaaaaaaaaaaa'}},
    {run:'rec-other-root', conversation:'x', state:'ended', workflow:{kind:'registered', name:'resolve-spacing', origin:'project', source_root:'other-project', revision:'r'}},
    {run:'rec-no-root', conversation:'y', state:'ended', workflow:{name:'resolve-spacing', origin:'project', revision:'r'}},
    {run:'run-new', conversation:'T1', state:'open', workflow:{kind:'registered', name:'resolve-spacing', origin:'project', source_root:'project'}}]};
  const ui = await mount({host:restarted, data:data({context:{sourceRef:'src', generation:g2}, selections:sel, runs, reopened}), thread:'T1', navigate:true});
  const current = region(ui.c, 'Runs in this conversation');
  assert.ok(current.querySelectorAll(node => node.getAttribute('aria-label') === 'Run run-new')[0], 'the current-session run is current');
  assert.equal(current.querySelectorAll(node => node.getAttribute('aria-label') === 'Run run-old')[0], undefined, 'the earlier session\'s run is not current');
  const earlier = region(ui.c, 'Runs whose conversation isn\'t loaded');
  assert.match(earlier.textContent, /Earlier runs with this conversation ID, from a Codex session that isn't loaded now:Recorded conversation T1/);
  assert.match(region(ui.c, 'Run run-old').textContent, /find it in History/);
  assert.equal(button(region(ui.c, 'Run run-old'), 'Show the conversation'), undefined, 'no navigation into the same-ID current conversation');
  assert.equal(region(ui.c, 'Run run-key-home'), undefined, 'another home\'s run is not listed');
  const recorded = region(ui.c, 'Recorded runs of this workflow').textContent;
  assert.match(recorded, /rec-same · revision rev-0-aaaaaa… · ended · recorded conversation thread-old/);
  assert.doesNotMatch(recorded, /rec-other-root|rec-no-root|run-new/, 'another source root, an incomplete source and a live run are not this family');
});

test('after Codex restarts and the run\'s conversation is not loaded, its runs stay findable as not loaded', async () => {
  const g2 = {...g, spawnCounter:2};
  const runs = [{reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', workflow:{name:'resolve-spacing', origin:'project', revision:'rev-1-0123456789ab'}, lifecycle:{state:'ended', end:{cause:'completed'}}},
    {reference:'run-other-home', conversation:'T9', home:'api-key', source:'s', workflow:{name:'resolve-spacing'}, lifecycle:{state:'ended', end:{cause:'completed'}}}];
  const restarted = host({generation:g2, workflowRoot:{context:{sourceRef:'src', generation:g2}}, threads:[{threadId:'T5', generation:g2, model:'invented-model', status:{type:'idle'}}]});
  const ui = await mount({host:restarted, data:data({context:{sourceRef:'src', generation:g2}, runs}), navigate:true});
  const unloaded = region(ui.c, 'Runs whose conversation isn\'t loaded');
  assert.ok(unloaded, 'the earlier run is still listed');
  assert.match(region(ui.c, 'Run run-1').textContent, /Ended as completed\..*Its conversation isn't loaded in this Codex session; find it in History\./);
  assert.equal(button(region(ui.c, 'Run run-1'), 'Show the conversation'), undefined, 'no navigation to a conversation that isn\'t loaded');
  assert.equal(region(ui.c, 'Run run-other-home'), undefined, 'another home\'s run is not listed');
});
