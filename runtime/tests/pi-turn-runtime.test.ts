import { afterEach, beforeEach, expect, it } from "vitest";
import { mkdtemp, realpath, rm, writeFile, mkdir, symlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHash } from "node:crypto";
import { createPiTurnRuntime } from "../packages/engine-pi-omlx/src/pi-turn-runtime.js";
import { createPiReadTool } from "../packages/engine-pi-omlx/src/pi-read-tool.js";
import type { AgentEngineRunInput, ResolveSelectedContextResponse, RuntimeToolDefinition, UIEvent } from "@chirality/runtime-contracts";
let directory: string, root: string, transcript: string, input: AgentEngineRunInput;
beforeEach(async () => {
  directory = await realpath(await mkdtemp(join(tmpdir(), "pi-port-")));
  root = join(directory, "project"); transcript = join(directory, "control", "transcripts");
  await mkdir(root); await mkdir(transcript, { recursive: true, mode: 0o700 });
  input = { session: { sessionId: "fixture-session", projectRoot: root, persona: "TASK", mode: "WORK", agentType: 2, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() }, message: "Read the fixture if necessary and answer.", opts: { model: "fixture-model", tools: ["read_file"], maxTurns: 4, persona: "TASK", mode: "WORK" }, turnId: "fixture-turn" };
});
afterEach(async () => { await rm(directory, { recursive: true, force: true }); });
const answer = (content: string, model = "fixture-model") => new Response(JSON.stringify({ model, choices: [{ message: { role: "assistant", content }, finish_reason: "stop" }], usage: { prompt_tokens: 3, completion_tokens: 2 } }), { status: 200 });
function runtime(fetchImpl: typeof fetch, extra = {}) { return createPiTurnRuntime({ canonicalRoot: root, baseUrl: "http://127.0.0.1:12345/v1", model: { id: "fixture-model", contextWindow: 8192, maxTokens: 64 }, fetchImpl, ...extra }); }
async function run(port: ReturnType<typeof runtime>) { const events: UIEvent[] = []; for await (const event of port.startTurn(input, { credential: "synthetic-fixture-key", disableBuiltIns: true, disableAmbientResources: true, transcriptRoot: transcript })) events.push(event); return events; }
it("uses the actual isolated Pi SDK with strict local transport and canonical terminal events", async () => {
  const originalFetch = globalThis.fetch;
  let requests = 0;
  const port = runtime(async (url, init) => { requests++; expect(url).toBe("http://127.0.0.1:12345/v1/chat/completions"); expect(init?.redirect).toBe("manual"); const body = JSON.parse(String(init?.body)); expect(body.tools.map((t: any) => t.function.name)).toEqual(["read_file"]); expect(body.model).toBe("fixture-model"); return answer("PI_RUNTIME_OK"); });
  const events = await run(port);
  expect(events[0]).toMatchObject({ type: "session:init", data: { adapterId: "pi", providerId: "omlx", model: "fixture-model" } });
  expect(events).toContainEqual({ type: "chat:delta", data: { text: "PI_RUNTIME_OK" } });
  expect(events.at(-1)).toEqual({ type: "process:exit", data: { exitCode: 0 } });
  expect(events.filter(e => e.type === "process:exit")).toHaveLength(1);
  expect(requests).toBe(1);
  expect(globalThis.fetch).toBe(originalFetch);
});
it("executes only the real custom read tool through the Pi tool loop", async () => {
  await writeFile(join(root, "sample.txt"), "CANARY_READ_OK");
  let count = 0;
  const events = await run(runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    if (++count === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: null, tool_calls: [{ id: "call1", type: "function", function: { name: "read_file", arguments: '{"path":"sample.txt"}' } }] }, finish_reason: "tool_calls" }] }));
    expect(body.messages.some((m: any) => m.role === "tool" && m.content === "CANARY_READ_OK")).toBe(true);
    return answer("READ_COMPLETE");
  }));
  expect(events).toContainEqual({ type: "tool:result", data: { name: "read_file", ok: true } });
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
  expect(count).toBe(2);
});
it("does not load malicious project context or extensions", async () => {
  await writeFile(join(root, "AGENTS.md"), "AMBIENT_SECRET_MUST_NOT_APPEAR");
  await mkdir(join(root, ".pi", "extensions"), { recursive: true });
  await writeFile(join(root, ".pi", "extensions", "evil.ts"), "throw new Error('ambient extension executed');");
  const events = await run(runtime(async (_url, init) => { expect(String(init?.body)).not.toContain("AMBIENT_SECRET"); return answer("isolated"); }));
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
});
it("rejects redirects and model mismatch without exposing provider payloads", async () => {
  for (const response of [new Response("PRIVATE PROVIDER BODY", { status: 302, headers: { location: "https://outside.example" } }), answer("PRIVATE PROVIDER BODY", "wrong-model")]) {
    const events = await run(runtime(async () => response));
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
    expect(JSON.stringify(events)).not.toContain("PRIVATE PROVIDER BODY");
  }
});
it("rejects pilot/root violations before model calls", async () => {
  let calls = 0; const port = runtime(async () => { calls++; return answer("no"); });
  for (const changed of [{ ...input, session: { ...input.session, agentType: 1 } }, { ...input, opts: { ...input.opts, tools: ["bash"] } }, { ...input, session: { ...input.session, projectRoot: directory } }]) await expect(port.preflight(changed as AgentEngineRunInput, "fixture")).rejects.toThrow();
  expect(calls).toBe(0);
});
it("read tool rejects traversal, symlink escape, protected paths and oversized files", async () => {
  await writeFile(join(directory, "outside.txt"), "OUTSIDE");
  await writeFile(join(root, "private.txt"), "PRIVATE");
  await writeFile(join(root, "large.txt"), "x".repeat(20));
  await symlink(join(directory, "outside.txt"), join(root, "alias"));
  const tool = createPiReadTool({ canonicalRoot: root, name: "read_file", protectedPaths: [join(root, "private.txt")], maxBytes: 10 });
  for (const path of ["../outside.txt", "alias", "private.txt", "large.txt"]) await expect(tool.execute("test", { path }, undefined, undefined, {} as never)).rejects.toThrow();
});
it("interrupts a pending model request and emits one interrupted terminal", async () => {
  let entered!: () => void; const requested = new Promise<void>(resolve => { entered = resolve; });
  const port = runtime(async (_url, init) => { entered(); return new Promise<Response>((_resolve, reject) => init?.signal?.addEventListener("abort", () => reject(new Error("aborted")), { once: true })); });
  const pending = run(port);
  await requested; await port.interrupt(input.session.sessionId);
  const events = await pending;
  expect(events.at(-1)).toEqual({ type: "process:exit", data: { exitCode: 0, interrupted: true } });
  expect(events.filter(e => e.type === "process:exit")).toHaveLength(1);
});
it("bounds a provider ignoring AbortSignal and requires a fresh session after timeout", async () => {
  const port = runtime(async () => new Promise<Response>(() => {}), { turnTimeoutMs: 30 });
  const events = await run(port);
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
  expect(JSON.stringify(events)).toContain("deadline exceeded");
  await expect(port.preflight(input, "fixture")).rejects.toThrow("fresh Runtime session");
  input.session.sessionId = "fresh-session";
  await expect(port.preflight(input, "fixture")).resolves.toBeUndefined();
});
it("rejects unknown tools and output overflow through one canonical failed terminal", async () => {
  const tool = { id: "bad", type: "function", function: { name: "bash", arguments: '{"command":"no"}' } };
  const responses = [new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: null, tool_calls: [tool] }, finish_reason: "tool_calls" }] })), answer("x".repeat(3000))];
  for (const response of responses) { const events = await run(runtime(async () => response, { maxOutputBytes: 2048 })); expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } }); expect(events.filter(e => e.type === "process:exit")).toHaveLength(1); }
});
it("the legacy read alias still invokes the bounded custom tool, never Pi's builtin", async () => {
  input.opts.tools = ["read"];
  await writeFile(join(directory, "outside-secret.txt"), "OUTSIDE_SECRET");
  let calls = 0;
  const events = await run(runtime(async (_url, init) => {
    if (++calls === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: null, tool_calls: [{ id: "call1", type: "function", function: { name: "read", arguments: '{"path":"../outside-secret.txt"}' } }] }, finish_reason: "tool_calls" }] }));
    expect(String(init?.body)).not.toContain("OUTSIDE_SECRET");
    return answer("DENIAL_HANDLED");
  }));
  expect(events).toContainEqual({ type: "tool:result", data: { name: "read", ok: false } });
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
});
it("rejects a concurrent turn for the same session without disturbing the live request", async () => {
  let entered!: () => void; const requested = new Promise<void>(resolve => { entered = resolve; });
  const port = runtime(async (_url, init) => { entered(); return new Promise<Response>((_resolve, reject) => init?.signal?.addEventListener("abort", () => reject(new Error("aborted")), { once: true })); });
  const first = run(port); await requested;
  await expect(run(port)).rejects.toMatchObject({ type: "TURN_IN_PROGRESS" });
  await port.interrupt(input.session.sessionId);
  expect((await first).at(-1)).toMatchObject({ type: "process:exit", data: { interrupted: true } });
});
it("performs real SDK automatic compaction with tool-free bounded summarization and metadata-only events", async () => {
  input.message = "ORIGINAL_CONTEXT_MARKER " + "project context ".repeat(100);
  let modelCalls = 0, summaryCalls = 0;
  const events = await run(runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    modelCalls++;
    if (body.tools) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: "ANSWER_BEFORE_COMPACTION" }, finish_reason: "stop" }], usage: { prompt_tokens: 8190, completion_tokens: 8 } }));
    summaryCalls++;
    expect(body.max_tokens).toBeLessThanOrEqual(64);
    expect(JSON.stringify(body.messages)).toContain("ORIGINAL_CONTEXT_MARKER");
    return answer("PRIVATE_COMPACTION_SUMMARY");
  }, { compaction: { reserveTokens: 64, keepRecentTokens: 1 } }));
  expect(summaryCalls).toBeGreaterThan(0);
  expect(modelCalls).toBeGreaterThan(1);
  const compaction = events.filter(e => e.type === "harness:event");
  expect(compaction.some(e => e.type === "harness:event" && e.data.type === "context.compaction.started")).toBe(true);
  expect(compaction.some(e => e.type === "harness:event" && e.data.type === "context.compacted")).toBe(true);
  expect(compaction.every(e => e.type === "harness:event" && e.data.sessionId === input.session.sessionId && e.data.turnId === input.turnId)).toBe(true);
  expect(JSON.stringify(events)).not.toContain("PRIVATE_COMPACTION_SUMMARY");
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
});
it("rejects tools from a summarization response and records compaction failure without a false success", async () => {
  input.message = "context ".repeat(200);
  const events = await run(runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    if (body.tools) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: "answer" }, finish_reason: "stop" }], usage: { prompt_tokens: 8190, completion_tokens: 8 } }));
    return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: null, tool_calls: [{ id: "summary-tool", type: "function", function: { name: "read_file", arguments: '{"path":"secret"}' } }] }, finish_reason: "tool_calls" }] }));
  }, { compaction: { reserveTokens: 64, keepRecentTokens: 1 } }));
  expect(events.some(e => e.type === "harness:event" && e.data.type === "context.compaction.failed")).toBe(true);
  expect(events.some(e => e.type === "harness:event" && e.data.type === "context.compacted")).toBe(false);
  expect(events.some(e => e.type === "tool:result")).toBe(false);
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
});
it("accepts observed oMLX tool-call shape with absent content while dropping reasoning content", async () => {
  await writeFile(join(root, "fixture.txt"), "OBSERVED_TOOL_READ");
  let calls = 0;
  const events = await run(runtime(async (_url, init) => {
    if (++calls === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", reasoning_content: "PRIVATE_REASONING_NOT_FOR_PROJECTION", tool_calls: [{ id: "observed-call", type: "function", function: { name: "read_file", arguments: '{"path":"fixture.txt"}' } }] }, finish_reason: "tool_calls" }] }));
    expect(String(init?.body)).not.toContain("PRIVATE_REASONING");
    expect(String(init?.body)).toContain("OBSERVED_TOOL_READ");
    return answer("REAL_SHAPE_HANDLED");
  }));
  expect(events).toContainEqual({ type: "tool:result", data: { name: "read_file", ok: true } });
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
  expect(JSON.stringify(events)).not.toContain("PRIVATE_REASONING");
});

it("preserves real SDK conversation across turns and rejects changed account or scope", async () => {
  let calls = 0;
  const port = runtime(async (_url, init) => {
    const body = String(init?.body);
    if (++calls === 2) { expect(body).toContain("FIRST_USER_CONTEXT"); expect(body).toContain("FIRST_ASSISTANT_CONTEXT"); expect(body).toContain("SECOND_USER_CONTEXT"); }
    return answer(calls === 1 ? "FIRST_ASSISTANT_CONTEXT" : "SECOND_ANSWER");
  });
  input.message = "FIRST_USER_CONTEXT"; await run(port);
  input.message = "SECOND_USER_CONTEXT"; input.turnId = "second-turn";
  expect((await run(port)).at(-1)).toMatchObject({ data: { exitCode: 0 } });
  await expect(port.preflight(input, "different-account")).rejects.toThrow("context changed");
  input.session.briefHash = "changed-brief";
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("context changed");
  expect(calls).toBe(2); await port.close();
});
it("bounds idle session count and expires old context without silently restarting", async () => {
  const port = runtime(async () => answer("ok"), { maxSessions: 1, sessionTtlMs: 20 });
  await run(port); const previous = input.session.sessionId;
  input.session.sessionId = "another-session";
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("capacity");
  await new Promise(resolve => setTimeout(resolve, 25));
  await expect(port.preflight(input, "synthetic-fixture-key")).resolves.toBeUndefined();
  input.session.sessionId = previous;
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("fresh Runtime session");
  await port.close(); await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("closed");
});
it("invokes the actual bound coordinator callback with empty input and revokes without broad-read fallback", async () => {
  const file = join(root, "selected.txt"); await writeFile(file, "selected");
  let calls = 0, receipts = 0;
  const port = runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    if (++calls === 1) {
      expect(body.tools[0].function.parameters).toMatchObject({ properties: {}, additionalProperties: false });
      return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", tool_calls: [{ id: "managed-read", type: "function", function: { name: "read_file", arguments: "{}" } }] }, finish_reason: "tool_calls" }] }));
    }
    expect(JSON.stringify(body.messages)).toContain("ACTUAL_CALLBACK_RESULT");
    return answer("managed complete");
  });
  input.session.parentSessionId = "manager-session";
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("bound Runtime read callback");
  const release = await port.toolBindings.bind(input.session.sessionId, [{ name: "read_file", description: "read selected", inputSchema: { type: "object", properties: {}, additionalProperties: false }, permission: { effect: "allow", operation: "read", roots: [file] }, async execute(args, signal) { expect(args).toEqual({}); expect(signal.aborted).toBe(false); receipts++; return { path: file, content: "ACTUAL_CALLBACK_RESULT" }; } }]);
  const events = await run(port);
  expect(receipts).toBe(1); expect(events).toContainEqual({ type: "tool:result", data: { name: "read_file", ok: true } });
  expect(events.at(-1)).toMatchObject({ data: { exitCode: 0 } });
  await release(); await release();
  delete input.session.parentSessionId;
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toThrow("fresh Runtime session");
  expect(receipts).toBe(1); await port.close();
});
it("delivers exact selected instructions and an admitted runtime method tool across two turns without cloning callbacks", async () => {
  const file = join(root, "selected-method-resource.txt"); await writeFile(file, "selected");
  const method = { sourceRootId: "chirality-root", source: "bundled" as const, kind: "skill" as const, name: "researcher" };
  const instructionContext: ResolveSelectedContextResponse = {
    schemaVersion: "chirality.selected-context/v3",
    roleId: "TASK",
    methods: [{ ...method, qualifiedId: "chirality-root:bundled:skill:researcher", description: "Research one bounded question.", central: false, compatibility: "canonical", executionRoleIds: ["TASK"], resources: ["SKILL.md", "references/evidence-contract.md"] }],
    documents: [],
    dispositions: [{ method, selected: true, activeRoleCompatible: true, eligibleRoleIds: ["TASK"], route: "primary" }],
    supplied: [
      { kind: "root", id: "root", content: "ROOT_INSTRUCTION_EXACT", sha256: "1".repeat(64) },
      { kind: "project", id: "project", content: "PROJECT_INSTRUCTION_EXACT", sha256: "2".repeat(64) },
      { kind: "role", id: "TASK", content: "ROLE_INSTRUCTION_EXACT", sha256: "3".repeat(64) },
      { kind: "catalog-description", id: "researcher", method, content: "CATALOG_DESCRIPTION_EXACT", sha256: "4".repeat(64) },
      { kind: "method-body", id: "researcher/SKILL.md", method, content: "METHOD_BODY_EXACT", sha256: "5".repeat(64) },
      { kind: "resource", id: "researcher/evidence-contract", method, resourcePath: "references/evidence-contract.md", content: "METHOD_RESOURCE_EXACT", sha256: "6".repeat(64) }
    ],
    basisPreview: { id: "basis-preview-1", sha256: "7".repeat(64), sources: [{ sourceRootId: "chirality-root", source: "bundled", version: "fixture-v1", rootSha256: "8".repeat(64) }], persisted: false },
    compatibilityInputs: []
  };
  let callbackReceipts = 0;
  const runtimeTool: RuntimeToolDefinition = {
    name: "chirality_method_resource", description: "read one selected method resource",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
    permission: { effect: "allow", operation: "read", roots: [file] },
    async execute(args, signal) {
      expect(args).toEqual({}); expect(signal.aborted).toBe(false); callbackReceipts++;
      return { content: "METHOD_TOOL_CALLBACK_EXACT" };
    }
  };
  input.instructionContext = instructionContext;
  input.runtimeTools = [runtimeTool];
  let providerCalls = 0;
  const observedSystemPrompts: string[] = [];
  const port = runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    const system = body.messages.find((message: any) => message.role === "system")?.content;
    expect(typeof system).toBe("string"); observedSystemPrompts.push(system);
    expect(system).toBe(`You are an Agent 2 specialist. Use only the supplied read tools and, when present, the Chirality method-change control callback inside the authorized project. Do not claim write, shell, network or delegation authority.\n\n<chirality-runtime-context schema="v3">\n${JSON.stringify(instructionContext.supplied)}\n</chirality-runtime-context>`);
    providerCalls++;
    if (providerCalls === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", tool_calls: [{ id: "method-tool", type: "function", function: { name: "chirality_method_resource", arguments: "{}" } }] }, finish_reason: "tool_calls" }] }));
    if (providerCalls === 2) {
      expect(body.messages).toContainEqual(expect.objectContaining({ role: "tool", content: expect.stringContaining("METHOD_TOOL_CALLBACK_EXACT") }));
      return answer("FIRST_METHOD_TURN_COMPLETE");
    }
    expect(JSON.stringify(body.messages)).toContain("FIRST_METHOD_TURN_COMPLETE");
    expect(JSON.stringify(body.messages)).toContain("SECOND_METHOD_TURN");
    return answer("SECOND_METHOD_TURN_COMPLETE");
  });
  const firstEvents = await run(port);
  expect(firstEvents.at(-1), JSON.stringify({ firstEvents, providerCalls, observedSystemPrompts, callbackReceipts })).toMatchObject({ data: { exitCode: 0 } });
  input.message = "SECOND_METHOD_TURN"; input.turnId = "method-turn-2";
  const secondEvents = await run(port);
  expect(secondEvents.at(-1), JSON.stringify({ secondEvents, providerCalls, observedSystemPrompts, callbackReceipts })).toMatchObject({ data: { exitCode: 0 } });
  expect(providerCalls).toBe(3);
  expect(callbackReceipts).toBe(1);
  expect(new Set(observedSystemPrompts)).toHaveLength(1);
  expect(input.runtimeTools?.[0]?.execute).toBe(runtimeTool.execute);
  await port.close();
});
it("executes only the exact admitted method-change control callback", async () => {
  let callbackReceipts = 0;
  const controlTool: RuntimeToolDefinition = {
    name: "chirality_request_method_change",
    description: "request a method change at the terminal boundary",
    inputSchema: {
      type: "object",
      properties: {
        mode: { type: "string", enum: ["merge", "replace"] },
        methods: { type: "array", items: { type: "object" } }
      },
      required: ["mode", "methods"],
      additionalProperties: false
    },
    permission: { effect: "allow", operation: "control" },
    async execute(args, signal) {
      expect(args).toEqual({ mode: "replace", methods: [] });
      expect(signal.aborted).toBe(false);
      callbackReceipts++;
      return { status: "requested", requestId: "request-1" };
    }
  };
  input.runtimeTools = [controlTool];
  let providerCalls = 0;
  const port = runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    expect(body.tools.map((tool: any) => tool.function.name)).toEqual(["read_file", "chirality_request_method_change"]);
    providerCalls++;
    if (providerCalls === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", tool_calls: [{ id: "control-call", type: "function", function: { name: "chirality_request_method_change", arguments: '{"mode":"replace","methods":[]}' } }] }, finish_reason: "tool_calls" }] }));
    expect(body.messages).toContainEqual(expect.objectContaining({ role: "tool", content: expect.stringContaining('"status":"requested"') }));
    return answer("CONTROL_REQUEST_RECORDED");
  });

  const events = await run(port);
  expect(events).toContainEqual({ type: "tool:result", data: { name: "chirality_request_method_change", ok: true } });
  expect(events.at(-1)).toMatchObject({ data: { exitCode: 0 } });
  expect(callbackReceipts).toBe(1);
  expect(providerCalls).toBe(2);
  await port.close();
});
it("rejects unknown control and all mutating Runtime callbacks before transport", async () => {
  let providerCalls = 0;
  const port = runtime(async () => { providerCalls++; return answer("UNREACHABLE"); });
  for (const [name, operation] of [
    ["chirality_unknown_control", "control"],
    ["chirality_write", "write"],
    ["chirality_shell", "shell"],
    ["chirality_network", "network"]
  ] as const) {
    input.runtimeTools = [{
      name,
      description: "forbidden",
      inputSchema: { type: "object", properties: {}, additionalProperties: false },
      permission: { effect: "allow", operation },
      async execute() { throw new Error("must not execute"); }
    }];
    await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toMatchObject({ type: "INVALID_REQUEST", status: 403 });
  }

  expect(providerCalls).toBe(0);
  await port.close();
});
it("prepares a reversible context successor and starts a distinct provider span", async () => {
  const supplied = (content: string, sha: string) => ({ kind: "role" as const, id: "TASK", content, sha256: sha.repeat(64) });
  const context = (id: string, content: string, sha: string): ResolveSelectedContextResponse => ({
    schemaVersion: "chirality.selected-context/v3", roleId: "TASK", methods: [], documents: [], dispositions: [], supplied: [supplied(content, sha)],
    basisPreview: { id, sha256: sha.repeat(64), sources: [], persisted: false }, compatibilityInputs: []
  });
  input.instructionContext = context("basis-before", "OLD_ROLE_BODY", "a");
  const bodies: any[] = [];
  const port = runtime(async (_url, init) => { bodies.push(JSON.parse(String(init?.body))); return answer(bodies.length === 1 ? "PRIOR_ASSISTANT" : "SUCCESSOR_ASSISTANT"); });
  const first = await run(port);
  const predecessorEngineSessionId = (first[0] as Extract<UIEvent, { type: "session:init" }>).data.engineSessionId;
  const transcript = JSON.stringify([{ role: "user", content: "PRIOR_USER" }, { role: "assistant", content: "PRIOR_ASSISTANT" }]);
  const continuationSha = createHash("sha256").update(transcript).digest("hex");
  const prepared = await port.prepareContextSuccessor({ sessionId: input.session.sessionId, predecessorEngineSessionId, fromBasisId: "basis-before", toBasisPreview: { id: "basis-after", sha256: "b".repeat(64) }, continuationContext: { transcript, sha256: continuationSha, priorBasisRefs: [{ basisId: "basis-before", sha256: "a".repeat(64) }] } });
  input.instructionContext = context("basis-after", "NEW_ROLE_BODY", "b"); input.contextSuccessor = prepared; input.message = "CURRENT_USER"; input.turnId = "successor-turn";
  const second = await run(port);
  expect((second[0] as Extract<UIEvent, { type: "session:init" }>).data.engineSessionId).not.toBe(predecessorEngineSessionId);
  const successorPrompt = JSON.stringify(bodies[1]);
  expect(successorPrompt).toContain("PRIOR_USER"); expect(successorPrompt).toContain("PRIOR_ASSISTANT"); expect(successorPrompt).toContain("NEW_ROLE_BODY"); expect(successorPrompt).not.toContain("OLD_ROLE_BODY");
  await port.close();
});
it("rejects model-supplied paths on the bound tool and never invents callback evidence", async () => {
  const file = join(root, "selected.txt"); await writeFile(file, "selected"); let calls = 0, receipts = 0;
  const port = runtime(async () => ++calls === 1 ? new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", tool_calls: [{ id: "bad-path", type: "function", function: { name: "read_file", arguments: '{"path":"selected.txt"}' } }] }, finish_reason: "tool_calls" }] })) : answer("denied"));
  await port.toolBindings.bind(input.session.sessionId, [{ name: "read_file", description: "bound", inputSchema: { type: "object", properties: {}, additionalProperties: false }, permission: { effect: "allow", operation: "read", roots: [file] }, async execute() { receipts++; return { content: "not allowed" }; } }]);
  const events = await run(port); expect(receipts).toBe(0); expect(events).toContainEqual({ type: "tool:result", data: { name: "read_file", ok: false } }); await port.close();
});
it("keeps actual compaction context for the next turn without persisting summary events", async () => {
  input.message = "LONG_CONTEXT_MARKER " + "context ".repeat(200);
  let ordinary = 0;
  const port = runtime(async (_url, init) => {
    const body = JSON.parse(String(init?.body));
    if (!body.tools) return answer("IN_MEMORY_COMPACTION_SUMMARY");
    if (++ordinary === 1) return new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", content: "before summary" }, finish_reason: "stop" }], usage: { prompt_tokens: 8190, completion_tokens: 8 } }));
    expect(JSON.stringify(body.messages)).toContain("IN_MEMORY_COMPACTION_SUMMARY");
    return answer("continued");
  }, { compaction: { reserveTokens: 64, keepRecentTokens: 1 } });
  const first = await run(port); expect(JSON.stringify(first)).not.toContain("IN_MEMORY_COMPACTION_SUMMARY");
  input.message = "Continue from prior context"; input.turnId = "after-compaction";
  expect((await run(port)).at(-1)).toMatchObject({ data: { exitCode: 0 } });
  expect(ordinary).toBe(2); await port.close();
});
it("does not expire active sessions and fences simultaneous cache admissions", async () => {
  let entered!: () => void; const requested = new Promise<void>(resolve => { entered = resolve; });
  const port = runtime(async (_url, init) => { entered(); return new Promise<Response>((_resolve, reject) => init?.signal?.addEventListener("abort", () => reject(new Error("aborted")), { once: true })); }, { sessionTtlMs: 1, maxSessions: 1 });
  const pending = run(port); await requested; await new Promise(resolve => setTimeout(resolve, 5));
  await expect(port.preflight(input, "synthetic-fixture-key")).rejects.toMatchObject({ type: "TURN_IN_PROGRESS" });
  const other = structuredClone(input); other.session.sessionId = "other";
  await expect(port.preflight(other, "synthetic-fixture-key")).rejects.toThrow("capacity");
  await port.interrupt(input.session.sessionId); await pending; await port.close();
});
it("revokes a bound callback that ignores AbortSignal and drains without inventing successful receipt", async () => {
  const file = join(root, "selected.txt"); await writeFile(file, "selected");
  let entered!: () => void; const requested = new Promise<void>(resolve => { entered = resolve; }); let receipts = 0;
  const port = runtime(async () => new Response(JSON.stringify({ model: "fixture-model", choices: [{ message: { role: "assistant", tool_calls: [{ id: "managed-hung", type: "function", function: { name: "read_file", arguments: "{}" } }] }, finish_reason: "tool_calls" }] })));
  const release = await port.toolBindings.bind(input.session.sessionId, [{ name: "read_file", description: "bound", inputSchema: { type: "object", properties: {}, additionalProperties: false }, permission: { effect: "allow", operation: "read", roots: [file] }, async execute() { entered(); await new Promise(() => {}); receipts++; return { content: "unreachable" }; } }]);
  const pending = run(port); await requested; await release();
  const events = await pending;
  expect(receipts).toBe(0); expect(events.at(-1)).toMatchObject({ data: { interrupted: true } });
  expect(events.filter(event => event.type === "process:exit")).toHaveLength(1);
  expect(events).not.toContainEqual({ type: "tool:result", data: { name: "read_file", ok: true } });
  await port.close();
});
