// @vitest-environment node
// Staging the Library edition: the whole edition as released, real files only, that edition only,
// every file accounted for; and never at the cost of its source or of what was staged before.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { chmodSync, copyFileSync, cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, renameSync, rmSync, statSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";

import { checkStaged, digest, files, recover, stage } from "./library.mjs";

const statMode = (path) => statSync(path).mode;

let root;
afterEach(() => root && rmSync(root, { recursive: true, force: true }));

/** A required step: the Library's enum check, as the edition's workflows run it from its root. */
const VALIDATE_ENUM = `import sys
ENUMS = {"BASIS_OF_ESTIMATE": ["QUOTE", "RATE_TABLE"]}
ok = sys.argv[2] in ENUMS.get(sys.argv[1], [])
print("valid" if ok else "invalid")
sys.exit(0 if ok else 1)
`;

/** An extracted edition (workflows, a tool they run, files at its top) under a folder whose name has
 * a space; its source archive; and its library.json. */
function edition() {
  root = mkdtempSync(join(tmpdir(), "library test "));
  const source = join(root, "extracted edition");
  for (const [path, text] of [
    ["workflows/estimate-snapshot/WORKFLOW.md", "Run `python3 tools/validation/validate_enum.py BASIS_OF_ESTIMATE {BASIS}`.\n"],
    ["workflows/scope/WORKFLOW.md", "# Scope\n"],
    ["tools/validation/validate_enum.py", VALIDATE_ENUM],
    [".github/CODEOWNERS", "* @owner\n"],
    ["LICENSE.md", "Licence\n"],
    ["README.md", "# Library\n"],
  ]) {
    mkdirSync(join(source, path, ".."), { recursive: true });
    writeFileSync(join(source, path), text);
  }
  const archive = join(root, "edition source.tar");
  execFileSync("tar", ["-cf", archive, "-C", source, "."], { env: { ...process.env, COPYFILE_DISABLE: "1" } });
  const meta = {
    tag: "library-v0.0.1",
    archive: { name: "edition source.tar", sha256: createHash("sha256").update(readFileSync(archive)).digest("hex") },
    files: files(source).length,
    digest: digest(source),
  };
  return { source, archive, library: join(root, "resources", "library"), meta };
}

