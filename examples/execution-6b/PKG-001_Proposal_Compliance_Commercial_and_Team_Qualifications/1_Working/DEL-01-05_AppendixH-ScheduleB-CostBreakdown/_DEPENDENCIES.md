# Dependencies

**Deliverable ID:** DEL-01-05
**Deliverable Name:** Appendix H - Schedule B - Cost Breakdown
**Package:** PKG-001 -- Proposal Compliance, Commercial & Team Qualifications
**Tracking Mode:** DECLARED + EXTRACTED

---

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated in the declared sections above. Extracted dependencies are maintained in the register below and in `Dependencies.csv`.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 19
**ANCHOR rows:** 7 (1 IMPLEMENTS_NODE, 6 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 12 (5 PREREQUISITE, 4 INTERFACE, 2 HANDOVER, 1 CONSTRAINT)

### ANCHOR Dependencies (Pass 1 -- Tree Linkage)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-01-05-A001 | IMPLEMENTS_NODE | SOW-0006 | Schedule B complete breakdown | HIGH | Parent scope item |
| DEP-01-05-A002 | TRACES_TO_REQUIREMENT | OBJ-007 | Produce a competitive compliant price package (35 pts) | HIGH | Primary objective |
| DEP-01-05-A003 | TRACES_TO_REQUIREMENT | C-05 | Must use Appendix H pricing template | HIGH | Hard constraint |
| DEP-01-05-A004 | TRACES_TO_REQUIREMENT | C-07 | Addenda acknowledgement required | HIGH | Hard constraint |
| DEP-01-05-A005 | TRACES_TO_REQUIREMENT | C-11 | FF&E not in base cost | HIGH | Hard constraint |
| DEP-01-05-A006 | TRACES_TO_REQUIREMENT | DEC-011 | CCIP insurance confirmed | HIGH | Decision trace |
| DEP-01-05-A007 | TRACES_TO_REQUIREMENT | DEC-012 | FF&E $20K cash allowance | HIGH | Decision trace |

### EXECUTION Dependencies (Pass 2 -- DAG / Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-01-05-E001 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-04 (Schedule A) | HIGH | BLOCKING: must be completed first |
| DEP-01-05-E002 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-03 (Bonding/Insurance) | HIGH | Cost basis for GR bonding/CCIP lines |
| DEP-01-05-E003 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-06 (Pricing Narrative) | HIGH | Consumes Schedule B data for assumptions/reconciliation |
| DEP-01-05-E004 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission) | HIGH | Schedule B assembled into Appendix H for proposal PDF |
| DEP-01-05-E005 | UPSTREAM | PREREQUISITE | DOCUMENT | Appendix H Template | HIGH | Defines required form structure |
| DEP-01-05-E006 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 8 | HIGH | Governs pricing format/tax treatment |
| DEP-01-05-E007 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Functional Program (Appendix B) | HIGH | Baseline scope for building cost estimation |
| DEP-01-05-E008 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 | HIGH | Cost impacts integration required |
| DEP-01-05-E009 | UPSTREAM | INTERFACE | DOCUMENT | Site Reference Reports (Appendix D E F) | MEDIUM | Geotech/grading/site basis per DEC-013 |
| DEP-01-05-E010 | UPSTREAM | INTERFACE | PACKAGE | PKG-002 Conceptual Design | MEDIUM | Design assumptions input (conditional) |
| DEP-01-05-E011 | UPSTREAM | INTERFACE | DOCUMENT | CCDC 14-2013 + Appendix J | MEDIUM | Bonding/insurance structure reference |
| DEP-01-05-E012 | UPSTREAM | CONSTRAINT | REQUIREMENT | C-01 (Single PDF under 15 MB) | HIGH | Submission format constraint |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 19 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 19 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

- **DECOMPOSITION_PATH:** `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, 2026-02-17)
- **SOURCE_DOCS (AUTO):** Datasheet.md, Specification.md, Guidance.md, Procedure.md
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
  - ANCHOR_DOC: Datasheet.md (contains identification, scope coverage, objective alignment, attributes)
  - EXECUTION_DOCS: Procedure.md (primary -- prerequisites, steps, verification), Specification.md (requirements, verification), Guidance.md (principles, considerations)
- **_REFERENCES.md:** Read; used for cross-reference resolution (DEL-01-04, DEL-01-06, DEL-01-03)
- **_CONTEXT.md:** Read; confirmed deliverable identity and scope coverage

### Decomposition Validation

- Decomposition located and loaded successfully (v2.3 FINAL)
- DEL-01-05 found in Decomposition §9 under PKG-001
- SOW-0006 confirmed IN scope, mapped to DEL-01-05 in Scope Ledger (§10)
- OBJ-007 confirmed as supported objective
- All target deliverable IDs (DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-06) validated as existing in decomposition

### Extraction Notes

- **Pass 1 (ANCHOR):** 7 rows extracted. 1 parent anchor (SOW-0006) and 6 trace anchors (OBJ-007, C-05, C-07, C-11, DEC-011, DEC-012). All explicitly stated in Datasheet and Specification. Conservative mode: no implicit anchors emitted.
- **Pass 2 (EXECUTION):** 12 rows extracted. Key finding: DEL-01-04 is an explicit blocking prerequisite per Procedure text ("MUST BE COMPLETED FIRST"). DEL-01-03 provides interface data (bonding/CCIP cost basis). DEL-01-06 and DEL-01-02 are downstream consumers. Four document-type prerequisites identified from Procedure Prerequisites section. PKG-002 is a conditional upstream interface (design assumptions may or may not be available).
- **Constraint C-12 (site servicing cash allowance):** Considered but not extracted as a separate anchor row because it is a pricing treatment instruction already covered by Addendum 03 document dependency (E008) and does not add independent traceability value at CONSERVATIVE strictness.
- **Constraint C-10 (Pickled Sand Storage excluded):** Similarly covered by Addendum 03 dependency. Not extracted as separate row.
- **DEC-013 (no additional geotech):** Referenced in E009 notes rather than as separate anchor row, since its primary impact is on the site reference reports interpretation, not a direct trace to a DEL-01-05 requirement.

### Warnings

_No warnings. Parent anchor found (1 IMPLEMENTS_NODE). No ambiguous anchors._

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (loaded) | None | 19 |
