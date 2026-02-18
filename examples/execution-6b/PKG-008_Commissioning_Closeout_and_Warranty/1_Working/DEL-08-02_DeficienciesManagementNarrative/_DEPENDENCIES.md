# Dependencies

**Deliverable ID:** DEL-08-02
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

### ANCHOR Dependencies (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-08-02-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0024 | Deficiencies management per RFP Section 7.3.7 | HIGH |
| DEP-08-02-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | Maximize Project Delivery Plan score (10 pts) | HIGH |

### EXECUTION Dependencies -- UPSTREAM (8 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID/Name | Confidence |
|---|---|---|---|---|
| DEP-08-02-003 | PREREQUISITE | DELIVERABLE | DEL-08-01 (Commissioning Training Closeout Narrative) | HIGH |
| DEP-08-02-004 | INTERFACE | DELIVERABLE | DEL-08-03 (Warranty Requirements Narrative) | HIGH |
| DEP-08-02-005 | INTERFACE | DELIVERABLE | DEL-09-01 (Detailed Project Schedule) | MEDIUM |
| DEP-08-02-006 | CONSTRAINT | DOCUMENT | RFP Section 7.3.7 (p.23) | HIGH |
| DEP-08-02-007 | CONSTRAINT | DOCUMENT | Appendix J SC54-SC55 (pp.71-72) | HIGH |
| DEP-08-02-008 | CONSTRAINT | DOCUMENT | CCDC 14-2013 Standard Design-Build Contract Form | HIGH |
| DEP-08-02-009 | PREREQUISITE | EXTERNAL | Cost estimation guidelines (labour rates, overhead/profit) | HIGH |
| DEP-08-02-012 | CONSTRAINT | DOCUMENT | RFP Section 7.5 (Substantial Performance, p.24) | HIGH |
| DEP-08-02-013 | CONSTRAINT | DOCUMENT | RFP Section 7.6 (Warranty Requirements, p.25) | HIGH |

### EXECUTION Dependencies -- DOWNSTREAM (2 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetID/Name | Confidence |
|---|---|---|---|---|
| DEP-08-02-010 | HANDOVER | DELIVERABLE | DEL-08-03 (Warranty Requirements Narrative) | HIGH |
| DEP-08-02-011 | HANDOVER | DELIVERABLE | DEL-08-01 (Commissioning Training Closeout Narrative) | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL)
**Decomposition Status:** Located and validated. DEL-08-02 confirmed in Section 9 (PKG-008); SOW-0024 confirmed in Section 7 (Scope Ledger); OBJ-002 confirmed in Section 6 (Objectives).

**Source Documents Scanned (AUTO):**
- ANCHOR_DOC: Datasheet.md (definition/traceability signals)
- EXECUTION_DOCS (in order): Procedure.md, Specification.md, Guidance.md

**Read-Only Inputs:**
- _REFERENCES.md (used for cross-reference resolution)
- _CONTEXT.md (used for deliverable identity confirmation)

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- scanned all .md files in deliverable folder excluding dependency artifacts and generated files (_SEMANTIC.md, _SEMANTIC_LENSING.md, _STATUS.md)
- DOC_ROLE_MAP: DEFAULT -- Datasheet.md matched ANCHOR_DOC heuristic; Procedure.md, Specification.md, Guidance.md matched EXECUTION_DOC heuristic
- ANCHOR_DOC: AUTO -- selected Datasheet.md (highest confidence match for definition/traceability)
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md first (clearest workflow/prerequisite signals), then Specification.md, then Guidance.md

**Warnings:** None.

**Integrity Checks:**
- Parent anchor check: 1 ACTIVE row with DependencyClass=ANCHOR, AnchorType=IMPLEMENTS_NODE (SOW-0024). PASS.
- Schema check: All 29 required columns present. PASS.
- DependencyID uniqueness: 13 unique IDs. PASS.
- Evidence check: All ACTIVE rows have EvidenceFile and SourceRef populated. PASS.
- Enum normalization: All values canonical. PASS.
- FromDeliverableID consistency: All rows = DEL-08-02. PASS.
- Target ID placement: Non-deliverable targets use TargetRefID/TargetName (TargetDeliverableID empty). Deliverable targets use TargetDeliverableID. PASS.

**Extraction Notes:**
- DEL-08-01 appears as both UPSTREAM PREREQUISITE (DEP-08-02-003) and DOWNSTREAM HANDOVER (DEP-08-02-011). This is correct: DEL-08-02 requires DEL-08-01's commissioning completion as an activation precondition (upstream), and DEL-08-02 produces the commissioning-to-deficiency handoff criteria that DEL-08-01 must reference (downstream). Bidirectional interface.
- DEL-08-03 appears as both UPSTREAM INTERFACE (DEP-08-02-004) and DOWNSTREAM HANDOVER (DEP-08-02-010). This is correct: DEL-08-02 requires cross-reference with DEL-08-03 for SC54-SC55 consistency (upstream), and DEL-08-02 produces the deficiency-to-warranty transition framework consumed by DEL-08-03 (downstream). Bidirectional interface.
- Cost estimation guidelines (DEP-08-02-009) are an EXTERNAL prerequisite from the Estimator role, not a deliverable. Recorded as TargetType=EXTERNAL.
- RFP Sections 7.3.7, 7.5, 7.6 and Appendix J SC54-SC55 and CCDC 14-2013 are DOCUMENT constraints. These are explicit required inputs per Procedure prerequisites.
- DEL-09-01 interface (DEP-08-02-005) is MEDIUM confidence because Procedure V-007 provides a fallback if the schedule is not yet available.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 13 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |

| DependencyClass | ACTIVE Count |
|---|---|
| ANCHOR | 2 |
| EXECUTION | 11 |

| Direction | ACTIVE Count |
|---|---|
| UPSTREAM | 11 |
| DOWNSTREAM | 2 |
