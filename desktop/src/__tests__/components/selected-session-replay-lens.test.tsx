import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import renderer, { act } from 'react-test-renderer';
import { describe, expect, it, vi } from 'vitest';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
const methodMocks = vi.hoisted(() => ({ revisions: vi.fn() }));
vi.mock('../../lib/harness/method-selection-client', async importOriginal => ({
  ...await importOriginal<typeof import('../../lib/harness/method-selection-client')>(),
  listNativePlanRevisions: methodMocks.revisions
}));
import { SelectedSessionReplayLens } from '../../components/woven-dialogue/selected-session-replay-lens';
import { buildSelectedSessionReplayProjection } from '../../lib/woven-dialogue/selected-session-replay';

function replayProjection(sessionOverrides: Record<string, unknown> = {}) {
  const session = {
    ...sessionOverrides,
    sessionId: 'recorded-session',
    projectRoot: '/repo/project',
    persona: 'WORKING_ITEMS',
    mode: 'governed',
    createdAt: '2026-07-23T00:00:00.000Z',
    updatedAt: '2026-07-23T00:00:00.000Z',
    engineSelection: {
      adapterId: 'pi',
      providerId: 'omlx',
      model: 'recorded-model'
    },
    status: 'completed'
  } as SessionRecord;
  const events: HarnessEvent[] = [
    {
      schemaVersion: 1,
      eventId: 'event-1',
      sessionId: session.sessionId,
      turnId: 'turn-1',
      timestamp: '2026-07-23T00:00:01.000Z',
      type: 'message.completed',
      data: { role: 'assistant', text: 'Recorded answer' }
    },
    {
      schemaVersion: 1,
      eventId: 'event-2',
      sessionId: session.sessionId,
      turnId: 'turn-1',
      timestamp: '2026-07-23T00:00:02.000Z',
      type: 'turn.completed',
      data: { stopReason: 'end_turn' }
    }
  ];

  return buildSelectedSessionReplayProjection(
    session.sessionId,
    {
      session,
      events,
      malformedLineCount: 0,
      summary: {
        eventCount: events.length,
        malformedLineCount: 0,
        eventTypeCounts: {
          'message.completed': 1,
          'turn.completed': 1
        },
        firstTimestamp: events[0].timestamp,
        lastTimestamp: events[1].timestamp
      },
      instructionHistory: [],
      instructionBases: []
    },
    {
      observedAt: '2026-07-23T01:00:00.000Z',
      currency: 'CURRENT'
    }
  );
}

