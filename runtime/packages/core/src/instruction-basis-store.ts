import { randomUUID } from "node:crypto";
import { open, readFile, rm, stat, truncate } from "node:fs/promises";
import { dirname, join } from "node:path";
import {
  assertAdmittedNativePlanEvent,
  RuntimeError,
  type ChiralityRoleName,
  type MethodCompatibilityMapping,
  type NativePlanRevision,
  type QualifiedMethodReference,
  type SelectedMethodDisposition,
  type SuppliedContextEntry
} from "@chirality/runtime-contracts";
import {
  appendJsonLine,
  assertSafeIdentifier,
  ensurePrivateDirectory,
  exists,
  readJson,
  sha256
} from "./fs.js";
import type { ProjectRegistry } from "./project-registry.js";

export interface FrozenInstructionEntry {
  kind: SuppliedContextEntry["kind"];
  id: string;
  origin: string;
  path: string;
  sha256: string;
  content: string;
  method?: QualifiedMethodReference;
  resourcePath?: string;
}

export interface InstructionBasisSnapshot {
  schemaVersion: "chirality.instruction-basis/v1";
  basisId: string;
  sessionId: string;
  createdAt: string;
  roleId: ChiralityRoleName;
  interactionMode: "chat" | "native-plan";
  permissionMode: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods: readonly QualifiedMethodReference[];
  instructionPolicySha256?: string;
  compatibilityInputs: readonly ("Workflow" | "TaskSkill")[];
  compatibilityMappings: readonly MethodCompatibilityMapping[];
  suppliedEntries: readonly FrozenInstructionEntry[];
  methodDispositions: readonly SelectedMethodDisposition[];
  continuationBoundary?: Readonly<Record<string, unknown>>;
}

export interface SelectionChangedHistoryRecord {
  type: "selection.changed";
  roleId: ChiralityRoleName;
  interactionMode: "chat" | "native-plan";
  permissionMode: "readOnly" | "ask" | "workspaceWrite" | "bypass";
  selectedMethods: readonly QualifiedMethodReference[];
  reason?: string;
  turnId?: string;
  invocationId?: string;
  acceptedTurn?: {
    turnId: string;
    eventId: string;
  };
  instructionPolicySha256?: string;
}

export interface ResourceLoadedHistoryRecord {
  type: "resource.loaded";
  turnId: string;
  invocationId: string;
  resourceKind: "method-body" | "resource";
  id: string;
  method?: QualifiedMethodReference;
  origin: string;
  path: string;
  sha256: string;
  content: string;
}

export interface InstructionBasisResolvedHistoryRecord {
  type: "instruction-basis.resolved";
  basisId: string;
  acceptedTurn: {
    turnId: string;
    eventId: string;
  };
}

export interface MethodChangeRequestedHistoryRecord {
  type: "method-change.requested";
  turnId: string;
  invocationId: string;
  acceptedTurn: {
    turnId: string;
    eventId: string;
  };
  mode: "merge" | "replace";
  methods: readonly QualifiedMethodReference[];
  expectedRevision: number;
  expectedBasisId?: string;
}

export interface MethodChangeAppliedHistoryRecord {
  type: "method-change.applied";
  requestHistoryId: string;
  resultingRevision: number;
  resultingBasisId?: string;
  selectedMethods: readonly QualifiedMethodReference[];
}

export interface MethodChangeFailedHistoryRecord {
  type: "method-change.failed";
  requestHistoryId: string;
  code: string;
  message: string;
}

export interface NativePlanRevisedHistoryRecord {
  type: "native-plan.revised";
  revision: NativePlanRevision;
  revisionSha256?: string;
  qualificationSha256?: string;
  admissionSha256?: string;
  provenance?: "trusted-native-plan-registry";
}

export interface NativeChildMethodLoadedHistoryRecord {
  type: "native-child.method-loaded";
  associationId: string;
  supplierGeneration: string;
  parentSessionId: string;
  rootThreadId: string;
  rootTurnId: string;
  parentTurnId: string;
  childThreadId: string;
  childTurnId: string;
  roleId: ChiralityRoleName;
  roleBasisDigest: string;
  inheritedToolsDigest: string;
  invocationId: string;
  selectedMethods: readonly QualifiedMethodReference[];
  childInstructionBasisId: string;
  instructionPolicySha256: string;
  loadedEntries: readonly ResourceLoadedHistoryRecord[];
}

