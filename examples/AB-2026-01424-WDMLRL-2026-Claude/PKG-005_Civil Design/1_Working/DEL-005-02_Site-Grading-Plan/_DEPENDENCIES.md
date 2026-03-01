# DEL-005-02 Dependencies

## Upstream Dependencies

### DEL-008-01 -- Geotechnical Investigation & Report (PKG-008)
- Required before subgrade/compaction grading notes can be finalized
- Status: PENDING

### DEL-008-02 -- Preliminary Site Survey (PKG-008)
- Required before grading design can commence; provides existing topography and control points
- Status: PENDING

### DEL-005-01 -- Preliminary Civil Design (PKG-005)
- County approval of preliminary design required before IFC grading design proceeds
- Status: PENDING

### DEL-002-02 -- Foundation Plan (PKG-002)
- Building pad / finished floor elevations required as grading control input (ASSUMPTION)
- Status: TBD

### DEL-001-02 -- Architectural Floor Plans (PKG-001)
- Finished floor elevations needed as grading control input (ASSUMPTION)
- Status: TBD

## Downstream Dependencies

### DEL-005-03 -- Drainage Plan (PKG-005)
- Drainage plan depends on grading plan surface grades for flow paths and collection points

### DEL-018-02 -- Site Grading & Landscaping (PKG-018)
- IFC grading plan issued to sitework contractor for construction

## Internal Dependencies

- Coordinate with DEL-005-03 (Drainage Plan) for drainage feature locations and inverts
- Coordinate with DEL-005-04 (Driving Surface Layout) for grade consistency

## External Dependencies

- County bulk earthwork (brushing/clearing and bulk cut/fill) must be completed before proponent grading design is implemented (R-01 S3.3.1)
- County approval tracked via DEL-005-01 gate

## NOT_TRACKED Dependencies
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
| ANCHOR rows | 5 |
| EXECUTION rows | 8 |

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-005-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0015 | ACTIVE |
| DEP-005-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | ACTIVE |
| DEP-005-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 | ACTIVE |
| DEP-005-02-011 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | WBS_NODE | SOW-0020 | ACTIVE |
| DEP-005-02-012 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | WBS_NODE | SOW-0021 | ACTIVE |
| DEP-005-02-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 | ACTIVE |
| DEP-005-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 | ACTIVE |
| DEP-005-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-01 | ACTIVE |
| DEP-005-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-02 | ACTIVE |
| DEP-005-02-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 | ACTIVE |
| DEP-005-02-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-005-03 | ACTIVE |
| DEP-005-02-010 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-018-02 | ACTIVE |
| DEP-005-02-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | EXTERNAL | County Bulk Earthwork | ACTIVE |

---

## Run Notes

- **Run Date:** 2026-02-26 (refresh run)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **SOURCE_DOCS:** AUTO -- Datasheet.md, Specification.md, Procedure.md, Guidance.md, _CONTEXT.md, _REFERENCES.md
- **ANCHOR_DOC:** Datasheet.md (selected by heuristic: filename contains 'datasheet')
- **EXECUTION_DOC_ORDER:** Procedure.md, Guidance.md, Specification.md, Datasheet.md (Procedure first as primary execution workflow doc)
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1 -- 2026-02-25)
- **Decomposition status:** Available; anchor validation successful
- **Parent anchor:** SOW-0015 confirmed in Scope Ledger (PKG-005, DEL-005-02); decomposition line 424 and Scope Ledger line 610 confirm assignment
- **Changes from prior run:**
  - Added DEP-005-02-011 (ANCHOR / TRACES_TO_REQUIREMENT for SOW-0020) -- explicitly cited in Datasheet Attributes, Specification REQ-001, and decomposition Scope Ledger
  - Added DEP-005-02-012 (ANCHOR / TRACES_TO_REQUIREMENT for SOW-0021) -- explicitly cited in Datasheet Attributes, Specification REQ-002, and decomposition Scope Ledger
  - Added DEP-005-02-013 (EXECUTION / UPSTREAM / CONSTRAINT for County Bulk Earthwork) -- Guidance Principle 4 explicitly describes this external constraint with specific handoff boundary implications
  - Enriched Notes and SourceRef fields on existing rows with additional cross-references found in Specification and Guidance documents
- No warnings.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (R1) | None | 10 |
| 2026-02-26 (refresh) | UPDATE | CONSERVATIVE | Available (R1) | None | 13 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |
| PENDING | 3 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

**BLOCKING dependencies (gate meaningful estimating):**
- **DEL-008-01** (Geotechnical Report) -- subgrade and compaction specifications directly affect earthwork quantities. Without the final geotech report, compaction density, lift thickness, and subgrade preparation depths cannot be specified, making earthwork quantity estimating unreliable.
- **DEL-008-02** (Preliminary Site Survey) -- existing topography is required to calculate cut/fill volumes. Without survey data, earthwork quantities cannot be estimated.
- **DEL-005-01** (Preliminary Design approval) -- gates all IFC design work. Until County approves the preliminary civil design, the final grading design scope is not confirmed.
- **DEL-018-02** (downstream) -- sitework construction estimating depends on receipt of the grading IFC. This deliverable is on the critical path to construction.

**ADVISORY dependencies (may change quantities/specs):**
- **DEL-002-02** and **DEL-001-02** -- building pad and finished floor elevations affect grading control elevations and may change earthwork quantities near the building footprint.
- **DEL-005-03** -- drainage plan coordination may affect grading feature quantities (drainage swale/berm extents integrated into grading).
- **County Bulk Earthwork** (EXTERNAL) -- the acceptance condition for County-completed bulk earthwork (tolerances, as-built data) affects the scope boundary between County work and proponent grading work. If the County handoff condition is poorly defined, residual earthwork quantities may shift to the proponent.
