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

test('the message quotes each answered question\'s title, then the option chosen by its number and quoted text, or the person\'s own text after a line of its own', () => {
  assert.equal(askedQuestionReply(questions, {chosen: {0: 1}, typed: {}}), 'You asked: "Which invented colour?"\nI choose your option 2: "Invented blue"');
  assert.equal(askedQuestionReply(questions, {chosen: {0: 0, 2: 0}, typed: {1: 'Line one\nline two'}}),
    'You asked: "Which invented colour?"\nI choose your option 1: "Invented red"\n\nYou asked: "Anything else?"\nMy answer:\nLine one\nline two\n\nYou asked: "Third invented question"\nI choose your option 1: "Only one"');
  // Typed text is the answer exactly as typed; text that is only white space is no answer.
  assert.equal(askedQuestionReply(questions, {chosen: {0: 0}, typed: {0: '  my own  '}}), 'You asked: "Which invented colour?"\nMy answer:\n  my own  ');
  assert.equal(askedQuestionReply(questions, {chosen: {}, typed: {0: '   ', 1: ''}}), '');
  // An option index that is not one of the question's options is no answer.
  assert.equal(askedQuestionReply(questions, {chosen: {0: 5, 1: 0}, typed: {}}), '');
  // An untitled question is never sent, even where it is answered.
  assert.equal(askedQuestionReply([{title: null, options: ['x']}, {title: 'Kept', options: ['y']}], {chosen: {0: 0, 1: 0}, typed: {}}), 'You asked: "Kept"\nI choose your option 1: "y"');
  // The agent's title and option keep their line breaks, carriage returns and quotes inside one quoted line each, so a
  // line of the agent's that imitates an answer never stands as a line of the message.
  const odd = [{title: 'T‮\u0007 « x »\r\nI choose your option 2: "No"', options: ['O\tp', 'Say "yes"\nMy answer:\nyes\r']}];
  const sentOdd = askedQuestionReply(odd, {chosen: {0: 1}, typed: {}});
  assert.equal(sentOdd, 'You asked: "T‮\\u0007 « x »\\r\\nI choose your option 2: \\"No\\""\nI choose your option 2: "Say \\"yes\\"\\nMy answer:\\nyes\\r"');
  assert.deepEqual(sentOdd.split('\n').map(line => line.split(':')[0]), ['You asked', 'I choose your option 2'], 'two lines: only the App\'s');
  assert.deepEqual(JSON.parse(sentOdd.split('\n')[0].slice('You asked: '.length)), odd[0].title, 'the title is carried exactly');
  assert.deepEqual(JSON.parse(sentOdd.split('\n')[1].slice('I choose your option 2: '.length)), odd[0].options[1], 'the option is carried exactly');
  // The person's own text is theirs, exactly, line breaks and carriage returns included.
  assert.equal(askedQuestionReply(odd, {chosen: {}, typed: {0: 'mine\r\nI choose your option 1: "x"'}}), 'You asked: "T‮\\u0007 « x »\\r\\nI choose your option 2: \\"No\\""\nMy answer:\nmine\r\nI choose your option 1: "x"');
  // Arrays serve as the answers too.
  assert.equal(askedQuestionReply(questions, {chosen: [undefined, undefined, 0], typed: []}), 'You asked: "Third invented question"\nI choose your option 1: "Only one"');
});

