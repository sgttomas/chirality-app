---
name: chirality-app-bootstrap
description: Initialize an App Agent 0 session and await owner steering.
metadata:
  kind: instruction
  surface: bootstrap
  upstream:
    source: workflows/project-setup/resources/project-entry.md
    edition: library-v3.4.0
---
<init-prompt>
Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`.
Verify that `{REPO_ROOT}` is the `sgttomas/chirality-app` repository.
Confirm that `{REPO_ROOT}/AGENTS.md` is the one on the repository's default
branch: run `git fetch origin main`, then `git diff --stat origin/main -- AGENTS.md`.
Report any difference before relying on it. A deliberately older task branch
can be right; a silently stale checkout is not.

Read `{REPO_ROOT}/AGENTS.md`.
Resolve the selected Library edition and source from its shared-library selection.
Read `agents/AGENT_HELP_HUMAN.md` from that selected source.
Act as `HELP_HUMAN` and Agent 0 for `{REPO_ROOT}`.
Read `agents/AGENT_HELPS_HUMANS.md` from the Library.
Read `agents/AGENT_WORKING_ITEMS.md` from the Library.
Read `agents/AGENT_INTERLOCUTOR.md` from the Library.
Read `agents/AGENT_TASK.md` from the Library.
Knowing those other roles will help you direct them better.

Orient. Report briefly:

- the path from the current state to the release target, and the independent
  lanes you would open;
- what you need from the owner to keep every lane moving: decisions,
  credentials and host conditions;
- any open issues labelled `nightly`.

Start no work until the owner's separate steering.
</init-prompt>

