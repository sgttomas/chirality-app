import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { AgentEngineRunInput } from '@chirality/runtime-contracts/agent-engine-port';
import { runEngineInterruptConformance } from '@chirality/runtime-contracts/engine-conformance';
import type { ResolvedOpts, SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';
import {
  createIsolatedPiResourceLoader,
  createIsolatedPiSession,
  createOmlxDiagnosticGuard,
  createOmlxRedirectGuard,
  installOmlxRedirectGuard,
  PiAgentEngineAdapter,
  type PiAgentEngineAdapterDependencies,
  type PiCustomToolDefinition,
  type PiSessionFactoryInput,
  type PiSessionLike
} from '../../lib/harness/pi-agent-engine-adapter';

const session: SessionRecord = {
  sessionId: 'sess_pi_test',
  projectRoot: '/tmp/chirality-pi-project',
  persona: 'TASK',
  mode: 'direct',
  createdAt: '2026-07-21T00:00:00.000Z',
  updatedAt: '2026-07-21T00:00:00.000Z',
  agentType: 2,
  parentSessionId: 'sess_parent',
  parentAgentType: 1,
  approvalRef: 'D-APP-72',
  allowedWriteTargets: []
};

const opts: ResolvedOpts = {
  model: 'local-model-exact',
  tools: ['read_file'],
  maxTurns: 2,
  persona: 'TASK',
  mode: 'direct'
};

const provider = {
  baseUrl: 'http://127.0.0.1:8000/v1',
  apiKey: 'omlx-secret-test-key',
  model: {
    id: 'local-model-exact',
    contextWindow: 32_768,
    maxTokens: 4_096
  }
};

const defaultReadTool: PiCustomToolDefinition = {
  name: 'read_file',
  description: 'Read a bounded file',
  parameters: {},
  chirality: {
    descriptorName: 'read_file',
    permissions: ['read'],
    pathScope: '/tmp/chirality-pi-project',
    readOnly: true,
    evidenceSource: 'chirality-tool-bridge'
  },
  execute: vi.fn()
};

let tmpDir = '';

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

async function useTempSessionRoot(): Promise<void> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-pi-adapter-'));
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpDir, 'sessions');
}

function runInput(overrides: Partial<AgentEngineRunInput> = {}): AgentEngineRunInput {
  return {
    session,
    message: 'hello',
    opts,
    turnId: 'turn_pi_test',
    ...overrides
  };
}

class FakePiSession implements PiSessionLike {
  readonly sessionFile = undefined;
  private listener?: (event: { type: string; [key: string]: unknown }) => void;
  readonly abort = vi.fn(async () => undefined);
  readonly dispose = vi.fn();
  readonly prompts: string[] = [];

  constructor(
    readonly sessionId: string,
    private readonly activeTools: string[],
    private readonly script: Array<{ type: string; [key: string]: unknown }> = [],
    private readonly promptImpl?: () => Promise<void>
  ) {}

  subscribe(listener: (event: { type: string; [key: string]: unknown }) => void): () => void {
    this.listener = listener;
    return () => {
      this.listener = undefined;
    };
  }

  async prompt(text: string, options?: { expandPromptTemplates?: boolean }): Promise<void> {
    this.prompts.push(text);
    expect(options).toEqual({ expandPromptTemplates: false });
    for (const event of this.script) {
      this.listener?.(event);
    }
    await this.promptImpl?.();
  }

  async waitForIdle(): Promise<void> {
    return undefined;
  }

  getActiveToolNames(): string[] {
    return [...this.activeTools];
  }

  emit(event: { type: string; [key: string]: unknown }): void {
    this.listener?.(event);
  }
}

function adapterWith(
  factory: (input: PiSessionFactoryInput) => Promise<PiSessionLike>,
  overrides: Partial<PiAgentEngineAdapterDependencies> = {}
): PiAgentEngineAdapter {
  return new PiAgentEngineAdapter({
    resolveProvider: vi.fn(async () => provider),
    buildSystemPrompt: vi.fn(async () => 'sealed Chirality prompt'),
    createSession: factory,
    customTools: [defaultReadTool],
    ...overrides
  });
}

