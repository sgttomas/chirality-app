# Dispatch record — APP-V4-FIRST-INCREMENT-20260928

Parent: HELP_HUMAN, Claude Code session (model `claude-opus-5-5`), worktree
`.claude/worktrees/test-ci-optimization-f6cacd`, branch
`claude/chirality-app-v4-60-percent-a41fd5`, base `6e18505e3`.
Mechanism: Claude Code `Agent` tool, background subagents; `Explore` (read-only)
for recovery research, `general-purpose` for TASK drafting. Subagents share the
parent's worktree; write fences are brief-enforced (instruction), not
host-enforced. Parent verifies changed paths against fences on return.
Selected methods: `chirality-root:bundled:workflow:construct-local-work-graph`
(Root `workflows/construct-local-work-graph/WORKFLOW.md` at `6e18505e3`).

## Recovery research (read-only, 2026-09-28)

| Node | Type | Supplied basis | Result |
|---|---|---|---|
| R-A App-side SoW summary (DEL-01-01…05, 02-04) | Explore | Launch prompt only | Returned; no writes |
| R-B Workflow/record/policy SoW summary (DEL-04-01…03, 02-01…03) | Explore | Launch prompt only | Returned; no writes |
| R-C Host-contract SoW summary (DEL-03-01…04, 05-01/02, 09-06, 09-09; HI; CASE-002 Open_Questions) | Explore | Launch prompt only | Returned; no writes |

## Wave 1 (dispatched 2026-09-28)

| Node | Type | Brief | Write fence | State |
|---|---|---|---|---|
| W1 | general-purpose TASK | [BRIEFS.md](BRIEFS.md) Common + W1 | DEL-04-01 `Design/` | ACTIVE |
| W2 | general-purpose TASK | Common + W2 | DEL-04-03, DEL-04-02 `Design/` | ACTIVE |
| W3 | general-purpose TASK | Common + W3 | DEL-03-01, DEL-03-02 `Design/` | ACTIVE |
| W4 | general-purpose TASK | Common + W4 | DEL-02-01 `Design/` | ACTIVE |
| W5 | general-purpose TASK | Common + W5 | DEL-05-01, DEL-05-02 `Design/` | ACTIVE |
| W6 | general-purpose TASK | Common + W6 | DEL-01-01 `Design/` | ACTIVE |
