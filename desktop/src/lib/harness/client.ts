import type { SessionSteerRequest, SessionSteerResponse, SessionSteerReceiptRequest } from '@chirality/runtime-contracts';
import type { AgentRosterEntry } from './agent-roster';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type { HarnessReplaySummary } from './session-events';
import type { TranscriptView } from '@chirality/runtime-contracts/transcript-replay';
import type {
  CoordinationMode,
  HarnessErrorResponse,
  InterruptRequest,
  ScaffoldExecutionRootResponse,
  SessionBootRequest,
  SessionBootResponse,
  SessionCreateRequest,
  SessionRecord,
  TurnRequest
} from '@chirality/runtime-contracts/types';
import type {
  ChiralityRoleName,
  ExportNativePlanRequest,
  ExportNativePlanResponse,
  FrozenInstructionBasisV3,
  InstructionHistoryRecordV3,
  MethodInspectionResponse,
  MethodReference,
  MethodsResponse,
  NativePlanCapabilityResponse,
  NativePlanRevisionsResponse,
  ReplaceSelectedMethodsRequest,
  ReplaceSelectedMethodsResponse,
  ResolveSelectedContextRequest,
  ResolveSelectedContextResponse,
  RolesResponse
} from '@chirality/runtime-contracts/v3';
import type {
  ReadableRuntimeSessionRecord,
  ServerRequestAnswer,
  SessionRequestsResponse,
  SessionTurnState
} from '@chirality/runtime-contracts';

export type HarnessReadableSessionRecord = SessionRecord | ReadableRuntimeSessionRecord;

export type SessionEventsReplay = {
  events: HarnessEvent[];
  malformedLineCount: number;
  summary: HarnessReplaySummary;
  session?: HarnessReadableSessionRecord;
  transcript?: TranscriptView;
  instructionHistory: readonly InstructionHistoryRecordV3[];
  instructionBases: readonly FrozenInstructionBasisV3[];
};

type JsonLike = Record<string, unknown>;

export type HarnessTurnStreamEvent = {
  event: string;
  data: unknown;
  /** Runtime turn-registry frame sequence (`id:` line); absent on unnumbered frames. */
  seq?: number;
};

export class HarnessApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = 'HarnessApiClientError';
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

async function readJson<T>(response: Response): Promise<T | undefined> {
  try {
    return (await response.json()) as T;
  } catch {
    return undefined;
  }
}

function fromHarnessErrorPayload(
  status: number,
  payload: HarnessErrorResponse | undefined,
  fallbackMessage: string
): HarnessApiClientError {
  const code = payload?.error?.type ?? 'HARNESS_API_ERROR';
  const message = payload?.error?.message ?? fallbackMessage;
  return new HarnessApiClientError(status, code, message, payload?.error?.details);
}

async function requestHarnessJson<T>(
  input: RequestInfo | URL,
  init: RequestInit,
  fallbackMessage: string
): Promise<T> {
  const response = await fetch(input, init);
  const payload = await readJson<T & HarnessErrorResponse>(response);

  if (!response.ok) {
    throw fromHarnessErrorPayload(response.status, payload, fallbackMessage);
  }

  if (!payload) {
    throw new HarnessApiClientError(
      response.status,
      'INVALID_RESPONSE',
      'Harness API returned an empty response body'
    );
  }

  return payload;
}

export function parseSseFrame(frame: string): HarnessTurnStreamEvent | null {
  const lines = frame.split('\n');
  let event = '';
  let seq: number | undefined;
  const dataLines: string[] = [];

  for (const rawLine of lines) {
    const line = rawLine.endsWith('\r') ? rawLine.slice(0, -1) : rawLine;
    if (line.startsWith(':')) {
      // Comment line (Runtime keepalive); it carries no frame.
      continue;
    }
    if (line.startsWith('event:')) {
      event = line.slice('event:'.length).trim();
      continue;
    }
    if (line.startsWith('id:')) {
      const value = Number(line.slice('id:'.length).trim());
      if (Number.isInteger(value) && value >= 0) seq = value;
      continue;
    }
    if (line.startsWith('data:')) {
      dataLines.push(line.slice('data:'.length).trimStart());
    }
  }

  if (!event || dataLines.length === 0) {
    return null;
  }

  const rawData = dataLines.join('\n');
  const withSeq = (data: unknown): HarnessTurnStreamEvent => (seq === undefined ? { event, data } : { event, data, seq });

  try {
    return withSeq(JSON.parse(rawData) as JsonLike);
  } catch {
    return withSeq(rawData);
  }
}

