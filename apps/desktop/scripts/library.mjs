// Puts the Library edition the app bundles (library.json) among its resources, whole, as released:
// src-tauri/library/<tag> holds the edition's source archive extracted (its workflows, the tools and
// files they run, its licence), with edition-relative paths kept. From that archive, or a folder it
// was extracted to:
//   CHIRALITY_LIBRARY=<chirality-library-…-source.tar, or its extracted folder> npm run library
// The archive is checked against library.json's archive digest, and every file of the edition against
// library.json's digest of the whole tree, before staging and again after; links are refused. It is
// staged beside the resources and swapped in only once checked, so a failure leaves them as they were.
// With no source given, it checks what is staged.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, realpathSync, renameSync, rmSync } from "node:fs";
import { basename, dirname, isAbsolute, join, relative, resolve } from "node:path";
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

const reason = (check) => {
  try {
    return check();
  } catch (e) {
    return e.message;
  }
};

/** Why `dir` is not the whole of `edition`, file by file, if it is not. */
function checkTree(dir, edition, skip) {
  if (kind(dir) !== "folder") return `${dir} is ${kind(dir)}`;
  const found = digest(dir, skip);
  if (found === edition.digest) return null;
  return `${dir} is not ${edition.tag}: ${files(dir, skip).length} files, digest ${found}; ${edition.tag} is ${edition.files} files`;
}

/** Why `library` (the staged resources) is not exactly `edition`, if it is not. */
export function checkStaged(library, edition) {
  return reason(() => {
    if (kind(library) !== "folder") return `${library} is ${kind(library)}`;
    const extra = readdirSync(library).filter((n) => n !== edition.tag);
    if (extra.length) return `${library} holds more than ${edition.tag}: ${extra.join(", ")}`;
    return checkTree(join(library, edition.tag), edition);
  });
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

/** Whether `path` is `folder` or inside it. */
function within(path, folder) {
  const rest = relative(folder, path);
  return rest === "" || (!rest.startsWith("..") && !isAbsolute(rest));
}

/** `path` with its nearest existing folder's real path. */
function real(path) {
  const parent = dirname(path);
  if (existsSync(path)) return realpathSync(path);
  return parent === path ? path : join(real(parent), basename(path));
}

/** Stages `source` (`edition`'s source archive, or a folder it was extracted to) as the whole of
 * `library`. Nothing is removed until the staged copy is checked; a source that overlaps `library`
 * is refused first. */
export function stage(source, library, edition) {
  const from = realpathSync(source);
  const to = join(real(dirname(resolve(library))), basename(library));
  const overlaps = [to, existsSync(to) ? realpathSync(to) : to].some((t) => within(from, t) || within(t, from));
  if (overlaps) throw new Error(`${source} overlaps ${library}: stage from an archive or extraction outside it`);
  mkdirSync(dirname(to), { recursive: true });
  const work = mkdtempSync(join(dirname(to), ".library-staging-"));
  try {
    let root = from;
    if (kind(from) === "file") {
      if (sha256(from) !== edition.archive.sha256) throw new Error(`${source} is not ${edition.archive.name}`);
      root = join(work, "extracted");
      mkdirSync(root);
      execFileSync("tar", ["-xf", from, "-C", root]);
    }
    const problem = reason(() => checkTree(root, edition, finder));
    if (problem) throw new Error(problem);
    const staged = join(work, "library");
    copy(root, join(staged, edition.tag));
    const check = checkStaged(staged, edition);
    if (check) throw new Error(check);
    const previous = join(work, "previous");
    const had = kind(to) !== "missing";
    if (had) renameSync(to, previous);
    try {
      renameSync(staged, to);
    } catch (e) {
      if (had) renameSync(previous, to);
      throw e;
    }
  } finally {
    rmSync(work, { recursive: true, force: true });
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const here = fileURLToPath(new URL("..", import.meta.url));
  const edition = JSON.parse(readFileSync(join(here, "library.json"), "utf8"));
  const library = join(here, "src-tauri", "library");
  const source = process.env.CHIRALITY_LIBRARY;
  if (source) stage(source, library, edition);
  const problem = checkStaged(library, edition);
  if (problem) throw new Error(source ? problem : `${problem}; set CHIRALITY_LIBRARY to ${edition.archive.name} or its extracted folder`);
  console.log(`${edition.tag} (${edition.commit}) is in ${relative(here, join(library, edition.tag))}, whole, and nothing else is`);
}
