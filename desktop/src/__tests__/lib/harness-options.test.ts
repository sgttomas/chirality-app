import { afterEach, describe, expect, it, vi } from 'vitest';
import { resolveRuntimeOptions } from '../../lib/harness/options';
import type { HarnessOpts, SessionRecord } from '@chirality/runtime-contracts/types';

const session: SessionRecord = {
  sessionId: 'sess_test',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-09-09T00:00:00.000Z',
  updatedAt: '2026-09-09T00:00:00.000Z'
};

afterEach(() => vi.restoreAllMocks());

describe('resolveRuntimeOptions compatibility defaults', () => {
  it('does not parse instruction Markdown for model, tools, or turn defaults', async () => {
    await expect(resolveRuntimeOptions(session)).resolves.toMatchObject({
      model: 'haiku',
      tools: ['read', 'write', 'bash'],
      maxTurns: 12,
      persona: 'WORKING_ITEMS',
      mode: 'direct'
    });
  });

  it('preserves explicit legacy overrides', async () => {
    await expect(resolveRuntimeOptions(session, {
      model: 'chosen', tools: [], maxTurns: 4, persona: 'TASK', mode: 'ask'
    })).resolves.toMatchObject({
      model: 'chosen', tools: [], maxTurns: 4, persona: 'TASK', mode: 'ask'
    });
  });

  it('passes governance compatibility input through and warns on unknown fields', async () => {
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const subagentGovernance = { contextSealed: true };
    const opts = { subagentGovernance, stale: true } as unknown as HarnessOpts;
    await expect(resolveRuntimeOptions(session, opts)).resolves.toMatchObject({ subagentGovernance });
    expect(warn).toHaveBeenCalledWith('[harness/options] Ignoring unknown opts field(s): stale');
  });
});
