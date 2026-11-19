// The agent's question that does not wait (Codex's request_user_input_async): the card drawn at an agent message
// carrying questions, the message it composes, and the send that goes through the conversation's own send path, only
// on the person's press. Invented material only.
import test from 'node:test';
import assert from 'node:assert/strict';
import {renderToStaticMarkup} from 'react-dom/server';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';

const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {AskedQuestionCard, AskedQuestionMount, AskedQuestionContext, askedQuestionReply, askedQuestionsOf, askedStanding} = loadSrc('AskedQuestionCard');
const {ConversationPanel} = loadSrc('App');

const questions = [{title: 'Which invented colour?', options: ['Invented red', 'Invented blue']}, {title: 'Anything else?', options: null}, {title: 'Third invented question', options: ['Only one']}];
const entry = {threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1', questions};
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container, tag) => container.querySelectorAll(element => element.localName === tag);
const button = (container, words) => elements(container, 'button').filter(element => element.textContent === words);
const field = container => elements(container, 'textarea').filter(element => element.parentNode.textContent.startsWith('Your own answer'));

test('the message is each answered question\'s title, then its answer on the next line, a blank line between, unanswered ones left out', () => {
  assert.equal(askedQuestionReply(questions, {chosen: {0: 1}, typed: {}}), 'Which invented colour?\nInvented blue');
  assert.equal(askedQuestionReply(questions, {chosen: {0: 0, 2: 0}, typed: {1: 'Line one\nline two'}}),
    'Which invented colour?\nInvented red\n\nAnything else?\nLine one\nline two\n\nThird invented question\nOnly one');
  // Typed text is the answer exactly as typed; text that is only white space is no answer.
  assert.equal(askedQuestionReply(questions, {chosen: {0: 0}, typed: {0: '  my own  '}}), 'Which invented colour?\n  my own  ');
  assert.equal(askedQuestionReply(questions, {chosen: {}, typed: {0: '   ', 1: ''}}), '');
  // An option index that is not one of the question's options is no answer.
  assert.equal(askedQuestionReply(questions, {chosen: {0: 5, 1: 0}, typed: {}}), '');
  // The agent's title and option text are carried byte for byte.
  const odd = [{title: 'T‮\u0007 « x »', options: ['O\tp']}];
  assert.equal(askedQuestionReply(odd, {chosen: {0: 0}, typed: {}}), 'T‮\u0007 « x »\nO\tp');
  // Arrays serve as the answers too.
  assert.equal(askedQuestionReply(questions, {chosen: [undefined, undefined, 0], typed: []}), 'Third invented question\nOnly one');
});

