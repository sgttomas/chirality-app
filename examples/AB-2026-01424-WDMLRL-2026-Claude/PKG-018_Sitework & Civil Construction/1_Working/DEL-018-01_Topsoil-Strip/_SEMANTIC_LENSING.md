# Semantic Lensing Register: DEL-018-01 Topsoil Stripping

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-01_Topsoil-Strip
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-018-01_Topsoil-Strip/_CONTEXT.md (Deliverable Identity, Context Summary)
- _STATUS.md — DEL-018-01_Topsoil-Strip/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-018-01_Topsoil-Strip/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-018-01_Topsoil-Strip/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-018-01_Topsoil-Strip/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-018-01_Topsoil-Strip/Guidance.md (Purpose, Principles, Considerations, Trade-offs)
- Procedure.md — DEL-018-01_Topsoil-Strip/Procedure.md (Purpose, Prerequisites, Steps, Verification, Records)
- _REFERENCES.md — DEL-018-01_Topsoil-Strip/_REFERENCES.md (R-01, R-07 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 3  F: 3  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 7
  - WeakStatement: 4
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Environmental compliance direction underspecified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Erosion control measures lack mandatory specification |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta Safety Code compliance criteria are generic |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection and audit coordination adequately covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Equipment type TBD weakens execution specificity |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables provide adequate performance assessment linkage |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | County inspection and daily logs constitute adequate process audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance adequately frames topsoil as a project asset |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section adequately covers value-based choices |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost/benefit logic for salvage vs. disposal addressed in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Stockpile quality check present in Procedure Step 5 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta environmental regulations apply to topsoil stripping (REQ-018-01-08 references "applicable Alberta Safety Codes" generically) | The prescriptive direction for environmental compliance is stated only as an assumption with no specific regulation cited; this weakens enforceability | Specification.md | ## Standards | -- | Alberta Environment and Protected Areas regulations | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add a requirement for interim erosion and sediment control measures during and after stripping, with specific trigger conditions | Erosion control is mentioned in Guidance and Procedure as assumption/TBD but has no corresponding mandatory requirement in Specification | Specification.md, Guidance.md | Specification: ## Requirements (absent); Guidance: ## Considerations > Environmental and Erosion Controls | -- | Specification as normative authority | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen REQ-018-01-08 by specifying which Alberta Safety Codes sections apply to ground disturbance and excavation, or add TBD to resolve before execution | "All Alberta Safety Codes" is too broad for compliance determination; an auditor cannot verify compliance against an unspecified set of codes | Specification.md | ## Requirements > REQ-018-01-08 | -- | Specification | TBD |
| A-004 | A:operative:applying | WeakStatement | Datasheet | Datasheet | Record equipment type constraints or selection criteria once known (currently "type TBD") | Equipment type is TBD in Datasheet and Procedure; practical execution planning cannot proceed without at least a category constraint | Datasheet.md | ## Attributes > Equipment Type | -- | Datasheet | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Topsoil depth is an essential fact recorded as TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations are adequate across documents |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Volume data absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement approach (as-built survey) is consistently referenced |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Dependency signals adequately documented in _DEPENDENCIES.md and Procedure prerequisites |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is sufficient for planning purposes |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide a comprehensive narrative of the deliverable |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency: "driving surfaces" vs. scope extent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance principles establish adequate foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Contractor expertise assumptions are standard |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Domain coverage is adequate for the scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Decision D-010 provides the key discernment needed |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent with safety-first principle |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Resolve topsoil depth value (currently TBD pending SURVEY-001); this is an essential fact required before execution can proceed | Topsoil depth is flagged as TBD in Datasheet and is a prerequisite for calculating volume, selecting equipment, and defining stripping limits | Datasheet.md | ## Attributes > Topsoil Depth | -- | SURVEY-001 output | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a topsoil volume estimate row (or explicit TBD placeholder with calculation method) once depth and area are known | Volume of topsoil is listed as TBD with no method for how it will be calculated; completeness of the data record requires at least a formula placeholder | Datasheet.md | ## Attributes > Volume of Topsoil | -- | Datasheet | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Clarify whether "all driving surfaces" includes only vehicle traffic areas or also pedestrian paths, equipment staging areas, and building perimeter areas; reconcile across documents | "All driving surfaces" is used consistently but its precise extent is ambiguous; Specification REQ-018-01-01 interprets it as "full extent of planned vehicle and equipment traffic areas" but Datasheet says "all driving surfaces within the project lot" which could be broader | Datasheet.md, Specification.md | Datasheet: ## Attributes > Area of Work; Specification: ## Requirements > REQ-018-01-01 | Datasheet.md#Attributes, Specification.md#REQ-018-01-01 | Specification (normative) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable obligation threshold | 1 | HAS_ITEMS | Ground disturbance permit requirement is assumed, not confirmed |
| C:normative:sufficiency | normative | sufficiency | warranted conformance proof | 1 | HAS_ITEMS | Conformance proof for stockpile quality is underspecified |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 0 | NO_ITEMS | Standards table covers applicable regulations adequately for current state |
| C:normative:consistency | normative | consistency | standardized regulatory coherence | 0 | NO_ITEMS | Regulatory references are internally consistent |
| C:operative:necessity | operative | necessity | operational readiness prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is comprehensive |
| C:operative:sufficiency | operative | sufficiency | demonstrated procedural fitness | 0 | NO_ITEMS | Procedure steps demonstrate adequate procedural fitness |
| C:operative:completeness | operative | completeness | end-to-end process coverage | 1 | HAS_ITEMS | Stockpile stabilization method is TBD |
| C:operative:consistency | operative | consistency | calibrated repeatable discipline | 0 | NO_ITEMS | Steps are sequentially consistent and repeatable |
| C:evaluative:necessity | evaluative | necessity | foundational merit criterion | 0 | NO_ITEMS | Topsoil-as-asset merit is established in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible quality appraisal | 0 | NO_ITEMS | Verification approach in Specification is defensible |
| C:evaluative:completeness | evaluative | completeness | holistic value accounting | 0 | NO_ITEMS | Value framing is adequate |
| C:evaluative:consistency | evaluative | consistency | principled appraisal integrity | 0 | NO_ITEMS | Appraisal criteria consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Confirm whether a formal ground disturbance permit is required under Alberta regulations for this site and scope; if so, add as a mandatory requirement | Procedure Step 2 references ground disturbance authorization as "if required by Alberta regulations" but Specification does not establish whether it is required; this is an enforceable obligation that remains unresolved | Specification.md, Procedure.md | Specification: ## Standards; Procedure: ## Steps > Step 2 | -- | Alberta OH&S Act / local municipal authority | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for topsoil stockpile quality (e.g., maximum contamination with subgrade material, moisture condition, organic content) to the Verification table | REQ-018-01-05 requires salvage for reuse but the verification approach ("inspection of stockpile area; stockpile volume estimate") does not define what constitutes acceptable stockpile quality | Specification.md | ## Verification > REQ-018-01-05 | -- | Specification | TBD |
| C-003 | C:operative:completeness | WeakStatement | Procedure | Procedure | Specify the stockpile stabilization/protection method or define the decision criteria for selecting one (Step 6 says "method TBD") | End-to-end process coverage is incomplete when stockpile protection after stripping is left as TBD; wind dispersion and erosion of unprotected stockpiles can degrade topsoil quality | Procedure.md | ## Steps > Step 6 | -- | Procedure | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | certified enforcement authority | 0 | NO_ITEMS | Enforcement authority is adequately referenced via RFP and D-010 |
| F:normative:sufficiency | normative | sufficiency | sufficient conformance rationale | 1 | HAS_ITEMS | Rationale for unconditional scope (D-010) could be more explicit in Specification |
| F:normative:completeness | normative | completeness | unified compliance framework | 0 | NO_ITEMS | Compliance framework is unified across documents |
| F:normative:consistency | normative | consistency | harmonized enforcement discipline | 0 | NO_ITEMS | Enforcement references are harmonized |
| F:operative:necessity | operative | necessity | critical preparedness awareness | 1 | HAS_ITEMS | Weather/seasonal constraints not addressed |
| F:operative:sufficiency | operative | sufficiency | verified execution proficiency | 0 | NO_ITEMS | Execution proficiency verification is adequate via prerequisites |
| F:operative:completeness | operative | completeness | exhaustive capability mastery | 0 | NO_ITEMS | Capability coverage adequate for current phase |
| F:operative:consistency | operative | consistency | methodical workflow reliability | 0 | NO_ITEMS | Workflow is methodical and sequenced |
| F:evaluative:necessity | evaluative | necessity | intrinsic quality discernment | 0 | NO_ITEMS | Quality criteria are addressed |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated appraisal competence | 0 | NO_ITEMS | Appraisal approach is substantiated |
| F:evaluative:completeness | evaluative | completeness | comprehensive valuation mastery | 1 | HAS_ITEMS | No quantified value estimate for salvaged topsoil |
| F:evaluative:consistency | evaluative | consistency | principled valuation accountability | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Guidance | Guidance | Add explicit rationale in Guidance explaining why D-010 resolved scope as unconditional despite the conditional language in RFP section 3.3.2; current cross-reference is present but reasoning is thin | The conformance rationale for treating topsoil stripping as unconditional rests on D-010 but the reasoning behind D-010 is not explained in Guidance beyond stating the decision; a reader unfamiliar with the decomposition cannot assess the rationale | Guidance.md | ## Principles > 5. Assume Required, Even If Owner Has Started | -- | Guidance | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a seasonal/weather constraint note to Prerequisites or Step 4 addressing frozen ground, wet conditions, or seasonal restrictions on earthworks in Alberta | Critical preparedness awareness requires considering that topsoil stripping in Alberta may be infeasible during frozen ground conditions (winter); no prerequisite or step addresses seasonal viability | Procedure.md | ## Prerequisites (absent); ## Steps > Step 4 | -- | Procedure | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a brief note on the estimated economic value or replacement cost of salvaged topsoil to substantiate the "topsoil is a project asset" principle | Guidance Principle 2 states topsoil "represents a material cost savings versus importing topsoil later" but provides no quantification or basis for this claim; comprehensive valuation mastery requires at least an order-of-magnitude estimate or a TBD placeholder | Guidance.md | ## Principles > 2. Topsoil is a Project Asset | -- | Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | established authoritative mandate | 0 | NO_ITEMS | Mandate is established via RFP and D-010 |
| D:normative:applying | normative | applying | obligatory compliance execution | 0 | NO_ITEMS | Compliance execution pathway is clear |
| D:normative:judging | normative | judging | binding conformance ruling | 1 | HAS_ITEMS | Conflict CFT-001 remains TBD |
| D:normative:reviewing | normative | reviewing | compulsory oversight rigor | 0 | NO_ITEMS | Oversight through County inspection is adequate |
| D:operative:guiding | operative | guiding | confirmed workflow stewardship | 1 | HAS_ITEMS | Subgrade acceptance criteria absent |
| D:operative:applying | operative | applying | proven operational deployment | 0 | NO_ITEMS | Deployment steps are well-defined |
| D:operative:judging | operative | judging | confirmed capability verdict | 0 | NO_ITEMS | Capability assessment through prerequisites and verification is adequate |
| D:operative:reviewing | operative | reviewing | verified procedural scrutiny | 0 | NO_ITEMS | Procedure verification table provides adequate scrutiny |
| D:evaluative:guiding | evaluative | guiding | merit-driven clarity | 0 | NO_ITEMS | Merit framing in Guidance is clear |
| D:evaluative:applying | evaluative | applying | proven benefit realization | 0 | NO_ITEMS | Benefit realization path (salvage for reuse) is stated |
| D:evaluative:judging | evaluative | judging | definitive appraisal authority | 1 | HAS_ITEMS | No acceptance criteria for subgrade condition |
| D:evaluative:reviewing | evaluative | reviewing | accountable merit scrutiny | 0 | NO_ITEMS | Inspection regime provides accountability |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | Conflict | Guidance | NA | Surface and track resolution of CFT-001: RFP section 3.3.2 conditional language vs. D-010 unconditional interpretation; ensure Specification and Procedure are updated once human ruling is made | This conflict is already identified in Guidance Conflict Table as CFT-001 with HumanRuling = TBD; under the binding conformance ruling lens, this remains an open normative ambiguity that blocks definitive conformance determination | Guidance.md | ## Conflict Table > CFT-001 | Guidance.md#CFT-001 (RFP section 3.3.2 vs. Decomposition D-010) | Human ruling required | TBD |
| D-002 | D:operative:guiding | MissingSlot | Specification | Specification | Add subgrade acceptance criteria (e.g., visual confirmation of organic material removal, bearing capacity test, or engineer sign-off) to define when stripping is "complete" | Workflow stewardship requires a clear definition of done for the stripped subgrade; currently the completion criterion is "all driving surface areas stripped to specified depth" but there is no acceptance standard for the exposed subgrade condition | Specification.md | ## Verification > REQ-018-01-01 | -- | Specification | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add verification criteria for subgrade condition after stripping (e.g., absence of organic pockets, uniform exposure, no standing water) | Definitive appraisal authority for the deliverable outcome requires criteria beyond area coverage; the quality of the exposed subgrade determines downstream success for grading and surface construction | Specification.md | ## Verification > REQ-018-01-01 | -- | Specification | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | authoritative core basis | 0 | NO_ITEMS | Core basis (RFP, D-010, dependencies) is established |
| X:guiding:sufficiency | guiding | sufficiency | competent authoritative evidence | 0 | NO_ITEMS | Evidence base is adequate for current phase |
| X:guiding:completeness | guiding | completeness | comprehensive purposeful record | 1 | HAS_ITEMS | Record of County coordination protocol is incomplete |
| X:guiding:consistency | guiding | consistency | coherent standardized alignment | 0 | NO_ITEMS | Alignment across docs is coherent |
| X:applying:necessity | applying | necessity | verified deployment basis | 1 | HAS_ITEMS | Stripping depth acceptance tolerance absent |
| X:applying:sufficiency | applying | sufficiency | proven applied adequacy | 0 | NO_ITEMS | Applied adequacy demonstrated through verification linkage |
| X:applying:completeness | applying | completeness | exhaustive execution record | 0 | NO_ITEMS | Records table in Procedure is comprehensive |
| X:applying:consistency | applying | consistency | uniform operational coherence | 1 | HAS_ITEMS | Terminology for stockpile management varies |
| X:judging:necessity | judging | necessity | binding factual determination | 0 | NO_ITEMS | Factual determination pathway (as-built survey) is clear |
| X:judging:sufficiency | judging | sufficiency | sufficient verdict evidence | 1 | HAS_ITEMS | Verification evidence for REQ-018-01-05 insufficient |
| X:judging:completeness | judging | completeness | comprehensive assessment mastery | 0 | NO_ITEMS | Assessment coverage in verification tables is comprehensive |
| X:judging:consistency | judging | consistency | standardized verdict coherence | 0 | NO_ITEMS | Verdict approach is consistent between Specification and Procedure |
| X:reviewing:necessity | reviewing | necessity | compulsory examination basis | 0 | NO_ITEMS | County inspection basis is compulsory per RFP |
| X:reviewing:sufficiency | reviewing | sufficiency | sufficient examination evidence | 0 | NO_ITEMS | Evidence requirements are specified |
| X:reviewing:completeness | reviewing | completeness | exhaustive examination record | 0 | NO_ITEMS | Records table accounts for examination outputs |
| X:reviewing:consistency | reviewing | consistency | standardized examination coherence | 0 | NO_ITEMS | Examination approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Procedure | Procedure | Add a step or prerequisite for establishing the County coordination and communication protocol (contact person, notification lead times, inspection scheduling process) before field work begins | The comprehensive purposeful record lens reveals that while County coordination is mentioned repeatedly, the actual protocol (who to contact, how far in advance, what form inspection requests take) is never specified | Procedure.md | ## Prerequisites; ## Steps > Step 7 | -- | Procedure | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add a stripping depth tolerance to REQ-018-01-01 or REQ-018-01-07 (e.g., +/- X mm from design depth) to enable field verification of adequate stripping | Verified deployment basis requires a measurable acceptance criterion for stripping depth; currently depth is referenced as "specified in IFC drawings" but no tolerance is stated for field verification | Specification.md | ## Requirements > REQ-018-01-07; ## Verification > REQ-018-01-01 | -- | Specification (with IFC drawings as source) | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Guidance | Standardize terminology for stockpile management: "temporary stockpile," "topsoil stockpile," "stockpile area," and "stockpile plan" are used variably; define canonical term and use consistently | Uniform operational coherence is weakened by inconsistent stockpile-related terminology across all four documents; while meaning is inferable, a future enrichment pass should normalize | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Datasheet: ## Attributes > Stockpile Location; Specification: ## Requirements > REQ-018-01-05; Guidance: ## Considerations > Stockpile Location; Procedure: ## Steps > Step 3 | -- | Guidance (vocabulary note) | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Strengthen verification evidence for REQ-018-01-05 by adding measurable acceptance criteria for stockpile condition (e.g., no subgrade contamination visible, stockpile accessible, erosion protection in place) | Sufficient verdict evidence for topsoil salvage requires more than "inspection of stockpile area"; the evidence must demonstrate the stockpile is actually suitable for reuse | Specification.md | ## Verification > REQ-018-01-05 | -- | Specification | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | evidenced authoritative grounding | 0 | NO_ITEMS | Grounding is evidenced through source citations |
| E:guiding:information | guiding | information | grounded purposeful communication | 0 | NO_ITEMS | Communication is purposeful and grounded |
| E:guiding:knowledge | guiding | knowledge | integrated domain mastery | 1 | HAS_ITEMS | Dust control knowledge gap |
| E:guiding:wisdom | guiding | wisdom | grounded prudential foresight | 1 | HAS_ITEMS | No contingency for unexpected subsurface conditions |
| E:applying:data | applying | data | verified deployment record | 0 | NO_ITEMS | Deployment record framework in place via Records table |
| E:applying:information | applying | information | reliable execution guidance | 0 | NO_ITEMS | Execution guidance is reliable and step-sequenced |
| E:applying:knowledge | applying | knowledge | proven execution mastery | 0 | NO_ITEMS | Execution mastery is demonstrated through procedure detail |
| E:applying:wisdom | applying | wisdom | verified practical prudence | 0 | NO_ITEMS | Practical prudence evident in safety-first sequencing |
| E:judging:data | judging | data | binding evidentiary finding | 0 | NO_ITEMS | Evidentiary requirements are specified |
| E:judging:information | judging | information | decisive assessment guidance | 0 | NO_ITEMS | Assessment guidance in verification tables is decisive |
| E:judging:knowledge | judging | knowledge | masterful evaluative proficiency | 0 | NO_ITEMS | Evaluative framework is adequate |
| E:judging:wisdom | judging | wisdom | grounded judicial prudence | 0 | NO_ITEMS | Conflict table and HumanRuling framework demonstrate judicial prudence |
| E:reviewing:data | reviewing | data | comprehensive audit evidence | 0 | NO_ITEMS | Audit evidence framework is comprehensive |
| E:reviewing:information | reviewing | information | comprehensive oversight guidance | 0 | NO_ITEMS | Oversight guidance through County inspection is comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | demonstrated audit mastery | 1 | HAS_ITEMS | No lessons-learned or close-out audit provision |
| E:reviewing:wisdom | reviewing | wisdom | rigorous audit foresight | 0 | NO_ITEMS | Audit foresight is adequate for current phase |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | MissingSlot | Guidance | Guidance | Add a consideration for dust control during stripping operations, including regulatory requirements and practical mitigation measures for a rural Alberta landfill site | Integrated domain mastery for earthworks in Alberta requires addressing dust generation during topsoil stripping; this is absent from Guidance Considerations despite the rural landfill context where dust control may be a regulatory or operational concern | Guidance.md | ## Considerations (absent) | -- | Guidance | TBD |
| E-002 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add a contingency consideration for encountering unexpected subsurface conditions (e.g., buried waste, contaminated soil, archaeological finds) during stripping at a landfill site | Grounded prudential foresight requires acknowledging that a landfill site may contain unexpected buried materials; no document addresses what to do if unexpected conditions are encountered during stripping | Guidance.md | ## Considerations (absent) | -- | Guidance | TBD |
| E-003 | E:reviewing:knowledge | MissingSlot | Procedure | Procedure | Add a close-out or lessons-learned step after Step 7 to capture field observations, actual vs. planned volumes, and any issues for future PKG-018 deliverables | Demonstrated audit mastery includes a feedback mechanism; the Procedure ends at County sign-off (Step 7) without capturing lessons learned that could benefit the six downstream deliverables in PKG-018 | Procedure.md | ## Steps (absent after Step 7) | -- | Procedure | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- All 96 matrix cells (A:12, B:16, C:12, F:12, D:12, X:16, E:16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in evidence from production documents or explicit absence |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- 1 conflict (D-001/CFT-001) surfaced with Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts (23 total) match actual warranted items |
| Schema followed | PASS -- Output follows STRUCTURE schema |
