// Puts the Library edition the app bundles (library.json) among its resources,
// at src-tauri/library/<tag> (its workflows and licence), from an extracted copy of that edition:
//   CHIRALITY_LIBRARY=<the edition's folder, holding workflows/ and LICENSE.md> npm run library
// The copy is checked against the edition's digest and licence first, and so is
// everything staged afterwards: src-tauri/library holds that edition and nothing
// else, as real files and folders. With no folder given, it checks what is staged.
import { createHash } from "node:crypto";
import { copyFileSync, lstatSync, mkdirSync, readdirSync, readFileSync, realpathSync, rmSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const sha256 = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");

/** What a path is, without following a link: "file", "folder", or why it is neither. */
function kind(path) {
  const stat = lstatSync(path, { throwIfNoEntry: false });
  if (!stat) return "missing";
  if (stat.isSymbolicLink()) return "a link";
  if (stat.isDirectory()) return "folder";
  if (stat.isFile()) return "file";
  return "not a file or folder";
}

/** Every file under `dir`, relative to it; a link or anything else not a file or folder is refused.
 * `skip` names entries left out (the source's Finder files). */
export function files(dir, skip = () => false) {
  return readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    if (skip(name)) return [];
    const k = kind(path);
    if (k === "folder") return files(path, skip).map((f) => join(name, f));
    if (k === "file") return [name];
    throw new Error(`${path} is ${k}`);
  });
}

/** sha256 of the sorted "<sha256>  <path>" lines of every file under `dir`. */
export function digest(dir, skip) {
  const lines = files(dir, skip).map((f) => `${sha256(join(dir, f))}  ${f}`).sort();
  return createHash("sha256").update(lines.join("\n") + "\n").digest("hex");
}

const finder = (name) => name === ".DS_Store";

/** Why `root` (holding workflows/ and LICENSE.md) is not `edition`, if it is not. */
function checkEdition(root, edition, skip) {
  const dir = join(root, "workflows");
  if (kind(dir) !== "folder") return `${dir} is ${kind(dir) === "missing" ? "missing" : `${kind(dir)}, not a folder`}`;
  const license = join(root, "LICENSE.md");
  if (kind(license) !== "file") return `${license} is ${kind(license)}`;
  const found = digest(dir, skip);
  if (found !== edition.digest) return `${dir} is not ${edition.tag} (digest ${found})`;
  return sha256(license) === edition.license ? null : `${license} is not ${edition.tag}'s licence`;
}

/** Why `library` (the staged resources) is not exactly `edition`, if it is not. */
export function checkStaged(library, edition) {
  try {
    if (kind(library) !== "folder") return `${library} is ${kind(library)}`;
    const extra = readdirSync(library).filter((n) => n !== edition.tag);
    if (extra.length) return `${library} holds more than ${edition.tag}: ${extra.join(", ")}`;
    const root = join(library, edition.tag);
    if (kind(root) !== "folder") return `${root} is ${kind(root)}`;
    const others = readdirSync(root).filter((n) => n !== "workflows" && n !== "LICENSE.md");
    if (others.length) return `${root} holds more than its workflows and licence: ${others.join(", ")}`;
    return checkEdition(root, edition);
  } catch (e) {
    return e.message;
  }
}

/** Copies real files and folders only, refusing links. */
function copy(from, to) {
  mkdirSync(to, { recursive: true });
  for (const name of readdirSync(from)) {
    if (finder(name)) continue;
    const k = kind(join(from, name));
    if (k === "folder") copy(join(from, name), join(to, name));
    else if (k === "file") copyFileSync(join(from, name), join(to, name));
    else throw new Error(`${join(from, name)} is ${k}`);
  }
}

/** Stages `source` (an extracted `edition`) as the whole of `library`, then checks what was staged. */
export function stage(source, library, edition) {
  const root = realpathSync(source);
  const problem = (() => {
    try {
      return checkEdition(root, edition, finder);
    } catch (e) {
      return e.message;
    }
  })();
  if (problem) throw new Error(problem);
  rmSync(library, { recursive: true, force: true });
  copy(join(root, "workflows"), join(library, edition.tag, "workflows"));
  copyFileSync(join(root, "LICENSE.md"), join(library, edition.tag, "LICENSE.md"));
  const staged = checkStaged(library, edition);
  if (staged) throw new Error(staged);
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const here = fileURLToPath(new URL("..", import.meta.url));
  const edition = JSON.parse(readFileSync(join(here, "library.json"), "utf8"));
  const library = join(here, "src-tauri", "library");
  const source = process.env.CHIRALITY_LIBRARY;
  if (source) stage(source, library, edition);
  const problem = checkStaged(library, edition);
  if (problem) throw new Error(source ? problem : `${problem}; set CHIRALITY_LIBRARY to the extracted ${edition.tag}`);
  console.log(`${edition.tag} (${edition.commit}) is in ${relative(here, join(library, edition.tag))}, and nothing else is`);
}
