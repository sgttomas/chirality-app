import { randomUUID } from "node:crypto";
import { HarnessError, type UIEvent } from "@chirality/runtime-contracts";
/** Canonical projection only; never forward provider/SDK envelopes or diagnostic payloads. */
export function mapPiEvent(event: unknown, identity?: { sessionId: string; turnId: string }): UIEvent[] {
  if (!event || typeof event !== "object") return [];
  const e = event as Record<string, any>;
  if (e.type === "compaction_start" || e.type === "compaction_end") {
    if (!identity?.sessionId || !identity.turnId || !["manual", "threshold", "overflow"].includes(e.reason)) throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Invalid Pi compaction identity");
    const result = e.result;
    const success = e.type === "compaction_end" && result && !e.aborted && !e.errorMessage;
    if (success && (typeof result.summary !== "string" || !Number.isFinite(result.tokensBefore) || result.tokensBefore < 0 || (result.estimatedTokensAfter !== undefined && (!Number.isFinite(result.estimatedTokensAfter) || result.estimatedTokensAfter < 0)))) throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Invalid Pi compaction evidence");
    return [{ type: "harness:event", data: { schemaVersion: 1, eventId: randomUUID(), sessionId: identity.sessionId, turnId: identity.turnId, timestamp: new Date().toISOString(),
      type: e.type === "compaction_start" ? "context.compaction.started" : success ? "context.compacted" : "context.compaction.failed",
      data: { reason: e.reason, ...(success ? { tokensBefore: result.tokensBefore, summaryBytes: Buffer.byteLength(result.summary), ...(result.estimatedTokensAfter !== undefined ? { estimatedTokensAfter: result.estimatedTokensAfter } : {}) } : e.type === "compaction_end" ? { aborted: e.aborted === true } : {}), ...(e.type === "compaction_end" ? { willRetry: e.willRetry === true } : {}) }
    } }];
  }
  if (e.type === "message_update" && e.assistantMessageEvent?.type === "text_delta") {
    const text = e.assistantMessageEvent.delta;
    if (typeof text !== "string") throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Invalid Pi text event");
    return [{ type: "chat:delta", data: { text } }];
  }
  if (e.type === "message_end" && e.message?.role === "assistant") {
    if (["error", "aborted"].includes(e.message.stopReason)) throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Pi model request did not complete");
    const content = e.message.content;
    if (!Array.isArray(content)) throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Invalid Pi assistant content");
    return [{ type: "chat:complete", data: { text: content.filter(item => item?.type === "text" && typeof item.text === "string").map(item => item.text).join("") } }];
  }
  if (e.type === "tool_execution_end") {
    if (!["read", "read_file"].includes(e.toolName) && !/^chirality_[a-z0-9_]+$/u.test(e.toolName)) throw new HarnessError("PROVIDER_PROTOCOL_FAILURE", 502, "Unexpected Pi tool execution");
    return [{ type: "tool:result", data: { name: e.toolName, ok: e.isError !== true } }];
  }
  return [];
}
