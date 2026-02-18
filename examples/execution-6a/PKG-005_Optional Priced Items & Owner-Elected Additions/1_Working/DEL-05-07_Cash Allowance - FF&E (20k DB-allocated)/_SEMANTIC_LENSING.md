# Semantic Lensing Register: DEL-05-07 Cash Allowance -- FF&E ($20k; DB-Allocated)

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-07_Cash Allowance - FF&E (20k DB-allocated)/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-07 context (deliverable identity, scope coverage SOW-0506, anticipated artifacts, DEC-005)
- _STATUS.md -- Current state SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (plus K transpose, not lensed per spec)
- Datasheet.md -- Present and read (identification, attributes, conditions, construction, references)
- Specification.md -- Present and read (scope, REQ-01 through REQ-08, standards, verification, documentation)
- Guidance.md -- Present and read (purpose, P-01 through P-05, C-01 through C-05, T-01/T-02, conflict table CON-001/CON-002)
- Procedure.md -- Present and read (Phase A steps A-1 through A-7, Phase B steps B-1 through B-5, verification, records)
- _REFERENCES.md -- Present and read (Addendum 03 section 1.18)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 2
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 3  B: 2  C: 2  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 4
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Source of $20k value ambiguity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Verification of separate pricing |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Verification table covers REQ-01 through REQ-08 adequately |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | No regulatory audit gap identified; deliverable is an allowance package not subject to AHJ review |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Both phases (proposal and admin) are well-directed in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are actionable with clear outputs |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing acceptance criteria for boundary definition quality |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal review step A-7 covers audit; adequate for proposal phase |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | P-01 through P-05 provide sufficient value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T-01/T-02 address merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Value proposition is clear: $20k separable allowance for Owner flexibility |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | No quality appraisal gap; scope is narrow and well-bounded |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify in REQ-01 the authoritative source for the $20,000 figure: Addendum 03 directs FF&E as "additional item" but does not state the dollar value; DEC-005 sets $20k | Guidance CON-001 identifies this ambiguity but the Specification REQ-01 cites both sources without noting that neither Addendum 03 alone establishes the value. Under a prescriptive-direction lens, the normative authority chain is unclear. | Specification.md; Guidance.md | Specification#REQ-01; Guidance#CON-001 | Specification.md#REQ-01 vs Guidance.md#CON-001 | DEC-005 for dollar value; Addendum 03 for treatment as separate item | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add verification criterion for REQ-02 confirming that FF&E line item is not subtotaled or aggregated with base costs in any summary table | REQ-02 requires separate pricing presentation; verification says "confirm FF&E appears as a distinct line, not embedded in base costs" but does not address how to verify in summary/aggregate tables where items might be re-combined | Specification.md | Specification#Verification (REQ-02 row) | -- | Specification | TBD |
| A-003 | A:operative:judging | MissingSlot | Specification | Specification | Add acceptance criteria for the quality/adequacy of the FF&E boundary definition (REQ-05) beyond mere presence -- e.g., minimum number of item classifications, or explicit semi-fixed item treatment | Verification for REQ-05 says only "Confirm written definition distinguishes FF&E from base construction." Under a performance-assessment lens, there is no criterion for whether the boundary definition is substantive enough to prevent disputes. | Specification.md | Specification#Verification (REQ-05 row) | -- | Specification | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Tax treatment of allowance not stated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations are present across all docs |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing currency/tax note |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dollar figures are consistent ($20k) across all docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (separation, Owner election, DB responsibility) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Narrative coverage is thorough |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message is coherent across all four docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding of allowance mechanics is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | DB expertise assumptions are stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of topic is thorough for proposal stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | No contradictions in knowledge/understanding across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs and principles provide adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance in T-01/T-02 is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers holistic picture |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-01 through P-05 are internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Is the $20,000 allowance inclusive or exclusive of applicable taxes (GST/PST)? If exclusive, note that procurement costs may reduce the effective allocation available for FF&E items. | Under an essential-fact lens, the tax treatment of the $20k allowance is not stated anywhere in the four documents. This is a necessary factual input for both the DB (procurement budgeting) and Owner (cost evaluation). | Datasheet.md; Specification.md | Datasheet#Attributes; Specification#REQ-01 | -- | Owner / contract terms | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a row to the Attributes table noting tax treatment (inclusive/exclusive) or flag as TBD pending Owner clarification | The Datasheet records the allowance value but does not note whether it is pre-tax or inclusive. Under a comprehensive-record lens, this is an expected data point for a financial allowance. | Datasheet.md | Datasheet#Attributes | -- | Datasheet | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 0 | NO_ITEMS | No regulatory imperative gap; this is a contractual allowance, not a code-driven item |
| C:normative:sufficiency | normative | sufficiency | Compliance Substantiation | 1 | HAS_ITEMS | Standards table incomplete |
| C:normative:completeness | normative | completeness | Regulatory Completeness | 0 | NO_ITEMS | Coverage of normative requirements is complete |
| C:normative:consistency | normative | consistency | Regulatory Conformity | 0 | NO_ITEMS | No conformity issues detected |
| C:operative:necessity | operative | necessity | Operational Imperative | 0 | NO_ITEMS | Operational needs are addressed by both phases |
| C:operative:sufficiency | operative | sufficiency | Operational Competence | 0 | NO_ITEMS | Procedure steps provide sufficient operational detail |
| C:operative:completeness | operative | completeness | Operational Thoroughness | 1 | HAS_ITEMS | Post-award warranty period FF&E handling not addressed |
| C:operative:consistency | operative | consistency | Operational Fidelity | 0 | NO_ITEMS | Procedure and Specification are operationally consistent |
| C:evaluative:necessity | evaluative | necessity | Value Imperative | 0 | NO_ITEMS | Value proposition is clearly stated |
| C:evaluative:sufficiency | evaluative | sufficiency | Value Substantiation | 0 | NO_ITEMS | Value reasoning in Guidance is adequate |
| C:evaluative:completeness | evaluative | completeness | Value Thoroughness | 0 | NO_ITEMS | Coverage of value considerations is sufficient |
| C:evaluative:consistency | evaluative | consistency | Value Fidelity | 0 | NO_ITEMS | Value messaging is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | TBD_Question | Specification | Specification | Record TBD: Confirm whether any Town of Penhold procurement policy or furniture standard (e.g., BIFMA, fire-retardant rating for institutional furnishings) applies to FF&E selections under this allowance | Specification Standards table notes Town procurement policy as "location TBD -- not in accessible sources" and includes an ASSUMPTION about no furniture standard. Under a compliance-substantiation lens, the absence of confirmed standard applicability is a gap that could surface post-award. | Specification.md | Specification#Standards | -- | Owner / Town procurement office | TBD |
| C-002 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a note or step addressing FF&E warranty and deficiency handling during the warranty period (e.g., who is responsible for FF&E defects -- manufacturer warranty vs. DB obligation) | Procedure covers reconciliation at substantial completion (Step B-5) but does not address what happens to FF&E items during the warranty period. Under an operational-thoroughness lens, the post-closeout lifecycle of FF&E items is a gap. | Procedure.md | Procedure#Phase B | -- | Procedure (or Guidance for rationale) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compliance Foundation | 0 | NO_ITEMS | Foundation of compliance (Addendum 03, DEC-005) is well-established |
| F:normative:sufficiency | normative | sufficiency | Compliance Threshold | 1 | HAS_ITEMS | Threshold for "adequate" boundary definition unclear |
| F:normative:completeness | normative | completeness | Compliance Coverage | 0 | NO_ITEMS | REQ-01 through REQ-08 cover anticipated artifacts |
| F:normative:consistency | normative | consistency | Compliance Discipline | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | Operational Foundation | 1 | HAS_ITEMS | Records table artifact count mismatch |
| F:operative:sufficiency | operative | sufficiency | Operational Threshold | 0 | NO_ITEMS | Steps provide sufficient detail for execution |
| F:operative:completeness | operative | completeness | Operational Coverage | 0 | NO_ITEMS | Both phases are covered |
| F:operative:consistency | operative | consistency | Operational Discipline | 1 | HAS_ITEMS | Normalization: "4 artifacts" vs "5 artifacts" |
| F:evaluative:necessity | evaluative | necessity | Value Foundation | 0 | NO_ITEMS | Value foundation is clear |
| F:evaluative:sufficiency | evaluative | sufficiency | Value Threshold | 0 | NO_ITEMS | Value thresholds addressed in trade-offs |
| F:evaluative:completeness | evaluative | completeness | Value Coverage | 0 | NO_ITEMS | Value coverage is adequate |
| F:evaluative:consistency | evaluative | consistency | Value Discipline | 0 | NO_ITEMS | Value discipline is maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-05 verification to include minimum content requirements for boundary definition (e.g., must address permanently attached vs. freestanding, must address semi-fixed items, must address appliance overlap with DEL-05-06) | Under a compliance-threshold lens, the verification for REQ-05 says "Confirm written definition distinguishes FF&E from base construction" but does not specify what constitutes an adequate distinction. The threshold for compliance is ambiguous. | Specification.md | Specification#Verification (REQ-05 row) | -- | Specification | TBD |
| F-002 | F:operative:necessity | Normalization | Procedure | Procedure | Correct Records table: "4 artifacts + allocation schedule" should read "5 artifacts" (boundary definition, allocation schedule, procurement notes, reconciliation approach, exclusions/assumptions) to match Specification Documentation section which lists 5 items | The Records table in Procedure says "DEL-05-07 proposal package (4 artifacts + allocation schedule)" implying the allocation schedule is separate from the other 4. However, Specification Documentation lists 5 required artifacts including the allocation schedule as one of the 5. This creates a minor counting inconsistency. | Procedure.md; Specification.md | Procedure#Records; Specification#Documentation | Procedure.md#Records vs Specification.md#Documentation | Specification (5 artifacts) | TBD |
| F-003 | F:operative:consistency | Normalization | Multi | Multi | Standardize artifact count terminology across Procedure Records table and Specification Documentation section: use "5 required artifacts" consistently | Under an operational-discipline lens, the inconsistent counting (4+1 vs 5) could cause confusion about whether the allocation schedule is a standalone artifact or part of the bundle. | Procedure.md; Specification.md | Procedure#Records; Specification#Documentation | Procedure.md#Records vs Specification.md#Documentation | Specification naming convention | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Mandate | 0 | NO_ITEMS | Mandate is settled (Addendum 03 + DEC-005) |
| D:normative:applying | normative | applying | Binding Standard | 1 | HAS_ITEMS | RFP full text not reviewed |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance determination approach is adequate |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Scrutiny | 0 | NO_ITEMS | No regulatory scrutiny applicable to allowance package |
| D:operative:guiding | operative | guiding | Settled Process Direction | 0 | NO_ITEMS | Process direction is settled in Procedure |
| D:operative:applying | operative | applying | Resolved Execution Standard | 0 | NO_ITEMS | Execution standard is clear |
| D:operative:judging | operative | judging | Definitive Process Assessment | 0 | NO_ITEMS | Assessment criteria present in verification tables |
| D:operative:reviewing | operative | reviewing | Resolved Process Scrutiny | 0 | NO_ITEMS | Internal review step covers process scrutiny |
| D:evaluative:guiding | evaluative | guiding | Settled Value Direction | 0 | NO_ITEMS | Value direction settled in Guidance |
| D:evaluative:applying | evaluative | applying | Resolved Merit Standard | 1 | HAS_ITEMS | No merit criteria for allocation quality |
| D:evaluative:judging | evaluative | judging | Definitive Worth Assessment | 0 | NO_ITEMS | Worth assessment is implicit in $20k cap |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Scrutiny | 0 | NO_ITEMS | Quality appraisal adequate for deliverable type |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | TBD_Question | Specification | Specification | Record TBD: Review full RFP 2024_004 text for any pricing format requirements that may apply to how the FF&E allowance must be presented in the proposal | Specification Standards table notes "RFP 2024_004 (main document) -- location TBD -- full text not reviewed." Under a binding-standard lens, there may be proposal pricing format requirements in the RFP that govern how optional items must be presented. This has not been confirmed. | Specification.md | Specification#Standards | -- | RFP 2024_004 text | TBD |
| D-002 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add rationale for why category-level (by space) is the appropriate granularity for the allocation schedule, rather than item-level or lump-sum-level | T-01 resolves the specificity tension in favor of category-level allocation, but the rationale could be strengthened by explaining why this particular granularity (not more, not less) serves the Owner's evaluation needs. Under a resolved-merit-standard lens, the merit basis for this resolution is thin. | Guidance.md | Guidance#T-01 | -- | Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Governing Requirement | 0 | NO_ITEMS | Governing requirements are identified |
| X:guiding:sufficiency | guiding | sufficiency | Governance Substantiation | 0 | NO_ITEMS | Governance chain is substantiated |
| X:guiding:completeness | guiding | completeness | Governance Comprehensiveness | 1 | HAS_ITEMS | OBJ-010 linkage is assumption-based |
| X:guiding:consistency | guiding | consistency | Governance Coherence | 0 | NO_ITEMS | Governance messaging is coherent |
| X:applying:necessity | applying | necessity | Implementation Requirement | 1 | HAS_ITEMS | Delivery/installation coordination detail |
| X:applying:sufficiency | applying | sufficiency | Implementation Competence | 0 | NO_ITEMS | Implementation competence is assumed (DB responsibility) |
| X:applying:completeness | applying | completeness | Implementation Coverage | 1 | HAS_ITEMS | Missing lead-time planning detail |
| X:applying:consistency | applying | consistency | Implementation Integrity | 0 | NO_ITEMS | Implementation instructions are consistent |
| X:judging:necessity | judging | necessity | Adjudicative Requirement | 0 | NO_ITEMS | Adjudication criteria present in verification tables |
| X:judging:sufficiency | judging | sufficiency | Adjudicative Substantiation | 0 | NO_ITEMS | Verification approaches are substantive |
| X:judging:completeness | judging | completeness | Adjudicative Comprehensiveness | 1 | HAS_ITEMS | No verification for REQ-05 boundary quality |
| X:judging:consistency | judging | consistency | Adjudicative Coherence | 0 | NO_ITEMS | Verification criteria are coherent across docs |
| X:reviewing:necessity | reviewing | necessity | Audit Requirement | 0 | NO_ITEMS | Audit trail is established via Records table |
| X:reviewing:sufficiency | reviewing | sufficiency | Audit Substantiation | 0 | NO_ITEMS | Records are sufficient for audit |
| X:reviewing:completeness | reviewing | completeness | Audit Comprehensiveness | 0 | NO_ITEMS | Records table is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Audit Coherence | 0 | NO_ITEMS | Audit trail is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | WeakStatement | Guidance | Guidance | Strengthen the OBJ-010 linkage from assumption-level to confirmed: either verify that OBJ-010 explicitly covers SOW-0506, or note that the association is inferred from package grouping | Guidance Purpose states OBJ-010 association is an ASSUMPTION "based on package-grouping heuristic." Under a governance-comprehensiveness lens, the objective linkage should either be confirmed or clearly flagged as unverified in all docs. | Guidance.md | Guidance#Purpose | -- | Decomposition / OBJ-010 definition | TBD |
| X-002 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add a note to Step B-4 about coordination requirements with the construction schedule for FF&E delivery and installation (e.g., storage requirements if FF&E arrives before installation area is ready) | Step B-4 says "Coordinate installation timing with construction schedule (typically near substantial completion)" but does not address what happens if FF&E is procured before the space is ready. Under an implementation-requirement lens, staging/storage is a practical gap. | Procedure.md | Procedure#Step B-4 | -- | Procedure | TBD |
| X-003 | X:applying:completeness | RationaleGap | Guidance | Guidance | Add guidance on lead-time planning for FF&E procurement relative to construction schedule milestones, explaining why early procurement decisions may be needed for long-lead items | Step A-3 mentions "lead-time considerations" as a topic for procurement notes, but Guidance does not explain why lead times matter or how they interact with the design-build schedule. Under an implementation-coverage lens, the rationale for timing is missing. | Guidance.md; Procedure.md | Guidance#C-03; Procedure#Step A-3 | -- | Guidance | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification criteria for REQ-05 that test boundary definition adequacy: must address at least (a) permanently attached vs. freestanding, (b) semi-fixed items, (c) appliance overlap with DEL-05-06 | This reinforces A-003 and F-001 from a verification-specific lens. The adjudicative comprehensiveness lens reveals that the verification table has no way to determine whether the boundary definition is materially adequate vs. merely present. | Specification.md | Specification#Verification (REQ-05 row) | -- | Specification | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Authoritative Obligation | 0 | NO_ITEMS | Authoritative obligations are met |
| E:normative:sufficiency | normative | sufficiency | Authoritative Verification | 1 | HAS_ITEMS | CON-001 not resolved in Specification |
| E:normative:completeness | normative | completeness | Authoritative Thoroughness | 0 | NO_ITEMS | Normative coverage is thorough |
| E:normative:consistency | normative | consistency | Authoritative Integrity | 0 | NO_ITEMS | Normative integrity is maintained |
| E:operative:necessity | operative | necessity | Operational Obligation | 0 | NO_ITEMS | Operational obligations are covered |
| E:operative:sufficiency | operative | sufficiency | Operational Verification | 0 | NO_ITEMS | Operational verification is adequate |
| E:operative:completeness | operative | completeness | Operational Comprehensiveness | 0 | NO_ITEMS | Operational coverage is comprehensive |
| E:operative:consistency | operative | consistency | Operational Integrity | 0 | NO_ITEMS | Operational integrity is maintained |
| E:evaluative:necessity | evaluative | necessity | Evaluative Obligation | 1 | HAS_ITEMS | Conflict: scope overlap with DEL-05-06 |
| E:evaluative:sufficiency | evaluative | sufficiency | Evaluative Verification | 0 | NO_ITEMS | Evaluative verification is adequate |
| E:evaluative:completeness | evaluative | completeness | Evaluative Comprehensiveness | 0 | NO_ITEMS | Evaluative coverage is complete |
| E:evaluative:consistency | evaluative | consistency | Evaluative Integrity | 0 | NO_ITEMS | Evaluative integrity is maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | VerificationGap | Specification | Specification | Add a verification step or cross-reference in the Specification Verification table confirming that CON-001 (source of $20k figure) has been resolved or accepted before final submission | Guidance CON-001 identifies that the $20k value source is split between Addendum 03 (which does not state the dollar value) and DEC-005 (which does). Under an authoritative-verification lens, the Specification should either resolve this or include a verification check that the conflict has been addressed. | Specification.md; Guidance.md | Specification#Verification; Guidance#CON-001 | -- | Human ruling on CON-001 | TBD |
| E-002 | E:evaluative:necessity | Conflict | Multi | TBD | Confirm whether freestanding kitchen appliances (e.g., microwave, coffee maker) fall under FF&E allowance (DEL-05-07/SOW-0506) or Appliances allowance (DEL-05-06/SOW-0505); update boundary definition and exclusions accordingly | Guidance CON-002 identifies this overlap. Under an evaluative-obligation lens, the obligation to provide clear value to the Owner requires this boundary to be resolved. The Datasheet excludes appliances from FF&E by assumption, the Guidance flags the overlap, and the Procedure exclusions step mentions it, but no authoritative resolution exists. | Guidance.md; Datasheet.md; Procedure.md | Guidance#CON-002; Datasheet#Conditions; Procedure#Step A-5 | Guidance.md#CON-002 (FF&E) vs Decomposition DEL-05-06 (Appliances) | Owner decision | TBD |
