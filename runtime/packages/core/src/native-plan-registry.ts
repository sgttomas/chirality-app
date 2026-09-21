import {
  assertAdmittedNativePlanEvent,
  RuntimeError,
  type NativePlanAdapterQualification,
  type NativePlanAdapterAdmission,
  type NativePlanCapabilityResponse,
  type NativePlanClarification,
  type NativePlanClarificationPrompt,
  type NativePlanClarificationsResponse,
  type NativePlanRevision,
  type NativePlanRevisionsResponse,
  type NativePlanTransportEvent,
  type ReplyNativePlanClarificationRequest,
  type RuntimeSessionRecord,
  type SupervisorNativePlanPort
} from "@chirality/runtime-contracts";
import type { DelegatedNativePlanSink, DelegatedNativePlanWorkerBinding } from "./delegated-runtime.js";
import type { TrustedNativePlanAdapterRegistry } from "./runtime-method-service.js";
import type { SessionStore } from "./session-store.js";

interface ActiveNativePlanTurn {
  binding: DelegatedNativePlanWorkerBinding;
  bridge: SupervisorNativePlanPort;
  clarifications: readonly NativePlanClarificationPrompt[];
  providerIdentity?: { threadId: string; turnId: string };
}

export interface TrustedNativePlanRegistryOptions {
  projectId: string;
  sessions: SessionStore;
  qualification?: NativePlanAdapterQualification;
  admission?: NativePlanAdapterAdmission;
  unavailableReason?: string;
}

/**
 * Production registry for the admitted supervisor composition. The registry
 * never accepts provider events from a public client and persists completed
 * plan items before the worker generation is retired.
 */
export class TrustedNativePlanRegistry implements TrustedNativePlanAdapterRegistry, DelegatedNativePlanSink {
  private readonly active = new Map<string, ActiveNativePlanTurn>();
  private readonly captures = new Map<string, Promise<void>>();
  private readonly admission?: Readonly<NativePlanAdapterAdmission>;

  constructor(private readonly options: TrustedNativePlanRegistryOptions) {
    if (options.qualification !== undefined && options.admission !== undefined) throw new Error("Native Plan adapter admission is ambiguous");
    const q = options.admission ?? options.qualification;
    if (q !== undefined && (q.adapterId.trim() === "" || q.providerId.trim() === "" || !/^[a-f0-9]{64}$/u.test(q.admissionSha256)
      || (q.evidenceClass === "native-adapter-qualified" ? q.qualificationId.trim() === "" : q.evidenceClass !== "native-adapter-local-human-trial" || q.dispositionId.trim() === ""))) throw new Error("Invalid native Plan adapter admission");
    this.admission = q === undefined ? undefined : Object.freeze(structuredClone(q));
  }

  async capability(session: RuntimeSessionRecord): Promise<NativePlanCapabilityResponse> {
    if (this.admission === undefined) return this.unavailable(this.options.unavailableReason ?? "Native Plan adapter admission is unavailable");
    if (session.projectId !== this.options.projectId) return this.unavailable("Native Plan adapter is not bound to this project");
    if (session.engineSelection.adapterId !== this.admission.adapterId || session.engineSelection.providerId !== this.admission.providerId) return this.unavailable("The selected engine is not the admitted native Plan adapter");
    return this.admission.evidenceClass === "native-adapter-qualified"
      ? { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification: { ...this.admission } }
      : { schemaVersion: "chirality.native-plan-capability/v3", status: "trial", admission: { ...this.admission } };
  }

  async revisions(projectId: string, sessionId: string): Promise<NativePlanRevisionsResponse> {
    this.project(projectId);
    await this.options.sessions.get(projectId, sessionId);
    const revisions = await this.persisted(projectId, sessionId);
    if (this.admission === undefined) return { schemaVersion: "chirality.native-plan-revisions/v3", status: "unavailable", reason: this.options.unavailableReason ?? "Native Plan adapter admission is unavailable", revisions: [] };
    return this.admission.evidenceClass === "native-adapter-qualified"
      ? { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification: { ...this.admission }, revisions }
      : { schemaVersion: "chirality.native-plan-revisions/v3", status: "trial", admission: { ...this.admission }, revisions };
  }

  async clarifications(projectId: string, sessionId: string): Promise<NativePlanClarificationsResponse> {
    this.project(projectId);
    await this.options.sessions.get(projectId, sessionId);
    if (this.admission === undefined) return { schemaVersion: "chirality.native-plan-clarifications/v3", status: "unavailable", reason: this.options.unavailableReason ?? "Native Plan adapter admission is unavailable", clarifications: [] };
    const entry = this.active.get(sessionId);
    const clarifications = entry === undefined ? [] : entry.clarifications.map(prompt => this.publicClarification(prompt));
    return this.admission.evidenceClass === "native-adapter-qualified"
      ? { schemaVersion: "chirality.native-plan-clarifications/v3", status: "qualified", qualification: { ...this.admission }, clarifications }
      : { schemaVersion: "chirality.native-plan-clarifications/v3", status: "trial", admission: { ...this.admission }, clarifications };
  }

