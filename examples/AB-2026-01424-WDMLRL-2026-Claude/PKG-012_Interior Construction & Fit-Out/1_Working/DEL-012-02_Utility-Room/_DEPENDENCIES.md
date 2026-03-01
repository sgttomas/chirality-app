# DEL-012-02: Utility Room - Dependencies

## Dependency Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Register File**: Dependencies.csv

## External Dependencies
- Facility shell construction completion
- Final equipment selection and specifications
- Design finalization and approval
- General Contractor availability and scheduling

## Internal Package Dependencies
- **DEL-012-01** (Parts Storage Room): Coordinate timing and utility access
- **DEL-012-03** (Office Space): Coordinate mechanical system distribution

## PKG-013 Dependencies (CRITICAL)
All PKG-013 deliverables depend on utility room completion:
- **DEL-013-01**: Heating System - Equipment mounting location
- **DEL-013-02**: Air Exchanger - Equipment location and ductwork
- **DEL-013-03**: Makeup Air System - Supply connection points
- **DEL-013-04**: Equipment Exhaust - Exhaust routing coordination
- **DEL-013-05**: Welding Exhaust - Connection infrastructure
- **DEL-013-06**: Ceiling Fans - Distribution points

## Constraint Notes
- Utility room must be complete before any PKG-013 equipment installation
- Equipment footprint must be finalized before construction start
- Service access must meet manufacturer requirements
- All utility infrastructure coordination required

## Dependency Map
```
Facility Shell --> DEL-012-02 (Utility) --> All PKG-013 Installations
                |
        PKG-013 HVAC & Mechanical Systems
```

---

## Extracted Dependency Register

**Total rows**: 21
**ACTIVE**: 21 | **RETIRED**: 0

### ANCHOR Rows (2 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-012-02-A01 | IMPLEMENTS_NODE | SOW-0030 | Construct utility room | HIGH |
| DEP-012-02-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop | HIGH |

### EXECUTION Rows -- UPSTREAM (10 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-012-02-E01 | PREREQUISITE | DELIVERABLE | DEL-011-01 (Superstructure) | Building shell must be complete before interior construction | BLOCKING |
| DEP-012-02-E02 | PREREQUISITE | DELIVERABLE | DEL-013-01 (Heating System) | Equipment selection/specs must be confirmed before construction start | BLOCKING |
| DEP-012-02-E03 | INTERFACE | DELIVERABLE | PKG-013 (collective) | Equipment submittals: footprints, weights, mounting, clearances | BLOCKING |
| DEP-012-02-E04 | INTERFACE | DELIVERABLE | PKG-013 (ventilation) | Mechanical engineer must define ventilation rate for penetration sizing | BLOCKING |
| DEP-012-02-E05 | INTERFACE | DELIVERABLE | DEL-014-01 (Cistern) | Cistern dimensions and pad/pit requirements from PKG-014 | ADVISORY |
| DEP-012-02-E06 | INTERFACE | DELIVERABLE | DEL-015-02 (Lighting) | Outlet locations, conduit paths, lighting mounting points from PKG-015 | ADVISORY |
| DEP-012-02-E07 | CONSTRAINT | DOCUMENT | IFC Drawings (P.Eng.) | IFC drawings stamped and issued before construction begins (hold-point) | BLOCKING |
| DEP-012-02-E08 | CONSTRAINT | DOCUMENT | Building Permit | Building permit in hand before construction (hold-point) | BLOCKING |
| DEP-012-02-E09 | INTERFACE | DELIVERABLE | DEL-011-07 (Mezzanine) | Mezzanine structural interface; clear height confirmation required | ADVISORY |
| DEP-012-02-E18 | CONSTRAINT | DOCUMENT | Approved Finish Schedule | Finish schedule approved by County PM before material procurement (hold-point) | ADVISORY |

### EXECUTION Rows -- DOWNSTREAM (9 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-012-02-E10 | HANDOVER | DELIVERABLE | DEL-013-01 (Heating System) | Utility room complete before heating system installation | BLOCKING |
| DEP-012-02-E11 | HANDOVER | DELIVERABLE | DEL-013-02 (Air Exchanger) | Utility room complete before air exchanger installation | BLOCKING |
| DEP-012-02-E12 | HANDOVER | DELIVERABLE | DEL-013-03 (Makeup Air) | Utility room complete before makeup air installation | BLOCKING |
| DEP-012-02-E13 | HANDOVER | DELIVERABLE | DEL-013-04 (Equipment Exhaust) | Utility room complete before equipment exhaust installation | BLOCKING |
| DEP-012-02-E14 | HANDOVER | DELIVERABLE | DEL-013-05 (Welding Exhaust) | Utility room complete before welding exhaust installation | BLOCKING |
| DEP-012-02-E15 | HANDOVER | DELIVERABLE | DEL-013-06 (Ceiling Fans) | Utility room complete before ceiling fan installation | BLOCKING |
| DEP-012-02-E16 | HANDOVER | DELIVERABLE | DEL-014-01 (Cistern) | Cistern housing complete before cistern equipment installation | BLOCKING |
| DEP-012-02-E17 | HANDOVER | DELIVERABLE | DEL-015-02 (Lighting) | Electrical rough-ins in place before lighting fixture installation | ADVISORY |
| DEP-012-02-E19 | INTERFACE | DELIVERABLE | DEL-014-04 (Floor Drains) | Floor drain rough-in coordination with PKG-014 before concrete placement | ADVISORY |

