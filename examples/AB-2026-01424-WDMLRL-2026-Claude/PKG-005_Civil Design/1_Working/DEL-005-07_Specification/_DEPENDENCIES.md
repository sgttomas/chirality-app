# DEL-005-07 Dependencies

## Upstream Dependencies

### DEL-005-01 -- Preliminary Civil Design (PKG-005)
- Prerequisite: County approval of preliminary design required before final specification proceeds.
- Source: Procedure.md Prerequisites; Procedure.md Step 9.
- Status: PENDING.

### DEL-008-01 -- Geotechnical Investigation Report (PKG-008)
- Prerequisite: Required for subgrade bearing capacity, CBR, frost penetration depth, and compaction standards. Critical-path dependency; specification cannot be finalized without this report.
- Source: Procedure.md Prerequisites; Procedure.md Step 2; Guidance.md Principle 3; Specification.md REQ-CIVIL-012.
- Status: PENDING.

### DEL-008-02 -- Preliminary Site Survey (PKG-008)
- Prerequisite: Required for existing grades and topography inputs.
- Source: Procedure.md Prerequisites.
- Status: PENDING.

### DEL-002-12 -- Structural Specification (PKG-002)
- Interface: Mud sump structural scope boundary and concrete pad structural design must be confirmed with Structural.
- Source: Guidance.md Mud Sump Interface; Procedure.md Step 1.
- Status: PENDING.

### DEL-006-08 -- Plumbing Specification (PKG-006)
- Interface: Mud sump plumbing scope boundary (sump vessel, drainage connection) must be confirmed with Plumbing.
- Source: Guidance.md Mud Sump Interface; Procedure.md Step 1.
- Status: PENDING.

### County Pre-Works (SOW-0200, SOW-0201) -- External
- Constraint: Brushing/clearing and bulk cut/fill must be completed by County before Proponent civil works begin. Specification must define measurable handoff criteria (REQ-CIVIL-017).
- Source: Procedure.md Step 1; Specification.md REQ-CIVIL-017.
- Status: PENDING.

### County Aggregate Supply (SOW-0203) -- External
- Constraint: County supplies aggregate (OUT of Proponent scope). Specification must define aggregate quality/gradation requirements. Testing responsibility unresolved (CF-CIVIL-02).
- Source: Datasheet.md Attributes; Specification.md REQ-CIVIL-004; Guidance.md CF-CIVIL-02.
- Status: PENDING.

### Appendix B Conceptual Drawings (R-04)
- Document input: Pad locations and layout reference.
- Source: Procedure.md Prerequisites.
- Status: SATISFIED (available in _Sources/).

### Appendix C Site Maps (R-07)
- Document input: Site orientation and expansion area.
- Source: Procedure.md Prerequisites.
- Status: SATISFIED (available in _Sources/).

## Downstream Dependencies

### DEL-005-06 -- Civil Calculation Package (PKG-005)
- Handover: Specification design basis (geotechnical values, design criteria, drainage calculations) is documented in the Civil Calculation Package.
- Source: Procedure.md Steps 2-5.

### DEL-018-01 -- Topsoil Stripping Construction (PKG-018)
- Handover: Specification governs topsoil stripping construction requirements.
- Source: Guidance.md Purpose.

### DEL-018-03 -- Gravel Driving Surface Construction (PKG-018)
- Handover: Specification governs driving surface construction requirements, materials, and QC.
- Source: Guidance.md Purpose.

### DEL-009-04 -- Code Compliance Register (PKG-009)
- Interface: Civil Engineer records applicable code sections in the code compliance register.
- Source: Specification.md REQ-CIVIL-011.

## Internal Dependencies

No internal (within-deliverable) dependencies identified beyond the normal document production sequence (Datasheet -> Guidance -> Procedure -> Specification).

## External Dependencies

### County Pre-Works Completion
- Brushing/clearing (SOW-0200), bulk cut/fill (SOW-0201) -- County responsibility.
- Civil specification defines handoff criteria for County-prepared subgrade.
- Source: RFP S3.3.1; Procedure.md Step 1; REQ-CIVIL-017.

### County Aggregate Supply
- County supplies aggregate/gravel (SOW-0203).
- Specification must set quality/gradation requirements for County-supplied material.
- Testing responsibility (Proponent vs County) unresolved -- see CF-CIVIL-02.
- Source: RFP S3.3.1; Datasheet.md; REQ-CIVIL-004.

### Alberta Building Code and Safety Codes
- Governing codes referenced but specific editions and clauses TBD by Civil Engineer.
- Source: RFP S3.3.2; Specification.md REQ-CIVIL-011.

## NOT_TRACKED Dependencies

### Coordination-only relationships
- Weekly meetings with County PM (SOW-0086) -- coordination, not information flow.
- General quality control management (SOW-0089) -- cross-cutting management, not a specific artifact transfer.
- These are not tracked here per the information-flow-only dependency model.

## Tracking Notes

