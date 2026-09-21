import { describe, expect, it, vi } from "vitest";
import type { ApplicationToolBinding, ApplicationToolCatalog, ApplicationToolResult, DynamicToolSpec, RuntimeSessionRecord } from "@chirality/runtime-contracts";
import type { CodexTurnEnvelope } from "@chirality/runtime-core";
import { ApplicationToolRegistry } from "../packages/daemon/src/application-tools.js";
import { CodexSupervisor, type CodexSupervisorHost, type CodexSupervisorOptions } from "../packages/daemon/src/codex-supervisor.js";
import type { CodexAppServerExit, CodexNotification, CodexServerRequest, CodexServerRequestHandler, CodexServerRequestOutcome } from "../packages/daemon/src/codex-app-server-client.js";
/** Scripted host: records requests, answers from a table, and lets the test raise notifications and server requests. */
function fakeHost() {
  const calls: { method: string; params: any }[] = [];
  let generation = 1;
  let nextThread = 1, nextTurn = 1;
  const listeners = new Set<(notification: CodexNotification) => void>();
  const exits = new Set<(exit: CodexAppServerExit, generation: number) => void>();
  let handler: CodexServerRequestHandler = async () => ({ error: { code: -32601, message: "none" } });
  const answers: Record<string, (params: any) => unknown> = {
    "thread/start": params => ({ thread: { id: `thread-${nextThread++}` }, model: params.model ?? "gpt-5-codex" }),
    "thread/resume": params => ({ thread: { id: params.threadId, status: { type: "idle" } }, model: params.model ?? "gpt-5-codex" }),
    "thread/settings/update": () => ({}),
    "thread/inject_items": () => ({}),
    "thread/loaded/list": () => ({ data: [], nextCursor: null }),
    "turn/start": () => ({ turn: { id: `turn-${nextTurn++}`, status: "inProgress" } }),
    "turn/interrupt": () => ({})
  };
  const host: CodexSupervisorHost & { calls: typeof calls; notify(method: string, params: unknown): void; exit(exit: CodexAppServerExit): void; ask(request: CodexServerRequest): Promise<CodexServerRequestOutcome>; restart(): void; respond(method: string, answer: (params: any) => unknown): void; fail(method: string, error: Error): void } = {
    get generation() { return generation; },
    calls,
    async request<T>(method: string, params: unknown): Promise<T> {
      calls.push({ method, params });
      const failure = failures.get(method);
      if (failure) { failures.delete(method); throw failure; }
      const answer = answers[method];
      if (!answer) throw new Error(`unscripted ${method}`);
      return answer(params) as T;
    },
    onNotification(listener) { listeners.add(listener); return () => { listeners.delete(listener); }; },
    onExit(listener) { exits.add(listener); return () => { exits.delete(listener); }; },
    onStart() { return () => {}; },
    setServerRequestHandler(next) { handler = next; },
    notify(method, params) { for (const listener of listeners) listener({ method, params }); },
    exit(exit) { const current = generation; for (const listener of exits) listener(exit, current); },
    ask(request) { return handler(request); },
    restart() { generation += 1; },
    respond(method, answer) { answers[method] = answer; },
    fail(method, error) { failures.set(method, error); }
  };
  const failures = new Map<string, Error>();
  return host;
}
function envelope(overrides: Partial<CodexTurnEnvelope> = {}): string {
  return JSON.stringify({ schema: "chirality-codex-turn/v1", prompt: "hello", cwd: "/tmp/project", policy: { approvalPolicy: "on-request", sandbox: "workspace-write" }, interactionMode: "chat", requestedRole: "untyped", projectId: "project", sessionId: "session", clientTurnId: "turn-a", ...overrides } satisfies CodexTurnEnvelope);
}
const tools: DynamicToolSpec[] = [{ type: "function", name: "inspect", description: "Inspect", inputSchema: {} }, { type: "namespace", name: "app", description: "App", tools: [{ type: "function", name: "preview", description: "Preview", inputSchema: {} }] }];
const binding: ApplicationToolBinding = { schemaVersion: 1, bindingId: "binding", applicationId: "application", workspaceId: "workspace", workspaceGeneration: "g1", toolSetHash: "hash", timeoutMs: 1000 };
const result: ApplicationToolResult = { success: true, contentItems: [{ type: "inputText", text: "done" }, { type: "inputImage", imageUrl: "data:image/png;base64,AA==" }, { type: "inputAudio", audioUrl: "data:audio/wav;base64,AA==" }] };
function registry() {
  return { prepareTurn: vi.fn(async () => ({ binding, tools })), call: vi.fn(async () => result), finishTurn: vi.fn(), cancelCall: vi.fn() } satisfies NonNullable<CodexSupervisorOptions["applicationTools"]>;
}
function request(overrides: Record<string, unknown> = {}, requestId: string | number = 42): CodexServerRequest {
  return { id: requestId, method: "item/tool/call", params: { threadId: "thread-1", turnId: "turn-1", callId: "call1", namespace: null, tool: "inspect", arguments: { selected: true }, ...overrides } };
}
function complete(host: ReturnType<typeof fakeHost>, turnId = "turn-1") { host.notify("turn/completed", { threadId: "thread-1", turn: { id: turnId, status: "completed" } }); }

