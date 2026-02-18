# Semantic Lensing Register: DEL-02-04 Mechanical Concept Narrative

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-04_MechanicalConceptNarrative
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-02-04_MechanicalConceptNarrative/_CONTEXT.md
- _STATUS.md -- DEL-02-04_MechanicalConceptNarrative/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-02-04_MechanicalConceptNarrative/_SEMANTIC.md (7 matrices: A, B, C, F, D, X, E; plus K transpose)
- Datasheet.md -- DEL-02-04_MechanicalConceptNarrative/Datasheet.md (present)
- Specification.md -- DEL-02-04_MechanicalConceptNarrative/Specification.md (present)
- Guidance.md -- DEL-02-04_MechanicalConceptNarrative/Guidance.md (present)
- Procedure.md -- DEL-02-04_MechanicalConceptNarrative/Procedure.md (present)
- _REFERENCES.md -- DEL-02-04_MechanicalConceptNarrative/_REFERENCES.md (present)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 2
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code standard identification gaps |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Generator fuel type undetermined |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ interaction method not specified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification matrix covers audit adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Cold Storage ventilation approach vague |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing airflow rate targets |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Phase A/B checklists cover process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance principles address value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | OBJ-003 alignment clear |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-001 through T-004 address this |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC checklists in Procedure adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of Alberta Building Code (ABC) is assumed (e.g., ABC 2019 or ABC 2023) and which edition of NECB is targeted; current text says "ASSUMPTION: applicable" without edition | Multiple requirements (R-MEL-11, R-MEL-25, R-MEL-17) cite Alberta Building Code as a prescriptive authority but no edition is identified; this makes compliance determination ambiguous | Specification.md | Standards section; R-MEL-11, R-MEL-25 | -- | Specification | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: confirm whether natural gas service is confirmed available at site boundary for generator fuel selection (Addendum 03 ss1.6 says "within a few feet" but formal confirmation needed) | Generator fuel type (natural gas vs. diesel) affects sizing, installation, and permitting; Addendum 03 ss1.6 context is informal and site utility confirmation is not yet documented | Datasheet.md | TBD Summary; Construction > Backup Generator | -- | Datasheet | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add a requirement or note specifying how and when AHJ pre-consultation for fire protection (R-MEL-27) will be initiated; current text states "AHJ approval is permit prerequisite" but no mechanism for early engagement at concept stage | Compliance determination for fire protection (wet vs. dry sprinkler) depends on AHJ preference; deferring AHJ contact entirely to design phase risks late-stage design changes | Specification.md | R-MEL-27 Notes; Verification section | -- | Specification | TBD |
| A-004 | A:operative:applying | WeakStatement | Datasheet | Guidance | Clarify Cold Storage ventilation concept: "adequate ventilation or alternate air circulation" is restated from RFP ss11.1.2 without further specificity; add whether passive ridge/soffit ventilation, ceiling fans, or mechanical exhaust is the baseline concept approach | Cold Storage ventilation is listed as REQUIRED in Datasheet and has a CONSTRAINT requirement (R-MEL-09) but the concept approach in Datasheet Construction section says "ventilation openings or ceiling fans" without committing to a direction | Datasheet.md; Specification.md | Datasheet > Construction > Cold Storage Ventilation; Specification R-MEL-09 | -- | Guidance | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for airflow rates: apparatus bay exhaust (CFM per bay), PW bay ventilation (air changes per hour), bunker gear room exhaust (CFM or ACH), decontamination area ventilation (ACH); current requirements state function but not measurable performance targets | R-MEL-01, R-MEL-04, R-MEL-06, R-MEL-08c specify ventilation functions but do not include quantified airflow targets against which performance can be assessed; verification methods reference "performance test" and "air balance" but no pass criteria | Specification.md | R-MEL-01, R-MEL-04, R-MEL-06, R-MEL-08c; Verification section | -- | Specification | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | SCBA temperature range missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Kitchen room size TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet is thorough in listing systems and zones |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Generator sizing inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals from Addendum 03 are embedded |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each system adequate at concept stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Systems enumeration complete |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design understanding demonstrated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Concept-level expertise adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of systems is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is internally coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Principles and trade-offs show discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance judgment adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: obtain SCBA cylinder manufacturer or NFPA specification for acceptable storage temperature range; current text labels this as ASSUMPTION without a numeric range | SCBA room climate control (R-MEL-10a) is a CONSTRAINT requirement but no temperature range is stated; this essential fact is needed to size the HVAC supply to the SCBA room | Datasheet.md; Specification.md | Datasheet > Conditions > SCBA Cylinder Temperature Sensitivity; Specification R-MEL-10a | -- | Datasheet | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Add approximate room sizes for Kitchen (TBD), ICP/Meeting Room (TBD), Office Areas (TBD), and Residential Quarters (TBD) or explicitly cross-reference the Functional Program row providing this data | Several zones in the Building Zones table list size as "TBD (Functional Program row X.0)" without providing the actual values from the Functional Program; adequate evidence for HVAC sizing depends on these | Datasheet.md | Attributes > Building Zones Requiring Mechanical Design | -- | Datasheet | TBD |
| B-003 | B:data:consistency | Conflict | Multi | Specification | Resolve generator sizing estimate inconsistency: Datasheet Construction table says "25-30 kW (ASSUMPTION)"; Specification R-MEL-24 says "25-30 kW"; Guidance EX-002 estimates design load at 16,000-25,000 W and recommends "25 kW unit as concept baseline"; Guidance C-002 Option 1 says "~20-25 kW" for minimum loads | The generator capacity figures vary across documents (20-25 kW vs. 25-30 kW vs. 25 kW baseline); while ranges overlap, they are not identical and could cause confusion in design phase load calculations | Datasheet.md; Specification.md; Guidance.md | Datasheet > Construction > Backup Generator; Specification R-MEL-24; Guidance C-002; Guidance EX-002 | Datasheet.md#Construction > Backup Generator (25-30 kW); Guidance.md#C-002 (20-25 kW for minimum); Guidance.md#EX-002 (25 kW baseline) | Specification | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | Fire code edition gap |
| C:normative:sufficiency | normative | sufficiency | Compliance Substantiation | 0 | NO_ITEMS | Substantiation approach documented in Verification |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Noise bylaw gap |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Order | 0 | NO_ITEMS | Regulatory references are consistent |
| C:operative:necessity | operative | necessity | Operational Foundation | 0 | NO_ITEMS | Operational prerequisites documented |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Capability demonstrated at concept level |
| C:operative:completeness | operative | completeness | Thorough Operational Delivery | 0 | NO_ITEMS | Procedure phases cover delivery |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process discipline addressed in checklists |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth | 0 | NO_ITEMS | Value proposition clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit | 1 | HAS_ITEMS | Missing lifecycle cost basis |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Appraisal | 0 | NO_ITEMS | Trade-offs provide comprehensive view |
| C:evaluative:consistency | evaluative | consistency | Principled Value Judgment | 0 | NO_ITEMS | Value judgments principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add reference to applicable fire code standard for fire protection system design (e.g., NFPA 13 or equivalent Canadian standard adopted in Alberta) alongside Alberta Building Code reference | R-MEL-25, R-MEL-26, R-MEL-27 reference Alberta Building Code for fire protection but do not identify the specific fire protection design standard (NFPA 13 or equivalent); this is a regulatory imperative gap for sprinkler system design | Specification.md | R-MEL-25, R-MEL-26; Standards section | -- | Specification | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add note about Town of Penhold noise bylaws and generator exhaust emissions requirements as applicable constraints; currently listed as "TBD in design phase" in Standards without a corresponding requirement | Datasheet Conditions and Specification Standards both mention Town of Penhold Bylaws for "utility connections, noise, emissions" as TBD; an outdoor generator has noise and emissions implications that should be tracked as a constraint even if resolution is deferred | Specification.md; Datasheet.md | Specification > Standards > Town of Penhold Bylaws; Datasheet > Conditions > Reference Design Standards | -- | Specification | TBD |
| C-003 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for the 50-year lifecycle cost claim in T-001 (HVAC efficiency vs. first cost); currently states "almost always favors the efficiency premium" without presenting a basis, even a rough order-of-magnitude comparison | Trade-off T-001 asserts lifecycle cost advantage for high-efficiency equipment but provides no quantified basis; substantiating merit requires at least a rough comparison to be credible at concept stage | Guidance.md | Trade-offs > T-001 | -- | Guidance | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Criterion | 1 | HAS_ITEMS | Backflow preventer type unspecified |
| F:normative:sufficiency | normative | sufficiency | Regulatory Burden of Proof | 0 | NO_ITEMS | Verification matrix provides proof approach |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Addendum 03 coverage complete per checklist |
| F:normative:consistency | normative | consistency | Uniform Compliance Standard | 0 | NO_ITEMS | Standards references uniform |
| F:operative:necessity | operative | necessity | Operational Readiness Baseline | 1 | HAS_ITEMS | Missing freeze protection verification |
| F:operative:sufficiency | operative | sufficiency | Validated Execution Capacity | 0 | NO_ITEMS | Execution capacity adequate at concept level |
| F:operative:completeness | operative | completeness | Complete Operational Mastery | 0 | NO_ITEMS | Operational coverage thorough |
| F:operative:consistency | operative | consistency | Consistent Operational Rigor | 0 | NO_ITEMS | Consistent rigor in procedures |
| F:evaluative:necessity | evaluative | necessity | Essential Value Criterion | 1 | HAS_ITEMS | Missing OBJ-004 scoring linkage |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Value Justification | 0 | NO_ITEMS | Justification grounded in trade-offs |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Assessment | 0 | NO_ITEMS | Assessment thorough in Guidance |
| F:evaluative:consistency | evaluative | consistency | Coherent Value Standard | 0 | NO_ITEMS | Value standard coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify R-MEL-15: specify that backflow prevention device type (RPZ vs. PVB vs. DCVA) will be confirmed with AHJ, and note that RPZ is typical for fire service connections; current text says "type per AHJ requirement TBD" without distinguishing between domestic and fire protection service entries | R-MEL-15 addresses domestic water backflow prevention and R-MEL-26 addresses fire protection connection; both need backflow prevention but the types may differ; this mandatory compliance criterion is underspecified | Specification.md | R-MEL-15; R-MEL-26 | -- | Specification | TBD |
| F-002 | F:operative:necessity | VerificationGap | Specification | Specification | Add verification criteria for freeze protection of water piping (R-MEL-17): specify that commissioning must include a freeze-protection inspection of all piping in exterior walls, unheated spaces, and sump discharge lines before first winter operation | R-MEL-17 requires freeze protection for water piping but the Verification matrix does not include a specific freeze-protection inspection; this operational readiness baseline item could be missed during commissioning | Specification.md | R-MEL-17; Verification section (R-MEL-14 through R-MEL-17 group) | -- | Specification | TBD |
| F-003 | F:evaluative:necessity | MissingSlot | Guidance | Guidance | Add explicit linkage between mechanical system selections and OBJ-004 (Sustainability and Energy, 15 pts) scoring criteria; Guidance references OBJ-004 in P-003 but does not connect specific system choices to scoring rubric elements | OBJ-004 is a 15-point evaluation criterion; Guidance P-003 references it but the trade-offs and considerations do not explicitly map mechanical choices to scoring criteria, making it harder to optimize the proposal for evaluator priorities | Guidance.md | P-003; Trade-offs section | -- | Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Direction | 0 | NO_ITEMS | Compliance direction adequate |
| D:normative:applying | normative | applying | Obligatory Conformance Practice | 0 | NO_ITEMS | Conformance practices identified |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance rulings deferred to AHJ appropriately |
| D:normative:reviewing | normative | reviewing | Standardized Regulatory Scrutiny | 0 | NO_ITEMS | Verification matrix provides scrutiny framework |
| D:operative:guiding | operative | guiding | Operational Governance Benchmark | 1 | HAS_ITEMS | Missing commissioning agent engagement timing |
| D:operative:applying | operative | applying | Verified Practical Implementation | 0 | NO_ITEMS | Implementation approach verified at concept level |
| D:operative:judging | operative | judging | Definitive Performance Verdict | 0 | NO_ITEMS | Performance assessment deferred appropriately to design |
| D:operative:reviewing | operative | reviewing | Systematic Process Assurance | 1 | HAS_ITEMS | Missing QC reviewer identification |
| D:evaluative:guiding | evaluative | guiding | Established Value Direction | 0 | NO_ITEMS | Value direction established in principles |
| D:evaluative:applying | evaluative | applying | Realized Value Commitment | 0 | NO_ITEMS | Value commitments realized in trade-offs |
| D:evaluative:judging | evaluative | judging | Definitive Worth Verdict | 0 | NO_ITEMS | Worth determination through trade-off analysis |
| D:evaluative:reviewing | evaluative | reviewing | Integrated Quality Review | 0 | NO_ITEMS | Quality review covered by checklists |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add a step or note in Phase B specifying when the commissioning agent should be engaged (e.g., at design kickoff or by 60% design); current verification references a "Commissioning Agent" but no procedure step addresses engagement timing | Operational governance for commissioning depends on early engagement; the Verification section references "Commissioning Agent" for multiple system tests but Phase B does not include a commissioning agent engagement step until the implied end of process | Procedure.md | Phase B steps; Verification section | -- | Procedure | TBD |
| D-002 | D:operative:reviewing | RationaleGap | Procedure | Procedure | Clarify who performs the Phase A QC review sign-off: the Procedure Records mention "Proposal Manager or QC lead" but no prior step identifies who the QC reviewer is or what their qualifications should be | Systematic process assurance requires a defined reviewer; the QC review step (A6) references "quality check" and the Records mention "QC lead sign-off" but no step identifies the reviewer or whether they are independent of the authoring Mechanical Engineer | Procedure.md | Step A6; Records > Phase A Records | -- | Procedure | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Authority | 0 | NO_ITEMS | Directive authority established |
| X:guiding:sufficiency | guiding | sufficiency | Guided Sufficiency Assurance | 0 | NO_ITEMS | Sufficiency guidance adequate |
| X:guiding:completeness | guiding | completeness | Complete Governance Scope | 0 | NO_ITEMS | Governance scope complete |
| X:guiding:consistency | guiding | consistency | Principled Governance Coherence | 0 | NO_ITEMS | Governance coherent |
| X:applying:necessity | applying | necessity | Essential Implementation Mandate | 1 | HAS_ITEMS | Water fill station verification gap |
| X:applying:sufficiency | applying | sufficiency | Proven Practice Adequacy | 0 | NO_ITEMS | Practice adequacy demonstrated |
| X:applying:completeness | applying | completeness | Exhaustive Practice Coverage | 1 | HAS_ITEMS | Missing laundry set verification |
| X:applying:consistency | applying | consistency | Standardized Practice Integrity | 0 | NO_ITEMS | Practice integrity consistent |
| X:judging:necessity | judging | necessity | Critical Adjudication Basis | 1 | HAS_ITEMS | Missing pass/fail for cold storage |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment | 0 | NO_ITEMS | Judgment substantiated |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope comprehensive |
| X:judging:consistency | judging | consistency | Uniform Adjudication Standard | 1 | HAS_ITEMS | Terminology inconsistency |
| X:reviewing:necessity | reviewing | necessity | Compulsory Audit Foundation | 0 | NO_ITEMS | Audit foundation established |
| X:reviewing:sufficiency | reviewing | sufficiency | Verified Audit Adequacy | 0 | NO_ITEMS | Audit adequacy verified |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Coverage | 0 | NO_ITEMS | Audit coverage comprehensive |
| X:reviewing:consistency | reviewing | consistency | Principled Audit Discipline | 0 | NO_ITEMS | Audit discipline principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add specific verification acceptance criteria for water fill stations (R-MEL-14): confirm 2" minimum diameter measurement, ground-level installation check, and flow rate test; current verification groups R-MEL-14 with R-MEL-15 through R-MEL-17 without station-specific acceptance test | Water fill stations are a critical Addendum 03 requirement (ss1.16) with specific physical attributes (2" minimum, ground level, female coupling); the verification matrix bundles them with general plumbing without explicit station-specific acceptance criteria | Specification.md | Verification section (R-MEL-14 through R-MEL-17 group) | -- | Specification | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification step for laundry set and dishwasher plumbing connections: hot/cold water supply, drain connections, and hot water capacity test for simultaneous laundry + decontamination + kitchen demand | OSR ss12.6 appliance list includes dishwasher and 2 laundry sets with plumbing requirements; the Verification matrix does not explicitly verify these connections or confirm hot water capacity under combined peak demand | Specification.md | Verification section; R-MEL-16 | -- | Specification | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add measurable acceptance criterion for Cold Storage ventilation (R-MEL-09): define what "adequate ventilation to prevent condensation and icing" means in verifiable terms (e.g., maximum relative humidity, absence of visible condensation/ice after 72 hours in winter) | R-MEL-09 verification includes "condensation/icing monitoring first winter" but no pass/fail criterion is defined; without a threshold, the critical adjudication basis for this requirement is absent | Specification.md | Verification section (R-MEL-09); R-MEL-09 | -- | Specification | TBD |
| X-004 | X:judging:consistency | Normalization | Multi | Guidance | Standardize terminology for PW bays: Datasheet uses "Public Works Equipment Bays (Workshop Bays)" and "PW bay"; Specification uses "Public Works equipment bays" and "PW bay"; Procedure uses "workshop bays" and "PW bay"; Guidance uses "PW bays"; room sizing table in Addendum 03 uses "Workshop/Storage Bay" | Inconsistent naming for the same space across documents could cause confusion in cross-discipline coordination; a single canonical term should be established | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet > Attributes > Building Zones (Public Works Equipment Bays); Specification R-MEL-04 (Public Works equipment bays); Procedure Step A1 (Workshop/Storage Bay) | -- | Guidance | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Regulatory Authority | 0 | NO_ITEMS | Covered under A and C lenses |
| E:normative:sufficiency | normative | sufficiency | Mandated Sufficiency Assurance | 0 | NO_ITEMS | Sufficiency assurance in verification |
| E:normative:completeness | normative | completeness | Absolute Regulatory Completeness | 1 | HAS_ITEMS | Missing drainage code reference |
| E:normative:consistency | normative | consistency | Systematic Regulatory Integrity | 0 | NO_ITEMS | Regulatory integrity consistent |
| E:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites documented in Procedure |
| E:operative:sufficiency | operative | sufficiency | Validated Performance Sufficiency | 0 | NO_ITEMS | Sufficiency validated at concept level |
| E:operative:completeness | operative | completeness | Exhaustive Operational Assurance | 0 | NO_ITEMS | Operational assurance exhaustive |
| E:operative:consistency | operative | consistency | Dependable Operational Consistency | 1 | HAS_ITEMS | Sump discharge terminology |
| E:evaluative:necessity | evaluative | necessity | Foundational Value Imperative | 0 | NO_ITEMS | Value imperative established |
| E:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Sufficiency | 0 | NO_ITEMS | Merit sufficiency justified |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Value Assessment | 0 | NO_ITEMS | Value assessment exhaustive in trade-offs |
| E:evaluative:consistency | evaluative | consistency | Coherent Value Integrity | 0 | NO_ITEMS | Value integrity coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | MissingSlot | Datasheet | Specification | Add reference to Alberta Plumbing Code (or applicable plumbing sub-code of ABC) as a governing standard for all plumbing work; currently only CSA B125 series is mentioned for plumbing standards without the jurisdictional plumbing code | R-MEL-08a, R-MEL-08b, R-MEL-15, R-MEL-18 all involve plumbing installations governed by a plumbing code; the Standards section lists CSA standards but not the jurisdictional plumbing code that governs installation practice | Datasheet.md; Specification.md | Datasheet > Conditions > Reference Design Standards; Specification > Standards | -- | Specification | TBD |
| E-002 | E:operative:consistency | Normalization | Datasheet | Datasheet | Standardize sump discharge options terminology: Datasheet uses "daylight, percolation, or municipal sewer"; Specification R-MEL-19 uses "daylight, percolation field, or municipal sewer"; Guidance C-004 uses "Municipal Sanitary Sewer / Percolation-Infiltration Field / Daylight Discharge"; align to a single set of terms | Three different phrasings for the same sump discharge options appear across documents; while substantively similar, the inconsistency could create confusion in civil coordination | Datasheet.md; Specification.md; Guidance.md | Datasheet > Construction > Bay Sumps; Specification R-MEL-19; Guidance C-004 | -- | Datasheet | TBD |

---

**End of Semantic Lensing Register**
