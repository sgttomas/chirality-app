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
const {ConversationPanel} = loadSrc('App');

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
