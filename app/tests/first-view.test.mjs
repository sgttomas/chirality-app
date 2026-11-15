import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// The first view at launch, and the move after a sign-in, through the mounted App on constructed host
// snapshots only: no real account, sign-in or model. The host's own account read at ready is the host's
// (access_provider_tests.rs codex_ready_reads_the_account_once_with_empty_params_as_the_apps_own_read_and_again_after_a_restart);
// here the readings it records arrive in the status the App polls.
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');

const g = {appSession: 's', home: 'h', spawnCounter: 1};
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container, tag) => container.querySelectorAll(element => element.localName === tag);
const byId = (c, id) => c.querySelectorAll(e => e.getAttribute('id') === id)[0];
const disclosureOpen = e => e.open ?? e.hasAttribute('open');
const visible = e => { for (let n = e; n; n = n.parentNode) if (props(n)?.hidden) return false; return true; };
const currentView = c => elements(c, 'a').find(a => props(a)?.['aria-current'] === 'page')?.textContent;

const base = (over = {}) => ({state: 'ready', generationClosed: false, generation: g, threads: [], roleLimits: {account: {roles: []}},
  homeRouting: {activeModeHomeClass: 'account', entries: [{modeHomeClass: 'account'}]}, serverRequests: [], ...over});
// One account read as the host records it: the App's own read at ready, answered (account, or null), or still waiting.
const reading = (host, answer, {ref = 'read-1', outcome = 'response-observed-result', extra = {}} = {}) => {
  const answered = outcome === 'response-observed-result';
  const row = {source: {generation: host.generation, home: host.generation.home, requestIdentity: 1, requestRef: ref, sourceCurrent: true,
    attemptedFrame: {method: 'account/read', params: {}}, outcome, authResponseShapeValid: answered, lastClientObservation: {initiator: {kind: 'app-rule', name: 'app-at-ready'}}, ...extra},
    accountObservation: answered ? {state: answer === null ? 'native account null observed' : 'native account type observed', account: answer, identityVerified: false} : null};
  return {...host, homeAccess: {modeHomeClass: 'account', observations: [row]},
    accountObservation: answered ? {generation: host.generation, home: host.generation.home, state: 'observed', nativeAccount: answer, identityVerified: false} : null};
};
const noAccount = (host = base(), o) => reading(host, null, o);
const signedIn = (host = base(), o) => reading(host, {type: 'chatgpt'}, o);
const underWay = (host = base()) => reading(host, undefined, {outcome: 'pending'});
const failed = (host = base()) => reading(host, undefined, {outcome: 'response-observed-error', extra: {lastClientObservation: {error: {code: -32603, message: 'invented'}}}});
// The stored conversations read for this Codex session to the end, listing none.
const historyEmpty = host => ({...host, nativeHistory: {state: 'history-receiving', home: g.home, generation: g, selectionEpoch: 0, threads: [], listCursor: {state: 'exhausted'}, listError: null, dispatches: []}});
// The App's own history list read when Codex became ready, as the host publishes it beside the list it fills
// (runtime_session.rs read_history_at_ready): under way with nothing received yet, read to its end, or stopped short
// with the list as far as it got (a cursor left).
const historyAtReady = (host, state, list = {}) => ({...host, nativeHistory: {state: 'history-receiving', home: g.home, generation: g, selectionEpoch: 0, threads: [],
  listCursor: {state: state === 'read-to-end' ? 'exhausted' : state === 'stopped' ? 'available' : 'not-reported'}, listError: null, dispatches: [], ...list,
  readAtReady: {generation: host.generation, state}}});
// A request from a conversation recovered after the relaunch (not loaded in this session), waiting on the person.
const recoveredRequest = host => ({...host, serverRequests: [{recordKind: 'server-request-entry', generation: g, requestIdentity: 'q1', method: 'item/tool/requestUserInput',
  classification: 'known-answerable', originClass: 'person-input', state: 'outstanding', replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'},
  nativeParameters: {threadId: 'recovered-thread', turnId: 'u1', itemId: 'i1', isBlocking: false, questions: [{id: 'q', header: 'Scope', question: 'Which folder?', isOther: false, isSecret: false, options: [{label: 'reports/', description: 'Reports'}]}]}}]});
