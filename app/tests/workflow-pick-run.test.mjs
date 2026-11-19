import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting, navigatorReadOf} from './support/idle-native-waiting.mjs';
import {chatInput, newChatButton, sendButton} from './support/conversation-view.mjs';

// The composer's Start run with a workflow picked in the Workflows tab (WorkflowPick.tsx), through the mounted App's
// native invoke boundary. A stand-in host keeps invented state in the shapes the host gives (lib.rs thread_start,
// workflow_select_production_bundle, workflow_select_listed, workflow_prepare_run, workflow_send_run; runtime_session.rs
// selection_view and the run rows) and records every command issued. No supplier, model, sign-in or person act.
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');

const g = {appSession: 's', home: 'h', spawnCounter: 1};
const key = id => JSON.stringify([g, id]);
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(n => n.localName === tag);
const labelled = (c, label) => c.querySelectorAll(n => n.getAttribute?.('aria-label') === label)[0];
const buttonIn = (c, text) => nodes(c, 'button').find(n => n.textContent === text || n.getAttribute('aria-label') === text);
const fieldAfter = (c, words) => nodes(c, 'input').find(n => n.parentNode.textContent.startsWith(words));
const ROOT = 'invented-library:library-v9.9.9', METHOD = 'invented.package.sha256/v1', PROJECT = '/invented/project', LIB = 'workflow-library:invented';
const undeclared = {raw: null, reading: 'undeclared', categories: {checkpoints: 'undeclared', expected_inputs: 'undeclared', required_tools: 'undeclared', returned_evidence: 'undeclared', returned_outputs: 'undeclared'}, elements: {}, findings: []};
const identity = (name, over = {}) => ({kind: 'workflow', origin: 'bundled', source_root: ROOT, name, revision: `${name}-revision-0123456789abcdef`, revision_method: METHOD, ...over});
const entry = (name, displayName = 'Plan the work', order = 1) => ({name, revision: `${name}-revision-0123456789abcdef`, origin: 'bundled', sourceRoot: ROOT, revisionMethod: METHOD, identity: identity(name), runnable: true, runLimit: null,
  description: `Invented description of ${name}.`, roles: ['HELP_HUMAN'], navigation: {category: 'core', tier: 'primary', order, displayName}, libraryPathsNamed: []});
const registered = {name: 'site-check', sequence: 2, revision: 'site-check-2-rev-0123456789abcdef', label: 'registered — approved in this App session (native A15)', evidence: 'in-process A15', selectable: true, reconfirm: false};
const library = {reference: LIB, root: {encoding: 'unix_bytes', bytes: [...new TextEncoder().encode(PROJECT)]}, origin: 'project', sourceRoot: PROJECT, registered: [registered],
  entryListing: {state: 'not observed', entries: [], limits: []}};
const thread = id => ({generation: g, threadId: id, appRole: {standing: 'app-observed', role: 'HELP_HUMAN'}, roleRelation: {kind: 'start'}, futureGuidanceNotices: [], status: {type: 'idle'}});
const OPEN = 'open (live); only the person\'s explicit end ends it';
const PREPARED = 'prepared; not a run until its start turn is observed';

/** The stand-in host. `fail` names a step to refuse (with the host's message) or to leave without its effect; `lost`
 * does the step and loses its reply. `state.view`, when set, changes what a status read returns (a row given in part, a
 * list not readable); `state.before` runs before each command; `declaration` and `compatibility` are a selection's. */
function standIn({threads = [], selections = [], runs = [], projectLibraryAvailable = true, fail = {}, declaration = undeclared, compatibility = undefined} = {}) {
  const state = {calls: [], prepared: 0, sel: 0, snapshot: null, fail, view: null, before: null};
  const root = {context: {sourceRef: 'src', generation: g, historyEpoch: 3}, projectLibraryAvailable, productionCatalog: {standing: 'invented', source: {tag: 'library-v9.9.9'}, entries: [entry('plan-work'), entry('tidy-notes', 'Tidy the notes', 2)]},
    activeLibrary: LIB, libraries: [library], selections, runs, reviews: [], offers: [], reopened: {runs: []}};
  state.snapshot = {state: 'ready', generation: g, homeRouting: {activeModeHomeClass: 'account'}, roleLimits: {account: {roles: []}},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'fixture role', default_for_new_chat: true}]},
    threads: threads.map(thread), workflowRoot: root};
  const select = (threadId, id) => { state.sel += 1; root.selections = [...root.selections.filter(row => row.threadId !== threadId),
    {sourceRef: 'src', threadId, selection: {reference: `sel-${state.sel}`, identity: id, runnable: true, runLimit: null, currentLimit: null, newerRevision: null, assurance: null, declaration, ...(compatibility ? {compatibility} : {})}}]; };
  const run = ref => root.runs.find(row => row.reference === ref);
  state.invoke = async (command, args) => {
    const fail = state.fail;
    state.calls.push({command, args: structuredClone(args)});
    state.before?.(command, args);
    if (command === 'host_status') { if (fail.status && state.calls.some(c => c.command === fail.status.after)) throw Error('status unavailable');
      const read = structuredClone(state.snapshot); return state.view ? state.view(read) ?? read : read; }
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_available_models') return {state: 'observed', generation: args.generation, modeHomeClass: args.modeHomeClass, serverProvider: 'openai', serverProviderState: 'named', complete: true, limits: [], models: []};
    if (command === 'thread_start') {
      // A refusal the host makes before anything is dispatched (App.tsx START_REFUSED_BEFORE_DISPATCH), and a rejection it does not class.
      if (fail.start === 'refused') throw Error('thread start in progress');
      if (fail.start === 'rejected') throw Error('Invented rejection the App does not class');
      if (fail.start === 'unknown') return {result: {thread: {}}};
      state.snapshot.threads = [...state.snapshot.threads, thread('created')];
      return {startGeneration: g, result: {thread: {id: 'created'}}};
    }
    if (command === 'workflow_select_production_bundle') {
      if (fail.select && fail.select !== 'lost') throw Error(fail.select);
      select(args.context.threadId, identity(args.name));
      if (fail.select === 'lost') throw Error('no reply');
      return {choiceChat: {sourceRef: 'src', threadId: args.context.threadId}};
    }
    if (command === 'workflow_select_listed') {
      if (fail.select) throw Error(fail.select);
      select(args.context.threadId, identity(args.name, {origin: 'project', source_root: PROJECT, revision: args.revision})); return {choiceChat: {sourceRef: 'src', threadId: args.context.threadId}};
    }
    if (command === 'workflow_prepare_run') {
      if (fail.prepare && fail.prepare !== 'lost') throw Error(fail.prepare);
      state.prepared += 1;
      const reference = `run:workflow:${state.prepared}`;
      root.runs = [...root.runs, {reference, conversation: args.threadId, home: g.home, generation: g, source: null, lifecycle: {state: PREPARED}, preparationOrder: root.runs.length,
        status: {state: 'prepared; WR records pending; not sent', sent: false}, publication: fail.admission ? {admissionRefusal: fail.admission} : {state: 'pending; not recorded'}, workflow: {name: 'plan-work'}}];
      if (fail.prepare === 'lost') throw Error('no reply');
      return {reference, state: 'original registered selection prepared; WR records pending; not sent'};
    }
    if (command === 'conversation_send_text') return {result: {}};
    if (command === 'workflow_follow_newer_revision') {
      if (fail.follow) throw Error(fail.follow);
      const row = root.selections.find(r => r.threadId === args.context.threadId);
      const newer = row.selection.newerRevision;
      select(args.context.threadId, {...row.selection.identity, revision: newer.revision});
      return {choiceChat: {sourceRef: 'src', threadId: args.context.threadId}};
    }
    if (command === 'workflow_send_run') {
      const row = run(args.runRef);
      if (fail.send === 'before') throw Error('Original run operation pending');
      if (fail.send === 'refused') { row.lifecycle = {state: 'start not confirmed'}; row.status = {state: 'native workflow-text turn/start refused by Codex', limit: 'invented refusal'}; row.source = {}; throw Error('turn/start refused'); }
      if (fail.send === 'unknown') { row.lifecycle = {state: 'start not confirmed'}; row.status = {state: 'native workflow-text turn/start outcome unknown'}; row.source = {}; throw Error('no reply'); }
      row.source = {requestIdentity: 12}; row.lifecycle = {state: OPEN}; row.turn = 'turn-1';
      return {state: 'sent'};
    }
    throw Error(`Unexpected command: ${command}`);
  };
  return state;
}

