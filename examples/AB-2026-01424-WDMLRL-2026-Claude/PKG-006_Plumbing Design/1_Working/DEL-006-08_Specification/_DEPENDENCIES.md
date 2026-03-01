# Deliverable Dependencies: DEL-006-08

**Deliverable ID:** DEL-006-08
**Name:** Plumbing Specification
**Package:** PKG-006 -- Plumbing Design
**Register Schema:** v3.1

---

## Declared Upstream Dependencies

_Human-owned. Edit this section manually as dependencies are identified._

- DEL-008-01 (Geotechnical Investigation & Report) -- cistern foundation and septic installation conditions
- DEL-008-02 (Preliminary Site Survey) -- existing septic tank location
- DEL-001-02 (Architectural Floor Plans) -- washroom/locker room/wash station layouts
- DEL-002-02 (Foundation Plan) -- slab penetrations, cistern support, sump pit, roof penetrations
- DEL-003-07 (Mechanical Specification) -- heating zones, freeze-risk, vent routing coordination
- DEL-004-09 (Electrical Specification) -- pump circuits, emergency shower alarm, hot water heater power
- DEL-006-01 (Preliminary Plumbing Design) -- County approval required before final specification
- DEL-006-06 (Plumbing Fixture Schedule) -- fixture types and flow rates
- DEL-006-07 (Plumbing Calculation Package) -- pipe sizing and flow calculations
- R-01 (RFP) -- primary plumbing scope and requirements source
- R-06 (Appendix B Plumbing) -- conceptual plumbing layout and fixture locations
- County preliminary plumbing design approval (SOW-0010f)
- Alberta Safety Codes (Plumbing Code) -- regulatory compliance constraint

## Declared Downstream Dependencies

_Human-owned. Edit this section manually as dependencies are identified._

- PKG-014 (Plumbing & Water Systems Installation) -- governing specification for construction execution
- DEL-006-02 through DEL-006-05 (Drawing Sets) -- governed by this specification

---

## Extracted Dependency Register

**Register Schema Version:** v3.1
**Total ACTIVE rows:** 21
**Total RETIRED rows:** 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-006-08-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0016 | Complete final plumbing design (water supply; drainage; septic) | HIGH |
| DEP-006-08-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |
| DEP-006-08-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | Install and commission all mechanical/plumbing/water storage systems to operational readiness | HIGH |

### EXECUTION Rows (18 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|---|
| DEP-006-08-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation & Report | BLOCKING | HIGH |
| DEP-006-08-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | BLOCKING | HIGH |
| DEP-006-08-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | BLOCKING | HIGH |
| DEP-006-08-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-002-02 Foundation Plan | BLOCKING | HIGH |
| DEP-006-08-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-07 Mechanical Specification | ADVISORY | MEDIUM |
| DEP-006-08-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-09 Electrical Specification | ADVISORY | MEDIUM |
| DEP-006-08-010 | UPSTREAM | CONSTRAINT | EXTERNAL | County preliminary design approval | BLOCKING | HIGH |
| DEP-006-08-011 | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 AB-2026-01424-WDMLRL RFP.pdf | INFO | HIGH |
| DEP-006-08-012 | UPSTREAM | PREREQUISITE | DOCUMENT | R-06 AB-2026-01424-Appendix B (Plumbing).pdf | INFO | HIGH |
| DEP-006-08-013 | DOWNSTREAM | HANDOVER | PACKAGE | PKG-014 Plumbing & Water Systems Installation | BLOCKING | HIGH |
| DEP-006-08-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | ADVISORY | MEDIUM |
| DEP-006-08-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-07 Civil Specification | ADVISORY | MEDIUM |
| DEP-006-08-016 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | ADVISORY | MEDIUM |
| DEP-006-08-017 | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-006-02 Water Distribution Plans | INFO | HIGH |
| DEP-006-08-018 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-07 Plumbing Calculation Package | BLOCKING | HIGH |
| DEP-006-08-019 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-06 Plumbing Fixture Schedule | ADVISORY | HIGH |
| DEP-006-08-020 | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Safety Codes (Plumbing Code) | BLOCKING | HIGH |
| DEP-006-08-021 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-01 Preliminary Plumbing Design | BLOCKING | HIGH |

---

## Run Notes

### Invocation Parameters

