# Dependencies: DEL-002-11 Foundation Design Package (Variable-Price)

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending — to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) — human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) — human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 13 rows)
- **RegisterSchemaVersion:** v3.1
- **ACTIVE rows:** 13
- **RETIRED rows:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-002-11-A01 | IMPLEMENTS_NODE | SOW-0019 | Design foundation (variable-price post-geotech) | HIGH |
| DEP-002-11-A02 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-002-11-A03 | TRACES_TO_REQUIREMENT | OBJ-006 | Variable-price foundation cost reconciliation | HIGH |

### EXECUTION Edges (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-002-11-E01 | UPSTREAM | PREREQUISITE | DEL-008-01 | Geotechnical Investigation & Report | BLOCKING |
| DEP-002-11-E02 | UPSTREAM | PREREQUISITE | DEL-002-01 | Preliminary Structural Design | BLOCKING |
| DEP-002-11-E03 | DOWNSTREAM | HANDOVER | DEL-002-02 | Foundation Plan | ADVISORY |
| DEP-002-11-E04 | DOWNSTREAM | HANDOVER | DEL-010-01 | Foundation Construction | BLOCKING |
| DEP-002-11-E05 | UPSTREAM | INTERFACE | DEL-001-02 | Architectural Floor Plans | ADVISORY |
| DEP-002-11-E06 | UPSTREAM | INTERFACE | DEL-006-04 | Cistern & Pump Details | ADVISORY |
| DEP-002-11-E07 | UPSTREAM | INTERFACE | DEL-016-01 | Two 5-Tonne Overhead Cranes | ADVISORY |
| DEP-002-11-E08 | DOWNSTREAM | HANDOVER | DEL-002-10 | Structural Calculation Package | ADVISORY |
| DEP-002-11-E09 | DOWNSTREAM | INTERFACE | DEL-002-08 | Steel Plate Embedment Plan | ADVISORY |
| DEP-002-11-E10 | UPSTREAM | CONSTRAINT | (DOCUMENT) R-01 | AB-2026-01424-WDMLRL RFP.pdf | BLOCKING |

## Run Notes

### Run: 2026-03-26 (SCA-001 refresh)

**Parameters:**
- SCOPE: PKG-002 (all deliverables DEL-002-01 through DEL-002-12)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)
- SOURCE_DOCS: AUTO | ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md

**SCA-001 impact assessment:**
- SOW-0019 unchanged: variable-price foundation scope remains as-is.
- The precast wall system change (Add. 2/4) may change superstructure load distribution to foundations, but this is captured through the existing interfaces (DEL-002-10 calculation package, DEL-002-02 foundation plan). No new dependency edges.
- No addenda changes directly affect foundation design variable-price scope.

**Extraction result:**
- All 13 existing ACTIVE rows re-confirmed. LastSeen updated to 2026-03-26.
- No new rows. No RETIRED rows.

**Warnings:**
- None.

---

### Run Configuration (2026-02-26)
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
- **Decomposition Status:** FOUND (R1 -- 2026-02-25). All anchor targets validated against decomposition sections 3, 5, 7, and 8.

### Source Document Configuration
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder, identified 4 candidate source documents.
- **ANCHOR_DOC:** AUTO -- selected `Datasheet.md` (contains identification table with SOW/OBJ references).
- **EXECUTION_DOC_ORDER:** AUTO -- `Specification.md` (requirements), `Procedure.md` (workflow/prerequisites), `Guidance.md` (principles/considerations).
- **_REFERENCES.md:** Read-only; used to resolve `TargetLocation` for RFP document (R-01 at `_Sources/`).

### Defaults Applied
- All `SatisfactionStatus` values defaulted to `TBD` (no evidence of fulfillment in source documents).
- All `RequiredMaturity` and `ProposedMaturity` values left empty (not determinable from current sources).

### Corrections Applied (UPDATE Mode)
- **DEP-002-11-E03:** Direction corrected from `UPSTREAM` to `DOWNSTREAM`; DependencyType corrected from `INTERFACE` to `HANDOVER`. The Datasheet Conditions section states "Foundation design produced here feeds the Foundation Plan drawing deliverable" -- the information flow is FROM DEL-002-11 TO DEL-002-02, making this a downstream handover rather than an upstream interface.

### New Rows Added (This Run)
- **DEP-002-11-E05:** Architectural Floor Plans (DEL-001-02) -- upstream interface for column grid/footprint confirmation. Source: Procedure Prerequisites table.
- **DEP-002-11-E06:** Cistern & Pump Details (DEL-006-04) -- upstream interface for cistern load data. Source: Procedure Prerequisites table.
- **DEP-002-11-E07:** Two 5-Tonne Overhead Cranes (DEL-016-01) -- upstream interface for crane technical data. Source: Procedure Prerequisites table.
- **DEP-002-11-E08:** Structural Calculation Package (DEL-002-10) -- downstream handover of foundation calculations. Source: Procedure Step 2.3.
- **DEP-002-11-E09:** Steel Plate Embedment Plan (DEL-002-08) -- downstream interface for embedment coordination. Source: Procedure Steps 2.3 and 2.4.
- **DEP-002-11-E10:** RFP Document (R-01) -- upstream constraint establishing variable-price mechanism. Source: Specification REQ-001 and REQ-002.

