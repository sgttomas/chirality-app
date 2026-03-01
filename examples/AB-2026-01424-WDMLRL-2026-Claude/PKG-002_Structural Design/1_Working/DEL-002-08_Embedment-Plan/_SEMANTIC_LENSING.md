# Semantic Lensing Register: DEL-002-08 Steel Plate Embedment Plan

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-002-08 identity and description (Name: Steel Plate Embedment Plan, PKG-002)
- _STATUS.md -- Current state SEMANTIC_READY (2026-02-26)
- _SEMANTIC.md -- All 7 matrices parsed (A, B, C, F, D, X, E); 96 cells total
- Datasheet.md -- Identification, Attributes, Conditions, Construction, References
- Specification.md -- Scope, Requirements REQ-001 through REQ-010, Standards, Verification, Documentation
- Guidance.md -- Purpose, Principles P-01 through P-05, Considerations C-01 through C-06, Trade-offs T-01/T-02, Conflict Table
- Procedure.md -- Steps 1-8, Prerequisites, Verification, Records
- _REFERENCES.md -- R-01 (RFP), R-04 (Appendix B Shop); read, scope not expanded

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 6
  - Specification: 8
  - Guidance: 4
  - Procedure: 3
  - Multi: 6
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code editions not pinned |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Standards marked ASSUMPTION |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No specific NBC/CSA clause-level criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table exists; audit path adequate at this stage |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-8 provide adequate direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Equipment load data source unresolved |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks in Procedure adequate |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section and verification table present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section provides value context |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No acceptance tolerance for flush condition |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-01/T-02 address key value judgments |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal quality review (Step 6) covers this |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm specific edition of NBC and Alberta Safety Codes applicable to this project (year, amendments) | The Standards table lists NBC and Alberta Safety Codes as applicable but marks editions as "location TBD" and ASSUMPTION. Prescriptive direction requires pinned code editions to be enforceable. | Specification.md | Standards table | -- | Structural Engineer / Alberta municipality | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which CSA standards are confirmed-applicable vs. assumed-applicable; remove ASSUMPTION tag once confirmed by Structural Engineer | Five standards in the Standards table are marked ASSUMPTION with "location TBD." Mandatory practice requires confirmed applicability, not assumptions. | Specification.md | Standards table | -- | Structural Engineer | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add clause-level acceptance criteria for REQ-008 (Code Compliance) linking to specific NBC/CSA provisions once code editions are confirmed | REQ-008 requires code compliance but the Verification row says only "Engineering review: design basis references applicable Alberta codes." Without clause-level criteria, compliance determination is not auditable. | Specification.md | REQ-008; Verification table row for REQ-008 | -- | Structural Engineer | TBD |
| A-004 | A:operative:applying | TBD_Question | Procedure | Procedure | Record TBD: Identify specific source for equipment load data (County fleet records, manufacturer specs, or Owner-provided data) and confirm availability timeline | Procedure Step 1.4 requires "equipment load data from the project team or County" but does not name a specific document, contact, or confirmed source. Practical execution depends on this input being obtainable. | Procedure.md | Step 1 -- Confirm Scope and Coordination Inputs, item 1.4 | -- | Project team / County | TBD |
| A-005 | A:evaluative:applying | VerificationGap | Specification | Specification | Add measurable flush tolerance for steel plate surface relative to finished concrete (e.g., +0/-Xmm) as acceptance criterion for REQ-004 | Guidance P-03 states plates must be "flush with or marginally proud of" finished surface but no numeric tolerance appears in the Specification or Verification table. Merit application (quality of installed result) cannot be assessed without a measurable tolerance. | Specification.md, Guidance.md | Specification REQ-004; Guidance P-03 | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Steel plate material grade TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Appendix B provides adequate conceptual evidence |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Plate dimensions absent from all docs |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Slab thickness TBD across multiple docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Core signals (equipment type, location zones) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate given early design stage |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | No thermal/frost loading mention in Specification |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally consistent on stated items |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering basis described adequately |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement ensures competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge scope adequate for drawing-set deliverable |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T-01/T-02 capture key judgment calls |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Deferred to Structural Engineer appropriately |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance Considerations provide holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm steel plate grade (e.g., CSA G40.20/G40.21 350W or equivalent) once Structural Engineer specifies | Datasheet states "TBD -- steel plate grade, thickness, and surface finish to be specified by Structural Engineer." This is an essential fact that cannot remain TBD at IFC stage. | Datasheet.md | Steel Plate Material | -- | Structural Engineer | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add steel plate dimensions (length, width, thickness) as TBD parameters once determined by Structural Engineer | No plate dimensions appear anywhere in the production documents. Guidance C-03 notes "RFP and Appendix B do not specify steel plate dimensions." For a comprehensive record, these must be captured. | Datasheet.md, Guidance.md | Datasheet Attributes; Guidance C-03 | -- | Structural Engineer | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Multi | Ensure slab thickness value is stated consistently once confirmed; currently TBD in Datasheet (Conditions) and Specification (REQ-005) and Procedure (Step 2) | Slab thickness is referenced as TBD in multiple documents. When resolved, it must be recorded consistently to maintain reliable measurement across all docs. | Datasheet.md, Specification.md, Procedure.md | Datasheet Design Conditions; Specification REQ-005; Procedure Step 2.3 | -- | Structural Engineer | TBD |
| B-004 | B:information:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing thermal/frost considerations for embedded plates (differential thermal expansion between steel and concrete in heated shop) | Datasheet Environmental Conditions mentions "frost depth, thermal loading in concrete slab, and temperature cycling" but Specification has no corresponding requirement addressing thermal considerations for the embedment. This is an information gap for a comprehensive account. | Datasheet.md, Specification.md | Datasheet Environmental Conditions; Specification entire Requirements section scanned | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Regulatory Baseline | 1 | HAS_ITEMS | Code editions unconfirmed |
| C:normative:sufficiency | normative | sufficiency | Certified Acceptance Criteria | 1 | HAS_ITEMS | Acceptance criteria rely on assumptions |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 0 | NO_ITEMS | REQ-001 through REQ-010 provide adequate scope |
| C:normative:consistency | normative | consistency | Harmonized Conformity Standard | 0 | NO_ITEMS | Standards table is consistent with Requirements |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Geotech dependency timing |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Work Readiness | 0 | NO_ITEMS | Prerequisites table in Procedure is adequate |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 0 | NO_ITEMS | Steps 1-8 cover full workflow |
| C:operative:consistency | operative | consistency | Standardized Procedural Coherence | 0 | NO_ITEMS | Procedure steps align with Specification requirements |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | OBJ-001 and OBJ-003 linkage established |
| C:evaluative:sufficiency | evaluative | sufficiency | Validated Merit Appraisal | 0 | NO_ITEMS | Trade-offs acknowledge value judgments appropriately |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Merit Profile | 0 | NO_ITEMS | Guidance provides comprehensive rationale |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Value alignment consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-008 to reference confirmed code editions (not ASSUMPTION) once editions are identified, to establish an enforceable regulatory baseline | REQ-008 says design "shall comply with all applicable codes" but the Standards table notes are all ASSUMPTION-based. An enforceable regulatory baseline requires confirmed, cited code provisions. | Specification.md | REQ-008; Standards table Note | -- | Structural Engineer / Project team | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen Verification approach for REQ-002 ("Confirm loading analysis in DEL-002-10 covers equipment types") by specifying what constitutes sufficient confirmation (e.g., load case summary table cross-referenced) | Verification for REQ-002 is described at a general level. Certified acceptance criteria require a defined method for demonstrating sufficiency, not just a general "confirm" instruction. | Specification.md | Verification table row for REQ-002 | -- | Structural Engineer (PROPOSAL) | TBD |
| C-003 | C:operative:necessity | RationaleGap | Guidance | Guidance | Add guidance on how to proceed if geotech report (DEL-008-01) is not available before embedment design must commence; clarify risk and fallback strategy beyond noting assumption | Guidance C-04 and Procedure Note on Geotech both mention proceeding with assumed parameters, but the rationale for what constitutes acceptable assumed values and the risk threshold for proceeding is not explained. This is a critical operational prerequisite that needs clearer directional guidance. | Guidance.md, Procedure.md | Guidance C-04; Procedure Prerequisites Note on Geotech | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Code Compliance | 0 | NO_ITEMS | Covered by A-001, A-003, C-001 already; no additional item warranted |
| F:normative:sufficiency | normative | sufficiency | Defensible Regulatory Justification | 1 | HAS_ITEMS | ASSUMPTION tags undermine defensibility |
| F:normative:completeness | normative | completeness | Exhaustive Governance Record | 1 | HAS_ITEMS | No record of which codes were searched |
| F:normative:consistency | normative | consistency | Coherent Compliance Assurance | 0 | NO_ITEMS | Compliance references consistent across docs |
| F:operative:necessity | operative | necessity | Verified Operational Readiness | 1 | HAS_ITEMS | Prerequisite status tracking gap |
| F:operative:sufficiency | operative | sufficiency | Competent Execution Basis | 0 | NO_ITEMS | Personnel prerequisites adequate |
| F:operative:completeness | operative | completeness | Complete Procedural Authority | 0 | NO_ITEMS | Steps 1-8 with verification table provide complete authority |
| F:operative:consistency | operative | consistency | Systematic Execution Coherence | 0 | NO_ITEMS | Procedure cross-references to Specification are coherent |
| F:evaluative:necessity | evaluative | necessity | Verified Intrinsic Worth | 0 | NO_ITEMS | OBJ linkage adequate |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Judgment | 0 | NO_ITEMS | Trade-offs defer to human ruling appropriately |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Authority | 1 | HAS_ITEMS | No lifecycle cost consideration |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Stability | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Guidance | Guidance | Add note in Guidance explaining basis for each ASSUMPTION-tagged standard (why it is likely applicable) to support defensible regulatory justification until confirmed | Five standards are marked ASSUMPTION. A defensible regulatory justification requires at minimum a documented rationale for why each is believed applicable, even before formal confirmation. | Specification.md, Guidance.md | Specification Standards table; Guidance entire document scanned | -- | Structural Engineer (PROPOSAL) | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add a "Standards Search Record" or note documenting which code/standard sources were checked and which were not accessible, to support an exhaustive governance record | The Specification Standards table Note says "No technical standards documents were accessible" but does not record what was searched. An exhaustive governance record requires documenting what was checked, not just what was found. | Specification.md | Standards table Note | -- | Document author (PROPOSAL) | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a prerequisites status-tracking mechanism (checklist or status column update protocol) to confirm each prerequisite is available before proceeding to Step 2 | Procedure Prerequisites table lists items with status but provides no protocol for confirming readiness before proceeding. Verified operational readiness requires an explicit go/no-go check. | Procedure.md | Prerequisites table | -- | Structural Engineer (PROPOSAL) | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration for lifecycle/maintenance implications of embedded steel plates (replaceability, corrosion protection, future re-surfacing) | Guidance considers design, coordination, and timing trade-offs but does not address lifecycle or maintenance considerations for the embedded plates. Exhaustive worth authority should include long-term value implications. | Guidance.md | Considerations section (entire) | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Governance Mandate | 0 | NO_ITEMS | Governance mandate (code compliance + P.Eng. stamp) clearly resolved |
| D:normative:applying | normative | applying | Justified Code Enactment | 0 | NO_ITEMS | REQ-007 and REQ-008 provide code enactment path |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 1 | HAS_ITEMS | No final conformance sign-off step |
| D:normative:reviewing | normative | reviewing | Assured Conformance Oversight | 0 | NO_ITEMS | Step 7 coordination review provides oversight |
| D:operative:guiding | operative | guiding | Confirmed Workflow Course | 0 | NO_ITEMS | Steps 1-8 confirm the workflow |
| D:operative:applying | operative | applying | Grounded Task Implementation | 0 | NO_ITEMS | Tasks are grounded in cross-referenced sources |
| D:operative:judging | operative | judging | Resolved Capability Authority | 1 | HAS_ITEMS | CAD technician qualifications unspecified |
| D:operative:reviewing | operative | reviewing | Confirmed Process Discipline | 0 | NO_ITEMS | Internal QA (Step 6) and coordination review (Step 7) adequate |
| D:evaluative:guiding | evaluative | guiding | Grounded Merit Direction | 0 | NO_ITEMS | OBJ-001/OBJ-003 provide grounded direction |
| D:evaluative:applying | evaluative | applying | Justified Worth Delivery | 0 | NO_ITEMS | Deliverable relationship to DEL-011-02 documented |
| D:evaluative:judging | evaluative | judging | Conclusive Value Ruling | 0 | NO_ITEMS | Trade-offs defer to human; appropriate at this stage |
| D:evaluative:reviewing | evaluative | reviewing | Reliable Excellence Review | 1 | HAS_ITEMS | No independent review step |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Procedure | Procedure | Add explicit conformance sign-off step (or checklist) in Procedure confirming all REQ-001 through REQ-010 are satisfied before P.Eng. stamping | Procedure Step 6 mentions review against code requirements and RFP but does not include a structured sign-off confirming each Specification requirement is met. A conclusive conformance ruling requires explicit requirement-by-requirement confirmation. | Procedure.md | Step 6 -- Internal Quality Review | -- | Structural Engineer (PROPOSAL) | TBD |
| D-002 | D:operative:judging | WeakStatement | Procedure | Procedure | Clarify minimum qualification or oversight requirement for CAD technician (e.g., "under direct supervision of the responsible P.Eng.") | Procedure lists "Drafting resource (CAD technician)" as a personnel prerequisite but does not specify qualification requirements or supervision structure. Resolved capability authority requires clarity on who is qualified to execute. | Procedure.md | Personnel Prerequisites | -- | Structural Engineer (PROPOSAL) | TBD |
| D-003 | D:evaluative:reviewing | MissingSlot | Procedure | Procedure | Add independent peer review step (or note that Step 7 coordination review serves this function) before P.Eng. stamping | Procedure Step 6 is "Internal Quality Review" (self-review by the Structural Engineer) and Step 7 is inter-discipline coordination. Neither explicitly constitutes an independent technical peer review. Reliable excellence review typically requires a reviewer other than the originator. | Procedure.md | Steps 6, 7 | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Course Mandate | 0 | NO_ITEMS | Course mandate is clear: produce IFC drawing set |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Directional Authority | 1 | HAS_ITEMS | Drawing scale not specified as requirement |
| X:guiding:completeness | guiding | completeness | Exhaustive Authority Documentation | 0 | NO_ITEMS | Documentation scope adequate |
| X:guiding:consistency | guiding | consistency | Harmonized Authority Measure | 0 | NO_ITEMS | Authority (P.Eng.) consistently referenced |
| X:applying:necessity | applying | necessity | Verified Implementation Basis | 1 | HAS_ITEMS | Anchor design standard unverified |
| X:applying:sufficiency | applying | sufficiency | Defensible Practice Competence | 0 | NO_ITEMS | Professional competence deferred to P.Eng. |
| X:applying:completeness | applying | completeness | Full Implementation Record | 1 | HAS_ITEMS | No revision management protocol |
| X:applying:consistency | applying | consistency | Consistent Enactment Measure | 0 | NO_ITEMS | Enactment measures consistent |
| X:judging:necessity | judging | necessity | Decisive Conformance Verdict | 0 | NO_ITEMS | Verification table covers all requirements |
| X:judging:sufficiency | judging | sufficiency | Justified Capability Finding | 0 | NO_ITEMS | Capability deferred to P.Eng. appropriately |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 1 | HAS_ITEMS | No coordination response log template |
| X:judging:consistency | judging | consistency | Reliable Adjudication Gauge | 0 | NO_ITEMS | Verification approaches are consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Conformance Checkpoint | 1 | HAS_ITEMS | Geotech assumption flag checkpoint |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Audit Foundation | 0 | NO_ITEMS | Audit foundation present in verification tables |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Ledger | 0 | NO_ITEMS | Records section covers required outputs |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Measure | 0 | NO_ITEMS | Audit measures consistent between Specification and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add verification criterion for drawing scale appropriateness (e.g., confirm scale is sufficient for field layout without interpolation) | Procedure Step 4.1 mentions "scale appropriate for construction use (TBD by Structural Engineer; typically 1:100 or 1:50)" but Specification REQ-010 does not include scale as a verifiable requirement. Warranted directional authority requires that drawing legibility for field use be verifiable. | Specification.md, Procedure.md | Specification REQ-010; Procedure Step 4.1 | -- | Structural Engineer (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm which anchor design standard applies (CSA A23.3 Annex D or equivalent) and specific edition, to establish verified implementation basis for anchor design | Specification Standards table lists CSA A23.3 as ASSUMPTION for anchor design. Procedure Step 2.3 references "Anchor capacity in shear and tension per CSA A23.3 (ASSUMPTION: applicable)." Verified implementation requires a confirmed standard, not an assumption. | Specification.md, Procedure.md | Specification Standards table (CSA A23.3 row); Procedure Step 2.3 | -- | Structural Engineer | TBD |
| X-003 | X:applying:completeness | MissingSlot | Procedure | Procedure | Add drawing revision management protocol (how revisions are numbered, tracked, and re-issued if design parameters change post-geotech) | Procedure Step 8.3 mentions "IFC Rev 0" but no revision management protocol is described for handling post-geotech or post-coordination revisions. A full implementation record requires a defined revision workflow. | Procedure.md | Step 8 -- P.Eng. Stamp and IFC Issue | -- | Project team (PROPOSAL) | TBD |
| X-004 | X:judging:completeness | VerificationGap | Procedure | Procedure | Add template or protocol for logging coordination review comments and resolutions from Step 7 inter-discipline review | Procedure Step 7.2 says "Document responses and any drawing revisions" but provides no template, log format, or required fields. Exhaustive adjudication requires a structured record of what was reviewed and how it was resolved. | Procedure.md | Step 7 -- Issue for Review / Coordination | -- | Project team (PROPOSAL) | TBD |
| X-005 | X:reviewing:necessity | Conflict | Multi | Multi | Resolve whether geotech assumption flag is a mandatory drawing note (Procedure says "must clearly note") vs. optional (Specification does not require it) | Procedure Prerequisites Note says the Structural Engineer "must clearly note the assumption on drawings" if geotech is pending. However, Specification REQ-005 requires coordination with DEL-002-02 but does not mandate an assumption flag on drawings. This creates ambiguity about whether the flag is a requirement or guidance. | Procedure.md, Specification.md | Procedure Prerequisites Note on Geotech; Specification REQ-005 | Procedure.md#Prerequisites Note on Geotech; Specification.md#REQ-005 | Specification (normative document) should govern (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Warranted Governance Trail | 0 | NO_ITEMS | Governance trail (RFP -> Decomp -> Deliverable) documented |
| E:guiding:information | guiding | information | Coherent Governance Account | 0 | NO_ITEMS | Governance account coherent across Purpose sections |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Steering Mastery | 0 | NO_ITEMS | Steering knowledge adequate in Guidance Principles |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Foresight | 0 | NO_ITEMS | Foresight captured in Considerations and Trade-offs |
| E:applying:data | applying | data | Demonstrated Execution Record | 1 | HAS_ITEMS | No IFC distribution checklist |
| E:applying:information | applying | information | Warranted Practice Account | 0 | NO_ITEMS | Practice account consistent across Procedure and Specification |
| E:applying:knowledge | applying | knowledge | Warranted Execution Proficiency | 0 | NO_ITEMS | Proficiency requirements met via P.Eng. requirement |
| E:applying:wisdom | applying | wisdom | Principled Implementation Insight | 0 | NO_ITEMS | Implementation insight in Guidance Considerations |
| E:judging:data | judging | data | Definitive Adjudication Record | 0 | NO_ITEMS | Verification tables provide structured adjudication |
| E:judging:information | judging | information | Unambiguous Judgment Account | 1 | HAS_ITEMS | 50,000L water storage coordination unclear |
| E:judging:knowledge | judging | knowledge | Thorough Adjudication Mastery | 0 | NO_ITEMS | Adjudication scope adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Foresight | 0 | NO_ITEMS | Conflict table in Guidance provides foresight |
| E:reviewing:data | reviewing | data | Validated Inspection Trail | 1 | HAS_ITEMS | Normalization needed |
| E:reviewing:information | reviewing | information | Comprehensive Oversight Account | 0 | NO_ITEMS | Oversight information adequate |
| E:reviewing:knowledge | reviewing | knowledge | Thorough Oversight Proficiency | 0 | NO_ITEMS | Oversight proficiency implied by P.Eng. |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Foresight in Guidance Conflict Table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | RationaleGap | Procedure | Guidance | Add rationale for IFC distribution list (why County PM, GC, and document control are the required recipients) and confirm whether other parties (e.g., building inspector, subtrades) need copies | Procedure Step 8.4 lists three distribution targets but provides no rationale for why this list is complete. Demonstrated execution record requires a justified distribution scope. | Procedure.md | Step 8.4 | -- | Project team (PROPOSAL) | TBD |
| E-002 | E:judging:information | Normalization | Multi | Multi | Normalize reference to 50,000 L water storage: Procedure Step 3.2 mentions it as a coordination item but Specification and Datasheet do not reference it; clarify whether this is in scope for conflict avoidance | Procedure Step 3.2 lists "50,000 L water storage footprint (confirm with DEL-001-02 and DEL-006-04)" as a coordination item, but this element does not appear in Specification REQ-006 (conflict avoidance) or Datasheet Interface Conditions. This inconsistency risks oversight. | Procedure.md, Specification.md, Datasheet.md | Procedure Step 3.2; Specification REQ-006; Datasheet Interface Conditions | -- | Specification should be updated if this is a real coordination constraint (PROPOSAL) | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Multi | Normalize deliverable cross-references: Datasheet uses "DEL-006-03 / DEL-014-04" for wash bay drainage; Procedure Step 3.2 adds "DEL-006-04"; confirm correct deliverable IDs | Datasheet Interface Conditions references "DEL-006-03 / DEL-014-04" for wash bay drainage coordination. Procedure Step 3.2 references "DEL-006-04" for water storage. These may be different deliverables or a typo. Validated inspection trail requires consistent cross-references. | Datasheet.md, Procedure.md | Datasheet Interface Conditions; Procedure Step 3.2 | -- | Decomposition document (PROPOSAL) | TBD |
