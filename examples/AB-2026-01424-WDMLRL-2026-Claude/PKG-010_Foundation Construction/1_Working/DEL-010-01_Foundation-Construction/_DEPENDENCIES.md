# Dependencies: DEL-010-01 Foundation Construction

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending — to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) — human-owned declarations
- PKG-008 Geotechnical Investigation & Surveying — Geotechnical report and site survey findings
- Dependencies coordinated externally by humans.

## Downstream (These need me) — human-owned declarations
- PKG-011 Building Structure & Envelope — Foundational support for superstructure
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

**Status:** COMPLETE
**Register file:** `Dependencies.csv` (v3.1 schema)
**Total ACTIVE rows:** 16

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-010-01-A01 | IMPLEMENTS_NODE | SOW-0023 | SOW-0023 — Construct foundation | HIGH |
| DEP-010-01-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001 — Functional Facility | HIGH |
| DEP-010-01-A03 | TRACES_TO_REQUIREMENT | OBJ-002 | OBJ-002 — Schedule Compliance | HIGH |
| DEP-010-01-A04 | TRACES_TO_REQUIREMENT | OBJ-006 | OBJ-006 — Geotechnical Risk Management | HIGH |

### EXECUTION Dependencies (12 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-010-01-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | HIGH | BLOCKING |
| DEP-010-01-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-11 Foundation Design Package | HIGH | BLOCKING |
| DEP-010-01-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-02 Foundation Plan | HIGH | BLOCKING |
| DEP-010-01-E04 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-02 Building Permit | HIGH | BLOCKING |
| DEP-010-01-E05 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-009-03 Safety Code Permits | HIGH | BLOCKING |
| DEP-010-01-E06 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-03 Construction Survey | MEDIUM | ADVISORY |
| DEP-010-01-E07 | UPSTREAM | CONSTRAINT | EXTERNAL | County bulk cut and fill | HIGH | BLOCKING |
| DEP-010-01-E08 | UPSTREAM | CONSTRAINT | EXTERNAL | County brushing and clearing | HIGH | BLOCKING |
| DEP-010-01-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-06 Service Pit Structural Details | MEDIUM | ADVISORY |
| DEP-010-01-E10 | UPSTREAM | CONSTRAINT | EXTERNAL | County aggregate supply | MEDIUM | ADVISORY |
| DEP-010-01-E11 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-011 Building Structure & Envelope | HIGH | BLOCKING |
| DEP-010-01-E12 | UPSTREAM | CONSTRAINT | EXTERNAL | Variable-price negotiation (commercial gate) | HIGH | BLOCKING |

## Run Notes

### Defaults and Chosen Paths
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 — 2026-02-25)
- **DECOMPOSITION_STATUS:** Available and validated
- **ANCHOR_DOC:** `Datasheet.md` (selected by DOC_ROLE_MAP heuristic — contains "datasheet")
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Guidance.md`, `Specification.md` (selected by DOC_ROLE_MAP heuristic)
- **SOURCE_DOCS scanned:** `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- **_REFERENCES.md:** Read; used to confirm document pointers (R-01, R-04 locations)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING

### Warnings
- None. No integrity warnings triggered.

### Assumptions Logged
- **DEP-010-01-E06:** PRE-09 (Construction Survey) is marked ASSUMPTION in source; survey control point dependency is inferred from Procedure Step 7 but not stated as an explicit RFP requirement.
- **DEP-010-01-E09:** Service pit scope boundary is TBD per Conflict Table CF-010-01; the interface dependency is extracted because the source explicitly states the structural details must be incorporated, but scope ownership is unresolved.
- **DEP-010-01-E10:** Aggregate timing dependency is ASSUMPTION; the County supplies aggregate (FACT per RFP §3.3.1) but the timing impact on foundation sequencing is inferred from Guidance C-4.
- **Objective mapping (A02-A04):** Objectives are marked as ASSUMPTION in Datasheet.md ("best-effort mapping per package heuristic") but are confirmed in Decomposition §7 PKG-010 deliverable table, so recorded as FACT in the register.

## Run History

| Run | Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1 2026-02-25) | None | 4 | 12 | 16 |

## Lifecycle Summary

| Lifecycle State | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 4 (all ANCHOR rows) |
| PENDING | 12 (all EXECUTION rows) |

| Confidence | Count |
|---|---|
| HIGH | 13 |
| MEDIUM | 3 |

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Critical Dependencies

The following EXECUTION dependencies are classified as **BLOCKING** for task estimating (9 of 12 execution rows):

1. **DEP-010-01-E01 (Geotech Report):** Foundation type, depth, and reinforcement are unknown until this is received. All quantity takeoffs and cost estimates for foundation work are blocked. This is the highest-priority upstream dependency.
2. **DEP-010-01-E02 (Foundation Design Package):** Design drawings define the scope of concrete, formwork, reinforcement, and embedded items. Without this package, no reliable quantity takeoff is possible.
3. **DEP-010-01-E03 (Foundation Plan):** IFC drawings required for dimensional takeoffs and layout.
4. **DEP-010-01-E04 (Building Permit):** Construction gate; affects mobilization timing but not quantity estimation.
5. **DEP-010-01-E05 (Safety Code Permits):** Construction gate; affects mobilization timing but not quantity estimation.
6. **DEP-010-01-E07 (County Bulk Cut/Fill):** External constraint on site readiness; timing affects mobilization planning.
7. **DEP-010-01-E08 (County Clearing):** External constraint on site readiness; timing affects mobilization planning.
8. **DEP-010-01-E11 (Handover to PKG-011):** Foundation completion is on the critical path for all superstructure work; schedule float between PKG-010 and PKG-011 is TBD and affects overall project risk.
9. **DEP-010-01-E12 (Variable-Price Negotiation):** Commercial gate; final pricing cannot be established until geotech report is available.

### Advisory Dependencies (3 of 12 execution rows):

- **DEP-010-01-E06 (Construction Survey):** Survey control points needed for layout but does not directly block quantity estimation.
- **DEP-010-01-E09 (Service Pit Details):** Scope boundary TBD per CF-010-01; may affect quantities if service pit is in PKG-010 scope.
- **DEP-010-01-E10 (Aggregate Supply):** Timing dependency; does not affect quantities but may affect construction sequencing.

### Key Estimating Insight

DEL-010-01 is a **variable-price scope item** (RFP §4.8.2). The preliminary estimate is based on assumed normal ground conditions. The actual scope, quantities, and cost are gated by the geotechnical report (E01) and Foundation Design Package (E02). Any task estimate produced before these dependencies are satisfied must be explicitly flagged as preliminary/placeholder with significant uncertainty range.
