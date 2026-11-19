// The left panel from the host's navigator read (Navigator.tsx; navigator_read.rs "What the read returns"), on
// constructed read answers only: every project in the read's order, the open project's runs in each state, runs not
// read for each reason and the busy rule over successive readings, limits, conversations of no project, homes not
// read, titles (untitled, equal, imitating the App's words), "Needs answer" from the same records "Waiting on you"
// counts, failed readings, and what choosing an entry does. Invented material only; no supplier, model or person act.
process.env.TZ = 'UTC';
import test from 'node:test';
import assert from 'node:assert/strict';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const nav = loadSrc('Navigator');
const {Navigator, NO_NAVIGATOR_READ, navigatorAfterRead, ROOT_BUSY, BUSY_READINGS, placeRequests, whenWords, runWord, entryOpen, NOT_OPEN_PROJECT, OTHER_HOME, NOT_CURRENT} = nav;
const {App, NAVIGATOR_READ_MS} = loadSrc('App');
const {waitingEntries} = loadSrc('WaitingOnYou');

// The host's own sentences (navigator_read.rs, runtime_session.rs, records_store.rs), as the read gives them.
const RUNS_NOT_YET = "Chirality has not yet read this project's recorded runs in this running App.";
const RUNS_FAILED = "The project's recorded runs could not be read.";
const HISTORY_CHANGED = "Whether records in the project folder are left out of this view is not known: where this project's records are kept changed while it was being read.";
const NOT_OPEN_RUNS = "Chirality reads a project's recorded runs once the project is open in this running App.";
const RUN_PENDING = 'An operation on this run is in progress in this running App, so its state is not known at this moment.';

const g = {home:'account', appSession:'s1', spawnCounter:1};
const earlier = {...g, spawnCounter:0};
const NOW = Date.parse('2026-11-19T12:00:00.000Z');
const PUMP = '/invented/projects/pump-station', HARBOUR = '/invented/projects/harbour', DEPOT = '/invented/projects/depot';

const workflow = name => ({name, title:null, origin:'included with the App', release:'Chirality Library 3.4.0'});
const run = (state, over = {}) => ({runId:`run-${state}`, workflow:workflow('define-work'), state, stateReason:null, endedBy:null, finishedReported:null, resultCount:null, ...over});
const loaded = (id, generation = g) => ({kind:'loaded', generation, threadId:id});
const history = id => ({kind:'history', home:'account', generation:g, selectionEpoch:3, threadId:id});
const entry = (id, over = {}) => ({id, home:'account', projectRoot:PUMP, projectSource:'recorded', title:`Chat ${id}`, titleSource:'name', createdAt:null,
  updatedAt:'2026-11-19T11:00:00.000Z', live:'idle', needsAnswer:0, needsAnswerOn:[], archived:false, open:loaded(id), run:null, runCount:0, childrenRunning:null, ...over});
const read = state => ({state, readAt:'2026-11-19T09:00:00.000Z', limits:[]});
const notRead = reason => ({state:'not-read', reason, readAt:null, limits:[]});
const project = (root, label, over = {}) => ({projectId:`P-${label}`, root, label, current:false, state:'listed', notice:null, runsRead:notRead(NOT_OPEN_RUNS), unplacedRuns:0, entries:[], ...over});
const open = (entries, over = {}) => project(PUMP, 'pump-station', {current:true, state:'open', runsRead:read('read'), entries, ...over});
const answer = (projects, over = {}) => ({readAt:'2026-11-19T12:00:00.000Z', projects, unassigned:[], registryLimits:[], unplacedRequests:[],
  conversations:[{home:'account', list:'saved conversations, not archived, as Codex listed them when it became ready', readAt:null, state:'read'}], ...over});
const held = (...answers) => answers.reduce((h, a, i) => navigatorAfterRead(h, a instanceof Error ? {failed:true, at:NOW + i * 2000} : {read:a, at:NOW + i * 2000}), NO_NAVIGATOR_READ);

