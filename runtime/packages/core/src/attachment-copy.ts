import { createHash, randomUUID } from "node:crypto";
import { constants } from "node:fs";
import { lstat, link, mkdir, open, realpath, unlink } from "node:fs/promises";
import { basename, extname, isAbsolute, join, resolve } from "node:path";
import { RuntimeError } from "@chirality/runtime-contracts";
import { isContained } from "./fs.js";

const MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024;
const MAX_TOTAL_ATTACHMENT_BYTES = 18 * 1024 * 1024;
const MIME_BY_EXTENSION: Readonly<Record<string, string>> = {
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
  ".pdf": "application/pdf", ".txt": "text/plain", ".md": "text/markdown", ".csv": "text/csv"
};
export type AttachmentBytes = { name: string; extension: string; mimeType: string; bytes: Buffer; sha256: string };
export type AttachmentBudget = { bytes: number };
export function assertAttachmentCount(paths: readonly string[]): void {
  if (paths.length > 8) throw new RuntimeError("INVALID_REQUEST", "At most eight attachments are supported");
}
export function assertAttachmentSourcePath(sourcePath: string, trustedRoot?: string): void {
  if (typeof sourcePath !== "string" || !isAbsolute(sourcePath) || resolve(sourcePath) !== sourcePath || /[\x00-\x1f]/u.test(sourcePath)) throw new RuntimeError("INVALID_REQUEST", "Attachment path must be normalized and absolute");
  // This lexical check precedes all source filesystem access. Canonical/symlink
  // checks below prevent a contained lexical path from resolving outside.
  if (trustedRoot !== undefined && !isContained(trustedRoot, sourcePath)) throw new RuntimeError("FORBIDDEN", "Attachment source is outside the project folder", 403);
}

/** Capture a real directory identity; the returned guard rejects replacement. */
export async function captureAttachmentDirectory(directory: string): Promise<() => Promise<void>> {
  if (!isAbsolute(directory) || resolve(directory) !== directory) throw new RuntimeError("FORBIDDEN", "Attachment directory must be canonical", 403);
  const identity = await lstat(directory);
  if (!identity.isDirectory() || identity.isSymbolicLink() || await realpath(directory) !== directory) throw new RuntimeError("FORBIDDEN", "Attachment staging directory is unsafe", 403);
  return async () => {
    const current = await lstat(directory);
    if (!current.isDirectory() || current.isSymbolicLink() || current.dev !== identity.dev || current.ino !== identity.ino || await realpath(directory) !== directory) throw new RuntimeError("FORBIDDEN", "Attachment staging directory changed during resolution", 403);
  };
}
export async function ensureAttachmentDirectory(directory: string): Promise<() => Promise<void>> {
  await mkdir(directory, { mode: 0o700 }).catch((error: NodeJS.ErrnoException) => { if (error.code !== "EEXIST") throw error; });
  return captureAttachmentDirectory(directory);
}

/** Shared source validation for native selection copies and final turn custody. */
export async function readAttachmentBytes(sourcePath: string, budget: AttachmentBudget): Promise<AttachmentBytes> {
  assertAttachmentSourcePath(sourcePath);
  const extension = extname(sourcePath).toLowerCase();
  const mimeType = MIME_BY_EXTENSION[extension];
  if (mimeType === undefined) throw new RuntimeError("INVALID_REQUEST", `Unsupported attachment extension: ${extension || "(none)"}`);
  const sourceRealPath = await realpath(sourcePath).catch(() => undefined);
  if (sourceRealPath !== sourcePath) throw new RuntimeError("INVALID_REQUEST", "Attachment path must not contain symbolic-link aliases");
  const selectedIdentity = await lstat(sourcePath);
  if (!selectedIdentity.isFile() || selectedIdentity.isSymbolicLink()) throw new RuntimeError("INVALID_REQUEST", "Attachment path must reference a regular file");
  const source = await open(sourcePath, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0)).catch(() => undefined);
  if (!source) throw new RuntimeError("INVALID_REQUEST", "Attachment file is not readable");
  try {
    const before = await source.stat();
    const currentIdentity = await lstat(sourcePath);
    if (currentIdentity.isSymbolicLink() || currentIdentity.dev !== before.dev || currentIdentity.ino !== before.ino || selectedIdentity.dev !== before.dev || selectedIdentity.ino !== before.ino || await realpath(sourcePath) !== sourcePath) throw new RuntimeError("INVALID_REQUEST", "Attachment source changed before reading");
    if (!before.isFile()) throw new RuntimeError("INVALID_REQUEST", "Attachment path must reference a regular file");
    if (before.size > MAX_ATTACHMENT_BYTES) throw new RuntimeError("INVALID_REQUEST", "Attachment exceeds the per-file size limit");
    if (budget.bytes + before.size > MAX_TOTAL_ATTACHMENT_BYTES) throw new RuntimeError("INVALID_REQUEST", "Attachments exceed the per-turn size limit");
    const bytes = await source.readFile();
    const after = await source.stat();
    if (after.dev !== before.dev || after.ino !== before.ino || after.size !== before.size || after.mtimeMs !== before.mtimeMs || bytes.byteLength !== before.size) throw new RuntimeError("INVALID_REQUEST", "Attachment changed during staging");
    budget.bytes += bytes.byteLength;
    return { name: basename(sourcePath), extension, mimeType, bytes, sha256: createHash("sha256").update(bytes).digest("hex") };
  } finally { await source.close(); }
}

/** Atomically publish a checked copy without overwriting existing different bytes. */
export async function writeAttachmentCopy(directory: string, name: string, attachment: AttachmentBytes, revalidate: () => Promise<void>): Promise<string> {
  if (!name || basename(name) !== name || name === "." || name === "..") throw new RuntimeError("INVALID_REQUEST", "Invalid attachment copy name");
  const stagedPath = join(directory, name);
  const temporaryPath = join(directory, `.${randomUUID()}.tmp`);
  await revalidate();
  try {
    const temporary = await open(temporaryPath, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY | (constants.O_NOFOLLOW ?? 0), 0o600);
    try { await temporary.writeFile(attachment.bytes); await temporary.sync(); }
    finally { await temporary.close(); }
    await revalidate();
    await link(temporaryPath, stagedPath).catch(async (error: NodeJS.ErrnoException) => {
      if (error.code !== "EEXIST") throw error;
      const existingIdentity = await lstat(stagedPath);
      if (!existingIdentity.isFile() || existingIdentity.isSymbolicLink()) throw new RuntimeError("FORBIDDEN", "Existing staged attachment is not a regular file", 403);
      const existing = await open(stagedPath, constants.O_RDONLY | (constants.O_NOFOLLOW ?? 0));
      try {
        const metadata = await existing.stat();
        if (!metadata.isFile() || metadata.dev !== existingIdentity.dev || metadata.ino !== existingIdentity.ino || metadata.size !== attachment.bytes.byteLength || createHash("sha256").update(await existing.readFile()).digest("hex") !== attachment.sha256) throw new RuntimeError("FORBIDDEN", "Existing staged attachment does not match its immutable content identity", 403);
      } finally { await existing.close(); }
    });
    await revalidate();
    return stagedPath;
  } finally { await unlink(temporaryPath).catch(() => undefined); }
}
