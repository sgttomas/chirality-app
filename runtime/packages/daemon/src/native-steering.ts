import {
  RuntimeError, validateSessionSteerRequest, validateSessionSteerReceiptRequest,
  type HarnessEvent, type SessionSteerReceiptRequest, type SessionSteerRequest, type SessionSteerResponse, type SessionTurnState
} from "@chirality/runtime-contracts";

export interface SteeringJournal {
  replay(projectId: string, sessionId: string): Promise<readonly HarnessEvent[]>;
  appendEvent(projectId: string, input: Omit<HarnessEvent, "schemaVersion" | "eventId" | "timestamp">): Promise<HarnessEvent>;
}
export interface NativeSteeringOptions {
  journal: SteeringJournal;
  state(projectId: string, sessionId: string): SessionTurnState;
  publish(projectId: string, sessionId: string, event: HarnessEvent): void;
  dispatch(projectId: string, sessionId: string, request: SessionSteerRequest): Promise<SessionSteerResponse>;
}
const record = (value: unknown): Record<string, unknown> => value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};

/** Session evidence is the deduplication boundary, including after restart.
 * An intent without an outcome is uncertain and is never automatically sent again.
 */
export class NativeSteering {
  private readonly pending = new Map<string, { request: SessionSteerRequest; result: Promise<SessionSteerResponse> }>();
  constructor(private readonly options: NativeSteeringOptions) {}

  steer(projectId: string, sessionId: string, input: SessionSteerRequest): Promise<SessionSteerResponse> {
    const request = validateSessionSteerRequest(input);
    const key = JSON.stringify([projectId, sessionId, request.operationId]);
    const existing = this.pending.get(key);
    if (existing) {
      this.sameRequest(existing.request, request);
      return existing.result;
    }
    const result = this.execute(projectId, sessionId, request);
    this.pending.set(key, { request, result });
    void result.finally(() => { if (this.pending.get(key)?.result === result) this.pending.delete(key); }).catch(() => undefined);
    return result;
  }

  /** Reconcile durable evidence only, including when no turn is active. Missing
   * intent is unknown: this path never creates an intent or reaches dispatch.
   */
  async receipt(projectId: string, sessionId: string, input: SessionSteerReceiptRequest): Promise<SessionSteerResponse> {
    const request = validateSessionSteerReceiptRequest(input);
    const active = this.pending.get(JSON.stringify([projectId, sessionId, request.operationId]));
    if (active) {
      if (active.request.expectedTurnId !== request.expectedTurnId) throw new RuntimeError("INVALID_REQUEST", "Steering receipt does not match the pending turn", 409);
      // Let the original outcome persist first so a late unknown response cannot
      // overwrite a receipt confirmation emitted by this same service instance.
      await active.result.catch(() => undefined);
    }

    const events = await this.options.journal.replay(projectId, sessionId);
    const prior = events.filter(event => event.type === "codex.steer" && event.data.operationId === request.operationId);
    if (!prior.length) return { operationId: request.operationId, turnId: request.expectedTurnId, status: "unknown", message: "No delivery record is available. Input was not sent by this receipt check." };
    const first = prior[0]!;
    if (first.data.expectedTurnId !== request.expectedTurnId || typeof first.data.text !== "string") {
      throw new RuntimeError("INVALID_REQUEST", "Steering receipt does not match the recorded turn", 409);
    }
    const original = { ...request, text: first.data.text };
    for (const event of prior) this.sameRequest(event.data, original);
    return this.reconcile(projectId, sessionId, events, prior.at(-1)!, original);
  }

