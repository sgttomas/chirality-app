import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';
import {chatInput, inSetting, inView, sendButton, settingButton, settingsLine} from './support/conversation-view.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// The conversation in the centre: the agent's prose, the turn's bubbles and folded activity, the composer in each turn
// state, and the settings line. Invented fixtures in the host's shapes (native_items.rs, conversation_transport.rs,
// codex_level.rs); no command is issued.
const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {AgentProse, PersonText, proseBlocks} = loadSrc('AgentText');
const {NativeActivityView, turnSegments} = loadSrc('NativeActivity');
const {ConversationPanel} = loadSrc('App');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const nodes = (container, tag) => container.querySelectorAll(node => node.localName === tag);
const RLO = '‮', ZWSP = '​';

// ---- The prose renderer ----
// Elements the renderer may make, and the attributes each may carry; anything else is a failure.
const PROSE_ELEMENTS = new Set(['div', 'p', 'strong', 'em', 'code', 'pre', 'ul', 'ol', 'li', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'td', 'hr', 'br', 'span']);
const PROSE_CLASSES = /^(agent-prose chat-markdown|agent-prose-[a-z-]+( agent-prose-[a-z-]+)*|agent-text-mark)$/;
function proseElements(raw) {
  const out = [];
  for (const m of raw.matchAll(/<([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[a-zA-Z-]+(?:="[^"]*")?)*)\s*\/?>/g)) {
    out.push({tag: m[1], attributes: [...m[2].matchAll(/([a-zA-Z-]+)(?:="([^"]*)")?/g)].map(a => [a[1], a[2] ?? ''])});
  }
  return out;
}
function assertProseOnly(raw, what) {
  const elements = proseElements(raw);
  assert.ok(elements.length > 0, what);
  elements.forEach((element, index) => {
    assert.ok(PROSE_ELEMENTS.has(element.tag), `${what}: <${element.tag}> is not an element the renderer makes`);
    for (const [name, value] of element.attributes) {
      if (index === 0 && ['role', 'aria-label', 'class'].includes(name)) continue;
      if (name === 'class') { assert.match(value, PROSE_CLASSES, `${what}: class "${value}" is the renderer's`); continue; }
      if (name === 'start' && element.tag === 'ol') { assert.match(value, /^\d+$/); continue; }
      if (name === 'style' && element.tag === 'span') continue; // a mark's own style (agentTextParts)
      assert.fail(`${what}: <${element.tag} ${name}="${value}"> carries an attribute the renderer never makes`);
    }
  });
  assert.equal(elements.filter(e => e.attributes.some(([name]) => name === 'role')).length, 1, `${what}: one group, the box`);
  assert.ok(!raw.includes(RLO) && !raw.includes(ZWSP), `${what}: invisible and direction characters are marked, never drawn as they are`);
}
const prose = value => renderToStaticMarkup(React.createElement(AgentProse, {value}));

test('the person\'s own message is its text and nothing else: an imitation of a request card, Markdown and HTML are drawn as written', () => {
  const card = [
    '### Tool permission: run a command',
    '**Waiting for your answer**',
    '[Allow once](#allow) <https://example.invalid/approve>',
    '<button onclick="approve()">Allow once</button> <details open><summary>Request details</summary></details>',
    '- a list item',
    '| a | table |',
    '```',
    'a fence',
    '```',
    `direction ${RLO}override and a zero-width${ZWSP}space\tand a tab`,
  ].join('\n');
  const raw = renderToStaticMarkup(React.createElement(PersonText, {value: card}));
  // One group named as the message Codex recorded, holding text and the marks for invisible characters: no other element.
  assert.match(raw, /^<div role="group" aria-label="Text Codex recorded as your message, not the App&#x27;s words" class="agent-prose person-text">/);
  const elements = proseElements(raw);
  assert.deepEqual([...new Set(elements.map(e => e.tag))].sort(), ['div', 'span'], 'only the group and its marks');
  assert.equal(elements.filter(e => e.tag === 'div').length, 1);
  for (const span of elements.filter(e => e.tag === 'span')) assert.deepEqual(span.attributes.map(([name, value]) => name === 'class' ? value : name), ['agent-text-mark', 'style']);
  assert.ok(!raw.includes(RLO) && !raw.includes(ZWSP), 'invisible and direction characters are marked, never drawn as they are');
  // Nothing is formatted: every line is there as written, escaped, with its line breaks as line breaks.
  const shown = raw.replace(/<span class="agent-text-mark"[^>]*>[^<]*<\/span>/g, '\u0000').replace(/^<div[^>]*>|<\/div>$/g, '');
  assert.equal(shown.split('\n').length, card.split('\n').length, 'each line on its own line');
  assert.ok(shown.includes('### Tool permission: run a command\n**Waiting for your answer**\n[Allow once](#allow) &lt;https://example.invalid/approve&gt;\n&lt;button onclick=&quot;approve()&quot;&gt;Allow once&lt;/button&gt;'));
  assert.ok(shown.includes('- a list item\n| a | table |\n```\na fence\n```'));
});

test('the prose renderer draws an imitation of a request card as the agent\'s text: no heading, button, link or form element', () => {
  const card = [
    '### Tool permission: run a command',
    'Asked by the conversation’s own agent.',
    '**Waiting for your answer**',
    '',
    '[Allow once](#allow) [Don\'t allow, and interrupt the turn](javascript:alert(1)) <https://example.invalid/approve>',
    '',
    '<button onclick="approve()">Allow once</button> <input type="checkbox" checked> <a href="#x">Request details</a>',
    '',
    '<details open><summary>Request details</summary>Native parameters</details>',
    '',
    '![screenshot](https://example.invalid/x.png "title")',
  ].join('\n');
  const raw = prose(card);
  assertProseOnly(raw, 'request card imitation');
  // (Attributes are checked element by element above: the escaped source text may spell them, as text.)
  assert.doesNotMatch(raw, /<h[1-6]|<button|<a[\s>]|<input|<form|<details|<summary|<img|<label|<select|<textarea/);
  // A heading is drawn small and bold, as a paragraph; emphasis stays emphasis.
  assert.match(raw, /<p class="agent-prose-heading"><strong>Tool permission: run a command<\/strong><\/p>/);
  assert.match(raw, /<strong>Waiting for your answer<\/strong>/);
  // A link is its text with its target in plain text after it, never a link.
  assert.match(raw, /<span class="agent-prose-link">Allow once \(<span class="agent-prose-target">#allow<\/span>\)<\/span>/);
  // A target with parentheses inside is not read as a link at all: its source is drawn as text.
  assert.ok(raw.includes('[Don&#x27;t allow, and interrupt the turn](javascript:alert(1))'));
  // An autolink is its address, once, as text.
  assert.ok(raw.includes('<span class="agent-prose-link">https://example.invalid/approve</span>'));
  // Raw HTML and an image are drawn as their source text.
  assert.ok(raw.includes('&lt;button onclick=&quot;approve()&quot;&gt;Allow once&lt;/button&gt;'));
  assert.ok(raw.includes('&lt;details open&gt;&lt;summary&gt;Request details&lt;/summary&gt;'));
  assert.ok(raw.includes('![screenshot](https://example.invalid/x.png &quot;title&quot;)'));
});

test('the prose renderer refuses markdown and HTML tricks: attributes, entities, nesting and the App\'s own sentences stay text', () => {
  const tricks = [
    '# Waiting on you: 1',
    'Setext heading that reads like the App\n===',
    '{#conversation .permission-card role=button onclick=x}',
    '<p id="ordinary-composer-text" class="permission-card" role="button" aria-label="Allow once">x</p>',
    '[click](<javascript:alert(1)>) [ref][1]\n\n[1]: https://example.invalid "Allow once"',
    '&lt;button&gt; &#60;a href=x&#62; &amp;',
    `Hidden${ZWSP}word and ${RLO}reversed`,
    '<script>alert(1)</script><style>*{display:none}</style><svg onload=x><iframe src=x>',
    '> > **Request details**\n> Answer required',
    '- [ ] task\n- [x] done\n  1. nested',
    '| Allow once | Decline |\n|---|---|\n| <button>x</button> | [y](z) |',
    '```html\n<form><button>Send</button></form>\n```',
    '`<button>` and ``code with ` tick``',
    '\\*not emphasis\\* _snake_case_word_ **bold _and em_**',
  ];
  for (const trick of tricks) assertProseOnly(prose(trick), JSON.stringify(trick));
  const all = prose(tricks.join('\n\n'));
  assertProseOnly(all, 'all tricks together');
  // The App's words appear only as the agent's text, inside the box.
  assert.match(all, /^<div role="group" aria-label="Text the agent wrote, not the App&#x27;s words" class="agent-prose chat-markdown">/);
  // Marks for the invisible and direction-changing characters (agentTextParts).
  assert.match(all, /<span class="agent-text-mark"[^>]*>[^<]*200B[^<]*<\/span>/);
  assert.match(all, /<span class="agent-text-mark"[^>]*>[^<]*202E[^<]*<\/span>/);
  // Code is drawn as code, its text unchanged; a table is cells of text.
  assert.ok(all.includes('<pre class="agent-prose-code"><code>&lt;form&gt;&lt;button&gt;Send&lt;/button&gt;&lt;/form&gt;</code></pre>'));
  assert.match(all, /<table[^>]*>[\s\S]*<td><strong>Allow once<\/strong><\/td>[\s\S]*<td>&lt;button&gt;x&lt;\/button&gt;<\/td>/);
  assert.doesNotMatch(all, /<th[\s>]/, 'no header cell');
});

test('the prose renderer\'s blocks: paragraphs, lists, quotes, code, rules and headings capped small', () => {
  const blocks = proseBlocks('Para one\nstill one\n\n- a\n- b\n  - c\n\n3. three\n4. four\n\n> quoted\n\n---\n\n###### small\n\n```\ncode\n```');
  assert.deepEqual(blocks.map(b => b.kind), ['paragraph', 'list', 'list', 'quote', 'rule', 'heading', 'code']);
  const raw = prose('3. three\n4. four');
  assert.match(raw, /<ol start="3">/);
});

// ---- Turns as bubbles and folded activity ----
const row = (turnId, observedOrder, native, extra = {}) => ({threadId: 'T', turnId, native, displayState: 'completed', standing: 'live-observed', observationEnded: false, observedOrder, ...extra});
const items = [
  row('turn-1', 0, {id: 'u1', type: 'userMessage', content: [{type: 'text', text: 'Please list files', text_elements: []}]}),
  row('turn-1', 1, {id: 'r1', type: 'reasoning', summary: ['thinking'], content: []}),
  row('turn-1', 2, {id: 'c1', type: 'commandExecution', command: 'ls', cwd: '/w', status: 'completed', exitCode: 0, commandActions: []}),
  row('turn-1', 3, {id: 'a1', type: 'agentMessage', text: 'Looking', phase: 'commentary'}),
  row('turn-1', 4, {id: 'a2', type: 'agentMessage', text: 'Here they are', phase: 'final_answer'}),
  row('turn-1', 5, {id: 'f1', type: 'fileChange', status: 'failed', changes: []}, {displayState: 'failed'}),
  row('turn-1', 6, {id: 'x1', type: 'futureTool', raw: 1}, {displayState: 'unknown'}),
];
test('a turn maps to bubbles: the person\'s and the agent\'s messages; failures and unfamiliar items stay at the turn; the rest folds', () => {
  const {segments, folded, atTurn, messages} = turnSegments(items);
  assert.deepEqual(segments.map(s => [s.kind, s.rows.map(r => r.native.id)]), [['you', ['u1']], ['agent', ['a1', 'a2']]]);
  assert.deepEqual(folded.map(r => r.native.id), ['r1', 'c1']);
  assert.deepEqual(atTurn.map(r => r.native.id), ['f1', 'x1']);
  assert.deepEqual(messages.map(r => r.native.id), ['u1', 'a1', 'a2']);
});

const view = (status, extra = {}) => ({supplierStanding: 'unverified-development', limits: [], items, revisions: [], descendants: [],
  turns: [{id: 'turn-1', status, startedAt: 1, items: [], ...(status === 'failed' ? {error: {message: 'Codex ended the turn with an error'}} : {})}], turnRecords: [{threadId: 'T', turnId: 'turn-1'}], ...extra});
const transcript = (v, more = {}) => agentPlain(renderToStaticMarkup(React.createElement(NativeActivityView, {view: v, threadId: 'T', ...more})));
test('the transcript draws "You" and the role the App established, folds the activity, and keeps errors outside the fold', () => {
  const html = transcript(view('failed'), {appRole: {standing: 'app-observed', role: 'HELP_HUMAN'}});
  assert.match(html, /<article class="chat-bubble chat-bubble--operator" data-role="operator" aria-label="Your message"><p class="chat-speaker">You<\/p>/);
  assert.match(html, /<article class="chat-bubble chat-bubble--assistant" data-role="assistant" aria-label="HELP_HUMAN reply"><p class="chat-speaker">HELP_HUMAN<\/p>/);
  // Ended: the fold says "Turn details" and how many items it holds; the turn's error and failed item are outside it.
  const fold = html.match(/<details class="turn-activity">[\s\S]*$/)[0];
  assert.match(fold, /^<details class="turn-activity"><summary><span class="turn-activity-summary">Turn details · 2 actions<\/span><\/summary>/);
  const beforeFold = html.slice(0, html.indexOf('<details class="turn-activity">'));
  assert.match(beforeFold, /<p class="chat-turn-status" role="status" data-turn-outcome="failed">Turn failed<\/p>/);
  assert.match(beforeFold, /<p role="alert">Turn error: ⟦Codex sent: Codex ended the turn with an error⟧<\/p>/);
  assert.match(beforeFold, /id="item-[^"]+"><div><b>File change<\/b>/, 'the failed item is at the turn');
  assert.match(beforeFold, /unfamiliar item/, 'an unfamiliar item is at the turn');
  // With no role the App established, the agent is "Agent".
  assert.match(transcript(view('completed')), /<p class="chat-speaker">Agent<\/p>/);
});

test('a running turn says what it is doing, and "waiting" only while a request of the conversation waits for the person', () => {
  const running = transcript(view('inProgress'));
  assert.match(running, /data-turn-live="true"/);
  assert.match(running, /<details class="turn-activity turn-activity--live"><summary><span class="turn-activity-summary">Working · 2 actions<\/span>/);
  assert.doesNotMatch(running, /Waiting for you|chat-turn-status/, 'no wait and no end claimed');
  assert.match(transcript(view('inProgress'), {waiting: true}), /<p class="chat-runtime-status" data-turn-phase="waiting" role="status">Waiting for you<\/p>/);
  // A completed turn claims no end beyond what the host status says: no status line, the fold says Turn details.
  const done = transcript(view('completed'));
  assert.doesNotMatch(done, /data-turn-live|chat-turn-status|Waiting for you|Working/);
  // Once the App stops receiving from that Codex process, an in-progress turn is not drawn as running.
  const ended = transcript({...view('inProgress'), observationEnded: true});
  assert.doesNotMatch(ended, /data-turn-live/);
  assert.match(ended, /Turn in progress when last observed; the App is no longer receiving from that Codex process, so its outcome is unknown/);
});

// ---- The composer and the settings line (ConversationPanel mounted on its own) ----
const g = {appSession: 's', home: 'h', spawnCounter: 1};
const key = id => JSON.stringify([g, id]);
const noop = async () => {};
const projectPath = '/invented/work/pump-skid';
const host = (over = {}) => ({state: 'ready', generation: g, roleLimits: {account: {roles: []}}, homeRouting: {activeModeHomeClass: 'account'},
  currentAppProjectContext: {reference: projectPath},
  attachmentSelections: {launchAppProjectObservation: {source: 'explicit App launch CHIRALITY_WORKSPACE', nativeRoot: {encoding: 'unix_bytes', bytes: [...new TextEncoder().encode(projectPath)]}}},
  levelDefault: {id: 'edits', origin: 'chosen', recorded: 'recorded', reading: 'not-limited', readingSentence: 'Reading is not limited by this level: the agent can read any file your account can.'},
  threads: [{generation: g, threadId: 'T', model: 'reported-model', modelProvider: 'openai', effortInForce: {state: 'known', effort: 'high'}, appRole: {standing: 'app-observed', role: 'HELP_HUMAN'}, roleRelation: {kind: 'start'}, futureGuidanceNotices: [],
    level: {chosen: {id: 'full', origin: 'chosen', recorded: 'recorded', reading: 'not-limited', readingSentence: 'Reading is not limited by this level: the agent can read any file your account can.'}}}],
  ...over});
const liveTurn = turnId => ({generation: g, threadId: 'T', turnId, nativeTurn: {id: turnId, status: 'inProgress', items: []}});
async function mounted(h, check, extra = {}) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const calls = [];
  const record = name => async (...args) => { calls.push([name, ...args]); };
  try {
    await React.act(async () => root.render(React.createElement(ConversationPanel, {host: h, threadKey: key('T'), setThreadKey: () => {}, answer: noop, runAct: noop,
      send: record('send'), steer: record('steer'), submitAttachments: noop, interrupt: record('interrupt'), checkPlanMode: noop, codexBusy: false, ...extra})));
    await check({container, calls});
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}
const composerButtons = container => nodes(container.querySelectorAll(n => n.localName === 'form' && n.getAttribute('class') === 'chat-input-row')[0], 'button');
const named = button => button.getAttribute('aria-label') ?? button.textContent;

test('the composer offers Send when no turn runs, and while one runs Update (only with a steering target) and Stop', async () => {
  await mounted(host(), async ({container}) => {
    assert.deepEqual(composerButtons(container).map(named), ['Attach files', 'Send text']);
    assert.equal(props(chatInput(container)).placeholder, 'Message HELP_HUMAN…');
    assert.equal(props(sendButton(container)).disabled, true, 'nothing to send yet');
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'Hello'}}));
    assert.equal(props(sendButton(container)).disabled, false);
  });
  // A live turn with no steering target: Stop only (no Update without a target to steer).
  await mounted(host({conversationTurns: [liveTurn('t1')]}), async ({container}) => {
    assert.deepEqual(composerButtons(container).map(named), ['Attach files', 'Send text', 'Stop the running turn']);
    assert.equal(props(composerButtons(container)[2]).disabled, false, 'the one live turn can be stopped');
  });
  // With a steering target: Update and Stop. While a turn runs Enter breaks the line (as on main); Update sends.
  await mounted(host({conversationTurns: [liveTurn('t1')], steeringTargets: [{generation: g, threadId: 'T', target: {generation: g, threadId: 'T', turnId: 't1'}}]}), async ({container, calls}) => {
    assert.deepEqual(composerButtons(container).map(named), ['Attach files', 'Send text', 'Update running turn', 'Stop the running turn']);
    assert.equal(props(chatInput(container)).placeholder, 'Add to the running turn…');
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'Also check tests'}}));
    let prevented = 0;
    await React.act(async () => props(chatInput(container)).onKeyDown({key: 'Enter', shiftKey: false, nativeEvent: {}, preventDefault() { prevented++; }}));
    assert.equal(prevented, 0, 'Enter while a turn runs is left to the field: it breaks the line');
    assert.deepEqual(calls, [], 'Enter while a turn runs sends and steers nothing');
    await React.act(async () => props(composerButtons(container).find(b => named(b) === 'Update running turn')).onClick());
    assert.deepEqual(calls.map(c => c[0]), ['steer'], 'Update adds to the running turn');
    assert.equal(calls[0][3], 't1');
  });
  // Two live turns: Stop is not offered against a guess; the turn is chosen under Conversation tools.
  await mounted(host({conversationTurns: [liveTurn('t1'), liveTurn('t2')]}), async ({container}) => {
    const stop = composerButtons(container).find(b => named(b) === 'Stop the running turn');
    assert.equal(props(stop).disabled, true);
  });
  // No dead control: no Workflows button anywhere in the composer.
  await mounted(host(), async ({container}) => {
    assert.ok(!composerButtons(container).some(b => /Workflow/i.test(named(b))));
  });
});

