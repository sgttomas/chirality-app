import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { AnthropicAgentSdkManager } from '../../lib/harness/anthropic-agent-sdk-manager';
import { replayHarnessEvents } from '../../lib/harness/session-events';
import { UIEvent } from '@chirality/runtime-contracts/types';

async function* createStream(events: unknown[]): AsyncIterable<unknown> {
  for (const event of events) {
    yield event;
  }
}

async function collectEvents(iterable: AsyncIterable<UIEvent>): Promise<UIEvent[]> {
  const events: UIEvent[] = [];
  for await (const event of iterable) {
    events.push(event);
  }
  return events;
}

function toLowercasePercentEncoding(value: string): string {
  return value.replace(/%[0-9A-F]{2}/g, (match) => match.toLowerCase());
}

function toDoubleUrlEncoding(value: string): string {
  return encodeURIComponent(encodeURIComponent(value));
}

function toDoubleQueryStyleEncoding(value: string): string {
  return encodeURIComponent(encodeURIComponent(value).replace(/%20/g, '+'));
}

const session = {
  sessionId: 'sess_provider',
  projectRoot: '/tmp/project',
  persona: 'WORKING_ITEMS',
  mode: 'chat',
  createdAt: '2026-02-23T00:00:00.000Z',
  updatedAt: '2026-02-23T00:00:00.000Z'
};
const v3Session = { ...session, instructionBasisId: 'basis-v3' };

const opts = {
  model: 'claude-sonnet-test',
  tools: ['read'],
  maxTurns: 4,
  persona: 'WORKING_ITEMS',
  mode: 'chat'
};

const executionRoots = {
  workingRoot: { path: v3Session.projectRoot, origin: 'registered-project-root' as const, identitySha256: '3'.repeat(64) },
  toolRoot: { path: '/tmp/trusted-instruction-root', origin: 'trusted-runtime-instruction-root' as const, identitySha256: '4'.repeat(64) }
};

let tmpDir = '';
// D-APP-25 parity adds lifecycle persistence (appendHarnessEvent) to the
// Anthropic manager. Isolate the session-events root to a per-test tmpdir so
// turns never write events.jsonl into the working tree.
let sessionRootDir = '';
const globalState = globalThis as unknown as Record<string, string | undefined>;

async function writeFixtureFile(name: string, content: string | Buffer): Promise<string> {
  if (!tmpDir) {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'anthropic-sdk-manager-test-'));
  }
  const filePath = path.join(tmpDir, name);
  await writeFile(filePath, content);
  return filePath;
}

async function getFixturePath(name: string): Promise<string> {
  if (!tmpDir) {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'anthropic-sdk-manager-test-'));
  }
  return path.join(tmpDir, name);
}

beforeEach(async () => {
  sessionRootDir = await mkdtemp(path.join(os.tmpdir(), 'anthropic-sdk-manager-events-'));
  process.env.CHIRALITY_SESSION_ROOT = path.join(sessionRootDir, 'sessions');
});

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_URL;
  delete process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS;
  delete process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS;
  delete process.env.CHIRALITY_ANTHROPIC_VERSION;
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete globalState.__CHIRALITY_UI_API_KEY__;
});

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
  if (sessionRootDir) {
    await rm(sessionRootDir, { recursive: true, force: true });
    sessionRootDir = '';
  }
});

