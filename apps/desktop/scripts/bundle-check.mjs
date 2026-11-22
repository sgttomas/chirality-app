// Checks a built app (by default this checkout's macOS bundle): its Library is the pinned edition,
// whole, and nothing else; a step the edition's workflows run outside workflows/ runs from it
// (estimate-snapshot's enum check of BASIS_OF_ESTIMATE); its Codex is the pinned package, whole with
// its notices and licences, signed by its team, and reports the pinned version (run with a scratch
// CODEX_HOME); and the fonts' licence is among its resources.
//   npm run check-bundle [-- <path to the .app>]
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { lstatSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { checkCodex } from "./codex.mjs";
import { checkStaged } from "./library.mjs";

const here = fileURLToPath(new URL("..", import.meta.url));
const edition = JSON.parse(readFileSync(join(here, "library.json"), "utf8"));
const pin = JSON.parse(readFileSync(join(here, "codex.json"), "utf8"));
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

const codex = checkCodex(join(resources, "codex"), pin);
if (codex) problems.push(codex);

// Nothing of a Codex that is not the pinned package is run, and never with the person's own Codex home.
if (!codex) {
  const home = mkdtempSync(join(tmpdir(), "chirality-bundle-check-codex-home-"));
  try {
    const run = spawnSync(join(resources, "codex", pin.tag, pin.entrypoint), ["--version"], { env: { ...process.env, CODEX_HOME: home }, encoding: "utf8", timeout: 60_000 });
    const said = (run.stdout ?? "").trim();
    if (run.status !== 0 || said !== `codex-cli ${pin.version}`) problems.push(`the bundled codex --version said ${JSON.stringify(said || run.error?.message || run.stderr)}, not codex-cli ${pin.version}`);
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
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
console.log(
  `${app}: ${edition.tag} whole (${edition.files} files), its enum step runs from it; Codex ${pin.version} whole (${pin.files} files, with its notices), signed by ${pin.team}, and reports that version; and the fonts' licence is in it`,
);
