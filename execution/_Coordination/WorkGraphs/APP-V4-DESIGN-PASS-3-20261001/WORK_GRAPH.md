# Work graph — App v4 standalone App deliverables: design pass 3

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, applied
under [`loop/LOOP_INIT.md`](../../../../loop/LOOP_INIT.md).

- **Stable run identity:** `APP-V4-DESIGN-PASS-3-20261001`. Run records:
  [`AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`](../../AgentRuns/APP-V4-DESIGN-PASS-3-20261001/).
- **Maintainer:** HELP_HUMAN, this session, under the recorded WORKING_ITEMS
  consultation, dispatching bounded Type 2 executors (Claude Opus 5.5, high
  effort).
- **Branch:** `claude/chirality-app-v4-60-percent-a41fd5`, at `main`
  `a38617d08b` when the run started.
- **Predecessor:** `APP-V4-DESIGN-PASS-2-20260930`, closed by
  [#1069](https://github.com/sgttomas/chirality/pull/1069) at `a38617d0`.
- **Owner direction (exact):** "Proceed as recommended." See
  [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md).

## Intent and route

- **Result:** the six standalone-App deliverables (DEL-01-02, 01-03, 01-04,
  01-05, 02-02, 02-04) gain first Design files at the 60% level described in
  LOOP_INIT, joined to the first increment's Design files; the owner choices
  that shape them are decided first; the contract changes of this and the
  previous pass are carried by one amendment.
- **Graph basis:** DAG-003, current at the start (the second pass's D0).
- **Not written by executors:** ScopeOfWork, registers, `_STATUS.md`,
  decomposition, scope-change, DAG, basis files (the amendment node changes
  them through `scope-change`, with the owner's checkpoints).
- **Excluded:** SWBPIPE work and host joins; the other 21 deliverables
  without design; implementation beyond local prototypes; qualification.

## Work

| ID / outcome | Write scope | Needs | Completion check | State |
|---|---|---|---|---|
| S0 Graph, direction, survey briefs | Run folder; this graph | Owner direction | Committed | COMPLETE |
| S1 Scoping survey (S1-A, S1-B, S1-C) | `SURVEY/S1-*.md` | S0 | Obligations, joins, collected proposals, owner choices, what exists, design scope | COMPLETE (this commit) — 161 obligations across six deliverables; owner choices merged into K |
| K Decision sitting: the choices that shape this pass, with recommendations | `DECISIONS_PENDING.md`; review page; `OWNER_DECISIONS.md` | S1 | Decided, or left open at a stated point of need | COMPLETE — DECISION-K3 as revised: eleven as recommended, K-7 the owner's alternative |
| R17 Rulings for the D nodes | `R17_RESOLUTIONS.md` | K | Every K answer and Part 2 matter placed | COMPLETE |
| D1…D6 Design per deliverable (round 1) | Each deliverable's new `Design/` folder; `D/<ID>.md` | R17 | R17-1; return file with join list | COMPLETE (round 1) |
| OBS-2 Local observations at 0.158.0 (K-11) | Scratch; `DEL-01-01/Design/OBS_2_0.158.0.md`, `prototype/obs2/`; `D/OBS-2.md` | R17 | R17-16 items recorded | COMPLETE (with the S-9 deviation recorded in DISPATCH) |
| F0 Join consolidation | `F/F0_JOINS.md` | D1…D6, OBS-2 | Per-file join table, conflicts, rows | COMPLETE |
| R18 + L Rulings on the conflicts; second owner package (L-1…L-7) | `R18_RESOLUTIONS.md`; `DECISIONS_PENDING_2.md`; review page | F0 | Decided, or left open at a stated point | ACTIVE — waiting on the owner |
| F First-increment edits from the join lists (R17-14), then D round 2 (OBS-2 cells) | First-increment Design files named in the join lists | D1…D6, OBS-2 | One version step per file | PLANNED |
| A SCA-V4-003: apply the contract proposals of passes 2 and 3 | `scope-change` route | Placement decided after K | Owner checkpoints; DAG currency | PLANNED |
| V… Comparisons, reviews, closeout, receipt, final PR | Per LOOP_INIT §§3–6 | D… | — | PLANNED |
