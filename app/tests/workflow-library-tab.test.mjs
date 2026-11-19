import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentBlocks, agentBlockText} from './support/agent-text.mjs';

// The right panel's Workflows tab (3.0.1's library) over the host state the Run guide reads. "Use in message" picks a
// workflow for the next message: the renderer holds the pick (WorkflowPick.tsx) and the tab issues no host command
// for it. Controlled host views with invented entries in the shapes the host gives (runtime_session.rs snapshot,
// workflow_library.rs registered_listing); no native App, supplier, model or person act.
if (!globalThis.document) installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {WorkflowLibrary} = loadSrc('WorkflowLibrary');
const {pickScope} = loadSrc('WorkflowPick');
const {includedSections} = loadSrc('IncludedWorkflows');
const {WorkflowRootPanel} = loadSrc('App');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const ROOT = 'invented-library:library-v9.9.9', METHOD = 'invented.package.sha256/v1', PROJECT_ROOT = '/invented/project';
const identity = (name, over = {}) => ({kind:'workflow', origin:'bundled', source_root:ROOT, name, revision:`${name}-revision-0123456789abcdef`, revision_method:METHOD, ...over});
const group = (key, label, order) => ({key, label, order});
const PLAN = group('plan-organize', 'Plan & organize', 1), REVIEW = group('review-check', 'Review & check', 5);
const entry = (name, navigation, over = {}) => ({name, revision:`${name}-revision-0123456789abcdef`, origin:'bundled', sourceRoot:ROOT, revisionMethod:METHOD, identity:identity(name), runnable:true, runLimit:null,
  description:`Invented description of ${name}.`, central:false, compatibility:'canonical', roles:['HELP_HUMAN'], navigation, libraryExecution:null, libraryPathsNamed:[], ...over});
const entries = [
  entry('review-b', {category:'specialist', tier:'supporting', order:1, group:REVIEW}),
  entry('review-a', {category:'specialist', tier:'primary', order:2, group:REVIEW}, {libraryPathsNamed:['tools/check.py'], compatibility:'legacy'}),
  entry('plan-work', {category:'specialist', tier:'primary', order:1, group:PLAN, displayName:'Plan the work'}, {description:'Turn a goal into ordered work.'}),
  entry('core-a', {category:'core', tier:'primary', order:1, displayName:'Begin a project'}),
  entry('loose', {category:'specialist', tier:'primary', order:1}),
  entry('old-way', {category:'superseded', tier:'primary', order:1}),
  entry('broken', {category:'specialist', tier:'primary', order:9, group:PLAN}, {runnable:false, runLimit:'its files differ from the release'}),
  entry('unreported', {category:'specialist', tier:'primary', order:8, group:PLAN}, {runnable:undefined}),
];
const catalog = (over = {}) => ({standing:'invented standing', source:{tag:'library-v9.9.9'}, entries, ...over});
const LIB = 'workflow-library:invented';
const listed = (name, sequence, over = {}) => ({name, sequence, revision:`${name}-${sequence}-rev-0123456789abcdef`, registeredAt:'2026-11-19T09:00:00Z', disposition:'registration',
  label:'registered — approved in this App session (native A15)', evidence:'in-process A15', selectable:true, reconfirm:false, offered:'Select; Refine (RF-1)', ...over});
const projectLibrary = (over = {}) => ({reference:LIB, root:{encoding:'unix_bytes', bytes:[...new TextEncoder().encode(PROJECT_ROOT)]}, origin:'project', sourceRoot:PROJECT_ROOT,
  registered:[listed('site-check', 1), listed('site-check', 2), listed('cold-flow', 1, {label:'registered — approval authenticity unverified; re-confirm to use in this App session', selectable:false, reconfirm:true})],
  entryListing:{state:'observed', reference:'listing-1', libraryRef:LIB, entries:[{reference:'entry-1', name:'new-flow', state:'unregistered', reviewable:true}], limits:[]}, ...over});
