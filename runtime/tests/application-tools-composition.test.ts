import { mkdir, mkdtemp, realpath, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { RuntimeClient } from "@chirality/runtime-client";
import type { ApplicationToolInvocation, ApplicationToolRegistrationRequest, UIEvent } from "@chirality/runtime-contracts";
import { startAppOwnedRuntime, type AppOwnedRuntimeConfig } from "../packages/daemon/src/app-owned-composition.js";
import { resolveHostedProjectTokenFile } from "../packages/daemon/src/hosted-paths.js";
import { createFakeCodexTransport, type FakeCodexTransport } from "./fake-codex-transport.js";

const cleanup: (() => Promise<unknown>)[] = [];
afterEach(async () => { for (const fn of cleanup.splice(0).reverse()) await fn(); });
const registration = (workspaceGeneration = "workspace-generation-1"): ApplicationToolRegistrationRequest => ({
  applicationId: "swbpipe", workspaceId: "invented-workspace", workspaceGeneration, timeoutMs: 30_000,
  tools: [{ type: "function", name: "swbpipe_inspect_selection", description: "Inspect the selected object in the bound workspace.", inputSchema: { type: "object", properties: {}, additionalProperties: false } }]
});
async function fixture() {
  const root = await realpath(await mkdtemp(join(tmpdir(), "at-")));
  cleanup.push(() => rm(root, { recursive: true, force: true }));
  const projectRoot = join(root, "project"); await mkdir(projectRoot);
  const manifestPath = join(projectRoot, "chirality.project.json");
  await writeFile(manifestPath, JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "tools-fixture", displayName: "Tool fixture", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["codex-app-server"], embeddedUi: { declared: false } }));
  const userCodexHome = join(root, "fixture-home"); await mkdir(userCodexHome);
  await writeFile(join(userCodexHome, "config.toml"), 'model = "gpt-5-codex"\n');
  const config: AppOwnedRuntimeConfig = { schema: "chirality-app-owned/v1", socketPath: join(root, "r.sock"), runtimeDirectory: join(root, "runtime"), instructionRoot: resolve(process.cwd(), "../.."), clientTokenFile: join(root, "host-token"), codex: { executablePath: join(root, "unused-codex"), userCodexHome, effectiveHome: join(root, "effective-home"), expectedVersion: "0.154.0" } };
  const transports: FakeCodexTransport[] = [];
  const options = { transportFactory: async () => { const transport = createFakeCodexTransport({ signedIn: true, pid: 700 + transports.length }); transports.push(transport); return transport.transport; } };
  let runtime = await startAppOwnedRuntime(config, options); cleanup.push(() => runtime.close());
  const app = new RuntimeClient({ socketPath: config.socketPath, tokenFile: config.clientTokenFile });
  const { projectId } = await app.registerHostedBootstrapProject({ manifestPath });
  const project = new RuntimeClient({ socketPath: config.socketPath, tokenFile: resolveHostedProjectTokenFile(config.runtimeDirectory, projectId) });
  await app.hostedBootstrapStatus(projectId);
  return { app, project, projectId, runtime: () => runtime, fake: () => transports.at(-1)!, async restart() { await runtime.close(); runtime = await startAppOwnedRuntime(config, options); } };
}
async function poll<T>(read: () => Promise<T>, ready: (value: T) => boolean): Promise<T> {
  for (let i = 0; i < 400; i++) { const value = await read(); if (ready(value)) return value; await new Promise(resolve => setTimeout(resolve, 5)); }
  throw new Error("Timed out waiting for controlled application-tool state");
}
async function collect(stream: AsyncIterable<UIEvent>) { const events: UIEvent[] = []; for await (const event of stream) events.push(event); return events; }
const response = { success: true, contentItems: [{ type: "inputText" as const, text: '{"basis_token":"opaque-basis-1","selected_refs":["node:fixture"]}' }] };

