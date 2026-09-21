import { randomUUID } from "node:crypto";
import { readdir, readFile, realpath, rename, rm, stat, truncate } from "node:fs/promises";
import { basename, join, resolve } from "node:path";
import {
  RuntimeError,
  canonicalApplicationJson,
  validateApplicationToolCatalog,
  type ApplicationToolCatalog,
  type ChiralityRoleName,
  type CreateSessionRequest,
  type HarnessEvent,
  type QualifiedMethodReference,
  type RuntimeSessionRecord
} from "@chirality/runtime-contracts";
import {
  appendJsonLine,
  assertSafeIdentifier,
  atomicWriteJson,
  ensurePrivateDirectory,
  exists,
  isContained,
  readJson,
  readJsonIfExists
} from "./fs.js";
import type { ProjectRegistry } from "./project-registry.js";
import {
  InstructionBasisStore,
  type InstructionBasisStoreOptions,
  type InstructionBasisSnapshot,
  type InstructionHistoryInput,
  type InstructionHistoryRecord,
  type MethodChangeAppliedHistoryRecord,
  type MethodChangeFailedHistoryRecord,
  type MethodChangeRequestedHistoryRecord,
  type ProviderSpanCancelledHistoryRecord,
  type ProviderSpanCommittedHistoryRecord,
  type ProviderSpanFailedHistoryRecord,
  type ProviderSpanPreparedHistoryRecord,
  type ResourceLoadedHistoryRecord,
  type SelectionChangedHistoryRecord
} from "./instruction-basis-store.js";

const acceptedTurnLocks = new Map<string, Promise<void>>();

interface AcceptedTurnTransaction {
  schemaVersion: "chirality.accepted-turn-transaction/v1";
  projectId: string;
  sessionId: string;
  priorEventBytes: number;
  event: HarnessEvent;
  instructionBasis: InstructionBasisSnapshot;
}

export class SessionStore {
  readonly instructionBases: InstructionBasisStore;

  constructor(
    private readonly runtimeDirectory: string,
    private readonly projects: ProjectRegistry,
    instructionBasisOptions: InstructionBasisStoreOptions = {}
  ) {
    this.instructionBases = new InstructionBasisStore(runtimeDirectory, projects, instructionBasisOptions);
  }

