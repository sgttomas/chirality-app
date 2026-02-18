# Semantic Lensing Register: DEL-02-05 Mechanical, Plumbing, Ventilation & Exhaust

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-05_Mechanical, Plumbing, Ventilation & Exhaust/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-02-05 identity, description, scope (SOW-0204, SOW-0213, SOW-0214, SOW-0223, SOW-0230)
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- All 7 matrices parsed (A, B, C, F, D, X, E); 92 cells total
- Datasheet.md -- Identification, Attributes (HVAC, Plumbing, Compressed Air), Conditions, Construction, References
- Specification.md -- Scope, Requirements REQ-M-01 through REQ-M-14, Standards, Verification, Documentation
- Guidance.md -- Purpose, Principles P-01 through P-06, Considerations C-01 through C-05, Trade-offs T-01 through T-03, Conflict Table
- Procedure.md -- Prerequisites, Steps Phases A through E, Verification, Records
- _REFERENCES.md -- OSR Appendix A, Addendum 03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 4
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 5
- By matrix:
  - A: 6  B: 4  C: 4  F: 3  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards table references unconfirmed codes |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Compressed air scope boundary unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC/ASHRAE not directly read; compliance claims assumption-based |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | AHJ review referenced but no audit procedure defined |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear phased direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps A-1 through E-4 cover execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing quantitative pass criteria for ventilation commissioning |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure covers audit trail needs |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-06 addresses 50-year design life value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T-01 through T-03 address merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No lifecycle cost or value-for-money criteria documented |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning verification covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm which edition of Alberta Building Code (ABC) and which ASHRAE standards apply; add edition/year to Standards table | The Standards table lists ABC, NBCC, ASHRAE 62.1, ASHRAE 90.1, Alberta Plumbing Code, NFPA 88A, and CSA standards all as "location TBD -- ASSUMPTION: applicable." No edition or year is confirmed, which makes prescriptive direction untraceable. | Specification.md | ## Standards | -- | PROPOSAL: Mechanical Engineer to confirm with AHJ | TBD |
