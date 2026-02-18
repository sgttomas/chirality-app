# Dependencies: DEL-01-01 ComplianceMatrixAndChecklist

## Dependency Tracking Mode
- **Mode:** TRACKED (upgraded from NOT_TRACKED by DEPENDENCIES agent run)
- **Register:** Dependencies.csv (schema v3.1)

---

## Declared Upstream (I need these before I can proceed)

- RFP 2024_004 (Sections 6-9) — primary source document for requirement extraction
- Addendum 01, 02, 03 — required inputs for addenda checklist
- Project Decomposition Document — required for deliverable mapping (Scope Ledger, Section 8 Deliverables)
- DEL-01-03 BondingAndInsuranceEvidence — compliance matrix tracks Agreement to Bond as a HIGH pass/fail risk; must receive status confirmation from DEL-01-03 to close risk
- DEL-01-02 FormalSubmissionPackage — compliance matrix tracks Appendix G (Letter of Offer) as a HIGH pass/fail risk; must receive completion status from DEL-01-02 to close risk

## Declared Downstream (These need me)

- DEL-01-02 FormalSubmissionPackage — proposal assembly SHALL NOT commence until Proposal Manager signs off on compliance matrix completion (explicit prerequisite stated in Specification.md and Procedure.md Step 14)

---

## Extracted Dependency Register

**Run date:** 2026-02-18
**Schema version:** v3.1
**Total ACTIVE rows:** 26
**ANCHOR rows (ACTIVE):** 4 (1 parent + 3 trace)
**EXECUTION rows (ACTIVE):** 22
**RETIRED rows:** 0

### ANCHOR Rows

| DependencyID | AnchorType | Direction | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-01-01-001 | IMPLEMENTS_NODE | UPSTREAM | WBS_NODE | — | PKG-01 Compliance & Submission | HIGH |
| DEP-01-01-002 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | SOW-003 | SOW-003 Integrate all addenda into proposal content and pricing | HIGH |
| DEP-01-01-003 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | OBJ-001 | OBJ-001 Pass all mandatory requirements (formal compliance) | HIGH |
| DEP-01-01-004 | TRACES_TO_REQUIREMENT | UPSTREAM | REQUIREMENT | OBJ-008 | OBJ-008 Manage risk and unknowns transparently | HIGH |

### EXECUTION Rows (summary)

