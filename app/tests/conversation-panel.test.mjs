import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The conversation section is mounted with react-dom/client on a minimal
// in-memory document, so the test sees what React actually leaves mounted
// when the person moves between conversations (native witness 2026-10-10 D-1:
// one more role header per conversation viewed).
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App, ConversationPanel} = loadSrc('App');

const g = {appSession: 's', home: 'h', spawnCounter: 1};
const thread = (threadId, role, relation = {kind: 'start'}) => ({generation: g, threadId, appRole: {standing: 'app-observed', role, supply_ref: `sup:${threadId}`}, roleRelation: relation, futureGuidanceNotices: []});
const host = {state: 'ready', generation: g, roleLimits: {account: {roles: []}},
  threads: [thread('thread-a', null), thread('thread-b', null), thread('thread-c', 'HELPS_HUMANS', {kind: 'continued-from', from: {sourceThread: 'thread-b', sourceRole: {standing: 'app-observed', role: null}}})]};
const key = threadId => JSON.stringify([g, threadId]);
const noop = async () => {};

test('exactly one role header, for the selected conversation, as the person moves between conversations', async () => {
  const errors = [];
  const consoleError = console.error;
  console.error = (...args) => { errors.push(args.map(String).join(' ')); };
  try {
    const container = document.createElement('div');
    document.body.appendChild(container);
    const root = createRoot(container);
    const show = threadKey => React.act(() => root.render(React.createElement(ConversationPanel, {host, threadKey, setThreadKey: () => {}, answer: noop, runAct: noop, send: noop, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false})));
    const headers = () => container.querySelectorAll(e => e.getAttribute('aria-label') === 'Conversation role');
    await show('');
    assert.equal(headers().length, 0, 'no conversation selected, no header');
    // The witness order: a conversation, the resumed one, then the Continue as conversation, and back.
    for (const [threadId, line] of [['thread-a', 'No role'], ['thread-b', 'No role'], ['thread-c', 'HELPS_HUMANS'], ['thread-a', 'No role']]) {
      await show(key(threadId));
      const shown = headers();
      assert.equal(shown.length, 1, `one header after selecting ${threadId}`);
      assert.ok(shown[0].textContent.startsWith(`Role: ${line}.`), `the header is ${threadId}'s`);
      assert.equal(shown[0].textContent.includes('Continues conversation thread-b'), threadId === 'thread-c');
    }
    await React.act(() => root.unmount());
    assert.equal(headers().length, 0);
  } finally {
    console.error = consoleError;
  }
  assert.deepEqual(errors.filter(e => e.includes('same key')), [], 'no two children of the section share a key');
});

// Exercise the ordinary Start button through App's native invoke boundary,
// including the refresh that supplies the newly admitted native thread.
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container, tag) => container.querySelectorAll(element => element.localName === tag);
const button = (container, text) => elements(container, 'button').find(element => element.textContent === text);
const labelled = (container, tag, text) => elements(container, tag).find(element => element.parentNode.textContent.startsWith(text));
const change = (element, value) => React.act(() => props(element).onChange({target: {value}}));