const ISSUED_ONLY = new Set(['host_status', 'decision_view', 'native_confirmation_content', 'read_available_models', 'read_fleet_records']);
/** Mounts the App over the stand-in; `ui.issued()` is every command but the reads the App makes by itself. */
async function mounted(host, check) {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const idle = installIdleNativeWaiting(host.invoke, {navigatorRead: () => navigatorReadOf(g, (host.snapshot?.threads ?? []).map(t => t.threadId))});
  // The App's timed status reads, run when the test says (as model-choice.test.mjs does).
  const intervals = new Map(), previous = {setInterval: globalThis.setInterval, clearInterval: globalThis.clearInterval}; let timer = 0;
  globalThis.setInterval = fn => { intervals.set(++timer, fn); return timer; }; globalThis.clearInterval = id => intervals.delete(id);
  const library = () => c.querySelectorAll(n => n.getAttribute?.('id') === 'view-library')[0];
  const ui = {c, host,
    tick: async () => React.act(async () => { for (const fn of intervals.values()) await fn(); }),
    issued: () => host.calls.filter(call => !ISSUED_ONLY.has(call.command)),
    names: () => ui.issued().map(call => call.command),
    composer: () => c.querySelectorAll(n => n.localName === 'form' && n.getAttribute('class') === 'chat-input-row')[0],
    send: () => sendButton(c),
    pick: async (name = 'Included workflow plan-work') => {
      await ui.tick();
      const card = labelled(library(), name);
      if (!card) throw Error(`${name} not drawn; library shows: ${labelled(c, 'Workflows')?.textContent.slice(0, 400)}`);
      const use = buttonIn(card, 'Use in message');
      if (!use) throw Error(`no Use in message: ${card.textContent}`);
      assert.equal(!!props(use).disabled, false, 'Use in message is offered');
      await React.act(async () => props(use).onClick());
    },
    write: async text => React.act(async () => props(chatInput(c)).onChange({target: {value: text}})),
    press: async () => { const send = sendButton(c); assert.equal(!!props(send).disabled, false, 'Start run is offered'); await React.act(async () => { await props(send).onClick({preventDefault() {}}); }); },
    /** Lets a press that reads again after a short wait (a run row given in part) finish. */
    settle: async (ms = 1300) => React.act(async () => { await new Promise(resolve => setTimeout(resolve, ms)); }),
    alert: () => c.querySelectorAll(n => n.getAttribute?.('role') === 'alert').map(n => n.textContent).join('\n'),
    newChat: async () => {
      await React.act(async () => props(newChatButton(c)).onClick());
      await React.act(async () => props(fieldAfter(c, 'Model ')).onChange({target: {value: 'chosen-model'}}));
    },
    choose: async id => { const radio = c.querySelectorAll(n => n.localName === 'input' && props(n)?.name === 'current-conversation' && props(n)?.value === key(id))[0];
      await React.act(async () => props(radio).onChange({target: {checked: true}})); },
  };
  try {
    await React.act(async () => root.render(React.createElement(App)));
    await check(ui);
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text);
    globalThis.setInterval = previous.setInterval; globalThis.clearInterval = previous.clearInterval; }
}
const TEXT = 'Plan the survey summary from notes/ é 家';

test('the message box takes the height of its draft, measured again as the draft changes', async () => {
  const proto = Object.getPrototypeOf(document.createElement('textarea'));
  // The mini-DOM measures nothing: a stand-in measure of one 22px line per line of the draft.
  Object.defineProperty(proto, 'scrollHeight', {configurable: true, get() { return 22 * String(props(this)?.value ?? '').split('\n').length; }});
  try {
    await mounted(standIn(), async ui => {
      await ui.newChat();
      await ui.write('one line');
      assert.ok(chatInput(ui.c).style.height === '22px', `one line: ${chatInput(ui.c).style.height}`);
      await ui.write('one\ntwo\nthree');
      assert.ok(chatInput(ui.c).style.height === '66px', `three lines: ${chatInput(ui.c).style.height}`);
      await ui.write('');
      assert.ok(chatInput(ui.c).style.height === '22px', `emptied: ${chatInput(ui.c).style.height}`);
    });
  } finally { delete proto.scrollHeight; }
});

test('picking a workflow lands in the message box; removing the pick returns the focus to the message box', async () => {
  const proto = Object.getPrototypeOf(document.createElement('textarea')); const focused = [], scrolled = [];
  const previous = {focus: proto.focus, scroll: proto.scrollIntoView};
  proto.focus = function () { focused.push(this); }; proto.scrollIntoView = function () { scrolled.push(this); };
  try {
    await mounted(standIn(), async ui => {
      await ui.newChat();
      focused.length = 0; scrolled.length = 0;
      await ui.pick();
      assert.ok(focused.length === 1 && focused[0].getAttribute('id') === 'ordinary-composer-text', 'the message box takes the focus once');
      assert.ok(scrolled.length === 1 && scrolled[0] === focused[0], 'and is brought into view');
      focused.length = 0; scrolled.length = 0;
      const remove = buttonIn(ui.composer(), 'Remove the picked workflow');
      assert.ok(!!remove, 'the chip offers its removal, named in the App\'s words');
      await React.act(async () => props(remove).onClick());
      // The Remove button is unmounted with the chip: the focus goes to the message box rather than to the page.
      assert.ok(!buttonIn(ui.composer(), 'Remove the picked workflow'), 'the chip and its button are gone');
      assert.ok(focused.length === 1 && focused[0] === chatInput(ui.c), 'the message box takes the focus');
      assert.ok(scrolled.length === 0, 'and the view does not move');
    });
  } finally { proto.focus = previous.focus; proto.scrollIntoView = previous.scroll; }
});

test('the chip shows the workflow\'s name and its source; the revision digest is whole under its Details', async () => {
  await mounted(standIn({threads: ['T1']}), async ui => {
    await ui.choose('T1'); await ui.pick();
    const chip = ui.composer().querySelectorAll(n => n.localName === 'li' && n.getAttribute('class') === 'method-chip')[0];
    assert.ok(chip, 'the chip is drawn');
    const small = chip.querySelectorAll(n => n.localName === 'small')[0];
    assert.equal(chip.querySelectorAll(n => n.localName === 'span')[0].textContent, 'Plan the work', 'the workflow\'s name as the library gives it');
    assert.equal(small.textContent, 'Chirality Library 9.9.9', 'its source');
    assert.ok(!small.textContent.includes('·') && !/revision|0123456789/.test(small.textContent), `name and source only: ${small.textContent}`);
    assert.ok(!chip.querySelectorAll(n => n.localName === 'code')[0], 'no digest on the chip');
    const details = ui.composer().querySelectorAll(n => n.localName === 'details' && n.getAttribute('class') === 'v4-pick-details')[0];
    assert.ok(details && !props(details).open, 'Details is closed');
    assert.ok(details.querySelectorAll(n => n.localName === 'code' && n.textContent === 'plan-work-revision-0123456789abcdef')[0], 'the digest, whole, under Details');
  });
});

