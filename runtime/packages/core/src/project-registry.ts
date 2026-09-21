import { randomUUID } from "node:crypto";
import { access, readFile, realpath, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { dirname, join, resolve } from "node:path";
import {
  RuntimeError,
  CHIRALITY_INSTRUCTION_ROOT_ENV,
  type ChiralityProjectManifest,
  type ChiralityProjectManifestV1,
  type ChiralityProjectManifestV2,
  type ProjectStatus,
  type RegisteredProject
} from "@chirality/runtime-contracts";
import {
  assertRelativeManifestPath,
  assertSafeIdentifier,
  atomicWriteJson,
  isContained,
  readJsonIfExists,
  sha256
} from "./fs.js";

interface RegistryFile {
  schemaVersion: "chirality.project-registry/v1";
  projects: RegisteredProject[];
}

export class ProjectRegistry {
  private readonly registryFile: string;

  constructor(
    private readonly runtimeDirectory: string,
    private readonly environment: Readonly<Record<string, string | undefined>> = process.env
  ) {
    this.registryFile = join(runtimeDirectory, "projects", "registry.json");
  }

  async register(
    manifestPath: string,
    approval: RegisteredProject["approval"],
    clientId: string | ((projectId: string) => string) = `project-${randomUUID()}`
  ): Promise<RegisteredProject> {
    const canonicalManifest = await realpath(manifestPath);
    const source = await readFile(canonicalManifest, "utf8");
    const manifest = this.parseManifest(source);
    const manifestDirectory = await realpath(dirname(canonicalManifest));
    const { workingRoot: canonicalRoot } = await this.validateReferences(
      manifestDirectory,
      manifest
    );
    const registry = await this.readRegistry();
    const record: RegisteredProject = {
      projectId: manifest.projectId,
      displayName: manifest.displayName,
      canonicalRoot,
      manifestPath: canonicalManifest,
      manifestHash: sha256(source),
      registeredAt: new Date().toISOString(),
      approval,
      clientId: typeof clientId === "function" ? clientId(manifest.projectId) : clientId,
      enabledAdapterIds: [...manifest.enabledAdapterIds],
      legacySessionRoots: [...(manifest.legacySessionRoots ?? [])]
    };
    await this.writeRegistry({
      ...registry,
      projects: [...registry.projects.filter((item) => item.projectId !== record.projectId), record]
    });
    return record;
  }

  async list(): Promise<readonly ProjectStatus[]> {
    const registry = await this.readRegistry();
    return Promise.all(registry.projects.map(async (project) => this.status(project.projectId)));
  }

  async status(projectId: string): Promise<ProjectStatus> {
    const project = await this.getRecord(projectId);
    const source = await readFile(project.manifestPath, "utf8").catch(() => "");
    const manifestDrift = sha256(source) !== project.manifestHash;
    return { project, manifestDrift, adaptersEnabled: !manifestDrift };
  }

  async requireAuthorized(projectId: string): Promise<RegisteredProject> {
    const status = await this.status(projectId);
    if (status.manifestDrift) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_DRIFT",
        "The project manifest changed after approval; re-registration is required",
        409,
        { projectId }
      );
    }
    return status.project;
  }

  async readManifest(projectId: string): Promise<ChiralityProjectManifest> {
    const project = await this.getRecord(projectId);
    return this.parseManifest(await readFile(project.manifestPath, "utf8"));
  }

  async roots(projectId: string): Promise<{ workingRoot: string; instructionRoot: string }> {
    const project = await this.requireAuthorized(projectId);
    const manifest = await this.readManifest(projectId);
    const instructionRoot =
      manifest.schemaVersion === "chirality.project/v1"
        ? await realpath(resolve(dirname(project.manifestPath), manifest.instructionRoot))
        : await this.runtimeInstructionRoot();
    if (
      manifest.schemaVersion === "chirality.project/v2" &&
      (isContained(instructionRoot, project.canonicalRoot) ||
        isContained(project.canonicalRoot, instructionRoot))
    ) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Runtime instruction root must be disjoint from the working root"
      );
    }
    return {
      workingRoot: project.canonicalRoot,
      instructionRoot
    };
  }

  private async getRecord(projectId: string): Promise<RegisteredProject> {
    assertSafeIdentifier(projectId, "projectId");
    const registry = await this.readRegistry();
    const record = registry.projects.find((project) => project.projectId === projectId);
    if (record === undefined) {
      throw new RuntimeError("PROJECT_NOT_FOUND", `Unknown project: ${projectId}`, 404);
    }
    return record;
  }

  private parseManifest(source: string): ChiralityProjectManifest {
    let value: unknown;
    try {
      value = JSON.parse(source);
    } catch {
      throw new RuntimeError("PROJECT_MANIFEST_INVALID", "Project manifest is not valid JSON");
    }
    if (!this.isManifest(value)) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Project manifest does not conform to chirality.project/v1 or chirality.project/v2"
      );
    }
    return value;
  }

  private isManifest(value: unknown): value is ChiralityProjectManifest {
    if (typeof value !== "object" || value === null) return false;
    const item = value as Record<string, unknown>;
    const profiles = item["profiles"] as Record<string, unknown> | undefined;
    const embeddedUi = item["embeddedUi"] as Record<string, unknown> | undefined;
    return (
      (item["schemaVersion"] === "chirality.project/v1" ||
        item["schemaVersion"] === "chirality.project/v2") &&
      typeof item["projectId"] === "string" &&
      typeof item["displayName"] === "string" &&
      typeof item["workingRoot"] === "string" &&
      (item["schemaVersion"] === "chirality.project/v1"
        ? typeof item["instructionRoot"] === "string"
        : this.isRuntimeInstructionRoot(item["instructionRoot"])) &&
      typeof item["defaultExecutionRoot"] === "string" &&
      typeof profiles === "object" &&
      Array.isArray(profiles?.["domain"]) &&
      Array.isArray(profiles?.["capability"]) &&
      Array.isArray(profiles?.["dataBoundary"]) &&
      Array.isArray(item["enabledAdapterIds"]) &&
      typeof embeddedUi === "object" &&
      typeof embeddedUi?.["declared"] === "boolean"
    );
  }

  private isRuntimeInstructionRoot(value: unknown): value is ChiralityProjectManifestV2["instructionRoot"] {
    if (typeof value !== "object" || value === null || Array.isArray(value)) return false;
    const item = value as Record<string, unknown>;
    return item["mode"] === "runtime" && Object.keys(item).length === 1;
  }

  private async validateReferences(
    manifestDirectory: string,
    manifest: ChiralityProjectManifest
  ): Promise<{ workingRoot: string; instructionRoot: string }> {
    assertSafeIdentifier(manifest.projectId, "projectId");
    assertRelativeManifestPath(manifest.workingRoot, "workingRoot");
    const workingRoot = await this.canonicalizeReference(
      manifestDirectory,
      manifest.workingRoot,
      "workingRoot"
    );
    const instructionRoot =
      manifest.schemaVersion === "chirality.project/v1"
        ? await this.relativeInstructionRoot(manifestDirectory, manifest)
        : await this.runtimeInstructionRoot();
    const rootsOverlap =
      isContained(instructionRoot, workingRoot) || isContained(workingRoot, instructionRoot);
    if (manifest.schemaVersion === "chirality.project/v1" && !rootsOverlap) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Working and instruction roots must belong to one canonical project tree"
      );
    }
    if (manifest.schemaVersion === "chirality.project/v2" && rootsOverlap) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Runtime instruction root must be disjoint from the working root"
      );
    }
    const paths = [
      ["defaultExecutionRoot", manifest.defaultExecutionRoot],
      ...(manifest.agentsOverlay === undefined
        ? []
        : ([["agentsOverlay", manifest.agentsOverlay]] as const)),
      ...(manifest.embeddedUi.path === undefined
        ? []
        : ([["embeddedUi.path", manifest.embeddedUi.path]] as const)),
      ...manifest.profiles.domain.map((path) => ["profiles.domain", path] as const),
      ...manifest.profiles.capability.map((path) => ["profiles.capability", path] as const),
      ...manifest.profiles.dataBoundary.map((path) => ["profiles.dataBoundary", path] as const),
      ...(manifest.legacySessionRoots ?? []).map((path) => ["legacySessionRoots", path] as const)
    ];
    for (const [label, path] of paths) {
      assertRelativeManifestPath(path, label);
      // legacySessionRoots is read-if-present downstream: SessionStore.list()
      // and SessionStore.get() (session-store.ts, listLegacyCandidates /
      // migrateLegacy) only enumerate or migrate legacy sessions from roots
      // that actually exist, and treat an absent root as "no legacy sessions".
      // Registration therefore tolerates a missing legacySessionRoots entry
      // (its containment check is skipped while absent) but still rejects any
      // entry that exists and escapes the declared roots. Every other
      // reference must exist at registration time.
      const tolerateAbsence = label === "legacySessionRoots";
      const canonical = await this.canonicalizeReference(
        manifestDirectory,
        path,
        label,
        tolerateAbsence
      );
      if (canonical === undefined) continue;
      if (!isContained(workingRoot, canonical) && !isContained(instructionRoot, canonical)) {
        throw new RuntimeError(
          "PROJECT_MANIFEST_INVALID",
          `${label} escapes the declared working and instruction roots`
        );
      }
    }
    return { workingRoot, instructionRoot };
  }

  private async relativeInstructionRoot(
    manifestDirectory: string,
    manifest: ChiralityProjectManifestV1
  ): Promise<string> {
    assertRelativeManifestPath(manifest.instructionRoot, "instructionRoot");
    return this.canonicalizeReference(
      manifestDirectory,
      manifest.instructionRoot,
      "instructionRoot"
    );
  }

  private async runtimeInstructionRoot(): Promise<string> {
    const configured = this.environment[CHIRALITY_INSTRUCTION_ROOT_ENV]?.trim();
    if (!configured) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        `${CHIRALITY_INSTRUCTION_ROOT_ENV} is required for chirality.project/v2`
      );
    }
    let canonical: string;
    try {
      canonical = await realpath(resolve(configured));
      await access(canonical, constants.R_OK);
      if (!(await stat(canonical)).isDirectory()) {
        throw Object.assign(new Error("not a directory"), { code: "ENOTDIR" });
      }
    } catch (error) {
      const code = (error as NodeJS.ErrnoException).code;
      if (code !== "ENOENT" && code !== "ENOTDIR" && code !== "EACCES") throw error;
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        `${CHIRALITY_INSTRUCTION_ROOT_ENV} is not a readable directory: ${configured}`
      );
    }
    return canonical;
  }

  private async canonicalizeReference(
    manifestDirectory: string,
    relativePath: string,
    label: string,
    tolerateAbsence?: false
  ): Promise<string>;
  private async canonicalizeReference(
    manifestDirectory: string,
    relativePath: string,
    label: string,
    tolerateAbsence: boolean
  ): Promise<string | undefined>;
  private async canonicalizeReference(
    manifestDirectory: string,
    relativePath: string,
    label: string,
    tolerateAbsence = false
  ): Promise<string | undefined> {
    try {
      return await realpath(resolve(manifestDirectory, relativePath));
    } catch (error) {
      const code = (error as NodeJS.ErrnoException).code;
      if (code !== "ENOENT" && code !== "ENOTDIR") throw error;
      if (tolerateAbsence) return undefined;
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        `${label} references a path that does not exist: ${relativePath}`
      );
    }
  }

  private readRegistry(): Promise<RegistryFile> {
    return readJsonIfExists(this.registryFile, {
      schemaVersion: "chirality.project-registry/v1",
      projects: []
    });
  }

  private writeRegistry(registry: RegistryFile): Promise<void> {
    return atomicWriteJson(this.registryFile, registry);
  }
}
