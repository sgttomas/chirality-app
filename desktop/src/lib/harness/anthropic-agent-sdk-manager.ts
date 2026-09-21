import Anthropic from '@anthropic-ai/sdk';
import { createHash, randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { getUiApiKey } from './api-key-store';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { createHarnessEvent } from './event-factory';
import type { HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import { harnessEventToUiEvent } from './harness-ui-bridge';
import { appendHarnessEvent } from './session-events';
import { ContentBlock, IAgentSdkManager, ResolvedOpts, SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';
import type {
  AgentEngineRunInput,
  ContextSuccessorRequest,
  PreparedContextSuccessor
} from '@chirality/runtime-contracts/agent-engine-port';

type ActiveTurnState = {
  interrupted: boolean;
  cancelled: boolean;
  abortController?: AbortController;
};

type AnthropicClientConfig = {
  apiKey: string;
  baseURL: string;
  anthropicVersion: string;
};

type AnthropicClient = {
  messages: {
    create(
      request: Record<string, unknown>,
      options?: { signal?: AbortSignal }
    ): Promise<AsyncIterable<unknown>> | AsyncIterable<unknown>;
  };
};

type AnthropicClientFactory = (config: AnthropicClientConfig) => AnthropicClient;

const DEFAULT_ANTHROPIC_BASE_URL = 'https://api.anthropic.com';
const DEFAULT_ANTHROPIC_VERSION = '2023-06-01';
const DEFAULT_ANTHROPIC_MAX_TOKENS = 1024;
const DEFAULT_STREAM_TIMEOUT_MS = 90_000;
const MAX_INLINE_IMAGE_BYTES = 5 * 1024 * 1024;
const FALLBACK_MODEL = 'haiku';
const ALLOWED_ANTHROPIC_API_HOSTNAMES = new Set<string>(['api.anthropic.com']);
const ALLOWED_ANTHROPIC_API_PROTOCOL = 'https:';
const SUPPORTED_INLINE_IMAGE_MIME_TYPES = new Set<string>([
  'image/png',
  'image/jpeg',
  'image/gif',
  'image/webp'
]);

const PERMISSION_DENY_MARKER = 'UNAPPROVED_DENY_TEST';
const PERMISSION_ALLOW_MARKER = 'UNAPPROVED_ALLOW_TEST';
const BOOT_SDK_FAIL_MODEL_MARKER = '__BOOT_SDK_FAIL__';
const TURN_SDK_FAIL_MARKER = 'TURN_SDK_FAIL_TEST';

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function toLowercasePercentEncoding(value: string): string {
  return value.replace(/%[0-9A-F]{2}/g, (match) => match.toLowerCase());
}

function addEncodedKeyVariantCandidates(variants: Set<string>, encoded: string): Set<string> {
  const nextRoundInputs = new Set<string>();
  if (encoded.length === 0) {
    return nextRoundInputs;
  }

  const lowercaseEncoded = toLowercasePercentEncoding(encoded);
  variants.add(encoded);
  variants.add(lowercaseEncoded);
  nextRoundInputs.add(encoded);
  nextRoundInputs.add(lowercaseEncoded);

  if (encoded.includes('%20')) {
    const queryEncoded = encoded.replace(/%20/g, '+');
    variants.add(queryEncoded);
    nextRoundInputs.add(queryEncoded);
  }
  if (lowercaseEncoded.includes('%20')) {
    const lowercaseQueryEncoded = lowercaseEncoded.replace(/%20/g, '+');
    variants.add(lowercaseQueryEncoded);
    nextRoundInputs.add(lowercaseQueryEncoded);
  }

  return nextRoundInputs;
}

function addUrlEncodedKeyVariants(variants: Set<string>, key: string): void {
  let roundInputs = new Set<string>([key]);
  for (let index = 0; index < 2; index += 1) {
    const nextRoundInputs = new Set<string>();
    for (const roundInput of roundInputs) {
      const encoded = encodeURIComponent(roundInput);
      const candidates = addEncodedKeyVariantCandidates(variants, encoded);
      for (const candidate of candidates) {
        nextRoundInputs.add(candidate);
      }
    }

    if (nextRoundInputs.size === 0) {
      break;
    }
    roundInputs = nextRoundInputs;
  }
}

function readConfiguredApiKeys(): string[] {
  const configuredKeys = [
    getUiApiKey(),
    asNonEmptyString(process.env.ANTHROPIC_API_KEY),
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_KEY)
  ].filter((value): value is string => Boolean(value));
  const variants = new Set<string>();
  for (const key of configuredKeys) {
    variants.add(key);
    addUrlEncodedKeyVariants(variants, key);
  }

  return Array.from(variants).sort((a, b) => b.length - a.length);
}

function redactConfiguredApiKeys(message: string | undefined): string | undefined {
  if (typeof message !== 'string' || message.length === 0) {
    return message;
  }

  const configuredApiKeys = readConfiguredApiKeys();
  if (configuredApiKeys.length === 0) {
    return message;
  }

  const pattern = configuredApiKeys.map(escapeRegExp).join('|');
  return message.replace(new RegExp(pattern, 'g'), '[REDACTED_API_KEY]');
}

function normalizeMimeType(value: string | undefined): string | undefined {
  const normalized = asNonEmptyString(value);
  if (!normalized) {
    return undefined;
  }

  const withoutParameters = normalized.split(';', 1)[0]?.trim().toLowerCase();
  return withoutParameters && withoutParameters.length > 0 ? withoutParameters : undefined;
}

function isValidMimeTypeToken(value: string | undefined): value is string {
  if (!value) {
    return false;
  }

  return /^[a-z0-9!#$&^_.+-]+\/[a-z0-9!#$&^_.+-]+$/.test(value);
}

function isSupportedInlineImageMimeType(value: string): boolean {
  return SUPPORTED_INLINE_IMAGE_MIME_TYPES.has(value);
}

function normalizeAnthropicBaseUrl(raw: string): string {
  const withoutTrailingSlash = raw.replace(/\/+$/, '');
  if (withoutTrailingSlash.endsWith('/v1/messages')) {
    return withoutTrailingSlash.slice(0, -'/v1/messages'.length);
  }
  return withoutTrailingSlash;
}

function validateAnthropicBaseUrl(raw: string): string {
  const normalized = normalizeAnthropicBaseUrl(raw);
  let parsed: URL;

  try {
    parsed = new URL(normalized);
  } catch {
    throw new HarnessError(
      'SDK_FAILURE',
      400,
      'Invalid CHIRALITY_ANTHROPIC_API_URL. Provide an absolute HTTPS Anthropic API URL.',
      {
        provider: 'anthropic',
        category: 'INVALID_BASE_URL'
      }
    );
  }

  const hostname = parsed.hostname.toLowerCase();
  if (parsed.protocol !== ALLOWED_ANTHROPIC_API_PROTOCOL) {
    throw new HarnessError(
      'SDK_FAILURE',
      400,
      `Outbound policy violation: Anthropic base URL must use ${ALLOWED_ANTHROPIC_API_PROTOCOL}.`,
      {
        provider: 'anthropic',
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        protocol: parsed.protocol
      }
    );
  }

  if (!ALLOWED_ANTHROPIC_API_HOSTNAMES.has(hostname)) {
    throw new HarnessError(
      'SDK_FAILURE',
      400,
      `Outbound policy violation: host '${hostname}' is not in the Anthropic allowlist.`,
      {
        provider: 'anthropic',
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        host: hostname,
        allowlist: Array.from(ALLOWED_ANTHROPIC_API_HOSTNAMES)
      }
    );
  }

  if (parsed.username || parsed.password) {
    throw new HarnessError(
      'SDK_FAILURE',
      400,
      'Outbound policy violation: Anthropic base URL must not include credentials.',
      {
        provider: 'anthropic',
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001'
      }
    );
  }

  if (parsed.port && parsed.port !== '443') {
    throw new HarnessError(
      'SDK_FAILURE',
      400,
      `Outbound policy violation: Anthropic base URL port '${parsed.port}' is not allowed.`,
      {
        provider: 'anthropic',
        category: 'NETWORK_POLICY_VIOLATION',
        policy: 'REQ-NET-001',
        port: parsed.port
      }
    );
  }

  return parsed.origin;
}

function getAnthropicBaseUrl(): string {
  const raw = asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_URL);
  const candidate = raw ?? DEFAULT_ANTHROPIC_BASE_URL;
  return validateAnthropicBaseUrl(candidate);
}

function readAnthropicApiKey(): string {
  // ENV+UI precedence (OI-001 / SCA-003): UI-provided key takes precedence,
  // then ANTHROPIC_API_KEY env var, then CHIRALITY_ANTHROPIC_API_KEY env var.
  const key =
    getUiApiKey() ??
    asNonEmptyString(process.env.ANTHROPIC_API_KEY) ??
    asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_API_KEY);
  if (!key) {
    throw new HarnessError(
      'SDK_FAILURE',
      503,
      'Anthropic API key is not configured. Enter a key in Settings or set ANTHROPIC_API_KEY.',
      {
        provider: 'anthropic',
        category: 'MISSING_API_KEY'
      }
    );
  }
  return key;
}

function getAnthropicVersion(): string {
  return asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_VERSION) ?? DEFAULT_ANTHROPIC_VERSION;
}

