import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The right panel's Run tab and the status strip's run: one shorter reading (runWord) over exactly runReading's
// conditions, the tab's acts (the guide's workflow_end_run under the guide's conditions), the present detail kept
// under Details, and the empty states. Controlled host views only: no native App, supplier, model or person act.
installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {runReading, runWord, delegatedReading, conversationRun, stripRun, ORDER_UNKNOWN_WORD, VIEW_NOT_REFRESHED} = loadSrc('RunJourney');
const {RunTab, NO_CONVERSATION, NO_RUN, reportedFiles} = loadSrc('RunTab');
const {ActivityStrip} = loadSrc('WorkspaceShell');

// The fixtures of the present runReading tests (tests/run-journey.test.mjs).
const UNKNOWN = {state:'native workflow-text send outcome unknown; original source retained', limit:'reply lost'};
const REFUSED = {state:'native workflow-text turn/start refused by Codex; original source retained', limit:'invented refusal'};
const NOT_CONFIRMED = 'start not confirmed (turn refused or outcome unknown); not opened, not live';
const OPEN = "open (live); only the person's explicit end ends it";
const PREPARED = 'prepared; not a run until its start turn is observed';
const g = {home:'account', appSession:'s1', spawnCounter:1};
const g2 = {...g, spawnCounter:2};
const view = (descendants = [], over = {}) => ({generation:g, descendants, items:[], turns:[], turnRecords:[], turnErrors:[], ...over});
function host(over = {}) {
  return {state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}},
    threads:[{threadId:'T1', generation:g, model:'invented-model', status:{type:'idle'}}, {threadId:'T2', generation:g, model:'invented-model', status:{type:'idle'}}],
    serverRequests:[], nativeView:view(), ...over};
}
const open = (over = {}) => ({reference:'run-1', conversation:'T1', home:'account', generation:g, source:'s', lifecycle:{state:OPEN}, workflow:{name:'resolve-spacing', origin:'project', revision:'rev-2-abcdef0123456789'}, status:{}, ...over});
const withThread = (status, extra = {}) => host({threads:[{threadId:'T1', generation:g, status, ...extra}]});
const outstanding = (threadId = 'T1') => ({state:'outstanding', nativeParameters:{threadId}});
const offer = {message:'agent-message-ref', finished:{run:'run-1', statement:'Workflow finished: project:resolve-spacing'}};
const child = (threadId, lastObservedStatus, over = {}) => ({threadId, parentThreadId:'T1', parentSource:'collabAgentToolCall.senderThreadId', lastObservedStatus, ...over});

