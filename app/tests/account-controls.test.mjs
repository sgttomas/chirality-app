// The account row at the foot of the navigator and its popover (AccountControls.tsx), on constructed host snapshots
// only: no real account, sign-in or model. What the row says for each sign-in reading and each connection state, what
// the popover offers and the command each action issues, and how the popover opens and closes. Nothing is stored.
import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {AccountRow, accountRowWords, accountAction, connectionFacts, sourceKey, useAccountController} = loadSrc('AccountControls');
const {accountReading, DIDNT_SAY, signInUnresolved} = loadSrc('AccountStatus');
const {WorkspaceConnectionStatus, connectionWords} = loadSrc('DailyWorkspace');
const {App} = loadSrc('App');

const g = {appSession: 's', home: 'h', spawnCounter: 1};
const EMAIL = 'harbour.surveyor@example.com';
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(n => n.localName === tag);
const rowOf = c => nodes(c, 'button').find(b => b.getAttribute('class') === 'account-controls-row');
const dialogOf = c => nodes(c, 'div').find(d => d.getAttribute('role') === 'dialog');
const group = (c, name) => nodes(c, 'section').find(s => s.getAttribute('aria-label') === name);
const avatarOf = c => nodes(c, 'span').find(s => /account-controls-avatar/.test(s.getAttribute('class') ?? ''));

const base = (over = {}) => ({state: 'ready', generationClosed: false, generation: g, threads: [], roleLimits: {account: {roles: []}},
  homeRouting: {activeModeHomeClass: 'account', entries: [{modeHomeClass: 'account'}]}, serverRequests: [], ...over});
// One account read as the host records it (hosting.rs SourceRequest::evidence; access.rs AccountObservation), as the
// first-view tests construct it, with the field each reading turns on.
const read = ({answer, outcome = 'response-observed-result', source = {}, observed, current, mode = 'account', host = base()} = {}) => {
  const answered = outcome === 'response-observed-result';
  const row = {source: {generation: g, home: g.home, requestIdentity: 1, requestRef: 'read-1', sourceCurrent: true, attemptedFrame: {method: 'account/read', params: {}},
    outcome, authResponseShapeValid: answered, lastClientObservation: {initiator: {kind: 'app-rule', name: 'app-at-ready'}}, ...source},
    accountObservation: observed ?? (answered ? {state: answer === null ? 'native account null observed' : 'native account type observed', account: answer, identityVerified: false} : null)};
  return {...host, homeRouting: {...host.homeRouting, activeModeHomeClass: mode}, homeAccess: {modeHomeClass: mode, observations: [row]},
    accountObservation: current ?? (answered ? {generation: g, home: g.home, state: 'observed', nativeAccount: answer, codexAccount: answer?.email ?? null, identityVerified: false} : null)};
};
const chatgpt = (plan = 'plus') => ({type: 'chatgpt', email: EMAIL, planType: plan});
// Each of the twelve readings (AccountStatus.tsx accountReading), from the host fields that produce it.
const READINGS = {
  unread: base(),
  reading: read({outcome: 'pending'}),
  stale: read({answer: null, source: {sourceCurrent: false}}),
  failed: read({outcome: 'response-observed-error', source: {lastClientObservation: {error: {code: -32603, message: 'invented account error'}}}}),
  pending: read({outcome: 'pending', source: {waitingEnded: true}}),
  unavailable: read({answer: null, source: {authResponseShapeValid: false}}),
  omitted: read({answer: null, observed: {state: 'account omitted; unknown/unavailable'}}),
  changed: read({answer: null, current: {generation: {...g, spawnCounter: 0}, home: g.home, state: 'observed', nativeAccount: null}}),
  'no-account': read({answer: null}),
  'chatgpt-account': read({answer: chatgpt()}),
  'api-key': read({answer: {type: 'apiKey'}}),
  unsupported: read({answer: {type: 'invented'}}),
};
const ROW = {
  unread: ['Sign-in not checked', null], reading: ['Checking sign-in…', null],
  'no-account': ['Not signed in', 'Sign in to start'], 'chatgpt-account': ['Signed in', 'Plan: plus'], 'api-key': ['API key connection', 'Not a ChatGPT sign-in'],
  ...Object.fromEntries(DIDNT_SAY.map(r => [r, ['Sign-in unknown', "Codex didn't say"]])),
};
// Each connection state in which Codex is not ready (lib.rs host_status state; DailyWorkspace.tsx connectionWords).
const INSPECT = 'Open Connection and access to inspect the current status and available controls.';
const NOT_READY = [
  ['no status yet', undefined, 'Reading connection status…', 'Waiting for the App to report its current connection.'],
  ['starting', base({state: 'starting'}), 'Codex is starting…', INSPECT],
  ['stopping', base({state: 'stopping'}), 'Codex is stopping…', INSPECT],
  ['refused', base({state: 'refused', startRefusalCause: 'busy'}), 'Codex was not started', 'The App was busy with another step when Codex was due to start, so it did not start it. Use Start Codex under Connection and access to try again.'],
  ['refused for this home', base({state: 'stopped', codexHome: 'h', lastStartRefusal: {reason: 'invented reason', home: 'h'}}), 'Codex was not started', INSPECT],
  ['exited', base({state: 'exited-unexpectedly'}), 'Codex could not stay connected', INSPECT],
  ['stopped', base({state: 'stopped'}), 'Codex is not connected', INSPECT],
  ['absent', base({state: 'absent'}), 'Codex is not connected', INSPECT],
  ['generation closed', read({answer: chatgpt(), host: base({generationClosed: true})}), 'Codex is not connected', INSPECT],
  // Setup needed speaks before the sign-in even where Codex is ready and reports a ChatGPT account.
  ['setup needed', read({answer: chatgpt(), host: base({desktopSetup: {launch: {state: 'setup-required'}}})}), 'Setup needed', 'Choose shared settings and a project below.'],
  ['setup saved', read({answer: chatgpt(), host: base({desktopSetup: {launch: {state: 'setup-required'}, pending: {}}})}), 'Setup saved — reopen to use it', 'Your saved choices apply on the next launch.'],
];

const noCommands = () => ({async checkAgain() {}, async startSignIn() {}, async signOut() {}});
const noReveals = {openSettings() {}, openConnection() {}};
// One controller, as the App holds one, and the account rows that share it: the navigator's, and with `rows: 2` the
// collapsed strip's beside it; with `line`, the workspace line above the conversation, wired as the App wires it.
function Surfaces({host, latest, commands, reveals, rows, line, moving}) {
  const account = useAccountController(host, latest, commands, moving);
  return React.createElement(React.Fragment, null, ...Array.from({length: rows}, (_, i) =>
    React.createElement('div', {key: i, 'data-surface': String(i)}, React.createElement(AccountRow, {host, account, reveals}))),
    line ? React.createElement(WorkspaceConnectionStatus, {key: 'line', ...connectionFacts(host), source: sourceKey(host), signIn: accountReading(host), completed: account.completed,
      busy: account.acting || signInUnresolved(host), checkAgain: () => account.act('check-again', host), startSignIn: () => account.act('sign-in', host)}) : null);
}
async function mountRow(host, check, {commands = noCommands(), reveals = noReveals, rows = 1, line = false, strict = false} = {}) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  // `latest` is the latest status the App has accepted when an action is sent: the status rendered, unless a test
  // moves it ahead. The status read the controller asks for returns it, unless the commands say otherwise.
  let current = host, moving = false, statusReads = 0;
  const all = {readStatus: async () => current, ...commands};
  const counted = {...all, readStatus: async () => { statusReads++; return all.readStatus(); }};
  const view = next => { const surfaces = React.createElement(Surfaces, {host: next, latest: () => current, commands: counted, reveals, rows, line, moving: () => moving});
    return strict ? React.createElement(React.StrictMode, null, surfaces) : surfaces; };
  const render = async next => { current = next; await React.act(async () => root.render(view(next))); };
  const surface = i => container.childNodes[i];
  try { await render(host); await check({container, render, surface, moveLatest: next => { current = next; }, setMoving: value => { moving = value; }, statusReads: () => statusReads,
    open: async (within = container) => React.act(async () => props(rowOf(within)).onClick())}); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}
