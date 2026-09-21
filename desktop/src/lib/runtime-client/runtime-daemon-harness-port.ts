import { basename, isAbsolute, relative, resolve } from 'node:path';
import { realpath } from 'node:fs/promises';

import {
  RuntimeClient,
  RuntimeTransportError,
  type RuntimeStream
} from '@chirality/runtime-client';
import {
  RuntimeError,
  type AnswerSessionRequestResponse,
  type HostedBootstrapProjectRegistrationResponse,
  type ProjectStatus,
  type RegisteredProject,
  type ReadableRuntimeSessionRecord,
  type ServerRequestAnswer,
  type SessionRequestsResponse,
  type SessionTurnState
} from '@chirality/runtime-contracts';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { resolveHostedProjectTokenFile } from '@chirality/runtime-daemon/hosted-paths';
import type {
  HarnessErrorType,
  SessionRecord
} from '@chirality/runtime-contracts/types';

import type {
  DaemonHarnessPort,
  DaemonProjectBinding,
  DaemonRequestOptions,
  DaemonTurnFrame,
  HostedBootstrapPort,
  HostedBootstrapStatusResponse,
  HostedProjectBindingResponse,
  HostedProjectInitializationResponse,
  RunningDaemonHarnessTurn
} from './daemon-harness-port';

const APP_DEV_PROJECT_ID = 'chirality-app-dev';

/**
 * Turn-registry surface of `RuntimeClient` (D-GOV-43 section 5). The methods
 * are declared here so this port type-checks against a client build that does
 * not carry them yet; a client that does is used as is, and a client that does
 * not is driven through its generic `requestEvents` / `requestJson` transport
 * against the contract routes. Nothing here constructs a second transport.
 */
export interface RuntimeDaemonHarnessPortOptions {
  client: RuntimeClient;
  projectId?: string;
  projectRoot?: string;
}

export interface RuntimeDaemonHarnessEnvironment {
  [name: string]: string | undefined;
  CHIRALITY_RUNTIME_SOCKET_PATH?: string;
  CHIRALITY_RUNTIME_TOKEN_FILE?: string;
  CHIRALITY_RUNTIME_PROJECT_ID?: string;
  CHIRALITY_RUNTIME_PROJECT_ROOT?: string;
  CHIRALITY_RUNTIME_DIRECTORY?: string;
}

export interface RuntimeHostedBootstrapPortOptions {
  bootstrapClient: RuntimeClient;
  runtimeDirectory: string;
  socketPath: string;
  createScopedClient?: (input: { socketPath: string; tokenFile: string }) => RuntimeClient;
  installBoundPort?: (
    port: DaemonHarnessPort,
    binding: DaemonProjectBinding,
    allowReplacement: boolean
  ) => void;
}

function asLegacySession(
  session: ReadableRuntimeSessionRecord,
  projectId = APP_DEV_PROJECT_ID
): ReadableRuntimeSessionRecord {
  if (session.projectId !== projectId) {
    throw new RuntimeError(
      'FORBIDDEN',
      'The daemon returned a session outside the configured app-dev project',
      403
    );
  }
  return session;
}

function harnessErrorType(error: RuntimeError): HarnessErrorType {
  switch (error.code) {
    case 'INVALID_REQUEST':
      return 'INVALID_REQUEST';
    case 'SESSION_NOT_FOUND':
    case 'NOT_FOUND':
      return 'SESSION_NOT_FOUND';
    case 'SESSION_TURN_IN_PROGRESS':
      return 'TURN_IN_PROGRESS';
    case 'MODEL_UNAVAILABLE':
    case 'MODEL_NOT_RESIDENT':
    case 'RESIDENCY_TRANSITION_IN_PROGRESS':
    case 'RESIDENCY_DRAIN_TIMEOUT':
    case 'RESIDENCY_UNMANAGED_CONFLICT':
      return 'MODEL_UNAVAILABLE';
    case 'OMLX_AUTHENTICATION_FAILED':
    case 'UNAUTHORIZED':
    case 'FORBIDDEN':
      return 'PROVIDER_AUTH_FAILURE';
    case 'OMLX_PROTOCOL_FAILURE':
      return 'PROVIDER_PROTOCOL_FAILURE';
    case 'PROJECT_NOT_FOUND':
      return 'WORKING_ROOT_INACCESSIBLE';
    case 'PROJECT_MANIFEST_INVALID':
    case 'PROJECT_MANIFEST_DRIFT':
      return 'WORKING_ROOT_CONFLICT';
    case 'ENGINE_UNAVAILABLE':
    case 'OMLX_UNAVAILABLE':
      return 'ENGINE_UNAVAILABLE';
    default:
      return 'SDK_FAILURE';
  }
}

