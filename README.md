# Chirality App

The Chirality App: the place to use the Chirality Library's workflows with an
agent, through a plain interface for workflows. It is being rebuilt on the
Chirality engine (`sgttomas/chirality-engine`), which supplies the agent,
conversations, workflows and the person's part in them through one typed Rust
API. The rebuilt app is what will be published as Chirality App v4.

## What this repository holds

- **The Chirality App**, rebuilt on the engine, at `apps/desktop`: the
  standard layout built from the engine's adapter and interface parts, to be
  published as v4 (now `4.0.0-dev`). It bundles the pinned Codex, so the
  built app needs no `CHIRALITY_CODEX_BIN`. See [its README](apps/desktop/README.md).
- **App v3.0.1**, the released app, at the tag `v3.0.1`. Its design language
  (layout, type, colour, spacing, the feel of the navigator and conversation)
  carries forward.
- **An earlier, unreleased attempt at v4**, kept for reference at the
  `app-v4/*` tags (`app-v4/reference-main`, `app-v4/reference-interface`).
  What it learned about Codex is recorded in the engine's `SPEC.md`; most of
  the rest is what not to do. Its code and governance documents are no longer
  on `main`.

## Related repositories

| Repository | What it is |
| --- | --- |
| `sgttomas/chirality-engine` | The engine every Chirality application builds on |
| `sgttomas/chirality-library` | The workflows and roles the app offers |
| `sgttomas/epc-project-init` | An application for FEED estimates and schedules, built on the engine |
