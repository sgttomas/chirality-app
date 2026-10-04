# Receipt — APP-V4-SCA003-20261002 (SCA-V4-003)

The third App v4 amendment. It wrote into the Scopes of Work what design
passes 2 and 3 found and what the owner decided along the way, and moved the
accepted graph from DAG-003 to DAG-004.
Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-SCA003-20261002/WORK_GRAPH.md).

## Owner acts

All are recorded with the owner's exact text in
[OWNER_DECISIONS.md](OWNER_DECISIONS.md):

- **Direction to prepare:** "Proceed as recommended." and "yes, run the
  closeout." (run APP-V4-DESIGN-PASS-3-20261001).
- **DECISION-1 (groups 1 and 2):** "accept the remaining items as
  recommended". This covered Q-1…Q-17, including Q-13, which moved the six
  standalone-App deliverables to IN_PROGRESS as a separate act.
- **DECISION-2 (group 3):** "I accept the audited result."
- **DECISION-3 (DAG-004):** "I accept DAG-004."

## What landed

- **Ledger and decisions:** a ledger of 216 proposals (191 INCLUDE, 10
  DEFER, 15 DROP) and the 17 owner items.
- **Scopes of Work:** 19 revised by 147 accepted blocks.
  - DEL-01-04 gains the App act control (OUT-005, REQ-008, AC-008, VER-008).
  - DEL-01-05 gains the start-up traffic requirement (REQ-010, AC-011,
    VER-011).
  - DEL-04-01 gains TBD-005.
- **Open_Issues:** OI-009 `RESOLVED_BY_OWNER_DECISION` (supersession row
  D-021); OI-018 gains a pointer.
- **Registers:** 20 refreshed (103 rows added, 63 updated, 1 retired).
  - 10 new arcs: 5 admitted, 5 held in SCC-002.
  - 202 → 212 arcs; the six SCCs are unchanged.
- **DAG-004:** published as the accepted graph (41 nodes; 129 admitted, 83
  held, 355 excluded). Currency CURRENT, then CURRENT_WITH_EVIDENCE_DRIFT
  after the DEL-01-03 TargetLocation repair.
- **Lifecycle:** DEL-01-02, 01-03, 01-04, 01-05, 02-02 and 02-04 moved from
  INITIALIZED to IN_PROGRESS.

## Checks

- **Pre-change baseline:** 0 / 35 / 93.
- **Post-change audit:** 0 / 52 / 77. Of the 17 more WARNINGs, 16 come from
  the Q-13 act and one (COV-129) cleared at acceptance.
- **Post-acceptance validation:** PASS 39/39.
- **Independent reviews:**
  - V23 returned HOLD; after repair RP1, the recheck V23b returned READY FOR
    CHECKPOINT.
  - V24 returned READY FOR GROUP 3 after M-1.
  - V25 returned READY FOR CHECKPOINT C, with an independent placement check
    of 567/567 rows.
- **Final review:** V26 MERGE.
- **Closure audit:** CLOSED_WITH_OBSERVATIONS (0 CRITICAL, 0 MAJOR, 2 MINOR,
  8 OBSERVATION).
- **Write fences:** recorded in DISPATCH for P3, P1 and AK1; review V26
  checked every commit's writes against its stage's area.

## Limits and carried obligations

- **Amendment record:** `OPEN_PENDING_DERIVATIVE_CLOSURE`, for the Design
  re-pins (23 Design files pin pre-REVISE ScopeOfWork hashes) and
  `Coverage_Telemetry.json` (owner-deferred).
- **Held for later owner decisions:**
  - Q-7 (S-01-4);
  - Q-9 (the four A12-mapping rows);
  - Q-14 (R-02-4);
  - three basis items.
- **For a later amendment or the register owners:**
  - DEL-09-02 still reads OI-009 as open (closure audit ASC-ISS-002;
    HELP_HUMAN proposes carrying it to the next amendment, for the owner);
  - five mirror rows were not extracted;
  - V25 m-1 (DEL-05-01 → DEL-01-05 is represented by an information-only
    row);
  - three mirror maturity differences;
  - the CASE-002 evidence update (`scc-resolution-case`).
- **Elsewhere:**
  - absolute home paths in run notes, tool outputs and prose (a separate
    task was suggested);
  - the Root `AGENTS.md` instruction notices (their own scope);
  - the Codex version-advance check (needs the owner's yes and a download).
- No Design file was changed by this run. Nothing is implemented or
  qualified.