test('a new chat: the first press starts the conversation and chooses the included workflow, then stops to show its tools; the second prepares and sends it once', async () => {
  await mounted(standIn(), async ui => {
    await ui.newChat();
    await ui.pick();
    await ui.write(TEXT);
    assert.equal(ui.send().textContent, 'Start run');
    assert.deepEqual(ui.issued(), [], 'picking and writing issue nothing');
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle']);
    const select = ui.issued()[1].args;
    assert.deepEqual(Object.keys(select).sort(), ['context', 'name']);
    assert.equal(select.name, 'plan-work');
    assert.deepEqual(select.context, {sourceRef: 'src', generation: g, historyEpoch: 3, threadId: 'created', selectionRef: null, inspectionRef: null, libraryRef: LIB}, 'the guide\'s context, for the new conversation');
    const order = ui.host.calls.map(call => call.command);
    assert.ok(order.indexOf('host_status', order.indexOf('thread_start')) < order.indexOf('workflow_select_production_bundle'), 'the status is read for the new row before choosing');
    assert.match(ui.c.textContent, /Read what it needs, then press Start run\. Nothing has been sent\./);
    assert.match(labelled(ui.c, 'Workflow for this message').textContent, /Required tools: not declared, so the App can't check them\./, 'the check is shown before anything is sent');
    assert.equal(props(chatInput(ui.c)).value, TEXT, 'the text is kept');
    // Left here, the conversation reads as what it is: a workflow chosen and no run started, not a run.
    assert.equal(labelled(ui.c, 'Workflow chosen, not started')?.textContent, 'Workflow chosen for this conversation: plan-work. No run has been started.');
    await ui.press();
    assert.ok(!labelled(ui.c, 'Workflow chosen, not started'), 'once a run of the conversation exists, the note is gone');
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    const prepare = ui.issued()[2].args;
    assert.deepEqual({...prepare, context: undefined}, {generation: g, threadId: 'created', personText: TEXT, context: undefined});
    assert.equal(prepare.context.selectionRef, 'sel-1', 'prepared against the selection read after choosing');
    assert.deepEqual(ui.issued()[3].args, {runRef: 'run:workflow:1'});
    // Started: the text and the pick are cleared, and the composer is the ordinary one again.
    assert.equal(props(chatInput(ui.c)).value, '');
    assert.equal(labelled(ui.c, 'Workflow for this message'), undefined);
    assert.equal(props(ui.send())['aria-label'], 'Send text');
  });
});

test('an open conversation: a registered revision is chosen with its library and revision, then prepared and sent; one already chosen goes straight to prepare and send', async () => {
  await mounted(standIn({threads: ['T1']}), async ui => {
    await ui.choose('T1');
    await ui.pick('Project workflow site-check');
    await ui.write(TEXT);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_listed']);
    const args = ui.issued()[0].args;
    assert.deepEqual({...args, context: undefined}, {libraryRef: LIB, name: 'site-check', revision: 'site-check-2-rev-0123456789abcdef', context: undefined});
    assert.equal(args.context.threadId, 'T1');
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_listed', 'workflow_prepare_run', 'workflow_send_run']);
    assert.equal(ui.issued()[1].args.threadId, 'T1');
  });
  // The conversation already has the picked workflow chosen: its tools are in view before the press, and one press runs.
  const chosen = [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-0', identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared}}];
  await mounted(standIn({threads: ['T1'], selections: chosen}), async ui => {
    await ui.choose('T1');
    await ui.pick();
    await ui.write(TEXT);
    assert.match(labelled(ui.c, 'Workflow for this message').textContent, /Required tools: not declared/);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_prepare_run', 'workflow_send_run']);
    assert.equal(ui.issued()[0].args.context.selectionRef, 'sel-0');
  });
});

test('a failure at each step keeps the text, says what happened, issues nothing after it, and a second press goes on from the first step not done', async () => {
  // Step 1 refused: nothing chosen; the person stays in New chat.
  await mounted(standIn({fail: {start: 'refused'}}), async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['thread_start']);
    assert.match(ui.alert(), /Couldn't start the conversation: thread start in progress\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'the pick is still shown');
  });
  // Step 1 rejected in words the App does not class as a refusal before dispatch: not confirmed, never "nothing started".
  await mounted(standIn({fail: {start: 'rejected'}}), async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['thread_start']);
    assert.match(ui.alert(), /The App couldn't confirm the conversation started; it may exist\. The workflow wasn't sent\./);
    assert.doesNotMatch(ui.alert(), /Couldn't start the conversation/);
  });
  // Step 1 not confirmed.
  await mounted(standIn({fail: {start: 'unknown'}}), async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['thread_start']);
    assert.match(ui.alert(), /The App couldn't confirm the conversation started; it may exist\. The workflow wasn't sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    // One may exist, so another start waits for the person: Start run is not offered, the pause is said, and the
    // rejected case above is held the same way.
    const paused = () => labelled(ui.c, 'Starting is paused');
    assert.ok(!!paused(), 'the pause is said');
    assert.ok(props(ui.send()).disabled === true, 'Start run is not offered while the start is in doubt');
    assert.match(ui.composer().textContent, /A conversation may already have started\. Choose it on the left, or say to start another\./);
    await React.act(async () => { await props(ui.send()).onClick({preventDefault() {}}); });
    assert.deepEqual(ui.names(), ['thread_start'], 'a press while paused starts nothing');
    // The person says to start another: the pause ends, and only then does a press start one.
    await React.act(async () => props(buttonIn(paused(), 'Start another conversation')).onClick());
    assert.ok(!paused(), 'the pause is gone once the person says so');
    assert.ok(props(ui.send()).disabled !== true, 'Start run is offered again');
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'the pick is kept');
  });
  // Step 3 refused: the conversation exists and is shown; the next press chooses again, in it.
  const host = standIn({fail: {select: 'Native history context is busy; refresh the workflow choice'}});
  await mounted(host, async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle']);
    assert.match(ui.alert(), /The conversation started, but the workflow wasn't chosen: the App was busy reading conversation history\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'the pick is still shown, in the new conversation');
    assert.equal(ui.c.querySelectorAll(n => n.localName === 'input' && props(n)?.name === 'current-conversation' && props(n)?.checked === true)[0] && props(ui.c.querySelectorAll(n => n.localName === 'input' && props(n)?.name === 'current-conversation' && props(n)?.checked === true)[0]).value, key('created'));
    // The host now accepts: the second press chooses in that conversation, with no second start.
    host.fail = {};
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle', 'workflow_select_production_bundle']);
    assert.equal(ui.issued()[2].args.context.threadId, 'created');
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle', 'workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
  });
  // Step 5 refused, then a second press: no second start or choice; prepare and send.
  const prep = standIn({threads: ['T1'], fail: {prepare: 'No explicit App project (CHIRALITY_WORKSPACE): WR recording unavailable, so the workflow run is not prepared or sent; no fallback store'}});
  await mounted(prep, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); // chooses, then stops to show the tools
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run']);
    assert.match(ui.alert(), /The run wasn't prepared: No explicit App project \(CHIRALITY_WORKSPACE\): WR recording unavailable, so the workflow run is not prepared or sent; no fallback store\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    prep.fail = {};
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_prepare_run', 'workflow_send_run'], 'the choice is not made again');
  });
  // Step 6 refused before sending: the same prepared run may be started again; it is not prepared again.
  const before = standIn({threads: ['T1'], fail: {send: 'before'}});
  await mounted(before, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    assert.match(ui.alert(), /The run wasn't started: Original run operation pending\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    before.fail = {};
    await ui.press();
    assert.deepEqual(ui.issued().filter(call => call.command === 'workflow_send_run').map(call => call.args.runRef), ['run:workflow:1', 'run:workflow:1'], 'the same prepared run, not prepared again');
    assert.equal(ui.names().filter(name => name === 'workflow_prepare_run').length, 1);
    assert.equal(props(chatInput(ui.c)).value, '', 'started: the text is cleared');
  });
});

test('a failed step is said once in view, in the App\'s sentence; the host\'s line is one action away, whole and marked', async () => {
  const reply = 'No explicit App project (CHIRALITY_WORKSPACE): WR recording unavailable, so the workflow run is not prepared or sent; no fallback store';
  const prep = standIn({threads: ['T1'], fail: {prepare: reply}});
  await mounted(prep, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    const said = ui.c.querySelectorAll(n => n.getAttribute?.('class') === 'v4-step-outcome')[0];
    assert.ok(said, 'the App\'s sentence beside the message box');
    assert.ok(ui.composer().parentNode.contains(said));
    const alert = said.querySelectorAll(n => n.getAttribute?.('role') === 'alert')[0];
    assert.match(alert.textContent, /^The run wasn't prepared: /);
    const details = said.querySelectorAll(n => n.localName === 'details')[0];
    assert.ok(details && !props(details).open, 'closed');
    assert.equal(details.querySelectorAll(n => n.localName === 'summary')[0].textContent, 'Details');
    const marked = details.querySelectorAll(n => (n.getAttribute?.('aria-label') ?? '').startsWith('The latest response, which may carry text the App received'))[0];
    assert.ok(marked, 'marked as text the App did not write');
    assert.ok(marked.textContent.includes(`workflow_prepare_run: Error: ${reply}`), 'nothing the host said is dropped');
    // Nothing above the conversation says it again: no command-prefixed block, and the command's name once in the page.
    assert.ok(!ui.c.querySelectorAll(n => n.getAttribute?.('aria-label') === 'Latest App response')[0], 'no response block above the conversation');
    assert.equal(ui.c.textContent.split('workflow_prepare_run:').length - 1, 1);
    // A new press clears it; the next failure's line replaces it.
    prep.fail = {};
    await ui.press();
    assert.ok(!ui.c.querySelectorAll(n => n.getAttribute?.('class') === 'v4-step-outcome')[0], 'a press that starts the run leaves no failure behind');
  });
});

