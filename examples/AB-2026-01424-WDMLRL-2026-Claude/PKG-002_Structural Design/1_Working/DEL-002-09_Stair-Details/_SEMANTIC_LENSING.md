# Semantic Lensing Register: DEL-002-09 Stair Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-09_Stair-Details/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-09_Stair-Details/_CONTEXT.md (Identification, Description, Anticipated Artifacts)
- _STATUS.md — DEL-002-09_Stair-Details/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-09_Stair-Details/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed; 96 cells total)
- Datasheet.md — DEL-002-09_Stair-Details/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-002-09_Stair-Details/Specification.md (Scope, Requirements REQ-001 through REQ-008, Standards, Verification, Documentation)
- Guidance.md — DEL-002-09_Stair-Details/Guidance.md (Purpose, Principles P-1 through P-5, Considerations C-1 through C-5, Trade-offs, Conflict Table)
- Procedure.md — DEL-002-09_Stair-Details/Procedure.md (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md — DEL-002-09_Stair-Details/_REFERENCES.md (R-01, R-04 listed; no scope expansion)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 2
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 4  B: 2  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition not identified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Stair material TBD affects mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No specific ABC clause references |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit path adequately described |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Welding standard assumption unresolved |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in Spec and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA steps covered in Procedure Step 4 |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose and value orientation clear in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off table present in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately covered by Guidance trade-offs and conflict table |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks present in Procedure verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify the specific Alberta Building Code edition and clause numbers governing stair geometry, live loads, and guardrails | REQ-004 states "comply with all applicable Alberta Safety Codes and the Alberta Building Code" but no edition year or clause references are provided; this leaves prescriptive direction incomplete | Specification.md | REQ-004 -- Code Compliance | -- | Structural Engineer / Building Code authority (PROPOSAL) | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm stair structural material selection (steel vs. concrete) so that mandatory practice requirements (material standards, fabrication codes) can be determined | Stair material is TBD in Datasheet; mandatory practice cannot be fully specified until material is selected because CSA S16 vs. CSA A23.3 applicability depends on this choice | Datasheet.md | Attributes -- Stair structural material | -- | Structural Engineer (PROPOSAL) | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen REQ-004 verification approach: specify which code clauses will be checked and by what method (e.g., dimension check against ABC Table X.X) | Verification for REQ-004 says "P.Eng. review and building permit authority review" but does not identify specific code clauses or acceptance criteria, making compliance determination vague | Specification.md | Verification -- REQ-004 | -- | Specification.md (PROPOSAL) | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify welding/bolting standard reference in Step 3.7: confirm whether CSA W47.1 or another standard applies and remove "or equivalent" ambiguity | Procedure Step 3.7 lists "CSA W47.1 or equivalent -- ASSUMPTION; location TBD" which is vague for practical execution; the specific standard should be confirmed before IFC | Procedure.md | Step 3 -- 3.7 General Notes | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Stair width not specified |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence from R-01 and R-04 is referenced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Several TBD values in Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements (35 ft ceiling, 130x100 ft footprint) are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (mezzanine function, load requirement) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context from RFP and decomposition referenced adequately |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set provides comprehensive account of scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across documents are coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of stair role and context is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise expectations clearly assigned to Structural Engineer |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Guidance provides thorough treatment of design considerations |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment in trade-offs and conflict identification is present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are clearly flagged as assumptions |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic perspective present in Guidance principles |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning in Guidance is principled and traceable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential datum: minimum stair width per applicable code (once ABC edition is confirmed) | Stair width is listed as "TBD (minimum per applicable Alberta Building Code)" -- this is an essential fact for structural detailing that is missing | Datasheet.md | Attributes -- Stair width | -- | Structural Engineer / ABC (PROPOSAL) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add missing data for: live load design value, tread/riser dimensions, number of stair runs, and handrail/guardrail specification once design basis is established | Six TBD entries in the Datasheet Attributes table represent gaps in the comprehensive record needed for IFC drawing production | Datasheet.md | Attributes -- multiple TBD entries | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Prerequisite | 1 | HAS_ITEMS | Geotechnical prerequisite status unresolved |
| C:normative:sufficiency | normative | sufficiency | Certified Justification | 0 | NO_ITEMS | Justification for requirements is traceable to RFP |
| C:normative:completeness | normative | completeness | Exhaustive Obligation | 1 | HAS_ITEMS | Fire rating obligation not addressed |
| C:normative:consistency | normative | consistency | Codified Coherence | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Critical Capability | 0 | NO_ITEMS | Critical capabilities identified in Procedure prerequisites |
| C:operative:sufficiency | operative | sufficiency | Workable Competence | 0 | NO_ITEMS | Procedure steps are workable given prerequisites |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 0 | NO_ITEMS | Procedure covers full lifecycle from prerequisites to IFC issue |
| C:operative:consistency | operative | consistency | Stable Execution Method | 0 | NO_ITEMS | Method is stable and repeatable as described |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Merit of deliverable is well-articulated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Adequacy | 0 | NO_ITEMS | Adequacy substantiated through RFP traceability |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal | 1 | HAS_ITEMS | No evaluation of seismic considerations |
| C:evaluative:consistency | evaluative | consistency | Principled Benchmark | 0 | NO_ITEMS | Benchmarks are principled (code-first approach) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Procedure | Specification | Add prerequisite status tracking: geotechnical investigation report is listed as TBD prerequisite but no verification step confirms its receipt before stair base anchor design begins | The geotechnical report is an enforceable prerequisite for anchor design (Procedure Prerequisites), but the Specification verification table does not check whether it has been received; this could allow design to proceed on unconfirmed bearing assumptions | Procedure.md; Specification.md | Prerequisites -- Geotechnical investigation report; Verification table | -- | Structural Engineer (PROPOSAL) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Multi | Guidance | Add consideration: fire rating requirements for stair enclosure or structural fire protection, if applicable under ABC for this occupancy and height | No document addresses whether the stair requires fire-rated enclosure or structural fire protection under the Alberta Building Code; for a 35 ft high industrial building this may be a code obligation that is absent from the exhaustive obligation scope | Specification.md; Guidance.md | entire document scanned | -- | Structural Engineer / ABC (PROPOSAL) | TBD |
| C-003 | C:evaluative:completeness | TBD_Question | Multi | Guidance | Record TBD: Confirm whether seismic design requirements apply to the stair structure under the Alberta Building Code / NBC for this geographic location and building type | No document addresses seismic design considerations for the stair; given the Alberta location this may not be critical, but the comprehensive appraisal is incomplete without confirming or excluding seismic requirements | Specification.md; Guidance.md; Datasheet.md | entire document scanned | -- | Structural Engineer / NBC (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Mandate | 0 | NO_ITEMS | Mandates from RFP are captured in requirements |
| F:normative:sufficiency | normative | sufficiency | Justified Conformance Standard | 1 | HAS_ITEMS | Standards table lacks edition specificity |
| F:normative:completeness | normative | completeness | Total Compliance Scope | 1 | HAS_ITEMS | Accessibility not addressed |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Logic | 0 | NO_ITEMS | Regulatory logic is harmonized across docs |
| F:operative:necessity | operative | necessity | Vital Operational Basis | 0 | NO_ITEMS | Operational basis in Procedure is adequate |
| F:operative:sufficiency | operative | sufficiency | Proven Preparedness | 0 | NO_ITEMS | Prerequisites table establishes preparedness |
| F:operative:completeness | operative | completeness | Exhaustive Process Scope | 0 | NO_ITEMS | Process scope is complete from design through IFC |
| F:operative:consistency | operative | consistency | Coherent Procedural Discipline | 0 | NO_ITEMS | Procedure is disciplined and internally coherent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Significance | 0 | NO_ITEMS | Significance is established in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Suitability | 0 | NO_ITEMS | Suitability demonstrated through RFP alignment |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Scope | 1 | HAS_ITEMS | No cost or schedule impact assessment |
| F:evaluative:consistency | evaluative | consistency | Principled Value Calibration | 0 | NO_ITEMS | Value calibration is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen Standards table: for each standard, specify the edition year or confirm "current edition at time of permit" and note whether the standard text is available to the design team | Standards table lists six standards with "ASSUMPTION -- likely applicable; location TBD" for most; justified conformance requires knowing which edition is being designed to | Specification.md | Standards | -- | Structural Engineer (PROPOSAL) | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Guidance | Add consideration: confirm whether barrier-free / accessibility requirements under ABC apply to this stair (e.g., if the mezzanine requires an accessible route, a stair alone may not satisfy it) | No document addresses whether the mezzanine requires barrier-free access under the Alberta Building Code; if so, the stair-only access assumption is a compliance gap | Specification.md; Guidance.md | entire document scanned | -- | Structural Engineer / ABC / Architect (PROPOSAL) | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale note: acknowledge that cost/schedule impacts of steel vs. concrete stair selection are relevant trade-off factors and should be considered alongside structural factors | The Trade-offs table in Guidance identifies structural considerations for steel vs. concrete but does not mention cost, schedule, or constructability factors that influence the valuation | Guidance.md | Trade-offs | -- | Structural Engineer / Project Manager (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Regime | 0 | NO_ITEMS | Directive regime is established through RFP requirements |
| D:normative:applying | normative | applying | Settled Obligatory Method | 0 | NO_ITEMS | Obligatory method (IFC drawing set) is well-defined |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | County approval gate not linked to verification |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Alignment | 0 | NO_ITEMS | Oversight alignment clear (P.Eng., County, permit authority) |
| D:operative:guiding | operative | guiding | Anchored Workflow Navigation | 1 | HAS_ITEMS | DEL-002-05 sequencing dependency unclear |
| D:operative:applying | operative | applying | Validated Practical Deployment | 0 | NO_ITEMS | Deployment steps are practical and validated |
| D:operative:judging | operative | judging | Conclusive Capability Finding | 0 | NO_ITEMS | Capability checks in Procedure verification table |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Integrity | 0 | NO_ITEMS | Integrity checks in Step 4 are adequate |
| D:evaluative:guiding | evaluative | guiding | Anchored Principled Priority | 0 | NO_ITEMS | Priorities well-anchored in Guidance principles |
| D:evaluative:applying | evaluative | applying | Validated Worth Recognition | 0 | NO_ITEMS | Worth recognition present in Purpose statement |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Verdict | 0 | NO_ITEMS | Worth verdict not required at this stage |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Assurance | 1 | HAS_ITEMS | No independent QA review identified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Procedure | Add verification step: confirm County approval of preliminary stair design (from Procedure Step 5) is recorded before IFC issue; link to Specification verification table | Procedure Step 5 describes County approval gate and Specification REQ-008 requires IFC format, but the Specification verification table does not include a check for County preliminary design approval as a precondition to conformance ruling | Specification.md; Procedure.md | Verification -- REQ-008; Steps 5-6 | -- | Project Manager (PROPOSAL) | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add rationale: explain the recommended sequencing between DEL-002-05 and DEL-002-09 and what to do if DEL-002-05 is not available when stair detailing must begin | Guidance P-1 says "Develop both deliverables in parallel or sequence DEL-002-05 before DEL-002-09" but does not explain what happens if DEL-002-05 is delayed; this affects anchored workflow navigation | Guidance.md | P-1 -- Integration with Mezzanine Framing | -- | Structural Engineer (PROPOSAL) | TBD |
| D-003 | D:evaluative:reviewing | VerificationGap | Procedure | Procedure | Add verification step: identify whether an independent P.Eng. review (separate from the engineer of record) is required or recommended before IFC issue | Procedure Step 4 describes self-review by the Structural Engineer but does not identify an independent quality assurance reviewer; for IFC documents bearing a P.Eng. stamp, an independent check may be warranted | Procedure.md | Step 4 -- Internal Quality Review; Step 6 -- IFC Issue | -- | Structural Engineer / Project Manager (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Sovereign Steering Foundation | 0 | NO_ITEMS | Steering foundation is sovereign (RFP + code) |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Competence | 0 | NO_ITEMS | Directional competence justified through referenced docs |
| X:guiding:completeness | guiding | completeness | Exhaustive Strategic Record | 1 | HAS_ITEMS | DEL-002-08 cross-reference incomplete |
| X:guiding:consistency | guiding | consistency | Harmonized Leadership Standard | 0 | NO_ITEMS | Leadership standard harmonized across docs |
| X:applying:necessity | applying | necessity | Indispensable Practice Foundation | 1 | HAS_ITEMS | Guardrail scope boundary unresolved |
| X:applying:sufficiency | applying | sufficiency | Justified Situated Practice | 0 | NO_ITEMS | Practice is justified and situated |
| X:applying:completeness | applying | completeness | Total Implementation Archive | 0 | NO_ITEMS | Implementation archive scope is total for drawing set |
| X:applying:consistency | applying | consistency | Consistent Method Standard | 0 | NO_ITEMS | Method standard is consistent |
| X:judging:necessity | judging | necessity | Binding Determination Basis | 1 | HAS_ITEMS | Live load verification gap |
| X:judging:sufficiency | judging | sufficiency | Justified Determination Finding | 0 | NO_ITEMS | Determination findings are justified |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Record | 0 | NO_ITEMS | Judgment records scope adequate |
| X:judging:consistency | judging | consistency | Integrated Conformance Measure | 0 | NO_ITEMS | Conformance measures integrated |
| X:reviewing:necessity | reviewing | necessity | Critical Assurance Foundation | 1 | HAS_ITEMS | Embedment plan cross-check is conditional |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Verification Coverage | 0 | NO_ITEMS | Verification coverage is justified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Verification Archive | 0 | NO_ITEMS | Verification archive scope adequate |
| X:reviewing:consistency | reviewing | consistency | Integrated Audit Standard | 0 | NO_ITEMS | Audit standard is integrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | Normalization | Multi | Multi | Normalize cross-reference to DEL-002-08: Guidance P-4 references it for floor embedments, Procedure Step 3.3 and Step 4.3 reference it conditionally; confirm whether DEL-002-08 is a required or conditional input and align all documents | DEL-002-08 is mentioned in Guidance P-4 as an unconditional cross-reference, but Procedure Step 3.3 and 4.3 use conditional language ("if a floor embedment is used"); this inconsistency in the strategic record could cause coordination gaps | Guidance.md; Procedure.md | P-4 -- Concrete Anchorage Detail Quality; Step 3.3; Step 4.3 | Guidance.md#P-4 vs Procedure.md#Step-3.3 | Structural Engineer (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | Conflict | Multi | Guidance | Resolve guardrail scope boundary: clarify which specific guardrail elements belong to DEL-002-09 vs. DEL-002-05, and update Specification REQ-006 accordingly | Guidance CON-001 identifies this conflict explicitly; Specification REQ-006 assigns guardrail details to this deliverable, but Guidance C-3 notes the scope boundary is ambiguous; this is a pre-existing conflict awaiting human ruling | Specification.md; Guidance.md | REQ-006; C-3; CON-001 | Specification.md#REQ-006 vs Guidance.md#CON-001 | Structural Engineer / per Guidance CON-001 proposed split (PROPOSAL) | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add specific acceptance criterion for live load: once live load design value is established, record it as an explicit acceptance criterion in the verification table for REQ-002 | REQ-002 requires mezzanine load compatibility but the verification approach ("Structural calculation review (DEL-002-10) and drawing set check for load path continuity") does not state what the target live load value is; binding determination requires a numeric threshold | Specification.md | Verification -- REQ-002 | -- | Structural Engineer (PROPOSAL) | TBD |
| X-004 | X:reviewing:necessity | Normalization | Procedure | Procedure | Normalize conditional language for DEL-002-08 cross-check in Step 4.3: either confirm the embedment is expected and make the check mandatory, or add a decision record for when it is not applicable | Procedure Step 4.3 says "If a floor embedment is used at stair base, confirm it is shown on the Embedment Plan" -- the conditional framing weakens the critical assurance foundation because it does not require a positive determination either way | Procedure.md | Step 4.3 | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Governance Repository | 0 | NO_ITEMS | Governance data repository is verified (RFP refs present) |
| E:guiding:information | guiding | information | Comprehensive Steering Message | 0 | NO_ITEMS | Steering message is comprehensive in Guidance |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Expertise | 0 | NO_ITEMS | Governance expertise is integrated |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Vision | 0 | NO_ITEMS | Governance vision is principled |
| E:applying:data | applying | data | Verified Implementation Evidence | 1 | HAS_ITEMS | Drawing set contents are assumptions |
| E:applying:information | applying | information | Coherent Implementation Account | 0 | NO_ITEMS | Implementation account is coherent |
| E:applying:knowledge | applying | knowledge | Integrated Applied Proficiency | 0 | NO_ITEMS | Applied proficiency expectations are integrated |
| E:applying:wisdom | applying | wisdom | Principled Execution Prudence | 0 | NO_ITEMS | Execution prudence is principled |
| E:judging:data | judging | data | Verified Determination Record | 0 | NO_ITEMS | Determination records are present |
| E:judging:information | judging | information | Coherent Adjudication Account | 0 | NO_ITEMS | Adjudication account is coherent |
| E:judging:knowledge | judging | knowledge | Integrated Adjudicative Mastery | 0 | NO_ITEMS | Adjudicative mastery expectations are integrated |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Prudence | 0 | NO_ITEMS | Prudence in judgment is principled |
| E:reviewing:data | reviewing | data | Verified Audit Archive | 1 | HAS_ITEMS | Records table incomplete |
| E:reviewing:information | reviewing | information | Coherent Verification Report | 0 | NO_ITEMS | Verification reporting is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Verification Mastery | 0 | NO_ITEMS | Verification mastery expectations are integrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Verification Prudence | 0 | NO_ITEMS | Verification prudence is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | MissingSlot | Specification | Specification | Add to Documentation section: confirm the minimum expected drawing set contents list (currently marked ASSUMPTION) by cross-referencing RFP requirements or structural engineering standards of practice | The Specification Documentation section lists "Minimum Expected Drawing Set Contents" as ASSUMPTION-based; verified implementation evidence requires confirming this list against the RFP or applicable standards | Specification.md | Documentation -- Minimum Expected Drawing Set Contents | -- | Structural Engineer (PROPOSAL) | TBD |
| E-002 | E:reviewing:data | TBD_Question | Procedure | Procedure | Record TBD: Confirm whether the Records table should include a record of the design team's agreement on stair location (currently mentioned in Required Authorizations but not in Records) | Procedure Required Authorizations mentions "Design team agreement on stair location, material, and scope boundary" but this agreement is not listed in the Records table; the verified audit archive should include all critical decision records | Procedure.md | Required Authorizations; Records | -- | Structural Engineer / Project Manager (PROPOSAL) | TBD |
