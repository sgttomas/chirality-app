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
  it("preserves absent, empty, and bounded brief scopes as distinct session state", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-session-scopes-"));
    const { manifestPath } = await createProjectFixture(root);
    const runtime = join(root, "user-data", "runtime");
    const projects = new ProjectRegistry(runtime);
    await projects.register(manifestPath, {
      approvedBy: "test",
      approvalReference: "D-TEST"
    });
    const sessions = new SessionStore(runtime, projects);
    const base = {
      projectId: "fixture",
      role: "agent1" as const,
      engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" }
    };

    const inherited = await sessions.create(base);
    const denied = await sessions.create({
      ...base,
      declaredContext: [],
      allowedWriteTargets: []
    });
    const boundedContext = [join(root, "execution", "PKG-01")];
    const boundedWrites = [join(root, "execution", "PKG-01", "output.md")];
    const bounded = await sessions.create({
      ...base,
      declaredContext: boundedContext,
      allowedWriteTargets: boundedWrites
    });

    expect(await sessions.get("fixture", inherited.sessionId)).not.toHaveProperty("declaredContext");
    expect(await sessions.get("fixture", inherited.sessionId)).not.toHaveProperty("allowedWriteTargets");
    expect(await sessions.get("fixture", denied.sessionId)).toMatchObject({
      declaredContext: [],
      allowedWriteTargets: []
    });
    expect(await sessions.get("fixture", bounded.sessionId)).toMatchObject({
      declaredContext: boundedContext,
      allowedWriteTargets: boundedWrites
    });
  });

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

describe("service shutdown settlement", () => {
  it("settles sessions left running by a service that ended without settlement when the next service starts", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-session-restart-"));
    const { manifestPath } = await createProjectFixture(root);
    const runtime = join(root, "user-data", "runtime");
    const projects = new ProjectRegistry(runtime);
    await projects.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" });
    const sessions = new SessionStore(runtime, projects);
    const stuck = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    const idle = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.appendEvent("fixture", { sessionId: stuck.sessionId, turnId: "turn-7", type: "turn.accepted", data: {} });
    await sessions.update({ ...(await sessions.get("fixture", stuck.sessionId)), status: "running" });
    expect(await sessions.settleRunningOnStart("fixture")).toEqual([stuck.sessionId]);
    expect(await sessions.get("fixture", stuck.sessionId)).toMatchObject({ status: "interrupted" });
    expect(await sessions.get("fixture", idle.sessionId)).toMatchObject({ status: "idle" });
    expect((await sessions.replay("fixture", stuck.sessionId)).filter((event) => event.type === "turn.interrupted")).toEqual([expect.objectContaining({ turnId: "turn-7", data: { reason: "service-restart" } })]);
    expect(await sessions.settleRunningOnStart("fixture")).toEqual([]);
  });

  it("records turn.interrupted with the reason for a still-running session and leaves settled sessions alone", async () => {
    const root = await mkdtemp(join(tmpdir(), "chirality-session-shutdown-"));
    const { manifestPath } = await createProjectFixture(root);
    const runtime = join(root, "user-data", "runtime");
    const projects = new ProjectRegistry(runtime);
    await projects.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" });
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    expect(await sessions.markInterruptedOnShutdown("fixture", created.sessionId, "turn-idle")).toBe(false);
    await sessions.update({ ...(await sessions.get("fixture", created.sessionId)), status: "running" });
    expect(await sessions.markInterruptedOnShutdown("fixture", created.sessionId, "turn-1")).toBe(true);
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({ status: "interrupted" });
    const events = await sessions.replay("fixture", created.sessionId);
    expect(events.filter((event) => event.type === "turn.interrupted")).toEqual([expect.objectContaining({ turnId: "turn-1", data: { reason: "service-shutdown" } })]);
    expect(await sessions.markInterruptedOnShutdown("fixture", created.sessionId, "turn-1")).toBe(false);
    expect((await sessions.replay("fixture", created.sessionId)).filter((event) => event.type === "turn.interrupted")).toHaveLength(1);
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
