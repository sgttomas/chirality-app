import { readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { mkdtemp } from "node:fs/promises";
import { describe, expect, it } from "vitest";
import { sha256 } from "../packages/core/src/fs.js";
import { InstructionBasisStore } from "../packages/core/src/instruction-basis-store.js";
import { evaluateMethodTransition } from "../packages/core/src/method-transition.js";
import { ProjectRegistry } from "@chirality/runtime-core";
import { SessionStore } from "../packages/core/src/session-store.js";
import { createProjectFixture } from "./helpers.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "chirality-instruction-basis-"));
  const runtime = join(root, "user-data", "runtime");
  const { manifestPath } = await createProjectFixture(root);
  const projects = new ProjectRegistry(runtime);
  await projects.register(manifestPath, { approvedBy: "test", approvalReference: "D-TEST" });
  return {
    runtime,
    projects,
    store: new InstructionBasisStore(runtime, projects, {
      validateNativePlanRevision(revision) {
        if (revision.sourceEvent.qualification.qualificationId !== "trusted-qualification") {
          throw new Error("untrusted");
        }
      }
    })
  };
}

const method = {
  sourceRootId: "root",
  source: "project" as const,
  kind: "workflow" as const,
  name: "chirality-change"
};

const loadedMethod = {
  sourceRootId: "root",
  source: "project" as const,
  kind: "skill" as const,
  name: "loaded-one"
};

const secondLoadedMethod = {
  sourceRootId: "bundled",
  source: "bundled" as const,
  kind: "workflow" as const,
  name: "loaded-two"
};

