#!/usr/bin/env node
import { RuntimeError } from "@chirality/runtime-contracts";
import { startStandaloneJob, type StandaloneJob } from "./standalone.js";

process.umask(0o077);
let job: StandaloneJob | undefined;
let stopping = false;
let finish!: () => void;
const stopped = new Promise<void>(resolve => { finish = resolve; });
const logger = {
  warn(event: string, fields?: Readonly<Record<string, unknown>>) { process.stderr.write(`${JSON.stringify({ level: "warn", event, ...(fields ?? {}) })}\n`); },
  error(event: string, fields?: Readonly<Record<string, unknown>>) { process.stderr.write(`${JSON.stringify({ level: "error", event, ...(fields ?? {}) })}\n`); }
};
async function stop(): Promise<void> {
  if (stopping) return;
  stopping = true;
  try { await job?.close(); } catch { process.stderr.write("Standalone shutdown failed\n"); process.exitCode = 1; }
  finally { finish(); }
}
const signal = () => { void stop(); };
process.on("SIGTERM", signal);
process.on("SIGINT", signal);
try {
  const [role, flag, configPath, ...extra] = process.argv.slice(2);
  if (role !== "daemon" || flag !== "--config" || !configPath || extra.length !== 0) throw new RuntimeError("INVALID_REQUEST", "Usage: chirality-runtime-service daemon --config <absolute-private-json>");
  job = await startStandaloneJob("daemon", configPath, { logger });
  if (stopping) await job.close();
  else {
    process.stdout.write(`${JSON.stringify({ ready: true, role: job.role, socketPath: job.socketPath, clientTokenFile: job.clientTokenFile })}\n`);
    await stopped;
  }
} catch (error) {
  process.stderr.write(`${error instanceof RuntimeError ? `${error.code}: ${error.message}` : `Standalone startup failed (${typeof (error as NodeJS.ErrnoException)?.code === "string" ? (error as NodeJS.ErrnoException).code : "unknown"})`}\n`);
  process.exitCode = 1;
} finally {
  process.off("SIGTERM", signal); process.off("SIGINT", signal);
}
