# Semantic Lensing Register: DEL-013-06 Ceiling Fans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-06_Ceiling-Fans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-013-06_Ceiling-Fans/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements, Related Deliverables)
- _STATUS.md — DEL-013-06_Ceiling-Fans/_STATUS.md (Current Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-013-06_Ceiling-Fans/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed; 96 cells total)
- Datasheet.md — DEL-013-06_Ceiling-Fans/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-013-06_Ceiling-Fans/Specification.md (Scope, Requirements REQ-013-06-01 through REQ-013-06-12, Standards, Verification, Documentation)
- Guidance.md — DEL-013-06_Ceiling-Fans/Guidance.md (Purpose, Principles P1-P5, Considerations, Trade-offs, Conflict Table CF-013-06-01 and CF-013-06-02)
- Procedure.md — DEL-013-06_Ceiling-Fans/Procedure.md (Prerequisites, Steps 1-8, Verification, Records)
- _REFERENCES.md — DEL-013-06_Ceiling-Fans/_REFERENCES.md (Primary References R-01 R-04, Standard References, Approval Documents)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 4
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 3  X: 6  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive authority for fan type selection |
| A:normative:applying | normative | applying | mandatory practice | 2 | HAS_ITEMS | Noise limit and clearance values TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standard clause references incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Safety Code inspection and permit process covered adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced with prerequisites |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Torque specification absent for mounting fasteners |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Commissioning verification table in Procedure is adequate |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table provides audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section articulates value well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table addresses merit comparison |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | No additional worth-determination gaps found |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Submittal review and commissioning provide quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether HVLS fan type is a requirement or recommendation; current language in Guidance P2 says "HVLS ... are the standard industrial solution" but Specification REQ-013-06-08 only says "industrial or heavy-commercial grade" without mandating HVLS | Guidance strongly implies HVLS is the correct product type but the normative document does not prescribe it, creating ambiguity about whether a bidder could propose standard high-speed fans and still comply | Specification.md; Guidance.md | REQ-013-06-08; Guidance P2 and Considerations "HVLS vs. Standard Industrial Fan" | -- | PROPOSAL: Mechanical Engineer to determine; Specification should state minimum performance criteria that effectively select fan type | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Add specific numeric noise limit (dBA at a defined distance/condition) for REQ-013-06-10; current language "acceptable for a maintenance shop work environment" is subjective and unenforceable | Without a numeric threshold, compliance determination for noise is purely subjective; different parties may have incompatible interpretations of "acceptable" | Specification.md | REQ-013-06-10 | -- | PROPOSAL: Mechanical Engineer to specify dBA limit or reference applicable occupational noise standard | TBD |
| A-003 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Specific minimum blade-to-floor clearance value (REQ-013-06-07) and minimum blade-to-crane-envelope clearance (REQ-013-06-06) are both stated as code-dependent but no specific code clause or numeric value is cited | These clearance values are critical safety constraints that cannot be verified without numeric thresholds; the applicable code clause must be identified | Specification.md | REQ-013-06-06; REQ-013-06-07 | -- | PROPOSAL: Safety Codes Officer or Mechanical Engineer to identify applicable Alberta Building Code / Safety Code clause and extract numeric clearance minima | TBD |
| A-004 | A:normative:judging | MissingSlot | Specification | Specification | Add specific Alberta Building Code clause references in Standards table; current entries say "Location TBD" for ABC, AEC, and CSA C22.2 No. 113 | Compliance determination requires knowing which clauses apply; "Location TBD" defers this indefinitely and blocks verification planning | Specification.md | Standards table | -- | PROPOSAL: Design-Builder's P.Eng. to identify applicable clauses during design phase | TBD |
| A-005 | A:operative:applying | MissingSlot | Procedure | Procedure | Add fastener torque verification criteria to Step 5.7; current check says "All mounting fasteners torqued" but does not reference manufacturer torque specifications or a torque value | Practical execution of the pre-energisation inspection requires knowing what torque values to verify against; without this, the check is unverifiable | Procedure.md | Step 5.7 | -- | PROPOSAL: Source from manufacturer installation instructions once equipment is selected | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Fan position coordinates are essential facts that are TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Voltage/amperage assumption lacks evidence |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet comprehensively catalogs known and TBD attributes |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements that exist are consistently sourced |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key information signals (quantity, location, ceiling height) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each TBD is adequately described |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive narrative of the deliverable |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Ceiling structure type inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding of destratification, HVLS, and crane clearance is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance demonstrates competent domain expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No additional knowledge gaps beyond those captured elsewhere |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Technical understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment points (crane clearance priority, scope interface) are captured in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table shows adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view captured across Guidance Considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Individual fan position coordinates (6 positions) must be determined; currently "TBD -- individual fan positions not explicitly shown on App B-Elec drawing" | Fan positions are essential facts for structural approval, electrical rough-in, and crane clearance verification; all downstream steps depend on this data | Datasheet.md | Attributes table, "Fan Positions (Layout)" row | -- | PROPOSAL: Mechanical Engineer to determine during design phase per Procedure Step 3 | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Strengthen evidence basis for Voltage/Amperage assumption; currently marked "ASSUMPTION: 120V single-phase" but HVLS fans (if selected per Guidance P2) typically require 208V/240V or 480V three-phase power | The assumption of 120V single-phase may be incorrect if HVLS fans are selected, which would materially change electrical circuit design (DEL-015 interface); the assumption should be flagged as potentially invalid | Datasheet.md | Attributes table, "Voltage / Amperage per Fan" row | -- | PROPOSAL: Confirm with Mechanical Engineer and fan manufacturer once product is selected; update Datasheet and coordinate with DEL-015 | TBD |
| B-003 | B:information:consistency | Conflict | Multi | Datasheet | Resolve ceiling structure type: Datasheet Conditions says "Concrete structure" (sourced to App B-Shop R-04) but Guidance P4 refers to "structural ceiling/purlin/beam" and Specification REQ-013-06-05 says "ceiling mounting structure (structural attachment point)"; Procedure Step 3.1 references "structural ceiling attachment points" and "purlin" -- a concrete ceiling and a purlin/beam structure are different mounting conditions | If the ceiling is indeed concrete (cast-in-place or precast), mounting requires concrete anchors and expansion bolts; if it is steel purlin/beam, mounting requires beam clamps or welded brackets; incorrect assumption affects structural design and safety | Datasheet.md; Guidance.md; Specification.md; Procedure.md | Datasheet Conditions "Ceiling Structure Type"; Guidance P4; Specification REQ-013-06-05; Procedure Step 3.1 | Datasheet.md#Conditions ("Concrete structure") vs. Guidance.md#P4 ("structural ceiling/purlin/beam") vs. Procedure.md#Step 3.1 ("structural ceiling attachment points ... purlin") | PROPOSAL: Verify against structural drawings (DEL-002) to confirm actual ceiling structure type; update Datasheet accordingly | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Threshold | 1 | HAS_ITEMS | Direction reversal requirement status ambiguous |
| C:normative:sufficiency | normative | sufficiency | Certified Regulatory Adequacy | 0 | NO_ITEMS | Regulatory adequacy path (permits, inspections) is clear |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Mechanical permit requirement unclear |
| C:normative:consistency | normative | consistency | Uniform Regulatory Fidelity | 0 | NO_ITEMS | Regulatory references are consistently applied across documents |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Missing prerequisite for crane status |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Readiness | 0 | NO_ITEMS | Readiness conditions are well-defined in prerequisites table |
| C:operative:completeness | operative | completeness | Comprehensive Execution Coverage | 0 | NO_ITEMS | Steps 1-8 provide comprehensive execution coverage |
| C:operative:consistency | operative | consistency | Dependable Process Repeatability | 0 | NO_ITEMS | Procedure is sequenced logically and consistently |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Core value proposition (destratification, comfort) is established |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Adequacy | 0 | NO_ITEMS | Merit justification in Guidance Purpose is adequate |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Accounting | 0 | NO_ITEMS | Full value accounting present in Guidance |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value propositions are coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify whether direction reversal in REQ-013-06-11 is mandatory or recommended; current language says "Reversal of direction ... is recommended" but Verification table says "Both forward and reverse modes confirmed operational" implying it is mandatory for acceptance | If reversal is only "recommended" then verification should not mandate it; if it is required, the requirement should use "shall" language | Specification.md | REQ-013-06-11; Verification table row for Step 7.1 | Specification.md#REQ-013-06-11 ("recommended") vs. Procedure.md#Verification ("Both forward and reverse modes confirmed operational") | PROPOSAL: Mechanical Engineer to rule on whether reversibility is mandatory; update REQ-013-06-11 language accordingly | TBD |
| C-002 | C:normative:completeness | TBD_Question | Specification | Specification | Record TBD: Determine whether a separate mechanical Safety Code permit is required for ceiling fan installation in addition to the electrical permit; Specification Standards table lists "Alberta Safety Codes Act" generally but Procedure Step 6 only addresses electrical inspection | If a mechanical permit is also required and is not obtained, the installation may be non-compliant with Alberta Safety Codes Act | Specification.md; Procedure.md | Specification Standards table; Procedure Step 6 | -- | PROPOSAL: Confirm with Safety Codes Officer whether mechanical permit is required for ceiling-mounted fan installation in Alberta | TBD |
| C-003 | C:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite: Confirm overhead crane installation status and whether cranes are operational/installed before fan installation begins; Step 7.6 assumes cranes are available for combined operation test but no prerequisite confirms crane readiness | If fans are installed before cranes, Step 7.6 (crane/fan combined test) cannot be completed at commissioning; if cranes are installed first, crane envelope must be verified before fan mounting positions are finalized | Procedure.md | Prerequisites table; Step 7.6 | -- | PROPOSAL: Add prerequisite referencing DEL-016 crane installation status and sequencing with fan installation | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Assurance Baseline | 1 | HAS_ITEMS | Vibration acceptance threshold not specified |
| F:normative:sufficiency | normative | sufficiency | Mandated Proof Authority | 0 | NO_ITEMS | Documentation artifacts for proof authority are well-defined |
| F:normative:completeness | normative | completeness | Total Assurance Registry | 1 | HAS_ITEMS | Warranty duration not specified |
| F:normative:consistency | normative | consistency | Standardized Assurance Discipline | 0 | NO_ITEMS | Assurance discipline is consistent |
| F:operative:necessity | operative | necessity | Essential Readiness Threshold | 0 | NO_ITEMS | Prerequisites table defines readiness thresholds |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Preparedness | 1 | HAS_ITEMS | No hold point for structural approval before proceeding |
| F:operative:completeness | operative | completeness | Total Execution Accounting | 0 | NO_ITEMS | Steps 1-8 with verification table provide total execution accounting |
| F:operative:consistency | operative | consistency | Stable Execution Discipline | 0 | NO_ITEMS | Execution discipline is stable and well-sequenced |
| F:evaluative:necessity | evaluative | necessity | Warranted Value Baseline | 0 | NO_ITEMS | Value baseline established in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Worth Justification | 0 | NO_ITEMS | Worth justification demonstrated through destratification and comfort rationale |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Documentation | 1 | HAS_ITEMS | Energy savings claim unsubstantiated |
| F:evaluative:consistency | evaluative | consistency | Sound Quality Alignment | 0 | NO_ITEMS | Quality alignment is sound across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add vibration acceptance threshold for REQ-013-06-12; current verification is "vibration observation at all speeds" and Procedure Step 7.3 says "vibration is within manufacturer limits" but no manufacturer limits are referenced in the Specification and no measurable threshold is stated | Without a defined vibration threshold (e.g., mm/s or manufacturer-specified limit), the verification is subjective and different inspectors may reach different conclusions | Specification.md; Procedure.md | REQ-013-06-12 Verification; Procedure Step 7.3 | -- | PROPOSAL: Reference manufacturer vibration limits once equipment is selected; add measurable pass/fail criterion to Specification | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add warranty requirements: minimum warranty period, warranty scope (parts/labor/both), and warranty start date; Procedure Step 8.2 mentions "Warranty documentation" in O&M manuals and Records table lists "Fan warranty certificates" but Specification has no warranty requirement | Warranty is part of the total assurance registry for this deliverable; without a specified minimum warranty period, the Owner has no basis to evaluate or enforce warranty terms | Specification.md; Procedure.md | Specification Documentation section; Procedure Records table "Fan warranty certificates" | -- | PROPOSAL: Add warranty requirement to Specification (e.g., minimum 1-year manufacturer warranty); confirm Owner expectations | TBD |
| F-003 | F:operative:sufficiency | VerificationGap | Procedure | Procedure | Add explicit hold point or sign-off gate after Step 3.2 (structural approval) before proceeding to Step 5 (installation); current procedure implies sequencing but does not create a formal hold point that prevents proceeding without structural approval | Without a formal hold point, there is risk that installation proceeds before structural engineer approval is confirmed, creating a safety and compliance gap | Procedure.md | Step 3.2; Step 5.1 | -- | PROPOSAL: Add "HOLD POINT: Do not proceed to Step 5 without documented structural engineer approval from Step 3.2" | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Substantiate energy savings claim in Considerations "Winter Destratification Savings" section; current text says "potentially reducing heating energy consumption significantly" but acknowledges "no specific energy model from sources is available" | An unsubstantiated energy savings claim could mislead cost-benefit analysis; either remove the claim, qualify it more carefully, or add a reference to an industry source | Guidance.md | Considerations, "Winter Destratification Savings" | -- | PROPOSAL: Add reference to published industry data on destratification energy savings in high-ceiling industrial spaces, or explicitly label as qualitative expectation only | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 1 | HAS_ITEMS | Scope authority conflict between RFP and App B-Elec |
| D:normative:applying | normative | applying | Enforced Verification Duty | 0 | NO_ITEMS | Verification duties are clearly assigned in Specification Verification table |
| D:normative:judging | normative | judging | Binding Conformance Verdict | 0 | NO_ITEMS | Conformance determination methods are defined for each requirement |
| D:normative:reviewing | normative | reviewing | Mandated Discipline Examination | 0 | NO_ITEMS | Safety Code inspection process provides discipline examination |
| D:operative:guiding | operative | guiding | Established Workflow Gate | 1 | HAS_ITEMS | Submittal approval timing relative to procurement |
| D:operative:applying | operative | applying | Resolved Task Enactment | 0 | NO_ITEMS | Task steps are well-resolved with clear actions |
| D:operative:judging | operative | judging | Resolved Performance Ruling | 0 | NO_ITEMS | Performance ruling criteria in verification table |
| D:operative:reviewing | operative | reviewing | Disciplined Workflow Review | 0 | NO_ITEMS | Workflow review points are adequate |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Anchor | 0 | NO_ITEMS | Worth anchor established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Resolved Merit Deployment | 1 | HAS_ITEMS | Control type decision deferred without resolution criteria |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | Worth determination criteria are implicit in commissioning pass/fail |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Inspection | 0 | NO_ITEMS | Quality inspection process is defined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Specification | Guidance | Existing conflict CF-013-06-01 in Guidance Conflict Table: ceiling fans appear in App B-Elec (R-05) but not in RFP Section 3.4 Design Requirements text; the directive authority for this deliverable rests on SOW-0040 decomposition, but the gap between RFP body text and appendix drawing creates ambiguity about mandatory status | If a dispute arises, the absence from RFP Section 3.4 could be used to argue fans are optional; the Guidance Conflict Table correctly surfaces this but it remains unresolved (HumanRuling = TBD) | Guidance.md; Specification.md | Guidance Conflict Table CF-013-06-01; Specification REQ-013-06-01 | Guidance.md#CF-013-06-01 ("R-05 App B-Elec: '6 Ceiling Fans for Main Shop'") vs. Guidance.md#CF-013-06-01 ("R-01 RFP Section 3.4: no explicit mention") | PROPOSAL: Treat as mandatory per SOW-0040; obtain Owner written confirmation | TBD |
| D-002 | D:operative:guiding | VerificationGap | Procedure | Procedure | Add verification check confirming that equipment procurement does not proceed before submittal approval (Step 2.3); current workflow states "Obtain Owner/Engineer written approval ... before ordering equipment" but the Verification table has no corresponding check row for Step 2.3 ordering gate | The Verification table checks Step 2.3 for "Equipment submittal approved" but does not verify that ordering was held pending approval; if ordering proceeds before approval, non-compliant equipment may arrive on site | Procedure.md | Step 2.3; Verification table | -- | PROPOSAL: Add verification row confirming purchase order date is after submittal approval date | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add decision criteria for resolving the control type trade-off (individual wall switches vs. centralized control panel); current Trade-offs table says "TBD -- centralized preferred for operator ease" without providing evaluation criteria or who decides | Without decision criteria, this trade-off cannot be resolved by the contractor; it needs Owner input on operational preferences and budget implications | Guidance.md | Trade-offs table, "Control type" row | -- | PROPOSAL: Add evaluation criteria (e.g., operational simplicity, cost, maintainability) and identify decision-maker (Owner/Mechanical Engineer) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Imperative | 0 | NO_ITEMS | Steering imperatives (safety, code compliance) are established |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Pathway Guidance | 1 | HAS_ITEMS | Temperature uniformity acceptance undefined |
| X:guiding:completeness | guiding | completeness | Complete Governance Repository | 0 | NO_ITEMS | Governance documents (permits, approvals, submittals) are enumerated |
| X:guiding:consistency | guiding | consistency | Unified Steering Alignment | 0 | NO_ITEMS | Steering is unified across documents |
| X:applying:necessity | applying | necessity | Critical Validation Basis | 1 | HAS_ITEMS | Air circulation verification lacks measurable criteria |
| X:applying:sufficiency | applying | sufficiency | Qualified Validation Evidence | 1 | HAS_ITEMS | Commissioning observation is subjective for several checks |
| X:applying:completeness | applying | completeness | Exhaustive Validation Record | 0 | NO_ITEMS | Commissioning report template captures all required checks |
| X:applying:consistency | applying | consistency | Calibrated Action Consistency | 0 | NO_ITEMS | Verification actions are consistently defined |
| X:judging:necessity | judging | necessity | Critical Compliance Finding | 1 | HAS_ITEMS | CSA product certification verification missing |
| X:judging:sufficiency | judging | sufficiency | Substantiated Compliance Judgment | 0 | NO_ITEMS | Compliance judgment is substantiated by inspection reports |
| X:judging:completeness | judging | completeness | Complete Adjudication Record | 0 | NO_ITEMS | Adjudication records enumerated in Documentation section |
| X:judging:consistency | judging | consistency | Harmonized Adjudication Standard | 0 | NO_ITEMS | Adjudication standards are harmonized |
| X:reviewing:necessity | reviewing | necessity | Critical Inspection Basis | 1 | HAS_ITEMS | Scope of mechanical inspection unclear |
| X:reviewing:sufficiency | reviewing | sufficiency | Qualified Audit Evidence | 0 | NO_ITEMS | Audit evidence requirements are qualified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Repository | 1 | HAS_ITEMS | Photo documentation not specified |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Protocol | 0 | NO_ITEMS | Audit protocol is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add measurable acceptance criterion for REQ-013-06-03 air circulation function; current verification is "Commissioning observation; temperature uniformity TBD" with an assumption of "functional test confirming perceptible air movement at floor level" -- "perceptible" is not measurable | Without a defined pass/fail criterion (e.g., minimum air velocity at occupied zone height, or maximum temperature differential floor-to-ceiling), the functional verification is unsubstantiated and may be disputed | Specification.md | REQ-013-06-03 Verification | -- | PROPOSAL: Define measurable criterion such as minimum air velocity (m/s) at 1.5m height or maximum temperature differential (degrees C) between floor and ceiling during heating season | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add measurable acceptance criterion for noise verification (REQ-013-06-10); current verification is "Commissioning observation" and "manufacturer spec review" but no measurement method or threshold is specified | Critical validation basis for noise requires a measurement method (e.g., sound level meter at specified distance) and a pass/fail threshold; without this, noise compliance cannot be objectively validated | Specification.md | REQ-013-06-10 Verification; Procedure Step 7.5 | -- | PROPOSAL: Specify measurement method (e.g., dBA at 1.5m floor level, all fans running) and threshold; alternatively, reference applicable occupational health standard | TBD |
| X-003 | X:applying:sufficiency | WeakStatement | Procedure | Specification | Strengthen commissioning observation for HVAC integration (Procedure Step 7.4); current check is "No adverse interaction observed" which relies on subjective observation without defining what constitutes "adverse interaction" | Qualified validation evidence requires defining observable indicators of adverse interaction (e.g., exhaust capture efficiency reduction, thermostat cycling, pressure imbalance at exhaust hoods) | Procedure.md; Specification.md | Procedure Step 7.4; Specification REQ-013-06-09 Verification | -- | PROPOSAL: Define specific observable indicators of adverse interaction for commissioning test protocol | TBD |
| X-004 | X:judging:necessity | MissingSlot | Specification | Specification | Add requirement for CSA or equivalent product safety certification for ceiling fans (e.g., CSA C22.2 No. 113 or UL 507); Standards table lists CSA C22.2 No. 113 as "ASSUMPTION: likely applicable" but no requirement mandates certified/listed equipment | Product safety certification is a critical compliance finding that should be a mandatory requirement, not an assumption; uncertified equipment may not be accepted by the electrical inspector | Specification.md | Standards table "CSA C22.2 No. 113" row; REQ-013-06-08 | -- | PROPOSAL: Add explicit requirement that all ceiling fans must bear CSA, UL, or equivalent product safety certification | TBD |
| X-005 | X:reviewing:necessity | MissingSlot | Procedure | Procedure | Add step or note clarifying whether mechanical Safety Code inspection is required in addition to electrical inspection; Step 6 only addresses electrical inspection | If mechanical inspection is required (see C-002) and is not included in the procedure, a required inspection may be missed | Procedure.md | Step 6 | -- | PROPOSAL: Add conditional step: "If mechanical Safety Code inspection is required, request and complete mechanical inspection before commissioning" | TBD |
| X-006 | X:reviewing:completeness | MissingSlot | Specification | Specification | Add requirement for photographic documentation of installation stages (mounting brackets installed, structural connections, pre-energisation state) as part of the commissioning/close-out package | Photo documentation provides an exhaustive audit repository for hidden conditions (structural connections behind finished surfaces) that cannot be reinspected after completion | Specification.md | Documentation section | -- | PROPOSAL: Add "Installation photographs" to Documentation artifacts table | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Documented Direction Authority | 1 | HAS_ITEMS | Reference document R-05 description inconsistent |
| E:guiding:information | guiding | information | Authoritative Governance Signal | 0 | NO_ITEMS | Governance signals are authoritative and consistent |
| E:guiding:knowledge | guiding | knowledge | Mastered Governance Competence | 0 | NO_ITEMS | Governance competence is demonstrated |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Governance | 0 | NO_ITEMS | Strategic governance is principled |
| E:applying:data | applying | data | Documented Verification Artifact | 1 | HAS_ITEMS | As-built vs IFC drawing relationship unclear |
| E:applying:information | applying | information | Actionable Verification Narrative | 0 | NO_ITEMS | Verification narratives are actionable |
| E:applying:knowledge | applying | knowledge | Commanding Verification Mastery | 0 | NO_ITEMS | Verification procedures demonstrate adequate mastery |
| E:applying:wisdom | applying | wisdom | Judicious Verification Insight | 0 | NO_ITEMS | Verification approach shows judicious insight |
| E:judging:data | judging | data | Proven Conformance Ruling | 1 | HAS_ITEMS | IP/NEMA rating requirement missing from Specification |
| E:judging:information | judging | information | Contextual Ruling Narrative | 0 | NO_ITEMS | Ruling narratives have adequate context |
| E:judging:knowledge | judging | knowledge | Commanding Adjudication Expertise | 0 | NO_ITEMS | Adjudication expertise is adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Adjudication principles are sound |
| E:reviewing:data | reviewing | data | Verified Audit Substantiation | 1 | HAS_ITEMS | Maintenance access plan not in close-out package |
| E:reviewing:information | reviewing | information | Comprehensive Audit Communication | 0 | NO_ITEMS | Audit communication is comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | Commanding Audit Expertise | 0 | NO_ITEMS | Audit expertise is adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Discernment | 0 | NO_ITEMS | Audit discernment is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Normalize reference to App B-Elec across documents; Datasheet References table calls it "AB-2026-01424-Appendix B (Electrical).pdf" with ref ID R-05; _REFERENCES.md calls it "R-04: Shop Floor Plan" for facility layout but does not list R-05 at all; _REFERENCES.md lists "R-01: Main RFP Section 3.4 HVAC" while Datasheet lists R-01 as the full RFP | _REFERENCES.md is incomplete relative to Datasheet: it does not list R-05 (App B-Elec) which is a primary source for this deliverable, and its R-04 description differs from Datasheet R-04 description | Datasheet.md; _REFERENCES.md | Datasheet References table; _REFERENCES.md Primary References | Datasheet.md#References ("R-05: AB-2026-01424-Appendix B (Electrical).pdf") vs. _REFERENCES.md#Primary References (R-05 not listed) | PROPOSAL: Update _REFERENCES.md to include R-05 and align reference descriptions with Datasheet | TBD |
| E-002 | E:applying:data | Normalization | Multi | Specification | Clarify relationship between IFC Layout Drawing and As-Built Drawing in Documentation artifacts; both are listed separately but the expected content overlap and update process is not described | Understanding which drawing is the "record" drawing at handover is important for future maintenance access; as-built should clearly supersede IFC | Specification.md | Documentation section, "IFC Layout Drawing" and "As-Built Drawing" rows | -- | PROPOSAL: Add note in Documentation section clarifying that As-Built Drawing supersedes IFC Layout Drawing and must reflect all field changes | TBD |
| E-003 | E:judging:data | RationaleGap | Specification | Specification | Add IP or NEMA enclosure rating requirement for fan motors; REQ-013-06-08 says "industrial or heavy-commercial grade, suitable for continuous operation in a shop environment subject to dust, vehicle exhaust, welding fumes, and temperature cycling" but does not specify a minimum IP/NEMA rating | Without a minimum IP/NEMA rating, conformance ruling for equipment durability is subjective; the environmental conditions described (dust, exhaust, fumes) suggest at least IP44 or NEMA 3/12 would be appropriate | Specification.md; Datasheet.md | Specification REQ-013-06-08; Datasheet Attributes "Finish / Material" and Conditions "Operating Environment" | -- | PROPOSAL: Specify minimum IP rating (e.g., IP44) or NEMA rating appropriate for the operating environment; confirm with Mechanical Engineer | TBD |
| E-004 | E:reviewing:data | Normalization | Guidance | Specification | Address maintenance access planning raised in Guidance Considerations "Maintenance Access" section; Guidance identifies that 35 ft height requires elevated access equipment and questions whether gantry cranes can be used, but this is not reflected in Specification requirements or Procedure close-out documentation | Maintenance access is a long-term operational concern that should be documented in the O&M manual requirements (Specification Documentation) or addressed as a deliverable design consideration | Guidance.md; Specification.md | Guidance Considerations "Maintenance Access"; Specification Documentation section "O&M Manuals" | -- | PROPOSAL: Add requirement in Specification Documentation that O&M manuals must include maintenance access method and recommended access equipment for 35 ft ceiling height | TBD |
