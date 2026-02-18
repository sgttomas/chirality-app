# Semantic Lensing Register: DEL-04-02 Cold Storage -- Doors, Openings & Hardware

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-004_Cold Storage Building (Unheated, 60'x100')/1_Working/DEL-04-02_Cold Storage - Doors, Openings & Hardware/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-04-02, PKG-004, SOW-0302, OBJ-004
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- All 7 matrices (A, B, C, F, D, X, E) parsed successfully
- Datasheet.md -- Read; Identification, Attributes, Conditions, Construction, References
- Specification.md -- Read; Scope, Requirements (REQ-4202-01 through REQ-4202-14), Standards, Verification, Documentation
- Guidance.md -- Read; Purpose, Principles (P1-P5), Considerations (C1-C5), Trade-offs (T1-T3), Conflict Table
- Procedure.md -- Read; Purpose, Prerequisites, Steps (Part A: Proposal, Part B: Implementation), Verification, Records
- _REFERENCES.md -- Read; OSR Appendix A listed; minimal content

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | ABC edition unresolved |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Person door size TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC edition unknown |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | AHJ review process adequately addressed |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps A1-A10, B1-B10 provide adequate direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Concrete apron dimensions absent |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in both Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table adequately covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose and Principles cover value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | Cost-benefit basis absent for hardware grade |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T1-T3 adequately address worth |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning tests cover quality assessment |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicable edition of Alberta Building Code (ABC) for person door egress, emergency lighting, and hardware requirements | The Standards table lists ABC as "current edition" with accessibility "Not directly accessed -- location TBD". Without confirming the specific edition, prescriptive direction for code compliance cannot be verified. | Specification.md | Standards table | -- | AHJ or Owner to confirm ABC edition | TBD |
| A-002 | A:normative:applying | WeakStatement | Datasheet | Datasheet | Clarify person door nominal size; Datasheet records "TBD (code-minimum; DB to confirm)" but no indicative dimension is provided | Mandatory practice requires a concrete dimension or at minimum a code-referenced minimum. The Procedure (Step A3) suggests "typically 32" wide x 80" high minimum" but neither Datasheet nor Specification commit to a dimension. | Datasheet.md | Person (Man) Doors table | -- | Design-Builder to confirm per ABC | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for person door minimum size against building code | REQ-4202-09 requires person doors to "meet applicable building code requirements for egress, size, and hardware" but the verification table for REQ-4202-09 only references "AHJ permit review and inspection" without specifying what code criteria will be checked pre-submission. | Specification.md | Verification table, REQ-4202-09 | -- | Specification | TBD |
| A-004 | A:operative:applying | WeakStatement | Datasheet | Datasheet | Add indicative concrete apron dimensions (minimum width, depth, thickness) or explicit TBD with design-basis parameters | Datasheet records apron dimensions as "TBD (DB to design; minimum sufficient for safe vehicle approach)" which is too vague for practical execution. Procedure Step A5 also defers this. | Datasheet.md | Concrete Aprons table | -- | Design-Builder (structural/civil) | TBD |
| A-005 | A:evaluative:applying | RationaleGap | Guidance | Guidance | Add rationale for why standard grade hardware is cost-appropriate for the 20-year design life, referencing expected use intensity and maintenance cycle | P3 states standard grade is appropriate but does not quantify the cost-benefit or expected replacement interval relative to the 20-year design life. C4 raises the 20-year concern but does not resolve it with a lifecycle cost perspective. | Guidance.md | Principles P3, Considerations C4 | -- | Guidance | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Overhead door material TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | OSR citations adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Hardware finish unspecified |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensions consistently reported |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Opening axis undetermined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope boundaries clearly defined |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles P1-P5 cover fundamentals |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | DB expertise delegation appropriate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Cross-deliverable refs adequate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T1-T3 provide discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment delegation to DB is appropriate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-package coordination noted |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Resolve TBD for overhead door material; Datasheet Construction table records "TBD (DB to select; material suitable for direction doors face)" without even a default assumption | This is an essential fact for the door schedule. The Guidance T2 suggests poly is generally preferred for cold storage but the Datasheet does not even record this as an assumed default. | Datasheet.md | Construction table, Overhead door material | -- | Design-Builder | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add hardware finish specification or explicit TBD with environmental parameters (freeze-thaw, unheated, exterior-grade) to the Construction table | Datasheet Construction table records "TBD (standard grade; finish to suit unheated environment)" but does not record the environmental parameters the finish must withstand. Guidance C4 and Procedure Step A4 both reference galvanized/zinc-plated as an assumption but this is not in the Datasheet. | Datasheet.md | Construction table, Hardware finish | -- | Design-Builder | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Guidance | Record TBD: Which two opposite sides (long 100' walls vs. short 60' ends) will receive the door openings? Document decision criteria and confirm with site layout | This is an essential signal for the entire deliverable. Guidance C1 identifies this as a DB decision but no resolution pathway or deadline is stated. The opening axis affects equipment routing, wind exposure, and apron design. | Guidance.md, Datasheet.md | Guidance C1, Datasheet Attributes | -- | Design-Builder with Owner input per DEL-04-01 and PKG-003 | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "man doors" vs. "person doors" -- documents use both terms inconsistently | Datasheet uses "Person (Man) Doors" as header. Specification uses "person (man) doors" and "person doors". Guidance uses "person doors". Procedure uses "Man Doors Specification" in Records and "person doors" elsewhere. _CONTEXT.md uses "Man doors specification". This inconsistency could cause confusion in schedules and specifications. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Multiple sections | -- | Guidance (vocabulary note) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Threshold | 1 | HAS_ITEMS | Code edition unresolved (related to A-001) |
| C:normative:sufficiency | normative | sufficiency | Compliance Justification | 0 | NO_ITEMS | OSR source citations provide justification |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Fire separation not addressed |
| C:normative:consistency | normative | consistency | Uniform Regulatory Standard | 0 | NO_ITEMS | Standards referenced consistently |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites adequately listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Competence | 0 | NO_ITEMS | DB competence delegation appropriate |
| C:operative:completeness | operative | completeness | Comprehensive Execution Scope | 1 | HAS_ITEMS | Weatherstripping scope gap |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process steps are consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Basis | 0 | NO_ITEMS | Value basis stated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Assessment | 0 | NO_ITEMS | Trade-offs provide merit justification |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Coverage | 0 | NO_ITEMS | Coverage adequate for proposal phase |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Values consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement or explicit exclusion note for fire separation rating at door openings between cold storage and any adjacent structure | Under the "Regulatory Threshold" lens, the Specification addresses egress (REQ-4202-09) and emergency lighting (REQ-4202-11) but does not address fire separation rating for the door openings, if any is required for an unheated standalone ancillary building. If no fire separation is required (standalone building), this should be explicitly stated. | Specification.md | Requirements section | -- | AHJ / ABC | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing whether overhead doors require wind-load rating given Alberta climate conditions | Datasheet Conditions table notes "snow, lateral, and wind loads per Alberta building code" for the building, but no requirement addresses wind-load rating for the overhead doors specifically. REQ-4202-02 specifies size only. Given 16'x16' openings in Alberta, wind-load performance is a regulatory threshold consideration. | Specification.md, Datasheet.md | Specification Requirements, Datasheet Conditions | -- | ABC / door manufacturer | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement or note for weatherstripping/sealing at overhead door and person door openings | Procedure Step A4 mentions "weatherstripping" for person door hardware sets, and Guidance C5 discusses weatherproof requirements, but no formal requirement in the Specification addresses weatherstripping or sealing at door openings. For an unheated building in Alberta, even minimal sealing affects snow infiltration and operational usability. | Specification.md, Procedure.md | Specification Requirements (entire section scanned), Procedure Step A4 | -- | Design-Builder | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Code Mandate | 1 | HAS_ITEMS | Standards not accessed |
| F:normative:sufficiency | normative | sufficiency | Proven Conformance Adequacy | 1 | HAS_ITEMS | Verification gap for window profile |
| F:normative:completeness | normative | completeness | Absolute Regulatory Coverage | 0 | NO_ITEMS | Covered by C-001 and C-002 above |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Regulatory references consistent |
| F:operative:necessity | operative | necessity | Functional Precondition | 1 | HAS_ITEMS | Vehicle clearance verification |
| F:operative:sufficiency | operative | sufficiency | Operational Readiness | 0 | NO_ITEMS | Procedure prerequisites adequate |
| F:operative:completeness | operative | completeness | Total Operational Command | 0 | NO_ITEMS | Operational steps comprehensive |
| F:operative:consistency | operative | consistency | Systematic Operational Reliability | 0 | NO_ITEMS | Consistent across docs |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit Imperative | 0 | NO_ITEMS | Merit basis present in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Valuation | 1 | HAS_ITEMS | Lifecycle cost gap |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Adequate for proposal |
| F:evaluative:consistency | evaluative | consistency | Harmonized Value Integrity | 0 | NO_ITEMS | Values harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen Standards table: record that ABC, Town bylaws, and IES Recommendations have "Not directly accessed" status and add action item to obtain and confirm applicable sections before detailed design | Three standards are listed as "Not directly accessed -- location TBD" in the Standards table. Under an authoritative code mandate lens, relying on unverified standards weakens the normative basis of the requirements. | Specification.md | Standards table | -- | Design-Builder / Owner | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification method for REQ-4202-03 (window profile match) that includes a specific comparison artifact (photo, drawing overlay, or spec cross-reference) rather than only "visual review" | The verification approach for REQ-4202-03 states "Cross-check with PKG-002 overhead door specification; visual review" but does not specify what constitutes a passing comparison. A more rigorous method (e.g., documented spec cross-reference or manufacturer model confirmation) would demonstrate conformance adequacy. | Specification.md | Verification table, REQ-4202-03 | -- | Design-Builder | TBD |
| F-003 | F:operative:necessity | VerificationGap | Specification | Procedure | Add verification step for vehicle clearance (REQ-4202-13) that includes documenting the actual equipment inventory and their heights against the 16' door opening | REQ-4202-13 verification states "Equipment clearance check against 16' door height; confirm in design narrative" but neither Specification nor Procedure defines what equipment list to check against or how to document the clearance confirmation. This is a functional precondition that needs a concrete verification artifact. | Specification.md, Procedure.md | Specification Verification REQ-4202-13, Procedure entire document scanned | -- | Design-Builder | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add lifecycle cost or maintenance interval estimate for standard grade hardware in an unheated Alberta environment to substantiate the valuation that standard grade is adequate for the 20-year design life | Guidance P3 and C4 both discuss standard grade hardware appropriateness but neither provides a substantiated valuation. The 20-year design life is stated but no estimate of hardware replacement frequency or lifecycle cost comparison is provided. | Guidance.md | Principles P3, Considerations C4 | -- | Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Codified Directive Authority | 0 | NO_ITEMS | Directive authority adequately established via OSR citations |
| D:normative:applying | normative | applying | Enforced Compliance Practice | 0 | NO_ITEMS | Compliance practice enforced through requirements |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | AHJ confirmation path incomplete |
| D:normative:reviewing | normative | reviewing | Mandated Oversight Integrity | 0 | NO_ITEMS | Oversight addressed via AHJ and commissioning |
| D:operative:guiding | operative | guiding | Established Method Guidance | 0 | NO_ITEMS | Procedure provides established method |
| D:operative:applying | operative | applying | Validated Implementation | 0 | NO_ITEMS | Implementation steps adequate |
| D:operative:judging | operative | judging | Definitive Performance Verdict | 0 | NO_ITEMS | Verification tables provide verdict basis |
| D:operative:reviewing | operative | reviewing | Operational Integrity Review | 0 | NO_ITEMS | Commissioning and records cover this |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Direction | 0 | NO_ITEMS | Guidance Purpose provides value direction |
| D:evaluative:applying | evaluative | applying | Substantiated Merit Delivery | 1 | HAS_ITEMS | Campus aesthetic contribution unquantified |
| D:evaluative:judging | evaluative | judging | Comprehensive Merit Judgment | 0 | NO_ITEMS | Trade-offs provide merit judgment |
| D:evaluative:reviewing | evaluative | reviewing | Harmonized Quality Oversight | 0 | NO_ITEMS | Quality oversight through commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Procedure | Procedure | Add a prerequisite or step for AHJ pre-consultation specifically for cold storage building door/egress requirements before detailed design submission | Procedure Prerequisites for Implementation Phase lists "AHJ pre-consultation completed" but does not specify what code topics to consult on for this deliverable. Under the "Definitive Conformance Ruling" lens, the AHJ consultation should confirm egress requirements, emergency lighting, and any exemptions for unheated ancillary buildings. | Procedure.md | Prerequisites for Detailed Design Phase | -- | AHJ | TBD |
| D-002 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add explicit statement connecting the window profile match requirement to OBJ-004 (campus aesthetic coherence) and quantifying or describing the expected visual benefit | Guidance P2 mentions "turnkey campus appearance" as the value driver for window profile consistency but does not explicitly connect this to OBJ-004 or describe how merit delivery will be assessed. Under "Substantiated Merit Delivery," the connection between the requirement and the objective should be explicit. | Guidance.md | Principles P2 | -- | Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Basis | 0 | NO_ITEMS | Directive basis adequate |
| X:guiding:sufficiency | guiding | sufficiency | Validated Guidance Sufficiency | 0 | NO_ITEMS | Guidance validated through OSR citations |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Coverage | 1 | HAS_ITEMS | Drainage direction not in guidance |
| X:guiding:consistency | guiding | consistency | Principled Guidance Coherence | 0 | NO_ITEMS | Guidance principles coherent |
| X:applying:necessity | applying | necessity | Critical Practice Mandate | 0 | NO_ITEMS | Practice mandates established |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Delivery Adequacy | 1 | HAS_ITEMS | Remote control range unspecified |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Scope | 0 | NO_ITEMS | Implementation scope comprehensive |
| X:applying:consistency | applying | consistency | Consistent Execution Standard | 0 | NO_ITEMS | Execution standards consistent |
| X:judging:necessity | judging | necessity | Critical Determination Basis | 1 | HAS_ITEMS | Key commonality verification |
| X:judging:sufficiency | judging | sufficiency | Evidence-Based Adjudication | 0 | NO_ITEMS | Evidence basis adequate for adjudication |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all requirements |
| X:judging:consistency | judging | consistency | Coherent Adjudication Standard | 0 | NO_ITEMS | Adjudication standards coherent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Assurance Baseline | 1 | HAS_ITEMS | Apron cure time not specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Oversight Adequacy | 0 | NO_ITEMS | Oversight adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Coverage | 0 | NO_ITEMS | Assurance coverage comprehensive |
| X:reviewing:consistency | reviewing | consistency | Systematic Assurance Governance | 0 | NO_ITEMS | Governance consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add consideration for concrete apron drainage direction and slope requirements relative to the building and site drainage (tie to PKG-003) | Procedure verification table includes "positive drainage confirmed" for aprons, and Procedure Step B8 mentions "Confirm apron drainage direction away from building." However, Guidance does not include any consideration for apron drainage design direction or coordination with site grading (PKG-003/DEL-03-02). This gap in guidance coverage means the drainage requirement appears only in implementation-phase procedure without design-phase rationale. | Guidance.md, Procedure.md | Guidance entire document scanned, Procedure Step B8 and Verification table | -- | Design-Builder (civil) | TBD |
| X-002 | X:applying:sufficiency | WeakStatement | Procedure | Specification | Clarify "reasonable range" for overhead door remote control operation in Procedure verification; add quantified pass criterion or reference to manufacturer specification | Procedure verification table states motorized opener pass criterion as "Full cycle without fault; remote operates within reasonable range." The term "reasonable range" is subjective and could lead to inconsistent delivery adequacy determinations. | Procedure.md | Verification table, Motorized opener function | -- | Specification | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Procedure | Add verification step for key commonality (REQ-4202-08) that includes a documented physical key test at both buildings before handover | Specification verification for REQ-4202-08 states "Key schedule cross-reference with pickled-sand building hardware" which is a document check, not a physical validation. The Procedure verification table includes "Physical key test -- Same key opens cold storage and pickled-sand building person doors" which is stronger, but this physical test is not referenced in the Specification verification table. Align both documents. | Specification.md, Procedure.md | Specification Verification REQ-4202-08, Procedure Verification table | -- | Specification and Procedure | TBD |
| X-004 | X:reviewing:necessity | MissingSlot | Specification | Specification | Add requirement or verification criterion for minimum concrete apron cure time before vehicle loading | Procedure Step B8 states "Allow adequate cure time before vehicle loading" but no requirement in Specification addresses cure time or early loading restrictions. This is a mandatory assurance baseline gap -- without a minimum cure standard, the concrete apron could be loaded prematurely. | Specification.md, Procedure.md | Specification Requirements (entire section scanned), Procedure Step B8 | -- | Design-Builder (structural/civil) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Non-Negotiable Compliance Basis | 0 | NO_ITEMS | Compliance basis established through REQ-4202-09, REQ-4202-11 |
| E:normative:sufficiency | normative | sufficiency | Substantiated Compliance Sufficiency | 1 | HAS_ITEMS | Standards accessibility gap |
| E:normative:completeness | normative | completeness | Absolute Compliance Completeness | 0 | NO_ITEMS | Addressed by C-001 and C-002 |
| E:normative:consistency | normative | consistency | Invariant Compliance Governance | 0 | NO_ITEMS | Governance consistent |
| E:operative:necessity | operative | necessity | Essential Functional Requirement | 0 | NO_ITEMS | Functional requirements covered |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Functional Adequacy | 0 | NO_ITEMS | Functional adequacy demonstrated through procedures |
| E:operative:completeness | operative | completeness | Total Functional Completeness | 0 | NO_ITEMS | Functional completeness adequate |
| E:operative:consistency | operative | consistency | Dependable Functional Discipline | 0 | NO_ITEMS | Process discipline consistent |
| E:evaluative:necessity | evaluative | necessity | Non-Negotiable Value Assurance | 0 | NO_ITEMS | Value assurance present through OBJ-004 linkage |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Value Sufficiency | 0 | NO_ITEMS | Value sufficiency adequate for proposal |
| E:evaluative:completeness | evaluative | completeness | Absolute Value Completeness | 1 | HAS_ITEMS | Keying scheme broader context |
| E:evaluative:consistency | evaluative | consistency | Disciplined Value Governance | 0 | NO_ITEMS | Value governance disciplined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Multi | Specification | Normalize how standards accessibility is recorded across Specification and Datasheet; both list "Not directly accessed -- location TBD" but Datasheet uses "Not directly accessed -- location TBD" for ABC while Specification adds "ASSUMPTION: applicable" -- align the phrasing and clarify whether standards have been obtained | Under "Substantiated Compliance Sufficiency," the normative basis depends on actually having accessed the standards. The inconsistent recording of standards accessibility status between Datasheet (References table) and Specification (Standards table) makes it unclear whether the standards have been reviewed or not. | Specification.md, Datasheet.md | Specification Standards table, Datasheet References table | -- | Specification | TBD |
| E-002 | E:evaluative:completeness | TBD_Question | Datasheet | Datasheet | Record TBD: Does the common keying scheme extend to any other buildings beyond cold storage and pickled-sand? If so, document the full keying matrix for all ancillary buildings | Under "Absolute Value Completeness," the keying scheme addresses only cold storage and pickled-sand buildings. If additional ancillary buildings or the main building require key coordination, the current scope may be incomplete. The deliverable should confirm whether the keying requirement is limited to these two buildings or part of a broader master-key scheme. | Datasheet.md, Specification.md | Datasheet Person (Man) Doors table, Specification REQ-4202-08 | -- | Owner | TBD |
