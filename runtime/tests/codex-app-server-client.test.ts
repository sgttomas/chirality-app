import { describe, expect, it } from "vitest";
import { CodexAppServerClient, CodexAppServerHost, JSON_RPC_METHOD_NOT_FOUND, redactAccountText, CODEX_APP_SERVER_ARGUMENTS } from "../packages/daemon/src/codex-app-server-client.js";
import { createFakeCodexTransport } from "./fake-codex-transport.js";

const tick = () => new Promise(resolve => setTimeout(resolve, 5));

describe("Codex app-server client", () => {
  it("correlates JSON-RPC responses, delivers notifications and answers server requests", async () => {
    const fake = createFakeCodexTransport();
    const client = new CodexAppServerClient(fake.transport, { requestTimeoutMs: 1000 });
    const seen: string[] = [];
    client.onNotification(notification => seen.push(notification.method));
    const initialized = await client.request<{ userAgent: string }>("initialize", { clientInfo: { name: "chirality", title: "Chirality", version: "0.0.0" }, capabilities: { experimentalApi: true } });
    expect(initialized.userAgent).toBe("fake-codex/0.154.0");
    await expect(client.request("nope/method", {})).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { jsonRpcCode: -32601 } });
    client.setServerRequestHandler(async request => request.method === "item/tool/call" ? { result: { success: false, contentItems: [] } } : { error: { code: JSON_RPC_METHOD_NOT_FOUND, message: "unsupported request" } });
    const answered = fake.server.serverRequest("item/tool/call", { threadId: "t", turnId: "u", callId: "c", tool: "x", arguments: {} });
    const refused = fake.server.serverRequest("attestation/generate", { threadId: "t" });
    await expect(answered).resolves.toEqual({ success: false, contentItems: [] });
    await expect(refused).resolves.toEqual({ error: { code: -32601, message: "unsupported request" } });
    fake.server.notify("thread/started", { thread: { id: "t-1" } });
    await tick();
    expect(seen).toEqual(["thread/started"]);
    expect(client.isRunning).toBe(true);
    await client.close();
    expect(client.isRunning).toBe(false);
  });

  it("rejects every pending request once the child exits and refuses new ones", async () => {
    const fake = createFakeCodexTransport();
    const client = new CodexAppServerClient(fake.transport, { requestTimeoutMs: 0 });
    const pending = client.request("thread/start", { cwd: "/nowhere" }).catch(error => error);
    // A request the fake never answers keeps the queue occupied; the exit must settle it.
    const hanging = client.request("chirality/never", {}).catch(error => error);
    await tick();
    fake.exit(null, "SIGKILL");
    const failure = await hanging;
    expect(failure).toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { reason: "CODEX_APP_SERVER_EXITED", signal: "SIGKILL" } });
    await pending;
    await expect(client.request("account/read", {})).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { reason: "CODEX_APP_SERVER_EXITED" } });
  });

  it("times out an unanswered request without disturbing the transport", async () => {
    const fake = createFakeCodexTransport();
    const client = new CodexAppServerClient(fake.transport, { requestTimeoutMs: 20 });
    await expect(client.request("chirality/never", {})).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", message: expect.stringContaining("within 20 ms") });
    await expect(client.request("account/read", {}, { timeoutMs: 1000 })).resolves.toMatchObject({ requiresOpenaiAuth: false });
    await client.close();
  });

  it("redacts e-mail-like tokens from diagnostics and pins the app-server arguments", () => {
    // The address-like token is assembled at runtime so no literal address lives in the fixture.
    expect(redactAccountText(`signed in as ${["someone", "example.test"].join("@")} today`)).toBe("signed in as [redacted] today");
    expect([...CODEX_APP_SERVER_ARGUMENTS]).toEqual(["-c", 'cli_auth_credentials_store="file"', "-c", "thread_unload_delay_secs=0", "app-server"]);
  });
});

describe("Codex app-server host", () => {
  it("initializes on start, restarts with backoff after an unexpected exit and fails active requests", async () => {
    const fakes: ReturnType<typeof createFakeCodexTransport>[] = [];
    const starts: number[] = [];
    const exits: { code: number | null; generation: number }[] = [];
    const host = new CodexAppServerHost({ clientVersion: "0.0.0", transportFactory: async () => { const fake = createFakeCodexTransport({ pid: 100 + fakes.length }); fakes.push(fake); return fake.transport; }, restartBackoffMs: [5], requestTimeoutMs: 1000 });
    host.onStart(generation => starts.push(generation));
    host.onExit((exit, generation) => exits.push({ code: exit.code, generation }));
    await host.start();
    expect(host.status()).toMatchObject({ state: "running", generation: 1, pid: 100, failures: 0 });
    expect(fakes[0]!.server.state.requests[0]).toMatchObject({ method: "initialize", params: { clientInfo: { name: "chirality" }, capabilities: { experimentalApi: true } } });
    const inFlight = host.request("chirality/never", {}).catch(error => error);
    await tick();
    fakes[0]!.exit(1);
    await expect(inFlight).resolves.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { reason: "CODEX_APP_SERVER_EXITED", code: 1 } });
    expect(exits).toEqual([{ code: 1, generation: 1 }]);
    await expect(host.request("account/read", {})).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { state: "restarting" } });
    await new Promise(resolve => setTimeout(resolve, 30));
    expect(host.status()).toMatchObject({ state: "running", generation: 2, pid: 101, failures: 1 });
    expect(starts).toEqual([1, 2]);
    await expect(host.request("account/read", {})).resolves.toMatchObject({ requiresOpenaiAuth: false });
    await host.close();
    expect(host.status().state).toBe("closed");
    expect(fakes[1]!.terminated).toBe(true);
  });

  it("stops restarting after repeated failures inside the window", async () => {
    let spawned = 0;
    const host = new CodexAppServerHost({ clientVersion: "0.0.0", transportFactory: async () => { spawned++; const fake = createFakeCodexTransport(); setTimeout(() => fake.exit(2), 2); return fake.transport; }, restartBackoffMs: [1], maxFailures: 3, failureWindowMs: 60_000, requestTimeoutMs: 1000 });
    await host.start();
    await new Promise(resolve => setTimeout(resolve, 80));
    expect(host.status()).toMatchObject({ state: "stopped", failures: 3 });
    expect(spawned).toBe(3);
    await host.close();
  });

  it("refuses to start when initialize fails and closes the child", async () => {
    const fake = createFakeCodexTransport();
    fake.server.feed = () => { /* never answers */ };
    const host = new CodexAppServerHost({ clientVersion: "0.0.0", transportFactory: async () => fake.transport, requestTimeoutMs: 20 });
    await expect(host.start()).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE" });
    expect(fake.terminated).toBe(true);
    expect(host.status().state).toBe("stopped");
  });
});