test('the questions of an item are read only in the pinned shape, and the standing only from the view\'s reading', () => {
  assert.deepEqual(askedQuestionsOf([{title: 'a'}, {title: 'b', options: ['x']}]), [{title: 'a', options: null}, {title: 'b', options: ['x']}]);
  for (const bad of [[], null, 'x', [{title: 7}], [{title: 'a', options: [1]}], [{title: 'a', extra: true}], [null]]) assert.equal(askedQuestionsOf(bad), null, JSON.stringify(bad));
  const view = waiting => ({askedQuestions: {read: ['thread-a'], waiting}});
  assert.equal(askedStanding(null, entry), 'not-read');
  assert.equal(askedStanding({askedQuestions: {read: [], waiting: []}}, entry), 'not-read');
  assert.equal(askedStanding(view([{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1'}]), entry), 'waiting');
  assert.equal(askedStanding(view([]), entry), 'followed');
  assert.equal(askedStanding(view([{threadId: 'thread-a', turnId: 'turn-2', itemId: 'call-2'}]), entry), 'superseded');
  assert.equal(askedStanding({...view([{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1'}]), observationEnded: true}, entry), 'not-read', 'an ended observation is not a current reading');
});

const unescape = html => html.replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&');
const draw = (standing, extra = {}) => unescape(agentPlain(renderToStaticMarkup(React.createElement(AskedQuestionCard, {entry, standing, send: async () => ({sent: true}), pending: false, unavailable: null, ...extra}))));
const LINE = 'The agent asked this and went on: its turn did not wait for you. Your answer is sent as your next message in this conversation.';

test('waiting: the App\'s line, each question\'s title and options as the agent\'s, a free field for each, and Send answers not yet enabled', () => {
  const html = draw('waiting');
  assert.ok(html.includes(LINE));
  assert.ok(html.includes('⟦Question 1: Which invented colour?⟧') && html.includes('⟦Option 2: Invented blue⟧') && html.includes('⟦Question 2: Anything else?⟧'));
  assert.equal((html.match(/>Choose option 1</g) ?? []).length, 2, 'each question with options offers them');
  assert.equal((html.match(/Your own answer/g) ?? []).length, 3, 'a free field for every question');
  assert.match(html, /<button[^>]*disabled=""[^>]*>Send answers<\/button>/);
  assert.ok(!html.includes('A message from you follows') && !html.includes('has not read'));
});

test('not read: the App says it cannot say whether the person replied, and answering is still offered', () => {
  const html = draw('not-read');
  assert.ok(html.includes("Chirality has not read this conversation's later messages, so it cannot say whether you replied."));
  assert.ok(html.includes(LINE) && html.includes('Send answers') && html.includes('Your own answer'));
});

test('followed or superseded: the questions are drawn as past, with no answer controls', () => {
  for (const [standing, words] of [['followed', 'A message from you follows this question.'], ['superseded', 'The agent asked a later question in this conversation']]) {
    const html = draw(standing);
    assert.ok(html.includes(words), standing);
    assert.ok(html.includes('⟦Question 1: Which invented colour?⟧') && html.includes('⟦Option 1: Invented red⟧'), standing);
    assert.ok(!/<button|<textarea|<input/.test(html), `${standing}: no control`);
    assert.ok(!html.includes('Your answer is sent'), standing);
  }
});

test('a reason the card cannot send is the App\'s words, and Send answers stays disabled', () => {
  const html = draw('waiting', {unavailable: 'unconfirmed'});
  assert.ok(html.includes("An earlier message to this conversation wasn't confirmed"));
  assert.ok(draw('waiting', {send: undefined}).includes("Answers can be sent from the conversation's own view."));
});

async function mounted(element) {
  const container = document.createElement('div'); document.body.appendChild(container);
  const root = createRoot(container);
  await React.act(() => root.render(element));
  return {container, root, done: async () => { await React.act(() => root.unmount()); document.body.removeChild(container); }};
}
const click = async element => React.act(async () => { await props(element).onClick(); });
const type = async (element, value) => React.act(() => props(element).onChange({target: {value}}));
const preview = container => {
  // The block box is named for whose text it is and how many lines it has; its lines are read without their numbers.
  const box = elements(container, 'div').find(d => (d.getAttribute?.('aria-label') ?? '').startsWith('The message the App will send for you: the agent\'s questions and your answers, '));
  return box ? elements(box, 'div').filter(d => d.getAttribute?.('class') === 'agent-text-line').map(line => line.childNodes.slice(1).map(c => c.textContent).join('')).join('\n') : null;
};

test('nothing is sent on render, on choosing an option or on typing; the press sends exactly the text shown', async () => {
  const sent = [];
  const send = async (threadId, text) => { sent.push([threadId, text]); return {sent: true}; };
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'waiting', send, pending: false, unavailable: null}));
  try {
    assert.equal(preview(container), null, 'no message shown before an answer');
    await click(button(container, 'Choose option 2')[0]);
    await type(field(container)[1], 'Invented free answer');
    assert.deepEqual(sent, [], 'nothing sent by choosing or typing');
    const expected = 'Which invented colour?\nInvented blue\n\nAnything else?\nInvented free answer';
    assert.equal(preview(container).replaceAll('⏎', ''), expected, 'the message is shown, exactly, before the press');
    assert.ok(container.textContent.includes('Selected: option 2 Its text: Invented blue'), 'the choice is shown as the request card shows it');
    // Typing replaces a choice; choosing replaces typing: the field never holds the agent's option text.
    await type(field(container)[0], 'typed instead');
    assert.ok(container.textContent.includes('Selected: your own answer, in the field above'));
    await click(button(container, 'Choose option 2')[0]);
    assert.equal(props(field(container)[0]).value, '');
    const send_ = button(container, 'Send answers')[0];
    assert.equal(props(send_).disabled, false);
    await click(send_);
    assert.deepEqual(sent, [['thread-a', expected]]);
    assert.equal(askedQuestionReply(questions, {chosen: {0: 1}, typed: {1: 'Invented free answer'}}), expected);
    assert.ok(container.textContent.includes('Sent as your message in this conversation.'));
    assert.equal(preview(container), null, 'a sent answer leaves the fields empty');
  } finally { await done(); }
});

test('a failed or refused send keeps every answer and says why; nothing is resent by itself', async () => {
  const results = [{sent: false, reported: 'invented host failure'}, {sent: false, unavailable: 'other-conversation'}];
  const sent = [];
  const send = async (threadId, text) => { sent.push(text); return results.shift(); };
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'not-read', send, pending: false, unavailable: null}));
  try {
    await click(button(container, 'Choose option 1')[0]);
    await click(button(container, 'Send answers')[0]);
    assert.ok(container.textContent.includes("The App couldn't confirm the send") && container.textContent.includes('invented host failure'));
    assert.ok(preview(container).includes('Invented red'), 'the answers are kept');
    await click(button(container, 'Send answers')[0]);
    assert.ok(container.textContent.includes('Open this conversation to send your answer there.'));
    assert.equal(sent.length, 2, 'one send per press');
  } finally { await done(); }
});

test('while a send is pending elsewhere the card does not send', async () => {
  const sent = [];
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'waiting', send: async (...a) => { sent.push(a); return {sent: true}; }, pending: true, unavailable: null}));
  try {
    await click(button(container, 'Choose option 1')[0]);
    assert.equal(props(button(container, 'Send answers')[0]).disabled, true);
    await click(button(container, 'Send answers')[0]);
    assert.deepEqual(sent, []);
  } finally { await done(); }
});

test('the mount draws the card only at an agent message with questions delivered async, standing read from the view', () => {
  const row = native => ({threadId: 'thread-a', turnId: 'turn-1', native});
  const asked = {id: 'call-1', type: 'agentMessage', text: 'x', delivery: 'async', questions};
  const host = {view: {askedQuestions: {read: ['thread-a'], waiting: [{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1', questions}]}}, send: async () => ({sent: true}), pending: false, unavailable: null};
  const html = r => unescape(renderToStaticMarkup(React.createElement(AskedQuestionContext.Provider, {value: host}, React.createElement(AskedQuestionMount, {row: r}))));
  assert.ok(html(row(asked)).includes('Send answers'));
  for (const other of [{...asked, delivery: undefined}, {...asked, delivery: 'sync'}, {...asked, questions: []}, {...asked, questions: null}, {...asked, type: 'userMessage'}]) assert.equal(html(row(other)), '', JSON.stringify(other));
  assert.ok(html(row({...asked, questions: [{title: 3}]})).includes('questions the App cannot read'));
  // Outside a conversation's own view (no host), the card says where answers are sent from and cannot send.
  const alone = unescape(renderToStaticMarkup(React.createElement(AskedQuestionMount, {row: row(asked)})));
  assert.ok(alone.includes("Chirality has not read this conversation's later messages") && alone.includes("Answers can be sent from the conversation's own view."));
});

// The conversation panel: the card's send is the conversation's own send command, with the composed text, to the
// conversation shown, only on the press; the message box's draft is untouched.
const g = {appSession: 's', home: 'h', spawnCounter: 1};
const thread = threadId => ({generation: g, threadId, appRole: {standing: 'app-observed', role: null, supply_ref: `sup:${threadId}`}, roleRelation: {kind: 'start'}, futureGuidanceNotices: []});
const askedRow = threadId => ({threadId, turnId: 'turn-1', native: {id: 'call-1', type: 'agentMessage', text: 'Asked text', delivery: 'async', questions}, displayState: 'completed', standing: 'live-observed', observationEnded: false, observedOrder: 1});
const panelHost = {state: 'ready', generation: g, roleLimits: {account: {roles: []}}, threads: [thread('thread-a'), thread('thread-b')],
  nativeView: {generation: g, home: 'h', items: [askedRow('thread-a')], descendants: [], askedQuestions: {read: ['thread-a'], waiting: [{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1', questions}]}}};
const noop = async () => {};

test('in the conversation panel the press sends one ordinary message through the existing send, to that conversation, and nothing else', async () => {
  const sends = [];
  const send = async (...args) => { sends.push(args); return {turn: {id: 'turn-2'}}; };
  const panel = () => React.createElement(ConversationPanel, {host: panelHost, threadKey: JSON.stringify([g, 'thread-a']), setThreadKey: () => {}, answer: noop, runAct: noop, send, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false});
  const {container, root, done} = await mounted(panel());
  try {
    assert.ok(container.textContent.includes(LINE), 'the card is drawn at the agent message');
    await click(button(container, 'Choose option 1')[0]);
    assert.deepEqual(sends, [], 'nothing sent on choosing');
    await click(button(container, 'Send answers')[0]);
    assert.deepEqual(sends, [[g, 'thread-a', 'Which invented colour?\nInvented red']], 'the existing send, with only the conversation and the text');
    await React.act(() => root.render(panel()));
    assert.ok(container.textContent.includes('Native turn/start response received.'), 'the outcome is the ordinary send\'s');
  } finally { await done(); }
});

test('in the conversation panel an unconfirmed send holds the card as it holds the message box', async () => {
  const sends = [];
  const send = async (...args) => { sends.push(args); throw new Error('invented write failure'); };
  const {container, done} = await mounted(React.createElement(ConversationPanel, {host: panelHost, threadKey: JSON.stringify([g, 'thread-a']), setThreadKey: () => {}, answer: noop, runAct: noop, send, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false}));
  try {
    await click(button(container, 'Choose option 1')[0]);
    await click(button(container, 'Send answers')[0]);
    assert.equal(sends.length, 1);
    assert.ok(container.textContent.includes('may have been sent'), 'held as an unconfirmed message');
    assert.ok(container.textContent.includes("An earlier message to this conversation wasn't confirmed"), 'the card says why it will not send');
    assert.equal(props(button(container, 'Send answers')[0]).disabled, true);
    await click(button(container, 'Send answers')[0]);
    assert.equal(sends.length, 1, 'no second send while the first is unconfirmed');
  } finally { await done(); }
});