test('the attach control opens the present attachment selection, which stays mounted while closed', async () => {
  const panel = React.createElement('div', {id: 'workspace-attachments'}, 'Selected text attachments');
  await mounted(host(), async ({container}) => {
    const attach = composerButtons(container).find(b => named(b) === 'Attach files');
    const region = () => container.querySelectorAll(n => n.getAttribute('aria-label') === 'Message attachments')[0];
    assert.ok(region().contains(container.querySelectorAll(n => n.getAttribute('id') === 'workspace-attachments')[0]));
    assert.equal(props(region()).hidden, true);
    await React.act(async () => props(attach).onClick());
    assert.equal(props(region()).hidden, false);assert.equal(props(attach)['aria-expanded'], true);
  }, {attachments: panel});
});

test('the settings line shows the folder, role, mode, access level, model and effort; the level\'s name is in view and its reading sentence is in its panel', async () => {
  await mounted(host({threads: [{...host().threads[0], cwd: projectPath}]}), async ({container}) => {
    const line = settingsLine(container);
    assert.match(line.textContent, /^Working in▱ pump-skid·HELP_HUMAN·Chat/);
    assert.equal(props(settingButton(container, 'Access level'))['aria-label'], 'Access level: Full access. Opens what it allows.', 'its name says what pressing it opens');
    assert.equal(settingButton(container, 'Access level').textContent, 'Full access', 'the level\'s name, and only it, is in view');
    assert.equal(settingButton(container, 'Model').textContent, 'reported-model');
    assert.equal(settingButton(container, 'Reasoning effort').textContent, 'high');
    // The panels are closed; the reading sentence is inside the level's panel, not in view.
    const levelPanel = container.querySelectorAll(n => n.getAttribute('aria-label') === 'Access level' && n.getAttribute('role') === 'dialog')[0];
    assert.equal(props(levelPanel).hidden, true);
    assert.match(levelPanel.textContent, /Reading is not limited by this level/);
    await React.act(async () => props(settingButton(container, 'Access level')).onClick());
    assert.equal(props(levelPanel).hidden, false);
    // Escape closes it.
    await React.act(async () => { for (const [type, listener] of document.listeners.map(l => [l.type, l.listener])) if (type === 'keydown') listener({key: 'Escape'}); });
    assert.equal(props(levelPanel).hidden, true, 'Escape closes the panel');
  });
  // With no project folder the App says so; it never guesses one.
  await mounted(host({currentAppProjectContext: null, attachmentSelections: null}), async ({container}) => {
    assert.match(settingsLine(container).textContent, /^Working inproject folder not established/);
  });
  // One press from the name: what the level allows, where it comes from, that reading is not limited, what allowing a
  // command means at a level that asks, and beside them what was sent and reported, the next-turn note, the project's
  // trust as sent and the lasting rules. Each sentence is the host's (invented here), or the App's own table's.
  const level = {chosen: {id: 'supervised', origin: 'chosen', dimensions: {writes: 'nowhere', network: 'off', asks: 'before-a-command-not-known-safe'},
      originSentence: 'Invented origin sentence.', readingSentence: 'Invented sentence: reading is not limited at any level.', allowing: 'Invented sentence: what allowing a command means.'},
    sent: {levelId: 'supervised', writeResult: 'written'}, agreement: 'agrees', takesEffectSentence: 'Invented sentence: a change takes effect from the next turn.',
    projectTrust: {lines: ['Invented trust line: sent as trusted.'], projectRoot: '/invented/project'}};
  await mounted(host({threads: [{...host().threads[0], level}], codexHomeRules: {appSentence: 'Invented lasting-rules sentence.', homes: []}}), async ({container}) => {
    assert.equal(settingButton(container, 'Access level').textContent, 'Supervised', 'only the name is in view');
    const panel = container.querySelectorAll(n => n.getAttribute('aria-label') === 'Access level' && n.getAttribute('role') === 'dialog')[0];
    assert.equal(props(panel).hidden, true, 'nothing else is in view until it is pressed');
    await React.act(async () => props(settingButton(container, 'Access level')).onClick());
    assert.equal(props(panel).hidden, false);
    const said = panel.textContent;
    for (const words of ['Commands cannot write within the sandbox.', 'Network access is off within the sandbox.', 'Codex asks before a command it does not know to be safe.',
      'Invented origin sentence.', 'Invented sentence: reading is not limited at any level.', 'Invented sentence: what allowing a command means.',
      'Last level sent: Supervised. Written to Codex.', 'Codex\'s report agrees with the level in force.', 'Invented sentence: a change takes effect from the next turn.',
      'Invented trust line: sent as trusted.', 'Lasting rules in this Codex home', 'Invented lasting-rules sentence.'])
      assert.ok(said.includes(words), words);
    // The project root the trust lines refer to is in the same panel, marked as text the App did not write.
    assert.ok(said.includes('/invented/project'), 'the project root of the trust lines is shown with them');
    // The lasting rules are in view in the panel, behind no further disclosure.
    assert.ok(nodes(panel, 'details').length === 0, 'nothing in the one-press panel needs a further press');
    assert.ok(nodes(panel, 'button').some(b => b.textContent === 'Change permission level'), 'the full panel is one press further');
  });
  // In a new chat there is no conversation to report on: nothing is said of what was sent.
  await mounted(host({threads: []}), async ({container}) => {
    const panel = container.querySelectorAll(n => n.getAttribute('aria-label') === 'Access level' && n.getAttribute('role') === 'dialog')[0];
    assert.doesNotMatch(panel.textContent, /Last level sent|Project trust/);
  });
  // A level the App asks the person to choose says so beside its name.
  await mounted(host({threads: [{...host().threads[0], level: {ask: {sentence: 'Choose a level for this conversation.'}}}]}), async ({container}) => {
    assert.match(settingButton(container, 'Access level').textContent, / — choose to continue$/);
  });
});

