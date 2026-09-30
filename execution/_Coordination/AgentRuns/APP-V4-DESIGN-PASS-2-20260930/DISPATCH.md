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
| A3 | Opus 5.5: DECISION-K1 written into 13 files; 37 designed-case results recomputed; ADAPTER and RELAY had no live carrier. Fence and RELAY span verified; committed `ce4088219`. Observations: EXEC CH-20 and WD-EX L-WDEX-7 bind different supports by their own statements (no conflict; no ruling); SP-6F has no declaration element to take it up (Wave B, B1) |
| A1-G | Opus 5.5: GUIDE v0.3 → v0.4, re-pinned last |
