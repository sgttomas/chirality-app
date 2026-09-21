import { readFile } from "node:fs/promises";
import { isAbsolute, resolve } from "node:path";
import { RuntimeError } from "@chirality/runtime-contracts";
import { startAppOwnedRuntime, validateAppOwnedRuntimeConfig, type AppOwnedRuntimeConfig, type AppOwnedRuntimeOptions } from "./app-owned-composition.js";

/**
 * Standalone entry for the App-owned composition. The only job is the
 * `daemon` role over a `chirality-app-owned/v1` configuration file; the
 * earlier controlled-worker and supervisor jobs are retired with the private
 * supply chain they depended on.
 */
export interface StandaloneJob { role: "daemon"; socketPath: string; clientTokenFile: string; close(): Promise<void> }

export async function readAppOwnedConfig(configPath: string): Promise<AppOwnedRuntimeConfig> {
  if (typeof configPath !== "string" || !isAbsolute(configPath) || resolve(configPath) !== configPath) throw new RuntimeError("INVALID_REQUEST", "Configuration path must be a normalized absolute path");
  let parsed: unknown;
  try { parsed = JSON.parse(await readFile(configPath, "utf8")); }
  catch (error) { throw new RuntimeError("INVALID_REQUEST", `Configuration file is unreadable (${(error as NodeJS.ErrnoException)?.code ?? "invalid JSON"})`); }
  return validateAppOwnedRuntimeConfig(parsed);
}

export async function startStandaloneJob(role: "daemon", configPath: string, options: AppOwnedRuntimeOptions = {}): Promise<StandaloneJob> {
  if (role !== "daemon") throw new RuntimeError("INVALID_REQUEST", "Expected the daemon job");
  const config = await readAppOwnedConfig(configPath);
  const runtime = await startAppOwnedRuntime(config, options);
  return { role: "daemon", socketPath: runtime.socketPath, clientTokenFile: runtime.clientTokenFile, close: () => runtime.close() };
}
