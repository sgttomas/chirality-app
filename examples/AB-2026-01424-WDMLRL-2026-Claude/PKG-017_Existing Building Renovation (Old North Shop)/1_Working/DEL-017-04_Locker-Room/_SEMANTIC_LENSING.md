# Semantic Lensing Register: DEL-017-04 New Locker/Change Room

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-017_Existing Building Renovation (Old North Shop)/1_Working/DEL-017-04_Locker-Room
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-017-04_Locker-Room/_CONTEXT.md (Deliverable Identity, Context Summary)
- _STATUS.md — DEL-017-04_Locker-Room/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-017-04_Locker-Room/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-017-04_Locker-Room/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-017-04_Locker-Room/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-017-04_Locker-Room/Guidance.md (Purpose, Principles, Considerations, Trade-offs)
- Procedure.md — DEL-017-04_Locker-Room/Procedure.md (Prerequisites, Steps Phases 1-3, Verification, Records)
- _REFERENCES.md — DEL-017-04_Locker-Room/_REFERENCES.md (Reference Map, R-01, R-04)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 6
  - Specification: 9
  - Guidance: 4
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 5  B: 2  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Occupancy classification not specified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code edition years TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for code compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection regime adequately covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure phases well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Demolition scope unclear |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Workforce headcount missing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off table present in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality appraisal consistent |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Punch-list process adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Add explicit occupancy classification for the locker/change room (e.g., Group D, Group E per NBC); design team to confirm | The prescriptive direction lens reveals that requirements REQ-017-04-03 and REQ-017-04-07 reference code compliance for "change room occupancy type" but the actual NBC occupancy classification is never stated. This affects ventilation rates, egress width, plumbing fixture counts, and fire separation requirements. | Specification.md | Requirements > REQ-017-04-03, REQ-017-04-07 | | Design team / building code consultant | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Specify applicable code edition years (NBC, NPC, CEC) or state "editions in force at time of permit application" as a mandatory practice | The mandatory practice lens reveals that the Standards table lists NBC, NPC, and CEC as ASSUMPTION with "Location TBD" and no edition years. This vagueness could lead to misapplied code requirements if editions change during the project. | Specification.md | Standards | | Design team | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-017-04-03 (Code Compliance) specifying which specific code inspections are required (building, plumbing, electrical, mechanical) and pass/fail criteria | The compliance determination lens reveals that while the Verification table says "Safety code inspection(s) with County representative present; inspection reports filed," it does not enumerate which specific inspections are required for this occupancy. The Procedure (Step 3.2) is more specific. Specification should match. | Specification.md | Verification | | Specification.md normative authority | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify demolition scope in Step 2.2: state whether demolition is expected or not, or explicitly condition on IFC drawings | The practical execution lens reveals Step 2.2 says "Scope of demolition is TBD pending final design" which is vague for an operational document. If no demolition is expected (this is new construction within existing space), the step should say so or be conditioned more precisely. | Procedure.md | Steps > Phase 2 > Step 2.2 | | Design team | TBD |
| A-005 | A:evaluative:guiding | TBD_Question | Multi | Datasheet | Record TBD: Obtain workforce headcount from County to size locker room, locker count, and bench capacity | The value orientation lens reveals that workforce headcount is identified as missing in Guidance (Space Planning) and Procedure (Prerequisites: "Workforce headcount"), but it is not recorded as a TBD in the Datasheet Attributes table where it would serve as a sizing parameter. | Datasheet.md; Guidance.md; Procedure.md | Datasheet: Attributes; Guidance: Considerations > Space Planning; Procedure: Prerequisites | | County (Owner) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Locker room footprint missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Shower facilities TBD not in Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data consistent where stated |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW and RFP references consistent |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Coverage adequate for current phase |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging consistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design-build concept understood |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade expertise identified |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for preparation phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Design-build latitude acknowledged |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table present |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable awareness present |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add "Locker room footprint (sq ft)" as an essential TBD attribute with note: "To be determined at design phase based on workforce headcount" | The essential fact lens reveals that the Datasheet records "Locker room footprint: TBD" but does not include it as a formal sizing attribute. The footprint is a foundational data point that drives all downstream design decisions (locker count, bench layout, laundry alcove, plumbing fixture count). | Datasheet.md | Attributes | | Design team | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add "Shower facilities: TBD -- not mentioned in RFP; confirm with County" to Attributes table | The comprehensive record lens reveals that Guidance mentions "Shower facilities are not mentioned in the RFP and should be treated as TBD pending County confirmation" but the Datasheet does not include this as an attribute row. For a comprehensive descriptive record, this anticipated question should be tracked. | Guidance.md; Datasheet.md | Guidance: Considerations > Plumbing; Datasheet: Attributes | | County (Owner) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Governing Mandate Clarity | 1 | HAS_ITEMS | Laundry scope boundary unclear |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Compliance Capacity | 0 | NO_ITEMS | Compliance capacity adequate |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Accessibility requirements missing |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | Core Operational Imperative | 0 | NO_ITEMS | Core operations covered |
| C:operative:sufficiency | operative | sufficiency | Validated Execution Readiness | 0 | NO_ITEMS | Execution prerequisites listed |
| C:operative:completeness | operative | completeness | Comprehensive Workflow Accounting | 1 | HAS_ITEMS | Commissioning step incomplete |
| C:operative:consistency | operative | consistency | Disciplined Process Alignment | 0 | NO_ITEMS | Process aligned |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Value proposition clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Assessment | 0 | NO_ITEMS | Merit assessment present |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Value trade-offs addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify in REQ-017-04-02 whether "laundry services" includes supply of appliances or only rough-in; current wording "Laundry equipment specifications (washer, dryer, hookups) are TBD pending design" is ambiguous on procurement responsibility | The Governing Mandate Clarity lens reveals that the boundary between "laundry services" as rough-in vs. appliance supply is ambiguous. Specification says "TBD pending design" but Procedure Step 2.12 assumes both supply and installation. The scope of this mandatory requirement needs tighter definition. | Specification.md; Procedure.md | Specification: Requirements > REQ-017-04-02; Procedure: Steps > Step 2.12 | | Design team / County | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement for accessibility compliance (Alberta Building Code / NBC accessibility provisions) if locker room is a common-use facility | The Exhaustive Regulatory Coverage lens reveals no mention of accessibility requirements (barrier-free design, accessible locker, bench height, door width) anywhere in the four documents. If the locker room is a common-use facility, Alberta Building Code accessibility provisions may apply. This is a potential regulatory gap. | Specification.md | Requirements (entire section scanned) | | Design team / building code consultant | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add commissioning/startup step for ventilation system (exhaust fan airflow verification against code-required rates) as a distinct step or sub-step in Phase 3 | The Comprehensive Workflow Accounting lens reveals that Procedure Step 2.6 installs ventilation and Step 3.2 addresses final inspections, but there is no explicit commissioning/functional test step for the ventilation system comparable to the laundry equipment test in Step 2.12. The Specification Verification table mentions "Functional test of exhaust fan; airflow verification per code" but no corresponding Procedure step exists. | Procedure.md; Specification.md | Procedure: Steps (Phase 2-3 scanned); Specification: Verification > REQ-017-04-07 | | Specification.md normative authority | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Regulatory Assurance | 1 | HAS_ITEMS | Fire separation TBD |
| F:normative:sufficiency | normative | sufficiency | Substantiated Compliance Warrant | 1 | HAS_ITEMS | P.Eng. scope gap |
| F:normative:completeness | normative | completeness | Total Regulatory Dominion | 0 | NO_ITEMS | Regulatory coverage adequate given TBDs |
| F:normative:consistency | normative | consistency | Coherent Governance Standard | 0 | NO_ITEMS | Governance references consistent |
| F:operative:necessity | operative | necessity | Critical Execution Certainty | 1 | HAS_ITEMS | Utility isolation not detailed |
| F:operative:sufficiency | operative | sufficiency | Warranted Process Competence | 0 | NO_ITEMS | Process competence adequate |
| F:operative:completeness | operative | completeness | Exhaustive Process Dominion | 0 | NO_ITEMS | Process coverage adequate |
| F:operative:consistency | operative | consistency | Principled Execution Reliability | 0 | NO_ITEMS | Execution consistency maintained |
| F:evaluative:necessity | evaluative | necessity | Foundational Worth Discernment | 1 | HAS_ITEMS | Cost/budget absent |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Justification | 0 | NO_ITEMS | Value justification present |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Reckoning | 0 | NO_ITEMS | Worth accounting adequate |
| F:evaluative:consistency | evaluative | consistency | Steadfast Merit Integrity | 0 | NO_ITEMS | Merit integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement or TBD note for fire separation between locker room and adjacent spaces (occupancy separation per NBC) | The Binding Regulatory Assurance lens reveals that the Specification does not address fire separation rating between the locker room and adjacent spaces (washroom, mezzanine area, connection corridor). For new construction within an existing building, fire separation requirements per NBC are a binding regulatory concern. | Specification.md | Requirements (entire section scanned) | | Design team / building code consultant | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Clarify in REQ-017-04-04 whether P.Eng. stamp requirement extends to mechanical/ventilation drawings or only architectural/structural/electrical/plumbing | The Substantiated Compliance Warrant lens reveals that REQ-017-04-04 requires P.Eng.-stamped IFC drawings but the scope of disciplines requiring stamping is not explicit. The Documentation table lists architectural, plumbing, and electrical IFC drawings but not mechanical/ventilation separately. If mechanical drawings are required, they should be listed. | Specification.md | Requirements > REQ-017-04-04; Documentation | | RFP section 3.3.2 | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite or step note for utility isolation verification before commencing rough-in work (Step 2.4, 2.5) -- currently mentioned in Step 2.1 but not as a formal prerequisite gate | The Critical Execution Certainty lens reveals that Step 2.1 mentions "Confirm utility isolation requirements with MEP subtrades before commencing demolition or rough-in" but this is not tracked as a formal prerequisite with a Status column entry like the other prerequisites. For critical execution certainty, utility isolation confirmation should be a gated prerequisite. | Procedure.md | Prerequisites; Steps > Phase 2 > Step 2.1 | | General Contractor | TBD |
| F-004 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add note in Considerations or Trade-offs acknowledging budget/cost constraints or stating that cost considerations are deferred to contract negotiation | The Foundational Worth Discernment lens reveals that neither Guidance nor any other document mentions budget, cost, or affordability constraints for this deliverable. While this is a design-build contract where cost is part of the proponent's proposal, acknowledging cost as a design driver (or explicitly deferring it) would strengthen the rationale for trade-off decisions like locker material and laundry equipment grade. | Guidance.md | Trade-offs; Considerations (entire sections scanned) | | County / Project Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Decisive Prescriptive Authority | 0 | NO_ITEMS | Prescriptive authority clear |
| D:normative:applying | normative | applying | Enforced Conformance Closure | 1 | HAS_ITEMS | Scope boundary ambiguity |
| D:normative:judging | normative | judging | Conclusive Compliance Ruling | 0 | NO_ITEMS | Compliance ruling path clear |
| D:normative:reviewing | normative | reviewing | Settled Oversight Regime | 0 | NO_ITEMS | Oversight regime settled |
| D:operative:guiding | operative | guiding | Confirmed Procedural Direction | 0 | NO_ITEMS | Procedural direction confirmed |
| D:operative:applying | operative | applying | Assured Task Deployment | 1 | HAS_ITEMS | Coordination mechanism vague |
| D:operative:judging | operative | judging | Resolved Performance Verdict | 0 | NO_ITEMS | Performance verdict approach clear |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Rigor | 0 | NO_ITEMS | Workflow rigor confirmed |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Direction | 0 | NO_ITEMS | Value direction resolved |
| D:evaluative:applying | evaluative | applying | Justified Worth Enactment | 0 | NO_ITEMS | Worth enactment justified |
| D:evaluative:judging | evaluative | judging | Definitive Merit Ruling | 1 | HAS_ITEMS | No quality standard for finishes |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Constancy | 0 | NO_ITEMS | Quality constancy adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | Guidance | Resolve CON-017-04-01: confirm physical boundary between DEL-017-04 (locker room) and DEL-017-03 (washroom) scope on IFC drawings; document ruling in Guidance Conflict Table | The Enforced Conformance Closure lens surfaces the existing conflict (CON-017-04-01 in Guidance) where RFP groups locker room with washroom expansion but the decomposition separates them. This conflict directly affects what work is "in scope" for conformance closure of this deliverable. | Guidance.md; Specification.md | Guidance: Conflict Table > CON-017-04-01; Specification: Scope > Included | Guidance.md#Conflict Table (RFP grouped); Specification.md#Scope (decomposition split) | Decomposition scope split; County to confirm on IFC | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add explicit coordination mechanism for DEL-017-03 interface (e.g., joint coordination meeting, shared MEP coordination drawing review) as a sub-step in Phase 1 or Phase 2 | The Assured Task Deployment lens reveals that while REQ-017-04-10 requires coordination with DEL-017-03, and Procedure Steps 1.1, 2.4 mention coordination, no specific coordination mechanism (meeting, drawing review, sign-off) is defined. For assured deployment, the interface should have a defined handshake. | Procedure.md; Specification.md | Procedure: Steps > Step 1.1, Step 2.4; Specification: Requirements > REQ-017-04-10 | | General Contractor / Project Manager | TBD |
| D-003 | D:evaluative:judging | TBD_Question | Specification | Specification | Record TBD: Define minimum quality standards or performance criteria for interior finishes (flooring, wall, ceiling) -- currently "TBD" with no direction | The Definitive Merit Ruling lens reveals that finishes are listed as "TBD" in Specification (Scope), Datasheet (Construction), and Procedure (Step 2.9) with no quality criteria. For a definitive merit ruling on completion quality, there must be at minimum a performance standard (e.g., slip resistance rating for flooring, moisture resistance for walls). | Specification.md; Datasheet.md; Procedure.md | Specification: Scope > Included; Datasheet: Construction > Finishes; Procedure: Steps > Step 2.9 | | Design team / County | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Directive Foundation | 0 | NO_ITEMS | Directive foundation grounded |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Stewardship Basis | 0 | NO_ITEMS | Stewardship basis warranted |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Coverage | 1 | HAS_ITEMS | No guidance on permit timeline |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Coherence | 0 | NO_ITEMS | Directional coherence maintained |
| X:applying:necessity | applying | necessity | Foundational Practice Mandate | 1 | HAS_ITEMS | Verification for door/hardware missing |
| X:applying:sufficiency | applying | sufficiency | Verified Implementation Basis | 0 | NO_ITEMS | Implementation basis verified |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | As-built drawings not listed |
| X:applying:consistency | applying | consistency | Coherent Implementation Standard | 0 | NO_ITEMS | Implementation standard coherent |
| X:judging:necessity | judging | necessity | Binding Assessment Foundation | 1 | HAS_ITEMS | Acceptance criteria for REQ-017-04-01 weak |
| X:judging:sufficiency | judging | sufficiency | Warranted Assessment Evidence | 0 | NO_ITEMS | Assessment evidence adequate |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Record | 0 | NO_ITEMS | Assessment records adequate |
| X:judging:consistency | judging | consistency | Congruent Assessment Integrity | 0 | NO_ITEMS | Assessment integrity congruent |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Imperative | 0 | NO_ITEMS | Audit imperative addressed |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Audit Competence | 0 | NO_ITEMS | Audit competence warranted |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 0 | NO_ITEMS | Audit coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Coherent Audit Integrity | 0 | NO_ITEMS | Audit integrity coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on permit application timeline relative to construction start; Procedure Step 1.5 requires permits before construction but no timeline guidance is provided | The Exhaustive Guidance Coverage lens reveals that while Procedure Step 1.5 requires permits before construction, Guidance does not discuss permit lead times, sequencing with design completion, or the County's role in fee payment timing. For exhaustive guidance, the relationship between permit timeline and construction schedule should be addressed. | Guidance.md; Procedure.md | Guidance: Considerations (entire section scanned); Procedure: Steps > Step 1.5 | | Project Manager | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification approach for doors and hardware (currently no verification entry for door installation quality, hardware function, or fire rating if applicable) | The Foundational Practice Mandate lens reveals that doors and hardware are listed in Specification Scope and Procedure Step 2.13, but the Verification table has no entry for door verification. If doors have fire rating requirements (linked to F-001 fire separation), this gap becomes critical. | Specification.md | Scope > Included; Verification (table scanned) | | Specification.md normative authority | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add "As-Built Drawings" to the Documentation artifacts table | The Exhaustive Implementation Record lens reveals that the Specification Documentation table lists IFC drawings but not as-built drawings. For a design-build project, as-built documentation is a standard deliverable for the owner's facility records. Procedure Records table also omits as-builts. | Specification.md; Procedure.md | Specification: Documentation; Procedure: Records | | RFP / CCDC 14-2013 | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen verification for REQ-017-04-01: "Visual inspection at substantial completion; punch-list review" is weak -- add measurable acceptance criteria (e.g., locker count matches specification, all fixtures operational, space dimensions match IFC) | The Binding Assessment Foundation lens reveals that the verification approach for the primary requirement (REQ-017-04-01 -- Locker/Change Room Construction) is only "Visual inspection at substantial completion; punch-list review." This is the least specific verification entry and does not provide a binding assessment foundation. Other requirements have more specific approaches. | Specification.md | Verification > REQ-017-04-01 | | Specification.md normative authority | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record adequate |
| E:guiding:information | guiding | information | Contextual Steering Signal | 1 | HAS_ITEMS | Dryer exhaust code requirements unclear |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Stewardship Mastery | 0 | NO_ITEMS | Stewardship mastery adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Stewardship Foresight | 0 | NO_ITEMS | Foresight adequate |
| E:applying:data | applying | data | Verified Execution Evidence | 1 | HAS_ITEMS | Normalization needed |
| E:applying:information | applying | information | Contextual Execution Indicator | 0 | NO_ITEMS | Execution indicators adequate |
| E:applying:knowledge | applying | knowledge | Proficient Execution Mastery | 0 | NO_ITEMS | Execution mastery adequate |
| E:applying:wisdom | applying | wisdom | Wise Implementation Judgment | 0 | NO_ITEMS | Implementation judgment wise |
| E:judging:data | judging | data | Authoritative Verdict Record | 0 | NO_ITEMS | Verdict record adequate |
| E:judging:information | judging | information | Contextual Verdict Clarity | 0 | NO_ITEMS | Verdict clarity adequate |
| E:judging:knowledge | judging | knowledge | Proficient Judgment Mastery | 0 | NO_ITEMS | Judgment mastery adequate |
| E:judging:wisdom | judging | wisdom | Principled Verdict Wisdom | 0 | NO_ITEMS | Verdict wisdom adequate |
| E:reviewing:data | reviewing | data | Authoritative Audit Record | 1 | HAS_ITEMS | Normalization for inspection terminology |
| E:reviewing:information | reviewing | information | Contextual Audit Clarity | 0 | NO_ITEMS | Audit clarity adequate |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Audit Mastery | 0 | NO_ITEMS | Audit mastery adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | TBD_Question | Guidance | Guidance | Add note clarifying whether dryer exhaust duct requires a building permit amendment or separate mechanical permit; current text only addresses routing options but not regulatory pathway | The Contextual Steering Signal lens reveals that Guidance discusses dryer exhaust duct routing options (wall vs. roof) but does not address the regulatory/permit implications of an exterior penetration through the Old North Shop wall. This is a steering signal gap -- the design team needs to know early whether this penetration triggers additional permit or structural review requirements. | Guidance.md | Considerations > Laundry Services | | Design team / permit authority | TBD |
| E-002 | E:applying:data | Normalization | Multi | Guidance | Normalize terminology: "laundry alcove" (Guidance, Procedure) vs. "laundry services" (Specification, RFP) vs. "laundry room" (Guidance Trade-offs) -- establish consistent term across documents | The Verified Execution Evidence lens reveals inconsistent terminology for the laundry area: Guidance uses "laundry alcove" and "separate laundry room" in trade-offs; Specification uses "laundry services"; Procedure Step 1.2 uses "laundry alcove." Consistent naming reduces ambiguity during execution. | Guidance.md; Specification.md; Procedure.md | Guidance: Considerations > Laundry Services; Trade-offs; Specification: Scope; Procedure: Steps > Step 1.2 | | Guidance.md (vocabulary authority) | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Guidance | Normalize "safety code inspection" vs. "Safety Code inspection" vs. "safety codes authority" vs. "authority having jurisdiction" -- use one consistent term throughout | The Authoritative Audit Record lens reveals inconsistent capitalization and naming for the inspection authority: "Alberta safety codes authority" (Procedure Step 2.4), "safety code inspection(s)" (Specification Verification), "authority having jurisdiction" (Procedure Step 2.6), "Alberta Safety Codes" (Specification Standards). A vocabulary note in Guidance would prevent drift. | Specification.md; Procedure.md | Specification: Verification; Standards; Procedure: Steps > Steps 2.4, 2.5, 2.6 | | Guidance.md (vocabulary authority) | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- all 96 matrix cells (A:12, B:16, C:12, F:12, D:12, X:16, E:16) have Lens Coverage entries |
| No invention | PASS -- all warranted items grounded in evidence or explicit absence in production documents |
| Provenance present | PASS -- every item has SourcePath + SectionRef |
| Conflicts surfaced | PASS -- 1 conflict (D-001 / CON-017-04-01) has Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- 24 total items matches sum of matrix items (5+2+3+4+3+4+3=24) |
| Schema followed | PASS -- output follows STRUCTURE schema |
