import { mkdir, mkdtemp, readFile, realpath, rm, stat, symlink, truncate, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type { HarnessEvent, UIEvent } from "@chirality/runtime-contracts";
import { RuntimeClient } from "@chirality/runtime-client";
import { APP_HOST_CLIENT_ID, startAppOwnedRuntime, validateAppOwnedRuntimeConfig, type AppOwnedRuntime, type AppOwnedRuntimeConfig } from "../packages/daemon/src/app-owned-composition.js";
import { resolveHostedProjectTokenFile } from "../packages/daemon/src/hosted-paths.js";
import { createFakeCodexTransport, type FakeCodexTransport } from "./fake-codex-transport.js";
import { createAttachmentSelectionHandler } from "../../chirality-app-dev/frontend/electron/attachment-picker.js";

const cleanups: (() => Promise<unknown>)[] = [];
afterEach(async () => { for (const cleanup of cleanups.splice(0).reverse()) await cleanup().catch(() => undefined); });

async function start(options: { signedIn?: boolean; productText?: string } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), "ao-")));
  cleanups.push(() => rm(root, { recursive: true, force: true }));
  const projectRoot = join(root, "project");
  await mkdir(projectRoot);
  await writeFile(join(projectRoot, "AGENTS.md"), "# Spike project\n", "utf8");
  const manifestPath = join(projectRoot, "chirality.project.json");
  await writeFile(manifestPath, `${JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "spike", displayName: "Spike", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["codex-app-server"], embeddedUi: { declared: false } })}\n`, "utf8");
  const userCodexHome = join(root, "user-codex");
  await mkdir(userCodexHome);
  await writeFile(join(userCodexHome, "config.toml"), "model = \"gpt-5-codex\"\n", "utf8");
  await writeFile(join(userCodexHome, "auth.json"), "{}", "utf8");
  // The bundled instruction tree of this checkout supplies the v3 role registry.
  const instructionRoot = resolve(process.cwd(), "../..");
  const transports: FakeCodexTransport[] = [];
  const config: AppOwnedRuntimeConfig = {
    schema: "chirality-app-owned/v1", socketPath: join(root, "d.sock"), runtimeDirectory: join(root, "runtime"), instructionRoot, clientTokenFile: join(root, "secrets", "app-host.token"),
    codex: { executablePath: join(root, "codex"), userCodexHome, effectiveHome: join(root, "runtime", "codex-home"), expectedVersion: "0.154.0" }
  };
  if (options.productText !== undefined) { config.productInstructionsPath = join(root, "product", "AGENTS.md"); await mkdir(join(root, "product")); await writeFile(config.productInstructionsPath, options.productText); }
  const logs: string[] = [];
  const logger = { warn: (event: string) => { logs.push(event); }, error: (event: string) => { logs.push(`error:${event}`); } };
  const runtimeOptions = { logger, transportFactory: async () => { const fake = createFakeCodexTransport({ signedIn: options.signedIn ?? true, pid: 100 + transports.length }); transports.push(fake); return fake.transport; } };
  const runtime: AppOwnedRuntime = await startAppOwnedRuntime(config, runtimeOptions);
  cleanups.push(() => runtime.close());
  /** A second service over the same runtime directory, as after a hard kill and relaunch. */
  const restart = async (): Promise<AppOwnedRuntime> => { const next = await startAppOwnedRuntime(config, runtimeOptions); cleanups.push(() => next.close()); return next; };
  const app = new RuntimeClient({ socketPath: config.socketPath, tokenFile: config.clientTokenFile });
  const registered = await app.registerHostedBootstrapProject({ manifestPath });
  const project = new RuntimeClient({ socketPath: config.socketPath, tokenFile: resolveHostedProjectTokenFile(config.runtimeDirectory, registered.projectId) });
  return { root, config, runtime, restart, app, project, projectId: registered.projectId, projectRoot, transports, logs, fake: () => transports[transports.length - 1]! };
}
async function collect(stream: AsyncIterable<UIEvent>, until?: (event: UIEvent) => boolean): Promise<UIEvent[]> {
  const events: UIEvent[] = [];
  for await (const event of stream) { events.push(event); if (until?.(event)) break; }
  return events;
}
const harness = (events: UIEvent[]): HarnessEvent[] => events.filter((event): event is Extract<UIEvent, { type: "harness:event" }> => event.type === "harness:event").map(event => event.data);
async function poll<T>(read: () => Promise<T>, ready: (value: T) => boolean, label: string): Promise<T> {
  for (let attempt = 0; attempt < 400; attempt++) { const value = await read(); if (ready(value)) return value; await new Promise(resolve => setTimeout(resolve, 5)); }
  throw new Error(`timed out waiting for ${label}`);
}