// The same status for another Codex process (a restart): every field naming the process names the new one.
const g2 = {...g, spawnCounter: 2};
const restartedAs = (status, generation = g2) => JSON.parse(JSON.stringify(status).replaceAll(JSON.stringify(g), JSON.stringify(generation)));
// A status that also lists account reads issued before its latest one, as the host lists every read it issued.
const withEarlier = (status, refs) => { const latest = status.homeAccess.observations.at(-1);
  return {...status, homeAccess: {...status.homeAccess, observations: [...refs.map(ref => ({...latest, source: {...latest.source, requestRef: ref}})), latest]}}; };
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return {promise, resolve, reject}; };
const lineOf = c => nodes(c, 'section').find(e => e.getAttribute('aria-label') === 'Workspace connection status');
const oauth = (phase, over = {}) => ({homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, phase, mode: 'Browser', ...over}}});
const completedOAuth = (ref = 'login-1') => oauth('CompletedSuccess', {observationRef: ref, actualWriteObserved: true});
const SIGN_IN = 'Sign in with your ChatGPT account (through Codex)…';
const said = c => nodes(group(c, 'Account'), 'p').map(p => p.textContent);
const button = (c, words) => nodes(dialogOf(c), 'button').find(b => b.textContent === words);

test('the row says each of the twelve readings in the App\'s words, and takes the signed-in avatar only for a ChatGPT account', async () => {
  assert.deepEqual(Object.keys(READINGS).sort(), ['api-key', 'changed', 'chatgpt-account', 'failed', 'no-account', 'omitted', 'pending', 'reading', 'stale', 'unavailable', 'unread', 'unsupported']);
  for (const [name, host] of Object.entries(READINGS)) {
    assert.equal(accountReading(host), name, `the fixture produces ${name}`);
    const [state, detail] = ROW[name];
    assert.deepEqual(accountRowWords(host), {state, detail, signedIn: name === 'chatgpt-account'}, name);
    await mountRow(host, async ({container}) => {
      const row = rowOf(container);
      assert.equal(row.getAttribute('aria-label'), `Account and settings, ${state}`, name);
      assert.equal(row.getAttribute('aria-haspopup'), 'dialog'); assert.equal(row.getAttribute('aria-expanded'), 'false');
      assert.equal(nodes(row, 'strong')[0].textContent, state, name);
      assert.equal(nodes(row, 'small')[0]?.textContent ?? null, detail, name);
      assert.equal(avatarOf(container).getAttribute('data-signed-in'), name === 'chatgpt-account' ? 'true' : 'false', name);
      assert.equal(/account-controls-avatar-signed-in/.test(avatarOf(container).getAttribute('class')), name === 'chatgpt-account', name);
    });
  }
  // A ChatGPT account whose plan Codex does not report, or reports outside the App's own list: no plan named.
  assert.equal(accountRowWords(read({answer: chatgpt('unknown')})).detail, 'ChatGPT account');
  assert.equal(accountRowWords(read({answer: chatgpt('invented-plan')})).detail, 'ChatGPT account');
});

test('Codex didn\'t say, not checked and still reading are never "Not signed in" and never the signed-in avatar', async () => {
  for (const name of [...DIDNT_SAY, 'unread', 'reading']) {
    await mountRow(READINGS[name], async ({container, open}) => {
      await open();
      assert.doesNotMatch(container.textContent, /Not signed in|not signed in/, name);
      assert.doesNotMatch(rowOf(container).getAttribute('aria-label'), /Not signed in/, name);
      assert.equal(avatarOf(container).getAttribute('data-signed-in'), 'false', name);
    });
  }
});

test('while Codex is not ready, the row says the workspace line\'s own title for the connection, never a sign-in state', async () => {
  for (const [name, host, title] of NOT_READY) {
    assert.equal(accountRowWords(host).state, title, name);
    assert.equal(accountRowWords(host).signedIn, false, name);
    assert.equal(accountAction(host), null, `${name}: no account action`);
    // The workspace line draws the same title from the same function.
    const facts = connectionFacts(host);
    assert.equal(connectionWords(facts).title, title, name);
    const line = document.createElement('div'); document.body.appendChild(line); const root = createRoot(line);
    await React.act(async () => root.render(React.createElement(WorkspaceConnectionStatus, {...facts, signIn: accountReading(host)})));
    assert.equal(nodes(line, 'strong')[0].textContent, title, `${name}: the workspace line says the same`);
    await React.act(() => root.unmount()); document.body.removeChild(line);
    await mountRow(host, async ({container}) => {
      assert.equal(rowOf(container).getAttribute('aria-label'), `Account and settings, ${title}`, name);
      assert.equal(avatarOf(container).getAttribute('data-signed-in'), 'false', name);
    });
  }
  // Ready, the connection speaks no title: the reading does.
  assert.equal(connectionWords(connectionFacts(base())), null);
});

test('the email Codex reports is never in a control or an accessible name; it stands in the popover as the account panel says it', async () => {
  await mountRow(READINGS['chatgpt-account'], async ({container, open}) => {
    assert.doesNotMatch(container.textContent, new RegExp(EMAIL), 'not in the row');
    await open();
    for (const control of container.querySelectorAll(n => ['button', 'a', 'summary', 'label', 'h1', 'h2', 'h3', 'h4'].includes(n.localName)))
      assert.doesNotMatch(control.textContent, new RegExp(EMAIL), `not inside a ${control.localName}`);
    for (const named of container.querySelectorAll(n => n.hasAttribute('aria-label')))
      assert.doesNotMatch(named.getAttribute('aria-label'), new RegExp(EMAIL), 'not in an accessible name');
    const said = nodes(group(container, 'Account'), 'p').map(p => p.textContent);
    assert.ok(said.includes(`Codex reports a ChatGPT account for this connection: ${EMAIL} · plan plus.`), 'the panel\'s present sentence');
    assert.ok(said.includes("Codex is running and you're signed in with your ChatGPT account. Plan: plus."), 'the workspace line\'s sentence');
  });
});

