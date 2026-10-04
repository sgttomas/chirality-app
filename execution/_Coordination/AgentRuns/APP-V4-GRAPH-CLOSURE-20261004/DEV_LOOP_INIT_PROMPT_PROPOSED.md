# Proposed init/dev-loop-init-prompt.md (draft for HELP_HUMAN)

Drafted by a Type 2 TASK (LI) for HELP_HUMAN, run
`APP-V4-GRAPH-CLOSURE-20261004`. It is a proposal: the live prompt is
unchanged. The proposed text is the block below.

```text
<init-prompt>
Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`.

Set `WORKING_ROOT` to `{REPO_ROOT}/projects/chirality-app-v4`.

Read `{REPO_ROOT}/AGENTS.md`.
Read `{REPO_ROOT}/agents/AGENT_HELP_HUMAN.md`.

Act as `HELP_HUMAN` for `{WORKING_ROOT}`.

Read `{WORKING_ROOT}/loop/LOOP_INIT.md` and follow it.

Steer (this run): <none>
</init-prompt>
```

## What changed, and why

- **Removed:** "Use its Project Management manual and Agent User Manual
  guidance; the Field Book is a summary." The owner's accepted entry reading
  replaces it: the Agent User Manual's headings and the Field Book, which
  LOOP_INIT now states. The removed sentence also tells the agent to treat
  the Field Book as secondary, which no longer fits.
- **Removed:** "within the owner's steering and live authority". The steer
  follows directly. AGENTS.md and the role already bound authority.
- **Kept:** the order. The agent reads AGENTS.md, then the role, then
  LOOP_INIT, then the steer.

## Option: choosing the role

AGENTS.md lets the human "directly select HELP_HUMAN, HELPS_HUMANS, or
WORKING_ITEMS". A development loop for one group may want to start as
WORKING_ITEMS. If so, replace the two role lines with:

```text
Role (this run): HELP_HUMAN
Read `{REPO_ROOT}/agents/AGENT_<Role>.md`.
Act as <Role> for `{WORKING_ROOT}`.
```

This is optional. The draft above keeps the current HELP_HUMAN entry.

## taskmgmt-init-prompt.md

It needs no change from LOOP_INIT's perspective. It is a compatibility
pointer that runs nothing. It sends Task Management to
`chirality-root:bundled:workflow:task-management` under WORKING_ITEMS, which
matches the intake permission in the proposed LOOP_INIT. It also says that
development continues through the development init prompt and
`loop/LOOP_INIT.md`, which is still true.

The Agent User Manual §13 says "No separate Task Management init prompt or
retired role is needed". The file could therefore be retired. That is a
separate housekeeping choice, and it is not needed for LOOP_INIT.
