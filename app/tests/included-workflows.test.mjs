import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The included workflows as a person chooses among them in Run a workflow.
// Controlled catalogue views only: invented entries in the shape the host's
// productionCatalog gives; no native App, supplier, model or person act.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {IncludedWorkflows, includedSections, includedEntryOf, matchesSearch, librarySourceWords} = loadSrc('IncludedWorkflows');

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

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const chosen = [];
  const render = () => root.render(React.createElement(IncludedWorkflows, {catalog:view.catalog ?? catalog, chosen:view.chosen, disabled:!!view.disabled, needsConversation:!!view.needsConversation, choose:name => chosen.push(name)}));
  await React.act(async () => render());
  return {c, chosen, search:async value => React.act(async () => props(all(c, 'input')[0]).onChange({target:{value}})),
    rerender:async next => { Object.assign(view, next); await React.act(async () => render()); }, close:async () => React.act(async () => root.unmount())};
}

test('the list follows the Library\'s own grouping: core first, its groups in its order, ungrouped, then superseded', () => {
  const sections = includedSections(entries);
  assert.deepEqual(sections.map(s => [s.label, s.entries.map(e => e.name)]), [
    ['Start here', ['core-a', 'core-b']],
    ['Plan & organize', ['plan-work', 'broken']],
    ['Review & check', ['beta-check', 'alpha-check', 'zeta-check']],
    ['Other workflows', ['loose']],
    ['Replaced by newer workflows', ['old-way']],
  ], 'primary before supporting, then the Library\'s order');
  assert.equal(librarySourceWords(SOURCE), 'Chirality Library 9.9.9');
  assert.equal(librarySourceWords({tag:'other'}), 'Chirality Library (other)');
  assert.equal(librarySourceWords(undefined), '');
  assert.equal(matchesSearch(entries[3], 'ORDERED goal'), true, 'every word, any case, in name, description or group');
  assert.equal(matchesSearch(entries[3], 'ordered spacing'), false);
  assert.equal(matchesSearch(entries[0], 'review'), true, 'the group label is searched');
});

