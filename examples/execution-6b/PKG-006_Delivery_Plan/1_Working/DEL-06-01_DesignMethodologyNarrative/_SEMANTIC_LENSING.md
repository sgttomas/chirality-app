# Semantic Lensing Register: DEL-06-01 Design Methodology Narrative

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-006_Delivery_Plan/1_Working/DEL-06-01_DesignMethodologyNarrative
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-06-01_DesignMethodologyNarrative/_CONTEXT.md (DEL-06-01, PKG-006, SOW-0008, OBJ-002)
- _STATUS.md -- DEL-06-01_DesignMethodologyNarrative/_STATUS.md (Current State: SEMANTIC_READY; last updated 2026-02-17)
- _SEMANTIC.md -- DEL-06-01_DesignMethodologyNarrative/_SEMANTIC.md (Matrices A, B, C, F, D, K, X, E parsed)
- Datasheet.md -- DEL-06-01_DesignMethodologyNarrative/Datasheet.md (present, read)
- Specification.md -- DEL-06-01_DesignMethodologyNarrative/Specification.md (present, read)
- Guidance.md -- DEL-06-01_DesignMethodologyNarrative/Guidance.md (present, read)
- Procedure.md -- DEL-06-01_DesignMethodologyNarrative/Procedure.md (present, read)
- _REFERENCES.md -- DEL-06-01_DesignMethodologyNarrative/_REFERENCES.md (present, read)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 2  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | RFP 7.1 exact text never directly accessed; prescriptive direction is assumption-based |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | NBCC/ABC edition TBD weakens mandatory practice grounding |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach for R-004 Addenda line-by-line check lacks defined pass/fail threshold |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit lens satisfied by Verification table in Specification and Step 9 checklist in Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-10 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Team roster prerequisite is TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Step 9 checklist and Verification table cover performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification section in Procedure covers process audit adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section and P-001 through P-006 orient value well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | EX-001 through EX-004 demonstrate merit application through examples |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scoring weight (3 of 10 pts) and evaluation criteria well established across documents |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA/QC at each phase milestone is well-defined in Procedure Step 6 and Specification R-008 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Multi | Datasheet | TBD: Obtain and review exact text of RFP Section 7.1 to confirm all sub-requirements are correctly derived; current requirements are assumption-based | All four documents note that RFP Section 7.1 exact text has not been directly accessed; prescriptive direction is reconstructed from decomposition references. If the actual text contains additional sub-requirements, the documents may be incomplete. | Datasheet.md, Specification.md, Guidance.md | Datasheet.md#Notes (ASSUMPTION note); Specification.md#Notes (ASSUMPTION note) | -- | RFP Section 7.1 source text | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which edition of NBCC and Alberta Building Code applies; currently listed as "TBD (likely 2020 NBCC or Alberta-adopted version)" | Mandatory practice under a building code requires knowing the exact applicable edition; "TBD" weakens the normative force of R-004, R-008, and R-010 which depend on code compliance | Specification.md | Specification.md#Standards | -- | AHJ / Alberta Building Code registry | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add explicit pass/fail threshold or rubric for R-004 Addenda verification; current acceptance criteria ("all 16+ ... acknowledged") lacks definition of "acknowledged" vs. "integrated" | R-004 verification says "line-by-line comparison" but acceptance criteria says "acknowledged in narrative" -- this is materially ambiguous for compliance determination (does acknowledgment = a sentence or full integration?) | Specification.md | Specification.md#Verification (R-004 row) | -- | Design Manager + Proposal Manager | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add guidance or placeholder for obtaining the Project Team Roster prerequisite (currently "TBD -- obtain from firm leadership") with a deadline relative to Step 3 | Practical execution of Steps 3-5 requires confirmed team names (Design Manager, Lead Architect, discipline leads) but the prerequisite is TBD with no timeline or fallback | Procedure.md | Procedure.md#Prerequisites > Required Inputs (Project Team Roster row) | -- | Design Manager / Firm Leadership | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Addendum 03 sections 1.12-1.16 content not fully enumerated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet references are comprehensive for available sources |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | CCDC 14-2013 clause numbers TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data elements are consistently presented across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scoring weight, audience, schedule flexibility) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each requirement and consideration is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Narrative scope and exclusions clearly bounded |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message across documents is coherent and mutually reinforcing |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design-Build delivery understanding is well demonstrated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Discipline leads and coordination approach show competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of design methodology topics is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding across documents is consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Owner review window duration is TBD |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs T-001 through T-005 demonstrate adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic coverage of considerations C-001 through C-007 is adequate |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Procedure | Datasheet | Enumerate Addendum 03 sections 1.12 through 1.16 content; currently noted as "(Additional clarifications -- confirm from addendum text; location TBD in detail)" | Procedure Step 2 lists Addendum 03 sections 1.1-1.11 and 1.17-1.18 but sections 1.12-1.16 are summarized as TBD. These are essential facts that may contain driver requirements not yet captured. | Procedure.md | Procedure.md#Step 2 (Addendum 03 list, line referencing 1.12-1.16) | -- | Addendum 03 source document | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Add specific CCDC 14-2013 clause references for design submission and Owner review obligations; currently "location TBD (document not directly accessed)" | Standards table in Specification states exact clause numbers are TBD. Without these, comprehensive record of applicable contract obligations is incomplete. | Specification.md | Specification.md#Standards (CCDC 14-2013 row) | -- | CCDC 14-2013 contract document | TBD |
| B-003 | B:wisdom:necessity | WeakStatement | Guidance | Specification | Define Owner review window duration (currently "[TBD: suggest 5-10 business days per phase]" in Guidance EX-002); record confirmed value in Specification or Datasheet | Owner review window is a schedule-critical parameter affecting all five milestone gates. Leaving it TBD means the design phase schedule cannot be finalized. | Guidance.md | Guidance.md#Examples > EX-002 | -- | Design Manager + Owner agreement | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 0 | NO_ITEMS | Regulatory imperatives (NBCC, ABC, NFPA) identified though editions TBD (covered in A-002) |
| C:normative:sufficiency | normative | sufficiency | conformance assurance | 1 | HAS_ITEMS | R-001 verification is checklist-based but RFP text not available |
| C:normative:completeness | normative | completeness | comprehensive mandate | 0 | NO_ITEMS | Mandate coverage is comprehensive across R-001 through R-011 |
| C:normative:consistency | normative | consistency | regulatory coherence | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is thorough |
| C:operative:sufficiency | operative | sufficiency | operational competence | 0 | NO_ITEMS | Competence demonstrated through role assignments and step detail |
| C:operative:completeness | operative | completeness | operational thoroughness | 0 | NO_ITEMS | 10-step procedure is operationally thorough |
| C:operative:consistency | operative | consistency | procedural reliability | 0 | NO_ITEMS | Procedure steps are logically sequenced and consistent |
| C:evaluative:necessity | evaluative | necessity | value criterion | 1 | HAS_ITEMS | Value engineering trigger threshold not defined |
| C:evaluative:sufficiency | evaluative | sufficiency | merit validation | 0 | NO_ITEMS | Merit validation through examples and trade-off analysis is sufficient |
| C:evaluative:completeness | evaluative | completeness | comprehensive valuation | 0 | NO_ITEMS | Valuation dimensions (cost, code, schedule, operational fit) well-covered |
| C:evaluative:consistency | evaluative | consistency | evaluative integrity | 0 | NO_ITEMS | Evaluative criteria consistent across Guidance trade-offs and Procedure steps |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add fallback verification method for R-001 in the event that RFP Section 7.1 full text remains unavailable; current checklist approach cannot be executed without the source document | R-001 verification says "Checklist review against RFP Section 7.1 sub-headings and requirements" but the RFP text has not been directly accessed. Conformance assurance cannot be provided if the checklist source is unavailable. | Specification.md | Specification.md#Verification (R-001 row) | -- | Proposal Manager / RFP source access | TBD |
| C-002 | C:evaluative:necessity | WeakStatement | Procedure | Specification | Define the value engineering trigger threshold (currently "[TBD %]" in Procedure Step 8); record as a parameter in Datasheet or Specification | The value engineering process in Procedure Step 8.3 triggers "when cost estimate exceeds budget target by [TBD %]" -- this is a critical value criterion that determines when innovation is constrained by cost | Procedure.md | Procedure.md#Step 8 (Step 8.3) | -- | Design Manager + Cost Consultant | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | compliance foundation | 0 | NO_ITEMS | Compliance foundations established through R-001 to R-011 and Standards table |
| F:normative:sufficiency | normative | sufficiency | regulatory sufficiency | 1 | HAS_ITEMS | NFPA 1 applicability is assumption-based |
| F:normative:completeness | normative | completeness | exhaustive compliance | 0 | NO_ITEMS | Compliance coverage across R-001 to R-011 is exhaustive for known requirements |
| F:normative:consistency | normative | consistency | governance uniformity | 0 | NO_ITEMS | Governance structure (Owner approval at each gate) is uniformly applied |
| F:operative:necessity | operative | necessity | execution foundation | 1 | HAS_ITEMS | Cost consultant role appears in Procedure but not in Specification requirements |
| F:operative:sufficiency | operative | sufficiency | procedural adequacy | 0 | NO_ITEMS | Procedural steps provide adequate detail for execution |
| F:operative:completeness | operative | completeness | comprehensive execution | 0 | NO_ITEMS | Execution steps cover all requirement areas |
| F:operative:consistency | operative | consistency | execution consistency | 1 | HAS_ITEMS | AHJ review time assumptions differ between documents |
| F:evaluative:necessity | evaluative | necessity | appraisal prerequisite | 0 | NO_ITEMS | Scoring weight and evaluation committee identified |
| F:evaluative:sufficiency | evaluative | sufficiency | evaluative adequacy | 0 | NO_ITEMS | Evaluation guidance is sufficient for narrative production |
| F:evaluative:completeness | evaluative | completeness | exhaustive appraisal | 0 | NO_ITEMS | Appraisal dimensions well-covered |
| F:evaluative:consistency | evaluative | consistency | appraisal fidelity | 0 | NO_ITEMS | Appraisal criteria are faithful to RFP scoring intent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Specification | Guidance | Add rationale for NFPA 1 inclusion as an applicable standard; currently listed as "ASSUMPTION: standard for fire stations in Canada; location TBD" with no RFP citation | NFPA 1 appears in Standards table as an assumed applicable standard but has no RFP or contract backing. If it is not actually required by the AHJ, referencing it in the narrative could create unnecessary obligations. | Specification.md | Specification.md#Standards (NFPA 1 row) | -- | AHJ confirmation | TBD |
| F-002 | F:operative:necessity | MissingSlot | Specification | Specification | Add a requirement (or note under R-008) for cost validation integration at each design phase, including Cost Consultant role; Procedure Step 6 and Guidance C-006 reference this but no Specification requirement captures it | Cost consultant involvement and cost validation at each phase is described in Procedure Step 6 and Guidance C-006 but has no corresponding requirement in Specification. This is an execution foundation gap -- the Procedure prescribes an activity not anchored in a requirement. | Procedure.md, Guidance.md | Procedure.md#Step 6 (QA/QC); Guidance.md#Considerations > C-006 | -- | Design Manager | TBD |
| F-003 | F:operative:consistency | Normalization | Multi | Guidance | Normalize AHJ review time assumptions: Guidance P-005 states "4-6 weeks" for building permits; Procedure Step 7 states "4-6 weeks" for Foundation and "6-8 weeks" for Building permit. Clarify whether these are the same or different estimates and record in Datasheet. | Guidance P-005 gives a single range for permits generally while Procedure Step 7 distinguishes Foundation vs. Building permit review times. The difference may be intentional but is not explained, creating execution consistency risk. | Guidance.md, Procedure.md | Guidance.md#Principles > P-005; Procedure.md#Step 7 (Permitting Timeline) | Guidance.md#P-005, Procedure.md#Step 7 | Design Manager + AHJ consultation | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | prescriptive resolution | 0 | NO_ITEMS | Prescriptive direction is clear through requirements and procedure |
| D:normative:applying | normative | applying | obligatory fulfillment | 0 | NO_ITEMS | Obligatory elements well-identified and tracked |
| D:normative:judging | normative | judging | compliance adjudication | 0 | NO_ITEMS | Verification table provides compliance adjudication structure |
| D:normative:reviewing | normative | reviewing | governance verification | 0 | NO_ITEMS | Owner approval gates at each milestone provide governance verification |
| D:operative:guiding | operative | guiding | procedural settlement | 0 | NO_ITEMS | Procedure is well-settled with 10 defined steps |
| D:operative:applying | operative | applying | operational fulfillment | 1 | HAS_ITEMS | Knowledge transfer to construction not in Specification |
| D:operative:judging | operative | judging | performance adjudication | 0 | NO_ITEMS | Step 9 verification checklist adjudicates performance |
| D:operative:reviewing | operative | reviewing | process reconciliation | 0 | NO_ITEMS | Cross-reference validation in Step 9 reconciles with related deliverables |
| D:evaluative:guiding | evaluative | guiding | value resolution | 0 | NO_ITEMS | Value orientation through scoring weight and evaluation dimensions is resolved |
| D:evaluative:applying | evaluative | applying | merit fulfillment | 0 | NO_ITEMS | Examples EX-001 through EX-004 demonstrate merit fulfillment |
| D:evaluative:judging | evaluative | judging | worth adjudication | 1 | HAS_ITEMS | Scoring rubric details not available |
| D:evaluative:reviewing | evaluative | reviewing | quality reconciliation | 0 | NO_ITEMS | QA/QC approach and Proposal Manager review provide quality reconciliation |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:applying | MissingSlot | Specification | Specification | Add a requirement addressing design-to-construction knowledge transfer (handoff documentation, system design narratives for complex systems); Guidance C-007 identifies this as important but no Specification requirement covers it | Guidance C-007 describes the importance of knowledge transfer from design to construction team, including documentation for complex systems (exhaust, generator, sump). This is absent from Specification requirements, creating a gap in operational fulfillment. | Guidance.md | Guidance.md#Considerations > C-007 | -- | Design Manager | TBD |
| D-002 | D:evaluative:judging | TBD_Question | Datasheet | Datasheet | TBD: Obtain the actual scoring rubric or evaluation criteria detail for the 3-point Design Methodology sub-criterion to confirm what evaluators assess beyond "process clarity, Owner responsiveness, and Addenda integration" | Worth adjudication depends on understanding what the evaluators weight. The Datasheet and Guidance note the 3-point scoring weight but the actual rubric is assumed, not confirmed. If evaluators use different criteria, the narrative may miss key scoring dimensions. | Datasheet.md, Guidance.md | Datasheet.md#Notes; Guidance.md#Notes | -- | RFP evaluation criteria source | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | directive closure | 0 | NO_ITEMS | Directives are closed through requirements and procedure steps |
| X:guiding:sufficiency | guiding | sufficiency | guided assurance | 0 | NO_ITEMS | Guidance provides sufficient assurance through principles and examples |
| X:guiding:completeness | guiding | completeness | directive completeness | 0 | NO_ITEMS | Directive set (R-001 to R-011, P-001 to P-006) is complete |
| X:guiding:consistency | guiding | consistency | directive fidelity | 0 | NO_ITEMS | Directives are faithful to RFP and Addenda sources |
| X:applying:necessity | applying | necessity | implemented obligation | 1 | HAS_ITEMS | R-011 verification deferred to another deliverable |
| X:applying:sufficiency | applying | sufficiency | applied competence | 0 | NO_ITEMS | Competence demonstrated through detailed procedure |
| X:applying:completeness | applying | completeness | exhaustive implementation | 0 | NO_ITEMS | Implementation steps are exhaustive |
| X:applying:consistency | applying | consistency | applied fidelity | 0 | NO_ITEMS | Implementation is faithful to requirements |
| X:judging:necessity | judging | necessity | adjudicated standard | 0 | NO_ITEMS | Standards identified and adjudication approach defined |
| X:judging:sufficiency | judging | sufficiency | validated sufficiency | 0 | NO_ITEMS | Validation approach is sufficient for each requirement |
| X:judging:completeness | judging | completeness | comprehensive adjudication | 0 | NO_ITEMS | All requirements have verification entries |
| X:judging:consistency | judging | consistency | adjudicative integrity | 0 | NO_ITEMS | Verification approaches are consistent in rigor |
| X:reviewing:necessity | reviewing | necessity | verified foundation | 1 | HAS_ITEMS | Geotechnical report sufficiency decision point lacks verification criteria |
| X:reviewing:sufficiency | reviewing | sufficiency | audited adequacy | 0 | NO_ITEMS | Adequacy is auditable through defined checks |
| X:reviewing:completeness | reviewing | completeness | exhaustive review | 0 | NO_ITEMS | Review coverage is exhaustive across all phases |
| X:reviewing:consistency | reviewing | consistency | audit fidelity | 0 | NO_ITEMS | Audit approach is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Clarify R-011 verification ownership: acceptance criteria says "Review during proposal assembly (SOW-0001)" but this is outside DEL-06-01 scope. Add a verification step within this deliverable's scope (e.g., confirm narrative formatting before handoff to Proposal Manager). | R-011 verification is fully deferred to SOW-0001/DEL-01-02. This means there is no verification of formatting compliance within the DEL-06-01 procedure itself, creating a gap where the implemented obligation for formatting may not be checked until final assembly. | Specification.md | Specification.md#Verification (R-011 row) | -- | Proposal Manager | TBD |
| X-002 | X:reviewing:necessity | VerificationGap | Guidance | Procedure | Add verification criteria for the geotechnical report sufficiency decision point described in Guidance C-004; currently described as a consideration but no procedure step defines what "sufficient" means or what triggers supplemental investigation | Guidance C-004 proposes that the design methodology include a decision point on geotechnical report sufficiency. Procedure Step 6 references Foundation IFC QA/QC checking "Foundation design consistent with 2021 geotechnical report" but does not define criteria for determining if the existing report is sufficient for final design. The verified foundation lens reveals this gap. | Guidance.md, Procedure.md | Guidance.md#Considerations > C-004; Procedure.md#Step 6 (Foundation IFC row) | -- | Structural Lead + Geotechnical Consultant | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | regulatory finality | 0 | NO_ITEMS | Regulatory finality achieved through Standards, Requirements, and Verification |
| E:normative:sufficiency | normative | sufficiency | mandated assurance | 0 | NO_ITEMS | Mandated assurance provided by R-001 to R-011 with verification |
| E:normative:completeness | normative | completeness | exhaustive governance | 0 | NO_ITEMS | Governance model (Owner gates, QA/QC, Decision Log) is exhaustive |
| E:normative:consistency | normative | consistency | governance fidelity | 1 | HAS_ITEMS | Approval authority hierarchy split across documents |
| E:operative:necessity | operative | necessity | operational finality | 0 | NO_ITEMS | Operational procedure is final and actionable |
| E:operative:sufficiency | operative | sufficiency | operational assurance | 0 | NO_ITEMS | Operational assurance through detailed steps and prerequisites |
| E:operative:completeness | operative | completeness | operational completeness | 0 | NO_ITEMS | Operations covered end-to-end (Steps 1-10) |
| E:operative:consistency | operative | consistency | operational fidelity | 0 | NO_ITEMS | Operational steps are faithful to requirements |
| E:evaluative:necessity | evaluative | necessity | evaluative finality | 0 | NO_ITEMS | Evaluative criteria are final and well-grounded |
| E:evaluative:sufficiency | evaluative | sufficiency | merit assurance | 0 | NO_ITEMS | Merit assured through examples, trade-offs, and principles |
| E:evaluative:completeness | evaluative | completeness | evaluative completeness | 1 | HAS_ITEMS | Accessibility/adaptability treatment is thin |
| E:evaluative:consistency | evaluative | consistency | evaluative fidelity | 0 | NO_ITEMS | Evaluative approach is consistent across all documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:consistency | Normalization | Datasheet | Guidance | Consolidate the Owner approval authority description: Datasheet says "Formal approval required at each major phase gate"; Procedure Step 4 defines a 3-tier hierarchy (Owner Committee / Design Manager / Discipline Lead); Guidance says "formal milestone approvals". Normalize these into a single authoritative description in Guidance or Specification. | Governance fidelity requires a single consistent description of approval authority. Currently the approval structure is described at different levels of detail in three places, which could lead to inconsistent interpretation. | Datasheet.md, Procedure.md, Guidance.md | Datasheet.md#Construction (Owner Review row); Procedure.md#Step 4; Guidance.md#Purpose | -- | Design Manager | TBD |
| E-002 | E:evaluative:completeness | RationaleGap | Specification | Guidance | Add rationale in Guidance for why R-010 (accessibility/adaptability) is limited to "high-level integration" rather than substantive treatment; clarify the boundary with DEL-03-06 more explicitly so evaluators understand this is deliberate scoping, not omission | R-010 requires the narrative to "demonstrate awareness" of accessibility but defers full treatment to DEL-03-06. From an evaluative completeness perspective, there is no rationale explaining why this boundary exists. Evaluators may perceive this as incomplete coverage unless the rationale is explicit. | Specification.md, Guidance.md | Specification.md#Requirements (R-010); Guidance.md (no dedicated accessibility principle) | -- | Design Manager | TBD |
