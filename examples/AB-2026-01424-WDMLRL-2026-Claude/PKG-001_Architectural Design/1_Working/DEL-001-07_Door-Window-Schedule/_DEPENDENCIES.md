# Dependencies: DEL-001-07 Door & Window Schedule

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema, 12 rows)
- **Summary:**
  - **ANCHOR rows:** 3 ACTIVE (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT)
  - **EXECUTION rows:** 9 ACTIVE (1 PREREQUISITE, 3 INTERFACE upstream/downstream, 1 CONSTRAINT, 2 HANDOVER, 2 additional INTERFACE)
  - **RETIRED rows:** 0

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-07-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-07-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-07-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | TargetID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|---|
| DEP-001-07-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH | BLOCKING |
| DEP-001-07-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 | Architectural Floor Plans | HIGH | ADVISORY |
| DEP-001-07-E03 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-03 | Power Distribution Plans | HIGH | ADVISORY |
| DEP-001-07-E04 | UPSTREAM | CONSTRAINT | EXTERNAL | -- | Camrose County Equipment Fleet Dimensions | HIGH | BLOCKING |
| DEP-001-07-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH | ADVISORY |
| DEP-001-07-E06 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH | ADVISORY |
| DEP-001-07-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 | Code Compliance Register & Inspection Log | MEDIUM | INFO |
| DEP-001-07-E08 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-06 | Panel Schedules | HIGH | ADVISORY |
| DEP-001-07-E09 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-001-11 | Architectural Specification | MEDIUM | INFO |

## Run Notes

### Defaults and Chosen Paths
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-07_Door-Window-Schedule`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents:
  1. Datasheet.md (ANCHOR_DOC)
  2. Specification.md (EXECUTION_DOC)
  3. Guidance.md (EXECUTION_DOC)
  4. Procedure.md (EXECUTION_DOC)
- **ANCHOR_DOC:** Datasheet.md (AUTO -- matched `datasheet` heuristic; contains Identification table with SOW/OBJ fields)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (AUTO -- Procedure matched `procedure` heuristic with highest workflow clarity; Specification matched `spec`; Guidance matched `guidance`)
- **_REFERENCES.md:** Present; used for document pointer resolution (R-01 and R-04 identified)

### Assumptions
- SOW-0011 is treated as the primary parent anchor (IMPLEMENTS_NODE) because the decomposition assigns DEL-001-07 to SOW-0011 as its primary scope item. SOW-0026 is also listed but SOW-0011 is the broader parent; SOW-0026 is a sub-scope item within the architectural design.
- DEL-002-03 (Structural Framing Plans) selected as the structural coordination target because the Procedure Reference Documents table explicitly names "DEL-002-03 Framing Plans" for structural opening coordination.
- DEL-003-02 (HVAC Layout Plans) selected as the mechanical coordination target because it is the primary HVAC deliverable in PKG-003 per the decomposition. The source text references "PKG-003" generally; DEL-003-02 is the most relevant specific deliverable for door-related thermal/HVAC data flow.
- E07 and E09 are DOWNSTREAM HANDOVER edges because Procedure Step 1.5 explicitly states code analysis output is "incorporated into" DEL-009-04 and DEL-001-11 -- this is a directional artifact transfer, not mere coordination.

### Warnings
- None.

### Integrity Check Results
- Parent anchor (IMPLEMENTS_NODE) count: 1 -- PASS
- DependencyID uniqueness: 12 unique IDs -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- Schema v3.1 enforced on all rows -- PASS
- No RETIRED rows (first full run) -- PASS

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1, 2026-02-25) | None | 3 | 9 | Initial extraction. CONSUMER_CONTEXT=TASK_ESTIMATING. 12 total ACTIVE rows. Extended from prior 8-row register to 12 rows with new E05-E09 edges. |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 12 (3 ANCHOR + 9 EXECUTION)
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown)
- **TBD:** 12
- **PENDING:** 0
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following dependencies are flagged as relevant for task estimating readiness:

### BLOCKING (gates meaningful estimating)
| DependencyID | Direction | Target | Statement |
|---|---|---|---|
| DEP-001-07-E01 | UPSTREAM | DEL-001-01 (Preliminary Architectural Design) | County approval of preliminary design required before IFC schedule can proceed. Estimating of DEL-001-07 effort is gated by the maturity of the preliminary design and Owner approval status. |
| DEP-001-07-E04 | UPSTREAM | External (Camrose County Equipment Fleet Dimensions) | Overhead door heights cannot be determined without Owner-provided motor scraper transport height. This blocks finalization of 3 of 12 door entries (D-OHD-01, D-OHD-02, D-OHD-03) and has significant cost implications for door procurement and structural header sizing. |

### ADVISORY (likely to affect quantities/specs)
| DependencyID | Direction | Target | Statement |
|---|---|---|---|
| DEP-001-07-E02 | UPSTREAM | DEL-001-02 (Floor Plans) | Schedule tag list depends on confirmed floor plans. Changes to room layout or door locations will change schedule content. |
| DEP-001-07-E03 | DOWNSTREAM | DEL-004-03 (Power Distribution Plans) | Motorized door operator specs flow to electrical design. Changes to door types or operator selections affect electrical scope. |
| DEP-001-07-E05 | UPSTREAM | DEL-002-03 (Structural Framing Plans) | Structural clearance of openings may constrain door sizes or locations. |
| DEP-001-07-E06 | DOWNSTREAM | DEL-003-02 (HVAC Layout Plans) | Door sizes affect HVAC makeup air and heating load calculations. |
| DEP-001-07-E08 | DOWNSTREAM | DEL-004-06 (Panel Schedules) | Motorized door data must appear in panel schedules; operator selections affect circuit sizing. |

### INFO (low likelihood of changing totals)
| DependencyID | Direction | Target | Statement |
|---|---|---|---|
| DEP-001-07-E07 | DOWNSTREAM | DEL-009-04 (Code Compliance Register) | Code analysis output feeds compliance register; informational for estimating. |
| DEP-001-07-E09 | DOWNSTREAM | DEL-001-11 (Architectural Specification) | Code findings and product standard selections feed into spec; informational for estimating. |

### Estimating Readiness Assessment
- DEL-001-07 has **2 BLOCKING dependencies** that must be resolved before high-confidence estimating is possible.
- The Owner equipment fleet dimensions (E04) are the single most critical input: without motor scraper transport height, door heights for the three largest openings remain TBD, making accurate door procurement cost estimating impossible.
- The preliminary design approval (E01) gates the overall workflow but is a standard project milestone dependency.
- All 5 ADVISORY dependencies represent normal design coordination interfaces that will refine but not fundamentally change the estimating scope.
