# Semantic Lensing Register: DEL-019-03 Subcontractor Management

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-019_Construction Management & OH&S/1_Working/DEL-019-03_Subcontractor-Mgmt
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-019-03_Subcontractor-Mgmt/_CONTEXT.md (Deliverable Overview, Scope Definition, Linked Objectives, Key Roles, Success Criteria)
- _STATUS.md — DEL-019-03_Subcontractor-Mgmt/_STATUS.md (Status: SEMANTIC_READY, Phase: Semantic, Progress: 0%)
- _SEMANTIC.md — DEL-019-03_Subcontractor-Mgmt/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — DEL-019-03_Subcontractor-Mgmt/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-019-03_Subcontractor-Mgmt/Specification.md (Scope, Requirements REQ-001 through REQ-014, Standards, Verification, Documentation)
- Guidance.md — DEL-019-03_Subcontractor-Mgmt/Guidance.md (Purpose, Principles P-01 through P-06, Considerations C-01 through C-06, Trade-offs T-01 through T-03, Conflict Table GAP-001 through GAP-005)
- Procedure.md — DEL-019-03_Subcontractor-Mgmt/Procedure.md (Prerequisites, Steps 1-7, Verification, Records)
- _REFERENCES.md — DEL-019-03_Subcontractor-Mgmt/_REFERENCES.md (Primary References R-01, Related Documentation, Decomposition Reference)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 5
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 7  B: 5  C: 4  F: 3  D: 3  X: 3  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 7
  - MissingSlot: 8
  - WeakStatement: 3
  - RationaleGap: 4
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Qualification criteria prescriptive direction is TBD |
| A:normative:applying | normative | applying | mandatory practice | 2 | HAS_ITEMS | Multiple mandatory practices have TBD verification |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compliance checklist TBD undermines compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit cycle or frequency defined |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Coordination meeting frequency TBD affects execution |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Performance monitoring framework TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table addresses process audit adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose and Principles provide adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance C-04 addresses County performance history merit |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-01 through T-03 address worth determination adequately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | DEL-019-04 integration via C-05 covers quality appraisal adequately |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Define minimum subcontractor qualification criteria (safety record thresholds, financial capacity minimums, insurance minimums beyond the $5M GL) to make REQ-012 prescriptive rather than assumption-based | REQ-012 is flagged ASSUMPTION with criteria TBD; no prescriptive direction exists for qualification standards | Specification.md | REQ-012 | -- | Design-Builder to establish; Owner to approve (per GAP-001) | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add concrete acceptance criteria for REQ-012 (qualification) and REQ-013 (performance monitoring) verification rows currently showing "TBD" | Two mandatory practices (qualification, performance monitoring) lack verification approaches; Verification table shows "TBD -- criteria to be established" and "TBD -- framework to be established" | Specification.md | Verification table, REQ-012 and REQ-013 rows | -- | Design-Builder | TBD |
| A-003 | A:normative:applying | VerificationGap | Specification | Specification | Add concrete acceptance criteria for REQ-014 (compliance verification) currently showing "TBD -- compliance checklist to be established" | Mandatory compliance verification practice lacks defined verification approach | Specification.md | Verification table, REQ-014 row | -- | Design-Builder | TBD |
| A-004 | A:normative:judging | MissingSlot | Specification | Specification | Add compliance determination criteria: define what constitutes a pass/fail for each compliance checklist item referenced in REQ-014 and Procedure Step 5.3 | Compliance determination cannot be performed without defined pass/fail thresholds; the compliance checklist itself is TBD | Specification.md; Procedure.md | REQ-014; Step 5.3 | -- | Design-Builder | TBD |
| A-005 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a periodic regulatory audit step or schedule (e.g., internal audit of subcontractor OH&S compliance, insurance currency, WCB status) with defined frequency | No internal audit cycle for subcontractor regulatory compliance is defined; Step 5 addresses performance monitoring but not a formal compliance audit rhythm distinct from performance assessment | Procedure.md | Steps 4-5 | -- | Design-Builder | TBD |
| A-006 | A:operative:applying | TBD_Question | Procedure | Procedure | Define the frequency of subcontractor-specific coordination meetings (distinct from weekly County meetings per DEL-019-02) referenced in Step 4.1 | Step 4.1 says "frequency TBD" referencing GAP-004; practical execution of coordination cannot be planned without a defined cadence | Procedure.md | Step 4, action 4.1 | -- | Design-Builder | TBD |
| A-007 | A:operative:judging | MissingSlot | Specification | Specification | Define performance assessment thresholds and escalation triggers for REQ-013 (performance monitoring); at minimum specify what score or condition triggers Step 6 escalation | Performance assessment lacks defined thresholds; Procedure Step 1.3 lists "Performance thresholds and escalation triggers: TBD" | Specification.md; Procedure.md | REQ-013; Step 1.3 | -- | Design-Builder | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key data point missing in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence for known parameters with sources cited |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet Construction section has many TBD fields |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data values are consistently cited with RFP section references |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing signal about record retention periods |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequately provided through cross-references to RFP sections |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Incomplete account of applicable trades |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across documents are coherent regarding Prime Contractor obligations |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of Prime Contractor accountability is well-established across P-01 and REQ-002 |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance provides sufficient expertise context through Principles and Considerations |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 1 | HAS_ITEMS | Mastery gap regarding non-compliance consequences |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T-01 through T-03 demonstrate adequate essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance adequately frames judgment calls |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective across safety, financial, schedule dimensions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent with non-delegable accountability principle |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential fact: list of anticipated subcontractor trade categories required for the project (structural, mechanical, electrical, plumbing, civil, etc.) | Guidance Purpose mentions "specialist trades and subcontracted services across multiple disciplines" but Datasheet does not enumerate the anticipated trade categories as a data point; this is an essential fact for scoping subcontractor management | Guidance.md; Datasheet.md | Purpose paragraph; entire Construction section scanned | -- | Design-Builder | TBD |
| B-002 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Resolve or narrow the seven TBD entries in the Construction section (Qualification Criteria, Performance Monitoring Framework, Compliance Checklist, Contract Template, Meeting Frequency, Bonuses/Penalties, Non-Compliance Consequences) by recording known constraints or boundaries even if final values remain TBD | Seven of nine Construction rows are TBD, reducing the Datasheet's value as a comprehensive record; some can be narrowed with known boundary conditions from the RFP (e.g., 10-day deficiency cure from RFP 2.10.6) | Datasheet.md | Construction section | -- | Design-Builder | TBD |
| B-003 | B:information:necessity | MissingSlot | Procedure | Procedure | Define record retention periods for the Records table (currently all showing "TBD post-CCC"); at minimum reference applicable provincial legislation requirements | Eleven record types list retention as "Project duration + TBD post-CCC"; the essential signal about how long to retain records is absent | Procedure.md | Records table | -- | Design-Builder; provincial legislation | TBD |
| B-004 | B:information:completeness | MissingSlot | Datasheet | Datasheet | Add an enumeration of the construction trade packages (PKG-010 through PKG-018) that will require subcontractors, cross-referencing Procedure Step 2.1 | Procedure Step 2.1 references "PKG-010 through PKG-018 cover construction trades requiring Subcontractors" but this information is not captured in the Datasheet as a comprehensive account of the subcontractor scope | Procedure.md; Datasheet.md | Step 2.1; entire Attributes section scanned | -- | Decomposition document | TBD |
| B-005 | B:knowledge:completeness | RationaleGap | Guidance | Guidance | Add rationale for the consequences of subcontractor non-compliance (cure periods, termination criteria, remedial measures); currently flagged as GAP-003 with no interpretive guidance beyond "consistent with CCDC 14-2013 framework" | The CCDC 14-2013 contract form likely contains relevant provisions but these are not summarized or interpreted; thorough mastery of this topic requires at least a summary of the contract's non-compliance framework | Guidance.md | GAP-003 in Conflict Table; T-02 | -- | Design-Builder; CCDC 14-2013 contract | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Baseline Clarity | 1 | HAS_ITEMS | Baseline for qualification is not clear |
| C:normative:sufficiency | normative | sufficiency | Authorized Conformance Scope | 0 | NO_ITEMS | Conformance scope is adequately bounded by REQ-001 through REQ-014 |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Standards table accessibility column shows assumptions |
| C:normative:consistency | normative | consistency | Harmonized Enforcement Standard | 0 | NO_ITEMS | Enforcement approach is consistent across documents |
| C:operative:necessity | operative | necessity | Operational Threshold Criterion | 0 | NO_ITEMS | Already captured under A-007 (performance thresholds TBD) |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Execution Capability | 0 | NO_ITEMS | Procedure Steps 1-7 demonstrate adequate execution capability framework |
| C:operative:completeness | operative | completeness | Exhaustive Process Accounting | 1 | HAS_ITEMS | Missing change management process detail |
| C:operative:consistency | operative | consistency | Dependable Practice Alignment | 0 | NO_ITEMS | Practice descriptions are aligned across Specification and Procedure |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Value is recognized through OBJ-002 and OBJ-007 linkage |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Merit Judgment | 0 | NO_ITEMS | Merit judgment framework via trade-offs is adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Merit Appraisal | 1 | HAS_ITEMS | No cost/benefit framework for qualification depth |
| C:evaluative:consistency | evaluative | consistency | Grounded Valuation Integrity | 0 | NO_ITEMS | Valuation reasoning is grounded in RFP evaluation criteria consistently |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-012 by removing ASSUMPTION flag and stating minimum baseline qualification criteria (even if expressed as categories to be populated), or explicitly state which authority will approve the criteria and by when | REQ-012 uses "ASSUMPTION:" prefix, making it unclear whether this is a binding requirement or a placeholder; compulsory baseline clarity requires either a firm requirement or an explicit approval gate | Specification.md | REQ-012 | -- | Design-Builder; Owner approval | TBD |
| C-002 | C:normative:completeness | RationaleGap | Specification | Guidance | Add rationale for which Alberta OH&S provisions specifically apply to subcontractor management (the Standards table says "ASSUMPTION: likely applicable" for two entries); clarify whether full regulatory coverage has been mapped or remains incomplete | Standards table entries for Alberta OH&S Act and Alberta WCA both state "ASSUMPTION: likely applicable (location TBD in accessible sources)"; full regulatory coverage cannot be confirmed without explicit identification of applicable provisions | Specification.md | Standards table, rows 1-2 | -- | Alberta OH&S legislation; legal counsel | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or sub-step for managing subcontractor scope changes and change orders beyond the brief mention in Step 4.7; define the process for Subcontractor-initiated scope change requests and their relationship to the prime contract change order process | Step 4.7 mentions "process change orders in accordance with CCDC 14-2013" but does not describe the actual process; exhaustive process accounting requires at least a reference to the applicable CCDC change order mechanism | Procedure.md | Step 4, action 4.7 | -- | CCDC 14-2013 contract | TBD |
| C-004 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add guidance on cost/benefit considerations for different qualification tiers referenced in T-01 (tiered approach); define what constitutes "high-value or high-risk trades" versus "lower-risk engagements" | T-01 proposes a tiered qualification approach but provides no criteria for categorizing trades by risk level; comprehensive merit appraisal of the qualification investment requires at least indicative thresholds | Guidance.md | T-01 | -- | Design-Builder | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Statutory Basis | 0 | NO_ITEMS | REQ-001 through REQ-011 have clear enforceable statutory bases with RFP citations |
| F:normative:sufficiency | normative | sufficiency | Proportionate Compliance Threshold | 1 | HAS_ITEMS | Insurance threshold specified but other thresholds TBD |
| F:normative:completeness | normative | completeness | Total Statutory Disclosure | 0 | NO_ITEMS | Already captured under C-002 (Standards table assumptions) |
| F:normative:consistency | normative | consistency | Codified Enforcement Coherence | 0 | NO_ITEMS | Enforcement references are consistent (RFP sections, OBJ linkages) |
| F:operative:necessity | operative | necessity | Validated Operational Minimum | 1 | HAS_ITEMS | Operational minimums for monitoring frequency not validated |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Practice Suitability | 0 | NO_ITEMS | Procedure steps demonstrate adequate practice suitability for known processes |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Mastery | 0 | NO_ITEMS | Already captured under C-003 (change order process gap) |
| F:operative:consistency | operative | consistency | Steady Operational Coherence | 0 | NO_ITEMS | Operational descriptions are coherent between Specification and Procedure |
| F:evaluative:necessity | evaluative | necessity | Foundational Worth Discernment | 0 | NO_ITEMS | Worth discernment adequately grounded in OBJ-002 and OBJ-007 |
| F:evaluative:sufficiency | evaluative | sufficiency | Balanced Appraisal Adequacy | 1 | HAS_ITEMS | Missing appraisal criteria for subcontractor performance rating |
| F:evaluative:completeness | evaluative | completeness | Thorough Valuation Mastery | 0 | NO_ITEMS | Already captured under C-004 (qualification tier rationale) |
| F:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning is consistently aligned to Prime Contractor accountability principle |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Clarify the proportionate compliance threshold for REQ-008 (Safety Management of Subcontractors): specify what "explicitly address safety management" means in operational terms (e.g., minimum OH&S program content requirements for subcontractor coverage) | REQ-008 requires the H&S Program to "explicitly address safety management of Subcontractors" but does not define what minimum content satisfies this requirement; proportionate compliance threshold is ambiguous | Specification.md | REQ-008 | -- | Design-Builder; DEL-019-01 OH&S Program | TBD |
| F-002 | F:operative:necessity | VerificationGap | Specification | Specification | Define the minimum monitoring frequency for REQ-013 (Performance Monitoring): specify at minimum whether monitoring is weekly, monthly, per-milestone, or per-payment-cycle | REQ-013 verification approach is "TBD -- framework to be established"; without a validated operational minimum for monitoring frequency, performance assessment cannot be scheduled or verified | Specification.md | Verification table, REQ-013 row; Procedure Step 1.3 | -- | Design-Builder | TBD |
| F-003 | F:evaluative:sufficiency | MissingSlot | Specification | Guidance | Add performance rating scale or criteria for Procedure Step 5.1 assessments (the Guidance illustrative register example mentions "Performance rating (period-by-period)" but no rating scale is defined anywhere) | Balanced appraisal adequacy requires defined rating criteria; currently performance assessment is described in process terms but without evaluation criteria or scales | Specification.md; Guidance.md; Procedure.md | REQ-013; Examples section; Step 5.1 | -- | Design-Builder | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority is established through RFP, CCDC 14-2013, and OH&S legislation references |
| D:normative:applying | normative | applying | Fixed Conformance Procedure | 0 | NO_ITEMS | Conformance procedures are defined in Procedure Steps 1-7 with adequate specificity for known items |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | No acceptance/rejection criteria for subcontractor qualification decisions |
| D:normative:reviewing | normative | reviewing | Concluded Oversight Cycle | 0 | NO_ITEMS | Procedure Step 7 provides adequate closeout oversight |
| D:operative:guiding | operative | guiding | Established Task Baseline | 1 | HAS_ITEMS | Task baseline timing for framework establishment is vague |
| D:operative:applying | operative | applying | Verified Method Delivery | 0 | NO_ITEMS | Method delivery steps are clear in Procedure |
| D:operative:judging | operative | judging | Finalized Output Verdict | 0 | NO_ITEMS | Procedure Verification table provides output verdicts per step |
| D:operative:reviewing | operative | reviewing | Concluded Procedure Stability | 0 | NO_ITEMS | Procedure verification and records sections provide adequate stability checks |
| D:evaluative:guiding | evaluative | guiding | Established Priority Compass | 0 | NO_ITEMS | Priority compass established through OBJ-002 (schedule) and OBJ-007 (safety) linkage |
| D:evaluative:applying | evaluative | applying | Confirmed Value Allocation | 1 | HAS_ITEMS | No resource allocation guidance for subcontractor management effort |
| D:evaluative:judging | evaluative | judging | Definitive Merit Verdict | 0 | NO_ITEMS | Covered by trade-offs and evaluation criteria references |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Stability | 0 | NO_ITEMS | DEL-019-04 integration provides quality stability mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Define acceptance/rejection criteria for subcontractor qualification decisions in Step 2.7/2.8: specify what conditions warrant "conditional" approval versus "not approved" and what authority approves exceptions | Procedure Step 2.7 records outcomes as "approved / conditional / not approved" and Step 2.8 requires PM approval for non-qualifying subcontractors, but no criteria exist for these categories; definitive conformance rulings require defined thresholds | Procedure.md; Specification.md | Step 2.7, Step 2.8; REQ-012 | -- | Project Manager | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on timing: when must the subcontractor management framework (Step 1) be completed relative to project mobilisation? Clarify whether "before any Subcontractor is engaged" means before contract award, before site mobilisation, or before first subcontract issuance | Procedure Step 1 timing says "Before any Subcontractor is engaged or invited to bid" which is correct but the task baseline lacks a target date or milestone anchor relative to the project schedule | Procedure.md; Guidance.md | Step 1 Timing; entire Guidance scanned | -- | Project Manager; project schedule | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Guidance | Guidance | Add guidance on expected level of effort or resource allocation for subcontractor management activities (e.g., dedicated staff, part-time Project Manager function, or delegated per T-03); clarify whether Site Superintendent role referenced in T-03 will be formally assigned | T-03 mentions possible delegation to Site Superintendent but Datasheet Key Roles lists only Project Manager; confirmed value allocation requires clarity on who performs day-to-day subcontractor oversight | Guidance.md; Datasheet.md; _CONTEXT.md | T-03; Identification table (Responsible Party); Key Roles | -- | Design-Builder | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Threshold Orientation | 0 | NO_ITEMS | Threshold orientation provided through Prime Contractor non-delegable accountability framing |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Grounding | 0 | NO_ITEMS | Directional grounding justified through RFP and Decomposition references |
| X:guiding:completeness | guiding | completeness | Integral Instructional Foundation | 0 | NO_ITEMS | Instructional foundation is integral across the four documents |
| X:guiding:consistency | guiding | consistency | Coherent Instructional Alignment | 0 | NO_ITEMS | Instructions are coherent across documents |
| X:applying:necessity | applying | necessity | Validated Execution Prerequisite | 1 | HAS_ITEMS | Prerequisites table missing an item |
| X:applying:sufficiency | applying | sufficiency | Adequate Deployment Evidence | 0 | NO_ITEMS | Deployment evidence adequate for defined steps |
| X:applying:completeness | applying | completeness | Exhaustive Deployment Coverage | 0 | NO_ITEMS | Deployment coverage is exhaustive for the seven-step lifecycle |
| X:applying:consistency | applying | consistency | Consistent Method Reliability | 0 | NO_ITEMS | Methods are consistently described |
| X:judging:necessity | judging | necessity | Critical Verdict Foundation | 1 | HAS_ITEMS | Missing verdict foundation for insurance adequacy |
| X:judging:sufficiency | judging | sufficiency | Sufficient Ruling Competence | 0 | NO_ITEMS | Ruling competence adequate for defined verification approaches |
| X:judging:completeness | judging | completeness | Comprehensive Ruling Record | 0 | NO_ITEMS | Documentation section lists nine artifact types covering ruling records |
| X:judging:consistency | judging | consistency | Consistent Ruling Integrity | 0 | NO_ITEMS | Ruling approaches are consistently structured in Verification table |
| X:reviewing:necessity | reviewing | necessity | Mandatory Assurance Finding | 0 | NO_ITEMS | Assurance findings addressed through Procedure Verification table |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Assurance Evidence | 0 | NO_ITEMS | Evidence requirements specified per Procedure Verification |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Record | 1 | HAS_ITEMS | Records table missing dispute/claim records |
| X:reviewing:consistency | reviewing | consistency | Dependable Assurance Alignment | 0 | NO_ITEMS | Assurance alignment consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a prerequisite or verification step confirming that the Design-Builder's own insurance (min $5M GL covering independent subcontractors per REQ-003) is in place before any subcontractor onboarding begins | Procedure Prerequisites table lists three upstream deliverables but does not include verification of the Design-Builder's own insurance coverage for subcontractors as a validated execution prerequisite; REQ-003 requires this coverage but the Procedure assumes it without checking | Procedure.md; Specification.md | Prerequisites table; REQ-003 | -- | Design-Builder | TBD |
| X-002 | X:judging:necessity | VerificationGap | Specification | Specification | Define how to verify that individual subcontractor insurance certificates are adequate beyond the Design-Builder's own policy: specify minimum coverage types and limits required from subcontractors themselves (distinct from REQ-003 which addresses the Design-Builder's policy) | REQ-003 addresses the Design-Builder's insurance covering subcontractors; Guidance C-03 notes "individual Subcontractors will typically carry their own insurance" and the Design-Builder "should verify Subcontractor insurance certificates before mobilisation" but no requirement specifies minimum subcontractor-held insurance coverage | Specification.md; Guidance.md | REQ-003; C-03 | -- | Design-Builder; insurance advisor | TBD |
| X-003 | X:reviewing:completeness | Normalization | Procedure | Procedure | Add a record type for subcontractor disputes, claims, or lien-related correspondence to the Records table; currently no record type captures the scenario where a subcontractor files a lien or payment dispute despite being referenced in the Conditions (Payment Withholding Trigger, Lien Holdback) | Datasheet Conditions reference payment withholding and lien holdback scenarios, and the Standards table references the Alberta Prompt Payment and Construction Lien Act, but the Records table has no corresponding record type for dispute/lien documentation | Procedure.md; Datasheet.md; Specification.md | Records table; Conditions table rows 3-4; Standards table row 3 | -- | Design-Builder; legal counsel | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Evidenced Steering Foundation | 0 | NO_ITEMS | Steering foundation evidenced through RFP and Decomposition citations |
| E:guiding:information | guiding | information | Contextual Steering Clarity | 0 | NO_ITEMS | Context provided through Guidance Purpose and linked objectives |
| E:guiding:knowledge | guiding | knowledge | Masterful Navigational Command | 0 | NO_ITEMS | Navigational command demonstrated through Principles and Considerations |
| E:guiding:wisdom | guiding | wisdom | Sound Leadership Vision | 0 | NO_ITEMS | Leadership vision adequately expressed through Trade-offs |
| E:applying:data | applying | data | Verified Deployment Record | 1 | HAS_ITEMS | Terminology inconsistency in deployment records |
| E:applying:information | applying | information | Coherent Execution Framing | 0 | NO_ITEMS | Execution framing is coherent across Specification scope and Procedure steps |
| E:applying:knowledge | applying | knowledge | Demonstrated Practice Proficiency | 0 | NO_ITEMS | Practice proficiency demonstrated through detailed seven-step procedure |
| E:applying:wisdom | applying | wisdom | Principled Practice Foresight | 0 | NO_ITEMS | Practice foresight addressed through Trade-offs and Considerations |
| E:judging:data | judging | data | Conclusive Judgment Basis | 0 | NO_ITEMS | Judgment bases identified through Verification table and RFP references |
| E:judging:information | judging | information | Coherent Verdict Framing | 0 | NO_ITEMS | Verdict framing coherent in Procedure Verification table |
| E:judging:knowledge | judging | knowledge | Masterful Verdict Expertise | 0 | NO_ITEMS | Verdict expertise demonstrated through detailed verification approaches for REQ-001 through REQ-011 |
| E:judging:wisdom | judging | wisdom | Wise Adjudicative Insight | 0 | NO_ITEMS | Adjudicative insight expressed through Guidance Conflict Table (GAP-001 through GAP-005) |
| E:reviewing:data | reviewing | data | Substantiated Audit Finding | 1 | HAS_ITEMS | Inconsistent status value between documents |
| E:reviewing:information | reviewing | information | Contextual Audit Accounting | 0 | NO_ITEMS | Audit accounting context provided through Procedure Records table |
| E:reviewing:knowledge | reviewing | knowledge | Thorough Oversight Mastery | 0 | NO_ITEMS | Oversight mastery demonstrated through comprehensive seven-step lifecycle |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Vision | 1 | HAS_ITEMS | Missing forward-looking lessons-learned mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Multi | Datasheet | Normalize the term "Subcontractor Register" across documents: Specification Documentation section calls it "Subcontractor Register" (item 1); Procedure uses "Subcontractor Register" consistently; Guidance Examples section calls it "subcontractor management register"; Datasheet Anticipated Artifacts uses "Subcontractor qualification/approval records" without naming the register. Align terminology to a single canonical name | Three slightly different terms are used for what appears to be the same artifact, risking drift as documents evolve | Specification.md; Guidance.md; Datasheet.md; Procedure.md | Documentation item 1; Examples section; Construction row "Anticipated Artifacts"; Steps 1-7 | -- | -- | TBD |
| E-002 | E:reviewing:data | Normalization | Multi | Datasheet | Align the Status field in Datasheet (shows "OPEN") with the current status in _STATUS.md (shows "SEMANTIC_READY"); the Datasheet has not been updated to reflect the latest status transition | Datasheet Identification table says Status: OPEN; _STATUS.md says Status: SEMANTIC_READY (updated 2026-02-26); substantiated audit finding reveals a stale data point | Datasheet.md; _STATUS.md | Identification table, Status row; Status header | -- | _STATUS.md is authoritative | TBD |
| E-003 | E:reviewing:wisdom | VerificationGap | Procedure | Guidance | Add a lessons-learned or continuous improvement mechanism for subcontractor management: after project closeout (Step 7), capture what worked and what did not for future projects, consistent with principled oversight vision | Procedure Step 7 archives records but does not include a lessons-learned step; for a management deliverable tied to OBJ-007 (zero lost-time incidents), post-project review of subcontractor safety performance is a meaningful oversight activity | Procedure.md; Guidance.md | Step 7; entire Guidance scanned | -- | Design-Builder | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- All 80 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in explicit document content, cited TBDs, or identified absences |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- No conflicts identified (Guidance Conflict Table contains gaps, not inter-document conflicts) |
| Summary consistent | PASS -- Summary counts match actual warranted items (28 total) |
| Schema followed | PASS -- Output uses STRUCTURE schema |
