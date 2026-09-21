import { RuntimeError } from "@chirality/runtime-contracts";

/**
 * Keeps the primary failure as the reported error and attaches a later
 * retirement/cleanup failure as its cause. A retirement diagnostic never
 * replaces the failure that made retirement necessary.
 */
export function withRetirementFailure(primary: unknown, retirement: unknown): unknown {
  if (retirement === undefined) return primary;
  if (primary === undefined) return retirement;
  // Idempotent cleanup can return the same rejection through several owners.
  if (primary === retirement) return primary;
  if (primary instanceof Error) {
    if (primary.cause === undefined) { try { Object.defineProperty(primary, "cause", { value: retirement, writable: true, configurable: true, enumerable: false }); return primary; } catch { /* frozen error */ } }
    const combined = new AggregateError([primary, retirement], primary.message);
    combined.name = primary.name;
    if (primary instanceof RuntimeError) { Object.defineProperty(combined, "code", { value: primary.code, enumerable: true }); Object.defineProperty(combined, "status", { value: primary.status, enumerable: true }); if (primary.details !== undefined) Object.defineProperty(combined, "details", { value: primary.details, enumerable: true }); }
    return combined;
  }
  return new AggregateError([primary, retirement], "Failure and retirement failed");
}

const MAX_DETAIL_STRING = 512, MAX_CAUSE_DEPTH = 4, MAX_DETAIL_KEYS = 32;

function boundedScalar(value: unknown): string | number | boolean | null | undefined {
  if (value === null || typeof value === "boolean") return value;
  if (typeof value === "number") return Number.isFinite(value) ? value : undefined;
  if (typeof value === "string") return value.length > MAX_DETAIL_STRING ? `${value.slice(0, MAX_DETAIL_STRING)}…` : value;
  return undefined;
}

function describeCause(error: unknown, depth: number): Record<string, unknown> | undefined {
  if (depth > MAX_CAUSE_DEPTH || !(error instanceof Error)) return error === undefined ? undefined : { message: boundedScalar(String(error)) };
  const description: Record<string, unknown> = { name: boundedScalar(error.name), message: boundedScalar(error.message) };
  if (error instanceof RuntimeError) { description.code = error.code; const details = boundedDetails(error.details); if (details) description.details = details; }
  if (error instanceof AggregateError) description.errors = error.errors.slice(0, 8).map(inner => describeCause(inner, depth + 1));
  const cause = describeCause(error.cause, depth + 1); if (cause) description.cause = cause;
  return description;
}

function boundedDetails(details: unknown): Record<string, unknown> | undefined {
  if (!details || typeof details !== "object") return undefined;
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(details).slice(0, MAX_DETAIL_KEYS)) {
    if (Array.isArray(value)) { const items = value.slice(0, 32).map(boundedScalar).filter(item => item !== undefined); if (items.length) result[key] = items; continue; }
    const scalar = boundedScalar(value); if (scalar !== undefined) result[key] = scalar;
  }
  return Object.keys(result).length ? result : undefined;
}

/**
 * Bounded, serializable failure evidence for durable events and logs: the
 * error's own scalar details plus the messages of its cause chain. Never
 * carries stack traces or unbounded payloads.
 */
export function describeFailureDetails(error: unknown): Record<string, unknown> | undefined {
  if (!(error instanceof Error)) return undefined;
  const result: Record<string, unknown> = {};
  if (error instanceof RuntimeError) { const details = boundedDetails(error.details); if (details) Object.assign(result, details); }
  if (error instanceof AggregateError) { const errors = error.errors.slice(0, 8).map(inner => describeCause(inner, 1)).filter(Boolean); if (errors.length) result.errors = errors; }
  const cause = describeCause(error.cause, 1); if (cause) result.cause = cause;
  return Object.keys(result).length ? result : undefined;
}
