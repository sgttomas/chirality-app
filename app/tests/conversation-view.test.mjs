import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';
import {chatInput, sendButton, settingButton, settingsLine} from './support/conversation-view.mjs';

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
  // With a steering target: Update and Stop; Enter adds to the running turn.
  await mounted(host({conversationTurns: [liveTurn('t1')], steeringTargets: [{generation: g, threadId: 'T', target: {generation: g, threadId: 'T', turnId: 't1'}}]}), async ({container, calls}) => {
    assert.deepEqual(composerButtons(container).map(named), ['Attach files', 'Send text', 'Update running turn', 'Stop the running turn']);
    assert.equal(props(chatInput(container)).placeholder, 'Add to the running turn…');
    await React.act(async () => props(chatInput(container)).onChange({target: {value: 'Also check tests'}}));
    await React.act(async () => props(chatInput(container)).onKeyDown({key: 'Enter', shiftKey: false, nativeEvent: {}, preventDefault() {}}));
    assert.deepEqual(calls.map(c => c[0]), ['steer'], 'Enter while a turn runs updates it');
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
  await mounted(host(), async ({container}) => {
    const line = settingsLine(container);
    assert.match(line.textContent, /^Working in▱ pump-skid·HELP_HUMAN·Chat/);
    assert.equal(props(settingButton(container, 'Access level'))['aria-label'], 'Access level: Full access');
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
  // A level the App asks the person to choose says so beside its name.
  await mounted(host({threads: [{...host().threads[0], level: {ask: {sentence: 'Choose a level for this conversation.'}}}]}), async ({container}) => {
    assert.match(settingButton(container, 'Access level').textContent, / — choose to continue$/);
  });
});