| DependencyID | Direction | DependencyType | TargetType | TargetID / TargetName | Statement (short) | Confidence |
|---|---|---|---|---|---|---|
| DEP-01-01-005 | DOWNSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 FormalSubmissionPackage | Compliance matrix sign-off gates proposal assembly | HIGH |
| DEP-01-01-006 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP-2024-004 | RFP Sections 6-9 required as primary extraction input | HIGH |
| DEP-01-01-007 | UPSTREAM | PREREQUISITE | DOCUMENT | ADD-01 | Addendum 01 required for addenda checklist | HIGH |
| DEP-01-01-008 | UPSTREAM | PREREQUISITE | DOCUMENT | ADD-02 | Addendum 02 required for addenda checklist | HIGH |
| DEP-01-01-009 | UPSTREAM | PREREQUISITE | DOCUMENT | ADD-03 | Addendum 03 required for addenda checklist | HIGH |
| DEP-01-01-010 | UPSTREAM | PREREQUISITE | DOCUMENT | DECOMP-V1 | Decomposition Document required for deliverable mapping | HIGH |
| DEP-01-01-011 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 ConceptDesignPackage | Compliance matrix tracks 7.1.1 and Addendum 03 items mapped to DEL-02-01 | HIGH |
| DEP-01-01-012 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-02 DesignBriefNarrative | Compliance matrix tracks 7.1.2-7.1.5 and Addendum 03 items mapped to DEL-02-02 | HIGH |
| DEP-01-01-013 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 AppendixH_ScheduleA | Compliance matrix tracks Proposal Price (35 pts) and addenda acknowledgment gate | HIGH |
| DEP-01-01-014 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 AppendixH_ScheduleB | Compliance matrix tracks Appendix H Schedule B mandatory completeness | HIGH |
| DEP-01-01-015 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 PricingNarrativeAndAssumptions | Compliance matrix tracks Addendum 03 items 1.7 and 1.18 mapped to DEL-05-03 | MEDIUM |
| DEP-01-01-016 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 DesignBuildFirmExperienceProfile | Compliance matrix tracks RFP 7.1.6 and team evaluation criteria mapped to DEL-07-01 | HIGH |
| DEP-01-01-017 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-02 KeyTeamMembersAndResumes | Compliance matrix tracks RFP 7.1.7 mapped to DEL-07-02 | HIGH |
| DEP-01-01-018 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-03 AppendixI_SubtradeAndConsultantList | Compliance matrix tracks Appendix I mandatory appendix completeness | HIGH |
| DEP-01-01-019 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 ConstructionMethodologyNarrative | Compliance matrix tracks RFP 7.2 and 7.3 sub-sections mapped to DEL-04-01 | HIGH |
| DEP-01-01-020 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 CommissioningTrainingCloseoutWarrantyNarrative | Compliance matrix tracks RFP 7.3.6 7.3.7 7.5 7.6 mapped to DEL-06-01 | HIGH |
| DEP-01-01-021 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-08-01 DetailedProjectSchedule | Compliance matrix tracks RFP 7.1.9 and Addendum 03 items 1.2 1.20 mapped to DEL-08-01 | HIGH |
| DEP-01-01-022 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-09-02 SiteConditionsAndDueDiligenceSummary | Compliance matrix tracks RFP 7.4 and Addendum 03 items 1.1 1.6 mapped to DEL-09-02 | HIGH |
| DEP-01-01-023 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-03 BondingAndInsuranceEvidence | Compliance matrix pass/fail risk register tracks Agreement to Bond (DEL-01-03 scope) | HIGH |
| DEP-01-01-024 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-02 FormalSubmissionPackage | Compliance matrix tracks Appendix G completeness owned by DEL-01-02 | HIGH |
| DEP-01-01-025 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 DesignMethodologyNarrative | Compliance matrix tracks RFP 7.1 and Section 8.3 Design Methodology mapped to DEL-03-01 | HIGH |
| DEP-01-01-026 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 DetailedDesignAndConstructionDocsPlan | Compliance matrix tracks RFP 7.1.8 mapped to DEL-03-02 | MEDIUM |

---

## Lifecycle Summary

| Dimension | Count |
|---|---|
| Total rows | 26 |
| ACTIVE | 26 |
| RETIRED | 0 |
| ANCHOR / ACTIVE | 4 |
| EXECUTION / ACTIVE | 22 |
| SatisfactionStatus = TBD | 25 |
| SatisfactionStatus = PENDING | 1 (DEP-01-01-005) |
| Confidence = HIGH | 24 |
| Confidence = MEDIUM | 2 |
| Confidence = LOW | 0 |

**Parent anchor check:** 1 ACTIVE IMPLEMENTS_NODE row found (DEP-01-01-001 → PKG-01). PASS.

---

## Run Notes

**Run date:** 2026-02-18
**Mode:** UPDATE (overwrite)
**Strictness:** CONSERVATIVE
**Agent:** DEPENDENCIES (Type 2)
**Schema version written:** v3.1

**Inputs used:**
- ANCHOR_DOC (chosen): `Datasheet.md` (contains Identification table with Package and Deliverable ID; also references _CONTEXT.md which holds explicit SOW and OBJ traces)
- EXECUTION_DOCS (ordered): `Specification.md`, `Procedure.md`, `Guidance.md` (primary execution signals); `_CONTEXT.md` (corroborating metadata); `_REFERENCES.md` (document pointers)
- DECOMPOSITION_PATH: `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` — located and read successfully
- _REFERENCES.md: read and used to populate TargetLocation for DOCUMENT-type targets

