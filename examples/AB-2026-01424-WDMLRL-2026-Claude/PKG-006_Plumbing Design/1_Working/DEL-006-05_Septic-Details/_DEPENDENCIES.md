# Deliverable Dependencies: DEL-006-05

**Deliverable ID:** DEL-006-05
**Name:** Septic System Details
**Package:** PKG-006 Plumbing Design

---

## Declared Upstream Dependencies

- DEL-006-01 — Preliminary Plumbing Design (County approval required before final design)
- DEL-008-01 — Geotechnical Investigation & Report (subsurface conditions for bedding/backfill)
- DEL-006-03 — Drain & Vent Plans (building drain connection, invert elevations)
- DEL-006-06 — Plumbing Fixture Schedule (fixture unit count for tank sizing verification)
- DEL-005-01 — Preliminary Civil Design (site grading, drainage, driving surfaces coordination)
- PKG-004 — Electrical Design (alarm/level indicator — TBD)
- App B (Plumbing) — Conceptual plumbing drawing (tank location — available)

## Declared Downstream Dependencies

- DEL-009-03 — Safety Code Permits (IFC drawings submitted for permit application)
- DEL-014-02 — Septic System Installation (IFC drawing set to Plumbing Contractor)
- DEL-020-01 — Building Systems Commissioning (as-built verification records handover)

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 14
**ACTIVE:** 14 | **RETIRED:** 0

### ANCHOR Rows (4 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-006-05-001 | IMPLEMENTS_NODE | SOW-0016 | Complete final plumbing design | HIGH |
| DEP-006-05-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Code-compliant fully functional facility | HIGH |
| DEP-006-05-003 | TRACES_TO_REQUIREMENT | OBJ-003 | Complete P.Eng.-stamped IFC documentation | HIGH |
| DEP-006-05-004 | TRACES_TO_REQUIREMENT | OBJ-004 | Install and commission all plumbing and water systems | HIGH |

### EXECUTION Rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetName | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|
| DEP-006-05-005 | UPSTREAM | PREREQUISITE | Preliminary Plumbing Design (DEL-006-01) | HIGH | BLOCKING |
| DEP-006-05-006 | UPSTREAM | PREREQUISITE | Geotechnical Investigation & Report (DEL-008-01) | HIGH | ADVISORY |
| DEP-006-05-007 | UPSTREAM | INTERFACE | Drain & Vent Plans (DEL-006-03) | HIGH | ADVISORY |
| DEP-006-05-008 | UPSTREAM | INTERFACE | Plumbing Fixture Schedule (DEL-006-06) | MEDIUM | ADVISORY |
| DEP-006-05-009 | UPSTREAM | INTERFACE | Preliminary Civil Design (DEL-005-01) | HIGH | ADVISORY |
| DEP-006-05-010 | UPSTREAM | INTERFACE | PKG-004 Electrical Design | MEDIUM | TBD |
| DEP-006-05-011 | UPSTREAM | PREREQUISITE | Conceptual Plumbing Drawing (App B) | HIGH | INFO |
| DEP-006-05-012 | DOWNSTREAM | HANDOVER | Safety Code Permits (DEL-009-03) | HIGH | BLOCKING |
| DEP-006-05-013 | DOWNSTREAM | HANDOVER | Septic System Installation (DEL-014-02) | HIGH | BLOCKING |
| DEP-006-05-014 | DOWNSTREAM | HANDOVER | Building Systems Commissioning (DEL-020-01) | HIGH | ADVISORY |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Defaults and Paths Used

| Parameter | Value |
|---|---|
| SCOPE | DEL-006-05_Septic-Details |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-05_Septic-Details |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md |
| SOURCE_DOCS (AUTO) | Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| ANCHOR_DOC (AUTO) | Datasheet.md (selected: contains "datasheet" in filename; Identification table has explicit SOW and objective references) |
| EXECUTION_DOC_ORDER (AUTO) | Procedure.md, Guidance.md, Specification.md, Datasheet.md |
| _REFERENCES.md | Present — used for document pointer resolution (R-01, R-06) |

### Decomposition Validation

