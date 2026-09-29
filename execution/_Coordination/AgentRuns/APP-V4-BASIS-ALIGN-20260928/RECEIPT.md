# Receipt — APP-V4-BASIS-ALIGN-20260928

This run aligned App v4's accepted basis with the owner's decisions
(DECISION-1…5), and with the first increment's closeout proposals. Graph:
[WORK_GRAPH.md](../../WorkGraphs/APP-V4-BASIS-ALIGN-20260928/WORK_GRAPH.md).

## Owner acts

All are in [OWNER_DECISIONS.md](OWNER_DECISIONS.md) with exact text:

| Decision | What the owner decided |
|---|---|
| Start | "go ahead with the next undertaking as recommended." |
| DECISION-6 | 14 deliverables recorded IN_PROGRESS; the 41-arc set; X-1 kept |
| DECISION-7 | Checkpoint A: scope-change groups 1–2 for SCA-V4-001, "accept the remaining items as recommended", after reviewing the packet on a review page |
| DECISION-8 | Checkpoint B: group 3 accepted; Coverage_Telemetry left stale for later; follow-on SCA-V4-002 |
| DECISION-9 | Incremental setup plan confirmed |
| DECISION-10 | Checkpoint C: DAG-002 accepted; four unproduced arcs routed to SCA-V4-002 (option A), which widens its scope |

## What landed

- **SCA-V4-001**, the first App v4 amendment. It is accepted, snapshot
  `_ScopeChange/SCA-V4-001_2026-09-28_2155/`.
  - Basis docs updated: PRD, ARCHITECTURE, HOST_INTEGRATION, EXAMINATION.
    - V4-WF-05 is phased to the governance layer.
    - V4-HOST-01 and V4-ARC-11 give model options, OAuth or API key, with no
      default.
    - V4-HOST-02 takes the owner's DECISION-5 text.
    - V4-HI-70 records host-agent destinations.
    - "Local-first" is amended.
  - The decomposition rows, a Decision Log heading and the stale-sentence fix.
  - Post-acceptance validation passed 43/43.
- **16 ScopeOfWork contracts revised** by `scope-of-work` REVISE and VERIFY:
  the 14 first-increment deliverables plus DEL-09-07 and DEL-08-01.
  All 74 first-closeout corrections are carried: 45 kept, 29 refreshed.
- **18 dependency registers refreshed** by `dependency-extract` UPDATE, from
  ScopeOfWork.md only, with the SCC guards held.
- **DAG-002 accepted and published.** `_DAG/_LATEST.md` points to it.
  - It has 41 nodes, 124 admitted and 74 held arcs, and 6 SCCs unchanged.
  - The follow-up currency audit is CURRENT, with nothing DAG pending.
  - DAG-001 is kept as history.
- **Lifecycle:** 14 deliverables are IN_PROGRESS.
- **SETUP_LOG:** INCREMENTAL SCA-V4-001 COMPLETE.

## Checks

- **Pre- and post-change audit-decomp,** on the same seven-package scope:
  every difference is attributed.
- **Independent reviews:**
  - V11, before group 3: READY;
  - V12, of the SoW revisions, registers and DAG-002: READY;
  - V13, of publication and records: see `reviews/`.
- **Strict audit:** `audit_dag.py --canonical --strict` exits 0.
- **Manifests:** DAG-001 61/61; DAG-002 37/37 and its source manifest 130/130.

## Open

- **SCA-V4-002**, scope per DECISION-8 and DECISION-10:
  - DEL-10-03 "local-first";
  - "consumes" sentences for N-18, N-21, N-24 and X-1;
  - the DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012;
  - Open_Issues OI-001/002 status;
  - the DEL-03-03 CLM-002 tail;
  - the A17b line join.
- **Coverage_Telemetry.json** needs a rebuild. SCA-V4-001's closure verdict is
  OPEN_PENDING_DERIVATIVE_CLOSURE for that derivative only.
- **`audit-scope-closure`** is proposed against SCA-V4-001.
- **V12 F1:** 34 dependency quotes lost their backticks; fix at the next
  extraction.
- **Design files** re-pin to the amended basis texts at the next design pass.
- **Routing:** hand DAG-002 to `construct-local-work-graph` for the next
  first-increment work.