**Decomposition resolution:** SUCCESSFUL. All anchor IDs validated against decomposition:
- PKG-01 confirmed in Section 7
- DEL-01-01 confirmed in Section 8
- SOW-003 confirmed in Section 10 Scope Ledger (maps to DEL-01-01, PKG-01, OBJ-001/OBJ-008)
- OBJ-001 and OBJ-008 confirmed in Section 6
- All target deliverable IDs (DEL-01-02, DEL-01-03, DEL-02-01, DEL-02-02, DEL-03-01, DEL-03-02, DEL-04-01, DEL-05-01, DEL-05-02, DEL-05-03, DEL-06-01, DEL-07-01, DEL-07-02, DEL-07-03, DEL-08-01, DEL-09-02) confirmed in Section 8.

**Defaults and choices:**
- `SOURCE_DOCS`: AUTO — scanned all non-dependency, non-generated files in deliverable folder
- `DOC_ROLE_MAP`: DEFAULT — Datasheet.md matched ANCHOR_DOC heuristic (contains "datasheet"); Specification.md, Procedure.md, Guidance.md matched EXECUTION_DOC heuristic
- `_SEMANTIC.md` and `_SEMANTIC_LENSING.md`: read; used as corroborating context only; not primary evidence sources for dependency rows
- `CONSUMER_CONTEXT`: NONE (not set by invoker); EstimateImpactClass and ConsumerHint populated only for DEP-01-01-005 where evidence strongly supported it

**Pass 1 (ANCHOR) notes:**
- _CONTEXT.md explicitly lists scope traces (SOW-003) and objectives (OBJ-001, OBJ-008); these are direct evidence for TRACES_TO_REQUIREMENT rows.
- Datasheet.md Identification table and Decomposition Section 7 PKG-01 definition together yield the IMPLEMENTS_NODE anchor.
- CONSERVATIVE strictness applied: no plausible-but-implicit anchors added.

**Pass 2 (EXECUTION) notes:**
- The most significant execution dependency found: DEL-01-01 is an explicit gate for DEL-01-02. Two independent source statements (Specification.md Compulsory Status note citing _SEMANTIC_LENSING.md ItemID C-001, and Procedure.md Step 14 citing ItemID X-002) both state proposal assembly cannot commence until this deliverable is signed off. Direction is DOWNSTREAM/PREREQUISITE from this deliverable's perspective (it enables DEL-01-02).
- Document prerequisites (RFP, Addendum 01/02/03, Decomposition) are explicit in Procedure.md Prerequisites section; listed as UPSTREAM/PREREQUISITE against DOCUMENT target type.
- Interface edges to other deliverables (DEL-02-01 through DEL-09-02) reflect the compliance matrix's function: it explicitly tracks the coverage status of those deliverables against RFP requirements. These are real information-flow edges (the compliance matrix receives integration-status signals from those deliverables and records them). Direction is DOWNSTREAM/INTERFACE because DEL-01-01 monitors and records coverage for those deliverables.
- DEL-01-02 and DEL-01-03 also appear as UPSTREAM/INTERFACE targets: the compliance matrix tracks mandatory appendix and Agreement to Bond completion status as HIGH pass/fail risk gates — it must receive confirmation of completion from those deliverables.
- No "coordination-only" or structural-adjacency edges were emitted.
- Excluded: DEL-04-02 (BudgetControlAndChangeManagementPlan) and DEL-04-03 (CommunicationsAndReportingPlan) — Specification.md does not explicitly map them to compliance matrix tracking rows; their inclusion in Section 7.3 narratives is covered under DEL-04-01 scope. CONSERVATIVE.

**Warnings:**
- None. Parent anchor found. No ambiguous anchors.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-18 | UPDATE | CONSERVATIVE | Located and read successfully | None | 26 |
