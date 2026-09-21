import { randomUUID } from "node:crypto";
import { homedir } from "node:os";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { lstat, mkdir, open, readFile, realpath } from "node:fs/promises";
import {
  assertAdmittedNativePlanEvent,
  CHIRALITY_ROLE_NAMES,
  RuntimeError,
  type ChiralityRoleName,
  type MethodInspectionResponse,
  type MethodReference,
  type MethodsResponse,
  type NativePlanCapabilityResponse,
  type NativePlanClarificationsResponse,
  type NativePlanRevision,
  type NativePlanRevisionsResponse,
  type QualifiedMethodReference,
  type ReplaceSelectedMethodsRequest,
  type ReplaceSelectedMethodsResponse,
  type ResolveSelectedContextRequest,
  type ResolveSelectedContextResponse,
  type RolesResponse,
  type RuntimeSessionRecord,
  type RuntimeToolDefinition,
  type AgentEnginePort,
  type PreparedContextSuccessor,
  type ExportNativePlanRequest,
  type ExportNativePlanResponse,
  type ReplyNativePlanClarificationRequest,
  type ReplyNativePlanClarificationResponse,
  type SelectedMethodDisposition,
  type SuppliedContextEntry
} from "@chirality/runtime-contracts";
import { sha256 } from "./fs.js";
import type { InstructionBasisSnapshot, FrozenInstructionEntry } from "./instruction-basis-store.js";
import {
  MethodCatalogError,
  discoverMethodCatalog,
  formatQualifiedMethodId,
  inspectMethod as inspectCatalogMethod,
  loadRoles,
  normalizeMethodSelection,
  parseQualifiedMethodId,
  readMethodResource,
  resolveMethodReferences,
  type CatalogMethodEntry,
  type MethodCatalog,
  type MethodSourceRoot
} from "./method-catalog.js";
import type { ProjectRegistry } from "./project-registry.js";
import type { EngineRegistry } from "./engine-registry.js";
import type { SessionStore } from "./session-store.js";
import { evaluateMethodTransition } from "./method-transition.js";

export interface TrustedNativePlanAdapterRegistry {
  capability(session: RuntimeSessionRecord): Promise<NativePlanCapabilityResponse>;
  revisions(projectId: string, sessionId: string): Promise<NativePlanRevisionsResponse>;
  clarifications?(projectId: string, sessionId: string): Promise<NativePlanClarificationsResponse>;
  replyClarification?(projectId: string, sessionId: string, request: ReplyNativePlanClarificationRequest): Promise<{ sent: true }>;
}

interface ResolvedInternal {
  response: ResolveSelectedContextResponse;
  snapshot: InstructionBasisSnapshot;
  activeInstructionPolicySha256: string;
}

const READ_TOOL = /^(?:read|read_file|search|find|list|inspect|catalog|chirality_)/u;
const responseAdmission = (value: Exclude<NativePlanCapabilityResponse | NativePlanRevisionsResponse | NativePlanClarificationsResponse, { status: "unavailable" }>) =>
  value.status === "qualified" ? value.qualification : value.admission;
const eventAdmission = (event: NativePlanRevision["sourceEvent"]) => event.qualificationState === "qualified" ? event.qualification : event.admission;

export interface ProductInstructionOptions {
  productInstructionsPath?: string;
  nativeProjectDiscovery?: boolean;
}

export class RuntimeMethodService {
  private readonly nativeChildActivationLocks = new Map<string, Promise<void>>();
  constructor(
    private readonly projects: ProjectRegistry,
    private readonly sessions: SessionStore,
    private readonly engines: EngineRegistry,
    private readonly nativePlan?: TrustedNativePlanAdapterRegistry,
    private readonly productInstructions: ProductInstructionOptions = {}
  ) {}

  async listRoles(projectId: string): Promise<RolesResponse> {
    const roots = await this.projects.roots(projectId);
    return this.mapError(() => loadRoles(roots.instructionRoot));
  }

  async listMethods(projectId: string): Promise<MethodsResponse> {
    return (await this.catalog(projectId)).response;
  }

  private async withNativeChildActivationLock<T>(identity: string, action: () => Promise<T>): Promise<T> {
    const previous = this.nativeChildActivationLocks.get(identity) ?? Promise.resolve();
    let release!: () => void;
    const current = previous.then(() => new Promise<void>(resolve => { release = resolve; }));
    this.nativeChildActivationLocks.set(identity, current);
    await previous;
    try { return await action(); }
    finally { release(); if (this.nativeChildActivationLocks.get(identity) === current) this.nativeChildActivationLocks.delete(identity); }
  }

  async inspectMethod(projectId: string, qualifiedId: string): Promise<MethodInspectionResponse> {
    const catalog = await this.catalog(projectId);
    let reference: QualifiedMethodReference;
    try { reference = parseQualifiedMethodId(qualifiedId); }
    catch (error) { throw this.runtimeError(error); }
    const resolved = resolveMethodReferences(catalog, [reference])[0];
    if (resolved?.status !== "resolved") this.throwResolution(resolved, qualifiedId);
    return this.mapError(() => inspectCatalogMethod(resolved.method));
  }

