# Semantic Lensing Register: DEL-014-01 50,000L Cistern & Distribution

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-01_Cistern
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-01_Cistern/_CONTEXT.md (Deliverable Overview, Scope of Work, Technical Context)
- _STATUS.md — DEL-014-01_Cistern/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-01_Cistern/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — DEL-014-01_Cistern/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-014-01_Cistern/Specification.md (Scope, Requirements REQ-014-01-001 through -010, Standards, Verification, Documentation)
- Guidance.md — DEL-014-01_Cistern/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-014-01_Cistern/Procedure.md (Prerequisites, Steps Phases 1-6, Verification, Records)
- _REFERENCES.md — DEL-014-01_Cistern/_REFERENCES.md (Primary References, SOW Documentation, Objective References, Related Deliverables)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 6
  - Specification: 12
  - Guidance: 5
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 4  F: 5  D: 3  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 9
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Freeze protection req lacks prescriptive specificity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Tank material TBD blocks mandatory practice definition |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standards table lacks specific clause references |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection process adequately covered in Procedure Phase 4 and Specification REQ-014-01-010 |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Pump electrical specs TBD blocks procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Steps 3.1-3.5 cover practical execution sequence adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No acceptance criteria for pressure test pass/fail |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure Verification table and Records section are adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section addresses value orientation adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance provides adequate merit analysis |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Documents address cost/benefit considerations in Guidance Trade-offs |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality is addressed through verification and commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-014-01-008 from "TBD" placeholder to a concrete prescriptive requirement once IFC design confirms freeze protection method (insulation class, heat trace spec, or building envelope strategy) | REQ-014-01-008 is currently a TBD assumption, not a prescriptive direction; this leaves the normative baseline incomplete for freeze protection | Specification.md | REQ-014-01-008: Freeze Protection | -- | IFC Plumbing Designer / P.Eng. | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm cistern tank material (HDPE, concrete, fiberglass, steel) and pipe material for distribution system | Tank material and pipe material are both listed as "TBD" in Datasheet; without material specification, mandatory practice cannot be fully defined | Datasheet.md | Attributes > Cistern (Tank material); Construction (Pipe material) | -- | IFC Plumbing Designer | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add specific Alberta Safety Code clause references and National Plumbing Code clause references to the Standards table, replacing "ASSUMPTION: likely applicable; location TBD" entries | Compliance determination requires identified standard clauses; the Standards table currently has four entries marked "ASSUMPTION" or "TBD" for applicability | Specification.md | Standards table | -- | P.Eng. / Safety Codes Officer | TBD |
| A-004 | A:operative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm pump motor voltage, amperage, starter type, and motor power requirement | Pump motor power requirement is TBD in Datasheet; Procedure Step 1.3 requires these specs for electrical coordination but they do not yet exist | Datasheet.md; Procedure.md | Attributes > Distribution Pump (Motor power requirement); Steps > Phase 1 > Step 1.3 | -- | IFC Plumbing Designer / Electrical Designer | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for pressure test (test pressure value, hold duration, allowable pressure drop) to the Verification table for REQ-014-01-004 and REQ-014-01-005 | Procedure Step 4.2 calls for pressure testing "per applicable Alberta Safety Code / plumbing code requirements" but neither the Specification Verification table nor Procedure specifies the numeric test parameters | Specification.md; Procedure.md | Verification table (REQ-014-01-004, REQ-014-01-005); Steps > Phase 4 > Step 4.2 | -- | P.Eng. / Alberta Plumbing Code | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Cistern placement (above vs below grade) unresolved |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Pump type TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet provides comprehensive attribute tables with sources |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Numeric values (50,000L, 100 LPM, 2.5") are consistent across all four documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Water quality classification signal missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for site conditions and operating environment is adequate in Datasheet Conditions table |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide a comprehensive narrative across all four documents |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | "Service water" vs potential potable use inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of cistern system function is well established across documents |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents demonstrate competent expertise appropriate for this deliverable stage |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage is appropriate for a design-build project at pre-IFC stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance Principles section provides essential discernment on key decisions |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table exercises adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance Considerations section provides holistic coverage of coordination needs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential datum: cistern installation type (above-grade, below-grade, or partially recessed) once determined in IFC design | Cistern type is stated as "Below-grade or above-grade" (unresolved) in Datasheet Attributes; this is an essential fact for structural coordination, freeze protection design, and installation sequencing | Datasheet.md | Attributes > Cistern (Tank type) | -- | IFC Plumbing Designer / Structural Engineer | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add pump type specification (centrifugal, positive displacement, submersible, etc.) once determined | Pump type is listed as "TBD" in Datasheet; adequate evidence for procurement and installation planning requires pump type selection | Datasheet.md | Attributes > Distribution Pump (Pump type) | -- | IFC Plumbing Designer | TBD |
| B-003 | B:information:necessity | Conflict | Multi | Guidance | Resolve water quality classification: is the cistern system potable or non-potable service water? This determination affects applicable Alberta Safety Code requirements, treatment needs, and cross-connection prevention obligations | The system is described as "service water distribution" (RFP/Specification) but plumbing drawing shows a water tap near washroom area which could imply potable use; Guidance Conflict Table already flags this as CONF-014-01-01 and CONF-014-01-02 | Specification.md; Guidance.md | REQ-014-01-005; REQ-014-01-006; Conflict Table CONF-014-01-01, CONF-014-01-02 | Specification.md#REQ-014-01-005 ("service water distribution"); Guidance.md#Conflict-Table (CONF-014-01-01: "water quality classification not stated") | Owner / Alberta Health Services | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: use either "service water" or "non-potable service water" consistently; clarify whether "water tap" at washroom implies potable classification | "Internal service water distribution" (Specification REQ-014-01-005, Datasheet) vs. "water tap" at "washroom area" (Datasheet Distribution Points) creates ambiguity about water quality classification | Specification.md; Datasheet.md | REQ-014-01-005; Distribution Points table | -- | Owner / P.Eng. | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Statutory Baseline | 1 | HAS_ITEMS | Statutory baseline incomplete without identified code clauses |
| C:normative:sufficiency | normative | sufficiency | Authorized Compliance Threshold | 1 | HAS_ITEMS | CSA standard for cistern vessel TBD |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Scope | 0 | NO_ITEMS | RFP source requirements are comprehensively captured in Specification REQ-014-01-001 through -010 |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Regulatory references are consistent across documents where stated |
| C:operative:necessity | operative | necessity | Critical Operational Capacity | 1 | HAS_ITEMS | Simultaneous demand capacity not verified |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Basis | 0 | NO_ITEMS | Procedure provides a competent six-phase execution basis |
| C:operative:completeness | operative | completeness | Thorough Execution Coverage | 0 | NO_ITEMS | Procedure covers procurement through closeout adequately |
| C:operative:consistency | operative | consistency | Stable Methodical Performance | 0 | NO_ITEMS | Procedure steps are methodically sequenced |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Guidance Purpose section establishes intrinsic merit |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Benefit Appraisal | 1 | HAS_ITEMS | Cistern sizing trade-off lacks quantitative demand data |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Assessment | 0 | NO_ITEMS | Guidance Trade-offs table provides holistic assessment of key decisions |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value judgments are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add specific Alberta Plumbing Code edition and clause numbers applicable to cistern installations, replacing "ASSUMPTION: likely applicable; location TBD" | An enforceable statutory baseline requires identified code provisions; the Standards table currently relies on assumptions about applicability | Specification.md | Standards table (rows 1, 2, 4) | -- | P.Eng. / Safety Codes Officer | TBD |
| C-002 | C:normative:sufficiency | MissingSlot | Specification | Specification | Add applicable CSA or ASTM standard number for cistern vessel (if pressure vessel or water storage tank standards apply) once tank type/material are determined | The Standards table row for "CSA standards for cistern/pressure vessel" is marked "TBD"; the authorized compliance threshold for the vessel itself is incomplete | Specification.md | Standards table (row 5: "CSA standards for cistern/pressure vessel") | -- | IFC Plumbing Designer / P.Eng. | TBD |
| C-003 | C:operative:necessity | RationaleGap | Guidance | Guidance | Add rationale for whether the 100 LPM pump minimum is adequate for simultaneous multi-point demand (pressure washer reel + water taps + emergency shower concurrently) | Guidance Principle 2 flags this concern ("100 LPM minimum may be a single-point floor") but does not provide a demand calculation basis or reference to confirm; this is a critical operational capacity question | Guidance.md | Principles > Principle 2 (Pump sizing must match distribution demand) | -- | IFC Plumbing Designer | TBD |
| C-004 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add quantitative water demand estimate (litres per shift, fill frequency analysis) to support the cistern sizing trade-off | Guidance Trade-offs table row 1 (Cistern sizing) recommends evaluating "water consumption per shift" but no quantitative basis is provided; warranted benefit appraisal requires data to justify size decision | Guidance.md | Trade-offs table (row 1: Cistern sizing) | -- | Owner / Operations Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Legal Anchor | 1 | HAS_ITEMS | Backflow prevention requirement absent |
| F:normative:sufficiency | normative | sufficiency | Justified Regulatory Minimum | 0 | NO_ITEMS | RFP minimums (50,000L, 100 LPM, 2.5") adequately justified in Specification |
| F:normative:completeness | normative | completeness | Exhaustive Statutory Coverage | 1 | HAS_ITEMS | No requirement for backflow prevention / cross-connection control |
| F:normative:consistency | normative | consistency | Consistent Statutory Measure | 0 | NO_ITEMS | Statutory references are internally consistent |
| F:operative:necessity | operative | necessity | Essential Execution Mandate | 1 | HAS_ITEMS | Cistern overflow/drainage provision not specified |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Adequacy | 0 | NO_ITEMS | Procedure demonstrates adequate six-phase coverage |
| F:operative:completeness | operative | completeness | Complete Operational Coverage | 1 | HAS_ITEMS | No flushing/disinfection step before commissioning |
| F:operative:consistency | operative | consistency | Consistent Execution Discipline | 0 | NO_ITEMS | Procedure steps are consistently structured |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 0 | NO_ITEMS | Quality imperatives adequately addressed through code compliance and verification |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Benchmark | 1 | HAS_ITEMS | No water quality testing at commissioning |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 0 | NO_ITEMS | Quality coverage is appropriate for this deliverable stage |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality treatment is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement for backflow prevention device(s) on the cistern fill connection and/or distribution system per Alberta Plumbing Code cross-connection control provisions | Backflow prevention is a mandatory legal anchor for plumbing systems in Alberta; no requirement addressing cross-connection control or backflow prevention exists in the current Specification | Specification.md | entire document scanned (no backflow/cross-connection requirement found) | -- | P.Eng. / Alberta Plumbing Code | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for cistern overflow provision and/or high-level alarm to prevent uncontrolled water discharge during bulk fill operations | Exhaustive statutory coverage for water storage requires overflow management; neither Specification nor Datasheet addresses overflow provisions | Specification.md; Datasheet.md | entire document scanned (no overflow requirement found) | -- | IFC Plumbing Designer / P.Eng. | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add step for verifying cistern overflow/drainage provisions during installation (Phase 3) and testing overflow function during commissioning (Phase 5) | Essential execution requires overflow management; Procedure has no step for installing or testing overflow provisions | Procedure.md | Steps (Phases 3 and 5 scanned) | -- | IFC Plumbing Designer | TBD |
| F-004 | F:operative:completeness | VerificationGap | Procedure | Procedure | Add a flushing and/or disinfection step before commissioning (between Phase 4 and Phase 5) per standard plumbing practice for new water distribution systems | Complete operational coverage for a new water distribution system should include flushing debris from piping before placing the system in service; this step is absent from Procedure | Procedure.md | Steps (Phase 4 to Phase 5 transition) | -- | P.Eng. / Alberta Plumbing Code | TBD |
| F-005 | F:evaluative:sufficiency | VerificationGap | Specification | Specification | Add verification method for water quality at commissioning (bacteriological test and/or turbidity check if system serves potable fixtures), contingent on resolution of water quality classification (see B-003) | The Verification table has no water quality test; if the system serves washroom fixtures, a quality benchmark test at commissioning is standard practice | Specification.md | Verification table (no water quality row) | -- | P.Eng. / Alberta Health Services (if potable) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Prescriptive Authority | 0 | NO_ITEMS | Prescriptive authority established through RFP citations and P.Eng. stamp requirement |
| D:normative:applying | normative | applying | Fixed Compliance Method | 1 | HAS_ITEMS | Compliance method for REQ-014-01-008 is TBD pending IFC design |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Specification Verification table provides conformance ruling basis for most requirements |
| D:normative:reviewing | normative | reviewing | Standardized Compliance Examination | 0 | NO_ITEMS | Alberta Safety Code inspection process is standardized and covered |
| D:operative:guiding | operative | guiding | Settled Operational Direction | 0 | NO_ITEMS | Procedure provides settled operational direction |
| D:operative:applying | operative | applying | Validated Active Deployment | 0 | NO_ITEMS | Six-phase deployment procedure is adequate |
| D:operative:judging | operative | judging | Settled Capability Determination | 1 | HAS_ITEMS | No pump head/pressure acceptance criterion |
| D:operative:reviewing | operative | reviewing | Systematic Workflow Assurance | 0 | NO_ITEMS | Procedure Verification table and Records section provide systematic assurance |
| D:evaluative:guiding | evaluative | guiding | Principled Merit Guidance | 0 | NO_ITEMS | Guidance Principles section provides principled merit guidance |
| D:evaluative:applying | evaluative | applying | Settled Benefit Realization | 0 | NO_ITEMS | Benefits are articulated in Guidance Purpose section |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Verdict | 1 | HAS_ITEMS | Duplex pump trade-off unresolved |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Examination | 0 | NO_ITEMS | Quality examination is addressed through verification and commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-014-01-008 verification method from "TBD -- design review of IFC plumbing documents" to a concrete inspection/test method once IFC design confirms freeze protection approach | The fixed compliance method for freeze protection is entirely TBD; verification cannot be applied until the requirement itself is defined | Specification.md | Verification table (REQ-014-01-008 row) | -- | IFC Plumbing Designer / P.Eng. | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add pump discharge pressure or head acceptance criterion to verify pump can serve the most remote/elevated distribution point at adequate pressure | Specification verifies pump flow (100 LPM) but not pump head or discharge pressure; capability determination is incomplete without pressure performance criteria | Specification.md | Verification table (REQ-014-01-002 row) | -- | IFC Plumbing Designer | TBD |
| D-003 | D:evaluative:judging | WeakStatement | Guidance | Guidance | Clarify trade-off recommendation on pump configuration (single vs. duplex): state whether operational continuity risk at a working landfill warrants the cost of duplex pump, or record as requiring human ruling | Guidance Trade-offs row 3 says "ASSUMPTION: Recommend considering duplex configuration for operational continuity. Human ruling recommended" but does not quantify downtime cost or provide a decision framework | Guidance.md | Trade-offs table (row 3: Pump configuration) | -- | Owner / Operations Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Anchored Directional Foundation | 0 | NO_ITEMS | Directional foundation is anchored in RFP and decomposition |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Adequacy | 0 | NO_ITEMS | Guidance provides justified directional adequacy |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Coverage | 1 | HAS_ITEMS | No guidance on cistern access/maintenance provisions |
| X:guiding:consistency | guiding | consistency | Coherent Guidance Alignment | 0 | NO_ITEMS | Guidance is coherent with Specification and Procedure |
| X:applying:necessity | applying | necessity | Validated Practice Foundation | 1 | HAS_ITEMS | No practice for cistern level monitoring |
| X:applying:sufficiency | applying | sufficiency | Justified Practice Competence | 0 | NO_ITEMS | Procedure demonstrates justified practice competence |
| X:applying:completeness | applying | completeness | Exhaustive Practice Coverage | 0 | NO_ITEMS | Practice coverage is appropriate for project stage |
| X:applying:consistency | applying | consistency | Harmonized Practice Reliability | 0 | NO_ITEMS | Practice is harmonized across Procedure and Specification |
| X:judging:necessity | judging | necessity | Binding Verdict Foundation | 0 | NO_ITEMS | Verification table provides binding verdict foundation for most requirements |
| X:judging:sufficiency | judging | sufficiency | Justified Verdict Adequacy | 1 | HAS_ITEMS | REQ-014-01-009 verification is long-duration only |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Scope | 0 | NO_ITEMS | Judgment scope covers all ten requirements |
| X:judging:consistency | judging | consistency | Coherent Judgment Integrity | 0 | NO_ITEMS | Verification methods are coherent with requirement types |
| X:reviewing:necessity | reviewing | necessity | Mandatory Audit Foundation | 0 | NO_ITEMS | Audit foundation established through inspection process |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Audit Adequacy | 0 | NO_ITEMS | Audit adequacy is justified through records and reporting |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 1 | HAS_ITEMS | No review/audit mechanism for guarantee period defect tracking |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Integrity | 0 | NO_ITEMS | Audit integrity is harmonized across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on cistern access provisions (manhole sizing, cleanout locations) and recommended maintenance frequency; Guidance Considerations mentions this as an assumption but provides no rationale for what provisions are needed | Exhaustive guidance coverage should include maintenance access rationale; Guidance mentions "access provisions (manholes, cleanouts) should be included in the IFC design" but provides no sizing guidance or standard reference | Guidance.md | Considerations > Cistern Access, Cleaning, and Maintenance | -- | IFC Plumbing Designer / O&M standards | TBD |
| X-002 | X:applying:necessity | MissingSlot | Datasheet | Datasheet | Add cistern level monitoring/indication method (sight glass, float switch, electronic level sensor) to Datasheet Attributes once determined in IFC design | No provision for cistern water level indication appears in any document; a validated practice foundation for bulk water management requires knowing when to order refill | Datasheet.md | Attributes > Cistern (no level monitoring row) | -- | IFC Plumbing Designer / Owner | TBD |
| X-003 | X:judging:sufficiency | WeakStatement | Specification | Specification | Clarify verification method for REQ-014-01-009 (Guarantee period): add pre-CCC deficiency inspection and/or handover checklist as a concrete verification event, rather than only "Contract compliance; defect log during 2-year warranty period" | The current verification method for the guarantee requirement is purely reactive (defect log over 2 years); a justified verdict at CCC issuance needs a proactive pre-handover inspection | Specification.md | Verification table (REQ-014-01-009 row) | -- | PM / Owner | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Procedure | Procedure | Add a guarantee-period defect tracking record to the Records table, or reference a project-level warranty tracking process | Exhaustive audit coverage requires a mechanism for tracking defects during the 2-year guarantee period; Procedure Records section has no warranty-period tracking entry | Procedure.md | Records table | -- | PM / Owner | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Validated Directional Evidence | 1 | HAS_ITEMS | Coupling type for 2.5" fill connection undefined |
| E:guiding:information | guiding | information | Coherent Advisory Intelligence | 0 | NO_ITEMS | Advisory information is coherent across Guidance sections |
| E:guiding:knowledge | guiding | knowledge | Authoritative Guidance Mastery | 0 | NO_ITEMS | Guidance demonstrates authoritative mastery of coordination needs |
| E:guiding:wisdom | guiding | wisdom | Principled Advisory Foresight | 0 | NO_ITEMS | Guidance Considerations and Trade-offs exercise principled foresight |
| E:applying:data | applying | data | Demonstrated Practice Evidence | 1 | HAS_ITEMS | 2.5" fill connection terminology inconsistency |
| E:applying:information | applying | information | Coherent Practice Intelligence | 0 | NO_ITEMS | Practice information is coherent across Procedure and Specification |
| E:applying:knowledge | applying | knowledge | Authoritative Practice Mastery | 0 | NO_ITEMS | Practice knowledge is appropriate for project stage |
| E:applying:wisdom | applying | wisdom | Principled Practice Foresight | 0 | NO_ITEMS | Procedure demonstrates foresight through prerequisite management |
| E:judging:data | judging | data | Validated Judgment Evidence | 0 | NO_ITEMS | Judgment evidence is validated through verification methods |
| E:judging:information | judging | information | Coherent Verdict Intelligence | 0 | NO_ITEMS | Verdict information is coherent |
| E:judging:knowledge | judging | knowledge | Authoritative Verdict Mastery | 0 | NO_ITEMS | Verdict knowledge is appropriate |
| E:judging:wisdom | judging | wisdom | Principled Judicial Foresight | 0 | NO_ITEMS | Judicial foresight is demonstrated through phased verification |
| E:reviewing:data | reviewing | data | Validated Audit Evidence | 0 | NO_ITEMS | Audit evidence requirements are validated in Records table |
| E:reviewing:information | reviewing | information | Coherent Audit Intelligence | 0 | NO_ITEMS | Audit intelligence is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Audit Mastery | 1 | HAS_ITEMS | Emergency shower feed assumption unresolved |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm coupling type for the 2.5-inch cistern filling connection (cam-lock, threaded, flanged, etc.) to enable coordination with DEL-014-03 bulk water fill system | Validated directional evidence requires the coupling specification; Guidance Considerations flags the need for coupling compatibility with DEL-014-03 but no coupling type is specified anywhere | Datasheet.md; Guidance.md | Attributes > Cistern (Fill connection diameter); Considerations > Coordination with Bulk Water Fill System | -- | IFC Plumbing Designer / DEL-014-03 contractor | TBD |
| E-002 | E:applying:data | Normalization | Specification | Specification | Normalize the description of the 2.5-inch connection: Specification REQ-014-01-003 calls it "cistern filling connection" while REQ-014-01-002 describes the pump as having "a 2.5 inch cistern filling connection for internal service water distribution"; clarify whether the 2.5" connection is the cistern inlet (for bulk fill from DEL-014-03) or a pump connection | The RFP text "Pump capable of 100 LPM complete with a 2.5 inch cistern filling connection" is ambiguous: is the 2.5" connection on the pump outlet to the cistern, or is it the external fill inlet? The Specification repeats this ambiguity | Specification.md | REQ-014-01-002; REQ-014-01-003 | Specification.md#REQ-014-01-002 ("pump...with a 2.5 inch cistern filling connection"); Specification.md#REQ-014-01-003 ("cistern filling connection shall be 2.5 inches") | Owner / P.Eng. (RFP interpretation) | TBD |
| E-003 | E:reviewing:knowledge | Conflict | Guidance | Guidance | Resolve whether the emergency shower is fed from the cistern distribution system or from a separate supply; documents make conflicting assumptions | Datasheet lists emergency shower as a "downstream consumer" with "(ASSUMPTION: combined cold water supply)" and Guidance Purpose says "(ASSUMPTION: fed from cistern supply network)" but Specification Scope explicitly excludes "Emergency shower plumbing (DEL-014-05)" as out of scope; if DEL-014-05 handles emergency shower plumbing, the cistern documents should not assume it as a distribution point | Specification.md; Datasheet.md; Guidance.md | Scope > Out of Scope ("Emergency shower plumbing DEL-014-05"); Conditions > Downstream consumers; Purpose | Specification.md#Out-of-Scope ("DEL-014-05"); Datasheet.md#Conditions ("ASSUMPTION: combined cold water supply"); Guidance.md#Purpose ("ASSUMPTION: fed from cistern supply network") | IFC Plumbing Designer / PM | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- All 96 matrix cells (A:12, B:16, C:12, F:12, D:12, X:16, E:16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in evidence or explicit absence with provenance |
| Provenance present | PASS -- Every item has SourcePath + SectionRef |
| Conflicts surfaced | PASS -- 2 conflicts (B-003, E-003) have Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts match actual warranted items (28 total) |
| Schema followed | PASS -- Output uses the STRUCTURE schema |
