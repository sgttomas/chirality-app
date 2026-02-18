# Semantic Lensing Register: DEL-03-04 Site Utilities Distribution & Allowance-Based Tie-Ins

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-04_Site Utilities Distribution & Allowance-Based Tie-Ins/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-03-04; PKG-003; Civil/Utilities; SOW-0109, SOW-0110
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- All 7 matrices (A, B, C, F, D, X, E) parsed successfully
- Datasheet.md -- Present and read
- Specification.md -- Present and read
- Guidance.md -- Present and read
- Procedure.md -- Present and read
- _REFERENCES.md -- Present and read

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 3
  - Specification: 8
  - Guidance: 4
  - Procedure: 4
  - Multi: 5
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards TBD items |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Allowance format TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for standards compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure covers AHJ sign-offs adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing upstream dependency declaration |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are detailed and sequenced |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Verification approach weak for service testing |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P4 covers allowance transparency rationale |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs documented in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Allowance reconciliation covers value accounting |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification table in Procedure is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify specific Town of Penhold municipal servicing standards and bylaws applicable to water/wastewater connections; confirm Alberta Safety Codes Act specific clauses for utility permits | Standards table lists 4 entries as "ASSUMPTION: likely applicable" or "TBD -- to be confirmed" with no specific clause references, making prescriptive direction incomplete | Specification.md | ## Standards | -- | Specification (Standards table) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify whether REQ-09 Allowance Management Plan has a mandatory format or if format is entirely at DB discretion; currently states "ASSUMPTION: specific format requirements for the allowance management plan are TBD pending Owner direction" | A mandatory practice lens reveals that the format requirement is ambiguous -- the requirement exists but its prescriptive content is deferred, which could lead to rejected submittals | Specification.md | ### REQ-09: Allowance Management Plan | -- | Specification | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-06 (Civil Design Standards) specifying which codes/standards the design review checks against, rather than the generic "Design review against OSR and applicable codes" | The verification approach for REQ-06 is circular -- it says "review against OSR and applicable codes" but the Standards table does not confirm which codes are applicable, so compliance determination has no concrete referent | Specification.md | ## Verification (REQ-06 row) | -- | Specification | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit upstream dependency declarations for DEL-03-01 (Site Plan) and DEL-03-02 (Grading/Stormwater) as procedural prerequisites, not just assumptions | Procedure notes these as "useful context" under an ASSUMPTION tag but does not declare them as formal prerequisites; procedural direction requires clear dependency signaling to avoid sequencing errors | Procedure.md | ### Declared Upstream Dependencies | -- | Procedure | TBD |
| A-005 | A:operative:judging | WeakStatement | Procedure | Specification | Strengthen verification for service testing (Procedure check "All utility services live and tested before occupancy") by specifying pass/fail criteria for each utility type (e.g., water pressure range, electrical energization confirmation, gas pressure test hold duration) | Performance assessment lens reveals that the verification check is outcome-stated ("live and tested") but lacks measurable acceptance thresholds for each of the five utility types | Procedure.md | ## Verification (row: "All utility services live and tested before occupancy") | -- | Specification | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing stub depth/invert data |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references are adequate for current phase |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Cold Storage utility sizing absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Stub proximity descriptions are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing provider identification |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for the allowance mechanism |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All five utility types are consistently enumerated |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology normalization needed |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance principles cover design rationale |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. requirement established |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Trade-offs and considerations cover the domain |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | DEC-004 rationale is documented in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off resolutions are reasoned |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers both technical and commercial dimensions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential factual data for each stub: invert elevation/depth, pipe diameter/conduit size, and service capacity (where known or to be confirmed post-award) | The Datasheet records stub proximity (e.g., "at site corner," "within a few feet") but omits dimensional/elevation data that is essential for routing design; these are essential facts that should at minimum be flagged as TBD with a placeholder | Datasheet.md | ### Utility Types In Scope | -- | Datasheet | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a row or section for Cold Storage Building utility service requirements (which utility types are needed, estimated loads/sizing) distinct from Main PSB | The Datasheet notes both buildings must be served but does not enumerate which utilities are required for the Cold Storage Building specifically or whether all five apply; comprehensive record requires per-building coverage | Datasheet.md | ### Buildings Receiving Utility Services | -- | Datasheet | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Datasheet | Record TBD: Identify each Utility Provider by name (water/wastewater authority, electrical utility company, gas provider, telecom provider) for Penhold; these are essential signals for coordination planning | Procedure step B2 references provider names as examples (ATCO Gas, Town of Penhold) but these are assumptions; the Datasheet does not list confirmed provider names, which are essential information for coordination | Datasheet.md, Procedure.md | Datasheet: entire document scanned; Procedure: ### Phase B step B2 | -- | Datasheet | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "Utility Provider" vs. "utility provider" vs. "provider" -- adopt a single capitalized term and define it once in Guidance, then use consistently | Documents alternate between capitalized "Utility Provider" (Specification REQ-01, Procedure) and lowercase "utility provider" (Guidance P2); a coherent message requires consistent terminology | Specification.md, Guidance.md, Procedure.md | Specification: REQ-01; Guidance: P2; Procedure: B2 | -- | Guidance | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Obligation Threshold | 1 | HAS_ITEMS | Obligation threshold unclear for permit costs |
| C:normative:sufficiency | normative | sufficiency | Compliance Sufficiency Standard | 0 | NO_ITEMS | REQ-07 P.Eng. sealing is clear |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Incomplete code coverage |
| C:normative:consistency | normative | consistency | Regulatory Uniformity | 0 | NO_ITEMS | Requirements are internally consistent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is adequate |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | P.Eng. and personnel prerequisites cover capability |
| C:operative:completeness | operative | completeness | End-to-End Implementation | 1 | HAS_ITEMS | Missing frost depth consideration |
| C:operative:consistency | operative | consistency | Operational Reliability | 0 | NO_ITEMS | Process steps are coherent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Purpose and value are established |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Appraisal | 0 | NO_ITEMS | Appraisal approach is adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal | 0 | NO_ITEMS | Verification table covers all requirements |
| C:evaluative:consistency | evaluative | consistency | Evaluative Integrity | 0 | NO_ITEMS | Evaluation criteria are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Procedure | Specification | Clarify whether utility permit costs fall within the cash allowance or are separately tracked; Procedure step B4 states "ASSUMPTION: Permit costs may be included within the cash allowance or separately tracked -- TBD based on Owner direction" | The regulatory obligation threshold for permit cost treatment is ambiguous; this affects both pricing and allowance management and needs a binding decision | Procedure.md | ### Phase B step B4 | -- | Specification (or Owner decision) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add specific code references for underground utility installation (e.g., CSA Z662 for gas, CSA C22.1 for electrical, Alberta Private Sewage Systems Standard of Practice for wastewater if applicable) to achieve full regulatory coverage | The Standards table in Specification lists broad categories (Alberta Safety Codes Act, ABC) but lacks the specific code sections that govern underground utility installation for each service type; full regulatory coverage requires these references | Specification.md | ## Standards | -- | Specification | TBD |
| C-003 | C:operative:completeness | RationaleGap | Guidance | Guidance | Add a consideration for minimum burial depth requirements (frost depth in Penhold, Alberta area) and how this affects trench design for water, gas, and wastewater lines | End-to-end implementation of utility trenching requires addressing frost penetration depth, which is a critical design parameter for central Alberta (~1.8m typical) but is not mentioned in any document; Guidance should note this as a design consideration | Guidance.md | ## Considerations | -- | Guidance | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Prescriptive Compliance Baseline | 1 | HAS_ITEMS | Baseline incomplete for provider-specific standards |
| F:normative:sufficiency | normative | sufficiency | Mandated Conformance Proof | 1 | HAS_ITEMS | Missing proof mechanism for provider standards |
| F:normative:completeness | normative | completeness | Total Regulatory Accounting | 0 | NO_ITEMS | Addressed by C-002 already |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | No conflicting standards detected |
| F:operative:necessity | operative | necessity | Validated Execution Readiness | 1 | HAS_ITEMS | Readiness gate missing |
| F:operative:sufficiency | operative | sufficiency | Substantiated Execution Competence | 0 | NO_ITEMS | Personnel prerequisites are clear |
| F:operative:completeness | operative | completeness | Comprehensive Delivery Assurance | 0 | NO_ITEMS | Phase structure covers design through closeout |
| F:operative:consistency | operative | consistency | Disciplined Execution Consistency | 0 | NO_ITEMS | Steps are consistently structured |
| F:evaluative:necessity | evaluative | necessity | Fundamental Value Priority | 0 | NO_ITEMS | Value priorities are established (P1-P5) |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Assessment | 0 | NO_ITEMS | Trade-offs are reasoned |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 1 | HAS_ITEMS | Missing allowance reporting frequency |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Consistency | 0 | NO_ITEMS | Merit reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add a requirement that the DB shall obtain and comply with each Utility Provider's specific connection standards, and that evidence of compliance with provider standards shall be part of the verification record | REQ-01 requires coordination with providers and REQ-06 requires compliance with "applicable codes," but there is no explicit requirement to obtain and follow provider-specific connection standards as a prescriptive baseline; the verification row for REQ-01 only requires "evidence of coordination correspondence" not evidence of standards compliance | Specification.md | ### REQ-01, ## Verification | -- | Specification | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Procedure | Add a verification step confirming that each Utility Provider has formally accepted the DB's connection design before construction begins (provider design approval as a conformance proof gate) | Mandated conformance proof requires demonstrating that the design meets provider requirements before execution; Procedure step B2 mentions obtaining provider standards but does not include a gate for provider design approval before proceeding to construction | Specification.md, Procedure.md | Specification: ## Verification (REQ-01); Procedure: ### Phase B step B2 | -- | Procedure | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add an explicit readiness gate between Phase B (Design) and Phase C (Construction) that validates: (a) Owner-provided drawings received, (b) provider design approvals obtained, (c) permits in hand, (d) allowance management plan approved | Validated execution readiness requires a clear gate before construction begins; currently the transition from Phase B to Phase C is implicit with no readiness checklist or hold point | Procedure.md | Between ### Phase B and ### Phase C | -- | Procedure | TBD |
| F-004 | F:evaluative:completeness | WeakStatement | Procedure | Specification | Specify the reporting frequency for allowance tracking (e.g., monthly, per drawdown event) in the Allowance Management Plan requirements; currently step B5 lists "Reporting frequency" as an item to include but the Specification does not mandate a frequency | Exhaustive merit accounting requires knowing how often the Owner will receive cost information; the requirement to include reporting frequency exists in Procedure but the Specification does not set a minimum, leaving it entirely discretionary | Procedure.md, Specification.md | Procedure: ### Phase B step B5; Specification: ### REQ-09 | -- | Specification | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Regulatory Direction | 0 | NO_ITEMS | Covered by A-001, C-002 |
| D:normative:applying | normative | applying | Resolved Compliance Practice | 1 | HAS_ITEMS | Practice not resolved for provider variation |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Verification table is adequate at current maturity |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Examination | 0 | NO_ITEMS | AHJ sign-off process covered in Procedure Phase D |
| D:operative:guiding | operative | guiding | Resolved Operational Guidance | 0 | NO_ITEMS | Guidance principles P1-P5 are clear |
| D:operative:applying | operative | applying | Resolved Execution Deployment | 1 | HAS_ITEMS | Trench backfill specification absent |
| D:operative:judging | operative | judging | Definitive Performance Confirmation | 0 | NO_ITEMS | Service testing covers this adequately (though A-005 flags threshold detail) |
| D:operative:reviewing | operative | reviewing | Resolved Process Examination | 0 | NO_ITEMS | Records section is adequate |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Orientation | 0 | NO_ITEMS | Value orientation is established in Guidance |
| D:evaluative:applying | evaluative | applying | Resolved Merit Application | 1 | HAS_ITEMS | Missing cost estimation guidance |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | Allowance reconciliation process covers this |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Examination | 0 | NO_ITEMS | Quality checks in Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | RationaleGap | Guidance | Guidance | Add a consideration explaining how to handle variation in provider connection processes (e.g., some providers require their own contractors for final connection, some allow the DB to self-perform); this affects execution planning | Resolved compliance practice requires understanding provider-specific process variation; Guidance does not discuss the practical reality that different providers may have different requirements for who performs the physical connection | Guidance.md | ## Considerations | -- | Guidance | TBD |
| D-002 | D:operative:applying | MissingSlot | Specification | Specification | Add a requirement for trench backfill and compaction standards for utility trenches (material specification, compaction percentage, testing requirements) | Resolved execution deployment for utility trenching requires backfill specification; Procedure step C1 references "bedding, pipe/conduit installation, and backfill" but no specification requirement governs backfill quality; this is a standard civil engineering requirement that is absent | Specification.md | ## Requirements (after REQ-11) | -- | Specification | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add guidance on how the DB should develop preliminary cost estimates for each utility tie-in to support the Owner's allowance budgeting, even though the allowance value is not pre-set | Resolved merit application requires understanding how the Owner will set or validate the allowance amount; Guidance discusses transparency (P4) but not how initial cost estimates should be developed or communicated to the Owner for budgeting | Guidance.md | ## Considerations | -- | Guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Directed Imperative Scope | 0 | NO_ITEMS | Scope boundaries are clear |
| X:guiding:sufficiency | guiding | sufficiency | Justified Guidance Threshold | 0 | NO_ITEMS | Guidance principles are adequate |
| X:guiding:completeness | guiding | completeness | Thorough Directive Span | 0 | NO_ITEMS | Directives span proposal through closeout |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Coherence | 0 | NO_ITEMS | Direction is consistent across documents |
| X:applying:necessity | applying | necessity | Critical Practice Baseline | 1 | HAS_ITEMS | Locate requirement assumed, not specified |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Practice Fitness | 0 | NO_ITEMS | Practice steps are sufficiently detailed |
| X:applying:completeness | applying | completeness | Comprehensive Application Span | 0 | NO_ITEMS | Phase A through E covers full lifecycle |
| X:applying:consistency | applying | consistency | Principled Practice Reliability | 0 | NO_ITEMS | Practice steps are consistent |
| X:judging:necessity | judging | necessity | Binding Necessity Verdict | 0 | NO_ITEMS | Verification table covers all requirements |
| X:judging:sufficiency | judging | sufficiency | Validated Sufficiency Judgment | 1 | HAS_ITEMS | Sufficiency judgment gap for drawings review |
| X:judging:completeness | judging | completeness | Comprehensive Judgment Scope | 0 | NO_ITEMS | Judgment scope covers all artifacts |
| X:judging:consistency | judging | consistency | Principled Adjudication Coherence | 0 | NO_ITEMS | Adjudication approach is consistent |
| X:reviewing:necessity | reviewing | necessity | Critical Audit Prerequisite | 1 | HAS_ITEMS | Missing design review milestone verification |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Fitness | 0 | NO_ITEMS | Records retention is adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Scope | 0 | NO_ITEMS | Records section covers all artifact types |
| X:reviewing:consistency | reviewing | consistency | Principled Audit Coherence | 0 | NO_ITEMS | Audit approach is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Normalization | Multi | Specification | Elevate Alberta One-Call (or equivalent) locate requirement from ASSUMPTION status in Procedure (step C1) to a formal requirement in Specification; this is a critical practice baseline that should not be assumption-tagged | Procedure step C1 notes "ASSUMPTION: required under provincial regulations" for locates prior to excavation; this is in fact a legal requirement in Alberta, not an assumption, and should be stated as a binding requirement | Procedure.md, Specification.md | Procedure: ### Phase C step C1; Specification: ## Requirements | -- | Specification | TBD |
| X-002 | X:judging:sufficiency | VerificationGap | Specification | Specification | Add verification criteria for utility distribution plan review: specify that the plan shall be reviewed at BDD, 60% DD, and 100% DD/IFC milestones with documented review comments and dispositions | The Specification verification for REQ-08 states "Artifact exists in deliverable package; reviewed and approved through design submission milestones" but does not specify which milestones or what constitutes adequate review; validated sufficiency judgment requires concrete review gates | Specification.md | ## Verification (REQ-08 row) | -- | Specification | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add a verification check confirming that site servicing drawings have been reviewed against Owner-provided underground services drawings to ensure no conflicts with existing services | Critical audit prerequisite: the entire design depends on Owner-provided drawings (OSR section 10.3.2), but no verification step confirms the DB's design was actually reconciled against that source data; this is a fundamental quality check that is missing | Procedure.md | ## Verification | -- | Procedure | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Sovereign Compliance Foundation | 0 | NO_ITEMS | Compliance foundation is established (REQ-01 through REQ-11) |
| E:normative:sufficiency | normative | sufficiency | Definitive Regulatory Fitness | 0 | NO_ITEMS | Regulatory fitness is addressed (standards, P.Eng., verification) |
| E:normative:completeness | normative | completeness | Total Prescriptive Coverage | 0 | NO_ITEMS | Coverage gaps already captured under A, C, F matrices |
| E:normative:consistency | normative | consistency | Harmonized Compliance Norm | 0 | NO_ITEMS | No conflicting compliance norms detected |
| E:operative:necessity | operative | necessity | Validated Operational Mandate | 1 | HAS_ITEMS | Scope clarification needed |
| E:operative:sufficiency | operative | sufficiency | Validated Execution Adequacy | 0 | NO_ITEMS | Execution adequacy is addressed through phased approach |
| E:operative:completeness | operative | completeness | Exhaustive Delivery Validation | 0 | NO_ITEMS | Delivery validation covered by verification table and closeout steps |
| E:operative:consistency | operative | consistency | Disciplined Operational Stability | 0 | NO_ITEMS | Operational approach is stable and consistent |
| E:evaluative:necessity | evaluative | necessity | Foundational Worth Imperative | 0 | NO_ITEMS | Worth imperative established through Guidance principles |
| E:evaluative:sufficiency | evaluative | sufficiency | Validated Merit Adequacy | 0 | NO_ITEMS | Merit adequacy established through trade-off analysis |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 1 | HAS_ITEMS | Contingency/dispute resolution gap |
| E:evaluative:consistency | evaluative | consistency | Principled Value Integrity | 0 | NO_ITEMS | Value integrity maintained across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:necessity | Normalization | Datasheet | Multi | Clarify in Datasheet the buildings-served scope: the ASSUMPTION note mentions Pickled Sand Storage was removed but the phrasing is confusing ("Cold Storage/Pickled Sand (note: ... removed)"); simplify to a definitive statement of exactly two buildings served | Validated operational mandate requires unambiguous scope; the current Datasheet ASSUMPTION paragraph is self-contradicting in structure (lists three buildings then removes one mid-sentence), creating confusion about the actual scope | Datasheet.md | ### Buildings Receiving Utility Services | -- | Datasheet | TBD |
| E-002 | E:evaluative:completeness | TBD_Question | Multi | Guidance | Record TBD: What is the dispute resolution process if actual tie-in costs exceed the Owner's expected allowance budget? Who bears overrun risk? Exhaustive value accounting requires addressing this scenario | The allowance mechanism has no pre-set value (DEC-004), and no document addresses what happens if actual costs significantly exceed expectations; this is a commercial risk that needs Owner direction | Guidance.md, Specification.md | Guidance: ### Cash Allowance Rationale; Specification: ### REQ-03 | -- | Guidance | TBD |