describe('AnthropicAgentSdkManager', () => {
  it('starts a successor with a fresh identity and prefers the committed engine identity on the next turn', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const manager = new AnthropicAgentSdkManager(vi.fn(() => ({ messages: { create: createMock } })) as never);
    const prepared = await manager.prepareContextSuccessor({
      sessionId: v3Session.sessionId, predecessorEngineSessionId: 'claude-old', fromBasisId: 'basis-old',
      toBasisPreview: { id: 'basis-new', sha256: 'a'.repeat(64) },
      continuationContext: {
        transcript: '[{"role":"user","text":"prior human"},{"role":"assistant","text":"prior assistant"}]',
        sha256: 'b'.repeat(64), priorBasisRefs: [{ basisId: 'basis-old', sha256: 'c'.repeat(64) }]
      }
    });
    const successorEvents = await collectEvents(manager.startRuntimeTurn({
      session: { ...v3Session, engineSessionId: 'claude-old', claudeSessionId: 'claude-old' },
      message: 'new request', opts, turnId: 'successor-turn', contextSuccessor: prepared,
      instructionContext: {
        schemaVersion: 'chirality.selected-context/v3', roleId: 'WORKING_ITEMS', methods: [], documents: [], dispositions: [],
        supplied: [{ kind: 'role', id: 'WORKING_ITEMS', content: 'new current body', sha256: 'd'.repeat(64) }],
        executionRoots,
        basisPreview: { id: 'basis-new', sha256: 'e'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false }, compatibilityInputs: [], compatibilityMappings: []
      }, runtimeTools: []
    }));
    expect(successorEvents[0]).toMatchObject({ type: 'session:init', data: { adapterId: 'anthropic-direct' } });
    const successorId = (successorEvents[0] as { data: { engineSessionId: string } }).data.engineSessionId;
    expect(successorId).not.toBe('claude-old');
    expect(JSON.stringify(createMock.mock.calls[0]?.[0].messages)).toContain('prior human');
    expect(JSON.stringify(createMock.mock.calls[0]?.[0].messages)).toContain('prior assistant');
    expect(JSON.stringify(createMock.mock.calls[0]?.[0].messages)).not.toContain('new current body');

    const nextEvents = await collectEvents(manager.startRuntimeTurn({
      session: { ...v3Session, engineSessionId: successorId, claudeSessionId: 'claude-old' },
      message: 'third turn', opts, turnId: 'third-turn', instructionContext: {
        schemaVersion: 'chirality.selected-context/v3', roleId: 'WORKING_ITEMS', methods: [], documents: [], dispositions: [],
        supplied: [{ kind: 'role', id: 'WORKING_ITEMS', content: 'new current body', sha256: 'd'.repeat(64) }],
        executionRoots,
        basisPreview: { id: 'basis-new', sha256: 'e'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false }, compatibilityInputs: [], compatibilityMappings: []
      }, runtimeTools: []
    }));
    expect(nextEvents[0]).toMatchObject({ type: 'session:init', data: { engineSessionId: successorId } });
  });

  it('boots a v3 session without consuming provider prompt context', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const manager = new AnthropicAgentSdkManager(vi.fn() as never);
    const events = await collectEvents(manager.startRuntimeTurn({
      session: v3Session,
      message: 'bootstrap', opts, turnId: 'boot-v3'
    }));
    expect(events.map((event) => event.type)).toEqual(['session:init', 'process:exit']);
  });

  it('sends exact Runtime context as system text and keeps attachments in user content', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const manager = new AnthropicAgentSdkManager(vi.fn(() => ({ messages: { create: createMock } })) as never);
    await collectEvents(manager.startRuntimeTurn({
      session: v3Session,
      message: 'normal directions', opts, turnId: 'turn-v3',
      contentBlocks: [{ type: 'text', text: 'attachment text' }],
      instructionContext: {
        schemaVersion: 'chirality.selected-context/v3', roleId: 'HELP_HUMAN', methods: [], documents: [], dispositions: [],
        supplied: [{ kind: 'role', id: 'HELP_HUMAN', content: 'frozen helper body', sha256: 'a'.repeat(64) }],
        executionRoots,
        basisPreview: { id: 'basis-v3', sha256: 'b'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false }, compatibilityInputs: [], compatibilityMappings: []
      },
      runtimeTools: []
    }));
    const request = createMock.mock.calls[0]?.[0];
    expect(request.system).toContain('frozen helper body');
    expect(request.system).not.toContain('attachment text');
    expect(JSON.stringify(request.messages)).toContain('attachment text');
  });

  it('fails closed when anthropic-direct receives Runtime tools it cannot expose', () => {
    const manager = new AnthropicAgentSdkManager(vi.fn() as never);
    expect(() => manager.startRuntimeTurn({
      session: v3Session,
      message: 'work', opts, turnId: 'turn-tools',
      runtimeTools: [{ name: 'chirality_list_methods', description: 'list', inputSchema: { type: 'object' }, permission: { effect: 'allow', operation: 'read' }, execute: async () => ({}) }]
    })).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE', status: 422 }));
  });

  it('returns successful bootstrap exit without SDK calls when API key is present', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn();
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    const events = await collectEvents(manager.startTurn(session, 'bootstrap', opts));

    expect(events.map((event) => event.type)).toEqual(['session:init', 'process:exit']);
    expect(events[1]).toMatchObject({
      type: 'process:exit',
      data: {
        exitCode: 0
      }
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed SDK_FAILURE when API key is missing', async () => {
    const createMock = vi.fn();
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 503
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('maps Anthropic stream deltas into harness SSE events using SDK stream', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        { type: 'content_block_delta', delta: { text: 'Hello' } },
        { type: 'content_block_delta', delta: { text: ' world' } },
        { type: 'message_stop' }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));

    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events = await collectEvents(
      manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])
    );

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event',
      'chat:delta',
      'chat:delta',
      'harness:event',
      'chat:complete',
      'session:complete',
      'process:exit'
    ]);
    // The bridged lifecycle timeline: turn.accepted -> turn.started before the
    // deltas, turn.completed after them.
    expect(
      events
        .filter((event) => event.type === 'harness:event')
        .map((event) => (event as { data: { type: string } }).data.type)
    ).toEqual(['turn.accepted', 'turn.started', 'turn.completed']);
    expect(events[6]).toMatchObject({
      type: 'chat:complete',
      data: {
        text: 'Hello world'
      }
    });
    expect(clientFactory).toHaveBeenCalledWith({
      apiKey: 'test-key',
      baseURL: 'https://api.anthropic.com',
      anthropicVersion: '2023-06-01'
    });
    expect(createMock).toHaveBeenCalledWith(
      expect.objectContaining({
        model: 'claude-sonnet-test',
        stream: true,
        max_tokens: 1024
      }),
      expect.objectContaining({
        signal: expect.any(AbortSignal)
      })
    );
  });

  it('persists the manager-lifecycle timeline to events.jsonl for replay parity', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockResolvedValue(
      createStream([{ type: 'content_block_delta', delta: { text: 'Hi' } }, { type: 'message_stop' }])
    );
    const clientFactory = vi.fn(() => ({ messages: { create: createMock } }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    // Parity with the Claude SDK manager: the lifecycle vocabulary is persisted
    // (live == replay), tagged with the anthropic provider.
    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'turn.completed'
    ]);
    expect(replay.events[0].data).toMatchObject({
      provider: 'anthropic',
      model: 'claude-sonnet-test'
    });
  });

  it('bridges and persists interruption lifecycle when interrupted mid-stream', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const manager = new AnthropicAgentSdkManager(
      (() => ({
        messages: {
          create: vi.fn(async () =>
            (async function* (): AsyncGenerator<unknown> {
              yield { type: 'content_block_delta', delta: { text: 'partial' } };
              await manager.interrupt(session.sessionId);
              yield { type: 'content_block_delta', delta: { text: ' more' } };
            })()
          )
        }
      })) as never
    );

    const events = await collectEvents(
      manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])
    );

    const sequence = events.map((event) => event.type);
    expect(sequence[sequence.length - 1]).toBe('process:exit');
    expect(events.at(-1)).toMatchObject({
      type: 'process:exit',
      data: { exitCode: 130, interrupted: true }
    });
    const bridgedTypes = events
      .filter((event) => event.type === 'harness:event')
      .map((event) => (event as { data: { type: string } }).data.type);
    expect(bridgedTypes).toEqual([
      'turn.accepted',
      'turn.started',
      'interruption.completed',
      'turn.interrupted'
    ]);

    // interruption.requested is persisted (operator action) but not bridged live.
    const replay = await replayHarnessEvents(session.sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'turn.accepted',
      'turn.started',
      'interruption.requested',
      'interruption.completed',
      'turn.interrupted'
    ]);
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL host is outside Anthropic allowlist', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://example.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        host: 'example.com',
        policy: 'REQ-NET-001'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL does not use https', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'http://api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        protocol: 'http:'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed SDK_FAILURE when CHIRALITY_ANTHROPIC_API_URL is malformed', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'not-a-url';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 400,
      details: expect.objectContaining({
        category: 'INVALID_BASE_URL'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL includes credentials', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://user:pass@api.anthropic.com/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails closed when CHIRALITY_ANTHROPIC_API_URL uses non-default https port', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com:444/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 400,
      details: expect.objectContaining({
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        port: '444'
      })
    });
    expect(clientFactory).not.toHaveBeenCalled();
    expect(createMock).not.toHaveBeenCalled();
  });

  it('accepts CHIRALITY_ANTHROPIC_API_URL when explicit default https port is used', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_API_URL = 'https://api.anthropic.com:443/v1/messages';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith({
      apiKey: 'test-key',
      baseURL: 'https://api.anthropic.com',
      anthropicVersion: '2023-06-01'
    });
    expect(createMock).toHaveBeenCalledTimes(1);
  });

  it('maps SDK auth errors to typed invalid-key failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'invalid x-api-key'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 401,
      details: expect.objectContaining({
        category: 'INVALID_API_KEY'
      })
    });
  });

  it('maps SDK 429 status errors to typed rate-limited failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 429,
      error: {
        type: 'rate_limit_error',
        message: 'rate limit reached for key test-key'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 429,
      details: expect.objectContaining({
        category: 'RATE_LIMITED'
      })
    });
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('maps named RateLimitError SDK errors without status to typed rate-limited failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const rateLimitError = new Error('rate limit reached for key test-key');
    rateLimitError.name = 'RateLimitError';
    const createMock = vi.fn().mockRejectedValue(rateLimitError);
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 429,
      details: expect.objectContaining({
        category: 'RATE_LIMITED'
      })
    });
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('maps SDK 5xx status errors to typed API response failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 529,
      error: {
        type: 'overloaded_error',
        message: 'upstream overloaded while serving key test-key'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 529,
      details: expect.objectContaining({
        category: 'API_RESPONSE_ERROR'
      })
    });
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('maps unreachable-endpoint failures to typed 503 network errors', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue(new Error('socket hang up while sending key test-key'));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 503,
      details: expect.objectContaining({
        category: 'NETWORK_ERROR',
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test-key')
      })
    });
  });

  it('maps stream timeouts to typed 504 request-timeout failures', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS = '25';
    const createMock = vi.fn(
      (_request: unknown, options: { signal: AbortSignal }) =>
        new Promise((_resolve, reject) => {
          options.signal.addEventListener('abort', () => {
            const abortError = new Error('Request aborted');
            abortError.name = 'AbortError';
            reject(abortError);
          });
        })
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    const events: UIEvent[] = [];
    let thrown: unknown;

    try {
      for await (const event of manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }])) {
        events.push(event);
      }
    } catch (error) {
      thrown = error;
    }

    expect(events.map((event) => event.type)).toEqual([
      'session:init',
      'harness:event',
      'harness:event'
    ]);
    expect(events.slice(1).map((event) => (event as { data: { type: string } }).data.type)).toEqual([
      'turn.accepted',
      'turn.failed'
    ]);
    expect(thrown).toMatchObject({
      type: 'SDK_FAILURE',
      status: 504,
      details: expect.objectContaining({
        category: 'REQUEST_TIMEOUT'
      })
    });
    expect((thrown as Error).message).toContain('Anthropic request timed out');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('redacts configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'provided key test-key is invalid'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('redacts URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${encodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(encodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts lowercase URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${lowercaseEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(lowercaseEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${doubleEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded query-style configured API key material from SDK error messages', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: `provided key ${doubleQueryEncodedKey} is invalid`
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleQueryEncodedKey);
    expect((thrown as Error).message).not.toContain('test key/with space');
  });

  it('redacts overlapping canonical and alias key material without leaking suffixes', async () => {
    process.env.ANTHROPIC_API_KEY = 'KEY';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'KEY_LONG';
    const createMock = vi.fn().mockRejectedValue({
      status: 401,
      error: {
        type: 'authentication_error',
        message: 'canonical=KEY alias=KEY_LONG failed'
      }
    });
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toBe(
      'canonical=[REDACTED_API_KEY] alias=[REDACTED_API_KEY] failed'
    );
    expect((thrown as Error).message).not.toContain('KEY_LONG');
    expect((thrown as Error).message).not.toContain('_LONG');
  });

  it('redacts configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: 'upstream rejected key test-key'
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain('test-key');
  });

  it('redacts URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${encodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(encodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts lowercase URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${lowercaseEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(lowercaseEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${doubleEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleEncodedKey);
    expect((thrown as Error).message).not.toContain('test:key/with?chars=1');
  });

  it('redacts double URL-encoded query-style configured API key material from stream error events', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockResolvedValue(
      createStream([
        {
          type: 'error',
          error: {
            status: 502,
            type: 'api_error',
            message: `upstream rejected key ${doubleQueryEncodedKey}`
          }
        }
      ])
    );
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toBeInstanceOf(Error);
    expect((thrown as Error).message).toContain('[REDACTED_API_KEY]');
    expect((thrown as Error).message).not.toContain(doubleQueryEncodedKey);
    expect((thrown as Error).message).not.toContain('test key/with space');
  });

  it('redacts configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const createMock = vi.fn().mockRejectedValue(new Error('socket rejected key test-key'));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test-key')
      })
    });
  });

  it('redacts URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const encodedKey = encodeURIComponent(process.env.ANTHROPIC_API_KEY);
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${encodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(encodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts lowercase URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const lowercaseEncodedKey = toLowercasePercentEncoding(
      encodeURIComponent(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${lowercaseEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(lowercaseEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts double URL-encoded configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test:key/with?chars=1';
    const doubleEncodedKey = toLowercasePercentEncoding(
      toDoubleUrlEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi.fn().mockRejectedValue(new Error(`socket rejected key ${doubleEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(doubleEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test:key/with?chars=1')
      })
    });
  });

  it('redacts double URL-encoded query-style configured API key material from network error details', async () => {
    process.env.ANTHROPIC_API_KEY = 'test key/with space';
    const doubleQueryEncodedKey = toLowercasePercentEncoding(
      toDoubleQueryStyleEncoding(process.env.ANTHROPIC_API_KEY)
    );
    const createMock = vi
      .fn()
      .mockRejectedValue(new Error(`socket rejected key ${doubleQueryEncodedKey}`));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.stringContaining('[REDACTED_API_KEY]')
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining(doubleQueryEncodedKey)
      })
    });
    expect(thrown).toMatchObject({
      details: expect.objectContaining({
        cause: expect.not.stringContaining('test key/with space')
      })
    });
  });

  it('uses compatibility alias key when canonical key is unset', async () => {
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'alias-key'
      })
    );
  });

  it('prefers canonical API key when both canonical and alias keys are set', async () => {
    process.env.ANTHROPIC_API_KEY = 'canonical-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'canonical-key'
      })
    );
  });

  it('prefers UI-provided key over environment keys when both are set', async () => {
    globalState.__CHIRALITY_UI_API_KEY__ = 'ui-key';
    process.env.ANTHROPIC_API_KEY = 'canonical-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'ui-key'
      })
    );
  });

  it('falls back to canonical environment key after UI key is cleared', async () => {
    globalState.__CHIRALITY_UI_API_KEY__ = 'ui-key';
    delete globalState.__CHIRALITY_UI_API_KEY__;
    process.env.ANTHROPIC_API_KEY = 'canonical-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'alias-key';
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(manager.startTurn(session, 'hello', opts, [{ type: 'text', text: 'hello' }]));

    expect(clientFactory).toHaveBeenCalledWith(
      expect.objectContaining({
        apiKey: 'canonical-key'
      })
    );
  });

  it('formats image attachments as Anthropic image content blocks', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('fake-image-data');
    const imagePath = await writeFixtureFile('fixture.png', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: 'application/octet-stream' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('fails with typed ATTACHMENT_FAILURE when image attachment is unreadable', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const missingImagePath = await getFixturePath('missing-fixture.png');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(
        manager.startTurn(session, 'hello', opts, [
          { type: 'text', text: 'hello' },
          { type: 'file', path: missingImagePath, mimeType: 'image/png' }
        ])
      );
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      type: 'ATTACHMENT_FAILURE',
      status: 400,
      details: {
        path: missingImagePath
      }
    });
    expect((thrown as Error).message).toContain(`Attachment '${missingImagePath}' is not readable`);
    expect(createMock).not.toHaveBeenCalled();
  });

  it('fails with typed ATTACHMENT_FAILURE when image attachment exceeds inline byte limit', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const oversizedImagePath = await writeFixtureFile(
      'oversized-image.png',
      Buffer.alloc((5 * 1024 * 1024) + 1, 1)
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);
    let thrown: unknown;

    try {
      await collectEvents(
        manager.startTurn(session, 'hello', opts, [
          { type: 'text', text: 'hello' },
          { type: 'file', path: oversizedImagePath, mimeType: 'image/png' }
        ])
      );
    } catch (error) {
      thrown = error;
    }

    expect(thrown).toMatchObject({
      type: 'ATTACHMENT_FAILURE',
      status: 400,
      details: {
        path: oversizedImagePath,
        byteLength: (5 * 1024 * 1024) + 1,
        limit: 5 * 1024 * 1024
      }
    });
    expect((thrown as Error).message).toContain('exceeds 5242880 byte inline image limit');
    expect(createMock).not.toHaveBeenCalled();
  });

  it('accepts image attachment when byte size is exactly at inline limit', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const maxInlineBytes = 5 * 1024 * 1024;
    const atLimitImageBytes = Buffer.alloc(maxInlineBytes, 1);
    const atLimitImagePath = await writeFixtureFile('at-limit-image.png', atLimitImageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: atLimitImagePath, mimeType: 'image/png' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: atLimitImageBytes.toString('base64')
        }
      }
    ]);
  });

  it('normalizes resolver-provided image mime metadata before classification', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data');
    const imagePath = await writeFixtureFile('resolver-output.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' Image/PNG ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('normalizes resolver-provided image mime metadata with parameters', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data-with-params');
    const imagePath = await writeFixtureFile('resolver-output-with-params.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' Image/PNG; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('treats uppercase octet-stream mime as extension-fallback input', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-octet-stream-image-data');
    const imagePath = await writeFixtureFile('resolver-output.PNG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' APPLICATION/OCTET-STREAM ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('treats parameterized octet-stream mime as extension-fallback input', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-octet-stream-image-data-with-params');
    const imagePath = await writeFixtureFile('resolver-output-with-params.PNG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' APPLICATION/OCTET-STREAM; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has no media-type token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-missing-token-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-empty-token.JpEg', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension and normalizes webp when resolver mime metadata has no media-type token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-missing-token-webp-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-empty-token.WeBp', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has malformed image token without subtype', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-malformed-token-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-malformed-token.GiF', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/ ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/gif',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has malformed image token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-malformed-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/ ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-malformed-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has wildcard subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-wildcard-subtype-image-data');
    const imagePath = await writeFixtureFile('resolver-output-with-wildcard-token.PnG', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/* ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has wildcard subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-wildcard-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/* ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-wildcard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-image-subtype-data');
    const imagePath = await writeFixtureFile('resolver-output-with-unsupported-image-token.JpEg', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/bmp ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-unsupported-image-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/bmp ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-image-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported image alias subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-image-alias-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-image-alias-token.JpEg',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jpg ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/jpeg',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported image alias subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-image-alias-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jpg ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-image-alias-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported vendor-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-vendor-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-vendor-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/x-png ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported vendor-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-vendor-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/x-png ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-vendor-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported dotted vendor-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-dotted-vendor-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-dotted-vendor-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/vnd.microsoft.icon ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported dotted vendor-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-dotted-vendor-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/vnd.microsoft.icon ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-dotted-vendor-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported personal-tree image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-personal-tree-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-personal-tree-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/prs.btif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported personal-tree image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-personal-tree-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/prs.btif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-personal-tree-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/heic ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/heic ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported alternative standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-alt-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-alt-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/avif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported alternative standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-alt-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/avif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-alt-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported additional alternative standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-additional-alt-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-alt-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jxl ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported additional alternative standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-alt-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jxl ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-additional-alt-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported additional standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-additional-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/tiff ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported additional standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/tiff ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-additional-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported supplementary standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-supplementary-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-supplementary-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jp2 ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported supplementary standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-supplementary-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jp2 ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-supplementary-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported additional supplementary standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-additional-supplementary-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-supplementary-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jpx ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported additional supplementary standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-supplementary-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jpx ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-additional-supplementary-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported further supplementary standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-further-supplementary-standard-image-subtype-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-further-supplementary-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jpm ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported further supplementary standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-further-supplementary-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jpm ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-further-supplementary-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported additional further supplementary standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from(
      'resolver-unsupported-additional-further-supplementary-standard-image-subtype-data'
    );
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-further-supplementary-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/jph ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported additional further supplementary standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-further-supplementary-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/jph ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-additional-further-supplementary-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported additional high-efficiency standard image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from(
      'resolver-unsupported-additional-high-efficiency-standard-image-subtype-data'
    );
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-high-efficiency-standard-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/heif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported additional high-efficiency standard image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-additional-high-efficiency-standard-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/heif ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-additional-high-efficiency-standard-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to extension when resolver mime metadata has unsupported structured-suffix image subtype token', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-unsupported-structured-suffix-image-data');
    const imagePath = await writeFixtureFile(
      'resolver-output-with-unsupported-structured-suffix-token.WeBp',
      imageBytes
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: ' image/svg+xml ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/webp',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has unsupported structured-suffix image subtype token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile(
      'resolver-output-with-unsupported-structured-suffix-token.bin',
      'placeholder'
    );
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' image/svg+xml ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-unsupported-structured-suffix-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('falls back to explicit text when resolver mime metadata has no media-type token and extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const filePath = await writeFixtureFile('resolver-output-with-empty-token.bin', 'placeholder');
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' ; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'text',
        text:
          "Attachment 'resolver-output-with-empty-token.bin' is available locally but not yet mapped to Anthropic multimodal request types."
      }
    ]);
  });

  it('trusts resolver-provided image mime type even when extension is non-image', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const imageBytes = Buffer.from('resolver-classified-image-data');
    const imagePath = await writeFixtureFile('resolver-output.bin', imageBytes);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: imagePath, mimeType: 'image/png' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'image',
        source: {
          type: 'base64',
          media_type: 'image/png',
          data: imageBytes.toString('base64')
        }
      }
    ]);
  });

  it('keeps resolver-provided non-image mime authoritative even when extension is image-like', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const pdfContent = '%PDF-1.7 test';
    const filePath = await writeFixtureFile('resolver-classified.png', pdfContent);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: 'application/pdf' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'document',
        title: 'resolver-classified.png',
        source: {
          type: 'base64',
          media_type: 'application/pdf',
          data: Buffer.from(pdfContent).toString('base64')
        }
      }
    ]);
  });

  it('keeps parameterized resolver-provided non-image mime authoritative even when extension is image-like', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const pdfContent = '%PDF-1.7 test';
    const filePath = await writeFixtureFile('resolver-classified-with-params.png', pdfContent);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review attachment', opts, [
        { type: 'text', text: 'review attachment' },
        { type: 'file', path: filePath, mimeType: ' application/pdf; charset=binary ' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'review attachment' },
      {
        type: 'document',
        title: 'resolver-classified-with-params.png',
        source: {
          type: 'base64',
          media_type: 'application/pdf',
          data: Buffer.from(pdfContent).toString('base64')
        }
      }
    ]);
  });

  it('formats resolver-provided text attachments into Anthropic plain-text document blocks', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const textPayload = 'hello';
    const filePath = await writeFixtureFile('notes.txt', textPayload);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'hello', opts, [
        { type: 'text', text: 'hello' },
        { type: 'file', path: filePath, mimeType: 'text/plain' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      { type: 'text', text: 'hello' },
      {
        type: 'document',
        title: 'notes.txt',
        source: {
          type: 'text',
          media_type: 'text/plain',
          data: textPayload
        }
      }
    ]);
  });

  it('preserves resolver warning text blocks while mapping pdf attachments to document blocks', async () => {
    process.env.ANTHROPIC_API_KEY = 'test-key';
    const pdfContent = '%PDF-1.7 test';
    const filePath = await writeFixtureFile('spec.pdf', pdfContent);
    const createMock = vi.fn().mockResolvedValue(createStream([{ type: 'message_stop' }]));
    const clientFactory = vi.fn(() => ({
      messages: {
        create: createMock
      }
    }));
    const manager = new AnthropicAgentSdkManager(clientFactory as never);

    await collectEvents(
      manager.startTurn(session, 'review the attachment', opts, [
        {
          type: 'text',
          text: "Attachment warning: 'legacy.bmp' rejected (unsupported extension)."
        },
        { type: 'text', text: 'review the attachment' },
        { type: 'file', path: filePath, mimeType: 'application/pdf' }
      ])
    );

    expect(createMock).toHaveBeenCalledTimes(1);
    const request = createMock.mock.calls[0][0] as {
      messages: Array<{ content: Array<Record<string, unknown>> }>;
    };
    expect(request.messages[0].content).toEqual([
      {
        type: 'text',
        text: "Attachment warning: 'legacy.bmp' rejected (unsupported extension)."
      },
      { type: 'text', text: 'review the attachment' },
      {
        type: 'document',
        title: 'spec.pdf',
        source: {
          type: 'base64',
          media_type: 'application/pdf',
          data: Buffer.from(pdfContent).toString('base64')
        }
      }
    ]);
  });
});