| Parameter | Value |
|---|---|
| SCOPE | DEL-006-08_Specification |
| RUN_ROOT | PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification |
| MODE | UPDATE |
| STRICTNESS | CONSERVATIVE |
| CONSUMER_CONTEXT | TASK_ESTIMATING |
| SOURCE_DOCS | AUTO |
| ANCHOR_DOC | AUTO (resolved: Datasheet.md) |
| EXECUTION_DOC_ORDER | AUTO (resolved: Procedure.md, Guidance.md, Specification.md) |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md |
| Decomposition status | Available; validated. R1 -- 2026-02-25 |

### Source Document Role Resolution

- **ANCHOR_DOC:** `Datasheet.md` -- selected by AUTO heuristic (filename matches `datasheet` pattern; contains explicit SOW-0016 / OBJ-003 / OBJ-004 identifiers in Identification table).
- **EXECUTION_DOC_ORDER:**
  1. `Procedure.md` -- highest workflow clarity; contains explicit Prerequisites table (P-01 through P-09) and phased Steps with deliverable cross-references.
  2. `Guidance.md` -- contains Coordinated Disciplines section with explicit interface descriptions and Conflict Table.
  3. `Specification.md` -- contains Requirements tables with cross-references to other deliverables (DEL-006-06, DEL-006-07) and downstream handover statement (PKG-014).
- **Excluded from scanning:** `_CONTEXT.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`, `_STATUS.md` (generated/scaffold artifacts).

### Assumptions and Decisions

- ANCHOR resolution: SOW-0016 confirmed in Decomposition S3 (SSOW) and S8 (Scope Ledger). OBJ-003 and OBJ-004 confirmed in Decomposition S5 (Objectives) and S7 (PKG-006 deliverables table).
- Procedure P-04 references "DEL-002-02 et seq." -- resolved to DEL-002-02 as lead structural drawing target. The full structural set (DEL-002-02 through DEL-002-10) is implied but only the lead deliverable is registered to avoid redundancy.
- Procedure P-05 references "DEL-003" generically -- resolved to DEL-003-07 (Mechanical Specification) as the most relevant single interface deliverable. Confidence set to MEDIUM.
- Procedure P-06 references "DEL-004" generically -- resolved to DEL-004-09 (Electrical Specification) as the most relevant single interface deliverable. Confidence set to MEDIUM.
- Guidance Coordinated Disciplines references PKG-002, PKG-005, PKG-001 as interfaces -- resolved to their respective Specification deliverables (DEL-002-12, DEL-005-07, DEL-001-11). These supplement the prerequisite-level dependency on DEL-002-02 (structural drawings) already captured.
- DEL-006-08 Documentation section lists DEL-006-02 through DEL-006-05 as governed drawing sets. Registered as a single DOWNSTREAM/ENABLES row targeting DEL-006-02 to represent the set without redundancy.
- Document dependencies (R-01, R-06) marked SATISFIED based on _REFERENCES.md confirming availability in _Sources/.

### Warnings

_(None)_

### Integrity Check Results

| Check | Result |
|---|---|
| Parent anchor (IMPLEMENTS_NODE) count | 1 (PASS) |
| DependencyID uniqueness | All 21 IDs unique (PASS) |
| ACTIVE rows with EvidenceFile + SourceRef | 21/21 (PASS) |
| Enum canonicality | All values canonical (PASS) |
| CSV parseability | 31 columns, 21 data rows (PASS) |
| FromDeliverableID consistency | All rows = DEL-006-08 (PASS) |
| RegisterSchemaVersion | All rows = v3.1 (PASS) |
| TargetDeliverableID placement | Non-deliverable targets have empty TargetDeliverableID; deliverable targets have populated TargetDeliverableID (PASS) |

### Items Not Extracted (conservative exclusions)

- Specification exclusions section lists PKG-003, PKG-004, PKG-002, PKG-005, PKG-014 as out-of-scope disciplines. These are structural adjacency statements (not information-flow dependencies) and are not extracted per protocol.
- Procedure Step 3.7 references interdisciplinary coordination with five disciplines. The coordination requirement is already captured through the interface dependencies (DEP-006-08-008, 009, 014, 015, 016) and prerequisite dependencies (DEP-006-08-006, 007). No additional rows warranted.
- Guidance Trade-offs section contains design decision options (cistern material, drain routing, freeze protection, hot water source, emergency shower supply). These are internal design decisions, not information-flow dependencies.
- Guidance Conflict Table items (CON-PLB-001, 002, 003) are internal design conflicts requiring human ruling. County confirmation of CON-PLB-003 (septic removal) is already captured through the broader County approval constraint (DEP-006-08-010).