export type V3TurnRequest = TurnRequest & {
  /** Identity chosen before POST so a lost response can be reconciled safely. */
  turnId?: string;
  interactionMode?: ResolveSelectedContextRequest['interactionMode'];
  permissionMode?: ResolveSelectedContextRequest['permissionMode'];
  methods?: readonly MethodReference[];
  /** Per-turn model override; the session's recorded model otherwise. */
  model?: string;
  /** Per-turn reasoning effort override. */
  reasoningEffort?: string;
};

async function openTurnStream(input: V3TurnRequest, signal?: AbortSignal): Promise<Response> {
  const response = await fetch('/api/harness/turn', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(input),
    ...(signal ? { signal } : {})
  });

  if (response.ok) {
    return response;
  }

  const payload = await readJson<HarnessErrorResponse>(response);
  throw fromHarnessErrorPayload(response.status, payload, 'Unable to start harness turn');
}

async function openAttachStream(sessionId: string, after: number, signal?: AbortSignal, turnId?: string): Promise<Response> {
  const response = await fetch(
    `/api/harness/session/${encodeURIComponent(sessionId)}/turn/stream?after=${Math.max(0, Math.floor(after))}${turnId === undefined ? '' : `&turnId=${encodeURIComponent(turnId)}`}`,
    { method: 'GET', ...(signal ? { signal } : {}) }
  );
  if (response.ok) {
    return response;
  }
  const payload = await readJson<HarnessErrorResponse>(response);
  throw fromHarnessErrorPayload(response.status, payload, 'Unable to attach to the running turn');
}

export function harnessApiErrorMessage(error: unknown): string {
  if (error instanceof HarnessApiClientError) {
    return `${error.code}: ${error.message}`;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'Unexpected harness API failure';
}

/**
 * Fetch the direct-chat persona roster (Type-0/Type-1 only, server-filtered via
 * `?directChat=1`) for the persona picker. D-APP-24 restricts direct chat to
 * conversational personas; Type-2 task agents run only via orchestration.
 */
export async function listDirectChatPersonas(): Promise<AgentRosterEntry[]> {
  const payload = await requestHarnessJson<{ agents: AgentRosterEntry[] }>(
    '/api/harness/agents?directChat=1',
    { method: 'GET' },
    'Unable to load direct-chat personas'
  );

  return payload.agents;
}

export async function listHarnessRoles(projectRoot: string): Promise<RolesResponse> {
  return requestHarnessJson<RolesResponse>(
    `/api/harness/roles?projectRoot=${encodeURIComponent(projectRoot)}`,
    { method: 'GET' },
    'Unable to load roles'
  );
}

export async function listHarnessMethods(input: {
  projectRoot: string;
  kind?: 'skill' | 'workflow';
  query?: string;
}): Promise<MethodsResponse> {
  const params = new URLSearchParams({ projectRoot: input.projectRoot });
  if (input.kind) params.set('kind', input.kind);
  if (input.query?.trim()) params.set('query', input.query.trim());
  return requestHarnessJson<MethodsResponse>(
    `/api/harness/methods?${params.toString()}`,
    { method: 'GET' },
    'Unable to load methods'
  );
}

export async function inspectHarnessMethod(input: {
  projectRoot: string;
  qualifiedId: string;
}): Promise<MethodInspectionResponse> {
  const params = new URLSearchParams({
    projectRoot: input.projectRoot,
    qualifiedId: input.qualifiedId
  });
  return requestHarnessJson<MethodInspectionResponse>(
    `/api/harness/methods/inspect?${params.toString()}`,
    { method: 'GET' },
    'Unable to inspect method'
  );
}

export async function resolveHarnessSelectedContext(input: {
  sessionId: string;
  request: ResolveSelectedContextRequest;
}): Promise<ResolveSelectedContextResponse> {
  return requestHarnessJson<ResolveSelectedContextResponse>(
    `/api/harness/session/${encodeURIComponent(input.sessionId)}/context/resolve`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input.request)
    },
    'Unable to resolve selected context'
  );
}

