# Dependencies: DEL-05-01 AppendixH ScheduleA PricingSummary

## Dependency Tracking Mode
- **Mode:** TRACKED (overwritten from NOT_TRACKED by DEPENDENCIES agent run 2026-02-18)
- **Notes:** This file is now maintained by the DEPENDENCIES agent (Type 2). Declared sections below are preserved as human-owned; extracted register sections are agent-maintained.

---

## Upstream (I need these before I can proceed)

| Deliverable / Artifact | What I need | Status |
|------------------------|-------------|--------|
| DEL-05-02 AppendixH ScheduleB CostBreakdown | Schedule B totals (Subtotal Base Requirements + Additional Item subtotals 1–6) to populate and reconcile Schedule A pricing lines | TBD |
| DEL-01-03 BondingAndInsuranceEvidence | Bond cost data to confirm inclusion of 50% Performance + 50% Labour/Material Payment bond costs in base contract price | TBD |
| DEL-01-01 ComplianceMatrixAndChecklist | Addenda log confirming all addenda received; required for addenda acknowledgment section | TBD |
| RFP Appendix H Schedule A template (page 57) | Mandatory form template (must be used exactly as provided per R-01.1) | TBD |
| Addendum 03 | Critical pricing impacts: pickled sand building removed; new technical requirements; service tie-in allowance; 12-acre site clarification | TBD |

---

## Downstream (These need me)

| Deliverable | What they need from me | Status |
|-------------|------------------------|--------|
| DEL-05-02 AppendixH ScheduleB CostBreakdown | Schedule A totals for reconciliation verification (acceptance criterion: A totals = B totals) | TBD |
| DEL-05-03 PricingNarrativeAndAssumptions | Schedule A values for consistency check; narrative must align with and explain Schedule A pricing | TBD |
| DEL-01-02 FormalSubmissionPackage | Completed Schedule A PDF for inclusion in final proposal submission PDF | TBD |

---

## Extracted Dependency Register

**Run date:** 2026-02-18
**Total rows:** 11
**ACTIVE rows:** 11
**RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetRefID / TargetDeliverableID | TargetName | Confidence | SatisfactionStatus |
|---|---|---|---|---|---|---|---|---|---|
| DEP-05-01-A-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-02 | PKG-02 Financial Proposal (Appendix H) | HIGH | TBD |
| DEP-05-01-A-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-005 | SOW-005: Complete Appendix H Schedule A pricing summary | HIGH | TBD |
| DEP-05-01-A-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-007 | OBJ-007: Produce a competitive compliant price package | HIGH | TBD |
| DEP-05-01-E-001 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-02 | DEL-05-02 AppendixH ScheduleB CostBreakdown | HIGH | TBD |
| DEP-05-01-E-002 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-03 | DEL-01-03 BondingAndInsuranceEvidence | HIGH | TBD |
| DEP-05-01-E-003 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-02 | DEL-05-02 AppendixH ScheduleB CostBreakdown | HIGH | TBD |
| DEP-05-01-E-004 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-03 | DEL-05-03 PricingNarrativeAndAssumptions | MEDIUM | TBD |
| DEP-05-01-E-005 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | DEL-01-02 FormalSubmissionPackage | HIGH | TBD |
| DEP-05-01-E-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 | DEL-01-01 ComplianceMatrixAndChecklist | MEDIUM | TBD |
| DEP-05-01-E-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP-APP-H | RFP Appendix H Schedule A template | HIGH | TBD |
| DEP-05-01-E-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | ADDENDUM-03 | Addendum 03 (scope clarifications and pricing impacts) | HIGH | TBD |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 11 |
| RETIRED | 0 |
| **Total** | **11** |

**Closure state breakdown (ACTIVE rows):**

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 11 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

**By DependencyClass:**

| Class | ACTIVE |
|-------|--------|
| ANCHOR | 3 |
| EXECUTION | 8 |

**Parent anchor (IMPLEMENTS_NODE) count:** 1 — integrity check PASSED.

---

## Run Notes

