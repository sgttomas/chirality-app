import { describe, expect, it, vi } from "vitest";
import { deriveTranscriptView, validateSessionSteerRequest, type HarnessEvent, type SessionSteerResponse } from "@chirality/runtime-contracts";
import { NativeSteering, type NativeSteeringOptions } from "../packages/daemon/src/native-steering.js";

const request = { operationId: "input-1", expectedTurnId: "runtime-1", text: "Use the second approach" };
function fixture() {
  const events: HarnessEvent[] = [];
  let active = true;
  const dispatch = vi.fn(async (): Promise<SessionSteerResponse> => ({ operationId: request.operationId, turnId: request.expectedTurnId, providerTurnId: "native-1", status: "accepted" }));
  const publish = vi.fn();
  const options: NativeSteeringOptions = {
    journal: { async replay() { return structuredClone(events); }, async appendEvent(_project, input) {
      const event: HarnessEvent = { ...structuredClone(input), schemaVersion: 1, eventId: `e${events.length}`, timestamp: new Date().toISOString() };
      events.push(event); return event;
    } },
    state: () => ({ active, turnId: "runtime-1", lastSeq: 0 }), publish, dispatch
  };
  return { events, options, dispatch, publish, stop() { active = false; }, steering: new NativeSteering(options) };
}
function confirmation(overrides: Record<string, unknown> = {}): HarnessEvent {
  return { schemaVersion: 1, eventId: "confirmation", timestamp: "now", sessionId: "s", turnId: "runtime-1", type: "codex.notification", data: {
    method: "item/started", codex: { isPrimaryThread: true }, params: { threadId: "native-thread", turnId: "native-1", item: { type: "userMessage", id: "user1", clientId: request.operationId, content: [{ type: "text", text: request.text }] } }, ...overrides
  } };
}
describe("Native steering receipt evidence", () => {
  it("persists intent before dispatch, publishes the same evidence and deduplicates concurrent/restarted requests", async () => {
    const f = fixture();
    f.dispatch.mockImplementation(async () => {
      expect(f.events[0]?.data.status).toBe("submitted");
      return { operationId: request.operationId, turnId: request.expectedTurnId, status: "accepted", providerTurnId: "native-1" };
    });
    const [a,b] = await Promise.all([f.steering.steer("p", "s", request), f.steering.steer("p", "s", request)]);
    expect(a).toEqual(b); expect(f.dispatch).toHaveBeenCalledTimes(1);
    f.stop();
    expect(await new NativeSteering(f.options).steer("p", "s", request)).toEqual(a);
    expect(f.dispatch).toHaveBeenCalledTimes(1);
    expect(f.publish).toHaveBeenCalledTimes(2);
    expect(f.events.map(event => event.data.status)).toEqual(["submitted", "accepted"]);
    await expect(new NativeSteering(f.options).steer("p", "s", { ...request, text: "changed" })).rejects.toMatchObject({ status: 409 });
  });
  it("rejects stale ownership without supplier input and preserves rejection on retry", async () => {
    const f = fixture(); f.stop();
    expect(await f.steering.steer("p", "s", request)).toMatchObject({ status: "rejected" });
    expect(await f.steering.steer("p", "s", request)).toMatchObject({ status: "rejected" });
    expect(f.dispatch).not.toHaveBeenCalled();
  });
  it("never resends after lost acknowledgment or a crash following persisted intent, but reconciles exact native echo", async () => {
    const f = fixture(); f.dispatch.mockRejectedValue(new Error("lost response"));
    expect(await f.steering.steer("p", "s", request)).toMatchObject({ status: "unknown" });
    const restarted = new NativeSteering(f.options);
    expect(await restarted.steer("p", "s", request)).toMatchObject({ status: "unknown" });
    f.events.push(confirmation({ codex: { isPrimaryThread: false } }));
    expect(await restarted.steer("p", "s", request)).toMatchObject({ status: "unknown" });
    f.events.push(confirmation());
    expect(await restarted.steer("p", "s", request)).toMatchObject({ status: "accepted", providerTurnId: "native-1" });
    expect(f.dispatch).toHaveBeenCalledTimes(1);
    const crash = fixture();
    await crash.options.journal.appendEvent("p", { sessionId: "s", turnId: request.expectedTurnId, type: "codex.steer", data: { ...request, status: "submitted" } });
    expect(await new NativeSteering(crash.options).steer("p", "s", request)).toMatchObject({ status: "unknown" });
    expect(crash.dispatch).not.toHaveBeenCalled();
  });
  it("validates text and identities and renders a single historical user message with receipt status", async () => {
    for (const value of [{ ...request, text: " " }, { ...request, operationId: "../bad" }, { ...request, nativeThreadId: "unowned" }]) expect(() => validateSessionSteerRequest(value)).toThrow();
    const f = fixture(); await f.steering.steer("p", "s", request);
    const view = deriveTranscriptView(f.events);
    expect(view.items).toHaveLength(1);
    expect(view.items[0]).toMatchObject({ role: "user", text: request.text, status: "accepted" });
  });
});

  it("uses the encoded session steering route in the Runtime client", async () => {
    const { RuntimeClient } = await import("@chirality/runtime-client");
    const client = new RuntimeClient({ socketPath: "/unused", tokenFile: "/unused" });
    const transport = vi.spyOn(client, "requestJson").mockResolvedValue({ operationId: request.operationId, turnId: request.expectedTurnId, status: "accepted" });
    await client.sessionTurnSteer("project name", "session/id", request);
    expect(transport).toHaveBeenCalledWith("/v1/projects/project%20name/sessions/session%2Fid/turn/steer", { method: "POST", body: request, signal: undefined });
  });