// Scripted protocol evidence only; does not qualify native tool inheritance.
describe("application tools on the Codex supervisor", () => {
  it("prepares before creation, supplies exact specs only to thread/start, and rebinds cold resume without replacing tools", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    applicationTools.prepareTurn.mockImplementationOnce(async () => { expect(host.calls).toEqual([]); return { binding, tools }; });
    const first = await supervisor.acquire("w1", envelope());
    expect(applicationTools.prepareTurn).toHaveBeenCalledWith("project", "session", "turn-a");
    expect(host.calls[0]!.params.dynamicTools).toEqual(tools);
    expect(host.calls.slice(1).every(call => !("dynamicTools" in call.params))).toBe(true);
    complete(host); await supervisor.retire(first.workerId, first.generation); host.restart();
    await supervisor.acquire("w2", envelope({ resumeThreadId: "thread-1", clientTurnId: "turn-b" }));
    expect(applicationTools.prepareTurn).toHaveBeenCalledWith("project", "session", "turn-b");
    expect(host.calls.find(call => call.method === "thread/resume")!.params).not.toHaveProperty("dynamicTools");
    expect(applicationTools.call).not.toHaveBeenCalled();
    await supervisor.close(); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(2);
  });
  it("omits tools by default and skips preparation for callers without a session", async () => {
    for (const withPort of [false, true]) {
      const host = fakeHost(), applicationTools = registry();
      const supervisor = new CodexSupervisor({ host, ...(withPort ? { applicationTools } : {}) });
      await supervisor.acquire("w1", envelope({ sessionId: undefined }));
      expect(host.calls[0]!.params).not.toHaveProperty("dynamicTools");
      expect(applicationTools.prepareTurn).not.toHaveBeenCalled();
      expect(await host.ask(request())).toMatchObject({ result: { success: false } });
      await supervisor.close();
    }
  });
  it("returns exact output and original request identity with request/resolution evidence", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    const worker = await supervisor.acquire("w1", envelope());
    expect(await host.ask(request())).toEqual({ result });
    expect(applicationTools.call).toHaveBeenCalledWith({ bindingId: "binding", runtimeProjectId: "project", runtimeSessionId: "session", runtimeTurnId: "turn-a", providerThreadId: "thread-1", providerTurnId: "turn-1", requestId: 42, callId: "call1", namespace: null, tool: "inspect", arguments: { selected: true } });
    const events = await supervisor.drainTurnProgress(worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "request" || event.type === "request-resolved")).toMatchObject([{ type: "request", params: request().params }, { type: "request-resolved", decision: result }]);
    expect(await host.ask(request({ namespace: "app", tool: "preview", callId: "c2" }, "42"))).toEqual({ result });
    await supervisor.close();
  });
  it("refuses malformed, unknown, foreign, stale and duplicate calls without dispatch", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    const worker = await supervisor.acquire("w1", envelope());
    for (const bad of [{ namespace: undefined }, { arguments: undefined }, { callId: 1 }, { threadId: "foreign" }, { turnId: "old" }, { tool: "absent" }, { namespace: "wrong" }]) expect(await host.ask(request(bad))).toMatchObject({ result: { success: false } });
    expect(applicationTools.call).not.toHaveBeenCalled(); await host.ask(request());
    expect(await host.ask(request())).toMatchObject({ result: { success: false } });
    expect(await host.ask(request({}, "other-id"))).toMatchObject({ result: { success: false } });
    expect(applicationTools.call).toHaveBeenCalledTimes(1); complete(host);
    expect(await host.ask(request({ callId: "late" }, 100))).toMatchObject({ result: { success: false } });
    await supervisor.retire(worker.workerId, worker.generation); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1);
  });
  it("waits for primary identity when a call precedes the turn/start response", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    let release!: (value: unknown) => void;
    host.respond("turn/start", () => new Promise(resolve => { release = resolve; }));
    const acquiring = supervisor.acquire("w1", envelope()); await vi.waitFor(() => expect(release).toBeTypeOf("function"));
    const answer = host.ask(request()); await Promise.resolve(); expect(applicationTools.call).not.toHaveBeenCalled();
    release({ turn: { id: "turn-1", status: "inProgress" } }); await acquiring; expect(await answer).toEqual({ result }); await supervisor.close();
  });
  it("routes observed child turns with original IDs before primary adoption and never executes historical items", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    let release!: (value: unknown) => void;
    host.respond("turn/start", () => new Promise(resolve => { release = resolve; }));
    const acquiring = supervisor.acquire("w1", envelope()); await vi.waitFor(() => expect(release).toBeTypeOf("function"));
    host.notify("thread/started", { thread: { id: "child", parentThreadId: "thread-1", status: { type: "active" } } });
    host.notify("turn/started", { threadId: "child", turn: { id: "child-turn" } });
    const childRequest = request({ threadId: "child", turnId: "child-turn", callId: "child-call" }, "child-rpc");
    const answer = host.ask(childRequest); release({ turn: { id: "turn-1", status: "inProgress" } });
    const worker = await acquiring; expect(await answer).toEqual({ result });
    expect(applicationTools.call).toHaveBeenCalledWith(expect.objectContaining({ providerThreadId: "child", providerTurnId: "child-turn", callId: "child-call", requestId: "child-rpc", runtimeTurnId: "turn-a" }));
    const events = await supervisor.drainTurnProgress(worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "request" || event.type === "request-resolved")).toMatchObject([{ providerThreadId: "child", providerTurnId: "child-turn" }, { providerThreadId: "child", providerTurnId: "child-turn" }]);
    host.notify("item/completed", { threadId: "child", turnId: "child-turn", item: { type: "dynamicToolCall", ...childRequest.params as object } });
    host.notify("turn/completed", { threadId: "child", turn: { id: "child-turn", status: "completed" } });
    expect(await host.ask(request({ threadId: "child", turnId: "child-turn", callId: "late" }, 91))).toMatchObject({ result: { success: false } });
    expect(applicationTools.call).toHaveBeenCalledTimes(1); complete(host); await supervisor.retire(worker.workerId, worker.generation);
    host.respond("turn/start", () => ({ turn: { id: "turn-2" } }));
    await supervisor.acquire("w2", envelope({ resumeThreadId: "thread-1", clientTurnId: "turn-b" }));
    expect(await host.ask(request({ threadId: "child", turnId: "child-turn", callId: "old" }, 92))).toMatchObject({ result: { success: false } }); await supervisor.close();
  });
  it.each(["complete", "retire", "interrupt", "exit", "close"])("cancels pending calls and finishes ownership once on %s", async action => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    let deliver!: (value: ApplicationToolResult) => void;
    applicationTools.call.mockImplementation(() => new Promise(resolve => { deliver = resolve; }));
    const worker = await supervisor.acquire("w1", envelope()), answer = host.ask(request());
    await vi.waitFor(() => expect(deliver).toBeTypeOf("function"));
    if (action === "complete") complete(host);
    if (action === "retire") await supervisor.retire(worker.workerId, worker.generation);
    if (action === "exit") host.exit({ code: 1, signal: null });
    if (action === "close") await supervisor.close();
    if (action === "interrupt") { const stopped = supervisor.interrupt(worker.workerId, worker.generation); complete(host); await stopped; }
    expect(await answer).toMatchObject({ result: { success: false } }); deliver(result); await Promise.resolve();
    await supervisor.close(); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1);
  });
  it.each(["thread/start", "thread/settings/update", "turn/start"])("releases prepared ownership on acquisition failure at %s", async method => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools }); host.fail(method, new Error("failed"));
    await expect(supervisor.acquire("w1", envelope())).rejects.toThrow("failed"); await supervisor.close(); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1);
  });
  it.each(["abort", "exit", "close"])("releases a binding returned after %s during asynchronous preparation", async action => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools }), abort = new AbortController();
    let release!: (value: { binding: ApplicationToolBinding; tools: DynamicToolSpec[] }) => void;
    applicationTools.prepareTurn.mockImplementation(() => new Promise(resolve => { release = resolve; }));
    const acquiring = supervisor.acquire("w1", envelope(), abort.signal);
    const rejected = expect(acquiring).rejects.toThrow();
    await vi.waitFor(() => expect(release).toBeTypeOf("function"));
    if (action === "abort") abort.abort();
    if (action === "exit") host.exit({ code: 1, signal: null });
    if (action === "close") await supervisor.close();
    release({ binding, tools }); await rejected;
    expect(host.calls).toEqual([]); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1); await supervisor.close();
  });

  it.each(["turn/completed", "serverRequest/resolved"])("cancels the exact observed child invocation on %s without a second resolution", async method => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    let deliver!: (value: ApplicationToolResult) => void;
    applicationTools.call.mockImplementation(() => new Promise(resolve => { deliver = resolve; }));
    const worker = await supervisor.acquire("w1", envelope());
    host.notify("thread/started", { thread: { id: "child", parentThreadId: "thread-1", status: { type: "active" } } });
    host.notify("turn/started", { threadId: "child", turn: { id: "child-turn" } });
    const answer = host.ask(request({ threadId: "child", turnId: "child-turn", callId: "child-call" }, "child-rpc"));
    await vi.waitFor(() => expect(deliver).toBeTypeOf("function"));
    // A different actor cannot resolve the child's JSON-RPC request.
    host.notify("serverRequest/resolved", { threadId: "thread-1", requestId: "child-rpc" });
    expect(applicationTools.cancelCall).not.toHaveBeenCalled();
    host.notify(method, method === "turn/completed" ? { threadId: "child", turn: { id: "child-turn", status: "completed" } } : { threadId: "child", requestId: "child-rpc" });
    expect(await answer).toMatchObject({ result: { success: false } });
    expect(applicationTools.cancelCall).toHaveBeenCalledWith(applicationTools.call.mock.calls[0]![0], "provider call cancelled");
    expect(applicationTools.cancelCall).toHaveBeenCalledTimes(1);
    deliver(result); await Promise.resolve();
    const events = await supervisor.drainTurnProgress(worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "request-resolved")).toEqual([expect.objectContaining({ providerThreadId: "child", providerTurnId: "child-turn", requestId: "child-rpc", outcome: "cancelled" })]);
    expect(applicationTools.finishTurn).not.toHaveBeenCalled();
    await supervisor.close();
  });

  it("interrupts during turn/start without prematurely settling the primary lifecycle", async () => {
    const host = fakeHost(), applicationTools = registry(), supervisor = new CodexSupervisor({ host, applicationTools });
    let release!: (value: unknown) => void;
    host.respond("turn/start", () => new Promise(resolve => { release = resolve; }));
    const acquiring = supervisor.acquire("w1", envelope()); await vi.waitFor(() => expect(release).toBeTypeOf("function"));
    const [handle] = await supervisor.inventory();
    const interrupted = supervisor.interrupt(handle!.workerId, handle!.generation);
    expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1);
    release({ turn: { id: "turn-1", status: "inProgress" } });
    const worker = await acquiring;
    expect(worker.state).toBe("running");
    await vi.waitFor(() => expect(host.calls.some(call => call.method === "turn/interrupt")).toBe(true));
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "interrupted" } });
    await interrupted;
    expect(await supervisor.wait(worker.workerId, worker.generation)).toMatchObject({ signal: "SIGTERM" });
    await supervisor.close(); expect(applicationTools.finishTurn).toHaveBeenCalledTimes(1);
  });

  it.each(["resolved", "exit", "interrupt", "abort", "retire", "close"])("never dispatches a call cancelled by %s before primary adoption (real registry)", async action => {
    let catalog: ApplicationToolCatalog | undefined;
    const applicationTools = new ApplicationToolRegistry({ sessions: {
      get: async () => ({ status: "idle" } as RuntimeSessionRecord),
      getApplicationToolCatalog: async () => catalog,
      registerApplicationToolCatalog: async (_projectId, _sessionId, value) => { catalog = structuredClone(value); return structuredClone(value); }
    } });
    const registered = await applicationTools.register("project", "session", { applicationId: "application", workspaceId: "workspace", workspaceGeneration: "g1", timeoutMs: 1000, tools });
    const call = vi.spyOn(applicationTools, "call");
    const host = fakeHost(), supervisor = new CodexSupervisor({ host, applicationTools }), abort = new AbortController();
    let release!: (value: unknown) => void;
    host.respond("turn/start", () => new Promise(resolve => { release = resolve; }));
    const acquiring = supervisor.acquire("w1", envelope(), abort.signal);
    await vi.waitFor(() => expect(release).toBeTypeOf("function"));
    const [handle] = await supervisor.inventory();
    const answer = host.ask(request());
    let interrupted: Promise<void> | undefined;
    if (action === "resolved") host.notify("serverRequest/resolved", { threadId: "thread-1", requestId: 42 });
    if (action === "exit") host.exit({ code: 1, signal: null });
    if (action === "interrupt") interrupted = supervisor.interrupt(handle!.workerId, handle!.generation);
    if (action === "abort") abort.abort();
    if (action === "retire") await supervisor.retire(handle!.workerId, handle!.generation);
    if (action === "close") await supervisor.close();
    // Cancellation resolves before turn/start does; the registry has no work.
    expect(await answer).toMatchObject({ result: { success: false } });
    expect(applicationTools.listCalls("project", "session", registered.bindingId)).toEqual([]);
    expect(call).not.toHaveBeenCalled();
    release({ turn: { id: "turn-1", status: "inProgress" } });
    const worker = await acquiring;
    await Promise.resolve();
    expect(call).not.toHaveBeenCalled();
    expect(applicationTools.listCalls("project", "session", registered.bindingId)).toEqual([]);
    if (action !== "retire" && action !== "close") {
      const events = await supervisor.drainTurnProgress(worker.workerId, worker.generation);
      expect(events.filter(event => event.type === "request-resolved")).toEqual([expect.objectContaining({ requestId: "42", providerThreadId: "thread-1", providerTurnId: "turn-1", outcome: "cancelled" })]);
    }
    complete(host);
    await interrupted;
    await supervisor.close(); applicationTools.close();
  });

});
