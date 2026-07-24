import { randomUUID } from "node:crypto";
import { readFile, realpath } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import {
  RuntimeError,
  type ChiralityProjectManifestV1,
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

  constructor(private readonly runtimeDirectory: string) {
    this.registryFile = join(runtimeDirectory, "projects", "registry.json");
  }

  async register(
    manifestPath: string,
    approval: RegisteredProject["approval"],
    clientId = `project-${randomUUID()}`
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
      clientId,
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

  async readManifest(projectId: string): Promise<ChiralityProjectManifestV1> {
    const project = await this.getRecord(projectId);
    return this.parseManifest(await readFile(project.manifestPath, "utf8"));
  }

  async roots(projectId: string): Promise<{ workingRoot: string; instructionRoot: string }> {
    const project = await this.requireAuthorized(projectId);
    const manifest = await this.readManifest(projectId);
    return {
      workingRoot: project.canonicalRoot,
      instructionRoot: await realpath(resolve(dirname(project.manifestPath), manifest.instructionRoot))
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

  private parseManifest(source: string): ChiralityProjectManifestV1 {
    let value: unknown;
    try {
      value = JSON.parse(source);
    } catch {
      throw new RuntimeError("PROJECT_MANIFEST_INVALID", "Project manifest is not valid JSON");
    }
    if (!this.isManifest(value)) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Project manifest does not conform to chirality.project/v1"
      );
    }
    return value;
  }

  private isManifest(value: unknown): value is ChiralityProjectManifestV1 {
    if (typeof value !== "object" || value === null) return false;
    const item = value as Record<string, unknown>;
    const profiles = item["profiles"] as Record<string, unknown> | undefined;
    const embeddedUi = item["embeddedUi"] as Record<string, unknown> | undefined;
    return (
      item["schemaVersion"] === "chirality.project/v1" &&
      typeof item["projectId"] === "string" &&
      typeof item["displayName"] === "string" &&
      typeof item["workingRoot"] === "string" &&
      typeof item["instructionRoot"] === "string" &&
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

  private async validateReferences(
    manifestDirectory: string,
    manifest: ChiralityProjectManifestV1
  ): Promise<{ workingRoot: string; instructionRoot: string }> {
    assertSafeIdentifier(manifest.projectId, "projectId");
    assertRelativeManifestPath(manifest.workingRoot, "workingRoot");
    assertRelativeManifestPath(manifest.instructionRoot, "instructionRoot");
    const workingRoot = await realpath(resolve(manifestDirectory, manifest.workingRoot));
    const instructionRoot = await realpath(resolve(manifestDirectory, manifest.instructionRoot));
    if (!isContained(instructionRoot, workingRoot) && !isContained(workingRoot, instructionRoot)) {
      throw new RuntimeError(
        "PROJECT_MANIFEST_INVALID",
        "Working and instruction roots must belong to one canonical project tree"
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
      const canonical = await realpath(resolve(manifestDirectory, path));
      if (!isContained(workingRoot, canonical) && !isContained(instructionRoot, canonical)) {
        throw new RuntimeError(
          "PROJECT_MANIFEST_INVALID",
          `${label} escapes the declared working and instruction roots`
        );
      }
    }
    return { workingRoot, instructionRoot };
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
