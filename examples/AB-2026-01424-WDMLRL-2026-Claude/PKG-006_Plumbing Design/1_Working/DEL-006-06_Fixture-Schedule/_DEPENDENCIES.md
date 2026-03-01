# Deliverable Dependencies: DEL-006-06

**Deliverable ID:** DEL-006-06_Fixture-Schedule
**Name:** Plumbing Fixture Schedule
**Package:** PKG-006 — Plumbing Design

---

## Declared Upstream Dependencies

*(Human-owned section. Add manually declared upstream dependencies here.)*

- None declared yet.

## Declared Downstream Dependencies

*(Human-owned section. Add manually declared downstream dependencies here.)*

- None declared yet.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 15 (3 ANCHOR + 12 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Dependencies (Tree Edges)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-006-06-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0016 | Complete final plumbing design (water supply; drainage; septic) | HIGH |
| DEP-006-06-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-006-06-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | Install and commission all plumbing systems to operational readiness | HIGH |

### EXECUTION Dependencies (DAG Edges) — Upstream

| DependencyID | DependencyType | TargetType | TargetID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-06-004 | PREREQUISITE | DELIVERABLE | DEL-001-02 | Architectural Floor Plans | HIGH | BLOCKING |
| DEP-006-06-005 | PREREQUISITE | DELIVERABLE | DEL-001-10 | Old North Shop Renovation Plans | HIGH | BLOCKING |
| DEP-006-06-006 | CONSTRAINT | DELIVERABLE | DEL-006-01 | Preliminary Plumbing Design (approval required) | HIGH | BLOCKING |
| DEP-006-06-007 | INTERFACE | DELIVERABLE | DEL-006-02 | Water Distribution Plans | MEDIUM | ADVISORY |
| DEP-006-06-008 | INTERFACE | DELIVERABLE | DEL-006-03 | Drain & Vent Plans | MEDIUM | ADVISORY |
| DEP-006-06-009 | INTERFACE | DELIVERABLE | DEL-006-04 | Cistern & Pump Details | MEDIUM | ADVISORY |
| DEP-006-06-010 | INTERFACE | DELIVERABLE | DEL-006-07 | Plumbing Calculation Package | MEDIUM | ADVISORY |
| DEP-006-06-011 | INTERFACE | DELIVERABLE | DEL-008-01 | Geotechnical Investigation & Report | MEDIUM | INFO |
| DEP-006-06-014 | PREREQUISITE | DOCUMENT | R-06 | Appendix B (Plumbing) — Conceptual Drawing | HIGH | INFO |
| DEP-006-06-015 | PREREQUISITE | DOCUMENT | R-01 | RFP — AB-2026-01424-WDMLRL | HIGH | INFO |

### EXECUTION Dependencies (DAG Edges) — Downstream

| DependencyID | DependencyType | TargetType | TargetID | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-06-012 | INTERFACE | DELIVERABLE | DEL-006-05 | Septic System Details | MEDIUM | ADVISORY |
| DEP-006-06-013 | HANDOVER | PACKAGE | PKG-014 | Plumbing & Water Systems Installation | HIGH | BLOCKING |

---

## Run Notes

**Run timestamp:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** TASK_ESTIMATING

### Defaults and Paths Used

| Setting | Value | Resolution |
|---|---|---|
| RUN_ROOT | `PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule` | Provided by invoker |
| DECOMPOSITION_PATH | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Provided by invoker; file found and read successfully |
| SOURCE_DOCS | AUTO | Resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md |
| ANCHOR_DOC | AUTO | Resolved to: `Datasheet.md` (contains identification table with SOW/OBJ references) |
| EXECUTION_DOC_ORDER | AUTO | Resolved to: `Procedure.md`, `Specification.md`, `Guidance.md` |
| _REFERENCES.md | Present | Used for document location resolution (R-01, R-06 paths) |

### Assumptions

- ASSUMPTION: Concurrent PKG-006 internal interfaces (DEL-006-02, DEL-006-03, DEL-006-04, DEL-006-07) are bidirectional in practice but modeled as UPSTREAM from the perspective of this deliverable, since the Procedure Prerequisites table lists them as required information inputs. Confidence set to MEDIUM because concurrent production means the flow direction is not strictly sequential.
- ASSUMPTION: DEL-008-01 (Geotech Report) is classified as INFO impact because the Procedure states "For information; affects drainage design" — indirect influence on fixture schedule content.
- ASSUMPTION: Document dependencies R-01 and R-06 are marked SATISFIED because the Procedure Prerequisites table shows their status as "Available."

### Warnings

- None. All quality checks passed.

### Excluded Items (not extracted)

The following coordination relationships were identified in source documents but excluded because they do not represent explicit information/artifact transfer from or to this deliverable:

- PKG-002 (Structural) — "Floor drain sleeve and penetration coordination" (Datasheet.md Coordination table). Coordination-only; no explicit artifact transfer stated.
- PKG-003 (Mechanical) — "Washroom ventilation coordination" (Datasheet.md Coordination table). Coordination-only.
- PKG-004 (Electrical) — "Pump motor electrical requirements; emergency shower lighting" (Datasheet.md Coordination table). Coordination-only; emergency shower heat tracing is a design question, not an explicit artifact flow from this schedule.
- Procedure Step 6 coordination review with PKG-001, PKG-003, PKG-004 — review/signoff process, not a persistent information handover.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Available (WDMLRL_Decomposition_Claude.md) | None | 3 | 12 | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

### Closure-State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 3 |
| PENDING | 10 |
| SATISFIED | 2 |

**Notes:**
- 3 ANCHOR rows have `SatisfactionStatus=TBD` (anchors are structural, not action items).
- 10 EXECUTION rows have `SatisfactionStatus=PENDING` (deliverable/package dependencies not yet fulfilled).
- 2 EXECUTION rows have `SatisfactionStatus=SATISFIED` (R-01 RFP and R-06 App B-Plumbing are available source documents).

---

## Downstream Handoff Notes

**Consumer context:** TASK_ESTIMATING

### Estimating-Relevant Dependencies

The following dependencies are flagged as relevant to task estimating readiness:

**BLOCKING (3 rows):** These gate meaningful estimating because scope or key quantities are unknown without them.
- DEP-006-06-004: Architectural Floor Plans (DEL-001-02) — fixture locations depend on room layouts; without confirmed plans, fixture counts and types cannot be finalized for estimating.
- DEP-006-06-005: Old North Shop Renovation Plans (DEL-001-10) — renovation fixture scope (washroom, urinal, laundry) cannot be quantified without confirmed renovation plans.
- DEP-006-06-006: Preliminary Plumbing Design approval (DEL-006-01) — approval gate before IFC issue; estimating can proceed with preliminary quantities but final scope confirmation is blocked.

**BLOCKING (1 downstream row):**
- DEP-006-06-013: Handover to PKG-014 (Plumbing Installation) — the fixture schedule is a critical input for plumbing installation contractor pricing and procurement. Estimating for PKG-014 is blocked without this deliverable.

**ADVISORY (5 rows):** These interfaces likely affect quantities or specifications but are not hard gates.
- DEP-006-06-007 through DEP-006-06-010: Concurrent PKG-006 internal interfaces (water distribution, drain/vent, cistern/pump, calculations). Changes in these deliverables may affect fixture specifications and quantities.
- DEP-006-06-012: Downstream interface to DEL-006-05 (Septic) — fixture drainage loads inform septic sizing.

**INFO (3 rows):** Low likelihood of changing estimating totals.
- DEP-006-06-011: Geotechnical report — indirect influence on drainage design.
- DEP-006-06-014, DEP-006-06-015: Source documents (R-06, R-01) — already available.
