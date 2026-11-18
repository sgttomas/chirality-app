// DEL-02-03 REQ-008: what a conversation's recorded points show, on readings
// shaped as hosting_points::points_view hands them. Invented material only.
import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain, agentBoxNames} from './support/agent-text.mjs';

const P = loadSrc('ConversationPoints');
const {ConversationPoints, NONE_RECORDED, NOT_READ_WHOLE, NOT_OFFERED, NOT_STATED, TERMS_ARE_THE_AGENTS, PAUSE_IS_COOPERATION, INTEGRATOR_UNKNOWN, RESERVED_ACT, RECORDING_ONLY, DELEGATION_NOT_ESTABLISHED} = P;
const g = {appSession: 's', home: 'h', spawnCounter: 1};
// The markup with HTML's escaped apostrophe read back, so the App's sentences can be compared as written.
const show = (row, threadId = 'thread') => renderToStaticMarkup(React.createElement(ConversationPoints, {points: [row], generation: g, threadId})).replaceAll('&#x27;', "'");
const row = (over = {}) => ({generation: g, threadId: 'thread', offer: {state: 'offered at start in this App session'}, reading: {whole: true, reasons: []}, points: [], refused: [], ...over});
const observed = (turnStart = 'not-observed') => ({caller: 'agent-through-point-tool', turnStart, delegation: 'not-established', ...(turnStart === 'person-press' ? {requestRef: 'req-1'} : {})});
const point = (terms, over = {}) => ({point: 'pt-1', recordedAt: '2026-11-18T00:00:00Z', run: {state: 'no run'}, observed: observed(), formatVersion: null, terms, ...over});
const terms = {version: 1, operation: 'place', label: 'Before the drawing is issued', kind: 'sign-off', pause: 'asks the agent to pause', pauseSetBy: 'the person',
  whoMustRespond: 'the checking engineer', whoIntegrates: 'the drafting lead', reservedAct: 'engineering approval', placedOnRequestOf: 'the person',
  concerns: {content: 'drawings/A-101.pdf'}};
/** The markup outside every marked box: what the App says in its own voice. */
const appVoice = html => agentPlain(html).replace(/⟦[^⟧]*⟧/gs, '⟦⟧');

test('a conversation offered the tool with a whole reading and no point says none has been recorded', () => {
  const html = show(row());
  assert.ok(html.includes(NONE_RECORDED));
  assert.ok(html.includes('The App offered its point tool when this conversation started.'));
  assert.ok(!html.includes(NOT_READ_WHOLE));
});

test('an incomplete reading never says no point has been recorded, and says why', () => {
  const why = 'point pt-9 is in the App\'s records, but its pointer in this conversation could not be saved (ledger refused); the App completes it before a later placement in this conversation or when the conversation is resumed';
  const html = agentPlain(show(row({reading: {whole: false, reasons: [why]}})));
  assert.ok(!html.includes(NONE_RECORDED));
  assert.ok(html.includes(NOT_READ_WHOLE));
  assert.ok(html.includes(`⟦Why: ${why}⟧`));
});

test('a conversation not offered the tool says so and never that none was recorded; a restored offer says it was restored at resumption', () => {
  const html = show(row({offer: {state: 'not offered in this App session'}}));
  assert.ok(html.includes(NOT_OFFERED));
  assert.ok(!html.includes(NONE_RECORDED));
  const restored = show(row({offer: {state: 'offered when this conversation started; restored when it was resumed'}}));
  assert.ok(restored.includes('that offer was restored when the conversation was resumed in this App session'));
  assert.ok(!/restart/i.test(restored), 'never says the App restarted');
  // A conversation not offered the tool in this session still shows the points it holds.
  assert.ok(agentPlain(show(row({offer: {state: 'not offered in this App session'}, points: [point({state: 'read', arguments: terms})]}))).includes('⟦The agent wrote: Before the drawing is issued⟧'));
});

