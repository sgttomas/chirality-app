import type { SessionSteerReceiptRequest, SessionSteerRequest, SessionSteerResponse } from '@chirality/runtime-contracts';
import { relative, resolve } from 'node:path';

import { HarnessError } from '@chirality/runtime-contracts/errors';
import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import type {
  InterruptRequest,
  ScaffoldExecutionRootRequest,
  ScaffoldExecutionRootResponse,
  SessionBootRequest,
  SessionBootResponse,
  SessionCreateRequest,
  SessionRecord,
  TurnRequest,
  UIEvent
} from '@chirality/runtime-contracts/types';
import type { TranscriptView } from '@chirality/runtime-contracts/transcript-replay';
import type {
  ChiralityRoleName,
  ExportNativePlanRequest,
  ExportNativePlanResponse,
  FrozenInstructionBasisV3,
  InstructionHistoryRecordV3,
  MethodInspectionResponse,
  MethodsResponse,
  NativePlanCapabilityResponse,
  NativePlanClarificationsResponse,
  NativePlanRevisionsResponse,
  ReplyNativePlanClarificationRequest,
  ReplyNativePlanClarificationResponse,
  ReplaceSelectedMethodsRequest,
  ReplaceSelectedMethodsResponse,
  ResolveSelectedContextRequest,
  ResolveSelectedContextResponse,
  RolesResponse
} from '@chirality/runtime-contracts/v3';
import type {
  AnswerSessionRequestResponse,
  ReadableRuntimeSessionRecord,
  ServerRequestAnswer,
  SessionRequestsResponse,
  SessionTurnState
} from '@chirality/runtime-contracts';
import type {
  HostedBootstrapLoginStartResponse,
  HostedBootstrapStatus
} from '@chirality/runtime-contracts';
import {
  createRuntimeDaemonHarnessPortFromEnvironment,
  createRuntimeHostedBootstrapPortFromEnvironment
} from './runtime-daemon-harness-port';

export type AgentRosterEntry = {
  name: string;
  type: number | undefined;
  class: string | undefined;
};

export type PermissionDecisionRequest = {
  sessionId: string;
  toolUseId: string;
  verdict: 'allow' | 'deny';
};

export type HarnessReplayResponse = {
  events: HarnessEvent[];
  malformedLineCount: number;
  summary: {
    eventCount: number;
    malformedLineCount: number;
    eventTypeCounts: Record<string, number>;
    firstTimestamp?: string;
    lastTimestamp?: string;
  };
  session: SessionRecord | ReadableRuntimeSessionRecord;
  transcript: TranscriptView;
  instructionHistory: readonly InstructionHistoryRecordV3[];
  instructionBases: readonly FrozenInstructionBasisV3[];
};

/**
 * One frame of a Runtime-owned turn stream. `seq` is the Runtime turn
 * registry's frame sequence (D-GOV-43 section 5); it is absent only on frames
 * produced by a Runtime that does not number its frames yet.
 */
export type DaemonTurnFrame = UIEvent & { seq?: number };

/**
 * A subscription to a turn the Runtime owns. `cancel()` only unsubscribes the
 * observer; it never interrupts the turn (the interrupt route does that).
 */
export type RunningDaemonHarnessTurn = {
  events: AsyncIterable<DaemonTurnFrame>;
  cancel(): Promise<void>;
};

export type { SessionTurnState, SessionRequestsResponse, ServerRequestAnswer };

export type DaemonRequestOptions = {
  signal?: AbortSignal;
};

export type HostedProjectBindingResponse =
  | { registration: 'required' }
  | { registration: 'registered'; projectId: string };

/**
 * Registration plus the Runtime's hosted account status. Under D-GOV-43 the
 * Runtime is App-owned and there is no account-host admission proof, so the
 * App tier reads status directly over the Runtime socket; the renderer no
 * longer needs a separate main-process IPC path for it.
 */
