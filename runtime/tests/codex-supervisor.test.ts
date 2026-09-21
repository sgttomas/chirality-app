import { describe, expect, it, vi } from "vitest";
import type { DelegatedTurnProgressEvent } from "@chirality/runtime-contracts";
import type { CodexTurnEnvelope } from "@chirality/runtime-core";
import { CodexSupervisor, INSTRUCTION_UNLOAD_TIMEOUT_MS, type CodexSupervisorHost } from "../packages/daemon/src/codex-supervisor.js";
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
const drain = async (supervisor: CodexSupervisor, workerId: string, generation: string): Promise<DelegatedTurnProgressEvent[]> => [...await supervisor.drainTurnProgress(workerId, generation)];

describe("Codex supervisor over the shared app-server", () => {
  it("starts a thread, applies the collaboration mode once, starts the turn and assembles text from deltas plus the completed message", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("w1", envelope({ developerInstructions: "# Chirality role: agent1", model: "gpt-5-codex", reasoningEffort: "high" }));
    expect(host.calls.map(call => call.method)).toEqual(["thread/start", "thread/settings/update", "turn/start"]);
    expect(host.calls[0]!.params).toMatchObject({ cwd: "/tmp/project", developerInstructions: "# Chirality role: agent1", approvalPolicy: "on-request", sandbox: "workspace-write", model: "gpt-5-codex", ephemeral: false, serviceName: "chirality" });
    expect(host.calls[0]!.params).not.toHaveProperty("baseInstructions");
    expect(host.calls[1]!.params).toEqual({ threadId: "thread-1", collaborationMode: { mode: "default", settings: { model: "gpt-5-codex", reasoning_effort: "high", developer_instructions: null } } });
    expect(host.calls[2]!.params).toEqual({ threadId: "thread-1", input: [{ type: "text", text: "hello" }], model: "gpt-5-codex", effort: "high" });
    expect(await drain(supervisor, worker.workerId, worker.generation)).toEqual([{ type: "started", providerThreadId: "thread-1", providerTurnId: "turn-1" }]);
    host.notify("turn/started", { threadId: "thread-1", turn: { id: "turn-1", status: "inProgress" } });
    host.notify("item/agentMessage/delta", { threadId: "thread-1", turnId: "turn-1", itemId: "m1", delta: "Hel" });
    host.notify("item/reasoning/textDelta", { threadId: "thread-1", turnId: "turn-1", itemId: "r1", delta: "thinking" });
    host.notify("item/completed", { threadId: "thread-1", turnId: "turn-1", item: { type: "agentMessage", id: "m1", text: "Hello there" } });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "completed", error: null } });
    const events = await drain(supervisor, worker.workerId, worker.generation);
    expect(events.map(event => event.type)).toEqual(["notification", "notification", "text", "notification", "notification", "text", "notification"]);
    expect(events.filter(event => event.type === "notification").map(event => (event as { method: string }).method)).toEqual(["turn/started", "item/agentMessage/delta", "item/reasoning/textDelta", "item/completed", "turn/completed"]);
    expect(events.filter(event => event.type === "text").map(event => (event as { text: string }).text)).toEqual(["Hel", "lo there"]);
    await expect(supervisor.wait(worker.workerId, worker.generation)).resolves.toMatchObject({ exitCode: 0, signal: null, threadId: "thread-1", stdout: "Hello there" });
    await supervisor.retire(worker.workerId, worker.generation);
    expect(await supervisor.inventory()).toEqual([]);

    // The same thread, same mode and same policy: no settings update and no policy resend.
    const second = await supervisor.acquire("w2", envelope({ resumeThreadId: "thread-1", clientTurnId: "turn-b", developerInstructions: "# Chirality role: agent1" }));
    expect(host.calls.slice(3).map(call => call.method)).toEqual(["turn/start"]);
    expect(host.calls[3]!.params).toEqual({ threadId: "thread-1", input: [{ type: "text", text: "hello" }] });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-2", status: "completed" } });
    await supervisor.wait(second.workerId, second.generation);
    await supervisor.retire(second.workerId, second.generation);

    // A policy change travels on turn/start; a mode change updates the thread settings.
    const third = await supervisor.acquire("w3", envelope({ resumeThreadId: "thread-1", clientTurnId: "turn-c", developerInstructions: "# Chirality role: agent1", interactionMode: "native-plan", policy: { approvalPolicy: "never", sandbox: "read-only" } }));
    expect(host.calls.slice(4).map(call => call.method)).toEqual(["thread/settings/update", "turn/start"]);
    expect(host.calls[4]!.params).toMatchObject({ collaborationMode: { mode: "plan" } });
    expect(host.calls[5]!.params).toMatchObject({ approvalPolicy: "never", sandboxPolicy: { type: "readOnly", networkAccess: false } });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-3", status: "completed" } });
    await supervisor.wait(third.workerId, third.generation);
    await supervisor.close();
  });

  it("resumes an unknown thread after the app-server restarted and fails live turns when the child exits", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const first = await supervisor.acquire("w1", envelope());
    host.exit({ code: 1, signal: null });
    const failed = await supervisor.wait(first.workerId, first.generation);
    expect(failed).toMatchObject({ exitCode: 1, stderr: expect.stringContaining("exited during the turn") });
    const progress = await drain(supervisor, first.workerId, first.generation);
    expect(progress.at(-1)).toMatchObject({ type: "notification", method: "chirality/appServer/exited" });
    await supervisor.retire(first.workerId, first.generation);
    host.restart();
    await supervisor.acquire("w2", envelope({ resumeThreadId: "thread-1", clientTurnId: "turn-b" }));
    expect(host.calls.slice(3).map(call => call.method)).toEqual(["thread/loaded/list", "thread/resume", "thread/inject_items", "thread/settings/update", "turn/start"]);
    expect(host.calls[4]!.params).toMatchObject({ threadId: "thread-1", cwd: "/tmp/project", approvalPolicy: "on-request", sandbox: "workspace-write" });
    await supervisor.close();
  });

  it("answers every server request kind: pending approvals, user input, elicitation, immediate dynamic tool refusal and visible unsupported outcomes", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("w1", envelope());
    await drain(supervisor, worker.workerId, worker.generation);
    const approval = host.ask({ id: 7, method: "item/commandExecution/requestApproval", params: { threadId: "thread-1", turnId: "turn-1", itemId: "cmd-1", command: "ls" } });
    const patch = host.ask({ id: 8, method: "applyPatchApproval", params: { conversationId: "thread-1", callId: "call-1", fileChanges: {} } });
    const permissions = host.ask({ id: 9, method: "item/permissions/requestApproval", params: { threadId: "thread-1", turnId: "turn-1", itemId: "perm-1", cwd: "/tmp/project", reason: "x", permissions: { network: { enabled: true } } } });
    const input = host.ask({ id: 10, method: "item/tool/requestUserInput", params: { threadId: "thread-1", turnId: "turn-1", itemId: "ask-1", questions: [{ id: "q1", header: "H", question: "Q?", isOther: false, isSecret: false, options: null }], isBlocking: true, autoResolutionMs: null } });
    const elicitation = host.ask({ id: 11, method: "mcpServer/elicitation/request", params: { threadId: "thread-1", turnId: "turn-1", serverName: "srv", mode: "form" } });
    await expect(host.ask({ id: 12, method: "item/tool/call", params: { threadId: "thread-1", turnId: "turn-1", callId: "c1", tool: "x", arguments: {} } })).resolves.toEqual({ result: { success: false, contentItems: [{ type: "inputText", text: "Chirality registers no dynamic tools" }] } });
    await expect(host.ask({ id: 13, method: "account/chatgptAuthTokens/refresh", params: { threadId: "thread-1" } })).resolves.toEqual({ error: { code: -32601, message: "unsupported request" } });
    await expect(host.ask({ id: 14, method: "attestation/generate", params: {} })).resolves.toEqual({ error: { code: -32601, message: "unsupported request" } });
    await expect(host.ask({ id: 15, method: "future/unknown", params: { threadId: "thread-1" } })).resolves.toEqual({ error: { code: -32601, message: "unsupported request" } });
    const pending = await supervisor.pendingRequests(worker.workerId, worker.generation);
    expect(pending.map(request => [request.requestId, request.method, request.itemId])).toEqual([["7", "item/commandExecution/requestApproval", "cmd-1"], ["8", "applyPatchApproval", "call-1"], ["9", "item/permissions/requestApproval", "perm-1"], ["10", "item/tool/requestUserInput", "ask-1"], ["11", "mcpServer/elicitation/request", undefined]]);
    const events = await drain(supervisor, worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "request").map(event => (event as { method: string }).method)).toEqual(["item/commandExecution/requestApproval", "applyPatchApproval", "item/permissions/requestApproval", "item/tool/requestUserInput", "mcpServer/elicitation/request", "item/tool/call", "account/chatgptAuthTokens/refresh", "future/unknown"]);
    expect(events.filter(event => event.type === "request-resolved").map(event => [(event as { requestId: string }).requestId, (event as { outcome: string }).outcome])).toEqual([["12", "answered"], ["13", "unsupported"], ["15", "unsupported"]]);

    await expect(supervisor.answerRequest(worker.workerId, worker.generation, "7", { kind: "userInput", answers: {} })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await supervisor.answerRequest(worker.workerId, worker.generation, "7", { kind: "approval", verdict: "allowForSession" });
    await supervisor.answerRequest(worker.workerId, worker.generation, "8", { kind: "approval", verdict: "deny" });
    await supervisor.answerRequest(worker.workerId, worker.generation, "9", { kind: "approval", verdict: "allow" });
    await supervisor.answerRequest(worker.workerId, worker.generation, "10", { kind: "userInput", answers: { q1: { answers: ["yes"] } } });
    await supervisor.answerRequest(worker.workerId, worker.generation, "11", { kind: "elicitation", action: "decline" });
    await expect(approval).resolves.toEqual({ result: { decision: "acceptForSession" } });
    await expect(patch).resolves.toEqual({ result: { decision: { denied: { rejection: "Declined by the user in Chirality" } } } });
    await expect(permissions).resolves.toEqual({ result: { permissions: { network: { enabled: true } }, scope: "turn" } });
    await expect(input).resolves.toEqual({ result: { answers: { q1: { answers: ["yes"] } } } });
    await expect(elicitation).resolves.toEqual({ result: { action: "decline", content: null, _meta: null } });
    await expect(supervisor.answerRequest(worker.workerId, worker.generation, "7", { kind: "approval", verdict: "allow" })).rejects.toMatchObject({ code: "NOT_FOUND" });
    expect(await supervisor.pendingRequests(worker.workerId, worker.generation)).toEqual([]);
    const resolved = await drain(supervisor, worker.workerId, worker.generation);
    expect(resolved.map(event => [(event as { requestId: string }).requestId, (event as { outcome: string }).outcome, (event as { decidedBy: string }).decidedBy])).toEqual([["7", "answered", "user"], ["8", "answered", "user"], ["9", "answered", "user"], ["10", "answered", "user"], ["11", "answered", "user"]]);
    await supervisor.close();
  });

  it("cancels still-pending requests when the turn ends and when the supplier resolves them itself", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("w1", envelope());
    const approval = host.ask({ id: 1, method: "item/fileChange/requestApproval", params: { threadId: "thread-1", turnId: "turn-1", itemId: "f1" } });
    const legacy = host.ask({ id: 2, method: "execCommandApproval", params: { conversationId: "thread-1", callId: "c2", command: ["ls"], cwd: "/tmp/project" } });
    const supplierResolved = host.ask({ id: 3, method: "item/tool/requestUserInput", params: { threadId: "thread-1", turnId: "turn-1", itemId: "ask", questions: [], isBlocking: false, autoResolutionMs: 10 } });
    host.notify("serverRequest/resolved", { threadId: "thread-1", requestId: 3 });
    await expect(supplierResolved).resolves.toEqual({ result: { answers: {} } });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "failed", error: { message: "boom" } } });
    await expect(approval).resolves.toEqual({ result: { decision: "cancel" } });
    await expect(legacy).resolves.toEqual({ result: { decision: "abort" } });
    await expect(supervisor.wait(worker.workerId, worker.generation)).resolves.toMatchObject({ exitCode: 1, stderr: "boom" });
    const events = await drain(supervisor, worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "request-resolved").map(event => [(event as { requestId: string }).requestId, (event as { outcome: string }).outcome, (event as { decidedBy: string }).decidedBy])).toEqual([["3", "cancelled", "runtime"], ["1", "cancelled", "runtime"], ["2", "cancelled", "runtime"]]);
    await supervisor.close();
  });

  it("interrupts through turn/interrupt without retiring, memoizes retirement per generation and rejects stale generations", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("w1", envelope());
    const interrupting = supervisor.interrupt(worker.workerId, worker.generation);
    await new Promise(resolve => setTimeout(resolve, 1));
    expect(host.calls.at(-1)).toEqual({ method: "turn/interrupt", params: { threadId: "thread-1", turnId: "turn-1" } });
    expect((await supervisor.inventory()).map(handle => handle.workerId)).toEqual(["w1"]);
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "interrupted" } });
    await interrupting;
    await expect(supervisor.wait(worker.workerId, worker.generation)).resolves.toMatchObject({ exitCode: null, signal: "SIGTERM", threadId: "thread-1" });
    expect((await supervisor.inventory()).map(handle => handle.state)).toEqual(["exited"]);
    await supervisor.interrupt(worker.workerId, worker.generation);
    const first = supervisor.retire(worker.workerId, worker.generation);
    const second = supervisor.retire(worker.workerId, worker.generation);
    expect(second).toBe(first);
    await first;
    expect(await supervisor.inventory()).toEqual([]);
    await expect(supervisor.retire(worker.workerId, "stale")).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", message: "unknown or stale worker generation" });
    await expect(supervisor.wait(worker.workerId, worker.generation)).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
    await expect(supervisor.retire(worker.workerId, worker.generation)).resolves.toBeUndefined();
    await expect(supervisor.acquire("w1", "not json")).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await supervisor.close();
    await expect(supervisor.acquire("w9", envelope())).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
  });

  it("waits for the turn identity when Stop arrives during the turn/start round trip", async () => {
    const host = fakeHost();
    let releaseStart!: () => void;
    const started = new Promise<void>(resolve => { releaseStart = resolve; });
    const original = host.request.bind(host);
    host.request = (async (method: string, params: unknown) => { if (method === "turn/start") await started; return original(method, params); }) as typeof host.request;
    const supervisor = new CodexSupervisor({ host });
    const acquiring = supervisor.acquire("w1", envelope());
    await new Promise(resolve => setTimeout(resolve, 1));
    const handles = await supervisor.inventory();
    expect(handles.map(handle => handle.workerId)).toEqual(["w1"]);
    const interrupting = supervisor.interrupt("w1", handles[0]!.generation);
    await new Promise(resolve => setTimeout(resolve, 1));
    expect(host.calls.some(call => call.method === "turn/interrupt")).toBe(false);
    releaseStart();
    const worker = await acquiring;
    await new Promise(resolve => setTimeout(resolve, 1));
    expect(host.calls.at(-1)).toEqual({ method: "turn/interrupt", params: { threadId: "thread-1", turnId: "turn-1" } });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "interrupted" } });
    await interrupting;
    await expect(supervisor.wait(worker.workerId, worker.generation)).resolves.toMatchObject({ signal: "SIGTERM" });
  });

  it("captures native plan items and clarifications for plan-mode turns and routes child-thread notifications to the parent turn", async () => {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("w1", envelope({ interactionMode: "native-plan" }));
    host.notify("thread/started", { thread: { id: "thread-child", parentThreadId: "thread-1" } });
    host.notify("item/completed", { threadId: "thread-child", turnId: "turn-x", item: { type: "agentMessage", id: "child-m", text: "child text" } });
    host.notify("item/completed", { threadId: "thread-1", turnId: "turn-1", item: { type: "plan", id: "plan-1", text: "1. do" } });
    const clarification = host.ask({ id: 5, method: "item/tool/requestUserInput", params: { threadId: "thread-1", turnId: "turn-1", itemId: "ask-1", questions: [{ id: "q1", header: "Scope", question: "Which?", isOther: true, isSecret: false, options: [{ label: "A", description: "a" }] }], isBlocking: true, autoResolutionMs: null } });
    const events = await drain(supervisor, worker.workerId, worker.generation);
    expect(events.filter(event => event.type === "notification").map(event => (event as { method: string; params: any }).method)).toEqual(["thread/started", "item/completed", "item/completed"]);
    expect(events.some(event => event.type === "text")).toBe(false);
    expect(await supervisor.drainNativePlanEvents(worker.workerId, worker.generation)).toEqual([expect.objectContaining({ projectId: "project", sessionId: "session", clientTurnId: "turn-a", providerThreadId: "thread-1", providerTurnId: "turn-1", eventId: "plan-1", plan: "1. do" })]);
    expect(await supervisor.drainNativePlanEvents(worker.workerId, worker.generation)).toEqual([]);
    expect(await supervisor.pendingNativePlanClarifications(worker.workerId, worker.generation)).toEqual([expect.objectContaining({ requestId: "5", itemId: "ask-1", isBlocking: true, autoResolutionMs: null, questions: [{ id: "q1", header: "Scope", question: "Which?", options: [{ label: "A", description: "a" }], isOther: true, isSecret: false }] })]);
    await supervisor.replyNativePlanClarification(worker.workerId, worker.generation, "5", { q1: { answers: ["A"] } });
    await expect(clarification).resolves.toEqual({ result: { answers: { q1: { answers: ["A"] } } } });
    expect(await supervisor.pendingNativePlanClarifications(worker.workerId, worker.generation)).toEqual([]);
    await supervisor.close();
  });
});


