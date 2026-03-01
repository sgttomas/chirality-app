# DEL-005-03 Dependencies

## Upstream Dependencies

### DEL-005-01 — Preliminary Civil Design (PKG-005)
- County approval of preliminary civil design required before IFC drainage plan release.
- Source: Procedure Prerequisites; Specification REQ-005.
- Impact: BLOCKING — IFC gate.

### DEL-008-01 — Geotechnical Investigation & Report (PKG-008)
- Geotech report required for soil permeability, frost depth, and subsurface drainage conditions.
- Source: Procedure Prerequisites; Datasheet Conditions; Guidance Principles.
- Impact: BLOCKING — design inputs and IFC gate.

### DEL-008-02 — Preliminary Site Survey (PKG-008)
- Preliminary survey required for existing site topography and pre-development drainage baseline.
- Source: Procedure Prerequisites; Datasheet Attributes.
- Impact: BLOCKING — baseline data for design.

### DEL-021-04 — CCDC 14-2013 Contract Execution (PKG-021)
- Project award and contract execution prerequisite before production can begin.
- Source: Procedure Prerequisites.
- Impact: BLOCKING — project-level gate.

### DEL-005-02 — Site Grading Plan (PKG-005)
- Drainage plan depends on grading plan for surface grades, flow paths, and collection points.
- Source: Procedure Prerequisites and Step B3; Guidance Principles.
- Impact: ADVISORY — parallel/interdependent production.

### DEL-005-06 — Civil Calculation Package (PKG-005)
- Drainage calculations support drainage plan sizing and design storm documentation.
- Source: Procedure Prerequisites and Step B2; Guidance Principles.
- Impact: ADVISORY — parallel production.

### DEL-005-05 — Civil Sections & Details (PKG-005)
- Cross-referenced standard civil sections and consistent nomenclature/elevation datums.
- Source: Procedure Step C5; Guidance Principles.
- Impact: ADVISORY — consistency interface.

### DEL-018-05 — Wash Bay Drainage & Mud Sump (PKG-018)
- Wash bay exterior mud sump drainage interface; drainage plan shows sump location and delineation from clean stormwater.
- Source: Specification REQ-007; Procedure Steps A4 and B4.
- Impact: ADVISORY — interface coordination.

### DEL-001-02 — Architectural Floor Plans (PKG-001)
- Building footprint and entrance/exit locations needed for coordination check.
- Source: Procedure Step D2.
- Impact: ADVISORY — coordination interface.

### DEL-006-03 — Drain & Vent Plans (PKG-006)
- Plumbing floor drain and sump drain locations needed for no-interference confirmation at building connections.
- Source: Procedure Step D2.
- Impact: ADVISORY — coordination interface.

### DEL-018-06 — Utility Tie-Ins (PKG-018)
- Utility crossing/conflict check required for vertical and horizontal clearance between drainage structures and utility crossings.
- Source: Procedure Step D2.
- Impact: ADVISORY — coordination interface.

### R-07 — Appendix C Site Maps (Document)
- Aerial site context and existing drainage patterns.
- Source: Procedure Prerequisites and Step A1.

### R-04 — Appendix B Shop Conceptual Drawing (Document)
- Building footprint and exterior pad locations.
- Source: Procedure Prerequisites and Step A1.

## Downstream Dependencies

### DEL-018-02 — Site Grading & Landscaping (PKG-018)
- IFC drainage plan issued to PKG-018 construction team for execution.
- Source: Procedure Step E4.
- Impact: BLOCKING — construction cannot proceed without IFC drawings.

### DEL-009-02 — Building Permit (PKG-009)
- Drainage plan submitted as part of regulatory submission package.
- Source: Procedure Step E3.
- Impact: INFO — permit submission logistics.

## Internal Dependencies

### DEL-005-02 — Site Grading Plan
- Drainage flow directions must be consistent with grading plan contours and spot elevations.
- Bidirectional interface within PKG-005.

### DEL-005-06 — Civil Calculation Package
- All sized drainage elements require supporting calculations in DEL-005-06.
- Parallel production within PKG-005.

### DEL-005-05 — Civil Sections & Details
- Standard civil sections (swales, ditches, culverts) cross-referenced.
- Nomenclature and elevation datum consistency required.

