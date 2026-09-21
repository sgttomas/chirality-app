import { createHash, randomUUID } from 'node:crypto';
import path from 'node:path';
import type {
  AgentEnginePort,
  AgentEngineRunInput,
  ContextSuccessorRequest,
  PreparedContextSuccessor
} from '@chirality/runtime-contracts/agent-engine-port';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import type { HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import type { HarnessErrorType, UIEvent } from '@chirality/runtime-contracts/types';
import type {
  AgentSessionEvent,
  ResourceLoader,
  ToolDefinition
} from '@earendil-works/pi-coding-agent';
import { createHarnessEvent } from './event-factory';
import { harnessEventToUiEvent } from './harness-ui-bridge';
import { appendHarnessEvent } from './session-events';
import {
  createPiEventMapperState,
  mapPiSessionEvent,
  type PiAgentSessionEventLike,
  type PiHarnessEventDraft,
  type PiTurnFailure
} from './pi-event-mapper';

export const PI_CODING_AGENT_PACKAGE_NAME = '@earendil-works/pi-coding-agent';
export const PI_CODING_AGENT_PACKAGE_VERSION = '0.82.0';

export type PiOmlxModelConfiguration = {
  id: string;
  name?: string;
  reasoning?: boolean;
  input?: Array<'text' | 'image'>;
  contextWindow: number;
  maxTokens: number;
  compat?: Record<string, unknown>;
};

export type PiOmlxProviderConfiguration = {
  baseUrl: string;
  apiKey: string;
  model: PiOmlxModelConfiguration;
};

/**
 * Structural boundary used by the neutral Chirality tool binder. The explicit
 * marker is checked at runtime as defense-in-depth; Pi never receives a tool
 * unless Chirality has classified it as read-only.
 */
export type PiCustomToolDefinition = {
  name: string;
  label?: string;
  description: string;
  parameters: unknown;
  execute: ToolDefinition['execute'];
  chirality: {
    descriptorName: string;
    permissions: readonly string[];
    pathScope: unknown;
    readOnly: boolean;
    evidenceSource: 'chirality-tool-bridge';
  };
};

export type PiSessionFactoryInput = {
  cwd: string;
  engineSessionId: string;
  provider: PiOmlxProviderConfiguration;
  systemPrompt: string;
  customTools: readonly PiCustomToolDefinition[];
};

export type PiSessionLike = {
  readonly sessionId: string;
  readonly sessionFile?: string;
  subscribe(listener: (event: PiAgentSessionEventLike) => void): () => void;
  prompt(text: string, options?: { expandPromptTemplates?: boolean }): Promise<void>;
  waitForIdle(): Promise<void>;
  abort(): Promise<void>;
  dispose(): void;
  getActiveToolNames(): string[];
};

export type PiAgentEngineAdapterDependencies = {
  resolveProvider(input: AgentEngineRunInput): Promise<PiOmlxProviderConfiguration>;
  buildSystemPrompt?(input: AgentEngineRunInput): Promise<string>;
  createSession?(input: PiSessionFactoryInput): Promise<PiSessionLike>;
  resolveCustomTools?(input: AgentEngineRunInput): Promise<readonly PiCustomToolDefinition[]>;
  /** Test/compatibility shortcut; production should bind tools per turn. */
  customTools?: readonly PiCustomToolDefinition[];
  /** Hard ceiling for a provider turn, including hung/disconnected streams. */
  turnTimeoutMs?: number;
};

type ActivePiTurn = {
  input: AgentEngineRunInput;
  session?: PiSessionLike;
  interrupted: boolean;
  cancelled: boolean;
};

const OMLX_REDIRECT_GUARD_STATE = Symbol.for('chirality.omlx.redirect-guard');
const OMLX_DIAGNOSTIC_GUARD_STATE = Symbol.for('chirality.omlx.diagnostic-guard');

type OmlxRedirectGuardState = {
  guardedFetch: typeof fetch;
};

type OmlxDiagnosticGuardState = {
  guardedError: typeof console.error;
};

class AsyncEventQueue<T> implements AsyncIterableIterator<T> {
  private readonly values: T[] = [];
  private readonly waiters: Array<{
    resolve: (result: IteratorResult<T>) => void;
    reject: (error: unknown) => void;
  }> = [];
  private closed = false;
  private failure: unknown;

  [Symbol.asyncIterator](): AsyncIterableIterator<T> {
    return this;
  }

  next(): Promise<IteratorResult<T>> {
    if (this.values.length > 0) {
      return Promise.resolve({ value: this.values.shift() as T, done: false });
    }
    if (this.failure !== undefined) {
      return Promise.reject(this.failure);
    }
    if (this.closed) {
      return Promise.resolve({ value: undefined, done: true });
    }
    return new Promise<IteratorResult<T>>((resolve, reject) => {
      this.waiters.push({ resolve, reject });
    });
  }

  push(value: T): void {
    if (this.closed || this.failure !== undefined) {
      return;
    }
    const waiter = this.waiters.shift();
    if (waiter) {
      waiter.resolve({ value, done: false });
      return;
    }
    this.values.push(value);
  }

  close(): void {
    if (this.closed || this.failure !== undefined) {
      return;
    }
    this.closed = true;
    for (const waiter of this.waiters.splice(0)) {
      waiter.resolve({ value: undefined, done: true });
    }
  }

  fail(error: unknown): void {
    if (this.closed || this.failure !== undefined) {
      return;
    }
    this.failure = error;
    for (const waiter of this.waiters.splice(0)) {
      waiter.reject(error);
    }
  }
}

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function requestUrl(input: Parameters<typeof fetch>[0]): URL | undefined {
  const raw =
    typeof input === 'string' || input instanceof URL
      ? input
      : typeof input.url === 'string'
        ? input.url
        : undefined;
  if (raw === undefined) {
    return undefined;
  }
  try {
    return new URL(raw);
  } catch {
    return undefined;
  }
}

function isOmlxRequest(input: Parameters<typeof fetch>[0]): boolean {
  const url = requestUrl(input);
  return Boolean(
    url &&
      url.protocol === 'http:' &&
      url.hostname === '127.0.0.1' &&
      (url.pathname === '/v1' || url.pathname.startsWith('/v1/'))
  );
}

/**
 * Pi 0.82.0's OpenAI transport does not expose the SDK fetch option. Guard the
 * process fetch narrowly so a loopback model server cannot redirect a prompt or
 * bearer credential off the approved oMLX endpoint.
 */
export function createOmlxRedirectGuard(fetchImpl: typeof fetch): typeof fetch {
  return (async (input, init) => {
    if (!isOmlxRequest(input)) {
      return fetchImpl(input, init);
    }
    return fetchImpl(input, { ...init, redirect: 'manual' });
  }) as typeof fetch;
}

export function installOmlxRedirectGuard(): void {
  const processGlobal = globalThis as typeof globalThis & {
    [OMLX_REDIRECT_GUARD_STATE]?: OmlxRedirectGuardState;
  };
  const existing = processGlobal[OMLX_REDIRECT_GUARD_STATE];
  if (existing?.guardedFetch === globalThis.fetch) {
    return;
  }
  const guardedFetch = createOmlxRedirectGuard(globalThis.fetch.bind(globalThis));
  processGlobal[OMLX_REDIRECT_GUARD_STATE] = { guardedFetch };
  globalThis.fetch = guardedFetch;
}

function isRawProviderParserDiagnostic(value: unknown): boolean {
  return (
    typeof value === 'string' &&
    (value.startsWith('Could not parse message into JSON:') || value.startsWith('From chunk:'))
  );
}

/** Prevent the upstream OpenAI stream parser from echoing malformed provider bytes. */
export function createOmlxDiagnosticGuard(
  errorImpl: typeof console.error
): typeof console.error {
  return ((...args: unknown[]) => {
    if (isRawProviderParserDiagnostic(args[0])) {
      errorImpl(args[0], '[REDACTED_PROVIDER_PAYLOAD]');
      return;
    }
    errorImpl(...args);
  }) as typeof console.error;
}

export function installOmlxDiagnosticGuard(): void {
  const processGlobal = globalThis as typeof globalThis & {
    [OMLX_DIAGNOSTIC_GUARD_STATE]?: OmlxDiagnosticGuardState;
  };
  const existing = processGlobal[OMLX_DIAGNOSTIC_GUARD_STATE];
  if (existing?.guardedError === console.error) {
    return;
  }
  const guardedError = createOmlxDiagnosticGuard(console.error.bind(console));
  processGlobal[OMLX_DIAGNOSTIC_GUARD_STATE] = { guardedError };
  console.error = guardedError;
}

function validateLoopbackBaseUrl(raw: string): string {
  let parsed: URL;
  try {
    parsed = new URL(raw);
  } catch {
    throw new HarnessError('INVALID_REQUEST', 400, 'oMLX base URL must be an absolute loopback URL.');
  }
  if (
    parsed.protocol !== 'http:' ||
    parsed.hostname !== '127.0.0.1' ||
    parsed.username ||
    parsed.password ||
    parsed.search ||
    parsed.hash
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'oMLX base URL must use http://127.0.0.1 with no credentials, query, or fragment.'
    );
  }
  const normalizedPath = parsed.pathname.replace(/\/+$/, '');
  if (normalizedPath !== '/v1') {
    throw new HarnessError('INVALID_REQUEST', 400, 'oMLX base URL path must be exactly /v1.');
  }
  return parsed.toString().replace(/\/$/, '');
}

