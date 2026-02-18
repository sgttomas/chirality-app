# Dependencies: DEL-01-05 Meetings, Documentation & Change Control

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (11 rows)
- **RegisterSchemaVersion:** v3.1

### Summary

| DependencyClass | AnchorType | Count (ACTIVE) |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 3 |
| EXECUTION | NOT_APPLICABLE | 7 |
| **Total** | | **11** |

### ANCHOR Edges (4 rows)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0105-001 | IMPLEMENTS_NODE | WBS_NODE | DEL-01-05_Project-Controls-and-Documentation | HIGH |
| DEP-0105-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0011 | HIGH |
| DEP-0105-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0012 | HIGH |
| DEP-0105-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | MEDIUM |

### EXECUTION Edges (7 rows)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0105-005 | UPSTREAM | CONSTRAINT | EXTERNAL | Contract Award (CCDC 14-2013) | HIGH |
| DEP-0105-006 | UPSTREAM | PREREQUISITE | EXTERNAL | Project Committee identified by Owner | HIGH |
| DEP-0105-007 | UPSTREAM | PREREQUISITE | EXTERNAL | Project Manager (PM) identified by Owner | HIGH |
| DEP-0105-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 Baseline Schedule Updates & Reporting | HIGH |
| DEP-0105-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-03 Health & Safety (Prime Contractor) Plan | HIGH |
| DEP-0105-010 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 Commissioning Training Closeout & Warranty | HIGH |
| DEP-0105-011 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 (with Town supplementary conditions) | MEDIUM |

## Run Notes

### Defaults and Paths Used
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- **ANCHOR_DOC:** AUTO (resolved to: Datasheet.md)
- **EXECUTION_DOC_ORDER:** AUTO (resolved to: Procedure.md, Specification.md, Guidance.md)
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (found and used for validation)
- **_REFERENCES.md:** Present; used for document pointer resolution (limited content -- single RFP reference)

### Assumptions and Warnings
- OBJ-008 mapping is marked ASSUMPTION in source (PACKAGE_HEURISTIC); carried as MEDIUM confidence. TBD (Lensing D-003): confirm whether additional objectives apply.
- CCDC 14-2013 contract text location is TBD (not accessed during this run); DEP-0105-011 TargetLocation set to `location TBD`.
- No warnings issued. Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE found (PASS). No FLOATING_NODE or AMBIGUOUS_ANCHOR conditions.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (FINAL v1.0 PHASE7) | None | 4 | 7 | 11 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 11 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no handoff notes produced.