/** A person-answerable request as "Waiting on you" holds it: its own conversation, and the one it descends from. */
const waiting = (kind, own, root = own, home = 'account', count = 1) => ({key:JSON.stringify([kind, own, root, home]), source:home === 'account' ? 'supplier-request' : 'waiting-overview',
  kind, count, asker:{kind:'request', asker:null}, responder:'you', concerns:{kind:'conversation', threadId:own, home}, integrator:'not recorded',
  group:{key:JSON.stringify(['conversation', home, root]), label:{kind:'conversation', threadId:root, home, otherHome:home !== 'account'}}, asOf:null,
  target:{kind:'request', group:{modeHomeClass:home, generation:g, threadId:own, count}, anchor:null}});

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, match) => c.querySelectorAll(match);
const cls = name => n => (n.getAttribute('class') ?? '').split(' ').includes(name);
const rows = c => all(c, n => n.localName === 'button' && cls('woven-navigator-session')(n));
const row = (c, id) => rows(c).find(b => b.getAttribute('data-session-id') === id);
const marks = (c, id, text) => row(c, id).parentNode.childNodes.filter(b => b.localName === 'button' && b.textContent === text);
const sectionOf = (c, label) => all(c, n => n.localName === 'section' && (n.textContent ?? '').includes(label))[0];
/** The accessible name the button's content gives: its text, leaving out what is hidden from assistive technology. */
const accessibleName = node => node.nodeType === 3 ? node.textContent : node.getAttribute?.('aria-hidden') === 'true' ? '' : node.childNodes.map(accessibleName).join('');
const notes = c => all(c, n => cls('woven-navigator-session-notice')(n) || cls('woven-folder-notice')(n)).map(n => n.textContent);

async function draw(h, check, over = {}) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const did = {choose:[], history:[], answer:[]};
  const render = (heldNow, more = {}) => React.act(async () => root.render(React.createElement(Navigator, {held:heldNow, waiting:[], now:NOW, activeHome:'account', generation:g, statusCurrent:true, selectedThread:null,
    choose:key => did.choose.push(key), openInHistory:o => did.history.push(o), answer:e => did.answer.push(e), newChat() {}, openSettings() {}, ...over, ...more})));
  try { await render(h); await check({c, did, render}); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(c); }
}
const unfold = async (c, label) => { const b = all(sectionOf(c, label), n => n.localName === 'button' && cls('v4-nav-fold')(n))[0]; await React.act(async () => props(b).onClick()); };

// ---- Successive readings ----

test('the busy rule: the run lines last shown stay through one and two busy readings, the sentence shows at the third, and the next reading recovers', () => {
  const good = answer([open([entry('A', {run:run('open'), runCount:2}), entry('B')])]);
  const busy = (entries = [entry('A', {title:'Renamed'}), entry('B'), entry('N')]) => answer([open(entries, {runsRead:notRead(ROOT_BUSY), unplacedRuns:0})]);
  let h = held(good);
  const runsOf = state => state.read.projects[0].entries.map(e => [e.id, e.run?.state ?? null, e.runCount]);
  assert.deepEqual(runsOf(h), [['A', 'open', 2], ['B', null, 0]]);
  for (let n = 1; n < BUSY_READINGS; n++) {
    h = navigatorAfterRead(h, {read:busy(), at:NOW + n});
    assert.deepEqual(runsOf(h), [['A', 'open', 2], ['B', null, 0], ['N', null, 0]], `reading ${n}: the run lines last shown, nothing new`);
    assert.deepEqual(h.read.projects[0].runsRead, read('read'), `reading ${n}: the reading last shown, not the busy sentence`);
    assert.equal(h.read.projects[0].entries[0].title, 'Renamed', `reading ${n}: the conversations are this answer's`);
    assert.equal(h.busy[PUMP], n);
  }
  h = navigatorAfterRead(h, {read:busy(), at:NOW + 9});
  assert.deepEqual(h.read.projects[0].runsRead, notRead(ROOT_BUSY), 'the third busy reading in a row is said');
  assert.deepEqual(runsOf(h), [['A', null, 0], ['B', null, 0], ['N', null, 0]], 'and no earlier run line is kept as current');
  h = navigatorAfterRead(h, {read:good, at:NOW + 10});
  assert.deepEqual(runsOf(h), [['A', 'open', 2], ['B', null, 0]], 'recovered');
  assert.deepEqual(h.busy, {}, 'the count starts again');
  // A busy first reading keeps nothing, and shows no sentence before the third.
  const first = navigatorAfterRead(NO_NAVIGATOR_READ, {read:busy([entry('A')]), at:NOW});
  assert.equal(first.read.projects[0].runsRead, null);
  // A failed reading between busy ones does not break the count: it is not a reading.
  let f = held(good, busy(), new Error('x'), busy());
  assert.equal(f.busy[PUMP], 2);
});