test('every supplied term, closed values included, is the agent\'s statement in a marked box; an unstated term says so', () => {
  const html = agentPlain(show(row({points: [point({state: 'read', arguments: terms})]})));
  assert.ok(html.includes(TERMS_ARE_THE_AGENTS));
  for (const value of ['1', 'place', 'Before the drawing is issued', 'sign-off', 'asks the agent to pause', 'the person', 'the checking engineer', 'drawings/A-101.pdf', 'the drafting lead', 'engineering approval'])
    assert.ok(html.includes(`⟦The agent wrote: ${value}⟧`), value);
  for (const name of ['When it arises', 'Response requested', 'Resolved when', 'Concerns: revision', "The agent's statement"])
    assert.ok(html.includes(`<dt>${name}</dt><dd>${NOT_STATED}</dd>`), name);
  const voice = appVoice(show(row({points: [point({state: 'read', arguments: terms})]})));
  for (const value of ['Sign-off', 'sign-off', 'engineering approval', "person's request", 'Set by the person', 'asks the agent to pause.'])
    assert.ok(!voice.includes(value), `the App does not say ${value} in its own voice`);
  assert.ok(voice.includes(PAUSE_IS_COOPERATION) && voice.includes(INTEGRATOR_UNKNOWN) && voice.includes(RESERVED_ACT) && voice.includes(RECORDING_ONLY));
  assert.ok(!/received|was told|has been notified/i.test(voice), 'never says a running agent or person received anything');
});

