# DEL-018-01_Topsoil-Strip | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Last Run**: 2026-02-26

---

## Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| SITE-ACCESS-001 | Site access and mobilization area | Pending | Site must be accessible for equipment |
| SURVEY-001 | Site survey and topsoil depth assessment | Pending | Determine excavation depth and volume |
| UTILITIES-001 | Utility location marking | Pending | Identify and mark underground utilities |

## Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| DEL-018-02 | Site Grading & Landscaping | Pending | Requires bare ground for grading work |
| DEL-018-03 | Gravel Driving Surface | Pending | Grading must be complete before surfacing |
| DEL-018-04 | Cement & Gravel Pads | Pending | Grading prerequisite for pad construction |
| DEL-018-05 | Wash Bay Drainage | Pending | Requires prepared ground surface |
| DEL-018-06 | Utility Tie-Ins | Pending | Utility work requires clear ground access |

---

## Extracted Dependency Register

**Total rows:** 13 (13 ACTIVE, 0 RETIRED)

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|
| DEP-018-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0075 -- Strip topsoil from all driving surfaces | HIGH | ACTIVE |
| DEP-018-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 -- Deliver a code-compliant fully functional maintenance shop addition | HIGH | ACTIVE |

### EXECUTION Edges -- Upstream (Information/Artifact Inputs)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass | Status |
|---|---|---|---|---|---|---|
| DEP-018-01-003 | PREREQUISITE | UNKNOWN | SURVEY-001 -- Site Survey and Topsoil Depth Assessment | HIGH | BLOCKING | ACTIVE |
| DEP-018-01-004 | CONSTRAINT | UNKNOWN | UTILITIES-001 -- Underground Utility Locate and Marking | HIGH | BLOCKING | ACTIVE |
| DEP-018-01-005 | PREREQUISITE | UNKNOWN | SITE-ACCESS-001 -- Site Access and Mobilization Area Preparation | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-006 | PREREQUISITE | EXTERNAL | SOW-0200 -- County Brushing and Clearing of Project Area | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-007 | PREREQUISITE | DELIVERABLE | DEL-005-02 -- Site Grading Plan (IFC Drawings) | HIGH | BLOCKING | ACTIVE |
| DEP-018-01-008 | INTERFACE | DOCUMENT | R-07 -- Appendix C - Site Maps | MEDIUM | INFO | ACTIVE |

### EXECUTION Edges -- Downstream (Information/Artifact Outputs)

| DependencyID | DependencyType | TargetType | Target | Confidence | EstimateImpactClass | Status |
|---|---|---|---|---|---|---|
| DEP-018-01-009 | HANDOVER | DELIVERABLE | DEL-018-02 -- Site Grading and Landscaping | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-010 | HANDOVER | DELIVERABLE | DEL-018-03 -- Gravel Driving Surface | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-011 | HANDOVER | DELIVERABLE | DEL-018-04 -- Cement and Gravel Pads | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-012 | HANDOVER | DELIVERABLE | DEL-018-05 -- Wash Bay Drainage and Mud Sump | HIGH | ADVISORY | ACTIVE |
| DEP-018-01-013 | HANDOVER | DELIVERABLE | DEL-018-06 -- Utility Tie-Ins | HIGH | ADVISORY | ACTIVE |

---

## Run Notes

### Run Configuration
- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO (resolved below)
- **ANCHOR_DOC:** Datasheet.md (selected: filename contains "datasheet", highest-confidence anchor signal)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md, Datasheet.md (selected: Procedure highest workflow clarity, then Specification for requirements, then Guidance for considerations)
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (file located and used successfully)
- **_REFERENCES.md:** Present and used for R-07 document pointer resolution

### Decomposition Validation
- SOW-0075 confirmed in decomposition scope ledger (§J, line SOW-0075 -> PKG-018 -> DEL-018-01, OBJ-001, D-010)
- OBJ-001 confirmed in decomposition objectives (§5)
- DEL-005-02 confirmed in decomposition (PKG-005, Site Grading Plan, Civil Engineer)
- DEL-018-02 through DEL-018-06 confirmed in decomposition (PKG-018 deliverables table)
- SOW-0200 confirmed in decomposition scope boundaries (County-responsibility, brushing and clearing)

### Source Document Scan
All four production documents were scanned:
1. **Datasheet.md** -- primary anchor signals (SOW-0075, OBJ-001, DEL-005-02 references, downstream sequence, upstream preconditions)
2. **Specification.md** -- requirements REQ-018-01-01 through REQ-018-01-10 with explicit prerequisite/constraint statements
3. **Guidance.md** -- principles confirming safety-critical nature of UTILITIES-001, IFC drawing dependency, clearing precedence, site map dependency
4. **Procedure.md** -- prerequisites table with 8 explicit preconditions; execution steps referencing all upstream inputs