describe("application tools through the owning host and production Runtime composition", () => {
  it("keeps ordinary conversations tool-free across consecutive turns", async () => {
    const f = await fixture(); const s = await f.project.createSession(f.projectId, { projectId: f.projectId });
    for (const message of ["first", "second"]) {
      const events = await collect(await f.project.turnSession(f.projectId, s.sessionId, { message }));
      expect(events.some(event => event.type === "chat:complete")).toBe(true);
    }
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start")).toHaveLength(1);
    expect(f.fake().server.state.requests.find(request => request.method === "thread/start")!.params).not.toHaveProperty("dynamicTools");
    await expect(f.app.registerApplicationTools(f.projectId, s.sessionId, registration())).rejects.toMatchObject({ status: 409 });
  });

  it("registers only from the host, carries caller identity, detaches without cancellation and completes once", async () => {
    const f = await fixture(); const s = await f.project.createSession(f.projectId, { projectId: f.projectId });
    await expect(f.project.registerApplicationTools(f.projectId, s.sessionId, registration())).rejects.toMatchObject({ status: 403 });
    const binding = await f.app.registerApplicationTools(f.projectId, s.sessionId, registration());
    const stream = await f.project.turnSession(f.projectId, s.sessionId, { message: "hang" });
    const observed = collect(stream);
    await poll(async () => f.fake().server.state.requests, requests => requests.some(request => request.method === "turn/start"));
    const threadId = [...f.fake().server.state.threads.keys()][0]!;
    expect(f.fake().server.state.requests.find(request => request.method === "thread/start")!.params).toMatchObject({ dynamicTools: registration().tools });
    const native = f.fake().server.serverRequest("item/tool/call", { threadId, turnId: "turn-1", callId: "inspect-call", namespace: null, tool: "swbpipe_inspect_selection", arguments: {} });
    const calls = await poll(() => f.app.listApplicationToolCalls(f.projectId, s.sessionId, binding.bindingId), result => result.calls.length === 1);
    const call = calls.calls[0]!;
    expect(call).toMatchObject({ bindingId: binding.bindingId, applicationId: "swbpipe", workspaceId: "invented-workspace", workspaceGeneration: "workspace-generation-1", runtimeProjectId: f.projectId, runtimeSessionId: s.sessionId, providerThreadId: threadId, providerTurnId: "turn-1", callId: "inspect-call", arguments: {}, status: "pending" });
    expect(call.runtimeTurnId).toBe((await f.project.sessionTurnState(f.projectId, s.sessionId)).turnId);
    await expect(f.project.listApplicationToolCalls(f.projectId, s.sessionId, binding.bindingId)).rejects.toMatchObject({ status: 403 });
    stream.cancel(); await observed.catch(() => undefined);
    expect((await f.project.sessionTurnState(f.projectId, s.sessionId)).active).toBe(true);
    await expect(f.app.completeApplicationToolCall(f.projectId, s.sessionId, call.invocationId, { bindingId: "foreign", result: response })).rejects.toMatchObject({ status: 409 });
    expect(await f.app.completeApplicationToolCall(f.projectId, s.sessionId, call.invocationId, { bindingId: binding.bindingId, result: response })).toEqual({ state: "completed" });
    expect(await native).toEqual(response);
    expect(await f.app.completeApplicationToolCall(f.projectId, s.sessionId, call.invocationId, { bindingId: binding.bindingId, result: response })).toEqual({ state: "already-completed" });
    await f.project.interruptSession(f.projectId, s.sessionId);
    await poll(() => f.project.sessionTurnState(f.projectId, s.sessionId), state => !state.active);
    expect(await f.app.completeApplicationToolCall(f.projectId, s.sessionId, call.invocationId, { bindingId: binding.bindingId, result: response })).toEqual({ state: "already-completed" });
    const replay = await f.project.replaySession(f.projectId, s.sessionId);
    expect(JSON.stringify(replay)).toContain("opaque-basis-1");
    expect((await f.app.listApplicationToolCalls(f.projectId, s.sessionId, binding.bindingId)).calls).toHaveLength(1);
    await expect(f.app.registerApplicationTools(f.projectId, s.sessionId, { ...registration(), tools: [] })).rejects.toMatchObject({ status: 409 });
  });

  it("cancels a pending call on Stop and refuses its delayed completion", async () => {
    const f = await fixture(); const s = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const binding = await f.app.registerApplicationTools(f.projectId, s.sessionId, registration());
    const events = collect(await f.project.turnSession(f.projectId, s.sessionId, { message: "hang" }));
    await poll(async () => f.fake().server.state.requests, requests => requests.some(request => request.method === "turn/start"));
    const threadId = [...f.fake().server.state.threads.keys()][0]!;
    const native = f.fake().server.serverRequest("item/tool/call", { threadId, turnId: "turn-1", callId: "cancel-call", namespace: null, tool: "swbpipe_inspect_selection", arguments: {} });
    const calls = await poll(() => f.app.listApplicationToolCalls(f.projectId, s.sessionId, binding.bindingId), result => result.calls.length === 1);
    await f.project.interruptSession(f.projectId, s.sessionId); await events;
    expect(await native).toMatchObject({ success: false });
    expect((await f.app.listApplicationToolCalls(f.projectId, s.sessionId, binding.bindingId)).calls[0]!.status).toBe("cancelled");
    await expect(f.app.completeApplicationToolCall(f.projectId, s.sessionId, calls.calls[0]!.invocationId, { bindingId: binding.bindingId, result: response })).rejects.toMatchObject({ status: 409 });
  });

  it("restores the immutable catalog but requires a fresh binding after service restart", async () => {
    const f = await fixture(); const s = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const oldBinding = await f.app.registerApplicationTools(f.projectId, s.sessionId, registration());
    await collect(await f.project.turnSession(f.projectId, s.sessionId, { message: "initial" }));
    await f.restart();
    const restored = await f.app.applicationTools(f.projectId, s.sessionId);
    expect(restored.catalog?.tools).toEqual(registration().tools); expect(restored.binding).toBeUndefined();
    const blocked = await collect(await f.project.turnSession(f.projectId, s.sessionId, { message: "no handler" }));
    expect(JSON.stringify(blocked)).toContain("handler is unavailable");
    expect(f.fake().server.state.requests.filter(request => request.method === "turn/start")).toHaveLength(0);
    const rebound = await f.app.registerApplicationTools(f.projectId, s.sessionId, registration("workspace-generation-2"));
    expect(rebound.bindingId).not.toBe(oldBinding.bindingId);
    const continued = await collect(await f.project.turnSession(f.projectId, s.sessionId, { message: "continued" }));
    expect(continued.some(event => event.type === "chat:complete")).toBe(true);
    const resumed = f.fake().server.state.requests.find(request => request.method === "thread/resume");
    expect(resumed).toBeDefined(); expect(resumed!.params).not.toHaveProperty("dynamicTools");
    await expect(f.app.listApplicationToolCalls(f.projectId, s.sessionId, oldBinding.bindingId)).rejects.toMatchObject({ status: 409 });
  });
});