// ---- The new chat's first message, bound to its press (ConversationPanel with a stubbed start and send) ----
const deferredValue = () => { let resolve; const promise = new Promise(yes => { resolve = yes; }); return {promise, resolve}; };
const g2 = {appSession: 's', home: 'h2', spawnCounter: 2};
const startSettings = (over = {}) => ({role: 'HELP_HUMAN', model: 'chosen-model', blocked: '', rolePanel: null, modelPanel: null, binding: 'settings-1', ...over});
async function newChatPanel(check, {h = host()} = {}) {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const starts = [], sends = [], chosen = [];
  let current = {host: h, threadKey: '', startNew: startSettings()};
  const draw = () => React.createElement(ConversationPanel, {host: current.host, threadKey: current.threadKey, setThreadKey: key => chosen.push(key), answer: noop, runAct: noop,
    steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false,
    startNew: {...current.startNew, start: () => { const d = deferredValue(); starts.push(d); return d.promise; }},
    // The ordinary send command: each call is recorded with its reply, which the test can await.
    send: (...args) => { const reply = Promise.resolve({result: {}}); sends.push({args, reply}); return reply; }});
  const render = async patch => { current = {...current, ...patch}; await React.act(async () => root.render(draw())); };
  // Done when the press has run to its end: the composer is no longer busy (the start and any send settled).
  const settled = async () => { for (let i = 0; i < 5 && props(chatInput(container)).disabled; i++) await React.act(async () => {}); assert.equal(props(chatInput(container)).disabled, false, 'the press has run to its end'); };
  const type = async value => React.act(async () => props(chatInput(container)).onChange({target: {value}}));
  const press = async (handler = props(sendButton(container)).onClick) => React.act(async () => { handler(); });
  const answer = async (i, outcome) => { await React.act(async () => { starts[i].resolve(outcome); await starts[i].promise; }); await settled(); };
  const alerts = () => container.querySelectorAll(n => n.getAttribute('role') === 'alert').map(n => n.textContent);
  try { await render({}); await check({container, render, type, press, answer, settled, starts, sends, chosen, alerts}); }
  finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
}
const VIEW_CHANGED = 'The conversation started, but the view changed before your message was sent. Nothing was sent; your draft stays here.';
const opened = (generation = g, id = 'new') => ({opened: JSON.stringify([generation, id])});