const completed = (host, ref = 'login-1') => ({...host, homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, observationRef: ref, phase: 'CompletedSuccess', mode: 'Browser', actualWriteObserved: true}}});

async function mountedApp(initial, check) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container), calls = [];
  // A reveal finds its target by id, as in the window.
  const previousGetById = document.getElementById;
  document.getElementById = id => container.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  let snapshot = initial;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_home_access') return snapshot.homeAccess;
    if (command === 'read_available_models') throw Error('no model list in this test');
    throw Error(`Unexpected command ${command}`);
  });
  const observe = async next => {
    snapshot = next; document.visibilityState = 'visible';
    await React.act(async () => { for (const {type, listener} of [...document.listeners]) if (type === 'visibilitychange') listener(); });
  };
  const navigate = async label => {
    const anchor = elements(container, 'a').find(e => e.textContent === label && visible(e)); assert.ok(anchor, label);
    const main = elements(container, 'main')[0]; await React.act(() => props(main).onClick({target: anchor, currentTarget: main}));
  };
  const type = async (id, value) => { const field = byId(container, id); assert.ok(field, id); await React.act(() => props(field).onChange({target: {value}})); };
  try { await React.act(async () => root.render(React.createElement(App))); await check({container, calls, observe, navigate, type}); }
  finally { const text = container.textContent; await React.act(() => root.unmount()); document.body.removeChild(container); idle.restore(text); document.getElementById = previousGetById; }
}

test('the first view at launch follows the launch account reading: no account, signed in with no conversation yet, otherwise Run a workflow', async () => {
  // No account: Settings & tools, with Connection and access open at the sign-in.
  await mountedApp(noAccount(), async ui => {
    assert.equal(currentView(ui.container), 'Settings & tools');
    assert.equal(disclosureOpen(byId(ui.container, 'workspace-connection')), true, 'Connection and access is open');
    assert.equal(byId(ui.container, 'workspace-sign-in')?.textContent, 'Sign in with your ChatGPT account (through Codex)…', 'at the sign-in');
    assert.deepEqual(ui.calls.filter(c => !['host_status', 'decision_view', 'native_confirmation_content'].includes(c.command)), [], 'moving reads, starts or signs in nothing');
  });
  // Signed in, and the stored conversations read to the end list none: Conversation, with New conversation open.
  await mountedApp(historyEmpty(signedIn()), async ui => {
    assert.equal(currentView(ui.container), 'Conversation');
    assert.equal(disclosureOpen(byId(ui.container, 'workspace-start')), true, 'New conversation is open');
  });
  // Otherwise Run a workflow stays: signed in with history not read (no conversation is not established), a conversation
  // in this session, the read under way, Codex didn't say, or Codex not running.
  for (const [name, host] of [['signed in, history not read', signedIn()], ['signed in, a conversation exists', historyEmpty(signedIn(base({threads: [{generation: g, threadId: 't'}]})))],
    ['under way', underWay()], ['failed read', failed()], ['not running', base({state: 'stopped'})]])
    await mountedApp(host, async ui => { assert.equal(currentView(ui.container), 'Run a workflow', name); });
});

