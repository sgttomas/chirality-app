# Public session init prompt

This public export does not include the private project loop entrypoints. Start
from the target workspace and select an Agent 0 or Agent 1 role from
`AGENTS.md`.

<init-prompt>
Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`.

Read `{REPO_ROOT}/AGENTS.md`, then read the selected instruction package under
`{REPO_ROOT}/agents/`.

State the target workspace, objective, accepted basis, authority, read scope,
write scope, tools, expected return, and human decision points before acting.
</init-prompt>