test('the popover: the state, the present sentence, and one action for the state; the App controls in every state', async () => {
  const expected = {
    unread: 'Check again', reading: null, 'no-account': 'Sign in with your ChatGPT account (through Codex)…', 'chatgpt-account': 'Sign out of ChatGPT…', 'api-key': null,
    ...Object.fromEntries(DIDNT_SAY.map(r => [r, 'Check again'])),
  };
  const sentence = {
    unread: /^Codex is running\. The App hasn't established whether you're signed in/, reading: /^Codex is running\. Checking whether you're signed in\./,
    'no-account': /^Codex is running\. You're not signed in\.$/, 'chatgpt-account': /^Codex is running and you're signed in with your ChatGPT account\. Plan: plus\.$/,
    'api-key': /^Codex is running\. Codex reports an API key for this connection, not a ChatGPT sign-in\./,
    // Where Codex didn't say, each reading keeps its own sentence, the account panel's.
    stale: /^The earlier account check is no longer current\. Check account status again\.$/,
    failed: /^Codex could not read account status\. Check again when ready\.$/,
    pending: /^The account read has not produced a result\. Account status is unknown\.$/,
    unavailable: /^Codex returned an unavailable account response\. Account status is unknown\.$/,
    omitted: /^Codex did not report account status\. This does not mean you are signed out\.$/,
    changed: /^Account status changed or is no longer confirmed for this connection\. Check account status again\.$/,
    unsupported: /^Codex did not provide a supported account status\. Account status is unknown\.$/,
  };
  assert.equal(new Set(DIDNT_SAY.map(r => String(sentence[r]))).size, DIDNT_SAY.length, 'a failed read, an unanswered one and the rest are told apart');
  const check = async (name, host, heading, action, said) => mountRow(host, async ({container, open}) => {
    assert.ok(!dialogOf(container), `${name}: closed, the popover is not in the document`);
    await open();
    const dialog = dialogOf(container);
    assert.equal(dialog.getAttribute('aria-label'), 'Account and settings');
    assert.equal(rowOf(container).getAttribute('aria-controls'), dialog.getAttribute('id'));
    assert.equal(rowOf(container).getAttribute('aria-expanded'), 'true');
    const account = group(dialog, 'Account');
    assert.equal(nodes(account, 'strong')[0].textContent, heading, name);
    assert.match(nodes(account, 'p')[0].textContent, said, name);
    assert.deepEqual(nodes(account, 'button').map(b => b.textContent), action ? [action] : [], name);
    assert.deepEqual(nodes(group(dialog, 'App controls'), 'button').map(b => b.textContent), ['Connection and access…', 'Settings & tools…'], name);
    assert.doesNotMatch(dialog.textContent, /About|Appearance|update/i, `${name}: nothing v4 cannot back`);
  });
  for (const [name, host] of Object.entries(READINGS)) await check(name, host, ROW[name][0], expected[name], sentence[name]);
  for (const [name, host, title, guidance] of NOT_READY)
    await check(name, host, title, null, new RegExp(`^${guidance.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
  // Codex's own message for a failed read, marked as the workspace line marks it.
  await mountRow(READINGS.failed, async ({container, open}) => {
    await open();
    const said = nodes(group(container, 'Account'), 'p').find(p => p.getAttribute('aria-label') === 'What Codex said');
    assert.ok(said && /invented account error/.test(said.textContent));
    assert.ok(said.querySelectorAll(n => /agent-text/.test(n.getAttribute('class') ?? '')).length > 0, 'inside the supplied-text box');
  });
  // A sign-in waiting, one that did not complete and one canceled: the account panel's present words; while one is
  // waiting, the sign-in is not offered a second time.
  for (const [name, state, words, disabled] of [
    ['pending', oauth('Pending'), 'Waiting for sign-in to complete.', true],
    ['failed', oauth('CompletedFailure'), 'Sign-in did not complete. Private details are withheld.', false],
    ['rejected', oauth('StartRejected'), 'Sign-in did not complete. Private details are withheld.', false],
    // A cancel Codex answered ends the sign-in (oauth_control.rs cancel_completed: Cancelled for both answers).
    ['canceled', oauth('Cancelled', {cancelStatus: 'canceled'}), 'The pending sign-in was canceled. Account status is separate.', false],
    ['nothing to cancel', oauth('Cancelled', {cancelStatus: 'notFound'}), 'Codex had no pending sign-in to cancel. Account status is separate.', false],
    // Every other phase the host reports is a sign-in not yet ended (hosting.rs oauth_terminal): no second is offered.
    ['awaiting the write', oauth('AwaitingWrite'), 'Waiting for sign-in to complete.', true],
    ['awaiting the reply', oauth('AwaitingReply'), 'Waiting for sign-in to complete.', true],
    ['cancelling', oauth('Cancelling'), 'An earlier sign-in has not ended. Another can start once it has ended or been canceled.', true],
    ['cancel outcome unknown', oauth('CancellationUnknown'), 'An earlier sign-in has not ended. Another can start once it has ended or been canceled.', true],
    ['end unknown', oauth('Unknown'), 'An earlier sign-in has not ended. Another can start once it has ended or been canceled.', true]]) {
    await mountRow({...READINGS['no-account'], ...state}, async ({container, open}) => {
      await open();
      assert.ok(said(container).includes(words), name);
      assert.equal(props(button(container, SIGN_IN)).disabled, disabled, name);
    });
  }
  // Signed in, a completed sign-in is said by the state, not by a second line.
  await mountRow({...READINGS['chatgpt-account'], ...completedOAuth()}, async ({container, open}) => {
    await open();
    assert.ok(!said(container).includes('Sign-in completed.'));
  });
});

test('each action issues the App\'s present command once, for the Codex process and home shown, under the present disabled conditions; the App controls close the popover', async () => {
  const calls = [];
  let release;
  const commands = {checkAgain: async (generation, mode) => { calls.push(['checkAgain', generation, mode]); },
    startSignIn: generation => { calls.push(['startSignIn', generation]); return new Promise(r => { release = r; }); },
    signOut: async (generation, mode) => { calls.push(['signOut', generation, mode]); }};
  const reveals = {openSettings: () => calls.push(['openSettings']), openConnection: () => calls.push(['openConnection'])};
  await mountRow(READINGS['no-account'], async ({container, open}) => {
    await open();
    assert.equal(props(button(container, SIGN_IN)).disabled, false);
    await React.act(async () => props(button(container, SIGN_IN)).onClick());
    assert.equal(props(button(container, SIGN_IN)).disabled, true, 'one at a time');
    await React.act(async () => props(button(container, SIGN_IN)).onClick());
    assert.deepEqual(calls, [['startSignIn', g]]);
    await React.act(async () => release());
    assert.equal(props(button(container, SIGN_IN)).disabled, false);
    assert.ok(dialogOf(container), 'starting a sign-in leaves the popover open');
  }, {commands, reveals});
  // The present conditions: the account home in use (and a current generation, without which there is no reading and
  // so neither action is offered).
  for (const [name, host, words] of [['no-account in another home', read({answer: null, mode: 'api-key'}), SIGN_IN],
    ['signed in, another home', read({answer: chatgpt(), mode: 'api-key'}), 'Sign out of ChatGPT…']]) {
    await mountRow(host, async ({container, open}) => {
      await open();
      assert.equal(props(button(container, words)).disabled, true, name);
    });
  }
  assert.equal(accountAction({...READINGS['no-account'], generation: undefined}), 'check-again', 'no generation: not read, so no sign-in or sign-out');
  calls.length = 0;
  await mountRow(READINGS['chatgpt-account'], async ({container, open}) => {
    await open();
    await React.act(async () => props(button(container, 'Sign out of ChatGPT…')).onClick());
  }, {commands, reveals});
  await mountRow(READINGS.failed, async ({container, open}) => {
    await open();
    await React.act(async () => props(button(container, 'Check again')).onClick());
  }, {commands, reveals});
  for (const words of ['Connection and access…', 'Settings & tools…']) {
    await mountRow(READINGS.unread, async ({container, open}) => {
      await open();
      await React.act(async () => props(button(container, words)).onClick());
      assert.ok(!dialogOf(container), `${words} closes the popover`);
    }, {commands, reveals});
  }
  assert.deepEqual(calls, [['signOut', g, 'account'], ['checkAgain', g, 'account'], ['openConnection'], ['openSettings']]);
});

test('an action is bound to the Codex process and home shown when it was pressed: a control of an earlier one sends nothing, and the popover closes when they are replaced', async () => {
  const calls = [];
  const commands = {checkAgain: async (...args) => { calls.push(['checkAgain', ...args]); }, startSignIn: async (...args) => { calls.push(['startSignIn', ...args]); }, signOut: async (...args) => { calls.push(['signOut', ...args]); }};
  const restarted = host => ({...host, generation: {...g, spawnCounter: 2}});
  // Codex restarted after the control was drawn and before the status with the new process was rendered: the press
  // is checked against the App's current status, and nothing is sent. Each action.
  for (const [name, host, words] of [['sign-in', READINGS['no-account'], SIGN_IN], ['sign-out', READINGS['chatgpt-account'], 'Sign out of ChatGPT…'], ['check again', READINGS.failed, 'Check again']]) {
    await mountRow(host, async ({container, open, render, moveLatest}) => {
      await open();
      const press = props(button(container, words)).onClick;
      moveLatest(restarted(host));
      await React.act(async () => press());
      assert.deepEqual(calls, [], `${name}: nothing is sent for a process that was replaced`);
      // The status with the new process arrives: the popover closes, so the earlier control is gone; a press of the
      // control captured from it still sends nothing.
      await render(restarted(host));
      assert.ok(!dialogOf(container), `${name}: the popover closes when the process is replaced`);
      await React.act(async () => press());
      assert.deepEqual(calls, [], name);
    }, {commands});
  }
  // The home in use is replaced: the same.
  await mountRow(READINGS['chatgpt-account'], async ({container, open, render}) => {
    await open();
    const press = props(button(container, 'Sign out of ChatGPT…')).onClick;
    await render(read({answer: chatgpt(), mode: 'api-key'}));
    assert.ok(!dialogOf(container), 'the popover closes when the home is replaced');
    await React.act(async () => press());
    assert.deepEqual(calls, []);
  }, {commands});
  // The same process and home, but the account's state no longer offers the action (signed out elsewhere since): a
  // sign-out captured before sends nothing, and the popover says so.
  await mountRow(READINGS['chatgpt-account'], async ({container, open, render, moveLatest}) => {
    await open();
    const press = props(button(container, 'Sign out of ChatGPT…')).onClick;
    moveLatest(READINGS['no-account']);
    await React.act(async () => press());
    assert.deepEqual(calls, []);
    await render(READINGS['no-account']);
    assert.ok(said(container).includes('The connection or the account changed before this was sent. Nothing was sent.'));
    // A sign-in waiting to complete: a sign-in control captured before it sends no second one.
    const signIn = props(button(container, SIGN_IN)).onClick;
    moveLatest({...READINGS['no-account'], ...oauth('Pending')});
    await React.act(async () => signIn());
    assert.deepEqual(calls, [], 'no second sign-in while one waits');
  }, {commands});
  // Unchanged, the press is sent for the process and home shown.
  await mountRow(READINGS['chatgpt-account'], async ({container, open}) => {
    await open();
    await React.act(async () => props(button(container, 'Sign out of ChatGPT…')).onClick());
    assert.deepEqual(calls, [['signOut', g, 'account']]);
  }, {commands});
});

test('one account action at a time across every surface, and across closing and reopening the popover', async () => {
  const calls = [];
  let release;
  const commands = {...noCommands(), startSignIn: () => { calls.push('startSignIn'); return new Promise(r => { release = r; }); }};
  await mountRow(READINGS['no-account'], async ({surface, open}) => {
    const [first, second] = [surface(0), surface(1)];
    await open(first);
    await React.act(async () => props(button(first, SIGN_IN)).onClick());
    // The other surface (the collapsed strip's row beside the navigator's) shows it under way and sends nothing.
    await open(second);
    assert.equal(props(button(second, SIGN_IN)).disabled, true, 'under way on every surface');
    await React.act(async () => props(button(second, SIGN_IN)).onClick());
    // Closed and opened again while the command is still out: still under way.
    await open(first); assert.ok(!dialogOf(first));
    await open(first);
    assert.equal(props(button(first, SIGN_IN)).disabled, true, 'reopening does not forget it');
    await React.act(async () => props(button(first, SIGN_IN)).onClick());
    assert.deepEqual(calls, ['startSignIn']);
    await React.act(async () => release());
    assert.equal(props(button(first, SIGN_IN)).disabled, false); assert.equal(props(button(second, SIGN_IN)).disabled, false);
  }, {commands, rows: 2});
});

test('an action that was refused or failed is said beside it in the App\'s words, and no longer once the account has moved on', async () => {
  const refuse = async () => { throw Error('invented refusal with a private detail'); };
  for (const [name, host, words, feedback] of [
    ['sign-in', READINGS['no-account'], SIGN_IN, 'The App could not confirm that a sign-in started.'],
    ['sign-out', READINGS['chatgpt-account'], 'Sign out of ChatGPT…', 'The App could not confirm the sign-out. Check again to see the account.'],
    ['check again', READINGS.failed, 'Check again', 'Account status could not be confirmed. Try checking again; this does not mean you are signed out.']]) {
    await mountRow(host, async ({container, open, render}) => {
      await open();
      await React.act(async () => props(button(container, words)).onClick());
      const status = nodes(group(container, 'Account'), 'p').find(p => p.getAttribute('role') === 'status');
      assert.equal(status?.textContent, feedback, name);
      assert.doesNotMatch(dialogOf(container).textContent, /invented refusal|private detail/, `${name}: the raw error is not in the popover`);
      assert.equal(props(button(container, words)).disabled, false, `${name}: it can be tried again`);
      // Closed and reopened, it is still said; once the account reads differently, it is not.
      await open(); await open();
      assert.ok(said(container).includes(feedback), `${name}: kept across reopening`);
      await render(READINGS.reading);
      assert.ok(!said(container).includes(feedback), `${name}: gone once the account has moved on`);
    }, {commands: {checkAgain: refuse, startSignIn: refuse, signOut: refuse}});
  }
});

test('a sign-in Codex reports completed is said as completed until an account read issued after it answers; a read made while it was pending, or one with no reference, is not that read', async () => {
  const pending = withEarlier({...READINGS['no-account'], ...oauth('Pending')}, []);
  // A status that reports the completion, with the account reads it lists (the latest last).
  const after = (ref, answer, earlier = [], outcome) => withEarlier(read({answer, outcome, source: {requestRef: ref}, host: {...base(), ...completedOAuth()}}), earlier);
  const calls = [];
  let answer = deferred();
  const commands = {...noCommands(), checkAgain: async () => { calls.push('checkAgain'); await answer.promise; }, startSignIn: async () => { calls.push('startSignIn'); }};
  await mountRow(pending, async ({container, open, render, statusReads}) => {
    await open();
    // The completion arrives in the same status as an account read issued while the sign-in was pending (read-2,
    // answering a ChatGPT account): that read is not taken for the account after the sign-in.
    await render(after('read-2', chatgpt(), ['read-1']));
    assert.equal(rowOf(container).getAttribute('aria-label'), 'Account and settings, Sign-in completed', 'not "Signed in" from a read made before');
    assert.equal(avatarOf(container).getAttribute('data-signed-in'), 'false');
    assert.ok(dialogOf(container), 'the completion alone does not close it');
    // Seeing the completion, the controller reads the status once for the reads already issued, then the account
    // once, without a press; while that read is out the account is being checked.
    assert.equal(statusReads(), 1); assert.deepEqual(calls, ['checkAgain']);
    assert.equal(nodes(rowOf(container), 'small')[0].textContent, 'Checking the account…');
    assert.ok(said(container).includes('Codex reports the sign-in completed. Checking the account with Codex…'));
    assert.deepEqual(nodes(group(container, 'Account'), 'button').map(b => b.textContent), [], 'no action while it is checked');
    // Its read has answered, but no status after it is shown yet: still not said, and Check again is offered, never a
    // second sign-in.
    await React.act(async () => answer.resolve());
    assert.equal(nodes(rowOf(container), 'small')[0].textContent, 'Account not read yet');
    assert.ok(said(container).includes('Codex reports the sign-in completed. The account has not been read since.'));
    assert.doesNotMatch(dialogOf(container).textContent, /not signed in|Not signed in/);
    assert.deepEqual(nodes(group(container, 'Account'), 'button').map(b => b.textContent), ['Check again']);
    // A newer read the status lists without a reference proves nothing.
    await render(after(undefined, chatgpt(), ['read-1', 'read-2']));
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Sign-in completed', 'a read without a reference is not the read after it');
    // The status after the controller's read lists it (read-3): that is the read after the completion.
    await render(after('read-3', chatgpt(), ['read-1', 'read-2']));
    assert.ok(!dialogOf(container), 'closed when the read after it confirms the account');
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Signed in');
    await open();
    await render(after('read-3', chatgpt(), ['read-1', 'read-2']));
    assert.ok(dialogOf(container), 'the same completion does not close it again');
    // The same completion seen again after a status in which it could not be read does not close a later opening.
    await render({...after('read-3', chatgpt(), ['read-1', 'read-2']), state: 'starting'});
    await render(after('read-3', chatgpt(), ['read-1', 'read-2']));
    assert.ok(dialogOf(container), 'a completion already seen never closes a later opening');
    assert.equal(statusReads(), 1); assert.deepEqual(calls, ['checkAgain'], 'one account read for the completion');
  }, {commands});
  // The read after the completion answers that there is no account: said as that, with the sign-in offered again.
  answer = deferred(); answer.resolve(); calls.length = 0;
  await mountRow(pending, async ({container, open, render}) => {
    await open();
    await render(after('read-1', null));
    await render(after('read-2', null, ['read-1']));
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Not signed in');
    assert.ok(button(container, SIGN_IN));
    assert.ok(dialogOf(container));
  }, {commands});
  // The read after it fails: the reading is said as Codex didn't say, with Check again to try once more.
  await mountRow(pending, async ({container, open, render}) => {
    await open();
    await render(after('read-1', null));
    await render(after('read-2', undefined, ['read-1'], 'response-observed-error'));
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Sign-in unknown');
    assert.ok(button(container, 'Check again'));
  }, {commands});
  // The status read for the baseline fails, before any account read: a clear retry, and the retry makes both reads.
  let statusFails = true;
  calls.length = 0;
  await mountRow(pending, async ({container, open, render, statusReads}) => {
    await open();
    await render(after('read-1', null));
    assert.deepEqual(calls, [], 'no account read without the baseline');
    assert.equal(nodes(rowOf(container), 'small')[0].textContent, 'Account not read yet');
    assert.ok(said(container).includes('Account status could not be confirmed. Try checking again; this does not mean you are signed out.'));
    statusFails = false;
    await React.act(async () => props(button(container, 'Check again')).onClick());
    assert.equal(statusReads(), 2); assert.deepEqual(calls, ['checkAgain']);
  }, {commands: {...commands, readStatus: async () => { if (statusFails) throw Error('invented status failure'); return after('read-1', null); }}});
  // A completion already there when this App view first saw the Codex process was not watched completing: no status
  // or account read is made for it, it moves and closes nothing, and the row says the reading the status shows.
  calls.length = 0;
  await mountRow(after('read-1', null), async ({container, open, render, statusReads}) => {
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Not signed in', 'what the status shows');
    await open();
    await render({...READINGS['chatgpt-account'], ...completedOAuth()});
    assert.ok(dialogOf(container));
    assert.equal(statusReads(), 0); assert.deepEqual(calls, []);
  }, {commands});
  // Under React's strict rendering (renders and effects run twice): still one status read and one account read.
  calls.length = 0;
  await mountRow(pending, async ({container, render, statusReads}) => {
    await render(after('read-2', chatgpt(), ['read-1']));
    assert.equal(statusReads(), 1); assert.deepEqual(calls, ['checkAgain']);
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Sign-in completed');
    await render(after('read-3', chatgpt(), ['read-1', 'read-2']));
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Signed in');
  }, {commands, strict: true});
  // A sign-in that did not complete keeps it open, so its words and the retry stay reachable.
  await mountRow(pending, async ({container, open, render}) => {
    await open();
    await render({...READINGS['no-account'], ...oauth('CompletedFailure')});
    assert.ok(dialogOf(container));
    assert.equal(props(button(container, SIGN_IN)).disabled, false);
  });
});

test('focus: the popover takes focus back only where the control that held it inside was removed, never because the body is active, and no focus it moves scrolls', async () => {
  const proto = Object.getPrototypeOf(document.createElement('div'));
  let focused = null;
  const moves = [], scrolls = [];
  proto.focus = function (options) { focused = this; moves.push(options); };
  proto.scrollIntoView = function () { scrolls.push(this); };
  Object.defineProperty(document, 'activeElement', {configurable: true, get: () => focused ?? document.body});
  const pending = withEarlier({...READINGS['no-account'], ...oauth('Pending')}, []);
  const confirmed = withEarlier(read({answer: chatgpt(), source: {requestRef: 'read-2'}, host: {...base(), ...completedOAuth()}}), ['read-1']);
  const completedFirst = withEarlier(read({answer: null, host: {...base(), ...completedOAuth()}}), []);
  const panelOf = c => dialogOf(c);
  try {
    // Sign out: the control that held focus is replaced by the sign-in; focus goes to the popover.
    await mountRow(READINGS['chatgpt-account'], async ({container, open, render}) => {
      await open();
      const signOut = button(container, 'Sign out of ChatGPT…');
      await React.act(async () => props(panelOf(container)).onFocus({target: signOut}));
      focused = null; // the pressed control is gone from the document: the browser leaves focus on the body
      await render(READINGS['no-account']);
      assert.ok(focused === dialogOf(container), 'focus is put on the popover');
    });
    // The body is active because the person moved focus away (to another window, or nowhere) while the control that
    // held focus is still there: the popover does not take focus.
    await mountRow(READINGS['no-account'], async ({container, open, render}) => {
      await open();
      await React.act(async () => props(panelOf(container)).onFocus({target: button(container, SIGN_IN)}));
      focused = null;
      await render({...READINGS['no-account']});
      assert.ok(focused === null, 'focus the person moved is not taken');
    });
    // A sign-in confirmed while focus is inside: the popover closes and focus goes to the row.
    await mountRow(pending, async ({container, open, render}) => {
      await open();
      assert.ok(focused === dialogOf(container));
      await render(completedFirst);
      await render(confirmed);
      assert.ok(!dialogOf(container)); assert.ok(focused === rowOf(container), 'focus returns to the row');
    });
    // Confirmed while the person's focus is elsewhere: the popover closes and their focus is left alone.
    await mountRow(pending, async ({container, open, render}) => {
      await open();
      await render(completedFirst);
      const elsewhere = document.createElement('button'); document.body.appendChild(elsewhere); focused = elsewhere;
      await render(confirmed);
      assert.ok(!dialogOf(container)); assert.ok(focused === elsewhere, 'focus elsewhere is not taken');
      document.body.removeChild(elsewhere);
    });
    // The row leaves view with focus inside: the popover closes and focus goes to the row without scrolling it back.
    const rectProto = proto, saved = {innerWidth: window.innerWidth, innerHeight: window.innerHeight};
    let rect = {top: 700, bottom: 756, left: 8};
    rectProto.getBoundingClientRect = function () { return rect; };
    Object.assign(window, {innerWidth: 1440, innerHeight: 900});
    try {
      await mountRow(READINGS['no-account'], async ({container, open, render}) => {
        await open();
        assert.ok(focused === dialogOf(container));
        rect = {top: 940, bottom: 996, left: 8};
        await render({...READINGS['no-account']});
        assert.ok(!dialogOf(container)); assert.ok(focused === rowOf(container));
      });
    } finally { delete rectProto.getBoundingClientRect; Object.assign(window, saved); }
    assert.ok(moves.length > 0);
    assert.ok(moves.every(options => options?.preventScroll === true), 'every automatic focus is made without scrolling');
    assert.equal(scrolls.length, 0, 'nothing is scrolled into view');
  } finally { delete proto.focus; delete proto.scrollIntoView; delete document.activeElement; }
});

test('the popover opens beside the row and takes focus; Escape returns focus to the row; a press outside or focus leaving closes it', async () => {
  const proto = Object.getPrototypeOf(document.createElement('div'));
  let focused = null;
  proto.focus = function () { focused = this; };
  const listeners = type => document.listeners.filter(l => l.type === type);
  try {
    await mountRow(READINGS['no-account'], async ({container, open}) => {
      await open();
      assert.ok(focused === dialogOf(container), 'the popover takes focus');
      // Escape: closed, focus back on the row.
      await React.act(async () => { for (const {listener} of listeners('keydown')) listener({key: 'Escape', preventDefault() {}}); });
      assert.ok(!dialogOf(container)); assert.ok(focused === rowOf(container));
      assert.equal(listeners('keydown').length + listeners('pointerdown').length, 0, 'its listeners are removed');
      // Another key does nothing.
      await open();
      await React.act(async () => { for (const {listener} of listeners('keydown')) listener({key: 'a', preventDefault() {}}); });
      assert.ok(dialogOf(container));
      // A press inside keeps it; outside closes it.
      const inside = nodes(dialogOf(container), 'button')[0];
      await React.act(async () => { for (const {listener} of listeners('pointerdown')) listener({target: inside}); });
      assert.ok(dialogOf(container), 'a press inside keeps it open');
      const elsewhere = document.createElement('div'); document.body.appendChild(elsewhere);
      await React.act(async () => { for (const {listener} of listeners('pointerdown')) listener({target: elsewhere}); });
      assert.ok(!dialogOf(container), 'a press outside closes it');
      // Focus moving within it keeps it; leaving closes it; focus leaving the window (no next element) keeps it.
      await open();
      const root = nodes(container, 'div').find(d => d.getAttribute('class') === 'account-controls-root');
      await React.act(async () => props(root).onBlur({relatedTarget: nodes(dialogOf(container), 'button')[1], currentTarget: root}));
      assert.ok(dialogOf(container));
      await React.act(async () => props(root).onBlur({relatedTarget: null, currentTarget: root}));
      assert.ok(dialogOf(container), 'the window losing focus (a browser opening for sign-in) keeps it');
      await React.act(async () => props(root).onBlur({relatedTarget: elsewhere, currentTarget: root}));
      assert.ok(!dialogOf(container), 'focus leaving closes it');
      document.body.removeChild(elsewhere);
      // The row toggles it.
      await open(); await open();
      assert.ok(!dialogOf(container));
    });
  } finally { delete proto.focus; }
});

test('the popover is placed within the window: above the row when there is more room above, else below', async () => {
  const proto = Object.getPrototypeOf(document.createElement('div'));
  const saved = {innerWidth: window.innerWidth, innerHeight: window.innerHeight};
  let rect;
  proto.getBoundingClientRect = function () { return rect; };
  Object.assign(window, {innerWidth: 1440, innerHeight: 900});
  try {
    rect = {top: 840, bottom: 896, left: 8};
    await mountRow(READINGS['no-account'], async ({container, open}) => {
      await open();
      const style = dialogOf(container).style;
      assert.equal(style.top, 'auto'); assert.equal(style.bottom, `${900 - 840 + 8}px`); assert.equal(style.left, '12px'); assert.equal(style.width, '300px');
    });
    rect = {top: 40, bottom: 96, left: 1300};
    await mountRow(READINGS['no-account'], async ({container, open}) => {
      await open();
      const style = dialogOf(container).style;
      assert.equal(style.top, '104px'); assert.equal(style.bottom, 'auto'); assert.equal(style.left, `${1440 - 300 - 12}px`, 'kept inside the window');
    });
    // The layout moves the row (a notice appears above the regions): the popover follows it at the next status.
    rect = {top: 700, bottom: 756, left: 8};
    await mountRow(READINGS['no-account'], async ({container, open, render}) => {
      await open();
      assert.equal(dialogOf(container).style.bottom, `${900 - 700 + 8}px`);
      rect = {top: 760, bottom: 816, left: 8};
      await render({...READINGS['no-account']});
      assert.equal(dialogOf(container).style.bottom, `${900 - 760 + 8}px`, 'placed again where the row now is');
      // The row leaves view (scrolled away, or its region no longer drawn): the popover closes.
      rect = {top: 940, bottom: 996, left: 8};
      await render({...READINGS['no-account']});
      assert.ok(!dialogOf(container), 'closed when its row is out of view');
    });
    rect = {top: 0, bottom: 0, left: 0, width: 0, height: 0};
    await mountRow(READINGS['no-account'], async ({container, open}) => {
      await open();
      assert.ok(!dialogOf(container), 'a row that is not drawn opens no popover');
    });
  } finally { delete proto.getBoundingClientRect; Object.assign(window, saved); }
});

test('a press that began on a control drawn for one Codex process never sends for its replacement, even where the replacement offers the same action in the same place', async () => {
  const calls = [];
  const commands = {checkAgain: async (...args) => { calls.push(['checkAgain', ...args]); }, startSignIn: async (...args) => { calls.push(['startSignIn', ...args]); }, signOut: async (...args) => { calls.push(['signOut', ...args]); }};
  for (const [name, host, words] of [['sign-in', READINGS['no-account'], SIGN_IN], ['check again', READINGS.failed, 'Check again']]) {
    await mountRow(host, async ({container, render}) => {
      // The pointer goes down on the line's control; before it is released, the status for the restarted Codex
      // process, whose account reads the same, is committed.
      const pressed = nodes(lineOf(container), 'button').find(b => b.textContent === words);
      const retained = props(pressed).onClick;
      await render(restartedAs(host));
      const now = nodes(lineOf(container), 'button').find(b => b.textContent === words);
      assert.ok(now, `${name}: the replacement offers its own`);
      assert.ok(now !== pressed, `${name}: a control drawn anew for the replacement`);
      assert.ok(!container.contains(pressed), `${name}: the control the press began on is no longer in the document`);
      // The release: the browser gives the click to the control the press began on only while it is in the document.
      if (container.contains(pressed)) await React.act(async () => { await props(pressed).onClick(); });
      assert.deepEqual(calls, [], `${name}: nothing is sent for the replacement`);
      // A callback kept from the earlier control sends nothing either.
      await React.act(async () => { await retained(); });
      assert.deepEqual(calls, [], `${name}: nor by a retained callback`);
      // The replacement's own control sends for the replacement.
      await React.act(async () => { await props(now).onClick(); });
      assert.deepEqual(calls.map(call => call[1]), [g2], `${name}: the replacement's control sends for it`);
      calls.length = 0;
    }, {commands, line: true, rows: 0});
  }
  // The latest status the App accepted names the replacement before it is rendered: a press on the control still
  // shown sends nothing, from the line or from the popover.
  await mountRow(READINGS['no-account'], async ({container, open, moveLatest}) => {
    moveLatest(restartedAs(READINGS['no-account']));
    await React.act(async () => { await props(nodes(lineOf(container), 'button').find(b => b.textContent === SIGN_IN)).onClick(); });
    await open();
    await React.act(async () => { await props(button(container, SIGN_IN)).onClick(); });
    assert.deepEqual(calls, []);
  }, {commands, line: true});
});