export type HostedBootstrapStatusResponse =
  | { registration: 'required' }
  | { registration: 'registered'; projectId: string; status: HostedBootstrapStatus };

/**
 * Explicit initialization returns only the verified registration and binding;
 * the caller reads status afterwards through {@link HostedBootstrapPort.getStatus}.
 */
export type HostedProjectInitializationResponse = Extract<
  HostedProjectBindingResponse,
  { registration: 'registered' }
>;

export interface HostedBootstrapPort {
  /** Server-only recovery of an authoritative session owner after restart. */
  resolveSessionPort?(sessionId: string, options?: DaemonRequestOptions): Promise<DaemonHarnessPort>;
  bindProject(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedProjectBindingResponse>;
  /**
   * Resolves and verifies the binding for the selected folder and, when the
   * folder is registered, reads the hosted account status from the Runtime.
   */
  getStatus(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapStatusResponse>;
  initializeProject(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedProjectInitializationResponse>;
  /**
   * Retained for wire compatibility only. Under D-GOV-43 no provider-network
   * consent step exists; the port reports the current status without changing it.
   */
  grantProviderNetworkConsent(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapStatus>;
  startLogin(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapLoginStartResponse>;
  cancelLogin(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapStatus>;
  signOut(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapStatus>;
}

export type DaemonProjectBinding = {
  projectId: string;
  projectRoot: string;
};

export type V3SessionCreateRequest = SessionCreateRequest & {
  roleId?: ChiralityRoleName;
  interactionMode?: ResolveSelectedContextRequest['interactionMode'];
  permissionMode?: ResolveSelectedContextRequest['permissionMode'];
  selectedMethods?: ResolveSelectedContextRequest['methods'];
  declaredContext?: string[];
  allowedWriteTargets?: string[];
  /** Session-fixed catalog choice; forwarded to Runtime `CreateSessionRequest.modelSelection`. */
  modelSelection?: { model: string; reasoningEffort: string };
};

export type V3TurnRequest = TurnRequest & {
  /** Identity chosen before POST so a lost response can be reconciled safely. */
  turnId?: string;
  interactionMode?: ResolveSelectedContextRequest['interactionMode'];
  permissionMode?: ResolveSelectedContextRequest['permissionMode'];
  methods?: ResolveSelectedContextRequest['methods'];
  /** Per-turn model override (Codex `turn/start.model`); the session default otherwise. */
  model?: string;
  /** Per-turn reasoning effort override (Codex `turn/start.effort`). */
  reasoningEffort?: string;
};

/**
 * Compatibility boundary between the existing Desktop renderer API and the
 * shared runtime daemon.
 *
 * The concrete runtime-client binder is responsible for resolving a
 * registered projectRoot to a projectId, resolving session ownership, mapping
 * canonical daemon events to the existing UI event names, and authenticating
 * over the Unix socket. Route handlers intentionally know none of those
 * details and have no in-process runtime fallback.
 */
export interface DaemonHarnessPort {
  createSession(
    request: V3SessionCreateRequest,
    options?: DaemonRequestOptions
  ): Promise<{ session: SessionRecord | ReadableRuntimeSessionRecord }>;
  listSessions(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<{ sessions: Array<SessionRecord | ReadableRuntimeSessionRecord> }>;
  getSession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<{ session: SessionRecord | ReadableRuntimeSessionRecord }>;
  deleteSession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<{ ok: true }>;
  bootSession(
    request: SessionBootRequest,
    options?: DaemonRequestOptions
  ): Promise<SessionBootResponse>;
  replaySession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<HarnessReplayResponse>;
  turn(
    request: V3TurnRequest,
    options?: DaemonRequestOptions
  ): Promise<RunningDaemonHarnessTurn>;
  /**
   * Attach to the active (or recently finished) turn of a session, replaying
   * buffered frames with `seq > after` first. Closing the subscription never
   * affects the turn.
   */
  attachTurn(
    sessionId: string,
    after: number,
    options?: DaemonRequestOptions & { turnId?: string }
  ): Promise<RunningDaemonHarnessTurn>;
  turnState(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<SessionTurnState>;
  listRequests(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<SessionRequestsResponse>;
  answerRequest(
    sessionId: string,
    requestId: string,
    answer: ServerRequestAnswer,
    options?: DaemonRequestOptions
  ): Promise<AnswerSessionRequestResponse>;
  steer(sessionId: string, request: SessionSteerRequest, options?: DaemonRequestOptions): Promise<SessionSteerResponse>;
  steerReceipt(sessionId: string, request: SessionSteerReceiptRequest, options?: DaemonRequestOptions): Promise<SessionSteerResponse>;
  interrupt(
    request: InterruptRequest,
    options?: DaemonRequestOptions
  ): Promise<{ ok: true }>;
  decidePermission(
    request: PermissionDecisionRequest,
    options?: DaemonRequestOptions
  ): Promise<{ ok: true; decided: boolean }>;
  listAgents(
    request: { directChatOnly: boolean },
    options?: DaemonRequestOptions
  ): Promise<{ agents: AgentRosterEntry[] }>;
  listRoles(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<RolesResponse>;
  listMethods(
    request: { projectRoot: string; kind?: 'skill' | 'workflow'; query?: string },
    options?: DaemonRequestOptions
  ): Promise<MethodsResponse>;
  inspectMethod(
    request: { projectRoot: string; qualifiedId: string },
    options?: DaemonRequestOptions
  ): Promise<MethodInspectionResponse>;
  resolveSelectedContext(
    sessionId: string,
    request: ResolveSelectedContextRequest,
    options?: DaemonRequestOptions
  ): Promise<ResolveSelectedContextResponse>;
  replaceSelectedMethods(
    sessionId: string,
    request: ReplaceSelectedMethodsRequest,
    options?: DaemonRequestOptions
  ): Promise<ReplaceSelectedMethodsResponse>;
  getNativePlanCapability(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<NativePlanCapabilityResponse>;
  listNativePlanRevisions(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<NativePlanRevisionsResponse>;
  listNativePlanClarifications(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<NativePlanClarificationsResponse>;
  replyNativePlanClarification(
    sessionId: string,
    requestId: string | number,
    answers: ReplyNativePlanClarificationRequest['answers'],
    options?: DaemonRequestOptions
  ): Promise<ReplyNativePlanClarificationResponse>;
  exportNativePlan(
    sessionId: string,
    request: ExportNativePlanRequest,
    options?: DaemonRequestOptions
  ): Promise<ExportNativePlanResponse>;
  scaffold(
    request: ScaffoldExecutionRootRequest,
    options?: DaemonRequestOptions
  ): Promise<ScaffoldExecutionRootResponse>;
}

function daemonClientUnavailable(): never {
  throw new HarnessError(
    'ENGINE_UNAVAILABLE',
    503,
    'Chirality runtime daemon client is not configured'
  );
}

const unboundDaemonHarnessPort: DaemonHarnessPort = {
  createSession: daemonClientUnavailable,
  listSessions: daemonClientUnavailable,
  getSession: daemonClientUnavailable,
  deleteSession: daemonClientUnavailable,
  bootSession: daemonClientUnavailable,
  replaySession: daemonClientUnavailable,
  turn: daemonClientUnavailable,
  attachTurn: daemonClientUnavailable,
  turnState: daemonClientUnavailable,
  listRequests: daemonClientUnavailable,
  answerRequest: daemonClientUnavailable,
  steer: daemonClientUnavailable,
  steerReceipt: daemonClientUnavailable,
  interrupt: daemonClientUnavailable,
  decidePermission: daemonClientUnavailable,
  listAgents: daemonClientUnavailable,
  listRoles: daemonClientUnavailable,
  listMethods: daemonClientUnavailable,
  inspectMethod: daemonClientUnavailable,
  resolveSelectedContext: daemonClientUnavailable,
  replaceSelectedMethods: daemonClientUnavailable,
  getNativePlanCapability: daemonClientUnavailable,
  listNativePlanRevisions: daemonClientUnavailable,
  listNativePlanClarifications: daemonClientUnavailable,
  replyNativePlanClarification: daemonClientUnavailable,
  exportNativePlan: daemonClientUnavailable,
  scaffold: daemonClientUnavailable
};

const unboundHostedBootstrapPort: HostedBootstrapPort = {
  bindProject: daemonClientUnavailable,
  getStatus: daemonClientUnavailable,
  initializeProject: daemonClientUnavailable,
  grantProviderNetworkConsent: daemonClientUnavailable,
  startLogin: daemonClientUnavailable,
  cancelLogin: daemonClientUnavailable,
  signOut: daemonClientUnavailable
};

type HarnessPortRegistry = {
  daemonPort?: DaemonHarnessPort;
  boundPorts?: Map<string, DaemonHarnessPort>;
  boundProjectIds?: Map<string, string>;
  sessionOwners?: Map<string, { port: DaemonHarnessPort; projectRoot: string }>;
  routingPort?: DaemonHarnessPort;
  daemonBinding?: DaemonProjectBinding;
  daemonEnvironmentInitialized?: boolean;
  hostedBootstrapPort?: HostedBootstrapPort;
  hostedBootstrapEnvironmentInitialized?: boolean;
};

const HARNESS_PORT_REGISTRY = Symbol.for('chirality.app.harness-port-registry/v1');

function portRegistry(): HarnessPortRegistry {
  const target = globalThis as typeof globalThis & {
    [HARNESS_PORT_REGISTRY]?: HarnessPortRegistry;
  };
  return target[HARNESS_PORT_REGISTRY] ??= {};
}

export function getDaemonHarnessPort(): DaemonHarnessPort {
  const registry = portRegistry();
  if (registry.daemonPort === undefined && !registry.daemonEnvironmentInitialized) {
    // Loading is intentionally lazy: tests and alternate hosts may inject a
    // port, while production route evaluation never constructs an engine.
    registry.daemonPort = createRuntimeDaemonHarnessPortFromEnvironment();
    registry.daemonEnvironmentInitialized = true;
    const projectId = process.env.CHIRALITY_RUNTIME_PROJECT_ID?.trim();
    const projectRoot = process.env.CHIRALITY_RUNTIME_PROJECT_ROOT?.trim();
    if (projectId && projectRoot) {
      registry.daemonBinding = { projectId, projectRoot: resolve(projectRoot) };
    }
  }
  if (!registry.daemonBinding) return registry.daemonPort ?? unboundDaemonHarnessPort;
  registry.boundPorts ??= new Map([[registry.daemonBinding.projectRoot, registry.daemonPort!]]);
  registry.boundProjectIds ??= new Map([[registry.daemonBinding.projectRoot, registry.daemonBinding.projectId]]);
  return registry.routingPort ??= createRoutingPort(registry);
}

// Every method declares its routing input. New session endpoints must choose an
// owner selector here; they cannot accidentally inherit the selected folder.
const routeKinds = {
  createSession: 'rootObject', listSessions: 'root', getSession: 'session',
  deleteSession: 'session', bootSession: 'sessionObject', replaySession: 'session',
  turn: 'sessionObject', attachTurn: 'session', turnState: 'session',
  listRequests: 'session', answerRequest: 'session', steer: 'session', steerReceipt: 'session',
  interrupt: 'sessionObject', decidePermission: 'sessionObject', listAgents: 'selected',
  listRoles: 'root', listMethods: 'rootObject', inspectMethod: 'rootObject',
  resolveSelectedContext: 'session', replaceSelectedMethods: 'session',
  getNativePlanCapability: 'session', listNativePlanRevisions: 'session',
  listNativePlanClarifications: 'session', replyNativePlanClarification: 'session',
  exportNativePlan: 'session', scaffold: 'executionRoot'
} as const satisfies Record<keyof DaemonHarnessPort,
  'rootObject' | 'root' | 'session' | 'sessionObject' | 'selected' | 'executionRoot'>;

function createRoutingPort(registry: HarnessPortRegistry): DaemonHarnessPort {
  const owners = registry.sessionOwners ??= new Map();
  const remember = (id: string, port: DaemonHarnessPort, projectRoot: string): void => {
    const owner = owners.get(id);
    if (owner && owner.projectRoot !== projectRoot) {
      throw new HarnessError('WORKING_ROOT_CONFLICT', 409, 'Session ownership changed');
    }
    if (!owner) owners.set(id, { port, projectRoot });
  };
  const sessionPort = async (id: string, options?: DaemonRequestOptions): Promise<DaemonHarnessPort> => {
    const known = owners.get(id);
    if (known) return known.port;
    let unavailableProbe: HarnessError | undefined;
    for (const port of new Set(registry.boundPorts?.values())) {
      let session: SessionRecord | ReadableRuntimeSessionRecord;
      try {
        ({ session } = await port.getSession(id, options));
      } catch (error) {
        if (!(error instanceof HarnessError)) throw error;
        if (error.type === 'SESSION_NOT_FOUND') continue;
        if (error.type === 'WORKING_ROOT_CONFLICT' || error.type === 'WORKING_ROOT_INACCESSIBLE') {
          // This is only an ownership probe. An unrelated unavailable folder
          // must not prevent another scoped port from proving the actual owner.
          // Preserve the failure unless a verified owner is subsequently found.
          unavailableProbe ??= error;
          continue;
        }
        throw error; // Authentication, authorization and transport errors stay fatal.
      }
      remember(id, port, session.projectRoot);
      return port;
    }
    const recover = getHostedBootstrapPort().resolveSessionPort;
    if (recover) {
      let port: DaemonHarnessPort;
      try {
        port = await recover.call(getHostedBootstrapPort(), id, options);
      } catch (error) {
        if (unavailableProbe && error instanceof HarnessError && error.type === 'SESSION_NOT_FOUND') {
          throw unavailableProbe;
        }
        throw error;
      }
      const { session } = await port.getSession(id, options);
      remember(id, port, session.projectRoot);
      return port;
    }
    if (unavailableProbe) throw unavailableProbe;
    throw new HarnessError('SESSION_NOT_FOUND', 404, `Unknown session: ${id}`);
  };
  const rootPort = async (root: string, options?: DaemonRequestOptions): Promise<DaemonHarnessPort> => {
    const matchingRoot = [...(registry.boundPorts?.keys() ?? [])]
      .filter(candidate => { const path = relative(candidate, root); return path === '' || (path !== '..' && !path.startsWith('../') && !path.startsWith('/')); })
      .sort((left, right) => right.length - left.length)[0];
    let port = matchingRoot === undefined ? undefined : registry.boundPorts?.get(matchingRoot);
    if (!port) {
      const binding = await getHostedBootstrapPort().bindProject(root, options);
      if (binding.registration === 'required') {
        throw new HarnessError('WORKING_ROOT_INACCESSIBLE', 404, 'No registered project owns the requested root');
      }
      port = registry.boundPorts?.get(root);
    }
    if (!port) throw new HarnessError('WORKING_ROOT_CONFLICT', 409, 'Project is not bound');
    return port;
  };
  return Object.fromEntries(Object.entries(routeKinds).map(([name, kind]) => [name,
    async (...args: unknown[]) => {
      const last = args.at(-1);
      const options = last && typeof last === 'object' && 'signal' in last ? last as DaemonRequestOptions : undefined;
      const input = args[0] as { sessionId: string; projectRoot: string; executionRoot: string };
      const port = kind === 'session' ? await sessionPort(args[0] as string, options)
        : kind === 'sessionObject' ? await sessionPort(input.sessionId, options)
        : kind === 'root' ? await rootPort(args[0] as string, options)
        : kind === 'rootObject' ? await rootPort(input.projectRoot, options)
        : kind === 'executionRoot' ? await rootPort(input.executionRoot, options)
        : registry.daemonPort ?? unboundDaemonHarnessPort;
      const result = await Reflect.apply(port[name as keyof DaemonHarnessPort], port, args);
      if (name === 'createSession' || name === 'listSessions') {
        const records = name === 'createSession' ? [result.session] : result.sessions;
        for (const record of records) remember(record.sessionId, port, record.projectRoot);
      }
      return result;
    }
  ])) as unknown as DaemonHarnessPort;
}

export function getHostedBootstrapPort(): HostedBootstrapPort {
  const registry = portRegistry();
  if (
    registry.hostedBootstrapPort === undefined &&
    !registry.hostedBootstrapEnvironmentInitialized
  ) {
    registry.hostedBootstrapPort = createRuntimeHostedBootstrapPortFromEnvironment(
      process.env,
      installBoundDaemonHarnessPort
    );
    registry.hostedBootstrapEnvironmentInitialized = true;
  }
  return registry.hostedBootstrapPort ?? unboundHostedBootstrapPort;
}

/**
 * Installed by the Desktop runtime-client composition root after it has loaded
 * the authenticated daemon client. It is deliberately not initialized from a
 * route module, which prevents Next from owning a second runtime singleton.
 */
export function installDaemonHarnessPort(port: DaemonHarnessPort): void {
  const registry = portRegistry();
  registry.daemonEnvironmentInitialized = true;
  registry.daemonPort = port;
  registry.daemonBinding = undefined;
  registry.boundPorts = undefined;
  registry.boundProjectIds = undefined;
  registry.sessionOwners = undefined;
  registry.routingPort = undefined;
}

export function installBoundDaemonHarnessPort(
  port: DaemonHarnessPort,
  binding: DaemonProjectBinding,
  allowReplacement = false
): void {
  const registry = portRegistry();
  const current = registry.daemonBinding;
  if (
    registry.daemonPort !== undefined &&
    !allowReplacement &&
    (current === undefined ||
      current.projectId !== binding.projectId ||
      current.projectRoot !== binding.projectRoot)
  ) {
    throw new HarnessError(
      'WORKING_ROOT_CONFLICT',
      409,
      'A different project is already bound to the Desktop runtime client'
    );
  }
  registry.daemonEnvironmentInitialized = true;
  registry.boundPorts ??= new Map();
  // Reuse the verified port for this root so cached session owners remain stable.
  registry.boundProjectIds ??= new Map();
  const previousId = registry.boundProjectIds.get(binding.projectRoot);
  if (previousId !== undefined && previousId !== binding.projectId) {
    throw new HarnessError('WORKING_ROOT_CONFLICT', 409, 'Verified project ownership changed');
  }
  registry.boundProjectIds.set(binding.projectRoot, binding.projectId);
  const retained = registry.boundPorts.get(binding.projectRoot);
  registry.daemonPort = retained ?? port;
  registry.boundPorts.set(binding.projectRoot, retained ?? port);
  registry.daemonBinding = binding;
}

export function installHostedBootstrapPort(port: HostedBootstrapPort): void {
  const registry = portRegistry();
  registry.hostedBootstrapEnvironmentInitialized = true;
  registry.hostedBootstrapPort = port;
}

export function resetDaemonHarnessPortForTests(): void {
  const registry = portRegistry();
  registry.daemonEnvironmentInitialized = false;
  registry.daemonPort = undefined;
  registry.daemonBinding = undefined;
  registry.hostedBootstrapEnvironmentInitialized = false;
  registry.hostedBootstrapPort = undefined;
  registry.boundPorts = undefined;
  registry.boundProjectIds = undefined;
  registry.sessionOwners = undefined;
  registry.routingPort = undefined;
}
