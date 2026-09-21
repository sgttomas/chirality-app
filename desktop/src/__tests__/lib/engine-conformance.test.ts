import type { SDKMessage } from '@anthropic-ai/claude-agent-sdk';
import { mkdtemp, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type {
  AgentEnginePort,
  AgentEngineRunInput,
  EngineDescriptor
} from '@chirality/runtime-contracts/agent-engine-port';
import type { HarnessEvent, HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import { ClaudeAgentSdkManager } from '../../lib/harness/claude-agent-sdk-manager';
import {
  runEngineConformance,
  runEngineInterruptConformance
} from '@chirality/runtime-contracts/engine-conformance';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import type { ResolvedOpts, SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';

const session: SessionRecord = {
  sessionId: 'sess_engine_conformance',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'direct',
  createdAt: '2026-06-13T00:00:00.000Z',
  updatedAt: '2026-06-13T00:00:00.000Z'
};

const opts: ResolvedOpts = {
  model: 'claude-test',
  tools: [],
  maxTurns: 2,
  persona: 'WORKING_ITEMS',
  mode: 'direct'
};

let tmpDir = '';

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

function createRunInput(overrides: Partial<AgentEngineRunInput> = {}): AgentEngineRunInput {
  return {
    session,
    message: 'hello',
    opts,
    turnId: 'turn_conformance',
    ...overrides
  };
}

function sdkInit(sessionId = 'sdk_1'): SDKMessage {
  return {
    type: 'system',
    subtype: 'init',
    session_id: sessionId,
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
  };
}

function sdkDelta(sessionId = 'sdk_1', text = 'Hi'): SDKMessage {
  return {
    type: 'stream_event',
    event: {
      type: 'content_block_delta',
      index: 0,
      delta: { type: 'text_delta', text }
    },
    parent_tool_use_id: null,
    uuid: '00000000-0000-0000-0000-000000000002',
    session_id: sessionId
  };
}

function sdkSuccess(sessionId = 'sdk_1', text = 'Hi'): SDKMessage {
  return {
    type: 'result',
    subtype: 'success',
    duration_ms: 10,
    duration_api_ms: 9,
    is_error: false,
    num_turns: 1,
    result: text,
    stop_reason: 'end_turn',
    total_cost_usd: 0,
    usage: {} as never,
    modelUsage: {},
    permission_denials: [],
    uuid: '00000000-0000-0000-0000-000000000003',
    session_id: sessionId
  };
}

function sdkFailure(sessionId = 'sdk_1'): SDKMessage {
  return {
    type: 'result',
    subtype: 'error_during_execution',
    duration_ms: 10,
    duration_api_ms: 9,
    is_error: true,
    num_turns: 1,
    total_cost_usd: 0,
    usage: {} as never,
    modelUsage: {},
    permission_denials: [],
    errors: ['provider failed'],
    terminal_reason: 'provider_error',
    uuid: '00000000-0000-0000-0000-000000000004',
    session_id: sessionId
  } as never;
}

function sdkAssistantToolUse(
  sessionId = 'sdk_1',
  toolUseId = 'toolu_read',
  toolName = 'Read',
  input: Record<string, unknown> = { file_path: 'README.md' }
): SDKMessage {
  return {
    type: 'assistant',
    message: {
      role: 'assistant',
      content: [{ type: 'tool_use', id: toolUseId, name: toolName, input }]
    },
    parent_tool_use_id: null,
    uuid: '00000000-0000-0000-0000-000000000005',
    session_id: sessionId
  } as never;
}

function sdkUserToolUseResult(
  sessionId = 'sdk_1',
  toolUseId = 'toolu_read',
  result: Record<string, unknown> = {
    type: 'tool_result',
    tool_use_id: 'toolu_read',
    content: 'file body'
  }
): SDKMessage {
  return {
    type: 'user',
    message: {
      role: 'user',
      content: []
    },
    parent_tool_use_id: toolUseId,
    tool_use_result: result,
    uuid: '00000000-0000-0000-0000-000000000006',
    session_id: sessionId
  } as never;
}

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

function createInterruptibleQuery(eventsBeforeInterrupt: SDKMessage[]) {
  let resolveInterrupt: () => void = () => undefined;
  const interrupted = new Promise<void>((resolve) => {
    resolveInterrupt = resolve;
  });
  const stream = (async function* (): AsyncGenerator<SDKMessage, void> {
    for (const event of eventsBeforeInterrupt) {
      yield event;
    }
    await interrupted;
    yield sdkDelta('sdk_interrupt', 'after interrupt');
  })() as AsyncGenerator<SDKMessage, void> & {
    interrupt: () => Promise<void>;
    close: () => void;
  };
  stream.interrupt = vi.fn(async () => {
    resolveInterrupt();
  });
  stream.close = vi.fn();
  return vi.fn(() => stream);
}

class ScriptedEnginePort implements AgentEnginePort {
  readonly subject = 'stub' as const;
  readonly descriptor: EngineDescriptor;

  constructor(
    private readonly script: Array<UIEvent | { type: string; data: unknown }>,
    descriptor: EngineDescriptor = {
    adapterId: 'stub',
    providerId: 'stub',
    capabilities: {
      credentials: false,
      tools: false,
      attachments: false,
      interruption: true,
      durableResume: false,
      compaction: false
    }
    }
  ) {
    this.descriptor = descriptor;
  }

  async preflight(_input: AgentEngineRunInput): Promise<void> {
    return undefined;
  }

  async *startTurn(_input: AgentEngineRunInput): AsyncIterable<UIEvent> {
    for (const event of this.script) {
      yield event as UIEvent;
    }
  }

  async interrupt(_sessionId: string): Promise<void> {
    return undefined;
  }
}

async function useTempSessionRoot(): Promise<void> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-engine-conformance-'));
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
}

function harnessEvent(
  eventId: string,
  type: HarnessEventType,
  data: Record<string, unknown> = {}
): HarnessEvent {
  return {
    schemaVersion: 1,
    eventId,
    sessionId: session.sessionId,
    turnId: 'turn_conformance',
    timestamp: '2026-06-13T00:00:00.000Z',
    type,
    data
  };
}

function harnessUi(event: HarnessEvent): UIEvent {
  return { type: 'harness:event', data: event };
}

describe('engine conformance fixtures', () => {
  it('passes a Claude Agent SDK success stream against the provider-neutral engine contract', async () => {
    await useTempSessionRoot();
    const query = createQuery([sdkInit(), sdkDelta(), sdkSuccess()]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');

    const report = await runEngineConformance(manager, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([]);
    expect(report.eventTypes).toEqual([
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
    // harness:event is a provider-neutral type name even though its payload carries
    // provider metadata (providerMetadataAllowed); the public type stream stays neutral.
    expect(report.eventTypes.join(' ')).not.toMatch(/sdk|claude|anthropic/i);
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

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'model.delta',
      'message.delta',
      'model.completed',
      'turn.completed'
    ]);
  });

  it('replays read-tool lifecycle evidence from a scripted SDK tool result turn', async () => {
    await useTempSessionRoot();
    const query = createQuery([
      sdkInit(),
      sdkAssistantToolUse(),
      sdkUserToolUseResult(),
      sdkSuccess('sdk_1', 'done')
    ]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');

    const report = await runEngineConformance(manager, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);
    // turn.accepted / turn.started bridge after session:init (D-APP-25), then each
    // persisted harness event (except per-token deltas and adapter.initialized)
    // bridges to a harness:event on the live stream: tool.queued, tool.started,
    // tool.completed, message.completed, model.completed, turn.completed.
    expect(report.eventTypes).toEqual([
      'session:init',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'tool.queued',
      'tool.started',
      'tool.completed',
      'message.completed',
      'model.completed',
      'turn.completed'
    ]);
    expect(replay.events[5].data).toMatchObject({
      toolName: 'Read',
      descriptorName: 'read_file',
      resultMetadata: {
        rawOutputPersisted: false,
        budgetClass: 'within-inline-budget'
      }
    });
  });

  it('replays failed read-tool evidence from a scripted SDK error tool result', async () => {
    await useTempSessionRoot();
    const query = createQuery([
      sdkInit(),
      sdkAssistantToolUse('sdk_1', 'toolu_grep', 'Grep', { pattern: 'needle' }),
      sdkUserToolUseResult('sdk_1', 'toolu_grep', {
        type: 'tool_result',
        tool_use_id: 'toolu_grep',
        is_error: true,
        content: 'grep failed'
      }),
      sdkSuccess('sdk_1', 'done')
    ]);
    const manager = new ClaudeAgentSdkManager(query as never, async () => 'persona prompt');

    const report = await runEngineConformance(manager, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'tool.queued',
      'tool.started',
      'tool.failed',
      'message.completed',
      'model.completed',
      'turn.completed'
    ]);
    expect(replay.events[5].data).toMatchObject({
      toolName: 'Grep',
      descriptorName: 'search_files',
      failureSource: 'tool_use_result',
      resultMetadata: {
        rawOutputPersisted: false
      }
    });
    expect(JSON.stringify(replay.events[5].data)).not.toContain('grep failed');
  });

  it('treats scripted provider failure as terminal public evidence instead of a provider-shaped UI event', async () => {
    await useTempSessionRoot();
    const manager = new ClaudeAgentSdkManager(
      createQuery([sdkInit(), sdkFailure()]) as never,
      async () => 'persona prompt'
    );

    const report = await runEngineConformance(manager, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);
    // session:init, then the buffered turn.accepted / turn.started, then the
    // mapper's turn.failed for the error result, then terminal process:exit.
    expect(report.eventTypes).toEqual([
      'session:init',
      'harness:event',
      'harness:event',
      'harness:event',
      'process:exit'
    ]);
    expect(report.events.at(-1)).toMatchObject({
      type: 'process:exit',
      data: {
        exitCode: 1,
        errorType: 'SDK_FAILURE',
        fatal: true
      }
    });

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'turn.failed'
    ]);
  });

  it('requires interrupted adapter turns to emit interruption terminal evidence', async () => {
    await useTempSessionRoot();
    const manager = new ClaudeAgentSdkManager(
      createInterruptibleQuery([sdkInit('sdk_interrupt')]) as never,
      async () => 'persona prompt'
    );

    const report = await runEngineInterruptConformance(manager, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);
    // session:init, the buffered turn.accepted / turn.started, then the bridged
    // interruption.completed / turn.interrupted terminal pair, then terminal exit.
    expect(report.eventTypes).toEqual([
      'session:init',
      'harness:event',
      'harness:event',
      'harness:event',
      'harness:event',
      'process:exit'
    ]);
    expect(report.events.at(-1)).toMatchObject({
      type: 'process:exit',
      data: {
        exitCode: 130,
        interrupted: true
      }
    });

    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'adapter.initialized',
      'interruption.requested',
      'interruption.completed',
      'turn.interrupted'
    ]);
  });

  it('flags non-public event names from scripted adapters', async () => {
    const port = new ScriptedEnginePort([
      {
        type: 'session:init',
        data: {
          engineSessionId: 'engine_1',
          adapterId: 'stub',
          providerId: 'stub',
          claudeSessionId: 'claude_1',
          model: 'claude-test'
        }
      },
      { type: 'sdk:delta', data: { text: 'provider-shaped event name' } },
      { type: 'process:exit', data: { exitCode: 0 } }
    ]);

    const report = await runEngineConformance(port, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(false);
    expect(report.issues).toEqual([
      expect.objectContaining({
        code: 'UNKNOWN_UI_EVENT',
        eventType: 'sdk:delta'
      })
    ]);
  });

  it('flags scripted adapters that finish without process:exit evidence', async () => {
    const port = new ScriptedEnginePort([
      {
        type: 'session:init',
        data: {
          engineSessionId: 'engine_1',
          adapterId: 'stub',
          providerId: 'stub',
          claudeSessionId: 'claude_1',
          model: 'claude-test'
        }
      },
      { type: 'chat:complete', data: { text: 'done' } },
      { type: 'session:complete', data: {} }
    ]);

    const report = await runEngineConformance(port, createRunInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(false);
    expect(report.issues).toEqual([
      expect.objectContaining({
        code: 'MISSING_PROCESS_EXIT'
      })
    ]);
  });

  it('strictly validates declared capabilities, tool pairing, compaction, persistence, and redaction', async () => {
    const persisted = [
      harnessEvent('evt_permission', 'tool.permission', {
        toolUseId: 'tool_read_1',
        decision: 'allow'
      }),
      harnessEvent('evt_started', 'tool.started', { toolCallId: 'tool_read_1' }),
      harnessEvent('evt_completed', 'tool.completed', { toolCallId: 'tool_read_1' }),
      harnessEvent('evt_compaction_start', 'context.compaction.started'),
      harnessEvent('evt_compaction_end', 'context.compacted'),
      harnessEvent('evt_terminal', 'turn.completed')
    ];
    const port = new ScriptedEnginePort(
      [
        {
          type: 'session:init',
          data: {
            engineSessionId: 'engine_strict',
            adapterId: 'stub',
            providerId: 'stub',
            model: 'claude-test'
          }
        },
        ...persisted.map(harnessUi),
        { type: 'session:complete', data: {} },
        { type: 'process:exit', data: { exitCode: 0 } }
      ],
      {
        adapterId: 'stub',
        providerId: 'stub',
        capabilities: {
          credentials: false,
          tools: true,
          attachments: false,
          interruption: true,
          durableResume: false,
          compaction: true
        }
      }
    );

    const report = await runEngineConformance(
      port,
      createRunInput({ opts: { ...opts, tools: ['read_file'] } }),
      {
        requireEngineSessionId: true,
        requireHarnessTerminal: true,
        requireToolPermissionEvidence: true,
        forbiddenEvidenceValues: ['super-secret'],
        readPersistedEvents: async () => persisted
      }
    );

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([]);
  });

  it('reports ordering, attribution, capability, lifecycle, persistence, and redaction violations', async () => {
    const secret = 'unredacted-api-key';
    const completed = harnessEvent('evt_completed_bad', 'tool.completed', {
      toolCallId: 'tool_bad'
    });
    const latePermission = harnessEvent('evt_permission_late', 'tool.permission', {
      toolUseId: 'tool_bad'
    });
    const compaction = harnessEvent('evt_compaction_bad', 'context.compacted');
    const successTerminal = harnessEvent('evt_terminal_success', 'turn.completed');
    const failureTerminal = harnessEvent('evt_terminal_failure', 'turn.failed');
    const notPersisted = harnessEvent('evt_not_persisted', 'turn.started');
    const port = new ScriptedEnginePort([
      { type: 'chat:delta', data: { text: secret } },
      {
        type: 'session:init',
        data: {
          engineSessionId: 'engine_bad',
          adapterId: 'different-adapter',
          providerId: 'different-provider',
          model: 'claude-test'
        }
      },
      harnessUi(notPersisted),
      harnessUi(completed),
      harnessUi(latePermission),
      harnessUi(compaction),
      harnessUi(successTerminal),
      harnessUi(failureTerminal),
      { type: 'process:exit', data: { exitCode: 1 } }
    ]);

    const report = await runEngineConformance(
      port,
      createRunInput({
        opts: { ...opts, tools: ['read_file'] },
        contentBlocks: [{ type: 'file', path: '/tmp/project/input.txt', mimeType: 'text/plain' }]
      }),
      {
        requireHarnessTerminal: true,
        requireToolPermissionEvidence: true,
        forbiddenEvidenceValues: [secret],
        readPersistedEvents: async () => [
          completed,
          latePermission,
          compaction,
          successTerminal,
          failureTerminal
        ]
      }
    );

    expect(report.passed).toBe(false);
    expect(report.issues.map((issue) => issue.code)).toEqual(
      expect.arrayContaining([
        'TOOLS_NOT_DECLARED',
        'ATTACHMENTS_NOT_DECLARED',
        'SESSION_INIT_NOT_FIRST',
        'SESSION_INIT_ADAPTER_MISMATCH',
        'SESSION_INIT_PROVIDER_MISMATCH',
        'MULTIPLE_HARNESS_TERMINAL',
        'HARNESS_TERMINAL_MISMATCH',
        'TOOL_RESULT_WITHOUT_START',
        'TOOL_PERMISSION_AFTER_RESULT',
        'COMPACTION_NOT_DECLARED',
        'COMPACTION_RESULT_WITHOUT_START',
        'MISSING_PERSISTED_EVENT',
        'UNREDACTED_EVIDENCE'
      ])
    );
  });

  it('rejects interrupted conformance when interruption is not a declared capability', async () => {
    const port = new ScriptedEnginePort(
      [
        {
          type: 'session:init',
          data: {
            engineSessionId: 'engine_no_interrupt',
            adapterId: 'stub',
            providerId: 'stub',
            model: 'claude-test'
          }
        },
        { type: 'process:exit', data: { exitCode: 0 } }
      ],
      {
        adapterId: 'stub',
        providerId: 'stub',
        capabilities: {
          credentials: false,
          tools: false,
          attachments: false,
          interruption: false,
          durableResume: false,
          compaction: false
        }
      }
    );

    const report = await runEngineConformance(port, createRunInput(), {
      requireInterruptedProcessExit: true
    });

    expect(report.issues.map((issue) => issue.code)).toEqual(
      expect.arrayContaining(['INTERRUPTION_NOT_DECLARED', 'MISSING_INTERRUPTED_PROCESS_EXIT'])
    );
  });
});
