import { lstat, mkdir, mkdtemp, readdir, readFile, readlink, realpath, rm, stat, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { isExcludedCodexHomeEntry, prepareCodexEffectiveHome } from "../packages/daemon/src/codex-effective-home.js";

const roots: string[] = [];
afterEach(async () => { await Promise.all(roots.splice(0).map(root => rm(root, { recursive: true, force: true }))); });

async function snapshot(directory: string): Promise<Record<string, string>> {
  const result: Record<string, string> = {};
  for (const name of (await readdir(directory)).sort()) {
    const info = await lstat(join(directory, name));
    result[name] = info.isSymbolicLink() ? `link:${await readlink(join(directory, name))}` : info.isDirectory() ? `dir:${info.mtimeMs}` : `file:${info.size}:${info.mtimeMs}`;
  }
  return result;
}

async function fakeUserHome(root: string): Promise<string> {
  const home = join(root, "user-codex");
  await mkdir(join(home, "sessions", "2026"), { recursive: true });
  await mkdir(join(home, "skills"), { recursive: true });
  await writeFile(join(home, "config.toml"), 'model = "gpt-5-codex"\n', "utf8");
  await writeFile(join(home, "AGENTS.md"), "# user instructions\n", "utf8");
  await writeFile(join(home, "history.jsonl"), "", "utf8");
  await writeFile(join(home, "auth.json"), '{"fixture":"never-read"}', "utf8");
  await writeFile(join(home, "auth.json.bak"), "x", "utf8");
  await writeFile(join(home, "models_cache.json"), "{}", "utf8");
  await writeFile(join(home, "version.lock"), "", "utf8");
  return home;
}

describe("Codex effective home overlay", () => {
  it("links every shared entry, excludes credential and cache files, and never writes into the user's home", async () => {
    const root = await realpath(await mkdtemp(join(tmpdir(), "codex-home-")));
    roots.push(root);
    const userCodexHome = await fakeUserHome(root);
    const before = await snapshot(userCodexHome);
    const effectiveHome = join(root, "runtime", "codex-home");
    const report = await prepareCodexEffectiveHome({ userCodexHome, effectiveHome });
    expect(report).toMatchObject({ effectiveHome, userCodexHome, userHomePresent: true, linked: ["AGENTS.md", "config.toml", "history.jsonl", "sessions", "skills"], excluded: ["auth.json", "auth.json.bak", "models_cache.json", "version.lock"], removed: [], retained: [] });
    expect((await stat(effectiveHome)).mode & 0o777).toBe(0o700);
    for (const name of report.linked) {
      expect(await readlink(join(effectiveHome, name))).toBe(join(userCodexHome, name));
    }
    expect(await readFile(join(effectiveHome, "config.toml"), "utf8")).toContain("gpt-5-codex");
    expect((await readdir(effectiveHome)).sort()).toEqual(["AGENTS.md", "config.toml", "history.jsonl", "sessions", "skills"]);
    expect(await snapshot(userCodexHome)).toEqual(before);
  });

  it("refreshes stale links, removes dangling ones, and retains files Codex created in the overlay", async () => {
    const root = await realpath(await mkdtemp(join(tmpdir(), "codex-home-")));
    roots.push(root);
    const userCodexHome = await fakeUserHome(root);
    const effectiveHome = join(root, "codex-home");
    await mkdir(effectiveHome, { recursive: true });
    await symlink(join(root, "elsewhere", "config.toml"), join(effectiveHome, "config.toml"));
    await symlink(join(root, "gone"), join(effectiveHome, "stale"));
    await symlink(join(userCodexHome, "auth.json"), join(effectiveHome, "auth.json"));
    await writeFile(join(effectiveHome, "models_cache.json"), "{}", "utf8");
    await mkdir(join(effectiveHome, "log"));
    await writeFile(join(effectiveHome, "skills"), "a real file shadows the shared entry", "utf8");
    const report = await prepareCodexEffectiveHome({ userCodexHome, effectiveHome });
    expect(report.removed).toEqual(["auth.json", "stale"]);
    expect(report.retained).toEqual(["log", "models_cache.json", "skills"]);
    expect(report.linked).toEqual(["AGENTS.md", "config.toml", "history.jsonl", "sessions"]);
    expect(await readlink(join(effectiveHome, "config.toml"))).toBe(join(userCodexHome, "config.toml"));
    expect((await lstat(join(effectiveHome, "skills"))).isSymbolicLink()).toBe(false);
    await expect(lstat(join(effectiveHome, "auth.json"))).rejects.toMatchObject({ code: "ENOENT" });
    const again = await prepareCodexEffectiveHome({ userCodexHome, effectiveHome });
    expect(again).toMatchObject({ removed: [], linked: report.linked, retained: report.retained });
  });

  it("yields an empty overlay when the user has no Codex home and refuses aliases", async () => {
    const root = await realpath(await mkdtemp(join(tmpdir(), "codex-home-")));
    roots.push(root);
    const report = await prepareCodexEffectiveHome({ userCodexHome: join(root, "missing"), effectiveHome: join(root, "overlay") });
    expect(report).toMatchObject({ userHomePresent: false, linked: [], excluded: [] });
    expect(await readdir(join(root, "overlay"))).toEqual([]);
    await expect(prepareCodexEffectiveHome({ userCodexHome: join(root, "same"), effectiveHome: join(root, "same") })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
    await mkdir(join(root, "real"));
    await symlink(join(root, "real"), join(root, "alias"));
    await expect(prepareCodexEffectiveHome({ userCodexHome: join(root, "missing"), effectiveHome: join(root, "alias") })).rejects.toMatchObject({ code: "FORBIDDEN" });
    await expect(prepareCodexEffectiveHome({ userCodexHome: "relative/home", effectiveHome: join(root, "x") })).rejects.toMatchObject({ code: "INVALID_REQUEST" });
  });

  it("names the excluded entries exactly", () => {
    for (const name of ["auth.json", "auth.json.tmp", "authorized", "models_cache.json", "anything.lock"]) expect(isExcludedCodexHomeEntry(name)).toBe(true);
    for (const name of ["config.toml", "sessions", "AGENTS.md", "history.jsonl", "skills", "log"]) expect(isExcludedCodexHomeEntry(name)).toBe(false);
  });
});