test('no account action is sent while the App is moving between homes', async () => {
  const calls = [];
  const commands = {checkAgain: async () => { calls.push('checkAgain'); }, startSignIn: async () => { calls.push('startSignIn'); }, signOut: async () => { calls.push('signOut'); }};
  for (const [host, words] of [[READINGS['no-account'], SIGN_IN], [READINGS['chatgpt-account'], 'Sign out of ChatGPT…'], [READINGS.failed, 'Check again']]) {
    await mountRow(host, async ({container, open, setMoving}) => {
      await open();
      setMoving(true);
      await React.act(async () => { await props(button(container, words)).onClick(); });
      assert.deepEqual(calls, [], words);
      assert.ok(said(container).includes('The connection or the account changed before this was sent. Nothing was sent.'), words);
      setMoving(false);
      await React.act(async () => { await props(button(container, words)).onClick(); });
      assert.equal(calls.length, 1, `${words}: sent once the move has ended`);
      calls.length = 0;
    }, {commands});
  }
});

test('an outcome is said for the attempt that produced it: a confirmation the person declined in fixed App words, a late failure only for the process it was sent for', async () => {
  // Declined at the native confirmation: the command resolves with its structured result, nothing was sent.
  for (const [name, host, words, commands, sentence] of [
    ['sign-in', READINGS['no-account'], SIGN_IN, {...noCommands(), startSignIn: async () => ({state: 'native start confirmation dismissed; no sign-in RPC'})}, 'Sign-in was not started.'],
    ['sign-out', READINGS['chatgpt-account'], 'Sign out of ChatGPT…', {...noCommands(), signOut: async () => ({state: 'native confirmation cancelled; no logout request', assessment: {invented: 'host words'}})}, 'You were not signed out.']]) {
    await mountRow(host, async ({container, open}) => {
      await open();
      await React.act(async () => { await props(button(container, words)).onClick(); });
      const status = nodes(group(container, 'Account'), 'p').find(p => p.getAttribute('role') === 'status');
      assert.equal(status?.textContent, sentence, name);
      assert.doesNotMatch(dialogOf(container).textContent, /native|host words/, `${name}: no text the host supplied`);
    }, {commands});
  }
  // Any other result is not a declined confirmation: nothing is said.
  await mountRow(READINGS['no-account'], async ({container, open}) => {
    await open();
    await React.act(async () => { await props(button(container, SIGN_IN)).onClick(); });
    assert.ok(!nodes(group(container, 'Account'), 'p').find(p => p.getAttribute('role') === 'status'));
  }, {commands: {...noCommands(), startSignIn: async () => ({state: 'invented'})}});
  // A failure that arrives after the Codex process was replaced is not said on the replacement, whose account reads
  // the same; it is said for the process it was sent for.
  for (const replaced of [true, false]) {
    const late = deferred();
    await mountRow(READINGS['no-account'], async ({container, open, render}) => {
      await open();
      await React.act(async () => { void props(button(container, SIGN_IN)).onClick(); });
      if (replaced) await render(restartedAs(READINGS['no-account']));
      await React.act(async () => { late.reject(Error('invented late failure')); await late.promise.catch(() => {}); });
      if (!dialogOf(container)) await open();
      const words = said(container);
      if (replaced) assert.ok(!words.includes('The App could not confirm that a sign-in started.'), 'not said on the replacement');
      else assert.ok(words.includes('The App could not confirm that a sign-in started.'), 'said for the process it was sent for');
    }, {commands: {...noCommands(), startSignIn: () => late.promise}});
  }
});

