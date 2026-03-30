# Dependencies: DEL-002-03 Structural Framing Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** 21 rows (3 ANCHOR, 18 EXECUTION; 21 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-03-A01 | IMPLEMENTS_NODE | SOW-0012 | Complete final structural design (concrete structure 35' ceiling) | HIGH |
| DEP-002-03-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant fully functional facility | HIGH |
| DEP-002-03-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC documentation | HIGH |

### EXECUTION Rows -- UPSTREAM (10 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-03-E01 | PREREQUISITE | DELIVERABLE | Preliminary Structural Design (DEL-002-01) | HIGH | BLOCKING |
| DEP-002-03-E02 | PREREQUISITE | DELIVERABLE | Geotechnical Investigation & Report (DEL-008-01) | HIGH | BLOCKING |
| DEP-002-03-E03 | INTERFACE | DELIVERABLE | Architectural Floor Plans (DEL-001-02) | MEDIUM | ADVISORY |
| DEP-002-03-E04 | PREREQUISITE | EXTERNAL | Crane Manufacturer Data (SOW-0067 supplier) | HIGH | BLOCKING |
| DEP-002-03-E05 | INTERFACE | DELIVERABLE | Foundation Plan (DEL-002-02) | HIGH | ADVISORY |
| DEP-002-03-E07 | PREREQUISITE | DELIVERABLE | Preliminary Site Survey (DEL-008-02) | MEDIUM | ADVISORY |
| DEP-002-03-E08 | PREREQUISITE | DELIVERABLE | Preliminary Architectural Design (DEL-001-01) | HIGH | BLOCKING |
| DEP-002-03-E09 | INTERFACE | DELIVERABLE | Structural Specification (DEL-002-12) | MEDIUM | ADVISORY |
| DEP-002-03-E17 | PREREQUISITE | DOCUMENT | National Building Code of Canada -- Climatic Data | HIGH | BLOCKING |
| DEP-002-03-E18 | CONSTRAINT | EXTERNAL | County Approval of Preliminary Design | HIGH | BLOCKING |

### EXECUTION Rows -- DOWNSTREAM (8 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-03-E06 | HANDOVER | DELIVERABLE | Concrete Superstructure (DEL-011-01) | HIGH | BLOCKING |
| DEP-002-03-E10 | HANDOVER | DELIVERABLE | Structural Sections & Details (DEL-002-04) | HIGH | ADVISORY |
| DEP-002-03-E11 | HANDOVER | DELIVERABLE | Mezzanine Framing Details (DEL-002-05) | HIGH | ADVISORY |
| DEP-002-03-E12 | HANDOVER | DELIVERABLE | Service Pit Structural Details (DEL-002-06) | HIGH | ADVISORY |
| DEP-002-03-E13 | HANDOVER | DELIVERABLE | Crane Support Structure Details (DEL-002-07) | HIGH | ADVISORY |
| DEP-002-03-E14 | INTERFACE | DELIVERABLE | Steel Plate Embedment Plan (DEL-002-08) | HIGH | ADVISORY |
| DEP-002-03-E15 | INTERFACE | DELIVERABLE | Structural Calculation Package (DEL-002-10) | HIGH | ADVISORY |
| DEP-002-03-E16 | HANDOVER | DELIVERABLE | Building Permit Application & Approval (DEL-009-02) | HIGH | BLOCKING |

---

## Run Notes

### Run: 2026-03-26 (SCA-001 refresh)

**Parameters:**
- SCOPE: PKG-002 (all deliverables DEL-002-01 through DEL-002-12)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)
- SOURCE_DOCS: AUTO | ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md

**SCA-001 impact assessment:**
- SOW-0012 updated: "precast concrete walls, steel roof structure, interior walls precast concrete" (Add. 2/4). This is a material change to the structural system that DEL-002-03 must show.
- _CONTEXT.md updated (2026-03-26): "Structural system updated: precast concrete walls + steel roof (Add. 2/4). Interior walls precast concrete (Add. 4, Q5). Crane corbels integrated into side walls (Add. 4, Q3)."
- SOW-0067 updated: 25' max bay spacing, corbel-supported. Affects crane runway framing shown on DEL-002-03.
- **Potential new dependency signal:** Precast wall panel supplier/fabricator data may become a new EXTERNAL PREREQUISITE for framing plan coordination (panel dimensions, connection details, corbel locations). However, source documents (Datasheet.md, Procedure.md, Specification.md, Guidance.md) have not yet been updated to reference precast supplier data as an explicit input. Under CONSERVATIVE strictness, no new row emitted.
- **Potential new dependency signal:** Addenda documents R-08, R-09, R-10 are now referenced in the decomposition. Source documents do not yet list these as explicit required inputs. Under CONSERVATIVE strictness, no new row emitted.
- **Recommendation:** After source documents are updated to reflect SCA-001 addenda content, re-run dependency extraction. A precast panel supplier/fabricator interface and the addenda constraint documents may warrant new EXECUTION rows.

**Extraction result:**
- All 21 existing ACTIVE rows re-confirmed. LastSeen updated to 2026-03-26.
- No new rows. No RETIRED rows.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) present and unique. No integrity issues.

---

