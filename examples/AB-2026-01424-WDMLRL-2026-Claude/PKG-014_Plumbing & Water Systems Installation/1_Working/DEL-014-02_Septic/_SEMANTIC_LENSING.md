# Semantic Lensing Register: DEL-014-02 Septic System

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-02_Septic
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-02_Septic/_CONTEXT.md § Deliverable Overview
- _STATUS.md — DEL-014-02_Septic/_STATUS.md § Current Status (SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-02_Septic/_SEMANTIC.md § Matrices A, B, C, F, D, X, E
- Datasheet.md — DEL-014-02_Septic/Datasheet.md § Identification, Attributes, Conditions, Construction
- Specification.md — DEL-014-02_Septic/Specification.md § Scope, Requirements, Standards, Verification
- Guidance.md — DEL-014-02_Septic/Guidance.md § Purpose, Principles, Considerations, Trade-offs
- Procedure.md — DEL-014-02_Septic/Procedure.md § Prerequisites, Steps, Verification, Records
- _REFERENCES.md — DEL-014-02_Septic/_REFERENCES.md § Primary References, Related Deliverables

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document (AppliesToDoc):
  - Datasheet: 4
  - Specification: 12
  - Guidance: 6
  - Procedure: 5
  - Multi: 1
- By matrix:
  - A: 5  B: 5  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 9
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Incomplete code editions in Standards |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Tank material spec TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ identity not specified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection and audit provisions are present and consistent |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Excavation safety standard not cited |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit provisions are present via inspection logs |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Pump-out frequency/cost rationale missing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Value determinations deferred to engineer appropriately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Specify the exact editions of the Alberta Safety Codes Act, Alberta Plumbing Code, and Alberta Environmental Protection and Enhancement Act that govern this work, or add a mechanism for the Plumbing Engineer of Record to confirm editions | Standards section lists codes as "ASSUMPTION: likely applicable; specific edition TBD" — this leaves prescriptive direction incomplete and could affect compliance determination | Specification.md | § Standards | — | PROPOSAL: Plumbing Engineer of Record to confirm | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Specification | Confirm tank material specification (fiberglass, polyethylene, or concrete) once DEL-006-05 design is complete; add as a requirement in Specification | Tank Material / Specification is TBD in Datasheet Construction table; mandatory practice cannot be applied without a specified material | Datasheet.md | § Construction — Tank Material / Specification | — | PROPOSAL: DEL-006-05 Plumbing Engineer of Record | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Identify the specific Authority Having Jurisdiction (AHJ) for plumbing/septic code compliance at this site (e.g., Camrose County Safety Codes Officer, Alberta Municipal Affairs) | Compliance determination requires knowing who the AHJ is; Specification references "AHJ" without identifying the specific authority for this jurisdiction | Specification.md | § Requirements REQ-014-02-05, § Verification | — | PROPOSAL: Owner/County to confirm AHJ identity | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add reference to applicable Alberta OH&S excavation safety requirements (e.g., Alberta OHS Code Part 32 — Excavating) in Step 2.2 and Step 3.1 | Procedure Step 2.2 mentions "applicable OH&S requirements" for excavation but does not cite the specific standard; practical execution requires an identifiable safety reference | Procedure.md | § Steps — Step 2.2, Step 3.1 | — | PROPOSAL: Plumbing Contractor safety officer to confirm | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add a note on expected pump-out frequency and approximate cost implications for a 2,000 US gal holding tank at a maintenance shop facility, to support value orientation for the Owner | Guidance discusses pump-out access but does not address expected pump-out frequency or lifecycle cost, which affects the Owner's understanding of ongoing operational commitment | Guidance.md | § Considerations — Pump-Out Access | — | PROPOSAL: Plumbing Engineer of Record or Owner operations staff | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Foundation/bedding data TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Existing tank characterization incomplete |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet records are comprehensive for available information |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Metric conversion notation inconsistency |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Electrical interface signal missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents for identified scope |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive where information exists |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding is present for core scope items |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements deferred to engineer appropriately |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery deferred to licensed professionals per design-build |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Winterization / frost protection discernment gap |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are appropriately flagged as TBD or ASSUMPTION |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight present in Guidance trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record foundation/bedding requirements once geotechnical investigation is complete; essential factual data for installation | Foundation / Bedding Requirements are listed as "TBD (pending geotechnical investigation and plumbing design)" — this is an essential fact required before installation can proceed | Datasheet.md | § Construction — Foundation / Bedding Requirements | — | PROPOSAL: Geotechnical Engineer + DEL-006-05 | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add attributes for the existing septic tank being removed: approximate size, material, location coordinates, current service status, and known contents — to constitute adequate evidence for removal planning | Existing tank is scoped for removal but Datasheet only records "Remove (demolition/removal in scope)"; no characterization data exists for demolition planning and disposal compliance | Datasheet.md | § Attributes — Existing Tank | — | PROPOSAL: Owner/site records or pre-construction survey | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Multi | Standardize unit convention: use either "US gallon" or "US gal" consistently across all documents; currently both forms appear | Datasheet uses "2,000 US gallon" and "2,000 US gal" in different rows; Specification uses "2,000 US gallons" and "2,000 US gal" — reliable measurement requires consistent notation | Datasheet.md, Specification.md | Datasheet § Attributes, § Construction; Specification § Scope, § Requirements, § Verification | — | PROPOSAL: Adopt "US gal" as abbreviation throughout | TBD |
| B-004 | B:information:necessity | TBD_Question | Datasheet | Specification | Confirm whether electrical connections (alarm, pump-out indicator, level sensor) are required and, if so, add as a requirement in Specification with coordination reference to PKG-015 | Datasheet lists "Electrical Connections" as TBD; Specification excludes electrical alarm/monitoring from scope but Guidance ASSUMPTION suggests it may be code-required — the essential signal about this interface is unresolved | Datasheet.md, Specification.md, Guidance.md | Datasheet § Construction — Electrical Connections; Specification § Scope — Excludes; Guidance § Considerations — Alarm / Monitoring | — | PROPOSAL: Plumbing Engineer of Record + PKG-015 Electrical | TBD |
| B-005 | B:wisdom:necessity | MissingSlot | Guidance | Guidance | Add a consideration for winterization and frost protection requirements specific to central Alberta climate, referencing the geotechnical report and applicable code requirements for buried tank insulation or depth | Guidance notes frost depth ASSUMPTION (>1.5 m) but no corresponding requirement or consideration for winterization measures (insulation, heat trace, minimum burial depth) appears in Specification or Procedure — essential discernment for a holding tank in a cold climate | Guidance.md | § Considerations — Site Conditions | — | PROPOSAL: Plumbing Engineer of Record + geotechnical report | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Mandate | 1 | HAS_ITEMS | Disposal regulation mandate incomplete |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Compliance | 0 | NO_ITEMS | Compliance demonstration provisions adequate in Specification |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Environmental regulation gap |
| C:normative:consistency | normative | consistency | Harmonized Governance | 0 | NO_ITEMS | Governance references are consistent across documents |
| C:operative:necessity | operative | necessity | Operational Threshold | 0 | NO_ITEMS | Operational thresholds met via prerequisites table |
| C:operative:sufficiency | operative | sufficiency | Practical Competence | 0 | NO_ITEMS | Practical competence provisions adequate |
| C:operative:completeness | operative | completeness | Complete Implementation | 0 | NO_ITEMS | Implementation steps are complete for known scope |
| C:operative:consistency | operative | consistency | Disciplined Uniformity | 0 | NO_ITEMS | Procedural consistency is maintained |
| C:evaluative:necessity | evaluative | necessity | Inherent Merit | 0 | NO_ITEMS | Inherent merit addressed via OBJ-001, OBJ-004 linkage |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Valuation | 0 | NO_ITEMS | Valuation deferred to design-build process appropriately |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal | 1 | HAS_ITEMS | Lifecycle/maintenance appraisal missing |
| C:evaluative:consistency | evaluative | consistency | Principled Consistency | 0 | NO_ITEMS | Value principles are consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-014-02-03 to explicitly cite the applicable Alberta regulation governing septic tank decommissioning and disposal (e.g., EPEA, Waste Control Regulation), rather than using "applicable regulations" | REQ-014-02-03 requires removal "in accordance with applicable regulations" — but does not identify which regulations; an enforceable mandate requires specificity for the contractor to comply | Specification.md | § Requirements — REQ-014-02-03 | — | PROPOSAL: Environmental consultant or County regulatory liaison | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add a verification entry for environmental/regulatory compliance of existing tank disposal (disposal documentation is listed in Documentation but has no corresponding verification approach in the Verification table) | The Verification table maps all REQ items but does not explicitly verify that disposal complies with environmental regulations; full regulatory coverage requires a verification mechanism for disposal compliance | Specification.md | § Verification (no row for environmental disposal compliance) | — | PROPOSAL: Add verification row referencing disposal documentation and regulatory sign-off | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a lifecycle/maintenance consideration section covering: expected tank service life, manufacturer warranty vs. project warranty, periodic inspection requirements, and long-term pump-out contract implications | Comprehensive appraisal of the septic system's value should include lifecycle considerations; Guidance covers installation trade-offs but not the long-term operational and maintenance picture | Guidance.md | § Considerations (no lifecycle subsection) | — | PROPOSAL: Plumbing Engineer of Record + Owner operations | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Statutory Foundation | 1 | HAS_ITEMS | Missing statutory reference for septic holding tanks |
| F:normative:sufficiency | normative | sufficiency | Warranted Conformance | 0 | NO_ITEMS | Conformance provisions are warranted where applicable |
| F:normative:completeness | normative | completeness | Total Compliance Scope | 1 | HAS_ITEMS | Backfill compaction standard not specified |
| F:normative:consistency | normative | consistency | Coherent Regulatory Alignment | 0 | NO_ITEMS | Regulatory references are aligned across documents |
| F:operative:necessity | operative | necessity | Execution Readiness | 1 | HAS_ITEMS | Missing hold/witness point definition |
| F:operative:sufficiency | operative | sufficiency | Verified Capability | 0 | NO_ITEMS | Capability verification is addressed via submittals |
| F:operative:completeness | operative | completeness | Total Delivery Mastery | 0 | NO_ITEMS | Delivery steps are complete for known scope |
| F:operative:consistency | operative | consistency | Sustained Reliability | 0 | NO_ITEMS | Reliability provisions are consistent |
| F:evaluative:necessity | evaluative | necessity | Foundational Worth | 0 | NO_ITEMS | Foundational worth tied to OBJ-001, OBJ-004 |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Assessment | 0 | NO_ITEMS | Assessment justification is adequate |
| F:evaluative:completeness | evaluative | completeness | Holistic Value Account | 1 | HAS_ITEMS | No as-built deliverable requirement |
| F:evaluative:consistency | evaluative | consistency | Coherent Value Standard | 0 | NO_ITEMS | Value standards are coherently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add reference to the specific Alberta regulation governing private sewage disposal systems (e.g., Alberta Private Sewage Systems Standard of Practice, or municipal equivalent) as a statutory foundation for holding tank installations | The Standards table references broad acts but not the specific standard of practice for private sewage/septic systems; statutory foundation for a holding tank installation needs this specific reference | Specification.md | § Standards | — | PROPOSAL: Plumbing Engineer of Record or municipal authority | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add a requirement and verification approach for backfill and compaction testing around the new tank (e.g., compaction density test or engineer inspection) | Specification scope includes "bedding, backfill, and surface restoration" but no specific requirement or verification for compaction quality; total compliance scope requires verifiable earthwork standards | Specification.md | § Scope — includes; § Verification (no backfill entry) | — | PROPOSAL: Geotechnical Engineer + DEL-006-05 | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Define mandatory hold points and witness points in the Procedure (e.g., hold point before backfill for tank inspection, witness point for leak test) with explicit County representative notification requirements | Procedure references County representative presence at inspections but does not define formal hold/witness points; execution readiness requires knowing which steps cannot proceed without authorization | Procedure.md | § Steps (no hold/witness point designations) | — | PROPOSAL: Owner/County project representative | TBD |
| F-004 | F:evaluative:completeness | VerificationGap | Specification | Specification | Clarify whether as-built drawings / record drawings are required (Procedure Step 6.1 lists them as "if required by contract") and, if so, add as a formal documentation requirement in Specification | Procedure references as-built mark-ups conditionally; Specification Documentation table does not include as-built drawings — holistic value accounting requires clarity on whether this record is required | Specification.md, Procedure.md | Specification § Documentation; Procedure § Steps — Step 6.1 | — | PROPOSAL: Contract administrator to confirm CCDC 14 requirements | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority established via RFP and SOW references |
| D:normative:applying | normative | applying | Definitive Compliance Practice | 1 | HAS_ITEMS | Connection details TBD |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance rulings tied to AHJ sign-off |
| D:normative:reviewing | normative | reviewing | Settled Oversight Assurance | 0 | NO_ITEMS | Oversight assurance settled via inspection provisions |
| D:operative:guiding | operative | guiding | Confirmed Procedural Plan | 1 | HAS_ITEMS | Service continuity gap |
| D:operative:applying | operative | applying | Proven Work Effectiveness | 0 | NO_ITEMS | Work effectiveness provisions are adequate |
| D:operative:judging | operative | judging | Resolved Performance Verdict | 0 | NO_ITEMS | Performance verdicts tied to verification table |
| D:operative:reviewing | operative | reviewing | Verified Process Integrity | 0 | NO_ITEMS | Process integrity addressed via inspection records |
| D:evaluative:guiding | evaluative | guiding | Anchored Value Priority | 0 | NO_ITEMS | Value priorities anchored to OBJ-001, OBJ-004 |
| D:evaluative:applying | evaluative | applying | Resolved Merit Application | 0 | NO_ITEMS | Merit application resolved through trade-offs |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 1 | HAS_ITEMS | Relocation decision provenance |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Benchmark | 0 | NO_ITEMS | Quality benchmarks confirmed through verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-014-02-04 by specifying minimum pipe slope, connection method, and acceptance test — currently defers entirely to "IFC plumbing drawings" with connection details "TBD" | Definitive compliance practice for wastewater connection cannot be achieved when the requirement defers all details to a design document not yet produced; at minimum, specify the acceptance criterion (e.g., leak test method and duration) | Specification.md | § Requirements — REQ-014-02-04 | — | PROPOSAL: DEL-006-05 design completion | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Guidance | Add a step or prerequisite addressing service continuity during the transition from existing to new septic system — Guidance Principle 2 mentions avoiding "service interruption during construction" but Procedure does not include a continuity plan step | Confirmed procedural plan should address how facility wastewater is managed between existing tank decommissioning and new tank commissioning; this is mentioned in Guidance but absent from Procedure | Procedure.md, Guidance.md | Procedure § Steps (no continuity step); Guidance § Principles — Principle 2 | — | PROPOSAL: Plumbing Contractor + Owner operations | TBD |
| D-003 | D:evaluative:judging | Conflict | Guidance | Guidance | RFP §3.4 text includes "(potentially removal and relocate existing septic tank)" suggesting relocation was considered; D-002 resolves as removal-only — CON-014-02-01 in Guidance flags this but HumanRuling remains TBD; this conflict should be tracked as a lensing finding requiring resolution before installation | The definitive worth judgment on scope (remove vs. relocate) depends on resolving this conflict; Guidance Conflict Table CON-014-02-01 correctly surfaces it but it remains unresolved | Guidance.md | § Conflict Table — CON-014-02-01 | Guidance.md#Conflict Table (RFP §3.4 vs. D-002/SOW-0043) | PROPOSAL: Accept D-002 per Guidance recommendation | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Steering Basis | 0 | NO_ITEMS | Steering basis grounded in RFP and decomposition |
| X:guiding:sufficiency | guiding | sufficiency | Justified Guidance Frame | 1 | HAS_ITEMS | Guidance examples section empty |
| X:guiding:completeness | guiding | completeness | Thorough Directive Record | 0 | NO_ITEMS | Directive records are thorough |
| X:guiding:consistency | guiding | consistency | Harmonized Steering Standard | 0 | NO_ITEMS | Steering standards are harmonized |
| X:applying:necessity | applying | necessity | Mandated Performance Basis | 1 | HAS_ITEMS | Tank installation depth not specified |
| X:applying:sufficiency | applying | sufficiency | Sufficient Delivery Proof | 0 | NO_ITEMS | Delivery proof provisions are sufficient |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Account | 0 | NO_ITEMS | Delivery account is exhaustive for known scope |
| X:applying:consistency | applying | consistency | Steady Conformance Tracking | 1 | HAS_ITEMS | Verification numbering gap |
| X:judging:necessity | judging | necessity | Binding Readiness Verdict | 0 | NO_ITEMS | Readiness verdicts are bound to prerequisites |
| X:judging:sufficiency | judging | sufficiency | Justified Performance Proof | 1 | HAS_ITEMS | Leak test criteria not specified |
| X:judging:completeness | judging | completeness | Comprehensive Verdict Record | 0 | NO_ITEMS | Verdict records are comprehensive |
| X:judging:consistency | judging | consistency | Reliable Verdict Standard | 0 | NO_ITEMS | Verdict standards are reliable |
| X:reviewing:necessity | reviewing | necessity | Authenticated Oversight Basis | 0 | NO_ITEMS | Oversight basis authenticated via AHJ references |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Oversight Scope | 1 | HAS_ITEMS | Warranty verification incomplete |
| X:reviewing:completeness | reviewing | completeness | Thorough Oversight Account | 0 | NO_ITEMS | Oversight account is thorough |
| X:reviewing:consistency | reviewing | consistency | Reliable Oversight Tracking | 0 | NO_ITEMS | Oversight tracking is reliable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Guidance | Guidance | Populate the Examples section with at least one reference example of a comparable rural Alberta holding tank installation, or explicitly note that examples will be added during design development | Guidance Examples section states "TBD — no project-specific examples are available"; a justified guidance frame benefits from precedent even if only referenced generically | Guidance.md | § Examples | — | PROPOSAL: Plumbing Engineer of Record | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Add a requirement for minimum tank burial depth or reference to frost protection requirements (per geotechnical report and Alberta code) to ensure mandated performance basis for installation in cold climate | No requirement specifies minimum installation depth or frost protection; Guidance notes frost depth concern but Specification has no corresponding requirement — mandated performance basis needs this for a buried tank in central Alberta | Specification.md, Guidance.md | Specification § Requirements (no depth requirement); Guidance § Considerations — Site Conditions | — | PROPOSAL: Geotechnical report + Plumbing Engineer of Record | TBD |
| X-003 | X:applying:consistency | Normalization | Specification | Specification | Align the Specification Verification table requirement labels with the formal REQ IDs (e.g., use "REQ-014-02-01: Tank Supply and Capacity" consistently rather than abbreviated forms) for steady conformance tracking | Specification Verification table uses shortened labels (e.g., "Tank capacity") that do not exactly match the formal requirement headings; this could cause tracking drift in audit | Specification.md | § Verification | — | PROPOSAL: Editorial alignment during enrichment | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Specify leak/pressure test parameters: test method (hydrostatic vs. air), test pressure, hold duration, and pass/fail criteria — currently stated as "Pressure/leak test or equivalent per applicable code" | Justified performance proof for wastewater connection (REQ-014-02-04) requires defined test parameters; current verification approach defers entirely to "applicable code" without specifying acceptance criteria | Specification.md | § Verification — REQ-014-02-04; § Requirements — REQ-014-02-04 | — | PROPOSAL: Plumbing Engineer of Record to specify per code | TBD |
| X-005 | X:reviewing:sufficiency | VerificationGap | Specification | Specification | Add verification mechanism for warranty period enforcement (e.g., warranty start date documentation, deficiency notification process during warranty period) beyond CCC issuance and warranty document submission | REQ-014-02-08 verification is "CCC issuance; warranty documentation submitted at project closeout" — but justified oversight scope should include a mechanism for warranty enforcement during the 2-year period, not just document submission | Specification.md | § Requirements — REQ-014-02-08; § Verification — REQ-014-02-08 | — | PROPOSAL: Contract administrator per CCDC 14 warranty provisions | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative with source citations |
| E:guiding:information | guiding | information | Clear Directive Context | 0 | NO_ITEMS | Directive context is clear |
| E:guiding:knowledge | guiding | knowledge | Proficient Directive Mastery | 0 | NO_ITEMS | Directive mastery demonstrated by engineer deferral pattern |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Vision | 1 | HAS_ITEMS | Sustainability/environmental stewardship gap |
| E:applying:data | applying | data | Verified Delivery Evidence | 1 | HAS_ITEMS | Photo documentation not specified |
| E:applying:information | applying | information | Contextual Delivery Signal | 0 | NO_ITEMS | Delivery signals are contextually adequate |
| E:applying:knowledge | applying | knowledge | Proficient Execution Capacity | 0 | NO_ITEMS | Execution capacity addressed via licensed contractor requirement |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment appropriately deferred to professionals |
| E:judging:data | judging | data | Definitive Judgment Evidence | 0 | NO_ITEMS | Judgment evidence tied to inspection reports and test records |
| E:judging:information | judging | information | Unambiguous Verdict Context | 0 | NO_ITEMS | Verdict context is unambiguous |
| E:judging:knowledge | judging | knowledge | Proficient Verdict Mastery | 0 | NO_ITEMS | Verdict mastery tied to AHJ and professional sign-off |
| E:judging:wisdom | judging | wisdom | Principled Verdict Foresight | 0 | NO_ITEMS | Verdict foresight present in conflict table and TBD flagging |
| E:reviewing:data | reviewing | data | Authenticated Inspection Record | 1 | HAS_ITEMS | Inspection record authentication gap |
| E:reviewing:information | reviewing | information | Clear Oversight Context | 0 | NO_ITEMS | Oversight context is clear |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Inspection Mastery | 0 | NO_ITEMS | Inspection mastery tied to qualified inspector requirement |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Oversight foresight addressed through warranty and closeout provisions |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add a consideration for environmental stewardship beyond regulatory compliance: e.g., groundwater protection measures during existing tank removal, spill containment during pump-out, and site restoration quality expectations | Principled leadership vision for a septic installation at a landfill site should address environmental stewardship explicitly; Guidance covers regulatory compliance but not the broader environmental ethic appropriate for a County-owned landfill property | Guidance.md | § Considerations — Environmental and Regulatory | — | PROPOSAL: Owner/County environmental policy | TBD |
| E-002 | E:applying:data | MissingSlot | Procedure | Procedure | Add a requirement for photographic documentation at key milestones (e.g., open excavation before backfill, existing tank condition before removal, new tank placement before backfill, completed connections) as verified delivery evidence | No provision for photographic records exists in Procedure or Specification; photo documentation at concealed-work stages provides critical verified delivery evidence for buried infrastructure | Procedure.md | § Records (no photo documentation entry) | — | PROPOSAL: Standard construction practice; add to Records table | TBD |
| E-003 | E:reviewing:data | Normalization | Procedure | Procedure | Standardize the Records table to include a column for "Format/Medium" and "Retention Period" to ensure authenticated inspection records meet long-term archival requirements | Procedure Records table lists records and responsible parties but does not specify format (digital/paper), retention period, or archival requirements — authenticated inspection records require these attributes for long-term traceability | Procedure.md | § Records | — | PROPOSAL: Contract administrator per CCDC 14 and County records policy | TBD |