function translateDaemonError(error: unknown): HarnessError {
  if (error instanceof HarnessError) return error;
  if (error instanceof RuntimeError) {
    return new HarnessError(
      harnessErrorType(error),
      error.status,
      error.message,
      error.details
    );
  }
  if (error instanceof RuntimeTransportError) {
    const transport = error as RuntimeTransportError & { reason?: string; operation?: string; sessionId?: string };
    const timeout = transport.reason === 'timeout';
    const boot = transport.operation === 'boot';
    const sessionId = typeof transport.sessionId === 'string' && /^[A-Za-z0-9_.-]{1,160}$/.test(transport.sessionId) ? transport.sessionId : undefined;
    return new HarnessError(
      'ENGINE_UNAVAILABLE',
      timeout ? 504 : 503,
      timeout ? (boot ? 'Session initialization timed out while waiting for Runtime.' : 'The Runtime request timed out.') : 'Chirality runtime daemon is unavailable',
      { transportReason: timeout ? 'timeout' : 'transport', ...(boot ? { operation: 'boot' } : {}), ...(sessionId ? { sessionId } : {}) }
    );
  }
  if (error instanceof Error) {
    return new HarnessError('SDK_FAILURE', 500, error.message);
  }
  return new HarnessError('SDK_FAILURE', 500, 'Unexpected runtime daemon failure');
}

async function mapped<T>(operation: () => Promise<T>): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    throw translateDaemonError(error);
  }
}

function containsPath(root: string, candidate: string): boolean {
  const child = relative(resolve(root), resolve(candidate));
  return child === '' || (!child.startsWith('..') && !isAbsolute(child));
}

function authorizedProject(status: ProjectStatus): RegisteredProject {
  if (status.manifestDrift || !status.adaptersEnabled) {
    throw new RuntimeError(
      'PROJECT_MANIFEST_DRIFT',
      'Project manifest changed after registration',
      409,
      { projectId: status.project.projectId }
    );
  }
  return status.project;
}

/**
 * Adapts the pre-daemon Desktop API to the versioned shared-runtime API.
 *
 * RuntimeClient supplies the authenticated Unix-socket transport. This class
 * owns only compatibility mappings; it does not construct an engine, session
 * store, permission broker, or other runtime singleton.
 */
export class RuntimeDaemonHarnessPort implements DaemonHarnessPort {
  private readonly projectId: string;
  private readonly projectRoot?: string;

  constructor(
    private readonly client: RuntimeClient,
    projectId = APP_DEV_PROJECT_ID,
    projectRoot?: string
  ) {
    this.projectId = projectId;
    this.projectRoot = projectRoot === undefined ? undefined : resolve(projectRoot);
  }