test('while the launch read is under way the App stays, then moves once when the reading arrives; a failed read stays and decides', async () => {
  await mountedApp(underWay(), async ui => {
    assert.equal(currentView(ui.container), 'Run a workflow');
    assert.match(ui.container.textContent, /Checking whether you're signed in\. If a sign-in is kept, Codex checks it with OpenAI\./);
    await ui.observe(noAccount());
    assert.equal(currentView(ui.container), 'Settings & tools', 'moves when the reading arrives');
  });
  // A failed read is "didn't say", never "not signed in": the App stays, and that decides the launch.
  await mountedApp(failed(), async ui => {
    assert.equal(currentView(ui.container), 'Run a workflow');
    assert.match(ui.container.textContent, /It didn't say whether you're signed in\./);
    assert.doesNotMatch(ui.container.textContent, /You're not signed in/);
    await ui.observe(noAccount(base(), {ref: 'read-2'}));
    assert.equal(currentView(ui.container), 'Run a workflow', 'at most once: the launch was decided by the first reading');
  });
});

test('at most once per launch: after the move, a later reading moves nothing', async () => {
  // Signed in with history unread: the launch decides to stay. A later read of an empty history moves nothing.
  await mountedApp(signedIn(), async ui => {
    assert.equal(currentView(ui.container), 'Run a workflow');
    await ui.observe(historyEmpty(signedIn()));
    assert.equal(currentView(ui.container), 'Run a workflow');
  });
  // Moved once to the sign-in; after a restart, a fresh no-account reading moves nothing more.
  await mountedApp(noAccount(), async ui => {
    assert.equal(currentView(ui.container), 'Settings & tools');
    const next = {...g, spawnCounter: 2};
    await ui.observe(base({generation: next}));
    await ui.observe(noAccount(base({generation: next}), {ref: 'read-2'}));
    assert.equal(currentView(ui.container), 'Settings & tools');
    assert.equal(ui.calls.filter(c => c.command === 'read_home_access').length, 0, 'the renderer itself reads nothing');
  });
});

test('no move after the person navigates, over unsent text, or over a waiting request from a recovered conversation', async () => {
  await mountedApp(underWay(), async ui => {
    await ui.navigate('History');
    assert.equal(currentView(ui.container), 'History');
    await ui.observe(noAccount());
    assert.equal(currentView(ui.container), 'History', 'the person navigated: the App does not move them');
  });
  await mountedApp(underWay(), async ui => {
    await ui.type('ordinary-composer-text', 'A draft not yet sent');
    await ui.observe(noAccount());
    assert.equal(currentView(ui.container), 'Run a workflow', 'unsent text: no move');
    assert.equal(props(byId(ui.container, 'ordinary-composer-text')).value, 'A draft not yet sent', 'the draft is kept');
  });
  await mountedApp(recoveredRequest(underWay()), async ui => {
    await ui.observe(recoveredRequest(noAccount()));
    assert.equal(currentView(ui.container), 'Run a workflow', 'a request waits on the person: the App stays');
    await ui.observe(recoveredRequest(noAccount(base(), {ref: 'read-2'})));
    assert.equal(currentView(ui.container), 'Run a workflow', 'and does nothing else');
  });
});

test('a sign-in completed in this process and confirmed by the read after it opens a new conversation, even after navigation, never over unsent text', async () => {
  const signedInLine = /You're signed in\. Choose a model to start a conversation\./;
  await mountedApp(noAccount(), async ui => {
    assert.equal(currentView(ui.container), 'Settings & tools');
    await ui.navigate('History');
    // The completion is seen first; the account read made after it confirms the account.
    await ui.observe(completed(noAccount()));
    assert.equal(currentView(ui.container), 'History', 'no move before the read confirms an account');
    await ui.observe(completed(signedIn(base(), {ref: 'read-after-sign-in'})));
    assert.equal(currentView(ui.container), 'Conversation', 'navigation does not block the move signing in asks for');
    assert.equal(disclosureOpen(byId(ui.container, 'workspace-start')), true);
    assert.match(ui.container.textContent, signedInLine);
    // Once per completion.
    await ui.navigate('History');
    await ui.observe(completed(signedIn(base(), {ref: 'read-later'})));
    assert.equal(currentView(ui.container), 'History');
  });
  await mountedApp(noAccount(), async ui => {
    await ui.type('ordinary-composer-text', 'Unsent');
    await ui.observe(completed(noAccount()));
    await ui.observe(completed(signedIn(base(), {ref: 'read-after-sign-in'})));
    assert.equal(currentView(ui.container), 'Settings & tools', 'unsent text blocks the move');
    assert.doesNotMatch(ui.container.textContent, signedInLine);
  });
});

test('the workspace line carries the sign-in itself when Codex reports no account, except on Settings & tools while Connection and access is open and carries it: one sign-in button on a view, and never none', async () => {
  const SIGN_IN = 'Sign in with your ChatGPT account (through Codex)…';
  await mountedApp(noAccount(), async ui => {
    const status = () => ui.container.querySelectorAll(e => e.getAttribute('aria-label') === 'Workspace connection status')[0];
    assert.match(status().textContent, /Codex is running\. You're not signed in\./);
    assert.equal(currentView(ui.container), 'Settings & tools');
    assert.equal(elements(ui.container, 'button').filter(b => b.textContent === SIGN_IN).length, 1, 'one sign-in button: Connection and access');
    assert.equal(elements(status(), 'button').filter(b => b.textContent === SIGN_IN).length, 0, 'not repeated on the line here');
    // Collapsing Connection and access never leaves the view without a way to sign in: the line carries it again.
    await React.act(() => props(byId(ui.container, 'workspace-connection')).onToggle({currentTarget: {open: false}}));
    assert.ok(elements(status(), 'button').find(b => b.textContent === SIGN_IN), 'Connection and access closed: the sign-in is on the line');
    await React.act(() => props(byId(ui.container, 'workspace-connection')).onToggle({currentTarget: {open: true}}));
    assert.equal(elements(status(), 'button').filter(b => b.textContent === SIGN_IN).length, 0, 'opened again: one button, in the section');
    await ui.navigate('History');
    assert.ok(elements(status(), 'button').find(b => b.textContent === SIGN_IN), 'on another view the sign-in is on the line');
    assert.equal(elements(status(), 'a').length, 0, 'no link to a section that holds the button');
  });
});

test('Connection and access leads with the sign-in only when it is needed; signed in, it leads with the account and Sign out', async () => {
  const {HomeAccessPanel} = loadSrc('App');
  const {renderToStaticMarkup} = await import('react-dom/server');
  const plain = html => html.replace(/<[^>]+>/g, ' ').replace(/&#x27;/g, "'").replace(/&amp;/g, '&').replace(/\s+/g, ' ');
  const panel = host => renderToStaticMarkup(React.createElement(HomeAccessPanel, {host, resources: null, act: async () => {}, readAccount: async () => {}}));
  const SIGN_IN = 'Sign in with your ChatGPT account (through Codex)…';
  const before = html => html.split('<summary>Other sign-in options</summary>')[0];
  for (const [name, host, leads] of [['no account', noAccount(), true], ['not yet read', base(), true], ['didn\'t say', failed(), true],
    ['under way', underWay(), false], ['signed in', signedIn(), false]]) {
    const html = panel(host);
    assert.equal(before(html).includes(SIGN_IN), leads, `${name}: the primary sign-in`);
    assert.equal(before(html).includes('Sign in with your ChatGPT account to reach a model.'), leads, `${name}: the line that asks for it`);
    assert.ok(html.includes(SIGN_IN), `${name}: signing in stays available`);
  }
  const html = panel(signedIn());
  const text = plain(before(html));
  assert.ok(text.indexOf('Codex reports a ChatGPT account') < text.indexOf('Sign out of ChatGPT…'), 'the account, then Sign out');
  assert.match(plain(html.split('<summary>Other sign-in options</summary>')[1]), new RegExp(SIGN_IN.replace(/[()…]/g, '.')), 'signing in again is among the other options');
  // After a sign-in in this process: "Sign-in completed.", then the account Codex reports once the read returns.
  const after = plain(panel(completed(signedIn())));
  assert.match(after, /Sign-in completed\. /);
  assert.doesNotMatch(after, /checked separately/);
});

test('signed in, the first view waits for the App\'s own history list read at ready: none listed to its end opens a new conversation; a read that stopped short establishes nothing', async () => {
  const historyReads = calls => calls.filter(c => ['history_action', 'history_select', 'history_continue'].includes(c.command) || /history|resume/.test(c.command));
  // The list arrives after the account reading: the App waits for it, then moves once.
  await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
    assert.equal(currentView(ui.container), 'Run a workflow', 'the list is still being read: no conversation is not established');
    await ui.observe(historyAtReady(signedIn(), 'read-to-end'));
    assert.equal(currentView(ui.container), 'Conversation', 'read to its end, none listed, none loaded');
    assert.equal(disclosureOpen(byId(ui.container, 'workspace-start')), true, 'New conversation is open');
    assert.deepEqual(historyReads(ui.calls), [], 'the renderer reads, selects, opens or resumes nothing');
  });
  // Stopped short (an error, no answer, a page missing or a cursor left), even with nothing listed so far: the App stays.
  // A page that arrives after the read stopped moves nothing either.
  await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
    await ui.observe(historyAtReady(signedIn(), 'stopped'));
    assert.equal(currentView(ui.container), 'Run a workflow', 'a partial read never counts as none');
    await ui.observe(historyAtReady(signedIn(), 'stopped', {listCursor: {state: 'exhausted'}}));
    assert.equal(currentView(ui.container), 'Run a workflow', 'decided once: a late page moves nothing');
  });
  // A stored conversation listed, or one loaded in this session: Run a workflow stays.
  for (const [name, host] of [['one listed', historyAtReady(signedIn(), 'read-to-end', {threads: [{native: {id: 'stored'}}]})],
    ['one loaded', historyAtReady(signedIn(base({threads: [{generation: g, threadId: 't'}]})), 'read-to-end')]])
    await mountedApp(host, async ui => { assert.equal(currentView(ui.container), 'Run a workflow', name); });
  // The view does not jump under the person: they navigated while the list was being read, and its late result moves nothing.
  await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
    await ui.navigate('History');
    await ui.observe(historyAtReady(signedIn(), 'reading'));
    await ui.observe(historyAtReady(signedIn(), 'read-to-end'));
    assert.equal(currentView(ui.container), 'History', 'the person navigated before the read returned');
  });
  // Nor over unsent text entered while the list was being read.
  await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
    await ui.type('ordinary-composer-text', 'A draft not yet sent');
    await ui.observe(historyAtReady(signedIn(), 'read-to-end'));
    assert.equal(currentView(ui.container), 'Run a workflow', 'unsent text: no move');
  });
  // A read made for an earlier Codex says nothing about this one.
  const earlier = {...historyAtReady(signedIn(), 'read-to-end')};
  earlier.nativeHistory = {...earlier.nativeHistory, readAtReady: {generation: {...g, spawnCounter: 0}, state: 'reading'}};
  await mountedApp(earlier, async ui => { assert.equal(currentView(ui.container), 'Conversation', 'only the running Codex\'s read is waited for'); });
});


