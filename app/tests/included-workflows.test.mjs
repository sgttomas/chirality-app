import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The included workflows as a person picks among them in the Workflows tab (WorkflowLibrary.tsx), which took them over
// from the Run a workflow guide's list. Controlled catalogue views only: invented entries in the shape the host's
// productionCatalog gives; no native App, supplier, model or person act.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {RoleBesideWorkflow, includedSections, includedEntryOf, matchesSearch, librarySourceWords, LIBRARY_GROUPS} = loadSrc('IncludedWorkflows');

const SOURCE = {repository:'https://example.invalid/library', tag:'library-v9.9.9', commit:'c0ffee'};
const ROOT = 'invented-library:library-v9.9.9', METHOD = 'invented.package.sha256/v1';
const identity = (name, over = {}) => ({kind:'workflow', origin:'bundled', source_root:ROOT, name, revision:`${name}-revision-0123456789abcdef`, revision_method:METHOD, derived_from:null, ...over});
// A selection as the host reports it for a conversation: its identity and whether the host admits it to run.
const selection = (name, over = {}, runnable = true) => ({state:'selected', reference:'sel', runnable, runLimit:runnable ? null : 'not resolved from the installed App resources', identity:identity(name, over)});
const entry = (name, navigation, over = {}) => ({name, revision:`${name}-revision-0123456789abcdef`, origin:'bundled', sourceRoot:ROOT, revisionMethod:METHOD, identity:identity(name), runnable:true, runLimit:null,
  description:`Invented description of ${name}.`, central:false, compatibility:'canonical', roles:['HELP_HUMAN'], navigation, libraryExecution:null, libraryPathsNamed:[], ...over});
const group = (key, label, order) => ({key, label, order});
const REVIEW = group('review-check', 'Review & check', 5), PLAN = group('plan-organize', 'Plan & organize', 1);
const entries = [
  entry('zeta-check', {category:'specialist', tier:'supporting', order:1, group:REVIEW}),
  entry('alpha-check', {category:'specialist', tier:'primary', order:2, group:REVIEW}, {libraryPathsNamed:['tools/validation/check_a.py', 'tools/validation/check_b.py'], roles:['TASK']}),
  entry('beta-check', {category:'specialist', tier:'primary', order:1, group:REVIEW}, {compatibility:'legacy'}),
  entry('plan-work', {category:'specialist', tier:'primary', order:1, group:PLAN}, {description:'Turn a goal into ordered work.'}),
  entry('core-b', {category:'core', tier:'primary', order:2}),
  entry('core-a', {category:'core', tier:'primary', order:1, displayName:'Begin a project'}),
  entry('old-way', {category:'superseded', tier:'primary', order:1}),
  entry('loose', {category:'specialist', tier:'primary', order:1}),
  entry('broken', {category:'specialist', tier:'primary', order:9, group:PLAN}, {runnable:false, runLimit:'its files differ from the release'}),
];
const catalog = {standing:'invented standing', source:SOURCE, entries};
const {WorkflowLibrary} = loadSrc('WorkflowLibrary');
const g = {home:'account', appSession:'s1', spawnCounter:1};
const host = {state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}}, serverRequests:[], threads:[]};

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const included = c => c.querySelectorAll(node => node.getAttribute('aria-labelledby') === 'method-group-included')[0];
const subgroups = c => all(included(c), 'details').filter(node => node.getAttribute('class') === 'method-library-subgroup');
const heading = node => `${all(node, 'h4')[0].textContent} (${node.querySelectorAll(n => n.getAttribute('class') === 'method-library-count')[0].textContent})`;
async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const picked = [];
  const render = () => root.render(React.createElement(WorkflowLibrary, {data:{context:{sourceRef:'src', generation:g}, productionCatalog:view.catalog ?? catalog, libraries:[], selections:view.chosen ? [{sourceRef:'src', threadId:'T1', selection:view.chosen}] : []},
    host, busy:false, pick:view.pick ?? null, setPick:next => { picked.push(next); view.pick = next; render(); }}));
  await React.act(async () => render());
  return {c, picked, search:async value => React.act(async () => props(all(c, 'input').find(n => props(n)?.type === 'search')).onChange({target:{value}})),
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); }, close:async () => React.act(async () => root.unmount())};
}

