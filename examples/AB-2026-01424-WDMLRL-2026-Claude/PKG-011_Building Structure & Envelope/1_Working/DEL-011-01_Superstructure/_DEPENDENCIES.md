# Dependencies: DEL-011-01 Concrete Superstructure

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- PKG-010 Foundation Construction -- Foundation system installation
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-011 Building Structure & Envelope -- Other envelope components depend on superstructure
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

- **Status:** ACTIVE
- **Dependencies.csv:** Dependencies.csv (v3.1)
- **Total Rows:** 37
- **ACTIVE:** 37
- **RETIRED:** 0

### ANCHOR Rows (3)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-01-A01 | IMPLEMENTS_NODE | SOW-0022 | Construct building with precast concrete walls and steel roof structure, 35' ceiling (Add. 2/4) | HIGH |
| DEP-011-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |
| DEP-011-01-A03 | TRACES_TO_REQUIREMENT | OBJ-002 | Complete all work on or before December 31 2026 | HIGH |

### EXECUTION Rows -- UPSTREAM (24)

| DependencyID | DependencyType | TargetType | TargetDeliverableID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-01-E01 | PREREQUISITE | DELIVERABLE | DEL-002-02 | Structural IFC Drawings (DEL-002-02 through DEL-002-10) | HIGH | BLOCKING |
| DEP-011-01-E02 | PREREQUISITE | DELIVERABLE | DEL-001-02 | Architectural IFC Drawings (DEL-001 series) | HIGH | BLOCKING |
| DEP-011-01-E03 | PREREQUISITE | PACKAGE | -- | MEP IFC Drawings (PKG-003 through PKG-006 series) | HIGH | BLOCKING |
| DEP-011-01-E04 | INTERFACE | DELIVERABLE | DEL-016-01 | Crane manufacturer requirements | HIGH | BLOCKING |
| DEP-011-01-E05 | PREREQUISITE | DELIVERABLE | DEL-008-01 | Geotechnical Investigation Report | HIGH | BLOCKING |
| DEP-011-01-E06 | PREREQUISITE | DELIVERABLE | DEL-002-10 | Structural Calculation Package (f'c) | HIGH | BLOCKING |
| DEP-011-01-E07 | PREREQUISITE | DELIVERABLE | DEL-009-02 | Building Permit | HIGH | BLOCKING |
| DEP-011-01-E08 | PREREQUISITE | DELIVERABLE | DEL-009-03 | Safety Code Permits | HIGH | BLOCKING |
| DEP-011-01-E09 | PREREQUISITE | DELIVERABLE | DEL-009-01 | Development Permit | HIGH | BLOCKING |
| DEP-011-01-E10 | PREREQUISITE | DELIVERABLE | DEL-010-01 | Foundation Construction | HIGH | BLOCKING |
| DEP-011-01-E11 | PREREQUISITE | DELIVERABLE | DEL-021-04 | CCDC 14-2013 Contract Execution | HIGH | BLOCKING |
| DEP-011-01-E12 | PREREQUISITE | DELIVERABLE | DEL-021-02 | Performance and Payment Bonds | HIGH | BLOCKING |
| DEP-011-01-E13 | PREREQUISITE | DELIVERABLE | DEL-021-03 | Insurance Package | HIGH | BLOCKING |
| DEP-011-01-E14 | PREREQUISITE | DELIVERABLE | DEL-019-01 | Prime Contractor Designation & OH&S | HIGH | BLOCKING |
| DEP-011-01-E15 | INTERFACE | DELIVERABLE | DEL-002-07 | Crane Support Structure Details | HIGH | ADVISORY |
| DEP-011-01-E16 | INTERFACE | DELIVERABLE | DEL-002-08 | Steel Plate Embedment Plan | HIGH | ADVISORY |
| DEP-011-01-E17 | INTERFACE | DELIVERABLE | DEL-002-06 | Service Pit/Trench Structural Details | HIGH | ADVISORY |
| DEP-011-01-E18 | INTERFACE | DELIVERABLE | DEL-002-05 | Mezzanine Framing Details | MEDIUM | ADVISORY |
| DEP-011-01-E19 | INTERFACE | DELIVERABLE | DEL-001-07 | Door and Window Schedule | MEDIUM | ADVISORY |
| DEP-011-01-E20 | INTERFACE | DELIVERABLE | DEL-014-01 | Cistern coordination | MEDIUM | ADVISORY |
| DEP-011-01-E21 | INTERFACE | DELIVERABLE | DEL-008-03 | Construction Survey | MEDIUM | ADVISORY |
| DEP-011-01-E30 | CONSTRAINT | EXTERNAL | -- | County site preparation | HIGH | BLOCKING |
| DEP-011-01-E31 | CONSTRAINT | EXTERNAL | -- | County/Landfill aggregate supply | MEDIUM | ADVISORY |
| DEP-011-01-E32 | INTERFACE | DELIVERABLE | DEL-014-04 | Floor Drains (MEP sleeve coordination) | MEDIUM | ADVISORY |

### EXECUTION Rows -- DOWNSTREAM (10)

| DependencyID | DependencyType | TargetType | TargetDeliverableID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-011-01-E22 | HANDOVER | DELIVERABLE | DEL-011-02 | Steel Plate Floor Embedments (field tracking) | HIGH | ADVISORY |
| DEP-011-01-E23 | ENABLES | DELIVERABLE | DEL-011-03 | Drive-Through Repair Bays | HIGH | ADVISORY |
| DEP-011-01-E24 | INTERFACE | DELIVERABLE | DEL-011-05 | Wash Bay Enclosure | HIGH | ADVISORY |
| DEP-011-01-E25 | ENABLES | DELIVERABLE | DEL-016-01 | Overhead Cranes (runway supports) | HIGH | ADVISORY |
| DEP-011-01-E26 | ENABLES | PACKAGE | -- | PKG-012 through PKG-015 (downstream trades) | HIGH | BLOCKING |
| DEP-011-01-E27 | HANDOVER | DELIVERABLE | DEL-008-04 | As-Built Survey | MEDIUM | ADVISORY |
| DEP-011-01-E28 | HANDOVER | DELIVERABLE | DEL-009-04 | Inspection Coordination Log | MEDIUM | ADVISORY |
| DEP-011-01-E29 | ENABLES | DELIVERABLE | DEL-021-05 | Guarantee Period Obligations | MEDIUM | INFO |
| DEP-011-01-E33 | ENABLES | DELIVERABLE | DEL-011-04 | Entrance/Exit Doors | MEDIUM | ADVISORY |
| DEP-011-01-E34 | INTERFACE | DELIVERABLE | DEL-018-05 | Wash Bay Drainage & Mud Sump | MEDIUM | ADVISORY |

---

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Inputs and Defaults:**
- SCOPE: DEL-011-01
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (located and read successfully)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: Datasheet.md (AUTO -- selected as highest-confidence anchor doc per filename heuristic)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md, Datasheet.md)
- DOC_ROLE_MAP: DEFAULT

