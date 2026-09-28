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
| W1 | general-purpose TASK | [BRIEFS.md](BRIEFS.md) Common + W1 | DEL-04-01 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |
| W2 | general-purpose TASK | Common + W2 | DEL-04-03, DEL-04-02 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |
| W3 | general-purpose TASK | Common + W3 | DEL-03-01, DEL-03-02 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |
| W4 | general-purpose TASK | Common + W4 | DEL-02-01 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |
| W5 | general-purpose TASK | Common + W5 | DEL-05-01, DEL-05-02 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |
| W6 | general-purpose TASK | Common + W6 | DEL-01-01 `Design/` | RETURNED 2026-09-28; fence verified (only its `Design/`) |

Wave-1 returns (v0.1 files, line counts as returned): W1 ACT_AND_POLICY_CONTRACT.md 532;
W2 RECORD_SEMANTICS.md 329, AUTONOMY_AND_STANDING_EXCHANGE.md 252; W3
CATALOG_AND_READ_BASIS.md 423, PROPOSAL_LIFECYCLE_AND_OUTCOMES.md 447; W4
WORKFLOW_DECLARATION.md 577, EXAMPLES.md 259; W5 LOOP_RECEIVING_CONTRACT.md 548,
PANEL_RECEIVING_CONTRACT.md 300; W6 HOSTING_BOUNDARY.md 663. The parent checked
`git status`: only the nine `Design/` folders were new. The executors'
findings are carried into V1 and R1 through their Design files' findings
sections.

## Owner decision

[OWNER_DECISIONS.md](OWNER_DECISIONS.md): D1–D4 answered (recommended options).

## V1 and W11 (dispatched 2026-09-28)

| Node | Type | Brief | Write fence | State |
|---|---|---|---|---|
| V1-A | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-A.md` | ACTIVE |
| V1-B | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-B.md` | ACTIVE |
| V1-C | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-C.md` | ACTIVE |
| W11 | general-purpose TASK (npm + local codex in scratch, CODEX_HOME scratch) | BRIEFS W11 | DEL-01-01 `Design/PIN_SPIKE_0.158.0.md`, `Design/generated/0.158.0/` | ACTIVE |