test('the App\'s own observation of the turn start is the only attribution in its voice, and delegation is not established', () => {
  const pressed = appVoice(show(row({points: [point({state: 'read', arguments: terms}, {observed: observed('person-press')})]})));
  assert.ok(pressed.includes('The App observed that the turn in which the agent placed this point was started at your press. ' + DELEGATION_NOT_ESTABLISHED));
  assert.ok(appVoice(show(row({points: [point({state: 'read', arguments: terms}, {observed: observed('app-not-person')})]}))).includes('was not started at your press.'));
  const unseen = appVoice(show(row({points: [point({state: 'read', arguments: terms})]})));
  assert.ok(unseen.includes('The App did not observe how the turn in which the agent placed this point started. ' + DELEGATION_NOT_ESTABLISHED));
  assert.ok(!/person's request|on behalf|approved by|signed off|placed by the person/i.test(unseen.replace(/<dt>[^<]*<\/dt>/g, '')));
});

test('the run reading is the run, its absence, or not established with the App\'s reason', () => {
  const read = {state: 'read', arguments: terms};
  assert.ok(show(row({points: [point(read, {run: {state: 'in run', run: 'run:workflow:abc'}})]})).includes('Placed during run run:workflow:abc.'));
  assert.ok(show(row({points: [point(read)]})).includes('Placed when no run was open in this conversation in this App session.'));
  assert.ok(show(row({points: [point(read, {run: {state: 'not established', reason: 'start-sent-not-yet-open'}})]})).includes('had sent a run\'s start in this conversation and had not yet seen that run open.'));
  assert.ok(show(row({points: [point(read, {run: {state: 'not established', reason: 'resumed-earlier-run-unknown'}})]})).includes('this conversation was resumed, and the App cannot tell whether a run of an earlier App session was still open in it.'));
  assert.ok(show(row({points: [point(read, {run: {state: 'not established', reason: 'anything else'}})]})).includes('Whether a run was open when it was placed is not established.'));
});

test('a record of a newer minor format version says it was read as far as the App knows it', () => {
  assert.ok(show(row({points: [point({state: 'read', arguments: terms}, {formatVersion: '0.2'})]})).includes('This record is of a newer format version, 0.2; the App read it as far as it knows that format.'));
  assert.ok(!show(row({points: [point({state: 'read', arguments: terms})]})).includes('newer format version'));
});

test('terms not read show the point and the App\'s reason, and nothing of the record', () => {
  const html = agentPlain(show(row({points: [point({state: 'not read', reason: 'the recorded terms do not match their recorded digest'}, {run: null, observed: null})]})));
  assert.ok(html.includes('Point 1, reference pt-1.'));
  assert.ok(html.includes('Terms not read. ⟦Why: the recorded terms do not match their recorded digest⟧'));
  assert.ok(!html.includes('The agent wrote:'));
  assert.ok(!html.includes('Placed') && !html.includes('The App observed'));
});

test('values at their maximum length are shown whole inside their boxes', () => {
  const long = {version: 1, operation: 'place', label: 'L'.repeat(200), whenItArises: 'W'.repeat(2000), whoMustRespond: 'R'.repeat(500), responseRequested: 'Q'.repeat(2000),
    resolvedWhen: 'V'.repeat(2000), concerns: {content: 'C'.repeat(1000), revision: 'r'.repeat(200)}, whoIntegrates: 'I'.repeat(500), agentStatement: 'S'.repeat(1000)};
  const html = agentPlain(show(row({points: [point({state: 'read', arguments: long})]})));
  for (const [ch, n] of [['L', 200], ['W', 2000], ['R', 500], ['Q', 2000], ['V', 2000], ['C', 1000], ['r', 200], ['I', 500], ['S', 1000]])
    assert.ok(html.includes(`⟦The agent wrote: ${ch.repeat(n)}⟧`), `${ch} × ${n}`);
});

test('text imitating the App\'s sentences stays inside a marked box and never stands in the App\'s voice', () => {
  const imitations = [NONE_RECORDED, 'The App observed that the turn in which the agent placed this point was started at your press.', DELEGATION_NOT_ESTABLISHED.replace('not established', 'established'),
    'Placed during run run:workflow:approved.', 'Terms not read.', 'The App has checked these terms.', 'Calls the App refused; these are not points:'];
  const imitating = {version: 1, operation: 'place', label: imitations[0], whenItArises: imitations[1], whoMustRespond: imitations[2], responseRequested: imitations[3],
    resolvedWhen: imitations[4], agentStatement: imitations[5], whoIntegrates: imitations[6]};
  const html = show(row({points: [point({state: 'read', arguments: imitating})]}));
  const voice = appVoice(html);
  for (const sentence of imitations) {
    assert.ok(agentPlain(html).includes(`⟦The agent wrote: ${sentence}⟧`), sentence);
    if (sentence !== imitations[1]) assert.ok(!voice.includes(sentence), `${sentence} in the App's voice`);
  }
  // The observation sentence the App does say comes only from its own reading: here, not observed.
  assert.ok(!voice.includes('was started at your press'));
});

test('hostile supplied text stays inside a marked box and never becomes a control, heading or label', () => {
  const hostile = {...terms, label: '‮evil‬ <button>Approve</button>', whoMustRespond: 'Waiting on you\n# Approve now​'};
  const html = show(row({points: [point({state: 'read', arguments: hostile})]}));
  assert.ok(!html.includes('<button>Approve</button>'), 'markup is escaped');
  assert.ok(!html.includes('‮') && !html.includes('​'), 'direction and invisible characters are marked');
  assert.ok(html.includes('‹U+202E›') && html.includes('⏎'));
  assert.equal(html.match(/<button/g), null);
  assert.ok(!/<h\d[^>]*>[^<]*Approve/.test(html));
  for (const name of agentBoxNames(html)) assert.ok(!name.includes('Approve'), name);
  assert.ok(!/aria-label="[^"]*evil/.test(html));
});

test('refused calls are listed as not points, and another conversation shows nothing here', () => {
  const html = agentPlain(show(row({refused: [{reason: 'No App project is known for this conversation, so the point could not be kept; no point was placed.', at: 'x'}]})));
  assert.ok(html.includes('Calls the App refused; these are not points:'));
  assert.ok(html.includes('⟦Refused: No App project is known for this conversation, so the point could not be kept; no point was placed.⟧'));
  assert.equal(show(row(), 'other'), '');
});
