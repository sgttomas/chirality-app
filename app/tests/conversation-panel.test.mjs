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