describe("App-owned Codex composition", () => {
  it("prepares the effective home, issues the app-host token, reports sign-in status with the catalog, and runs a turn with a declined approval", async () => {
    const f = await start();
    expect((await stat(f.config.clientTokenFile)).mode & 0o777).toBe(0o600);
    expect((await readFile(f.config.clientTokenFile, "utf8")).trim().length).toBeGreaterThan(20);
    expect(f.runtime.effectiveHome).toMatchObject({ linked: ["config.toml"], excluded: ["auth.json"] });
    expect(f.runtime.host.status()).toMatchObject({ state: "running", generation: 1, pid: 100 });
    expect(f.fake().server.state.requests[0]).toMatchObject({ method: "initialize", params: { clientInfo: { name: "chirality", version: "0.154.0" } } });

    const status = await f.app.hostedBootstrapStatus(f.projectId);
    expect(status).toMatchObject({ projectId: f.projectId, ceremony: "signed-in", admission: "ready", canStartLogin: false, selection: { model: "gpt-5-codex", reasoningEffort: "medium" } });
    expect(status.models?.map(entry => entry.model)).toEqual(["gpt-5-codex", "gpt-5-mini"]);
    expect(JSON.stringify(status)).not.toContain("@");

    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    expect(session.engineSelection).toEqual({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-5-codex" });
    const alt = await f.project.createSession(f.projectId, { projectId: f.projectId, modelSelection: { model: "gpt-5-mini", reasoningEffort: "medium" } });
    expect(alt.engineSelection.model).toBe("gpt-5-mini");
    await expect(f.project.createSession(f.projectId, { projectId: f.projectId, modelSelection: { model: "not-listed", reasoningEffort: "low" } })).rejects.toMatchObject({ status: expect.any(Number) });

    const streaming = collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "please approve" }));
    const requests = await poll(() => f.project.listSessionRequests(f.projectId, session.sessionId), value => value.requests.length > 0, "the approval request");
    expect(requests.requests[0]).toMatchObject({ method: "item/commandExecution/requestApproval", itemId: "cmd-turn-1" });
    await expect(f.project.decidePermission(f.projectId, session.sessionId, { requestId: "cmd-turn-1", decision: "deny" })).resolves.toMatchObject({ accepted: true, decision: "deny" });
    const events = await streaming;
    expect(harness(events)[0]?.type).toBe("turn.accepted");
    expect(events.findIndex(event => event.type === "session:init")).toBeGreaterThanOrEqual(0);
    expect(events.findIndex(event => event.type === "session:init")).toBeLessThan(events.findIndex(event => event.type === "chat:delta"));
    const types = harness(events).map(event => event.type);
    expect(types).toEqual(expect.arrayContaining(["turn.started", "tool.started", "tool.permission", "tool.failed", "codex.request.resolved"]));
    expect(types.filter(type => type === "tool.permission")).toHaveLength(2);
    const permission = harness(events).filter(event => event.type === "tool.permission").map(event => event.data as Record<string, unknown>);
    expect(permission[0]).toMatchObject({ behavior: "ask", toolUseId: "cmd-turn-1", toolName: "commandExecution", reason: "scripted" });
    expect(permission[1]).toMatchObject({ behavior: "deny", toolUseId: "cmd-turn-1" });
    expect(harness(events).find(event => event.type === "tool.failed")?.data).toMatchObject({ toolUseId: "cmd-turn-1", status: "declined" });
    // Non-tool notifications pass through unfiltered as codex.notification events.
    expect(harness(events).filter(event => event.type === "codex.notification").map(event => (event.data as { method: string }).method)).toEqual(expect.arrayContaining(["serverRequest/resolved", "item/started", "item/completed"]));
    expect(events.find(event => event.type === "chat:complete")).toMatchObject({ data: { text: "echo: please approve" } });
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
    expect(f.fake().server.state.notes).toContainEqual({ decision: { decision: "decline" } });

    const threadStart = f.fake().server.state.requests.find(request => request.method === "thread/start")?.params as Record<string, unknown>;
    expect(threadStart).toMatchObject({ cwd: f.projectRoot, approvalPolicy: "on-request", sandbox: "workspace-write", model: "gpt-5-codex", ephemeral: false, serviceName: "chirality" });
    expect(typeof threadStart.developerInstructions).toBe("string");
    expect(threadStart.developerInstructions as string).toContain("Chirality");
    expect(f.fake().server.state.requests.find(request => request.method === "thread/settings/update")?.params).toMatchObject({ collaborationMode: { mode: "default", settings: { model: "gpt-5-codex", reasoning_effort: "medium", developer_instructions: null } } });
    expect(f.fake().server.state.requests.find(request => request.method === "turn/start")?.params).toMatchObject({ input: [{ type: "text", text: "please approve" }], model: "gpt-5-codex", effort: "medium" });
    expect(f.fake().server.state.requests.some(request => request.method === "thread/resume")).toBe(false);

    // The next turn of the same session resumes the durable thread; the fake still knows it so no thread/resume is needed.
    const second = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "question" }).then(async stream => { void poll(() => f.project.listSessionRequests(f.projectId, session.sessionId), value => value.requests.some(request => request.method === "item/tool/requestUserInput"), "the question").then(value => f.project.answerSessionRequest(f.projectId, session.sessionId, value.requests[0]!.requestId, { kind: "userInput", answers: { q1: { answers: ["all"] } } })); return stream; }));
    expect(harness(second).map(event => event.type)).toEqual(expect.arrayContaining(["codex.request", "codex.request.resolved"]));
    expect(f.fake().server.state.notes).toContainEqual({ answers: { answers: { q1: { answers: ["all"] } } } });
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start")).toHaveLength(1);
    expect(f.fake().server.state.requests.filter(request => request.method === "turn/start").at(-1)?.params).toMatchObject({ threadId: "thread-1" });
    expect(JSON.stringify(f.logs)).not.toContain("@");
  });

  it("copies native selections into project inputs then session custody before stock Codex input", async () => {
    const f = await start();
    const outside = join(f.root, "selected");
    await mkdir(outside);
    const inside = join(f.projectRoot, "inside.txt");
    const external = join(outside, "visitor-desk-brief.txt");
    const pdf = join(outside, "visitor-plan.pdf");
    const image = join(outside, "visitor-map.png");
    await writeFile(inside, "Inside project notes");
    await writeFile(external, "Visitor desk owner is Morgan.");
    await writeFile(pdf, "%PDF-1.7\ncontrolled fixture\n");
    await writeFile(image, Buffer.from([0x89, 0x50, 0x4e, 0x47]));
    const originals = [inside, external, pdf, image];
    const originalBytes = await Promise.all(originals.map(file => readFile(file)));
    const picker = createAttachmentSelectionHandler({ authorized: () => true, showOpenDialog: async () => ({ canceled: false, filePaths: originals }) });
    const selected = await picker({}, { projectRoot: f.projectRoot });
    if (selected.cancelled) throw new Error(selected.error);
    expect(selected.paths.every(file => file.startsWith(join(f.projectRoot, ".chirality", "attachment-inputs") + "/"))).toBe(true);
    await writeFile(external, "Changed after attachment selection");
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const events = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "Inspect these attachments", attachments: selected.paths }));
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
    expect(harness(events).find(event => event.type === "turn.accepted")?.data).toMatchObject({ attachments: selected.paths });
    const custody = join(f.projectRoot, ".chirality", "attachments", session.sessionId);
    const history = (await readFile(join(custody, "history.jsonl"), "utf8")).trim().split("\n").map(line => JSON.parse(line));
    expect(history.map(item => item.name)).toEqual(["inside.txt", "visitor-desk-brief.txt", "visitor-plan.pdf", "visitor-map.png"]);
    for (const [index, item] of history.entries()) {
      expect(item.sha256).toMatch(/^[a-f0-9]{64}$/);
      expect(await readFile(join(custody, item.stagedName))).toEqual(originalBytes[index]);
      if (originals[index] !== external) expect(await readFile(originals[index]!)).toEqual(originalBytes[index]);
    }
    const native = f.fake().server.state.requests.find(request => request.method === "turn/start")?.params as { input: Array<Record<string, unknown>> };
    expect(native.input).toEqual([
      { type: "text", text: "Inspect these attachments" },
      { type: "text", text: expect.stringContaining("Inside project notes") },
      { type: "text", text: expect.stringContaining("Visitor desk owner is Morgan.") },
      { type: "text", text: expect.stringContaining(join(custody, history[2].stagedName)) },
      { type: "localImage", path: join(custody, history[3].stagedName) }
    ]);
    expect(JSON.stringify(native)).not.toContain(outside);
    const retried = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "Read the same attached copies again", attachments: selected.paths }));
    expect(retried.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
    expect(JSON.stringify(f.fake().server.state.requests.filter(request => request.method === "turn/start").at(-1)?.params)).toContain("Visitor desk owner is Morgan.");
    expect(await readFile(external, "utf8")).toBe("Changed after attachment selection");
    expect(f.fake().server.state.requests.find(request => request.method === "thread/start")?.params).toMatchObject({ cwd: f.projectRoot, sandbox: "workspace-write" });
  });

  it("rejects invalid explicit attachment sources before stock Codex dispatch", async () => {
    const f = await start();
    const selected = join(f.projectRoot, "selected");
    await mkdir(selected);
    const valid = join(selected, "brief.txt");
    const alias = join(selected, "alias.txt");
    const directory = join(selected, "directory.txt");
    const unsupported = join(selected, "script.sh");
    const oversized = join(selected, "oversized.txt");
    const tenMiB = join(selected, "ten.txt");
    const nineMiB = join(selected, "nine.txt");
    await writeFile(valid, "Selected brief"); await symlink(valid, alias); await mkdir(directory);
    await writeFile(unsupported, "echo fixture");
    for (const [file, bytes] of [[oversized, 10 * 1024 * 1024 + 1], [tenMiB, 10 * 1024 * 1024], [nineMiB, 9 * 1024 * 1024]] as const) {
      await writeFile(file, ""); await truncate(file, bytes);
    }
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    for (const attachments of [[alias], [directory], [unsupported], [join(selected, "missing.txt")], [oversized], [tenMiB, nineMiB], Array<string>(9).fill(valid)]) {
      const events = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "Read selected input", attachments }));
      expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
      expect(harness(events).some(event => event.type === "turn.accepted")).toBe(false);
    }
    expect(f.fake().server.state.requests.some(request => request.method === "turn/start")).toBe(false);
    expect(await readFile(valid, "utf8")).toBe("Selected brief");
  });

  it("interrupts a live turn through the session route and records the interrupted terminal", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const streaming = collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "hang" }));
    await poll(() => f.project.sessionTurnState(f.projectId, session.sessionId), state => state.active, "the active turn");
    await poll(async () => f.fake().server.state.requests.some(request => request.method === "turn/start"), Boolean, "turn/start");
    await f.project.interruptSession(f.projectId, session.sessionId);
    const events = await streaming;
    expect(f.fake().server.state.requests.some(request => request.method === "turn/interrupt")).toBe(true);
    expect(harness(events).map(event => event.type)).toContain("turn.interrupted");
    expect(harness(events).find(event => event.type === "turn.interrupted")?.data.reason).toBeUndefined();
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 130 } });
    expect((await f.runtime.service.sessions.get(f.projectId, session.sessionId)).status).not.toBe("running");
  });

  it("shuts down with a live turn: interrupts it as service-shutdown, stops the daemon and terminates the app-server", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const streaming = collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "hang" }));
    await poll(async () => f.fake().server.state.requests.some(request => request.method === "turn/start"), Boolean, "turn/start");
    await f.runtime.close();
    const events = await streaming;
    const terminals = harness(events).filter(event => event.type === "turn.interrupted");
    expect(terminals).toHaveLength(1);
    expect(terminals[0]).toMatchObject({ data: { outcome: "interrupted", reason: "service-shutdown" } });
    const replayed = await f.runtime.service.sessions.replay(f.projectId, session.sessionId);
    expect(replayed.find(event => event.eventId === terminals[0]!.eventId)).toEqual(terminals[0]);
    expect(f.fake().server.state.requests.filter(request => request.method === "turn/start")).toHaveLength(1);
    expect(f.fake().terminated).toBe(true);
    expect(f.runtime.host.status().state).toBe("closed");
    await expect(stat(f.config.socketPath)).rejects.toMatchObject({ code: "ENOENT" });
    await expect(f.runtime.close()).resolves.toBeUndefined();
  });

  it("recovers a persisted running session when the next service starts", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const streaming = collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "hang" }));
    await poll(async () => f.fake().server.state.requests.some(request => request.method === "turn/start"), Boolean, "turn/start");
    expect((await f.runtime.service.sessions.get(f.projectId, session.sessionId)).status).toBe("running");
    // Tear down the fixture through the production shutdown ordering, then
    // deliberately construct stale persisted running state for startup recovery.
    // This tests persisted-state recovery, not actual SIGKILL behavior.
    await f.runtime.close();
    await streaming;
    await f.runtime.service.sessions.update({ ...(await f.runtime.service.sessions.get(f.projectId, session.sessionId)), status: "running" });
    const relaunched = await f.restart();
    expect(f.logs).toContain("runtime.sessions.settled_on_start");
    expect((await relaunched.service.sessions.get(f.projectId, session.sessionId)).status).toBe("interrupted");
    const events = await relaunched.service.sessions.replay(f.projectId, session.sessionId);
    expect(events.at(-1)).toMatchObject({ type: "turn.interrupted", data: { reason: "service-restart" } });
    // The session accepts a new turn again; the relaunched app-server resumes the durable thread.
    const project = new RuntimeClient({ socketPath: f.config.socketPath, tokenFile: resolveHostedProjectTokenFile(f.config.runtimeDirectory, f.projectId) });
    const next = await collect(await project.turnSession(f.projectId, session.sessionId, { message: "after relaunch" }));
    expect(next.find(event => event.type === "chat:complete")).toMatchObject({ data: { text: "echo: after relaunch" } });
    expect(next.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
    // Startup preserves provider continuity when a durable thread association
    // exists; otherwise it establishes a thread for the recovered session.
    expect(f.fake().server.state.requests.some(request => request.method === "thread/resume" || request.method === "thread/start")).toBe(true);
  });

  it("fails the live turn when the app-server dies and keeps serving status afterwards", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const streaming = collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "hang" }));
    await poll(async () => f.fake().server.state.requests.some(request => request.method === "turn/start"), Boolean, "turn/start");
    f.transports[0]!.exit(null, "SIGKILL");
    const events = await streaming;
    expect(harness(events).map(event => event.type)).toContain("turn.failed");
    expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 1 } });
    expect(f.runtime.host.status()).toMatchObject({ state: "restarting", failures: 1 });
    expect(f.logs).toContain("codex.app-server.restart");
  });

  it("relays the sign-in ceremony and refuses new sessions while signed out", async () => {
    const f = await start({ signedIn: false });
    const signedOut = await f.app.hostedBootstrapStatus(f.projectId);
    expect(signedOut).toMatchObject({ ceremony: "ready-to-start", admission: "unavailable", canStartLogin: true });
    expect(signedOut).not.toHaveProperty("models");
    await expect(f.project.createSession(f.projectId, { projectId: f.projectId })).rejects.toMatchObject({ status: 503 });
    const login = await f.app.startHostedBootstrapLogin(f.projectId);
    expect(login).toMatchObject({ authUrl: "https://auth.example.test/authorize?state=opaque" });
    expect(await f.app.hostedBootstrapStatus(f.projectId)).toMatchObject({ ceremony: "pending", canStartLogin: false });
    await expect(f.app.startHostedBootstrapLogin(f.projectId)).rejects.toMatchObject({ status: 409 });
    expect(await f.app.cancelHostedBootstrapLogin(f.projectId)).toMatchObject({ ceremony: "cancelled", canStartLogin: true });
    // A completed ceremony is observed through the account notification and the next status read.
    const again = await f.app.startHostedBootstrapLogin(f.projectId);
    f.fake().server.state.signedIn = true;
    f.fake().server.notify("account/login/completed", { loginId: again.loginId, success: true, error: null });
    expect(await f.app.hostedBootstrapStatus(f.projectId)).toMatchObject({ ceremony: "signed-in", admission: "ready", selection: { model: "gpt-5-codex", reasoningEffort: "medium" } });
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    expect(session.engineSelection.model).toBe("gpt-5-codex");
    expect(await f.app.signOutHostedProject(f.projectId)).toMatchObject({ ceremony: "ready-to-start", admission: "unavailable" });
    expect(f.fake().server.state.requests.some(request => request.method === "account/logout")).toBe(true);
    expect(await f.app.grantHostedProviderNetworkConsent(f.projectId)).toMatchObject({ ceremony: "ready-to-start" });
  });

  it("validates the configuration before touching the file system", () => {
    const base: AppOwnedRuntimeConfig = { schema: "chirality-app-owned/v1", socketPath: "/tmp/d.sock", runtimeDirectory: "/tmp/runtime", instructionRoot: "/tmp/instructions", clientTokenFile: "/tmp/app.token", codex: { executablePath: "/usr/local/bin/codex", userCodexHome: "/tmp/user-codex", effectiveHome: "/tmp/runtime/codex-home", expectedVersion: "0.154.0" } };
    expect(validateAppOwnedRuntimeConfig(base)).toEqual(base);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, schema: "chirality-standalone/v1" })).toThrow(/schema/);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, socketPath: "relative.sock" })).toThrow(/socketPath/);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, socketPath: `/tmp/${"x".repeat(120)}.sock` })).toThrow(/103/);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, codex: { ...base.codex, expectedVersion: "latest" } })).toThrow(/semantic/);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, extra: true })).toThrow(/exactly/);
    expect(validateAppOwnedRuntimeConfig({ ...base, productInstructionsPath: "/tmp/product/AGENTS.md" }).productInstructionsPath).toBe("/tmp/product/AGENTS.md");
    expect(() => validateAppOwnedRuntimeConfig({ ...base, productInstructionsPath: "relative.md" })).toThrow(/absolute/);
    expect(() => validateAppOwnedRuntimeConfig({ ...base, productInstructionsPath: "/tmp/user-codex/AGENTS.md" })).toThrow(/outside Codex/);
    expect(APP_HOST_CLIENT_ID).toBe("app-host");
  });

  it("boots a session without a Codex turn: readiness is recorded and the thread starts with the first message", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    const booted = await f.project.bootSession(f.projectId, session.sessionId);
    expect(booted.boot).toMatchObject({ adapterId: "codex-app-server", providerId: "openai", model: "gpt-5-codex" });
    expect(booted.boot.engineSessionId).toBeUndefined();
    expect(typeof booted.boot.bootedAt).toBe("string");
    expect(booted.session.bootFingerprint).toBe(booted.boot.bootFingerprint);
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start" || request.method === "turn/start")).toHaveLength(0);
    const events = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "after boot", turnId: "client-submitted-turn" }), event => event.type === "process:exit");
    expect(harness(events).filter(event => event.type === "turn.accepted" || event.type === "turn.completed").map(event => event.turnId)).toEqual(["client-submitted-turn", "client-submitted-turn"]);
    expect(harness(events).map(event => event.type)).toContain("turn.completed");
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start")).toHaveLength(1);
  });

  it("adopts changed methods through verified unload and cold resume on the same thread", async () => {
    const f = await start();
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "first" }), event => event.type === "process:exit");
    const firstStarts = f.fake().server.state.requests.filter(request => request.method === "turn/start").length;
    const replacement = await f.project.replaceSelectedMethods(f.projectId, session.sessionId, { boundaryConfirmed: true, methods: [{ kind: "workflow", name: "project-setup" }] });
    expect(replacement.transition).toEqual({ status: "additive", successorAvailable: false });
    expect(replacement.methods).toEqual([expect.objectContaining({ kind: "workflow", name: "project-setup" })]);
    await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "second" }), event => event.type === "process:exit");
    const starts = f.fake().server.state.requests.filter(request => request.method === "turn/start");
    expect(starts).toHaveLength(firstStarts + 1);
    const input = (starts.at(-1)!.params as { input: { type: string; text?: string }[] }).input;
    expect(input.some(item => item.type === "text" && item.text?.startsWith("Chirality context update:"))).toBe(false);
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/unsubscribe")).toHaveLength(1);
    expect(f.fake().server.state.requests.find(request => request.method === "thread/resume")?.params).toMatchObject({ threadId: "thread-1", developerInstructions: expect.stringContaining("project-setup") });
    expect(input.some(item => item.type === "text" && item.text === "second")).toBe(true);
    // One provider thread throughout: no successor, no second thread/start.
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start")).toHaveLength(1);
  });

  it("requires the accepted post-turn basis for workflow changes and preserves earlier supplied instructions", async () => {
    const f = await start({ productText: "PRODUCT_ORIGINAL" });
    const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
    await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "first" }), event => event.type === "process:exit");
    const firstReplay = await f.project.replaySession(f.projectId, session.sessionId);
    const frozen = firstReplay.instructionBases;
    const beforeEdit = await f.project.getSession(f.projectId, session.sessionId);
    await writeFile(f.config.productInstructionsPath!, "PRODUCT_EDITED");
    await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "adopt edit" }), event => event.type === "process:exit");
    const current = await f.project.getSession(f.projectId, session.sessionId);
    expect(current.instructionBasisId).not.toBe(beforeEdit.instructionBasisId);
    expect(current.methodSelectionRevision).toBe(beforeEdit.methodSelectionRevision);
    const methods = [{ sourceRootId: "chirality-root", source: "bundled" as const, kind: "workflow" as const, name: "create-workflow" }];
    await expect(f.project.replaceSelectedMethods(f.projectId, session.sessionId, {
      expectedBasisId: beforeEdit.instructionBasisId, expectedRevision: beforeEdit.methodSelectionRevision,
      boundaryConfirmed: true, selectionMode: "merge", methods
    })).rejects.toThrow("Instruction basis changed before method replacement");
    const replacement = await f.project.replaceSelectedMethods(f.projectId, session.sessionId, {
      expectedBasisId: current.instructionBasisId, expectedRevision: current.methodSelectionRevision,
      boundaryConfirmed: true, selectionMode: "merge", methods
    });
    expect(replacement.methods).toEqual(methods);
    expect(replacement.transition.status).toBe("additive");
    await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "create the workflow" }), event => event.type === "process:exit");
    const replay = await f.project.replaySession(f.projectId, session.sessionId);
    expect(replay.instructionBases).toEqual(expect.arrayContaining(frozen));
    expect(frozen.some(basis => basis.suppliedEntries.some(entry => entry.content === "PRODUCT_ORIGINAL"))).toBe(true);
    expect(replay.instructionBases.some(basis => basis.suppliedEntries.some(entry => entry.content === "PRODUCT_EDITED"))).toBe(true);
    expect(f.fake().server.state.requests.filter(request => request.method === "thread/start")).toHaveLength(1);
  });

  it("creates sessions for a project whose pre-replatform manifest never listed the Codex adapter", async () => {
    const f = await start();
    // A manifest whose enabledAdapterIds name only pre-D-GOV-43 adapters.
    const legacyRoot = join(f.root, "legacy");
    await mkdir(legacyRoot);
    const manifestPath = join(legacyRoot, "chirality.project.json");
    await writeFile(manifestPath, `${JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "legacy-project", displayName: "Legacy", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["stub", "pi"], embeddedUi: { declared: false } })}\n`, "utf8");
    const registered = await f.app.registerHostedBootstrapProject({ manifestPath });
    const legacy = new RuntimeClient({ socketPath: f.config.socketPath, tokenFile: resolveHostedProjectTokenFile(f.config.runtimeDirectory, registered.projectId) });
    const session = await legacy.createSession(registered.projectId, { projectId: registered.projectId });
    expect(session.engineSelection.adapterId).toBe("codex-app-server");
  });
});

