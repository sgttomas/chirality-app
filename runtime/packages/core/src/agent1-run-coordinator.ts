import { randomUUID } from "node:crypto";
import { constants, type BigIntStats } from "node:fs";
import { lstat, open, readFile, realpath } from "node:fs/promises";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import {
  RuntimeError,
  type Agent1RunRequest,
  type EngineSelection,
  type RuntimeSessionRecord,
  type RuntimeToolDefinition,
  type UIEvent
} from "@chirality/runtime-contracts";
import { atomicWriteJson, isContained, sha256 } from "./fs.js";
import type { ProjectRegistry } from "./project-registry.js";
import type { ResidencyCoordinator } from "./residency-coordinator.js";
import type { SessionStore } from "./session-store.js";
import type { RequiredToolReceipt, TurnCoordinator } from "./turn-coordinator.js";

export interface Agent2Return {
  childSessionId: string;
  returnText: string;
  model: string;
  residencyEpoch: string;
}

export interface Agent1ManagerHooks {
  delegate(input: { sealedBrief: string }): Promise<Agent2Return>;
  review(input: {
    childSessionId: string;
    decision: "accepted" | "rejected";
    rationale: string;
  }): Promise<void>;
}

export interface Agent1ManagerRuntimePort {
  execute(
    session: RuntimeSessionRecord,
    request: Agent1RunRequest,
    hooks: Agent1ManagerHooks,
    signal: AbortSignal
  ): AsyncIterable<UIEvent>;
  interrupt?(sessionId: string): Promise<void>;
}

export interface RuntimeToolBindingPort {
  bind(sessionId: string, tools: readonly RuntimeToolDefinition[]): Promise<() => Promise<void>>;
}

export interface GovernedAgent1RunOptions {
  hookDrainTimeoutMs?: number;
  /** Absolute Runtime control and transcript roots excluded from bound reads. */
  protectedPaths?: readonly string[];
  projects: ProjectRegistry;
  sessions: SessionStore;
  turns: TurnCoordinator;
  residency: ResidencyCoordinator;
  manager: Agent1ManagerRuntimePort;
  tools: RuntimeToolBindingPort;
  resolveManagerSelection(projectId: string): Promise<EngineSelection>;
}

interface AgentRunRecord {
  schemaVersion: "chirality.agent-run/v1";
  runId: string;
  projectId: string;
  managerSessionId: string;
  managerAgentId: string;
  managerSelection: EngineSelection;
  sealedBrief: string;
  briefHash: string;
  child?: {
    sessionId: string;
    role: "agent2";
    selection: EngineSelection;
    residencyEpoch: string;
    sealedBrief: string;
    sealedBriefHash: string;
    returnHash?: string;
    evidenceReference?: {
      projectId: string;
      sessionId: string;
      source: "canonical-session-events";
    };
    acceptance?: {
      decision: "accepted" | "rejected";
      rationaleHash: string;
    };
    permissions: ["read"];
    tool: "read_file";
    status: "launched" | "completed" | "failed" | "interrupted";
  };
  review?: {
    decision: "accepted" | "rejected";
    rationaleHash: string;
  };
  status: "running" | "completed" | "failed" | "interrupted";
  failureCode?: string;
  reconciliationRequired?: boolean;
  progressRecordedAt?: string;
  approvalReference: string;
  createdAt: string;
  completedAt?: string;
}

export class GovernedAgent1RunCoordinator {
  private readonly active = new Map<
    string,
    { projectId: string; controller: AbortController; childSessionId?: string }
  >();

  constructor(private readonly options: GovernedAgent1RunOptions) {
    const timeout = options.hookDrainTimeoutMs ?? 5000;
    if (!Number.isSafeInteger(timeout) || timeout < 1 || timeout > 30000) throw new RuntimeError("INVALID_REQUEST", "Invalid manager hook drain bound");
  }

  isActive(projectId: string, sessionId: string): boolean {
    return this.active.get(sessionId)?.projectId === projectId;
  }