### Run Parameters (2026-02-26)
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO (resolved: Datasheet.md, Specification.md, Procedure.md, Guidance.md)
- **ANCHOR_DOC:** AUTO (resolved: Datasheet.md -- contains "datasheet" keyword; highest-confidence anchor source with explicit Scope Item and Objectives fields)
- **EXECUTION_DOC_ORDER:** AUTO (resolved: Procedure.md, Specification.md, Guidance.md -- Procedure contains explicit prerequisites and step-by-step workflow; Specification contains scope exclusions/relationships; Guidance contains sequencing rationale)
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1, 2026-02-25)
- **_REFERENCES.md:** Present; used for document pointer resolution.

### Decomposition Validation
- DEL-002-03 confirmed in decomposition: PKG-002, Structural Framing Plans, Drawing Set, covers SOW-0012, supports OBJ-001, OBJ-003.
- SOW-0012 confirmed: "Complete final structural design (concrete structure, 35' ceiling)" -- IN scope.
- OBJ-001 confirmed: "Deliver a code-compliant, fully functional maintenance shop addition."
- OBJ-003 confirmed: "Produce complete, P.Eng.-stamped IFC design documentation across all disciplines."
- All target deliverable IDs resolved and confirmed in decomposition.

### Defaults and Assumptions
- ANCHOR_DOC selection: Datasheet.md chosen by AUTO heuristic (filename contains "datasheet"; document contains structured Identification fields with explicit Scope Item and Objectives references).
- EXECUTION_DOC_ORDER selection: Procedure.md prioritized (contains "procedure" keyword; structured prerequisites and steps). Specification.md second (scope exclusions table with explicit relationship statements). Guidance.md third (supporting rationale and sequencing notes).
- All ANCHOR rows emitted from explicit identifiers only (CONSERVATIVE mode).
- All EXECUTION rows emitted from explicit prerequisite/interface/handover/constraint statements only.
- No IMPLICIT rows emitted in this run.

### Warnings
- None. All checks passed.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE (Anchor) | ACTIVE (Execution) | RETIRED |
|---|---|---|---|---|---|---|---|---|
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | R2 2026-03-26 SCA-001 (validated) | None | 3 | 18 | 0 |
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | R1 2026-02-25 (validated) | None | 3 | 18 | 0 |

---

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
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 18 | 0 |

### By Direction (EXECUTION only)
| Direction | Count |
|---|---|
| UPSTREAM | 10 |
| DOWNSTREAM | 8 |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating Readiness Assessment

DEL-002-03 (Structural Framing Plans) has **6 BLOCKING upstream dependencies** that gate meaningful estimating:

1. **DEP-002-03-E01 (DEL-002-01 Preliminary Structural Design):** The structural system type and column grid cannot be finalized without County-approved preliminary design. This affects member sizes, quantities, and material type (concrete vs. hybrid). BLOCKING for estimating.

2. **DEP-002-03-E02 (DEL-008-01 Geotechnical Investigation):** Required for final structural loads. Guidance notes that superstructure framing can begin before geotech, but finalization (and therefore accurate quantity takeoff) requires geotech completion. BLOCKING for final estimate; preliminary estimate possible with assumptions.

3. **DEP-002-03-E04 (Crane Manufacturer Data):** Crane wheel loads and runway span are required to size crane runway beams -- a major cost driver. Without crane data, runway framing quantities cannot be estimated accurately. BLOCKING for crane-related scope.

4. **DEP-002-03-E08 (DEL-001-01 Preliminary Architectural Design):** Approved architectural layout sets the room program and column spacing constraints. BLOCKING for estimating column grid and framing quantities.

5. **DEP-002-03-E17 (NBC Climatic Data):** Snow, wind, and seismic loads directly affect member sizing. These are standard lookup values for the site location and can be obtained independently. BLOCKING but resolvable without external dependency.

6. **DEP-002-03-E18 (County Approval):** Contractual gate per R-01 s3.3.2. No IFC production (and therefore no final estimate basis) without this approval. BLOCKING.

### ADVISORY Dependencies (Estimating Impact)

- **DEP-002-03-E03 (Architectural Floor Plans):** Changes to room layout could shift column locations and affect quantities. Monitor for stability.
- **DEP-002-03-E05 (Foundation Plan):** Column base connection type (pinned vs. fixed) affects framing design but is typically resolved during detailed design. Low risk to preliminary estimate.
- **DEP-002-03-E07 (Preliminary Site Survey):** Site datum needed for elevation references; unlikely to change framing quantities significantly.
- **DEP-002-03-E09 (Structural Specification):** Material specification (concrete class, steel grade) affects unit costs but not quantities.

### Downstream Estimating Impact

DEL-002-03 produces the primary structural geometry from which **5 downstream deliverables** derive their scope:
- DEL-002-04 (Structural Sections & Details)
- DEL-002-05 (Mezzanine Framing Details)
- DEL-002-06 (Service Pit Structural Details)
- DEL-002-07 (Crane Support Structure Details)
- DEL-002-08 (Steel Plate Embedment Plan)

These downstream deliverables cannot be accurately estimated until DEL-002-03 framing plans establish the member layout and grid. DEL-002-03 is therefore a **critical path deliverable for PKG-002 structural estimating**.

Additionally, DEL-002-03 produces IFC drawings required for:
- DEL-011-01 (Concrete Superstructure construction) -- BLOCKING for construction estimating
- DEL-009-02 (Building Permit Application) -- BLOCKING for permit timeline

---

*_DEPENDENCIES.md generated by DEPENDENCIES agent (Type 2). Date: 2026-02-26.*
*Run 1: UPDATE mode, CONSERVATIVE strictness, TASK_ESTIMATING consumer context.*