test('a send whose start is not confirmed is never sent again: the guide\'s words, and a new run only after the acknowledgement', async () => {
  const host = standIn({threads: ['T1'], fail: {send: 'unknown'}});
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    assert.match(ui.alert(), /Start not confirmed — outcome unknown\. The App could not confirm whether Codex received the starting message.*The App will not resend it\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT, 'the text is kept');
    // The conversation now holds a start of unknown outcome: Start run waits for the guide's acknowledgement.
    assert.equal(!!props(ui.send()).disabled, true);
    assert.match(ui.c.textContent, /Read the conversation: the last start's outcome is unknown and it may have run\./);
    const box = ui.c.querySelectorAll(n => n.localName === 'input' && props(n)?.type === 'checkbox')[0];
    assert.match(box.parentNode.textContent, /I read the conversation and want to prepare a new run anyway/);
    await React.act(async () => props(box).onChange({target: {checked: true}}));
    await ui.press();
    const sends = ui.issued().filter(call => call.command === 'workflow_send_run').map(call => call.args.runRef);
    assert.deepEqual(sends, ['run:workflow:1', 'run:workflow:2'], 'the unconfirmed run is not sent again; a new prepared run is');
  });
});

test('Codex refusing the start, and a prepared run whose records cannot be saved, are said and not sent again', async () => {
  await mounted(standIn({threads: ['T1'], fail: {send: 'refused'}}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press(); await ui.press();
    assert.match(ui.alert(), /Codex refused to start the run\. Codex refused the starting message, so this workflow did not run\. Reason: invented refusal\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
  });
  await mounted(standIn({threads: ['T1'], fail: {admission: 'records store not admitted'}}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press(); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run'], 'not sent');
    assert.match(ui.alert(), /The run was prepared, but its records can't be saved: records store not admitted\. It wasn't started\. Nothing was sent\./);
  });
});

test('a selection the host does not admit stops the press with the host\'s reason; nothing is prepared', async () => {
  const host = standIn({threads: ['T1']});
  const invoke = host.invoke;
  host.invoke = async (command, args) => {
    const value = await invoke(command, args);
    if (command === 'workflow_select_production_bundle') host.snapshot.workflowRoot.selections[0].selection = {...host.snapshot.workflowRoot.selections[0].selection, runnable: false, runLimit: 'the bundled copy differs from the release'};
    return value;
  };
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle']);
    assert.match(ui.alert(), /The workflow can't run: the bundled copy differs from the release\. Nothing was sent\./);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle'], 'a second press prepares nothing either');
  });
});

test('an open conversation\'s run that is still open stops Start run, as the Run guide did, and says where to end it', async () => {
  const open = [{reference: 'run:workflow:0', conversation: 'T1', home: g.home, generation: g, source: {}, lifecycle: {state: OPEN}, preparationOrder: 0, status: {}, workflow: {name: 'plan-work'}}];
  await mounted(standIn({threads: ['T1'], runs: open}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.equal(!!props(ui.send()).disabled, true);
    assert.match(ui.c.textContent, /A workflow run is still open in this conversation\. End it with End run in the Run tab before starting another\./);
    assert.deepEqual(ui.issued(), []);
  });
  // A run opened after the view was drawn: the press reads the host first and stops before choosing anything.
  const later = standIn({threads: ['T1']});
  await mounted(later, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    later.snapshot.workflowRoot.runs = open;
    await ui.press();
    assert.deepEqual(ui.issued(), []);
    assert.match(ui.alert(), /A workflow run is still open in this conversation\. End it with End run in the Run tab before starting another\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
  });
  // Runs whose order the App can't tell (no preparationOrder): an open one among them still holds a new run, and a start
  // of unknown outcome among them is said without a "last start" claim (ported from the Run a workflow guide's Results test).
  const unordered = over => [{reference: 'run:workflow:y', conversation: 'T1', home: g.home, generation: g, source: {}, lifecycle: {state: 'ended', end: {cause: 'completed'}}, status: {}, workflow: {name: 'plan-work'}},
    {reference: 'run:workflow:x', conversation: 'T1', home: g.home, generation: g, source: {}, status: {}, workflow: {name: 'plan-work'}, ...over}];
  await mounted(standIn({threads: ['T1'], runs: unordered({lifecycle: {state: OPEN}})}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.equal(!!props(ui.send()).disabled, true, 'an open run among them still holds a new preparation');
    assert.match(ui.c.textContent, /A workflow run is still open in this conversation\./);
    assert.deepEqual(ui.issued(), []);
  });
  await mounted(standIn({threads: ['T1'], runs: unordered({lifecycle: {state: 'start not confirmed (turn refused or outcome unknown); not opened, not live'}, status: {state: 'native workflow-text send outcome unknown; original source retained'}})}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.equal(!!props(ui.send()).disabled, true);
    assert.match(ui.c.textContent, /Read the conversation: a start here has an unknown outcome and may have run; the App can't tell which run is latest\./, 'no "last start" claim without an order');
    assert.doesNotMatch(ui.c.textContent, /the last start's outcome/);
    assert.deepEqual(ui.issued(), []);
  });
});

test('a change of workflow source or generation drops the pick, says so in one line, and issues nothing', async () => {
  const host = standIn({threads: ['T1']});
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    host.snapshot.workflowRoot.context = {...host.snapshot.workflowRoot.context, sourceRef: 'src-2'};
    // The App's own timed read brings the change.
    await ui.tick();
    assert.equal(labelled(ui.c, 'Workflow for this message'), undefined);
    assert.match(ui.c.textContent, /The workflow you picked was removed: Codex or the workflow source changed\. Pick it again under Workflows\./);
    assert.equal(ui.send().textContent, '↑', 'the ordinary Send again');
    assert.deepEqual(ui.issued(), []);
  });
  // A new Codex generation: the same.
  const gen = standIn({threads: ['T1']});
  await mounted(gen, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    const next = {...g, spawnCounter: 2};
    gen.snapshot.generation = next; gen.snapshot.workflowRoot.context = {...gen.snapshot.workflowRoot.context, generation: next};
    await ui.tick();
    assert.equal(labelled(ui.c, 'Workflow for this message'), undefined);
    assert.deepEqual(ui.issued(), []);
  });
  // The source changes while the press runs: it stops after the step under way, and nothing after it is issued.
  const under = standIn({threads: ['T1']});
  const invoke = under.invoke;
  under.invoke = async (command, args) => {
    const value = await invoke(command, args);
    if (command === 'workflow_select_production_bundle') under.snapshot.workflowRoot.context = {...under.snapshot.workflowRoot.context, sourceRef: 'src-2'};
    return value;
  };
  await mounted(under, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle']);
    assert.match(ui.alert(), /Codex or the workflow source changed, so the App stopped\. The workflow was chosen for it\. Nothing was sent\./);
    assert.match(ui.c.textContent, /The workflow you picked was removed: Codex or the workflow source changed\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
  });
});