  async interrupt(projectId: string, sessionId: string): Promise<void> {
    const active = this.active.get(sessionId);
    if (active === undefined || active.projectId !== projectId) return;
    active.controller.abort();
    await Promise.all([
      this.options.manager.interrupt?.(sessionId) ?? Promise.resolve(),
      active.childSessionId === undefined
        ? Promise.resolve()
        : this.options.turns.interrupt(projectId, active.childSessionId)
    ]);
  }

  async *run(projectId: string, request: Agent1RunRequest): AsyncIterable<UIEvent> {
    const project = await this.options.projects.requireAuthorized(projectId);
    if (request.brief.trim() === "") {
      throw new RuntimeError("INVALID_REQUEST", "Agent 1 brief cannot be empty");
    }
    if (request.approvalReference.trim() === "") {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Agent 1 approvalReference cannot be empty"
      );
    }
    const managerAgentId = request.agentId ?? "WORKING_ITEMS";
    const managerDefinition = (await this.listManagerDefinitions(projectId)).find(
      (agent) => agent.agentId === managerAgentId
    );
    if (managerDefinition === undefined || managerDefinition.agentType !== 1) {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        `Direct run target must be an Agent 1: ${managerAgentId}`,
        403
      );
    }
    const managerSelection = await this.options.resolveManagerSelection(projectId);
    if (!project.enabledAdapterIds.includes(managerSelection.adapterId)) {
      throw new RuntimeError(
        "DELEGATION_POLICY_VIOLATION",
        `Agent 1 adapter is not enabled for project ${projectId}: ${managerSelection.adapterId}`,
        403
      );
    }
    const managerSession = await this.options.sessions.create({
      projectId,
      role: "agent1",
      engineSelection: managerSelection,
      persona: managerAgentId,
      mode: "direct"
    });
    const turnId = randomUUID();
    const runId = randomUUID();
    const createdAt = new Date().toISOString();
    const controller = new AbortController();
    this.active.set(managerSession.sessionId, { projectId, controller });
    let managerActualSelection = managerSelection;
    let child:
      | {
          sessionId: string;
          selection: EngineSelection;
          epoch: string;
          sealedBrief: string;
          sealedBriefHash: string;
          returnHash?: string;
          evidenceReference?: {
            projectId: string;
            sessionId: string;
            source: "canonical-session-events";
          };
          acceptance?: {
            decision: "accepted" | "rejected";
            rationaleHash: string;
          };
          status: "launched" | "completed" | "failed" | "interrupted";
        }
      | undefined;
    let reviewClaimed = false;
    let delegationClaimed = false; // A consumed admission attempt is never reset after asynchronous failure.
    let review: { decision: "accepted" | "rejected"; rationaleHash: string } | undefined;
    let hooksOpen = true;
    const pendingHooks = new Set<Promise<unknown>>();
    const assertHookLive = () => { if (!hooksOpen || controller.signal.aborted) throw new RuntimeError("INTERRUPTED", "Manager hook authority has ended", 499); };
    const trackHook = <T>(operation: () => Promise<T>): Promise<T> => {
      assertHookLive();
      const promise = operation(); pendingHooks.add(promise);
      void promise.then(() => pendingHooks.delete(promise), () => pendingHooks.delete(promise));
      return promise;
    };
    let persistence: Promise<void> = Promise.resolve();
    const persistHook = (record: AgentRunRecord): Promise<void> => {
      const next = persistence.then(async () => { assertHookLive(); await this.persistAgentProgress(projectId, runId, record); });
      persistence = next.catch(() => undefined);
      return next;
    };
    await this.persistAgentRun(projectId, runId, {
      schemaVersion: "chirality.agent-run/v1",
      runId,
      projectId,
      managerSessionId: managerSession.sessionId,
      managerAgentId,
      managerSelection,
      sealedBrief: request.brief,
      briefHash: sha256(request.brief),
      status: "running",
      approvalReference: request.approvalReference,
      createdAt
    });
    const accepted = await this.options.sessions.appendEvent(projectId, {
      sessionId: managerSession.sessionId,
      turnId,
      type: "turn.accepted",
      data: { runId, agentId: managerAgentId, briefHash: sha256(request.brief) }
    });
    try {
      yield { type: "harness:event", data: accepted };
      const rawHooks: Agent1ManagerHooks = {
      delegate: async ({ sealedBrief }) => {
        assertHookLive();
        if (controller.signal.aborted) {
          throw new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499);
        }
        if (request.localModel === undefined) {
          throw new RuntimeError(
            "DELEGATION_POLICY_VIOLATION",
            "This run did not authorize a local child",
            403
          );
        }
        if (delegationClaimed) {
          throw new RuntimeError(
            "DELEGATION_POLICY_VIOLATION",
            "Agent 1 may launch at most one local child in this milestone",
            403
          );
        }
        // Reserve synchronously before residency, storage or tool binding can yield.
        delegationClaimed = true;
        if (request.readOnlyTool?.name !== "read_file") {
          throw new RuntimeError(
            "DELEGATION_POLICY_VIOLATION",
            "Local child requires one declared read_file tool",
            403
          );
        }
        const residency = await this.options.residency.status();
        if (
          residency.phase !== "READY" ||
          residency.managedModelId !== request.localModel ||
          residency.epoch === undefined
        ) {
          throw new RuntimeError(
            "MODEL_NOT_RESIDENT",
            `Exact local model is not resident: ${request.localModel}`,
            409
          );
        }
        const selection: EngineSelection = {
          adapterId: "pi",
          providerId: "omlx",
          model: request.localModel
        };
        if (!project.enabledAdapterIds.includes(selection.adapterId)) {
          throw new RuntimeError(
            "DELEGATION_POLICY_VIOLATION",
            "Pi is not enabled by the registered project manifest",
            403
          );
        }
        assertHookLive();
        const childSession = await this.options.sessions.create({
          projectId,
          role: "agent2",
          engineSelection: selection,
          persona: "TASK",
          mode: "readOnly",
          parentSessionId: managerSession.sessionId,
          approvalRef: request.approvalReference,
          allowedWriteTargets: []
        });
        child = {
          sessionId: childSession.sessionId,
          selection,
          epoch: residency.epoch.epochId,
          sealedBrief,
          sealedBriefHash: sha256(sealedBrief),
          status: "launched"
        };
        const active = this.active.get(managerSession.sessionId);
        if (active !== undefined) active.childSessionId = child.sessionId;
        assertHookLive();
        await persistHook({
          schemaVersion: "chirality.agent-run/v1",
          runId,
          projectId,
          managerSessionId: managerSession.sessionId,
          managerAgentId,
          managerSelection: managerActualSelection,
          sealedBrief: request.brief,
          briefHash: sha256(request.brief),
          child: {
            sessionId: child.sessionId,
            role: "agent2",
            selection: child.selection,
            residencyEpoch: child.epoch,
            sealedBrief: child.sealedBrief,
            sealedBriefHash: child.sealedBriefHash,
            permissions: ["read"],
            tool: "read_file",
            status: child.status
          },
          status: "running",
          approvalReference: request.approvalReference,
          createdAt
        });
        const childTurnId = randomUUID();
        const { tool, receipt } = await this.readFileTool({
          projectId,
          projectRoot: project.canonicalRoot,
          sessionId: childSession.sessionId,
          turnId: childTurnId,
          relativePath: request.readOnlyTool.relativePath
        });
        assertHookLive();
        const release = await this.options.tools.bind(childSession.sessionId, [tool]);
        const interruptChild = (): void => {
          void this.options.turns
            .interrupt(projectId, childSession.sessionId)
            .catch(() => undefined);
        };
        controller.signal.addEventListener("abort", interruptChild);
        let text = "";
        let successful = false;
        let interrupted = false;
        let requiredToolFailure = false;
        try {
          if (controller.signal.aborted) {
            throw new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499);
          }
          for await (const event of this.options.turns.run(
            projectId,
            childSession.sessionId,
            { prompt: sealedBrief, turnId: childTurnId },
            ["read_file"],
            [receipt]
          )) {
            if (event.type === "chat:delta") {
              text += event.data.text;
            } else if (event.type === "chat:complete") {
              text = event.data.text;
            }
            if (
              event.type === "harness:event" &&
              (event.data.type === "turn.interrupted" ||
                event.data.type === "turn.cancelled")
            ) {
              interrupted = true;
            }
            if (
              event.type === "turn:error" &&
              (event.data.details as { runtimeCode?: unknown } | undefined)
                ?.runtimeCode === "REQUIRED_DELEGATION_MISSING"
            ) {
              requiredToolFailure = true;
            }
            if (event.type === "process:exit") successful = event.data.exitCode === 0;
          }
        } catch (error) {
          child.status = controller.signal.aborted ? "interrupted" : "failed";
          throw error;
        } finally {
          controller.signal.removeEventListener("abort", interruptChild);
          await release();
        }
        if (!successful || interrupted || controller.signal.aborted) {
          child.status =
            interrupted || controller.signal.aborted ? "interrupted" : "failed";
          throw interrupted || controller.signal.aborted
            ? new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499)
            : requiredToolFailure
              ? new RuntimeError(
                  "REQUIRED_DELEGATION_MISSING",
                  "Local child did not complete the required read_file tool",
                  422
                )
              : new RuntimeError("ENGINE_UNAVAILABLE", "Local child did not complete", 502);
        }
        if (!receipt.completed()) {
          child.status = "failed";
          await this.options.sessions.update({
            ...(await this.options.sessions.get(projectId, childSession.sessionId)),
            status: "failed"
          });
          throw new RuntimeError(
            "REQUIRED_DELEGATION_MISSING",
            "Local child did not complete the required read_file tool",
            422
          );
        }
        const completedChild = await this.options.sessions.get(
          projectId,
          childSession.sessionId
        );
        assertHookLive();
        child.selection = completedChild.engineSelection;
        child.returnHash = sha256(text);
        child.evidenceReference = {
          projectId,
          sessionId: childSession.sessionId,
          source: "canonical-session-events"
        };
        child.status = "completed";
        await persistHook({
          schemaVersion: "chirality.agent-run/v1",
          runId,
          projectId,
          managerSessionId: managerSession.sessionId,
          managerAgentId,
          managerSelection: managerActualSelection,
          sealedBrief: request.brief,
          briefHash: sha256(request.brief),
          child: {
            sessionId: child.sessionId,
            role: "agent2",
            selection: child.selection,
            residencyEpoch: child.epoch,
            sealedBrief: child.sealedBrief,
            sealedBriefHash: child.sealedBriefHash,
            returnHash: child.returnHash,
            evidenceReference: child.evidenceReference,
            permissions: ["read"],
            tool: "read_file",
            status: child.status
          },
          status: "running",
          approvalReference: request.approvalReference,
          createdAt
        });
        return {
          childSessionId: childSession.sessionId,
          returnText: text,
          model: request.localModel,
          residencyEpoch: residency.epoch.epochId
        };
      },
      review: async (input) => {
        assertHookLive();
        if (!input || !["accepted", "rejected"].includes(input.decision) || typeof input.rationale !== "string" || !input.rationale.trim() || input.rationale.length > 65536) throw new RuntimeError("INVALID_REQUEST", "Invalid child review");
        if (reviewClaimed || child === undefined || input.childSessionId !== child.sessionId || child.status !== "completed" || child.returnHash === undefined || child.evidenceReference === undefined) {
          throw new RuntimeError(
            "DELEGATION_POLICY_VIOLATION",
            "Review must refer to this manager's governed child",
            403
          );
        }
        reviewClaimed = true;
        review = {
          decision: input.decision,
          rationaleHash: sha256(input.rationale)
        };
        child.acceptance = review;
        const event = await this.options.sessions.appendEvent(projectId, {
          sessionId: managerSession.sessionId,
          turnId,
          type: "coordination.acknowledged",
          data: {
            childSessionId: child.sessionId,
            decision: input.decision,
            rationaleHash: review.rationaleHash
          }
        });
        assertHookLive();
        await this.options.sessions.persistEvent(projectId, event);
        await persistHook({
          schemaVersion: "chirality.agent-run/v1",
          runId,
          projectId,
          managerSessionId: managerSession.sessionId,
          managerAgentId,
          managerSelection: managerActualSelection,
          sealedBrief: request.brief,
          briefHash: sha256(request.brief),
          child: {
            sessionId: child.sessionId,
            role: "agent2",
            selection: child.selection,
            residencyEpoch: child.epoch,
            sealedBrief: child.sealedBrief,
            sealedBriefHash: child.sealedBriefHash,
            ...(child.returnHash === undefined ? {} : { returnHash: child.returnHash }),
            ...(child.evidenceReference === undefined
              ? {}
              : { evidenceReference: child.evidenceReference }),
            acceptance: child.acceptance,
            permissions: ["read"],
            tool: "read_file",
            status: child.status
          },
          review,
          status: "running",
          approvalReference: request.approvalReference,
          createdAt
        });
      }
      };
      const hooks: Agent1ManagerHooks = {
        delegate: input => trackHook(() => rawHooks.delegate(input)),
        review: input => trackHook(() => rawHooks.review(input))
      };
      let failure: RuntimeError | undefined;
      try {
      for await (const event of this.options.manager.execute(
        managerSession,
        request,
        hooks,
        controller.signal
      )) {
        if (controller.signal.aborted) {
          throw new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499);
        }
        if (event.type === "process:exit") {
          throw new RuntimeError(
            "INTERNAL_FAILURE",
            "Manager runtime must leave terminal ownership to the coordinator",
            500
          );
        }
        if (
          event.type === "harness:event" &&
          ["turn.completed", "turn.failed", "turn.cancelled", "turn.interrupted"].includes(
            event.data.type
          )
        ) {
          throw new RuntimeError(
            "INTERNAL_FAILURE",
            "Manager runtime emitted a terminal harness event",
            500
          );
        }
        if (event.type === "harness:event") {
          await this.options.sessions.persistEvent(projectId, event.data);
        }
        if (event.type === "session:init") {
          managerActualSelection = {
            adapterId: event.data.adapterId,
            providerId: event.data.providerId,
            model: event.data.model
          };
        }
        yield event;
      }
      if (controller.signal.aborted) {
        failure = new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499);
      } else if (
        request.localModel !== undefined &&
        (child === undefined || child.status !== "completed" || child.returnHash === undefined || child.evidenceReference === undefined || review === undefined)
      ) {
        failure = new RuntimeError(
          "REQUIRED_DELEGATION_MISSING",
          "Agent 1 did not complete and review the required local delegation",
          409
        );
      }
      } catch (error) {
        failure = controller.signal.aborted
          ? new RuntimeError("INTERRUPTED", "Agent 1 run was interrupted", 499)
          : error instanceof RuntimeError
            ? error
            : new RuntimeError("INTERNAL_FAILURE", "Agent 1 run failed", 500);
      }
      // A manager may finish its own iterator while a callback is still executing.
      // Revoke new/late authority first, then drain the work it already launched.
      const hadPendingHooks = pendingHooks.size > 0;
      hooksOpen = false;
      let reconciliationRequired = false;
      if (failure !== undefined || hadPendingHooks) {
        failure ??= new RuntimeError("REQUIRED_DELEGATION_MISSING", "Manager returned with an unfinished callback", 409);
        controller.abort();
        const interruptions = [Promise.resolve().then(() => this.options.manager.interrupt?.(managerSession.sessionId)),
          Promise.resolve().then(() => child === undefined ? undefined : this.options.turns.interrupt(projectId, child.sessionId))];
        let timer: ReturnType<typeof setTimeout> | undefined;
        const drained = await Promise.race([
          Promise.allSettled([...pendingHooks, ...interruptions, persistence]).then(() => true),
          new Promise<false>(resolve => { timer = setTimeout(() => resolve(false), this.options.hookDrainTimeoutMs ?? 5000); })
        ]);
        clearTimeout(timer);
        reconciliationRequired = !drained;
      }
      // Queued publications are fenced; a drain timeout remains explicit reconciliation.
      if (failure !== undefined && child?.status === "launched") {
        child.status = failure.code === "INTERRUPTED" ? "interrupted" : "failed";
        const childSession = await this.options.sessions
          .get(projectId, child.sessionId)
          .catch(() => undefined);
        if (childSession !== undefined) {
          await this.options.sessions.update({
            ...childSession,
            status: child.status
          });
        }
      }
      const completedAt = new Date().toISOString();
      const record: AgentRunRecord = {
      schemaVersion: "chirality.agent-run/v1",
      runId,
      projectId,
      managerSessionId: managerSession.sessionId,
      managerAgentId,
      managerSelection: managerActualSelection,
      sealedBrief: request.brief,
      briefHash: sha256(request.brief),
      status:
        failure === undefined
          ? "completed"
          : failure.code === "INTERRUPTED"
            ? "interrupted"
            : "failed",
      approvalReference: request.approvalReference,
      createdAt,
      completedAt,
      ...(child === undefined
        ? {}
        : {
            child: {
              sessionId: child.sessionId,
              role: "agent2",
              selection: child.selection,
              residencyEpoch: child.epoch,
              sealedBrief: child.sealedBrief,
              sealedBriefHash: child.sealedBriefHash,
              ...(child.returnHash === undefined ? {} : { returnHash: child.returnHash }),
              ...(child.evidenceReference === undefined
                ? {}
                : { evidenceReference: child.evidenceReference }),
              ...(child.acceptance === undefined ? {} : { acceptance: child.acceptance }),
              permissions: ["read"],
              tool: "read_file",
              status: child.status
            }
          }),
      ...(review === undefined ? {} : { review }),
      ...(failure === undefined ? {} : { failureCode: failure.code }),
      ...(reconciliationRequired ? { reconciliationRequired: true } : {})
      };
      await this.persistAgentRun(projectId, runId, record);
      const terminal = await this.options.sessions.appendEvent(projectId, {
      sessionId: managerSession.sessionId,
      turnId,
      type:
        failure === undefined
          ? "turn.completed"
          : failure.code === "INTERRUPTED"
            ? "turn.interrupted"
            : "turn.failed",
      data:
        failure === undefined
          ? { runId }
          : { runId, code: failure.code, message: failure.message }
      });
      await this.options.sessions.update({
        ...(await this.options.sessions.get(projectId, managerSession.sessionId)),
        status:
          failure === undefined
            ? "completed"
            : failure.code === "INTERRUPTED"
              ? "interrupted"
              : "failed"
      });
      yield { type: "harness:event", data: terminal };
      if (failure !== undefined) {
        yield {
        type: "turn:error",
        data: {
          phase: "mid-stream",
          errorType: "SDK_FAILURE",
          message: failure.message,
          status: failure.status,
          severity: "error",
          fatal: true,
          details: { runtimeCode: failure.code }
        }
        };
      }
      yield {
      type: "process:exit",
      data: {
        exitCode: failure === undefined ? 0 : 1,
        ...(failure === undefined
          ? {}
          : {
              error: failure.message,
              errorType: failure.code,
              status: failure.status,
              severity: "error",
              fatal: true
            })
      }
      };
    } finally {
      hooksOpen = false;
      controller.abort();
      this.active.delete(managerSession.sessionId);
    }
  }

  private async readFileTool(input: {
    projectId: string;
    projectRoot: string;
    sessionId: string;
    turnId: string;
    relativePath: string;
  }): Promise<{ tool: RuntimeToolDefinition; receipt: RequiredToolReceipt }> {
    const { projectId, projectRoot, sessionId, turnId, relativePath } = input;
    const denied = (): RuntimeError => new RuntimeError(
      "FORBIDDEN", "read_file target left its authorized regular-file boundary", 403
    );
    const maxBytes = 1024 * 1024;
    if (!relativePath || relativePath.length > 4096 || isAbsolute(relativePath) || /[\x00-\x1f\x7f]/u.test(relativePath)) {
      throw new RuntimeError("INVALID_REQUEST", "read_file path must be relative");
    }
    const canonicalRoot = projectRoot;
    const canonicalPath = resolve(canonicalRoot, relativePath);
    if (!isAbsolute(canonicalRoot) || resolve(canonicalRoot) !== canonicalRoot ||
        !isContained(canonicalRoot, canonicalPath) || canonicalRoot === canonicalPath ||
        (this.options.protectedPaths ?? []).some((path) => isContained(resolve(path), canonicalPath))) {
      throw denied();
    }
    const sameIdentity = (a: BigIntStats, b: BigIntStats): boolean =>
      a.dev === b.dev && a.ino === b.ino && a.mode === b.mode;
    const sameFile = (a: BigIntStats, b: BigIntStats): boolean =>
      sameIdentity(a, b) && a.nlink === b.nlink && a.size === b.size &&
      a.mtimeNs === b.mtimeNs && a.ctimeNs === b.ctimeNs;
    // Pin every component at authorization. Never canonicalize a replacement
    // symlink into fresh authority, including a replacement of the project root.
    const paths = [canonicalRoot];
    for (const component of relative(canonicalRoot, canonicalPath).split(sep)) {
      paths.push(resolve(paths[paths.length - 1]!, component));
    }
    const inspect = async (): Promise<BigIntStats[]> => {
      if (await realpath(canonicalRoot) !== canonicalRoot || await realpath(canonicalPath) !== canonicalPath) throw denied();
      const stats: BigIntStats[] = [];
      for (const [index, path] of paths.entries()) {
        const info = await lstat(path, { bigint: true });
        if (info.isSymbolicLink() || (index < paths.length - 1 && !info.isDirectory())) throw denied();
        stats.push(info);
      }
      const file = stats[stats.length - 1]!;
      if (!file.isFile() || file.nlink !== 1n || file.size > BigInt(maxBytes)) throw denied();
      return stats;
    };
    const authorized = await inspect();
    const metadata = authorized[authorized.length - 1]!;
    const checkContinuity = async (): Promise<void> => {
      const current = await inspect();
      if (!current.every((info, index) => index === current.length - 1
        ? sameFile(authorized[index]!, info)
        : sameIdentity(authorized[index]!, info))) throw denied();
    };
    let completed = false;
    const tool: RuntimeToolDefinition = {
      name: "read_file",
      description: "Read the one file declared by the governing Agent 1 run.",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false
      },
      permission: { effect: "allow", operation: "read", roots: [canonicalPath] },
      execute: async (_input, signal) => {
        const toolUseId = randomUUID();
        const evidence = {
          toolName: "read_file",
          adapterToolName: "read_file",
          toolUseId,
          source: "chirality-runtime-tool-bridge",
          pathMetadata: { relativePath }
        };
        await this.options.sessions.appendEvent(projectId, {
          sessionId,
          turnId,
          type: "tool.permission",
          data: {
            ...evidence,
            decision: "allow",
            operation: "read",
            reason: "Bounded Agent 1 authorization"
          }
        });
        await this.options.sessions.appendEvent(projectId, {
          sessionId,
          turnId,
          type: "tool.started",
          data: evidence
        });
        const startedAt = Date.now();
        try {
          if (signal.aborted) {
            throw new RuntimeError("INTERRUPTED", "Read interrupted", 499);
          }
          if (!_input || typeof _input !== "object" || Array.isArray(_input) || Object.keys(_input).length !== 0) throw denied();
          await checkContinuity();
          const handle = await open(canonicalPath, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
          let content: string;
          let byteLength: number;
          try {
            const before = await handle.stat({ bigint: true });
            if (!before.isFile() || !sameFile(metadata, before)) throw denied();
            await checkContinuity();
            // Fixed allocation and an extra byte bound growth even during a race.
            const buffer = Buffer.alloc(maxBytes + 1);
            let offset = 0;
            while (offset < buffer.length) {
              if (signal.aborted) throw new RuntimeError("INTERRUPTED", "Read interrupted", 499);
              const { bytesRead } = await handle.read(buffer, offset, buffer.length - offset, offset);
              if (bytesRead === 0) break;
              offset += bytesRead;
            }
            if (offset > maxBytes || BigInt(offset) !== before.size || !sameFile(before, await handle.stat({ bigint: true }))) throw denied();
            await checkContinuity();
            if (signal.aborted) throw new RuntimeError("INTERRUPTED", "Read interrupted", 499);
            content = new TextDecoder("utf-8", { fatal: true }).decode(buffer.subarray(0, offset));
            byteLength = offset;
          } finally {
            await handle.close();
          }
          await this.options.sessions.appendEvent(projectId, {
            sessionId,
            turnId,
            type: "tool.completed",
            data: {
              ...evidence,
              durationMs: Date.now() - startedAt,
              resultMetadata: {
                byteLength,
                rawOutputPersisted: false
              }
            }
          });
          completed = true;
          return { path: relativePath, content };
        } catch (error) {
          await this.options.sessions.appendEvent(projectId, {
            sessionId,
            turnId,
            type: "tool.failed",
            data: {
              ...evidence,
              durationMs: Date.now() - startedAt,
              error: error instanceof RuntimeError ? error.code : "READ_FAILED"
            }
          });
          throw error;
        }
      }
    };
    return {
      tool,
      receipt: {
        toolName: "read_file",
        completed: () => completed
      }
    };
  }

  private async listManagerDefinitions(
    projectId: string
  ): Promise<readonly { agentId: string; agentType: 0 | 1 | 2 }[]> {
    const roots = await this.options.projects.roots(projectId);
    const result: { agentId: string; agentType: 0 | 1 | 2 }[] = [];
    const { readdir } = await import("node:fs/promises");
    for (const directory of [join(roots.instructionRoot, "agents"), join(roots.workingRoot, "agents")]) {
      for (const entry of await readdir(directory, { withFileTypes: true }).catch(() => [])) {
        const nameMatch = /^AGENT_(.+)\.md$/u.exec(entry.name);
        if (!entry.isFile() || nameMatch?.[1] === undefined) continue;
        const source = await readFile(join(directory, entry.name), "utf8");
        const match = /AGENT_TYPE\s*:\s*([012])/iu.exec(source);
        if (match?.[1] !== undefined) {
          result.push({
            agentId: nameMatch[1],
            agentType: Number(match[1]) as 0 | 1 | 2
          });
        }
      }
    }
    return result;
  }

  private async persistAgentRun(
    projectId: string,
    runId: string,
    record: AgentRunRecord
  ): Promise<void> {
    await this.writeAgentRun(projectId, runId, record, "run.json");
  }

  /** Non-authoritative immutable progress; late I/O cannot replace the terminal run record. */
  private async persistAgentProgress(projectId: string, runId: string, record: AgentRunRecord): Promise<void> {
    await this.writeAgentRun(projectId, runId, { ...record, progressRecordedAt: new Date().toISOString() }, `progress-${randomUUID()}.json`);
  }

  private async writeAgentRun(projectId: string, runId: string, record: AgentRunRecord, filename: string): Promise<void> {
    const project = await this.options.projects.requireAuthorized(projectId);
    const manifest = await this.options.projects.readManifest(projectId);
    const executionRoot = await realpath(resolve(project.canonicalRoot, manifest.defaultExecutionRoot));
    if (!isContained(project.canonicalRoot, executionRoot)) {
      throw new RuntimeError("FORBIDDEN", "Execution root escapes the project", 403);
    }
    await atomicWriteJson(
      join(executionRoot, "_Coordination", "AgentRuns", "runtime", runId, filename),
      record
    );
  }
}