export interface ProviderSpanContinuedHistoryRecord {
  type: "provider-span.continued";
  preparationId: string;
  adapterId: string;
  providerId: string;
  engineSessionId: string;
  spanId: string;
  sessionInitEventId: string;
  continuationBoundary: Readonly<Record<string, unknown>>;
}

export interface ProviderSpanTransitionIdentity {
  preparationId: string;
  adapterId: string;
  providerId: string;
  predecessor: {
    engineSessionId: string;
    providerSpanId?: string;
  };
  targetBasisId: string;
  targetReference: string;
  continuationHash: string;
}

export interface ProviderSpanPreparedHistoryRecord extends ProviderSpanTransitionIdentity {
  type: "provider-span.prepared";
}

export interface ProviderSpanCommittedHistoryRecord extends ProviderSpanTransitionIdentity {
  type: "provider-span.committed";
  commitmentReference: string;
}

export interface ProviderSpanCancelledHistoryRecord extends ProviderSpanTransitionIdentity {
  type: "provider-span.cancelled";
  reason: string;
}

export interface ProviderSpanFailedHistoryRecord extends ProviderSpanTransitionIdentity {
  type: "provider-span.failed";
  code: string;
  message: string;
}

export type InstructionHistoryInput =
  | SelectionChangedHistoryRecord
  | ResourceLoadedHistoryRecord
  | InstructionBasisResolvedHistoryRecord
  | MethodChangeRequestedHistoryRecord
  | MethodChangeAppliedHistoryRecord
  | MethodChangeFailedHistoryRecord
  | NativePlanRevisedHistoryRecord
  | NativeChildMethodLoadedHistoryRecord
  | ProviderSpanContinuedHistoryRecord
  | ProviderSpanPreparedHistoryRecord
  | ProviderSpanCommittedHistoryRecord
  | ProviderSpanCancelledHistoryRecord
  | ProviderSpanFailedHistoryRecord;

export type InstructionHistoryRecord = InstructionHistoryInput & {
  schemaVersion: "chirality.instruction-history/v1";
  historyId: string;
  sessionId: string;
  sequence: number;
  timestamp: string;
};

const historyLocks = new Map<string, Promise<void>>();

export interface InstructionBasisStoreOptions {
  validateNativePlanRevision?: (revision: NativePlanRevision) => void;
}

/** Stores the exact instruction payload supplied to a session and its ordered load history. */
export class InstructionBasisStore {
  constructor(
    private readonly runtimeDirectory: string,
    private readonly projects: ProjectRegistry,
    private readonly options: InstructionBasisStoreOptions = {}
  ) {}

  /** Validates a candidate without reading or changing persistent state. */
  prepare(snapshot: InstructionBasisSnapshot): InstructionBasisSnapshot {
    this.validateSnapshot(snapshot);
    return structuredClone(snapshot);
  }

  /**
   * Commits a prepared basis only when the caller supplies the accepted-turn
   * identity. The caller invokes this while holding the existing session turn
   * lock, immediately after accepting that turn.
   */
  async commitWithTurn(
    projectId: string,
    snapshot: InstructionBasisSnapshot,
    acceptedTurn: { turnId: string; eventId: string }
  ): Promise<InstructionBasisSnapshot> {
    await this.projects.requireAuthorized(projectId);
    if (!nonempty(acceptedTurn.turnId) || !nonempty(acceptedTurn.eventId)) {
      throw invalid("Instruction basis commit requires an accepted turn identity");
    }
    assertSafeIdentifier(snapshot.sessionId, "sessionId");
    assertSafeIdentifier(snapshot.basisId, "basisId");
    this.validateSnapshot(snapshot);
    const path = this.basisFile(projectId, snapshot.sessionId, snapshot.basisId);
    if (await exists(path)) {
      const current = await readJson<InstructionBasisSnapshot>(path);
      if (sameFrozenMaterial(current, snapshot)) {
        const history = await this.history(projectId, snapshot.sessionId);
        if (!history.some((record) =>
          record.type === "instruction-basis.resolved" &&
          record.basisId === snapshot.basisId &&
          record.acceptedTurn.eventId === acceptedTurn.eventId
        )) {
          await this.appendHistory(projectId, snapshot.sessionId, {
            type: "instruction-basis.resolved",
            basisId: snapshot.basisId,
            acceptedTurn
          });
        }
        return current;
      }
      throw conflict("An instruction basis is frozen and cannot be replaced");
    }
    await writeNewJson(path, snapshot);
    try {
      await this.appendHistory(projectId, snapshot.sessionId, {
        type: "instruction-basis.resolved",
        basisId: snapshot.basisId,
        acceptedTurn
      });
    } catch (error) {
      await rm(path, { force: true });
      throw error;
    }
    return snapshot;
  }

