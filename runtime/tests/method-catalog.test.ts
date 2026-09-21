import { mkdtemp, mkdir, readFile, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { describe, expect, it } from "vitest";
import {
  RUNTIME_ROUTES,
  nativePlanRevisionFromAdapterEvent,
  type NativePlanAdapterEvent
} from "@chirality/runtime-contracts";
import {
  discoverMethodCatalog,
  formatQualifiedMethodId,
  inspectMethod,
  loadRoles,
  normalizeMethodSelection,
  parseQualifiedMethodId,
  resolveMethodReferences,
  type MethodSourceRoot
} from "@chirality/runtime-core";

async function put(path: string, content: string): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, content, "utf8");
}

function frontmatter(name: string, description = `${name} description`): string {
  return `---\nname: ${name}\ndescription: ${description}\n---\n\n# ${name}\n`;
}

async function root(source: MethodSourceRoot["source"], sourceRootId: string): Promise<MethodSourceRoot> {
  return { source, sourceRootId, rootPath: await mkdtemp(join(tmpdir(), `chirality-${source}-`)), version: "fixture-v1" };
}

describe("v3 role and method catalog", () => {
  it("loads exactly the four production roles from the contained checked-in registry", async () => {
    const response = await loadRoles(resolve(process.cwd(), "../.."));
    expect(response.defaultRole).toBe("HELP_HUMAN");
    expect(response.roles.map(role => [role.id, role.agentType, role.directEntry, role.defaultForNewChat])).toEqual([
      ["HELP_HUMAN", 0, true, true],
      ["HELPS_HUMANS", 1, true, false],
      ["WORKING_ITEMS", 1, true, false],
      ["TASK", 2, false, false]
    ]);
  });

  it("discovers standard metadata, maps current compatibility, and excludes the project-only bundled change skill", async () => {
    const bundled = await root("bundled", "chirality-root");
    await put(join(bundled.rootPath, "workflows", "alpha", "WORKFLOW.md"), frontmatter("alpha", "Alpha workflow"));
    await put(join(bundled.rootPath, "workflows", "alpha", "execution.json"), JSON.stringify({ schema_version: 1, compatible_roles: ["WORKING_ITEMS"] }));
    await put(join(bundled.rootPath, ".agents", "skills", "review", "SKILL.md"), frontmatter("review", "Review skill"));
    await put(join(bundled.rootPath, ".agents", "skills", "chirality-change", "SKILL.md"), frontmatter("chirality-change"));
    await put(join(bundled.rootPath, "workflows", "index.json"), JSON.stringify({
      schema: "chirality-method-index/v1",
      library: { source: "bundled", sourceRootId: "chirality-root" },
      precedence: ["project", "user", "bundled"],
      centralWorkflowNames: ["alpha"],
      methods: [{ kind: "workflow", name: "alpha", source: "bundled", sourceRootId: "chirality-root", description: "Alpha workflow", central: true, compatibility: "current", executionRoleIds: ["WORKING_ITEMS"], resources: ["WORKFLOW.md"] }]
    }));
    const catalog = await discoverMethodCatalog([bundled]);
    expect(catalog.response.malformedPackages).toEqual([]);
    expect(catalog.response.methods.map(method => method.name)).toEqual(["review", "alpha"]);
    expect(catalog.response.methods.find(method => method.name === "alpha")).toMatchObject({
      qualifiedId: "chirality-root:bundled:workflow:alpha",
      central: true,
      compatibility: "canonical",
      executionRoleIds: ["WORKING_ITEMS"]
    });
  });

  it("carries catalog navigation from the bundled index onto workflow descriptors only", async () => {
    const bundled = await root("bundled", "chirality-root");
    const project = await root("project", "project-library");
    for (const name of ["core-flow", "step-flow", "old-flow"]) {
      await put(join(bundled.rootPath, "workflows", name, "WORKFLOW.md"), frontmatter(name, `${name} workflow`));
    }
    await put(join(bundled.rootPath, ".agents", "skills", "helper", "SKILL.md"), frontmatter("helper", "Helper skill"));
    await put(join(project.rootPath, "workflows", "core-flow", "WORKFLOW.md"), frontmatter("core-flow", "Project core-flow"));
    const entry = (name: string, extra: Record<string, unknown>) => ({
      kind: "workflow", name, source: "bundled", sourceRootId: "chirality-root", description: `${name} workflow`,
      central: false, compatibility: "canonical", executionRoleIds: ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"], resources: ["WORKFLOW.md"], ...extra
    });
    const index = {
      schema: "chirality-method-index/v1",
      library: { source: "bundled", sourceRootId: "chirality-root" },
      precedence: ["project", "user", "bundled"],
      centralWorkflowNames: ["core-flow"],
      methods: [
        entry("core-flow", { central: true, navigation: { category: "core", tier: "primary", order: 6, displayName: "Manage flow" } }),
        entry("step-flow", { navigation: { category: "specialist", tier: "supporting", order: 2, group: { key: "plan-organize", label: "Plan & organize", order: 3 } } }),
        entry("old-flow", { compatibility: "legacy", navigation: { category: "superseded", tier: "primary", order: 0, supersededBy: "step-flow" } }),
        { kind: "skill", name: "helper", source: "bundled", sourceRootId: "chirality-root", description: "Helper skill", central: false, compatibility: "canonical", executionRoleIds: ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"], resources: ["SKILL.md"] }
      ]
    };
    await put(join(bundled.rootPath, "workflows", "index.json"), JSON.stringify(index));
    const catalog = await discoverMethodCatalog([bundled, project]);
    expect(catalog.response.malformedPackages).toEqual([]);
    const byId = new Map(catalog.response.methods.map(method => [method.qualifiedId, method]));
    expect(byId.get("chirality-root:bundled:workflow:core-flow")).toMatchObject({
      central: true, compatibility: "canonical", navigation: { category: "core", tier: "primary", order: 6, displayName: "Manage flow" }
    });
    expect(byId.get("chirality-root:bundled:workflow:step-flow")?.navigation).toEqual({
      category: "specialist", tier: "supporting", order: 2, group: { key: "plan-organize", label: "Plan & organize", order: 3 }
    });
    expect(byId.get("chirality-root:bundled:workflow:old-flow")).toMatchObject({
      compatibility: "legacy", navigation: { category: "superseded", tier: "primary", order: 0, supersededBy: "step-flow" }
    });
    expect(byId.get("chirality-root:bundled:skill:helper")).not.toHaveProperty("navigation");
    expect(byId.get("project-library:project:workflow:core-flow")).toMatchObject({ central: false, compatibility: "canonical" });
    expect(byId.get("project-library:project:workflow:core-flow")).not.toHaveProperty("navigation");
  });

  it("rejects malformed navigation index entries as an invalid bundled index", async () => {
    const invalidNavigations: readonly Record<string, unknown>[] = [
      { category: "featured", tier: "primary", order: 0 },
      { category: "core", tier: "optional", order: 0 },
      { category: "core", tier: "primary", order: 1.5 },
      { category: "core", tier: "primary", order: "0" },
      { category: "core", tier: "primary", order: 0, displayName: 7 },
      { category: "specialist", tier: "primary", order: 0 },
      { category: "specialist", tier: "primary", order: 0, group: { key: "plan-organize", label: 3, order: 0 } },
      { category: "specialist", tier: "primary", order: 0, group: { key: "Plan Organize", label: "Plan", order: 0 } },
      { category: "specialist", tier: "primary", order: 0, group: { key: "plan-organize", label: "Plan" } },
      { category: "specialist", tier: "primary", order: 0, group: { key: "plan-organize", label: "Plan", order: "0" } },
      { category: "specialist", tier: "primary", order: 0, group: { key: "plan-organize", label: "Plan", order: -1 } },
      { category: "core", tier: "primary", order: 0, group: { key: "plan-organize", label: "Plan", order: 0 } },
      { category: "core", tier: "primary", order: 0, supersededBy: "other-flow" },
      { category: "specialist", tier: "primary", order: 0, group: { key: "plan", label: "Plan", order: 0 }, supersededBy: "other-flow" },
      { category: "superseded", tier: "primary", order: 0 },
      { category: "core", tier: "primary", order: 0, extra: true }
    ];
    for (const navigation of invalidNavigations) {
      const bundled = await root("bundled", "chirality-root");
      await put(join(bundled.rootPath, "workflows", "flow", "WORKFLOW.md"), frontmatter("flow", "Flow workflow"));
      const compatibility = navigation.category === "superseded" ? "legacy" : "canonical";
      await put(join(bundled.rootPath, "workflows", "index.json"), JSON.stringify({
        schema: "chirality-method-index/v1", library: { source: "bundled", sourceRootId: "chirality-root" }, precedence: ["project", "user", "bundled"], centralWorkflowNames: [],
        methods: [{ kind: "workflow", name: "flow", source: "bundled", sourceRootId: "chirality-root", description: "Flow workflow", central: false, compatibility, executionRoleIds: ["TASK"], resources: ["WORKFLOW.md"], navigation }]
      }));
      const catalog = await discoverMethodCatalog([bundled]);
      expect(catalog.response.methods, JSON.stringify(navigation)).toEqual([]);
      expect(catalog.response.malformedPackages.map(issue => issue.code), JSON.stringify(navigation)).toEqual(["malformed-execution-metadata"]);
      expect(catalog.response.malformedPackages[0]?.message, JSON.stringify(navigation)).toMatch(/navigation/);
    }
    const mismatched = await root("bundled", "chirality-root");
    await put(join(mismatched.rootPath, "workflows", "flow", "WORKFLOW.md"), frontmatter("flow", "Flow workflow"));
    await put(join(mismatched.rootPath, "workflows", "index.json"), JSON.stringify({
      schema: "chirality-method-index/v1", library: { source: "bundled", sourceRootId: "chirality-root" }, precedence: ["project", "user", "bundled"], centralWorkflowNames: [],
      methods: [{ kind: "workflow", name: "flow", source: "bundled", sourceRootId: "chirality-root", description: "Flow workflow", central: false, compatibility: "legacy", executionRoleIds: ["TASK"], resources: ["WORKFLOW.md"], navigation: { category: "core", tier: "primary", order: 0 } }]
    }));
    const catalog = await discoverMethodCatalog([mismatched]);
    expect(catalog.response.malformedPackages.map(issue => [issue.code, issue.message])).toEqual([["malformed-execution-metadata", "method index navigation category disagrees with compatibility"]]);
  });

  it("accepts canonical YAML metadata maps and multiline descriptions while reporting duplicate and malformed YAML", async () => {
    const project = await root("bundled", "bundled-library");
    await put(join(project.rootPath, ".agents", "skills", "rich", "SKILL.md"), `---\nname: rich\ndescription: >-\n  A multiline\n  description.\nmetadata:\n  owner: project\n  tags: [one, two]\n---\n# rich\n`);
    await put(join(project.rootPath, ".agents", "skills", "duplicate", "SKILL.md"), `---\nname: duplicate\nname: duplicate\ndescription: invalid\n---\n`);
    await put(join(project.rootPath, ".agents", "skills", "broken", "SKILL.md"), `---\nname: [broken\ndescription: invalid\n---\n`);
    await put(join(project.rootPath, ".agents", "skills", "denied", "SKILL.md"), frontmatter("denied"));
    await put(join(project.rootPath, ".agents", "skills", "denied", "execution.json"), JSON.stringify({ schema_version: 1, compatible_roles: [] }));
    await put(join(project.rootPath, ".agents", "skills", "bad-execution", "SKILL.md"), frontmatter("bad-execution"));
    await put(join(project.rootPath, ".agents", "skills", "bad-execution", "execution.json"), JSON.stringify({ schema_version: 1, compatible_roles: ["INVENTED"] }));
    await put(join(project.rootPath, ".agents", "skills", "embedded-delimiter", "SKILL.md"), frontmatter("embedded-delimiter", "before---after"));
    const valid64 = `a${"b".repeat(63)}`;
    await put(join(project.rootPath, ".agents", "skills", valid64, "SKILL.md"), frontmatter(valid64));
    await put(join(project.rootPath, ".agents", "skills", `a${"b".repeat(64)}`, "SKILL.md"), frontmatter(`a${"b".repeat(64)}`));
    await put(join(project.rootPath, ".agents", "skills", "a--b", "SKILL.md"), frontmatter("a--b"));
    const catalog = await discoverMethodCatalog([project]);
    expect(catalog.response.methods).toEqual(expect.arrayContaining([
      expect.objectContaining({ name: "denied", executionRoleIds: [], execution: expect.objectContaining({ compatibleRoles: [] }) }),
      expect.objectContaining({ name: "embedded-delimiter", description: "before---after" }),
      expect.objectContaining({ name: "rich", description: "A multiline description.", metadata: { owner: "project", tags: ["one", "two"] }, executionRoleIds: ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"] }),
      expect.objectContaining({ name: valid64 })
    ]));
    expect(catalog.response.methods.map(method => method.name)).not.toContain("a--b");
    expect(catalog.response.methods.map(method => method.name)).not.toContain(`a${"b".repeat(64)}`);
    expect(catalog.response.malformedPackages.map(issue => [issue.packageName, issue.code])).toEqual([
      ["bad-execution", "malformed-execution-metadata"],
      ["broken", "malformed-frontmatter"],
      ["duplicate", "malformed-frontmatter"]
    ]);
  });

  it("resolves ordered refs by project then user then bundled and blocks malformed higher-precedence shadowing", async () => {
    const project = await root("project", "project-library");
    const user = await root("user", "user-library");
    const bundled = await root("bundled", "chirality-root");
    await put(join(project.rootPath, "workflows", "same", "WORKFLOW.md"), frontmatter("wrong"));
    await put(join(user.rootPath, "workflows", "same", "WORKFLOW.md"), frontmatter("same", "User same"));
    await put(join(bundled.rootPath, "workflows", "same", "WORKFLOW.md"), frontmatter("same", "Bundled same"));
    await put(join(bundled.rootPath, "workflows", "other", "WORKFLOW.md"), frontmatter("other"));
    const catalog = await discoverMethodCatalog([bundled, user, project]);
    const blocked = resolveMethodReferences(catalog, [{ kind: "workflow", name: "same" }]);
    expect(blocked[0]).toMatchObject({ status: "malformed", issues: [{ source: "project", packageName: "same" }] });

    const ordered = resolveMethodReferences(catalog, [
      { kind: "workflow", name: "other" },
      { sourceRootId: "user-library", source: "user", kind: "workflow", name: "same" }
    ]);
    expect(ordered.map(result => result.status)).toEqual(["resolved", "resolved"]);
    expect(ordered.map(result => result.status === "resolved" ? result.method.descriptor.name : "")).toEqual(["other", "same"]);
  });

  it("exposes collisions and preserves stable qualified identity round trips", async () => {
    const first = await root("project", "project-a");
    const second = await root("project", "project-b");
    await put(join(first.rootPath, "workflows", "same", "WORKFLOW.md"), frontmatter("same"));
    await put(join(second.rootPath, "workflows", "same", "WORKFLOW.md"), frontmatter("same"));
    const catalog = await discoverMethodCatalog([second, first]);
    const result = resolveMethodReferences(catalog, [{ kind: "workflow", name: "same" }])[0];
    expect(result).toMatchObject({ status: "ambiguous" });
    if (result?.status !== "ambiguous") throw new Error("expected collision");
    expect(result.candidates.map(formatQualifiedMethodId)).toEqual([
      "project-a:project:workflow:same",
      "project-b:project:workflow:same"
    ]);
    expect(parseQualifiedMethodId(formatQualifiedMethodId(result.candidates[0]!))).toEqual({
      sourceRootId: "project-a", source: "project", kind: "workflow", name: "same"
    });
  });

  it("matches the shared SEM-5 legacy normalization cases", async () => {
    const bundled = await root("bundled", "fixture-bundle");
    await put(join(bundled.rootPath, ".agents", "skills", "converted-skill", "SKILL.md"), frontmatter("converted-skill"));
    await put(join(bundled.rootPath, "workflows", "example", "WORKFLOW.md"), frontmatter("example"));
    await put(join(bundled.rootPath, "workflows", "legacy-methods.json"), JSON.stringify({
      schema: "chirality-legacy-methods/v1",
      convertedWorkflowAliases: { "converted-skill": { kind: "skill", name: "converted-skill" } },
      legacyWorkflowNames: [], historicalOnly: [], unknownLegacyBehavior: "error"
    }));
    const catalog = await discoverMethodCatalog([bundled]);
    const fixture = JSON.parse(await readFile(resolve(process.cwd(), "../../tools/workflow_runtime/fixtures/legacy_method_normalization_cases.json"), "utf8")) as {
      schema: string;
      cases: readonly { id: string; input: Parameters<typeof normalizeMethodSelection>[1]; outcome?: { methods: unknown; compatibilityInputs: unknown; decisions: unknown }; error?: { code: string; messagePattern: string } }[];
    };
    expect(fixture.schema).toBe("chirality-sem5-legacy-normalization-cases/v1");
    for (const fixtureCase of fixture.cases) {
      if (fixtureCase.error) {
        try {
          normalizeMethodSelection(catalog, fixtureCase.input);
          throw new Error(`expected ${fixtureCase.id} to fail`);
        } catch (error) {
          expect(error).toMatchObject({ code: fixtureCase.error.code });
          expect((error as Error).message).toMatch(new RegExp(fixtureCase.error.messagePattern));
        }
      } else {
        const normalized = normalizeMethodSelection(catalog, fixtureCase.input);
        expect(normalized).toEqual({
          methods: fixtureCase.outcome?.methods,
          compatibilityInputs: fixtureCase.outcome?.compatibilityInputs,
          compatibilityMappings: fixtureCase.outcome?.decisions
        });
      }
    }
  });

  it("loads only bundled skills while explicit non-bundled historical identities remain forbidden", async () => {
    const project = await root("project", "project-library");
    const bundled = await root("bundled", "chirality-root");
    await put(join(project.rootPath, ".agents", "skills", "converted-skill", "SKILL.md"), frontmatter("converted-skill"));
    await put(join(bundled.rootPath, ".agents", "skills", "converted-skill", "SKILL.md"), frontmatter("converted-skill"));
    await put(join(bundled.rootPath, "workflows", "legacy-methods.json"), JSON.stringify({
      schema: "chirality-legacy-methods/v1",
      convertedWorkflowAliases: { "converted-skill": { kind: "skill", name: "converted-skill" } },
      legacyWorkflowNames: [], historicalOnly: [], unknownLegacyBehavior: "error"
    }));
    const catalog = await discoverMethodCatalog([project, bundled]);
    expect(catalog.response.methods).not.toContainEqual(expect.objectContaining({ source: "project", kind: "skill", name: "converted-skill" }));
    const bundledReference = { sourceRootId: "chirality-root", source: "bundled" as const, kind: "skill" as const, name: "converted-skill" };
    const inputMethods = [bundledReference, bundledReference];
    expect(normalizeMethodSelection(catalog, { methods: inputMethods, taskSkill: "converted-skill" }).methods).toEqual(inputMethods);
    expect(inputMethods).toEqual([bundledReference, bundledReference]);

    const projectReference = { sourceRootId: "project-library", source: "project" as const, kind: "skill" as const, name: "converted-skill" };
    expect(resolveMethodReferences(catalog, [projectReference, { kind: "skill", name: "converted-skill" }]).map(value => value.status))
      .toEqual(["forbidden", "resolved"]);
    expect(() => normalizeMethodSelection(catalog, { methods: [projectReference] }))
      .toThrow(expect.objectContaining({ code: "UNSUPPORTED_METHOD_ORIGIN" }));
  });

  it("keeps project and user workflows discoverable and source-qualified while excluding their skills", async () => {
    const project = await root("project", "project-library");
    const user = await root("user", "user-library");
    const bundled = await root("bundled", "trusted-bundle");
    for (const source of [project, user, bundled]) {
      await put(join(source.rootPath, ".agents", "skills", `${source.source}-skill`, "SKILL.md"), frontmatter(`${source.source}-skill`));
      await put(join(source.rootPath, "workflows", `${source.source}-workflow`, "WORKFLOW.md"), frontmatter(`${source.source}-workflow`));
    }
    const catalog = await discoverMethodCatalog([bundled, user, project]);
    expect(catalog.response.methods.filter(value => value.kind === "skill").map(value => value.qualifiedId))
      .toEqual(["trusted-bundle:bundled:skill:bundled-skill"]);
    expect(catalog.response.methods.filter(value => value.kind === "workflow").map(value => value.qualifiedId))
      .toEqual([
        "project-library:project:workflow:project-workflow",
        "user-library:user:workflow:user-workflow",
        "trusted-bundle:bundled:workflow:bundled-workflow"
      ]);
  });

  it("rejects resource symlinks that escape a method package", async () => {
    const project = await root("bundled", "bundled-library");
    const packageRoot = join(project.rootPath, "workflows", "contained");
    await put(join(packageRoot, "WORKFLOW.md"), frontmatter("contained"));
    const outside = join(project.rootPath, "outside.txt");
    await put(outside, "outside");
    await mkdir(join(packageRoot, "resources"));
    await symlink(outside, join(packageRoot, "resources", "escape.txt"));
    const catalog = await discoverMethodCatalog([project]);
    await expect(inspectMethod(catalog.entries[0]!)).rejects.toMatchObject({ code: "RESOURCE_ESCAPE" });
  });

  it("rejects escaped skill packages and resource directory cycles", async () => {
    const project = await root("bundled", "bundled-library");
    const outsidePackage = join(project.rootPath, "outside-skill");
    await put(join(outsidePackage, "SKILL.md"), frontmatter("escaped"));
    await mkdir(join(project.rootPath, ".agents", "skills"), { recursive: true });
    await symlink(outsidePackage, join(project.rootPath, ".agents", "skills", "escaped"));
    const cyclePackage = join(project.rootPath, "workflows", "cycle");
    await put(join(cyclePackage, "WORKFLOW.md"), frontmatter("cycle"));
    await mkdir(join(cyclePackage, "resources"));
    await symlink(join(cyclePackage, "resources"), join(cyclePackage, "resources", "loop"));
    const catalog = await discoverMethodCatalog([project]);
    expect(catalog.response.malformedPackages).toContainEqual(expect.objectContaining({ code: "entrypoint-escape", kind: "skill", packageName: "escaped" }));
    const cycle = catalog.entries.find(entry => entry.descriptor.name === "cycle")!;
    await expect(inspectMethod(cycle)).rejects.toMatchObject({ code: "RESOURCE_ESCAPE" });
  });

  it("rejects a skill collection whose canonical directory escapes its source root", async () => {
    const project = await root("bundled", "bundled-library");
    const outsideCollection = await mkdtemp(join(tmpdir(), "chirality-outside-skills-"));
    await put(join(outsideCollection, "outside", "SKILL.md"), frontmatter("outside"));
    await mkdir(join(project.rootPath, ".agents"), { recursive: true });
    await symlink(outsideCollection, join(project.rootPath, ".agents", "skills"));
    const catalog = await discoverMethodCatalog([project]);
    expect(catalog.response.methods).toEqual([]);
    expect(catalog.response.malformedPackages).toContainEqual(expect.objectContaining({ code: "invalid-source-root", kind: "skill" }));
  });

  it("keeps v3 routes encoded and refuses revisions from unavailable Native Plan events", () => {
    const qualified = "root:bundled:workflow:alpha";
    expect(RUNTIME_ROUTES.method("p / 1", qualified)).toBe("/v1/projects/p%20%2F%201/methods/root%3Abundled%3Aworkflow%3Aalpha");
    expect(RUNTIME_ROUTES.sessionContextResolve("p", "s")).toBe("/v1/projects/p/sessions/s/context/resolve");
    const admitted: NativePlanAdapterEvent = { qualificationState: "trial", eventId: "event-0", occurredAt: "2026-09-10T00:00:00.000Z",
      admission: { evidenceClass: "native-adapter-local-human-trial", adapterId: "codex-app-server", providerId: "openai", dispositionId: "trial-1", admissionSha256: "a".repeat(64) } };
    expect(nativePlanRevisionFromAdapterEvent(1, admitted)).toEqual({ revision: 1, sourceEvent: admitted });
    const unavailable: NativePlanAdapterEvent = { qualificationState: "unavailable", eventId: "event-1", reason: "adapter unavailable" };
    expect(() => nativePlanRevisionFromAdapterEvent(1, unavailable)).toThrow(Error);
  });
});
