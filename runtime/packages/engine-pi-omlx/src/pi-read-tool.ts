import { constants } from "node:fs";
import { lstat, open, realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep } from "node:path";
import { Type } from "@earendil-works/pi-ai";
import type { ToolDefinition } from "@earendil-works/pi-coding-agent";
import { HarnessError } from "@chirality/runtime-contracts";
const inside = (root: string, path: string) => { const rel = relative(root, path); return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel)); };
const denied = () => new HarnessError("INVALID_REQUEST", 403, "Read is outside the authorized regular-file boundary");
export function createPiReadTool(options: { canonicalRoot: string; name: "read" | "read_file"; protectedPaths?: readonly string[]; maxBytes?: number }): ToolDefinition {
  const canonicalRoot = options.canonicalRoot, name = options.name;
  if (!["read", "read_file"].includes(name)) throw denied();
  const maxBytes = options.maxBytes ?? 65536;
  if (!Number.isSafeInteger(maxBytes) || maxBytes < 1 || maxBytes > 1048576) throw denied();
  const protectedPaths = [...(options.protectedPaths ?? [])].map(path => resolve(path));
  return {
    name, label: "Read authorized project file", description: "Read one bounded regular UTF-8 file inside the authorized project. Paths outside the project and protected control paths are unavailable.",
    parameters: Type.Object({ path: Type.String({ minLength: 1, maxLength: 4096 }) }, { additionalProperties: false }),
    async execute(_id, input, signal) {
      if (signal?.aborted) throw denied();
      const value = input as { path?: unknown };
      if (!value || typeof value.path !== "string" || !value.path || /[\x00-\x1f\x7f]/.test(value.path) || Object.keys(value).some(key => key !== "path")) throw denied();
      const root = canonicalRoot;
      if (await realpath(root) !== root) throw denied();
      const path = resolve(root, value.path);
      if (!inside(root, path) || path === root || protectedPaths.some(protectedPath => inside(protectedPath, path))) throw denied();
      let handle;
      try {
        // Reject each symlink component, not merely a symlink final leaf.
        let cursor = root;
        for (const component of relative(root, path).split(sep)) { cursor = resolve(cursor, component); if ((await lstat(cursor)).isSymbolicLink()) throw denied(); }
        if (await realpath(path) !== path) throw denied();
        handle = await open(path, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
        const before = await handle.stat({ bigint: true });
        if (!before.isFile() || before.nlink !== 1n || before.size > BigInt(maxBytes)) throw denied();
        const buffer = Buffer.alloc(maxBytes + 1);
        const { bytesRead } = await handle.read(buffer, 0, buffer.length, 0);
        const after = await handle.stat({ bigint: true });
        const current = await lstat(path, { bigint: true });
        if (signal?.aborted || BigInt(bytesRead) !== before.size || bytesRead > maxBytes || before.dev !== current.dev || before.ino !== current.ino || before.size !== after.size || before.mtimeNs !== after.mtimeNs || before.ctimeNs !== after.ctimeNs || await realpath(path) !== path) throw denied();
        const text = new TextDecoder("utf-8", { fatal: true }).decode(buffer.subarray(0, bytesRead));
        return { content: [{ type: "text", text }], details: { bytes: bytesRead, path: relative(root, path) } };
      } catch { throw denied(); } finally { await handle?.close(); }
    }
  };
}

/** Empty-input coordinator callback: the host, never the model, selects its one file. */
export function createBoundPiReadTool(options: { canonicalRoot: string; tool: import("@chirality/runtime-contracts").RuntimeToolDefinition; protectedPaths: readonly string[]; isCurrent(): boolean; signal: AbortSignal; maxBytes?: number }): ToolDefinition {
  const tool = options.tool, maxBytes = options.maxBytes ?? 1048576;
  const schema = tool.inputSchema as Record<string, any>;
  if (tool.name !== "read_file" || tool.permission.effect !== "allow" || tool.permission.operation !== "read" || tool.permission.roots?.length !== 1 || schema.type !== "object" || !schema.properties || Object.keys(schema.properties).length !== 0 || schema.additionalProperties !== false || (schema.required !== undefined && (!Array.isArray(schema.required) || schema.required.length !== 0)) || Object.keys(schema).some(key => !["type", "properties", "additionalProperties", "required"].includes(key))) throw denied();
  const root = options.canonicalRoot, path = tool.permission.roots[0]!;
  if (!isAbsolute(path) || resolve(path) !== path || !inside(root, path) || path === root || options.protectedPaths.some(protectedPath => inside(protectedPath, path))) throw denied();
  return {
    name: "read_file", label: "Read the authorized manager file", description: "Read the one file already selected by the governing manager. No arguments or alternate paths are accepted.", parameters: Type.Object({}, { additionalProperties: false }),
    async execute(_id, args, signal) {
      if (!args || typeof args !== "object" || Array.isArray(args) || Object.keys(args).length !== 0 || !options.isCurrent() || options.signal.aborted || signal?.aborted || await realpath(root) !== root) throw denied();
      let cursor = root;
      for (const component of relative(root, path).split(sep)) { cursor = resolve(cursor, component); if ((await lstat(cursor)).isSymbolicLink()) throw denied(); }
      const metadata = await lstat(path);
      if (await realpath(path) !== path || !metadata.isFile() || metadata.nlink !== 1 || metadata.size > maxBytes) throw denied();
      // The actual coordinator callback performs the read and records its receipt.
      // This bridge never manufactures permission/read completion evidence.
      const combinedSignal = signal ? AbortSignal.any([signal, options.signal]) : options.signal;
      const result = await new Promise<unknown>((resolveResult, reject) => {
        const aborted = () => reject(denied());
        if (combinedSignal.aborted) { aborted(); return; }
        combinedSignal.addEventListener("abort", aborted, { once: true });
        Promise.resolve().then(() => { if (combinedSignal.aborted) throw denied(); return tool.execute({}, combinedSignal); }).then(resolveResult, reject).finally(() => combinedSignal.removeEventListener("abort", aborted)).catch(() => {});
      });
      if (!options.isCurrent() || options.signal.aborted || signal?.aborted || !result || typeof result !== "object" || typeof (result as { content?: unknown }).content !== "string") throw denied();
      const text = (result as { content: string }).content;
      if (Buffer.byteLength(text) > maxBytes) throw denied();
      return { content: [{ type: "text", text }], details: { bytes: Buffer.byteLength(text), source: "bound-runtime-callback" } };
    }
  };
}
