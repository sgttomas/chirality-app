# Dependencies: DEL-001-08 Finish Schedule

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema)
- **Total ACTIVE rows:** 12
- **ANCHOR rows:** 3
- **EXECUTION rows:** 9

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-08-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-08-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-08-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (abbrev.) | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-001-08-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | County preliminary design approval gates IFC issue | BLOCKING |
| DEP-001-08-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | Room layout and IDs required before production begins | BLOCKING |
| DEP-001-08-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-05 Interior Elevations | Wall finish type/height must match | ADVISORY |
| DEP-001-08-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-06 Reflected Ceiling Plans | Ceiling finish type/height must match | ADVISORY |
| DEP-001-08-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | Product specs and flame spread ratings must correspond | ADVISORY |
| DEP-001-08-E06 | UPSTREAM | INTERFACE | PACKAGE | PKG-002 Structural Design | Mezzanine dead load and service trench cover coordination; structural engineer sign-off required | BLOCKING |
| DEP-001-08-E07 | UPSTREAM | INTERFACE | PACKAGE | PKG-006 Plumbing Design | Wash Bay drain/slope coordination | ADVISORY |
| DEP-001-08-E08 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code (NBC 2019 Alberta Edition) | Code compliance for all finish materials; occupancy classification required | BLOCKING |
| DEP-001-08-E09 | UPSTREAM | PREREQUISITE | UNKNOWN | Site Investigation Results (Old North Shop) | Substrate conditions required for B-series renovation finish selections | BLOCKING |

## Run Notes

### Run Parameters
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- loaded and validated
- **SCOPE:** DEL-001-08_Finish-Schedule

### Source Document Resolution (AUTO)
- **SOURCE_DOCS (AUTO):** `Datasheet.md`, `Specification.md`, `Procedure.md`, `Guidance.md`
- **ANCHOR_DOC (AUTO):** `Datasheet.md` -- selected as highest-confidence anchor doc (contains "Covers SOW" and "Supports Objectives" fields)
- **EXECUTION_DOC_ORDER (AUTO):** `Procedure.md` (primary -- contains explicit prerequisites and step gates), `Specification.md` (requirements and coordination statements), `Guidance.md` (considerations and trade-offs)
- **DOC_ROLE_MAP:** DEFAULT heuristic applied. Datasheet matched ANCHOR_DOC pattern; Procedure and Specification matched EXECUTION_DOC pattern; Guidance used as supplementary.
- **_REFERENCES.md:** Read. Contains R-01 (RFP) and R-04 (Appendix B Shop) references. Used for context; no additional dependency rows emitted solely from _REFERENCES.md.

### Defaults and Assumptions
- Decomposition was available and used for anchor validation and target resolution.
- All 3 ANCHOR rows confirmed against decomposition Section 5 (Objectives) and Section 7 (PKG-001 deliverables table).
- All deliverable target IDs (DEL-001-01, DEL-001-02, DEL-001-05, DEL-001-06, DEL-001-11) confirmed in decomposition Section 7 PKG-001 table.
- PKG-002 and PKG-006 confirmed in decomposition Section 6 Packages table.
- Site Investigation Results (E09) could not be resolved to a specific deliverable ID in the decomposition. Recorded as `TargetType=UNKNOWN`. The mandatory site meeting (RFP S3.2, March 3, 2026) and post-award investigation are referenced in Procedure P-PRE-01 but no formal deliverable ID exists for the investigation output.
- Alberta Building Code (E08) recorded as `TargetType=DOCUMENT` with `TargetLocation=location TBD` since the code text is not in project files.
- `SatisfactionStatus` set to `PENDING` for execution rows where the dependency is clearly not yet fulfilled (prerequisites not yet delivered). Set to `TBD` where status is unknown.

### Extraction Decisions
- **E01 (Preliminary Design):** Elevated from the earlier extraction. Evidence strengthened with Procedure P-PRE-01 gate reference (Step 7). Reclassified `SatisfactionStatus` from `TBD` to `PENDING`.
- **E02 (Floor Plans):** Elevated from the earlier extraction. Reclassified from INTERFACE to PREREQUISITE because Procedure P-PRE-01 explicitly identifies it as "Gate for Step 1" (a hard prerequisite, not just coordination). Evidence quote updated. `SatisfactionStatus` set to `PENDING`.
- **E03 (Interior Elevations):** Refreshed. Evidence file updated to Procedure.md Step 5.1. `EstimateImpactClass` adjusted from INFO to ADVISORY (coordination affects finish heights/types, which may influence material quantities).
- **E04 (Reflected Ceiling Plans):** New row. Extracted from Procedure Step 5.2 and Specification Documentation section. Explicit ceiling finish coordination requirement.
- **E05 (Architectural Specification):** New row. Extracted from Procedure Step 5.3 and Specification REQ-DS-006a, REQ-DS-008. Product spec correspondence and flame spread ratings.
- **E06 (Structural Design PKG-002):** New row. Extracted from Procedure P-PRE-01 (gate for Steps 3.5 and 3.7). Specification REQ-DS-010 requires written structural engineer confirmation for mezzanine. REQ-DS-003a requires trench cover coordination. Targeted at package level because multiple structural deliverables are involved (DEL-002-05 Mezzanine Details, DEL-002-06 Service Pit Details, DEL-002-08 Embedment Plan).
- **E07 (Plumbing Design PKG-006):** New row. Extracted from Procedure P-PRE-01 (gate for Step 3.3). Specification REQ-DS-005a. Targeted at package level.
- **E08 (Alberta Building Code):** New row. Extracted from Specification REQ-DS-007 and Procedure Step 4. External code document required as input for occupancy classification and flame spread thresholds.
- **E09 (Site Investigation):** New row. Extracted from Procedure P-PRE-01 (gate for Step 3.6, B-series only). Specification REQ-DS-011. No formal deliverable ID found in decomposition for site investigation output.

