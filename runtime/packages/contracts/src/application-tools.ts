import { RuntimeError } from "./errors.js";

export type ApplicationJson = null | boolean | number | string | ApplicationJson[] | { [key: string]: ApplicationJson };
export interface DynamicToolFunctionSpec { type: "function"; name: string; description: string; inputSchema: ApplicationJson; deferLoading?: boolean }
export type DynamicToolSpec = DynamicToolFunctionSpec | { type: "namespace"; name: string; description: string; tools: DynamicToolFunctionSpec[] };
export interface ApplicationToolCatalog { schemaVersion: 1; applicationId: string; workspaceId: string; tools: DynamicToolSpec[] }
export interface ApplicationToolRegistrationRequest { applicationId: string; workspaceId: string; workspaceGeneration: string; tools: DynamicToolSpec[]; timeoutMs: number }
export interface ApplicationToolBinding { schemaVersion: 1; bindingId: string; applicationId: string; workspaceId: string; workspaceGeneration: string; toolSetHash: string; timeoutMs: number }
export interface ApplicationToolResult { success: boolean; contentItems: ({ type: "inputText"; text: string } | { type: "inputImage"; imageUrl: string } | { type: "inputAudio"; audioUrl: string })[] }
export interface ApplicationToolCompletionRequest { bindingId: string; result: ApplicationToolResult }
export interface ApplicationToolInvocation {
  invocationId: string; bindingId: string; applicationId: string; workspaceId: string; workspaceGeneration: string;
  runtimeProjectId: string; runtimeSessionId: string; runtimeTurnId: string; providerThreadId: string; providerTurnId: string;
  requestId: string | number; callId: string; namespace: string | null; tool: string; arguments: ApplicationJson;
  status: "pending" | "completed" | "cancelled" | "failed"; createdAt: string; deadline: string; result?: ApplicationToolResult; failure?: string;
}