// ---- Through the mounted App: the commands each action issues, and where a failure is said ----
async function mountedApp(initial, check, refuse = new Set(), held = {}, results = {}) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container), calls = [];
  const previousGetById = document.getElementById;
  document.getElementById = id => container.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (held[command]) await held[command];
    if (refuse.has(command)) throw Error('invented refusal');
    if (command === 'host_status') return initial;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_home_access') return initial.homeAccess;
    if (command === 'oauth_start' || command === 'logout_home') return results[command] ?? {state: 'invented'};
    if (command === 'read_available_models') throw Error('no model list in this test');
    throw Error(`Unexpected command ${command}`);
  });
  try { await React.act(async () => root.render(React.createElement(App))); await check({container, calls}); }
  finally { const text = container.textContent; await React.act(() => root.unmount()); document.body.removeChild(container); idle.restore(text); document.getElementById = previousGetById; }
}
const byIdIn = (c, id) => c.querySelectorAll(n => n.getAttribute('id') === id)[0];
const navigatorOf = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'Workspace Navigator')[0];
const pressInPopover = async (c, words) => {
  await React.act(async () => props(rowOf(navigatorOf(c))).onClick());
  const control = nodes(dialogOf(navigatorOf(c)), 'button').find(b => b.textContent === words);
  assert.ok(control, words);
  await React.act(async () => { await props(control).onClick(); });
};
const issued = (calls, command) => calls.filter(c => c.command === command).map(c => c.args);

