# Semantic Lensing Register: DEL-016-01 Overhead Cranes — Two 5-Tonne Units

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-016_Crane & Lifting Equipment/1_Working/DEL-016-01_Overhead-Cranes
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-016-01_Overhead-Cranes/_CONTEXT.md (Deliverable Identity, Scope of Work References, Context Summary)
- _STATUS.md — DEL-016-01_Overhead-Cranes/_STATUS.md (Current Status: SEMANTIC_READY; not modified)
- _SEMANTIC.md — DEL-016-01_Overhead-Cranes/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-016-01_Overhead-Cranes/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md — DEL-016-01_Overhead-Cranes/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-016-01_Overhead-Cranes/Guidance.md (Purpose, Principles, Considerations, Trade-offs)
- Procedure.md — DEL-016-01_Overhead-Cranes/Procedure.md (Prerequisites, Steps A-E, Verification, Records)
- _REFERENCES.md — DEL-016-01_Overhead-Cranes/_REFERENCES.md (R-01, R-04; read)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 11
  - Guidance: 3
  - Procedure: 9
  - Multi: 1
- By matrix:
  - A: 5  B: 4  C: 4  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 9
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards assumptions need confirmation |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Load test requirement is assumption-tagged |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for crane type requirement |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Safety code audit sequencing gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure covers operational direction adequately |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Installation steps are adequately described |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Verification table missing REQ-016-01-06 and REQ-016-01-08 |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section adequately covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance clearly articulates value drivers |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off table addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Evaluation criteria in Procedure Step A2 adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Closeout documentation covers quality record |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify REQ-016-01-08: replace "ASSUMPTION" tag on CSA Z256 and ASME B30.2 with a definitive requirement once confirmed by engineer, or convert to explicit TBD requiring human resolution | Standards are tagged ASSUMPTION in both Specification and Datasheet but are the core prescriptive direction for the entire deliverable; leaving them as assumptions risks procurement proceeding without confirmed regulatory basis | Specification.md | Section 2.2 (Code and Standards Requirements), REQ-016-01-08 | -- | PROPOSAL: Structural/crane engineer to confirm applicable standards | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify REQ-016-01-15: specify whether load test is rated load or proof load, and at what percentage of rated capacity; current wording "ASSUMPTION -- a rated load test (or proof load test per applicable standard)" is ambiguous for mandatory practice | Load test is a mandatory practice for crane commissioning; the current requirement uses hedging language that does not give the Crane Contractor a definitive test protocol | Specification.md | Section 2.4 (Commissioning and Testing), REQ-016-01-15 | -- | PROPOSAL: Authority Having Jurisdiction to confirm test standard | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for REQ-016-01-06 (Crane Type) in Procedure Section 4 verification table; currently only in Specification Section 4 but missing from Procedure verification checks | Procedure Section 4 verification table does not include a check for crane type (REQ-016-01-06), creating a gap in compliance determination at commissioning | Procedure.md | Section 4 (Verification) | -- | PROPOSAL: Add to Procedure verification table | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or prerequisite for scheduling and coordinating the Alberta Safety Code inspection with the Authority Having Jurisdiction, including lead-time allowance; currently Step D3 says "Arrange and attend" but provides no guidance on when to initiate this | Regulatory audit by AHJ requires advance scheduling; without lead-time planning, the inspection could delay commissioning and breach the Dec 31, 2026 deadline | Procedure.md | Section 3, Phase D, Step D3 | -- | PROPOSAL: Crane Contractor / Project Manager | TBD |
| A-005 | A:operative:judging | VerificationGap | Procedure | Procedure | Add verification rows for REQ-016-01-06 (Crane Type confirmation) and REQ-016-01-08 (Standards compliance) to the Procedure Section 4 verification table | Procedure verification table covers 9 of 16 requirements but omits REQ-016-01-06 and REQ-016-01-08; these are verified in Specification Section 4 but the operational verification checklist should include them for field execution | Procedure.md | Section 4 (Verification) | -- | PROPOSAL: Add to Procedure verification table | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Crane span value TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Voltage/amperage TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet comprehensive for available information |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Building dimension inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Context and references provide adequate signals |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Section 2 covers fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Role assignments adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Covered across document set |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Duty class decision unresolved |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table provides adequate judgment basis |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Crane span (runway-to-runway) is an essential fact currently marked TBD pending structural engineering output from DEL-002-07; this value is needed before procurement RFQ can be issued | Crane span is a fundamental equipment parameter required for supplier quotation; without it, procurement cannot proceed and RFQ (Procedure Step A1) will be incomplete | Datasheet.md | Section 2.2 (Physical / Geometric Attributes) | -- | PROPOSAL: Structural Engineer (DEL-002-07) | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Voltage/amperage for crane circuit is TBD pending electrical design (DEL-004 series); without this, adequate evidence for electrical coordination is missing | Crane power data is needed for both procurement (selecting the correct crane model) and electrical design coordination (Procedure Step A4) | Datasheet.md | Section 2.3 (Power Supply) | -- | PROPOSAL: Electrical Engineer (PKG-004) and crane supplier | TBD |
| B-003 | B:data:consistency | Normalization | Datasheet | Multi | Normalize building width reference: Datasheet Section 2.2 states "130 ft building width per App B" for runway length, but the building dimensions from App B are 130 ft x 100 ft; clarify whether 130 ft is the building length or width and which dimension drives runway length | Inconsistent use of "width" vs "length" for the 130 ft dimension could cause confusion in structural and crane layout coordination; Specification does not repeat this dimension | Datasheet.md | Section 2.2 (Physical / Geometric Attributes, Runway length row) | -- | PROPOSAL: Confirm against App B floor plan | TBD |
| B-004 | B:wisdom:necessity | TBD_Question | Guidance | Guidance | Record TBD: Crane duty class (CMAA Specification 70 classification) must be determined with input from Camrose County on anticipated lift frequency and load types; this essential discernment is currently unresolved and tagged ASSUMPTION in Datasheet, Specification, and Guidance | Duty class affects equipment selection, cost, service life, and safety; it cannot be left as an assumption through procurement | Guidance.md | Section 3.1 (Crane Configuration Options) | -- | PROPOSAL: Camrose County to provide anticipated use data; engineer to classify | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Statutory Obligation | 1 | HAS_ITEMS | Specific Alberta Safety Code sections not cited |
| C:normative:sufficiency | normative | sufficiency | Certified Acceptance Criteria | 1 | HAS_ITEMS | Acceptance criteria for standards compliance are assumption-dependent |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Standards table in Specification Section 3 is appropriately comprehensive for current stage |
| C:normative:consistency | normative | consistency | Codified Compliance Uniformity | 0 | NO_ITEMS | Consistent compliance language across documents |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 1 | HAS_ITEMS | Missing anti-collision requirement |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Competence | 0 | NO_ITEMS | Procedure demonstrates adequate competence pathway |
| C:operative:completeness | operative | completeness | Unified Workflow Completeness | 1 | HAS_ITEMS | Warranty coordination step missing |
| C:operative:consistency | operative | consistency | Reliable Methodical Discipline | 0 | NO_ITEMS | Procedure methodology is consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Guidance adequately recognizes intrinsic merit of cranes |
| C:evaluative:sufficiency | evaluative | sufficiency | Grounded Professional Judgment | 0 | NO_ITEMS | Trade-off analysis provides grounded judgment |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Appraisal | 0 | NO_ITEMS | Guidance Section 3.4 covers warranty/guarantee value |
| C:evaluative:consistency | evaluative | consistency | Equitable Integrity Assurance | 0 | NO_ITEMS | Value assessments consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add specific Alberta Safety Codes section/regulation numbers applicable to overhead crane installation (e.g., Alberta Elevating Devices and Amusement Rides Regulation, if applicable) rather than generic "Alberta Safety Codes applicable to lifting equipment" | Enforceable statutory obligations must be precisely identified so the Crane Contractor can verify compliance; generic reference risks misinterpretation of which codes apply | Specification.md | Section 2.2 (REQ-016-01-07) and Section 3 (Standards table) | -- | PROPOSAL: Authority Having Jurisdiction to confirm applicable regulation numbers | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-016-01-08 (standards compliance): specify what evidence constitutes proof of compliance with CSA Z256 / ASME B30.2 (e.g., manufacturer's declaration of conformity, third-party certification, test reports) | Current verification method for REQ-016-01-08 is "Manufacturer's certification and documentation review" which lacks specificity on what documentation constitutes certified acceptance | Specification.md | Section 4 (Verification table, REQ-016-01-08 row) | -- | PROPOSAL: Engineer to define acceptable evidence | TBD |
| C-003 | C:operative:necessity | MissingSlot | Specification | Specification | Add requirement for anti-collision system or operational protocol if two cranes share any runway rails or operate in proximity; Guidance Section 3.2 raises this consideration but no corresponding requirement exists | Two cranes in one bay may require anti-collision protection for critical operational readiness; this is discussed in Guidance but absent from Specification requirements | Specification.md; Guidance.md | Specification: entire Section 2 scanned; Guidance: Section 3.2 | -- | PROPOSAL: Structural Engineer and crane supplier to advise | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step in Phase E (Closeout) to verify and record that crane supplier warranty terms align with the 2-year guarantee period per RFP Section 2.10, as noted in Guidance Section 3.4 | Guidance identifies warranty alignment as a consideration but the Procedure closeout sequence does not include a warranty verification step, creating a gap in unified workflow completeness | Procedure.md; Guidance.md | Procedure: Section 3, Phase E; Guidance: Section 3.4 | -- | PROPOSAL: Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Regulatory Command | 1 | HAS_ITEMS | P.Eng. requirement scope ambiguity |
| F:normative:sufficiency | normative | sufficiency | Demonstrable Compliance Warrant | 0 | NO_ITEMS | Compliance warrant structure adequate |
| F:normative:completeness | normative | completeness | Compulsory Governance Scope | 1 | HAS_ITEMS | Missing municipal permit requirements |
| F:normative:consistency | normative | consistency | Systematic Statutory Coherence | 0 | NO_ITEMS | Statutory references are internally coherent |
| F:operative:necessity | operative | necessity | Demonstrated Capacity Foundation | 1 | HAS_ITEMS | Installer qualification requirements vague |
| F:operative:sufficiency | operative | sufficiency | Verified Operational Fitness | 0 | NO_ITEMS | Operational fitness verification covered by commissioning steps |
| F:operative:completeness | operative | completeness | Comprehensive Workflow Mastery | 0 | NO_ITEMS | Workflow is comprehensive |
| F:operative:consistency | operative | consistency | Disciplined Process Transparency | 0 | NO_ITEMS | Process is transparent and disciplined |
| F:evaluative:necessity | evaluative | necessity | Definitive Value Awareness | 0 | NO_ITEMS | Value awareness adequately established |
| F:evaluative:sufficiency | evaluative | sufficiency | Evidenced Quality Appraisal | 1 | HAS_ITEMS | No quality criteria for crane supplier selection |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Mastery | 0 | NO_ITEMS | Valuation covered in Guidance trade-offs |
| F:evaluative:consistency | evaluative | consistency | Integrated Ethical Alignment | 0 | NO_ITEMS | Ethical alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify scope of P.Eng. requirement in REQ-016-01-09: "Any engineered components of the crane installation (runway connections, load data, anchorage)" is hedged by "any"; specify whether this includes shop drawings, installation drawings, or only structural anchorage calculations | REQ-016-01-09 uses "any engineered components" which is open to interpretation; the Crane Contractor may interpret this narrowly while the Owner may expect broad coverage including all IFC drawings per RFP Section 3.3.2 | Specification.md | Section 2.2 (REQ-016-01-09) | -- | PROPOSAL: Owner / Project Manager to define scope | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement addressing whether municipal building permit or development permit is required for crane installation within the new building addition, or confirm this is covered under the general building permit for the project | Compulsory governance scope should include all permit requirements; crane installation within a new building may trigger specific municipal or provincial permit requirements beyond safety codes | Specification.md | Section 2.2 (Code and Standards Requirements) and Section 3 (Standards table) — entire sections scanned | -- | PROPOSAL: Project Manager to confirm with municipality | TBD |
| F-003 | F:operative:necessity | WeakStatement | Specification | Specification | Strengthen installer qualification language: REQ-016-01-13 references "Prime Contractor's OH&S program" for safe installation but does not specify that crane installation personnel must hold specific certifications (e.g., certified rigger, journeyman ironworker, or crane installer credential); Procedure PRE-016-01-10 mentions "certified crane installers / riggers" but this is only a prerequisite, not a specification requirement | Demonstrated capacity foundation requires that personnel qualifications be specified as a requirement, not merely a procedural prerequisite; the Specification is the normative authority | Specification.md; Procedure.md | Specification: Section 2.3 (REQ-016-01-13); Procedure: Section 2.2 (PRE-016-01-10) | -- | PROPOSAL: Add installer qualification requirement to Specification | TBD |
| F-004 | F:evaluative:sufficiency | MissingSlot | Procedure | Specification | Add supplier evaluation criteria (quality metrics) for Step A2: Procedure says "Evaluate against specification requirements" but does not list quality-related criteria such as manufacturer's track record, warranty terms, or certifications (e.g., ISO 9001) | Evidenced quality appraisal requires defined criteria beyond "specification requirements"; without quality evaluation criteria, supplier selection may default to lowest price rather than best value | Procedure.md | Section 3, Phase A, Step A2 | -- | PROPOSAL: Project Manager / Owner to define evaluation weighting | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority well established across documents |
| D:normative:applying | normative | applying | Enforced Compliance Delivery | 0 | NO_ITEMS | Compliance delivery pathway clear |
| D:normative:judging | normative | judging | Definitive Governance Ruling | 1 | HAS_ITEMS | Gantry/overhead conflict needs human ruling |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Alignment | 0 | NO_ITEMS | Oversight alignment adequate |
| D:operative:guiding | operative | guiding | Validated Process Navigation | 1 | HAS_ITEMS | Missing procurement timeline guidance |
| D:operative:applying | operative | applying | Verified Field Performance | 0 | NO_ITEMS | Field performance verification adequate |
| D:operative:judging | operative | judging | Confirmed Capability Adequacy | 0 | NO_ITEMS | Capability adequacy confirmed through testing steps |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Transparency | 0 | NO_ITEMS | Procedural transparency adequate |
| D:evaluative:guiding | evaluative | guiding | Purposeful Merit Alignment | 0 | NO_ITEMS | Merit alignment with objectives clear |
| D:evaluative:applying | evaluative | applying | Confirmed Worth Delivery | 0 | NO_ITEMS | Worth delivery pathway clear |
| D:evaluative:judging | evaluative | judging | Final Valuation Decree | 0 | NO_ITEMS | Valuation criteria adequate |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Integrity Review | 1 | HAS_ITEMS | No post-commissioning review step |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | Conflict | Multi | NA | Surface existing conflict CONF-016-01-01 for human ruling: App B labels equipment as "Gantry" while RFP Section 3.4 and SOW-0067 specify "overhead cranes on trolley"; D-001 proposes resolution but human ruling is still TBD | This conflict directly affects crane type procurement (free-standing gantry vs. top-running overhead bridge) and structural runway design; Guidance has documented this but it requires definitive governance ruling | Guidance.md; Datasheet.md | Guidance: Conflict Table (CONF-016-01-01); Datasheet: Section 2.1 (Note D-001) | Guidance.md#Conflict-Table (App B "Gantry" label) vs. Specification.md#Section-2.1 (REQ-016-01-06 overhead bridge type) | PROPOSAL: Follow D-001 per Decomposition Decision Log; confirm with County/Structural Engineer | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add procurement timeline guidance: specify target dates or milestone triggers for RFQ issuance, supplier selection, and purchase order relative to the December 31, 2026 deadline, given the 8-12 week lead time noted in Guidance Section 2.1 | Validated process navigation requires timeline guidance; Guidance identifies lead time as a risk but does not translate this into actionable procurement milestones | Guidance.md | Section 2.1 (Cranes Are a Long-Lead Item) | -- | PROPOSAL: Project Manager to establish procurement milestone dates | TBD |
| D-003 | D:evaluative:reviewing | MissingSlot | Procedure | Procedure | Add a post-commissioning warranty review step: after the guarantee period begins, schedule a review to confirm crane operational status and address any warranty claims before the 2-year guarantee period expires | Resolved integrity review should include lifecycle assurance; the Procedure ends at commissioning closeout but the 2-year guarantee period (RFP Section 2.10) requires ongoing stewardship | Procedure.md | Section 3, Phase E (Closeout) — entire phase scanned | -- | PROPOSAL: Owner / Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Baseline Awareness | 0 | NO_ITEMS | Baseline awareness established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Competent Steering | 1 | HAS_ITEMS | Specification assumptions need resolution path |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Command | 0 | NO_ITEMS | Governance command adequate for current stage |
| X:guiding:consistency | guiding | consistency | Reliable Governance Bearing | 0 | NO_ITEMS | Governance bearing consistent |
| X:applying:necessity | applying | necessity | Critical Compliance Foundation | 1 | HAS_ITEMS | Missing requirement traceability in Procedure |
| X:applying:sufficiency | applying | sufficiency | Proven Performance Evidence | 0 | NO_ITEMS | Performance evidence pathway adequate |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Record | 1 | HAS_ITEMS | As-installed documentation gap |
| X:applying:consistency | applying | consistency | Stable Delivery Coherence | 0 | NO_ITEMS | Delivery coherence stable |
| X:judging:necessity | judging | necessity | Binding Threshold Finding | 1 | HAS_ITEMS | Load test pass/fail criteria missing |
| X:judging:sufficiency | judging | sufficiency | Evidenced Capability Verdict | 0 | NO_ITEMS | Capability verdict evidence adequate |
| X:judging:completeness | judging | completeness | Absolute Adjudication Record | 0 | NO_ITEMS | Adjudication record framework adequate |
| X:judging:consistency | judging | consistency | Consistent Ruling Standard | 0 | NO_ITEMS | Ruling standards consistent |
| X:reviewing:necessity | reviewing | necessity | Foundational Oversight Awareness | 0 | NO_ITEMS | Oversight awareness adequate |
| X:reviewing:sufficiency | reviewing | sufficiency | Verified Procedural Oversight | 1 | HAS_ITEMS | Shop drawing review signoff not specified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Archive | 0 | NO_ITEMS | Records section comprehensive |
| X:reviewing:consistency | reviewing | consistency | Aligned Oversight Standard | 0 | NO_ITEMS | Oversight standards aligned |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for the assumption that independent runways (four rails) are preferred over shared runways (two rails with anti-collision): Guidance Section 3.2 states the assumption but does not provide the safety or operational reasoning that supports it | Justified competent steering requires that assumptions driving major structural decisions include their rationale; the shared-vs-independent runway decision has significant cost and safety implications | Guidance.md | Section 3.2 (Two Cranes in One Bay) | -- | PROPOSAL: Structural Engineer and Crane Contractor to provide input | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add explicit requirement traceability column to Procedure Phase C installation steps, linking each step to the Specification requirement it satisfies (e.g., Step C2 to REQ-016-01-03, REQ-016-01-06) | Critical compliance foundation requires that installation actions be traceable to their normative requirements; currently the Procedure steps do not cross-reference Specification requirement IDs | Procedure.md | Section 3, Phase C (Installation) | -- | PROPOSAL: Add REQ-ID references to Procedure steps | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement for as-installed survey/dimensional record to be completed and submitted, including actual crane span, hook height achieved, and runway rail alignment measurements | Exhaustive delivery record requires that the as-installed configuration be documented against designed parameters; Specification Section 5.1 lists "As-Installed Documentation" but does not specify what measurements it must contain | Specification.md | Section 5.1 (Required Submittals, As-Installed Documentation row) | -- | PROPOSAL: Define as-installed documentation contents | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add explicit pass/fail criteria for load test (REQ-016-01-15): specify what constitutes a passing result (e.g., no structural deformation, deflection within limits, all safety devices functional under load) | Binding threshold finding requires defined pass/fail boundaries; current verification method is "Witnessed load test; load test certificate" without specifying what the test must demonstrate beyond "crane passed" | Specification.md | Section 4 (Verification table, REQ-016-01-15 row) | -- | PROPOSAL: Engineer to define per applicable standard | TBD |
| X-005 | X:reviewing:sufficiency | RationaleGap | Procedure | Procedure | Add specification of who has approval authority for shop drawing review in Step B1, and what constitutes an approved shop drawing (e.g., stamped "Approved" vs. "Approved as Noted" vs. "Revise and Resubmit") | Verified procedural oversight requires that the review/approval process have defined authority and acceptance categories; Step B1 says "Record shop drawing approval" but does not specify the approval authority or disposition categories | Procedure.md | Section 3, Phase B, Step B1 | -- | PROPOSAL: Project Manager to define approval process | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Steering Datum | 1 | HAS_ITEMS | Hook height estimate not in Datasheet |
| E:guiding:information | guiding | information | Contextualized Governance Signal | 0 | NO_ITEMS | Governance signals adequately contextualized |
| E:guiding:knowledge | guiding | knowledge | Commanding Navigational Expertise | 0 | NO_ITEMS | Expertise requirements adequately specified |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Vision | 0 | NO_ITEMS | Leadership vision clear in Guidance |
| E:applying:data | applying | data | Verified Delivery Evidence | 1 | HAS_ITEMS | Delivery inspection criteria missing |
| E:applying:information | applying | information | Situated Performance Account | 0 | NO_ITEMS | Performance account adequate |
| E:applying:knowledge | applying | knowledge | Proficient Delivery Mastery | 0 | NO_ITEMS | Delivery mastery pathway clear |
| E:applying:wisdom | applying | wisdom | Principled Delivery Foresight | 0 | NO_ITEMS | Delivery foresight addressed in Guidance |
| E:judging:data | judging | data | Definitive Adjudication Record | 0 | NO_ITEMS | Adjudication record structure adequate |
| E:judging:information | judging | information | Decisive Verdict Clarity | 0 | NO_ITEMS | Verdict clarity adequate |
| E:judging:knowledge | judging | knowledge | Expert Adjudication Mastery | 0 | NO_ITEMS | Expert knowledge requirements specified |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Rationale | 0 | NO_ITEMS | Adjudication rationale adequate |
| E:reviewing:data | reviewing | data | Comprehensive Audit Evidence | 1 | HAS_ITEMS | Photographic record not specified |
| E:reviewing:information | reviewing | information | Transparent Oversight Account | 0 | NO_ITEMS | Oversight account transparent |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Audit Mastery | 0 | NO_ITEMS | Audit mastery framework adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Judgment | 0 | NO_ITEMS | Oversight judgment principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Add the illustrative hook height estimate (28-30 ft) from Guidance Section 5 to the Datasheet Section 2.2 Physical/Geometric Attributes as an ASSUMPTION datum, with cross-reference to Guidance; currently this data point exists only in Guidance Examples section | Authoritative steering datum for hook height should reside in the Datasheet as the descriptive repository, even if marked ASSUMPTION/TBD; Guidance is not the canonical location for factual parameters | Guidance.md; Datasheet.md | Guidance: Section 5 (Examples); Datasheet: Section 2.2 (Hook height row) | -- | PROPOSAL: Move datum to Datasheet; retain Guidance narrative | TBD |
| E-002 | E:applying:data | MissingSlot | Procedure | Procedure | Add specific inspection criteria for equipment receipt in Step B3: define what constitutes acceptable condition (e.g., no visible damage, all components present per packing list, nameplate data matches purchase order) | Verified delivery evidence requires defined inspection criteria; Step B3 says "Inspect all components for shipping damage" but does not specify a checklist or acceptance standard | Procedure.md | Section 3, Phase B, Step B3 | -- | PROPOSAL: Crane Contractor to define inspection checklist | TBD |
| E-003 | E:reviewing:data | TBD_Question | Procedure | Procedure | Record TBD: Should photographic documentation be required at key installation milestones (equipment receipt, runway placement, electrical connection, load test) as part of comprehensive audit evidence? | Comprehensive audit evidence for a critical-path equipment installation typically includes photographic records; Procedure Step B3 mentions "photograph any damage" for delivery inspection but no other phases require photographic documentation | Procedure.md | Section 3 (entire procedure scanned for photo documentation requirements) | -- | PROPOSAL: Project Manager to decide | TBD |
