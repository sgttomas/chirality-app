---
name: chirality-app-standing-instructions
description: How to work in the Chirality App, rebuilt on the Chirality engine.
metadata:
  kind: instruction
  surface: standing
---
# Working in chirality-app

This repository is the Chirality App, being rebuilt on the Chirality engine
(`sgttomas/chirality-engine`). Read `README.md`, then the engine's `SPEC.md`
and `AGENTS.md`: the engine is the agent; this app is a plain interface for
using workflows with it.

The v4 code and its governance documents (`execution/`, `docs/`, `tools/`,
the release target) are retired. They do not govern new work. Read them as
reference only: what v4 learned about Codex is in the engine's `SPEC.md`, and
most of the rest is what not to do (the engine's Non-goals list it).

## How to work

- Use the engine only through its API; what the app needs that the engine
  does not offer goes to the engine.
- T3 Code is the pattern for the agent interface; Chirality 3.0.1 (tag
  `v3.0.1`) for the design language only.
- Keep modules small and single-purpose (about 600 lines at most), types at
  every boundary, and tests on data the engine produced.
- Interface text: say what the person needs, once. No explanatory text,
  warnings or disclosures they did not ask for. No reviews of wording.

## Boundaries

- Development and tests use a scratch Codex home, never `~/.codex`.
- No agent signs in, enters or reads a credential. Live model turns need the
  owner's own sign-in.
- Ordinary packages from npm and crates.io may be added and are pinned in the
  lockfiles. Any other download (a binary, an archive) needs the owner's yes,
  naming the file, source and size.
- Do not commit secrets, Codex homes, session records or downloaded binaries.
- Preserve existing release tags.

## Git

Branch from `main` with a prefix naming the author (`claude/`, `codex/`).
Merge through a pull request once its checks pass and any review it needs is
done. No force pushes or history rewrites.