  async replyClarification(projectId: string, sessionId: string, request: ReplyNativePlanClarificationRequest): Promise<{ sent: true }> {
    this.project(projectId);
    if (this.admission === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", this.options.unavailableReason ?? "Native Plan adapter admission is unavailable", 503);
    const entry = this.active.get(sessionId);
    if (entry === undefined) throw new RuntimeError("NOT_FOUND", "No live native Plan clarification exists for this session", 404);
    const prompt = entry.clarifications.find(value => value.requestId === request.requestId);
    if (prompt === undefined) throw new RuntimeError("NOT_FOUND", "Unknown native Plan clarification request", 404);
    const sent = await entry.bridge.replyNativePlanClarification(entry.binding.workerId, entry.binding.generation, request.requestId, request.answers);
    if (sent.sent === true && this.active.get(sessionId) === entry) entry.clarifications = entry.clarifications.filter(value => value.requestId !== request.requestId);
    return sent;
  }

  async open(binding: DelegatedNativePlanWorkerBinding, bridge: SupervisorNativePlanPort): Promise<void> {
    this.binding(binding);
    const session = await this.options.sessions.get(binding.projectId, binding.sessionId);
    const capability = await this.capability(session);
    if (capability.status === "unavailable") throw new RuntimeError("ENGINE_UNAVAILABLE", capability.reason, 503);
    if (session.status !== "running") throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Native Plan worker requires the Runtime session's active accepted turn", 409);
    const replay = await this.options.sessions.replayDetailed(binding.projectId, binding.sessionId);
    const accepted = [...replay.events].reverse().find(event => event.type === "turn.accepted");
    const terminal = replay.events.some(event => event.turnId === binding.clientTurnId && (event.type === "turn.completed" || event.type === "turn.failed" || event.type === "turn.interrupted"));
    if (accepted?.turnId !== binding.clientTurnId || terminal) throw new RuntimeError("RUNTIME_COMPATIBILITY_MISMATCH", "Native Plan worker does not match the current nonterminal accepted turn", 409);
    if (this.admission === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", this.options.unavailableReason ?? "Native Plan adapter admission is unavailable", 503);
    if (this.active.has(binding.sessionId)) throw new RuntimeError("SESSION_TURN_IN_PROGRESS", "Native Plan session already has a live worker", 409);
    this.active.set(binding.sessionId, { binding: structuredClone(binding), bridge, clarifications: [] });
  }

  async capture(binding: DelegatedNativePlanWorkerBinding, events: readonly NativePlanTransportEvent[], clarifications: readonly NativePlanClarificationPrompt[]): Promise<void> {
    this.binding(binding);
    const entry = this.active.get(binding.sessionId);
    if (entry === undefined || !this.sameBinding(entry.binding, binding)) throw new RuntimeError("FORBIDDEN", "Native Plan capture does not match the live worker generation", 403);
    const identities = [...events.map(event => ({ threadId: event.providerThreadId, turnId: event.providerTurnId })), ...clarifications.map(prompt => ({ threadId: prompt.providerThreadId, turnId: prompt.providerTurnId }))];
    if (identities.some(identity => !identity.threadId || !identity.turnId) || new Set(identities.map(identity => `${identity.threadId}\0${identity.turnId}`)).size > 1) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan capture mixed provider thread or turn identities", 503);
    if (identities[0] !== undefined) {
      if (entry.providerIdentity !== undefined && (entry.providerIdentity.threadId !== identities[0].threadId || entry.providerIdentity.turnId !== identities[0].turnId)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan provider identity changed during the admitted turn", 503);
      entry.providerIdentity ??= { ...identities[0] };
    }
    this.validateClarifications(binding, clarifications);
    entry.clarifications = structuredClone(clarifications);
    const prior = this.captures.get(binding.sessionId) ?? Promise.resolve();
    const capture = prior.then(() => this.persistEvents(binding, events));
    this.captures.set(binding.sessionId, capture);
    try { await capture; } finally { if (this.captures.get(binding.sessionId) === capture) this.captures.delete(binding.sessionId); }
  }

  async close(binding: DelegatedNativePlanWorkerBinding): Promise<void> {
    this.binding(binding);
    const entry = this.active.get(binding.sessionId);
    if (entry !== undefined && this.sameBinding(entry.binding, binding)) this.active.delete(binding.sessionId);
    await this.captures.get(binding.sessionId);
  }

  private async persistEvents(binding: DelegatedNativePlanWorkerBinding, events: readonly NativePlanTransportEvent[]): Promise<void> {
    const admission = this.admission;
    if (admission === undefined) throw new RuntimeError("ENGINE_UNAVAILABLE", this.options.unavailableReason ?? "Native Plan adapter admission is unavailable", 503);
    let revisions = await this.persisted(binding.projectId, binding.sessionId);
    for (const event of events) {
      if (event.projectId !== binding.projectId || event.sessionId !== binding.sessionId || event.clientTurnId !== binding.clientTurnId || !event.providerThreadId || !event.providerTurnId || !event.eventId || !Number.isFinite(Date.parse(event.occurredAt))) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan event identity does not match the admitted worker", 503);
      const existing = revisions.find(value => value.sourceEvent.eventId === event.eventId);
      const common = { eventId: event.eventId, occurredAt: event.occurredAt, binding: { projectId: event.projectId, sessionId: event.sessionId, clientTurnId: event.clientTurnId, providerThreadId: event.providerThreadId, providerTurnId: event.providerTurnId }, plan: structuredClone(event.plan) };
      const sourceEvent = admission.evidenceClass === "native-adapter-qualified"
        ? { qualificationState: "qualified" as const, qualification: { ...admission }, ...common }
        : { qualificationState: "trial" as const, admission: { ...admission }, ...common };
      assertAdmittedNativePlanEvent(sourceEvent);
      if (existing !== undefined) {
        if (JSON.stringify(existing.sourceEvent) !== JSON.stringify(sourceEvent)) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan event identity was reused with different content", 503);
        continue;
      }
      const revision: NativePlanRevision = { revision: (revisions.at(-1)?.revision ?? 0) + 1, sourceEvent };
      await this.options.sessions.instructionBases.appendTrustedNativePlanRevision(binding.projectId, binding.sessionId, revision);
      revisions = [...revisions, revision];
    }
  }

  private async persisted(projectId: string, sessionId: string): Promise<readonly NativePlanRevision[]> {
    const history = await this.options.sessions.instructionBases.history(projectId, sessionId);
    return history.filter(record => record.type === "native-plan.revised").map(record => record.revision);
  }

  private validateClarifications(binding: DelegatedNativePlanWorkerBinding, prompts: readonly NativePlanClarificationPrompt[]): void {
    if (!Array.isArray(prompts) || prompts.length > 64) throw new RuntimeError("ENGINE_UNAVAILABLE", "Invalid native Plan clarification inventory", 503);
    const ids = new Set<string>();
    for (const prompt of prompts) {
      const id = `${typeof prompt.requestId}:${String(prompt.requestId)}`;
      if (ids.has(id) || prompt.projectId !== binding.projectId || prompt.sessionId !== binding.sessionId || prompt.clientTurnId !== binding.clientTurnId || !prompt.providerThreadId || !prompt.providerTurnId || !prompt.itemId || !Array.isArray(prompt.questions) || prompt.questions.length === 0) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan clarification identity does not match the admitted worker", 503);
      ids.add(id);
    }
  }

  private publicClarification(prompt: NativePlanClarificationPrompt): NativePlanClarification {
    return { clientTurnId: prompt.clientTurnId, providerThreadId: prompt.providerThreadId, providerTurnId: prompt.providerTurnId, requestId: prompt.requestId, itemId: prompt.itemId, questions: structuredClone(prompt.questions), isBlocking: prompt.isBlocking, autoResolutionMs: prompt.autoResolutionMs };
  }

  private project(projectId: string): void {
    if (projectId !== this.options.projectId) throw new RuntimeError("FORBIDDEN", "Native Plan registry is not bound to this project", 403);
  }

  private binding(binding: DelegatedNativePlanWorkerBinding): void {
    this.project(binding.projectId);
    for (const value of [binding.sessionId, binding.clientTurnId, binding.workerId, binding.generation]) if (!value) throw new RuntimeError("ENGINE_UNAVAILABLE", "Native Plan worker binding is incomplete", 503);
  }

  private sameBinding(left: DelegatedNativePlanWorkerBinding, right: DelegatedNativePlanWorkerBinding): boolean {
    return left.projectId === right.projectId && left.sessionId === right.sessionId && left.clientTurnId === right.clientTurnId && left.workerId === right.workerId && left.generation === right.generation;
  }

  private unavailable(reason: string): NativePlanCapabilityResponse {
    return { schemaVersion: "chirality.native-plan-capability/v3", status: "unavailable", reason };
  }
}
