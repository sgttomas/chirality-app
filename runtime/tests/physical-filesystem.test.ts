import { createHash } from "node:crypto";
import * as ordinary from "node:fs/promises";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { selectRuntimePhysicalFilesystemForTests } from "../packages/core/src/physical-filesystem.js";

const roots: string[] = [];
afterEach(async () => { while (roots.length) await rm(roots.pop()!, { recursive: true, force: true }); });

describe("physical filesystem observation adapter", () => {
  it("uses ordinary Node promises outside Electron", () => {
    const requireBuiltin = vi.fn(() => { throw new Error("must remain unused"); });
    const selected = selectRuntimePhysicalFilesystemForTests({ electron: false, requireBuiltin, nodeFilesystem: ordinary });
    expect(selected.open).toBe(ordinary.open); expect(selected.lstat).toBe(ordinary.lstat); expect(selected.readdir).toBe(ordinary.readdir);
    expect(requireBuiltin).not.toHaveBeenCalled();
  });

  it("selects Electron original-fs and observes an archive root as one physical file", async () => {
    const root = await ordinary.realpath(await mkdtemp(join(tmpdir(), "physical-asar-"))); roots.push(root);
    const path = join(root, "app.asar"), content = Buffer.from("physical archive root bytes"); await writeFile(path, content);
    const patched = { ...ordinary, open: vi.fn(async () => { const error = new Error("virtual archive root") as NodeJS.ErrnoException; error.code = "ENOENT"; throw error; }),
      lstat: vi.fn(async () => ({ isFile: () => false, isDirectory: () => true })) };
    const requireBuiltin = vi.fn((id: string) => id === "original-fs" ? { promises: ordinary } : undefined);
    const selected = selectRuntimePhysicalFilesystemForTests({ electron: true, requireBuiltin, nodeFilesystem: patched });
    expect(requireBuiltin).toHaveBeenCalledWith("original-fs");
    expect((await selected.lstat(path)).isFile()).toBe(true); expect(await selected.realpath(path)).toBe(path);
    const handle = await selected.open(path, "r");
    try {
      const before = await handle.stat({ bigint: true }), bytes = Buffer.alloc(content.length); expect((await handle.read(bytes, 0, bytes.length, 0)).bytesRead).toBe(content.length);
      const after = await handle.stat({ bigint: true }); expect(bytes).toEqual(content); expect([before.dev, before.ino, before.size, before.mtimeNs, before.ctimeNs]).toEqual([after.dev, after.ino, after.size, after.mtimeNs, after.ctimeNs]);
    } finally { await handle.close(); }
    expect(await selected.readdir(root)).toEqual(["app.asar"]); expect(patched.open).not.toHaveBeenCalled(); expect(patched.lstat).not.toHaveBeenCalled();
  });

  it("fails closed when Electron original-fs or one required promise operation is unavailable", () => {
    expect(() => selectRuntimePhysicalFilesystemForTests({ electron: true, requireBuiltin() { throw new Error("missing"); }, nodeFilesystem: ordinary })).toThrow("Electron physical filesystem");
    expect(() => selectRuntimePhysicalFilesystemForTests({ electron: true, requireBuiltin: () => ({ promises: { ...ordinary, open: undefined } }), nodeFilesystem: ordinary })).toThrow("Physical filesystem");
  });
});