test('the pick survives switching tabs; the Workflows button shows the tab; without a pick the composer sends as before', async () => {
  await mounted(standIn({threads: ['T1']}), async ui => {
    const tab = id => ui.c.querySelectorAll(n => n.getAttribute?.('id') === id)[0];
    await ui.choose('T1');
    const workflows = nodes(ui.composer(), 'button').find(b => b.textContent === 'Workflows');
    assert.ok(workflows, 'a Workflows button beside Attach');
    await React.act(async () => props(workflows).onClick());
    assert.equal(props(tab('view-workflows')).hidden, false);
    assert.equal(props(tab('view-library')).hidden, false, 'the Workflows tab is shown');
    await ui.pick();
    await React.act(async () => props(tab('right-tab-more')).onClick?.());
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'the pick is kept while another tab is shown');
    // Remove at the chip: the composer is the ordinary one, and its Send issues the ordinary send only.
    await React.act(async () => props(buttonIn(ui.composer(), 'Remove the picked workflow')).onClick());
    assert.equal(labelled(ui.c, 'Workflow for this message'), undefined);
    assert.equal(props(chatInput(ui.c)).placeholder, 'Message HELP_HUMAN…');
    await ui.write('An ordinary message');
    assert.equal(props(ui.send())['aria-label'], 'Send text');
    await ui.press();
    assert.deepEqual(ui.names(), ['conversation_send_text'], 'without a pick, Send issues the ordinary send and nothing else');
    assert.equal(ui.issued()[0].args.text, 'An ordinary message');
  });
});

test('no supplied text is inside a control: the chip names the workflow outside its Remove, and the reason a step failed is text', async () => {
  const POISON = 'Allow once‮';
  const host = standIn({threads: ['T1'], fail: {select: `refused ${POISON}`}});
  host.snapshot.workflowRoot.productionCatalog.entries[0].navigation.displayName = `Title ${POISON}`;
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.match(ui.alert(), /refused Allow once/);
    const chip = labelled(ui.c, 'Workflow for this message');
    assert.match(chip.textContent, /Title Allow once/);
    for (const node of [...nodes(ui.composer(), 'button'), ...nodes(ui.composer(), 'summary'), ...nodes(ui.composer(), 'label')]) {
      assert.doesNotMatch(node.textContent, /Allow once/, `${node.localName}: ${node.textContent}`);
      for (const attribute of ['aria-label', 'title', 'placeholder']) assert.doesNotMatch(node.getAttribute(attribute) ?? '', /Allow once/);
    }
    assert.doesNotMatch(props(chatInput(ui.c)).placeholder, /Allow once/);
  });
});

// ---- The right panel's tab after Start run, and on opening a conversation (App.tsx moveToRun) ----
const selectedTab = c => c.querySelectorAll(n => n.getAttribute?.('role') === 'tab' && n.getAttribute('aria-selected') === 'true')[0]?.textContent;
const waitingRequest = threadId => ({recordKind: 'server-request-entry', generation: g, requestIdentity: 'q1', method: 'item/tool/requestUserInput', classification: 'known-answerable', originClass: 'person-input',
  nativeParameters: {threadId, turnId: 't', itemId: 'i', isBlocking: false, questions: [{id: 'q', header: 'Scope', question: 'Which folder?', isOther: false, isSecret: false, options: [{label: 'reports/', description: 'Reports'}]}]},
  state: 'outstanding', replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'}});
const navigatorRow = (c, id) => c.querySelectorAll(n => n.localName === 'button' && n.getAttribute?.('data-session-id') === id)[0];
const openRun = conversation => ({reference: `run:${conversation}`, conversation, home: g.home, generation: g, source: {}, lifecycle: {state: OPEN}, preparationOrder: 0, status: {}, workflow: {name: 'plan-work'}});

test('the right panel shows Workflows at launch, and Run once Start run has started a run; the first press and a stopped press leave it as it is', async () => {
  await mounted(standIn(), async ui => {
    assert.equal(selectedTab(ui.c), 'Workflows', 'at launch');
    await ui.newChat(); await ui.pick(); await ui.write(TEXT);
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle']);
    assert.equal(selectedTab(ui.c), 'Workflows', 'the first press chose the workflow and stopped: no run, no move');
    await ui.press();
    assert.deepEqual(ui.names().slice(-2), ['workflow_prepare_run', 'workflow_send_run']);
    assert.equal(selectedTab(ui.c), 'Run', 'the run started: the Run tab');
    assert.equal(props(ui.c.querySelectorAll(n => n.getAttribute?.('id') === 'view-current-run')[0]).hidden, false);
  });
  await mounted(standIn({threads: ['T1'], fail: {prepare: 'Workflow App source changed; nothing selected or prepared'}}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press(); await ui.press();
    assert.match(ui.alert(), /run wasn't prepared/);
    assert.equal(selectedTab(ui.c), 'Workflows', 'a press that stopped moves nothing');
  });
});

test('after Start run, unsent work in another view or a request waiting on the person keeps the right panel where it is', async () => {
  // Unsent work: a draft name typed in the workflow studio, under More.
  await mounted(standIn({threads: ['T1']}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await React.act(async () => props(fieldAfter(ui.c, 'New draft name')).onChange({target: {value: 'unsent-draft-name'}}));
    await ui.press(); await ui.press();
    assert.deepEqual(ui.names().slice(-2), ['workflow_prepare_run', 'workflow_send_run']);
    assert.equal(selectedTab(ui.c), 'Workflows', 'the person\'s unsent work is not left behind');
  });
  // A request waiting on the person, in another conversation.
  const host = standIn({threads: ['T1', 'T2']});
  host.snapshot.serverRequests = [waitingRequest('T2')];
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press(); await ui.press();
    assert.deepEqual(ui.names().slice(-2), ['workflow_prepare_run', 'workflow_send_run']);
    assert.equal(selectedTab(ui.c), 'Workflows', 'a request waits on the person: the App stays');
  });
});

test('opening a conversation that has a run shows the Run tab; one with none leaves the panel; unsent text or a waiting request blocks the move', async () => {
  await mounted(standIn({threads: ['T1', 'T2'], runs: [openRun('T2')]}), async ui => {
    const before = ui.issued().length;
    await React.act(async () => props(navigatorRow(ui.c, 'T1')).onClick());
    assert.equal(selectedTab(ui.c), 'Workflows', 'no run: left as it is');
    await React.act(async () => props(ui.c.querySelectorAll(n => n.getAttribute?.('id') === 'right-tab-more')[0]).onClick());
    await React.act(async () => props(navigatorRow(ui.c, 'T2')).onClick());
    assert.equal(selectedTab(ui.c), 'Run', 'a run: the Run tab');
    assert.equal(ui.issued().length, before, 'opening issues no command');
  });
  await mounted(standIn({threads: ['T1', 'T2'], runs: [openRun('T2')]}), async ui => {
    await ui.write('A draft not yet sent');
    await React.act(async () => props(navigatorRow(ui.c, 'T2')).onClick());
    assert.equal(selectedTab(ui.c), 'Workflows', 'unsent text: no move');
    assert.equal(props(chatInput(ui.c)).value, 'A draft not yet sent');
  });
  const host = standIn({threads: ['T1', 'T2'], runs: [openRun('T2')]});
  host.snapshot.serverRequests = [waitingRequest('T1')];
  await mounted(host, async ui => {
    await React.act(async () => props(navigatorRow(ui.c, 'T2')).onClick());
    assert.equal(selectedTab(ui.c), 'Workflows', 'a request waits on the person: no move');
  });
});

// ---- The run guide's "follow the newer revision", at the chip ----
const listedChosen = (newer, over = {}) => [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-0', runnable: true, currentLimit: null, assurance: null, declaration: undeclared,
  identity: identity('site-check', {origin: 'project', source_root: PROJECT, revision: registered.revision}), newerRevision: newer, ...over}}];
const NEWER = {sequence: 3, revision: 'site-check-3-rev-0123456789abcdef', notice: 'newer revision 3 available', selectable: true, offered: 'Select revision 3'};
const withRevision3 = host => { host.snapshot.workflowRoot.libraries = [{...library, registered: [registered, {...registered, sequence: 3, revision: NEWER.revision}]}]; return host; };
const detailsOf = c => labelled(c, 'Workflow for this message');

