# Work graph — App v4 first increment: second design pass

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, applied
under [`loop/LOOP_INIT.md`](../../../../loop/LOOP_INIT.md).

- **Stable run identity:** `APP-V4-DESIGN-PASS-2-20260930`. Run records:
  [`AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/).
- **Maintainer:** HELP_HUMAN, this session, under the recorded
  WORKING_ITEMS consultation (as in the three predecessor runs), dispatching
  bounded Type 2 TASK executors directly.
- **Branch:** `claude/chirality-app-v4-60-percent-a41fd5`, at `main`
  `74b3c73134` when the run started.
- **Predecessor:** `APP-V4-SCA002-20260929`, merged in
  [#1061](https://github.com/sgttomas/chirality/pull/1061) at `45ffd91d`.
- **Owner direction (exact):** "Start the next first-increment design pass
  using DAG-003." See [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md)
  for the reading and the standing directions that apply.

## Intent and route

- **Result:** the 14 first-increment deliverables' Design files stand on the
  amended basis and the revised ScopeOfWork contracts, and are developed
  further toward the 60% level (interfaces, states, data, operating
  sequences, failure behaviour, verification). They stay DRAFT, unsupplied and
  unaccepted.
- **Graph basis:** accepted DAG-003 (`_DAG/_LATEST.md`), CURRENT per
  `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218`. Both DAG-003 manifests
  pass at the start of the run (37/37 and 130/130). The 78 held arcs are
  non-gating; they organize co-development and receiver comparisons.
- **Route through DAG-003:** as in the first pass: roots DEL-04-01 and
  DEL-01-01; the SCC-002 members DEL-03-01/02/03, DEL-02-01/03, DEL-04-02/03
  and DEL-05-01/02 co-developed; then DEL-09-09, DEL-09-06 and DEL-03-04 as
  integrating consumers (GUIDE re-pinned last).
- **Not written in this run:** ScopeOfWork.md, registers, `_STATUS.md`,
  `_Decomposition/`, `_ScopeChange/`, `_DAG/` and the basis docs. A finding
  that needs one of them is returned as a proposal for its own route.
- **Excluded:** SWBPIPE construction, host joins (deferred, DECISION-3), the
  relay; the Coverage_Telemetry rebuild; the audit-script fix; product
  implementation beyond a bounded spike that answers a design question;
  qualification, lifecycle CHECKING/ISSUED, SCC closure, a DAG successor.
- **Completion conditions:**
  1. Every Design file is re-pinned to current sources, GUIDE last, with the
     pins verified by script.
  2. Each node below has produced its stated result, reviewed against the
     revised ScopeOfWork.
  3. Receiver comparisons recorded for the joins the pass changes, including
     N-18, N-21, N-24 and X-1.
  4. Owner-level choices found are decided or left open at a stated point of
     need.
  5. DAG-003 currency rechecked at the end; no bound file changed.
  6. Independent review, bounded closeout, receipt, MEMORY rows and the final
     PR merged.

## Work

States: PLANNED, READY, ACTIVE, BLOCKED, UNCERTAIN, COMPLETE.

| ID / outcome | Write scope | Needs | Completion check | State |
|---|---|---|---|---|
| S0 Graph, direction, survey briefs | Run folder; this graph | Owner direction | Committed | COMPLETE |
| S1 Scoping survey (S1-A…S1-F) | `SURVEY/S1-*.md` only | S0 | Six reports: pins, SoW alignment, amended basis, open items by class, 60% depth, joins, carried review items, recommended work; outside neighbours | ACTIVE |
| S2 Route: nodes for the pass, owner questions | This graph; `BRIEFS.md`; `DECISIONS_PENDING.md` if needed | S1 | Each node bounded with a write fence and a check | PLANNED |
| W… Design work | Set by S2 | S2 | Set by S2 | PLANNED |
| V… Reviews, closeout, receipt, final PR | Set by S2 | W… | Per LOOP_INIT §§3–6 | PLANNED |
