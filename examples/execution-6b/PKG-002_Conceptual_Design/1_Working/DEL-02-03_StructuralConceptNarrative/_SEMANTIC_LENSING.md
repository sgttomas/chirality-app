# Semantic Lensing Register: DEL-02-03 Structural Concept Narrative

**Generated:** 2026-02-17
**Deliverable Folder:** test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/_CONTEXT.md
- _STATUS.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/_STATUS.md
- _SEMANTIC.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/_SEMANTIC.md
- Datasheet.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/Datasheet.md
- Specification.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/Specification.md
- Guidance.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/Guidance.md
- Procedure.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/Procedure.md
- _REFERENCES.md — test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-03_StructuralConceptNarrative/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 5
  - Specification: 5
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 3  B: 4  C: 2  F: 2  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 4
  - WeakStatement: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | NBCC edition not specified |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Mandatory practices well covered across documents |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Post-disaster exemption verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit approach adequately addressed in Procedure Step 8 |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps well defined in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Equipment load values inconsistent between documents |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Review process defined in Procedure Step 8 |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Cost-effectiveness orientation clear across documents |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | OBJ-003 evaluation context consistently addressed |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-off table in Guidance provides adequate worth assessment |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal review checklist in Procedure covers quality |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of NBCC applies (e.g., NBCC 2020 or applicable Alberta-adopted edition); currently states "Designer to verify applicable edition" which leaves a prescriptive gap | The primary structural code edition is unresolved; this affects snow/wind/seismic load values that govern structural design. A prescriptive direction lens requires the governing code edition to be identified or explicitly flagged as TBD with resolution path. | Specification.md | Standards table, NBCC row | — | Structural Engineer | TBD |
