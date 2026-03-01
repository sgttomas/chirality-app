# Semantic Lensing Register: DEL-021-02 Performance & Payment Bonds

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-021_Bonding, Insurance & Warranty/1_Working/DEL-021-02_Performance-Bonds
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-021-02_Performance-Bonds/_CONTEXT.md (Deliverable Overview, Scope Definition, Success Criteria)
- _STATUS.md — DEL-021-02_Performance-Bonds/_STATUS.md (Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-021-02_Performance-Bonds/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-021-02_Performance-Bonds/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-021-02_Performance-Bonds/Specification.md (Scope, Requirements REQ-021-02-001 through -007, Standards, Verification, Documentation)
- Guidance.md — DEL-021-02_Performance-Bonds/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-021-02_Performance-Bonds/Procedure.md (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md — DEL-021-02_Performance-Bonds/_REFERENCES.md (Primary References, Related Documentation, SOW Items)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 4  B: 2  C: 3  F: 3  D: 3  X: 2  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Bond duration not prescribed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Bond form standard assumption |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta surety legislation gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers regulatory audit adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-6 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Escalation/contingency missing |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure verification table covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value orientation clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Bond premium cost mentioned in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Not salient; bonds are mandatory not discretionary |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Not salient for mandatory instruments |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Datasheet | Specification | Add explicit requirement or datasheet entry for bond duration/expiry period; currently marked as ASSUMPTION with no governing source cited | Datasheet Conditions states bond duration is an ASSUMPTION; no normative requirement specifies bond term length or expiry, creating ambiguity about when obligations terminate | Datasheet.md | Conditions (Duration row) | -- | PROPOSAL: Confirm with Owner per RFP full text or CCDC 14-2013 | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-021-02-005 to specify which bond form standard is required rather than relying on assumption that CCDC A312 is acceptable | Bond form is stated as "forms acceptable to Owner" but the specific standard form is marked ASSUMPTION in both Specification Standards table and Datasheet Construction table; this could lead to form rejection at execution | Specification.md | Standards (CCDC A312 rows); REQ-021-02-005 | -- | PROPOSAL: Owner confirmation required before bond execution | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Identify the specific Alberta statute governing surety company licensing (e.g., Alberta Insurance Act) and record it as a standard | The Standards table references "Alberta Surety Legislation" with "specific act not cited in accessible sources"; compliance determination requires knowing which statute applies | Specification.md | Standards (Alberta Surety Legislation row) | -- | PROPOSAL: Consult Alberta Insurance Council or legal counsel | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add contingency/escalation step if surety cannot issue bonds within the 10-day timeline (e.g., alternative surety engagement, Owner notification of delay) | Procedure covers the happy path but does not address what happens if a step fails or timeline is at risk; practical execution requires contingency planning given the tight 10-day window | Procedure.md | Steps (between Step 4 and Step 5) | -- | PROPOSAL: Project Manager discretion | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | RFP section reference inconsistency |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence with source citations |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet covers all key bond parameters |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | RFP section numbering inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Award notification trigger is clearly identified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context across documents is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are coherent across the set |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles provide fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents presume competent personnel |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Not salient; documents are appropriate for P1 stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section covers key judgment calls |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance Considerations section provides holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | Normalization | Datasheet | Multi | Normalize RFP section reference: Datasheet Identification table cites "RFP S2.12" for Regulatory Basis while _CONTEXT.md cites "RFP S2.10"; confirm which RFP section number is authoritative | Essential facts must be accurate; the RFP section number for bonding requirements is cited as S2.12 in production documents but S2.10 in _CONTEXT.md, creating a potential traceability error | Datasheet.md, _CONTEXT.md | Datasheet: Identification (Regulatory Basis); _CONTEXT.md: Regulatory Context | Datasheet.md#Identification (S2.12), _CONTEXT.md#Regulatory Context (S2.10) | PROPOSAL: RFP full text is authoritative; production documents appear to use S2.12 consistently | TBD |
| B-002 | B:data:consistency | Normalization | Multi | Multi | Standardize RFP section citation format: Datasheet uses "RFP S2.12.1.1" while _CONTEXT.md uses "Main RFP S2.10"; ensure all documents use the same section numbering for bonding requirements | Reliable measurement requires consistent identifiers; the discrepancy between S2.10 and S2.12 across _CONTEXT.md and production documents risks citation errors in future references | _CONTEXT.md, Datasheet.md, Specification.md | _CONTEXT.md: Regulatory Context; Datasheet.md: entire document; Specification.md: entire document | _CONTEXT.md#Regulatory Context (S2.10), Datasheet.md#Identification (S2.12) | PROPOSAL: Verify against RFP table of contents and normalize | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Mandate | 0 | NO_ITEMS | Requirements REQ-021-02-001 through -007 cover compulsory mandates |
| C:normative:sufficiency | normative | sufficiency | Certified Threshold Validation | 1 | HAS_ITEMS | Threshold for surety certification not specified |
| C:normative:completeness | normative | completeness | Comprehensive Statutory Coverage | 1 | HAS_ITEMS | Missing CCDC 14-2013 text |
| C:normative:consistency | normative | consistency | Uniform Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Functional Activation | 0 | NO_ITEMS | Award notification trigger is clearly defined |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Capability | 0 | NO_ITEMS | Roles and responsibilities are defined |
| C:operative:completeness | operative | completeness | Exhaustive Process Delivery | 1 | HAS_ITEMS | No Owner rejection handling |
| C:operative:consistency | operative | consistency | Predictable Systematic Execution | 0 | NO_ITEMS | Procedure steps are sequenced and consistent |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Benchmark | 0 | NO_ITEMS | Bond amounts established at 50% benchmarks |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Expert Appraisal | 0 | NO_ITEMS | Trade-offs table provides expert assessment framing |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Accounting | 0 | NO_ITEMS | Insurance vs. bonding distinction covered |
| C:evaluative:consistency | evaluative | consistency | Calibrated Worth Assurance | 0 | NO_ITEMS | Bond amounts consistently stated at 50% |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification criterion for surety company financial capacity/rating (e.g., minimum A.M. Best rating or equivalent); currently only Alberta licensing is verified | Certified threshold validation requires that the surety not only be licensed but also financially capable of backing the bond; no financial strength threshold is specified or verified | Specification.md | Verification (REQ-021-02-004 row); Standards table | -- | PROPOSAL: Industry practice suggests A.M. Best A- rating minimum; confirm with Owner | TBD |
| C-002 | C:normative:completeness | TBD_Question | Specification | Specification | Obtain and review CCDC 14-2013 contract form and associated standard bond forms to confirm compatibility requirements; record specific clause references | Comprehensive statutory coverage requires access to CCDC 14-2013 text, which is cited as a standard but marked "full text not in accessible sources"; bond form compatibility cannot be fully verified without it | Specification.md | Standards (CCDC 14-2013 row) | -- | PROPOSAL: Obtain CCDC 14-2013 from Canadian Construction Documents Committee | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add step or sub-step addressing what happens if Owner rejects the proposed bond form (per Step 3 confirmation); include re-engagement with surety and revised timeline assessment | Exhaustive process delivery requires handling the case where Owner does not accept the proposed bond form; the current procedure assumes acceptance | Procedure.md | Step 3 (Confirm Surety Company and Bond Form) | -- | PROPOSAL: Project Manager discretion | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Statutory Obligation | 1 | HAS_ITEMS | Timing conflict between RFP sections |
| F:normative:sufficiency | normative | sufficiency | Qualified Conformance Standard | 0 | NO_ITEMS | Conformance standards are defined with appropriate TBD markers |
| F:normative:completeness | normative | completeness | Total Prescriptive Authority | 0 | NO_ITEMS | Requirements are comprehensive for accessible source material |
| F:normative:consistency | normative | consistency | Rigorous Statutory Alignment | 1 | HAS_ITEMS | Verification evidence gap |
| F:operative:necessity | operative | necessity | Proven Operational Imperative | 0 | NO_ITEMS | Operational triggers and imperatives are clear |
| F:operative:sufficiency | operative | sufficiency | Verified Procedural Readiness | 0 | NO_ITEMS | Prerequisites table defines readiness criteria |
| F:operative:completeness | operative | completeness | Exhaustive Fulfillment Record | 1 | HAS_ITEMS | Distribution list incomplete |
| F:operative:consistency | operative | consistency | Disciplined Performance Fidelity | 0 | NO_ITEMS | Procedure and Specification verification tables are aligned |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Determination | 0 | NO_ITEMS | Bond value determination is formula-based (50% of contract) |
| F:evaluative:sufficiency | evaluative | sufficiency | Equitable Valuation Standard | 0 | NO_ITEMS | 50% threshold from RFP is clear |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Assessment Authority | 0 | NO_ITEMS | Not salient; bond amounts are prescribed not assessed |
| F:evaluative:consistency | evaluative | consistency | Principled Assessment Integrity | 0 | NO_ITEMS | Valuation methodology is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Conflict | Specification | Guidance | Resolve timing interpretation: REQ-021-02-003 (10 days from award) vs. REQ-021-02-007 (concurrent with contract execution) -- clarify whether these are complementary or potentially conflicting deadlines | This is the same conflict identified in Guidance CON-021-02-01; the absolute statutory obligation lens confirms this is a material conflict requiring human ruling on sequencing | Specification.md, Guidance.md | Specification: REQ-021-02-003, REQ-021-02-007; Guidance: Conflict Table CON-021-02-01 | Specification.md#REQ-021-02-003 (10-day outer deadline), Specification.md#REQ-021-02-007 (concurrent with contract execution) | PROPOSAL: Per Guidance CON-021-02-01 proposed reading -- 10-day clock governs, aim for bonds ready before signing | TBD |
| F-002 | F:normative:consistency | VerificationGap | Specification | Specification | Add verification evidence for REQ-021-02-005 (bond form acceptability): specify what constitutes "written acceptance" (email, letter, countersignature) and at what point in the process it must be obtained | Rigorous statutory alignment requires that verification evidence be unambiguous; current verification says "Owner written acceptance or countersignature" but does not specify acceptable format or timing relative to bond execution | Specification.md | Verification (REQ-021-02-005 row) | -- | PROPOSAL: Define in Specification or Procedure Step 3 | TBD |
| F-003 | F:operative:completeness | WeakStatement | Specification | Specification | Clarify document distribution requirements in Documentation section: "ASSUMPTION" label on distribution scope weakens the fulfillment record; specify minimum distribution (Owner, Proponent file, Architect if required) | The Document Distribution paragraph is prefaced with "ASSUMPTION" and states distribution requirements are "not explicitly stated in accessible RFP text"; this leaves fulfillment record incomplete | Specification.md | Documentation (Document Distribution) | -- | PROPOSAL: Confirm distribution list with Owner | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Prescriptive Duty | 0 | NO_ITEMS | Prescriptive duties are well-defined in Specification |
| D:normative:applying | normative | applying | Compulsory Conformance Target | 1 | HAS_ITEMS | Pass/fail criteria for bond amounts |
| D:normative:judging | normative | judging | Binding Jurisdictional Ruling | 0 | NO_ITEMS | Alberta jurisdiction clearly stated |
| D:normative:reviewing | normative | reviewing | Confirmed Compliance Inspection | 0 | NO_ITEMS | Verification table maps to each requirement |
| D:operative:guiding | operative | guiding | Established Workflow Counsel | 0 | NO_ITEMS | Guidance Principles provide workflow counsel |
| D:operative:applying | operative | applying | Confirmed Delivery Readiness | 1 | HAS_ITEMS | Pre-award readiness checklist |
| D:operative:judging | operative | judging | Finalized Capability Review | 0 | NO_ITEMS | Procedure Verification table covers capability |
| D:operative:reviewing | operative | reviewing | Systematic Dependability Verification | 0 | NO_ITEMS | Records section supports systematic verification |
| D:evaluative:guiding | evaluative | guiding | Established Significance Basis | 0 | NO_ITEMS | Purpose section establishes significance |
| D:evaluative:applying | evaluative | applying | Confirmed Value Delivery | 0 | NO_ITEMS | Not salient; bonds are mandatory |
| D:evaluative:judging | evaluative | judging | Definitive Holistic Verdict | 1 | HAS_ITEMS | Success criteria cross-reference |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Excellence Scrutiny | 0 | NO_ITEMS | Not salient for compliance-driven deliverable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add explicit pass/fail acceptance criterion for bond amount tolerance: specify whether bond face amount must be exactly 50% or whether rounding conventions apply (e.g., to nearest dollar, hundred, thousand) | Compulsory conformance target requires precision; REQ-021-02-006 states "50% of Contract price" but verification says "confirm face amount equals 50%" without addressing rounding or tolerance for the calculated amount | Specification.md | Verification (REQ-021-02-006 row); REQ-021-02-006 | -- | PROPOSAL: Typically exact to the dollar; confirm with surety practice | TBD |
| D-002 | D:operative:applying | MissingSlot | Guidance | Guidance | Add a pre-award readiness checklist in Guidance Considerations that consolidates the preparation actions mentioned across documents (surety pre-qualification, Consent of Surety status, draft bond form review, estimated contract price) into a single actionable list | Confirmed delivery readiness requires a consolidated view of pre-award preparations; these are mentioned in Guidance Considerations and Procedure Prerequisites but not assembled into one ready-reference | Guidance.md | Considerations (Timeline Compression Risk) | -- | PROPOSAL: Guidance is the natural home for a readiness checklist | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add explicit cross-reference from Guidance to _CONTEXT.md Success Criteria, mapping each criterion to the verification approach that satisfies it | Definitive holistic verdict requires connecting Success Criteria from _CONTEXT.md to verification in Specification; currently Success Criteria are stated in _CONTEXT.md but not referenced in any production document | Guidance.md, _CONTEXT.md | Guidance: entire document scanned; _CONTEXT.md: Success Criteria | -- | PROPOSAL: Guidance is appropriate for traceability rationale | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Anchored Instructional Imperative | 0 | NO_ITEMS | Guidance Principles section provides anchored imperatives |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Framework | 0 | NO_ITEMS | Guidance trade-offs and considerations justify direction |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Authority | 0 | NO_ITEMS | Guidance covers all major decision points |
| X:guiding:consistency | guiding | consistency | Coherent Prescriptive Fidelity | 0 | NO_ITEMS | Guidance is consistent with Specification and Procedure |
| X:applying:necessity | applying | necessity | Obligatory Preparedness Reality | 1 | HAS_ITEMS | Surety pre-engagement confirmation |
| X:applying:sufficiency | applying | sufficiency | Competent Conformance Delivery | 0 | NO_ITEMS | Procedure provides sufficient detail |
| X:applying:completeness | applying | completeness | Comprehensive Delivery Assurance | 0 | NO_ITEMS | Procedure Steps 1-6 cover delivery comprehensively |
| X:applying:consistency | applying | consistency | Stable Conformance Assurance | 0 | NO_ITEMS | Procedure is consistent with Specification requirements |
| X:judging:necessity | judging | necessity | Binding Adjudication Standard | 0 | NO_ITEMS | Verification table maps each requirement to evidence |
| X:judging:sufficiency | judging | sufficiency | Justified Conclusive Assessment | 0 | NO_ITEMS | Evidence types are specified in Verification table |
| X:judging:completeness | judging | completeness | Total Adjudication Record | 0 | NO_ITEMS | All 7 requirements have verification entries |
| X:judging:consistency | judging | consistency | Coherent Adjudication Fidelity | 0 | NO_ITEMS | Verification criteria are consistent with requirements |
| X:reviewing:necessity | reviewing | necessity | Critical Dependability Assurance | 1 | HAS_ITEMS | Bond maintenance/renewal gap |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Dependability Evidence | 0 | NO_ITEMS | Records section defines retention artifacts |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Compliance Authority | 0 | NO_ITEMS | Records section is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Stable Compliance Coherence | 0 | NO_ITEMS | Records align with Specification Documentation |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | WeakStatement | Procedure | Procedure | Strengthen Procedure Prerequisites: DEL-021-01 (Bid Security) status is "ASSUMPTION: Complete prior to award; confirm surety is still engaged" -- replace ASSUMPTION with an explicit verification check or gate (e.g., "Verify surety Consent of Surety letter is on file and surety confirms continued engagement") | Obligatory preparedness reality requires confirmed upstream dependency status, not assumed status; if the surety relationship has lapsed between bid and award, the 10-day timeline is at risk | Procedure.md | Prerequisites (DEL-021-01 row) | -- | PROPOSAL: Project Manager to verify at award notification | TBD |
| X-002 | X:reviewing:necessity | RationaleGap | Datasheet | Guidance | Add rationale in Guidance for bond maintenance obligations during construction: Datasheet Conditions states bond duration is an ASSUMPTION; Guidance should explain what happens if bonds expire or need renewal during construction, and who monitors this | Critical dependability assurance requires ongoing bond validity; the documents address procurement and initial delivery but do not address post-delivery bond maintenance, renewal, or monitoring responsibilities | Datasheet.md, Guidance.md | Datasheet: Conditions (Duration row); Guidance: entire document scanned | -- | PROPOSAL: Confirm bond duration requirements with CCDC 14-2013 and Owner | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Record | 0 | NO_ITEMS | Directive data is recorded with source citations |
| E:guiding:information | guiding | information | Coherent Advisory Orientation | 0 | NO_ITEMS | Guidance provides coherent advisory information |
| E:guiding:knowledge | guiding | knowledge | Expert Mentorship Command | 0 | NO_ITEMS | Guidance Principles demonstrate domain expertise |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 0 | NO_ITEMS | Trade-offs and Conflict Table demonstrate foresight |
| E:applying:data | applying | data | Verified Delivery Evidence | 1 | HAS_ITEMS | Surety company identity TBD |
| E:applying:information | applying | information | Transparent Fulfillment Context | 0 | NO_ITEMS | Fulfillment context is transparent |
| E:applying:knowledge | applying | knowledge | Proficient Delivery Mastery | 0 | NO_ITEMS | Procedure demonstrates delivery proficiency |
| E:applying:wisdom | applying | wisdom | Judicious Delivery Foresight | 0 | NO_ITEMS | Guidance Considerations section shows foresight |
| E:judging:data | judging | data | Binding Evidentiary Verdict | 0 | NO_ITEMS | Verification evidence types are specified |
| E:judging:information | judging | information | Transparent Adjudication Account | 0 | NO_ITEMS | Verification approach is transparent |
| E:judging:knowledge | judging | knowledge | Authoritative Ruling Mastery | 0 | NO_ITEMS | Not salient; compliance is binary for this deliverable |
| E:judging:wisdom | judging | wisdom | Sage Adjudication Foresight | 0 | NO_ITEMS | Conflict table shows adjudication foresight |
| E:reviewing:data | reviewing | data | Verified Compliance Record | 1 | HAS_ITEMS | Bond number/tracking fields |
| E:reviewing:information | reviewing | information | Transparent Compliance Narrative | 0 | NO_ITEMS | Records section creates compliance narrative trail |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Compliance Mastery | 0 | NO_ITEMS | Not salient for P1 stage |
| E:reviewing:wisdom | reviewing | wisdom | Principled Compliance Foresight | 0 | NO_ITEMS | Not salient for P1 stage |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | TBD_Question | Datasheet | Datasheet | Record whether the surety company used for Consent of Surety at bid (DEL-021-01) is confirmed as the intended surety for performance/payment bonds; add a Datasheet attribute row for "Intended Surety Company" with value "TBD -- same as bid bond surety per Guidance Principle 2" | Verified delivery evidence requires knowing the intended surety; Datasheet lists "Surety Company Identity: TBD" without linking to the upstream surety relationship from DEL-021-01 | Datasheet.md | Attributes (Surety Company Identity row) | -- | PROPOSAL: Confirm upon award notification | TBD |
| E-002 | E:reviewing:data | MissingSlot | Datasheet | Datasheet | Add bond number fields to Datasheet Attributes (Performance Bond Number: TBD, Payment Bond Number: TBD) as tracking identifiers for the compliance record | Verified compliance record requires unique instrument identifiers; Procedure Records mentions "bond numbers" in the Contract Register Entry but Datasheet does not include bond number fields as attributes | Datasheet.md, Procedure.md | Datasheet: Attributes (no bond number row); Procedure: Records (Contract Register Entry) | -- | PROPOSAL: Datasheet is the natural home for instrument identifiers | TBD |