  async resolveSelectedContext(
    projectId: string,
    sessionId: string,
    request: ResolveSelectedContextRequest
  ): Promise<ResolveSelectedContextResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    const roleId = this.roleId(session);
    if (request.roleId !== roleId) {
      throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Context role must match the authorized session role", 409);
    }
    return (await this.resolveInternal(projectId, session, request)).response;
  }

  async resolveForTurn(
    projectId: string,
    session: RuntimeSessionRecord,
    request: Partial<ResolveSelectedContextRequest> = {}
  ): Promise<ResolvedInternal> {
    const roleId = this.roleId(session);
    const resolved = await this.resolveInternal(projectId, session, {
      roleId,
      interactionMode: request.interactionMode ?? session.interactionMode ?? "chat",
      permissionMode: request.permissionMode ?? session.permissionMode ?? "ask",
      methods: request.methods ?? session.selectedMethods ?? [],
      ...(request.resources === undefined ? {} : { resources: request.resources }),
      ...(request.workflow === undefined ? {} : { workflow: request.workflow }),
      ...(request.taskSkill === undefined ? {} : { taskSkill: request.taskSkill })
    });
    const instructionHistory = await this.sessions.instructionBases.history(projectId, session.sessionId);
    const lastAccepted = [...instructionHistory].reverse().find(record => record.type === "instruction-basis.resolved");
    const successor = session.adapterSession?.contextSuccessor;
    if (successor !== undefined) {
      const prepared = instructionHistory.find(record => record.type === "provider-span.prepared" && record.preparationId === successor.preparationId);
      const committed = instructionHistory.find(record => record.type === "provider-span.committed" && record.preparationId === successor.preparationId);
      const invalidated = instructionHistory.find(record => (record.type === "provider-span.cancelled" || record.type === "provider-span.failed") && record.preparationId === successor.preparationId);
      if (prepared === undefined || committed === undefined || invalidated !== undefined) {
        await this.engines.resolve(session.engineSelection).cancelContextSuccessor?.(successor.preparationId).catch(() => undefined);
        await this.sessions.failProviderSpanPreparation(projectId, session.sessionId, successor.preparationId, { code: "UNCOMMITTED_SUCCESSOR_PROJECTION", message: "Provider successor projection has no durable committed preparation" }).catch(() => undefined);
        await this.sessions.clearContextSuccessor(projectId, session.sessionId, successor.preparationId);
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Provider successor projection has no durable committed preparation", 409, { preparationId: successor.preparationId });
      }
      const expectedReference = `${resolved.response.basisPreview.id}:${resolved.response.basisPreview.sha256}`;
      if (successor.targetBasisId !== resolved.response.basisPreview.id || successor.targetReference !== expectedReference) {
        await this.engines.resolve(session.engineSelection).cancelContextSuccessor?.(successor.preparationId).catch(() => undefined);
        await this.sessions.failProviderSpanPreparation(projectId, session.sessionId, successor.preparationId, { code: "INSTRUCTION_BASIS_DRIFT", message: "Prepared successor target no longer matches the freshly resolved instruction basis" }).catch(() => undefined);
        await this.sessions.clearContextSuccessor(projectId, session.sessionId, successor.preparationId);
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Prepared successor target no longer matches the freshly resolved instruction basis", 409, { expectedBasisId: successor.targetBasisId, actualBasisId: resolved.response.basisPreview.id });
      }
    }
    // An engine without successor preparation keeps its provider thread and
    // supplies changed developer instructions at its verified adoption boundary;
    // changed instruction bytes are re-frozen with the accepting turn.
    const additiveEngine = this.engines.resolve(session.engineSelection).prepareContextSuccessor === undefined;
    if (lastAccepted?.type === "instruction-basis.resolved" && !additiveEngine) {
      const accepted = await this.sessions.instructionBases.get(projectId, session.sessionId, lastAccepted.basisId);
      const latestLoad = [...instructionHistory].reverse().find(record => record.type === "selection.changed" && record.reason === "agent-load");
      const intentionalDynamicBaseline = latestLoad?.type === "selection.changed"
        && latestLoad.sequence > lastAccepted.sequence
        && "instructionPolicySha256" in latestLoad
        && latestLoad.instructionPolicySha256 === resolved.response.basisPreview.instructionPolicySha256;
      if (accepted.instructionPolicySha256 !== undefined
        && accepted.instructionPolicySha256 !== resolved.response.basisPreview.instructionPolicySha256
        && successor === undefined
        && !intentionalDynamicBaseline) {
        throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Instruction or effective method policy changed after the accepted basis", 409, { successorRequired: true, acceptedInstructionPolicySha256: accepted.instructionPolicySha256, resolvedInstructionPolicySha256: resolved.response.basisPreview.instructionPolicySha256 });
      }
    }
    const current = (session.selectedMethods ?? []).map(formatQualifiedMethodId);
    const next = resolved.response.methods.map(method => formatQualifiedMethodId(this.reference(method)));
    const changed = current.length !== next.length || current.some((value, index) => value !== next[index]);
    if (request.methods !== undefined && changed && session.instructionBasisId !== "basis-pending") {
      throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Turn methods cannot bypass the selected-method transition endpoint", 409, { selectionEndpointRequired: true });
    }
    return resolved;
  }

  async replaceSelectedMethods(
    projectId: string,
    sessionId: string,
    request: ReplaceSelectedMethodsRequest
  ): Promise<ReplaceSelectedMethodsResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    if (request.expectedBasisId !== undefined && request.expectedBasisId !== session.instructionBasisId) {
      throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Instruction basis changed before method replacement", 409);
    }
    if (request.expectedRevision !== undefined && request.expectedRevision !== (session.methodSelectionRevision ?? 0)) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Method selection revision changed before replacement", 409);
    const targetRoleId = request.roleId ?? this.roleId(session);
    const targetRole = (await this.listRoles(projectId)).roles.find(role => role.id === targetRoleId);
    if (targetRole === undefined || (!targetRole.directEntry && targetRoleId !== this.roleId(session))) throw new RuntimeError("INVALID_REQUEST", `Role '${targetRoleId}' is unavailable for direct session transition`, 400);
    if (this.roleId(session) === "TASK" && targetRoleId !== "TASK") throw new RuntimeError("FORBIDDEN", "A TASK session cannot promote itself to a manager role", 403);
    let resolved!: ResolvedInternal;
    let prepared: PreparedContextSuccessor | undefined;
    let preparedEngine: AgentEnginePort | undefined;
    let additive = false;
    const revision = (session.methodSelectionRevision ?? 0) + 1;
    try { await this.sessions.mutateSelection(projectId, sessionId, { instructionBasisId: session.instructionBasisId, methodSelectionRevision: session.methodSelectionRevision ?? 0 }, async (current, lockedSnapshot) => {
      const replay = lockedSnapshot.events;
      const priorTurnAccepted = replay.some(event => event.type === "turn.accepted");
      const instructionHistory = lockedSnapshot.instructionHistory;
      const acceptedBasisId = instructionHistory.filter(record => record.type === "instruction-basis.resolved").at(-1)?.basisId;
      const acceptedBasis = acceptedBasisId === undefined ? undefined : await this.sessions.instructionBases.get(projectId, sessionId, acceptedBasisId);
      const acceptedMethods = acceptedBasis?.selectedMethods;
      const priorBasisRefs = await Promise.all([...new Set(instructionHistory.filter(record => record.type === "instruction-basis.resolved").map(record => record.basisId))].map(async basisId => {
        const snapshot = await this.sessions.instructionBases.get(projectId, sessionId, basisId);
        return { basisId, sha256: sha256(JSON.stringify(snapshot)) };
      }));
      const selectionMode = request.selectionMode ?? "replace";
      if (selectionMode === "merge" && (request.methods === undefined || request.methods.length === 0)) throw new RuntimeError("INVALID_REQUEST", "Merge selection requires at least one method", 400);
      const requestedMethods = request.methods === undefined ? (current.selectedMethods ?? []) : selectionMode === "merge" ? [...(current.selectedMethods ?? []), ...request.methods] : request.methods;
      resolved = await this.resolveInternal(projectId, current, { roleId: targetRoleId, interactionMode: current.interactionMode ?? "chat", permissionMode: current.permissionMode ?? "ask", methods: requestedMethods });
      let references = resolved.response.methods.map(method => this.reference(method));
      if (selectionMode === "merge") {
        references = [...new Map(references.map(reference => [formatQualifiedMethodId(reference), reference])).values()];
        if (references.length !== resolved.response.methods.length) resolved = await this.resolveInternal(projectId, current, { roleId: targetRoleId, interactionMode: current.interactionMode ?? "chat", permissionMode: current.permissionMode ?? "ask", methods: references });
      }
      const decision = evaluateMethodTransition({ sessionId, sessionStatus: current.status, currentRoleId: this.roleId(current), nextRoleId: targetRoleId, currentMethods: current.selectedMethods ?? [], nextMethods: references, methodCompatibility: resolved.response.dispositions.every(value => value.route === "primary") ? "compatible" : "incompatible", boundaryConfirmed: request.boundaryConfirmed === true });
      const changed = decision.selectedMethods.length !== (current.selectedMethods ?? []).length || decision.selectedMethods.some((value, index) => formatQualifiedMethodId(value) !== formatQualifiedMethodId((current.selectedMethods ?? [])[index]!));
      const changedFromAccepted = acceptedMethods !== undefined && (references.length !== acceptedMethods.length || references.some((value, index) => formatQualifiedMethodId(value) !== formatQualifiedMethodId(acceptedMethods[index]!)));
      const policyChangedFromAccepted = acceptedBasis?.instructionPolicySha256 !== undefined && acceptedBasis.instructionPolicySha256 !== resolved.response.basisPreview.instructionPolicySha256;
      const needsSuccessor = (changed || changedFromAccepted || policyChangedFromAccepted || targetRoleId !== this.roleId(current)) && (current.engineSessionId !== undefined || priorTurnAccepted || acceptedMethods !== undefined);
      let providerSpanPreparation: import("./instruction-basis-store.js").ProviderSpanPreparedHistoryRecord | undefined;
      const engineForTransition = this.engines.resolve(current.engineSelection);
      // Additive engines (no successor preparation) keep their thread; the
      // next turn carries the changed instructions as a context update.
      additive = needsSuccessor && engineForTransition.prepareContextSuccessor === undefined;
      if (needsSuccessor && !additive) {
        const engine = engineForTransition;
        if (engine.prepareContextSuccessor === undefined || engine.cancelContextSuccessor === undefined || current.engineSessionId === undefined) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Selected adapter cannot prepare a reversible context successor", 409, { successorAvailable: false });
        const dialogue: { role: "user" | "assistant"; content: string; turnId?: string }[] = [];
        for (const event of replay) {
          if (event.type === "turn.accepted" && typeof event.data.message === "string") dialogue.push({ role: "user", content: event.data.message, ...(event.turnId ? { turnId: event.turnId } : {}) });
          if (event.type === "message.delta") {
            const content = typeof event.data.text === "string" ? event.data.text : typeof event.data.delta === "string" ? event.data.delta : "";
            if (!content) continue;
            const last = dialogue.at(-1);
            if (last?.role === "assistant" && last.turnId === event.turnId) last.content += content;
            else dialogue.push({ role: "assistant", content, ...(event.turnId ? { turnId: event.turnId } : {}) });
          }
        }
        const transcript = JSON.stringify(dialogue);
        const adapterPrepared = await engine.prepareContextSuccessor({ sessionId, predecessorEngineSessionId: current.engineSessionId, fromBasisId: current.instructionBasisId ?? "legacy", toBasisPreview: { id: resolved.response.basisPreview.id, sha256: resolved.response.basisPreview.sha256 }, continuationContext: { transcript, sha256: sha256(transcript), priorBasisRefs } });
        prepared = adapterPrepared;
        preparedEngine = engine;
        if (adapterPrepared.adapterId !== current.engineSelection.adapterId || adapterPrepared.providerId !== current.engineSelection.providerId || adapterPrepared.predecessorEngineSessionId !== current.engineSessionId || adapterPrepared.targetBasisId !== resolved.response.basisPreview.id || adapterPrepared.targetReference !== `${resolved.response.basisPreview.id}:${resolved.response.basisPreview.sha256}` || adapterPrepared.continuationSha256 !== sha256(adapterPrepared.continuationText)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Adapter returned an invalid context successor preparation", 502);
        providerSpanPreparation = { type: "provider-span.prepared", preparationId: adapterPrepared.preparationId, adapterId: adapterPrepared.adapterId, providerId: adapterPrepared.providerId, predecessor: { engineSessionId: current.engineSessionId }, targetBasisId: adapterPrepared.targetBasisId, targetReference: adapterPrepared.targetReference, continuationHash: adapterPrepared.continuationSha256 };
      }
      const nextRole = targetRoleId === "HELP_HUMAN" ? { role: "agent0" as const, agentType: 0 as const } : targetRoleId === "TASK" ? { role: "agent2" as const, agentType: 2 as const } : { role: "agent1" as const, agentType: 1 as const };
      const next = { ...current, schemaVersion: "chirality.session/v3" as const, roleId: targetRoleId, ...nextRole, persona: targetRoleId === this.roleId(current) ? current.persona : targetRoleId, interactionMode: current.interactionMode ?? "chat", permissionMode: current.permissionMode ?? "ask", selectedMethods: references, methodSelectionRevision: revision, instructionBasisId: resolved.response.basisPreview.id, ...(prepared === undefined ? {} : { adapterSession: { ...(current.adapterSession ?? {}), contextSuccessor: prepared } }) };
      return { session: next, history: { type: "selection.changed" as const, roleId: next.roleId, interactionMode: next.interactionMode, permissionMode: next.permissionMode, selectedMethods: references, reason: "runtime-api" }, ...(providerSpanPreparation === undefined ? {} : { providerSpanPreparation, providerSpanCommitmentReference: `selection:${revision}` }) };
    });
    } catch (error) { if (prepared && preparedEngine?.cancelContextSuccessor) await preparedEngine.cancelContextSuccessor(prepared.preparationId).catch(() => undefined); if (prepared) await this.sessions.cancelProviderSpanPreparation(projectId, sessionId, prepared.preparationId, "selection replacement failed").catch(() => undefined); throw error; }
    return {
      schemaVersion: "chirality.selected-methods/v3",
      sessionId,
      revision,
      methods: resolved.response.methods.map(method => this.reference(method)),
      basisPreview: resolved.response.basisPreview,
      transition: prepared !== undefined
        ? { status: "prepared", successorAvailable: true, preparationId: prepared.preparationId }
        : additive ? { status: "additive", successorAvailable: false } : { status: "unchanged", successorAvailable: true }
    };
  }

  async applyPendingMethodChanges(projectId: string, sessionId: string, turnId: string): Promise<void> {
    const pending = (await this.sessions.pendingMethodChanges(projectId, sessionId)).filter(record => record.turnId === turnId);
    for (const request of pending) {
      try {
        const current = await this.sessions.get(projectId, sessionId);
        if ((current.methodSelectionRevision ?? 0) !== request.expectedRevision || current.instructionBasisId !== request.expectedBasisId) {
          throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Deferred method change became stale before the turn boundary", 409);
        }
        const result = await this.replaceSelectedMethods(projectId, sessionId, {
          expectedRevision: request.expectedRevision,
          ...(request.expectedBasisId === undefined ? {} : { expectedBasisId: request.expectedBasisId }),
          boundaryConfirmed: true,
          selectionMode: request.mode,
          methods: request.methods
        });
        await this.sessions.settleMethodChange(projectId, sessionId, request.historyId, { resultingRevision: result.revision, resultingBasisId: result.basisPreview.id, selectedMethods: result.methods });
      } catch (error) {
        const failure = error instanceof RuntimeError ? error : new RuntimeError("INTERNAL_FAILURE", (error as Error).message, 500);
        await this.sessions.settleMethodChange(projectId, sessionId, request.historyId, { failed: true, code: failure.code, message: failure.message }).catch(() => undefined);
      }
    }
  }

  async getNativePlanCapability(projectId: string, sessionId: string): Promise<NativePlanCapabilityResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    if (this.nativePlan === undefined) return { schemaVersion: "chirality.native-plan-capability/v3", status: "unavailable", reason: "No trusted admitted native Plan adapter is registered" };
    return this.nativePlan.capability(session);
  }

  async listNativePlanRevisions(projectId: string, sessionId: string): Promise<NativePlanRevisionsResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    let revisions = await this.persistedNativePlanRevisions(projectId, sessionId);
    let unavailableReason = "No trusted admitted native Plan adapter is registered";
    if (this.nativePlan !== undefined) {
      try {
        const [capability, live] = await Promise.all([this.nativePlan.capability(session), this.nativePlan.revisions(projectId, sessionId)]);
        unavailableReason = capability.status === "unavailable" ? capability.reason : live.status === "unavailable" ? live.reason : unavailableReason;
        if (capability.status !== "unavailable" && live.status !== "unavailable") {
          if (capability.status !== live.status || JSON.stringify(responseAdmission(capability)) !== JSON.stringify(responseAdmission(live))) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry admission changed while reading revisions", 503);
          let priorRevision = 0;
          const eventIds = new Set<string>();
          for (const revision of live.revisions) {
            try { assertAdmittedNativePlanEvent(revision.sourceEvent); } catch { throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry returned an unadmitted revision", 503); }
            if (!Number.isSafeInteger(revision.revision) || revision.revision <= priorRevision || eventIds.has(revision.sourceEvent.eventId)) {
              throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry returned conflicting or unordered revisions", 503);
            }
            const sameRevision = revisions.find(recorded => recorded.revision === revision.revision);
            const sameEvent = revisions.find(recorded => recorded.sourceEvent.eventId === revision.sourceEvent.eventId);
            if ((sameRevision !== undefined || sameEvent !== undefined) && JSON.stringify(sameRevision) !== JSON.stringify(revision)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry conflicts with durable revision history", 503);
            if (sameRevision === undefined && JSON.stringify(eventAdmission(revision.sourceEvent)) !== JSON.stringify(responseAdmission(capability))) throw new RuntimeError("ENGINE_UNAVAILABLE", "New Native Plan revision does not match the current trusted admission", 503);
            priorRevision = revision.revision;
            eventIds.add(revision.sourceEvent.eventId);
          }
          const newRevisions = live.revisions.filter(revision => !revisions.some(recorded => recorded.revision === revision.revision));
          if (newRevisions.length > 0 && newRevisions[0]!.revision <= (revisions.at(-1)?.revision ?? 0)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry revisions do not extend durable history", 503);
          for (const revision of newRevisions) await this.sessions.instructionBases.appendTrustedNativePlanRevision(projectId, sessionId, revision);
          revisions = await this.persistedNativePlanRevisions(projectId, sessionId);
        }
      } catch (error) {
        if (revisions.length === 0) unavailableReason = error instanceof Error ? error.message : unavailableReason;
      }
    }
    if (revisions.length === 0) return { schemaVersion: "chirality.native-plan-revisions/v3", status: "unavailable", reason: unavailableReason, revisions: [] };
    const latest = revisions.at(-1)!.sourceEvent;
    return latest.qualificationState === "qualified"
      ? { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification: latest.qualification, revisions }
      : { schemaVersion: "chirality.native-plan-revisions/v3", status: "trial", admission: latest.admission, revisions };
  }

  async listNativePlanClarifications(projectId: string, sessionId: string): Promise<NativePlanClarificationsResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    if (this.nativePlan?.clarifications === undefined) return { schemaVersion: "chirality.native-plan-clarifications/v3", status: "unavailable", reason: "No trusted admitted native Plan clarification bridge is registered", clarifications: [] };
    const [capability, pending] = await Promise.all([this.nativePlan.capability(session), this.nativePlan.clarifications(projectId, sessionId)]);
    if (capability.status === "unavailable") return { schemaVersion: "chirality.native-plan-clarifications/v3", status: "unavailable", reason: capability.reason, clarifications: [] };
    if (pending.status === "unavailable") return pending;
    if (capability.status !== pending.status || JSON.stringify(responseAdmission(capability)) !== JSON.stringify(responseAdmission(pending))) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan registry admission changed while reading clarifications", 503);
    return pending;
  }

  async replyNativePlanClarification(projectId: string, sessionId: string, request: ReplyNativePlanClarificationRequest): Promise<ReplyNativePlanClarificationResponse> {
    const session = await this.sessions.get(projectId, sessionId);
    if (this.nativePlan?.replyClarification === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", "No trusted admitted native Plan clarification bridge is registered", 503);
    const capability = await this.nativePlan.capability(session);
    if (capability.status === "unavailable") throw new RuntimeError("ENGINE_UNAVAILABLE", capability.reason, 503);
    if ((typeof request.requestId !== "string" && typeof request.requestId !== "number") || (typeof request.requestId === "string" && request.requestId.length === 0) || (typeof request.requestId === "number" && !Number.isSafeInteger(request.requestId))) throw new RuntimeError("INVALID_REQUEST", "Native Plan clarification reply requires an exact request identity");
    if (!request.answers || typeof request.answers !== "object" || Array.isArray(request.answers) || Object.keys(request.answers).length === 0) throw new RuntimeError("INVALID_REQUEST", "Native Plan clarification reply requires question answers");
    for (const [questionId, answer] of Object.entries(request.answers)) {
      if (!questionId || !answer || typeof answer !== "object" || !Array.isArray(answer.answers) || answer.answers.some(value => typeof value !== "string")) throw new RuntimeError("INVALID_REQUEST", "Native Plan clarification answers must preserve question IDs and answer arrays");
    }
    const delivered = await this.nativePlan.replyClarification(projectId, sessionId, request);
    if (delivered.sent !== true) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan clarification reply was not written to the provider transport", 503);
    return { schemaVersion: "chirality.native-plan-clarification-reply/v3", sessionId, requestId: request.requestId, sent: true };
  }

  async exportNativePlan(projectId: string, sessionId: string, request: ExportNativePlanRequest): Promise<ExportNativePlanResponse> {
    await this.sessions.get(projectId, sessionId);
    const targetParts = request.targetRelativePath.split(/[\\/]/u);
    if (!Number.isSafeInteger(request.revision) || request.revision < 1 || !request.targetRelativePath || isAbsolute(request.targetRelativePath) || request.targetRelativePath.includes("\0") || targetParts.some(part => part === "" || part === "." || part === "..")) {
      throw new RuntimeError("INVALID_REQUEST", "Native Plan export requires a positive revision and project-relative target");
    }
    const [revisions, project] = await Promise.all([this.persistedNativePlanRevisions(projectId, sessionId), this.projects.requireAuthorized(projectId)]);
    const revision = revisions.find(value => value.revision === request.revision);
    if (revision === undefined) {
      throw new RuntimeError("NOT_FOUND", `Unknown admitted native Plan revision: ${request.revision}`, 404);
    }
    const target = resolve(project.canonicalRoot, ...targetParts);
    if (!this.contained(project.canonicalRoot, target)) throw new RuntimeError("FORBIDDEN", "Native Plan export target escapes the project", 403);
    const canonicalRoot = await realpath(project.canonicalRoot);
    let parent = canonicalRoot;
    for (const part of targetParts.slice(0, -1)) {
      const next = join(parent, part);
      const metadata = await lstat(next).catch(error => (error as NodeJS.ErrnoException).code === "ENOENT" ? undefined : Promise.reject(error));
      if (metadata?.isSymbolicLink()) throw new RuntimeError("FORBIDDEN", "Native Plan export refuses symlinked ancestors", 403);
      if (metadata === undefined) await mkdir(next, { mode: 0o700 });
      else if (!metadata.isDirectory()) throw new RuntimeError("INVALID_REQUEST", "Native Plan export parent must be a directory");
      parent = await realpath(next);
      if (!this.contained(canonicalRoot, parent)) throw new RuntimeError("FORBIDDEN", "Native Plan export parent escapes the project", 403);
    }
    const existing = await lstat(target).catch(error => (error as NodeJS.ErrnoException).code === "ENOENT" ? undefined : Promise.reject(error));
    if (existing?.isSymbolicLink()) throw new RuntimeError("FORBIDDEN", "Native Plan export refuses symlink targets", 403);
    if (existing && request.overwrite !== true) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Native Plan export target already exists", 409);
    if (existing && !existing.isFile()) throw new RuntimeError("INVALID_REQUEST", "Native Plan export target must be a file");
    const plan = revision.sourceEvent.plan;
    const content = typeof plan === "string"
      ? (plan.endsWith("\n") ? plan : `${plan}\n`)
      : plan !== null && typeof plan === "object" && !Array.isArray(plan) && (plan as { type?: unknown }).type === "plan" && typeof (plan as { text?: unknown }).text === "string"
      ? ((plan as { text: string }).text.endsWith("\n") ? (plan as { text: string }).text : `${(plan as { text: string }).text}\n`)
      : `${JSON.stringify(plan, null, 2)}\n`;
    const handle = await open(target, request.overwrite === true ? "w" : "wx", 0o600);
    try { await handle.writeFile(content, "utf8"); await handle.sync(); } finally { await handle.close(); }
    return { schemaVersion: "chirality.native-plan-export/v3", sessionId, revision: request.revision, targetRelativePath: request.targetRelativePath, sha256: sha256(content) };
  }

  runtimeTools(projectId: string, sessionId: string, turnId: string, activeToolNames: readonly string[] = []): readonly RuntimeToolDefinition[] {
    const read = { effect: "allow" as const, operation: "read" as const };
    return [
      { name: "chirality_list_methods", description: "List authorized Chirality methods and their compatibility metadata.", inputSchema: { type: "object", additionalProperties: false }, permission: read,
        execute: async () => this.listMethods(projectId) },
      { name: "chirality_inspect_method", description: "Inspect one authorized method entrypoint and resource inventory.", inputSchema: { type: "object", properties: { qualifiedId: { type: "string" } }, required: ["qualifiedId"], additionalProperties: false }, permission: read,
        execute: async input => { const inspected = await this.inspectMethod(projectId, this.stringField(input, "qualifiedId")); return { schemaVersion: inspected.schemaVersion, method: inspected.method, entrypoint: { sha256: inspected.entrypoint.sha256 }, resources: inspected.resources }; } },
      { name: "chirality_load_method", description: "Resolve selected method context for this session without changing role or launching delegation.", inputSchema: { type: "object", properties: {
          methods: { type: "array", items: { type: "object", properties: { kind: { type: "string", enum: ["skill", "workflow"] }, name: { type: "string" }, sourceRootId: { type: "string" }, source: { type: "string", enum: ["project", "user", "bundled"] } }, required: ["kind", "name"], additionalProperties: false } },
          resources: { type: "array", items: { type: "object", properties: { method: { type: "object", properties: { kind: { type: "string", enum: ["skill", "workflow"] }, name: { type: "string" }, sourceRootId: { type: "string" }, source: { type: "string", enum: ["project", "user", "bundled"] } }, required: ["sourceRootId", "source", "kind", "name"], additionalProperties: false }, paths: { type: "array", items: { type: "string" } } }, required: ["method", "paths"], additionalProperties: false } }
        }, required: ["methods"], additionalProperties: false }, permission: read,
        execute: async (input, _signal, executionContext) => {
          if (!input || typeof input !== "object" || Array.isArray(input)) throw new RuntimeError("INVALID_REQUEST", "Method load input must be an object");
          const value = input as Partial<ResolveSelectedContextRequest>;
          if (!Array.isArray(value.methods)) throw new RuntimeError("INVALID_REQUEST", "Method load requires a methods array");
          const invocationId = randomUUID();
          let exactResult: { documents: ResolveSelectedContextResponse["documents"]; dispositions: ResolveSelectedContextResponse["dispositions"] } | undefined;
          const prepare = async (current: RuntimeSessionRecord, activationTurnId = turnId) => {
              const catalog = await this.catalog(projectId);
              let normalized: ReturnType<typeof normalizeMethodSelection>;
              try { normalized = normalizeMethodSelection(catalog, { methods: value.methods! }); }
              catch (error) { throw this.runtimeError(error); }
              const requestedMethods = resolveMethodReferences(catalog, normalized.methods).map((resolution, index) => {
                if (resolution.status !== "resolved") this.throwResolution(resolution, `${normalized.methods[index]?.kind}:${normalized.methods[index]?.name}`);
                return resolution.method.descriptor;
              });
              await this.restrictRequestedTools(projectId, this.roleId(current), current.permissionMode, requestedMethods, activeToolNames);
              const dynamicallyRestricted = requestedMethods.filter(method => method.execution?.tools?.capabilities !== undefined && !method.execution.tools.capabilities.some(capability => capability === "read" || capability === "runtime-methods" || capability === "chirality_load_method"));
              if (dynamicallyRestricted.length) throw new RuntimeError("ENGINE_UNAVAILABLE", `Dynamically loaded method cannot admit the active read callback: ${dynamicallyRestricted.map(method => method.qualifiedId).join(", ")}`, 422, { unavailableOperation: "read", methods: dynamicallyRestricted.map(method => method.qualifiedId) });
              const loadedMethods = requestedMethods.map(method => this.reference(method));
              const unionReferences = [...new Map([...(current.selectedMethods ?? []), ...loadedMethods].map(reference => [formatQualifiedMethodId(reference), reference])).values()];
              const union = await this.resolveInternal(projectId, { ...current, selectedMethods: unionReferences }, { roleId: this.roleId(current), interactionMode: current.interactionMode ?? "chat", permissionMode: current.permissionMode ?? "ask", methods: unionReferences, ...(value.resources === undefined ? {} : { resources: value.resources }) }, catalog);
              const loadedIds = new Set(loadedMethods.map(formatQualifiedMethodId));
              const documents = union.response.documents.filter(document => loadedIds.has(formatQualifiedMethodId(document.method)));
              const dispositions = union.response.dispositions.filter(disposition => loadedIds.has(formatQualifiedMethodId(disposition.method)));
              const loadedEntries: import("./instruction-basis-store.js").ResourceLoadedHistoryRecord[] = union.snapshot.suppliedEntries
                .filter(entry => entry.method !== undefined && loadedIds.has(formatQualifiedMethodId(entry.method)) && (entry.kind === "method-body" || entry.kind === "resource"))
                .map(entry => ({ type: "resource.loaded", resourceKind: entry.kind === "resource" ? "resource" : "method-body", id: entry.id, method: entry.method!, origin: entry.origin, path: entry.path, sha256: entry.sha256, content: entry.content, turnId: activationTurnId, invocationId }));
              exactResult = { documents, dispositions };
              return { methods: loadedMethods, cumulativeMethods: union.response.methods.map(method => this.reference(method)), childInstructionBasisId: union.response.basisPreview.id, instructionPolicySha256: union.activeInstructionPolicySha256, loadedEntries };
          };
          if (executionContext?.nativeChild) {
            const child = executionContext.nativeChild;
            if (child.selectedRole.kind !== "configured" || !CHIRALITY_ROLE_NAMES.includes(child.selectedRole.name as ChiralityRoleName)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native child method loading requires an exact configured Runtime role", 422);
            const selectedRole = child.selectedRole as Extract<typeof child.selectedRole, { kind: "configured" }>;
            const parent = await this.sessions.get(projectId, sessionId);
            if (executionContext.threadId === child.parentThreadId || executionContext.turnId === child.parentTurnId) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native child activation cannot use the parent turn identity", 503);
            const childHistoryId = `native-${sha256(JSON.stringify({ schema: "chirality-native-child-history/v1", parentSessionId: sessionId, supplierGeneration: child.supplierGeneration, rootThreadId: child.rootThreadId, rootTurnId: child.rootTurnId, associationId: child.associationId, childThreadId: executionContext.threadId, childTurnId: executionContext.turnId }))}`;
            await this.withNativeChildActivationLock(childHistoryId, async () => {
              const history = await this.sessions.instructionBases.history(projectId, childHistoryId);
              const prior = [...history].reverse().find(record => record.type === "native-child.method-loaded");
              const scoped = { ...parent, sessionId: childHistoryId, schemaVersion: "chirality.session/v3" as const, roleId: selectedRole.name as ChiralityRoleName, persona: selectedRole.name,
                selectedMethods: prior?.type === "native-child.method-loaded" ? prior.selectedMethods : [], methodSelectionRevision: history.length,
                instructionBasisId: prior?.type === "native-child.method-loaded" ? prior.childInstructionBasisId : undefined };
              const activation = await prepare(scoped, executionContext.turnId);
              await this.sessions.instructionBases.appendHistory(projectId, childHistoryId, {
                type: "native-child.method-loaded", associationId: child.associationId, supplierGeneration: child.supplierGeneration, parentSessionId: sessionId,
                rootThreadId: child.rootThreadId, rootTurnId: child.rootTurnId, parentTurnId: child.parentTurnId,
                childThreadId: executionContext.threadId, childTurnId: executionContext.turnId, roleId: scoped.roleId,
                roleBasisDigest: selectedRole.basisDigest, inheritedToolsDigest: child.inheritedToolsDigest, invocationId,
                selectedMethods: activation.cumulativeMethods, childInstructionBasisId: activation.childInstructionBasisId,
                instructionPolicySha256: activation.instructionPolicySha256, loadedEntries: activation.loadedEntries
              });
            });
          } else {
            await this.sessions.activateLoadedMethods(projectId, sessionId, { turnId, invocationId, methods: [], loadedEntries: [], prepare });
          }
          if (exactResult === undefined) throw new RuntimeError("INTERNAL_FAILURE", "Method activation produced no frozen result", 500);
          return { schemaVersion: "chirality.method-load/v3", turnId: executionContext?.turnId ?? turnId, invocationId, documents: exactResult.documents, dispositions: exactResult.dispositions };
        } },
      { name: "chirality_request_method_change", description: "Request an ordered method merge or replacement at the current turn's terminal boundary.", inputSchema: { type: "object", properties: {
          mode: { type: "string", enum: ["merge", "replace"] },
          methods: { type: "array", items: { type: "object", properties: { kind: { type: "string", enum: ["skill", "workflow"] }, name: { type: "string" }, sourceRootId: { type: "string" }, source: { type: "string", enum: ["project", "user", "bundled"] } }, required: ["kind", "name"], additionalProperties: false } }
        }, required: ["mode", "methods"], additionalProperties: false }, permission: { effect: "allow", operation: "control" },
        execute: async input => {
          if (!input || typeof input !== "object" || Array.isArray(input)) throw new RuntimeError("INVALID_REQUEST", "Method change request must be an object");
          const value = input as { mode?: unknown; methods?: unknown };
          if (value.mode !== "merge" && value.mode !== "replace") throw new RuntimeError("INVALID_REQUEST", "Method change mode must be merge or replace");
          if (!Array.isArray(value.methods) || (value.mode === "merge" && value.methods.length === 0)) throw new RuntimeError("INVALID_REQUEST", "Method change requires a methods array; merge cannot be empty");
          const catalog = await this.catalog(projectId);
          const resolutions = resolveMethodReferences(catalog, value.methods as MethodReference[]);
          const methods: QualifiedMethodReference[] = [];
          for (const resolution of resolutions) {
            if (resolution.status !== "resolved") this.throwResolution(resolution, `${resolution.requested.kind}:${resolution.requested.name}`);
            methods.push(this.reference(resolution.method.descriptor));
          }
          const session = await this.sessions.get(projectId, sessionId);
          const invocationId = randomUUID();
          const requested = await this.sessions.requestMethodChange(projectId, sessionId, { turnId, invocationId, mode: value.mode, methods, expectedRevision: session.methodSelectionRevision ?? 0, ...(session.instructionBasisId === undefined ? {} : { expectedBasisId: session.instructionBasisId }) });
          return { schemaVersion: "chirality.method-change-request/v3", status: "deferred", requestId: requested.historyId, turnId, invocationId, mode: value.mode, methods };
        } }
    ];
  }

  async restrictRequestedTools(projectId: string, roleId: ChiralityRoleName, permissionMode: RuntimeSessionRecord["permissionMode"], methods: ResolveSelectedContextResponse["methods"], requested: readonly string[]): Promise<string[]> {
    const mode = permissionMode ?? "ask";
    let allowed = [...requested];
    if (mode === "readOnly") allowed = allowed.filter(name => READ_TOOL.test(name));
    const restrictions = methods.map(method => method.execution?.tools?.capabilities).filter((value): value is readonly string[] => value !== undefined);
    const roleTools = (await this.listRoles(projectId)).roles.find(role => role.id === roleId)?.tools ?? [];
    allowed = allowed.filter(tool => roleTools.includes(tool) || roleTools.includes(this.semanticToolCapability(tool)) || roleTools.includes("all"));
    for (const capabilitySet of restrictions) allowed = allowed.filter(tool => capabilitySet.includes(tool) || capabilitySet.includes(this.semanticToolCapability(tool)));
    if (methods.some(method => method.execution?.tools?.commands !== undefined)) allowed = allowed.filter(tool => this.semanticToolCapability(tool) !== "bash");
    const denied = requested.filter(tool => !allowed.includes(tool));
    if (denied.length) throw new RuntimeError("ENGINE_UNAVAILABLE", `Requested tools are unavailable under the selected permission mode and methods: ${denied.join(", ")}`, 422, { unavailableTools: denied, permissionMode: mode });
    return allowed;
  }

  async restrictRuntimeTools(projectId: string, roleId: ChiralityRoleName, permissionMode: RuntimeSessionRecord["permissionMode"], methods: ResolveSelectedContextResponse["methods"], definitions: readonly RuntimeToolDefinition[]): Promise<readonly RuntimeToolDefinition[]> {
    const allowedOperations = permissionMode === "readOnly" ? new Set(["read"]) : permissionMode === "ask" || permissionMode === "workspaceWrite" || permissionMode === "bypass" ? new Set(["read", "write", "shell", "network"]) : new Set<string>();
    const declared = methods.map(method => method.execution?.tools?.capabilities).filter((value): value is readonly string[] => value !== undefined);
    const roleTools = (await this.listRoles(projectId)).roles.find(role => role.id === roleId)?.tools ?? [];
    return definitions.filter(definition => {
      if (definition.permission.effect !== "allow") return false;
      if (definition.name === "chirality_request_method_change" && definition.permission.operation === "control") return true;
      return allowedOperations.has(definition.permission.operation) && (roleTools.includes(definition.name) || roleTools.includes(definition.permission.operation) || roleTools.includes("runtime-methods") || roleTools.includes("all")) && declared.every(capabilities => capabilities.includes(definition.name) || capabilities.includes(definition.permission.operation));
    });
  }

  private async resolveInternal(projectId: string, session: RuntimeSessionRecord, request: ResolveSelectedContextRequest, catalogOverride?: MethodCatalog): Promise<ResolvedInternal> {
    const roots = await this.projects.roots(projectId);
    const rootBinding = async <T extends "registered-project-root" | "trusted-runtime-instruction-root">(path: string, origin: T) => {
      const metadata = await lstat(path, { bigint: true });
      if (!metadata.isDirectory() || metadata.isSymbolicLink() || await realpath(path) !== path) throw new RuntimeError("ENGINE_UNAVAILABLE", `Execution root is no longer a canonical directory: ${origin}`, 503);
      return Object.freeze({ path, origin, identitySha256: sha256(JSON.stringify({ schema: "chirality.execution-root/v1", path, origin, dev: `${metadata.dev}`, ino: `${metadata.ino}` })) });
    };
    const executionRoots = Object.freeze({
      workingRoot: await rootBinding(roots.workingRoot, "registered-project-root"),
      toolRoot: await rootBinding(roots.instructionRoot, "trusted-runtime-instruction-root")
    });
    const catalog = catalogOverride ?? await this.catalog(projectId);
    let normalized: ReturnType<typeof normalizeMethodSelection>;
    try { normalized = normalizeMethodSelection(catalog, request); }
    catch (error) { throw this.runtimeError(error); }
    const resolutions = resolveMethodReferences(catalog, normalized.methods);
    const selected: CatalogMethodEntry[] = [];
    for (const resolution of resolutions) {
      if (resolution.status !== "resolved") this.throwResolution(resolution, `${resolution.requested.kind}:${resolution.requested.name}`);
      selected.push(resolution.method);
    }
    const resources = new Map((request.resources ?? []).map(value => [formatQualifiedMethodId(value.method), value.paths]));
    const supplied: SuppliedContextEntry[] = [];
    const frozen: FrozenInstructionEntry[] = [];
    const add = (kind: SuppliedContextEntry["kind"], id: string, origin: string, path: string, content: string, method?: QualifiedMethodReference, resourcePath?: string): void => {
      const digest = sha256(content);
      supplied.push({ kind, id, content, sha256: digest, ...(method ? { method } : {}), ...(resourcePath ? { resourcePath } : {}) });
      frozen.push({ kind, id, origin, path, content, sha256: digest, ...(method ? { method } : {}), ...(resourcePath ? { resourcePath } : {}) });
    };
    const productPath = this.productInstructions.productInstructionsPath ?? join(roots.instructionRoot, "AGENTS.md");
    await this.addFile(add, "root", "root:AGENTS", dirname(productPath), productPath);
    if (!this.productInstructions.nativeProjectDiscovery && roots.workingRoot !== roots.instructionRoot) await this.addFile(add, "project", "project:AGENTS", roots.workingRoot, join(roots.workingRoot, "AGENTS.md"), true);
    const role = (await this.listRoles(projectId)).roles.find(value => value.id === request.roleId)!;
    if (this.productInstructions.nativeProjectDiscovery) {
      for (const nativeRole of (await this.listRoles(projectId)).roles) {
        const path = join(roots.instructionRoot, nativeRole.instruction);
        await this.addFile((kind, id, origin, file, content) => {
          add(kind, id, origin, file, content);
          if (nativeRole.id === role.id) add("role", `role:${role.id}`, origin, file, content);
        }, "resource", `native-role:${nativeRole.id}`, roots.instructionRoot, path);
      }
      add("resource", "product:library", roots.instructionRoot, roots.instructionRoot,
        `Bundled skills: ${join(roots.instructionRoot, ".agents", "skills")}\nBundled workflows: ${join(roots.instructionRoot, "workflows")}\nRole library: ${join(roots.instructionRoot, "agents")}\nUse named native roles with a bounded brief and fresh context (fork_context=false); full-history forks do not isolate the role in Codex 0.154.0.`);
    } else {
      await this.addFile(add, "role", `role:${role.id}`, roots.instructionRoot, join(roots.instructionRoot, role.instruction));
    }
    for (const entry of catalog.entries.filter(value => value.descriptor.kind === "skill")) {
      const reference = this.reference(entry.descriptor);
      add("catalog-description", `method-description:${entry.descriptor.qualifiedId}`, entry.sourceRootPath, entry.entrypointPath, entry.descriptor.description, reference);
    }
    const documents: ResolveSelectedContextResponse["documents"][number][] = [];
    const dispositions: SelectedMethodDisposition[] = [];
    for (const entry of selected) {
      const reference = this.reference(entry.descriptor);
      const inspection = await this.mapError(() => inspectCatalogMethod(entry));
      const activeRoleCompatible = entry.descriptor.executionRoleIds.includes(request.roleId);
      const managed = entry.descriptor.executionRoleIds.some(eligible => role.delegatesTo?.includes(eligible));
      const route = activeRoleCompatible ? "primary" : managed ? "managed-delegation" : "unavailable";
      dispositions.push({ method: reference, selected: true, activeRoleCompatible, eligibleRoleIds: entry.descriptor.executionRoleIds, route });
      if (route === "primary") {
        add("method-body", `method:${entry.descriptor.qualifiedId}`, entry.sourceRootPath, entry.entrypointPath, inspection.entrypoint.content, reference);
        documents.push({ method: reference, path: entry.descriptor.kind === "skill" ? "SKILL.md" : "WORKFLOW.md", content: inspection.entrypoint.content, sha256: inspection.entrypoint.sha256 });
        for (const path of resources.get(entry.descriptor.qualifiedId) ?? []) {
          const loaded = await this.mapError(() => readMethodResource(entry, path));
          add("resource", `resource:${entry.descriptor.qualifiedId}:${path}`, entry.sourceRootPath, join(entry.packageRoot, path), loaded.content, reference, path);
          documents.push({ method: reference, path, content: loaded.content, sha256: loaded.sha256 });
        }
      }
    }
    const sources = [...new Map(selected.map(entry => [entry.descriptor.sourceRootId, { sourceRootId: entry.descriptor.sourceRootId, source: entry.descriptor.source, version: entry.sourceRootVersion, rootSha256: sha256(JSON.stringify(catalog.entries.filter(value => value.descriptor.sourceRootId === entry.descriptor.sourceRootId).map(value => value.descriptor))) }])).values()];
    const effectivePolicy = {
      role: { id: role.id, tools: role.tools ?? [], delegatesTo: role.delegatesTo ?? [] },
      methods: selected.map(value => ({ qualifiedId: value.descriptor.qualifiedId, executionRoleIds: value.descriptor.executionRoleIds, execution: value.descriptor.execution ?? null })),
      brief: {
        allowedWriteTargets: { present: session.allowedWriteTargets !== undefined, value: session.allowedWriteTargets ?? null },
        declaredContext: { present: (session as RuntimeSessionRecord & { declaredContext?: readonly string[] }).declaredContext !== undefined, value: (session as RuntimeSessionRecord & { declaredContext?: readonly string[] }).declaredContext ?? null }
      }
    };
    add("selection-metadata", "selection:dispositions", "runtime", "selection/dispositions.json", JSON.stringify({ selectedMethods: selected.map(value => this.reference(value.descriptor)), dispositions, compatibilityInputs: normalized.compatibilityInputs, compatibilityMappings: normalized.compatibilityMappings, effectivePolicy, sources, executionRoots }));
    const instructionPolicyMaterial = { roleId: request.roleId, methods: selected.map(value => value.descriptor.qualifiedId), dispositions, effectivePolicy, sources, executionRoots };
    const instructionPolicySha256 = sha256(JSON.stringify({ ...instructionPolicyMaterial, supplied: supplied.map(value => ({ kind: value.kind, id: value.id, sha256: value.sha256 })) }));
    const activeInstructionPolicySha256 = sha256(JSON.stringify({ ...instructionPolicyMaterial, supplied: supplied.filter(value => value.kind !== "resource").map(value => ({ kind: value.kind, id: value.id, sha256: value.sha256 })) }));
    const basisMaterial = JSON.stringify({ instructionPolicySha256, interactionMode: request.interactionMode, permissionMode: request.permissionMode, compatibilityInputs: normalized.compatibilityInputs, compatibilityMappings: normalized.compatibilityMappings });
    const basisSha = sha256(basisMaterial);
    const basisId = `basis-${basisSha}`;
    const response: ResolveSelectedContextResponse = { schemaVersion: "chirality.selected-context/v3", roleId: request.roleId, methods: selected.map(value => value.descriptor), documents, dispositions, supplied, executionRoots, basisPreview: { id: basisId, sha256: basisSha, instructionPolicySha256, sources, persisted: false }, compatibilityInputs: normalized.compatibilityInputs, compatibilityMappings: normalized.compatibilityMappings };
    return { response, activeInstructionPolicySha256, snapshot: { schemaVersion: "chirality.instruction-basis/v1", basisId, sessionId: session.sessionId, createdAt: session.createdAt, roleId: request.roleId, interactionMode: request.interactionMode, permissionMode: request.permissionMode, selectedMethods: selected.map(value => this.reference(value.descriptor)), instructionPolicySha256, compatibilityInputs: normalized.compatibilityInputs, compatibilityMappings: normalized.compatibilityMappings, suppliedEntries: frozen, methodDispositions: dispositions } };
  }

  private async catalog(projectId: string): Promise<MethodCatalog> {
    const roots = await this.projects.roots(projectId);
    const project = await this.projects.requireAuthorized(projectId);
    const userRoot = homedir();
    const sourceRoots: MethodSourceRoot[] = [
      { sourceRootId: `project-${sha256(roots.workingRoot).slice(0, 24)}`, source: "project", rootPath: roots.workingRoot, version: project.manifestHash, skillDirectory: ".agents/skills", workflowDirectory: ".chirality/workflows" },
      { sourceRootId: `user-${sha256(userRoot).slice(0, 24)}`, source: "user", rootPath: userRoot, version: sha256(userRoot), skillDirectory: ".agents/skills", workflowDirectory: ".chirality/workflows" },
      { sourceRootId: "chirality-root", source: "bundled", rootPath: roots.instructionRoot, version: await this.rootVersion(roots.instructionRoot), skillDirectory: ".agents/skills", workflowDirectory: "workflows" }
    ];
    return discoverMethodCatalog(sourceRoots);
  }

  private async persistedNativePlanRevisions(projectId: string, sessionId: string): Promise<readonly NativePlanRevision[]> {
    const revisions = (await this.sessions.instructionBases.history(projectId, sessionId)).filter(record => record.type === "native-plan.revised").map(record => record.revision);
    let priorRevision = 0;
    const eventIds = new Set<string>();
    for (const revision of revisions) {
      if (revision.revision <= priorRevision || eventIds.has(revision.sourceEvent.eventId)) throw new RuntimeError("INTERNAL_FAILURE", "Persisted Native Plan revision history conflicts or is unordered", 500);
      priorRevision = revision.revision;
      eventIds.add(revision.sourceEvent.eventId);
    }
    return revisions;
  }

  private roleId(session: RuntimeSessionRecord): ChiralityRoleName {
    return session.roleId ?? (session.role === "agent0" ? "HELP_HUMAN" : session.role === "agent2" ? "TASK" : "WORKING_ITEMS");
  }
  private semanticToolCapability(tool: string): string { if (/^(?:read|read_file|search|find|list|inspect)/u.test(tool)) return "read"; if (/^(?:bash|shell|exec)/u.test(tool)) return "bash"; if (/^(?:write|edit|apply)/u.test(tool)) return "write"; return tool; }
  private contained(root: string, candidate: string): boolean { const value = relative(root, candidate); return value === "" || (value !== ".." && !value.startsWith(`..${sep}`) && !isAbsolute(value)); }
  private async rootVersion(root: string): Promise<string> { const values = await Promise.all(["AGENTS.md", "agents/registry.json", "workflows/index.json"].map(path => readFile(join(root, path)).catch(() => Buffer.alloc(0)))); return sha256(Buffer.concat(values)); }
  private reference(value: QualifiedMethodReference): QualifiedMethodReference { return { sourceRootId: value.sourceRootId, source: value.source, kind: value.kind, name: value.name }; }
  private stringField(input: unknown, field: string): string { const value = input && typeof input === "object" && !Array.isArray(input) ? (input as Record<string, unknown>)[field] : undefined; if (typeof value !== "string" || value.trim() === "") throw new RuntimeError("INVALID_REQUEST", `${field} must be a non-empty string`); return value; }
  private async addFile(add: (kind: SuppliedContextEntry["kind"], id: string, origin: string, path: string, content: string) => void, kind: SuppliedContextEntry["kind"], id: string, origin: string, path: string, optional = false): Promise<void> {
    let canonicalOrigin: string;
    let canonicalPath: string;
    try {
      [canonicalOrigin, canonicalPath] = await Promise.all([realpath(origin), realpath(path)]);
    } catch (error) {
      if (optional && (error as NodeJS.ErrnoException).code === "ENOENT") return;
      throw error;
    }
    if (!this.contained(canonicalOrigin, canonicalPath)) throw new RuntimeError("FORBIDDEN", `Instruction context escapes its declared origin: ${id}`, 403);
    add(kind, id, canonicalOrigin, canonicalPath, await readFile(canonicalPath, "utf8"));
  }
  private throwResolution(resolution: ReturnType<typeof resolveMethodReferences>[number] | undefined, label: string): never { if (resolution?.status === "forbidden") throw new RuntimeError("FORBIDDEN", `Skill origin is not trusted for loading: ${label}`, 403, { method: resolution.method }); if (resolution?.status === "malformed") throw new RuntimeError("INVALID_REQUEST", `Malformed method shadow blocks resolution: ${label}`, 422, { issues: resolution.issues }); if (resolution?.status === "ambiguous") throw new RuntimeError("INVALID_REQUEST", `Method reference is ambiguous: ${label}`, 409, { candidates: resolution.candidates }); throw new RuntimeError("NOT_FOUND", `Unknown method: ${label}`, 404); }
  private runtimeError(error: unknown): RuntimeError {
    if (error instanceof MethodCatalogError) {
      return error.code === "UNSUPPORTED_METHOD_ORIGIN"
        ? new RuntimeError("FORBIDDEN", error.message, 403, { methodCode: error.code })
        : new RuntimeError("INVALID_REQUEST", error.message, 400, { methodCode: error.code });
    }
    return error instanceof RuntimeError ? error : new RuntimeError("INTERNAL_FAILURE", (error as Error).message, 500);
  }
  private async mapError<T>(operation: () => Promise<T>): Promise<T> { try { return await operation(); } catch (error) { throw this.runtimeError(error); } }
}
