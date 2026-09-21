import { describe, expect, it } from 'vitest';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import {
  derivePermissionRequests,
  deriveSubagentActivity,
  deriveToolActivity,
  selectPendingPermissionRequests
} from '../../lib/shell/harness-event-views';

let counter = 0;

function event(
  type: HarnessEventType,
  data: Record<string, unknown>,
  sessionId = 'sess_test'
): HarnessEvent {
  counter += 1;
  return {
    schemaVersion: 1,
    eventId: `evt_${counter}`,
    sessionId,
    timestamp: `2026-06-18T00:00:0${counter % 10}.000Z`,
    type,
    data
  };
}

describe('deriveToolActivity', () => {
  it('collapses the tool lifecycle into one row per toolUseId in first-seen order', () => {
    const events = [
      event('tool.queued', {
        toolUseId: 't1',
        toolName: 'Read',
        source: 'model',
        surface: 'filesystem',
        inputMetadata: { pathFields: { file_path: '/a/b.ts' } }
      }),
      event('tool.started', { toolUseId: 't1', toolName: 'Read', source: 'adapter' }),
      event('tool.completed', { toolUseId: 't1', toolName: 'Read' }),
      event('tool.queued', { toolUseId: 't2', toolName: 'Bash', source: 'model' }),
      event('tool.failed', { toolUseId: 't2', toolName: 'Bash' })
    ];

    const rows = deriveToolActivity(events);

    expect(rows.map((row) => row.key)).toEqual(['t1', 't2']);
    expect(rows[0]).toMatchObject({
      toolName: 'Read',
      status: 'completed',
      surface: 'filesystem',
      pathFields: { file_path: '/a/b.ts' },
      lastEventType: 'tool.completed',
      eventCount: 3
    });
    expect(rows[1]).toMatchObject({
      toolName: 'Bash',
      status: 'failed',
      eventCount: 2
    });
  });

  it('ignores non-tool harness events and falls back to eventId when toolUseId is absent', () => {
    const noId = event('tool.permission', { toolName: 'Write' });
    const events = [
      event('model.completed', { usage: {} }),
      event('turn.completed', {}),
      noId
    ];

    const rows = deriveToolActivity(events);

    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: noId.eventId,
      toolName: 'Write',
      status: 'permission'
    });
  });

  it('returns an empty list when there is no tool activity', () => {
    expect(deriveToolActivity([])).toEqual([]);
  });

  it('folds a summary-style completion (no toolUseId) onto the preceding rows', () => {
    const events = [
      event('tool.started', { toolUseId: 't1', toolName: 'Read' }),
      event('tool.started', { toolUseId: 't2', toolName: 'Grep' }),
      // tool_use_summary: a tool.completed that carries only precedingToolUseIds.
      event('tool.completed', { source: 'adapter', precedingToolUseIds: ['t1', 't2'] })
    ];

    const rows = deriveToolActivity(events);

    // No orphan "tool" row; both referenced rows flip to completed.
    expect(rows.map((row) => row.key)).toEqual(['t1', 't2']);
    expect(rows.every((row) => row.status === 'completed')).toBe(true);
    expect(rows.map((row) => row.toolName)).toEqual(['Read', 'Grep']);
  });

  it('keeps first-seen order even as later events update earlier rows', () => {
    const events = [
      event('tool.started', { toolUseId: 't1', toolName: 'Read' }),
      event('tool.started', { toolUseId: 't2', toolName: 'Bash' }),
      event('tool.progress', { toolUseId: 't1', toolName: 'Read' }),
      event('tool.completed', { toolUseId: 't1', toolName: 'Read' })
    ];

    expect(deriveToolActivity(events).map((row) => row.key)).toEqual(['t1', 't2']);
  });
});