// Every branch of runReading, with its present title, and the word, sentence and actions the Run tab gives it.
const BRANCHES = [
  ['ended as completed', open({lifecycle:{state:'ended by the person', end:{cause:'completed'}}}), host(), undefined,
    'Ended as completed', 'Ended', "You ended it as completed, on the agent's report.", []],
  ['ended by the person', open({lifecycle:{state:'ended by the person', end:{cause:'ended by the person'}}}), host(), undefined,
    'Ended by you', 'Ended', 'You ended it.', []],
  ['ended to start another', open({lifecycle:{state:'ended by the person', end:{cause:'ended to start other-flow'}}}), host(), undefined,
    'Ended to start another workflow', 'Ended', 'It ended so that another workflow could start.', []],
  ['ended, other cause', open({lifecycle:{state:'ended', end:{cause:'invalid'}}}), host(), undefined,
    'Ended', 'Ended', 'The run ended. Its recorded cause is under Details.', []],
  ['ended, no cause', open({lifecycle:{state:'ended', end:null}}), host(), undefined,
    'Ended', 'Ended', 'The run ended. Its recorded cause is under Details.', []],
  ['start refused', open({source:null, lifecycle:{state:NOT_CONFIRMED}, status:REFUSED}), host(), undefined,
    'Codex refused to start the run', 'Start refused', 'Codex refused the starting message, so this workflow did not run.', []],
  ['start unknown', open({source:null, lifecycle:{state:NOT_CONFIRMED}, status:UNKNOWN}), host(), undefined,
    'Start not confirmed — outcome unknown', 'Start unknown', "The App can't tell whether Codex received the starting message. It may have run, and the App will not resend it. Read the conversation first.", ['show']],
  ['earlier Codex session', open({generation:g}), host({generation:g2, threads:[{threadId:'T1', generation:g2, status:{type:'idle'}}]}), undefined,
    'Open in an earlier Codex session', 'Earlier session', "Open in a Codex session that isn't the current one, so the App can't see what it is doing. Find its conversation in History.", []],
  ['outstanding request', open(), host({serverRequests:[outstanding()]}), undefined,
    'Waiting for your answer', 'Needs answer', 'Codex is asking a question or approval in the conversation.', ['answer', 'end']],
  ['two outstanding requests', open(), host({serverRequests:[outstanding(), outstanding()]}), undefined,
    'Waiting for your answer', 'Needs answer', 'Codex is asking 2 questions or approvals in the conversation.', ['answer', 'end']],
  ['generation closed', open(), host({generationClosed:true}), undefined,
    'Open — the App is no longer receiving from Codex', 'Not receiving', 'The App is no longer receiving from Codex for this run, so what it was doing is not known.', ['show', 'end']],
  ['status observation ended', open(), withThread(null, {statusObservationEnded:true, lastObservedStatus:{type:'active', activeFlags:[]}}), undefined,
    'Open — the App is no longer receiving from Codex', 'Not receiving', 'The App is no longer receiving from Codex for this run, so what it was doing is not known.', ['show', 'end']],
  ['active, waiting on approval', open(), withThread({type:'active', activeFlags:['waitingOnApproval']}), undefined,
    'Codex reports it is waiting for an approval or an answer', 'Waiting', 'Codex reports it is waiting for an approval or your answer. The request shows in the conversation once the App receives it.', ['show', 'end']],
  ['active, waiting on input', open(), withThread({type:'active', activeFlags:['waitingOnUserInput']}), undefined,
    'Codex reports it is waiting for an approval or an answer', 'Waiting', 'Codex reports it is waiting for an approval or your answer. The request shows in the conversation once the App receives it.', ['show', 'end']],
  ['active', open(), withThread({type:'active', activeFlags:[]}), undefined,
    'Open — Codex reports this conversation active', 'Working', 'Codex reports this conversation active.', ['show', 'end']],
  ['system error', open(), withThread({type:'systemError'}), undefined,
    'Codex reported an error', 'Error', 'Codex reported a system error. The run is still open; read the conversation first.', ['show', 'end']],
  ['idle, no delegated agent', open(), host(), undefined,
    'Open — Codex reports this conversation idle', 'Your move', "The agent's turn has ended. The run is open.", ['reply', 'end']],
  ['idle, delegated agent idle', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g, status:{type:'idle'}}], nativeView:view([child('C1', {status:'completed'})])}), undefined,
    'Open — Codex reports this conversation idle', 'Your move', "The agent's turn has ended. The run is open.", ['reply', 'end']],
  ['idle, delegated agent reported active', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g, status:{type:'active', activeFlags:[]}}], nativeView:view([child('C1', null)])}), undefined,
    'Open — Codex reports this conversation idle', 'Working', "The agent's turn has ended, and an agent it delegated work to is reported active.", ['show', 'end']],
  ['idle, delegated agent reported running by its delegating item', open(), host({nativeView:view([child('C1', {status:'running'})])}), undefined,
    'Open — Codex reports this conversation idle', 'Working', "The agent's turn has ended, and an agent it delegated work to is reported active.", ['show', 'end']],
  ['idle, delegated agent unreadable', open(), host({nativeView:view([child('C1', {status:'completed'})])}), undefined,
    'Open — Codex reports this conversation idle', 'Turn ended', "The agent's turn has ended. The App can't see whether the agents it delegated to are still working.", ['reply', 'end']],
  ['idle, no native view to read', open(), host({nativeView:null}), undefined,
    'Open — Codex reports this conversation idle', 'Turn ended', "The agent's turn has ended. The App can't see whether it delegated work to other agents.", ['reply', 'end']],
  ['idle, finished offer', open(), host(), offer,
    'Open — Codex reports this conversation idle', 'Agent says finished', "That is the agent's word. Ending the run is yours.", ['end-completed', 'end']],
  ['idle, finished offer, delegated agent unreadable', open(), host({nativeView:view([child('C1', null)])}), offer,
    'Open — Codex reports this conversation idle', 'Agent says finished', "That is the agent's word. Ending the run is yours. The App can't see whether agents it delegated to are still working.", ['end-completed', 'end']],
  ['active, finished offer', open(), withThread({type:'active', activeFlags:[]}), offer,
    'Open — Codex reports this conversation active', 'Working', 'Codex reports this conversation active.', ['show', 'end-completed', 'end']],
  ['status not readable', open(), withThread({type:'notLoaded'}), undefined,
    'Open — what Codex is doing is not known', 'State unknown', "The App can't tell what Codex is doing in this conversation. Read it before deciding what to do.", ['show', 'end']],
  ['no status row', open(), host({threads:[]}), undefined,
    'Open — what Codex is doing is not known', 'State unknown', "The App can't tell what Codex is doing in this conversation. Read it before deciding what to do.", ['show', 'end']],
  ['starting', open({source:'sent', lifecycle:{state:PREPARED}}), host(), undefined,
    'Starting', 'Starting', "The App has issued the starting message and is waiting for Codex's reply.", []],
  ['not sent, known state', open({source:null, lifecycle:{state:PREPARED}, status:{sent:false, state:'WR pre-send publication failed; nothing sent', limit:'disk full'}}), host(), undefined,
    'Not started', 'Not started', 'Nothing was sent. Details say why.', []],
  ['not sent, other state', open({source:null, lifecycle:{state:PREPARED}, status:{sent:false, state:'invented', limit:'x'}}), host(), undefined,
    'Not started', 'Not started', 'The App reports this run was not sent. Details say why.', []],
  ['prepared', open({source:null, lifecycle:{state:PREPARED}, status:{sent:false}}), host(), undefined,
    'Ready to start', 'Not started', 'The run is prepared. Nothing has been sent.', []],
];
const SEVEN = ['Not started', 'Starting', 'Working', 'Needs answer', 'Your move', 'Agent says finished', 'Ended'];