// Every control in the visible view, as the person meets it: what it is, what it says, and whether it can be used.
const controlsShown = c => c.querySelectorAll(e => ['a', 'button', 'input', 'select', 'textarea', 'summary'].includes(e.localName) && visible(e))
  .map(e => [e.localName, e.getAttribute('id') ?? '', e.textContent.trim(), !!props(e)?.disabled]);
const withoutReadAtReady = host => { const {readAtReady, ...history} = host.nativeHistory; return {...host, nativeHistory: history}; };

test('the App is fully usable while the history list read is under way: only the automatic move waits for it', async () => {
  const views = ['Run a workflow', 'Make a workflow', 'Conversation', 'History', 'Settings & tools'];
  // What each view offers, view by view, with the read under way and never returning, and with no read at all.
  const tour = async host => {
    const seen = {};
    await mountedApp(host, async ui => {
      seen.first = currentView(ui.container);
      for (const view of views) {
        await ui.navigate(view);
        assert.equal(currentView(ui.container), view, `the person can go to ${view} while the read is under way`);
        seen[view] = controlsShown(ui.container);
      }
      seen.calls = ui.calls.map(c => c.command).filter(command => !['host_status', 'decision_view', 'native_confirmation_content'].includes(command));
    });
    return seen;
  };
  // Signed in, the account still being read, and no account: in each, the history read is under way (the host marks it
  // before the account is read) and it never returns.
  for (const [name, account] of [['signed in', signedIn()], ['account read under way', underWay()], ['no account', noAccount()]]) {
    const stalled = historyAtReady(account, 'reading');
    const during = await tour(stalled), without = await tour(withoutReadAtReady(stalled));
    assert.equal(during.first, without.first, `${name}: the first view is the one it would be without the read`);
    for (const view of views) assert.deepEqual(during[view], without[view], `${name}: ${view} offers the same controls, none disabled or covered by the read`);
    assert.deepEqual(during.calls, without.calls, `${name}: the read changes nothing the App asks of the host`);
  }
  // Named directly: the workflow controls, New conversation's controls, History's own read and the sign-in.
  await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
    assert.equal(currentView(ui.container), 'Run a workflow', 'the move waits; nothing else does');
    const runControls = controlsShown(ui.container).filter(([tag]) => tag !== 'a');
    assert.ok(runControls.length > 0, 'Run a workflow shows its controls');
    await ui.navigate('Conversation');
    assert.equal(disclosureOpen(byId(ui.container, 'workspace-start')), true, 'New conversation is open, as without the read');
    await ui.navigate('History');
    const read = elements(ui.container, 'button').find(b => b.textContent === 'Read stored conversations' && visible(b));
    assert.ok(read, 'History offers its own read'); assert.equal(props(read).disabled, false, 'History\'s own read is not disabled by the App\'s');
  });
  await mountedApp(historyAtReady(noAccount(), 'reading'), async ui => {
    const signIn = byId(ui.container, 'workspace-sign-in');
    assert.ok(signIn && visible(signIn), 'the sign-in is offered'); assert.equal(props(signIn).disabled, false, 'the sign-in is not disabled by the read');
  });
});