function validateProviderConfiguration(
  input: AgentEngineRunInput,
  configuration: PiOmlxProviderConfiguration
): PiOmlxProviderConfiguration {
  const apiKey = asNonEmptyString(configuration.apiKey);
  if (!apiKey) {
    throw new HarnessError('MISSING_API_KEY', 503, 'oMLX API key is not configured.', {
      provider: 'omlx'
    });
  }
  const exactModel = asNonEmptyString(configuration.model.id);
  if (!exactModel || exactModel !== input.opts.model) {
    throw new HarnessError(
      'MODEL_UNAVAILABLE',
      503,
      `The exact oMLX model '${input.opts.model}' is not available.`,
      { provider: 'omlx', requestedModel: input.opts.model }
    );
  }
  if (
    !Number.isFinite(configuration.model.contextWindow) ||
    configuration.model.contextWindow <= 0 ||
    !Number.isFinite(configuration.model.maxTokens) ||
    configuration.model.maxTokens <= 0
  ) {
    throw new HarnessError('PROVIDER_PROTOCOL_FAILURE', 502, 'oMLX returned invalid model limits.', {
      provider: 'omlx',
      model: exactModel
    });
  }
  return {
    ...configuration,
    baseUrl: validateLoopbackBaseUrl(configuration.baseUrl),
    apiKey,
    model: { ...configuration.model, id: exactModel }
  };
}

