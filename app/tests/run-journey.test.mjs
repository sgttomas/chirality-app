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
  const render = () => root.render(React.createElement(RunWorkflowGuide, {data:view.data, host:view.host, thread, busy:false, text,
    chooseThread:value => { thread = value; calls.push({choose:value}); render(); }, setText:value => { text = value; render(); },
    act:async (command, args) => { calls.push({command, args}); }, outcome:view.outcome ?? null}));
  await React.act(async () => render());
  return {c, calls, press:async label => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); },
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
  assert.equal(runReading({conversation:'T1', lifecycle:{state:'start not confirmed (turn refused or outcome unknown); not opened, not live'}}, host()).tone, 'failed');
  const sent = runReading({conversation:'T1', source:'sent', lifecycle:{state:PREPARED}}, host());
  assert.equal(sent.title, 'Starting', 'a send acknowledgment is not a started or completed run');
  assert.equal(runReading({conversation:'T1', lifecycle:{state:PREPARED}, status:{sent:false, state:'WR pre-send publication failed; nothing sent', limit:'disk full'}}, host()).title, 'Not started');
  assert.equal(runReading({conversation:'T1', lifecycle:{state:PREPARED}, status:{sent:false}}, host()).title, 'Ready to start');
  const done = runReading({conversation:'T1', source:'s', lifecycle:{state:'ended by the person', end:{cause:'completed'}}}, host());
  assert.equal(done.tone, 'done'); assert.match(done.detail, /completed/);
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
  const prepared = {reference:'run-1', conversation:'T1', home:'account', workflow:{name:'resolve-spacing'}, lifecycle:{state:PREPARED}, status:{sent:false}, compatibility:[{preparation:{declaration}}]};
  await ui.rerender({data:data({selections:selected(), runs:[prepared]})});
  assert.equal(button(ui.c, 'Prepare this run'), undefined);
  assert.match(region(ui.c, 'Run progress').textContent, /Ready to start/);
  await ui.press('Start the run');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_send_run', args:{runRef:'run-1'}});
  const results = region(ui.c, 'Where the results go').textContent;
  assert.match(results, /report-file — reports\/spacing\.md in \/invented\/project: The written report/);
});

test('an open run reports questions, offers End this run and refuses a second prepare; a finished run says so', async () => {
  const open = {reference:'run-1', conversation:'T1', home:'account', source:'sent', workflow:{name:'resolve-spacing'}, lifecycle:{state:OPEN}, status:{}};
  const ui = await mount({thread:'T1', host:host({serverRequests:[{state:'outstanding', nativeParameters:{threadId:'T1'}}]}), data:data({selections:selected(), runs:[open]})});
  assert.match(region(ui.c, 'Run progress').textContent, /Waiting for your answer/);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true, 'an open run is not prepared again from the guide');
  assert.ok(all(region(ui.c, 'Run progress'), 'a').some(a => a.getAttribute('href') === '#conversation'));
  await ui.press('End this run');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:null}});
  await ui.rerender({host:host(), data:data({selections:selected(), runs:[{...open, lifecycle:{state:'ended by the person', end:{cause:'completed'}}}]})});
  assert.match(region(ui.c, 'Run progress').textContent, /Finished\..*completed/);
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
  assert.match(guide.textContent, /Included with the App: coordinated-knowledge-work\. This build can't run it directly yet \(production bundle candidate; not a published release\)/);
  assert.equal(all(guide, 'button').some(b => b.textContent.includes('coordinated-knowledge-work')), false);
  await ui.rerender({data:data({selections:selected(false)})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: resolve-spacing can't run: not registered/);
  assert.equal(props(button(ui.c, 'Prepare this run')).disabled, true);
  await ui.rerender({data:data({selections:selected(), reviews:[{reference:'rev-ref', status:{presentation:{entries:[]}}}], activeReview:'rev-ref'})});
  assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#workflow-reviews'));
});

test('a stale workflow source disables every guide command', async () => {
  const ui = await mount({thread:'T1', host:host({workflowRoot:{context:{sourceRef:'other', generation:g}}}), data:data({selections:selected()})});
  assert.match(region(ui.c, 'Run a workflow').textContent, /Next: The workflow view is out of date/);
  for (const label of ['Reload this project\'s workflows', 'Use resolve-spacing', 'Review draft-free-entry for first use…', 'Look for other workflows in this library', 'Prepare this run'])
    assert.equal(props(button(ui.c, label)).disabled, true, label);
  assert.deepEqual(ui.calls, []);
});