async function collect(stream: AsyncIterable<UIEvent>): Promise<UIEvent[]> {
  const events: UIEvent[] = [];
  for await (const event of stream) {
    events.push(event);
  }
  return events;
}

describe('PiAgentEngineAdapter', () => {
  it('authorizes the exact union of the bound child tool and Runtime method tools', async () => {
    await useTempSessionRoot();
    const runtimeTool: PiCustomToolDefinition = {
      ...defaultReadTool,
      name: 'chirality_list_methods',
      description: 'List admitted methods'
    };
    const createSession = vi.fn(async (input: PiSessionFactoryInput) =>
      new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [
        { type: 'agent_start' }, { type: 'turn_start' },
        { type: 'message_end', message: { role: 'assistant', content: [{ type: 'text', text: 'ok' }] } },
        { type: 'turn_end', message: { role: 'assistant', usage: { output: 1 } } },
        { type: 'agent_end', willRetry: false }, { type: 'agent_settled' }
      ])
    );
    const adapter = adapterWith(createSession, {
      resolveCustomTools: vi.fn(async () => [defaultReadTool, runtimeTool])
    });
    await collect(adapter.startTurn(runInput({
      runtimeTools: [{
        name: 'chirality_list_methods', description: 'List admitted methods', inputSchema: { type: 'object' },
        permission: { effect: 'allow', operation: 'read' }, execute: async () => ({ methods: [] })
      }]
    })));
    expect(createSession.mock.calls[0]?.[0].customTools.map((tool) => tool.name)).toEqual([
      'read_file', 'chirality_list_methods'
    ]);
  });

  it('admits only the exact Runtime method-change control beside the required read tool', async () => {
    await useTempSessionRoot();
    const controlTool: PiCustomToolDefinition = {
      name: 'chirality_request_method_change',
      description: 'Request a method change at the terminal turn boundary',
      parameters: {},
      chirality: {
        descriptorName: 'chirality_request_method_change',
        permissions: ['control'],
        pathScope: [],
        readOnly: false,
        evidenceSource: 'chirality-tool-bridge'
      },
      execute: vi.fn()
    };
    const createSession = vi.fn(async (input: PiSessionFactoryInput) =>
      new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [
        { type: 'agent_start' }, { type: 'turn_start' },
        { type: 'message_end', message: { role: 'assistant', content: [{ type: 'text', text: 'ok' }] } },
        { type: 'turn_end', message: { role: 'assistant', usage: { output: 1 } } },
        { type: 'agent_end', willRetry: false }, { type: 'agent_settled' }
      ])
    );
    const adapter = adapterWith(createSession, {
      resolveCustomTools: vi.fn(async () => [defaultReadTool, controlTool])
    });
    const runtimeControl = {
      name: 'chirality_request_method_change',
      description: 'Request method change',
      inputSchema: { type: 'object' },
      permission: { effect: 'allow' as const, operation: 'control' as const },
      execute: async () => ({ requested: true })
    };

    await collect(adapter.startTurn(runInput({ runtimeTools: [runtimeControl] })));
    expect(createSession.mock.calls[0]?.[0].customTools.map((tool) => tool.name)).toEqual([
      'read_file', 'chirality_request_method_change'
    ]);

    const unrecognizedControl = {
      ...controlTool,
      name: 'unrecognized_control',
      chirality: { ...controlTool.chirality, descriptorName: 'unrecognized_control' }
    };
    const rejectingAdapter = adapterWith(createSession, {
      resolveCustomTools: vi.fn(async () => [defaultReadTool, unrecognizedControl])
    });
    await expect(collect(rejectingAdapter.startTurn(runInput({
      runtimeTools: [{ ...runtimeControl, name: 'unrecognized_control' }]
    })))).resolves.toEqual(expect.arrayContaining([
      expect.objectContaining({
        type: 'turn:error',
        data: expect.objectContaining({ errorType: 'INVALID_REQUEST', status: 400 })
      }),
      expect.objectContaining({ type: 'process:exit', data: expect.objectContaining({ exitCode: 1 }) })
    ]));
  });

  it('prepares a reversible successor and uses a fresh Pi identity with prior dialogue only', async () => {
    await useTempSessionRoot();
    let created: FakePiSession | undefined;
    const createSession = vi.fn(async (input: PiSessionFactoryInput) => {
      created = new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [
        { type: 'agent_start' }, { type: 'turn_start' },
        { type: 'message_end', message: { role: 'assistant', content: [{ type: 'text', text: 'continued' }] } },
        { type: 'turn_end', message: { role: 'assistant', usage: { output: 1 } } },
        { type: 'agent_end', willRetry: false }, { type: 'agent_settled' }
      ]);
      return created;
    });
    const adapter = adapterWith(createSession);
    const prepared = await adapter.prepareContextSuccessor({
      sessionId: session.sessionId, predecessorEngineSessionId: 'pi-old', fromBasisId: 'basis-old',
      toBasisPreview: { id: 'basis-new', sha256: 'a'.repeat(64) },
      continuationContext: {
        transcript: '[{"role":"user","text":"prior human"},{"role":"assistant","text":"prior assistant"}]',
        sha256: 'b'.repeat(64), priorBasisRefs: [{ basisId: 'basis-old', sha256: 'c'.repeat(64) }]
      }
    });
    await expect(adapter.cancelContextSuccessor(prepared.preparationId)).resolves.toBeUndefined();
    await collect(adapter.startTurn(runInput({
      session: { ...session, engineSessionId: 'pi-old' },
      message: 'new request', contextSuccessor: prepared
    })));
    expect(createSession.mock.calls[0]?.[0].engineSessionId).not.toBe('pi-old');
    expect(created?.prompts[0]).toContain('prior human');
    expect(created?.prompts[0]).toContain('prior assistant');
    expect(created?.prompts[0]).toContain('basis-new');
    expect(created?.prompts[0]).toContain('new request');
    expect(created?.prompts[0]).not.toContain('sealed Chirality prompt');
  });

  it('publishes exact Pi/oMLX attribution and bootstraps without creating a Pi session', async () => {
    await useTempSessionRoot();
    const createSession = vi.fn(async () => {
      throw new Error('bootstrap must not create a provider session');
    });
    const adapter = adapterWith(createSession);
    const input = runInput({ message: 'bootstrap' });

    await expect(adapter.preflight(input)).resolves.toBeUndefined();
    const events = await collect(adapter.startTurn(input));

    expect(adapter.descriptor).toMatchObject({
      adapterId: 'pi',
      providerId: 'omlx',
      packageName: '@earendil-works/pi-coding-agent',
      packageVersion: '0.82.0'
    });
    expect(events).toHaveLength(2);
    expect(events[0]).toMatchObject({
      type: 'session:init',
      data: { adapterId: 'pi', providerId: 'omlx', model: 'local-model-exact' }
    });
    expect(events[1]).toEqual({ type: 'process:exit', data: { exitCode: 0 } });
    expect(createSession).not.toHaveBeenCalled();
  });

  it('streams text through canonical events with one terminal process exit', async () => {
    await useTempSessionRoot();
    const createSession = vi.fn(async (input: PiSessionFactoryInput) =>
      new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [
        { type: 'agent_start' },
        { type: 'turn_start' },
        {
          type: 'message_update',
          assistantMessageEvent: { type: 'text_delta', delta: 'Hello' }
        },
        {
          type: 'message_end',
          message: { role: 'assistant', content: [{ type: 'text', text: 'Hello' }] }
        },
        { type: 'turn_end', message: { role: 'assistant', usage: { output: 1 } } },
        { type: 'agent_end', willRetry: false },
        { type: 'agent_settled' }
      ])
    );
    const adapter = adapterWith(createSession);

    const events = await collect(adapter.startTurn(runInput()));

    expect(events[0]?.type).toBe('session:init');
    expect(events.at(-1)).toEqual({ type: 'process:exit', data: { exitCode: 0 } });
    expect(events.filter((event) => event.type === 'process:exit')).toHaveLength(1);
    expect(events).toContainEqual({ type: 'chat:delta', data: { text: 'Hello' } });
    expect(events).toContainEqual({ type: 'chat:complete', data: { text: 'Hello' } });
    expect(events).toContainEqual({ type: 'session:complete', data: {} });
    expect(createSession).toHaveBeenCalledWith(
      expect.objectContaining({ systemPrompt: 'sealed Chirality prompt', customTools: [defaultReadTool] })
    );
  });

  it('allows only exact requested read-only Chirality tools without persisting Pi arguments or results', async () => {
    await useTempSessionRoot();
    const readTool = defaultReadTool;
    const sensitivePath = `/private/${provider.apiKey}/README.md`;
    const sensitiveResult = `file body contains ${provider.apiKey}`;
    const createSession = vi.fn(async (input: PiSessionFactoryInput) =>
      new FakePiSession(input.engineSessionId, ['read_file'], [
        {
          type: 'tool_execution_start',
          toolCallId: 'tool_1',
          toolName: 'read_file',
          args: { file_path: sensitivePath }
        },
        {
          type: 'tool_execution_end',
          toolCallId: 'tool_1',
          toolName: 'read_file',
          result: { content: [{ type: 'text', text: sensitiveResult }] },
          isError: false
        },
        { type: 'agent_end', willRetry: false }
      ])
    );
    const adapter = adapterWith(createSession, { customTools: [readTool] });
    const input = runInput({ opts: { ...opts, tools: ['read_file'] } });

    await expect(adapter.preflight(input)).resolves.toBeUndefined();
    const events = await collect(adapter.startTurn(input));

    expect(createSession.mock.calls[0]?.[0].customTools).toEqual([readTool]);
    expect(events).toContainEqual({
      type: 'tool:result',
      data: { name: 'read_file', ok: true }
    });
    const persisted = await readFile(
      path.join(process.env.CHIRALITY_SESSION_ROOT!, session.sessionId, 'events.jsonl'),
      'utf8'
    );
    expect(persisted).not.toContain(sensitivePath);
    expect(persisted).not.toContain(sensitiveResult);
    expect(persisted).not.toContain(provider.apiKey);
    expect(persisted).not.toContain('"type":"tool.started"');
    expect(persisted).not.toContain('"type":"tool.completed"');
    expect(events.filter((event) => event.type === 'process:exit')).toHaveLength(1);
  });

  it('fails closed for an undeclared or non-read-only tool', async () => {
    await useTempSessionRoot();
    const unsafe = {
      name: 'write_file',
      description: 'unsafe',
      parameters: {},
      chirality: {
        descriptorName: 'write_file',
        permissions: ['write'],
        pathScope: '/tmp/chirality-pi-project',
        readOnly: false,
        evidenceSource: 'chirality-tool-bridge'
      },
      execute: vi.fn()
    } as unknown as PiCustomToolDefinition;
    const adapter = adapterWith(vi.fn(), { customTools: [unsafe] });

    await expect(
      adapter.preflight(runInput({ opts: { ...opts, tools: ['write_file'] } }))
    ).rejects.toThrow('not an explicitly classified read tool or exact Runtime session-control tool');
    await expect(
      adapterWith(vi.fn(), { customTools: [] }).preflight(
        runInput({ opts: { ...opts, tools: ['read_file'] } })
      )
    ).rejects.toThrow('must exactly match the authorized turn tool allowlist');
  });

  it('rejects direct/supervisor sessions, write targets, and file attachments', async () => {
    await useTempSessionRoot();
    const adapter = adapterWith(vi.fn());

    await expect(
      adapter.preflight(runInput({ session: { ...session, agentType: 1 } }))
    ).rejects.toThrow('restricted to an approved managed Agent 2 child');
    await expect(
      adapter.preflight(runInput({ session: { ...session, allowedWriteTargets: ['OUTPUT.md'] } }))
    ).rejects.toThrow('cannot receive write targets');
    await expect(
      adapter.preflight(
        runInput({
          contentBlocks: [{ type: 'file', path: '/tmp/input.txt', mimeType: 'text/plain' }]
        })
      )
    ).rejects.toThrow('does not accept file attachments');
  });

  it('normalizes injected oMLX discovery failures to provider-neutral harness errors', async () => {
    await useTempSessionRoot();
    const adapter = adapterWith(vi.fn(), {
      resolveProvider: vi.fn(async () => {
        throw Object.assign(new Error('oMLX is unavailable'), { code: 'OMLX_OFFLINE' });
      })
    });

    await expect(adapter.preflight(runInput())).rejects.toMatchObject({
      type: 'ENGINE_UNAVAILABLE',
      status: 503,
      message: 'oMLX is unavailable'
    });
  });

  it('maps provider failures, redacts the credential, and emits one failing terminal', async () => {
    await useTempSessionRoot();
    const createSession = vi.fn(async (input: PiSessionFactoryInput) =>
      new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [
        {
          type: 'message_update',
          assistantMessageEvent: {
            type: 'error',
            error: { errorMessage: `unauthorized ${provider.apiKey}` }
          }
        },
        { type: 'agent_end', willRetry: false }
      ])
    );
    const events = await collect(adapterWith(createSession).startTurn(runInput()));
    const turnError = events.find((event) => event.type === 'turn:error');
    const exits = events.filter((event) => event.type === 'process:exit');

    expect(turnError).toMatchObject({
      type: 'turn:error',
      data: { errorType: 'PROVIDER_AUTH_FAILURE', fatal: true }
    });
    expect(JSON.stringify(events)).not.toContain(provider.apiKey);
    expect(exits).toHaveLength(1);
    expect(exits[0]).toMatchObject({ type: 'process:exit', data: { exitCode: 1 } });
  });

  it('times out and aborts a provider stream that never reaches idle', async () => {
    await useTempSessionRoot();
    const never = new Promise<void>(() => undefined);
    let fake: FakePiSession | undefined;
    const adapter = adapterWith(async (input) => {
      fake = new FakePiSession(input.engineSessionId, ['read_file'], [], () => never);
      return fake;
    }, { turnTimeoutMs: 5 });

    const events = await collect(adapter.startTurn(runInput({ turnId: 'turn_pi_timeout' })));

    expect(fake?.abort).toHaveBeenCalledOnce();
    expect(events.filter((event) => event.type === 'turn:error')).toEqual([
      expect.objectContaining({
        data: expect.objectContaining({
          errorType: 'PROVIDER_PROTOCOL_FAILURE',
          status: 504
        })
      })
    ]);
    expect(events.filter((event) => event.type === 'process:exit')).toEqual([
      expect.objectContaining({
        data: expect.objectContaining({
          exitCode: 1,
          errorType: 'PROVIDER_PROTOCOL_FAILURE',
          status: 504
        })
      })
    ]);
  });

  it('interrupts an active Pi session and emits the canonical interrupted terminal', async () => {
    await useTempSessionRoot();
    let releasePrompt: () => void = () => undefined;
    let markStarted: () => void = () => undefined;
    const started = new Promise<void>((resolve) => {
      markStarted = resolve;
    });
    const promptPending = new Promise<void>((resolve) => {
      releasePrompt = resolve;
    });
    let fake: FakePiSession;
    const createSession = vi.fn(async (input: PiSessionFactoryInput) => {
      fake = new FakePiSession(input.engineSessionId, input.customTools.map((tool) => tool.name), [], async () => {
        markStarted();
        await promptPending;
      });
      fake.abort.mockImplementation(async () => {
        fake.emit({ type: 'agent_end', willRetry: false });
        releasePrompt();
      });
      return fake;
    });
    const adapter = adapterWith(createSession);
    const collecting = collect(adapter.startTurn(runInput()));
    await started;

    await adapter.interrupt(session.sessionId);
    const events = await collecting;

    expect(fake!.abort).toHaveBeenCalledOnce();
    expect(events.filter((event) => event.type === 'process:exit')).toEqual([
      { type: 'process:exit', data: { exitCode: 130, interrupted: true } }
    ]);
    expect(events.some((event) => event.type === 'harness:event' && event.data.type === 'turn.interrupted')).toBe(true);
  });

  it('passes early-interrupt conformance without constructing or prompting a provider session', async () => {
    await useTempSessionRoot();
    const createSession = vi.fn(async () => {
      throw new Error('early interrupt must not construct Pi');
    });
    const report = await runEngineInterruptConformance(adapterWith(createSession), runInput(), {
      requireEngineSessionId: true
    });

    expect(report.passed).toBe(true);
    expect(report.issues).toEqual([]);
    expect(createSession).not.toHaveBeenCalled();
  });
});