  async createSession(
    request: Parameters<DaemonHarnessPort['createSession']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['createSession']> {
    return mapped(async () => {
      const project = await this.requirePathInConfiguredProject(
        request.projectRoot,
        options?.signal
      );
      const permissionMode = request.permissionMode ?? (
        request.mode === 'dontAsk' ? 'readOnly' : undefined
      );
      const session = await this.client.createSession(
        this.projectId,
        {
          projectId: this.projectId,
          ...(request.roleId === undefined ? {} : { roleId: request.roleId }),
          ...(request.interactionMode === undefined
            ? {}
            : { interactionMode: request.interactionMode }),
          ...(permissionMode === undefined
            ? {}
            : { permissionMode }),
          ...(request.selectedMethods === undefined
            ? {}
            : { selectedMethods: request.selectedMethods }),
          ...(request.declaredContext === undefined
            ? {}
            : { declaredContext: request.declaredContext }),
          ...(request.allowedWriteTargets === undefined
            ? {}
            : { allowedWriteTargets: request.allowedWriteTargets }),
          ...(request.modelSelection === undefined
            ? {}
            : { modelSelection: request.modelSelection }),
          ...(request.persona === undefined ? {} : { persona: request.persona }),
          ...(request.mode === undefined ? {} : { mode: request.mode })
        },
        options?.signal
      );
      return { session: asLegacySession(session, this.projectId) };
    });
  }

  async listSessions(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listSessions']> {
    return mapped(async () => {
      await this.requirePathInConfiguredProject(projectRoot, options?.signal);
      const sessions = await this.client.listSessions(this.projectId, options?.signal);
      return {
        sessions: sessions.map((session) => asLegacySession(session, this.projectId))
      };
    });
  }

  async getSession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['getSession']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const session = await this.client.getSession(
        this.projectId,
        sessionId,
        options?.signal
      );
      return { session: asLegacySession(session, this.projectId) };
    });
  }

  async deleteSession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['deleteSession']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      await this.client.deleteSession(this.projectId, sessionId, options?.signal);
      return { ok: true };
    });
  }

  async bootSession(
    request: Parameters<DaemonHarnessPort['bootSession']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['bootSession']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.bootSession(
        this.projectId,
        request.sessionId,
        { opts: request.opts },
        options?.signal
      );
    });
  }

  async replaySession(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['replaySession']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const replay = await this.client.replaySession(
        this.projectId,
        sessionId,
        options?.signal
      );
      return {
        ...replay,
        session: asLegacySession(replay.session, this.projectId),
        events: [...replay.events]
      };
    });
  }

  async turn(
    request: Parameters<DaemonHarnessPort['turn']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['turn']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const stream = await this.client.turnSession(
        this.projectId,
        request.sessionId,
        {
          message: request.message,
          ...(request.turnId === undefined ? {} : { turnId: request.turnId }),
          ...(request.opts === undefined ? {} : { opts: request.opts }),
          ...(request.attachments === undefined
            ? {}
            : { attachments: request.attachments }),
          ...(request.interactionMode === undefined
            ? {}
            : { interactionMode: request.interactionMode }),
          ...(request.permissionMode === undefined
            ? {}
            : { permissionMode: request.permissionMode }),
          ...(request.model === undefined ? {} : { model: request.model }),
          ...(request.reasoningEffort === undefined
            ? {}
            : { reasoningEffort: request.reasoningEffort }),
          ...(request.methods === undefined ? {} : { methods: request.methods })
        },
        options?.signal
      );
      return this.runningTurn(stream);
    });
  }

  async attachTurn(
    sessionId: string,
    after: number,
    options?: DaemonRequestOptions & { turnId?: string }
  ): Promise<RunningDaemonHarnessTurn> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const afterSeq = Number.isFinite(after) && after > 0 ? Math.floor(after) : 0;
      const stream = await this.client.attachSessionTurn(
        this.projectId,
        sessionId,
        { after: afterSeq, ...(options?.turnId === undefined ? {} : { turnId: options.turnId }) },
        options?.signal
      );
      return this.runningTurn(stream);
    });
  }

  async turnState(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<SessionTurnState> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.sessionTurnState(this.projectId, sessionId, options?.signal);
    });
  }

  async listRequests(
    sessionId: string,
    options?: DaemonRequestOptions
  ): Promise<SessionRequestsResponse> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.listSessionRequests(this.projectId, sessionId, options?.signal);
    });
  }

  async answerRequest(
    sessionId: string,
    requestId: string,
    answer: ServerRequestAnswer,
    options?: DaemonRequestOptions
  ): Promise<AnswerSessionRequestResponse> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.answerSessionRequest(this.projectId, sessionId, requestId, answer, options?.signal);
    });
  }

  async steer(sessionId: string, request: Parameters<DaemonHarnessPort['steer']>[1], options?: DaemonRequestOptions): ReturnType<DaemonHarnessPort['steer']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.sessionTurnSteer(this.projectId, sessionId, request, options?.signal);
    });
  }

  async steerReceipt(sessionId: string, request: Parameters<DaemonHarnessPort['steerReceipt']>[1], options?: DaemonRequestOptions): ReturnType<DaemonHarnessPort['steerReceipt']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.sessionTurnSteerReceipt(this.projectId, sessionId, request, options?.signal);
    });
  }

  async interrupt(
    request: Parameters<DaemonHarnessPort['interrupt']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['interrupt']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      await this.client.interruptSession(
        this.projectId,
        request.sessionId,
        options?.signal
      );
      return { ok: true };
    });
  }

  async decidePermission(
    request: Parameters<DaemonHarnessPort['decidePermission']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['decidePermission']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const response = await this.client.decidePermission(
        this.projectId,
        request.sessionId,
        {
          requestId: request.toolUseId,
          decision: request.verdict
        },
        options?.signal
      );
      const compatibility = response as typeof response & { decided?: boolean };
      return {
        ok: true,
        decided: compatibility.decided ?? compatibility.accepted
      };
    });
  }

  async listAgents(
    request: Parameters<DaemonHarnessPort['listAgents']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listAgents']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      const roles = await this.client.listRoles(this.projectId, options?.signal);
      return {
        agents: roles.roles
          .filter((role) => !request.directChatOnly || role.directEntry)
          .map((role) => ({
            name: role.id,
            type: role.agentType,
            class: role.agentType === 2 ? 'TASK' : 'PERSONA'
          }))
      };
    });
  }

  async listRoles(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listRoles']> {
    return mapped(async () => {
      await this.requirePathInConfiguredProject(projectRoot, options?.signal);
      return this.client.listRoles(this.projectId, options?.signal);
    });
  }

  async listMethods(
    request: Parameters<DaemonHarnessPort['listMethods']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listMethods']> {
    return mapped(async () => {
      await this.requirePathInConfiguredProject(request.projectRoot, options?.signal);
      const response = await this.client.listMethods(this.projectId, options?.signal);
      const query = request.query?.trim().toLocaleLowerCase();
      return {
        ...response,
        methods: response.methods.filter((method) =>
          (request.kind === undefined || method.kind === request.kind) &&
          (query === undefined ||
            method.name.toLocaleLowerCase().includes(query) ||
            method.description.toLocaleLowerCase().includes(query))
        )
      };
    });
  }

  async inspectMethod(
    request: Parameters<DaemonHarnessPort['inspectMethod']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['inspectMethod']> {
    return mapped(async () => {
      await this.requirePathInConfiguredProject(request.projectRoot, options?.signal);
      return this.client.inspectMethod(this.projectId, request.qualifiedId, options?.signal);
    });
  }

  async resolveSelectedContext(
    sessionId: string,
    request: Parameters<DaemonHarnessPort['resolveSelectedContext']>[1],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['resolveSelectedContext']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.resolveSelectedContext(
        this.projectId,
        sessionId,
        request,
        options?.signal
      );
    });
  }

  async replaceSelectedMethods(
    sessionId: string,
    request: Parameters<DaemonHarnessPort['replaceSelectedMethods']>[1],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['replaceSelectedMethods']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.replaceSelectedMethods(
        this.projectId,
        sessionId,
        request,
        options?.signal
      );
    });
  }

  async getNativePlanCapability(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['getNativePlanCapability']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.getNativePlanCapability(this.projectId, sessionId, options?.signal);
    });
  }

  async listNativePlanRevisions(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listNativePlanRevisions']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.listNativePlanRevisions(this.projectId, sessionId, options?.signal);
    });
  }

  async listNativePlanClarifications(
    sessionId: string,
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['listNativePlanClarifications']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.listNativePlanClarifications(
        this.projectId,
        sessionId,
        options?.signal
      );
    });
  }

  async replyNativePlanClarification(
    sessionId: string,
    requestId: string | number,
    answers: Parameters<DaemonHarnessPort['replyNativePlanClarification']>[2],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['replyNativePlanClarification']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.replyNativePlanClarification(
        this.projectId,
        sessionId,
        { requestId, answers },
        options?.signal
      );
    });
  }

  async exportNativePlan(
    sessionId: string,
    request: Parameters<DaemonHarnessPort['exportNativePlan']>[1],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['exportNativePlan']> {
    return mapped(async () => {
      await this.requireConfiguredProject(options?.signal);
      return this.client.exportNativePlan(this.projectId, sessionId, request, options?.signal);
    });
  }

  async scaffold(
    request: Parameters<DaemonHarnessPort['scaffold']>[0],
    options?: DaemonRequestOptions
  ): ReturnType<DaemonHarnessPort['scaffold']> {
    return mapped(async () => {
      const project = await this.requireConfiguredProject(options?.signal);
      for (const candidate of [request.executionRoot, request.decompositionPath]) {
        if (!containsPath(project.canonicalRoot, candidate)) {
          throw new RuntimeError(
            'PROJECT_NOT_FOUND',
            'The requested path is outside the configured app-dev project',
            404
          );
        }
      }
      return this.client.scaffold(this.projectId, request, options?.signal);
    });
  }

  /**
   * The Runtime owns the turn; this object is only an observer of it. A
   * cancelled observer closes its own subscription and nothing else: the turn
   * keeps running and explicit Stop goes through `interrupt`.
   */
  private runningTurn(stream: RuntimeStream): RunningDaemonHarnessTurn {
    let cancelled = false;
    return {
      events: stream as AsyncIterable<DaemonTurnFrame>,
      cancel: async (): Promise<void> => {
        if (cancelled) return;
        cancelled = true;
        stream.cancel();
      }
    };
  }

  private async requireConfiguredProject(signal?: AbortSignal): Promise<RegisteredProject> {
    const project = authorizedProject(await this.client.projectStatus(this.projectId, signal));
    if (
      project.projectId !== this.projectId ||
      (this.projectRoot !== undefined &&
        resolve(project.canonicalRoot) !== this.projectRoot)
    ) {
      throw new RuntimeError(
        'PROJECT_MANIFEST_DRIFT',
        'The daemon project registration does not match the Desktop project binding',
        409,
        { projectId: this.projectId }
      );
    }
    return project;
  }

  private async requirePathInConfiguredProject(
    candidate: string,
    signal?: AbortSignal
  ): Promise<RegisteredProject> {
    const project = await this.requireConfiguredProject(signal);
    if (!containsPath(project.canonicalRoot, candidate)) {
      throw new RuntimeError(
        'PROJECT_NOT_FOUND',
        'The requested path is outside the configured app-dev project',
        404
      );
    }
    return project;
  }
}