  async get(projectId: string, sessionId: string, basisId: string): Promise<InstructionBasisSnapshot> {
    await this.projects.requireAuthorized(projectId);
    assertSafeIdentifier(sessionId, "sessionId");
    assertSafeIdentifier(basisId, "basisId");
    const snapshot = await readJson<InstructionBasisSnapshot>(
      this.basisFile(projectId, sessionId, basisId)
    ).catch((error: NodeJS.ErrnoException) => {
      if (error.code === "ENOENT") {
        throw new RuntimeError("NOT_FOUND", `Unknown instruction basis: ${basisId}`, 404);
      }
      throw error;
    });
    this.validateSnapshot(snapshot);
    if (snapshot.sessionId !== sessionId || snapshot.basisId !== basisId) {
      throw new RuntimeError("INTERNAL_FAILURE", "Invalid instruction basis identity", 500);
    }
    return snapshot;
  }

  async appendHistory(
    projectId: string,
    sessionId: string,
    input: InstructionHistoryInput
  ): Promise<InstructionHistoryRecord> {
    assertSafeIdentifier(sessionId, "sessionId");
    this.validateHistoryInput(input);
    const path = this.historyFile(projectId, sessionId);
    return this.withHistoryLock(path, async () => {
      await this.projects.requireAuthorized(projectId);
      const history = await this.history(projectId, sessionId);
      const record = {
        ...input,
        schemaVersion: "chirality.instruction-history/v1" as const,
        historyId: randomUUID(),
        sessionId,
        sequence: history.length,
        timestamp: new Date().toISOString()
      } as InstructionHistoryRecord;
      await appendJsonLine(path, record);
      return record;
    });
  }

  async appendTrustedNativePlanRevision(projectId: string, sessionId: string, revision: NativePlanRevision): Promise<InstructionHistoryRecord> {
    assertAdmittedNativePlanEvent(revision.sourceEvent);
    const evidence = revision.sourceEvent.qualificationState === "qualified" ? revision.sourceEvent.qualification : revision.sourceEvent.admission;
    const input: NativePlanRevisedHistoryRecord = {
      type: "native-plan.revised",
      revision,
      revisionSha256: sha256(JSON.stringify(revision)),
      ...(revision.sourceEvent.qualificationState === "qualified"
        ? { qualificationSha256: sha256(JSON.stringify(evidence)) }
        : { admissionSha256: sha256(JSON.stringify(evidence)) }),
      provenance: "trusted-native-plan-registry"
    };
    assertSafeIdentifier(sessionId, "sessionId");
    this.validateNativePlanRevision(input, true);
    const path = this.historyFile(projectId, sessionId);
    return this.withHistoryLock(path, async () => {
      await this.projects.requireAuthorized(projectId);
      const history = await this.historyUnlocked(path, sessionId);
      const existing = history.filter(record => record.type === "native-plan.revised");
      if (existing.some(record => record.revision.revision === revision.revision || record.revision.sourceEvent.eventId === revision.sourceEvent.eventId)) {
        const identical = existing.find(record => record.revision.revision === revision.revision && record.revision.sourceEvent.eventId === revision.sourceEvent.eventId && JSON.stringify(record.revision) === JSON.stringify(revision));
        if (identical !== undefined) return identical;
        throw invalid("Native Plan revision or source event conflicts with recorded history");
      }
      if (existing.some(record => record.revision.revision > revision.revision)) throw invalid("Native Plan revisions must be recorded in increasing order");
      const record = { ...input, schemaVersion: "chirality.instruction-history/v1" as const, historyId: randomUUID(), sessionId, sequence: history.length, timestamp: new Date().toISOString() } as InstructionHistoryRecord;
      await appendJsonLine(path, record);
      return record;
    });
  }

