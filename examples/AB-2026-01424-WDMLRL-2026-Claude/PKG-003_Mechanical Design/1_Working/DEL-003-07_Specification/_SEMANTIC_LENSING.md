# Semantic Lensing Register: DEL-003-07 Mechanical Specification

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-003_Mechanical Design/1_Working/DEL-003-07_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-07_Specification/_CONTEXT.md
- _STATUS.md — DEL-003-07_Specification/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-07_Specification/_SEMANTIC.md
- Datasheet.md — DEL-003-07_Specification/Datasheet.md
- Specification.md — DEL-003-07_Specification/Specification.md
- Guidance.md — DEL-003-07_Specification/Guidance.md
- Procedure.md — DEL-003-07_Specification/Procedure.md
- _REFERENCES.md — DEL-003-07_Specification/_REFERENCES.md (present; pointers listed, scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 14
  - Guidance: 5
  - Procedure: 2
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 4  F: 5  D: 3  X: 5  E: 3
- By type:
  - Conflict: 3
  - VerificationGap: 6
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards list contains many ASSUMPTION labels lacking confirmed code editions |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Wash bay ventilation/exhaust not explicitly required in Specification |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Service pit code classification unresolved |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No acceptance criteria for Safety Code inspection outcomes |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are clear and sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps in Procedure are actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative performance thresholds in Specification for heating or ventilation |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table covers audit points |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-3 and P-4 articulate design-build value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Lifecycle cost analysis referenced in Guidance C-1 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure verification table covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify each ASSUMPTION-tagged standard in the Standards table with confirmed code edition or record as explicit TBD requiring engineer resolution | Five of seven entries in the Standards table are marked ASSUMPTION with "edition TBD" or "location TBD," making prescriptive direction materially ambiguous for code compliance | Specification.md | Standards | -- | Mechanical Engineer to confirm applicable code editions | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add a requirement for wash bay exhaust ventilation (humidity and condensation control) as a mandatory mechanical practice | Guidance C-6 identifies wash bay humidity/freeze protection as a design consideration, but no corresponding REQ-M entry exists in the Specification; the lens reveals a missing mandatory practice | Specification.md; Guidance.md | Specification#Requirements; Guidance#C-6 | -- | Mechanical Engineer | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Guidance | Record TBD: Confirm whether the service pit qualifies as a "repair garage" under Alberta Safety Codes and what ventilation rate applies | Guidance C-4 raises this as an open question; no compliance determination can be made without this classification, yet neither Specification nor Guidance resolves it | Specification.md; Guidance.md | Specification#REQ-M-006; Guidance#C-4 | -- | AHJ / Mechanical Engineer to determine code classification | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Specification | Specification | Add acceptance criteria defining what constitutes successful Safety Code inspection outcome (e.g., "no outstanding deficiencies") in the Verification table | Specification REQ-M-008 requires Safety Code compliance and permits; the Verification table references "Safety Code Permits obtained; inspection reports provided" but does not define acceptance criteria for passing inspection | Specification.md | Verification | -- | PROPOSAL: Specification | TBD |
| A-005 | A:operative:judging | WeakStatement | Specification | Specification | Add quantitative performance thresholds (heating capacity, ventilation rates, capture velocities) as placeholders in requirements REQ-M-001 through REQ-M-006, marked TBD pending DEL-003-06 | All performance requirements use qualitative language ("high-recovery," "high-volume," "adequate capture") without numeric thresholds; performance assessment is not possible without measurable criteria | Specification.md | Requirements (REQ-M-001 through REQ-M-006) | -- | Mechanical Engineer via DEL-003-06 | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Design outdoor temperature not recorded |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet source citations are traceable to RFP |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Mechanical controls not enumerated in Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (SOW, OBJ references) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for current stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document scope sections are comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for exhaust fan scope |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental engineering principles referenced |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. expertise requirement stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Appropriate for specification stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Design-build latitude principle articulated |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table provides judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers system-level interactions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with design-build principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add Alberta design outdoor temperature (heating design day) as an essential fact in the Conditions table | Heating load calculations (DEL-003-06) require a design outdoor temperature; this essential fact is absent from the Datasheet even though it drives REQ-M-001 sizing | Datasheet.md | Conditions#Design Conditions | -- | PROPOSAL: Datasheet | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add mechanical controls and interlocks (thermostats, CO sensors, VFDs) as a system category in the Mechanical Systems table | Procedure Step 1 checklist includes "mechanical controls and interlocks" but no corresponding entry appears in the Datasheet systems inventory; this is an incomplete record | Datasheet.md; Procedure.md | Datasheet#Mechanical Systems -- Identified; Procedure#Step 1 | -- | PROPOSAL: Datasheet | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology for general building exhaust fan(s): align Datasheet "Exhaust Fan(s)" entry, Procedure Step 1 checklist item, and Guidance CONF-M-02 scope boundary into a single consistent term and scope definition | Datasheet references "Exhaust Fan(s)" citing SOW-0066; Procedure Step 1 references "General building exhaust fan(s)"; Guidance CONF-M-02 discusses scope boundary. The three documents use different framing for the same system element, risking drift | Datasheet.md; Procedure.md; Guidance.md | Datasheet#Mechanical Systems -- Identified; Procedure#Step 1; Guidance#CONF-M-02 | -- | PROPOSAL: Guidance (vocabulary note) + Datasheet + Procedure | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Baseline | 1 | HAS_ITEMS | NBC/ABC edition not confirmed |
| C:normative:sufficiency | normative | sufficiency | Prescribed Competence Threshold | 0 | NO_ITEMS | P.Eng. competence threshold stated |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | OH&S code for welding fume OELs not identified |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references internally consistent where cited |
| C:operative:necessity | operative | necessity | Essential Operational Capacity | 1 | HAS_ITEMS | TAB requirements missing from Specification |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Execution | 0 | NO_ITEMS | Procedure steps are sufficient for specification production |
| C:operative:completeness | operative | completeness | Thorough Operational Integration | 1 | HAS_ITEMS | No commissioning requirement in Specification |
| C:operative:consistency | operative | consistency | Standardized Process Reliability | 0 | NO_ITEMS | Process described consistently in Procedure |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Owner value (occupant safety, cost efficiency) articulated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Credible Merit Assessment | 0 | NO_ITEMS | Trade-off analysis provides credible basis |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Accounting | 0 | NO_ITEMS | Lifecycle cost referenced though TBD |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Values aligned with design-build framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm applicable edition of NBC / Alberta Building Code for this project and add to Standards table | The Standards table lists NBC and ABC as ASSUMPTION with "edition TBD"; the compulsory compliance baseline cannot be established without confirmed code editions | Specification.md | Standards | -- | AHJ / Mechanical Engineer | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add Alberta OH&S Code reference for occupational exposure limits (welding fumes, CO) to the Standards table | Guidance P-1 references OELs and Guidance C-3 references ACGIH; the Specification Standards table does not cite Alberta OH&S Code, leaving exhaustive regulatory coverage incomplete for occupational health | Specification.md; Guidance.md | Specification#Standards; Guidance#P-1; Guidance#C-3 | -- | PROPOSAL: Specification | TBD |
| C-003 | C:operative:necessity | MissingSlot | Specification | Specification | Add Testing, Adjusting, and Balancing (TAB) requirement as a normative requirement (e.g., REQ-M-012) or as a subsection of the Verification section | Procedure Step 6 checklist calls for "TAB requirements" as a specification section, and Procedure Records lists a "TAB report" as a required record, but no TAB requirement exists in Specification; this is an essential operational capacity gap | Specification.md; Procedure.md | Specification#Requirements; Procedure#Step 6; Procedure#Records | -- | PROPOSAL: Specification | TBD |
| C-004 | C:operative:completeness | VerificationGap | Specification | Specification | Add startup and commissioning requirements as a normative requirement or verification entry | Procedure Step 6 checklist includes "Startup and commissioning requirements" as a specification section to draft, but no corresponding requirement or verification entry exists in the Specification; thorough operational integration requires this | Specification.md; Procedure.md | Specification#Requirements; Specification#Verification; Procedure#Step 6 | -- | PROPOSAL: Specification + Procedure | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Compliance Imperative | 1 | HAS_ITEMS | CSA B149.1 edition unconfirmed |
| F:normative:sufficiency | normative | sufficiency | Stipulated Regulatory Sufficiency | 1 | HAS_ITEMS | No requirement for equipment submittals review |
| F:normative:completeness | normative | completeness | Total Prescriptive Authority | 0 | NO_ITEMS | Scope sections provide clear authority boundaries |
| F:normative:consistency | normative | consistency | Coherent Prescriptive Standard | 1 | HAS_ITEMS | Ceiling fan count sourcing inconsistent |
| F:operative:necessity | operative | necessity | Critical Functional Prerequisite | 1 | HAS_ITEMS | Air balance calculation prerequisite not in Specification |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Process Competence | 0 | NO_ITEMS | Procedure demonstrates competent workflow |
| F:operative:completeness | operative | completeness | Comprehensive Operational Scope | 0 | NO_ITEMS | Operational scope covers all identified systems |
| F:operative:consistency | operative | consistency | Uniform Operational Dependability | 0 | NO_ITEMS | Operational steps consistently structured |
| F:evaluative:necessity | evaluative | necessity | Foundational Quality Imperative | 1 | HAS_ITEMS | No energy efficiency / heat recovery requirement |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Adequacy | 0 | NO_ITEMS | Quality adequacy framework present |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 0 | NO_ITEMS | Quality accounting adequate for current stage |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm applicable CSA B149.1 edition for natural gas installation and update Standards table | CSA B149.1 is listed as ASSUMPTION with "location TBD"; an absolute compliance imperative for natural gas piping requires confirmed code reference | Specification.md | Standards | -- | AHJ / Mechanical Engineer | TBD |
| F-002 | F:normative:sufficiency | MissingSlot | Specification | Specification | Add a requirement for mechanical equipment submittal review process (shop drawings, cut sheets, performance data) prior to installation | The Specification does not address equipment submittal requirements; for stipulated regulatory sufficiency and contractual completeness, a submittal review requirement is standard practice for design-build IFC specifications | Specification.md | Requirements | -- | PROPOSAL: Specification | TBD |
| F-003 | F:normative:consistency | Conflict | Multi | Specification | Resolve ceiling fan count authority: Decomposition SOW-0040 states 6 ceiling fans citing App B-Elec; App B (Shop) does not confirm this count; Specification REQ-M-007 inherits the 6-fan assumption | Two sources disagree on whether the 6-fan count is confirmed or assumed; this is already identified as CONF-M-01 in Guidance but remains unresolved and affects Specification REQ-M-007 and Datasheet attributes | Specification.md; Guidance.md; Datasheet.md | Specification#REQ-M-007; Guidance#CONF-M-01; Datasheet#Mechanical Systems -- Identified | Specification.md#REQ-M-007 vs. Guidance.md#CONF-M-01 | PROPOSAL: County or design team to confirm via App B-Elec | TBD |
| F-004 | F:operative:necessity | VerificationGap | Specification | Specification | Add requirement that makeup air volume must equal or exceed total exhaust volume, with air balance calculation documented in DEL-003-06 | Guidance C-2 identifies air balance as critical; Specification REQ-M-002 notes "sized to balance exhaust air volumes" but has no formal requirement for a documented air balance calculation as a verification artifact | Specification.md; Guidance.md | Specification#REQ-M-002; Guidance#C-2 | -- | PROPOSAL: Specification | TBD |
| F-005 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale for why heat recovery should be a normative requirement vs. a design preference, citing RFP "high recovery" language and lifecycle cost implications | Guidance P-3 discusses "high-recovery heating" as an owner requirement but the Specification treats heat recovery as optional ("encouraged" in REQ-M-003 notes). The foundational quality imperative lens reveals this gap between owner intent and specification strength | Specification.md; Guidance.md | Specification#REQ-M-003; Guidance#P-3 | -- | PROPOSAL: Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Compliance Direction | 0 | NO_ITEMS | Compliance direction is stated in Guidance P-1, P-3 |
| D:normative:applying | normative | applying | Enforced Adequacy Standard | 1 | HAS_ITEMS | Specification format not confirmed |
| D:normative:judging | normative | judging | Resolved Conformance Boundary | 1 | HAS_ITEMS | MEP responsibility boundary unresolved |
| D:normative:reviewing | normative | reviewing | Settled Regulatory Verification | 0 | NO_ITEMS | Verification approaches mapped to requirements |
| D:operative:guiding | operative | guiding | Resolved Capability Guidance | 0 | NO_ITEMS | Capability guidance in Guidance and Procedure adequate |
| D:operative:applying | operative | applying | Settled Execution Proficiency | 0 | NO_ITEMS | Execution steps in Procedure are proficient |
| D:operative:judging | operative | judging | Resolved Performance Judgment | 0 | NO_ITEMS | Performance judgment framework in place (pending numeric values) |
| D:operative:reviewing | operative | reviewing | Settled Process Verification | 0 | NO_ITEMS | Procedure verification checklist is settled |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Direction | 0 | NO_ITEMS | Worth direction established in Guidance principles |
| D:evaluative:applying | evaluative | applying | Settled Merit Deployment | 0 | NO_ITEMS | Trade-offs table provides merit deployment framework |
| D:evaluative:judging | evaluative | judging | Resolved Quality Verdict | 0 | NO_ITEMS | Quality verdict deferred appropriately to design stage |
| D:evaluative:reviewing | evaluative | reviewing | Settled Worth Appraisal | 1 | HAS_ITEMS | No Owner post-occupancy feedback mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Procedure | Procedure | Clarify specification format: Procedure Step 6 notes CSC MasterFormat "or equivalent" as ASSUMPTION; confirm with design-builder whether MasterFormat Division 23 or an alternative format will be used | The enforced adequacy standard requires a definitive specification format; the current ASSUMPTION label leaves the format ambiguous, which could affect how requirements are structured in the IFC package | Procedure.md | Step 6 | -- | Design-builder quality management plan | TBD |
| D-002 | D:normative:judging | Conflict | Multi | Specification | Resolve MEP responsibility boundary for exhaust fan(s) per SOW-0066: Is the general building exhaust fan mechanical scope (with electrical supply from PKG-004) or electrical scope? | This is already identified as CONF-M-02 in Guidance but remains TBD; the resolved conformance boundary lens highlights that this unresolved boundary affects Specification scope and requirements coverage | Specification.md; Guidance.md | Specification#Scope; Guidance#CONF-M-02 | Guidance.md#CONF-M-02 (Decomposition SOW-0066 vs. RFP §3.4 mechanical scope) | PROPOSAL: MEP coordination meeting to resolve | TBD |
| D-003 | D:evaluative:reviewing | RationaleGap | Guidance | Guidance | Add a note on post-occupancy performance validation: how will the Owner verify that the mechanical systems achieve the intended comfort, safety, and efficiency outcomes after construction completion? | The settled worth appraisal lens reveals no mechanism for the Owner to evaluate long-term system performance after the CCC is issued; Procedure Records lists a CCC but no operational performance evaluation | Guidance.md; Procedure.md | Guidance#Considerations; Procedure#Records | -- | PROPOSAL: Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Anchored Directive Foundation | 0 | NO_ITEMS | Directive foundation is anchored to RFP and Decomposition |
| X:guiding:sufficiency | guiding | sufficiency | Calibrated Guidance Adequacy | 0 | NO_ITEMS | Guidance adequately calibrated for design-build context |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Scope | 1 | HAS_ITEMS | No directive on ductwork material standards |
| X:guiding:consistency | guiding | consistency | Uniform Directive Coherence | 0 | NO_ITEMS | Directive messaging coherent across Guidance |
| X:applying:necessity | applying | necessity | Obligatory Practice Foundation | 1 | HAS_ITEMS | No requirement for coordination meeting records |
| X:applying:sufficiency | applying | sufficiency | Validated Execution Adequacy | 0 | NO_ITEMS | Execution adequacy validated by Procedure steps |
| X:applying:completeness | applying | completeness | Exhaustive Practice Coverage | 0 | NO_ITEMS | Practice coverage adequate for specification production |
| X:applying:consistency | applying | consistency | Stable Practice Uniformity | 0 | NO_ITEMS | Practice steps consistently structured |
| X:judging:necessity | judging | necessity | Essential Adjudication Basis | 1 | HAS_ITEMS | No criteria for evaluating design-build proposals against specification |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Evidence | 0 | NO_ITEMS | Evidence basis in Verification table is justified |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Record | 1 | HAS_ITEMS | No traceability matrix from RFP requirements to specification requirements |
| X:judging:consistency | judging | consistency | Coherent Adjudication Standard | 0 | NO_ITEMS | Adjudication standards coherent |
| X:reviewing:necessity | reviewing | necessity | Essential Verification Basis | 1 | HAS_ITEMS | Verification for REQ-M-005 lacks capture velocity standard |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Verification Scope | 0 | NO_ITEMS | Verification scope covers all REQ-M items |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Verification Coverage | 0 | NO_ITEMS | All 11 requirements have verification entries |
| X:reviewing:consistency | reviewing | consistency | Uniform Verification Coherence | 0 | NO_ITEMS | Verification approaches consistently structured |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on ductwork material standards and insulation requirements for the 35 ft ceiling environment (condensation control, energy efficiency, fire rating) | The comprehensive directive scope lens reveals that Guidance addresses system types and performance but not ductwork material selection, which is a significant design decision for a large industrial building with temperature differentials | Guidance.md | Considerations | -- | PROPOSAL: Guidance | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a requirement in Procedure Step 7 to retain formal records of MEP coordination meetings (attendees, decisions, action items) as verification evidence | Procedure Step 7 mentions "Resolve all coordination comments" and "Document coordination in transmittal log" but does not require formal meeting records as a verification artifact; this is an obligatory practice for demonstrating coordination occurred | Procedure.md | Step 7 | -- | PROPOSAL: Procedure | TBD |
| X-003 | X:judging:necessity | WeakStatement | Specification | Specification | Add evaluation criteria for how mechanical equipment submittals will be judged against specification requirements (e.g., performance data must meet or exceed minimum thresholds) | No adjudication basis exists for evaluating equipment submittals or design-build proposals against the Specification requirements; this is linked to the missing submittal requirement (F-002) | Specification.md | Requirements | -- | PROPOSAL: Specification | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add a requirements traceability matrix (or cross-reference table) mapping each RFP §3.4 requirement to the corresponding REQ-M entry | The comprehensive adjudication record lens reveals no formal traceability from RFP requirements to Specification requirements; the current approach relies on Source notes in individual requirements but no consolidated cross-reference exists | Specification.md | entire document scanned | -- | PROPOSAL: Specification or companion document | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add a specific verification standard for REQ-M-005 (welding exhaust): define the minimum capture velocity value or reference the ACGIH standard that will be used to verify performance | Specification Verification table states "Design review confirming capture velocity meets applicable standard" but does not identify which standard or what numeric threshold; verification cannot be performed without a defined standard | Specification.md | Verification (REQ-M-005 row) | -- | PROPOSAL: Specification (cite ACGIH standard and required capture velocity) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative and sourced |
| E:guiding:information | guiding | information | Coherent Directive Intelligence | 0 | NO_ITEMS | Directive information is coherent |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Directive Mastery | 1 | HAS_ITEMS | No guidance on Alberta cold-start heating strategy |
| E:guiding:wisdom | guiding | wisdom | Principled Directive Foresight | 0 | NO_ITEMS | Foresight demonstrated in trade-offs and coordination notes |
| E:applying:data | applying | data | Verified Practice Evidence | 1 | HAS_ITEMS | Datasheet does not record preliminary design approval gate |
| E:applying:information | applying | information | Actionable Practice Intelligence | 0 | NO_ITEMS | Procedure provides actionable intelligence |
| E:applying:knowledge | applying | knowledge | Validated Execution Expertise | 0 | NO_ITEMS | Execution expertise appropriately scoped to P.Eng. |
| E:applying:wisdom | applying | wisdom | Grounded Execution Judgment | 0 | NO_ITEMS | Execution judgment grounded in design-build principles |
| E:judging:data | judging | data | Substantiated Judgment Record | 0 | NO_ITEMS | Judgment record substantiated by source citations |
| E:judging:information | judging | information | Articulated Judgment Rationale | 0 | NO_ITEMS | Judgment rationale articulated in Guidance conflict table |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Mastery | 0 | NO_ITEMS | Adjudication deferred to P.Eng. and AHJ appropriately |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Adjudication principles consistent with professional practice |
| E:reviewing:data | reviewing | data | Confirmed Audit Evidence | 1 | HAS_ITEMS | Conflict table rulings all TBD |
| E:reviewing:information | reviewing | information | Contextual Audit Intelligence | 0 | NO_ITEMS | Audit context adequate |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Expertise | 0 | NO_ITEMS | Audit scope comprehensive for current stage |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight demonstrated in Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | Normalization | Guidance | Guidance | Add a consideration for cold-start heating strategy: how will the building be brought from cold soak to operating temperature (overnight or weekend shutdowns) given the 35 ft ceiling and thermal mass | Guidance P-2 and P-3 discuss ceiling height and high-recovery heating but do not address cold-start scenarios, which are a significant operational knowledge gap for Alberta industrial buildings with large thermal mass | Guidance.md | Considerations | -- | PROPOSAL: Guidance | TBD |
| E-002 | E:applying:data | Normalization | Datasheet | Datasheet | Add a field in the Datasheet Conditions or Construction section noting whether County preliminary design approval is required for mechanical design specifically (Procedure Step 9 flags this as conditional) | Procedure Step 9 raises this as a conditional gate; the Datasheet does not record this approval requirement as a condition, creating a gap in verified practice evidence | Datasheet.md; Procedure.md | Datasheet#Conditions; Procedure#Step 9 | -- | PROPOSAL: Datasheet | TBD |
| E-003 | E:reviewing:data | Conflict | Guidance | Guidance | All three conflicts in the Guidance conflict table (CONF-M-01, CONF-M-02, CONF-M-03) have HumanRuling = TBD; these must be resolved before the specification can be finalized | The confirmed audit evidence lens reveals that no conflict has been adjudicated; the conflict table contains 3 open items that block definitive resolution of specification content | Guidance.md | Conflict Table | Guidance.md#CONF-M-01; Guidance.md#CONF-M-02; Guidance.md#CONF-M-03 | PROPOSAL: County project representative + MEP coordination | TBD |

---

*End of Semantic Lensing Register.*
