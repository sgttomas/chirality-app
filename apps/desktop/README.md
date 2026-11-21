# The Chirality App

The plain application on the Chirality engine: projects and their threads on
the left, the conversation in the centre (a composer with attachments, `@`
file references, the workflow picker, model, reasoning and access), the side
panel on the right (the thread's changes as diffs, the workflow in use, a
preview of a changed file), and first use (sign in, add a project folder,
start). Workflows come from the bundled Library edition and the project's own
`.chirality/workflows`.

It is built from the engine's parts (`sgttomas/chirality-engine`): the crate
`chirality-engine-tauri` and the package `@chirality/engine-ui`, both at one
engine revision named in `src-tauri/Cargo.toml` and `package.json` (a test
checks they agree). The engine repository is private: fetching it uses your
own SSH access to GitHub.

## Build

```sh
npm ci
CHIRALITY_LIBRARY=<the extracted library-v3.4.0> npm run library   # once; checked against library.json
npm run typecheck && npm test
(cd src-tauri && cargo test)
npx tauri build --bundles app
```

## Run

The pinned Codex is not bundled; name it, and a Codex home if not your own:

```sh
CHIRALITY_CODEX_BIN=<the pinned codex> CODEX_HOME=<a Codex home> \
  src-tauri/target/release/bundle/macos/Chirality.app/Contents/MacOS/chirality-app
```

`CHIRALITY_WORKFLOW_ROOTS` (`:`-separated) replaces the bundled Library.
`npm run dev` runs the interface in a browser on a scripted engine
(`?scene=firstUse|empty|running|approval|question|diff|fork|home`).

## Moving the engine pin

Change the revision in `src-tauri/Cargo.toml` and `package.json`, then
`npm install` and `cargo update -p chirality-engine-tauri` (in `src-tauri`).