  async appendHistoryBatchWithCommit<T>(
    projectId: string,
    sessionId: string,
    inputs: readonly InstructionHistoryInput[],
    commit: () => Promise<T>
  ): Promise<{ records: readonly InstructionHistoryRecord[]; result: T }> {
    assertSafeIdentifier(sessionId, "sessionId");
    for (const input of inputs) this.validateHistoryInput(input);
    const path = this.historyFile(projectId, sessionId);
    return this.withHistoryLock(path, async () => {
      await this.projects.requireAuthorized(projectId);
      const history = await this.historyUnlocked(path, sessionId);
      const priorSize = await stat(path).then(value => value.size).catch((error: NodeJS.ErrnoException) => error.code === "ENOENT" ? 0 : Promise.reject(error));
      const records = inputs.map((input, offset) => ({ ...input, schemaVersion: "chirality.instruction-history/v1" as const, historyId: randomUUID(), sessionId, sequence: history.length + offset, timestamp: new Date().toISOString() } as InstructionHistoryRecord));
      try {
        for (const record of records) await appendJsonLine(path, record);
        const result = await commit();
        return { records, result };
      } catch (error) {
        if (priorSize === 0) await rm(path, { force: true });
        else await truncate(path, priorSize);
        throw error;
      }
    });
  }

  async history(projectId: string, sessionId: string): Promise<readonly InstructionHistoryRecord[]> {
    await this.projects.requireAuthorized(projectId);
    assertSafeIdentifier(sessionId, "sessionId");
    return this.historyUnlocked(this.historyFile(projectId, sessionId), sessionId);
  }

  private async historyUnlocked(path: string, sessionId: string): Promise<readonly InstructionHistoryRecord[]> {
    const source = await readFile(path, "utf8").catch(
      (error: NodeJS.ErrnoException) => {
        if (error.code === "ENOENT") return "";
        throw error;
      }
    );
    const records: InstructionHistoryRecord[] = [];
    for (const line of source.split("\n")) {
      if (line.trim() === "") continue;
      let record: InstructionHistoryRecord;
      try {
        record = JSON.parse(line) as InstructionHistoryRecord;
      } catch {
        throw new RuntimeError("INTERNAL_FAILURE", "Malformed instruction history", 500);
      }
      if (
        record.schemaVersion !== "chirality.instruction-history/v1" ||
        record.sessionId !== sessionId ||
        record.sequence !== records.length
      ) {
        throw new RuntimeError("INTERNAL_FAILURE", "Invalid instruction history ordering", 500);
      }
      this.validateHistoryInput(record, true);
      records.push(record);
    }
    return records;
  }

  private validateSnapshot(snapshot: InstructionBasisSnapshot): void {
    if (
      snapshot.schemaVersion !== "chirality.instruction-basis/v1" ||
      !nonempty(snapshot.roleId) ||
      !nonempty(snapshot.interactionMode) ||
      !nonempty(snapshot.permissionMode) ||
      !Array.isArray(snapshot.selectedMethods) ||
      (snapshot.instructionPolicySha256 !== undefined && !validHash(snapshot.instructionPolicySha256)) ||
      !Array.isArray(snapshot.compatibilityInputs) ||
      !Array.isArray(snapshot.compatibilityMappings) ||
      !Array.isArray(snapshot.suppliedEntries) ||
      !Array.isArray(snapshot.methodDispositions)
    ) {
      throw invalid("Invalid instruction basis snapshot");
    }
    for (const entry of snapshot.suppliedEntries) this.validateEntry(entry);
  }

  private validateEntry(entry: FrozenInstructionEntry): void {
    if (
      !["root", "project", "role", "catalog-description", "selection-metadata", "method-body", "resource"].includes(entry.kind) ||
      !nonempty(entry.id) ||
      !nonempty(entry.origin) ||
      !nonempty(entry.path) ||
      !validHash(entry.sha256) ||
      sha256(entry.content) !== entry.sha256
    ) {
      throw invalid("Instruction entry content does not match its declared identity");
    }
  }

