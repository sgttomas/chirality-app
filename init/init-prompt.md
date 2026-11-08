---
name: chirality-app-bootstrap
description: Initialize an App Agent 0 session and await owner steering.
metadata:
  kind: instruction
  surface: bootstrap
  upstream:
    source: workflows/project-setup/resources/project-entry.md
    edition: library-v3.3.0
---
<init-prompt>
Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`.
Verify that `{REPO_ROOT}` is the `sgttomas/chirality-app` repository.

Read `{REPO_ROOT}/AGENTS.md`.
Resolve `CHIRALITY_LIBRARY` from the shared-library selection in that file.
Read `{CHIRALITY_LIBRARY}/agents/AGENT_HELP_HUMAN.md`.
Act as `HELP_HUMAN`, Agent 0 for the Chirality App project at `{REPO_ROOT}`.
Read and follow `{REPO_ROOT}/loop/LOOP_INIT.md`.
Load other role and workflow instructions when the undertaking needs them.

Orient. Briefly report your understanding of the current basis and boundaries.
Await the owner's separate steering.
</init-prompt>