function normalizeProviderResolverError(error: unknown): HarnessError {
  if (error instanceof HarnessError) {
    return error;
  }
  const candidate = error as { code?: unknown; message?: unknown; status?: unknown };
  const message = typeof candidate?.message === 'string' ? candidate.message : 'oMLX provider setup failed.';
  const status = typeof candidate?.status === 'number' ? candidate.status : undefined;
  switch (candidate?.code) {
    case 'OMLX_AUTHENTICATION':
      return new HarnessError('PROVIDER_AUTH_FAILURE', 503, message, { provider: 'omlx' });
    case 'OMLX_MODEL_UNKNOWN':
    case 'OMLX_MODELS_EMPTY':
      return new HarnessError('MODEL_UNAVAILABLE', 503, message, { provider: 'omlx' });
    case 'OMLX_OFFLINE':
      return new HarnessError('ENGINE_UNAVAILABLE', 503, message, { provider: 'omlx' });
    case 'OMLX_CONFIG_INVALID':
      return new HarnessError('INVALID_REQUEST', 400, message, { provider: 'omlx' });
    case 'OMLX_PROTOCOL':
    case 'OMLX_MODELS_MALFORMED':
      return new HarnessError('PROVIDER_PROTOCOL_FAILURE', status ?? 502, message, {
        provider: 'omlx'
      });
    default:
      return new HarnessError('PROVIDER_PROTOCOL_FAILURE', 502, 'oMLX provider setup failed.', {
        provider: 'omlx'
      });
  }
}

