# Dependencies: DEL-003-05 Mechanical Equipment Schedule

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (21 rows, all ACTIVE)
- **Schema Version:** v3.1

### Summary by Class

| DependencyClass | AnchorType | Count |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 18 |
| **Total** | | **21** |

### Summary by Direction

| Direction | Count |
|---|---|
| UPSTREAM | 13 |
| DOWNSTREAM | 8 |
| **Total** | **21** |

### ANCHOR Rows

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-003-05-001 | IMPLEMENTS_NODE | SOW-0013 | Final mechanical design -- HVAC ventilation exhaust systems | HIGH |
| DEP-003-05-002 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-003-05-003 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all mechanical plumbing and water storage systems | HIGH |

### EXECUTION Rows -- UPSTREAM (this deliverable requires)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-003-05-004 | PREREQUISITE | DELIVERABLE | DEL-003-01 (Preliminary Mechanical Design) | County-approved preliminary design required before equipment selections committed | HIGH | BLOCKING |
| DEP-003-05-005 | PREREQUISITE | DELIVERABLE | DEL-003-06 (Mechanical Calculation Package) | Calculation package required before performance values entered in schedule | HIGH | BLOCKING |
| DEP-003-05-006 | PREREQUISITE | DELIVERABLE | DEL-008-01 (Geotechnical Report) | Geotech report required for heating load calculations | MEDIUM | ADVISORY |
| DEP-003-05-007 | INTERFACE | PACKAGE | PKG-002 (Structural Design) | Structural inputs: mounting loads, crane girder layout for fan coordination | HIGH | ADVISORY |
| DEP-003-05-008 | INTERFACE | PACKAGE | PKG-004 (Electrical Design) | Electrical inputs: phase/voltage/FLA per equipment item | HIGH | ADVISORY |
| DEP-003-05-009 | CONSTRAINT | EXTERNAL | SOW-0204 (County welding equipment specs) | County-supplied specs needed for EXH-003 sizing; timing unknown | HIGH | BLOCKING |
| DEP-003-05-010 | PREREQUISITE | DOCUMENT | R-01 (RFP) | RFP required for equipment scope confirmation | HIGH | INFO |
| DEP-003-05-011 | PREREQUISITE | DOCUMENT | R-04 (Appendix B Shop) | Conceptual drawings required for equipment location planning | HIGH | INFO |
| DEP-003-05-020 | CONSTRAINT | REQUIREMENT | SOW-0018 (P.Eng. stamp) | IFC schedule must be stamped by Alberta P.Eng. | HIGH | ADVISORY |
| DEP-003-05-021 | CONSTRAINT | REQUIREMENT | SOW-0010c (County approval) | County approval of preliminary design is a hard gate before IFC | HIGH | BLOCKING |

### EXECUTION Rows -- DOWNSTREAM (these need this deliverable)

| DependencyID | DependencyType | TargetType | Target | Statement (abbreviated) | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-003-05-012 | HANDOVER | DELIVERABLE | DEL-003-02 (HVAC Layout Plans) | Equipment tags applied on HVAC plans | HIGH | ADVISORY |
| DEP-003-05-013 | HANDOVER | DELIVERABLE | DEL-003-03 (Ductwork Plans) | Equipment tags applied on ductwork plans | HIGH | ADVISORY |
| DEP-003-05-014 | HANDOVER | DELIVERABLE | DEL-003-04 (Exhaust System Plans) | Equipment tags applied on exhaust plans | HIGH | ADVISORY |
| DEP-003-05-015 | HANDOVER | DELIVERABLE | DEL-003-07 (Mechanical Specification) | Schedule data consistent with specification | MEDIUM | ADVISORY |
| DEP-003-05-016 | HANDOVER | PACKAGE | PKG-013 (Mechanical & HVAC Installation) | Procurement anchor for mechanical contractor | HIGH | BLOCKING |
| DEP-003-05-017 | INTERFACE | PACKAGE | PKG-002 (Structural Design) | Equipment weights/mounting/vibration data provided to structural | HIGH | ADVISORY |
| DEP-003-05-018 | INTERFACE | PACKAGE | PKG-004 (Electrical Design) | Electrical load data per equipment item provided to electrical | HIGH | ADVISORY |
| DEP-003-05-019 | HANDOVER | DELIVERABLE | DEL-020-01 (Building Systems Commissioning) | Commissioning baseline parameters | HIGH | ADVISORY |

---

## Run Notes

