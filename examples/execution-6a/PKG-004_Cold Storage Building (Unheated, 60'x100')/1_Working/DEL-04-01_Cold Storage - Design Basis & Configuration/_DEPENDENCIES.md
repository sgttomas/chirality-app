# Dependencies: DEL-04-01 Cold Storage - Design Basis & Configuration

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Dependencies.csv (13 rows)
- **Last Run:** 2026-02-17
- **Schema Version:** v3.1

### Summary

| DependencyClass | Count (ACTIVE) |
|---|---|
| ANCHOR | 4 |
| EXECUTION | 9 |
| **Total** | **13** |

### ANCHOR Edges (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-04-01-A001 | IMPLEMENTS_NODE | PACKAGE | PKG-004 Cold Storage Building (Unheated 60x100) | HIGH |
| DEP-04-01-A002 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0300 | HIGH |
| DEP-04-01-A003 | TRACES_TO_REQUIREMENT | WBS_NODE | SOW-0301 | HIGH |
| DEP-04-01-A004 | TRACES_TO_REQUIREMENT | WBS_NODE | OBJ-004 | HIGH |

### EXECUTION Edges (9 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-04-01-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 (main building door/window profile) | HIGH |
| DEP-04-01-E002 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (Appendix D) | HIGH |
| DEP-04-01-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 (site plan / building location) | HIGH |
| DEP-04-01-E004 | UPSTREAM | PREREQUISITE | DOCUMENT | Public Works Critical Design Equipment List (Appendix B) | HIGH |
| DEP-04-01-E005 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-02 (doors/openings/hardware) | HIGH |
| DEP-04-01-E006 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-03 (floor & foundation) | HIGH |
| DEP-04-01-E007 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-04 (electrical & ventilation) | HIGH |
| DEP-04-01-E008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 (grading/drainage) | HIGH |
| DEP-04-01-E009 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-04 (permitting & AHJ) | MEDIUM |

## Run Notes

### Run: 2026-02-17

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- ANCHOR_DOC: AUTO (resolved: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved: Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (found; accessible)
- _REFERENCES.md: present (minimal content; used for document location resolution)

**Defaults applied:**
- ANCHOR_DOC selected as Datasheet.md (contains `datasheet` keyword; strongest definition/traceability signal with Identification table containing Scope Items, Objective, Package IDs)
- EXECUTION_DOC_ORDER: Procedure.md first (contains `procedure` keyword; explicit Prerequisites table and phased Steps), then Specification.md (cross-references and scope boundary statements), then Guidance.md (considerations and trade-offs)

**Decomposition validation:**
- All anchor target identifiers (PKG-004, SOW-0300, SOW-0301, OBJ-004) validated against decomposition
- All deliverable target IDs (DEL-02-04, DEL-03-01, DEL-03-02, DEL-04-02, DEL-04-03, DEL-04-04, DEL-01-04) confirmed in decomposition Phase 5

**Warnings:** None.

**Integrity checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-04-01-A001) -- PASS
- DependencyID uniqueness: PASS (13 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- All enums canonical: PASS
- No duplicate extracted rows: PASS

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (v1.0 PHASE7) | None | 13 (4 ANCHOR + 9 EXECUTION) |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |
