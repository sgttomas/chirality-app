# DAG-002 currency audit — APP_V4_SCA002

**Result: `DEPARTURE`.** 4 arcs added to the accepted DAG-002, 0 removed. All four are held inside the unchanged 13-member SCC-002; no admitted arc changes, no existing arc changes layer or representative. The six SCCs and the 41-node inventory are unchanged. **5 deliverables are `DAG pending`** until the owner accepts the successor DAG-003 or rejects the change at checkpoint C.

- **Audit:** `project-dag` `currency.md`, run `APP-V4-SCA002-20260929`, node D1, 2026-09-29. Snapshot `CURRENCY_APP_V4_SCA002_2026-09-29_2057`; `_Evaluation/DAGCurrency/_LATEST.md` moved here.
- **Basis audited:** commit `8cd783d8d7493fbfe663fb108449e4ceda04a00b`, clean tree. That is after every register-changing brief of SCA-V4-002 returned: the 9 SoW REVISEs with the B-06a reading-rule note (AK2 Part 2) and the `dependency-extract` UPDATE of 11 registers (DX). One audit, as ARC_EFFECT §4 and the owner's accepted order (OWNER_DECISIONS, step 4) foresaw.
- **Exact commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). Outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` is in SPEC §11.2 form: `Latest: DAG-002`, `Basis revision: b585e5ebe…`, `Supersedes: DAG-001`. The registered parser reads it, and this audit resolves DAG-002 from it and its [ACCEPTANCE_RECORD](../../../_DAG/DAG-002/ACCEPTANCE_RECORD.md) (DECISION-10 of the predecessor run; covers project-dag checkpoints 1 and 2). No candidate later than DAG-002 exists other than the DAG-003 folder this run opened, and no `REJECTION_RECORD.md` exists anywhere under `_Candidates/`, so no departure has been rejected before.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-002/` | **37/37 OK**, exit 0. The accepted snapshot is intact |
| `shasum -a 256 -c _DAG/DAG-002/SOURCE_MANIFEST.sha256`, run in the execution root | **98 OK, 32 FAILED**, exit 1. Output kept in `Evidence/source_manifest.stdout.txt` |
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-001/` (superseded) | **61/61 OK**, exit 0. The history is unchanged |

The 32 changed members are the 9 revised `ScopeOfWork.md` (DEL-01-01, 01-04, 02-01, 02-02, 02-03, 03-03, 04-02, 09-07, 10-03), the 11 refreshed `Dependencies.csv` and 11 `_DEPENDENCIES.md` (those nine plus DEL-04-01 and DEL-04-03), and `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`.

**Inventory.** `_LATEST_ACCEPTED.md` changed bytes because SCA-V4-002 appended the B-06a reading-rule note (ASC-ISS-006 option (a), accepted at DECISION-2). It still names `GROUP3-20260928T001055Z`, and the register that snapshot holds, `canonical/Deliverables.csv` (sha256 `bcdf6f2f…15eb`), is unchanged. The inventory recorded in DAG-002's `GRAPH_BASIS.md` is therefore unchanged: **this is evidence drift, not an inventory change or an arc change.** DAG-003's manifest re-binds the changed pointer bytes, so the note falls inside this one departure rather than causing a second (BASIS_AMENDMENT "Timing of B-06a").

## 3. Scratch re-application of DAG-002's rules

Because bytes changed, [Evidence/reapply_selection.py](Evidence/reapply_selection.py) re-applied DAG-002's confirmed SR-1…SR-7 (carried unchanged from DAG-001) to the current registers as a scratch assembly, and compared the result with DAG-002's edge and candidate files. It is not a graph version.

| Comparison | DAG-002 | Current | Change |
|---|---:|---:|---|
| Admitted arcs | 124 | 124 | **0** (same arc set) |
| Candidate arcs (SCC holds) | 74 | 78 | +4 |
| All arcs | 198 | 202 | **+4 added, 0 removed**; no existing arc changes layer; no representative changes |
| SCCs | 6 | 6 | Identical member sets (2/13/2/3/2/2) |
| Nodes | 41 | 41 | Unchanged (GROUP3) |

The registered `audit_dag.py` (sha256 `830d0d53…3449a`) was run on the scratch admissible set: exit 0, 202 edges, 6 SCCs, 0 canonical findings (`Evidence/scratch_admissible_audit.json`). The per-arc list is [Evidence/added_arcs.csv](Evidence/added_arcs.csv); the whole comparison is [Evidence/reapplication_result.json](Evidence/reapplication_result.json).

**The added arcs against what the owner accepted for SCA-V4-002** (OWNER_ITEMS Q-4, DECISION-2; ARC_EFFECT §1). The four are exactly the expected set, one consumer-side UPSTREAM INTERFACE row each, none extra, none missing:

| Arc | Consumer → supplier | Row | Layer | Reverse arc |
|---|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEP-02-01-029 (INITIALIZED / PENDING) | held, SCC-002 | present: DEP-03-02-027 (N-B3) |
| N-21 | DEL-02-03 → DEL-03-02 | DEP-02-03-025 (INITIALIZED / TBD) | held, SCC-002 | none |
| N-24 | DEL-02-03 → DEL-03-03 | DEP-02-03-026 (INITIALIZED / TBD) | held, SCC-002 | present: DEP-03-03-014 (N-27) |
| X-1 | DEL-02-03 → DEL-01-04 | DEP-02-03-027 (INITIALIZED / TBD) | held, SCC-002 | none |

Guards: N-12 and N-B8 are absent; none of the SCC-enlarging arcs E-1…E-5 or reverse citations K-1…K-12 is present; DEL-04-01 keeps 0 suppliers; no SCC-002 member consumes DEL-09-06.

**Analyzer cross-check.** The registered closure analyzer, run without `--output-dir` (`Evidence/analyzer.stdout.json`), reads the §11.2 pointer and reports `accepted_dag`: version DAG-002, result **`DEPARTURE`**, the same 4 added arcs, 0 removed, 5 `DAG pending`. The closure snapshot `CLOSURE_APP_V4_SCA002_2026-09-29_2056` holds the same comparison in `Evidence/dag_pending.csv`. The pointer-form finding of the previous audits is closed.

## 4. Classification

**`DEPARTURE`**: arcs were added. The SCCs and inventory did not change, so no SCC forms, changes or dissolves, and no case opens or closes. Drift alone (§6) would have been `CURRENT_WITH_EVIDENCE_DRIFT`.

## 5. `DAG pending` deliverables (5)

A pending deliverable gets no ready or blocked verdict from dependencies until the owner decides. Unaffected deliverables keep using DAG-002. **The decision awaited for every row is the same:** the owner's checkpoint C decision on successor candidate `_DAG/_Candidates/DAG-003/`, to accept it or reject the change. Either answer clears the flag; a follow-up currency audit then records it.

"→" marks a new input the deliverable consumes; "←" marks a new consumer of the deliverable. All four arcs are in the non-gating candidate layer (C), inside SCC-002 (SCC-CASE-002).

| Deliverable | New inputs it consumes | New consumers of it |
|---|---|---|
| DEL-01-04 | — | X-1 ← DEL-02-03 (C) |
| DEL-02-01 | N-18 → DEL-03-02 (C) | — |
| DEL-02-03 | N-21 → DEL-03-02 (C); N-24 → DEL-03-03 (C); X-1 → DEL-01-04 (C) | — |
| DEL-03-02 | — | N-18 ← DEL-02-01 (C); N-21 ← DEL-02-03 (C) |
| DEL-03-03 | — | N-24 ← DEL-02-03 (C) |

These are the five ARC_EFFECT §4 predicted. **All five are already members of SCC-002**, whose internal arcs are held; the departure adds held arcs only. While pending they get no dependency verdict at all (SPEC §5.4); once decided, their blockers again come from the admitted layer, which the departure does not touch.

**Not pending.** DEL-04-01, DEL-04-02, DEL-04-03, DEL-09-07, DEL-10-03, DEL-01-01 and DEL-02-02 changed bytes without an arc change (§6). They keep using DAG-002.

## 6. Evidence drift alongside the departure

These changes do not alter the arc set, a layer, a representative, an SCC or the inventory. They are read from the live files:

- **Re-quoted evidence.** 34 `EvidenceQuote` cells in DEL-04-01 (9), DEL-04-02 (12) and DEL-04-03 (13) now reproduce the SoW's inline-code backticks exactly (ASC-ISS-008; V12 F1). 15 of them are on DAG-002 representatives; DAG-003 will copy the new bytes. The 34 quotes are exact substrings of their SoWs (DX_SCC-CHECK sweep: 820/820).
- **Rows.** 1 EXTERNAL row retired: DEP-01-04-014 (OI-002 constraint, `source_revised`). 0 rows removed. 16 further rows have SourceRef, Statement, TargetName or Notes edits (DEL-01-01: 2; DEL-01-04: 4; DEL-02-02: 1; DEL-03-03: 1; DEL-04-02: 1; DEL-09-07: 4; DEL-10-03: 1; and DEP-04-02-007, DEP-03-03-008, DEP-01-04-011 on existing arcs). The remaining rows in the 11 refreshed registers changed `LastSeen` only. Of DAG-002's 198 representatives, 60 changed bytes: 40 `LastSeen` only, 15 `EvidenceQuote`, 3 `SourceRef`, 2 `Notes`.
- **Text.** SoW text in 9 deliverables (the SCA-V4-002 MODIFY actions); the B-06a note on `_LATEST_ACCEPTED.md` (§2).
- **Mirrors.** No new mirror comparison: each of the four new arcs has one row. No representative changes.

## 7. Advice: renewed examination (not `DAG pending`)

The four arcs are held inside SCC-002, so they gate nothing and no route through an admitted arc changed. The only deliverables whose routes reach a changed arc are SCC-002 members and their consumers, and the held layer does not feed routes. No renewed examination is called for on account of this departure. The advice list in DAG-002's `HANDOFF_STATE.md` (DEL-09-07, DEL-10-03, DEL-09-02 and others) stands unchanged.

## 8. What follows

A candidate successor is prepared for these decisions only: `_DAG/_Candidates/DAG-003/` (project-dag TRIGGER=SUCCESSOR, CURRENCY_REPORT = this audit). This audit does not edit DAG-001, DAG-002, the pointer, or any local file. It establishes currency only, not satisfaction, readiness or lifecycle.