describe("safe developer instruction adoption", () => {
  async function prepared(timeout = 10) {
    const host = fakeHost();
    const supervisor = new CodexSupervisor({ host, instructionUnloadTimeoutMs: timeout });
    const worker = await supervisor.acquire("first", envelope({ developerInstructions: "old" }));
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "completed" } });
    await supervisor.retire(worker.workerId, worker.generation);
    host.respond("thread/loaded/list", () => ({ data: ["thread-1"], nextCursor: null }));
    host.respond("thread/read", () => ({ thread: { parentThreadId: null, status: { type: "idle" } } }));
    host.respond("thread/unsubscribe", () => ({ status: "unsubscribed" }));
    return { host, supervisor };
  }
  it("waits for actual closure, holds thread ownership, and resumes with new guidance and additive role config", async () => {
    const { host, supervisor } = await prepared(1000);
    const config = { "agents.TASK.config_file": "/tmp/TASK-abc.toml", "agents.TASK.description": "Task" };
    const next = supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new", nativeRoleConfig: config, interactionMode: "native-plan" }));
    await new Promise(resolve => setTimeout(resolve, 1));
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    expect(host.calls.some(call => call.method === "thread/resume")).toBe(false);
    await expect(supervisor.acquire("racer", envelope({ resumeThreadId: "thread-1", developerInstructions: "old" }))).rejects.toThrow(/adoption/);
    host.notify("thread/closed", { threadId: "thread-1" });
    const worker = await next;
    const resume = host.calls.find(call => call.method === "thread/resume")!;
    expect(resume.params).toMatchObject({ threadId: "thread-1", developerInstructions: "new", config });
    expect(resume.params).not.toHaveProperty("baseInstructions");
    expect(host.calls.at(-1)!.params.input).toEqual([{ type: "text", text: "hello" }]);
    expect(host.calls.at(-2)!.params.collaborationMode.mode).toBe("plan");
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-2", status: "completed" } });
    await supervisor.retire(worker.workerId, worker.generation);
    await supervisor.close();
  });
  it.each(["delayed", "failed", "notSubscribed"])("leaves %s unload pending without a hot resume or new turn", async mode => {
    const { host, supervisor } = await prepared();
    if (mode === "failed") host.fail("thread/unsubscribe", new Error("unload failed"));
    if (mode === "notSubscribed") host.respond("thread/unsubscribe", () => ({ status: "notSubscribed" }));
    await expect(supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }))).rejects.toMatchObject({ details: { reason: "INSTRUCTION_ADOPTION_PENDING" } });
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    expect(host.calls.some(call => call.method === "thread/resume")).toBe(false);
    // Reverting the prose cannot silently reuse an unsubscribed cached thread.
    await expect(supervisor.acquire("retry", envelope({ resumeThreadId: "thread-1", developerInstructions: "old" }))).rejects.toThrow(/pending/);
    await supervisor.close();
  });
  it("defers for an active grandchild after the primary retires without interrupting it", async () => {
    const { host, supervisor } = await prepared();
    host.respond("thread/loaded/list", () => ({ data: ["thread-1", "child", "grandchild"], nextCursor: null }));
    host.respond("thread/read", params => ({ thread: { parentThreadId: params.threadId === "child" ? "thread-1" : params.threadId === "grandchild" ? "child" : null, status: { type: params.threadId === "grandchild" ? "active" : "idle" } } }));
    await expect(supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }))).rejects.toThrow(/descendant is active/);
    expect(host.calls.some(call => ["thread/unsubscribe", "thread/resume", "thread/inject_items", "turn/interrupt"].includes(call.method))).toBe(false);
    await supervisor.close();
  });
  it.each([false, true])("checks every loaded-list page after a missed closed notification (still loaded: %s)", async stillLoaded => {
    const { host, supervisor } = await prepared();
    host.respond("thread/unsubscribe", () => {
      host.respond("thread/loaded/list", params => params.cursor === "next" ? { data: stillLoaded ? ["thread-1"] : [], nextCursor: null } : { data: ["other"], nextCursor: "next" });
      return { status: "unsubscribed" };
    });
    const next = supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }));
    if (stillLoaded) {
      await expect(next).rejects.toMatchObject({ code: "INSTRUCTION_ADOPTION_PENDING" });
      expect(host.calls.some(call => call.method === "thread/resume")).toBe(false);
      expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    } else {
      await next;
      expect(host.calls.find(call => call.method === "thread/resume")?.params).toMatchObject({ threadId: "thread-1", developerInstructions: "new" });
    }
    expect(host.calls.some(call => call.method === "thread/loaded/list" && call.params.cursor === "next")).toBe(true);
    await supervisor.close();
  });
  it("retains an active primary without unsubscribing or interrupting it", async () => {
    const { host, supervisor } = await prepared();
    host.respond("thread/read", () => ({ thread: { parentThreadId: null, status: { type: "active" } } }));
    await expect(supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }))).rejects.toMatchObject({ code: "INSTRUCTION_ADOPTION_PENDING" });
    expect(host.calls.some(call => ["thread/unsubscribe", "thread/resume", "thread/inject_items", "turn/interrupt"].includes(call.method))).toBe(false);
    await supervisor.close();
  });
  it("waits through the supplier ten-second shutdown allowance plus scheduling margin", async () => {
    vi.useFakeTimers();
    try {
      expect(INSTRUCTION_UNLOAD_TIMEOUT_MS).toBe(12_000);
      const { host, supervisor: previous } = await prepared();
      await previous.close();
      const supervisor = new CodexSupervisor({ host });
      const next = supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }));
      await vi.advanceTimersByTimeAsync(11_000);
      expect(host.calls.some(call => call.method === "thread/resume")).toBe(false);
      expect(host.calls.filter(call => call.method === "thread/loaded/list")).toHaveLength(1);
      host.notify("thread/closed", { threadId: "thread-1" });
      await next;
      expect(host.calls.some(call => call.method === "thread/resume")).toBe(true);
      await supervisor.close();
    } finally { vi.useRealTimers(); }
  });
  it.each(["failed", "lost-ack", "invalid-ack"])("does not latch config-only adoption after %s injection, then safely retries and reuses unchanged guidance", async failure => {
    const { host, supervisor } = await prepared();
    const history = ["OLD AMBER"];
    let configured = "OLD AMBER";
    host.respond("thread/unsubscribe", () => { host.notify("thread/closed", { threadId: "thread-1" }); return { status: "unsubscribed" }; });
    host.respond("thread/resume", params => { configured = params.developerInstructions; return { thread: { id: params.threadId, status: { type: "idle" } }, model: "gpt-5-codex" }; });
    const append = (params: any) => { expect(params.items).toHaveLength(1); expect(params.items[0]).toMatchObject({ type: "message", role: "developer", content: [{ type: "input_text" }] }); history.push(params.items[0].content[0].text); };
    host.respond("thread/inject_items", params => {
      if (failure !== "failed") append(params);
      if (failure === "invalid-ack") return null;
      throw new Error(failure);
    });
    await expect(supervisor.acquire("failed", envelope({ resumeThreadId: "thread-1", developerInstructions: "NEW COPPER" }))).rejects.toMatchObject({ code: "INSTRUCTION_ADOPTION_PENDING", details: { stage: "developer-history-injection" } });
    expect(configured).toBe("NEW COPPER");
    expect(history[0]).toBe("OLD AMBER");
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    expect(await supervisor.inventory()).toEqual([]);
    host.respond("thread/inject_items", params => { append(params); return {}; });
    const retry = await supervisor.acquire("retry", envelope({ resumeThreadId: "thread-1", developerInstructions: "NEW COPPER" }));
    expect(host.calls.filter(call => call.method === "thread/resume")).toHaveLength(2);
    expect(host.calls.filter(call => call.method === "thread/inject_items")).toHaveLength(2);
    expect(history.at(-1)).toContain("supersedes earlier Chirality-provided");
    expect(history.at(-1)).toMatch(/NEW COPPER$/);
    const progress = await supervisor.drainTurnProgress(retry.workerId, retry.generation);
    expect(progress[0]).toMatchObject({ type: "started", instructionHistoryInjection: { method: "thread/inject_items", text: history.at(-1), sha256: expect.stringMatching(/^[a-f0-9]{64}$/) } });
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-2", status: "completed" } });
    await supervisor.retire(retry.workerId, retry.generation);
    const unchanged = await supervisor.acquire("unchanged", envelope({ resumeThreadId: "thread-1", developerInstructions: "NEW COPPER" }));
    expect(host.calls.filter(call => call.method === "thread/inject_items")).toHaveLength(2);
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-3", status: "completed" } });
    await supervisor.retire(unchanged.workerId, unchanged.generation);
    host.restart();
    await supervisor.acquire("restarted", envelope({ resumeThreadId: "thread-1", developerInstructions: "NEW COPPER" }));
    expect(host.calls.filter(call => call.method === "thread/inject_items")).toHaveLength(3);
    expect(history.at(-1)).toMatch(/NEW COPPER$/);
    await supervisor.close();
  });
  it("holds the user turn and competing acquisition until injection is acknowledged", async () => {
    const { host, supervisor } = await prepared();
    host.respond("thread/unsubscribe", () => { host.notify("thread/closed", { threadId: "thread-1" }); return { status: "unsubscribed" }; });
    let acknowledge!: (value: unknown) => void;
    host.respond("thread/inject_items", () => new Promise(resolve => { acknowledge = resolve; }));
    const next = supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }));
    await new Promise(resolve => setTimeout(resolve, 1));
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    await expect(supervisor.acquire("racer", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }))).rejects.toThrow(/adoption/);
    acknowledge({});
    await next;
    const methods = host.calls.map(call => call.method);
    expect(methods.lastIndexOf("thread/resume")).toBeLessThan(methods.lastIndexOf("thread/inject_items"));
    expect(methods.lastIndexOf("thread/inject_items")).toBeLessThan(methods.lastIndexOf("turn/start"));
    await supervisor.close();
  });
  it("never injects into a resume whose returned status is active", async () => {
    const { host, supervisor } = await prepared();
    host.respond("thread/unsubscribe", () => { host.notify("thread/closed", { threadId: "thread-1" }); return { status: "unsubscribed" }; });
    host.respond("thread/resume", () => ({ thread: { id: "thread-1", status: { type: "active" } }, model: "gpt-5-codex" }));
    await expect(supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }))).rejects.toMatchObject({ code: "INSTRUCTION_ADOPTION_PENDING" });
    expect(host.calls.some(call => call.method === "thread/inject_items")).toBe(false);
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    await supervisor.close();
  });
  it("honors Stop while waiting for unload without starting another turn", async () => {
    const { host, supervisor } = await prepared(1000);
    const controller = new AbortController();
    const next = supervisor.acquire("next", envelope({ resumeThreadId: "thread-1", developerInstructions: "new" }), controller.signal);
    await new Promise(resolve => setTimeout(resolve, 1));
    controller.abort(new Error("user stopped"));
    await expect(next).rejects.toThrow("user stopped");
    host.notify("thread/closed", { threadId: "thread-1" });
    expect(host.calls.filter(call => call.method === "turn/start")).toHaveLength(1);
    expect(host.calls.some(call => call.method === "thread/resume")).toBe(false);
    await supervisor.close();
  });
  it("rejects the retired user-text instruction shortcut", async () => {
    const supervisor = new CodexSupervisor({ host: fakeHost() });
    await expect(supervisor.acquire("next", envelope({ contextUpdate: "new instructions" }))).rejects.toThrow(/retired/);
    await supervisor.close();
  });
});