describe("instruction basis persistence", () => {
  it("freezes exact supplied content and rejects replacement or a false hash", async () => {
    const { runtime, store } = await fixture();
    const content = "line one\r\nline two  \n";
    const snapshot = {
      schemaVersion: "chirality.instruction-basis/v1" as const,
      basisId: "basis-1",
      sessionId: "session-1",
      createdAt: "2026-09-09T00:00:00.000Z",
      roleId: "WORKING_ITEMS",
      interactionMode: "chat" as const,
      permissionMode: "workspaceWrite" as const,
      selectedMethods: [method],
      compatibilityInputs: [],
      compatibilityMappings: [],
      suppliedEntries: [{
        kind: "role" as const,
        id: "WORKING_ITEMS",
        origin: "accepted-root@abc123",
        path: "agents/AGENT_WORKING_ITEMS.md",
        sha256: sha256(content),
        content
      }],
      methodDispositions: [{
        method,
        selected: true as const,
        activeRoleCompatible: true,
        eligibleRoleIds: ["WORKING_ITEMS" as const],
        route: "primary" as const
      }]
    };
    expect(store.prepare(snapshot)).toEqual(snapshot);
    await store.commitWithTurn("fixture", snapshot, { turnId: "turn-1", eventId: "event-1" });
    expect(await store.get("fixture", "session-1", "basis-1")).toEqual(snapshot);
    const bytes = await readFile(
      join(runtime, "projects", "fixture", "sessions", "session-1", "instruction-bases", "basis-1.json"),
      "utf8"
    );
    expect(JSON.parse(bytes).suppliedEntries[0].content).toBe(content);
    await expect(store.commitWithTurn(
      "fixture",
      { ...snapshot, roleId: "HELP_HUMAN" },
      { turnId: "turn-2", eventId: "event-2" }
    ))
      .rejects.toMatchObject({ status: 409 });
    expect(() => store.prepare({
      ...snapshot,
      basisId: "basis-bad",
      suppliedEntries: [{ ...snapshot.suppliedEntries[0], sha256: "0".repeat(64) }]
    })).toThrow(expect.objectContaining({ code: "INVALID_REQUEST" }));
    expect((await store.history("fixture", "session-1"))[0]).toMatchObject({
      type: "instruction-basis.resolved",
      acceptedTurn: { turnId: "turn-1", eventId: "event-1" }
    });
  });

  it("keeps one ordered append-only history for selections, loads, and qualified plans", async () => {
    const { store } = await fixture();
    const loaded = "# method\n";
    const plan = "{\"steps\":[\"inspect\",\"change\"]}";
    const inputs = [
      {
        type: "selection.changed" as const,
        roleId: "WORKING_ITEMS",
        interactionMode: "chat" as const,
        permissionMode: "workspaceWrite" as const,
        selectedMethods: [method]
      },
      {
        type: "resource.loaded" as const,
        turnId: "turn-load",
        invocationId: "load-1",
        resourceKind: "method-body" as const,
        id: "chirality-change",
        method,
        origin: "root@abc123",
        path: "workflows/chirality-change/WORKFLOW.md",
        sha256: sha256(loaded),
        content: loaded
      },
      {
        type: "native-plan.revised" as const,
        revision: {
          revision: 2,
          sourceEvent: {
            qualificationState: "qualified" as const,
            eventId: "event-17",
            occurredAt: "2026-09-09T00:00:00.000Z",
            qualification: {
              adapterId: "codex-app-server",
              providerId: "openai",
              qualificationId: "trusted-qualification",
              admissionSha256: "a".repeat(64),
              evidenceClass: "native-adapter-qualified" as const
            },
            plan: JSON.parse(plan)
          }
        }
      }
    ];
    await Promise.all(inputs.map((input) => store.appendHistory("fixture", "session-2", input)));
    const history = await store.history("fixture", "session-2");
    expect(history.map((entry) => entry.sequence)).toEqual([0, 1, 2]);
    expect(history.map((entry) => entry.type)).toEqual(inputs.map((entry) => entry.type));
    expect(history[1]).toMatchObject({ content: loaded, origin: "root@abc123" });
    await expect(store.appendHistory("fixture", "session-2", {
      ...inputs[2],
      revision: {
        ...inputs[2].revision,
        sourceEvent: {
          ...inputs[2].revision.sourceEvent,
          qualification: {
            ...inputs[2].revision.sourceEvent.qualification,
            qualificationId: "renderer-self-attested"
          }
        }
      }
    })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("commits turn acceptance and its basis together and rolls back a conflicting basis", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const session = await sessions.create({
      projectId: "fixture",
      role: "agent1",
      engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" }
    });
    const content = "accepted basis\n";
    const snapshot = {
      schemaVersion: "chirality.instruction-basis/v1" as const,
      basisId: "accepted-basis",
      sessionId: session.sessionId,
      createdAt: "2026-09-09T00:00:00.000Z",
      roleId: "WORKING_ITEMS",
      interactionMode: "chat",
      permissionMode: "workspaceWrite",
      selectedMethods: [method],
      compatibilityInputs: [],
      compatibilityMappings: [],
      suppliedEntries: [{ kind: "method-body" as const, id: "chirality-change", method, origin: "root@abc", path: "workflow.md", sha256: sha256(content), content }],
      methodDispositions: [{ method, selected: true as const, activeRoleCompatible: true, eligibleRoleIds: ["WORKING_ITEMS" as const], route: "primary" as const }]
    };
    const committed = await sessions.commitWithAcceptedTurn(session, {
      sessionId: session.sessionId,
      turnId: "turn-accepted",
      type: "turn.accepted",
      data: { message: "do work" }
    }, snapshot);
    expect(committed.event.type).toBe("turn.accepted");
    expect(await sessions.get("fixture", session.sessionId)).toMatchObject({
      schemaVersion: "chirality.session/v3",
      roleId: "WORKING_ITEMS",
      interactionMode: "chat",
      permissionMode: "workspaceWrite",
      selectedMethods: [method],
      instructionBasisId: "accepted-basis",
      status: "running"
    });
    const restarted = new SessionStore(runtime, projects);
    expect(await restarted.replay("fixture", session.sessionId)).toHaveLength(1);
    expect(await restarted.instructionBases.get("fixture", session.sessionId, "accepted-basis"))
      .toEqual(snapshot);

    const completed = { ...(await sessions.get("fixture", session.sessionId)), status: "completed" as const };
    await sessions.update(completed);
    const secondSession = await sessions.get("fixture", session.sessionId);
    const reused = await sessions.commitWithAcceptedTurn(secondSession, {
      sessionId: session.sessionId,
      turnId: "turn-second",
      type: "turn.accepted",
      data: { message: "continue" }
    }, { ...snapshot, createdAt: "2026-09-09T01:00:00.000Z" });
    expect(reused.instructionBasis).toEqual(snapshot);
    expect((await sessions.instructionBases.history("fixture", session.sessionId))
      .filter((entry) => entry.type === "instruction-basis.resolved")).toHaveLength(2);
    await sessions.update({ ...(await sessions.get("fixture", session.sessionId)), status: "completed" });

    await expect(sessions.commitWithAcceptedTurn(await sessions.get("fixture", session.sessionId), {
      sessionId: session.sessionId,
      turnId: "turn-conflict",
      type: "turn.accepted",
      data: { message: "different basis" }
    }, { ...snapshot, roleId: "HELP_HUMAN" })).rejects.toMatchObject({ status: 409 });
    expect((await sessions.replay("fixture", session.sessionId)).map((event) => event.turnId))
      .toEqual(["turn-accepted", "turn-second"]);
  });

  it("keeps replay behind an in-flight accepted-turn transaction", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const session = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    const content = "basis\n";
    const snapshot = {
      schemaVersion: "chirality.instruction-basis/v1" as const, basisId: "basis-concurrent", sessionId: session.sessionId,
      createdAt: "2026-09-09T00:00:00.000Z", roleId: "WORKING_ITEMS" as const, interactionMode: "chat" as const,
      permissionMode: "ask" as const, selectedMethods: [method],
      compatibilityInputs: [], compatibilityMappings: [],
      suppliedEntries: [{ kind: "method-body" as const, id: "method", method, origin: "root", path: "WORKFLOW.md", sha256: sha256(content), content }],
      methodDispositions: [{ method, selected: true as const, activeRoleCompatible: true, eligibleRoleIds: ["WORKING_ITEMS" as const], route: "primary" as const }]
    };
    const original = sessions.instructionBases.commitWithTurn.bind(sessions.instructionBases);
    let release!: () => void;
    let entered!: () => void;
    const enteredPromise = new Promise<void>((resolve) => { entered = resolve; });
    const gate = new Promise<void>((resolve) => { release = resolve; });
    sessions.instructionBases.commitWithTurn = async (...args) => { entered(); await gate; return original(...args); };
    const committing = sessions.commitWithAcceptedTurn(session, { sessionId: session.sessionId, turnId: "turn", type: "turn.accepted", data: { message: "x" } }, snapshot);
    await enteredPromise;
    let replayFinished = false;
    const replaying = sessions.replay("fixture", session.sessionId).then((events) => { replayFinished = true; return events; });
    await Promise.resolve();
    expect(replayFinished).toBe(false);
    release();
    await committing;
    expect(await replaying).toHaveLength(1);
  });

  it("serializes delayed selection changes and rejects a stale CAS", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({ ...created, schemaVersion: "chirality.session/v3", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis-old" });
    let release!: () => void;
    let entered!: () => void;
    const enteredPromise = new Promise<void>((resolve) => { entered = resolve; });
    const gate = new Promise<void>((resolve) => { release = resolve; });
    const expected = { instructionBasisId: "basis-old", methodSelectionRevision: 0 };
    const first = sessions.mutateSelection("fixture", created.sessionId, expected, async (current) => {
      entered();
      await gate;
      return {
        session: { ...current, selectedMethods: [method], methodSelectionRevision: 1, instructionBasisId: "basis-new" },
        history: { type: "selection.changed" as const, roleId: "WORKING_ITEMS" as const, interactionMode: "chat" as const, permissionMode: "ask" as const, selectedMethods: [method] }
      };
    });
    await enteredPromise;
    let staleCallbackRan = false;
    const stale = sessions.mutateSelection("fixture", created.sessionId, expected, (current) => {
      staleCallbackRan = true;
      return { session: current, history: { type: "selection.changed", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [] } };
    });
    release();
    await first;
    await expect(stale).rejects.toMatchObject({ status: 409 });
    expect(staleCallbackRan).toBe(false);
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({ methodSelectionRevision: 1, instructionBasisId: "basis-new" });

    const beforeAcceptance = await sessions.get("fixture", created.sessionId);
    let releaseSelection!: () => void;
    let selectionEntered!: () => void;
    const selectionEnteredPromise = new Promise<void>((resolve) => { selectionEntered = resolve; });
    const selectionGate = new Promise<void>((resolve) => { releaseSelection = resolve; });
    const advancing = sessions.mutateSelection(
      "fixture",
      created.sessionId,
      { instructionBasisId: "basis-new", methodSelectionRevision: 1 },
      async (current) => {
        selectionEntered();
        await selectionGate;
        return {
          session: { ...current, roleId: "HELP_HUMAN", role: "agent0", persona: "HELP_HUMAN", agentType: 0, selectedMethods: [], methodSelectionRevision: 2, instructionBasisId: "basis-final", adapterSession: { engineSessionId: "engine-transition" } },
          history: { type: "selection.changed", roleId: "HELP_HUMAN", interactionMode: "chat", permissionMode: "ask", selectedMethods: [] }
        };
      }
    );
    await selectionEnteredPromise;
    const basisContent = "stale accepted basis\n";
    const accepting = sessions.commitWithAcceptedTurn(beforeAcceptance, {
      sessionId: created.sessionId,
      turnId: "stale-turn",
      type: "turn.accepted",
      data: { message: "stale" }
    }, {
      schemaVersion: "chirality.instruction-basis/v1",
      basisId: "basis-new",
      sessionId: created.sessionId,
      createdAt: "2026-09-09T00:00:00.000Z",
      roleId: "WORKING_ITEMS",
      interactionMode: "chat",
      permissionMode: "ask",
      selectedMethods: [method],
      compatibilityInputs: [],
      compatibilityMappings: [],
      suppliedEntries: [{ kind: "method-body", id: "method", method, origin: "root", path: "WORKFLOW.md", sha256: sha256(basisContent), content: basisContent }],
      methodDispositions: [{ method, selected: true, activeRoleCompatible: true, eligibleRoleIds: ["WORKING_ITEMS"], route: "primary" }]
    });
    releaseSelection();
    await advancing;
    await expect(accepting).rejects.toMatchObject({ status: 409 });
    expect(await sessions.replay("fixture", created.sessionId)).toEqual([]);
    await sessions.update({ ...beforeAcceptance, status: "failed" });
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({
      roleId: "HELP_HUMAN",
      role: "agent0",
      persona: "HELP_HUMAN",
      agentType: 0,
      methodSelectionRevision: 2,
      instructionBasisId: "basis-final",
      adapterSession: { engineSessionId: "engine-transition" },
      status: "failed"
    });
  });

  it("atomically activates agent-loaded methods for the accepted running turn and preserves them across stale updates", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({
      ...created,
      schemaVersion: "chirality.session/v3",
      roleId: "WORKING_ITEMS",
      interactionMode: "chat",
      permissionMode: "ask",
      selectedMethods: [method],
      methodSelectionRevision: 4,
      instructionBasisId: "basis-accepted"
    });
    const acceptedSession = await sessions.get("fixture", created.sessionId);
    const content = "accepted method body\n";
    const snapshot = {
      schemaVersion: "chirality.instruction-basis/v1" as const,
      basisId: "basis-accepted",
      sessionId: created.sessionId,
      createdAt: "2026-09-09T00:00:00.000Z",
      roleId: "WORKING_ITEMS" as const,
      interactionMode: "chat" as const,
      permissionMode: "ask" as const,
      selectedMethods: [method],
      compatibilityInputs: [],
      compatibilityMappings: [],
      suppliedEntries: [{ kind: "method-body" as const, id: "method", method, origin: "root", path: "WORKFLOW.md", sha256: sha256(content), content }],
      methodDispositions: [{ method, selected: true as const, activeRoleCompatible: true, eligibleRoleIds: ["WORKING_ITEMS" as const], route: "primary" as const }]
    };
    await sessions.commitWithAcceptedTurn(acceptedSession, {
      sessionId: created.sessionId,
      turnId: "active-turn",
      type: "turn.accepted",
      data: { message: "load methods" }
    }, snapshot);
    const staleCoordinator = await sessions.get("fixture", created.sessionId);

    const originalBatch = sessions.instructionBases.appendHistoryBatchWithCommit.bind(sessions.instructionBases);
    let releaseFirst!: () => void;
    let firstEntered!: () => void;
    const firstEnteredPromise = new Promise<void>((resolve) => { firstEntered = resolve; });
    const firstGate = new Promise<void>((resolve) => { releaseFirst = resolve; });
    sessions.instructionBases.appendHistoryBatchWithCommit = async (...args) => {
      if (args[2].some(record => record.type === "selection.changed" && record.invocationId === "load-1")) {
        firstEntered();
        await firstGate;
      }
      return originalBatch(...args);
    };
    const first = sessions.activateLoadedMethods("fixture", created.sessionId, {
      turnId: "active-turn",
      invocationId: "load-1",
      methods: [method, loadedMethod, loadedMethod], instructionPolicySha256: "a".repeat(64), loadedEntries: []
    });
    await firstEnteredPromise;
    let secondFinished = false;
    const second = sessions.activateLoadedMethods("fixture", created.sessionId, {
      turnId: "active-turn",
      invocationId: "load-2",
      methods: [loadedMethod, secondLoadedMethod], instructionPolicySha256: "b".repeat(64), loadedEntries: []
    }).then((record) => { secondFinished = true; return record; });
    await Promise.resolve();
    expect(secondFinished).toBe(false);
    releaseFirst();
    expect(await first).toMatchObject({ methodSelectionRevision: 5, instructionBasisId: "basis-accepted" });
    expect(await second).toMatchObject({
      selectedMethods: [method, loadedMethod, secondLoadedMethod],
      methodSelectionRevision: 6,
      instructionBasisId: "basis-accepted"
    });
    expect(await sessions.activateLoadedMethods("fixture", created.sessionId, {
      turnId: "active-turn",
      invocationId: "load-duplicate",
      methods: [secondLoadedMethod, loadedMethod], instructionPolicySha256: "b".repeat(64), loadedEntries: []
    })).toMatchObject({ methodSelectionRevision: 6, instructionBasisId: "basis-accepted" });

    await sessions.update({ ...staleCoordinator, status: "completed" });
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({
      selectedMethods: [method, loadedMethod, secondLoadedMethod],
      methodSelectionRevision: 6,
      instructionBasisId: "basis-accepted",
      status: "completed"
    });
    expect((await sessions.instructionBases.history("fixture", created.sessionId)).filter((record) => record.type === "selection.changed"))
      .toEqual([
        expect.objectContaining({ reason: "agent-load", turnId: "active-turn", invocationId: "load-1", acceptedTurn: { turnId: "active-turn", eventId: expect.any(String) }, selectedMethods: [method, loadedMethod] }),
        expect.objectContaining({ reason: "agent-load", turnId: "active-turn", invocationId: "load-2", acceptedTurn: { turnId: "active-turn", eventId: expect.any(String) }, selectedMethods: [method, loadedMethod, secondLoadedMethod] })
      ]);
  });

  it("rejects loaded-method activation outside the current accepted running turn and rolls back history failures", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await expect(sessions.activateLoadedMethods("fixture", created.sessionId, { turnId: "missing", invocationId: "load", methods: [loadedMethod], instructionPolicySha256: "a".repeat(64), loadedEntries: [] }))
      .rejects.toMatchObject({ status: 409 });

    await sessions.update({ ...created, schemaVersion: "chirality.session/v3", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis" });
    await sessions.appendEvent("fixture", { sessionId: created.sessionId, turnId: "accepted", type: "turn.accepted", data: { message: "run" } });
    await sessions.update({ ...(await sessions.get("fixture", created.sessionId)), status: "running" });
    await expect(sessions.activateLoadedMethods("fixture", created.sessionId, { turnId: "wrong", invocationId: "load", methods: [loadedMethod], instructionPolicySha256: "a".repeat(64), loadedEntries: [] }))
      .rejects.toMatchObject({ status: 409 });

    const originalBatch = sessions.instructionBases.appendHistoryBatchWithCommit.bind(sessions.instructionBases);
    sessions.instructionBases.appendHistoryBatchWithCommit = async (...args) => {
      if (args[2].some(record => record.type === "selection.changed")) throw new Error("simulated agent-load history failure");
      return originalBatch(...args);
    };
    await expect(sessions.activateLoadedMethods("fixture", created.sessionId, { turnId: "accepted", invocationId: "load", methods: [loadedMethod], instructionPolicySha256: "a".repeat(64), loadedEntries: [] }))
      .rejects.toThrow("simulated agent-load history failure");
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({ selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis", status: "running" });
  });

  it("persists deferred method changes without widening the active turn and settles them after the boundary", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({ ...created, schemaVersion: "chirality.session/v3", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [method], methodSelectionRevision: 2, instructionBasisId: "basis-active" });
    await sessions.appendEvent("fixture", { sessionId: created.sessionId, turnId: "turn-one", type: "turn.accepted", data: { message: "change after this" } });
    await sessions.update({ ...(await sessions.get("fixture", created.sessionId)), status: "running" });

    const requested = await sessions.requestMethodChange("fixture", created.sessionId, {
      turnId: "turn-one",
      invocationId: "change-1",
      mode: "merge",
      methods: [loadedMethod],
      expectedRevision: 2,
      expectedBasisId: "basis-active"
    });
    expect(requested).toMatchObject({
      type: "method-change.requested",
      acceptedTurn: { turnId: "turn-one", eventId: expect.any(String) },
      mode: "merge",
      methods: [loadedMethod]
    });
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({
      selectedMethods: [method],
      methodSelectionRevision: 2,
      instructionBasisId: "basis-active",
      status: "running"
    });
    expect((await sessions.pendingMethodChanges("fixture", created.sessionId)).map((record) => record.historyId)).toEqual([requested.historyId]);

    await sessions.appendEvent("fixture", { sessionId: created.sessionId, turnId: "turn-one", type: "turn.completed", data: {} });
    await sessions.update({ ...(await sessions.get("fixture", created.sessionId)), status: "completed" });
    const applied = await sessions.mutateSelection("fixture", created.sessionId, { instructionBasisId: "basis-active", methodSelectionRevision: 2 }, current => ({
      session: { ...current, selectedMethods: [method, loadedMethod], methodSelectionRevision: 3, instructionBasisId: "basis-next" },
      history: { type: "selection.changed", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [method, loadedMethod], reason: "runtime-api" }
    }));
    await sessions.settleMethodChange("fixture", created.sessionId, requested.historyId, {
      resultingRevision: applied.methodSelectionRevision ?? 0,
      resultingBasisId: applied.instructionBasisId,
      selectedMethods: applied.selectedMethods ?? []
    });
    expect(await sessions.pendingMethodChanges("fixture", created.sessionId)).toEqual([]);
    expect((await sessions.instructionBases.history("fixture", created.sessionId)).at(-1)).toMatchObject({
      type: "method-change.applied",
      requestHistoryId: requested.historyId,
      resultingRevision: 3,
      resultingBasisId: "basis-next"
    });

    await sessions.appendEvent("fixture", { sessionId: created.sessionId, turnId: "turn-two", type: "turn.accepted", data: { message: "new turn" } });
    await sessions.update({ ...(await sessions.get("fixture", created.sessionId)), status: "running" });
    await expect(sessions.requestMethodChange("fixture", created.sessionId, {
      turnId: "turn-one",
      invocationId: "stale-callback",
      mode: "replace",
      methods: [],
      expectedRevision: 3,
      expectedBasisId: "basis-next"
    })).rejects.toMatchObject({ status: 409 });
    expect(await sessions.pendingMethodChanges("fixture", created.sessionId)).toEqual([]);
  });

  it("prepares provider continuation before selection commit and learns successor identity only from session:init", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({ ...created, schemaVersion: "chirality.session/v3", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis-old", engineSessionId: "engine-predecessor" });
    const common = {
      preparationId: "preparation-1",
      adapterId: "codex-app-server",
      providerId: "openai",
      predecessor: { engineSessionId: "engine-predecessor", providerSpanId: "span-predecessor" },
      targetBasisId: "basis-new",
      targetReference: "thread/start",
      continuationHash: sha256("predecessor->basis-new")
    };
    const originalAppend = sessions.instructionBases.appendHistory.bind(sessions.instructionBases);
    let releaseCommit!: () => void;
    let commitEntered!: () => void;
    const commitEnteredPromise = new Promise<void>((resolve) => { commitEntered = resolve; });
    const commitGate = new Promise<void>((resolve) => { releaseCommit = resolve; });
    sessions.instructionBases.appendHistory = async (...args) => {
      if (args[2].type === "provider-span.committed") { commitEntered(); await commitGate; }
      return originalAppend(...args);
    };
    const mutating = sessions.mutateSelection("fixture", created.sessionId, { instructionBasisId: "basis-old", methodSelectionRevision: 0 }, current => ({
      session: { ...current, selectedMethods: [method], methodSelectionRevision: 1, instructionBasisId: "basis-new" },
      history: { type: "selection.changed", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [method] },
      providerSpanPreparation: { type: "provider-span.prepared", ...common },
      providerSpanCommitmentReference: "provider-commit-1"
    }));
    await commitEnteredPromise;
    let initFinished = false;
    const initializing = sessions.recordProviderSpanSessionInit("fixture", created.sessionId, "preparation-1", {
      sessionInitEventId: "session-init-event-1",
      engineSessionId: "engine-successor",
      providerSpanId: "span-successor"
    }).then((record) => { initFinished = true; return record; });
    await Promise.resolve();
    expect(initFinished).toBe(false);
    releaseCommit();
    await mutating;
    const preparedHistory = await sessions.instructionBases.history("fixture", created.sessionId);
    expect(preparedHistory.map((record) => record.type).slice(0, 3)).toEqual(["provider-span.prepared", "selection.changed", "provider-span.committed"]);
    expect(JSON.stringify(preparedHistory[0])).not.toContain("successor");
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({ engineSessionId: "engine-predecessor" });

    const committed = preparedHistory[2];
    expect(committed).toMatchObject({
      type: "provider-span.committed",
      predecessor: { engineSessionId: "engine-predecessor" },
      commitmentReference: "provider-commit-1"
    });
    expect(JSON.stringify(committed)).not.toContain("engine-successor");
    const continued = await initializing;
    expect(continued).toMatchObject({ type: "provider-span.continued", engineSessionId: "engine-successor", spanId: "span-successor" });
  });

  it("rolls back a failed prepared selection and records cancellation without changing predecessor identity", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const created = await sessions.create({ projectId: "fixture", role: "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({ ...created, schemaVersion: "chirality.session/v3", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [], methodSelectionRevision: 0, instructionBasisId: "basis-old", engineSessionId: "engine-predecessor" });
    const originalAppend = sessions.instructionBases.appendHistory.bind(sessions.instructionBases);
    let failSelectionOnce = true;
    sessions.instructionBases.appendHistory = async (...args) => {
      if (args[2].type === "selection.changed" && failSelectionOnce) {
        failSelectionOnce = false;
        throw new Error("simulated history failure");
      }
      return originalAppend(...args);
    };
    const preparation = {
      type: "provider-span.prepared" as const,
      preparationId: "preparation-failed",
      adapterId: "codex-app-server",
      providerId: "openai",
      predecessor: { engineSessionId: "engine-predecessor" },
      targetBasisId: "basis-new",
      targetReference: "thread/start",
      continuationHash: sha256("failed-transition")
    };
    await expect(sessions.mutateSelection("fixture", created.sessionId, { instructionBasisId: "basis-old", methodSelectionRevision: 0 }, current => ({
      session: { ...current, selectedMethods: [method], methodSelectionRevision: 1, instructionBasisId: "basis-new" },
      history: { type: "selection.changed", roleId: "WORKING_ITEMS", interactionMode: "chat", permissionMode: "ask", selectedMethods: [method] },
      providerSpanPreparation: preparation,
      providerSpanCommitmentReference: "provider-commit-failed"
    }))).rejects.toThrow("simulated history failure");
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({
      instructionBasisId: "basis-old",
      methodSelectionRevision: 0,
      engineSessionId: "engine-predecessor"
    });
    expect((await sessions.instructionBases.history("fixture", created.sessionId)).map((record) => record.type))
      .toEqual(["provider-span.prepared", "provider-span.failed"]);

    const openPreparation = { ...preparation, preparationId: "preparation-cancelled", targetBasisId: "basis-cancelled", continuationHash: sha256("cancelled-transition") };
    await originalAppend("fixture", created.sessionId, openPreparation);
    await sessions.cancelProviderSpanPreparation("fixture", created.sessionId, openPreparation.preparationId, "user cancelled before start");
    await expect(sessions.recordProviderSpanSessionInit("fixture", created.sessionId, openPreparation.preparationId, {
      sessionInitEventId: "late-init",
      engineSessionId: "must-not-commit",
      providerSpanId: "late-span"
    })).rejects.toMatchObject({ status: 409 });
    expect(await sessions.get("fixture", created.sessionId)).toMatchObject({ engineSessionId: "engine-predecessor" });
  });

  it("reads historical v1 sessions and v2 events without rewriting their files", async () => {
    const { runtime, projects } = await fixture();
    const sessions = new SessionStore(runtime, projects);
    const session = await sessions.create({
      projectId: "fixture",
      role: "agent1",
      engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" }
    });
    const sessionPath = join(runtime, "projects", "fixture", "sessions", session.sessionId, "session.json");
    const raw = JSON.parse(await readFile(sessionPath, "utf8"));
    raw.schemaVersion = "chirality.session/v1";
    raw.persona = "CHANGE";
    const legacyBytes = `${JSON.stringify(raw)}\n`;
    await writeFile(sessionPath, legacyBytes, "utf8");
    const event = {
      schemaVersion: 2,
      eventId: "event-v2",
      sequence: 0,
      timestamp: "2026-09-09T00:00:00.000Z",
      projectId: "fixture",
      sessionId: session.sessionId,
      turnId: "turn-v2",
      type: "turn.completed",
      data: { outcome: "completed" }
    };
    const eventsPath = join(runtime, "projects", "fixture", "sessions", session.sessionId, "events.jsonl");
    const eventBytes = `${JSON.stringify(event)}\n`;
    await writeFile(eventsPath, eventBytes, "utf8");
    const read = await new SessionStore(runtime, projects).get("fixture", session.sessionId);
    expect(read).toMatchObject({ persona: "CHANGE", roleId: "WORKING_ITEMS" });
    expect((await sessions.replay("fixture", session.sessionId))[0]).toEqual(event);
    expect(await readFile(sessionPath, "utf8")).toBe(legacyBytes);
    expect(await readFile(eventsPath, "utf8")).toBe(eventBytes);
  });
});

describe("method transitions", () => {
  it("retains a forbidden historical skill in the from-boundary but refuses to select it again", () => {
    const historicalSkill = { sourceRootId: "project-history", source: "project" as const, kind: "skill" as const, name: "historical-skill" };
    const nextWorkflow = { sourceRootId: "project-current", source: "project" as const, kind: "workflow" as const, name: "current-workflow" };
    const decision = evaluateMethodTransition({
      sessionId: "session-history",
      sessionStatus: "completed",
      currentRoleId: "WORKING_ITEMS",
      currentMethods: [historicalSkill],
      nextMethods: [nextWorkflow],
      methodCompatibility: "incompatible",
      boundaryConfirmed: true,
      recordContinuationBoundary: true
    });
    expect(decision.continuationBoundary?.fromMethods).toEqual([historicalSkill]);
    expect(decision.selectedMethods).toEqual([nextWorkflow]);
    expect(() => evaluateMethodTransition({
      sessionId: "session-history",
      sessionStatus: "completed",
      currentRoleId: "WORKING_ITEMS",
      currentMethods: [historicalSkill],
      nextMethods: [historicalSkill],
      methodCompatibility: "compatible",
      boundaryConfirmed: true
    })).toThrow(expect.objectContaining({ code: "FORBIDDEN", status: 403 }));
  });

  it("rejects incompatible replacement until a confirmed non-running boundary", () => {
    const base = {
      sessionId: "session-3",
      currentRoleId: "WORKING_ITEMS",
      currentMethods: [{ ...method, name: "legacy-change" }],
      nextMethods: [method],
      methodCompatibility: "incompatible" as const
    };
    expect(() => evaluateMethodTransition({
      ...base,
      sessionStatus: "running",
      boundaryConfirmed: true
    })).toThrow(expect.objectContaining({ status: 409 }));
    expect(() => evaluateMethodTransition({
      ...base,
      sessionStatus: "completed",
      boundaryConfirmed: false
    })).toThrow(expect.objectContaining({ status: 409 }));
  });

  it("changes methods without inventing a role change and records provider continuation", () => {
    const decision = evaluateMethodTransition({
      sessionId: "session-4",
      sessionStatus: "completed",
      currentRoleId: "WORKING_ITEMS",
      currentMethods: [{ ...method, name: "legacy-change" }],
      nextMethods: [method],
      methodCompatibility: "incompatible",
      boundaryConfirmed: true,
      activeProviderSpan: { providerId: "openai", spanId: "thread-123" }
    });
    expect(decision.roleId).toBe("WORKING_ITEMS");
    expect(decision.continuationBoundary).toMatchObject({
      fromRoleId: "WORKING_ITEMS",
      toRoleId: "WORKING_ITEMS",
      providerId: "openai",
      providerSpanId: "thread-123"
    });
  });
});
