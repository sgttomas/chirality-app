# Semantic Lensing Register: DEL-003-06 Mechanical Calculation Package

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-003_Mechanical Design/1_Working/DEL-003-06_Calculation-Package/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-06_Calculation-Package/_CONTEXT.md
- _STATUS.md — DEL-003-06_Calculation-Package/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-06_Calculation-Package/_SEMANTIC.md
- Datasheet.md — DEL-003-06_Calculation-Package/Datasheet.md
- Specification.md — DEL-003-06_Calculation-Package/Specification.md
- Guidance.md — DEL-003-06_Calculation-Package/Guidance.md
- Procedure.md — DEL-003-06_Calculation-Package/Procedure.md
- _REFERENCES.md — DEL-003-06_Calculation-Package/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 11
  - Guidance: 3
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 3  X: 5  E: 5
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 8
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Design temperature not prescribed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code clause specificity gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Acceptance criteria for system balance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 11 covers P.Eng. review and audit trail adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Mezzanine zone procedure gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-11 in Procedure cover execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Spec and Procedure are consistent |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Life-cycle cost rationale gap |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off T-01 in Guidance addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost and energy tradeoffs noted in Guidance T-01 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal review process in Step 11 is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify specific design outdoor heating temperature value in REQ-M-001 rather than deferring entirely to "TBD; ASSUMPTION: per NBCC or local climate data" | The normative prescriptive direction for heating load calculation lacks a committed design temperature. Multiple documents reference "approximately -35C or colder" as assumption but no document commits to a specific value, which could change equipment sizing. | Specification.md; Datasheet.md | Specification.md#REQ-M-001; Datasheet.md#Conditions | -- | PROPOSAL: Mechanical Engineer to confirm from NBCC climate data tables for nearest station to Ferintosh, AB | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add specific Alberta Building Code and ASHRAE 62.1 clause references to each requirement where code compliance is claimed | REQ-M-010 requires code compliance but all clause references in the Standards table are listed as "location TBD -- text not accessible." Mandatory practice cannot be applied without specific clause identification. | Specification.md | Specification.md#Standards; Specification.md#REQ-M-010 | -- | PROPOSAL: Mechanical Engineer to populate specific code clause numbers once code texts are obtained | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criterion for system balance in REQ-M-009 verification (e.g., net balance within stated percentage) | REQ-M-009 states "ASSUMPTION: plus/minus 10% or per applicable standard" but the Verification table entry only says "Confirm supply/exhaust balance table shows acceptable net pressure" without a binding numeric threshold. Compliance determination requires a specific acceptance value. | Specification.md | Specification.md#REQ-M-009; Specification.md#Verification | -- | PROPOSAL: Mechanical Engineer to set acceptance threshold and cite basis | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a procedure step or sub-step addressing mezzanine zone HVAC determination | Guidance C-06 identifies the mezzanine as a zone requiring code evaluation for ventilation, but Procedure Steps 1-11 do not include any step for mezzanine zone analysis. Procedural direction for this zone is absent. | Procedure.md; Guidance.md | Procedure.md#Steps; Guidance.md#C-06 | -- | PROPOSAL: Insert as sub-step under Step 3 (Ventilation Rate Calculations) | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for ceiling fan quantity (6 fans) -- whether driven by coverage area analysis, manufacturer recommendation, or Owner preference | Guidance C-01 mentions destratification function but does not explain why exactly 6 fans rather than 4 or 8. The value basis for this quantity is not established anywhere in the documents. | Guidance.md; Datasheet.md | Guidance.md#C-01; Datasheet.md#Mechanical Systems Inventory | -- | PROPOSAL: Mechanical Engineer to document basis for fan quantity in calculation package | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing building envelope U-values |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references are sourced to RFP |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing room dimensions for office, utility room |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements cited are consistent with App B |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Welding spec dependency |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate contextual framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Guidance Considerations C-01 through C-06 cover key topics |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally consistent on messaging |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Calculation methodology references (ASHRAE, ACGIH) are identified |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement addresses competence |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Standards table in Specification is comprehensive |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-document references are aligned |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off T-01, T-02, and Conflicts CON-M-001 through CON-M-003 in Guidance surface the key judgment points |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Human rulings are correctly deferred as TBD |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers system-level integration perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Conservative design principle (P-01) provides consistent reasoning basis |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Building envelope U-values (wall, roof, slab, window, door assemblies) are essential input data not yet available; source is PKG-001/PKG-002 | Heating load calculation (REQ-M-001) cannot proceed without envelope thermal properties. Datasheet lists these as required but does not record even preliminary values. The essential fact is absent. | Datasheet.md; Specification.md | Datasheet.md#Conditions; Specification.md#REQ-M-001 | -- | PROPOSAL: Obtain from Architectural (PKG-001) and Structural (PKG-002) packages | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add dimensions for office space and utility room (currently listed as "dimensions TBD -- not stated in sources") | The comprehensive record of building physical parameters is incomplete for two rooms that require zone-by-zone ventilation calculations. | Datasheet.md | Datasheet.md#Building Physical Parameters | -- | PROPOSAL: Obtain from confirmed architectural drawings or App B measurement | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Specification | Record TBD: County welding equipment specifications (SOW-0204) are an essential signal required to finalize REQ-M-006; formal RFI timeline should be tracked | Multiple documents note this dependency (Guidance P-03, Procedure Step 6, Specification REQ-M-006) but no document records the expected receipt date or escalation path. | Specification.md; Guidance.md; Procedure.md | Specification.md#REQ-M-006; Guidance.md#P-03; Procedure.md#Step 6 | -- | PROPOSAL: Project Manager to issue RFI and track response timeline | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Basis | 1 | HAS_ITEMS | Indoor temperature setpoints weak |
| C:normative:sufficiency | normative | sufficiency | Mandated Substantiation | 0 | NO_ITEMS | Specification provides adequate substantiation basis per requirement |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Wash bay ventilation requirement gap |
| C:normative:consistency | normative | consistency | Uniform Compliance Standard | 0 | NO_ITEMS | Standards table applies uniformly across requirements |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites PR-01 through PR-09 in Procedure are comprehensive |
| C:operative:sufficiency | operative | sufficiency | Competent Process Execution | 0 | NO_ITEMS | Step-by-step procedure is adequate for competent execution |
| C:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 1 | HAS_ITEMS | Wash bay ventilation procedure step missing |
| C:operative:consistency | operative | consistency | Reliable Procedural Coherence | 0 | NO_ITEMS | Procedure steps track to Specification requirements consistently |
| C:evaluative:necessity | evaluative | necessity | Fundamental Value Criterion | 0 | NO_ITEMS | OBJ-003 and OBJ-004 establish value criteria in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Appraisal | 0 | NO_ITEMS | Guidance substantiates purpose adequately |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Account | 0 | NO_ITEMS | Guidance covers comprehensive value considerations |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Conservative design principle (P-01) provides consistent value basis |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen indoor design temperature setpoints in REQ-M-002 from "ASSUMPTION: approximately +10C in shop areas" to a committed value with code basis | The obligatory compliance basis for heating system sizing depends on indoor setpoints, but these are stated as approximate assumptions. Implementation decisions (equipment capacity) change materially depending on whether the setpoint is +5C, +10C, or +15C. | Specification.md | Specification.md#REQ-M-002 | -- | PROPOSAL: Mechanical Engineer to confirm per Alberta Building Code occupancy requirements | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a dedicated requirement for wash bay ventilation/moisture control (currently addressed only in Guidance C-04, not in Specification requirements) | Guidance C-04 identifies wash bay humidity as a distinct zone requiring ventilation design, but no dedicated REQ-M exists for wash bay ventilation. The exhaust regulatory coverage is incomplete without this zone. REQ-M-003 mentions wash bay only as a line item in the ACH list, without addressing moisture-specific requirements. | Specification.md; Guidance.md | Specification.md#REQ-M-003; Guidance.md#C-04 | -- | PROPOSAL: Add REQ-M-012 for wash bay ventilation/moisture control, or expand REQ-M-003 | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a procedure step for wash bay ventilation sizing, coordinating with moisture control and drainage considerations from Guidance C-04 | Procedure Steps 3-9 cover main shop, repair bays, service pit, welding, and ceiling fans, but there is no dedicated step for wash bay ventilation sizing. The operative completeness gap means the wash bay zone could be overlooked during execution. | Procedure.md; Guidance.md | Procedure.md#Steps; Guidance.md#C-04 | -- | PROPOSAL: Insert wash bay ventilation step between Step 3 and Step 4, or as sub-step under Step 3 | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Regulatory Mandate | 1 | HAS_ITEMS | ASHRAE 90.1 applicability uncertain |
| F:normative:sufficiency | normative | sufficiency | Defensible Regulatory Adequacy | 1 | HAS_ITEMS | Safety factor basis weak |
| F:normative:completeness | normative | completeness | Total Regulatory Authority | 0 | NO_ITEMS | REQ-M-010 addresses code compliance comprehensively |
| F:normative:consistency | normative | consistency | Coherent Regulatory Discipline | 0 | NO_ITEMS | Standards references are applied consistently |
| F:operative:necessity | operative | necessity | Indispensable Process Foundation | 1 | HAS_ITEMS | Exhaust drops per bay TBD |
| F:operative:sufficiency | operative | sufficiency | Validated Operational Competence | 0 | NO_ITEMS | P.Eng. stamp and review process validate competence |
| F:operative:completeness | operative | completeness | Complete Process Authority | 0 | NO_ITEMS | Steps 1-11 achieve complete procedural coverage |
| F:operative:consistency | operative | consistency | Disciplined Process Alignment | 1 | HAS_ITEMS | Units inconsistency |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | OBJ-003 and OBJ-004 establish merit basis |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Appraisal Competence | 0 | NO_ITEMS | Trade-offs in Guidance address appraisal |
| F:evaluative:completeness | evaluative | completeness | Total Valuation Authority | 0 | NO_ITEMS | Complete value scope covered |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Coherence | 0 | NO_ITEMS | Consistent merit principles across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify whether ASHRAE 90.1 energy standard is applicable or not; REQ-M-010 lists it as "ASSUMPTION: may be applicable" -- resolve to yes/no | The absolute regulatory mandate for energy compliance is uncertain. If ASHRAE 90.1 applies, it affects equipment efficiency requirements and may require additional calculations. The "may be applicable" language is too vague for a normative requirement. | Specification.md | Specification.md#REQ-M-010; Specification.md#Standards | -- | PROPOSAL: Mechanical Engineer to determine applicability from Alberta Building Code energy provisions | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Guidance | Clarify basis and range for the heating load safety factor in REQ-M-002 / Procedure Step 2.4 ("ASSUMPTION: 10-15% or per engineering judgment") | Defensible regulatory adequacy requires a justified safety factor, not a range stated as assumption. The choice between 10% and 15% could change equipment selection by tens of kW. | Specification.md; Procedure.md | Specification.md#REQ-M-002; Procedure.md#Step 2 | -- | PROPOSAL: Mechanical Engineer to document selected factor and engineering basis in calculation package | TBD |
| F-003 | F:operative:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Number of exhaust hose drops per repair bay is unspecified (Specification REQ-M-005 and Procedure Step 5.1 both note "TBD -- not specified in RFP") | This is an indispensable process input. The exhaust system flow rate depends directly on the number of drops. If each bay has 2 drops rather than 1, exhaust flow doubles, affecting MUA sizing and system balance. | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Mechanical Systems Inventory; Specification.md#REQ-M-005; Procedure.md#Step 5 | -- | PROPOSAL: Design decision by Mechanical Engineer or RFI to Owner for operational requirements | TBD |
| F-004 | F:operative:consistency | Normalization | Multi | Guidance | Normalize airflow units across all documents: Procedure uses both "CFM or L/s" and "L/s or CFM" interchangeably; Specification uses "CFM or L/s" in REQ-M-008 | Disciplined process alignment requires consistent unit conventions. Mixed unit references risk transcription errors when values flow from calculations to equipment schedules and drawings. | Specification.md; Procedure.md | Specification.md#REQ-M-008; Procedure.md#Step 3; Procedure.md#Step 9 | -- | PROPOSAL: Establish primary unit convention (likely L/s per Canadian practice or CFM per equipment catalogs) in Guidance and apply uniformly | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Guidance establishes clear directive authority via P-01 through P-05 |
| D:normative:applying | normative | applying | Enforced Compliance Duty | 1 | HAS_ITEMS | P.Eng. stamp scope ambiguity |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 0 | NO_ITEMS | Verification table maps each requirement to a verification approach |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Examination | 0 | NO_ITEMS | Internal review and P.Eng. stamp process is defined |
| D:operative:guiding | operative | guiding | Resolved Operational Guidance | 0 | NO_ITEMS | Procedure provides clear step-by-step operational guidance |
| D:operative:applying | operative | applying | Confirmed Execution Delivery | 1 | HAS_ITEMS | Drawing coordination timing gap |
| D:operative:judging | operative | judging | Definitive Performance Ruling | 0 | NO_ITEMS | Verification checks in Procedure are adequate |
| D:operative:reviewing | operative | reviewing | Resolved Workflow Examination | 0 | NO_ITEMS | Records section provides adequate workflow examination basis |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Direction | 1 | HAS_ITEMS | Energy efficiency objective gap |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Deployment | 0 | NO_ITEMS | Trade-offs are identified for resolution |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 0 | NO_ITEMS | CON-M-001 through CON-M-003 route judgment to human |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Examination | 0 | NO_ITEMS | Internal review process addresses quality examination |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Clarify whether the P.Eng. stamp requirement (REQ-M-011) covers the entire calculation package or only the final IFC version; Procedure distinguishes PRELIMINARY and FINAL versions | Enforced compliance duty requires clarity on which version(s) require the P.Eng. stamp. REQ-M-011 says "signed/stamped by a P.Eng." but Procedure Step 11.4 implies stamping occurs only at the final IFC stage. If the PRELIMINARY version circulates without a stamp, it may not satisfy interim compliance needs. | Specification.md; Procedure.md | Specification.md#REQ-M-011; Procedure.md#Step 11 | -- | PROPOSAL: Clarify in Specification that stamp applies to FINAL IFC only, or state requirements for interim versions | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Procedure | Add explicit verification step confirming calculated values are transmitted to and reconciled with DEL-003-02 through DEL-003-05 before IFC issuance | Confirmed execution delivery requires that calculation outputs flow correctly into downstream deliverables. Procedure Step 11.5 mentions coordination but does not include a verification checkpoint for reconciling calculation values with drawing values. | Procedure.md | Procedure.md#Step 11; Procedure.md#Verification | -- | PROPOSAL: Add verification row in Procedure Verification table for drawing/schedule reconciliation | TBD |
| D-003 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add consideration or principle addressing energy efficiency objectives for the mechanical systems (e.g., whether Owner has energy performance targets beyond code minimum) | Resolved worth direction for this deliverable focuses on sizing correctness and code compliance but does not address whether the Owner values energy efficiency beyond code minimum. Trade-off T-01 mentions "life-cycle cost considerations" but no principle or consideration establishes an energy performance target. | Guidance.md | Guidance.md#Principles; Guidance.md#Trade-offs T-01 | -- | PROPOSAL: Add consideration C-07 addressing energy performance expectations or confirm code-minimum-only approach with Owner | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Imperative | 0 | NO_ITEMS | Guidance Purpose section establishes foundational directive |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Guidance Adequacy | 1 | HAS_ITEMS | Crane envelope guidance insufficient |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Coverage | 0 | NO_ITEMS | Guidance covers all major topics |
| X:guiding:consistency | guiding | consistency | Consistent Guidance Alignment | 0 | NO_ITEMS | Guidance principles and considerations are internally aligned |
| X:applying:necessity | applying | necessity | Mandatory Enactment Basis | 1 | HAS_ITEMS | Combustion air requirement gap |
| X:applying:sufficiency | applying | sufficiency | Justified Implementation Proof | 0 | NO_ITEMS | Procedure verification checks provide sufficient proof basis |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 0 | NO_ITEMS | Records section in Procedure is comprehensive |
| X:applying:consistency | applying | consistency | Stable Implementation Coherence | 0 | NO_ITEMS | Procedure is internally consistent |
| X:judging:necessity | judging | necessity | Binding Judgment Foundation | 1 | HAS_ITEMS | Verification approach for REQ-M-010 |
| X:judging:sufficiency | judging | sufficiency | Justified Verdict Adequacy | 0 | NO_ITEMS | Verification approaches are tied to specific requirements |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 0 | NO_ITEMS | All 11 requirements have verification entries |
| X:judging:consistency | judging | consistency | Consistent Ruling Standard | 0 | NO_ITEMS | Verification table applies consistent approach |
| X:reviewing:necessity | reviewing | necessity | Foundational Examination Basis | 1 | HAS_ITEMS | Review criteria specificity |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Examination Adequacy | 0 | NO_ITEMS | Internal review plus P.Eng. stamp provides adequate examination |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Coverage | 1 | HAS_ITEMS | Missing commissioning interface verification |
| X:reviewing:consistency | reviewing | consistency | Consistent Examination Standard | 0 | NO_ITEMS | Review standard is consistently defined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on crane envelope clearance constraints for overhead mechanical equipment (referenced in Procedure PR-04 and Step 8.4 but not elaborated in Guidance) | Warranted guidance adequacy requires that the crane envelope constraint be explained with enough detail for the Mechanical Engineer to act. Guidance T-01 mentions crane conflict briefly but does not provide clearance values or methodology for confirming adequate clearance. | Guidance.md; Procedure.md | Guidance.md#T-01; Procedure.md#PR-04; Procedure.md#Step 8 | -- | PROPOSAL: Add to Guidance Considerations a paragraph on crane envelope dimensions and required clearance methodology | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Add requirement for combustion air supply calculation if gas-fired heating equipment is selected | Mandatory enactment basis for gas-fired equipment includes combustion air supply per code. Guidance C-05 establishes the gas-fired assumption, but no requirement in Specification addresses combustion air calculation. If gas-fired unit heaters or MUA with gas heating coil are selected, combustion air supply sizing is a code requirement. | Specification.md; Guidance.md | Specification.md#Requirements (entire section scanned); Guidance.md#C-05 | -- | PROPOSAL: Add REQ-M-013 for combustion air supply calculation (conditional on gas-fired equipment selection) | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen REQ-M-010 verification approach beyond "P.Eng. stamp and code references included" to require a code compliance matrix mapping each code requirement to the calculation section demonstrating compliance | Binding judgment foundation for code compliance requires more than a stamp. The current verification approach for REQ-M-010 is the weakest in the table -- it does not specify how compliance is demonstrated beyond inclusion of references. | Specification.md | Specification.md#Verification (REQ-M-010 row) | -- | PROPOSAL: Require a code compliance cross-reference matrix as part of Section 10 of the calculation package | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add specific review criteria for the internal review in Step 11.1 (e.g., checklist of items to verify: arithmetic, assumption justification, code compliance, system balance closure) | Foundational examination basis requires more specificity than "reviews all sections for arithmetic errors, unjustified assumptions, missing inputs, inconsistencies with drawing set." A structured review checklist would make the examination reproducible and auditable. | Procedure.md | Procedure.md#Step 11 | -- | PROPOSAL: Add a review checklist as an appendix or sub-table in Step 11 | TBD |
| X-005 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add verification or record confirming that calculation package outputs are transmitted to PKG-020 (Commissioning) for use in commissioning test procedures | Exhaustive examination coverage should include the commissioning interface. Datasheet notes PKG-020 handles commissioning, and the calculation package provides the basis values (design flows, temperatures, pressures) that commissioning must verify, but no verification step or record addresses this handoff. | Procedure.md; Datasheet.md | Procedure.md#Verification; Procedure.md#Records; Datasheet.md#Construction Package Context | -- | PROPOSAL: Add record or verification row for commissioning handoff | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 1 | HAS_ITEMS | Datasheet status field inconsistency |
| E:guiding:information | guiding | information | Coherent Directive Intelligence | 0 | NO_ITEMS | Guidance provides coherent directive information |
| E:guiding:knowledge | guiding | knowledge | Sovereign Guidance Mastery | 0 | NO_ITEMS | Guidance demonstrates adequate domain mastery for this stage |
| E:guiding:wisdom | guiding | wisdom | Principled Guidance Wisdom | 0 | NO_ITEMS | Conservative design principle and explicit assumption tracking reflect wisdom |
| E:applying:data | applying | data | Documented Execution Record | 1 | HAS_ITEMS | Calculation subjects table lacks target values |
| E:applying:information | applying | information | Actionable Deployment Intelligence | 0 | NO_ITEMS | Procedure provides actionable intelligence for execution |
| E:applying:knowledge | applying | knowledge | Sovereign Execution Mastery | 0 | NO_ITEMS | Steps are detailed enough for competent execution |
| E:applying:wisdom | applying | wisdom | Prudent Execution Wisdom | 0 | NO_ITEMS | Conservative assumptions and explicit flagging reflect prudence |
| E:judging:data | judging | data | Authoritative Verdict Record | 1 | HAS_ITEMS | Verification approach not tracing to specific acceptance values |
| E:judging:information | judging | information | Decisive Verdict Intelligence | 0 | NO_ITEMS | Verification table provides adequate information for verdicts |
| E:judging:knowledge | judging | knowledge | Sovereign Adjudication Mastery | 0 | NO_ITEMS | P.Eng. requirement ensures adjudication competence |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Human ruling mechanism preserves principled adjudication |
| E:reviewing:data | reviewing | data | Authoritative Inspection Record | 1 | HAS_ITEMS | Records missing version control |
| E:reviewing:information | reviewing | information | Comprehensive Inspection Intelligence | 0 | NO_ITEMS | Records section provides comprehensive retention basis |
| E:reviewing:knowledge | reviewing | knowledge | Sovereign Inspection Mastery | 0 | NO_ITEMS | Review process is adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Wisdom | 1 | HAS_ITEMS | Conflict between Spec and Guidance on air exchanger role |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Normalize Datasheet Status field to match _STATUS.md: Datasheet says "INITIALIZED" while _STATUS.md says "SEMANTIC_READY" | The authoritative guidance record contains a status inconsistency. Datasheet Identification table shows Status as "INITIALIZED" but _STATUS.md records current state as "SEMANTIC_READY." This drift risks confusion about the deliverable's lifecycle position. | Datasheet.md; _STATUS.md | Datasheet.md#Identification; _STATUS.md | -- | PROPOSAL: Update Datasheet Status field to match _STATUS.md current state | TBD |
| E-002 | E:applying:data | VerificationGap | Datasheet | Datasheet | Add target values or ranges to the Calculation Subjects table in Datasheet (currently all "TBD") to provide a baseline for verification once calculations are performed | The documented execution record should include at least preliminary target ranges (e.g., estimated heating load range, approximate exhaust flow) so that calculated results can be sanity-checked. All 8 calculation subjects have Status "TBD" with no preliminary ranges. | Datasheet.md | Datasheet.md#Calculation Subjects | -- | PROPOSAL: Mechanical Engineer to add order-of-magnitude estimates as initial targets after preliminary design | TBD |
| E-003 | E:judging:data | TBD_Question | Specification | Specification | Record TBD: What specific acceptance values (numeric thresholds) apply to each verification approach? Current verification table uses qualitative language only (e.g., "Confirm selected equipment capacity >= calculated peak heating load with appropriate safety factor") | The authoritative verdict record lacks quantitative acceptance thresholds for most requirements. While the verification approaches are reasonable, they use relative language ("appropriate safety factor," "acceptable net pressure") without committed numeric values. | Specification.md | Specification.md#Verification | -- | PROPOSAL: Populate numeric acceptance criteria as calculations are completed | TBD |
| E-004 | E:reviewing:data | MissingSlot | Procedure | Procedure | Add version control or revision tracking requirement to Procedure Records section (e.g., revision number, date, and change description for each version of the calculation package) | The authoritative inspection record does not include a mechanism for tracking changes between PRELIMINARY and FINAL versions. Records lists PRELIMINARY and FINAL but does not require a revision log showing what changed. | Procedure.md | Procedure.md#Records | -- | PROPOSAL: Add revision tracking requirement to Records table | TBD |
| E-005 | E:reviewing:wisdom | Conflict | Multi | Guidance | Resolve whether the "high volume air exchanger" (SOW-0036) is exhaust-only, supply-only, or bidirectional (HRV/ERV); Specification REQ-M-003 and REQ-M-004 treat it ambiguously; Guidance T-02 surfaces the conflict but Procedure Step 9 system balance table lists both "Air Exchanger -- Supply" and "Air Exchanger -- Exhaust" as separate line items implying bidirectional operation | This conflict is already partially identified as CON-M-002 in Guidance, but the principled inspection wisdom lens reveals that the Procedure system balance table (Step 9) has already assumed bidirectional operation by listing both supply and exhaust rows for the air exchanger, while the Specification requirements do not commit to this interpretation. The Procedure has pre-decided what CON-M-002 left open. | Specification.md; Procedure.md; Guidance.md | Specification.md#REQ-M-003; Specification.md#REQ-M-004; Procedure.md#Step 9; Guidance.md#T-02; Guidance.md#CON-M-002 | Procedure.md#Step 9 (assumes bidirectional); Guidance.md#CON-M-002 (leaves open) | PROPOSAL: Align Procedure Step 9 system balance table with the unresolved status of CON-M-002; either resolve CON-M-002 first or make the table conditional | TBD |