test('the Run tab\'s word covers every branch of runReading and says no more than the branch', () => {
  const titles = new Set();
  for (const [name, run, h, finished, title, word, sentence, actions] of BRANCHES) {
    assert.equal(runReading(run, h).title, title, `${name}: the present reading`);
    titles.add(title);
    const shorter = runWord(run, h, finished);
    assert.deepEqual([shorter.word, shorter.sentence, shorter.actions], [word, sentence, actions], name);
  }
  // Every title runReading can give is reached by the table.
  for (const title of ['Ended as completed', 'Ended by you', 'Ended to start another workflow', 'Ended', 'Codex refused to start the run', 'Start not confirmed — outcome unknown',
    'Open in an earlier Codex session', 'Waiting for your answer', 'Open — the App is no longer receiving from Codex', 'Codex reports it is waiting for an approval or an answer',
    'Open — Codex reports this conversation active', 'Codex reported an error', 'Open — Codex reports this conversation idle', 'Open — what Codex is doing is not known',
    'Starting', 'Not started', 'Ready to start']) assert.ok(titles.has(title), title);
  // The cases the App cannot establish each have a word of their own, never one of the seven.
  for (const [name, run, h, finished] of BRANCHES) {
    const reading = runReading(run, h);
    if (reading.tone === 'uncertain' || reading.tone === 'failed' && !/Not started/.test(reading.title)) assert.ok(!SEVEN.includes(runWord(run, h, finished).word), name);
  }
  assert.ok(!SEVEN.includes(ORDER_UNKNOWN_WORD.word));
  // Ended is never complete or checked, and an unknown start keeps the caution a person needs before acting.
  for (const [name, run, h, f] of BRANCHES) { const w = runWord(run, h, f); if (w.word === 'Ended') assert.doesNotMatch(w.sentence, /complete\b|completed\.|checked/, name); }
  assert.match(runWord(BRANCHES[6][1], BRANCHES[6][2]).sentence, /will not resend it\. Read the conversation first\./);
});

