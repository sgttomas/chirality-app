# Dependencies

**Deliverable ID:** DEL-03-05
**Deliverable Name:** Electrical/IT Design Brief
**Package:** PKG-003 -- Design Brief
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total rows:** 10
**ACTIVE:** 10 | **RETIRED:** 0

### ANCHOR Edges (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-03-05-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0011 | HIGH |
| DEP-03-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | HIGH |

### EXECUTION Edges -- UPSTREAM (6 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-03-05-003 | PREREQUISITE | DELIVERABLE | DEL-02-05 (Electrical/IT Concept Narrative) | Concept rationale is foundation for brief justification; required before authoring | HIGH |
| DEP-03-05-004 | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Concept Package) | Roof orientation needed for solar-readiness provisions | HIGH |
| DEP-03-05-005 | PREREQUISITE | DELIVERABLE | DEL-02-04 (Mechanical Concept Narrative) | Generator sizing, critical loads, HVAC controls integration assumptions | HIGH |
| DEP-03-05-006 | CONSTRAINT | DOCUMENT | Addendum 03 | Binding requirements: solar-readiness (s1.17), generator (s1.15), site servicing (s1.6/s1.7) | HIGH |
| DEP-03-05-007 | PREREQUISITE | DOCUMENT | RFP Appendix B (Functional Program) | Zone-level program data for power and IT requirements | HIGH |
| DEP-03-05-008 | INTERFACE | DELIVERABLE | DEL-03-04 (Mechanical Design Brief) | Cross-check for generator integration, door openers, HVAC controls consistency | HIGH |

### EXECUTION Edges -- DOWNSTREAM (2 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-03-05-009 | HANDOVER | DELIVERABLE | DEL-04-03 (Electrical Energy Efficiency) | Design rationale (LED, controls, solar-ready) consumed by energy efficiency narrative | HIGH |
| DEP-03-05-010 | HANDOVER | DELIVERABLE | DEL-05-04 (Electrical Maintainability) | Maintainability-relevant design rationale consumed by maintainability narrative | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, 2026-02-17)
- SOURCE_DOCS: AUTO -- scanned deliverable folder, identified 4 source documents
- ANCHOR_DOC: `Datasheet.md` (contains identification fields, scope item, objective references)
- EXECUTION_DOC_ORDER: `Procedure.md` (strongest prerequisite/workflow signal), `Specification.md` (requirements with cross-references), `Guidance.md` (considerations and coordination)
- _REFERENCES.md: read for document pointer resolution (DEL-02-05, DEL-04-03 cross-references confirmed)

**Extraction Summary:**
- Pass 1 (ANCHOR): 2 rows extracted -- 1 IMPLEMENTS_NODE (SOW-0011), 1 TRACES_TO_REQUIREMENT (OBJ-004)
- Pass 2 (EXECUTION): 8 rows extracted -- 3 PREREQUISITE (upstream deliverables), 1 CONSTRAINT (Addendum 03), 1 PREREQUISITE (document), 1 INTERFACE (same-package), 2 HANDOVER (downstream deliverables)
- All targets resolved to known identifiers in Decomposition v2.3

**Integrity Checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 found -- PASS (no FLOATING_NODE warning)
- Multiple parent anchors: no -- PASS (no AMBIGUOUS_ANCHOR warning)
- DependencyID uniqueness: PASS (10 unique IDs)
- Required columns present: PASS (29 columns)
- All ACTIVE rows have EvidenceFile and SourceRef: PASS
- CSV parseable: PASS
- Counts consistent with this summary: PASS

**Warnings:** None.

**Assumptions:**
- Addendum 03 and RFP Appendix B are treated as DOCUMENT-type targets (not deliverables) since they are source/reference documents rather than project deliverables.
- DEL-03-04 (Mechanical Design Brief) is classified as UPSTREAM INTERFACE rather than PREREQUISITE because the Procedure describes a cross-check relationship (Step 10) rather than a strict sequential prerequisite. Both briefs are produced concurrently within PKG-003; the interface is for mutual consistency, not one-way information flow.

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 10 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |

---
