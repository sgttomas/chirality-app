# Deliverable Dependencies: DEL-006-04

**Deliverable ID:** DEL-006-04
**Name:** Cistern & Pump Details
**Package:** PKG-006 -- Plumbing Design

---

## Declared Upstream Dependencies

*Human-owned section. Add manually identified upstream dependencies here.*

- DEL-006-01 (Preliminary Plumbing Design) -- required before IFC issue
- DEL-001-02 (Architectural Floor Plans) -- required for spatial coordination
- DEL-002 (Structural Design package) -- cistern installation type and structural loads
- DEL-008-01 (Geotech Report) -- required if cistern is below-grade
- DEL-004 (Electrical Design) -- pump electrical interface coordination
- DEL-005-02 (Site Grading Plan) -- bulk fill point and overflow drainage
- DEL-006-06 (Plumbing Fixture Schedule) -- peak daily water demand for cistern sizing

## Declared Downstream Dependencies

*Human-owned section. Add manually identified downstream dependencies here.*

- DEL-006-02 (Water Distribution Plans) -- cistern feeds building distribution
- DEL-006-03 (Drain & Vent Plans) -- cistern overflow and drain connections
- DEL-006-07 (Plumbing Calculation Package) -- cistern volume and pump TDH calculations
- DEL-004-06 (Panel Schedules) -- pump motor load data for electrical panel
- DEL-009-03 (Safety Code Permits) -- IFC drawings for plumbing permit application

---

## Extracted Dependency Register

**Register Schema Version:** v3.1
**Total ACTIVE rows:** 18
**Total RETIRED rows:** 0

### ANCHOR Edges (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-006-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0016 | Complete final plumbing design (water supply, drainage, septic) | HIGH |
| DEP-006-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-006-04-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-006-04-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | Install and commission all mechanical, plumbing, and water storage systems | HIGH |

### EXECUTION Edges (14 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-04-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | Preliminary Plumbing Design (DEL-006-01) | HIGH | BLOCKING |
| DEP-006-04-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | Architectural Floor Plans (DEL-001-02) | HIGH | BLOCKING |
| DEP-006-04-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | Structural Design package (DEL-002) | HIGH | BLOCKING |
| DEP-006-04-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | Geotechnical Investigation & Report (DEL-008-01) | HIGH | BLOCKING |
| DEP-006-04-009 | UPSTREAM | INTERFACE | DELIVERABLE | Electrical Design (DEL-004) | HIGH | ADVISORY |
| DEP-006-04-010 | UPSTREAM | PREREQUISITE | DELIVERABLE | Site Grading Plan (DEL-005-02) | HIGH | ADVISORY |
| DEP-006-04-011 | DOWNSTREAM | INTERFACE | DELIVERABLE | Water Distribution Plans (DEL-006-02) | HIGH | ADVISORY |
| DEP-006-04-012 | DOWNSTREAM | INTERFACE | DELIVERABLE | Drain & Vent Plans (DEL-006-03) | HIGH | ADVISORY |
| DEP-006-04-013 | DOWNSTREAM | HANDOVER | DELIVERABLE | Plumbing Calculation Package (DEL-006-07) | HIGH | ADVISORY |
| DEP-006-04-014 | UPSTREAM | PREREQUISITE | DOCUMENT | AB-2026-01424-WDMLRL RFP.pdf | HIGH | INFO |
| DEP-006-04-015 | UPSTREAM | PREREQUISITE | DOCUMENT | AB-2026-01424-Appendix B (Plumbing).pdf | HIGH | INFO |
| DEP-006-04-016 | DOWNSTREAM | INTERFACE | DELIVERABLE | Panel Schedules (DEL-004-06) | HIGH | ADVISORY |
| DEP-006-04-017 | DOWNSTREAM | ENABLES | DELIVERABLE | Safety Code Permits (DEL-009-03) | MEDIUM | INFO |
| DEP-006-04-018 | UPSTREAM | INTERFACE | DELIVERABLE | Plumbing Fixture Schedule (DEL-006-06) | MEDIUM | ADVISORY |

---

## Run Notes

