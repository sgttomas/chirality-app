import { afterEach, describe, expect, it } from 'vitest';
import { createHarnessEvent } from '../../lib/harness/event-factory';
import { harnessEventToUiEvent } from '../../lib/harness/harness-ui-bridge';

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
});

describe('harnessEventToUiEvent', () => {
  it('forwards rich tool-lifecycle events as a provider-neutral harness:event passthrough', () => {
    const event = createHarnessEvent({
      sessionId: 'sess_bridge',
      type: 'tool.completed',
      data: { toolName: 'Read', toolUseId: 'toolu_1', adapterName: 'claude-agent-sdk' }
    });

    const ui = harnessEventToUiEvent(event);

    expect(ui?.type).toBe('harness:event');
    if (ui?.type !== 'harness:event') {
      throw new Error('expected a harness:event passthrough');
    }
    // The passthrough carries the same shape persisted to events.jsonl (live == replay).
    expect(ui.data).toMatchObject({
      type: 'tool.completed',
      sessionId: 'sess_bridge',
      data: { toolName: 'Read', toolUseId: 'toolu_1' }
    });
  });

  it('forwards subagent fan-out events', () => {
    const event = createHarnessEvent({
      sessionId: 'sess_bridge',
      type: 'subagent.started',
      data: { taskId: 'task_1', subagentType: 'SCHEDULE_PREP' }
    });

    expect(harnessEventToUiEvent(event)?.type).toBe('harness:event');
  });

  it('skips per-token text and boot events already covered by thin UI events', () => {
    for (const type of ['model.delta', 'message.delta', 'adapter.initialized'] as const) {
      const event = createHarnessEvent({ sessionId: 'sess_bridge', type, data: { text: 'x' } });
      expect(harnessEventToUiEvent(event)).toBeNull();
    }
  });

  it('redacts configured API keys from forwarded payloads', () => {
    const apiKey = 'sk-ant-bridge-secret-key';
    process.env.ANTHROPIC_API_KEY = apiKey;
    const event = createHarnessEvent({
      sessionId: 'sess_bridge',
      type: 'tool.failed',
      data: { message: `failed with ${apiKey}` }
    });

    const serialized = JSON.stringify(harnessEventToUiEvent(event));

    expect(serialized).toContain('[REDACTED_API_KEY]');
    expect(serialized).not.toContain(apiKey);
  });
});
