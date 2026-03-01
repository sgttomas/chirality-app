# Semantic Lensing Register: DEL-002-05 Mezzanine Framing Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-05_Mezzanine-Details/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-05_Mezzanine-Details/_CONTEXT.md (identity, description, package PKG-002)
- _STATUS.md — DEL-002-05_Mezzanine-Details/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-05_Mezzanine-Details/_SEMANTIC.md (matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-002-05_Mezzanine-Details/Datasheet.md (descriptive attributes, conditions, references)
- Specification.md — DEL-002-05_Mezzanine-Details/Specification.md (normative requirements REQ-DS-001 through REQ-DS-014)
- Guidance.md — DEL-002-05_Mezzanine-Details/Guidance.md (directional principles, considerations, trade-offs, conflict table)
- Procedure.md — DEL-002-05_Mezzanine-Details/Procedure.md (operational steps 1-7, prerequisites, verification)
- _REFERENCES.md — DEL-002-05_Mezzanine-Details/_REFERENCES.md (R-01, R-04 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 26
- By document:
  - Datasheet: 2
  - Specification: 10
  - Guidance: 4
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 4  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction on corrosion protection standard |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Seismic design treatment ambiguous |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC edition not confirmed for compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit path adequately covered in Specification and Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing procedural direction for corrosion protection scope |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps adequately sequenced in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment checkpoints present in Procedure verification table |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit adequately covered by internal review step and field review reports |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit value rationale for deck system selection criteria |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application addressed through trade-off table in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination implicitly covered by Owner confirmation process |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal addressed by internal review and P.Eng. stamp process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Add requirement for corrosion protection standard (e.g., CSA G189 or equivalent) for steel members in wash bay exposure zone | Specification REQ-DS-008 references CSA S16 for steel design but no normative requirement addresses corrosion protection despite Guidance identifying wash bay as a corrosive environment. This gap could lead to inconsistent corrosion protection approaches. | Specification.md; Guidance.md | Specification.md#2.2 Design Requirements; Guidance.md#3.3 Wash bay environment | — | PROPOSAL: Structural Engineer of Record | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify seismic design applicability: state whether seismic analysis is required or explicitly excluded for the mezzanine, with reference to ABC seismic provisions | REQ-DS-005 requires ABC compliance broadly but no specific requirement addresses seismic design. Datasheet lists seismic zone as TBD. For a secondary structure within a concrete building, seismic applicability is a mandatory practice question that should be resolved normatively. | Specification.md; Datasheet.md | Specification.md#2.2 Design Requirements; Datasheet.md#3 Conditions (seismic zone) | — | PROPOSAL: Structural Engineer of Record | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: confirm applicable ABC edition with Camrose County permit authority before compliance determination can be finalized | Multiple documents reference ABC compliance but the specific code edition is TBD. Compliance determination cannot be finalized until the governing code edition is confirmed. Guidance and Procedure both flag this but Specification does not include a conditional statement. | Specification.md; Guidance.md; Procedure.md | Specification.md#3 Standards; Guidance.md#3.5; Procedure.md#Step 1 action 3 | — | PROPOSAL: Camrose County permit authority | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add procedural step or sub-step addressing corrosion protection specification for steel members in wash bay zone (e.g., galvanizing specification, paint system selection) | Guidance identifies wash bay corrosion as a key consideration (Guidance.md 3.3) but Procedure has no corresponding step to address corrosion protection specification or coordination. | Procedure.md; Guidance.md | Procedure.md#3 Steps (no wash bay corrosion step); Guidance.md#3.3 | — | PROPOSAL: Structural Engineer of Record | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add value-based selection criteria for deck system choice (load capacity, maintenance, cost, drainage) linking to Owner priorities | Guidance 3.1 and Trade-offs table list deck system options but do not provide explicit evaluation criteria or Owner priority weighting. The deck system choice significantly affects cost, maintenance, and load distribution. | Guidance.md | Guidance.md#3.1; Guidance.md#4 Trade-offs | — | PROPOSAL: Structural Engineer of Record with Owner input | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Mezzanine plan dimensions not yet established as essential facts |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence from R-01 and R-04 adequately referenced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Dead load values missing from Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement data consistently sourced from R-01 and R-04 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (RFP requirements, floor plan) adequately captured |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for design adequately framed in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-document narrative adequately comprehensive for current state |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Mezzanine extent messaging inconsistent between RFP text and Appendix B |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental structural understanding adequately represented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Design expertise requirements addressed through P.Eng. stamp requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No gap — thoroughness deferred appropriately to Structural Engineer of Record |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistently communicated across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment items (conflicts, trade-offs) identified in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately deferred to Structural Engineer of Record and Owner |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance considerations and trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistently grounded in source documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: obtain from Owner the maximum number of oil totes, equipment list with weights, and desired arrangement to establish essential design load data | Datasheet lists oil tote weight as approximate (1,000 kg per IBC tote, marked ASSUMPTION) and live load as TBD. These are essential facts for structural design that must be sourced from the Owner before design can proceed. | Datasheet.md | Datasheet.md#2.4 Live Load (Design Basis) | — | PROPOSAL: Owner / Camrose County | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add dead load estimates (self-weight range for candidate framing and deck systems) to Datasheet for comprehensive load record | Datasheet records live load as TBD and notes dead load as "TBD — self-weight of deck, framing, and any permanent fixtures" but provides no preliminary range even for the candidate systems discussed in Guidance. A comprehensive record should include at least order-of-magnitude dead load values for each candidate system. | Datasheet.md | Datasheet.md#2.4 Live Load (Design Basis) | — | PROPOSAL: Structural Engineer of Record | TBD |
| B-003 | B:information:consistency | Conflict | Multi | Guidance | Clarify mezzanine lateral extent: reconcile RFP text (parts room + utility room only) with Appendix B drawing notes (parts room + utility room + wash bay) | This is the same conflict as CF-DS-002 in Guidance. Under the coherent message lens, the inconsistency between R-01 text and R-04 drawing notes risks different interpretations of mezzanine extent. Already flagged in Guidance Conflict Table but not yet ruled upon. | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#2.1; Specification.md#REQ-DS-001; Guidance.md#6 CF-DS-002 | Guidance.md#6 CF-DS-002: R-01 §3.4 vs. R-04 App B | PROPOSAL: Follow Appendix B (more detailed); confirm with Owner | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Threshold | 1 | HAS_ITEMS | Fire protection threshold not addressed |
| C:normative:sufficiency | normative | sufficiency | Defensible Certification Basis | 1 | HAS_ITEMS | CSA code edition not confirmed for defensible certification |
| C:normative:completeness | normative | completeness | Comprehensive Mandate Coverage | 0 | NO_ITEMS | Mandate coverage adequate — requirements REQ-DS-001 through REQ-DS-014 span structural, code, and deliverable content |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Adherence | 0 | NO_ITEMS | Regulatory adherence consistently referenced across documents |
| C:operative:necessity | operative | necessity | Critical Functional Prerequisite | 1 | HAS_ITEMS | Owner load confirmation is critical prerequisite not yet resolved |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Performance | 0 | NO_ITEMS | Procedure provides sufficient detail for competent execution |
| C:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 0 | NO_ITEMS | Operational steps 1-7 cover design through construction support |
| C:operative:consistency | operative | consistency | Repeatable Process Discipline | 0 | NO_ITEMS | Process discipline maintained through structured steps and verification table |
| C:evaluative:necessity | evaluative | necessity | Inherent Worth Recognition | 1 | HAS_ITEMS | Worth of mezzanine over wash bay not confirmed relative to cost/complexity |
| C:evaluative:sufficiency | evaluative | sufficiency | Credible Value Appraisal | 0 | NO_ITEMS | Value appraisal deferred to trade-off analysis in Guidance — adequate |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting adequately represented through trade-off options |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation coherent across Guidance trade-offs and Procedure steps |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement addressing fire protection for steel mezzanine framing per ABC occupancy classification, or explicitly state that fire protection is not required and cite the applicable ABC exemption | Guidance mentions fire protection as a consideration for steel framing (Guidance 3.1, Option A disadvantages) but no normative requirement in Specification addresses it. For an obligatory compliance threshold, fire protection applicability must be resolved. | Specification.md; Guidance.md | Specification.md#2.2 Design Requirements (absent); Guidance.md#3.1 (mention only) | — | PROPOSAL: Structural Engineer of Record / Building Code review | TBD |
| C-002 | C:normative:sufficiency | TBD_Question | Specification | Specification | Record TBD: confirm specific edition numbers for CSA S16, CSA A23.3, and CSA W59 applicable to this permit to establish defensible certification basis | Specification Standards table lists these codes as ASSUMPTION with "location TBD" and "confirm code edition with permit authority." A defensible certification basis requires confirmed code editions before final design. | Specification.md | Specification.md#3 Standards | — | PROPOSAL: Camrose County permit authority | TBD |
| C-003 | C:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit hold point or gate in Procedure Step 2 requiring documented Owner confirmation of design live load before proceeding to Step 3 (structural analysis) | Procedure Step 1 requests Owner confirmation of live load and Step 2 uses it, but there is no explicit hold point or verification that the Owner confirmation has been received before analysis proceeds. This is a critical functional prerequisite that should have a formal gate. | Procedure.md | Procedure.md#Step 1; Procedure.md#Step 2 | — | PROPOSAL: Project Manager / Structural Engineer of Record | TBD |
| C-004 | C:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale section addressing whether mezzanine over wash bay adds sufficient value relative to structural/corrosion complexity, linking to CF-DS-002 resolution | CF-DS-002 flags the mezzanine extent conflict but Guidance does not analyze whether the incremental storage over the wash bay justifies the additional structural and corrosion-protection cost. Inherent worth recognition requires this evaluation. | Guidance.md | Guidance.md#3.2; Guidance.md#6 CF-DS-002 | — | PROPOSAL: Owner with Structural Engineer input | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Compliance Imperative | 1 | HAS_ITEMS | Deflection limit not stated as enforceable requirement |
| F:normative:sufficiency | normative | sufficiency | Warranted Conformance Proof | 1 | HAS_ITEMS | Verification approach for REQ-DS-012 (penetrations) weak |
| F:normative:completeness | normative | completeness | Total Regulatory Mandate Scope | 0 | NO_ITEMS | Regulatory scope adequately covered by 14 requirements plus standards table |
| F:normative:consistency | normative | consistency | Standardized Conformance Measure | 0 | NO_ITEMS | Conformance measures consistently linked to calculation review, drawing review, and inspection |
| F:operative:necessity | operative | necessity | Core Operational Demand | 0 | NO_ITEMS | Core operational demands identified in Procedure prerequisites |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Readiness | 1 | HAS_ITEMS | Upstream dependency readiness not formally verified |
| F:operative:completeness | operative | completeness | Total Process Mastery | 0 | NO_ITEMS | Process coverage adequate across 7 steps |
| F:operative:consistency | operative | consistency | Systematic Execution Rigor | 0 | NO_ITEMS | Execution rigor maintained through structured steps and verification |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Judgment | 0 | NO_ITEMS | Merit judgment adequately represented through trade-off analysis |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Assessment | 0 | NO_ITEMS | Worth assessment deferred to Owner and Structural Engineer — appropriate |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Merit Inventory | 1 | HAS_ITEMS | Cost/schedule impact of candidate systems not inventoried |
| F:evaluative:consistency | evaluative | consistency | Integrated Valuation Consistency | 0 | NO_ITEMS | Valuation consistently aligned across Guidance trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add explicit deflection limit requirement for mezzanine framing (e.g., L/360 for live load, L/240 for total load, or per ABC/CSA S16) with verification approach | Procedure Step 3 action 7 mentions "check deflection limits per ABC / CSA S16" but Specification has no corresponding requirement stating the enforceable deflection limit. An enforceable compliance imperative requires a normative statement, not just a procedural check. | Specification.md; Procedure.md | Specification.md#2.2 Design Requirements (absent); Procedure.md#Step 3 action 7 | — | PROPOSAL: Structural Engineer of Record per CSA S16 / ABC | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen verification approach for REQ-DS-012 (service penetrations): specify who signs off on coordination and what evidence constitutes warranted conformance (e.g., signed coordination drawing, RFI closure log) | Specification Verification table for REQ-DS-012 states "Inter-discipline coordination review prior to IFC issue" which is vague. Warranted conformance proof requires specific evidence: who reviews, what artifact is produced, and when sign-off occurs. | Specification.md | Specification.md#4 Verification (REQ-DS-012 row) | — | PROPOSAL: Project Manager / Lead Discipline Engineers | TBD |
| F-003 | F:operative:sufficiency | MissingSlot | Procedure | Procedure | Add prerequisite readiness check in Procedure Step 2 confirming that DEL-002-03 (Structural Framing Plans) building grid is available before establishing mezzanine column locations | Procedure lists DEL-002-03 as a required reference and an upstream dependency but has no explicit readiness gate verifying that the building grid from DEL-002-03 is available before mezzanine column locations are established in Step 2. Proven operational readiness requires this verification. | Procedure.md | Procedure.md#2.3 Upstream Dependencies; Procedure.md#Step 2 action 2 | — | PROPOSAL: Structural Engineer of Record | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Guidance | Guidance | Add comparative merit summary for candidate framing/deck systems covering approximate cost, schedule, and maintenance implications to support comprehensive merit inventory | Guidance Trade-offs table lists qualitative pros/cons but provides no order-of-magnitude cost or schedule comparison. A comprehensive merit inventory should include at least relative cost/schedule signals to inform the Owner's decision. | Guidance.md | Guidance.md#4 Trade-offs | — | PROPOSAL: Structural Engineer of Record with Contractor input | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Governing Authority | 0 | NO_ITEMS | Governing authority adequately established through ABC, CSA standards, and P.Eng. requirement |
| D:normative:applying | normative | applying | Binding Implementation Closure | 1 | HAS_ITEMS | No requirement for as-built verification against IFC drawings |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling path clear through P.Eng. certification and permit authority review |
| D:normative:reviewing | normative | reviewing | Settled Regulatory Benchmark | 0 | NO_ITEMS | Regulatory benchmark adequately defined pending ABC edition confirmation |
| D:operative:guiding | operative | guiding | Authoritative Process Guidance | 0 | NO_ITEMS | Process guidance authoritative through Guidance principles and Procedure steps |
| D:operative:applying | operative | applying | Verified Field Delivery | 1 | HAS_ITEMS | Welding inspection scope not explicitly linked to mezzanine-specific connections |
| D:operative:judging | operative | judging | Definitive Execution Evaluation | 0 | NO_ITEMS | Execution evaluation covered by internal review and field review reports |
| D:operative:reviewing | operative | reviewing | Settled Procedural Review | 0 | NO_ITEMS | Procedural review adequately settled through verification table |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Direction | 0 | NO_ITEMS | Worth direction adequately framed in Guidance |
| D:evaluative:applying | evaluative | applying | Enacted Quality Realization | 1 | HAS_ITEMS | Quality realization criteria for deck system not enacted |
| D:evaluative:judging | evaluative | judging | Definitive Quality Ruling | 0 | NO_ITEMS | Quality ruling path clear through P.Eng. stamp and inspection |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Standard | 0 | NO_ITEMS | Quality standard adequately settled through standards table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add requirement or verification approach for as-built survey of mezzanine framing confirming conformance with IFC drawings (linking to SOW-0004) | Specification Documentation section references as-built survey (SOW-0004) but no verification row confirms that the as-built condition matches the IFC design. Binding implementation closure requires a normative link between the as-built record and the IFC drawings. | Specification.md | Specification.md#5.2 Supporting Documentation (SOW-0004 reference); Specification.md#4 Verification (absent) | — | PROPOSAL: Structural Engineer of Record | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add explicit step or sub-step in Step 7 (Construction Support) specifying welding inspection scope for mezzanine connections (types of welds, inspection frequency, CSA W59 compliance verification) | Specification Standards table lists CSA W59 and Procedure Step 7 mentions shop drawing review but does not specify welding inspection scope for mezzanine-specific connections. Verified field delivery requires explicit inspection scope for critical connections. | Procedure.md; Specification.md | Procedure.md#Step 7; Specification.md#3 Standards (CSA W59); Specification.md#4 Field Verification | — | PROPOSAL: Structural Engineer of Record | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add selection criteria or decision framework for deck system that links Owner operational requirements (forklift traffic, drainage, maintenance) to specific deck type recommendation | Guidance Trade-offs mention deck system options but do not link selection to Owner operational requirements. Enacted quality realization requires a clear path from operational needs to deck system decision. | Guidance.md | Guidance.md#3.1; Guidance.md#4 Trade-offs (deck system row) | — | PROPOSAL: Structural Engineer of Record with Owner input | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directional Authority | 0 | NO_ITEMS | Directional authority adequately established in Guidance |
| X:guiding:sufficiency | guiding | sufficiency | Justified Governance Basis | 0 | NO_ITEMS | Governance basis justified through RFP and code references |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Inventory | 0 | NO_ITEMS | Governance inventory complete within available source documents |
| X:guiding:consistency | guiding | consistency | Consistent Directional Standard | 0 | NO_ITEMS | Directional standards consistently applied |
| X:applying:necessity | applying | necessity | Mandatory Execution Baseline | 1 | HAS_ITEMS | No mandatory baseline for embed installation timing |
| X:applying:sufficiency | applying | sufficiency | Warranted Delivery Evidence | 0 | NO_ITEMS | Delivery evidence requirements clear through IFC stamp and inspection reports |
| X:applying:completeness | applying | completeness | Comprehensive Delivery Record | 1 | HAS_ITEMS | Shop drawing review not listed as a required record in Specification |
| X:applying:consistency | applying | consistency | Dependable Practice Standard | 0 | NO_ITEMS | Practice standards consistent across documents |
| X:judging:necessity | judging | necessity | Mandatory Compliance Finding | 0 | NO_ITEMS | Compliance findings path clear through permit review and inspection |
| X:judging:sufficiency | judging | sufficiency | Qualified Judgment Basis | 1 | HAS_ITEMS | Guardrail design load value not stated for judgment basis |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Ledger | 0 | NO_ITEMS | Assessment ledger adequately populated by verification tables |
| X:judging:consistency | judging | consistency | Reliable Assessment Measure | 0 | NO_ITEMS | Assessment measures consistently defined |
| X:reviewing:necessity | reviewing | necessity | Mandatory Audit Baseline | 0 | NO_ITEMS | Audit baseline established through County inspector attendance requirement |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Audit Competence | 0 | NO_ITEMS | Audit competence justified through P.Eng. certification |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Record | 1 | HAS_ITEMS | Terminology for inspection records inconsistent |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Standard | 0 | NO_ITEMS | Audit standards consistently referenced |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Procedure | Specification | Add requirement specifying that embed/anchor bolt locations must be verified and approved by Structural Engineer of Record before concrete pour (mandatory execution baseline for cast-in-place embeds) | Guidance recommends cast-in-place embeds (Guidance 2.2) and Procedure Step 7 mentions embed inspection before concrete pour, but no normative requirement in Specification mandates this approval sequence. The mandatory execution baseline should be normatively stated. | Procedure.md; Guidance.md; Specification.md | Procedure.md#Step 7 action 2-3; Guidance.md#2.2; Specification.md#4 Field Verification | — | PROPOSAL: Structural Engineer of Record | TBD |
| X-002 | X:applying:completeness | MissingSlot | Specification | Specification | Add shop drawing review as a required deliverable/record in Specification Documentation section to ensure comprehensive delivery record | Procedure Step 7 requires shop drawing review and Specification mentions IFC drawings, but the Specification Documentation section does not list shop drawing review records as a required supporting document. Comprehensive delivery record should include this artifact. | Specification.md; Procedure.md | Specification.md#5.2 Supporting Documentation; Procedure.md#Step 7 action 1 | — | PROPOSAL: Structural Engineer of Record | TBD |
| X-003 | X:judging:sufficiency | WeakStatement | Specification | Specification | Specify the horizontal design load for guardrail posts (e.g., 0.75 kN/m or per ABC applicable clause) to provide a qualified judgment basis for guardrail adequacy | REQ-DS-010 states guardrails "shall meet ABC requirements for height (minimum 1,070 mm)" and "be designed to resist applicable horizontal loads per ABC" but does not state the specific load value. A qualified judgment basis requires the actual design load to be documented. | Specification.md | Specification.md#REQ-DS-010 | — | PROPOSAL: Structural Engineer of Record per ABC | TBD |
| X-004 | X:reviewing:completeness | Normalization | Multi | Guidance | Normalize terminology for construction inspection records: documents variously use "field review reports," "inspection reports," and "site review" — establish a consistent vocabulary | Specification uses "inspection reports" and "site inspection," Procedure uses "field review reports" and "site review," and Datasheet does not reference them. Inconsistent terminology risks confusion about whether these are the same or different record types. | Specification.md; Procedure.md | Specification.md#4 Field Verification; Procedure.md#Step 7; Procedure.md#5 Records | — | PROPOSAL: Guidance vocabulary note | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Documented Guidance Benchmark | 0 | NO_ITEMS | Guidance benchmarks adequately documented from R-01 and R-04 |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering intelligence coherent across Guidance considerations |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Mastery | 0 | NO_ITEMS | Governance mastery appropriately deferred to Structural Engineer of Record |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Vision | 0 | NO_ITEMS | Strategic vision adequately expressed in Guidance purpose and principles |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Drawing numbering convention not established |
| E:applying:information | applying | information | Situated Performance Intelligence | 0 | NO_ITEMS | Performance intelligence adequately situated through Procedure steps |
| E:applying:knowledge | applying | knowledge | Integrated Delivery Proficiency | 0 | NO_ITEMS | Delivery proficiency addressed through P.Eng. requirement and internal review |
| E:applying:wisdom | applying | wisdom | Prudent Implementation Judgment | 0 | NO_ITEMS | Implementation judgment prudently framed through trade-offs and conflict table |
| E:judging:data | judging | data | Documented Adjudication Evidence | 1 | HAS_ITEMS | Snow load applicability not documented |
| E:judging:information | judging | information | Contextual Assessment Intelligence | 0 | NO_ITEMS | Assessment intelligence adequately contextualized |
| E:judging:knowledge | judging | knowledge | Integrated Assessment Mastery | 0 | NO_ITEMS | Assessment mastery appropriately deferred to Structural Engineer of Record |
| E:judging:wisdom | judging | wisdom | Principled Evaluation Wisdom | 0 | NO_ITEMS | Evaluation wisdom adequately represented in conflict table and trade-offs |
| E:reviewing:data | reviewing | data | Documented Inspection Evidence | 1 | HAS_ITEMS | Terminology for SOW references inconsistent |
| E:reviewing:information | reviewing | information | Situated Audit Intelligence | 0 | NO_ITEMS | Audit intelligence adequately situated |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Inspection Mastery | 0 | NO_ITEMS | Inspection mastery appropriately deferred to P.Eng. |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Discernment | 0 | NO_ITEMS | Audit discernment adequately framed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | WeakStatement | Procedure | Datasheet | Add drawing numbering convention or cross-reference to project drawing register in Datasheet or Procedure to support verified execution records | Procedure Step 4 action 3 states "Assign drawing numbers per project drawing register" but neither Datasheet nor Procedure identifies the drawing numbering convention or references where the project drawing register is maintained. This weakens the verified execution record traceability. | Procedure.md; Datasheet.md | Procedure.md#Step 4 action 3; Datasheet.md#4.1 (anticipated sheets only) | — | PROPOSAL: Project Manager | TBD |
| E-002 | E:judging:data | TBD_Question | Specification | Specification | Record TBD: confirm whether snow load transfer to mezzanine framing applies (mezzanine is internal to building but verify if any portion is exposed or if roof load path affects mezzanine columns) | Procedure Step 3 action 1 mentions "snow load transfer (if applicable)" but neither Specification nor Datasheet documents whether snow load affects the mezzanine structure. Since the mezzanine is internal to a 35' building, it likely does not receive snow load directly, but column load paths from roof may affect mezzanine column design. This should be documented as adjudication evidence. | Procedure.md; Specification.md | Procedure.md#Step 3 action 1; Specification.md#2.2 (absent) | — | PROPOSAL: Structural Engineer of Record | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Datasheet | Normalize SOW references across documents: Datasheet references SOW-0012, SOW-0032, SOW-0033, SOW-0034; Procedure references SOW-0084, SOW-0085, SOW-0004, SOW-0006 — consolidate all applicable SOW references in Datasheet for single-source traceability | Different production documents reference different SOW items without a consolidated list. The Datasheet Identification section lists four SOW items while Procedure references four additional ones. For documented inspection evidence, all applicable SOW references should be consolidated in the descriptive document. | Datasheet.md; Procedure.md | Datasheet.md#1 Identification (Covers SOW); Procedure.md#Step 6-7 (SOW-0004, SOW-0006, SOW-0084, SOW-0085) | — | PROPOSAL: Datasheet as single SOW reference source | TBD |