test('mounted: the popover\'s sign-in, Check again and Sign out issue the present commands with the present arguments', async () => {
  await mountedApp(READINGS['no-account'], async ({container, calls}) => {
    await pressInPopover(container, 'Sign in with your ChatGPT account (through Codex)…');
    assert.deepEqual(issued(calls, 'oauth_start'), [{generation: g, mode: 'browser'}]);
  });
  await mountedApp(READINGS['chatgpt-account'], async ({container, calls}) => {
    await pressInPopover(container, 'Sign out of ChatGPT…');
    assert.deepEqual(issued(calls, 'logout_home'), [{generation: g, modeHomeClass: 'account'}]);
  });
  await mountedApp(READINGS.failed, async ({container, calls}) => {
    await pressInPopover(container, 'Check again');
    assert.deepEqual(issued(calls, 'read_home_access'), [{generation: g, modeHomeClass: 'account'}]);
  });
  // Opening the popover asks the host nothing.
  await mountedApp(READINGS['no-account'], async ({container, calls}) => {
    const before = calls.length;
    await React.act(async () => props(rowOf(navigatorOf(container))).onClick());
    assert.equal(calls.length, before);
  });
});

test('mounted: a refused sign-in or sign-out is said beside the action in the App\'s words and on the App line in the present words', async () => {
  const beside = c => nodes(group(dialogOf(navigatorOf(c)), 'Account'), 'p').find(p => p.getAttribute('role') === 'status')?.textContent;
  await mountedApp(READINGS['no-account'], async ({container}) => {
    await pressInPopover(container, SIGN_IN);
    assert.match(container.textContent, /oauth_start: Error: invented refusal/);
    assert.equal(beside(container), 'The App could not confirm that a sign-in started.');
  }, new Set(['oauth_start']));
  await mountedApp(READINGS['chatgpt-account'], async ({container}) => {
    await pressInPopover(container, 'Sign out of ChatGPT…');
    assert.match(container.textContent, /logout_home: Error: invented refusal/);
    assert.equal(beside(container), 'The App could not confirm the sign-out. Check again to see the account.');
  }, new Set(['logout_home']));
});

