import { describe, expect, it } from 'vitest';
import {
  createPiEventMapperState,
  mapPiSessionEvent
} from '../../lib/harness/pi-event-mapper';

describe('mapPiSessionEvent', () => {
  it('maps compaction lifecycle without making it a process terminal', () => {
    const state = createPiEventMapperState();

    expect(mapPiSessionEvent({ type: 'compaction_start', reason: 'threshold' }, state)).toEqual([
      {
        kind: 'harness',
        type: 'context.compaction.started',
        data: { reason: 'threshold', source: 'pi' }
      }
    ]);
    expect(
      mapPiSessionEvent(
        {
          type: 'compaction_end',
          reason: 'threshold',
          aborted: false,
          willRetry: false,
          result: { summary: 'bounded' }
        },
        state
      )
    ).toEqual([
      {
        kind: 'harness',
        type: 'context.compacted',
        data: {
          reason: 'threshold',
          aborted: false,
          willRetry: false,
          source: 'pi'
        }
      }
    ]);
  });

  it('classifies context exhaustion from Pi provider errors', () => {
    const state = createPiEventMapperState();

    expect(
      mapPiSessionEvent(
        {
          type: 'message_update',
          assistantMessageEvent: {
            type: 'error',
            error: { errorMessage: 'maximum context length exceeded' }
          }
        },
        state
      )
    ).toEqual([]);
    expect(state.failure).toEqual({
      errorType: 'CONTEXT_EXHAUSTED',
      message: 'maximum context length exceeded',
      status: 422
    });
  });

  it('leaves persisted tool evidence to the neutral bridge and emits only safe UI metadata', () => {
    const state = createPiEventMapperState();
    const sensitivePath = '/project/private/omlx-secret-key.txt';
    const sensitiveResult = 'file contents with omlx-secret-key';

    expect(
      mapPiSessionEvent(
        {
          type: 'tool_execution_start',
          toolCallId: 'tool_sensitive',
          toolName: 'read_file',
          args: { file_path: sensitivePath }
        },
        state
      )
    ).toEqual([]);
    expect(
      mapPiSessionEvent(
        {
          type: 'tool_execution_update',
          toolCallId: 'tool_sensitive',
          toolName: 'read_file',
          partialResult: { content: [{ type: 'text', text: sensitiveResult }] }
        },
        state
      )
    ).toEqual([]);

    const completed = mapPiSessionEvent(
      {
        type: 'tool_execution_end',
        toolCallId: 'tool_sensitive',
        toolName: 'read_file',
        result: { content: [{ type: 'text', text: sensitiveResult }] },
        isError: false
      },
      state
    );

    expect(completed).toEqual([
      {
        kind: 'ui',
        event: { type: 'tool:result', data: { name: 'read_file', ok: true } }
      }
    ]);
    expect(JSON.stringify(completed)).not.toContain(sensitivePath);
    expect(JSON.stringify(completed)).not.toContain(sensitiveResult);
    expect(completed.some((event) => event.kind === 'harness')).toBe(false);
  });
});
