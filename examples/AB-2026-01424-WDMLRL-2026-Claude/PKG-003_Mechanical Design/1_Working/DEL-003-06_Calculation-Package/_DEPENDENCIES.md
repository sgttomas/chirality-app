# Dependencies: DEL-003-06 Mechanical Calculation Package

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Status:** POPULATED
**Dependencies.csv:** 20 rows (20 ACTIVE, 0 RETIRED)
**Schema Version:** v3.1

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-003-06-A001 | IMPLEMENTS_NODE | SOW-0013 | Complete final mechanical design (HVAC, ventilation, exhaust systems) | HIGH |
| DEP-003-06-A002 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-003-06-A003 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all mechanical systems to operational readiness | HIGH |

### EXECUTION Edges -- UPSTREAM (9 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-003-06-E001 | PREREQUISITE | DELIVERABLE | DEL-003-01 (Preliminary Mechanical Design) | County approval of preliminary design required before final calcs | BLOCKING |
| DEP-003-06-E002 | PREREQUISITE | PACKAGE | PKG-001 / PKG-002 | Building envelope U-values required for heating load calculation | BLOCKING |
| DEP-003-06-E003 | PREREQUISITE | DOCUMENT | R-04 Appendix B (Shop drawing) | Floor plan review required for zone sizing | -- |
| DEP-003-06-E004 | CONSTRAINT | DELIVERABLE | DEL-016-01 (Overhead Cranes) | Crane envelope clearance required before positioning overhead equipment | BLOCKING |
| DEP-003-06-E005 | PREREQUISITE | EXTERNAL | County Welding Equipment Specs (SOW-0204) | Welding exhaust sizing preliminary until County specs received | ADVISORY |
| DEP-003-06-E006 | PREREQUISITE | DELIVERABLE | DEL-008-01 (Geotech Report) | Geotech affects foundation type and utility routing | ADVISORY |
| DEP-003-06-E007 | INTERFACE | DELIVERABLE | DEL-002-06 (Service Pit Details) | Pit dimensions needed for ventilation calculation | ADVISORY |
| DEP-003-06-E008 | INTERFACE | DELIVERABLE | DEL-002-07 (Crane Support Details) | Crane rail height needed for overhead equipment clearance | ADVISORY |
| DEP-003-06-E009 | INTERFACE | DELIVERABLE | DEL-018-06 (Utility Tie-Ins) | Natural gas supply pressure confirmation needed for equipment sizing | ADVISORY |

### EXECUTION Edges -- DOWNSTREAM (8 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-003-06-E010 | HANDOVER | DELIVERABLE | DEL-003-02 (HVAC Layout Plans) | Engineering basis of record for HVAC plans | BLOCKING |
| DEP-003-06-E011 | HANDOVER | DELIVERABLE | DEL-003-03 (Ductwork Plans) | Engineering basis of record for ductwork plans | BLOCKING |
| DEP-003-06-E012 | HANDOVER | DELIVERABLE | DEL-003-04 (Exhaust Plans) | Engineering basis of record for exhaust plans | BLOCKING |
| DEP-003-06-E013 | HANDOVER | DELIVERABLE | DEL-003-05 (Equipment Schedule) | Engineering basis of record for equipment schedule | BLOCKING |
| DEP-003-06-E014 | HANDOVER | DELIVERABLE | DEL-003-07 (Mechanical Specification) | Engineering basis of record for mechanical specification | BLOCKING |
| DEP-003-06-E015 | INTERFACE | DELIVERABLE | DEL-004-08 (Electrical Calc Package) | Ceiling fan power requirements communicated to electrical | ADVISORY |
| DEP-003-06-E016 | HANDOVER | PACKAGE | PKG-013 (Mechanical Installation) | Sizing outputs required by mechanical contractor | BLOCKING |
| DEP-003-06-E017 | HANDOVER | PACKAGE | PKG-020 (Commissioning) | Design flows/temps/pressures transmitted for commissioning tests | ADVISORY |

---

## Run Notes

### Run 2026-02-26 -- Initial Extraction

**Parameters:**
- SCOPE: DEL-003-06_Calculation-Package
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- SOURCE_DOCS: AUTO (resolved below)
- ANCHOR_DOC: AUTO (resolved to Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to Procedure.md, Guidance.md, Specification.md, Datasheet.md)

**Paths used:**
- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-003_Mechanical Design/1_Working/DEL-003-06_Calculation-Package`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md`
- _REFERENCES.md: read (used for document location resolution)

