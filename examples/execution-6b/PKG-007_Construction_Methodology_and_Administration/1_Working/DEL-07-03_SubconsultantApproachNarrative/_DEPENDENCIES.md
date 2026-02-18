# Dependencies

**Deliverable ID:** DEL-07-03
**Deliverable Name:** Subconsultant Approach Narrative
**Package:** PKG-007 -- Construction Methodology & Administration
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated in the declared sections above. The extracted register below is machine-generated from source document analysis.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 12
**ANCHOR rows:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 8 (3 PREREQUISITE, 4 INTERFACE, 1 CONSTRAINT)
**RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-07-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0021 | ACTIVE |
| DEP-07-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-002 | ACTIVE |
| DEP-07-03-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | ACTIVE |
| DEP-07-03-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | DEC-013 | ACTIVE |
| DEP-07-03-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-09 (Appendix I) | ACTIVE |
| DEP-07-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-08 (Key Resumes) | ACTIVE |
| DEP-07-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-10-02 (Site Conditions) | ACTIVE |
| DEP-07-03-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Construction Methodology) | ACTIVE |
| DEP-07-03-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 (Construction Administration) | ACTIVE |
| DEP-07-03-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 (Structural Durability) | ACTIVE |
| DEP-07-03-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | USG1123 Geotechnical Report (Appendix D) | ACTIVE |
| DEP-07-03-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.3.4 (page 22) | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located and used)
**Source Documents Scanned:**
- ANCHOR_DOC: `Datasheet.md` (definition/traceability signal -- matched heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md`
**_REFERENCES.md:** Read; used to confirm document pointers for TargetLocation on DOCUMENT-type rows
**Defaults Applied:**
- SOURCE_DOCS=AUTO: scanned deliverable folder; identified 4 candidate source documents (Datasheet.md, Guidance.md, Procedure.md, Specification.md); excluded _DEPENDENCIES.md, _REFERENCES.md, _CONTEXT.md, _STATUS.md, _SEMANTIC.md, _SEMANTIC_LENSING.md as generated/meta files
- DOC_ROLE_MAP=DEFAULT: Datasheet.md classified as ANCHOR_DOC; Procedure.md, Specification.md, Guidance.md classified as EXECUTION_DOCS
- ANCHOR_DOC=AUTO: selected Datasheet.md (highest-confidence match)
- EXECUTION_DOC_ORDER=AUTO: Procedure.md (strongest workflow clarity), Specification.md, Guidance.md

**Extraction Notes:**
- Pass 1 (ANCHOR): Extracted 1 parent anchor (SOW-0021) and 3 trace anchors (OBJ-002, OBJ-006, DEC-013) from Datasheet.md. All identifiers confirmed present in Decomposition v2.3.
- Pass 2 (EXECUTION): Extracted 8 execution edges from Datasheet.md cross-references, Procedure.md prerequisites/cross-check table, Specification.md requirements, and Guidance.md C-004 consistency table. All deliverable targets resolved to stable IDs in Decomposition.
- No DOWNSTREAM edges extracted: source documents describe what this deliverable requires, not what depends on it. Other deliverables' dependency runs would capture reverse edges.
- DEC-013 treated as ANCHOR (TRACES_TO_REQUIREMENT) rather than EXECUTION because it is a binding scope decision/constraint from the definition layer, not an information-flow handover.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 12 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 12 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 12 |

---
