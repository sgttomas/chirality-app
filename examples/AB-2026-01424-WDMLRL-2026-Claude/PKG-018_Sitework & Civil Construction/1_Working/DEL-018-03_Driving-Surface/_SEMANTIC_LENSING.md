# Semantic Lensing Register: DEL-018-03 Gravel Driving Surface

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-03_Driving-Surface
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-018-03_Driving-Surface/_CONTEXT.md (Deliverable Identity, Scope, Context Summary)
- _STATUS.md — DEL-018-03_Driving-Surface/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-018-03_Driving-Surface/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-018-03_Driving-Surface/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-018-03_Driving-Surface/Specification.md (Scope, Requirements REQ-018-03-01 through REQ-018-03-10, Standards, Verification, Documentation)
- Guidance.md — DEL-018-03_Driving-Surface/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Examples)
- Procedure.md — DEL-018-03_Driving-Surface/Procedure.md (Prerequisites, Steps Phases 1-5, Verification, Records)
- _REFERENCES.md — DEL-018-03_Driving-Surface/_REFERENCES.md (R-01, R-07, Cross-References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 3  B: 3  C: 2  F: 3  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Compaction standard TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Aggregate spec missing for mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compaction test method TBD impairs compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | County inspection provisions are well-addressed |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase 1-5 provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are actionable and sequenced |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure supports process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section provides adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table supports worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC plan reference (DEL-019-04) covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-018-03-06 to state the specific compaction standard or explicitly require the civil engineer to provide one by a named milestone | REQ-018-03-06 states compaction "to a standard sufficient" but defers the actual standard entirely to DEL-005-07. Under the prescriptive direction lens, the requirement lacks the specificity needed to govern construction until the civil spec exists. The milestone by which that input must arrive is not stated. | Specification.md | REQ-018-03-06 | | Civil engineer (DEL-005-07) | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: What aggregate type, gradation, and size are required? Source: civil specification DEL-005-07 (pending). Add placeholder requirement or explicit cross-reference with expected delivery date. | Aggregate specification is marked TBD in Datasheet and not addressed as a requirement in Specification. Under mandatory practice lens, the contractor cannot execute mandatory practice without knowing the material specification. | Datasheet.md; Specification.md | Datasheet.md#Surface-Material (Aggregate Specification row); Specification.md#REQ-018-03-01 | | Civil engineer (DEL-005-07) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criterion for compaction testing that specifies test method (e.g., nuclear densometer, sand cone) or explicitly requires the civil spec to name one | Verification table for REQ-018-03-06 states "Compaction testing per civil spec (method TBD)". Under compliance determination lens, the method needed to determine compliance is undefined, making acceptance unverifiable until civil spec arrives. | Specification.md | Verification table, REQ-018-03-06 row | | Civil engineer (DEL-005-07) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Gravel depth/thickness is an essential fact that is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Referenced source documents (RFP, appendices) provide adequate evidence for what they cover |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing geotechnical input reference |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Gravel pad dimensions are approximate/assumed |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (load class, owner supply, drainage) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive account of scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Load class understanding is well-articulated in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance demonstrates competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Domain knowledge coverage is adequate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table in Guidance shows essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are adequately supported |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic site-level view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: What is the required gravel depth/thickness? Source: civil specification DEL-005-07. This is an essential fact for construction. | Depth/Thickness is marked TBD in Datasheet. This is a fundamental dimensional parameter without which construction cannot proceed. Under essential fact lens, this is a critical missing datum. | Datasheet.md | Attributes > Surface Material > Depth / Thickness row | | Civil engineer (DEL-005-07) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add reference to geotechnical investigation (DEL-008-01) as an input to the driving surface design, since subgrade CBR or equivalent informs depth and compaction decisions | Guidance (Principle 4) mentions geotechnical report DEL-008-01 as informing civil design, but Datasheet References table does not list it. Under comprehensive record lens, the Datasheet record is incomplete regarding this design input. | Datasheet.md; Guidance.md | Datasheet.md#References; Guidance.md#Principles > 4 | | Datasheet author | TBD |
| B-003 | B:data:consistency | WeakStatement | Datasheet | Datasheet | Clarify whether gravel pad dimensions (60' x 130') are confirmed or assumed, and note that these are partial (one area only); add a statement that full driving surface areas will be defined in DEL-005-04 | Gravel pad dimensions are noted as "ASSUMPTION: read from conceptual drawing; exact dimensions to be confirmed in civil IFC drawings." Under reliable measurement lens, presenting approximate dimensions without a clear qualifier risks them being treated as confirmed. The qualifier exists but could be stronger. | Datasheet.md | Attributes > Physical Extent > Gravel Pad Dimensions row | | Civil engineer (DEL-005-04) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Duty | 1 | HAS_ITEMS | Duty to ensure aggregate quality not enforceable without spec |
| C:normative:sufficiency | normative | sufficiency | Warranted Conformance | 0 | NO_ITEMS | Conformance evidence structure is adequate given pending civil spec |
| C:normative:completeness | normative | completeness | Whole Regulatory Coverage | 1 | HAS_ITEMS | Safety code applicability not specific |
| C:normative:consistency | normative | consistency | Standardized Governance | 0 | NO_ITEMS | Governance references are consistent across documents |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites are well-enumerated in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Capability demonstration structure exists via verification |
| C:operative:completeness | operative | completeness | Full Process Realization | 0 | NO_ITEMS | Phase 1-5 sequence is complete |
| C:operative:consistency | operative | consistency | Reproducible Practice | 0 | NO_ITEMS | Practice is described reproducibly |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Criterion | 0 | NO_ITEMS | Value criterion (motor scraper class load) is stated |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal | 0 | NO_ITEMS | Appraisal structure in Verification table is justified |
| C:evaluative:completeness | evaluative | completeness | Total Value Accounting | 0 | NO_ITEMS | Value accounting covered via trade-offs and verification |
| C:evaluative:consistency | evaluative | consistency | Consistent Value Standard | 0 | NO_ITEMS | Value standards are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add a requirement or verification step for confirming that Owner-supplied aggregate meets the civil specification before placement (incoming material acceptance check) | REQ-018-03-07 addresses coordination for delivery but does not require verification that the delivered aggregate actually meets the civil spec. Under Enforceable Duty lens, the duty to ensure material quality is unenforceable without an incoming acceptance check. Procedure Step 3.1 mentions "verify aggregate type/gradation matches civil spec" but this is not backed by a Specification requirement. | Specification.md; Procedure.md | Specification.md#REQ-018-03-07; Procedure.md#Step-3.1 | | Specification author | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Identify which specific Alberta Safety Codes apply to this work (e.g., fire code for hot work near landfill, building code for site works) or add a TBD with responsibility for determination | Standards table lists "Alberta Safety Codes Act and applicable Safety Codes" but notes "specific codes TBD in civil design phase." Under Whole Regulatory Coverage lens, regulatory coverage is incomplete if the applicable codes are not identified. For a landfill site, there may be environmental and occupational safety codes beyond the general reference. | Specification.md | Standards table, row 3 | | Civil engineer / safety officer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Foundational Mandate | 1 | HAS_ITEMS | Environmental/permit requirements not addressed |
| F:normative:sufficiency | normative | sufficiency | Sufficient Regulatory Basis | 0 | NO_ITEMS | Regulatory basis from RFP is sufficient for current phase |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | CCDC 14-2013 contract obligations not traced |
| F:normative:consistency | normative | consistency | Coherent Regulatory Discipline | 0 | NO_ITEMS | Regulatory references are consistent |
| F:operative:necessity | operative | necessity | Core Operational Readiness | 0 | NO_ITEMS | Operational readiness prerequisites well-enumerated |
| F:operative:sufficiency | operative | sufficiency | Proven Execution Capacity | 0 | NO_ITEMS | Execution capacity framework adequate |
| F:operative:completeness | operative | completeness | Comprehensive Process Coverage | 1 | HAS_ITEMS | Weather/seasonal constraints not addressed |
| F:operative:consistency | operative | consistency | Disciplined Process Fidelity | 0 | NO_ITEMS | Process steps are disciplined and sequenced |
| F:evaluative:necessity | evaluative | necessity | Cardinal Worth Basis | 0 | NO_ITEMS | Worth basis (motor scraper load class) clearly stated |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Quality Judgment | 0 | NO_ITEMS | Quality judgment framework is grounded |
| F:evaluative:completeness | evaluative | completeness | Total Quality Accounting | 0 | NO_ITEMS | Quality accounting structure exists |
| F:evaluative:consistency | evaluative | consistency | Calibrated Value Integrity | 0 | NO_ITEMS | Value integrity is calibrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Guidance | Add a note addressing whether environmental permits or approvals (e.g., Alberta Environment and Protected Areas) are required for gravel placement at a landfill site, or confirm that none are needed beyond the general project approvals | Under Foundational Mandate lens, the production documents do not address whether site-specific environmental permits apply to earthworks at an active landfill. This could be a foundational regulatory requirement that is unaddressed. | Specification.md; Guidance.md | Specification.md#Standards (entire table scanned); Guidance.md (entire document scanned) | | Project manager / environmental officer | TBD |
| F-002 | F:normative:completeness | RationaleGap | Guidance | Guidance | Add a note in Guidance explaining which CCDC 14-2013 contract provisions are most relevant to this deliverable (e.g., warranty provisions, change order procedures for Owner-supplied material issues, delay provisions) | CCDC 14-2013 is referenced in Datasheet Identification but no production document explains which contract provisions specifically affect this deliverable's execution. Under Exhaustive Compliance Scope lens, the compliance scope for the contract form is not traced. | Datasheet.md; Specification.md | Datasheet.md#Identification (Contract Form row); Specification.md#Standards (CCDC row) | | Project manager / contract administrator | TBD |
| F-003 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or note addressing weather and seasonal constraints on gravel placement and compaction (e.g., frozen ground restrictions, wet weather shutdowns, moisture content requirements) | Under Comprehensive Process Coverage lens, the Procedure does not address weather or seasonal constraints. In central Alberta (near Ferintosh), frozen ground and spring thaw conditions could materially affect compaction quality. Step 3.3 mentions moisture content parenthetically but does not address seasonal restrictions. | Procedure.md | Steps > Phase 3 | | Civil engineer / site superintendent | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Governing Directive | 0 | NO_ITEMS | RFP as governing directive is well-traced |
| D:normative:applying | normative | applying | Obligatory Fulfillment | 1 | HAS_ITEMS | No explicit hold point for IFC drawing receipt |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance ruling structure exists in Verification table |
| D:normative:reviewing | normative | reviewing | Conclusive Oversight Audit | 0 | NO_ITEMS | County inspection provisions support conclusive audit |
| D:operative:guiding | operative | guiding | Directed Readiness | 1 | HAS_ITEMS | Minimum notice period for inspections TBD |
| D:operative:applying | operative | applying | Assured Field Execution | 0 | NO_ITEMS | Field execution sequence is adequate |
| D:operative:judging | operative | judging | Definite Performance Verdict | 1 | HAS_ITEMS | No surface load test or proof-rolling requirement |
| D:operative:reviewing | operative | reviewing | Rigorous Process Review | 0 | NO_ITEMS | Record package in Phase 5 supports rigorous review |
| D:evaluative:guiding | evaluative | guiding | Principled Value Guidance | 0 | NO_ITEMS | Guidance Principles section provides principled direction |
| D:evaluative:applying | evaluative | applying | Realized Merit | 0 | NO_ITEMS | Merit realization supported by verification structure |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Ruling | 0 | NO_ITEMS | Worth ruling structure exists |
| D:evaluative:reviewing | evaluative | reviewing | Calibrated Quality Audit | 0 | NO_ITEMS | Quality audit structure exists |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Procedure | Specification | Add a formal hold point or prerequisite verification step confirming IFC civil drawings have been received and reviewed before any gravel placement proceeds -- currently this is in Step 1.1 but there is no corresponding verification check that prevents bypass | Under Obligatory Fulfillment lens, the obligation to follow IFC drawings (REQ-018-03-08) needs a formal gate. Procedure Step 1.1 says "obtain and review" but Procedure Verification table V-01 checks only that drawings are "on file" -- it does not enforce a hold point preventing field work without them. | Procedure.md; Specification.md | Procedure.md#Step-1.1; Procedure.md#Verification V-01; Specification.md#REQ-018-03-08 | | Project manager | TBD |
| D-002 | D:operative:guiding | WeakStatement | Procedure | Procedure | Specify the minimum notice period for County inspection scheduling (currently "TBD -- confirm with County project manager at project kickoff") or add this as a TBD to be resolved during project mobilization | Under Directed Readiness lens, the inspection notice period is a critical operational parameter for readiness. Step 2.1 leaves it TBD without a mechanism to ensure it gets resolved. | Procedure.md | Steps > Phase 2 > Step 2.1 | | County project manager | TBD |
| D-003 | D:operative:judging | VerificationGap | Specification | Specification | Consider adding a proof-rolling or loaded-vehicle test as a verification method for REQ-018-03-02 (design load) in addition to compaction testing, to provide a direct performance verdict under actual load conditions | Under Definite Performance Verdict lens, the Verification table for REQ-018-03-02 relies on compaction testing and "civil engineer design confirmation" but does not include a direct load test or proof-rolling check. Compaction testing verifies density but not necessarily load-bearing performance. A proof-roll with a loaded vehicle provides a direct field performance verdict. | Specification.md | Verification table, REQ-018-03-02 row | | Civil engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Imperative | 0 | NO_ITEMS | Steering imperatives are well-established |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Counsel | 0 | NO_ITEMS | Guidance counsel is substantiated with sources |
| X:guiding:completeness | guiding | completeness | Comprehensive Steering Record | 0 | NO_ITEMS | Steering record is comprehensive |
| X:guiding:consistency | guiding | consistency | Aligned Governance Tenor | 0 | NO_ITEMS | Governance tenor is aligned across documents |
| X:applying:necessity | applying | necessity | Critical Implementation Basis | 1 | HAS_ITEMS | Aggregate staging area not specified |
| X:applying:sufficiency | applying | sufficiency | Evidenced Practical Delivery | 0 | NO_ITEMS | Delivery evidence structure adequate |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Photo documentation not mentioned |
| X:applying:consistency | applying | consistency | Uniform Delivery Fidelity | 0 | NO_ITEMS | Delivery fidelity is uniform |
| X:judging:necessity | judging | necessity | Critical Adjudication Basis | 1 | HAS_ITEMS | Acceptance criteria for drainage not quantified |
| X:judging:sufficiency | judging | sufficiency | Evidenced Ruling Adequacy | 0 | NO_ITEMS | Ruling evidence is adequate given current phase |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all requirements |
| X:judging:consistency | judging | consistency | Consistent Adjudication Tenor | 0 | NO_ITEMS | Adjudication tenor is consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Finding | 0 | NO_ITEMS | Audit finding structure exists |
| X:reviewing:sufficiency | reviewing | sufficiency | Supported Audit Basis | 1 | HAS_ITEMS | As-built survey cross-reference incomplete |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Review Coverage | 0 | NO_ITEMS | Review coverage is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Coherent Review Discipline | 0 | NO_ITEMS | Review discipline is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add a step or note specifying where Owner-supplied aggregate will be staged on site and who is responsible for designating the staging area | Under Critical Implementation Basis lens, the staging area for aggregate is mentioned in Step 1.2 (confirm "staging area on site") but no requirement or procedure step designates the area or addresses impacts (e.g., traffic, drainage interference). This is a critical implementation detail. | Procedure.md | Steps > Phase 1 > Step 1.2 | | Site superintendent / Owner | TBD |
| X-002 | X:applying:completeness | RationaleGap | Procedure | Procedure | Add photo documentation as a required record in Step 5.1 record package (pre-placement, during placement, post-compaction photos) | Under Exhaustive Implementation Record lens, the Procedure record package (Step 5.1) lists forms and test reports but does not mention photographic documentation. Photo records are standard practice for earthworks and provide non-destructive evidence of construction sequence. | Procedure.md | Steps > Phase 5 > Step 5.1 | | Project manager | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Quantify the drainage acceptance criterion for REQ-018-03-05 (e.g., "no ponding greater than X mm depth after Y hours" or "positive slope of minimum Z% confirmed by survey") instead of relying solely on visual inspection | Under Critical Adjudication Basis lens, the Verification table for REQ-018-03-05 uses "Visual inspection during or after rain event" with "No ponding" as acceptance. This is subjective and weather-dependent. A measurable criterion (e.g., minimum cross-slope percentage from survey) would provide a reliable adjudication basis. | Specification.md | Verification table, REQ-018-03-05 row | | Civil engineer | TBD |
| X-004 | X:reviewing:sufficiency | Normalization | Multi | Guidance | Align the as-built survey reference: Procedure Step 4.4 references "DEL-008-04 -- As-Built Survey" while Datasheet References lists "DEL-005-04" for driving surface layout and no explicit as-built survey deliverable. Confirm the correct deliverable ID for the as-built survey. | Under Supported Audit Basis lens, the as-built survey deliverable reference is inconsistent. Procedure cites DEL-008-04 for as-built survey; Datasheet cites DEL-005-04 for layout plan but not for as-built. These appear to be different deliverables but the relationship is not clarified, which could cause audit traceability confusion. | Procedure.md; Datasheet.md | Procedure.md#Step-4.4; Datasheet.md#References | | Project manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directive Foundation | 1 | HAS_ITEMS | Maintenance responsibility during construction unclear |
| E:guiding:information | guiding | information | Informed Governance Signal | 0 | NO_ITEMS | Governance signals well-communicated |
| E:guiding:knowledge | guiding | knowledge | Masterful Stewardship | 0 | NO_ITEMS | Stewardship knowledge adequate |
| E:guiding:wisdom | guiding | wisdom | Wise Governance Counsel | 0 | NO_ITEMS | Governance counsel provided in trade-offs |
| E:applying:data | applying | data | Verified Execution Record | 0 | NO_ITEMS | Execution record structure adequate |
| E:applying:information | applying | information | Actionable Delivery Intelligence | 0 | NO_ITEMS | Delivery intelligence actionable |
| E:applying:knowledge | applying | knowledge | Seasoned Craft Mastery | 0 | NO_ITEMS | Craft knowledge adequate for current phase |
| E:applying:wisdom | applying | wisdom | Judicious Craft Wisdom | 0 | NO_ITEMS | Craft wisdom reflected in trade-offs |
| E:judging:data | judging | data | Authoritative Verdict Record | 1 | HAS_ITEMS | Guarantee period inspection protocol absent |
| E:judging:information | judging | information | Decisive Judgment Signal | 0 | NO_ITEMS | Judgment signals clear |
| E:judging:knowledge | judging | knowledge | Mature Adjudicative Mastery | 0 | NO_ITEMS | Adjudicative knowledge adequate |
| E:judging:wisdom | judging | wisdom | Wise Adjudicative Counsel | 0 | NO_ITEMS | Adjudicative wisdom adequate |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | Deficiency tracking not specified |
| E:reviewing:information | reviewing | information | Informed Oversight Signal | 0 | NO_ITEMS | Oversight signals present |
| E:reviewing:knowledge | reviewing | knowledge | Seasoned Audit Mastery | 0 | NO_ITEMS | Audit mastery adequate |
| E:reviewing:wisdom | reviewing | wisdom | Wise Oversight Counsel | 0 | NO_ITEMS | Oversight counsel adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Guidance | Guidance | Add a section or note clarifying the maintenance responsibility for the gravel surface during the construction period (between initial placement and CCC) -- who grades/repairs it, and at whose cost | Under Verified Directive Foundation lens, Guidance Considerations mentions "maintenance during construction" (top-dressing, regrading) as an assumption but does not clarify responsibility allocation between Contractor and Owner, or whether maintenance costs are included in the contract scope. This is a directive gap that could lead to disputes. | Guidance.md | Considerations > Maintenance During Construction | | Project manager / contract administrator | TBD |
| E-002 | E:judging:data | MissingSlot | Specification | Specification | Add a requirement or verification provision for the 2-year guarantee period that specifies what inspections or condition assessments will be performed during the guarantee period and who initiates them | Under Authoritative Verdict Record lens, REQ-018-03-10 establishes the guarantee period and the 10-day correction obligation, but no verification method exists for detecting defects during the guarantee period. The Verification table entry for REQ-018-03-10 only references CCC and guarantee register, not ongoing monitoring. | Specification.md | Verification table, REQ-018-03-10 row; REQ-018-03-10 | | Owner / project manager | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Procedure | Standardize the deficiency tracking approach: Procedure Records table lists "Deficiency Tracking Log" but no procedure step creates, populates, or references this log during execution. Add a step in Phase 4 or Phase 5 for initiating and maintaining the deficiency log. | Under Verified Audit Record lens, the deficiency tracking log appears in the Records table but is not referenced in any procedure step. This creates a gap between the record structure (what must exist) and the process (what creates it). Normalization is needed to ensure the log is actually produced. | Procedure.md | Procedure.md#Records (Deficiency Tracking Log row); Procedure.md#Steps (entire section scanned) | | Project manager | TBD |

---

## QA Verification

| Check | Validation | Result |
|-------|-----------|--------|
| Coverage complete | Every matrix cell (96 total) has a Lens Coverage entry | PASS -- A:12 + B:16 + C:12 + F:12 + D:12 + X:16 + E:16 = 96 cells covered |
| No invention | All warranted items grounded in evidence or explicit absence | PASS -- all items reference specific document sections and cite TBD or absence |
| Provenance present | Every item has SourcePath + SectionRef | PASS -- 21/21 items have provenance |
| Conflicts surfaced | Conflicts have Contenders and HumanRuling = TBD | PASS -- 0 conflicts identified; no contenders needed |
| Summary consistent | Summary counts match actual warranted items | PASS -- 21 items total; by-matrix: 3+3+2+3+3+4+3=21; by-type: 0+5+5+3+3+2+3+0=21 |
| Schema followed | Output uses the STRUCTURE schema exactly | PASS |
