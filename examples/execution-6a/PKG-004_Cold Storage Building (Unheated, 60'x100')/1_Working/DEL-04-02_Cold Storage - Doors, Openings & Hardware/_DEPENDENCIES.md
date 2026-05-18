# Dependencies: DEL-04-02 Cold Storage - Doors, Openings & Hardware

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (11 rows; 11 ACTIVE, 0 RETIRED)
- **Summary:** 2 ANCHOR rows + 9 EXECUTION rows extracted from source documents.

### ANCHOR Edges (Tree)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0402-A01 | IMPLEMENTS_NODE | SOW-0302 | SOW-0302: Provide openings on two opposite sides with doors and hardware | HIGH |
| DEP-0402-A02 | TRACES_TO_REQUIREMENT | OBJ-004 | OBJ-004: Deliver unheated cold storage building with practical access and door configuration compatible with main building | HIGH |

### EXECUTION Edges (DAG)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0402-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 Cold Storage - Design Basis & Configuration | HIGH |
| DEP-0402-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 Structure Envelope Roof & Overhead Doors (Main Building) | HIGH |
| DEP-0402-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 Site Plan Circulation Parking & Operational Layout | HIGH |
| DEP-0402-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 Grading Earthworks Drainage & Stormwater | MEDIUM |
| DEP-0402-E05 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-04-03 Cold Storage - Floor & Foundation (DB Proposed) | MEDIUM |
| DEP-0402-E06 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-04-04 Cold Storage - Electrical & Ventilation | HIGH |
| DEP-0402-E07 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code (ABC) | HIGH |
| DEP-0402-E08 | UPSTREAM | INTERFACE | EXTERNAL | Pickled-Sand Storage Building (key commonality) | HIGH |
| DEP-0402-E09 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Appendix A (OSR) | HIGH |

## Run Notes

- **Run date:** 2026-02-17
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- **ANCHOR_DOC:** AUTO (resolved to: Datasheet.md -- contains explicit identification fields with Scope Coverage and Objective Support)
- **EXECUTION_DOC_ORDER:** AUTO (resolved to: Procedure.md, Guidance.md, Specification.md)
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for anchor validation and target resolution)
- **_REFERENCES.md:** Available; used to confirm OSR source document location
- **Existing Dependencies.csv:** Not present (new file created)

### Defaults and Assumptions
- ANCHOR_DOC selected as Datasheet.md based on presence of explicit identification table (Scope Coverage, Objective Support fields).
- EXECUTION_DOC_ORDER prioritized Procedure.md (contains explicit Prerequisites section and step-by-step workflow) followed by Guidance.md and Specification.md.
- All ANCHOR rows confirmed against decomposition scope ledger and objectives table.
- All DELIVERABLE target IDs confirmed against decomposition deliverables tables.
- DEP-0402-E08 (pickled-sand key commonality) classified as EXTERNAL because pickled-sand storage is explicitly out of scope (SOW-0400).
- DEP-0402-A02 TargetType set to WBS_NODE (OBJ-004 is an objective in the decomposition tree, not a formal requirement ID).

### Warnings
- None.

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 PHASE7) | None | 11 |

## Lifecycle Summary

- **ACTIVE:** 11
- **RETIRED:** 0
- **Total:** 11

### By DependencyClass
- ANCHOR: 2 ACTIVE, 0 RETIRED
- EXECUTION: 9 ACTIVE, 0 RETIRED

### By SatisfactionStatus
- TBD: 11

### Integrity Check Results
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE -- PASS
- DependencyID uniqueness: PASS
- All ACTIVE rows have EvidenceFile and SourceRef: PASS
- CSV parseable: PASS
- Counts consistent with Dependencies.csv: PASS
