# Semantic Lensing Register: DEL-002-02 Foundation Plan

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-002_Structural Design/1_Working/DEL-002-02_Foundation-Plan/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-02_Foundation-Plan/_CONTEXT.md
- _STATUS.md — DEL-002-02_Foundation-Plan/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-02_Foundation-Plan/_SEMANTIC.md (Audit Result: PASS, 2026-02-26)
- Datasheet.md — DEL-002-02_Foundation-Plan/Datasheet.md
- Specification.md — DEL-002-02_Foundation-Plan/Specification.md
- Guidance.md — DEL-002-02_Foundation-Plan/Guidance.md
- Procedure.md — DEL-002-02_Foundation-Plan/Procedure.md
- _REFERENCES.md — DEL-002-02_Foundation-Plan/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 6
  - Specification: 8
  - Guidance: 1
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 8
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp verification gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ confirmation missing |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit adequately covered in Specification Verification table and Procedure Verification table |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Crane supplier data sequencing |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-8 in Procedure cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Slab performance criteria missing |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit addressed via Procedure Verification table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance trade-offs section covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Adequately addressed in Guidance Considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost/schedule trade-offs addressed in Guidance T-1, T-2, T-3 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality addressed through verification tables in Specification and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific edition(s) of Alberta Building Code and NBC govern this project; resolve "current edition" to a specific year/edition reference | R-005 and the Standards table both state "current edition" without identifying the specific code edition; this ambiguity could affect which code provisions apply to foundation design | Specification.md | R-005 -- Code Compliance; Standards table | -- | PROPOSAL: Structural Engineer to confirm applicable edition with AHJ prior to design | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add explicit verification that the P.Eng. stamp is by an engineer licensed specifically in Alberta (not merely any P.Eng.) | R-001 verification says "confirm stamp and signature" but does not explicitly require confirming the Alberta licensing status of the stamping engineer | Specification.md | R-001 -- IFC Drawing Stamp, Verification table row R-001 | -- | PROPOSAL: Specification verification should include Alberta licence number confirmation | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Which Authority Having Jurisdiction (AHJ) will review the building permit application for this site (SW 14-44-21-W4)? Is it Camrose County Safety Codes Officer or a provincial authority? | The AHJ identity is not specified in any production document; R-005 verification depends on "building permit issued by AHJ" but the AHJ is never identified | Specification.md, Procedure.md | R-005 -- Code Compliance; Procedure Step 8 | -- | PROPOSAL: Design-Builder to confirm AHJ identity with Camrose County | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add guidance on sequencing and timeline for obtaining crane supplier technical data; clarify whether preliminary crane loads are sufficient for preliminary design or whether supplier data is a hard prerequisite for Step 2 | Procedure Step 1.3 mentions contacting crane supplier and using "conservative preliminary loading" but does not specify when confirmed data is required relative to other steps | Procedure.md | Step 1 -- Mobilize and Gather Inputs, substep 1.3 | -- | PROPOSAL: Structural Engineer to establish crane data timeline | TBD |
| A-005 | A:operative:judging | MissingSlot | Specification | Specification | Add acceptance criteria for slab-on-grade performance: minimum slab thickness range, reinforcement criteria, or reference to a design standard for industrial floor loading | R-010 requires slab provisions but verification is only "slab specifications appear on foundation plan drawings"; no performance threshold or acceptance basis is stated | Specification.md | R-010 -- Slab-on-Grade Provisions | -- | PROPOSAL: Structural Engineer to define acceptance criteria based on equipment loading from Datasheet | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Frost depth value absent |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Bearing capacity TBD without interim value |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Reinforcing grade missing |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key dependency signals (geotech-first, County approval) consistently communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for design decisions adequately provided in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All load sources and coordination requirements listed |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency: Service Pit vs. service pit |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural design fundamentals referenced appropriately |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement ensures competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Design knowledge scope covered by standards references and code citations |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of design approach consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key judgment calls (geotech timing, variable-price transparency) addressed in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of project constraints present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across Guidance principles and trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add a preliminary frost depth value or range for central Alberta (e.g., 1.2 m to 1.5 m as noted in Procedure Step 2.3) to the Foundation-Specific Attributes table; currently shows only "TBD" | Frost depth is an essential design fact for foundation embedment depth; the Datasheet records it only as TBD while Procedure 2.3 provides an assumed range | Datasheet.md, Procedure.md | Datasheet: Foundation-Specific Attributes -- Frost depth row; Procedure: Step 2.3 | -- | PROPOSAL: Adopt Procedure assumed range (1.2-1.5 m) as preliminary value in Datasheet pending DEL-008-01 | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify "TBD -- to be established from geotechnical report" for bearing capacity by adding a preliminary assumed value or range for normal ground conditions to support preliminary design per RFP section 4.8.2 | The normal-ground-conditions assumption is repeatedly referenced but no preliminary bearing capacity value is documented anywhere; this limits the ability to verify adequacy of preliminary design | Datasheet.md | Foundation-Specific Attributes -- Foundation bearing capacity row | -- | PROPOSAL: Structural Engineer to state assumed preliminary bearing capacity for normal ground conditions | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add concrete reinforcing steel grade (e.g., 400R, 500R per CSA standards) to Foundation-Specific Attributes, or note as TBD | Procedure Step 6.1 references "general structural notes: reinforcing grade" as a required drawing element, but no reinforcing grade value appears in Datasheet | Datasheet.md | Foundation-Specific Attributes table; Construction section | -- | PROPOSAL: Structural Engineer to specify reinforcing grade | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: use either "Service Pit" or "service pit" consistently across all documents; currently both terms appear, sometimes interchangeably | Datasheet uses "Service Pit/pit" and "Service pit/trench"; Specification uses "Service Pit/pit"; Guidance uses "Service Pit/pit" and "service pit"; Procedure uses both forms -- inconsistent usage risks confusion in construction | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Datasheet: Construction -- Service pit/trench structure; Specification: R-006; Guidance: C-3; Procedure: Step 3.2, Step 6.1 | -- | PROPOSAL: Adopt a single canonical term (e.g., "service pit") with a parenthetical note defining the synonym on first use in each document | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Regulatory Basis | 1 | HAS_ITEMS | CSA standard citations lack clause specificity |
| C:normative:sufficiency | normative | sufficiency | Mandated Competence Proof | 0 | NO_ITEMS | P.Eng. requirement adequately establishes mandated competence |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Record | 1 | HAS_ITEMS | Standards table missing specific clause refs |
| C:normative:consistency | normative | consistency | Mandated Regulatory Fidelity | 0 | NO_ITEMS | Regulatory references consistent where provided |
| C:operative:necessity | operative | necessity | Critical Operational Capacity | 0 | NO_ITEMS | Procedure steps establish critical operational capacity adequately |
| C:operative:sufficiency | operative | sufficiency | Validated Operational Scope | 0 | NO_ITEMS | Scope adequately bounded by Specification inclusions/exclusions |
| C:operative:completeness | operative | completeness | Comprehensive Process Mastery | 1 | HAS_ITEMS | Missing interdisciplinary hold point |
| C:operative:consistency | operative | consistency | Repeatable Process Integrity | 0 | NO_ITEMS | Process steps are sequenced consistently |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Clarity | 0 | NO_ITEMS | Variable-price scope mechanism establishes foundational worth clarity |
| C:evaluative:sufficiency | evaluative | sufficiency | Competent Merit Appraisal | 0 | NO_ITEMS | Trade-offs provide adequate merit appraisal framing |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation Mastery | 0 | NO_ITEMS | Guidance covers all major valuation dimensions (cost, schedule, capacity) |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Stability | 0 | NO_ITEMS | Valuation reasoning consistent across Guidance trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Add specific clause references for CSA A23.3 and CSA A23.1/A23.2 that are applicable to foundation design (e.g., CSA A23.3 clause for footing design, development length) or state that the Structural Engineer will identify applicable clauses | The Standards table lists CSA A23.3 and CSA A23.1/A23.2 with generic applicability descriptions but no clause-level specificity; the accompanying note acknowledges this gap but does not set a mechanism for resolution | Specification.md | Standards table -- CSA A23.3, CSA A23.1/A23.2 rows; Note below Standards table | -- | PROPOSAL: Structural Engineer to append applicable clause list after design begins | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add reference to Alberta Environmental Protection and Enhancement Act (EPEA) or other environmental regulation if applicable to below-grade construction near a landfill (site is at a regional landfill) | The site is at a regional landfill; environmental regulations may impose requirements on below-grade construction (e.g., contamination testing, liner requirements); no environmental regulatory reference appears in Standards or Requirements | Specification.md | Standards table; entire document scanned | -- | PROPOSAL: Design-Builder to confirm whether EPEA or other environmental requirements apply to foundation construction at a landfill site | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add an explicit hold point between Step 5 (geotech integration) and Step 6 (IFC production) requiring sign-off that geotech data has been integrated before IFC drawing production begins | Guidance P-1 emphasizes geotech-first principle, but Procedure does not include a formal hold point or gate check between Steps 5 and 6; this risks IFC production proceeding before geotech integration is confirmed | Procedure.md | Between Step 5 and Step 6 | -- | PROPOSAL: Add hold-point verification row to Procedure Verification table | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Conformance Awareness | 0 | NO_ITEMS | Conformance awareness adequately established in Specification R-005 |
| F:normative:sufficiency | normative | sufficiency | Sufficient Regulatory Threshold | 1 | HAS_ITEMS | Threshold for code compliance acceptance not explicit |
| F:normative:completeness | normative | completeness | Total Conformance Command | 0 | NO_ITEMS | Conformance coverage addressed across all 12 requirements |
| F:normative:consistency | normative | consistency | Uniform Conformance Assurance | 0 | NO_ITEMS | Conformance messaging consistent across docs |
| F:operative:necessity | operative | necessity | Core Procedural Foundation | 1 | HAS_ITEMS | Missing electrical coordination |
| F:operative:sufficiency | operative | sufficiency | Proven Procedural Adequacy | 0 | NO_ITEMS | Procedure scope adequate for described task |
| F:operative:completeness | operative | completeness | Total Procedural Coverage | 0 | NO_ITEMS | Procedure steps 1-8 cover the full lifecycle |
| F:operative:consistency | operative | consistency | Stable Procedural Coherence | 0 | NO_ITEMS | Procedure steps are internally consistent |
| F:evaluative:necessity | evaluative | necessity | Vital Appraisal Foundation | 0 | NO_ITEMS | OBJ-006 provides the vital appraisal foundation |
| F:evaluative:sufficiency | evaluative | sufficiency | Competent Worth Demonstration | 0 | NO_ITEMS | Variable-price documentation requirement in R-009 is adequate |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Accounting | 1 | HAS_ITEMS | No mechanism for tracking assumption changes |
| F:evaluative:consistency | evaluative | consistency | Principled Worth Consistency | 0 | NO_ITEMS | Worth reasoning consistent between Specification R-009 and Guidance P-2 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for R-005 (Code Compliance) beyond "building permit issued by AHJ"; specify whether a code compliance review or third-party review is required before permit submission | R-005 verification is "building permit issued by AHJ" which is a lagging indicator; no leading verification (e.g., code compliance checklist, independent review) is specified to catch non-compliance before permit submission | Specification.md | R-005 -- Code Compliance, Verification table row R-005 | -- | PROPOSAL: Add a pre-submission code compliance review step to Specification verification | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add electrical engineer coordination to Procedure Step 1.4 or as a separate substep; electrical coordination is needed for service pit lighting and power, and potentially for embedded conduit in slab | Guidance C-3 mentions electrical coordination for service pit lighting and power, but Procedure Step 1.4 lists only plumbing and mechanical engineer inputs; electrical is omitted from the prerequisite input list | Procedure.md, Guidance.md | Procedure: Step 1.4; Guidance: C-3 | -- | PROPOSAL: Add electrical engineer input to Procedure Step 1 prerequisites | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add guidance on how design assumption changes between preliminary and final design should be tracked and communicated; clarify the documentation format for variable-price assumption baseline | Guidance P-2 and Specification R-009 require documenting assumptions, but neither explains how changes to those assumptions should be tracked across the design lifecycle or what constitutes a baseline for cost comparison | Guidance.md | P-2 -- Variable-Price Scope Transparency | -- | PROPOSAL: Guidance should describe an assumption-tracking mechanism or reference a project-level change management process | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Directive authority clear: P.Eng. holds design authority per RFP |
| D:normative:applying | normative | applying | Resolved Compulsory Practice | 0 | NO_ITEMS | Compulsory practices enumerated in Specification requirements |
| D:normative:judging | normative | judging | Binding Adherence Ruling | 1 | HAS_ITEMS | Variable-price scope boundary unclear |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Conformance | 0 | NO_ITEMS | Oversight conformance addressed through County approval and P.Eng. stamp |
| D:operative:guiding | operative | guiding | Resolved Operational Pathway | 0 | NO_ITEMS | Procedure provides a resolved operational pathway |
| D:operative:applying | operative | applying | Resolved Performance Delivery | 0 | NO_ITEMS | Performance delivery steps are clear |
| D:operative:judging | operative | judging | Resolved Capability Verdict | 0 | NO_ITEMS | Capability verified via structural calculations (DEL-002-10) |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Soundness | 0 | NO_ITEMS | Procedure verification table provides soundness review |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Guidance | 1 | HAS_ITEMS | Old North Shop interface value question |
| D:evaluative:applying | evaluative | applying | Resolved Merit Enactment | 0 | NO_ITEMS | Merit enacted through coordinated design process |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | Worth determination deferred to post-geotech negotiation per OBJ-006 |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Assurance | 0 | NO_ITEMS | QA addressed via verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | Conflict | Multi | TBD | Resolve whether variable-price scope (SOW-0019) includes only the foundation design revision triggered by geotechnical findings, or also the baseline foundation design; Specification R-009 implies the drawings identify variable-price elements, but the boundary between firm-price and variable-price foundation work is not defined in accessible sources | Guidance C-002 conflict identifies this issue; Specification R-009 requires "clearly identify the variable-price scope elements" but no definition of which elements are variable-price vs. firm-price exists in production documents; CCDC 14-2013 (which would define this) is not accessible | Specification.md, Guidance.md | Specification: R-009; Guidance: Conflict Table C-002 | Specification.md#R-009 (variable-price elements on drawings), Guidance.md#C-002 (CCDC 14-2013 terms not accessible) | PROPOSAL: Legal/contract review of CCDC 14-2013 to define firm-price vs. variable-price boundary for foundation scope | TBD |
| D-002 | D:evaluative:guiding | TBD_Question | Multi | Guidance | Record TBD: Does the Foundation Plan need to address any structural interface with the existing Old North Shop (105 ft x 40 ft adjacent structure)? If yes, what is the scope of interface work (new foundation adjacent to existing, tie-in, independent)? | Guidance Conflict C-001 raises this; Datasheet records both buildings but the interface scope is undefined; this affects whether the foundation plan must show interface details or is strictly limited to new construction | Datasheet.md, Guidance.md | Datasheet: Building Configuration -- Combined site width; Guidance: Conflict Table C-001 | -- | PROPOSAL: Structural Engineer and County to confirm scope boundary per Guidance C-001 proposal | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Purposeful Foundational Mandate | 0 | NO_ITEMS | Foundational mandate (geotech-first, code-compliant) clearly established |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Guided Competence | 0 | NO_ITEMS | Guided competence established through P.Eng. requirement and standards references |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Mastery | 0 | NO_ITEMS | Directive coverage comprehensive across 12 specification requirements |
| X:guiding:consistency | guiding | consistency | Stable Directive Alignment | 0 | NO_ITEMS | Directives aligned across documents |
| X:applying:necessity | applying | necessity | Essential Execution Grounding | 1 | HAS_ITEMS | Concrete cover requirements absent |
| X:applying:sufficiency | applying | sufficiency | Sufficient Applied Competence | 0 | NO_ITEMS | Applied competence scope adequate |
| X:applying:completeness | applying | completeness | Thorough Execution Account | 1 | HAS_ITEMS | Drawing sheet count not estimated |
| X:applying:consistency | applying | consistency | Consistent Execution Precision | 0 | NO_ITEMS | Execution steps consistent |
| X:judging:necessity | judging | necessity | Critical Conformance Basis | 0 | NO_ITEMS | Conformance basis established via code and contract references |
| X:judging:sufficiency | judging | sufficiency | Sufficient Judgment Evidence | 0 | NO_ITEMS | Judgment evidence will be provided by DEL-002-10 calculations |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Record | 0 | NO_ITEMS | Judgment coverage addressed by verification tables |
| X:judging:consistency | judging | consistency | Uniform Judgment Stability | 0 | NO_ITEMS | Judgment criteria consistent across Specification and Procedure verification tables |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | No drawing revision control requirement |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Oversight Competence | 0 | NO_ITEMS | Oversight roles defined in Procedure |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Mastery | 0 | NO_ITEMS | Audit coverage comprehensive |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Integrity | 0 | NO_ITEMS | Audit approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Datasheet | Datasheet | Add concrete cover requirements to Foundation-Specific Attributes (e.g., minimum cover for footings, slabs, grade beams per CSA A23.1); Procedure Step 6.1 lists "concrete cover" as a required general note item but no value is recorded in Datasheet | Concrete cover is a fundamental execution parameter for foundation construction; it is referenced as a required drawing note in Procedure but has no recorded value or TBD placeholder in Datasheet | Datasheet.md, Procedure.md | Datasheet: Foundation-Specific Attributes (absent); Procedure: Step 6.1 | -- | PROPOSAL: Structural Engineer to specify per CSA A23.1 exposure class for this site | TBD |
| X-002 | X:applying:completeness | RationaleGap | Specification | Guidance | Add rationale for anticipated number of drawing sheets and drawing organization (e.g., whether foundation plan is one sheet or multiple sheets, whether sections/details appear on the foundation plan or only in DEL-002-04) | Specification Documentation section notes "one or more sheets depending on building complexity" but provides no guidance on what determines the split; this could affect coordination review scope | Specification.md | Documentation -- Additional Anticipated Documentation | -- | PROPOSAL: Structural Engineer to establish drawing sheet organization at preliminary design stage | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add a requirement for drawing revision control: each IFC sheet must include a revision block with revision number, date, and description of changes | Neither Specification nor Procedure requires revision control on the drawings; Specification Documentation mentions "Revision log" but no verification requirement ensures revision tracking on individual sheets | Specification.md | Documentation -- Additional Anticipated Documentation; Verification table (absent) | -- | PROPOSAL: Add revision control requirement to Specification and corresponding verification check | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Steering Record | 0 | NO_ITEMS | Steering record substantiated by RFP and Decomposition references |
| E:guiding:information | guiding | information | Coherent Guidance Narrative | 0 | NO_ITEMS | Guidance narrative coherent and well-structured |
| E:guiding:knowledge | guiding | knowledge | Proficient Directive Expertise | 0 | NO_ITEMS | Directive expertise reflected in Specification requirements |
| E:guiding:wisdom | guiding | wisdom | Holistic Directive Foresight | 0 | NO_ITEMS | Foresight addressed by Guidance trade-offs and geotech-first principle |
| E:applying:data | applying | data | Substantiated Practice Record | 1 | HAS_ITEMS | Bay width discrepancy |
| E:applying:information | applying | information | Coherent Execution Account | 0 | NO_ITEMS | Execution account in Procedure is coherent |
| E:applying:knowledge | applying | knowledge | Proficient Applied Mastery | 0 | NO_ITEMS | Applied knowledge adequate for design task |
| E:applying:wisdom | applying | wisdom | Judicious Execution Foresight | 0 | NO_ITEMS | Execution foresight covered by geotech timing trade-off |
| E:judging:data | judging | data | Documented Ruling Basis | 0 | NO_ITEMS | Ruling basis documented via source citations |
| E:judging:information | judging | information | Coherent Verdict Account | 0 | NO_ITEMS | Verdict accounts coherent in Specification verification |
| E:judging:knowledge | judging | knowledge | Comprehensive Ruling Expertise | 0 | NO_ITEMS | Ruling expertise reflected in standards and code references |
| E:judging:wisdom | judging | wisdom | Principled Ruling Discernment | 0 | NO_ITEMS | Ruling discernment present in Guidance conflict table |
| E:reviewing:data | reviewing | data | Substantiated Oversight Record | 1 | HAS_ITEMS | County PM identity TBD |
| E:reviewing:information | reviewing | information | Coherent Oversight Narrative | 0 | NO_ITEMS | Oversight narrative coherent |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Review Expertise | 0 | NO_ITEMS | Review expertise scope adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Oversight foresight addressed by verification tables and records requirements |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Datasheet | Datasheet | Normalize bay width data: Datasheet Bay Layout table shows "24 ft, 18 ft (multiple bays indicated)" for drive-through bays while Procedure Step 1.2 says "24 ft, 18 ft (multiple)"; confirm whether these are two distinct bay widths or a range, and record the exact count of each bay width from App B | The bay width description is imprecise in both documents; for a foundation plan, exact bay widths and count directly determine column grid spacing and footing locations | Datasheet.md, Procedure.md | Datasheet: Bay Layout table -- Drive-through repair bays; Procedure: Step 1.2 | -- | PROPOSAL: Extract exact bay widths and counts from Appendix B (Shop) and record in Datasheet | TBD |
| E-002 | E:reviewing:data | Normalization | Datasheet | Datasheet | Add County Project Manager identity or explicit TBD placeholder to Datasheet Conditions table; currently noted as "identity TBD -- confirmed at award" but no mechanism to update this after award | The County PM coordinates inspections and approvals (Procedure Steps 4, 8); their identity is a necessary oversight data point that should be updated once known | Datasheet.md | Conditions table -- County project manager coordination row | -- | PROPOSAL: Update after contract award; add a status note indicating when this TBD should be resolved | TBD |

---

## Verification (QA Contract)

| Check | Validation | Result |
|---|---|---|
| Coverage complete | Every matrix cell (A: 12, B: 16, C: 12, F: 12, D: 12, X: 16, E: 16 = 96 total) has a Lens Coverage entry | PASS (96 entries) |
| No invention | All warranted items grounded in evidence from production documents or explicit absence therein | PASS |
| Provenance present | Every item has SourcePath and SectionRef | PASS |
| Conflicts surfaced | 1 conflict (D-001) has Contenders and HumanRuling = TBD | PASS |
| Summary consistent | Summary counts match actual warranted items (22 items) | PASS |
| Schema followed | Output follows STRUCTURE schema from AGENT_CHIRALITY_LENS | PASS |
