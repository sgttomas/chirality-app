import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
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
    assert.doesNotMatch(html.replace(/<button>Allow once<\/button> <code>[A-Za-z_]+<\/code>/g, ''), /Allow once<\/button>/, `${r.method}: no "Allow once" button made of agent text`);
    for (const box of html.match(/⟦[^⟧]*⟧/g)) if (box.includes('Allow once')) assert.match(box, /⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once|\\n&lt;button&gt;Allow once&lt;\/button&gt;\\nAllow once|^⟦Option 2: Allow once⟧$/, `${r.method}: ${box}`);
    assert.doesNotMatch(html.replace(/⟦[^⟧]*⟧/g, ''), /&lt;button&gt;|Keep|Tidy/, `${r.method}: the look-alike appears only inside a box`);
    for (const [, inner] of raw.matchAll(/<button[^>]*>([\s\S]*?)<\/button>/g)) {
      assert.doesNotMatch(inner, /agent-text|&lt;|Keep|Tidy|Pick/, `${r.method}: no agent text in a button: ${inner}`);
      assert.match(inner.replace(/<\/?code>/g, '').replace(/&quot;/g, '"').replace(/&#x27;/g, "'"), APP_BUTTON, `${r.method}: button words are the App's: ${inner}`);
    }
    assert.doesNotMatch(raw.replace(/<h3 class="permission-card-tool">[^<]*<\/h3>/, ''), /<h[1-6][\s>]/, `${r.method}: the card has one heading, the App's`);
    assert.match(raw, /<h3 class="permission-card-tool">(Tool permission: run a command|Question from the agent|Input request from an MCP server or the agent \(not established\))<\/h3>/);
  }
  const elicitation = card(injected[2], view);
  assert.match(elicitation, /<\/h3>(<span class="permission-card-badge">answer required<\/span>)?<\/header><p>MCP server, as named in the request: ⟦Server name: srv⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧<\/p>/, 'the server name leaves the heading');
  const commandCard = card(injected[0], view);
  assert.match(commandCard, /Reason given: ⟦The agent wrote: Tidy up⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/);
  assert.match(commandCard, /<small>The words shown:<\/small> ⟦Rule words: rm x⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/);
});

