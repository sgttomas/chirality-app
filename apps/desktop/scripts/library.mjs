// Puts the Library edition the app bundles (library.json) among its resources, whole, as released:
// src-tauri/library/<tag> holds the edition's source archive extracted (its workflows, the tools and
// files they run, its licence), with edition-relative paths kept. From that archive, or a folder it
// was extracted to:
//   CHIRALITY_LIBRARY=<chirality-library-…-source.tar, or its extracted folder> npm run library
// The archive is checked against library.json's archive digest, and every file of the edition against
// library.json's digest of the whole tree (each file's bytes, and whether it is executable), before
// staging and again after; links and empty folders are refused. It is staged beside the resources and
// swapped in only once checked, so a failure leaves them as they were, and what an interrupted
// staging had set aside is put back. With no source given, it checks what is staged.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, realpathSync, renameSync, rmSync, statSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";
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

/** Every file under `dir`, relative to it; a link, an empty folder or anything else not a file or
 * folder is refused. `skip` names entries left out (the source's Finder files). */
export function files(dir, skip = () => false) {
  const names = readdirSync(dir).filter((name) => !skip(name));
  if (!names.length) throw new Error(`${dir} is an empty folder`);
  const odd = names.find((name) => name.includes("\n"));
  if (odd) throw new Error(`${join(dir, odd)} has a line break in its name`);
  return names.flatMap((name) => {
    const path = join(dir, name);
    const k = kind(path);
    if (k === "folder") return files(path, skip).map((f) => join(name, f));
    if (k === "file") return [name];
    throw new Error(`${path} is ${k}`);
  });
}

const executable = (path) => (lstatSync(path).mode & 0o111) !== 0;

/** sha256 of the sorted "<sha256>  <x or ->  <path>" lines of every file under `dir`: x for an
 * executable file. */
export function digest(dir, skip) {
  const lines = files(dir, skip).map((f) => `${sha256(join(dir, f))}  ${executable(join(dir, f)) ? "x" : "-"}  ${f}`).sort();
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

/** What the file system says `path` (or, where it does not exist, the nearest folder above it) and
 * every folder above it are: the same folder under another spelling is the same one. */
function lineage(path) {
  const stat = statSync(path, { bigint: true, throwIfNoEntry: false });
  const parent = dirname(path);
  return [...(stat ? [`${stat.dev}:${stat.ino}`] : []), ...(parent === path ? [] : lineage(parent))];
}

/** Whether `path`, which exists, is `folder` or inside it. */
const within = (path, folder) => existsSync(folder) && lineage(path).includes(lineage(folder)[0]);

/** `path` with its nearest existing folder's real path. */
function real(path) {
  const parent = dirname(path);
  if (existsSync(path)) return realpathSync(path);
  return parent === path ? path : join(real(parent), basename(path));
}

/** The prefix of the folders staging `to` works in, beside it: `.library-staging-` for `library`. */
const staging = (to) => `.${basename(to)}-staging-`;

/** Puts back what an interrupted staging had set aside, when nothing is staged. Only a staging
 * folder that is a real folder holding what staging makes, and not holding `source`, is touched. */
export function recover(library, source) {
  const to = resolve(library);
  if (kind(to) !== "missing" || kind(dirname(to)) !== "folder") return;
  for (const name of readdirSync(dirname(to)).filter((n) => n.startsWith(staging(to)))) {
    const work = join(dirname(to), name);
    const previous = join(work, "previous");
    if (kind(work) !== "folder" || kind(previous) !== "folder") continue;
    if (readdirSync(work).some((n) => !["previous", "library", "extracted"].includes(n))) continue;
    if (source && existsSync(source) && within(realpathSync(source), work)) continue;
    renameSync(previous, to);
    rmSync(work, { recursive: true, force: true });
    return;
  }
}

/** Stages `source` (`edition`'s source archive, or a folder it was extracted to) as the whole of
 * `library`. Nothing is removed until the staged copy is checked; a source that is a link, or that
 * overlaps `library`, is refused first. The archive is checked against `edition.archive`'s sha256
 * (and its size, where it names one); `inspect`, given the extracted folder, says why it is not the
 * edition before its digest is checked, if it can. */
export function stage(source, library, edition, inspect = () => null) {
  // As named, without a trailing separator or dot that would name something else.
  if (kind(resolve(source)) === "a link") throw new Error(`${source} is a link`);
  const from = realpathSync(source);
  const named = resolve(library);
  const to = join(real(dirname(named)), basename(named));
  // `from` in what would be replaced (as named, or where a link there leads), or holding it.
  const overlaps = within(from, to) || [to, ...(existsSync(to) ? [realpathSync(to)] : [])].some((t) => lineage(t).includes(lineage(from)[0]));
  if (overlaps) throw new Error(`${source} overlaps ${library}: stage from an archive or extraction outside it`);
  mkdirSync(dirname(to), { recursive: true });
  const work = mkdtempSync(join(dirname(to), staging(to)));
  try {
    let root = from;
    if (kind(from) === "file") {
      const size = edition.archive.size;
      if ((size !== undefined && statSync(from).size !== size) || sha256(from) !== edition.archive.sha256) throw new Error(`${source} is not ${edition.archive.name}`);
      root = join(work, "extracted");
      mkdirSync(root);
      execFileSync("tar", ["-xf", from, "-C", root]);
    }
    const problem = reason(() => inspect(root) ?? checkTree(root, edition, finder));
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
  recover(library, source);
  if (source) stage(source, library, edition);
  const problem = checkStaged(library, edition);
  if (problem) throw new Error(source ? problem : `${problem}; set CHIRALITY_LIBRARY to ${edition.archive.name} or its extracted folder`);
  console.log(`${edition.tag} (${edition.commit}) is in ${relative(here, join(library, edition.tag))}, whole, and nothing else is`);
}