test('every other reason a project\'s runs are not read is shown at once, whole, and no earlier run line is kept', () => {
  for (const reason of [RUNS_NOT_YET, RUNS_FAILED, HISTORY_CHANGED, NOT_OPEN_RUNS]) {
    const h = held(answer([open([entry('A', {run:run('open'), runCount:1})])]), answer([open([entry('A')], {runsRead:notRead(reason)})]));
    assert.deepEqual(h.read.projects[0].runsRead, notRead(reason), reason);
    assert.equal(h.read.projects[0].entries[0].run, null, reason);
    assert.deepEqual(h.busy, {});
  }
});

test('a failed reading keeps what is shown and says when; an answer not of the read\'s shape counts as failed', () => {
  const good = answer([open([entry('A')])]);
  const h = held(good, new Error('x'));
  assert.deepEqual(h.read, held(good).read, 'the earlier answer stays');
  assert.equal(h.failedAt, NOW + 2000);
  assert.equal(held(good, {projects:[]}).failedAt, NOW + 2000, 'missing arrays: not taken as an answer with no projects');
  assert.equal(held(good, {projects:[]}).read.projects.length, 1);
  assert.equal(held(good, new Error('x'), good).failedAt, null, 'a good reading clears it');
});

// ---- Drawing the read ----

test('several projects in the read\'s order: the open one first and unfolded, the others folded with their counts; unfolded, a project not open says so and offers nothing to choose', async () => {
  const h = held(answer([open([entry('A'), entry('B')]), project(HARBOUR, 'harbour', {entries:[entry('H1', {open:history('H1')}), entry('H2', {open:history('H2')})]}), project(DEPOT, 'depot')]));
  await draw(h, async ({c, did}) => {
    const headings = all(c, cls('woven-chat-section-heading--folder'));
    assert.deepEqual(headings.map(n => n.childNodes[0].textContent), ['▱ pump-station · current', '▱ harbour', '▱ depot'], 'the read\'s order; the folder\'s name is text, never in a control');
    assert.ok(headings.every(n => n.localName === 'div' && all(n, b => b.localName === 'button').every(b => !b.textContent.includes('harbour') && !b.textContent.includes('pump'))));
    assert.deepEqual(rows(c).map(b => b.getAttribute('data-session-id')), ['A', 'B'], 'only the open project is unfolded at first');
    assert.ok(headings[1].textContent.includes('2'), 'a folded project shows its count');
    await unfold(c, 'harbour');
    assert.deepEqual(rows(c).map(b => b.getAttribute('data-session-id')), ['A', 'B', 'H1', 'H2']);
    assert.ok(notes(c).includes(NOT_OPEN_RUNS), 'the host\'s sentence, whole');
    assert.ok(notes(c).includes(NOT_OPEN_PROJECT), 'the App\'s sentence once for the project');
    assert.ok(props(row(c, 'H1')).disabled, 'it does not look like a working choice');
    assert.match(row(c, 'H1').getAttribute('aria-description'), /Not opened from here/);
    await unfold(c, 'harbour');
    assert.deepEqual(rows(c).map(b => b.getAttribute('data-session-id')), ['A', 'B'], 'folded again');
    await React.act(async () => props(row(c, 'A')).onClick());
    assert.deepEqual(did.choose, [JSON.stringify([g, 'A'])], 'a loaded conversation is chosen in the conversation view');
  });
});

