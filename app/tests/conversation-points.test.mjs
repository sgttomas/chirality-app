// DEL-02-03 REQ-008: what a conversation's recorded points show, on readings
// shaped as hosting_points::points_view hands them. Invented material only.
import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain, agentBoxNames} from './support/agent-text.mjs';

const {ConversationPoints, NONE_RECORDED, NOT_READ_WHOLE, NOT_OFFERED, PAUSE_IS_COOPERATION, INTEGRATOR_UNKNOWN, RESERVED_ACT} = loadSrc('ConversationPoints');
const g = {appSession: 's', home: 'h', spawnCounter: 1};
// The markup with HTML's escaped apostrophe read back, so the App's sentences can be compared as written.
const show = (row, threadId = 'thread') => renderToStaticMarkup(React.createElement(ConversationPoints, {points: [row], generation: g, threadId})).replaceAll('&#x27;', "'");
const row = (over = {}) => ({generation: g, threadId: 'thread', offer: {state: 'offered at start in this App session'}, reading: {whole: true, reasons: []}, points: [], refused: [], ...over});
const placer = {observed: {caller: "this conversation's agent, through the App's point tool", turnStart: null, turnStartLimit: 'the App did not observe starting this turn'}};
const point = (terms, over = {}) => ({point: 'pt-1', turn: 'turn-1', call: 'call-1', run: {state: 'no run', reason: 'no run open in this conversation in this App session'}, placer, recordedAt: '2026-11-18T00:00:00Z', terms, ...over});
const terms = {version: 1, operation: 'place', label: 'Before the drawing is issued', kind: 'review', pause: 'asks the agent to pause', pauseSetBy: 'the person',
  whoMustRespond: 'the checking engineer', whoIntegrates: 'the drafting lead', reservedAct: 'engineering approval', placedOnRequestOf: 'the person',
  concerns: {content: 'drawings/A-101.pdf'}};

test('a conversation offered the tool with a whole reading and no point says none has been recorded', () => {
  const html = show(row());
  assert.ok(html.includes(NONE_RECORDED));
  assert.ok(html.includes('The App offered its point tool when this conversation started.'));
  assert.ok(!html.includes(NOT_READ_WHOLE));
});

test('an incomplete reading never says no point has been recorded, and says why', () => {
  const html = agentPlain(show(row({reading: {whole: false, reasons: ['the pointer to point pt-9 could not be saved (ledger refused); the App completes it when it next can']}})));
  assert.ok(!html.includes(NONE_RECORDED));
  assert.ok(html.includes(NOT_READ_WHOLE));
  assert.ok(html.includes('⟦Why: the pointer to point pt-9 could not be saved (ledger refused); the App completes it when it next can⟧'));
});

test('a conversation not offered the tool says so and never that none was recorded', () => {
  const html = show(row({offer: {state: 'not offered in this App session'}}));
  assert.ok(html.includes(NOT_OFFERED));
  assert.ok(!html.includes(NONE_RECORDED));
  assert.ok(show(row({offer: {state: 'offered when this conversation started, restored after the App restarted'}})).includes('that offer was restored after the App restarted'));
});

test('read terms are shown as the agent wrote them, with the App\'s sentences on pause, integrator and reserved act', () => {
  const html = agentPlain(show(row({points: [point({state: 'read', arguments: terms})]})));
  assert.ok(html.includes('Point 1, reference pt-1. Placed when no run was open in this conversation in this App session.'));
  assert.ok(html.includes('⟦The agent wrote: Before the drawing is issued⟧'));
  assert.ok(html.includes('⟦The agent wrote: the checking engineer⟧'));
  assert.ok(html.includes('⟦Content: drawings/A-101.pdf⟧') && html.includes('Revision not recorded.'));
  assert.ok(html.includes('Kind: Review.'));
  assert.ok(html.includes(PAUSE_IS_COOPERATION) && html.includes('The point asks the agent to pause. Set by the person.'));
  assert.ok(html.includes(INTEGRATOR_UNKNOWN));
  assert.ok(html.includes('The point names a reserved act: engineering approval. ' + RESERVED_ACT));
  assert.ok(html.includes("Placed at the person's request."));
  assert.ok(html.includes('<dt>Resolved when</dt><dd>not recorded</dd>'), 'a term the person did not state is not recorded, never invented');
  assert.ok(!/received|was told|has been notified/i.test(html), 'never says a running agent or person received anything');
});

test('the run reading is the run, its absence, or not established', () => {
  assert.ok(show(row({points: [point({state: 'read', arguments: terms}, {run: {state: 'in run', run: 'run:abc'}})]})).includes('Placed during run run:abc.'));
  assert.ok(show(row({points: [point({state: 'read', arguments: terms}, {run: {state: 'not established', reason: 'x'}})]})).includes('Whether a run was open when it was placed is not established.'));
});

test('terms not read show the point and the App\'s reason, never terms from elsewhere', () => {
  const html = agentPlain(show(row({points: [point({state: 'not read', reason: 'the recorded terms do not match the digest kept with the pointer'})]})));
  assert.ok(html.includes('Point 1, reference pt-1.'));
  assert.ok(html.includes('Terms not read. ⟦Why: the recorded terms do not match the digest kept with the pointer⟧'));
  assert.ok(!html.includes('The agent wrote:'));
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
