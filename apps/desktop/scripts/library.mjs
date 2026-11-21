// Puts the Library edition the app bundles (library.json) among its resources,
// at src-tauri/library/<tag> (its workflows and licence), from an extracted copy of that edition:
//   CHIRALITY_LIBRARY=<the edition's folder, holding workflows/ and LICENSE.md> npm run library
// Every file is checked against the edition's digest, and its licence, first. With the edition
// already in place and no folder given, it checks what is there.
import { createHash } from "node:crypto";
import { cpSync, existsSync, readdirSync, readFileSync, rmSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const here = new URL("..", import.meta.url).pathname;
const edition = JSON.parse(readFileSync(join(here, "library.json"), "utf8"));
const target = join(here, "src-tauri/library", edition.tag);

function files(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const path = join(dir, e.name);
    if (e.name === ".DS_Store") return [];
    return e.isDirectory() ? files(path) : [path];
  });
}

/** sha256 of the sorted "<sha256>  <path>" lines of every file under `dir`. */
export function digest(dir) {
  const lines = files(dir)
    .map((path) => `${createHash("sha256").update(readFileSync(path)).digest("hex")}  ${relative(dir, path)}`)
    .sort();
  return createHash("sha256").update(lines.join("\n") + "\n").digest("hex");
}

const sha256 = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");

/** Why `root` (holding workflows/ and LICENSE.md) is not the edition, if it is not. */
function check(root) {
  const dir = join(root, "workflows");
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return `${dir} is not a folder`;
  const found = digest(dir);
  if (found !== edition.digest) return `${dir} is not ${edition.tag} (digest ${found})`;
  const license = join(root, "LICENSE.md");
  return existsSync(license) && sha256(license) === edition.license ? null : `${license} is not ${edition.tag}'s licence`;
}

const source = process.env.CHIRALITY_LIBRARY;
if (source) {
  const problem = check(source);
  if (problem) throw new Error(problem);
  rmSync(target, { recursive: true, force: true });
  cpSync(join(source, "workflows"), join(target, "workflows"), { recursive: true, filter: (p) => !p.endsWith(".DS_Store") });
  cpSync(join(source, "LICENSE.md"), join(target, "LICENSE.md"));
}
const problem = check(target);
if (problem) throw new Error(source ? problem : `${problem}; set CHIRALITY_LIBRARY to the extracted ${edition.tag}`);
console.log(`${edition.tag} (${edition.commit}) is in ${relative(here, target)}`);
