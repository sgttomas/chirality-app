# Dependencies

**Deliverable ID:** DEL-07-05
**Deliverable Name:** Quality Management Narrative
**Package:** PKG-007 -- Construction Methodology & Administration
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 13
**Total RETIRED rows:** 0

| Class | Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 10 |

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-07-05-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0029 | HIGH |
| DEP-07-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |
| DEP-07-05-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | HIGH |

### EXECUTION Edges (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (short) |
|---|---|---|---|---|---|
| DEP-07-05-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-01 | Parent QA/QC responsibility framework and H&S obligations |
| DEP-07-05-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-03 | Discipline consultants who perform design QC and inspections |
| DEP-07-05-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-06-02 | Design QC checkpoint context and submission milestone schedule |
| DEP-07-05-007 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-08-01 | Commissioning QC handoff and integration |
| DEP-07-05-008 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-02 | Deficiency process summary; cross-reference required |
| DEP-07-05-009 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 | Inspection and testing milestone schedule integration |
| DEP-07-05-010 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 | QC framework for operational QC implementation |
| DEP-07-05-011 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.2 | Primary normative source: QA/QC and Documentation requirements |
| DEP-07-05-012 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.3 | Discipline inspection and documentation obligations |
| DEP-07-05-013 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 + Appendix J | Design-Build contract quality obligations |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located and validated)
**Source Documents (AUTO):**
- ANCHOR_DOC: `Datasheet.md`
- EXECUTION_DOCS (ordered): `Procedure.md`, `Specification.md`, `Guidance.md`
**Read-only inputs:** `_REFERENCES.md`, `_CONTEXT.md`

**Defaults applied:**
- SOURCE_DOCS=AUTO: All four deliverable documents scanned (Datasheet.md, Procedure.md, Specification.md, Guidance.md)
- DOC_ROLE_MAP=DEFAULT: Datasheet.md selected as ANCHOR_DOC (contains "datasheet" keyword); Procedure.md, Specification.md, Guidance.md as EXECUTION_DOCS
- ANCHOR_DOC=AUTO: Datasheet.md (highest-confidence match)
- EXECUTION_DOC_ORDER=AUTO: Procedure.md first (strongest prerequisite/workflow signals), Specification.md second, Guidance.md third

**Assumptions recorded:**
- None. All 13 rows are grounded in explicit source text (FACT).

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: 1 row (SOW-0029). No ambiguity.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 3 | 10 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |

---
