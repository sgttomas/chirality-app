# The Chirality App

The plain application on the Chirality engine: projects and their threads on
the left, the conversation in the centre (a composer with attachments, `@`
file references, the workflow picker, model, reasoning and access), the side
panel on the right (the thread's changes as diffs, the workflow in use, a
preview of a changed file), and first use (sign in, add a project folder,
start). Workflows come from the bundled Library edition and the project's own
`.chirality/workflows`. The app bundles the edition `library.json` names, whole
as released (its source archive extracted: the workflows, the tools and files
they run, its licence), and no other; the engine is given its `workflows`.
`npm run library` stages it from the archive or its extracted folder, as real
files (refusing links), and checks every file against `library.json`'s digest
of the whole tree before swapping it in. The fonts' licence (SIL OFL, with the
IBM Plex copyright notices) is bundled under `licenses/`.

The app bundles the Codex `codex.json` names (0.171.0, OpenAI's release
package for Apple Silicon), whole with its layout, notices and licences, and
runs its `bin/codex`. `npm run codex` stages it from the archive or its
extracted folder, checking the archive's size and digest, the package's version
and target, every file against `codex.json`'s digest, and OpenAI's signature.
A build for any other target is refused. Codex's licence and notice (from its
source at `rust-v0.171.0`) are bundled under `licenses/codex/`.

It is built from the engine's parts (`sgttomas/chirality-engine`): the crate
`chirality-engine-tauri` and the package `@chirality/engine-ui`, both at one
engine revision named in `src-tauri/Cargo.toml` and `package.json` (a test
checks they agree). Both are fetched from GitHub over https.

Development builds are `Chirality Dev`, version `4.0.0-dev`, with the bundle
identifier `com.chirality.app.dev`, apart from an installed Chirality's name,
preferences, data and grants. The release name and identifier are chosen at
release.

## Build

```sh
npm ci
CHIRALITY_LIBRARY=<chirality-library-3.4.0-source.tar, or its extracted folder> npm run library   # once
CHIRALITY_CODEX=<codex-package-aarch64-apple-darwin.tar.gz, or its extracted folder> npm run codex   # once
npm run typecheck && npm test
(cd src-tauri && cargo test)
npx tauri build --bundles app
npm run check-bundle   # the built bundle's Library, a workflow step run from it, its Codex and that version, the fonts' licence
```

## Run

Open the built app; it runs its bundled Codex with your Codex home, or
`CODEX_HOME`:

```sh
CODEX_HOME=<a Codex home> \
  "src-tauri/target/release/bundle/macos/Chirality Dev.app/Contents/MacOS/chirality-app"
```

`CHIRALITY_CODEX_BIN` runs another Codex instead.
`CHIRALITY_WORKFLOW_ROOTS` (`:`-separated) replaces the bundled Library.
`npm run dev` runs the interface in a browser on a scripted engine
(`?scene=firstUse|empty|running|approval|question|diff|fork|home`).

## Moving the engine pin

Change the revision in `src-tauri/Cargo.toml` and `package.json`, then
`npm install` and `cargo update -p chirality-engine-tauri` (in `src-tauri`).
npm writes the engine's `resolved` line in `package-lock.json` as `git+ssh`; put it
back to `git+https` (the pin test fails until it is).
