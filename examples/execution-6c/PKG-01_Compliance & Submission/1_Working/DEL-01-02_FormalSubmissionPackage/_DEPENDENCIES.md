# Dependencies: DEL-01-02 FormalSubmissionPackage

## Upstream (I need these before I can proceed)

The following are explicitly stated prerequisites in source documents. All upstream proposal content deliverables must reach Final maturity before the formal submission package can be assembled.

### Compliance and Formal Execution (PKG-01)
- **DEL-01-01** — Compliance Matrix and Checklist (Final): Required for content completeness cross-check during assembly (Procedure Step 6; Specification R-08)
- **DEL-01-03** — Bonding and Insurance Evidence (Final, executed): Mandatory insertion item in the final PDF (Procedure Prerequisites)

### Design Proposal (PKG-04)
- **DEL-02-01** — Concept Design Package (Final)
- **DEL-02-02** — Design Brief Narrative (Final)
- **DEL-02-03** — Sustainability and Energy Narrative (Final)

### Delivery Plan (PKG-05)
- **DEL-03-01** — Design Methodology Narrative (Final)
- **DEL-03-02** — Detailed Design and Construction Docs Plan (Final)

### Construction Methodology (PKG-06)
- **DEL-04-01** — Construction Methodology Narrative (Final)
- **DEL-04-02** — Budget Control and Change Management Plan (Final)
- **DEL-04-03** — Communications and Reporting Plan (Final)

### Financial Proposal (PKG-02)
- **DEL-05-01** — Appendix H Schedule A — Pricing Summary (Final, executed; includes addenda acknowledgement required by Constraint C-07)
- **DEL-05-02** — Appendix H Schedule B — Cost Breakdown (Final)
- **DEL-05-03** — Pricing Narrative and Assumptions (Final)

### Commissioning and Closeout (PKG-07)
- **DEL-06-01** — Commissioning/Training/Closeout/Warranty Narrative (Final)

### Team Qualifications (PKG-03)
- **DEL-07-01** — Design-Build Firm Experience Profile (Final)
- **DEL-07-02** — Key Team Members and Resumes (Final)
- **DEL-07-03** — Appendix I — Subtrade and Consultant List (Final)

### Schedule (PKG-08)
- **DEL-08-01** — Detailed Project Schedule (Final)

### Due Diligence and Risk (PKG-09)
- **DEL-09-01** — Risk Register and Mitigation Plan (Final)
- **DEL-09-02** — Site Conditions and Due Diligence Summary (Final)

### External Documents and Constraints
- **RFP 2024_004** — AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf (Sections 4.2–4.3, 5.2, 6–9): Normative governance of submission format, structure, and execution requirements
- **Addendum 01** — Must be acknowledged in submission package (Appendix H)
- **Addendum 02** — Must be acknowledged in submission package (Appendix H)
- **Addendum 03** — Must be acknowledged in submission package (Appendix H); contains scope changes affecting final assembly
- **Hard Deadline** — Aug 30, 2024 @ 2:00 PM MST (Town of Penhold); missed deadline = automatic disqualification

## Downstream (These need me)

- **Town of Penhold Procurement** — The completed formal submission package (final PDF + submission email) is the terminal output delivered to Town Procurement as the proposal response.

---

## Extracted Dependency Register

