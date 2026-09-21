import { afterEach, describe, expect, it, vi } from "vitest";
import { ApplicationToolRegistry, type ApplicationToolCall, type ApplicationToolSessions } from "../packages/daemon/src/application-tools.js";
import { canonicalApplicationJson, validateApplicationToolCatalog, validateApplicationToolRegistration, validateApplicationToolResult, type ApplicationToolCatalog, type ApplicationToolRegistrationRequest, type RuntimeSessionRecord } from "@chirality/runtime-contracts";
const request = (): ApplicationToolRegistrationRequest => ({ applicationId: "test-app", workspaceId: "w", workspaceGeneration: "g1", timeoutMs: 1000, tools: [{ type: "function", name: "inspect", description: "Inspect", inputSchema: { type: "object" } }, { type: "namespace", name: "edit", description: "Edits", tools: [{ type: "function", name: "preview", description: "Preview", inputSchema: true }] }] });
const result = () => ({ success: true, contentItems: [{ type: "inputText" as const, text: "done" }] });
function fixture() {
  let catalog: ApplicationToolCatalog | undefined;
  const record = { status: "idle" } as RuntimeSessionRecord;
  const sessions: ApplicationToolSessions = {
    get: async () => record,
    getApplicationToolCatalog: async () => catalog && structuredClone(catalog),
    registerApplicationToolCatalog: async (_p, _s, next) => { if (catalog && canonicalApplicationJson(next) !== canonicalApplicationJson(catalog)) throw Error("immutable"); catalog = structuredClone(next); return structuredClone(catalog); }
  };
  const registry = new ApplicationToolRegistry({ sessions });
  return { sessions, registry, record };
}
async function ready(registry: ApplicationToolRegistry) {
  const binding = await registry.register("p", "s", request());
  await registry.prepareTurn("p", "s", "t");
  const call: ApplicationToolCall = { bindingId: binding.bindingId, runtimeProjectId: "p", runtimeSessionId: "s", runtimeTurnId: "t", providerThreadId: "pt", providerTurnId: "tt", requestId: 1, callId: "c", namespace: null, tool: "inspect", arguments: { x: 1 } };
  return { binding, call };
}
afterEach(() => vi.useRealTimers());
describe("application tool contracts", () => {
  it("clones descriptions and validates bounded transport without interpreting JSON Schema", () => {
    const input = request(); const copy = validateApplicationToolRegistration(input); input.tools[0]!.description = "changed";
    expect(copy.tools[0]!.description).toBe("Inspect");
    expect(canonicalApplicationJson({ b: 2, a: 1 })).toBe('{"a":1,"b":2}');
    expect(() => validateApplicationToolRegistration({ ...request(), callbackUrl: "https://example.test" })).toThrow();
    expect(() => validateApplicationToolRegistration({ ...request(), timeoutMs: 999 })).toThrow();
    expect(() => validateApplicationToolRegistration({ ...request(), tools: [request().tools[0], request().tools[0]] })).toThrow();
    expect(() => canonicalApplicationJson({ bad: undefined })).toThrow();
    expect(() => canonicalApplicationJson({ bad: Infinity })).toThrow();
    expect(() => canonicalApplicationJson("x".repeat(262144))).toThrow();
    const cyclic: unknown[] = []; cyclic.push(cyclic); expect(() => canonicalApplicationJson(cyclic)).toThrow();
    expect(() => validateApplicationToolCatalog({ ...request(), schemaVersion: 2 })).toThrow();
    expect(validateApplicationToolResult({ success: false, contentItems: [{ type: "inputImage", imageUrl: "data:test" }, { type: "inputAudio", audioUrl: "data:test" }] }).success).toBe(false);
    expect(() => validateApplicationToolResult({ success: true, contentItems: [{ type: "text", text: "wrong upstream shape" }] })).toThrow();
  });
});
describe("application tool registry", () => {
  it("registers, freezes and defensively returns catalog and result ownership", async () => {
    const { registry } = fixture(); const req = request(); const first = await registry.register("p", "s", req); req.tools[0]!.name = "mutated";
    first.workspaceGeneration = "mutated"; const { binding, call } = await ready(registry);
    expect(binding.workspaceGeneration).toBe("g1");
    const promise = registry.call(call); call.arguments = { mutated: true };
    const [invocation] = registry.listCalls("p", "s", binding.bindingId); expect(invocation!.arguments).toEqual({ x: 1 });
    invocation!.arguments = null; expect(registry.listCalls("p", "s", binding.bindingId)[0]!.arguments).toEqual({ x: 1 });
    const output = result(); expect(registry.complete("p", "s", invocation!.invocationId, { bindingId: binding.bindingId, result: output })).toEqual({ state: "completed" });
    output.contentItems[0]!.text = "mutated"; expect(await promise).toEqual(result()); registry.close();
  });
  it("deduplicates calls and completions and rejects argument or result conflicts", async () => {
    const { registry } = fixture(); const { binding, call } = await ready(registry);
    const one = registry.call(call); const two = registry.call({ ...call, requestId: 2 });
    expect((await registry.call({ ...call, arguments: {} })).success).toBe(false);
    const calls = registry.listCalls("p", "s", binding.bindingId); expect(calls).toHaveLength(1);
    const completion = { bindingId: binding.bindingId, result: result() };
    registry.complete("p", "s", calls[0]!.invocationId, completion);
    expect(registry.complete("p", "s", calls[0]!.invocationId, completion)).toEqual({ state: "already-completed" });
    expect(() => registry.complete("p", "s", calls[0]!.invocationId, { ...completion, result: { success: false, contentItems: [] } })).toThrow();
    expect(await one).toEqual(await two); expect(await registry.call(call)).toEqual(result()); registry.close();
  });
  it("requires explicit rebind after restart, permits same active registration, forbids changed active binding", async () => {
    const { registry, sessions } = fixture(); const { binding } = await ready(registry);
    expect((await registry.register("p", "s", request())).bindingId).toBe(binding.bindingId);
    await expect(registry.register("p", "s", { ...request(), workspaceGeneration: "g2" })).rejects.toThrow();
    registry.close(); const restarted = new ApplicationToolRegistry({ sessions });
    expect((await restarted.binding("p", "s")).binding).toBeUndefined();
    await expect(restarted.prepareTurn("p", "s", "t2")).rejects.toThrow(/rebind/);
    const next = await restarted.register("p", "s", request()); expect(next.bindingId).not.toBe(binding.bindingId);
    await expect(restarted.register("p", "s", { ...request(), applicationId: "other" })).rejects.toThrow(/immutable/);
    restarted.close();
  });
  it("serializes concurrent registration and preparation in either order", async () => {
    const { registry } = fixture(); const registration = registry.register("p", "s", request()); const preparation = registry.prepareTurn("p", "s", "t");
    expect((await preparation)!.binding.bindingId).toBe((await registration).bindingId); registry.close();
    const unused = fixture(); const other = unused.registry;
    expect(await other.prepareTurn("p", "s", "t")).toBeUndefined();
    unused.record.status = "running";
    await expect(other.register("p", "s", request())).rejects.toThrow(/idle/); other.close();
  });
  it("does not claim tool-free turns and allows binding when the session remains genuinely unused", async () => {
    const { registry } = fixture();
    expect(await registry.prepareTurn("p", "s", "t1")).toBeUndefined();
    expect(await registry.prepareTurn("p", "s", "t2")).toBeUndefined();
    const binding = await registry.register("p", "s", request());
    expect((await registry.prepareTurn("p", "s", "t3"))!.binding.bindingId).toBe(binding.bindingId);
    registry.close();
  });
  it("acknowledges identical completed results after finish but rejects conflicts and old bindings", async () => {
    const { registry } = fixture(); const { binding, call } = await ready(registry);
    const pending = registry.call(call); const id = registry.listCalls("p", "s", binding.bindingId)[0]!.invocationId;
    const completion = { bindingId: binding.bindingId, result: result() };
    registry.complete("p", "s", id, completion); await pending;
    registry.finishTurn("p", "s", "t", "done");
    expect(registry.complete("p", "s", id, completion)).toEqual({ state: "already-completed" });
    expect(() => registry.complete("p", "s", id, { ...completion, result: { success: false, contentItems: [] } })).toThrow(/Conflicting/);
    expect((await registry.call(call)).success).toBe(false);
    await registry.register("p", "s", { ...request(), workspaceGeneration: "g2" });
    expect(() => registry.complete("p", "s", id, completion)).toThrow();
    registry.close();
  });
  it("times out pending calls and refuses late completions", async () => {
    vi.useFakeTimers(); const { registry } = fixture(); const { binding, call } = await ready(registry); const pending = registry.call(call);
    const id = registry.listCalls("p", "s", binding.bindingId)[0]!.invocationId; await vi.advanceTimersByTimeAsync(1000);
    expect((await pending).success).toBe(false); expect(registry.listCalls("p", "s", binding.bindingId)[0]!.status).toBe("failed");
    expect(() => registry.complete("p", "s", id, { bindingId: binding.bindingId, result: result() })).toThrow(); registry.close(); expect(vi.getTimerCount()).toBe(0);
  });
  it("settles finish, release and close without redispatching stale calls", async () => {
    for (const action of ["finish", "release", "close"]) {
      const { registry } = fixture(); const { binding, call } = await ready(registry); const pending = registry.call(call);
      if (action === "finish") registry.finishTurn("p", "s", "t", "interrupted");
      else if (action === "release") await registry.release("p", "s", binding.bindingId);
      else registry.close();
      expect((await pending).success).toBe(false); expect((await registry.call(call)).success).toBe(false);
      if (action !== "close") expect(registry.listCalls("p", "s", binding.bindingId)[0]!.status).toBe("cancelled"); registry.close();
    }
  });
  it("cancels one child invocation without cancelling other calls under the parent turn", async () => {
    vi.useFakeTimers();
    const { registry } = fixture(); const { binding, call } = await ready(registry);
    const child = { ...call, providerThreadId: "child-thread", providerTurnId: "child-turn" };
    const childPending = registry.call(child); const parentPending = registry.call(call);
    for (const patch of [{ bindingId: "foreign" }, { runtimeSessionId: "foreign" }, { runtimeTurnId: "old" }, { providerTurnId: "old" }, { callId: "unknown" }]) {
      registry.cancelCall({ ...child, ...patch }, "ignored");
    }
    expect(registry.listCalls("p", "s", binding.bindingId).map(item => item.status)).toEqual(["pending", "pending"]);
    registry.cancelCall(child, "child turn ended");
    expect((await childPending).success).toBe(false);
    const calls = registry.listCalls("p", "s", binding.bindingId);
    expect(calls.map(item => item.status)).toEqual(["cancelled", "pending"]);
    expect(vi.getTimerCount()).toBe(1);
    expect(() => registry.complete("p", "s", calls[0]!.invocationId, { bindingId: binding.bindingId, result: result() })).toThrow();
    expect((await registry.call(child)).success).toBe(false);
    expect(registry.listCalls("p", "s", binding.bindingId)).toHaveLength(2);
    registry.complete("p", "s", calls[1]!.invocationId, { bindingId: binding.bindingId, result: result() });
    expect(await parentPending).toEqual(result());
    registry.cancelCall(call, "terminal call is unchanged");
    expect(registry.listCalls("p", "s", binding.bindingId)[1]!.status).toBe("completed");
    expect(vi.getTimerCount()).toBe(0); registry.close();
  });
  it("does not publish a binding after close during an awaited registration", async () => {
    const { sessions } = fixture(); let proceed!: () => void;
    const gate = new Promise<void>(resolve => { proceed = resolve; });
    const get = sessions.get; sessions.get = async (...args) => { await gate; return get(...args); };
    const registry = new ApplicationToolRegistry({ sessions });
    const registration = registry.register("p", "s", request()); await Promise.resolve(); registry.close(); proceed();
    await expect(registration).rejects.toThrow(/closed/);
  });
  it("supports namespace dispatch and refuses unknown or foreign bindings and sources", async () => {
    const { registry } = fixture(); const { binding, call } = await ready(registry);
    for (const patch of [{ bindingId: "foreign" }, { runtimeSessionId: "other" }, { runtimeTurnId: "old" }, { namespace: "wrong" }, { tool: "missing" }]) expect((await registry.call({ ...call, ...patch })).success).toBe(false);
    const pending = registry.call({ ...call, namespace: "edit", tool: "preview" }); const id = registry.listCalls("p", "s", binding.bindingId)[0]!.invocationId;
    expect(() => registry.complete("p", "other", id, { bindingId: binding.bindingId, result: result() })).toThrow();
    registry.finishTurn("p", "s", "t", "done"); await pending;
    const rebound = await registry.register("p", "s", { ...request(), workspaceGeneration: "g2" }); expect(rebound.bindingId).not.toBe(binding.bindingId);
    await registry.prepareTurn("p", "s", "t2"); expect((await registry.call(call)).success).toBe(false); registry.close();
  });
});
