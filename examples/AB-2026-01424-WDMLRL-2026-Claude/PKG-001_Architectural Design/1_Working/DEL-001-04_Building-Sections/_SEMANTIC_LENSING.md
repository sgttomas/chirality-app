# Semantic Lensing Register: DEL-001-04 Building Sections

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-04_Building-Sections/_CONTEXT.md
- _STATUS.md — DEL-001-04_Building-Sections/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-04_Building-Sections/_SEMANTIC.md
- Datasheet.md — DEL-001-04_Building-Sections/Datasheet.md
- Specification.md — DEL-001-04_Building-Sections/Specification.md
- Guidance.md — DEL-001-04_Building-Sections/Guidance.md
- Procedure.md — DEL-001-04_Building-Sections/Procedure.md
- _REFERENCES.md — DEL-001-04_Building-Sections/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 4
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction for ABC edition |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing overhead door height values |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC clause references absent |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit approach present in Specification and Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Procedure references CAD/BIM tools as TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are adequately described in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered via Verification tables |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No inter-discipline review record template |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed in Guidance Purpose and Principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered in Guidance Trade-offs |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately addressed via Guidance trade-offs and Specification verification |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal present in Procedure verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of the Alberta Building Code applies (state "current edition as of project permit application" or specify year) | Specification REQ-009 and Standards table reference "applicable edition" without identifying which edition, creating ambiguity for compliance determination | Specification.md | REQ-009; Standards table | -- | Architect / building official | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: overhead door opening heights for repair bays and wash bay (currently only widths are recorded) | Mandatory practice for section drawings requires door opening heights; Datasheet records widths (24') but heights are TBD, and Specification REQ-008 notes heights are TBD | Datasheet.md; Specification.md | Overhead Door Openings; REQ-008 | -- | Structural engineer / door supplier | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add specific Alberta Building Code clause references for headroom, stair geometry, fire separation, and pit ventilation requirements | Compliance determination requires identifiable code clauses; Specification REQ-009 and Guidance C-03 reference Alberta Building Code but no specific clause numbers are cited anywhere in the document set | Specification.md; Guidance.md | REQ-009; Standards; C-03 | -- | Architect / code consultant | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Specify minimum CAD/BIM platform requirements or selection criteria rather than "TBD by Architect" | Procedural direction for drawing production requires knowing the tools; Procedure lists "Architectural CAD or BIM platform (TBD by Architect)" and "Discipline coordination model / clash detection (TBD)" with no criteria | Procedure.md | Prerequisites > Software and Tools | -- | Architect | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a template or minimum-content checklist for the inter-discipline coordination review record (Step B-4) | Process audit requires a reviewable record; Procedure Step B-4 requires documenting clashes and reviewer names but provides no record format or template | Procedure.md | Step B-4 | -- | Architect | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service pit dimensions are essential facts still TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Mezzanine floor elevation not established |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet provides comprehensive attribute tables |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Unit inconsistency (imperial/metric) |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals are present via cross-references between documents |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequately provided in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Comprehensive accounts present across all four documents |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 1 | HAS_ITEMS | No fire separation assessment for mezzanine |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed via P.Eng. stamp and coordination |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Document set shows thorough domain coverage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment present in Guidance principles and trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately exercised in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic perspective provided in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning evident in Guidance and Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: service pit width and depth dimensions (essential facts for section drawing production) | Service pit dimensions are essential data for section drawings; Datasheet lists "TBD (width and depth)" for Service Pit and Specification REQ-005 notes depth is "TBD -- to be confirmed by structural design" | Datasheet.md; Specification.md | Principal Spaces table; REQ-005 | -- | Structural engineer (DEL-002-06) | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Multi | Datasheet | Record TBD: mezzanine floor elevation above finished floor level (no numeric value exists anywhere in the document set) | Adequate evidence for mezzanine section production requires a floor elevation; no document provides even an assumed value. Guidance P-03 flags this as needing structural coordination but no assumed datum is offered | Datasheet.md; Specification.md; Guidance.md | Datasheet > Attributes; REQ-004; P-03 | -- | Structural engineer (DEL-002-05) | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Guidance | Standardize measurement units: Datasheet uses imperial (35', 130'x100', 24') while Procedure Step A-1 introduces metric (10,668 mm, 0.00 m). Establish a project convention and document it | Reliable measurement requires consistent units; Datasheet and Specification use imperial throughout, but Procedure Step A-1 introduces metric equivalents without noting a conversion convention | Datasheet.md; Procedure.md | Datasheet > Attributes; Procedure Step A-1 | -- | Architect / project convention | TBD |
| B-004 | B:knowledge:necessity | MissingSlot | Guidance | Guidance | Add assessment of whether mezzanine creates a separate fire compartment requiring fire separation in sections (currently noted as a question in C-03 but not resolved or tracked as a TBD) | Fundamental understanding of fire separation is needed for section content; Guidance C-03 raises the possibility that "if the mezzanine creates a separate fire compartment, this must be documented in sections" but no determination is made and no TBD is tracked | Guidance.md | C-03 | -- | Architect / code consultant | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Foundational Standard | 1 | HAS_ITEMS | Foundation design basis missing from sections |
| C:normative:sufficiency | normative | sufficiency | Authorized Compliance Justification | 0 | NO_ITEMS | Compliance justification pathway present via REQ-009 and P.Eng. stamp |
| C:normative:completeness | normative | completeness | Total Regulatory Closure | 1 | HAS_ITEMS | Incomplete code clause identification |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Discipline | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Operational readiness addressed through prerequisite tracking |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Execution Capability | 0 | NO_ITEMS | Execution capability is demonstrated through phased workflow |
| C:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 1 | HAS_ITEMS | Drawing numbering/sheet organization missing |
| C:operative:consistency | operative | consistency | Standardized Process Integrity | 0 | NO_ITEMS | Process steps are internally consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Merit of section drawing set is recognized in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Grounded Value Appraisal | 0 | NO_ITEMS | Value appraisal present in Guidance trade-offs |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Portrait | 0 | NO_ITEMS | Worth portrait adequately presented |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value statements are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement for showing foundation/footing condition at section cuts (the enforceable foundational standard for below-grade construction is absent from the section requirements) | Sections showing the service pit and slab require foundation context; Datasheet notes "Foundation -- Negotiated post-geotech report" and Specification does not require sections to show foundation conditions even generically | Specification.md; Datasheet.md | REQ-005; REQ-007; Datasheet > Construction | -- | Architect / structural engineer | TBD |
| C-002 | C:normative:completeness | RationaleGap | Guidance | Guidance | Add rationale for which National Building Code of Canada provisions apply through Alberta adoption and how they affect section content (currently listed as "ASSUMPTION: likely applicable" in Specification Standards table with no further guidance) | Total regulatory closure requires understanding the code adoption chain; Specification Standards table lists NBC as "ASSUMPTION: likely applicable" and Guidance C-03 discusses ABC implications but does not address NBC adoption | Specification.md; Guidance.md | Standards table; C-03 | -- | Architect / code consultant | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement for drawing sheet organization, numbering convention, and scale notation standard for the section drawing set | Exhaustive operational coverage requires knowing how the drawing set is organized; Specification Documentation section lists expected drawings but provides no sheet numbering convention, and Procedure produces drawings without referencing a numbering standard | Specification.md; Procedure.md | Documentation > Expected Drawing Sheet Content; entire Procedure scanned | -- | Architect | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Prescriptive Validity | 1 | HAS_ITEMS | REQ-001 section cut list is assumption-based |
| F:normative:sufficiency | normative | sufficiency | Substantiated Conformance Warrant | 0 | NO_ITEMS | Conformance warrant pathway present |
| F:normative:completeness | normative | completeness | Total Codified Governance | 0 | NO_ITEMS | Codified governance adequately scoped |
| F:normative:consistency | normative | consistency | Systematic Governance Coherence | 0 | NO_ITEMS | Governance references are coherent |
| F:operative:necessity | operative | necessity | Mission-Critical Capability Proof | 1 | HAS_ITEMS | Geotechnical report dependency untracked |
| F:operative:sufficiency | operative | sufficiency | Verified Process Competence | 0 | NO_ITEMS | Process competence demonstrated |
| F:operative:completeness | operative | completeness | Total Operational Mastery | 0 | NO_ITEMS | Operational coverage thorough |
| F:operative:consistency | operative | consistency | Disciplined Process Coherence | 0 | NO_ITEMS | Process is coherent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Discernment | 1 | HAS_ITEMS | Wash bay height profile undetermined |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Appraisal | 0 | NO_ITEMS | Merit appraisal present |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting addressed |
| F:evaluative:consistency | evaluative | consistency | Principled Worth Calibration | 0 | NO_ITEMS | Worth calibration consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-001 section cut list from ASSUMPTION to confirmed minimum requirement, or add explicit acceptance criteria for determining if the list is sufficient | Absolute prescriptive validity requires that the minimum section cut list be authoritative; REQ-001 labels its minimum cut list as "ASSUMPTION: based on space types and structural differentiation" which weakens its prescriptive force | Specification.md | REQ-001 | -- | Architect | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit tracking mechanism for geotechnical report receipt as a gate before foundation/slab assumptions are made in sections (currently listed as prerequisite but no verification step confirms receipt) | Mission-critical capability proof requires confirming prerequisite inputs; Procedure Prerequisites list geotechnical report as "Required before foundation/slab assumptions are made" but no Step or Verification check confirms its receipt or reviews its content | Procedure.md | Prerequisites > Upstream Information Required; Verification table | -- | Architect | TBD |
| F-003 | F:evaluative:necessity | WeakStatement | Guidance | Guidance | Clarify whether the wash bay has the full 35' ceiling height or a reduced height, and document rationale for the determination | Fundamental worth discernment requires understanding the wash bay vertical profile; Guidance P-01 notes "(full 35' or partial -- TBD)" for the wash bay height but this is left as an open question with no tracking or resolution pathway | Guidance.md | P-01 | -- | Architect | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Conclusive Governing Mandate | 0 | NO_ITEMS | Governing mandate is conclusively stated |
| D:normative:applying | normative | applying | Confirmed Obligatory Practice | 1 | HAS_ITEMS | Verification approach for REQ-006 is weak |
| D:normative:judging | normative | judging | Binding Regulatory Verdict | 0 | NO_ITEMS | Regulatory verdict pathway present via P.Eng. stamp |
| D:normative:reviewing | normative | reviewing | Settled Compliance Oversight | 0 | NO_ITEMS | Compliance oversight addressed |
| D:operative:guiding | operative | guiding | Authoritative Process Steering | 0 | NO_ITEMS | Process steering is authoritative in Procedure |
| D:operative:applying | operative | applying | Confirmed Operational Delivery | 1 | HAS_ITEMS | Preliminary vs. IFC content differentiation weak |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 0 | NO_ITEMS | Performance verdict pathway present |
| D:operative:reviewing | operative | reviewing | Settled Procedural Examination | 0 | NO_ITEMS | Procedural examination covered |
| D:evaluative:guiding | evaluative | guiding | Decisive Merit Direction | 0 | NO_ITEMS | Merit direction present in Guidance |
| D:evaluative:applying | evaluative | applying | Justified Value Commitment | 0 | NO_ITEMS | Value commitment justified in Guidance trade-offs |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Ruling | 1 | HAS_ITEMS | No quality acceptance criteria for section drawings |
| D:evaluative:reviewing | evaluative | reviewing | Settled Merit Verification | 0 | NO_ITEMS | Merit verification present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Strengthen verification approach for REQ-006 (Wall/Roof Assembly): "Assembly reference or legend present on drawings" is necessary but not sufficient -- add check that assembly references are consistent with DEL-001-11 Architectural Specification | Confirmed obligatory practice requires verifiable acceptance criteria; REQ-006 verification is "Assembly reference or legend present on drawings" which confirms existence but not correctness or cross-reference consistency | Specification.md | Verification table, REQ-006 row | -- | Architect | TBD |
| D-002 | D:operative:applying | WeakStatement | Specification | Specification | Define minimum content differences between Preliminary Design and IFC section drawings (Specification does not differentiate content requirements by issue stage) | Confirmed operational delivery requires knowing what "done" looks like at each stage; Specification does not distinguish preliminary vs. IFC content scope, though Procedure Step A-3 describes preliminary content informally | Specification.md; Procedure.md | Specification > Documentation > Issue States; Procedure Step A-3 | -- | Architect | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add drawing-level quality acceptance criteria (e.g., annotation completeness, dimension chain closure, scale correctness) beyond requirement-level verification | Conclusive quality ruling requires acceptance criteria at the drawing level, not only at the requirement level; Specification Verification table checks requirement fulfillment but has no criteria for drawing production quality | Specification.md | Verification table | -- | Architect | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Anchor | 0 | NO_ITEMS | Foundational steering present in Guidance Purpose |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Informed Leadership | 0 | NO_ITEMS | Leadership substantiation present |
| X:guiding:completeness | guiding | completeness | Total Directional Coverage | 1 | HAS_ITEMS | Old North Shop interface incomplete |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Clarity | 0 | NO_ITEMS | Directional clarity is harmonized |
| X:applying:necessity | applying | necessity | Validated Implementation Basis | 1 | HAS_ITEMS | Crane runway elevation prerequisite unverified |
| X:applying:sufficiency | applying | sufficiency | Proven Practice Fulfillment | 0 | NO_ITEMS | Practice fulfillment pathway present |
| X:applying:completeness | applying | completeness | Total Implementation Scope | 1 | HAS_ITEMS | Scope of renovation interface unclear |
| X:applying:consistency | applying | consistency | Coherent Execution Reliability | 0 | NO_ITEMS | Execution reliability is coherent |
| X:judging:necessity | judging | necessity | Decisive Adjudication Ground | 1 | HAS_ITEMS | No acceptance criteria for coordination review |
| X:judging:sufficiency | judging | sufficiency | Substantiated Verdict Competence | 0 | NO_ITEMS | Verdict competence present |
| X:judging:completeness | judging | completeness | Absolute Adjudication Coverage | 0 | NO_ITEMS | Adjudication coverage adequate |
| X:judging:consistency | judging | consistency | Principled Verdict Alignment | 0 | NO_ITEMS | Verdict alignment principled |
| X:reviewing:necessity | reviewing | necessity | Fundamental Audit Catalyst | 1 | HAS_ITEMS | Conflict between ceiling height interpretations |
| X:reviewing:sufficiency | reviewing | sufficiency | Qualified Inspection Evidence | 0 | NO_ITEMS | Inspection evidence qualifications present |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Record | 0 | NO_ITEMS | Examination record scope adequate |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Transparency | 0 | NO_ITEMS | Audit transparency consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on when and how to document the Old North Shop interface condition in building sections (structural connection, fire separation, weatherproofing at shared boundary) | Total directional coverage requires addressing the Old North Shop interface; Guidance C-04 identifies this as TBD but provides no directional guidance on how to document it in sections or what triggers the determination | Guidance.md | C-04 | -- | Architect | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add verification step confirming crane runway beam elevation has been received from structural engineer before finalizing crane clearance sections | Validated implementation basis requires confirming critical upstream inputs; Procedure Prerequisites list crane runway beam elevations (DEL-002-07) as required but no Step explicitly gates section finalization on receipt of this data | Procedure.md | Prerequisites > Upstream Information Required; Steps B-1 through B-5 | -- | Architect | TBD |
| X-003 | X:applying:completeness | RationaleGap | Specification | Guidance | Clarify scope of renovation interface shown in building sections -- Specification Excluded list excludes renovation drawings but allows "renovation interfaces with the addition are shown for context"; add guidance on what constitutes the boundary of that context | Total implementation scope requires knowing the boundary; Specification Scope > Excluded states "except where renovation interfaces with the addition are shown for context" without defining what that context includes or where it stops | Specification.md; Guidance.md | Specification > Scope > Excluded; Guidance C-04 | -- | Architect | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for the inter-discipline coordination review (REQ-010) -- currently verification is "no unresolved clashes at IFC" but no threshold or method for determining "unresolved" is defined | Decisive adjudication ground requires a clear threshold; Specification Verification for REQ-010 states "Inter-discipline review completed; no unresolved clashes at IFC" but does not define what constitutes a clash, how clashes are categorized, or what "unresolved" means | Specification.md | Verification table, REQ-010 row | -- | Architect | TBD |
| X-005 | X:reviewing:necessity | Conflict | Multi | NA | Surface conflict: 35' ceiling height is described as "Concrete structure 35' ceiling" (RFP/Datasheet) which could mean structural frame height or finished interior ceiling height. Guidance C-002 already flags this but it remains unresolved across documents | Fundamental audit catalyst: this ambiguity affects every section drawing datum; Datasheet states "35' (concrete structure)" and Guidance Conflict C-002 identifies the ambiguity but all documents continue to use "35' ceiling height" without resolving whether this is finished ceiling or structural frame height | Datasheet.md; Specification.md; Guidance.md | Datasheet > Attributes; Specification REQ-002; Guidance C-002 | Datasheet.md#Attributes (35' concrete structure); Guidance.md#C-002 (ambiguity flagged) | Human ruling required per Guidance C-002 | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directional Authority | 1 | HAS_ITEMS | Cistern location not addressed in sections |
| E:guiding:information | guiding | information | Contextualized Steering Signal | 0 | NO_ITEMS | Steering signals are contextualized |
| E:guiding:knowledge | guiding | knowledge | Integrated Leadership Mastery | 0 | NO_ITEMS | Leadership mastery demonstrated in Guidance |
| E:guiding:wisdom | guiding | wisdom | Judicious Strategic Foresight | 0 | NO_ITEMS | Strategic foresight present in trade-offs |
| E:applying:data | applying | data | Confirmed Execution Record | 1 | HAS_ITEMS | Execution record for County approval incomplete |
| E:applying:information | applying | information | Contextualized Action Briefing | 0 | NO_ITEMS | Action briefing adequately contextualized |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Execution mastery demonstrated |
| E:applying:wisdom | applying | wisdom | Judicious Implementation Foresight | 0 | NO_ITEMS | Implementation foresight present |
| E:judging:data | judging | data | Definitive Evidentiary Finding | 1 | HAS_ITEMS | No section-specific QA checklist |
| E:judging:information | judging | information | Transparent Adjudication Account | 0 | NO_ITEMS | Adjudication account transparent |
| E:judging:knowledge | judging | knowledge | Authoritative Judgment Mastery | 0 | NO_ITEMS | Judgment mastery present |
| E:judging:wisdom | judging | wisdom | Prudent Ruling Discernment | 0 | NO_ITEMS | Ruling discernment adequate |
| E:reviewing:data | reviewing | data | Verified Inspection Evidence | 1 | HAS_ITEMS | Normalization of "section" terminology |
| E:reviewing:information | reviewing | information | Transparent Audit Accounting | 0 | NO_ITEMS | Audit accounting transparent |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Inspection Mastery | 0 | NO_ITEMS | Inspection mastery present |
| E:reviewing:wisdom | reviewing | wisdom | Prudent Inspection Discernment | 0 | NO_ITEMS | Inspection discernment adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | MissingSlot | Datasheet | Specification | Add consideration of whether the 50,000 L water cistern location requires a section cut or notation on building sections (Datasheet records its existence but no section requirement addresses it) | Verified directional authority requires that all significant building elements be accounted for in section scope; Datasheet records "Water Storage Area -- 50,000 L cistern location" but Specification REQ-001 section cut list does not mention it and Guidance does not discuss it | Datasheet.md; Specification.md | Datasheet > Principal Spaces; Specification REQ-001 | -- | Architect | TBD |
| E-002 | E:applying:data | VerificationGap | Procedure | Procedure | Add verification check confirming County approval has been received and any County comments have been addressed before proceeding to Phase B (IFC) | Confirmed execution record requires evidence of stage-gate completion; Procedure Step A-6 describes submission to County but Verification table only states "County written approval record -- After Step A-6" without making it a gate condition for Phase B | Procedure.md | Step A-6; Verification table | -- | Architect / County | TBD |
| E-003 | E:judging:data | MissingSlot | Specification | Procedure | Add a section-drawing-specific QA checklist as an artifact (e.g., dimension chain closure, annotation completeness, grid line consistency, scale block accuracy) to support definitive evidentiary findings at review | Definitive evidentiary finding requires structured evidence; Procedure Step B-5 references "final drawing review" and "all TBD items resolved" but no checklist artifact is specified for the reviewer to complete | Specification.md; Procedure.md | Specification > Verification; Procedure Step B-5 | -- | Architect | TBD |
| E-004 | E:reviewing:data | Normalization | Multi | Guidance | Standardize terminology: Specification uses "Building Sections" as a drawing set name, but Specification Documentation table uses "Section" as a prefix for individual drawings. Ensure consistent naming convention across documents (e.g., "Section A-A" vs. "Building Section A-A") | Verified inspection evidence requires consistent naming; Specification Documentation table lists drawings as "Section -- Longitudinal (primary)" etc., while the deliverable title and all other references use "Building Sections" -- individual section naming convention is not defined | Specification.md; Datasheet.md | Specification > Documentation > Expected Drawing Sheet Content; Datasheet > Identification | -- | Architect | TBD |