  async create(request: CreateSessionRequest & { reasoningEffort?: string }): Promise<RuntimeSessionRecord> {
    if (request.role === undefined || request.engineSelection === undefined) {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "SessionStore requires a daemon-resolved role and engine selection",
        500
      );
    }
    const project = await this.projects.requireAuthorized(request.projectId);
    const sessionId = randomUUID();
    const now = new Date().toISOString();
    const record: RuntimeSessionRecord = {
      schemaVersion: "chirality.session/v2",
      projectId: request.projectId,
      projectRoot: project.canonicalRoot,
      sessionId,
      createdAt: now,
      updatedAt: now,
      persona: request.persona ?? request.role,
      mode: request.mode ?? "governed",
      agentType: request.role === "agent0" ? 0 : request.role === "agent1" ? 1 : 2,
      role: request.role,
      engineSelection: request.engineSelection,
      ...(request.reasoningEffort === undefined ? {} : { reasoningEffort: request.reasoningEffort }),
      status: "idle",
      ...(request.parentSessionId === undefined ? {} : { parentSessionId: request.parentSessionId }),
      ...(request.approvalRef === undefined ? {} : { approvalRef: request.approvalRef }),
      ...(request.declaredContext === undefined
        ? {}
        : { declaredContext: [...request.declaredContext] }),
      ...(request.allowedWriteTargets === undefined
        ? {}
        : { allowedWriteTargets: [...request.allowedWriteTargets] })
    };
    await atomicWriteJson(this.sessionFile(request.projectId, sessionId), record);
    return record;
  }

  async list(projectId: string): Promise<readonly RuntimeSessionRecord[]> {
    const project = await this.projects.requireAuthorized(projectId);
    const records = new Map<string, RuntimeSessionRecord>();
    const central = this.sessionsDirectory(projectId);
    for (const entry of await readdir(central, { withFileTypes: true }).catch(() => [])) {
      if (!entry.isDirectory()) continue;
      const record = await this.readCentral(projectId, entry.name).catch(() => undefined);
      if (record !== undefined) records.set(record.sessionId, record);
    }
    for (const legacyRoot of project.legacySessionRoots) {
      for (const candidate of await this.listLegacyCandidates(project.canonicalRoot, legacyRoot)) {
        if (records.has(candidate.sessionId)) continue;
        if (await exists(this.deletedMarker(projectId, candidate.sessionId))) continue;
        const record = this.normalizeLegacy(projectId, project.canonicalRoot, candidate.sessionId, candidate.raw);
        if (record !== undefined) records.set(record.sessionId, record);
      }
    }
    return [...records.values()].sort((left, right) => left.createdAt.localeCompare(right.createdAt));
  }

  async get(projectId: string, sessionId: string): Promise<RuntimeSessionRecord> {
    assertSafeIdentifier(sessionId, "sessionId");
    return withSessionLock(`${projectId}\0${sessionId}`, () => this.getUnlocked(projectId, sessionId));
  }

  /** Application descriptors are immutable provider-thread context, separate from live handler bindings. */
  async getApplicationToolCatalog(projectId: string, sessionId: string): Promise<ApplicationToolCatalog | undefined> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const raw = await readJsonIfExists<unknown>(join(this.sessionDirectory(projectId, sessionId), "application-tools.json"), undefined);
      return raw === undefined ? undefined : validateApplicationToolCatalog(raw);
    });
  }

  /** Stock Codex 0.154 accepts dynamicTools on thread/start, not on thread/resume. */
  async registerApplicationToolCatalog(projectId: string, sessionId: string, catalog: ApplicationToolCatalog): Promise<ApplicationToolCatalog> {
    const proposed = validateApplicationToolCatalog(catalog);
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      const file = join(this.sessionDirectory(projectId, sessionId), "application-tools.json");
      const raw = await readJsonIfExists<unknown>(file, undefined);
      if (raw !== undefined) {
        const existing = validateApplicationToolCatalog(raw);
        if (canonicalApplicationJson(existing) !== canonicalApplicationJson(proposed)) {
          throw new RuntimeError("INVALID_REQUEST", "Application tool definitions and workspace identity are fixed for this conversation. Start a new conversation to change them.", 409, { reason: "APPLICATION_TOOL_CATALOG_IMMUTABLE" });
        }
        return existing;
      }
      if (current.status !== "idle" || current.bootedAt || current.engineSessionId || current.adapterSession?.engineSessionId || current.adapterSession?.lastRuntimeTurnId) {
        throw new RuntimeError("INVALID_REQUEST", "Register application tools before the conversation is booted or used. Start a new conversation for these tools.", 409, { reason: "APPLICATION_TOOL_CATALOG_TOO_LATE" });
      }
      await atomicWriteJson(file, proposed);
      return proposed;
    });
  }

  private async getUnlocked(projectId: string, sessionId: string): Promise<RuntimeSessionRecord> {
    const project = await this.projects.requireAuthorized(projectId);
    await this.reconcileAcceptedTurn(projectId, sessionId);
    if (await exists(this.deletedMarker(projectId, sessionId))) {
      throw new RuntimeError("SESSION_NOT_FOUND", `Unknown session: ${sessionId}`, 404);
    }
    const central = await this.readCentral(projectId, sessionId).catch((error: unknown) => {
      if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
      throw error;
    });
    if (central !== undefined) return central;
    for (const legacyRoot of project.legacySessionRoots) {
      const migrated = await this.migrateLegacy(
        projectId,
        project.canonicalRoot,
        legacyRoot,
        sessionId
      );
      if (migrated !== undefined) return migrated;
    }
    throw new RuntimeError("SESSION_NOT_FOUND", `Unknown session: ${sessionId}`, 404);
  }

  /**
   * Service shutdown settlement for a turn that did not reach its own terminal in
   * time: records `turn.interrupted` with the reason and moves a still-running
   * session to `interrupted`. A session that already settled is left unchanged.
   */
  async markInterruptedOnShutdown(projectId: string, sessionId: string, turnId: string, reason = "service-shutdown"): Promise<boolean> {
    const current = await this.get(projectId, sessionId);
    if (current.status !== "running") return false;
    await this.appendEvent(projectId, { sessionId, turnId, type: "turn.interrupted", data: { reason } });
    await this.update({ ...current, status: "interrupted" });
    return true;
  }

  /**
   * Service start: a fresh service owns no turns, so a session whose record still
   * says `running` was left there by a service that ended without settling it
   * (hard kill, crash). Records `turn.interrupted` with the reason against the
   * last accepted turn and moves the session to `interrupted`. Returns the
   * settled session ids.
   */
  async settleRunningOnStart(projectId: string, reason = "service-restart"): Promise<readonly string[]> {
    const settled: string[] = [];
    for (const record of await this.list(projectId)) {
      if (record.status !== "running") continue;
      const events = await this.replay(projectId, record.sessionId).catch(() => [] as readonly HarnessEvent[]);
      const turnId = [...events].reverse().find((event) => event.turnId !== undefined && (event.type === "turn.accepted" || event.type === "turn.started"))?.turnId ?? "unknown";
      if (await this.markInterruptedOnShutdown(projectId, record.sessionId, turnId, reason)) settled.push(record.sessionId);
    }
    return settled;
  }

  async update(record: RuntimeSessionRecord): Promise<void> {
    await withSessionLock(`${record.projectId}\0${record.sessionId}`, async () => {
      await this.projects.requireAuthorized(record.projectId);
      const current = await this.getUnlocked(record.projectId, record.sessionId);
      if (current.projectRoot !== record.projectRoot) {
        throw new RuntimeError("FORBIDDEN", "Session project root cannot be changed", 403);
      }
      await atomicWriteJson(this.sessionFile(record.projectId, record.sessionId), {
        ...record,
        ...preservedConcurrentSelection(current, record),
        updatedAt: new Date().toISOString()
      });
    });
  }

  async withSessionMutation<T>(
    projectId: string,
    sessionId: string,
    operation: (current: RuntimeSessionRecord) => Promise<T>
  ): Promise<T> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () =>
      operation(await this.getUnlocked(projectId, sessionId))
    );
  }

  async mutateWhenNotRunning(
    projectId: string,
    sessionId: string,
    mutate: (current: RuntimeSessionRecord) => RuntimeSessionRecord
  ): Promise<RuntimeSessionRecord> {
    const key = `${projectId}\0${sessionId}`;
    return withSessionLock(key, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.status === "running") throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session already has an active turn", 409);
      const next = mutate(current);
      if (next.projectId !== projectId || next.sessionId !== sessionId || next.projectRoot !== current.projectRoot) throw new RuntimeError("FORBIDDEN", "Session mutation cannot change identity", 403);
      const persisted = { ...next, updatedAt: new Date().toISOString() };
      await atomicWriteJson(this.sessionFile(projectId, sessionId), persisted);
      return persisted;
    });
  }

  async clearContextSuccessor(projectId: string, sessionId: string, preparationId: string): Promise<RuntimeSessionRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.adapterSession?.contextSuccessor?.preparationId !== preparationId) return current;
      const adapterSession = { ...(current.adapterSession ?? {}) };
      delete adapterSession.contextSuccessor;
      const persisted = { ...current, adapterSession, updatedAt: new Date().toISOString() };
      await atomicWriteJson(this.sessionFile(projectId, sessionId), persisted);
      return persisted;
    });
  }

  async mutateSelection(
    projectId: string,
    sessionId: string,
    expected: { instructionBasisId?: string; methodSelectionRevision: number },
    mutate: (current: RuntimeSessionRecord, lockedSnapshot: { events: readonly HarnessEvent[]; instructionHistory: readonly InstructionHistoryRecord[] }) => Promise<{
      session: RuntimeSessionRecord;
      history: SelectionChangedHistoryRecord;
      providerSpanPreparation?: ProviderSpanPreparedHistoryRecord;
      providerSpanCommitmentReference?: string;
    }> | {
      session: RuntimeSessionRecord;
      history: SelectionChangedHistoryRecord;
      providerSpanPreparation?: ProviderSpanPreparedHistoryRecord;
      providerSpanCommitmentReference?: string;
    }
  ): Promise<RuntimeSessionRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.status === "running") {
        throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session already has an active turn", 409);
      }
      if (
        current.instructionBasisId !== expected.instructionBasisId ||
        (current.methodSelectionRevision ?? 0) !== expected.methodSelectionRevision
      ) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Session selection changed before mutation", 409);
      }
      const events = (await this.replayDetailedUnlocked(projectId, sessionId)).events;
      const instructionHistory = await this.instructionBases.history(projectId, sessionId);
      const result = await mutate(current, { events, instructionHistory });
      const next = result.session;
      if (next.projectId !== projectId || next.sessionId !== sessionId || next.projectRoot !== current.projectRoot) {
        throw new RuntimeError("FORBIDDEN", "Session mutation cannot change identity", 403);
      }
      const preparation = result.providerSpanPreparation;
      const commitmentReference = result.providerSpanCommitmentReference;
      if ((preparation === undefined) !== (commitmentReference === undefined)) {
        throw new RuntimeError("INVALID_REQUEST", "Provider span preparation and commitment reference must be supplied together", 400);
      }
      if (preparation !== undefined) {
        if (
          preparation.targetBasisId !== next.instructionBasisId ||
          preparation.predecessor.engineSessionId !== current.engineSessionId
        ) {
          throw new RuntimeError("INVALID_REQUEST", "Provider span preparation does not match predecessor and target selection", 400);
        }
        await this.instructionBases.appendHistory(projectId, sessionId, preparation);
      }
      const persisted = { ...next, updatedAt: new Date().toISOString() };
      try {
        await atomicWriteJson(this.sessionFile(projectId, sessionId), persisted);
        await this.instructionBases.appendHistory(projectId, sessionId, result.history);
        if (preparation !== undefined && commitmentReference !== undefined) {
          await this.instructionBases.appendHistory(projectId, sessionId, {
            ...preparation,
            type: "provider-span.committed",
            commitmentReference
          });
        }
      } catch (error) {
        await atomicWriteJson(this.sessionFile(projectId, sessionId), current);
        if (preparation !== undefined) {
          await this.instructionBases.appendHistory(projectId, sessionId, {
            ...preparation,
            type: "provider-span.failed",
            code: "SELECTION_MUTATION_FAILED",
            message: error instanceof Error ? error.message : "Selection mutation failed"
          });
        }
        throw error;
      }
      return persisted;
    });
  }

  /**
   * Activates compatible methods loaded by the agent during the currently
   * accepted turn. The accepted basis remains the turn's frozen basis; the
   * expanded selection is used when resolving the next turn.
   */
  async activateLoadedMethods(
    projectId: string,
    sessionId: string,
    input: {
      turnId: string;
      invocationId: string;
      methods: readonly QualifiedMethodReference[];
      instructionPolicySha256?: string;
      loadedEntries: readonly ResourceLoadedHistoryRecord[];
      prepare?: (current: RuntimeSessionRecord) => Promise<{
        methods: readonly QualifiedMethodReference[];
        instructionPolicySha256: string;
        loadedEntries: readonly ResourceLoadedHistoryRecord[];
      }>;
    }
  ): Promise<RuntimeSessionRecord> {
    if (
      !nonempty(input.turnId) ||
      !nonempty(input.invocationId) ||
      (input.prepare === undefined && (!Array.isArray(input.methods) || !input.methods.every(validQualifiedMethod))) ||
      (input.prepare === undefined && !validHash(input.instructionPolicySha256)) ||
      (input.prepare === undefined && !Array.isArray(input.loadedEntries))
    ) {
      throw new RuntimeError("INVALID_REQUEST", "Method activation requires turn, invocation, and method identities", 400);
    }
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.status !== "running") {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Methods can only be activated during a running turn", 409);
      }
      const accepted = await this.requireCurrentAcceptedTurnUnlocked(projectId, sessionId, input.turnId);
      const activation = input.prepare === undefined ? input : await input.prepare(current);
      if (!Array.isArray(activation.methods) || !activation.methods.every(validQualifiedMethod) || !Array.isArray(activation.loadedEntries)) {
        throw new RuntimeError("INVALID_REQUEST", "Prepared method activation is invalid", 400);
      }
      const selectedMethods = orderedMethodUnion(current.selectedMethods ?? [], activation.methods);
      const changed = selectedMethods.length !== (current.selectedMethods ?? []).length;
      const instructionPolicySha256 = input.prepare !== undefined
        ? activation.instructionPolicySha256
        : input.instructionPolicySha256!;
      if (!validHash(instructionPolicySha256)) throw new RuntimeError("INVALID_REQUEST", "Resolved method activation policy fingerprint is invalid", 400);
      const persisted: RuntimeSessionRecord = {
        ...current,
        schemaVersion: "chirality.session/v3",
        selectedMethods,
        methodSelectionRevision: (current.methodSelectionRevision ?? 0) + (changed ? 1 : 0),
        updatedAt: new Date().toISOString()
      };
      const records: InstructionHistoryInput[] = [...activation.loadedEntries];
      if (changed) records.push({
          type: "selection.changed",
          roleId: current.roleId ?? compatibleRoleId(current.persona, current.role),
          interactionMode: current.interactionMode ?? "chat",
          permissionMode: current.permissionMode ?? "ask",
          selectedMethods,
          reason: "agent-load",
          turnId: input.turnId,
          invocationId: input.invocationId,
          acceptedTurn: { turnId: input.turnId, eventId: accepted.eventId },
          instructionPolicySha256
      });
      return (await this.instructionBases.appendHistoryBatchWithCommit(projectId, sessionId, records, async () => {
        await atomicWriteJson(this.sessionFile(projectId, sessionId), persisted);
        return persisted;
      })).result;
    });
  }

  async requestMethodChange(
    projectId: string,
    sessionId: string,
    input: {
      turnId: string;
      invocationId: string;
      mode: "merge" | "replace";
      methods: readonly QualifiedMethodReference[];
      expectedRevision: number;
      expectedBasisId?: string;
    }
  ): Promise<Extract<InstructionHistoryRecord, { type: "method-change.requested" }>> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.status !== "running") {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Method changes can only be requested during a running turn", 409);
      }
      if (
        (current.methodSelectionRevision ?? 0) !== input.expectedRevision ||
        current.instructionBasisId !== input.expectedBasisId
      ) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Session selection changed before the method-change request", 409);
      }
      const accepted = await this.requireCurrentAcceptedTurnUnlocked(projectId, sessionId, input.turnId);
      return await this.instructionBases.appendHistory(projectId, sessionId, {
        type: "method-change.requested",
        ...input,
        acceptedTurn: { turnId: input.turnId, eventId: accepted.eventId }
      }) as Extract<InstructionHistoryRecord, { type: "method-change.requested" }>;
    });
  }

  async pendingMethodChanges(
    projectId: string,
    sessionId: string
  ): Promise<readonly Extract<InstructionHistoryRecord, { type: "method-change.requested" }>[]> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const history = await this.instructionBases.history(projectId, sessionId);
      const settled = new Set(history.flatMap((record) =>
        record.type === "method-change.applied" || record.type === "method-change.failed"
          ? [record.requestHistoryId]
          : []
      ));
      return history.filter((record): record is Extract<InstructionHistoryRecord, { type: "method-change.requested" }> =>
        record.type === "method-change.requested" && !settled.has(record.historyId)
      );
    });
  }

  async settleMethodChange(
    projectId: string,
    sessionId: string,
    requestHistoryId: string,
    outcome:
      | Omit<MethodChangeAppliedHistoryRecord, "type" | "requestHistoryId">
      | ({ failed: true } & Omit<MethodChangeFailedHistoryRecord, "type" | "requestHistoryId">)
  ): Promise<InstructionHistoryRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      const current = await this.getUnlocked(projectId, sessionId);
      if (current.status === "running") {
        throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "A pending method change cannot settle during an active turn", 409);
      }
      const history = await this.instructionBases.history(projectId, sessionId);
      const request = history.find((record) => record.type === "method-change.requested" && record.historyId === requestHistoryId);
      if (request === undefined) throw new RuntimeError("NOT_FOUND", `Unknown pending method change: ${requestHistoryId}`, 404);
      if (history.some((record) =>
        (record.type === "method-change.applied" || record.type === "method-change.failed") &&
        record.requestHistoryId === requestHistoryId
      )) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Pending method change is already settled", 409);
      }
      if ("failed" in outcome) {
        return this.instructionBases.appendHistory(projectId, sessionId, {
          type: "method-change.failed",
          requestHistoryId,
          code: outcome.code,
          message: outcome.message
        });
      }
      if (
        outcome.resultingRevision !== (current.methodSelectionRevision ?? 0) ||
        outcome.resultingBasisId !== current.instructionBasisId ||
        !sameMethodSelection(outcome.selectedMethods, current.selectedMethods ?? [])
      ) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Applied method-change outcome does not match the persisted session", 409);
      }
      return this.instructionBases.appendHistory(projectId, sessionId, {
        type: "method-change.applied",
        requestHistoryId,
        ...outcome
      });
    });
  }

  private async requireCurrentAcceptedTurnUnlocked(
    projectId: string,
    sessionId: string,
    turnId: string
  ): Promise<HarnessEvent> {
    const replay = await this.replayDetailedUnlocked(projectId, sessionId);
    const accepted = [...replay.events].reverse().find((event) => event.type === "turn.accepted");
    if (accepted === undefined || accepted.turnId !== turnId) {
      throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Operation does not identify the currently accepted turn", 409);
    }
    const terminal = replay.events.some((event) =>
      event.turnId === turnId &&
      (event.type === "turn.completed" || event.type === "turn.failed" || event.type === "turn.interrupted")
    );
    if (terminal) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "The accepted turn is already terminal", 409);
    return accepted;
  }

  async commitProviderSpanPreparation(
    projectId: string,
    sessionId: string,
    preparationId: string,
    commitmentReference: string
  ): Promise<ProviderSpanCommittedHistoryRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const prepared = await this.requireOpenProviderSpanPreparation(projectId, sessionId, preparationId);
      const record: ProviderSpanCommittedHistoryRecord = {
        ...prepared,
        type: "provider-span.committed",
        commitmentReference
      };
      await this.instructionBases.appendHistory(projectId, sessionId, record);
      return record;
    });
  }

  async recordProviderSpanSessionInit(
    projectId: string,
    sessionId: string,
    preparationId: string,
    input: { sessionInitEventId: string; engineSessionId: string; providerSpanId: string }
  ) {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const history = await this.instructionBases.history(projectId, sessionId);
      const prepared = this.providerSpanPreparation(history, preparationId);
      const committed = history.some((record) =>
        record.type === "provider-span.committed" && record.preparationId === preparationId
      );
      const terminal = history.some((record) =>
        (record.type === "provider-span.continued" || record.type === "provider-span.cancelled" || record.type === "provider-span.failed") &&
        record.preparationId === preparationId
      );
      if (!committed || terminal) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Provider span is not awaiting session:init", 409);
      }
      return this.instructionBases.appendHistory(projectId, sessionId, {
        type: "provider-span.continued",
        preparationId,
        adapterId: prepared.adapterId,
        providerId: prepared.providerId,
        engineSessionId: input.engineSessionId,
        spanId: input.providerSpanId,
        sessionInitEventId: input.sessionInitEventId,
        continuationBoundary: {
          predecessor: prepared.predecessor,
          targetBasisId: prepared.targetBasisId,
          targetReference: prepared.targetReference,
          continuationHash: prepared.continuationHash
        }
      });
    });
  }

  async cancelProviderSpanPreparation(
    projectId: string,
    sessionId: string,
    preparationId: string,
    reason: string
  ): Promise<ProviderSpanCancelledHistoryRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const prepared = await this.requireOpenProviderSpanPreparation(projectId, sessionId, preparationId, true);
      const record: ProviderSpanCancelledHistoryRecord = { ...prepared, type: "provider-span.cancelled", reason };
      await this.instructionBases.appendHistory(projectId, sessionId, record);
      return record;
    });
  }

  async failProviderSpanPreparation(
    projectId: string,
    sessionId: string,
    preparationId: string,
    failure: { code: string; message: string }
  ): Promise<ProviderSpanFailedHistoryRecord> {
    return withSessionLock(`${projectId}\0${sessionId}`, async () => {
      await this.getUnlocked(projectId, sessionId);
      const prepared = await this.requireOpenProviderSpanPreparation(projectId, sessionId, preparationId, true);
      const record: ProviderSpanFailedHistoryRecord = { ...prepared, type: "provider-span.failed", ...failure };
      await this.instructionBases.appendHistory(projectId, sessionId, record);
      return record;
    });
  }

  private async requireOpenProviderSpanPreparation(
    projectId: string,
    sessionId: string,
    preparationId: string,
    allowCommitted = false
  ): Promise<ProviderSpanPreparedHistoryRecord> {
    const history = await this.instructionBases.history(projectId, sessionId);
    const prepared = this.providerSpanPreparation(history, preparationId);
    const terminal = history.find((record) =>
      ((!allowCommitted && record.type === "provider-span.committed") || record.type === "provider-span.continued" || record.type === "provider-span.cancelled" || record.type === "provider-span.failed") &&
      record.preparationId === preparationId
    );
    if (terminal !== undefined) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Provider span preparation is already terminal", 409);
    return prepared;
  }

  private providerSpanPreparation(
    history: readonly import("./instruction-basis-store.js").InstructionHistoryRecord[],
    preparationId: string
  ): ProviderSpanPreparedHistoryRecord {
    const prepared = history.find((record) =>
      record.type === "provider-span.prepared" && record.preparationId === preparationId
    );
    if (prepared === undefined || prepared.type !== "provider-span.prepared") {
      throw new RuntimeError("NOT_FOUND", `Unknown provider span preparation: ${preparationId}`, 404);
    }
    return prepared;
  }

  async delete(projectId: string, sessionId: string): Promise<void> {
    await this.get(projectId, sessionId);
    await rm(this.sessionDirectory(projectId, sessionId), { recursive: true, force: false });
    await atomicWriteJson(this.deletedMarker(projectId, sessionId), {
      schemaVersion: "chirality.session-deletion/v1",
      sessionId,
      deletedAt: new Date().toISOString()
    });
  }

  async appendEvent(
    projectId: string,
    input: Omit<HarnessEvent, "schemaVersion" | "eventId" | "timestamp">
  ): Promise<HarnessEvent> {
    return withSessionLock(`${projectId}\0${input.sessionId}`, async () => {
      const event: HarnessEvent = {
        ...input,
        schemaVersion: 1,
        eventId: randomUUID(),
        timestamp: new Date().toISOString()
      };
      await this.getUnlocked(projectId, input.sessionId);
      await appendJsonLine(this.eventsFile(projectId, input.sessionId), event);
      return event;
    });
  }

  /**
   * Persists turn acceptance and its frozen instruction basis as one serialized
   * session operation. A failed basis commit rolls the event log back to its
   * prior byte boundary, leaving neither half visible.
   */
  async commitWithAcceptedTurn(
    session: RuntimeSessionRecord,
    input: Omit<HarnessEvent, "schemaVersion" | "eventId" | "timestamp">,
    snapshot: InstructionBasisSnapshot
  ): Promise<{ event: HarnessEvent; instructionBasis: InstructionBasisSnapshot }> {
    if (
      input.type !== "turn.accepted" ||
      input.sessionId !== session.sessionId ||
      snapshot.sessionId !== session.sessionId
    ) {
      throw new RuntimeError(
        "INVALID_REQUEST",
        "Accepted turn and instruction basis must identify the same session",
        400
      );
    }
    this.instructionBases.prepare(snapshot);
    const key = `${session.projectId}\0${session.sessionId}`;
    return withSessionLock(key, async () => {
      const current = await this.getUnlocked(session.projectId, session.sessionId);
      if (current.status === "running") {
        throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Session already has an active turn", 409);
      }
      if (current.instructionBasisId !== session.instructionBasisId || current.methodSelectionRevision !== session.methodSelectionRevision) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Session method selection changed before turn acceptance", 409);
      }
      const eventsPath = this.eventsFile(session.projectId, session.sessionId);
      const priorSize = await stat(eventsPath).then((value) => value.size).catch(
        (error: NodeJS.ErrnoException) => {
          if (error.code === "ENOENT") return 0;
          throw error;
        }
      );
      const event: HarnessEvent = {
        ...input,
        schemaVersion: 1,
        eventId: randomUUID(),
        timestamp: new Date().toISOString()
      };
      const transaction: AcceptedTurnTransaction = {
        schemaVersion: "chirality.accepted-turn-transaction/v1",
        projectId: session.projectId,
        sessionId: session.sessionId,
        priorEventBytes: priorSize,
        event,
        instructionBasis: snapshot
      };
      const marker = this.acceptedTurnTransactionFile(session.projectId, session.sessionId);
      await atomicWriteJson(marker, transaction);
      await appendJsonLine(eventsPath, event);
      let basisCommitted = false;
      try {
        const instructionBasis = await this.instructionBases.commitWithTurn(
          session.projectId,
          snapshot,
          { turnId: input.turnId ?? "session-turn", eventId: event.eventId }
        );
        basisCommitted = true;
        await atomicWriteJson(this.sessionFile(session.projectId, session.sessionId), {
          ...current,
          schemaVersion: "chirality.session/v3",
          roleId: snapshot.roleId,
          interactionMode: snapshot.interactionMode,
          permissionMode: snapshot.permissionMode,
          selectedMethods: [...snapshot.selectedMethods],
          instructionBasisId: snapshot.basisId,
          status: "running",
          updatedAt: new Date().toISOString()
        });
        await rm(marker, { force: true });
        return { event, instructionBasis };
      } catch (error) {
        if (!basisCommitted) {
          if (priorSize === 0) await rm(eventsPath, { force: true });
          else await truncate(eventsPath, priorSize);
          await rm(marker, { force: true });
        }
        // Once the immutable basis is committed, retain the marker and event.
        // A later locked read finishes the session projection idempotently.
        throw error;
      }
    });
  }

  private async reconcileAcceptedTurn(projectId: string, sessionId: string): Promise<void> {
    const marker = this.acceptedTurnTransactionFile(projectId, sessionId);
    const transaction = await readJsonIfExists<AcceptedTurnTransaction | undefined>(marker, undefined);
    if (transaction === undefined) return;
    if (
      transaction.schemaVersion !== "chirality.accepted-turn-transaction/v1" ||
      transaction.projectId !== projectId ||
      transaction.sessionId !== sessionId ||
      transaction.event.sessionId !== sessionId ||
      transaction.instructionBasis.sessionId !== sessionId
    ) {
      throw new RuntimeError("INTERNAL_FAILURE", "Invalid accepted-turn recovery marker", 500);
    }
    const eventsPath = this.eventsFile(projectId, sessionId);
    const source = await readFile(eventsPath, "utf8").catch((error: NodeJS.ErrnoException) => {
      if (error.code === "ENOENT") return "";
      throw error;
    });
    const eventPresent = source.split("\n").some((line) => {
      if (line.trim() === "") return false;
      try { return (JSON.parse(line) as { eventId?: string }).eventId === transaction.event.eventId; }
      catch { return false; }
    });
    if (!eventPresent) {
      await rm(marker, { force: true });
      return;
    }
    try {
      await this.instructionBases.commitWithTurn(projectId, transaction.instructionBasis, {
        turnId: transaction.event.turnId ?? "session-turn",
        eventId: transaction.event.eventId
      });
      const current = await this.readCentral(projectId, sessionId);
      await atomicWriteJson(this.sessionFile(projectId, sessionId), {
        ...current,
        schemaVersion: "chirality.session/v3",
        roleId: transaction.instructionBasis.roleId,
        interactionMode: transaction.instructionBasis.interactionMode,
        permissionMode: transaction.instructionBasis.permissionMode,
        selectedMethods: [...transaction.instructionBasis.selectedMethods],
        instructionBasisId: transaction.instructionBasis.basisId,
        status: "running",
        updatedAt: new Date().toISOString()
      });
      await rm(marker, { force: true });
    } catch (error) {
      if (transaction.priorEventBytes === 0) await rm(eventsPath, { force: true });
      else await truncate(eventsPath, transaction.priorEventBytes);
      await rm(marker, { force: true });
      throw error;
    }
  }

  async persistEvent(projectId: string, event: HarnessEvent): Promise<void> {
    if (event.schemaVersion !== 1) {
      throw new RuntimeError("INVALID_REQUEST", "Unsupported harness event schema", 400);
    }
    await withSessionLock(`${projectId}\0${event.sessionId}`, async () => {
      await this.getUnlocked(projectId, event.sessionId);
      const existing = await this.replayDetailedUnlocked(projectId, event.sessionId);
      if (existing.events.some((candidate) => candidate.eventId === event.eventId)) return;
      await appendJsonLine(this.eventsFile(projectId, event.sessionId), event);
    });
  }

  async replay(projectId: string, sessionId: string): Promise<readonly HarnessEvent[]> {
    return (await this.replayDetailed(projectId, sessionId)).events;
  }

  async replayDetailed(
    projectId: string,
    sessionId: string
  ): Promise<{
    events: readonly HarnessEvent[];
    malformedLineCount: number;
    summary: {
      eventCount: number;
      malformedLineCount: number;
      eventTypeCounts: Record<string, number>;
      firstTimestamp?: string;
      lastTimestamp?: string;
    };
  }> {
    return withSessionLock(`${projectId}\0${sessionId}`, () =>
      this.replayDetailedUnlocked(projectId, sessionId)
    );
  }

  private async replayDetailedUnlocked(
    projectId: string,
    sessionId: string
  ): Promise<{
    events: readonly HarnessEvent[];
    malformedLineCount: number;
    summary: {
      eventCount: number;
      malformedLineCount: number;
      eventTypeCounts: Record<string, number>;
      firstTimestamp?: string;
      lastTimestamp?: string;
    };
  }> {
    await this.getUnlocked(projectId, sessionId);
    const source = await readFile(this.eventsFile(projectId, sessionId), "utf8").catch(
      (error: NodeJS.ErrnoException) => {
        if (error.code === "ENOENT") return "";
        throw error;
      }
    );
    const events: HarnessEvent[] = [];
    let malformedLineCount = 0;
    for (const line of source.split("\n")) {
      if (line.trim() === "") continue;
      try {
        const value = JSON.parse(line) as HarnessEvent | (Record<string, unknown> & {
          schemaVersion: 2;
          eventId: string;
          sessionId: string;
          timestamp: string;
          type: string;
        });
        if ((value.schemaVersion !== 1 && value.schemaVersion !== 2) || value.sessionId !== sessionId) {
          malformedLineCount += 1;
          continue;
        }
        // Keep the legacy public return type while preserving v2 event objects
        // byte-for-field for migration readers.
        events.push(value as HarnessEvent);
      } catch {
        malformedLineCount += 1;
      }
    }
    const eventTypeCounts: Record<string, number> = {};
    for (const event of events) {
      eventTypeCounts[event.type] = (eventTypeCounts[event.type] ?? 0) + 1;
    }
    return {
      events,
      malformedLineCount,
      summary: {
        eventCount: events.length,
        malformedLineCount,
        eventTypeCounts,
        ...(events[0]?.timestamp === undefined ? {} : { firstTimestamp: events[0].timestamp }),
        ...(events.at(-1)?.timestamp === undefined
          ? {}
          : { lastTimestamp: events.at(-1)!.timestamp })
      }
    };
  }

  private async readCentral(projectId: string, sessionId: string): Promise<RuntimeSessionRecord> {
    const raw = await readJson<Record<string, unknown>>(this.sessionFile(projectId, sessionId));
    if (
      !["chirality.session/v1", "chirality.session/v2", "chirality.session/v3"].includes(
        String(raw["schemaVersion"])
      ) ||
      raw["projectId"] !== projectId ||
      raw["sessionId"] !== sessionId
    ) {
      throw new RuntimeError("INTERNAL_FAILURE", "Invalid central session record", 500);
    }
    if (raw["schemaVersion"] === "chirality.session/v2" || raw["schemaVersion"] === "chirality.session/v3") {
      const record = raw as unknown as RuntimeSessionRecord;
      if (isChiralityRoleName(raw["roleId"])) return record;
      return {
        ...record,
        roleId: compatibleRoleId(record.persona, record.role)
      } as RuntimeSessionRecord;
    }
    // v1 and v3 records are normalized only in memory for the compatibility
    // API. Their persisted bytes and version remain untouched.
    return this.normalizeLegacy(projectId, String(raw["projectRoot"]), sessionId, raw) ?? (() => {
      throw new RuntimeError("INTERNAL_FAILURE", "Invalid central session record", 500);
    })();
  }

  private async migrateLegacy(
    projectId: string,
    projectRoot: string,
    relativeLegacyRoot: string,
    sessionId: string
  ): Promise<RuntimeSessionRecord | undefined> {
    const root = await this.resolveLegacyRoot(projectRoot, relativeLegacyRoot);
    if (root === undefined) return undefined;
    const directoryCandidate = join(root, sessionId, "session.json");
    const flatCandidate = join(root, `${sessionId}.json`);
    const sourceFile = (await exists(directoryCandidate))
      ? directoryCandidate
      : (await exists(flatCandidate))
        ? flatCandidate
        : undefined;
    if (sourceFile === undefined) return undefined;
    const raw = await readJson<Record<string, unknown>>(sourceFile);
    if (typeof raw["projectRoot"] === "string") {
      const legacyProjectRoot = await realpath(raw["projectRoot"]).catch(() => undefined);
      if (legacyProjectRoot !== projectRoot) return undefined;
    }
    const record = this.normalizeLegacy(projectId, projectRoot, sessionId, {
      ...raw,
      projectRoot
    });
    if (record === undefined) return undefined;
    const temporary = join(this.sessionsDirectory(projectId), `.${sessionId}.${randomUUID()}.tmp`);
    await ensurePrivateDirectory(temporary);
    await atomicWriteJson(join(temporary, "session.json"), {
      ...record,
      legacy: { sourcePath: sourceFile, migratedAt: new Date().toISOString() }
    });
    const legacyEvents = join(root, sessionId, "events.jsonl");
    if (await exists(legacyEvents)) {
      const lines = await readFile(legacyEvents, "utf8");
      const { writeFile, chmod } = await import("node:fs/promises");
      await writeFile(join(temporary, "events.jsonl"), lines, { encoding: "utf8", mode: 0o600 });
      await chmod(join(temporary, "events.jsonl"), 0o600);
    }
    await ensurePrivateDirectory(this.sessionsDirectory(projectId));
    const destination = this.sessionDirectory(projectId, sessionId);
    try {
      await rename(temporary, destination);
    } catch (error) {
      await rm(temporary, { recursive: true, force: true });
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    }
    return this.readCentral(projectId, sessionId);
  }

  private normalizeLegacy(
    projectId: string,
    projectRoot: string,
    sessionId: string,
    raw: Record<string, unknown>
  ): RuntimeSessionRecord | undefined {
    const rawRoot = typeof raw["projectRoot"] === "string" ? resolve(raw["projectRoot"]) : projectRoot;
    if (rawRoot !== projectRoot) return undefined;
    const selection = raw["engineSelection"] as Record<string, unknown> | undefined;
    const inferredAdapter =
      typeof selection?.["adapterId"] === "string"
        ? selection["adapterId"]
        : raw["sdkSessionId"] !== undefined
          ? "claude-agent-sdk"
          : "stub";
    const inferredProvider =
      typeof selection?.["providerId"] === "string"
        ? selection["providerId"]
        : inferredAdapter === "stub"
          ? "stub"
          : "anthropic";
    const now = new Date().toISOString();
    const persona = typeof raw["persona"] === "string" ? raw["persona"] : "agent1";
    const role =
      raw["role"] === "agent0" || raw["role"] === "agent2" || raw["role"] === "agent1"
        ? raw["role"]
        : "agent1";
    return {
      ...raw,
      schemaVersion: "chirality.session/v2",
      projectId,
      projectRoot,
      sessionId,
      createdAt: typeof raw["createdAt"] === "string" ? raw["createdAt"] : now,
      updatedAt: typeof raw["updatedAt"] === "string" ? raw["updatedAt"] : now,
      persona,
      mode: typeof raw["mode"] === "string" ? raw["mode"] : "governed",
      agentType:
        raw["agentType"] === 0 || raw["agentType"] === 2 || raw["agentType"] === 1
          ? raw["agentType"]
          : 1,
      role,
      roleId: isChiralityRoleName(raw["roleId"])
        ? raw["roleId"]
        : compatibleRoleId(persona, role),
      engineSelection: {
        adapterId: inferredAdapter,
        providerId: inferredProvider,
        model:
          typeof selection?.["model"] === "string"
            ? selection["model"]
            : typeof raw["model"] === "string"
              ? raw["model"]
              : ""
      },
      status:
        raw["status"] === "running" ||
        raw["status"] === "completed" ||
        raw["status"] === "failed" ||
        raw["status"] === "interrupted" ||
        raw["status"] === "idle"
          ? raw["status"]
          : "idle",
      ...(typeof raw["engineSessionId"] === "string"
        ? { engineSessionId: raw["engineSessionId"] }
        : typeof raw["sdkSessionId"] === "string"
          ? { engineSessionId: raw["sdkSessionId"] }
          : {}),
      ...(typeof raw["claudeSessionId"] === "string"
        ? { claudeSessionId: raw["claudeSessionId"] }
        : {}),
      ...(typeof raw["parentSessionId"] === "string"
        ? { parentSessionId: raw["parentSessionId"] }
        : {})
    };
  }

  private async listLegacyCandidates(
    projectRoot: string,
    relativeLegacyRoot: string
  ): Promise<readonly { sessionId: string; raw: Record<string, unknown> }[]> {
    const root = await this.resolveLegacyRoot(projectRoot, relativeLegacyRoot);
    if (root === undefined) return [];
    const candidates: { sessionId: string; raw: Record<string, unknown> }[] = [];
    for (const entry of await readdir(root, { withFileTypes: true }).catch(() => [])) {
      const source = entry.isDirectory()
        ? join(root, entry.name, "session.json")
        : entry.isFile() && entry.name.endsWith(".json")
          ? join(root, entry.name)
          : undefined;
      if (source === undefined || !(await exists(source))) continue;
      const sessionId = entry.isDirectory() ? entry.name : basename(entry.name, ".json");
      const raw = await readJsonIfExists<Record<string, unknown> | undefined>(source, undefined);
      if (raw !== undefined) candidates.push({ sessionId, raw });
    }
    return candidates;
  }

  private async resolveLegacyRoot(
    projectRoot: string,
    relativePath: string
  ): Promise<string | undefined> {
    const candidate = resolve(projectRoot, relativePath);
    if (!isContained(projectRoot, candidate)) {
      throw new RuntimeError("FORBIDDEN", "Legacy session root escapes the project", 403);
    }
    const canonicalRoot = await realpath(projectRoot);
    // Legacy session roots are read-if-present: an absent root simply holds no
    // legacy sessions, so callers skip it instead of failing the request.
    // Escape checks above and below still apply whenever the root exists.
    let canonical: string;
    try {
      canonical = await realpath(candidate);
    } catch (error) {
      const code = (error as NodeJS.ErrnoException).code;
      if (code === "ENOENT" || code === "ENOTDIR") return undefined;
      throw error;
    }
    if (!isContained(canonicalRoot, canonical)) {
      throw new RuntimeError("FORBIDDEN", "Legacy session root escapes through a symlink", 403);
    }
    return canonical;
  }

  private sessionsDirectory(projectId: string): string {
    assertSafeIdentifier(projectId, "projectId");
    return join(this.runtimeDirectory, "projects", projectId, "sessions");
  }

  private sessionDirectory(projectId: string, sessionId: string): string {
    assertSafeIdentifier(sessionId, "sessionId");
    return join(this.sessionsDirectory(projectId), sessionId);
  }

  private sessionFile(projectId: string, sessionId: string): string {
    return join(this.sessionDirectory(projectId, sessionId), "session.json");
  }

  private eventsFile(projectId: string, sessionId: string): string {
    return join(this.sessionDirectory(projectId, sessionId), "events.jsonl");
  }

  private deletedMarker(projectId: string, sessionId: string): string {
    assertSafeIdentifier(sessionId, "sessionId");
    return join(this.sessionsDirectory(projectId), ".deleted", `${sessionId}.json`);
  }

  private acceptedTurnTransactionFile(projectId: string, sessionId: string): string {
    return join(this.sessionDirectory(projectId, sessionId), "accepted-turn-transaction.json");
  }
}

