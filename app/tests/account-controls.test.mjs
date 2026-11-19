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
const {AccountRow, accountRowWords, accountAction, connectionFacts} = loadSrc('AccountControls');
const {accountReading, DIDNT_SAY} = loadSrc('AccountStatus');
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
const NOT_READY = [
  ['no status yet', undefined, 'Reading connection status…'],
  ['starting', base({state: 'starting'}), 'Codex is starting…'],
  ['stopping', base({state: 'stopping'}), 'Codex is stopping…'],
  ['refused', base({state: 'refused', startRefusalCause: 'busy'}), 'Codex was not started'],
  ['refused for this home', base({state: 'stopped', codexHome: 'h', lastStartRefusal: {reason: 'invented reason', home: 'h'}}), 'Codex was not started'],
  ['exited', base({state: 'exited-unexpectedly'}), 'Codex could not stay connected'],
  ['stopped', base({state: 'stopped'}), 'Codex is not connected'],
  ['absent', base({state: 'absent'}), 'Codex is not connected'],
  ['generation closed', read({answer: chatgpt(), host: base({generationClosed: true})}), 'Codex is not connected'],
];

const noActions = () => ({openSettings() {}, openConnection() {}, async checkAgain() {}, async startSignIn() {}, async signOut() {}});
async function mountRow(host, check, actions = noActions()) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const render = async next => { await React.act(async () => root.render(React.createElement(AccountRow, {host: next, actions}))); };
  try { await render(host); await check({container, render, open: async () => React.act(async () => props(rowOf(container)).onClick())}); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}

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
    ...Object.fromEntries(DIDNT_SAY.map(r => [r, /^Codex is running\. It didn't say whether you're signed in\.$/])),
  };
  const check = async (name, host, heading, action, said) => mountRow(host, async ({container, open}) => {
    assert.equal(dialogOf(container), undefined, `${name}: closed, the popover is not in the document`);
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
  for (const [name, host, title] of NOT_READY) {
    const guidance = connectionWords(connectionFacts(host)).guidance;
    await check(name, host, title, null, new RegExp(`^${guidance.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`));
  }
  // Codex's own message for a failed read, marked as the workspace line marks it.
  await mountRow(READINGS.failed, async ({container, open}) => {
    await open();
    const said = nodes(group(container, 'Account'), 'p').find(p => p.getAttribute('aria-label') === 'What Codex said');
    assert.ok(said && /invented account error/.test(said.textContent));
    assert.ok(said.querySelectorAll(n => /agent-text/.test(n.getAttribute('class') ?? '')).length > 0, 'inside the supplied-text box');
  });
  // A sign-in pending: the panel's present words.
  const pending = {...READINGS['no-account'], homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, phase: 'Pending', mode: 'Browser'}}};
  await mountRow(pending, async ({container, open}) => {
    await open();
    assert.ok(nodes(group(container, 'Account'), 'p').some(p => p.textContent === 'Waiting for sign-in to complete.'));
  });
});

test('each action calls the App\'s present command once, under the present disabled conditions; the App controls close the popover', async () => {
  const calls = [];
  let release;
  const actions = {openSettings: () => calls.push('openSettings'), openConnection: () => calls.push('openConnection'),
    checkAgain: async () => { calls.push('checkAgain'); }, startSignIn: () => { calls.push('startSignIn'); return new Promise(r => { release = r; }); }, signOut: async () => { calls.push('signOut'); }};
  const button = (c, words) => nodes(dialogOf(c), 'button').find(b => b.textContent === words);
  await mountRow(READINGS['no-account'], async ({container, open}) => {
    await open();
    const signIn = button(container, 'Sign in with your ChatGPT account (through Codex)…');
    assert.equal(props(signIn).disabled, false);
    await React.act(async () => props(signIn).onClick());
    assert.equal(props(button(container, 'Sign in with your ChatGPT account (through Codex)…')).disabled, true, 'one at a time');
    await React.act(async () => props(button(container, 'Sign in with your ChatGPT account (through Codex)…')).onClick());
    assert.deepEqual(calls, ['startSignIn']);
    await React.act(async () => release());
    assert.equal(props(button(container, 'Sign in with your ChatGPT account (through Codex)…')).disabled, false);
    assert.ok(dialogOf(container), 'starting a sign-in leaves the popover open');
  }, actions);
  // The present conditions: the account home in use (and a current generation, without which there is no reading and
  // so neither action is offered).
  for (const [name, host, words] of [['no-account in another home', read({answer: null, mode: 'api-key'}), 'Sign in with your ChatGPT account (through Codex)…'],
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
  }, actions);
  await mountRow(READINGS.failed, async ({container, open}) => {
    await open();
    await React.act(async () => props(button(container, 'Check again')).onClick());
  }, actions);
  for (const words of ['Connection and access…', 'Settings & tools…']) {
    await mountRow(READINGS.unread, async ({container, open}) => {
      await open();
      await React.act(async () => props(button(container, words)).onClick());
      assert.equal(dialogOf(container), undefined, `${words} closes the popover`);
    }, actions);
  }
  assert.deepEqual(calls, ['signOut', 'checkAgain', 'openConnection', 'openSettings']);
});

