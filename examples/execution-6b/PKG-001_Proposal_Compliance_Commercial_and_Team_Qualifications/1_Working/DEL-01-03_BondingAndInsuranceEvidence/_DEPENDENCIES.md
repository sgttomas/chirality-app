# Dependencies

**Deliverable ID:** DEL-01-03
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13
**Total RETIRED rows:** 0

| Class | Count |
|-------|-------|
| ANCHOR | 4 |
| EXECUTION | 9 |

| Direction | Count |
|-----------|-------|
| UPSTREAM | 8 |
| DOWNSTREAM | 5 |

### ANCHOR Edges (Pass 1)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-01-03-001 | IMPLEMENTS_NODE | SOW-0004 | Agreement to Bond + bond inclusion | HIGH |
| DEP-01-03-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Pass all mandatory requirements | HIGH |
| DEP-01-03-003 | TRACES_TO_REQUIREMENT | OBJ-007 | Competitive compliant price package | HIGH |
| DEP-01-03-004 | TRACES_TO_REQUIREMENT | C-08 | Agreement to Bond (50%+50%) | HIGH |

### EXECUTION Edges (Pass 2)

| DependencyID | Direction | Type | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-01-03-005 | UPSTREAM | PREREQUISITE | DEL-01-04 | Schedule A Pricing Summary | HIGH |
| DEP-01-03-006 | UPSTREAM | PREREQUISITE | DEL-01-05 | Schedule B Cost Breakdown | HIGH |
| DEP-01-03-007 | DOWNSTREAM | HANDOVER | DEL-01-05 | Schedule B Cost Breakdown | HIGH |
| DEP-01-03-008 | DOWNSTREAM | HANDOVER | DEL-01-06 | Pricing Narrative and Assumptions | HIGH |
| DEP-01-03-009 | DOWNSTREAM | HANDOVER | DEL-01-01 | Compliance Matrix and Checklist | HIGH |
| DEP-01-03-010 | DOWNSTREAM | HANDOVER | DEL-01-04 | Schedule A Pricing Summary | HIGH |
| DEP-01-03-011 | DOWNSTREAM | HANDOVER | DEL-01-02 | Formal Submission Package | HIGH |
| DEP-01-03-012 | UPSTREAM | CONSTRAINT | -- | RFP Section 5.3.1 (Document) | HIGH |
| DEP-01-03-013 | UPSTREAM | CONSTRAINT | -- | Appendix J SC 50-52 (Document) | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; found 4 source documents: Datasheet.md, Specification.md, Guidance.md, Procedure.md
- DOC_ROLE_MAP: DEFAULT heuristic applied
- ANCHOR_DOC: Datasheet.md (contains identification table with SOW/OBJ/Constraint references)
- EXECUTION_DOC_ORDER: Procedure.md (primary workflow), Guidance.md (principles/considerations), Specification.md (requirements/verification)
- _REFERENCES.md: read; used to confirm cross-reference targets (DEL-01-04, DEL-01-05, DEL-01-06)

**Decomposition Status:** Available and validated. v2.3 FINAL. All anchor targets (SOW-0004, OBJ-001, OBJ-007, C-08) confirmed present in decomposition.

**Warnings:** None.

**Assumptions:**
- None. All extracted rows are based on explicit statements in source documents.

**Observations:**
- DEL-01-04 (Schedule A) has a bidirectional relationship: UPSTREAM as a prerequisite (provides base price for bond calculation per Procedure PR-001) and DOWNSTREAM as a handover (receives updated total incorporating bond/insurance costs per Procedure Step 3 Action 3). Both directions are recorded as separate rows (DEP-01-03-005 and DEP-01-03-010).
- Appendix J SC 50-52 is referenced extensively but full clause text was not accessed during source document preparation (noted in Procedure N-002 and Datasheet Open Items). Confidence set to MEDIUM for DEP-01-03-013.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available, validated) | None | 13 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |

---

*End of Dependencies*