async function ordinaryStartCase({initialThread = false, startGeneration = g, outcome = 'success'}) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const calls = [];
  let snapshot = {...host, threads: initialThread ? [thread('existing', null)] : [],
    homeRouting: {activeModeHomeClass: 'account'},
    roleSet: {available: true, defaultRole: 'HELP_HUMAN', roles: [{name: 'HELP_HUMAN', meaning: 'Alignment', default_for_new_chat: true}]}};
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command !== 'thread_start') throw Error(`Unexpected native command: ${command}`);
    if (outcome === 'refused') throw Error('Native start refused before send');
    if (outcome === 'failed') throw Error('Native start result unknown; no automatic retry');
    if (outcome === 'missing-id') return {startGeneration, result: {thread: {}}};
    if (outcome === 'missing-generation') return {result: {thread: {id: 'created'}}};
    const created = {...thread('created', 'HELP_HUMAN'), generation: startGeneration, model: args.model, modelProvider: args.modelProvider};
    snapshot = {...snapshot, generation: startGeneration, threads: [...snapshot.threads, created]};
    return {id: 42, startGeneration, result: {thread: {id: created.threadId}}, roleSupplyRecord: {state: 'recorded'}};
  }};
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    const selectedKey = () => props(elements(conversation(), 'select')[0]).value;
    if (initialThread) await change(elements(conversation(), 'select')[0], key('existing'));
    await change(labelled(container, 'input', 'Model '), 'chosen-model');
    await change(labelled(container, 'input', 'Configured Codex provider '), 'openai');
    await change(labelled(container, 'select', 'Access entry '), 'chatgpt-account');
    const draft = 'Unsent person text é / 家';
    await change(elements(conversation(), 'textarea')[0], draft);
    const start = button(container, 'Start thread');
    assert.equal(props(start).disabled, false);
    await React.act(async () => {await props(start).onClick();});
    assert.deepEqual(calls.filter(call => call.command === 'thread_start'), [{command: 'thread_start', args: {
      model: 'chosen-model', modelProvider: 'openai', entryId: 'chatgpt-account', modeHomeClass: 'account', role: 'HELP_HUMAN', preselected: true,
    }}], 'one person-initiated start with the chosen configuration');
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'thread_start'].includes(call.command)), 'Start never sends composer text or retries');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft, 'unsent composer retained');
    if (outcome === 'success') {
      assert.equal(selectedKey(), JSON.stringify([startGeneration, 'created']), 'opens the native ID in the returned start generation');
      assert.equal(props(button(conversation(), 'Send text')).disabled, false, 'the displayed new conversation can receive an explicit send');
      const headers = conversation().querySelectorAll(element => element.getAttribute('aria-label') === 'Conversation role');
      assert.equal(headers.length, 1);
      assert.ok(headers[0].textContent.startsWith('Role: HELP_HUMAN.'), 'shows the new conversation');
    } else {
      assert.equal(selectedKey(), initialThread ? key('existing') : '', 'unsuccessful start keeps the selection');
      assert.equal(props(button(conversation(), 'Send text')).disabled, !initialThread);
      if (outcome === 'refused' || outcome === 'failed') assert.ok(container.textContent.includes('thread_start: Error: Native start'));
    }
  } finally {
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    window.__TAURI_INTERNALS__ = previous;
  }
}

test('ordinary Start opens the admitted conversation without sending its composer', async () => {
  await ordinaryStartCase({});
  await ordinaryStartCase({initialThread: true});
  // The host's actual start generation can differ from the pre-click snapshot.
  await ordinaryStartCase({initialThread: true, startGeneration: {appSession: 's', home: 'other-home', spawnCounter: 2}});
});

test('refused, failed and identity-incomplete Start preserve selection and composer', async () => {
  for (const outcome of ['refused', 'failed', 'missing-id', 'missing-generation']) {
    await ordinaryStartCase({outcome});
    await ordinaryStartCase({initialThread: true, outcome});
  }
});