function validateBoundedChildPosture(input: AgentEngineRunInput): void {
  const session = input.session;
  if (
    session.agentType !== 2 ||
    !asNonEmptyString(session.parentSessionId) ||
    !asNonEmptyString(session.approvalRef)
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      403,
      'Pi/oMLX is restricted to an approved managed Agent 2 child session.'
    );
  }
  if ((session.allowedWriteTargets ?? []).length > 0) {
    throw new HarnessError(
      'INVALID_REQUEST',
      403,
      'Pi/oMLX Agent 2 children cannot receive write targets in this milestone.'
    );
  }
  if (input.opts.tools.length !== 1) {
    throw new HarnessError(
      'INVALID_REQUEST',
      403,
      'Pi/oMLX Agent 2 children require exactly one authorized read-only tool.'
    );
  }
  if (input.contentBlocks?.some((block) => block.type === 'file')) {
    throw new HarnessError(
      'ATTACHMENT_FAILURE',
      422,
      'The Pi/oMLX milestone does not accept file attachments.'
    );
  }
}

function selectAuthorizedTools(
  input: AgentEngineRunInput,
  availableTools: readonly PiCustomToolDefinition[]
): readonly PiCustomToolDefinition[] {
  const byName = new Map<string, PiCustomToolDefinition>();
  for (const tool of availableTools) {
    const readTool =
      tool.chirality?.readOnly === true &&
      tool.chirality.evidenceSource === 'chirality-tool-bridge' &&
      tool.chirality.permissions.length === 1 &&
      tool.chirality.permissions[0] === 'read';
    const sessionControl =
      tool.name === 'chirality_request_method_change' &&
      tool.chirality?.readOnly === false &&
      tool.chirality.evidenceSource === 'chirality-tool-bridge' &&
      tool.chirality.permissions.length === 1 &&
      tool.chirality.permissions[0] === 'control';
    if (!readTool && !sessionControl) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        `Pi tool '${tool.name}' is not an explicitly classified read tool or exact Runtime session-control tool.`
      );
    }
    if (!asNonEmptyString(tool.name) || byName.has(tool.name)) {
      throw new HarnessError('INVALID_REQUEST', 400, 'Pi custom tool names must be non-empty and unique.');
    }
    byName.set(tool.name, tool);
  }

  const authorizedToolNames = [
    ...input.opts.tools,
    ...(input.runtimeTools ?? []).map((tool) => tool.name)
  ];
  if (new Set(authorizedToolNames).size !== authorizedToolNames.length) {
    throw new HarnessError('INVALID_REQUEST', 400, 'Pi tool allowlist must not contain duplicates.');
  }
  if (
    byName.size !== authorizedToolNames.length ||
    [...byName.keys()].some((name) => !authorizedToolNames.includes(name))
  ) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'Injected Pi tools must exactly match the authorized turn tool allowlist.'
    );
  }

  return authorizedToolNames.map((name) => {
    const tool = byName.get(name);
    if (!tool) {
      throw new HarnessError(
        'INVALID_REQUEST',
        400,
        `Pi tool '${name}' is not present in the authorized Chirality tool set.`
      );
    }
    return tool;
  });
}

function createMemoryCredentialStore(): object {
  const values = new Map<string, unknown>();
  return {
    async read(providerId: string) {
      return values.get(providerId);
    },
    async list() {
      return [];
    },
    async modify(
      providerId: string,
      fn: (current: unknown) => Promise<unknown | undefined>
    ) {
      const next = await fn(values.get(providerId));
      if (next !== undefined) {
        values.set(providerId, next);
      }
      return values.get(providerId);
    },
    async delete(providerId: string) {
      values.delete(providerId);
    }
  };
}

function createMemoryModelsStore(): object {
  const values = new Map<string, unknown>();
  return {
    async read(providerId: string) {
      return values.get(providerId);
    },
    async write(providerId: string, entry: unknown) {
      values.set(providerId, entry);
    },
    async delete(providerId: string) {
      values.delete(providerId);
    }
  };
}

/**
 * Construct a Pi loader that cannot ingest project/global extensions, skills,
 * prompts, themes, AGENTS files, or appended system prompts.
 */
