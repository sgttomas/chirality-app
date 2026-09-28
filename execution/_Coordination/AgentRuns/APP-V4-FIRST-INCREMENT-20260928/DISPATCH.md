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
| V1-A | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-A.md` | RETURNED: 19 agree / 25 disagree (1 BLOCKING) |
| V1-B | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-B.md` | RETURNED: 24 agree / 23 disagree (2 BLOCKING); ran one read-only `git rev-parse` outside brief (no effect) |
| V1-C | general-purpose independent reviewer | BRIEFS V1 | `comparisons/V1-C.md` | RETURNED: 19 agree / 28 disagree (1 BLOCKING) |
| W11 | general-purpose TASK (npm + local codex in scratch, CODEX_HOME scratch) | BRIEFS W11 | DEL-01-01 `Design/PIN_SPIKE_0.158.0.md`, `Design/generated/0.158.0/` | RETURNED. Fence held; the agent ran read-only `git rev-parse`/`status` outside the brief (no effect). The supplier itself fetched `openai/plugins.git` on each fresh CODEX_HOME start, and in one run its git children outlived it; none were running at parent check. The parent re-selected the committed form: TS trees moved to scratch (hashed in the manifest), JSON Schema bundles + manifest + `_spike/` committed. |

## R1 repair (dispatched 2026-09-28)

Integrator resolutions: [R1_RESOLUTIONS.md](R1_RESOLUTIONS.md). Repairs were
sent by `SendMessage` to the **original Wave-1 authors**, resuming them with
their v0.1 context. The same write fences apply. Independence comes from V1 and
the planned IR1 review, not from the repairers.

| Node | Agent (resumed) | Files | State |
|---|---|---|---|
| R1-W1 | W1 author | DEL-04-01 v0.2 | RETURNED v0.2; fence verified |
| R1-W2 | W2 author | DEL-04-03, DEL-04-02 v0.2 | RETURNED v0.2; fence verified |
| R1-W3 | W3 author | DEL-03-01, DEL-03-02 v0.2 | RETURNED v0.2; fence verified |
| R1-W4 | W4 author | DEL-02-01 v0.2 | RETURNED v0.2; fence verified |
| R1-W5 | W5 author | DEL-05-01, DEL-05-02 v0.2 | RETURNED v0.2; fence verified |
| R1-W6 | W6 author | DEL-01-01 v0.2 (with spike findings S-F-01…18) | RETURNED v0.2; fence verified |

R1 returns: every R1 resolution was applied without divergence. The repairers
drew sibling v0.2 elements from R1_RESOLUTIONS and did not read the siblings'
text. Their cross-file findings are collected in [R2_CANDIDATES.md](R2_CANDIDATES.md).
The DEL-04-02/03 repairer's line-count wildcard included DEL-04-01's file
(lines counted, contents not read). The parent corrected one stale row in
PIN_SPIKE_0.158.0.md (DEL-01-01 F-17).

## IR1 (dispatched 2026-09-28; fresh general-purpose reviewers)

| Node | Output | Result |
|---|---|---|
| IR1-A | [reviews/IR1-A.md](reviews/IR1-A.md) | 0 BLOCKING / 8 MAJOR / 13 MINOR; fit to merge as v0.2 drafts; ran read-only git (outside brief, no effect) |
| IR1-B | [reviews/IR1-B.md](reviews/IR1-B.md) | 0 / 10 / 13; fit to merge as drafts; ran read-only git (outside brief, no effect) |
| IR1-C | [reviews/IR1-C.md](reviews/IR1-C.md) | 0 / 5 / 17; fit to merge as drafts; ran read-only git (outside brief, no effect) |

The parent fixed IR1C-04 in the spike evidence ([COMMITTED_STATE.md](../../../PKG-01_Native%20App%20and%20third-party%20harness%20integration/1_Working/DEL-01-01_Stock%20Codex%20hosting%20and%20supplier%20contract/Design/generated/0.158.0/COMMITTED_STATE.md)).
Rulings: [R2_RESOLUTIONS.md](R2_RESOLUTIONS.md). From R2 onward, briefs permit
read-only git, because the absolute ban was repeatedly and harmlessly breached.

## R2 alignment (dispatched 2026-09-28; original authors resumed)

| Node | Files | State |
|---|---|---|
| R2-W1 | DEL-04-01 v0.3 | RETURNED v0.3 |
| R2-W2 | DEL-04-03, DEL-04-02 v0.3 | RETURNED v0.3; fence verified |
| R2-W3 | DEL-03-01, DEL-03-02 v0.3 | RETURNED v0.3; fence verified |
| R2-W4 | DEL-02-01 v0.3 | RETURNED v0.3; fence verified |
| R2-W5 | DEL-05-01, DEL-05-02 v0.3 | RETURNED v0.3; fence verified |
| R2-W6 | DEL-01-01 v0.3 | RETURNED v0.3; fence verified |

R2 returns: all rulings applied. The aligners read sibling v0.2 text from
`28bd00499` via `git show`, as directed. The parent's grep sweep for superseded
terms found only change-log or negation mentions.

## R3 micro-edits ([R3_RESOLUTIONS.md](R3_RESOLUTIONS.md)), dispatched and returned 2026-09-28

The authors of DEL-02-01, DEL-04-01, DEL-05-01/02 and DEL-03-01 made in-place
edits without a version bump and reported no new findings.

## V2 and Wave 2 start (dispatched 2026-09-28)

| Node | Type | Scope | State |
|---|---|---|---|
| V2 | general-purpose independent reviewer | Bounded consistency check of v0.3 at `ba0b37123` → `reviews/V2.md` | RETURNED: MERGE AS v0.3 DRAFTS; 0 BLOCKING / 1 MAJOR / 13 MINOR |
| W7 | general-purpose TASK | DEL-02-03 `Design/` (inputs pinned at `ba0b37123`) | ACTIVE |
| W8 | general-purpose TASK (read-only `gh pr view 885` permitted) | DEL-03-03 `Design/` | ACTIVE |

Wave-2 files are kept out of PR #1039, which carries Wave 1 only.
