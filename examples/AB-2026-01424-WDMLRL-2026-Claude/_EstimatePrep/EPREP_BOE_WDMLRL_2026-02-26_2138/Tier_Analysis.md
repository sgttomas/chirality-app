# Tier Analysis — EPREP_BOE_WDMLRL_2026-02-26_2138

## Inputs
- SCAFFOLD_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
- DEPENDENCY_SOURCES: `AUTO` (per-deliverable `Dependencies.csv`)

## Graph construction rules (for tiering)
- Included rows: `DependencyClass=EXECUTION`, `TargetType=DELIVERABLE`, `Status=ACTIVE`, `EstimateImpactClass=BLOCKING`.
- Deliverable ID normalization: `DEL-XXX-YY_Label` → `DEL-XXX-YY`; package-level `DEL-XXX` mapped to a representative deliverable (see Decision Log / Conflicts).
- Edge orientation: `UPSTREAM` ⇒ `TargetDeliverableID → FromDeliverableID`; `DOWNSTREAM` ⇒ `FromDeliverableID → TargetDeliverableID`.
- Cycle handling: compute SCCs; tier the SCC condensation DAG; all deliverables within an SCC share the same tier (iterative bundle).

## Summary stats
- Deliverables (nodes): 117
- EXECUTION deliverable-to-deliverable rows found: 1001
- Blocking rows used (pre-dedup): 420
- Unique blocking edges (after de-dup): 364
- SCC component count: 106
- Cyclic SCC bundles (size>1): 4
- Tier count (SCC DAG): 13
- Max tier index: T12

### Blocking edges by DependencyType
| DependencyType | Count |
|---|---:|
| PREREQUISITE | 292 |
| HANDOVER | 52 |
| INTERFACE | 30 |
| ENABLES | 26 |
| CONSTRAINT | 20 |

### Excluded row counts (diagnostic)
| Reason | Count |
|---|---:|
| impact_ADVISORY | 507 |
| non_deliverable_target | 488 |
| impact_INFO | 71 |
| missing_from_or_target | 11 |
| impact_TBD | 2 |
| impact_(blank) | 1 |

## Tier distribution
| Tier | Deliverables | Example items |
|---|---:|---|
| T0 | 7 | DEL-003-01, DEL-008-01, DEL-008-02, DEL-015-01, DEL-017-02, DEL-021-01, DEL-021-03 |
| T1 | 6 | DEL-001-01, DEL-002-01, DEL-002-10, DEL-005-01, DEL-006-01, DEL-021-02 |
| T2 | 18 | DEL-001-03, DEL-001-05, DEL-001-07, DEL-001-09, DEL-001-11, DEL-002-02, DEL-002-03, DEL-002-04, DEL-002-06, DEL-004-01 … |
| T3 | 12 | DEL-001-02, DEL-001-10, DEL-002-05, DEL-002-11, DEL-004-08, DEL-005-03, DEL-007-02, DEL-009-02, DEL-011-06, DEL-014-02 … |
| T4 | 15 | DEL-001-06, DEL-001-08, DEL-002-08, DEL-002-09, DEL-004-04, DEL-004-05, DEL-005-05, DEL-006-04, DEL-006-06, DEL-007-03 … |
| T5 | 6 | DEL-006-03, DEL-006-07, DEL-007-04, DEL-008-04, DEL-009-03, DEL-020-01 |
| T6 | 9 | DEL-006-02, DEL-006-08, DEL-009-04, DEL-010-01, DEL-017-01, DEL-017-03, DEL-017-04, DEL-018-02, DEL-020-02 |
| T7 | 12 | DEL-002-07, DEL-003-05, DEL-003-06, DEL-004-02, DEL-004-03, DEL-004-06, DEL-015-04, DEL-016-01, DEL-018-03, DEL-018-04 … |
| T8 | 9 | DEL-001-04, DEL-002-12, DEL-003-02, DEL-003-04, DEL-003-07, DEL-004-07, DEL-004-09, DEL-011-01, DEL-018-06 |
| T9 | 7 | DEL-003-03, DEL-011-02, DEL-011-04, DEL-011-05, DEL-015-02, DEL-015-03, DEL-015-05 |
| T10 | 5 | DEL-011-03, DEL-011-07, DEL-012-02, DEL-013-01, DEL-018-05 |
| T11 | 6 | DEL-012-01, DEL-013-02, DEL-013-04, DEL-013-06, DEL-014-01, DEL-014-04 |
| T12 | 5 | DEL-013-03, DEL-013-05, DEL-014-03, DEL-014-05, DEL-014-06 |

## Cyclic SCC bundles (iterative)
The following SCCs contain cycles in BLOCKING dependencies; treat each as an iterative coordination bundle (single tier):
- (9 items) DEL-002-07, DEL-003-05, DEL-003-06, DEL-004-02, DEL-004-03, DEL-004-06, DEL-015-04, DEL-016-01, DEL-018-04
- (2 items) DEL-002-01, DEL-002-10
- (2 items) DEL-012-02, DEL-013-01
- (2 items) DEL-013-03, DEL-013-05
