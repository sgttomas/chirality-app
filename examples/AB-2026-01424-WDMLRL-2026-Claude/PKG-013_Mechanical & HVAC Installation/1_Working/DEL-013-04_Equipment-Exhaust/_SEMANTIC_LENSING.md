# Semantic Lensing Register: DEL-013-04 Heavy Equipment Exhaust System

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-04_Equipment-Exhaust/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-013-04_Equipment-Exhaust/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements)
- _STATUS.md -- DEL-013-04_Equipment-Exhaust/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-013-04_Equipment-Exhaust/_SEMANTIC.md (Matrices A, B, C, F, D, X, E)
- Datasheet.md -- DEL-013-04_Equipment-Exhaust/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md -- DEL-013-04_Equipment-Exhaust/Specification.md (Scope, Requirements REQ-001 through REQ-011, Standards, Verification, Documentation)
- Guidance.md -- DEL-013-04_Equipment-Exhaust/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md -- DEL-013-04_Equipment-Exhaust/Procedure.md (Prerequisites, Steps 1-16, Verification, Records)
- _REFERENCES.md -- DEL-013-04_Equipment-Exhaust/_REFERENCES.md (Primary References, Standard References, Drawing References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 12
  - Guidance: 4
  - Procedure: 4
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 4  F: 5  D: 3  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific code clause references missing for exhaust standards |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Filtration requirement conditional; needs resolution |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Environmental compliance verification method underspecified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Safety codes audit scope not linked to specific inspection hold points |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate direction for installation sequence |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-16 provide sufficient execution detail for current project stage |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Fan airflow tolerance assumed at +/-10% without normative basis |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Pre-commissioning inspection (Step 11) and records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value orientation clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table provides adequate merit comparison |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality appraisal addressed via commissioning requirements |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification tables in both Specification and Procedure are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Provide specific ASHRAE standard number (e.g., ASHRAE 62.1, ASHRAE Fundamentals Ch. 46) and specific Alberta OHS Code Part 25 clause references applicable to exhaust systems | REQ-004 lists standards by name but all have "location TBD" for clause references; prescriptive direction cannot be followed without identifiable clauses | Specification.md | REQ-004 -- Code-Compliant Installation; Standards table | -- | Mechanical Engineer to identify applicable clauses during design | TBD |
| A-002 | A:normative:applying | Conflict | Multi | Specification | Resolve whether filtration is mandatory scope or conditional; if conditional, add decision gate in Specification and Procedure | _CONTEXT.md Scope lists "Filtration and treatment systems installation" as in-scope, while R-01 section 3.4 specifies only "exhaust hoses and fans" without mentioning filtration; Guidance CQ-002 flags this but Specification REQ-010 defers to design | Specification.md; Guidance.md | REQ-010; Guidance CQ-002 | _CONTEXT.md#Scope vs R-01 section 3.4 per Guidance CQ-002 | Environmental compliance review determines; mechanical engineer specifies | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add specific environmental permit acceptance criteria or reference the regulatory determination that must be completed before outlet construction | REQ-005 requires compliance but does not specify what regulatory approval artifact constitutes compliance determination; verification method says "Review of outlet location... against environmental permit conditions" but no permit requirement is established as a prerequisite | Specification.md | REQ-005 -- Environmental and Safety Compliance; Verification table REQ-005 row | -- | Environmental reviewer to define acceptance criteria | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add explicit inspection hold points with Safety Codes Officer notification requirements at critical stages (e.g., before duct concealment, after penetration sealing) | Procedure Step 11 mentions pre-commissioning inspection but does not identify mandatory regulatory inspection hold points; Specification Verification references "Inspection by Alberta Safety Codes Officer" but Procedure does not sequence when this occurs | Procedure.md; Specification.md | Procedure Step 11; Specification Verification REQ-004 row | -- | Safety Codes Officer / Project Manager to define hold points | TBD |
| A-005 | A:operative:judging | WeakStatement | Procedure | Specification | Confirm fan airflow tolerance from mechanical specification; replace ASSUMPTION with normative tolerance value | Procedure Verification table states "Measured CFM within +/-10% of design (ASSUMPTION -- tolerance TBD in mechanical specification)"; this tolerance directly affects pass/fail judgment but lacks normative authority | Procedure.md | Verification table -- "Fan airflow within design tolerance" row | -- | Mechanical Engineer to specify in DEL-003-05 | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Equipment exhaust volume data not yet available |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Hose drop count TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet adequately catalogues known and TBD parameters |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units and parameter naming consistent across documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Equipment type list incomplete |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Documents provide adequate context for what is known |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents consistently acknowledge TBD items |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for collection devices |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Source-capture principle well established in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents assume competent mechanical contractor |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for current project stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs provide adequate discernment framing |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment scope appropriate for design-build delivery |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | System integration considerations adequately noted |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain equipment exhaust volume data (CFM per piece of equipment) from County or equipment manufacturers for fan sizing | This is the essential datum required for system design; Datasheet lists Fan Type/Quantity as TBD, Guidance Principle 2 states sizing "must be based on actual exhaust flow rates" but no exhaust volume data exists in any document | Datasheet.md; Guidance.md | Datasheet Attributes "Fan Type / Quantity"; Guidance Principles section 2 | -- | County to supply equipment list; Mechanical Engineer to obtain exhaust volumes | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm number of exhaust hose drops per bay and total system capacity | Datasheet notes "one exhaust drop per bay minimum; exact quantity TBD" as an ASSUMPTION; Specification REQ-002 defers to mechanical design; adequate evidence for system sizing depends on this count | Datasheet.md; Specification.md | Datasheet Attributes "Number of Repair Bays Served"; Specification REQ-002 | -- | Mechanical Engineer via DEL-003-04 | TBD |
| B-003 | B:information:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain formal equipment list identifying all heavy equipment types serviced at the facility with engine size and fuel type | Datasheet Conditions "Equipment Types Served" notes equipment list is TBD; Guidance flags this as "Equipment Type Uncertainty"; the equipment list is an essential input for filtration selection, hose sizing, and hazard classification | Datasheet.md; Guidance.md | Datasheet Conditions "Equipment Types Served"; Guidance Considerations "Equipment Type Uncertainty" | -- | County to provide equipment fleet list | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: choose one term for exhaust collection devices and use consistently (e.g., "exhaust hose drops" or "exhaust hose reel assemblies" or "collection hoods") | Documents use varying terms: "exhaust hoses" (Spec REQ-001), "exhaust hose drops" (Procedure Step 6 title), "hose reel assemblies" (Procedure Step 6 body), "collection hoods" (Specification Scope item 4), "capture devices" (Datasheet Construction); Guidance Trade-offs distinguishes "fixed pendant drops" vs "retractable hose reels" as options, but the baseline term is unstable | Specification.md; Procedure.md; Datasheet.md | Specification REQ-001, Scope item 4; Procedure Step 6; Datasheet Construction "Collection Hoods" row | -- | Mechanical Engineer to standardize in design specification | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Grasp | 1 | HAS_ITEMS | Mandatory worker exposure limits not cited |
| C:normative:sufficiency | normative | sufficiency | Warranted Regulatory Basis | 0 | NO_ITEMS | Regulatory basis adequately cited for current stage (RFP, codes named) |
| C:normative:completeness | normative | completeness | Exhaustive Governance Coverage | 1 | HAS_ITEMS | Fire code requirements for ductwork not fully addressed |
| C:normative:consistency | normative | consistency | Stable Regulatory Uniformity | 0 | NO_ITEMS | Regulatory references consistent across documents |
| C:operative:necessity | operative | necessity | Critical Execution Readiness | 1 | HAS_ITEMS | Condensate management decision missing |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Grounding | 0 | NO_ITEMS | Procedure prerequisites table comprehensive |
| C:operative:completeness | operative | completeness | Total Operational Capture | 0 | NO_ITEMS | Installation steps cover full scope |
| C:operative:consistency | operative | consistency | Reproducible Process Coherence | 0 | NO_ITEMS | Procedure steps internally consistent |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Discernment | 0 | NO_ITEMS | Value proposition clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Appraisal | 0 | NO_ITEMS | Trade-off table provides sufficient appraisal basis |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Accounting | 1 | HAS_ITEMS | Lifecycle/operating cost not addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Evaluation Stability | 0 | NO_ITEMS | Evaluation criteria stable across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement or reference for worker exposure limits (e.g., Alberta OHS Code Part 25 Table 4 TLVs for CO, NO2, diesel particulate matter) applicable during system operation and during testing | REQ-003 requires "safe capture" and prevention of "hazardous concentrations" but does not cite the occupational exposure limit (OEL) values that define "hazardous"; this is the obligatory compliance threshold the system must achieve | Specification.md | REQ-003 -- Safe Removal of Hazardous Exhaust | -- | Alberta OHS Code, ACGIH TLV values | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification method for fire code compliance of ductwork penetrations (NFC requirements for fire-rated assemblies at duct penetrations through fire separations) | Procedure Step 5.5 mentions "fire-rated sleeves or sealed assemblies as required by the building code and fire code" but the Specification has no corresponding requirement for fire-rated penetrations, and the Verification table does not include a fire code check for ductwork penetrations | Specification.md; Procedure.md | Specification Verification table (no fire code row); Procedure Step 5.5 | -- | Fire code compliance officer; Mechanical Engineer | TBD |
| C-003 | C:operative:necessity | WeakStatement | Procedure | Specification | Resolve whether condensate management is required; if yes, add requirement to Specification and specify slope direction and drain points in Procedure Step 5.2 | Procedure Step 5.2 states "Install ductwork with positive slope toward drain points (if condensate management is specified by the mechanical engineer -- TBD)"; this conditional phrasing leaves a critical execution step unresolved and could lead to rework if drainage is needed after installation | Procedure.md | Step 5 -- Install Exhaust Ductwork, sub-step 2 | -- | Mechanical Engineer to determine during design | TBD |
| C-004 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration of lifecycle operating cost (energy consumption, filter replacement, hose wear) as a factor in trade-off decisions between options | Guidance Trade-offs table compares options by complexity and cost but does not address lifecycle operating cost, maintenance burden, or energy consumption as evaluation factors; holistic merit accounting requires these considerations for design-build value | Guidance.md | Trade-offs table | -- | Project Manager / Mechanical Engineer to evaluate | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Compliance Mandate | 1 | HAS_ITEMS | Capture velocity requirement missing |
| F:normative:sufficiency | normative | sufficiency | Sufficient Governance Evidence | 1 | HAS_ITEMS | Standards accessibility barrier |
| F:normative:completeness | normative | completeness | Absolute Accountability Scope | 0 | NO_ITEMS | Accountability chain adequately traced through verification table |
| F:normative:consistency | normative | consistency | Principled Conformance Clarity | 0 | NO_ITEMS | Conformance requirements stable across documents |
| F:operative:necessity | operative | necessity | Decisive Operational Fluency | 1 | HAS_ITEMS | Controls functional specification missing |
| F:operative:sufficiency | operative | sufficiency | Confirmed Execution Adequacy | 0 | NO_ITEMS | Installation steps adequate for current stage |
| F:operative:completeness | operative | completeness | Exhaustive Procedural Command | 1 | HAS_ITEMS | Training/handover requirements absent |
| F:operative:consistency | operative | consistency | Systematic Execution Discipline | 0 | NO_ITEMS | Procedure sequencing internally disciplined |
| F:evaluative:necessity | evaluative | necessity | Rigorous Value Foundation | 0 | NO_ITEMS | Value foundation established through safety and compliance rationale |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Justification | 1 | HAS_ITEMS | Warranty scope for subcomponents unclear |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Quality Authority | 0 | NO_ITEMS | Quality requirements traced through commissioning and inspection |
| F:evaluative:consistency | evaluative | consistency | Coherent Appraisal Discipline | 0 | NO_ITEMS | Appraisal criteria consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add quantitative capture velocity requirement at hose connection points (e.g., minimum face velocity in FPM per ACGIH Industrial Ventilation Manual) | REQ-011 verification requires confirming "exhaust capture velocity at hose connection points meets design specification" but no numeric capture velocity requirement exists in any production document; the authoritative compliance mandate for capture effectiveness has no measurable threshold | Specification.md | REQ-011 -- Commissioning and Performance Testing; REQ-001 -- Exhaust Capture at Source | -- | Mechanical Engineer per ACGIH Industrial Ventilation guidelines | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | For each standard in the Standards table, either provide a specific accessible clause reference or record a TBD action to obtain it before design completion | All seven entries in the Standards table have "location TBD" for accessibility; sufficient governance evidence requires that the normative basis be accessible to the person verifying compliance; currently no standard clause can be checked | Specification.md | Standards table (all rows) | -- | Mechanical Engineer / Code consultant to identify clauses | TBD |
| F-003 | F:operative:necessity | MissingSlot | Specification | Specification | Add requirement defining controls functional specification (fan interlock with bay door? automatic start on hose connection? manual switch only? alarm on fan failure?) | REQ-011 verification item 4 requires "Controls and monitoring function as designed" but no requirement defines what the controls must do; Datasheet lists "Controls and Monitoring" as TBD; Procedure Step 10 installs per "controls specification (TBD)"; decisive operational fluency requires a defined control function | Specification.md; Datasheet.md; Procedure.md | Specification REQ-011; Datasheet Attributes "Controls and Monitoring"; Procedure Step 10 | -- | Mechanical Engineer to specify in design | TBD |
| F-004 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add step or sub-phase for operator training/handover (beyond the owner demonstration in Step 16); include maintenance schedule handover and filter replacement procedures | Procedure Step 16 includes "Owner Demonstration" but does not address formal operator training on daily use (hose connection procedure, system start/stop, alarm response) or handover of maintenance schedule; for a continuously operating facility this is an operational completeness gap | Procedure.md | Step 16 -- Final Walkthrough and Owner Demonstration | -- | Project Manager / Mechanical Contractor | TBD |
| F-005 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Clarify warranty coverage scope: does the 2-year warranty cover replacement of consumables (hoses, filters) or only fixed equipment (fans, ductwork)? Add guidance note | Datasheet states "Warranty Period: 2 years post CCC" and Procedure Records references "warranty documentation per RFP section 2.10" but no document clarifies whether consumable components (flexible hoses, filter media) are included or excluded; defensible quality justification requires this distinction | Datasheet.md; Procedure.md | Datasheet Attributes "Warranty Period"; Procedure Records "Warranty Documentation" | -- | Contract review of CCDC 14-2013 warranty provisions | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Steering | 0 | NO_ITEMS | Regulatory steering adequate for design-build approach |
| D:normative:applying | normative | applying | Enforced Compliance Method | 0 | NO_ITEMS | Compliance methods identified in verification table |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 1 | HAS_ITEMS | No acceptance criteria for re-entrainment test |
| D:normative:reviewing | normative | reviewing | Authoritative Adherence Review | 0 | NO_ITEMS | Adherence review via Safety Codes Officer inspection adequate |
| D:operative:guiding | operative | guiding | Resolved Workflow Guidance | 0 | NO_ITEMS | Workflow guidance resolved through phased procedure |
| D:operative:applying | operative | applying | Verified Work Delivery | 1 | HAS_ITEMS | As-built documentation requirements need specification |
| D:operative:judging | operative | judging | Definitive Execution Verdict | 0 | NO_ITEMS | Commissioning test provides execution verdict |
| D:operative:reviewing | operative | reviewing | Rigorous Workflow Inspection | 0 | NO_ITEMS | Pre-commissioning inspection (Step 11) adequate |
| D:evaluative:guiding | evaluative | guiding | Resolved Quality Direction | 0 | NO_ITEMS | Quality direction resolved via principles |
| D:evaluative:applying | evaluative | applying | Justified Quality Enactment | 1 | HAS_ITEMS | No product substitution control documented |
| D:evaluative:judging | evaluative | judging | Definitive Holistic Appraisal | 0 | NO_ITEMS | Commissioning report provides appraisal basis |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Worth Inspection | 0 | NO_ITEMS | Worth inspection addressed through owner walkthrough |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add measurable pass/fail criterion for re-entrainment test (REQ-005 verification): define test method (e.g., smoke release at outlet during building air intake operation) and acceptance threshold | REQ-005 requires outlet positioned to "prevent re-entrainment" but Verification says only "Review of outlet location and stack height against environmental permit conditions"; no field test or acceptance criterion exists for confirming absence of re-entrainment, making a conclusive conformance verdict impossible | Specification.md | REQ-005 Verification row; REQ-011 | -- | Mechanical Engineer / Environmental reviewer | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add as-built documentation requirements specifying what must be marked up (duct routing deviations, actual hose drop locations, actual outlet position) and the format/timing for as-built submission | Procedure Records lists "As-Built Mark-Up Drawings" but no procedure step describes when or how as-built markups are created; Specification Documentation table lists "Installation Record" with timing "At completion" but no specification for content or format; verified work delivery requires traceable as-built records | Procedure.md; Specification.md | Procedure Records table; Specification Documentation table "Installation Record" row | -- | Project Manager to define as-built requirements | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Specification | Specification | Add product substitution control requirement: if approved products are unavailable, require formal substitution request with engineering review before installation of alternate products | Specification Documentation requires "Product Submittals... for review and approval" but no requirement addresses what happens if an approved product becomes unavailable after submittal approval; for justified quality enactment, a substitution control process preserves the merit basis of the original approval | Specification.md | Documentation table "Product Submittals" row | -- | Mechanical Engineer / Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Clarity | 0 | NO_ITEMS | Steering clarity established through Guidance principles |
| X:guiding:sufficiency | guiding | sufficiency | Grounded Directional Competence | 0 | NO_ITEMS | Directional competence grounded in RFP and code references |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Coverage | 1 | HAS_ITEMS | No guidance on system decommissioning/modification |
| X:guiding:consistency | guiding | consistency | Coherent Steering Stability | 0 | NO_ITEMS | Steering consistent across documents |
| X:applying:necessity | applying | necessity | Verified Procedural Imperative | 1 | HAS_ITEMS | Duct material specification missing |
| X:applying:sufficiency | applying | sufficiency | Grounded Implementation Evidence | 0 | NO_ITEMS | Implementation evidence adequate for current stage |
| X:applying:completeness | applying | completeness | Comprehensive Enactment Record | 0 | NO_ITEMS | Enactment record requirements adequate in Records table |
| X:applying:consistency | applying | consistency | Uniform Execution Assurance | 0 | NO_ITEMS | Execution assurance uniform across procedure steps |
| X:judging:necessity | judging | necessity | Binding Determination Finding | 1 | HAS_ITEMS | No noise/vibration acceptance criteria |
| X:judging:sufficiency | judging | sufficiency | Warranted Judgment Basis | 0 | NO_ITEMS | Judgment basis warranted through test methods |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Archive | 0 | NO_ITEMS | Judgment archive requirements adequate |
| X:judging:consistency | judging | consistency | Stable Verdict Coherence | 0 | NO_ITEMS | Verdict criteria consistent between Specification and Procedure verification tables |
| X:reviewing:necessity | reviewing | necessity | Vital Inspection Discovery | 0 | NO_ITEMS | Inspection scope adequate for identified risks |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Inspection Basis | 0 | NO_ITEMS | Inspection basis warranted |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Archive | 1 | HAS_ITEMS | Photo documentation not specified |
| X:reviewing:consistency | reviewing | consistency | Transparent Audit Coherence | 0 | NO_ITEMS | Audit trail coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add consideration for future system modification or capacity expansion (e.g., if additional equipment bays are added or equipment fleet changes) | Guidance Considerations address current design dependencies but do not address future adaptability; for exhaustive directional coverage the design rationale should note whether the system should be sized for current load only or include expansion capacity | Guidance.md | Considerations section (entire section scanned) | -- | Project Manager / County to determine expansion requirements | TBD |
| X-002 | X:applying:necessity | Normalization | Specification | Specification | Specify ductwork material requirement (e.g., galvanized steel per SMACNA standards for industrial exhaust) or explicitly defer to mechanical design specification | Specification Scope item 3 references "Ductwork" and Datasheet Construction lists "Rigid ductwork... material and routing TBD"; Procedure Step 5 says "Install rigid ductwork" and Step 5.4 says "Seal all duct joints with approved sealant per the mechanical specification" but no document specifies duct material; this is a verified procedural imperative that cannot be executed without material specification | Specification.md; Datasheet.md; Procedure.md | Specification Scope item 3; Datasheet Construction "Ductwork"; Procedure Step 5 | -- | Mechanical Engineer per SMACNA Industrial Duct Construction Standards | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add noise and vibration acceptance criteria for exhaust fan operation (e.g., maximum dBA at operator position, acceptable vibration amplitude) | Procedure Step 12.3 says "Listen for unusual vibration, noise, or bearing noise; shut down and investigate if abnormal" but no quantitative acceptance criterion exists; binding determination of "abnormal" requires a measurable threshold | Specification.md; Procedure.md | Procedure Step 12.3; Specification Verification table (no noise/vibration row) | -- | Mechanical Engineer / Equipment manufacturer specifications | TBD |
| X-004 | X:reviewing:completeness | Normalization | Procedure | Procedure | Add photo documentation requirement at key installation milestones (duct support attachment to structure, penetration sealing before concealment, hose drop installation) to support exhaustive inspection archive | Procedure Records lists drawing markups and reports but does not require photographic records; for concealed work (duct penetrations sealed behind finishes) photo documentation is standard practice to support post-completion review | Procedure.md | Records table (entire table scanned) | -- | Project Manager / Mechanical Contractor standard practice | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Anchored Leadership Evidence | 0 | NO_ITEMS | Leadership evidence anchored in RFP references |
| E:guiding:information | guiding | information | Contextualized Steering Signal | 0 | NO_ITEMS | Steering signals contextualized in Guidance |
| E:guiding:knowledge | guiding | knowledge | Integrated Leadership Mastery | 0 | NO_ITEMS | Integration knowledge adequate in Guidance system coordination sections |
| E:guiding:wisdom | guiding | wisdom | Principled Steering Foresight | 0 | NO_ITEMS | Foresight demonstrated in trade-offs and assumptions |
| E:applying:data | applying | data | Evidenced Practice Record | 1 | HAS_ITEMS | Duct leakage test method unspecified |
| E:applying:information | applying | information | Grounded Execution Context | 0 | NO_ITEMS | Execution context grounded in prerequisite table |
| E:applying:knowledge | applying | knowledge | Verified Practice Mastery | 0 | NO_ITEMS | Practice knowledge adequate for installer |
| E:applying:wisdom | applying | wisdom | Judicious Practice Foresight | 0 | NO_ITEMS | Practice foresight demonstrated in phased approach |
| E:judging:data | judging | data | Definitive Verdict Evidence | 1 | HAS_ITEMS | Commissioning report format not specified |
| E:judging:information | judging | information | Transparent Judgment Account | 0 | NO_ITEMS | Judgment account transparent through verification tables |
| E:judging:knowledge | judging | knowledge | Comprehensive Judgment Mastery | 0 | NO_ITEMS | Judgment knowledge adequate |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Judgment foresight adequate |
| E:reviewing:data | reviewing | data | Evidenced Inspection Record | 0 | NO_ITEMS | Inspection records defined in Records table |
| E:reviewing:information | reviewing | information | Warranted Inspection Account | 0 | NO_ITEMS | Inspection account warranted |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Mastery | 1 | HAS_ITEMS | Deficiency classification system absent |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 0 | NO_ITEMS | Inspection foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | VerificationGap | Procedure | Specification | Specify duct leakage test method and acceptance criteria (e.g., SMACNA leakage class, test pressure, maximum allowable leakage rate) or explicitly state that leakage testing is not required | Procedure Step 11.3 states "Perform a duct leakage test if required by the mechanical specification or applicable standard (method TBD in IFC design)" -- the conditional phrasing and TBD method mean no evidenced practice record can be produced for duct integrity; the decision on whether to test must be made | Procedure.md | Step 11.3 -- Pre-Commissioning Inspection and Leak Test | -- | Mechanical Engineer to specify or waive | TBD |
| E-002 | E:judging:data | Normalization | Specification | Specification | Define commissioning report format requirements (minimum data fields, report template or standard to follow) to ensure definitive verdict evidence is consistently structured | Specification Documentation lists "Commissioning Report: Documented performance test results; fan airflow and static pressure; capture velocity measurements" and Procedure Step 13 says "Document all test readings in the commissioning report" but neither specifies a report format or template; without format standardization the verdict evidence may be incomplete or inconsistent | Specification.md; Procedure.md | Specification Documentation "Commissioning Report" row; Procedure Step 13.5 | -- | Mechanical Engineer / Commissioning agent to define template | TBD |
| E-003 | E:reviewing:knowledge | Conflict | Procedure | Procedure | Align deficiency handling: Procedure Step 11.6 references "RFI or non-conformance report" while Records table references "Deficiency List and Close-Out" -- clarify whether these are the same document or different instruments, and define severity classification for deficiencies | Procedure Step 11.6 says "Issue an RFI or non-conformance report for any deficiencies found" while the Records table lists "Deficiency List and Close-Out" as a separate record; the relationship between these instruments is unclear and comprehensive audit mastery requires a defined deficiency classification and escalation process | Procedure.md | Step 11.6; Records table "Deficiency List and Close-Out" row | Procedure.md#Step-11 vs Procedure.md#Records | Project Manager to define deficiency management process | TBD |