test('"Your move" is never said with a request, a finished offer, an unreadable or active delegated agent, a closed session or an earlier one', () => {
  const idle = host();
  assert.equal(runWord(open(), idle).word, 'Your move', 'the control case');
  const never = [
    ['outstanding request', open(), host({serverRequests:[outstanding()]})],
    ['finished offer', open(), idle, offer],
    ['delegated agent unreadable', open(), host({nativeView:view([child('C1', null)])})],
    ['delegated agent with no status row and a completed report', open(), host({nativeView:view([child('C1', {status:'completed'})])})],
    ['delegated agent whose row and report disagree', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g, status:{type:'idle'}}], nativeView:view([child('C1', {status:'running'})])})],
    ['delegated agent active', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g, status:{type:'active', activeFlags:[]}}], nativeView:view([child('C1', null)])})],
    ['grandchild active', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g, status:{type:'idle'}}, {threadId:'C2', generation:g, status:{type:'active'}}],
      nativeView:view([child('C1', null), child('C2', null, {parentThreadId:'C1'})])})],
    ['delegated agent in another session only', open(), host({threads:[{threadId:'T1', generation:g, status:{type:'idle'}}, {threadId:'C1', generation:g2, status:{type:'idle'}}], nativeView:view([child('C1', null)])})],
    ['native view of another session', open(), host({nativeView:{...view(), generation:g2}})],
    ['native view observation ended', open(), host({nativeViewObservationEnded:true})],
    ['closed generation', open(), host({generationClosed:true})],
    ['status observation ended', open(), withThread({type:'idle'}, {statusObservationEnded:true})],
    ['earlier session, same-numbered idle conversation now', open(), host({generation:g2, threads:[{threadId:'T1', generation:g2, status:{type:'idle'}}], nativeView:{...view(), generation:g2}})],
  ];
  for (const [name, run, h, f] of never) assert.notEqual(runWord(run, h, f).word, 'Your move', name);
  // What the delegated reading rests on, for each agent.
  assert.deepEqual(delegatedReading('T1', host({threads:[{threadId:'C1', generation:g, status:{type:'idle'}}, {threadId:'C2', generation:g, status:{type:'active'}}],
    nativeView:view([child('C1', null), child('C2', null), child('C3', {status:'pendingInit'}), child('C4', {status:'running'}, {observationEnded:true})])})),
    {viewReadable:true, active:2, idle:1, unreadable:1});
});

test('"Needs answer" is said only for a request the App holds outstanding for this conversation', () => {
  const words = [];
  for (const [, run, h, f] of BRANCHES) { const w = runWord(run, h, f); words.push(w.word); if (w.word === 'Needs answer') assert.ok(h.serverRequests.some(r => r.state === 'outstanding' && r.nativeParameters.threadId === run.conversation)); }
  for (const h of [host({serverRequests:[outstanding('T2')]}), host({serverRequests:[{state:'answered', nativeParameters:{threadId:'T1'}}]}), withThread({type:'active', activeFlags:['waitingOnUserInput']}),
    host({serverRequests:[{...outstanding(), generation:g2}]})]) {
    const w = runWord(open(), h); assert.notEqual(w.word, 'Needs answer'); assert.ok(!w.actions.includes('answer'), 'no answer offered without a request the App holds');
  }
});

// ---- The tab, mounted ----
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => all(c, 'button').find(node => node.textContent === label);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const data = (over = {}) => ({context:{sourceRef:'src', generation:g}, runs:[], offers:[], selections:[], ...over});
async function mount({data: d, host: h, thread = 'T1', busy = false, viewStale = false, readFailure = null, navigate = true}) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = [], shown = [];
  await React.act(async () => root.render(React.createElement(RunTab, {data:d, host:h, thread, busy, viewStale, readFailure, outcome:null,
    showConversation:navigate ? (id, target) => shown.push([id, target]) : undefined, act:async (command, args) => { calls.push({command, args}); }})));
  return {c, calls, shown, close:() => React.act(async () => root.unmount())};
}

test('the tab\'s acts are the guide\'s workflow_end_run, with its arguments and its conditions', async () => {
  const ui = await mount({data:data({runs:[open()], offers:[offer]}), host:host()});
  try {
    assert.equal(region(ui.c, 'Run state').textContent.includes('Agent says finished'), true);
    assert.match(region(ui.c, 'Agent finished report').textContent, /The agent wrote Workflow finished: project:resolve-spacing/);
    await React.act(async () => props(button(ui.c, 'End run as completed')).onClick());
    await React.act(async () => props(button(ui.c, 'End run')).onClick());
    assert.deepEqual(ui.calls, [{command:'workflow_end_run', args:{runRef:'run-1', finishedReport:'agent-message-ref'}}, {command:'workflow_end_run', args:{runRef:'run-1', finishedReport:null}}]);
  } finally { await ui.close(); }
  // Never while busy, never while the shown workflow source or Codex session differs from the host's.
  for (const [name, d, h, busy] of [['busy', data({runs:[open()], offers:[offer]}), host(), true],
    ['source changed', data({runs:[open()], offers:[offer]}), host({workflowRoot:{context:{sourceRef:'other', generation:g}}}), false],
    ['session of the shown source differs', data({context:{sourceRef:'src', generation:g2}, runs:[open()], offers:[offer]}), host(), false]]) {
    const view = await mount({data:d, host:h, busy});
    try {
      for (const label of ['End run as completed', 'End run']) assert.equal(props(button(view.c, label)).disabled, true, `${name}: ${label}`);
      await React.act(async () => { props(button(view.c, 'End run')).onClick(); });
      assert.deepEqual(view.calls, [], `${name}: nothing is sent`);
    } finally { await view.close(); }
  }
  // Needs answer goes to the requests; Your move's Reply and the other states' Show go to the conversation. None sends anything.
  const asking = await mount({data:data({runs:[open()]}), host:host({serverRequests:[outstanding()]})});
  try { await React.act(async () => props(button(asking.c, 'Answer in the conversation')).onClick()); assert.deepEqual(asking.shown, [['T1', 'conversation-requests']]); assert.deepEqual(asking.calls, []); }
  finally { await asking.close(); }
  const move = await mount({data:data({runs:[open()]}), host:host()});
  try { await React.act(async () => props(button(move.c, 'Reply')).onClick()); assert.deepEqual(move.shown, [['T1', 'conversation']]); assert.equal(button(move.c, 'End run as completed'), undefined); }
  finally { await move.close(); }
});

