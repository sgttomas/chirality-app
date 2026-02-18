# Semantic Lensing Register: DEL-05-02 Option -- Yard Lighting (Per Light)

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-02_Option - Yard Lighting (Per Light)/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-02 context (yard lighting concept; pole/fixture basis; unit rate sheet; SOW-0501; OBJ-010)
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- 7 matrices parsed (A, B, C, F, D, X, E); all cells populated
- Datasheet.md -- Identification, Attributes, Conditions, Construction, Anticipated Artifacts, References
- Specification.md -- Scope, Requirements REQ-01 through REQ-09, Standards, Verification, Documentation
- Guidance.md -- Purpose, Principles, Considerations, Trade-offs, Conflict Table
- Procedure.md -- Purpose, Prerequisites, Steps (Phase A/B), Verification, Records
- _REFERENCES.md -- OSR Appendix A section 12.2; optional priced item notes

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 4
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 4  B: 4  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | AEC/IES applicability is assumed, not prescribed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Control strategy TBD weakens mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach for REQ-08 lacks specificity |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure B5 handover covers audit records adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps A1-A6 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Minimum quantity assumption unresolved |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure records table adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles 1-5 establish clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs in Guidance address merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Owner election mechanism provides worth determination path |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning and IES compliance checks cover quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether OSR 10.5 LED/IES standards are prescriptive for yard lighting or only assumed applicable; record as confirmed or TBD | REQ-03 and REQ-04 both carry ASSUMPTION tags about applicability of OSR 10.5 to yard lighting, weakening prescriptive direction for a normative requirement | Specification.md | REQ-03, REQ-04 | -- | Specification.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: control strategy (photocell, timer, manual, or combination) -- source decision from electrical discipline or Owner | Control strategy is listed as TBD in Datasheet Attributes and never resolved in any document; this affects mandatory practice for switching/commissioning | Datasheet.md | Attributes table (Control strategy row) | -- | Electrical discipline lead | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific verification method for REQ-08 code compliance beyond "confirm AEC reference present" -- e.g., confirm AEC edition cited, confirm AHJ jurisdiction identified | Verification for REQ-08 states only "Confirm design narrative or specification references AEC compliance" which is a document-presence check, not a compliance determination | Specification.md | Verification table, REQ-08 row | -- | Specification.md | TBD |
| A-004 | A:operative:applying | WeakStatement | Guidance | Guidance | Clarify minimum quantity assumption for unit rate validity (referenced in Trade-off 3 but left as TBD -- "confirm approach with pricing team") | Guidance Trade-off 3 identifies the fixed-cost allocation problem but defers resolution; practical execution of unit rate preparation cannot proceed without this input | Guidance.md | Trade-offs, Trade-off 3 | -- | Pricing team | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Pole spec and electrical routing are TBD essential facts |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Existing OSR citations provide adequate evidence basis |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Yard dimensions not recorded |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | "~100 m" approximation used inconsistently |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (optional status, per-light basis) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for Owner decision-making is adequately framed |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive account of scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 1 | HAS_ITEMS | IES publication identity unknown |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Electrical discipline expertise assumed adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for proposal stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs in Guidance demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are flagged appropriately |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Adequate for proposal scope |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add pole specification data (type, height range, material) once determined; currently TBD in Attributes table | Pole specification is an essential fact for unit rate preparation and is listed as TBD with no resolution path identified | Datasheet.md | Attributes table (Pole specification row) | -- | Electrical discipline lead | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Record actual yard dimensions (length x width) or note as TBD pending site plan from DEL-03-01 | Yard area dimensions are stated as "TBD" in Conditions table; fixture count estimation requires yard geometry | Datasheet.md | Conditions table (Site geometry row) | -- | Civil/site plan (DEL-03-01) | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Datasheet | Standardize fence-line distance expression: confirm whether "approximately 100 m" or "~100 m" is the canonical value and whether it is measured to fence line or property boundary | Fence-line distance is stated as "Approximately 100 m" in Datasheet, "approximately 100 m" in Specification REQ-02, and "~100 m" in Procedure A1; minor inconsistency but could drift | Datasheet.md, Specification.md, Procedure.md | Datasheet Attributes; Specification REQ-02; Procedure Step A1 | -- | Datasheet.md (factual authority) | TBD |
| B-004 | B:knowledge:necessity | TBD_Question | Specification | Specification | Record TBD: identify specific IES publication applicable to outdoor municipal yard lighting (e.g., IES RP-8 or other) | Specification REQ-04 references "IES recommendations" generically; Guidance mentions IES RP-8 as a candidate but does not confirm; the applicable publication is unknown | Specification.md, Guidance.md | Specification REQ-04; Guidance IES Outdoor Lighting Standards | -- | Electrical discipline / IES reference library | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Mandatory Compliance Threshold | 1 | HAS_ITEMS | AEC edition not specified |
| C:normative:sufficiency | normative | sufficiency | Justified Regulatory Basis | 0 | NO_ITEMS | OSR citations justify regulatory basis adequately |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Municipal regulations not enumerated |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Standards references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites in Procedure are adequately stated |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Competence | 0 | NO_ITEMS | Competence requirements are implicit in discipline assignments |
| C:operative:completeness | operative | completeness | Comprehensive Process Coverage | 1 | HAS_ITEMS | Phase B permitting step gap |
| C:operative:consistency | operative | consistency | Stable Operational Repeatability | 0 | NO_ITEMS | Process is repeatable as described |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | Worth criteria (Owner decision support, pricing transparency) are clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Judgment | 0 | NO_ITEMS | Merit judgment framework in Guidance is adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Assessment | 0 | NO_ITEMS | Value assessment covers key considerations |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value principles are coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Specify AEC edition/year applicable to this project (e.g., "Alberta Electrical Code, 2024 edition" or as adopted by AHJ) | REQ-08 references "Alberta Electrical Code (AEC)" without edition; mandatory compliance threshold requires a specific, identifiable standard | Specification.md | REQ-08; Standards table | -- | AHJ / project legal requirements | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add reference to applicable municipal bylaws or confirm none apply beyond provincial codes | Standards table lists AEC, ABC, CSA C22.1, and IES but does not address Town of Penhold municipal bylaws or land-use regulations that may apply to exterior pole installations | Specification.md | Standards table | -- | AHJ / municipal planning authority | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step in Phase B for AHJ permit application and inspection coordination for exterior electrical and pole foundation work | Procedure Phase B covers design, procurement, installation, commissioning, and handover but does not include a permitting/inspection coordination step; exterior pole installations typically require AHJ approval | Procedure.md | Phase B steps (between B1 and B2) | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Prescriptive Conformance Baseline | 1 | HAS_ITEMS | IP rating not specified |
| F:normative:sufficiency | normative | sufficiency | Adequate Compliance Substantiation | 0 | NO_ITEMS | Substantiation adequate for proposal stage |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Assurance | 0 | NO_ITEMS | Regulatory assurance coverage adequate given assumptions |
| F:normative:consistency | normative | consistency | Integrated Prescriptive Alignment | 0 | NO_ITEMS | Prescriptive alignment is consistent |
| F:operative:necessity | operative | necessity | Foundational Operational Mandate | 1 | HAS_ITEMS | Electrical service routing prerequisite gap |
| F:operative:sufficiency | operative | sufficiency | Sufficient Operational Readiness | 0 | NO_ITEMS | Readiness framework adequate |
| F:operative:completeness | operative | completeness | Total Operational Assurance | 0 | NO_ITEMS | Operational assurance adequate for scope |
| F:operative:consistency | operative | consistency | Disciplined Process Consistency | 0 | NO_ITEMS | Process is consistent |
| F:evaluative:necessity | evaluative | necessity | Core Valuation Imperative | 0 | NO_ITEMS | Core valuation (per-light rate, Owner flexibility) well established |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Value Substantiation | 1 | HAS_ITEMS | Lifecycle cost rationale gap |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting adequate for proposal stage |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Integrity | 0 | NO_ITEMS | Valuation principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add minimum IP rating requirement for exterior fixtures (e.g., IP65 or IP66) to REQ-06 or as a new sub-requirement | REQ-06 requires "weatherproof" construction but does not specify a minimum IP rating; verification table says "Confirm fixture IP rating" but there is no acceptance threshold to verify against | Specification.md | REQ-06; Verification table REQ-06 row | -- | Specification.md | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite or step confirming electrical service point capacity and routing feasibility before developing unit rate (relates to Step A4 but is not a prerequisite check) | Procedure Prerequisites list "Electrical discipline input on available service points" but Step A4 treats routing as a design task; no explicit go/no-go check on whether adequate electrical capacity exists at the service point | Procedure.md | Prerequisites; Step A4 | -- | Procedure.md | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add brief lifecycle cost consideration (LED lamp life, maintenance frequency, replacement cost) to support Owner value judgment on electing the option | Guidance covers initial pricing transparency and technology choice but does not address lifecycle cost or total cost of ownership, which supports the Owner's value determination for electing the option | Guidance.md | Considerations section | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Direction | 0 | NO_ITEMS | Compliance direction established via OSR references |
| D:normative:applying | normative | applying | Verified Mandatory Fulfillment | 1 | HAS_ITEMS | Scope boundary verification gap |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance approach defined in Verification table |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Oversight | 0 | NO_ITEMS | Oversight path through proposal review and post-award inspection |
| D:operative:guiding | operative | guiding | Established Process Governance | 0 | NO_ITEMS | Process governance adequate in Procedure |
| D:operative:applying | operative | applying | Confirmed Operational Deployment | 0 | NO_ITEMS | Deployment sequence is clear (Phase A/B) |
| D:operative:judging | operative | judging | Definitive Performance Verdict | 0 | NO_ITEMS | Commissioning test (Step B4) provides performance verdict |
| D:operative:reviewing | operative | reviewing | Assured Process Integrity | 0 | NO_ITEMS | Records table in Procedure supports process integrity |
| D:evaluative:guiding | evaluative | guiding | Established Value Authority | 0 | NO_ITEMS | Value authority established through Owner election model |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Realization | 1 | HAS_ITEMS | No post-installation performance confirmation for Owner |
| D:evaluative:judging | evaluative | judging | Definitive Worth Determination | 0 | NO_ITEMS | Owner election mechanism serves as worth determination |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Standard | 0 | NO_ITEMS | Quality standard assured through IES compliance and commissioning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification check confirming Out of Scope boundaries are respected (e.g., confirm yard lighting does not extend to Fire Department yard or interior spaces) | Specification Out of Scope section defines exclusions but the Verification table does not include a check confirming scope boundaries are observed; verified mandatory fulfillment requires confirming what is excluded as well as included | Specification.md | Out of Scope; Verification table | -- | Specification.md | TBD |
| D-002 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add note on how Owner confirms realized value post-installation (e.g., illuminance measurement, operational feedback period) | Guidance focuses on pre-election decision support but does not address how the Owner would confirm that the elected option delivered the anticipated merit after installation | Guidance.md | entire document scanned | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Governing Mandate Foundation | 0 | NO_ITEMS | Mandate foundation is clear (OSR 12.2, OBJ-010) |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Governance Basis | 0 | NO_ITEMS | Governance basis substantiated through OSR references |
| X:guiding:completeness | guiding | completeness | Total Governance Coverage | 0 | NO_ITEMS | Governance coverage adequate |
| X:guiding:consistency | guiding | consistency | Unified Governance Coherence | 0 | NO_ITEMS | Governance coherent across documents |
| X:applying:necessity | applying | necessity | Confirmed Implementation Necessity | 1 | HAS_ITEMS | Coordination boundary TBD |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Implementation Adequacy | 0 | NO_ITEMS | Implementation approach adequate for proposal stage |
| X:applying:completeness | applying | completeness | Complete Implementation Coverage | 1 | HAS_ITEMS | Photocell/timer control scope gap |
| X:applying:consistency | applying | consistency | Consistent Implementation Discipline | 0 | NO_ITEMS | Implementation approach is consistent |
| X:judging:necessity | judging | necessity | Binding Adjudication Standard | 0 | NO_ITEMS | Adjudication standards (IES, AEC) identified |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment Proof | 0 | NO_ITEMS | Judgment proof path defined through verification table |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers requirements |
| X:judging:consistency | judging | consistency | Principled Adjudication Consistency | 0 | NO_ITEMS | Adjudication consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Oversight Threshold | 1 | HAS_ITEMS | Glare/light trespass not addressed |
| X:reviewing:sufficiency | reviewing | sufficiency | Demonstrated Oversight Sufficiency | 0 | NO_ITEMS | Oversight sufficient for proposal stage |
| X:reviewing:completeness | reviewing | completeness | Complete Oversight Assurance | 0 | NO_ITEMS | Oversight coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Principled Oversight Reliability | 0 | NO_ITEMS | Oversight principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Conflict | Specification | Specification | Resolve coordination boundary between yard lighting electrical service and base scope electrical distribution; Specification Out of Scope says tie-in is "either part of base scope or a separate cash allowance per SOW-0110 -- ASSUMPTION: coordination boundary TBD" while Guidance says infrastructure cost "should be included in the per-light unit rate" | Specification Out of Scope and Guidance Electrical Service Coordination give contradictory signals about whether electrical service infrastructure is in the yard lighting unit rate or in base scope | Specification.md, Guidance.md | Specification Out of Scope; Guidance Electrical Service Coordination | Specification.md#Out-of-Scope, Guidance.md#Electrical-Service-Coordination | Human ruling needed | TBD |
| X-002 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement or sub-requirement for lighting control system (photocell, timer, manual, or combination) as part of the per-light scope | REQ-01 scope of unit rate includes "commissioning of each fixture" but does not address the control system (switching mechanism); Datasheet lists control strategy as TBD; complete implementation requires this to be specified | Specification.md, Datasheet.md | REQ-01; Datasheet Attributes (Control strategy) | -- | Specification.md | TBD |
| X-003 | X:reviewing:necessity | MissingSlot | Specification | Specification | Add consideration for light trespass and glare control in fixture/layout requirements (IES criteria typically address this for outdoor installations) | No document addresses light trespass to neighboring properties or glare control for equipment operators; this is a standard consideration in IES outdoor lighting that could trigger oversight issues if omitted | Specification.md, Guidance.md | entire document scanned | -- | Specification.md / Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Authoritative Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandate adequately established |
| E:normative:sufficiency | normative | sufficiency | Proven Regulatory Sufficiency | 0 | NO_ITEMS | Sufficiency adequate for proposal stage |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Completeness | 0 | NO_ITEMS | Regulatory completeness adequate given identified assumptions |
| E:normative:consistency | normative | consistency | Unified Regulatory Integrity | 0 | NO_ITEMS | Regulatory integrity maintained across documents |
| E:operative:necessity | operative | necessity | Mandatory Operational Baseline | 1 | HAS_ITEMS | Upstream dependency formalization gap |
| E:operative:sufficiency | operative | sufficiency | Proven Operational Adequacy | 0 | NO_ITEMS | Operational adequacy proven through procedure structure |
| E:operative:completeness | operative | completeness | Comprehensive Operational Completeness | 0 | NO_ITEMS | Operational completeness adequate |
| E:operative:consistency | operative | consistency | Disciplined Operational Integrity | 0 | NO_ITEMS | Operational integrity maintained |
| E:evaluative:necessity | evaluative | necessity | Foundational Value Imperative | 0 | NO_ITEMS | Value imperative (transparent separable pricing) well established |
| E:evaluative:sufficiency | evaluative | sufficiency | Proven Value Sufficiency | 1 | HAS_ITEMS | Warranty coverage scope for optional item |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Value Completeness | 0 | NO_ITEMS | Value completeness adequate for proposal |
| E:evaluative:consistency | evaluative | consistency | Principled Value Integrity | 0 | NO_ITEMS | Value integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | Normalization | Multi | Guidance | Normalize upstream dependency references: Procedure states "No upstream dependencies declared in _DEPENDENCIES.md" but then lists two assumptions about DEL-03-01 and DEL-02-06; clarify whether these are formal dependencies or informational notes | Procedure Prerequisites section contradicts itself by stating no upstream dependencies exist while simultaneously noting assumed dependencies on DEL-03-01 (site plan) and DEL-02-06 (base electrical); terminology should be normalized | Procedure.md | Prerequisites (Upstream Dependencies subsection) | -- | Procedure.md / _DEPENDENCIES.md | TBD |
| E-002 | E:evaluative:sufficiency | WeakStatement | Procedure | Specification | Clarify whether 12-month warranty stated in Procedure B5 applies to Owner-elected optional items or only base scope; confirm warranty scope in Specification | Procedure Step B5 states "12-month warranty consistent with base scope" but Specification does not address warranty for this optional item; it is unclear whether the base scope warranty terms automatically extend to Owner-elected additions | Procedure.md, Specification.md | Procedure Step B5; Specification entire document scanned | -- | Contract / legal review | TBD |