test('mounted: the workspace line and the popover share one account action at a time, and neither starts a sign-in while one waits', async () => {
  let release;
  const held = {oauth_start: new Promise(r => { release = r; })};
  const line = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'Workspace connection status')[0];
  const lineSignIn = c => nodes(line(c), 'button').find(b => b.textContent === SIGN_IN);
  const leaveSettings = async c => React.act(async () => props(nodes(c, 'button').find(b => b.getAttribute('role') === 'tab' && b.textContent === 'History')).onClick());
  await mountedApp(READINGS['no-account'], async ({container, calls}) => {
    // Away from Connection and access, the line above the conversation carries the sign-in.
    await leaveSettings(container);
    assert.equal(props(lineSignIn(container)).disabled, false);
    await React.act(async () => { void props(lineSignIn(container)).onClick(); });
    assert.equal(issued(calls, 'oauth_start').length, 1);
    // Under way: the popover's sign-in is not pressable, and a press of it sends nothing.
    await React.act(async () => props(rowOf(navigatorOf(container))).onClick());
    const inPopover = () => nodes(dialogOf(navigatorOf(container)), 'button').find(b => b.textContent === SIGN_IN);
    assert.equal(props(inPopover()).disabled, true, 'the popover shows the line\'s action under way');
    await React.act(async () => { await props(inPopover()).onClick(); });
    assert.equal(issued(calls, 'oauth_start').length, 1, 'one sign-in start');
    await React.act(async () => { release(); await held.oauth_start; });
    assert.equal(props(inPopover()).disabled, false);
  }, new Set(), held);
  // A sign-in waiting to complete, whichever surface started it: neither offers a second.
  await mountedApp({...READINGS['no-account'], ...oauth('Pending')}, async ({container, calls}) => {
    await leaveSettings(container);
    assert.equal(props(lineSignIn(container)).disabled, true, 'the line');
    await React.act(async () => props(rowOf(navigatorOf(container))).onClick());
    const inPopover = nodes(dialogOf(navigatorOf(container)), 'button').find(b => b.textContent === SIGN_IN);
    assert.equal(props(inPopover).disabled, true, 'the popover');
    await React.act(async () => { await props(inPopover).onClick(); });
    assert.deepEqual(issued(calls, 'oauth_start'), []);
  });
});