export async function replaceHarnessSelectedMethods(input: {
  sessionId: string;
  request: ReplaceSelectedMethodsRequest;
}): Promise<ReplaceSelectedMethodsResponse> {
  return requestHarnessJson<ReplaceSelectedMethodsResponse>(
    `/api/harness/session/${encodeURIComponent(input.sessionId)}/methods`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input.request)
    },
    'Unable to replace selected methods'
  );
}

export async function getHarnessNativePlanCapability(
  sessionId: string
): Promise<NativePlanCapabilityResponse> {
  return requestHarnessJson<NativePlanCapabilityResponse>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/capability`,
    { method: 'GET' },
    'Unable to read native Plan capability'
  );
}

export async function listHarnessNativePlanRevisions(
  sessionId: string
): Promise<NativePlanRevisionsResponse> {
  return requestHarnessJson<NativePlanRevisionsResponse>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/revisions`,
    { method: 'GET' },
    'Unable to load native Plan revisions'
  );
}

export async function exportHarnessNativePlan(
  sessionId: string,
  request: ExportNativePlanRequest
): Promise<ExportNativePlanResponse> {
  return requestHarnessJson<ExportNativePlanResponse>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/native-plan/export`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(request) },
    'Failed to export native Plan revision'
  );
}

/**
 * List the harness sessions recorded for a Working Root (most-recent ordering
 * is whatever the server returns). Feeds the Phase 5 session-list UI (D-APP-22).
 */
export async function listHarnessSessions(projectRoot: string): Promise<HarnessReadableSessionRecord[]> {
  const payload = await requestHarnessJson<{ sessions: HarnessReadableSessionRecord[] }>(
    `/api/harness/session/list?projectRoot=${encodeURIComponent(projectRoot)}`,
    { method: 'GET' },
    'Unable to list harness sessions'
  );

  return payload.sessions;
}

/**
 * Replay a session's persisted harness events (D-APP-22 hydrate-on-open). The
 * caller seeds the live buffer with `events`; `malformedLineCount` is surfaced
 * so a corrupt log is reported, not silently dropped.
 */
export async function replaySessionEvents(sessionId: string): Promise<SessionEventsReplay> {
  return requestHarnessJson<SessionEventsReplay>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/events`,
    { method: 'GET' },
    'Unable to load session events'
  );
}

export type HarnessModelSelection = { model: string; reasoningEffort: string };

export async function createHarnessSession(input: SessionCreateRequest & {
  roleId?: ChiralityRoleName;
  interactionMode?: ResolveSelectedContextRequest['interactionMode'];
  permissionMode?: ResolveSelectedContextRequest['permissionMode'];
  selectedMethods?: readonly MethodReference[];
  /** Catalog choice fixed for the session; Runtime rejects (never substitutes) a pair outside the authenticated catalog. */
  modelSelection?: HarnessModelSelection;
}): Promise<SessionRecord> {
  const payload = await requestHarnessJson<{ session: SessionRecord }>(
    '/api/harness/session/create',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to create harness session'
  );

  return payload.session;
}

/** Read only: reconciliation never retries creation or bootstrap. */
export async function getHarnessSession(sessionId: string): Promise<HarnessReadableSessionRecord> {
  const payload = await requestHarnessJson<{ session: HarnessReadableSessionRecord }>(
    `/api/harness/session/${encodeURIComponent(sessionId)}`, { method: 'GET' }, 'Unable to check session initialization'
  );
  return payload.session;
}

export async function bootHarnessSession(input: SessionBootRequest): Promise<SessionBootResponse> {
  return requestHarnessJson<SessionBootResponse>(
    '/api/harness/session/boot',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to boot harness session'
  );
}

export async function decideHarnessPermission(input: {
  sessionId: string;
  toolUseId: string;
  verdict: 'allow' | 'deny';
}): Promise<{ ok: boolean; decided: boolean }> {
  return requestHarnessJson<{ ok: boolean; decided: boolean }>(
    '/api/harness/permission',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to submit permission decision'
  );
}

export async function interruptHarnessSession(input: InterruptRequest): Promise<void> {
  await requestHarnessJson<{ ok: boolean }>(
    '/api/harness/interrupt',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to interrupt harness session'
  );
}

