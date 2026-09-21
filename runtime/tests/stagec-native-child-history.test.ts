import { createHash } from "node:crypto";
import { mkdtemp, mkdir, realpath, rm, writeFile } from "node:fs/promises";
import { resolve, join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { ProjectRegistry, SessionStore, RuntimeMethodService, EngineRegistry } from "@chirality/runtime-core";

const cleanup: string[] = [];
const sha = (value: string) => createHash("sha256").update(value).digest("hex");
const historyId = (parentSessionId: string, supplierGeneration: string, rootTurnId: string, associationId: string, childThreadId: string, childTurnId: string) =>
  `native-${sha(JSON.stringify({ schema: "chirality-native-child-history/v1", parentSessionId, supplierGeneration, rootThreadId: "root-thread", rootTurnId, associationId, childThreadId, childTurnId }))}`;
afterEach(async () => { await Promise.all(cleanup.splice(0).map(path => rm(path, { recursive: true, force: true }))); });

describe("Stage C child-scoped method activation", () => {
  it("records configured-child activation under the child association without changing parent selection/history", async () => {
    const directory = await realpath(await mkdtemp("/tmp/chirality-c-child-history-")); cleanup.push(directory);
    const projectRoot = join(directory, "project"), runtime = join(directory, "runtime");
    for (const name of ["loader-only", "authored-workflow", "second-workflow"]) await mkdir(join(projectRoot, ".chirality", "workflows", name), { recursive: true });
    await writeFile(join(projectRoot, "AGENTS.md"), "# Child history fixture\n");
    await writeFile(join(projectRoot, ".chirality", "workflows", "loader-only", "WORKFLOW.md"), "---\nname: loader-only\ndescription: Loader\n---\n");
    await writeFile(join(projectRoot, ".chirality", "workflows", "loader-only", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"], tools: { capabilities: ["chirality_load_method"] } })}\n`);
    await writeFile(join(projectRoot, ".chirality", "workflows", "authored-workflow", "WORKFLOW.md"), "---\nname: authored-workflow\ndescription: Child method\n---\n\nCHILD_METHOD_BODY\n");
    await writeFile(join(projectRoot, ".chirality", "workflows", "authored-workflow", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"], tools: { capabilities: ["chirality_load_method", "read"] } })}\n`);
    await writeFile(join(projectRoot, ".chirality", "workflows", "second-workflow", "WORKFLOW.md"), "---\nname: second-workflow\ndescription: Second child method\n---\n\nSECOND_METHOD_BODY\n");
    await writeFile(join(projectRoot, ".chirality", "workflows", "second-workflow", "execution.json"), `${JSON.stringify({ schema_version: 1, compatible_roles: ["HELP_HUMAN"], tools: { capabilities: ["chirality_load_method", "read"] } })}\n`);
    const manifestPath = join(projectRoot, "chirality.project.json");
    await writeFile(manifestPath, `${JSON.stringify({ schemaVersion: "chirality.project/v2", projectId: "child-history", displayName: "Child", workingRoot: ".", instructionRoot: { mode: "runtime" }, defaultExecutionRoot: ".", profiles: { domain: [], capability: [], dataBoundary: [] }, enabledAdapterIds: ["stub"], embeddedUi: { declared: false } })}\n`);
    await mkdir(runtime, { mode: 0o700 });
    const projects = new ProjectRegistry(runtime, { CHIRALITY_INSTRUCTION_ROOT: resolve(process.cwd(), "../..") });
    await projects.register(manifestPath, "controlled-test", "child-history");
    const sessions = new SessionStore(runtime, projects), methods = new RuntimeMethodService(projects, sessions, new EngineRegistry());
    const parent = await sessions.create({ projectId: "child-history", role: "agent0", engineSelection: { adapterId: "stub", providerId: "stub", model: "fixture" } });
    await sessions.update({ ...parent, schemaVersion: "chirality.session/v3", roleId: "HELP_HUMAN", persona: "HELP_HUMAN", interactionMode: "chat", permissionMode: "workspaceWrite", selectedMethods: [{ sourceRootId: "project-workflows", source: "project", kind: "workflow", name: "loader-only" }], methodSelectionRevision: 1 });
    const load = methods.runtimeTools("child-history", parent.sessionId, "parent-turn", ["read"]).find(tool => tool.name === "chirality_load_method")!;
    const child = { associationId: "a".repeat(32), supplierGeneration: "supplier-generation-one", rootThreadId: "root-thread", rootTurnId: "parent-turn", parentThreadId: "root-thread", parentTurnId: "parent-turn", selectedRole: { kind: "configured" as const, name: "HELP_HUMAN", basisDigest: "b".repeat(64) }, inheritedToolsDigest: "c".repeat(64) };
    const result = await load.execute({ methods: [{ kind: "workflow", name: "authored-workflow" }] }, new AbortController().signal, {
      threadId: "child-thread", turnId: "child-turn", callId: "child-call", nativeChild: child
    }) as any;
    expect(result).toMatchObject({ schemaVersion: "chirality.method-load/v3", turnId: "child-turn", documents: [{ content: expect.stringContaining("CHILD_METHOD_BODY") }] });
    expect((await sessions.get("child-history", parent.sessionId)).selectedMethods).toEqual([{ sourceRootId: "project-workflows", source: "project", kind: "workflow", name: "loader-only" }]);
    expect((await sessions.instructionBases.history("child-history", parent.sessionId)).some(record => record.type === "native-child.method-loaded")).toBe(false);
    const firstHistoryId = historyId(parent.sessionId, child.supplierGeneration, child.rootTurnId, child.associationId, "child-thread", "child-turn");
    expect(await sessions.instructionBases.history("child-history", firstHistoryId)).toEqual([
      expect.objectContaining({ type: "native-child.method-loaded", supplierGeneration: child.supplierGeneration, rootThreadId: "root-thread", rootTurnId: "parent-turn", parentSessionId: parent.sessionId, parentTurnId: "parent-turn", childThreadId: "child-thread", childTurnId: "child-turn", roleId: "HELP_HUMAN", selectedMethods: [expect.objectContaining({ name: "authored-workflow" })], childInstructionBasisId: expect.any(String), loadedEntries: [expect.objectContaining({ turnId: "child-turn", content: expect.stringContaining("CHILD_METHOD_BODY") })] })
    ]);
    await load.execute({ methods: [{ kind: "workflow", name: "second-workflow" }] }, new AbortController().signal, { threadId: "child-thread", turnId: "child-turn", callId: "child-call-2", nativeChild: child });
    const cumulative = await sessions.instructionBases.history("child-history", firstHistoryId);
    expect(cumulative).toHaveLength(2);
    expect(cumulative[1]).toMatchObject({ type: "native-child.method-loaded", selectedMethods: [expect.objectContaining({ name: "authored-workflow" }), expect.objectContaining({ name: "second-workflow" })], loadedEntries: [expect.objectContaining({ content: expect.stringContaining("SECOND_METHOD_BODY") })] });

    const isolated = { ...child, associationId: "e".repeat(32), childThreadId: undefined, supplierGeneration: "supplier-generation-two", rootTurnId: "fresh-root-turn", parentTurnId: "fresh-root-turn" };
    await load.execute({ methods: [{ kind: "workflow", name: "second-workflow" }] }, new AbortController().signal, { threadId: "other-child", turnId: "other-turn", callId: "other-call", nativeChild: isolated });
    const isolatedHistoryId = historyId(parent.sessionId, isolated.supplierGeneration, isolated.rootTurnId, isolated.associationId, "other-child", "other-turn");
    expect((await sessions.instructionBases.history("child-history", isolatedHistoryId))[0]).toMatchObject({ selectedMethods: [expect.objectContaining({ name: "second-workflow" })] });
    expect(isolatedHistoryId).not.toBe(firstHistoryId);

    const reusedAssociation = { ...child, supplierGeneration: "supplier-generation-three", rootTurnId: "repeated-root", parentTurnId: "repeated-root" };
    await load.execute({ methods: [{ kind: "workflow", name: "second-workflow" }] }, new AbortController().signal, { threadId: "child-thread", turnId: "child-turn", callId: "reused-call", nativeChild: reusedAssociation });
    const reusedHistoryId = historyId(parent.sessionId, reusedAssociation.supplierGeneration, reusedAssociation.rootTurnId, reusedAssociation.associationId, "child-thread", "child-turn");
    expect(reusedHistoryId).not.toBe(firstHistoryId);
    expect((await sessions.instructionBases.history("child-history", reusedHistoryId))[0]).toMatchObject({ selectedMethods: [expect.objectContaining({ name: "second-workflow" })] });
    await expect(load.execute({ methods: [{ kind: "workflow", name: "authored-workflow" }] }, new AbortController().signal, {
      threadId: "upstream-thread", turnId: "upstream-turn", callId: "upstream-call", nativeChild: { associationId: "d".repeat(32), supplierGeneration: "supplier-generation-one", rootThreadId: "root-thread", rootTurnId: "parent-turn", parentThreadId: "root-thread", parentTurnId: "parent-turn", selectedRole: { kind: "upstream" }, inheritedToolsDigest: "c".repeat(64) }
    })).rejects.toThrow("exact configured Runtime role");
    expect(await sessions.instructionBases.history("child-history", historyId(parent.sessionId, "supplier-generation-one", "parent-turn", "d".repeat(32), "upstream-thread", "upstream-turn"))).toEqual([]);
  });
});