const projectIdentity = (name, revision) => identity(name, {origin:'project', source_root:PROJECT_ROOT, revision});
const selection = (id, over = {}) => [{sourceRef:'src', threadId:'T1', selection:{state:'selected', reference:'sel-1', runnable:true, runLimit:null, currentLimit:null, identity:id, ...over}}];
const host = (threads = [{threadId:'T1', generation:g, status:{type:'idle'}}]) => ({state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}}, serverRequests:[], threads});
const data = (over = {}) => ({context:{sourceRef:'src', generation:g, historyEpoch:3}, projectLibraryAvailable:true, activeLibrary:null, libraries:[],
  productionCatalog:catalog(), selections:[], runs:[], reviews:[], ...over});

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const labelled = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const buttons = node => all(node, 'button');
const button = (node, label) => buttons(node).find(b => b.textContent === label);
const card = (c, name) => labelled(c, `Included workflow ${name}`) ?? labelled(c, `Project workflow ${name}`);
const notes = c => c.querySelectorAll(node => node.getAttribute('class') === 'method-library-note').map(n => n.textContent);

async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const picks = [];
  // The pick is the App's state; here the test holds it, as App.tsx does, and every setPick is recorded.
  const calls = [];
  const render = () => root.render(React.createElement(WorkflowLibrary, {data:view.data ?? data(), host:view.host ?? host(), busy:!!view.busy, pick:view.pick ?? null,
    setPick:next => { picks.push(next); view.pick = next; render(); }, viewStale:!!view.viewStale, outcome:view.outcome ?? null,
    act:view.act ? async (command, args) => { calls.push({command, args}); } : undefined}));
  await React.act(async () => render());
  return {c, picks, calls, get pick() { return view.pick ?? null; },
    search:async value => React.act(async () => props(c.querySelectorAll(n => n.localName === 'input' && props(n)?.type === 'search')[0]).onChange({target:{value}})),
    press:async node => { assert.ok(node, 'the control is drawn'); assert.equal(!!props(node).disabled, false, `${node.textContent} enabled`); await React.act(async () => props(node).onClick()); },
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); },
    close:async () => React.act(async () => root.unmount())};
}

test('the included workflows keep the App\'s grouping and order, each folded subgroup with its count, the first open', async () => {
  const ui = await mount({});
  const subgroups = all(ui.c, 'details').filter(d => d.getAttribute('class') === 'method-library-subgroup');
  const expected = includedSections(entries);
  assert.deepEqual(subgroups.map(d => all(d, 'h4')[0].textContent), expected.map(s => s.label), 'the sections includedSections gives, in its order');
  assert.deepEqual(subgroups.map(d => all(d, 'span').find(s => s.getAttribute('class') === 'method-library-count').textContent), expected.map(s => String(s.entries.length)));
  assert.deepEqual(subgroups.map(d => all(d, 'li').map(li => li.getAttribute('aria-label'))), expected.map(s => s.entries.map(e => `Included workflow ${e.name}`)), 'entries in the section\'s order');
  assert.deepEqual(subgroups.map(d => props(d).open === true), expected.map((_, i) => i === 0), 'only the first is open');
  assert.deepEqual(all(ui.c, 'h3').map(h => h.textContent), ['Included with Chirality', 'This project']);
  await ui.close();
});

test('search uses the App\'s rule, over the included and the project\'s workflows, and opens every subgroup it shows', async () => {
  const ui = await mount({data:data({activeLibrary:LIB, libraries:[projectLibrary()]})});
  await ui.search('ORDERED goal');
  const subgroups = all(ui.c, 'details').filter(d => d.getAttribute('class') === 'method-library-subgroup');
  assert.deepEqual(subgroups.map(d => all(d, 'h4')[0].textContent), ['Plan & organize']);
  assert.ok(subgroups.every(d => props(d).open === true));
  assert.deepEqual(all(ui.c, 'li').map(li => li.getAttribute('aria-label')), ['Included workflow plan-work']);
  assert.ok(ui.c.querySelectorAll(n => n.getAttribute('role') === 'status').some(n => n.textContent === '1 match.'));
  await ui.search('site');
  assert.deepEqual(all(ui.c, 'li').map(li => li.getAttribute('aria-label')), ['Project workflow site-check', 'Project workflow site-check']);
  await ui.search('nothing like this');
  assert.ok(ui.c.querySelectorAll(n => n.getAttribute('role') === 'status').some(n => n.textContent === 'No workflow matches. Try fewer or other words.'));
  await ui.close();
});

