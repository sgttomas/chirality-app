// @vitest-environment node
// Staging the pinned Codex: OpenAI's package whole, with its layout kept, that version and target only,
// signed by its team; anything else refused, and nothing staged from it.
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { chmodSync, copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";

import { checkCodex, checkTarget, stageCodex, team } from "./codex.mjs";
import { digest, files } from "./library.mjs";

let root;
afterEach(() => root && rmSync(root, { recursive: true, force: true }));

const signedBy = (name) => () => name;

/** A small package laid out as Codex's (an entrypoint that answers --version, its helpers, codex-path,
 * codex-resources with a notice and a licence) in a folder whose name has a space; its archive; and
 * its codex.json. */
function release({ version = "0.0.1", target = "aarch64-apple-darwin" } = {}) {
  root = mkdtempSync(join(tmpdir(), "codex test "));
  const source = join(root, "extracted package");
  const manifest = { layoutVersion: 1, version, target, variant: "codex", entrypoint: "bin/codex", execServer: "bin/codex-exec-server", resourcesDir: "codex-resources", pathDir: "codex-path" };
  for (const [path, text, mode] of [
    ["codex-package.json", JSON.stringify(manifest, null, 2), 0o644],
    ["bin/codex", `#!/bin/sh\necho "codex-cli ${version}"\n`, 0o755],
    ["bin/codex-exec-server", "#!/bin/sh\n", 0o755],
    ["bin/codex-code-mode-host", "#!/bin/sh\n", 0o755],
    ["codex-path/rg", "#!/bin/sh\n", 0o755],
    ["codex-resources/voice/NOTICE.md", "# Notices\n", 0o644],
    ["codex-resources/voice/licenses/zlib.txt", "zlib licence\n", 0o644],
  ]) {
    mkdirSync(join(source, path, ".."), { recursive: true });
    writeFileSync(join(source, path), text, { mode });
  }
  const archive = join(root, "codex package.tar.gz");
  execFileSync("tar", ["-czf", archive, "-C", source, "."], { env: { ...process.env, COPYFILE_DISABLE: "1" } });
  const bytes = readFileSync(archive);
  const pin = {
    tag: "codex-0.0.1-aarch64-apple-darwin",
    version: "0.0.1",
    target: "aarch64-apple-darwin",
    layoutVersion: 1,
    entrypoint: "bin/codex",
    team: "TESTTEAM",
    archive: { name: "codex package.tar.gz", size: bytes.length, sha256: createHash("sha256").update(bytes).digest("hex") },
    files: files(source).length,
    digest: digest(source),
  };
  return { source, archive, dir: join(root, "resources", "codex"), pin };
}

describe("staging the pinned Codex", () => {
  it("stages the package from its archive with its layout kept, so its entrypoint runs from there", () => {
    const { source, archive, dir, pin } = release();
    stageCodex(archive, dir, pin, signedBy("TESTTEAM"));
    const staged = join(dir, pin.tag);
    expect(checkCodex(dir, pin, signedBy("TESTTEAM"))).toBeNull();
    expect(files(staged).sort()).toEqual(files(source).sort());
    for (const exe of ["bin/codex", "bin/codex-exec-server", "codex-path/rg"]) expect(statSync(join(staged, exe)).mode & 0o100).not.toBe(0);
    expect(execFileSync(join(staged, pin.entrypoint), ["--version"], { encoding: "utf8" })).toBe("codex-cli 0.0.1\n");
    expect(existsSync(join(staged, "codex-resources/voice/licenses/zlib.txt"))).toBe(true);
  });

  it("stages the package from its extracted folder", () => {
    const { source, dir, pin } = release();
    stageCodex(source, dir, pin, signedBy("TESTTEAM"));
    expect(checkCodex(dir, pin, signedBy("TESTTEAM"))).toBeNull();
  });

  it("refuses an archive whose digest or size is not the pinned one", () => {
    const { archive, dir, pin } = release();
    expect(() => stageCodex(archive, dir, { ...pin, archive: { ...pin.archive, sha256: "0".repeat(64) } }, signedBy("TESTTEAM"))).toThrow(/is not codex package\.tar\.gz/);
    expect(() => stageCodex(archive, dir, { ...pin, archive: { ...pin.archive, size: pin.archive.size + 1 } }, signedBy("TESTTEAM"))).toThrow(/is not codex package\.tar\.gz/);
    expect(existsSync(dir)).toBe(false);
  });

  it("refuses a folder of another version or target, by its codex-package.json, and stages nothing", () => {
    const { pin, dir } = release();
    const other = release({ version: "0.0.2" });
    expect(() => stageCodex(other.source, dir, pin, signedBy("TESTTEAM"))).toThrow(/is Codex 0\.0\.2 for aarch64-apple-darwin, not 0\.0\.1 for aarch64-apple-darwin/);
    const intel = release({ target: "x86_64-apple-darwin" });
    expect(() => stageCodex(intel.source, intel.dir, pin, signedBy("TESTTEAM"))).toThrow(/for x86_64-apple-darwin, not 0\.0\.1 for aarch64-apple-darwin/);
    expect(existsSync(intel.dir)).toBe(false);
  });

  it("refuses a folder that is not a Codex package, or whose files are not the package's", () => {
    const { source, dir, pin } = release();
    rmSync(join(source, "codex-package.json"));
    expect(() => stageCodex(source, dir, pin, signedBy("TESTTEAM"))).toThrow(/no codex-package\.json/);
    const again = release();
    writeFileSync(join(again.source, "bin/codex"), "#!/bin/sh\necho changed\n");
    expect(() => stageCodex(again.source, again.dir, again.pin, signedBy("TESTTEAM"))).toThrow(/is not codex-0\.0\.1-aarch64-apple-darwin/);
  });

  it("refuses an entrypoint not signed by the pinned team", () => {
    const { source, dir, pin } = release();
    expect(() => stageCodex(source, dir, pin, signedBy(null))).toThrow(/bin\/codex is not signed by TESTTEAM$/);
    expect(() => stageCodex(source, dir, pin, signedBy("OTHER"))).toThrow(/is not signed by TESTTEAM but by OTHER/);
    expect(existsSync(dir)).toBe(false);
  });

  it("refuses a helper its owner cannot run, staged or to be staged, though others can", () => {
    const { source, dir, pin } = release();
    stageCodex(source, dir, pin, signedBy("TESTTEAM"));
    chmodSync(join(dir, pin.tag, "codex-path/rg"), 0o645);
    expect(checkCodex(dir, pin, signedBy("TESTTEAM"))).toMatch(/is not codex-0\.0\.1-aarch64-apple-darwin/);
    chmodSync(join(source, "codex-path/rg"), 0o645);
    expect(() => stageCodex(source, dir, pin, signedBy("TESTTEAM"))).toThrow(/is not codex-0\.0\.1-aarch64-apple-darwin/);
  });

  it("is bundled for the package's target only", () => {
    const { pin } = release();
    expect(checkTarget(undefined, pin)).toBeNull();
    expect(checkTarget("aarch64-apple-darwin", pin)).toBeNull();
    for (const triple of ["x86_64-apple-darwin", "universal-apple-darwin"]) expect(checkTarget(triple, pin)).toBe(`Codex 0.0.1 is bundled for aarch64-apple-darwin only; this build is for ${triple}`);
  });

  it("finds no team on a file that is not signed", () => {
    const { source } = release();
    expect(team(join(source, "bin/codex"))).toBeNull();
  });

  it("refuses anything staged beside the package, or a file missing from it", () => {
    const { source, dir, pin } = release();
    stageCodex(source, dir, pin, signedBy("TESTTEAM"));
    mkdirSync(join(dir, "codex-9.9.9-aarch64-apple-darwin"));
    expect(checkCodex(dir, pin, signedBy("TESTTEAM"))).toMatch(/holds more than codex-0\.0\.1-aarch64-apple-darwin/);
    rmSync(join(dir, "codex-9.9.9-aarch64-apple-darwin"), { recursive: true });
    rmSync(join(dir, pin.tag, "bin/codex-code-mode-host"));
    expect(checkCodex(dir, pin, signedBy("TESTTEAM"))).toMatch(/is not codex-0\.0\.1-aarch64-apple-darwin: 6 files/);
  });

  it("runs as npm run codex from a folder whose path has spaces, and refuses a package OpenAI did not sign", () => {
    const { archive, pin } = release();
    const app = join(root, "my app");
    mkdirSync(join(app, "scripts"), { recursive: true });
    for (const script of ["codex.mjs", "library.mjs"]) copyFileSync(fileURLToPath(new URL(`./${script}`, import.meta.url)), join(app, "scripts", script));
    writeFileSync(join(app, "codex.json"), JSON.stringify(pin));
    const run = (env) => spawnSync(process.execPath, [join(app, "scripts", "codex.mjs")], { env: { ...process.env, ...env }, encoding: "utf8" });
    const unsigned = run({ CHIRALITY_CODEX: archive });
    expect(unsigned.status).not.toBe(0);
    expect(unsigned.stderr).toMatch(/bin\/codex is not signed by TESTTEAM/);
    expect(existsSync(join(app, "src-tauri/codex"))).toBe(false);
    const intel = run({ CHIRALITY_CODEX: archive, TAURI_ENV_TARGET_TRIPLE: "x86_64-apple-darwin" });
    expect(intel.stderr).toMatch(/bundled for aarch64-apple-darwin only; this build is for x86_64-apple-darwin/);
    expect(existsSync(join(app, "src-tauri/codex"))).toBe(false);
    const unstaged = run({ CHIRALITY_CODEX: "" });
    expect(unstaged.stderr).toMatch(/src-tauri\/codex is missing; set CHIRALITY_CODEX to codex package\.tar\.gz or its extracted folder/);
  });
});
