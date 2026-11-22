// Puts the pinned Codex (codex.json) among the app's resources, whole, with its layout kept:
// src-tauri/codex/<tag> holds OpenAI's release package (bin/codex and its helpers, codex-path,
// codex-resources with their notices and licences), which the app runs from there. From that archive,
// or a folder it was extracted to:
//   CHIRALITY_CODEX=<codex-package-aarch64-apple-darwin.tar.gz, or its extracted folder> npm run codex
// The archive is checked against codex.json's size and sha256; the package's codex-package.json
// against its version, target and layout; every file against codex.json's digest of the whole tree;
// and the entrypoint's signature against its team. Staging is the Library's (library.mjs): beside the
// resources, swapped in only once checked. With no source given, it checks what is staged.
import { spawnSync } from "node:child_process";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

import { checkStaged, recover, stage } from "./library.mjs";

/** The team that signed `path`, if its signature is valid; null if it is not signed or not valid. */
export function team(path) {
  if (spawnSync("codesign", ["--verify", "--strict", path]).status !== 0) return null;
  const shown = spawnSync("codesign", ["-dv", "--verbose=2", path], { encoding: "utf8" });
  return /^TeamIdentifier=(\S+)$/m.exec(shown.stderr ?? "")?.[1] ?? null;
}

/** Why the package at `root` is not `pin`'s version, target and layout, by its codex-package.json. */
export function checkPackage(root, pin) {
  const path = join(root, "codex-package.json");
  if (!lstatSync(path, { throwIfNoEntry: false })?.isFile()) return `${root} is not a Codex package: no codex-package.json`;
  let meta;
  try {
    meta = JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return `${path} is not JSON`;
  }
  if (meta.version !== pin.version || meta.target !== pin.target) return `${root} is Codex ${meta.version} for ${meta.target}, not ${pin.version} for ${pin.target}`;
  if (meta.layoutVersion !== pin.layoutVersion || meta.entrypoint !== pin.entrypoint) return `${root} is not laid out as ${pin.tag}: layout ${meta.layoutVersion}, entrypoint ${meta.entrypoint}`;
  return null;
}

/** Why the entrypoint of the package at `root` is not signed by `pin`'s team, if it is not. */
export function checkSigned(root, pin, signer = team) {
  const entry = join(root, pin.entrypoint);
  const found = signer(entry);
  return found === pin.team ? null : `${entry} is not signed by ${pin.team}${found ? ` but by ${found}` : ""}`;
}

/** What `stage` checks of a package before its digest. */
const inspect = (pin, signer) => (root) => checkPackage(root, pin) ?? checkSigned(root, pin, signer);

/** Stages `source` (`pin`'s archive, or a folder it was extracted to) as the whole of `dir`. */
export function stageCodex(source, dir, pin, signer = team) {
  stage(source, dir, pin, inspect(pin, signer));
}

/** Why `dir` (the staged resources) is not exactly `pin`'s package, if it is not. */
export function checkCodex(dir, pin, signer = team) {
  return checkStaged(dir, pin) ?? inspect(pin, signer)(join(dir, pin.tag));
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const here = fileURLToPath(new URL("..", import.meta.url));
  const pin = JSON.parse(readFileSync(join(here, "codex.json"), "utf8"));
  const dir = join(here, "src-tauri", "codex");
  const source = process.env.CHIRALITY_CODEX;
  recover(dir, source);
  if (source) stageCodex(source, dir, pin);
  const problem = checkCodex(dir, pin);
  if (problem) throw new Error(source ? problem : `${problem}; set CHIRALITY_CODEX to ${pin.archive.name} or its extracted folder`);
  console.log(`Codex ${pin.version} (${pin.target}) is in ${relative(here, join(dir, pin.tag))}, whole, and nothing else is`);
}
