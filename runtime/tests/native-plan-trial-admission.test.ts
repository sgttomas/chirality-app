import { createHash } from "node:crypto";
import { mkdtemp, realpath, rm } from "node:fs/promises";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { assertAdmittedNativePlanEvent, assertQualifiedNativePlanEvent, type NativePlanAdapterTrialAdmission } from "../packages/contracts/src/v3.js";
import { EngineRegistry } from "../packages/core/src/engine-registry.js";
import { RuntimeMethodService } from "../packages/core/src/runtime-method-service.js";
import { ProjectRegistry } from "../packages/core/src/project-registry.js";
import { SessionStore } from "../packages/core/src/session-store.js";
import { TrustedNativePlanRegistry } from "../packages/core/src/native-plan-registry.js";
import { createProjectFixture } from "./helpers.js";

const cleanup: string[] = [];
const sha = (value: string) => createHash("sha256").update(value).digest("hex");
afterEach(async () => { await Promise.all(cleanup.splice(0).map(path => rm(path, { recursive: true, force: true }))); });

async function fixture() {
  const root = await realpath(await mkdtemp("/tmp/chirality-native-plan-trial-")); cleanup.push(root);
  const runtime = join(root, "runtime"), { manifestPath } = await createProjectFixture(root);
  const projects = new ProjectRegistry(runtime); await projects.register(manifestPath, { approvedBy: "test", approvalReference: "D-TRIAL" });
  const sessions = new SessionStore(runtime, projects);
  const created = await sessions.create({ projectId: "fixture", role: "agent0", engineSelection: { adapterId: "codex-app-server", providerId: "openai", model: "selected-after-login" } });
  await sessions.update({ ...created, status: "running" });
  const session = await sessions.get("fixture", created.sessionId);
  await sessions.appendEvent("fixture", { sessionId: session.sessionId, turnId: "client-turn", type: "turn.accepted", data: { message: "human foreground trial" } });
  const admission: NativePlanAdapterTrialAdmission = { adapterId: "codex-app-server", providerId: "openai", dispositionId: "worker-trial-record", admissionSha256: sha("same accepted worker trial basis"), evidenceClass: "native-adapter-local-human-trial" };
  const replies: unknown[] = [];
  const registry = new TrustedNativePlanRegistry({ projectId: "fixture", sessions, admission });
  const binding = { projectId: "fixture", sessionId: session.sessionId, clientTurnId: "client-turn", workerId: "worker", generation: "generation" };
  const bridge = { async drainNativePlanEvents() { return []; }, async pendingNativePlanClarifications() { return []; }, async replyNativePlanClarification(_worker: string, _generation: string, requestId: string | number, answers: unknown) { replies.push({ requestId, answers }); return { sent: true as const }; } };
  return { projects, sessions, session, admission, registry, binding, bridge, replies };
}

describe("native Plan local human trial admission", () => {
  it("keeps the qualified validator strict while admitting the exact trial event union", () => {
    const admission: NativePlanAdapterTrialAdmission = { adapterId: "codex-app-server", providerId: "openai", dispositionId: "worker-trial-record", admissionSha256: sha("worker"), evidenceClass: "native-adapter-local-human-trial" };
    const event = { qualificationState: "trial" as const, eventId: "event", occurredAt: "2026-09-10T00:00:00.000Z", admission, plan: { steps: ["observe"] } };
    expect(() => assertQualifiedNativePlanEvent(event)).toThrow();
    expect(() => assertAdmittedNativePlanEvent(event)).not.toThrow();
    expect(() => assertAdmittedNativePlanEvent({ ...event, admission: { ...admission, admissionSha256: "0".repeat(64), extra: true } } as any)).toThrow();
  });

  it("persists trial revisions and clarifications under one exact worker admission", async () => {
    const f = await fixture();
    expect(await f.registry.capability(f.session)).toEqual({ schemaVersion: "chirality.native-plan-capability/v3", status: "trial", admission: f.admission });
    await f.registry.open(f.binding, f.bridge);
    const event = { projectId: "fixture", sessionId: f.session.sessionId, clientTurnId: "client-turn", providerThreadId: "provider-thread", providerTurnId: "provider-turn", eventId: "event-one", occurredAt: "2026-09-10T00:00:00.000Z", plan: { steps: ["observe", "report"] } };
    const clarification = { ...f.binding, providerThreadId: "provider-thread", providerTurnId: "provider-turn", requestId: "question", itemId: "item", questions: [{ id: "scope", header: "Scope", question: "Continue?", options: [], isOther: true, isSecret: false }], isBlocking: true, autoResolutionMs: null };
    await f.registry.capture(f.binding, [event], [clarification]);
    expect(await f.registry.revisions("fixture", f.session.sessionId)).toMatchObject({ status: "trial", admission: f.admission, revisions: [{ revision: 1, sourceEvent: { qualificationState: "trial", admission: f.admission, binding: { clientTurnId: "client-turn" } } }] });
    expect(await f.registry.clarifications("fixture", f.session.sessionId)).toMatchObject({ status: "trial", admission: f.admission, clarifications: [{ requestId: "question" }] });
    await f.registry.replyClarification("fixture", f.session.sessionId, { requestId: "question", answers: { scope: { answers: ["yes"] } } });
    expect(f.replies).toEqual([{ requestId: "question", answers: { scope: { answers: ["yes"] } } }]);
    const history = await f.sessions.instructionBases.history("fixture", f.session.sessionId), record = history.find(value => value.type === "native-plan.revised")!;
    expect(record).toMatchObject({ provenance: "trusted-native-plan-registry", admissionSha256: sha(JSON.stringify(f.admission)), revision: { sourceEvent: { qualificationState: "trial", admission: f.admission } } });
    expect(record).not.toHaveProperty("qualificationSha256");
    await f.registry.close(f.binding);
    const historical = new RuntimeMethodService(f.projects, f.sessions, new EngineRegistry());
    expect(await historical.listNativePlanRevisions("fixture", f.session.sessionId)).toMatchObject({ status: "trial", admission: f.admission, revisions: [{ revision: 1 }] });
  });

  it("rejects event substitution and cross-family capture", async () => {
    const f = await fixture(); await f.registry.open(f.binding, f.bridge);
    const event = { projectId: "fixture", sessionId: f.session.sessionId, clientTurnId: "client-turn", providerThreadId: "provider-thread", providerTurnId: "provider-turn", eventId: "same-event", occurredAt: "2026-09-10T00:00:00.000Z", plan: { steps: ["first"] } };
    await f.registry.capture(f.binding, [event], []);
    await expect(f.registry.capture(f.binding, [{ ...event, plan: { steps: ["substituted"] } }], [])).rejects.toThrow("reused with different content");
    await expect(f.registry.capture({ ...f.binding, clientTurnId: "other-turn" }, [], [])).rejects.toThrow("live worker generation");
  });
});
