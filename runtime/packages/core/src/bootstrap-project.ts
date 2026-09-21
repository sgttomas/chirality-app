import { randomUUID } from "node:crypto";
import { constants } from "node:fs";
import { link, lstat, open, realpath, unlink } from "node:fs/promises";
import { basename, isAbsolute, join, parse, resolve } from "node:path";
import { RuntimeError, type ChiralityProjectManifestV2 } from "@chirality/runtime-contracts";

export const HOSTED_PROJECT_MANIFEST_NAME = "chirality.project.json";

/**
 * Resolves an existing manifest or atomically creates the minimal hosted v2
 * manifest. It never replaces an existing directory entry.
 */
export async function ensureHostedProjectManifest(projectRoot: string): Promise<string> {
  if (typeof projectRoot !== "string" || projectRoot.trim() === "" || !isAbsolute(projectRoot) || resolve(projectRoot) !== projectRoot || projectRoot === parse(projectRoot).root) {
    throw new RuntimeError("INVALID_REQUEST", "projectRoot must be a normalized absolute non-root path");
  }
  let rootMetadata;
  try {
    rootMetadata = await lstat(projectRoot);
  } catch (error) {
    throw new RuntimeError("INVALID_REQUEST", "projectRoot must be an existing directory", 400, {
      cause: error instanceof Error ? error.message : "unavailable"
    });
  }
  if (!rootMetadata.isDirectory() || rootMetadata.isSymbolicLink()) {
    throw new RuntimeError("INVALID_REQUEST", "projectRoot must be a regular directory");
  }
  const canonicalRoot = await realpath(projectRoot);
  if (canonicalRoot !== projectRoot) throw new RuntimeError("INVALID_REQUEST", "projectRoot must not contain symbolic-link aliases");
  const manifestPath = join(canonicalRoot, HOSTED_PROJECT_MANIFEST_NAME);
  const existing = await lstat(manifestPath).catch((error: NodeJS.ErrnoException) => {
    if (error.code === "ENOENT") return undefined;
    throw error;
  });
  if (existing !== undefined) {
    if (!existing.isFile() || existing.isSymbolicLink()) {
      throw new RuntimeError("PROJECT_MANIFEST_INVALID", "Existing project manifest must be a regular nonsymlink file");
    }
    return manifestPath;
  }

  const displayName = basename(canonicalRoot) || "Chirality Project";
  const manifest: ChiralityProjectManifestV2 = {
    schemaVersion: "chirality.project/v2",
    projectId: randomUUID(),
    displayName,
    workingRoot: ".",
    instructionRoot: { mode: "runtime" },
    defaultExecutionRoot: ".",
    profiles: { domain: [], capability: [], dataBoundary: [] },
    enabledAdapterIds: ["codex-app-server"],
    embeddedUi: { declared: false }
  };
  const temporaryPath = join(canonicalRoot, `.${HOSTED_PROJECT_MANIFEST_NAME}.${process.pid}.${randomUUID()}.tmp`);
  const noFollow = constants.O_NOFOLLOW ?? 0;
  let handle;
  try {
    handle = await open(temporaryPath, constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY | noFollow, 0o600);
    try {
      await handle.writeFile(`${JSON.stringify(manifest, null, 2)}\n`, "utf8");
      await handle.sync();
    } finally {
      await handle.close();
    }
    const currentRoot = await lstat(canonicalRoot);
    if (!currentRoot.isDirectory() || currentRoot.isSymbolicLink() || currentRoot.dev !== rootMetadata.dev || currentRoot.ino !== rootMetadata.ino || await realpath(canonicalRoot) !== canonicalRoot) {
      throw new RuntimeError("INVALID_REQUEST", "projectRoot changed during initialization");
    }
    await link(temporaryPath, manifestPath);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "EEXIST") throw error;
    const raced = await lstat(manifestPath);
    if (!raced.isFile() || raced.isSymbolicLink()) {
      throw new RuntimeError("PROJECT_MANIFEST_INVALID", "Existing project manifest must be a regular nonsymlink file");
    }
  } finally {
    await unlink(temporaryPath).catch(() => undefined);
  }
  return manifestPath;
}