it("captures editable product guidance, isolates native roles, and preserves prior adopted bytes across edits", async () => {
  const f = await start({ productText: "# Product common\nFIRST CUSTOM GUIDANCE\n" });
  const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
  await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "first" }));
  const first = f.fake().server.state.requests.find(request => request.method === "thread/start")!.params as { developerInstructions: string; config: Record<string, string> };
  expect(first.developerInstructions).toContain("FIRST CUSTOM GUIDANCE");
  expect(first.developerInstructions).toContain("# HELP_HUMAN");
  expect(first.developerInstructions).not.toContain("# TASK\n");
  expect(first.developerInstructions).not.toContain("# Spike project");
  expect(first.developerInstructions).toContain(join(f.config.instructionRoot, ".agents", "skills"));
  expect(Object.keys(first.config)).toHaveLength(8);
  expect(Object.keys(first.config).every(key => /^agents\.(HELP_HUMAN|HELPS_HUMANS|WORKING_ITEMS|TASK)\.(description|config_file)$/.test(key))).toBe(true);
  const roleFiles = Object.entries(first.config).filter(([key]) => key.endsWith("config_file"));
  for (const [key, path] of roleFiles) {
    const role = key.split(".")[1]!;
    const body = await readFile(path, "utf8");
    const instructions = JSON.parse(body.trim().slice("developer_instructions = ".length)) as string;
    expect(instructions).toContain("FIRST CUSTOM GUIDANCE");
    expect(instructions).toContain(`\n# Active role: ${role}\n`);
    expect(instructions).toContain(`\n# ${role}\n`);
    expect(instructions).toContain("fork_context=false");
    for (const other of ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"].filter(value => value !== role)) expect(instructions).not.toContain(`\n# ${other}\n`);
  }
  const firstEvents = await f.runtime.service.sessions.replay(f.projectId, session.sessionId);
  const acceptance = firstEvents.find(event => event.type === "adapter.initialized");
  expect(acceptance?.data).toMatchObject({ instructionAcceptance: "provider-accepted", providerThreadId: "thread-1" });
  const historyBefore = await f.runtime.service.sessions.instructionBases.history(f.projectId, session.sessionId);
  const firstBasisId = historyBefore.find(record => record.type === "instruction-basis.resolved")!.basisId;
  expect(acceptance?.data.instructionBasisId).toBe(firstBasisId);
  const firstBasis = await f.runtime.service.sessions.instructionBases.get(f.projectId, session.sessionId, firstBasisId);
  expect(firstBasis.suppliedEntries.find(entry => entry.kind === "root")).toMatchObject({ content: "# Product common\nFIRST CUSTOM GUIDANCE\n", path: f.config.productInstructionsPath, origin: join(f.root, "product") });
  expect(firstBasis.suppliedEntries.some(entry => entry.kind === "project")).toBe(false);
  await writeFile(f.config.productInstructionsPath!, "# Product common\nSECOND CUSTOM GUIDANCE\n");
  const events = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "second" }));
  expect(events.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
  const resumed = f.fake().server.state.requests.find(request => request.method === "thread/resume")!.params as { threadId: string; developerInstructions: string; config: Record<string, string> };
  expect(resumed.threadId).toBe("thread-1");
  expect(resumed.developerInstructions).toContain("SECOND CUSTOM GUIDANCE");
  expect(resumed.developerInstructions).not.toContain("FIRST CUSTOM GUIDANCE");
  expect(resumed.config["agents.TASK.config_file"]).not.toBe(first.config["agents.TASK.config_file"]);
  expect(await readFile(first.config["agents.TASK.config_file"]!, "utf8")).toContain("FIRST CUSTOM GUIDANCE");
  expect(await readFile(resumed.config["agents.TASK.config_file"]!, "utf8")).toContain("SECOND CUSTOM GUIDANCE");
  expect(await f.runtime.service.sessions.instructionBases.get(f.projectId, session.sessionId, firstBasisId)).toEqual(firstBasis);
  expect((f.fake().server.state.threads.get("thread-1") as unknown as { developerInstructions: string }).developerInstructions).toBe(resumed.developerInstructions);
  const injection = f.fake().server.state.requests.find(request => request.method === "thread/inject_items")!.params as { threadId: string; items: { type: string; role: string; content: { type: string; text: string }[] }[] };
  expect(injection).toMatchObject({ threadId: "thread-1", items: [{ type: "message", role: "developer", content: [{ type: "input_text" }] }] });
  const injectedText = injection.items[0]!.content[0]!.text;
  expect(injectedText).toContain("supersedes earlier Chirality-provided");
  expect(injectedText.endsWith(resumed.developerInstructions)).toBe(true);
  const historyViews = f.fake().server.state.notes.filter((note: any) => note.modelHistory) as { modelHistory: { content: { text: string }[] }[] }[];
  expect(historyViews[0]!.modelHistory[0]!.content[0]!.text).toBe(first.developerInstructions);
  expect(historyViews[1]!.modelHistory[0]!.content[0]!.text).toBe(first.developerInstructions);
  expect(historyViews[1]!.modelHistory.at(-1)!.content[0]!.text).toBe(injectedText);
  const secondAcceptance = harness(events).find(event => event.type === "adapter.initialized")!;
  expect(secondAcceptance.data.instructionHistoryInjection).toMatchObject({ method: "thread/inject_items", text: injectedText, sha256: expect.stringMatching(/^[a-f0-9]{64}$/) });
  const methods = f.fake().server.state.requests.map(request => request.method);
  expect(methods.indexOf("thread/resume")).toBeLessThan(methods.indexOf("thread/inject_items"));
  expect(methods.indexOf("thread/inject_items")).toBeLessThan(methods.lastIndexOf("turn/start"));
});