describe("receipt-only reconciliation", () => {
  const lookup = { operationId: request.operationId, expectedTurnId: request.expectedTurnId };
  it("never creates intent or dispatches when the initial transport was lost before Runtime, even with an active turn", async () => {
    const f = fixture();
    expect(await f.steering.receipt("p", "s", lookup)).toMatchObject({ status: "unknown" });
    f.events.push(confirmation()); // No intent: an echo alone cannot reconstruct the original authorized request.
    expect(await new NativeSteering(f.options).receipt("p", "s", lookup)).toMatchObject({ status: "unknown" });
    expect(f.events).toHaveLength(1);
    expect(f.dispatch).not.toHaveBeenCalled();
    expect(f.publish).not.toHaveBeenCalled();
  });
  it("confirms a late durable echo after unknown, turn completion and manager reload without dispatching again", async () => {
    const f = fixture(); f.dispatch.mockRejectedValue(new Error("lost response"));
    expect(await f.steering.steer("p", "s", request)).toMatchObject({ status: "unknown" });
    f.stop();
    const restarted = new NativeSteering(f.options);
    expect(await restarted.receipt("p", "s", lookup)).toMatchObject({ status: "unknown" });
    expect(f.events.map(event => event.data.status)).toEqual(["submitted", "unknown"]);
    f.events.push(confirmation({ codex: { isPrimaryThread: false } }));
    expect(await restarted.receipt("p", "s", lookup)).toMatchObject({ status: "unknown" });
    f.events.push(confirmation());
    expect(await restarted.receipt("p", "s", lookup)).toMatchObject({ status: "accepted", providerTurnId: "native-1" });
    expect(f.events.at(-1)).toMatchObject({ type: "codex.steer", data: { ...request, status: "accepted" } });
    expect(await new NativeSteering(f.options).receipt("p", "s", lookup)).toMatchObject({ status: "accepted" });
    expect(f.dispatch).toHaveBeenCalledTimes(1);
    expect(deriveTranscriptView(f.events).items.find(item => item.role === "user")).toMatchObject({ status: "accepted", text: request.text });
  });
  it("preserves explicit rejection and refuses mismatched turn identity or input-bearing receipt bodies", async () => {
    const f = fixture(); f.stop(); await f.steering.steer("p", "s", request);
    f.events.push(confirmation());
    expect(await f.steering.receipt("p", "s", lookup)).toMatchObject({ status: "rejected" });
    await expect(f.steering.receipt("p", "s", { ...lookup, expectedTurnId: "wrong-turn" })).rejects.toMatchObject({ status: 409 });
    await expect(f.steering.receipt("p", "s", { ...lookup, text: "not allowed" } as never)).rejects.toMatchObject({ status: 400 });
    expect(f.dispatch).not.toHaveBeenCalled();
  });
  it("waits for an in-flight original outcome before reconciling without creating a second dispatch", async () => {
    const f = fixture();
    let release!: (value: SessionSteerResponse) => void;
    f.dispatch.mockImplementation(() => new Promise(resolve => { release = resolve; }));
    const original = f.steering.steer("p", "s", request);
    await vi.waitFor(() => expect(f.dispatch).toHaveBeenCalledTimes(1));
    let checked = false;
    const receipt = f.steering.receipt("p", "s", lookup).then(value => { checked = true; return value; });
    await Promise.resolve(); expect(checked).toBe(false);
    release({ operationId: lookup.operationId, turnId: lookup.expectedTurnId, status: "unknown" });
    await original;
    expect(await receipt).toMatchObject({ status: "unknown" });
    expect(f.events.map(event => event.data.status)).toEqual(["submitted", "unknown"]);
    expect(f.dispatch).toHaveBeenCalledTimes(1);
  });
  it("uses the encoded dedicated receipt route without including model input", async () => {
    const { RuntimeClient } = await import("@chirality/runtime-client");
    const client = new RuntimeClient({ socketPath: "/unused", tokenFile: "/unused" });
    const transport = vi.spyOn(client, "requestJson").mockResolvedValue({ operationId: lookup.operationId, turnId: lookup.expectedTurnId, status: "unknown" });
    await client.sessionTurnSteerReceipt("project name", "session/id", lookup);
    expect(transport).toHaveBeenCalledWith("/v1/projects/project%20name/sessions/session%2Fid/turn/steer/receipt", { method: "POST", body: lookup, signal: undefined });
  });
});
