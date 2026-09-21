import { createRequire } from "node:module";
import * as ordinary from "node:fs/promises";
import { RuntimeError } from "@chirality/runtime-contracts";

export type RuntimePhysicalFilesystem = Pick<typeof ordinary, "open" | "readFile" | "lstat" | "stat" | "realpath" | "readdir">;
const REQUIRED = Object.freeze(["open", "readFile", "lstat", "stat", "realpath", "readdir"] as const);
let cached: RuntimePhysicalFilesystem | undefined;

function inspect(value: unknown): RuntimePhysicalFilesystem {
  if (!value || typeof value !== "object" || REQUIRED.some(name => typeof (value as Record<string, unknown>)[name] !== "function")) {
    throw new RuntimeError("ENGINE_UNAVAILABLE", "Physical filesystem observation is unavailable", 503);
  }
  return Object.freeze(Object.fromEntries(REQUIRED.map(name => [name, (value as Record<string, unknown>)[name]]))) as RuntimePhysicalFilesystem;
}

function select(electron: boolean, requireBuiltin: (id: string) => unknown, nodeFilesystem: unknown): RuntimePhysicalFilesystem {
  if (!electron) return inspect(nodeFilesystem);
  let original: unknown;
  try { original = requireBuiltin("original-fs"); } catch { throw new RuntimeError("ENGINE_UNAVAILABLE", "Electron physical filesystem observation is unavailable", 503); }
  return inspect((original as { promises?: unknown } | undefined)?.promises);
}

/** Physical observation only. It does not alter Electron ASAR/module resolution. */
export function runtimePhysicalFilesystem(): RuntimePhysicalFilesystem {
  return cached ??= select(Boolean(process.versions.electron), createRequire(process.execPath), ordinary);
}

/** Controlled selector seam; it never changes or populates the production cache. */
export function selectRuntimePhysicalFilesystemForTests(input: {
  electron: boolean;
  requireBuiltin(id: string): unknown;
  nodeFilesystem: unknown;
}): RuntimePhysicalFilesystem {
  return select(input.electron, input.requireBuiltin, input.nodeFilesystem);
}
