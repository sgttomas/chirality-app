# Work graph — App v4 graph closure toward 60%

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, under
`loop/LOOP_INIT.md`.
- **Coordination:** `bundled:chirality-root/coordinated-knowledge-work`
  (WORKFLOW.md sha256 `44049bcd…1b18`).
- **Graph work:** `project-dag`, `scc-resolution-case`, `dependency-extract`,
  `audit-dep-closure` and `scope-change`, under
  `docs/CYCLE_DRIVEN_RESOLUTION.md`.

- **Run:** `APP-V4-GRAPH-CLOSURE-20261004`; records in
  [`AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/`](../../AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/).
- **Maintainer:** HELP_HUMAN, coordinating directly. A WORKING_ITEMS instance
  is introduced only if integration starts displacing owner-facing work.
- **Owner direction (exact):** see OWNER_DECISIONS.md, which holds the 60%
  criterion and "Good. And consider the `coordinated-knowledge-work`
  workflow…".
- **Graph basis:** DAG-004 (accepted 2026-10-03; current, 128/130 with
  recorded DEL-01-03 drift).

## Coordination (coordinated-knowledge-work)

**Consumer and usable result.** The owner judges 60%: "the DAG won't change
and all SCCs have been resolved, so that work can proceed enmass in
parallel". Then implementers build in parallel. The usable result is an
accepted DAG-005 that has:
- no unresolved SCC;
- registers current with the Design files;
- admitted edges whose interfaces say the same thing on both sides;
- write boundaries mapped to the person or an agent.

**Closure conditions.** These are the only gates (§6):
1. the objective and edge semantics are confirmed by the owner;
2. the registers are current with the designs;
3. every SCC is resolved by a named move (decompose, invert, merge or cut),
   with each cut or merge ruled by the owner;
4. every open structural matter is either shown not to change an arc, or is
   settled;
5. admitted-edge interfaces agree;
6. DAG-005 is assembled, audited strict, independently reviewed and
   accepted.

Design gaps that change no edge are 60%→90% work and are not gates.

**Shared premise checked first.** The objective and edge semantics are the
consequential shared basis, because every case's move depends on them
(§1, §5). DAG-004's semantics are part-level: "before the stated part of its
work. Not whole-deliverable completion." The proposal to the owner comes
with a small set of worked edge classifications that every case agent must
apply the same way. RV3 checks them against the sources before they reach
the owner.

**Early path.** CASE-002 (13 members) goes all the way through first:
- survey;
- updated registers for its members;
- a named move for each cycle-closing edge;
- the owner's ruling for any cut or merge;
- a closure rerun showing the component gone.

If CASE-002 needs a decomposition change, that changes everything else, so
the other five cases wait for it. The registers survey and the structural
matter check are independent and continue in parallel.

**Owners.**
- The standing design agents (O-A…O-F) keep their deliverables' registers
  and edges. Deliverables with no standing agent go to one extraction agent
  per brief, as `dependency-extract` requires.
- One graph agent runs the project-dag mechanics through assembly.
- RV2 and RV3 continue as reviewers. A fresh reviewer independently reviews
  the graph version (project-dag step 6).
- The ready-work limit is one waiting unit per agent.

**Cheap checks where defects enter.**
- `dag_reach.py` when a row is proposed.
- `dependency-extract`'s validators when a register changes.
- `audit-dep-closure` after the evidence is frozen.
- `audit_dag.py --canonical --strict` at assembly.

Reuse these; build no new tooling unless a named obstruction needs it.

**Reporting.** Usable results and material gaps.

## Nodes

| ID / outcome | Write scope | Needs | Check | State |
|---|---|---|---|---|
| G0 Direction, graph | Run folder; this graph | Owner direction | Committed | COMPLETE |
| G1 Objective survey: DAG-004 objective and semantics, every SCC's cycle-closing edges by kind, candidate move per edge | `SURVEY/G1.md` | G0 | RV3 on the classifications | ACTIVE |
| G2 Register currency survey: interfaces in Design files missing from, or contradicting, the registers | `SURVEY/G2.md` | G0 | Counts sampled by HELP_HUMAN | ACTIVE |
| G3 Checkpoint 1 (basis): objective, semantics, worked classifications | Owner-facing packet | G1, RV3 | Owner | PENDING |
| G4 Early path: CASE-002 | Case home; members' registers by owner | G2, G3 | Closure rerun; RV | PENDING |
| G5 Other five cases | Case homes | G4 pattern | Closure rerun; RV | PENDING |
| G6 Structural matters' effect on arcs | `SURVEY/G6.md` | G1 | RV | PENDING |
| G7 Admitted-edge interface agreement; role mapping | Owners' Design files | G4/G5 edges | RV | PENDING |
| G8 Register amendment and DAG-005 assembly, audit, independent review | scope-change; `_DAG/` candidate | G4–G7 | Strict audit; fresh reviewer | PENDING |
| G9 Checkpoint 2: DAG-005 acceptance (the 60% judgment) | — | G8 | Owner | PENDING |

## Redirection to build (owner, 2026-10-04)

The owner wrote: "We're not trying to play games here, we're trying to build software." They then approved: "Yes you can take this approach and monitor its effectiveness in actually delivering the required content."

The node states below are revised accordingly. G4–G9 stop where they stand, and their findings remain as records:
- G1, G2 and G2b;
- the seven case analyses;
- rulings GC-1…GC-6.

The contract core is treated as one merged unit under change control. Its contracts are frozen, and any change is named, reviewed and propagated.

**Usable result now.** Running App v4 code for one thin path, built against the frozen contracts:
1. a Tauri 2 shell whose Rust main process hosts the stock Codex App Server;
2. a person's decision on a decision package, through the App act control (A16);
3. the RS record written and validated against `RS_RECORD.schema.json`;
4. the decision shown in the decision view.

**Effectiveness measures** (reported at each return; supporting work is reported separately from delivery):
- steps of the path that run as code with automated tests, out of 4;
- elapsed time from dispatch to the first runnable end-to-end path;
- contract issues found by implementation, logged in `app/CONTRACT_ISSUES.md` with file and section, and their disposition;
- share of the return that is code and tests versus records.

| ID / outcome | Write scope | Needs | Check | State |
|---|---|---|---|---|
| B0 Merge page: the core's member list under the build objective, and the remaining small cuts (one page, for the record) | Run folder | G2b, RVG-G2b | RVG | PENDING |
| B1 Walking skeleton, steps 1–4 | `projects/chirality-app-v4/app/` | Frozen contracts; local Codex 0.158.0; offline build caches | Automated tests; code review | ACTIVE |
| B2 Contract issues from B1 through change control | Owners' Design files, by change | B1 | RV | PENDING |
| B3 Fan-out plan along the contract boundaries | Work graph | B1 working | — | PENDING |
