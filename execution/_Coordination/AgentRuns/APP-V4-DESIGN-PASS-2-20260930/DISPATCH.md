# Dispatch — APP-V4-DESIGN-PASS-2-20260930

Mechanism: harness-native descendants (Claude Code Agent tool) of the
HELP_HUMAN session, under D-GOV-35. Each executor received its brief by path
([BRIEFS.md](BRIEFS.md)) and the repository at the run's working tree. Host
enforcement of the write fence: none beyond the session's own permissions;
fences are verified afterwards by `git status`.

| Node | State |
|---|---|
| S0 | Branch fast-forwarded to `main` `74b3c73134` (main had changed only `projects/chirality-piping`). DAG-003 manifests pass: 37/37 and 130/130. Owner direction recorded. Graph and briefs written |
| S1 | Six Type 2 executors launched in parallel (S1-A…S1-F), read-only on project state, one report file each. All six returned; `git status` showed only `SURVEY/` new. Report sha256 prefixes: S1-A `87baa03d`, S1-B `eae76ecf`, S1-C `5b60dd41`, S1-D `a3b0546a`, S1-E `e0e95522`, S1-F `a504772d`. Stale pins: A 32, B 45, C 30, D 26, E 51. Committed `fbebb12a5` |
| S2 | R9 rulings written (R9-1…R9-11). R9-1's requester reading is INTEGRATION and goes to the owner at K1. Route recorded in the graph: Wave A (alignment), owner package, Wave B (design development), closeout |
| A1 | Five Type 2 executors launched in parallel (A1-A…A1-E), fresh contexts, each fenced to its cluster's Design files and one return file. A1-G (GUIDE) follows integration |
| K0 | One Type 2 executor, read-only on project state: `DECISIONS_DRAFT.md`, 27 choices; integrator wrote `DECISIONS_PENDING.md` (six asked, with recommendations) and a review page |
| K1 | Owner: "accept all six as recommended" (DECISION-K1) |
| A1 returns | All five integrated; fences verified; RELAY span unchanged; committed `344d86e3e`. R10 written (R10-1 corrects R9-2). HANDOFF truth fixes by the integrator `dda9380d1` |
| A2 | One Type 2: apply R10 and check sibling citations across the 15 files |
