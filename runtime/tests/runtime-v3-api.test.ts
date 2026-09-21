import { RuntimeError } from "@chirality/runtime-contracts";
import { mkdir, mkdtemp, readFile, realpath, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import type { AgentEnginePort, AgentEngineRunInput, ContextSuccessorRequest, OmlxControlPort, PreparedContextSuccessor, UIEvent } from "@chirality/runtime-contracts";
import { AuthRegistry, EngineRegistry, ProjectRegistry, ResidencyCoordinator, RuntimeService, SessionStore, TurnCoordinator } from "@chirality/runtime-core";
import { RuntimeDaemon } from "../packages/daemon/src/runtime-daemon.js";
import { RuntimeClient } from "@chirality/runtime-client";

const daemons: RuntimeDaemon[] = [];
afterEach(async () => { await Promise.all(daemons.splice(0).map(daemon => daemon.stop().catch(() => undefined))); });

async function setup(startTurn: AgentEnginePort["startTurn"], nativePlan?: any, successor?: Partial<Pick<AgentEnginePort, "preflight" | "prepareContextSuccessor" | "cancelContextSuccessor" | "interrupt">>, runtimeControlTools = true) {
  const directory = await mkdtemp(join(tmpdir(), "chirality-v3-api-"));
  const projectRoot = join(directory, "project");
  const runtime = join(directory, "runtime");
  await mkdir(join(projectRoot, ".chirality", "workflows", "fixture-method"), { recursive: true });
  await writeFile(join(projectRoot, "AGENTS.md"), "# Fixture project\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "fixture-method", "WORKFLOW.md"), "---\nname: fixture-method\ndescription: Runtime API fixture method.\n---\n\n# Method body\nExact fixture instructions.\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "fixture-method", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"] })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "lazy-method"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "lazy-method", "WORKFLOW.md"), "---\nname: lazy-method\ndescription: Dynamically loaded fixture.\n---\n\nLAZY_METHOD_EXACT\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "lazy-method", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"] })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "lazy-method", "resources"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "lazy-method", "resources", "note.md"), "LAZY_RESOURCE_EXACT\n", "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "lazy-method-two"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "lazy-method-two", "WORKFLOW.md"), "---\nname: lazy-method-two\ndescription: Second dynamically loaded fixture.\n---\n\nLAZY_METHOD_TWO_EXACT\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "lazy-method-two", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"] })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "manager-method"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "manager-method", "WORKFLOW.md"), "---\nname: manager-method\ndescription: Manager routed fixture.\n---\n\nMANAGER_BODY_MUST_NOT_BE_SUPPLIED\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "manager-method", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELPS_HUMANS"] })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "restricted-method"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "restricted-method", "WORKFLOW.md"), "---\nname: restricted-method\ndescription: Restricted dynamic fixture.\n---\n\nRESTRICTED_BODY\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "restricted-method", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"], tools: { capabilities: ["bash"], commands: ["git status"] } })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "manager-readonly"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "manager-readonly", "WORKFLOW.md"), "---\nname: manager-readonly\ndescription: Read-only manager fixture.\n---\n\nREAD_ONLY_MANAGER_BODY\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "manager-readonly", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELPS_HUMANS"], tools: { capabilities: ["read"] } })}\n`, "utf8");
  await mkdir(join(projectRoot, ".chirality", "workflows", "task-method"), { recursive: true });
  await writeFile(join(projectRoot, ".chirality", "workflows", "task-method", "WORKFLOW.md"), "---\nname: task-method\ndescription: TASK lifecycle fixture.\n---\n\nTASK_METHOD_BODY\n", "utf8");
  await writeFile(join(projectRoot, ".chirality", "workflows", "task-method", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["TASK"], tools: { capabilities: ["read"] } })}\n`, "utf8");
  const manifestPath = join(projectRoot, "chirality.project.json");
  await writeFile(manifestPath, `${JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "v3-api", displayName: "v3 API", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["stub"], embeddedUi: { declared: false } })}\n`, "utf8");
  const instructionRoot = resolve(process.cwd(), "../..");
  const projects = new ProjectRegistry(runtime, { CHIRALITY_INSTRUCTION_ROOT: instructionRoot });
  const sessions = new SessionStore(runtime, projects);
  const engines = new EngineRegistry();
  engines.register({ descriptor: { adapterId: "stub", providerId: "stub", capabilities: { credentials: false, tools: true, attachments: true, interruption: true, durableResume: true, compaction: true, runtimeControlTools } }, subject: "stub", async preflight() {}, startTurn, async interrupt() {}, ...successor });
  const control: OmlxControlPort = { async listStatus() { return []; }, async load() {}, async unload() {} };
  const residency = new ResidencyCoordinator(control, runtime);
  const service = new RuntimeService(projects, sessions, engines, residency, new TurnCoordinator(projects, sessions, engines, residency), new AuthRegistry(runtime), { async get() { return undefined; }, async status() { return { configured: false }; }, async set() {}, async remove() {} }, undefined, undefined, undefined, { async resolve({ agentType }) { return { role: agentType === 0 ? "agent0" : "agent1", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } }; } }, nativePlan);
  const registered = await service.registerProject(manifestPath, "test", "v3-api-test");
  const socketPath = join(directory, "runtime.sock");
  const daemon = new RuntimeDaemon({ runtimeDirectory: runtime, socketPath, service });
  daemons.push(daemon);
  await daemon.start();
  const client = new RuntimeClient({ socketPath, tokenFile: registered.tokenFile });
  return { directory, projectRoot, runtime, projects, sessions, service, client, daemon };
}

async function drain(source: Awaited<ReturnType<RuntimeClient["turnSession"]>>): Promise<UIEvent[]> { const events: UIEvent[] = []; for await (const event of source) events.push(event); return events; }

describe("v3 Runtime API integration", () => {
  it("authenticates catalog/context routes and supplies frozen context plus callable loader across restart/replay", async () => {
    const captured: AgentEngineRunInput[] = [];
    let loadResult: unknown;
    const fixture = await setup(async function* (input) {
      captured.push(input);
      loadResult = await input.runtimeTools?.find(tool => tool.name === "chirality_load_method")?.execute({ methods: [{ kind: "workflow", name: "fixture-method" }] }, new AbortController().signal);
      yield { type: "session:init", data: { engineSessionId: `engine-${captured.length}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "harness:event", data: { schemaVersion: 1, eventId: `completed-${captured.length}`, sessionId: input.session.sessionId, turnId: input.turnId, timestamp: new Date().toISOString(), type: "turn.completed", data: {} } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const roles = await fixture.client.listRoles("v3-api");
    expect(roles.defaultRole).toBe("HELP_HUMAN");
    expect(roles.roles.map(role => [role.id, role.directEntry])).toEqual([["HELP_HUMAN", true], ["HELPS_HUMANS", true], ["WORKING_ITEMS", true], ["TASK", false]]);
    const methods = await fixture.client.listMethods("v3-api");
    const selected = methods.methods.find(method => method.name === "fixture-method" && method.source === "project")!;
    expect(selected.sourceRootId).toMatch(/^project-[a-f0-9]{24}$/u);
    const inspection = await fixture.client.inspectMethod("v3-api", selected.qualifiedId);
    expect(inspection.entrypoint.content).toContain("Exact fixture instructions");
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    expect(session).toMatchObject({ role: "agent0", roleId: "HELP_HUMAN", persona: "HELP_HUMAN" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "first prompt" }));
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "second prompt" }));
    expect(captured.map(input => input.message)).toEqual(["first prompt", "second prompt"]);
    expect(captured[0]?.instructionContext?.supplied.some(entry => entry.content.includes("Exact fixture instructions"))).toBe(true);
    const routed = await fixture.client.resolveSelectedContext("v3-api", session.sessionId, { roleId: "HELP_HUMAN", interactionMode: "chat", permissionMode: "ask", methods: [{ kind: "workflow", name: "manager-method" }] });
    expect(routed.dispositions).toContainEqual(expect.objectContaining({ route: "managed-delegation", activeRoleCompatible: false }));
    expect(routed.supplied.find(entry => entry.kind === "selection-metadata")?.content).toContain("manager-method");
    expect(routed.supplied.find(entry => entry.kind === "selection-metadata")?.content).toContain("managed-delegation");
    expect(routed.supplied.some(entry => entry.content.includes("MANAGER_BODY_MUST_NOT_BE_SUPPLIED"))).toBe(false);
    expect(JSON.stringify(loadResult)).toContain("Exact fixture instructions");
    const replay = await fixture.client.replaySession("v3-api", session.sessionId);
    expect(replay.events.filter(event => event.type === "turn.accepted")).toHaveLength(2);
    expect(replay.instructionBases).toHaveLength(1);
    expect(replay.instructionBases[0]?.selectedMethods).toEqual([expect.objectContaining({ name: "fixture-method" })]);
    expect(replay.instructionBases[0]?.compatibilityInputs).toEqual([]);
    expect(replay.instructionBases[0]?.compatibilityMappings).toEqual([]);
    // An engine without successor preparation transitions additively: the
    // selection changes durably and the next turn carries a context update.
    await expect(fixture.client.replaceSelectedMethods("v3-api", session.sessionId, { methods: [] })).resolves.toMatchObject({ transition: { status: "additive", successorAvailable: false } });
    await fixture.daemon.stop();
    daemons.splice(daemons.indexOf(fixture.daemon), 1);
    const restarted = new RuntimeDaemon({ runtimeDirectory: fixture.runtime, socketPath: join(fixture.directory, "restart.sock"), service: fixture.service });
    daemons.push(restarted); await restarted.start();
    const afterRestart = new RuntimeClient({ socketPath: join(fixture.directory, "restart.sock"), tokenFile: (fixture.client as any).options.tokenFile });
    expect((await afterRestart.replaySession("v3-api", session.sessionId)).events.filter(event => event.type === "turn.accepted")).toHaveLength(2);
    expect(await afterRestart.getNativePlanCapability("v3-api", session.sessionId)).toMatchObject({ status: "unavailable" });
  }, 15_000);

  it("refuses project skills across discovery, inspection, context resolution, and dynamic loading", async () => {
    let dynamicLoadError: unknown;
    const fixture = await setup(async function* (input) {
      const projectWorkflow = (await fixture.client.listMethods("v3-api")).methods.find(method => method.source === "project" && method.kind === "workflow")!;
      try {
        await input.runtimeTools?.find(tool => tool.name === "chirality_load_method")?.execute({
          methods: [{ sourceRootId: projectWorkflow.sourceRootId, source: "project", kind: "skill", name: "untrusted-skill" }]
        }, new AbortController().signal);
      } catch (error) { dynamicLoadError = error; }
      yield { type: "session:init", data: { engineSessionId: "untrusted-skill-engine", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const skillPath = join(fixture.projectRoot, ".agents", "skills", "untrusted-skill", "SKILL.md");
    await mkdir(join(fixture.projectRoot, ".agents", "skills", "untrusted-skill"), { recursive: true });
    await writeFile(skillPath, "---\nname: untrusted-skill\ndescription: Must remain unavailable.\n---\n\nUNTRUSTED_SKILL_BODY\n", "utf8");
    const methods = await fixture.client.listMethods("v3-api");
    expect(methods.methods).not.toContainEqual(expect.objectContaining({ kind: "skill", name: "untrusted-skill" }));
    const projectSourceRootId = methods.methods.find(method => method.source === "project" && method.kind === "workflow")!.sourceRootId;
    const qualified = `${projectSourceRootId}:project:skill:untrusted-skill`;
    await expect(fixture.client.inspectMethod("v3-api", qualified)).rejects.toMatchObject({ code: "FORBIDDEN" });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    await expect(fixture.client.resolveSelectedContext("v3-api", session.sessionId, {
      roleId: "HELP_HUMAN", interactionMode: "chat", permissionMode: "ask", methods: [{ kind: "skill", name: "untrusted-skill" }]
    })).rejects.toMatchObject({ code: "NOT_FOUND" });
    await expect(fixture.client.resolveSelectedContext("v3-api", session.sessionId, {
      roleId: "HELP_HUMAN", interactionMode: "chat", permissionMode: "ask",
      methods: [{ sourceRootId: projectSourceRootId, source: "project", kind: "skill", name: "untrusted-skill" }]
    })).rejects.toMatchObject({ code: "FORBIDDEN" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "attempt untrusted skill load" }));
    expect(dynamicLoadError).toMatchObject({ code: "FORBIDDEN", status: 403 });
    expect((await fixture.sessions.get("v3-api", session.sessionId)).selectedMethods).toEqual([]);
    expect(JSON.stringify(await fixture.sessions.instructionBases.history("v3-api", session.sessionId))).not.toContain("UNTRUSTED_SKILL_BODY");
  });

  it("round-trips a contained project workflow revision while leaving its prior frozen basis unchanged", async () => {
    const captured: AgentEngineRunInput[] = [];
    const fixture = await setup(async function* (input) {
      captured.push(input);
      yield { type: "session:init", data: { engineSessionId: `workflow-roundtrip-${captured.length}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const packageRoot = join(fixture.projectRoot, ".chirality", "workflows", "roundtrip-workflow");
    const workflowPath = join(packageRoot, "WORKFLOW.md");
    await mkdir(packageRoot, { recursive: true });
    await writeFile(workflowPath, "---\nname: roundtrip-workflow\ndescription: Contained roundtrip fixture.\n---\n\nROUNDTRIP_REVISION_ONE\n", "utf8");

    const firstDescriptor = (await fixture.client.listMethods("v3-api")).methods.find(method => method.name === "roundtrip-workflow")!;
    expect(firstDescriptor).toMatchObject({ source: "project", kind: "workflow" });
    expect(firstDescriptor.qualifiedId).toBe(`${firstDescriptor.sourceRootId}:project:workflow:roundtrip-workflow`);
    const firstInspection = await fixture.client.inspectMethod("v3-api", firstDescriptor.qualifiedId);
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "roundtrip-workflow" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "freeze revision one" }));
    const frozenBefore = (await fixture.client.replaySession("v3-api", session.sessionId)).instructionBases[0]!;
    expect(frozenBefore.suppliedEntries.some(entry => entry.content.includes("ROUNDTRIP_REVISION_ONE"))).toBe(true);

    await writeFile(workflowPath, "---\nname: roundtrip-workflow\ndescription: Contained roundtrip fixture.\n---\n\nROUNDTRIP_REVISION_TWO\n", "utf8");
    const refreshedDescriptor = (await fixture.client.listMethods("v3-api")).methods.find(method => method.name === "roundtrip-workflow")!;
    expect(refreshedDescriptor.qualifiedId).toBe(firstDescriptor.qualifiedId);
    const secondInspection = await fixture.client.inspectMethod("v3-api", refreshedDescriptor.qualifiedId);
    expect(secondInspection.entrypoint.sha256).not.toBe(firstInspection.entrypoint.sha256);
    expect(secondInspection.entrypoint.content).toContain("ROUNDTRIP_REVISION_TWO");
    const refreshed = await fixture.client.resolveSelectedContext("v3-api", session.sessionId, {
      roleId: "HELP_HUMAN", interactionMode: "chat", permissionMode: "ask", methods: [{ sourceRootId: firstDescriptor.sourceRootId, source: "project", kind: "workflow", name: "roundtrip-workflow" }]
    });
    expect(refreshed.documents[0]?.sha256).toBe(secondInspection.entrypoint.sha256);
    const frozenAfter = (await fixture.client.replaySession("v3-api", session.sessionId)).instructionBases[0]!;
    expect(frozenAfter).toEqual(frozenBefore);
    expect(JSON.stringify(frozenAfter)).not.toContain("ROUNDTRIP_REVISION_TWO");
  });

  it("preserves legacy mapping inputs and decisions in selected context and frozen replay", async () => {
    let captured: AgentEngineRunInput | undefined;
    const fixture = await setup(async function* (input) {
      captured = input;
      yield { type: "session:init", data: { engineSessionId: "legacy-mapping-engine", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [] });
    const legacyEvents = await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "legacy mapping", workflow: "deliverable-consistency", taskSkill: "deliverable-consistency" }));
    if (captured === undefined) throw new Error(JSON.stringify(legacyEvents));
    expect(captured?.instructionContext?.compatibilityInputs).toEqual(["Workflow", "TaskSkill"]);
    expect(captured?.instructionContext?.compatibilityMappings).toEqual([
      { field: "Workflow", original: "deliverable-consistency", mapping: "converted-alias", resolved: { sourceRootId: "chirality-root", source: "bundled", kind: "skill", name: "deliverable-consistency" } },
      { field: "TaskSkill", original: "deliverable-consistency", normalizedAlias: "deliverable-consistency", mapping: "converted-alias", resolved: { sourceRootId: "chirality-root", source: "bundled", kind: "skill", name: "deliverable-consistency" } }
    ]);
    const metadata = captured?.instructionContext?.supplied.find(entry => entry.kind === "selection-metadata")?.content ?? "";
    expect(metadata).toContain('"original":"deliverable-consistency"');
    expect(metadata).toContain('"mapping":"converted-alias"');
    expect(captured?.instructionContext?.executionRoots).toEqual({
      workingRoot: { path: await realpath(fixture.projectRoot), origin: "registered-project-root", identitySha256: expect.stringMatching(/^[a-f0-9]{64}$/u) },
      toolRoot: { path: resolve(process.cwd(), "../.."), origin: "trusted-runtime-instruction-root", identitySha256: expect.stringMatching(/^[a-f0-9]{64}$/u) }
    });
    expect(JSON.parse(metadata).executionRoots).toEqual(captured?.instructionContext?.executionRoots);
    const replay = await fixture.client.replaySession("v3-api", session.sessionId);
    expect(replay.instructionBases[0]?.compatibilityInputs).toEqual(["Workflow", "TaskSkill"]);
    expect(replay.instructionBases[0]?.compatibilityMappings).toEqual(captured?.instructionContext?.compatibilityMappings);
    expect(replay.instructionBases[0]?.suppliedEntries.find(entry => entry.kind === "selection-metadata")?.content).toContain('"trusted-runtime-instruction-root"');
  });

  it("rejects a method replacement after turn acceptance while provider preflight is delayed", async () => {
    let release!: () => void;
    const gate = new Promise<void>(resolveGate => { release = resolveGate; });
    const fixture = await setup(async function* (input) { await gate; yield { type: "session:init", data: { engineSessionId: "engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    const stream = await fixture.client.turnSession("v3-api", session.sessionId, { message: "hold" });
    const iterator = stream[Symbol.asyncIterator]();
    await iterator.next();
    await expect(fixture.service.replaceSelectedMethods("v3-api", session.sessionId, { methods: [] })).rejects.toMatchObject({ code: "SESSION_TURN_IN_PROGRESS" });
    release();
    while (!(await iterator.next()).done) { /* drain */ }
  });

  it("freezes successor dialogue only after acquiring the selection lock", async () => {
    let turn = 0;
    let successorTranscript = "";
    const fixture = await setup(async function* () {
      turn += 1;
      yield { type: "session:init", data: { engineSessionId: `race-engine-${turn}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, {
      async prepareContextSuccessor(request) {
        successorTranscript = request.continuationContext.transcript;
        return { preparationId: "race-successor", adapterId: "stub", providerId: "stub", predecessorEngineSessionId: request.predecessorEngineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` };
      },
      async cancelContextSuccessor() {}
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "first accepted message" }));
    const originalMutate = fixture.sessions.mutateSelection.bind(fixture.sessions);
    let releaseMutation!: () => void;
    let markWaiting!: () => void;
    const mutationWaiting = new Promise<void>(resolveWaiting => { markWaiting = resolveWaiting; });
    const mutationGate = new Promise<void>(resolveGate => { releaseMutation = resolveGate; });
    fixture.sessions.mutateSelection = (async (...args: Parameters<typeof originalMutate>) => {
      markWaiting();
      await mutationGate;
      return originalMutate(...args);
    }) as typeof fixture.sessions.mutateSelection;
    const replacement = fixture.service.replaceSelectedMethods("v3-api", session.sessionId, { boundaryConfirmed: true, methods: [] });
    await mutationWaiting;
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "intervening accepted message" }));
    releaseMutation();
    await replacement;
    expect(successorTranscript).toContain("first accepted message");
    expect(successorTranscript).toContain("intervening accepted message");
  });

  it("keeps the persisted session running while the provider is paused after session:init", async () => {
    let release!: () => void;
    const gate = new Promise<void>(resolveGate => { release = resolveGate; });
    const fixture = await setup(async function* () { yield { type: "session:init", data: { engineSessionId: "paused-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; await gate; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    const iterator = (await fixture.client.turnSession("v3-api", session.sessionId, { message: "pause after init" }))[Symbol.asyncIterator]();
    for (;;) { const event = await iterator.next(); if (event.value?.type === "session:init") break; }
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ status: "running", engineSessionId: "paused-engine" });
    await expect(fixture.service.replaceSelectedMethods("v3-api", session.sessionId, { methods: [] })).rejects.toMatchObject({ code: "SESSION_TURN_IN_PROGRESS" });
    release(); while (!(await iterator.next()).done) { /* drain */ }
  });

  it("keeps an explicitly untyped compatibility session on its legacy input basis", async () => {
    let captured: AgentEngineRunInput | undefined;
    const fixture = await setup(async function* (input) { captured = input; yield { type: "session:init", data: { engineSessionId: "legacy-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", persona: "UNTYPED" });
    expect(session).toMatchObject({ schemaVersion: "chirality.session/v2", persona: "UNTYPED", role: "agent1" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "legacy prompt" }));
    expect(captured?.message).toBe("legacy prompt");
    expect(captured?.instructionContext).toBeUndefined();
    expect(captured?.runtimeTools).toBeUndefined();
  });

  it("supplies and freezes exact v3 context for an actual adapter boot", async () => {
    let captured: AgentEngineRunInput | undefined;
    const fixture = await setup(async function* (input) { captured = input; yield { type: "session:init", data: { engineSessionId: "boot-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await fixture.service.bootSession("v3-api", session.sessionId);
    expect(captured?.message).toBe("bootstrap");
    expect(captured?.instructionContext?.supplied).toContainEqual(expect.objectContaining({ kind: "method-body", content: expect.stringContaining("Exact fixture instructions") }));
    expect(captured?.runtimeTools?.map(tool => tool.name)).toContain("chirality_load_method");
    const replay = await fixture.client.replaySession("v3-api", session.sessionId);
    expect(replay.events).toContainEqual(expect.objectContaining({ type: "turn.accepted", data: expect.objectContaining({ message: "bootstrap", boot: true }) }));
    expect(replay.instructionBases).toContainEqual(expect.objectContaining({ basisId: captured?.instructionContext?.basisPreview.id }));
  });

  it("boots a v3 session under its persisted permission mode rather than the legacy chat mode", async () => {
    let captured: AgentEngineRunInput | undefined;
    const fixture = await setup(async function* (input) { captured = input; yield { type: "session:init", data: { engineSessionId: "boot-mode-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", permissionMode: "workspaceWrite" });
    expect(session).toMatchObject({ schemaVersion: "chirality.session/v3", permissionMode: "workspaceWrite" });
    expect(["readOnly", "ask", "workspaceWrite", "bypass"]).not.toContain(session.mode);
    await fixture.service.bootSession("v3-api", session.sessionId);
    expect(captured?.message).toBe("bootstrap");
    expect(captured?.opts.mode).toBe("workspaceWrite");
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ status: "idle", permissionMode: "workspaceWrite" });
  });

  it("settles disconnected boot through real interruption and rejects a duplicate boot", async () => {
    let release!: () => void, began!: () => void;
    const started = new Promise<void>(resolve => { began = resolve; });
    const terminal = new Promise<void>(resolve => { release = resolve; });
    let interrupts = 0;
    const fixture = await setup(async function* () {
      yield { type: "session:init", data: { engineSessionId: "cancel-boot", adapterId: "stub", providerId: "stub", model: "fixture" } };
      began(); await terminal;
      yield { type: "process:exit", data: { exitCode: 130, interrupted: true } };
    }, undefined, { async interrupt() { interrupts++; release(); } });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    const controller = new AbortController();
    const pending = fixture.service.bootSession("v3-api", session.sessionId, {}, undefined, controller.signal);
    const failed = expect(pending).rejects.toMatchObject({ details: { reason: "BOOT_CANCELLED", sessionId: session.sessionId } });
    await started;
    await expect(fixture.service.bootSession("v3-api", session.sessionId)).rejects.toMatchObject({ code: "SESSION_TURN_IN_PROGRESS" });
    controller.abort(); await failed;
    expect(interrupts).toBe(1);
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ status: "failed" });
    expect((await fixture.sessions.get("v3-api", session.sessionId)).bootedAt).toBeUndefined();
  });

  it("propagates an HTTP boot disconnect to the service cancellation signal", async () => {
    const fixture = await setup(async function* () {});
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    let entered!: () => void, cancelled!: () => void;
    const began = new Promise<void>(resolve => { entered = resolve; });
    const stopped = new Promise<void>(resolve => { cancelled = resolve; });
    fixture.service.bootSession = async (_project, _session, _opts, _expected, signal) => {
      expect(signal).toBeDefined(); entered();
      await new Promise<void>(resolve => signal!.addEventListener("abort", () => { cancelled(); resolve(); }, { once: true }));
      throw new RuntimeError("ENGINE_UNAVAILABLE", "controlled disconnected boot");
    };
    const controller = new AbortController();
    const request = fixture.client.bootSession("v3-api", session.sessionId, {}, controller.signal);
    const failed = expect(request).rejects.toMatchObject({ operation: "boot", sessionId: session.sessionId });
    await began; controller.abort(); await failed; await stopped;
  });

  it("terminalizes an accepted v3 boot when preflight fails", async () => {
    const preflightFailure = new RuntimeError("ENGINE_UNAVAILABLE", "controlled preflight failure", 503, { reason: "CODEX_PROTOCOL_FAILURE" });
    preflightFailure.cause = new RuntimeError("ENGINE_UNAVAILABLE", "controlled retirement diagnostic", 503, { reason: "DESCENDANT_RECONCILIATION_REQUIRED", detachedCount: 1 });
    const fixture = await setup(async function* () { yield { type: "process:exit", data: { exitCode: 1 } }; }, undefined, { async preflight() { throw preflightFailure; } });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    await expect(fixture.service.bootSession("v3-api", session.sessionId)).rejects.toThrow("controlled preflight failure");
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ status: "failed" });
    expect(await fixture.sessions.replay("v3-api", session.sessionId)).toContainEqual(expect.objectContaining({ type: "turn.failed", data: expect.objectContaining({ boot: true, code: "ENGINE_UNAVAILABLE",
      details: { reason: "CODEX_PROTOCOL_FAILURE", cause: expect.objectContaining({ message: "controlled retirement diagnostic", details: { reason: "DESCENDANT_RECONCILIATION_REQUIRED", detachedCount: 1 } }) } }) }));
  });

  it("terminalizes an accepted v3 boot when the provider exits unsuccessfully", async () => {
    const fixture = await setup(async function* () { yield { type: "session:init", data: { engineSessionId: "failed-boot-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 1, error: "controlled provider failure" } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    await expect(fixture.service.bootSession("v3-api", session.sessionId)).rejects.toThrow("Boot turn did not initialize");
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ status: "failed" });
    expect((await fixture.sessions.replay("v3-api", session.sessionId)).filter(event => event.type === "turn.failed")).toHaveLength(1);
  });

  it("rejects a dynamic read-only method before exposing it while bash remains active", async () => {
    let loadError: unknown;
    const fixture = await setup(async function* (input) {
      try { await input.runtimeTools?.find(tool => tool.name === "chirality_load_method")?.execute({ methods: [{ kind: "workflow", name: "manager-readonly" }] }, new AbortController().signal); } catch (error) { loadError = error; }
      yield { type: "session:init", data: { engineSessionId: "manager-engine", adapterId: "stub", providerId: "stub", model: "fixture" } }; yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", roleId: "HELPS_HUMANS" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "restricted dynamic load", opts: { tools: ["bash"] } }));
    expect(loadError).toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { unavailableTools: ["bash"] } });
    expect((await fixture.sessions.instructionBases.history("v3-api", session.sessionId)).some(record => record.type === "resource.loaded" && record.content.includes("READ_ONLY_MANAGER_BODY"))).toBe(false);
  });

  it("activates a dynamically loaded method for later turns while preserving ordered selection", async () => {
    let loaded: any;
    let restrictedError: unknown;
    let turns = 0;
    const inputs: AgentEngineRunInput[] = [];
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      if (++turns === 2) {
        const loader = input.runtimeTools?.find(tool => tool.name === "chirality_load_method");
        expect((loader?.inputSchema as any).properties.resources.items.properties.paths.items).toEqual({ type: "string" });
        const lazy = (await fixture.client.listMethods("v3-api")).methods.find(method => method.name === "lazy-method" && method.source === "project")!;
        loaded = await loader?.execute({ methods: [{ kind: "workflow", name: "lazy-method" }], resources: [{ method: { sourceRootId: lazy.sourceRootId, source: lazy.source, kind: lazy.kind, name: lazy.name }, paths: ["resources/note.md"] }] }, new AbortController().signal);
        try { await loader?.execute({ methods: [{ kind: "workflow", name: "restricted-method" }] }, new AbortController().signal); } catch (error) { restrictedError = error; }
      }
      yield { type: "session:init", data: { engineSessionId: `dynamic-${turns}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "establish provider span" }));
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "load another method" }));
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "enforce loaded method on later turn" }));
    expect(JSON.stringify(loaded)).toContain("LAZY_METHOD_EXACT");
    expect(JSON.stringify(loaded)).toContain("LAZY_RESOURCE_EXACT");
    expect(restrictedError).toMatchObject({ code: "ENGINE_UNAVAILABLE", details: { unavailableOperation: "read" } });
    expect((await fixture.sessions.get("v3-api", session.sessionId)).selectedMethods).toEqual([
      expect.objectContaining({ name: "fixture-method" }),
      expect.objectContaining({ name: "lazy-method" })
    ]);
    expect((await fixture.sessions.get("v3-api", session.sessionId)).methodSelectionRevision).toBe(1);
    expect(inputs[2]?.instructionContext?.methods.map(method => method.name)).toEqual(["fixture-method", "lazy-method"]);
    const history = await fixture.sessions.instructionBases.history("v3-api", session.sessionId);
    expect(history).toContainEqual(expect.objectContaining({ type: "resource.loaded", turnId: expect.any(String), invocationId: expect.any(String), content: expect.stringContaining("LAZY_METHOD_EXACT"), method: expect.objectContaining({ name: "lazy-method" }) }));
    expect(history).toContainEqual(expect.objectContaining({ type: "selection.changed", reason: "agent-load", turnId: expect.any(String), invocationId: expect.any(String), selectedMethods: [expect.objectContaining({ name: "fixture-method" }), expect.objectContaining({ name: "lazy-method" })] }));
  });

  it("serializes concurrent dynamic-load union fingerprints for the next turn", async () => {
    const inputs: AgentEngineRunInput[] = [];
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      if (inputs.length === 1) {
        const loader = input.runtimeTools?.find(tool => tool.name === "chirality_load_method")!;
        await Promise.all([
          loader.execute({ methods: [{ kind: "workflow", name: "lazy-method" }] }, new AbortController().signal),
          loader.execute({ methods: [{ kind: "workflow", name: "lazy-method-two" }] }, new AbortController().signal)
        ]);
      }
      yield { type: "session:init", data: { engineSessionId: `concurrent-load-${inputs.length}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "load both concurrently" }));
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "run with exact concurrent union" }));
    expect(inputs).toHaveLength(2);
    expect(new Set(inputs[1]?.instructionContext?.methods.map(method => method.name))).toEqual(new Set(["fixture-method", "lazy-method", "lazy-method-two"]));
    const history = await fixture.sessions.instructionBases.history("v3-api", session.sessionId);
    const loads = history.filter(record => record.type === "resource.loaded");
    expect(loads.filter(record => record.content.includes("LAZY_METHOD_EXACT"))).toHaveLength(1);
    expect(loads.filter(record => record.content.includes("LAZY_METHOD_TWO_EXACT"))).toHaveLength(1);
    const changes = history.filter(record => record.type === "selection.changed" && record.reason === "agent-load");
    expect(changes).toHaveLength(2);
    expect(new Set(changes.at(-1)?.selectedMethods.map(method => method.name))).toEqual(new Set(["fixture-method", "lazy-method", "lazy-method-two"]));
    expect(changes.at(-1)?.instructionPolicySha256).toBe(inputs[1]?.instructionContext?.basisPreview.instructionPolicySha256);
  });

  it("returns and records bytes from the single locked union resolution", async () => {
    let loadResult: any;
    const inputs: AgentEngineRunInput[] = [];
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      if (inputs.length === 1) loadResult = await input.runtimeTools?.find(tool => tool.name === "chirality_load_method")?.execute({ methods: [{ kind: "workflow", name: "lazy-method" }] }, new AbortController().signal);
      yield { type: "session:init", data: { engineSessionId: `single-union-${inputs.length}`, adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const methodService = (fixture.service as unknown as { methods: { restrictRequestedTools: (...args: any[]) => Promise<string[]> } }).methods;
    const originalRestriction = methodService.restrictRequestedTools.bind(methodService);
    let releaseValidation!: () => void;
    let validationReached!: () => void;
    const validationGate = new Promise<void>(resolveGate => { releaseValidation = resolveGate; });
    const reached = new Promise<void>(resolveReached => { validationReached = resolveReached; });
    let gated = false;
    methodService.restrictRequestedTools = async (...args: any[]) => {
      const methods = args[3] as { name: string }[];
      if (!gated && methods.some(method => method.name === "lazy-method")) {
        gated = true;
        validationReached();
        await validationGate;
      }
      return originalRestriction(...args);
    };
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    const firstTurn = drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "load after descriptor validation" }));
    await reached;
    await writeFile(join(fixture.projectRoot, ".chirality", "workflows", "lazy-method", "WORKFLOW.md"), "---\nname: lazy-method\ndescription: Dynamically loaded fixture.\n---\n\nLAZY_METHOD_MUTATED_AT_LOCK\n", "utf8");
    releaseValidation();
    await firstTurn;
    expect(JSON.stringify(loadResult)).toContain("LAZY_METHOD_MUTATED_AT_LOCK");
    expect(JSON.stringify(loadResult)).not.toContain("LAZY_METHOD_EXACT");
    const loaded = (await fixture.sessions.instructionBases.history("v3-api", session.sessionId)).filter(record => record.type === "resource.loaded" && record.method.name === "lazy-method");
    expect(loaded).toHaveLength(1);
    expect(loaded[0]?.content).toContain("LAZY_METHOD_MUTATED_AT_LOCK");
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "use the exact locked baseline" }));
    expect(inputs).toHaveLength(2);
  });

  it("blocks instruction drift until an explicit same-reference successor is prepared", async () => {
    const inputs: AgentEngineRunInput[] = [];
    let preparation = 0;
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      yield { type: "session:init", data: { engineSessionId: inputs.length === 1 ? "drift-old" : "drift-new", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, {
      async prepareContextSuccessor(request) { return { preparationId: `drift-prepared-${++preparation}`, adapterId: "stub", providerId: "stub", predecessorEngineSessionId: request.predecessorEngineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` }; },
      async cancelContextSuccessor() {}
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "old basis" }));
    await writeFile(join(fixture.projectRoot, ".chirality", "workflows", "fixture-method", "WORKFLOW.md"), "---\nname: fixture-method\ndescription: Runtime API fixture method.\n---\n\nCHANGED_INSTRUCTION_BYTES\n", "utf8");
    const blocked = await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "must block drift" }));
    expect(blocked).toContainEqual(expect.objectContaining({ type: "turn:error", data: expect.objectContaining({ details: { runtimeCode: "RUNTIME_COMPATIBILITY_MISMATCH" } }) }));
    expect(inputs).toHaveLength(1);
    const current = await fixture.sessions.get("v3-api", session.sessionId);
    const refreshed = await fixture.client.replaceSelectedMethods("v3-api", session.sessionId, { expectedRevision: current.methodSelectionRevision, expectedBasisId: current.instructionBasisId, boundaryConfirmed: true, methods: current.selectedMethods });
    expect(refreshed.transition).toMatchObject({ status: "prepared", preparationId: "drift-prepared-1" });
    await writeFile(join(fixture.projectRoot, ".chirality", "workflows", "fixture-method", "WORKFLOW.md"), "---\nname: fixture-method\ndescription: Runtime API fixture method.\n---\n\nCHANGED_AFTER_PREPARE\n", "utf8");
    const stalePreparation = await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "stale prepared successor" }));
    expect(stalePreparation).toContainEqual(expect.objectContaining({ type: "turn:error", data: expect.objectContaining({ details: { runtimeCode: "RUNTIME_COMPATIBILITY_MISMATCH" } }) }));
    expect(inputs).toHaveLength(1);
    expect((await fixture.sessions.get("v3-api", session.sessionId)).adapterSession?.contextSuccessor).toBeUndefined();
    const stale = await fixture.sessions.get("v3-api", session.sessionId);
    const repaired = await fixture.client.replaceSelectedMethods("v3-api", session.sessionId, { expectedRevision: stale.methodSelectionRevision, expectedBasisId: stale.instructionBasisId, boundaryConfirmed: true, methods: stale.selectedMethods });
    expect(repaired.transition).toMatchObject({ status: "prepared", preparationId: "drift-prepared-2" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "fresh successor" }));
    expect(inputs).toHaveLength(2);
    expect(inputs[1]?.instructionContext?.documents[0]?.content).toContain("CHANGED_AFTER_PREPARE");
  });

  it("rejects and clears an uncommitted successor projection before provider start", async () => {
    let invoked = false;
    const cancelled: string[] = [];
    const fixture = await setup(async function* () { invoked = true; yield { type: "process:exit", data: { exitCode: 0 } }; }, undefined, { async cancelContextSuccessor(preparationId) { cancelled.push(preparationId); } });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [] });
    await fixture.sessions.update({
      ...session,
      adapterSession: {
        contextSuccessor: {
          preparationId: "crash-window",
          adapterId: "stub",
          providerId: "stub",
          predecessorEngineSessionId: "old-engine",
          continuationText: "[]",
          continuationSha256: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e5c57a18f0c08e8e8f6f0f1",
          targetBasisId: session.instructionBasisId ?? "basis-pending",
          targetReference: `${session.instructionBasisId ?? "basis-pending"}:missing`
        }
      }
    });
    const events = await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "must not start" }));
    expect(events).toContainEqual(expect.objectContaining({ type: "turn:error", data: expect.objectContaining({ details: { runtimeCode: "RUNTIME_COMPATIBILITY_MISMATCH" } }) }));
    expect(invoked).toBe(false);
    expect(cancelled).toEqual(["crash-window"]);
    expect((await fixture.sessions.get("v3-api", session.sessionId)).adapterSession?.contextSuccessor).toBeUndefined();
  });

  it("admits a permission-only basis revision in the same provider span", async () => {
    const inputs: AgentEngineRunInput[] = [];
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      yield { type: "session:init", data: { engineSessionId: "permission-span", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "ask basis" }));
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "read only basis", permissionMode: "readOnly" }));
    expect(inputs).toHaveLength(2);
    expect(inputs.map(input => input.instructionContext?.permissionMode)).toEqual([undefined, undefined]);
    expect(inputs[0]?.instructionContext?.basisPreview.instructionPolicySha256).toBe(inputs[1]?.instructionContext?.basisPreview.instructionPolicySha256);
    expect(inputs[0]?.instructionContext?.basisPreview.id).not.toBe(inputs[1]?.instructionContext?.basisPreview.id);
  });

  it("rejects project instruction symlink escape without supplying outside bytes", async () => {
    let invoked = false;
    const fixture = await setup(async function* () { invoked = true; yield { type: "process:exit", data: { exitCode: 0 } }; });
    const outside = join(fixture.directory, "outside-agents.md");
    await writeFile(outside, "OUTSIDE_SECRET_MUST_NOT_BE_SUPPLIED\n", "utf8");
    await rm(join(fixture.projectRoot, "AGENTS.md"));
    await symlink(outside, join(fixture.projectRoot, "AGENTS.md"));
    await expect(fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [] })).rejects.toMatchObject({ code: "FORBIDDEN" });
    expect(invoked).toBe(false);
  });

  it("defers an exact read-only stop request until terminal and applies it through a successor", async () => {
    let selectedDuringTurn: readonly unknown[] = [];
    const fixture = await setup(async function* (input) {
      const control = input.runtimeTools?.find(tool => tool.name === "chirality_request_method_change");
      expect(control?.permission.operation).toBe("control");
      const requested = await control?.execute({ mode: "replace", methods: [] }, new AbortController().signal) as any;
      expect(requested).toMatchObject({ status: "deferred", mode: "replace", methods: [] });
      selectedDuringTurn = (await fixture.sessions.get("v3-api", input.session.sessionId)).selectedMethods ?? [];
      yield { type: "session:init", data: { engineSessionId: "control-predecessor", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, {
      async prepareContextSuccessor(request) { return { preparationId: "control-successor", adapterId: "stub", providerId: "stub", predecessorEngineSessionId: request.predecessorEngineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` }; },
      async cancelContextSuccessor() {}
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", permissionMode: "readOnly", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "stop after this turn" }));
    expect(selectedDuringTurn).toEqual([expect.objectContaining({ name: "fixture-method" })]);
    expect((await fixture.sessions.get("v3-api", session.sessionId)).selectedMethods).toEqual([]);
    const history = await fixture.sessions.instructionBases.history("v3-api", session.sessionId);
    expect(history.map(record => record.type)).toEqual(expect.arrayContaining(["method-change.requested", "method-change.applied"]));
  });

  it("does not expose control callbacks to an adapter without control support", async () => {
    let toolNames: string[] = [];
    const fixture = await setup(async function* (input) {
      toolNames = input.runtimeTools?.map(tool => tool.name) ?? [];
      yield { type: "session:init", data: { engineSessionId: "no-control", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, undefined, false);
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [] });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "no control" }));
    expect(toolNames).not.toContain("chirality_request_method_change");
  });

  it("preserves TASK identity and sealed scope through a deferred method stop", async () => {
    let selectedDuringTurn: readonly unknown[] = [];
    const fixture = await setup(async function* (input) {
      const control = input.runtimeTools?.find(tool => tool.name === "chirality_request_method_change");
      expect(control?.permission.operation).toBe("control");
      await control?.execute({ mode: "replace", methods: [] }, new AbortController().signal);
      selectedDuringTurn = (await fixture.sessions.get("v3-api", input.session.sessionId)).selectedMethods ?? [];
      yield { type: "session:init", data: { engineSessionId: "task-predecessor", adapterId: "stub", providerId: "stub", model: "fixture" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, {
      async prepareContextSuccessor(request) { return { preparationId: "task-stop-successor", adapterId: "stub", providerId: "stub", predecessorEngineSessionId: request.predecessorEngineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` }; },
      async cancelContextSuccessor() {}
    });
    const created = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "task-method" }], parentSessionId: "parent-session", declaredContext: [], allowedWriteTargets: [] });
    await fixture.sessions.update({ ...created, roleId: "TASK", role: "agent2", agentType: 2, persona: "sealed-task-persona" });
    await drain(await fixture.client.turnSession("v3-api", created.sessionId, { message: "finish TASK method" }));
    expect(selectedDuringTurn).toEqual([expect.objectContaining({ name: "task-method" })]);
    expect(await fixture.sessions.get("v3-api", created.sessionId)).toMatchObject({
      roleId: "TASK", role: "agent2", agentType: 2, persona: "sealed-task-persona", parentSessionId: "parent-session",
      declaredContext: [], allowedWriteTargets: [], selectedMethods: []
    });
    await expect(fixture.service.replaceSelectedMethods("v3-api", created.sessionId, { roleId: "HELPS_HUMANS", methods: [] })).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("merges methods as an ordered union by resolved qualified identity", async () => {
    const fixture = await setup(async function* () { yield { type: "process:exit", data: { exitCode: 0 } }; });
    const descriptor = (await fixture.client.listMethods("v3-api")).methods.find(method => method.name === "fixture-method" && method.source === "project")!;
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    const merged = await fixture.client.replaceSelectedMethods("v3-api", session.sessionId, {
      selectionMode: "merge",
      methods: [
        { kind: "workflow", name: "fixture-method" },
        { sourceRootId: descriptor.sourceRootId, source: descriptor.source, kind: descriptor.kind, name: descriptor.name }
      ]
    });
    expect(merged.methods).toEqual([{ sourceRootId: descriptor.sourceRootId, source: descriptor.source, kind: descriptor.kind, name: descriptor.name }]);
  });

  it("uses the same semantic read capability for provider and Runtime callbacks", async () => {
    const fixture = await setup(async function* () { yield { type: "process:exit", data: { exitCode: 0 } }; });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", roleId: "HELPS_HUMANS" });
    const context = await fixture.service.resolveSelectedContext("v3-api", session.sessionId, {
      roleId: "HELPS_HUMANS", interactionMode: "chat", permissionMode: "ask", methods: [{ kind: "workflow", name: "manager-readonly" }]
    });
    const methodService = (fixture.service as unknown as { methods: { restrictRequestedTools: Function; restrictRuntimeTools: Function } }).methods;
    await expect(methodService.restrictRequestedTools("v3-api", "HELPS_HUMANS", "ask", context.methods, ["read_file"])).resolves.toEqual(["read_file"]);
    await expect(methodService.restrictRuntimeTools("v3-api", "HELPS_HUMANS", "ask", context.methods, [{ name: "read_file", description: "read", inputSchema: { type: "object" }, permission: { effect: "allow", operation: "read", pathScope: "workspace" }, async execute() { return {}; } }])).resolves.toHaveLength(1);
  });

  it("prepares a role successor and records its actual provider span identity", async () => {
    const inputs: AgentEngineRunInput[] = [];
    const preparations: ContextSuccessorRequest[] = [];
    const cancelled: string[] = [];
    const fixture = await setup(async function* (input) {
      inputs.push(input);
      const successor = input.contextSuccessor;
      yield { type: "session:init", data: { engineSessionId: successor ? "engine-successor" : inputs.length === 1 ? "engine-predecessor" : "engine-third", ...(successor ? { providerSpanId: "span-successor" } : {}), adapterId: "stub", providerId: "stub", model: "fixture" } };
      if (inputs.length === 1) yield { type: "chat:delta", data: { text: "prior assistant response" } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    }, undefined, {
      async prepareContextSuccessor(request): Promise<PreparedContextSuccessor> {
        preparations.push(request);
        return { preparationId: "prepared-successor", adapterId: "stub", providerId: "stub", predecessorEngineSessionId: request.predecessorEngineSessionId, continuationText: request.continuationContext.transcript, continuationSha256: request.continuationContext.sha256, targetBasisId: request.toBasisPreview.id, targetReference: `${request.toBasisPreview.id}:${request.toBasisPreview.sha256}` };
      },
      async cancelContextSuccessor(preparationId) { cancelled.push(preparationId); }
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api", selectedMethods: [{ kind: "workflow", name: "fixture-method" }] });
    await fixture.sessions.update({ ...session, sdkSessionId: "legacy-predecessor-sdk-session", sdkTranscriptPath: "/legacy/transcript", sdkSessionStoreKey: "legacy-store-key" });
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "prior user prompt" }));
    const replacement = await fixture.client.replaceSelectedMethods("v3-api", session.sessionId, { expectedRevision: 0, roleId: "HELPS_HUMANS", boundaryConfirmed: true, methods: [] });
    expect(replacement.transition).toEqual({ status: "prepared", successorAvailable: true, preparationId: "prepared-successor" });
    expect(preparations[0]?.continuationContext.transcript).toContain("prior user prompt");
    expect(preparations[0]?.continuationContext.transcript).toContain("prior assistant response");
    expect(preparations[0]?.continuationContext.transcript).not.toContain("Exact fixture instructions");
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "successor prompt" }));
    expect(inputs[1]?.contextSuccessor).toMatchObject({ preparationId: "prepared-successor", predecessorEngineSessionId: "engine-predecessor" });
    expect(cancelled).toEqual([]);
    const replay = await fixture.client.replaySession("v3-api", session.sessionId);
    expect(replay.instructionHistory.map(record => record.type)).toEqual(expect.arrayContaining(["provider-span.prepared", "provider-span.committed", "provider-span.continued"]));
    expect(await fixture.sessions.get("v3-api", session.sessionId)).toMatchObject({ roleId: "HELPS_HUMANS", engineSessionId: "engine-successor" });
    expect((await fixture.sessions.get("v3-api", session.sessionId)).adapterSession?.contextSuccessor).toBeUndefined();
    await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "third prompt" }));
    expect(inputs[2]?.contextSuccessor).toBeUndefined();
    expect(inputs[2]?.session.sdkSessionId).toBeUndefined();
    expect(inputs[2]?.session.sdkTranscriptPath).toBeUndefined();
    expect(inputs[2]?.session.sdkSessionStoreKey).toBeUndefined();
  });

  it("exports only a trusted stored native Plan revision and rejects symlinked parents", async () => {
    const qualification = { adapterId: "stub", providerId: "stub", qualificationId: "fixture-qualified", admissionSha256: "a".repeat(64), evidenceClass: "native-adapter-qualified" as const };
    const sourceEvent = { qualificationState: "qualified" as const, eventId: "native-event", occurredAt: new Date().toISOString(), qualification, plan: { title: "trusted plan" } };
    const markdownEvent = { qualificationState: "qualified" as const, eventId: "native-markdown", occurredAt: new Date().toISOString(), qualification, plan: { id: "plan-item", type: "plan", text: "# Trusted plan\n\n1. Inspect\n2. Revise" } };
    const stringEvent = { qualificationState: "qualified" as const, eventId: "native-string", occurredAt: new Date().toISOString(), qualification, plan: "# Earlier text plan" };
    const fixture = await setup(async function* (input) { yield { type: "session:init", data: { engineSessionId: "engine", adapterId: "stub", providerId: "stub", model: input.opts.model } }; yield { type: "process:exit", data: { exitCode: 0 } }; }, {
      async capability() { return { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification }; },
      async revisions() { return { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification, revisions: [{ revision: 1, sourceEvent }, { revision: 2, sourceEvent: markdownEvent }, { revision: 3, sourceEvent: stringEvent }] }; }
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    await fixture.client.listNativePlanRevisions("v3-api", session.sessionId);
    const exported = await fixture.client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "plans/revision-1.json" });
    expect(exported).toMatchObject({ revision: 1, targetRelativePath: "plans/revision-1.json" });
    expect(JSON.parse(await readFile(join(fixture.projectRoot, "plans", "revision-1.json"), "utf8"))).toEqual({ title: "trusted plan" });
    await fixture.client.exportNativePlan("v3-api", session.sessionId, { revision: 2, targetRelativePath: "plans/revision-2.md" });
    expect(await readFile(join(fixture.projectRoot, "plans", "revision-2.md"), "utf8")).toBe("# Trusted plan\n\n1. Inspect\n2. Revise\n");
    await fixture.client.exportNativePlan("v3-api", session.sessionId, { revision: 3, targetRelativePath: "plans/revision-3.md" });
    expect(await readFile(join(fixture.projectRoot, "plans", "revision-3.md"), "utf8")).toBe("# Earlier text plan\n");
    const outside = join(fixture.directory, "outside"); await mkdir(outside); await symlink(outside, join(fixture.projectRoot, "escape"));
    await expect(fixture.client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "escape/plan.json" })).rejects.toMatchObject({ code: "FORBIDDEN" });
    await expect(readFile(join(outside, "plan.json"))).rejects.toMatchObject({ code: "ENOENT" });
  });

  it("keeps native Plan clarifications distinct from permission decisions and preserves multi-question answers", async () => {
    const qualification = { adapterId: "stub", providerId: "stub", qualificationId: "fixture-qualified", admissionSha256: "a".repeat(64), evidenceClass: "native-adapter-qualified" as const };
    const replies: unknown[] = [];
    const clarification = { clientTurnId: "client-turn", providerThreadId: "provider-thread", providerTurnId: "provider-turn", requestId: 42, itemId: "question-item", questions: [
      { id: "scope", header: "Scope", question: "Which scope?", options: [{ label: "A", description: "First" }], isOther: true, isSecret: false },
      { id: "token", header: "Secret", question: "Supply token", options: [], isOther: false, isSecret: true }
    ], isBlocking: true, autoResolutionMs: null };
    const fixture = await setup(async function* () { yield { type: "process:exit", data: { exitCode: 0 } }; }, {
      async capability() { return { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification }; },
      async revisions() { return { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification, revisions: [] }; },
      async clarifications() { return { schemaVersion: "chirality.native-plan-clarifications/v3", status: "qualified", qualification, clarifications: [clarification] }; },
      async replyClarification(projectId: string, sessionId: string, request: unknown) { replies.push({ projectId, sessionId, request }); return { sent: true }; }
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    expect(await fixture.client.listNativePlanClarifications("v3-api", session.sessionId)).toMatchObject({ status: "qualified", clarifications: [clarification] });
    const request = { requestId: 42, answers: { scope: { answers: ["A", "custom"] }, token: { answers: ["secret"] } } };
    await expect(fixture.client.replyNativePlanClarification("v3-api", session.sessionId, request)).resolves.toEqual({ schemaVersion: "chirality.native-plan-clarification-reply/v3", sessionId: session.sessionId, requestId: 42, sent: true });
    expect(replies).toEqual([{ projectId: "v3-api", sessionId: session.sessionId, request }]);
  });

  it("lists and exports recorded qualified Native Plan revisions after restart without the registry", async () => {
    const qualification = { adapterId: "stub-native", providerId: "stub", qualificationId: "qualification-a", admissionSha256: "a".repeat(64), evidenceClass: "native-adapter-qualified" as const };
    const sourceEvent = { qualificationState: "qualified" as const, eventId: "native-a-1", occurredAt: "2026-09-09T12:00:00.000Z", qualification, plan: { steps: ["persisted-a"] } };
    let providerInvoked = false;
    const fixture = await setup(async function* (input) { providerInvoked = true; yield { type: "session:init", data: { engineSessionId: "native-history", adapterId: "stub", providerId: "stub", model: input.opts.model } }; yield { type: "process:exit", data: { exitCode: 0 } }; }, {
      async capability() { return { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification }; },
      async revisions() { return { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification, revisions: [{ revision: 1, sourceEvent }] }; }
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    expect(await fixture.client.listNativePlanRevisions("v3-api", session.sessionId)).toMatchObject({ status: "qualified", qualification, revisions: [{ revision: 1, sourceEvent }] });
    const history = await fixture.sessions.instructionBases.history("v3-api", session.sessionId);
    expect(history).toContainEqual(expect.objectContaining({ type: "native-plan.revised", revision: { revision: 1, sourceEvent }, provenance: "trusted-native-plan-registry", revisionSha256: expect.any(String), qualificationSha256: expect.any(String) }));
    await fixture.daemon.stop();
    daemons.splice(daemons.indexOf(fixture.daemon), 1);
    (fixture.service as any).methods.nativePlan = undefined;
    const socketPath = join(fixture.directory, "native-restart.sock");
    const restarted = new RuntimeDaemon({ runtimeDirectory: fixture.runtime, socketPath, service: fixture.service });
    daemons.push(restarted); await restarted.start();
    const client = new RuntimeClient({ socketPath, tokenFile: (fixture.client as any).options.tokenFile });
    expect(await client.getNativePlanCapability("v3-api", session.sessionId)).toMatchObject({ status: "unavailable" });
    expect(await client.listNativePlanRevisions("v3-api", session.sessionId)).toMatchObject({ status: "qualified", qualification, revisions: [{ revision: 1, sourceEvent }] });
    const unavailableTurn = await drain(await client.turnSession("v3-api", session.sessionId, { message: "new plan must remain gated", interactionMode: "native-plan" }));
    expect(unavailableTurn).toContainEqual(expect.objectContaining({ type: "turn:error", data: expect.objectContaining({ details: { runtimeCode: "ENGINE_UNAVAILABLE" } }) }));
    expect(providerInvoked).toBe(false);
    const exported = await client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "plans/historical-a.json" });
    expect(exported.revision).toBe(1);
    expect(JSON.parse(await readFile(join(fixture.projectRoot, "plans", "historical-a.json"), "utf8"))).toEqual(sourceEvent.plan);

    const qualificationB = { ...qualification, qualificationId: "qualification-b", admissionSha256: "b".repeat(64) };
    const sourceEventB = { qualificationState: "qualified" as const, eventId: "native-b-2", occurredAt: "2026-09-09T13:00:00.000Z", qualification: qualificationB, plan: { steps: ["persisted-b"] } };
    (fixture.service as any).methods.nativePlan = {
      async capability() { return { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification: qualificationB }; },
      async revisions() { return { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification: qualificationB, revisions: [{ revision: 1, sourceEvent }, { revision: 2, sourceEvent: sourceEventB }] }; }
    };
    expect(await client.getNativePlanCapability("v3-api", session.sessionId)).toMatchObject({ status: "qualified", qualification: qualificationB });
    expect(await client.listNativePlanRevisions("v3-api", session.sessionId)).toMatchObject({ status: "qualified", qualification: qualificationB, revisions: [{ revision: 1, sourceEvent }, { revision: 2, sourceEvent: sourceEventB }] });
    await client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "plans/historical-a-under-b.json" });
    (fixture.service as any).methods.nativePlan = {
      async capability() { throw new Error("transient registry failure"); },
      async revisions() { throw new Error("transient registry failure"); }
    };
    expect(await client.listNativePlanRevisions("v3-api", session.sessionId)).toMatchObject({ status: "qualified", qualification: qualificationB, revisions: [{ revision: 1, sourceEvent }, { revision: 2, sourceEvent: sourceEventB }] });
    await client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "plans/historical-a-during-failure.json" });
  });

  it("rejects untrusted append and tampered persisted Native Plan history", async () => {
    const qualification = { adapterId: "stub-native", providerId: "stub", qualificationId: "qualification-a", admissionSha256: "a".repeat(64), evidenceClass: "native-adapter-qualified" as const };
    const sourceEvent = { qualificationState: "qualified" as const, eventId: "native-tamper-1", occurredAt: "2026-09-09T12:00:00.000Z", qualification, plan: { value: "original" } };
    const fixture = await setup(async function* () { yield { type: "process:exit", data: { exitCode: 0 } }; }, {
      async capability() { return { schemaVersion: "chirality.native-plan-capability/v3", status: "qualified", qualification }; },
      async revisions() { return { schemaVersion: "chirality.native-plan-revisions/v3", status: "qualified", qualification, revisions: [{ revision: 1, sourceEvent }] }; }
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    await expect(fixture.sessions.instructionBases.appendHistory("v3-api", session.sessionId, { type: "native-plan.revised", revision: { revision: 2, sourceEvent: { ...sourceEvent, eventId: "caller-supplied" } }, provenance: "trusted-native-plan-registry", revisionSha256: "0".repeat(64), qualificationSha256: "0".repeat(64) })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await fixture.client.listNativePlanRevisions("v3-api", session.sessionId);
    await expect(fixture.sessions.instructionBases.appendTrustedNativePlanRevision("v3-api", session.sessionId, { revision: 1, sourceEvent: { ...sourceEvent, eventId: "conflicting-revision" } })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    const historyPath = join(fixture.runtime, "projects", "v3-api", "sessions", session.sessionId, "instruction-history.jsonl");
    const lines = (await readFile(historyPath, "utf8")).trimEnd().split("\n");
    const record = JSON.parse(lines.at(-1)!);
    const unqualified = JSON.parse(JSON.stringify(record));
    unqualified.revision.sourceEvent.qualificationState = "unavailable";
    lines[lines.length - 1] = JSON.stringify(unqualified);
    await writeFile(historyPath, `${lines.join("\n")}\n`, "utf8");
    await expect(fixture.client.listNativePlanRevisions("v3-api", session.sessionId)).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    record.revision.sourceEvent.plan = { value: "tampered" };
    lines[lines.length - 1] = JSON.stringify(record);
    await writeFile(historyPath, `${lines.join("\n")}\n`, "utf8");
    await expect(fixture.client.listNativePlanRevisions("v3-api", session.sessionId)).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await expect(fixture.client.exportNativePlan("v3-api", session.sessionId, { revision: 1, targetRelativePath: "plans/tampered.json" })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("passes per-turn model and effort through the client and recovers a disconnected turn by attaching", async () => {
    const captured: AgentEngineRunInput[] = [];
    let release!: () => void;
    const gate = new Promise<void>(resolveGate => { release = resolveGate; });
    const fixture = await setup(async function* (input) {
      captured.push(input);
      yield { type: "session:init", data: { engineSessionId: `engine-${captured.length}`, adapterId: "stub", providerId: "stub", model: input.opts.model } };
      if (captured.length === 2) { yield { type: "chat:delta", data: { text: "before" } }; await gate; yield { type: "chat:delta", data: { text: "missed" } }; }
      yield { type: "harness:event", data: { schemaVersion: 1, eventId: `completed-${captured.length}`, sessionId: input.session.sessionId, turnId: input.turnId, timestamp: new Date().toISOString(), type: "turn.completed", data: {} } };
      yield { type: "process:exit", data: { exitCode: 0 } };
    });
    const session = await fixture.client.createSession("v3-api", { projectId: "v3-api" });
    const first = await drain(await fixture.client.turnSession("v3-api", session.sessionId, { message: "override", model: "fixture-alt", reasoningEffort: "low" }));
    expect(first.map(event => event.seq)).toEqual([1, 2, 3, 4]);
    expect(captured[0]).toMatchObject({ reasoningEffort: "low", opts: { model: "fixture-alt" }, session: { engineSelection: { model: "fixture-alt" } } });
    expect(await fixture.client.getSession("v3-api", session.sessionId)).toMatchObject({ status: "completed", engineSelection: { model: "fixture" }, lastUsedModel: "fixture-alt", lastUsedReasoningEffort: "low" });

    const stream = await fixture.client.turnSession("v3-api", session.sessionId, { message: "disconnect mid-turn" });
    const iterator = stream[Symbol.asyncIterator]();
    expect((await iterator.next()).value).toMatchObject({ seq: 1, type: "harness:event" });
    expect((await iterator.next()).value).toMatchObject({ seq: 2, type: "session:init" });
    stream.cancel();
    let state = await fixture.client.sessionTurnState("v3-api", session.sessionId);
    for (let attempt = 0; attempt < 100 && state.lastSeq < 3; attempt += 1) { await new Promise(resolve => setTimeout(resolve, 10)); state = await fixture.client.sessionTurnState("v3-api", session.sessionId); }
    expect(state).toMatchObject({ active: true, lastSeq: 3 });
    const attached = await fixture.client.attachSessionTurn("v3-api", session.sessionId, { after: 2 });
    release();
    const recovered = await drain(attached);
    expect(recovered.map(event => [event.seq, event.type])).toEqual([[3, "chat:delta"], [4, "chat:delta"], [5, "harness:event"], [6, "process:exit"]]);
    expect(recovered[1]).toMatchObject({ data: { text: "missed" } });
    expect(await fixture.client.sessionTurnState("v3-api", session.sessionId)).toMatchObject({ active: false, lastSeq: 6 });
    expect(await fixture.client.getSession("v3-api", session.sessionId)).toMatchObject({ status: "completed", lastUsedModel: "fixture" });
    expect((await fixture.sessions.replay("v3-api", session.sessionId)).filter(event => event.type === "turn.interrupted")).toHaveLength(0);
  });
});