| A-002 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for the post-disaster importance category exemption claim; currently stated as fact in Datasheet but no verification method exists in Specification to confirm AHJ has granted or will grant the exemption | Datasheet states "Not required; AHJ intends to exempt PSB from post-disaster designation" but no verification method confirms this with the AHJ. Compliance determination requires evidence or a confirmation step. | Datasheet.md; Specification.md | Datasheet: Attributes table "Post-disaster importance"; Specification: Verification section | — | PM / AHJ | TBD |
| A-003 | A:operative:judging | Normalization | Multi | Datasheet | Normalize fire apparatus GVW assumption: Datasheet C-002 states "25-40 tonnes (250-400 kN)" while Procedure Step 4 states "35-40 tonnes (350-400 kN)"; align to a single authoritative range | Two documents provide different lower-bound estimates for the same equipment type. This inconsistency could affect slab design load cases and the performance assessment of floor adequacy. | Guidance.md; Procedure.md | Guidance: C-002 Equipment Load Estimates; Procedure: Step 4 action item 1 | Guidance.md#C-002; Procedure.md#Step 4 | Structural Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Geotechnical values TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Appendix D inaccessible |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Cold Storage ventilation loads absent from Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key structural signals present in all documents |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts sufficiently comprehensive for proposal stage |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Cold Storage floor option numbering |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental structural concepts well communicated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise level appropriate for concept stage |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage appropriate for scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off reasoning present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls in Guidance adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic perspective maintained |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record specific geotechnical parameters (bearing capacity, groundwater level, frost depth) from Appendix D as essential facts; currently all marked TBD in both Datasheet and Procedure | Essential factual data for foundation design is identified as needed but not yet populated. The Appendix D report exists but has not been accessed. These are essential facts without which the foundation strategy cannot be confirmed. | Datasheet.md; Procedure.md | Datasheet: Conditions table "Geotechnical status"; Procedure: Step 2 parameter table | — | PM to retrieve Appendix D | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Strengthen Cold Storage "minimum height" reference: Datasheet states "clear span of usable interior space, minimum height" without specifying what the minimum height is; RFP OSR §10.2 and §10.3.5 should be checked for a stated height | The adequate evidence standard requires that stated dimensional requirements include their values. "Minimum height" is referenced but never quantified for the Cold Storage building. | Datasheet.md | Attributes table "Cold Storage footprint" | — | Structural Engineer / RFP review | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Cold Storage ventilation structural coordination note: Guidance C-004 identifies ventilation to prevent condensation/icing with structural implications (openings, louvers), but Datasheet has no corresponding condition or attribute entry | Guidance identifies a structural coordination need for Cold Storage ventilation (OSR §11.1.2) but the Datasheet does not record this as a condition or construction element, creating an incomplete data record. | Datasheet.md; Guidance.md | Datasheet: Conditions table (absent); Guidance: C-004 | — | Structural Engineer | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize Cold Storage floor option labeling: Datasheet labels them "Option 1" and "Option 2" matching RFP OSR §10.3.8; Guidance T-006 labels them "Option 1" and "Option 2" consistently, but Procedure Step 3.5 describes them without explicit option labels — add consistent labels in Procedure | Minor normalization: Procedure Step 3 item 5 describes the two Cold Storage floor approaches without using the "Option 1 / Option 2" labels that Datasheet and Guidance use, risking terminology drift. | Datasheet.md; Guidance.md; Procedure.md | Datasheet: Attributes "Floor slab -- Cold Storage"; Guidance: T-006; Procedure: Step 3 item 5 | — | Structural Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable obligation | 1 | HAS_ITEMS | Seismic classification missing |
| C:normative:sufficiency | normative | sufficiency | mandated substantiation | 0 | NO_ITEMS | Substantiation approach adequate for proposal stage |
| C:normative:completeness | normative | completeness | total regulatory coverage | 0 | NO_ITEMS | Regulatory coverage comprehensive for identified codes |
| C:normative:consistency | normative | consistency | codified enforcement | 0 | NO_ITEMS | Enforcement references consistent |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites well defined in Procedure |
| C:operative:sufficiency | operative | sufficiency | demonstrated capability | 0 | NO_ITEMS | Capability demonstration adequate |
| C:operative:completeness | operative | completeness | exhaustive operational scope | 1 | HAS_ITEMS | Second-storey structural impact incomplete |
| C:operative:consistency | operative | consistency | process coherence | 0 | NO_ITEMS | Process steps coherent |
| C:evaluative:necessity | evaluative | necessity | inherent value criterion | 0 | NO_ITEMS | Value criteria well established |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible valuation | 0 | NO_ITEMS | Valuation defensible |
| C:evaluative:completeness | evaluative | completeness | holistic value accounting | 0 | NO_ITEMS | Value accounting adequate |
| C:evaluative:consistency | evaluative | consistency | anchored value standard | 0 | NO_ITEMS | Value standards anchored |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement addressing seismic design classification for Penhold, Alberta; SR-015 covers snow, lateral, and wind loads but does not explicitly mention seismic loads or site classification even though NBCC applies and Penhold is in a low-seismic zone | Under the enforceable obligation lens, the NBCC requires seismic design consideration for all structures. The Specification addresses snow, wind, and lateral loads but does not explicitly call out seismic classification. While Penhold is low-seismic, the obligation to address it exists under NBCC. | Specification.md | Requirements table SR-015; Standards table | — | Structural Engineer | TBD |
| C-002 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing second-storey structural load path if architectural concept includes upper level; Guidance C-008 identifies this as a non-trivial structural consideration but no SR requirement captures it | Guidance C-008 identifies that a second storey adds "inter-storey shear frame requirements and floor loads" and "must not be assumed trivial." However, no Specification requirement exists to ensure the structural narrative addresses this if the architectural concept includes it. This creates an operational completeness gap. | Specification.md; Guidance.md | Specification: Requirements table (absent); Guidance: C-008 | — | Structural Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | absolute compliance mandate | 0 | NO_ITEMS | Compliance mandates adequately captured |
| F:normative:sufficiency | normative | sufficiency | warranted regulatory authority | 0 | NO_ITEMS | Regulatory authority references sufficient |
| F:normative:completeness | normative | completeness | integral compliance architecture | 1 | HAS_ITEMS | ABC relationship to NBCC unclear |
| F:normative:consistency | normative | consistency | coherent conformance framework | 0 | NO_ITEMS | Framework coherent |
| F:operative:necessity | operative | necessity | critical process foundation | 0 | NO_ITEMS | Process foundations established |
| F:operative:sufficiency | operative | sufficiency | proven operational readiness | 0 | NO_ITEMS | Readiness adequately addressed |
| F:operative:completeness | operative | completeness | total execution authority | 0 | NO_ITEMS | Execution scope complete for proposal stage |
| F:operative:consistency | operative | consistency | systematic process alignment | 0 | NO_ITEMS | Process alignment systematic |
| F:evaluative:necessity | evaluative | necessity | foundational merit imperative | 1 | HAS_ITEMS | Evaluation scoring not mapped to SRs |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated merit judgment | 0 | NO_ITEMS | Merit substantiation adequate |
| F:evaluative:completeness | evaluative | completeness | unified value mastery | 0 | NO_ITEMS | Value coverage unified |
| F:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Value coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:completeness | RationaleGap | Guidance | Guidance | Clarify the relationship between NBCC and Alberta Building Code (ABC) for this project; Specification lists both but does not explain which governs structural design vs. building permit/occupancy; Guidance should explain their complementary roles | The integral compliance architecture lens asks whether the full regulatory framework is coherently structured. The Specification lists NBCC and ABC as separate standards but their hierarchical relationship (NBCC for structural design, ABC for permitting) is not explained. This could cause confusion about which standard governs which aspect. | Specification.md | Standards table, NBCC and ABC rows | — | Structural Engineer | TBD |
| F-002 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add guidance note explaining how individual structural narrative sections map to the OBJ-003 evaluation criteria; the evaluation context is stated (20 pts for conceptual design) but no guidance explains what evaluators prioritize in structural content | The foundational merit imperative lens asks whether the basis for value assessment is grounded. While the Purpose section mentions OBJ-003, there is no guidance on what structural content elements are likely to score highest with the evaluation committee. This gap means the narrative author has no evaluator-perspective signal. | Guidance.md | Purpose section | — | Design Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive regulatory mandate | 0 | NO_ITEMS | Regulatory mandates clearly guided |
| D:normative:applying | normative | applying | authorized enforcement | 0 | NO_ITEMS | Enforcement authority clear |
| D:normative:judging | normative | judging | settled conformance verdict | 0 | NO_ITEMS | Conformance criteria stated |
| D:normative:reviewing | normative | reviewing | conclusive compliance review | 0 | NO_ITEMS | Review process defined |
| D:operative:guiding | operative | guiding | anchored operational guidance | 1 | HAS_ITEMS | Appendix B not explicitly listed as input |
| D:operative:applying | operative | applying | validated implementation | 0 | NO_ITEMS | Implementation approach validated |
| D:operative:judging | operative | judging | definitive performance verdict | 0 | NO_ITEMS | Performance criteria adequate |
| D:operative:reviewing | operative | reviewing | resolved process integrity | 0 | NO_ITEMS | Process integrity maintained |
| D:evaluative:guiding | evaluative | guiding | grounded value purpose | 0 | NO_ITEMS | Value purpose well grounded |
| D:evaluative:applying | evaluative | applying | enacted merit deployment | 0 | NO_ITEMS | Merit deployment clear |
| D:evaluative:judging | evaluative | judging | conclusive merit verdict | 1 | HAS_ITEMS | Trade-off T-006 lacks verdict |
| D:evaluative:reviewing | evaluative | reviewing | resolved quality assurance | 0 | NO_ITEMS | QA approach adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add RFP Appendix B (Functional Program) to the _REFERENCES.md cross-references; Procedure lists it as a required prerequisite but it is absent from _REFERENCES.md | Anchored operational guidance requires that all prerequisite documents are traceable. The Procedure identifies "RFP Appendix B -- Functional Program" as a required input, but _REFERENCES.md does not list it, creating a gap in the operational reference chain. | Procedure.md; _REFERENCES.md | Procedure: Prerequisites table; _REFERENCES.md: entire document scanned | — | Structural Engineer | TBD |
| D-002 | D:evaluative:judging | WeakStatement | Guidance | Guidance | Strengthen Trade-off T-006 (Cold Storage floor) recommendation: currently states both options and notes Option 2 is more durable and Option 1 is lower cost, but does not state a clear recommendation or decision criterion for selecting between them | The conclusive merit verdict lens asks whether evaluative judgments reach decisive conclusions. T-006 presents both Cold Storage floor options without a recommendation tied to the design philosophy (OSR §10.3.4 "practical, cost effective, easy to maintain"). A clear recommended starting position would strengthen the narrative. | Guidance.md | Trade-offs table T-006 | — | Structural Engineer / PM | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational governance charter | 0 | NO_ITEMS | Governance framework adequate |
| X:guiding:sufficiency | guiding | sufficiency | warranted directive proof | 0 | NO_ITEMS | Directive proof adequate |
| X:guiding:completeness | guiding | completeness | exhaustive governance direction | 0 | NO_ITEMS | Direction comprehensive |
| X:guiding:consistency | guiding | consistency | unified directional coherence | 0 | NO_ITEMS | Direction coherent |
| X:applying:necessity | applying | necessity | imperative enactment readiness | 1 | HAS_ITEMS | Verification responsibility gap |
| X:applying:sufficiency | applying | sufficiency | validated deployment warrant | 0 | NO_ITEMS | Deployment validation adequate |
| X:applying:completeness | applying | completeness | comprehensive implementation scope | 1 | HAS_ITEMS | Verification missing for standards compliance |
| X:applying:consistency | applying | consistency | consistent authorized practice | 0 | NO_ITEMS | Practice consistency maintained |
| X:judging:necessity | judging | necessity | imperative adjudication standard | 0 | NO_ITEMS | Adjudication standards defined |
| X:judging:sufficiency | judging | sufficiency | validated sufficiency finding | 0 | NO_ITEMS | Sufficiency findings adequate |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 0 | NO_ITEMS | Adjudication scope adequate |
| X:judging:consistency | judging | consistency | aligned adjudication integrity | 0 | NO_ITEMS | Adjudication integrity aligned |
| X:reviewing:necessity | reviewing | necessity | mandatory oversight verification | 1 | HAS_ITEMS | No verification for CCDC 14-2013 design responsibility |
| X:reviewing:sufficiency | reviewing | sufficiency | warranted review adequacy | 0 | NO_ITEMS | Review adequacy acceptable |
| X:reviewing:completeness | reviewing | completeness | integral oversight examination | 0 | NO_ITEMS | Oversight examination integral |
| X:reviewing:consistency | reviewing | consistency | unified oversight coherence | 0 | NO_ITEMS | Oversight coherence unified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification row for SR-012 (cost-effectiveness rationale) that specifies what constitutes adequate cost-effectiveness justification; current verification states "Narrative includes explicit cost-value justification" without defining what makes it adequate | Imperative enactment readiness requires verification criteria to be specific enough to act on. The acceptance criterion for SR-012 is circular ("includes explicit cost-value justification") and does not define what evidence or comparison constitutes adequate justification. | Specification.md | Verification table, SR-012 row | — | Design Manager | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification approach for Standards compliance (NBCC, ABC, CSA S16, CSA A23.3); Standards are listed in the Specification but no verification row confirms the narrative addresses applicable code requirements | The comprehensive implementation scope lens asks whether all specified elements have verification. Standards are listed (NBCC, ABC, CSA S16, CSA A23.3) but no verification row addresses whether the narrative correctly references or applies these standards. | Specification.md | Standards table; Verification section | — | Structural Engineer | TBD |
| X-003 | X:reviewing:necessity | TBD_Question | Specification | Guidance | Clarify how CCDC 14-2013 Design-Builder performance risk obligation is verified at concept stage; Guidance C-006 states the narrative "should reflect this responsibility" but no verification method confirms it has been adequately communicated | Mandatory oversight verification requires that contractual obligations have a verification path. The CCDC 14-2013 performance risk allocation is identified in both Specification (Standards) and Guidance (C-006), but no mechanism verifies that the narrative adequately reflects the Design-Builder's structural design responsibility. | Specification.md; Guidance.md | Specification: Standards table CCDC 14-2013 row; Guidance: C-006 | — | PM / Design Manager | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | sovereign compliance authority | 0 | NO_ITEMS | Compliance authority adequately established |
| E:normative:sufficiency | normative | sufficiency | substantiated regulatory fitness | 0 | NO_ITEMS | Regulatory fitness substantiated |
| E:normative:completeness | normative | completeness | total regulatory jurisdiction | 0 | NO_ITEMS | Jurisdiction scope adequate |
| E:normative:consistency | normative | consistency | harmonized regulatory protocol | 0 | NO_ITEMS | Protocol harmonized |
| E:operative:necessity | operative | necessity | critical operational mandate | 0 | NO_ITEMS | Operational mandates clear |
| E:operative:sufficiency | operative | sufficiency | demonstrated operational fitness | 1 | HAS_ITEMS | Corrosion protection spec weak |
| E:operative:completeness | operative | completeness | complete operational fulfillment | 0 | NO_ITEMS | Operational fulfillment adequate for scope |
| E:operative:consistency | operative | consistency | unified operational reliability | 0 | NO_ITEMS | Operational reliability unified |
| E:evaluative:necessity | evaluative | necessity | fundamental quality imperative | 0 | NO_ITEMS | Quality imperatives grounded |
| E:evaluative:sufficiency | evaluative | sufficiency | demonstrated value adequacy | 1 | HAS_ITEMS | Conflicting slab thickness |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality fulfillment | 0 | NO_ITEMS | Quality fulfillment adequate |
| E:evaluative:consistency | evaluative | consistency | principled quality integrity | 0 | NO_ITEMS | Quality integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:sufficiency | Normalization | Datasheet | Datasheet | Align corrosion protection description: Datasheet states "TBD specification details (aligned with DEL-05-02)" while Guidance P-005 provides a specific example phrase and EX-004 specifies "standard protective coatings"; normalize to a consistent level of specificity across documents | Demonstrated operational fitness requires consistent articulation of protective measures. The Datasheet construction table uses "TBD specification details" for corrosion protection while Guidance examples provide more specific language. The inconsistency could produce a narrative that either over-commits or under-commits relative to what was intended. | Datasheet.md; Guidance.md | Datasheet: Construction table "Corrosion protection"; Guidance: P-005, EX-004 | Datasheet.md#Construction; Guidance.md#P-005 | Structural Engineer | TBD |
| E-002 | E:evaluative:sufficiency | Conflict | Procedure | Procedure | Resolve conflicting concrete apron thickness: Procedure Step 3.6 states "ASSUMPTION minimum 200 mm (8") concrete" for aprons, while Procedure Step 3.5 states apparatus bay slab "minimum 150 mm (6") thickness"; clarify whether the 200 mm apron assumption is based on different loading or is an error relative to the bay slab thickness | Demonstrated value adequacy requires that stated dimensional assumptions are internally consistent and justified. Both values appear in the same Procedure document. The apron is stated as 200 mm while the bay slab (which also supports heavy vehicles) is 150 mm. The difference may be intentional (aprons see more concentrated loads) but the rationale is not stated. | Procedure.md | Step 3 items 5 and 6 | Procedure.md#Step-3 item 5; Procedure.md#Step-3 item 6 | Structural Engineer | TBD |