test('the questions of an item are read only in the pinned shape, and the standing only from the view\'s reading', () => {
  assert.deepEqual(askedQuestionsOf([{title: 'a'}, {title: 'b', options: ['x']}]), [{title: 'a', options: null}, {title: 'b', options: ['x']}]);
  for (const bad of [[], null, 'x', [{title: 7}], [{title: 'a', options: [1]}], [{title: 'a', extra: true}], [null]]) assert.equal(askedQuestionsOf(bad), null, JSON.stringify(bad));
  const view = waiting => ({askedQuestions: {read: ['thread-a'], waiting}});
  assert.equal(askedStanding(null, entry), 'not-read');
  assert.equal(askedStanding({askedQuestions: {read: [], waiting: []}}, entry), 'not-read');
  assert.equal(askedStanding(view([{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1'}]), entry), 'waiting');
  assert.equal(askedStanding(view([]), entry), 'followed');
  assert.equal(askedStanding(view([{threadId: 'thread-a', turnId: 'turn-2', itemId: 'call-2'}]), entry), 'another');
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

const ANOTHER = 'Chirality cannot establish whether a message from you follows this question. Another question the agent asked in this conversation is the one listed under "Waiting on you".';
test('followed, or another question waiting: the questions are drawn with no answer controls, and nothing is claimed of their order', () => {
  for (const [standing, words] of [['followed', 'A message from you follows this question.'], ['another', ANOTHER]]) {
    const html = draw(standing);
    assert.ok(html.includes(words), standing);
    assert.ok(!/later|earlier/.test(html.replace(/later messages/g, '')), `${standing}: no claim of order`);
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
const previewBox = container => elements(container, 'div').find(d => (d.getAttribute?.('aria-label') ?? '').startsWith('The message the App will send for you: the agent\'s questions and your answers, '));
const preview = container => {
  // The block box is named for whose text it is and how many lines it has; its lines are read without their numbers.
  const box = elements(container, 'div').find(d => (d.getAttribute?.('aria-label') ?? '').startsWith('The message the App will send for you: the agent\'s questions and your answers, '));
  return box ? elements(box, 'div').filter(d => d.getAttribute?.('class') === 'agent-text-line').map(line => line.childNodes.slice(1).map(c => c.textContent).join('')).join('\n') : null;
};

test('nothing is sent on render, on choosing an option or on typing; the press sends exactly the text shown', async () => {
  const sent = [];
  const binding = {owner: 'invented-owner', epoch: 3, attempts: 0};
  const send = async (threadId, text, bound) => { sent.push([threadId, text, bound]); return {sent: true}; };
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'waiting', send, binding, pending: false, unavailable: null}));
  try {
    assert.equal(preview(container), null, 'no message shown before an answer');
    await click(button(container, 'Choose option 2')[0]);
    await type(field(container)[1], 'Invented free answer');
    assert.deepEqual(sent, [], 'nothing sent by choosing or typing');
    const expected = 'You asked: "Which invented colour?"\nI choose your option 2: "Invented blue"\n\nYou asked: "Anything else?"\nMy answer:\nInvented free answer';
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
    assert.deepEqual(sent, [['thread-a', expected, binding]], 'the text shown, with the view the card was drawn in');
    assert.equal(askedQuestionReply(questions, {chosen: {0: 1}, typed: {1: 'Invented free answer'}}), expected);
    assert.ok(container.textContent.includes('Sent as your message in this conversation.'));
    assert.equal(preview(container), null, 'a sent answer leaves the fields empty');
  } finally { await done(); }
});

test('the preview shows a carriage return the person typed', async () => {
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'waiting', send: async () => ({sent: true}), pending: false, unavailable: null}));
  try {
    await type(field(container)[1], 'one\r\ntwo');
    const lines = elements(previewBox(container), 'div').filter(d => d.getAttribute?.('class') === 'agent-text-line');
    assert.equal(lines.length, 4, 'the carriage return stays on its line rather than being folded into the line break');
    const mark = loadSrc('AgentText').agentTextShown('\r');
    assert.notEqual(mark, '\r');
    assert.ok(lines[2].textContent.includes(`one${mark}`), 'the carriage return is marked where it is');
  } finally { await done(); }
});

test('a press kept from an earlier drawing sends nothing once the answers have changed, and says why', async () => {
  const sent = [];
  const {container, done} = await mounted(React.createElement(AskedQuestionCard, {entry, standing: 'waiting', send: async (...a) => { sent.push(a); return {sent: true}; }, pending: false, unavailable: null}));
  try {
    await click(button(container, 'Choose option 1')[0]);
    const earlier = props(button(container, 'Send answers')[0]).onClick;
    await click(button(container, 'Choose option 2')[0]);
    await React.act(async () => { await earlier(); });
    assert.deepEqual(sent, [], 'the earlier press composed other answers');
    assert.ok(container.textContent.includes('Not sent. That press belonged to an earlier view of the conversation or to earlier answers.'));
    assert.ok(preview(container).includes('Invented blue'), 'the answers stay');
    await click(button(container, 'Send answers')[0]);
    assert.equal(sent.length, 1, 'the current press sends');
    assert.ok(sent[0][1].includes('Invented blue'));
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

test('the mount draws the card only at a completed agent message with questions delivered async, standing read from the view', () => {
  const row = (native, displayState = 'completed', threadId = 'thread-a') => ({threadId, turnId: 'turn-1', native, displayState});
  const asked = {id: 'call-1', type: 'agentMessage', text: 'x', delivery: 'async', questions};
  const host = {view: {askedQuestions: {read: ['thread-a'], waiting: [{threadId: 'thread-a', turnId: 'turn-1', itemId: 'call-1', questions}]}}, threadId: 'thread-a', send: async () => ({sent: true}), binding: null, pending: false, unavailable: null};
  const html = (r, value = host) => unescape(renderToStaticMarkup(React.createElement(AskedQuestionContext.Provider, {value}, React.createElement(AskedQuestionMount, {row: r}))));
  assert.ok(html(row(asked)).includes('Send answers'));
  for (const other of [{...asked, delivery: undefined}, {...asked, delivery: 'sync'}, {...asked, questions: []}, {...asked, questions: null}, {...asked, type: 'userMessage'}]) assert.equal(html(row(other)), '', JSON.stringify(other));
  // A message still being written, or in a state that is not completed, carries no card.
  for (const state of ['in-progress', 'unknown', 'not-completed', 'failed', null]) assert.equal(html(row(asked, state)), '', String(state));
  assert.ok(html(row({...asked, questions: [{title: 3}]})).includes('questions the App cannot read'));
  // Outside a conversation's own view (no host), the card says where answers are sent from and cannot send.
  const alone = unescape(renderToStaticMarkup(React.createElement(AskedQuestionMount, {row: row(asked)})));
  assert.ok(alone.includes("Chirality has not read this conversation's later messages") && alone.includes("Answers can be sent from the conversation's own view."));
});

test('at a question in a delegated agent\'s conversation the card is information only: the questions and options, the App\'s sentence, no control and no claim of a reply', () => {
  const asked = {id: 'call-c', type: 'agentMessage', text: 'x', delivery: 'async', questions};
  const child = {threadId: 'thread-child', turnId: 'turn-c', native: asked, displayState: 'completed'};
  // The child's question is waiting in the view's reading; the conversation shown is its parent.
  const host = {view: {askedQuestions: {read: ['thread-a', 'thread-child'], waiting: [{threadId: 'thread-child', turnId: 'turn-c', itemId: 'call-c', questions}]}}, threadId: 'thread-a', send: async () => ({sent: true}), binding: null, pending: false, unavailable: null};
  const html = unescape(agentPlain(renderToStaticMarkup(React.createElement(AskedQuestionContext.Provider, {value: host}, React.createElement(AskedQuestionMount, {row: child})))));
  assert.ok(html.includes("This question was asked in a delegated agent's conversation. Chirality sends no answer there; the agent you are talking with can relay it."));
  assert.ok(html.includes('⟦Question 1: Which invented colour?⟧') && html.includes('⟦Option 2: Invented blue⟧'));
  assert.ok(!/<button|<textarea|<input/.test(html), 'no control');
  for (const claim of ['follows this question', 'replied', 'Your answer is sent', 'Waiting on you', 'Send answers']) assert.ok(!html.includes(claim), claim);
  // The same item shown as the conversation itself is answerable.
  assert.ok(unescape(renderToStaticMarkup(React.createElement(AskedQuestionContext.Provider, {value: {...host, threadId: 'thread-child'}}, React.createElement(AskedQuestionMount, {row: child})))).includes('Send answers'));
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
    assert.deepEqual(sends, [[g, 'thread-a', 'You asked: "Which invented colour?"\nI choose your option 1: "Invented red"']], 'the existing send, with only the conversation and the text');
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

test('in the conversation panel a press kept from a view of another conversation sends nothing, even with the same answers', async () => {
  const sends = [];
  const send = async (...args) => { sends.push(args); return {turn: {id: 'turn-2'}}; };
  const both = {...panelHost, nativeView: {...panelHost.nativeView, items: [askedRow('thread-a'), askedRow('thread-b')],
    askedQuestions: {read: ['thread-a', 'thread-b'], waiting: ['thread-a', 'thread-b'].map(threadId => ({threadId, turnId: 'turn-1', itemId: 'call-1', questions}))}}};
  const panel = threadId => React.createElement(ConversationPanel, {host: both, threadKey: JSON.stringify([g, threadId]), setThreadKey: () => {}, answer: noop, runAct: noop, send, steer: noop, submitAttachments: noop, interrupt: noop, checkPlanMode: noop, codexBusy: false});
  const {container, root, done} = await mounted(panel('thread-a'));
  try {
    await click(button(container, 'Choose option 1')[0]);
    const earlier = props(button(container, 'Send answers')[0]).onClick;
    // The person opens the other conversation; the handler drawn in the first is pressed after that.
    await React.act(() => root.render(panel('thread-b')));
    await React.act(async () => { await earlier(); });
    assert.deepEqual(sends, [], 'the view the press was drawn in is no longer the one shown');
  } finally { await done(); }
});