export async function scaffoldHarnessExecutionRoot(input: {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
}): Promise<ScaffoldExecutionRootResponse> {
  return requestHarnessJson<ScaffoldExecutionRootResponse>(
    '/api/harness/scaffold',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input)
    },
    'Unable to scaffold execution root'
  );
}

/** Runtime-owned turn state for a session (D-GOV-43 disconnection rule). */
export async function getHarnessTurnState(sessionId: string, signal?: AbortSignal): Promise<SessionTurnState> {
  return requestHarnessJson<SessionTurnState>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/turn/state`,
    { method: 'GET', ...(signal ? { signal } : {}) },
    'Unable to read the turn state'
  );
}

export async function listHarnessSessionRequests(sessionId: string, signal?: AbortSignal): Promise<SessionRequestsResponse> {
  return requestHarnessJson<SessionRequestsResponse>(
    `/api/harness/session/${encodeURIComponent(sessionId)}/requests`,
    { method: 'GET', ...(signal ? { signal } : {}) },
    'Unable to list pending requests'
  );
}

export async function answerHarnessSessionRequest(input: {
  sessionId: string;
  requestId: string;
  answer: ServerRequestAnswer;
}): Promise<{ sent: true }> {
  return requestHarnessJson<{ sent: true }>(
    `/api/harness/session/${encodeURIComponent(input.sessionId)}/requests/${encodeURIComponent(input.requestId)}/answer`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answer: input.answer })
    },
    'Unable to answer the request'
  );
}

/**
 * Attach to the session's active (or recently finished) Runtime-owned turn,
 * replaying buffered frames after `after`. Resolves when the Runtime closes
 * the subscription; the caller decides from the frames whether the turn ended.
 */
export async function attachHarnessTurn(
  sessionId: string,
  after: number,
  onEvent: (event: HarnessTurnStreamEvent) => void,
  signal?: AbortSignal,
  turnId?: string
): Promise<void> {
  const response = await openAttachStream(sessionId, after, signal, turnId);
  await readTurnStream(response, onEvent, 'Attach response did not include a stream body');
}

export async function streamHarnessTurn(
  input: V3TurnRequest,
  onEvent: (event: HarnessTurnStreamEvent) => void,
  signal?: AbortSignal
): Promise<void> {
  const response = await openTurnStream(input, signal);
  await readTurnStream(response, onEvent, 'Harness turn response did not include a stream body');
}

async function readTurnStream(
  response: Response,
  onEvent: (event: HarnessTurnStreamEvent) => void,
  missingBodyMessage: string
): Promise<void> {
  if (!response.body) {
    throw new HarnessApiClientError(response.status, 'INVALID_RESPONSE', missingBodyMessage);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    if (value) {
      buffer += decoder.decode(value, { stream: true });
    }

    while (true) {
      const boundaryIndex = buffer.indexOf('\n\n');
      if (boundaryIndex < 0) {
        break;
      }

      const frame = buffer.slice(0, boundaryIndex);
      buffer = buffer.slice(boundaryIndex + 2);
      const parsed = parseSseFrame(frame);
      if (parsed) {
        onEvent(parsed);
      }
    }
  }

  buffer += decoder.decode();
  const trailingFrame = buffer.trim();
  if (trailingFrame) {
    const parsed = parseSseFrame(trailingFrame);
    if (parsed) {
      onEvent(parsed);
    }
  }
}

export async function steerHarnessSession(sessionId: string, request: SessionSteerRequest): Promise<SessionSteerResponse> {
  return requestHarnessJson<SessionSteerResponse>(`/api/harness/session/${encodeURIComponent(sessionId)}/turn/steer`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(request)
  }, 'The update receipt could not be confirmed.');
}

/** Receipt lookup cannot submit user input, even when no original intent exists. */
export async function checkHarnessSteeringReceipt(sessionId: string, request: SessionSteerReceiptRequest): Promise<SessionSteerResponse> {
  return requestHarnessJson<SessionSteerResponse>(`/api/harness/session/${encodeURIComponent(sessionId)}/turn/steer/receipt`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(request)
  }, 'Update delivery remains unconfirmed.');
}