test('the chip\'s Details offers the guide\'s newer-revision command under its conditions, and the pick follows the revision', async () => {
  const host = withRevision3(standIn({threads: ['T1'], selections: listedChosen(NEWER)}));
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick('Project workflow site-check'); await ui.write(TEXT);
    const note = labelled(detailsOf(ui.c), 'Newer revision for this conversation');
    assert.ok(note, 'the note is at the chip');
    assert.match(note.textContent, /A newer revision of site-check is registered \(newer revision 3 available\)\. This conversation keeps the one it has until you choose the newer one\./);
    const use = buttonIn(note, 'Use the newer revision');
    assert.equal(!!props(use).disabled, false);
    assert.deepEqual(ui.issued(), [], 'reading the note issues nothing');
    await React.act(async () => { await props(use).onClick(); });
    assert.deepEqual(ui.names(), ['workflow_follow_newer_revision']);
    const args = ui.issued()[0].args;
    assert.deepEqual({...args, context: undefined}, {selectionRef: 'sel-0', revision: NEWER.revision, context: undefined}, 'the guide\'s arguments');
    assert.equal(args.context.threadId, 'T1'); assert.equal(args.context.selectionRef, 'sel-0');
    assert.match(detailsOf(ui.c).textContent, /Moved this conversation to the newer revision\./);
    assert.match(detailsOf(ui.c).textContent, /revision 3/, 'the pick is now the revision followed');
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_follow_newer_revision', 'workflow_prepare_run', 'workflow_send_run'], 'Start run does not choose the earlier revision again');
  });
  // The host's refusal is said in the guide's words; nothing else is issued.
  const refused = withRevision3(standIn({threads: ['T1'], selections: listedChosen(NEWER), fail: {follow: 'The selection changed since the notice was shown; nothing selected'}}));
  await mounted(refused, async ui => {
    await ui.choose('T1'); await ui.pick('Project workflow site-check');
    await React.act(async () => { await props(buttonIn(detailsOf(ui.c), 'Use the newer revision')).onClick(); });
    assert.match(detailsOf(ui.c).textContent, /Couldn't move to the newer revision: The selection changed since the notice was shown; nothing selected/);
    assert.deepEqual(ui.names(), ['workflow_follow_newer_revision']);
    assert.match(detailsOf(ui.c).textContent, /revision 2/, 'the pick is unchanged');
  });
});

test('the newer revision at the chip: not selectable says the host\'s words with no command; a limit is said, except for a bundled selection; a stale source disables it', async () => {
  await mounted(withRevision3(standIn({threads: ['T1'], selections: listedChosen({...NEWER, selectable: false, offered: 'registered — re-confirm to use in this App session'})})), async ui => {
    await ui.choose('T1'); await ui.pick('Project workflow site-check');
    const note = labelled(detailsOf(ui.c), 'Newer revision for this conversation');
    assert.match(note.textContent, /registered — re-confirm to use in this App session\./);
    assert.equal(buttonIn(note, 'Use the newer revision'), undefined, 'not selectable: no command offered');
  });
  await mounted(standIn({threads: ['T1'], selections: listedChosen({limit: 'library busy; newer revisions not read now'})}), async ui => {
    await ui.choose('T1'); await ui.pick('Project workflow site-check');
    assert.match(detailsOf(ui.c).textContent, /Newer revisions of site-check can't be checked: library busy; newer revisions not read now/);
  });
  const bundled = [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-0', identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared,
    newerRevision: {limit: "the selection's library is not open in this App session; newer revisions not read"}}}];
  await mounted(standIn({threads: ['T1'], selections: bundled}), async ui => {
    await ui.choose('T1'); await ui.pick();
    assert.ok(detailsOf(ui.c));
    assert.doesNotMatch(detailsOf(ui.c).textContent, /can't be checked|newer revision/i, 'an included workflow has no library revisions to follow');
  });
  // The shown workflow source is not the host's (its Codex generation differs): the command is not offered as usable.
  const stale = withRevision3(standIn({threads: ['T1'], selections: listedChosen(NEWER)}));
  await mounted(stale, async ui => {
    await ui.choose('T1'); await ui.pick('Project workflow site-check');
    const use = () => buttonIn(detailsOf(ui.c), 'Use the newer revision');
    assert.equal(!!props(use()).disabled, false);
    stale.snapshot.workflowRoot.context = {...stale.snapshot.workflowRoot.context, generation: {...g, spawnCounter: 9}};
    await ui.tick();
    if (use()) { assert.equal(!!props(use()).disabled, true, 'disabled while the source is not current'); await React.act(async () => { await props(use()).onClick(); }); }
    assert.deepEqual(ui.names(), [], 'nothing issued');
  });
});

test('a required tool reported missing is said at the chip and never blocks Start run (DEL-02-03 REQ-001)', async () => {
  const tool = {name:'delegate', purpose:'Use delegate.', necessity:'required', stages:['Method'], class:'harness_capability', capability:'agent-delegation'};
  const declaration = {reading:'recognized', findings:[], categories:{required_tools:'recognized'}, elements:{required_tools:[{value:tool, reading:'recognized', findings:[]}]}};
  const compatibility = {preparation:{declaration, requirements:[{outcome:'missing', reason:"the conversation's model reports multiAgentVersion disabled (NPTD §7.1 (1))"}],
    check:{result:'unsupported', tools:[]}, basis:{acting_pin:'App Codex 0.169.0', surface:'X'}}, statement:'requirement check …', advisory:true};
  const chosen = [{sourceRef:'src', threadId:'T1', selection:{reference:'sel-0', identity:identity('plan-work'), runnable:true, currentLimit:null, declaration, compatibility}}];
  await mounted(standIn({threads:['T1'], selections:chosen}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.match(labelled(ui.c, 'Workflow for this message').textContent, /delegate missing\./);
    assert.equal(!!props(ui.send()).disabled, false, 'Start run is offered');
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_prepare_run', 'workflow_send_run']);
  });
});

// ---- What a press may reuse, repeat and send, and what it holds back on (review round 1) ----
const {runPickedWorkflow, pickMemory, pickScope} = loadSrc('WorkflowPick');
const partialRow = reference => ({reference, state: 'original run operation pending', preparationOrder: null});
const checkbox = c => c.querySelectorAll(n => n.localName === 'input' && props(n)?.type === 'checkbox')[0];
const prepares = ui => ui.names().filter(name => name === 'workflow_prepare_run').length;
const sentRefs = ui => ui.issued().filter(call => call.command === 'workflow_send_run').map(call => call.args.runRef);

test('a preparation is reused only for what it was prepared for: another pick in the same conversation, with the same text, prepares anew', async () => {
  const host = standIn({threads: ['T1'], fail: {status: {after: 'workflow_prepare_run'}}});
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run']);
    assert.match(ui.alert(), /The run was prepared, but the App couldn't read its state afterwards, so it wasn't started\. Nothing was sent\./);
    // The reads come back; another workflow is picked and the draft is kept.
    host.fail = {}; await ui.tick();
    await ui.pick('Included workflow tidy-notes');
    assert.equal(props(chatInput(ui.c)).value, TEXT);
    await ui.press();
    assert.deepEqual(ui.names().slice(2), ['workflow_select_production_bundle'], 'the new pick is chosen, then shown');
    await ui.press();
    assert.deepEqual(ui.names().slice(3), ['workflow_prepare_run', 'workflow_send_run'], 'prepared anew for the new pick');
    assert.deepEqual(sentRefs(ui), ['run:workflow:2'], 'the run prepared for the first pick is never sent for the second');
    assert.equal(ui.issued()[3].args.context.selectionRef, 'sel-2');
  });
});

test('a send whose first readings catch the run held by the host is read again: the run that opened is started, and no doubt is said', async () => {
  // The host's own observation of a run just opened holds it for a moment; the status gives the row only in part then.
  const host = standIn({threads: ['T1']});
  let hidden = null, partial = 0;
  host.before = command => { if (command === 'workflow_send_run') hidden = 'run:workflow:1'; };
  host.view = read => { if (hidden && partial < 2) { partial += 1; read.workflowRoot.runs = read.workflowRoot.runs.map(r => r.reference === hidden ? partialRow(r.reference) : r); } };
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press(); await ui.settle(800);
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    assert.equal(partial, 2, 'two readings gave the row in part');
    assert.doesNotMatch(ui.alert(), /Start not confirmed|Nothing was sent|wasn't started/);
    assert.equal(props(chatInput(ui.c)).value, '', 'the text went with the run');
    assert.ok(!labelled(ui.c, 'Workflow for this message'), 'and the pick is used');
  });
});

