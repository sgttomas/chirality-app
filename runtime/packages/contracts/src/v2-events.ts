import type { RuntimeEvent } from "./events.js";

export const HARNESS_V2_TERMINALS = ["turn.completed", "turn.failed", "turn.interrupted", "turn.cancelled"] as const;
export interface EventAttributionV2 { adapterId: string; providerId: string; model: string; reasoningEffort?: string }
interface EventPayloadsV2 {
  "session.created": { role: "untyped" | "agent0" | "agent1" | "agent2" | "task" };
  "session.resumed": { resumed: true };
  "turn.accepted": { message: string };
  "turn.started": { started: true };
  "message.started": { messageId: string };
  "message.delta": { text: string };
  "message.completed": { messageId: string };
  "model.request.started": { requestId: string; model: string };
  "model.delta": { requestId: string; text: string };
  "model.completed": { requestId: string };
  "approval.requested": { approvalId: string; actorId: string; host: string; protocol: "http" | "https"; groupingCaveat: string };
  "approval.decided": { approvalId: string; actorId: string; decision: "accept" | "decline" | "acceptForSession"; explicitUserAct: true };
  "turn.completed": { outcome: "completed" };
  "turn.failed": { code: string; message: string };
  "turn.interrupted": { outcome: "interrupted" };
  "turn.cancelled": { outcome: "cancelled" };
  /** Stock Codex notification passthrough: the upstream method name and its raw params. */
  "codex.notification": { method: string; params?: unknown; [key: string]: unknown };
  /** Stock Codex server request awaiting a decision. */
  "codex.request": { method: string; requestId?: string; [key: string]: unknown };
  /** Resolution of a Codex server request; an unanswered request never implies approval. */
  "codex.request.resolved": { outcome: "answered" | "cancelled" | "unsupported" | "failed"; method?: string; requestId?: string; decidedBy?: "user" | "policy" | "runtime"; [key: string]: unknown };
}
export type HarnessEventTypeV2 = keyof EventPayloadsV2;
export type HarnessEventV2 = { [K in HarnessEventTypeV2]: {
  schemaVersion: 2; eventId: string; sequence: number; timestamp: string;
  projectId: string; sessionId: string; turnId: string; attribution?: EventAttributionV2;
  type: K; data: EventPayloadsV2[K];
} }[HarnessEventTypeV2];