### Extraction Decisions
- **SURVEY-001, UTILITIES-001, SITE-ACCESS-001:** These are referenced by symbolic IDs but not mapped to specific deliverables in the decomposition. Set as TargetType=UNKNOWN per CONSERVATIVE strictness. They may resolve to deliverables or external activities in a future reconciliation pass.
- **SOW-0200 (County Brushing/Clearing):** Set as TargetType=EXTERNAL because this is a County responsibility, not a Proponent deliverable.
- **R-07 (Site Maps):** Set as TargetType=DOCUMENT and DependencyType=INTERFACE because the maps provide informational input (clearing limits, topography) rather than gating execution.
- **Downstream DEL-018-02 through DEL-018-06:** All typed as HANDOVER because DEL-018-01 produces the stripped subgrade surface that these deliverables explicitly consume.
- **Procedure prerequisites SEASONAL-001, COUNTY-PROTOCOL, OH&S-PLAN, IFC-DRAWINGS:** These are operational/coordination prerequisites that do not represent distinct information/artifact transfers from identifiable source entities. SEASONAL-001 is a weather condition, COUNTY-PROTOCOL is a coordination setup, OH&S-PLAN is an internal document. IFC-DRAWINGS is already captured as DEP-018-01-007 (DEL-005-02). Per information-flow-only extraction rule, these are not emitted as separate dependency rows.
- **EstimateImpactClass:** Set BLOCKING for SURVEY-001 (depth drives volume calculation -- core estimating input), UTILITIES-001 (safety-critical gate), and DEL-005-02 (defines stripping extent -- core estimating input). Set ADVISORY for SITE-ACCESS-001 and SOW-0200 (affect schedule but do not change scope/quantities). Set INFO for R-07 (informational context, low likelihood of changing estimating totals).

### Warnings
None. All integrity checks passed:
- Exactly 1 ACTIVE IMPLEMENTS_NODE anchor (no FLOATING_NODE or AMBIGUOUS_ANCHOR)
- All DependencyIDs unique (13/13)
- All ACTIVE rows have EvidenceFile and SourceRef
- CSV parseable with 31 columns (29 required + 2 extension)

---

## Run History

| Run Date | Mode | Strictness | Consumer Context | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (located) | None | 2 | 11 | 13 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total Rows | 13 |
| ACTIVE | 13 |
| RETIRED | 0 |

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 11 | 0 |

### Closure State Breakdown (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| PENDING | 8 |
| TBD | 5 |
| NOT_APPLICABLE | 2 |

Note: ANCHOR rows use SatisfactionStatus=NOT_APPLICABLE (traceability links, not closure-gated). Upstream EXECUTION rows are PENDING (awaiting fulfillment). Downstream EXECUTION rows are TBD (closure depends on DEL-018-01 completion and handoff acceptance by target deliverables).

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant to downstream task estimating workflows:

### Estimating-Blocking Dependencies (3 rows)
These dependencies must be resolved before meaningful estimating of DEL-018-01 can proceed:

1. **DEP-018-01-003 (SURVEY-001):** Topsoil depth is unknown. Depth drives the volume calculation (Volume = Area x Depth), which is the primary quantity for this deliverable. Without survey data, volume is TBD and equipment selection/duration cannot be estimated with confidence. **Estimating impact: quantity and duration.**

2. **DEP-018-01-004 (UTILITIES-001):** Utility locate is a safety-critical constraint. While it does not directly change quantities, failure to complete it before excavation is a hard stop. **Estimating impact: schedule gate.**

3. **DEP-018-01-007 (DEL-005-02 -- IFC Site Grading Plan):** Stripping area limits are defined by IFC drawings. Without them, the area component of the volume calculation is TBD. "All driving surfaces" scope extent is ambiguous (see Conflict Table CFT-002). **Estimating impact: quantity (area) and scope definition.**

### Estimating-Advisory Dependencies (7 rows)
These dependencies may affect quantities, approach, or procurement but are not hard gates:

- **DEP-018-01-005 (SITE-ACCESS-001):** Affects mobilization timing and equipment access route planning.
- **DEP-018-01-006 (SOW-0200):** County clearing must complete first; timing affects Proponent schedule but not quantities.
- **DEP-018-01-009 through DEP-018-01-013 (Downstream handoffs):** These inform the sequencing and resource planning for the five downstream DEL-018-xx deliverables. The stripped subgrade quality and stockpile condition affect DEL-018-02 estimating in particular.

### Key TBD Items Affecting Estimating
- Topsoil depth: TBD (blocked on SURVEY-001)
- Stripping area: TBD (blocked on DEL-005-02 IFC drawings)
- Volume of topsoil: TBD (dependent on both depth and area)
- Stockpile location: TBD (affects hauling distance/duration)
- Equipment type: TBD (dependent on depth and area)

---

## Critical Path Assessment
- **On Critical Path**: YES
- **Justification**: Foundational sitework activity that must be completed before all other DEL-018 deliverables can proceed; critical for project schedule

## Interdependency Matrix

### Within PKG-018
- Upstream to all other sitework deliverables (DEL-018-02 through 06)
- Critical path item determining project timeline
- Proper site preparation essential for efficiency of subsequent work

### Cross-Package Dependencies
- Requires IFC drawings from PKG-005 (Civil Design) -- DEL-005-02
- Requires site maps from design documentation package (R-07)