function getMaxTokens(): number {
  const raw = asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_MAX_TOKENS);
  if (!raw) {
    return DEFAULT_ANTHROPIC_MAX_TOKENS;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return DEFAULT_ANTHROPIC_MAX_TOKENS;
  }
  return parsed;
}

function getStreamTimeoutMs(): number {
  const raw = asNonEmptyString(process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS);
  if (!raw) {
    return DEFAULT_STREAM_TIMEOUT_MS;
  }

  const parsed = Number.parseInt(raw, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return DEFAULT_STREAM_TIMEOUT_MS;
  }
  return parsed;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function buildAnthropicClient(config: AnthropicClientConfig): AnthropicClient {
  const options = {
    apiKey: config.apiKey,
    baseURL: config.baseURL,
    defaultHeaders: {
      'anthropic-version': config.anthropicVersion
    }
  } as ConstructorParameters<typeof Anthropic>[0];

  return new Anthropic(options) as unknown as AnthropicClient;
}

function detectMimeType(filePath: string, fallbackMimeType: string): string {
  const normalizedFallbackMimeType = normalizeMimeType(fallbackMimeType);
  const parsedFallbackMimeType = isValidMimeTypeToken(normalizedFallbackMimeType)
    ? normalizedFallbackMimeType
    : undefined;
  const authoritativeFallbackMimeType =
    parsedFallbackMimeType?.startsWith('image/') &&
    !isSupportedInlineImageMimeType(parsedFallbackMimeType)
      ? undefined
      : parsedFallbackMimeType;

  if (
    authoritativeFallbackMimeType &&
    authoritativeFallbackMimeType !== 'application/octet-stream'
  ) {
    return authoritativeFallbackMimeType;
  }

  const extension = path.extname(filePath).toLowerCase();
  switch (extension) {
    case '.png':
      return 'image/png';
    case '.jpg':
    case '.jpeg':
      return 'image/jpeg';
    case '.gif':
      return 'image/gif';
    case '.webp':
      return 'image/webp';
    default:
      return authoritativeFallbackMimeType || 'application/octet-stream';
  }
}

async function readImageAsBase64(filePath: string): Promise<string> {
  let bytes: Buffer;
  try {
    bytes = await readFile(filePath);
  } catch {
    throw new HarnessError('ATTACHMENT_FAILURE', 400, `Attachment '${filePath}' is not readable`, {
      path: filePath
    });
  }

  if (bytes.byteLength > MAX_INLINE_IMAGE_BYTES) {
    throw new HarnessError(
      'ATTACHMENT_FAILURE',
      400,
      `Attachment '${filePath}' exceeds ${MAX_INLINE_IMAGE_BYTES} byte inline image limit`,
      {
        path: filePath,
        byteLength: bytes.byteLength,
        limit: MAX_INLINE_IMAGE_BYTES
      }
    );
  }

  return bytes.toString('base64');
}

async function readPDFAsBase64(filePath: string): Promise<string> {
  let bytes: Buffer;
  try {
    bytes = await readFile(filePath);
  } catch {
    throw new HarnessError('ATTACHMENT_FAILURE', 400, `Attachment '${filePath}' is not readable`, {
      path: filePath
    });
  }

  return bytes.toString('base64');
}

async function readPlainTextDocument(filePath: string): Promise<string> {
  try {
    return await readFile(filePath, 'utf8');
  } catch {
    throw new HarnessError('ATTACHMENT_FAILURE', 400, `Attachment '${filePath}' is not readable`, {
      path: filePath
    });
  }
}

async function formatContentBlocks(
  message: string,
  contentBlocks: ContentBlock[] | undefined
): Promise<Array<Record<string, unknown>>> {
  const blocks: ContentBlock[] =
    (contentBlocks ?? []).length > 0 ? contentBlocks ?? [] : [{ type: 'text', text: message }];
  const anthropicContent: Array<Record<string, unknown>> = [];

  for (const block of blocks) {
    if (block.type === 'text') {
      anthropicContent.push({
        type: 'text',
        text: block.text
      });
      continue;
    }

    const mimeType = detectMimeType(block.path, block.mimeType);
    if (mimeType.startsWith('image/')) {
      anthropicContent.push({
        type: 'image',
        source: {
          type: 'base64',
          media_type: mimeType,
          data: await readImageAsBase64(block.path)
        }
      });
      continue;
    }

    if (mimeType === 'application/pdf') {
      anthropicContent.push({
        type: 'document',
        title: path.basename(block.path),
        source: {
          type: 'base64',
          media_type: 'application/pdf',
          data: await readPDFAsBase64(block.path)
        }
      });
      continue;
    }

    if (mimeType.startsWith('text/')) {
      anthropicContent.push({
        type: 'document',
        title: path.basename(block.path),
        source: {
          type: 'text',
          media_type: 'text/plain',
          data: await readPlainTextDocument(block.path)
        }
      });
      continue;
    }

    anthropicContent.push({
      type: 'text',
      text: `Attachment '${path.basename(block.path)}' is available locally but not yet mapped to Anthropic multimodal request types.`
    });
  }

  return anthropicContent;
}

function readEventType(event: unknown): string | undefined {
  if (!isRecord(event)) {
    return undefined;
  }
  return typeof event.type === 'string' ? event.type : undefined;
}

function readMessageStop(event: unknown): boolean {
  return readEventType(event) === 'message_stop';
}

function readTextDelta(event: unknown): string | undefined {
  if (!isRecord(event)) {
    return undefined;
  }

  const delta = event.delta;
  if (isRecord(delta) && typeof delta.text === 'string' && delta.text.length > 0) {
    return delta.text;
  }

  const contentBlock = event.content_block;
  if (isRecord(contentBlock) && typeof contentBlock.text === 'string' && contentBlock.text.length > 0) {
    return contentBlock.text;
  }

  if (typeof event.text === 'string' && event.text.length > 0) {
    return event.text;
  }

  return undefined;
}

function toAnthropicStreamEventError(event: unknown): HarnessError {
  if (isRecord(event) && isRecord(event.error) && typeof event.error.message === 'string') {
    const status = typeof event.error.status === 'number' ? event.error.status : 502;
    const sanitizedMessage = redactConfiguredApiKeys(event.error.message);
    return new HarnessError('SDK_FAILURE', status, sanitizedMessage ?? 'Anthropic stream returned an error event', {
      provider: 'anthropic',
      category: 'API_RESPONSE_ERROR',
      upstreamType: typeof event.error.type === 'string' ? event.error.type : undefined
    });
  }

  return new HarnessError('SDK_FAILURE', 502, 'Anthropic stream returned an error event', {
    provider: 'anthropic',
    category: 'API_RESPONSE_ERROR'
  });
}

function classifyHttpError(
  status: number
): { message: string; category: string } {
  if (status === 401 || status === 403) {
    return {
      message: 'Anthropic authentication failed. Re-provision ANTHROPIC_API_KEY.',
      category: 'INVALID_API_KEY'
    };
  }

  if (status === 429) {
    return {
      message: 'Anthropic rate limit reached. Retry after backoff.',
      category: 'RATE_LIMITED'
    };
  }

  if (status >= 500) {
    return {
      message: 'Anthropic API server error.',
      category: 'API_RESPONSE_ERROR'
    };
  }

  return {
    message: `Anthropic request failed with status ${status}.`,
    category: 'API_RESPONSE_ERROR'
  };
}

function readErrorDetails(error: unknown): {
  status?: number;
  message?: string;
  upstreamType?: string;
  name?: string;
} {
  if (!isRecord(error)) {
    return {};
  }

  const status =
    typeof error.status === 'number'
      ? error.status
      : typeof error.statusCode === 'number'
        ? error.statusCode
        : undefined;

  const upstreamType =
    typeof error.type === 'string'
      ? error.type
      : isRecord(error.error) && typeof error.error.type === 'string'
        ? error.error.type
        : undefined;

  const message =
    typeof error.message === 'string'
      ? error.message
      : isRecord(error.error) && typeof error.error.message === 'string'
        ? error.error.message
        : undefined;

  const name = typeof error.name === 'string' ? error.name : undefined;

  return {
    status,
    message,
    upstreamType,
    name
  };
}

function toAnthropicSdkError(error: unknown): HarnessError | undefined {
  const { status, message, upstreamType, name } = readErrorDetails(error);
  const sanitizedMessage = redactConfiguredApiKeys(message);

  if (typeof status === 'number') {
    const classification = classifyHttpError(status);
    return new HarnessError('SDK_FAILURE', status, sanitizedMessage ?? classification.message, {
      provider: 'anthropic',
      category: classification.category,
      upstreamType
    });
  }

  if (name === 'AuthenticationError') {
    return new HarnessError(
      'SDK_FAILURE',
      401,
      sanitizedMessage ?? 'Anthropic authentication failed. Re-provision ANTHROPIC_API_KEY.',
      {
        provider: 'anthropic',
        category: 'INVALID_API_KEY',
        upstreamType
      }
    );
  }

  if (name === 'RateLimitError') {
    return new HarnessError(
      'SDK_FAILURE',
      429,
      sanitizedMessage ?? 'Anthropic rate limit reached. Retry after backoff.',
      {
        provider: 'anthropic',
        category: 'RATE_LIMITED',
        upstreamType
      }
    );
  }

  return undefined;
}

function isAbortError(error: unknown): boolean {
  if (error instanceof Error) {
    return error.name === 'AbortError';
  }
  if (isRecord(error) && typeof error.name === 'string') {
    return error.name === 'AbortError';
  }
  return false;
}

function toNetworkError(error: unknown): HarnessError | undefined {
  if (isAbortError(error)) {
    return undefined;
  }

  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 503, 'Unable to reach Anthropic API endpoint.', {
      provider: 'anthropic',
      category: 'NETWORK_ERROR',
      cause: redactConfiguredApiKeys(error.message)
    });
  }

  if (isRecord(error) && typeof error.message === 'string') {
    return new HarnessError('SDK_FAILURE', 503, 'Unable to reach Anthropic API endpoint.', {
      provider: 'anthropic',
      category: 'NETWORK_ERROR',
      cause: redactConfiguredApiKeys(error.message)
    });
  }

  return undefined;
}

