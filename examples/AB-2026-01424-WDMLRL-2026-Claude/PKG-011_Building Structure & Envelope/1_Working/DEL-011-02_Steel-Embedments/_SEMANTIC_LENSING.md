# Semantic Lensing Register: DEL-011-02 Steel Plate Floor Embedments

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-011_Building Structure & Envelope/1_Working/DEL-011-02_Steel-Embedments/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-011-02_Steel-Embedments/_CONTEXT.md
- _STATUS.md — DEL-011-02_Steel-Embedments/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-011-02_Steel-Embedments/_SEMANTIC.md
- Datasheet.md — DEL-011-02_Steel-Embedments/Datasheet.md
- Specification.md — DEL-011-02_Steel-Embedments/Specification.md
- Guidance.md — DEL-011-02_Steel-Embedments/Guidance.md
- Procedure.md — DEL-011-02_Steel-Embedments/Procedure.md
- _REFERENCES.md — DEL-011-02_Steel-Embedments/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 6
  - Specification: 10
  - Guidance: 4
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 3
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction on embedment method |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Material grade mandatory practice is TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compliance determination for welding standards gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately covered in Specification and Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Concrete cure duration not specified in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps are detailed across Procedure phases |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered via verification tables |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit addressed through inspection hold points |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit quality acceptance criteria for surface finish |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered implicitly through trade-off table |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination covered through load rating certification |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal provisions present in Procedure verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify REQ-011-02-06 to state whether cast-in-place is mandatory or whether surface-mount is an acceptable alternative; currently hedged as ASSUMPTION throughout all documents | The prescriptive direction for the embedment method (cast-in-place vs. surface-mounted) is flagged as ASSUMPTION in Specification REQ-011-02-06, Guidance Principle 2, and Procedure Phase 2 header, yet the entire construction sequence depends on this choice. This is the single most consequential ambiguity in the deliverable. | Specification.md; Guidance.md; Procedure.md | Specification REQ-011-02-06; Guidance Principles #2; Procedure Phase 2 header | Guidance CON-011-02-01 identifies this conflict | PROPOSAL: Structural engineer via DEL-002-08 | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm steel plate material grade (CSA G40.20/G40.21 vs. ASTM A36 vs. other) once DEL-002-12 is issued; currently stated as ASSUMPTION in both Datasheet and Specification | Mandatory practice for material grade cannot be enforced when the grade itself is unconfirmed. REQ-011-02-04 explicitly defers to DEL-002-12. | Specification.md; Datasheet.md | Specification REQ-011-02-04; Datasheet Attributes Material | -- | PROPOSAL: Structural engineer via DEL-002-12 | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add explicit acceptance criteria for welding inspection: specify which CSA standard (W59 or W47.1) governs acceptance/rejection of anchorage welds; currently stated as ASSUMPTION in Specification REQ-011-02-08 | Compliance determination for welding quality requires a named standard with defined acceptance criteria. The Specification references CSA W47.1/W59 as ASSUMPTION only, leaving the compliance basis ambiguous. | Specification.md | Specification REQ-011-02-08; Verification table row for REQ-011-02-06 | -- | PROPOSAL: Structural engineer via DEL-002-12 | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add concrete cure time requirement or cross-reference to DEL-011-01 concrete specification for minimum cure period before post-pour inspection (Step 11) | Procedural direction for Step 11 says "after concrete has reached sufficient cure" but does not state the required cure duration or reference a specific standard. The GC needs a defined threshold to schedule the post-pour inspection. | Procedure.md | Procedure Step 11 | -- | PROPOSAL: DEL-011-01 concrete specification | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Specification | Specification | Add quantitative flush tolerance value (e.g., +/- X mm) or explicitly state it is deferred to DEL-002-08; currently REQ-011-02-05 says "within the tolerance specified by the structural engineer" without a fallback value | Value orientation for surface finish quality lacks a measurable threshold. Without a stated tolerance, the GC and inspector cannot independently judge flush compliance until DEL-002-08 arrives. | Specification.md; Procedure.md | Specification REQ-011-02-05; Procedure Step 11 verification | -- | PROPOSAL: Structural engineer via DEL-002-08 | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Design load values are essential facts not yet present |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Plate dimensions not yet evidenced |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Record structure is comprehensive for what is known |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Bay width inconsistency potential |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (upstream dependencies, hold points) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for construction sequence is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive given current design stage |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Upstream dependency description inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of embedment purpose is clear |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed through qualification prerequisites |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for construction-stage deliverable |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment needs addressed via Guidance trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment provisions adequate in Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present through cross-deliverable references |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Specific design load values (kPa, point loads, dynamic amplification factors) are essential facts for this deliverable; confirm whether a placeholder load table should be added pending DEL-002-10 | Essential factual data for design loads is entirely deferred to DEL-002-10. While the deferral is appropriate, neither Datasheet nor Specification contains even placeholder load categories or ranges that would help the GC scope procurement and anchorage. | Datasheet.md; Specification.md | Datasheet Conditions Design Loads; Specification REQ-011-02-03 | -- | PROPOSAL: Structural engineer via DEL-002-10 | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Individual plate dimensions (length, width, thickness) are absent; add placeholder dimension table referencing DEL-002-08 for future population | Adequate evidence for plate geometry is entirely absent. Datasheet states "TBD" for plate thickness and individual plate dimensions. Without even approximate ranges, procurement lead time estimation is impossible. | Datasheet.md | Datasheet Attributes Quantity and Layout; Attributes Material | -- | PROPOSAL: Structural engineer via DEL-002-08 | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Datasheet | Standardize bay width representation: Datasheet uses "24'" (feet); verify this is consistent with metric/imperial convention used in DEL-002-08 structural drawings. If IFC drawings use metric, convert or dual-state the dimension. | Reliable measurement requires consistent units. Datasheet uses imperial (24') citing Appendix B R-04. If structural IFC drawings use metric (as is common in Alberta for structural work under ABC), a unit mismatch could cause field layout errors. | Datasheet.md | Datasheet Attributes Quantity and Layout | -- | PROPOSAL: Confirm with structural engineer | TBD |
| B-004 | B:information:consistency | Conflict | Multi | Specification | Resolve inconsistency in upstream dependency description: Datasheet says "concrete deck must be cured and ready before embedment installation" (implying post-cure), while Specification REQ-011-02-07 and Procedure correctly state plates are installed before pour. Datasheet wording is misleading. | Coherent messaging requires that all documents describe the construction sequence consistently. Datasheet Floor System Interface section implies plates go in after cure, contradicting the cast-in-place assumption used everywhere else. | Datasheet.md; Specification.md | Datasheet Floor System Interface; Specification REQ-011-02-07 Note | Datasheet.md#Floor System Interface vs. Specification.md#REQ-011-02-07 | PROPOSAL: Align Datasheet wording with Specification | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Basis | 1 | HAS_ITEMS | ABC edition not specified |
| C:normative:sufficiency | normative | sufficiency | Certified Obligatory Standing | 0 | NO_ITEMS | Certification requirements adequately described |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Standards table incomplete |
| C:normative:consistency | normative | consistency | Harmonized Adherence Standard | 0 | NO_ITEMS | Standards references are internally consistent |
| C:operative:necessity | operative | necessity | Essential Process Threshold | 0 | NO_ITEMS | Process thresholds covered via prerequisites |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Readiness | 0 | NO_ITEMS | Readiness criteria in Procedure prerequisites |
| C:operative:completeness | operative | completeness | Total Execution Coverage | 0 | NO_ITEMS | Execution steps comprehensive for cast-in-place method |
| C:operative:consistency | operative | consistency | Disciplined Process Coherence | 0 | NO_ITEMS | Process steps are coherent and sequenced |
| C:evaluative:necessity | evaluative | necessity | Irreducible Merit Foundation | 1 | HAS_ITEMS | Service life not stated |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Assessment | 0 | NO_ITEMS | Trade-off table provides defensible assessment |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Mastery | 0 | NO_ITEMS | Value considerations adequately covered |
| C:evaluative:consistency | evaluative | consistency | Consistent Value Reasoning | 0 | NO_ITEMS | Value reasoning consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Specify the applicable edition of the Alberta Building Code in REQ-011-02-08 or state "edition in force at time of permit issuance" explicitly; current wording says "applicable edition at time of permit issuance" which is acceptable but should be confirmed against the actual permit | The compulsory regulatory basis requires identifying the governing code edition. REQ-011-02-08 references ABC generally. Since code editions change and inspection obligations may differ between editions, this should be tightened once the building permit is obtained. | Specification.md | Specification REQ-011-02-08 | -- | PROPOSAL: GC to confirm at permit issuance | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add CSA A23.1/A23.2 (Concrete Materials and Methods of Concrete Construction) to Standards table as it governs the concrete interface zone where plates are embedded | Exhaustive compliance scope should include the concrete construction standard that governs the slab into which the plates are cast. The Specification Standards table lists steel and welding standards but omits the concrete construction standard that applies to the placement interface. | Specification.md | Specification Standards table | -- | PROPOSAL: Confirm with structural engineer | TBD |
| C-003 | C:evaluative:necessity | WeakStatement | Datasheet | Guidance | Clarify service life expectation: state whether embedments are designed for the full building service life (e.g., 40-50 years) or a shorter replacement cycle; current Datasheet says "TBD" | Irreducible merit foundation requires knowing the minimum expected service life to evaluate material selection and corrosion protection adequacy. The Datasheet notes "TBD" with an assumption of building service life, but this has not been confirmed and has implications for wash bay corrosion protection. | Datasheet.md | Datasheet Conditions Service Life | -- | PROPOSAL: Owner/structural engineer to confirm | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Integrated Statutory Mandate | 0 | NO_ITEMS | Statutory mandates identified and integrated |
| F:normative:sufficiency | normative | sufficiency | Justified Compliance Authority | 1 | HAS_ITEMS | P.Eng. stamp requirement incomplete |
| F:normative:completeness | normative | completeness | Total Compliance Archive | 1 | HAS_ITEMS | Documentation checklist gap |
| F:normative:consistency | normative | consistency | Principled Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are coherent |
| F:operative:necessity | operative | necessity | Verified Execution Criteria | 1 | HAS_ITEMS | Vibration plan not specified |
| F:operative:sufficiency | operative | sufficiency | Proficient Execution Benchmark | 0 | NO_ITEMS | Execution benchmarks covered through prerequisites |
| F:operative:completeness | operative | completeness | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution coverage comprehensive |
| F:operative:consistency | operative | consistency | Disciplined Operational Uniformity | 0 | NO_ITEMS | Operational consistency maintained |
| F:evaluative:necessity | evaluative | necessity | Grounded Quality Imperative | 1 | HAS_ITEMS | Corrosion protection not addressed |
| F:evaluative:sufficiency | evaluative | sufficiency | Competent Quality Threshold | 0 | NO_ITEMS | Quality thresholds adequate where specified |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Panorama | 0 | NO_ITEMS | Quality panorama adequate for current stage |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality reasoning coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification requirement: confirm that the load rating certification (REQ-011-02-03 verification) must be issued by a P.Eng. licensed in Alberta; currently the Verification table says "Structural engineer" but does not explicitly require P.Eng. stamp on the certification itself | Justified compliance authority requires that the load rating certification carry the same professional seal requirement as the IFC drawings (REQ-011-02-02 requires P.Eng. stamp). The verification for REQ-011-02-03 does not state the certification must be P.Eng.-sealed. | Specification.md | Specification Verification table row REQ-011-02-03 | -- | PROPOSAL: Align with REQ-011-02-02 P.Eng. requirement | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Procedure | Add as-built drawing submission to Specification Documentation table as a formally required artifact (currently listed in Procedure Records but not in Specification Documentation table) | Total compliance archive requires that all required documentation artifacts be listed consistently. Procedure Step 14 lists "As-built mark-up of DEL-002-08 drawings" but the Specification Documentation table lists "As-built mark-up" only as an ASSUMPTION. Cross-reference should be explicit. | Specification.md; Procedure.md | Specification Documentation table; Procedure Step 14 | -- | PROPOSAL: Add to Specification Documentation | TBD |
| F-003 | F:operative:necessity | WeakStatement | Procedure | Procedure | Specify concrete vibration/consolidation plan requirements in Step 9: currently says "Ensure vibration/consolidation plan does not disturb plate positions" but does not state what plan or approval is needed | Verified execution criteria for the concrete pour step require a defined vibration protocol near the embedments. The current wording acknowledges the risk but does not prescribe a verification method or responsible party for the vibration plan. | Procedure.md | Procedure Step 9 | -- | PROPOSAL: GC to develop vibration plan with concrete subcontractor | TBD |
| F-004 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale for whether corrosion protection (galvanizing, epoxy coating, or sacrificial thickness) is needed for steel plates in the wash bay given exposure to water, chemicals, and hydrocarbons; Guidance Considerations mentions it as a question but does not frame the decision criteria | Grounded quality imperative requires that the corrosion protection decision be framed with decision criteria, not just flagged as a consideration. The wash bay environment (water, chemicals, hydrocarbons) differs materially from the repair bay, potentially requiring different treatment. | Guidance.md | Guidance Considerations Interface with Wash Bay | -- | PROPOSAL: Structural engineer to address in DEL-002-12 | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Regulatory Command | 0 | NO_ITEMS | Regulatory command established through code references |
| D:normative:applying | normative | applying | Resolved Compulsory Implementation | 1 | HAS_ITEMS | Scope boundary for wash bay not resolved |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling framework present |
| D:normative:reviewing | normative | reviewing | Resolved Institutional Oversight | 0 | NO_ITEMS | Institutional oversight roles defined |
| D:operative:guiding | operative | guiding | Established Execution Steering | 0 | NO_ITEMS | Execution steering established via Procedure phases |
| D:operative:applying | operative | applying | Resolved Operational Delivery | 1 | HAS_ITEMS | Plate protection during pour not addressed |
| D:operative:judging | operative | judging | Settled Capability Verdict | 0 | NO_ITEMS | Capability assessment covered through verification |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Alignment | 0 | NO_ITEMS | Procedural alignment resolved across documents |
| D:evaluative:guiding | evaluative | guiding | Established Merit Direction | 0 | NO_ITEMS | Merit direction established through trade-offs |
| D:evaluative:applying | evaluative | applying | Resolved Value Deployment | 0 | NO_ITEMS | Value deployment addressed |
| D:evaluative:judging | evaluative | judging | Definitive Quality Finding | 1 | HAS_ITEMS | No post-installation load test specified |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Alignment | 0 | NO_ITEMS | Merit alignment resolved |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Specification | Specification | Resolve whether wash bay steel plate embedments are within DEL-011-02 scope or shared with DEL-027a; Specification Scope includes wash bay but CON-011-02-03 flags potential overlap with SOW-0027a and DEL-018-05 | Resolved compulsory implementation requires clear scope boundaries. The Specification Included section lists wash bay plates as in-scope, but Guidance CON-011-02-03 identifies that SOW-0027a (wash bay structural scope) and SOW-0027b (drainage scope, PKG-018) may overlap. | Specification.md; Guidance.md | Specification Scope Included; Guidance Conflict Table CON-011-02-03 | Specification.md#Scope vs. Guidance.md#CON-011-02-03 (SOW-0027a/SOW-0027b) | PROPOSAL: Confirm with project decomposition owner | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add step or sub-step for plate surface protection during concrete pour: specify whether plate top surfaces need temporary covering/masking to prevent concrete bonding to the wearing surface | Resolved operational delivery should address protection of the plate wearing surface during the pour. Step 9 addresses plate position monitoring during pour but does not address whether concrete splash, slurry, or finishing operations could damage or bond to the plate top surface. | Procedure.md | Procedure Step 9, Step 10 | -- | PROPOSAL: GC construction practice; confirm with structural engineer | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Clarify whether load rating certification (REQ-011-02-03 verification) requires a physical load test or is satisfied by calculation-based certification from the structural engineer; currently ambiguous | Definitive quality finding requires knowing whether the load rating certification is by analysis only or includes physical testing. Specification Verification table says "Structural engineer confirmation via calculation package" which implies analysis only, but the term "load rating certification" in the Documentation table could imply testing. | Specification.md | Specification Verification table REQ-011-02-03; Documentation table | -- | PROPOSAL: Structural engineer to define certification method | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Criterion | 0 | NO_ITEMS | Steering criteria established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Capacity | 0 | NO_ITEMS | Steering capacity justified through Guidance principles |
| X:guiding:completeness | guiding | completeness | Holistic Leadership Authority | 1 | HAS_ITEMS | No escalation path defined |
| X:guiding:consistency | guiding | consistency | Coherent Leadership Measure | 0 | NO_ITEMS | Leadership measures coherent |
| X:applying:necessity | applying | necessity | Validated Implementation Basis | 1 | HAS_ITEMS | Pre-pour checklist not formalized |
| X:applying:sufficiency | applying | sufficiency | Justified Competent Deployment | 0 | NO_ITEMS | Competent deployment justified through qualifications |
| X:applying:completeness | applying | completeness | Comprehensive Deployment Record | 1 | HAS_ITEMS | Post-pour photo requirement incomplete |
| X:applying:consistency | applying | consistency | Standardized Delivery Indicator | 0 | NO_ITEMS | Delivery indicators standardized |
| X:judging:necessity | judging | necessity | Fundamental Conformance Criterion | 1 | HAS_ITEMS | Acceptance/rejection criteria for pre-pour inspection |
| X:judging:sufficiency | judging | sufficiency | Informed Conformance Judgment | 0 | NO_ITEMS | Conformance judgment framework present |
| X:judging:completeness | judging | completeness | Exhaustive Conformance Authority | 0 | NO_ITEMS | Conformance authority established |
| X:judging:consistency | judging | consistency | Standardized Conformance Measure | 0 | NO_ITEMS | Conformance measures standardized |
| X:reviewing:necessity | reviewing | necessity | Essential Oversight Rationale | 0 | NO_ITEMS | Oversight rationale present |
| X:reviewing:sufficiency | reviewing | sufficiency | Informed Oversight Appraisal | 1 | HAS_ITEMS | County representative role at pre-pour not defined |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Archive | 0 | NO_ITEMS | Audit archive provisions adequate |
| X:reviewing:consistency | reviewing | consistency | Consistent Oversight Indicator | 0 | NO_ITEMS | Oversight indicators consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add escalation path for the scenario where DEL-002-08 IFC drawings are not issued in time for the scheduled slab pour: who has authority to delay the pour, what is the notification chain, and what are the contractual implications | Holistic leadership authority requires defined escalation for the most critical risk identified in Guidance (Considerations: Drawing Availability). The Guidance notes the risk but does not define who decides to delay, how much notice is needed, or how delay costs are allocated. | Guidance.md | Guidance Considerations Drawing Availability | -- | PROPOSAL: GC project management + Owner | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Formalize the pre-pour inspection as a checklist with explicit pass/fail criteria (plate position tolerance, elevation tolerance, anchorage count, weld visual acceptance); Step 8 describes what to inspect but not the quantitative pass/fail thresholds | Validated implementation basis requires that the hold point inspection (Step 8) have defined acceptance criteria. Currently the step says "inspect plate positions vs. IFC" but does not state the positional tolerance or what constitutes a failed inspection. | Procedure.md | Procedure Step 8 | -- | PROPOSAL: Define in coordination with structural engineer | TBD |
| X-003 | X:applying:completeness | Normalization | Specification | Specification | Align Documentation table artifact naming with Procedure Records table: Specification says "Photographs -- pre-pour" while Procedure says "Photographs (pre-pour + post-pour)"; Specification should include post-pour photos explicitly | Comprehensive deployment record requires that the documentation requirements in Specification and Procedure use consistent naming and scope for the photographic record. The Specification Documentation table lists only "Photographs -- pre-pour" in passing, while Procedure Records explicitly includes both pre-pour and post-pour. | Specification.md; Procedure.md | Specification Documentation table; Procedure Records table | -- | PROPOSAL: Align Specification with Procedure | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for the pre-pour hold point in the Specification Verification table: currently REQ-011-02-06 verification says "Inspection prior to concrete pour (hold point)" but does not state what constitutes pass/fail for the anchorage inspection | Fundamental conformance criterion for the pre-pour hold point (the single most critical quality gate) lacks formal acceptance/rejection criteria in the Specification. The Verification table defers to "welding inspection per CSA W59 (ASSUMPTION)" without confirming the standard or stating quantitative criteria. | Specification.md | Specification Verification table REQ-011-02-06 | -- | PROPOSAL: Define once DEL-002-12 confirms welding standard | TBD |
| X-005 | X:reviewing:sufficiency | RationaleGap | Guidance | Guidance | Clarify the County project representative's authority at the pre-pour hold point: is the County representative's role advisory or does their sign-off constitute a formal approval gate that can block the pour | Informed oversight appraisal requires clarity on whether the County representative has veto authority at the pre-pour hold point. Procedure Step 8 requires "written sign-off from structural engineer and County representative" but does not distinguish between an approval gate and a witness/notification role. | Procedure.md; Guidance.md | Procedure Step 8; RFP R-01 section 3.3.2 | -- | PROPOSAL: Confirm with Owner/contract terms | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Orientation Record | 0 | NO_ITEMS | Orientation records verified through references |
| E:guiding:information | guiding | information | Contextual Governance Signal | 0 | NO_ITEMS | Governance signals contextualized |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Orientation Mastery | 0 | NO_ITEMS | Orientation mastery adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Insight | 0 | NO_ITEMS | Leadership insight present in Guidance |
| E:applying:data | applying | data | Proven Implementation Evidence | 1 | HAS_ITEMS | No as-built tolerance for plate position |
| E:applying:information | applying | information | Contextual Execution Account | 0 | NO_ITEMS | Execution account contextual and complete |
| E:applying:knowledge | applying | knowledge | Certified Deployment Mastery | 1 | HAS_ITEMS | Installer qualification not specified |
| E:applying:wisdom | applying | wisdom | Principled Execution Insight | 0 | NO_ITEMS | Execution insight present |
| E:judging:data | judging | data | Verified Compliance Inventory | 0 | NO_ITEMS | Compliance inventory verified |
| E:judging:information | judging | information | Contextual Compliance Account | 0 | NO_ITEMS | Compliance account contextual |
| E:judging:knowledge | judging | knowledge | Comprehensive Compliance Mastery | 0 | NO_ITEMS | Compliance mastery adequate |
| E:judging:wisdom | judging | wisdom | Principled Compliance Wisdom | 0 | NO_ITEMS | Compliance wisdom present |
| E:reviewing:data | reviewing | data | Verified Audit Inventory | 1 | HAS_ITEMS | Warranty inspection protocol not defined |
| E:reviewing:information | reviewing | information | Contextual Audit Account | 0 | NO_ITEMS | Audit account contextual |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Mastery | 0 | NO_ITEMS | Audit mastery adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Wisdom | 0 | NO_ITEMS | Audit wisdom present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Datasheet | Datasheet | Standardize terminology for plate positioning tolerance: Datasheet says "flush (or per structural drawing tolerance)" while Specification says "within the tolerance specified by the structural engineer" and Procedure says "per DEL-002-08 tolerance"; use a single consistent formulation across all three documents | Proven implementation evidence requires that the tolerance reference be stated consistently. Three different phrasings across three documents create ambiguity about whether there is a single tolerance source or multiple potentially different tolerances. | Datasheet.md; Specification.md; Procedure.md | Datasheet Floor System Interface; Specification REQ-011-02-05; Procedure Step 6 | -- | PROPOSAL: Single tolerance reference to DEL-002-08 | TBD |
| E-002 | E:applying:knowledge | MissingSlot | Specification | Specification | Add requirement for steel plate installer/ironworker qualification (e.g., journeyperson ironworker or equivalent) or state that qualification requirements are per DEL-002-12 | Certified deployment mastery requires knowing who is qualified to install the embedments. The Procedure prerequisite P-07 addresses welding subcontractor qualification but no document specifies the qualification required for the personnel who physically position and secure the plates. | Specification.md; Procedure.md | Specification Requirements (entire section scanned); Procedure Prerequisites P-07 | -- | PROPOSAL: GC to confirm; may be covered by DEL-002-12 | TBD |
| E-003 | E:reviewing:data | MissingSlot | Procedure | Specification | Add warranty-period inspection protocol: REQ-011-02-10 states a 2-year guarantee but no document specifies inspection frequency, inspection criteria, or defect reporting procedures during the guarantee period | Verified audit inventory for the warranty period is absent. Specification REQ-011-02-10 and the Verification table say "Guarantee bond; two-year monitoring" but do not define what monitoring entails, who performs it, or at what intervals. | Specification.md; Procedure.md | Specification REQ-011-02-10; Verification table row REQ-011-02-10; Procedure (entire document scanned) | -- | PROPOSAL: Owner and GC to define in warranty administration procedures | TBD |

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | PASS -- All 76 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in evidence from production documents or explicit absence therein |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- 3 conflicts (B-004, D-001, A-001) have Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts match actual warranted items (27 total) |
| Schema followed | PASS -- Output follows STRUCTURE schema |