  private async reconcile(projectId: string, sessionId: string, events: readonly HarnessEvent[], last: HarnessEvent, request: SessionSteerRequest): Promise<SessionSteerResponse> {
    // Explicit rejection is terminal receipt evidence, not an invitation to retry.
    const nativeId = last.data.status === "rejected" ? undefined : this.confirmation(events, request, typeof last.data.providerTurnId === "string" ? last.data.providerTurnId : undefined);
    const status = nativeId ? "accepted" : last.data.status === "accepted" || last.data.status === "rejected" ? last.data.status : "unknown";
    const result: SessionSteerResponse = { operationId: request.operationId, turnId: request.expectedTurnId, status,
      ...(typeof last.data.message === "string" ? { message: last.data.message } : {}),
      ...(nativeId ? { providerTurnId: nativeId } : typeof last.data.providerTurnId === "string" ? { providerTurnId: last.data.providerTurnId } : {}) };
    if (nativeId && last.data.status !== "accepted") {
      result.message = "Codex input receipt was confirmed from the conversation.";
      await this.evidence(projectId, sessionId, request, "accepted", result);
    } else if (status === "unknown") result.message = "Input delivery remains unconfirmed. It was not resent.";
    return result;
  }

  private sameRequest(prior: { expectedTurnId?: unknown; text?: unknown }, request: SessionSteerRequest): void {
    if (prior.expectedTurnId !== request.expectedTurnId || prior.text !== request.text) throw new RuntimeError("INVALID_REQUEST", "Steering operationId was already used for different input", 409);
  }

  private async evidence(projectId: string, sessionId: string, request: SessionSteerRequest, status: "submitted" | SessionSteerResponse["status"], response?: SessionSteerResponse): Promise<void> {
    const event = await this.options.journal.appendEvent(projectId, {
      sessionId, turnId: request.expectedTurnId, type: "codex.steer",
      data: { ...request, status, ...(response?.message === undefined ? {} : { message: response.message }), ...(response?.providerTurnId === undefined ? {} : { providerTurnId: response.providerTurnId }) }
    });
    this.options.publish(projectId, sessionId, event);
  }

  private confirmation(events: readonly HarnessEvent[], request: SessionSteerRequest, expectedProviderTurnId?: string): string | undefined {
    for (const event of events) {
      if (event.type !== "codex.notification" || event.turnId !== request.expectedTurnId) continue;
      const params = record(event.data.params);
      if (expectedProviderTurnId !== undefined && params.turnId !== expectedProviderTurnId) continue;
      const item = record(params.item);
      const codex = record(event.data.codex);
      if (codex.isPrimaryThread !== true || !["item/started", "item/completed"].includes(String(event.data.method)) || item.type !== "userMessage" || item.clientId !== request.operationId) continue;
      const content = Array.isArray(item.content) ? item.content : [];
      if (content.length !== 1 || record(content[0]).type !== "text" || record(content[0]).text !== request.text) continue;
      if (typeof params.turnId === "string" && params.turnId) return params.turnId;
    }
    return undefined;
  }

  private async execute(projectId: string, sessionId: string, request: SessionSteerRequest): Promise<SessionSteerResponse> {
    const base = { operationId: request.operationId, turnId: request.expectedTurnId };
    const events = await this.options.journal.replay(projectId, sessionId);
    const prior = events.filter(event => event.type === "codex.steer" && event.data.operationId === request.operationId);
    if (prior.length) {
      for (const event of prior) this.sameRequest(event.data, request);
      return this.reconcile(projectId, sessionId, events, prior.at(-1)!, request);
    }
    // Persist intent before checking ownership/dispatch. A crash anywhere after
    // this point cannot cause the same operation to be submitted twice.
    await this.evidence(projectId, sessionId, request, "submitted");
    const state = this.options.state(projectId, sessionId);
    let result: SessionSteerResponse;
    if (!state.active || state.turnId !== request.expectedTurnId) {
      result = { ...base, status: "rejected", message: "The target turn is no longer active; no input was sent." };
    } else {
      try { result = await this.options.dispatch(projectId, sessionId, request); }
      catch { result = { ...base, status: "unknown", message: "Input delivery is unconfirmed. It may have been received; it was not resent." }; }
      const confirmed = this.confirmation(await this.options.journal.replay(projectId, sessionId), request, result.providerTurnId);
      if (confirmed && result.status !== "rejected") result = { ...base, status: "accepted", providerTurnId: confirmed };
    }
    await this.evidence(projectId, sessionId, request, result.status, result);
    return result;
  }
}