test('the open project\'s runs: each state in a word in the App\'s mark, the run count, and an unknown state\'s reason shown whole', async () => {
  const entries = [
    entry('W', {live:'running', run:run('open'), runCount:1}),
    entry('Y', {live:'idle', run:run('open'), runCount:3}),
    entry('L', {live:'not-loaded', open:history('L'), run:run('open'), runCount:1}),
    entry('F', {live:'idle', run:run('open', {finishedReported:true}), runCount:1}),
    entry('O', {live:'unknown', run:run('open'), runCount:1}),
    entry('E', {run:run('ended', {endedBy:{stoppedBy:'person', cause:'completed'}}), runCount:2}),
    entry('S', {run:run('start-not-confirmed'), runCount:1}),
    entry('U', {run:run('unknown', {stateReason:RUN_PENDING}), runCount:1}),
    entry('N'),
  ];
  await draw(held(answer([open(entries)])), async ({c}) => {
    const word = id => all(row(c, id), cls('v4-nav-mark')).map(n => n.textContent);
    assert.deepEqual(['W', 'Y', 'L', 'F', 'O', 'E', 'S', 'U', 'N'].map(word), [['Working'], ['Your move'], ['Your move'], ['Agent says finished'], ['Open'], ['Ended'], ['Start not confirmed'], ['State not known'], []]);
    assert.ok(all(row(c, 'W'), cls('woven-navigator-session-dot')).length === 1, 'a running turn\'s mark');
    assert.match(row(c, 'Y').textContent, /define-work · Your move · 3 runs$/);
    assert.doesNotMatch(row(c, 'W').textContent, /runs/, 'one run: no count');
    assert.ok(notes(c).includes(RUN_PENDING), 'the reason the record leaves it unknown, whole');
    assert.ok(accessibleName(row(c, 'F')).startsWith('Agent says finished. Title: Chat F'), 'the state word first in the name');
    assert.match(row(c, 'Y').getAttribute('aria-description'), /Latest run: define-work; 3 runs in this conversation\./);
  });
});

test('a project whose runs are not read says why, whole, for each reason; a limited reading keeps its limits behind a disclosure, and unplaced runs are said', async () => {
  for (const reason of [RUNS_NOT_YET, RUNS_FAILED, HISTORY_CHANGED]) {
    await draw(held(answer([open([entry('A')], {runsRead:notRead(reason)})])), async ({c}) => assert.ok(notes(c).includes(reason), reason));
  }
  const limits = ['This project\'s records are kept in the records store. Records in the project folder have not been imported and may not be shown in this view.',
    '1 recorded run of this project names no conversation, so it is not shown under any conversation.'];
  await draw(held(answer([open([entry('A', {run:run('open'), runCount:1})], {runsRead:{state:'limited', readAt:'2026-11-19T09:00:00.000Z', limits}, unplacedRuns:1})])), async ({c}) => {
    const details = all(c, cls('v4-nav-limits'))[0];
    assert.equal(all(details, n => n.localName === 'summary')[0].textContent, 'Runs read with limits');
    assert.deepEqual(all(details, n => n.localName === 'p').map(p => p.textContent), limits, 'each limit whole');
    assert.ok(notes(c).includes('1 recorded run of this project is not shown under any conversation.'));
    assert.deepEqual(all(row(c, 'A'), cls('v4-nav-mark')).map(n => n.textContent), ['Your move'], 'the runs that were read are shown');
  });
  // The busy sentence only at the third busy reading.
  const busy = answer([open([entry('A')], {runsRead:notRead(ROOT_BUSY)})]);
  await draw(held(answer([open([entry('A', {run:run('open'), runCount:1})])]), busy, busy), async ({c, render}) => {
    assert.ok(!notes(c).includes(ROOT_BUSY)); assert.equal(all(row(c, 'A'), cls('v4-nav-mark')).length, 1, 'the run line last shown');
    await render(held(answer([open([entry('A', {run:run('open'), runCount:1})])]), busy, busy, busy));
    assert.ok(notes(c).includes(ROOT_BUSY)); assert.equal(all(row(c, 'A'), cls('v4-nav-mark')).length, 0);
  });
});

test('conversations of no project, a home whose conversations were not read, registry limits, and no projects yet', async () => {
  const homeReason = 'Codex is not running for this home, so its conversations were not read.';
  const registry = "The records store's list of project folders ends in an incomplete line; the folders before it are listed.";
  await draw(held(answer([open([entry('A')])], {unassigned:[entry('Z', {projectRoot:null, projectSource:'reported-folder', open:history('Z')})],
    conversations:[{home:'account', list:'x', readAt:null, state:'read'}, {home:'api-key', list:'x', readAt:null, state:'not-read', reason:homeReason}], registryLimits:[registry]})), async ({c, did}) => {
    const heading = all(c, n => n.localName === 'button' && cls('woven-chat-section-heading')(n))[0];
    assert.equal(heading.textContent, 'Conversations without a project1', 'the App\'s heading is its own fold control');
    assert.ok(notes(c).includes(`The API key home: ${homeReason}`));
    assert.ok(notes(c).includes(registry));
    await React.act(async () => props(row(c, 'Z')).onClick());
    assert.deepEqual(did.history, [{kind:'history', generation:g, selectionEpoch:3, threadId:'Z'}], 'a stored conversation of no project opens in History');
    assert.match(row(c, 'Z').getAttribute('aria-description'), /Opens in History, where it can be continued\./);
  });
  await draw(held(answer([])), async ({c}) => {
    assert.match(c.textContent, /No projects or conversations yet\. New chat starts one\./);
  });
});