**Source documents scanned (4):**
1. Datasheet.md (ANCHOR_DOC)
2. Procedure.md (EXECUTION_DOC, primary)
3. Guidance.md (EXECUTION_DOC)
4. Specification.md (EXECUTION_DOC)

**Excluded from scan:** _CONTEXT.md, _DEPENDENCIES.md, _REFERENCES.md, _SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md (generated/meta files)

**Decomposition status:** AVAILABLE. Validated all deliverable IDs, package IDs, SOW items, and objective IDs against decomposition Section 5, 6, 7, and 8.

**Defaults applied:**
- ANCHOR_DOC resolved to Datasheet.md (contains "datasheet" in filename; highest-confidence match per DOC_ROLE_MAP default heuristic)
- EXECUTION_DOC_ORDER resolved by DOC_ROLE_MAP: Procedure.md first (contains "procedure"), then Guidance.md (contains "guidance"), then Specification.md (contains "spec")
- All four source documents also scanned for cross-references during both passes

**Assumptions:**
- PKG-001/PKG-002 envelope inputs (E002) treated as a single combined prerequisite rather than two separate rows because the source text references them jointly ("Architectural and Structural packages")
- DEL-002-07 (Crane Support Details) treated as separate interface from DEL-016-01 (Overhead Cranes) because the information flows are distinct: structural dimensions vs. crane equipment specs
- Natural gas supply coordination (E009) targets DEL-018-06 because SOW-0080 maps to PKG-018 in decomposition

**Warnings:** None.

**Quality check results:**
- Parent anchor count: 1 (SOW-0013) -- PASS
- DependencyID uniqueness: 20/20 -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- All enums are canonical write-form -- PASS
- No duplicate rows detected -- PASS
- CSV parseable -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE | Total RETIRED |
|---|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | AVAILABLE | None | 3 | 17 | 20 | 0 |

---

## Lifecycle Summary

**Extraction Lifecycle:**
- ACTIVE: 20
- RETIRED: 0

**Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only):**
- TBD: 12
- PENDING: 8
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Interpretation:** All dependencies are newly extracted. Upstream execution dependencies where the required input is known to not yet exist are marked PENDING. All others are TBD pending further project status confirmation.

---

## Downstream Handoff Notes

**CONSUMER_CONTEXT: TASK_ESTIMATING**

This register is intended to support downstream task-level estimating. Key observations for estimating consumers:

### BLOCKING upstream dependencies (affect estimating readiness)
1. **DEP-003-06-E001 (DEL-003-01 Preliminary Design approval):** The calculation package cannot be finalized until County approves the preliminary mechanical design. Estimating should account for this approval gate in the schedule.
2. **DEP-003-06-E002 (PKG-001/PKG-002 envelope U-values):** Heating load calculation is blocked without building envelope data. This is a cross-discipline dependency that affects the core sizing calculation.
3. **DEP-003-06-E004 (DEL-016-01 crane envelope):** Overhead mechanical equipment positioning depends on crane clearance confirmation. Affects equipment selection and potentially equipment cost.

### ADVISORY upstream dependencies (may change quantities or approach)
4. **DEP-003-06-E005 (County welding specs, SOW-0204):** Welding exhaust section can proceed with assumptions but is PRELIMINARY. Final equipment selection may change.
5. **DEP-003-06-E006 (DEL-008-01 geotech):** Utility routing may change; low likelihood of materially affecting mechanical equipment sizing.
6. **DEP-003-06-E007/E008 (structural details):** Pit dimensions and crane support details are interface data; these refine calculations but are unlikely to change the scope of work.
7. **DEP-003-06-E009 (gas supply):** Gas pressure confirmation affects equipment selection but not the scope of the calculation work itself.

### BLOCKING downstream dependencies (estimating impact on other deliverables)
8. **DEP-003-06-E010 through E014 (DEL-003-02 through DEL-003-07):** All five downstream PKG-003 deliverables cannot be finalized until this calculation package is complete. Estimating for those deliverables should sequence after this one.
9. **DEP-003-06-E016 (PKG-013 Mechanical Installation):** The mechanical contractor cannot proceed without correct sizing from this package.

### Summary for estimating
- This deliverable sits on the **critical path** for all mechanical design and installation work.
- 3 upstream dependencies are BLOCKING for meaningful estimating.
- 6 downstream deliverables and 1 downstream package depend directly on this package's outputs.
- The welding exhaust section is conditionally PRELIMINARY pending external County input with no documented timeline.
