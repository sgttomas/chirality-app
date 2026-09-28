# Work graph — App v4: SWBPIPE answer intake

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, applied
under [`loop/LOOP_INIT.md`](../../../../loop/LOOP_INIT.md).

- **Maintainer:** HELP_HUMAN (this Claude Code session). It dispatches bounded
  Type 2 TASK executors directly.
- **Predecessor:** [APP-V4-FIRST-INCREMENT-20260928](../APP-V4-FIRST-INCREMENT-20260928/WORK_GRAPH.md),
  closed at `65e2d6c2`, with its relay record at `d1cc97ce`.

## Intent and selected route

- **Run identity:** `APP-V4-SWBPIPE-INTAKE-20260928`. Run records are in
  [`AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/`](../../AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/).
- **Owner decision:** [DECISION-3](../../AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md):
  "yes, do 1 and 2, and defer the host joins".
- **Input:** the SWBPIPE answers `RELAY_ANSWERS_SWBPIPE.md` (sha256
  `64ea4e596b314cc1db93915bb3292415c7f017caa62613ec610233c3328c0689`).
  - Source: SWBPIPE records branch `codex/piping-numerical-integrity-20260926`
    at `7092582d8`.
  - Its fact sheet is `FACTS_SQ01_SQ32.md`, sha256 `2f61d3ba…ddfc`.
  - Both hashes match SWBPIPE's `SHA256SUMS`.
  - A byte-identical copy sits beside the questions in DEL-09-06 `Design/`.
- **Completion conditions:**
  1. The answers are recorded as received in the RELAY §4 ledger.
  2. Every answer is traced to its dependent definitions (an intake map).
  3. R8 rulings settle the SQ-02 and SQ-28 consequences and each of the 12
     contradicted assumptions. Owner-level items are brought to the owner.
  4. The affected Design files are revised in place, or by version where
     meaning changes, and the GUIDE is re-pinned.
  5. An independent review returns no BLOCKING items. PRs merge under standing
     authority. Receipt and MEMORY rows are written.
- **Excluded:**
  - all SWBPIPE work and decisions;
  - host joins (DECISION-3);
  - ScopeOfWork, register, lifecycle and DAG-bound files (C1 proposals carry
    over to the successor route);
  - new App-side features beyond what an answer forces.

## Work

States: PLANNED, READY, ACTIVE, BLOCKED, UNCERTAIN, COMPLETE.

| ID / outcome | Write scope | Needs | Completion check | State / result |
|---|---|---|---|---|
| I0 Graph, decision, briefs | This folder; run folder | DECISION-3 | Committed | COMPLETE |
| I1 Receipt record | RELAY §4 ledger; GUIDE RELAY pin; answers copy | I0 | Ledger names source, revision, date, custody and hashes; no value change; GUIDE pins match | COMPLETE — RELAY `dfb62587…` re-pinned; handoff status updated |
| I2 Intake map | Run folder `INTAKE_MAP.md` only (read-only on Design) | I1 | Every SQ answer → dependent file/section → effect class (value change / assumption contradicted / confirms / no effect); the 12 §3 items each mapped; proposed edits per file; rulings needed | COMPLETE (against `64ea4e59…`; delta check pending): 221 rows (V 86, A 71, C 27, N 37) |
| I3 R8 intake rulings | Run folder `R8_RESOLUTIONS.md` | I2 | Each ruling-needed item decided or routed to the owner | BLOCKED — owner discussion (DECISION-4) |
| I4 Apply | Affected Design files (parallel by file cluster) | I3 | Every R8 item applied; change rows; GUIDE re-pinned last | PLANNED |
| V9 Independent review | `reviews/V9.md` | I4 | Verdict covering the actual candidate | PLANNED |
| F Receipt, MEMORY, PR | Run folder; affected `MEMORY.md` | V9 | PR merged | PLANNED |

## Current state and recovery

- Branch: `claude/chirality-app-v4-60-percent-a41fd5` (worktree
  `.claude/worktrees/test-ci-optimization-f6cacd`), synced to main at
  `d1cc97ce`.
- SWBPIPE delivered the answers into DEL-09-06 `Design/` in #1047 (`41aeb2a02`):
  `RELAY_ANSWERS_SWBPIPE.md` sha256 `6f01add3…` and `FACTS_SQ01_SQ32.md`
  `733fb88a…`. These supersede the recorder's earlier copy (`64ea4e59…`). The
  RELAY ledger and GUIDE pin cite the delivered version.
- **I2 basis delta:** INTAKE_MAP was built against the earlier copy. A delta
  check against `6f01add3…` is needed before R8.
- **Held for owner discussion:** DECISION-4 (D6 direction; loop paradigm;
  residency). R8 is not written until they are clarified.
- **#1046 merge note:** #1046 was merged while one check (App Runtime
  integration) was still pending. The recorder's command did not stop on it,
  and GitHub accepted the merge. Its result is recorded in DISPATCH.