test('before any reading the panel says it is reading; a failed first reading never says there are no projects; a failed later one keeps the list as of its time', async () => {
  await draw(NO_NAVIGATOR_READ, async ({c, render}) => {
    assert.match(c.textContent, /Reading your projects and conversations…/);
    await render(held(new Error('x')));
    assert.match(c.textContent, /could not be read at 12:00:00; the App reads them again shortly\./);
    assert.doesNotMatch(c.textContent, /No projects/);
    await render(held(answer([open([entry('A')])]), new Error('x')));
    assert.ok(row(c, 'A'), 'still listed');
    assert.match(c.textContent, /Shown as read at 12:00:00; the reading at 12:00:02 failed\./);
  });
  await draw(held(answer([open([entry('A')])])), async ({c}) => assert.match(c.textContent, /Shown as read at 12:00:00; a newer reading has not answered yet\./), {now:NOW + 11_000});
});

test('titles: the title alone on one line in the navigator\'s type, "Untitled chat" with its time, equal titles told apart by their times and then by entry number', async () => {
  const entries = [
    entry('U', {title:null, titleSource:'none', updatedAt:'2026-11-18T10:00:00.000Z'}),
    entry('S1', {title:'Pump sizing', updatedAt:'2026-11-19T10:05:00.000Z'}),
    entry('S2', {title:'Pump sizing', updatedAt:'2026-11-19T10:06:00.000Z'}),
    entry('Q1', {title:'Valve list', updatedAt:'2026-11-12T09:00:10.000Z'}),
    entry('Q2', {title:'Valve list', updatedAt:'2026-11-12T09:00:40.000Z'}),
    entry('T', {title:'Today', updatedAt:'2026-11-19T11:30:00.000Z'}),
  ];
  await draw(held(answer([open(entries)])), async ({c}) => {
    const when = id => all(row(c, id), cls('woven-navigator-session-when'))[0].textContent;
    assert.equal(all(row(c, 'U'), cls('v4-nav-untitled'))[0].textContent, 'Untitled chat');
    assert.equal(when('U'), 'Wed', 'yesterday, by its weekday');
    assert.match(row(c, 'U').getAttribute('aria-description'), /^No title supplied\. Updated Wed\./);
    assert.equal(when('T'), '11:30');
    assert.deepEqual([when('S1'), when('S2')], ['Nov 19, 10:05', 'Nov 19, 10:06'], 'the same title: their times to the minute');
    assert.deepEqual([when('Q1'), when('Q2')], ['Nov 12, 09:00', 'Nov 12, 09:00']);
    assert.match(row(c, 'Q1').getAttribute('aria-description'), /Entry 4 in this list\./, 'equal times: the entry number in the description');
    assert.match(row(c, 'Q2').getAttribute('aria-description'), /Entry 5 in this list\./);
    assert.doesNotMatch(row(c, 'S1').getAttribute('aria-description'), /Entry/);
    assert.match(row(c, 'T').getAttribute('aria-description'), /^Title supplied by Codex\. Updated 11:30\.$/, 'who supplied the title, said once, in the description');
    assert.doesNotMatch(c.textContent, /supplied by Codex|invented-model|openai/, 'no attribution sentence, model or provider in the list');
  });
  assert.equal(whenWords('2025-03-04T05:06:07Z', NOW), 'Mar 4, 2025');
  assert.equal(whenWords('not a time', NOW), null);
});

