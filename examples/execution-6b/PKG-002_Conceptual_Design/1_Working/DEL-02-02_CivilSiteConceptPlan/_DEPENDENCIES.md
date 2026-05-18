# Dependencies

**Deliverable ID:** DEL-02-02
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here. Extracted dependencies are maintained in Dependencies.csv.

---

## Extracted Dependency Register

**Total Rows:** 19
**ACTIVE:** 19 | **RETIRED:** 0

### ANCHOR Dependencies (4 rows)

| DependencyID | AnchorType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-02-02-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-002 -- Conceptual Design | HIGH | ACTIVE |
| DEP-02-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0009 | HIGH | ACTIVE |
| DEP-02-02-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0010 | HIGH | ACTIVE |
| DEP-02-02-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 | HIGH | ACTIVE |

### EXECUTION Dependencies (15 rows)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|
| DEP-02-02-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Concept Package | HIGH | ACTIVE |
| DEP-02-02-006 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 (Jul 10 2024) | HIGH | ACTIVE |
| DEP-02-02-007 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH | ACTIVE |
| DEP-02-02-008 | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading TPN46 (Tagish Engineering Jan 6 2022) | HIGH | ACTIVE |
| DEP-02-02-009 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Report USG1123 (Union Street Geotechnical Feb 12 2021) | HIGH | ACTIVE |
| DEP-02-02-010 | UPSTREAM | PREREQUISITE | DOCUMENT | Wetland Assessment Ghostpine Project 5646 (Aug 11 2021) | HIGH | ACTIVE |
| DEP-02-02-011 | UPSTREAM | PREREQUISITE | DOCUMENT | Flood Zone Map (Town of Penhold) | HIGH | ACTIVE |
| DEP-02-02-012 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B RFP p.46) | HIGH | ACTIVE |
| DEP-02-02-013 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 Structural Concept Narrative | HIGH | ACTIVE |
| DEP-02-02-014 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-04 Mechanical Concept Narrative | HIGH | ACTIVE |
| DEP-02-02-015 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Electrical/IT Concept Narrative | HIGH | ACTIVE |
| DEP-02-02-016 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-02 Civil Design Brief | HIGH | ACTIVE |
| DEP-02-02-017 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-10-02 Site Conditions and Due Diligence Summary | MEDIUM | ACTIVE |
| DEP-02-02-018 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-10-01 Risk Register and Mitigation Plan | HIGH | ACTIVE |
| DEP-02-02-019 | UPSTREAM | CONSTRAINT | EXTERNAL | DEC-013 -- No additional geotechnical investigation | HIGH | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 19 |
| **RETIRED** | 0 |
| **Total** | 19 |

### By DependencyClass

| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 4 | 0 |
| EXECUTION | 15 | 0 |

### By SatisfactionStatus

| Status | Count |
|---|---|
| TBD | 19 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located successfully)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents: Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **ANCHOR_DOC:** Datasheet.md (selected: contains `datasheet` keyword; highest confidence for definition/traceability signal)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity)
- **_REFERENCES.md:** Read; used to corroborate DEL-02-01 and DEL-10-02 cross-references

### Extraction Notes

- **Pass 1 (ANCHOR):** 4 rows extracted. Parent anchor (IMPLEMENTS_NODE) resolved to PKG-002 via decomposition Section 9. Three trace anchors: SOW-0009, SOW-0010, OBJ-003 -- all confirmed in decomposition Scope Ledger (lines 669-670) and Objectives (Section 6).
- **Pass 2 (EXECUTION):** 15 rows extracted. One critical-path deliverable prerequisite (DEL-02-01, building footprint). Seven document prerequisites explicitly listed in Procedure.md Prerequisites table. Three cross-discipline interfaces (DEL-02-03, DEL-02-04, DEL-02-05) from Specification R-19. Two downstream handovers (DEL-03-02 civil design brief, DEL-10-01 risk register) from Datasheet Related Deliverables. One upstream deliverable input (DEL-10-02 site conditions). One explicit constraint (DEC-013 no additional geotech).
- **Target Resolution:** All deliverable targets resolved against decomposition Section 9. All document targets matched to Procedure prerequisites table. DEC-013 constraint confirmed in decomposition Decision Log (Section 13).
- **Confidence Notes:** DEP-02-02-017 (DEL-10-02) rated MEDIUM because DEL-02-02 also directly reads the same reference reports; the dependency is real but partially redundant with direct document inputs.

### Warnings

_(none)_

### Quality Check Results

- Schema: All 29 required columns present. CSV parseable. PASS.
- DependencyID uniqueness: 19 unique IDs. PASS.
- EvidenceFile/SourceRef: All 19 ACTIVE rows have EvidenceFile and SourceRef populated. PASS.
- Enum normalization: All values canonical. PASS.
- Parent anchor check: Exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-02-02-001). PASS.
- FromDeliverableID consistency: All rows have FromDeliverableID=DEL-02-02. PASS.
- _DEPENDENCIES.md counts match Dependencies.csv: 19 total, 4 ANCHOR, 15 EXECUTION, 19 ACTIVE, 0 RETIRED. PASS.
- Duplicate check: No obvious duplicate extracted rows. PASS.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | (none) | 4 | 15 | 19 |
