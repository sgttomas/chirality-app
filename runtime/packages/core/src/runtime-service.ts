import { randomUUID } from "node:crypto";
import { describeFailureDetails } from "./retirement-failure.js";
import { readdir, readFile, realpath, stat } from "node:fs/promises";
import { basename, join, relative, resolve } from "node:path";
import {
  CODEX_ENGINE_ADAPTER_ID,
  HarnessError,
  HOSTED_MODEL_ID_PATTERN,
  HOSTED_REASONING_EFFORT_PATTERN,
  RuntimeError,
  type Agent1RunRequest,
  type AgentDefinitionSummary,
  type AgentEngineRunInput,
  type Agent1EngineOutcome,
  type CreateSessionRequest,
  type EngineSelection,
  type HarnessEvent,
  type HarnessOpts,
  type PermissionDecisionRequest,
  type ProviderCredentialPort,
  type ScaffoldExecutionRootResponse,
  type ScaffoldRequest,
  type SessionBootResponse,
  type SessionTurnRequest,
  type UIEvent
} from "@chirality/runtime-contracts";
import type { AuthRegistry, RuntimeScope } from "./auth-registry.js";
import type { EngineRegistry } from "./engine-registry.js";
import { isContained, sha256 } from "./fs.js";
import type { ProjectRegistry } from "./project-registry.js";
import type { ResidencyCoordinator } from "./residency-coordinator.js";
import type { SessionStore } from "./session-store.js";
import type { TurnCoordinator } from "./turn-coordinator.js";
import { RuntimeMethodService, type TrustedNativePlanAdapterRegistry, type ProductInstructionOptions } from "./runtime-method-service.js";

export interface RuntimeCredentialStore extends ProviderCredentialPort {
  set(providerId: string, value: string): Promise<void>;
  remove(providerId: string): Promise<void>;
}

export interface ProjectScaffoldPort {
  scaffold(projectId: string, request: ScaffoldRequest): Promise<ScaffoldExecutionRootResponse>;
}

export interface PermissionDecisionPort {
  submit(
    projectId: string,
    sessionId: string,
    request: PermissionDecisionRequest
  ): Promise<void>;
}

/** Narrow view of the delegated runtime's approval answer; declared here so the broker compiles against the method name only. */
export interface DelegatedApprovalAnswerPort {
  answerApprovalByToolUseId(projectId: string, sessionId: string, toolUseId: string, verdict: "allow" | "deny" | "allowForSession"): Promise<unknown>;
}

/**
 * Permission broker for the stock Codex composition: a `PermissionDecisionRequest`
 * names the tool-use id (the Codex item id carried by `tool.permission`) and the
 * broker forwards the verdict to the delegated runtime's approval answer.
 */
export function createDelegatedPermissionBroker(port: DelegatedApprovalAnswerPort): PermissionDecisionPort {
  return {
    async submit(projectId, sessionId, request) {
      if (typeof request.requestId !== "string" || request.requestId.trim() === "") {
        throw new RuntimeError("INVALID_REQUEST", "Permission decision requires the tool-use id as requestId", 400, { reason: "PERMISSION_REQUEST_ID_INVALID" });
      }
      if (request.decision !== "allow" && request.decision !== "deny") {
        throw new RuntimeError("INVALID_REQUEST", "Permission decision must be allow or deny", 400, { reason: "PERMISSION_DECISION_INVALID" });
      }
      await port.answerApprovalByToolUseId(projectId, sessionId, request.requestId, request.decision);
    }
  };
}

export interface Agent1RunPort {
  run(projectId: string, request: Agent1RunRequest): AsyncIterable<UIEvent>;
  interrupt?(projectId: string, sessionId: string): Promise<void>;
  isActive?(projectId: string, sessionId: string): boolean;
}