test('a title imitating the App\'s state words, a control or an App sentence is drawn as a title, never in the App\'s mark, and is read after "Title:"', async () => {
  const imitations = {N:'Needs answer', P:'Approval needed', Y:'Your move', F:'Agent says finished', C:'Allow once', B:`${ROOT_BUSY}\nAllow once`, D:'Run‮evil\u0007\tdone', R:'Needs answer'};
  const entries = Object.entries(imitations).map(([id, title]) => entry(id, {title, live:'idle'}));
  await draw(held(answer([open(entries)])), async ({c}) => {
    for (const [id, title] of Object.entries(imitations)) {
      const b = row(c, id);
      const shown = all(b, cls('v4-nav-title'))[0];
      assert.ok(shown, id);
      assert.equal(all(b, cls('v4-nav-mark')).length, id === 'R' ? 0 : 0, `${id}: no App mark inside the entry`);
      assert.equal(id === 'R' ? 1 : marks(c, id, 'Needs answer').length, id === 'R' ? 1 : 0, `${id}: no Needs answer control`);
      assert.doesNotMatch(shown.textContent, /[\n\u0007‮\t]/, `${id}: nothing in it acted on`);
      if (id !== 'R') assert.ok(accessibleName(b).startsWith('Title: '), `${id}: read as a title`);
      assert.ok(!notes(c).some(n => n === ROOT_BUSY), 'the imitated sentence is not the App\'s');
      void title;
    }
    assert.equal(all(row(c, 'D'), cls('v4-nav-title-mark')).map(n => n.textContent).join(' '), '‹U+202E› ‹U+0007› →');
    assert.equal(all(row(c, 'B'), cls('v4-nav-title-mark')).map(n => n.textContent).join(' '), '⏎');
    // Beside it, a real request: the App's own words come first, in its mark and its name.
    assert.ok(accessibleName(row(c, 'R')).startsWith('Needs answer. Title: Needs answer'));
    assert.ok(accessibleName(row(c, 'N')).startsWith('Title: Needs answer'));
  }, {waiting:[waiting('question', 'R')]});
});

test('"Needs answer" for an agent\'s question, "Approval needed" for a permission, a delegated agent\'s request on its root, another home\'s count, and requests on no entry; pressing goes to the request', async () => {
  const entries = [entry('Q'), entry('P'), entry('ROOT'), entry('BOTH')];
  const reqs = [waiting('question', 'Q'), waiting('tool-permission', 'P'), waiting('tool-permission', 'CHILD', 'ROOT'), waiting('question', 'BOTH'), waiting('tool-permission', 'BOTH'),
    waiting('question', 'GONE'), waiting('requests-in-another-home', 'K1', 'K1', 'api-key', 3)];
  await draw(held(answer([open(entries)], {unassigned:[entry('K1', {home:'api-key', projectRoot:null, open:history('K1')})]})), async ({c, did}) => {
    assert.equal(marks(c, 'Q', 'Needs answer').length, 1); assert.equal(marks(c, 'Q', 'Approval needed').length, 0);
    assert.equal(marks(c, 'P', 'Approval needed').length, 1); assert.equal(marks(c, 'P', 'Needs answer').length, 0);
    assert.equal(marks(c, 'ROOT', 'Approval needed').length, 1, 'a delegated agent\'s request on the conversation it descends from');
    assert.equal(marks(c, 'BOTH', 'Needs answer').length + marks(c, 'BOTH', 'Approval needed').length, 2);
    assert.equal(marks(c, 'K1', 'Needs answer').length, 1, 'another home\'s requests, counted there, need an answer');
    assert.ok(accessibleName(row(c, 'BOTH')).startsWith('Needs answer. Approval needed. Title: '));
    assert.equal(row(c, 'K1').getAttribute('disabled') !== null || props(row(c, 'K1')).disabled, true, 'another home\'s conversation is not chosen from here');
    assert.ok(notes(c).includes(OTHER_HOME));
    assert.ok(notes(c).some(n => n.startsWith('1 request waits on a conversation not listed here.')), `a request on no entry is said, so none the top line counts is missed: ${JSON.stringify(notes(c))}`);
    await React.act(async () => props(marks(c, 'ROOT', 'Approval needed')[0]).onClick());
    assert.equal(did.answer.at(-1).concerns.threadId, 'CHILD', 'the request\'s own conversation is the one opened');
    await React.act(async () => props(all(c, n => n.localName === 'button' && n.textContent === 'Go to it')[0]).onClick());
    assert.equal(did.answer.at(-1).concerns.threadId, 'GONE');
  }, {waiting:reqs});
  const placed = placeRequests(reqs, new Set(['Q', 'P', 'ROOT', 'BOTH'].map(id => JSON.stringify(['account', id]))));
  assert.deepEqual(placed.unplaced.map(e => e.concerns.threadId), ['GONE', 'K1']);
  assert.equal([...placed.on.values()].reduce((n, r) => n + r.questions + r.approvals, 0), 5);
});

