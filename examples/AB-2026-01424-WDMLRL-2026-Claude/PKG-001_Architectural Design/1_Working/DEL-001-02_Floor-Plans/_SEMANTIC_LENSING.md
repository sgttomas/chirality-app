# Semantic Lensing Register: DEL-001-02 Architectural Floor Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-02_Floor-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-02_Floor-Plans/_CONTEXT.md (present; deliverable identity and description)
- _STATUS.md — DEL-001-02_Floor-Plans/_STATUS.md (present; current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-02_Floor-Plans/_SEMANTIC.md (present; matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-001-02_Floor-Plans/Datasheet.md (present)
- Specification.md — DEL-001-02_Floor-Plans/Specification.md (present)
- Guidance.md — DEL-001-02_Floor-Plans/Guidance.md (present)
- Procedure.md — DEL-001-02_Floor-Plans/Procedure.md (present)
- _REFERENCES.md — DEL-001-02_Floor-Plans/_REFERENCES.md (present; R-01, R-04 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | ABC edition not confirmed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | IFC stamp ambiguity |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Occupancy classification TBD |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit path adequately covered in Procedure Step 7 and Specification Verification table |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing prerequisite gate logic |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Steps 1-9 provide adequate practical execution sequence |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered by Procedure Verification table |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | Coordination review record not formalized |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose and Principles adequately establish value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T-1 through T-3 address merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table addresses worth determination for each requirement |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Verification table covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicable edition of Alberta Building Code with AHJ before finalizing floor plan layout | The ABC is referenced as the governing code throughout all four documents but the specific edition is never confirmed. This is a prescriptive-direction gap that blocks compliance determination. | Specification.md; Guidance.md | Specification.md#Standards; Guidance.md#P-5 | -- | PROPOSAL: Architect to confirm with AHJ | TBD |
| A-002 | A:normative:applying | Conflict | Specification | Specification | Clarify whether P.Eng. stamp requirement (RFP ss3.3.2) applies to architectural drawings or only engineering discipline drawings; confirm whether architectural stamp is also required | RFP mandates P.Eng. stamp on all IFC drawings but standard practice has architects stamping architectural drawings. This creates ambiguity in mandatory practice for floor plan issuance. Already identified as CONF-003 in Guidance. | Specification.md; Guidance.md | Specification.md#REQ-022; Guidance.md#Conflict Table CONF-003 | Specification.md#REQ-022 (P.Eng. stamp required per RFP); Guidance.md#CONF-003 (standard practice: Architect stamps architectural drawings) | PROPOSAL: Owner and AHJ to clarify | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Confirm building occupancy classification under Alberta Building Code (likely Group F industrial with possible mixed-use sub-classifications) | Compliance determination for code requirements (egress, fire separations, accessible design) depends on occupancy classification, which is stated only as an assumption in Procedure Step 1.2. No authoritative classification exists in any document. | Procedure.md; Specification.md | Procedure.md#Step 1.2; Specification.md#REQ-021 | -- | PROPOSAL: Architect to determine per ABC | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit prerequisite gate: confirm County approval of DEL-001-01 before commencing IFC production (Step 8) | Procedure lists DEL-001-01 County approval as a prerequisite but does not include an explicit hold-point or gate check at the transition from design to IFC production. Procedural direction for this critical dependency is implicit rather than explicit. | Procedure.md | Procedure.md#Prerequisites; Procedure.md#Step 8 | -- | PROPOSAL: Procedure.md | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a formal coordination review record template or checklist reference in Records section | Procedure Step 6.2 requires resolving coordination comments and documenting deviations, but the Records section lists only "Coordination review log" without specifying format or minimum content. Process audit readiness requires a defined record structure. | Procedure.md | Procedure.md#Step 6; Procedure.md#Records | -- | PROPOSAL: Procedure.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Utility room and office dimensions TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes tables provide adequate evidence with sources |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Work bench dimensions absent |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Normalization issue on structure type |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Cross-reference signals between documents are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set provides a comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across the four documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Documents demonstrate fundamental understanding of the maintenance shop program |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise level demonstrated is adequate for floor plan production |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery of the deliverable scope is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance Trade-offs demonstrate essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis shows adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance demonstrates holistic insight into cross-discipline coordination |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning across documents is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify whether utility room and office dimensions will be determined by Architect alone or require Owner input; record anticipated size ranges if available | Utility room and office are listed as "TBD (exact dimensions)" in Datasheet and "TBD by Architect" in Specification. These are essential facts for the floor plan but have no target range, making layout planning ambiguous. | Datasheet.md; Specification.md | Datasheet.md#Spatial Program; Specification.md#REQ-008, #REQ-009 | -- | PROPOSAL: Architect to size per program | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add work bench area dimensions or location criteria to Spatial Program table | Work bench areas are listed in Datasheet as "Shown on conceptual drawing" and in Guidance Examples section, but no dimensions or minimum requirements are recorded. This is a comprehensive-record gap for a programmatic element shown on R-04. | Datasheet.md | Datasheet.md#Spatial Program | -- | PROPOSAL: Datasheet.md | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Guidance | Normalize "concrete structure" (Datasheet) vs. implicit steel-frame-with-concrete-floor usage throughout Specification and Guidance; confirm structural system type | Datasheet states "Structure type: Concrete structure" (from RFP ss3.4, R-04) but Specification and Guidance discuss steel plates embedded in concrete floor, overhead crane runways (typically steel), and mezzanine steel framing. The term "concrete structure" may refer to the floor/foundation only, not the overall structural system. Terminology drift may cause confusion. | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Attributes (Structure type); Specification.md#REQ-015; Guidance.md#C-4 | -- | PROPOSAL: Guidance.md vocabulary note | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Compliance Imperative | 1 | HAS_ITEMS | Fire separation requirements not explicit |
| C:normative:sufficiency | normative | sufficiency | Justified Governance Threshold | 0 | NO_ITEMS | Governance thresholds are justified with source references |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Accessible design coverage incomplete |
| C:normative:consistency | normative | consistency | Harmonized Governance Discipline | 0 | NO_ITEMS | Governance references are harmonized across documents |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Operational readiness prerequisites adequately listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Practical Competence | 0 | NO_ITEMS | Procedure demonstrates practical competence for floor plan production |
| C:operative:completeness | operative | completeness | Integrated Execution Mastery | 0 | NO_ITEMS | Execution steps are comprehensive |
| C:operative:consistency | operative | consistency | Synchronized Operational Coherence | 1 | HAS_ITEMS | Coordination sequence gap |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Discernment | 0 | NO_ITEMS | Value drivers established in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Appraisal | 0 | NO_ITEMS | Trade-offs substantiated with source references |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Integrity | 0 | NO_ITEMS | Valuation scope is comprehensive |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Consistency | 0 | NO_ITEMS | Valuation principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement for fire separation identification on floor plan where mixed occupancies exist (shop vs. office vs. storage) | As an authoritative compliance imperative, fire separations between occupancy groups are mentioned in Procedure Step 1.3 and Step 7.1 but are absent from Specification requirements. If the building has mixed occupancies, fire-rated separations must be shown on the floor plan. No REQ addresses this. | Specification.md; Procedure.md | Specification.md#Requirements (entire section scanned); Procedure.md#Step 1.3, #Step 7.1 | -- | PROPOSAL: Specification.md | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for accessible design compliance (currently mentioned in REQ-021 as "where required" but no verification method specified) | Exhaustive regulatory coverage requires that accessible design, if triggered by ABC, has a verification path. REQ-021 mentions accessible design parenthetically but the Verification table entry for REQ-021 only says "Architect performs code compliance review" without specifically addressing accessibility verification. | Specification.md | Specification.md#REQ-021; Specification.md#Verification (REQ-021 row) | -- | PROPOSAL: Specification.md | TBD |
| C-003 | C:operative:consistency | RationaleGap | Guidance | Guidance | Add guidance on sequencing of discipline coordination requests (which discipline inputs are needed first for floor plan layout vs. which can follow) | Synchronized operational coherence requires that the coordination sequence is clear. Procedure Step 2 addresses structural, Step 3 addresses layout, and Step 6 addresses interdisciplinary review, but Guidance does not explain the rationale for the coordination order or identify which discipline inputs are critical-path for the floor plan (e.g., structural column grid before mechanical equipment zones). | Guidance.md; Procedure.md | Guidance.md#P-4; Procedure.md#Steps 2, 3, 6 | -- | PROPOSAL: Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Conformance Basis | 0 | NO_ITEMS | Conformance basis is established through code references |
| F:normative:sufficiency | normative | sufficiency | Qualified Conformance Rigor | 1 | HAS_ITEMS | Standards table lacks edition specificity |
| F:normative:completeness | normative | completeness | Total Governance Command | 0 | NO_ITEMS | Governance scope adequately comprehensive |
| F:normative:consistency | normative | consistency | Unified Conformance Logic | 0 | NO_ITEMS | Conformance logic is unified across documents |
| F:operative:necessity | operative | necessity | Critical Capability Baseline | 1 | HAS_ITEMS | Emergency shower not in floor plan requirements |
| F:operative:sufficiency | operative | sufficiency | Qualified Execution Preparedness | 0 | NO_ITEMS | Execution prerequisites are adequately qualified |
| F:operative:completeness | operative | completeness | Total Performance Proficiency | 0 | NO_ITEMS | Performance coverage is complete |
| F:operative:consistency | operative | consistency | Dependable Coordination Discipline | 0 | NO_ITEMS | Coordination discipline is dependable |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 1 | HAS_ITEMS | Energy efficiency / insulation not addressed |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Appraisal Adequacy | 0 | NO_ITEMS | Appraisal adequacy is grounded |
| F:evaluative:completeness | evaluative | completeness | Integral Appraisal Command | 0 | NO_ITEMS | Appraisal command is integral |
| F:evaluative:consistency | evaluative | consistency | Disciplined Quality Coherence | 0 | NO_ITEMS | Quality coherence is disciplined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen Standards table entries: replace "ASSUMPTION: likely applicable" with confirmed edition references once AHJ consultation is complete | Qualified conformance rigor requires that standards be identified with sufficient specificity to determine compliance. The Standards table uses "ASSUMPTION: likely applicable" for both ABC and NBC entries, which is insufficient for conformance determination. | Specification.md | Specification.md#Standards | -- | PROPOSAL: Architect to confirm editions | TBD |
| F-002 | F:operative:necessity | MissingSlot | Specification | Specification | Add requirement for emergency shower/eyewash station location on floor plan if required by occupancy and operations (referenced in Procedure Step 6.1 under Plumbing coordination) | Critical capability baseline: Procedure Step 6.1 mentions "emergency shower location (DEL-006)" as a plumbing coordination item, but no corresponding requirement exists in Specification for showing an emergency shower location on the floor plan. If the facility operations require it, this is a missing floor plan element. | Specification.md; Procedure.md | Specification.md#Requirements (entire section scanned); Procedure.md#Step 6.1 | -- | PROPOSAL: Specification.md (pending confirmation of need) | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add consideration for building envelope thermal performance and its impact on floor plan wall thickness and spatial clearances | Intrinsic merit foundation: the floor plan must accommodate wall assembly thicknesses driven by insulation requirements (Alberta climate), which affects interior dimensions. No document addresses how thermal performance requirements may influence floor plan spatial clearances or wall thicknesses. This is a value-driver gap for a building in central Alberta. | Guidance.md; Datasheet.md | Guidance.md#Considerations (entire section scanned); Datasheet.md#Attributes | -- | PROPOSAL: Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority well established through RFP and code references |
| D:normative:applying | normative | applying | Resolved Compliance Enactment | 0 | NO_ITEMS | Compliance enactment resolved through requirements and verification |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 0 | NO_ITEMS | Conformance verdict pathway established via AHJ permit approval |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Verification | 0 | NO_ITEMS | Oversight verification resolved through Specification Verification table |
| D:operative:guiding | operative | guiding | Established Method Guidance | 1 | HAS_ITEMS | Drawing scale/format guidance missing |
| D:operative:applying | operative | applying | Confirmed Task Deployment | 0 | NO_ITEMS | Task deployment confirmed through Procedure Steps 1-9 |
| D:operative:judging | operative | judging | Resolved Effectiveness Verdict | 0 | NO_ITEMS | Effectiveness verdict resolved through Procedure Verification |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Integrity | 0 | NO_ITEMS | Workflow integrity confirmed through sequential procedure steps |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Stewardship | 1 | HAS_ITEMS | Lifecycle/maintenance consideration gap |
| D:evaluative:applying | evaluative | applying | Confirmed Value Enactment | 0 | NO_ITEMS | Value enactment confirmed through trade-off analysis |
| D:evaluative:judging | evaluative | judging | Definitive Merit Determination | 0 | NO_ITEMS | Merit determination established through verification matrix |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Assurance | 0 | NO_ITEMS | Merit assurance resolved through quality checks in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Datasheet | Datasheet | Clarify drawing format expectations: sheet size, scale conventions, and CAD/BIM standards for the floor plan drawing set | Established method guidance requires that the drawing production method be defined. Datasheet Construction section states "Drawing set (multi-sheet, format TBD by Architect)" but provides no guidance on sheet size, scale conventions, or CAD/BIM requirements. For a design-build project these parameters affect coordination with other disciplines. | Datasheet.md | Datasheet.md#Construction | -- | PROPOSAL: Datasheet.md | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add consideration for how floor plan layout decisions affect long-term maintenance access and future equipment changeout (lifecycle value perspective) | Principled worth stewardship: the floor plan locks in spatial relationships that affect the building's long-term operational value. Guidance addresses immediate coordination and code compliance but does not discuss how layout decisions (e.g., bay access clearances, service pit positioning, mezzanine access) affect future maintenance operations or equipment replacement over the building lifecycle. | Guidance.md | Guidance.md#Considerations (entire section scanned) | -- | PROPOSAL: Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Direction | 0 | NO_ITEMS | Governance direction foundations are established |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Methodical Stewardship | 0 | NO_ITEMS | Methodical stewardship is substantiated |
| X:guiding:completeness | guiding | completeness | Exhaustive Methodical Command | 0 | NO_ITEMS | Methodical command is exhaustive |
| X:guiding:consistency | guiding | consistency | Unified Directive Stability | 0 | NO_ITEMS | Directive stability is unified |
| X:applying:necessity | applying | necessity | Mandatory Activation Foundation | 1 | HAS_ITEMS | Verification of door count/type gap |
| X:applying:sufficiency | applying | sufficiency | Substantiated Implementation Adequacy | 0 | NO_ITEMS | Implementation adequacy is substantiated |
| X:applying:completeness | applying | completeness | Comprehensive Enactment Coverage | 1 | HAS_ITEMS | Mezzanine load verification gap |
| X:applying:consistency | applying | consistency | Dependable Enactment Coherence | 0 | NO_ITEMS | Enactment coherence is dependable |
| X:judging:necessity | judging | necessity | Critical Assessment Finding | 1 | HAS_ITEMS | No pass/fail criteria for area tolerance |
| X:judging:sufficiency | judging | sufficiency | Substantiated Verdict Adequacy | 0 | NO_ITEMS | Verdict adequacy is substantiated |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Coverage | 1 | HAS_ITEMS | Cross-ref verification for crane coordination |
| X:judging:consistency | judging | consistency | Unified Assessment Stability | 0 | NO_ITEMS | Assessment stability is unified |
| X:reviewing:necessity | reviewing | necessity | Critical Examination Foundation | 0 | NO_ITEMS | Examination foundation is established |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Audit Competence | 0 | NO_ITEMS | Audit competence is substantiated |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Completeness | 0 | NO_ITEMS | Audit completeness is adequate |
| X:reviewing:consistency | reviewing | consistency | Unified Examination Reliability | 0 | NO_ITEMS | Examination reliability is unified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification approach for REQ-019 (entrance/exit doors) specifying minimum number, type (person door vs. overhead), and code-required egress door count | Mandatory activation foundation: REQ-019 requires "separate entrance and exit door locations" and the Verification table says "Confirm separate entrance and exit doors shown." However, neither specifies how many doors, what types, or how code-minimum egress doors factor in. The verification is underspecified for a code-sensitive element. | Specification.md | Specification.md#REQ-019; Specification.md#Verification (REQ-019 row) | -- | PROPOSAL: Specification.md | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification approach for mezzanine loading capacity shown on floor plan (currently REQ-013 verification does not address how load-bearing capacity is confirmed on the architectural drawing) | Comprehensive enactment coverage: REQ-013 requires the mezzanine to be "load-bearing for heavy items (oil totes, pumping equipment)" but the Verification table only confirms "mezzanine extent shown" and cross-reference to structural drawings. There is no verification that the architectural floor plan carries a loading note or capacity reference. Procedure Step 4.1 mentions a "loading note" but this is not verified. | Specification.md; Procedure.md | Specification.md#REQ-013; Specification.md#Verification (REQ-013 row); Procedure.md#Step 4.1 | -- | PROPOSAL: Specification.md | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Define acceptable tolerance for "approximately 13,000 sq ft" in REQ-001 (e.g., +/- 5% or +/- 500 sq ft) to enable pass/fail determination | Critical assessment finding: REQ-001 uses "approximately 13,000 sq ft" and the Verification table says "confirms against RFP threshold." Without a defined tolerance, the verification has no pass/fail boundary. This impedes definitive assessment. | Specification.md | Specification.md#REQ-001; Specification.md#Verification (REQ-001 row) | -- | PROPOSAL: Specification.md (tolerance to be confirmed with Owner) | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add explicit cross-reference verification step confirming crane runway positions on floor plan match structural crane support details (DEL-002-07) | Exhaustive assessment coverage: REQ-017 verification says "Confirm crane runway footprint shown; cross-reference structural crane support details (DEL-002-07)" but does not specify what constitutes a passing cross-reference (e.g., matching centerline positions, matching span, matching rail gauge). The crane runway is a high-risk multi-discipline interface. | Specification.md | Specification.md#REQ-017; Specification.md#Verification (REQ-017 row) | -- | PROPOSAL: Specification.md | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative and well-sourced |
| E:guiding:information | guiding | information | Authoritative Steering Narrative | 0 | NO_ITEMS | Steering narrative is clear and authoritative |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Leadership Proficiency | 0 | NO_ITEMS | Leadership proficiency demonstrated through Guidance Principles |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Judgment | 0 | NO_ITEMS | Strategic judgment demonstrated in Trade-offs |
| E:applying:data | applying | data | Substantiated Execution Record | 0 | NO_ITEMS | Execution records well-defined in Procedure |
| E:applying:information | applying | information | Integrated Deployment Narrative | 1 | HAS_ITEMS | Ceiling fan coordination gap |
| E:applying:knowledge | applying | knowledge | Skilled Execution Command | 0 | NO_ITEMS | Execution command demonstrated in Procedure steps |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Execution judgment demonstrated through prerequisite structure |
| E:judging:data | judging | data | Verified Finding Archive | 0 | NO_ITEMS | Finding archive established through verification matrix |
| E:judging:information | judging | information | Coherent Finding Narrative | 0 | NO_ITEMS | Finding narrative is coherent |
| E:judging:knowledge | judging | knowledge | Comprehensive Verdict Proficiency | 0 | NO_ITEMS | Verdict proficiency demonstrated in Specification Verification |
| E:judging:wisdom | judging | wisdom | Principled Verdict Wisdom | 0 | NO_ITEMS | Verdict wisdom reflected in conflict identification |
| E:reviewing:data | reviewing | data | Substantiated Inspection Archive | 0 | NO_ITEMS | Inspection archive substantiated through Records table |
| E:reviewing:information | reviewing | information | Integrated Inspection Narrative | 1 | HAS_ITEMS | Normalization on terminology |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Inspection Proficiency | 0 | NO_ITEMS | Inspection proficiency is comprehensive |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Wisdom | 0 | NO_ITEMS | Inspection wisdom reflected in QA structure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:information | MissingSlot | Specification | Specification | Add requirement or coordination note for ceiling fan locations (6 fans per Decomp SOW-0040) to be shown or referenced on floor plan | Integrated deployment narrative: Procedure Step 6.1 mentions "ceiling fan locations (6 fans in main shop area per Decomp SOW-0040)" as a mechanical coordination item, but no corresponding requirement exists in Specification, and Datasheet does not list ceiling fans as a floor plan coordination element. This is a deployment signal present in Procedure but missing from the normative chain. | Specification.md; Procedure.md; Datasheet.md | Specification.md#Requirements (entire section scanned); Procedure.md#Step 6.1; Datasheet.md#Attributes (entire section scanned) | -- | PROPOSAL: Specification.md or Datasheet.md | TBD |
| E-002 | E:reviewing:information | Normalization | Multi | Guidance | Normalize terminology for the below-grade element: "service pit" vs. "Service Pit" vs. "service pit/trench" used interchangeably across documents | Integrated inspection narrative: an inspection or review would need a single consistent term for the below-grade service element. Specification uses "service pit/trench" (REQ-012), Datasheet uses "Service Pit / pit", Guidance uses "service pit/trench", and Procedure uses both forms. Establishing one primary term with the alternative as a parenthetical would improve cross-document traceability. | Specification.md; Datasheet.md; Guidance.md; Procedure.md | Specification.md#REQ-012; Datasheet.md#Spatial Program; Guidance.md#C-3; Procedure.md#Step 3.5 | -- | PROPOSAL: Guidance.md vocabulary note | TBD |
