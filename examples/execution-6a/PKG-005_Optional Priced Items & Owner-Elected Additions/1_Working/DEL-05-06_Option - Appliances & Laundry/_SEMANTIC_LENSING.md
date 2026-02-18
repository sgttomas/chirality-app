# Semantic Lensing Register: DEL-05-06 Option -- Appliances & Laundry

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-06_Option - Appliances & Laundry/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-06 deliverable folder / Context section
- _STATUS.md -- DEL-05-06 deliverable folder / Current State: SEMANTIC_READY
- _SEMANTIC.md -- DEL-05-06 deliverable folder / Matrices A, B, C, F, D, X, E parsed
- Datasheet.md -- DEL-05-06 deliverable folder / Identification, Attributes, Conditions, Construction, References
- Specification.md -- DEL-05-06 deliverable folder / Scope, Requirements, Standards, Verification, Documentation
- Guidance.md -- DEL-05-06 deliverable folder / Purpose, Principles, Considerations, Trade-offs, Conflict Table
- Procedure.md -- DEL-05-06 deliverable folder / Purpose, Prerequisites, Steps (Parts A and B), Verification, Records
- _REFERENCES.md -- DEL-05-06 deliverable folder / Applicable References, Notes

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 4
  - Specification: 8
  - Guidance: 4
  - Procedure: 2
  - Multi: 4
- By matrix:
  - A: 4  B: 4  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards section relies on assumptions rather than confirmed prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Appliance certification requirement is assumed, not mandated with specificity |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach for standards compliance is absent |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit perspective covered adequately by Procedure verification table |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear procedural direction in Parts A and B |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are well-articulated in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance criteria for appliance quality/grade beyond "residential" |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table provides adequate process audit checkpoints |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1 (Transparency First) establishes value orientation clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance trade-offs address merit considerations adequately |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Option election mechanism supports worth determination by Owner |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning steps in Procedure provide quality appraisal checkpoints |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen Standards section: replace assumption-based applicability with confirmed code references or explicit TBD markers requiring DB confirmation at design development | The Standards table lists four standards/codes, each marked "Not directly reviewed; ASSUMPTION: likely applicable." This weakens prescriptive direction -- the DB has no confirmed normative basis for code compliance in this deliverable. | Specification.md | Standards | -- | Specification.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Add explicit requirement that all supplied appliances shall bear CSA or equivalent certification marking; currently stated only as assumption | CSA/UL certification is listed as "ASSUMPTION: standard requirement" rather than a mandatory practice with normative authority. For a Canadian building project, this should be a firm requirement, not an assumption. | Specification.md | Standards | -- | Specification.md | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for standards/code compliance (e.g., "DB to submit code compliance confirmation during design development") | The Verification table covers all REQ items but does not include a verification approach for the Standards section itself. There is no check confirming appliances meet CEC, NPC, NBC/ABC, or CSA requirements. | Specification.md | Verification | -- | Specification.md | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add minimum performance or quality criteria for appliances (e.g., energy rating, warranty duration, capacity thresholds) to enable performance assessment | Beyond "residential-grade," no performance criteria exist for evaluating proposed appliance quality. Without measurable performance benchmarks, the Owner cannot objectively assess whether proposed appliances represent adequate quality. | Specification.md | Requirements | -- | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Laundry location is assumed, not confirmed as essential fact |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence for kitchen appliance scope |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing energy/utility load data for appliances |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Quantities are consistent across all documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | OSR and Functional Program signals are adequately captured |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for kitchen and laundry areas is adequate |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | No account of gas vs. electric decision for range/stove |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding of option mechanics is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | DB expertise expectations are implicit but adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope is narrow enough that mastery is achievable from current docs |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Guidance trade-off T2 raises allowance vs. fixed price but resolution is inconclusive |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Trade-offs and considerations provide holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm laundry set location -- is it Functional Program room 22.0 (Unisex Locker Room) or another designated laundry room? OSR section 12.6 does not specify room number. | The laundry set location is flagged as ASSUMPTION in Datasheet and Specification. This is an essential fact that affects rough-in design, yet no confirmed authority exists. Must be resolved with Owner or design team. | Datasheet.md; Specification.md | Datasheet#Location Context; Specification#REQ-05-06-006 | -- | Owner / Design Team | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add electrical load data for each appliance category (voltage, amperage, circuit requirements) and plumbing connection requirements to Datasheet Attributes | The Datasheet lists appliances by type and quantity but does not record electrical or plumbing connection requirements. This data is essential for verifying base building rough-in adequacy. Procedure Step A4 references these but they are not recorded as factual attributes. | Datasheet.md | Attributes | -- | Datasheet.md | TBD |
