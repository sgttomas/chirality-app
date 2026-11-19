import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
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
const entry = name => ({name, revision: `${name}-revision-0123456789abcdef`, origin: 'bundled', sourceRoot: ROOT, revisionMethod: METHOD, identity: identity(name), runnable: true, runLimit: null,
  description: `Invented description of ${name}.`, roles: ['HELP_HUMAN'], navigation: {category: 'core', tier: 'primary', order: 1, displayName: 'Plan the work'}, libraryPathsNamed: []});
const registered = {name: 'site-check', sequence: 2, revision: 'site-check-2-rev-0123456789abcdef', label: 'registered — approved in this App session (native A15)', evidence: 'in-process A15', selectable: true, reconfirm: false};
const library = {reference: LIB, root: {encoding: 'unix_bytes', bytes: [...new TextEncoder().encode(PROJECT)]}, origin: 'project', sourceRoot: PROJECT, registered: [registered],
  entryListing: {state: 'not observed', entries: [], limits: []}};
const thread = id => ({generation: g, threadId: id, appRole: {standing: 'app-observed', role: 'HELP_HUMAN'}, roleRelation: {kind: 'start'}, futureGuidanceNotices: [], status: {type: 'idle'}});
const OPEN = 'open (live); only the person\'s explicit end ends it';
const PREPARED = 'prepared; not a run until its start turn is observed';

/** The stand-in host. `fail` names a step to refuse (with the host's message) or to leave without its effect. */
function standIn({threads = [], selections = [], runs = [], projectLibraryAvailable = true, fail = {}} = {}) {
  const state = {calls: [], prepared: 0, sel: 0, snapshot: null, fail};
  const root = {context: {sourceRef: 'src', generation: g, historyEpoch: 3}, projectLibraryAvailable, productionCatalog: {standing: 'invented', source: {tag: 'library-v9.9.9'}, entries: [entry('plan-work')]},
    activeLibrary: LIB, libraries: [library], selections, runs, reviews: [], offers: [], reopened: {runs: []}};
  state.snapshot = {state: 'ready', generation: g, homeRouting: {activeModeHomeClass: 'account'}, roleLimits: {account: {roles: []}},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'fixture role', default_for_new_chat: true}]},
    threads: threads.map(thread), workflowRoot: root};
  const select = (threadId, id) => { state.sel += 1; root.selections = [...root.selections.filter(row => row.threadId !== threadId),
    {sourceRef: 'src', threadId, selection: {reference: `sel-${state.sel}`, identity: id, runnable: true, runLimit: null, currentLimit: null, newerRevision: null, assurance: null, declaration: undeclared}}]; };
  const run = ref => root.runs.find(row => row.reference === ref);
  state.invoke = async (command, args) => {
    const fail = state.fail;
    state.calls.push({command, args: structuredClone(args)});
    if (command === 'host_status') { if (fail.status && state.calls.some(c => c.command === fail.status.after)) throw Error('status unavailable'); return structuredClone(state.snapshot); }
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
      if (fail.select) throw Error(fail.select);
      select(args.context.threadId, identity(args.name)); return {choiceChat: {sourceRef: 'src', threadId: args.context.threadId}};
    }
    if (command === 'workflow_select_listed') {
      if (fail.select) throw Error(fail.select);
      select(args.context.threadId, identity(args.name, {origin: 'project', source_root: PROJECT, revision: args.revision})); return {choiceChat: {sourceRef: 'src', threadId: args.context.threadId}};
    }
    if (command === 'workflow_prepare_run') {
      if (fail.prepare) throw Error(fail.prepare);
      state.prepared += 1;
      const reference = `run:workflow:${state.prepared}`;
      root.runs = [...root.runs, {reference, conversation: args.threadId, home: g.home, generation: g, source: null, lifecycle: {state: PREPARED}, preparationOrder: root.runs.length,
        status: {state: 'prepared; WR records pending; not sent', sent: false}, publication: fail.admission ? {admissionRefusal: fail.admission} : {state: 'pending; not recorded'}, workflow: {name: 'plan-work'}}];
      return {reference, state: 'original registered selection prepared; WR records pending; not sent'};
    }
    if (command === 'conversation_send_text') return {result: {}};
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
  const idle = installIdleNativeWaiting(host.invoke);
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

test('picking a workflow lands in the message box; removing the pick moves nothing', async () => {
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
      const remove = ui.composer().querySelectorAll(n => n.localName === 'button' && /^Remove /.test(n.getAttribute('aria-label') ?? ''))[0];
      assert.ok(!!remove, 'the chip offers its removal');
      await React.act(async () => props(remove).onClick());
      assert.ok(focused.length === 0 && scrolled.length === 0, 'removing the pick moves neither focus nor the view');
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
    assert.equal(labelled(ui.c, 'Workflow chosen, not started')?.textContent, 'plan-work is chosen for this conversation. No run has been started.');
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
    assert.match(ui.alert(), /Plan the work can't run: the bundled copy differs from the release\. Nothing was sent\./);
    await ui.press();
    assert.deepEqual(ui.names(), ['workflow_select_production_bundle'], 'a second press prepares nothing either');
  });
});

test('an open conversation\'s run that is still open stops Start run, as the Run guide does', async () => {
  const open = [{reference: 'run:workflow:0', conversation: 'T1', home: g.home, generation: g, source: {}, lifecycle: {state: OPEN}, preparationOrder: 0, status: {}, workflow: {name: 'plan-work'}}];
  await mounted(standIn({threads: ['T1'], runs: open}), async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    assert.equal(!!props(ui.send()).disabled, true);
    assert.match(ui.c.textContent, /A workflow run is still open in this conversation\. End it under Run a workflow before starting another\./);
    assert.deepEqual(ui.issued(), []);
  });
  // A run opened after the view was drawn: the press reads the host first and stops before choosing anything.
  const later = standIn({threads: ['T1']});
  await mounted(later, async ui => {
    await ui.choose('T1'); await ui.pick(); await ui.write(TEXT);
    later.snapshot.workflowRoot.runs = open;
    await ui.press();
    assert.deepEqual(ui.issued(), []);
    assert.match(ui.alert(), /A workflow run is still open in this conversation\. End it under Run a workflow before starting another\. Nothing was sent\./);
    assert.equal(props(chatInput(ui.c)).value, TEXT);
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
    assert.match(ui.alert(), /Codex or the workflow source changed, so the App stopped\. Nothing was sent\./);
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
    await React.act(async () => props(tab('right-tab-history')).onClick?.());
    assert.ok(labelled(ui.c, 'Workflow for this message'), 'the pick is kept while another tab is shown');
    // Remove at the chip: the composer is the ordinary one, and its Send issues the ordinary send only.
    await React.act(async () => props(buttonIn(ui.composer(), 'Remove plan-work')).onClick());
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
