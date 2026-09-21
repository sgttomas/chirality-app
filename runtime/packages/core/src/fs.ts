import { createHash, randomUUID } from "node:crypto";
import { chmod, mkdir, open, readFile, realpath, rename, rm, stat } from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";

export async function ensurePrivateDirectory(path: string): Promise<void> {
  await mkdir(path, { recursive: true, mode: 0o700 });
  await chmod(path, 0o700);
}

export async function atomicWriteJson(path: string, value: unknown): Promise<void> {
  await ensurePrivateDirectory(dirname(path));
  const temporary = `${path}.${process.pid}.${randomUUID()}.tmp`;
  const handle = await open(temporary, "wx", 0o600);
  try {
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`, "utf8");
    await handle.sync();
  } finally {
    await handle.close();
  }
  await rename(temporary, path);
  await chmod(path, 0o600);
}

export async function appendJsonLine(path: string, value: unknown): Promise<void> {
  await ensurePrivateDirectory(dirname(path));
  const handle = await open(path, "a", 0o600);
  try {
    await handle.appendFile(`${JSON.stringify(value)}\n`, "utf8");
    await handle.sync();
  } finally {
    await handle.close();
  }
  await chmod(path, 0o600);
}

export async function readJson<T>(path: string): Promise<T> {
  return JSON.parse(await readFile(path, "utf8")) as T;
}

export async function readJsonIfExists<T>(path: string, fallback: T): Promise<T> {
  try {
    return await readJson<T>(path);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return fallback;
    throw error;
  }
}

export async function exists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw error;
  }
}

export function sha256(value: string | Buffer): string {
  return createHash("sha256").update(value).digest("hex");
}

export function assertSafeIdentifier(value: string, label: string): void {
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(value)) {
    throw new Error(`${label} is not a safe identifier`);
  }
}

export function assertRelativeManifestPath(value: string, label: string): void {
  if (value.length === 0 || isAbsolute(value)) {
    throw new Error(`${label} must be a non-empty relative path`);
  }
}

export function isContained(root: string, candidate: string): boolean {
  const rel = relative(root, candidate);
  return rel === "" || (!(rel === ".." || rel.startsWith(`..${sep}`)) && !isAbsolute(rel));
}

export async function resolveContained(root: string, child: string): Promise<string> {
  const canonicalRoot = await realpath(root);
  const candidate = resolve(canonicalRoot, child);
  const canonical = await realpath(candidate);
  const rel = relative(canonicalRoot, canonical);
  if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
    throw new Error(`Path escapes project root: ${child}`);
  }
  return canonical;
}

export async function removeIfExists(path: string): Promise<void> {
  await rm(path, { force: true });
}

// Private record helpers shared by the retirement journal and the daemon
// composition. They reject aliases before writing and keep records owner-only.
import { constants as fsConstants } from "node:fs";
import { link, lstat, open as openFile, realpath as realpathFs, rename as renameFs, unlink } from "node:fs/promises";
import { join as joinPath, parse as parsePath } from "node:path";
import { RuntimeError, type WorkerContinuity } from "@chirality/runtime-contracts";

const forbidden = (message: string) => new RuntimeError("FORBIDDEN", message, 403);
export function recordKey(value: unknown): string {
  return createHash("sha256").update(JSON.stringify(value)).digest("hex");
}
export function continuityFields(value: WorkerContinuity): readonly unknown[] {
  return [value.canonicalRoot, value.accountId, value.accountEpoch, value.policyDigest, value.cwd];
}
export function sameContinuity(a: WorkerContinuity, b: WorkerContinuity): boolean {
  return JSON.stringify(continuityFields(a)) === JSON.stringify(continuityFields(b));
}
export function validContinuity(value: WorkerContinuity): boolean {
  return Boolean(value && typeof value.canonicalRoot === "string" && isAbsolute(value.canonicalRoot)
    && resolve(value.canonicalRoot) === value.canonicalRoot && value.cwd === value.canonicalRoot
    && typeof value.accountId === "string" && value.accountId.trim()
    && Number.isSafeInteger(value.accountEpoch) && value.accountEpoch >= 0
    && typeof value.policyDigest === "string" && value.policyDigest.trim());
}
export async function assertContinuity(value: WorkerContinuity): Promise<void> {
  if (!validContinuity(value)) throw forbidden("Invalid root/account/epoch/policy/cwd continuity");
  try {
    if (await realpathFs(value.canonicalRoot) !== value.canonicalRoot || !(await lstat(value.canonicalRoot)).isDirectory()) {
      throw forbidden("Root must be the canonical directory and cwd must equal it");
    }
  } catch (error) {
    if (error instanceof RuntimeError) throw error;
    throw forbidden("Canonical root is unavailable");
  }
}
/** Private app-owned directories; reject aliases before writing or chmodding anything. */
export async function privateDirectory(directory: string): Promise<void> {
  if (!isAbsolute(directory) || resolve(directory) !== directory) throw forbidden("Private directory must be canonical and absolute");
  let current = parsePath(directory).root;
  for (const segment of directory.slice(current.length).split(sep).filter(Boolean)) {
    current = joinPath(current, segment);
    try { await mkdir(current, { mode: 0o700 }); } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw forbidden("Cannot create private storage");
    }
    const info = await lstat(current);
    if (!info.isDirectory() || info.isSymbolicLink()) throw forbidden("Private storage cannot traverse symlinks");
  }
  const info = await lstat(directory);
  if ((info.mode & 0o077) !== 0 || (process.getuid && info.uid !== process.getuid())) throw forbidden("Storage must be owner-private (0700)");
}
export async function syncDirectory(directory: string): Promise<void> {
  const handle = await openFile(directory, fsConstants.O_RDONLY | fsConstants.O_NOFOLLOW);
  try { await handle.sync(); } finally { await handle.close(); }
}
export async function privateRead<T>(file: string): Promise<T | undefined> {
  let handle;
  try {
    handle = await openFile(file, fsConstants.O_RDONLY | fsConstants.O_NOFOLLOW);
    const info = await handle.stat();
    if (!info.isFile() || (info.mode & 0o077) !== 0 || (process.getuid && info.uid !== process.getuid())) throw forbidden("Record must be an owner-private regular file");
    return JSON.parse(await handle.readFile("utf8")) as T;
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return undefined;
    if (error instanceof RuntimeError) throw error;
    throw new RuntimeError("INTERNAL_FAILURE", "Private record is unreadable or malformed", 500);
  } finally { await handle?.close(); }
}
/** fsync bytes before publication, then directory. Exclusive link is cross-process CAS. */
export async function publishPrivate(file: string, value: unknown, exclusive: boolean): Promise<boolean> {
  await privateDirectory(dirname(file));
  const temp = `${file}.${randomUUID()}.tmp`;
  const handle = await openFile(temp, fsConstants.O_WRONLY | fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_NOFOLLOW, 0o600);
  try { await handle.writeFile(`${JSON.stringify(value)}\n`); await handle.sync(); } finally { await handle.close(); }
  try {
    if (exclusive) {
      try { await link(temp, file); } catch (error) {
        if ((error as NodeJS.ErrnoException).code === "EEXIST") {
          // Another publisher may not yet have synced the directory.
          await syncDirectory(dirname(file));
          return false;
        }
        throw error;
      }
    } else {
      // Refuse a pre-existing malicious alias even though rename itself does not follow it.
      await privateRead(file);
      await renameFs(temp, file);
    }
    await syncDirectory(dirname(file));
    return true;
  } finally { await unlink(temp).catch(error => { if (error.code !== "ENOENT") throw error; }); }
}
