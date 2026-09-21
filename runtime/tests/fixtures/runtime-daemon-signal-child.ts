import { readFile } from "node:fs/promises";
import type { IncomingMessage, Server } from "node:http";
import { connect } from "node:net";
import { join } from "node:path";
import {
  AuthRegistry,
  EngineRegistry,
  ProjectRegistry,
  ResidencyCoordinator,
  RuntimeService,
  SessionStore,
  TurnCoordinator
} from "../../packages/core/src/index.js";
import { RuntimeDaemon } from "../../packages/daemon/src/runtime-daemon.js";
import { installRuntimeDaemonSignalShutdown } from "../../packages/daemon/src/signal-shutdown.js";

const runtimeDirectory = process.env["CHIRALITY_SIGNAL_FIXTURE_RUNTIME"];
if (runtimeDirectory === undefined) throw new Error("fixture runtime directory is required");

const socketPath = join(runtimeDirectory, "control.sock");
const projects = new ProjectRegistry(runtimeDirectory);
const sessions = new SessionStore(runtimeDirectory, projects);
const engines = new EngineRegistry();
const residency = new ResidencyCoordinator(
  {
    async listStatus() {
      return [];
    },
    async load() {},
    async unload() {}
  },
  runtimeDirectory
);
const auth = new AuthRegistry(runtimeDirectory);
const turns = new TurnCoordinator(projects, sessions, engines, residency);
const service = new RuntimeService(
  projects,
  sessions,
  engines,
  residency,
  turns,
  auth,
  {
    async get() {
      return undefined;
    },
    async status() {
      return { configured: false };
    },
    async set() {},
    async remove() {}
  }
);
const daemon = new RuntimeDaemon({ runtimeDirectory, socketPath, service });
const started = await daemon.start();
const token = (await readFile(started.operatorTokenFile, "utf8")).trim();

const initialSigtermListeners = process.listenerCount("SIGTERM");
const shutdown = installRuntimeDaemonSignalShutdown(daemon, {
  reportFailure(error, signal) {
    process.stderr.write(
      `${JSON.stringify({ event: "STOP_FAILED", signal, error: String(error) })}\n`
    );
  }
});
const installedSigtermListeners = process.listenerCount("SIGTERM");

const server = (daemon as unknown as { server?: Server }).server;
if (server === undefined) throw new Error("daemon server was not available after start");
let observedRequest: IncomingMessage | undefined;
const requestParsed = new Promise<void>((resolve) => {
  const observe = (request: IncomingMessage): void => {
    if (request.url !== "/v1/projects/register") return;
    observedRequest = request;
    server.off("request", observe);
    resolve();
  };
  server.on("request", observe);
});

const holder = connect(socketPath);
holder.on("error", (error) => {
  process.stderr.write(`${JSON.stringify({ event: "HOLDER_FAILED", error: error.message })}\n`);
  process.exitCode = 1;
});
await new Promise<void>((resolve, reject) => {
  holder.once("connect", resolve);
  holder.once("error", reject);
});

const declaredLength = 100;
const partialBody = "{";
const flushed = holder.write(
  [
    "POST /v1/projects/register HTTP/1.1",
    "Host: chirality.local",
    `Authorization: Bearer ${token}`,
    "Content-Type: application/json",
    `Content-Length: ${declaredLength}`,
    "Connection: keep-alive",
    "",
    partialBody
  ].join("\r\n")
);

if (!flushed) await new Promise<void>((resolve) => holder.once("drain", resolve));
await Promise.race([
  requestParsed,
  new Promise<never>((_resolve, reject) =>
    setTimeout(() => reject(new Error("partial request headers were not parsed")), 1_000)
  )
]);
await new Promise((resolve) => setTimeout(resolve, 50));
if (observedRequest === undefined || observedRequest.complete || observedRequest.readableEnded) {
  throw new Error("partial request did not remain active with its body incomplete");
}
process.stdout.write(
  `${JSON.stringify({
    event: "ARMED",
    socketPath,
    ownerFile: `${socketPath}.owner.json`,
    declaredLength,
    suppliedLength: Buffer.byteLength(partialBody),
    requestParsed: true,
    requestComplete: observedRequest.complete,
    requestReadableEnded: observedRequest.readableEnded,
    installedSigtermListeners: installedSigtermListeners - initialSigtermListeners
  })}\n`
);

await shutdown.completion;
process.stdout.write(
  `${JSON.stringify({
    event: "STOPPED",
    sigtermListenersRestored:
      process.listenerCount("SIGTERM") === initialSigtermListeners
  })}\n`
);
