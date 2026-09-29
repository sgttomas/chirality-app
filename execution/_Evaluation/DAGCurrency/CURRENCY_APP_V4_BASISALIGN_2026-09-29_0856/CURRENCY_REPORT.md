# DAG-001 currency audit — APP_V4_BASISALIGN

**Result: `DEPARTURE`.** 37 arcs added to the accepted DAG-001, 0 removed. The six SCCs and the 41-node inventory are unchanged. **15 deliverables are `DAG pending`** until the owner accepts the successor DAG-002 or rejects the change at checkpoint C.

- **Audit:** `project-dag` `currency.md`, run `APP-V4-BASIS-ALIGN-20260928`, node D1, 2026-09-29. Snapshot `CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`; `_Evaluation/DAGCurrency/_LATEST.md` moved here.
- **Basis audited:** commit `b585e5ebead38f8ece442c80cd3bec5be8363cf3`, clean tree. That is after every register-changing brief of the undertaking returned: the 16 SoW revisions (RV-1…RV-4) and the dependency-extract UPDATE of 18 registers (DX-1/2/3). One audit, as SUCCESSOR_PLAN §1 advised.
- **Exact commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). Outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` names DAG-001 in prose, with a link to [DAG-001/ACCEPTANCE_RECORD.md](../../../_DAG/DAG-001/ACCEPTANCE_RECORD.md). It has no SPEC §11.2 `Latest:` line, so the registered closure analyzer reports its accepted-DAG comparison as `INCOMPLETE` (`_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`). This audit resolves DAG-001 from the prose pointer and its acceptance record, and does not rely on the analyzer's pointer read. The pointer form is a checkpoint C item (C2-6). No candidate is open other than DAG-001's historical folder, and no `REJECTION_RECORD.md` exists, so no departure has been rejected before.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-001/` | **61/61 OK**, exit 0. The accepted snapshot is intact |
| `shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`, run in the execution root | **78 OK, 52 FAILED**, exit 1. Output kept in `Evidence/source_manifest.stdout.txt` |

The 52 changed members are 16 `ScopeOfWork.md` (the SCA-V4-001 revisions), 18 `Dependencies.csv` and 18 `_DEPENDENCIES.md` (the DX registers). The 7 decomposition and coordination members are unchanged. The accepted decomposition pointer still names `GROUP3-20260928T001055Z`, the inventory recorded in DAG-001's `GRAPH_BASIS.md`.

## 3. Scratch re-application of DAG-001's rules

Because bytes changed, [Evidence/reapply_selection.py](Evidence/reapply_selection.py) re-applied DAG-001's confirmed SR-1…SR-7 to the current registers as a scratch assembly, and compared the result with DAG-001's edge and candidate files. It is not a graph version.

| Comparison | DAG-001 | Current | Change |
|---|---:|---:|---|
| Admitted arcs | 109 | 124 | +15 |
| Candidate arcs (SCC holds) | 52 | 74 | +22 |
| All arcs | 161 | 198 | **+37 added, 0 removed**; no existing arc changes layer |
| SCCs | 6 | 6 | Identical member sets (2/13/2/3/2/2) |
| Nodes | 41 | 41 | Unchanged (GROUP3) |

The registered `audit_dag.py` (sha256 `830d0d53…3449a`) was run on the scratch admissible set: exit 0, 198 edges, 6 SCCs, 0 canonical findings (`Evidence/scratch_admissible_audit.json`). The per-arc list is [Evidence/added_arcs.csv](Evidence/added_arcs.csv); the whole comparison is [Evidence/reapplication_result.json](Evidence/reapplication_result.json).

**The added arcs against what the owner accepted at checkpoint A (DECISION-6).** The 37 are exactly the refreshed 41 less four that no register row carries:

| Arc | Consumer → supplier | Why absent |
|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEL-02-01's SoW names DEL-03-02 as an owner only (DX-2 return) |
| N-21 | DEL-02-03 → DEL-03-02 | DEL-02-03's SoW: ownership sentence only |
| N-24 | DEL-02-03 → DEL-03-03 | DEL-02-03's SoW: ownership sentence only |
| X-1 | DEL-02-03 → DEL-01-04 | DEL-02-03's SoW: "constructs the App act control", a construction statement |

No arc outside the accepted set was added. N-12 and N-B8 are absent. None of the SCC-enlarging arcs E-1…E-5 or reverse citations K-1…K-12 is present. N-07 (DEL-02-03 → DEL-04-02) is carried by DEL-04-02's supplier-side row.

## 4. Classification

**`DEPARTURE`**: arcs were added. The SCCs and inventory did not change, so no SCC forms, changes or dissolves, and no case opens or closes.

## 5. `DAG pending` deliverables (15)

A pending deliverable gets no ready or blocked verdict from dependencies until the owner decides. Unaffected deliverables keep using DAG-001. **The decision awaited for every row is the same:** the owner's checkpoint C decision on successor candidate `_DAG/_Candidates/DAG-002/`, to accept it or reject the change. Either answer clears the flag; a follow-up currency audit then records it.

Arcs are listed by P2 label. "→" marks a new input the deliverable consumes; "←" marks a new consumer of the deliverable. (A) is the admitted layer and (C) the non-gating candidate layer (SCC-002, SCC-CASE-002).

