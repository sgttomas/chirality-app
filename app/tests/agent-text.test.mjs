import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain, agentBoxNames} from './support/agent-text.mjs';

// Text the App did not write is shown in its own marked box, and nothing in
// it is acted on (unit 1, requirements 2 and 3). Invented material only.
const {AgentText, agentTextShown, agentTextParts} = loadSrc('AgentText');
const ch = code => String.fromCodePoint(code);
const RLO = ch(0x202e), ZWSP = ch(0x200b), NEL = ch(0x85), CSI = ch(0x9b), LSEP = ch(0x2028), BOM = ch(0xfeff), ISOLATE = ch(0x2066), BELL = ch(0x07), CR = ch(0x0d);
const render = props => renderToStaticMarkup(React.createElement(AgentText, props));
// Markup that would read as a control, heading, link or list item, as elements or as roles.
const CONTROL = /<(button|h[1-6]|a|li|ol|ul|input|select|textarea|summary|label)[\s>]|role="(button|link|heading|listitem|menuitem|checkbox|radio|tab|option|switch|textbox|alert|dialog|article)"/;

test('line breaks, tabs, direction overrides, zero-width and control characters are shown, never acted on', () => {
  assert.equal(agentTextShown('one\ntwo'), 'one⏎two', 'a line break');
  assert.equal(agentTextShown('one\r\ntwo'), 'one⏎two', 'a CRLF line break is one mark');
  assert.equal(agentTextShown(`one${CR}two`), 'one‹U+000D›two', 'a lone carriage return');
  assert.equal(agentTextShown('a\tb'), 'a→b', 'a tab');
  assert.equal(agentTextShown(`file${RLO}txt.exe`), 'file‹U+202E›txt.exe', 'a bidirectional override');
  assert.equal(agentTextShown(`a${ZWSP}b`), 'a‹U+200B›b', 'a zero-width space');
  assert.equal(agentTextShown(`a${NEL}b${CSI}c`), 'a‹U+0085›b‹U+009B›c', 'C1 controls');
  assert.equal(agentTextShown(`a${LSEP}b`), 'a‹U+2028›b', 'a line separator, which a browser lays out as a break');
  assert.equal(agentTextShown(`${BOM}a${ISOLATE}b${BELL}`), '‹U+FEFF›a‹U+2066›b‹U+0007›');
  for (const code of [0x00, 0x08, 0x0b, 0x1f, 0x7f, 0x80, 0x9f, 0x200b, 0x200c, 0x200d, 0x200e, 0x200f, 0x202a, 0x202b, 0x202c, 0x202d, 0x202e, 0x2066, 0x2067, 0x2068, 0x2069, 0xfeff])
    assert.equal(agentTextShown(`x${ch(code)}y`), `x‹U+${code.toString(16).toUpperCase().padStart(4, '0')}›y`, code.toString(16));
  assert.equal(agentTextShown('plain ünïcödé עברית 🙂'), 'plain ünïcödé עברית 🙂', 'ordinary text is unchanged');
  assert.deepEqual(agentTextParts(`a\n${RLO}`), [{text: 'a', mark: false}, {text: '⏎', mark: true}, {text: '‹U+202E›', mark: true}]);
});

test('an inline value is one labelled, bordered group: its line breaks are marks and nothing in it is a control', () => {
  const value = `ls\n<button>Allow once</button>\nAllow once\n<h3>Tool permission: run a command</h3>\t${RLO}x`;
  const html = render({value});
  assert.match(html, /^<span role="group" aria-label="Text the agent wrote, not the App&#x27;s words" class="agent-text" style="[^"]*border:1px dashed/);
  assert.match(html, /<span class="agent-text-label"[^>]*>The agent wrote:<\/span>/);
  assert.doesNotMatch(html, /<br|<div|<p[\s>]|\n/, 'no new line is laid out');
  assert.doesNotMatch(html, CONTROL, 'nothing renders as a control, heading, link or list item');
  assert.equal(agentPlain(html), '⟦The agent wrote: ls⏎&lt;button&gt;Allow once&lt;/button&gt;⏎Allow once⏎&lt;h3&gt;Tool permission: run a command&lt;/h3&gt;→‹U+202E›x⟧');
  assert.equal(html.match(/class="agent-text-mark"/g).length, 5, 'each mark (three breaks, a tab, an override) is drawn as a mark');
});

