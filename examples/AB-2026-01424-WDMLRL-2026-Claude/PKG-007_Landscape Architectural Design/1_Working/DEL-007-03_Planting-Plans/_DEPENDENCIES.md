# DEL-007-03 Planting & Restoration Plans — Dependencies

## Tracking Status
- **Dependency Tracking**: ACTIVE
- **Register Schema**: v3.1
- **Last Run**: 2026-02-26

## Upstream Dependencies
- **DEL-007-02**: Landscape Site Plans (must be approved; provides spatial framework)
- **DEL-007-01**: Preliminary Landscape Design (establishes plant selection approach; County approval gate before IFC)
- **PKG-005**: Civil Grading Plan (drainage features, graded contours — integration required)
- RFP landscape design and sustainability requirements (R-01)
- Site ecological assessment and existing vegetation documentation

## Internal Dependencies
- Landscape architect coordination with design team
- Plant palette and zonation development process

## Downstream Dependencies
- **DEL-007-04**: Landscape Specification (references planting callouts and plant details)
- **DEL-018-02**: Site Grading & Landscaping — construction execution (consumes IFC planting plans)

## External Dependencies
- Landscape Architect discipline assignment
- Horticultural and ecological expertise
- Native plant availability and sourcing information
- Stakeholder review and approval availability

## Blocking Issues
- None currently identified

## Notes
Dependency tracking activated by DEPENDENCIES agent run 2026-02-26. Formal register in Dependencies.csv.

---

## Extracted Dependency Register

**Total rows:** 11 | **ACTIVE:** 11 | **RETIRED:** 0

### ANCHOR Rows (3)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-007-03-001 | IMPLEMENTS_NODE | SOW-0017 | SOW-0017 -- Complete landscape architectural design | HIGH | ACTIVE |
| DEP-007-03-002 | TRACES_TO_REQUIREMENT | OBJ-001 | OBJ-001 -- Deliver code-compliant functional maintenance shop addition | MEDIUM | ACTIVE |
| DEP-007-03-003 | TRACES_TO_REQUIREMENT | OBJ-003 | OBJ-003 -- Produce complete IFC design documentation | MEDIUM | ACTIVE |

### EXECUTION Rows (8)

| DependencyID | Direction | DependencyType | TargetName | Confidence | EstimateImpactClass | Status |
|---|---|---|---|---|---|---|
| DEP-007-03-004 | UPSTREAM | PREREQUISITE | DEL-007-01 -- Preliminary Landscape Design | HIGH | BLOCKING | ACTIVE |
| DEP-007-03-005 | UPSTREAM | PREREQUISITE | DEL-007-02 -- Landscape Site Plans | HIGH | BLOCKING | ACTIVE |
| DEP-007-03-006 | UPSTREAM | INTERFACE | PKG-005 -- Civil Design (Site Grading Plan) | HIGH | BLOCKING | ACTIVE |
| DEP-007-03-007 | DOWNSTREAM | HANDOVER | DEL-007-04 -- Landscape Specification | HIGH | ADVISORY | ACTIVE |
| DEP-007-03-008 | UPSTREAM | CONSTRAINT | R-01 -- RFP (IFC Stamp Requirement) | MEDIUM | ADVISORY | ACTIVE |
| DEP-007-03-009 | UPSTREAM | CONSTRAINT | R-01 -- RFP (Completion Deadline and Guarantee) | MEDIUM | ADVISORY | ACTIVE |
| DEP-007-03-010 | DOWNSTREAM | HANDOVER | DEL-018-02 -- Site Grading & Landscaping (Construction) | MEDIUM | ADVISORY | ACTIVE |
| DEP-007-03-011 | UPSTREAM | INTERFACE | R-07 -- Appendix C Site Maps | HIGH | INFO | ACTIVE |

---

## Run Notes

### Defaults and Paths Used
- **SCOPE:** DEL-007-03
- **RUN_ROOT:** PKG-007_Landscape Architectural Design/1_Working/DEL-007-03_Planting-Plans/
- **DECOMPOSITION_PATH:** _Decomposition/WDMLRL_Decomposition_Claude.md (R1 -- 2026-02-25)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS (AUTO):** Datasheet.md (ANCHOR_DOC), Guidance.md, Procedure.md, Specification.md (EXECUTION_DOCS)
- **ANCHOR_DOC:** Datasheet.md (selected: contains Identification table with SOW Reference and Objectives Supported)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity)

### Decomposition Validation
- Decomposition located and read successfully.
- DEL-007-03_Planting-Plans confirmed in DECOMP section 7 PKG-007 table (line 450).
- SOW-0017 confirmed in DECOMP section 8 Scope Ledger (line 612): mapped to DEL-007-02 thru DEL-007-04.
- OBJ-001 and OBJ-003 confirmed in DECOMP section 7 PKG-007 table for DEL-007-03.

### Anchor Integrity
- Parent anchor: 1 ACTIVE IMPLEMENTS_NODE (DEP-007-03-001 -> SOW-0017). No warnings.
- Trace anchors: 2 ACTIVE TRACES_TO_REQUIREMENT (OBJ-001, OBJ-003). Confidence MEDIUM -- Datasheet states mapping is "best-effort" ASSUMPTION, but DECOMP table confirms the same mapping.