/** Maps retired session personas to the v3 role taxonomy without changing the recorded persona. */
export function compatibleRoleId(
  persona: string,
  role: RuntimeSessionRecord["role"]
): ChiralityRoleName {
  if (persona === "HELP_HUMAN" || persona === "HELPS_HUMANS" || persona === "WORKING_ITEMS" || persona === "TASK") {
    return persona as ChiralityRoleName;
  }
  if (role === "agent0") return "HELP_HUMAN";
  if (role === "agent2") return "TASK";
  return "WORKING_ITEMS";
}

function isChiralityRoleName(value: unknown): value is ChiralityRoleName {
  return value === "HELP_HUMAN" || value === "HELPS_HUMANS" || value === "WORKING_ITEMS" || value === "TASK";
}

async function withSessionLock<T>(key: string, operation: () => Promise<T>): Promise<T> {
  const previous = acceptedTurnLocks.get(key) ?? Promise.resolve();
  const result = previous.then(operation);
  const queued = result.then(() => undefined, () => undefined);
  acceptedTurnLocks.set(key, queued);
  try {
    return await result;
  } finally {
    if (acceptedTurnLocks.get(key) === queued) acceptedTurnLocks.delete(key);
  }
}

function preservedConcurrentSelection(
  current: RuntimeSessionRecord,
  proposed: RuntimeSessionRecord
): Partial<RuntimeSessionRecord> {
  const sameTuple =
    current.instructionBasisId === proposed.instructionBasisId &&
    current.methodSelectionRevision === proposed.methodSelectionRevision;
  const initializingV3 =
    current.schemaVersion !== "chirality.session/v3" &&
    current.instructionBasisId === undefined &&
    current.methodSelectionRevision === undefined;
  if (sameTuple || initializingV3) return { status: proposed.status };
  return {
    ...(current.schemaVersion === "chirality.session/v3"
      ? { schemaVersion: "chirality.session/v3" as const }
      : {}),
    roleId: current.roleId,
    role: current.role,
    persona: current.persona,
    agentType: current.agentType,
    interactionMode: current.interactionMode,
    permissionMode: current.permissionMode,
    selectedMethods: current.selectedMethods,
    methodSelectionRevision: current.methodSelectionRevision,
    instructionBasisId: current.instructionBasisId,
    adapterSession: current.adapterSession,
    // A stale status update may still intentionally advance status; the caller
    // supplies that field. Selection state above always comes from disk.
    status: proposed.status
  };
}

