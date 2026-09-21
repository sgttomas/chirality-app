import { mkdtemp, readFile, realpath, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  HARNESS_EVENT_TYPES,
  HarnessError,
  PUBLIC_UI_EVENT_NAMES,
  RUNTIME_ROUTES
} from "@chirality/runtime-contracts";
import { HarnessError as SubpathHarnessError } from "@chirality/runtime-contracts/errors";
import { ProjectRegistry, SessionStore } from "@chirality/runtime-core";
import { createProjectFixture } from "./helpers.js";

describe("standalone promoted contracts", () => {
  it("preserves existing values and identities while adding daemon routes", () => {
    expect(HarnessError).toBe(SubpathHarnessError);
    expect(HARNESS_EVENT_TYPES).toContain("turn.interrupted");
    expect(PUBLIC_UI_EVENT_NAMES).toEqual(
      expect.arrayContaining(["session:init", "harness:event", "process:exit"])
    );
    expect(RUNTIME_ROUTES.sessionTurn("p", "s")).toBe("/v1/projects/p/sessions/s/turn");
  });
});

describe("project registry", () => {
  it("registers a V2 working repository against a disjoint runtime instruction root", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-v2-"));
    const working = join(root, "working");
    const instructions = join(root, "instructions");
    const { mkdir } = await import("node:fs/promises");
    await mkdir(join(working, "execution"), { recursive: true });
    await mkdir(join(instructions, "agents"), { recursive: true });
    await writeFile(join(working, "domain-pack.yaml"), "id: external\n", "utf8");
    await writeFile(join(instructions, "agents", "AGENT_TASK.md"), "AGENT_TYPE: 2\n", "utf8");
    const manifestPath = join(working, "chirality.project.json");
    await writeFile(
      manifestPath,
      JSON.stringify({
        schemaVersion: "chirality.project/v2",
        projectId: "external-domain",
        displayName: "External Domain",
        workingRoot: ".",
        instructionRoot: { mode: "runtime" },
        defaultExecutionRoot: "execution",
        profiles: {
          domain: ["domain-pack.yaml"],
          capability: [],
          dataBoundary: []
        },
        enabledAdapterIds: ["anthropic-direct", "claude-agent-sdk", "pi"],
        embeddedUi: { declared: false },
        legacySessionRoots: []
      }),
      "utf8"
    );
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"), {
      CHIRALITY_INSTRUCTION_ROOT: instructions
    });
    await registry.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    await expect(registry.roots("external-domain")).resolves.toEqual({
      workingRoot: await realpath(working),
      instructionRoot: await realpath(instructions)
    });
  });

  it("rejects V2 when the runtime instruction root is missing or overlaps the working root", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-v2-invalid-"));
    const { mkdir } = await import("node:fs/promises");
    await mkdir(join(root, "execution"), { recursive: true });
    await writeFile(join(root, "domain-pack.yaml"), "id: invalid\n", "utf8");
    const manifestPath = join(root, "chirality.project.json");
    await writeFile(
      manifestPath,
      JSON.stringify({
        schemaVersion: "chirality.project/v2",
        projectId: "invalid-v2",
        displayName: "Invalid V2",
        workingRoot: ".",
        instructionRoot: { mode: "runtime" },
        defaultExecutionRoot: "execution",
        profiles: { domain: ["domain-pack.yaml"], capability: [], dataBoundary: [] },
        enabledAdapterIds: ["pi"],
        embeddedUi: { declared: false },
        legacySessionRoots: []
      }),
      "utf8"
    );
    await expect(
      new ProjectRegistry(join(root, "runtime-missing"), {}).register(manifestPath, {
        approvedBy: "test",
        approvalReference: "D-TEST"
      })
    ).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_INVALID",
      message: "CHIRALITY_INSTRUCTION_ROOT is required for chirality.project/v2"
    });
    await expect(
      new ProjectRegistry(join(root, "runtime-overlap"), {
        CHIRALITY_INSTRUCTION_ROOT: root
      }).register(manifestPath, {
        approvedBy: "test",
        approvalReference: "D-TEST"
      })
    ).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_INVALID",
      message: "Runtime instruction root must be disjoint from the working root"
    });
  });

  it("allows profile references under a distinct declared instruction root and detects drift", async () => {
    const repository = await mkdtemp(join(tmpdir(), "chirality-project-"));
    const project = join(repository, "projects", "pec");
    const profile = join(repository, "_DomainEngines", "profiles");
    const { mkdir } = await import("node:fs/promises");
    await mkdir(project, { recursive: true });
    await mkdir(profile, { recursive: true });
    await mkdir(join(project, "execution"));
    await writeFile(join(profile, "pec.yaml"), "id: pec\n", "utf8");
    const manifestPath = join(project, "chirality.project.json");
    await writeFile(
      manifestPath,
      JSON.stringify({
        schemaVersion: "chirality.project/v1",
        projectId: "pec",
        displayName: "PEC",
        workingRoot: ".",
        instructionRoot: "../..",
        defaultExecutionRoot: "execution",
        profiles: {
          domain: ["../../_DomainEngines/profiles/pec.yaml"],
          capability: [],
          dataBoundary: []
        },
        enabledAdapterIds: ["pi"],
        embeddedUi: { declared: false },
        legacySessionRoots: []
      }),
      "utf8"
    );
    const registry = new ProjectRegistry(join(repository, "user-data", "runtime"));
    await registry.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    expect((await registry.status("pec")).manifestDrift).toBe(false);
    await writeFile(manifestPath, `${await readFile(manifestPath, "utf8")}\n`, "utf8");
    expect((await registry.status("pec")).manifestDrift).toBe(true);
    await expect(registry.requireAuthorized("pec")).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_DRIFT"
    });
  });

  it("registers a manifest whose referenced paths all exist", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-existing-"));
    const { manifestPath } = await createProjectFixture(root, "existing");
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"));
    const record = await registry.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    expect(record.projectId).toBe("existing");
    expect((await registry.status("existing")).manifestDrift).toBe(false);
  });

  it("rejects a missing defaultExecutionRoot with a typed manifest error naming label and path", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-missing-exec-"));
    const { manifest, manifestPath } = await createProjectFixture(root, "missing-exec");
    manifest.defaultExecutionRoot = "missing-execution";
    await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"));
    await expect(
      registry.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" })
    ).rejects.toMatchObject({
      name: "RuntimeError",
      code: "PROJECT_MANIFEST_INVALID",
      message: "defaultExecutionRoot references a path that does not exist: missing-execution"
    });
  });

  it("rejects a missing workingRoot with a typed manifest error naming label and path", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-missing-root-"));
    const { manifest, manifestPath } = await createProjectFixture(root, "missing-root");
    manifest.workingRoot = "no-such-root";
    await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"));
    await expect(
      registry.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" })
    ).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_INVALID",
      message: "workingRoot references a path that does not exist: no-such-root"
    });
  });

  it("tolerates an absent legacySessionRoots entry and lists no legacy sessions from it", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-legacy-absent-"));
    const { manifest, manifestPath } = await createProjectFixture(root, "legacy-absent");
    manifest.legacySessionRoots = ["frontend/.chirality/sessions"];
    await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
    const runtimeDirectory = join(root, "user-data", "runtime");
    const registry = new ProjectRegistry(runtimeDirectory);
    const record = await registry.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    expect(record.legacySessionRoots).toEqual(["frontend/.chirality/sessions"]);
    const sessions = new SessionStore(runtimeDirectory, registry);
    await expect(sessions.list("legacy-absent")).resolves.toEqual([]);
  });

  it("still rejects a legacySessionRoots entry that exists but escapes the declared roots", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-legacy-escape-"));
    const { manifest, manifestPath } = await createProjectFixture(root, "legacy-escape");
    const { mkdir } = await import("node:fs/promises");
    await mkdir(join(root, "..", "outside-sessions"), { recursive: true });
    manifest.legacySessionRoots = ["../outside-sessions"];
    await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"));
    await expect(
      registry.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" })
    ).rejects.toMatchObject({
      code: "PROJECT_MANIFEST_INVALID",
      message: "legacySessionRoots escapes the declared working and instruction roots"
    });
  });

  it("rejects symlink/path escapes outside both declared roots", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-escape-"));
    const { manifest, manifestPath } = await createProjectFixture(root, "escape");
    manifest.profiles.domain = ["../outside.yaml"];
    await writeFile(join(root, "..", "outside.yaml"), "outside\n", "utf8");
    await writeFile(manifestPath, JSON.stringify(manifest), "utf8");
    const registry = new ProjectRegistry(join(root, "user-data", "runtime"));
    await expect(
      registry.register(manifestPath, {
        approvedBy: "test",
        approvalReference: "D-TEST"
      })
    ).rejects.toBeDefined();
  });
});
