# Dispatch — APP-V4-DESIGN-PASS-2-20260930

Mechanism: harness-native descendants (Claude Code Agent tool) of the
HELP_HUMAN session, under D-GOV-35. Each executor received its brief by path
([BRIEFS.md](BRIEFS.md)) and the repository at the run's working tree. Host
enforcement of the write fence: none beyond the session's own permissions;
fences are verified afterwards by `git status`.

**Executor model.** S1, A1 and K0 ran on Claude Fable 5.1, the session's
model when they were launched. From 2026-09-30, owner direction: "Ensure you
are using `opus-5.5` models on `high` reasoning for your Type 1 and Type 2
agent instances." From then on every executor is launched with the Agent
tool's `model: opus`, which resolves to `claude-opus-5-5` (confirmed by a
probe executor reporting its own model ID), and runs at the session's effort,
`high` (session record: model `claude-opus-5-5`, effort `high`). The probe
could not see its own effort setting, so `high` rests on the session setting,
not on the executor's report. A user-level agent definition
`~/.claude/agents/type2-opus-high.md` (model `claude-opus-5-5`, effort
`high`) was written; it is not loaded until a new session starts.

| Node | State |
|---|---|
| S0 | Branch fast-forwarded to `main` `74b3c73134` (main had changed only `projects/chirality-piping`). DAG-003 manifests pass: 37/37 and 130/130. Owner direction recorded. Graph and briefs written |
| S1 | Six Type 2 executors launched in parallel (S1-A…S1-F), read-only on project state, one report file each. All six returned; `git status` showed only `SURVEY/` new. Report sha256 prefixes: S1-A `87baa03d`, S1-B `eae76ecf`, S1-C `5b60dd41`, S1-D `a3b0546a`, S1-E `e0e95522`, S1-F `a504772d`. Stale pins: A 32, B 45, C 30, D 26, E 51. Committed `fbebb12a5` |
| S2 | R9 rulings written (R9-1…R9-11). R9-1's requester reading is INTEGRATION and goes to the owner at K1. Route recorded in the graph: Wave A (alignment), owner package, Wave B (design development), closeout |
| A1 | Five Type 2 executors launched in parallel (A1-A…A1-E), fresh contexts, each fenced to its cluster's Design files and one return file. A1-G (GUIDE) follows integration |
| K0 | One Type 2 executor, read-only on project state: `DECISIONS_DRAFT.md`, 27 choices; integrator wrote `DECISIONS_PENDING.md` (six asked, with recommendations) and a review page |
| K1 | Owner: "accept all six as recommended" (DECISION-K1) |
| A1 returns | All five integrated; fences verified; RELAY span unchanged; committed `344d86e3e`. R10 written (R10-1 corrects R9-2). HANDOFF truth fixes by the integrator `dda9380d1` |
| A2 | First launch (Fable 5.1) stopped by the integrator on the owner's model direction; its partial edits to 12 files were saved to the session scratchpad and discarded (`git checkout` of those files only; all earlier work was committed). Relaunched on Opus 5.5 at high effort with the same brief plus a note to leave DECISION-K1 to A3 |
| A2 return | Opus 5.5: R10 applied in 12 files; 3 citation fixes; 3 content mismatches (one dangling ID, passed to A3; two W7 history citations left as history). Fence and RELAY span verified; committed `42456ca08` |
| A3 | Opus 5.5: DECISION-K1 written into 13 files; 39 designed-case results recomputed (A3.md §2 counts 34 rows, five naming two or three cases; the figure 37 given at the time was a miscount, V17-B m-1); ADAPTER and RELAY had no live carrier. Fence and RELAY span verified; committed `ce4088219`. Observations: A3 returned EXEC CH-20 against WD-EX R-9b / L-WDEX-7 as an R10 candidate; the integrator wrongly recorded it here as "no conflict" — CH-20 states no binding of its own (V17-B B-1; repaired under R11-2); SP-6F has no declaration element to take it up (Wave B, B1) |
| A1-G | Opus 5.5: GUIDE v0.3 → v0.4, re-pinned last |
| V17 | Two Opus 5.5 reviewers (V17-A, V17-B), fresh contexts, read-only, on the candidate named at launch |
| V17 return | V17-A HOLD (1 BLOCKING, 1 MAJOR, 3 MINOR, 5 NOTE); V17-B HOLD (1 BLOCKING, 3 MAJOR, 4 MINOR, 5 NOTE). Every finding dispositioned in R11. Records corrected by the integrator (R11-10): A3 count 37 → 39; the A3 row's wrong "no conflict" statement; OWNER_DECISIONS cites the page wording and quotes the executor-model direction |
| A4 | One Opus 5.5 executor applies R11-1…R11-9 and two notes across the 16 Design files |
| A4 return | R11-1…R11-9 and notes N-1, N-2 applied in 16 files; 66 header pins match the final record bytes; GUIDE 18/18; RELAY span unchanged; fence verified. R11-9 returned for B7 (no current-phase case shows the "content no longer current or other kind" negative). Integrator's reading of the two items A4 left: (1) the BRIEFS pins `698d91d8…` (14 files) and `c201c6df…` (GUIDE) sit in each node's input line and equal the brief bytes that node received (BRIEFS at `fbebb12a5`/`3dd7c22c7` and at `c507e809d`), so they are true input records, not stale current-claims; (2) RS R15 and PANEL §3.8 recording "boundary refusals" go beyond V4-HI-70 (destinations contacted) — carried to node B5 with the R11-5 reasoning |
| V17b | One fresh Opus 5.5 reviewer rechecks every V17 finding against R11 and reviews the A4 diff |
| V17b return | MERGE AS DRAFTS (0/0/2/6). Both minors and the notes carried to Wave B (B2, B5, B7, B8); no further edit to the candidate |
| P1 | PR [#1065](https://github.com/sgttomas/chirality/pull/1065) opened after V17b; CI monitor and auto-merge on; merged `292e123d` with CI green. Branch fast-forwarded to it |
| Download | Owner chose Qwen3 4B (2.28 GB). The integrator's download command failed before running (no `timeout` in the shell); nothing was downloaded. A second listing showed chat models already installed since June 2026; the integrator's earlier statement that only an embedding model was present was wrong, and is corrected in OWNER_DECISIONS. OBS-1 will use the installed `Qwen3.5-9B-MLX-4bit` |
| Wave B round 1 | R12 written. Six Opus 5.5 executors launched in parallel (B1, B2, B3, B4, B6, B9), disjoint fences; network only for B9 (the published Chat Completions reference) |
| Round 1 return | B1, B2, B3, B4, B6, B9 returned; fences verified; the integrator reran every prototype (HOSTING 35/35, WD 54/54, EXEC all hold, C 21/21 and schemas, P, ADAPTER mapper on the SH-1 run, ACT, AS, RS, LOOP 19/19, PANEL 4/4): all pass. Committed `5970e0a5b`. Join changes collected for V18 from the six return files |
| Round 2 | B5 and B7 launched (Opus 5.5) |
| OBS-1 | Launched (Opus 5.5) under the B6 brief with the integrator's decisions in BRIEFS (P-5, parts C and D allowed; part B not run; no download; R-1 only) |
| OBS-1 Part B | Owner approved the second turn; relayed to the running OBS-1 executor by message, with the same limits |
| OBS-1 return | One Codex turn (R-1, local qwen3.5-9b, LM Studio 0.4.16): **no tool call** (S-8). Codex sent the MCP tool as a Responses `namespace` tool; LM Studio ignored that type, so the model never saw the tool. Part B not run (the relayed condition). Parts C and D observed. No download; no sign-in. Supplier start-up contacted chatgpt.com (remote control; a 401 plugins request) and github.com (plugin sync) with analytics disabled. Fence verified; committed with this row |
| OBS-1 decision | Owner chose the local command-line turn (OBS-1b); no cloud turn, no sign-in |
| B5 return | Destination flow written once (LOOP §5.3), cited by seven files; 0 one-sided elements by script; MCP 2026-07-28 statelessness evidence rule; prototypes pass. Fence verified (B7 and OBS-1 files excluded from this commit) |
| OBS-1b | Launched (Opus 5.5) |
| B7 return | CA v0.6, XT v0.6: failure rows, current-phase sequence, option sheet (0/10 steps examinable against SWBPIPE now; 9/10 on SH-1), result records, suite order and reopen table. Integrator reran both rehearsals: pass. Fence verified |
| R13 | Rulings on the questions Wave B returned (R13-1…R13-6), including how OBS-1's findings enter the files |
| V18 | Four Opus 5.5 comparators launched in parallel, read-only |