---

## Run History

| Timestamp | Mode | Strictness | Consumer Context | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (R1 -- 2026-02-25) | None | 3 | 18 | 21 |

---

## Lifecycle Summary

### Extraction Lifecycle

| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 19 |
| SATISFIED | 2 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

### Confidence Distribution (ACTIVE rows)

| Confidence | Count |
|---|---|
| HIGH | 16 |
| MEDIUM | 5 |
| LOW | 0 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Summary for Estimating

DEL-006-08 (Plumbing Specification) has **9 BLOCKING dependencies** that gate meaningful estimating readiness:

1. **DEP-006-08-004** (DEL-008-01 Geotechnical Investigation) -- Required to inform cistern foundation/support design and septic tank installation conditions. Without geotech data, cistern and septic scope quantities remain uncertain.
2. **DEP-006-08-005** (DEL-008-02 Preliminary Site Survey) -- Required to establish existing septic tank location for removal coordination and cost scoping.
3. **DEP-006-08-006** (DEL-001-02 Architectural Floor Plans) -- Required to confirm washroom, locker room, wash station layouts and drain rough-in locations. Fixture counts and drain quantities depend on this.
4. **DEP-006-08-007** (DEL-002-02 Foundation Plan) -- Required to confirm slab penetrations, cistern support, sump pit construction, vent system roof penetrations. Structural interface drives material and installation cost.
5. **DEP-006-08-010** (County preliminary design approval) -- External constraint; final specification cannot proceed without County approval of preliminary plumbing design.
6. **DEP-006-08-013** (PKG-014 downstream handover) -- This specification governs all PKG-014 construction execution. PKG-014 estimating is entirely dependent on DEL-006-08 content.
7. **DEP-006-08-018** (DEL-006-07 Plumbing Calculation Package) -- Pipe sizing and flow calculations directly inform specification values and material quantities.
8. **DEP-006-08-020** (Alberta Safety Codes) -- Code edition must be confirmed before specification requirements can be finalized. Code requirements may affect material standards and testing scope.
9. **DEP-006-08-021** (DEL-006-01 Preliminary Plumbing Design) -- Preliminary design must be approved before final specification. Scope and system selections are set at preliminary stage.

**6 ADVISORY dependencies** are likely to influence quantities or specifications but are not hard gates:

- Mechanical interface (DEL-003-07): Heating zones affect freeze protection approach and may change drain trap specifications.
- Electrical interface (DEL-004-09): Pump motor circuits and hot water heater power affect equipment selection.
- Structural specification interface (DEL-002-12): Cistern support and roof penetration details may affect material and installation scope.
- Civil specification interface (DEL-005-07): Mud sump location relative to site grading affects exterior work scope.
- Architectural specification interface (DEL-001-11): Washroom and fixture layout details may refine fixture counts.
- Fixture schedule interface (DEL-006-06): Fixture types and flow rates directly inform material selection and pricing.

**3 INFO dependencies** are informational and unlikely to change estimating totals:

- R-01 (RFP) and R-06 (App B Plumbing): Already available (SATISFIED).
- DEL-006-02 through DEL-006-05 (drawing sets): Downstream outputs governed by this specification.

### Estimating Readiness Assessment

DEL-006-08 has 9 BLOCKING dependencies. Of these, DEP-006-08-011 and DEP-006-08-012 (source documents R-01 and R-06) are classified as INFO rather than BLOCKING and are already SATISFIED. The 7 genuinely blocking gates are: geotechnical investigation (DEP-006-08-004), preliminary site survey (DEP-006-08-005), architectural floor plans (DEP-006-08-006), structural foundation plan (DEP-006-08-007), County preliminary design approval (DEP-006-08-010), plumbing calculation package (DEP-006-08-018), and preliminary plumbing design (DEP-006-08-021). Additionally, DEP-006-08-020 (Alberta Safety Codes) is BLOCKING for code edition confirmation. Preliminary estimates may be feasible using RFP quantities and conceptual drawings, but definitive estimating requires resolution of these blocking prerequisites.
