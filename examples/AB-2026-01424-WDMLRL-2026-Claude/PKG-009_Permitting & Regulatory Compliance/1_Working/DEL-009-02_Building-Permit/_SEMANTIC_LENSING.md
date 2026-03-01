# Semantic Lensing Register: DEL-009-02 Building Permit Application & Approval

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-02_Building-Permit/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-009-02_Building-Permit/_CONTEXT.md (Deliverable Identity, Business Objective, Scope, Stakeholder Engagement, Success Criteria)
- _STATUS.md -- DEL-009-02_Building-Permit/_STATUS.md (Current Status: SEMANTIC_READY, Change Log)
- _SEMANTIC.md -- DEL-009-02_Building-Permit/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md -- DEL-009-02_Building-Permit/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md -- DEL-009-02_Building-Permit/Specification.md (Scope, Requirements REQ-009-02-01 through REQ-009-02-11, Standards, Verification, Documentation)
- Guidance.md -- DEL-009-02_Building-Permit/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md -- DEL-009-02_Building-Permit/Procedure.md (Prerequisites, Steps Phases 1-5, Verification, Records)
- _REFERENCES.md -- DEL-009-02_Building-Permit/_REFERENCES.md (Primary References, Regulatory References, Internal Project References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific Alberta code identifiers TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Safety Code permit coordination unclear |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach for code compliance relies on permit issuance as proxy |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection audit provisions well covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure phases are well structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Pre-application consultation step lacks acceptance criteria |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers execution checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure adequately tracks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Schedule value trade-off missing quantification |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Success criteria in _CONTEXT adequately address worth |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality review covered by internal review step |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: Identify specific Alberta Safety Codes Act citation (RSA 2000, c S-1), Alberta Building Code edition, and Camrose County Land Use Bylaw number applicable to this permit | The prescriptive direction lens reveals that the normative codes governing this permit are cited generically ("all applicable Alberta building codes") without specific act/edition/bylaw identifiers. Datasheet lists "TBD" for specific Alberta codes; Specification Standards table marks editions as assumptions. | Datasheet.md; Specification.md | Datasheet.md#Attributes ("Specific Alberta code(s)"); Specification.md#Standards | -- | Camrose County building authority; Alberta Municipal Affairs | TBD |
| A-002 | A:normative:applying | Conflict | Multi | TBD | Clarify whether building permit and Safety Code permits (DEL-009-03) are submitted together or separately to Camrose County, and document the coordination protocol | Under the mandatory practice lens, the coordination between DEL-009-02 and DEL-009-03 is unresolved. The Guidance Conflict Table (CONF-009-02-01) already flags this but it remains TBD. The Specification treats them as distinct (REQ-009-02-01 vs DEL-009-03 in Out of Scope), while the Procedure Step 2 instructs clarification but has no resolution pathway. | Guidance.md; Specification.md; Procedure.md | Guidance.md#Conflict Table (CONF-009-02-01); Specification.md#Out of Scope; Procedure.md#Phase 1 Step 2 | Guidance.md#Conflict Table; Specification.md#Out of Scope | Camrose County building authority | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen verification approach for REQ-009-02-04 and REQ-009-02-05 beyond "verify by permit issuance" -- add explicit pre-submission code compliance review criteria | The compliance determination lens highlights that the verification approach for code compliance requirements (REQ-009-02-04, REQ-009-02-05) relies primarily on "permit issuance" as a proxy for compliance. This is circular -- the permit authority's acceptance is treated as the verification, but no independent pre-submission compliance check is specified. | Specification.md | Specification.md#Verification (REQ-009-02-04, REQ-009-02-05) | -- | Project Manager | TBD |
| A-004 | A:operative:applying | VerificationGap | Procedure | Specification | Add acceptance criteria for Step 2 (pre-application engagement) outputs -- define what constitutes a complete set of authority requirements before proceeding to Phase 2 | Under practical execution, Step 2 lists items to confirm with the building authority but has no defined acceptance criteria for when the engagement is "complete enough" to proceed. The go/no-go between Phase 1 and Phase 2 is undefined. | Procedure.md | Procedure.md#Phase 1 Step 2 | -- | Project Manager | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for the schedule impact of building authority processing time -- quantify or bracket the expected review duration and its effect on the December 2026 deadline | The value orientation lens reveals that the critical-path schedule risk is discussed qualitatively in Guidance Considerations, but no quantified or bracketed processing timeline is provided. The Datasheet records processing timeline as "TBD." Without this, the Project Manager cannot evaluate the actual schedule risk magnitude. | Guidance.md; Datasheet.md | Guidance.md#Considerations ("Schedule Risk: Critical Path Position"); Datasheet.md#Attributes ("Processing timeline") | -- | Camrose County building authority; Project Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Application forms TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | IFC drawing requirements well specified |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Accessibility and fire safety standards not enumerated |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Source references consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Dependency signals well documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for current stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All known information accounted for |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Status field inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Alberta Safety Codes framework explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement established |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge gaps flagged as TBDs appropriately |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table provides discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Recommendations in trade-offs are reasoned |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance considerations provide holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain Camrose County building permit application form(s) and submission checklist; record form identifiers in Datasheet Attributes | The essential fact lens reveals that the application form identifiers are recorded as "TBD" in the Datasheet. These are essential facts needed to assemble the application package. Procedure Step 2 instructs obtaining them but they remain unrecorded data items. | Datasheet.md; Procedure.md | Datasheet.md#Attributes ("Application form(s)"); Procedure.md#Phase 1 Step 2 | -- | Camrose County building authority | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Add entries for accessibility standards and fire safety requirements to the Standards table, even if as TBD placeholders | The comprehensive record lens reveals that the Standards table in the Specification lists Alberta Building Code and Safety Codes Act generically, but does not enumerate accessibility standards or fire safety requirements separately. _REFERENCES.md lists these as "TBD" under External Standards, confirming the gap. For a 13,000 sq ft commercial structure, these are reasonably expected standard categories. | Specification.md; _REFERENCES.md | Specification.md#Standards; _REFERENCES.md#External Standards | -- | Building authority; Design Team | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Datasheet | Align Datasheet "Current Status" field (shows "OPEN") with _STATUS.md (shows "SEMANTIC_READY") | The coherent message lens reveals a status inconsistency: Datasheet Identification table states "Current Status: OPEN" while _STATUS.md records "SEMANTIC_READY" as of 2026-02-26. This creates a misleading signal about deliverable progress. | Datasheet.md; _STATUS.md | Datasheet.md#Identification ("Current Status"); _STATUS.md#Current Status | Datasheet.md#Identification; _STATUS.md#Current Status | -- | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Obligation | 1 | HAS_ITEMS | Priority field missing on some requirements |
| C:normative:sufficiency | normative | sufficiency | Threshold Acceptance Criteria | 1 | HAS_ITEMS | Acceptance criteria for drawing completeness underspecified |
| C:normative:completeness | normative | completeness | Total Prescriptive Coverage | 0 | NO_ITEMS | Requirements cover the full permit lifecycle |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Requirements are internally coherent |
| C:operative:necessity | operative | necessity | Core Functional Imperative | 0 | NO_ITEMS | Core workflow well established in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Readiness | 0 | NO_ITEMS | Prerequisites table in Procedure covers readiness |
| C:operative:completeness | operative | completeness | Total Execution Breadth | 0 | NO_ITEMS | All phases covered from pre-application through inspection |
| C:operative:consistency | operative | consistency | Disciplined Execution Stability | 0 | NO_ITEMS | Step sequencing is consistent and stable |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Imperative | 0 | NO_ITEMS | Value proposition clear (regulatory gate) |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Basis | 0 | NO_ITEMS | Merit basis established through RFP linkage |
| C:evaluative:completeness | evaluative | completeness | Integral Worth Accounting | 1 | HAS_ITEMS | Cost impact of permit conditions not addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Assessment Alignment | 0 | NO_ITEMS | Assessment criteria aligned across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Normalization | Specification | Specification | Add explicit "Priority: Mandatory" field to REQ-009-02-07 (currently missing Priority field) for consistency with other requirements | Under the Compulsory Regulatory Obligation lens, REQ-009-02-07 (County Representative at Inspections) lacks a "Priority" field while all other requirements include one. This inconsistency in the normative register could lead to ambiguity about whether this requirement is mandatory or advisory. | Specification.md | Specification.md#Requirements (REQ-009-02-07) | -- | -- | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Specification | Specification | Clarify what constitutes "complete IFC drawings" in REQ-009-02-03 -- enumerate the required design disciplines explicitly in the requirement statement or add a cross-reference to the Datasheet discipline list | The Threshold Acceptance Criteria lens reveals that REQ-009-02-03 states "covering all required design disciplines" without enumerating them. The Procedure Step 4 lists specific disciplines (architectural, structural, mechanical/HVAC, electrical, civil/site grading, plumbing) but the requirement itself uses weak phrasing. This could lead to disputes about completeness. | Specification.md; Procedure.md | Specification.md#Requirements (REQ-009-02-03); Procedure.md#Phase 2 Step 4 | -- | Project Manager | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a consideration addressing the potential cost and schedule impact of permit conditions on the construction program -- currently the worth accounting of permit conditions stops at documentation | The Integral Worth Accounting lens reveals that Guidance Principle 5 notes permit conditions "may affect materials, sequencing, or inspection hold points" but does not address the cost or schedule impact evaluation of those conditions. The completeness of worth accounting requires acknowledging that permit conditions may have financial and timeline consequences beyond documentation. | Guidance.md | Guidance.md#Principles (Principle 5); Guidance.md#Considerations | -- | Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Obligatory Mandate | 0 | NO_ITEMS | Core permit obligation well established |
| F:normative:sufficiency | normative | sufficiency | Qualified Compliance Basis | 1 | HAS_ITEMS | Compliance basis for Alberta codes rests on assumptions |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Register | 1 | HAS_ITEMS | No environmental or heritage overlay check |
| F:normative:consistency | normative | consistency | Systematic Compliance Uniformity | 0 | NO_ITEMS | Compliance approach consistent |
| F:operative:necessity | operative | necessity | Essential Delivery Prerequisite | 0 | NO_ITEMS | Prerequisites well documented |
| F:operative:sufficiency | operative | sufficiency | Proven Delivery Competence | 0 | NO_ITEMS | Competence assumptions reasonable at this stage |
| F:operative:completeness | operative | completeness | Complete Operational Archive | 0 | NO_ITEMS | Records table comprehensive |
| F:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Process steps are disciplined and sequenced |
| F:evaluative:necessity | evaluative | necessity | Indispensable Worth Criterion | 0 | NO_ITEMS | Construction gate criterion clear |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Fitness Appraisal | 1 | HAS_ITEMS | No fitness check for resubmission scenario |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Scope | 0 | NO_ITEMS | Valuation scope adequate for permit deliverable |
| F:evaluative:consistency | evaluative | consistency | Integrated Appraisal Coherence | 0 | NO_ITEMS | Appraisal criteria consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen the Standards table entries for Alberta Safety Codes Act and Alberta Building Code by removing "ASSUMPTION" qualifier once actual edition/citation is confirmed, or explicitly flag as blocking TBD | The Qualified Compliance Basis lens reveals that the Standards table uses "ASSUMPTION: likely applicable; location TBD" for the two primary governing codes. This weakens the compliance basis -- the deliverable claims compliance with codes whose specific text and edition are not confirmed. | Specification.md | Specification.md#Standards | -- | Camrose County building authority; Alberta Municipal Affairs | TBD |
| F-002 | F:normative:completeness | TBD_Question | Multi | Specification | Record TBD: Confirm whether environmental assessment, heritage overlay, or other municipal/provincial regulatory overlays apply to this site and building permit application | The Exhaustive Regulatory Register lens reveals that the Standards table and Conditions do not address whether environmental or heritage overlays apply to the Camrose County site. For a new 13,000 sq ft structure on County land, additional regulatory checks (wetland, environmental, heritage) may apply. _REFERENCES.md lists "Accessibility standards: TBD" and "Fire safety requirements: TBD" but does not mention environmental/heritage. | Specification.md; Datasheet.md; _REFERENCES.md | Specification.md#Standards; Datasheet.md#Conditions; _REFERENCES.md#External Standards | -- | Camrose County planning department; Alberta Environment | TBD |
| F-003 | F:evaluative:sufficiency | MissingSlot | Procedure | Procedure | Add a contingency step or branch in Phase 3 for the scenario where the building authority rejects the application or requests major revisions -- define the re-submission workflow and responsible parties | The Justified Fitness Appraisal lens reveals that Procedure Step 9 addresses "requests for additional information" but does not define a workflow for outright rejection or major revision requests. The fitness appraisal of the process is incomplete without a defined re-submission path, which is a reasonably expected scenario for a complex permit application. | Procedure.md | Procedure.md#Phase 3 Step 9 | -- | Project Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Authoritative Charge | 0 | NO_ITEMS | Authoritative charge clear (permit obligation from RFP) |
| D:normative:applying | normative | applying | Resolved Obligatory Performance | 0 | NO_ITEMS | Obligatory performance requirements resolved |
| D:normative:judging | normative | judging | Definitive Regulatory Ruling | 0 | NO_ITEMS | Ruling mechanism (permit issuance) defined |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Examination | 1 | HAS_ITEMS | Inspection stages not enumerated |
| D:operative:guiding | operative | guiding | Resolved Procedural Stewardship | 0 | NO_ITEMS | Procedure provides clear stewardship direction |
| D:operative:applying | operative | applying | Resolved Capable Delivery | 0 | NO_ITEMS | Delivery capability addressed through prerequisites |
| D:operative:judging | operative | judging | Definitive Performance Finding | 0 | NO_ITEMS | Performance verification defined |
| D:operative:reviewing | operative | reviewing | Resolved Systematic Scrutiny | 0 | NO_ITEMS | Process review covered by verification table |
| D:evaluative:guiding | evaluative | guiding | Resolved Principled Direction | 0 | NO_ITEMS | Principles clearly articulated in Guidance |
| D:evaluative:applying | evaluative | applying | Resolved Merit Deployment | 0 | NO_ITEMS | Merit deployment through trade-offs table |
| D:evaluative:judging | evaluative | judging | Definitive Worth Adjudication | 1 | HAS_ITEMS | No success metric for processing time |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Comprehensive Appraisal | 0 | NO_ITEMS | Appraisal mechanisms in place |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:reviewing | MissingSlot | Specification | Specification | Add a placeholder list of anticipated mandatory inspection stages (e.g., foundation, framing, mechanical rough-in, electrical rough-in, final) to the Verification table or Documentation section, marked as TBD pending authority confirmation | The Resolved Compliance Examination lens reveals that inspection stages are mentioned generically in Procedure Step 13 ("specific stages TBD") but are not listed even as placeholders in the Specification. For the compliance examination objective to be "resolved," the anticipated inspection stages should be enumerated so they can be verified. | Specification.md; Procedure.md | Specification.md#Verification; Procedure.md#Phase 5 Step 13 | -- | Camrose County building authority | TBD |
| D-002 | D:evaluative:judging | TBD_Question | Datasheet | Datasheet | Record TBD: Define a target or acceptable range for building authority processing time (in weeks) so that schedule impact can be evaluated against the December 2026 deadline | The Definitive Worth Adjudication lens reveals that neither the Datasheet nor any other document provides a target or range for building authority processing time. The Datasheet records "Processing timeline: TBD." Without this, the worth of the schedule cannot be definitively adjudicated -- the Project Manager cannot determine if the permit timeline supports the December 2026 completion. | Datasheet.md; Guidance.md | Datasheet.md#Attributes ("Processing timeline"); Guidance.md#Considerations ("Schedule Risk") | -- | Camrose County building authority; Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Anchor | 0 | NO_ITEMS | Governance anchored in RFP and SOW |
| X:guiding:sufficiency | guiding | sufficiency | Justified Governance Basis | 0 | NO_ITEMS | Governance basis justified through source tracing |
| X:guiding:completeness | guiding | completeness | Total Governance Purview | 1 | HAS_ITEMS | No mention of permit renewal or amendment |
| X:guiding:consistency | guiding | consistency | Aligned Governance Integrity | 0 | NO_ITEMS | Governance alignment consistent |
| X:applying:necessity | applying | necessity | Critical Implementation Mandate | 0 | NO_ITEMS | Implementation mandates clear |
| X:applying:sufficiency | applying | sufficiency | Grounded Implementation Competence | 0 | NO_ITEMS | Competence assumptions reasonable |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | No archival or closeout step |
| X:applying:consistency | applying | consistency | Harmonized Execution Fidelity | 0 | NO_ITEMS | Execution steps faithful to requirements |
| X:judging:necessity | judging | necessity | Fundamental Decisional Anchor | 0 | NO_ITEMS | Decision anchors clear (permit issuance, gate checks) |
| X:judging:sufficiency | judging | sufficiency | Justified Determination Basis | 1 | HAS_ITEMS | Verification for REQ-009-02-11 is weak |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Scope | 0 | NO_ITEMS | Judgment scope covers all requirements |
| X:judging:consistency | judging | consistency | Harmonized Judgment Integrity | 0 | NO_ITEMS | Judgment criteria consistent |
| X:reviewing:necessity | reviewing | necessity | Foundational Oversight Anchor | 0 | NO_ITEMS | Oversight anchored in inspection requirements |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Oversight Foundation | 1 | HAS_ITEMS | County representative notice period undefined |
| X:reviewing:completeness | reviewing | completeness | Total Oversight Purview | 0 | NO_ITEMS | Oversight purview comprehensive |
| X:reviewing:consistency | reviewing | consistency | Aligned Oversight Consistency | 0 | NO_ITEMS | Oversight approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add a consideration addressing permit amendment, renewal, or extension scenarios -- what happens if construction timeline extends or design changes after permit issuance | The Total Governance Purview lens reveals that the documents address the permit lifecycle from application through inspection but do not mention the scenario where the permit needs amendment (design change after issuance) or renewal/extension (construction delay beyond permit validity). For total governance purview, this scenario should be at least acknowledged. | Guidance.md; Procedure.md | Guidance.md#Considerations; Procedure.md#Phase 4 | -- | Camrose County building authority | TBD |
| X-002 | X:applying:completeness | VerificationGap | Procedure | Procedure | Add a closeout or archival step at the end of Phase 5 that confirms all inspection stages are complete, the permit is "closed out" with the authority, and all records are archived in the project record system | The Total Implementation Coverage lens reveals that the Procedure ends at Step 18 (address deficiencies) but lacks a final closeout step confirming all inspections are complete and the permit can be considered fulfilled. The Records table lists the artifacts but there is no procedural step to confirm the permit lifecycle is complete. | Procedure.md | Procedure.md#Phase 5 (after Step 18); Procedure.md#Records | -- | Project Manager | TBD |
| X-003 | X:judging:sufficiency | VerificationGap | Specification | Specification | Strengthen verification approach for REQ-009-02-11 (completion deadline) -- define specific schedule monitoring checkpoints or milestone dates rather than generic "monitoring permit acquisition milestone against project schedule" | The Justified Determination Basis lens reveals that the verification approach for REQ-009-02-11 states "Verify by monitoring permit acquisition milestone against project schedule" without defining what constitutes adequate monitoring (frequency, escalation triggers, checkpoint dates). This is insufficient to justify a determination of compliance with the December 2026 deadline. | Specification.md | Specification.md#Verification (REQ-009-02-11) | -- | Project Manager | TBD |
| X-004 | X:reviewing:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on the minimum advance notice period required for County representative attendance at inspections, and rationale for the scheduling approach chosen | The Justified Oversight Foundation lens reveals that Guidance Principle 4 and Consideration "Inspection Coordination" state that advance notice is "essential" but do not specify a minimum notice period. Procedure Steps 14-16 instruct coordination but also lack a defined notice period. Without this, the oversight foundation is not sufficiently justified -- the Proponent cannot plan inspection scheduling without knowing the required lead time. | Guidance.md; Procedure.md | Guidance.md#Principles (Principle 4); Guidance.md#Considerations ("Inspection Coordination"); Procedure.md#Phase 5 Steps 14-16 | -- | Camrose County project manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Record | 0 | NO_ITEMS | Directive records well maintained via source tracing |
| E:guiding:information | guiding | information | Coherent Directive Intelligence | 0 | NO_ITEMS | Directive information coherent across docs |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Stewardship Mastery | 0 | NO_ITEMS | Stewardship knowledge well represented in Guidance |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Strategic foresight addressed via trade-offs and considerations |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Submission tracking reference not defined |
| E:applying:information | applying | information | Actionable Performance Intelligence | 0 | NO_ITEMS | Performance information adequate |
| E:applying:knowledge | applying | knowledge | Integrated Execution Expertise | 0 | NO_ITEMS | Execution expertise integrated across Procedure steps |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment principles in Guidance |
| E:judging:data | judging | data | Substantiated Judgment Record | 0 | NO_ITEMS | Judgment records defined in Records table |
| E:judging:information | judging | information | Coherent Adjudication Intelligence | 0 | NO_ITEMS | Adjudication information coherent |
| E:judging:knowledge | judging | knowledge | Integrated Evaluative Mastery | 0 | NO_ITEMS | Evaluative knowledge integrated across documents |
| E:judging:wisdom | judging | wisdom | Principled Evaluative Foresight | 0 | NO_ITEMS | Evaluative foresight present in Guidance |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 1 | HAS_ITEMS | Record storage location inconsistency |
| E:reviewing:information | reviewing | information | Coherent Audit Intelligence | 0 | NO_ITEMS | Audit information coherent |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Mastery | 0 | NO_ITEMS | Audit knowledge comprehensive |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | TBD_Question | Procedure | Datasheet | Record TBD: Define the tracking reference format or system for the building permit application submission (e.g., authority receipt number, internal tracking ID) in the Datasheet | The Verified Execution Record lens reveals that Procedure Step 8 instructs obtaining "confirmation of receipt (submission date, tracking reference, or receipt number)" but no format or system for tracking this reference is defined. The Datasheet does not include a field for submission tracking reference. For verified execution records, this data element should be pre-defined. | Procedure.md; Datasheet.md | Procedure.md#Phase 3 Step 8; Datasheet.md#Attributes | -- | Project Manager | TBD |
| E-002 | E:reviewing:data | Normalization | Procedure | Procedure | Normalize the record storage locations: "Completed inspection reports" are listed in Records as stored in both "DEL-009-02 folder + DEL-009-04" while other records reference only one location. Clarify which is the primary record location and which is the reference copy. | The Substantiated Audit Record lens reveals that the Records table lists "Completed inspection reports" with dual storage ("DEL-009-02 folder + DEL-009-04") while most other records have a single location. Additionally, the Datasheet Construction section states "detailed inspection tracking resides in DEL-009-04" while the Procedure stores reports in both. The primary vs. copy distinction should be normalized to avoid confusion about the record of authority. | Procedure.md; Datasheet.md | Procedure.md#Records ("Completed inspection reports"); Datasheet.md#Construction (item 4) | -- | Project Manager | TBD |