**Run date:** 2026-02-18
**Total ACTIVE rows:** 30
**RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | DependencyType | TargetType | TargetName | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-01-02-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-01 — Compliance & Submission | HIGH | ACTIVE |
| DEP-01-02-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-001 — Assemble compliant PDF & submit by email | HIGH | ACTIVE |
| DEP-01-02-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-002 — Letter of Offer + execution requirements | HIGH | ACTIVE |
| DEP-01-02-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 — Pass all mandatory requirements | HIGH | ACTIVE |
| DEP-01-02-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01_ComplianceMatrixAndChecklist | HIGH | ACTIVE |
| DEP-01-02-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-03_BondingAndInsuranceEvidence | HIGH | ACTIVE |
| DEP-01-02-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01_ConceptDesignPackage | HIGH | ACTIVE |
| DEP-01-02-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02_DesignBriefNarrative | HIGH | ACTIVE |
| DEP-01-02-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03_SustainabilityAndEnergyNarrative | HIGH | ACTIVE |
| DEP-01-02-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01_DesignMethodologyNarrative | HIGH | ACTIVE |
| DEP-01-02-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02_DetailedDesignAndConstructionDocsPlan | HIGH | ACTIVE |
| DEP-01-02-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-01_ConstructionMethodologyNarrative | HIGH | ACTIVE |
| DEP-01-02-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-02_BudgetControlAndChangeManagementPlan | HIGH | ACTIVE |
| DEP-01-02-014 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-03_CommunicationsAndReportingPlan | HIGH | ACTIVE |
| DEP-01-02-015 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-01_AppendixH_ScheduleA_PricingSummary | HIGH | ACTIVE |
| DEP-01-02-016 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-02_AppendixH_ScheduleB_CostBreakdown | HIGH | ACTIVE |
| DEP-01-02-017 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-05-03_PricingNarrativeAndAssumptions | HIGH | ACTIVE |
| DEP-01-02-018 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-06-01_CommissioningTrainingCloseoutWarrantyNarrative | HIGH | ACTIVE |
| DEP-01-02-019 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-01_DesignBuildFirmExperienceProfile | HIGH | ACTIVE |
| DEP-01-02-020 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-02_KeyTeamMembersAndResumes | HIGH | ACTIVE |
| DEP-01-02-021 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-03_AppendixI_SubtradeAndConsultantList | HIGH | ACTIVE |
| DEP-01-02-022 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-01_DetailedProjectSchedule | HIGH | ACTIVE |
| DEP-01-02-023 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-01_RiskRegisterAndMitigationPlan | HIGH | ACTIVE |
| DEP-01-02-024 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-02_SiteConditionsAndDueDiligenceSummary | HIGH | ACTIVE |
| DEP-01-02-025 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DOCUMENT | RFP 2024_004 | HIGH | ACTIVE |
| DEP-01-02-026 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DOCUMENT | Addendum 01 | HIGH | ACTIVE |
| DEP-01-02-027 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DOCUMENT | Addendum 02 | HIGH | ACTIVE |
| DEP-01-02-028 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DOCUMENT | Addendum 03 | HIGH | ACTIVE |
| DEP-01-02-029 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | EXTERNAL | Town of Penhold Submission Deadline | HIGH | ACTIVE |
| DEP-01-02-030 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | EXTERNAL | Town of Penhold Procurement — Formal Proposal Submission | HIGH | ACTIVE |

**Breakdown by class:**
- ANCHOR: 4 rows (1 IMPLEMENTS_NODE + 3 TRACES_TO_REQUIREMENT)
- EXECUTION: 26 rows (20 PREREQUISITE DELIVERABLE + 3 INTERFACE DOCUMENT + 1 CONSTRAINT EXTERNAL + 1 HANDOVER EXTERNAL + 1 CONSTRAINT EXTERNAL)

**Breakdown by direction:**
- UPSTREAM: 29 rows
- DOWNSTREAM: 1 row

---

## Run Notes

**Run date:** 2026-02-18
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

**Source documents scanned:**
- `Datasheet.md` — ANCHOR_DOC (selected as highest-confidence anchor source per DEFAULT heuristic; filename contains `datasheet`)
- `Specification.md` — EXECUTION_DOC (contains `spec`)
- `Guidance.md` — EXECUTION_DOC
- `Procedure.md` — EXECUTION_DOC (primary execution signal; filename contains `procedure`)
- `_CONTEXT.md` — read-only supplementary input
- `_REFERENCES.md` — read-only reference input
- `_SEMANTIC.md` — read-only supplementary input (matrices only; no dependency signals extracted)

**Decomposition path used:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- Status: Located and read successfully.
- Decomposition confirmed DEL-01-02 definition (§8), PKG-01 membership (§7), SOW-001/SOW-002 mapping (§10), and OBJ-001 (§6).

