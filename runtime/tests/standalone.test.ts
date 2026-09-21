import { spawn } from "node:child_process";
import { chmod, mkdir, mkdtemp, realpath, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";
import { RuntimeClient } from "@chirality/runtime-client";
import { readAppOwnedConfig, startStandaloneJob } from "../packages/daemon/src/standalone.js";

const cleanups: (() => Promise<unknown>)[] = [];
afterEach(async () => { for (const cleanup of cleanups.splice(0).reverse()) await cleanup().catch(() => undefined); });
const runtimeRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const fakeCodex = join(runtimeRoot, "tests", "fixtures", "fake-codex.mjs");
const binary = join(runtimeRoot, "packages", "daemon", "dist", "standalone-bin.js");

async function configFile(options: { version?: string; executable?: string } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), "sa-")));
  cleanups.push(() => rm(root, { recursive: true, force: true }));
  await mkdir(join(root, "instructions"));
  await mkdir(join(root, "user-codex"));
  await writeFile(join(root, "user-codex", "config.toml"), "", "utf8");
  // A shim keeps the fixture executable on the configured absolute path with the real node.
  const shim = join(root, "codex");
  await writeFile(shim, `#!/bin/sh\nexec "${process.execPath}" "${fakeCodex}" "$@"\n`, "utf8");
  await chmod(shim, 0o700);
  const config = { schema: "chirality-app-owned/v1", socketPath: join(root, "d.sock"), runtimeDirectory: join(root, "runtime"), instructionRoot: join(root, "instructions"), clientTokenFile: join(root, "app.token"), codex: { executablePath: options.executable ?? shim, userCodexHome: join(root, "user-codex"), effectiveHome: join(root, "runtime", "codex-home"), expectedVersion: options.version ?? "0.154.0" } };
  const path = join(root, "config.json");
  await writeFile(path, JSON.stringify(config), "utf8");
  return { root, path, config };
}

describe("standalone daemon job", () => {
  it("reads only the app-owned configuration and rejects other schemas or roles", async () => {
    const { path, config, root } = await configFile();
    expect(await readAppOwnedConfig(path)).toEqual(config);
    await writeFile(join(root, "legacy.json"), JSON.stringify({ schema: "chirality-standalone/v1", mode: "controlled-worker" }), "utf8");
    await expect(readAppOwnedConfig(join(root, "legacy.json"))).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(readAppOwnedConfig(join(root, "missing.json"))).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(readAppOwnedConfig("relative.json")).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(startStandaloneJob("supervisor" as never, path)).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("refuses a Codex executable whose version differs from the pin before spawning the app-server", async () => {
    const { path, root } = await configFile({ version: "0.153.0" });
    await expect(startStandaloneJob("daemon", path)).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { reason: "CODEX_VERSION_MISMATCH", observed: "0.154.0" } });
    await expect(stat(join(root, "d.sock"))).rejects.toMatchObject({ code: "ENOENT" });
    const missing = await configFile({ executable: join(root, "no-such-codex") });
    await expect(startStandaloneJob("daemon", missing.path)).rejects.toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { reason: "CODEX_EXECUTABLE_UNAVAILABLE" } });
  });

  it("starts the daemon over the pinned fake Codex, serves the app-host token, and closes cleanly", async () => {
    const { path, config } = await configFile();
    const job = await startStandaloneJob("daemon", path);
    cleanups.push(() => job.close());
    expect(job).toMatchObject({ role: "daemon", socketPath: config.socketPath, clientTokenFile: config.clientTokenFile });
    const client = new RuntimeClient({ socketPath: job.socketPath, tokenFile: job.clientTokenFile });
    await expect(client.health()).resolves.toHaveProperty("apiVersion");
    await job.close();
    await expect(stat(config.socketPath)).rejects.toMatchObject({ code: "ENOENT" });
  });

  it("prints exactly one ready line from the binary and exits 0 on SIGTERM", async () => {
    const { path, config } = await configFile();
    const child = spawn(process.execPath, [binary, "daemon", "--config", path], { stdio: ["ignore", "pipe", "pipe"] });
    cleanups.push(async () => { if (child.exitCode === null) child.kill("SIGKILL"); });
    let stdout = "", stderr = "";
    child.stdout.setEncoding("utf8"); child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => { stdout += chunk; });
    child.stderr.on("data", (chunk: string) => { stderr += chunk; });
    const exited = new Promise<{ code: number | null; signal: NodeJS.Signals | null }>(resolve => child.once("exit", (code, signal) => resolve({ code, signal })));
    for (let attempt = 0; attempt < 600 && !stdout.includes("\n"); attempt++) await new Promise(resolve => setTimeout(resolve, 10));
    expect(stdout.split("\n").filter(Boolean)).toHaveLength(1);
    expect(JSON.parse(stdout.trim())).toEqual({ ready: true, role: "daemon", socketPath: config.socketPath, clientTokenFile: config.clientTokenFile });
    const client = new RuntimeClient({ socketPath: config.socketPath, tokenFile: config.clientTokenFile });
    await expect(client.health()).resolves.toHaveProperty("apiVersion");
    child.kill("SIGTERM");
    await expect(exited).resolves.toEqual({ code: 0, signal: null });
    expect(stdout.split("\n").filter(Boolean)).toHaveLength(1);
    expect(stderr).not.toContain("@");
    await expect(stat(config.socketPath)).rejects.toMatchObject({ code: "ENOENT" });
  });

  it("reports a usage error for unsupported roles", async () => {
    const { path } = await configFile();
    const child = spawn(process.execPath, [binary, "supervisor", "--config", path], { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";
    child.stderr.setEncoding("utf8"); child.stderr.on("data", (chunk: string) => { stderr += chunk; });
    const exit = await new Promise<number | null>(resolve => child.once("exit", code => resolve(code)));
    expect(exit).toBe(1);
    expect(stderr).toContain("INVALID_REQUEST");
  });
});