test('the first message is sent only while the press is still current: start confirmed in its generation, then the same source, home, view and draft', async () => {
  // Confirmed and nothing changed: the pressed draft is sent once to the started conversation, and cleared though the
  // new conversation has not rendered as the one shown.
  await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    assert.equal(ui.starts.length, 1);
    await ui.answer(0, opened());
    assert.deepEqual(ui.sends.map(s => s.args), [[g, 'new', 'Hello', undefined, undefined]]);
    await ui.sends[0].reply;
    await ui.settled();
    assert.equal(props(chatInput(ui.container)).value, '', 'the confirmed send cleared the pressed draft');
  });
  // While the start was pending the person chose another conversation: kept, and nothing sent.
  await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    await ui.render({threadKey: key('T')});
    await ui.answer(0, opened());
    assert.deepEqual(ui.sends, [], 'no send was dispatched');
    assert.deepEqual(ui.chosen, [], 'the newer choice is not replaced');
    assert.ok(ui.alerts().includes(VIEW_CHANGED));
    assert.equal(props(chatInput(ui.container)).value, 'Hello');
  });
  // The source was replaced, or the home changed, while the start was pending: nothing sent.
  for (const [what, patch] of [['generation', {host: {...host(), generation: g2, threads: []}}], ['home', {host: {...host(), homeRouting: {activeModeHomeClass: 'api-key'}}}]]) await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    await ui.render(patch);
    await ui.answer(0, opened());
    assert.deepEqual(ui.sends, [], `${what}: no send was dispatched`);
    assert.ok(ui.alerts().includes(VIEW_CHANGED), what);
    assert.equal(props(chatInput(ui.container)).value, 'Hello');
  });
  // The text changed while the start was pending: the newer text is kept and nothing is sent.
  await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    await ui.type('Hello again');
    await ui.answer(0, opened());
    assert.deepEqual(ui.sends, []);
    assert.ok(ui.alerts().includes(VIEW_CHANGED));
    assert.equal(props(chatInput(ui.container)).value, 'Hello again');
  });
  // A reply naming another generation than the one the start was issued for is not a success.
  await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    await ui.answer(0, opened(g2));
    assert.deepEqual(ui.sends, []);
    assert.ok(ui.alerts().includes('The App could not confirm that a new conversation started. If it did start, it is listed on the left. Your message was not sent; your draft stays here.'));
  });
});

test('one press binds the first message through its start and send: a settings edit, a home change still pending, a navigation away and back or a mode change since the press sends nothing', async () => {
  // The person's choices as the parent counts them; the start reports the changes it made itself.
  const own = {settings: 1, navigation: 1};
  const confirmed = {...opened(), own};
  const cases = [
    ['nothing changed but the start\'s own selection and consumption', intent => { intent.settings += 1; intent.navigation += 1; }, true],
    ['a settings edit (the model, provider, entry or role)', intent => { intent.settings += 2; intent.navigation += 1; }, false],
    ['a navigation away and back', intent => { intent.settings += 1; intent.navigation += 3; }, false],
    ['a home change still pending', intent => { intent.settings += 1; intent.navigation += 1; intent.homePending = true; }, false],
    ['a home change', intent => { intent.settings += 1; intent.navigation += 1; intent.home += 1; }, false],
  ];
  for (const [what, during, sent] of cases) {
    const intent = {settings: 4, navigation: 7, home: 2, homePending: false};
    await newChatPanel(async ui => {
      await ui.render({startNew: startSettings({intent: () => ({...intent})})});
      await ui.type('Hello'); await ui.press();
      during(intent);
      await ui.answer(0, confirmed);
      if (sent) assert.deepEqual(ui.sends.map(s => s.args[2]), ['Hello'], what);
      else {
        assert.deepEqual(ui.sends, [], `${what}: conversation_send_text was not issued`);
        assert.ok(ui.alerts().includes(VIEW_CHANGED), what);
        assert.equal(props(chatInput(ui.container)).value, 'Hello', `${what}: the draft stays`);
      }
    });
  }
  // The mode chosen on the settings line after the press: nothing is sent.
  await newChatPanel(async ui => {
    const intent = {settings: 0, navigation: 0, home: 0, homePending: false};
    await ui.render({startNew: startSettings({intent: () => ({...intent})})});
    await ui.type('Hello'); await ui.press();
    intent.settings++; intent.navigation++;
    const plan = ui.container.querySelectorAll(n => n.localName === 'input' && props(n).type === 'radio' && n.parentNode.textContent.includes('Plan (experimental)'))[0];
    await React.act(async () => props(plan).onChange());
    await ui.answer(0, confirmed);
    assert.deepEqual(ui.sends, [], 'conversation_send_text was not issued');
    assert.ok(ui.alerts().includes(VIEW_CHANGED));
  }, {h: host({planMode: {state: 'offered'}})});
});

test('a definite refusal says nothing started; any other rejection says only what is established; a retry is not held', async () => {
  await newChatPanel(async ui => {
    await ui.type('Hello'); await ui.press();
    await ui.answer(0, {failed: 'refusal-words'});
    assert.ok(ui.alerts().includes('The conversation was not started: Reported: refusal-words Your draft stays here; nothing was sent.'));
    // The host's words are boxed beside the App's, never inside a control.
    const alert = ui.container.querySelectorAll(n => n.getAttribute('role') === 'alert')[0];
    const box = alert.querySelectorAll(n => n.getAttribute('aria-label') === "What the host reported about the start, not the App's words")[0];
    assert.ok(box, 'the reason is in a box naming whose words they are');
    for (let n = box; n && n !== alert; n = n.parentNode) assert.notEqual(n.localName, 'button');
    await ui.press();
    assert.equal(ui.starts.length, 2, 'a second start is the person\'s retry, not held');
    await ui.answer(1, {notConfirmed: true, reason: 'unknown-words'});
    assert.ok(ui.alerts().includes('The App could not confirm that a new conversation started: Reported: unknown-words If it did start, it is listed on the left. Your message was not sent; your draft stays here.'));
    assert.deepEqual(ui.sends, []);
  });
});

test('a Send captured before the draft or the new conversation\'s settings changed starts nothing', async () => {
  await newChatPanel(async ui => {
    await ui.type('Hello');
    const stale = props(sendButton(ui.container)).onClick;
    await ui.type('Hello, edited');
    await ui.press(stale);
    assert.equal(ui.starts.length, 0, 'the text changed after the press was captured');
    assert.ok(ui.alerts().some(a => a.startsWith('Not started: that Send belonged to an earlier view, text or choice of settings for the new conversation.')));
  });
  await newChatPanel(async ui => {
    await ui.type('Hello');
    const stale = props(sendButton(ui.container)).onClick;
    await ui.render({startNew: startSettings({model: 'another-model', binding: 'settings-2'})});
    await ui.press(stale);
    assert.equal(ui.starts.length, 0, 'the start settings changed after the press was captured');
    await ui.press();
    assert.equal(ui.starts.length, 1, 'a fresh press starts');
  });
});

test('a new chat is only "no conversation chosen": a chosen conversation that is missing offers no Send, and text from another conversation is said to start a new one', async () => {
  await newChatPanel(async ui => {
    await ui.render({threadKey: key('gone')});
    await ui.type('Hello');
    assert.equal(props(sendButton(ui.container)).disabled, true);
    const line = ui.container.querySelectorAll(n => n.getAttribute('id') === 'ordinary-send-readiness')[0];
    assert.equal(line.textContent, 'The conversation chosen is not available now. Choose a conversation or press New chat. Your draft stays here.');
    assert.ok(inView(line) && line.getAttribute('class') === 'v4-composer-status');
    await React.act(async () => props(chatInput(ui.container)).onKeyDown({key: 'Enter', shiftKey: false, nativeEvent: {}, preventDefault() {}}));
    assert.equal(ui.starts.length, 0, 'nothing is started for a missing conversation');
    assert.equal(settingsLine(ui.container).getAttribute('id'), null, 'the new conversation\'s settings line is not shown');
  });
  await newChatPanel(async ui => {
    await ui.render({threadKey: key('T')});
    await ui.type('Written for T');
    await ui.render({threadKey: ''});
    const note = ui.container.querySelectorAll(n => n.getAttribute('aria-label') === 'Where your text goes')[0];
    assert.equal(note?.textContent, 'Your unsent text was written while another conversation was shown. It is kept; if you send it now it starts a new conversation.');
  });
});

