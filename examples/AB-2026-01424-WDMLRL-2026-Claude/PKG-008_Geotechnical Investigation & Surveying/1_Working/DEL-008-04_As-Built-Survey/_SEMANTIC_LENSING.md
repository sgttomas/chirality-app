# Semantic Lensing Register: DEL-008-04 As-Built Survey

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-04_As-Built-Survey/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-008-04 Context (Deliverable Identity, Description, Scope)
- _STATUS.md -- DEL-008-04 Status (State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-008-04 Semantic Matrices (A, B, C, F, D, X, E parsed successfully)
- Datasheet.md -- DEL-008-04 Datasheet (Identification, Attributes, Conditions, Construction, References)
- Specification.md -- DEL-008-04 Specification (Scope, Requirements REQ-001 through REQ-008, Standards, Verification, Documentation)
- Guidance.md -- DEL-008-04 Guidance (Purpose, Principles P-1 through P-5, Considerations, Trade-offs)
- Procedure.md -- DEL-008-04 Procedure (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md -- DEL-008-04 References (R-01 RFP, R-07 Appendix C, related deliverables, standards placeholders)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 4
  - Specification: 8
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Accuracy standard gap affects prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Mandatory practices have TBD parameters |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Conformance tolerance undefined |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | AOLS standards not accessible |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-6 cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Verification tolerance TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA review step present in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance links deliverable to CCC process and long-term value |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Verification table covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: What accuracy standard (horizontal and vertical) governs the as-built survey? Consult AOLS standards and Owner. | REQ-005 states accuracy is TBD. Without a prescribed accuracy standard, the normative direction for field work is incomplete. The Surveyor cannot determine compliance without a stated tolerance. | Specification.md | REQ-005 -- Horizontal and Vertical Accuracy | -- | AOLS professional standards + Owner direction (PROPOSAL) | TBD |
| A-002 | A:normative:applying | WeakStatement | Datasheet | Datasheet | Clarify "TBD" entries for Position Datum, Elevation Datum, Instrument Type, Survey Method, Coordinate Format, and Output Format in Attributes table. | Six attributes critical to mandatory practice are listed as TBD. These are not merely unknowns -- they are prerequisites for executing mandatory survey practice. Their absence weakens the normative force of the Datasheet as a descriptive record. | Datasheet.md | Attributes table | -- | Surveyor + Owner at project execution (PROPOSAL) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add numerical tolerance or acceptance criteria for construction conformance verification (REQ-003). Currently "qualitative check" by assumption. | REQ-003 requires conformance verification against IFC drawings but no tolerance is defined. The Verification table entry for REQ-003 references "comparison" without a pass/fail threshold. Compliance determination requires a measurable standard. | Specification.md | REQ-003 -- Construction Verification; Verification table | -- | Owner + Surveyor (PROPOSAL) | TBD |
| A-004 | A:normative:reviewing | TBD_Question | Specification | Specification | Record TBD: Obtain AOLS professional standards, Alberta Surveys Act, and Alberta Land Surveyors Act clause-level requirements applicable to as-built surveys. | The Standards table lists six potentially applicable standards, all marked "Not accessible; location TBD." Without accessible standard text, regulatory audit is not possible. | Specification.md | Standards table | -- | Surveyor (ALS designation holder) (PROPOSAL) | TBD |
| A-005 | A:operative:judging | VerificationGap | Procedure | Procedure | Add specific pass/fail criteria for "Control network closure" check -- currently states "Within stated accuracy tolerance (TBD)". | The Procedure Verification table references a TBD tolerance for closure checks. Without a defined threshold, performance assessment during field work cannot be objectively evaluated. | Procedure.md | Verification table -- Control network closure | -- | Surveyor per AOLS standards (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Critical datum parameters TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available data sources (RFP, appendices) adequately identified |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Output format undefined |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Datum consistency dependency on DEL-008-03 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Context and dependencies provide essential signals |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations section provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for septic system |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Professional surveying expertise requirements stated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | ALS designation assumption covers competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Procedure steps demonstrate thorough field knowledge |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of deliverable purpose is coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section addresses discernment needs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | P-4 and P-5 provide holistic project lifecycle insight |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-1 through P-5 provide consistent reasoning framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add confirmed horizontal and vertical datum identifiers (e.g., NAD83/CGVD2013) once established by DEL-008-03 or confirmed with Owner. | Position Datum and Elevation Datum are both TBD in the Attributes table. These are essential facts for any survey deliverable. The Procedure (Step 1.4) references "NAD83 or provincial grid -- TBD" and "CGVD2013 or local benchmark -- TBD" but no confirmed value exists. | Datasheet.md; Procedure.md | Datasheet Attributes table; Procedure Step 1.4 | -- | DEL-008-03 records + Owner direction (PROPOSAL) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add confirmed Output Format (CAD/PDF/digital data file format) once agreed with Owner. | Output Format is TBD in the Attributes table. Without a defined deliverable format, the comprehensive record function of the Datasheet is incomplete. Guidance GAP-002 and Procedure Step 4.5 both reference this gap. | Datasheet.md; Guidance.md | Datasheet Attributes table; Guidance Conflict Table GAP-002 | -- | Owner direction at project execution (PROPOSAL) | TBD |
| B-003 | B:data:consistency | RationaleGap | Guidance | Guidance | Add rationale for how datum continuity with DEL-008-03 will be verified if DEL-008-03 control points are disturbed during construction. | P-2 states the as-built survey must reference the same datum as DEL-008-03, and Procedure Step 2.1 requires checking closure. However, no guidance addresses the contingency if control points have been disturbed or destroyed. For a construction site at an active landfill, this is a realistic risk. | Guidance.md; Procedure.md | Guidance P-2; Procedure Step 2.1 | -- | Surveyor professional judgment (PROPOSAL) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize septic system terminology: "2,000 US gallon septic holding tank" (Datasheet) vs. "septic holding tank and associated infrastructure" (Specification) vs. "septic system location (holding tank)" (Procedure). Confirm capacity and whether relocation of existing tank is in scope for as-built documentation. | The Datasheet references "2,000 US gallon" capacity and "potentially relocating existing tank" (from RFP s3.4). Specification REQ-002 references "Septic system location" without capacity. Procedure Step 2.3 references "access lid location, approximate tank footprint." The relocation question is mentioned only in Datasheet. Inconsistent granularity risks drift. | Datasheet.md; Specification.md; Procedure.md | Datasheet Construction table; Specification REQ-002; Procedure Step 2.3 | -- | Owner + Surveyor (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 1 | HAS_ITEMS | Survey mandate clear but component scope TBD |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Conformance | 1 | HAS_ITEMS | Conformance demonstration method incomplete |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Requirements REQ-001 through REQ-008 cover regulatory scope |
| C:normative:consistency | normative | consistency | Uniform Regulatory Discipline | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Operational Threshold | 0 | NO_ITEMS | Prerequisites table adequately defines operational thresholds |
| C:operative:sufficiency | operative | sufficiency | Proven Competence | 0 | NO_ITEMS | ALS assumption and calibration requirement cover competence |
| C:operative:completeness | operative | completeness | Integrated Operational Scope | 0 | NO_ITEMS | Steps 1-6 cover full operational scope |
| C:operative:consistency | operative | consistency | Repeatable Process Assurance | 1 | HAS_ITEMS | Deviation classification scheme undefined |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Three downstream purposes clearly stated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Judgment | 0 | NO_ITEMS | Quality judgment framework present in trade-offs |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Lifecycle value articulated in Guidance P-4, P-5 |
| C:evaluative:consistency | evaluative | consistency | Enduring Quality Standard | 0 | NO_ITEMS | Quality standard intent consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-002 note: replace "Exact component list shall be confirmed with the Owner at project execution" with a firmer requirement to document the confirmation and any additions. | REQ-002 lists components but hedges with "ASSUMPTION: all major site components listed in s3.4 shall be documented." The enforceable obligation is weakened by the assumption qualifier. Guidance GAP-003 also flags this. Without confirmed scope, the survey mandate cannot be fully enforced. | Specification.md; Guidance.md | REQ-002 Note; Guidance Conflict Table GAP-003 | -- | Owner + Surveyor (PROPOSAL) | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for how "conformance" is demonstrated when no numerical tolerance exists. Currently REQ-003 verification says "Comparison... discrepancy report if deviations identified" but no threshold for what constitutes a deviation vs. acceptable variance. | Demonstrated Conformance requires a threshold. The Verification table entry for REQ-003 describes a comparison method but does not define what constitutes a passing result. This is linked to but distinct from the accuracy gap (REQ-005). | Specification.md | Verification table -- REQ-003; REQ-003 Note | -- | Owner + Surveyor (PROPOSAL) | TBD |
| C-003 | C:operative:consistency | WeakStatement | Procedure | Procedure | Define deviation classification criteria in Step 3.4: specify what constitutes "within tolerance," "minor," and "material" deviations. Currently these categories are stated without definitions. | Step 3.4 instructs the Surveyor to "Classify deviations as within tolerance (TBD), minor, or material" but provides no classification criteria. Repeatable process assurance requires consistent classification across survey personnel. | Procedure.md | Step 3.4 | -- | Surveyor + PM (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Governance Baseline | 0 | NO_ITEMS | REQ-001 through REQ-008 establish governance baseline |
| F:normative:sufficiency | normative | sufficiency | Adequate Regulatory Proof | 1 | HAS_ITEMS | Proof of ALS designation not addressed |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Register | 0 | NO_ITEMS | Requirements cover identified compliance obligations |
| F:normative:consistency | normative | consistency | Harmonized Governance Framework | 0 | NO_ITEMS | Requirements internally consistent |
| F:operative:necessity | operative | necessity | Essential Performance Parameter | 1 | HAS_ITEMS | Instrument type TBD |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Fitness | 0 | NO_ITEMS | Calibration and QA requirements stated |
| F:operative:completeness | operative | completeness | Total Capability Archive | 0 | NO_ITEMS | Records table in Procedure covers capability documentation |
| F:operative:consistency | operative | consistency | Controlled Process Fidelity | 0 | NO_ITEMS | Process steps internally consistent |
| F:evaluative:necessity | evaluative | necessity | Core Quality Anchor | 0 | NO_ITEMS | Quality anchored to IFC comparison and Owner acceptance |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Appraisal | 0 | NO_ITEMS | Trade-off analysis provides justified basis |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Register | 1 | HAS_ITEMS | Missing lifecycle cost/value consideration |
| F:evaluative:consistency | evaluative | consistency | Grounded Valuation Coherence | 0 | NO_ITEMS | Valuation reasoning consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | MissingSlot | Specification | Procedure | Add prerequisite or verification check confirming the Surveyor holds (or subcontracts to) an ALS-designated professional, per the assumption in the Standards section. | The Specification Standards section states "ASSUMPTION: The Surveyor responsible for DEL-008-04 holds an Alberta Land Surveyor (ALS) designation or sub-contracts to one." However, neither the Procedure prerequisites nor the Verification table includes a check for this. For adequate regulatory proof, this assumption should be verified. | Specification.md; Procedure.md | Specification Standards section (assumption); Procedure Prerequisites table | -- | Project Manager (PROPOSAL) | TBD |
| F-002 | F:operative:necessity | MissingSlot | Datasheet | Datasheet | Add confirmed Instrument Type (total station, GNSS, or other) and Survey Method once determined by the Surveyor. | Instrument Type and Survey Method are TBD in the Datasheet Attributes table. These are essential performance parameters that affect accuracy, cost, and schedule. The Procedure (Step 2.1-2.5) implies GNSS or total station but does not confirm. | Datasheet.md; Procedure.md | Datasheet Attributes table; Procedure Step 2.1-2.5 | -- | Surveyor (PROPOSAL) | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration of the cost/schedule implications of different deliverable format options (CAD vs. PDF vs. digital data) in the trade-offs section. | The Trade-offs table lists "Full CAD drawing set with data files" vs. "PDF drawings only" but provides no analysis of cost, effort, or long-term maintenance value differences. For a comprehensive value register, the rationale for format selection should be more explicit. | Guidance.md | Trade-offs table -- Deliverable format | -- | Owner + Surveyor (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | REQ-001 establishes survey mandate as directive authority |
| D:normative:applying | normative | applying | Binding Implementation Proof | 1 | HAS_ITEMS | No requirement for signed/sealed deliverable |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | REQ-003 + Verification table address conformance judgment |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Alignment | 0 | NO_ITEMS | Owner acceptance step in Procedure covers oversight |
| D:operative:guiding | operative | guiding | Established Operational Benchmark | 0 | NO_ITEMS | P-1, P-2 establish operational benchmarks |
| D:operative:applying | operative | applying | Confirmed Execution Capability | 0 | NO_ITEMS | Prerequisites table confirms execution readiness |
| D:operative:judging | operative | judging | Finalized Effectiveness Verdict | 1 | HAS_ITEMS | Owner acceptance criteria undefined |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Soundness | 0 | NO_ITEMS | Internal QA review (Step 4) confirms procedural soundness |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Foundation | 0 | NO_ITEMS | Three downstream purposes articulated in Guidance |
| D:evaluative:applying | evaluative | applying | Confirmed Worth Realization | 0 | NO_ITEMS | CCC linkage demonstrates worth realization path |
| D:evaluative:judging | evaluative | judging | Final Merit Settlement | 1 | HAS_ITEMS | No criteria for evaluating long-term utility |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Coherence | 0 | NO_ITEMS | Quality appraisal approach adequate in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add requirement or note clarifying whether as-built drawings must be signed and sealed by an ALS. Records table mentions "signed/sealed by ALS if required -- TBD." | The Procedure Records table entry for "As-built drawings" includes "(signed/sealed by ALS if required -- TBD)." For binding implementation proof, whether the deliverable requires professional sealing is a material question that affects legal standing of the record. | Procedure.md; Specification.md | Procedure Records table; Specification Documentation section | -- | Alberta Surveys Act + Owner (PROPOSAL) | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Specification | Add Owner acceptance criteria for the as-built deliverable. Currently Procedure Step 5.4 says "Obtain Owner written acceptance" but no criteria for what constitutes acceptable work are defined. | For a finalized effectiveness verdict, the Owner must have defined acceptance criteria. The Verification table says "As-built drawing set and/or report accepted by Owner as final record" but does not specify what the Owner will evaluate against. | Procedure.md; Specification.md | Procedure Step 5.4; Specification Verification table -- REQ-006 | -- | Owner (PROPOSAL) | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add discussion of how the as-built survey's long-term utility will be evaluated or measured (e.g., usability for future facility modifications, compatibility with County GIS systems). | Guidance identifies three downstream purposes (verification, operational baseline, future modifications) but provides no guidance on how to evaluate whether the deliverable successfully serves these purposes after delivery. For final merit settlement, evaluation criteria for long-term value should be articulated. | Guidance.md | Guidance Purpose section | -- | Owner + Facility Manager (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Reference Basis | 0 | NO_ITEMS | DEL-008-03 dependency provides reference basis |
| X:guiding:sufficiency | guiding | sufficiency | Informed Guidance Standard | 0 | NO_ITEMS | Guidance Principles provide informed standard |
| X:guiding:completeness | guiding | completeness | Exhaustive Orientation Record | 1 | HAS_ITEMS | Examples section empty |
| X:guiding:consistency | guiding | consistency | Stable Orientation Metric | 0 | NO_ITEMS | Principles P-1 through P-5 provide stable orientation |
| X:applying:necessity | applying | necessity | Validated Deployment Baseline | 1 | HAS_ITEMS | Pre-field validation incomplete |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Operational Fitness | 0 | NO_ITEMS | Calibration requirement covers operational fitness |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Archive | 0 | NO_ITEMS | Records table provides comprehensive archive plan |
| X:applying:consistency | applying | consistency | Dependable Performance Measure | 0 | NO_ITEMS | Verification table provides performance measurement framework |
| X:judging:necessity | judging | necessity | Critical Conformance Determination | 1 | HAS_ITEMS | IFC drawing availability not confirmed |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Finding | 0 | NO_ITEMS | Verification approaches defined for each REQ |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Record | 0 | NO_ITEMS | Documentation artifacts list covers assessment records |
| X:judging:consistency | judging | consistency | Coherent Assessment Standard | 0 | NO_ITEMS | Verification methods consistent across requirements |
| X:reviewing:necessity | reviewing | necessity | Critical Soundness Verification | 1 | HAS_ITEMS | No independent review of survey data |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Oversight Audit | 0 | NO_ITEMS | Owner acceptance provides oversight |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Archive | 0 | NO_ITEMS | Records table covers audit trail |
| X:reviewing:consistency | reviewing | consistency | Stable Audit Indicator | 0 | NO_ITEMS | Verification checks are stable and repeatable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add reference examples of as-built survey deliverables or standards (e.g., from AOLS, or similar Camrose County facility projects) when available. | The Guidance Examples section explicitly states "No project-specific as-built survey examples are available" and notes "TBD -- examples may be referenced at project execution." For an exhaustive orientation record, example deliverables would inform the Surveyor's approach. | Guidance.md | Examples section | -- | Surveyor + PM (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | WeakStatement | Procedure | Procedure | Strengthen Step 1.4 datum confirmation: specify that the datum must be confirmed (not left TBD) before field work commences. Add as a prerequisite gate. | Step 1.4 lists datum as "horizontal (NAD83 or provincial grid -- TBD) and vertical (CGVD2013 or local benchmark -- TBD)." This is a pre-field preparation step but the TBD is carried forward without a clear resolution gate. For validated deployment baseline, datum must be confirmed before deployment. | Procedure.md | Step 1.4 | -- | Surveyor + DEL-008-03 records (PROPOSAL) | TBD |
| X-003 | X:judging:necessity | TBD_Question | Multi | TBD | Record TBD: Confirm that IFC drawings will be available to the Surveyor for as-built comparison. Identify who provides them and in what format. | REQ-003 requires comparison against IFC drawings, and Procedure Step 1.2 requires reviewing them. However, no prerequisite explicitly confirms IFC drawing availability, and no document identifies the source or custodian. For critical conformance determination, the reference documents must be secured. | Specification.md; Procedure.md | Specification REQ-003; Procedure Step 1.2; Procedure Prerequisites table | -- | Project Manager / Design team (PROPOSAL) | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add requirement or note addressing whether an independent peer review of survey data is required or recommended (beyond the Surveyor's internal QA). | The Procedure includes an internal QA review (Step 4) but no independent review or third-party check is mentioned. For critical soundness verification of a permanent legal record, independent review may be warranted. The Standards table references professional standards that may require peer review, but these standards are not accessible. | Specification.md; Procedure.md | Specification Standards table; Procedure Step 4 | -- | AOLS professional standards (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Evidence | 0 | NO_ITEMS | Guidance cites RFP and dependencies as evidence |
| E:guiding:information | guiding | information | Reliable Orientation Signal | 0 | NO_ITEMS | Principles provide reliable signals |
| E:guiding:knowledge | guiding | knowledge | Masterful Orientation Command | 0 | NO_ITEMS | Guidance demonstrates adequate domain command |
| E:guiding:wisdom | guiding | wisdom | Principled Navigational Foresight | 0 | NO_ITEMS | Trade-offs and considerations show foresight |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Field notes requirements could be more specific |
| E:applying:information | applying | information | Situated Implementation Status | 0 | NO_ITEMS | Status tracking adequate via milestones |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Procedure demonstrates integrated execution knowledge |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Contingency handling in guidance adequate |
| E:judging:data | judging | data | Conclusive Verdict Evidence | 1 | HAS_ITEMS | Deviation reporting requirements incomplete |
| E:judging:information | judging | information | Situated Verdict Report | 0 | NO_ITEMS | Construction verification report artifact listed |
| E:judging:knowledge | judging | knowledge | Expert Assessment Authority | 0 | NO_ITEMS | ALS assumption covers expert authority |
| E:judging:wisdom | judging | wisdom | Judicious Assessment Foresight | 0 | NO_ITEMS | CCC linkage demonstrates assessment foresight |
| E:reviewing:data | reviewing | data | Confirmed Inspection Record | 0 | NO_ITEMS | Records table covers inspection documentation |
| E:reviewing:information | reviewing | information | Situated Inspection Report | 0 | NO_ITEMS | Report structure defined in Step 3.5 |
| E:reviewing:knowledge | reviewing | knowledge | Expert Inspection Authority | 0 | NO_ITEMS | Professional standards assumption covers authority |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 0 | NO_ITEMS | Guidance links inspection to long-term facility stewardship |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Procedure | Procedure | Standardize field note requirements: Step 2.5 lists "date, weather, instrument type and serial number, crew members, control points used, and any anomalies." The Records table lists "Dated field records: instrument, crew, control points occupied, features collected." Align these two descriptions to a single definitive list. | Two locations in the same document describe field note contents with different item lists. Step 2.5 includes "weather" and "anomalies" which are absent from the Records table description. The Records table includes "features collected" which is absent from Step 2.5. For a verified execution record, the field note requirements should be consistent. | Procedure.md | Step 2.5; Records table -- Field notes | -- | Surveyor (PROPOSAL) | TBD |
| E-002 | E:judging:data | Normalization | Multi | Specification | Clarify what constitutes a "material deviation" requiring a separate deviation table/markup (Procedure Step 3.4) vs. a routine variance. Add definition to Specification or Guidance. | Procedure Step 3.4 instructs preparing a "deviation table or markup if any material deviations are found" and the Records table lists "Deviation table / markup -- If material deviations found." The Documentation section in Specification lists "Construction verification report or summary" but does not reference the deviation table as a separate artifact. The threshold for "material" is undefined. For conclusive verdict evidence, deviation reporting must be consistently defined. | Procedure.md; Specification.md | Procedure Step 3.4; Procedure Records table; Specification Documentation section | -- | PM + Surveyor (PROPOSAL) | TBD |