describe("staging the Library edition", () => {
  it("stages the whole edition, so a step its workflows run outside workflows/ runs from the staged copy", () => {
    const { source, library, meta } = edition();
    writeFileSync(join(source, "workflows", ".DS_Store"), "finder");
    stage(source, library, meta);
    const staged = join(library, meta.tag);
    expect(checkStaged(library, meta)).toBeNull();
    expect(files(staged).sort()).toEqual(files(source, (n) => n === ".DS_Store").sort());
    const run = (value) => execFileSync("python3", ["tools/validation/validate_enum.py", "BASIS_OF_ESTIMATE", value], { cwd: staged, encoding: "utf8" });
    expect(run("QUOTE")).toBe("valid\n");
    expect(() => run("GUESS")).toThrow();
  });

  it("stages from the edition's archive, and refuses an archive that is not it", () => {
    const { archive, library, meta } = edition();
    stage(archive, library, meta);
    expect(checkStaged(library, meta)).toBeNull();
    expect(() => stage(archive, library, { ...meta, archive: { ...meta.archive, sha256: "0".repeat(64) } })).toThrow(/is not edition source\.tar/);
  });

  it("refuses a source that is a link, and a link inside it", () => {
    const { source, library, meta } = edition();
    symlinkSync(join(source, "workflows/scope/WORKFLOW.md"), join(source, "workflows/estimate-snapshot/LINK.md"));
    expect(() => stage(source, library, meta)).toThrow(/LINK\.md is a link/);
    rmSync(join(source, "workflows/estimate-snapshot/LINK.md"));
    const viaLink = join(root, "via link");
    mkdirSync(viaLink);
    symlinkSync(join(source, "tools"), join(viaLink, "tools"));
    expect(() => stage(viaLink, library, meta)).toThrow(/tools is a link/);
    const link = join(root, "link to edition");
    symlinkSync(source, link);
    expect(() => stage(link, library, meta)).toThrow(/link to edition is a link/);
    expect(existsSync(library)).toBe(false);
  });

  it("refuses an edition whose file lost its executable flag, or that gained an empty folder", () => {
    const { source, library, meta: plain } = edition();
    chmodSync(join(source, "tools/validation/validate_enum.py"), 0o755);
    const meta = { ...plain, digest: digest(source) };
    expect(meta.digest).not.toBe(plain.digest);
    stage(source, library, meta);
    expect((0o111 & Number(statMode(join(library, meta.tag, "tools/validation/validate_enum.py")))) !== 0).toBe(true);
    chmodSync(join(library, meta.tag, "tools/validation/validate_enum.py"), 0o644);
    expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1/);
    chmodSync(join(library, meta.tag, "tools/validation/validate_enum.py"), 0o755);
    mkdirSync(join(library, meta.tag, "workflows/empty"));
    expect(checkStaged(library, meta)).toMatch(/empty is an empty folder/);
  });

  it("refuses a staged link even where the digest would match through it", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    rmSync(join(library, meta.tag, "tools"), { recursive: true });
    symlinkSync(join(source, "tools"), join(library, meta.tag, "tools"));
    expect(checkStaged(library, meta)).toMatch(/tools is a link/);
  });

  it("refuses another edition beside it, and any file added to or missing from it", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    mkdirSync(join(library, "library-v9.9.9/workflows"), { recursive: true });
    expect(checkStaged(library, meta)).toMatch(/holds more than library-v0\.0\.1: library-v9\.9\.9/);
    rmSync(join(library, "library-v9.9.9"), { recursive: true });
    for (const extra of ["NOTES.md", "workflows/scope/extra.md", "workflows/.DS_Store"]) {
      writeFileSync(join(library, meta.tag, extra), "extra");
      expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1: 7 files/);
      rmSync(join(library, meta.tag, extra));
    }
    rmSync(join(library, meta.tag, "README.md"));
    expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1: 5 files/);
  });

  it("refuses a source inside what it would replace, or holding it, and both survive", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    const staged = join(library, meta.tag);
    expect(() => stage(staged, library, meta)).toThrow(/overlaps/);
    expect(checkStaged(library, meta)).toBeNull();
    expect(() => stage(source, join(source, "resources", "library"), meta)).toThrow(/overlaps/);
    expect(digest(source, (n) => n === ".DS_Store")).toBe(meta.digest);
  });

  it("refuses a source inside what it would replace however either is spelled, and it survives", () => {
    const { source, archive, library, meta } = edition();
    stage(source, library, meta);
    // An entry of the staged folder whose name starts with two dots.
    const inside = join(library, "..edition");
    cpSync(source, inside, { recursive: true });
    expect(() => stage(inside, library, meta)).toThrow(/overlaps/);
    expect(digest(inside)).toBe(meta.digest);
    const tar = join(library, "..source.tar");
    copyFileSync(archive, tar);
    expect(() => stage(tar, library, meta)).toThrow(/overlaps/);
    expect(existsSync(tar)).toBe(true);
    // The staged folder reached by another name: a link to it, and (where the volume ignores case) another case.
    const alias = join(root, "resources", "alias");
    symlinkSync(library, alias);
    expect(() => stage(inside, alias, meta)).toThrow(/overlaps/);
    if (existsSync(join(root, "resources", "LIBRARY"))) expect(() => stage(inside, join(root, "resources", "LIBRARY"), meta)).toThrow(/overlaps/);
    expect(digest(inside)).toBe(meta.digest);
  });

  it("puts back what an interrupted staging had set aside", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    // Stopped between setting the staged edition aside and putting the new one in its place.
    const work = join(library, "..", ".library-staging-stopped");
    mkdirSync(work);
    renameSync(library, join(work, "previous"));
    recover(library);
    expect(checkStaged(library, meta)).toBeNull();
    expect(readdirSync(join(library, ".."))).toEqual(["library"]);
  });

  it("leaves what was staged before when a staging fails, and no work behind", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    writeFileSync(join(source, "README.md"), "# Changed\n");
    expect(() => stage(source, library, meta)).toThrow(/is not library-v0\.0\.1/);
    expect(checkStaged(library, meta)).toBeNull();
    expect(readdirSync(join(library, ".."))).toEqual(["library"]);
  });

  it("replaces whatever was staged before", () => {
    const { source, library, meta } = edition();
    mkdirSync(join(library, "library-v0.0.0"), { recursive: true });
    stage(source, library, meta);
    expect(checkStaged(library, meta)).toBeNull();
  });

  it("runs as npm run library from a folder whose path has spaces", () => {
    const { archive, meta } = edition();
    const app = join(root, "my app");
    mkdirSync(join(app, "scripts"), { recursive: true });
    copyFileSync(fileURLToPath(new URL("./library.mjs", import.meta.url)), join(app, "scripts", "library.mjs"));
    writeFileSync(join(app, "library.json"), JSON.stringify({ ...meta, commit: "0".repeat(40) }));
    const out = execFileSync(process.execPath, [join(app, "scripts", "library.mjs")], { env: { ...process.env, CHIRALITY_LIBRARY: archive }, encoding: "utf8" });
    expect(out).toMatch(/library-v0\.0\.1 .* is in src-tauri\/library\/library-v0\.0\.1, whole, and nothing else is/);
    expect(existsSync(join(app, "src-tauri/library", meta.tag, "tools/validation/validate_enum.py"))).toBe(true);
  });
});