**Run parameters:**
- SCOPE: DEL-05-01 AppendixH ScheduleA PricingSummary
- DELIVERABLE_PATH: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary`
- EXECUTION_ROOT: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c`
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE

**Source documents scanned (AUTO):**
- Datasheet.md (ANCHOR_DOC — selected per DOC_ROLE_MAP heuristic; filename contains "datasheet")
- Specification.md (EXECUTION_DOC — primary; filename contains "spec")
- Guidance.md (EXECUTION_DOC)
- Procedure.md (EXECUTION_DOC — primary; filename contains "procedure")
- _CONTEXT.md (read for deliverable identity and scope traceability)
- _REFERENCES.md (read for document pointer resolution)
- _SEMANTIC.md (read; semantic matrices only — no dependency signals)

**Decomposition file used:** `Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- Decomposition status: LOCATED and READ. Anchor validation performed successfully.
- DEL-05-01 confirmed in decomposition Section 8.
- PKG-02 confirmed in decomposition Section 7.
- SOW-005 confirmed in Scope Ledger (Section 10), mapped to DEL-05-01 and OBJ-007.
- OBJ-007 confirmed in decomposition Section 6.

**_REFERENCES.md used:** Yes — used to resolve document pointer paths for TargetType=DOCUMENT rows (DEP-05-01-E-007, DEP-05-01-E-008). Sources directory: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Sources/`.

**Pass 1 (ANCHOR) notes:**
- Parent anchor identified: PKG-02 (WBS_NODE) via IMPLEMENTS_NODE. Confidence: HIGH (confirmed in decomposition).
- Trace anchors identified: SOW-005 and OBJ-007. Both confirmed in decomposition Scope Ledger and Objectives sections.
- STRICTNESS=CONSERVATIVE applied: only explicitly stated identifiers from _CONTEXT.md Scope Traceability section used.

**Pass 2 (EXECUTION) notes:**
- Primary execution signals found in: Specification.md (Interfaces table, Requirements), Procedure.md (Prerequisites, Steps 2, 10, 11), Guidance.md (Notes section), Datasheet.md (Addenda Integration, References).
- DEL-05-02 appears as both UPSTREAM PREREQUISITE (Schedule B must be complete before Schedule A can be populated) and DOWNSTREAM HANDOVER (Schedule A outputs consumed by Schedule B reconciliation). Both edges retained as they represent distinct information flows.
- DEL-01-01 interface: Guidance.md Notes provides explicit operational reference; Specification.md Interfaces table marks it ASSUMPTION; conservative approach retained the row given Guidance operational reference (MEDIUM confidence assigned).
- DEL-05-03 downstream handover: Procedure Step 11 provides explicit operational reference; source-level ASSUMPTION annotation in Specification does not negate the Procedure evidence (MEDIUM confidence assigned reflecting the dual sourcing).
- RFP template (DEP-05-01-E-007) and Addendum 03 (DEP-05-01-E-008) retained as DOCUMENT PREREQUISITE rows because source documents explicitly state these artifacts are required inputs before DEL-05-01 can be produced — not merely references.
- No COORDINATION-only or structural adjacency edges created.

**Quality checks performed:**
- Required CSV columns: PRESENT (all 28 required columns populated).
- DependencyID uniqueness: VERIFIED (11 distinct IDs).
- ACTIVE rows with EvidenceFile + SourceRef: VERIFIED (all 11 rows).
- Status enum values: CANONICAL (ACTIVE).
- SatisfactionStatus enum values: CANONICAL (TBD).
- Parent anchor count (ACTIVE ANCHOR IMPLEMENTS_NODE): 1 — PASSED.
- _DEPENDENCIES.md counts consistent with Dependencies.csv: VERIFIED.
- No duplicate extracted rows detected.

**Warnings:** None.

---

## Run History

| Run # | Timestamp | Mode | Strictness | Decomposition Status | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|-------|-----------|------|------------|----------------------|----------|---------------|-----------------|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | LOCATED (Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md) | None | 3 | 8 |