// ---- The composer sends only what main sent ----
const planHost = (last, over = {}) => host({planMode: {state: 'offered'}, requestedModes: last ? [{generation: g, threadId: 'T', mode: last, standing: 'requested'}] : [], ...over});
test('a mode is sent only when the person chose one on the settings line and it differs from the last mode requested', async () => {
  for (const [last, choice, sent, word] of [[null, null, undefined, 'Chat'], [null, 'plan', 'plan', 'Plan'], ['plan', 'plan', undefined, 'Plan'], ['plan', 'chat', 'default', 'Chat'], ['plan', null, undefined, 'Plan'], [null, 'chat', undefined, 'Chat'], ['default', 'plan', 'plan', 'Plan']]) {
    await mounted(planHost(last), async ({container, calls}) => {
      if (choice) {
        const radio = await inSetting(container, React.act, 'Mode', n => n.localName === 'input' && n.parentNode.textContent.startsWith(choice === 'plan' ? ' Plan' : ' Chat'));
        assert.ok(radio, `the ${choice} choice is in the open Mode panel`);
        await React.act(async () => props(radio).onChange({target: {checked: true}}));
      }
      assert.equal(settingButton(container, 'Mode').textContent, word, `last ${last}, chosen ${choice}: the word shown`);
      await React.act(async () => props(chatInput(container)).onChange({target: {value: 'Hello'}}));
      await React.act(async () => { props(sendButton(container)).onClick(); });
      assert.deepEqual(calls.map(c => [c[0], c[4]]), [['send', sent]], `last ${last}, chosen ${choice}: the mode sent`);
    });
  }
});

test('Enter sends and Shift+Enter breaks the line only while no turn runs; Stop targets the chosen or the only live turn', async () => {
  await mounted(host(), async ({container, calls}) => {
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'Hello'}}));
    let prevented = 0;
    await React.act(async () => props(chatInput(container)).onKeyDown({key: 'Enter', shiftKey: true, nativeEvent: {}, preventDefault() { prevented++; }}));
    assert.deepEqual([prevented, calls.length], [0, 0], 'Shift+Enter breaks the line');
    await React.act(async () => props(chatInput(container)).onKeyDown({key: 'Enter', shiftKey: false, nativeEvent: {}, preventDefault() { prevented++; }}));
    assert.deepEqual([prevented, calls.map(c => c[0])], [1, ['send']], 'Enter sends');
  });
  // Two live turns and none chosen: Stop is unavailable and says, in view, to choose one; chosen, it stops that one.
  await mounted(host({conversationTurns: [liveTurn('t1'), liveTurn('t2')]}), async ({container, calls}) => {
    const stop = () => composerButtons(container).find(b => named(b) === 'Stop the running turn');
    assert.equal(props(stop()).disabled, true);
    const note = container.querySelectorAll(n => n.getAttribute('aria-label') === 'Which turn Stop stops')[0];
    assert.equal(note?.textContent, 'Several turns are running here. Choose the one to stop under Conversation tools, in “Interrupt a live turn”.');
    assert.ok(inView(note));
    const select = nodes(container, 'select').find(n => n.parentNode.textContent.startsWith('Observed live turn'));
    await React.act(async () => props(select).onChange({target: {value: 't2'}}));
    assert.equal(props(stop()).disabled, false);
    await React.act(async () => { props(stop()).onClick(); });
    assert.deepEqual(calls.map(c => [c[0], c[3]]), [['interrupt', 't2']]);
  });
  await mounted(host({conversationTurns: [liveTurn('t1')]}), async ({container, calls}) => {
    await React.act(async () => { props(composerButtons(container).find(b => named(b) === 'Stop the running turn')).onClick(); });
    assert.deepEqual(calls.map(c => [c[0], c[3]]), [['interrupt', 't1']], 'the one live turn');
  });
});

test('with attachments selected and their panel closed, the composer says Send sends the text without them', async () => {
  await mounted(host({attachmentSelections: {...host().attachmentSelections, selections: [{selection: {selectionRef: 'sel-1'}}]}}), async ({container}) => {
    const note = () => container.querySelectorAll(n => n.getAttribute('aria-label') === 'Selected attachments')[0];
    assert.equal(note()?.textContent, 'Send sends your text without the selected attachments. To send them, open the attachments (⊕) and use “Send text and ordered attachments”.');
    assert.ok(inView(note()));
    await React.act(async () => props(composerButtons(container).find(b => named(b) === 'Attach files')).onClick());
    assert.equal(note(), undefined, 'with the panel open, its own controls say it');
  });
});

// ---- Landing and reading ----
test('"Working in" names the App\'s folder only where the conversation\'s row reports that folder', async () => {
  await mounted(host({threads: [{...host().threads[0], cwd: '/somewhere/else'}]}), async ({container}) => {
    const line = settingsLine(container);
    assert.match(agentPlain(line.textContent), /^Working inCodex reports another folder: Folder: \/somewhere\/else·/);
    const box = line.querySelectorAll(n => n.getAttribute('aria-label') === "The folder Codex reports for this conversation, not the App's words")[0];
    assert.ok(box, 'the reported folder is marked as Codex\'s text');
    for (let n = box; n && n !== line; n = n.parentNode) assert.notEqual(n.localName, 'button', 'outside any control');
    assert.doesNotMatch(line.textContent, /pump-skid/);
  });
  await mounted(host(), async ({container}) => {
    assert.match(settingsLine(container).textContent, /^Working infolder not reported by Codex·/);
  });
  await mounted(host({threads: [{...host().threads[0], cwd: `${projectPath}/`}]}), async ({container}) => {
    assert.match(settingsLine(container).textContent, /^Working in▱ pump-skid·/, 'the same folder with a trailing separator, as the navigator reads it');
  });
});

test('the model help says where the mode is chosen', async () => {
  await mounted(host(), async ({container}) => {
    const help = await inSetting(container, React.act, 'Model', n => n.getAttribute('id') === 'ordinary-model-help');
    assert.match(help.textContent, /^Applies to your next message, sent with Send in the mode chosen under Mode on this line, and to the plan and default sends under Conversation tools\./);
    assert.doesNotMatch(help.textContent, /controls below/);
  });
});

test('"Waiting for you" marks only the turn a waiting request names, or the one live turn when the request names none', () => {
  const two = {...view('inProgress'), items: [...items, row('turn-2', 7, {id: 'a3', type: 'agentMessage', text: 'Second'})],
    turns: [{id: 'turn-1', status: 'inProgress', startedAt: 1, items: []}, {id: 'turn-2', status: 'inProgress', startedAt: 2, items: []}], turnRecords: [{threadId: 'T', turnId: 'turn-1'}, {threadId: 'T', turnId: 'turn-2'}]};
  const marked = html => [...html.matchAll(/aria-label="Conversation turn (\d)"[\s\S]*?<\/section>/g)].filter(m => m[0].includes('Waiting for you')).map(m => m[1]);
  assert.deepEqual(marked(transcript(two, {waitingTurns: ['turn-2']})), ['2'], 'only the turn the request names');
  assert.deepEqual(marked(transcript(two, {waiting: true})), [], 'a request naming no turn marks none of two live turns');
  assert.deepEqual(marked(transcript(view('inProgress'), {waiting: true})), ['1'], 'a request naming no turn marks the one live turn');
});

test('the transcript follows the latest while the person is at or near its end, and stays where they scrolled to', async () => {
  const more = n => host({nativeView: {...view('completed'), generation: g, home: 'h', items: Array.from({length: n}, (_, i) => row('turn-1', i, {id: `a${i}`, type: 'agentMessage', text: `Message ${i}`}))}});
  await mounted(more(2), async ({container}) => {
    const node = container.querySelectorAll(n => (n.getAttribute('class') ?? '').startsWith('panel-body chat-transcript'))[0];
    let height = 1000;
    Object.defineProperty(node, 'scrollHeight', {configurable: true, get: () => height});
    Object.defineProperty(node, 'clientHeight', {configurable: true, get: () => 200});
    const latest = () => nodes(container, 'button').some(b => b.textContent === 'Latest');
    // Scrolled to the very top: the person is behind, and "Latest" is offered.
    node.scrollTop = 0; await React.act(async () => props(node).onScroll());
    assert.equal(latest(), true);
    node.scrollTop = 790; await React.act(async () => props(node).onScroll());
    assert.equal(latest(), false, 'within 48 pixels of the end counts as at the end');
    height = 1600;
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'a re-render'}}));
    assert.equal(node.scrollTop, 1600, 'what arrived is followed');
    // Scrolled up: what arrives does not move the view, and "Latest" takes the person to the end.
    node.scrollTop = 100; await React.act(async () => props(node).onScroll());
    assert.equal(latest(), true, '"Latest" is offered');
    height = 2400;
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'another re-render'}}));
    assert.equal(node.scrollTop, 100, 'the view stays where the person scrolled to');
    await React.act(async () => { props(nodes(container, 'button').find(b => b.textContent === 'Latest')).onClick(); });
    assert.equal(node.scrollTop, 2400);
    assert.equal(latest(), false);
  });
});

