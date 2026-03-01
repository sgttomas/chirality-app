# Semantic Lensing Register: DEL-001-01 Preliminary Architectural Design

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-001_Architectural Design/1_Working/DEL-001-01_Preliminary-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-01_Preliminary-Design/_CONTEXT.md
- _STATUS.md — DEL-001-01_Preliminary-Design/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-01_Preliminary-Design/_SEMANTIC.md
- Datasheet.md — DEL-001-01_Preliminary-Design/Datasheet.md
- Specification.md — DEL-001-01_Preliminary-Design/Specification.md
- Guidance.md — DEL-001-01_Preliminary-Design/Guidance.md
- Procedure.md — DEL-001-01_Preliminary-Design/Procedure.md
- _REFERENCES.md — DEL-001-01_Preliminary-Design/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 9
  - Guidance: 4
  - Procedure: 7
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 6
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Drive-through bay count |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 8 covers County approval review adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Coordination protocol weak |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-8 cover execution adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Presentation format TBD |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance trade-offs section adequate |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | County approval gate serves as worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification table sufficient |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify specific Alberta Building Code edition and Alberta Safety Codes editions applicable to this project as of 2026 | Prescriptive direction lens reveals that the governing code editions are not identified; Specification REQ-012 notes "specific code editions and clause references are not identified" and marks as ASSUMPTION. Without identified editions, normative direction is incomplete. | Specification.md | REQ-012 | -- | PROPOSAL: Architect to confirm applicable code editions at project mobilization | TBD |
| A-002 | A:normative:applying | Conflict | Multi | Specification | Clarify whether "two drive-through bays" are distinct from the open crane bay area or co-located; resolve bay count and configuration | Mandatory practice lens surfaces CONF-001 from Guidance: RFP states "two drive-through bays" but App B plan does not explicitly label them as distinct. This conflict is already identified but not resolved. | Guidance.md, Specification.md | Guidance#Conflict Table CONF-001, Specification#REQ-003 | Guidance.md#CONF-001 (R-01 ss3.1 vs R-04 App B) | PROPOSAL: Confirm with County at site meeting | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for REQ-012 (code compliance) that specifies what constitutes adequate preliminary-stage code acknowledgment vs. full compliance matrix at IFC | Under compliance determination lens, REQ-012 verification says "Code compliance noted in preliminary design; detailed compliance matrix to be produced at final design stage" but does not define acceptance criteria for the preliminary-stage acknowledgment. | Specification.md | REQ-012, Verification table row REQ-012 | -- | PROPOSAL: Specification | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen Step 1.5 coordination protocol from ASSUMPTION to a defined coordination schedule or reference a project coordination plan | Procedural direction lens reveals the interdisciplinary coordination protocol (Step 1.5) is marked as ASSUMPTION ("Weekly or bi-weekly coordination meetings"). This is a key operational direction that governs the coordination baseline but has no committed frequency. | Procedure.md | Step 1 -- Step 1.5 | -- | PROPOSAL: Procedure | TBD |
| A-005 | A:evaluative:guiding | TBD_Question | Guidance | Guidance | Record TBD: Confirm County's preferred format for the preliminary design presentation (PDF, plotted drawings, digital model, etc.) | Value orientation lens highlights that the presentation format is a key evaluative driver for whether the deliverable meets the County's expectations, yet it is marked as ASSUMPTION in Guidance C-7 and Procedure Step 1.2. | Guidance.md | C-7 | -- | PROPOSAL: Confirm with County project manager at site meeting | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service pit depth TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes well-sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | R-07 site maps not read |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Building dimension confirmation pending |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals captured in Datasheet conditions |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Old North Shop existing conditions |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging consistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design intent understood across documents |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Architect qualifications addressed |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope boundaries clear |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off section in Guidance adequate |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls flagged as ASSUMPTION appropriately |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Procedure | Datasheet | Record TBD: Service pit depth is not specified in accessible sources; obtain from structural or operational requirements | Essential fact lens reveals that service pit depth is noted as "TBD -- not specified in accessible sources" in Procedure Step 3.1 and is absent from Datasheet. This is an essential dimensional fact needed for the preliminary section drawing. | Procedure.md, Datasheet.md | Procedure#Step 3.1, Datasheet#Building Program | -- | PROPOSAL: Confirm with County or structural engineer | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add reference to R-07 (Site Maps) data in Datasheet References or Conditions; record site orientation and property boundary constraints | Comprehensive record lens reveals that R-07 (Appendix C -- Site Maps) is listed in Procedure Step 1.1 and noted in Guidance C-1 as needing review, but is absent from Datasheet References table. Site boundary and orientation data are missing from the descriptive record. | Datasheet.md, Guidance.md | Datasheet#References, Guidance#C-1 | -- | PROPOSAL: Datasheet | TBD |
| B-003 | B:data:consistency | WeakStatement | Datasheet | Datasheet | Clarify whether "~130 ft x 100 ft" is a design target or a constraint; note that dimensions are "scaled" from conceptual plan and subject to site survey confirmation | Reliable measurement lens reveals the building footprint is stated as "~130 ft x 100 ft (New North Shop portion)" with source noted as "R-04, App B (scaled)." The qualifier "scaled" and the tilde indicate these are approximate, but the Specification uses them as though they are design parameters (Procedure Step 2.1). | Datasheet.md | Datasheet#Building Program (Overall building footprint) | -- | PROPOSAL: Datasheet | TBD |
| B-004 | B:information:completeness | MissingSlot | Guidance | Guidance | Add a consideration for existing Old North Shop structural condition and any constraints the existing structure imposes on the connection to the new addition | Comprehensive account lens reveals that while renovation scope is addressed (Guidance P-5, Specification REQ-010), there is no mention of the existing building's structural condition or interface requirements at the connection point between old and new. This is an information gap for preliminary design. | Guidance.md, Specification.md | Guidance#P-5, Specification#REQ-010 | -- | PROPOSAL: Guidance | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Compliance Threshold | 1 | HAS_ITEMS | Occupancy classification missing |
| C:normative:sufficiency | normative | sufficiency | Mandated Justification Standard | 0 | NO_ITEMS | Justification chain from RFP adequate |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Environmental/hazmat gap |
| C:normative:consistency | normative | consistency | Uniform Regulatory Harmony | 0 | NO_ITEMS | Regulatory references consistent across docs |
| C:operative:necessity | operative | necessity | Critical Operational Capacity | 0 | NO_ITEMS | Procedure prerequisites cover critical items |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Functional Competence | 0 | NO_ITEMS | Architect qualification addressed |
| C:operative:completeness | operative | completeness | Thorough Execution Coverage | 0 | NO_ITEMS | Steps 1-8 comprehensive |
| C:operative:consistency | operative | consistency | Stable Procedural Alignment | 0 | NO_ITEMS | Procedure aligns with Specification |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Value proposition clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Merit Appraisal | 0 | NO_ITEMS | Trade-offs adequate |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 1 | HAS_ITEMS | Lifecycle cost absent |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add identification of building occupancy classification under Alberta Building Code (e.g., Group F Division 2 or 3) as a design parameter for the preliminary presentation | Binding compliance threshold lens reveals that no occupancy classification is stated in any document, yet it is a fundamental code-driven parameter affecting exits, fire separation, and structural requirements. Specification REQ-012 references code compliance generically but does not capture this binding threshold. | Specification.md, Datasheet.md | Specification#REQ-012, Datasheet#Conditions (Applicable codes) | -- | PROPOSAL: Specification | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add consideration for environmental or hazardous materials handling requirements applicable to a maintenance shop (oil storage, fuel, solvents) at the preliminary design stage | Exhaustive regulatory coverage lens reveals that the building will contain oil totes, oil pumping equipment, wash bay drainage, and welding operations, but no environmental or hazardous materials regulatory requirements are mentioned. This is a regulatory coverage gap for a maintenance shop facility. | Specification.md, Guidance.md | Specification#Standards, Guidance#entire document scanned | -- | PROPOSAL: Specification (standards) and Guidance (considerations) | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale for the "~13,000 sq ft" area target -- whether this is a minimum, maximum, or approximate target and what drives the number | Holistic value accounting lens reveals that the 13,000 sq ft figure is used as a target across all documents but its derivation or basis is not explained. Is it driven by equipment count, operational need, or budget? Understanding this helps the Architect evaluate design trade-offs. | Specification.md, Datasheet.md | Specification#REQ-002, Datasheet#Building Program (Useable area) | -- | PROPOSAL: Guidance | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Proof Mandate | 1 | HAS_ITEMS | REQ-001 verification weak |
| F:normative:sufficiency | normative | sufficiency | Validated Governance Benchmark | 1 | HAS_ITEMS | Acceptance criteria form |
| F:normative:completeness | normative | completeness | Total Compliance Assurance | 0 | NO_ITEMS | Requirements cover scope |
| F:normative:consistency | normative | consistency | Integrated Compliance Coherence | 0 | NO_ITEMS | Requirements consistent with conditions |
| F:operative:necessity | operative | necessity | Foundational Execution Imperative | 0 | NO_ITEMS | Prerequisites list adequate |
| F:operative:sufficiency | operative | sufficiency | Proven Process Proficiency | 0 | NO_ITEMS | Steps demonstrate proficiency path |
| F:operative:completeness | operative | completeness | Comprehensive Execution Scope | 1 | HAS_ITEMS | Signoff routing missing |
| F:operative:consistency | operative | consistency | Harmonized Performance Standard | 0 | NO_ITEMS | Performance checks aligned |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 1 | HAS_ITEMS | QA/QC step missing |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Appraisal | 0 | NO_ITEMS | Trade-offs provide defensibility |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 0 | NO_ITEMS | Verification table covers quality |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Clarify what constitutes "written County approval" for REQ-001 -- email, signed letter, meeting minutes, or formal sign-off form | Authoritative proof mandate lens reveals that REQ-001 verification is "County written approval or sign-off on record" but does not specify the form of that proof. For an authoritative proof mandate, the form of evidence matters. | Specification.md | REQ-001, Verification table row REQ-001 | -- | PROPOSAL: Specification | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Define acceptance tolerance for REQ-002 area target -- what range around "approximately 13,000 sq ft" is acceptable (e.g., +/-5%, +/-10%) | Validated governance benchmark lens reveals that REQ-002 uses "approximately 13,000 square feet" as the target but no acceptance band is defined. The verification is "Area calculation or scaled floor plan demonstrating compliance with target" but "compliance with target" is ambiguous without a tolerance. | Specification.md | REQ-002, Verification table row REQ-002 | -- | PROPOSAL: Specification | TBD |
| F-003 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or sub-step for formal submission routing: who receives the presentation, how it is transmitted, and what acknowledgment of receipt is expected | Comprehensive execution scope lens reveals that Procedure Steps 7.3-7.4 say "Submit... to the Camrose County project manager" and "Record the submission date and method" but do not specify the routing mechanism or receipt confirmation. For a mandatory approval gate, the submission protocol should be explicit. | Procedure.md | Step 7 -- Steps 7.3, 7.4 | -- | PROPOSAL: Procedure | TBD |
| F-004 | F:evaluative:necessity | MissingSlot | Procedure | Procedure | Add a QA/QC self-check step before submission (e.g., internal review of preliminary package against RFP ss3.4 checklist and Specification requirements) | Fundamental quality imperative lens reveals that the Procedure moves directly from assembly (Step 7) to submission without an explicit internal quality review. The Verification table in Procedure lists checks but does not tie them to a procedural step. | Procedure.md | Step 7, Verification table | -- | PROPOSAL: Procedure (add step between 6 and 7 or at start of 7) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Authoritative Mandate | 0 | NO_ITEMS | County approval gate well-established |
| D:normative:applying | normative | applying | Binding Protocol Execution | 1 | HAS_ITEMS | Mezzanine extent conflict |
| D:normative:judging | normative | judging | Assured Conformance Ruling | 0 | NO_ITEMS | Verification approach clear |
| D:normative:reviewing | normative | reviewing | Unified Conformance Inspection | 0 | NO_ITEMS | Audit path via County review |
| D:operative:guiding | operative | guiding | Grounded Process Stewardship | 1 | HAS_ITEMS | Site meeting TBD follow-up |
| D:operative:applying | operative | applying | Established Workflow Proficiency | 0 | NO_ITEMS | Workflow steps adequate |
| D:operative:judging | operative | judging | Comprehensive Capability Verdict | 0 | NO_ITEMS | Capability checks in Procedure adequate |
| D:operative:reviewing | operative | reviewing | Harmonized Systematic Review | 0 | NO_ITEMS | Step 5 covers systematic coordination review |
| D:evaluative:guiding | evaluative | guiding | Grounded Principled Vision | 0 | NO_ITEMS | Principles P-1 through P-5 adequate |
| D:evaluative:applying | evaluative | applying | Justified Quality Enactment | 0 | NO_ITEMS | Quality actions embedded in steps |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Ruling | 1 | HAS_ITEMS | No County feedback mechanism |
| D:evaluative:reviewing | evaluative | reviewing | Assured Worth Inspection | 0 | NO_ITEMS | County review serves as worth inspection |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | Specification | Resolve whether mezzanine extends over wash bay (per App B note) or is limited to parts room + utility room (per RFP ss3.4 text); update Specification REQ-009 and Datasheet accordingly | Binding protocol execution lens surfaces CONF-002 from Guidance: the mezzanine extent is described differently in RFP ss3.4 vs App B. This conflict directly affects binding protocol execution for the preliminary floor plan. | Guidance.md, Specification.md, Datasheet.md | Guidance#CONF-002, Specification#REQ-009, Datasheet#Building Program (Mezzanine storage) | Guidance.md#CONF-002 (R-01 ss3.4 vs R-04 App B) | PROPOSAL: Accept App B as more specific; confirm with County | TBD |
| D-002 | D:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen Step 1.2 to include a checklist of items to confirm at the mandatory site meeting (presentation format, approval routing, site constraints, geotech timeline) | Grounded process stewardship lens reveals that the mandatory site meeting (Step 1.2) is a critical steering event but the items to confirm are loosely listed. A structured checklist would ground the process stewardship for downstream steps. | Procedure.md | Step 1 -- Step 1.2 | -- | PROPOSAL: Procedure | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on what constitutes a successful County review outcome vs. a conditional approval vs. a rejection, and how revisions should be managed | Conclusive merit ruling lens reveals that while REQ-001 requires "County written approval," there is no guidance on what the County's evaluation criteria might be, what a conditional approval looks like, or how revision cycles are managed. Guidance addresses trade-offs (T-1) but not the ruling process itself. | Guidance.md, Specification.md | Guidance#Trade-offs T-1, Specification#REQ-001 | -- | PROPOSAL: Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Authority | 0 | NO_ITEMS | Steering authority clear via REQ-001 |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Directional Command | 1 | HAS_ITEMS | Elevation count assumption |
| X:guiding:completeness | guiding | completeness | Exhaustive Stewardship Scope | 0 | NO_ITEMS | Scope boundaries clear |
| X:guiding:consistency | guiding | consistency | Integrated Directional Harmony | 0 | NO_ITEMS | Direction consistent across docs |
| X:applying:necessity | applying | necessity | Critical Implementation Foundation | 1 | HAS_ITEMS | Cistern location verification |
| X:applying:sufficiency | applying | sufficiency | Proven Craft Methodology | 0 | NO_ITEMS | Methodology adequate |
| X:applying:completeness | applying | completeness | Total Implementation Mastery | 0 | NO_ITEMS | Implementation steps complete |
| X:applying:consistency | applying | consistency | Harmonized Method Reliability | 0 | NO_ITEMS | Methods consistent |
| X:judging:necessity | judging | necessity | Critical Compliance Finding | 1 | HAS_ITEMS | REQ-013 verification weak |
| X:judging:sufficiency | judging | sufficiency | Substantiated Performance Ruling | 0 | NO_ITEMS | Performance measures adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 1 | HAS_ITEMS | No departure tracking |
| X:judging:consistency | judging | consistency | Consistent Adjudication Standard | 0 | NO_ITEMS | Adjudication standards consistent |
| X:reviewing:necessity | reviewing | necessity | Fundamental Audit Acuity | 0 | NO_ITEMS | Audit trail via records adequate |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Audit Appraisal | 1 | HAS_ITEMS | Interdisciplinary signoff |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Record | 0 | NO_ITEMS | Records section covers outputs |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Consistency | 0 | NO_ITEMS | Audit checks consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Procedure | Guidance | Clarify how many elevations are required for the preliminary presentation -- Procedure Step 3.2 is marked ASSUMPTION ("one or two elevations") with no resolution path beyond "confirm with County" | Substantiated directional command lens reveals that the number and orientation of building elevations in the preliminary presentation is an unresolved ASSUMPTION. This affects scope and effort but lacks a decision criterion. | Procedure.md | Step 3 -- Step 3.2 | -- | PROPOSAL: Guidance (add to C-7 or new consideration) | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add explicit verification for cistern location compatibility with building layout (50,000 L cistern is a major space-planning item but verification is absent from Specification verification table) | Critical implementation foundation lens reveals that the 50,000 L cistern is mentioned in Datasheet and Guidance C-6 as having architectural space-planning implications, but there is no Specification requirement or verification entry for cistern accommodation. REQ-003 lists program spaces but cistern is not individually called out. | Specification.md, Datasheet.md, Guidance.md | Specification#Verification table, Datasheet#Building Program (Water storage cistern), Guidance#C-6 | -- | PROPOSAL: Specification | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen verification for REQ-013 (geotech/survey coordination) beyond "Design notes acknowledgment" -- specify what acknowledgment must contain (e.g., list of pending dependencies, foundation approach held open) | Critical compliance finding lens reveals that REQ-013 verification is "Design notes acknowledgment" which is weak for a critical dependency. A compliance finding requires more than acknowledgment -- it requires evidence of what was acknowledged and what remains open. | Specification.md | REQ-013, Verification table row REQ-013 | -- | PROPOSAL: Specification | TBD |
| X-004 | X:judging:completeness | MissingSlot | Specification | Guidance | Add a mechanism for tracking design departures from the conceptual drawing (R-04, App B) -- Guidance P-1 requires departures to be "explicitly flagged" but no log or register format is specified | Exhaustive adjudication record lens reveals that Guidance P-1 requires the Architect to flag departures from the conceptual layout, but there is no structured format for recording or tracking those departures. This creates a gap in the adjudication record for the County's review. | Guidance.md, Specification.md | Guidance#P-1, Specification#entire document scanned | -- | PROPOSAL: Guidance (add departure log recommendation) | TBD |
| X-005 | X:reviewing:sufficiency | WeakStatement | Procedure | Procedure | Add expected outcome or signoff mechanism for Step 5 interdisciplinary coordination review -- currently states "Incorporate coordination feedback" but does not define how agreement is recorded | Substantiated audit appraisal lens reveals that Procedure Step 5 describes interdisciplinary coordination review but does not specify how the coordination outcomes are formally recorded or agreed. Step 5.2 says "Document any unresolved coordination items" but no signoff or agreement mechanism is defined. | Procedure.md | Step 5 -- Steps 5.1, 5.2 | -- | PROPOSAL: Procedure | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Basis | 1 | HAS_ITEMS | R-05/R-06 data gap |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering information coherent |
| E:guiding:knowledge | guiding | knowledge | Accomplished Directional Mastery | 0 | NO_ITEMS | Directional knowledge adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 0 | NO_ITEMS | Foresight captured in Guidance trade-offs |
| E:applying:data | applying | data | Proven Execution Evidence | 1 | HAS_ITEMS | Heating system specification gap |
| E:applying:information | applying | information | Contextual Implementation Insight | 0 | NO_ITEMS | Implementation context adequate |
| E:applying:knowledge | applying | knowledge | Accomplished Craft Authority | 0 | NO_ITEMS | Craft knowledge embedded in steps |
| E:applying:wisdom | applying | wisdom | Judicious Craft Foresight | 0 | NO_ITEMS | Foresight in trade-offs adequate |
| E:judging:data | judging | data | Binding Verdict Evidence | 1 | HAS_ITEMS | Normalization: terminology |
| E:judging:information | judging | information | Coherent Adjudication Insight | 0 | NO_ITEMS | Adjudication information coherent |
| E:judging:knowledge | judging | knowledge | Accomplished Judgment Authority | 0 | NO_ITEMS | Judgment authority clear |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Judgment foresight adequate |
| E:reviewing:data | reviewing | data | Substantiated Inspection Record | 0 | NO_ITEMS | Records section adequate |
| E:reviewing:information | reviewing | information | Coherent Inspection Intelligence | 0 | NO_ITEMS | Inspection information coherent |
| E:reviewing:knowledge | reviewing | knowledge | Accomplished Audit Mastery | 1 | HAS_ITEMS | Assumption tracking |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Datasheet | Guidance | Add rationale or consideration for R-05 (Appendix B Electrical) and R-06 (Appendix B Plumbing) data -- Procedure Step 1.4 says to review these but no architectural implications are captured in Datasheet or Guidance | Authoritative directive basis lens reveals that R-05 and R-06 are mentioned in Procedure Step 1.4 as inputs requiring review, but neither Datasheet nor Guidance extracts any data or implications from them. If they contain architectural space-planning constraints, this is a gap in the directive basis. | Procedure.md, Datasheet.md, Guidance.md | Procedure#Step 1.4, Datasheet#References, Guidance#entire document scanned | -- | PROPOSAL: Guidance (add consideration re: electrical/plumbing appendices) | TBD |
| E-002 | E:applying:data | WeakStatement | Datasheet | Datasheet | Clarify "high recovery heating system (forced air makeup)" -- is this a design requirement or a suggestion? Add source clarity for whether the heating system type is prescribed or performance-based | Proven execution evidence lens reveals that the Datasheet lists "High recovery heating system (forced air makeup)" as an attribute sourced to R-01 ss3.4 and R-04 App B, but the language is descriptive rather than prescriptive. It is unclear whether the Architect must specify this exact system type or may propose alternatives meeting a performance requirement. | Datasheet.md | Datasheet#Building Program (Heating) | -- | PROPOSAL: Datasheet and Specification (add REQ or clarify in existing) | TBD |
| E-003 | E:judging:data | Normalization | Multi | Guidance | Normalize terminology: "service trench" vs "service pit" -- Datasheet uses "Service trench / pit" while Specification and Procedure use "service pit." Establish a single term and define it | Binding verdict evidence lens reveals inconsistent terminology for the below-grade service access feature. Datasheet says "Service trench / pit" with dimensions "~24 ft x 100 ft per plan." Specification REQ-003 says "ventilated/lighted service pit." Procedure says "service pit" and "service trench/pit." Inconsistent naming risks confusion in the preliminary presentation. | Datasheet.md, Specification.md, Procedure.md | Datasheet#Building Program (Service trench / pit), Specification#REQ-003, Procedure#Step 2.1, Step 3.1 | -- | PROPOSAL: Guidance (vocabulary note) and normalize across all docs | TBD |
| E-004 | E:reviewing:knowledge | Normalization | Multi | Guidance | Create an ASSUMPTION register or tracking mechanism -- ASSUMPTIONs are scattered across all four documents with no consolidated tracking, which makes audit and resolution difficult | Accomplished audit mastery lens reveals that numerous ASSUMPTIONs are tagged across all documents (Datasheet: drive-through bay count; Specification: REQ-011, REQ-012, REQ-013; Guidance: P-2, C-7; Procedure: survey data, qualifications, coordination meetings, elevations, package contents) but there is no consolidated register. This hinders audit mastery because assumptions cannot be systematically reviewed or resolved. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | entire document scanned (all four) | -- | PROPOSAL: Guidance or new section in Procedure (assumption register) | TBD |

---

*End of Semantic Lensing Register.*