**_REFERENCES.md used:** Yes — resolved document pointers for RFP, Addendum 01/02/03 to local paths under `_Sources/`.

**Prior state of _DEPENDENCIES.md:** Placeholder only (NOT_TRACKED mode, no declared rows). No declared rows to preserve.

**Prior Dependencies.csv:** Did not exist; created fresh.

**Pass 1 (ANCHOR) notes:**
- Parent anchor (IMPLEMENTS_NODE): PKG-01 — confirmed in decomposition §7 and _CONTEXT.md. Single parent anchor found. No FLOATING_NODE or AMBIGUOUS_ANCHOR condition.
- Requirement trace anchors: SOW-001, SOW-002 (from _CONTEXT.md Scope Traceability, confirmed in Decomposition Scope Ledger §10), and OBJ-001 (from _CONTEXT.md, confirmed in Decomposition §6).

**Pass 2 (EXECUTION) notes:**
- Prerequisite deliverables: 20 rows extracted from the explicit prerequisite table in Procedure.md § Prerequisites / Dependencies. All deliverable IDs resolved against decomposition §8 with HIGH confidence.
- Document interface dependencies: RFP and three addenda extracted from _REFERENCES.md (required as normative inputs per Procedure § Reference Materials and Specification requirements R-01 through R-07).
- Constraint dependency: Hard submission deadline extracted from Specification R-04 and Decomposition §1 (Aug 30, 2024 @ 2:00 PM MST). Classified as EXTERNAL CONSTRAINT because it is a hard gate imposed by the procuring authority.
- Downstream handover: Town of Penhold Procurement classified as EXTERNAL HANDOVER — the final submitted PDF is the terminal output of this deliverable (Procedure Step 11).
- NOT extracted: General coordination language ("dependencies coordinated externally by humans") was present in the original _DEPENDENCIES.md — this is NOT an information-flow dependency and was deliberately excluded per model rules.
- NOT extracted: The Procedure's Guidance Context references (Guidance.md principles) were not extracted as separate dependencies — they are internal document cross-references, not external information-flow edges.

**Quality checks passed:**
- Schema: All required columns present; RegisterSchemaVersion = v3.1 on all rows.
- DependencyID uniqueness: DEP-01-02-001 through DEP-01-02-030 — all unique.
- ACTIVE rows with evidence: All 30 rows include EvidenceFile and SourceRef.
- Parent anchor count: 1 ACTIVE IMPLEMENTS_NODE row — no FLOATING_NODE, no AMBIGUOUS_ANCHOR warning.
- Enum values: All canonical (no legacy values).
- TargetDeliverableID populated for DELIVERABLE rows; empty for non-DELIVERABLE rows.
- TargetRefID used for non-deliverable targets (WBS_NODE, REQUIREMENT, DOCUMENT, EXTERNAL).
- Markdown counts consistent with CSV (30 ACTIVE, 0 RETIRED).

---

## Run History

| Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count | RETIRED Count |
|---|---|---|---|---|---|---|
| 2026-02-18 | UPDATE | CONSERVATIVE | Found — Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md | None | 30 | 0 |

---

## Lifecycle Summary

**Total rows:** 30
**ACTIVE:** 30
**RETIRED:** 0

**SatisfactionStatus breakdown (ACTIVE rows):**
- PENDING: 29
- TBD: 1 (DEP-01-02-029, external constraint — deadline itself is not "satisfied" until submission occurs)

**DependencyClass breakdown:**
- ANCHOR: 4
- EXECUTION: 26

**Direction breakdown (ACTIVE):**
- UPSTREAM: 29
- DOWNSTREAM: 1

**Closure notes:** All EXECUTION PREREQUISITE (deliverable) dependencies are marked PENDING — they require upstream deliverables to reach Final maturity before this deliverable can proceed to assembly. The downstream HANDOVER row (DEP-01-02-030) remains PENDING until submission is executed.