export class AnthropicAgentSdkManager implements IAgentSdkManager {
  private readonly activeTurns = new Map<string, ActiveTurnState>();

  constructor(private readonly clientFactory: AnthropicClientFactory = buildAnthropicClient) {}

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
      adapterId: 'anthropic-direct',
      providerId: 'anthropic',
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

  startRuntimeTurn(input: AgentEngineRunInput): AsyncIterable<UIEvent> {
    if (input.message.trim() === 'bootstrap') {
      return this.startTurn(
        input.session,
        input.message,
        input.opts,
        input.contentBlocks,
        input.turnId
      );
    }
    if ((input.runtimeTools?.length ?? 0) > 0) {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        422,
        'anthropic-direct cannot expose Runtime method tools; select a tool-capable adapter.'
      );
    }
    const systemPrompt = input.instructionContext?.supplied.map((entry) => [
      `## ${entry.kind}: ${entry.id}`,
      `contentSha256: ${entry.sha256}`,
      entry.content
    ].join('\n')).join('\n\n---\n\n');
    if ('instructionBasisId' in input.session && systemPrompt === undefined) {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Runtime did not supply the frozen instruction basis for this session.'
      );
    }
    const runtimeSession = input.contextSuccessor === undefined ? input.session : {
      ...input.session,
      engineSessionId: undefined,
      claudeSessionId: undefined,
      sdkSessionId: undefined,
      adapterSession: undefined
    };
    return this.startTurn(
      runtimeSession,
      input.message,
      input.opts,
      input.contentBlocks,
      input.turnId,
      systemPrompt,
      input.contextSuccessor?.continuationText
    );
  }

  // D-APP-25 Anthropic-manager parity: persist and bridge a manager-level
  // lifecycle event through the same provider-neutral path as the Claude SDK
  // manager. The bridge (harnessEventToUiEvent) redacts configured API keys, so
  // no new leak path is introduced.
  private async *emitLifecycle(
    sessionId: string,
    type: HarnessEventType,
    data: Record<string, unknown> = {}
  ): AsyncGenerator<UIEvent> {
    const turnId = typeof data.turnId === 'string' ? data.turnId : undefined;
    const event = createHarnessEvent({
      sessionId,
      turnId,
      type,
      data: { provider: 'anthropic', ...data }
    });
    await appendHarnessEvent(event);
    const bridged = harnessEventToUiEvent(event);
    if (bridged) {
      yield bridged;
    }
  }

  async interrupt(sessionId: string): Promise<void> {
    const activeTurn = this.activeTurns.get(sessionId);
    if (!activeTurn) {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `No active turn for session '${sessionId}'`, {
        sessionId
      });
    }

    // Persisted-only, mirroring the Claude SDK manager: interruption.requested
    // originates from the operator's own interrupt action (out-of-band from the
    // turn stream), so it is recorded for replay but not bridged live.
    await appendHarnessEvent(
      createHarnessEvent({
        sessionId,
        type: 'interruption.requested',
        data: { provider: 'anthropic' }
      })
    );
    activeTurn.interrupted = true;
    activeTurn.abortController?.abort();
  }

  async cancel(sessionId: string): Promise<void> {
    const activeTurn = this.activeTurns.get(sessionId);
    if (!activeTurn) {
      return;
    }

    activeTurn.cancelled = true;
    activeTurn.abortController?.abort();
  }

  async *startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts,
    contentBlocks?: ContentBlock[],
    suppliedTurnId?: string,
    systemPrompt?: string,
    continuationText?: string
  ): AsyncIterable<UIEvent> {
    const turnState: ActiveTurnState = { interrupted: false, cancelled: false };
    this.activeTurns.set(session.sessionId, turnState);
    const turnId = suppliedTurnId ?? `turn_${randomUUID()}`;

    let timeoutHandle: NodeJS.Timeout | undefined;
    let timedOut = false;
    // Tracks whether turn.accepted was emitted, so the catch/interrupt teardown
    // only closes a lifecycle that was actually opened (bootstrap turns stay
    // lifecycle-free, mirroring the Claude SDK manager).
    let lifecycleOpened = false;

    const claudeSessionId = session.engineSessionId ?? session.claudeSessionId ?? `claude_${randomUUID()}`;
    const trimmedMessage = message.trim();

    try {
      yield {
        type: 'session:init',
        data: {
          engineSessionId: claudeSessionId,
          adapterId: 'anthropic-direct',
          providerId: 'anthropic',
          claudeSessionId,
          model: opts.model || FALLBACK_MODEL
        }
      };

      if (trimmedMessage === 'bootstrap' && opts.model === BOOT_SDK_FAIL_MODEL_MARKER) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 1
          }
        };
        return;
      }

      const isBootstrap = trimmedMessage === 'bootstrap';
      if (!isBootstrap) {
        // Open the turn timeline (accepted -> started -> completed/cancelled/failed)
        // for real turns. session:init is already the first public UIEvent.
        yield* this.emitLifecycle(session.sessionId, 'turn.accepted', {
          turnId,
          model: opts.model || FALLBACK_MODEL,
          persona: opts.persona,
          mode: opts.mode
        });
        lifecycleOpened = true;
      }

      if (trimmedMessage.includes(TURN_SDK_FAIL_MARKER)) {
        throw new HarnessError('SDK_FAILURE', 500, 'Turn failed before completion', {
          marker: TURN_SDK_FAIL_MARKER
        });
      }

      if (opts.mode === 'dontAsk' && trimmedMessage.includes(PERMISSION_DENY_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: false,
            output: 'permission denied'
          }
        };
        yield* this.emitLifecycle(session.sessionId, 'turn.completed', {
          turnId,
          stopReason: 'permission_denied'
        });
        yield {
          type: 'chat:complete',
          data: {
            text: 'Denied: unapproved Bash command under dontAsk.'
          }
        };
        yield {
          type: 'session:complete',
          data: {}
        };
        yield {
          type: 'process:exit',
          data: {
            exitCode: 0
          }
        };
        return;
      }

      if (opts.mode === 'dontAsk' && trimmedMessage.includes(PERMISSION_ALLOW_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: true,
            output: PERMISSION_ALLOW_MARKER
          }
        };
      }

      const apiKey = readAnthropicApiKey();

      if (isBootstrap) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 0
          }
        };
        return;
      }

      const resolvedContent = await formatContentBlocks(
        continuationText === undefined
          ? message
          : `${continuationText}\n\nCurrent user message:\n${message}`,
        contentBlocks
      );
      const abortController = new AbortController();
      turnState.abortController = abortController;
      timeoutHandle = setTimeout(() => {
        timedOut = true;
        abortController.abort();
      }, getStreamTimeoutMs());

      const client = this.clientFactory({
        apiKey,
        baseURL: getAnthropicBaseUrl(),
        anthropicVersion: getAnthropicVersion()
      });

      const stream = await client.messages.create(
        {
          model: opts.model || FALLBACK_MODEL,
          stream: true,
          max_tokens: getMaxTokens(),
          ...(systemPrompt === undefined ? {} : { system: systemPrompt }),
          messages: [
            {
              role: 'user',
              content: resolvedContent
            }
          ]
        },
        {
          signal: abortController.signal
        }
      );

      yield* this.emitLifecycle(session.sessionId, 'turn.started', { turnId });

      let fullText = '';

      for await (const event of stream) {
        if (turnState.cancelled) {
          yield {
            type: 'process:exit',
            data: { exitCode: 130, interrupted: false }
          };
          return;
        }

        if (turnState.interrupted) {
          yield* this.emitLifecycle(session.sessionId, 'interruption.completed', { turnId });
          yield* this.emitLifecycle(session.sessionId, 'turn.interrupted', { turnId });
          yield {
            type: 'process:exit',
            data: {
              exitCode: 130,
              interrupted: true
            }
          };
          return;
        }

        if (readEventType(event) === 'error') {
          throw toAnthropicStreamEventError(event);
        }

        const delta = readTextDelta(event);
        if (delta) {
          fullText += delta;
          yield {
            type: 'chat:delta',
            data: {
              text: delta
            }
          };
        }

        if (readMessageStop(event)) {
          break;
        }
      }

      yield* this.emitLifecycle(session.sessionId, 'turn.completed', {
        turnId,
        stopReason: 'end_turn',
        textLength: fullText.length
      });
      yield {
        type: 'chat:complete',
        data: {
          text: fullText
        }
      };
      yield {
        type: 'session:complete',
        data: {}
      };
      yield {
        type: 'process:exit',
        data: {
          exitCode: 0
        }
      };
    } catch (error) {
      if (turnState.cancelled) {
        yield {
          type: 'process:exit',
          data: { exitCode: 130, interrupted: false }
        };
        return;
      }

      if (turnState.interrupted) {
        if (lifecycleOpened) {
          yield* this.emitLifecycle(session.sessionId, 'interruption.completed', { turnId });
          yield* this.emitLifecycle(session.sessionId, 'turn.interrupted', { turnId });
        }
        yield {
          type: 'process:exit',
          data: {
            exitCode: 130,
            interrupted: true
          }
        };
        return;
      }

      // Resolve the throwable using the existing precedence (timeout, typed
      // HarnessError, classified SDK/network error, raw), then bridge a
      // redacted turn.failed before re-throwing so the loop sees the failure
      // in the turn timeline.
      let failure: unknown;
      if (timedOut) {
        failure = new HarnessError('SDK_FAILURE', 504, 'Anthropic request timed out', {
          provider: 'anthropic',
          category: 'REQUEST_TIMEOUT'
        });
      } else if (error instanceof HarnessError) {
        failure = error;
      } else {
        failure = toAnthropicSdkError(error) ?? toNetworkError(error) ?? error;
      }

      if (lifecycleOpened) {
        const failureMessage = failure instanceof Error ? failure.message : 'Anthropic turn failed';
        yield* this.emitLifecycle(session.sessionId, 'turn.failed', {
          turnId,
          error: redactConfiguredApiKeys(failureMessage) ?? failureMessage
        });
      }

      throw failure;
    } finally {
      if (timeoutHandle) {
        clearTimeout(timeoutHandle);
      }
      // Identity-guarded teardown (parity with the Claude SDK manager, DESIGN
      // §5.3): only retire THIS turn's state. If the turn lock was released early
      // and a newer same-session turn already installed fresh state, this stale
      // teardown must not clobber it.
      if (this.activeTurns.get(session.sessionId) === turnState) {
        this.activeTurns.delete(session.sessionId);
      }
    }
  }
}