export async function createIsolatedPiResourceLoader(
  cwd: string,
  systemPrompt: string
): Promise<ResourceLoader> {
  const { DefaultResourceLoader, SettingsManager } = await import(
    '@earendil-works/pi-coding-agent'
  );
  const loader = new DefaultResourceLoader({
    cwd,
    agentDir: path.join(cwd, '.chirality-pi-ambient-disabled'),
    settingsManager: SettingsManager.inMemory({}, { projectTrusted: false }),
    noExtensions: true,
    noSkills: true,
    noPromptTemplates: true,
    noThemes: true,
    noContextFiles: true,
    systemPrompt,
    appendSystemPrompt: [],
    extensionsOverride: (base) => ({ ...base, extensions: [], errors: [] }),
    skillsOverride: () => ({ skills: [], diagnostics: [] }),
    promptsOverride: () => ({ prompts: [], diagnostics: [] }),
    themesOverride: () => ({ themes: [], diagnostics: [] }),
    agentsFilesOverride: () => ({ agentsFiles: [] }),
    systemPromptOverride: () => systemPrompt,
    appendSystemPromptOverride: () => []
  });
  await loader.reload();
  return loader;
}

/** Real in-process Pi construction; tests normally inject a narrow fake. */
export async function createIsolatedPiSession(input: PiSessionFactoryInput): Promise<PiSessionLike> {
  installOmlxRedirectGuard();
  installOmlxDiagnosticGuard();
  const {
    createAgentSession,
    ModelRuntime,
    SessionManager,
    SettingsManager
  } = await import('@earendil-works/pi-coding-agent');
  const modelRuntime = await ModelRuntime.create({
    credentials: createMemoryCredentialStore() as never,
    modelsPath: null,
    modelsStore: createMemoryModelsStore() as never,
    allowModelNetwork: false
  });
  modelRuntime.registerProvider('omlx', {
    baseUrl: input.provider.baseUrl,
    api: 'openai-completions',
    models: [
      {
        id: input.provider.model.id,
        name: input.provider.model.name ?? input.provider.model.id,
        reasoning: input.provider.model.reasoning ?? false,
        input: input.provider.model.input ?? ['text'],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: input.provider.model.contextWindow,
        maxTokens: input.provider.model.maxTokens,
        compat: input.provider.model.compat
      }
    ]
  });
  await modelRuntime.setRuntimeApiKey('omlx', input.provider.apiKey);
  const model = modelRuntime.getModel('omlx', input.provider.model.id);
  if (!model) {
    throw new HarnessError('MODEL_UNAVAILABLE', 503, 'Pi could not construct the selected oMLX model.');
  }

  const resourceLoader = await createIsolatedPiResourceLoader(input.cwd, input.systemPrompt);
  const sessionManager = SessionManager.inMemory(input.cwd, { id: input.engineSessionId });
  const settingsManager = SettingsManager.inMemory(
    {
      defaultProvider: 'omlx',
      defaultModel: input.provider.model.id,
      packages: [],
      extensions: [],
      skills: [],
      prompts: [],
      themes: [],
      enableSkillCommands: false
    },
    { projectTrusted: false }
  );
  const customTools = [...input.customTools] as unknown as ToolDefinition[];
  const { session } = await createAgentSession({
    cwd: input.cwd,
    model,
    modelRuntime,
    sessionManager,
    settingsManager,
    resourceLoader,
    noTools: 'all',
    tools: customTools.map((tool) => tool.name),
    customTools
  });

  return {
    sessionId: session.sessionId,
    sessionFile: session.sessionFile,
    subscribe(listener) {
      return session.subscribe((event: AgentSessionEvent) => listener(event as PiAgentSessionEventLike));
    },
    prompt(text, options) {
      return session.prompt(text, options);
    },
    waitForIdle() {
      return session.waitForIdle();
    },
    abort() {
      return session.abort();
    },
    dispose() {
      session.dispose();
    },
    getActiveToolNames() {
      return session.getActiveToolNames();
    }
  };
}

function redactSecret(message: string, secret: string | undefined): string {
  return secret ? message.split(secret).join('[REDACTED]') : message;
}

function classifyThrownError(error: unknown, secret?: string): PiTurnFailure {
  if (error instanceof HarnessError) {
    return {
      errorType: error.type,
      message: redactSecret(error.message, secret),
      status: error.status
    };
  }
  const message = redactSecret(error instanceof Error ? error.message : 'Pi agent turn failed', secret);
  return {
    errorType: 'PROVIDER_PROTOCOL_FAILURE',
    message,
    status: 502
  };
}

async function persistHarnessDraft(
  input: AgentEngineRunInput,
  draft: PiHarnessEventDraft
): Promise<UIEvent | null> {
  const event = createHarnessEvent({
    sessionId: input.session.sessionId,
    turnId: input.turnId,
    type: draft.type,
    data: { turnId: input.turnId, ...draft.data }
  });
  await appendHarnessEvent(event);
  return harnessEventToUiEvent(event);
}

