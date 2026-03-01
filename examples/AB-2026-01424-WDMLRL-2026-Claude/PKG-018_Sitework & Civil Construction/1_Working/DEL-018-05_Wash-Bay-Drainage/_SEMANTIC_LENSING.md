# Semantic Lensing Register: DEL-018-05 Wash Bay Drainage & Mud Sump

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-05_Wash-Bay-Drainage
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-018-05_Wash-Bay-Drainage/_CONTEXT.md (Deliverable Identity, Scope Summary)
- _STATUS.md — DEL-018-05_Wash-Bay-Drainage/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-018-05_Wash-Bay-Drainage/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-018-05_Wash-Bay-Drainage/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-018-05_Wash-Bay-Drainage/Specification.md (Scope, Requirements REQ-001 through REQ-011, Standards, Verification, Documentation)
- Guidance.md — DEL-018-05_Wash-Bay-Drainage/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-018-05_Wash-Bay-Drainage/Procedure.md (Prerequisites, Steps 1-8, Verification, Records)
- _REFERENCES.md — DEL-018-05_Wash-Bay-Drainage/_REFERENCES.md (R-01, R-07, Cross-References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 2 | HAS_ITEMS | Environmental regulatory gap and code specificity gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Sump dimensions TBD prevents mandatory practice execution |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Environmental compliance verification incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Regulatory audit readiness gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction across all steps |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-8 cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure addresses process audit needs |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification approach in Specification addresses worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Inspection and verification checks adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Identify specific Alberta environmental regulations applicable to wash bay effluent discharge at a landfill site; REQ-009 currently references OBJ-004 but does not identify the governing regulatory framework | REQ-009 is typed as ASSUMPTION and the specific regulatory requirements are TBD; prescriptive direction cannot be established without knowing which regulations apply | Specification.md | REQ-009 -- Environmental Discharge Compliance | -- | PROPOSAL: Alberta Environment and Protected Areas (AEPA) regulatory scoping | TBD |
| A-002 | A:normative:guiding | WeakStatement | Specification | Specification | Specify the applicable edition of the Alberta Building Code and identify specific Safety Code disciplines (plumbing, building) applicable to this drainage work in REQ-008 | REQ-008 references "applicable Alberta building codes" and "Safety Codes" without identifying specific editions or disciplines; this vagueness could lead to different compliance interpretations | Specification.md | REQ-008 -- Code Compliance; Standards table | -- | PROPOSAL: Civil/plumbing engineer to confirm applicable codes | TBD |
| A-003 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record mud sump dimensions, capacity, pipe diameter, and invert elevations once civil/plumbing design is complete; six Physical Parameters are currently TBD | Multiple TBD parameters in the Datasheet prevent mandatory practice from being fully defined; construction cannot proceed without these values | Datasheet.md | Physical Parameters table | -- | PROPOSAL: Civil/plumbing IFC drawings (DEL-005, DEL-006) | TBD |
| A-004 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-009 (Environmental Discharge) specifying what evidence constitutes compliance (e.g., permit obtained, regulatory letter of no objection, effluent monitoring results) | REQ-009 verification says "Environmental permit on file (if required)" but the "if required" qualifier means compliance determination is indeterminate until the regulatory question is answered | Specification.md | Verification table -- REQ-009 | -- | PROPOSAL: Environmental regulatory scoping outcome determines verification approach | TBD |
| A-005 | A:normative:reviewing | MissingSlot | Specification | Specification | Add a requirement or verification item for retention and traceability of regulatory audit documentation (permits, inspection reports, environmental approvals) as a consolidated compliance file | Regulatory audit readiness requires a defined documentation package; the Documentation section lists anticipated artifacts but does not define a consolidated compliance file for audit purposes | Specification.md | Documentation -- Required Artifacts | -- | PROPOSAL: Project Manager / County | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Critical data TBDs in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence from RFP and App B is adequately cited |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing data items |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Measurement basis absent for key parameters |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scope, dependencies, sequencing) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive within available RFP information |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency identified |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core engineering knowledge requirements are identified |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements delegated to P.Eng. per REQ-007 |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery deferred to IFC design phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance provides essential discernment via principles and trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table supports adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight addressed through considerations section |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Record the frost depth value for the site once the geotechnical report (SOW-0001) is available; this is an essential fact for sump and pipe design | Frost depth is referenced in Guidance and Procedure as critical for design but no value is recorded in the Datasheet; it is an essential fact for sizing and burial depth | Datasheet.md | Physical Parameters table | -- | PROPOSAL: Geotechnical report (SOW-0001) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a parameter row for the drainage pipe slope (minimum gradient) required for positive flow from floor drain to sump | Pipe slope/gradient is implied by REQ-003 (positive flow) and Procedure Step 4.2 (design invert slope) but is not recorded as a parameter in the Datasheet | Datasheet.md | Physical Parameters table | -- | PROPOSAL: Civil IFC drawings (DEL-005) | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Guidance | Standardize the term for the sump cover/access arrangement across documents; Guidance uses "open-top or removable-cover", Procedure uses "sump cover or top treatment", Specification uses "open-top or removable-cover configuration" | Inconsistent terminology for the sump access configuration across documents could cause confusion during procurement and construction | Guidance.md, Procedure.md, Specification.md | Guidance: Trade-offs table; Procedure: Step 3.3; Specification: REQ-004 Note | -- | PROPOSAL: Guidance should define the canonical vocabulary | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology for "effluent" vs. "wash water" vs. "discharge" across documents; these terms are used interchangeably but have different regulatory connotations | Datasheet uses "effluent" and "wash water", Specification uses "wash bay effluent" and "environmental discharge", Guidance uses "wash water" and "sediment-laden water"; in a regulatory context these terms may carry different meanings | Datasheet.md, Specification.md, Guidance.md | Datasheet: Conditions -- Operating Context; Specification: REQ-009; Guidance: Purpose paragraph 1 | -- | PROPOSAL: Guidance should define terms; Specification should use consistently | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative Clarity | 1 | HAS_ITEMS | Regulatory imperative unclear for environmental permit |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Conformance Adequacy | 0 | NO_ITEMS | Conformance demonstration is adequate given current TBD state |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 1 | HAS_ITEMS | Regulatory coverage incomplete |
| C:normative:consistency | normative | consistency | Standardized Regulatory Discipline | 0 | NO_ITEMS | Regulatory discipline is consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Operational readiness adequately addressed through prerequisites |
| C:operative:sufficiency | operative | sufficiency | Proficient Execution Assurance | 0 | NO_ITEMS | Execution steps are proficient |
| C:operative:completeness | operative | completeness | Exhaustive Operational Accounting | 1 | HAS_ITEMS | Missing operational step for winter construction |
| C:operative:consistency | operative | consistency | Systematic Operational Uniformity | 0 | NO_ITEMS | Steps are systematically uniform |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Value of the drainage system clearly articulated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Fitness Judgment | 0 | NO_ITEMS | Fitness judgment supported by trade-offs analysis |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation Scope | 0 | NO_ITEMS | Valuation scope covers environmental, operational, and maintenance aspects |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation reasoning is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Guidance | Guidance | Add rationale for why environmental discharge permitting is uncertain (e.g., explain what factors determine whether a permit is required at an Alberta landfill for equipment wash water) to help the design team scope the regulatory inquiry | REQ-009 is marked as ASSUMPTION and CF-002 flags the permit uncertainty, but neither document explains what regulatory factors determine permit applicability; this gap makes regulatory imperative unclear | Guidance.md | Principles -- 4. Environmental Compliance is a Key Driver; Conflict Table CF-002 | -- | PROPOSAL: Environmental consultant or Alberta Environment | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement addressing the sump's structural integrity under frost heave and soil loading conditions, referencing the geotechnical report | The Specification has no requirement for structural performance of the sump pit itself; Guidance mentions frost protection and the Procedure references frost depth, but no normative requirement mandates structural adequacy of the sump under site conditions | Specification.md | entire document scanned -- no structural integrity requirement found | -- | PROPOSAL: Civil/structural engineer via IFC design | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or note addressing cold-weather construction considerations (e.g., concrete curing in sub-zero temperatures, frost protection during open excavation) given the Alberta location and potential for winter construction | The Procedure does not address cold-weather construction despite the Alberta site and December 2026 deadline, which means sump concrete work could occur in freezing conditions | Procedure.md | entire document scanned -- no cold weather provisions found | -- | PROPOSAL: General Contractor construction plan | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Verified Statutory Obligation | 1 | HAS_ITEMS | Statutory obligation not verified for environmental permit |
| F:normative:sufficiency | normative | sufficiency | Grounded Regulatory Justification | 0 | NO_ITEMS | Justification is grounded in RFP for most requirements |
| F:normative:completeness | normative | completeness | Exhaustive Governance Record | 1 | HAS_ITEMS | Governance record gap |
| F:normative:consistency | normative | consistency | Coherent Prescriptive Stability | 0 | NO_ITEMS | Prescriptive requirements are coherently stable |
| F:operative:necessity | operative | necessity | Foundational Process Competence | 0 | NO_ITEMS | Process foundations are competent |
| F:operative:sufficiency | operative | sufficiency | Validated Capability Assurance | 1 | HAS_ITEMS | Capability validation gap |
| F:operative:completeness | operative | completeness | Complete Workflow Mastery | 0 | NO_ITEMS | Workflow is complete within the 8-step structure |
| F:operative:consistency | operative | consistency | Disciplined Performance Stability | 0 | NO_ITEMS | Performance discipline is stable across steps |
| F:evaluative:necessity | evaluative | necessity | Core Quality Awareness | 0 | NO_ITEMS | Quality awareness present through verification approach |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Basis | 1 | HAS_ITEMS | Value basis for discharge approach not defensible without regulatory clarity |
| F:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting is holistic |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification approach for confirming that the specific statutory obligations (Alberta Building Code edition, Safety Code disciplines) have been identified and met, not just that "inspections passed" | REQ-008 verification says "Inspection reports from applicable Safety Code officers" but does not verify that the correct codes were identified in the first place; the statutory obligation is unverified at the identification level | Specification.md | Verification table -- REQ-008 | -- | PROPOSAL: Civil/plumbing engineer confirms applicable codes during design | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for REQ-006 (no alteration of neighbouring drainage) that specifies what survey evidence or engineering analysis is required before and after construction | REQ-006 verification says "Civil engineer review and confirmation" and "survey if required" -- the "if required" qualifier leaves the governance record incomplete; there should be a definitive requirement for pre/post survey comparison | Specification.md | Verification table -- REQ-006 | -- | PROPOSAL: Civil engineer to define survey requirements | TBD |
| F-003 | F:operative:sufficiency | VerificationGap | Procedure | Procedure | Add a hold point or checkpoint in Step 2 (Mud Sump Excavation) requiring geotechnical confirmation of actual soil conditions against design assumptions before proceeding with sump construction | Procedure Step 2.3 mentions notifying the engineer if soil conditions differ, but there is no formal hold point requiring validation of capability (soil bearing capacity, groundwater conditions) before proceeding | Procedure.md | Step 2 -- Mud Sump Excavation, clause 2.3 | -- | PROPOSAL: Geotechnical engineer confirmation | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for how the discharge arrangement trade-off (Trade-offs table, row 3: no overflow vs. engineered overflow) should be evaluated; explain what environmental and operational factors determine acceptability | The trade-off is listed but the basis for choosing between options is not explained beyond "Environmental permitting determines which is acceptable"; a defensible value basis requires more guidance on the evaluation criteria | Guidance.md | Trade-offs table -- Discharge arrangement row | -- | PROPOSAL: Environmental consultant and civil engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Directive Authority | 0 | NO_ITEMS | Directive authority clearly established through RFP and SOW citations |
| D:normative:applying | normative | applying | Enforced Compliance Method | 1 | HAS_ITEMS | Compliance enforcement gap for scope boundary |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 0 | NO_ITEMS | Conformance verdict mechanisms in place via verification |
| D:normative:reviewing | normative | reviewing | Settled Oversight Assurance | 0 | NO_ITEMS | Oversight through County representative and inspection process |
| D:operative:guiding | operative | guiding | Anchored Workflow Guidance | 0 | NO_ITEMS | Workflow guidance anchored in prerequisite and step structure |
| D:operative:applying | operative | applying | Verified Practical Delivery | 1 | HAS_ITEMS | Practical delivery gap for scope boundary documentation |
| D:operative:judging | operative | judging | Settled Effectiveness Ruling | 0 | NO_ITEMS | Effectiveness ruling supported by verification table in Procedure |
| D:operative:reviewing | operative | reviewing | Rigorous Process Examination | 0 | NO_ITEMS | Process examination covered by inspection steps |
| D:evaluative:guiding | evaluative | guiding | Grounded Merit Direction | 0 | NO_ITEMS | Merit direction grounded in Guidance Purpose and Principles |
| D:evaluative:applying | evaluative | applying | Justified Worth Deployment | 0 | NO_ITEMS | Worth deployment justified through trade-offs analysis |
| D:evaluative:judging | evaluative | judging | Settled Merit Adjudication | 1 | HAS_ITEMS | Merit adjudication gap for sump sizing |
| D:evaluative:reviewing | evaluative | reviewing | Principled Fitness Review | 0 | NO_ITEMS | Fitness review addressed through inspection and verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Scope boundary for wash bay floor drain between DEL-018-05 (SOW-0027b, PKG-018) and DEL-014-04 (SOW-0045/SOW-0046, PKG-014) is flagged in Guidance CF-001 but no resolution mechanism is specified in the Specification or Procedure beyond "confirm during contract award" | The enforced compliance method for this deliverable depends on a resolved scope boundary; CF-001 is flagged but the Specification does not condition REQ-002 on CF-001 resolution, creating a potential enforcement gap | Specification.md, Guidance.md | Specification: REQ-002; Guidance: Conflict Table CF-001 | Guidance.md#CF-001 (SOW-0027b vs SOW-0045/SOW-0046) | PROPOSAL: Resolve during contract award; document in Specification REQ-002 | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Strengthen Step 1.3 scope boundary confirmation from "Document the agreed boundary in writing" to specify what document format and who must sign off (e.g., written confirmation letter signed by both GC and Plumbing Contractor, countersigned by Owner) | The scope boundary confirmation is weakly stated; "in writing" is ambiguous regarding formality and could result in an email being treated as equivalent to a formal scope boundary agreement | Procedure.md | Step 1 -- Pre-Construction Coordination, clause 1.3 | -- | PROPOSAL: Project Manager defines documentation standard | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on how to evaluate whether the mud sump sizing is adequate for the operational context (e.g., what cleanout frequency is acceptable, what equipment wash frequency is assumed, what sediment loading rate to expect) | Guidance Considerations mentions "reasonable cleanout interval" and "frequency TBD" but provides no framework for evaluating whether a proposed size represents settled merit; the engineer has no guidance on what constitutes adequate sizing | Guidance.md | Considerations -- Sump Sizing | -- | PROPOSAL: Civil engineer with Owner input on operational expectations | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Imperative Foundational Steering | 0 | NO_ITEMS | Foundational steering present through Guidance Principles |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Competence | 0 | NO_ITEMS | Directional competence justified through design delegation |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Scope | 1 | HAS_ITEMS | Directional scope gap for sediment disposal |
| X:guiding:consistency | guiding | consistency | Coherent Directional Stability | 0 | NO_ITEMS | Direction is coherent and stable across Guidance |
| X:applying:necessity | applying | necessity | Verified Implementation Imperative | 1 | HAS_ITEMS | Implementation imperative gap for backfill specification |
| X:applying:sufficiency | applying | sufficiency | Validated Execution Foundation | 0 | NO_ITEMS | Execution foundation validated through IFC dependency chain |
| X:applying:completeness | applying | completeness | Comprehensive Execution Record | 1 | HAS_ITEMS | Execution record gap |
| X:applying:consistency | applying | consistency | Trustworthy Execution Coherence | 0 | NO_ITEMS | Execution steps are coherent with requirements |
| X:judging:necessity | judging | necessity | Definitive Assessment Finding | 1 | HAS_ITEMS | Assessment finding gap for sump capacity |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Basis | 0 | NO_ITEMS | Adjudication basis justified through verification table |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 0 | NO_ITEMS | Adjudication records defined in Procedure Records section |
| X:judging:consistency | judging | consistency | Stable Adjudication Coherence | 0 | NO_ITEMS | Adjudication criteria consistent between Specification and Procedure |
| X:reviewing:necessity | reviewing | necessity | Vital Oversight Foundation | 0 | NO_ITEMS | Oversight foundation established through County representative requirement |
| X:reviewing:sufficiency | reviewing | sufficiency | Grounded Audit Competence | 0 | NO_ITEMS | Audit competence addressed through inspection reports |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Coverage | 1 | HAS_ITEMS | Audit coverage gap |
| X:reviewing:consistency | reviewing | consistency | Trustworthy Audit Stability | 0 | NO_ITEMS | Audit requirements stable across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add a consideration for sediment disposal procedures post-cleanout, including whether disposal at the landfill itself is permitted or whether the material must be characterized and disposed of as regulated waste | Guidance Considerations mentions sediment disposal at a high level but says "This is a facility operations consideration but the contractor should flag it during design review" without providing directional guidance on the disposal pathway; the exhaustive directional scope is incomplete | Guidance.md | Considerations -- Sediment Disposal | -- | PROPOSAL: Environmental consultant and landfill operator | TBD |
| X-002 | X:applying:necessity | WeakStatement | Procedure | Procedure | Specify the backfill material and compaction standard for drainage pipe burial in Step 4.5; currently says "per IFC specification" but no fallback if IFC is silent on backfill requirements | Procedure Step 4.5 says "Backfill over the drainage pipe in lifts per IFC specification" but IFC drawings are TBD; if IFC drawings do not specify backfill, the Procedure provides no default standard, leaving a verified implementation imperative unmet | Procedure.md | Step 4 -- Drainage Pipe Installation, clause 4.5 | -- | PROPOSAL: Civil engineer specifies in IFC; Procedure should note fallback standard | TBD |
| X-003 | X:applying:completeness | MissingSlot | Datasheet | Datasheet | Add an entry in the Datasheet for the excavator access clearance envelope dimensions (minimum width and height) required around the mud sump | Excavator access clearance is referenced in Specification REQ-004, Guidance Considerations, and Procedure Step 3.4, but no specific dimension is recorded in the Datasheet as a parameter; this data gap means the comprehensive execution record cannot be established | Datasheet.md | Physical Parameters table | -- | PROPOSAL: Civil engineer defines in IFC drawings | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add a verification approach for confirming that the mud sump capacity is adequate for the intended sediment loading and cleanout interval; current verification only addresses location and excavator access, not volumetric adequacy | The Verification table for REQ-001 checks sump location but not capacity; there is no definitive assessment finding possible for whether the sump is sized correctly for the operational context | Specification.md | Verification table -- REQ-001 | -- | PROPOSAL: Civil engineer defines acceptance criteria for capacity | TBD |
| X-005 | X:reviewing:completeness | Conflict | Specification | Specification | Specification Documentation section lists "Environmental discharge permit or equivalent regulatory confirmation (ENV-PERMIT-001) -- if required" as an anticipated artifact, but _DEPENDENCIES.md lists ENV-PERMIT-001 as a pending upstream dependency without the "if required" qualifier; resolve whether the permit is conditional or assumed required | The Specification treats the environmental permit as conditional while _DEPENDENCIES.md treats it as an expected dependency; this inconsistency means audit coverage for environmental compliance is ambiguous | Specification.md, _DEPENDENCIES.md | Specification: Documentation section; Procedure: Prerequisites table (ENV-PERMIT-001) | Specification.md#Documentation vs Procedure.md#Prerequisites (ENV-PERMIT-001 conditionality) | PROPOSAL: Resolve via regulatory scoping per CF-002 | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directional Evidence | 1 | HAS_ITEMS | Directional evidence gap for cleanout frequency |
| E:guiding:information | guiding | information | Contextualized Steering Clarity | 0 | NO_ITEMS | Steering clarity adequate through Guidance context |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Guidance Mastery | 0 | NO_ITEMS | Guidance mastery adequate for current phase |
| E:guiding:wisdom | guiding | wisdom | Prudent Directional Foresight | 1 | HAS_ITEMS | Foresight gap for long-term maintenance |
| E:applying:data | applying | data | Proven Delivery Evidence | 1 | HAS_ITEMS | Delivery evidence gap |
| E:applying:information | applying | information | Contextualized Delivery Clarity | 0 | NO_ITEMS | Delivery context adequate |
| E:applying:knowledge | applying | knowledge | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution mastery deferred to IFC phase |
| E:applying:wisdom | applying | wisdom | Prudent Execution Foresight | 0 | NO_ITEMS | Execution foresight addressed through trade-offs |
| E:judging:data | judging | data | Definitive Ruling Evidence | 0 | NO_ITEMS | Ruling evidence framework in place |
| E:judging:information | judging | information | Contextualized Judgment Clarity | 0 | NO_ITEMS | Judgment context adequate |
| E:judging:knowledge | judging | knowledge | Comprehensive Adjudication Mastery | 0 | NO_ITEMS | Adjudication mastery adequate |
| E:judging:wisdom | judging | wisdom | Prudent Evaluative Foresight | 0 | NO_ITEMS | Evaluative foresight present in Guidance |
| E:reviewing:data | reviewing | data | Verified Oversight Evidence | 1 | HAS_ITEMS | Oversight evidence gap |
| E:reviewing:information | reviewing | information | Contextualized Oversight Clarity | 0 | NO_ITEMS | Oversight context adequate |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Review Mastery | 0 | NO_ITEMS | Review mastery adequate |
| E:reviewing:wisdom | reviewing | wisdom | Prudent Oversight Foresight | 0 | NO_ITEMS | Oversight foresight present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | TBD_Question | Datasheet | Datasheet | Record the assumed cleanout frequency or sediment accumulation rate for the mud sump; this is an essential datum for sizing validation and maintenance planning | The Datasheet Conditions table lists cleanout frequency as TBD/ASSUMPTION but never resolves it; this data gap prevents verified directional evidence for sump sizing and maintenance planning | Datasheet.md | Conditions -- Operating Context (Cleanout Frequency) | -- | PROPOSAL: Owner to define operational expectations; engineer to validate | TBD |
| E-002 | E:guiding:wisdom | TBD_Question | Guidance | Guidance | Add a forward-looking consideration addressing long-term maintenance access if future site development encroaches on the sump excavator access zone; recommend a maintenance easement or exclusion zone notation on site plans | Guidance addresses excavator access clearance as a design consideration but does not address the foresight question of whether future site changes could compromise access; prudent directional foresight requires considering this risk | Guidance.md | Considerations -- Excavator Access Clearance | -- | PROPOSAL: Owner/site planner to define long-term access protection | TBD |
| E-003 | E:applying:data | Normalization | Datasheet | Datasheet | Reconcile the floor drain count: Datasheet says "one drain shown on App B (Plumbing)" while Specification REQ-002 and Procedure Step 5.1 use "floor drain(s)" in plural; clarify whether one or multiple drains are expected | The parenthetical "(s)" usage creates ambiguity about whether the system has one drain or multiple; this affects pipe sizing and connection design | Datasheet.md, Specification.md, Procedure.md | Datasheet: Physical Parameters (Floor Drain Count); Specification: REQ-002; Procedure: Step 5.1 | -- | PROPOSAL: Plumbing IFC drawings (DEL-006-03) resolve count | TBD |
| E-004 | E:reviewing:data | TBD_Question | Datasheet | Datasheet | Record the as-built survey requirements (what specific points must be surveyed, to what accuracy) for the sump and drainage pipe; the Datasheet References section mentions DEL-008-04 (as-built survey) but does not specify what measurements are required | The as-built survey is listed as an anticipated artifact in Specification and as a record in Procedure, but the specific survey scope (what to measure, what tolerances) is not defined; this leaves verified oversight evidence incomplete | Specification.md, Procedure.md | Specification: Documentation section (As-built survey); Procedure: Records table (As-built survey data) | -- | PROPOSAL: Civil engineer defines survey scope | TBD |
