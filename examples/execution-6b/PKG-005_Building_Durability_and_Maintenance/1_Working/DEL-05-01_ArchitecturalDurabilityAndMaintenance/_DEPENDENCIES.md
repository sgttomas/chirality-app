# Dependencies

**Deliverable ID:** DEL-05-01
**Deliverable Name:** Architectural Durability and Maintenance
**Package:** PKG-005 -- Building Durability & Maintenance
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 10
**Total RETIRED rows:** 0

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-05-01-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-005 -- Building Durability & Maintenance | HIGH | ACTIVE |
| DEP-05-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0013 -- Building durability/ease of repair and maintenance narrative | HIGH | ACTIVE |
| DEP-05-01-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 -- Demonstrate durability and ease of maintenance (15 pts) | HIGH | ACTIVE |

### EXECUTION Dependencies (7 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-05-01-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Concept Package | HIGH | ACTIVE |
| DEP-05-01-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 Structural Durability and Maintenance | HIGH | ACTIVE |
| DEP-05-01-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 Mechanical Maintainability | HIGH | ACTIVE |
| DEP-05-01-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 Electrical Maintainability | HIGH | ACTIVE |
| DEP-05-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP AB-2024-07156 | HIGH | ACTIVE |
| DEP-05-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH | ACTIVE |
| DEP-05-01-010 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 Formal Submission Package | HIGH | ACTIVE |

---

## Run Notes

**Run timestamp:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

### Defaults and Paths Used

- **DECOMPOSITION_PATH:** `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located; version v2.3 FINAL)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents:
  - `Datasheet.md` (ANCHOR_DOC -- primary anchor/definition signals)
  - `Specification.md` (EXECUTION_DOC -- requirements with cross-references)
  - `Procedure.md` (EXECUTION_DOC -- workflow steps with explicit prerequisites and handoffs)
  - `Guidance.md` (EXECUTION_DOC -- design principles with coordination considerations)
- **ANCHOR_DOC:** `Datasheet.md` (selected: contains Identification table with Package, Scope Item, Objective, and RFP Section references)
- **EXECUTION_DOC_ORDER:** `Procedure.md`, `Specification.md`, `Guidance.md` (Procedure prioritized for workflow clarity; Specification for requirements-level cross-references; Guidance for coordination considerations)
- **_REFERENCES.md:** Read; used to confirm cross-references to DEL-02-01 and DEL-05-02

### Assumptions

- All ANCHOR targets (PKG-005, SOW-0013, OBJ-005) validated against Decomposition sections 8, 7, and 6 respectively. All confirmed present.
- DEL-02-01 classified as PREREQUISITE (not merely INTERFACE) because Procedure Step A2 explicitly requires extracting material selections from it as an input action step, not just coordination.
- DEL-05-02, DEL-05-03, and DEL-05-04 classified as INTERFACE because Procedure Steps A3-A4 and Specification D-002 describe bidirectional coordination meetings producing shared design decisions, not a unidirectional input.
- RFP and Addendum 03 classified as DOCUMENT type PREREQUISITE dependencies because they are the authoritative source documents required before any work can proceed.
- DEL-01-02 classified as DOWNSTREAM HANDOVER because Procedure Step A7 explicitly states the final narrative is delivered for integration into the formal submission package.

### Warnings

None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution |
|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 3 | 7 |

---

## Lifecycle Summary

| Category | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 7 | 0 |
| **Total** | **10** | **0** |

### Satisfaction Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |

---