| Deliverable | New inputs it consumes | New consumers of it |
|---|---|---|
| DEL-01-01 | — | N-16 ← DEL-02-01 (A); N-23 ← DEL-02-03 (A); N-B4 ← DEL-03-03 (A); N-B9 ← DEL-03-04 (A); N-15 ← DEL-04-03 (A); N-C5 ← DEL-09-06 (A) |
| DEL-02-01 | N-16 → DEL-01-01 (A); N-17 → DEL-02-03 (C) | N-B3 ← DEL-03-02 (C); N-20 ← DEL-03-03 (C); N-19 ← DEL-09-06 (A) |
| DEL-02-02 | — | N-C1 ← DEL-09-06 (A) |
| DEL-02-03 | N-23 → DEL-01-01 (A); N-07 → DEL-04-02 (C); N-22 → DEL-05-01 (C) | N-17 ← DEL-02-01 (C); N-27 ← DEL-03-03 (C); N-02 ← DEL-04-02 (C); N-13 ← DEL-04-03 (C); N-25 ← DEL-05-02 (C); N-26 ← DEL-09-09 (C) |
| DEL-03-01 | N-11 → DEL-04-03 (C) | N-01 ← DEL-04-02 (C); N-10 ← DEL-04-03 (C); N-C2 ← DEL-09-06 (A) |
| DEL-03-02 | N-B3 → DEL-02-01 (C); N-05 → DEL-04-02 (C) | N-C3 ← DEL-09-06 (A) |
| DEL-03-03 | N-B4 → DEL-01-01 (A); N-20 → DEL-02-01 (C); N-27 → DEL-02-03 (C); N-06 → DEL-04-02 (C) | N-14 ← DEL-04-03 (C); N-C4 ← DEL-09-06 (A) |
| DEL-03-04 | N-B9 → DEL-01-01 (A); N-B10 → DEL-09-06 (A); N-B11 → DEL-09-09 (A) | — |
| DEL-04-01 | — | N-28 ← DEL-09-06 (A) |
| DEL-04-02 | N-02 → DEL-02-03 (C); N-01 → DEL-03-01 (C); R8-A → DEL-05-01 (C) | N-07 ← DEL-02-03 (C); N-05 ← DEL-03-02 (C); N-06 ← DEL-03-03 (C); N-03 ← DEL-05-01 (C); N-04 ← DEL-05-02 (C); N-08 ← DEL-09-06 (A); N-09 ← DEL-09-09 (C) |
| DEL-04-03 | N-15 → DEL-01-01 (A); N-13 → DEL-02-03 (C); N-10 → DEL-03-01 (C); N-14 → DEL-03-03 (C); R8-B → DEL-05-01 (C) | N-11 ← DEL-03-01 (C) |
| DEL-05-01 | N-03 → DEL-04-02 (C) | N-22 ← DEL-02-03 (C); R8-A ← DEL-04-02 (C); R8-B ← DEL-04-03 (C); N-C6 ← DEL-09-09 (C) |
| DEL-05-02 | N-25 → DEL-02-03 (C); N-04 → DEL-04-02 (C) | — |
| DEL-09-06 | N-C5 → DEL-01-01 (A); N-19 → DEL-02-01 (A); N-C1 → DEL-02-02 (A); N-C2 → DEL-03-01 (A); N-C3 → DEL-03-02 (A); N-C4 → DEL-03-03 (A); N-28 → DEL-04-01 (A); N-08 → DEL-04-02 (A) | N-B10 ← DEL-03-04 (A) |
| DEL-09-09 | N-26 → DEL-02-03 (C); N-09 → DEL-04-02 (C); N-C6 → DEL-05-01 (C) | N-B11 ← DEL-03-04 (A) |

These are the 14 first-increment deliverables plus DEL-02-02 (through N-C1). **DEL-01-04 is not pending.** P2 expected 16, with DEL-01-04 pending through X-1; X-1 is not in any register, so it is not a departure.

## 6. Evidence drift alongside the departure

These changes do not alter the arc set. They are read from the live files:

- **Representatives.** Four existing arcs have a new SR-6 representative (the new consumer-side row). The old one becomes a MIRROR: DEL-04-02 → DEL-03-02, DEL-04-03 → DEL-03-02, DEL-04-03 → DEL-04-01 and DEL-04-03 → DEL-04-02. No layer changes.
- **Mirrors.** 16 new mirror comparisons, two with a RequiredMaturity difference (TBD against INITIALIZED): DEL-03-03 → DEL-04-01 and DEL-09-06 → DEL-04-03. Assessed in the DAG-002 candidate's `Evidence/MirrorAssessment.md`.
- **Rows.** 10 new EXTERNAL rows; 4 EXTERNAL rows retired (DEP-02-03-015/-016, DEP-05-02-014/-015); 52 existing rows with field edits (statements, sources, quotes, notes, target names); SoW text in 16 deliverables.

## 7. Advice: renewed examination (not `DAG pending`)

These deliverables are not endpoints of a changed arc, so they are not pending. They consume a deliverable that gained inputs, so their route may be worth re-examining when they next rely on those inputs:

- DEL-09-07 (consumes DEL-09-06);
- DEL-10-03 (consumes DEL-02-01, DEL-02-03, DEL-03-01, DEL-03-02, DEL-04-03, DEL-05-01, DEL-05-02);
- DEL-09-02 (consumes DEL-02-01, DEL-02-03, DEL-04-03);
- DEL-01-04, DEL-06-01, DEL-06-02, DEL-09-05 and DEL-09-11 (consume DEL-04-03);
- DEL-02-04 and DEL-08-02 (consume DEL-02-01);
- DEL-08-01 (consumes DEL-05-01).

DEL-01-02 and DEL-01-03 are the route to DEL-01-01, which gains six admitted consumers; P2 named them as advice too.

## 8. What follows

A candidate successor is prepared for these decisions only: `_DAG/_Candidates/DAG-002/` (project-dag TRIGGER=SUCCESSOR, CURRENCY_REPORT = this audit). This audit does not edit DAG-001, the pointer, or any local file. It establishes currency only, not satisfaction, readiness or lifecycle.
