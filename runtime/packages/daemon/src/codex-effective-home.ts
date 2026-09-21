import { lstat, mkdir, readdir, readlink, stat, symlink, unlink, chmod } from "node:fs/promises";
import { isAbsolute, join, resolve } from "node:path";
import { RuntimeError } from "@chirality/runtime-contracts";

/**
 * Effective Codex home (SPIKE_DESIGN section 3). The directory shares the
 * user's `~/.codex` entries by reference through same-named symlinks, except
 * the credential and models-cache files, which stay private to Chirality and
 * are created by Codex itself after a Chirality sign-in. Nothing is ever
 * created, copied, moved or written inside the user's home, and `auth.json`
 * is never opened.
 */
export interface CodexEffectiveHomeOptions {
  /** The user's Codex home (`~/.codex`); a missing directory yields an empty overlay. */
  userCodexHome: string;
  /** `<runtimeDirectory>/codex-home`, created 0700. */
  effectiveHome: string;
}
export interface CodexEffectiveHomeReport {
  effectiveHome: string;
  userCodexHome: string;
  userHomePresent: boolean;
  /** Entry names linked or refreshed this run. */
  linked: readonly string[];
  /** Entry names deliberately excluded from sharing. */
  excluded: readonly string[];
  /** Dangling overlay symlinks removed this run. */
  removed: readonly string[];
  /** Overlay entries that are not symlinks and were left untouched. */
  retained: readonly string[];
}

export function isExcludedCodexHomeEntry(name: string): boolean {
  return name === "auth.json" || name === "models_cache.json" || name.startsWith("auth") || name.endsWith(".lock");
}

function absolute(value: string, label: string): void {
  if (typeof value !== "string" || !isAbsolute(value) || resolve(value) !== value || /[\x00-\x1f]/.test(value)) throw new RuntimeError("INVALID_REQUEST", `${label} must be a normalized absolute path`);
}

export async function prepareCodexEffectiveHome(options: CodexEffectiveHomeOptions): Promise<CodexEffectiveHomeReport> {
  absolute(options.userCodexHome, "User Codex home");
  absolute(options.effectiveHome, "Effective Codex home");
  if (options.effectiveHome === options.userCodexHome) throw new RuntimeError("INVALID_REQUEST", "Effective Codex home must differ from the user's Codex home");
  await mkdir(options.effectiveHome, { recursive: true, mode: 0o700 });
  await chmod(options.effectiveHome, 0o700);
  const overlay = await lstat(options.effectiveHome);
  if (!overlay.isDirectory() || overlay.isSymbolicLink()) throw new RuntimeError("FORBIDDEN", "Effective Codex home must be a private directory, not an alias", 403);

  let userEntries: string[] = [];
  let userHomePresent = false;
  try {
    const info = await lstat(options.userCodexHome);
    if (info.isDirectory() || info.isSymbolicLink()) { userEntries = await readdir(options.userCodexHome); userHomePresent = true; }
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "ENOENT" && (error as NodeJS.ErrnoException).code !== "ENOTDIR") throw error;
  }

  const linked: string[] = [], excluded: string[] = [], removed: string[] = [], retained: string[] = [];
  const wanted = new Map<string, string>();
  for (const name of userEntries) {
    if (name === "." || name === "..") continue;
    if (isExcludedCodexHomeEntry(name)) { excluded.push(name); continue; }
    wanted.set(name, join(options.userCodexHome, name));
  }

  // Refresh existing overlay entries first: relink stale symlinks, drop dangling ones,
  // and never touch regular files or directories Codex created in the overlay.
  for (const name of await readdir(options.effectiveHome)) {
    const path = join(options.effectiveHome, name);
    const info = await lstat(path);
    if (!info.isSymbolicLink()) { retained.push(name); wanted.delete(name); continue; }
    const target = wanted.get(name);
    const current = await readlink(path).catch(() => undefined);
    if (target !== undefined) {
      if (current !== target) { await unlink(path); await symlink(target, path); }
      linked.push(name);
      wanted.delete(name);
      continue;
    }
    const alive = await stat(path).then(() => true, () => false);
    if (!alive || isExcludedCodexHomeEntry(name)) { await unlink(path); removed.push(name); }
    else retained.push(name);
  }
  for (const [name, target] of wanted) {
    await symlink(target, join(options.effectiveHome, name));
    linked.push(name);
  }
  return { effectiveHome: options.effectiveHome, userCodexHome: options.userCodexHome, userHomePresent, linked: linked.sort(), excluded: excluded.sort(), removed: removed.sort(), retained: retained.sort() };
}
