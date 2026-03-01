# Semantic Lensing Register: DEL-005-02 Site Grading Plan

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-005_Civil Design/1_Working/DEL-005-02_Site-Grading-Plan/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-005-02_Site-Grading-Plan/_CONTEXT.md (Identification, Description, Anticipated Artifacts)
- _STATUS.md — DEL-005-02_Site-Grading-Plan/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-005-02_Site-Grading-Plan/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-005-02_Site-Grading-Plan/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md — DEL-005-02_Site-Grading-Plan/Specification.md (Scope, Requirements REQ-001 through REQ-010, Standards, Verification)
- Guidance.md — DEL-005-02_Site-Grading-Plan/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-005-02_Site-Grading-Plan/Procedure.md (Prerequisites, Steps Phases 1-4, Verification, Records)
- _REFERENCES.md — DEL-005-02_Site-Grading-Plan/_REFERENCES.md (R-01, R-07)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 2
  - Specification: 10
  - Guidance: 3
  - Procedure: 5
  - Multi: 1
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 1
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Design storm return period lacks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Stormwater design standards TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta Safety Codes -- specific codes TBD |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions addressed via P.Eng. stamp and County approval |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | CAD platform and survey data format not specified |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Phases 1-4 in Procedure adequately cover practical execution |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative acceptance criteria for driving surface load capacity |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal QA review step and verification table present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles provide adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance covers merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification methods align with requirements |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA review step in Procedure covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify applicable stormwater design return period (e.g., 1:10, 1:25, 1:100) per Alberta standards and confirm with County | REQ-001 requires positive drainage for "future storm events" but no design storm return period is prescribed; this is a material design input without which prescriptive direction is incomplete | Specification.md; Guidance.md | Specification#REQ-001; Guidance#Stormwater Design Storm (AMB-001) | -- | Civil Engineer per Alberta standards; County confirmation | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add reference to specific stormwater management standard or guideline that governs design storm selection and drainage sizing | Standards table lists "Stormwater design standards / return period criteria" as TBD; mandatory practice for drainage design lacks a cited governing standard | Specification.md | Specification#Standards | -- | Civil Engineer / PM | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify which specific Alberta Safety Codes apply to site grading works (e.g., Alberta Building Code sections for site drainage, Plumbing Code for storm connections if applicable) | "Alberta Safety Codes Act and associated regulations" is cited as applicable but no specific code sections are identified; compliance determination cannot be performed against an unspecified standard | Specification.md | Specification#Standards | -- | Civil Engineer | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Specify CAD/drafting platform requirements and survey data interchange format (e.g., DWG, LandXML) to remove ambiguity from procedural direction | Procedure lists CAD platform as "ASSUMPTION: Standard civil drafting software... specific platform TBD" and survey data format as "TBD"; this leaves procedural direction ambiguous for execution | Procedure.md | Procedure#Required Personnel and Tools | -- | PM / Civil Engineer | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for driving surface load capacity (e.g., minimum bearing pressure or reference to geotechnical report recommendation) | REQ-005 requires design for heavy equipment weight and turning radius but verification says "specific load criteria TBD -- subject to geotechnical report"; performance assessment lacks a quantitative threshold | Specification.md | Specification#REQ-005 Verification | -- | Civil Engineer (pending DEL-008-01 geotech report) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Existing topographic data completeness unclear |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes well-sourced from R-01 and R-07 |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Utility location data gap |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement sources (survey, geotech) identified consistently |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (positive drainage, neighbour protection, P.Eng.) clear |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided across all four documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages align across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Civil engineering fundamentals well-represented in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Professional judgment deferred to P.Eng. appropriately |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope of required expertise adequately bounded |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | County vs. proponent scope boundary discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable awareness present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential fact: existing site elevation datum and benchmark reference (geodetic or local) used for survey control | No elevation datum or benchmark is identified in Datasheet or Procedure despite grading design being elevation-critical; this is an essential fact for grading plan production | Datasheet.md; Procedure.md | Datasheet#Conditions; Procedure#Step 1.2 | -- | Surveyor (DEL-008-02) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add record of known utility locations within expansion area (or note that none exist / are TBD from survey) | Procedure Step 1.2 mentions "Utility locations (if surveyed)" but Datasheet Conditions section does not record any utility data or note its absence; comprehensive record is incomplete | Datasheet.md; Procedure.md | Datasheet#Conditions; Procedure#Step 1.2 | -- | Surveyor (DEL-008-02) | TBD |
| B-003 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Add rationale for how County-performed bulk cut/fill interfaces with proponent grading design sequencing (e.g., what condition must bulk earthwork be in before proponent design is implementable) | Guidance Principle 4 notes the County/proponent interface but does not explain the acceptance condition for County-completed bulk work; essential discernment about this handoff boundary is missing | Guidance.md | Guidance#Principles, Principle 4 | -- | PM / County representative | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Threshold Mandate | 1 | HAS_ITEMS | Minimum slope threshold not mandated |
| C:normative:sufficiency | normative | sufficiency | Certified Directive Provision | 0 | NO_ITEMS | P.Eng. certification provision addressed |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Adherence | 1 | HAS_ITEMS | Regulatory list incomplete |
| C:normative:consistency | normative | consistency | Calibrated Systematic Uniformity | 0 | NO_ITEMS | Uniform standards approach consistent |
| C:operative:necessity | operative | necessity | Operational Activation Baseline | 0 | NO_ITEMS | Prerequisites table covers activation baseline |
| C:operative:sufficiency | operative | sufficiency | Proven Method Acceptance | 0 | NO_ITEMS | Method steps adequate |
| C:operative:completeness | operative | completeness | Total Workflow Mastery | 0 | NO_ITEMS | Phases 1-4 cover workflow |
| C:operative:consistency | operative | consistency | Coordinated Methodical Stability | 0 | NO_ITEMS | Steps are internally consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Purpose and value articulated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Valuation Judgment | 0 | NO_ITEMS | Trade-offs provide valuation framework |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation Authority | 1 | HAS_ITEMS | No evaluation of erosion control adequacy criteria |
| C:evaluative:consistency | evaluative | consistency | Reliable Valuation Coherence | 0 | NO_ITEMS | Valuation approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add minimum slope requirement as a verifiable threshold (e.g., reference to "minimum 1-2% cross-fall" noted as ASSUMPTION in Guidance Examples, or cite applicable standard) | REQ-001 mandates positive drainage but no minimum slope threshold is specified in Specification; Guidance Examples section notes "1-2% cross-fall" as ASSUMPTION only; an authoritative threshold is absent | Specification.md; Guidance.md | Specification#REQ-001; Guidance#Examples | -- | Civil Engineer per applicable standards | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add municipal development permit requirements (Camrose County bylaws) and Alberta Environment stormwater guidelines to Standards table with confirmed applicability status | Standards table lists Camrose County bylaws, Alberta Building Code, and Alberta Environment guidelines all as ASSUMPTION with "location TBD"; comprehensive regulatory adherence requires confirmation of applicability | Specification.md | Specification#Standards | -- | Civil Engineer / PM | TBD |
| C-003 | C:evaluative:completeness | VerificationGap | Specification | Specification | Add acceptance criteria for erosion and sediment control measures (e.g., type, placement criteria, maintenance during construction) | Erosion control details are listed as a required artifact in Specification Documentation table and Datasheet Construction table but no requirement (REQ) or verification method governs their adequacy | Specification.md; Datasheet.md | Specification#Documentation; Datasheet#Construction | -- | Civil Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Threshold | 1 | HAS_ITEMS | Compaction specification threshold missing |
| F:normative:sufficiency | normative | sufficiency | Structured Compliance Demonstration | 0 | NO_ITEMS | Verification table provides structured demonstration |
| F:normative:completeness | normative | completeness | Exhaustive Prescriptive Authority | 0 | NO_ITEMS | Requirements REQ-001 through REQ-010 cover main scope |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Benchmark | 0 | NO_ITEMS | Requirements consistently reference R-01 source |
| F:operative:necessity | operative | necessity | Validated Readiness Condition | 1 | HAS_ITEMS | DEL-008-01 status gate unclear |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Execution Proficiency | 0 | NO_ITEMS | Steps demonstrate execution path |
| F:operative:completeness | operative | completeness | Full Procedural Dominion | 0 | NO_ITEMS | Procedure phases cover full workflow |
| F:operative:consistency | operative | consistency | Stable Procedural Harmony | 0 | NO_ITEMS | Procedure internally consistent |
| F:evaluative:necessity | evaluative | necessity | Integral Appraisal Verity | 0 | NO_ITEMS | Value case articulated in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal Competence | 0 | NO_ITEMS | Professional judgment framework adequate |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Appraisal Dominion | 1 | HAS_ITEMS | No appraisal of schedule risk from upstream dependencies |
| F:evaluative:consistency | evaluative | consistency | Unified Ethical Valuation | 0 | NO_ITEMS | Ethical framework (P.Eng. responsibility) consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add compaction specification requirement or reference placeholder pending geotechnical report (DEL-008-01) recommendations | Procedure Step 3.6 references "Compaction specifications (per geotechnical recommendations)" but no Specification requirement governs compaction; mandatory compliance threshold for earthwork quality is absent | Specification.md; Procedure.md | Specification#Requirements (absent); Procedure#Step 3.6 | -- | Civil Engineer (pending DEL-008-01) | TBD |
| F-002 | F:operative:necessity | WeakStatement | Procedure | Procedure | Clarify status gate for DEL-008-01: specify whether grading design may commence with preliminary geotech data or must wait for final report issuance | Prerequisites table says DEL-008-01 "Must be complete before subgrade/compaction grading notes finalized" but Step 1.3 says "Receive geotechnical investigation report" without specifying what "complete" means; validated readiness condition is ambiguous | Procedure.md | Procedure#Prerequisites; Procedure#Step 1.3 | -- | PM / Civil Engineer | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration of schedule risk: REQ-010 deadline of December 31, 2026 depends on timely receipt of DEL-008-01 and DEL-008-02; note risk if upstream deliverables are delayed | REQ-010 sets a hard deadline but Guidance does not discuss how upstream dependency delays (geotech, survey, preliminary approval) affect schedule feasibility; exhaustive appraisal of delivery risk is absent | Guidance.md; Specification.md | Guidance#Considerations (absent); Specification#REQ-010 | -- | PM | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Commanding Prescriptive Resolve | 0 | NO_ITEMS | Specification scope and Guidance principles provide commanding direction |
| D:normative:applying | normative | applying | Enforced Conformance Evidence | 1 | HAS_ITEMS | Neighbour drainage verification method weak |
| D:normative:judging | normative | judging | Binding Authoritative Verdict | 0 | NO_ITEMS | County approval gate provides binding verdict mechanism |
| D:normative:reviewing | normative | reviewing | Established Oversight Benchmark | 0 | NO_ITEMS | P.Eng. review and County inspection provisions present |
| D:operative:guiding | operative | guiding | Confirmed Workflow Threshold | 0 | NO_ITEMS | Prerequisites table confirms workflow thresholds |
| D:operative:applying | operative | applying | Verified Action Delivery | 0 | NO_ITEMS | IFC issue steps cover delivery |
| D:operative:judging | operative | judging | Decisive Capability Verdict | 0 | NO_ITEMS | Verification checks table covers capability assessment |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Examination | 0 | NO_ITEMS | Internal QA review step present |
| D:evaluative:guiding | evaluative | guiding | Grounded Principled Conviction | 0 | NO_ITEMS | Guidance Purpose and Principles ground convictions |
| D:evaluative:applying | evaluative | applying | Definitive Worth Enactment | 0 | NO_ITEMS | Trade-offs table enables worth-based decisions |
| D:evaluative:judging | evaluative | judging | Authoritative Valuation Decree | 1 | HAS_ITEMS | No formal acceptance criteria for drawing set completeness |
| D:evaluative:reviewing | evaluative | reviewing | Grounded Quality Examination | 0 | NO_ITEMS | QA review checklist referenced in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-002 verification: specify quantitative method for pre/post drainage comparison (e.g., flow rate calculation, drainage area delineation, or reference to applicable standard) | REQ-002 verification says "Comparison of pre- and post-grading drainage patterns at property boundaries; confirmation in design narrative or drawing notes" but does not specify what constitutes adequate comparison; enforced conformance evidence is weak | Specification.md | Specification#REQ-002 Verification | -- | Civil Engineer | TBD |
| D-002 | D:evaluative:judging | VerificationGap | Specification | Procedure | Add drawing set completeness checklist as a verification artifact: confirm all required artifacts from Documentation table are present before IFC issue | Specification Documentation table lists 8 required artifacts but no verification method confirms all are present in the final set; the valuation of completeness has no formal check | Specification.md; Procedure.md | Specification#Documentation; Procedure#Step 3.7 | -- | Civil Engineer / PM | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Mandate Activation | 1 | HAS_ITEMS | Inspection requirements unclear |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Capability | 0 | NO_ITEMS | Guidance provides justified steering |
| X:guiding:completeness | guiding | completeness | Comprehensive Commanding Dominion | 0 | NO_ITEMS | Cross-document coverage adequate |
| X:guiding:consistency | guiding | consistency | Unified Commanding Alignment | 0 | NO_ITEMS | Documents aligned on key directives |
| X:applying:necessity | applying | necessity | Mandatory Realization Proof | 1 | HAS_ITEMS | County approval record format undefined |
| X:applying:sufficiency | applying | sufficiency | Competent Enforcement Scope | 0 | NO_ITEMS | Enforcement scope adequate for IFC process |
| X:applying:completeness | applying | completeness | Full Compliance Delivery | 0 | NO_ITEMS | Delivery steps cover full IFC process |
| X:applying:consistency | applying | consistency | Harmonized Enforcement Stability | 0 | NO_ITEMS | Enforcement approach consistent |
| X:judging:necessity | judging | necessity | Conclusive Judgment Basis | 0 | NO_ITEMS | Verification table provides judgment basis |
| X:judging:sufficiency | judging | sufficiency | Sufficient Ruling Competence | 0 | NO_ITEMS | Verification responsibilities assigned |
| X:judging:completeness | judging | completeness | Comprehensive Adjudicative Authority | 0 | NO_ITEMS | Requirements each have verification methods |
| X:judging:consistency | judging | consistency | Unified Ruling Alignment | 0 | NO_ITEMS | Verification methods consistently structured |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Drawing revision tracking format TBD |
| X:reviewing:sufficiency | reviewing | sufficiency | Competent Oversight Scope | 0 | NO_ITEMS | Oversight scope adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Authority | 0 | NO_ITEMS | Audit provisions present |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Alignment | 0 | NO_ITEMS | Audit approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | TBD_Question | Procedure | Procedure | Record TBD: Clarify what County inspections are required for site grading and at what milestones (e.g., subgrade inspection before gravel placement) | Procedure Step 4.3 says "Coordinate with County project representative for any required inspections" but does not identify which inspections apply or when; grounded mandate activation for inspections is undefined | Procedure.md | Procedure#Step 4.3 | -- | County representative / PM | TBD |
| X-002 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add specification of County approval record format for DEL-005-01 (e.g., written letter, email confirmation, meeting minutes) | Procedure Step 2.4 says "receive written County project team approval" and Records table says "Written or documented County project team approval" but acceptable format is not specified; mandatory realization proof format is undefined | Procedure.md | Procedure#Step 2.4; Procedure#Records | -- | PM / County representative | TBD |
| X-003 | X:reviewing:necessity | Normalization | Multi | Multi | Normalize drawing revision tracking: Procedure Records says "Drawing revision history tracked on drawing title block or revision log" -- clarify whether both are required or either suffices, and align with Specification Documentation table | Procedure Records section and Specification Documentation table both reference drawing outputs but revision tracking method is stated loosely ("or"); essential audit foundation requires a definitive record-keeping standard | Procedure.md; Specification.md | Procedure#Records; Specification#Documentation | -- | PM / Civil Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Directive Record | 0 | NO_ITEMS | Directive records well-sourced |
| E:guiding:information | guiding | information | Coherent Leadership Narrative | 0 | NO_ITEMS | Guidance provides coherent narrative |
| E:guiding:knowledge | guiding | knowledge | Integrated Directorial Command | 0 | NO_ITEMS | Integration of knowledge sources adequate |
| E:guiding:wisdom | guiding | wisdom | Panoramic Strategic Foresight | 1 | HAS_ITEMS | Foresight for post-construction warranty obligations |
| E:applying:data | applying | data | Verified Conformance Record | 0 | NO_ITEMS | Conformance records defined |
| E:applying:information | applying | information | Coordinated Delivery Narrative | 0 | NO_ITEMS | Delivery narrative coherent across documents |
| E:applying:knowledge | applying | knowledge | Proficient Conformance Command | 0 | NO_ITEMS | Conformance knowledge adequate |
| E:applying:wisdom | applying | wisdom | Resolute Delivery Insight | 0 | NO_ITEMS | Delivery insight adequate |
| E:judging:data | judging | data | Decisive Adjudicative Record | 0 | NO_ITEMS | Adjudicative records addressed |
| E:judging:information | judging | information | Coherent Verdict Narrative | 0 | NO_ITEMS | Verdict methods coherent |
| E:judging:knowledge | judging | knowledge | Proficient Judicial Command | 0 | NO_ITEMS | Judicial knowledge adequate |
| E:judging:wisdom | judging | wisdom | Authoritative Judicial Foresight | 0 | NO_ITEMS | Judicial foresight adequate via verification table |
| E:reviewing:data | reviewing | data | Substantiated Examination Record | 1 | HAS_ITEMS | QA review record format TBD |
| E:reviewing:information | reviewing | information | Coherent Examination Narrative | 0 | NO_ITEMS | Examination narrative coherent |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Examination Command | 0 | NO_ITEMS | Examination knowledge adequate |
| E:reviewing:wisdom | reviewing | wisdom | Panoramic Oversight Foresight | 0 | NO_ITEMS | Oversight foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add consideration of post-construction warranty obligations: Datasheet notes 2-year warranty period (R-01 section 2.10.2) but Guidance does not discuss implications for grading design durability or maintenance access | Datasheet records a 2-year warranty period but Guidance and Specification do not address how grading design should account for warranty-period maintenance or durability expectations; panoramic strategic foresight is incomplete | Datasheet.md; Guidance.md | Datasheet#Attributes (Warranty Period); Guidance#Considerations (absent) | -- | Civil Engineer / PM | TBD |
| E-002 | E:reviewing:data | TBD_Question | Procedure | Procedure | Record TBD: Define internal QA review record format (e.g., checklist template, reviewer sign-off form) for substantiated examination record | Procedure Records table lists "Internal QA review record" as "ASSUMPTION: Completed QA checklist or reviewer sign-off (format TBD per project quality plan)"; without a defined format, substantiated examination records cannot be produced | Procedure.md | Procedure#Records | -- | PM / Quality Manager | TBD |
