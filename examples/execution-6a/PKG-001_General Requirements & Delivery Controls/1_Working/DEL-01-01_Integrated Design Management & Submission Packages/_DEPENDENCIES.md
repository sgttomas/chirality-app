# Dependencies: DEL-01-01 Integrated Design Management & Submission Packages

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (21 rows)
- **Last Run:** 2026-02-17
- **Schema Version:** v3.1

### Summary

| Category | Count |
|---|---|
| Total Rows | 21 |
| ANCHOR rows | 9 |
| EXECUTION rows | 12 |
| ACTIVE | 21 |
| RETIRED | 0 |

### ANCHOR Edges (9)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-01-01-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-001 General Requirements & Delivery Controls | HIGH |
| DEP-01-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0001 | HIGH |
| DEP-01-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0002 | HIGH |
| DEP-01-01-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0003 | HIGH |
| DEP-01-01-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0004 | HIGH |
| DEP-01-01-006 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0005 | HIGH |
| DEP-01-01-007 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0006 | HIGH |
| DEP-01-01-008 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |
| DEP-01-01-009 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | HIGH |

### EXECUTION Edges (12)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-01-01-010 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 | HIGH |
| DEP-01-01-011 | UPSTREAM | PREREQUISITE | DOCUMENT | Addenda 01-03 | HIGH |
| DEP-01-01-012 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR (Appendix A) | HIGH |
| DEP-01-01-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | HIGH |
| DEP-01-01-014 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (Appendix D) | HIGH |
| DEP-01-01-015 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading Information (Appendix E) | HIGH |
| DEP-01-01-016 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Plan (Appendix F) | HIGH |
| DEP-01-01-017 | UPSTREAM | PREREQUISITE | DOCUMENT | Executed CCDC 14-2013 Contract | HIGH |
| DEP-01-01-018 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 Baseline Schedule | HIGH |
| DEP-01-01-019 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 Baseline Schedule | HIGH |
| DEP-01-01-020 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-04 Permitting & AHJ | HIGH |
| DEP-01-01-021 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-01-05 Meetings & Change Control | HIGH |

## Run Notes

### Run: 2026-02-17

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO
- ANCHOR_DOC: AUTO

**Resolved Defaults:**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains `datasheet`)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (selected by heuristic: procedure > spec > guidance)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for anchor validation and label resolution)

**Assumptions:**
- ANCHOR_DOC selection based on DEFAULT heuristic (filename pattern matching).
- Execution doc ordering based on DEFAULT heuristic (procedure first for workflow clarity).
- OBJ-001 and OBJ-008 treated as TRACES_TO_REQUIREMENT anchors (objective trace links explicitly stated in Datasheet).

**Warnings:**
- None. All checks passed.

**Quality Check Results:**
- Required columns present: PASS
- DependencyID uniqueness: PASS (21 unique IDs)
- ACTIVE rows with evidence: PASS (all 21 rows have EvidenceFile + SourceRef)
- Enum normalization: PASS (all canonical)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE)
- FromDeliverableID consistency: PASS (all rows = DEL-01-01_Integrated-Design-Management)
- No duplicate rows detected.
- _DEPENDENCIES.md counts consistent with Dependencies.csv: PASS

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | ACTIVE Total |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (FINAL v1.0 PHASE7) | None | 9 | 12 | 21 |

## Lifecycle Summary

### Extraction Lifecycle

| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

### Closure Lifecycle (SatisfactionStatus)

| SatisfactionStatus | Count |
|---|---|
| TBD | 21 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 9 | 0 |
| EXECUTION | 12 | 0 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT: NONE -- no consumer-specific handoff notes generated.
