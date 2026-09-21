import { PassThrough } from "node:stream";
import type { CodexAppServerExit, CodexAppServerTransport } from "../packages/daemon/src/codex-app-server-client.js";
// @ts-expect-error plain ESM fixture shared with the standalone entry test
import { createFakeCodexServer } from "./fixtures/fake-codex-app-server.mjs";

export interface FakeCodexServer {
  state: { injectionOutcome?: "reject" | "applied-error"; signedIn: boolean; threads: Map<string, { id: string; cwd: string; model: string; mode: string }>; requests: { method: string; params: unknown }[]; notes: unknown[]; login?: { loginId: string; pending: boolean } };
  attach(write: (chunk: string) => void): void;
  feed(chunk: string): void;
  notify(method: string, params: unknown): void;
  serverRequest(method: string, params: unknown): Promise<unknown>;
}
export interface FakeCodexTransport {
  transport: CodexAppServerTransport;
  server: FakeCodexServer;
  /** Simulates the child dying. */
  exit(code: number | null, signal?: NodeJS.Signals | null): void;
  terminated: boolean;
}
export function createFakeCodexTransport(options: { signedIn?: boolean; pid?: number } = {}): FakeCodexTransport {
  const stdin = new PassThrough();
  const stdout = new PassThrough();
  const server: FakeCodexServer = createFakeCodexServer(options);
  server.attach(chunk => { if (!handle.terminated) stdout.write(chunk); });
  stdin.setEncoding("utf8");
  stdin.on("data", (chunk: string) => server.feed(chunk));
  let settle!: (exit: CodexAppServerExit) => void;
  const exited = new Promise<CodexAppServerExit>(resolve => { settle = resolve; });
  const handle: FakeCodexTransport = {
    server, terminated: false,
    transport: { pid: options.pid ?? 4242, stdin, stdout, exited, async terminate() { if (!handle.terminated) { handle.terminated = true; settle({ code: 0, signal: null }); } await exited; } },
    exit(code, signal = null) { if (!handle.terminated) { handle.terminated = true; settle({ code, signal }); } }
  };
  return handle;
}