test('mounted: Connection and access shares the one admission with the row, the strip and the line, both ways', async () => {
  const panel = c => c.querySelectorAll(n => n.getAttribute('aria-label') === 'Account connection')[0];
  const inPanel = (c, words) => nodes(panel(c), 'button').find(b => b.textContent === words);
  const inPopover = (c, words) => nodes(dialogOf(navigatorOf(c)), 'button').find(b => b.textContent === words);
  const openPopover = async c => React.act(async () => props(rowOf(navigatorOf(c))).onClick());
  const leaveSettings = async c => React.act(async () => props(nodes(c, 'button').find(b => b.getAttribute('role') === 'tab' && b.textContent === 'History')).onClick());
  const lineButton = (c, words) => nodes(c.querySelectorAll(n => n.getAttribute('aria-label') === 'Workspace connection status')[0], 'button').find(b => b.textContent === words);
  // A sign-out from the popover is under way: Connection and access neither sends another nor checks the account.
  let release;
  const signOutHeld = {logout_home: new Promise(r => { release = r; })};
  await mountedApp(READINGS['chatgpt-account'], async ({container, calls}) => {
    await openPopover(container);
    await React.act(async () => { void props(inPopover(container, 'Sign out of ChatGPT…')).onClick(); });
    assert.equal(issued(calls, 'logout_home').length, 1);
    assert.equal(props(inPanel(container, 'Sign out of ChatGPT…')).disabled, true, 'shown under way in Connection and access');
    await React.act(async () => { await props(inPanel(container, 'Sign out of ChatGPT…')).onClick(); });
    assert.equal(issued(calls, 'logout_home').length, 1, 'one sign-out');
    assert.equal(props(inPanel(container, 'Check account status')).disabled, true);
    await React.act(async () => { await props(inPanel(container, 'Check account status')).onClick(); });
    assert.equal(issued(calls, 'read_home_access').length, 0, 'no account read beside it');
    await React.act(async () => { release(); await signOutHeld.logout_home; });
  }, new Set(), signOutHeld);
  // The reverse: Connection and access's sign-in is under way; the line and the popover send none.
  const signInHeld = {oauth_start: new Promise(r => { release = r; })};
  await mountedApp(READINGS['no-account'], async ({container, calls}) => {
    await React.act(async () => { void props(byIdIn(container, 'workspace-sign-in')).onClick(); });
    assert.equal(issued(calls, 'oauth_start').length, 1);
    await leaveSettings(container);
    assert.equal(props(lineButton(container, SIGN_IN)).disabled, true, 'the line shows it under way');
    await React.act(async () => { await props(lineButton(container, SIGN_IN)).onClick(); });
    await openPopover(container);
    assert.equal(props(inPopover(container, SIGN_IN)).disabled, true, 'the popover shows it under way');
    await React.act(async () => { await props(inPopover(container, SIGN_IN)).onClick(); });
    await React.act(async () => { await props(inPanel(container, 'Sign in through native device code…')).onClick(); });
    assert.equal(issued(calls, 'oauth_start').length, 1, 'one sign-in start');
    await React.act(async () => { release(); await signInHeld.oauth_start; });
  }, new Set(), signInHeld);
  // The host reports an earlier sign-in that has not ended, in each such phase: no surface offers or sends another;
  // Connection and access keeps its own controls for showing and canceling it.
  for (const phase of ['AwaitingWrite', 'AwaitingReply', 'Pending', 'Cancelling', 'CancellationUnknown', 'Unknown']) {
    await mountedApp({...READINGS['no-account'], ...oauth(phase, {presentationAvailable: true, cancelAvailable: true})}, async ({container, calls}) => {
      for (const control of [byIdIn(container, 'workspace-sign-in'), inPanel(container, 'Sign in through native device code…')]) {
        assert.equal(props(control).disabled, true, `${phase}: ${control.textContent}`);
        await React.act(async () => { await props(control).onClick(); });
      }
      assert.equal(props(inPanel(container, 'Show pending native sign-in…')).disabled, false, `${phase}: it can still be shown`);
      assert.equal(props(inPanel(container, 'Cancel original pending sign-in with native confirmation…')).disabled, false, `${phase}: it can still be canceled`);
      await leaveSettings(container);
      assert.equal(props(lineButton(container, SIGN_IN)).disabled, true, `${phase}: the line`);
      await React.act(async () => { await props(lineButton(container, SIGN_IN)).onClick(); });
      await openPopover(container);
      assert.equal(props(inPopover(container, SIGN_IN)).disabled, true, `${phase}: the popover`);
      await React.act(async () => { await props(inPopover(container, SIGN_IN)).onClick(); });
      assert.deepEqual(issued(calls, 'oauth_start'), [], phase);
    });
  }
});

test('mounted: the App line an attempt left is retired once a later attempt of the same action for the same Codex process goes through', async () => {
  const refuse = new Set(['oauth_start']);
  await mountedApp(READINGS['no-account'], async ({container, calls}) => {
    await pressInPopover(container, SIGN_IN);
    assert.match(container.textContent, /oauth_start: Error: invented refusal/);
    refuse.delete('oauth_start');
    await React.act(async () => { await props(nodes(dialogOf(navigatorOf(container)), 'button').find(b => b.textContent === SIGN_IN)).onClick(); });
    assert.equal(issued(calls, 'oauth_start').length, 2);
    assert.doesNotMatch(container.textContent, /oauth_start: Error/, 'retired by the attempt that went through');
  }, refuse);
  // A sign-in declined at its confirmation did not go through: the earlier line stays.
  const declining = new Set(['oauth_start']);
  await mountedApp(READINGS['no-account'], async ({container}) => {
    await pressInPopover(container, SIGN_IN);
    declining.delete('oauth_start');
    await React.act(async () => { await props(nodes(dialogOf(navigatorOf(container)), 'button').find(b => b.textContent === SIGN_IN)).onClick(); });
    assert.match(container.textContent, /oauth_start: Error: invented refusal/, 'a declined attempt retires nothing');
    assert.ok(nodes(group(dialogOf(navigatorOf(container)), 'Account'), 'p').some(p => p.textContent === 'Sign-in was not started.'));
  }, declining, {}, {oauth_start: {state: 'native start confirmation dismissed; no sign-in RPC'}});
});
