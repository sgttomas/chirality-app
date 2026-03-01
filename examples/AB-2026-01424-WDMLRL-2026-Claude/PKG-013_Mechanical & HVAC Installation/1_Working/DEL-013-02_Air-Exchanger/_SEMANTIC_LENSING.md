# Semantic Lensing Register: DEL-013-02 High-Volume Air Exchanger

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-02_Air-Exchanger/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-013-02_Air-Exchanger/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements, Related Deliverables)
- _STATUS.md — DEL-013-02_Air-Exchanger/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-013-02_Air-Exchanger/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — DEL-013-02_Air-Exchanger/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-013-02_Air-Exchanger/Specification.md (Scope, Requirements REQ-001 through REQ-013, Standards, Verification, Documentation)
- Guidance.md — DEL-013-02_Air-Exchanger/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-013-02_Air-Exchanger/Procedure.md (Prerequisites, Steps Phases 1-5, Verification, Records)
- _REFERENCES.md — DEL-013-02_Air-Exchanger/_REFERENCES.md (Primary References, Related Documentation, Standard References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 11
  - Guidance: 4
  - Procedure: 9
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards applicability gaps |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Cold-climate rating as mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ inspection criteria underspecified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure covers Safety Codes Officer inspection and records adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Ductwork insulation procedural gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps in Procedure are well-sequenced |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Airflow tolerance not confirmed |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table covers process audit adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value orientation clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Objective linkage and value rationale are present |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning report and Owner acceptance provide quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific ASHRAE 62.1 occupancy category and ventilation rate procedure (rate or IAQ procedure) applies to this industrial maintenance shop | Specification REQ-001 references ASHRAE 62.1 but states "applicable occupancy type" without identifying the specific category; this ambiguity could change airflow sizing significantly | Specification.md | REQ-001 | — | PROPOSAL: Mechanical Engineer to identify occupancy category in DEL-003-07 | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add a requirement that the selected HRV/ERV unit shall carry a cold-climate certification or manufacturer rating to a minimum design temperature (e.g., -40C) | Cold-climate operation is mentioned in REQ-011 but without a specific minimum temperature rating or certification standard; for Alberta the unit must function at extreme cold | Specification.md | REQ-011 | — | PROPOSAL: Mechanical Engineer to confirm minimum design temperature | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add explicit acceptance criteria for Safety Codes inspection: what specific items the AHJ will inspect and what constitutes a pass for this deliverable | REQ-009 verification is "Inspection and sign-off by Alberta Safety Codes Officer" but no checklist or acceptance criteria are provided for what specifically is being inspected on this equipment | Specification.md | REQ-009, Verification table | — | PROPOSAL: Mechanical Contractor to prepare inspection checklist per permit requirements | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit step or note in Phase 2 requiring cold-side ductwork insulation specification (type, R-value, vapor barrier) prior to installation | Procedure Step 2.3 includes a parenthetical ASSUMPTION about ductwork insulation but no confirmed specification or procedural direction for the installer | Procedure.md | Step 2.3 | — | PROPOSAL: Mechanical Engineer to specify insulation requirements in DEL-003-07 | TBD |
| A-005 | A:operative:judging | WeakStatement | Procedure | Specification | Confirm airflow measurement tolerance (stated as +/-10% ASSUMPTION in Procedure) in the Specification or Mechanical Specification | Procedure verification table Step 4.3 states "within +/-10% of design (ASSUMPTION -- tolerance TBD per DEL-003-07)" -- this tolerance directly affects pass/fail and must be normatively confirmed | Procedure.md | Verification table, Step 4.3 | — | PROPOSAL: Mechanical Engineer to confirm tolerance in DEL-003-07 | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Facility volume is an assumption |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Heat recovery efficiency target missing |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet comprehensively records known attributes with source tracing |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements cited (13,000 sq ft, 35 ft, 130x100) are consistently sourced |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Electrical scope boundary signal missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents for current stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide a comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | HRV vs ERV terminology inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of system purpose and function is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents appropriately defer to Mechanical Engineer expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Acceptable at current project stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance provides essential discernment through principles and trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis in Guidance demonstrates adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers system-level interactions holistically |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record confirmed facility volume (currently flagged as ASSUMPTION: ~455,000 cu ft); confirm whether interior partitions, mezzanine, or ceiling structure reduce effective volume for ventilation calculation | Facility volume is an essential fact for equipment sizing (REQ-001, REQ-010) but is currently an unconfirmed assumption derived from approximate floor plan dimensions | Datasheet.md | Attributes — Facility Volume (approximate) | — | PROPOSAL: Mechanical Engineer to confirm in DEL-003-06 Calculation Package | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Specification | Add a minimum heat recovery efficiency target (numeric percentage) as a requirement or TBD placeholder in the Specification | Heat recovery efficiency is listed as TBD in Datasheet Attributes and REQ-002 requires meeting "applicable code and energy-efficiency standards" but no numeric target or standard-specific minimum is stated | Datasheet.md; Specification.md | Attributes — Heat Recovery Efficiency; REQ-002 | — | PROPOSAL: Mechanical Engineer to specify minimum efficiency in DEL-003-07 | TBD |
| B-003 | B:information:necessity | Conflict | Multi | TBD | Resolve the electrical scope boundary between PKG-013 (Mechanical Contractor) and PKG-015 (Electrical Contractor) for the air exchanger power connection | This scope boundary is flagged as unresolved in Guidance Conflict Table C-002 and Procedure Step 3.6; the Specification does not define the boundary; this is an essential signal for both contractors | Guidance.md; Procedure.md; Specification.md | Guidance — Conflict Table C-002; Procedure — Step 3.6; entire Specification scanned | Guidance.md#Conflict Table C-002 vs. Procedure.md#Step 3.6 | PROPOSAL: Design-Builder to define scope split in trade coordination matrix | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: consistently use either "HRV" or "ERV" or "HRV/ERV" across all documents, and clarify in Guidance that the final selection (HRV vs. ERV) is TBD pending Mechanical Engineer determination | Datasheet uses "HRV / ERV", Specification uses "heat recovery ventilator / energy recovery ventilator", Guidance discusses HRV vs ERV as a trade-off but sometimes implies HRV is preferred; _CONTEXT.md says "heat recovery ventilation" suggesting HRV only | Datasheet.md; Specification.md; Guidance.md; _CONTEXT.md | Datasheet — Attributes; Specification — Scope; Guidance — Trade-offs; _CONTEXT.md — Description | Datasheet.md#Attributes vs. _CONTEXT.md#Description | PROPOSAL: Guidance to establish canonical term pending Mechanical Engineer decision | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Standard Basis | 1 | HAS_ITEMS | Standards marked ASSUMPTION without confirmed applicability |
| C:normative:sufficiency | normative | sufficiency | Regulatory Assurance Threshold | 1 | HAS_ITEMS | Assurance threshold for NMeCC not established |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Record | 0 | NO_ITEMS | Standards table in Specification is comprehensive for current stage |
| C:normative:consistency | normative | consistency | Uniform Compliance Rigor | 0 | NO_ITEMS | Compliance language is consistent across documents |
| C:operative:necessity | operative | necessity | Operational Readiness Baseline | 1 | HAS_ITEMS | Missing fire stopping requirement for wall penetrations |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability Proof | 0 | NO_ITEMS | Procedure prerequisites adequately establish capability requirements |
| C:operative:completeness | operative | completeness | Full Process Coverage | 0 | NO_ITEMS | Procedure covers full lifecycle from design through closeout |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process steps are consistently structured and sequenced |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Criterion | 0 | NO_ITEMS | Value criteria (IAQ, energy recovery, code compliance) are well-founded |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Assessment | 0 | NO_ITEMS | Guidance Purpose section justifies the deliverable's worth |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | All value dimensions (health, energy, integration) are accounted for |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Harmony | 0 | NO_ITEMS | Value priorities are harmonized across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Confirm whether ASHRAE 62.1, ASHRAE 90.1, and CSA standards are mandatory or advisory for this Alberta jurisdiction; identify exact edition and applicable clauses | Multiple standards in the Specification Standards table are marked "ASSUMPTION" and "Likely applicable" -- for an enforceable standard basis these must be confirmed or removed | Specification.md | Standards table | — | PROPOSAL: Mechanical Engineer to confirm governing standards in DEL-003-07 | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification method for NMeCC compliance: identify what specific NMeCC provisions apply to this installation and how compliance will be demonstrated | National Mechanical Code of Canada is listed as Mandatory in Standards table but REQ-009 verification ("Safety Codes Officer inspection") does not specifically reference NMeCC provisions being verified | Specification.md | Standards table — NMeCC; REQ-009 | — | PROPOSAL: Safety Codes Officer inspection implicitly covers NMeCC but explicit traceability would strengthen assurance | TBD |
| C-003 | C:operative:necessity | MissingSlot | Procedure | Specification | Add requirement for fire stopping / firestopping at all wall penetrations (fresh air intake and exhaust outlet) per applicable fire code | Procedure Step 2.2 describes wall penetrations with "flashing and weatherproofing" but does not mention fire stopping, which is typically required where ductwork penetrates fire-rated assemblies | Procedure.md; Specification.md | Procedure — Step 2.2; Specification — REQ-005, REQ-006 | — | PROPOSAL: Confirm fire rating of penetrated walls and add fire stopping requirement if applicable | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Codified Enforcement Mandate | 0 | NO_ITEMS | Code compliance requirement REQ-009 is well-stated |
| F:normative:sufficiency | normative | sufficiency | Defensible Conformance Evidence | 1 | HAS_ITEMS | Commissioning evidence requirements incomplete |
| F:normative:completeness | normative | completeness | Total Regulatory Inventory | 0 | NO_ITEMS | Regulatory inventory is complete for current stage |
| F:normative:consistency | normative | consistency | Harmonized Compliance Standard | 0 | NO_ITEMS | Standards references are harmonized |
| F:operative:necessity | operative | necessity | Operational Prerequisite Threshold | 1 | HAS_ITEMS | Structural support prerequisite underspecified |
| F:operative:sufficiency | operative | sufficiency | Confirmed Execution Fitness | 1 | HAS_ITEMS | Vibration isolation not confirmed |
| F:operative:completeness | operative | completeness | Exhaustive Process Authority | 0 | NO_ITEMS | Process coverage is exhaustive |
| F:operative:consistency | operative | consistency | Stable Execution Coherence | 0 | NO_ITEMS | Execution steps are coherent and stable |
| F:evaluative:necessity | evaluative | necessity | Essential Quality Imperative | 0 | NO_ITEMS | Quality imperatives (IAQ, heat recovery, code compliance) are established |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Judgment | 0 | NO_ITEMS | Merit judgments in Guidance Trade-offs are substantiated |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Quality Authority | 1 | HAS_ITEMS | Noise/acoustic criteria missing |
| F:evaluative:consistency | evaluative | consistency | Calibrated Quality Coherence | 0 | NO_ITEMS | Quality criteria are coherently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add requirement for commissioning agent or third-party air balancing agency involvement; clarify whether independent commissioning is required or if Mechanical Contractor self-certification is acceptable | Specification REQ-012 requires "performance testing and commissioning" but Procedure Step 4.3 notes "Engage a certified air balancing agency if required by Mechanical Specification (DEL-003-07). (ASSUMPTION -- requirement TBD.)" -- the evidence standard for defensible conformance is unclear | Specification.md; Procedure.md | REQ-012; Procedure Step 4.3 | — | PROPOSAL: Owner/Design-Builder to determine if independent commissioning is required | TBD |
| F-002 | F:operative:necessity | RationaleGap | Specification | Guidance | Add rationale in Guidance for structural support requirements: explain why structural verification may be needed for industrial HRV/ERV units (weight, vibration) and when structural engineer involvement is triggered | Procedure Step 3.2 notes "Structural support is adequate for unit weight (confirm with structural design if required -- ASSUMPTION for heavy unit)" but no requirement or rationale addresses when structural verification is necessary | Procedure.md; Specification.md | Procedure — Step 3.2; entire Specification scanned | — | PROPOSAL: Mechanical Engineer to confirm unit weight and structural coordination need in design | TBD |
| F-003 | F:operative:sufficiency | WeakStatement | Procedure | Specification | Specify whether vibration isolation is required for the air exchanger installation, and if so, the type and performance criteria | Procedure Step 3.2 mentions "Vibration isolation (if specified by Mechanical Engineer)" -- this conditional language leaves execution fitness ambiguous; large industrial HRV units typically require vibration isolation | Procedure.md | Step 3.2 | — | PROPOSAL: Mechanical Engineer to confirm vibration isolation requirement in DEL-003-07 | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add noise/acoustic criteria for the air exchanger installation: maximum sound level at nearest occupied space, or reference to applicable noise standard | No acoustic or noise requirement appears in any production document; industrial HRV/ERV units can generate significant noise that affects occupant comfort and workplace safety (hearing protection thresholds) | Specification.md | entire document scanned | — | PROPOSAL: Mechanical Engineer to specify acoustic criteria in DEL-003-07 | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Decisive Regulatory Guidance | 0 | NO_ITEMS | Guidance provides clear regulatory direction |
| D:normative:applying | normative | applying | Enforced Compliance Practice | 0 | NO_ITEMS | Compliance practice is enforced through permit and inspection requirements |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Safety Codes Officer provides definitive ruling mechanism |
| D:normative:reviewing | normative | reviewing | Settled Conformance Oversight | 0 | NO_ITEMS | Inspection and CCC provide conformance oversight |
| D:operative:guiding | operative | guiding | Resolved Workflow Direction | 1 | HAS_ITEMS | Design coordination sequencing gap |
| D:operative:applying | operative | applying | Assured Task Execution | 0 | NO_ITEMS | Task execution steps are assured through prerequisites and sequencing |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 1 | HAS_ITEMS | Heat recovery test conditions undefined |
| D:operative:reviewing | operative | reviewing | Verified Process Stability | 0 | NO_ITEMS | Process stability verification is covered |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Direction | 0 | NO_ITEMS | Quality direction is settled through principles and considerations |
| D:evaluative:applying | evaluative | applying | Decisive Merit Deployment | 0 | NO_ITEMS | Merit deployment is addressed through trade-off analysis |
| D:evaluative:judging | evaluative | judging | Authoritative Worth Verdict | 1 | HAS_ITEMS | Owner training requirement unresolved |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Benchmark | 0 | NO_ITEMS | Benchmarks are established through commissioning criteria |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on the design coordination meeting/milestone: when must PKG-003 design outputs be finalized relative to PKG-013 procurement, and what is the escalation path if design delays threaten the December 2026 deadline | Guidance P-4 states "coordinate before design locks in" and Considerations discuss the dependency, but no explicit timeline guidance or escalation path is provided for resolving the design-to-procurement sequencing | Guidance.md | Principles — P-4; Considerations — Mechanical Design Dependency | — | PROPOSAL: Project Manager to establish design-to-procurement milestone in project schedule | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Define heat recovery performance test conditions: at what outdoor and indoor temperatures, at what airflow rate, and against what baseline shall heat recovery efficiency be measured during commissioning | Specification REQ-002 verification states "commissioning test data" but does not define test conditions; heat recovery efficiency varies significantly with temperature differential and airflow rate | Specification.md | REQ-002 — Verification | — | PROPOSAL: Mechanical Engineer to define commissioning test protocol in DEL-003-07 | TBD |
| D-003 | D:evaluative:judging | TBD_Question | Procedure | Procedure | Confirm whether Owner training (Procedure Step 5.4) is contractually required under CCDC 14-2013 or the RFP, and if so, define minimum training content and duration | Procedure Step 5.4 is marked "ASSUMPTION -- Owner training typically expected; confirm with Design-Builder whether formal training is required under this contract" -- this affects worth determination for the deliverable closeout | Procedure.md | Step 5.4 | — | PROPOSAL: Design-Builder to confirm training requirement against contract terms | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Directive Mandate | 0 | NO_ITEMS | Directive mandates are grounded in RFP and code references |
| X:guiding:sufficiency | guiding | sufficiency | Validated Advisory Basis | 0 | NO_ITEMS | Advisory basis in Guidance is validated through source references |
| X:guiding:completeness | guiding | completeness | Exhaustive Counsel Scope | 1 | HAS_ITEMS | Condensate drain guidance missing |
| X:guiding:consistency | guiding | consistency | Coherent Advisory Alignment | 0 | NO_ITEMS | Advisory content is coherently aligned across Guidance sections |
| X:applying:necessity | applying | necessity | Mandatory Deployment Trigger | 0 | NO_ITEMS | Deployment triggers (prerequisites) are clearly defined |
| X:applying:sufficiency | applying | sufficiency | Proven Implementation Fitness | 1 | HAS_ITEMS | Filter maintenance access not addressed |
| X:applying:completeness | applying | completeness | Total Deployment Record | 1 | HAS_ITEMS | Warranty registration step missing |
| X:applying:consistency | applying | consistency | Dependable Deployment Accuracy | 0 | NO_ITEMS | Deployment steps are accurately and consistently described |
| X:judging:necessity | judging | necessity | Decisive Adjudication Basis | 0 | NO_ITEMS | Adjudication bases are decisively established |
| X:judging:sufficiency | judging | sufficiency | Evidenced Adjudication Competence | 1 | HAS_ITEMS | Air balance report content not specified |
| X:judging:completeness | judging | completeness | Exhaustive Ruling Authority | 0 | NO_ITEMS | Ruling authority is exhaustively established through verification table |
| X:judging:consistency | judging | consistency | Harmonized Verdict Standard | 0 | NO_ITEMS | Verdict standards are harmonized |
| X:reviewing:necessity | reviewing | necessity | Verified Oversight Imperative | 0 | NO_ITEMS | Oversight imperatives are verified |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Review Evidence | 1 | HAS_ITEMS | As-built documentation acceptance unclear |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 0 | NO_ITEMS | Audit coverage through records table is exhaustive |
| X:reviewing:consistency | reviewing | consistency | Standardized Review Measure | 0 | NO_ITEMS | Review measures are standardized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add consideration for condensate drain management: HRV/ERV units produce condensate from the heat recovery core, especially in heating season; drain routing and freeze protection must be addressed | Guidance Considerations section covers cold-climate performance, coordination, and electrical interface but does not mention condensate drainage -- a common installation issue for HRV/ERV units in cold climates | Guidance.md | Considerations — entire section scanned | — | PROPOSAL: Mechanical Engineer to address condensate drain in equipment specification | TBD |
| X-002 | X:applying:sufficiency | MissingSlot | Specification | Specification | Add requirement for maintenance access: unit shall be installed with sufficient clearance for filter replacement, core cleaning, and routine service per manufacturer requirements | Procedure Step 3.2 mentions "service clearances" but no Specification requirement establishes minimum maintenance access; filter maintenance is listed in the O&M manual scope (Documentation table) but access is not ensured by any requirement | Specification.md; Procedure.md | Specification — entire Requirements section scanned; Procedure — Step 3.2 | — | PROPOSAL: Mechanical Engineer to specify clearances in DEL-003-07 | TBD |
| X-003 | X:applying:completeness | VerificationGap | Procedure | Procedure | Add closeout step for warranty registration with equipment manufacturer, including documentation of installation per manufacturer requirements to preserve warranty | Procedure Phase 5 covers commissioning report, O&M manual, as-builts, and training but does not include warranty registration; Specification REQ-013 establishes a 2-year guarantee period that depends on proper warranty activation | Procedure.md; Specification.md | Procedure — Phase 5; Specification — REQ-013 | — | PROPOSAL: Mechanical Contractor to confirm manufacturer warranty registration requirements | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Define minimum content requirements for the air balance report: what measurements, zones, and data points must be included to constitute adequate evidence of compliance with REQ-001, REQ-003, and REQ-004 | Specification Verification table references "air balance test" for REQ-003 and REQ-004 and Procedure records table lists "Air balance report" but neither defines what the report must contain | Specification.md; Procedure.md | Specification — Verification table REQ-003, REQ-004; Procedure — Records table | — | PROPOSAL: Define air balance report requirements in DEL-003-07 or Specification | TBD |
| X-005 | X:reviewing:sufficiency | WeakStatement | Procedure | Procedure | Clarify who reviews and accepts as-built mark-ups, and what constitutes acceptable as-built documentation (e.g., red-line on IFC drawings, digital overlay, tolerance for deviations) | Procedure Step 5.3 states "Submit to Design-Builder for as-built drawing compilation" but does not define acceptance criteria or review process for as-built accuracy | Procedure.md | Step 5.3 | — | PROPOSAL: Design-Builder to define as-built submission requirements | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative and well-sourced |
| E:guiding:information | guiding | information | Integrated Directive Context | 0 | NO_ITEMS | Directive context is well-integrated |
| E:guiding:knowledge | guiding | knowledge | Mastered Advisory Proficiency | 0 | NO_ITEMS | Advisory proficiency demonstrated in Guidance |
| E:guiding:wisdom | guiding | wisdom | Principled Directive Judgment | 0 | NO_ITEMS | Principled judgment demonstrated in trade-offs and principles |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Receiving inspection record gap |
| E:applying:information | applying | information | Actionable Deployment Report | 0 | NO_ITEMS | Deployment reporting is actionable |
| E:applying:knowledge | applying | knowledge | Proven Deployment Mastery | 0 | NO_ITEMS | Deployment steps demonstrate procedural mastery |
| E:applying:wisdom | applying | wisdom | Principled Deployment Judgment | 0 | NO_ITEMS | Deployment judgment is principled |
| E:judging:data | judging | data | Documented Verdict Record | 1 | HAS_ITEMS | Pre-startup checklist not documented |
| E:judging:information | judging | information | Contextualized Verdict Account | 0 | NO_ITEMS | Verdict accounts are contextualized |
| E:judging:knowledge | judging | knowledge | Expert Adjudication Command | 0 | NO_ITEMS | Expert adjudication is adequately established |
| E:judging:wisdom | judging | wisdom | Principled Verdict Wisdom | 0 | NO_ITEMS | Verdict wisdom demonstrated through conflict table |
| E:reviewing:data | reviewing | data | Comprehensive Audit Record | 1 | HAS_ITEMS | Conflict between Guidance and Specification on HRV vs ERV |
| E:reviewing:information | reviewing | information | Coherent Audit Narrative | 0 | NO_ITEMS | Audit narrative is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Mastered Audit Proficiency | 0 | NO_ITEMS | Audit proficiency demonstrated through records table |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Discernment | 1 | HAS_ITEMS | Sustainability/energy rationale gap |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Procedure | Procedure | Add explicit receiving inspection record/form to the Records table: document that equipment was inspected on delivery and found acceptable | Procedure Step 3.1 describes receiving inspection (check for damage, verify model/serial) but no record or form is listed in the Records table to document this inspection | Procedure.md | Step 3.1; Records table | — | PROPOSAL: Mechanical Contractor to add receiving inspection to record set | TBD |
| E-002 | E:judging:data | Normalization | Procedure | Procedure | Add pre-startup checklist to the Records table as a documented verdict record; Step 4.1 references the checklist and Verification table references "Pre-startup checklist form" but Records table does not list it | The pre-startup checklist is referenced in Procedure Step 4.1 and Verification table but is absent from the Records table, creating a documentation gap | Procedure.md | Step 4.1; Verification table; Records table | — | PROPOSAL: Add to Records table | TBD |
| E-003 | E:reviewing:data | Conflict | Guidance | Guidance | Resolve whether interim assumption should be HRV (as stated in Guidance Conflict Table C-001) or remain open as HRV/ERV pending Mechanical Engineer determination | Guidance Conflict Table C-001 proposes "treat as HRV in interim" but Specification Scope uses "heat recovery ventilator / energy recovery ventilator" and Datasheet uses "HRV / ERV" -- the interim assumption in Guidance is not reflected in the other documents | Guidance.md; Specification.md; Datasheet.md | Guidance — Conflict Table C-001; Specification — Scope; Datasheet — Attributes | Guidance.md#Conflict Table C-001 vs. Specification.md#Scope | PROPOSAL: Human ruling needed on whether to treat as HRV pending design confirmation | TBD |
| E-004 | E:reviewing:wisdom | RationaleGap | Guidance | Guidance | Add a consideration or principle addressing energy performance and sustainability: explain the relationship between heat recovery efficiency, operating cost, and Owner long-term value beyond code minimums | Guidance discusses heat recovery as "essential for Alberta climate operation" (P-2) from a heating-load perspective but does not address whether the Owner's objectives (OBJ-001, OBJ-004) imply a preference for exceeding code-minimum energy performance | Guidance.md | Principles — P-2; Purpose — Objective linkage | — | PROPOSAL: Design-Builder/Owner to confirm whether energy performance beyond code minimum is a project value | TBD |