test('the present detail stays reachable under Details, word for word; error notices stay in view', async () => {
  const notice = {threadId:'T1', turnId:'turn-9', generation:g, error:{message:'Reconnecting... 2', additionalDetails:'Connection failed'}, willRetry:true, ordinalInTurn:1, observedOrder:4, laterFrameForTurn:false};
  const d = data({runs:[open(), open({reference:'run-0', preparationOrder:0, lifecycle:{state:'ended', end:{cause:'completed'}}})].map((r, i) => i === 0 ? {...r, preparationOrder:1} : r)});
  const h = withThread({type:'active', activeFlags:[]});
  h.nativeView = view([], {turnErrors:[notice]});
  const ui = await mount({data:d, host:h});
  try {
    const details = all(ui.c, 'details').find(n => n.getAttribute('class') === 'run-tab-details');
    assert.ok(details, 'one Details disclosure'); assert.equal(props(details).open, undefined, 'closed');
    const reading = runReading(d.runs[0], h);
    assert.ok(details.textContent.includes(`${reading.title}. ${reading.detail}`), 'the present reading, word for word');
    assert.ok(details.textContent.includes("Ending here records that you ended it — not that it completed. To stop only Codex's current step, use Stop in the conversation; the run stays open."));
    assert.ok(details.textContent.includes("These are what the workflow declares it produces; the App hasn't checked that any of them exist."));
    assert.ok(details.textContent.includes('The conversation\'s activity shows file changes reported by Codex; it does not establish every file changed by commands or tools.'));
    assert.match(region(details, 'Run run-0').textContent, /Ended as completed\./, 'the earlier run, in the Results wording');
    assert.ok(all(details, 'a').some(a => a.getAttribute('href') === '#run-evidence-' + [...'run-1'].map(ch => ch.charCodeAt(0).toString(16).padStart(4, '0')).join('')), 'the run\'s recorded evidence');
    const notes = region(ui.c, 'Error notices the App holds for this conversation');
    assert.ok(notes, 'notices in view'); let inside = false; for (let n = notes; n; n = n.parentNode) if (n === details) inside = true;
    assert.equal(inside, false, 'outside the disclosure');
    assert.match(notes.textContent, /The App holds an error notice from Codex for turn turn-9 of this conversation: Reconnecting\.\.\. 2 — Connection failed Codex said it will retry\./);
  } finally { await ui.close(); }
});