const object = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null && !Array.isArray(v) && Object.getPrototypeOf(v) === Object.prototype;
const str = (v: unknown): v is string => typeof v === "string";
const nonempty = (v: unknown): v is string => str(v) && v.trim().length > 0;
const exact = (v: Record<string, unknown>, keys: string[]): boolean => Object.keys(v).length === keys.length && keys.every(k => Object.hasOwn(v, k));
function payload(type: HarnessEventTypeV2, data: Record<string, unknown>): boolean {
  const fields = (...keys: string[]) => exact(data, keys) && keys.every(k => str(data[k]));
  switch (type) {
    case "session.created": return exact(data, ["role"]) && str(data.role) && ["untyped", "agent0", "agent1", "agent2", "task"].includes(data.role);
    case "session.resumed": return exact(data, ["resumed"]) && data.resumed === true;
    case "turn.accepted": return fields("message");
    case "turn.started": return exact(data, ["started"]) && data.started === true;
    case "message.started": case "message.completed": return fields("messageId") && nonempty(data.messageId);
    case "message.delta": return fields("text");
    case "model.request.started": return fields("requestId", "model") && nonempty(data.requestId) && nonempty(data.model);
    case "model.delta": return fields("requestId", "text") && nonempty(data.requestId);
    case "model.completed": return fields("requestId") && nonempty(data.requestId);
    case "approval.requested": return fields("approvalId", "actorId", "host", "protocol", "groupingCaveat") && Object.values(data).every(nonempty) && ["http", "https"].includes(String(data.protocol));
    case "approval.decided": return exact(data, ["approvalId", "actorId", "decision", "explicitUserAct"]) && nonempty(data.approvalId) && nonempty(data.actorId) && str(data.decision) && ["accept", "decline", "acceptForSession"].includes(data.decision) && data.explicitUserAct === true;
    case "turn.failed": return fields("code", "message") && nonempty(data.code);
    case "turn.completed": case "turn.interrupted": case "turn.cancelled": return exact(data, ["outcome"]) && data.outcome === type.slice(5);
    // Codex passthrough carries the raw upstream payload, so only the identifying fields are checked.
    case "codex.notification": case "codex.request": return nonempty(data.method) && (data.requestId === undefined || nonempty(data.requestId));
    case "codex.request.resolved": return str(data.outcome) && ["answered", "cancelled", "unsupported", "failed"].includes(data.outcome)
      && (data.method === undefined || nonempty(data.method)) && (data.requestId === undefined || nonempty(data.requestId))
      && (data.decidedBy === undefined || (str(data.decidedBy) && ["user", "policy", "runtime"].includes(data.decidedBy)));
    default: return false;
  }
}
/** Strict canonical wire validation: unknown envelope and payload fields are rejected. */
export function validateHarnessEventV2(value: unknown): value is HarnessEventV2 {
  if (!object(value)) return false;
  const keys = ["schemaVersion", "eventId", "sequence", "timestamp", "projectId", "sessionId", "turnId", "type", "data"];
  if (Object.hasOwn(value, "attribution")) keys.push("attribution");
  if (!exact(value, keys) || value.schemaVersion !== 2 || !Number.isSafeInteger(value.sequence) || Number(value.sequence) < 0) return false;
  if (![value.eventId, value.projectId, value.sessionId, value.turnId, value.type].every(nonempty)) return false;
  if (!str(value.timestamp) || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value.timestamp) || !Number.isFinite(Date.parse(value.timestamp))) return false;
  if (new Date(value.timestamp).toISOString() !== value.timestamp.replace(/Z$/, value.timestamp.includes(".") ? "Z" : ".000Z")) return false;
  if (value.attribution !== undefined && (!object(value.attribution) || !exact(value.attribution, Object.hasOwn(value.attribution, "reasoningEffort") ? ["adapterId", "providerId", "model", "reasoningEffort"] : ["adapterId", "providerId", "model"]) || !Object.values(value.attribution).every(nonempty))) return false;
  return object(value.data) && payload(value.type as HarnessEventTypeV2, value.data);
}
export type EventProjectionV2 = { kind: "event"; event: HarnessEventV2 } | { kind: "quarantined"; reason: "unsupported_event" | "invalid_payload" | "invalid_envelope" };
/** Project only documented runtime events. Quarantine never echoes unknown provider content. */
export function projectRuntimeEventV2(source: Omit<RuntimeEvent, "type"> & { type: RuntimeEvent["type"] | "turn.cancelled" }): EventProjectionV2 {
  if (source.schemaVersion !== "chirality.event/v1") return { kind: "quarantined", reason: "invalid_envelope" };
  const data = object(source.data) ? source.data : {};
  let projected: unknown;
  switch (source.type) {
    case "turn.accepted": projected = { message: data.message }; break;
    case "turn.started": projected = { started: true }; break;
    case "message.delta": projected = { text: data.text }; break;
    case "turn.completed": projected = { outcome: "completed" }; break;
    case "turn.interrupted": projected = { outcome: "interrupted" }; break;
    case "turn.cancelled": projected = { outcome: "cancelled" }; break;
    case "turn.failed": projected = { code: data.code, message: data.message }; break;
    default: return { kind: "quarantined", reason: "unsupported_event" };
  }
  const event = {
    schemaVersion: 2, eventId: source.id, sequence: source.sequence, timestamp: source.timestamp,
    projectId: source.projectId, sessionId: source.sessionId, turnId: source.turnId, type: source.type, data: projected,
    ...(source.attribution ? { attribution: { adapterId: source.attribution.adapterId, providerId: source.attribution.providerId, model: source.attribution.model, ...(source.attribution.reasoningEffort === undefined ? {} : { reasoningEffort: source.attribution.reasoningEffort }) } } : {})
  };
  return validateHarnessEventV2(event) ? { kind: "event", event } : { kind: "quarantined", reason: "invalid_payload" };
}