| B-003 | B:information:completeness | TBD_Question | Multi | Guidance | Record TBD: Is the stove/oven gas or electric? This affects rough-in scope (gas line vs. electrical circuit), pricing, and code compliance requirements. OSR section 12.6 does not specify fuel type. | No document addresses whether the range/stove is gas or electric. This is a fundamental design decision that affects mechanical rough-in, code compliance (gas fitting vs. electrical), and pricing. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire document scanned | -- | Owner / DB Design Team | TBD |
| B-004 | B:wisdom:necessity | WeakStatement | Guidance | Guidance | Strengthen Trade-off T2 resolution: clarify whether the preferred pricing format is fixed-price, allowance, or hybrid, or explicitly state this is an Owner decision to be confirmed | Trade-off T2 discusses allowance vs. fixed price and proposes a "hybrid approach" but uses hedging language ("may structure part of this as an allowance"). The DB needs clearer direction on which pricing format to use. | Guidance.md | Trade-offs#T2 | -- | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 1 | HAS_ITEMS | Enforceable obligations rely heavily on assumptions for code/certification |
| C:normative:sufficiency | normative | sufficiency | Justified Compliance | 0 | NO_ITEMS | Compliance justification is adequate for OSR-sourced requirements |
| C:normative:completeness | normative | completeness | Exhaustive Compliance | 1 | HAS_ITEMS | Compliance scope does not address appliance warranty obligations |
| C:normative:consistency | normative | consistency | Uniform Adjudication | 0 | NO_ITEMS | Requirements are uniformly structured and consistently numbered |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites in Procedure are well-defined for both phases |
| C:operative:sufficiency | operative | sufficiency | Competent Delivery | 0 | NO_ITEMS | Steps A1-A6 and B1-B6 provide sufficient delivery guidance |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 0 | NO_ITEMS | Execution steps cover both proposal and implementation phases |
| C:operative:consistency | operative | consistency | Disciplined Coordination | 1 | HAS_ITEMS | Coordination between option scope and base scope lacks explicit interface document |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Valuation | 0 | NO_ITEMS | Value proposition of the option is clear |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Appraisal | 0 | NO_ITEMS | Appraisal framework for Owner election is adequate |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Valuation coverage is adequate for option scope |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation | 0 | NO_ITEMS | Valuation principles are consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Specification | Guidance | Add rationale in Guidance explaining why Standards section entries are assumption-based and what the DB must do to confirm them (e.g., "DB shall confirm applicable code editions during design development and update this section") | The Specification Standards section lists four code/standard families as "ASSUMPTION: likely applicable" without rationale for why these are not yet confirmed. A reader cannot determine whether this is a deliberate design-development deferral or an oversight. | Specification.md | Standards | -- | Guidance.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement addressing minimum appliance warranty obligations (e.g., "All appliances shall carry minimum manufacturer warranty of [TBD] years") | No requirement addresses appliance warranty terms. Procedure Step B6 mentions providing warranty cards but there is no normative requirement specifying minimum warranty duration. For Owner-procured equipment in a public building, warranty terms are a standard compliance consideration. | Specification.md; Procedure.md | Specification#Requirements; Procedure#Step B6 | -- | Specification.md | TBD |
| C-003 | C:operative:consistency | MissingSlot | Multi | Procedure | Add a coordination checkpoint or interface register entry clarifying which rough-in elements are base scope (PKG-002) and which are option scope (DEL-05-06) | Guidance P3 states base building design must accommodate appliances regardless of option election, and Procedure Step A4 asks DB to "confirm which rough-ins are included in base scope." However, no explicit interface register or coordination document maps the boundary between base scope rough-in (PKG-002) and option scope (DEL-05-06). This risks scope gaps. | Guidance.md; Procedure.md | Guidance#P3; Procedure#Step A4 | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance | 0 | NO_ITEMS | Mandated conformance points are well-established via REQ items |
| F:normative:sufficiency | normative | sufficiency | Substantiated Adherence | 1 | HAS_ITEMS | REQ-05-06-004 lacks measurable acceptance criteria |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Functional Program reference missing for room 22.0 in References |
| F:normative:consistency | normative | consistency | Coherent Enforcement | 0 | NO_ITEMS | Enforcement mechanisms are consistent across documents |
| F:operative:necessity | operative | necessity | Essential Functional Criterion | 0 | NO_ITEMS | Functional criteria are adequately specified |
| F:operative:sufficiency | operative | sufficiency | Proficient Preparedness | 0 | NO_ITEMS | Prerequisites in Procedure are sufficient |
| F:operative:completeness | operative | completeness | Comprehensive Operational Fulfillment | 0 | NO_ITEMS | Steps cover both production and implementation phases |
| F:operative:consistency | operative | consistency | Systematic Operational Coherence | 0 | NO_ITEMS | Operational steps are coherent with requirements |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth | 0 | NO_ITEMS | Fundamental worth of the option is clearly stated |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth | 0 | NO_ITEMS | Worth is substantiated through pricing transparency |
| F:evaluative:completeness | evaluative | completeness | Definitive Value Assessment | 1 | HAS_ITEMS | No lifecycle cost or total-cost-of-ownership guidance |
| F:evaluative:consistency | evaluative | consistency | Integrated Value Consistency | 0 | NO_ITEMS | Value messaging is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-05-06-004 (e.g., "Installation coordination notes shall address at minimum: [list of categories] with connection type, circuit/pipe size, and location for each") | REQ-05-06-004 requires "installation coordination notes" covering mechanical, electrical, ventilation, and design interfaces but provides no measurable acceptance threshold. The verification approach says "Check notes for mechanical, electrical, ventilation, and design interface items" without specifying what constitutes sufficient coverage. | Specification.md | Requirements#REQ-05-06-004; Verification | -- | Specification.md | TBD |
| F-002 | F:normative:completeness | Normalization | Datasheet | Multi | Add Functional Program section 22.0 (Unisex Locker Room) to Datasheet References table; currently referenced in Location Context but absent from the formal References section | The Datasheet Location Context section references "Functional Program room 22.0" but the References table lists only Functional Program section 16.0. This inconsistency could cause a reviewer to miss the laundry location authority. | Datasheet.md | Location Context; References | -- | Datasheet.md | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration in Guidance addressing lifecycle cost comparison (e.g., residential vs. commercial appliance expected lifespan in a public-use facility) to support Owner's value assessment | The Guidance trade-off T1 discusses residential vs. commercial grade but only in terms of upfront cost and rough-in requirements. For a public facility with multi-decade expected use, lifecycle cost (replacement frequency, energy consumption, maintenance) is relevant to the Owner's election decision but is not addressed. | Guidance.md | Trade-offs#T1 | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Directive authority from OSR section 12.6 is clearly resolved |
| D:normative:applying | normative | applying | Verified Compulsory Practice | 1 | HAS_ITEMS | No requirement for DB to submit compliance confirmation |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance determination is supported by verification table |
| D:normative:reviewing | normative | reviewing | Conclusive Compliance Oversight | 0 | NO_ITEMS | Oversight is addressed through Procedure verification checks |
| D:operative:guiding | operative | guiding | Settled Process Governance | 0 | NO_ITEMS | Process governance is well-established |
| D:operative:applying | operative | applying | Validated Implementation Readiness | 0 | NO_ITEMS | Implementation readiness checks are present in Procedure |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 0 | NO_ITEMS | Commissioning steps provide conclusive performance check |
| D:operative:reviewing | operative | reviewing | Settled Process Integrity | 0 | NO_ITEMS | Process integrity is maintained through structured steps |
| D:evaluative:guiding | evaluative | guiding | Settled Value Direction | 0 | NO_ITEMS | Value direction is settled by OBJ-010 and Guidance P1 |
| D:evaluative:applying | evaluative | applying | Validated Merit Realization | 1 | HAS_ITEMS | No mechanism for Owner to compare option price against market |
| D:evaluative:judging | evaluative | judging | Definitive Merit Verdict | 0 | NO_ITEMS | Merit verdict rests with Owner election decision |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Assurance | 0 | NO_ITEMS | QA is addressed through commissioning and warranty handover |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Procedure | Procedure | Add a step or verification check requiring DB to submit written confirmation that proposed appliances comply with applicable codes and standards (CEC, NPC, NBC/ABC, CSA) | Specification Standards section lists applicable codes but there is no procedural step requiring the DB to confirm compliance. The note says "DB is responsible for confirming code compliance during design development" but this is not captured as a formal verification gate in Procedure. | Specification.md; Procedure.md | Specification#Standards; Procedure#Verification | -- | Procedure.md | TBD |
| D-002 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add guidance suggesting the Owner may wish to compare option pricing against independent appliance procurement to validate merit of the DB-supplied option | Guidance P1 emphasizes transparency so the Owner can "compare it against independent procurement," but no guidance or procedure step actually facilitates this comparison. The merit realization of the option depends on the Owner having a benchmark. | Guidance.md | Principles#P1 | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Imperative | 0 | NO_ITEMS | Foundational imperatives (OSR, OBJ-010) are well-established |
| X:guiding:sufficiency | guiding | sufficiency | Guided Sufficiency | 0 | NO_ITEMS | Guidance provides sufficient direction |
| X:guiding:completeness | guiding | completeness | Exhaustive Guided Scope | 1 | HAS_ITEMS | Guidance does not address disposal of packaging/shipping materials |
| X:guiding:consistency | guiding | consistency | Principled Governance | 0 | NO_ITEMS | Governance principles are consistently applied |
| X:applying:necessity | applying | necessity | Mandated Prerequisite Action | 1 | HAS_ITEMS | Owner election mechanism not specified as formal prerequisite |
| X:applying:sufficiency | applying | sufficiency | Proven Practical Competence | 0 | NO_ITEMS | Practical steps are sufficient |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | No step for appliance protection during remaining construction |
| X:applying:consistency | applying | consistency | Consistent Disciplined Practice | 0 | NO_ITEMS | Practice is consistent between proposal and implementation phases |
| X:judging:necessity | judging | necessity | Decisive Compliance Finding | 0 | NO_ITEMS | Compliance findings are addressable through verification table |
| X:judging:sufficiency | judging | sufficiency | Demonstrated Sufficiency Ruling | 0 | NO_ITEMS | Sufficiency demonstration is adequate |
| X:judging:completeness | judging | completeness | Exhaustive Determination | 0 | NO_ITEMS | Determination scope is proportionate to deliverable |
| X:judging:consistency | judging | consistency | Principled Uniform Ruling | 0 | NO_ITEMS | Ruling criteria are uniform |
| X:reviewing:necessity | reviewing | necessity | Mandatory Foundational Scrutiny | 1 | HAS_ITEMS | No review gate for Owner approval of basis-of-design selections |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Sufficiency Assurance | 0 | NO_ITEMS | Assurance mechanisms are adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Review | 0 | NO_ITEMS | Review scope is proportionate |
| X:reviewing:consistency | reviewing | consistency | Aligned Integrity Assurance | 0 | NO_ITEMS | Integrity assurance is aligned |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add consideration addressing site logistics for appliance delivery (e.g., timing relative to construction, protection of installed appliances, disposal of packaging) | Guidance covers pricing, code compliance, and integration with base design but does not address practical delivery logistics. For a construction site, appliance delivery timing relative to interior finishing is a material coordination concern. | Guidance.md | Considerations | -- | Guidance.md | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add requirement specifying the formal mechanism for Owner election of this option (e.g., written notice, election deadline relative to contract milestones) | REQ-05-06-007 states "The Owner retains the right to elect or decline this option" but does not specify how or when election must occur. Procedure Step B1 references "Owner's written election" but there is no corresponding Specification requirement establishing the election mechanism. | Specification.md; Procedure.md | Specification#REQ-05-06-007; Procedure#Prerequisites for Implementation | -- | Specification.md | TBD |
| X-003 | X:applying:completeness | MissingSlot | Procedure | Procedure | Add step in Part B addressing protection of installed appliances during remaining construction (e.g., protective covers, access restrictions until substantial performance) | Procedure Part B covers installation and commissioning but does not address protecting installed appliances if construction activities continue after appliance installation. Appliances installed before substantial performance could be damaged by ongoing trades. | Procedure.md | Steps#Part B | -- | Procedure.md | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add verification checkpoint for Owner review and approval of proposed basis-of-design appliance selections before final procurement | Procedure Step B1 mentions Owner may request substitutions, and Step A2 selects basis-of-design appliances, but there is no formal Owner review/approval gate between proposal and procurement. If the Owner has not reviewed the specific selections, procurement may proceed on unapproved choices. | Procedure.md | Steps#Step A2; Steps#Step B1 | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Compliance Foundation | 0 | NO_ITEMS | Binding compliance foundation is established by OSR and REQ items |
| E:normative:sufficiency | normative | sufficiency | Guaranteed Compliance Adequacy | 1 | HAS_ITEMS | Adequacy not guaranteed due to assumption-laden Standards section |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Assurance | 0 | NO_ITEMS | Coverage gaps addressed under Matrices A and C items |
| E:normative:consistency | normative | consistency | Invariant Regulatory Alignment | 0 | NO_ITEMS | Regulatory alignment is consistent where established |
| E:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Operational readiness is addressed through prerequisites |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Competence | 0 | NO_ITEMS | Competence demonstration is adequate |
| E:operative:completeness | operative | completeness | Exhaustive Operational Coverage | 0 | NO_ITEMS | Coverage is proportionate to scope |
| E:operative:consistency | operative | consistency | Disciplined Operational Integrity | 0 | NO_ITEMS | Operational integrity is maintained |
| E:evaluative:necessity | evaluative | necessity | Foundational Merit Imperative | 0 | NO_ITEMS | Merit imperative is grounded in OBJ-010 |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Adequacy | 0 | NO_ITEMS | Merit adequacy is substantiated through transparency |
| E:evaluative:completeness | evaluative | completeness | Holistic Quality Determination | 1 | HAS_ITEMS | No holistic quality metric across all appliance categories |
| E:evaluative:consistency | evaluative | consistency | Enduring Value Integrity | 0 | NO_ITEMS | Value integrity is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Multi | Multi | Standardize the term "residential-grade" across documents: Datasheet uses "Residential or commercial-grade," Specification uses "residential-grade" implicitly, Guidance P4 explicitly states "Residential Grade is Acceptable" -- align terminology | Datasheet Attributes table describes refrigerators as "Residential or commercial-grade" while Guidance P4 establishes that residential-grade is the default. This inconsistency in terminology could lead a reader of the Datasheet alone to assume commercial-grade is equally expected. | Datasheet.md; Guidance.md | Datasheet#Attributes; Guidance#P4 | -- | Guidance.md; Datasheet.md | TBD |
| E-002 | E:evaluative:completeness | WeakStatement | Specification | Specification | Add requirement or guidance for DB to propose a quality rating or grading system for the appliance option (e.g., ENERGY STAR rating, expected appliance lifespan) to enable holistic quality assessment | No document provides a holistic quality metric for evaluating proposed appliances beyond "residential-grade." The Owner has no basis for comparing one DB proposal's appliance quality against another. A minimum quality benchmark (e.g., ENERGY STAR certification, minimum warranty years) would strengthen the evaluation framework. | Specification.md | Requirements | -- | Specification.md | TBD |
