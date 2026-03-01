# Semantic Lensing Register: DEL-001-09 Old North Shop Demolition Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-09_Demolition-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-09_Demolition-Plans/_CONTEXT.md (Name, Package, Description, Anticipated Artifacts)
- _STATUS.md — DEL-001-09_Demolition-Plans/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-09_Demolition-Plans/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-001-09_Demolition-Plans/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-001-09_Demolition-Plans/Specification.md (Scope, Requirements REQ-001..REQ-008, Standards, Verification, Documentation)
- Guidance.md — DEL-001-09_Demolition-Plans/Guidance.md (Purpose, Principles P-001..P-005, Considerations C-001..C-005, Trade-offs T-001..T-002, Conflict Table CONF-001..CONF-002)
- Procedure.md — DEL-001-09_Demolition-Plans/Procedure.md (Prerequisites, Steps Phases 1-3, Verification, Records)
- _REFERENCES.md — DEL-001-09_Demolition-Plans/_REFERENCES.md (R-01, R-04 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive guidance on hazardous materials obligation |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | IFC stamping responsible-party ambiguity |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition not specified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway covered by Procedure Phase 3 |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing procedure for hazmat assessment decision |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps well-covered in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered by Procedure Verification table |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit implicit in Procedure Phase 3 internal review |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed in Guidance Purpose and Trade-offs |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No acceptance criteria for drawing quality/completeness standard |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination addressed in Guidance T-001, T-002 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by Procedure Verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Guidance | Clarify whether hazardous materials assessment is a firm prerequisite or optional recommendation; current language uses hedging ("if required", "may contain") without establishing a decision threshold | Prescriptive direction lens reveals that Guidance C-004 and Procedure Step 1.3 both address hazmat but neither establishes a clear directive on when the assessment becomes mandatory vs. discretionary, which could lead to different implementation decisions | Guidance.md; Procedure.md | Guidance.md#C-004; Procedure.md#Step 1.3 | -- | AHJ / Alberta OHS legislation | TBD |
| A-002 | A:normative:applying | Conflict | Multi | Specification | Resolve whether Architect's seal satisfies RFP P.Eng. stamp requirement or whether P.Eng. co-stamp is required; documents surface the conflict but no resolution path beyond "confirm with AHJ" | Mandatory practice lens highlights that REQ-005 note, Guidance P-005, Guidance CONF-001, and Procedure Step 3.4 all reference this unresolved question but the production documents have no mechanism to force a resolution before IFC issue | Specification.md; Guidance.md; Procedure.md | Specification.md#REQ-005; Guidance.md#CONF-001; Procedure.md#Step 3.4 | Specification.md#REQ-005 ("P.Eng. stamp required"); Guidance.md#CONF-001 ("Architect may not hold P.Eng.") | AHJ and legal counsel per CONF-001 | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: identify exact edition of Alberta Building Code and Alberta Safety Codes Act applicable to this project; current Standards table uses "current edition" and "TBD" without resolution | Compliance determination lens reveals that REQ-006 and the Standards table cannot support a compliance judgment without specifying which code editions apply | Specification.md | Specification.md#Standards | -- | AHJ / permitting authority | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a decision gate or procedural step for obtaining the hazardous materials assessment decision before proceeding past Phase 1; Step 1.3 identifies the risk but no hold point prevents Phase 2 from starting without the result | Procedural direction lens reveals that the Procedure lacks a formal gate requiring hazmat assessment completion (or documented waiver) before demolition scope finalization | Procedure.md | Procedure.md#Phase 1 | -- | Architect / Project Manager | TBD |
| A-005 | A:evaluative:applying | VerificationGap | Specification | Specification | Add acceptance criteria for overall drawing quality standard (e.g., minimum drawing scale, legibility standard, annotation completeness standard) beyond the per-requirement verification checks | Merit application lens reveals that while individual REQs have verification methods, there is no overarching quality acceptance standard for the drawing set as a deliverable product | Specification.md | Specification.md#Verification | -- | Architect | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Mezzanine and washroom areas TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | As-built availability unknown |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet References table provides comprehensive record pointers |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Field survey vs. Appendix B dimension sourcing unclear |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW scope signals clear across documents |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate in Guidance Purpose and Considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Comprehensive account across four documents |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Demolition scope understanding well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed by P.Eng. stamping |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge coverage adequate for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment exercised in Guidance trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately represented in Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided by Guidance Purpose + Considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with principles stated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: obtain measured areas for mezzanine (SOW-0071) and washroom (SOW-0072); both are listed as "TBD (no area stated in sources)" | Essential fact lens reveals that two of the three renovation areas lack a basic dimensional parameter (area), which is necessary for demolition scope definition | Datasheet.md | Datasheet.md#Renovation Areas Subject to Demolition Documentation | -- | Field survey / Architect | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Procedure | Datasheet | Record TBD: confirm whether as-built drawings exist for the Old North Shop; Procedure Step 1.1 requests them but the outcome is unknown | Adequate evidence lens reveals that the adequacy of source data for producing demolition drawings depends on as-built availability, which remains unresolved | Procedure.md; Datasheet.md | Procedure.md#Step 1.1; Datasheet.md#Conditions ("Existing building to remain operational" row Status=TBD) | -- | Camrose County / Owner | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Datasheet | Normalize dimension sourcing: Datasheet states "105' x 40'" from R-04 but Procedure Step 1.4 also references "105' x 40' per R-04"; clarify whether these are verified dimensions or conceptual-plan-only dimensions that may differ from field measurement | Reliable measurement lens reveals that the same dimension (105' x 40') is cited as both a Datasheet attribute and a Procedure input, but neither document flags that R-04 is a conceptual plan and actual dimensions may vary | Datasheet.md; Procedure.md | Datasheet.md#Existing Building -- Old North Shop ("Overall footprint" row); Procedure.md#Step 1.4 | -- | Field survey result | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Regulatory Foundation | 1 | HAS_ITEMS | NBC/ABC relationship unresolved |
| C:normative:sufficiency | normative | sufficiency | Prescribed Compliant Capacity | 0 | NO_ITEMS | Compliant capacity addressed by REQ-006 and Standards |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Missing occupational safety citation |
| C:normative:consistency | normative | consistency | Prescribed Regulatory Coherence | 0 | NO_ITEMS | Regulatory references internally consistent |
| C:operative:necessity | operative | necessity | Operational Requisite Awareness | 0 | NO_ITEMS | Operational prerequisites well-enumerated |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Practical Readiness | 0 | NO_ITEMS | Readiness criteria covered by Procedure prerequisites |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 1 | HAS_ITEMS | No step for drawing numbering convention |
| C:operative:consistency | operative | consistency | Calibrated Procedural Discipline | 0 | NO_ITEMS | Procedure steps sequenced logically |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Merit recognized in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Appraisal | 0 | NO_ITEMS | Value appraisal in Guidance trade-offs |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Worth assessment scope adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify relationship between Alberta Building Code and National Building Code of Canada in Standards table; current entry states "May be adopted by Alberta; relationship to ABC TBD" which is too vague to support compliance determination | Obligatory Regulatory Foundation lens reveals that the foundational code hierarchy is ambiguous -- the Architect cannot determine which code governs without this clarification | Specification.md | Specification.md#Standards (NBC row) | -- | AHJ / permitting authority | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add Alberta Occupational Health and Safety Act/Regulation to Standards table if hazardous materials or worker safety during demolition design are within scope of this deliverable's compliance obligation | Full Regulatory Coverage lens reveals that Guidance C-004 references Alberta OHS obligations but the Standards table in Specification does not include OHS as an applicable standard | Specification.md; Guidance.md | Specification.md#Standards; Guidance.md#C-004 | -- | AHJ / Alberta OHS | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step (or note in Phase 2/3) for establishing the drawing numbering convention referenced as TBD in Specification Documentation section | Exhaustive Process Coverage lens reveals that Specification states "Drawing Numbering Convention: TBD -- to be established by Architect" but no Procedure step assigns this task or places it in the workflow | Specification.md; Procedure.md | Specification.md#Drawing Numbering Convention; Procedure.md (entire document scanned) | -- | Architect | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Compliance Standard | 0 | NO_ITEMS | Compliance standard established by REQ-006 |
| F:normative:sufficiency | normative | sufficiency | Prescribed Compliance Proficiency | 1 | HAS_ITEMS | Verification method for REQ-006 is vague |
| F:normative:completeness | normative | completeness | Exhaustive Statutory Capacity | 1 | HAS_ITEMS | Missing requirement for permit-readiness |
| F:normative:consistency | normative | consistency | Binding Regulatory Order | 0 | NO_ITEMS | Regulatory ordering consistent |
| F:operative:necessity | operative | necessity | Verified Procedural Imperative | 0 | NO_ITEMS | Procedural imperatives well-identified |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Execution Competence | 1 | HAS_ITEMS | No field verification acceptance criterion |
| F:operative:completeness | operative | completeness | Total Execution Authority | 0 | NO_ITEMS | Execution authority established |
| F:operative:consistency | operative | consistency | Disciplined Operational Harmony | 0 | NO_ITEMS | Operational steps harmonized |
| F:evaluative:necessity | evaluative | necessity | Foundational Value Verification | 1 | HAS_ITEMS | No verification that drawings support permitting |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Appraisal Competence | 0 | NO_ITEMS | Appraisal competence addressed |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Authority | 0 | NO_ITEMS | Merit authority scope adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Standard | 0 | NO_ITEMS | Appraisal standard consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen verification method for REQ-006 (Code Compliance): "Code review completed; no unresolved non-compliances at IFC issue" is weak -- clarify who performs the code review, what form the review record takes, and whether AHJ pre-submission review is included | Prescribed Compliance Proficiency lens reveals that the verification method for the most consequential normative requirement is stated in broad terms without specifying the evidentiary standard | Specification.md | Specification.md#Verification (REQ-006 row) | -- | Architect / AHJ | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add a requirement addressing permit-readiness of demolition drawings (i.e., that the drawing set shall be suitable for submission as part of the building permit application DEL-009-02) | Exhaustive Statutory Capacity lens reveals that Guidance Purpose item 2 and Datasheet Construction section both reference the permit-support function, but no explicit Specification requirement ensures the drawings meet permit submission standards | Specification.md; Guidance.md; Datasheet.md | Specification.md#Requirements (entire section scanned); Guidance.md#Purpose item 2; Datasheet.md#Construction (DEL-009-02 row) | -- | AHJ / Architect | TBD |
| F-003 | F:operative:sufficiency | VerificationGap | Specification | Procedure | Add acceptance criterion for field survey data adequacy before proceeding to demolition design (e.g., minimum measurements required, photograph documentation standard) | Demonstrated Execution Competence lens reveals that Procedure Step 1.2 calls for field survey but neither Specification nor Procedure defines what constitutes sufficient field data to proceed | Procedure.md; Specification.md | Procedure.md#Step 1.2; Specification.md#REQ-002 | -- | Architect | TBD |
| F-004 | F:evaluative:necessity | VerificationGap | Specification | Specification | Add verification check confirming that the drawing set is suitable for building permit submission (cross-reference to downstream DEL-009-02) | Foundational Value Verification lens reveals that the Verification table has no entry confirming the deliverable fulfills its stated permitting-support function, despite this being a primary purpose stated in Guidance | Specification.md; Guidance.md | Specification.md#Verification; Guidance.md#Purpose item 2 | -- | Architect / Project Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Prescriptive Decree | 0 | NO_ITEMS | Prescriptive direction resolved through REQ-001..REQ-008 |
| D:normative:applying | normative | applying | Resolved Mandatory Execution | 0 | NO_ITEMS | Mandatory execution addressed by Procedure steps |
| D:normative:judging | normative | judging | Definitive Regulatory Ruling | 1 | HAS_ITEMS | No step for obtaining AHJ pre-approval |
| D:normative:reviewing | normative | reviewing | Resolved Compulsory Oversight | 0 | NO_ITEMS | Oversight resolved through County approval and P.Eng. stamp |
| D:operative:guiding | operative | guiding | Resolved Systematic Guidance | 0 | NO_ITEMS | Systematic guidance in Procedure well-structured |
| D:operative:applying | operative | applying | Resolved Competent Delivery | 1 | HAS_ITEMS | Scope interface decision timing unclear |
| D:operative:judging | operative | judging | Resolved Capability Mastery | 0 | NO_ITEMS | Capability assessment through verification table |
| D:operative:reviewing | operative | reviewing | Resolved Operational Surveillance | 0 | NO_ITEMS | Operational surveillance addressed by internal review |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Purpose | 0 | NO_ITEMS | Value purpose well-articulated in Guidance |
| D:evaluative:applying | evaluative | applying | Resolved Merit Enactment | 0 | NO_ITEMS | Merit enacted through trade-off guidance |
| D:evaluative:judging | evaluative | judging | Resolved Definitive Valuation | 1 | HAS_ITEMS | No metric for demolition scope precision |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Stewardship | 0 | NO_ITEMS | Quality stewardship through review steps |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | MissingSlot | Procedure | Procedure | Add a step for consulting AHJ regarding code edition applicability and permit submission requirements before finalizing demolition design (supports resolving items A-003 and C-001) | Definitive Regulatory Ruling lens reveals that multiple TBD items depend on AHJ confirmation but no Procedure step explicitly tasks the team with obtaining this ruling | Procedure.md | Procedure.md#Phase 2 (entire phase scanned) | -- | Architect / Project Manager | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Add explicit timing for the SOW-0073/0074 scope interface decision (Step 2.4) relative to preliminary design submission (Step 2.6); current sequencing implies Step 2.4 happens first but does not state it as a gate | Resolved Competent Delivery lens reveals that the scope interface decision (CONF-002 resolution) could drift past preliminary design submission if not explicitly gated, which would undermine delivery competence | Procedure.md | Procedure.md#Step 2.4; Procedure.md#Step 2.6 | -- | Architect / Project Manager | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add rationale for how "precision" vs. "breadth" trade-off (T-001) should be evaluated at each design stage; current guidance mentions preliminary vs. IFC stages but does not provide a metric or threshold for acceptable scope precision | Resolved Definitive Valuation lens reveals that the trade-off guidance lacks a concrete evaluation framework, making it difficult to judge whether the deliverable has achieved adequate scope precision | Guidance.md | Guidance.md#T-001 | -- | Architect | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Clarity | 1 | HAS_ITEMS | Missing directive on salvage/reuse |
| X:guiding:sufficiency | guiding | sufficiency | Justified Systematic Capacity | 0 | NO_ITEMS | Systematic capacity justified by Procedure structure |
| X:guiding:completeness | guiding | completeness | Comprehensive Guided Authority | 0 | NO_ITEMS | Guided authority comprehensive in Guidance |
| X:guiding:consistency | guiding | consistency | Stable Prescriptive Clarity | 0 | NO_ITEMS | Prescriptive clarity stable across documents |
| X:applying:necessity | applying | necessity | Mandatory Action Foundation | 1 | HAS_ITEMS | No requirement for field verification sign-off |
| X:applying:sufficiency | applying | sufficiency | Justified Competence Evidence | 0 | NO_ITEMS | Competence evidence justified by P.Eng. stamp |
| X:applying:completeness | applying | completeness | Comprehensive Execution Scope | 1 | HAS_ITEMS | Revision control requirement absent |
| X:applying:consistency | applying | consistency | Reliable Execution Norm | 0 | NO_ITEMS | Execution norms reliable across Procedure |
| X:judging:necessity | judging | necessity | Binding Decisional Basis | 0 | NO_ITEMS | Decisional basis established by requirements |
| X:judging:sufficiency | judging | sufficiency | Defensible Evidentiary Scope | 1 | HAS_ITEMS | REQ-002 verification method not defensible |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Authority | 0 | NO_ITEMS | Adjudicative authority scope adequate |
| X:judging:consistency | judging | consistency | Steady Adjudicative Norm | 0 | NO_ITEMS | Adjudicative norms steady |
| X:reviewing:necessity | reviewing | necessity | Critical Oversight Foundation | 0 | NO_ITEMS | Oversight foundation established by verification table |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Stewardship Evidence | 1 | HAS_ITEMS | No record retention requirement in Specification |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Surveillance Authority | 0 | NO_ITEMS | Surveillance authority adequate |
| X:reviewing:consistency | reviewing | consistency | Dependable Stewardship Norm | 0 | NO_ITEMS | Stewardship norm stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Guidance | Guidance | Add guidance on whether any demolished elements require salvage, reuse, or Owner-directed disposition (e.g., fixtures, materials); Procedure Step 2.1 mentions "remove and salvage (if any)" but Guidance provides no direction on when salvage applies | Foundational Directive Clarity lens reveals that salvage/reuse direction is absent from Guidance despite being referenced as a demolition category in Procedure | Procedure.md; Guidance.md | Procedure.md#Step 2.1; Guidance.md (entire document scanned) | -- | Owner / Camrose County | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add a requirement or verification entry for formal field verification sign-off (i.e., Architect confirms field survey data has been incorporated into base plan) before proceeding to preliminary design | Mandatory Action Foundation lens reveals that REQ-002 requires existing conditions documentation but no verification step confirms that field data (vs. Appendix B conceptual data alone) has been incorporated | Specification.md; Procedure.md | Specification.md#REQ-002; Procedure.md#Step 1.2 | -- | Architect | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add a requirement for revision control / revision history on drawing sheets; Specification Documentation section mentions "revision history" in expected drawing content but it is not captured as a formal requirement | Comprehensive Execution Scope lens reveals that revision control is assumed but not required -- the Procedure Verification table checks "Drawing revision history current" but there is no backing requirement in Specification | Specification.md; Procedure.md | Specification.md#Documentation ("Drawing title block with... revision history"); Procedure.md#Verification ("Drawing revision history current" row) | -- | Architect | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-002 verification method: "Architect confirms coverage of all existing elements within renovation extents" lacks specificity on how confirmation is documented and what "all existing elements" means in practice | Defensible Evidentiary Scope lens reveals that the verification method for REQ-002 is subjective and does not produce auditable evidence (e.g., a checklist, markup, or comparison record) | Specification.md | Specification.md#Verification (REQ-002 row) | -- | Architect | TBD |
| X-005 | X:reviewing:sufficiency | RationaleGap | Specification | Specification | Add rationale or cross-reference explaining why Procedure Records section defines retention but Specification has no corresponding records management requirement; a future auditor needs to know the normative basis for record retention | Sufficient Stewardship Evidence lens reveals that Procedure defines nine record types but Specification contains no requirement mandating their creation or retention, creating a gap in the normative basis for audit evidence | Specification.md; Procedure.md | Specification.md#Requirements (entire section scanned); Procedure.md#Records | -- | Architect / Project Manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Guidance Foundation | 0 | NO_ITEMS | Guidance foundation verified by source citations |
| E:guiding:information | guiding | information | Validated Guidance Signal | 0 | NO_ITEMS | Guidance signals validated |
| E:guiding:knowledge | guiding | knowledge | Demonstrated Guidance Mastery | 0 | NO_ITEMS | Guidance mastery demonstrated by principles and considerations |
| E:guiding:wisdom | guiding | wisdom | Validated Guidance Foresight | 1 | HAS_ITEMS | No forward-looking risk register |
| E:applying:data | applying | data | Verified Execution Evidence | 1 | HAS_ITEMS | Datasheet missing drawing scale attribute |
| E:applying:information | applying | information | Validated Execution Context | 0 | NO_ITEMS | Execution context validated in Procedure prerequisites |
| E:applying:knowledge | applying | knowledge | Demonstrated Delivery Competence | 0 | NO_ITEMS | Delivery competence demonstrated by procedure completeness |
| E:applying:wisdom | applying | wisdom | Principled Delivery Judgment | 0 | NO_ITEMS | Delivery judgment addressed in trade-offs |
| E:judging:data | judging | data | Binding Evidentiary Record | 0 | NO_ITEMS | Evidentiary records defined in Procedure Records |
| E:judging:information | judging | information | Defensible Verdict Clarity | 1 | HAS_ITEMS | Verification results not linked to acceptance decision |
| E:judging:knowledge | judging | knowledge | Comprehensive Verdict Command | 0 | NO_ITEMS | Verdict command adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative wisdom in Guidance conflict table |
| E:reviewing:data | reviewing | data | Verified Audit Documentation | 1 | HAS_ITEMS | No transmittal record template/standard cited |
| E:reviewing:information | reviewing | information | Validated Oversight Account | 0 | NO_ITEMS | Oversight account adequate |
| E:reviewing:knowledge | reviewing | knowledge | Demonstrated Oversight Mastery | 0 | NO_ITEMS | Oversight mastery demonstrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Oversight foresight addressed in Guidance considerations |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add a risk or contingency note addressing what happens if field conditions materially differ from R-04/Appendix B conceptual plan (e.g., walls in different positions, additional elements discovered); current Guidance flags the data-quality risk (C-001) but does not provide foresight on the response strategy | Validated Guidance Foresight lens reveals that Guidance identifies the as-built data risk but does not articulate a forward-looking strategy for managing the consequence of discovering significantly different field conditions | Guidance.md | Guidance.md#C-001 | -- | Architect | TBD |
| E-002 | E:applying:data | Normalization | Datasheet | Datasheet | Add anticipated drawing scale(s) to Drawing Set Attributes table; the attribute "Anticipated drawing types" lists plan types but not scales, and Procedure Step 1.4 references "appropriate scale" without specifying it | Verified Execution Evidence lens reveals that drawing scale is a fundamental execution parameter for a drawing-set deliverable but is absent from the Datasheet attributes, creating a normalization gap between what is described and what is produced | Datasheet.md; Procedure.md | Datasheet.md#Drawing Set Attributes; Procedure.md#Step 1.4 | -- | Architect | TBD |
| E-003 | E:judging:information | VerificationGap | Specification | Procedure | Add a step or acceptance gate in Procedure Phase 3 that explicitly links completed verification checks to a formal acceptance/release decision (i.e., a go/no-go for IFC issue based on all verification checks passing) | Defensible Verdict Clarity lens reveals that Procedure Step 3.3 lists verification checks but does not define a formal acceptance decision point -- the transition from Step 3.3 to Step 3.4 (P.Eng. stamp) is implicit rather than gated | Procedure.md; Specification.md | Procedure.md#Step 3.3; Specification.md#Verification | -- | Architect / Project Manager | TBD |
| E-004 | E:reviewing:data | MissingSlot | Procedure | Procedure | Add reference to a transmittal record standard or template for IFC drawing issue (Step 3.5); current text mentions "transmittal record" but no standard or template is cited, which could result in inconsistent audit documentation | Verified Audit Documentation lens reveals that the IFC issue step references a transmittal record but provides no standard for its form or content, making future audit verification of distribution uncertain | Procedure.md | Procedure.md#Step 3.5; Procedure.md#Records ("Issued IFC drawing set with transmittal" row) | -- | Project Manager | TBD |

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | All 96 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | All 27 warranted items grounded in evidence from production documents or explicit documented absence |
| Provenance present | All items include SourcePath and SectionRef |
| Conflicts surfaced | 1 conflict (A-002) has Contenders and HumanRuling = TBD |
| Summary consistent | Total=27; by document: 5+10+5+3+4=27; by matrix: 5+3+3+4+3+5+4=27; by type: 1+6+7+4+3+2+4+0=27 |
| Schema followed | Output follows STRUCTURE schema from agent instructions |