### Defaults and Chosen Paths
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule`
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (accessible; used for anchor validation and deliverable ID resolution)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO -- resolved to: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
  - ANCHOR_DOC: `Datasheet.md` (contains "datasheet" in filename; highest-confidence match for definition/traceability signal)
  - EXECUTION_DOCS (ordered): `Procedure.md`, `Guidance.md`, `Specification.md`
- **_REFERENCES.md:** Present and read; used for document location resolution (R-01, R-04 paths confirmed)

### Decomposition Validation
- Decomposition file located and accessible.
- DEL-003-05 confirmed in decomposition deliverable table (PKG-003, SOW-0013, OBJ-003/OBJ-004).
- All referenced deliverable IDs (DEL-003-01, DEL-003-02, DEL-003-03, DEL-003-04, DEL-003-06, DEL-003-07, DEL-008-01, DEL-020-01) confirmed in decomposition.
- All referenced package IDs (PKG-002, PKG-003, PKG-004, PKG-008, PKG-013, PKG-015, PKG-020) confirmed in decomposition.
- All referenced SOW IDs (SOW-0013, SOW-0010c, SOW-0018, SOW-0204) confirmed in decomposition.
- All referenced OBJ IDs (OBJ-003, OBJ-004) confirmed in decomposition.

### Extraction Notes
- Pass 1 (ANCHOR): 1 IMPLEMENTS_NODE anchor to SOW-0013, 2 TRACES_TO_REQUIREMENT anchors to OBJ-003 and OBJ-004. All explicit in Datasheet Section 1.
- Pass 2 (EXECUTION): 18 execution edges extracted. Procedure Section 2.1 (Required Upstream Inputs) was the richest single source for upstream dependencies. Guidance Section 1 (Purpose) and Specification Section 1.3 (Relationship to Other Deliverables) were primary sources for downstream handovers.
- Bidirectional interfaces with PKG-002 and PKG-004 are represented as separate UPSTREAM and DOWNSTREAM rows (DEP-003-05-007/017 and DEP-003-05-008/018 respectively) because distinct data items flow in each direction.
- DEP-003-05-021 (SOW-0010c County approval constraint) reinforces DEP-003-05-004 (DEL-003-01 prerequisite) but is retained as a separate row because it captures a distinct constraint type (approval gate vs. artifact transfer).
- PKG-013 is represented as a single PACKAGE-level downstream handover (DEP-003-05-016) rather than 6 individual deliverable rows (DEL-013-01 through DEL-013-06) because the source documents reference the package-level procurement relationship rather than individual installation deliverables.
- Documents R-01 (RFP) and R-04 (Appendix B Shop) are marked SatisfactionStatus=SATISFIED because they are confirmed available per _REFERENCES.md and Procedure Section 2.1.

### Warnings
- No warnings. Parent anchor found (1x IMPLEMENTS_NODE). No ambiguous anchors.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Accessible; validated | None | 3 | 18 | 21 |

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
| TBD | 11 |
| PENDING | 8 |
| SATISFIED | 2 |
| IN_PROGRESS | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

Note: TBD satisfaction statuses are on ANCHOR rows, downstream HANDOVER rows, and INTERFACE rows where the deliverable itself is not yet produced. PENDING statuses are on upstream PREREQUISITE/CONSTRAINT rows where inputs are not yet received. SATISFIED statuses are on document inputs (R-01, R-04) confirmed available.

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating Readiness Assessment

This deliverable has **4 BLOCKING upstream dependencies** that directly gate meaningful estimating:

1. **DEP-003-05-004 (DEL-003-01 Preliminary Mechanical Design)** -- County approval of the preliminary design is the primary gate. Equipment selections cannot be committed without it, meaning performance specifications and procurement costs are indeterminate.
2. **DEP-003-05-005 (DEL-003-06 Mechanical Calculation Package)** -- All performance values in the equipment schedule derive from engineering calculations. Without the calculation package, equipment sizing and therefore cost estimation are speculative.
3. **DEP-003-05-009 (SOW-0204 County welding equipment specifications)** -- The welding exhaust system (EXH-003) cannot be sized without County-supplied welding equipment specifications. Timing is unknown and County-controlled.
4. **DEP-003-05-021 (SOW-0010c County approval)** -- Reinforces DEP-003-05-004; the County approval gate is a hard prerequisite for IFC-level costing.

### ADVISORY dependencies affecting estimating accuracy:
- **DEP-003-05-006 (DEL-008-01 Geotech Report)** -- Affects heating load calculations indirectly (slab conditions).
- **DEP-003-05-007/008 (PKG-002/PKG-004 interfaces)** -- Structural mounting and electrical characteristics affect equipment selection refinement and cost accuracy.

### Estimating implications:
- Equipment cost estimation for this deliverable is gated by DEL-003-06 (performance sizing) and DEL-003-01 (County approval).
- The Mechanical Calculation Package (DEL-003-06) is the critical-path predecessor for cost-quality estimates.
- Until SOW-0204 (welding specs) is received, EXH-003 costs carry elevated uncertainty.
- Downstream handovers (DEL-003-02/03/04, PKG-013, DEL-020-01) cannot be fully estimated until this schedule is populated with confirmed performance values.