---

## Run Notes

**Run timestamp**: 2026-02-26
**Mode**: UPDATE
**Strictness**: CONSERVATIVE
**Consumer context**: TASK_ESTIMATING

### Defaults and Paths Used
- **RUN_ROOT**: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- **DECOMPOSITION_PATH**: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (found and used)
- **SOURCE_DOCS (AUTO)**: Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **DOC_ROLE_MAP (DEFAULT)**:
  - ANCHOR_DOC: Datasheet.md (matched "datasheet" pattern)
  - EXECUTION_DOCS: Procedure.md, Guidance.md, Specification.md (matched execution patterns)
- **ANCHOR_DOC**: Datasheet.md
- **EXECUTION_DOC_ORDER**: Procedure.md, Specification.md, Guidance.md, _DEPENDENCIES.md (declared lists used as supplementary evidence)

### Decomposition Validation
- Decomposition document located and used for anchor validation and target ID resolution.
- SOW-0030 confirmed in decomposition scope ledger (S8): mapped to PKG-012 / DEL-012-02 / OBJ-001.
- OBJ-001 confirmed in decomposition objectives (S5).
- All target deliverable IDs (DEL-011-01, DEL-011-07, DEL-013-01 through DEL-013-06, DEL-014-01, DEL-014-04, DEL-015-02) confirmed in decomposition Section 7.

### Assumptions and Warnings
- No warnings. All checks passed.
- DEP-012-02-E03 and DEP-012-02-E04: TargetDeliverableID left blank because these dependencies target PKG-013 collectively (multiple deliverables are the source of submittals/calculations). TargetPackageID set to PKG-013.
- Internal package dependencies (DEL-012-01 coordination, DEL-012-03 coordination) from the declared section were NOT extracted as execution rows because the source documents describe "coordinate timing" without specifying a concrete information/artifact transfer. This is consistent with CONSERVATIVE strictness and the information-flow-only extraction model.

### Quality Check Results
- Schema: All 29 required columns present + 2 extension columns. CSV parseable.
- DependencyID: All 21 IDs unique.
- Evidence: All 21 ACTIVE rows have EvidenceFile and SourceRef populated.
- Enum normalization: All enums are canonical write-form values.
- Parent anchor: Exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-012-02-A01). No warnings.
- No duplicate rows detected.
- _DEPENDENCIES.md counts (21 ACTIVE, 0 RETIRED) match Dependencies.csv.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) -- validated | None | 21 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 21 |
| RETIRED | 0 |

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 19 | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)
| SatisfactionStatus | Count |
|---|---|
| PENDING | 19 |
| NOT_APPLICABLE | 2 |

---

## Downstream Handoff Notes

**Consumer context**: TASK_ESTIMATING

This register contains 21 dependency rows relevant to task-level estimating for DEL-012-02 (Utility Room).

### Estimating-Critical Observations

1. **BLOCKING upstream prerequisites (4 rows)**: DEL-012-02 cannot begin construction until PKG-011 building shell is complete (DEP-012-02-E01), PKG-013 equipment selection is confirmed (DEP-012-02-E02), IFC drawings are P.Eng.-stamped and issued (DEP-012-02-E07), and building permit is in hand (DEP-012-02-E08). These gates affect the earliest possible start date for this deliverable.

2. **BLOCKING upstream interfaces (2 rows)**: PKG-013 equipment submittals (DEP-012-02-E03) and ventilation design calculation (DEP-012-02-E04) are required inputs that define the utility room's internal layout, penetration sizing, and equipment platform design. Without these, estimating quantities for partitions, platforms, and penetrations will carry significant uncertainty.

3. **BLOCKING downstream handovers (7 rows)**: All six PKG-013 deliverables (DEP-012-02-E10 through E15) and the PKG-014 cistern installation (DEP-012-02-E16) are blocked until this utility room is complete. This makes DEL-012-02 a critical-path gating deliverable for the mechanical and plumbing installation packages. Schedule delay on DEL-012-02 cascades directly to 7 downstream deliverables.

4. **TBD quantities affecting estimate accuracy**: Room dimensions (CON-012-02-01), clear height below mezzanine (CON-012-02-04), fire rating requirements (CON-012-02-05), cistern pad scope (CON-012-02-02), and penetration sleeve responsibility (CON-012-02-03) are all unresolved. These TBDs affect partition material quantities, door specifications, fire-stopping material requirements, and structural pad scope.

5. **Scope boundary risk**: Three conflicts (CON-012-02-02, CON-012-02-03, CON-012-02-05) affect whether certain work items are in PKG-012 scope or belong to adjacent packages. Estimating should carry allowances for these items until scope boundaries are resolved.
