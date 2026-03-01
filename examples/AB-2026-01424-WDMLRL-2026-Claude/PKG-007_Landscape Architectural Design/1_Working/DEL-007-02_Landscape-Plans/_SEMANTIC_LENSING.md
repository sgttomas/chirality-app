# Semantic Lensing Register: DEL-007-02 Landscape Site Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-007_Landscape Architectural Design/1_Working/DEL-007-02_Landscape-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-007-02_Landscape-Plans/_CONTEXT.md
- _STATUS.md — DEL-007-02_Landscape-Plans/_STATUS.md (State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-007-02_Landscape-Plans/_SEMANTIC.md
- Datasheet.md — DEL-007-02_Landscape-Plans/Datasheet.md
- Specification.md — DEL-007-02_Landscape-Plans/Specification.md
- Guidance.md — DEL-007-02_Landscape-Plans/Guidance.md
- Procedure.md — DEL-007-02_Landscape-Plans/Procedure.md
- _REFERENCES.md — DEL-007-02_Landscape-Plans/_REFERENCES.md (read; pointers noted, scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 11
  - Guidance: 4
  - Procedure: 7
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 5  E: 5
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 9
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0 (2 conflicts already recorded in Guidance Conflict Table; no new conflicts discovered)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | P.Eng./LAA stamp ambiguity is prescriptive direction gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | CAD standard mandatory practice not established |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta Building Code clause specifics TBD |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure V-8 addresses P.Eng. stamp audit adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Motor scraper turning radius dimension not specified |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-8 in Procedure cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure addresses performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA review step (Step 7) adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit quality/value criteria for landscape design outcomes |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance P-1 establishes functionality-first value |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table provides checklist-level worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Step 7 internal quality review covers this |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm whether LAA (Landscape Architect) registered seal is required in addition to P.Eng. stamp under Alberta professional practice rules for landscape architectural drawings | REQ-007-02-06 flags P.Eng. requirement with an assumption that LAA seal may also be needed; no prescriptive direction resolves this. Guidance CONF-007-02-01 surfaces same question but no ruling exists. | Specification.md; Guidance.md | Specification#REQ-007-02-06; Guidance#CONF-007-02-01 | -- | PROPOSAL: Project legal/professional team | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add CAD/Drawing Standard value once project CAD standard is established; currently recorded as TBD | The Datasheet and Specification both note CAD standard as TBD. Without a mandatory practice standard for drawing production, downstream consistency is at risk. | Datasheet.md; Specification.md | Datasheet#Attributes (CAD/Drawing Standard); Specification#Standards | -- | PROPOSAL: Project team to establish CAD standard | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify which specific Alberta Building Code clauses apply to landscape site works (current language says "likely applicable; specific clauses location TBD") | The Standards table lists ABC as "ASSUMPTION: likely applicable" which is too weak for compliance determination. A compliance check cannot be executed against an unspecified standard. | Specification.md | Specification#Standards | -- | PROPOSAL: Landscape Architect / Code consultant | TBD |
| A-004 | A:operative:guiding | TBD_Question | Guidance | Guidance | Record TBD: Obtain minimum turning radius dimension for motor scraper-class equipment from civil/structural team or equipment manufacturer data | Guidance C-4 identifies motor scraper turning radius as TBD with no specific dimension in RFP. Without a dimension, driving surface layout cannot be verified for adequacy. | Guidance.md | Guidance#C-4 | -- | PROPOSAL: Civil/structural team or equipment data | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Guidance | Guidance | Add explicit quality/performance objectives for the landscape site plan deliverable (e.g., constructability review criteria, drawing clarity standards for field use) | Guidance provides design principles (P-1 through P-5) focused on regulatory and coordination topics but does not articulate value orientation for the quality of the drawing set itself as a construction document. | Guidance.md | Guidance#Principles | -- | PROPOSAL: Landscape Architect / Project team | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Geotechnical data dependency flagged but no fallback if delayed |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Site survey data adequacy not confirmed |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Drawing scale not established |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data from App B referenced consistently across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (approvals, coordination triggers) are identified in Procedure |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context well-established across Guidance considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope sections in Specification provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | SOW reference inconsistency between docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of scope established in all four docs |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Professional competence requirements addressed via P.Eng./LAA |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No gaps in domain knowledge coverage for stated scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs section in Guidance addresses essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Conflict table and assumptions provide adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers schedule, coordination, and scope trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning in Guidance is principled and traceable to sources |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | RationaleGap | Procedure | Guidance | Add rationale/contingency guidance for what to do if geotechnical report (DEL-008-01) is unavailable or delayed when landscape design must proceed | Procedure Step 5 depends on geotech report but provides no fallback if it is delayed. Guidance C-5 notes the dependency but does not address the schedule risk if geotech is late relative to December 31, 2026 deadline. | Procedure.md; Guidance.md | Procedure#Step 5; Guidance#C-5 | -- | PROPOSAL: Project manager / Landscape Architect | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Procedure | Procedure | Clarify what constitutes "adequate" existing conditions documentation in Prerequisites (Step 1); currently says "Available or underway" for site survey which is vague for a prerequisite | The Procedure prerequisites list site survey as "Available or underway" which does not define a threshold for adequacy. Design development may proceed on insufficient survey data. | Procedure.md | Procedure#Prerequisites | -- | PROPOSAL: Project team | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add drawing scale information once established (currently TBD); this is essential data for a comprehensive drawing set record | Datasheet Attributes lists Drawing Scale(s) as TBD. For a Drawing Set deliverable, scale is a fundamental data attribute that must eventually be recorded. | Datasheet.md | Datasheet#Attributes (Drawing Scale(s)) | -- | PROPOSAL: Landscape Architect | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize SOW reference citations across documents; Datasheet references SOW-0017 and SOW-0076 while Specification references SOW-0020, SOW-0021 and others without a unified reference list | Datasheet lists SOW-0017, SOW-0076 in Identification. Specification cites SOW-0020, SOW-0021. Procedure cites SOW-0075 through SOW-0079. The full set of applicable SOW items is not consolidated in any single location, risking omission during verification. | Datasheet.md; Specification.md; Procedure.md | Datasheet#Identification; Specification#REQ-007-02-02; Procedure#Step 3 | -- | PROPOSAL: Consolidated SOW reference in Datasheet | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Awareness | 1 | HAS_ITEMS | Grading design standards reference TBD |
| C:normative:sufficiency | normative | sufficiency | Qualified Conformance Baseline | 0 | NO_ITEMS | Verification table provides conformance baseline |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Standards table has multiple TBD entries |
| C:normative:consistency | normative | consistency | Standardized Compliance Integrity | 0 | NO_ITEMS | Consistent treatment of compliance requirements across docs |
| C:operative:necessity | operative | necessity | Essential Operational Capability | 0 | NO_ITEMS | Procedure steps establish essential operational capability |
| C:operative:sufficiency | operative | sufficiency | Verified Execution Readiness | 0 | NO_ITEMS | Prerequisites and verification checks adequate |
| C:operative:completeness | operative | completeness | Comprehensive Operational Mastery | 1 | HAS_ITEMS | No record-keeping requirement for coordination meetings |
| C:operative:consistency | operative | consistency | Disciplined Process Coherence | 0 | NO_ITEMS | Procedure steps are sequenced coherently |
| C:evaluative:necessity | evaluative | necessity | Fundamental Quality Valuation | 0 | NO_ITEMS | Functionality-first principle (P-1) covers this |
| C:evaluative:sufficiency | evaluative | sufficiency | Grounded Appraisal Competence | 0 | NO_ITEMS | Verification table criteria are grounded |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation Authority | 0 | NO_ITEMS | Quality review in Step 7 covers holistic check |
| C:evaluative:consistency | evaluative | consistency | Coherent Quality Discipline | 0 | NO_ITEMS | Quality criteria consistent across Specification and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen the Grading Design Standards entry in Standards table from "ASSUMPTION: applicable provincial civil/grading engineering standards; specific reference TBD" to a concrete standard reference | For compulsory regulatory awareness, a normative standard reference must be identifiable. The current assumption-level statement cannot support compliance determination. | Specification.md | Specification#Standards (Grading Design Standards row) | -- | PROPOSAL: Civil Engineer / Landscape Architect | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add Landscape Architects Act (Alberta) / AALA practice standards as a confirmed applicable standard (currently listed as ASSUMPTION) and identify specific clauses relevant to drawing production | The Standards table lists LAA standards as an assumption. For exhaustive compliance scope, all applicable regulatory instruments must be confirmed or explicitly deferred as TBD. | Specification.md | Specification#Standards (Landscape Architects Act row) | -- | PROPOSAL: Landscape Architect / Project legal | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a record-keeping requirement for Step 2 (scope boundary agreement) and Step 4 (civil coordination meetings) to the Records table, or cross-reference the Records section from those steps | The Records table lists "Scope Boundary Coordination Note" and "Civil Coordination Review Record" but Steps 2 and 4 do not explicitly direct the practitioner to create these records. Comprehensive operational mastery requires the procedural steps to reference the records they are expected to produce. | Procedure.md | Procedure#Steps 2 and 4; Procedure#Records | -- | PROPOSAL: Landscape Architect | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Statutory Certainty | 1 | HAS_ITEMS | Alberta Safety Codes cited without clause specificity |
| F:normative:sufficiency | normative | sufficiency | Regulatory Competence Threshold | 0 | NO_ITEMS | P.Eng. requirement establishes regulatory competence threshold |
| F:normative:completeness | normative | completeness | Authoritative Compliance Breadth | 0 | NO_ITEMS | Scope inclusions/exclusions are comprehensive |
| F:normative:consistency | normative | consistency | Principled Regulatory Alignment | 0 | NO_ITEMS | Regulatory references are consistently cited |
| F:operative:necessity | operative | necessity | Critical Execution Certainty | 1 | HAS_ITEMS | IFC drawing content checklist not formalized |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Execution Competence | 0 | NO_ITEMS | Procedure steps demonstrate execution competence path |
| F:operative:completeness | operative | completeness | Total Execution Authority | 0 | NO_ITEMS | Steps 1-8 cover the full execution sequence |
| F:operative:consistency | operative | consistency | Consistent Procedural Discipline | 0 | NO_ITEMS | Procedure is internally consistent |
| F:evaluative:necessity | evaluative | necessity | Essential Merit Discernment | 1 | HAS_ITEMS | No acceptance criteria for drawing quality/readability |
| F:evaluative:sufficiency | evaluative | sufficiency | Sound Appraisal Justification | 0 | NO_ITEMS | Verification approaches in Specification are justified |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Merit Authority | 0 | NO_ITEMS | Verification table covers all requirements |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Coherence | 0 | NO_ITEMS | Verification approaches are consistently structured |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Identify specific Alberta Safety Codes clauses applicable to landscape site works (currently cited without clause-level specificity) | For obligatory statutory certainty, the normative references must be traceable to specific clauses. "Alberta Safety Codes" alone is too broad for compliance verification. | Specification.md | Specification#Standards (Alberta Safety Codes row) | -- | PROPOSAL: Code consultant / Project team | TBD |
| F-002 | F:operative:necessity | VerificationGap | Specification | Procedure | Add a formalized drawing content checklist (or reference to one) that maps each required element from REQ-007-02-01 to specific drawing sheet locations | Specification REQ-007-02-01 lists required site plan content elements but Verification merely says "Internal drawing review checklist against App B." No actual checklist artifact is defined. Critical execution certainty requires a verifiable artifact. | Specification.md; Procedure.md | Specification#Verification (REQ-007-02-01 row); Procedure#Step 7 | -- | PROPOSAL: Landscape Architect | TBD |
| F-003 | F:evaluative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for drawing quality attributes (legibility, scale appropriateness, annotation completeness) beyond content-only verification | The Verification table checks content presence but not drawing quality attributes. Essential merit discernment requires criteria for how well the drawings communicate, not just what they contain. | Specification.md | Specification#Verification | -- | PROPOSAL: Landscape Architect / QA reviewer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Directive Closure | 0 | NO_ITEMS | Guidance principles provide binding directive closure through P-4, P-5 |
| D:normative:applying | normative | applying | Enforced Compliance Standard | 1 | HAS_ITEMS | Verification of driving surface design for heavy equipment lacks measurable criterion |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Verification table supports conformance determination |
| D:normative:reviewing | normative | reviewing | Settled Oversight Verification | 0 | NO_ITEMS | V-8 and V-9 cover oversight verification |
| D:operative:guiding | operative | guiding | Decisive Operational Direction | 0 | NO_ITEMS | Procedure provides clear operational direction |
| D:operative:applying | operative | applying | Validated Practical Implementation | 1 | HAS_ITEMS | No validation method for planting zone framework adequacy |
| D:operative:judging | operative | judging | Settled Capability Judgment | 0 | NO_ITEMS | Verification checks cover capability assessment |
| D:operative:reviewing | operative | reviewing | Confirmed Process Uniformity | 0 | NO_ITEMS | Process is uniform and sequenced |
| D:evaluative:guiding | evaluative | guiding | Committed Quality Direction | 0 | NO_ITEMS | P-1 functionality-first principle provides quality direction |
| D:evaluative:applying | evaluative | applying | Justified Worth Application | 0 | NO_ITEMS | Trade-offs in Guidance justify design approach |
| D:evaluative:judging | evaluative | judging | Definitive Quality Governance | 1 | HAS_ITEMS | No formal sign-off authority defined for quality review |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Merit Soundness | 0 | NO_ITEMS | QA review and verification checks confirm merit |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add measurable acceptance criterion for REQ-007-02-03 verification (driving surface design for heavy equipment); currently says "confirm motor scraper turning radius accommodation" without specifying what dimension or standard to confirm against | Enforced compliance standard requires a measurable threshold. The verification approach references turning radius accommodation but no minimum dimension or reference standard is cited. | Specification.md | Specification#Verification (REQ-007-02-03 row) | -- | PROPOSAL: Civil Engineer to provide turning radius data | TBD |
| D-002 | D:operative:applying | VerificationGap | Specification | Specification | Add verification approach for REQ-007-02-10 (Planting and Restoration Framework) that defines what constitutes adequate spatial framework zones/extents for DEL-007-03 adoption | The Verification table says "Confirm zones/extents in DEL-007-02 are referenced and adopted in DEL-007-03" but this is a downstream check that cannot be performed at DEL-007-02 IFC time. A verifiable criterion at DEL-007-02 issue is needed. | Specification.md | Specification#Verification (REQ-007-02-10 row) | -- | PROPOSAL: Landscape Architect | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Procedure | Procedure | Add explicit sign-off authority (role/person) for Step 7 internal quality review; currently says "conduct internal quality review" without specifying who has authority to approve | Definitive quality governance requires an identified authority for quality sign-off. The Procedure describes the review but does not name or role-define the approver. | Procedure.md | Procedure#Step 7 | -- | PROPOSAL: Project manager / QA lead | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Action Mandate | 1 | HAS_ITEMS | No explicit mandate for when to escalate unresolved coordination conflicts |
| X:guiding:sufficiency | guiding | sufficiency | Competent Directional Validation | 0 | NO_ITEMS | Guidance principles provide sufficient directional validation |
| X:guiding:completeness | guiding | completeness | Exhaustive Stewardship Scope | 0 | NO_ITEMS | Scope coverage is exhaustive in Specification |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Precision | 0 | NO_ITEMS | Directives are harmonized across docs |
| X:applying:necessity | applying | necessity | Enforceable Execution Basis | 1 | HAS_ITEMS | Topsoil stripping responsibility boundary unclear |
| X:applying:sufficiency | applying | sufficiency | Grounded Conformance Proof | 0 | NO_ITEMS | Verification approaches provide conformance proof basis |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Anticipated sheet list not linked to requirements traceability |
| X:applying:consistency | applying | consistency | Standardized Execution Coherence | 0 | NO_ITEMS | Execution steps are consistent |
| X:judging:necessity | judging | necessity | Decisive Governance Determination | 1 | HAS_ITEMS | County approval criteria for DEL-007-01 not defined |
| X:judging:sufficiency | judging | sufficiency | Evidenced Oversight Competence | 0 | NO_ITEMS | Verification and Records sections demonstrate oversight |
| X:judging:completeness | judging | completeness | Total Adjudication Authority | 0 | NO_ITEMS | Conflict table and verification together provide adjudication basis |
| X:judging:consistency | judging | consistency | Coherent Adjudication Precision | 0 | NO_ITEMS | Verification criteria are coherent |
| X:reviewing:necessity | reviewing | necessity | Confirmed Audit Foundation | 1 | HAS_ITEMS | No drawing revision tracking protocol |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Inspection Basis | 0 | NO_ITEMS | Verification checks provide sufficient inspection basis |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Authority | 0 | NO_ITEMS | QA review step is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Alignment | 0 | NO_ITEMS | Audit/review criteria are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Guidance | Guidance | Add escalation protocol for unresolved cross-discipline coordination conflicts (e.g., landscape vs. civil grading disagreements identified in Step 4) | Authoritative action mandate lens reveals no guidance on what happens when Step 4 coordination reveals irreconcilable conflicts between landscape and civil drawings. The Procedure says "resolve any conflicts" but Guidance does not specify escalation path. | Guidance.md; Procedure.md | Guidance#Considerations; Procedure#Step 4 | -- | PROPOSAL: Project manager | TBD |
| X-002 | X:applying:necessity | WeakStatement | Datasheet | Datasheet | Clarify Owner vs. Proponent responsibility boundary for topsoil stripping; Datasheet says "Strip topsoil from all driving surfaces (if not already performed by Owner)" but does not define how to determine what has already been performed | The parenthetical "(if not already performed by Owner)" creates ambiguity about enforceable execution basis. Without a defined method to confirm prior Owner work, the Proponent's scope extent is uncertain. | Datasheet.md | Datasheet#Construction (Topsoil Strip row) | -- | PROPOSAL: Project team to confirm with County | TBD |
| X-003 | X:applying:completeness | Normalization | Specification | Specification | Add requirements-to-sheet traceability mapping in Documentation section linking each REQ to anticipated drawing sheet(s) | Specification lists anticipated drawing sheets and lists requirements separately but does not trace which requirements appear on which sheets. Exhaustive implementation record requires this traceability. | Specification.md | Specification#Documentation | -- | PROPOSAL: Landscape Architect | TBD |
| X-004 | X:judging:necessity | RationaleGap | Guidance | Guidance | Add guidance on what County approval criteria for DEL-007-01 are expected to be, so that DEL-007-02 design development can anticipate approval conditions | REQ-007-02-08 gates IFC on County approval of DEL-007-01 but neither Specification nor Guidance describes what the County evaluates for approval. Without this, DEL-007-02 design development cannot proactively align with approval expectations. | Specification.md; Guidance.md | Specification#REQ-007-02-08; Guidance#P-5 | -- | PROPOSAL: Project manager / County liaison | TBD |
| X-005 | X:reviewing:necessity | MissingSlot | Procedure | Procedure | Add drawing revision tracking protocol (revision numbering, revision history block, revision cloud conventions) to Procedure or reference a project-wide revision control standard | Confirmed audit foundation requires traceable revision history. Procedure Step 6 mentions "revision block" as a drawing element but no protocol governs how revisions are tracked, numbered, or documented across design development iterations. | Procedure.md | Procedure#Step 6 | -- | PROPOSAL: Project team / CAD standard | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 1 | HAS_ITEMS | No Appendix B (Shop) document identified with full title in Datasheet References |
| E:guiding:information | guiding | information | Commanding Guidance Signal | 0 | NO_ITEMS | Guidance provides commanding signals through principles and considerations |
| E:guiding:knowledge | guiding | knowledge | Strategic Leadership Mastery | 0 | NO_ITEMS | Guidance trade-offs section addresses strategic knowledge |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Conflict table and trade-offs provide governance foresight |
| E:applying:data | applying | data | Verified Operational Record | 1 | HAS_ITEMS | Building dimensions sourced only from App B conceptual drawing |
| E:applying:information | applying | information | Actionable Performance Account | 0 | NO_ITEMS | Procedure provides actionable performance steps |
| E:applying:knowledge | applying | knowledge | Applied Deployment Proficiency | 0 | NO_ITEMS | Procedure steps demonstrate deployment proficiency |
| E:applying:wisdom | applying | wisdom | Prudent Deployment Wisdom | 0 | NO_ITEMS | Guidance trade-offs address deployment wisdom |
| E:judging:data | judging | data | Substantiated Judgment Record | 1 | HAS_ITEMS | Verification pass conditions lack measurable thresholds in some cases |
| E:judging:information | judging | information | Clear Adjudication Account | 0 | NO_ITEMS | Verification table provides clear adjudication structure |
| E:judging:knowledge | judging | knowledge | Authoritative Judgment Mastery | 0 | NO_ITEMS | Cross-discipline coordination review provides judgment expertise basis |
| E:judging:wisdom | judging | wisdom | Principled Verdict Insight | 0 | NO_ITEMS | Conflict table with human ruling preserves principled verdict |
| E:reviewing:data | reviewing | data | Documented Examination Record | 1 | HAS_ITEMS | Records table does not include a copy/reference of source documents reviewed |
| E:reviewing:information | reviewing | information | Clear Examination Account | 0 | NO_ITEMS | Procedure verification checks provide clear examination account |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Audit Mastery | 0 | NO_ITEMS | QA review covers integrated audit |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Insight | 1 | HAS_ITEMS | No lessons-learned or feedback mechanism defined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Normalize Appendix B reference: use consistent full document title "AB-2026-01424-Appendix B (Shop).pdf" in both References table and Attributes table citations | Datasheet References table uses "AB-2026-01424-Appendix B (Shop).pdf" but the Attributes table cites "App B (Shop)" without the full document identifier. For an authoritative guidance record, reference identifiers should be consistent. | Datasheet.md | Datasheet#References; Datasheet#Attributes | -- | PROPOSAL: Document control convention | TBD |
| E-002 | E:applying:data | RationaleGap | Multi | Guidance | Add rationale/note that building dimensions (130' x 100' New North Shop, 105' x 40' Old North Shop) are sourced from conceptual Appendix B only and must be confirmed by surveyed/engineered dimensions before IFC | Datasheet and Procedure both cite specific building dimensions from App B (conceptual drawing). These are design-basis dimensions that have not been confirmed by survey or structural engineering. Verified operational record requires acknowledgment of this limitation. | Datasheet.md; Procedure.md | Datasheet#Attributes (Expansion Area); Procedure#Step 3 | -- | PROPOSAL: Structural Engineer / Surveyor | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Add measurable pass/fail thresholds to Verification table entries V-3 and V-4 (currently rely on "transmittal record exists" and "conflict log cleared" without defining what constitutes adequate transmittal or clearance) | Substantiated judgment record requires that verification pass conditions be measurably deterministic. "Drawing transmittal record exists" and "Conflict log cleared or open items documented" are necessary but not sufficient -- they do not define what content the transmittal must contain or what constitutes acceptable open items. | Specification.md | Specification#Verification (REQ-007-02-07 and REQ-007-02-09 rows) | -- | PROPOSAL: QA lead / Project manager | TBD |
| E-004 | E:reviewing:data | VerificationGap | Procedure | Procedure | Add to Records table a record entry for "Source Document Register" or equivalent that documents which source documents (and versions) were reviewed during Step 1 | Documented examination record requires traceability to source documents. The Procedure References section lists required references but the Records table does not require documentation of which versions were actually used as design basis. | Procedure.md | Procedure#Records | -- | PROPOSAL: Document control | TBD |
| E-005 | E:reviewing:wisdom | MissingSlot | Procedure | Guidance | Add a lessons-learned or post-IFC feedback mechanism (e.g., construction feedback loop, field issue tracking) to capture whether the landscape site plans were adequate for construction purposes | Principled audit insight requires a mechanism for the organization to learn from the deliverable's performance in the field. No feedback loop from construction (PKG-018) back to the landscape design team is defined. | Procedure.md; Guidance.md | Procedure#entire document scanned; Guidance#entire document scanned | -- | PROPOSAL: Project manager | TBD |