// ---- Requests: one mounted owner through the change of state, who asks in view, a closed summary ----
const outstandingRequest = {recordKind: 'server-request-entry', requestIdentity: 7, generation: g, method: 'item/commandExecution/requestApproval', classification: 'known-answerable', originClass: 'a14',
  nativeParameters: {threadId: 'T', turnId: 'turn-1', itemId: 'c1', command: 'ls', availableDecisions: ['accept', 'decline']}, state: 'outstanding', replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'}};
test('a request keeps one mounted card through its change of state: never foldable while it waits, folded after behind the App\'s words', async () => {
  const withRequest = request => host({serverRequests: [request], nativeView: {...view('inProgress'), generation: g, home: 'h'}});
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const draw = h => React.createElement(ConversationPanel, {host: h, threadKey: key('T'), setThreadKey: () => {}, answer: noop, runAct: noop, send: noop, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false});
  try {
    await React.act(async () => root.render(draw(withRequest(outstandingRequest))));
    const entry = () => container.querySelectorAll(n => (n.getAttribute('class') ?? '').startsWith('v4-request-entry'))[0];
    const card = () => entry().querySelectorAll(n => n.localName === 'article' && (n.getAttribute('class') ?? '').includes('request-card'))[0];
    const toggle = () => entry().querySelectorAll(n => n.localName === 'button' && (n.getAttribute('class') ?? '') === 'v4-request-earlier-toggle')[0];
    const [entryBefore, cardBefore] = [entry(), card()];
    assert.equal(toggle(), undefined, 'a waiting request is never folded');
    assert.ok(inView(card()));
    // Who asks is in view with the question and its answers, not behind "Request details".
    const asker = card().querySelectorAll(n => n.getAttribute('class') === 'request-asker')[0];
    assert.equal(asker.textContent, 'Asked by the conversation’s own agent.');
    assert.ok(inView(asker));
    for (let n = asker; n !== card(); n = n.parentNode) assert.notEqual(n.localName, 'details');
    // Answered, then resolved by Codex with a supplied cause: the same wrapper and card, folded behind the App's words.
    await React.act(async () => root.render(draw(withRequest({...outstandingRequest, state: 'resolved-by-supplier', supplierResolution: {cause: 'supplier-cause-words'}}))));
    assert.equal(entry(), entryBefore, 'the same wrapper element: nothing remounted');
    assert.equal(card(), cardBefore, 'the same card element');
    assert.equal(toggle().textContent, 'Tool permission: run a command · Resolved by Codex before you answered', 'the control holds only the App\'s words');
    assert.equal(props(toggle())['aria-expanded'], false);
    assert.equal(inView(card()), false, 'folded: kept mounted and hidden');
    await React.act(async () => { props(toggle()).onClick(); });
    assert.ok(inView(card()));
    assert.match(card().textContent, /supplier-cause-words|cause: supplier-cause-words/, 'the cause stays on the card');
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
});
test('the earlier-request summary is a closed App sentence for every state: nothing supplied reaches it', () => {
  const {requestStateWords, cardState} = loadSrc('RequestCards');
  const SUPPLIED = 'SUPPLIED-CAUSE';
  for (const state of ['received', 'errored', 'outstanding', 'settling', 'reply-outcome-unknown', 'answered', 'declined', 'settle-write-failed', 'resolved-by-supplier', 'ended-unanswered', 'future-state', undefined]) {
    const request = {...outstandingRequest, state, supplierResolution: {cause: SUPPLIED}, settlement: {origin: {class: SUPPLIED, ruleName: SUPPLIED}}, endContext: SUPPLIED};
    assert.doesNotMatch(requestStateWords(request), new RegExp(SUPPLIED), String(state));
  }
  assert.equal(cardState({state: 'resolved-by-supplier', supplierResolution: {cause: 'plain-cause'}}), 'Resolved by Codex before you answered', 'the card\'s sentence is the closed one; the cause is beside it');
});

// ---- Only the person's own message is drawn as theirs ----
test('the person\'s bubble holds only their own message\'s text; a delegated agent\'s input and non-text input stay marked', () => {
  const input = [{type: 'text', text: 'Please look', text_elements: []}, {type: 'localImage', path: '/invented/shot.png'}];
  const asked = {...view('completed'), items: [row('turn-1', 0, {id: 'u1', type: 'userMessage', content: input}), row('turn-1', 1, {id: 'a1', type: 'agentMessage', text: 'Done'})]};
  const own = renderToStaticMarkup(React.createElement(NativeActivityView, {view: asked, threadId: 'T'}));
  assert.match(own, /<article class="chat-bubble chat-bubble--operator" data-role="operator" aria-label="Your message"><p class="chat-speaker">You<\/p>/);
  const person = own.match(/<div role="group" aria-label="[^"]*" class="agent-prose person-text">([^]*?)<\/div>/)[1];
  assert.equal(person, 'Please look', 'the person\'s text group holds their text only');
  assert.match(agentPlain(own), /⟦A local image reference, as Codex recorded it:\n\{\n  &quot;type&quot;: &quot;localImage&quot;,\n  &quot;path&quot;: &quot;\/invented\/shot\.png&quot;\n\}⟧/, 'the image reference is a marked box labelled by what it is');
  // The conversation shown is one the view holds as a delegated agent's (a descendant of another).
  const delegated = renderToStaticMarkup(React.createElement(NativeActivityView, {view: {...asked, descendants: [{threadId: 'T', parentThreadId: 'P', parentSource: 'collabAgentToolCall.senderThreadId'}]}, threadId: 'T'}));
  assert.doesNotMatch(delegated, /person-text|aria-label="Your message"|<p class="chat-speaker">You<\/p>/, 'nothing is drawn as the person\'s');
  assert.match(delegated, /<article class="chat-bubble chat-bubble--input" data-role="input" aria-label="Input to this agent"><p class="chat-speaker">Input to this agent<\/p>/);
  assert.match(agentPlain(delegated), /⟦Input to this agent:\nPlease look⟧/);
  assert.match(delegated, /aria-label="Input Codex recorded for this delegated agent, not the App&#x27;s words and not your message, 1 line"/);
  assert.match(agentPlain(delegated), /⟦A local image reference, as Codex recorded it:/);
});
test('a descendant\'s input, opened from the conversation, is that agent\'s input, not the person\'s', async () => {
  const v = {...view('completed'), items: [...items, row('turn-c', 0, {id: 'cu', type: 'userMessage', content: [{type: 'text', text: 'Delegated task'}]}, {threadId: 'C'})],
    turns: [...view('completed').turns, {id: 'turn-c', status: 'completed', startedAt: 5, items: []}], turnRecords: [{threadId: 'T', turnId: 'turn-1'}, {threadId: 'C', turnId: 'turn-c'}],
    descendants: [{threadId: 'C', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId'}]};
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  try {
    await React.act(async () => root.render(React.createElement(NativeActivityView, {view: v, threadId: 'T'})));
    await React.act(async () => props(nodes(container, 'select')[0]).onChange({target: {value: 'C'}}));
    const bubbles = container.querySelectorAll(n => n.localName === 'article');
    assert.deepEqual(bubbles.map(b => b.getAttribute('aria-label')), ['Input to this agent', 'Agent reply']);
    assert.equal(container.querySelectorAll(n => (n.getAttribute('class') ?? '').includes('person-text')).length, 0);
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
});

// ---- Who an input is from ----
const raw = (v, more = {}) => renderToStaticMarkup(React.createElement(NativeActivityView, {view: v, threadId: 'T', ...more}));
const bubbleNames = html => [...html.matchAll(/<article class="chat-bubble[^"]*" data-role="[a-z]+" aria-label="([^"]+)"/g)].map(m => m[1]);
test('an input with no text is not the person\'s message: it is marked input, with what it is', () => {
  const v = view('completed', {items: [
    row('turn-1', 0, {id: 'u1', type: 'userMessage', content: [{type: 'text', text: 'Look at this'}]}),
    row('turn-1', 1, {id: 'u2', type: 'userMessage', content: [{type: 'localImage', path: '/invented/shot.png'}]}),
    row('turn-1', 2, {id: 'a1', type: 'agentMessage', text: 'Seen'}),
  ]});
  const html = raw(v);
  assert.deepEqual(bubbleNames(html), ['Your message', 'Input Codex recorded, not text you wrote', 'Agent reply']);
  const input = html.slice(html.indexOf('aria-label="Input Codex recorded, not text you wrote"'), html.indexOf('aria-label="Agent reply"'));
  assert.match(input, /<p class="chat-speaker">Input Codex recorded<\/p>/);
  assert.match(input, /A local image reference, as Codex recorded it:/, 'what it is');
  assert.doesNotMatch(input, /person-text|aria-label="Your message"|with your message/, 'nothing in it is drawn as the person\'s');
});

test('a conversation whose native thread source is a sub-agent\'s shows its input as that agent\'s, before its id is among the descendants', () => {
  const source = {subAgent: {thread_spawn: {parent_thread_id: 'P', depth: 1}}};
  const html = raw(view('completed'), {threadSource: source});
  assert.deepEqual(bubbleNames(html), ['Input to this agent', 'Agent reply']);
  assert.doesNotMatch(html, /person-text|aria-label="Your message"/);
  // A conversation started from the App's own source is the person's.
  assert.deepEqual(bubbleNames(raw(view('completed'), {threadSource: 'appServer'})), ['Your message', 'Agent reply']);
});

test('the App\'s own Continue as request is shown as sent by the App, marked, identified by its handoff record\'s turn, never by its text', () => {
  const v = view('completed', {items: [...items, row('turn-2', 7, {id: 'u9', type: 'userMessage', content: [{type: 'text', text: 'Handoff from conversation T (No role). Invented request text.'}]})],
    turns: [...view('completed').turns, {id: 'turn-2', status: 'completed', startedAt: 2, items: []}], turnRecords: [{threadId: 'T', turnId: 'turn-1'}, {threadId: 'T', turnId: 'turn-2'}]});
  const html = raw(v, {appSentTurns: ['turn-2']});
  assert.deepEqual(bubbleNames(html), ['Your message', 'Agent reply', 'Sent by the App for Continue as, not your message', 'Agent reply']);
  const app = html.slice(html.indexOf('aria-label="Sent by the App for Continue as, not your message"'));
  assert.match(app, /<p class="chat-speaker">Sent by the App for Continue as<\/p>/);
  assert.match(app, /aria-label="The App&#x27;s request for a handoff summary, as Codex recorded it; not your message, 1 line"/, 'marked');
  // The same text in a turn no handoff names is the person's.
  assert.deepEqual(bubbleNames(raw(v)), ['Your message', 'Agent reply', 'Your message', 'Agent reply']);
});

test('the conversation panel names the App\'s Continue as turn from the status\'s open handoff in this conversation and generation', async () => {
  const v = view('completed', {generation: g, home: g.home});
  const handoff = turnId => ({id: 'h1', generation: g, sourceThread: 'T', request: {state: 'sent', turnId}, entries: []});
  for (const [handoffs, expected] of [[[handoff('turn-1')], 'Sent by the App for Continue as, not your message'], [[{...handoff('turn-1'), sourceThread: 'U'}], 'Your message'], [[{...handoff('turn-1'), generation: g2}], 'Your message'], [[], 'Your message']]) {
    await mounted(host({nativeView: v, continueAs: handoffs}), async ({container}) => {
      const first = container.querySelectorAll(n => n.localName === 'article')[0];
      assert.equal(first?.getAttribute('aria-label'), expected, JSON.stringify(handoffs));
    });
  }
});

// ---- A reveal of a Conversation tools target lands on a shown target ----
test('"Change permission level" from the settings line selects the Conversation tools tab before it reveals the level, so the focus lands on a shown target', async () => {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const previousGetById = document.getElementById;
  document.getElementById = id => container.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null;
  const proto = Object.getPrototypeOf(document.createElement('div'));
  const focused = [];
  proto.focus = function () { focused.push({id: this.getAttribute('id'), shown: inView(this)}); };
  const snapshot = host();
  const idle = installIdleNativeWaiting(async command => {
    if (command === 'host_status') return snapshot;
    if (command === 'decision_view') return {rows: []};
    if (command === 'native_confirmation_content') return [];
    throw Error(`Unexpected ${command}`);
  });
  try {
    const {App} = loadSrc('App');
    await React.act(async () => root.render(React.createElement(App)));
    const change = await inSetting(container, React.act, 'Access level', n => n.localName === 'button' && n.textContent === 'Change permission level');
    assert.ok(change);
    await React.act(async () => { props(change).onClick(); });
    const level = focused.filter(f => f.id === 'conversation-level');
    assert.equal(level.length, 1, 'the level is focused once');
    assert.equal(level[0].shown, true, 'it is not hidden when it is focused');
    const tab = nodes(container, 'button').find(b => b.getAttribute('role') === 'tab' && b.getAttribute('aria-selected') === 'true');
    assert.equal(tab?.textContent, 'Conversation tools');
  } finally {
    delete proto.focus; document.getElementById = previousGetById;
    const text = container.textContent; await React.act(() => root.unmount()); document.body.removeChild(container); idle.restore(text);
  }
});

// ---- The prose renderer: bounded, lossless, HTML literal ----
const {PROSE_MAX_DEPTH, PROSE_MAX_INLINE_LINE, PROSE_MAX_CHARS} = loadSrc('AgentText');
// The page's visible text, with each mark read back as the character it stands for.
const visible = raw => raw.replace(/<span class="agent-text-mark"[^>]*>‹U\+([0-9A-F]+)›<\/span>/g, (_, hex) => String.fromCodePoint(parseInt(hex, 16)))
  .replace(/<span class="agent-text-mark"[^>]*>→<\/span>/g, '\t').replace(/<br\/>/g, '\n').replace(/<[^>]+>/g, '')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, '&');
const timed = value => { const t = performance.now(); const raw = prose(value); return {raw, ms: performance.now() - t}; };
test('the prose renderer is bounded: deep quotations and a long line of unclosed emphasis render quickly, nothing lost', () => {
  const deep = '>'.repeat(6000) + ' deep';
  const quoted = timed(deep);
  assert.ok(quoted.ms < 500, `6,000 quotation markers in ${quoted.ms} ms`);
  assert.equal((quoted.raw.match(/<blockquote>/g) ?? []).length, PROSE_MAX_DEPTH, 'nested to the bound, no deeper');
  assert.ok(visible(quoted.raw).includes('>'.repeat(6000 - PROSE_MAX_DEPTH) + ' deep'), 'beyond the bound the line is literal text');
  const emphasis = '*a'.repeat(6000);
  const line = timed(emphasis);
  assert.ok(line.ms < 500, `12,000 characters of unclosed emphasis in ${line.ms} ms`);
  assert.ok(emphasis.length > PROSE_MAX_INLINE_LINE && visible(line.raw).includes(emphasis), 'every character is there, as written');
  assert.doesNotMatch(line.raw, /<em>|<strong>/);
  // A message beyond the size bound is drawn whole in the marked form, as tool output is.
  const large = 'word '.repeat(PROSE_MAX_CHARS / 5 + 1);
  const big = prose(large);
  assert.match(big, /^<div role="group" aria-label="Text the agent wrote, not the App&#x27;s words, 1 line" class="agent-text agent-text-block"/);
  assert.doesNotMatch(big, /agent-prose/);
});

test('the prose renderer keeps what malformed syntax would swallow: invisible lines, cell edges, long rows and fence information', () => {
  const ZWJ = '‍', LRI = '⁦', WJ = '⁠';
  const marks = raw => [...raw.matchAll(/<span class="agent-text-mark"[^>]*>‹U\+([0-9A-F]+)›<\/span>/g)].map(m => m[1]);
  // A line holding only invisible or format characters is a line of text, not a blank line.
  const invisible = prose(`First\n${ZWSP}${WJ}\nSecond`);
  assert.deepEqual(marks(invisible), ['200B', '2060']);
  assert.match(invisible, /^<div[^>]*><p>First<br\/><span[^>]*>‹U\+200B›<\/span><span[^>]*>‹U\+2060›<\/span><br\/>Second<\/p><\/div>$/);
  // Cells keep invisible and direction characters at their edges; a row longer than the header keeps every cell, and no row is padded.
  const table = prose(`| ${ZWSP}a${RLO} | b |\n|---|---|\n| c | d | ${ZWJ}e${LRI} |`);
  assert.deepEqual(marks(table), ['200B', '202E', '200D', '2066']);
  assert.match(visible(table), /e/);
  assert.equal((table.match(/<td>/g) ?? []).length, 5, 'the header\'s two cells and the row\'s three: only the cells supplied, none added');
  // A fence's information string is shown as text, whatever it holds; a plain language name too.
  const fence = prose(`\`\`\`js onclick="x" ${RLO}\ncode\n\`\`\``);
  assert.match(fence, /<p class="agent-prose-code-info">js onclick=&quot;x&quot; <span[^>]*>‹U\+202E›<\/span><\/p><pre class="agent-prose-code"><code>code<\/code><\/pre>/);
  assert.match(prose('```python\nx = 1\n```'), /<p class="agent-prose-code-info">python<\/p>/);
  for (const raw of [invisible, table, fence]) assertProseOnly(raw, 'kept characters');
});

test('the prose renderer draws what looks like an HTML tag as its source text: nothing inside it is formatted', () => {
  const raw = prose('<span title="**Allow**">x</span> and **bold**');
  assert.ok(raw.includes('&lt;span title=&quot;**Allow**&quot;&gt;x&lt;/span&gt;'), 'the tag as written, its emphasis markers kept');
  assert.equal((raw.match(/<strong>/g) ?? []).length, 1, 'only the emphasis outside the tag is formatted');
  assert.ok(prose('<!-- **x** -->').includes('&lt;!-- **x** --&gt;'));
  assertProseOnly(raw, 'html literal');
});

// A seeded generator, so a failure is reproducible.
const seeded = seed => () => { seed |= 0; seed = seed + 0x6d2b79f5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const ALPHABET = ['*', '**', '_', '`', '```', '~~~', '#', '## ', '>', '> ', '-', '- ', '+ ', '1. ', '2) ', '|', '|---|', '[', ']', '(', ')', '![', '\\', '<', '>', '<span title="', '">', '</b>', '<!--', '-->', '<a href=x>', '<https://e.invalid>', ':', '=', '---', '"', "'",
  ' ', '  ', '\t', '\n', '\n\n', '\r\n', 'a', 'b', 'x', 'é', '家', '🙂', '‮', '⁦', '​', '‍', '﻿', ' ', '\u0085', '͏', '︀', '\u{E0100}'];
// The ASCII characters the renderer may take as syntax: punctuation, digits, space, tab, CR, LF.
const SYNTAX = /[\x20-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e0-9\t\r\n]/;
// Syntax characters placed where nothing can make them syntax: inside a code span, a tag or image syntax. Their
// insides hold every ASCII syntax character those forms allow, pipes and emphasis markers included.
const INSIDE = ['|', '*', '**', '_', '#', '-', '+', '\\', '!', '[', '(', '~', '=', ':', '.', '1', ' ', 'a', '家'];
const inert = random => {
  let inside = 'a';
  for (let k = 0, n = 1 + Math.floor(random() * 8); k < n; k++) inside += INSIDE[Math.floor(random() * INSIDE.length)];
  inside += 'z';
  const form = Math.floor(random() * 3);
  // What must be shown, contiguous and whole: a code span's inside; a tag's or an image's whole source.
  return form === 0 ? {source: '`' + inside + '`', shown: inside} : form === 1 ? {source: `<span title="${inside}">`, shown: `<span title="${inside}">`} : {source: `![${inside}](${inside.replace(/[()\s]/g, '')})`, shown: `![${inside}](${inside.replace(/[()\s]/g, '')})`};
};
const count = (chars, c) => chars.filter(d => d === c).length;
test('property: on generated Markdown with its ASCII syntax kept, HTML, tables, line breaks and invisible characters, the output holds only the renderer\'s elements, every character that is not syntax in order and once, no syntax character it was not given, and every code span, tag and image whole', () => {
  const random = seeded(20261119);
  for (let n = 0; n < 400; n++) {
    let input = '';
    const fragments = [];
    // Some inputs are tables, so pipes inside the inert forms meet cell boundaries.
    const table = random() < 0.35;
    if (table) input += '| h | i |\n|---|---|\n| ';
    // Inputs with inert forms keep every other syntax character in their noise, but none that could open or close a
    // code span, a tag or an image around them (a backtick, "<", "!" or a backslash), and tables keep to one row.
    const withInert = table || random() < 0.5;
    const length = 1 + Math.floor(random() * 60);
    for (let i = 0; i < length; i++) {
      if (withInert && random() < 0.15) { const f = inert(random); fragments.push(f); input += ` ${f.source} `; continue; }
      const c = ALPHABET[Math.floor(random() * ALPHABET.length)];
      input += withInert ? (/[`<!\\]/.test(c) ? 'q' : table ? c.replace(/\r?\n/g, ' ') : c) : c;
    }
    const raw = prose(input);
    assertProseOnly(raw, JSON.stringify(input));
    const shownText = visible(raw), shown = [...shownText];
    // Every character that is not ASCII syntax is shown, in order, and none twice.
    assert.deepEqual(shown.filter(c => !SYNTAX.test(c)), [...input].filter(c => !SYNTAX.test(c)), `${JSON.stringify(input)} → ${JSON.stringify(shownText)}`);
    // No syntax character is shown more often than it was supplied (a link's own " (" and ")" aside).
    for (const c of new Set([...input].filter(c => SYNTAX.test(c) && !' ()\n\r\t'.includes(c)))) assert.ok(count(shown, c) <= count([...input], c), `${JSON.stringify(input)}: ${c} shown more often than supplied`);
    // Each code span's inside, each tag and each image is shown whole: none of its characters taken as syntax.
    for (const f of fragments) assert.ok(shownText.includes(f.shown), `${JSON.stringify(input)}: ${JSON.stringify(f.shown)} not shown whole in ${JSON.stringify(shownText)}`);
  }
});

test('a table\'s cells are split only at pipes outside code spans, tags and image syntax, and every character is kept', () => {
  const raw = prose('| `a|b` | <span title="x|y">z</span> | ![p|q](r|s) | e\\|f |\n|---|---|---|---|\n| 1 | 2 | 3 | 4 |');
  assert.equal((raw.match(/<tr>/g) ?? []).length, 2);
  assert.equal((raw.match(/<td>/g) ?? []).length, 8, 'four cells in each row: no pipe inside the code span, tag or image split one');
  const shown = visible(raw);
  for (const whole of ['a|b', '<span title="x|y">z</span>', '![p|q](r|s)', 'e|f']) assert.ok(shown.includes(whole), whole);
  assert.match(raw, /<code>a\|b<\/code>/);
  // An emphasis marker inside a tag or an image is its text, even with an opener before it.
  const em = prose('*a <span title="b*">c* and _d ![e_](f) g_');
  assert.ok(visible(em).includes('<span title="b*">') && visible(em).includes('![e_](f)'), 'the markers inside are kept');
  assert.equal((em.match(/<em>/g) ?? []).length, 2, 'each emphasis closes after the tag or image');
  // A link's brackets are never inside a code span.
  const link = prose('[`a](b`)');
  assert.ok(visible(link).includes('a](b'), 'the code span is whole');
  assert.doesNotMatch(link, /agent-prose-target/);
});

test('the prose renderer bounds the elements it makes: a header of 1,000 cells over 10,000 one-pipe rows renders quickly, only the cells supplied, the rest shown as written', () => {
  const {PROSE_MAX_ELEMENTS, PROSE_REST_LINE} = loadSrc('AgentText');
  const header = '| ' + Array.from({length: 1000}, (_, k) => `h${k}`).join(' | ') + ' |';
  const input = `Intro\n\n${header}\n|${'---|'.repeat(1000)}\n${'|\n'.repeat(10000)}after`;
  const {raw, ms} = timed(input);
  assert.ok(ms < 3000, `rendered in ${ms} ms`);
  assert.ok(raw.includes(PROSE_REST_LINE), 'a line says the rest is shown as written');
  assert.ok((raw.match(/<td>/g) ?? []).length === 0, 'the table that would pass the bound is not drawn as a table');
  assert.match(raw, /<p>Intro<\/p>/, 'the blocks before it are formatted');
  const shown = visible(raw);
  assert.ok(shown.includes('h0') && shown.includes('h999') && shown.includes('after'), 'every cell and the text after it are shown');
  // A table within the bound: only the cells each row supplies.
  const small = prose(`${header}\n|${'---|'.repeat(1000)}\n${'|\n'.repeat(3)}`);
  assert.equal((small.match(/<td>/g) ?? []).length, 1000 + 3, 'the header\'s cells and one cell for each one-pipe row');
  // Many small formatted blocks: the elements drawn formatted stop at the bound, and nothing is lost.
  const many = Array.from({length: 4000}, (_, k) => `**b${k}** *i${k}*`).join('\n\n');
  const big = prose(many);
  const formatted = big.slice(0, big.indexOf(PROSE_REST_LINE));
  assert.ok(big.includes(PROSE_REST_LINE));
  assert.ok((formatted.match(/<[a-z]+[ >\/]/g) ?? []).length <= PROSE_MAX_ELEMENTS, 'no more elements than the bound before the rest');
  assert.ok(visible(big).includes('b0') && visible(big).includes('i3999'));
  assertProseOnly(formatted, 'the formatted part');
});

test('the combining grapheme joiner and variation selectors are marked in the agent\'s prose and the person\'s message; an emoji keeps its one presentation selector', () => {
  const marks = raw => [...raw.matchAll(/‹U\+([0-9A-F]+)›/g)].map(m => m[1]);
  const person = value => renderToStaticMarkup(React.createElement(PersonText, {value}));
  // U+034F, a variation selector after a letter, the supplementary selectors, a selector after a selector, and a
  // selector other than U+FE0E or U+FE0F after an emoji: all marked. The emoji's own U+FE0F, once, is kept.
  const input = 'a͏b x︀ y\u{E0100}\u{E01EF} ❤️ ❤️️ 🙂︁ ☺︎';
  for (const raw of [prose(input), person(input)]) {
    assert.deepEqual(marks(raw), ['034F', 'FE00', 'E0100', 'E01EF', 'FE0F', 'FE01']);
    assert.ok(raw.includes('❤️ <') || raw.includes('❤️'), 'the heart keeps its emoji presentation');
    assert.ok(raw.includes('☺︎'), 'a text presentation selector after an emoji is kept too');
  }
  // Hidden data carried as a run of selectors after one emoji is shown as marks.
  assert.equal(marks(prose('🙂' + '︀︁︂'.repeat(4))).length, 12);
});

test('the speaker\'s label is the strongest text in a bubble: no prose heading or bold is larger or heavier', async () => {
  const {readFileSync} = await import('node:fs');
  const css = readFileSync(new URL('../src/workspace.css', import.meta.url), 'utf8');
  const tail = css.slice(css.lastIndexOf('/* v4 review repairs'));
  assert.match(tail, /\.chat-panel--woven \.chat-bubble \.chat-speaker \{ font-size:13\.5px; font-weight:700; \}/);
  assert.match(tail, /\.agent-prose strong \{ font-weight:600; \}/);
  assert.match(tail, /\.agent-prose p\.agent-prose-heading, \.agent-prose p\.agent-prose-heading--major \{ font-size:13\.5px; \}/);
  assert.match(tail, /\.chat-bubble--assistant \.agent-prose\.chat-markdown \{ padding-left:12px; border-left:2px solid var\(--rule\); \}/, 'the prose has a visible boundary of its own');
  assert.match(tail, /\.agent-prose li, \.agent-prose td \{ white-space:pre-wrap; overflow-wrap:anywhere; \}/, 'list entries and cells wrap as a paragraph does');
});
