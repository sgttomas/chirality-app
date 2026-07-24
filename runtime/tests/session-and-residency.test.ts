import { mkdtemp, readFile, writeFile, mkdir, realpath } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import type { OmlxControlPort, OmlxModelStatus } from "@chirality/runtime-contracts";
import { ProjectRegistry, ResidencyCoordinator, SessionStore } from "@chirality/runtime-core";
import { createProjectFixture } from "./helpers.js";

class FakeOmlx implements OmlxControlPort {
  models: OmlxModelStatus[] = [
    { id: "model-a", kind: "llm", loaded: true, loading: false },
    { id: "model-b", kind: "llm", loaded: false, loading: false },
    { id: "embed", kind: "embedding", loaded: true, loading: false }
  ];
  failLoad = false;
  failUnloadAfterMutation = false;
  unloads: string[] = [];

  async listStatus() {
    return this.models;
  }
  async load(modelId: string) {
    if (this.failLoad) throw new Error("memory");
    this.models = this.models.map((model) =>
      model.id === modelId ? { ...model, loaded: true } : model
    );
  }
  async unload(modelId: string) {
    this.unloads.push(modelId);
    this.models = this.models.map((model) =>
      model.id === modelId ? { ...model, loaded: false } : model
    );
    if (this.failUnloadAfterMutation) throw new Error("response lost");
  }
}

describe("central sessions", () => {
  it("lazily copies a legacy record without modifying the source", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-session-"));
    const { manifestPath } = await createProjectFixture(root);
    const legacyId = "legacy-one";
    await mkdir(join(root, "legacy-sessions", legacyId));
    const legacyPath = join(root, "legacy-sessions", legacyId, "session.json");
    const legacySource = JSON.stringify({
      sessionId: legacyId,
      projectRoot: root,
      persona: "HELP_HUMAN",
      mode: "direct",
      model: "claude",
      createdAt: "2026-01-01T00:00:00.000Z",
      updatedAt: "2026-01-01T00:00:00.000Z"
    });
    await writeFile(legacyPath, legacySource, "utf8");
    const runtime = join(root, "user-data", "runtime");
    const projects = new ProjectRegistry(runtime);
    await projects.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    const sessions = new SessionStore(runtime, projects);
    const migrated = await sessions.get("fixture", legacyId);
    expect(migrated.legacy?.sourcePath).toBe(await realpath(legacyPath));
    expect(await readFile(legacyPath, "utf8")).toBe(legacySource);
    expect(migrated.persona).toBe("HELP_HUMAN");
    await sessions.delete("fixture", legacyId);
    await expect(sessions.get("fixture", legacyId)).rejects.toMatchObject({
      code: "SESSION_NOT_FOUND"
    });
    expect(await readFile(legacyPath, "utf8")).toBe(legacySource);
  });

  it("enters NO_MODEL when an unload outcome is ambiguous", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-residency-ambiguous-"));
    const control = new FakeOmlx();
    const coordinator = new ResidencyCoordinator(control, root, {
      totalTimeoutMs: 1_000,
      pollIntervalMs: 2
    });
    await coordinator.activate("model-a", "D-TEST");
    control.failUnloadAfterMutation = true;
    await expect(coordinator.activate("model-b", "D-TEST")).rejects.toBeDefined();
    expect(await coordinator.status()).toMatchObject({
      phase: "NO_MODEL",
      acceptingLocalTurns: false
    });
  });
});

describe("model residency", () => {
  it("requires non-empty approval attribution", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-residency-approval-"));
    const coordinator = new ResidencyCoordinator(new FakeOmlx(), root);
    await expect(coordinator.activate("model-a", " ")).rejects.toMatchObject({
      code: "INVALID_REQUEST"
    });
  });

  it("reconciles an externally unloaded managed model before status or admission", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-residency-drift-"));
    const control = new FakeOmlx();
    const coordinator = new ResidencyCoordinator(control, root);
    await coordinator.activate("model-a", "D-TEST");
    control.models = control.models.map((model) =>
      model.id === "model-a" ? { ...model, loaded: false } : model
    );
    expect(await coordinator.status()).toMatchObject({
      phase: "NO_MODEL",
      acceptingLocalTurns: false
    });
    await expect(coordinator.admitTurn("model-a")).rejects.toMatchObject({
      code: "RESIDENCY_TRANSITION_IN_PROGRESS"
    });
  });

  it("drains without force and enters NO_MODEL after a post-unload load failure", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-residency-"));
    const control = new FakeOmlx();
    const coordinator = new ResidencyCoordinator(control, root, {
      drainTimeoutMs: 15,
      totalTimeoutMs: 1_000,
      pollIntervalMs: 2
    });
    const ready = await coordinator.activate("model-a", "D-TEST");
    expect(ready.managedModelId).toBe("model-a");
    expect(ready.acceptingLocalTurns).toBe(true);
    const release = await coordinator.admitTurn("model-a");
    await expect(coordinator.activate("model-b", "D-TEST")).rejects.toMatchObject({
      code: "RESIDENCY_DRAIN_TIMEOUT"
    });
    expect((await coordinator.status()).managedModelId).toBe("model-a");
    release();
    control.failLoad = true;
    await expect(coordinator.activate("model-b", "D-TEST")).rejects.toBeDefined();
    const failed = await coordinator.status();
    expect(failed.phase).toBe("NO_MODEL");
    expect(failed.managedModelId).toBeUndefined();
    expect(control.unloads).toEqual(["model-a"]);
    expect(control.models.find((model) => model.id === "embed")?.loaded).toBe(true);
  });
});
