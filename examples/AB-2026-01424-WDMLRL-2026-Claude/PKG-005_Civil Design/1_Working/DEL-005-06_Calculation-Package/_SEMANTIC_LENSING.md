# Semantic Lensing Register: DEL-005-06 Civil Calculation Package

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-06_Calculation-Package/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-005-06_Calculation-Package/_CONTEXT.md (Identification, Description, Scope of Work References, Anticipated Artifacts)
- _STATUS.md — DEL-005-06_Calculation-Package/_STATUS.md (Current Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-005-06_Calculation-Package/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — DEL-005-06_Calculation-Package/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-005-06_Calculation-Package/Specification.md (Scope, Requirements REQ-001 through REQ-009, Standards, Verification, Documentation)
- Guidance.md — DEL-005-06_Calculation-Package/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-005-06_Calculation-Package/Procedure.md (Steps 1-9, Verification, Records)
- _REFERENCES.md — DEL-005-06_Calculation-Package/_REFERENCES.md (Primary References R-01, R-07; Additional References pointer)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 13
  - Guidance: 5
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 4  F: 5  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Design storm return period not prescribed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Specific Alberta codes not identified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compliance checklist criteria lack specificity |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit trail adequately addressed across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps well-sequenced with clear direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Utility sizing execution steps thin |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Spec and Procedure cover this |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal QA review step (Step 7) addresses process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit cost-engineering trade-off guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance trade-off table provides merit framing |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification approach adequate for worth assessment |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Checker review in Procedure covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm design storm return period(s) from applicable Alberta/Camrose County drainage standards. Add explicit return period requirement to REQ-001 or new REQ once confirmed. | RFP uses "future storm events" without specifying return periods. Guidance CONF-001 identifies this but Specification REQ-001 still lacks a numeric or standard-referenced criterion. | Specification.md; Guidance.md | Specification#REQ-001; Guidance#Conflict Table CONF-001 | -- | PROPOSAL: Civil Engineer to confirm with County per Guidance CONF-001 | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Identify specific Alberta Safety Code clauses, NBC edition, Alberta Drainage Design Guideline sections, and Camrose County bylaw numbers applicable to this project. Populate Standards table with clause-level references. | Specification Standards table lists five governing standards/codes but all have "TBD" for clause-level requirements or specific bylaw numbers. Mandatory practice cannot be verified without specific clause references. | Specification.md | Specification#Standards | -- | PROPOSAL: Civil Engineer to research and populate during Step 1 | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify acceptance criteria for REQ-006 (code compliance) verification. Current "Design compliance checklist referencing applicable Safety Codes; County inspection sign-offs" is vague without identified codes. | Without specific code clauses identified (see A-002), compliance determination has no concrete benchmark. The verification approach is circular until codes are specified. | Specification.md | Specification#Verification (REQ-006 row) | -- | PROPOSAL: Specification is normative authority for acceptance criteria | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add a step or sub-step for utility sizing calculations. Current procedure has no explicit step for civil utility sizing despite it being in scope (Specification scope, Datasheet Construction table). | Specification scope includes "Utility sizing calculations within civil scope" and Datasheet lists "Utility sizing calculations" as a calculation topic, but Procedure has no step addressing this work. | Procedure.md | entire document scanned | -- | PROPOSAL: Procedure is operative authority; add between Step 4 and Step 5 or as sub-step | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Guidance | Guidance | Add a value-orientation note on cost-engineering trade-offs for drainage infrastructure sizing, particularly the cost impact of higher vs. lower design storm return periods. | Guidance Trade-offs table mentions "Conservative (100-year) vs. minimum required by code" but frames it only as size/cost, without explicit value-engineering guidance on how to weigh cost against risk for this specific rural landfill context. | Guidance.md | Guidance#Trade-offs (Design storm return period row) | -- | PROPOSAL: Guidance is directional authority | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Site area numeric value missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotech dependency noted but no interim values |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Construction table provides comprehensive topic coverage |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units and data references consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Septic coordination signal weak |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context well-established across all four documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-references between docs provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design-build context and engineering basis well-communicated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement and method selection adequately framed |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Calculation topic coverage is thorough per scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of scope boundaries consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Landfill-specific drainage discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table and principles provide adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic view including coordination points |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with design-build and regulatory context |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify "Site Area / Building Footprint" attribute: replace "approx. 13,000 sq ft building area" with confirmed values once survey (DEL-008-02) is available, and distinguish building footprint from total site development area. | Datasheet records site area as "TBD -- geotech survey not yet completed; conceptual footprint approx. 13,000 sq ft building area." The essential fact of total development area (not just building footprint) is needed for drainage basin delineation but is not even placeholder-identified. | Datasheet.md | Datasheet#Attributes (Site Area row) | -- | PROPOSAL: Datasheet is descriptive authority | TBD |
| B-002 | B:data:sufficiency | RationaleGap | Guidance | Guidance | Add guidance on what interim design parameter values (e.g., conservative subgrade CBR, preliminary surface thickness) should be assumed for preliminary design before DEL-008-01 is available, and document the basis for those interim assumptions. | Guidance Principle 3 and Considerations note that calculations cannot be finalized before geotech, but do not explain what conservative interim values to use for preliminary design approval (Step 8). Procedure Step 4 cannot begin without some basis. | Guidance.md | Guidance#Principles (3. Upstream Data Dependency); Guidance#Considerations (Heavy Equipment Loading Context) | -- | PROPOSAL: Guidance is directional authority | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add a requirement or coordination note addressing the septic system drainage interface (DEL-006-05) as a civil drainage design input. Currently absent from Specification requirements. | Guidance mentions coordination with PKG-006 for septic and drainage outfall, but Specification has no requirement capturing this as a design input. The civil drainage calculation needs to know the septic system drainage envelope. | Specification.md; Guidance.md | Specification#Requirements (entire section scanned); Guidance#Considerations (Coordination with PKG-006) | -- | PROPOSAL: Specification is normative authority for requirements | TBD |
| B-004 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Expand the landfill site context consideration to include explicit rationale for how surface drainage near active landfill cells should be handled in the calculation package, and whether environmental regulatory approvals may be needed. | Guidance Considerations mentions not directing runoff toward active cells but labels it as an ASSUMPTION to confirm at the site meeting. No rationale is provided for what regulatory framework (e.g., Alberta EPEA) governs drainage near landfill cells. | Guidance.md | Guidance#Considerations (Landfill Site Context) | -- | PROPOSAL: Guidance is directional authority | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Design Basis | 1 | HAS_ITEMS | Enforceability gap on code clauses |
| C:normative:sufficiency | normative | sufficiency | Justified Conformance Capacity | 0 | NO_ITEMS | Conformance approach justified through verification table |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 1 | HAS_ITEMS | Regulatory coverage incomplete |
| C:normative:consistency | normative | consistency | Uniform Regulatory Alignment | 0 | NO_ITEMS | Regulatory references consistent where stated |
| C:operative:necessity | operative | necessity | Critical Execution Foundation | 1 | HAS_ITEMS | Prerequisite timing not testable |
| C:operative:sufficiency | operative | sufficiency | Adequate Procedural Competence | 0 | NO_ITEMS | Procedure demonstrates adequate competence for scope |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 0 | NO_ITEMS | Steps 1-9 cover full scope with records |
| C:operative:consistency | operative | consistency | Coherent Procedural Discipline | 0 | NO_ITEMS | Steps reference upstream data consistently |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Value basis established through RFP-linked requirements |
| C:evaluative:sufficiency | evaluative | sufficiency | Sufficient Merit Justification | 0 | NO_ITEMS | Trade-offs and rationale provide sufficient justification |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Quality Account | 1 | HAS_ITEMS | QA roles not fully defined |
| C:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality approach consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add specific code clause references to each requirement where applicable (REQ-001, REQ-003, REQ-006) so that the enforceable design basis has traceable regulatory anchors, not just general standard names. | Specification REQ-006 states "adhere to all applicable Alberta Safety Codes, applicable building codes, and municipal/county development requirements" but the Standards table shows all clause-level requirements as TBD. An enforceable design basis requires identifiable clauses. | Specification.md | Specification#REQ-006; Specification#Standards | -- | PROPOSAL: Specification is normative authority | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement addressing environmental regulatory compliance for drainage near an active landfill (e.g., Alberta EPEA or equivalent). Currently no requirement captures this regulatory dimension. | Guidance identifies the landfill context and runoff-near-active-cells concern but Specification has no requirement for environmental regulatory compliance related to landfill proximity. Comprehensive regulatory coverage requires this. | Specification.md; Guidance.md | Specification#Requirements (entire section); Guidance#Considerations (Landfill Site Context) | -- | PROPOSAL: Specification is normative authority | TBD |
| C-003 | C:operative:necessity | WeakStatement | Procedure | Procedure | Clarify prerequisite timing: add explicit hold points or gate checks that prevent Step 3 from proceeding without DEL-008-02 and Step 4 without DEL-008-01, rather than only noting "Required before Step N" in the prerequisites table. | Procedure prerequisites table states timing as "Required before Step 3" and "Required before Step 4" but the step text itself does not include a hold-point or gate check. A critical execution foundation requires enforceable sequencing. | Procedure.md | Procedure#Prerequisites; Procedure#Steps (Step 3, Step 4) | -- | PROPOSAL: Procedure is operative authority | TBD |
| C-004 | C:evaluative:completeness | VerificationGap | Procedure | Procedure | Clarify checker qualifications: Procedure Step 7.1 says "independent of preparer, also P.Eng. or under P.Eng. supervision" but does not specify whether the checker must have civil engineering competence specifically, or what "independent" means (different firm? different team?). | For a comprehensive quality account, the checker role definition should be unambiguous. Current wording could allow a non-civil P.Eng. to check civil calculations. | Procedure.md | Procedure#Steps (Step 7.1) | -- | PROPOSAL: Procedure is operative authority for process; Specification could also define acceptance criteria for checker | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Criterion | 1 | HAS_ITEMS | Slope stability trigger criteria not specified |
| F:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Capacity | 0 | NO_ITEMS | Verification table provides substantiation approach |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Record | 1 | HAS_ITEMS | Compliance record structure incomplete |
| F:normative:consistency | normative | consistency | Consistent Compliance Standard | 1 | HAS_ITEMS | Normalization issue on scope terminology |
| F:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table adequately defines upstream dependencies |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Adequacy | 0 | NO_ITEMS | Procedure steps demonstrate adequate procedural coverage |
| F:operative:completeness | operative | completeness | Exhaustive Procedural Record | 1 | HAS_ITEMS | Records list missing one item |
| F:operative:consistency | operative | consistency | Consistent Procedural Standard | 0 | NO_ITEMS | Procedure internally consistent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Criterion | 1 | HAS_ITEMS | No explicit accuracy/precision criteria |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Quality Adequacy | 0 | NO_ITEMS | QA review step demonstrates quality adequacy |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Record | 0 | NO_ITEMS | Records section comprehensive |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Standard | 0 | NO_ITEMS | Quality approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify trigger criteria for slope stability analysis in REQ or as a new requirement: specify what site conditions (e.g., cut/fill height threshold, slope angle threshold) require analysis vs. a documented determination that analysis is not required. | Specification scope says "Slope stability assessment (if site conditions require)" and Procedure Step 5 says "if required" but neither defines the trigger criteria. This is a mandatory compliance gap -- the practitioner has no defined threshold for when analysis becomes mandatory. | Specification.md; Procedure.md | Specification#Scope (What This Deliverable Covers); Procedure#Steps (Step 5) | -- | PROPOSAL: Specification is normative authority | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for cross-document consistency between the calculation package and the Civil Specification (DEL-005-07). REQ-003 verification only references DEL-005-02 and DEL-005-03 drawing cross-reference, not DEL-005-07. | Specification scope states the package supports DEL-005-07 (Civil Specification), and Procedure Step 7.3 mentions cross-document consistency with DEL-005-07, but the Specification Verification table for REQ-003 only references DEL-005-02/DEL-005-03. Exhaustive compliance record requires all downstream documents verified. | Specification.md; Procedure.md | Specification#Verification (REQ-003 row); Procedure#Steps (Step 7.3) | -- | PROPOSAL: Specification is normative authority | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Multi | Normalize terminology: "finish cut/fill" (Specification), "detailed finish grading volumes" (Datasheet), "Grading and cut/fill volume calculations" (Datasheet Construction table), "grading volumes: finish cut/fill" (Procedure Step 3.5). Adopt one term consistently. | Multiple variant phrasings for the same scope item across documents risk drift in interpretation of what grading volumes are within Proponent scope. | Specification.md; Datasheet.md; Procedure.md | Specification#Scope; Datasheet#Attributes; Datasheet#Construction; Procedure#Steps (Step 3.5) | -- | PROPOSAL: Guidance vocabulary note, then apply across all docs | TBD |
| F-004 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add a record entry for the design storm return period confirmation document (output of Step 1.4). Current Records section does not explicitly list this, though Step 1 says "Record: Site visit notes; scope confirmation memo (TBD)." | Procedure Step 1.4 directs the engineer to confirm design storm return period(s) but the Records section has no explicit entry for this confirmation artifact. The scope confirmation memo is labeled "TBD" which is ambiguous. | Procedure.md | Procedure#Steps (Step 1, Record line); Procedure#Records | -- | PROPOSAL: Procedure is operative authority | TBD |
| F-005 | F:evaluative:necessity | MissingSlot | Specification | Specification | Add a requirement or quality criterion specifying acceptable calculation accuracy/precision standards (e.g., volume calculation tolerance, flow rate significant figures, or reference to applicable engineering practice standards for calculation presentation). | No document specifies what accuracy or precision is expected for the calculations. For a fundamental quality criterion, the calculation package should define what level of precision is acceptable for each calculation type. | Specification.md | Specification#Requirements (entire section scanned) | -- | PROPOSAL: Specification is normative authority for quality criteria | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Directive | 1 | HAS_ITEMS | NBC edition not identified |
| D:normative:applying | normative | applying | Verified Mandatory Implementation | 0 | NO_ITEMS | Implementation path clear through Procedure |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Verification table provides conformance ruling framework |
| D:normative:reviewing | normative | reviewing | Authoritative Standards Verification | 0 | NO_ITEMS | Step 6 compliance verification and Step 7 review cover this |
| D:operative:guiding | operative | guiding | Resolved Procedural Priority | 0 | NO_ITEMS | Procedure step sequencing resolves priorities |
| D:operative:applying | operative | applying | Verified Practical Delivery | 0 | NO_ITEMS | Steps map to calculation topics with records |
| D:operative:judging | operative | judging | Conclusive Performance Record | 0 | NO_ITEMS | Records section comprehensive for performance documentation |
| D:operative:reviewing | operative | reviewing | Systematic Process Verification | 1 | HAS_ITEMS | County review feedback loop |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Direction | 0 | NO_ITEMS | Guidance purpose and principles establish worth direction |
| D:evaluative:applying | evaluative | applying | Verified Merit Delivery | 0 | NO_ITEMS | Trade-off analysis and design method selection cover this |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Judgment | 1 | HAS_ITEMS | No final quality sign-off criterion |
| D:evaluative:reviewing | evaluative | reviewing | Principled Merit Verification | 0 | NO_ITEMS | Checker review and P.Eng. seal provide merit verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm which edition of the National Building Code of Canada (NBC) is applicable. Specification Standards table lists NBC as "ASSUMPTION: likely applicable; edition TBD; location TBD." | A definitive regulatory directive requires the specific NBC edition to be identified. The applicable edition determines which requirements apply to civil works. | Specification.md | Specification#Standards (NBC row) | -- | PROPOSAL: Civil Engineer to confirm during project setup | TBD |
| D-002 | D:operative:reviewing | WeakStatement | Procedure | Specification | Clarify what happens if County rejects preliminary design at Step 8: add a rework loop or rejection-handling sub-step. Currently Step 8.3 says "Incorporate any County review comments" but does not address the possibility of design rejection requiring fundamental recalculation. | Systematic process verification requires a defined path for both approval and rejection outcomes. The current procedure assumes County comments are incorporable, not that the design might be rejected. | Procedure.md | Procedure#Steps (Step 8) | -- | PROPOSAL: Procedure is operative authority | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add a final quality judgment criterion: define what constitutes a "complete" calculation package (e.g., all calculation topics from Datasheet Construction table addressed, all TBDs resolved, all records from Procedure produced). | No document defines the completeness acceptance criterion for the calculation package as a whole. Individual requirement verifications exist but there is no overall completeness check. | Specification.md; Datasheet.md; Procedure.md | Specification#Verification (entire table); Datasheet#Construction; Procedure#Records | -- | PROPOSAL: Specification is normative authority | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governing Imperative | 0 | NO_ITEMS | Governing imperatives well-established from RFP |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Directive Capacity | 1 | HAS_ITEMS | Directive capacity gap on landscape coordination |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Scope | 0 | NO_ITEMS | Governance scope comprehensive across four docs |
| X:guiding:consistency | guiding | consistency | Uniform Governance Coherence | 0 | NO_ITEMS | Governance references uniform |
| X:applying:necessity | applying | necessity | Essential Delivery Foundation | 1 | HAS_ITEMS | Delivery foundation gap on stormwater approach |
| X:applying:sufficiency | applying | sufficiency | Substantiated Delivery Competence | 0 | NO_ITEMS | Delivery competence demonstrated through method selection guidance |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Scope | 0 | NO_ITEMS | Implementation scope tracks Datasheet topics |
| X:applying:consistency | applying | consistency | Uniform Implementation Coherence | 1 | HAS_ITEMS | Normalization issue on equipment loading term |
| X:judging:necessity | judging | necessity | Essential Conformance Basis | 0 | NO_ITEMS | Conformance basis established through REQ-to-verification mapping |
| X:judging:sufficiency | judging | sufficiency | Substantiated Assessment Capacity | 0 | NO_ITEMS | Assessment methods identified for each requirement |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Scope | 1 | HAS_ITEMS | Assessment scope gap |
| X:judging:consistency | judging | consistency | Uniform Assessment Coherence | 0 | NO_ITEMS | Assessment approach internally coherent |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Imperative | 0 | NO_ITEMS | Audit imperative addressed by P.Eng. and County review |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Review Capacity | 0 | NO_ITEMS | Review capacity adequate with checker + County |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Scope | 0 | NO_ITEMS | Review scope covers all steps |
| X:reviewing:consistency | reviewing | consistency | Uniform Verification Coherence | 0 | NO_ITEMS | Verification approach uniform across requirements |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Guidance | Guidance | Add coordination guidance for communicating civil drainage design outputs (final grades, outfall locations) to the Landscape Architect (PKG-007) as a procedural step or Guidance coordination note with specific information exchange requirements. | Guidance mentions coordination with PKG-007 but only as a general statement. No specific information exchange items are identified (e.g., which grades, which outfall coordinates, what format). Substantiated directive capacity requires actionable coordination content. | Guidance.md | Guidance#Considerations (Coordination with PKG-007) | -- | PROPOSAL: Guidance is directional authority; Procedure could also add a coordination sub-step | TBD |
| X-002 | X:applying:necessity | TBD_Question | Multi | Guidance | Record TBD: Determine preferred stormwater management approach (detention pond, infiltration, directed outfall, or combination) before detailed drainage calculations. Document decision basis in Guidance trade-off resolution. | Guidance Trade-offs table lists stormwater management approach as TBD after geotech. However, the calculation procedure (Step 3.3) assumes features can be sized without first resolving this fundamental approach decision. The essential delivery foundation for drainage calculations depends on this. | Guidance.md; Procedure.md | Guidance#Trade-offs (Stormwater management approach row); Procedure#Steps (Step 3.3) | -- | PROPOSAL: Civil Engineer decision documented in Guidance | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Multi | Normalize the driving surface load reference: Datasheet says "motor scraper class," Specification REQ-004 says "large construction equipment (motor scraper class as minimum)," Procedure Step 4.1 says "motor-scraper-class equipment." Adopt one consistent term. | Minor but potentially significant: "motor scraper class as minimum" in Specification implies other heavier equipment might also need to be considered, while Datasheet and Procedure use it as the design load itself. This could affect design calculation inputs. | Datasheet.md; Specification.md; Procedure.md | Datasheet#Attributes (Driving Surface Design Load); Specification#REQ-004; Procedure#Steps (Step 4.1) | -- | PROPOSAL: Specification is normative authority for the design load definition | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification approach for REQ-009 (topsoil stripping) that specifies how stripping volume accuracy will be confirmed (e.g., comparison with surveyed stripping depth, reconciliation with County-performed work). | Specification Verification table for REQ-009 says "Stripping volumes and extents included or cross-referenced in calculations" which is a completeness check but not a verification of accuracy or correctness of the volumes themselves. | Specification.md | Specification#Verification (REQ-009 row) | -- | PROPOSAL: Specification is normative authority | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Governance Record | 0 | NO_ITEMS | Governance data well-recorded across docs |
| E:guiding:information | guiding | information | Coherent Governance Signal | 0 | NO_ITEMS | Governance signals coherent |
| E:guiding:knowledge | guiding | knowledge | Authoritative Steering Mastery | 0 | NO_ITEMS | Steering knowledge adequate in Guidance |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Insight | 0 | NO_ITEMS | Principles and considerations provide governance insight |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Revision control gap |
| E:applying:information | applying | information | Coherent Execution Account | 0 | NO_ITEMS | Execution account coherent across Procedure |
| E:applying:knowledge | applying | knowledge | Demonstrated Execution Mastery | 0 | NO_ITEMS | Execution methods well-described |
| E:applying:wisdom | applying | wisdom | Principled Execution Insight | 0 | NO_ITEMS | Design-build context provides execution insight |
| E:judging:data | judging | data | Verified Assessment Record | 1 | HAS_ITEMS | Assessment record gap on pre-development baseline |
| E:judging:information | judging | information | Coherent Assessment Account | 0 | NO_ITEMS | Assessment information coherent |
| E:judging:knowledge | judging | knowledge | Demonstrated Judgment Mastery | 0 | NO_ITEMS | Judgment knowledge adequate through verification methods |
| E:judging:wisdom | judging | wisdom | Principled Judgment Insight | 0 | NO_ITEMS | Judgment principles adequate |
| E:reviewing:data | reviewing | data | Verified Audit Record | 0 | NO_ITEMS | Audit records specified in Procedure |
| E:reviewing:information | reviewing | information | Coherent Audit Account | 1 | HAS_ITEMS | Conflict between Spec and Guidance on REQ-004 source |
| E:reviewing:knowledge | reviewing | knowledge | Demonstrated Audit Mastery | 0 | NO_ITEMS | Audit knowledge adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Insight | 0 | NO_ITEMS | Audit insight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Datasheet | Datasheet | Add a revision control field or version tracking row to the Datasheet Identification table so that changes to key parameters (e.g., site area once survey complete, geotech data once available) are tracked with dates and sources. | Datasheet has multiple TBD values that will be updated as upstream deliverables become available. Without revision tracking, the verified execution record cannot confirm which version of parameters was used in calculations. | Datasheet.md | Datasheet#Identification | -- | PROPOSAL: Datasheet is descriptive authority | TBD |
| E-002 | E:judging:data | RationaleGap | Guidance | Guidance | Add rationale and method guidance for establishing the pre-development drainage baseline: specify what data sources (survey, historical records, aerial imagery), what analysis method (rational method, SCS CN, etc.), and what documentation standard is expected for the baseline. | Procedure Step 2 directs the engineer to document pre-development conditions but neither Guidance nor Specification specifies what analysis method or documentation standard to use. The verified assessment record for REQ-002 (no neighbour drainage alteration) depends on a defensible baseline, but the method is left entirely to practitioner discretion without guidance. | Procedure.md; Guidance.md | Procedure#Steps (Step 2); Guidance#Principles (5. Neighbour Drainage Non-Alteration) | -- | PROPOSAL: Guidance is directional authority | TBD |
| E-003 | E:reviewing:information | Conflict | Specification | Specification | Resolve inconsistency: Specification REQ-004 Source cites "R-01 section 3.3.2; Decomposition SOW-0077" but Datasheet Attributes cite only "R-01 section 3.3.2" for Driving Surface Design Load. SOW-0077 is not mentioned in Datasheet or Context. Confirm SOW-0077 is the correct SOW reference and add it to Datasheet if so. | The SOW reference for driving surface design differs between Specification and Datasheet. This is a minor but real inconsistency that could cause confusion during traceability audits. | Specification.md; Datasheet.md | Specification#REQ-004 (Source line); Datasheet#Attributes (Driving Surface Design Load row) | Specification.md#REQ-004 (cites SOW-0077); Datasheet.md#Attributes (does not cite SOW-0077) | PROPOSAL: Confirm correct SOW from Decomposition, update both docs to match | TBD |

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | PASS -- All 96 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in document evidence or explicit absence |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- 1 conflict (E-003) has Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts match actual warranted items (28 total) |
| Schema followed | PASS -- Output follows STRUCTURE schema |