it("records resolved edits without provider acceptance while a native child keeps working", async () => {
  const f = await start({ productText: "original guidance" });
  const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
  await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "first" }));
  const child = { id: "child", cwd: f.projectRoot, model: "gpt-5-codex", mode: "default", loaded: true, parentThreadId: "thread-1", status: "active" };
  f.fake().server.state.threads.set("child", child);
  await writeFile(f.config.productInstructionsPath!, "pending edited guidance");
  const pending = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "second" }));
  expect(pending.some(event => event.type === "session:init")).toBe(false);
  expect(harness(pending).some(event => event.type === "adapter.initialized")).toBe(false);
  expect(harness(pending).find(event => event.type === "turn.failed")?.data).toMatchObject({ code: "INSTRUCTION_ADOPTION_PENDING", message: expect.stringContaining("Instruction update pending") });
  expect(pending.find(event => event.type === "turn:error")).toMatchObject({ data: { errorType: "INSTRUCTION_ADOPTION_PENDING", details: { reason: "INSTRUCTION_ADOPTION_PENDING" } } });
  expect(pending.find(event => event.type === "process:exit")).toMatchObject({ data: { errorType: "INSTRUCTION_ADOPTION_PENDING" } });
  expect(f.fake().server.state.requests.filter(request => request.method === "turn/start")).toHaveLength(1);
  expect(f.fake().server.state.requests.some(request => ["thread/unsubscribe", "turn/interrupt"].includes(request.method))).toBe(false);
  const resolved = (await f.runtime.service.sessions.instructionBases.history(f.projectId, session.sessionId)).filter(record => record.type === "instruction-basis.resolved");
  expect(resolved).toHaveLength(2);
  const replay = await f.runtime.service.sessions.replay(f.projectId, session.sessionId);
  expect(replay.filter(event => event.type === "adapter.initialized")).toHaveLength(1);
  child.status = "idle";
  const retry = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "retry" }));
  expect(harness(retry).find(event => event.type === "adapter.initialized")?.data.instructionAcceptance).toBe("provider-accepted");
  expect(f.fake().server.state.requests.filter(request => request.method === "turn/start")).toHaveLength(2);
});


