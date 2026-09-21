import { describe, expect, it } from 'vitest';
import type { ResolvedOpts, SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';
import { StubAgentSdkManager } from '../../lib/harness/agent-sdk-manager';

const session: SessionRecord = {
  sessionId: 'sess_stub_contract',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-07-22T00:00:00.000Z',
  updatedAt: '2026-07-22T00:00:00.000Z',
  // Legacy stub records can carry this ambiguous Claude-shaped field. The
  // provider-neutral stub must neither reuse nor republish it.
  claudeSessionId: 'claude_legacy_stub'
};

const opts: ResolvedOpts = {
  model: 'stub-test-model',
  tools: [],
  maxTurns: 1,
  persona: 'WORKING_ITEMS',
  mode: 'direct'
};

describe('StubAgentSdkManager provider-neutral initialization', () => {
  it('emits a stub engine session ID without Claude-only metadata', async () => {
    const manager = new StubAgentSdkManager();
    const events: UIEvent[] = [];

    for await (const event of manager.startTurn(session, 'hello', opts)) {
      events.push(event);
    }

    const init = events.find((event) => event.type === 'session:init');
    expect(init).toEqual({
      type: 'session:init',
      data: {
        engineSessionId: expect.stringMatching(/^stub_/),
        adapterId: 'stub',
        providerId: 'stub',
        model: 'stub-test-model'
      }
    });
    if (init?.type === 'session:init') {
      expect(init.data.claudeSessionId).toBeUndefined();
      expect(init.data.engineSessionId).not.toBe(session.claudeSessionId);
    }
  });
});