### Extraction Notes
- DEP-007-03-004 (DEL-007-01 prerequisite): Strong multi-source evidence. Procedure.md Prerequisites table, Guidance P-5, Specification REQ-007-03-012, and R-01 section 3.3.2 all independently state this prerequisite. This is an approval gate, not coordination.
- DEP-007-03-005 (DEL-007-02 prerequisite): Strong multi-source evidence. Procedure.md Prerequisites, Procedure Step 1.3 and Step 4.1, Datasheet Attributes, Guidance P-2, Specification REQ-007-03-002.
- DEP-007-03-006 (PKG-005 interface): Explicit cross-package interface. R-01 section 3.4 (SOW-0020, SOW-0021) requires grading integration. TargetType=PACKAGE because the sources reference "PKG-005 civil grading" generically rather than a specific deliverable within PKG-005; DEL-005-02 (Site Grading Plan) is the most likely specific target but this is not explicitly stated.
- DEP-007-03-007 (DEL-007-04 handover): Explicit downstream consumer. Plant codes, zone designations, and callouts flow from DEL-007-03 to DEL-007-04.
- DEP-007-03-008 (IFC stamp constraint): Contractual constraint from R-01 section 3.3.2 / SOW-0018. Under active dispute (CONF-007-03-001: P.Eng. vs. RLA stamp for landscape drawings).
- DEP-007-03-009 (Deadline/guarantee constraint): Contractual constraint affecting scope definition. Under active dispute (CONF-007-03-002: restoration phasing vs. December 31, 2026 deadline).
- DEP-007-03-010 (DEL-018-02 handover): Inferred downstream handover. DECOMP excludes construction execution from PKG-007 and assigns it to PKG-018. DEL-018-02 (Site Grading & Landscaping, SOW-0076) is the most likely consumer. Confidence MEDIUM because specific target is inferred.
- DEP-007-03-011 (R-07 interface): R-07 Appendix C is explicitly cited as a required reference in Procedure.md Prerequisites and Datasheet.md. Provides essential spatial/ecological context but does not gate design progression in the same way as DEL-007-01 or DEL-007-02.

### Edges Not Extracted (justification)
- "Landscape architect coordination with design team" (declared Internal Dependency): Not extracted. This is coordination, not information/artifact transfer.
- "Stakeholder review and approval availability" (declared External Dependency): Not extracted. Generic availability concern, not a specific information dependency.
- "Native plant availability and sourcing information" (declared External Dependency): Not extracted. Market/procurement concern, not a specific artifact/data transfer from an identifiable target.
- "Horticultural and ecological expertise" (declared External Dependency): Not extracted. Personnel/capability concern, not an information flow edge.
- DEL-007-04 draft as coordination input to DEL-007-03 (Procedure.md Prerequisites Reference Documents table): Not extracted as a separate upstream edge. The Procedure.md table lists DEL-007-04 draft as a reference for "coordination of plant codes and zone designations." This is bi-directional coordination during production, not a prerequisite input. The primary information flow is downstream (DEP-007-03-007).

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (R1, located) | None | 11 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **Total Rows** | 11 |
| **ACTIVE** | 11 |
| **RETIRED** | 0 |
| | |
| **ANCHOR** | 3 |
| -- IMPLEMENTS_NODE | 1 |
| -- TRACES_TO_REQUIREMENT | 2 |
| **EXECUTION** | 8 |
| -- PREREQUISITE | 2 |
| -- INTERFACE | 2 |
| -- HANDOVER | 2 |
| -- CONSTRAINT | 2 |
| | |
| **SatisfactionStatus** | |
| -- TBD | 11 |
| | |
| **Confidence** | |
| -- HIGH | 7 |
| -- MEDIUM | 4 |

---

## Downstream Handoff Notes (CONSUMER_CONTEXT: TASK_ESTIMATING)

### Estimating-Critical Dependencies

Three execution dependencies are classified as **BLOCKING** for task estimating:

1. **DEP-007-03-004 (DEL-007-01 prerequisite):** The County approval gate on preliminary landscape design must be satisfied before IFC planting plans can be issued. Until DEL-007-01 is approved, the scope and plant palette for DEL-007-03 are provisional. Estimating should flag this as a scope-maturity gate.

2. **DEP-007-03-005 (DEL-007-02 prerequisite):** The approved Landscape Site Plans provide the spatial framework for all planting zones. Without DEL-007-02, planting quantities and zone extents cannot be reliably estimated. Estimating should treat this as a quantity-definition gate.

3. **DEP-007-03-006 (PKG-005 interface):** Civil grading design defines where planting zones can and cannot be sited (drainage, infrastructure, driving surfaces). Without sufficiently advanced PKG-005 output, planting area calculations and scope delineation are unreliable. Estimating should account for this cross-package dependency.

### Advisory Dependencies

- **DEP-007-03-008 (IFC stamp constraint):** CONF-007-03-001 is unresolved. If P.Eng. co-signature is required for landscape drawings, this may affect professional services cost estimation. If RLA stamp alone suffices, no additional cost.
- **DEP-007-03-009 (Deadline/guarantee constraint):** CONF-007-03-002 is unresolved. If spring 2027 planting is acceptable, restoration scope may split across two mobilizations (affecting cost). If all planting must be complete by December 31, 2026, the scope may be limited to fast-establishment methods (sodding, erosion control seeding) which carry different unit costs.
- **DEP-007-03-010 (DEL-018-02 handover):** Planting plan outputs flow to construction execution. Estimating for PKG-018 should await finalization of DEL-007-03 for planting quantities.

### Estimating Readiness Assessment

DEL-007-03 has significant TBD elements (plant palette, planting density, restoration phasing, soil conditions) that depend on resolution of its three BLOCKING upstream dependencies and two unresolved conflicts (CONF-007-03-001, CONF-007-03-002). Estimating should treat DEL-007-03 scope quantities as provisional until these gates are cleared.
