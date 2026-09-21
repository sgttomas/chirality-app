import { describe, expect, it } from 'vitest';
import { buildRecordedAgentHierarchy } from '../../lib/woven-dialogue/recorded-agent-hierarchy';

describe('recorded agent hierarchy projection', () => {
  it('builds hierarchy edges only from exact recorded parentSessionId values', () => {
    const hierarchy = buildRecordedAgentHierarchy([
      {
        sessionId: 'parent',
        sourceReference: 'session:parent',
        observedAt: '2026-07-23T10:00:00Z',
        currency: 'CURRENT',
        persona: 'WORKING_ITEMS',
        role: 'agent1',
        status: 'running'
      },
      {
        sessionId: 'child',
        parentSessionId: 'parent',
        sourceReference: 'session:child',
        observedAt: '2026-07-23T10:01:00Z',
        currency: 'CURRENT',
        persona: 'TASK',
        role: 'agent2',
        status: 'idle'
      }
    ]);

    expect(hierarchy.roots.map((session) => session.sessionId)).toEqual(['parent']);
    expect(
      hierarchy.childrenByParentSessionId.parent.map((session) => session.sessionId)
    ).toEqual(['child']);
    expect(hierarchy.childrenByParentSessionId.parent[0].parentage).toEqual({
      state: 'RECORDED',
      parentSessionId: 'parent',
      parentAvailable: true
    });
  });

  it('retains exact unresolved parent identifiers in a detached evidence group', () => {
    const hierarchy = buildRecordedAgentHierarchy([
      {
        sessionId: 'child',
        parentSessionId: 'missing-parent',
        sourceReference: 'session:child',
        observedAt: '2026-07-23T10:01:00Z'
      }
    ]);

    expect(hierarchy.roots).toEqual([]);
    expect(hierarchy.detached.map((session) => session.sessionId)).toEqual(['child']);
    expect(hierarchy.unresolvedParentSessionIds).toEqual(['missing-parent']);
    expect(hierarchy.childrenByParentSessionId['missing-parent'][0].diagnostics).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ code: 'PARENT_SESSION_UNAVAILABLE' })
      ])
    );
  });

  it('keeps cyclic parentage inspectable without inventing a hierarchy root', () => {
    const hierarchy = buildRecordedAgentHierarchy([
      {
        sessionId: 'first',
        parentSessionId: 'second',
        sourceReference: 'session:first',
        observedAt: '2026-07-23T10:01:00Z'
      },
      {
        sessionId: 'second',
        parentSessionId: 'first',
        sourceReference: 'session:second',
        observedAt: '2026-07-23T10:02:00Z'
      }
    ]);

    expect(hierarchy.roots).toEqual([]);
    expect(hierarchy.detached.map((session) => session.sessionId)).toEqual([
      'first',
      'second'
    ]);
  });

  it('does not infer role, status, parentage, model, or currency from persona or timestamps', () => {
    const hierarchy = buildRecordedAgentHierarchy([
      {
        sessionId: 'session-1',
        sourceReference: 'session:1',
        observedAt: '2026-07-23T10:00:00Z',
        persona: 'TASK'
      }
    ]);
    const projection = hierarchy.roots[0];

    expect(projection.persona).toBe('TASK');
    expect(projection.role).toBeUndefined();
    expect(projection.runtimeStatus).toBeUndefined();
    expect(projection.model).toBeUndefined();
    expect(projection.currency).toBe('UNKNOWN');
    expect(projection.parentage).toEqual({ state: 'NOT_RECORDED' });
  });

  it('marks duplicate session records conflicting instead of merging their claims', () => {
    const hierarchy = buildRecordedAgentHierarchy([
      {
        sessionId: 'duplicate',
        sourceReference: 'source:a',
        observedAt: '2026-07-23T10:00:00Z',
        role: 'agent1'
      },
      {
        sessionId: 'duplicate',
        sourceReference: 'source:b',
        observedAt: '2026-07-23T10:01:00Z',
        role: 'agent2'
      }
    ]);

    expect(hierarchy.roots).toHaveLength(1);
    expect(hierarchy.roots[0].role).toBe('agent1');
    expect(hierarchy.roots[0].currency).toBe('CONFLICTING');
    expect(hierarchy.diagnostics).toEqual(
      expect.arrayContaining([expect.objectContaining({ code: 'DUPLICATE_SESSION_ID' })])
    );
  });
});