// A miniature DOM, not an accessibility engine: it reads each element's role, aria-label and text as drawn.
test('agent text shaped like a control holds no control role, no aria-label and no control element in the drawn card (miniature DOM)', async () => {
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

test('question options: each option\'s control is named "Choose option N" and its label stands beside it as the agent\'s', () => {
  const html = card(injected[1], view);
  // Each option is a radio button named in the App's words; the agent's label and description stand beside it, boxed.
  assert.match(html, /<input type="radio" aria-label="Choose option 1" name="[^"]+"\/><span>⟦Option 1: Keep⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧ ⟦Its description: first⏎/);
  assert.match(html, /<input type="radio" aria-label="Choose option 2" name="[^"]+"\/><span>⟦Option 2: Allow once⟧ ⟦Its description: &lt;h3&gt;Tool permission: run a command&lt;\/h3&gt;⟧/);
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
  const esc = w => w.replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
  // The agent's message, under its label, is one prose box: its lines one paragraph, none a heading or a control.
  const message = html.match(/<p class="chat-speaker">Agent<\/p><div class="v4-agent-message" id="[^"]+">(⟦[^⟧]*⟧)/)?.[1];
  assert.equal(message, `⟦Text the agent wrote, not the App&#x27;s words: <p>${words.split('\n').map(esc).join('<br/>')}</p>⟧`, 'the message is one box with its lines inside');
  assert.ok(html.includes(`⟦Tool output:\n${words.replace(/"/g, '&quot;').replace(/'/g, '&#x27;')}⟧`), 'command output is one box');
  assert.match(html, /<div>Command: ⟦The agent wrote: echo⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧<\/div>/);
  assert.match(html, /add ⟦Path: a\.txt⏎&lt;button&gt;Allow once&lt;\/button&gt;⏎Allow once⟧/, 'a file name is the agent\'s, outside the disclosure control');
  assert.doesNotMatch(raw, /<summary>[^<]*a\.txt/, 'the file name is not inside a summary');
  assert.doesNotMatch(raw, /<h[1-6][\s>]/, 'no heading is made of the agent\'s words');
  assert.doesNotMatch(raw, /<button|<article(?! class="chat-bubble )|permission-card/, 'nothing in the stream is a card or a control (its articles are the speakers\' bubbles)');
  // Every line of the card's words is inside a box that names it as the agent's.
  const boxes = [...raw.matchAll(/<div role="group" aria-label="([^"]*)" class="agent-text agent-text-block"/g)].map(m => m[1]);
  assert.ok(boxes.includes('Text the agent wrote, not the App&#x27;s words, 5 lines'), boxes.join(' | '));
  const outside = raw.replace(/<div role="group"[^>]*class="agent-prose (?:chat-markdown|person-text)">[\s\S]*?<\/div>/g, '').replace(/<div role="group"[^>]*class="agent-text agent-text-block"[\s\S]*?<\/div><\/div><\/div>/g, '').replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, '').replace(/<details><summary>Native item<\/summary>[\s\S]*?<\/details>/g, '');
  assert.doesNotMatch(outside, /Tool permission: run a command|Waiting for your answer|Allow once/, 'none of the card\'s words appears outside a box');
});

// A workflow name may come from a file an agent wrote: inside the App's run sentence only in the form
// the App's own name rule admits; anything else is drawn as text the App did not write. Codex's cause
// sits in the App's sentence only as a plain token.
test('the run label and both run markers draw a name outside the App\'s name rule, a run reference and an end cause boxed, and Codex\'s cause outside a plain token never inside the App\'s sentence', () => {
  const {RunLabel, RunStartMarker, RunEndMarker} = loadSrc('NativeActivity');
  const {cardState} = loadSrc('RequestCards');
  const plain = renderToStaticMarkup(React.createElement(RunLabel, {run: {workflow: {name: 'pump-skid-extract', revision: 'abc123def456aa'}}}));
  assert.match(plain, /During the run of <b>pump-skid-extract abc123def456<\/b>/);
  const crafted = renderToStaticMarkup(React.createElement(RunLabel, {run: {workflow: {name: 'x\n<button>Allow once</button>\nAllow once', revision: 'abc'}}}));
  assert.doesNotMatch(crafted, /<b>/, 'not inside the App\'s sentence');
  assert.doesNotMatch(crafted, CONTROL, 'nothing reads as a control');
  assert.match(agentPlain(crafted), /Allow once/, 'the name is still shown');
  assert.ok(agentBoxNames(crafted).some(name => /Workflow name as recorded/.test(name)), 'inside a box named as not the App\'s words');
  // The two markers: the same name rule, the run reference by the identifier rule, the end cause boxed.
  const hostile = {reference: `run${RLO}x`, workflow: {name: 'x\n<button>Allow once</button>', revision: 'abc'}, lifecycle: {state: 'ended', end: {cause: `ended${RLO}<button>Allow once</button>`}}};
  for (const marker of [RunStartMarker, RunEndMarker]) {
    const raw = renderToStaticMarkup(React.createElement(marker, {run: hostile}));
    assert.doesNotMatch(raw, CONTROL, `${marker.name}: nothing reads as a control`);
    assert.doesNotMatch(raw.replace(/<span role="group"[\s\S]*?<\/span><\/span>/g, ''), new RegExp(`${RLO}|Allow once`), `${marker.name}: nothing supplied outside a box`);
    assert.ok(agentBoxNames(raw).some(name => /Workflow name as recorded/.test(name)) && agentBoxNames(raw).some(name => /Identity|Run reference/.test(name)), `${marker.name}: name and reference boxed`);
  }
  assert.ok(agentBoxNames(renderToStaticMarkup(React.createElement(RunEndMarker, {run: hostile}))).some(name => /Why the run ended/.test(name)), 'the end cause boxed');
  assert.match(renderToStaticMarkup(React.createElement(RunStartMarker, {run: {reference: 'run-1', workflow: {name: 'pump-skid', revision: 'abc123'}}})), /Workflow run started: <b>pump-skid abc123<\/b> \(run <code>run-1<\/code>\)/, 'App-rule names and plain references in the App\'s words');
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

// ---- The sweep: guard 1 ----
// Every preformatted block in the App's source is drawn through AgentText (src/AgentText.tsx), so text an agent, a
// tool, a file or Codex supplies is marked, with its control and format characters shown, wherever the App shows it.
// The rule and the forms it judges are in tests/support/presentation-guard.mjs (preformattedFindings); it covers
// app/src and every subdirectory. An exception is only for an element that draws the App's own literal.
const preformattedExceptions = JSON.parse(readFileSync(new URL('./support/preformatted-guard-exceptions.json', import.meta.url), 'utf8'));
test('guard: no source draws preformatted text outside AgentText; each exception is an App literal, scoped and counted', async () => {
  const {preformattedFailures, exceptionShapeFailures, PREFORMATTED_RULE} = await import('./support/presentation-guard.mjs');
  assert.deepEqual(preformattedFailures(new URL('../src/', import.meta.url), preformattedExceptions), [], 'draw preformatted text with AgentText (block) or RecordedData');
  assert.equal(preformattedExceptions[0].scope, PREFORMATTED_RULE);
  assert.deepEqual(exceptionShapeFailures(preformattedExceptions, {needsWhere: false, bases: ['an App-owned literal vocabulary']}), []);
});
test('guard 1 judges each preformatted form, in a nested directory too, and lists only an App literal', async () => {
  const {preformattedSourceFailures, preformattedFailures} = await import('./support/presentation-guard.mjs');
  const fails = (code, why, name = 'Invented.tsx') => assert.notDeepEqual(preformattedSourceFailures(name, code).failures, [], why);
  const passes = (code, why, listed = []) => assert.deepEqual(preformattedSourceFailures('Invented.tsx', code, listed).failures, [], why);
  fails('export const V = ({ s }: any) => <pre>{s}</pre>;', 'a <pre> element');
  fails('import { createElement } from "react"; export const V = ({ s }: any) => createElement("pre", null, s);', 'createElement("pre")');
  fails('import React from "react"; const T = "pre"; export const V = ({ s }: any) => React.createElement(T, null, s);', 'createElement through a const of "pre"');
  fails('import { createElement } from "react"; export const V = ({ s, t }: any) => createElement(t, null, s);', 'createElement with a tag the guard cannot resolve');
  fails('const ReviewPre = "pre"; export const V = ({ s }: any) => <ReviewPre>{s}</ReviewPre>;', 'an element through an alias of "pre"');
  fails('const A = "pre"; const ReviewPre = A; export const V = ({ s }: any) => <ReviewPre>{s}</ReviewPre>;', 'an alias of an alias');
  fails('export const V = ({ s }: any) => <div style={{whiteSpace:"pre-wrap",fontFamily:"monospace"}}>{s}</div>;', "the reader's styled div");
  fails('export const V = ({ s }: any) => <span style={{"white-space":"pre"}}>{s}</span>;', 'a hyphenated key');
  fails('const box = { whiteSpace: "pre-line" } as const; export const V = ({ s }: any) => <p style={box}>{s}</p>;', 'a const style object');
  fails('const base = { whiteSpace: "pre-wrap" as const }; const box = { ...base, margin: 0 }; export const V = ({ s }: any) => <p style={box}>{s}</p>;', 'a spread of a const style');
  fails('const W = "pre-wrap"; export const V = ({ s }: any) => <p style={{whiteSpace: W}}>{s}</p>;', 'a const whiteSpace value');
  fails('export const V = ({ s, on }: any) => <p style={on ? {whiteSpace:"pre"} : {}}>{s}</p>;', 'one branch of a choice');
  fails('export const V = ({ s, ws }: any) => <p style={{whiteSpace: ws}}>{s}</p>;', 'a whiteSpace that is not a literal');
  fails('export const V = ({ s, k }: any) => <p style={{[k]: "pre"}}>{s}</p>;', 'a style key that is not a literal');
  fails('import { createElement } from "react"; export const V = ({ s }: any) => createElement("div", {style: {whiteSpace: "pre-wrap"}}, s);', 'createElement with a preformatted style');
  // Round two's reader: a const reused in both arms of a choice is not a cycle, and a capitalised parameter is not a
  // component.
  fails('const s = { whiteSpace: "pre-wrap" } as const; export const V = ({ value, flag }: any) => <div style={flag ? s : s}>{value}</div>;', 'the same const style in both arms');
  fails('const s = { whiteSpace: "pre-line" } as const; export const V = ({ value, flag }: any) => <span style={{ ...(flag ? s : s) }}>{value}</span>;', 'the same const style in both arms of a spread');
  fails('export const V = ({ value, flag }: any) => { const P = "pre"; const Tag = flag ? P : P; return <Tag>{value}</Tag>; };', 'the same alias of "pre" in both arms');
  fails('import { createElement } from "react"; export const V = ({ s, Tag }: any) => createElement(Tag, null, s);', 'createElement with a capitalised parameter for a tag');
  passes('import { createElement } from "react"; function Box({ children }: any) { return <div>{children}</div>; } export const V = ({ s }: any) => createElement(Box, null, s);', 'createElement with a declared component');
  passes('import { createElement } from "react"; import { Pretty } from "./Pretty"; export const V = ({ s }: any) => createElement(Pretty, null, s);', 'createElement with an imported component');
  passes('export const V = ({ s }: any) => <p style={{whiteSpace:"nowrap"}}>{s}</p>;', 'another whiteSpace');
  passes('export const V = ({ s, style }: any) => <p style={style}>{s}</p>;', 'a style the guard cannot read as a whole is not judged');
  // An App-literal preformatted element passes only when listed, scoped to its component and counted.
  const literal = 'export const V = () => <p style={{whiteSpace:"pre-wrap"}}>Line one{"\\n"}Line two</p>;';
  const entry = {file: 'Invented.tsx', expr: '<p style={{whiteSpace:"pre-wrap"}}>Line one{"\\n"}Line two</p>', component: 'V', count: 1, basis: 'an App-owned literal vocabulary', reason: 'invented'};
  fails(literal, 'unlisted, even the App\'s literal fails');
  passes(literal, 'listed, the App\'s literal passes', [entry]);
  assert.notDeepEqual(preformattedSourceFailures('Invented.tsx', literal, [{...entry, component: 'W'}]).failures, [], 'outside its named component it is not exempt');
  assert.notDeepEqual(preformattedSourceFailures('Invented.tsx', literal + literal.replace('const V', 'const V2').replace('() =>', '() =>'), [entry]).failures, [], 'another component with the same spelling is not exempt');
  const twice = 'export const V = () => <div><p style={{whiteSpace:"pre-wrap"}}>Line one{"\\n"}Line two</p><p style={{whiteSpace:"pre-wrap"}}>Line one{"\\n"}Line two</p></div>;';
  assert.match(preformattedSourceFailures('Invented.tsx', twice, [entry]).failures.join('\n'), /lists 1 occurrence\(s\) and matches 2/, 'an extra occurrence fails');
  const supplied = 'export const V = ({ s }: any) => <p style={{whiteSpace:"pre-wrap"}}>{s}</p>;';
  assert.notDeepEqual(preformattedSourceFailures('Invented.tsx', supplied, [{...entry, expr: '<p style={{whiteSpace:"pre-wrap"}}>{s}</p>'}]).failures, [], 'a listing on a supplied value is not an exception');
  // A file in a nested subdirectory is read, and a stale listing fails.
  const {mkdtempSync, mkdirSync, writeFileSync, rmSync} = await import('node:fs');
  const {join} = await import('node:path');
  const {tmpdir} = await import('node:os');
  const {pathToFileURL} = await import('node:url');
  const dir = mkdtempSync(join(tmpdir(), 'guard1-'));
  try {
    mkdirSync(join(dir, 'deep', 'er'), {recursive: true});
    writeFileSync(join(dir, 'AgentText.tsx'), 'export const X = ({ s }: any) => <span style={{whiteSpace:"pre-wrap"}}>{s}</span>;');
    writeFileSync(join(dir, 'deep', 'er', 'Nested.tsx'), 'export const V = ({ s }: any) => <div style={{whiteSpace:"pre-wrap"}}>{s}</div>;');
    const found = preformattedFailures(pathToFileURL(dir + '/'), []);
    assert.equal(found.length, 1, found.join('\n'));
    assert.match(found[0], /^deep\/er\/Nested\.tsx:1 \(d\)/, 'the nested file fails; AgentText.tsx itself is not judged');
    assert.match(preformattedFailures(pathToFileURL(dir + '/'), [{...entry, file: 'deep/er/Gone.tsx'}]).join('\n'), /stale exception/);
  } finally { rmSync(dir, {recursive: true, force: true}); }
});

test('the repaired preformatted sites box a supplied value: a review\'s scalar and path, an action response and an observation limit', () => {
  const {WorkflowRegistrationReview} = loadSrc('WorkflowRegistrationReview');
  const review = renderToStaticMarkup(React.createElement(WorkflowRegistrationReview, {presentation: {message: `Waiting for your answer\nAllow once${RLO}`, entries: []}}));
  assert.doesNotMatch(review, /\u202e/, 'no live override');
  assert.doesNotMatch(review, /<span style="white-space:pre-wrap/, 'no raw preformatted span');
  assert.match(agentPlain(review), /Value as reported: ⟦?Waiting for your answer⏎Allow once‹U\+202E›/, 'the scalar is boxed, its line break and override marked');
  const {ActionFeedback} = loadSrc('ActionFeedback');
  const plain = renderToStaticMarkup(React.createElement(ActionFeedback, {message: `cmd: failed\nAllow once${RLO}`}));
  assert.doesNotMatch(plain, /\u202e/);
  assert.match(plain, /class="agent-text"/, 'a plain response is boxed');
  const technical = renderToStaticMarkup(React.createElement(ActionFeedback, {message: `cmd: {"state":"Allow once${RLO}"}`}));
  assert.doesNotMatch(technical, /\u202e/);
  assert.match(agentPlain(technical), /state: .*Allow once‹U\+202E›/, 'a reported field is boxed beside its key');
});

test('a recorded dump is marked, with a plain label true of App-only and mixed dumps alike', () => {
  const {RecordedData, RECORDED_DATA_LABEL} = loadSrc('AgentText');
  assert.equal(RECORDED_DATA_LABEL, 'Recorded data (JSON):');
  const raw = renderToStaticMarkup(React.createElement(RecordedData, {value: {cause: `ended ${RLO}by the person`, note: 'Allow once\nWaiting for your answer'}}));
  assert.match(raw, /^<div role="group" aria-label="Recorded data, \d+ lines" class="agent-text agent-text-block"/);
  assert.doesNotMatch(raw, /‮/, 'a direction override inside JSON is shown as a mark, not passed through');
  assert.match(agentPlain(raw), /&quot;cause&quot;: &quot;ended ‹U\+202E›by the person&quot;/);
});

// ---- Third round: a chosen option is kept apart from the person's own answer (the second reading's finding 1) ----
test('choosing an option never puts its label in the free-answer field; the field holds only what the person types, and each is sent as given', async () => {
  const {installMiniDom} = await import('./support/mini-dom.mjs');
  const document = installMiniDom();
  const {createRoot} = await import('react-dom/client');
  const label = `UNTRUSTED\n${RLO}Allow once`;
  const q = request('item/tool/requestUserInput', {threadId: 'T', turnId: 'u', itemId: 'i', questions: [{id: 'q', header: 'Pick', question: 'Which?', isOther: true, isSecret: false,
    options: [{label, description: 'first'}, {label: 'Second', description: 'second'}]}]});
  const sent = [];
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
  const button = text => container.querySelectorAll(n => n.localName === 'button' && n.textContent === text)[0];
  // The free-answer field: the question's one text input (its options are radio buttons).
  const field = () => container.querySelectorAll(n => n.localName === 'input' && props(n).type !== 'radio')[0];
  const option = name => container.querySelectorAll(n => n.localName === 'input' && n.getAttribute('aria-label') === name)[0];
  try {
    await React.act(() => root.render(React.createElement(NativeRequestCard, {request: q, view, answer: async (_r, value) => { sent.push(value); return undefined; }})));
    await React.act(() => props(option('Choose option 1')).onChange({target: {checked: true}}));
    assert.equal(props(field()).value, '', 'the free-answer field stays empty');
    const selected = container.querySelectorAll(n => n.localName === 'p' && n.textContent.startsWith('Selected:'))[0];
    assert.match(selected.textContent, /^Selected: option 1 Its label: UNTRUSTED/, 'the choice is said by number, its label beside it');
    assert.ok(selected.querySelectorAll(n => n.getAttribute?.('role') === 'group' && /agent-text/.test(n.getAttribute('class') ?? '')).length === 1, 'the label is boxed');
    assert.ok(!selected.textContent.includes(RLO), 'its direction override is a mark');
    await React.act(() => props(button('Send current question answers…')).onClick());
    assert.deepEqual(sent.at(-1), {answers: {q: {answers: [label]}}}, 'the option is sent with its label exactly as offered');
    // Typing replaces the choice; the field holds the person's text and that is what is sent.
    await React.act(() => props(option('Choose option 2')).onChange({target: {checked: true}}));
    await React.act(() => props(field()).onChange({target: {value: 'my own'}}));
    assert.equal(props(field()).value, 'my own');
    // The Selected line ends with its Leave unanswered control, in the App's words.
    assert.match(container.querySelectorAll(n => n.localName === 'p' && n.textContent.startsWith('Selected:'))[0].textContent, /^Selected: your own answer, in the field above Leave unanswered$/);
    await React.act(() => props(button('Send current question answers…')).onClick());
    assert.deepEqual(sent.at(-1), {answers: {q: {answers: ['my own']}}});
  } finally { await React.act(() => root.unmount()); document.body.removeChild(container); }
});

// ---- The sweep: the controls rule on every other view (the presentation guard's controls mode) ----
const controlsExceptions = JSON.parse(readFileSync(new URL('./support/controls-guard-exceptions.json', import.meta.url), 'utf8'));
test('controls rule on every other view: no failure, and each exception opens with the rule, names its basis, component and count', async () => {
  const {controlsFailures, exceptionShapeFailures} = await import('./support/presentation-guard.mjs');
  assert.deepEqual(controlsFailures(new URL('../src/', import.meta.url), controlsExceptions), []);
  assert.deepEqual(exceptionShapeFailures(controlsExceptions), []);
  const extra = {file: 'ModelChoice.tsx', where: '<button>', expr: 'row.displayName', component: 'AvailableModels', count: 1, basis: 'an App-owned literal vocabulary', reason: 'invented entry for an expression that no longer fails'};
  assert.match(controlsFailures(new URL('../src/', import.meta.url), [...controlsExceptions, extra]).join('\n'), /stale exception ModelChoice\.tsx/, 'a listed expression that no longer fails is stale');
  for (const e of controlsExceptions.slice(1)) assert.doesNotMatch(e.reason, /^(trusted source|Host composed|not agent written)\.?$/i, `${e.file} ${e.expr}: a reason names its producer`);
});
test('controls rule: a same-file helper\'s returned JSX is judged with the caller\'s control; a call the guard cannot follow fails', async () => {
  const {sourceFailures} = await import('./support/presentation-guard.mjs');
  const judge = source => sourceFailures('Invented.tsx', source, [], 'controls').failures;
  const fails = (source, why) => assert.notDeepEqual(judge(source), [], why);
  const passes = (source, why) => assert.deepEqual(judge(source), [], why);
  fails('function words(v: any) { return <span>{v}</span>; } export const x = ({ row }: any) => <button>{words(row.title)}</button>;', "the reader's helper inside a button");
  fails('import { words } from "./Words"; export const x = ({ row }: any) => <button>{words(row.title)}</button>;', 'an imported helper that is not trusted');
  fails('export const x = ({ row, obj }: any) => <button>{obj.render(row.title)}</button>;', 'a method on an object');
  fails('export const x = ({ row, f }: any) => { const g = f; return <button>{g(row.title)}</button>; };', 'a call through a variable');
  fails('export const x = ({ row }: any) => { const label = <span>{row.title}</span>; return <button>{label}</button>; };', 'a const holding JSX with a supplied value');
  fails('function Wrap({ children }: any) { return <button>{children}</button>; } export const x = ({ row }: any) => <Wrap>{row.title}</Wrap>;', 'children drawn inside a control');
  passes('function words() { return <span>Open the file</span>; } export const x = () => <button>{words()}</button>;', 'a same-file helper returning only App literals');
  // The same helper used once outside any control and once inside a button: the ordinary use does not exempt the other.
  const twice = 'function words(v: any) { return <span>{v}</span>; } export const x = ({ row }: any) => <div><p>{words(row.title)}</p><button>{words(row.title)}</button></div>;';
  assert.match(judge(twice).join('\n'), /<button> v \(in words\)/, 'the use inside the button fails');
  passes('function words(v: any) { return <span>{v}</span>; } export const x = ({ row }: any) => <div><p>{words(row.title)}</p></div>;', 'outside a control alone it is not judged by this rule');
  // Round two's reader: a children attribute keeps the element's control context, directly and through a helper.
  fails('export const V = ({ s }: any) => <button children={s} />;', 'a children attribute on a button');
  fails('function words(s: any) { return <span children={s} />; } export const V = ({ s }: any) => <div><p>{words(s)}</p><button>{words(s)}</button></div>;', 'a helper whose JSX carries a children attribute, used outside then inside a button');
  passes('export const V = () => <button children="Open the file" />;', 'a children attribute holding the App\'s literal');
});
test('controls rule: a field value reused as a children attribute on a button fails at every real field-value exception', async () => {
  const {sourceFailures} = await import('./support/presentation-guard.mjs');
  const exceptions = JSON.parse(readFileSync(new URL('./support/controls-guard-exceptions.json', import.meta.url), 'utf8')).filter(e => e.file);
  const fields = exceptions.filter(e => e.where === '@value');
  assert.ok(fields.length >= 30, 'the field-value exceptions are read');
  for (const e of fields) {
    const source = readFileSync(new URL(`../src/${e.file}`, import.meta.url), 'utf8');
    const listed = exceptions.filter(x => x.file === e.file);
    assert.deepEqual(sourceFailures(e.file, source, listed, 'controls').failures, [], `${e.file}: passes as it is`);
    const at = source.indexOf(`value={${e.expr}}`);
    assert.ok(at >= 0, `${e.file}: ${e.expr} is found`);
    const close = source.indexOf('>', at);
    const reused = source.slice(0, close + 1) + `<button children={${e.expr}} />` + source.slice(close + 1);
    assert.notDeepEqual(sourceFailures(e.file, reused, listed, 'controls').failures, [], `${e.file}: ${e.expr} as a button's children attribute fails`);
  }
});
test('controls rule: an exception is scoped to its place, component and count; a field value excepted never names a control', async () => {
  const {sourceFailures} = await import('./support/presentation-guard.mjs');
  const entry = {file: 'Invented.tsx', where: '@value', expr: 'draft', component: 'V', count: 1, basis: 'an editable value permitted in that field', reason: 'invented'};
  const run = (source, listed = [entry]) => sourceFailures('Invented.tsx', source, listed, 'controls').failures;
  const field = 'export function V({ draft }: any) { return <div><textarea value={draft} />';
  assert.deepEqual(run(field + '</div>; }'), [], 'the field value is excepted');
  assert.notDeepEqual(run(field + '<button>{draft}</button></div>; }'), [], 'the same expression as a button\'s text fails');
  assert.notDeepEqual(run('export function V({ draft }: any) { return <button>{draft}</button>; }'), [], 'a field-value exception never matches a button\'s text, even where it is the only use');
  assert.notDeepEqual(run(field + '<input aria-label={draft} /></div>; }'), [], 'and as an accessible name');
  assert.notDeepEqual(run(field + '<button children={draft} /></div>; }'), [], 'and as a button\'s children attribute');
  assert.match(run(field + '<textarea value={draft} /></div>; }').join('\n'), /lists 1 occurrence\(s\) and matches 2/, 'an extra occurrence fails');
  assert.notDeepEqual(run('export function W({ draft }: any) { return <textarea value={draft} />; }'), [], 'outside its component it is not exempt');
});
test('controls rule: a control, heading or naming attribute on any other view holds only App-made forms, and a form never seen fails', async () => {
  const {sourceFailures} = await import('./support/presentation-guard.mjs');
  const judge = (source, name = 'Invented.tsx') => sourceFailures(name, source, [], 'controls').failures;
  const fails = (source, why) => assert.notDeepEqual(judge(source), [], why);
  const passes = (source, why) => assert.deepEqual(judge(source), [], why);
  const imports = 'import { idWords, safeName } from "./AgentText";\n';
  // App-made: literals, choices between them, counts, a .map index, the App-word helpers, a const with an App-made value.
  passes(imports + 'const x = rows.map((row, i) => <button>{busy ? "Reading…" : "Read"} {[...rows].length} {i + 1} {idWords(row.id)} {safeName(row.name)}</button>);', 'App-made forms in a button');
  passes(imports + 'const n = idWords(row.sequence);\nconst LIMIT = 2000;\nconst x = <button>{`Trial ${n}`} {LIMIT}</button>;', 'a const whose value is App-made');
  passes('const x = <button>{a === b && "Chosen"}</button>;', 'a condition is never taken for drawn text');
  passes('const x = <p>{row.title}</p>;', 'outside a control or heading the controls rule does not judge (the page rule does, on the guarded views)');
  // A helper's name alone is not trusted.
  fails('const idWords = (v: any) => v;\nconst x = <button>{idWords(row.title)}</button>;', 'a local function named idWords');
  fails('import { text as idWords } from "./AgentText";\nconst x = <button>{idWords(row.title)}</button>;', 'another function imported as idWords');
  fails('import { idWords } from "./elsewhere";\nconst x = <button>{idWords(row.title)}</button>;', 'idWords from another module');
  // An identifier is judged by its declaration, never its name.
  fails('const n = row.title;\nconst x = <button>{n}</button>;', 'an index-like name holding a supplied value');
  fails('const x = (i: any) => <button>{i}</button>;', 'a parameter named i that is not a .map index');
  fails('let n = "Read";\nconst x = <button>{n}</button>;', 'a let can be reassigned');
  // A supplied value in a control, a heading or a naming attribute fails; so does a box inside a control.
  fails('const x = <button>{agent.text}</button>;', 'in a button');
  fails('const x = <h3>{run.name}</h3>;', 'in a heading');
  fails('const x = <div aria-label={`Run ${run.name}`} />;', 'in an accessible name');
  fails('const x = <label>Pick <select>{rows.map(r => <option key={r.id}>{r.title}</option>)}</select></label>;', 'in an option, checked option by option');
  fails('import { AgentText } from "./AgentText";\nconst x = <summary>Reasoning <AgentText value={v} /></summary>;', 'a box inside a summary');
  fails('const x = <div {...{ title: row.title }} />;', 'a spread carrying a supplied title');
  // A radio button's or checkbox's value is what it submits, never drawn; a text field's value is drawn.
  passes('const x = <input type="radio" value={row.id} />;', 'a radio value');
  fails('const x = <input type={kind} value={row.id} />;', 'an input whose type is not a literal');
  fails('const x = <input value={row.id} />;', 'a text field value');
  // A role attribute is an element's; on a component it is the component's own prop (a conversation role).
  passes('function RoleLimits({ role }: any) { return <p>{role}</p>; }\nconst x = <RoleLimits role={row.role} />;', 'a component\'s role prop');
  fails('const x = <div role={row.kind}>words</div>;', 'an element\'s role not built of literals');
  // An invented form the guard has never seen fails.
  fails('const x = <option>{new Proxy(target, handler)}</option>;', 'a constructed value');
  fails('const x = <label>{await import("x")}</label>;', 'an awaited value');
  fails('const x = <a>{tagged`words`}</a>;', 'a tagged template');
});

// Conversation choices (ConversationChoices, AgentText.tsx): each radio button's label holds the App's words, then the
// title marked inside the label; the attribution is said once per list and, in each name, before the title; the model
// and provider stand beside, boxed, and reach the control only as its description, after the App's attribution.
// Invented identities and titles only.
const choices = loadSrc('AgentText');
const {threadChoices, storedRelation} = loadSrc('presentation');
const UNTRUSTED = `UNTRUSTED\n${RLO}Allow once`;
const renderChoices = (value, over = {}) => renderToStaticMarkup(React.createElement(choices.ConversationChoices, {legend: 'Conversation', group: 'invented', value, chosen: '', onChoose: () => {}, ...over}));
const labelsIn = html => [...html.matchAll(/<label>(.*?)<\/label>/g)].map(m => m[1]);
const attr = (tag, name) => tag.match(new RegExp(` ${name}="([^"]*)"`))?.[1] ?? null;
const unescaped = text => text.replace(/<!-- -->/g, '').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const APP_LABEL = /^ (Conversation [A-Za-z0-9._:-]+…?|Conversation \d+ \(identity shown beside\))(, (child|fork) of (conversation [A-Za-z0-9._:-]+…?|a conversation whose identity is shown beside))?$/;
const invented = [
  {key: 'k1', id: '019a2b3c-0000-7000-8000-000000000001', title: UNTRUSTED, model: `model${RLO}x`, provider: 'invented-provider'},
  {key: 'k2', id: '019a2b3c-0000-7000-8000-000000000002', title: 'Ordinary invented title', model: 'invented-model', provider: 'invented-provider'},
];

// What a choice shows (the label as seen, without the words only its accessible name carries) and what it is named (the
// label's whole text, which is the radio button's accessible name).
const HIDDEN_NAME_WORDS = /<span class="conversation-choice-title-name" style="[^"]*">[^<]*<\/span>/g;
const plainOf = label => unescaped(label.replace(/^<input[^>]*\/>/, '').replace(/<[^>]+>/g, ''));
const shownOf = label => plainOf(label.replace(HIDDEN_NAME_WORDS, ''));
const SHOWN_TITLE = 'UNTRUSTED⏎‹U+202E›Allow once';

test('a conversation choice shows the App\'s words and identifier, then the title in its marked form; its name says who supplied the title, before it', () => {
  const html = renderChoices(invented);
  const labels = labelsIn(html);
  assert.equal(labels.length, 2);
  const [first, second] = labels;
  // What is seen: the App's words first, then the title, marked; no model or provider in the label.
  const shown = shownOf(first);
  const app = shown.slice(0, shown.indexOf(' UNTRUSTED'));
  assert.match(app, APP_LABEL, 'the App\'s words and a plain identifier come first');
  assert.equal(shown, `${app} ${SHOWN_TITLE}`, 'then the title, its line break and override shown as marks');
  assert.match(first, /<span class="conversation-choice-title" style="[^"]*outline:1px dotted[^"]*">UNTRUSTED<span class="agent-text-mark"/, 'the title is set apart from the App\'s words');
  for (const supplied of ['model', 'invented-provider']) assert.ok(!plainOf(first).includes(supplied), `${supplied} is not in the label`);
  // What it is named: the App's words, then the attribution, then the marked title.
  assert.equal(plainOf(first), `${app}, title supplied by Codex: ${SHOWN_TITLE}`);
  assert.equal(plainOf(second).replace(/^ Conversation [^,]+/, ''), ', title supplied by Codex: Ordinary invented title');
  // The list says once, under its legend, whose the titles are.
  assert.match(html, /<fieldset class="conversation-choices"[^>]*><legend>Conversation<\/legend><p class="conversation-choices-attribution"[^>]*><small>The titles shown are supplied by Codex, not the App&#x27;s words\.<\/small><\/p>/);
  assert.equal(html.split('The titles shown are supplied by Codex').length, 2, 'once for the list, not in every row');
  assert.doesNotMatch(renderChoices([{key: 'k', id: 'abc'}]), /The titles shown/, 'no attribution line where no title is shown');
});

test('a title shaped like a control or an App sentence, or carrying an override, is never raw and never first, in what is shown or in the name', () => {
  for (const title of [UNTRUSTED, 'Allow once', 'Conversation 019a2b3c… Ready to send', `${RLO}Deny`, 'Line one\nAllow once']) {
    const html = renderChoices([{key: 'k1', id: '019a2b3c-0000-7000-8000-000000000001', title}]);
    const [label] = labelsIn(html);
    assert.match(shownOf(label), /^ Conversation 019a2b3c…? /, `${JSON.stringify(title)}: the App's words are first in what is shown`);
    assert.ok(plainOf(label).startsWith(' Conversation 019a2b3c') && plainOf(label).includes(', title supplied by Codex: '), `${JSON.stringify(title)}: the name gives the App's words, then the attribution, before the title`);
    assert.ok(plainOf(label).endsWith(`, title supplied by Codex: ${choices.agentTextShown(title)}`), `${JSON.stringify(title)}: the title, marked, comes after the attribution and ends the name`);
    assert.ok(shownOf(label).endsWith(` ${choices.agentTextShown(title)}`), `${JSON.stringify(title)}: the title, marked, ends what is shown`);
    assert.doesNotMatch(html, new RegExp(`\\n|${RLO}`), `${JSON.stringify(title)}: no raw line break or override anywhere in the markup`);
    for (const tag of html.match(/<(input|legend)[\s>][^>]*>/g)) assert.doesNotMatch(attr(tag, 'value') ?? '', /UNTRUSTED|Allow|Deny/, 'no control submits it as a value');
  }
  const html = renderChoices(invented);
  assert.ok(agentPlain(html).includes('⟦Model: model‹U+202E›x⟧ ⟦Provider: invented-provider⟧'), 'model and provider are boxed beside the label, never identifiers');
});

test('the radio button\'s accessible description carries the model, provider and status beside the label, attributed and marked, not the title', () => {
  const description = choices.choiceDescription(invented[0]);
  assert.equal(description, 'Model reported by Codex: model‹U+202E›x. Provider reported by Codex: invented-provider');
  assert.doesNotMatch(description, /UNTRUSTED|Allow once|[\n\r‮]/);
  const radios = renderChoices(invented).match(/<input type="radio"[^>]*\/>/g);
  assert.equal(unescaped(attr(radios[0], 'aria-description')), description, 'the description is on the radio button itself, as aria-description');
  assert.equal(attr(radios[0], 'aria-describedby'), null, 'never a describedby pointing at a supplied value');
  assert.equal(attr(radios[0], 'aria-label'), null, 'its name is its label');
  assert.equal(choices.choiceDescription({key: 'k', id: 'abc', title: 'only a title'}), null, 'nothing beside the label: no description');
  assert.equal(attr(renderChoices([{key: 'k', id: 'abc', title: 't'}]).match(/<input type="radio"[^>]*\/>/)[0], 'aria-description'), null);
});

test('a long title or child prompt is a bounded preview, with how much is shown said in the App\'s words in what is seen and in the name', () => {
  const long = 'Invented child prompt. '.repeat(30);
  const html = renderChoices([{key: 'k', id: 'child-1', title: long, relation: {kind: 'child', id: 'parent-1'}}]);
  const total = [...long].length;
  const head = [...long].slice(0, choices.CHOICE_TITLE_LIMIT).join('');
  const [label] = labelsIn(html);
  assert.equal(shownOf(label), ` Conversation child-1, child of conversation parent-1 ${head} (its first ${choices.CHOICE_TITLE_LIMIT} of ${total} characters)`);
  assert.equal(plainOf(label), ` Conversation child-1, child of conversation parent-1, title supplied by Codex: ${head} (its first ${choices.CHOICE_TITLE_LIMIT} of ${total} characters)`);
  assert.equal(choices.boundedTitle('🙂'.repeat(choices.CHOICE_TITLE_LIMIT + 1)).text, '🙂'.repeat(choices.CHOICE_TITLE_LIMIT), 'cut at whole code points');
});

test('each shortened identity tells its conversation apart from every other in the list, lengthened where a prefix is shared', () => {
  const ids = ['019a2b3c4d5e6f70-aaaa', '019a2b3c4d5e6f70-aaab', '019a2b3c-zzzz', 'abcdefgh', 'abcdefghij', 'abc', 'zzzzzzzzzzzzzzzz'];
  const shown = choices.shortIds(ids);
  assert.deepEqual(shown, ['019a2b3c4d5e6f70-aaaa', '019a2b3c4d5e6f70-aaab', '019a2b3c-…', 'abcdefgh', 'abcdefghi…', 'abc', 'zzzzzzzz…']);
  assert.equal(new Set(shown).size, ids.length, 'no two shown alike');
  shown.forEach((form, i) => {
    const prefix = form.replace(/…$/, '');
    assert.ok(ids[i].startsWith(prefix));
    if (form.endsWith('…')) assert.deepEqual(ids.filter(id => id.startsWith(prefix)), [ids[i]], `${form} names only ${ids[i]}`);
  });
  const repeated = choices.choiceLabels([{key: 'a', id: 'same-identity-1'}, {key: 'b', id: 'same-identity-1'}]);
  assert.notEqual(repeated[0], repeated[1], 'an identity listed twice is told apart by its entry');
  assert.deepEqual(choices.shortIds(['not plain ✱', 42]), [null, '42']);
  assert.deepEqual(choices.choiceLabels([{key: 'a', id: 'not plain ✱'}]), ['Conversation 1 (identity shown beside)']);
  assert.ok(agentPlain(renderChoices([{key: 'a', id: 'not plain ✱'}])).includes('⟦Identity: not plain ✱⟧'), 'an identity that is not plain is boxed beside');
});

test('a child or fork relationship comes from the recorded field, never from the title', () => {
  const parent = {key: 'p', id: '019aaaaa-parent'}, titled = {key: 't', id: '019bbbbb-titled', title: 'child of conversation 019aaaaa-parent'};
  const recorded = {key: 'c', id: '019ccccc-child', title: 'Invented prompt', relation: {kind: 'child', id: '019aaaaa-parent'}};
  const labels = choices.choiceLabels([parent, titled, recorded]);
  assert.equal(labels[1], 'Conversation 019bbbbb…', 'a title saying "child of" makes no relationship');
  assert.equal(labels[2], 'Conversation 019ccccc…, child of conversation 019aaaaa…', 'the recorded parent, by its shortened identity in the list');
  assert.deepEqual(storedRelation({source: {subAgent: {thread_spawn: {parent_thread_id: 'P', depth: 1}}}, preview: 'fork of conversation X'}), {kind: 'child', id: 'P'});
  assert.deepEqual(storedRelation({forkedFromId: 'F', name: 'child of conversation Y'}), {kind: 'fork', id: 'F'});
  assert.equal(storedRelation({name: 'child of conversation Y', preview: 'forked from Z'}), null);
  assert.deepEqual(threadChoices([{threadId: 'T', generation: 1, name: 'child of conversation Q', forkedFrom: {threadId: 'S'}}], row => row.threadId)[0].relation, {kind: 'fork', id: 'S'});
  assert.equal(threadChoices([{threadId: 'T', generation: 1, name: 'fork of conversation Q'}], row => row.threadId)[0].relation, null);
});

test('choosing calls back with the row\'s key; the none choice, the chosen row and a disabled list are as given', () => {
  const chosen = [];
  const tree = choices.ConversationChoices({legend: 'Send to', group: 'g', value: invented, chosen: 'k2', onChoose: key => chosen.push(key), none: 'No conversation chosen', disabled: true});
  const inputs = [];
  const walk = node => { if (!node || typeof node !== 'object') return; if (Array.isArray(node)) return node.forEach(walk); if (node.type === 'input') inputs.push(node); walk(node.props?.children); };
  walk(tree);
  assert.deepEqual(inputs.map(input => [input.props.value, input.props.checked, input.props.disabled, input.props.name]), [['', false, true, 'g'], ['k1', false, true, 'g'], ['k2', true, true, 'g']]);
  inputs[1].props.onChange(); inputs[0].props.onChange();
  assert.deepEqual(chosen, ['k1', '']);
  assert.equal(tree.props.disabled, true, 'the fieldset is disabled too');
});

test('guard: ConversationChoices is a trusted presentation whose rows, choice and handler are never drawn; its legend and none words are judged', async () => {
  const {sourceFailures} = await import('./support/presentation-guard.mjs');
  const judge = source => sourceFailures('Invented.tsx', 'import { ConversationChoices } from "./AgentText";\n' + source, [], 'controls').failures;
  assert.deepEqual(judge('const x = <ConversationChoices legend="Send to" group={`g-${row.ref}`} value={rows.map(r => ({ key: r.k, id: r.id, title: r.title }))} chosen={state.key} onChoose={k => set(k)} disabled={!!busy} none="None chosen" />;'), []);
  assert.notDeepEqual(judge('const x = <ConversationChoices legend={row.title} group="g" value={rows} chosen="" onChoose={set} />;'), [], 'a supplied legend fails');
  assert.notDeepEqual(judge('const x = <ConversationChoices legend="Send to" group="g" value={rows} chosen="" onChoose={set} none={row.title} />;'), [], 'supplied none words fail');
  assert.notDeepEqual(judge('const x = <label>Pick <ConversationChoices legend="Send to" group="g" value={rows} chosen="" onChoose={set} /></label>;'), [], 'never inside a label');
  // On a guarded view every component is judged: the one from AgentText passes, one of the same name from elsewhere fails.
  const page = from => sourceFailures('Invented.tsx', `import { ConversationChoices } from "${from}";\nconst x = <ConversationChoices legend="L" group="g" value={rows} chosen={k} onChoose={set} />;`, [], 'page').failures;
  assert.deepEqual(page('./AgentText'), []);
  assert.notDeepEqual(page('./elsewhere'), [], 'only the one from AgentText is trusted');
});

test('clockWords: a time the App holds as HH:MM:SS; anything that is not a finite number giving a valid date is null', () => {
  const {clockWords} = loadSrc('AgentText');
  const at = new Date(2026, 10, 14, 7, 5, 9).getTime();
  assert.equal(clockWords(at), '07:05:09');
  assert.match(clockWords(0), /^\d\d:\d\d:\d\d$/);
  for (const bad of ['1700000000000', 'UNTRUSTED\n\u202eAllow once', NaN, Infinity, -Infinity, {valueOf: () => 1}, null, undefined, true, 8.64e15 + 1])
    assert.equal(clockWords(bad), null, String(bad));
});
