import { describe, expect, it } from 'vitest';
import { PUBLIC_UI_EVENT_NAMES } from '@chirality/runtime-contracts/agent-engine-port';

describe('agent engine port contract', () => {
  it('keeps browser UI event names stable and provider-neutral', () => {
    expect(PUBLIC_UI_EVENT_NAMES).toEqual([
      'session:init',
      'chat:delta',
      'chat:complete',
      'tool:result',
      'session:complete',
      'turn:error',
      'process:exit',
      'harness:event'
    ]);
    expect(PUBLIC_UI_EVENT_NAMES.join(' ')).not.toMatch(/sdk|anthropic|claude/i);
  });
});
