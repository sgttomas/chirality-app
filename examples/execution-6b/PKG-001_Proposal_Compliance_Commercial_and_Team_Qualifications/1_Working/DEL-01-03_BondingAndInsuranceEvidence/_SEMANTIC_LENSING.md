# Semantic Lensing Register: DEL-01-03 Bonding and Insurance Evidence

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-001_Proposal_Compliance_Commercial_and_Team_Qualifications/1_Working/DEL-01-03_BondingAndInsuranceEvidence
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-01-03 context; SOW-0004; OBJ-001, OBJ-007
- _STATUS.md -- Current state SEMANTIC_READY; last updated 2026-02-17
- _SEMANTIC.md -- All 7 matrices (A, B, C, F, D, X, E) parsed; 92 cells total; no parse errors
- Datasheet.md -- Present and read
- Specification.md -- Present and read
- Guidance.md -- Present and read
- Procedure.md -- Present and read
- _REFERENCES.md -- Present and read

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 14
- By document:
  - Datasheet: 3
  - Specification: 5
  - Guidance: 2
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 3  B: 3  C: 1  F: 2  D: 1  X: 3  E: 1
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 3
  - WeakStatement: 2
  - RationaleGap: 1
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Bond form assumption needs confirmation |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Appendix J SC 50-52 policy limits TBD |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Pass/fail criteria well-defined across docs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Agreement to Bond vs executed bond ambiguity |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps adequately covered |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks cover performance |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA reviewer roles assigned in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Strategic rationale in Guidance is clear |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Cost treatment principles adequately stated |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost certainty commitment is clear |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks embedded in verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Clarify whether bond forms are CCDC-19/CCDC-20 or an alternative; currently stated as "ASSUMPTION" without resolution path beyond "confirm against Appendix J text" | The prescriptive direction for bond form selection is marked as assumption in Datasheet and Specification; if Appendix J specifies a different form, current documents may need revision; the resolution path should be explicit | Datasheet.md; Specification.md | Datasheet: "Bond Forms" under Construction; Specification: R-001 table "Bond Form" row | -- | Appendix J SC 50 | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Confirm specific policy limits, deductibles, and additional insured wording from Appendix J SC 50-52; currently referenced as "location TBD" across all documents | Mandatory practice under SC 50-52 governs insurance requirements, but specific limits are not yet extracted from Appendix J; this blocks accurate Schedule B insurance costing and verification of coverage adequacy | Specification.md; Datasheet.md; Guidance.md | Specification: Standards table "Appendix J" row; Datasheet: References table Appendix J row; Guidance: C-003 | -- | Appendix J SC 50-52 full text | TBD |
| A-003 | A:normative:reviewing | Conflict | Procedure | Multi | Resolve whether RFP 5.3.1 requires a fully executed bond instrument at proposal submission or an "Agreement to Bond" (surety pre-commitment letter); Procedure Note N-001 flags this ambiguity but no resolution path is assigned | Procedure N-001 explicitly identifies this ambiguity but the Datasheet and Specification assume full execution is required; regulatory audit under this lens reveals the distinction is consequential for procurement timeline and compliance | Procedure.md; Datasheet.md; Specification.md | Procedure: Note N-001; Datasheet: Conditions "Execution Requirement" row; Specification: R-001 "Submission" row | Procedure.md#Note N-001 (Agreement to Bond = possibly pre-commitment letter); Datasheet.md#Conditions (assumes executed document); Specification.md#R-001 (assumes executed document) | RFP Section 5.3.1 / Town RFP administrator | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Bond duration language inconsistency |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence requirements well-specified |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing surety registry verification detail |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Bond amount calculation method consistent |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Decision authority (DEC-011) consistently cited |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | CCIP vs OCIP context adequately explained |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-reference network is complete |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Payment bond beneficiary description varies |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Bonding/insurance fundamentals adequately covered |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Broker/surety expertise requirements stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage types comprehensively listed |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of CCIP consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Risk allocation reasoning present in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers both bonding and insurance holistically |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | Normalization | Datasheet | Multi | Harmonize bond duration language: Datasheet says "12-month warranty period" for Performance Bond duration but Payment Bond says "statutory lien period (typically 2 years post-substantial performance in Alberta)"; Specification R-001 says "From contract execution through substantial performance + 12-month warranty period" for both bond types without distinguishing | Essential fact about bond duration differs between Performance Bond and Payment Bond in Datasheet, but Specification R-001 collapses both to a single duration statement; the Payment Bond has a different legal duration (statutory lien period) which is correctly stated in Datasheet but not reflected in Specification | Datasheet.md; Specification.md | Datasheet: Construction > Artifact 1 (Performance Bond "Duration" vs Payment Bond "Duration"); Specification: R-001 table "Duration" row | Datasheet.md#Performance Bond Duration ("substantial performance + 12-month warranty"); Datasheet.md#Payment Bond Duration ("statutory lien period, typically 2 years"); Specification.md#R-001 Duration ("contract execution through substantial performance + 12-month warranty period") | RFP Section 5.3.1 / Appendix J SC 50-51 | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add specific Alberta Insurance Council registry URL or verification method for confirming surety authorization; currently says "confirm against Alberta Insurance Council registry or equivalent" without providing the lookup mechanism | Comprehensive record lens reveals that the verification method for surety Alberta authorization is described generically but no specific registry URL, phone number, or search method is provided; this could delay the verification step in Procedure Step 1 | Datasheet.md; Procedure.md | Datasheet: Conditions "Surety Authorization" row; Procedure: PR-002 | -- | Alberta Insurance Council | TBD |
| B-003 | B:information:consistency | Normalization | Datasheet | Specification | Harmonize Payment Bond beneficiary description: Datasheet says "Lien claimants; Town of Penhold may also be named" while Specification R-001 says "Lien claimants + Town of Penhold (Payment Bond)" -- "may also be named" vs definitive inclusion | The coherent message lens reveals a minor but legally significant inconsistency: whether the Town is definitively named as Payment Bond beneficiary or only potentially named; this should be resolved to one consistent statement | Datasheet.md; Specification.md | Datasheet: Construction > Payment Bond "Beneficiary"; Specification: R-001 table "Beneficiary" row | Datasheet.md#Payment Bond Beneficiary ("may also be named"); Specification.md#R-001 Beneficiary ("Lien claimants + Town of Penhold") | RFP Section 5.3.1 / Appendix J SC 51 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 0 | NO_ITEMS | C-08 constraint well-documented |
| C:normative:sufficiency | normative | sufficiency | Compliance Sufficiency | 0 | NO_ITEMS | Sufficiency criteria in VER-001 through VER-005 |
| C:normative:completeness | normative | completeness | Exhaustive Mandate | 0 | NO_ITEMS | All mandate elements enumerated |
| C:normative:consistency | normative | consistency | Uniform Compliance | 0 | NO_ITEMS | Compliance language consistent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | PR-001 through PR-004 cover prerequisites |
| C:operative:sufficiency | operative | sufficiency | Practiced Competence | 0 | NO_ITEMS | Competence requirements stated |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 1 | HAS_ITEMS | Missing fallback if surety declines |
| C:operative:consistency | operative | consistency | Reliable Process | 0 | NO_ITEMS | Process steps consistently described |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Value proposition clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation | 0 | NO_ITEMS | Cost treatment adequately described |
| C:evaluative:completeness | evaluative | completeness | Holistic Appraisal | 0 | NO_ITEMS | Full cost picture provided |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add contingency step or decision gate for scenario where primary surety declines bonding capacity or fails to deliver executed bonds within the proposal timeline; Guidance C-002 mentions co-bonding as an option but Procedure has no corresponding contingency step | Comprehensive execution lens reveals that while Guidance C-002 mentions limited bonding capacity and co-bonding arrangements, the Procedure does not include a contingency pathway if the primary surety declines; this is a gap in execution completeness for a critical-path compliance item | Procedure.md; Guidance.md | Procedure: Steps 1 and 5 (no fallback); Guidance: C-002 (mentions backup surety and co-bonding) | -- | Proposal Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandate Threshold | 0 | NO_ITEMS | Mandate threshold clearly defined (C-08) |
| F:normative:sufficiency | normative | sufficiency | Prescribed Threshold | 1 | HAS_ITEMS | WC exemption verification gap |
| F:normative:completeness | normative | completeness | Total Compliance Scope | 0 | NO_ITEMS | All compliance requirements enumerated |
| F:normative:consistency | normative | consistency | Harmonized Mandate | 0 | NO_ITEMS | Mandate consistently stated |
| F:operative:necessity | operative | necessity | Core Capability Need | 0 | NO_ITEMS | Core capabilities identified |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Readiness | 0 | NO_ITEMS | Readiness verification in prerequisites |
| F:operative:completeness | operative | completeness | Thorough Operational Scope | 0 | NO_ITEMS | Operational scope complete |
| F:operative:consistency | operative | consistency | Systematic Reliability | 0 | NO_ITEMS | Systematic approach consistent |
| F:evaluative:necessity | evaluative | necessity | Grounded Merit | 0 | NO_ITEMS | Merit grounding adequate |
| F:evaluative:sufficiency | evaluative | sufficiency | Sound Assessment | 0 | NO_ITEMS | Assessment approach sound |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation | 1 | HAS_ITEMS | Missing verification for insurance quote currency |
| F:evaluative:consistency | evaluative | consistency | Evaluative Integrity | 0 | NO_ITEMS | Evaluative consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification item for Workers' Compensation exemption status determination; Guidance C-004 identifies the WC exemption question and notes Appendix J SC 52 may override, but no verification step exists in Specification or Procedure to confirm this | Prescribed threshold lens reveals that WC coverage is listed as a required coverage type in R-002 but the exemption pathway described in Guidance C-004 has no corresponding verification or acceptance criterion; this could result in either unnecessary cost inclusion or non-compliance | Specification.md; Guidance.md; Procedure.md | Specification: R-002 "Scope of Coverage" (lists WC); Guidance: C-004 (exemption discussion); Procedure: Step 2 (mentions WC but no exemption check) | -- | Alberta Workers' Compensation Act / Appendix J SC 52 | TBD |
| F-002 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add verification criterion confirming insurance broker quote is dated within 2-3 weeks of submission deadline; Procedure Step 2 verification mentions this but Specification VER-003/VER-004 do not include quote currency as a success criterion | Exhaustive valuation lens reveals that the cost basis for CCIP insurance depends on quote currency (Guidance C-005 and Procedure Step 2 both mention 2-3 week window), but Specification verification items do not include this temporal requirement as a formal acceptance criterion | Specification.md; Procedure.md; Guidance.md | Specification: VER-003 and VER-004 (no date currency check); Procedure: Step 2 Verification (mentions 2-3 weeks); Guidance: C-005 (mentions timing) | -- | Proposal Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Directive | 0 | NO_ITEMS | Directive is settled (C-08 + DEC-011) |
| D:normative:applying | normative | applying | Enforced Standard | 0 | NO_ITEMS | Standards consistently enforced |
| D:normative:judging | normative | judging | Definitive Conformance | 0 | NO_ITEMS | Conformance criteria definitive |
| D:normative:reviewing | normative | reviewing | Mandated Oversight | 0 | NO_ITEMS | Oversight via VER-001 through VER-005 |
| D:operative:guiding | operative | guiding | Established Workflow | 0 | NO_ITEMS | 7-step workflow established |
| D:operative:applying | operative | applying | Confirmed Performance | 0 | NO_ITEMS | Performance criteria confirmed |
| D:operative:judging | operative | judging | Operational Verdict | 0 | NO_ITEMS | V-001 through V-004 provide verdict criteria |
| D:operative:reviewing | operative | reviewing | Validated Workflow | 0 | NO_ITEMS | Workflow validation in Step 7 |
| D:evaluative:guiding | evaluative | guiding | Purposive Quality | 1 | HAS_ITEMS | Missing rationale for contingency cost absorption |
| D:evaluative:applying | evaluative | applying | Realized Worth | 0 | NO_ITEMS | Worth realization adequately covered |
| D:evaluative:judging | evaluative | judging | Definitive Worth | 0 | NO_ITEMS | Worth criteria defined |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality | 0 | NO_ITEMS | Quality assurance covered |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add brief rationale or risk quantification guidance for the insurance market hardening scenario; Guidance C-005 states the proponent absorbs cost changes but provides no guidance on how to assess or bound this risk in the pricing decision | Purposive quality lens reveals that while Guidance C-005 correctly identifies the insurance market volatility risk, it does not provide decision-support guidance on how to assess the magnitude of this risk or whether any risk margin is appropriate in Schedule B pricing; this could lead to either underpricing (absorbing unbudgeted cost) or overpricing (adding contingency the Guidance says not to add) | Guidance.md | Guidance: C-005 "Insurance Market Volatility and Cost Certainty Commitment" | -- | Commercial Lead | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Direction | 0 | NO_ITEMS | Foundational direction established |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Direction | 0 | NO_ITEMS | Direction sufficiently warranted |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance | 0 | NO_ITEMS | Guidance comprehensive |
| X:guiding:consistency | guiding | consistency | Coherent Orientation | 0 | NO_ITEMS | Orientation coherent |
| X:applying:necessity | applying | necessity | Enforced Prerequisite | 1 | HAS_ITEMS | Missing pre-submission file size check |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Capacity | 0 | NO_ITEMS | Capacity demonstration covered |
| X:applying:completeness | applying | completeness | Thorough Implementation | 0 | NO_ITEMS | Implementation steps thorough |
| X:applying:consistency | applying | consistency | Disciplined Execution | 0 | NO_ITEMS | Execution discipline maintained |
| X:judging:necessity | judging | necessity | Judgment Foundation | 1 | HAS_ITEMS | Submission deadline in Procedure needs verification |
| X:judging:sufficiency | judging | sufficiency | Qualified Determination | 0 | NO_ITEMS | Determination criteria qualified |
| X:judging:completeness | judging | completeness | Exhaustive Verdict | 1 | HAS_ITEMS | No verification of surety name consistency |
| X:judging:consistency | judging | consistency | Principled Judgment | 0 | NO_ITEMS | Judgment principles consistent |
| X:reviewing:necessity | reviewing | necessity | Assurance Foundation | 0 | NO_ITEMS | Assurance foundation present |
| X:reviewing:sufficiency | reviewing | sufficiency | Confirmed Assurance | 0 | NO_ITEMS | Assurance confirmed |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance | 0 | NO_ITEMS | Assurance checks comprehensive |
| X:reviewing:consistency | reviewing | consistency | Reliable Assurance | 0 | NO_ITEMS | Assurance reliability maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add a verification sub-step in Step 7 to confirm that the bond PDF file size, when combined with the main proposal PDF, does not exceed the 15 MB RFP limit (RFP 4.2); currently Step 7 mentions this as an either/or packaging decision but does not include a file-size check as a verification item | Enforced prerequisite lens reveals that while Procedure Step 7 mentions the 15 MB limit as context for packaging options, there is no explicit verification step to check file size compliance before submission; exceeding the limit could cause submission failure | Procedure.md; Specification.md | Procedure: Step 7 Action item 2; Specification: R-001 "Submission" row | -- | RFP Section 4.2 | TBD |
| X-002 | X:judging:necessity | TBD_Question | Procedure | Datasheet | Verify whether the submission deadline "August 30, 2024, 2:00 PM MST" stated in Procedure is correct and consistent with the current RFP timeline; this date is stated only in Procedure and not cross-referenced in Datasheet or Specification | Judgment foundation lens reveals that the submission deadline is a critical scheduling constraint stated in Procedure but not confirmed in any other deliverable document; if the date is incorrect or has changed via addenda, all timeline planning in the Procedure could be invalid | Procedure.md | Procedure: Purpose section "Deadline" statement | -- | RFP submission requirements / Addenda | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification criterion to VER-005 (or new VER-006) confirming that the surety company name is consistent across the executed bond document, DEL-01-06 (Pricing Narrative), and DEL-01-01 (Compliance Matrix); currently VER-005 checks terminology and amounts but does not explicitly verify surety name consistency | Exhaustive verdict lens reveals that while VER-005 checks cross-document consistency for terminology, amounts, and CCIP/OCIP designation, it does not explicitly verify that the surety company name (once known) is consistently stated wherever it appears; surety name inconsistency could signal a compliance defect | Specification.md; Procedure.md | Specification: VER-005 success criteria; Procedure: Step 6 (mentions surety name in compliance matrix entry) | -- | Proposal Manager | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Requirement | 0 | NO_ITEMS | Binding requirements fully enumerated |
| E:normative:sufficiency | normative | sufficiency | Certified Compliance | 0 | NO_ITEMS | Compliance certification pathway clear |
| E:normative:completeness | normative | completeness | Comprehensive Mandate | 0 | NO_ITEMS | Mandate comprehensively documented |
| E:normative:consistency | normative | consistency | Disciplined Mandate | 0 | NO_ITEMS | Mandate discipline maintained |
| E:operative:necessity | operative | necessity | Execution Foundation | 0 | NO_ITEMS | Execution foundation established |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Fitness | 0 | NO_ITEMS | Fitness demonstration covered |
| E:operative:completeness | operative | completeness | Thorough Capability | 0 | NO_ITEMS | Capability coverage thorough |
| E:operative:consistency | operative | consistency | Reliable Practice | 0 | NO_ITEMS | Practice reliability maintained |
| E:evaluative:necessity | evaluative | necessity | Essential Quality | 1 | HAS_ITEMS | Guidance says no contingency uplift but absorb cost |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Merit | 0 | NO_ITEMS | Merit demonstration adequate |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Valuation | 0 | NO_ITEMS | Valuation comprehensive |
| E:evaluative:consistency | evaluative | consistency | Principled Merit | 0 | NO_ITEMS | Merit principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:evaluative:necessity | WeakStatement | Guidance | Guidance | Clarify apparent tension in Guidance C-005: states "Do not apply a contingency uplift to the broker quote in Schedule B -- use the broker's figure directly" but also states "any market-driven cost increase post-award is the Design-Builder's responsibility"; if no contingency is allowed and cost increases are absorbed, the guidance for how to price this risk is ambiguous | Essential quality lens reveals that the instruction to use the broker quote directly without contingency while also absorbing post-award market changes creates a potential logical gap; the proponent has no mechanism to price the absorption risk, which could affect pricing quality and financial security | Guidance.md | Guidance: C-005 paragraphs 2-3 | -- | Commercial Lead | TBD |

---

*End of Semantic Lensing Register*
