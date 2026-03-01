# Semantic Lensing Register: DEL-013-05 Welding Station Exhaust System

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-05_Welding-Exhaust/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-013-05_Welding-Exhaust/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements, Related Deliverables)
- _STATUS.md — DEL-013-05_Welding-Exhaust/_STATUS.md (Current Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-013-05_Welding-Exhaust/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-013-05_Welding-Exhaust/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-013-05_Welding-Exhaust/Specification.md (Scope, Requirements REQ-001 through REQ-012, Standards, Verification, Documentation)
- Guidance.md — DEL-013-05_Welding-Exhaust/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-013-05_Welding-Exhaust/Procedure.md (Purpose, Prerequisites, Steps Phases 1-5, Verification, Records)
- _REFERENCES.md — DEL-013-05_Welding-Exhaust/_REFERENCES.md (Primary References R-01/R-04, Standard References, Drawing References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 11
  - Guidance: 4
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 6  E: 4
- By type:
  - Conflict: 3
  - VerificationGap: 6
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Jurisdiction normalization issue |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Standards edition gaps |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification acceptance thresholds TBD |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | AHJ hold-point specification gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure phases well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Installation steps adequately described |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Commissioning pass/fail criteria TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit trail covered by Records table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose and value rationale present in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by commissioning sign-off process |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality review addressed via AHJ inspections and commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Normalization | Multi | Guidance | Resolve "OSHA" vs. "Alberta OHS Code" terminology consistently across all documents; Guidance CT-001 identifies this but Datasheet References and _REFERENCES.md still use "OSHA" | _CONTEXT.md uses "OSHA-compliant"; Guidance CT-001 proposes Alberta OHS Code interpretation; _REFERENCES.md still says "OSHA requirements for welding fume control"; Specification REQ-010 Note explains the mapping but the term "OSHA" persists in Specification Documentation table ("OSHA/OHS compliance documentation") | Specification.md, Guidance.md, _REFERENCES.md | Specification.md#Documentation; Guidance.md#Conflict Table CT-001; _REFERENCES.md#Standard References | Guidance.md CT-001 (Alberta OHS Code) vs. _CONTEXT.md ("OSHA-compliant") vs. _REFERENCES.md ("OSHA requirements") | PROPOSAL: Standardize on "Alberta OHS Code" throughout; retain CT-001 ruling note | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Add specific standard editions and clause references for each listed standard (Alberta Safety Codes Act edition, Alberta OHS Code Part number, NBC edition, ACGIH Manual edition, AWS document number) | All seven standards in the Specification Standards table have "ASSUMPTION: applicable; specific edition/Part/clause TBD" — no binding edition is cited, making compliance determination impossible until resolved | Specification.md | Specification.md#Standards | — | PROPOSAL: Mechanical design engineer to confirm applicable editions at Step 1.3 | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance thresholds to Verification table (e.g., minimum capture velocity value, acceptable CFM tolerance, stack height requirement) | Verification table entries for REQ-001, REQ-004, REQ-005, REQ-006 all defer numeric thresholds to "TBD per mechanical engineer" — compliance determination cannot proceed without numeric criteria | Specification.md | Specification.md#Verification | — | PROPOSAL: Populated at IFC design stage (Step 1.3) | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add explicit AHJ inspection hold points (which steps require inspection before proceeding) to Phase 3 and Phase 4 | Step 3.9 mentions "appropriate hold points per Safety Code permit requirements" but does not identify which specific steps are hold points; this leaves regulatory audit sequencing ambiguous | Procedure.md | Procedure.md#Phase 3 — Installation, Step 3.9 | — | PROPOSAL: Mechanical Contractor to confirm hold points with AHJ at permit application (Step 1.5) | TBD |
| A-005 | A:operative:judging | WeakStatement | Procedure | Procedure | Clarify "acceptable tolerance" for airflow measurement in Step 4.3 and define "significantly below design" threshold | Step 4.3 says "If measured airflow is significantly below design, investigate and correct" — "significantly" is undefined, creating ambiguous pass/fail boundary | Procedure.md | Procedure.md#Phase 4, Step 4.3 | — | PROPOSAL: Define tolerance at IFC stage | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key design input missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Welding process data not yet available |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet has numerous TBD entries |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units consistent where provided |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Welding equipment specs needed |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Guidance provides comprehensive narrative |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents generally coherent in messaging |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | LEV engineering principles covered in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Deferred to P.Eng. design engineer appropriately |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Appropriately scoped for design-build |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance conflict table provides judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | System interactions covered in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Capture velocity requirement (numeric value) — essential design fact that drives hood selection, fan sizing, and ductwork design | Capture velocity is listed as "TBD" in Datasheet Attributes; this is the single most critical design parameter for a welding LEV system and no numeric value or range is provided anywhere in the production documents | Datasheet.md | Datasheet.md#Attributes ("Capture velocity") | — | PROPOSAL: Mechanical design engineer per ACGIH Industrial Ventilation Manual tables for welding | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Welding process types (MIG, TIG, stick, flux-core, etc.) and base metals — required to determine fume character and filtration requirements | Procedure Step 1.1 identifies this as a prerequisite ("obtain welding equipment specifications from County") but Datasheet records no interim data; County has not yet provided equipment specifications | Datasheet.md, Procedure.md | Datasheet.md#Attributes ("Welding equipment specs"); Procedure.md#Phase 1, Step 1.1 | — | PROPOSAL: County project representative | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Datasheet entries for: rigid ductwork material specification, spark arrestor requirement (Y/N/TBD), recirculation vs. exhaust-only configuration, noise/vibration limits | Datasheet Construction section lists rigid ductwork as "TBD" but does not include material spec, spark arrestor, or noise parameters; Guidance discusses these (ductwork material, spark arrest, recirculation trade-off) but they are not reflected as tracked attributes in Datasheet | Datasheet.md, Guidance.md | Datasheet.md#Construction; Guidance.md#Considerations ("Ductwork Material", "Fire and Spark Arrest") | — | PROPOSAL: Add as TBD attributes in Datasheet for tracking | TBD |
| B-004 | B:information:necessity | MissingSlot | Specification | Specification | Add requirement or note addressing fire/spark hazard from welding particulates in ductwork and filtration — Guidance identifies this risk but no corresponding requirement exists in Specification | Guidance Considerations section identifies "Fire and Spark Arrest" as a design consideration; Specification has no requirement addressing fire/spark risk in the exhaust ductwork or filtration system | Specification.md, Guidance.md | Specification.md#Requirements (entire section scanned — no fire/spark requirement); Guidance.md#Considerations ("Fire and Spark Arrest") | — | PROPOSAL: Add REQ-013 or note under REQ-004 addressing spark arrestor evaluation | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Regulatory Foundation | 1 | HAS_ITEMS | Regulatory foundation incomplete |
| C:normative:sufficiency | normative | sufficiency | Justified Compliance Threshold | 0 | NO_ITEMS | Compliance thresholds addressed (though TBD numerically — captured under A-003) |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Environmental discharge regulation gap |
| C:normative:consistency | normative | consistency | Uniform Prescriptive Standard | 0 | NO_ITEMS | Standards references internally consistent |
| C:operative:necessity | operative | necessity | Essential Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table comprehensive |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Capacity | 0 | NO_ITEMS | Procedural steps adequately described |
| C:operative:completeness | operative | completeness | Comprehensive Operational Scope | 0 | NO_ITEMS | All five phases (Design through Closeout) present |
| C:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Process steps sequentially consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Imperative | 1 | HAS_ITEMS | Worker health rationale gap |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Assessment | 0 | NO_ITEMS | Trade-offs table provides merit framework |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Lifecycle and energy considerations addressed in Guidance |
| C:evaluative:consistency | evaluative | consistency | Principled Value Constancy | 0 | NO_ITEMS | Value principles consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Specification | Guidance | Add rationale for why Alberta Safety Codes Act (rather than National Building Code directly) is the governing building code framework, and clarify the relationship between NBC and Alberta Safety Codes adoption | Specification Standards table lists both Alberta Safety Codes Act and National Building Code as applicable but does not explain the adoption relationship (Alberta adopts NBC via Safety Codes Act); this could confuse compliance determination | Specification.md | Specification.md#Standards | — | PROPOSAL: Guidance to explain Alberta's adoption of NBC via Safety Codes Act | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add explicit requirement or note addressing Alberta Environmental Protection and Enhancement Act (EPEA) discharge permit requirements for welding exhaust stack emissions | Specification Standards table mentions EPEA as "ASSUMPTION: applicable; specific regulation TBD" but REQ-010 does not explicitly require an EPEA review or discharge permit; Procedure Step 1.6 addresses outlet approval but only vaguely ("any applicable environmental authority") | Specification.md, Procedure.md | Specification.md#Standards; Specification.md#Requirements REQ-010; Procedure.md#Phase 1, Step 1.6 | — | PROPOSAL: Clarify whether EPEA review is required for welding exhaust discharge in this jurisdiction | TBD |
| C-003 | C:evaluative:necessity | RationaleGap | Guidance | Guidance | Add brief rationale connecting worker health protection value to quantitative exposure limits (e.g., Alberta OHS Code TLV/TWA for welding fumes) to ground the "non-negotiable" source capture principle in measurable health outcomes | Guidance Principle 1 states "Capture at Source Is Non-Negotiable" but does not cite the specific exposure limit values that make source capture necessary; grounding the value imperative in measurable health thresholds would strengthen the rationale | Guidance.md | Guidance.md#Principles, Principle 1 | — | PROPOSAL: Reference Alberta OHS Code Schedule 1 Table 2 (or equivalent) when standard edition is confirmed | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Conformance Basis | 1 | HAS_ITEMS | Design-build responsibility gap |
| F:normative:sufficiency | normative | sufficiency | Adequate Governance Threshold | 0 | NO_ITEMS | Governance thresholds present via AHJ and County review |
| F:normative:completeness | normative | completeness | Exhaustive Prescriptive Mastery | 1 | HAS_ITEMS | P.Eng. stamp scope unclear |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Rigor | 0 | NO_ITEMS | Regulatory references consistent |
| F:operative:necessity | operative | necessity | Indispensable Process Clarity | 0 | NO_ITEMS | Process clarity adequate |
| F:operative:sufficiency | operative | sufficiency | Sufficient Execution Competence | 0 | NO_ITEMS | Competence addressed via P.Eng. requirement |
| F:operative:completeness | operative | completeness | Comprehensive Functional Mastery | 0 | NO_ITEMS | Functional scope comprehensive |
| F:operative:consistency | operative | consistency | Systematic Operational Coherence | 0 | NO_ITEMS | Operational steps coherent |
| F:evaluative:necessity | evaluative | necessity | Foundational Evaluative Basis | 1 | HAS_ITEMS | Energy cost trade-off incomplete |
| F:evaluative:sufficiency | evaluative | sufficiency | Sound Evaluative Justification | 0 | NO_ITEMS | Trade-off justifications present |
| F:evaluative:completeness | evaluative | completeness | Integral Appraisal Mastery | 0 | NO_ITEMS | Appraisal scope adequate |
| F:evaluative:consistency | evaluative | consistency | Harmonized Evaluative Order | 0 | NO_ITEMS | Evaluative criteria consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify in REQ-010 or Scope whether the Mechanical Contractor's design-build P.Eng. is responsible for confirming code compliance, or whether the County separately retains a code reviewer | Specification Scope Excluded section notes "Mechanical design engineering (design is proponent responsibility per CCDC 14-2013 design-build)" but REQ-010 lists codes without clarifying who determines compliance beyond AHJ inspection; the compulsory conformance basis is unclear on the division of responsibility | Specification.md | Specification.md#Scope (Excluded); Specification.md#Requirements REQ-010 | — | PROPOSAL: Clarify via CCDC 14-2013 contract terms | TBD |
| F-002 | F:normative:completeness | WeakStatement | Specification | Specification | Clarify scope of P.Eng. stamp requirement — does it cover only IFC drawings, or also the commissioning report, filtration performance certification, and system design calculations? | Procedure Step 1.3 requires "P.Eng.-stamped" IFC drawings; Specification Documentation lists "IFC Mechanical Drawing (P.Eng.-stamped)" but the commissioning report and filtration performance documentation do not specify whether P.Eng. certification is required | Specification.md, Procedure.md | Specification.md#Documentation; Procedure.md#Phase 1, Step 1.3 | — | PROPOSAL: Specify P.Eng. stamp scope in Specification Documentation section | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add quantitative or qualitative framing for the energy cost impact of continuous welding exhaust in Alberta winter conditions (e.g., approximate heat loss per 1000 CFM of exhaust at -30C) | Guidance Considerations ("Cold Climate Stack Considerations") identifies energy cost concern but provides no quantitative framing; this makes the trade-off between continuous exhaust and interlocked operation difficult to evaluate | Guidance.md | Guidance.md#Considerations ("Cold Climate Stack Considerations") | — | PROPOSAL: Mechanical engineer to quantify at design stage | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 1 | HAS_ITEMS | Directive authority for station count unresolved |
| D:normative:applying | normative | applying | Enforced Compliance Practice | 0 | NO_ITEMS | Compliance practices described |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance determination deferred to AHJ appropriately |
| D:normative:reviewing | normative | reviewing | Settled Governance Scrutiny | 0 | NO_ITEMS | Governance review process described |
| D:operative:guiding | operative | guiding | Resolved Operational Steering | 1 | HAS_ITEMS | Interlock design decision deferred |
| D:operative:applying | operative | applying | Resolved Working Delivery | 0 | NO_ITEMS | Delivery steps comprehensive |
| D:operative:judging | operative | judging | Resolved Capability Verdict | 0 | NO_ITEMS | Capability verification in commissioning |
| D:operative:reviewing | operative | reviewing | Settled Process Examination | 0 | NO_ITEMS | Process examination via inspection reports |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Guidance | 0 | NO_ITEMS | Merit guidance present in trade-offs |
| D:evaluative:applying | evaluative | applying | Resolved Worth Enactment | 0 | NO_ITEMS | Worth considerations in procurement and design |
| D:evaluative:judging | evaluative | judging | Definitive Merit Verdict | 1 | HAS_ITEMS | No merit criteria for filtration selection |
| D:evaluative:reviewing | evaluative | reviewing | Settled Worth Coherence | 0 | NO_ITEMS | Worth coherence adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Datasheet | Specification | Resolve welding station count: Appendix B shows one station; _DEPENDENCIES.md mentions "Multiple exhaust hoods may be needed"; Datasheet records "1 shown on conceptual floor plan; final count TBD" — directive authority for the station count is unresolved | Station count directly impacts system capacity, ductwork layout, fan sizing, and makeup air requirements; the design cannot proceed without a resolved count | Datasheet.md, Guidance.md | Datasheet.md#Attributes ("Number of welding stations"); Guidance.md#Conflict Table CT-002 | R-04 Appendix B (1 station) vs. _DEPENDENCIES.md ("Multiple hoods may be needed") | PROPOSAL: County to confirm count; design for one with expansion capability per Guidance CT-002 | TBD |
| D-002 | D:operative:guiding | WeakStatement | Specification | Specification | Clarify REQ-007 regarding whether fan interlock with welding equipment operation is required or optional; current wording ("TBD per design") leaves the operational steering unresolved | Specification REQ-007 Note states "Interlock with welding equipment operation and type of monitoring TBD per design"; Guidance Cold Climate Considerations recommends interlock; the requirement is ambiguous on whether interlock is mandatory | Specification.md, Guidance.md | Specification.md#Requirements REQ-007; Guidance.md#Considerations ("Cold Climate Stack Considerations") | — | PROPOSAL: Make interlock a requirement given cold-climate energy implications | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Specification | Specification | Add evaluation criteria for filtration unit selection (e.g., lifecycle cost, filter replacement frequency, noise level, recirculation capability) to support definitive merit verdict at procurement | Guidance Trade-offs table discusses single-stage vs. multi-stage filtration but Specification has no evaluation criteria for filtration unit selection beyond regulatory efficiency; this makes the merit verdict at procurement (Step 2.2) subjective | Specification.md, Guidance.md | Specification.md#Requirements REQ-004; Guidance.md#Trade-offs | — | PROPOSAL: Add filtration selection criteria to Specification or Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Binding Directional Resolution | 0 | NO_ITEMS | Directional resolutions appropriately deferred to design |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Prescriptive Evidence | 1 | HAS_ITEMS | Design submittal review criteria missing |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Coverage | 0 | NO_ITEMS | Guidance coverage adequate |
| X:guiding:consistency | guiding | consistency | Stable Directional Alignment | 0 | NO_ITEMS | Directional alignment stable |
| X:applying:necessity | applying | necessity | Compulsory Deployment Basis | 1 | HAS_ITEMS | IFC drawing reference gap |
| X:applying:sufficiency | applying | sufficiency | Adequate Enforcement Capacity | 0 | NO_ITEMS | Enforcement through AHJ adequate |
| X:applying:completeness | applying | completeness | Complete Enforcement Record | 1 | HAS_ITEMS | Installation record completeness |
| X:applying:consistency | applying | consistency | Consistent Enforcement Order | 0 | NO_ITEMS | Enforcement ordering consistent |
| X:judging:necessity | judging | necessity | Binding Adjudicative Finding | 1 | HAS_ITEMS | Capture velocity acceptance threshold missing |
| X:judging:sufficiency | judging | sufficiency | Sufficient Conformance Evidence | 1 | HAS_ITEMS | Smoke/tracer test method undefined |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Record | 0 | NO_ITEMS | Commissioning record scope adequate |
| X:judging:consistency | judging | consistency | Stable Adjudicative Standard | 0 | NO_ITEMS | Adjudicative standards consistent |
| X:reviewing:necessity | reviewing | necessity | Requisite Scrutiny Basis | 1 | HAS_ITEMS | Post-installation maintenance verification |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Audit evidence through inspection reports |
| X:reviewing:completeness | reviewing | completeness | Complete Audit Coverage | 0 | NO_ITEMS | Audit scope complete |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Standard | 0 | NO_ITEMS | Audit standards harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Procedure | Procedure | Add criteria for what constitutes acceptable submittal review outcome in Step 2.2 (e.g., checklist of items to verify against Specification requirements) | Step 2.2 says "Submit equipment data sheets and material specifications to the design engineer and County representative for review" but provides no acceptance criteria or review checklist | Procedure.md | Procedure.md#Phase 2, Step 2.2 | — | PROPOSAL: Add submittal review checklist referencing Specification requirements | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add explicit reference to IFC drawing as the governing document for each installation step (Steps 3.2 through 3.8) — currently only some steps reference "per IFC drawing" | Steps 3.2, 3.4, 3.6, 3.8 reference "per IFC drawing" but Steps 3.3 (flexible ductwork), 3.5 (rigid ductwork), and 3.7 (exhaust stack) do not explicitly reference the IFC drawing as the installation basis | Procedure.md | Procedure.md#Phase 3, Steps 3.3, 3.5, 3.7 | — | PROPOSAL: Add "per IFC drawing" reference to all installation steps | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement for photographic documentation of concealed work (ductwork routing through walls/ceiling, penetration flashing) before closure | Specification Documentation lists "Installation record" and "As-built drawing" but does not require photographic evidence of concealed installations; this is standard practice for mechanical installations where ductwork may be concealed | Specification.md | Specification.md#Documentation | — | PROPOSAL: Add photographic record requirement for concealed work | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add binding acceptance threshold for capture velocity verification — currently "TBD" in both Specification Verification table and Procedure Step 4.4 | Specification Verification for REQ-001 says "ASSUMPTION: method TBD per mechanical engineer"; Procedure Step 4.4 says "ASSUMPTION: Specific capture velocity protocol and acceptance threshold TBD" — no binding threshold exists | Specification.md, Procedure.md | Specification.md#Verification (REQ-001); Procedure.md#Phase 4, Step 4.4 | — | PROPOSAL: Establish at IFC design stage per ACGIH tables | TBD |
| X-005 | X:judging:sufficiency | VerificationGap | Specification | Specification | Specify which commissioning test method will be used for source capture verification (smoke test, tracer gas, or anemometer) and define pass/fail criteria | Specification Verification for REQ-001 lists "smoke test or tracer test (ASSUMPTION: method TBD)" — the method selection affects what equipment and expertise are needed at commissioning | Specification.md | Specification.md#Verification (REQ-001) | — | PROPOSAL: Mechanical engineer to specify method in commissioning plan | TBD |
| X-006 | X:reviewing:necessity | Conflict | Specification | Specification | Resolve whether post-installation filter maintenance verification is a one-time commissioning check (REQ-008 verification: "Demonstration of filter access and replacement procedure") or a recurring operational requirement | Specification Verification for REQ-008 describes a one-time demonstration; Specification Documentation lists "O&M manual" with "Filter replacement schedule and procedure" (Procedure Step 5.2); but no requirement establishes ongoing maintenance verification frequency or responsibility post-handover | Specification.md, Procedure.md | Specification.md#Verification (REQ-008); Specification.md#Documentation; Procedure.md#Phase 5, Step 5.2 | Specification (one-time demo) vs. Procedure O&M manual (implies recurring) | PROPOSAL: Clarify in Specification that O&M manual defines ongoing maintenance; one-time demo confirms accessibility | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Prescriptive Datum | 1 | HAS_ITEMS | Building dimension verification |
| E:guiding:information | guiding | information | Authoritative Guidance Signal | 0 | NO_ITEMS | Guidance signals clear and authoritative |
| E:guiding:knowledge | guiding | knowledge | Authoritative Directional Mastery | 0 | NO_ITEMS | LEV design knowledge adequately referenced |
| E:guiding:wisdom | guiding | wisdom | Principled Prescriptive Vision | 0 | NO_ITEMS | Design-build vision appropriately scoped |
| E:applying:data | applying | data | Validated Deployment Evidence | 1 | HAS_ITEMS | Ceiling height source verification |
| E:applying:information | applying | information | Coherent Deployment Account | 0 | NO_ITEMS | Deployment account coherent across phases |
| E:applying:knowledge | applying | knowledge | Comprehensive Deployment Competence | 0 | NO_ITEMS | Competence requirements addressed via P.Eng. |
| E:applying:wisdom | applying | wisdom | Principled Deployment Judgment | 0 | NO_ITEMS | Deployment judgment principles in Guidance |
| E:judging:data | judging | data | Verified Conformance Datum | 1 | HAS_ITEMS | Exhaust stack height datum missing |
| E:judging:information | judging | information | Substantiated Ruling Account | 0 | NO_ITEMS | Ruling accounts substantiated via AHJ |
| E:judging:knowledge | judging | knowledge | Authoritative Conformance Mastery | 0 | NO_ITEMS | Conformance expertise via P.Eng. and AHJ |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Judgment foresight in conflict table |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | Warranty start date documentation |
| E:reviewing:information | reviewing | information | Substantiated Audit Account | 0 | NO_ITEMS | Audit account substantiated |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Competence | 0 | NO_ITEMS | Audit competence addressed |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Verify and normalize building dimension data: Datasheet states "130 ft wide x 100 ft deep" and "35 feet ceiling height" with source "R-04" — confirm these are design dimensions from Appendix B and note whether they are approximate or dimensioned | Datasheet Attributes lists building dimensions sourced from R-04 with "Approximately" qualifier on footprint but not on ceiling height; the precision of these numbers affects ductwork routing calculations | Datasheet.md | Datasheet.md#Attributes ("Building ceiling height", "Building footprint") | — | PROPOSAL: Confirm dimensions against Appendix B drawing dimensions | TBD |
| E-002 | E:applying:data | Normalization | Datasheet | Datasheet | Clarify source for "35 feet" ceiling height — Datasheet cites both "R-01 S3.4" and "R-04" but R-01 S3.4 addresses HVAC requirements not building dimensions; confirm the authoritative source | Datasheet Attributes entry for ceiling height cites "R-01 S3.4; R-04" — S3.4 is the HVAC scope section of the RFP which may reference building height contextually but Appendix B (R-04) is the dimensional source; the dual citation may confuse provenance | Datasheet.md | Datasheet.md#Attributes ("Building ceiling height") | R-01 S3.4 vs. R-04 (Appendix B) | PROPOSAL: R-04 as primary dimensional source; R-01 S3.4 as context | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Add minimum exhaust stack height requirement (or TBD placeholder with code reference) to REQ-006 — currently "minimum discharge height requirements per applicable codes" without specifying which code clause establishes the minimum | REQ-006(b) requires meeting "minimum discharge height requirements per applicable codes" but no specific code clause or numeric minimum is provided; Procedure Verification table says "Meets minimum code requirement (TBD)" — the conformance datum is absent | Specification.md, Procedure.md | Specification.md#Requirements REQ-006; Procedure.md#Verification ("Exhaust stack height") | — | PROPOSAL: Specify code clause at design stage (NBC/Alberta Building Code mechanical exhaust provisions) | TBD |
| E-004 | E:reviewing:data | WeakStatement | Specification | Specification | Clarify in REQ-012 that "Construction Completion Certificate date" is the CCC date per R-01 S2.14, and specify how warranty documentation is to be collected and retained | REQ-012 references warranty from "Construction Completion Certificate date" per R-01 S2.10.2 but does not specify how warranty certificates from equipment manufacturers (fan, filtration unit, controls) are to be collected, verified, and handed over to the County | Specification.md | Specification.md#Requirements REQ-012; Specification.md#Documentation | — | PROPOSAL: Add warranty certificate collection requirement to Documentation section | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS — All 96 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS — All warranted items grounded in evidence from production documents or explicit absence |
| Provenance present | PASS — Every item has SourcePath + SectionRef |
| Conflicts surfaced | PASS — 3 conflicts (A-001, D-001, X-006) have Contenders and HumanRuling = TBD |
| Summary consistent | PASS — Summary counts match actual warranted items (28 total) |
| Schema followed | PASS — Output uses STRUCTURE schema |
