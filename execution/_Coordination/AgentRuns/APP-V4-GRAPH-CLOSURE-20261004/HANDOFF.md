# Handoff to the first App v4 development session (ephemeral)

This note is for the owner's next session only. It is not a standing record
and is not maintained after use. Durable facts live in the records it points
to.

## Starting the session

Use `projects/chirality-app-v4/init/dev-loop-init-prompt.md`. A suggested
steer:

> Steer (this run): Group A (runtime and contract core) development loop, starting from the walking skeleton in `app/`. First: resolve the nine contract issues in `app/CONTRACT_ISSUES.md` through change control with the affected deliverables' design agents; then fan out within group A. The owner's merge hold of 2026-10-04 still applies unless lifted: commit locally, do not merge.

Change or drop the last sentence once the hold is lifted. Groups B and C can
start their own loops in parallel against group A's agreed contracts.

## Where things are

- **Groups, order, and how to record relationships found later:**
  `AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GROUPS.md`, with GC-7 and GC-8 in
  `GC_RULINGS.md`.
- **Group A's first work items:**
  - the contract issues CI-1…CI-9;
  - the three reading-choice rewordings named in `SURVEY/GROUP_SORT.md`
    (D07, D49, U08);
  - the design-level dependencies that `SURVEY/G2b.md` and `GROUP_SORT.md`
    sorted into each group. Record them in the group's work graph (GC-7).
- **Prior analyses** (inputs, not commitments): the case analyses under
  `_DAG/cases/*/PAIR_ANALYSIS_2026-10-04.md` and `ACT51_ANALYSIS_2026-10-04.md`.
  Their proposed rewordings remain proposals.

## Local environment on this machine (not recorded in the repository)

- **Codex.** Stock Codex 0.158.0 is at
  `~/Library/Caches/chirality-dev/codex/0.158.0/codex`, with sha256
  `788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8`. Set
  `CHIRALITY_CODEX_BIN` and `CHIRALITY_CODEX_EXPECTED_SHA256` as
  `app/README.md` describes.
- **Manual renderer.** Its pinned dependencies are in
  `/tmp/chirality-manual-renderer`, which may not survive a restart.

## Owner decisions the loops will need soon

1. **Dependency downloads.** Real building will need crates and npm packages
   that are not cached. One option is a standing authorisation for packages
   from crates.io and npm into `app/`, recorded in the lockfiles and reviewed
   in the PR. Otherwise each download needs its own yes.
2. **Model turns.** No model provider is available: no local model server is
   running, and sign-in and API keys are "not now" under L-6. Agent-facing
   features need one of these.
3. **Network defaults.** Stock Codex contacts a hosted service at
   `thread/start` unless it is configured otherwise. Decide how the App's
   development defaults and the product's disclosure handle this
   (CONTRACT_ISSUES CI-8).
4. **SWBPIPE host joins.** These are still deferred under DECISION-3, and
   they gate the host-facing parts of groups A and D.
5. **The Codex version.** Move from 0.158.0 to a newer version (0.160.0 has
   been checked) before much code depends on it?
6. **CI for `app/`.** A macOS job with Rust and Tauri needs CI minutes and
   network access.
7. **Review independence for product code.** V4-OPS-34 prefers a Codex
   reviewer when product candidates are examined.
8. **Placement (OI-013/014).** This shapes the internals of group A.
