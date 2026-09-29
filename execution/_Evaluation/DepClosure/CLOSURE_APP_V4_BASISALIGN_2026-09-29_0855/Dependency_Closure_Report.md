# Dependency closure report — APP_V4_BASISALIGN

- **Snapshot:** `CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`, run `APP-V4-BASIS-ALIGN-20260928`, node D1.
- **Workflow:** `chirality-root:bundled:workflow:audit-dep-closure`.
- **Basis:** commit `b585e5ebead38f8ece442c80cd3bec5be8363cf3`, clean tree. It follows the SCA-V4-001 SoW revisions (RV-1…RV-4) and the dependency-extract UPDATE of 18 registers (DX-1/2/3).
- **Frozen manifest:** 130 entries, SHA-256 `6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250`, over the same file classes as DAG-001.
- **Comparison basis:** `CLOSURE_APP_V4_TARGETS_2026-09-27_2237` (DAG-001's closure, source `85dcc17c`).
- **Tool:** `tools/coordination/analyze_dep_closure.py`, sha256 `2b8de3cbd2439ba1234aadf10e07348c4e2d30dd73da66cd0d88774e417a9adc`. Exact arguments and the input basis with hashes are in [Tool_Run.json](Tool_Run.json).

## Scope inventory

| Item | Value |
|---|---|
| Inventory source | GROUP3-20260928T001055Z `canonical/Deliverables.csv`, via `_LATEST_ACCEPTED.md` |
| Counted units | 41 Deliverables in 11 Packages; 41 workspace folders; they agree |
| Exemptions | none |
| Tracking mode | FULL_GRAPH (`_COORDINATION.md` and all 41 `_DEPENDENCIES.md`) |

## Core checks

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | Schema compliance | PASS | 41/41 valid v3.1 (`Evidence/coverage.csv`); strict SCH/EVQ/DRB 0 findings (`Evidence/register_validation.json`) |
| 2 | Orphan dependencies | PASS | 0 (`Evidence/orphans.csv`); 0 outside-scope (`Evidence/outside_scope.csv`) |
| 3 | Circular dependencies | **BLOCKER** (raw acyclic objective) | 6 SCCs, 24 nodes (`Evidence/scc_summary.csv`); 6 representative cycles (`Evidence/cycles_sample.csv`) |
| 4 | Anchor coverage | PASS | 41/41 `IMPLEMENTS_NODE` |
| 5 | Misplaced fields | PASS | 0 |
| 6 | ID format | PASS | 0 long-form IDs, 0 normalizations (`Evidence/id_normalization.csv`) |
| 7 | Isolated deliverables | PASS | 0 (`Evidence/isolated.csv`) |
| 8 | Hubs (≥ 20) | WARNING | 3 (`Evidence/hubs.csv`) |
| 9 | Bidirectional pairs | INFO | 22 (`Evidence/bidirectional_pairs.csv`) |
| 10 | Declared disagreements | PASS | 0 disagreements, 0 declared-only, 0 unread |
| 11 | Accepted DAG currency | WARNING (INCOMPLETE) | `_DAG/_LATEST.md` has no `Latest:` line; `Evidence/dag_pending.csv` empty for that reason only. The `project-dag` currency audit governs |

## Graph

| Metric | Prior (85dcc17c) | Now (b585e5ebe) | Delta |
|---|---:|---:|---:|
| Nodes | 41 | 41 | 0 |
| Rows (all) | 759 | 822 | +63 |
| ACTIVE EXECUTION rows | 403 | 462 | +59 (63 added, 4 retired) |
| Rows with a Deliverable target | 201 | 254 | +53 |
| Arcs (consumer → supplier) | 161 | 198 | +37, 0 removed |
| SCCs | 6 | 6 | 0, identical member sets |
| Nodes in SCCs | 24 | 24 | 0 |
| Intra-SCC rows / arcs | 66 / 52 | 96 / 74 | +30 / +22, all in SCC-002 |
| Bidirectional pairs | 14 | 22 | +8, all in SCC-002 |
| Hubs (≥ 20) | 1 | 3 | +2 |

### SCCs and case lineage

| SCC (this snapshot) | Size | Members | Internal rows / arcs (prior) | Continuing case |
|---|---:|---|---|---|
| SCC-001 | 2 | DEL-01-01; DEL-01-05 | 4 / 2 (4 / 2) | SCC-CASE-001 |
| SCC-002 | 13 | DEL-01-04; DEL-02-01; DEL-02-02; DEL-02-03; DEL-02-04; DEL-03-01; DEL-03-02; DEL-03-03; DEL-04-02; DEL-04-03; DEL-05-01; DEL-05-02; DEL-09-09 | **76 / 62** (46 / 40) | SCC-CASE-002 (SCC-CASE-004 constituent history) |
| SCC-003 | 2 | DEL-01-06; DEL-09-01 | 2 / 2 (2 / 2) | SCC-CASE-003 |
| SCC-004 | 3 | DEL-07-01; DEL-07-02; DEL-08-01 | 8 / 4 (8 / 4) | SCC-CASE-005 |
| SCC-005 | 2 | DEL-10-02; DEL-10-04 | 3 / 2 (3 / 2) | SCC-CASE-006 |
| SCC-006 | 2 | DEL-11-01; DEL-11-03 | 3 / 2 (3 / 2) | SCC-CASE-007 |

Every member set equals the prior snapshot's, so each SCC continues its case by member-set matching. No case opens, closes or needs a matching ruling. The 22 new arcs inside SCC-002 are evidence for CASE-002.

### New bidirectional pairs (all inside SCC-002)

DEL-02-01 ↔ DEL-02-03; DEL-02-03 ↔ DEL-04-02; DEL-02-03 ↔ DEL-04-03; DEL-02-03 ↔ DEL-05-01; DEL-03-01 ↔ DEL-04-03; DEL-03-02 ↔ DEL-04-02; DEL-04-02 ↔ DEL-05-01; DEL-04-03 ↔ DEL-05-01. Each pair joins two separately stated interfaces. The DX returns and ARC_ANALYSIS (N-03 with R8-A; N-11 with N-10; N-17 with DEP-02-03 → DEL-02-01) describe distinct contributions in each direction.

### Hubs

| Deliverable | Dependents (in) | Suppliers (out) | Total | Prior |
|---|---:|---:|---:|---:|
| DEL-04-03 | 17 | 10 | 27 | 21 |
| DEL-02-03 | 12 | 8 | 20 | below threshold |
| DEL-04-01 | 20 | 0 | 20 | below threshold |

These are coordination concentrations. DEL-04-01 is a pure supplier (policy and human-act distinctions) and stays outside every SCC.

## Arcs added (37) and removed (0)

The added arcs are exactly the refreshed arc set accepted at checkpoint A (DECISION-6), less N-18, N-21, N-24 and X-1, which no register row carries (see the DX-2 returns for DEL-02-01 and DEL-02-03). The disputed arcs N-12 and N-B8 are absent. None of the kept-out guard arcs E-1…E-5 or K-1…K-12 is present. The per-arc list with P2 labels, layer and representative row is in the currency audit (`_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856/Evidence/added_arcs.csv`).

| Group | Arcs |
|---|---|
| Outside any SCC (15) | DEL-02-01 → DEL-01-01 (N-16); DEL-02-03 → DEL-01-01 (N-23); DEL-03-03 → DEL-01-01 (N-B4); DEL-03-04 → DEL-01-01 (N-B9), → DEL-09-06 (N-B10), → DEL-09-09 (N-B11); DEL-04-03 → DEL-01-01 (N-15); DEL-09-06 → DEL-01-01 (N-C5), DEL-02-01 (N-19), DEL-02-02 (N-C1), DEL-03-01 (N-C2), DEL-03-02 (N-C3), DEL-03-03 (N-C4), DEL-04-01 (N-28), DEL-04-02 (N-08) |
| Inside SCC-002 (22) | N-01…N-07, N-09, N-10, N-11, N-13, N-14, N-17, N-20, N-22, N-25, N-26, N-27, N-B3, N-C6, R8-A, R8-B |

## Accepted-DAG currency (advisory)

The analyzer's comparison returned `INCOMPLETE`: "no `Latest:` line naming a version" in `_DAG/_LATEST.md`. This is the pointer-form finding P2 recorded (SUCCESSOR_PLAN §1). It is not a register defect. The `project-dag` currency audit `CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856` resolved DAG-001 from the prose pointer and its acceptance record, and classifies the change as `DEPARTURE`.

## Routing

- **SCCs:** `scc-resolution-case` evidence update for CASE-002 only (new held arcs). Cases 001, 003, 005, 006, 007 unchanged. No remedy is prescribed.
- **Registers:** no coverage defect; no `dependency-extract` repair is routed from this run.
- **Pointer form:** to the owner at checkpoint C (C2-6), via the integrator.
- **Currency and the successor:** `project-dag` (the currency audit and the DAG-002 candidate).

This observation is not an accepted graph and establishes no readiness, satisfaction or lifecycle change.
