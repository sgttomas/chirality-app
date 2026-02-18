# Dependencies

**Deliverable ID:** DEL-04-01
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Source:** `Dependencies.csv` (RegisterSchemaVersion v3.1)
**Total rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 12 |

### ANCHOR Rows (3)

| DependencyID | AnchorType | Direction | TargetType | TargetRefID / TargetName | Confidence |
|--------------|------------|-----------|------------|--------------------------|------------|
| DEP-04-01-001 | IMPLEMENTS_NODE | UPSTREAM | WBS_NODE | PKG-004 (Sustainability & Energy) | HIGH |
| DEP-04-01-002 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | SOW-0012 (Sustainability/energy narrative) | HIGH |
| DEP-04-01-003 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | OBJ-004 (Deliver a strong Design Brief) | HIGH |

### EXECUTION Rows (12)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|--------------|-----------|----------------|------------|--------|------------|
| DEP-04-01-004 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 (base RFP) | HIGH |
| DEP-04-01-005 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH |
| DEP-04-01-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 (Architectural Concept Package) | HIGH |
| DEP-04-01-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 (Mechanical Energy and Solar Readiness) | HIGH |
| DEP-04-01-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-03 (Electrical Energy Efficiency) | HIGH |
| DEP-04-01-009 | UPSTREAM | CONSTRAINT | EXTERNAL | NECB (National Energy Code for Buildings) | HIGH |
| DEP-04-01-010 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-02 (Mechanical Energy and Solar Readiness) | HIGH |
| DEP-04-01-011 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-03 (Electrical Energy Efficiency) | HIGH |
| DEP-04-01-012 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 (Architectural Durability and Maintenance) | HIGH |
| DEP-04-01-013 | UPSTREAM | CONSTRAINT | DOCUMENT | OSR (Appendix A) | MEDIUM |
| DEP-04-01-014 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 (Structural Concept Narrative) | MEDIUM |
| DEP-04-01-015 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 (Structural Design Brief) | MEDIUM |

---

## Run Notes

**Run date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE
**Decomposition path:** test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL)

**Defaults applied:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md (ANCHOR_DOC), Guidance.md, Procedure.md, Specification.md (EXECUTION_DOCS)
- DOC_ROLE_MAP: DEFAULT -- Datasheet.md matched ANCHOR_DOC pattern; Procedure.md, Guidance.md, Specification.md matched EXECUTION_DOC patterns
- ANCHOR_DOC: Datasheet.md (highest-confidence match)
- EXECUTION_DOC_ORDER: Procedure.md, Guidance.md, Specification.md

**Paths used:**
- Deliverable folder: test/execution-6b/PKG-004_Sustainability_and_Energy/1_Working/DEL-04-01_BuildingEnvelopeAndEnergyStrategy/
- Decomposition: test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md
- _REFERENCES.md: read (used for document pointer resolution)

**Anchor validation (against Decomposition):**
- PKG-004 confirmed in Decomposition Section 8 (Package definitions)
- DEL-04-01 confirmed in Decomposition Section 9 (Deliverable definitions, under PKG-004)
- SOW-0012 confirmed in Decomposition Section 10 (Scope Ledger, mapped to PKG-004 / DEL-04-01)
- OBJ-004 confirmed in Decomposition Section 6 (Objectives table)

**Target resolution notes:**
- DEL-02-01 resolved to PKG-002 via Decomposition Section 9
- DEL-04-02 resolved to PKG-004 via Decomposition Section 9
- DEL-04-03 resolved to PKG-004 via Decomposition Section 9
- DEL-05-01 resolved to PKG-005 via Decomposition Section 9
- DEL-02-03 resolved to PKG-002 via Decomposition Section 9
- DEL-03-03 resolved to PKG-003 via Decomposition Section 9
- NECB: TargetType=EXTERNAL; not a deliverable; location TBD (not in project sources)
- OSR (Appendix A): TargetType=DOCUMENT; embedded in RFP; specific section references location TBD

**Warnings:** None.

**Integrity checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 found -- PASS
- Multiple parent anchors: No -- PASS
- DependencyID uniqueness: 15 unique / 15 total -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef: PASS
- FromDeliverableID consistency: all rows = DEL-04-01 -- PASS
- Schema version: all rows v3.1 -- PASS
- Enum normalization: all Direction values canonical (UPSTREAM/DOWNSTREAM) -- PASS

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|-----------|------|------------|---------------|----------|---------------|------------------|--------------|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 3 | 12 | 15 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 15 |

---
