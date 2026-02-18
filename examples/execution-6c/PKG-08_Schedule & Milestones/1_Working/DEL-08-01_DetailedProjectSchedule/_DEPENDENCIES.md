# Dependencies: DEL-08-01 DetailedProjectSchedule

## Dependency Tracking Mode
- **Mode:** NOT_TRACKED (source document declaration; see original `_DEPENDENCIES.md`)
- **Notes:** Source document declares "NOT_TRACKED — dependencies coordinated externally by humans." This agent run extracts explicit evidence-backed dependency edges from source documents into the canonical register below. Declared lists preserved as-is; extracted register added per AGENT_DEPENDENCIES protocol.

---

## Upstream (I need these before I can proceed)

_Declared by source document:_
- Dependencies coordinated externally by humans.

_Extracted upstream dependencies (see Extracted Dependency Register below):_
- DEL-02-01 ConceptDesignPackage (PREREQUISITE — scope clarity for phasing/durations)
- DEL-04-01 ConstructionMethodologyNarrative (PREREQUISITE — construction sequencing alignment)
- DEL-05-01 AppendixH_ScheduleA_PricingSummary (INTERFACE — cost basis/escalation alignment)
- DEL-05-02 AppendixH_ScheduleB_CostBreakdown (INTERFACE — procurement cost alignment)
- DEL-06-01 CommissioningTrainingCloseoutWarrantyNarrative (INTERFACE — commissioning duration/scope alignment)
- DEL-09-01 RiskRegisterAndMitigationPlan (INTERFACE — schedule buffers/contingencies)
- DEL-09-02 SiteConditionsAndDueDiligenceSummary (PREREQUISITE — site constraints for phasing)

---

## Downstream (These need me)

_Declared by source document:_
- Dependencies coordinated externally by humans.

_Extracted downstream dependencies (see Extracted Dependency Register below):_
- DEL-01-02 FormalSubmissionPackage (HANDOVER — schedule artifacts integrated into proposal PDF)

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**ANCHOR rows (ACTIVE):** 3
**EXECUTION rows (ACTIVE):** 8
**RETIRED rows:** 0

| DependencyID | DependencyClass | AnchorType | Direction | DependencyType | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | SatisfactionStatus | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| DEP-08-01-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-08 | PKG-08 Schedule & Milestones | HIGH | TBD | ACTIVE |
| DEP-08-01-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-023 | SOW-023 Detailed project schedule | HIGH | TBD | ACTIVE |
| DEP-08-01-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-009 | OBJ-009 Provide a believable schedule | HIGH | TBD | ACTIVE |
| DEP-08-01-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 | DEL-02-01 ConceptDesignPackage | HIGH | PENDING | ACTIVE |
| DEP-08-01-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01 | DEL-04-01 ConstructionMethodologyNarrative | HIGH | PENDING | ACTIVE |
| DEP-08-01-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 | DEL-05-01 AppendixH_ScheduleA_PricingSummary | HIGH | PENDING | ACTIVE |
| DEP-08-01-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 | DEL-05-02 AppendixH_ScheduleB_CostBreakdown | HIGH | PENDING | ACTIVE |
| DEP-08-01-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 | DEL-06-01 CommissioningTrainingCloseoutWarrantyNarrative | HIGH | PENDING | ACTIVE |
| DEP-08-01-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 | DEL-09-01 RiskRegisterAndMitigationPlan | HIGH | PENDING | ACTIVE |
| DEP-08-01-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-02 | DEL-09-02 SiteConditionsAndDueDiligenceSummary | MEDIUM | PENDING | ACTIVE |
| DEP-08-01-011 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | DEL-01-02 FormalSubmissionPackage | HIGH | PENDING | ACTIVE |

---

## Run Notes

### Run Parameters
- **Mode:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (all .md files in deliverable folder, excluding dependency artifacts)
- **ANCHOR_DOC:** Datasheet.md (highest-confidence anchor candidate; contains Identification, Attributes with explicit WBS/scope/objective references)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (Procedure contains explicit prerequisite list; Specification contains Boundaries and Interfaces; Guidance provides supporting context)
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- **Decomposition status:** LOCATED AND READ — anchor validation performed; labels resolved from Section 6, 7, 8, 9, 10.
- **Run date:** 2026-02-18

### Defaults Applied
- `DOC_ROLE_MAP`: DEFAULT heuristic applied.
- `TargetLocation` for DELIVERABLE rows: constructed from decomposition package structure; paths are best-effort approximations relative to execution root.

### Anchor Validation Notes
- **PKG-08** confirmed in decomposition Section 7 as parent package of DEL-08-01. Label "Schedule & Milestones" confirmed.
- **SOW-023** confirmed in decomposition Section 9 and Section 10 Scope Ledger. Statement: "Provide detailed project schedule (Gantt + milestones + critical path) and schedule assumptions." Mapped to PKG-08 / DEL-08-01 / OBJ-009.
- **OBJ-009** confirmed in decomposition Section 6. Statement: "Provide a believable schedule (Gantt/milestones/critical path; key risks accounted for)."
- **Parent anchor count (IMPLEMENTS_NODE):** 1 — no FLOATING_NODE or AMBIGUOUS_ANCHOR warning required.

### Exclusions (not extracted)
- RFP Section 7.1.9 references: mentioned throughout as "location TBD / PDF not accessible" — no stable TargetRefID can be assigned. Would be TargetType=DOCUMENT if accessible; not extracted under CONSERVATIVE strictness without confirmed pointer.
- Addenda 01/02/03: referenced as constraints on schedule content, but the dependency is on the decomposition-integrated content (already captured via SOW-023 and Datasheet conditions). Not extracted as separate rows to avoid duplication.
- DEL-05-03 (Pricing Narrative): Specification REQ-SCH-010 mentions "pricing basis in DEL-05-01/02 (Appendix H)" as the interface target; DEL-05-03 is cited in Specification verification row as a cross-check partner but the primary interface stated in Boundaries is DEL-05-01/02. DEL-05-03 not extracted separately to avoid low-signal duplication; DEL-05-01 and DEL-05-02 capture the interface.
- DEL-03-01 (Design Methodology): Guidance mentions it as context for the schedule ("temporal backbone that connects design methodology...") but does not explicitly state an information/artifact transfer. Not extracted under CONSERVATIVE strictness.
- PMI PMBOK, CSI MasterFormat, Alberta Building Code: referenced as applicable standards (all ASSUMPTION-labeled); no explicit interface stated. Not extracted.

### Warnings
- None.

---

## Lifecycle Summary

| Lifecycle Status | Count |
|---|---|
| ACTIVE rows | 11 |
| RETIRED rows | 0 |
| **Total rows** | **11** |

| SatisfactionStatus | ANCHOR rows | EXECUTION rows | Total |
|---|---|---|---|
| TBD | 3 | 0 | 3 |
| PENDING | 0 | 8 | 8 |
| IN_PROGRESS | 0 | 0 | 0 |
| SATISFIED | 0 | 0 | 0 |
| WAIVED | 0 | 0 | 0 |
| NOT_APPLICABLE | 0 | 0 | 0 |

**Parent anchor check:** 1 ACTIVE IMPLEMENTS_NODE row found. No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.

---

## Run History

| Run # | Date | Mode | Strictness | Decomposition Status | Warnings | ACTIVE Count | Notes |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | LOCATED | None | 11 | Initial extraction run. Source docs: Datasheet.md, Specification.md, Guidance.md, Procedure.md, _CONTEXT.md, _REFERENCES.md, _SEMANTIC.md. Decomposition: Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md. |