| A-002 | A:normative:applying | Conflict | Multi | TBD | Resolve compressed air system scope boundary: DEL-02-05 (mechanical) vs. DEL-02-02 (firehall systems) | Functional Program references compressed air in apparatus bays; Decomposition maps SOW-0203 to DEL-02-02; Datasheet lists it under DEL-02-05 Attributes. Guidance CON-M-01 already flags this. The conflict is present across documents and requires a human ruling. | Guidance.md; Datasheet.md | Guidance.md#Conflict Table; Datasheet.md#Compressed Air (Coordination Note) | Guidance.md#CON-M-01; Datasheet.md#Compressed Air | PROPOSAL: Treat compressed air as DEL-02-05 lead per Guidance CON-M-01 proposal | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify compliance determination method for standards marked "location TBD -- ASSUMPTION: applicable" | Seven standards are listed but none are confirmed as directly applicable. Compliance determination against unconfirmed standards cannot be definitive. The phrase "ASSUMPTION: applicable" does not establish a binding compliance basis. | Specification.md | ## Standards | -- | PROPOSAL: Specification | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or checkpoint for AHJ pre-submission review / code compliance pre-check before permit application (Phase C) | Procedure references AHJ permit submission (C-2) but does not include a pre-submission compliance self-audit step. Regulatory audit preparedness is absent. | Procedure.md | ## Steps > Phase C | -- | PROPOSAL: Procedure | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative pass criteria for apparatus bay exhaust commissioning (e.g., capture velocity, air flow rate, or CO concentration threshold) | Verification table for REQ-M-02/03 says "system capacity calculation; commissioning test" but does not define what constitutes a pass. Without measurable criteria, performance assessment is subjective. | Specification.md | ## Verification (REQ-M-02/03 row) | -- | PROPOSAL: Specification | TBD |
| A-006 | A:evaluative:judging | MissingSlot | Guidance | Guidance | Add lifecycle cost or value-for-money evaluation criteria for mechanical system selection (e.g., comparison framework for HVAC system types or exhaust system types) | Guidance T-01 discusses capital cost vs. operational flexibility for exhaust systems but provides no structured evaluation method. Worth determination has no defined criteria. | Guidance.md | ## Trade-offs > T-01 | -- | PROPOSAL: Guidance | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Climate design data missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references are adequate for data provenance |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing fixture count data |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data values are internally consistent |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Heating fuel type assumed, not confirmed |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each system is adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope in/out documented comprehensively |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design principles adequately communicated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Professional registration requirements stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of sub-systems is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Sump interceptor requirement not confirmed |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs show adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-discipline coordination noted throughout |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add outdoor design conditions for Penhold, Alberta (heating/cooling design temperatures, degree days) to the Datasheet Attributes | Procedure step A-1 requires establishing outdoor design conditions, but no climate data values are recorded in the Datasheet. This is an essential fact for HVAC load calculations. | Datasheet.md | ## Attributes > HVAC -- Main Building | -- | PROPOSAL: Datasheet | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add plumbing fixture count basis or reference fixture schedule by space type to the Datasheet | Procedure step A-6 requires developing a fixture count and confirming code minimums, but no fixture data exists in the Datasheet. The comprehensive record of plumbing facts is incomplete. | Datasheet.md | ## Attributes > Plumbing | -- | PROPOSAL: Datasheet | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Datasheet | Record TBD: Confirm heating fuel source (natural gas assumed per Addendum 03 section 1.6 mention of gas proximity; not explicitly stated as design fuel) | Procedure step A-2 assumes natural gas but the ASSUMPTION label indicates this is not confirmed. Fuel source is an essential signal for HVAC system selection. | Procedure.md; Datasheet.md | Procedure.md#Phase A > A-2; Datasheet.md#entire document scanned | -- | PROPOSAL: Confirm with Owner / utility provider | TBD |
| B-004 | B:wisdom:necessity | TBD_Question | Multi | Specification | Record TBD: Confirm with Town of Penhold AHJ whether oil/water interceptors are required for bay sump drainage | Guidance P-04 notes interceptor requirements are assumed to be governed by local municipal utility authority but not confirmed. This essential discernment point requires external input before sump design can proceed. | Guidance.md; Specification.md | Guidance.md#P-04; Specification.md#REQ-M-06 | -- | PROPOSAL: Design-Builder to confirm with AHJ during permitting | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 1 | HAS_ITEMS | Obligations stated but enforcement mechanism unclear for some |
| C:normative:sufficiency | normative | sufficiency | Defensible Conformance | 1 | HAS_ITEMS | Conformance defense weakened by unconfirmed standards |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 0 | NO_ITEMS | Requirements REQ-M-01 through REQ-M-14 cover all identified scope items |
| C:normative:consistency | normative | consistency | Coherent Regulatory Alignment | 0 | NO_ITEMS | Requirements are internally coherent |
| C:operative:necessity | operative | necessity | Essential Operational Capacity | 1 | HAS_ITEMS | Missing prerequisite for PW bay count confirmation |
| C:operative:sufficiency | operative | sufficiency | Competent Execution Basis | 0 | NO_ITEMS | Execution basis is sufficient in Procedure |
| C:operative:completeness | operative | completeness | Complete Operational Scope | 0 | NO_ITEMS | Procedure covers all scope items through phases A-E |
| C:operative:consistency | operative | consistency | Stable Process Reliability | 0 | NO_ITEMS | Process is consistent across phases |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 1 | HAS_ITEMS | No acceptance criteria for energy efficiency |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Basis | 0 | NO_ITEMS | Value basis is adequate through trade-off discussion |
| C:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting covered through commissioning |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value principles are consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-M-01 from "adequate ventilation" to include a reference to specific code section or ventilation rate standard (e.g., ASHRAE 62.1 minimum rates) | REQ-M-01 uses "adequate ventilation per applicable building code" which is an enforceable obligation in principle but lacks specificity. The word "adequate" without a quantified threshold is a weak statement for a binding requirement. | Specification.md | ## Requirements > REQ-M-01 | -- | PROPOSAL: Specification | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-M-04 "adequate ventilation to accommodate occasional short-term vehicle idling and very occasional welding" by adding ventilation rate or air changes per hour target | REQ-M-04 uses performance language ("adequate," "occasional," "very occasional") that does not constitute defensible conformance without quantified criteria. The Design-Builder cannot demonstrate sufficiency without a measurable target. | Specification.md | ## Requirements > REQ-M-04 | -- | PROPOSAL: Specification | TBD |
| C-003 | C:operative:necessity | RationaleGap | Procedure | Guidance | Add rationale for PW bay count assumption (four bays) and document the dependency on DEL-02-03 confirmation | Procedure step A-7 states "ASSUMPTION: four PW bays based on SOW-0211; confirm exact count with DEL-02-03." This is an essential operational capacity question that affects sump count (currently assumed at 8 total). The rationale for assuming four PW bays is not explained. | Procedure.md | ## Steps > Phase A > A-7 | -- | PROPOSAL: Guidance | TBD |
| C-004 | C:evaluative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for HVAC energy efficiency (ASHRAE 90.1 or equivalent) if applicable | Standards table lists ASHRAE 90.1 as likely applicable but no requirement or verification entry references energy efficiency. If energy efficiency is a fundamental worth criterion, it needs a corresponding requirement and verification approach. | Specification.md | ## Standards; ## Verification | -- | PROPOSAL: Specification | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Regulatory Imperative | 0 | NO_ITEMS | Regulatory imperatives captured in REQ-M-01 through REQ-M-14 |
| F:normative:sufficiency | normative | sufficiency | Justified Regulatory Threshold | 1 | HAS_ITEMS | Threshold values missing for several requirements |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 0 | NO_ITEMS | All identified compliance areas covered |
| F:normative:consistency | normative | consistency | Uniform Compliance Integrity | 0 | NO_ITEMS | Requirements use consistent structure |
| F:operative:necessity | operative | necessity | Indispensable Readiness | 1 | HAS_ITEMS | Prerequisites missing status for some upstream deliverables |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Adequacy | 0 | NO_ITEMS | Procedure adequately demonstrates execution path |
| F:operative:completeness | operative | completeness | Total Operational Assurance | 0 | NO_ITEMS | All operational phases covered |
| F:operative:consistency | operative | consistency | Predictable Process Discipline | 0 | NO_ITEMS | Process is predictable and well-structured |
| F:evaluative:necessity | evaluative | necessity | Irreducible Quality Standard | 1 | HAS_ITEMS | No minimum equipment quality/grade requirement stated |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Merit Basis | 0 | NO_ITEMS | Merit basis is demonstrated through trade-offs |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Synthesis | 0 | NO_ITEMS | Worth synthesis covered across Guidance and Specification |
| F:evaluative:consistency | evaluative | consistency | Coherent Quality Discipline | 0 | NO_ITEMS | Quality discipline is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add quantified ventilation rate thresholds for PW bay ventilation (REQ-M-04) and bunker gear room ventilation (REQ-M-05) | Requirements REQ-M-04 and REQ-M-05 use "adequate ventilation" without thresholds. Justified regulatory threshold requires measurable pass/fail criteria to determine if the regulatory bar has been met. | Specification.md | ## Requirements > REQ-M-04, REQ-M-05; ## Verification | -- | PROPOSAL: Specification | TBD |
| F-002 | F:operative:necessity | Normalization | Procedure | Multi | Normalize prerequisite status values: Procedure uses "Available," "Required before...," and "Obtain from..." inconsistently for prerequisite readiness status | The prerequisites table mixes availability statements ("Available") with dependency statements ("Required before...") and action items ("Obtain from AHJ"). A uniform status vocabulary would improve readiness tracking. | Procedure.md | ## Prerequisites > Information Prerequisites | -- | PROPOSAL: Procedure and Datasheet | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale for minimum equipment quality expectations (e.g., equipment grade, warranty duration, local serviceability requirements) in context of 50-year design life | Guidance P-06 mentions maintainability and locally-serviceable products but does not establish an irreducible quality standard for equipment selection. What minimum quality floor applies? | Guidance.md | ## Principles > P-06 | -- | PROPOSAL: Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Prescriptive Authority | 0 | NO_ITEMS | Authority is settled via OSR and Addendum references |
| D:normative:applying | normative | applying | Justified Mandatory Compliance | 1 | HAS_ITEMS | REQ-M-13 generator interface is ASSUMPTION-based |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Verification table provides conformance pathways |
| D:normative:reviewing | normative | reviewing | Systematic Conformance Review | 0 | NO_ITEMS | Review mechanisms adequately defined |
| D:operative:guiding | operative | guiding | Established Process Governance | 0 | NO_ITEMS | Process governance is well-established |
| D:operative:applying | operative | applying | Confirmed Operational Action | 1 | HAS_ITEMS | Missing confirmation of bay door HVAC interface |
| D:operative:judging | operative | judging | Definitive Performance Judgment | 0 | NO_ITEMS | Performance judgment criteria in Verification table |
| D:operative:reviewing | operative | reviewing | Confirmed Process Scrutiny | 0 | NO_ITEMS | Phase-gate reviews implied through milestone submissions |
| D:evaluative:guiding | evaluative | guiding | Established Value Principle | 0 | NO_ITEMS | Value principles well-established in Guidance |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Delivery | 0 | NO_ITEMS | Merit delivery tracked through artifact list |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 1 | HAS_ITEMS | No evaluation criteria for proposal Mechanical Design Brief |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Appraisal | 0 | NO_ITEMS | Quality appraisal covered through commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-M-13 from ASSUMPTION to confirmed requirement or record as TBD pending DEL-02-07 coordination | REQ-M-13 (generator interface) is labeled ASSUMPTION but written as a "shall" requirement. This creates ambiguity about whether it is mandatory. If it is mandatory, the ASSUMPTION label should be removed after confirmation. If unconfirmed, the "shall" language is premature. | Specification.md | ## Requirements > REQ-M-13 | -- | PROPOSAL: Specification | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add a step for bay door / HVAC interlock coordination (exhaust system and bay door operation sequence) referencing DEL-02-04 and DEL-02-07 | Guidance P-01 notes "System integration with bay door operation (doors open before apparatus moves)." Procedure D-3 mentions "bay exhaust system integration with bay door operation" in construction phase but no design-phase step addresses this interlock design. The confirmed operational action of designing the interlock is missing from Phase A or B. | Guidance.md; Procedure.md | Guidance.md#P-01; Procedure.md#Phase D > D-3 | -- | PROPOSAL: Procedure (add to Phase A or B) | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add evaluation criteria for the Mechanical Design Brief (REQ-M-14) -- what constitutes a passing proposal submission | REQ-M-14 requires a Mechanical Design Brief for proposal submission, and Verification says "Included in proposal submission per RFP 7.1.2." This is a presence check only; no qualitative evaluation criteria exist for judging the brief's worth. | Specification.md | ## Requirements > REQ-M-14; ## Verification | -- | PROPOSAL: Specification or Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Imperative | 0 | NO_ITEMS | Foundational directives adequately captured |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Governance Assurance | 0 | NO_ITEMS | Governance assurance is sufficient |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 1 | HAS_ITEMS | Directive scope missing decontamination area ventilation |
| X:guiding:consistency | guiding | consistency | Harmonized Governance Standard | 0 | NO_ITEMS | Governance is harmonized |
| X:applying:necessity | applying | necessity | Mandatory Execution Practice | 1 | HAS_ITEMS | No mandatory hold/witness points defined |
| X:applying:sufficiency | applying | sufficiency | Competent Applied Sufficiency | 0 | NO_ITEMS | Applied sufficiency is adequate |
| X:applying:completeness | applying | completeness | Comprehensive Applied Coverage | 0 | NO_ITEMS | Applied coverage is comprehensive |
| X:applying:consistency | applying | consistency | Stable Implementation Practice | 0 | NO_ITEMS | Implementation practice is stable |
| X:judging:necessity | judging | necessity | Binding Determination Basis | 1 | HAS_ITEMS | Missing commissioning acceptance standard |
| X:judging:sufficiency | judging | sufficiency | Justified Determination Finding | 0 | NO_ITEMS | Determination findings are justified |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Scope | 0 | NO_ITEMS | Judgment scope is exhaustive |
| X:judging:consistency | judging | consistency | Consistent Judgment Standard | 0 | NO_ITEMS | Judgment standard is consistent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Examination Basis | 1 | HAS_ITEMS | No as-built vs. design comparison requirement |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Verification Basis | 0 | NO_ITEMS | Verification basis is adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Examination Scope | 0 | NO_ITEMS | Examination scope is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Coherent Oversight Discipline | 0 | NO_ITEMS | Oversight discipline is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add a requirement or scope note for decontamination area ventilation (negative pressure, exhaust, chemical vapor management) | Guidance C-04 discusses bunker gear room ventilation in decontamination context and mentions negative pressure, but no explicit requirement exists in Specification for the decontamination area itself. The directive scope for ventilation is incomplete without addressing this space. | Specification.md; Guidance.md | Specification.md#entire document scanned; Guidance.md#C-04 | -- | PROPOSAL: Specification | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add mandatory hold/witness points for critical inspections (e.g., exhaust duct pressure test, sump waterproofing inspection, plumbing rough-in) | Procedure Phase D references "coordinate rough-in inspections with AHJ" but does not define mandatory hold points for the Design-Builder's own QA/QC process. Mandatory execution practice requires defined pause points. | Procedure.md | ## Steps > Phase D | -- | PROPOSAL: Procedure | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add a reference to a commissioning standard or protocol (e.g., ASHRAE Guideline 0, or project-specific Cx specification) for mechanical systems commissioning | Verification table references commissioning tests and balancing but does not cite a commissioning standard. A binding determination basis requires a reference standard to judge pass/fail. | Specification.md | ## Verification | -- | PROPOSAL: Specification | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Specification | Add requirement for as-built drawing comparison against IFC design documents as a mandatory examination step | Procedure Records table lists "As-Built Drawings -- Mechanical" at closeout but no verification step confirms as-built accuracy against IFC design. Mandatory examination basis is incomplete without this review step. | Procedure.md; Specification.md | Procedure.md#Records; Specification.md#Verification | -- | PROPOSAL: Procedure (add to Phase E) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Sovereign Compliance Mandate | 1 | HAS_ITEMS | Fire code compliance for exhaust not explicitly referenced |
| E:normative:sufficiency | normative | sufficiency | Confirmed Regulatory Sufficiency | 0 | NO_ITEMS | Regulatory sufficiency is confirmed through AHJ permit process |
| E:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | Regulatory completeness is addressed across requirements |
| E:normative:consistency | normative | consistency | Unified Regulatory Coherence | 0 | NO_ITEMS | Regulatory coherence is unified |
| E:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | No indoor air quality monitoring requirement |
| E:operative:sufficiency | operative | sufficiency | Adequate Operational Competence | 0 | NO_ITEMS | Operational competence is adequate |
| E:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 0 | NO_ITEMS | Operational coverage is exhaustive |
| E:operative:consistency | operative | consistency | Principled Operational Stability | 0 | NO_ITEMS | Operational stability is principled |
| E:evaluative:necessity | evaluative | necessity | Irreducible Value Imperative | 1 | HAS_ITEMS | No noise/vibration criteria for HVAC equipment |
| E:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Sufficiency | 0 | NO_ITEMS | Merit sufficiency is justified |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Worth Accounting | 0 | NO_ITEMS | Worth accounting is comprehensive |
| E:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality coherence is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | Normalization | Specification | Specification | Normalize fire code references: REQ-M-02 references "direct exhaust ventilation" but does not cite the applicable fire code section (NFPA 1500, NFPA 1581, or Alberta fire code equivalent) governing fire station apparatus bay ventilation | The sovereign compliance mandate for fire apparatus bay exhaust should reference the governing fire code, not just the OSR. Standards table lists NFPA 88A (parking structures) but not NFPA 1500/1581 (fire department occupational safety / infection control), which are more directly applicable. | Specification.md | ## Requirements > REQ-M-02; ## Standards | -- | PROPOSAL: Specification (Standards table and REQ-M-02) | TBD |
| E-002 | E:operative:necessity | RationaleGap | Guidance | Guidance | Add consideration for indoor air quality (IAQ) monitoring or CO detection in apparatus bays and PW bays as a critical operational prerequisite | Apparatus bays handle diesel exhaust (carcinogenic); PW bays handle welding fumes. No requirement or guidance addresses IAQ monitoring, CO/NO2 detection, or alarm systems. This is a critical operational prerequisite for occupant safety. | Guidance.md; Specification.md | Guidance.md#P-01; Specification.md#entire document scanned | -- | PROPOSAL: Guidance (consideration) and Specification (if required by code) | TBD |
| E-003 | E:evaluative:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm whether noise or vibration criteria apply to HVAC equipment selection (adjacent sleeping quarters for fire department personnel) | The facility includes sleeping areas for firefighters. HVAC equipment noise and vibration may affect occupant comfort and operational readiness. No noise criteria or equipment vibration limits are documented anywhere. This is an irreducible value imperative for a fire station with 24-hour occupancy. | Datasheet.md; Specification.md | Datasheet.md#entire document scanned; Specification.md#entire document scanned | -- | PROPOSAL: Confirm with Owner whether noise criteria are required | TBD |
