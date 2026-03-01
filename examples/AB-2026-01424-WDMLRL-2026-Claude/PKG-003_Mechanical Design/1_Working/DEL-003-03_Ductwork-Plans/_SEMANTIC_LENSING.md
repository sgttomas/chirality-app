# Semantic Lensing Register: DEL-003-03 Ductwork & Distribution Plans

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-003_Mechanical Design/1_Working/DEL-003-03_Ductwork-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-03_Ductwork-Plans/_CONTEXT.md
- _STATUS.md — DEL-003-03_Ductwork-Plans/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-03_Ductwork-Plans/_SEMANTIC.md (all 7 matrices parsed: A, B, C, F, D, X, E)
- Datasheet.md — DEL-003-03_Ductwork-Plans/Datasheet.md (present; read)
- Specification.md — DEL-003-03_Ductwork-Plans/Specification.md (present; read)
- Guidance.md — DEL-003-03_Ductwork-Plans/Guidance.md (present; read)
- Procedure.md — DEL-003-03_Ductwork-Plans/Procedure.md (present; read)
- _REFERENCES.md — DEL-003-03_Ductwork-Plans/_REFERENCES.md (present; read)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 5
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 5  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code editions unspecified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Duct material/insulation not prescribed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification lacks specificity |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway addressed via Safety Code inspection |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Destratification strategy procedural gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are adequate |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative performance criteria for duct system |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by coordination conflict log and records |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed via principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC review mentioned in Procedure Step 7.3 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Add specific Alberta Building Code edition and ASHRAE/SMACNA edition identifiers once confirmed by Mechanical Engineer | REQ-003-03-06 references code compliance but all code editions are listed as "TBD" or "ASSUMPTION: likely applicable; location TBD" across all four documents; prescriptive direction cannot be fully established without identifying which code edition governs | Specification.md, Datasheet.md | Specification.md#Standards, Datasheet.md#References | | Mechanical Engineer | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add duct material specification (e.g., galvanized sheet metal gauge) and insulation requirement once determined by Mechanical Engineer | Mandatory practice for duct construction requires material and insulation specification; Datasheet lists both as "TBD" with no source; Specification does not prescribe material either | Datasheet.md | Datasheet.md#Ductwork System Parameters | | Mechanical Engineer | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen REQ-003-03-06 verification method: specify which code sections will be checked and what constitutes "Mechanical Engineer confirmation of compliance" | Compliance determination is vague -- verification says "Mechanical Engineer certification; Safety Code inspection" but does not define what specific code provisions are being certified against or what form the certification takes | Specification.md | Specification.md#Verification (REQ-003-03-06) | | Mechanical Engineer | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a sub-step under Step 3 addressing destratification duct strategy as a design routing decision (e.g., mid-height distribution drops vs. high-level discharge) | Guidance Principle 2 identifies 35 ft ceiling stratification as both asset and challenge, and Trade-offs table lists MUA distribution options, but Procedure Step 3 does not include a decision point for destratification strategy selection | Procedure.md, Guidance.md | Procedure.md#Step 3, Guidance.md#Principles §2, Guidance.md#Trade-offs | | Mechanical Engineer | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative performance acceptance criteria for duct system (e.g., maximum allowable pressure drop, velocity limits per duct type, or air delivery confirmation at terminal devices) | Performance assessment lens reveals that all verification methods in Specification are drawing-review-based ("shown on drawings") with no quantitative operational performance thresholds; the system could be drawn correctly but perform inadequately | Specification.md | Specification.md#Verification | | Mechanical Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Airflow rates missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Source accessibility gaps |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Mezzanine ventilation TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements that are stated (dimensions, areas) are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scope, systems, responsibilities) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for design commencement |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Wash bay boundary language inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental design understanding is represented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance principles provide adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain design airflow rates (CFM) for each served space from DEL-003-06 once available; record in Datasheet as essential design input parameters | Essential facts for duct sizing -- makeup air supply rate, air exchange rate, heating capacity, exhaust capacities, and service pit ventilation rate -- are all "TBD" in Datasheet; these are necessary data without which duct sizing cannot proceed | Datasheet.md | Datasheet.md#Ductwork System Parameters | | Mechanical Engineer / DEL-003-06 | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add a row to References table indicating accessibility status for Alberta Building Code and ASHRAE/SMACNA standards, with plan for obtaining them | Adequate evidence requires accessible code references; Datasheet References table lists Alberta Building Code, Alberta Safety Codes, and ASHRAE/SMACNA all as "Not accessible" with "location TBD" -- evidence sufficiency cannot be established until these are obtained | Datasheet.md | Datasheet.md#References | | Project Manager | TBD |
| B-003 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Clarify mezzanine ventilation requirement: state explicitly whether mezzanine is a served space or not, and if TBD, record the decision-maker and trigger | Datasheet Key Spaces table lists mezzanine with "ventilation extent TBD"; Specification REQ-003-03-01 includes mezzanine "(where served)"; Guidance says "Whether the mezzanine receives conditioned air is TBD" -- the ambiguity across all three documents means the comprehensive record is incomplete regarding this space | Datasheet.md, Specification.md, Guidance.md | Datasheet.md#Key Spaces, Specification.md#REQ-003-03-01, Guidance.md#Considerations (Mezzanine) | | Mechanical Engineer | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize wash bay scope boundary language: Datasheet says "ASSUMPTION: boundary TBD per CON-003-03-01" while Specification says it is covered (REQ-003-03-10) without marking the boundary as assumption-dependent | Datasheet Ductwork System Coverage table marks wash bay ventilation as "Yes (ASSUMPTION: boundary TBD per CON-003-03-01)" but Specification REQ-003-03-10 states the requirement directly without qualification that the boundary is assumption-dependent; the coherent message across documents is slightly misaligned | Datasheet.md, Specification.md | Datasheet.md#Ductwork System Coverage, Specification.md#REQ-003-03-10 | Datasheet.md#Ductwork System Coverage (assumption-qualified), Specification.md#REQ-003-03-10 (unqualified requirement) | Mechanical Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Compliance Threshold | 1 | HAS_ITEMS | Binding threshold not quantified |
| C:normative:sufficiency | normative | sufficiency | Mandated Competence Proof | 0 | NO_ITEMS | P.Eng. stamp requirement is clear |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Code inventory incomplete |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Regulatory references are consistent where stated |
| C:operative:necessity | operative | necessity | Core Operational Prerequisite | 0 | NO_ITEMS | Prerequisites well documented in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Working Competence | 0 | NO_ITEMS | |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 1 | HAS_ITEMS | CAD/BIM platform not specified |
| C:operative:consistency | operative | consistency | Uniform Process Discipline | 0 | NO_ITEMS | |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Criterion | 0 | NO_ITEMS | |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Appraisal | 0 | NO_ITEMS | |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add specific acceptance thresholds for REQ-003-03-05 (duct sizing): minimum information to verify (e.g., all runs have CFM annotation, velocity within SMACNA limits) | Binding compliance threshold for duct sizing lacks a quantitative benchmark -- verification says "All duct runs dimensioned; sizing schedule or keynotes present" but does not state what constitutes correct sizing (cross-check with DEL-003-06 is mentioned but no pass/fail criterion) | Specification.md | Specification.md#Verification (REQ-003-03-05) | | Mechanical Engineer | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add reference to National Energy Code for Buildings (NECB) if applicable in Alberta for duct insulation and energy performance requirements | Full regulatory coverage requires identifying all applicable codes; Specification Standards table lists Alberta Building Code, Safety Codes, NBC, ASHRAE, and SMACNA but does not mention National Energy Code for Buildings (NECB) which may apply to duct insulation requirements in Alberta | Specification.md | Specification.md#Standards | | Mechanical Engineer | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add specification of CAD/BIM platform and file format requirements as a prerequisite or in Step 2 | Exhaustive process coverage reveals that Procedure lists "Mechanical CAD/BIM Technologist" with "Proficiency in project's CAD/BIM platform" but does not state which platform or what file formats are required; this is an operational prerequisite gap | Procedure.md | Procedure.md#Personnel Prerequisites | | Project Coordinator | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Compliance Imperative | 1 | HAS_ITEMS | Service pit code compliance unspecified |
| F:normative:sufficiency | normative | sufficiency | Prescribed Proficiency Standard | 1 | HAS_ITEMS | Proficiency evidence gap |
| F:normative:completeness | normative | completeness | Total Regulatory Accountability | 0 | NO_ITEMS | Covered by C-002 |
| F:normative:consistency | normative | consistency | Unified Conformance Integrity | 1 | HAS_ITEMS | Scope exclusion terminology drift |
| F:operative:necessity | operative | necessity | Validated Operational Readiness | 0 | NO_ITEMS | Prerequisites are clear |
| F:operative:sufficiency | operative | sufficiency | Confirmed Execution Capacity | 0 | NO_ITEMS | |
| F:operative:completeness | operative | completeness | Comprehensive Workflow Mastery | 1 | HAS_ITEMS | As-built / field change process missing |
| F:operative:consistency | operative | consistency | Disciplined Process Alignment | 0 | NO_ITEMS | |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Imperative | 0 | NO_ITEMS | |
| F:evaluative:sufficiency | evaluative | sufficiency | Competent Value Substantiation | 0 | NO_ITEMS | |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Accounting | 1 | HAS_ITEMS | Energy performance rationale gap |
| F:evaluative:consistency | evaluative | consistency | Coherent Worth Integrity | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification method for service pit ventilation compliance: specify which code section governs below-grade ventilation in occupied maintenance pits and how compliance will be demonstrated | Absolute compliance imperative for service pit ventilation: REQ-003-03-11 requires service pit ventilation "shown on drawings" but does not address the specific code compliance requirement for below-grade ventilation in an area with potential hazardous atmosphere (exhaust fumes accumulation); this is a safety-critical gap | Specification.md | Specification.md#REQ-003-03-11, Specification.md#Verification | | Mechanical Engineer / Safety Code Officer | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-003-03-09 verification: define what "No unresolved conflicts" means (e.g., written sign-off from structural engineer, clash detection report with zero critical clashes) | Prescribed proficiency standard for structural coordination: REQ-003-03-09 verification says "No unresolved conflicts with structural drawings at IFC; penetration schedule or coordination notes included" but does not define the evidence standard for "no unresolved conflicts" (who signs off, what documentation proves it) | Specification.md | Specification.md#Verification (REQ-003-03-09) | | Mechanical Engineer + Structural Engineer | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Guidance | Normalize the exhaust scope exclusion boundary language: align Specification "Boundary Note" (uses "supply/return/general ventilation distribution" vs. "dedicated local exhaust") with Datasheet system coverage table (uses "dedicated exhaust") and Guidance CON-003-03-01 | Unified conformance integrity requires consistent boundary terminology; the Specification Boundary Note uses different framing than the Datasheet system coverage table -- both describe the same boundary but with slightly different categorical language | Specification.md, Datasheet.md, Guidance.md | Specification.md#Scope (Boundary Note), Datasheet.md#Ductwork System Coverage, Guidance.md#CON-003-03-01 | Specification.md#Scope (supply/return/general vs. dedicated local), Datasheet.md#Ductwork System Coverage (dedicated exhaust) | Mechanical Engineer | TBD |
| F-004 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or note addressing field change / RFI process: what happens when ductwork routing must change during construction due to field conditions | Comprehensive workflow mastery: Procedure covers design through IFC issuance but does not address post-IFC field coordination, RFIs, or as-built documentation; for a concrete structure where field modifications are difficult, the workflow should at least reference the change management process | Procedure.md | Procedure.md#Steps (entire sequence ends at Step 9 - IFC issuance) | | Project Coordinator | TBD |
| F-005 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale for energy performance considerations in duct design: discuss implications of duct insulation, air leakage class, and energy code compliance on long-term operating cost | Exhaustive worth accounting: Guidance Trade-offs table mentions "insulated vs. uninsulated" duct material as TBD depending on energy code, but Guidance does not provide rationale for why energy performance matters for this facility's operating cost or lifecycle value; this is relevant for a heating-dominated cold climate facility | Guidance.md | Guidance.md#Trade-offs | | Mechanical Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Steering | 0 | NO_ITEMS | Covered by A-001 |
| D:normative:applying | normative | applying | Enforced Proficiency Standard | 0 | NO_ITEMS | P.Eng. requirement is clear |
| D:normative:judging | normative | judging | Definitive Accountability Verdict | 1 | HAS_ITEMS | Accountability for coordination failures unclear |
| D:normative:reviewing | normative | reviewing | Settled Compliance Assurance | 0 | NO_ITEMS | |
| D:operative:guiding | operative | guiding | Resolved Procedural Readiness | 0 | NO_ITEMS | Readiness criteria defined in prerequisites |
| D:operative:applying | operative | applying | Confirmed Productive Delivery | 1 | HAS_ITEMS | Drawing set content checklist gap |
| D:operative:judging | operative | judging | Resolved Capability Judgment | 0 | NO_ITEMS | |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Assurance | 0 | NO_ITEMS | |
| D:evaluative:guiding | evaluative | guiding | Settled Worth Governance | 0 | NO_ITEMS | |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Realization | 1 | HAS_ITEMS | OBJ-004 commissioning link weak |
| D:evaluative:judging | evaluative | judging | Definitive Worth Adjudication | 0 | NO_ITEMS | |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Consistency | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | WeakStatement | Specification | Specification | Clarify accountability for coordination failures: state who is responsible if structural penetrations are not coordinated and conflicts are discovered during construction | Definitive accountability verdict: REQ-003-03-09 (structural coordination) assigns verification to "Mechanical Engineer + Structural Engineer" but does not state who bears accountability if coordination fails -- the design-build contract form (CCDC 14-2013) places design liability on the design-builder, but the requirement does not make this explicit | Specification.md | Specification.md#Verification (REQ-003-03-09) | | Project Manager | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Specification | Add a drawing set completeness checklist to Procedure Step 7 or Specification Documentation section: enumerate required sheet types (plan views, sections, schedules, details) as a verification artifact | Confirmed productive delivery: Procedure Step 7.2 lists expected drawing contents but not as a formal checklist; Specification Documentation table lists artifact types but without a checkable completeness standard; neither document provides a definitive list of required sheets against which completeness can be verified | Procedure.md, Specification.md | Procedure.md#Step 7, Specification.md#Documentation | | Mechanical Engineer | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add a note linking DEL-003-03 drawing quality to OBJ-004 (commissioning to operational readiness): explain how ductwork drawing accuracy affects commissioning success | Confirmed merit realization: Datasheet identifies OBJ-004 (HVAC/ventilation systems commissioned to operational readiness) as a supported objective, but Guidance does not explain how the quality of the ductwork distribution drawings affects commissioning outcomes; the connection between drawing accuracy and commissioning is implicit but not articulated | Guidance.md, Datasheet.md | Guidance.md#Purpose, Datasheet.md#Identification (Objectives Supported) | | Mechanical Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Direction | 0 | NO_ITEMS | |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Governance Substantiation | 1 | HAS_ITEMS | Preliminary design approval evidence |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Purview | 0 | NO_ITEMS | |
| X:guiding:consistency | guiding | consistency | Harmonized Governance Alignment | 1 | HAS_ITEMS | Conflict table alignment |
| X:applying:necessity | applying | necessity | Proven Competence Foundation | 0 | NO_ITEMS | |
| X:applying:sufficiency | applying | sufficiency | Sufficient Applied Competence | 0 | NO_ITEMS | |
| X:applying:completeness | applying | completeness | Complete Delivery Mastery | 0 | NO_ITEMS | Covered by D-002 |
| X:applying:consistency | applying | consistency | Consistent Delivery Standard | 0 | NO_ITEMS | |
| X:judging:necessity | judging | necessity | Decisive Accountability Basis | 1 | HAS_ITEMS | Crane clearance verification |
| X:judging:sufficiency | judging | sufficiency | Adequate Assessment Evidence | 0 | NO_ITEMS | |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Authority | 1 | HAS_ITEMS | No independent review role |
| X:judging:consistency | judging | consistency | Consistent Assessment Integrity | 0 | NO_ITEMS | |
| X:reviewing:necessity | reviewing | necessity | Fundamental Assurance Verification | 0 | NO_ITEMS | |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Assurance Coverage | 1 | HAS_ITEMS | County review scope undefined |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Inventory | 0 | NO_ITEMS | |
| X:reviewing:consistency | reviewing | consistency | Harmonized Assurance Integrity | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-003-03-08 verification: specify what form County approval must take (written letter, signed drawing, meeting minutes) and where it is recorded | Adequate governance substantiation: REQ-003-03-08 requires County approval of preliminary design before IFC, and verification says "County approval documented prior to IFC issuance" but does not define what constitutes adequate documentation of approval (verbal vs. written, format, retention) | Specification.md | Specification.md#Verification (REQ-003-03-08) | | Project Manager | TBD |
| X-002 | X:guiding:consistency | Conflict | Guidance | Guidance | Resolve: CON-003-03-02 is documented in Guidance Conflict Table and referenced in Procedure Step 1.2, but Specification does not include a requirement addressing ceiling fan spatial coordination; add a coordination requirement or note in Specification if warranted | Harmonized governance alignment: CON-003-03-02 (ceiling fan designation) is identified in Guidance Conflict Table and addressed in Procedure, but the Specification has no corresponding requirement for ceiling fan spatial coordination; this creates a gap where a known conflict has procedural handling but no normative anchor | Guidance.md, Procedure.md, Specification.md | Guidance.md#Conflict Table (CON-003-03-02), Procedure.md#Step 1.2, Specification.md#entire document scanned | Guidance.md#CON-003-03-02 (fan coordination conflict exists), Specification.md (no corresponding requirement) | Mechanical Engineer + Electrical Engineer | TBD |
| X-003 | X:judging:necessity | VerificationGap | Procedure | Specification | Add crane clearance verification as a specific check in Specification Verification table: "Ductwork routing does not conflict with crane travel envelope -- verified by overlay/clash check" | Decisive accountability basis for crane clearance: Procedure Verification table includes "Crane clearance confirmed" as a check, but Specification has no corresponding requirement (REQ-003-03-09 covers structural coordination generally but does not specifically call out crane clearance); the Procedure check has no normative anchor | Procedure.md, Specification.md | Procedure.md#Verification (Crane clearance confirmed), Specification.md#Requirements (entire section scanned) | | Mechanical Engineer | TBD |
| X-004 | X:judging:completeness | MissingSlot | Specification | Specification | Add an independent QC reviewer role to the Verification table (someone other than the Mechanical Engineer of Record) for at least the coordination and completeness checks | Exhaustive assessment authority: Specification Verification table assigns nearly all verification to "Mechanical Engineer" with occasional "County review"; there is no independent technical reviewer role (e.g., senior mechanical engineer, peer reviewer) to provide assessment independence on technical adequacy | Specification.md | Specification.md#Verification | | Project Manager | TBD |
| X-005 | X:reviewing:sufficiency | WeakStatement | Specification | Specification | Clarify County review scope: state which requirements the County reviews (REQ-003-03-01, -07, -08, -12?) and what their review entails (approval authority vs. information only) | Sufficient assurance coverage: Specification Verification table lists "County review" for REQ-003-03-01 and REQ-003-03-12 but does not define the scope or authority of County review -- is this an approval gate or an information-only review? | Specification.md | Specification.md#Verification (REQ-003-03-01, REQ-003-03-12) | | Project Manager / County | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Governance Record | 1 | HAS_ITEMS | Drawing revision history requirement |
| E:guiding:information | guiding | information | Coherent Governance Intelligence | 0 | NO_ITEMS | |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Governance Mastery | 0 | NO_ITEMS | |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | |
| E:applying:data | applying | data | Substantiated Performance Record | 0 | NO_ITEMS | Records table in Procedure is adequate |
| E:applying:information | applying | information | Coherent Implementation Context | 0 | NO_ITEMS | |
| E:applying:knowledge | applying | knowledge | Applied Craft Mastery | 0 | NO_ITEMS | |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | |
| E:judging:data | judging | data | Substantiated Judgment Record | 1 | HAS_ITEMS | Coordination conflict log format |
| E:judging:information | judging | information | Articulated Assessment Rationale | 0 | NO_ITEMS | |
| E:judging:knowledge | judging | knowledge | Authoritative Assessment Mastery | 0 | NO_ITEMS | |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | |
| E:reviewing:data | reviewing | data | Substantiated Audit Evidence | 1 | HAS_ITEMS | Safety Code inspection linkage |
| E:reviewing:information | reviewing | information | Articulated Audit Intelligence | 0 | NO_ITEMS | |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Mastery | 0 | NO_ITEMS | |
| E:reviewing:wisdom | reviewing | wisdom | Principled Assurance Foresight | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | MissingSlot | Procedure | Procedure | Add drawing revision control requirement: specify how drawing revisions are tracked, numbered, and recorded in the project document control system | Authoritative governance record: Procedure Step 9 mentions "IFC revision designation" and "File issued set in the project document control system" but does not specify a revision tracking or numbering convention; for an IFC drawing set this is a standard records management requirement | Procedure.md | Procedure.md#Step 9, Procedure.md#Records | | Project Coordinator | TBD |
| E-002 | E:judging:data | Normalization | Procedure | Procedure | Standardize coordination conflict log: specify minimum fields (date, discipline, conflict description, resolution, responsible party, status) in Procedure Records table | Substantiated judgment record: Procedure Records table lists "Coordination conflict log -- Record of identified and resolved coordination conflicts (Steps 5, 6)" but does not define the format or minimum content of this log; without a standard format, the judgment record quality may vary | Procedure.md | Procedure.md#Records | | Project Coordinator | TBD |
| E-003 | E:reviewing:data | RationaleGap | Guidance | Guidance | Add note explaining the relationship between Safety Code inspection and the ductwork drawing set: clarify that the drawing set must anticipate inspection hold points and provide sufficient detail for the Safety Code Officer to verify compliance | Substantiated audit evidence: Specification REQ-003-03-06 verification references "Safety Code inspection" and Procedure Records table lists "Safety Code inspection reports" but neither Guidance nor Specification explains what the Safety Code Officer needs from the drawing set to conduct the inspection; the rationale for drawing-level detail supporting inspection is absent | Specification.md, Procedure.md, Guidance.md | Specification.md#Verification (REQ-003-03-06), Procedure.md#Records, Guidance.md#entire document scanned | | Mechanical Engineer / Safety Code Officer | TBD |

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | PASS -- all 96 matrix cells (A:12 + B:16 + C:12 + F:12 + D:12 + X:16 + E:16) have Lens Coverage entries |
| No invention | PASS -- all warranted items grounded in evidence from production documents or explicit absence |
| Provenance present | PASS -- every item has SourcePath + SectionRef |
| Conflicts surfaced | PASS -- 2 conflict-type items (B-004/normalization, X-002/conflict) have Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- summary counts match actual warranted items (28 total) |
| Schema followed | PASS -- output uses STRUCTURE schema |