describe("native steering and descendant evidence", () => {
  it("checks Runtime/provider ownership, sends the pinned request, and distinguishes rejection from uncertain acknowledgment", async () => {
    const host = fakeHost(); const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("steer-worker", envelope());
    const input = { operationId: "steer-1", expectedTurnId: "turn-a", text: "Adjust the plan" };
    host.respond("turn/steer", () => ({ turnId: "turn-1" }));
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, { ...input, expectedTurnId: "stale" })).toMatchObject({ status: "rejected" });
    expect(host.calls.filter(call => call.method === "turn/steer")).toHaveLength(0);
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "accepted", providerTurnId: "turn-1" });
    expect(host.calls.at(-1)).toEqual({ method: "turn/steer", params: { threadId: "thread-1", expectedTurnId: "turn-1", clientUserMessageId: "steer-1", input: [{ type: "text", text: "Adjust the plan", text_elements: [] }] } });
    const { RuntimeError } = await import("@chirality/runtime-contracts");
    host.fail("turn/steer", new RuntimeError("ENGINE_UNAVAILABLE", "no active turn to steer", 503, { jsonRpcCode: -32600 }));
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "rejected" });
    host.fail("turn/steer", new RuntimeError("ENGINE_UNAVAILABLE", "internal failure", 503, { jsonRpcCode: -32603 }));
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "unknown" });
    host.fail("turn/steer", new Error("response lost"));
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "unknown" });
    host.respond("turn/steer", () => ({ turnId: "wrong-native-turn" }));
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "unknown" });
    host.restart();
    expect(await supervisor.steerTurn(worker.workerId, worker.generation, input)).toMatchObject({ status: "rejected" });
    await supervisor.close();
  });
  it("resolves descendant questions and records an explicit observation limit for active children at parent completion", async () => {
    const host = fakeHost(); const supervisor = new CodexSupervisor({ host });
    const worker = await supervisor.acquire("child-worker", envelope());
    host.notify("thread/started", { thread: { id: "child", parentThreadId: "thread-1", status: { type: "active", activeFlags: ["waitingOnUserInput"] } } });
    const question = host.ask({ id: 501, method: "item/tool/requestUserInput", params: { threadId: "child", turnId: "child-turn", itemId: "q", questions: [], isBlocking: false } });
    await Promise.resolve();
    expect(await supervisor.pendingRequests(worker.workerId, worker.generation)).toHaveLength(1);
    host.notify("serverRequest/resolved", { threadId: "child", requestId: 501 });
    await question;
    expect(await supervisor.pendingRequests(worker.workerId, worker.generation)).toHaveLength(0);
    host.notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "completed" } });
    const progress = await drain(supervisor, worker.workerId, worker.generation);
    expect(progress).toContainEqual(expect.objectContaining({ type: "notification", method: "chirality/nativeChildren/observationEnded", params: expect.objectContaining({ agentThreadIds: ["child"] }) }));
    expect(progress).toContainEqual(expect.objectContaining({ type: "request-resolved", requestId: "501" }));
    await supervisor.close();
  });
});
