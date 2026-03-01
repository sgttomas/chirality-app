# Semantic Lensing Register: DEL-017-03 Washroom Renovation & Expansion

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-017_Existing Building Renovation (Old North Shop)/1_Working/DEL-017-03_Washroom-Reno
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-017-03_Washroom-Reno/_CONTEXT.md (Deliverable Identity, Context Summary)
- _STATUS.md — DEL-017-03_Washroom-Reno/_STATUS.md (Current Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-017-03_Washroom-Reno/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-017-03_Washroom-Reno/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-017-03_Washroom-Reno/Specification.md (Scope, Requirements REQ-001 through REQ-010, Standards, Verification, Documentation)
- Guidance.md — DEL-017-03_Washroom-Reno/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-017-03_Washroom-Reno/Procedure.md (Prerequisites, Steps Phases 1-6, Verification, Records)
- _REFERENCES.md — DEL-017-03_Washroom-Reno/_REFERENCES.md (Reference Map, Cross-References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 6
  - Specification: 8
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 7
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code editions not specified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Accessibility standard vague |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for accessibility |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection coordination well-covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Hot water requirement unclear |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers execution checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No quality/durability criteria for fixtures |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table captures design-build discretion |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Implicitly covered via code compliance and functional testing |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Punch-list process captures quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of the Alberta Building Code and National Plumbing Code of Canada applies (year/edition). Standards table lists "edition TBD" for both. | The prescriptive direction lens reveals that the governing code editions are unresolved, which could change design decisions. | Specification.md | ## Standards | -- | PROPOSAL: Design team to confirm applicable code editions during design phase (Step 1.2 of Procedure) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-008 accessibility requirement: specify whether Alberta Building Code Part 3 barrier-free provisions or another standard applies; remove ASSUMPTION tag once confirmed. | Mandatory practice lens shows REQ-008 is tagged as ASSUMPTION with no specific standard cited, creating ambiguity about what accessibility provisions are obligatory. | Specification.md | ### REQ-008 | -- | PROPOSAL: Design team to confirm applicable accessibility provisions per code review (CODE-REVIEW-001 / ACCESS-REVIEW-001) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for REQ-008 (accessibility): define measurable pass/fail criteria (e.g., turning radius, grab bar presence, clearances) or reference the applicable code section. | Compliance determination lens reveals that verification for REQ-008 is "Accessibility review completed and confirmed during design and inspection phases" which lacks specific acceptance criteria. | Specification.md | ## Verification (REQ-008 row) | -- | PROPOSAL: Architect/Engineer to define acceptance criteria based on applicable code | TBD |
| A-004 | A:operative:guiding | TBD_Question | Procedure | Guidance | TBD: Confirm whether hot water supply is required for washroom fixtures per Alberta Building Code. Procedure Step 3.1 notes "hot water if required by code" but does not resolve the question. | Procedural direction lens surfaces an unresolved prerequisite that affects plumbing rough-in scope. | Procedure.md | ### Step 3.1 | -- | PROPOSAL: Plumbing designer (PKG-006) to confirm hot water requirement | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Specification | Guidance | Add guidance on minimum fixture quality/durability expectations for an industrial maintenance facility environment (e.g., commercial-grade vitreous china, vandal-resistant accessories). | Value orientation lens reveals no fixture quality or durability criteria exist in the normative or guidance documents, despite the industrial context suggesting this matters for lifecycle value. | Specification.md; Guidance.md | entire document scanned | -- | PROPOSAL: Design team to establish fixture quality direction in Guidance | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Existing condition dimensions unknown |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Fixture count TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet References section is comprehensive |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistently sourced from App B |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW references and RFP sections clearly cited |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context Summary and Guidance Purpose provide adequate framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Four documents together provide a comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology variation for "ADA/Alberta accessibility" |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design-build authority principle well-articulated in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade professional coordination documented |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of phases 1-6 is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict Table C-01 demonstrates needed discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Documents together present holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Record existing washroom footprint dimensions once existing condition survey (Step 1.1) is completed. Currently "TBD -- existing washroom footprint not dimensioned." | Essential fact lens: existing washroom size is a foundational datum required for design decisions (expansion vs. reconfiguration), currently absent. | Datasheet.md | ## Attributes (Existing Condition Size row) | -- | PROPOSAL: GC site survey to populate this field | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Record existing fixture inventory (type, quantity, condition) once existing condition survey is completed. Currently "TBD -- existing fixture inventory not documented." | Adequate evidence lens: without existing fixture count, the scope of demolition and replacement cannot be fully quantified. | Datasheet.md | ## Attributes (Fixture Count existing row) | -- | PROPOSAL: GC site survey to populate this field | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Standardize accessibility terminology: Procedure uses "ADA/Alberta accessibility requirements" (Step 1.2, Prerequisite ACCESS-REVIEW-001) while Specification and Guidance use "Alberta accessibility requirements." ADA is a US standard and does not apply in Alberta. | Coherent message lens: mixed use of "ADA" and "Alberta" accessibility terminology creates a risk of misinterpretation about which standard governs. | Procedure.md; Specification.md; Guidance.md | Procedure ## Prerequisites (ACCESS-REVIEW-001); Specification ### REQ-008; Guidance ## Considerations ### Accessibility | -- | PROPOSAL: Remove "ADA/" reference from Procedure; use "Alberta Building Code accessibility provisions" consistently | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Governing Threshold | 1 | HAS_ITEMS | Electrical inspection not listed |
| C:normative:sufficiency | normative | sufficiency | Mandated Substantiation | 0 | NO_ITEMS | Substantiation for each REQ is provided via Source fields |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Record | 1 | HAS_ITEMS | Electrical permit gap |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Regulatory references are consistent across docs |
| C:operative:necessity | operative | necessity | Operational Readiness Demand | 0 | NO_ITEMS | Prerequisites table covers readiness demands |
| C:operative:sufficiency | operative | sufficiency | Confirmed Operational Capability | 0 | NO_ITEMS | Operational capability confirmation covered by verification checks |
| C:operative:completeness | operative | completeness | Whole-Process Execution Scope | 0 | NO_ITEMS | Phases 1-6 cover the full execution scope |
| C:operative:consistency | operative | consistency | Dependable Process Coherence | 0 | NO_ITEMS | Process steps are coherent and sequenced |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Purpose statement in Guidance articulates value |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Value Appraisal | 0 | NO_ITEMS | Trade-offs provide value appraisal |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 1 | HAS_ITEMS | No lifecycle/maintenance considerations |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Alignment | 0 | NO_ITEMS | Worth reasoning aligned across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add electrical inspection to the Verification table. Procedure references electrical rough-in (Step 3.3) and trim-out (Step 4.3) but Specification Verification table does not list an electrical inspection requirement. | Compulsory Governing Threshold lens: electrical work in Alberta requires Safety Code permits and inspections; this verification step is absent from the normative document. | Specification.md | ## Verification | -- | PROPOSAL: GC/Electrical Inspector to confirm electrical inspection requirement | TBD |
| C-002 | C:normative:completeness | MissingSlot | Procedure | Specification | Add electrical permit to the Safety Code permits list in Procedure Prerequisites and Specification Documentation. Procedure lists "plumbing and mechanical permits at minimum" but omits electrical despite electrical rough-in being scoped. | Exhaustive Regulatory Record lens: the permit inventory is incomplete -- electrical work scope (lighting, fan circuit, receptacles) would require a separate electrical permit under Alberta Safety Codes. | Procedure.md; Specification.md | Procedure ## Prerequisites ### Additional Prerequisites (Safety Code Permits row); Specification ## Documentation | -- | PROPOSAL: Confirm electrical permit requirement with AHJ | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a Considerations subsection addressing lifecycle maintenance and ease of cleaning for selected fixtures and finishes, given the industrial maintenance facility context. | Holistic Worth Assessment lens: no lifecycle or maintenance-of-fixtures rationale exists in Guidance, despite the harsh operational environment (landfill maintenance facility) making this a material factor for long-term value. | Guidance.md | ## Considerations | -- | PROPOSAL: Design team to address in finish schedule rationale | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Conformance Baseline | 1 | HAS_ITEMS | Fire separation not addressed |
| F:normative:sufficiency | normative | sufficiency | Stipulated Evidence Threshold | 0 | NO_ITEMS | Evidence thresholds defined by inspection reports and P.Eng. stamps |
| F:normative:completeness | normative | completeness | Total Compliance Assurance | 0 | NO_ITEMS | Compliance coverage adequate for identified codes |
| F:normative:consistency | normative | consistency | Codified Conformance Integrity | 0 | NO_ITEMS | Conformance references internally consistent |
| F:operative:necessity | operative | necessity | Execution Preparedness Gate | 1 | HAS_ITEMS | Asbestos/hazmat survey missing |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Competence | 0 | NO_ITEMS | Trade coordination assignments are clear |
| F:operative:completeness | operative | completeness | Total Procedural Capacity | 0 | NO_ITEMS | Procedure phases are complete |
| F:operative:consistency | operative | consistency | Systematic Workflow Discipline | 0 | NO_ITEMS | Workflow sequencing is systematic |
| F:evaluative:necessity | evaluative | necessity | Foundational Value Threshold | 0 | NO_ITEMS | Value proposition clear via Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Standard | 0 | NO_ITEMS | Merit is justified by operational necessity |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Quality Mastery | 1 | HAS_ITEMS | Commissioning criteria gap |
| F:evaluative:consistency | evaluative | consistency | Harmonized Value Integrity | 0 | NO_ITEMS | Value integrity is harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Specification | Guidance | TBD: Determine whether the washroom renovation triggers fire separation requirements under the Alberta Building Code (e.g., fire-rated wall between washroom and adjacent spaces, or between renovated area and mezzanine above). | Compulsory Conformance Baseline lens: fire separation is a common code requirement for renovation work; no mention exists in any production document. The building has a mezzanine above the washroom. | Specification.md; Guidance.md | entire document scanned | -- | PROPOSAL: Code review (CODE-REVIEW-001) should explicitly address fire separation | TBD |
| F-002 | F:operative:necessity | TBD_Question | Procedure | Procedure | TBD: Determine whether a hazardous materials survey (asbestos, lead paint) is required before demolition of existing washroom fixtures and finishes in the Old North Shop (existing building). | Execution Preparedness Gate lens: the Old North Shop is an existing building; demolition of existing finishes in older buildings typically requires hazmat assessment under Alberta OH&S. No mention in any production document. | Procedure.md | ### Phase 2 -- Site Preparation and Demolition | -- | PROPOSAL: GC OH&S program to confirm hazmat survey requirement before demolition | TBD |
| F-003 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add measurable commissioning acceptance criteria for ventilation system (e.g., minimum exhaust air flow rate per Alberta Building Code) to Verification table for REQ-007. | Comprehensive Quality Mastery lens: REQ-007 verification states "Ventilation system inspected and confirmed compliant" but provides no measurable performance criteria for the commissioning check. | Specification.md | ## Verification (REQ-007 row) | -- | PROPOSAL: Mechanical designer (PKG-003) to specify ventilation performance criteria | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Directive Closure | 0 | NO_ITEMS | Binding directives are clear and closed via REQs |
| D:normative:applying | normative | applying | Substantiated Obligatory Act | 0 | NO_ITEMS | Obligations substantiated by source references |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 0 | NO_ITEMS | Conformance verdicts mapped to inspections |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Standing | 0 | NO_ITEMS | Regulatory standing will be resolved via inspection regime |
| D:operative:guiding | operative | guiding | Settled Execution Instruction | 0 | NO_ITEMS | Execution instructions are settled in Procedure |
| D:operative:applying | operative | applying | Demonstrated Skilled Proficiency | 0 | NO_ITEMS | Trade coordination demonstrates skill assignment |
| D:operative:judging | operative | judging | Finalized Performance Verdict | 1 | HAS_ITEMS | Functional test criteria vague |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Order | 0 | NO_ITEMS | Procedural order is well-resolved (Phases 1-6) |
| D:evaluative:guiding | evaluative | guiding | Settled Merit Direction | 0 | NO_ITEMS | Merit direction settled by Purpose and Principles |
| D:evaluative:applying | evaluative | applying | Finalized Quality Delivery | 1 | HAS_ITEMS | Finish quality criteria absent |
| D:evaluative:judging | evaluative | judging | Definitive Quality Verdict | 0 | NO_ITEMS | Quality verdict path via punch-list and inspections |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Standing | 0 | NO_ITEMS | Quality standing resolution path exists |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:judging | VerificationGap | Procedure | Specification | Add specific functional test acceptance criteria for REQ-006 plumbing fixtures (e.g., minimum water pressure at fixture, drain flow rate, leak test duration/method). Currently "Functional testing of all fixtures; no leaks; drain confirmed clear" -- needs measurable criteria. | Finalized Performance Verdict lens: the functional test criteria are described in general terms but lack the specificity needed to produce a definitive pass/fail verdict. | Procedure.md; Specification.md | Procedure ## Verification (All fixtures operational row); Specification ## Verification (REQ-006 row) | -- | PROPOSAL: Plumbing designer (PKG-006) to define test procedures and acceptance criteria | TBD |
| D-002 | D:evaluative:applying | MissingSlot | Specification | Specification | Add requirement or reference for finish material specification criteria (minimum durability rating, slip resistance for floor tile, moisture resistance) applicable to industrial washroom in a landfill maintenance facility. | Finalized Quality Delivery lens: the finish schedule is deferred to DEL-001-08 but no minimum performance criteria for finishes are stated in the Specification, leaving the quality delivery standard undefined for this deliverable. | Specification.md; Datasheet.md | Specification ## Documentation (Finish Schedule row); Datasheet ## Construction (Finishes row) | -- | PROPOSAL: Design team to establish finish performance criteria | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Ground | 0 | NO_ITEMS | Foundational directives grounded in RFP/SOW |
| X:guiding:sufficiency | guiding | sufficiency | Justified Informed Counsel | 0 | NO_ITEMS | Guidance Principles section provides justified counsel |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Archive | 1 | HAS_ITEMS | Missing reference to OH&S Act specifics |
| X:guiding:consistency | guiding | consistency | Unified Governance Clarity | 0 | NO_ITEMS | Governance direction is unified |
| X:applying:necessity | applying | necessity | Validated Practice Imperative | 1 | HAS_ITEMS | Scope boundary coordination gap |
| X:applying:sufficiency | applying | sufficiency | Substantiated Capable Delivery | 0 | NO_ITEMS | Delivery capability substantiated by trade assignments |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Mastery | 0 | NO_ITEMS | Delivery scope coverage is exhaustive |
| X:applying:consistency | applying | consistency | Coherent Delivery Standard | 0 | NO_ITEMS | Delivery standards coherent across documents |
| X:judging:necessity | judging | necessity | Critical Conformance Criterion | 1 | HAS_ITEMS | Warranty verification gap |
| X:judging:sufficiency | judging | sufficiency | Proven Contextual Verdict | 0 | NO_ITEMS | Verdict contexts are proven via inspection reports |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Archive | 0 | NO_ITEMS | Assessment archive requirements defined in Records |
| X:judging:consistency | judging | consistency | Transparent Harmonized Judgment | 0 | NO_ITEMS | Judgment criteria harmonized across verification tables |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Catalyst | 0 | NO_ITEMS | Audit triggers defined by inspection milestones |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Oversight Position | 0 | NO_ITEMS | Oversight position justified by County presence requirement |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Trail | 1 | HAS_ITEMS | As-built drawing requirement missing |
| X:reviewing:consistency | reviewing | consistency | Stable Harmonized Appraisal | 0 | NO_ITEMS | Appraisal approach stable and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add specific Alberta OH&S Act reference (or section) to Standards table. Currently listed as "Alberta OH&S Legislation" with "Prime Contractor obligations during construction" -- no Act citation or specific obligation enumeration. | Exhaustive Governance Archive lens: the OH&S reference is generic; a complete governance archive would identify the specific Act and key obligation sections (e.g., prime contractor duties under Part 2). | Specification.md | ## Standards (Alberta OH&S row) | -- | PROPOSAL: GC OH&S program to identify specific Act sections | TBD |
| X-002 | X:applying:necessity | Normalization | Multi | Guidance | Standardize the cross-reference format for DEL-017-04 scope boundary across documents. Datasheet Conditions says "Locker/Change Room"; Guidance Principle 3 says "DEL-017-04 (locker/change room with laundry, SOW-0073)"; Specification exclusion table says "Locker/change room with laundry services." Use consistent phrasing. | Validated Practice Imperative lens: the scope boundary with DEL-017-04 is referenced with varying levels of detail across documents, risking drift in how the boundary is understood. | Datasheet.md; Specification.md; Guidance.md | Datasheet ## Conditions (Locker/Change Room row); Specification ## Scope ### Exclusions; Guidance ## Principles ### 3 | -- | PROPOSAL: Adopt "Locker/change room with laundry services (DEL-017-04, SOW-0073)" as canonical phrasing | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Procedure | Add a warranty period verification checkpoint to Procedure: confirm warranty documentation is produced, warranty start date recorded at CCC, and defect rectification obligation is tracked. REQ-010 verification says "Warranty obligations maintained through guarantee period" but no procedural step or record explicitly triggers this. | Critical Conformance Criterion lens: the warranty requirement (REQ-010) has a verification statement but no corresponding procedural step to initiate warranty tracking at CCC. | Specification.md; Procedure.md | Specification ## Verification (REQ-010 row); Procedure ## Steps ### Phase 6 | -- | PROPOSAL: Add warranty initiation step to Phase 6 | TBD |
| X-004 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add as-built drawing requirement to Records table. Renovation work will modify the existing building layout; an as-built record of the completed washroom (reflecting actual plumbing locations, partition positions, fixture positions) is standard practice for facility operations and future maintenance. | Comprehensive Audit Trail lens: the Records table does not include as-built drawings for the washroom renovation, which would be needed for facility management after handover. | Procedure.md | ## Records | -- | PROPOSAL: GC/Architect to confirm as-built requirement per CCDC 14-2013 | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Anchored Stewardship Record | 0 | NO_ITEMS | Stewardship data well-anchored in Datasheet |
| E:guiding:information | guiding | information | Transparent Policy Guidance | 0 | NO_ITEMS | Policy guidance transparent in Guidance doc |
| E:guiding:knowledge | guiding | knowledge | Integrated Stewardship Mastery | 0 | NO_ITEMS | Stewardship knowledge integrated across documents |
| E:guiding:wisdom | guiding | wisdom | Principled Stewardship Foresight | 1 | HAS_ITEMS | Conflict C-01 unresolved |
| E:applying:data | applying | data | Validated Performance Record | 0 | NO_ITEMS | Performance records defined |
| E:applying:information | applying | information | Contextual Execution Account | 0 | NO_ITEMS | Execution context adequately accounted |
| E:applying:knowledge | applying | knowledge | Grounded Workmanship Proficiency | 0 | NO_ITEMS | Workmanship proficiency requirements implicit in trade assignments |
| E:applying:wisdom | applying | wisdom | Prudent Craft Foresight | 0 | NO_ITEMS | Craft foresight demonstrated in Considerations |
| E:judging:data | judging | data | Authoritative Finding Record | 0 | NO_ITEMS | Finding records defined via inspection reports |
| E:judging:information | judging | information | Transparent Verdict Account | 0 | NO_ITEMS | Verdict transparency via County presence at inspections |
| E:judging:knowledge | judging | knowledge | Expert Adjudication Mastery | 0 | NO_ITEMS | Adjudication delegated to AHJ/inspectors |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Judgment foresight covered by conflict table |
| E:reviewing:data | reviewing | data | Validated Oversight Record | 0 | NO_ITEMS | Oversight records defined in Records table |
| E:reviewing:information | reviewing | information | Transparent Oversight Account | 0 | NO_ITEMS | Oversight account transparent via County PM involvement |
| E:reviewing:knowledge | reviewing | knowledge | Expert Audit Mastery | 0 | NO_ITEMS | Audit expertise assigned to inspectors |
| E:reviewing:wisdom | reviewing | wisdom | Prudent Oversight Foresight | 1 | HAS_ITEMS | Scope-split risk for contract |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | Conflict | Multi | TBD | Conflict C-01 (from Guidance) is unresolved: RFP section 3.4 groups "urinal and locker change room, including laundry services" as a single expansion item, but the Decomposition separates this into DEL-017-03 and DEL-017-04. The Guidance PROPOSAL to accept the split is pending human ruling. This must be confirmed before contract/subcontract scope documents are finalized. | Principled Stewardship Foresight lens: unresolved scope-split conflict between RFP and Decomposition affects contract clarity and subcontract scope definition. | Guidance.md; Specification.md | Guidance ## Conflict Table (C-01); Specification ## Scope | RFP section 3.4 vs. Decomposition section 7 (PKG-017 table) | PROPOSAL: Accept Decomposition split per Guidance C-01 proposal | TBD |
| E-002 | E:reviewing:wisdom | RationaleGap | Guidance | Guidance | Add rationale explaining how the DEL-017-03 / DEL-017-04 scope split should be reflected in subcontract scope documents, and what coordination obligations exist between the two deliverables during construction (shared wall, shared plumbing chase, sequencing). | Prudent Oversight Foresight lens: the scope split is documented as a conflict (C-01) but the practical coordination implications for construction execution are not addressed, creating a gap for future oversight. | Guidance.md | ## Principles ### 3. Scope Boundary with DEL-017-04 | -- | PROPOSAL: Project Manager to define coordination protocol between DEL-017-03 and DEL-017-04 | TBD |