test('Results: what the workflow declares, and the files Codex reported changing in this conversation', async () => {
  const declaration = {elements:{returned_outputs:[{value:{name:'report-file', path:'reports/spacing.md'}}]}};
  const fileChange = (id, order, changes, state = 'completed', threadId = 'T1') => ({threadId, turnId:'u', native:{id, type:'fileChange', changes}, displayState:state, observedOrder:order});
  const items = [fileChange('a', 1, [{path:'/invented/work/notes/a.md', kind:{type:'add'}}]), fileChange('b', 2, [{path:'/invented/work/notes/a.md', kind:{type:'update'}}, {path:'/invented/work/b.md', kind:{type:'update', move_path:'/invented/work/c.md'}}]),
    fileChange('c', 3, [{path:'/invented/work/declined.md', kind:{type:'add'}}], 'declined'), fileChange('d', 4, [{path:'/invented/work/other.md', kind:{type:'add'}}], 'completed', 'T2')];
  const h = host({nativeView:view([], {items})});
  assert.deepEqual(reportedFiles(h, 'T1'), [{path:'/invented/work/notes/a.md', kind:'new file'}, {path:'/invented/work/c.md', kind:'moved'}], 'added, then changed, is still a new file');
  assert.deepEqual(reportedFiles({...h, nativeView:{...h.nativeView, generation:g2}}, 'T1'), [], 'another session\'s view says nothing');
  const ui = await mount({data:data({runs:[open({compatibility:[{preparation:{declaration}}]})]}), host:h});
  try {
    assert.match(ui.c.textContent, /report-file reports\/spacing\.md/);
    assert.match(ui.c.textContent, /Declared by the workflow; the App hasn't checked that any exist\. The agent reports its results in the conversation\./);
    const files = region(ui.c, 'Files the agent reported changing');
    assert.match(files.textContent, /^2 files changed in this conversation/); assert.match(files.textContent, /Reported by the agent\. The App hasn't checked it\.$/);
    assert.equal(all(files, 'button').length, 0, 'no Open or Reveal: the host has no command for it');
  } finally { await ui.close(); }
});

test('the strip and the tab say the same word for the open conversation\'s run', async () => {
  for (const [name, run, h, finished] of BRANCHES) {
    const d = data({runs:[{...run, preparationOrder:0}], offers:finished ? [finished] : []});
    const strip = stripRun(d, h, 'T1');
    const expected = conversationRun(d, h, 'T1').word;
    if (!expected) { assert.equal(strip, null, name); continue; }
    assert.equal(strip.word, expected.word, name); assert.equal(strip.name, 'resolve-spacing', name);
    const c = document.createElement('div'); const root = createRoot(c);
    await React.act(async () => root.render(React.createElement(React.Fragment, null, React.createElement(ActivityStrip, {phase:null, run:strip}),
      React.createElement(RunTab, {data:d, host:h, thread:'T1', busy:false, act:async () => {}, outcome:null}))));
    const status = c.querySelectorAll(n => n.getAttribute('role') === 'status')[0];
    assert.equal(status.textContent, `resolve-spacing · ${strip.word}`, name);
    assert.ok(region(c, 'Run state')?.textContent.startsWith(strip.word), `${name}: the tab's word`);
    await React.act(async () => root.unmount());
  }
  // Several runs whose order is unknown: one word for both, and no latest run chosen.
  const two = data({runs:[open({reference:'a'}), open({reference:'b'})]});
  assert.deepEqual(stripRun(two, host(), 'T1'), {name:'Workflow runs', word:'Order unknown', mark:'unknown'});
  // Only this conversation's runs of this Codex session.
  assert.equal(stripRun(data({runs:[open({conversation:'T2'})]}), host(), 'T1'), null);
  assert.equal(stripRun(data({runs:[open({generation:g2})]}), host(), 'T1'), null);
  // Without a run the strip says the turn phase, with the owner's word for an outstanding request.
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(ActivityStrip, {phase:'waiting'})));
  assert.equal(c.textContent, 'Needs answer');
  await React.act(async () => root.unmount());
});

test('the empty states, and a view that may be from before the last operation', async () => {
  const none = await mount({data:data(), host:host(), thread:''});
  try { assert.equal(none.c.textContent, NO_CONVERSATION); assert.equal(all(none.c, 'button').length, 0); } finally { await none.close(); }
  const previous = document.getElementById; const revealed = [];
  document.getElementById = id => { revealed.push(id); return null; };
  const empty = await mount({data:data({runs:[open({conversation:'T2'})]}), host:host()});
  try {
    assert.match(empty.c.textContent, new RegExp(`^${NO_RUN}`));
    await React.act(async () => props(button(empty.c, 'Choose a workflow')).onClick());
    assert.deepEqual(revealed, ['view-library'], 'selects the Workflows tab');
    assert.deepEqual(empty.calls, []);
  } finally { await empty.close(); document.getElementById = previous; }
  const stale = await mount({data:data({runs:[open()]}), host:host(), viewStale:true, readFailure:'invented failure'});
  try {
    assert.match(stale.c.textContent, new RegExp(VIEW_NOT_REFRESHED.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.match(stale.c.textContent, /The last read failed: invented failure/);
    assert.equal(all(stale.c, 'button').length, 0, 'no act');
  } finally { await stale.close(); }
  const failed = await mount({data:data({runs:[open()]}), host:host(), readFailure:'invented failure'});
  try { assert.match(region(failed.c, 'Last status read failed').textContent, /The App's last read of its state failed \(invented failure\)\. What is shown here was read before that\./); } finally { await failed.close(); }
});
