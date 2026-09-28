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
| W7 | general-purpose TASK | DEL-02-03 `Design/` (inputs pinned at `ba0b37123`) | RETURNED v0.1 (934 lines); fence verified |
| W8 | general-purpose TASK (read-only `gh pr view 885` permitted) | DEL-03-03 `Design/` | RETURNED v0.1 (944 lines); fence verified |

Wave-2 files are kept out of PR #1039, which carries Wave 1 only.

PR #1039 merged 2026-09-28 as merge commit `98b1723b1b263cf3672db5fbb83b9e670773edc2` (head `1c36b6d97`).

| W9 | general-purpose TASK | DEL-09-06, DEL-09-09 `Design/` (3 files) | RETURNED (461/796/391 lines); fence verified |

Owner decision 2 was recorded after an interrupted session turn (auto-mode classifier outages). The owner then directed "continue, defer SWBPIPE until final review".

## A1 sweep and W10 (dispatched 2026-09-28)

Rulings: [R4_RESOLUTIONS.md](R4_RESOLUTIONS.md) (`f05c7e4cd`). The original
authors were resumed; siblings read at `f05c7e4cd`.

| Node | Files | State |
|---|---|---|
| A1-W1 | DEL-04-01 → v0.4 | RETURNED; fence verified |
| A1-W2 | DEL-04-03, DEL-04-02 → v0.4 | RETURNED; fence verified |
| A1-W3 | DEL-03-01, DEL-03-02 → v0.4 | RETURNED; fence verified |
| A1-W4 | DEL-02-01 → v0.4 | RETURNED; fence verified |
| A1-W5 | DEL-05-01, DEL-05-02 → v0.4 | RETURNED; fence verified |
| A1-W6 | DEL-01-01 → v0.4 | RETURNED; fence verified |
| A1-W7 | DEL-02-03 → v0.2 | RETURNED; fence verified |
| A1-W8 | DEL-03-03 → v0.2 | RETURNED; fence verified |
| W10 | DEL-03-04 GUIDE-v0.1 (new general-purpose TASK; inputs at `f05c7e4cd` + R4) | RETURNED (575 lines); CC-5 gap G-3 relayed to W9 author |
| A1-W9 | DEL-09-06/09-09 W9 files → v0.2 (DECISION-2, R4, G-3 addendum) | RETURNED; fence verified (`9fc77baa3`) |

Scratchpad note: W10 found a shared scratchpad folder overwritten by a concurrent agent. It re-extracted its pinned inputs and verified their hashes. Later briefs use per-agent scratch folders.

## V3, R5, V4 and C1 (2026-09-28)

| Node | Result |
|---|---|
| V3-A / V3-B | Both MERGE AS DRAFTS: 0 BLOCKING, 10 MAJOR, 26 MINOR ([V3-A](reviews/V3-A.md), [V3-B](reviews/V3-B.md)) |
| R5 pass (9 authors resumed) | Wave-1 files → v0.5; EXEC, ADAPTER and W9 files → v0.3; all fences verified. Integrator pass-through rulings: HP-4 and person-directed turns; multi-checkpoint precedence; App-only HS-5; SQ-02-status mapping. `d3cebd1cc` |
| CA/RELAY E1 correction | E1 via the external channel is unsupported (EXEC MT-2). `816c917f0` |
| GUIDE v0.2 | CC-1…CC-11 pass. `c7f5513db` |
| V4-A / V4-B | Independent review of the final candidate `c7f5513db`: ACTIVE |
| C1-A / C1-B / C1-C | Bounded closeout comparisons, proposing edits only: ACTIVE |

Agents after W10 used private scratch folders.

## V5 and R7 (2026-09-28)

| Node | Result |
|---|---|
| V4-A / V4-B | MERGE AS DRAFTS: 0 BLOCKING, 5 MAJOR, 23 MINOR. R6 applied: `375c3970c`, `2f42fba02` |
| C1-A / C1-B / C1-C | RETURNED; proposals only. Combined in `closeout/CLOSEOUT_ACCOUNT.md` |
| V5 | Bounded check of R6 at `2f42fba02`: MERGE AS DRAFTS, 0 BLOCKING, 3 MAJOR, 8 MINOR ([V5](reviews/V5.md)) |
| R7 repair | One Type 2 applied [R7](R7_RESOLUTIONS.md) in place to 12 Design files (HOSTING, P, LOOP, PANEL and SPIKE untouched), with GUIDE re-pinned last. RETURNED; fence verified |
| R7 integrator close | Confirmed the repairer's reading of R7-3: an A5 checkpoint's derived held actions (the governed operations) take precedence over the kind (b)/(c) default, as in EXEC §3.6. Qualified PANEL §3.2 (model-supplied, R6-5) and ACT FX-39 (re-hold, R6-3), replaced RELAY's "uncommitted at repair" placeholders, and re-pinned GUIDE for PANEL, ACT and RELAY. All 16 GUIDE pins match the working tree; both DAG-001 manifests pass |
| V6 | Bounded check of R7 at `c6f81a4f2`: MERGE AS DRAFTS, 0 BLOCKING, 0 MAJOR, 7 MINOR ([V6](reviews/V6.md)); fence verified |
| PR-3 | [#1043](https://github.com/sgttomas/chirality/pull/1043) at `c6f81a4f2`. The first CI run failed on "Update the PR base" (the coverage planner requires `main` to be integrated), so `origin/main` was merged into the branch. `main` changed no App v4 file |
| PR-3 merge | [#1043](https://github.com/sgttomas/chirality/pull/1043) merged `df6d59e3` (CI 9 pass, 4 skipped). The first merge attempt was refused by the session's permission classifier. The owner then restated standing permission to merge once CI is green, and the merge proceeded |
| F1 | Final PR [#1045](https://github.com/sgttomas/chirality/pull/1045): closeout account, receipt, 14 MEMORY rows, handoff pointer, graph. V7 at `fc35e2811`: DO NOT MERGE (B-1: wrong list of arcs not proposed for SCC reasons). B-1, M-1 and m-1…m-4 fixed; bounded recheck V7b |
| F1 merge | [#1045](https://github.com/sgttomas/chirality/pull/1045) merged `65e2d6c2` (V7b MERGE; CI 9 pass / 4 skipped), at the owner's direction "CI is green. Merge while we wait for the SWBPIPE response." |
| Relay | Owner (chat, 2026-09-28): "I've sent the questions to the SWBPIPE session and that agent is working on answering." Recorded in the RELAY §4 ledger and the handoff, with GUIDE re-pinned. Follow-up PR |