test('choosing: a loaded conversation of the active home is chosen; a stored one of the open project opens in History; another home, another generation and a record-only one are not offered', () => {
  assert.deepEqual(entryOpen(entry('A'), 'account', g, true), {kind:'choose', key:JSON.stringify([g, 'A'])});
  assert.deepEqual(entryOpen(entry('A', {open:history('A')}), 'account', g, true), {kind:'history', generation:g, selectionEpoch:3, threadId:'A'});
  assert.deepEqual(entryOpen(entry('A', {open:history('A')}), 'account', g, false), {kind:'none', why:NOT_OPEN_PROJECT});
  assert.deepEqual(entryOpen(entry('A', {open:loaded('A')}), 'account', g, false), {kind:'choose', key:JSON.stringify([g, 'A'])}, 'loaded in this running App, whatever its project');
  assert.deepEqual(entryOpen(entry('A', {home:'api-key'}), 'account', g, true), {kind:'none', why:OTHER_HOME});
  assert.deepEqual(entryOpen(entry('A', {open:loaded('A', earlier)}), 'account', g, true), {kind:'none', why:NOT_CURRENT});
  const why = 'This conversation is known from a run record only, and the App does not know which Codex home holds it, so it cannot be opened from here.';
  assert.deepEqual(entryOpen(entry('A', {home:null, open:{kind:'not-openable', reason:why}}), 'account', g, true), {kind:'none', why});
  assert.equal(runWord(null, 'idle', false), null);
  assert.equal(runWord(run('open'), 'idle', true), null, 'a request is said by its own mark');
});

test('a record-only entry says the host\'s reason under it and cannot be pressed; nothing is chosen while the conversation view takes no choice', async () => {
  const why = 'This conversation is known from the App\'s own record, but it is not in the list Codex gave for its home (it may have been archived or removed), so it cannot be opened from here.';
  await draw(held(answer([open([entry('R', {title:null, updatedAt:null, open:{kind:'not-openable', reason:why}, run:run('ended'), runCount:1}), entry('A')])])), async ({c, did}) => {
    assert.ok(notes(c).includes(why));
    assert.ok(props(row(c, 'R')).disabled);
    assert.equal(all(row(c, 'R'), cls('woven-navigator-session-when'))[0].textContent, 'time not known');
    await React.act(async () => props(row(c, 'R')).onClick());
    assert.deepEqual(did.choose, []);
  });
  await draw(held(answer([open([entry('A')])])), async ({c}) => assert.ok(props(row(c, 'A')).disabled), {choose:null});
});

// ---- Mounted: the read on its timer, and agreement with "Waiting on you" ----

const thread = (id, type = 'idle') => ({generation:g, threadId:id, model:'invented-model', status:{type}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const request = (id, method, threadId) => ({recordKind:'server-request-entry', generation:g, requestIdentity:id, method, classification:'known-answerable',
  originClass:method === 'item/tool/requestUserInput' ? 'person-input' : 'a14', state:'outstanding', replyWriteResult:'not-attempted', acknowledgmentObservation:{status:'not-observed'},
  nativeParameters:method === 'item/tool/requestUserInput'
    ? {threadId, turnId:'u1', itemId:'i1', isBlocking:false, questions:[{id:'q', header:'Scope', question:'Which folder?', isOther:false, isSecret:false, options:[{label:'reports/', description:'Reports'}]}]}
    : {threadId, turnId:'u1', itemId:'i2', command:'ls', cwd:'/invented'}});
const descendants = [{threadId:'C1', parentThreadId:'T1', parentSource:'collabAgentToolCall.senderThreadId', guidance:'not-known', nativeThread:{id:'C1'}}];
const hostView = (over = {}) => ({state:'ready', generation:g, threads:[thread('T1'), thread('T2'), thread('T3'), thread('C1')], roleLimits:{account:{roles:[]}}, homeRouting:{activeModeHomeClass:'account'},
  nativeView:{home:'account', generation:g, items:[], turns:[], turnRecords:[], revisions:[], descendants}, serverRequests:[], nativeHistory:{home:'account', generation:g, selectionEpoch:7},
  workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[], drafts:{drafts:[]}}, ...over});

async function mountApp(host, navigatorRead, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [], revealed = [];
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  const timers = [];
  document.getElementById = id => { revealed.push(id); return c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null; };
  globalThis.setInterval = (fn, ms) => { timers.push({fn, ms}); return timers.length; }; globalThis.clearInterval = () => {};
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return structuredClone(host);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content' || command === 'request_answer_companions') return [];
    if (command === 'open_waiting_requests') return {modeHomeClass:args.modeHomeClass, generation:args.generation, threadId:args.threadId, threadLoaded:true, standing:'invented'};
    if (command === 'history_select') return {state:'selected'};
    assert.fail(`Unexpected IPC: ${command}`);
  }, {navigatorRead:n => { calls.push({command:'navigator_read', args:n}); return navigatorRead(n); }});
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await check({c, calls, revealed, timers});
  } finally {
    const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById;
  }
}
const mountedNav = c => all(c, n => n.getAttribute('aria-label') === 'Workspace Navigator')[0];

