# Blockers Report -- EST_DEL-02-03_2026-02-18_1500

## DEL-02-03: Sustainability & Energy Narrative

**Source:** Dependencies.csv (AUTO mode; 11 rows extracted)

---

## BLOCKING Dependencies (EstimateImpactClass = BLOCKING)

These dependencies are flagged as BLOCKING in the dependency register and may affect the ability to finalize deliverable content. They do not block the cost estimate itself (hours and rates are pre-determined), but they indicate unresolved inputs for narrative production.

### DEP-0004: DEL-02-01 ConceptDesignPackage (UPSTREAM INTERFACE)

- **What is needed:** Building orientation, massing, and roof configuration from DEL-02-01
- **Why blocking:** Solar-ready roof orientation and energy narrative alignment cannot be specified without knowing the building orientation from the concept design
- **SatisfactionStatus:** TBD
- **Evidence:** Datasheet.md; Specification.md REQ-003.3; Guidance.md CONF-001

### DEP-0010: RFP Appendix A -- OSR (UPSTREAM PREREQUISITE)

- **What is needed:** Energy performance targets, code requirements (ABC / NECB edition), LEED requirements, sustainability performance criteria
- **Why blocking:** Cannot establish code compliance baseline without confirmed code editions from the OSR
- **SatisfactionStatus:** TBD
- **Evidence:** Procedure.md Prerequisites; Datasheet.md; Specification.md Standards section

### DEP-0011: RFP Addendum 03 (UPSTREAM CONSTRAINT)

- **What is needed:** Confirmed mandatory constraints: solar capable roofing provisions, 16-ft overhead doors, bay sumps, fire apparatus exhaust, generator for ICP, fill stations
- **Why blocking:** All must be addressed in the narrative per Addendum 03 mandate
- **SatisfactionStatus:** TBD
- **Evidence:** Specification.md REQ-001.1, REQ-002.2, REQ-002.4, REQ-003.1-003.5, REQ-004.3, REQ-007.1

---

## ADVISORY Dependencies (EstimateImpactClass = ADVISORY)

These are coordination or scope-boundary dependencies that inform narrative authoring but do not constitute hard gates.

| DependencyID | Target | Direction | Type | Note |
|-------------|--------|-----------|------|------|
| DEP-0005 | DEL-02-02 (Design Brief Narrative) | UPSTREAM | INTERFACE | Scope boundary: DEL-02-02 = materials/durability; DEL-02-03 = energy/sustainability |
| DEP-0006 | DEL-09-02 (Site Conditions) | UPSTREAM | INTERFACE | Site constraints for stormwater/water efficiency section |
| DEP-0007 | DEL-06-01 (Commissioning) | DOWNSTREAM | INTERFACE | DEL-02-03 provides high-level commissioning role; DEL-06-01 expands to detail |

---

## INFO Dependencies (EstimateImpactClass = INFO)

| DependencyID | Target | Direction | Type | Note |
|-------------|--------|-----------|------|------|
| DEP-0008 | DEL-01-01 (Compliance Matrix) | DOWNSTREAM | HANDOVER | DEL-02-03 produces compliance mapping table for integration |
| DEP-0009 | DEL-01-02 (Formal Submission Package) | DOWNSTREAM | HANDOVER | Final narrative delivered for proposal PDF assembly |

---

## Summary

| Impact Class | Count | Unresolved |
|-------------|-------|-----------|
| BLOCKING | 3 | 3 (all TBD) |
| ADVISORY | 3 | N/A (coordination) |
| INFO | 2 | N/A (downstream) |
| **Total** | **8** | **3 unresolved blockers** |

**Assessment:** The 3 BLOCKING dependencies relate to narrative content production inputs (building orientation, code edition, Addendum 03 constraints). They do not affect the cost estimate computation (hours x rates). The estimate total of $4,770 is valid as a production cost regardless of blocker resolution status.