describe('SelectedSessionReplayLens', () => {
  it('labels replay as read-only and renders exact provenance and attribution', () => {
    const html = renderToStaticMarkup(
      <SelectedSessionReplayLens
        state={{ status: 'READY', projection: replayProjection() }}
        primarySessionId="primary-live-session"
        onReturnToPrimary={() => {}}
      />
    );

    expect(html).toContain('Recorded chat · read-only');
    expect(html).toContain('<summary>Inspect recorded session</summary>');
    expect(html).toContain('recorded-session');
    expect(html).toContain('primary-live-session');
    expect(html).toContain('session:recorded-session/events');
    expect(html).toContain('Recorded answer');
    expect(html).toContain('recorded-model');
    expect(html).toContain('Recorded runtime status');
    expect(html).toContain('Return to primary dialogue');
  });

  it('renders the recorded reasoning effort under the model only when the record carries it', () => {
    const withEffort = renderToStaticMarkup(
      <SelectedSessionReplayLens
        state={{ status: 'READY', projection: replayProjection({ reasoningEffort: 'low' }) }}
        primarySessionId="primary-live-session"
        onReturnToPrimary={() => {}}
      />
    );
    expect(withEffort).toContain('<dt>Recorded model selection</dt><dd>recorded-model</dd><dt>Reasoning</dt><dd>low</dd>');

    const withoutEffort = renderToStaticMarkup(
      <SelectedSessionReplayLens
        state={{ status: 'READY', projection: replayProjection() }}
        primarySessionId="primary-live-session"
        onReturnToPrimary={() => {}}
      />
    );
    expect(withoutEffort).not.toContain('<dt>Reasoning</dt>');
  });

  it('exposes no historical mutation controls', () => {
    const html = renderToStaticMarkup(
      <SelectedSessionReplayLens
        state={{ status: 'READY', projection: replayProjection() }}
        onReturnToPrimary={() => {}}
      />
    );

    for (const forbidden of [
      'Send',
      'Continue',
      'Interrupt',
      'Allow',
      'Deny',
      'Resume',
      'Boot',
      'Delete'
    ]) {
      expect(html).not.toContain(`>${forbidden}<`);
    }
    expect((html.match(/<button/g) ?? [])).toHaveLength(1);
  });

  it('shows frozen instruction selection and supplied-entry hashes without progress claims', () => {
    const method = { sourceRootId: 'chirality-root', source: 'bundled' as const, kind: 'workflow' as const, name: 'project-setup' };
    const projection = {
      ...replayProjection(),
      instructionHistory: [{ schemaVersion: 'chirality.instruction-history/v1' as const, historyId: 'history-1', sessionId: 'recorded-session', sequence: 1, timestamp: '2026-09-09T00:00:00.000Z', type: 'instruction-basis.resolved' as const, basisId: 'basis-1' }],
      instructionBases: [{ schemaVersion: 'chirality.instruction-basis/v1' as const, basisId: 'basis-1', sessionId: 'recorded-session', createdAt: '2026-09-09T00:00:00.000Z', roleId: 'HELP_HUMAN' as const, interactionMode: 'chat' as const, permissionMode: 'ask' as const, selectedMethods: [method], compatibilityInputs: [], compatibilityMappings: [], suppliedEntries: [{ kind: 'method-body' as const, id: 'workflow:project-setup', content: 'frozen body', sha256: 'a'.repeat(64), method, origin: 'bundled:chirality-root', path: 'workflows/project-setup/WORKFLOW.md' }], methodDispositions: [{ method, selected: true as const, activeRoleCompatible: false, eligibleRoleIds: ['WORKING_ITEMS' as const], route: 'managed-delegation' as const }] }]
    };
    const html = renderToStaticMarkup(<SelectedSessionReplayLens state={{ status: 'READY', projection }} onReturnToPrimary={() => {}} />);
    expect(html).toContain('Instruction history');
    expect(html).toContain('workflow:project-setup');
    expect(html).toContain('bundled:chirality-root');
    expect(html).toContain('a'.repeat(64));
    expect(html).toContain('do not indicate workflow progress');
    expect(html).not.toContain('Workflow complete');
  });

  it('offers only Return and optional Retry when replay is unavailable', () => {
    const onReturn = vi.fn();
    const onRetry = vi.fn();
    const tree = renderer.create(
      <SelectedSessionReplayLens
        state={{
          status: 'UNAVAILABLE',
          selectedSessionId: 'missing-session',
          message: 'canonical replay unavailable'
        }}
        primarySessionId="primary-live-session"
        onReturnToPrimary={onReturn}
        onRetry={onRetry}
      />
    );
    const buttons = tree.root.findAllByType('button');

    expect(buttons.map((button) => button.children.join(''))).toEqual([
      'Return to primary dialogue',
      'Retry'
    ]);

    act(() => {
      buttons[0].props.onClick();
      buttons[1].props.onClick();
    });
    expect(onReturn).toHaveBeenCalledOnce();
    expect(onRetry).toHaveBeenCalledOnce();
  });

  it('keeps Return available while canonical replay evidence is loading', () => {
    const html = renderToStaticMarkup(
      <SelectedSessionReplayLens
        state={{ status: 'LOADING', selectedSessionId: 'recorded-session' }}
        primarySessionId="primary-live-session"
        onReturnToPrimary={() => {}}
      />
    );

    expect(html).toContain('Loading canonical replay evidence');
    expect(html).toContain('Return to primary dialogue');
    expect((html.match(/<button/g) ?? [])).toHaveLength(1);
  });

  it('offers continuation for an admitted v3 record and renders recorded native plan revisions', async () => {
    const qualification = { adapterId: 'native', providerId: 'provider', qualificationId: 'admitted', admissionSha256: 'a'.repeat(64), evidenceClass: 'native-adapter-qualified' as const };
    methodMocks.revisions.mockResolvedValue({ schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification,
      revisions: [{ revision: 1, sourceEvent: { qualificationState: 'qualified', eventId: 'plan-event', occurredAt: '2026-09-09T00:00:00Z', qualification, plan: 'Recorded plan body' } }] });
    const projection = replayProjection();
    projection.session!.continuation = { schemaVersion: 'chirality.session/v3', projectRoot: '/repo/project', roleId: 'WORKING_ITEMS', mode: 'governed', interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [], methodSelectionRevision: 1, instructionBasisId: 'basis-1' };
    const onContinue = vi.fn();
    let tree!: ReturnType<typeof renderer.create>;
    await act(async () => { tree = renderer.create(<SelectedSessionReplayLens state={{ status: 'READY', projection }} onReturnToPrimary={() => {}} onContinue={onContinue} />); });
    await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
    const button = tree.root.findAllByType('button').find(item => item.children.includes('Continue this chat'))!;
    act(() => button.props.onClick());
    expect(onContinue).toHaveBeenCalledWith(projection);
    expect(JSON.stringify(tree.toJSON())).toContain('Recorded plan body');
    act(() => tree.unmount());
  });
});