**Decomposition status:** LOCATED and VALIDATED. DEL-011-01 confirmed in decomposition S7 PKG-011 as covering SOW-0022, supporting OBJ-001 and OBJ-002.

**_REFERENCES.md status:** Read. Two references listed (R-01 RFP, R-04 Appendix B Shop). Used for context but no additional dependency rows emitted solely from reference listing.

**Warnings:**
- None.

**Pass 1 (ANCHOR) findings:**
- 1 IMPLEMENTS_NODE anchor found (SOW-0022) -- validated against decomposition S3-D and S7 PKG-011.
- 2 TRACES_TO_REQUIREMENT anchors found (OBJ-001, OBJ-002) -- validated against decomposition S5 and S7 PKG-011.

**Pass 2 (EXECUTION) findings:**
- 24 UPSTREAM execution dependencies extracted (13 PREREQUISITE, 9 INTERFACE from Procedure prerequisites and Specification/Procedure step-level references, 2 CONSTRAINT from external County obligations).
- 10 DOWNSTREAM execution dependencies extracted (3 HANDOVER, 4 ENABLES, 3 INTERFACE/ENABLES).
- All execution dependencies supported by explicit textual evidence in source documents.
- DEL-016-01 appears in both UPSTREAM (crane manufacturer requirements needed as input) and DOWNSTREAM (crane installation enabled by runway supports) -- this is intentional and correct: information flows in both directions at different stages.

**Estimating impact assessment (CONSUMER_CONTEXT=TASK_ESTIMATING):**
- 16 rows classified as BLOCKING (explicit prerequisites/constraints that gate construction commencement).
- 17 rows classified as ADVISORY (interfaces/handovers that affect scope/quantities but are not hard gates).
- 1 row classified as INFO (warranty tracking linkage).
- 3 rows have no estimating classification (ANCHOR rows).

### Run 2026-03-26 (SCA-001 Refresh)

**Inputs and Defaults:**
- SCOPE: DEL-011-01 (as part of PKG-011 batch)
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-app/examples/AB-2026-01424-WDMLRL-2026-Claude/
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (R2 -- 2026-03-26, SCA-001)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: Datasheet.md (AUTO)
- EXECUTION_DOC_ORDER: AUTO (Procedure.md, Specification.md, Guidance.md, Datasheet.md)

**Decomposition status:** LOCATED and VALIDATED. R2 decomposition reflects SCA-001 changes (Addenda 2, 3, 4).

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0022 updated: "Construct building with precast concrete walls and steel roof structure, 35' ceiling height (Add. 2 required full concrete; Add. 4 relaxed to precast walls + steel roof)"
- DEP-011-01-A01 anchor statement updated to reflect precast walls + steel roof clarification.
- Crane corbel support (Add. 4, Q3) reinforces existing DEP-011-01-E04 and DEP-011-01-E15 interface dependencies. No new rows needed -- existing edges already capture this coupling.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 37 ACTIVE rows.
- Updated DEP-011-01-A01 statement to reflect SCA-001 SOW-0022 text (precast walls + steel roof).
- No new rows added. No rows retired.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Located and validated | None | 3 | 34 | 37 |
| 2026-03-26 | UPDATE | CONSERVATIVE | Located and validated (R2 SCA-001) | None | 3 | 34 | 37 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 37 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| PENDING | 34 |
| TBD | 3 |

**Notes:** All ANCHOR rows have SatisfactionStatus=TBD (anchors represent traceability, not closure-trackable dependencies). All EXECUTION rows are PENDING (no evidence of satisfaction at this stage).
