# Blockers Report — DEL-02-01 Architectural Concept Package

**Note:** These are execution/production blockers identified from dependency evidence, NOT pricing blockers. All 4 line items in this estimate are fully priced.

---

## Upstream Interface Dependencies (Execution Sequencing)

These deliverables must provide input data before DEL-02-01 drawings can be finalized:

| DependencyID | Source Deliverable | Required Input | Impact |
|---|---|---|---|
| DEP-0201-E01 | DEL-02-02 (Civil/Site Concept Plan) | 12-acre developable area boundary; building footprint placement; parking layout; fire access routes; utility connection points; Cold Storage placement | Floor plan layout and site plan drawing cannot be finalized without site boundary and placement inputs |
| DEP-0201-E02 | DEL-02-03 (Structural Concept Narrative) | Proposed structural system; column grid layout overlay; slab sump integration zones; floor-to-floor heights; geotechnical assumptions | Column grid governs architectural floor plan layout |
| DEP-0201-E03 | DEL-02-04 (Mechanical Concept Narrative) | Apparatus bay direct exhaust strategy; bunker gear room ventilation approach; generator location; fill station locations; mechanical room sizing; sump drainage strategy | Ductwork zones and mechanical room sizing must be spatially reserved on floor plan |
| DEP-0201-E04 | DEL-02-05 (Electrical/IT Concept Narrative) | Solar-capable roof orientation decision; electrical room location and size; generator connection point and ATS location; access control device locations | Solar orientation governs elevation design; electrical room must be reserved on floor plan |

## Upstream Prerequisite Documents

| DependencyID | Document | Status | Impact |
|---|---|---|---|
| DEP-0201-E05 | RFP Appendix A -- Owner Statement of Requirements (OSR) | PENDING | Gated prerequisite (V-00): bay count and operational requirements must be extracted before floor plan layout proceeds |
| DEP-0201-E06 | RFP Appendix B -- Functional Program | PENDING | Gated prerequisite (V-00): complete room list must be extracted before program analysis |

## Upstream Constraint

| DependencyID | Document | Impact |
|---|---|---|
| DEP-0201-E07 | RFP Addendum 03 (Jul 31, 2024) | Governs room sizing ranges and special requirements; addendum values override base RFP |

---

## Summary

- **4 interface dependencies** with sibling PKG-002 deliverables (design data exchange)
- **2 prerequisite documents** with PENDING satisfaction status
- **1 governing constraint** document (Addendum 03)
- **None of these blockers affect the cost estimate.** They affect execution sequencing and readiness for production.
