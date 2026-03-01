# Semantic Lensing Register: DEL-003-05 Mechanical Equipment Schedule

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-003_Mechanical Design/1_Working/DEL-003-05_Equipment-Schedule/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-05_Equipment-Schedule/_CONTEXT.md
- _STATUS.md — DEL-003-05_Equipment-Schedule/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-05_Equipment-Schedule/_SEMANTIC.md
- Datasheet.md — DEL-003-05_Equipment-Schedule/Datasheet.md
- Specification.md — DEL-003-05_Equipment-Schedule/Specification.md
- Guidance.md — DEL-003-05_Equipment-Schedule/Guidance.md
- Procedure.md — DEL-003-05_Equipment-Schedule/Procedure.md
- _REFERENCES.md — DEL-003-05_Equipment-Schedule/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 6
  - Specification: 9
  - Guidance: 3
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 5  C: 3  F: 3  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 9
  - WeakStatement: 4
  - RationaleGap: 2
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Heating system interpretation ambiguity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code standard editions unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ inspection criteria absent |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately described |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing wash bay ventilation resolution step |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps well-structured |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative acceptance criteria for TBD values |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit checks present in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation covered in Guidance trade-offs |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application implicit in equipment selection rationale |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination deferred to engineering judgment |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC review step adequate in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Multi | Guidance | Clarify definition of "high-recovery heating system" -- the RFP phrase is undefined and the Guidance acknowledges multiple technology interpretations without establishing a decision framework or threshold for "high-recovery" | The term "high-recovery" governs a major equipment selection (HTG-001) but has no operational definition anywhere in the document set; this creates prescriptive ambiguity that could lead to materially different designs | Guidance.md, Datasheet.md | Guidance.md #3.1, Datasheet.md #2.2 (HTG-001 row) | | PROPOSAL: Mechanical Engineer to define in DEL-003-06; record definition in Guidance | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record specific editions of Alberta Building Code, ASHRAE 62.1, ASHRAE 90.1, NFPA 91, and ACGIH referenced -- all are listed as "edition TBD" or "location TBD" | Mandatory practice requires specific code editions to determine applicable clause-level requirements; without editions, compliance determination is indeterminate | Specification.md | Specification.md #3 (Standards table) | | PROPOSAL: Mechanical Engineer to confirm applicable editions at design start | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria or pass/fail thresholds for REQ-013 (Code Compliance) -- the verification method is "AHJ inspection; building permit process" but no specific compliance checklist or submission requirements are stated | Compliance determination requires defined acceptance criteria; current verification method is a placeholder pointing to external process without specifying what the deliverable must demonstrate | Specification.md | Specification.md #4.1 (Verification Matrix, REQ-013 row) | | PROPOSAL: Mechanical Engineer to define code compliance verification checklist items | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit step in Phase 1 or Phase 2 for resolving wash bay ventilation scope (Guidance #3.7 identifies the gap but Procedure contains no corresponding resolution step) | Procedural direction is missing for a known scope ambiguity; the Guidance identifies the wash bay ventilation gap but the Procedure does not include a step to resolve it | Procedure.md | Procedure.md #3 (Steps -- Phase 1 and Phase 2); cf. Guidance.md #3.7 | | PROPOSAL: Add step between 1.1 and 1.2 or as 1.1a | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Define how "IFC schedule shall not contain TBD values in required performance fields" (Procedure Step 3.3) is verified -- no corresponding requirement or verification row exists in Specification for the no-TBD-at-IFC rule | Performance assessment at IFC requires a verification method for confirming all TBD values are resolved; this is stated in Procedure but not formalized in Specification verification matrix | Procedure.md, Specification.md | Procedure.md #3 (Step 3.3); Specification.md #4.1 | | PROPOSAL: Add REQ-016 or equivalent in Specification with verification method | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Climate design temperatures TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | R-05 Electrical appendix not read |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Service pit equipment tag EXH-004 placeholder only |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistently sourced where present |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing CSA B149.1 in Datasheet references |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for scaffold stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account comprehensive for available inputs |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Inconsistent standard listing across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Engineering fundamentals deferred to P.Eng. |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery deferred to Mechanical Engineer |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment points identified in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls appropriately flagged as assumptions |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record outdoor design temperatures for heating and cooling -- these are essential facts for equipment sizing but are listed as TBD with an assumption of "approximately -35C or colder" | Essential data for heating load calculations (HTG-001, MAU-001 sizing) remains TBD; the assumption of -35C is not confirmed and could affect equipment capacity significantly | Datasheet.md | Datasheet.md #3.1 (Operating Conditions table) | | PROPOSAL: Mechanical Engineer to confirm from Alberta climate data or ASHRAE weather tables | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Note that R-05 (Appendix B Electrical) is cited as source for ceiling fan count (6x) but listed as "Not directly read; cited in decomposition" -- the evidence chain relies on indirect citation | Adequate evidence for CF-001 through CF-006 quantity and placement relies on a reference that was not directly read; if the reference contains relevant constraints (fan locations, circuit assignments), those are unavailable | Datasheet.md | Datasheet.md #5 (References table, R-05 row) | | PROPOSAL: Read R-05 directly and update equipment register if additional constraints are found | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add EXH-004 (service pit ventilation) as a formal row in the Equipment Register table with TBD values, rather than only as a note -- currently it is mentioned only in a note below the table as "Tag reserved: EXH-004 (TBD)" | A comprehensive equipment record should include all anticipated equipment as rows, even if performance values are TBD; the current note-only treatment risks the item being overlooked in downstream coordination | Datasheet.md | Datasheet.md #2.2 (note after Equipment Register table) | | PROPOSAL: Add EXH-004 row to Equipment Register table | TBD |
| B-004 | B:information:necessity | Normalization | Multi | Specification | Add CSA B149.1 to Datasheet references table and Procedure required references -- it appears in Specification #3 (Standards) and Procedure #2.2 but is absent from Datasheet #5 (References) | An essential signal (gas installation code applicability) is present in two documents but absent from the third, creating an inconsistent reference register | Specification.md, Procedure.md, Datasheet.md | Specification.md #3 (Standards); Procedure.md #2.2; Datasheet.md #5 (References) | | PROPOSAL: Add CSA B149.1 to Datasheet References table | TBD |
| B-005 | B:information:consistency | Normalization | Multi | Multi | Harmonize the list of applicable standards across all four documents -- Specification lists CSA B149.1, Procedure lists CSA B149.1 and ACGIH, Datasheet lists ACGIH and NFPA 91 but not CSA B149.1, Guidance does not list standards explicitly | Standards referenced inconsistently across documents; a reader checking any single document gets an incomplete picture of applicable codes | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Datasheet.md #5; Specification.md #3; Procedure.md #2.2; Guidance.md (entire document scanned) | | PROPOSAL: Create a single canonical standards list and reference it consistently | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Imperative | 1 | HAS_ITEMS | Wash bay ventilation scope ambiguity |
| C:normative:sufficiency | normative | sufficiency | Certified Substantiation | 0 | NO_ITEMS | Substantiation pathway clear via P.Eng. stamp |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | No air curtain / vestibule mention |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Discipline | 0 | NO_ITEMS | Regulatory references consistent where present |
| C:operative:necessity | operative | necessity | Critical Operational Threshold | 0 | NO_ITEMS | Operational thresholds deferred to calculations |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Competence | 0 | NO_ITEMS | Competence requirements clear |
| C:operative:completeness | operative | completeness | Exhaustive Process Traceability | 1 | HAS_ITEMS | Drawing cross-reference traceability gap |
| C:operative:consistency | operative | consistency | Reproducible Operational Fidelity | 0 | NO_ITEMS | Procedures reproducible as written |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Discernment | 0 | NO_ITEMS | Value discernment present in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Quality Benchmark | 0 | NO_ITEMS | Quality benchmarks deferred to standards |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Mastery | 0 | NO_ITEMS | Valuation scope adequate for scaffold |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Conflict | Multi | Specification | Service pit ventilation (SOW-0028) is required by RFP but not enumerated in mechanical equipment list (SOW-0035 through SOW-0040) -- Specification REQ-010 addresses this but the Datasheet only reserves a tag in a note, creating a gap between the authoritative imperative (RFP requirement) and the equipment register | The RFP mandates ventilated service pit (SOW-0028) but the mechanical scope items (SOW-0035-0040) do not include it; this is a scope boundary conflict between the RFP's functional requirement and the enumerated mechanical work items | Datasheet.md, Specification.md | Datasheet.md #2.2 (note re EXH-004); Specification.md #2.1 (REQ-010) | Datasheet.md#2.2 (note only), Specification.md#2.1 REQ-010 (conditional requirement) | PROPOSAL: Mechanical Engineer to confirm scope inclusion and add to Datasheet equipment register | TBD |
| C-002 | C:normative:completeness | MissingSlot | Guidance | Guidance | Add consideration of air curtain or vestibule strategy for overhead doors -- Guidance #3.2 discusses MAU sizing for infiltration when doors are open but does not mention air curtains as an alternative or complement, despite this being a standard industrial approach | Exhaustive regulatory coverage for infiltration control in high-bay industrial shops typically includes evaluation of air curtain options; the Guidance discusses the problem but omits a known solution category | Guidance.md | Guidance.md #3.2 (Makeup Air Unit Sizing Criticality) | | PROPOSAL: Add air curtain consideration to Guidance #3.2 or Guidance #4 (Trade-offs) | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement for drawing-to-schedule tag reconciliation as a formal verification step -- REQ-015 requires the cross-reference field but no verification method confirms bidirectional tag consistency (schedule tags appearing on drawings AND drawing tags appearing in schedule) | Exhaustive process traceability requires bidirectional reconciliation; the current verification is one-directional ("schedule tags match drawing tags") but does not verify completeness in the other direction | Specification.md | Specification.md #2.2 (REQ-015); #4.1 (Verification Matrix, REQ-015 row) | | PROPOSAL: Update REQ-015 verification to require bidirectional reconciliation | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Compliance Foundation | 1 | HAS_ITEMS | County approval dependency timing |
| F:normative:sufficiency | normative | sufficiency | Mandated Compliance Proficiency | 0 | NO_ITEMS | Compliance proficiency pathway clear |
| F:normative:completeness | normative | completeness | Absolute Governance Archive | 0 | NO_ITEMS | Governance archive scope adequate |
| F:normative:consistency | normative | consistency | Definitive Conformance Benchmark | 1 | HAS_ITEMS | Tag convention not confirmed |
| F:operative:necessity | operative | necessity | Validated Operational Baseline | 0 | NO_ITEMS | Operational baseline prerequisites documented |
| F:operative:sufficiency | operative | sufficiency | Substantiated Execution Capability | 0 | NO_ITEMS | Execution capability deferred to engineering |
| F:operative:completeness | operative | completeness | Absolute Procedural Mastery | 0 | NO_ITEMS | Procedure comprehensive for scaffold |
| F:operative:consistency | operative | consistency | Systematic Performance Stability | 0 | NO_ITEMS | Performance metrics consistently TBD |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Clarity | 1 | HAS_ITEMS | Lead time risk not quantified |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Judgment | 0 | NO_ITEMS | Worth judgment deferred to engineering selection |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Authority | 0 | NO_ITEMS | Valuation scope adequate |
| F:evaluative:consistency | evaluative | consistency | Harmonized Appraisal Integrity | 0 | NO_ITEMS | Appraisal approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Procedure | Guidance | Add rationale for why County approval of DEL-003-01 is a hard gate before IFC equipment selections -- the requirement is stated in Specification (REQ-012) and Procedure (Step 2.6) but the Guidance does not explain what happens if County approval is delayed or conditional | The obligatory compliance foundation (County approval gate) is documented as a requirement but its rationale and failure-mode handling are not addressed; a delay in County approval could cascade to project schedule | Procedure.md, Specification.md | Procedure.md #3 (Step 2.6); Specification.md #2.1 (REQ-012); Guidance.md (entire document scanned) | | PROPOSAL: Add to Guidance #2.4 a note on schedule impact if County approval is delayed | TBD |
| F-002 | F:normative:consistency | WeakStatement | Specification | Specification | Strengthen REQ-002 tag convention from "ASSUMPTION: system prefix + sequential number" to a definitive tag scheme or explicitly require the Mechanical Engineer to establish and document the convention before schedule population | The tag convention is stated as an assumption in both Datasheet and Specification; if different team members interpret the assumption differently, tags across schedule and drawings may diverge | Specification.md, Datasheet.md | Specification.md #2.1 (REQ-002); Datasheet.md #2.2 (Equipment Tag Scheme heading) | | PROPOSAL: Mechanical Engineer to confirm tag convention at project start; update REQ-002 to remove ASSUMPTION qualifier | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add guidance on how to evaluate equipment lead time risk against the December 31, 2026 deadline -- Guidance #4.1 mentions lead time as a factor but does not provide a decision framework or threshold for when a long-lead item triggers early procurement action | Fundamental merit clarity requires that the value trade-off between lead time and equipment specification be operationalized; current guidance is directional but lacks actionable thresholds | Guidance.md | Guidance.md #4.1 (Equipment Efficiency vs. First Cost vs. Lead Time) | | PROPOSAL: Add decision threshold or checklist for long-lead procurement triggers | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Prescriptive Anchor | 0 | NO_ITEMS | Prescriptive anchor established by RFP references |
| D:normative:applying | normative | applying | Enforced Adherence Capability | 1 | HAS_ITEMS | No change management process defined |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling process clear via AHJ |
| D:normative:reviewing | normative | reviewing | Confirmed Compliance Examination | 0 | NO_ITEMS | Compliance examination via P.Eng. stamp |
| D:operative:guiding | operative | guiding | Anchored Workflow Navigation | 0 | NO_ITEMS | Workflow navigation adequate in Procedure |
| D:operative:applying | operative | applying | Verified Practical Delivery | 1 | HAS_ITEMS | Coordination records format unspecified |
| D:operative:judging | operative | judging | Confirmed Performance Authority | 0 | NO_ITEMS | Performance authority via P.Eng. and DEL-003-06 |
| D:operative:reviewing | operative | reviewing | Systematic Operational Assurance | 0 | NO_ITEMS | Operational assurance via QC review step |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Guidance | 0 | NO_ITEMS | Value guidance present in Guidance document |
| D:evaluative:applying | evaluative | applying | Confirmed Quality Realization | 1 | HAS_ITEMS | No quality gate between prelim and IFC |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Adjudication | 0 | NO_ITEMS | Quality adjudication via QC review |
| D:evaluative:reviewing | evaluative | reviewing | Rigorous Valuation Examination | 0 | NO_ITEMS | Valuation examination deferred to commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add requirement for change management when equipment selections deviate from preliminary design approved by County -- Specification REQ-012 requires County approval of preliminary design but does not address what constitutes a material change requiring re-approval | Enforced adherence capability requires a defined process for handling deviations from the approved baseline; without this, changes could be made without County awareness | Specification.md | Specification.md #2.1 (REQ-012) | | PROPOSAL: Add REQ-016 or note under REQ-012 defining material change threshold | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Specify format or minimum content for coordination records in Step 3.2 -- currently stated as "email or meeting minutes, filed per project QC protocol" without defining what constitutes adequate coordination evidence | Verified practical delivery requires that coordination with Structural and Electrical engineers produce records with defined content; "email or meeting minutes" is too vague to ensure adequate evidence of coordination | Procedure.md | Procedure.md #3 (Step 3.2) | | PROPOSAL: Define minimum coordination record content (e.g., confirmed load data, agreed electrical characteristics) | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Procedure | Procedure | Add explicit quality gate or hold point between preliminary schedule (Phase 2) and IFC schedule (Phase 3) to confirm that County-approved equipment selections have not materially changed | Confirmed quality realization requires a checkpoint ensuring the IFC schedule remains consistent with the County-approved preliminary design; no such gate exists between Phase 2 and Phase 3 | Procedure.md | Procedure.md #3 (between Phase 2 and Phase 3) | | PROPOSAL: Add hold point or checklist between Step 2.6 and Step 3.1 | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Purposeful Foundational Direction | 0 | NO_ITEMS | Foundational direction established |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Guidance Capacity | 1 | HAS_ITEMS | Overhead crane coordination missing |
| X:guiding:completeness | guiding | completeness | Holistic Steering Mastery | 0 | NO_ITEMS | Steering scope adequate |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Coherence | 0 | NO_ITEMS | Directional coherence maintained |
| X:applying:necessity | applying | necessity | Validated Implementation Reality | 1 | HAS_ITEMS | Electrical load data gap |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Implementation Proof | 0 | NO_ITEMS | Implementation proof deferred to IFC |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Mastery | 1 | HAS_ITEMS | Missing vibration/noise data fields |
| X:applying:consistency | applying | consistency | Stable Implementation Coherence | 0 | NO_ITEMS | Implementation coherence maintained |
| X:judging:necessity | judging | necessity | Binding Adjudication Reality | 1 | HAS_ITEMS | No acceptance criteria for REQ-004 through REQ-009 |
| X:judging:sufficiency | judging | sufficiency | Justified Determination Evidence | 0 | NO_ITEMS | Determination evidence pathways clear |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Record | 0 | NO_ITEMS | Adjudication record scope adequate |
| X:judging:consistency | judging | consistency | Consistent Adjudication Fidelity | 0 | NO_ITEMS | Adjudication consistency maintained |
| X:reviewing:necessity | reviewing | necessity | Thorough Scrutiny Foundation | 1 | HAS_ITEMS | Peer review independence not specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Examination Evidence | 0 | NO_ITEMS | Examination evidence pathways clear |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Examination Record | 0 | NO_ITEMS | Examination record scope adequate |
| X:reviewing:consistency | reviewing | consistency | Harmonized Examination Fidelity | 0 | NO_ITEMS | Examination fidelity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Guidance | Guidance | Add guidance on coordinating ceiling fan locations with overhead crane layout (SOW-0067, two 5-tonne cranes) -- Guidance #3.5 mentions this coordination need but only in passing; no guidance on conflict resolution if crane girders and fan positions interfere | Substantiated guidance capacity requires actionable direction on a known interference risk; the current mention is awareness-level only, not guidance-level | Guidance.md | Guidance.md #3.5 (Ceiling Fan Coordination with Structure) | | PROPOSAL: Expand Guidance #3.5 with coordination protocol or decision rule | TBD |
| X-002 | X:applying:necessity | TBD_Question | Datasheet | Datasheet | Record electrical load summary per equipment item (phase, voltage, FLA/RLA) -- the Datasheet Equipment Register does not include electrical characteristics columns although Specification REQ-003 requires "connection requirements (electrical characteristics)" | Validated implementation reality requires electrical data for each equipment item to enable coordination with PKG-004; this data category is required by Specification but absent from the Datasheet register format | Datasheet.md, Specification.md | Datasheet.md #2.2 (Equipment Register table columns); Specification.md #2.1 (REQ-003) | | PROPOSAL: Add electrical characteristics columns to Datasheet equipment register table | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add data fields for equipment weight, vibration characteristics, and acoustical data (sound power/pressure levels) to REQ-003 minimum data fields -- Procedure Step 3.2 requires providing "equipment weights, vibration characteristics, and mounting requirements" to Structural Engineer but REQ-003 does not require these as schedule data fields | Exhaustive implementation mastery requires that all data needed for downstream coordination be captured in the schedule; weight and vibration data are needed for structural coordination but not required by the specification | Specification.md, Procedure.md | Specification.md #2.1 (REQ-003); Procedure.md #3 (Step 3.2) | | PROPOSAL: Add weight, vibration, and acoustical data to REQ-003 minimum fields | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add specific acceptance criteria for REQ-004 through REQ-009 (performance parameter requirements) -- the verification method is "Engineering calculation review (DEL-003-06); design team QC" but no pass/fail criteria are stated (e.g., minimum heating capacity, minimum airflow) | Binding adjudication reality requires that each performance requirement have measurable acceptance criteria; currently the verification is "review" without defining what constitutes acceptable values | Specification.md | Specification.md #4.1 (Verification Matrix, REQ-004 to REQ-009 row) | | PROPOSAL: Add acceptance criteria column to verification matrix or note that criteria are derived from DEL-003-06 calculations | TBD |
| X-005 | X:reviewing:necessity | WeakStatement | Procedure | Procedure | Clarify whether QC review in Step 3.5 is self-review or independent peer review -- the text says "Mechanical Engineer (or a qualified peer reviewer)" which allows self-review as the default | Thorough scrutiny foundation requires clarity on reviewer independence; the parenthetical "(or a qualified peer reviewer)" implies peer review is optional, which weakens the QC gate | Procedure.md | Procedure.md #3 (Step 3.5) | | PROPOSAL: Specify whether peer review is required or optional; if optional, state conditions under which it becomes required | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 1 | HAS_ITEMS | Indoor temperature assumptions not reconciled |
| E:guiding:information | guiding | information | Integrated Directional Insight | 0 | NO_ITEMS | Directional insight integrated across Guidance |
| E:guiding:knowledge | guiding | knowledge | Masterful Directional Authority | 0 | NO_ITEMS | Directional authority deferred to P.Eng. |
| E:guiding:wisdom | guiding | wisdom | Principled Navigational Foresight | 0 | NO_ITEMS | Navigational foresight present in trade-offs |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Equipment quantities inconsistent |
| E:applying:information | applying | information | Substantiated Delivery Account | 0 | NO_ITEMS | Delivery account adequate |
| E:applying:knowledge | applying | knowledge | Masterful Execution Authority | 0 | NO_ITEMS | Execution authority clear |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 0 | NO_ITEMS | Execution foresight present |
| E:judging:data | judging | data | Definitive Verdict Record | 1 | HAS_ITEMS | Verification milestone timing |
| E:judging:information | judging | information | Grounded Adjudication Insight | 0 | NO_ITEMS | Adjudication insight adequate |
| E:judging:knowledge | judging | knowledge | Masterful Adjudication Authority | 0 | NO_ITEMS | Adjudication authority clear |
| E:judging:wisdom | judging | wisdom | Principled Ruling Foresight | 0 | NO_ITEMS | Ruling foresight adequate |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | QC checklist not defined |
| E:reviewing:information | reviewing | information | Grounded Audit Insight | 0 | NO_ITEMS | Audit insight adequate |
| E:reviewing:knowledge | reviewing | knowledge | Masterful Audit Authority | 0 | NO_ITEMS | Audit authority clear |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Conflict | Datasheet | Datasheet | Reconcile indoor design temperature assumptions -- Datasheet #3.1 lists "minimum 18C (heavy industrial)" for Main Shop and "21C (light occupancy)" for Office, both as ASSUMPTIONs, but Guidance does not reference or confirm these values and no source document establishes them as design targets | The authoritative guidance record should establish design temperatures as confirmed data rather than unattributed assumptions; these values directly drive heating system sizing (HTG-001) and MAU-001 capacity | Datasheet.md, Guidance.md | Datasheet.md #3.1 (Operating Conditions, indoor temperatures); Guidance.md (entire document scanned -- no mention of indoor design temperatures) | Datasheet.md#3.1 (18C and 21C assumptions), Guidance.md (silent on indoor temperatures) | PROPOSAL: Mechanical Engineer to confirm indoor design temperatures and record basis in Guidance or DEL-003-06 | TBD |
| E-002 | E:applying:data | Normalization | Datasheet | Datasheet | Normalize equipment quantities -- the Datasheet Equipment Register lists "TBD" in the Qty column for all items except CF-001 through CF-006 (which shows "6"), but some items clearly have known quantities (e.g., HTG-001 is described as singular, EXH-001 and EXH-002 are one each) | The verified execution record requires that known quantities be stated rather than listed as TBD; quantities of 1 for discrete identified equipment items are inferable from the tag assignment and should be recorded | Datasheet.md | Datasheet.md #2.2 (Equipment Register table, Qty column) | | PROPOSAL: Populate Qty column with known values (1 each for HTG-001, AEX-001, MAU-001, EXH-001, EXH-002, EXH-003) | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Specify verification milestone timing relative to project schedule -- the Verification Matrix uses "IFC issue" and "Before IFC" as milestones but does not establish calendar dates or schedule dependencies that would allow tracking | The definitive verdict record requires verifiable milestones; "IFC issue" is a relative milestone that cannot be tracked without linking to the project schedule (December 31, 2026 completion deadline) | Specification.md | Specification.md #4.1 (Verification Matrix, Verification Milestone column) | | PROPOSAL: Add note linking verification milestones to project schedule or DEL-003-01 timeline | TBD |
| E-004 | E:reviewing:data | VerificationGap | Procedure | Procedure | Define QC review checklist content -- Procedure Step 3.5 references a QC review with enumerated checks, and Records #5 lists "QC review checklist" as an output, but no checklist template or minimum content is defined | The verified audit record requires that the QC checklist be defined before use, not created ad hoc at review time; the Records table anticipates the checklist but its content is undefined | Procedure.md | Procedure.md #3 (Step 3.5); #5 (Records table, row 7) | | PROPOSAL: Define QC checklist template content in Procedure or as an appendix | TBD |

---

## Matrices K, G, T -- Intermediate/Auxiliary Matrices

These matrices (K = transpose of D, G = truncation of B, T = transpose of B) are construction intermediates used to derive X and E. They do not serve as independent lenses. Per the agent protocol, only matrices A, B, C, F, D, X, and E are applied as lenses. K, G, and T are documented in _SEMANTIC.md for algebraic traceability but are not part of the lensing register.

---

*End of Semantic Lensing Register*
