# Semantic Lensing Register: DEL-008-02 Preliminary Site Survey

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-02_Preliminary-Survey/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-008-02_Preliminary-Survey/_CONTEXT.md (Deliverable Identity, Scope, Responsibility)
- _STATUS.md — DEL-008-02_Preliminary-Survey/_STATUS.md (State: SEMANTIC_READY, Last Updated: 2026-02-26)
- _SEMANTIC.md — DEL-008-02_Preliminary-Survey/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-008-02_Preliminary-Survey/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md — DEL-008-02_Preliminary-Survey/Specification.md (Scope, Requirements R-001 through R-010, Standards, Verification, Documentation)
- Guidance.md — DEL-008-02_Preliminary-Survey/Guidance.md (Purpose, Principles, Considerations, Trade-offs)
- Procedure.md — DEL-008-02_Preliminary-Survey/Procedure.md (Prerequisites, Steps 1-7, Verification, Records)
- _REFERENCES.md — DEL-008-02_Preliminary-Survey/_REFERENCES.md (Document references R-01, R-07; related deliverables; standards notes)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 3
  - Specification: 12
  - Guidance: 5
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Survey accuracy class and datum not prescribed; weak directive language |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Accuracy class left as TBD in mandatory requirement R-007 |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta Land Surveyors Act compliance path not confirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table in Specification covers audit trail adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | No site safety protocol specifics for active landfill |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure Verification table covers step-level checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure covers retention |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit priority ranking among survey scope elements |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance Trade-offs section addresses value trade-offs |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance section on downstream data integration covers value |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Specification Verification table covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify R-007 with a specific accuracy class or explicit decision gate for accuracy class selection at survey plan stage | R-007 states accuracy "shall be appropriate" without defining what appropriate means; this vagueness could lead to different interpretations by surveyor vs. design team. | Specification.md | R-007 -- Survey Accuracy | -- | Owner / Prime Consultant confirmation | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm target survey accuracy class (e.g., Alberta Order of survey, or project-specific tolerance) with Owner before survey plan submission | The Datasheet lists Survey Accuracy Class as TBD. R-007 in Specification is also TBD. This mandatory attribute lacks a value needed before fieldwork. | Datasheet.md | Attributes table -- Survey Accuracy Class | -- | Owner / Surveyor | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm whether boundary work requires a legal boundary survey under the Alberta Land Surveyors Act, triggering ALS involvement and certification | Specification Standards table notes ALS may be required but leaves it as "Location TBD". Guidance also flags this as needing Owner clarification. Without resolution, compliance path for boundary work is indeterminate. | Specification.md | Standards table -- Alberta Land Surveyors Act | -- | Owner / Legal | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add site-specific health and safety requirements for field work at active landfill (e.g., PPE requirements, site induction protocol, emergency procedures) | Procedure Step 1 mentions "Health and safety considerations for the active landfill site (ASSUMPTION)" but no specific safety protocol is described. Guidance Considerations mentions PPE and safety protocols should be observed but details are absent. | Procedure.md | Step 1 -- Develop and Submit Survey Plan | -- | Proponent HSE / WDMLRL facility management | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add explicit priority ranking for survey scope elements (topographic vs. boundary vs. control vs. existing conditions) to guide resource allocation if schedule is constrained | Guidance Principles list survey-first and control-point-as-asset but do not rank the four survey scope elements by relative priority. If the survey schedule is compressed, the team has no documented basis for prioritizing one scope element over another. | Guidance.md | Principles section | -- | Project Manager / Surveyor | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Horizontal/vertical datum TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Contour interval not specified |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Construction table enumerates all survey elements |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Coordinate system TBD creates consistency risk |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Specification requirements provide essential scope signals |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations provides adequate site context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Four documents together give a comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are consistent in describing scope and purpose |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles section conveys foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure presumes competent surveyor; adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Not relevant as a gap; this is an execution-phase concern |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-document understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Survey timing vs. County earthworks decision not resolved |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance Trade-offs section provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers site context, regulatory, seasonal, and downstream integration |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Trade-off reasoning is internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm horizontal datum (e.g., NAD83 CSRS), vertical datum (e.g., CGVD2013), and coordinate system with Owner and design team | Datasheet Attributes table lists Horizontal Datum, Vertical Datum, and Coordinate System all as TBD. These are essential facts required before fieldwork can begin per R-006. | Datasheet.md | Attributes table -- Horizontal Datum, Vertical Datum, Coordinate System | -- | Owner / design team | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm mapping scale and contour interval with Owner and civil engineer | Datasheet Attributes table lists Mapping Scale / Contour Interval as TBD. Without this, the survey data density cannot be planned and adequacy of evidence for grading design is undetermined. | Datasheet.md | Attributes table -- Mapping Scale / Contour Interval | -- | Owner / civil engineer | TBD |
| B-003 | B:data:consistency | WeakStatement | Specification | Specification | Strengthen R-006 to specify which datum and coordinate system shall be used (or at minimum name the expected default, e.g., NAD83 CSRS / CGVD2013) rather than deferring entirely | R-006 states datum "shall be confirmed with the Owner" but does not name a default or expected datum. This leaves a consistency gap: if datum is not confirmed before fieldwork, data may be collected in an incompatible reference frame. | Specification.md | R-006 -- Coordinate System and Datum | -- | Owner / Surveyor | TBD |
| B-004 | B:wisdom:necessity | WeakStatement | Guidance | Guidance | Clarify the recommended survey timing relative to County earthworks with a decision rule or explicit question to County project manager | Guidance Trade-offs table notes the survey timing vs. County earthworks trade-off but does not recommend a resolution or decision mechanism. The Considerations section says timing "should be confirmed" but the language is non-committal. | Guidance.md | Trade-offs table -- Survey timing vs. County earthworks; Considerations -- Site Context | -- | County project manager | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforced Regulatory Threshold | 1 | HAS_ITEMS | ALS licensing requirement not confirmed for boundary scope |
| C:normative:sufficiency | normative | sufficiency | Certified Mandate Justification | 0 | NO_ITEMS | Specification requirements cite RFP and context sources |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 1 | HAS_ITEMS | No explicit reference to Alberta Surveys Act monument protection |
| C:normative:consistency | normative | consistency | Harmonized Compliance Regime | 0 | NO_ITEMS | Standards table is internally consistent |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Prerequisites section covers readiness requirements |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Execution | 0 | NO_ITEMS | Procedure steps are sufficiently detailed for execution |
| C:operative:completeness | operative | completeness | Comprehensive Delivery Mastery | 0 | NO_ITEMS | Steps 1-7 cover full lifecycle from planning to acceptance |
| C:operative:consistency | operative | consistency | Standardized Process Verification | 0 | NO_ITEMS | Procedure Verification table is consistent with Steps |
| C:evaluative:necessity | evaluative | necessity | Fundamental Merit Assessment | 0 | NO_ITEMS | Guidance Purpose section establishes foundational value |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Expert Valuation | 0 | NO_ITEMS | Expert valuation presumed via surveyor role |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Appraisal | 1 | HAS_ITEMS | No cost/budget considerations documented |
| C:evaluative:consistency | evaluative | consistency | Principled Uniform Evaluation | 0 | NO_ITEMS | Evaluation criteria are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add verification criterion for ALS involvement: specify how boundary survey compliance with Alberta Land Surveyors Act will be verified (e.g., ALS stamp on boundary plan) | Specification Standards table cites the Alberta Land Surveyors Act but the Verification table for R-003 only says "Boundary data shown on survey drawing; ALS stamp if boundary survey required." The conditional "if" leaves it unclear whether ALS involvement is actually required, creating a verification gap. | Specification.md | Standards table -- Alberta Land Surveyors Act; Verification table -- R-003 | -- | Owner / Legal | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add reference to Alberta Surveys Act requirements regarding protection/preservation of existing survey monuments encountered during fieldwork | Specification Standards table references the Alberta Land Surveyors Act and Alberta Surveys Act but does not address obligations regarding existing survey monuments that may be encountered on site. The Alberta Surveys Act governs monument protection. | Specification.md | Standards table -- Alberta Surveys Act | -- | Surveyor / ALS | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration of budget/cost implications for survey scope decisions (e.g., legal boundary survey cost vs. approximate boundary, extended coverage cost) | Guidance Trade-offs table references "higher cost, longer timeline" for legal boundary survey but no explicit cost/budget section exists. Cost is a relevant evaluative dimension for completeness of the worth appraisal. | Guidance.md | Trade-offs table | -- | Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Compliance Standard | 1 | HAS_ITEMS | Digital data file format TBD in R-008 |
| F:normative:sufficiency | normative | sufficiency | Justified Regulatory Competence | 0 | NO_ITEMS | Requirements cite sources adequately |
| F:normative:completeness | normative | completeness | Absolute Mandate Authority | 1 | HAS_ITEMS | Survey plan approval requirement sourced from assumption |
| F:normative:consistency | normative | consistency | Systematic Governance Coherence | 0 | NO_ITEMS | Requirements are mutually consistent |
| F:operative:necessity | operative | necessity | Critical Capability Activation | 1 | HAS_ITEMS | Existing geodetic benchmark availability not confirmed |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Proficiency | 0 | NO_ITEMS | Procedure demonstrates sufficient proficiency for execution |
| F:operative:completeness | operative | completeness | Exhaustive Operational Scope | 0 | NO_ITEMS | Steps 1-7 cover complete operational scope |
| F:operative:consistency | operative | consistency | Disciplined Operational Coherence | 0 | NO_ITEMS | Procedure steps are internally coherent |
| F:evaluative:necessity | evaluative | necessity | Foundational Significance Criterion | 0 | NO_ITEMS | Guidance Purpose establishes significance |
| F:evaluative:sufficiency | evaluative | sufficiency | Proven Appraisal Defensibility | 0 | NO_ITEMS | Guidance Trade-offs section is defensible |
| F:evaluative:completeness | evaluative | completeness | Definitive Quality Accounting | 1 | HAS_ITEMS | No explicit QA/QC plan requirement for survey data |
| F:evaluative:consistency | evaluative | consistency | Transparent Principled Assessment | 0 | NO_ITEMS | Assessment approach is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen R-008 to specify required digital data file formats or define a mechanism for confirming format (e.g., "format to be confirmed with design team and documented in survey plan") | R-008 states "Digital survey data files (format TBD, confirmed with design team)" -- the format is an obligatory compliance element but remains undefined. Without format agreement, data may be unusable by downstream disciplines. | Specification.md | R-008 -- Survey Products / Deliverable Artifacts | -- | Design team lead | TBD |
| F-002 | F:normative:completeness | RationaleGap | Specification | Guidance | Add rationale for R-009 (Owner Approval of Survey Plan) explaining why this requirement exists and what the approval is intended to confirm | R-009 is sourced from "ASSUMPTION -- inferred from Owner approval requirements." The mandate for Owner approval of the survey plan is reasonable but the rationale is entirely assumed rather than grounded in an explicit source. Guidance should explain why this approval gate matters. | Specification.md | R-009 -- Owner Approval of Survey Plan | -- | Project Manager | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a prerequisite step to confirm availability of existing geodetic benchmarks or control network in the vicinity of the site before mobilization | Procedure Step 2 assumes existing geodetic control points can be found ("Identify and locate existing geodetic control points or benchmarks in the vicinity"). No prerequisite confirms their availability. If none exist nearby, the control network approach must change. | Procedure.md | Step 2 -- Mobilize and Establish Control Network; Prerequisites -- Technical Prerequisites | -- | Surveyor | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add a requirement for QA/QC procedures on survey data (e.g., independent check, redundancy analysis, outlier detection) as a verifiable quality accounting measure | Specification Verification table for R-007 references "Closure checks and redundancy analysis documented in survey report" but there is no explicit requirement for a QA/QC plan or protocol. The quality accounting lens suggests this should be a stated requirement, not just a verification approach. | Specification.md | Verification table -- R-007; entire document scanned | -- | Surveyor | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Directed Compliance Closure | 0 | NO_ITEMS | R-009 provides compliance closure pathway via Owner approval |
| D:normative:applying | normative | applying | Enforced Compliance Capability | 0 | NO_ITEMS | Requirements R-001 through R-010 enforce compliance capability |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 1 | HAS_ITEMS | No formal acceptance criteria for survey deliverable |
| D:normative:reviewing | normative | reviewing | Mandated Governance Inspection | 0 | NO_ITEMS | Specification Verification table and Procedure Verification section cover inspection |
| D:operative:guiding | operative | guiding | Mobilized Workflow Orientation | 0 | NO_ITEMS | Procedure Steps 1-7 provide workflow orientation |
| D:operative:applying | operative | applying | Verified Productive Delivery | 1 | HAS_ITEMS | No explicit deliverable review period or turnaround time |
| D:operative:judging | operative | judging | Settled Capability Measurement | 0 | NO_ITEMS | Procedure Verification table measures capabilities at each step |
| D:operative:reviewing | operative | reviewing | Resolved Process Integrity | 0 | NO_ITEMS | Records table ensures process integrity through retention requirements |
| D:evaluative:guiding | evaluative | guiding | Resolved Priority Benchmark | 0 | NO_ITEMS | Addressed under A-005 (priority ranking gap) |
| D:evaluative:applying | evaluative | applying | Justified Value Realization | 0 | NO_ITEMS | Guidance Purpose section connects survey to downstream value |
| D:evaluative:judging | evaluative | judging | Settled Quality Adjudication | 1 | HAS_ITEMS | Owner acceptance criteria for survey products not defined |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Worth Oversight | 0 | NO_ITEMS | Owner acceptance process in Step 7 provides worth oversight |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add formal acceptance criteria for the overall survey deliverable (beyond individual requirement verification) defining what constitutes a conforming preliminary survey | Specification Verification table verifies individual requirements but there is no overarching acceptance criterion for the deliverable as a whole. The "Conclusive Conformance Verdict" lens reveals no single test that confirms the full survey deliverable is conforming. | Specification.md | Verification table -- entire section | -- | Owner / Project Manager | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Specify expected review period and response turnaround for Owner review of survey deliverables in Step 7 | Procedure Step 7 says "Allow review period; respond to review comments" without specifying a duration. This vagueness could create schedule risk given the December 31, 2026 deadline. | Procedure.md | Step 7 -- Deliver Artifacts and Obtain Acceptance | -- | Project Manager / Owner | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add Owner acceptance criteria for survey products (e.g., what the Owner will check, what constitutes rejection, how disputes are resolved) | Specification Verification for R-008 says "All listed artifacts received and reviewed by Owner and design team" but does not define what the Owner is evaluating or what would cause rejection. The quality adjudication lens requires clearer criteria. | Specification.md | Verification table -- R-008 | -- | Owner | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Foundational Directive | 0 | NO_ITEMS | Guidance Principles provide authoritative foundational directives |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Competence | 0 | NO_ITEMS | Guidance is sufficiently justified with source references |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Coverage | 1 | HAS_ITEMS | No guidance on data backup/security during field operations |
| X:guiding:consistency | guiding | consistency | Coherent Guidance Stability | 0 | NO_ITEMS | Guidance is internally coherent and stable |
| X:applying:necessity | applying | necessity | Verified Skill Foundation | 1 | HAS_ITEMS | Surveyor qualifications not specified |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Delivery Competence | 0 | NO_ITEMS | Procedure Steps demonstrate sufficient delivery competence |
| X:applying:completeness | applying | completeness | Exhaustive Execution Accounting | 0 | NO_ITEMS | Procedure covers all execution phases |
| X:applying:consistency | applying | consistency | Stable Output Transparency | 0 | NO_ITEMS | Output requirements are stable and transparent across documents |
| X:judging:necessity | judging | necessity | Binding Threshold Finding | 1 | HAS_ITEMS | Survey closure tolerance not specified |
| X:judging:sufficiency | judging | sufficiency | Justified Capability Verdict | 0 | NO_ITEMS | Verification approaches in Specification are justified |
| X:judging:completeness | judging | completeness | Exhaustive Conformance Record | 0 | NO_ITEMS | Documentation table in Specification lists complete records |
| X:judging:consistency | judging | consistency | Stable Conformance Transparency | 0 | NO_ITEMS | Verification criteria are consistent between Specification and Procedure |
| X:reviewing:necessity | reviewing | necessity | Mandatory Integrity Baseline | 1 | HAS_ITEMS | Terminology inconsistency: "control points" vs. "control stations" |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Inspection Assurance | 0 | NO_ITEMS | Review and inspection processes are justified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Coverage | 0 | NO_ITEMS | Procedure Verification table covers all steps |
| X:reviewing:consistency | reviewing | consistency | Stable Inspection Coherence | 1 | HAS_ITEMS | Record retention periods inconsistent (project + 2yr vs. Owner TBD) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add guidance on data backup and security protocols during field operations (e.g., daily backup of raw field data, secure storage of digital files) | Procedure Step 4 mentions "Download and back up all raw field data" but Guidance provides no directional content on data protection during the field campaign itself. Loss of raw field data before backup would require remobilization. | Guidance.md | entire document scanned; Procedure.md Step 4 | -- | Surveyor / IT | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add a requirement specifying minimum surveyor qualifications (e.g., licensed ALS for boundary work, or CLS/surveyor-in-training under ALS supervision) | No document specifies the required qualifications of the surveyor performing the work. Datasheet identifies "Surveyor" as responsible role but does not define what qualifications that role must hold. This is a verified skill foundation gap. | Specification.md | entire document scanned; Datasheet.md Identification table -- Responsible Role | -- | Owner / Proponent | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add specific closure tolerance or accuracy threshold for control network adjustment (e.g., positional closure ratio, angular closure limit) as a binding verification threshold | Specification Verification for R-007 says "Closure checks and redundancy analysis documented in survey report" but no numeric threshold is defined. Without a binding threshold, there is no objective basis for pass/fail determination. | Specification.md | Verification table -- R-007 | -- | Surveyor / Owner | TBD |
| X-004 | X:reviewing:necessity | Normalization | Multi | Guidance | Normalize terminology: "control points" (Datasheet, Specification, Guidance) vs. "control stations" (Procedure Step 2) -- adopt one term and define it | Procedure Step 2 introduces "primary control stations" and "working control stations" while other documents consistently use "control points." This inconsistency could cause confusion about whether these are the same or different things. | Procedure.md#Step 2; Datasheet.md#Construction table; Specification.md#R-005 | Step 2 -- Mobilize and Establish Control Network; Attributes and Construction tables; R-005 | -- | Surveyor / Guidance vocabulary note | TBD |
| X-005 | X:reviewing:consistency | Normalization | Procedure | Procedure | Harmonize record retention periods: resolve "project duration + 2 years minimum (ASSUMPTION)" vs. "project duration + Owner's records requirements (TBD)" into a single retention policy or clarify the distinction | Procedure Records table uses two different retention periods without explaining the distinction. Some records have "project duration + 2 years minimum (ASSUMPTION)" while others have "project duration + Owner's records requirements (TBD)." The inconsistency risks records being disposed of prematurely. | Procedure.md | Records table | -- | Owner / Proponent | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Record | 0 | NO_ITEMS | Guidance provides authoritative directive content with sources |
| E:guiding:information | guiding | information | Authoritative Steering Signal | 0 | NO_ITEMS | Guidance signals are clear and well-sourced |
| E:guiding:knowledge | guiding | knowledge | Masterful Navigation Authority | 0 | NO_ITEMS | Guidance Principles demonstrate navigation authority for the domain |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 1 | HAS_ITEMS | No foresight on what happens if survey is delayed past design start |
| E:applying:data | applying | data | Verified Execution Evidence | 0 | NO_ITEMS | Procedure produces verifiable execution evidence at each step |
| E:applying:information | applying | information | Informed Delivery Transparency | 0 | NO_ITEMS | Delivery process is transparent through Step 7 |
| E:applying:knowledge | applying | knowledge | Demonstrated Craft Mastery | 0 | NO_ITEMS | Not a document-level gap; craft mastery is execution-phase |
| E:applying:wisdom | applying | wisdom | Prudent Execution Foresight | 0 | NO_ITEMS | Guidance Trade-offs and Procedure Steps cover prudent execution |
| E:judging:data | judging | data | Conclusive Conformance Evidence | 0 | NO_ITEMS | Verification tables provide conformance evidence framework |
| E:judging:information | judging | information | Informed Determination Account | 0 | NO_ITEMS | Verification approaches are informed and accountable |
| E:judging:knowledge | judging | knowledge | Masterful Regulatory Expertise | 1 | HAS_ITEMS | Standards table lacks detail on regulatory requirements |
| E:judging:wisdom | judging | wisdom | Principled Conformance Judgment | 0 | NO_ITEMS | Judgment framework is principled through verification tables |
| E:reviewing:data | reviewing | data | Verified Integrity Evidence | 0 | NO_ITEMS | Records table ensures integrity evidence is retained |
| E:reviewing:information | reviewing | information | Informed Oversight Assurance | 0 | NO_ITEMS | Owner review in Step 7 provides informed oversight |
| E:reviewing:knowledge | reviewing | knowledge | Masterful Inspection Authority | 0 | NO_ITEMS | Not a document-level gap |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 1 | HAS_ITEMS | No consideration of long-term control point preservation |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add foresight guidance on schedule risk: what happens to downstream design if the preliminary survey is delayed, and what minimum survey data would allow design to proceed in parallel | Guidance Principle 1 says "survey should be completed and accepted before detailed design phases proceed" but provides no contingency guidance for delay scenarios. Given the December 31, 2026 hard deadline, the absence of foresight on this risk is a gap. | Guidance.md | Principles -- 1. Survey First, Design After | -- | Project Manager / Prime Consultant | TBD |
| E-002 | E:judging:knowledge | Normalization | Multi | Multi | Standardize the citation of regulatory standards: either provide full legal citations (e.g., RSA 2000, c. A-31.5) for all standards or use a consistent short-form across all documents | Specification Standards table provides formal citations for statutes (RSA 2000, c. A-31.5; RSA 2000, c. S-26) but Guidance and Procedure reference these only by common name ("Alberta Land Surveyors Act"). Consistent citation convention would reduce ambiguity. | Specification.md#Standards table; Guidance.md#Considerations -- Regulatory; Procedure.md#Prerequisites -- Reference Documents | Standards table; Considerations -- Regulatory / Professional; Prerequisites -- Reference Documents Required | -- | Technical writer | TBD |
| E-003 | E:reviewing:wisdom | MissingSlot | Multi | Guidance | Add consideration of long-term control point preservation strategy beyond the immediate project (e.g., whether control points should be registered with a provincial survey control database or shared with the County for future use) | Guidance Principle 2 addresses control points as a "long-duration asset" within the project lifecycle but does not address post-project preservation or registration. For a County-owned facility, the long-term value of a permanent control network extends beyond this project. | Guidance.md | Principles -- 2. Control Points Are a Long-Duration Asset | -- | Owner / Surveyor | TBD |
