import { mkdtemp, readFile, writeFile } from "node:fs/promises";
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
import { ProjectRegistry } from "@chirality/runtime-core";
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