### Edges NOT Extracted (Documented)
- **Civil/site grading coordination (PKG-005):** Procedure Step 2.5 item 4 mentions issuing foundation plan to Civil Engineer for drainage interface. This is a coordination statement without a specific artifact transfer or prerequisite gate. Not extracted per information-flow-only rule.
- **Mechanical penetrations (PKG-003):** Procedure Step 2.5 item 2 mentions issuing foundation plan to Mechanical Engineer. General coordination without specific prerequisite; not extracted.
- **Plumbing drains/stub-ups (PKG-006 beyond DEL-006-04):** Procedure Step 2.5 item 3 mentions plumbing coordination for floor drains. DEL-006-04 cistern interface already captured as E06; remaining plumbing coordination is not a distinct prerequisite.
- **CFT-001 (OBJ-001 mapping question):** Datasheet Conflict Table flags whether DEL-002-11 should also support OBJ-001. This is a human ruling item. Not extracted as an anchor because the decomposition does not list OBJ-001 for DEL-002-11, and CONSERVATIVE strictness prohibits assumed anchors.

### Warnings
- (None)

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | FOUND (R2, SCA-001) | None | 3 | 10 | 13 |
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | FOUND (R1, 2026-02-25) | None | 3 | 10 | 13 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 13
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus)
- **TBD:** 13
- **PENDING:** 0
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

### By DependencyClass
- **ANCHOR:** 3 (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT)
- **EXECUTION:** 10 (2 PREREQUISITE, 3 INTERFACE upstream, 1 CONSTRAINT, 3 HANDOVER downstream, 1 INTERFACE downstream)

### Parent Anchor Check
- IMPLEMENTS_NODE count: 1 (DEP-002-11-A01 -> SOW-0019)
- Status: PASS (exactly one parent anchor)

## Downstream Handoff Notes

### Consumer Context: TASK_ESTIMATING

The following notes are provided for downstream task-estimating workflows:

**BLOCKING dependencies (3 execution edges + 1 constraint):**
- **DEP-002-11-E01 (DEL-008-01 Geotech Report):** This is the single most significant dependency for estimating. The entire variable-price mechanism hinges on geotech results. Proposal-phase estimates proceed on assumed normal conditions; post-geotech, the foundation scope and cost may change materially. Estimators must account for two estimate scenarios: (a) proposal-phase assumed conditions, and (b) post-geotech revised conditions.
- **DEP-002-11-E02 (DEL-002-01 Preliminary Structural Design):** County approval of preliminary design gates IFC drawings. Estimating should account for a County review cycle before IFC can be finalized.
- **DEP-002-11-E04 (DEL-010-01 Foundation Construction):** DEL-002-11 produces the technical basis for foundation construction. Foundation construction cannot proceed without IFC drawings from this deliverable. This is a hard gate on the construction critical path.
- **DEP-002-11-E10 (RFP Document R-01):** The RFP establishes the variable-price contractual framework. All estimating must reference RFP section 4.8.2 for the boundary between firm-price and variable-price scope.

**ADVISORY dependencies (6 execution edges):**
- **DEP-002-11-E03 (DEL-002-02 Foundation Plan):** Foundation design feeds the drawing deliverable. Quantities for plan production depend on design completion.
- **DEP-002-11-E05 (DEL-001-02 Architectural Floor Plans):** Column grid and footprint confirmation affect footing layout. If architectural plans change, foundation design may require revision.
- **DEP-002-11-E06 (DEL-006-04 Cistern Details):** Cistern load is a material input to foundation load schedule. 50,000L full weight is significant; cistern location affects footing or slab design locally.
- **DEP-002-11-E07 (DEL-016-01 Crane Data):** Crane wheel loads and rail spacing affect crane column base design. If crane data is unavailable at proposal, assumed loads are used and flagged for revision.
- **DEP-002-11-E08 (DEL-002-10 Calculation Package):** Foundation calculations contribute to the broader structural calculation package. Estimating for DEL-002-10 should account for the foundation component.
- **DEP-002-11-E09 (DEL-002-08 Embedment Plan):** Steel plate embedment details require coordination between foundation design and the embedment plan deliverable.

**Key estimating consideration:** The variable-price nature of DEL-002-11 means that the proposal-phase estimate is inherently preliminary. The Structural Engineer's effort should be estimated in two phases: (1) proposal-phase design on assumed conditions (lighter effort), and (2) post-geotech IFC completion (full effort, potentially including re-design). The total effort depends on the delta between assumed and actual geotechnical conditions.