test('mounted: the navigator marks exactly the requests "Waiting on you" counts as the person\'s, on the entry they belong to; pressing a mark opens that request', async () => {
  const host = hostView({serverRequests:[request('q1', 'item/tool/requestUserInput', 'T3'), request('a1', 'item/commandExecution/requestApproval', 'T2'), request('c1', 'item/tool/requestUserInput', 'C1'),
    {...request('done', 'item/tool/requestUserInput', 'T1'), state:'answered', replyWriteResult:'written'}]});
  const entries = ['T1', 'T2', 'T3'].map(id => entry(id));
  await mountApp(host, () => answer([open(entries)]), async ({c, calls}) => {
    const navigator = mountedNav(c);
    const shown = id => marks(navigator, id, 'Needs answer').length + marks(navigator, id, 'Approval needed').length;
    assert.deepEqual(['T1', 'T2', 'T3'].map(shown), [1, 1, 1], 'T1 by its delegated agent\'s question, T2 by an approval, T3 by a question; the answered one marks nothing');
    const counted = waitingEntries({host, decisions:{rows:[]}}).filter(nav.isPersonRequest);
    assert.equal(counted.length, 3, 'the same three that "Waiting on you" lists');
    assert.equal(marks(navigator, 'T2', 'Approval needed').length, 1);
    const before = calls.length;
    await React.act(async () => { await props(marks(navigator, 'T1', 'Needs answer')[0]).onClick(); });
    assert.deepEqual(calls.slice(before).find(x => x.command === 'open_waiting_requests')?.args, {modeHomeClass:'account', generation:g, threadId:'C1'}, 'the delegated agent\'s own conversation is opened');
  });
});

test('mounted: the read is made at mount and on its own timer; choosing a stored conversation selects it in History with the epoch its view holds', async () => {
  const entries = [entry('T1'), entry('OLD', {open:history('OLD'), live:'not-loaded'})];
  await mountApp(hostView(), () => answer([open(entries)]), async ({c, calls, timers}) => {
    assert.ok(calls.some(x => x.command === 'navigator_read'), 'read at mount');
    const timer = timers.find(t => t.ms === NAVIGATOR_READ_MS);
    assert.ok(timer, 'its own timer');
    const n = calls.filter(x => x.command === 'navigator_read').length;
    await React.act(async () => { timer.fn(); await new Promise(r => setTimeout(r, 0)); });
    assert.equal(calls.filter(x => x.command === 'navigator_read').length, n + 1);
    const before = calls.length;
    await React.act(async () => { props(row(mountedNav(c), 'OLD')).onClick(); await new Promise(r => setTimeout(r, 0)); });
    assert.deepEqual(calls.slice(before).find(x => x.command === 'history_select')?.args, {generation:g, selectionEpoch:7, threadId:'OLD'});
    const selected = all(c, n => n.getAttribute('role') === 'tab' && n.getAttribute('aria-selected') === 'true')[0];
    assert.equal(selected.textContent, 'More', 'History stands under More');
    const back = all(c, n => n.getAttribute('class') === 'v4-more-back')[0];
    assert.ok(!!back && back.textContent.endsWith('History'), 'and it is History that More shows, where the conversation can be continued');
  });
});