### Run: 2026-02-26

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md -- matched "datasheet" heuristic; contains Identification table with SOW Reference and Objectives Supported fields)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Guidance.md, Specification.md, Datasheet.md -- Procedure ranked first as primary workflow/prerequisite source; Guidance second for design-basis cross-references; Specification third; Datasheet fourth for interface table)
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found; R1 2026-02-25)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic used
- _REFERENCES.md: read; used to confirm document locations (_Sources/) for R-01 and R-06

**Warnings:**
- None

**Assumptions recorded in extraction:**
- DEP-006-04-007: Procedure references "DEL-002 (Structural Design package)" generically; resolved to DEL-002-02_Foundation-Plan as the most relevant structural deliverable for cistern foundation/slab coordination. Actual interface may span multiple PKG-002 deliverables.
- DEP-006-04-009: Procedure references "DEL-004 (Electrical Design)" generically; resolved to DEL-004-03_Power-Plans as the most relevant electrical deliverable for pump power coordination. Actual interface may span multiple PKG-004 deliverables.
- DEP-006-04-008: Geotech prerequisite is conditional ("Required if cistern is below-grade"). Registered as BLOCKING because cistern installation type is currently TBD.

**Target resolution notes:**
- All deliverable targets resolved against decomposition section 7 deliverable tables.
- SOW-0016 confirmed in decomposition section 3 (SSOW) and section 8 (Scope Ledger).
- OBJ-001, OBJ-003, OBJ-004 confirmed in decomposition section 5 (Objectives) and section 7 PKG-006 row.
- Document targets (RFP, Appendix B Plumbing) resolved via _REFERENCES.md to _Sources/ directory.

---

## Run History

| Timestamp | Mode | Strictness | ConsumerContext | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (R1) | None | 4 | 14 | 18 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| Total ACTIVE | 18 |
| Total RETIRED | 0 |
| ANCHOR / ACTIVE | 4 |
| EXECUTION / ACTIVE | 14 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 9 |

*Note: PENDING status assigned to upstream prerequisites and document inputs where the required information/artifact has not yet been confirmed as received. TBD assigned to downstream interfaces, handovers, and anchors where satisfaction tracking is not yet initialized.*

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for downstream task-estimating workflows:

### Blocking Dependencies (4 rows)

These upstream dependencies are classified as BLOCKING for estimating purposes because they gate scope definition or key design parameters that affect quantities:

1. **DEP-006-04-005 -- DEL-006-01 (Preliminary Plumbing Design):** County approval of preliminary design is a formal project gate before final IFC design can proceed. Without this, the scope and configuration of the cistern/pump system is not confirmed.

2. **DEP-006-04-006 -- DEL-001-02 (Architectural Floor Plans):** Utility room dimensions and building layout directly affect cistern spatial constraints. Without floor plans, cistern type (above-grade vs. below-grade) and available footprint cannot be confirmed.

3. **DEP-006-04-007 -- DEL-002 (Structural Design):** Slab details, structural capacity, and foundation design determine whether an in-slab or below-grade cistern is feasible. This directly affects cistern material selection and installation method, which are major cost drivers.

4. **DEP-006-04-008 -- DEL-008-01 (Geotech Report):** Conditional on cistern installation type. If cistern is below-grade, geotech conditions determine excavation, waterproofing, and material requirements. Currently TBD -- cistern installation type is unresolved (see CONF-001 in Guidance.md).

### Advisory Dependencies (8 rows)

These dependencies are likely to affect quantities, specifications, or procurement approach but do not hard-gate estimating:

- Electrical interface (DEL-004, DEL-004-06): pump circuit sizing affects electrical scope/cost but does not block plumbing estimating.
- Site grading (DEL-005-02): affects bulk fill point location and overflow drainage path.
- Downstream interfaces (DEL-006-02, DEL-006-03, DEL-006-07): design outputs from this deliverable consumed by sibling plumbing deliverables.
- Fixture schedule (DEL-006-06): peak daily demand input for cistern volume adequacy -- may increase cistern size above 50,000 L minimum.

### Key Estimating Risks

- **Cistern installation type is TBD** (CONF-001): above-grade vs. below-grade has significant cost implications (excavation, waterproofing, insulation, structural support). Estimating should carry contingency or dual scenarios until resolved.
- **Pump identity ambiguity** (CONF-002): whether the 100 LPM distribution pump is the same as the "fire hose pump" (70A circuit) affects circuit count and pump procurement scope.
- **Water quality classification** (C-003): if potable water treatment is required, scope and cost increase materially.