test('a send the host shows only in part is not confirmed: never "Nothing was sent", held until the person acknowledges, never sent again', async () => {
  const host = standIn({threads: ['T1']});
  let hidden = null, gone = false;
  host.before = command => { if (command === 'workflow_send_run') hidden = 'run:workflow:1'; };
  host.view = read => { read.workflowRoot.runs = read.workflowRoot.runs.filter(r => !(gone && r.reference === hidden)).map(r => r.reference === hidden ? partialRow(r.reference) : r); };
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press(); await ui.settle();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    assert.match(ui.alert(), /Start not confirmed — outcome unknown\. The App could not confirm whether Codex received the starting message\. It may have run\. The App will not resend it\./);
    assert.doesNotMatch(ui.alert(), /Nothing was sent|wasn't started/);
    assert.equal(props(chatInput(ui.c)).value, TEXT, 'the draft is kept');
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'and the pick');
    const held = () => props(ui.send()).disabled === true;
    assert.ok(held(), 'Start run is held');
    assert.ok(!labelled(ui.c, 'Workflow chosen, not started'), 'the conversation is not said to have no run');
    // Later reads give the row in part again, then not at all: the hold stands.
    await ui.tick();
    assert.ok(held(), 'held while the row is given in part');
    gone = true; await ui.tick();
    assert.ok(held(), 'held while the row is missing');
    assert.match(ui.composer().textContent, /Read the conversation: the App couldn't confirm the last start and it may have run\./);
    // The person says they read the conversation: a new run is prepared and sent; the first is never sent again.
    assert.match(checkbox(ui.c).parentNode.textContent, /I read the conversation and want to prepare a new run anyway/);
    await React.act(async () => props(checkbox(ui.c)).onChange({target: {checked: true}}));
    assert.ok(!held(), 'offered once acknowledged');
    await ui.press();
    assert.deepEqual(sentRefs(ui), ['run:workflow:1', 'run:workflow:2']);
    assert.equal(prepares(ui), 2);
  });
});

test('a choice or a preparation whose reply was lost is read for before it is repeated; one the host confirmed is not prepared again', async () => {
  // The choice's reply is lost and the selections cannot be read: the choice is not made again until a read shows them.
  const chooser = standIn({threads: ['T1'], fail: {select: 'lost'}});
  let unreadable = true;
  chooser.view = read => { if (unreadable) delete read.workflowRoot.selections; };
  await mounted(chooser, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press();
    assert.match(ui.alert(), /The App couldn't read whether the workflow was chosen\. Nothing was sent\./);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle'], 'not chosen again while the outcome is not established');
    assert.match(ui.alert(), /The App couldn't establish whether the workflow was chosen, so it didn't choose it again\./);
    unreadable = false; chooser.fail = {};
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle'], 'the read shows it chosen: shown, not chosen again');
    assert.match(ui.c.textContent, /Read what it needs, then press Start run\. Nothing has been sent\./);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
  });
  // The preparation's reply is lost: the run it made is found and sent; it is prepared once.
  await mounted(standIn({threads: ['T1'], fail: {prepare: 'lost'}}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
    assert.deepEqual(sentRefs(ui), ['run:workflow:1']);
  });
  // Lost, and the runs are given in part: nothing is established, so nothing is prepared again until the person says.
  const lost = standIn({threads: ['T1'], fail: {prepare: 'lost'}});
  let part = false;
  lost.before = command => { if (command === 'workflow_prepare_run') part = true; };
  lost.view = read => { if (part) read.workflowRoot.runs = read.workflowRoot.runs.map(r => partialRow(r.reference)); };
  await mounted(lost, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.match(ui.alert(), /The App couldn't establish whether the run was prepared: no reply\. Nothing was sent\./);
    assert.doesNotMatch(ui.alert(), /wasn't prepared/);
    await ui.press();
    assert.equal(prepares(ui), 1, 'not prepared again');
    assert.match(ui.alert(), /The App couldn't establish whether the run was prepared, so it didn't prepare it again\./);
    await React.act(async () => props(checkbox(ui.c)).onChange({target: {checked: true}}));
    lost.fail = {};
    await ui.press();
    assert.equal(prepares(ui), 2, 'prepared again only after the person said to go on');
    assert.deepEqual(sentRefs(ui), [], 'and nothing sent while its row cannot be read');
  });
  // Confirmed with its reference, then given in part on the reads after: kept, not prepared again, sent once readable.
  const confirmed = standIn({threads: ['T1']});
  let reads = 0;
  confirmed.before = command => { if (command === 'workflow_prepare_run') reads = 3; };
  confirmed.view = read => { if (reads > 0) { reads -= 1; read.workflowRoot.runs = read.workflowRoot.runs.map(r => partialRow(r.reference)); } };
  await mounted(confirmed, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    await ui.press(); await ui.press();
    assert.match(ui.alert(), /The run was prepared, but the App can't read it as ready to start now, so it wasn't started\./);
    await ui.press();
    assert.equal(prepares(ui), 1, 'a row given in part on a later read does not discard the preparation');
    reads = 0;
    await ui.press();
    assert.deepEqual(sentRefs(ui), ['run:workflow:1']);
    assert.equal(prepares(ui), 1);
  });
});

test('a press is bound to its conversation: another chosen during the first read stops it before anything is prepared or sent', async () => {
  const chosen = [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-0', identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared}}];
  const host = standIn({threads: ['T1', 'T2'], selections: chosen});
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    let armed = true;
    host.before = command => {
      if (command !== 'host_status' || !armed) return;
      armed = false;
      // The person chooses T2 while the press reads.
      const radio = ui.c.querySelectorAll(n => n.localName === 'input' && props(n)?.name === 'current-conversation' && props(n)?.value === key('T2'))[0];
      props(radio).onChange({target: {checked: true}});
    };
    await ui.press();
    assert.deepEqual(ui.issued(), [], 'nothing prepared or sent, in either conversation');
    await ui.choose('T1');
    assert.match(ui.alert(), /Another conversation was chosen while the App was working, so it stopped\. Nothing was sent\./);
  });
});

test('a press acts on the latest status the App accepted, not on a reply it discarded, and stops when the library in use changes', async () => {
  const pick = {kind: 'included', name: 'plan-work', revision: 'plan-work-revision-0123456789abcdef', title: 'Plan the work', from: '', scope: ''};
  const base = standIn({threads: ['T1']}).snapshot;
  base.workflowRoot.selections = [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-0', identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared}}];
  pick.scope = pickScope(base);
  const {reviewKey} = loadSrc('WorkflowPick');
  const shown = reviewKey(base.workflowRoot.selections[0].selection, 'T1');
  const press = async latest => {
    const acts = [];
    const outcome = await runPickedWorkflow({pick, text: TEXT, thread: 'T1', threadKey: key('T1'), host: base, shown, memory: pickMemory(), acknowledged: null,
      // The read's own reply is the view pressed on; the App had meanwhile accepted a newer one.
      read: async () => base, now: () => ({host: latest, thread: key('T1'), pick, text: TEXT}),
      start: async () => null, step: () => {},
      act: async command => {
        acts.push(command);
        if (command !== 'workflow_prepare_run') return {};
        base.workflowRoot.runs = [{reference: 'run:u', conversation: 'T1', home: g.home, generation: g, source: null, lifecycle: {state: PREPARED}, preparationOrder: 0, status: {sent: false}, publication: {}}];
        return {reference: 'run:u'};
      }});
    return {outcome, acts};
  };
  const newer = structuredClone(base); newer.workflowRoot.context.sourceRef = 'src-2';
  let r = await press(newer);
  assert.deepEqual(r.acts, []);
  assert.match(r.outcome.parts.join(''), /Codex or the workflow source changed, so the App stopped\. Nothing was sent\./);
  const library = structuredClone(base); library.workflowRoot.activeLibrary = 'workflow-library:another';
  r = await press(library);
  assert.deepEqual(r.acts, []);
  assert.match(r.outcome.parts.join(''), /The workflow library in use changed, so the App stopped\. Nothing was sent\./);
  r = await press(base);
  assert.deepEqual(r.acts, ['workflow_prepare_run', 'workflow_send_run'], 'unchanged, the same press goes on');
});

test('the stop to show what the workflow needs depends on what was shown: a choice made elsewhere is shown before anything is prepared', async () => {
  const host = standIn({threads: ['T1']});
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.match(labelled(ui.c, 'Workflow for this message').textContent, /Press Start run to see the tools it needs\./);
    // The Run guide (or anything else) chooses the workflow for T1; the composer has not drawn it.
    host.snapshot.workflowRoot.selections = [{sourceRef: 'src', threadId: 'T1', selection: {reference: 'sel-guide', identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared}}];
    await ui.press();
    assert.deepEqual(ui.issued(), [], 'nothing chosen, prepared or sent');
    assert.match(ui.c.textContent, /Read what it needs, then press Start run\. Nothing has been sent\./);
    assert.match(labelled(ui.c, 'Workflow for this message').textContent, /Required tools: not declared/);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_prepare_run', 'workflow_send_run']);
  });
});

