import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type {
  AgentEnginePort,
  AgentEngineRunInput
} from '@chirality/runtime-contracts/agent-engine-port';
import type {
  ISessionManager,
  ResolvedOpts,
  SessionRecord,
  UIEvent
} from '@chirality/runtime-contracts/types';
import { runEngineConformance } from '@chirality/runtime-contracts/engine-conformance';
import { PiAgentEngineAdapter } from '../../lib/harness/pi-agent-engine-adapter';
import { createBoundedReadToolDefinitions } from '../../lib/harness/chirality-tool-bridge';
import { bindChiralityToolsForPi } from '../../lib/harness/pi-tool-binder';
import {
  OmlxProviderError,
  requireOmlxModel,
  resolveOmlxProviderConfig
} from '../../lib/harness/omlx-provider-config';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import { AgentEngineRegistry } from '../../lib/harness/engine-registry';
import { TurnEngine } from '../../lib/harness/turn-engine';
import {
  completionChunk,
  startFakeOpenAiLoopback,
  type FakeCompletionResponse,
  type FakeModelResponse,
  type FakeOpenAiLoopback
} from './fake-openai-loopback';

let tempRoot = '';
let providers: FakeOpenAiLoopback[] = [];
let previousSessionRoot: string | undefined;
let sessionSequence = 0;

async function startProvider(input: {
  apiKey: string;
  models: FakeModelResponse;
  completions?: readonly FakeCompletionResponse[];
}): Promise<FakeOpenAiLoopback> {
  const provider = await startFakeOpenAiLoopback(input);
  providers.push(provider);
  return provider;
}

async function collect(events: AsyncIterable<UIEvent>): Promise<UIEvent[]> {
  const result: UIEvent[] = [];
  for await (const event of events) result.push(event);
  return result;
}

function createInput(projectRoot: string, model: string, sessionId?: string): AgentEngineRunInput {
  const resolvedSessionId = sessionId ?? `sess_pi_wire_${++sessionSequence}`;
  return {
    session: {
      sessionId: resolvedSessionId,
      projectRoot,
      persona: 'TASK',
      mode: 'readOnly',
      agentType: 2,
      parentSessionId: 'sess_claude_parent',
      approvalRef: 'D-APP-72',
      declaredContext: [projectRoot],
      declaredTools: ['read_file'],
      allowedWriteTargets: [],
      engineSelection: { adapterId: 'pi', providerId: 'omlx', model },
      createdAt: '2026-07-21T00:00:00.000Z',
      updatedAt: '2026-07-21T00:00:00.000Z'
    },
    message: 'Read known.txt and report the requested result.',
    opts: {
      model,
      tools: ['read_file'],
      maxTurns: 2,
      persona: 'TASK',
      mode: 'readOnly'
    },
    turnId: `turn_${resolvedSessionId}`
  };
}

function createAdapter(input: {
  baseUrl: () => string;
  apiKey: string;
  projectRoot: string;
  turnTimeoutMs?: number;
}): PiAgentEngineAdapter {
  return new PiAgentEngineAdapter({
    // Loopback provider: scripted streams either finish immediately or hang
    // until this timeout fires, so a short timeout keeps the hung-path tests
    // fast. Tests that interrupt a hung stream BEFORE the timeout may elapse
    // pass a longer value so the timeout cannot race the deliberate interrupt.
    turnTimeoutMs: input.turnTimeoutMs ?? 200,
    resolveProvider: async (runInput) => {
      const config = resolveOmlxProviderConfig({
        baseUrl: input.baseUrl(),
        apiKey: input.apiKey
      });
      await requireOmlxModel(runInput.opts.model, config);
      return {
        ...config,
        model: { id: runInput.opts.model, contextWindow: 32768, maxTokens: 4096 }
      };
    },
    buildSystemPrompt: async () => 'Use only read_file for the sealed task.',
    resolveCustomTools: async (runInput) =>
      bindChiralityToolsForPi(
        createBoundedReadToolDefinitions({
          context: {
            projectRoot: input.projectRoot,
            sessionId: runInput.session.sessionId,
            turnId: runInput.turnId,
            mode: 'readOnly',
            allowedReadScopes: [input.projectRoot],
            allowedWriteTargets: []
          },
          allowedToolNames: ['read_file']
        })
      )
  });
}