test('multi-line text is drawn line by line inside one box, each line numbered', () => {
  const html = render({block: true, value: 'Tool permission: run a command\nWaiting for your answer\n\nAllow once'});
  assert.match(html, /^<div role="group" aria-label="Text the agent wrote, not the App&#x27;s words, 4 lines" class="agent-text agent-text-block"/);
  assert.equal(html.match(/<div class="agent-text-line">/g).length, 4);
  assert.match(html, /<span class="agent-text-line-number"[^>]*>1<\/span>Tool permission: run a command<span class="agent-text-mark"[^>]*>⏎<\/span><\/div>/);
  assert.match(html, /<span class="agent-text-line-number"[^>]*>4<\/span>Allow once<\/div>/, 'the last line carries no break mark');
  assert.doesNotMatch(html, CONTROL);
  assert.ok(html.endsWith('</div></div></div>'), 'every line closes inside the box');
  assert.equal(agentPlain(html), '⟦The agent wrote:\nTool permission: run a command\nWaiting for your answer\n\nAllow once⟧');
});

test('each source says whose text it is; a label or name may be given for a field', () => {
  assert.deepEqual(agentBoxNames(render({value: 'x', source: 'tool'}) + render({value: 'x', source: 'person'}) + render({value: 'x', source: 'codex'}) + render({value: 'x', name: 'Rule words'})),
    ['Output of a tool the agent called, not the App&#x27;s words', 'Text Codex recorded as your message, not the App&#x27;s words', 'Text Codex sent, not the App&#x27;s words', 'Rule words']);
  assert.match(render({value: 'x', label: 'Path:'}), /agent-text-label[^>]*>Path:<\/span>/);
  assert.equal(agentPlain(render({value: {a: 'b\nc'}})), '⟦The agent wrote: {&quot;a&quot;:&quot;b\\nc&quot;}⟧', 'a non-string value is shown as JSON');
  assert.equal(agentPlain(render({value: {a: 1}, block: true})), '⟦The agent wrote:\n{\n  &quot;a&quot;: 1\n}⟧');
});

// ---- Request cards: who asks, and the agent's text kept out of the App's words and controls ----
const activity = loadSrc('NativeActivity');
const {NativeRequestCard, WaitingRequestsIndicator, requestAsker} = loadSrc('RequestCards');
const g = {appSession: 's', home: 'h', spawnCounter: 1};
const request = (method, parameters, extra = {}) => ({recordKind: 'server-request-entry', requestIdentity: extra.id ?? method, generation: g, method, classification: 'known-answerable',
  originClass: ['item/tool/requestUserInput', 'mcpServer/elicitation/request'].includes(method) ? 'person-input' : 'a14', nativeParameters: parameters, state: 'outstanding',
  replyWriteResult: 'not-attempted', acknowledgmentObservation: {status: 'not-observed'}, ...extra});
