import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { CoordinationPanel } from '../../components/woven-dialogue/coordination-panel';
it('shows native assignment evidence in Agents without inventing completion from the call', () => {
  const events = [{ schemaVersion: 1, timestamp: '2026-09-12T00:00:00Z', eventId: 'spawn', sessionId: 's', turnId: 'r', type: 'codex.notification', data: { method: 'item/completed', params: { threadId: 'p', turnId: 'n', item: { type: 'collabAgentToolCall', status: 'completed', receiverThreadIds: ['child'], prompt: 'Review the plan', agentsStates: { child: { status: 'running', message: 'Checking the constraints' } } } } } }] as HarnessEvent[];
  const html = renderToStaticMarkup(<CoordinationPanel activeView="agents" nativeEvents={events} hierarchy={{ roots: [], detached: [], childrenByParentSessionId: {}, unresolvedParentSessionIds: [], diagnostics: [] }} sessionsLoading={false} sessionsError={null} selectionDisabled={false} onSelectView={() => {}} onRefreshSessions={() => {}} onSelectSession={() => {}} />);
  expect(html).toContain('Review the plan'); expect(html).toContain('Checking the constraints'); expect(html).toContain('running'); expect(html).not.toContain('completed');
});

it('shows the recorded stock child path once without a fabricated session selection or role', () => {
  const events = ['started', 'completed'].map((phase, index) => ({ schemaVersion: 1, timestamp: '2026-09-12T00:00:00Z', eventId: String(index), sessionId: 's', turnId: 'r', type: 'codex.notification', data: { method: `item/${phase}`, params: { threadId: 'p', item: { type: 'subAgentActivity', id: 'a', kind: 'started', agentThreadId: 'child', agentPath: '/root/checker' } } } })) as HarnessEvent[];
  const html = renderToStaticMarkup(<CoordinationPanel activeView="agents" nativeEvents={events} hierarchy={{ roots: [], detached: [], childrenByParentSessionId: {}, unresolvedParentSessionIds: [], diagnostics: [] }} sessionsLoading={false} sessionsError={null} selectionDisabled={false} onSelectView={() => {}} onRefreshSessions={() => {}} onSelectSession={() => { throw new Error('Native evidence must not select a Runtime session'); }} />);
  expect(html.match(/\/root\/checker/g)).toHaveLength(1);
  expect(html).toContain('running'); expect(html).not.toContain('Role:');
  expect(html).toContain('Native work in current chat');
  expect(html).not.toContain('data-session-id="child"');
});