test('each included workflow shows its description, source and revision, and is chosen with the guide\'s own command', async () => {
  const ui = await mount({});
  const list = region(ui.c, 'Workflows included with the App');
  assert.match(list.textContent, /^Included with the App: 9 workflows from Chirality Library 9\.9\.9\./);
  const sections = all(list, 'details').filter(node => /\(\d+\)$/.test(all(node, 'summary')[0]?.textContent ?? ''));
  assert.deepEqual(sections.map(node => all(node, 'summary')[0].textContent), ['Start here (2)', 'Plan & organize (2)', 'Review & check (3)', 'Other workflows (1)', 'Replaced by newer workflows (1)']);
  assert.equal(props(sections[0]).open, true, 'the core workflows are open to begin with');
  assert.equal(props(sections[2]).open, undefined, 'other groups open when the person opens them');
  const row = region(ui.c, 'Included workflow core-a');
  assert.match(row.textContent, /^Begin a project \(core-a\) — Invented description of core-a\. Use core-a/, 'a display name keeps the workflow\'s own name beside it');
  assert.match(row.textContent, /Source: Chirality Library 9\.9\.9, included with the App\. Revision core-a-revis…/);
  assert.equal(all(row, 'code').find(node => node.getAttribute('title'))?.getAttribute('title'), 'core-a-revision-0123456789abcdef', 'the full revision is kept on the short one');
  const use = all(row, 'button')[0];
  await React.act(async () => props(use).onClick());
  assert.deepEqual(ui.chosen, ['core-a']);
  const broken = region(ui.c, 'Included workflow broken');
  assert.equal(all(broken, 'button').length, 0, 'a package the host does not admit offers no Use');
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
  const whole = region(ui.c, 'Workflows included with the App').textContent;
  assert.doesNotMatch(whole, /\bneed|requires?\b|required tool|must be|obtained from|\btools? that\b|needs no tools|available|missing/i, 'nothing states or implies a requirement, an availability or that a workflow needs no tools');
  assert.match(region(ui.c, 'Included workflow beta-check').textContent, /The Library marks it as legacy\./);
  const none = region(ui.c, 'Included workflow plan-work');
  assert.doesNotMatch(none.textContent, /files name|not included in the App/, 'an empty list says nothing');
  await ui.rerender({catalog:{...catalog, entries:[entry('one-path', {category:'core', tier:'primary', order:1}, {libraryPathsNamed:['agents/AGENT_TASK.md']})]}});
  assert.match(region(ui.c, 'Included workflow one-path').textContent, /This workflow's files name 1 path of Chirality Library 9\.9\.9 that is not included in the App \(for example agents\/AGENT_TASK\.md\)\. The App has not checked whether a run uses it\./, 'a role file is a path, not a tool');
  await ui.close();
});

test('search narrows the list and opens what matches; without a conversation nothing can be chosen and the list says why', async () => {
  const ui = await mount({needsConversation:true});
  const list = region(ui.c, 'Workflows included with the App');
  assert.match(list.textContent, /Choose a conversation above to use one\./);
  assert.ok(all(list, 'button').every(node => props(node).disabled === true));
  await ui.search('check review');
  assert.match(list.textContent, /3 of 9 match\./);
  const sections = all(list, 'details').filter(node => /\(\d+\)$/.test(all(node, 'summary')[0]?.textContent ?? ''));
  assert.deepEqual(sections.map(node => [all(node, 'summary')[0].textContent, props(node).open]), [['Review & check (3)', true]]);
  await ui.search('nothing-like-this');
  assert.match(list.textContent, /No included workflow matches\. Try fewer or other words\./);
  await ui.search('');
  await ui.rerender({needsConversation:false, chosen:selection('zeta-check')});
  const chosenRow = region(ui.c, 'Included workflow zeta-check');
  assert.match(chosenRow.textContent, /Chosen\./); assert.equal(all(chosenRow, 'button').length, 0);
  const review = all(list, 'details').find(node => all(node, 'summary')[0]?.textContent === 'Review & check (3)');
  assert.equal(props(review).open, true, 'the chosen workflow\'s group is open');
  await ui.rerender({chosen:selection('zeta-check', {origin:'project'})});
  assert.doesNotMatch(region(ui.c, 'Included workflow zeta-check').textContent, /Chosen\./, 'a same-named library workflow is not the included one');
  await ui.close();
});

// Review round 1: "Chosen." and the Library source were asserted from a match
// on origin, name and revision alone.
test('Chosen is said only of the entry the selection is by its whole identity, and only when the host admits it to run', async () => {
  // A library holding copy with the bundle's identity: the host keeps it not runnable.
  const ui = await mount({chosen:selection('zeta-check', {}, false)});
  const row = () => region(ui.c, 'Included workflow zeta-check');
  assert.doesNotMatch(row().textContent, /Chosen\./, 'a copy the host does not admit is not the included workflow chosen');
  const use = all(row(), 'button').find(node => node.textContent === 'Use zeta-check');
  assert.ok(use && props(use).disabled === false, 'the runnable included entry keeps its Use');
  await React.act(async () => props(use).onClick());
  assert.deepEqual(ui.chosen, ['zeta-check']);
  // Each identity field that differs makes it another workflow.
  for (const over of [{source_root:'chirality-root'}, {revision:'another-revision'}, {revision_method:'other/v1'}, {kind:'other'}, {origin:'user'}]) {
    await ui.rerender({chosen:selection('zeta-check', over)});
    assert.doesNotMatch(row().textContent, /Chosen\./, JSON.stringify(over));
    assert.ok(all(row(), 'button').some(node => node.textContent === 'Use zeta-check'), JSON.stringify(over));
  }
  assert.equal(includedEntryOf(catalog, selection('zeta-check'))?.name, 'zeta-check');
  assert.equal(includedEntryOf(catalog, selection('zeta-check', {source_root:'chirality-root'})), undefined, 'the development holding copy is not a catalogue entry');
  assert.equal(includedEntryOf(catalog, {identity:null}), undefined);
  assert.equal(includedEntryOf({entries:[{name:'zeta-check', revision:'zeta-check-revision-0123456789abcdef'}]}, selection('zeta-check')), undefined, 'an entry without the host\'s identity matches nothing');
  await ui.rerender({chosen:selection('zeta-check')});
  assert.match(row().textContent, /Chosen\./); assert.equal(all(row(), 'button').length, 0);
  await ui.close();
});

test('a search that is active when the catalogue becomes short can still be cleared', async () => {
  const view = {};
  const ui = await mount(view);
  await ui.search('nothing-like-this');
  await ui.rerender({catalog:{...catalog, entries:[entries[0]]}});
  const list = region(ui.c, 'Workflows included with the App');
  assert.match(list.textContent, /No included workflow matches/);
  assert.equal(all(list, 'input').length, 1, 'the search field stays while a search is active');
  await ui.search('');
  assert.ok(region(ui.c, 'Included workflow zeta-check'));
  assert.equal(all(region(ui.c, 'Workflows included with the App'), 'input').length, 0);
  await ui.close();
});

test('a short catalogue is one plain list with no search, and a catalogue without the Library fields still lists its workflow', async () => {
  const bare = {standing:'s', entries:[{name:'coordinated-knowledge-work', revision:'3730d84debb5d775', runnable:true}]};
  const ui = await mount({catalog:bare});
  const list = region(ui.c, 'Workflows included with the App');
  assert.match(list.textContent, /^Included with the App: 1 workflow\./);
  assert.equal(all(list, 'input').length, 0);
  assert.equal(all(list, 'button')[0].textContent, 'Use coordinated-knowledge-work');
  assert.match(list.textContent, /Source: included with the App\. Revision 3730d84debb5…/);
  await ui.rerender({catalog:{standing:'s', entries:[{name:'unreported', revision:'r'}]}});
  const unreported = region(ui.c, 'Included workflow unreported');
  assert.equal(all(unreported, 'button').length, 0);
  assert.match(unreported.textContent, /The App hasn't reported whether this workflow can be used here\./, 'an unreported admission is neither usable nor refused');
  await ui.close();
  const none = await mount({catalog:{entries:[]}});
  assert.equal(region(none.c, 'Workflows included with the App'), undefined);
  await none.close();
});
