# Dependencies: DEL-02-05 Mechanical, Plumbing, Ventilation & Exhaust

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register (populated by DEPENDENCIES agent)

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (18 rows; schema v3.1)
- **Summary:** 6 ANCHOR rows + 12 EXECUTION rows = 18 total (all ACTIVE)

### ANCHOR Edges (6)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0205-A01 | IMPLEMENTS_NODE | WBS_NODE | DEL-02-05 decomposition entry (PKG-002) | HIGH |
| DEP-0205-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0204 | HIGH |
| DEP-0205-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0213 | HIGH |
| DEP-0205-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0214 | HIGH |
| DEP-0205-A05 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0223 | HIGH |
| DEP-0205-A06 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0230 | HIGH |

### EXECUTION Edges (12)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-0205-E01 | UPSTREAM | PREREQUISITE | DEL-02-02 | Firehall Apparatus Bays & Support Spaces | HIGH |
| DEP-0205-E02 | UPSTREAM | PREREQUISITE | DEL-02-03 | Public Works Shop Bays Workshop & Support Spaces | HIGH |
| DEP-0205-E03 | UPSTREAM | PREREQUISITE | DEL-02-01 | Architectural Program Layout & Code Planning | HIGH |
| DEP-0205-E04 | UPSTREAM | PREREQUISITE | DEL-03-04 | Site Utilities Distribution & Allowance-Based Tie-Ins | HIGH |
| DEP-0205-E05 | UPSTREAM | PREREQUISITE | DEL-02-07 | Emergency Power & Backup Generator | HIGH |
| DEP-0205-E06 | UPSTREAM | INTERFACE | DEL-02-04 | Structure Envelope Roof & Overhead Doors | HIGH |
| DEP-0205-E07 | UPSTREAM | INTERFACE | DEL-03-02 | Grading Earthworks Drainage & Stormwater | HIGH |
| DEP-0205-E08 | UPSTREAM | INTERFACE | DEL-02-02 | Firehall Apparatus Bays (compressed air scope boundary) | MEDIUM |
| DEP-0205-E09 | DOWNSTREAM | HANDOVER | DEL-01-07 | Commissioning Training Closeout & Warranty | HIGH |
| DEP-0205-E10 | DOWNSTREAM | INTERFACE | DEL-02-07 | Emergency Power & Backup Generator | HIGH |
| DEP-0205-E11 | UPSTREAM | CONSTRAINT | DEL-02-03 | PW Shop Bays (bay count confirmation for sump design) | HIGH |
| DEP-0205-E12 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code and applicable codes | HIGH |

## Run Notes

### Defaults and Paths Used
- **Run date:** 2026-02-17
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents
- **ANCHOR_DOC:** AUTO -- selected `Datasheet.md` (contains Identification table with scope items and objectives)
- **EXECUTION_DOC_ORDER:** AUTO -- `Procedure.md` (strongest prerequisite/workflow signal), `Specification.md` (cross-references), `Guidance.md` (considerations and conflicts)
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` -- located and read successfully
- **_REFERENCES.md:** Read; used to confirm source document accessibility (OSR and Addendum 03 locations)

### Warnings
- None. No integrity warnings generated.

### Assumptions Logged
- Objectives OBJ-001, OBJ-002, OBJ-003 are listed as ASSUMPTION in Datasheet (package-heuristic mapping); not extracted as ANCHOR rows since they are heuristic and not explicitly assigned to this deliverable in the decomposition scope ledger. Decomposition confirms the mapping at best-effort level.
- DEP-0205-E08 (compressed air scope boundary) is rated MEDIUM confidence because the interface is explicit but the resolution direction is TBD (CON-M-01 awaiting human ruling).

## Run History

| Timestamp | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Located and validated (PHASE7 v1.0) | None | 18 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 18
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown for ACTIVE rows)
- **TBD:** 18
- **PENDING:** 0
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

### Tree x DAG Integrity
- **Parent anchor (IMPLEMENTS_NODE):** 1 (PASS)
- **Requirement trace anchors (TRACES_TO_REQUIREMENT):** 5
- **Execution edges:** 12 (10 UPSTREAM, 2 DOWNSTREAM)
- **Cross-package dependencies:** 3 (DEL-03-04, DEL-03-02, DEL-01-07)

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no consumer-specific notes generated.
