# Semantic Lensing Register: DEL-003-04 Exhaust System Plans

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-003_Mechanical Design/1_Working/DEL-003-04_Exhaust-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-04_Exhaust-Plans/_CONTEXT.md
- _STATUS.md — DEL-003-04_Exhaust-Plans/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-04_Exhaust-Plans/_SEMANTIC.md
- Datasheet.md — DEL-003-04_Exhaust-Plans/Datasheet.md
- Specification.md — DEL-003-04_Exhaust-Plans/Specification.md
- Guidance.md — DEL-003-04_Exhaust-Plans/Guidance.md
- Procedure.md — DEL-003-04_Exhaust-Plans/Procedure.md
- _REFERENCES.md — DEL-003-04_Exhaust-Plans/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 29
- By document:
  - Datasheet: 6
  - Specification: 11
  - Guidance: 5
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 6  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code editions TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Exhaust hose quantity unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ confirmation absent |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit pathway documented in Specification verification table and Procedure verification table |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Wash bay exhaust gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Step sequence is clear and actionable |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Quantitative pass criteria absent |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QC review and coordination log in Procedure Records table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value principles (source capture, zone isolation, cold climate) well articulated in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off table in Guidance covers key merit decisions |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Addressed via trade-off recommendations |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC review in Procedure Step 5.3 covers internal quality check |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicable Alberta Building Code edition and Alberta Safety Codes Act edition in effect at time of permitting; add specific clause references for exhaust system requirements | REQ-008 references code compliance but no specific code edition or clause is identified; all standards in Standards table carry "ASSUMPTION: likely applicable" with "full text not accessible" | Specification.md | REQ-008 — Code Compliance; Standards table | — | PROPOSAL: AHJ (Camrose County) to confirm code editions | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify minimum exhaust drop quantity per repair bay in REQ-001 (currently states "TBD (quantity per final design)" and assumption of "minimum of one exhaust drop per repair bay") | The mandatory practice of providing exhaust hoses per SOW-0038 is stated but the quantity is deferred entirely to assumptions; this could change implementation decisions | Specification.md | REQ-001 Notes | — | PROPOSAL: Mechanical Engineer to confirm per DEL-003-06 calculations | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-008 (Code Compliance) that do not depend solely on downstream permits (DEL-009-03) and inspections (DEL-009-04); add a pre-IFC code review check | Verification for REQ-008 relies entirely on safety code permits and inspection reports from other deliverables; there is no verification step within this deliverable's own review cycle | Specification.md | Verification table — REQ-008 row | — | PROPOSAL: Include a design-phase code review step in Procedure | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a procedural step or sub-step addressing wash bay exhaust system design; currently wash bay is identified as an exhaust source in Step 1.1 but has no corresponding system design step in Step 3 | Step 3.1 covers repair bays, welding station, service pit, and general fans but omits the wash bay exhaust/ventilation system, even though Step 1.1 explicitly lists wash bay as an exhaust source location | Procedure.md | Step 3 — System Design and Layout | — | PROPOSAL: Mechanical Engineer to confirm if wash bay exhaust is in scope of DEL-003-04 or DEL-003-02 | TBD |
| A-005 | A:operative:judging | MissingSlot | Procedure | Procedure | Add quantitative pass/fail criteria to the Procedure verification table (e.g., airflow tolerance, acceptable deviations from calculations) | Procedure verification checks use qualitative criteria ("no conflicts," "values identical," "no interferences") but do not specify acceptable tolerances or measurement methods for airflow/pressure verification | Procedure.md | Verification table | — | PROPOSAL: Mechanical Engineer to define acceptance tolerances | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service pit airflow TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | R-05 not fully reviewed |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Wash bay exhaust data absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements present are consistent across documents (ceiling height, bay width) |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Cross-deliverable dependencies clearly signalled |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context well-established in all four documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive within the accessible source constraints |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Engineering fundamentals well-represented in Guidance Principles |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise level is appropriate throughout |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Within accessible sources, knowledge coverage is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherently presented |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Service pit continuous-vs-demand ventilation unresolved |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls well-documented in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic perspective present |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential data for service pit ventilation: pit dimensions (depth, width, length), ventilation airflow rate requirement, and air changes per hour target | Service pit is identified as a ventilated space but no dimensional or airflow data is recorded in the Datasheet; these are essential facts for design | Datasheet.md | Exhaust System Components table — Service pit ventilation row | — | PROPOSAL: Mechanical Engineer to determine per DEL-003-06 and structural drawings DEL-002-06 | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Multi | Datasheet | Record TBD: Obtain and review R-05 App B-Elec (electrical conceptual drawing) in sufficient detail to confirm exhaust fan locations and quantities | R-05 is referenced but explicitly noted as "not accessible in sufficient detail" during drafting; this undermines data sufficiency for REQ-004 and general fan coordination | Datasheet.md; Specification.md | Datasheet — Exhaust Fans (general) row; Specification REQ-004 Notes | — | PROPOSAL: Electrical Engineer / DEL-004 team to provide | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add wash bay exhaust system component entry to the Exhaust System Components table (currently absent; only repair bays, welding station, service pit, general fans, and air exchanger are listed) | Wash bay is identified as an exhaust source in Datasheet Conditions table and Guidance Principle 3, but has no entry in the Exhaust System Components table | Datasheet.md | Exhaust System Components table | — | PROPOSAL: Confirm if wash bay exhaust is in DEL-003-04 scope vs. DEL-003-02 | TBD |
| B-004 | B:wisdom:necessity | WeakStatement | Guidance | Guidance | Strengthen the service pit ventilation trade-off entry: clarify what code research is needed and who will perform it; the current "TBD -- depends on Alberta OHS Code requirements" leaves the decision pathway undefined | The trade-off between continuous and demand-controlled service pit ventilation is left entirely open with no path to resolution identified beyond a generic code reference | Guidance.md | Trade-offs table — Service pit ventilation row | — | PROPOSAL: Mechanical Engineer + safety consultant to resolve | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Standard Grasp | 1 | HAS_ITEMS | Standards access gap |
| C:normative:sufficiency | normative | sufficiency | Regulatory Adequacy Proof | 0 | NO_ITEMS | Sufficiency is constrained by code-text access but correctly flagged |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 1 | HAS_ITEMS | Ceiling fan exhaust interaction |
| C:normative:consistency | normative | consistency | Harmonized Adherence Standard | 0 | NO_ITEMS | Standards references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Process Baseline | 0 | NO_ITEMS | Process baseline is established in Procedure |
| C:operative:sufficiency | operative | sufficiency | Proven Operational Fitness | 0 | NO_ITEMS | Procedure steps are sufficient for the defined scope |
| C:operative:completeness | operative | completeness | Comprehensive Process Integration | 1 | HAS_ITEMS | Commissioning gap |
| C:operative:consistency | operative | consistency | Stable Performance Coherence | 0 | NO_ITEMS | Procedure is internally consistent |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Awareness | 0 | NO_ITEMS | Merit awareness well-grounded in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Merit Judgment | 0 | NO_ITEMS | Trade-off judgments are warranted |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Assessment | 0 | NO_ITEMS | Value dimensions adequately covered |
| C:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Guidance | Guidance | Add a Guidance note explaining which specific ASHRAE 62.1 or Alberta OHS Code provisions are anticipated to govern exhaust system design, even if clause numbers are TBD; document the rationale for why each standard is assumed applicable | Multiple standards are listed as "ASSUMPTION: likely applicable" with no explanation of which specific provisions would apply to which exhaust subsystem; this leaves the compulsory standard grasp incomplete | Specification.md; Guidance.md | Specification Standards table; Guidance Principle 1, Principle 4 | — | PROPOSAL: Mechanical Engineer to document applicability rationale | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement or note addressing the interaction between the 6 ceiling fans (SOW-0040) and the exhaust system performance (air circulation patterns may affect exhaust capture efficiency at source) | Datasheet Conditions table lists "6 ceiling fans in main shop area (supplement air circulation)" but no requirement or consideration addresses how ceiling fan air movement interacts with exhaust capture systems, particularly the welding LEV and hose reel systems | Datasheet.md; Specification.md | Datasheet Conditions — Ceiling fans row; Specification entire document scanned | — | PROPOSAL: Mechanical Engineer to assess during design | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Specification | Add a requirement or procedural step for commissioning/functional testing of exhaust systems after installation (currently the Procedure ends at IFC issue with no commissioning verification) | Procedure covers design through IFC issue but does not address post-installation commissioning or functional performance verification, which is needed for comprehensive process integration from design through operational readiness (OBJ-004) | Procedure.md; Specification.md | Procedure entire document scanned; Specification Verification table | — | PROPOSAL: Commissioning may be covered by PKG-013 installation deliverables; confirm scope boundary | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Conformance Command | 1 | HAS_ITEMS | SOW cross-check gap |
| F:normative:sufficiency | normative | sufficiency | Validated Compliance Threshold | 1 | HAS_ITEMS | Airflow thresholds absent |
| F:normative:completeness | normative | completeness | Exhaustive Statutory Authority | 0 | NO_ITEMS | All RFP requirements traced; statutory completeness limited by code text access as noted |
| F:normative:consistency | normative | consistency | Uniform Statutory Alignment | 0 | NO_ITEMS | Statutory references are uniformly applied |
| F:operative:necessity | operative | necessity | Essential Execution Foresight | 1 | HAS_ITEMS | Makeup air coordination gap |
| F:operative:sufficiency | operative | sufficiency | Warranted Execution Capacity | 0 | NO_ITEMS | Execution capacity is sufficient given dependencies |
| F:operative:completeness | operative | completeness | Total Workflow Mastery | 0 | NO_ITEMS | Workflow is complete within deliverable scope |
| F:operative:consistency | operative | consistency | Systematic Execution Rigor | 0 | NO_ITEMS | Execution steps are systematic |
| F:evaluative:necessity | evaluative | necessity | Principled Merit Perception | 0 | NO_ITEMS | Merit well-grounded |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Measure | 0 | NO_ITEMS | Worth measures defensible |
| F:evaluative:completeness | evaluative | completeness | Whole Appraisal Authority | 1 | HAS_ITEMS | Guarantee period implications |
| F:evaluative:consistency | evaluative | consistency | Coherent Worth Reasoning | 0 | NO_ITEMS | Worth reasoning coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add a traceability check confirming all SOW items assigned to DEL-003-04 (SOW-0013, SOW-0028, SOW-0036, SOW-0038, SOW-0039, SOW-0040, SOW-0066) are addressed by at least one requirement | The Specification references SOW-0038, SOW-0039, SOW-0028, SOW-0066, SOW-0036 in various requirements but SOW-0013 (overall mechanical design) and SOW-0040 (ceiling fans) have no explicit requirement mapping; obligatory conformance requires complete SOW coverage | Specification.md; Datasheet.md | Specification Requirements section; Datasheet Identification — Covers SOW row | — | PROPOSAL: Add SOW traceability matrix | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add quantitative acceptance thresholds for airflow verification in the Verification table (e.g., "Airflow within +/-10% of DEL-003-06 calculated values" or equivalent) | Verification for REQ-001 through REQ-005 uses "drawing review" and "cross-reference" but never specifies what constitutes sufficient proof that the design meets airflow or capture velocity requirements | Specification.md | Verification table — REQ-001 through REQ-005 rows | — | PROPOSAL: Mechanical Engineer to define acceptance tolerances per applicable standards | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a step or sub-step in Step 3 for explicit coordination with the forced-air makeup air system (SOW-0037) to confirm exhaust/makeup air balance; currently only REQ-005 mentions coordination but no procedural action is assigned | Essential execution foresight requires that the makeup air balance is actively coordinated during design, not just stated as a requirement; Procedure Step 3 does not include a makeup air coordination sub-step | Procedure.md | Step 3 — System Design and Layout | — | PROPOSAL: Add sub-step 3.6 for makeup air balance verification | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a Guidance note addressing the 2-year guarantee period (Datasheet: "Construction period + 2 years post-CCC") and its implications for exhaust system material selection, durability, and maintainability | Datasheet records a 2-year guarantee period but no document discusses how this affects exhaust system design choices (e.g., corrosion resistance for wash bay exhaust, durability of flexible hoses, accessibility for maintenance) | Datasheet.md; Guidance.md | Datasheet Key Design Parameters — Guarantee period row; Guidance entire document scanned | — | PROPOSAL: Mechanical Engineer to address in Guidance or DEL-003-07 Specification | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Regulatory Directive | 0 | NO_ITEMS | Regulatory directives documented; resolution pending code confirmation |
| D:normative:applying | normative | applying | Enforced Sufficiency Rule | 0 | NO_ITEMS | Sufficiency rules present in requirements |
| D:normative:judging | normative | judging | Final Regulatory Finding | 0 | NO_ITEMS | Regulatory findings deferred to permitting appropriately |
| D:normative:reviewing | normative | reviewing | Confirmed Compliance Review | 0 | NO_ITEMS | Compliance review addressed |
| D:operative:guiding | operative | guiding | Resolved Execution Planning | 1 | HAS_ITEMS | Preliminary design gate unclear |
| D:operative:applying | operative | applying | Confirmed Production Delivery | 0 | NO_ITEMS | Production delivery pathway clear |
| D:operative:judging | operative | judging | Confirmed Capability Authority | 1 | HAS_ITEMS | Overhead crane clearance data |
| D:operative:reviewing | operative | reviewing | Confirmed Systematic Examination | 0 | NO_ITEMS | Systematic examination defined in Procedure verification table |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Compass | 0 | NO_ITEMS | Merit compass established in Guidance Principles |
| D:evaluative:applying | evaluative | applying | Confirmed Worth Realization | 0 | NO_ITEMS | Worth realization path clear |
| D:evaluative:judging | evaluative | judging | Final Merit Authority | 0 | NO_ITEMS | Merit authority deferred to engineering judgment appropriately |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Appraisal Rationale | 1 | HAS_ITEMS | Conflict on deliverable boundary |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Procedure | Procedure | Clarify the relationship between Step 3.5 and Step 4: Step 3.5 says "do not proceed to IFC until County approval" but Step 4 is titled "County Approval of Preliminary Design" and comes after Step 3; clarify whether Step 3.5 output is the preliminary design or whether Step 4 is a separate gate | The execution planning has an ambiguous gate: Step 3.5 appears to perform and gate on the same action that Step 4 then describes in detail; the sequencing could confuse the executing engineer | Procedure.md | Step 3.5; Step 4 | — | PROPOSAL: Restructure to make gate sequence unambiguous | TBD |
| D-002 | D:operative:judging | MissingSlot | Datasheet | Datasheet | Add overhead crane data (crane type, runway height, hook height) to the Datasheet Building Context or Key Design Parameters table; Procedure verification references "crane runway heights (5-tonne cranes, DEL-002-07)" but this data does not appear in the Datasheet | Confirmed capability authority requires that all design constraints used in verification are traceable to recorded data; crane clearance is a verification check but the crane data is not in the Datasheet | Procedure.md; Datasheet.md | Procedure Verification table — Overhead crane clearances row; Datasheet entire document scanned | — | PROPOSAL: Source from DEL-002-07 structural drawings | TBD |
| D-003 | D:evaluative:reviewing | Conflict | Multi | Guidance | Resolve the DEL-003-03 vs DEL-003-04 ductwork scope boundary: Guidance CFT-001 proposes DEL-003-04 covers "all exhaust-specific ductwork" but this assumption has no confirmed authority | Guidance CFT-001 identifies this conflict and proposes a resolution, but HumanRuling = TBD; this conflict affects appraisal of whether exhaust ductwork is complete within this deliverable or split across two | Guidance.md; Specification.md | Guidance Conflict Table CFT-001; Specification Scope — What This Deliverable Covers | Guidance.md#CFT-001 (DEL-003-03 scope) vs. Specification.md#Scope (DEL-003-04 scope) | PROPOSAL: Per Guidance CFT-001 proposal — DEL-003-04 covers exhaust-specific ductwork | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Authority Indicator | 1 | HAS_ITEMS | P.Eng. verification gap |
| X:guiding:sufficiency | guiding | sufficiency | Validated Counsel Scope | 0 | NO_ITEMS | Counsel scope validated in Guidance |
| X:guiding:completeness | guiding | completeness | Comprehensive Governance Authority | 0 | NO_ITEMS | Governance authority documented |
| X:guiding:consistency | guiding | consistency | Coherent Governance Alignment | 0 | NO_ITEMS | Governance alignment coherent |
| X:applying:necessity | applying | necessity | Vital Delivery Competence | 1 | HAS_ITEMS | Drawing sheet list not finalized |
| X:applying:sufficiency | applying | sufficiency | Warranted Delivery Threshold | 0 | NO_ITEMS | Delivery thresholds present |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Coordination record gap |
| X:applying:consistency | applying | consistency | Consistent Delivery Measure | 0 | NO_ITEMS | Delivery measures consistent |
| X:judging:necessity | judging | necessity | Decisive Conformance Basis | 1 | HAS_ITEMS | No independent airflow verification method |
| X:judging:sufficiency | judging | sufficiency | Validated Capability Finding | 0 | NO_ITEMS | Capability findings present |
| X:judging:completeness | judging | completeness | Comprehensive Ruling Account | 0 | NO_ITEMS | Ruling accounts documented |
| X:judging:consistency | judging | consistency | Stable Conformance Ruling | 0 | NO_ITEMS | Conformance ruling stable |
| X:reviewing:necessity | reviewing | necessity | Vital Examination Basis | 1 | HAS_ITEMS | Terminology inconsistency |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Examination Scope | 0 | NO_ITEMS | Examination scope warranted |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Record | 1 | HAS_ITEMS | No sign-off record requirement |
| X:reviewing:consistency | reviewing | consistency | Stable Examination Coherence | 0 | NO_ITEMS | Examination coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | VerificationGap | Specification | Procedure | Add a verification step confirming the P.Eng. reviewer has Alberta practice licence before stamping (REQ-006 requires Alberta licence but verification only says "Verify P.Eng. stamp and Alberta licence number on each drawing sheet" without specifying who checks or how licence validity is confirmed) | Foundational authority for IFC drawings rests on a valid P.Eng. stamp; the verification approach does not specify a licence validation method | Specification.md | Verification table — REQ-006 row | — | PROPOSAL: Add licence verification step to Procedure Step 6.1 | TBD |
| X-002 | X:applying:necessity | WeakStatement | Specification | Specification | Clarify that the "Required Artifacts" table in Specification Documentation section is the minimum deliverable list; currently the Procedure Step 5.1 has a more detailed sheet list marked "anticipated content -- actual sheet list determined by Mechanical Engineer" which may not match | The delivery competence requirement needs a clear minimum artifact list; the Specification lists 3 artifacts while Procedure lists 6 anticipated sheets, creating ambiguity about what constitutes a complete delivery | Specification.md; Procedure.md | Specification Documentation — Required Artifacts table; Procedure Step 5.1 | — | PROPOSAL: Align artifact lists or clarify that Procedure list is illustrative | TBD |
| X-003 | X:applying:completeness | VerificationGap | Procedure | Procedure | Add a requirement for a coordination record (log or sign-off) with each cross-discipline team (Electrical, Structural, Architectural) as a formal deliverable output, not just a verification check | Procedure verification checks coordination completeness but the Records table only lists "Coordination log" without specifying content requirements or sign-off format; exhaustive implementation requires formal coordination closure | Procedure.md | Procedure Verification table; Records table | — | PROPOSAL: Define coordination record format | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add a verification method for airflow performance that is independent of drawing review (e.g., reference to post-installation air balance testing per DEL-003-06 calculated values) | All verification approaches in the Specification are based on drawing review or cross-reference; there is no provision for confirming actual exhaust system performance, which is the decisive conformance basis | Specification.md | Verification table | — | PROPOSAL: May be covered by PKG-013 commissioning; confirm | TBD |
| X-005 | X:reviewing:necessity | Normalization | Multi | Guidance | Normalize terminology: "service pit" vs "Service Pit" — Datasheet and Specification alternate between these terms; adopt one and define the other as an alias | "Service pit" appears in Specification REQ-003 statement; "Service Pit" appears in Specification REQ-003 source text; "service pit/trench" used in Procedure Step 1.1; inconsistent terminology creates review ambiguity | Datasheet.md; Specification.md; Procedure.md | Datasheet Building Context — Service pit row; Specification REQ-003; Procedure Step 1.1 | — | PROPOSAL: Adopt "service pit" as primary term per RFP §3.4 wording | TBD |
| X-006 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add a formal sign-off record for the internal QC review (Step 5.3); currently listed as "Internal QC review sign-off" in Records but no sign-off template or format is specified in the Procedure steps | Exhaustive examination record requires that the QC review produces a documented artifact with defined content; the current Procedure describes QC checks but not the record format | Procedure.md | Procedure Step 5.3; Records table — Internal QC review sign-off row | — | PROPOSAL: Define QC sign-off format or reference PKG-019 QC template | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Basis | 0 | NO_ITEMS | Directive data basis is authoritative |
| E:guiding:information | guiding | information | Strategic Orientation Context | 1 | HAS_ITEMS | Cold climate design data absent |
| E:guiding:knowledge | guiding | knowledge | Strategic Governance Mastery | 0 | NO_ITEMS | Governance knowledge present |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Governance foresight demonstrated in Guidance |
| E:applying:data | applying | data | Validated Execution Record | 0 | NO_ITEMS | Execution record framework in place |
| E:applying:information | applying | information | Direct Implementation Context | 0 | NO_ITEMS | Implementation context clear |
| E:applying:knowledge | applying | knowledge | Validated Implementation Mastery | 0 | NO_ITEMS | Implementation knowledge adequate |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 1 | HAS_ITEMS | Energy efficiency consideration absent |
| E:judging:data | judging | data | Binding Adjudication Evidence | 0 | NO_ITEMS | Adjudication evidence framework present |
| E:judging:information | judging | information | Decisive Conformance Context | 0 | NO_ITEMS | Conformance context established |
| E:judging:knowledge | judging | knowledge | Validated Assessment Authority | 0 | NO_ITEMS | Assessment authority documented |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Insight | 0 | NO_ITEMS | Adjudication insight present |
| E:reviewing:data | reviewing | data | Verified Inspection Record | 1 | HAS_ITEMS | CFT-002 unresolved |
| E:reviewing:information | reviewing | information | Warranted Inspection Context | 0 | NO_ITEMS | Inspection context warranted |
| E:reviewing:knowledge | reviewing | knowledge | Validated Inspection Mastery | 0 | NO_ITEMS | Inspection mastery demonstrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 1 | HAS_ITEMS | Noise/vibration inspection absent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain winter design temperature for Ferintosh, Alberta from ASHRAE Fundamentals or Alberta Building Code climate data; add to Key Design Parameters table | Guidance Principle 5 identifies cold climate considerations as critical for exhaust termination design but no design temperature data is recorded anywhere in the production documents | Datasheet.md; Guidance.md | Datasheet Key Design Parameters table; Guidance Principle 5 | — | PROPOSAL: Source from ASHRAE Fundamentals Handbook or Alberta Building Code climate appendix | TBD |
| E-002 | E:applying:wisdom | RationaleGap | Guidance | Guidance | Add a consideration or trade-off entry addressing energy efficiency of exhaust systems (e.g., heat recovery from exhaust air, VFD on exhaust fans, demand-controlled ventilation for non-pit zones) given that the building is in a cold climate with significant heating costs | Principled execution foresight should address the energy implications of exhausting heated indoor air in a cold Alberta climate; the high-volume air exchanger (SOW-0036) implies heat recovery is valued but no exhaust-side energy consideration appears | Guidance.md | Guidance entire document scanned | — | PROPOSAL: Mechanical Engineer to address in Guidance Considerations or trade-offs | TBD |
| E-003 | E:reviewing:data | Conflict | Specification | Specification | Resolve Guidance CFT-002: exhaust fan locations and quantities from R-05 App B-Elec could not be verified against the mechanical scope; this creates a data gap in the verified inspection record for REQ-004 | Guidance CFT-002 identifies that R-05 was "not accessible in sufficient detail"; until this is resolved, verification of REQ-004 (general exhaust fans coordinated with electrical drawing) cannot produce a verified inspection record | Specification.md; Guidance.md | Specification REQ-004; Guidance Conflict Table CFT-002 | Specification.md#REQ-004 (mechanical fan scope) vs. R-05 App B-Elec (electrical fan placement — not fully reviewed) | PROPOSAL: Per Guidance CFT-002 — coordination meeting between Mechanical and Electrical Engineers | TBD |
| E-004 | E:reviewing:wisdom | Normalization | Specification | Specification | Add a note or requirement addressing exhaust fan noise and vibration considerations (exhaust fans in an industrial shop with 35 ft ceilings near occupied work zones); currently no production document addresses acoustic or vibration impact of exhaust equipment | Principled inspection foresight should consider that exhaust fans and ductwork generate noise and vibration; in a heavy-equipment shop this may not be critical but Alberta OHS Code may have occupational noise exposure requirements that interact with exhaust fan selection | Specification.md; Guidance.md | Specification entire document scanned; Guidance entire document scanned | — | PROPOSAL: Mechanical Engineer to assess whether noise/vibration is a design consideration for this facility type | TBD |
