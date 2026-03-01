# Tier Analysis — EPREP_BOE_WDMLRL_2026-02-26_2131

## Inputs
- SCAFFOLD_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
- DEPENDENCY_SOURCES: `AUTO` (per-deliverable `Dependencies.csv`)

## Graph construction rules (for tiering)
- Included: `DependencyClass=EXECUTION`, `TargetType=DELIVERABLE`, `Status=ACTIVE`, `EstimateImpactClass=BLOCKING`.
- Edge orientation: `UPSTREAM` ⇒ `TargetDeliverableID → FromDeliverableID`; `DOWNSTREAM` ⇒ `FromDeliverableID → TargetDeliverableID`.
- Excluded from tiering: non-deliverable targets (documents/external), non-blocking edges (ADVISORY/INFO), rows with missing IDs, unknown directions, and edges referencing unknown deliverables.

## Summary stats
- Deliverables (nodes): 117
- EXECUTION deliverable-to-deliverable rows found: 1001
- Blocking rows used for DAG: 407
- Unique blocking edges (after de-dup): 353
- Tier count: 6
- Max tier index: T5
- Cycles detected: YES

### Blocking edges by DependencyType
| DependencyType | Count |
|---|---:|
| PREREQUISITE | 281 |
| HANDOVER | 51 |
| INTERFACE | 30 |
| ENABLES | 26 |
| CONSTRAINT | 19 |

### Excluded row counts (diagnostic)
| Reason | Count |
|---|---:|
| impact_ADVISORY | 507 |
| non_deliverable_target | 488 |
| impact_INFO | 71 |
| unknown_node | 13 |
| missing_from_or_target | 11 |
| impact_TBD | 2 |
| impact_(blank) | 1 |

## Tier distribution
| Tier | Deliverables | Example items |
|---|---:|---|
| T0 | 11 | DEL-003-01, DEL-006-04, DEL-006-06, DEL-008-01, DEL-008-02, DEL-015-01, DEL-017-02, DEL-020-01 … |
| T1 | 6 | DEL-001-01, DEL-005-01, DEL-006-01, DEL-006-03, DEL-020-03, DEL-021-02 |
| T2 | 13 | DEL-001-03, DEL-001-05, DEL-001-07, DEL-001-09, DEL-001-11, DEL-004-01, DEL-005-02, DEL-005-04 … |
| T3 | 8 | DEL-001-10, DEL-004-08, DEL-005-03, DEL-007-02, DEL-014-02, DEL-018-01, DEL-019-01, DEL-021-05 |
| T4 | 5 | DEL-005-05, DEL-007-03, DEL-019-02, DEL-019-03, DEL-019-04 |
| T5 | 1 | DEL-007-04 |

## Cycle nodes
The following deliverables could not be tiered due to cycles in the blocking dependency graph:
- DEL-001-02
- DEL-001-04
- DEL-001-06
- DEL-001-08
- DEL-002-01
- DEL-002-02
- DEL-002-03
- DEL-002-04
- DEL-002-05
- DEL-002-06
- DEL-002-07
- DEL-002-08
- DEL-002-09
- DEL-002-10
- DEL-002-11
- DEL-002-12
- DEL-003-02
- DEL-003-03
- DEL-003-04
- DEL-003-05
- DEL-003-06
- DEL-003-07
- DEL-004-02
- DEL-004-03
- DEL-004-04
- DEL-004-05
- DEL-004-06
- DEL-004-07
- DEL-004-09
- DEL-006-02
- DEL-006-07
- DEL-006-08
- DEL-008-03
- DEL-008-04
- DEL-009-01
- DEL-009-02
- DEL-009-03
- DEL-009-04
- DEL-010-01
- DEL-011-01
- DEL-011-02
- DEL-011-03
- DEL-011-04
- DEL-011-05
- DEL-011-06
- DEL-011-07
- DEL-012-01
- DEL-012-02
- DEL-012-03
- DEL-013-01
- DEL-013-02
- DEL-013-03
- DEL-013-04
- DEL-013-05
- DEL-013-06
- DEL-014-01
- DEL-014-03
- DEL-014-04
- DEL-014-05
- DEL-014-06
- DEL-015-02
- DEL-015-03
- DEL-015-04
- DEL-015-05
- DEL-016-01
- DEL-017-01
- DEL-017-03
- DEL-017-04
- DEL-018-02
- DEL-018-03
- DEL-018-04
- DEL-018-05
- DEL-018-06