describe('deriveSubagentActivity', () => {
  it('collapses the subagent lifecycle into one row per childRunId', () => {
    const events = [
      event('subagent.started', {
        childRunId: 'c1',
        agentName: 'TASK',
        description: 'Investigate the failing import'
      }),
      event('subagent.progress', {
        childRunId: 'c1',
        lastToolName: 'Grep',
        summary: 'searching for the symbol'
      }),
      event('subagent.completed', { childRunId: 'c1', outputArtifactPath: '/runs/c1.md' })
    ];

    const rows = deriveSubagentActivity(events);

    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: 'c1',
      agentName: 'TASK',
      status: 'completed',
      description: 'Investigate the failing import',
      summary: 'searching for the symbol',
      lastToolName: 'Grep',
      outputArtifactPath: '/runs/c1.md',
      eventCount: 3
    });
  });

  it('falls back to taskId for the key and subagentType for the name', () => {
    const events = [
      event('subagent.started', { taskId: 'task-9', subagentType: 'Explore' }),
      event('subagent.failed', { taskId: 'task-9', subagentType: 'Explore' })
    ];

    const rows = deriveSubagentActivity(events);

    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: 'task-9',
      agentName: 'Explore',
      status: 'failed',
      eventCount: 2
    });
  });

  it('collapses a completion that lacks childRunId onto the running row via taskId', () => {
    // The SDK mapper sets taskId on every subagent.* event but omits childRunId
    // for a task_updated completion with no output file. Keying on taskId keeps
    // the completion on the same row instead of forking an orphan.
    const events = [
      event('subagent.started', { taskId: 'task-7', childRunId: 'c7', agentName: 'TASK' }),
      event('subagent.progress', { taskId: 'task-7', childRunId: 'c7', lastToolName: 'Read' }),
      event('subagent.completed', { taskId: 'task-7', status: 'completed' })
    ];

    const rows = deriveSubagentActivity(events);

    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: 'task-7',
      agentName: 'TASK',
      status: 'completed',
      lastToolName: 'Read',
      eventCount: 3
    });
  });

  it('ignores non-subagent harness events', () => {
    expect(deriveSubagentActivity([event('tool.completed', { toolUseId: 't1' })])).toEqual([]);
  });
});

describe('derivePermissionRequests', () => {
  it('surfaces an ask as a pending request with reason and path fields', () => {
    const events = [
      event('tool.permission', {
        behavior: 'ask',
        toolUseId: 'tp1',
        toolName: 'Write',
        reason: 'requires interactive approval and write hooks before execution.',
        mode: 'ask',
        safeMetadata: { inputMetadata: { pathFields: { file_path: '/proj/x.ts' } } }
      })
    ];

    const rows = derivePermissionRequests(events);

    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({
      key: 'tp1',
      sessionId: 'sess_test',
      toolName: 'Write',
      status: 'pending',
      mode: 'ask',
      pathFields: { file_path: '/proj/x.ts' }
    });
  });

  it('resolves the same request when the operator verdict follows', () => {
    const allowed = derivePermissionRequests([
      event('tool.permission', { behavior: 'ask', toolUseId: 'tp1', toolName: 'Write' }),
      event('tool.permission', { behavior: 'allow', toolUseId: 'tp1', toolName: 'Write', source: 'human' })
    ]);
    expect(allowed).toHaveLength(1);
    expect(allowed[0].status).toBe('allowed');

    const denied = derivePermissionRequests([
      event('tool.permission', { behavior: 'ask', toolUseId: 'tp2', toolName: 'Bash' }),
      event('tool.permission', { behavior: 'deny', toolUseId: 'tp2', toolName: 'Bash', source: 'human' })
    ]);
    expect(denied[0].status).toBe('denied');
  });

  it('ignores straight policy allows/denies that never paused on ask', () => {
    const rows = derivePermissionRequests([
      event('tool.permission', { behavior: 'allow', toolUseId: 'auto1', toolName: 'Read' }),
      event('tool.permission', { behavior: 'deny', toolUseId: 'auto2', toolName: 'Bash' })
    ]);
    expect(rows).toEqual([]);
  });

  it('captures the owning session per request from a non-default session id', () => {
    // A distinct session id proves the row tracks event.sessionId rather than a
    // constant or the wrong field (DESIGN §5.3 item b).
    const rows = derivePermissionRequests([
      event(
        'tool.permission',
        { behavior: 'ask', toolUseId: 'tp9', toolName: 'Write' },
        'sess_owner_9'
      )
    ]);
    expect(rows).toHaveLength(1);
    expect(rows[0].sessionId).toBe('sess_owner_9');
  });
});

describe('selectPendingPermissionRequests', () => {
  const askEvents = [
    event('tool.permission', {
      behavior: 'ask',
      toolUseId: 'tp1',
      toolName: 'Write',
      reason: 'requires interactive approval and write hooks before execution.'
    })
  ];

  it('surfaces pending requests while the turn is live (active)', () => {
    const rows = selectPendingPermissionRequests(askEvents, true);
    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({ key: 'tp1', status: 'pending' });
  });

  it('surfaces nothing once the turn has ended (inactive), even with a pending event', () => {
    expect(selectPendingPermissionRequests(askEvents, false)).toEqual([]);
  });

  it('drops a request that has resolved while still active', () => {
    const resolved = [
      ...askEvents,
      event('tool.permission', {
        behavior: 'allow',
        toolUseId: 'tp1',
        toolName: 'Write',
        source: 'human'
      })
    ];
    expect(selectPendingPermissionRequests(resolved, true)).toEqual([]);
  });
});