function finalText(model: string, text: string): FakeCompletionResponse {
  return {
    kind: 'sse',
    values: [
      completionChunk(model, { role: 'assistant', content: '' }),
      completionChunk(model, { content: text }),
      completionChunk(model, {}, 'stop')
    ]
  };
}

function toolCall(model: string, args = '{"file_path":"known.txt"}'): FakeCompletionResponse {
  return {
    kind: 'sse',
    values: [
      completionChunk(model, { role: 'assistant', content: '' }),
      completionChunk(model, {
        tool_calls: [
          {
            index: 0,
            id: 'call_wire_read',
            type: 'function',
            function: { name: 'read_file', arguments: args }
          }
        ]
      }),
      completionChunk(model, {}, 'tool_calls')
    ]
  };
}

function expectSingleFailure(events: readonly UIEvent[], errorType?: string): void {
  expect(events.filter((event) => event.type === 'process:exit')).toEqual([
    expect.objectContaining({
      type: 'process:exit',
      data: expect.objectContaining({ exitCode: 1, ...(errorType ? { errorType } : {}) })
    })
  ]);
  expect(events.at(-1)?.type).toBe('process:exit');
}

class ScriptedClaudeParentPort implements AgentEnginePort {
  readonly subject = 'claude-agent-sdk';
  readonly descriptor = {
    adapterId: 'claude-agent-sdk',
    providerId: 'anthropic',
    packageName: '@anthropic-ai/claude-agent-sdk',
    packageVersion: 'scripted-test',
    capabilities: {
      credentials: true,
      tools: true,
      attachments: true,
      interruption: true,
      durableResume: true,
      compaction: true
    }
  } as const;
  readonly interrupt = vi.fn(async () => undefined);
  private releaseTurn: () => void = () => undefined;
  private readonly released = new Promise<void>((resolve) => {
    this.releaseTurn = resolve;
  });

  async preflight(): Promise<void> {
    return undefined;
  }

  async *startTurn(input: AgentEngineRunInput): AsyncIterable<UIEvent> {
    yield {
      type: 'session:init',
      data: {
        engineSessionId: `claude_scripted_${input.session.sessionId}`,
        claudeSessionId: `claude_scripted_${input.session.sessionId}`,
        adapterId: 'claude-agent-sdk',
        providerId: 'anthropic',
        model: input.opts.model
      }
    };
    await this.released;
    yield { type: 'chat:complete', data: { text: 'PARENT_STILL_ISOLATED' } };
    yield { type: 'session:complete', data: {} };
    yield { type: 'process:exit', data: { exitCode: 0 } };
  }

  finish(): void {
    this.releaseTurn();
  }
}

function createMemorySessionManager(records: readonly SessionRecord[]): ISessionManager {
  const sessions = new Map(records.map((record) => [record.sessionId, { ...record }]));
  return {
    async create(input) {
      const created: SessionRecord = {
        sessionId: `created_${sessions.size}`,
        projectRoot: input.projectRoot,
        persona: input.persona ?? 'TASK',
        mode: input.mode ?? 'readOnly',
        createdAt: '2026-07-21T00:00:00.000Z',
        updatedAt: '2026-07-21T00:00:00.000Z'
      };
      sessions.set(created.sessionId, created);
      return created;
    },
    async resume(sessionId) {
      const record = sessions.get(sessionId);
      if (!record) throw new Error(`Unknown test session ${sessionId}`);
      return record;
    },
    async getById(sessionId) {
      const record = sessions.get(sessionId);
      if (!record) throw new Error(`Unknown test session ${sessionId}`);
      return record;
    },
    async save(sessionId, updates) {
      const current = sessions.get(sessionId);
      if (!current) throw new Error(`Unknown test session ${sessionId}`);
      const saved = { ...current, ...updates, updatedAt: '2026-07-21T00:00:01.000Z' };
      sessions.set(sessionId, saved);
      return saved;
    },
    async list(projectRoot) {
      return [...sessions.values()].filter((record) => record.projectRoot === projectRoot);
    },
    async delete(sessionId) {
      sessions.delete(sessionId);
    }
  };
}

