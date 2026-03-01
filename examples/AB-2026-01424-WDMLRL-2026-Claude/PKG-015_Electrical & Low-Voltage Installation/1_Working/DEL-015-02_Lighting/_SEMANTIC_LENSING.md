# Semantic Lensing Register: DEL-015-02 Lighting Installation

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-015_Electrical & Low-Voltage Installation/1_Working/DEL-015-02_Lighting
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-015-02_Lighting Context, §Deliverable Overview, §Scope of Work
- _STATUS.md — DEL-015-02_Lighting Status, §Current Status (SEMANTIC_READY)
- _SEMANTIC.md — DEL-015-02 Lighting Installation, Matrices A, B, C, F, D, X, E (all parsed)
- Datasheet.md — DEL-015-02 Lighting Installation, §Identification through §References
- Specification.md — DEL-015-02 Lighting Installation, §Scope through §Documentation
- Guidance.md — DEL-015-02 Lighting Installation, §Purpose through §Conflict Table
- Procedure.md — DEL-015-02 Lighting Installation, §Purpose through §Records
- _REFERENCES.md — DEL-015-02_Lighting References (read; scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 12
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 4  F: 5  D: 3  X: 4  E: 3
- By type:
  - Conflict: 3
  - VerificationGap: 5
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Emergency lighting prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Wash Bay fixture spec incomplete |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition not identified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection and audit provisions adequate |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Switching strategy TBD in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps well-covered in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No illuminance-level acceptance criteria |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit provisions adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value rationale addressed in Guidance §Purpose |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit considerations implicit in LED-only rationale |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Warranty and quality provisions present |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add explicit requirement for emergency/exit lighting or record TBD with reference to Alberta Safety Codes Act | Prescriptive direction lens reveals that emergency lighting is neither required nor explicitly excluded; Guidance C-4 and CONF-L-02 flag the ambiguity but no normative requirement exists | Specification.md | §Scope — Out of Scope; §Requirements | — | PROPOSAL: Owner and AHJ to confirm scope inclusion | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify REQ-L-04: specify minimum wattage and lumen output for Wash Bay fixtures, or record TBD with clear trigger for resolution (IFC drawing milestone) | Mandatory practice lens highlights that REQ-L-04 says "TBD" for performance parameters, leaving the requirement unenforceable until resolved | Specification.md | §Requirements — REQ-L-04 | — | PROPOSAL: Electrical Engineer of Record via IFC design | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Identify the specific edition of CSA C22.1 applicable to this installation (e.g., 2024 edition) per the local AHJ | Compliance determination lens reveals that REQ-L-10 references CSA C22.1 but labels the edition as ASSUMPTION/TBD; the applicable edition affects specific clause requirements | Specification.md | §Requirements — REQ-L-10; §Standards | — | PROPOSAL: Confirm with AHJ during permit application | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add procedural step or prerequisite for confirming switching/control strategy before Phase 2 rough-in begins, since REQ-L-14 and all switching references are TBD | Procedural direction lens reveals that Step 7 (Install Switching Devices) depends on IFC switch locations that are TBD, but no hold-point or prerequisite explicitly gates rough-in on switching design completion | Procedure.md | §Steps — Phase 2, Step 7 | — | PROPOSAL: Add hold-point or prerequisite reference | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for maintained illuminance levels (lux/footcandles) by zone, or record TBD pending photometric study | Performance assessment lens reveals no quantitative illuminance acceptance criterion exists in Specification or Procedure; only fixture count and data sheet review are verified. Guidance C-1 notes the photometric study gap. | Specification.md | §Verification; Guidance.md §Considerations — C-1 | — | PROPOSAL: Electrical Engineer to establish per photometric study | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing wattage/lumen data for Z-2 through Z-5 |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available data adequate where specified |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Conduit type, circuit assignments absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Stated measurements consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Controls/switching strategy absent |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context sufficient for stated requirements |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Narrative coverage adequate |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Fixture count discrepancy risk |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Domain understanding evidenced in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise assumptions reasonable |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage adequate for current state |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment present in Guidance trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls appropriately flagged as TBD |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Record TBD: Wattage and lumen output for Z-2, Z-3, Z-4, Z-5 fixtures pending IFC design | Essential fact lens: four of five zones lack fixture performance data; Datasheet notes this but does not assign a resolution path or milestone | Datasheet.md | §Attributes — Lighting Zones and Fixture Schedule | — | PROPOSAL: Electrical Engineer via IFC drawings | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add TBD entries for conduit type, circuit breaker sizes, panel assignments, and circuit count to Datasheet §Construction or a new §Electrical Design Parameters section | Comprehensive record lens: Datasheet §Construction lists conduit type, panel/circuit assignments, and controls as TBD but these are scattered notations rather than a structured register of missing data | Datasheet.md | §Construction | — | PROPOSAL: Populate once IFC drawings are issued | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Guidance | Clarify: Will lighting controls include occupancy sensing, daylight harvesting, or manual switching only? Record as TBD with decision owner and milestone | Essential signal lens: Guidance C-3 acknowledges switching strategy is TBD; Datasheet §Construction confirms "Controls / switching — Not explicitly specified"; Specification REQ-L-14 is TBD. No document assigns a decision owner or resolution milestone | Datasheet.md; Specification.md; Guidance.md | Datasheet §Construction; Specification §Requirements REQ-L-14; Guidance §Considerations C-3 | — | PROPOSAL: Owner to decide; Electrical Engineer to implement in IFC | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize total fixture count: Datasheet states "Total fixture count: 35 (ASSUMPTION: sum of zones above)" while other docs list per-zone counts. Confirm that 20+6+1+2+6=35 is the authoritative total and remove ASSUMPTION tag if confirmed | Coherent message lens: Datasheet labels the total as ASSUMPTION despite it being a simple arithmetic sum of the zone counts. This tagging creates unnecessary uncertainty about whether the total is contested | Datasheet.md; Specification.md | Datasheet §Attributes — total fixture count note | — | PROPOSAL: Confirm sum and remove ASSUMPTION label | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Mandated Compliance Floor | 1 | HAS_ITEMS | Minimum illuminance targets missing |
| C:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Adherence | 1 | HAS_ITEMS | CSA C22.1 clauses not identified |
| C:normative:completeness | normative | completeness | Exhaustive Obligation Scope | 1 | HAS_ITEMS | Emergency lighting scope gap |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Regulatory references consistent where present |
| C:operative:necessity | operative | necessity | Critical Operational Protocol | 0 | NO_ITEMS | Core installation protocol covered |
| C:operative:sufficiency | operative | sufficiency | Verified Competent Delivery | 0 | NO_ITEMS | Delivery verification adequate |
| C:operative:completeness | operative | completeness | Whole Workflow Coverage | 1 | HAS_ITEMS | Ceiling fan coordination step missing |
| C:operative:consistency | operative | consistency | Reliable Method Discipline | 0 | NO_ITEMS | Method discipline consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Value Recognition | 0 | NO_ITEMS | Value recognition present in Guidance §Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Value Judgment | 0 | NO_ITEMS | Value judgments appropriately scoped |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Account | 0 | NO_ITEMS | Value account adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Benchmark | 0 | NO_ITEMS | Valuation consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add minimum maintained illuminance levels (footcandles or lux) by zone as acceptance criteria, or record TBD pending photometric study by EOR | Mandated Compliance Floor lens: the normative minimum for lighting performance is fixture count and data sheet wattage/lumens only; no zone-level illuminance target exists to confirm the installation actually achieves adequate light levels at task height | Specification.md | §Requirements (no illuminance req); §Verification (no illuminance check) | — | PROPOSAL: EOR photometric study to establish targets | TBD |
| C-002 | C:normative:sufficiency | RationaleGap | Specification | Guidance | Add note in Guidance explaining which specific CSA C22.1 sections are expected to apply (e.g., Section 30 for lighting, Section 22 for wiring), or record TBD for EOR to identify during design | Substantiated Regulatory Adherence lens: REQ-L-10 references CSA C22.1 generically but provides no specific section citations; this makes it difficult to verify which code clauses are actually relevant | Specification.md; Guidance.md | Specification §Standards; Guidance — not addressed | — | PROPOSAL: EOR to identify applicable clauses in IFC design package | TBD |
| C-003 | C:normative:completeness | Conflict | Specification | Specification | Resolve whether emergency/exit lighting is in-scope, out-of-scope, or conditionally in-scope. Record the ruling in Specification §Scope | Exhaustive Obligation Scope lens: Specification §Scope Out of Scope lists emergency lighting as "TBD; ASSUMPTION: required under Alberta Safety Codes" while Guidance CONF-L-02 flags the same ambiguity. The scope boundary is unresolved. | Specification.md; Guidance.md | Specification §Scope — Out of Scope; Guidance §Conflict Table CONF-L-02 | Specification.md#Scope (TBD), Guidance.md#Conflict-Table (CONF-L-02) | PROPOSAL: Owner and AHJ to rule | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a coordination step in Procedure Phase 1 or Phase 3 addressing ceiling fan mounting location coordination with Main Shop high-bay fixture layout | Whole Workflow Coverage lens: Guidance C-5 notes that 6 ceiling fans share the Main Shop ceiling with 20 high-bay fixtures and coordination is advisable, and Guidance CONF-L-03 flags the coordination gap; but Procedure contains no step addressing fan coordination | Procedure.md; Guidance.md | Procedure §Steps (entire); Guidance §Considerations C-5; Guidance §Conflict Table CONF-L-03 | — | PROPOSAL: Add coordination checkpoint in Procedure Phase 1 | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Regulatory Threshold | 1 | HAS_ITEMS | NBC illuminance requirements not addressed |
| F:normative:sufficiency | normative | sufficiency | Defensible Conformance Basis | 1 | HAS_ITEMS | No photometric evidence path |
| F:normative:completeness | normative | completeness | Unified Obligation Inventory | 0 | NO_ITEMS | Obligation inventory adequate for declared scope |
| F:normative:consistency | normative | consistency | Coherent Conformance Measure | 0 | NO_ITEMS | Conformance measures consistent |
| F:operative:necessity | operative | necessity | Validated Operational Readiness | 1 | HAS_ITEMS | BOM validation step weak |
| F:operative:sufficiency | operative | sufficiency | Confirmed Execution Capability | 0 | NO_ITEMS | Execution capability provisions adequate |
| F:operative:completeness | operative | completeness | Whole Process Authority | 1 | HAS_ITEMS | Voltage drop compliance mentioned in Guidance only |
| F:operative:consistency | operative | consistency | Stable Performance Rhythm | 0 | NO_ITEMS | Performance rhythm consistent |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Awareness | 0 | NO_ITEMS | Merit awareness present |
| F:evaluative:sufficiency | evaluative | sufficiency | Credible Appraisal Basis | 0 | NO_ITEMS | Appraisal basis adequate |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Appraisal Scope | 1 | HAS_ITEMS | Energy efficiency not addressed |
| F:evaluative:consistency | evaluative | consistency | Enduring Quality Standard | 0 | NO_ITEMS | Quality standard consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Guidance | Guidance | Record TBD: What are the minimum maintained illuminance levels required by the National Building Code of Canada / Alberta Safety Codes for each occupancy type in this facility (industrial workshop, office, wash bay)? | Absolute Regulatory Threshold lens: Guidance C-1 acknowledges that Alberta Safety Codes and NBC prescribe minimum illuminance by occupancy type and that "specific lux/footcandle targets are TBD pending the engineer's photometric study." This threshold is a non-negotiable regulatory datum that remains unresolved. | Guidance.md | §Considerations — C-1 | — | PROPOSAL: EOR to confirm per NBC and applicable standards | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add a verification method for photometric performance (e.g., "EOR photometric analysis report demonstrating minimum illuminance per zone") to the Verification table | Defensible Conformance Basis lens: the Specification verification table checks fixture count, data sheets, and code inspection, but includes no method to verify that the installed system actually delivers adequate illuminance at task height — the conformance basis is incomplete | Specification.md | §Verification | — | PROPOSAL: EOR photometric study as verification artifact | TBD |
| F-003 | F:operative:necessity | WeakStatement | Procedure | Procedure | Strengthen Prerequisite P-7: specify that BOM shall be verified against IFC drawing fixture schedule and approved submittal quantities, not just "verified against the BOM" | Validated Operational Readiness lens: P-7 says materials are "verified against the BOM" but the BOM itself is an ASSUMPTION — there is no reference to verifying the BOM against the IFC fixture schedule, creating a circular reference | Procedure.md | §Prerequisites — P-7 | — | PROPOSAL: Reference IFC fixture schedule as BOM source | TBD |
| F-004 | F:operative:completeness | RationaleGap | Guidance | Guidance | Add rationale in Guidance for voltage drop compliance: explain why it matters (fixture performance, code compliance) and what the acceptable limit is (typically 3% branch, 5% total per CSA C22.1) | Whole Process Authority lens: Guidance C-2 mentions that "circuit lengths are appropriate for voltage drop compliance" but provides no explanation of applicable limits or why this matters. Specification has no corresponding requirement. | Guidance.md | §Considerations — C-2 | — | PROPOSAL: EOR to confirm voltage drop limits in IFC design | TBD |
| F-005 | F:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration noting energy efficiency targets or energy code requirements (e.g., NECB lighting power density limits) if applicable to this facility | Exhaustive Appraisal Scope lens: Guidance discusses LED rationale (P-3) but does not address whether the National Energy Code for Buildings (NECB) or Alberta energy code applies and whether lighting power density limits must be met | Guidance.md | §Principles — P-3 (LED rationale only); entire document scanned | — | PROPOSAL: Confirm NECB applicability with EOR | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Governance Bound | 0 | NO_ITEMS | Governance bounds established |
| D:normative:applying | normative | applying | Compulsory Compliance Execution | 1 | HAS_ITEMS | Mounting method unresolved |
| D:normative:judging | normative | judging | Resolved Conformance Ruling | 0 | NO_ITEMS | Conformance rulings deferred appropriately to AHJ |
| D:normative:reviewing | normative | reviewing | Mandated Conformance Review | 0 | NO_ITEMS | Review provisions adequate |
| D:operative:guiding | operative | guiding | Assured Process Stewardship | 0 | NO_ITEMS | Process stewardship adequate |
| D:operative:applying | operative | applying | Resolved Delivery Capability | 1 | HAS_ITEMS | Elevated access equipment not specified |
| D:operative:judging | operative | judging | Resolved Productivity Verdict | 0 | NO_ITEMS | Productivity assessment adequate |
| D:operative:reviewing | operative | reviewing | Systematic Cadence Verification | 0 | NO_ITEMS | Cadence verification adequate |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Stewardship | 0 | NO_ITEMS | Merit stewardship present |
| D:evaluative:applying | evaluative | applying | Confirmed Value Realization | 0 | NO_ITEMS | Value realization provisions adequate |
| D:evaluative:judging | evaluative | judging | Resolved Merit Finding | 0 | NO_ITEMS | Merit finding provisions adequate |
| D:evaluative:reviewing | evaluative | reviewing | Settled Standard Scrutiny | 1 | HAS_ITEMS | Warranty scope incomplete |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Datasheet | Datasheet | Clarify mounting method: specify whether pendant, chain, or aircraft cable mount is required for Main Shop and Wash Bay, or record TBD with resolution milestone tied to IFC drawings | Compulsory Compliance Execution lens: Datasheet §Construction says "Mounting method — Pendant, surface, or chain mount as appropriate to ceiling height and zone — TBD per final electrical design." This leaves three options unresolved, which affects procurement and installation planning. | Datasheet.md | §Construction — Mounting method | — | PROPOSAL: EOR to specify in IFC drawings | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Specify in P-8 or Step 8a: minimum platform height and type of elevated access equipment required for 35-foot ceiling installation (e.g., articulating boom lift rated to 40 ft) | Resolved Delivery Capability lens: Procedure P-8 says "Appropriate elevated access equipment (aerial work platform or scaffolding) is available" but does not specify the required reach height or equipment type for a 35-foot ceiling. This could lead to inadequate equipment being mobilized. | Procedure.md | §Prerequisites — P-8; §Steps — Step 8a | — | PROPOSAL: Electrical Contractor to confirm equipment specification | TBD |
| D-003 | D:evaluative:reviewing | VerificationGap | Specification | Specification | Add verification criterion for fixture manufacturer warranty duration (e.g., minimum manufacturer warranty of X years) distinct from the contractor 2-year warranty | Settled Standard Scrutiny lens: REQ-L-13 and the verification table address the contractor's 2-year warranty but do not address the manufacturer's product warranty for LED fixtures. LED fixture manufacturer warranties often exceed 5 years and are a separate quality assurance element. | Specification.md | §Requirements — REQ-L-13; §Verification — V-10 | — | PROPOSAL: Specify minimum manufacturer warranty in Specification | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Governance Signal | 0 | NO_ITEMS | Governance signals adequate |
| X:guiding:sufficiency | guiding | sufficiency | Validated Stewardship Scope | 1 | HAS_ITEMS | Scope boundary for Old North Shop unclear |
| X:guiding:completeness | guiding | completeness | Entire Governance Inventory | 0 | NO_ITEMS | Governance inventory complete |
| X:guiding:consistency | guiding | consistency | Coherent Leadership Metric | 0 | NO_ITEMS | Leadership metrics consistent |
| X:applying:necessity | applying | necessity | Obligatory Capability Proof | 1 | HAS_ITEMS | No commissioning acceptance criteria |
| X:applying:sufficiency | applying | sufficiency | Validated Fulfilment Range | 0 | NO_ITEMS | Fulfilment range adequate |
| X:applying:completeness | applying | completeness | Entire Capability Record | 0 | NO_ITEMS | Capability records addressed in Procedure §Records |
| X:applying:consistency | applying | consistency | Reliable Implementation Gauge | 0 | NO_ITEMS | Implementation measures consistent |
| X:judging:necessity | judging | necessity | Definitive Performance Fact | 1 | HAS_ITEMS | No quantified performance acceptance test |
| X:judging:sufficiency | judging | sufficiency | Substantiated Performance Finding | 0 | NO_ITEMS | Performance findings adequate where specified |
| X:judging:completeness | judging | completeness | Entire Conformance Account | 0 | NO_ITEMS | Conformance account adequate |
| X:judging:consistency | judging | consistency | Reliable Determination Metric | 0 | NO_ITEMS | Determination metrics consistent |
| X:reviewing:necessity | reviewing | necessity | Anchored Oversight Awareness | 0 | NO_ITEMS | Oversight awareness adequate |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Oversight Record | 0 | NO_ITEMS | Oversight records addressed |
| X:reviewing:completeness | reviewing | completeness | Entire Oversight Register | 1 | HAS_ITEMS | Owner inspection hold-points not explicit |
| X:reviewing:consistency | reviewing | consistency | Reliable Audit Cadence | 0 | NO_ITEMS | Audit cadence adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | Conflict | Specification | Specification | Resolve Old North Shop lighting scope: explicitly confirm exclusion or inclusion in Specification §Scope with reference to IFC drawings as the trigger | Validated Stewardship Scope lens: Specification §Scope Out of Scope says "Old North Shop lighting (unless explicitly included in issued construction drawings — TBD)." This conditional exclusion creates scope ambiguity — if the IFC drawings include it, the scope changes without a formal change order. | Specification.md | §Scope — Out of Scope | Specification.md#Scope (conditional exclusion), _CONTEXT.md (no mention of Old North Shop) | PROPOSAL: Owner to confirm scope exclusion | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add a commissioning acceptance criterion (e.g., all fixtures operational, all switches functional, no fault conditions) as a formal verification row in the Verification table distinct from the functional test in Procedure Step 11 | Obligatory Capability Proof lens: Procedure Step 11 describes a functional test (energize and confirm operation), but Specification §Verification has no corresponding "commissioning acceptance" row. The Procedure test is operational but there is no normative acceptance gate. | Specification.md; Procedure.md | Specification §Verification (no commissioning row); Procedure §Steps — Step 11 | — | PROPOSAL: Add commissioning acceptance verification to Specification | TBD |
| X-003 | X:judging:necessity | RationaleGap | Guidance | Guidance | Add rationale explaining why fixture count and data sheet review alone may be insufficient for performance acceptance — specifically the gap between component specification and system performance | Definitive Performance Fact lens: current verification relies on counting fixtures and reviewing data sheets, but no definitive system-level performance fact (measured illuminance) is tested. Guidance should explain the difference between component compliance and system performance. | Guidance.md | entire document scanned; §Considerations C-1 (closest) | — | PROPOSAL: EOR to address in design documentation | TBD |
| X-004 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add explicit owner/inspector hold-points in Procedure (e.g., after Step 4 mark-out, after Step 8 fixture installation, before Step 11 energization) for owner representative inspection | Entire Oversight Register lens: Procedure verification table references "Owner Inspector" as responsible party for multiple checks but the Step sequence does not identify explicit hold-points where the owner inspector must sign off before work proceeds | Procedure.md | §Steps (entire); §Verification — V-1 through V-10 | — | PROPOSAL: Coordinate hold-points with Owner representative | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Record | 0 | NO_ITEMS | Directive records adequate |
| E:guiding:information | guiding | information | Unambiguous Governance Account | 1 | HAS_ITEMS | Ceiling fan governance unclear |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Mastery | 0 | NO_ITEMS | Governance knowledge adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Governance foresight present in Guidance trade-offs |
| E:applying:data | applying | data | Validated Deployment Record | 1 | HAS_ITEMS | Deployment records incomplete for Z-2 through Z-5 |
| E:applying:information | applying | information | Clear Deployment Account | 0 | NO_ITEMS | Deployment account clear where specified |
| E:applying:knowledge | applying | knowledge | Validated Execution Mastery | 0 | NO_ITEMS | Execution knowledge adequate |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment appropriately deferred |
| E:judging:data | judging | data | Decisive Conformance Proof | 0 | NO_ITEMS | Conformance proof provisions adequate |
| E:judging:information | judging | information | Unambiguous Conformance Finding | 0 | NO_ITEMS | Conformance findings unambiguous where present |
| E:judging:knowledge | judging | knowledge | Substantiated Conformance Mastery | 0 | NO_ITEMS | Conformance mastery adequate |
| E:judging:wisdom | judging | wisdom | Principled Conformance Judgment | 0 | NO_ITEMS | Conformance judgment provisions adequate |
| E:reviewing:data | reviewing | data | Complete Oversight Evidence | 1 | HAS_ITEMS | As-built drawing scope unclear |
| E:reviewing:information | reviewing | information | Grounded Oversight Account | 0 | NO_ITEMS | Oversight account adequate |
| E:reviewing:knowledge | reviewing | knowledge | Validated Scrutiny Mastery | 0 | NO_ITEMS | Scrutiny mastery adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Oversight foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | Conflict | Multi | Guidance | Resolve ceiling fan ownership: Guidance CONF-L-03 identifies that ceiling fans are noted in App B-Elec but not assigned to DEL-015-02. Confirm which deliverable owns ceiling fan installation and record the coordination interface. | Unambiguous Governance Account lens: Guidance C-5 and CONF-L-03 identify that 6 ceiling fans share the Main Shop ceiling space but are not assigned to this deliverable. The governance account is ambiguous — no document clearly states who owns the fans or the coordination interface. | Guidance.md; Specification.md | Guidance §Considerations C-5; Guidance §Conflict Table CONF-L-03; Specification §Scope — Out of Scope (fans not mentioned) | Guidance.md#Conflict-Table (CONF-L-03), Specification.md#Scope (silent on fans) | PROPOSAL: Owner/PM to assign fan scope to a deliverable | TBD |
| E-002 | E:applying:data | Normalization | Datasheet | Datasheet | Normalize fixture type nomenclature: use consistent terminology across Datasheet, Specification, and Procedure for the 8-foot fixtures (currently "8-foot LED strip/tube fixture", "8-foot LED fixture", "8-foot LED strip or linear fixture") | Validated Deployment Record lens: the 8-foot fixture type is described with three slightly different names across documents, creating potential confusion about whether these are the same fixture type | Datasheet.md; Specification.md; Procedure.md | Datasheet §Attributes — Fixture Schedule (column "Fixture Type"); Specification §Scope; Procedure §Steps Step 8c-8e | — | PROPOSAL: Standardize to one term and apply across all docs | TBD |
| E-003 | E:reviewing:data | MissingSlot | Specification | Specification | Add as-built drawing requirements to Specification §Documentation: specify scope of as-builts (all five zones, circuit routing, panel schedule), format, and submission deadline | Complete Oversight Evidence lens: Specification §Documentation lists "As-Built Drawings" as a required artifact with description "Redlined or updated drawings reflecting actual installed conditions — ASSUMPTION: standard practice." The scope, format, and deadline of as-builts are not specified, weakening the oversight evidence chain. | Specification.md | §Documentation — Required Artifacts | — | PROPOSAL: Define as-built requirements in Specification | TBD |

---

## Cross-Matrix Observations

The following patterns emerged across multiple matrices and are noted for the enrichment pass:

1. **Illuminance acceptance criteria** (items A-005, C-001, F-001, F-002, X-003): The most prominent gap across the production documents is the absence of quantitative illuminance acceptance criteria. Multiple lenses (normative/judging, normative/necessity, evaluative) converge on this gap. The Guidance acknowledges it (C-1) but no requirement or verification method addresses it.

2. **Emergency lighting scope** (items A-001, C-003): Two lenses independently surface the unresolved emergency lighting scope boundary. This aligns with existing CONF-L-02 in Guidance but remains unresolved in the normative document.

3. **Switching/controls TBD chain** (items A-004, B-003): The switching strategy gap propagates from Datasheet through Specification to Procedure, with no resolution milestone or decision owner assigned in any document.

4. **Ceiling fan coordination** (items C-004, E-001): Two lenses surface the governance and procedural gap for ceiling fan coordination. Guidance flags it but Procedure and Specification do not operationalize the coordination.