type VerifiedHostedBinding = {
  projectId: string;
  projectRoot: string;
  manifestHash: string;
  client: RuntimeClient;
};

type HostedBindingReservation =
  | { kind: 'explicit'; selectionGeneration: number }
  | { kind: 'hydration'; selectionGeneration: number; hydrationGeneration: number };

export class RuntimeHostedBootstrapPort implements HostedBootstrapPort {
  private binding?: VerifiedHostedBinding;
  private readonly bindings = new Map<string, VerifiedHostedBinding>();
  private bindingSelectionGeneration = 0;
  private hydrationGeneration = 0;
  private pendingExplicitSelection?: number;
  private readonly createScopedClient: NonNullable<
    RuntimeHostedBootstrapPortOptions['createScopedClient']
  >;
  private readonly installBoundPort?: RuntimeHostedBootstrapPortOptions['installBoundPort'];

  constructor(private readonly options: RuntimeHostedBootstrapPortOptions) {
    this.createScopedClient = options.createScopedClient ?? (
      (input) => new RuntimeClient(input)
    );
    this.installBoundPort = options.installBoundPort;
  }

  async bindProject(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedProjectBindingResponse> {
    return mapped(async () => {
      const canonicalRoot = await this.canonicalRoot(projectRoot);
      const capturedBinding = this.bindings.get(canonicalRoot);
      if (capturedBinding !== undefined) {
        this.requireSameRoot(canonicalRoot, capturedBinding);
        await this.revalidateBinding(capturedBinding, options?.signal);
        this.installBinding(capturedBinding, true);
        return { registration: 'registered', projectId: capturedBinding.projectId };
      }
      const binding = await this.resolveAndBind(canonicalRoot, options?.signal);
      if (!binding) return { registration: 'required' };
      return { registration: 'registered', projectId: binding.projectId };
    });
  }

  /**
   * Registration probe plus the Runtime's hosted account status for a
   * registered folder. The App-owned Runtime has no account-host admission
   * step, so the ordinary project-scoped client reads status directly.
   */
  async getStatus(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedBootstrapStatusResponse> {
    return mapped(async () => {
      const canonicalRoot = await this.canonicalRoot(projectRoot);
      const binding = await this.resolveAndBind(canonicalRoot, options?.signal);
      if (!binding) return { registration: 'required' };
      const status = await binding.client.hostedBootstrapStatus(binding.projectId, options?.signal);
      return { registration: 'registered', projectId: binding.projectId, status };
    });
  }

  async initializeProject(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): Promise<HostedProjectInitializationResponse> {
    return mapped(async () => {
      const reservation = this.reserveExplicitSelection();
      try {
        const canonicalRoot = await this.canonicalRoot(projectRoot);
        const registration = await this.options.bootstrapClient.initializeHostedBootstrapProject(
          { projectRoot: canonicalRoot },
          options?.signal
        );
        const binding = await this.verifyAndBind(
          canonicalRoot,
          registration,
          true,
          options?.signal,
          reservation
        );
        return { registration: 'registered', projectId: binding.projectId };
      } finally {
        if (this.pendingExplicitSelection === reservation.selectionGeneration) {
          this.pendingExplicitSelection = undefined;
        }
      }
    });
  }

  /**
   * No consent step exists under D-GOV-43: the stock Codex App Server talks to
   * its provider on its own terms. The method survives only so the route keeps
   * its shape; it reads and returns the current status without any mutation.
   */
  async grantProviderNetworkConsent(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<HostedBootstrapPort['grantProviderNetworkConsent']> {
    return mapped(async () => {
      const binding = await this.requireBinding(projectRoot, options?.signal, this.binding);
      return binding.client.hostedBootstrapStatus(binding.projectId, options?.signal);
    });
  }

  /**
   * Sign-in, cancel and sign-out are account actions of the App host, so they
   * travel over the per-launch client token; the project-scoped client keeps
   * its least scopes (runtime, sessions, model reads).
   */
  async startLogin(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<HostedBootstrapPort['startLogin']> {
    return mapped(async () => {
      const binding = await this.requireBinding(projectRoot, options?.signal, this.binding);
      return this.options.bootstrapClient.startHostedBootstrapLogin(binding.projectId, options?.signal);
    });
  }

  async cancelLogin(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<HostedBootstrapPort['cancelLogin']> {
    return mapped(async () => {
      const binding = await this.requireBinding(projectRoot, options?.signal, this.binding);
      return this.options.bootstrapClient.cancelHostedBootstrapLogin(binding.projectId, options?.signal);
    });
  }

  async signOut(
    projectRoot: string,
    options?: DaemonRequestOptions
  ): ReturnType<HostedBootstrapPort['signOut']> {
    return mapped(async () => {
      const capturedBinding = this.binding;
      const binding = await this.requireBinding(projectRoot, options?.signal, capturedBinding);
      if (this.binding !== binding) {
        throw new RuntimeError(
          'PROJECT_MANIFEST_DRIFT',
          'A newer project binding operation superseded this request',
          409
        );
      }
      return this.options.bootstrapClient.signOutHostedProject(binding.projectId, options?.signal);
    });
  }

  private async canonicalRoot(projectRoot: string): Promise<string> {
    const requested = resolve(projectRoot);
    if (projectRoot !== requested) {
      throw new RuntimeError(
        'INVALID_REQUEST',
        'The selected project folder must be a normalized absolute path',
        400
      );
    }
    let canonical: string;
    try {
      canonical = await realpath(requested);
    } catch {
      throw new RuntimeError('PROJECT_NOT_FOUND', 'The selected project folder is inaccessible', 404);
    }
    if (canonical !== requested) {
      throw new RuntimeError(
        'INVALID_REQUEST',
        'The selected project folder must be a canonical non-symlink path',
        400
      );
    }
    return canonical;
  }

  private async resolveAndBind(
    canonicalRoot: string,
    signal?: AbortSignal
  ): Promise<VerifiedHostedBinding | undefined> {
    const capturedBinding = this.bindings.get(canonicalRoot);
    if (capturedBinding !== undefined) {
      return this.revalidateBinding(capturedBinding, signal);
    }
    const reservation = this.reserveHydration();
    let registered: RegisteredProject;
    try {
      registered = await this.options.bootstrapClient.resolveProjectByRoot(
        canonicalRoot,
        signal
      );
    } catch (error) {
      if (error instanceof RuntimeError && error.code === 'PROJECT_NOT_FOUND') {
        return undefined;
      }
      throw error;
    }
    return this.verifyAndBind(
      canonicalRoot,
      {
        projectId: registered.projectId,
        manifestHash: registered.manifestHash
      },
      false,
      signal,
      reservation
    );
  }

  private requireSameRoot(canonicalRoot: string, binding = this.binding): void {
    if (binding?.projectRoot !== canonicalRoot) {
      throw new RuntimeError(
        'PROJECT_MANIFEST_DRIFT',
        'A different project is already bound to the Desktop runtime client',
        409
      );
    }
  }

  private async requireBinding(
    projectRoot: string,
    signal?: AbortSignal,
    capturedBinding = this.binding
  ): Promise<VerifiedHostedBinding> {
    const canonicalRoot = await this.canonicalRoot(projectRoot);
    const rootBinding = this.bindings.get(canonicalRoot);
    if (rootBinding !== undefined) {
      return this.revalidateBinding(rootBinding, signal);
    }
    const reservation = this.reserveHydration();
    const registered = await this.options.bootstrapClient.resolveProjectByRoot(
      canonicalRoot,
      signal
    );
    return this.verifyAndBind(
      canonicalRoot,
      { projectId: registered.projectId, manifestHash: registered.manifestHash },
      false,
      signal,
      reservation
    );
  }

  private async verifyAndBind(
    canonicalRoot: string,
    registration: HostedBootstrapProjectRegistrationResponse,
    allowReplacement: boolean,
    signal?: AbortSignal,
    reservation: HostedBindingReservation = this.reserveHydration()
  ): Promise<VerifiedHostedBinding> {
    const trustedStatus = await this.options.bootstrapClient.projectStatus(
      registration.projectId,
      signal
    );
    const trustedProject = authorizedProject(trustedStatus);
    this.assertRegistration(canonicalRoot, registration, trustedProject);

    const tokenFile = resolveHostedProjectTokenFile(
      this.options.runtimeDirectory,
      registration.projectId
    );
    const client = this.createScopedClient({
      socketPath: this.options.socketPath,
      tokenFile
    });
    const scopedProject = authorizedProject(
      await client.projectStatus(registration.projectId, signal)
    );
    this.assertRegistration(canonicalRoot, registration, scopedProject);

    const binding = {
      projectId: registration.projectId,
      projectRoot: canonicalRoot,
      manifestHash: registration.manifestHash,
      client
    };
    const retained = this.bindings.get(canonicalRoot);
    if (retained && retained.projectId !== binding.projectId) {
      throw new RuntimeError('PROJECT_MANIFEST_DRIFT', 'Verified project ownership changed', 409);
    }
    // A superseded selection may still establish a valid separate folder.
    // Retain it for later root-specific requests without replacing the selection.
    if (!retained || this.reservationIsCurrent(reservation)) this.bindings.set(canonicalRoot, binding);
    if (!this.reservationIsCurrent(reservation)) {
      throw new RuntimeError(
        'PROJECT_MANIFEST_DRIFT',
        'A newer project binding operation superseded this request',
        409
      );
    }
    this.installBinding(binding, allowReplacement || this.binding !== undefined);
    this.binding = binding;
    return binding;
  }

  private installBinding(binding: VerifiedHostedBinding, allowReplacement: boolean): DaemonHarnessPort {
    const port = new RuntimeDaemonHarnessPort(binding.client, binding.projectId, binding.projectRoot);
    this.installBoundPort?.(port, { projectId: binding.projectId, projectRoot: binding.projectRoot }, allowReplacement);
    return port;
  }

  async resolveSessionPort(sessionId: string, options?: DaemonRequestOptions): Promise<DaemonHarnessPort> {
    return mapped(async () => {
      // The existing Runtime lookup obeys the launch client's actual scopes.
      // Re-verify its project and use a project-scoped client for the operation.
      const owner = await this.options.bootstrapClient.resolveSessionOwner(sessionId, options?.signal);
      const canonicalRoot = await this.canonicalRoot(owner.project.canonicalRoot);
      let binding = this.bindings.get(canonicalRoot);
      if (binding) {
        await this.revalidateBinding(binding, options?.signal);
      } else {
        binding = await this.verifyAndBind(canonicalRoot, {
          projectId: owner.project.projectId, manifestHash: owner.project.manifestHash
        }, true, options?.signal);
      }
      const port = new RuntimeDaemonHarnessPort(binding.client, binding.projectId, binding.projectRoot);
      await port.getSession(sessionId, options);
      return port;
    });
  }

  private reserveExplicitSelection(): Extract<HostedBindingReservation, { kind: 'explicit' }> {
    const selectionGeneration = ++this.bindingSelectionGeneration;
    this.pendingExplicitSelection = selectionGeneration;
    this.hydrationGeneration += 1;
    return { kind: 'explicit', selectionGeneration };
  }

  private reserveHydration(): Extract<HostedBindingReservation, { kind: 'hydration' }> {
    if (this.pendingExplicitSelection !== undefined) {
      throw new RuntimeError(
        'PROJECT_MANIFEST_DRIFT',
        'An explicit project binding is still in progress',
        409
      );
    }
    return {
      kind: 'hydration',
      selectionGeneration: this.bindingSelectionGeneration,
      hydrationGeneration: ++this.hydrationGeneration
    };
  }

  private reservationIsCurrent(reservation: HostedBindingReservation): boolean {
    if (reservation.selectionGeneration !== this.bindingSelectionGeneration) return false;
    if (reservation.kind === 'explicit') return this.pendingExplicitSelection === reservation.selectionGeneration;
    return this.pendingExplicitSelection === undefined && reservation.hydrationGeneration === this.hydrationGeneration;
  }

  private assertRegistration(
    canonicalRoot: string,
    registration: HostedBootstrapProjectRegistrationResponse,
    project: RegisteredProject
  ): void {
    if (
      project.projectId !== registration.projectId ||
      resolve(project.canonicalRoot) !== canonicalRoot ||
      project.manifestHash !== registration.manifestHash
    ) {
      throw new RuntimeError(
        'PROJECT_MANIFEST_DRIFT',
        'Hosted project registration does not match the selected folder',
        409,
        { projectId: registration.projectId }
      );
    }
  }

  private async revalidateBinding(
    binding: VerifiedHostedBinding,
    signal?: AbortSignal
  ): Promise<VerifiedHostedBinding> {
    const registration = {
      projectId: binding.projectId,
      manifestHash: binding.manifestHash
    };
    const trustedProject = authorizedProject(
      await this.options.bootstrapClient.projectStatus(binding.projectId, signal)
    );
    this.assertRegistration(binding.projectRoot, registration, trustedProject);
    const scopedProject = authorizedProject(
      await binding.client.projectStatus(binding.projectId, signal)
    );
    this.assertRegistration(binding.projectRoot, registration, scopedProject);
    return binding;
  }
}

export function createRuntimeDaemonHarnessPort(
  options: RuntimeDaemonHarnessPortOptions
): DaemonHarnessPort {
  return new RuntimeDaemonHarnessPort(
    options.client,
    options.projectId,
    options.projectRoot
  );
}

export function createRuntimeHostedBootstrapPort(
  options: RuntimeHostedBootstrapPortOptions
): HostedBootstrapPort {
  return new RuntimeHostedBootstrapPort(options);
}

/**
 * The Desktop composition root provides these paths to its Next child.
 * Credentials are read by RuntimeClient from a private file and never cross
 * the renderer boundary.
 */
export function createRuntimeDaemonHarnessPortFromEnvironment(
  environment: RuntimeDaemonHarnessEnvironment = process.env
): DaemonHarnessPort {
  const socketPath = environment.CHIRALITY_RUNTIME_SOCKET_PATH?.trim();
  const tokenFile = environment.CHIRALITY_RUNTIME_TOKEN_FILE?.trim();
  const projectId = environment.CHIRALITY_RUNTIME_PROJECT_ID?.trim();
  const projectRoot = environment.CHIRALITY_RUNTIME_PROJECT_ROOT?.trim();
  if (
    !socketPath ||
    !tokenFile ||
    !/^project-[A-Za-z0-9_-]+\.token$/u.test(basename(tokenFile)) ||
    projectId !== APP_DEV_PROJECT_ID ||
    !projectRoot
  ) {
    throw new HarnessError(
      'ENGINE_UNAVAILABLE',
      503,
      'Chirality runtime daemon client is not configured'
    );
  }
  return new RuntimeDaemonHarnessPort(
    new RuntimeClient({
      socketPath: resolve(socketPath),
      tokenFile: resolve(tokenFile)
    }),
    APP_DEV_PROJECT_ID,
    resolve(projectRoot)
  );
}

export function createRuntimeHostedBootstrapPortFromEnvironment(
  environment: RuntimeDaemonHarnessEnvironment = process.env,
  installBoundPort?: RuntimeHostedBootstrapPortOptions['installBoundPort']
): HostedBootstrapPort {
  const socketPath = environment.CHIRALITY_RUNTIME_SOCKET_PATH?.trim();
  const clientTokenFile = environment.CHIRALITY_RUNTIME_TOKEN_FILE?.trim();
  const runtimeDirectory = environment.CHIRALITY_RUNTIME_DIRECTORY?.trim();
  if (
    !socketPath ||
    !clientTokenFile ||
    !runtimeDirectory ||
    !isAbsolute(socketPath) ||
    !isAbsolute(clientTokenFile) ||
    !isAbsolute(runtimeDirectory) ||
    resolve(socketPath) !== socketPath ||
    resolve(clientTokenFile) !== clientTokenFile ||
    resolve(runtimeDirectory) !== runtimeDirectory
  ) {
    throw new HarnessError(
      'ENGINE_UNAVAILABLE',
      503,
      'Chirality hosted bootstrap client is not configured'
    );
  }
  return new RuntimeHostedBootstrapPort({
    bootstrapClient: new RuntimeClient({ socketPath, tokenFile: clientTokenFile }),
    runtimeDirectory,
    socketPath,
    installBoundPort
  });
}