describe('Pi resource and runtime isolation', () => {
  it('redacts malformed upstream SSE payloads before they reach process diagnostics', () => {
    const sink = vi.fn<typeof console.error>();
    const guarded = createOmlxDiagnosticGuard(sink);

    guarded('Could not parse message into JSON:', 'RAW_PROVIDER_SECRET');
    guarded('From chunk:', 'data: RAW_PROVIDER_SECRET');
    guarded('ordinary diagnostic', 'safe detail');

    expect(sink).toHaveBeenNthCalledWith(
      1,
      'Could not parse message into JSON:',
      '[REDACTED_PROVIDER_PAYLOAD]'
    );
    expect(sink).toHaveBeenNthCalledWith(2, 'From chunk:', '[REDACTED_PROVIDER_PAYLOAD]');
    expect(sink).toHaveBeenNthCalledWith(3, 'ordinary diagnostic', 'safe detail');
    expect(JSON.stringify(sink.mock.calls)).not.toContain('RAW_PROVIDER_SECRET');
  });

  it('forces manual redirects only for literal loopback oMLX /v1 requests', async () => {
    const fetchImpl = vi.fn<typeof fetch>(async () => new Response(null, { status: 307 }));
    const guarded = createOmlxRedirectGuard(fetchImpl);
    const omlxInit: RequestInit = { method: 'POST', redirect: 'follow' };
    const externalInit: RequestInit = { method: 'POST', redirect: 'follow' };

    await guarded('http://127.0.0.1:8000/v1/chat/completions', omlxInit);
    await guarded('https://api.anthropic.com/v1/messages', externalInit);

    expect(fetchImpl).toHaveBeenNthCalledWith(1, 'http://127.0.0.1:8000/v1/chat/completions', {
      method: 'POST',
      redirect: 'manual'
    });
    expect(fetchImpl).toHaveBeenNthCalledWith(2, 'https://api.anthropic.com/v1/messages', externalInit);
  });

  it('installs the process redirect guard idempotently', () => {
    const originalFetch = globalThis.fetch;
    try {
      installOmlxRedirectGuard();
      const firstGuard = globalThis.fetch;
      installOmlxRedirectGuard();
      expect(globalThis.fetch).toBe(firstGuard);
      expect(firstGuard).not.toBe(originalFetch);
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it('ignores ambient Pi, agent, prompt, extension, skill, settings, and context sentinels', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-pi-isolation-'));
    await mkdir(path.join(tmpDir, '.pi', 'agent', 'skills', 'ambient'), { recursive: true });
    await mkdir(path.join(tmpDir, '.agents', 'skills', 'ambient'), { recursive: true });
    await writeFile(path.join(tmpDir, 'AGENTS.md'), 'AMBIENT_CONTEXT_SENTINEL');
    await writeFile(path.join(tmpDir, '.pi', 'agent', 'settings.json'), '{"defaultModel":"ambient"}');
    await writeFile(path.join(tmpDir, '.pi', 'agent', 'skills', 'ambient', 'SKILL.md'), 'AMBIENT_SKILL');
    await writeFile(path.join(tmpDir, '.agents', 'skills', 'ambient', 'SKILL.md'), 'AMBIENT_AGENT_SKILL');

    const loader = await createIsolatedPiResourceLoader(tmpDir, 'SEALED_SYSTEM_PROMPT');

    expect(loader.getExtensions().extensions).toEqual([]);
    expect(loader.getSkills().skills).toEqual([]);
    expect(loader.getPrompts().prompts).toEqual([]);
    expect(loader.getThemes().themes).toEqual([]);
    expect(loader.getAgentsFiles().agentsFiles).toEqual([]);
    expect(loader.getSystemPrompt()).toBe('SEALED_SYSTEM_PROMPT');
    expect(loader.getAppendSystemPrompt()).toEqual([]);
  });

  it('constructs a real in-memory Pi session with no built-in tools or transcript', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-pi-real-session-'));
    const piSession = await createIsolatedPiSession({
      cwd: tmpDir,
      engineSessionId: 'pi_isolated_test',
      provider,
      systemPrompt: 'SEALED_SYSTEM_PROMPT',
      customTools: []
    });
    try {
      expect(piSession.sessionId).toBe('pi_isolated_test');
      expect(piSession.sessionFile).toBeUndefined();
      expect(piSession.getActiveToolNames()).toEqual([]);
    } finally {
      piSession.dispose();
    }
  });
});
