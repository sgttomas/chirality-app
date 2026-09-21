import { mkdir, readFile, realpath, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { mkdtemp } from "node:fs/promises";
import { describe, expect, it } from "vitest";
import { codexNativeRoleConfigOverrides, loadRolesFromCapturedRegistry, loadTrustedNativeRoleConfiguration } from "@chirality/runtime-core";

describe("trusted native role configuration", () => {
  it("isolates exact hashed role bodies and pins the reviewed V1 native delegation surface", async () => {
    const root = resolve(process.cwd(), "../..");
    const result = await loadTrustedNativeRoleConfiguration(root, "HELP_HUMAN");
    expect(result.schemaVersion).toBe("chirality.codex-native-roles/v1");
    expect(result.pins).toEqual({ agentsEnabled: true, multiAgentV1: true, multiAgentV2: false, maxDepth: 2 });
    expect(result.activeRole?.roleId).toBe("HELP_HUMAN");
    expect(result.activeRole?.instruction).toContain("# HELP_HUMAN");
    expect(result.nativeRoles.map(role => role.roleId)).toEqual(["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]);
    const working = result.nativeRoles.find(role => role.roleId === "WORKING_ITEMS")!;
    expect(working.configToml).toContain(JSON.stringify(working.instruction));
    expect(working.configToml).not.toContain(result.activeRole!.instruction);

    const paths = Object.fromEntries(result.nativeRoles.map(role => [role.roleId, `/private/runtime/native-roles/${role.configFileName}`])) as Record<typeof result.nativeRoles[number]["roleId"], string>;
    const overrides = codexNativeRoleConfigOverrides(result, paths);
    expect(overrides.slice(0, 4)).toEqual(["agents.enabled=true", "features.multi_agent=true", "features.multi_agent_v2=false", "agents.max_depth=2"]);
    expect(overrides).toContain(`agents.WORKING_ITEMS.config_file=${JSON.stringify(paths.WORKING_ITEMS)}`);
    expect(overrides.some(value => value.startsWith("model") || value.includes("fanout") || value.includes("concurrency"))).toBe(false);
    const roleSetOnly = await loadTrustedNativeRoleConfiguration(root);
    const anotherParent = await loadTrustedNativeRoleConfiguration(root, "TASK");
    expect(roleSetOnly.activeRole).toBeUndefined();
    expect(anotherParent.activeRole?.roleId).toBe("TASK");
    expect(roleSetOnly.digest).toBe(result.digest);
    expect(anotherParent.digest).toBe(result.digest);
  });

  it("rejects substituted role files and incomplete materialization maps", async () => {
    const source = resolve(process.cwd(), "../..");
    const root = await mkdtemp(join(tmpdir(), "chirality-native-roles-"));
    await mkdir(join(root, "agents"), { recursive: true });
    const registry = await import("node:fs/promises").then(fs => fs.readFile(join(source, "agents", "registry.json"), "utf8"));
    await writeFile(join(root, "agents", "registry.json"), registry, "utf8");
    for (const name of ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]) await writeFile(join(root, "agents", `AGENT_${name}.md`), `# ${name}\n`, "utf8");
    const outside = join(root, "outside.md");
    await writeFile(outside, "# HELP_HUMAN substituted\n", "utf8");
    await import("node:fs/promises").then(fs => fs.rm(join(root, "agents", "AGENT_HELP_HUMAN.md")));
    await symlink(outside, join(root, "agents", "AGENT_HELP_HUMAN.md"));
    await expect(loadTrustedNativeRoleConfiguration(await realpath(root), "HELP_HUMAN")).rejects.toThrow(/direct contained regular file/);

    const valid = await loadTrustedNativeRoleConfiguration(source, "TASK");
    expect(() => codexNativeRoleConfigOverrides(valid, { HELP_HUMAN: "/a", HELPS_HUMANS: "/b", WORKING_ITEMS: "/c" } as never)).toThrow(/exactly four/);
    const tampered = { ...valid, nativeRoles: valid.nativeRoles.map(role => role.roleId === "TASK" ? { ...role, instruction: `${role.instruction}\nsubstitute` } : role) };
    expect(() => codexNativeRoleConfigOverrides(tampered, { HELP_HUMAN: "/a", HELPS_HUMANS: "/b", WORKING_ITEMS: "/c", TASK: "/d" })).toThrow(/Invalid trusted native role configuration/);
  });

  it("resolves role paths from the captured registry bytes rather than a later path replacement", async () => {
    const source = resolve(process.cwd(), "../..");
    const root = await realpath(await mkdtemp(join(tmpdir(), "chirality-captured-roles-")));
    await mkdir(join(root, "agents"), { recursive: true });
    const captured = await readFile(join(source, "agents", "registry.json"), "utf8");
    for (const name of ["HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK"]) await writeFile(join(root, "agents", `AGENT_${name}.md`), `# ${name}\n`, "utf8");
    await writeFile(join(root, "agents", "ALTERNATE.md"), "# alternate\n", "utf8");
    const replacement = JSON.parse(captured) as { roles: Record<string, { instruction: string }> };
    replacement.roles.HELP_HUMAN!.instruction = "agents/ALTERNATE.md";
    await writeFile(join(root, "agents", "registry.json"), JSON.stringify(replacement), "utf8");
    const roles = await loadRolesFromCapturedRegistry(root, captured);
    expect(roles.roles.find(role => role.id === "HELP_HUMAN")?.instruction).toBe("agents/AGENT_HELP_HUMAN.md");
  });
});
