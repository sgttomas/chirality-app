import type { SDKMessage } from '@anthropic-ai/claude-agent-sdk';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ClaudeAgentSdkManager } from '../../lib/harness/claude-agent-sdk-manager';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import {
  getPermissionEventChannel,
  resetPermissionEventChannelForTests
} from '../../lib/harness/permission-event-channel';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { ResolvedOpts, SessionRecord } from '@chirality/runtime-contracts/types';
import type { AgentEngineRunInput } from '@chirality/runtime-contracts/agent-engine-port';

async function* createSdkStream(events: SDKMessage[]): AsyncGenerator<SDKMessage, void> {
  for (const event of events) {
    yield event;
  }
}

function createQuery(events: SDKMessage[]) {
  const stream = createSdkStream(events) as AsyncGenerator<SDKMessage, void> & {
    interrupt: () => Promise<void>;
    close: () => void;
  };
  stream.interrupt = vi.fn(async () => undefined);
  stream.close = vi.fn();
  return vi.fn(() => stream);
}

const session: SessionRecord = {
  sessionId: 'sess_sdk',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-02-23T00:00:00.000Z',
  updatedAt: '2026-02-23T00:00:00.000Z'
};

const opts: ResolvedOpts = {
  model: 'claude-test',
  tools: [],
  maxTurns: 2,
  persona: 'WORKING_ITEMS',
  mode: 'direct'
};

const executionRoots = {
  workingRoot: { path: session.projectRoot, origin: 'registered-project-root' as const, identitySha256: '1'.repeat(64) },
  toolRoot: { path: '/tmp/trusted-instruction-root', origin: 'trusted-runtime-instruction-root' as const, identitySha256: '2'.repeat(64) }
};

let tmpDir = '';
const GLOBAL_API_KEY = '__CHIRALITY_UI_API_KEY__';
const apiKeyGlobal = globalThis as typeof globalThis & Record<typeof GLOBAL_API_KEY, string | undefined>;