export interface DefaultSessionPolicy {
  resolve(input: {
    projectId: string;
    persona: string;
    mode: string;
    agentType: 0 | 1;
    /** Client catalog choice; a policy that honours it returns the same model and reasoningEffort. */
    modelSelection?: { model: string; reasoningEffort: string };
  }): Promise<{ role: "agent0" | "agent1"; engineSelection: EngineSelection; reasoningEffort?: string }>;
}

/**
 * Pre-catalog shape gate: a request must carry exactly `model` and `reasoningEffort`
 * before any catalog can be consulted. Catalog membership is decided only by
 * `resolveHostedModelSelection` in the daemon's default session policy.
 */
function validateModelSelection(value: unknown): { model: string; reasoningEffort: string } {
  const invalid = () => new RuntimeError("INVALID_REQUEST", "modelSelection requires exactly model and reasoningEffort", 400, { reason: "MODEL_SELECTION_INVALID" });
  if (!value || typeof value !== "object" || Array.isArray(value) || Object.keys(value).sort().join(",") !== "model,reasoningEffort") throw invalid();
  const { model, reasoningEffort } = value as Record<string, unknown>;
  if (typeof model !== "string" || !HOSTED_MODEL_ID_PATTERN.test(model) || typeof reasoningEffort !== "string" || !HOSTED_REASONING_EFFORT_PATTERN.test(reasoningEffort)) throw invalid();
  return { model, reasoningEffort };
}

export class RuntimeService {
  readonly methods: RuntimeMethodService;
  private readonly bootingSessions = new Set<string>();
  constructor(
    readonly projects: ProjectRegistry,
    readonly sessions: SessionStore,
    readonly engines: EngineRegistry,
    readonly residency: ResidencyCoordinator,
    readonly turns: TurnCoordinator,
    readonly auth: AuthRegistry,
    readonly credentials: RuntimeCredentialStore,
    private readonly scaffoldPort?: ProjectScaffoldPort,
    private readonly agent1Runs?: Agent1RunPort,
    private readonly permissions?: PermissionDecisionPort,
    private readonly defaultSessionPolicy?: DefaultSessionPolicy,
    nativePlan?: TrustedNativePlanAdapterRegistry,
    productInstructions?: ProductInstructionOptions
  ) {
    this.methods = new RuntimeMethodService(projects, sessions, engines, nativePlan, productInstructions);
    this.turns.configureRuntimeMethods(this.methods);
  }

