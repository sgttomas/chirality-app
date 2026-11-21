// @vitest-environment node
// Staging the Library edition: real files only, that edition only, every file accounted for.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it } from "vitest";

import { checkStaged, digest, stage } from "./library.mjs";

let root;
afterEach(() => root && rmSync(root, { recursive: true, force: true }));

/** An extracted edition (two workflows and a licence) under a folder whose name has a space, and its library.json. */
function edition() {
  root = mkdtempSync(join(tmpdir(), "library test "));
  const source = join(root, "extracted edition");
  for (const [path, text] of [["workflows/estimate/WORKFLOW.md", "# Estimate\n"], ["workflows/scope/WORKFLOW.md", "# Scope\n"]]) {
    mkdirSync(join(source, path, ".."), { recursive: true });
    writeFileSync(join(source, path), text);
  }
  writeFileSync(join(source, "LICENSE.md"), "Licence\n");
  const meta = {
    tag: "library-v0.0.1",
    digest: digest(join(source, "workflows")),
    license: createHash("sha256").update(readFileSync(join(source, "LICENSE.md"))).digest("hex"),
  };
  return { source, library: join(root, "resources", "library"), meta };
}

describe("staging the Library edition", () => {
  it("stages the edition as real files, under its tag, and checks it", () => {
    const { source, library, meta } = edition();
    writeFileSync(join(source, "workflows", ".DS_Store"), "finder");
    stage(source, library, meta);
    expect(readFileSync(join(library, meta.tag, "workflows/scope/WORKFLOW.md"), "utf8")).toBe("# Scope\n");
    expect(checkStaged(library, meta)).toBeNull();
  });

  it("refuses a workflows folder that is a link, and a link inside it", () => {
    const { source, library, meta } = edition();
    const linked = join(root, "linked");
    symlinkSync(join(source, "workflows"), linked);
    const viaLink = join(root, "via link");
    mkdirSync(viaLink);
    symlinkSync(linked, join(viaLink, "workflows"));
    writeFileSync(join(viaLink, "LICENSE.md"), readFileSync(join(source, "LICENSE.md")));
    expect(() => stage(viaLink, library, meta)).toThrow(/workflows is a link/);

    symlinkSync(join(source, "workflows/scope/WORKFLOW.md"), join(source, "workflows/estimate/LINK.md"));
    expect(() => stage(source, library, meta)).toThrow(/LINK\.md is a link/);
  });

  it("refuses a staged link even where the digest would match through it", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    rmSync(join(library, meta.tag, "workflows"), { recursive: true });
    symlinkSync(join(source, "workflows"), join(library, meta.tag, "workflows"));
    expect(checkStaged(library, meta)).toMatch(/workflows is a link/);
  });

  it("refuses another edition beside it, and any file added to or missing from it", () => {
    const { source, library, meta } = edition();
    stage(source, library, meta);
    mkdirSync(join(library, "library-v9.9.9/workflows/extra"), { recursive: true });
    writeFileSync(join(library, "library-v9.9.9/workflows/extra/WORKFLOW.md"), "# Extra\n");
    expect(checkStaged(library, meta)).toMatch(/holds more than library-v0\.0\.1: library-v9\.9\.9/);
    rmSync(join(library, "library-v9.9.9"), { recursive: true });

    writeFileSync(join(library, meta.tag, "NOTES.md"), "extra");
    expect(checkStaged(library, meta)).toMatch(/holds more than its workflows and licence: NOTES\.md/);
    rmSync(join(library, meta.tag, "NOTES.md"));

    writeFileSync(join(library, meta.tag, "workflows/scope/extra.md"), "extra");
    expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1/);
    rmSync(join(library, meta.tag, "workflows/scope/extra.md"));

    writeFileSync(join(library, meta.tag, "workflows/.DS_Store"), "finder");
    expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1/);
    rmSync(join(library, meta.tag, "workflows/.DS_Store"));

    rmSync(join(library, meta.tag, "workflows/estimate/WORKFLOW.md"));
    expect(checkStaged(library, meta)).toMatch(/is not library-v0\.0\.1/);
  });

  it("replaces whatever was staged before", () => {
    const { source, library, meta } = edition();
    mkdirSync(join(library, "library-v0.0.0"), { recursive: true });
    stage(source, library, meta);
    expect(checkStaged(library, meta)).toBeNull();
  });

  it("runs as npm run library from a folder whose path has spaces", () => {
    const { source, meta } = edition();
    const app = join(root, "my app");
    mkdirSync(join(app, "scripts"), { recursive: true });
    copyFileSync(fileURLToPath(new URL("./library.mjs", import.meta.url)), join(app, "scripts", "library.mjs"));
    writeFileSync(join(app, "library.json"), JSON.stringify({ ...meta, commit: "0".repeat(40) }));
    const out = execFileSync(process.execPath, [join(app, "scripts", "library.mjs")], { env: { ...process.env, CHIRALITY_LIBRARY: source }, encoding: "utf8" });
    expect(out).toMatch(/library-v0\.0\.1 .* is in src-tauri\/library\/library-v0\.0\.1, and nothing else is/);
    expect(existsSync(join(app, "src-tauri/library", meta.tag, "workflows/scope/WORKFLOW.md"))).toBe(true);
  });
});