test('an included card: its title and identifier, its description, where it comes from, Inspect and Use in message', async () => {
  const ui = await mount({});
  const plan = card(ui.c, 'plan-work');
  const heading = plan.querySelectorAll(n => n.getAttribute('class') === 'method-card-heading')[0];
  assert.equal(all(heading, 'strong')[0].textContent, 'Plan the work');
  assert.equal(all(heading, 'code')[0].textContent, 'plan-work');
  assert.ok(all(plan, 'p').some(p => p.textContent === 'Turn a goal into ordered work.'));
  assert.equal(plan.querySelectorAll(n => n.getAttribute('class') === 'method-card-meta')[0].textContent, 'Chirality Library 9.9.9');
  assert.deepEqual(buttons(plan).filter(b => !b.closest?.('details')).slice(0, 2).map(b => [b.textContent, b.getAttribute('aria-pressed')]), [['Inspect', null], ['Use in message', 'false']]);
  // A title that is the name shows once, as 3.0.1's card does.
  assert.equal(all(card(ui.c, 'loose'), 'code').filter(n => n.getAttribute('class') === 'method-card-identifier').length, 0);
  // What is not needed at a glance is behind the card's own disclosure, nothing lost.
  const details = all(card(ui.c, 'review-a'), 'details')[0];
  assert.equal(all(details, 'summary')[0].textContent, 'Details');
  assert.match(details.textContent, /Revision review-a-rev…/);
  assert.match(details.textContent, /The Library lists it for these roles: HELP_HUMAN\./);
  assert.match(details.textContent, /The Library marks it as legacy\./);
  assert.match(details.textContent, /This workflow's files name 1 path of Chirality Library 9\.9\.9 that is not included in the App \(for example tools\/check\.py\)\./);
  // An entry the host does not admit, or has not reported on, says so in the present words and cannot be chosen.
  const broken = card(ui.c, 'broken');
  assert.match(broken.textContent, /Can't be used in this App: its files differ from the release\./);
  assert.equal(!!props(button(broken, 'Use in message')).disabled, true);
  const unreported = card(ui.c, 'unreported');
  assert.match(unreported.textContent, /The App hasn't reported whether this workflow can be used here\./);
  assert.equal(!!props(button(unreported, 'Use in message')).disabled, true);
  await ui.close();
});

test('Use in message picks an included workflow for the next message: no host command, the card then offers Remove, one pick at a time', async () => {
  const previous = window.__TAURI_INTERNALS__; const issued = [];
  window.__TAURI_INTERNALS__ = {invoke: async command => { issued.push(command); return null; }};
  try {
    const ui = await mount({});
    await ui.press(button(card(ui.c, 'plan-work'), 'Use in message'));
    assert.deepEqual(ui.pick, {kind:'included', name:'plan-work', revision:'plan-work-revision-0123456789abcdef', title:'Plan the work', from:'Chirality Library 9.9.9', scope:pickScope(host())});
    assert.deepEqual(issued, [], 'picking sends nothing to the host');
    const picked = button(card(ui.c, 'plan-work'), 'Remove');
    assert.equal(picked.getAttribute('aria-pressed'), 'true');
    assert.equal(card(ui.c, 'plan-work').getAttribute('data-chosen'), 'true');
    assert.equal(button(card(ui.c, 'plan-work'), 'Use in message'), undefined);
    // Another card replaces the pick; only one card is pressed.
    await ui.press(button(card(ui.c, 'loose'), 'Use in message'));
    assert.equal(ui.pick.name, 'loose');
    assert.equal(buttons(ui.c).filter(b => b.getAttribute('aria-pressed') === 'true').length, 1);
    assert.ok(button(card(ui.c, 'plan-work'), 'Use in message'));
    // Remove drops the pick, and sends nothing either.
    await ui.press(button(card(ui.c, 'loose'), 'Remove'));
    assert.equal(ui.pick, null);
    assert.equal(buttons(ui.c).filter(b => b.getAttribute('aria-pressed') === 'true').length, 0);
    assert.deepEqual(issued, []);
    await ui.close();
  } finally { window.__TAURI_INTERNALS__ = previous; }
});

test('this project\'s workflows: a registered revision is picked with its library and revision; one to re-confirm or review says so and cannot be picked', async () => {
  const ui = await mount({data:data({activeLibrary:LIB, libraries:[projectLibrary()]})});
  const project = labelled(ui.c, 'Workflows').querySelectorAll(n => n.getAttribute('aria-labelledby') === 'method-group-project')[0];
  assert.deepEqual(all(project, 'li').map(li => li.getAttribute('aria-label')), ['Project workflow site-check', 'Project workflow site-check', 'Project workflow cold-flow', 'Project workflow new-flow']);
  const [first, second, cold, fresh] = all(project, 'li');
  assert.equal(all(first, 'strong')[0].textContent, 'site-check');
  assert.equal(first.querySelectorAll(n => n.getAttribute('class') === 'method-card-meta')[0].textContent, 'project workflow library · revision 1 · another revision has the same name');
  assert.equal(second.querySelectorAll(n => n.getAttribute('class') === 'method-card-meta')[0].textContent, 'project workflow library · revision 2 · another revision has the same name');
  await ui.press(button(second, 'Use in message'));
  assert.deepEqual(ui.pick, {kind:'listed', name:'site-check', revision:'site-check-2-rev-0123456789abcdef', libraryRef:LIB, sequence:2,
    label:'registered — approved in this App session (native A15)', title:'site-check', from:'project workflow library', scope:pickScope(host())}, 'the arguments workflow_select_listed will take, held until Start run');
  const rows = all(ui.c, 'li').filter(li => li.getAttribute('aria-label') === 'Project workflow site-check');
  assert.deepEqual(rows.map(li => buttons(li).find(b => b.getAttribute('aria-pressed'))?.textContent), ['Use in message', 'Remove'], 'only the picked revision is pressed');
  assert.equal(!!props(button(cold, 'Use in message')).disabled, true);
  assert.match(cold.textContent, /registered — approval authenticity unverified; re-confirm to use in this App session\. Re-confirm cold-flow in the workflow studio/);
  assert.equal(button(fresh, 'Use in message'), undefined, 'an entry not approved for use has no choosing control');
  assert.match(fresh.textContent, /In the folder but not yet approved for use here\. Read it once and confirm it in the App's dialog; nothing runs during the review\./);
  assert.equal(all(fresh, 'a').length, 0, 'no link to the removed guide');
  await ui.close();
});

test('where the project\'s workflows come from, and a library or list that could not be read, in the App\'s present words', async () => {
  let ui = await mount({});
  assert.ok(notes(ui.c).includes('This App has a project folder. Its workflows are kept in its .chirality folder.'));
  await ui.rerender({data:data({projectLibraryAvailable:false})});
  assert.ok(notes(ui.c).includes('No project folder is set for this App yet. Choose a project in Desktop setup — the choice applies when you next open the App.'));
  await ui.rerender({data:data({activeLibrary:LIB, libraries:[projectLibrary({registered:{limit:'ledger unreadable'}, entryListing:{state:'unavailable', reference:'listing-1', libraryRef:LIB, entries:[], limits:['folder busy']}})]})});
  assert.match(ui.c.textContent, /This library's list of approved workflows can't be read: ledger unreadable/);
  assert.match(ui.c.textContent, /The App couldn't look in this library's folder for other workflows: folder busy/);
  await ui.rerender({data:data({activeLibrary:LIB, libraries:[projectLibrary({registered:[], entryListing:{state:'observed', reference:'l', libraryRef:LIB, entries:[], limits:[]}})]})});
  assert.ok(notes(ui.c).includes('No workflow in this library has been approved for use yet.'));
  await ui.close();
  ui = await mount({data:data({productionCatalog:{standing:'candidate catalog unavailable', entries:[], limit:'manifest unreadable'}})});
  assert.match(ui.c.textContent, /The included workflows can't be read: manifest unreadable/);
  await ui.close();
});

test('the pressed state follows the pick, not any conversation\'s selection; a pick from another source is not this card\'s', async () => {
  // A conversation's selection no longer marks a card: the tab is about the next message.
  const ui = await mount({data:data({selections:selection(identity('plan-work'))})});
  assert.equal(buttons(ui.c).filter(b => b.getAttribute('aria-pressed') === 'true').length, 0);
  assert.equal(buttons(ui.c).filter(b => b.textContent === 'Chosen').length, 0);
  assert.doesNotMatch(ui.c.textContent, /chosen under Run a workflow|can't run:/);
  // A pick of the same name at another revision, or of a registered revision in another library, is not this card's.
  await ui.rerender({pick:{kind:'included', name:'plan-work', revision:'another-revision', title:'Plan the work', from:'', scope:pickScope(host())}});
  assert.equal(button(card(ui.c, 'plan-work'), 'Remove'), undefined);
  await ui.rerender({data:data({activeLibrary:LIB, libraries:[projectLibrary()]}), pick:{kind:'listed', name:'site-check', revision:'site-check-2-rev-0123456789abcdef', libraryRef:'workflow-library:other', title:'site-check', from:'', scope:pickScope(host())}});
  assert.equal(buttons(ui.c).filter(b => b.textContent === 'Remove').length, 0);
  // The picked card's subgroup opens.
  await ui.rerender({data:data(), pick:{kind:'included', name:'review-a', revision:'review-a-revision-0123456789abcdef', title:'review-a', from:'', scope:pickScope(host())}});
  const review = all(ui.c, 'details').find(d => all(d, 'h4')[0]?.textContent === 'Review & check');
  assert.equal(props(review).open, true);
  assert.equal(button(card(ui.c, 'review-a'), 'Remove').getAttribute('aria-pressed'), 'true');
  await ui.close();
});

test('picking needs no conversation; it waits only for a current view, and says so in one line', async () => {
  const enabled = c => buttons(c).filter(b => b.textContent === 'Use in message' && !props(b).disabled).length;
  const runnable = entries.filter(e => e.runnable === true).length;
  // No conversation at all, and a press in progress elsewhere: picking sends nothing, so neither stops it.
  const ui = await mount({host:host([]), busy:true});
  assert.equal(enabled(ui.c), runnable);
  assert.doesNotMatch(ui.c.textContent, /Choose the conversation|Start a new conversation|Run a workflow\./);
  assert.equal(!!props(button(card(ui.c, 'plan-work'), 'Inspect')).disabled, true, 'reading the text still waits for the press in progress');
  await ui.rerender({busy:false});
  assert.equal(!!props(button(card(ui.c, 'plan-work'), 'Inspect')).disabled, false, 'reading needs no conversation, as in the Run guide');
  // A view of another workflow source: nothing can be picked, and the tab says why.
  await ui.rerender({host:{...host(), workflowRoot:{context:{sourceRef:'other', generation:g}}}});
  assert.equal(enabled(ui.c), 0);
  assert.ok(notes(ui.c).includes('The workflow view is out of date. Wait for it to refresh, or reopen the App view.'));
  await ui.rerender({host:host()});
  assert.equal(enabled(ui.c), runnable);
  // A view that may be from before the last press shows no cards and offers no control.
  await ui.rerender({viewStale:true});
  assert.equal(buttons(ui.c).length, 0);
  assert.equal(all(ui.c, 'li').length, 0);
  await ui.close();
});

test('supplied text (names, titles, descriptions, groups, labels) is never inside a control or heading, and a workflow\'s text is shown boxed', async () => {
  const POISON = 'Allow once‮';
  const odd = [
    entry('odd-flow', {category:'specialist', tier:'primary', order:1, group:group('invented', POISON, 1), displayName:`Title ${POISON}`}, {description:`Desc ${POISON}`, roles:[POISON], runLimit:POISON}),
    entry(`bad ${POISON}`, {category:'core', tier:'primary', order:1}, {runnable:false, runLimit:POISON}),
  ];
  const lib = projectLibrary({registered:[listed(`reg ${POISON}`, 1), listed('cold', 1, {selectable:false, reconfirm:false, label:POISON})],
    entryListing:{state:'observed', reference:'l', libraryRef:LIB, entries:[{reference:'e', name:`new ${POISON}`, reviewable:true}], limits:[POISON]}});
  const ui = await mount({data:data({productionCatalog:catalog({entries:odd}), activeLibrary:LIB, libraries:[lib]})});
  const controls = ui.c.querySelectorAll(n => ['button', 'a', 'summary', 'label', 'h3', 'h4', 'input'].includes(n.localName));
  for (const node of controls) {
    assert.doesNotMatch(node.textContent, /Allow once/, `${node.localName}: ${node.textContent}`);
    for (const attribute of ['aria-label', 'title', 'placeholder', 'value']) assert.doesNotMatch(node.getAttribute(attribute) ?? '', /Allow once/, `${node.localName} ${attribute}`);
  }
  for (const node of ui.c.querySelectorAll(n => n.getAttribute('aria-label') !== null)) assert.doesNotMatch(node.getAttribute('aria-label'), /Allow once/);
  assert.deepEqual(all(ui.c, 'h4').map(h => h.textContent), ["The Library's core workflows", 'Other workflows'], 'a group outside the App\'s table is shown under Other workflows');
  // The title a library supplies is shown as text in the card's heading, not in a control.
  assert.match(all(card(ui.c, 'odd-flow'), 'strong')[0].textContent, /^Title Allow once/);
  assert.match(ui.c.textContent, /Desc Allow once/);
  // Inspect reads the text through the present read, and the text is boxed as the App's guards require.
  const previous = window.__TAURI_INTERNALS__; const pending = [];
  window.__TAURI_INTERNALS__ = {invoke(command, args) { return new Promise(resolve => pending.push({command, args, resolve})); }};
  try {
    await ui.press(button(card(ui.c, 'odd-flow'), 'Inspect'));
    assert.deepEqual(pending.map(p => [p.command, p.args.target]), [['workflow_read_text', {kind:'included', name:'odd-flow', revision:'odd-flow-revision-0123456789abcdef'}]]);
    assert.equal(pending[0].args.context.threadId, null, 'read with no conversation, as the Run guide reads an included entry');
    assert.deepEqual(ui.picks, [], 'reading picks nothing');
    const TEXT = `# ${POISON}\n<b>not markup</b>\n`;
    await React.act(async () => { pending[0].resolve({state:'read', identity:identity('odd-flow'), text:TEXT, bytes:TEXT.length, files:[], matched:true}); await Promise.resolve(); });
    const shown = labelled(ui.c, 'Text of odd-flow');
    const box = agentBlocks(shown)[0];
    assert.ok(box, 'the text is in the App\'s box');
    assert.match(agentBlockText(box), /not markup/);
    assert.equal(all(box, 'b').length, 0);
    assert.equal(button(card(ui.c, 'odd-flow'), 'Inspect').getAttribute('aria-expanded'), 'true');
    await ui.press(button(card(ui.c, 'odd-flow'), 'Inspect'));
    assert.equal(labelled(ui.c, 'Text of odd-flow'), undefined, 'Inspect again hides it');
  } finally { window.__TAURI_INTERNALS__ = previous; }
  await ui.close();
});

test('in the panel, the tab picks through the App\'s setPick with no conversation chosen, and issues no command', async () => {
  const c = document.createElement('div'); const root = createRoot(c); const calls = [], picks = [];
  const d = data(), h = {...host(), workflowRoot:d};
  await React.act(async () => root.render(React.createElement(WorkflowRootPanel, {data:d, host:h, view:'workflows', pick:null, setPick:next => { picks.push(next); }, act:async (command, args) => { calls.push([command, args]); return {}; }})));
  const library = c.querySelectorAll(n => n.getAttribute('id') === 'view-library')[0];
  assert.equal(props(library).hidden, false, 'the Workflows view is shown');
  assert.equal(c.querySelectorAll(n => n.getAttribute('id') === 'view-run' || n.getAttribute('id') === 'run-workflow').length, 0, 'the Run a workflow guide is gone');
  assert.equal(props(c.querySelectorAll(n => n.getAttribute('id') === 'workflow-studio')[0]).hidden, true, 'the studio is not shown under Workflows');
  const reads = buttons(c).find(b => b.textContent === 'Read recorded workflow supply (durable, read-only)');
  assert.equal(props(reads.parentNode).hidden, true, 'the studio\'s record reads are not shown under Workflows');
  // No conversation is chosen, and the card can still be used.
  await React.act(async () => props(button(card(library, 'plan-work'), 'Use in message')).onClick());
  assert.deepEqual(calls, [], 'picking issues no host command');
  assert.equal(picks.length, 1);
  assert.equal(picks[0].name, 'plan-work');
  assert.equal(picks[0].scope, pickScope(h));
  await React.act(async () => root.unmount());
});

// The Run a workflow guide's commands for this project's workflows, now in this tab: the same commands, arguments and
// conditions (run-journey.test.mjs held them for the guide).
test('this project\'s workflows: shown, looked for and reviewed for first use with the guide\'s own commands; nothing while busy, stale or Codex not ready', async () => {
  const ui = await mount({act:true});
  await ui.press(button(ui.c, 'Show this project\'s workflows'));
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_open_project_library', args:{}});
  await ui.rerender({data:data({activeLibrary:LIB, libraries:[projectLibrary({entryListing:{state:'observed', reference:'listing-1', libraryRef:LIB,
    entries:[{reference:'entry-1', name:'new-flow', state:'unregistered', reviewable:true}, {reference:'entry-2', name:'broken', state:'malformed', reviewable:false}], limits:[]}})]})});
  assert.ok(button(ui.c, 'Reload this project\'s workflows'), 'an opened library is reloaded with the same command');
  const fresh = card(ui.c, 'new-flow');
  assert.ok(labelled(ui.c, 'Project workflow broken') === undefined, 'an entry that cannot be reviewed is not offered');
  await ui.press(button(fresh, 'Review for first use…'));
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_review_library_entries', args:{libraryRef:LIB, listingRef:'listing-1', entryRefs:['entry-1']}}, 'reviewed singly');
  await ui.press(button(ui.c, 'Look for other workflows in this library'));
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_library_entries_refresh', args:{libraryRef:LIB}});
  const count = ui.calls.length;
  const labels = ['Reload this project\'s workflows', 'Review for first use…', 'Look for other workflows in this library'];
  const disabledAll = async (why, list = labels) => { for (const label of list) { const node = button(ui.c, label); assert.ok(node, `${why}: ${label}`); assert.equal(!!props(node).disabled, true, `${why}: ${label}`);
    await React.act(async () => props(node).onClick()); } };
  await ui.rerender({busy:true}); await disabledAll('busy');
  await ui.rerender({busy:false, host:{...host(), workflowRoot:{context:{sourceRef:'other', generation:g}}}}); await disabledAll('a stale workflow source');
  await ui.rerender({host:{...host(), state:'stopped'}}); await disabledAll('Codex not ready', ['Reload this project\'s workflows']);
  assert.equal(!!props(button(ui.c, 'Look for other workflows in this library')).disabled, false, 'the library\'s own list needs no Codex, as in the guide');
  assert.equal(ui.calls.length, count, 'a retained click on a disabled control dispatches nothing');
  // No project folder: nothing to show, and Desktop setup is named.
  await ui.rerender({host:host(), data:data({projectLibraryAvailable:false})});
  assert.equal(button(ui.c, 'Show this project\'s workflows'), undefined);
  assert.ok(all(ui.c, 'a').some(a => a.getAttribute('href') === '#desktop-setup'));
  await ui.close();
});

test('the result of the tab\'s own project commands is said in its words; another view\'s press is not', async () => {
  const ui = await mount({act:true, outcome:{command:'workflow_open_project_library', message:'{}', failed:false, settled:true}});
  assert.equal(labelled(ui.c, 'Workflows — last result').textContent.split('What the App reported')[0], "Opened this project's workflow library.");
  await ui.rerender({outcome:{command:'workflow_review_library_entries', message:'Error: Native history context is busy; refresh the workflow choice', failed:true, settled:true}});
  assert.match(labelled(ui.c, 'Workflows — last result').textContent, /^Couldn't open the review: the App was busy reading conversation history, so nothing was done\. Press the button again\./);
  await ui.rerender({outcome:{command:'workflow_end_run', message:'{}', failed:false, settled:true}});
  assert.equal(labelled(ui.c, 'Workflows — last result'), undefined, 'the Run tab\'s press is said there');
  await ui.rerender({outcome:{command:'workflow_open_project_library', message:'', failed:false, settled:false}});
  assert.equal(labelled(ui.c, 'Workflows — last result'), undefined, 'nothing is claimed before the result arrives');
  await ui.close();
});
