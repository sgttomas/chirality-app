# Dependencies: DEL-05-03 Option - Access Control

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (9 rows; schema v3.1)
- **ACTIVE rows:** 9 (2 ANCHOR + 7 EXECUTION)
- **RETIRED rows:** 0

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID/Name | Confidence |
|---|---|---|---|---|
| DEP-05-03-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0502 | HIGH |
| DEP-05-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-010 | HIGH |

### EXECUTION Dependencies (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|---|
| DEP-05-03-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Program) | Requires floor plan concept for zone mapping | HIGH |
| DEP-05-03-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-06 (Electrical/IT) | Requires coordination for low-voltage power, conduit, network | HIGH |
| DEP-05-03-005 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 (Security & Cameras) | Integration interface notes for complementary optional item | MEDIUM |
| DEP-05-03-006 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 (Commissioning/Closeout) | Commissioning test results and training records feed into building commissioning | HIGH |
| DEP-05-03-007 | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-01-01 (Design Management) | Submittals governed by design milestone schedule | HIGH |
| DEP-05-03-008 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | Key Fob Access room designations required as input | HIGH |
| DEP-05-03-009 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR S12.3 (Access Control) | Primary requirement statement defining scope and zone intent | HIGH |

## Run Notes

### Defaults and Paths Used
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected by DOC_ROLE_MAP heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Guidance.md, Specification.md (ordered by workflow clarity)
- **Decomposition path:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (located and used for validation)
- **_REFERENCES.md:** Read; used to confirm OSR source location

### Assumptions
- ANCHOR_DOC selected as Datasheet.md per AUTO heuristic (highest-confidence match for definition/traceability signal).
- Functional Program and OSR are contained within the RFP PDF at `_Sources/AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf`; TargetLocation points there.
- DEL-05-04 interface (DEP-05-03-005) is rated MEDIUM confidence because the integration is described as optional/complementary rather than a hard requirement; the systems are designed to be self-contained.

### Warnings
- None.

### Quality Check Results
- All 29 required columns present in Dependencies.csv.
- All 9 DependencyIDs are unique.
- All ACTIVE rows have EvidenceFile and SourceRef populated.
- Exactly 1 ACTIVE IMPLEMENTS_NODE anchor found (DEP-05-03-001) -- parent anchor check PASS.
- FromDeliverableID consistent across all rows (DEL-05-03_Optional-Access-Control).
- No legacy enum values requiring normalization.
- No duplicate rows detected.
- CSV parses successfully (Python csv.DictReader validation).

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (v1.0 PHASE7) | None | 9 (2 ANCHOR + 7 EXECUTION) |

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE | 9 |
| RETIRED | 0 |
| **Total** | **9** |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |

All satisfaction statuses are TBD pending downstream work initiation.
