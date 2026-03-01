# Semantic Lensing Register: DEL-001-07 Door & Window Schedule

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-07_Door-Window-Schedule/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-07_Door-Window-Schedule/_CONTEXT.md
- _STATUS.md — DEL-001-07_Door-Window-Schedule/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-07_Door-Window-Schedule/_SEMANTIC.md
- Datasheet.md — DEL-001-07_Door-Window-Schedule/Datasheet.md
- Specification.md — DEL-001-07_Door-Window-Schedule/Specification.md
- Guidance.md — DEL-001-07_Door-Window-Schedule/Guidance.md
- Procedure.md — DEL-001-07_Door-Window-Schedule/Procedure.md
- _REFERENCES.md — DEL-001-07_Door-Window-Schedule/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 4
  - Procedure: 6
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 4  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 9
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Fire rating prescriptive direction missing |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Overhead door height TBD blocks mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC compliance verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 6 QA review and Step 8 inspection cover this adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Mechanical coordination not in Procedure prerequisites |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-8 cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure Verification table covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Step 6 internal QA review is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No rationale for hardware durability level selection |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by trade-offs and code analysis |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Step 6 quality review addresses this |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add prescriptive requirement for fire rating determination methodology (reference to ABC occupancy classification process) | REQ-DW-006 requires ABC compliance but does not prescribe the method or standard for determining fire ratings; Guidance mentions code analysis but Specification lacks a directive statement on how fire ratings shall be assigned | Specification.md | REQ-DW-006 | -- | PROPOSAL: Architect to specify fire rating determination method per ABC | TBD |
| A-002 | A:normative:applying | TBD_Question | Multi | Datasheet | Record TBD: Obtain motor scraper transport height from Owner to resolve overhead door height for D-OHD-01, D-OHD-02, D-OHD-03 | Multiple TBD height values in Datasheet block mandatory practice; the schedule cannot be finalized without this input | Datasheet.md | Door Schedule table -- D-OHD-01 through D-OHD-03 | -- | PROPOSAL: Owner (Camrose County) provides equipment fleet dimensions | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for REQ-DW-006 sub-items (egress widths, accessibility, natural light) as individually checkable criteria rather than a single "Architect code compliance review" | REQ-DW-006 verification is a single broad entry; individual sub-requirements (egress, fire separation, accessibility, natural light) lack discrete verification criteria | Specification.md | Verification table -- REQ-DW-006 | -- | PROPOSAL: Specification should itemize verification for each ABC sub-requirement | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit prerequisite for mechanical/HVAC coordination (PKG-003) regarding overhead door heat loss impact | Procedure Step 5.3 mentions mechanical coordination but it is not listed in the Prerequisites table; this creates a risk that HVAC coordination is missed in scheduling | Procedure.md | Prerequisites table; Step 5.3 | -- | PROPOSAL: Add HVAC coordination to Prerequisites table | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for industrial-grade hardware selection criteria (load ratings, corrosion resistance, cycle life) to support Architect decisions | Guidance Principle 1 states "standard residential or light-commercial hardware groups are not appropriate" but does not provide criteria for what constitutes adequate industrial-grade hardware | Guidance.md | Principles -- 1. Industrial Building Character | -- | PROPOSAL: Guidance should outline hardware selection criteria for industrial use | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Door frame material TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet sources are adequately cited |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Finish column missing from Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Dimension units inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW mapping is present and adequate |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document coverage is comprehensive for available info |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core domain knowledge is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance demonstrates competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for design-phase schedule |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table in Guidance demonstrates discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are appropriately deferred to Architect/Owner |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is adequate |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add door frame material as a column or attribute in the Door Schedule table (currently noted only as "TBD" in Construction section) | Frame material is listed in REQ-DW-005 as a required schedule column but is absent from the Datasheet door schedule table; it appears only as a TBD note in the Construction section | Datasheet.md; Specification.md | Datasheet -- Door Schedule table; Specification -- REQ-DW-005 | -- | PROPOSAL: Datasheet should include frame material column | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Finish column to Door Schedule table per REQ-DW-005 requirements | REQ-DW-005 requires "Finish" as a schedule column but the Datasheet door schedule table does not include a Finish column | Datasheet.md; Specification.md | Datasheet -- Door Schedule table; Specification -- REQ-DW-005 | -- | PROPOSAL: Datasheet should add Finish column | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Guidance | Standardize dimensional notation: Datasheet uses feet-and-inches notation (24', 6') while Specification uses mixed (24', 6 feet (6')); establish consistent unit convention | Minor inconsistency in how dimensions are expressed across Datasheet and Specification could lead to drift in downstream documents | Datasheet.md; Specification.md | Datasheet -- Door Schedule table; Specification -- REQ-DW-004 | -- | PROPOSAL: Guidance should define unit convention for the schedule | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Foundation | 1 | HAS_ITEMS | Accessibility requirements weak |
| C:normative:sufficiency | normative | sufficiency | Mandated Proficiency Threshold | 1 | HAS_ITEMS | No acceptance threshold for door height adequacy |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Mezzanine door coverage gap |
| C:normative:consistency | normative | consistency | Mandated Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are consistent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites are enumerated |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability Threshold | 0 | NO_ITEMS | Procedure steps are sufficient |
| C:operative:completeness | operative | completeness | Exhaustive Operational Scope | 0 | NO_ITEMS | Operational steps cover full lifecycle |
| C:operative:consistency | operative | consistency | Repeatable Operational Discipline | 0 | NO_ITEMS | Steps are repeatable and ordered |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Value basis is established through purpose statements |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Appraisal | 0 | NO_ITEMS | Trade-offs table provides justified appraisals |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Quality Appraisal | 1 | HAS_ITEMS | No quality criteria for schedule drawing format |
| C:evaluative:consistency | evaluative | consistency | Calibrated Value Integrity | 0 | NO_ITEMS | Value judgments are calibrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-DW-006 accessibility language: clarify whether accessibility requirements apply to the Addition (industrial occupancy may have limited accessibility scope under ABC) | REQ-DW-006 says "Accessibility (where applicable to the occupancy classification)" -- the qualifier "where applicable" is ambiguous and could lead to the requirement being overlooked entirely | Specification.md | REQ-DW-006 | -- | PROPOSAL: Architect to determine and state whether accessibility applies to this occupancy | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criterion for overhead door height: define minimum clearance above tallest equipment (motor scraper transport height + safety margin) once Owner provides equipment dimensions | REQ-DW-002 and REQ-DW-003 specify 24' minimum width but the height acceptance threshold is absent; verification says "confirm height accommodates motor scraper class equipment" without a numeric criterion | Specification.md | REQ-DW-002; REQ-DW-003; Verification table | -- | PROPOSAL: Add numeric height criterion once equipment dimensions are confirmed | TBD |
| C-003 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement addressing mezzanine access door (if required by code or design) as identified in Guidance Considerations | Guidance raises the possibility of a mezzanine landing door but there is no corresponding requirement in Specification; if required, it should be enumerated | Specification.md; Guidance.md | Specification -- Requirements (entire section scanned); Guidance -- Considerations -- Mezzanine Access | -- | PROPOSAL: Architect to determine if mezzanine door is required and add to requirements if so | TBD |
| C-004 | C:evaluative:completeness | MissingSlot | Specification | Specification | Add quality or format requirement for the schedule drawing sheet (e.g., legibility, standard format, cross-reference to floor plans) | REQ-DW-005 lists required data columns but does not address drawing sheet quality, format consistency, or cross-referencing convention | Specification.md | REQ-DW-005; Documentation section | -- | PROPOSAL: Specification or Guidance should address schedule presentation standards | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Compliance Evidence | 1 | HAS_ITEMS | No evidence mechanism for ABC compliance |
| F:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Competence | 0 | NO_ITEMS | Standards table addresses this |
| F:normative:completeness | normative | completeness | Exhaustive Governance Record | 1 | HAS_ITEMS | Hardware standard references missing |
| F:normative:consistency | normative | consistency | Calibrated Governing Standard | 0 | NO_ITEMS | Standards references are internally consistent |
| F:operative:necessity | operative | necessity | Operational Readiness Input | 1 | HAS_ITEMS | Site investigation prerequisite weak |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Operational Fitness | 0 | NO_ITEMS | Procedure steps demonstrate operational fitness |
| F:operative:completeness | operative | completeness | Thorough Workflow Proficiency | 0 | NO_ITEMS | Workflow steps are thorough |
| F:operative:consistency | operative | consistency | Standardized Process Alignment | 0 | NO_ITEMS | Process is consistently described |
| F:evaluative:necessity | evaluative | necessity | Fundamental Value Indicator | 0 | NO_ITEMS | Purpose statements provide value indicators |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Assessment Competence | 0 | NO_ITEMS | Assessment approach is warranted |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Scope | 0 | NO_ITEMS | Valuation scope adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Harmony | 1 | HAS_ITEMS | Professional seal terminology inconsistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Procedure | Add procedural step or verification check for documenting the code compliance evidence trail (code analysis report output from Step 1 to be retained as compliance evidence) | REQ-DW-006 verification relies on "Architect's code compliance review" and AHJ inspection, but there is no requirement to produce or retain a compliance evidence document linking each door to its code basis | Specification.md; Procedure.md | Specification -- Verification -- REQ-DW-006; Procedure -- Step 1 | -- | PROPOSAL: Procedure should require retention of code analysis as a record | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add specific hardware and assembly standard references (e.g., CSA A453, ASTM E2074, NFPA 80) once Architect determines applicable standards | Standards table lists "ASTM / CSA standards for door hardware and assemblies" as "specific standards TBD by Architect"; this leaves a gap in the governance record until resolved | Specification.md | Standards table | -- | PROPOSAL: Architect to identify and list specific product standards | TBD |
| F-003 | F:operative:necessity | WeakStatement | Procedure | Procedure | Strengthen site investigation prerequisite from general statement to specific required outputs (existing wall type, existing rough openings, existing door conditions) | Prerequisite "Site investigation of Old North Shop renovation areas" is described as "Required" but does not specify what information the investigation must produce | Procedure.md | Prerequisites table -- Site investigation | -- | PROPOSAL: Procedure should enumerate required site investigation outputs | TBD |
| F-004 | F:evaluative:consistency | Normalization | Multi | Guidance | Harmonize professional seal terminology: Specification REQ-DW-007 says "professional engineer (or architect, as applicable)"; Procedure Step 7.2 says "Architect of Record (or P.Eng. as applicable)"; the order of preference is reversed | The inconsistency in which professional designation is stated first could create confusion about the expected signing authority | Specification.md; Procedure.md | Specification -- REQ-DW-007; Procedure -- Step 7.2 | Specification.md#REQ-DW-007; Procedure.md#Step-7 | PROPOSAL: Guidance should clarify the applicable professional designation for this project | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Governing Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandates are clearly governed |
| D:normative:applying | normative | applying | Obligatory Proficiency Standard | 1 | HAS_ITEMS | No proficiency standard for Architect's code analysis |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance is addressed by verification methods |
| D:normative:reviewing | normative | reviewing | Settled Compliance Benchmark | 0 | NO_ITEMS | Benchmarks are stated (24' width, 6' width, etc.) |
| D:operative:guiding | operative | guiding | Resolved Process Guidance | 0 | NO_ITEMS | Process guidance is resolved in Procedure |
| D:operative:applying | operative | applying | Confirmed Working Delivery | 1 | HAS_ITEMS | No delivery confirmation milestone defined |
| D:operative:judging | operative | judging | Resolved Capability Ruling | 0 | NO_ITEMS | Capability checks in Procedure Step 6 |
| D:operative:reviewing | operative | reviewing | Harmonized Workflow Review | 0 | NO_ITEMS | QA review step exists |
| D:evaluative:guiding | evaluative | guiding | Resolved Purposeful Valuation | 0 | NO_ITEMS | Purpose is clearly articulated |
| D:evaluative:applying | evaluative | applying | Enacted Settled Appraisal | 0 | NO_ITEMS | Trade-offs provide enacted appraisals |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Determination | 1 | HAS_ITEMS | Thermal performance worth not addressed for doors |
| D:evaluative:reviewing | evaluative | reviewing | Calibrated Merit Inspection | 0 | NO_ITEMS | Merit inspection covered by Step 6 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add acceptance criterion for the code compliance analysis itself (e.g., analysis shall address all occupancy classifications, all fire separations, and egress paths in the project scope) | REQ-DW-006 requires code compliance but has no acceptance standard for the analysis process; Procedure Step 1 describes what to do but the Specification does not define when the analysis is "sufficient" | Specification.md; Procedure.md | Specification -- REQ-DW-006; Procedure -- Step 1 | -- | PROPOSAL: Add proficiency standard for code analysis deliverable | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add explicit delivery milestone or gate between draft schedule completion (Step 4 output) and coordination (Step 5) confirming the draft is internally complete before external coordination begins | Steps 4 and 5 flow without a confirmation gate; there is no checkpoint to confirm the draft schedule is internally complete before coordinating with other disciplines | Procedure.md | Steps 4 and 5 | -- | PROPOSAL: Add a draft completeness check between Steps 4 and 5 | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add consideration for thermal performance of overhead doors (U-value, air infiltration at large openings) given Alberta climate and 35' ceiling height | Guidance discusses thermal performance for windows but not for overhead doors, which represent a much larger thermal bridge and air infiltration risk in this building | Guidance.md | Considerations -- Window Requirements (discusses thermal); Principles -- 1. Industrial Building Character | -- | PROPOSAL: Guidance should address overhead door thermal performance trade-offs | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Orienting Imperative | 1 | HAS_ITEMS | Wash station enclosure question unresolved |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Directive Competence | 0 | NO_ITEMS | Directives are substantiated with sources |
| X:guiding:completeness | guiding | completeness | Thorough Authoritative Coverage | 1 | HAS_ITEMS | No coverage of door operator specifications |
| X:guiding:consistency | guiding | consistency | Dependable Directive Alignment | 0 | NO_ITEMS | Directives are aligned across documents |
| X:applying:necessity | applying | necessity | Required Implementation Trigger | 1 | HAS_ITEMS | No trigger criteria for when schedule revision is required |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Implementation Standard | 0 | NO_ITEMS | Implementation standards are demonstrated |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 0 | NO_ITEMS | Implementation records are enumerated |
| X:applying:consistency | applying | consistency | Standardized Consistent Enactment | 0 | NO_ITEMS | Enactment is consistently described |
| X:judging:necessity | judging | necessity | Required Assessment Ruling | 1 | HAS_ITEMS | No ruling mechanism for shop drawing acceptance |
| X:judging:sufficiency | judging | sufficiency | Substantiated Assessment Adequacy | 0 | NO_ITEMS | Assessment methods are substantiated |
| X:judging:completeness | judging | completeness | Exhaustive Determination Record | 0 | NO_ITEMS | Determination records are comprehensive |
| X:judging:consistency | judging | consistency | Calibrated Ruling Alignment | 0 | NO_ITEMS | Ruling criteria are aligned |
| X:reviewing:necessity | reviewing | necessity | Required Audit Standard | 1 | HAS_ITEMS | No audit standard for schedule revision tracking |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Audit Competence | 0 | NO_ITEMS | Audit approach is substantiated |
| X:reviewing:completeness | reviewing | completeness | Thorough Audit Completeness | 0 | NO_ITEMS | Audit scope is thorough |
| X:reviewing:consistency | reviewing | consistency | Dependable Audit Harmony | 0 | NO_ITEMS | Audit methods are harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | TBD_Question | Guidance | Guidance | Record TBD: Confirm with Owner whether the wash station (SOW-0050) will be enclosed; if enclosed, add door to schedule | Guidance notes assumption that wash station is open, but this has not been confirmed; if the Owner intends enclosure, a door is missing from the schedule | Guidance.md | Considerations -- Wash Station Area | -- | PROPOSAL: Owner confirmation required | TBD |
| X-002 | X:guiding:completeness | MissingSlot | Specification | Specification | Add requirement or specification note for overhead door operator type, voltage, and control requirements to support electrical coordination (REQ-DW-008) | REQ-DW-008 requires identification of doors needing power but does not require the schedule to include operator specifications (type, voltage, HP); Procedure Step 5.2 mentions "operator specifications and power requirements" but the Specification does not require these as schedule columns | Specification.md; Procedure.md | Specification -- REQ-DW-008; Procedure -- Step 5.2 | -- | PROPOSAL: Add operator specification fields to REQ-DW-005 column list or REQ-DW-008 | TBD |
| X-003 | X:applying:necessity | WeakStatement | Procedure | Procedure | Add criteria defining when a schedule revision is triggered (e.g., any change to door type, size, rating, or hardware group after IFC issue requires formal revision) | Procedure Step 8.5 states "Any field changes require written Architect approval and a schedule revision" but does not define the threshold for what constitutes a change requiring revision vs. a minor field adjustment | Procedure.md | Step 8.5 | -- | PROPOSAL: Define revision trigger criteria | TBD |
| X-004 | X:judging:necessity | VerificationGap | Procedure | Procedure | Add acceptance criteria for shop drawing review (Step 8.3): define what constitutes acceptable vs. rejected shop drawings for doors and hardware | Procedure Step 8.3 requires shop drawings to be "submitted to the Architect for review before fabrication" but does not state acceptance criteria or turnaround expectations | Procedure.md | Step 8.3 | -- | PROPOSAL: Add shop drawing review acceptance criteria | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add requirement for schedule revision history tracking (drawing revision block management) as a verification record | Procedure Records table lists "Schedule revision history" but there is no verification check confirming revision tracking is maintained | Procedure.md | Records table -- Schedule revision history; Verification table (entire scanned) | -- | PROPOSAL: Add revision tracking verification check | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Governing Substantiated Record | 1 | HAS_ITEMS | Datasheet SOW cross-reference incomplete |
| E:guiding:information | guiding | information | Coherent Governing Indicator | 0 | NO_ITEMS | Governing indicators are coherent |
| E:guiding:knowledge | guiding | knowledge | Commanding Proficient Insight | 0 | NO_ITEMS | Domain insight is proficient |
| E:guiding:wisdom | guiding | wisdom | Principled Governing Foresight | 0 | NO_ITEMS | Foresight demonstrated in trade-offs and conflict table |
| E:applying:data | applying | data | Demonstrated Delivery Measure | 1 | HAS_ITEMS | No delivery acceptance measure for completeness |
| E:applying:information | applying | information | Informed Delivery Indicator | 0 | NO_ITEMS | Delivery indicators present |
| E:applying:knowledge | applying | knowledge | Proficient Actionable Capability | 0 | NO_ITEMS | Actionable capability demonstrated |
| E:applying:wisdom | applying | wisdom | Prudent Insightful Practice | 0 | NO_ITEMS | Practice is prudent |
| E:judging:data | judging | data | Substantiated Conclusive Finding | 0 | NO_ITEMS | Findings are substantiated |
| E:judging:information | judging | information | Decisive Informed Verdict | 0 | NO_ITEMS | Verdicts are informed |
| E:judging:knowledge | judging | knowledge | Thorough Authoritative Adjudication | 0 | NO_ITEMS | Adjudication is thorough |
| E:judging:wisdom | judging | wisdom | Principled Conclusive Judgment | 0 | NO_ITEMS | Judgment is principled |
| E:reviewing:data | reviewing | data | Verified Exhaustive Finding | 1 | HAS_ITEMS | Conflict table inconsistency |
| E:reviewing:information | reviewing | information | Informed Oversight Narrative | 0 | NO_ITEMS | Oversight narrative is informed |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Oversight Mastery | 0 | NO_ITEMS | Oversight mastery is proficient |
| E:reviewing:wisdom | reviewing | wisdom | Principled Holistic Oversight | 0 | NO_ITEMS | Holistic oversight demonstrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Add SOW-0008 and SOW-0009 to Datasheet SOW Coverage field (currently lists only SOW-0011 and SOW-0026; Specification REQ-DW-006 references SOW-0008 and SOW-0009) | Datasheet Identification table lists SOW Coverage as "SOW-0011, SOW-0026" but the Specification references SOW-0008 and SOW-0009 as sources for code compliance; these SOW items are within scope but not reflected in the Datasheet | Datasheet.md; Specification.md | Datasheet -- Identification -- SOW Coverage; Specification -- REQ-DW-006 | -- | PROPOSAL: Datasheet SOW Coverage should include all applicable SOW items | TBD |
| E-002 | E:applying:data | WeakStatement | Specification | Specification | Clarify REQ-DW-005 completeness verification: define what "all required columns populated" means (all cells have non-TBD values, or all cells have a value including TBD with justification) | Verification for REQ-DW-005 says "confirm all required columns populated" but does not define whether TBD entries count as populated or whether all TBDs must be resolved before the schedule is considered complete | Specification.md | Verification table -- REQ-DW-005 | -- | PROPOSAL: Specification should define acceptance threshold for TBD resolution | TBD |
| E-003 | E:reviewing:data | Conflict | Guidance | Guidance | Resolve Guidance Conflict Table reference inconsistency: CONF-DW-001 Impacted Sections references "Procedure Step 4" but the corresponding procedure step is Step 2 (Confirm Program with Owner) and Step 3/4 (tag list and populate schedule) | Guidance Conflict Table CONF-DW-001 cites "Procedure Step 4" as impacted, but the relevant prerequisite and confirmation step is Procedure Step 2; Step 4 is where the entrance/exit doors would be populated, not where the conflict is resolved | Guidance.md; Procedure.md | Guidance -- Conflict Table -- CONF-DW-001; Procedure -- Step 2; Procedure -- Step 4 | Guidance.md#Conflict-Table-CONF-DW-001 (Step 4); Procedure.md#Step-2 (confirmation step) | PROPOSAL: Guidance Conflict Table should reference both Step 2 and Step 4 | TBD |

---

*End of Semantic Lensing Register*
