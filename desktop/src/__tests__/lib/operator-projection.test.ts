import { describe, expect, it } from 'vitest';
import type { SessionRecord } from '@chirality/runtime-contracts/types';
import {
  buildOperatorSessionProjection,
  projectOperatorSession
} from '../../lib/woven-dialogue/operator-projection';

function session(
  sessionId: string,
  overrides: Partial<SessionRecord> & Record<string, unknown> = {}
): SessionRecord {
  return {
    sessionId,
    projectRoot: '/repo/project',
    persona: 'WORKING_ITEMS',
    mode: 'governed',
    createdAt: '2026-07-23T00:00:00.000Z',
    updatedAt: '2026-07-23T00:00:00.000Z',
    ...overrides
  };
}

describe('operator session projection', () => {
  it('uses exact recorded parentage and provider-neutral attribution fields', () => {
    const parent = session('parent', {
      role: 'agent1',
      agentType: 1,
      status: 'running',
      engineSelection: {
        adapterId: 'pi',
        providerId: 'omlx',
        model: 'local-model'
      },
      residencyEpoch: 'epoch-7'
    });
    const child = session('child', {
      persona: 'TASK',
      role: 'agent2',
      parentSessionId: 'parent',
      status: 'completed',
      outputArtifact: 'runs/child/RETURN.md',
      approvalRef: 'OWNER-1'
    });

    const result = buildOperatorSessionProjection([parent, child], {
      observedAt: '2026-07-23T01:00:00.000Z',
      currencyBySessionId: { parent: 'CURRENT', child: 'CURRENT' }
    });

    expect(result.sessions[0]).toMatchObject({
      sessionId: 'parent',
      role: 'agent1',
      runtimeStatus: 'running',
      adapterId: 'pi',
      providerId: 'omlx',
      model: 'local-model',
      residencyEpoch: 'epoch-7',
      parentage: { state: 'NOT_RECORDED' }
    });
    expect(result.sessions[1]).toMatchObject({
      sessionId: 'child',
      role: 'agent2',
      runtimeStatus: 'completed',
      parentage: {
        state: 'RECORDED',
        parentSessionId: 'parent',
        parentAvailable: true
      },
      outputArtifactReference: 'runs/child/RETURN.md',
      approvalEvidenceReference: 'OWNER-1'
    });
  });

  it('does not infer role, parentage, status, model, or currency from persona and time', () => {
    const projected = projectOperatorSession(
      session('untyped', {
        persona: 'TASK',
        createdAt: '2020-01-01T00:00:00.000Z',
        model: undefined
      }),
      new Set(['untyped']),
      { observedAt: '2026-07-23T01:00:00.000Z' }
    );

    expect(projected).toMatchObject({
      sessionId: 'untyped',
      persona: 'TASK',
      currency: 'UNKNOWN',
      parentage: { state: 'NOT_RECORDED' }
    });
    expect(projected.role).toBeUndefined();
    expect(projected.runtimeStatus).toBeUndefined();
    expect(projected.model).toBeUndefined();
  });

  it('preserves an unresolved exact parent identifier without inventing an edge target', () => {
    const result = buildOperatorSessionProjection(
      [session('child', { parentSessionId: 'missing-parent' })],
      { observedAt: '2026-07-23T01:00:00.000Z' }
    );

    expect(result.sessions[0].parentage).toEqual({
      state: 'RECORDED',
      parentSessionId: 'missing-parent',
      parentAvailable: false
    });
  });

  it('fails closed on conflicting role fields and duplicate session records', () => {
    const first = session('conflict', {
      role: 'agent1',
      agentType: 2,
      status: 'running'
    });
    const second = session('conflict', {
      role: 'agent1',
      agentType: 1,
      status: 'completed'
    });

    const result = buildOperatorSessionProjection([first, second], {
      observedAt: '2026-07-23T01:00:00.000Z',
      currencyBySessionId: { conflict: 'CURRENT' }
    });

    expect(result.sessions).toHaveLength(1);
    expect(result.sessions[0].currency).toBe('CONFLICTING');
    expect(result.sessions[0].role).toBeUndefined();
    expect(result.sessions[0].diagnostics.map(({ code }) => code)).toEqual(
      expect.arrayContaining([
        'CONFLICTING_SESSION_RECORDS',
        'CONFLICTING_RECORDED_ROLE'
      ])
    );
    expect(result.diagnostics.map(({ code }) => code)).toContain(
      'CONFLICTING_SESSION_RECORDS'
    );
  });

  it('offers continuation only for a complete canonical v3 session record, running ones included so a reopened chat re-attaches to its turn', () => {
    const selectedMethod = { kind: 'workflow', name: 'project-setup', source: 'bundled', sourceRootId: 'chirality-root' };
    const v3 = session('v3', {
      schemaVersion: 'chirality.session/v3', role: 'agent1', agentType: 1, roleId: 'WORKING_ITEMS', status: 'completed',
      interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [selectedMethod], methodSelectionRevision: 3,
      instructionBasisId: 'basis-3'
    });
    expect(projectOperatorSession(v3, new Set(['v3']), { observedAt: '2026-09-09' }).bootstrapConfirmed).toBe(false);
    expect(projectOperatorSession({ ...v3, bootedAt: '2026-09-09', bootFingerprint: 'confirmed', engineSessionId: 'native' }, new Set(['v3']), { observedAt: '2026-09-09' }).bootstrapConfirmed).toBe(true);
    expect(projectOperatorSession(v3, new Set(['v3']), { observedAt: '2026-09-09' }).continuation).toEqual({
      schemaVersion: 'chirality.session/v3', projectRoot: '/repo/project', roleId: 'WORKING_ITEMS', mode: 'governed',
      interactionMode: 'chat', permissionMode: 'ask', selectedMethods: [selectedMethod], methodSelectionRevision: 3,
      instructionBasisId: 'basis-3'
    });
    expect(projectOperatorSession(session('running', { ...v3, sessionId: 'running', status: 'running' }), new Set(['running']), { observedAt: '2026-09-09' }).continuation).toMatchObject({ roleId: 'WORKING_ITEMS', instructionBasisId: 'basis-3' });
    expect(projectOperatorSession(session('legacy'), new Set(['legacy']), { observedAt: '2026-09-09' }).continuation).toBeUndefined();
    expect(projectOperatorSession(session('task', { ...v3, sessionId: 'task', role: 'agent2', agentType: 2, roleId: 'TASK' }), new Set(['task']), { observedAt: '2026-09-09' }).continuation).toBeUndefined();
  });

  it('projects the recorded session-fixed reasoning effort beside the model without inferring either', () => {
    const recorded = session('codex', {
      engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-alt' },
      reasoningEffort: 'low'
    });
    const projected = projectOperatorSession(recorded, new Set(['codex']), { observedAt: '2026-09-09' });
    expect(projected.model).toBe('gpt-alt');
    expect(projected.reasoningEffort).toBe('low');

    const withoutEffort = projectOperatorSession(session('legacy', {
      engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-default' }
    }), new Set(['legacy']), { observedAt: '2026-09-09' });
    expect(withoutEffort.model).toBe('gpt-default');
    expect(withoutEffort).not.toHaveProperty('reasoningEffort');
    expect(projectOperatorSession(session('blank', { reasoningEffort: '   ' }), new Set(['blank']), { observedAt: '2026-09-09' })).not.toHaveProperty('reasoningEffort');
    expect(projectOperatorSession(session('typed', { reasoningEffort: 3 }), new Set(['typed']), { observedAt: '2026-09-09' })).not.toHaveProperty('reasoningEffort');

    // Effort changes the signature so a conflicting duplicate is detected, as for the model.
    const conflict = buildOperatorSessionProjection([recorded, session('codex', {
      engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-alt' }, reasoningEffort: 'high'
    })], { observedAt: '2026-09-09' });
    expect(conflict.sessions[0]?.currency).toBe('CONFLICTING');
  });
});

it.each([
  { adapterId: 'codex-app-server', schemaVersion: 'chirality.session/v3', bootedAt: '2026-09-13', bootFingerprint: 'boot-proof', expected: true },
  { adapterId: 'codex-app-server', schemaVersion: 'chirality.session/v3', bootedAt: '2026-09-13', bootFingerprint: '', expected: false },
  { adapterId: 'codex-app-server', schemaVersion: 'chirality.session/v3', bootedAt: '', bootFingerprint: 'boot-proof', expected: false },
  { adapterId: 'claude-agent-sdk', schemaVersion: 'chirality.session/v3', bootedAt: '2026-09-13', bootFingerprint: 'boot-proof', expected: false },
  { adapterId: 'future-engine', schemaVersion: 'chirality.session/v3', bootedAt: '2026-09-13', bootFingerprint: 'boot-proof', expected: false }
])('projects boot:none readiness without inventing a provider thread: %j', ({ expected, adapterId, ...boot }) => {
  const record = session('pre-provider', { ...boot, engineSelection: { adapterId, providerId: 'openai', model: 'configured-model' } });
  expect(projectOperatorSession(record, new Set(['pre-provider']), { observedAt: '2026-09-13' }).bootstrapConfirmed).toBe(expected);
});
