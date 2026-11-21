# Chirality App

The Chirality App: the place to use the Chirality Library's workflows with an
agent, through a plain interface for workflows. It is being rebuilt on the
Chirality engine (`sgttomas/chirality-engine`), which supplies the agent,
conversations, workflows and the person's part in them through one typed Rust
API.

## What this repository holds

- **The Chirality App**, rebuilt on the engine, at `apps/desktop`: the
  standard layout built from the engine's adapter and interface parts. See
  [its README](apps/desktop/README.md).
- **App v3.0.1**, the released app, at the tag `v3.0.1`. Its design language
  (layout, type, colour, spacing, the feel of the navigator and conversation)
  carries forward.
- **App v4**, retired as a product and kept for reference at the tags
  `app-v4/reference-main` and `app-v4/reference-interface`. What it learned
  about Codex is recorded in the engine's `SPEC.md`; most of the rest is what
  not to do. Its code and governance documents are still on `main` until the
  rebuild replaces them.

## Related repositories

| Repository | What it is |
| --- | --- |
| `sgttomas/chirality-engine` | The engine every Chirality application builds on |
| `sgttomas/chirality-library` | The workflows and roles the app offers |
| `sgttomas/epc-project-init` | An application for FEED estimates and schedules, built on the engine |
