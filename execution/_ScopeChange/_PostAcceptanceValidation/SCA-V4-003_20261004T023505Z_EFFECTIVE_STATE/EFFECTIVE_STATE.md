# SCA-V4-003 — effective state

Record written: 20261004T023505Z, by HELP_HUMAN, at HEAD 90d3a5b6a7655e4b4829dd53b265c1b8c6e45181, after the owner accepted
DAG-004 (DECISION-3 of run APP-V4-SCA003-20261002) and after the closure audit
`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/`
(CLOSED_WITH_OBSERVATIONS; its ASC-ISS-001 asks for this record).
Append-only: it edits no SCA-V4-003 group-bound byte, moves no pointer and
accepts nothing.

Since group-3 acceptance (DECISION-2):
- The 19 ScopeOfWork REVISEs: done (run records `RV/RA.md`, `RV/RB.md`;
  validators 19/19; VERIFY PASS; NO_STATUS_TOUCH).
- The register UPDATE: done for the 20 registers (`DX/`), 212 arcs, six
  SCCs unchanged; five expected mirror rows not extracted (no arc effect;
  carried by DECISION-3).
- DAG-004: accepted (DECISION-3) and published; follow-up currency CURRENT;
  after the DEL-01-03 TargetLocation repair (`DX/FX.md`),
  CURRENT_WITH_EVIDENCE_DRIFT, 0 pending.
- Still open:
  - the Design re-pins of the 23 Design files that pin a pre-REVISE
    ScopeOfWork hash (the next design touch);
  - the Coverage_Telemetry.json rebuild (owner-deferred under
    APP-V4-BASIS-ALIGN-20260928 DECISION-8);
  - DEL-09-02 (outside this amendment) still reads OI-009 as open in its
    ScopeOfWork TBD-002 and register row DEP-09-02-027 (closure audit
    ASC-ISS-002); its ScopeOfWork can change only by a later amendment;
    HELP_HUMAN proposes carrying the item to the next one (a proposal put to
    the owner, not an owner decision; review V26 m-1). The authoritative status reads
    through `Open_Issues.csv` and the active supersession map.

Closure verdict of the amendment record: OPEN_PENDING_DERIVATIVE_CLOSURE, for
the Design re-pins and Coverage_Telemetry.json.