Dependencies will be updated as project progresses and scope is refined.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 18
**ACTIVE:** 18 | **RETIRED:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetName | Status |
|---|---|---|---|---|---|---|
| DEP-005-07-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | SOW-0015 | ACTIVE |
| DEP-005-07-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | SOW-0020 | ACTIVE |
| DEP-005-07-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | SOW-0021 | ACTIVE |
| DEP-005-07-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | OBJ-001 | ACTIVE |
| DEP-005-07-005 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | OBJ-003 | ACTIVE |
| DEP-005-07-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | Preliminary Civil Design (DEL-005-01) | ACTIVE |
| DEP-005-07-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | Geotechnical Investigation Report (DEL-008-01) | ACTIVE |
| DEP-005-07-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | Preliminary Site Survey (DEL-008-02) | ACTIVE |
| DEP-005-07-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | Structural Specification (DEL-002-12) | ACTIVE |
| DEP-005-07-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | Plumbing Specification (DEL-006-08) | ACTIVE |
| DEP-005-07-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | County Pre-Works (SOW-0200, SOW-0201) | ACTIVE |
| DEP-005-07-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | Appendix B Conceptual Drawings | ACTIVE |
| DEP-005-07-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | Appendix C Site Maps | ACTIVE |
| DEP-005-07-014 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | Civil Calculation Package (DEL-005-06) | ACTIVE |
| DEP-005-07-015 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | Topsoil Stripping Construction (DEL-018-01) | ACTIVE |
| DEP-005-07-016 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | Gravel Driving Surface Construction (DEL-018-03) | ACTIVE |
| DEP-005-07-017 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | Code Compliance Register (DEL-009-04) | ACTIVE |
| DEP-005-07-018 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | County Aggregate Supply (SOW-0203) | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

**Defaults and Paths Used:**
- `RUN_ROOT`: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-07_Specification`
- `DECOMPOSITION_PATH`: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
- `SOURCE_DOCS`: AUTO -- scanned deliverable folder; identified 4 source documents: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- `ANCHOR_DOC`: AUTO -- selected `Datasheet.md` (contains "datasheet" in filename; highest-confidence anchor signal per heuristic)
- `EXECUTION_DOC_ORDER`: AUTO -- `Procedure.md` (procedure), `Guidance.md` (guidance), `Specification.md` (spec); ordered by workflow clarity
- `_REFERENCES.md`: Present; used for document resolution (R-01, R-04, R-07 locations confirmed)
- No existing `Dependencies.csv` found; file created fresh

**Assumptions:**
- OBJ-001 and OBJ-003 are treated as TRACES_TO_REQUIREMENT anchors with TargetType=UNKNOWN because the project's objective IDs do not map cleanly to WBS_NODE or REQUIREMENT canonical types. Preserving the raw identifiers.
- TargetLocation paths for deliverable targets use inferred folder conventions (e.g., `PKG-008_Geotech/1_Working/DEL-008-01_Geotech-Investigation`). These are best-effort based on the project folder naming pattern; actual paths may differ.
- DEL-005-06 is listed as DOWNSTREAM because the specification process produces design basis data that is recorded in the calculation package. The information flow is: specification work generates design values -> documented in calc package.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: 1. No integrity warnings.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | None | 5 | 13 |

---

## Lifecycle Summary

**Extraction Lifecycle:**
- ACTIVE: 18
- RETIRED: 0

**Closure Lifecycle (ACTIVE rows):**
- TBD: 9
- PENDING: 7
- SATISFIED: 2
- IN_PROGRESS: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Tree x DAG Integrity:**
- IMPLEMENTS_NODE anchors (ACTIVE): 1 -- OK
- TRACES_TO_REQUIREMENT anchors (ACTIVE): 4

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for downstream task estimating:

### Blocking Dependencies (EstimateImpactClass = BLOCKING)
These dependencies gate meaningful estimating because scope or key quantities are unknown without them:

1. **DEP-005-07-006 -- DEL-005-01 (Preliminary Civil Design):** County approval of preliminary design is a hard prerequisite. Until approved, final specification scope may change. Estimating should treat preliminary design approval as a milestone gate.

2. **DEP-005-07-007 -- DEL-008-01 (Geotechnical Report):** This is the critical-path dependency. Subgrade preparation, granular base depth, compaction standards, and frost protection depth all depend on geotechnical data. Specification contains multiple `[GEO TBD]` placeholders. **Estimating cannot meaningfully quantify subgrade/granular materials without this input.** Guidance.md explicitly flags this as a schedule risk (see Guidance Principle 3).

3. **DEP-005-07-008 -- DEL-008-02 (Preliminary Site Survey):** Existing grades and topography are required to establish cut/fill quantities and grading design. Estimating for earthwork quantities is blocked without survey data.

4. **DEP-005-07-011 -- County Pre-Works:** Handoff criteria for County-prepared subgrade (REQ-CIVIL-017) are TBD. The starting condition for Proponent civil works affects scope and quantities.

5. **DEP-005-07-018 -- County Aggregate Supply:** Specification must define aggregate quality requirements. Testing responsibility is unresolved (CF-CIVIL-02). This affects whether aggregate testing costs are in Proponent's estimate.

### Advisory Dependencies (EstimateImpactClass = ADVISORY)
These may change quantities or approach but are not hard gates:

1. **DEP-005-07-009 -- DEL-002-12 (Structural Specification):** Mud sump and concrete pad scope boundary with Structural. Until resolved, quantities for civil-scope concrete work vs structural-scope concrete work are uncertain.

2. **DEP-005-07-010 -- DEL-006-08 (Plumbing Specification):** Mud sump scope boundary with Plumbing. Affects which drainage elements are civil-estimated vs plumbing-estimated.

3. **DEP-005-07-014/015/016 -- Downstream handovers to DEL-005-06, DEL-018-01, DEL-018-03:** These are outbound; they indicate that the specification is a prerequisite for construction estimating of PKG-018 deliverables.

### Key Unresolved Items for Estimating
- **Design vehicle parameters** (motor scraper class, axle load, turning radius): TBD per Datasheet.md. Affects driving surface thickness design.
- **Design storm return period** (REQ-CIVIL-003): TBD. Affects drainage infrastructure sizing.
- **Frost penetration depth**: TBD pending DEL-008-01.
- **Aggregate quality/gradation requirements**: TBD pending specification development and CF-CIVIL-02 resolution.
- **Concrete pad structural details**: Deferred to PKG-002 interface resolution.