## External Dependencies

### Alberta Building Code and Safety Codes
- Code compliance required per R-01, Section 3.3.2 and Section 3.4.
- Specific edition and drainage-specific clauses TBD.

### Alberta Environment and Protected Areas Stormwater Guidance
- May set design storm criteria and impose landfill-proximity requirements.
- Applicability TBD (ASSUMPTION).

### Camrose County Municipal Drainage Requirements
- Development and building permit requirements may include site drainage conditions.
- Specific requirements TBD pending permit application.

## NOT_TRACKED Dependencies

### Structural adjacency within PKG-005
- DEL-005-04 (Driving Surface Layout) shares the same package but no explicit information-flow dependency was identified beyond shared scope coverage.
- Not tracked because no explicit artifact transfer is stated in sources.

## Tracking Notes
Dependencies extracted from source documents on 2026-02-26 using CONSERVATIVE strictness. Dependencies will be updated as project progresses and scope is refined.

---

## Extracted Dependency Register

**Total rows:** 20
**ACTIVE rows:** 20
**RETIRED rows:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-005-03-001 | ANCHOR | IMPLEMENTS_NODE | UP | OTHER | WBS_NODE | SOW-0015 | ACTIVE |
| DEP-005-03-002 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-001 | ACTIVE |
| DEP-005-03-003 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-003 | ACTIVE |
| DEP-005-03-012 | ANCHOR | TRACES_TO_REQ | UP | OTHER | WBS_NODE | SOW-0020 | ACTIVE |
| DEP-005-03-013 | ANCHOR | TRACES_TO_REQ | UP | OTHER | WBS_NODE | SOW-0021 | ACTIVE |
| DEP-005-03-004 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-005-01 | ACTIVE |
| DEP-005-03-005 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-008-01 | ACTIVE |
| DEP-005-03-006 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-008-02 | ACTIVE |
| DEP-005-03-017 | EXECUTION | N/A | UP | CONSTRAINT | DELIVERABLE | DEL-021-04 | ACTIVE |
| DEP-005-03-007 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-005-02 | ACTIVE |
| DEP-005-03-008 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-005-06 | ACTIVE |
| DEP-005-03-014 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-005-05 | ACTIVE |
| DEP-005-03-010 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-018-05 | ACTIVE |
| DEP-005-03-015 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-001-02 | ACTIVE |
| DEP-005-03-016 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-006-03 | ACTIVE |
| DEP-005-03-020 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-018-06 | ACTIVE |
| DEP-005-03-018 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | R-07 | ACTIVE |
| DEP-005-03-019 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | R-04 | ACTIVE |
| DEP-005-03-009 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-018-02 | ACTIVE |
| DEP-005-03-011 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-009-02 | ACTIVE |

---

## Run Notes

**Run date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

**Defaults and paths used:**
- `RUN_ROOT`: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-03_Drainage-Plan`
- `DECOMPOSITION_PATH`: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md` (accessible, R1 2026-02-25)
- `SOURCE_DOCS`: AUTO resolved to: `Datasheet.md`, `Procedure.md`, `Specification.md`, `Guidance.md`
- `ANCHOR_DOC`: AUTO resolved to: `Datasheet.md` (matches `datasheet` heuristic; contains explicit SOW and OBJ identifiers)
- `EXECUTION_DOC_ORDER`: AUTO resolved to: `Procedure.md` (highest workflow clarity), `Specification.md`, `Guidance.md`
- `_REFERENCES.md`: present and read (used for R-04 and R-07 target location resolution)

**Assumptions:**
- ASSUMPTION: DEL-001-02 is the most relevant architectural deliverable for building footprint coordination (Procedure Step D2 references PKG-001 generically).
- ASSUMPTION: DEL-006-03 (Drain & Vent Plans) is the most relevant plumbing deliverable for floor drain coordination (Procedure Step D2 references PKG-006 generically).

**Warnings:**
- None. Decomposition accessible and all identifiers validated.