async function ordinaryContinueCase({initialThread = false, outcome = 'success', source = g}) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  const calls = [];
  const unknownRole = {standing: 'unknown', reason: 'original App role not established in this App process'};
  const metadata = {thread: {id: 'stored', status: {type: 'notLoaded'}, agentRole: 'HELP_HUMAN'}};
  const query = {factory_id: 1, query_id: 2, home: source.home, generation: source, method: 'thread/resume', params: {threadId: 'stored'}};
  const existing = {...thread('existing', null), generation: source};
  let continueResponded = false;
  const interleave = outcome === 'delayed-source-choice' || outcome === 'delayed-chat-choice';
  let releaseDecision, decisionHeld, pendingContinue;
  const heldDecision = new Promise(resolve => {releaseDecision = resolve;});
  const reachedDecision = new Promise(resolve => {decisionHeld = resolve;});
  let holdNextDecision = interleave;
  let expectedKey = outcome === 'success' ? JSON.stringify([source, 'stored']) : initialThread ? JSON.stringify([source, 'existing']) : '';
  let snapshot = {...host, generation: source, threads: interleave ? [existing, {...thread('other-current', null), generation: source}] : initialThread ? [existing] : [],
    homeRouting: {activeModeHomeClass: 'account', entries: [{modeHomeClass: 'account'}, {modeHomeClass: 'api-key'}]},
    nativeHistory: {state: 'history-receiving', home: source.home, generation: source, selectionEpoch: 0, threads: [{native: metadata.thread}], dispatches: outcome === 'old-admission' ? [{requestRef: 'req:resume'}] : []}};
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke: async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') {
      if (outcome === 'refresh-failed' && continueResponded) throw Error('Current source read failed');
      return snapshot;
    }
    if (command === 'decision_view') {
      if (continueResponded && holdNextDecision) {holdNextDecision = false; decisionHeld(); return heldDecision;}
      return {rows: []};
    }
    if (command === 'select_home') {
      const nextSource = {...source, home: 'chosen-other-home', spawnCounter: 2};
      snapshot = {...snapshot, generation: nextSource, homeRouting: {...snapshot.homeRouting, activeModeHomeClass: args.modeHomeClass},
        threads: [{...thread('other-current', null), generation: nextSource}],
        nativeHistory: {...snapshot.nativeHistory, generation: nextSource, home: nextSource.home, selectionEpoch: 0, selected: null, dispatches: []}};
      return {state: 'selected'};
    }
    if (command === 'native_confirmation_content') return [];
    if (command === 'history_select') {
      snapshot = {...snapshot, nativeHistory: {...snapshot.nativeHistory, selectionEpoch: 1, selected: {threadId: args.threadId, state: 'indexed-read-only', appRole: unknownRole}}};
      return snapshot.nativeHistory;
    }
    if (command !== 'history_action') throw Error(`Unexpected native command: ${command}`);
    if (args.action === 'metadata') {
      snapshot = {...snapshot, nativeHistory: {...snapshot.nativeHistory, selected: {...snapshot.nativeHistory.selected, metadata}}};
      return snapshot.nativeHistory;
    }
    assert.equal(args.action, 'continue');
    if (outcome === 'refused' || outcome === 'failed') throw Error(`Native resume ${outcome}`);
    const admitted = {generation: source, threadId: 'stored', status: {type: 'idle'}, appRole: unknownRole, nativeResumeObserved: true, resumeRequestRef: 'req:resume'};
    const dispatch = {generation: source, home: source.home, requestRef: 'req:resume', writeResult: 'written', outcome: 'response-observed-result', sourceCurrent: true, localQuery: query, activeAdmission: admitted};
    const result = {...snapshot.nativeHistory, selected: {...snapshot.nativeHistory.selected, state: 'resume-response-observed', resumeEligibilityCurrent: true,
      resume: {thread: {...metadata.thread, status: {type: 'idle'}}}, streamResolutions: {'thread-state': {outcome: 'native-result-observed', query}}}, dispatches: [dispatch]};
    if (outcome === 'read-only') result.selected.state = 'indexed-read-only';
    if (outcome === 'ineligible') result.selected.resumeEligibilityCurrent = false;
    if (outcome === 'not-admitted') delete dispatch.activeAdmission;
    if (outcome === 'pending') dispatch.outcome = 'pending';
    if (outcome === 'stale-dispatch') dispatch.sourceCurrent = false;
    if (outcome === 'missing-id') delete admitted.threadId;
    if (outcome === 'missing-generation') delete admitted.generation;
    if (outcome === 'wrong-id') admitted.threadId = 'other';
    if (outcome === 'wrong-query') dispatch.localQuery = {...query, query_id: 99};
    snapshot = {...snapshot, nativeHistory: result, threads: [...snapshot.threads, {...admitted, generation: source, threadId: 'stored'}]};
    if (outcome === 'not-ready') snapshot = {...snapshot, state: 'stopped'};
    if (outcome === 'no-current-thread') snapshot = {...snapshot, threads: initialThread ? [existing] : []};
    continueResponded = true;
    if (outcome === 'source-changed') snapshot = {...snapshot, generation: {...source, spawnCounter: 9}};
    if (outcome === 'selection-changed') snapshot = {...snapshot, nativeHistory: {...result, selectionEpoch: 2}};
    if (outcome === 'query-superseded') snapshot = {...snapshot, nativeHistory: {...result, selected: {...result.selected, streamResolutions: {'thread-state': {outcome: 'native-result-observed', query: {...query, query_id: 99}}}}}};
    return result;
  }};
  try {
    await React.act(async () => {root.render(React.createElement(App));});
    const conversation = () => container.querySelectorAll(element => element.getAttribute('id') === 'conversation')[0];
    const selectedKey = () => props(elements(conversation(), 'select')[0]).value;
    const priorKey = JSON.stringify([source, 'existing']);
    if (initialThread) await change(elements(conversation(), 'select')[0], priorKey);
    const draft = 'Unsent continuation text é / 家';
    await change(elements(conversation(), 'textarea')[0], draft);
    await React.act(async () => {await props(labelled(container, 'select', 'Stored conversation ')).onChange({target: {value: 'stored'}});});
    await React.act(async () => {await props(button(container, 'Read metadata')).onClick();});
    assert.equal(selectedKey(), initialThread ? priorKey : '', 'index and metadata reads do not open an operational chat');
    const continueButton = button(container, 'Continue selected conversation');
    assert.equal(props(continueButton).disabled, false);
    if (interleave) {
      await React.act(async () => {pendingContinue = props(continueButton).onClick(); await reachedDecision;});
      // The old host_status has rendered, but its decision_view is still held.
      if (outcome === 'delayed-source-choice') {
        await React.act(async () => {await props(button(container, 'Use api-key home')).onClick();});
      }
      expectedKey = JSON.stringify([snapshot.generation, 'other-current']);
      await change(elements(conversation(), 'select')[0], expectedKey);
      assert.equal(selectedKey(), expectedKey, 'the person has chosen the newer current chat');
      await React.act(async () => {releaseDecision({rows: []}); await pendingContinue;});
    } else {
      await React.act(async () => {await props(continueButton).onClick();});
    }
    assert.deepEqual(calls.filter(call => call.command === 'history_action').map(call => call.args), ['metadata', 'continue'].map(action => ({generation: source, selectionEpoch: 1, action, cursor: null, direction: 'desc', reference: null})), 'one explicit Continue and no retry');
    assert.ok(calls.every(call => ['host_status', 'decision_view', 'native_confirmation_content', 'history_select', 'history_action', 'select_home'].includes(call.command)), 'Continue never sends text or changes role');
    assert.equal(props(elements(conversation(), 'textarea')[0]).value, draft);
    assert.equal(selectedKey(), expectedKey, 'a delayed Continue cannot replace a newer source or chat choice');
    if (outcome === 'success') {
      assert.equal(props(button(conversation(), 'Send text')).disabled, false);
      assert.ok(conversation().textContent.includes('Role not established in this App process'), 'cold role stays unknown despite native agentRole');
    }
  } finally {
    if (pendingContinue) await React.act(async () => {releaseDecision({rows: []}); await pendingContinue;});
    await React.act(() => root.unmount());
    document.body.removeChild(container);
    window.__TAURI_INTERNALS__ = previous;
  }
}

test('explicit Continue opens the newly admitted current conversation and retains the cold role limit', async () => {
  await ordinaryContinueCase({});
  await ordinaryContinueCase({initialThread: true, source: {...g, home: 'another-home', spawnCounter: 2}});
});

test('Continue with no matching new current admission preserves selection and composer', async () => {
  for (const outcome of ['read-only', 'ineligible', 'not-admitted', 'refused', 'failed', 'pending', 'stale-dispatch', 'missing-id', 'missing-generation', 'wrong-id', 'wrong-query', 'old-admission', 'source-changed', 'selection-changed', 'query-superseded', 'not-ready', 'no-current-thread', 'refresh-failed']) {
    await ordinaryContinueCase({initialThread: true, outcome});
  }
});


test('a Continue refresh awaiting decision_view cannot overwrite a newer source or chat choice', async () => {
  await ordinaryContinueCase({initialThread: true, outcome: 'delayed-source-choice'});
  await ordinaryContinueCase({initialThread: true, outcome: 'delayed-chat-choice'});
});