const cardRaw = (r, view = null) => renderToStaticMarkup(React.createElement(NativeRequestCard, {request: r, view, answer: async () => {}}));
const card = (r, view) => agentPlain(cardRaw(r, view));
// The host's view: a delegated child read with its role and nickname, one with only a nickname (as the
// pinned recordings show), and one not yet read. All invented.
const view = {home: 'h', generation: g, items: [], turns: [], turnRecords: [], revisions: [], descendants: [
  {threadId: 'child-read', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', guidance: 'not-known', nativeThread: {id: 'child-read', agentRole: 'reviewer', agentNickname: 'Ada'}},
  {threadId: 'child-nick', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', guidance: 'not-known', nativeThread: {id: 'child-nick', agentRole: null, agentNickname: 'Bo'}},
  {threadId: 'child-unread', parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', guidance: 'not-known'},
]};
const command = (threadId, params = {}) => request('item/commandExecution/requestApproval', {threadId, turnId: 'u', itemId: 'i', command: 'ls', cwd: '/w', ...params}, {id: `cmd-${threadId}`});
const askedLine = html => html.match(/<p class="request-asker">([\s\S]*?)<\/p>/)?.[1];

test('who asks: this conversation\'s agent, a delegated agent with the role and name Codex reports, or one not yet read', () => {
  assert.equal(askedLine(card(command('T'), view)), 'Asked by the conversation’s own agent.');
  // The view covers the whole Codex process: a request on another conversation's thread is not this one's.
  assert.equal(askedLine(card(command('U'), view)), 'Asked by the conversation’s own agent.');
  assert.doesNotMatch(card(command('U'), view), /this conversation/);
  assert.equal(askedLine(card(command('child-read'), view)), 'Asked by the delegated agent ⟦Name: Ada⟧, role ⟦Role: reviewer⟧, as Codex reports them.');
  assert.equal(askedLine(card(command('child-unread'), view)), 'Asked by a delegated agent; role and name not reported.');
  assert.equal(askedLine(card(command('child-nick'), view)), 'Asked by the delegated agent ⟦Name: Bo⟧, as Codex reports it; role not reported.', 'a missing role is not inferred');
  // The nickname and role are the agent's text, named as such.
  assert.deepEqual(agentBoxNames(cardRaw(command('child-read'), view)).slice(0, 2), ['Agent nickname as Codex reports it, not the App&#x27;s words', 'Agent role as Codex reports it, not the App&#x27;s words']);
  // Without the host's view of that Codex process, nothing is claimed about who asked.
  assert.equal(askedLine(card(command('child-read'), null)), 'Who asked is not established: this view holds no delegation record from the Codex process that asked.');
  assert.equal(askedLine(card(command('child-read'), {...view, generation: {...g, spawnCounter: 2}})), 'Who asked is not established: this view holds no delegation record from the Codex process that asked.');
  assert.deepEqual(requestAsker('child-read', g, view), {kind: 'delegated', role: 'reviewer', nickname: 'Ada'});
  // A legacy request names its conversation by conversationId.
  assert.equal(askedLine(card(request('execCommandApproval', {conversationId: 'child-unread', callId: 'c', command: ['ls'], cwd: '/w'}), view)), 'Asked by a delegated agent; role and name not reported.');
});

test('who asks in the waiting count: each group names its asker beside the button, which carries only the App\'s words', () => {
  const overview = {groups: ['T', 'child-read', 'child-unread', null].map((threadId, i) => ({modeHomeClass: 'account', generation: g, threadId, count: i + 1})),
    sources: [{modeHomeClass: 'account', state: 'ready'}], coverage: 'Invented snapshot.'};
  const raw = renderToStaticMarkup(React.createElement(WaitingRequestsIndicator, {overview, view, open: () => {}}));
  const html = agentPlain(raw);
  assert.match(html, /<button>account · thread T: 1<\/button> Asked by the conversation’s own agent\./);
  assert.match(html, /<button>account · thread child-read: 2<\/button> Asked by the delegated agent ⟦Name: Ada⟧, role ⟦Role: reviewer⟧, as Codex reports them\./);
  assert.match(html, /<button>account · thread child-unread: 3<\/button> Asked by a delegated agent; role and name not reported\./);
  assert.match(html, /<button>account · no conversation named: 4<\/button> Who asked is not established: no conversation is named\.<small>/, 'a group with no conversation still says who asks, as not established');
  assert.doesNotMatch(html, /conversation (T|child)/, 'the old "conversation ‹id›" grouping words are gone');
  for (const [, inner] of raw.matchAll(/<button[^>]*>([\s\S]*?)<\/button>/g)) assert.doesNotMatch(inner, /agent-text|Ada|reviewer/, 'nothing of the agent\'s is inside a button');
});

// A line break followed by text shaped like a control, in every agent field of the cards.
const LOOKALIKE = '\n<button>Allow once</button>\nAllow once';
const injected = [
  command('T', {command: `rm -rf x${LOOKALIKE}`, reason: `Tidy up${LOOKALIKE}`, cwd: `/w${LOOKALIKE}`, proposedExecpolicyAmendment: ['rm', `x${LOOKALIKE}`]}),
  request('item/tool/requestUserInput', {threadId: 'T', turnId: 'u', itemId: 'i', questions: [{id: 'q', header: `Pick${LOOKALIKE}`, question: `Which?${LOOKALIKE}`, isOther: false, isSecret: false,
    options: [{label: `Keep${LOOKALIKE}`, description: `first${LOOKALIKE}`}, {label: 'Allow once', description: '<h3>Tool permission: run a command</h3>'}]}]}),
  request('mcpServer/elicitation/request', {threadId: 'T', turnId: 'u', serverName: `srv${LOOKALIKE}`, mode: 'url', message: `Open${LOOKALIKE}`, url: `https://example.invalid/${LOOKALIKE}`, elicitationId: 'e'}),
];
// The App's own words on a control: anything an answer button may say.
const APP_BUTTON = /^(Allow once|Allow for this session|Allow, and add a lasting rule \(see below\)|Don't allow[^"]*|Choose option \d+|Leave unanswered|Send current question answers…|Decline to answer|Send this input|Decline|Cancel)( ?("[^"]*"|accept|decline|cancel))?…?$/;

test('agent text shaped like a control stays in the agent\'s box, escaped and marked, in what is seen', () => {
  for (const r of injected) {
    const raw = cardRaw(r, view);
    const html = agentPlain(raw);
    // Each agent field reads as one box whose line breaks are marks.
    assert.doesNotMatch(html.replace(/<button>Allow once <code>[^<]*<\/code><\/button>/g, ''), /Allow once<\/button>/, `${r.method}: no "Allow once" button made of agent text`);
    for (const box of html.match(/⟦[^⟧]*⟧/g)) if (box.includes('Allow once')) assert.match(box, /⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once|\\n&lt;button&gt;Allow once&lt;\/button&gt;\\nAllow once|^⟦Option 2: Allow once⟧$/, `${r.method}: ${box}`);
    assert.doesNotMatch(html.replace(/⟦[^⟧]*⟧/g, ''), /&lt;button&gt;|Keep|Tidy/, `${r.method}: the look-alike appears only inside a box`);
    for (const [, inner] of raw.matchAll(/<button[^>]*>([\s\S]*?)<\/button>/g)) {
      assert.doesNotMatch(inner, /agent-text|&lt;|Keep|Tidy|Pick/, `${r.method}: no agent text in a button: ${inner}`);
      assert.match(inner.replace(/<\/?code>/g, '').replace(/&quot;/g, '"').replace(/&#x27;/g, "'"), APP_BUTTON, `${r.method}: button words are the App's: ${inner}`);
    }
    assert.doesNotMatch(raw.replace(/<h3>[^<]*<\/h3>/, ''), /<h[1-6][\s>]/, `${r.method}: the card has one heading, the App's`);
    assert.match(raw, /<h3>(Tool permission: run a command|Question from the agent|Input request from an MCP server or the agent \(not established\))<\/h3>/);
  }
  const elicitation = card(injected[2], view);
  assert.match(elicitation, /<\/h3><p>MCP server, as named in the request: ⟦Server name: srv⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧<\/p>/, 'the server name leaves the heading');
  const commandCard = card(injected[0], view);
  assert.match(commandCard, /Reason given: ⟦The agent wrote: Tidy up⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/);
  assert.match(commandCard, /<small>The words shown:<\/small> ⟦Rule words: rm x⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/);
});

test('agent text shaped like a control is never presented as a control in the accessibility tree', async () => {
  const {installMiniDom} = await import('./support/mini-dom.mjs');
  const document = installMiniDom();
  const {createRoot} = await import('react-dom/client');
  const CONTROL_TAGS = new Set(['button', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'summary', 'li', 'option', 'select', 'input', 'textarea']);
  const CONTROL_ROLES = /^(button|link|heading|listitem|menuitem|checkbox|radio|tab|option|switch|textbox|dialog|article)$/;
  for (const r of injected) {
    const container = document.createElement('div'); document.body.appendChild(container);
    const root = createRoot(container);
    await React.act(() => root.render(React.createElement(NativeRequestCard, {request: r, view, answer: async () => {}})));
    const elements = container.querySelectorAll(() => true);
    for (const el of elements) {
      const role = el.getAttribute?.('role');
      if (role) assert.doesNotMatch(role, CONTROL_ROLES, `${r.method}: role ${role}`);
      const name = el.getAttribute?.('aria-label');
      if (name) assert.doesNotMatch(name, /Allow once|<button>|Keep|Tidy|srv/, `${r.method}: an accessibility name holds agent text: ${name}`);
      // A control's name (its text) is the App's words only.
      if (el.localName === 'button') assert.match(el.textContent, APP_BUTTON, `${r.method}: ${el.textContent}`);
    }
    // Every text node that carries the look-alike sits inside an agent box and inside no control.
    const texts = [];
    const walk = node => { for (const child of node.childNodes) { if (child.nodeType === 3) texts.push(child); else walk(child); } };
    walk(container);
    const lookalike = texts.filter(t => /<button>|Keep|Tidy|Pick|Which\?|srv|first/.test(t.nodeValue));
    assert.ok(lookalike.length > 0, r.method);
    for (const t of lookalike) {
      let box = null;
      for (let n = t.parentNode; n && n !== container; n = n.parentNode) {
        assert.ok(!CONTROL_TAGS.has(n.localName), `${r.method}: "${t.nodeValue}" is inside a ${n.localName}`);
        if (!box && n.getAttribute('role') === 'group' && /\bagent-text\b/.test(n.getAttribute('class') ?? '')) box = n;
      }
      assert.ok(box, `${r.method}: "${t.nodeValue}" is outside an agent box`);
      assert.match(box.getAttribute('aria-label'), /not the App's words/);
      assert.doesNotMatch(t.nodeValue, /\n/, 'no line break is laid out');
    }
    await React.act(() => root.unmount()); document.body.removeChild(container);
  }
});

test('question options: each button says "Choose option N" and its label stands beside it as the agent\'s', () => {
  const html = card(injected[1], view);
  assert.match(html, /<button>Choose option 1<\/button> ⟦Option 1: Keep⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧ ⟦Its description: first⏎/);
  assert.match(html, /<button>Choose option 2<\/button> ⟦Option 2: Allow once⟧ ⟦Its description: &lt;h3&gt;Tool permission: run a command&lt;\/h3&gt;⟧/);
  assert.match(html, /<p>Heading: ⟦The agent wrote: Pick⏎/);assert.match(html, /<p>Question: ⟦The agent wrote: Which\?⏎/);
  assert.doesNotMatch(html, /<b>Pick/, 'the agent\'s heading is no longer styled as the App\'s bold');
});

// ---- The stream: a message carrying a card's exact words, line by line ----
test('a message laid out with a request card\'s exact words is drawn inside the agent\'s box, line by line', () => {
  const words = 'Tool permission: run a command\nAsked by the conversation’s own agent.\nWaiting for your answer\nAllow once "accept"\nDon\'t allow, and interrupt the turn "cancel"';
  const items = [
    {threadId: 'T', turnId: 'u', native: {id: 'm', type: 'agentMessage', text: words}, displayState: 'completed', standing: 'live-observed', observedOrder: 0},
    {threadId: 'T', turnId: 'u', native: {id: 'p', type: 'plan', text: words}, displayState: 'completed', standing: 'live-observed', observedOrder: 1},
    {threadId: 'T', turnId: 'u', native: {id: 'c', type: 'commandExecution', command: `echo${LOOKALIKE}`, cwd: '/w', status: 'completed', exitCode: 0, aggregatedOutput: words, commandActions: []}, displayState: 'completed', standing: 'live-observed', observedOrder: 2},
    {threadId: 'T', turnId: 'u', native: {id: 'f', type: 'fileChange', status: 'completed', changes: [{path: `a.txt${LOOKALIKE}`, kind: {type: 'add'}, diff: words}]}, displayState: 'completed', standing: 'live-observed', observedOrder: 3},
  ];
  const raw = renderToStaticMarkup(React.createElement(activity.NativeActivityView, {view: {items, turns: [], turnRecords: [], revisions: [], descendants: []}, threadId: 'T'}));
  const html = agentPlain(raw);
  assert.ok(html.includes(`<b>Agent</b>⟦The agent wrote:\n${words.replace(/"/g, '&quot;').replace(/'/g, '&#x27;')}⟧`), 'the message is one box with its lines inside');
  assert.ok(html.includes(`⟦Tool output:\n${words.replace(/"/g, '&quot;').replace(/'/g, '&#x27;')}⟧`), 'command output is one box');
  assert.match(html, /<div>Command: ⟦The agent wrote: echo⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧<\/div>/);
  assert.match(html, /add ⟦Path: a\.txt⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/, 'a file name is the agent\'s, outside the disclosure control');
  assert.doesNotMatch(raw, /<summary>[^<]*a\.txt/, 'the file name is not inside a summary');
  assert.equal(raw.match(/<h3>/g).length, 1, 'the only heading of that level is the App\'s Activity heading');
  assert.doesNotMatch(raw, /<button|<article/, 'nothing in the stream is a card or a control');
  // Every line of the card's words is inside a box that names it as the agent's.
  const boxes = [...raw.matchAll(/<div role="group" aria-label="([^"]*)" class="agent-text agent-text-block"/g)].map(m => m[1]);
  assert.ok(boxes.includes('Text the agent wrote, not the App&#x27;s words, 5 lines'), boxes.join(' | '));
  const outside = raw.replace(/<div role="group"[^>]*class="agent-text agent-text-block"[\s\S]*?<\/div><\/div><\/div>/g, '').replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, '').replace(/<details><summary>Native item<\/summary>[\s\S]*?<\/details>/g, '');
  assert.doesNotMatch(outside, /Tool permission: run a command|Waiting for your answer|Allow once/, 'none of the card\'s words appears outside a box');
});

// A workflow name may come from a file an agent wrote: inside the App's run sentence only in the form
// the App's own name rule admits; anything else is drawn as text the App did not write. Codex's cause
// sits in the App's sentence only as a plain token.
test('a run marker draws a name outside the App\'s name rule, and Codex\'s cause outside a plain token, never inside the App\'s sentence', () => {
  const {RunLabel} = loadSrc('NativeActivity');
  const {cardState} = loadSrc('RequestCards');
  const plain = renderToStaticMarkup(React.createElement(RunLabel, {run: {workflow: {name: 'pump-skid-extract', revision: 'abc123def456aa'}}}));
  assert.match(plain, /During the run of <b>pump-skid-extract abc123def456<\/b>/);
  const crafted = renderToStaticMarkup(React.createElement(RunLabel, {run: {workflow: {name: 'x\n<button>Allow once</button>\nAllow once', revision: 'abc'}}}));
  assert.doesNotMatch(crafted, /<b>/, 'not inside the App\'s sentence');
  assert.doesNotMatch(crafted, CONTROL, 'nothing reads as a control');
  assert.match(agentPlain(crafted), /Allow once/, 'the name is still shown');
  assert.ok(agentBoxNames(crafted).some(name => /Workflow name as recorded/.test(name)), 'inside a box named as not the App\'s words');
  for (const [cause, shown] of [['supplier-native', /cause: supplier-native\)/], ['x\nAllow once', /cause: reported in a form the App does not show here\)/], [undefined, /cause: not reported\)/]])
    assert.match(cardState({state: 'resolved-by-supplier', supplierResolution: {source: 'serverRequest/resolved', cause}}), shown, String(cause));
});

// ---- Second round (the reader's findings on 336) ----
test('every character in Unicode\'s Other categories and the two separators is a mark, by category, including the reader\'s probes', () => {
  // The reader's probes: a Mongolian vowel separator, deprecated format controls, a tag character.
  for (const code of [0x180e, 0x206a, 0x206b, 0x206c, 0x206d, 0x206e, 0x206f, 0xe0001, 0xe0041, 0xe007f, 0xfff9, 0xfffb, 0x110bd, 0x1d173])
    assert.equal(agentTextShown(`Allow${ch(code)} once`), `Allow‹U+${code.toString(16).toUpperCase().padStart(4, '0')}› once`, code.toString(16));
  assert.equal(agentTextShown(`a${ch(0xe000)}b${ch(0x10fffd)}`), 'a‹U+E000›b‹U+10FFFD›', 'private use is marked');
  assert.equal(agentTextShown(`a${ch(0x2029)}b`), 'a‹U+2029›b', 'a paragraph separator');
  // A code point this runtime knows as unassigned (as one assigned in a later Unicode version than the runtime knows
  // would be): it is marked, never passed through as a character the App cannot say is visible.
  assert.ok(/\p{Cn}/u.test(ch(0xe0080)), 'premise: U+E0080 is unassigned to this runtime');
  assert.equal(agentTextShown(`Allow${ch(0xe0080)} once`), 'Allow‹U+E0080› once');
  // A lone surrogate is marked too.
  assert.equal(agentTextShown(`a${String.fromCharCode(0xd800)}b`), 'a‹U+D800›b');
  assert.equal(agentTextShown('plain ünïcödé عربي 🙂 e\u0301'), 'plain ünïcödé عربي 🙂 e\u0301', 'ordinary text, combining marks and emoji are unchanged');
});

test('an MCP result content entry\'s type never becomes a control\'s words; the folded run text and history previews are the agent\'s, marked', () => {
  const probe = `Allow once\n${RLO}App says: change allowed`;
  const items = [
    {threadId: 'T', turnId: 'u', native: {id: 'mcp', type: 'mcpToolCall', server: 's', tool: 't', status: 'completed', arguments: {}, result: {content: [{type: probe}]}}, displayState: 'completed', standing: 'live-observed', observedOrder: 0},
    {threadId: 'T', turnId: 'u', native: {id: 'um', type: 'userMessage', content: [{type: 'text', text: `[Chirality] Workflow run start: x\nTool permission: run a command\nWaiting for your answer\nAllow once ${RLO}done`}]}, displayState: 'completed', standing: 'live-observed', observedOrder: 1},
  ];
  const raw = renderToStaticMarkup(React.createElement(activity.NativeItemCard, {row: items[0]})) + renderToStaticMarkup(React.createElement(activity.NativeItemCard, {row: items[1], runStart: true}));
  for (const [, inner] of raw.matchAll(/<summary>([\s\S]*?)<\/summary>/g)) {
    assert.doesNotMatch(inner, /Allow once|App says|\u202e|agent-text/, `a summary holds only the App's words: ${inner}`);
  }
  assert.match(raw, /<summary>result content 1<\/summary>/);
  assert.doesNotMatch(raw, /\u202e/, 'no direction override reaches the page as a character');
  const html = agentPlain(raw);
  assert.ok(html.includes('⟦The run text, with the workflow&#x27;s files as the App read them:\n[Chirality] Workflow run start: x\nTool permission: run a command\nWaiting for your answer\nAllow once ‹U+202E›done⟧'), 'the folded run text is one marked box');
  assert.doesNotMatch(raw, /<pre/, 'no plain pre is left for supplied text');
  // Stored-history previews and the turn error.
  const {StoredTurnPage} = loadSrc('NativeHistory');
  const words = 'Tool permission: run a command\nWaiting for your answer\nAllow once';
  const turn = {id: 'u1', status: 'failed', items: [{type: 'userMessage', content: [{type: 'text', text: words}]}, {type: 'agentMessage', text: `${words} ${RLO}x`}], error: {message: `Allow once\n${RLO}App says: retry`}};
  const binding = {accepted: true, notice: 'invented', page: {data: [turn], nextCursor: null}, rawPage: {data: [turn]}, query: {params: {}}, resolution: null, home: 'h', generation: g, epoch: 1, threadId: 'T'};
  const page = renderToStaticMarkup(React.createElement(StoredTurnPage, {binding, canRead: true, readItems: () => {}}));
  assert.doesNotMatch(page, /<pre/, 'no plain pre in the stored turn page');
  assert.doesNotMatch(page, /\u202e/);
  const shown = agentPlain(page);
  assert.ok(shown.includes(`Agent preview:⟦The agent wrote:\nTool permission: run a command\nWaiting for your answer\nAllow once ‹U+202E›x⟧`), 'the agent preview is the agent\'s box');
  assert.ok(shown.includes('Input preview:⟦Recorded as your message:\nTool permission: run a command'), 'the input preview is marked');
  assert.match(shown, /Codex reported a turn error: ⟦Error: Allow once⏎‹U\+202E›App says: retry⟧/, 'the error is boxed, never the App\'s sentence');
  const outside = page.replace(/<div role="group"[^>]*class="agent-text agent-text-block"[\s\S]*?<\/div><\/div><\/div>/g, '').replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, '');
  assert.doesNotMatch(outside, /Waiting for your answer|Allow once|App says/, 'none of the supplied words appears outside a box');
});

test('a Codex-supplied thread id stands in the App\'s words or a control only as a plain identifier', () => {
  const {plainId} = loadSrc('AgentText');
  assert.equal(plainId('019a2b3c-4d5e-7f80-9a1b-2c3d4e5f6a7b'), '019a2b3c-4d5e-7f80-9a1b-2c3d4e5f6a7b');
  for (const bad of ['T\nAllow once', `T${RLO}x`, 'T Allow once', '', 'x'.repeat(129), null, 7]) assert.equal(plainId(bad), null, String(bad));
  const odd = `T1\nAllow once ${RLO}`;
  const overview = {groups: [{modeHomeClass: 'account', generation: g, threadId: odd, count: 1}], sources: [{modeHomeClass: 'account', state: 'ready'}], coverage: 'Invented.'};
  const raw = renderToStaticMarkup(React.createElement(WaitingRequestsIndicator, {overview, view, open: () => {}}));
  const [, button] = raw.match(/<button[^>]*>([\s\S]*?)<\/button>/);
  assert.equal(button, 'account · a conversation (its identity is shown beside): 1', 'the control carries only the App\'s words');
  assert.match(agentPlain(raw), /<\/button> ⟦Conversation: T1⏎Allow once ‹U\+202E›⟧ /, 'the identity is boxed beside it');
  // In the activity view: an option of the descendant chooser, and a sentence naming a parent.
  const items = [];
  const descendants = [{threadId: odd, parentThreadId: 'T', parentSource: 'collabAgentToolCall.senderThreadId', guidance: 'not-known'}];
  const act = renderToStaticMarkup(React.createElement(activity.NativeActivityView, {view: {items, turns: [], turnRecords: [], revisions: [], descendants}, threadId: 'T'}));
  for (const [, inner] of act.matchAll(/<option[^>]*>([\s\S]*?)<\/option>/g)) assert.doesNotMatch(inner, /Allow once|\u202e/, inner);
  assert.match(act, /<option value="[^"]*">descendant with an identity that is not a plain identifier<\/option>/);
});