it("does not report adoption or dispatch a user turn after an uncertain injection, then retries the full current basis", async () => {
  const f = await start({ productText: "OLD AMBER" });
  const session = await f.project.createSession(f.projectId, { projectId: f.projectId });
  await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "first" }));
  await writeFile(f.config.productInstructionsPath!, "NEW COPPER");
  f.fake().server.state.injectionOutcome = "applied-error";
  const failed = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "second" }));
  expect(harness(failed).some(event => event.type === "adapter.initialized")).toBe(false);
  expect(failed.some(event => event.type === "session:init")).toBe(false);
  expect(failed.find(event => event.type === "turn:error")).toMatchObject({ data: { errorType: "INSTRUCTION_ADOPTION_PENDING" } });
  expect(f.fake().server.state.requests.filter(request => request.method === "turn/start")).toHaveLength(1);
  const retry = await collect(await f.project.turnSession(f.projectId, session.sessionId, { message: "retry" }));
  expect(retry.at(-1)).toMatchObject({ type: "process:exit", data: { exitCode: 0 } });
  expect(f.fake().server.state.requests.filter(request => request.method === "thread/inject_items")).toHaveLength(2);
  expect(f.fake().server.state.requests.filter(request => request.method === "thread/resume")).toHaveLength(2);
  const accepted = harness(retry).find(event => event.type === "adapter.initialized")!;
  expect(accepted.data.instructionHistoryInjection).toMatchObject({ text: expect.stringContaining("NEW COPPER") });
  const views = f.fake().server.state.notes.filter((note: any) => note.modelHistory) as { modelHistory: { content: { text: string }[] }[] }[];
  expect(views).toHaveLength(2);
  expect(views[1]!.modelHistory).toHaveLength(3);
  expect(views[1]!.modelHistory.at(-1)!.content[0]!.text).toContain("NEW COPPER");
  expect(views[1]!.modelHistory[0]!.content[0]!.text).toContain("OLD AMBER");
});
