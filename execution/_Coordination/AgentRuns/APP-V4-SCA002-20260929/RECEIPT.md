# Receipt — APP-V4-SCA002-20260929

This run closed SCA-V4-001's audit, then ran the follow-on amendment
SCA-V4-002 through acceptance, propagation, DAG-003 and its own closure audit.
Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-SCA002-20260929/WORK_GRAPH.md).

## Owner acts

All in [OWNER_DECISIONS.md](OWNER_DECISIONS.md), with exact text.

| Decision | What the owner decided |
|---|---|
| Start | "Proposal accepted.  Proceed accordingly." (closure audit first, in parallel with the packet) |
| DECISION-2 | Checkpoint A: SCA-V4-002 groups 1–2, "accept the remaining items as recommended" (all four arcs kept; OI-001/002 kept OPEN; ASC-ISS-001 option (a); the record fixes) |
| DECISION-3 | Checkpoint B: group 3 accepted |
| DECISION-4 | Checkpoint C: DAG-003 accepted |

## What landed

- **SCA-V4-001 closure audit:** first OPEN (ASC-ISS-001 provisional
  CRITICAL), then, after SCA-V4-002, a superseding snapshot
  **CLOSED_WITH_OBSERVATIONS** (0 CRITICAL/MAJOR/MINOR).
- **SCA-V4-002 accepted** (snapshot `_ScopeChange/SCA-V4-002_2026-09-29_1901/`,
  now `_ScopeChange/_LATEST.md` in SPEC §11.2 form): the HOST_INTEGRATION line
  break; the DEL-04-01 qualifier and mirror; the OI-012 pointer; the
  reading-rule notes; the 18-row supersession delta that answers ASC-ISS-001;
  the SCA-V4-001 effective-state record. Post-acceptance validation 47/47.
- **9 ScopeOfWork contracts revised** (DEL-10-03, 02-01, 02-03, 09-07, 01-04,
  02-02, 03-03, 04-02, 01-01) by REVISE and VERIFY, NO_STATUS_TOUCH.
- **11 dependency registers refreshed:** the four arcs N-18, N-21, N-24 and
  X-1 produced; 34 quotes restored with backticks; DEP-09-07-016 restated.
- **DAG-003 accepted and published.** 41 nodes, 124 admitted (unchanged from
  DAG-002) and 78 held arcs; six SCCs unchanged; strict audit exit 0;
  follow-up currency CURRENT, 0 pending. DAG-002 and DAG-001 kept as history.
- **SCA-V4-002 closure audit:** CLOSED_WITH_OBSERVATIONS (1 MINOR, answered by
  the SCA-V4-002 effective-state record).
- **SETUP_LOG:** INCREMENTAL SCA-V4-002 COMPLETE.

## Checks

- Pre- and post-change audit-decomp on seven packages, every difference
  attributed.
- Independent reviews: V14 (before group 3) and V15 (propagation and
  DAG-003), both READY; V16 covers publication and records.
- Manifests: DAG-001 61/61, DAG-002 37/37, DAG-003 37/37 and its source
  manifest 130/130.

## Open

- **Owner-deferred:** the Coverage_Telemetry.json rebuild (then an audit-decomp
  rerun); the 17 Design files' re-pin to the amended basis texts, GUIDE last.
- **With the next SWBPIPE relay:** the handoff's "local-first" line; the
  DECISION-5 host obligations.
- **Tooling:** the inherited audit-decomp script misreads the §11.2
  accepted-predecessor line; carried as (f)/(g) until the base is fixed.
- **Next:** hand DAG-003 to `construct-local-work-graph` for the next
  first-increment design work; that pass also does the Design re-pins.