  async registerProject(
    manifestPath: string,
    approvedBy: string,
    approvalReference: string
  ): Promise<{
    projectId: string;
    clientId: string;
    tokenFile: string;
    manifestHash: string;
  }> {
    if (approvedBy.trim() === "" || approvalReference.trim() === "") {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Project registration requires non-empty approval attribution"
      );
    }
    const clientId = `project-${randomUUID()}`;
    const project = await this.projects.register(
      manifestPath,
      { approvedBy, approvalReference },
      clientId
    );
    await this.auth.revokeProjectClients(project.projectId);
    const scopes: RuntimeScope[] = [
      "runtime:read",
      "sessions:read",
      "sessions:write",
      "models:read"
    ];
    const issued = await this.auth.issueClient(clientId, scopes, project.projectId);
    return {
      projectId: project.projectId,
      clientId,
      tokenFile: issued.tokenFile,
      manifestHash: project.manifestHash
    };
  }

  async createSession(request: CreateSessionRequest) {
    const project = await this.projects.requireAuthorized(request.projectId);
    const persona = request.persona ?? request.roleId ?? "HELP_HUMAN";
    const mode = request.mode ?? "direct";
    const selectedRoleId = request.roleId ?? (request.persona === undefined ? "HELP_HUMAN" : undefined);
    const v3Role = selectedRoleId === undefined ? undefined : (await this.methods.listRoles(request.projectId)).roles.find(value => value.id === selectedRoleId);
    if (selectedRoleId !== undefined && (v3Role === undefined || !v3Role.directEntry)) {
      throw new HarnessError("INVALID_REQUEST", 400, `Role '${selectedRoleId}' is not available for direct chat`);
    }
    const roster = v3Role === undefined ? await this.listAgents(request.projectId, true) : [];
    const rosterEntry = v3Role === undefined
      ? (persona.trim().toUpperCase() === "UNTYPED" ? { name: persona, type: 1 as const } : roster.find((entry) => entry.name === persona))
      : { name: v3Role.id, type: v3Role.agentType };
    if (rosterEntry?.type !== 0 && rosterEntry?.type !== 1) {
      throw new HarnessError(
        "INVALID_REQUEST",
        400,
        `Persona '${persona}' is not available for direct chat`
      );
    }
    let role = request.role;
    let engineSelection = request.engineSelection;
    let reasoningEffort: string | undefined;
    const modelSelection = request.modelSelection === undefined ? undefined : validateModelSelection(request.modelSelection);
    if ((role === undefined) !== (engineSelection === undefined)) {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Explicit role and engineSelection must be supplied together"
      );
    }
    if (modelSelection !== undefined && engineSelection !== undefined) {
      throw new RuntimeError("INVALID_REQUEST", "modelSelection cannot be combined with an explicit engineSelection", 400, { reason: "MODEL_SELECTION_INVALID" });
    }
    if (role === undefined || engineSelection === undefined) {
      if (this.defaultSessionPolicy === undefined) {
        throw new RuntimeError(
          "ENGINE_UNAVAILABLE",
          "Daemon default session policy is not configured",
          503
        );
      }
      const resolved = await this.defaultSessionPolicy.resolve({
        projectId: request.projectId,
        persona,
        mode,
        agentType: rosterEntry.type,
        ...(modelSelection === undefined ? {} : { modelSelection })
      });
      role = resolved.role;
      engineSelection = resolved.engineSelection;
      reasoningEffort = resolved.reasoningEffort;
      // A policy that cannot validate the request must not quietly fall back to its default.
      if (modelSelection !== undefined && (engineSelection.model !== modelSelection.model || reasoningEffort !== modelSelection.reasoningEffort)) {
        throw new RuntimeError("INVALID_REQUEST", "modelSelection is not supported by this project's session policy", 400, { reason: "MODEL_SELECTION_UNSUPPORTED", model: modelSelection.model, reasoningEffort: modelSelection.reasoningEffort });
      }
    }
    if (role === "agent2") {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        "Agent 2 sessions may be created only by the governed Agent 1 coordinator",
        403
      );
    }
    // Codex is the sole engine (D-GOV-43); manifests written before the
    // re-platform list other adapters and must not lock the user out.
    if (engineSelection.adapterId !== CODEX_ENGINE_ADAPTER_ID && !project.enabledAdapterIds.includes(engineSelection.adapterId)) {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        `Engine adapter is not enabled for project ${request.projectId}: ${engineSelection.adapterId}`,
        403
      );
    }
    const expectedRole = rosterEntry.type === 0 ? "agent0" : "agent1";
    if (role !== expectedRole) {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        "Explicit role conflicts with the persona authority contract",
        403
      );
    }
    const created = await this.sessions.create({
      ...request,
      role,
      engineSelection,
      ...(reasoningEffort === undefined ? {} : { reasoningEffort }),
      persona,
      mode
    });
    if (selectedRoleId === undefined && request.selectedMethods === undefined && request.interactionMode === undefined && request.permissionMode === undefined) return created;
    const roleId = selectedRoleId ?? (role === "agent0" ? "HELP_HUMAN" : "WORKING_ITEMS");
    const seeded = { ...created, schemaVersion: "chirality.session/v3" as const, roleId,
      interactionMode: request.interactionMode ?? "chat", permissionMode: request.permissionMode ?? "ask",
      selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis-pending" };
    const resolved = await this.methods.resolveForTurn(request.projectId, seeded, { methods: request.selectedMethods ?? [] });
    const updated = { ...seeded, selectedMethods: resolved.response.methods.map(value => ({ sourceRootId: value.sourceRootId, source: value.source, kind: value.kind, name: value.name })), instructionBasisId: resolved.response.basisPreview.id };
    await this.sessions.update(updated);
    return updated;
  }

  listRoles(projectId: string) { return this.methods.listRoles(projectId); }
  listMethods(projectId: string) { return this.methods.listMethods(projectId); }
  inspectMethod(projectId: string, qualifiedId: string) { return this.methods.inspectMethod(projectId, qualifiedId); }
  resolveSelectedContext(projectId: string, sessionId: string, request: import("@chirality/runtime-contracts").ResolveSelectedContextRequest) { return this.methods.resolveSelectedContext(projectId, sessionId, request); }
  replaceSelectedMethods(projectId: string, sessionId: string, request: import("@chirality/runtime-contracts").ReplaceSelectedMethodsRequest) { return this.methods.replaceSelectedMethods(projectId, sessionId, request); }
  getNativePlanCapability(projectId: string, sessionId: string) { return this.methods.getNativePlanCapability(projectId, sessionId); }
  listNativePlanRevisions(projectId: string, sessionId: string) { return this.methods.listNativePlanRevisions(projectId, sessionId); }
  listNativePlanClarifications(projectId: string, sessionId: string) { return this.methods.listNativePlanClarifications(projectId, sessionId); }
  replyNativePlanClarification(projectId: string, sessionId: string, request: import("@chirality/runtime-contracts").ReplyNativePlanClarificationRequest) { return this.methods.replyNativePlanClarification(projectId, sessionId, request); }
  exportNativePlan(projectId: string, sessionId: string, request: import("@chirality/runtime-contracts").ExportNativePlanRequest) { return this.methods.exportNativePlan(projectId, sessionId, request); }

  async bootSession(projectId: string, sessionId: string, opts: HarnessOpts = {}, expectedSelection?: EngineSelection, signal?: AbortSignal): Promise<SessionBootResponse> {
    const key = `${projectId}:${sessionId}`;
    if (this.bootingSessions.has(key)) throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session boot is still settling", 409, { sessionId });
    this.bootingSessions.add(key);
    try { return await this.performBootSession(projectId, sessionId, opts, expectedSelection, signal); }
    finally { this.bootingSessions.delete(key); }
  }

  private async performBootSession(
    projectId: string,
    sessionId: string,
    opts: HarnessOpts = {},
    expectedSelection?: EngineSelection,
    signal?: AbortSignal
  ): Promise<SessionBootResponse> {
    let session = await this.sessions.get(projectId, sessionId);
    if (
      expectedSelection !== undefined &&
      (expectedSelection.adapterId !== session.engineSelection.adapterId ||
        expectedSelection.providerId !== session.engineSelection.providerId ||
        expectedSelection.model !== session.engineSelection.model)
    ) {
      throw new RuntimeError(
        "ENGINE_UNAVAILABLE",
        "Session engine selection changed before boot",
        409,
        { expectedSelection, actualSelection: session.engineSelection }
      );
    }
    const project = await this.projects.requireAuthorized(projectId);
    const persona = opts.persona ?? session.persona;
    // A v3 session boots under its persisted permission mode, exactly as its
    // turns do (TurnCoordinator). The legacy chat `mode` (PORTAL, ...) is not a
    // permission mode and only remains the fallback for pre-v3 sessions.
    const mode = session.permissionMode ?? opts.mode ?? session.mode;
    if (session.schemaVersion === "chirality.session/v3") {
      const role = (await this.methods.listRoles(projectId)).roles.find(value => value.id === session.roleId);
      if (role === undefined || !role.directEntry || persona !== role.id) throw new HarnessError("INVALID_REQUEST", 400, `Persona '${persona}' is not available for direct chat`);
    } else if (persona.trim().toUpperCase() !== "UNTYPED") {
      const roster = await this.listAgents(projectId, true);
      if (!roster.some((agent) => agent.name === persona)) {
        throw new HarnessError(
          "INVALID_REQUEST",
          400,
          `Persona '${persona}' is not available for direct chat`
        );
      }
    }
    const engine = this.engines.resolve(session.engineSelection);
    if (engine.descriptor.boot === "none") {
      // No boot turn: the engine keeps a durable provider thread per session
      // and starts it with the first real turn. Readiness is recorded now.
      const bootedAt = new Date().toISOString();
      const fingerprint = this.runtimeFingerprint(engine, session.engineSelection);
      const bootFingerprint = sha256(JSON.stringify([project.manifestHash, session.persona, session.mode, fingerprint]));
      const updated = { ...session, bootFingerprint, runtimeFingerprint: fingerprint, bootedAt };
      await this.sessions.update(updated);
      return {
        session: updated,
        boot: {
          ...(session.engineSessionId === undefined ? {} : { engineSessionId: session.engineSessionId }),
          adapterId: session.engineSelection.adapterId,
          providerId: session.engineSelection.providerId,
          model: session.engineSelection.model,
          bootFingerprint,
          runtimeFingerprint: fingerprint,
          bootedAt
        }
      };
    }
    const turnId = randomUUID();
    const resolvedContext = session.schemaVersion === "chirality.session/v3" ? await this.methods.resolveForTurn(projectId, session) : undefined;
    const requestedTools = opts.tools ?? [];
    const admittedTools = resolvedContext === undefined ? requestedTools : await this.methods.restrictRequestedTools(projectId, resolvedContext.response.roleId, session.permissionMode, resolvedContext.response.methods, requestedTools);
    const input: AgentEngineRunInput = {
      projectId,
      session,
      // Boot is a real adapter turn with a reserved compatibility message.
      // Production adapters use this value to distinguish an attributed boot
      // from an ordinary turn while still carrying Runtime's frozen context.
      message: "bootstrap",
      ...(signal === undefined ? {} : { signal }),
      interactionMode: session.interactionMode ?? "chat",
      opts: {
        model: opts.model ?? session.engineSelection.model,
        tools: admittedTools,
        maxTurns: opts.maxTurns ?? 1,
        persona,
        mode,
        ...(opts.subagentGovernance === undefined
          ? {}
          : { subagentGovernance: opts.subagentGovernance })
      },
      turnId,
      ...(resolvedContext === undefined ? {} : {
        instructionContext: resolvedContext.response,
        runtimeTools: await this.methods.restrictRuntimeTools(projectId, resolvedContext.response.roleId, session.permissionMode, resolvedContext.response.methods, this.methods.runtimeTools(projectId, sessionId, turnId, admittedTools))
      }),
      ...(session.adapterSession?.contextSuccessor === undefined ? {} : { contextSuccessor: session.adapterSession.contextSuccessor })
    };
    if (resolvedContext !== undefined) await this.sessions.commitWithAcceptedTurn(session, { sessionId, turnId, type: "turn.accepted", data: { message: input.message, boot: true } }, resolvedContext.snapshot);
    const failBoot = async (error: unknown): Promise<void> => {
      if (resolvedContext === undefined) return;
      const failure = error instanceof Error ? error : new Error("Boot failed");
      const details = describeFailureDetails(error);
      await this.sessions.appendEvent(projectId, { sessionId, turnId, type: "turn.failed", data: { code: error instanceof RuntimeError ? error.code : "ENGINE_UNAVAILABLE", message: failure.message, boot: true, ...(details ? { details } : {}) } }).catch(() => undefined);
      const current = await this.sessions.get(projectId, sessionId);
      const adapterSession = { ...(current.adapterSession ?? {}) };
      delete adapterSession.contextSuccessor;
      await this.sessions.update({ ...current, status: "failed", adapterSession }).catch(() => undefined);
      if (input.contextSuccessor !== undefined) {
        await engine.cancelContextSuccessor?.(input.contextSuccessor.preparationId).catch(() => undefined);
        await this.sessions.failProviderSpanPreparation(projectId, sessionId, input.contextSuccessor.preparationId, { code: error instanceof RuntimeError ? error.code : "BOOT_FAILED", message: failure.message }).catch(() => undefined);
      }
    };
    const cancelled = () => new RuntimeError("ENGINE_UNAVAILABLE", "Session boot was cancelled before completion", 503, { reason: "BOOT_CANCELLED", sessionId });
    try { if (signal?.aborted) throw cancelled(); await engine.preflight(input); } catch (error) { await failBoot(error); throw error; }
    let engineSessionId: string | undefined;
    let adapterId: string | undefined;
    let providerId: string | undefined;
    let model: string | undefined;
    let claudeSessionId: string | undefined;
    let processExit: Extract<UIEvent, { type: "process:exit" }> | undefined;
    let terminalHarnessEvent: HarnessEvent | undefined;
    let fatalTurnError = false;
    let eventIndex = 0;
    const harnessEvents: HarnessEvent[] = [];
    let interruption: Promise<void> | undefined;
    let interruptionError: unknown;
    const interrupt = () => { if (!engine.handlesAbortSignal) interruption ??= engine.interrupt(sessionId).catch(error => { interruptionError = error; }); };
    signal?.addEventListener("abort", interrupt, { once: true });
    try { for await (const event of engine.startTurn(input)) {
      if (signal?.aborted) interrupt();
      if (processExit !== undefined) {
        throw new HarnessError(
          "SDK_FAILURE",
          502,
          "Boot engine emitted an event after process:exit"
        );
      }
      if (eventIndex === 0 && event.type !== "session:init") {
        throw new HarnessError(
          "SDK_FAILURE",
          502,
          "Boot engine must emit session:init first"
        );
      }
      if (event.type === "harness:event") {
        if (
          event.data.sessionId !== sessionId ||
          (event.data.turnId !== undefined && event.data.turnId !== input.turnId)
        ) {
          throw new HarnessError(
            "SDK_FAILURE",
            502,
            "Boot engine emitted an event outside the active session or turn"
          );
        }
        if (
          ["turn.completed", "turn.failed", "turn.cancelled", "turn.interrupted"].includes(
            event.data.type
          )
        ) {
          if (terminalHarnessEvent !== undefined) {
            throw new HarnessError(
              "SDK_FAILURE",
              502,
              "Boot engine emitted multiple terminal harness events"
            );
          }
          terminalHarnessEvent = event.data;
        }
        harnessEvents.push(event.data);
      }
      if (event.type === "session:init") {
        if (eventIndex !== 0 || engineSessionId !== undefined) {
          throw new HarnessError(
            "SDK_FAILURE",
            502,
            "Boot engine emitted multiple or out-of-order session:init events"
          );
        }
        if (
          event.data.engineSessionId.trim() === "" ||
          event.data.adapterId !== engine.descriptor.adapterId ||
          event.data.providerId !== engine.descriptor.providerId ||
          event.data.model !== input.opts.model
        ) {
          throw new HarnessError(
            "SDK_FAILURE",
            502,
            "Boot engine initialization attribution does not match the selected adapter"
          );
        }
        engineSessionId = event.data.engineSessionId;
        adapterId = event.data.adapterId;
        providerId = event.data.providerId;
        model = event.data.model;
        claudeSessionId =
          providerId === "anthropic" ? event.data.claudeSessionId : undefined;
        if (input.contextSuccessor !== undefined) await this.sessions.recordProviderSpanSessionInit(projectId, sessionId, input.contextSuccessor.preparationId, { sessionInitEventId: randomUUID(), engineSessionId: event.data.engineSessionId, providerSpanId: event.data.providerSpanId ?? event.data.engineSessionId });
      }
      if (event.type === "turn:error" && event.data.fatal) {
        fatalTurnError = true;
      }
      if (event.type === "process:exit") {
        processExit = event;
      }
      eventIndex += 1;
    } } catch (error) { await failBoot(error); throw error; }
    finally { signal?.removeEventListener("abort", interrupt); await interruption; }
    if (interruptionError !== undefined) { await failBoot(interruptionError); throw interruptionError; }
    if (
      processExit === undefined ||
      processExit.data.exitCode !== 0 ||
      fatalTurnError ||
      engineSessionId === undefined ||
      adapterId === undefined ||
      providerId === undefined ||
      model === undefined ||
      (terminalHarnessEvent !== undefined &&
        terminalHarnessEvent.type !== "turn.completed")
    ) {
      const failure = signal?.aborted && processExit?.data.interrupted === true
        ? new RuntimeError("ENGINE_UNAVAILABLE", "Session boot was interrupted before completion", 503, {
            reason: signal.reason?.name === "TimeoutError" ? "BOOT_TIMEOUT" : "BOOT_CANCELLED", operation: "boot", sessionId
          })
        : new HarnessError("SDK_FAILURE", 500, "Boot turn did not initialize and complete a conformant engine session",
            processExit === undefined ? undefined : { exitCode: processExit.data.exitCode });
      await failBoot(failure);
      throw failure;
    }
    for (const event of harnessEvents) {
      await this.sessions.persistEvent(projectId, event);
    }
    const bootedAt = new Date().toISOString();
    const fingerprint = this.runtimeFingerprint(engine, { adapterId, providerId, model });
    const bootFingerprint = sha256(
      JSON.stringify([project.manifestHash, session.persona, session.mode, fingerprint])
    );
    const updated = {
      ...session,
      engineSessionId,
      engineSelection: { adapterId, providerId, model },
      adapterSession: {
        ...session.adapterSession,
        engineSessionId,
        packageName: engine.descriptor.packageName,
        packageVersion: engine.descriptor.packageVersion
      },
      ...(providerId === "anthropic" && claudeSessionId !== undefined
        ? { claudeSessionId }
        : {}),
      bootFingerprint,
      runtimeFingerprint: fingerprint,
      bootedAt
    };
    if (updated.adapterSession !== undefined) delete updated.adapterSession.contextSuccessor;
    if (input.contextSuccessor !== undefined) {
      delete updated.sdkSessionId;
      delete updated.sdkTranscriptPath;
      delete updated.sdkSessionStoreKey;
      if (claudeSessionId === undefined) delete updated.claudeSessionId;
    }
    await this.sessions.update(updated);
    return {
      session: updated,
      boot: {
        engineSessionId,
        adapterId,
        providerId,
        model,
        bootFingerprint,
        runtimeFingerprint: fingerprint,
        bootedAt,
        ...(updated.claudeSessionId === undefined
          ? {}
          : { claudeSessionId: updated.claudeSessionId })
      }
    };
  }

  private runtimeFingerprint(engine: ReturnType<EngineRegistry["resolve"]>, attribution: { adapterId: string; providerId: string; model: string }): SessionBootResponse["boot"]["runtimeFingerprint"] {
    const { adapterId, providerId, model } = attribution;
    const fingerprint = {
      schemaVersion: "chirality.runtime-fingerprint/v2",
      personaComposerVersion: "shared-runtime/v1",
      permissionPolicyVersion: "shared-runtime/v1",
      managedDelegationPolicyVersion: "shared-runtime/v1",
      subagentPolicyVersion: "shared-runtime/v1",
      toolRegistryVersion: "shared-runtime/v1",
      sdkPackageVersion: engine.descriptor.packageVersion ?? "embedded",
      engineAdapter: {
        adapterId,
        providerId,
        model,
        ...(engine.descriptor.packageName === undefined
          ? {}
          : { packageName: engine.descriptor.packageName }),
        ...(engine.descriptor.packageVersion === undefined
          ? {}
          : { packageVersion: engine.descriptor.packageVersion })
      },
      mcpServers: [],
      fingerprintSha256: ""
    };
    fingerprint.fingerprintSha256 = sha256(JSON.stringify(fingerprint));
    return fingerprint;
  }

  async listAgents(
    projectId: string,
    directChatOnly = false
  ): Promise<readonly AgentDefinitionSummary[]> {
    const roots = await this.projects.roots(projectId);
    const directory = join(roots.instructionRoot, "agents");
    const agents: AgentDefinitionSummary[] = [];
    for (const entry of await readdir(directory).catch(() => [])) {
      const match = /^AGENT_(.+)\.md$/u.exec(entry);
      if (match?.[1] === undefined) continue;
      const path = await realpath(join(directory, entry)).catch(() => undefined);
      if (path === undefined || !isContained(roots.instructionRoot, path)) continue;
      const source = await readFile(path, "utf8").catch(() => undefined);
      if (source === undefined) continue;
      const typeMatch =
        /AGENT_TYPE\s*:\s*(?:TYPE\s*)?([012])\b/iu.exec(source) ??
        /\|\s*\*\*AGENT_TYPE\*\*\s*\|\s*TYPE\s*([012])\s*\|/iu.exec(source);
      const classMatch =
        /AGENT_CLASS\s*:\s*([^\n|]+)/iu.exec(source) ??
        /\|\s*\*\*AGENT_CLASS\*\*\s*\|\s*([^|]+)\|/iu.exec(source);
      const type =
        typeMatch?.[1] === undefined ? undefined : (Number(typeMatch[1]) as 0 | 1 | 2);
      if (directChatOnly && type !== 0 && type !== 1) continue;
      agents.push({
        name: match[1],
        ...(type === undefined ? {} : { type }),
        ...(classMatch?.[1] === undefined ? {} : { class: classMatch[1].trim() })
      });
    }
    return agents.sort((left, right) => left.name.localeCompare(right.name));
  }

  async scaffold(projectId: string, request: ScaffoldRequest) {
    await this.projects.requireAuthorized(projectId);
    if (this.scaffoldPort === undefined) {
      throw new RuntimeError("ENGINE_UNAVAILABLE", "Project scaffold adapter is unavailable", 501);
    }
    return this.scaffoldPort.scaffold(projectId, request);
  }

  async decidePermission(
    projectId: string,
    sessionId: string,
    request: PermissionDecisionRequest
  ): Promise<void> {
    if (this.permissions === undefined) {
      throw new RuntimeError(
        "ENGINE_UNAVAILABLE",
        "No active permission broker is configured",
        409
      );
    }
    await this.permissions.submit(projectId, sessionId, request);
  }

  async interruptSession(projectId: string, sessionId: string, reason?: string): Promise<void> {
    await Promise.all([
      this.turns.interrupt(projectId, sessionId, reason),
      this.agent1Runs?.interrupt?.(projectId, sessionId) ?? Promise.resolve()
    ]);
  }

  runSessionTurn(
    projectId: string,
    sessionId: string,
    request: SessionTurnRequest
  ): AsyncIterable<UIEvent> {
    if (this.agent1Runs?.isActive?.(projectId, sessionId) === true) {
      throw new RuntimeError(
        "SESSION_TURN_IN_PROGRESS",
        "Session is reserved by an active governed Agent 1 run",
        409
      );
    }
    return this.turns.run(projectId, sessionId, request);
  }

  runAgent1(projectId: string, request: Agent1RunRequest): AsyncIterable<UIEvent> {
    if (this.agent1Runs === undefined) {
      throw new RuntimeError(
        "REQUIRED_DELEGATION_MISSING",
        "No governed Agent 1 runner is configured",
        409
      );
    }
    return this.agent1Runs.run(projectId, request);
  }
}