### Edges NOT Extracted (rationale)
- **R-01 (RFP) and R-04 (Appendix B):** These are reference documents available now, not information-flow dependencies. They are already in `_REFERENCES.md`. Not extracted as dependency rows.
- **Cross-coordination with DEL-001-02 for room ID consistency (Step 5.4):** Already captured in E02 (DEL-001-02 as prerequisite). The Step 5 cross-check is a verification activity, not a separate information-flow edge.
- **County aesthetic approval (Step 6):** This is a scheduling/approval gate, not an information-flow dependency from another deliverable. The prerequisite is already captured in E01 (Preliminary Design approval).
- **Guidance trade-offs (T-01, T-02, T-03):** Directional design considerations, not information-flow dependencies.
- **Occupancy classification (REQ-DS-007a):** This is an internal Architect determination, not an external dependency. The code input is captured in E08.

### Warnings
- None.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) -- loaded | None | 3 | 9 | Full extraction. 3 anchor + 9 execution rows. CONSUMER_CONTEXT=TASK_ESTIMATING. |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 12 (3 ANCHOR + 9 EXECUTION)
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown -- ACTIVE rows only)
- **TBD:** 6 (A01, A02, A03, E03, E04, E05)
- **PENDING:** 6 (E01, E02, E06, E07, E08, E09)
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following notes are provided for downstream task estimating workflows:

### Blocking Dependencies (gate estimating readiness)
1. **DEP-001-08-E01 (Preliminary Design):** Until County approves the Preliminary Design, the Finish Schedule cannot be issued for construction. Estimating should account for this approval gate in schedule assumptions.
2. **DEP-001-08-E02 (Floor Plans):** Room layout and IDs from DEL-001-02 are the first input to Finish Schedule production. Without confirmed room IDs, the schedule cannot be drafted. Estimating should sequence Finish Schedule production after Floor Plans reach coordination-issue maturity.
3. **DEP-001-08-E06 (Structural Design):** Structural engineer written sign-off is required for mezzanine finish dead load (REQ-DS-010) and service trench cover specification (REQ-DS-003a). These are hard gates for specific rows of the Finish Schedule. Estimating should account for structural coordination lead time.
4. **DEP-001-08-E08 (Alberta Building Code):** Occupancy classification must be determined before flame spread and smoke development thresholds can be populated. This is an Architect determination but requires code reference access. Estimating should flag occupancy classification as an early-design-development task.
5. **DEP-001-08-E09 (Site Investigation):** Old North Shop renovation area finishes (B-series) cannot be finalized without site investigation results. A-series (new addition) areas may proceed in parallel. Estimating should model B-series finish selection as a separate work stream gated by post-award site investigation.

### Advisory Dependencies (may affect quantities or approach)
6. **DEP-001-08-E03 (Interior Elevations):** Wall finish heights and partial-height treatments must be coordinated. Changes in interior elevations may affect material quantities for tile, FRP, or paint.
7. **DEP-001-08-E04 (Reflected Ceiling Plans):** Ceiling finish type changes affect material specification. 35 ft exposed-structure notation in Main Shop must be consistent.
8. **DEP-001-08-E05 (Architectural Specification):** Product specification correspondence affects procurement approach. Each finish product must have a matching section in DEL-001-11.
9. **DEP-001-08-E07 (Plumbing Design):** Wash Bay floor drain locations and slope requirements affect floor finish detailing and material quantities for slope/drain interface areas.

### Estimating Sequencing Recommendation
- **Phase 1 (can begin now):** Anchor resolution, preliminary finish category assignment for A-series areas based on available RFP and App B information.
- **Phase 2 (requires DEL-001-02 coordination issue):** Room list compilation, specific product selection for A-series areas.
- **Phase 3 (requires site investigation + structural coordination):** B-series finish selection, mezzanine finish confirmation, service trench cover specification.
- **Phase 4 (requires County Preliminary Design approval):** Final IFC issue.