async function persistHarnessEvent(
  input: AgentEngineRunInput,
  type: HarnessEventType,
  data: Record<string, unknown>
): Promise<UIEvent | null> {
  return persistHarnessDraft(input, { kind: 'harness', type, data });
}

export class PiAgentEngineAdapter implements AgentEnginePort {
  readonly subject = 'pi' as const;
  readonly descriptor = {
    adapterId: 'pi',
    providerId: 'omlx',
    packageName: PI_CODING_AGENT_PACKAGE_NAME,
    packageVersion: PI_CODING_AGENT_PACKAGE_VERSION,
    capabilities: {
      credentials: true,
      tools: true,
      attachments: false,
      interruption: true,
      durableResume: false,
      compaction: true,
      runtimeControlTools: true
    }
  } as const;

  private readonly activeTurns = new Map<string, ActivePiTurn>();
  private readonly createSession: (input: PiSessionFactoryInput) => Promise<PiSessionLike>;
  private readonly turnTimeoutMs: number;

  constructor(private readonly dependencies: PiAgentEngineAdapterDependencies) {
    this.createSession = dependencies.createSession ?? createIsolatedPiSession;
    this.turnTimeoutMs = dependencies.turnTimeoutMs ?? 120_000;
  }

  private async resolveCustomTools(input: AgentEngineRunInput): Promise<readonly PiCustomToolDefinition[]> {
    return this.dependencies.resolveCustomTools
      ? this.dependencies.resolveCustomTools(input)
      : (this.dependencies.customTools ?? []);
  }

  private async resolveProvider(input: AgentEngineRunInput): Promise<PiOmlxProviderConfiguration> {
    try {
      return validateProviderConfiguration(input, await this.dependencies.resolveProvider(input));
    } catch (error) {
      throw normalizeProviderResolverError(error);
    }
  }

  async preflight(input: AgentEngineRunInput): Promise<void> {
    validateBoundedChildPosture(input);
    await this.resolveProvider(input);
    selectAuthorizedTools(input, await this.resolveCustomTools(input));
  }

