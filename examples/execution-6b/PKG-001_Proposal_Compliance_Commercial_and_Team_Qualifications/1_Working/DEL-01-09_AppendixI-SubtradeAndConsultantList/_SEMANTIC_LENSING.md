# Semantic Lensing Register: DEL-01-09 Appendix I -- Subtrade and Consultant List

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-001_Proposal_Compliance_Commercial_and_Team_Qualifications/1_Working/DEL-01-09_AppendixI-SubtradeAndConsultantList
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-01-09 identity, PKG-001, SOW-0007, OBJ-006
- _STATUS.md — Current state SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E parsed (92 cells total)
- Datasheet.md — Identification, Attributes, Conditions, Construction (25 anticipated scope rows), References
- Specification.md — R-01 through R-11, Standards, Verification (8 checks), Documentation, Notes
- Guidance.md — Purpose, Principles P-01 through P-05, Considerations C-01 through C-04, Trade-Offs T-01 through T-03, Examples EX-01 through EX-03
- Procedure.md — Prerequisites (7), Steps 1-7, Verification summary, Records, Notes
- _REFERENCES.md — Cross-references to DEL-01-07, DEL-01-08, DEL-07-03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 5
  - Specification: 6
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 3  B: 3  C: 2  F: 2  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive language on scope row determination |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | R-01 through R-11 cover mandatory practices well |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No verification check for R-05 legal name accuracy method |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Alberta professional registration verification gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 are well-structured |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps provide actionable instructions |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification summary table covers step-level checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA review built into Step 5 and Step 7 |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | P-05 addresses scoring weight alignment |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance EX-01/EX-02 illustrate format merit |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scoring rubric (0-100% x 15 pts) documented |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA sign-off in Step 5/7 addresses quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify R-02 minimum scope coverage -- the ASSUMPTION qualifier weakens what should be a prescriptive minimum list; consider splitting into a confirmed mandatory minimum set and a Proponent-discretionary expansion set | R-02 uses "ASSUMPTION: minimum scope coverage includes..." which makes a mandatory requirement depend on an unconfirmed assumption; evaluators may expect a definitive minimum scope list | Specification.md | R-02 | — | Specification.md is the requirements authority | TBD |
| A-002 | A:normative:judging | VerificationGap | Specification | Specification | Add a verification check for R-05 (legal name accuracy) specifying the method for confirming Alberta corporate registry status (e.g., Alberta Corporate Registry search) | Specification Verification table includes "Legal Name Accuracy" check with "Company names match Alberta corporate registry or equivalent" but no method or tool is specified for how to perform the check; R-05 requires legal names but no verification procedure links to a specific registry lookup method | Specification.md | Verification table, "Legal Name Accuracy" row | — | Specification.md | TBD |
| A-003 | A:normative:reviewing | VerificationGap | Specification | Specification | Add a verification check confirming that all professional consultants listed in Appendix I hold current Alberta registration (P.Eng. via APEGA, B.Arch. via AAA) -- currently implied by Standards table but not explicit in Verification table | Standards table references "Professional Engineers Alberta / Architects Association of Alberta" for professional registration but no corresponding verification check row exists in the Verification table to confirm registration status during QA review | Specification.md | Verification table; Standards table row "Professional Engineers Alberta / Architects Association of Alberta" | — | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing factual field in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes table provides adequate sourced evidence |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet Construction table missing potential scopes |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Source citations are consistently provided |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scoring weight, template format) documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Four documents provide comprehensive coverage |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Purpose section establishes understanding well |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure prerequisites ensure competent assembly |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents collectively provide thorough coverage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T-01 through T-03 provide discernment guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance considerations provide holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-01 through P-05 establish principled reasoning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add an Attribute row for "Submission Deadline" with value "August 30, 2024 at 2:00 PM MST" (RFP section 5.3, p.14) -- this essential fact appears in Procedure.md Notes but not in the Datasheet | The submission deadline is a critical factual parameter for this deliverable; Procedure.md references it (Step 7 verification, Notes) but the Datasheet, which should enumerate key factual attributes, omits it | Datasheet.md; Procedure.md | Datasheet: Attributes table; Procedure: Step 7 verification, Notes | — | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Consider adding anticipated scope rows for Geotechnical Engineering, Building Science / Building Envelope Consultant, and Landscape Architecture if applicable to this project -- these are common DB team disciplines not currently listed in the 25 anticipated rows | Datasheet Construction table lists 25 anticipated scope rows but omits several disciplines commonly present on Design-Build teams for complex facilities (geotechnical, building science/envelope, landscape architecture); these may be relevant given the project includes a high-performance building with energy strategy requirements | Datasheet.md | Construction table (rows 1-25) | — | Datasheet.md | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize scope naming conventions across documents -- Datasheet uses "Mechanical Engineering (HVAC, Plumbing)" while Guidance EX-01 uses "Mechanical Engineering" and Procedure Step 1 uses "Mechanical Engineering"; Guidance P-01 recommends "Mechanical Engineering -- HVAC" style; establish one canonical naming pattern | Scope-of-work naming is inconsistent across documents; this risks drift when populating the actual Appendix I table, as the evaluator sees all three deliverables and inconsistent naming may reduce perceived coherence | Datasheet.md; Guidance.md; Procedure.md | Datasheet: Construction table; Guidance: P-01 Application, EX-01; Procedure: Step 1 Actions item 1 | — | Guidance.md (vocabulary authority) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Conformance | 0 | NO_ITEMS | R-01 through R-11 establish enforceable conformance well |
| C:normative:sufficiency | normative | sufficiency | Validated Threshold | 1 | HAS_ITEMS | Scoring threshold guidance gap |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 0 | NO_ITEMS | Standards table covers applicable regulatory authorities |
| C:normative:consistency | normative | consistency | Harmonized Conformance | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Functional Baseline | 0 | NO_ITEMS | Prerequisites table establishes functional baseline |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Readiness | 0 | NO_ITEMS | Step sequence demonstrates readiness pathway |
| C:operative:completeness | operative | completeness | Comprehensive Process Coverage | 0 | NO_ITEMS | Steps 1-7 cover the full production process |
| C:operative:consistency | operative | consistency | Coordinated Discipline | 0 | NO_ITEMS | Step ownership and verification are coordinated |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth | 0 | NO_ITEMS | 15-point evaluation weight documented |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit | 1 | HAS_ITEMS | No guidance on what distinguishes scoring tiers |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Valuation | 0 | NO_ITEMS | Valuation framework (0-100% x 15 pts) documented |
| C:evaluative:consistency | evaluative | consistency | Principled Integrity | 0 | NO_ITEMS | Principles P-01 through P-05 establish integrity framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | RationaleGap | Guidance | Guidance | Add interpretation guidance for what "Validated Threshold" means in practice for Appendix I -- specifically, what minimum standard of completeness and quality distinguishes an "Acceptable" (60%) from "Very Good" (80%) from "Exceptional" (100%) score under the 15-point criterion | Guidance P-05 references the scoring rubric (0-100% x 15 pts) but does not help the Proponent understand what concrete attributes of Appendix I would move the score between tiers; without this, the 15-point scoring weight is acknowledged but not actionable | Guidance.md | P-05 | — | Guidance.md | TBD |
| C-002 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for how evaluators likely assess "Substantiated Merit" in Appendix I -- e.g., whether the depth of key personnel credentials, geographic proximity of firms, or breadth of specialty coverage is most likely to drive higher scores | The evaluative lens of substantiated merit highlights that while the documents describe the scoring mechanism, they provide no interpretation of what specific content attributes (beyond completeness) drive evaluator judgment for this criterion | Guidance.md | P-05; entire document scanned | — | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Compliance Awareness | 0 | NO_ITEMS | Compliance obligations well documented in Spec Standards table |
| F:normative:sufficiency | normative | sufficiency | Verified Benchmark Attainment | 1 | HAS_ITEMS | Verification gap for R-07 named individuals requirement |
| F:normative:completeness | normative | completeness | Total Compliance Command | 0 | NO_ITEMS | R-01 through R-11 provide comprehensive requirements |
| F:normative:consistency | normative | consistency | Systematic Regulatory Alignment | 0 | NO_ITEMS | Requirements align with RFP and standards systematically |
| F:operative:necessity | operative | necessity | Essential Operational Readiness | 0 | NO_ITEMS | Prerequisites table covers readiness |
| F:operative:sufficiency | operative | sufficiency | Confirmed Execution Capacity | 0 | NO_ITEMS | Steps provide confirmed execution pathway |
| F:operative:completeness | operative | completeness | Thorough Operational Mastery | 1 | HAS_ITEMS | Missing procedural step for handling shared-scope rows |
| F:operative:consistency | operative | consistency | Integrated Procedural Consistency | 0 | NO_ITEMS | Step sequence is internally consistent |
| F:evaluative:necessity | evaluative | necessity | Critical Value Discrimination | 0 | NO_ITEMS | Evaluation criterion documented |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Evaluative Competence | 0 | NO_ITEMS | Guidance provides evaluative framework |
| F:evaluative:completeness | evaluative | completeness | Complete Value Mastery | 0 | NO_ITEMS | Value framework is complete for this deliverable scope |
| F:evaluative:consistency | evaluative | consistency | Principled Evaluative Consistency | 0 | NO_ITEMS | Evaluation principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification check confirming R-07 compliance: that key personnel entries are named individuals (not generic role placeholders) -- the current verification checks address "Column 2 Completeness" (populated fields) but do not specifically verify that entries are named persons vs. role titles | R-07 requires "named individuals -- not generic role placeholders" but the Verification table's "Column 2 Completeness" check only verifies that fields are "populated -- no partially blank rows" without confirming the content is a named person rather than a role title | Specification.md | R-07; Verification table "Column 2 Completeness" row | — | Specification.md | TBD |
| F-002 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add guidance in Step 2 or Step 4 for handling scopes where two firms share responsibility (e.g., joint ventures or split mechanical/electrical) -- Step 2 verification note says "No scope is assigned to two firms without explicit note of shared responsibility" but no procedural action describes how to format this in the two-column template | Step 2 verification includes a check for shared-scope situations but no corresponding procedural action in Step 2 or Step 4 explains how to document shared responsibility in the Appendix I two-column format | Procedure.md | Step 2 Verification; Step 4 Actions | — | Procedure.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Decisive Compliance Mandate | 0 | NO_ITEMS | Compliance mandate is decisively established |
| D:normative:applying | normative | applying | Enforced Standard Practice | 0 | NO_ITEMS | Standard practices enforced through requirements |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 1 | HAS_ITEMS | No final pass/fail criterion defined |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Inspection | 0 | NO_ITEMS | Step 7 sign-off provides regulatory closure |
| D:operative:guiding | operative | guiding | Readiness-Driven Process Command | 0 | NO_ITEMS | Prerequisites and step sequence establish readiness |
| D:operative:applying | operative | applying | Confirmed Capability Deployment | 0 | NO_ITEMS | Steps deploy capability systematically |
| D:operative:judging | operative | judging | Confirmed Performance Attainment | 0 | NO_ITEMS | Step-level verification confirms performance |
| D:operative:reviewing | operative | reviewing | Resolved Process Inspection | 0 | NO_ITEMS | QA review in Step 5 resolves process inspection |
| D:evaluative:guiding | evaluative | guiding | Settled Value Prioritization | 0 | NO_ITEMS | P-05 settles value priority (15-point weight) |
| D:evaluative:applying | evaluative | applying | Enacted Quality Practice | 0 | NO_ITEMS | Quality practices enacted through procedures |
| D:evaluative:judging | evaluative | judging | Definitive Value Fulfillment | 1 | HAS_ITEMS | No self-assessment against scoring rubric |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Assessment | 0 | NO_ITEMS | QA sign-off settles quality assessment |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add a summary pass/fail acceptance criterion to the Verification table that defines the minimum conditions under which Appendix I is considered "complete and compliant" for submission (e.g., all mandatory R-01 through R-11 requirements met, no blank mandatory fields, all cross-references verified) | The Verification table lists individual checks but lacks a conclusive overall conformance verdict -- there is no single criterion or gate that says "Appendix I passes" vs. "Appendix I fails"; this makes the final sign-off in Procedure Step 7 subjective | Specification.md | Verification table (entire section) | — | Specification.md | TBD |
| D-002 | D:evaluative:judging | MissingSlot | Procedure | Procedure | Add a self-assessment step (e.g., in Step 7 or between Step 5 and Step 6) where the Proposal Manager rates the completed Appendix I against the RFP section 8.3 scoring rubric (Unacceptable through Exceptional) to identify improvement opportunities before final submission | The objective of "Definitive Value Fulfillment" highlights that the procedure has no step where the team assesses their own Appendix I against the evaluation rubric before submission; this pre-submission self-check could improve scoring outcomes | Procedure.md | Step 7; Guidance P-05 | — | Procedure.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Directed Essential Enforcement | 0 | NO_ITEMS | Essential enforcement direction is established |
| X:guiding:sufficiency | guiding | sufficiency | Directed Adequacy Confirmation | 0 | NO_ITEMS | Adequacy confirmation directed through verification checks |
| X:guiding:completeness | guiding | completeness | Directed Total Coverage | 1 | HAS_ITEMS | No verification that all Addendum 03 options are addressed |
| X:guiding:consistency | guiding | consistency | Directed Coherent Alignment | 1 | HAS_ITEMS | Cross-document terminology alignment not verified |
| X:applying:necessity | applying | necessity | Mandatory Capability Enactment | 0 | NO_ITEMS | Mandatory capabilities enacted through requirements |
| X:applying:sufficiency | applying | sufficiency | Practiced Standard Delivery | 0 | NO_ITEMS | Standard delivery practices established |
| X:applying:completeness | applying | completeness | Thorough Scope Implementation | 0 | NO_ITEMS | Scope implementation covered by Steps 1-4 |
| X:applying:consistency | applying | consistency | Uniform Coordinated Practice | 0 | NO_ITEMS | Coordination addressed in Steps 2-5 |
| X:judging:necessity | judging | necessity | Decisive Fulfillment Confirmation | 0 | NO_ITEMS | Fulfillment confirmation addressed by verification checks |
| X:judging:sufficiency | judging | sufficiency | Validated Attainment Verdict | 0 | NO_ITEMS | Attainment validated through step verification |
| X:judging:completeness | judging | completeness | Complete Attainment Verdict | 0 | NO_ITEMS | Step 7 sign-off provides completion verdict |
| X:judging:consistency | judging | consistency | Aligned Attainment Verdict | 0 | NO_ITEMS | Cross-reference check in Step 5 provides alignment |
| X:reviewing:necessity | reviewing | necessity | Foundational Compliance Review | 1 | HAS_ITEMS | Datasheet Conditions table has unresolved TBDs |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficiency Verification Review | 0 | NO_ITEMS | Verification checks address sufficiency |
| X:reviewing:completeness | reviewing | completeness | Total Domain Review | 1 | HAS_ITEMS | No verification of DEL-07-03 alignment |
| X:reviewing:consistency | reviewing | consistency | Integrated Alignment Review | 0 | NO_ITEMS | Step 5 cross-check provides alignment review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | WeakStatement | Specification | Specification | Strengthen R-11 to explicitly enumerate which Addendum 03 scopes require unique firm assignment vs. which may be bundled -- currently phrased as "where unique subtrade/specialist assignment is needed" with parenthetical examples, leaving the determination to Proponent judgment without clear criteria | R-11 requires Addendum 03 scopes to be included "where unique subtrade/specialist assignment is needed" but this phrasing is ambiguous -- it does not define what triggers the need for "unique" assignment vs. permissible bundling; this could lead to under-coverage | Specification.md | R-11 | — | Specification.md | TBD |
| X-002 | X:guiding:consistency | Normalization | Multi | Guidance | Establish a canonical term for the deliverable cross-reference set -- documents variously refer to "DEL-01-07" / "Firm Experience" / "Firm Experience Profile" / "Design-Build Firm Experience Profile" and "DEL-01-08" / "Key Team Members" / "Key Personnel Resumes" / "Key Team Members and Resumes"; standardize to one label each | Inconsistent naming of cross-referenced deliverables across all four documents risks confusion during cross-checking and could cause alignment errors in the actual proposal assembly | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Attributes "Cross-References" row; Specification: R-08, R-09; Guidance: P-03; Procedure: Step 5 | — | Guidance.md (vocabulary authority) | TBD |
| X-003 | X:reviewing:necessity | TBD_Question | Datasheet | Datasheet | Resolve Conditions table TBD items: (1) "Subtrade/consultant roster finalized" -- what is the expected timeline for roster finalization relative to proposal deadline? (2) "All trade/discipline scopes defined" -- is there a definitive scope list from the Owner or must it be inferred from OSR? Consult Proposal Manager and Design Lead | Three of seven Conditions in Datasheet are marked TBD; these represent foundational compliance prerequisites that must be resolved before Appendix I can be completed; the documents do not indicate a resolution pathway or owner for these TBDs | Datasheet.md | Conditions table: rows 2, 3, 4 | — | Proposal Manager / Design Lead | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Specification | Specification | Add a verification check for alignment with DEL-07-03 (Subconsultant Approach Narrative) -- R-08 and R-09 require alignment with DEL-01-07 and DEL-01-08 but there is no requirement or verification check for consistency with DEL-07-03, which is listed as a cross-reference in _REFERENCES.md and is mentioned in Guidance C-02 and C-04 | _REFERENCES.md lists DEL-07-03 as a cross-reference; Guidance C-02 says Appendix I should reflect the technical strategy in DEL-01-07 and C-04 notes sub-tier handling may be in DEL-07-03; but Specification has no requirement or verification check for DEL-07-03 consistency | Specification.md; _REFERENCES.md; Guidance.md | Specification: R-08, R-09, Verification table; _REFERENCES.md: Cross-References; Guidance: C-02, C-04 | — | Specification.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Verified Binding Enforcement | 0 | NO_ITEMS | Binding enforcement verified through requirements and checks |
| E:normative:sufficiency | normative | sufficiency | Assured Standard Attainment | 0 | NO_ITEMS | Standard attainment assured through verification table |
| E:normative:completeness | normative | completeness | Confirmed Total Fulfillment | 0 | NO_ITEMS | Total fulfillment pathway established (Steps 1-7 + verification) |
| E:normative:consistency | normative | consistency | Confirmed Regulatory Coherence | 0 | NO_ITEMS | Regulatory coherence confirmed across documents |
| E:operative:necessity | operative | necessity | Verified Operational Deployment | 1 | HAS_ITEMS | Datasheet missing operational parameter |
| E:operative:sufficiency | operative | sufficiency | Validated Operational Adequacy | 0 | NO_ITEMS | Operational adequacy validated through step verification |
| E:operative:completeness | operative | completeness | Complete Operational Delivery | 0 | NO_ITEMS | Steps 1-7 provide complete delivery pathway |
| E:operative:consistency | operative | consistency | Verified Process Integration | 0 | NO_ITEMS | Process integration verified through cross-checks |
| E:evaluative:necessity | evaluative | necessity | Essential Quality Standard | 0 | NO_ITEMS | Quality standard established through P-01 through P-05 |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Sufficiency | 0 | NO_ITEMS | Value sufficiency substantiated through scoring documentation |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Value Fulfillment | 1 | HAS_ITEMS | Missing evaluative consideration |
| E:evaluative:consistency | evaluative | consistency | Integrated Quality Judgment | 0 | NO_ITEMS | Quality judgment framework is integrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | MissingSlot | Datasheet | Datasheet | Add an Attribute row for "Estimated Row Count" or "Minimum Expected Rows" to the Datasheet Attributes table -- the Construction table shows 25 anticipated rows but this parameter is not surfaced as a tracked attribute | The Datasheet Attributes table captures key parameters (format, template columns, scoring weight, constraints) but does not include the anticipated scope count as a tracked attribute; this operational parameter is important for planning and completeness verification | Datasheet.md | Attributes table; Construction table | — | Datasheet.md | TBD |
| E-002 | E:evaluative:completeness | WeakStatement | Guidance | Guidance | Add a consideration addressing how the Proponent should handle the case where a firm covers multiple scopes -- P-01 says "use separate rows -- one row per scope assignment" but does not address whether repeating the same firm across many rows could be perceived negatively by evaluators (suggesting over-reliance on a single firm) | Guidance P-01 provides clear direction to use separate rows per scope but does not address the evaluative implication of a single firm appearing in many rows, which could signal either efficiency or over-concentration; this gap could affect scoring under the 15-point team evaluation criterion | Guidance.md | P-01 Application | — | Guidance.md | TBD |
