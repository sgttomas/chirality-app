# DEL-005-01 Dependencies

## Upstream Dependencies
Section for deliverables or work items that must be completed before this deliverable can proceed.

### DEL-008-02 — Preliminary Site Survey (PKG-008)
- Required input for existing topography and site control
- Status: PENDING

### DEL-008-01 — Geotechnical Investigation & Report (PKG-008)
- Preferred input for subgrade design parameters; design proceeds on conservative assumptions if unavailable
- Status: PENDING

### PKG-002 — Structural Design (DEL-002-02 Foundation Plan)
- Interface coordination for mud sump structural design and foundation perimeter drainage
- Status: TBD

### PKG-006 — Plumbing Design
- Interface coordination for mud sump connection to wash bay drainage (plumbing interface)
- Status: TBD

### PKG-007 — Landscape Architectural Design
- Interface coordination at grading/landscaping boundary
- Status: TBD

### Camrose County — Approval Authority
- County approval of preliminary civil design required before final design proceeds
- Status: PENDING

### Mandatory Site Meeting — March 3, 2026
- Required per RFP section 3.2; non-attendance disqualifies proposal
- Design vehicle confirmation, scope boundary verification, and County preferences expected
- Status: PENDING

## Downstream Dependencies
Section for deliverables or work items that depend on this deliverable.

### DEL-005-02 through DEL-005-07 (PKG-005 Final Civil Design)
- County approval of DEL-005-01 is a gate before all final civil design deliverables can proceed to IFC
- Impact if delayed: All PKG-005 IFC deliverables blocked

## Internal Dependencies
Section for dependencies between tasks within this deliverable package.

- None identified at this time.

## External Dependencies
Section for dependencies external to the project (regulatory, third-party, etc.).

### Mandatory Site Meeting — March 3, 2026
- Required per RFP section 3.2; non-attendance disqualifies proposal
- Status: PENDING

### RFP Document and Addenda (R-01, R-02)
- Primary design input; available
- Status: SATISFIED

### Appendix B Conceptual Drawings (R-04, R-05, R-06)
- Spatial context for preliminary civil design layout; available
- Status: SATISFIED

## NOT_TRACKED Dependencies
Items intentionally not tracked in this template but documented elsewhere.

- None identified.

## Tracking Notes
Dependencies will be updated as project progresses and scope is refined.

---

## Extracted Dependency Register

| Metric | Count |
|---|---|
| Total rows | 13 |
| ACTIVE | 13 |
| RETIRED | 0 |
| ANCHOR rows | 3 |
| EXECUTION rows | 10 |

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Status | EstImpact |
|---|---|---|---|---|---|---|---|---|
| DEP-005-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0010e | ACTIVE | |
| DEP-005-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | ACTIVE | |
| DEP-005-01-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 | ACTIVE | |
| DEP-005-01-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 | ACTIVE | BLOCKING |
| DEP-005-01-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 | ACTIVE | ADVISORY |
| DEP-005-01-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | R-01 (RFP) | ACTIVE | INFO |
| DEP-005-01-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-02 | ACTIVE | ADVISORY |
| DEP-005-01-008 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-005-02 | ACTIVE | BLOCKING |
| DEP-005-01-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | PACKAGE | PKG-007 | ACTIVE | INFO |
| DEP-005-01-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | EXTERNAL | Camrose County | ACTIVE | BLOCKING |
| DEP-005-01-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | EXTERNAL | Site Meeting Mar 3 | ACTIVE | BLOCKING |
| DEP-005-01-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | R-04 (App B) | ACTIVE | INFO |
| DEP-005-01-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | PACKAGE | PKG-006 | ACTIVE | ADVISORY |

---

## Run Notes

- **Run Date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO — scanned Datasheet.md, Specification.md, Procedure.md, Guidance.md, _REFERENCES.md, _CONTEXT.md
- **ANCHOR_DOC:** Datasheet.md (contains explicit SOW and OBJ references in Identification table)
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md, Datasheet.md
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1 — 2026-02-25)
- **Decomposition status:** Available; anchor validation and target resolution performed successfully
- **Parent anchor:** SOW-0010e confirmed in decomposition Scope Ledger (PKG-005, DEL-005-01)
- **Objective anchors:** OBJ-001 and OBJ-003 confirmed in decomposition Objectives section
- **Deliverable targets resolved:** DEL-008-02, DEL-008-01, DEL-002-02, DEL-005-02 confirmed in decomposition Deliverables by Package section
- **Package targets resolved:** PKG-007, PKG-006 confirmed in decomposition Packages section
- **New rows this run:** DEP-005-01-011 (mandatory site meeting constraint), DEP-005-01-012 (Appendix B drawings prerequisite), DEP-005-01-013 (PKG-006 plumbing interface)
- **Retired rows this run:** None
- No warnings.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1) | None | 10 |
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1) | None | 13 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 7 |
| PENDING | 4 |
| SATISFIED | 2 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

Key dependencies affecting estimating readiness for DEL-005-01:

- **BLOCKING:** Mandatory Site Meeting (March 3, 2026) — design vehicle confirmation, scope boundary verification, and County preferences are required inputs that directly affect estimating scope. Non-attendance disqualifies the proposal entirely.
- **BLOCKING:** DEL-008-02 (Preliminary Site Survey) — required input for site grading strategy; scope quantities for grading cannot be estimated without survey data.
- **BLOCKING:** County approval constraint — estimating for final civil design (DEL-005-02 through DEL-005-07) is gated on County approval of this deliverable.
- **BLOCKING:** DEL-005-01 enables DEL-005-02 through DEL-005-07 — all downstream civil design estimating depends on preliminary design approval.
- **ADVISORY:** DEL-008-01 (Geotechnical Report) — subgrade design parameters affect driving surface quantities and cross-section thickness; design can proceed on conservative assumptions but estimates may change when geotech data arrives.
- **ADVISORY:** PKG-002 interface (DEL-002-02) — mud sump structural coordination may affect civil scope quantities for sump surrounds and excavator access grading.
- **ADVISORY:** PKG-006 interface — plumbing/wash bay drainage coordination may affect mud sump sizing and surface drainage design at the building/site boundary.
- **INFO:** R-01 (RFP) and R-04 (Appendix B) — primary design inputs; both available and satisfied.
- **INFO:** PKG-007 interface — landscape/civil boundary coordination; low impact on civil estimating totals at preliminary stage.
