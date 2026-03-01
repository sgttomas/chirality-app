# Semantic Lensing Register: DEL-011-04 Entrance/Exit Doors

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-011_Building Structure & Envelope/1_Working/DEL-011-04_Doors-Entrances/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-011-04_Doors-Entrances/_CONTEXT.md
- _STATUS.md — DEL-011-04_Doors-Entrances/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-011-04_Doors-Entrances/_SEMANTIC.md
- Datasheet.md — DEL-011-04_Doors-Entrances/Datasheet.md
- Specification.md — DEL-011-04_Doors-Entrances/Specification.md
- Guidance.md — DEL-011-04_Doors-Entrances/Guidance.md
- Procedure.md — DEL-011-04_Doors-Entrances/Procedure.md
- _REFERENCES.md — DEL-011-04_Doors-Entrances/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 1
  - Procedure: 6
  - Multi: 2
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Fire rating and accessibility code clauses TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Installation tolerances unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Occupancy classification TBD affects compliance scope |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | SCO inspection scope not linked to specific reqs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps adequately described |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantified pass/fail criteria for operational test |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records closeout is clear |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose and value adequately stated in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs addressed in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality appraisal covered by operational testing |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality review covered in Procedure verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add specific Alberta Building Code clause references for fire-rating and accessibility requirements once occupancy classification is confirmed in IFC documents | The Specification references ABC/NBC requirements (REQ-011-04-03, REQ-011-04-04) but defers all specific clause numbers to "TBD at design stage"; under the prescriptive direction lens, the governing code edition and applicable clauses should be identified when available to make the prescriptive direction actionable | Specification.md | REQ-011-04-03, REQ-011-04-04, Standards table | -- | DEL-001-11 (Architectural Specification) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify installation tolerance requirements (e.g., frame plumb/level/square tolerances) by reference to manufacturer standards or DEL-001-11 | REQ-011-04-02 requires "strict conformance" to IFC documents but no numeric installation tolerances are stated; Procedure Step 4.3 references "out of tolerance" without defining the tolerance, making mandatory practice ambiguous | Specification.md; Procedure.md | REQ-011-04-02; Step 4 | -- | DEL-001-11 | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm occupancy classification for the New North Shop addition under Alberta Building Code to determine applicable door requirements (egress width, fire separation, accessibility scope) | REQ-011-04-03 states "occupancy classification TBD in IFC design documents"; compliance determination cannot be fully scoped until this is resolved | Specification.md | REQ-011-04-03 Note | -- | Architect (PKG-001) / DEL-001-11 | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Specification | Specification | Add traceability between Safety Code inspection scope (Verification table row REQ-011-04-03) and specific code requirements that the SCO will inspect against | The Verification table states "Safety Code inspection and sign-off" but does not indicate which specific code provisions the SCO inspection covers; regulatory audit needs explicit linkage to the requirements being audited | Specification.md | Verification table, REQ-011-04-03 row | -- | Safety Codes Officer / AHJ | TBD |
| A-005 | A:operative:judging | VerificationGap | Procedure | Procedure | Add quantified pass/fail criteria for operational testing in Step 8 (e.g., maximum closer-return time, maximum acceptable gap dimension for weather stripping, force limits for accessible hardware) | Step 8 lists functional checks (open, close, latch, lock, seal) but all pass conditions are qualitative ("correctly," "without binding"); performance assessment requires measurable criteria | Procedure.md | Step 8 — Operational Testing and Adjustment | -- | DEL-001-11 / manufacturer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Door quantity TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence sources identified where available |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Multiple Datasheet attributes TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (upstream dependency, design-build sequencing) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are thorough given TBD design inputs |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Parts room door dimension inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Construction knowledge requirements clear |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicit in procedure |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery scope adequate for construction deliverable |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment needs captured in Guidance considerations |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance present in trade-offs section |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance purpose |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Record TBD: Confirm exact door count and locations once DEL-001-07 is issued; this is an essential fact for procurement, scheduling, and verification | Door quantity is listed as "TBD" in Datasheet Attributes; this is the single most critical missing essential fact for this deliverable | Datasheet.md | Attributes table, "Number of doors" row | -- | DEL-001-07 (Door & Window Schedule) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add entries for: (1) door leaf material, (2) insulation/thermal performance value, (3) door weight/mass once specified in DEL-001-07/DEL-001-11 | Multiple Datasheet attribute values are TBD (leaf dimensions, frame type, hardware set, glazing, threshold/weather seal, security/locking, finish/colour, fire rating); comprehensiveness of the data record requires these to be populated when design documents are issued | Datasheet.md | Attributes table | -- | DEL-001-07, DEL-001-11 | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Align parts room roll-up door dimension: Datasheet states "6'-wide" (Construction table) while Guidance states "16'" in the Principles section | Datasheet Construction table says "6'-wide roll-up door for parts storage room (DEL-012-01, SOW-0029)" while Guidance Principles section 2 says "parts room roll-up door (16')"; these are inconsistent dimension references for the same element | Datasheet.md; Guidance.md | Datasheet: Construction table, "Parts room roll-up door" row; Guidance: Principles section 2 | Datasheet.md#Construction ("6'-wide"); Guidance.md#Principles ("16'") | RFP Appendix B (R-04) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Imperative | 1 | HAS_ITEMS | Egress requirement not explicitly linked to NBC egress provisions |
| C:normative:sufficiency | normative | sufficiency | Qualified Conformance | 0 | NO_ITEMS | Conformance qualification adequate given TBD status |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Energy code not addressed |
| C:normative:consistency | normative | consistency | Uniform Prescriptive Rigor | 0 | NO_ITEMS | Prescriptive rigor is uniform where requirements exist |
| C:operative:necessity | operative | necessity | Critical Operational Basis | 0 | NO_ITEMS | Operational basis adequately established |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Capability demonstration through procedure steps |
| C:operative:completeness | operative | completeness | Comprehensive Process Coverage | 1 | HAS_ITEMS | Protection of installed doors not addressed |
| C:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Process discipline consistent |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Criterion | 0 | NO_ITEMS | Value criteria present in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit | 0 | NO_ITEMS | Merit substantiation adequate |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Value accounting covered |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Value alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add explicit egress requirement referencing NBC/ABC means-of-egress provisions (e.g., minimum egress door width, swing direction, panic hardware requirements for the applicable occupancy) | Under the Authoritative Imperative lens, the Specification requires "separate entrance/exit doors" (REQ-011-04-01) and code compliance (REQ-011-04-03) but does not explicitly address means-of-egress provisions (minimum width, swing direction, panic hardware) which are distinct from accessibility and from general safety code compliance | Specification.md | REQ-011-04-01, REQ-011-04-03 | -- | Alberta Building Code / NBC Part 3 | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Guidance | Add consideration of National Energy Code of Canada for Buildings (NECB) or Alberta energy code requirements for exterior door assemblies (thermal transmittance, air leakage) | Under the Exhaustive Regulatory Scope lens, the Standards table lists Alberta Building Code and Safety Codes Act but does not mention the National Energy Code for Buildings (NECB) or Alberta energy efficiency requirements; exterior pedestrian doors in a heated industrial building in Alberta may be subject to energy code thermal performance requirements | Specification.md | Standards table | -- | NECB / Alberta energy code provisions | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or note for temporary protection of installed door assemblies during remaining construction activities (e.g., protection from welding spatter, concrete dust, paint overspray) before final handover | Under the Comprehensive Process Coverage lens, the Procedure covers installation through testing but does not address protection of installed doors during the remaining construction period before handover; this is a common construction sequencing concern for finish elements installed before project completion | Procedure.md | Between Step 8 and Step 9 (or as a note in Step 6) | -- | Standard construction practice | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Compliance Threshold | 1 | HAS_ITEMS | Threshold for "suitability" not quantified |
| F:normative:sufficiency | normative | sufficiency | Calibrated Regulatory Adequacy | 0 | NO_ITEMS | Regulatory adequacy calibration deferred to design docs |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Covered under C-002 |
| F:normative:consistency | normative | consistency | Harmonized Prescriptive Integrity | 0 | NO_ITEMS | Prescriptive integrity harmonized across docs |
| F:operative:necessity | operative | necessity | Foundational Task Competence | 1 | HAS_ITEMS | Installer qualification not addressed |
| F:operative:sufficiency | operative | sufficiency | Validated Practical Proficiency | 0 | NO_ITEMS | Proficiency validation implicit in procedure |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Mastery | 0 | NO_ITEMS | Workflow coverage adequate |
| F:operative:consistency | operative | consistency | Systematic Performance Coherence | 0 | NO_ITEMS | Performance coherence maintained |
| F:evaluative:necessity | evaluative | necessity | Grounded Value Discernment | 0 | NO_ITEMS | Value discernment grounded in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Threshold | 0 | NO_ITEMS | Value threshold defensible |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Appraisal | 0 | NO_ITEMS | Worth appraisal scope adequate |
| F:evaluative:consistency | evaluative | consistency | Harmonized Quality Integrity | 1 | HAS_ITEMS | Guarantee scope for hardware adjustment |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify REQ-011-04-05: replace "suitable for the Alberta climate" with specific performance thresholds (e.g., air infiltration rate, thermal transmittance value) once DEL-001-11 is available, or state explicit deferral to DEL-001-11 for numeric values | Under the Mandated Compliance Threshold lens, REQ-011-04-05 uses "suitable for the Alberta climate" and "appropriate for the cold-climate location" without quantified performance thresholds; this vague language cannot function as a mandated compliance threshold | Specification.md | REQ-011-04-05 | -- | DEL-001-11 / NECB | TBD |
| F-002 | F:operative:necessity | RationaleGap | Procedure | Guidance | Add guidance on required installer qualifications or trade certifications for door/frame/hardware installation (e.g., journeyman carpenter, manufacturer-certified installer for fire-rated assemblies) | Under the Foundational Task Competence lens, the Procedure assigns all work to "General Contractor" but does not address whether specific trade qualifications or manufacturer certifications are required, particularly for fire-rated assembly installation per ULC listing requirements | Procedure.md; Guidance.md | Procedure: Steps 5-6; Guidance: entire document scanned | -- | DEL-001-11 / ULC listing requirements | TBD |
| F-003 | F:evaluative:consistency | WeakStatement | Specification | Guidance | Clarify whether the 2-year guarantee (REQ-011-04-08) covers hardware adjustment/readjustment due to normal settling and seasonal thermal movement, or only defects in materials and workmanship | Under the Harmonized Quality Integrity lens, REQ-011-04-08 states a 2-year guarantee for "materials and workmanship" but doors in cold-climate industrial buildings commonly require seasonal re-adjustment; the boundary between warranty-covered adjustment and maintenance is unclear | Specification.md | REQ-011-04-08 | -- | CCDC 14-2013 warranty provisions | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Prescriptive Aim | 0 | NO_ITEMS | Prescriptive aim clear: comply with IFC and codes |
| D:normative:applying | normative | applying | Resolved Obligatory Practice | 1 | HAS_ITEMS | Shop drawing requirement conditional |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling process defined |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Assurance | 0 | NO_ITEMS | Oversight assurance through SCO and County rep |
| D:operative:guiding | operative | guiding | Grounded Procedural Aim | 0 | NO_ITEMS | Procedural aims grounded in 10-step procedure |
| D:operative:applying | operative | applying | Resolved Execution Standard | 1 | HAS_ITEMS | Material receiving inspection criteria absent |
| D:operative:judging | operative | judging | Decisive Performance Ruling | 0 | NO_ITEMS | Performance rulings tied to verification table |
| D:operative:reviewing | operative | reviewing | Resolved Process Assurance | 0 | NO_ITEMS | Process assurance through records closeout |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Orientation | 0 | NO_ITEMS | Worth orientation clear in Guidance |
| D:evaluative:applying | evaluative | applying | Realized Merit Standard | 0 | NO_ITEMS | Merit standard realized through trade-off analysis |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Verdict | 1 | HAS_ITEMS | No hold/release point for frame inspection |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Assurance | 0 | NO_ITEMS | Quality assurance resolved through documentation |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Procedure | Procedure | Clarify whether shop drawing submittal (Step 2) is mandatory or conditional; current phrasing "if required" creates ambiguity about when this obligation applies | Under the Resolved Obligatory Practice lens, Procedure Step 2 is titled "Submittal and Approval (if required)" and sourced as "ASSUMPTION"; this conditionality leaves the obligatory practice unresolved — either the submittal is required (per standard design-build practice and Specification Documentation table) or it is not | Procedure.md | Step 2 — Submittal and Approval | -- | DEL-001-11 | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Procedure | Add explicit receiving inspection criteria in Step 3.3 (e.g., check against approved submittal for model/size/finish, inspect for shipping damage to frame/leaf/hardware, verify fire-rating labels if applicable) | Under the Resolved Execution Standard lens, Procedure Step 3.3 says "inspect delivered materials against the approved submittals" but does not list specific inspection criteria; the execution standard for receiving inspection is not resolved | Procedure.md | Step 3 — Material Procurement, substep 3.3 | -- | Standard construction practice | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Procedure | Procedure | Add an explicit hold point after frame installation (Step 5.3) requiring documented sign-off before proceeding to door hanging (Step 6); currently the check exists but is not designated as a mandatory hold/release point | Under the Conclusive Quality Verdict lens, Step 5.3 states "Inspect installed frames before hanging door leaves" but this is not designated as a formal hold point requiring sign-off; a conclusive quality verdict at this stage prevents costly rework if frames are found non-conforming after doors are hung | Procedure.md | Step 5.3, Step 6 | -- | Standard construction QA practice | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Directive Foundation | 0 | NO_ITEMS | Directive foundation established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directive Counsel | 0 | NO_ITEMS | Counsel justified by RFP and code references |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 1 | HAS_ITEMS | No directive on coordination with building envelope sealant scope |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Clarity | 0 | NO_ITEMS | Directive clarity harmonized |
| X:applying:necessity | applying | necessity | Vital Practice Foundation | 1 | HAS_ITEMS | No verification of anchor type/spacing |
| X:applying:sufficiency | applying | sufficiency | Proven Execution Adequacy | 0 | NO_ITEMS | Execution adequacy proven through procedure |
| X:applying:completeness | applying | completeness | Thorough Execution Coverage | 0 | NO_ITEMS | Execution coverage thorough |
| X:applying:consistency | applying | consistency | Consistent Practice Alignment | 0 | NO_ITEMS | Practice alignment consistent |
| X:judging:necessity | judging | necessity | Binding Fitness Determination | 1 | HAS_ITEMS | No acceptance criteria for caulking/weatherproofing |
| X:judging:sufficiency | judging | sufficiency | Justified Fitness Ruling | 0 | NO_ITEMS | Fitness rulings justified where defined |
| X:judging:completeness | judging | completeness | Exhaustive Fitness Account | 0 | NO_ITEMS | Fitness account covered in Verification table |
| X:judging:consistency | judging | consistency | Coherent Fitness Measure | 1 | HAS_ITEMS | Weather performance verification method weak |
| X:reviewing:necessity | reviewing | necessity | Core Assurance Foundation | 0 | NO_ITEMS | Assurance foundation present |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Assurance Review | 0 | NO_ITEMS | Assurance review justified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Coverage | 0 | NO_ITEMS | Assurance coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Harmonized Oversight Integrity | 0 | NO_ITEMS | Oversight integrity harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add consideration of coordination between door frame perimeter caulking (this deliverable) and building envelope air/vapour barrier continuity (PKG-011 envelope scope) to ensure no gap in responsibility | Under the Exhaustive Directive Scope lens, Guidance does not address how door frame perimeter caulking integrates with the overall building envelope air barrier and vapour barrier system; this is a common coordination gap in construction where the door installer's caulking must tie into the envelope contractor's air barrier detailing | Guidance.md | Considerations section (entire section scanned) | -- | PKG-011 envelope design / DEL-001-11 | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification method for frame anchorage (anchor type, spacing, and embedment) in the Verification table; currently only dimensional conformance is checked but anchorage adequacy is not independently verified | Under the Vital Practice Foundation lens, REQ-011-04-02 requires conformance to IFC documents which will specify anchorage, but the Verification table does not include a separate check for frame anchorage adequacy; Procedure Step 5.1 mentions "anchor type and spacing TBD in DEL-001-11" but there is no corresponding verification entry | Specification.md; Procedure.md | Specification: Verification table, REQ-011-04-02 row; Procedure: Step 5.1 | -- | DEL-001-11 | TBD |
| X-003 | X:judging:necessity | WeakStatement | Specification | Specification | Strengthen verification method for REQ-011-04-05 (Weather performance): replace "Visual inspection of weather stripping and threshold installation; operational test (no visible gaps)" with measurable criteria (e.g., air infiltration test, or reference to manufacturer's installation verification protocol) | Under the Binding Fitness Determination lens, the verification method for weather performance is "visual inspection" and "no visible gaps" — this is insufficient for a binding fitness determination in a cold-climate industrial building; visual inspection cannot detect air infiltration through improperly compressed weather stripping | Specification.md | Verification table, REQ-011-04-05 row | -- | DEL-001-11 / NECB / manufacturer | TBD |
| X-004 | X:judging:consistency | Normalization | Multi | Specification | Align the verification method for REQ-011-04-05 (Specification Verification table) with the corresponding check in Procedure Verification table: Specification says "Visual inspection ... operational test (no visible gaps)" while Procedure says "Operational test passed ... all doors open, close, latch, lock, seal, and closer-return correctly" — the Procedure's verification is broader and should be reflected in the Specification | Under the Coherent Fitness Measure lens, the Specification Verification table and Procedure Verification table describe different scopes of verification for weather/operational performance; the Procedure's verification checks are more comprehensive than what the Specification's Verification table describes for REQ-011-04-05 | Specification.md; Procedure.md | Specification: Verification table REQ-011-04-05; Procedure: Verification table "Operational test passed" | Specification.md#Verification ("Visual inspection...no visible gaps"); Procedure.md#Verification ("all doors open, close, latch, lock, seal, and closer-return correctly") | Specification should govern | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Datum | 0 | NO_ITEMS | Directive data adequately referenced |
| E:guiding:information | guiding | information | Integrated Directive Signal | 0 | NO_ITEMS | Directive signals integrated |
| E:guiding:knowledge | guiding | knowledge | Mastered Prescriptive Insight | 0 | NO_ITEMS | Prescriptive insight demonstrated |
| E:guiding:wisdom | guiding | wisdom | Judicious Prescriptive Foresight | 0 | NO_ITEMS | Foresight present in Guidance trade-offs |
| E:applying:data | applying | data | Verified Execution Datum | 1 | HAS_ITEMS | No as-built recording requirement in Specification |
| E:applying:information | applying | information | Informed Execution Context | 0 | NO_ITEMS | Execution context adequately informed |
| E:applying:knowledge | applying | knowledge | Proven Execution Mastery | 0 | NO_ITEMS | Execution mastery demonstrated in procedure |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Execution judgment guidance present |
| E:judging:data | judging | data | Conclusive Assessment Datum | 0 | NO_ITEMS | Assessment data defined in verification table |
| E:judging:information | judging | information | Informed Assessment Signal | 0 | NO_ITEMS | Assessment signals adequate |
| E:judging:knowledge | judging | knowledge | Mastered Assessment Expertise | 0 | NO_ITEMS | Assessment expertise requirements clear |
| E:judging:wisdom | judging | wisdom | Principled Verdict Foresight | 0 | NO_ITEMS | Verdict foresight adequate |
| E:reviewing:data | reviewing | data | Verified Oversight Datum | 0 | NO_ITEMS | Oversight data defined |
| E:reviewing:information | reviewing | information | Informed Oversight Signal | 0 | NO_ITEMS | Oversight signals clear |
| E:reviewing:knowledge | reviewing | knowledge | Mastered Oversight Expertise | 1 | HAS_ITEMS | County rep role at operational testing unclear |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Oversight foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | RationaleGap | Datasheet | Datasheet | Add a note in Datasheet or Specification Documentation section explaining that as-built documentation (deviations from IFC) must be formally transmitted to the Architect for record drawings, with a clear responsible party and timeline | Under the Verified Execution Datum lens, Procedure Step 10.1 mentions "As-built notes (if any deviations)" and Step 10.2 mentions submission to County, but the Datasheet and Specification do not include as-built documentation as a formal deliverable output with defined acceptance criteria; the data trail for verified execution is incomplete | Datasheet.md; Procedure.md | Datasheet: entire document scanned; Procedure: Step 10 | -- | RFP closeout requirements | TBD |
| E-002 | E:reviewing:knowledge | TBD_Question | Specification | Specification | Clarify whether the County project representative's witnessing of operational testing (Verification table, REQ-011-04-07) constitutes formal acceptance or is merely observational; clarify the County representative's authority to require re-testing or reject | Under the Mastered Oversight Expertise lens, the Specification Verification table states operational testing is "witnessed by County Representative" but does not define the County representative's authority (accept/reject/require rework) vs. the GC's self-certification role; this affects the oversight expertise required and the weight of the review | Specification.md | Verification table, REQ-011-04-07 row | -- | RFP / CCDC 14-2013 | TBD |