test('the automatic first-view move has its own bound of 10 s from the renderer first seeing Codex ready: a later reading is shown and moves nothing', async () => {
  const {FIRST_VIEW_MOVE_BOUND_MS} = loadSrc('App');
  assert.equal(FIRST_VIEW_MOVE_BOUND_MS, 10_000);
  const realNow = Date.now; let now = 1_000_000; Date.now = () => now;
  const emptyList = {threads: [], listPage: {data: [], nextCursor: null}};
  try {
    // Read to its end, none listed, arriving after the bound: the view stays, and History holds the empty list.
    await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
      now += FIRST_VIEW_MOVE_BOUND_MS + 1;
      await ui.observe(historyAtReady(signedIn(), 'read-to-end', emptyList));
      assert.equal(currentView(ui.container), 'Run a workflow', 'a late reading moves nothing');
      await ui.navigate('History');
      assert.match(ui.container.textContent, /No conversation rows are available from the received list\./, 'History holds the empty list the read returned');
    });
    // Arriving within the bound: it moves.
    await mountedApp(historyAtReady(signedIn(), 'reading'), async ui => {
      now += FIRST_VIEW_MOVE_BOUND_MS - 1;
      await ui.observe(historyAtReady(signedIn(), 'read-to-end', emptyList));
      assert.equal(currentView(ui.container), 'Conversation', 'within the bound: a new conversation');
    });
    // The no-account move rests on the account read (its own wait is 20 s): a late answer moves nothing.
    await mountedApp(underWay(), async ui => {
      now += FIRST_VIEW_MOVE_BOUND_MS + 1;
      await ui.observe(noAccount());
      assert.equal(currentView(ui.container), 'Run a workflow', 'a late no-account reading moves nothing');
      assert.match(ui.container.textContent, /You're not signed in/, 'the reading is still shown');
    });
    await mountedApp(underWay(), async ui => {
      now += FIRST_VIEW_MOVE_BOUND_MS - 1;
      await ui.observe(noAccount());
      assert.equal(currentView(ui.container), 'Settings & tools', 'within the bound: the sign-in');
    });
  } finally { Date.now = realNow; }
});
