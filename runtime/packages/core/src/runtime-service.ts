import { randomUUID } from "node:crypto";
import { readdir, readFile, realpath, stat } from "node:fs/promises";
import { basename, join, relative, resolve } from "node:path";
import {
  HarnessError,
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
  }): Promise<{ role: "agent0" | "agent1"; engineSelection: EngineSelection }>;
}

export class RuntimeService {
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
    private readonly defaultSessionPolicy?: DefaultSessionPolicy
  ) {}

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
    const persona = request.persona ?? "UNTYPED";
    const mode = request.mode ?? "direct";
    const roster = await this.listAgents(request.projectId, true);
    const rosterEntry =
      persona.trim().toUpperCase() === "UNTYPED"
        ? { name: persona, type: 1 as const }
        : roster.find((entry) => entry.name === persona);
    if (rosterEntry?.type !== 0 && rosterEntry?.type !== 1) {
      throw new HarnessError(
        "INVALID_REQUEST",
        400,
        `Persona '${persona}' is not available for direct chat`
      );
    }
    let role = request.role;
    let engineSelection = request.engineSelection;
    if ((role === undefined) !== (engineSelection === undefined)) {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Explicit role and engineSelection must be supplied together"
      );
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
        agentType: rosterEntry.type
      });
      role = resolved.role;
      engineSelection = resolved.engineSelection;
    }
    if (role === "agent2") {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        "Agent 2 sessions may be created only by the governed Agent 1 coordinator",
        403
      );
    }
    if (!project.enabledAdapterIds.includes(engineSelection.adapterId)) {
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
    return this.sessions.create({
      ...request,
      role,
      engineSelection,
      persona,
      mode
    });
  }

  async bootSession(
    projectId: string,
    sessionId: string,
    opts: HarnessOpts = {},
    expectedSelection?: EngineSelection
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
    const mode = opts.mode ?? session.mode;
    if (persona.trim().toUpperCase() !== "UNTYPED") {
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
    const input: AgentEngineRunInput = {
      session,
      message: "",
      opts: {
        model: opts.model ?? session.engineSelection.model,
        tools: opts.tools ?? [],
        maxTurns: opts.maxTurns ?? 1,
        persona,
        mode,
        ...(opts.subagentGovernance === undefined
          ? {}
          : { subagentGovernance: opts.subagentGovernance })
      },
      turnId: randomUUID()
    };
    await engine.preflight(input);
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
    for await (const event of engine.startTurn(input)) {
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
      }
      if (event.type === "turn:error" && event.data.fatal) {
        fatalTurnError = true;
      }
      if (event.type === "process:exit") {
        processExit = event;
      }
      eventIndex += 1;
    }
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
      throw new HarnessError(
        "SDK_FAILURE",
        500,
        "Boot turn did not initialize and complete a conformant engine session",
        processExit === undefined ? undefined : { exitCode: processExit.data.exitCode }
      );
    }
    for (const event of harnessEvents) {
      await this.sessions.persistEvent(projectId, event);
    }
    const bootedAt = new Date().toISOString();
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

  async interruptSession(projectId: string, sessionId: string): Promise<void> {
    await Promise.all([
      this.turns.interrupt(projectId, sessionId),
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