  async prepareContextSuccessor(request: ContextSuccessorRequest): Promise<PreparedContextSuccessor> {
    const preparationId = `context_${randomUUID()}`;
    const continuationText = JSON.stringify({
      predecessorEngineSessionId: request.predecessorEngineSessionId,
      fromBasisId: request.fromBasisId,
      toBasisId: request.toBasisPreview.id,
      priorBasisRefs: request.continuationContext.priorBasisRefs,
      transcript: request.continuationContext.transcript
    });
    return {
      preparationId,
      adapterId: this.descriptor.adapterId,
      providerId: this.descriptor.providerId,
      predecessorEngineSessionId: request.predecessorEngineSessionId,
      continuationText,
      continuationSha256: createHash('sha256').update(continuationText).digest('hex'),
      targetBasisId: request.toBasisPreview.id,
      targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}`
    };
  }

  async cancelContextSuccessor(_preparationId: string): Promise<void> {
    // Preparation is pure and creates no provider state before the next turn.
  }

  async interrupt(sessionId: string): Promise<void> {
    const active = this.activeTurns.get(sessionId);
    if (!active) {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `No active Pi turn for session '${sessionId}'.`);
    }
    active.interrupted = true;
    const event = createHarnessEvent({
      sessionId,
      turnId: active.input.turnId,
      type: 'interruption.requested',
      data: { turnId: active.input.turnId, provider: 'omlx', adapter: 'pi' }
    });
    await appendHarnessEvent(event);
    await active.session?.abort();
  }

  async cancel(sessionId: string): Promise<void> {
    const active = this.activeTurns.get(sessionId);
    if (!active) {
      return;
    }
    active.cancelled = true;
    await active.session?.abort();
  }

  async *startTurn(input: AgentEngineRunInput): AsyncIterable<UIEvent> {
    const active: ActivePiTurn = {
      input,
      interrupted: false,
      cancelled: false
    };
    this.activeTurns.set(input.session.sessionId, active);
    const engineSessionId = input.contextSuccessor === undefined
      ? input.session.engineSessionId ?? `pi_${randomUUID()}`
      : `pi_${randomUUID()}`;
    let provider: PiOmlxProviderConfiguration | undefined;
    let unsubscribe: (() => void) | undefined;
    let timeoutHandle: NodeJS.Timeout | undefined;

    yield {
      type: 'session:init',
      data: {
        engineSessionId,
        adapterId: 'pi',
        providerId: 'omlx',
        model: input.opts.model
      }
    };

    try {
      validateBoundedChildPosture(input);
      const customTools = selectAuthorizedTools(input, await this.resolveCustomTools(input));
      if (active.interrupted || active.cancelled) {
        if (active.interrupted) {
          const completed = await persistHarnessEvent(input, 'interruption.completed', {
            adapter: 'pi',
            provider: 'omlx'
          }).catch(() => null);
          if (completed) {
            yield completed;
          }
        }
        const type: HarnessEventType = active.cancelled ? 'turn.cancelled' : 'turn.interrupted';
        const terminal = await persistHarnessEvent(input, type, {
          adapter: 'pi',
          provider: 'omlx'
        }).catch(() => null);
        if (terminal) {
          yield terminal;
        }
        yield { type: 'process:exit', data: { exitCode: 130, interrupted: true } };
        return;
      }
      if (input.message.trim() === 'bootstrap') {
        yield { type: 'process:exit', data: { exitCode: 0 } };
        return;
      }

      provider = await this.resolveProvider(input);
      const systemPrompt = (await this.dependencies.buildSystemPrompt?.(input)) ?? '';
      const session = await this.createSession({
        cwd: input.session.projectRoot,
        engineSessionId,
        provider,
        systemPrompt,
        customTools
      });
      active.session = session;

      if (session.sessionId !== engineSessionId || session.sessionFile !== undefined) {
        throw new HarnessError(
          'PROVIDER_PROTOCOL_FAILURE',
          502,
          'Pi session isolation failed: expected the supplied in-memory session identity.'
        );
      }
      const activeToolNames = session.getActiveToolNames();
      if (
        activeToolNames.length !== customTools.length ||
        activeToolNames.some((name, index) => name !== customTools[index]?.name)
      ) {
        throw new HarnessError(
          'PROVIDER_PROTOCOL_FAILURE',
          502,
          'Pi session exposed tools outside the Chirality allowlist.'
        );
      }
      if (active.interrupted || active.cancelled) {
        await session.abort();
        if (active.interrupted) {
          const completed = await persistHarnessEvent(input, 'interruption.completed', {
            adapter: 'pi',
            provider: 'omlx'
          }).catch(() => null);
          if (completed) {
            yield completed;
          }
        }
        const type: HarnessEventType = active.cancelled ? 'turn.cancelled' : 'turn.interrupted';
        const terminal = await persistHarnessEvent(input, type, {
          adapter: 'pi',
          provider: 'omlx'
        }).catch(() => null);
        if (terminal) {
          yield terminal;
        }
        yield { type: 'process:exit', data: { exitCode: 130, interrupted: true } };
        return;
      }

      for (const lifecycle of [
        ['turn.accepted', { adapter: 'pi', provider: 'omlx', model: input.opts.model }],
        ['turn.started', { adapter: 'pi', provider: 'omlx', model: input.opts.model }]
      ] as const) {
        const bridged = await persistHarnessEvent(input, lifecycle[0], lifecycle[1]);
        if (bridged) {
          yield bridged;
        }
      }

      const queue = new AsyncEventQueue<PiAgentSessionEventLike>();
      const mapperState = createPiEventMapperState();
      unsubscribe = session.subscribe((event) => queue.push(event));
      const textBlocks = (input.contentBlocks ?? [])
        .filter((block): block is Extract<typeof block, { type: 'text' }> => block.type === 'text')
        .map((block) => block.text)
        .filter(Boolean);
      const prompt = [
        input.contextSuccessor?.continuationText,
        input.contextSuccessor === undefined ? undefined : 'Current user message:',
        input.message,
        ...textBlocks
      ].filter(Boolean).join('\n\n');
      const promptRun = (async () => {
        try {
          await session.prompt(prompt, { expandPromptTemplates: false });
          await session.waitForIdle();
          queue.close();
        } catch (error) {
          queue.fail(error);
        }
      })();
      timeoutHandle = setTimeout(() => {
        queue.fail(
          new HarnessError(
            'PROVIDER_PROTOCOL_FAILURE',
            504,
            'oMLX provider stream timed out.',
            { adapterId: 'pi', providerId: 'omlx', category: 'REQUEST_TIMEOUT' }
          )
        );
        void session.abort().catch(() => undefined);
      }, this.turnTimeoutMs);

      for await (const event of queue) {
        for (const mapped of mapPiSessionEvent(event, mapperState)) {
          if (mapped.kind === 'ui') {
            yield mapped.event;
            continue;
          }
          const bridged = await persistHarnessDraft(input, mapped);
          if (bridged) {
            yield bridged;
          }
        }
      }
      await promptRun;
      clearTimeout(timeoutHandle);
      timeoutHandle = undefined;

      if (active.interrupted || active.cancelled) {
        const interruptedType: HarnessEventType = active.cancelled ? 'turn.cancelled' : 'turn.interrupted';
        if (active.interrupted) {
          const completed = await persistHarnessEvent(input, 'interruption.completed', {
            adapter: 'pi',
            provider: 'omlx'
          });
          if (completed) {
            yield completed;
          }
        }
        const terminal = await persistHarnessEvent(input, interruptedType, {
          adapter: 'pi',
          provider: 'omlx'
        });
        if (terminal) {
          yield terminal;
        }
        yield { type: 'process:exit', data: { exitCode: 130, interrupted: true } };
        return;
      }

      if (mapperState.failure) {
        const failure = mapperState.failure;
        const failed = await persistHarnessEvent(input, 'turn.failed', {
          adapter: 'pi',
          provider: 'omlx',
          errorType: failure.errorType,
          message: redactSecret(failure.message, provider.apiKey)
        });
        if (failed) {
          yield failed;
        }
        yield {
          type: 'turn:error',
          data: {
            phase: 'mid-stream',
            errorType: failure.errorType,
            message: redactSecret(failure.message, provider.apiKey),
            status: failure.status,
            severity: 'error',
            fatal: true
          }
        };
        yield {
          type: 'process:exit',
          data: {
            exitCode: 1,
            error: redactSecret(failure.message, provider.apiKey),
            errorType: failure.errorType,
            status: failure.status,
            severity: 'error',
            fatal: true
          }
        };
        return;
      }

      if (mapperState.lastAssistantText) {
        yield { type: 'chat:complete', data: { text: mapperState.lastAssistantText } };
      }
      const completed = await persistHarnessEvent(input, 'turn.completed', {
        adapter: 'pi',
        provider: 'omlx',
        model: input.opts.model
      });
      if (completed) {
        yield completed;
      }
      yield { type: 'session:complete', data: {} };
      yield { type: 'process:exit', data: { exitCode: 0 } };
    } catch (error) {
      const failure = classifyThrownError(error, provider?.apiKey);
      if (active.interrupted || active.cancelled) {
        const type: HarnessEventType = active.cancelled ? 'turn.cancelled' : 'turn.interrupted';
        const terminal = await persistHarnessEvent(input, type, {
          adapter: 'pi',
          provider: 'omlx'
        }).catch(() => null);
        if (terminal) {
          yield terminal;
        }
        yield { type: 'process:exit', data: { exitCode: 130, interrupted: true } };
        return;
      }
      const failed = await persistHarnessEvent(input, 'turn.failed', {
        adapter: 'pi',
        provider: 'omlx',
        errorType: failure.errorType,
        message: failure.message
      }).catch(() => null);
      if (failed) {
        yield failed;
      }
      yield {
        type: 'turn:error',
        data: {
          phase: 'mid-stream',
          errorType: failure.errorType,
          message: failure.message,
          status: failure.status,
          severity: 'error',
          fatal: true
        }
      };
      yield {
        type: 'process:exit',
        data: {
          exitCode: 1,
          error: failure.message,
          errorType: failure.errorType,
          status: failure.status,
          severity: 'error',
          fatal: true
        }
      };
    } finally {
      if (timeoutHandle) {
        clearTimeout(timeoutHandle);
      }
      unsubscribe?.();
      active.session?.dispose();
      if (this.activeTurns.get(input.session.sessionId) === active) {
        this.activeTurns.delete(input.session.sessionId);
      }
    }
  }
}
