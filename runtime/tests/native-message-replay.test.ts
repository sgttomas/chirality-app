import { describe, expect, it } from "vitest";
import { deriveTranscriptView, type HarnessEvent } from "@chirality/runtime-contracts";

let id = 0;
function event(type: HarnessEvent["type"], data: Record<string, unknown>, turnId = "r1"): HarnessEvent {
  return { schemaVersion: 1, eventId: String(++id), timestamp: "now", sessionId: "s1", turnId, type, data };
}
function native(method: string, data: Record<string, unknown>, primary = true): HarnessEvent {
  return event("codex.notification", { method, codex: { isPrimaryThread: primary }, params: { threadId: primary ? "primary" : "child", turnId: "n1", ...data } });
}
describe("Native transcript message boundaries", () => {
  it("replaces partial text with authoritative completion, preserves phases and ignores duplicated frames/late deltas", () => {
    const delta = native("item/agentMessage/delta", { itemId: "m1", delta: "Checking" });
    const final = native("item/completed", { item: { type: "agentMessage", id: "m2", phase: "final_answer", text: "Done." } });
    const events = [event("turn.accepted", { message: "hello" }), delta, delta,
      native("item/completed", { item: { type: "agentMessage", id: "m1", phase: "commentary", text: "Checked it." } }),
      native("item/agentMessage/delta", { itemId: "m1", delta: "duplicate" }), final, final,
      event("message.delta", { text: "legacy aggregate" }), event("message.completed", { role: "assistant", text: "legacy complete" }),
      native("item/completed", { item: { type: "agentMessage", id: "child-message", phase: "final_answer", text: "child secret" } }, false)];
    expect(deriveTranscriptView(events).items.map(row => [row.role, row.text, row.phase])).toEqual([
      ["user", "hello", undefined], ["assistant", "Checked it.", "commentary"], ["assistant", "Done.", "final_answer"]
    ]);
    expect(deriveTranscriptView(events.slice(0,3)).items[1]).toMatchObject({ text: "Checking", phase: null, status: "started", nativeItemId: "m1" });
  });
  it("keeps unknown phases and legacy-only turns readable", () => {
    const events = [native("item/completed", { item: { type: "agentMessage", id: "m1", phase: null, text: "Unknown phase" } }), event("message.delta", { text: "Legacy" }, "r2")];
    expect(deriveTranscriptView(events).items.map(row => [row.text,row.phase])).toEqual([["Unknown phase", null],["Legacy",undefined]]);
  });
});