test('the popover opens beside the row and takes focus; Escape returns focus to the row; a press outside or focus leaving closes it', async () => {
  const proto = Object.getPrototypeOf(document.createElement('div'));
  let focused = null;
  proto.focus = function () { focused = this; };
  const listeners = type => document.listeners.filter(l => l.type === type);
  try {
    await mountRow(READINGS['no-account'], async ({container, open}) => {
      await open();
      assert.equal(focused, dialogOf(container), 'the popover takes focus');
      // Escape: closed, focus back on the row.
      await React.act(async () => { for (const {listener} of listeners('keydown')) listener({key: 'Escape', preventDefault() {}}); });
      assert.equal(dialogOf(container), undefined); assert.equal(focused, rowOf(container));
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
      assert.equal(dialogOf(container), undefined, 'a press outside closes it');
      // Focus moving within it keeps it; leaving closes it; focus leaving the window (no next element) keeps it.
      await open();
      const root = container.childNodes[0];
      await React.act(async () => props(root).onBlur({relatedTarget: nodes(dialogOf(container), 'button')[1], currentTarget: root}));
      assert.ok(dialogOf(container));
      await React.act(async () => props(root).onBlur({relatedTarget: null, currentTarget: root}));
      assert.ok(dialogOf(container), 'the window losing focus (a browser opening for sign-in) keeps it');
      await React.act(async () => props(root).onBlur({relatedTarget: elsewhere, currentTarget: root}));
      assert.equal(dialogOf(container), undefined, 'focus leaving closes it');
      document.body.removeChild(elsewhere);
      // The row toggles it.
      await open(); await open();
      assert.equal(dialogOf(container), undefined);
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
  } finally { delete proto.getBoundingClientRect; Object.assign(window, saved); }
});

test('a sign-in that completes while the popover is open closes it; one already complete when it opened does not', async () => {
  const pending = {...READINGS['no-account'], homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, phase: 'Pending', mode: 'Browser'}}};
  const completed = ref => ({...READINGS['chatgpt-account'], homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, observationRef: ref, phase: 'CompletedSuccess', mode: 'Browser', actualWriteObserved: true}}});
  await mountRow(pending, async ({container, open, render}) => {
    await open();
    await render(pending);
    assert.ok(dialogOf(container));
    await render(completed('login-1'));
    assert.equal(dialogOf(container), undefined, 'closed on completion');
    assert.equal(nodes(rowOf(container), 'strong')[0].textContent, 'Signed in', 'the row now says the state');
    await open();
    await render(completed('login-1'));
    assert.ok(dialogOf(container), 'the same completion does not close it again');
  });
  // A sign-in that did not complete keeps it open, so its words and the retry stay reachable.
  await mountRow(pending, async ({container, open, render}) => {
    await open();
    await render({...READINGS['no-account'], homeOAuth: {state: 'source-observed', source: {generation: g, requestIdentity: 31, phase: 'CompletedFailure', mode: 'Browser'}}});
    assert.ok(dialogOf(container));
  });
});

// ---- Through the mounted App: the commands each action issues, and where a failure is said ----
async function mountedApp(initial, check, refuse = new Set()) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container), calls = [];
  const previousGetById = document.getElementById;
  document.getElementById = id => container.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null;
  const idle = installIdleNativeWaiting(async (command, args) => {
    calls.push({command, args});
    if (refuse.has(command)) throw Error('invented refusal');
    if (command === 'host_status') return initial;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    if (command === 'read_home_access') return initial.homeAccess;
    if (command === 'oauth_start' || command === 'logout_home') return {state: 'invented'};
    if (command === 'read_available_models') throw Error('no model list in this test');
    throw Error(`Unexpected command ${command}`);
  });
  try { await React.act(async () => root.render(React.createElement(App))); await check({container, calls}); }
  finally { const text = container.textContent; await React.act(() => root.unmount()); document.body.removeChild(container); idle.restore(text); document.getElementById = previousGetById; }
}
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

test('mounted: a refused sign-in or sign-out is said on the App line in the present words', async () => {
  await mountedApp(READINGS['no-account'], async ({container}) => {
    await pressInPopover(container, 'Sign in with your ChatGPT account (through Codex)…');
    assert.match(container.textContent, /oauth_start: Error: invented refusal/);
  }, new Set(['oauth_start']));
  await mountedApp(READINGS['chatgpt-account'], async ({container}) => {
    await pressInPopover(container, 'Sign out of ChatGPT…');
    assert.match(container.textContent, /logout_home: Error: invented refusal/);
  }, new Set(['logout_home']));
});