  private validateHistoryInput(input: InstructionHistoryInput, trustedRead = false): void {
    switch (input.type) {
      case "selection.changed":
        if (
          !nonempty(input.roleId) ||
          !nonempty(input.interactionMode) ||
          !nonempty(input.permissionMode) ||
          !Array.isArray(input.selectedMethods) ||
          !input.selectedMethods.every(validQualifiedMethod) ||
          (input.instructionPolicySha256 !== undefined && !validHash(input.instructionPolicySha256))
        ) throw invalid("Invalid selection history record");
        if (
          input.reason === "agent-load" &&
          (
            !nonempty(input.turnId) ||
            !nonempty(input.invocationId) ||
            !nonempty(input.acceptedTurn?.turnId) ||
            !nonempty(input.acceptedTurn?.eventId) ||
            input.acceptedTurn.turnId !== input.turnId
          )
        ) {
          throw invalid("Agent-loaded selection history requires original invocation and accepted-turn identity");
        }
        return;
      case "resource.loaded":
        if (!nonempty(input.turnId) || !nonempty(input.invocationId)) {
          throw invalid("Resource load history requires turn and invocation identity");
        }
        this.validateEntry({ ...input, kind: input.resourceKind });
        return;
      case "native-child.method-loaded":
        if (!/^[a-f0-9]{32}$/u.test(input.associationId) || !nonempty(input.supplierGeneration) || !nonempty(input.parentSessionId) || !nonempty(input.rootThreadId) || !nonempty(input.rootTurnId) || !nonempty(input.parentTurnId)
          || !nonempty(input.childThreadId) || !nonempty(input.childTurnId) || !nonempty(input.invocationId)
          || !/^[a-f0-9]{64}$/u.test(input.roleBasisDigest) || !/^[a-f0-9]{64}$/u.test(input.inheritedToolsDigest)
          || !/^[a-f0-9]{64}$/u.test(input.instructionPolicySha256) || !nonempty(input.childInstructionBasisId) || !Array.isArray(input.selectedMethods) || !input.selectedMethods.every(validQualifiedMethod)
          || !Array.isArray(input.loadedEntries)) throw invalid("Invalid native child method activation history");
        for (const entry of input.loadedEntries) this.validateHistoryInput(entry);
        return;
      case "instruction-basis.resolved":
        assertSafeIdentifier(input.basisId, "basisId");
        if (!nonempty(input.acceptedTurn?.turnId) || !nonempty(input.acceptedTurn?.eventId)) {
          throw invalid("Resolved instruction basis requires an accepted turn identity");
        }
        return;
      case "method-change.requested":
        if (
          !nonempty(input.turnId) ||
          !nonempty(input.invocationId) ||
          input.acceptedTurn?.turnId !== input.turnId ||
          !nonempty(input.acceptedTurn?.eventId) ||
          (input.mode !== "merge" && input.mode !== "replace") ||
          !Array.isArray(input.methods) ||
          !input.methods.every(validQualifiedMethod) ||
          !Number.isSafeInteger(input.expectedRevision) ||
          input.expectedRevision < 0 ||
          (input.expectedBasisId !== undefined && !nonempty(input.expectedBasisId))
        ) throw invalid("Invalid pending method-change request");
        return;
      case "method-change.applied":
        if (
          !nonempty(input.requestHistoryId) ||
          !Number.isSafeInteger(input.resultingRevision) ||
          input.resultingRevision < 0 ||
          (input.resultingBasisId !== undefined && !nonempty(input.resultingBasisId)) ||
          !Array.isArray(input.selectedMethods) ||
          !input.selectedMethods.every(validQualifiedMethod)
        ) throw invalid("Invalid applied method-change record");
        return;
      case "method-change.failed":
        if (!nonempty(input.requestHistoryId) || !nonempty(input.code) || !nonempty(input.message)) {
          throw invalid("Invalid failed method-change record");
        }
        return;
      case "native-plan.revised":
        this.validateNativePlanRevision(input, false, trustedRead);
        return;
      case "provider-span.continued":
        if (
          !nonempty(input.preparationId) ||
          !nonempty(input.adapterId) ||
          !nonempty(input.providerId) ||
          !nonempty(input.engineSessionId) ||
          !nonempty(input.spanId) ||
          !nonempty(input.sessionInitEventId) ||
          !plainObject(input.continuationBoundary)
        ) throw invalid("Invalid provider continuation record");
        return;
      case "provider-span.prepared":
        this.validateProviderSpanTransition(input);
        return;
      case "provider-span.committed":
        this.validateProviderSpanTransition(input);
        if (!nonempty(input.commitmentReference)) throw invalid("Committed provider span requires a commitment reference");
        return;
      case "provider-span.cancelled":
        this.validateProviderSpanTransition(input);
        if (!nonempty(input.reason)) throw invalid("Cancelled provider span requires a reason");
        return;
      case "provider-span.failed":
        this.validateProviderSpanTransition(input);
        if (!nonempty(input.code) || !nonempty(input.message)) {
          throw invalid("Failed provider span requires code and message");
        }
        return;
      default:
        throw invalid("Unsupported instruction history record");
    }
  }