beforeEach(async () => {
  tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-pi-wire-'));
  previousSessionRoot = process.env.CHIRALITY_SESSION_ROOT;
  process.env.CHIRALITY_SESSION_ROOT = path.join(tempRoot, 'sessions');
  providers = [];
  sessionSequence = 0;
});

afterEach(async () => {
  await Promise.all(providers.map((provider) => provider.close()));
  providers = [];
  if (previousSessionRoot === undefined) delete process.env.CHIRALITY_SESSION_ROOT;
  else process.env.CHIRALITY_SESSION_ROOT = previousSessionRoot;
  await rm(tempRoot, { recursive: true, force: true });
});

describe('Pi/oMLX wire integration', () => {
  it('discovers the exact model, executes one governed read tool, persists evidence, and finishes canonically', async () => {
    const projectRoot = path.join(tempRoot, 'project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'KNOWN_WIRE_FIXTURE\n', 'utf8');
    const apiKey = 'wire-proof-key';
    const model = 'wire-exact-model';
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [toolCall(model), finalText(model, 'WIRE_PI_CHILD_OK')]
    });
    // Success-path I/O must not race the short deadline used by hung-stream tests.
    const adapter = createAdapter({ baseUrl: () => provider.baseUrl, apiKey, projectRoot, turnTimeoutMs: 2_000 });
    const input = createInput(projectRoot, model, 'sess_pi_wire_success');

    await expect(adapter.preflight(input)).resolves.toBeUndefined();
    const report = await runEngineConformance(adapter, input, {
      requireEngineSessionId: true,
      requireHarnessTerminal: true,
      requireToolPermissionEvidence: true,
      forbiddenEvidenceValues: [apiKey],
      readPersistedEvents: async (sessionId) => (await replayHarnessEvents(sessionId)).events
    });

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([]);
    expect(report.events[0]).toMatchObject({
      type: 'session:init',
      data: { adapterId: 'pi', providerId: 'omlx', model }
    });
    expect(report.events).toContainEqual({
      type: 'tool:result',
      data: expect.objectContaining({ name: 'read_file', ok: true })
    });
    expect(report.events).toContainEqual({
      type: 'chat:complete',
      data: { text: 'WIRE_PI_CHILD_OK' }
    });
    expect(provider.posts).toHaveLength(2);
    expect(JSON.stringify(provider.posts[1])).toContain('KNOWN_WIRE_FIXTURE');
    const replay = await replayHarnessEvents(input.session.sessionId);
    const permissionIndex = replay.events.findIndex((event) => event.type === 'tool.permission');
    const resultIndex = replay.events.findIndex((event) => event.type === 'tool.completed');
    expect(permissionIndex).toBeGreaterThanOrEqual(0);
    expect(resultIndex).toBeGreaterThan(permissionIndex);
  });

  it('fails closed for bad authentication, empty/unknown models, malformed discovery, and redirects', async () => {
    const apiKey = 'discovery-key';
    const model = 'loaded-model';
    const cases: Array<{
      name: string;
      models: FakeModelResponse;
      suppliedKey?: string;
      requestedModel?: string;
      code: OmlxProviderError['code'];
    }> = [
      {
        name: 'authentication',
        models: { kind: 'json', body: { data: [{ id: model }] } },
        suppliedKey: 'wrong-key',
        code: 'OMLX_AUTHENTICATION'
      },
      {
        name: 'empty model list',
        models: { kind: 'json', body: { data: [] } },
        code: 'OMLX_MODELS_EMPTY'
      },
      {
        name: 'unknown exact model',
        models: { kind: 'json', body: { data: [{ id: model }] } },
        requestedModel: 'alias-is-not-translated',
        code: 'OMLX_MODEL_UNKNOWN'
      },
      {
        name: 'malformed JSON',
        models: { kind: 'raw', body: '{not-json' },
        code: 'OMLX_MODELS_MALFORMED'
      },
      {
        name: 'malformed schema',
        models: { kind: 'json', body: { models: [{ name: model }] } },
        code: 'OMLX_MODELS_MALFORMED'
      },
      {
        name: 'redirect',
        models: { kind: 'redirect', location: 'http://127.0.0.1:9/v1/models' },
        code: 'OMLX_PROTOCOL'
      }
    ];

    for (const testCase of cases) {
      const provider = await startProvider({ apiKey, models: testCase.models });
      const promise = requireOmlxModel(testCase.requestedModel ?? model, {
        baseUrl: provider.baseUrl,
        apiKey: testCase.suppliedKey ?? apiKey,
        timeoutMs: 500
      });
      await expect(promise, testCase.name).rejects.toMatchObject({
        code: testCase.code
      } satisfies Partial<OmlxProviderError>);
    }
  });

  it.each([
    {
      name: 'malformed SSE JSON',
      completion: { kind: 'raw', body: 'data: {not-json}\n\ndata: [DONE]\n\n' } as const,
      expected: 'PROVIDER_PROTOCOL_FAILURE'
    },
    {
      name: 'context exhaustion',
      completion: {
        kind: 'error',
        status: 400,
        body: { error: { message: 'maximum context length exceeded: too many tokens' } }
      } as const,
      expected: 'CONTEXT_EXHAUSTED'
    },
    {
      name: 'mid-stream disconnect',
      completion: {
        kind: 'disconnect',
        body: `data: ${JSON.stringify(completionChunk('failure-model', { role: 'assistant' }))}\n\n`
      } as const,
      expected: 'PROVIDER_PROTOCOL_FAILURE'
    },
    {
      name: 'completion redirect',
      completion: { kind: 'redirect', location: 'http://127.0.0.1:9/credential-sink' } as const,
      expected: 'PROVIDER_PROTOCOL_FAILURE'
    }
  ])('maps $name to one redacted canonical failure and releases the turn', async ({ completion, expected }) => {
    const projectRoot = path.join(tempRoot, 'failure-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'safe\n', 'utf8');
    const apiKey = 'failure-secret-key';
    const model = 'failure-model';
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [completion]
    });
    const adapter = createAdapter({ baseUrl: () => provider.baseUrl, apiKey, projectRoot });
    const input = createInput(projectRoot, model);

    const events = await collect(adapter.startTurn(input));

    expectSingleFailure(events, expected);
    expect(JSON.stringify(events)).not.toContain(apiKey);
    const replay = await replayHarnessEvents(input.session.sessionId);
    expect(replay.events.filter((event) => event.type === 'turn.failed')).toHaveLength(1);
    expect(JSON.stringify(replay.events)).not.toContain(apiKey);
    await expect(adapter.interrupt(input.session.sessionId)).rejects.toMatchObject({
      type: 'SESSION_NOT_FOUND'
    });
  });

  it('fails a malformed tool call without invoking the governed tool', async () => {
    const projectRoot = path.join(tempRoot, 'malformed-tool-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'MUST_NOT_BE_READ\n', 'utf8');
    const apiKey = 'malformed-tool-key';
    const model = 'malformed-tool-model';
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [toolCall(model, '{"file_path":')]
    });
    const adapter = createAdapter({ baseUrl: () => provider.baseUrl, apiKey, projectRoot });
    const input = createInput(projectRoot, model);

    const events = await collect(adapter.startTurn(input));

    expectSingleFailure(events, 'PROVIDER_PROTOCOL_FAILURE');
    expect(events.filter((event) => event.type === 'tool:result')).toEqual([
      expect.objectContaining({
        data: expect.objectContaining({ name: 'read_file', ok: false })
      })
    ]);
    expect(JSON.stringify(events)).not.toContain('MUST_NOT_BE_READ');
  });

  it('interrupts a hung stream deterministically and emits one interrupted terminal outcome', async () => {
    const projectRoot = path.join(tempRoot, 'hung-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'safe\n', 'utf8');
    const apiKey = 'hung-key';
    const model = 'hung-model';
    let markStreamStarted: () => void = () => undefined;
    const streamStarted = new Promise<void>((resolve) => {
      markStreamStarted = resolve;
    });
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [{ kind: 'hang', started: markStreamStarted }]
    });
    const adapter = createAdapter({
      baseUrl: () => provider.baseUrl,
      apiKey,
      projectRoot,
      turnTimeoutMs: 750
    });
    const input = createInput(projectRoot, model);
    const collection = collect(adapter.startTurn(input));

    await Promise.race([
      streamStarted,
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error('stream did not start')), 2_000))
    ]);
    await adapter.interrupt(input.session.sessionId);
    const events = await Promise.race([
      collection,
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error('interrupt timed out')), 2_000))
    ]);

    expect(events.filter((event) => event.type === 'process:exit')).toEqual([
      { type: 'process:exit', data: { exitCode: 130, interrupted: true } }
    ]);
    const replay = await replayHarnessEvents(input.session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(
      expect.arrayContaining(['interruption.requested', 'interruption.completed', 'turn.interrupted'])
    );
  });

  it('times out a hung provider stream, aborts it, and releases the adapter for a later turn', async () => {
    const projectRoot = path.join(tempRoot, 'timeout-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'safe\n', 'utf8');
    const apiKey = 'timeout-key';
    const model = 'timeout-model';
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [{ kind: 'hang' }]
    });
    const adapter = createAdapter({ baseUrl: () => provider.baseUrl, apiKey, projectRoot });
    const input = createInput(projectRoot, model);

    const events = await collect(adapter.startTurn(input));

    expectSingleFailure(events, 'PROVIDER_PROTOCOL_FAILURE');
    expect(events.at(-1)).toMatchObject({
      data: { status: 504, fatal: true }
    });
    await expect(adapter.interrupt(input.session.sessionId)).rejects.toMatchObject({
      type: 'SESSION_NOT_FOUND'
    });
  });

  it('recovers on a later turn after a disconnected provider and server restart', async () => {
    const projectRoot = path.join(tempRoot, 'recovery-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'RECOVERY_FIXTURE\n', 'utf8');
    const apiKey = 'recovery-key';
    const model = 'recovery-model';
    let provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [{ kind: 'disconnect' }]
    });
    const adapter = createAdapter({ baseUrl: () => provider.baseUrl, apiKey, projectRoot });
    const failed = await collect(adapter.startTurn(createInput(projectRoot, model, 'sess_recovery_failed')));
    expectSingleFailure(failed, 'PROVIDER_PROTOCOL_FAILURE');

    await provider.close();
    providers = providers.filter((candidate) => candidate !== provider);
    provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: model }] } },
      completions: [finalText(model, 'RECOVERED_AFTER_RESTART')]
    });
    const recoveredInput = createInput(projectRoot, model, 'sess_recovery_success');

    await expect(adapter.preflight(recoveredInput)).resolves.toBeUndefined();
    const recovered = await collect(adapter.startTurn(recoveredInput));
    expect(recovered).toContainEqual({
      type: 'chat:complete',
      data: { text: 'RECOVERED_AFTER_RESTART' }
    });
    expect(recovered.at(-1)).toEqual({ type: 'process:exit', data: { exitCode: 0 } });
  });

  it('keeps a scripted Claude parent and real Pi child isolated during concurrent targeted interruption', async () => {
    const projectRoot = path.join(tempRoot, 'concurrent-project');
    await mkdir(projectRoot, { recursive: true });
    await writeFile(path.join(projectRoot, 'known.txt'), 'CONCURRENT_FIXTURE\n', 'utf8');
    const apiKey = 'concurrent-key';
    const childModel = 'concurrent-pi-model';
    let markChildStarted: () => void = () => undefined;
    const childStarted = new Promise<void>((resolve) => {
      markChildStarted = resolve;
    });
    const provider = await startProvider({
      apiKey,
      models: { kind: 'json', body: { data: [{ id: childModel }] } },
      completions: [{ kind: 'hang', started: markChildStarted }]
    });
    const piAdapter = createAdapter({
      baseUrl: () => provider.baseUrl,
      apiKey,
      projectRoot,
      turnTimeoutMs: 750
    });
    const parentAdapter = new ScriptedClaudeParentPort();
    const registry = new AgentEngineRegistry();
    registry.register('claude-agent-sdk', () => parentAdapter);
    registry.register('pi', () => piAdapter);
    const parentSession: SessionRecord = {
      sessionId: 'sess_concurrent_parent',
      projectRoot,
      persona: 'WORKING_ITEMS',
      mode: 'readOnly',
      agentType: 1,
      engineSelection: {
        adapterId: 'claude-agent-sdk',
        providerId: 'anthropic',
        model: 'claude-scripted-parent-model'
      },
      createdAt: '2026-07-21T00:00:00.000Z',
      updatedAt: '2026-07-21T00:00:00.000Z'
    };
    const childSession = createInput(
      projectRoot,
      childModel,
      'sess_concurrent_child'
    ).session;
    const sessionManager = createMemorySessionManager([parentSession, childSession]);
    const resolvedOptions = (record: SessionRecord): ResolvedOpts => ({
      model: record.engineSelection?.model ?? 'missing-model',
      tools: record.engineSelection?.adapterId === 'pi' ? ['read_file'] : [],
      maxTurns: 2,
      persona: record.persona,
      mode: record.mode
    });
    const turnEngine = new TurnEngine({
      sessionManager,
      personaManager: {
        async buildSystemPrompt() {
          return 'isolated test prompt';
        },
        getBootFingerprint() {
          return 'test-fingerprint';
        }
      },
      attachmentResolver: {
        async resolveAttachmentsToContentBlocks() {
          return { contentBlocks: [], errors: [] };
        }
      },
      resolveEngine: (record, resolved) =>
        registry.resolve(record.engineSelection ?? {
          adapterId: 'claude-agent-sdk',
          providerId: 'anthropic',
          model: resolved.model
        }),
      resolveRuntimeOptions: async (record) => resolvedOptions(record),
      evaluateSubagentGovernance: (async () => ({
        allowed: false,
        delegatedSubagents: [],
        delegatedAgentInstructions: {},
        reason: 'test'
      })) as never
    });

    expect(registry.resolve(parentSession.engineSelection!).port).toBe(parentAdapter);
    expect(registry.resolve(childSession.engineSelection!).port).toBe(piAdapter);
    expect(registry.resolve(childSession.engineSelection!).port).toBe(piAdapter);

    const parentTurn = await turnEngine.runTurn({
      sessionId: parentSession.sessionId,
      message: 'Supervise the child.'
    });
    const childTurn = await turnEngine.runTurn({
      sessionId: childSession.sessionId,
      message: 'Read only the fixture.'
    });
    const parentEventsPromise = collect(parentTurn.events);
    const childEventsPromise = collect(childTurn.events);
    await Promise.race([
      childStarted,
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error('child did not start')), 2_000))
    ]);

    await turnEngine.interrupt(childSession.sessionId);
    const childEvents = await childEventsPromise;
    const parentFinishedEarly = await Promise.race([
      parentEventsPromise.then(() => true),
      new Promise<false>((resolve) => setTimeout(() => resolve(false), 50))
    ]);

    expect(parentFinishedEarly).toBe(false);
    expect(parentAdapter.interrupt).not.toHaveBeenCalled();
    expect(childEvents[0]).toMatchObject({
      type: 'session:init',
      data: { adapterId: 'pi', providerId: 'omlx', model: childModel }
    });
    expect(childEvents.at(-1)).toEqual({
      type: 'process:exit',
      data: { exitCode: 130, interrupted: true }
    });

    parentAdapter.finish();
    const parentEvents = await parentEventsPromise;
    expect(parentEvents[0]).toMatchObject({
      type: 'session:init',
      data: {
        adapterId: 'claude-agent-sdk',
        providerId: 'anthropic',
        model: 'claude-scripted-parent-model'
      }
    });
    expect(parentEvents).toContainEqual({
      type: 'chat:complete',
      data: { text: 'PARENT_STILL_ISOLATED' }
    });
    expect(parentEvents.at(-1)).toEqual({ type: 'process:exit', data: { exitCode: 0 } });
  });
});
