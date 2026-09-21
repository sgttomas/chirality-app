import { mkdir, mkdtemp, readFile, realpath, rm, symlink, writeFile } from "node:fs/promises";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, expect, it, vi } from "vitest";

const fsCalls = vi.hoisted(() => ({ open: vi.fn(), realpath: vi.fn() }));
vi.mock("node:fs/promises", async importOriginal => {
  const fs = await importOriginal<typeof import("node:fs/promises")>();
  fsCalls.open.mockImplementation(fs.open); fsCalls.realpath.mockImplementation(fs.realpath);
  return { ...fs, open: fsCalls.open, realpath: fsCalls.realpath };
});
import { RuntimeAttachmentResolver } from "../packages/core/src/runtime-attachment-resolver.js";
import { captureAttachmentDirectory, readAttachmentBytes, writeAttachmentCopy } from "../packages/core/src/attachment-copy.js";

const roots: string[] = [];
afterEach(async () => { await Promise.all(roots.splice(0).map(root => rm(root, { recursive: true, force: true }))); });
async function fixture() {
  const root = await realpath(await mkdtemp(join(tmpdir(), "attachment-boundary-"))); roots.push(root);
  const projectRoot = join(root, "project"); const otherProject = join(root, "other");
  await mkdir(projectRoot); await mkdir(otherProject);
  const inside = join(projectRoot, "inside.txt"); const outside = join(otherProject, "outside.txt");
  await writeFile(inside, "Inside"); await writeFile(outside, "Outside");
  return { root, projectRoot, otherProject, inside, outside, context: { projectRoot, projectId: "project", sessionId: "session" } };
}
it('rejects forged outside raw sources before opening or resolving any source in the batch', async () => {
  const f = await fixture(); fsCalls.open.mockClear(); fsCalls.realpath.mockClear();
  await expect(new RuntimeAttachmentResolver().resolveAttachmentsToContentBlocks("message", [f.inside, f.outside], f.context)).rejects.toMatchObject({ code: "FORBIDDEN" });
  expect(fsCalls.open).not.toHaveBeenCalled();
  expect(fsCalls.realpath).not.toHaveBeenCalled();
});
it('rejects another project’s staged copy and contained symlink aliases', async () => {
  const f = await fixture();
  const otherInput = join(f.otherProject, ".chirality", "attachment-inputs", "host-random"); await mkdir(otherInput, { recursive: true });
  const copy = join(otherInput, "brief.txt"); await writeFile(copy, "Other project copy");
  fsCalls.open.mockClear();
  await expect(new RuntimeAttachmentResolver().resolveAttachmentsToContentBlocks("message", [copy], f.context)).rejects.toMatchObject({ code: "FORBIDDEN" });
  expect(fsCalls.open).not.toHaveBeenCalled();
  const alias = join(f.projectRoot, "alias.txt"); await symlink(f.outside, alias);
  await expect(new RuntimeAttachmentResolver().resolveAttachmentsToContentBlocks("message", [alias], f.context)).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  expect(fsCalls.open.mock.calls.some(([file]) => file === alias || file === f.outside)).toBe(false);
});
it('publishes identical bytes idempotently and never overwrites a different existing copy', async () => {
  const f = await fixture(); const guard = await captureAttachmentDirectory(f.projectRoot);
  const bytes = await readAttachmentBytes(f.inside, { bytes: 0 });
  const first = await writeAttachmentCopy(f.projectRoot, "copy.txt", bytes, guard);
  expect(await writeAttachmentCopy(f.projectRoot, "copy.txt", bytes, guard)).toBe(first);
  await writeFile(first, "Altered");
  await expect(writeAttachmentCopy(f.projectRoot, "copy.txt", bytes, guard)).rejects.toMatchObject({ code: "FORBIDDEN" });
  expect(await readFile(first, "utf8")).toBe("Altered");
});

it('rejects special source and existing destination files before opening them', async () => {
  const f = await fixture();
  const sourceFifo = join(f.projectRoot, "source.txt");
  const destinationFifo = join(f.projectRoot, "destination.txt");
  execFileSync("mkfifo", [sourceFifo, destinationFifo]);
  fsCalls.open.mockClear();
  await expect(readAttachmentBytes(sourceFifo, { bytes: 0 })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  expect(fsCalls.open).not.toHaveBeenCalled();
  const bytes = await readAttachmentBytes(f.inside, { bytes: 0 });
  const guard = await captureAttachmentDirectory(f.projectRoot);
  fsCalls.open.mockClear();
  await expect(writeAttachmentCopy(f.projectRoot, "destination.txt", bytes, guard)).rejects.toMatchObject({ code: "FORBIDDEN" });
  expect(fsCalls.open.mock.calls.some(([file]) => file === destinationFifo)).toBe(false);
});