function orderedMethodUnion(
  current: readonly QualifiedMethodReference[],
  loaded: readonly QualifiedMethodReference[]
): readonly QualifiedMethodReference[] {
  const selected: QualifiedMethodReference[] = [];
  const identities = new Set<string>();
  for (const method of [...current, ...loaded]) {
    const identity = `${method.sourceRootId}\0${method.source}\0${method.kind}\0${method.name}`;
    if (identities.has(identity)) continue;
    identities.add(identity);
    selected.push(method);
  }
  return selected;
}

function sameMethodSelection(
  left: readonly QualifiedMethodReference[],
  right: readonly QualifiedMethodReference[]
): boolean {
  if (left.length !== right.length) return false;
  return left.every((method, index) => {
    const candidate = right[index];
    return candidate !== undefined &&
      method.sourceRootId === candidate.sourceRootId &&
      method.source === candidate.source &&
      method.kind === candidate.kind &&
      method.name === candidate.name;
  });
}

function nonempty(value: unknown): value is string {
  return typeof value === "string" && value.trim() !== "";
}

function validHash(value: unknown): value is string {
  return typeof value === "string" && /^[a-f0-9]{64}$/u.test(value);
}

function validQualifiedMethod(value: QualifiedMethodReference): boolean {
  return nonempty(value.sourceRootId) &&
    (value.source === "project" || value.source === "user" || value.source === "bundled") &&
    (value.kind === "skill" || value.kind === "workflow") &&
    nonempty(value.name);
}
