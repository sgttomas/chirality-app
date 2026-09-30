# Dependency closure report — APP_V4_SCA002

- **Snapshot:** `CLOSURE_APP_V4_SCA002_2026-09-29_2056`, run `APP-V4-SCA002-20260929`, node D1.
- **Workflow:** `chirality-root:bundled:workflow:audit-dep-closure`.
- **Basis:** commit `8cd783d8d7493fbfe663fb108449e4ceda04a00b`, clean tree. It follows the accepted scope change SCA-V4-002 (DECISION-2, DECISION-3): the 9 SoW REVISEs with the B-06a reading-rule note, and the `dependency-extract` UPDATE of 11 registers (DX).
- **Frozen manifest:** 130 entries, SHA-256 `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5`, over the same file classes as DAG-001 and DAG-002; 32 members changed since DAG-002.
- **Comparison basis:** `CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855` (DAG-002's closure, source `b585e5ebe`).
- **Tool:** `tools/coordination/analyze_dep_closure.py`, sha256 `2b8de3cbd2439ba1234aadf10e07348c4e2d30dd73da66cd0d88774e417a9adc`. Exact arguments and the input basis with hashes are in [Tool_Run.json](Tool_Run.json).

## Scope inventory

| Item | Value |
|---|---|
| Inventory source | GROUP3-20260928T001055Z `canonical/Deliverables.csv`, via `_LATEST_ACCEPTED.md` (pointer text changed by B-06a; the named snapshot and register are unchanged) |
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
| 8 | Hubs (≥ 20) | WARNING | 4 (`Evidence/hubs.csv`) |
| 9 | Bidirectional pairs | INFO | 24 (`Evidence/bidirectional_pairs.csv`) |
| 10 | Declared disagreements | PASS | 0 disagreements, 0 declared-only, 0 unread |
| 11 | Accepted DAG currency | WARNING (**DEPARTURE**) | Against DAG-002: 4 arcs added, 0 removed, 5 `DAG pending` (`Evidence/dag_pending.csv`). Advisory; the `project-dag` currency audit governs |

## Graph

| Metric | Prior (b585e5ebe) | Now (8cd783d8d) | Delta |
|---|---:|---:|---:|
| Nodes | 41 | 41 | 0 |
| Rows (all) | 822 | 826 | +4 |
| ACTIVE EXECUTION rows | 462 | 465 | +3 (4 added, 1 retired) |
| Rows with a Deliverable target | 254 | 258 | +4 |
| Arcs (consumer → supplier) | 198 | 202 | +4, 0 removed |
| SCCs | 6 | 6 | 0, identical member sets |
| Nodes in SCCs | 24 | 24 | 0 |
| Intra-SCC rows / arcs | 96 / 74 | 100 / 78 | +4 / +4, all in SCC-002 |
| Bidirectional pairs | 22 | 24 | +2, both in SCC-002 |
| Hubs (≥ 20) | 3 | 4 | +1 |

### SCCs and case lineage

| SCC (this snapshot) | Size | Members | Internal rows / arcs (prior) | Continuing case |
|---|---:|---|---|---|
| SCC-001 | 2 | DEL-01-01; DEL-01-05 | 4 / 2 (4 / 2) | SCC-CASE-001 |
| SCC-002 | 13 | DEL-01-04; DEL-02-01; DEL-02-02; DEL-02-03; DEL-02-04; DEL-03-01; DEL-03-02; DEL-03-03; DEL-04-02; DEL-04-03; DEL-05-01; DEL-05-02; DEL-09-09 | **80 / 66** (76 / 62) | SCC-CASE-002 (SCC-CASE-004 constituent history) |
| SCC-003 | 2 | DEL-01-06; DEL-09-01 | 2 / 2 (2 / 2) | SCC-CASE-003 |
| SCC-004 | 3 | DEL-07-01; DEL-07-02; DEL-08-01 | 8 / 4 (8 / 4) | SCC-CASE-005 |
| SCC-005 | 2 | DEL-10-02; DEL-10-04 | 3 / 2 (3 / 2) | SCC-CASE-006 |
| SCC-006 | 2 | DEL-11-01; DEL-11-03 | 3 / 2 (3 / 2) | SCC-CASE-007 |

Every member set equals the prior snapshot's, so each SCC continues its case by member-set matching. No case opens, closes or needs a matching ruling. The 4 new arcs inside SCC-002 are evidence for CASE-002.

### New bidirectional pairs (both inside SCC-002)

DEL-02-01 ↔ DEL-03-02 (N-18 with the existing N-B3, DEP-03-02-027) and DEL-02-03 ↔ DEL-03-03 (N-24 with the existing N-27, DEP-03-03-014). ARC_EFFECT §3 predicted both. Each joins two separately stated interfaces: the consumer's use of the supplier's dispositions, identities and observations on one side, and the supplier's receipt of declared constraints or the checkpoint statement on the other.

### Hubs

| Deliverable | Dependents (in) | Suppliers (out) | Total | Prior |
|---|---:|---:|---:|---:|
| DEL-04-03 | 17 | 10 | 27 | 27 |
| DEL-02-03 | 12 | 11 | 23 | 20 |
| DEL-02-01 | 12 | 8 | 20 | below threshold |
| DEL-04-01 | 20 | 0 | 20 | 20 |

These are coordination concentrations. DEL-04-01 is a pure supplier (policy and human-act distinctions) and stays outside every SCC; it gained no supplier (the DX guard held).

## Arcs added (4) and removed (0)

The added arcs are exactly the four the owner kept under SCA-V4-002 (OWNER_ITEMS Q-4; DECISION-2 "accept the remaining items as recommended"), now carried by the consumer-side rows the DX run extracted from the revised CLM-002 sentences:

| Label | Arc | Row | Reverse row present |
|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEP-02-01-029 UPSTREAM INTERFACE | DEP-03-02-027 (N-B3) |
| N-21 | DEL-02-03 → DEL-03-02 | DEP-02-03-025 UPSTREAM INTERFACE | — |
| N-24 | DEL-02-03 → DEL-03-03 | DEP-02-03-026 UPSTREAM INTERFACE | DEP-03-03-014 (N-27) |
| X-1 | DEL-02-03 → DEL-01-04 | DEP-02-03-027 UPSTREAM INTERFACE | — |

All four have both ends inside SCC-002, so none changes the partition. The disputed arcs N-12 and N-B8 remain absent. None of the kept-out guard arcs E-1…E-5 or K-1…K-12 is present; DEL-04-01 keeps 0 suppliers; no SCC-002 member depends on DEL-09-06.

## Accepted-DAG currency (advisory)

The analyzer resolved `Latest: DAG-002` from `_DAG/_LATEST.md` and reports `DEPARTURE`: the four arcs above added, none removed, no inventory change, and five deliverables `DAG pending`: DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03 (`Evidence/dag_pending.csv`). The `project-dag` currency audit `CURRENCY_APP_V4_SCA002_2026-09-29_2057` governs, classifies the change as `DEPARTURE`, and names the decision awaited (owner checkpoint C on the DAG-003 candidate).

## Routing

- **SCCs:** `scc-resolution-case` evidence update for CASE-002 only (four new held arcs). Cases 001, 003, 005, 006, 007 unchanged. No remedy is prescribed.
- **Registers:** no coverage defect; no `dependency-extract` repair is routed from this run.
- **Currency and the successor:** `project-dag` (the currency audit and the DAG-003 candidate).

This observation is not an accepted graph and establishes no readiness, satisfaction or lifecycle change.
