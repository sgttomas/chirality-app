# Semantic Lensing Register: DEL-005-01 Preliminary Civil Design

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-01_Preliminary-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-005-01_Preliminary-Design/_CONTEXT.md (Identification, Description, Scope References, Anticipated Artifacts)
- _STATUS.md — DEL-005-01_Preliminary-Design/_STATUS.md (Current Status: SEMANTIC_READY, dated 2026-02-26)
- _SEMANTIC.md — DEL-005-01_Preliminary-Design/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed; all 7 result tables extracted)
- Datasheet.md — DEL-005-01_Preliminary-Design/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-005-01_Preliminary-Design/Specification.md (Scope, Requirements R-001 through R-013, Standards, Verification, Documentation)
- Guidance.md — DEL-005-01_Preliminary-Design/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-005-01_Preliminary-Design/Procedure.md (Prerequisites, Steps 1-9, Verification, Records)
- _REFERENCES.md — DEL-005-01_Preliminary-Design/_REFERENCES.md (R-01, R-07 listed; pointer to 0_References/ folder)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 5
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 4  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 4
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards table incomplete |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code edition TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for R-011 |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 8 covers QA review adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Design storm return period TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-9 provide adequate operational direction |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in both Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Step 8 internal QA review adequately covers process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Rationale for drainage approach selection absent |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance covers merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | County approval gate serves as worth determination mechanism |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA review in Procedure Step 8 adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta codes and municipal standards apply; populate the Standards table with confirmed edition numbers or record explicit TBDs for each | The Standards table lists four entries but three have "ASSUMPTION: applicable; specific edition TBD" or similar language. This vagueness could change compliance interpretation. | Specification.md | ## Standards | -- | PROPOSAL: Civil Engineer to confirm at permit application stage (PKG-009) | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm Alberta Building Code edition year applicable to this project (current edition not identified) | R-011 requires adherence to "all applicable Alberta building codes" but no specific code edition is identified anywhere in the production documents. | Specification.md | ### R-011 Code Compliance; ## Standards | -- | PROPOSAL: Confirm with County or PKG-009 permit process | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for R-012 (P.Eng. stamp) confirming the Civil Engineer's Alberta licensure is verified at preliminary stage | R-012 is listed as "Informational at preliminary stage" but the Verification table has no entry for R-012. Even at preliminary stage, confirming the responsible engineer's licensure is a verifiable prerequisite. | Specification.md | ## Verification | -- | PROPOSAL: Add R-012 verification row | TBD |
| A-004 | A:operative:guiding | TBD_Question | Procedure | Guidance | Record TBD: Confirm design storm return period for drainage design (e.g., 1:25 year, 1:100 year) with County or Alberta practice | Procedure Step 3.2 references "design storm return period -- TBD" and Guidance mentions "future storm events" but no specific return period is stated. This is a key input for drainage design. | Procedure.md; Guidance.md | ### Step 3 -- Develop Preliminary Grading Strategy; ## Principles | -- | PROPOSAL: Civil Engineer to confirm with County at site meeting | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for why open swales are preferred over piped drainage in a landfill context, or record that this is a design decision pending site survey | The Trade-offs table mentions swales vs. piped but the rationale is thin ("suggest open swales are likely more appropriate"). The word "likely" signals incomplete evaluation. | Guidance.md | ## Trade-offs | -- | PROPOSAL: Civil Engineer to determine based on site survey data | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Design vehicle dimensions TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotechnical data gap |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing some pad dimensions |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistent across documents where stated |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (approval gate, scope boundaries) adequately communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided is adequate for preliminary stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Narrative accounts are comprehensive for this stage |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency on pad naming |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Engineering fundamentals adequately referenced |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Role assignments clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope coverage is appropriate for preliminary design |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off structure provides discernment framework |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls identified and flagged for human ruling |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic site integration addressed in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Multi | Datasheet | Record TBD: Design vehicle GVW and turning radius dimensions for motor scraper class equipment | Procedure Step 2.1 lists GVW and turning radius as "TBD from site meeting / County confirmation." Datasheet states "motor scraper class" but provides no numeric values. These are essential facts for driving surface design. | Datasheet.md; Procedure.md | ## Attributes (Driving Surface Design Load); ### Step 2 -- Establish Design Basis | -- | PROPOSAL: Confirm at mandatory site meeting March 3, 2026 | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add geotechnical data status section or cross-reference to PKG-008 with explicit listing of assumed parameters pending geotech report | The Datasheet Conditions table references geotechnical investigation but does not record the specific assumed design parameters (subgrade bearing capacity, frost depth) that Procedure Step 2.2 identifies as TBD. | Datasheet.md | ## Conditions | -- | PROPOSAL: Populate after geotech report receipt from PKG-008 | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add dimensions for cement pads (west and east) and gravel pad (north) to Attributes table, even if recorded as TBD at preliminary stage | Datasheet records "Gravel Pad" as "dimensions TBD at final design" and cement pads by location only. No preliminary dimensions are stated despite Appendix B providing spatial layout. Recording "TBD" explicitly for each pad would improve completeness. | Datasheet.md | ## Attributes; ## Construction | -- | PROPOSAL: Extract approximate dimensions from App B or record TBD with rationale | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize pad terminology: Datasheet uses "Cement Pad" and "Gravel Pad"; Specification uses "cement pads" and "gravel pad"; Guidance references "cement pad west," "cement pad east side (near wash bay)," and "gravel pad." Establish a consistent naming convention (e.g., "Cement Pad West," "Cement Pad East," "Gravel Pad North") | Inconsistent pad naming across documents risks confusion at final design. Three distinct pad elements are referenced but not consistently named. | Datasheet.md; Specification.md; Guidance.md | ## Construction; ### R-007; ### R-008; ## Considerations | -- | PROPOSAL: Guidance to establish vocabulary note; other docs to adopt | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | Municipal development standards not identified |
| C:normative:sufficiency | normative | sufficiency | Mandated Competence | 0 | NO_ITEMS | Competence requirements (P.Eng.) stated |
| C:normative:completeness | normative | completeness | Exhaustive Obligation | 1 | HAS_ITEMS | Missing verification for R-012 |
| C:normative:consistency | normative | consistency | Harmonized Standard | 0 | NO_ITEMS | Standards references are consistent where present |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is comprehensive |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Proficiency | 0 | NO_ITEMS | Proficiency demonstrated through procedure detail |
| C:operative:completeness | operative | completeness | Complete Operational Scope | 0 | NO_ITEMS | Steps 1-9 cover the full production cycle |
| C:operative:consistency | operative | consistency | Repeatable Discipline | 1 | HAS_ITEMS | QA checklist could be more explicit |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Basis | 0 | NO_ITEMS | Value basis (County approval gate, schedule risk reduction) well stated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Judgment | 0 | NO_ITEMS | Trade-offs table provides judgment framework |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Worth assessment is appropriate for preliminary stage |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value framework is internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Identify specific Camrose County municipal development standards applicable to site grading and drainage | The Standards table acknowledges municipal/county standards as "ASSUMPTION: applicable; specific requirements TBD -- confirm with County at permit stage." Under a Regulatory Imperative lens, the absence of identified municipal standards is a gap that could affect drainage and grading compliance. | Specification.md | ## Standards | -- | PROPOSAL: County or PKG-009 permit process to provide | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification entry for R-012 (even if informational at preliminary stage) to confirm the responsible Civil Engineer holds a valid Alberta P.Eng. license | The Verification table covers R-001 through R-011 and R-013 but omits R-012. Under an Exhaustive Obligation lens, even informational requirements should have a stated verification approach for traceability. | Specification.md | ## Verification | -- | PROPOSAL: Add row confirming P.Eng. license check | TBD |
| C-003 | C:operative:consistency | WeakStatement | Procedure | Procedure | Strengthen the QA review checklist in Step 8 by adding explicit check items for topsoil stripping completeness (R-006) and mud sump access clearance (R-009) | Step 8.1 lists five review items but does not explicitly mention R-006 topsoil stripping or R-009 mud sump access. These are covered elsewhere in the procedure but omitting them from the QA checklist weakens repeatable discipline. | Procedure.md | ### Step 8 -- Internal QA Review | -- | PROPOSAL: Add checklist items | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Threshold | 1 | HAS_ITEMS | Minimum slope criteria stated as assumption |
| F:normative:sufficiency | normative | sufficiency | Defensible Compliance Basis | 1 | HAS_ITEMS | Frost depth assumption needs confirmation |
| F:normative:completeness | normative | completeness | Total Conformance Coverage | 0 | NO_ITEMS | Requirements R-001 through R-013 cover the full scope |
| F:normative:consistency | normative | consistency | Principled Regulatory Uniformity | 0 | NO_ITEMS | Requirements are consistently sourced to RFP sections |
| F:operative:necessity | operative | necessity | Validated Process Foundation | 1 | HAS_ITEMS | Scope boundary verification step missing |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Readiness | 0 | NO_ITEMS | Readiness criteria adequately stated in Prerequisites |
| F:operative:completeness | operative | completeness | Exhaustive Process Mastery | 0 | NO_ITEMS | Steps are comprehensive |
| F:operative:consistency | operative | consistency | Methodical Performance Rigor | 0 | NO_ITEMS | Process steps are methodically sequenced |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit Evidence | 0 | NO_ITEMS | Value evidence (schedule benefit, risk reduction) present in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Appraisal | 0 | NO_ITEMS | Trade-offs provide defensible appraisal framework |
| F:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 1 | HAS_ITEMS | Cost/schedule impact of geotech delay not quantified |
| F:evaluative:consistency | evaluative | consistency | Trustworthy Value Integrity | 0 | NO_ITEMS | Value assessments consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Procedure | Specification | Clarify whether the stated minimum slope criteria ("minimum 2% grade on gravel surfaces and 1% on hardstand") are requirements or assumptions; if assumptions, add to Specification as formal TBD requirements | Procedure Step 3.2 states "ASSUMPTION: minimum 2% grade on gravel surfaces and 1% on hardstand where achievable" but Specification does not include minimum slope as a requirement. Under a Mandatory Compliance Threshold lens, design slope criteria should be normatively stated or explicitly flagged as TBD. | Procedure.md; Specification.md | ### Step 3; ## Requirements | -- | PROPOSAL: Civil Engineer to confirm against Alberta practice and elevate to Specification if warranted | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Procedure | Guidance | Clarify the assumed frost penetration depth range ("approximately 1.5-2.0 m") by recording its source basis or confirming it as a conservative Alberta assumption pending geotech data | Procedure Step 2.2 states frost depth as "ASSUMPTION, location TBD for local value." The range is stated but its defensibility is not explained. Under a Defensible Compliance Basis lens, the assumption basis should be documented in Guidance. | Procedure.md | ### Step 2 -- Establish Design Basis | -- | PROPOSAL: Guidance to record assumption basis; confirm with geotech report | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add an explicit step or sub-step for verifying scope boundary between County-supplied and Proponent-supplied items before starting design (referencing Datasheet Conditions table) | Procedure Step 2.4 says "Confirm scope boundary with County" but there is no explicit verification step to confirm that the scope boundary recorded in Datasheet Conditions matches the agreed County responsibilities. Under a Validated Process Foundation lens, this is a missing operational prerequisite. | Procedure.md | ### Step 2 -- Establish Design Basis | -- | PROPOSAL: Add verification sub-step referencing Datasheet Conditions | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add discussion of cost/schedule impact if geotechnical data is not available at preliminary design stage, to support the Trade-off decision between Option A (proceed with assumptions) and Option B (wait for geotech) | The Trade-offs table presents the grading-without-geotech trade-off but does not quantify or qualitatively describe the schedule or cost impact of either option. Under a Holistic Value Accounting lens, the evaluation basis is incomplete. | Guidance.md | ## Trade-offs | -- | PROPOSAL: Civil Engineer or Project Manager to provide schedule impact estimate | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Prescriptive Boundary | 1 | HAS_ITEMS | Scope exclusion boundary could be stronger |
| D:normative:applying | normative | applying | Established Compliance Practice | 0 | NO_ITEMS | Compliance practices established in Specification |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 1 | HAS_ITEMS | County approval criteria not defined |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Examination | 0 | NO_ITEMS | Procedure Step 8 and Verification table adequate |
| D:operative:guiding | operative | guiding | Grounded Workflow Stewardship | 0 | NO_ITEMS | Procedure provides grounded workflow |
| D:operative:applying | operative | applying | Resolved Execution Readiness | 0 | NO_ITEMS | Prerequisites and steps address readiness |
| D:operative:judging | operative | judging | Definitive Capability Judgment | 1 | HAS_ITEMS | Driving surface design capability verification |
| D:operative:reviewing | operative | reviewing | Settled Procedural Verification | 0 | NO_ITEMS | Verification checklists present |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Direction | 0 | NO_ITEMS | Guidance Purpose section establishes worth direction |
| D:evaluative:applying | evaluative | applying | Justified Worth Realization | 0 | NO_ITEMS | Trade-offs and Considerations address value realization |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Determination | 1 | HAS_ITEMS | No acceptance criteria from County perspective |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Reliability | 0 | NO_ITEMS | QA process covers quality confirmation |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | MissingSlot | Specification | Specification | Add explicit statement in Scope Exclusions that utility routing and tie-in (PKG-018) is excluded from the preliminary civil grading, and that landscape planting (PKG-007) is excluded | The Specification exclusions list covers structural design, landscape planting, utility routing, and others, but the boundary with PKG-007 landscape integration is only addressed in Guidance. Under a Binding Prescriptive Boundary lens, the normative exclusion boundary should be explicit in the Specification. | Specification.md; Guidance.md | ### What this deliverable excludes; ## Considerations | -- | PROPOSAL: Specification to include explicit PKG-007 boundary statement | TBD |
| D-002 | D:normative:judging | MissingSlot | Specification | Specification | Add acceptance criteria or expected evaluation dimensions that the County project team will use to judge the preliminary civil design submission (e.g., completeness of drainage approach, consistency with App B, design basis clarity) | R-001 states "shall be delivered to the County project team for review and approval" but does not define what criteria the County will apply. Under a Definitive Conformance Verdict lens, the absence of defined acceptance criteria leaves the approval gate ambiguous. | Specification.md | ### R-001 County Approval; ## Verification | -- | PROPOSAL: Confirm County acceptance criteria at site meeting or project award | TBD |
| D-003 | D:operative:judging | VerificationGap | Specification | Specification | Add verification approach for driving surface design that includes confirmation of turning radius adequacy (not just stating design vehicle in narrative) | The Verification table for R-004/R-005 says "Design narrative confirms gravel surface and states design loading basis (motor scraper class); cross-section included" but does not mention turning radius adequacy check. Specification R-005 explicitly requires accommodation of turning radius. | Specification.md | ## Verification (R-004 / R-005 row) | -- | PROPOSAL: Add turning radius check to verification approach | TBD |
| D-004 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add discussion of what constitutes a "successful" preliminary design from the County's perspective, beyond the binary approval/rejection gate | Guidance states the deliverable is an "approval gate" but provides no insight into what the County values most in the submission (e.g., clarity of assumptions vs. completeness of layout vs. drainage confidence). Under a Conclusive Merit Determination lens, the evaluation framework for the County's decision is absent. | Guidance.md | ## Purpose; ## Principles | -- | PROPOSAL: Civil Engineer to discuss with County PM at project award | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Essential Directive Foundation | 0 | NO_ITEMS | Directives are grounded in RFP citations |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Guidance Scope | 1 | HAS_ITEMS | Guidance silent on PKG-002 structural coordination |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Coverage | 0 | NO_ITEMS | Guidance covers all major design aspects |
| X:guiding:consistency | guiding | consistency | Coherent Directive Alignment | 0 | NO_ITEMS | Directives aligned across Guidance and Specification |
| X:applying:necessity | applying | necessity | Mandated Action Foundation | 1 | HAS_ITEMS | Mandatory site meeting not in Specification |
| X:applying:sufficiency | applying | sufficiency | Warranted Implementation Scope | 0 | NO_ITEMS | Implementation scope adequately covered |
| X:applying:completeness | applying | completeness | Complete Implementation Record | 1 | HAS_ITEMS | Records table missing design revision log |
| X:applying:consistency | applying | consistency | Stable Implementation Coherence | 0 | NO_ITEMS | Implementation steps are coherent across documents |
| X:judging:necessity | judging | necessity | Essential Adjudication Basis | 1 | HAS_ITEMS | Stormwater calculation basis undefined |
| X:judging:sufficiency | judging | sufficiency | Warranted Adjudication Depth | 0 | NO_ITEMS | Verification approaches have adequate depth for preliminary stage |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | All requirements have verification entries (except R-012 noted above) |
| X:judging:consistency | judging | consistency | Uniform Adjudication Standard | 0 | NO_ITEMS | Verification approaches are uniformly structured |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Traceability from SOW items to requirements incomplete |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Audit Evidence | 0 | NO_ITEMS | Evidence trails are adequate for preliminary stage |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Coverage | 0 | NO_ITEMS | Records table covers key audit artifacts |
| X:reviewing:consistency | reviewing | consistency | Stable Audit Coherence | 0 | NO_ITEMS | Audit approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Guidance | Guidance | Add a Consideration for mud sump structural coordination with PKG-002, noting that Procedure Step 6.4 identifies this as a coordination point but Guidance does not discuss the design implications | Procedure Step 6.4 states "Coordinate sump structural design with structural engineer (PKG-002)" but Guidance Considerations only mentions PKG-007 landscape coordination and PKG-008 geotech. Under a Warranted Guidance Scope lens, the PKG-002 structural coordination for the mud sump is a missing guidance topic. | Guidance.md; Procedure.md | ## Considerations; ### Step 6 | -- | PROPOSAL: Add consideration for PKG-002 sump coordination | TBD |
| X-002 | X:applying:necessity | Normalization | Multi | Specification | Add the mandatory site meeting (March 3, 2026) as a prerequisite or input reference in the Specification, not only in the Procedure | The mandatory site meeting is described in Procedure Step 1.2 and Prerequisites but is not referenced in the Specification. Under a Mandated Action Foundation lens, a mandatory input event should be recognized in the normative document. | Specification.md; Procedure.md | ## Prerequisites; ### Step 1 | -- | PROPOSAL: Add site meeting reference to Specification scope or prerequisites | TBD |
| X-003 | X:applying:completeness | MissingSlot | Procedure | Procedure | Add a "Design revision log" entry to the Records table to track design iterations prior to County submission, distinct from the revision log in Step 9.3 which covers post-submission revisions only | The Records table lists "Revision log (Step 9.3, if applicable)" but this only covers County-requested revisions. Internal design iterations before submission are not explicitly recorded. Under a Complete Implementation Record lens, pre-submission revision tracking is a missing slot. | Procedure.md | ## Records | -- | PROPOSAL: Add internal design iteration log to Records | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add verification basis for R-002 stormwater adequacy: define whether positive drainage is demonstrated by calculation, narrative, or drawing annotation; and whether storm event capacity requires a calculation or qualitative assessment at preliminary stage | Verification for R-002 states "Grading plan reviewed by Civil Engineer to confirm positive drainage slopes" but does not specify whether calculations are required or if narrative confirmation suffices at preliminary stage. Under an Essential Adjudication Basis lens, the evidentiary basis for the drainage verdict is undefined. | Specification.md | ## Verification (R-002 row) | -- | PROPOSAL: Civil Engineer to define verification rigor appropriate for preliminary stage | TBD |
| X-005 | X:reviewing:necessity | Normalization | Datasheet | Datasheet | Add a cross-reference column or note in Datasheet linking each Construction element to its corresponding Specification requirement ID (R-001 through R-013) and SOW item, to support traceability audits | Datasheet Construction table references SOW items but does not link to Specification requirement IDs. Specification requirements reference SOW items independently. Under an Essential Audit Foundation lens, bidirectional traceability between Datasheet elements and Specification requirements is missing. | Datasheet.md | ## Construction | -- | PROPOSAL: Add requirement ID cross-reference to Datasheet | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 1 | HAS_ITEMS | Guidance conflict table provenance |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering information is coherent |
| E:guiding:knowledge | guiding | knowledge | Authoritative Steering Mastery | 0 | NO_ITEMS | Engineering knowledge adequately represented |
| E:guiding:wisdom | guiding | wisdom | Principled Advisory Foresight | 0 | NO_ITEMS | Foresight demonstrated in trade-offs and timing considerations |
| E:applying:data | applying | data | Verified Execution Record | 0 | NO_ITEMS | Execution records adequately defined in Procedure |
| E:applying:information | applying | information | Contextualized Action Intelligence | 0 | NO_ITEMS | Action context well provided |
| E:applying:knowledge | applying | knowledge | Proficient Delivery Mastery | 0 | NO_ITEMS | Delivery steps show proficiency |
| E:applying:wisdom | applying | wisdom | Principled Implementation Judgment | 0 | NO_ITEMS | Implementation judgment demonstrated in procedure |
| E:judging:data | judging | data | Authoritative Verdict Evidence | 1 | HAS_ITEMS | Conflict evidence incomplete |
| E:judging:information | judging | information | Grounded Verdict Intelligence | 0 | NO_ITEMS | Verdict intelligence adequately grounded |
| E:judging:knowledge | judging | knowledge | Authoritative Judgment Mastery | 0 | NO_ITEMS | Judgment criteria established |
| E:judging:wisdom | judging | wisdom | Principled Verdict Foresight | 0 | NO_ITEMS | Foresight items identified in trade-offs |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | _REFERENCES.md incomplete |
| E:reviewing:information | reviewing | information | Contextualized Audit Intelligence | 0 | NO_ITEMS | Audit context adequate |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Inspection Mastery | 0 | NO_ITEMS | Inspection approach adequate for preliminary stage |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Forward-looking audit items (geotech confirmation, TBDs) identified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Conflict | Guidance | Guidance | Clarify the relationship between the cement pad east of the wash bay mud sump and the other cement pads: Guidance CNF-005-01-01 identifies this as a potential conflict between App B layout and RFP text, but the Datasheet Construction table treats them as separate line items without noting the ambiguity | Guidance Conflict Table identifies CNF-005-01-01 regarding cement pad configuration ambiguity between App B and RFP. The Datasheet does not reflect this conflict. Under an Authoritative Guidance Record lens, the conflict record should be cross-referenced so that downstream documents acknowledge it. | Guidance.md; Datasheet.md | ## Conflict Table; ## Construction | Guidance.md#Conflict Table vs. Datasheet.md#Construction | PROPOSAL: Datasheet to add note referencing CNF-005-01-01 | TBD |
| E-002 | E:judging:data | VerificationGap | Specification | Specification | Add verification approach for confirming that the preliminary layout is consistent with App B conceptual drawings (currently stated only as an informal cross-check in Procedure Step 7.3, not in Specification Verification table) | The Verification table for R-007 and R-008 says "consistent with App B conceptual drawing" but the method of confirming consistency (overlay, dimensional comparison, etc.) is not specified. Procedure Step 7.3 mentions a cross-check but this is not formalized in Specification. Under an Authoritative Verdict Evidence lens, the evidentiary standard for App B consistency is undefined. | Specification.md; Procedure.md | ## Verification (R-007, R-008 rows); ### Step 7 | -- | PROPOSAL: Define consistency check method in Specification Verification | TBD |
| E-003 | E:reviewing:data | RationaleGap | Datasheet | Datasheet | Add references R-02 (addenda), R-04, R-05, R-06 to the Datasheet References table, or explain why only R-01 and R-07 are listed when the Procedure and Specification reference the full set | Datasheet References table lists only R-01, R-04, R-07, and the Decomposition file. The _REFERENCES.md file lists only R-01 and R-07. Procedure Prerequisites references R-01, R-02, R-04, R-05, R-06, R-07. Under a Verified Audit Record lens, the reference inventory across documents is inconsistent and the Datasheet/REFERENCES.md appear incomplete. | Datasheet.md; _REFERENCES.md; Procedure.md | ## References; ## Primary References; ## Prerequisites | -- | PROPOSAL: Align Datasheet References and _REFERENCES.md with full reference set used in Specification and Procedure | TBD |