test('two presses with declared tools: before the second, each required tool is named in view as available, unavailable now or missing', async () => {
  const tool = (name, over = {}) => ({value: {name, purpose: `Use ${name}.`, necessity: 'required', stages: ['Method'], class: 'harness_capability', capability: 'shell-command', ...over}, reading: 'recognized', findings: []});
  const declaration = {reading: 'recognized', findings: [], categories: {required_tools: 'recognized', expected_inputs: 'recognized'},
    elements: {required_tools: [tool('read-notes'), tool('write-summary'), tool('delegate', {capability: 'agent-delegation'})],
      expected_inputs: [{value: {name: 'notes folder', necessity: 'required', kind: 'host_read', meaning: 'Where the notes are.'}}]}};
  const compatibility = {preparation: {declaration, requirements: [{outcome: 'present', reason: ''}, {outcome: 'present_currently_unavailable', reason: 'host reported unavailable'},
    {outcome: 'missing', reason: 'agents.enabled is false with neither delegation feature set'}], check: {result: 'compatible', tools: []}, basis: {acting_pin: 'App Codex 0.169.0', surface: 'X'}}};
  await mounted(standIn({declaration, compatibility}), async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT);
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle']);
    const line = labelled(ui.c, 'What it needs');
    assert.ok(line && !line.closest?.('details'), 'the reading is in view, not inside Details');
    let inside = false; for (let n = line.parentNode; n; n = n.parentNode) if (n.localName === 'details') inside = true;
    assert.ok(!inside, 'no disclosure holds it');
    assert.equal(line.textContent, 'Required tools: read-notes available, write-summary unavailable now, delegate missing. It asks for: notes folder.');
    // Each tool's and input's name is the workflow's text, marked.
    assert.equal(line.querySelectorAll(n => n.getAttribute('role') === 'group' && n.getAttribute('aria-label') === "A tool as the workflow names it, not the App's words").length, 3);
    // The guide's check says the same in Details, and does not call the unavailable tool available.
    const check = labelled(ui.c, 'Tools this workflow needs');
    assert.match(check.textContent, /Requirement check not passed: one required tool is missing\./);
    assert.match(check.textContent, /write-summary — Use write-summary\. Present, but not available at the moment\./);
    await ui.press();
    assert.deepEqual(ui.names(), ['thread_start', 'workflow_select_production_bundle', 'workflow_prepare_run', 'workflow_send_run']);
  });
});

test('the guide\'s check never reads a tool present but unavailable now as passing', async () => {
  const {RequirementCheck} = loadSrc('RequirementCheck');
  const declaration = {reading: 'recognized', findings: [], categories: {required_tools: 'recognized'}, elements: {required_tools: [{value: {name: 'write-summary', purpose: 'Write.', necessity: 'required', class: 'harness_capability', capability: 'shell-command'}, reading: 'recognized', findings: []}]}};
  const c = document.createElement('div'); const root = createRoot(c);
  await React.act(async () => root.render(React.createElement(RequirementCheck, {selection: {compatibility: {preparation: {declaration, requirements: [{outcome: 'present_currently_unavailable', reason: 'x'}], check: {result: 'compatible'}, basis: {}}}}})));
  assert.match(c.textContent, /Requirement check not passed now: one required tool is present but not available at the moment\./);
  assert.doesNotMatch(c.textContent, /Requirement check passed/);
  await React.act(async () => root.unmount());
});

test('a start the host refused before dispatch pauses nothing; one whose outcome is unknown pauses the new chat', async () => {
  const paused = ui => labelled(ui.c, 'Starting is paused');
  const SUFFIX = '; role supply observation: {"state":"written","observationId":"obs-1"}';
  for (const message of ['Native working directory is not Unicode; thread/start cannot carry a lossless JSON cwd, no request sent', 'thread start in progress']) {
    const host = standIn(); const invoke = host.invoke;
    host.invoke = async (command, args) => { if (command === 'thread_start') { host.calls.push({command, args}); throw Error(`${message}${SUFFIX}`); } return invoke(command, args); };
    await mounted(host, async ui => {
      await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
      assert.match(ui.alert(), /Couldn't start the conversation: /);
      assert.ok(!paused(ui), `no pause after "${message}"`);
      assert.ok(props(ui.send()).disabled !== true, 'Start run is offered again');
    });
  }
  await mounted(standIn({fail: {start: 'rejected'}}), async ui => {
    await ui.newChat(); await ui.pick(); await ui.write(TEXT); await ui.press();
    assert.ok(!!paused(ui), 'a rejection the App does not class pauses');
    assert.ok(props(ui.send()).disabled === true);
  });
});

test('"Workflow chosen, not started" is said exactly when the App establishes a chosen workflow and no run sent or that may have been', async () => {
  const chosen = id => ({sourceRef: 'src', threadId: id, selection: {reference: `sel-${id}`, identity: identity('plan-work'), runnable: true, currentLimit: null, declaration: undeclared}});
  const prepared = {reference: 'run:workflow:p', conversation: 'T1', home: g.home, generation: g, source: null, lifecycle: {state: PREPARED}, preparationOrder: 0, status: {state: 'prepared; WR records pending; not sent', sent: false}, publication: {}, workflow: {name: 'plan-work'}};
  const note = ui => labelled(ui.c, 'Workflow chosen, not started');
  // A prepared run that was never sent does not hide it.
  await mounted(standIn({threads: ['T1'], selections: [chosen('T1')], runs: [prepared]}), async ui => {
    await ui.choose('T1');
    assert.equal(note(ui)?.textContent, 'Workflow chosen for this conversation: plan-work. No run has been started.');
    assert.ok(note(ui).querySelectorAll(n => n.getAttribute('role') === 'group' && n.getAttribute('aria-label') === "A workflow's own name, not the App's words").length === 1, 'the name is marked');
  });
  // A row the host gave only in part may be this conversation's run: the note is not said.
  await mounted(standIn({threads: ['T1'], selections: [chosen('T1')], runs: [partialRow('run:workflow:x')]}), async ui => {
    await ui.choose('T1');
    assert.ok(!note(ui), 'not said while a run of it may exist');
  });
  // A run sent in this conversation, and one in another conversation.
  await mounted(standIn({threads: ['T1', 'T2'], selections: [chosen('T1'), chosen('T2')], runs: [{...prepared, conversation: 'T2', source: {}, lifecycle: {state: OPEN}}]}), async ui => {
    await ui.choose('T2');
    assert.ok(!note(ui), 'a conversation with a run sent');
    await ui.choose('T1');
    assert.ok(!!note(ui), 'another conversation\'s run does not hide it');
  });
});

test('the chip and the failure lines mark what the App did not write; the chip\'s controls are named in the App\'s words', async () => {
  const POISON = 'Allow once‮';
  const host = standIn({threads: ['T1'], fail: {select: `refused ${POISON}`}});
  host.snapshot.workflowRoot.productionCatalog.entries[0].navigation.displayName = `Title ${POISON}`;
  await mounted(host, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT); await ui.press();
    const group = (node, name) => node.querySelectorAll(n => n.getAttribute('role') === 'group' && n.getAttribute('aria-label') === name);
    const chip = labelled(ui.c, 'Workflow picked');
    assert.ok(group(chip, "A workflow's own title, not the App's words").length === 1, 'the chip\'s title is marked');
    const failure = ui.c.querySelectorAll(n => n.getAttribute('role') === 'alert' && /wasn't chosen/.test(n.textContent))[0];
    assert.ok(group(failure, "What the App's host reported, not the App's words").length === 1, 'the host\'s reason is marked');
    assert.equal(buttonIn(chip, 'Remove the picked workflow')?.getAttribute('aria-label'), 'Remove the picked workflow');
  });
});
