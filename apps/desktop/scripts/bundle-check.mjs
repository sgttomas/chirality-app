// Checks a built app (by default this checkout's macOS bundle): its Library is the pinned edition,
// whole, and nothing else; a step the edition's workflows run outside workflows/ runs from it
// (estimate-snapshot's enum check of BASIS_OF_ESTIMATE); and the fonts' licence is among its resources.
//   npm run check-bundle [-- <path to the .app>]
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { lstatSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { checkStaged } from "./library.mjs";

const here = fileURLToPath(new URL("..", import.meta.url));
const edition = JSON.parse(readFileSync(join(here, "library.json"), "utf8"));
const { productName } = JSON.parse(readFileSync(join(here, "src-tauri", "tauri.conf.json"), "utf8"));
const app = process.argv[2] ?? join(here, "src-tauri", "target", "release", "bundle", "macos", `${productName}.app`);
const resources = join(app, "Contents", "Resources");
const sha256 = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");

const problems = [];
const library = checkStaged(join(resources, "library"), edition);
if (library) problems.push(library);

// Nothing of a Library that is not the pinned edition is run.
if (!library) {
  const step = (value) =>
    spawnSync("python3", ["tools/validation/validate_enum.py", "BASIS_OF_ESTIMATE", value], { cwd: join(resources, "library", edition.tag), encoding: "utf8" });
  const quote = step("QUOTE");
  if (quote.status !== 0) problems.push(`estimate-snapshot's step zero failed for QUOTE: ${quote.error?.message ?? (quote.stderr || quote.stdout).trim()}`);
  if (step("GUESS").status === 0) problems.push("estimate-snapshot's step zero accepted GUESS");
}

const licence = join(resources, "licenses", "LICENSE-IBM-Plex-OFL.txt");
const shipped = join(here, "node_modules", "@chirality", "engine-ui", "src", "fonts", "LICENSE-IBM-Plex-OFL.txt");
const real = (path) => lstatSync(path, { throwIfNoEntry: false });
if (!real(join(resources, "licenses"))?.isDirectory() || !real(licence)?.isFile()) problems.push(`${licence} is missing or not a file`);
else if (sha256(licence) !== sha256(shipped)) problems.push(`${licence} is not the engine package's fonts licence`);

if (problems.length) {
  console.error(problems.join("\n"));
  process.exit(1);
}
console.log(`${app}: ${edition.tag} whole (${edition.files} files), its enum step runs from it, and the fonts' licence is in it`);