  private validateNativePlanRevision(input: NativePlanRevisedHistoryRecord, trustedWrite: boolean, trustedRead = false): void {
    try {
      if (!Number.isSafeInteger(input.revision.revision) || input.revision.revision < 1) throw new Error("revision");
      assertAdmittedNativePlanEvent(input.revision.sourceEvent);
      if (input.provenance === "trusted-native-plan-registry") {
        if (!validHash(input.revisionSha256) || input.revisionSha256 !== sha256(JSON.stringify(input.revision))) throw new Error("revision hash");
        const evidence = input.revision.sourceEvent.qualificationState === "qualified" ? input.revision.sourceEvent.qualification : input.revision.sourceEvent.admission;
        if (input.revision.sourceEvent.qualificationState === "qualified"
          ? (!validHash(input.qualificationSha256) || input.admissionSha256 !== undefined || input.qualificationSha256 !== sha256(JSON.stringify(evidence)))
          : (!validHash(input.admissionSha256) || input.qualificationSha256 !== undefined || input.admissionSha256 !== sha256(JSON.stringify(evidence)))) throw new Error("admission hash");
        if (!trustedWrite && !trustedRead) throw new Error("untrusted append");
        return;
      }
      if (this.options.validateNativePlanRevision === undefined) throw new Error("validator");
      this.options.validateNativePlanRevision(input.revision);
    } catch {
      throw invalid("Native plan revisions require trusted adapter qualification evidence");
    }
  }

  private validateProviderSpanTransition(input: ProviderSpanTransitionIdentity): void {
    if (
      !nonempty(input.preparationId) ||
      !nonempty(input.adapterId) ||
      !nonempty(input.providerId) ||
      !nonempty(input.predecessor?.engineSessionId) ||
      !nonempty(input.targetBasisId) ||
      !nonempty(input.targetReference) ||
      !validHash(input.continuationHash)
    ) {
      throw invalid("Invalid provider span transition identity");
    }
  }

  private async withHistoryLock<T>(path: string, operation: () => Promise<T>): Promise<T> {
    const previous = historyLocks.get(path) ?? Promise.resolve();
    const result = previous.then(operation);
    const queued = result.then(() => undefined, () => undefined);
    historyLocks.set(path, queued);
    try {
      return await result;
    } finally {
      if (historyLocks.get(path) === queued) historyLocks.delete(path);
    }
  }

  private sessionDirectory(projectId: string, sessionId: string): string {
    assertSafeIdentifier(projectId, "projectId");
    assertSafeIdentifier(sessionId, "sessionId");
    return join(this.runtimeDirectory, "projects", projectId, "sessions", sessionId);
  }

  private basisFile(projectId: string, sessionId: string, basisId: string): string {
    return join(this.sessionDirectory(projectId, sessionId), "instruction-bases", `${basisId}.json`);
  }

  private historyFile(projectId: string, sessionId: string): string {
    return join(this.sessionDirectory(projectId, sessionId), "instruction-history.jsonl");
  }
}

function invalid(message: string): RuntimeError {
  return new RuntimeError("INVALID_REQUEST", message, 400);
}

function conflict(message: string): RuntimeError {
  return new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", message, 409);
}

function nonempty(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

function validHash(value: unknown): value is string {
  return typeof value === "string" && /^[a-f0-9]{64}$/.test(value);
}

function plainObject(value: unknown): value is Readonly<Record<string, unknown>> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function validQualifiedMethod(value: unknown): value is QualifiedMethodReference {
  if (!plainObject(value)) return false;
  return nonempty(value["sourceRootId"]) &&
    ["project", "user", "bundled"].includes(String(value["source"])) &&
    ["skill", "workflow"].includes(String(value["kind"])) &&
    nonempty(value["name"]);
}

function sameFrozenMaterial(
  current: InstructionBasisSnapshot,
  candidate: InstructionBasisSnapshot
): boolean {
  const { createdAt: _currentCreatedAt, ...currentMaterial } = current;
  const { createdAt: _candidateCreatedAt, ...candidateMaterial } = candidate;
  return canonicalJson(currentMaterial) === canonicalJson(candidateMaterial);
}

function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (plainObject(value)) {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

async function writeNewJson(path: string, value: unknown): Promise<void> {
  await ensurePrivateDirectory(dirname(path));
  const handle = await open(path, "wx", 0o600).catch((error: NodeJS.ErrnoException) => {
    if (error.code === "EEXIST") throw conflict("An instruction basis is frozen and cannot be replaced");
    throw error;
  });
  try {
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`, "utf8");
    await handle.sync();
  } finally {
    await handle.close();
  }
}
