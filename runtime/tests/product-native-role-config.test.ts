import { createHash } from "node:crypto";
import { mkdir, mkdtemp, readFile, realpath, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, expect, it } from "vitest";
import { CHIRALITY_ROLE_NAMES, type ResolveSelectedContextResponse } from "@chirality/runtime-contracts";
import { materializeProductNativeRoles } from "../packages/core/src/product-native-role-config.js";

const directories: string[] = [];
afterEach(async () => { for (const path of directories.splice(0)) await rm(path, { recursive: true, force: true }); });
async function fixture() {
  const root = await realpath(await mkdtemp(join(tmpdir(), "product-roles-"))); directories.push(root);
  const entry = (id: string, content: string, kind = "resource") => ({ id, content, kind, sha256: createHash("sha256").update(content).digest("hex") });
  const context = { supplied: [entry("root:AGENTS", "common", "root"), entry("product:library", "library"), ...CHIRALITY_ROLE_NAMES.map(role => entry(`native-role:${role}`, `# ${role}`))] } as ResolveSelectedContextResponse;
  return { root, directory: join(root, "roles"), context };
}
it("rejects directory aliases and file substitutions without changing their targets", async () => {
  const f = await fixture();
  const target = join(f.root, "elsewhere"); await mkdir(target);
  await symlink(target, f.directory);
  await expect(materializeProductNativeRoles(f.context, f.directory)).rejects.toThrow(/canonical/);
  await rm(f.directory);
  const config = await materializeProductNativeRoles(f.context, f.directory);
  const path = config["agents.TASK.config_file"]!;
  const bytes = await readFile(path, "utf8");
  const targetFile = join(target, "role.toml"); await writeFile(targetFile, bytes);
  await rm(path); await symlink(targetFile, path);
  await expect(materializeProductNativeRoles(f.context, f.directory)).rejects.toThrow();
  expect(await readFile(targetFile, "utf8")).toBe(bytes);
});
it("rejects an aliased parent before creating the materialization directory", async () => {
  const f = await fixture();
  const alias = join(f.root, "alias"); await symlink(f.root, alias);
  await expect(materializeProductNativeRoles(f.context, join(alias, "roles"))).rejects.toThrow(/canonical/);
  await expect(readFile(f.directory)).rejects.toMatchObject({ code: "ENOENT" });
});