// Transport limits only; the application owns JSON Schema and domain validation.
// UTF-8 JSON is capped at 256 KiB, depth 32 and 16,384 nodes; catalog has at most
// 128 descriptors/functions, names 64 ASCII characters, identity tokens 256,
// descriptions 8 KiB, result items 128, timeout 1 second through 1 hour.
export const APPLICATION_TOOL_JSON_MAX_BYTES = 262144;
function invalid(message: string): never { throw new RuntimeError("INVALID_REQUEST", message); }
function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value) || (Object.getPrototypeOf(value) !== Object.prototype && Object.getPrototypeOf(value) !== null)) invalid("Expected a plain JSON object");
  return value as Record<string, unknown>;
}
function keys(value: Record<string, unknown>, allowed: string[]) { if (Object.keys(value).some(key => !allowed.includes(key))) invalid("Unexpected application tool field"); }
function token(value: unknown): string { if (typeof value !== "string" || value.length < 1 || value.length > 256 || /[\u0000-\u001f]/u.test(value)) invalid("Invalid application tool identity"); return value; }
function name(value: unknown): string { if (typeof value !== "string" || !/^[a-zA-Z0-9_-]{1,64}$/.test(value)) invalid("Invalid dynamic tool name"); return value; }
function description(value: unknown): string { if (typeof value !== "string" || value.length > 8192) invalid("Invalid dynamic tool description"); return value; }
export function canonicalApplicationJson(value: unknown): string {
  let nodes = 0;
  const visit = (item: unknown, depth: number): string => {
    if (++nodes > 16384 || depth > 32) invalid("Application tool JSON exceeds structural limits");
    if (item === null || typeof item === "boolean") return JSON.stringify(item);
    if (typeof item === "number") { if (!Number.isFinite(item)) invalid("JSON numbers must be finite"); return JSON.stringify(item); }
    if (typeof item === "string") { if (item.length > APPLICATION_TOOL_JSON_MAX_BYTES) invalid("Application tool string too large"); return JSON.stringify(item); }
    if (Array.isArray(item)) return `[${Array.from(item, child => visit(child, depth + 1)).join(",")}]`;
    const record = object(item);
    return `{${Object.keys(record).sort().map(key => `${visit(key, depth + 1)}:${visit(record[key], depth + 1)}`).join(",")}}`;
  };
  const result = visit(value, 0);
  if (new TextEncoder().encode(result).byteLength > APPLICATION_TOOL_JSON_MAX_BYTES) invalid("Application tool JSON exceeds 256 KiB");
  return result;
}
export function applicationToolKey(namespace: string | null, tool: string): string { return JSON.stringify([namespace, tool]); }
function tools(value: unknown): DynamicToolSpec[] {
  if (!Array.isArray(value) || value.length > 128) invalid("Invalid dynamic tools array");
  const seen = new Set<string>(); let count = 0;
  const fn = (raw: unknown, namespace: string | null): DynamicToolFunctionSpec => {
    const item = object(raw); keys(item, ["type", "name", "description", "inputSchema", "deferLoading"]);
    if (item.type !== "function" || !Object.hasOwn(item, "inputSchema")) invalid("Invalid dynamic function spec");
    const toolName = name(item.name); const key = applicationToolKey(namespace, toolName);
    if (seen.has(key) || ++count > 128) invalid("Duplicate or excessive dynamic tools"); seen.add(key);
    if (item.deferLoading !== undefined && typeof item.deferLoading !== "boolean") invalid("Invalid deferLoading");
    return { type: "function", name: toolName, description: description(item.description), inputSchema: JSON.parse(canonicalApplicationJson(item.inputSchema)) as ApplicationJson, ...(item.deferLoading === undefined ? {} : { deferLoading: item.deferLoading as boolean }) };
  };
  const top = new Set<string>();
  return value.map(raw => {
    const item = object(raw); const itemName = name(item.name);
    if (top.has(itemName)) invalid("Duplicate top-level dynamic tool name"); top.add(itemName);
    if (item.type === "function") return fn(item, null);
    keys(item, ["type", "name", "description", "tools"]);
    if (item.type !== "namespace" || !Array.isArray(item.tools) || item.tools.length === 0 || ++count > 128) invalid("Invalid dynamic namespace spec");
    return { type: "namespace", name: itemName, description: description(item.description), tools: item.tools.map(child => fn(child, itemName)) };
  });
}
export function validateApplicationToolCatalog(value: unknown): ApplicationToolCatalog {
  canonicalApplicationJson(value); const item = object(value); keys(item, ["schemaVersion", "applicationId", "workspaceId", "tools"]);
  if (item.schemaVersion !== 1) invalid("Unsupported application tool catalog version");
  return { schemaVersion: 1, applicationId: token(item.applicationId), workspaceId: token(item.workspaceId), tools: tools(item.tools) };
}
export function validateApplicationToolRegistration(value: unknown): ApplicationToolRegistrationRequest {
  canonicalApplicationJson(value); const item = object(value); keys(item, ["applicationId", "workspaceId", "workspaceGeneration", "tools", "timeoutMs"]);
  if (typeof item.timeoutMs !== "number" || !Number.isInteger(item.timeoutMs) || item.timeoutMs < 1000 || item.timeoutMs > 3600000) invalid("timeoutMs must be an integer from 1000 through 3600000");
  return { applicationId: token(item.applicationId), workspaceId: token(item.workspaceId), workspaceGeneration: token(item.workspaceGeneration), tools: tools(item.tools), timeoutMs: item.timeoutMs };
}
export function validateApplicationToolResult(value: unknown): ApplicationToolResult {
  canonicalApplicationJson(value); const item = object(value); keys(item, ["success", "contentItems"]);
  if (typeof item.success !== "boolean" || !Array.isArray(item.contentItems) || item.contentItems.length > 128) invalid("Invalid application tool result");
  const contentItems = item.contentItems.map(raw => {
    const content = object(raw); const field = content.type === "inputText" ? "text" : content.type === "inputImage" ? "imageUrl" : content.type === "inputAudio" ? "audioUrl" : invalid("Unknown result content type");
    keys(content, ["type", field]); if (typeof content[field] !== "string") invalid("Invalid result content");
    return { ...content } as ApplicationToolResult["contentItems"][number];
  });
  return { success: item.success, contentItems };
}
export function validateApplicationToolCompletion(value: unknown): ApplicationToolCompletionRequest {
  canonicalApplicationJson(value); const item = object(value); keys(item, ["bindingId", "result"]);
  return { bindingId: token(item.bindingId), result: validateApplicationToolResult(item.result) };
}