Decomposition document found and loaded. All target identifiers validated:
- SOW-0016: confirmed in Decomposition §3 SSOW and §8 Scope Ledger (maps to PKG-006, DEL-006-02 thru DEL-006-08)
- OBJ-001, OBJ-003, OBJ-004: confirmed in Decomposition §5 Objectives
- DEL-006-01, DEL-006-03, DEL-006-06, DEL-005-01, DEL-008-01: confirmed in Decomposition §7 Deliverables by Package
- DEL-009-03, DEL-014-02, DEL-020-01: confirmed in Decomposition §7 Deliverables by Package
- PKG-004, PKG-005: confirmed in Decomposition §6 Packages

### Warnings

None.

### Extraction Notes

- **DEP-006-05-010 (PKG-004 Electrical):** Recorded as `TargetType=PACKAGE` because the source text references PKG-004 broadly ("coordinate with PKG-004 Electrical Design") without identifying a specific deliverable. The dependency is conditional on whether an alarm/level indicator is required (TBD). Marked `Confidence=MEDIUM` and `EstimateImpactClass=TBD`.
- **DEP-006-05-006 (DEL-008-01 Geotech):** Source classifies as "SOFT" prerequisite (can proceed with conservative assumptions). Mapped to `DependencyType=PREREQUISITE` with `EstimateImpactClass=ADVISORY` rather than BLOCKING because scope/quantities are not gated by it.
- **DEP-006-05-011 (App B Plumbing):** This document input is already available; `SatisfactionStatus=SATISFIED`.
- **Pass 1 parent anchor:** Exactly 1 IMPLEMENTS_NODE row (SOW-0016). No FLOATING_NODE or AMBIGUOUS_ANCHOR warnings.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution |
|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | Loaded (WDMLRL_Decomposition_Claude.md R1) | None | 4 | 10 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **Total Rows** | 14 |
| **ACTIVE** | 14 |
| **RETIRED** | 0 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 10 | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| PENDING | 8 |
| TBD | 5 |
| SATISFIED | 1 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

The following observations are relevant for downstream task estimating workflows:

### Blocking Dependencies for Estimating

1. **DEP-006-05-005 (DEL-006-01 Preliminary Plumbing Design):** This is the single hard gate. County must approve preliminary design before final design proceeds. Estimating for DEL-006-05 cannot proceed meaningfully until the scope baseline from the preliminary design is established.

2. **DEP-006-05-012 (DEL-009-03 Safety Code Permits):** Downstream — IFC drawings from this deliverable are a required input for the Safety Code permit application. Permit timeline is dependent on this deliverable's completion.

3. **DEP-006-05-013 (DEL-014-02 Septic System Installation):** Downstream — construction cannot proceed without IFC drawings. This deliverable is on the critical path to construction start for the septic system.

### Advisory Dependencies for Estimating

4. **DEP-006-05-006 (DEL-008-01 Geotech):** Soft prerequisite. Design can proceed with conservative assumptions for bedding/backfill; geotech results may change material quantities and installation approach but do not gate the scope definition.

5. **DEP-006-05-007 (DEL-006-03 Drain & Vent Plans):** Interface — invert elevations are TBD. Estimating can proceed with placeholder elevations; final coordination required before IFC.

6. **DEP-006-05-008 (DEL-006-06 Fixture Schedule):** Interface — fixture unit count needed to verify 2,000 US gal tank is code-adequate. If count shows tank is undersized, a scope change discussion would be triggered.

7. **DEP-006-05-009 (DEL-005-01 Civil Design):** Interface — tank location and pump-out access depend on site grading. Estimating can proceed with conceptual location.

8. **DEP-006-05-014 (DEL-020-01 Commissioning):** Downstream — as-built records flow to commissioning. Advisory impact on estimating; does not affect design scope or quantities.

### Key Estimating Assumptions

- The deliverable scope is a **holding tank only** (no drain field, no treatment system). If AHJ requires a treatment system, this is a scope change.
- Tank capacity (2,000 US gal) is specified by the RFP. If code requires a larger tank, this is a scope change.
- Existing tank removal is IN scope; relocation is OUT of scope (County responsibility per D-002).
- Tank material is TBD (precast concrete, polyethylene, or fibreglass) — material selection will affect cost but not scope.