**Quality check results:**
- Schema: All 30 required columns present. CSV parseable.
- DependencyID uniqueness: PASS (20 unique IDs).
- Evidence coverage: PASS (all ACTIVE rows have EvidenceFile and SourceRef).
- Enum normalization: PASS (all enums canonical).
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-005-03-001).
- Duplicate check: PASS (no duplicate rows identified).
- Counts consistency: PASS (20 ACTIVE, 0 RETIRED matches CSV).

---

## Run History

| Run | Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | ACTIVE Total |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (R1) | None | 5 | 15 | 20 |

---

## Lifecycle Summary

**Extraction lifecycle:**
- ACTIVE: 20
- RETIRED: 0

**Closure lifecycle (SatisfactionStatus):**
- PENDING: 4 (DEP-005-03-004, DEP-005-03-005, DEP-005-03-006, DEP-005-03-017)
- TBD: 16

**By DependencyClass:**
- ANCHOR: 5 (1 IMPLEMENTS_NODE, 4 TRACES_TO_REQUIREMENT)
- EXECUTION: 15 (4 PREREQUISITE, 1 CONSTRAINT, 7 INTERFACE, 2 HANDOVER, 1 PREREQUISITE/DOCUMENT)

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

The following dependencies are flagged as relevant for task estimating readiness:

### BLOCKING dependencies (4)
These gate meaningful estimating because scope or key quantities are unknown without them:
1. **DEP-005-03-004** — DEL-005-01 (Preliminary Civil Design): County approval gates IFC release. Estimating should assume the preliminary design approval cycle is on the critical path.
2. **DEP-005-03-005** — DEL-008-01 (Geotechnical Report): Soil permeability and frost depth data govern drainage approach (surface vs. subsurface, infiltration feasibility, pipe invert depths). Quantities and material selections are uncertain until geotech data is available.
3. **DEP-005-03-006** — DEL-008-02 (Preliminary Site Survey): Existing topography governs drainage flow paths and grading quantities. Drainage element sizing depends on contributing catchment areas established from survey data.
4. **DEP-005-03-017** — DEL-021-04 (Contract Execution): Project-level gate; no work can proceed until contract is executed.

### BLOCKING downstream (1)
1. **DEP-005-03-009** — DEL-018-02 (Site Grading & Landscaping): PKG-018 construction team requires IFC drainage plan. Estimating for PKG-018 sitework should account for this dependency on completed drainage design.

### ADVISORY dependencies (7)
These are likely to change quantities, specs, or approach but are not hard gates for estimating:
1. **DEP-005-03-007** — DEL-005-02 (Site Grading Plan): Interdependent parallel production; grade consistency affects drainage element placement and quantities.
2. **DEP-005-03-008** — DEL-005-06 (Civil Calculation Package): Parallel production; sizing calculations affect material quantities.
3. **DEP-005-03-014** — DEL-005-05 (Civil Sections & Details): Cross-referenced sections may affect detail quantities.
4. **DEP-005-03-010** — DEL-018-05 (Wash Bay Drainage): Interface coordination may affect drainage detail scope (mud sump connection).
5. **DEP-005-03-015** — DEL-001-02 (Architectural Floor Plans): Building footprint coordination may affect drainage routing.
6. **DEP-005-03-016** — DEL-006-03 (Plumbing Drain & Vent Plans): Plumbing connection coordination may affect drainage detail scope.
7. **DEP-005-03-020** — DEL-018-06 (Utility Tie-Ins): Utility crossing clearance may affect drainage structure placement and depth.

### Key estimating uncertainty notes
- **Design storm return period (TBD):** The RFP does not specify a design storm return period or rainfall intensity. This is the single most consequential open normative parameter for drainage sizing. Until resolved, all drainage structure sizing is TBD and estimates should carry a range. (Specification REQ-002, Guidance Conflict C-001.)
- **Stormwater disposal method (TBD):** On-site detention vs. graded dispersal is not specified. Rural site with no confirmed municipal storm sewer. Approach selection materially affects scope and cost. (Guidance Conflict C-003.)
- **Aggregate specification (TBD):** County-supplied aggregate fines content affects runoff volume assumptions. (Guidance X-002.)
- **Geotechnical data (PENDING):** Complete geotech report not yet available. Drainage design may need revision after report. (Datasheet Conditions.)