test('each included workflow shows its description, source and revision, and is picked for the next message', async () => {
  const ui = await mount({});
  assert.deepEqual(subgroups(ui.c).map(heading), ["The Library's core workflows (2)", 'Plan & organize (2)', 'Review & check (3)', 'Other workflows (1)', 'Marked superseded by the Library (1)']);
  assert.equal(props(subgroups(ui.c)[0]).open, true, 'the core workflows are open to begin with');
  assert.equal(props(subgroups(ui.c)[2]).open, undefined, 'other groups open when the person opens them');
  const row = region(ui.c, 'Included workflow core-a');
  assert.match(row.textContent, /^Begin a projectcore-aInvented description of core-a\.Chirality Library 9\.9\.9/, 'a display name keeps the workflow\'s own name beside it, then its description and source');
  assert.match(row.textContent, /Revision core-a-revis…/);
  assert.equal(all(row, 'code').find(node => node.textContent.startsWith('core-a-revis'))?.getAttribute('title'), 'core-a-revision-0123456789abcdef', 'the full revision is kept on the short one');
  await React.act(async () => props(all(row, 'button').find(b => b.textContent === 'Use in message')).onClick());
  assert.deepEqual(ui.picked.map(p => [p.kind, p.name, p.revision]), [['included', 'core-a', 'core-a-revision-0123456789abcdef']], 'picked by name and revision; the composer\'s Start run chooses it with the guide\'s own command');
  const broken = region(ui.c, 'Included workflow broken');
  assert.equal(!!props(all(broken, 'button').find(b => b.textContent === 'Use in message')).disabled, true, 'a package the host does not admit cannot be picked');
  assert.match(broken.textContent, /Can't be used in this App: its files differ from the release\./);
  await ui.close();
});

test('named Library paths are a statement of what the files name, never a requirement, and an empty list says nothing', async () => {
  const ui = await mount({});
  const named = region(ui.c, 'Included workflow alpha-check');
  assert.match(named.textContent, /This workflow's files name 2 paths of Chirality Library 9\.9\.9 that are not included in the App \(for example tools\/validation\/check_a\.py\)\. The App has not checked whether a run uses them\./);
  assert.match(named.textContent, /All 2 pathstools\/validation\/check_a\.pytools\/validation\/check_b\.py/);
  assert.match(named.textContent, /The Library lists it for these roles: TASK\./);
  // Review round 1: the sentence said steps "need those files present" and what "a run requires". The field establishes neither.
  const whole = included(ui.c).textContent;
  assert.doesNotMatch(whole, /\bneed|requires?\b|required tool|must be|obtained from|\btools? that\b|needs no tools|available|missing/i, 'nothing states or implies a requirement, an availability or that a workflow needs no tools');
  assert.match(region(ui.c, 'Included workflow beta-check').textContent, /The Library marks it as legacy\./);
  const none = region(ui.c, 'Included workflow plan-work');
  assert.doesNotMatch(none.textContent, /files name|not included in the App/, 'an empty list says nothing');
  await ui.rerender({catalog:{...catalog, entries:[entry('one-path', {category:'core', tier:'primary', order:1}, {libraryPathsNamed:['agents/AGENT_TASK.md']})]}});
  assert.match(region(ui.c, 'Included workflow one-path').textContent, /This workflow's files name 1 path of Chirality Library 9\.9\.9 that is not included in the App \(for example agents\/AGENT_TASK\.md\)\. The App has not checked whether a run uses it\./, 'a role file is a path, not a tool');
  await ui.close();
});

test('search narrows the list and opens what matches; the picked workflow\'s group is open', async () => {
  const ui = await mount({});
  await ui.search('check review');
  assert.match(ui.c.textContent, /3 match\./);
  assert.deepEqual(subgroups(ui.c).map(node => [heading(node), props(node).open]), [['Review & check (3)', true]]);
  await ui.search('nothing-like-this');
  assert.match(ui.c.textContent, /No workflow matches\. Try fewer or other words\./);
  await ui.search('');
  await ui.rerender({pick:{kind:'included', name:'zeta-check', revision:'zeta-check-revision-0123456789abcdef', title:'zeta-check', from:'', scope:''}});
  const review = subgroups(ui.c).find(node => all(node, 'h4')[0].textContent === 'Review & check');
  assert.equal(props(review).open, true, 'the picked workflow\'s group is open');
  assert.equal(all(region(ui.c, 'Included workflow zeta-check'), 'button').find(b => b.getAttribute('aria-pressed') === 'true')?.textContent, 'Remove');
  await ui.close();
});

// Review round 1: "Chosen." and the Library source were asserted from a match on origin, name and revision alone.
test('an included entry is the selection only by its whole identity; a conversation\'s selection marks no card', async () => {
  assert.equal(includedEntryOf(catalog, selection('zeta-check'))?.name, 'zeta-check');
  for (const over of [{source_root:'chirality-root'}, {revision:'another-revision'}, {revision_method:'other/v1'}, {kind:'other'}, {origin:'user'}])
    assert.equal(includedEntryOf(catalog, selection('zeta-check', over)), undefined, JSON.stringify(over));
  assert.equal(includedEntryOf(catalog, {identity:null}), undefined);
  assert.equal(includedEntryOf({entries:[{name:'zeta-check', revision:'zeta-check-revision-0123456789abcdef'}]}, selection('zeta-check')), undefined, 'an entry without the host\'s identity matches nothing');
  // The tab is about the next message: a conversation's selection, admitted or not, presses no card and keeps its Use.
  for (const chosen of [selection('zeta-check'), selection('zeta-check', {}, false)]) {
    const ui = await mount({chosen});
    const row = region(ui.c, 'Included workflow zeta-check');
    assert.doesNotMatch(row.textContent, /Chosen/);
    const use = all(row, 'button').find(node => node.textContent === 'Use in message');
    assert.ok(use && !props(use).disabled, 'the runnable included entry keeps its Use in message');
    await ui.close();
  }
});

test('the search stays while the catalogue becomes short, and can be cleared', async () => {
  const view = {};
  const ui = await mount(view);
  await ui.search('nothing-like-this');
  await ui.rerender({catalog:{...catalog, entries:[entries[0]]}});
  assert.match(ui.c.textContent, /No workflow matches/);
  await ui.search('');
  assert.ok(region(ui.c, 'Included workflow zeta-check'));
  await ui.close();
});

test('a catalogue without the Library fields still lists its workflow; an unreported admission is neither usable nor refused', async () => {
  const bare = {standing:'s', entries:[{name:'coordinated-knowledge-work', revision:'3730d84debb5d775', runnable:true}]};
  const ui = await mount({catalog:bare});
  const row = region(ui.c, 'Included workflow coordinated-knowledge-work');
  assert.ok(row);
  assert.equal(!!props(all(row, 'button').find(b => b.textContent === 'Use in message')).disabled, false);
  assert.match(row.textContent, /Included with the App/);
  assert.match(row.textContent, /Revision 3730d84debb5…/);
  await ui.rerender({catalog:{standing:'s', entries:[{name:'unreported', revision:'r'}]}});
  const unreported = region(ui.c, 'Included workflow unreported');
  assert.equal(!!props(all(unreported, 'button').find(b => b.textContent === 'Use in message')).disabled, true);
  assert.match(unreported.textContent, /The App hasn't reported whether this workflow can be used here\./, 'an unreported admission is neither usable nor refused');
  await ui.close();
  const none = await mount({catalog:{entries:[]}});
  assert.equal(subgroups(none.c).length, 0, 'no entries, no group');
  await none.close();
});

test('the conversation\'s role is shown beside the roles the Library lists for the chosen workflow, with no judgment of fit', async () => {
  const {renderToStaticMarkup} = await import('react-dom/server');
  const h = props => renderToStaticMarkup(React.createElement(RoleBesideWorkflow, props)).replace(/<[^>]+>/g, '').replaceAll('&#x27;', "'");
  const listed = entry('alpha-check', {category:'specialist'}, {roles:['TASK', 'WORKING_ITEMS']});
  const conversation = appRole => ({threadId:'chat-1', appRole});
  assert.equal(h({entry:listed, conversation:conversation({standing:'app-observed', role:'HELP_HUMAN', supply_ref:'sup:1'})}),
    'This conversation is in the role HELP_HUMAN. The Library lists alpha-check for: TASK, WORKING_ITEMS.', 'a role the workflow is not listed for is shown as the two facts, not as a refusal or a warning');
  assert.equal(h({entry:listed, conversation:conversation({standing:'app-observed', role:null})}), 'This conversation was started with no role. The Library lists alpha-check for: TASK, WORKING_ITEMS.');
  // A role this App process did not establish is not known, whatever else the row says.
  for (const unknown of [conversation({standing:'unknown', reason:'original App supply binding not established'}), conversation(undefined), undefined, {threadId:'chat-1', appRole:{role:'HELP_HUMAN'}}])
    assert.equal(h({entry:listed, conversation:unknown}), "This conversation's role is not known to this App process. The Library lists alpha-check for: TASK, WORKING_ITEMS.");
  // Only the catalogue carries the Library's list: no entry, or an entry with no roles, says nothing.
  assert.equal(h({entry:undefined, conversation:conversation({standing:'app-observed', role:'HELP_HUMAN'})}), '');
  assert.equal(h({entry:entry('plain', {}, {roles:[]}), conversation:conversation({standing:'app-observed', role:'HELP_HUMAN'})}), '');
  assert.equal(h({entry:entry('plain', {}, {roles:undefined}), conversation:conversation({standing:'app-observed', role:'HELP_HUMAN'})}), '');
});