afterEach(async () => {
  delete apiKeyGlobal[GLOBAL_API_KEY];
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_SESSION_ROOT;
  resetPermissionEventChannelForTests();
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('ClaudeAgentSdkManager', () => {
  it('prepares a reversible successor and starts it with a fresh provider identity', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-successor-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const query = createQuery([{
      type: 'system', subtype: 'init', session_id: 'sdk_successor',
      uuid: '00000000-0000-0000-0000-000000000089', apiKeySource: 'temporary',
      claude_code_version: '1.2.3', cwd: '/tmp/project', tools: [], mcp_servers: [],
      model: 'claude-test', permissionMode: 'default', slash_commands: [],
      output_style: 'default', skills: [], plugins: []
    }, {
      type: 'result', subtype: 'success', duration_ms: 1, duration_api_ms: 1,
      is_error: false, num_turns: 1, result: 'continued', stop_reason: 'end_turn',
      total_cost_usd: 0, usage: {} as never, modelUsage: {}, permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000088', session_id: 'sdk_successor'
    }]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'new frozen role and method body');
    const predecessor = { ...session, sdkSessionId: 'sdk_predecessor', engineSessionId: 'sdk_predecessor' };
    const request = {
      sessionId: session.sessionId,
      predecessorEngineSessionId: 'sdk_predecessor',
      fromBasisId: 'basis-old',
      toBasisPreview: { id: 'basis-new', sha256: 'a'.repeat(64) },
      continuationContext: {
        transcript: '[{"role":"user","text":"prior human"},{"role":"assistant","text":"prior assistant"}]', sha256: 'b'.repeat(64),
        priorBasisRefs: [{ basisId: 'basis-old', sha256: 'c'.repeat(64) }]
      }
    };
    const cancelled = await manager.prepareContextSuccessor(request);
    await expect(manager.cancelContextSuccessor(cancelled.preparationId)).resolves.toBeUndefined();

    const predecessorQuery = createQuery([{
      type: 'result', subtype: 'success', duration_ms: 1, duration_api_ms: 1,
      is_error: false, num_turns: 1, result: 'old', stop_reason: 'end_turn',
      total_cost_usd: 0, usage: {} as never, modelUsage: {}, permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000087', session_id: 'sdk_predecessor'
    }]);
    const predecessorManager = new ClaudeAgentSdkManager(predecessorQuery as never, async () => 'old prompt');
    for await (const _event of predecessorManager.startTurn({ session: predecessor, message: 'still usable', opts, turnId: 'old-turn' })) { /* exhaust */ }
    const predecessorCall = (predecessorQuery.mock.calls as unknown[][])[0]?.[0] as { options: { resume?: string } };
    expect(predecessorCall.options.resume).toBe('sdk_predecessor');

    const prepared = await manager.prepareContextSuccessor(request);
    const events = [];
    for await (const event of manager.startTurn({
      session: predecessor, message: 'new request', opts, turnId: 'new-turn', contextSuccessor: prepared
    })) events.push(event);
    expect(events[0]).toMatchObject({ type: 'session:init', data: { adapterId: 'claude-agent-sdk' } });
    expect((events[0] as { data: { engineSessionId: string } }).data.engineSessionId).not.toBe('sdk_predecessor');
    const successorCall = (query.mock.calls as unknown[][])[0]?.[0] as { options: { resume?: string }; prompt: string };
    expect(successorCall.options.resume).toBeUndefined();
    expect(successorCall.prompt).toContain('basis-old');
    expect(successorCall.prompt).toContain('basis-new');
    expect(successorCall.prompt).toContain('prior human');
    expect(successorCall.prompt).toContain('prior assistant');
    expect(successorCall.prompt).toContain('new request');
    expect(successorCall.prompt).not.toContain('old prompt');
    expect(prepared.continuationSha256).toMatch(/^[a-f0-9]{64}$/);

    const nextQuery = createQuery([{
      type: 'result', subtype: 'success', duration_ms: 1, duration_api_ms: 1,
      is_error: false, num_turns: 1, result: 'next', stop_reason: 'end_turn',
      total_cost_usd: 0, usage: {} as never, modelUsage: {}, permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000086', session_id: 'sdk_successor'
    }]);
    const nextManager = new ClaudeAgentSdkManager(nextQuery as never, async () => 'new frozen role and method body');
    const migratedAfterSuccessor = {
      ...predecessor,
      engineSessionId: 'sdk_successor',
      claudeSessionId: 'sdk_successor',
      sdkSessionId: 'sdk_predecessor'
    };
    for await (const _event of nextManager.startTurn({ session: migratedAfterSuccessor, message: 'third turn', opts, turnId: 'third-turn' })) { /* exhaust */ }
    const nextCall = (nextQuery.mock.calls as unknown[][])[0]?.[0] as { options: { resume?: string } };
    expect(nextCall.options.resume).toBe('sdk_successor');
  });

  it('passes only Runtime-supplied instructions and tools to the real SDK adapter boundary', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-runtime-context-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const query = createQuery([{
      type: 'result', subtype: 'success', duration_ms: 1, duration_api_ms: 1,
      is_error: false, num_turns: 1, result: 'done', stop_reason: 'end_turn',
      total_cost_usd: 0, usage: {} as never, modelUsage: {}, permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000099', session_id: 'sdk_context'
    }]);
    const promptBuilder = vi.fn(async (_root, _persona, _mode, _tools, supplied) => supplied ?? 'legacy');
    const manager = new ClaudeAgentSdkManager(query as never, promptBuilder);
    const execute = vi.fn(async () => ({ methods: [] }));
    const input: AgentEngineRunInput = {
      session,
      message: 'work normally',
      opts,
      turnId: 'turn_runtime_context',
      contentBlocks: [{ type: 'text', text: 'ordinary attachment body' }],
      instructionContext: {
        schemaVersion: 'chirality.selected-context/v3',
        roleId: 'HELP_HUMAN', methods: [], documents: [], dispositions: [],
        supplied: [
          { kind: 'root', id: 'AGENTS.md', content: 'root overview', sha256: 'a'.repeat(64) },
          { kind: 'role', id: 'HELP_HUMAN', content: 'active helper body', sha256: 'b'.repeat(64) },
          { kind: 'method-body', id: 'workflow:central', content: 'selected workflow body', sha256: 'c'.repeat(64) }
        ],
        executionRoots,
        basisPreview: { id: 'basis-1', sha256: 'd'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false },
        compatibilityInputs: [], compatibilityMappings: []
      },
      runtimeTools: [{
        name: 'chirality_list_methods', description: 'List methods',
        inputSchema: { type: 'object', additionalProperties: false },
        permission: { effect: 'allow', operation: 'read' }, execute
      }]
    };

    for await (const _event of manager.startTurn(input)) { /* exhaust */ }

    const supplied = promptBuilder.mock.calls[0]?.[4] as string;
    expect(supplied).toContain('active helper body');
    expect(supplied).toContain('selected workflow body');
    expect(supplied).not.toContain('ordinary attachment body');
    expect(query).toHaveBeenCalledWith(expect.objectContaining({
      prompt: expect.stringContaining('ordinary attachment body'),
      options: expect.objectContaining({
        systemPrompt: expect.objectContaining({ append: supplied }),
        allowedTools: expect.arrayContaining(['mcp__chirality_runtime__chirality_list_methods']),
        mcpServers: expect.objectContaining({ chirality_runtime: expect.anything() })
      })
    }));
  });

  it('maps SDK stream messages to existing UI events and appends HarnessEvent evidence', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-manager-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const query = createQuery([
      {
        type: 'system',
        subtype: 'init',
        session_id: 'sdk_1',
        uuid: '00000000-0000-0000-0000-000000000001',
        apiKeySource: 'temporary',
        claude_code_version: '1.2.3',
        cwd: '/tmp/project',
        tools: [],
        mcp_servers: [],
        model: 'claude-test',
        permissionMode: 'default',
        slash_commands: [],
        output_style: 'default',
        skills: [],
        plugins: []
      },
      {
        type: 'stream_event',
        event: {
          type: 'content_block_delta',
          index: 0,
          delta: { type: 'text_delta', text: 'Hi' }
        },
        parent_tool_use_id: null,
        uuid: '00000000-0000-0000-0000-000000000002',
        session_id: 'sdk_1'
      },
      {
        type: 'result',
        subtype: 'success',
        duration_ms: 10,
        duration_api_ms: 9,
        is_error: false,
        num_turns: 1,
        result: 'Hi',
        stop_reason: 'end_turn',
        total_cost_usd: 0,
        usage: {} as never,
        modelUsage: {},
        permission_denials: [],
        uuid: '00000000-0000-0000-0000-000000000003',
        session_id: 'sdk_1'
      }
    ]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');
    const events = [];

    for await (const event of manager.startTurn(session, 'hello', opts)) {
      events.push(event);
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event',
      'chat:delta',
      'harness:event',
      'harness:event',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);
    // The rich harness events bridge to the live stream before the terminal uiEvents.
    // turn.accepted / turn.started bridge immediately after session:init (D-APP-25),
    // then model.completed / turn.completed from the result message.
    const harnessEventTypes = events
      .filter((event) => event.type === 'harness:event')
      .map((event) => event.data.type);
    expect(harnessEventTypes).toEqual([
      'turn.accepted',
      'turn.started',
      'model.completed',
      'turn.completed'
    ]);
    expect(query).toHaveBeenCalledWith(
      expect.objectContaining({
        prompt: 'hello',
        options: expect.objectContaining({
          settingSources: [],
          tools: [],
          allowedTools: []
        })
      })
    );
    const replay = await replayHarnessEvents('sess_sdk');
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'model.delta',
      'message.delta',
      'model.completed',
      'turn.completed'
    ]);
    expect(replay.events[0].data).toMatchObject({
      provider: 'claude-agent-sdk',
      sdkPackageVersion: '0.3.150',
      persona: 'WORKING_ITEMS',
      mode: 'direct',
      model: 'claude-test',
      personaPromptHash: expect.stringMatching(/^[a-f0-9]{64}$/)
    });
  });

  it('keeps the retired Agent bridge absent from SDK options', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-manager-agent-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const query = createQuery([
      {
        type: 'result',
        subtype: 'success',
        duration_ms: 10,
        duration_api_ms: 9,
        is_error: false,
        num_turns: 1,
        result: 'done',
        stop_reason: 'end_turn',
        total_cost_usd: 0,
        usage: {} as never,
        modelUsage: {},
        permission_denials: [],
        uuid: '00000000-0000-0000-0000-000000000004',
        session_id: 'sdk_1'
      }
    ]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');

    for await (const _event of manager.startTurn(session, 'delegate', {
      ...opts,
      mode: 'workspaceWrite',
      tools: ['Agent'],
      delegatedSubagents: ['TASK']
    })) {
      // Exhaust the stream.
    }

    expect(query).toHaveBeenCalledWith(
      expect.objectContaining({
        options: expect.objectContaining({
          tools: [],
          allowedTools: [],
          disallowedTools: expect.arrayContaining(['Agent']),
          agents: undefined
        })
      })
    );
  });

  it('injects active API key into SDK env, restores prior env, and redacts persisted failures', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-manager-api-key-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    const priorApiKey = 'prior-env-key-stab02';
    const uiApiKey = 'ui-active-turn-key-stab02';
    process.env.ANTHROPIC_API_KEY = priorApiKey;
    apiKeyGlobal[GLOBAL_API_KEY] = uiApiKey;
    const observedApiKeys: Array<string | undefined> = [];
    const query = vi.fn(() => {
      observedApiKeys.push(process.env.ANTHROPIC_API_KEY);
      throw new Error(`SDK failed with ${uiApiKey}`);
    });
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');
    const events: unknown[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts)) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 500,
      message: 'SDK failed with [REDACTED_API_KEY]'
    });
    // The synchronous SDK failure bridges a redacted turn.failed before throwing
    // (D-APP-25). turn.accepted was buffered but never flushed (no session:init),
    // so it stays persisted-only — the live stream carries only turn.failed.
    expect(events.map((event) => (event as { type: string }).type)).toEqual(['harness:event']);
    expect((events[0] as { data: { type: string } }).data.type).toBe('turn.failed');
    expect(observedApiKeys).toEqual([uiApiKey]);
    expect(process.env.ANTHROPIC_API_KEY).toBe(priorApiKey);
    const replay = await replayHarnessEvents('sess_sdk');
    expect(replay.events.map((event) => event.type)).toEqual(['turn.accepted', 'turn.failed']);
    const serializedEvents = JSON.stringify(replay.events);
    expect(serializedEvents).toContain('[REDACTED_API_KEY]');
    expect(serializedEvents).not.toContain(uiApiKey);
    expect(serializedEvents).not.toContain(priorApiKey);
  });

  it('bridges out-of-band permission events into the live stream while the SDK is paused', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-sdk-manager-perm-'));
    process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
    resetPermissionEventChannelForTests();

    const initMessage: SDKMessage = {
      type: 'system',
      subtype: 'init',
      session_id: 'sdk_1',
      uuid: '00000000-0000-0000-0000-0000000000a1',
      apiKeySource: 'temporary',
      claude_code_version: '1.2.3',
      cwd: '/tmp/project',
      tools: [],
      mcp_servers: [],
      model: 'claude-test',
      permissionMode: 'default',
      slash_commands: [],
      output_style: 'default',
      skills: [],
      plugins: []
    };
    const resultMessage: SDKMessage = {
      type: 'result',
      subtype: 'success',
      duration_ms: 10,
      duration_api_ms: 9,
      is_error: false,
      num_turns: 1,
      result: 'done',
      stop_reason: 'end_turn',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      uuid: '00000000-0000-0000-0000-0000000000a3',
      session_id: 'sdk_1'
    };
    const permissionEvent: HarnessEvent = {
      schemaVersion: 1,
      eventId: 'evt_perm_1',
      sessionId: 'sess_sdk',
      timestamp: '2026-06-18T00:00:00.000Z',
      type: 'tool.permission',
      data: { behavior: 'ask', toolUseId: 'tp1', toolName: 'Write' }
    };

    async function* scriptedWithPause(): AsyncGenerator<SDKMessage, void> {
      yield initMessage;
      // Simulate canUseTool publishing while the SDK is suspended awaiting a verdict:
      // the channel resolves while the SDK iterator stays pending.
      getPermissionEventChannel().publish('sess_sdk', permissionEvent);
      await new Promise((resolve) => setTimeout(resolve, 10));
      yield resultMessage;
    }

    const stream = scriptedWithPause() as AsyncGenerator<SDKMessage, void> & {
      interrupt: () => Promise<void>;
      close: () => void;
    };
    stream.interrupt = vi.fn(async () => undefined);
    stream.close = vi.fn();
    const query = vi.fn(() => stream);

    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');
    const events = [];
    for await (const event of manager.startTurn(session, 'hello', opts)) {
      events.push(event);
    }

    const sequence = events.map((event) => event.type);
    const harnessTypes = events
      .filter((event) => event.type === 'harness:event')
      .map((event) => event.data.type);

    expect(harnessTypes).toContain('tool.permission');
    expect(sequence[sequence.length - 1]).toBe('process:exit');
    // turn.accepted / turn.started bridge immediately after session:init (D-APP-25).
    expect(harnessTypes.slice(0, 2)).toEqual(['turn.accepted', 'turn.started']);
    // The bridged permission event lands after session:init and before the terminal exit.
    const permIndex = events.findIndex(
      (event) => event.type === 'harness:event' && event.data.type === 'tool.permission'
    );
    expect(permIndex).toBeGreaterThan(sequence.indexOf('session:init'));
    expect(permIndex).toBeLessThan(sequence.lastIndexOf('process:exit'));
  });
});
