# Semantic Lensing Register: DEL-004-08 Electrical Calculation Package

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-004_Electrical Design/1_Working/DEL-004-08_Calculation-Package/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-004-08_Calculation-Package/_CONTEXT.md
- _STATUS.md — DEL-004-08_Calculation-Package/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-004-08_Calculation-Package/_SEMANTIC.md
- Datasheet.md — DEL-004-08_Calculation-Package/Datasheet.md
- Specification.md — DEL-004-08_Calculation-Package/Specification.md
- Guidance.md — DEL-004-08_Calculation-Package/Guidance.md
- Procedure.md — DEL-004-08_Calculation-Package/Procedure.md
- _REFERENCES.md — DEL-004-08_Calculation-Package/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 12
  - Guidance: 4
  - Procedure: 6
  - Multi: 3
- By matrix:
  - A: 6  B: 5  C: 3  F: 3  D: 4  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 8
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | CEC edition unspecified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Welding receptacle assumption unconfirmed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Safety Code compliance path incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Audit trail for assumptions |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Service voltage not confirmed |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table covers major requirements |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QC review step adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance trade-offs section addresses value direction |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | Growth margin criteria undefined |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Add the specific CEC edition (Part I) adopted by Alberta at time of design to REQ-004-08-15, REQ-004-08-16, and the Standards table | Multiple requirements reference the CEC but the specific edition is recorded as "TBD by Electrical Engineer" throughout; without the edition, prescriptive direction cannot be anchored to an authoritative code text | Specification.md; Guidance.md | Specification.md#Standards; REQ-004-08-15; REQ-004-08-16; Guidance.md#Principles — Code Compliance is Non-Negotiable | | PROPOSAL: Electrical Engineer to confirm applicable CEC edition and update Specification Standards table | TBD |
| A-002 | A:normative:applying | Conflict | Multi | Specification | Resolve welding receptacle rating: 50 A / 240 V is an ASSUMPTION (D-009) pending County confirmation per RFP section 3.4 — clarify whether this is a mandatory practice value or a placeholder | The mandatory practice lens reveals that the 50 A / 240 V rating is treated as a design value across Datasheet and Specification but is explicitly flagged as an assumption awaiting County data; the documents use it as if confirmed while simultaneously marking it TBD | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Receptacles (note); Specification.md#REQ-004-08-08; Guidance.md#Conflict Table — CONF-004-08-02 | Datasheet.md#Receptacles vs. RFP section 3.4 (County to supply specs) | PROPOSAL: County to provide welding equipment specifications; Electrical Engineer to update all documents upon receipt | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add explicit compliance determination criteria for Alberta Safety Codes in the Verification table — currently REQ-004-08-18 verification is delegated to "Safety Code inspection and permit sign-off (administered via PKG-009)" with no internal acceptance criteria for this deliverable | Compliance determination lens shows that the calculation package itself has no self-contained check for code compliance beyond deferring to PKG-009; the deliverable should define what "adheres to all applicable Alberta Safety Codes" means in testable terms for its own QC step | Specification.md | Specification.md#Verification — REQ-004-08-18 row | | PROPOSAL: Add internal acceptance criterion such as "all CEC clause references recorded for each sizing calculation" as a pre-PKG-009 check | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or checklist item for tracking assumptions through to resolution (audit trail) — the Procedure flags assumptions but does not define a formal review gate where assumptions must be resolved or accepted before IFC stamp | Regulatory audit lens reveals that assumptions (welding ampacity, wash bay wattage, crane data, overhead door data) are flagged throughout but there is no procedural checkpoint where all open assumptions are formally reviewed and accepted/resolved before IFC release | Procedure.md | Procedure.md#Steps — Step 10 (P.Eng. Stamp and IFC Release); Step 8.3; Step 8.4 | | PROPOSAL: Add a formal assumption resolution gate between Step 9 (QC Review) and Step 10 (IFC Release) requiring sign-off that all ASSUMPTION items are resolved or formally accepted as design assumptions | TBD |
| A-005 | A:operative:applying | TBD_Question | Procedure | Procedure | Confirm three-phase service voltage with utility provider — Step 2.2 identifies this as a required action but Status column is not tracked in Prerequisites and no deadline or responsible party for utility confirmation is stated | Practical execution lens shows that the service voltage (120/208 V vs. 347/600 V) affects every calculation in the package but there is no mechanism to ensure this critical input is obtained before calculations proceed | Procedure.md | Procedure.md#Steps — Step 2.2; Step 2.1 (ASSUMPTION note) | | PROPOSAL: Add utility voltage confirmation to Prerequisites table with responsible party and target date | TBD |
| A-006 | A:evaluative:judging | WeakStatement | Guidance | Guidance | Clarify growth margin criterion — "adding growth margin increases upfront cost but reduces future upgrade expense" is directional but does not state a recommended range or decision framework | Worth determination lens reveals that the trade-off for service entrance sizing margin lacks evaluative criteria; Procedure Step 4.1 states "minimum growth margin" with "typical practice 20-25%" as assumption, but Guidance does not commit to a recommended approach | Guidance.md; Procedure.md | Guidance.md#Trade-offs — Service entrance sizing margin; Procedure.md#Steps — Step 4.1 | | PROPOSAL: Add recommended growth margin range or decision framework to Guidance Trade-offs section, referencing Owner consultation requirement | TBD |

---

## Matrix B — Conceptualization (4x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Crane electrical data missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Overhead door data gap |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Exhaust fan data incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Stated values are internally consistent where provided |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Hazardous area classification |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology normalization needed |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Multi | Datasheet | Add crane manufacturer electrical data (motor FLA, voltage, phases, duty cycle) to Datasheet once obtained — currently flagged as TBD across all four documents | Essential fact lens identifies that crane electrical data is the single most critical missing data point; it affects service entrance sizing, dedicated circuit calculations, voltage drop, and panel schedules; all documents consistently flag this gap but the Datasheet has no placeholder row for the specific data fields expected | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet.md#Dedicated Equipment Circuits — crane row; Specification.md#REQ-004-08-09; Guidance.md#Considerations — Crane Power Feeds; Procedure.md#Prerequisites — Crane manufacturer data | | PROPOSAL: Add structured placeholder rows in Datasheet for crane FLA, voltage, phases, and duty cycle; coordinate with PKG-016 | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add overhead door operator electrical data (quantity, ampacity per unit) as structured Datasheet entries — currently only an assumption of "15-20 A / 120 V" in Specification with no Datasheet record | Adequate evidence lens reveals that overhead door power is mentioned in Specification REQ-004-08-10 and Procedure but the Datasheet does not enumerate the quantity of overhead doors or record the assumed operator rating; this data gap could lead to under-sizing | Datasheet.md; Specification.md | Datasheet.md#Dedicated Equipment Circuits (no overhead door row); Specification.md#REQ-004-08-10 | | PROPOSAL: Add overhead door entry to Datasheet with quantity TBD and assumed rating; coordinate with DEL-001-07 | TBD |
| B-003 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Clarify exhaust fan data — Datasheet states "Quantity/placement: TBD" and Specification states "Quantity and wattage TBD"; neither document records even an assumed wattage range for planning purposes | Comprehensive record lens reveals exhaust fans are the least-specified electrical load in the package; unlike ceiling fans (which at least have a count of 6) or overhead doors (which have an assumed ampacity), exhaust fans have no count, no wattage, and no assumed value | Datasheet.md; Specification.md | Datasheet.md#Exhaust Fans; Specification.md#REQ-004-08-13 | | PROPOSAL: Coordinate with PKG-003 Mechanical Design to obtain exhaust fan count and motor data; record planning assumptions in Datasheet | TBD |
| B-004 | B:information:necessity | MissingSlot | Specification | Guidance | Add hazardous area classification determination for service pit — Procedure Step 5.5 mentions potential need for explosion-proof fixtures but no requirement or guidance exists for performing the classification assessment | Essential signal lens identifies that the service pit may require hazardous area classification under CEC rules (potential flammable vapors from vehicle maintenance); this classification affects fixture type selection and circuit design but is not mentioned in Specification requirements or Guidance considerations beyond a parenthetical note | Procedure.md; Specification.md | Procedure.md#Steps — Step 5.5; Specification.md#REQ-004-08-06 | | PROPOSAL: Add to Guidance Considerations a note on hazardous area classification for the service pit; add to Specification a requirement that the Electrical Engineer shall determine whether hazardous area classification applies | TBD |
| B-005 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology for the building name — documents use "Maintenance Shop Addition," "New North Shop," "maintenance shop" interchangeably | Coherent message lens reveals that the building is referred to as "West Dried Meat Lake Regional Landfill Maintenance Shop Addition" (Specification, Guidance, Procedure) and "New North Shop" (Specification scope section, Datasheet) without establishing which is the canonical name for the electrical calculation package context | Specification.md; Datasheet.md | Specification.md#Scope — "New North Shop" in parenthetical; Datasheet.md#Identification — "Project" field | | PROPOSAL: Establish canonical building name in Guidance or Datasheet and use consistently | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Basis | 1 | HAS_ITEMS | CEC clause traceability |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy Standard | 0 | NO_ITEMS | Requirements define adequate scope |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Lighting standard gap |
| C:normative:consistency | normative | consistency | Prescriptive Uniformity | 0 | NO_ITEMS | Requirements are consistent where stated |
| C:operative:necessity | operative | necessity | Core Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table is comprehensive |
| C:operative:sufficiency | operative | sufficiency | Verified Operational Capacity | 0 | NO_ITEMS | |
| C:operative:completeness | operative | completeness | Comprehensive Process Scope | 1 | HAS_ITEMS | Mechanical coordination scope |
| C:operative:consistency | operative | consistency | Repeatable Process Fidelity | 0 | NO_ITEMS | |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Criterion | 0 | NO_ITEMS | |
| C:evaluative:sufficiency | evaluative | sufficiency | Sufficient Quality Demonstration | 0 | NO_ITEMS | |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | |
| C:evaluative:consistency | evaluative | consistency | Stable Value Integrity | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add CEC clause references to each requirement — requirements cite RFP and Appendix B but not the specific CEC clauses that govern the calculation methodology | Compulsory compliance basis lens reveals that while REQ-004-08-15 and REQ-004-08-16 reference "applicable Canadian Electrical Code," no requirement specifies which CEC sections/clauses govern each calculation type (e.g., Section 8 for conductor sizing, Section 40 for cranes); without clause references, the compliance basis is incomplete | Specification.md | Specification.md#Requirements — REQ-004-08-15; REQ-004-08-16; Standards table | | PROPOSAL: Electrical Engineer to populate CEC clause references once the applicable edition is confirmed | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add illuminance standard reference (IES or equivalent) to Standards table — currently listed as "ASSUMPTION: may apply" with no commitment | Total regulatory coverage lens shows that the Specification Standards table lists "IEC/ANSI lighting standards for industrial facilities" as "ASSUMPTION: may apply" but lighting calculations (REQ-004-08-03 through REQ-004-08-06) require an illuminance target; without a committed standard, the adequacy of lighting calculations cannot be verified against a normative benchmark | Specification.md; Guidance.md | Specification.md#Standards — IEC/ANSI row; Guidance.md#Examples — IES methodology reference | | PROPOSAL: Electrical Engineer to confirm applicable illuminance standard and move from ASSUMPTION to confirmed in Standards table | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add explicit mechanical coordination step for forced-air makeup air unit (MUA) — Guidance mentions SOW-0037 and Procedure Step 1.4 lists coordination with Mechanical for "heating system, makeup air unit, exhaust fans, ceiling fans" but the connected load schedule in Step 3.1 separately lists "Forced-air makeup air unit (per mechanical data — TBD)" and "Heating system (per mechanical data — TBD)" without a clear cross-reference to which SOWs or deliverables provide this data | Comprehensive process scope lens reveals that the mechanical-electrical coordination pathway for MUA and heating loads is stated in Steps 1.4 and 3.1 but there is no corresponding entry in the Prerequisites table for heating system data (only "Mechanical equipment electrical data" generically) and no requirement in Specification for heating/MUA circuit sizing | Procedure.md; Specification.md | Procedure.md#Prerequisites; Procedure.md#Steps — Step 1.4, Step 3.1; Specification.md#Requirements (no heating/MUA requirement) | | PROPOSAL: Add REQ for heating/MUA circuit sizing to Specification; add heating system data as distinct Prerequisites entry with source PKG-003 | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Proof Imperative | 1 | HAS_ITEMS | Demand factor documentation |
| F:normative:sufficiency | normative | sufficiency | Qualified Conformance Benchmark | 0 | NO_ITEMS | |
| F:normative:completeness | normative | completeness | Exhaustive Code Command | 0 | NO_ITEMS | Covered by C-001 |
| F:normative:consistency | normative | consistency | Harmonized Conformance Logic | 1 | HAS_ITEMS | Voltage drop limit inconsistency |
| F:operative:necessity | operative | necessity | Essential Capability Validation | 0 | NO_ITEMS | |
| F:operative:sufficiency | operative | sufficiency | Baseline Capability Assurance | 0 | NO_ITEMS | |
| F:operative:completeness | operative | completeness | Total Workflow Command | 0 | NO_ITEMS | |
| F:operative:consistency | operative | consistency | Principled Workflow Harmony | 0 | NO_ITEMS | |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Recognition | 0 | NO_ITEMS | |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Appraisal | 1 | HAS_ITEMS | IP rating justification |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Inventory | 0 | NO_ITEMS | |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Calibration | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add requirement that demand factor basis shall be documented for each load category — Procedure Step 3.2 states "Document the demand factor basis" but no corresponding requirement exists in Specification | Mandatory proof imperative lens reveals that demand factor application is a critical CEC compliance element and the calculation package's professional credibility depends on transparent demand factor documentation; Procedure directs this but Specification does not require it as a deliverable attribute | Specification.md; Procedure.md | Specification.md#Requirements (no demand factor requirement); Procedure.md#Steps — Step 3.2 | | PROPOSAL: Add REQ requiring documented demand factor basis for each load category | TBD |
| F-002 | F:normative:consistency | Normalization | Procedure | Multi | Harmonize voltage drop limit expression — Procedure Step 7.1 states "typically 3% on feeders, 5% total" but qualifies with "specific limits per current CEC edition, location TBD"; Specification REQ-004-08-15 says "compliance with applicable code limits" without stating the limits | Harmonized conformance logic lens reveals a potential for inconsistency: the Procedure provides a typical value (3%/5%) that may differ from the actual CEC edition requirements; if the adopted CEC edition specifies different limits, the Procedure guidance could mislead | Procedure.md; Specification.md | Procedure.md#Steps — Step 7.1; Specification.md#REQ-004-08-15 | | PROPOSAL: Once CEC edition is confirmed, update both documents with the actual code-specified voltage drop limits | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for wash bay fixture IP rating selection in Trade-offs — IP65 vs. IP66/IP67 trade-off is listed but no guidance on how to decide; the wash bay serves large vehicles with high-pressure wash and the IP rating affects both cost and maintenance | Justified worth appraisal lens shows that the IP rating decision has cost and maintenance implications but the Guidance does not provide a decision framework beyond stating the trade-off exists; the Electrical Engineer needs guidance on what factors should drive the selection | Guidance.md | Guidance.md#Trade-offs — Wash bay lighting IP rating | | PROPOSAL: Add decision criteria (e.g., wash pressure expected, maintenance access, cost threshold) to help the Electrical Engineer justify the selected IP rating | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Conclusive Directive Authority | 0 | NO_ITEMS | |
| D:normative:applying | normative | applying | Enforced Performance Standard | 1 | HAS_ITEMS | Illuminance acceptance criteria |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Covered by A-003 |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Assurance | 0 | NO_ITEMS | |
| D:operative:guiding | operative | guiding | Confirmed Workflow Guidance | 1 | HAS_ITEMS | Revision linkage |
| D:operative:applying | operative | applying | Established Task Delivery | 0 | NO_ITEMS | |
| D:operative:judging | operative | judging | Confirmed Operational Proficiency | 0 | NO_ITEMS | |
| D:operative:reviewing | operative | reviewing | Systematic Procedural Alignment | 1 | HAS_ITEMS | Drawing cross-reference mechanism |
| D:evaluative:guiding | evaluative | guiding | Principled Quality Direction | 0 | NO_ITEMS | |
| D:evaluative:applying | evaluative | applying | Grounded Quality Realization | 1 | HAS_ITEMS | 40-year facility life consideration |
| D:evaluative:judging | evaluative | judging | Comprehensive Value Judgment | 0 | NO_ITEMS | |
| D:evaluative:reviewing | evaluative | reviewing | Rigorous Merit Verification | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add quantitative illuminance acceptance criteria for lighting requirements REQ-004-08-03 through REQ-004-08-06 — currently the verification method is "Illuminance calculation output review" with no stated target lux/foot-candle value | Enforced performance standard lens reveals that lighting requirements specify fixture counts and wattages but do not state what illuminance level constitutes adequate performance; the Procedure directs the engineer to determine per IES but the Specification has no acceptance threshold to verify against | Specification.md | Specification.md#Requirements — REQ-004-08-03, REQ-004-08-04, REQ-004-08-05, REQ-004-08-06; Specification.md#Verification — lighting rows | | PROPOSAL: Add minimum illuminance targets (or require the Electrical Engineer to establish and document them before calculation) for each lighting zone | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on calculation-to-drawing revision linkage — Guidance Principles states "Revisions to drawings must trigger corresponding revision to calculations" but does not explain the mechanism or timing | Confirmed workflow guidance lens reveals that while the principle of revision linkage is stated, there is no operational guidance on how to implement it (e.g., revision numbering scheme, cross-reference table format, trigger criteria for re-calculation) | Guidance.md | Guidance.md#Principles — Calculation Package as Living Document | | PROPOSAL: Add a paragraph explaining the expected revision linkage mechanism and timing relative to drawing revisions | TBD |
| D-003 | D:operative:reviewing | WeakStatement | Procedure | Procedure | Strengthen drawing cross-reference requirement in Step 8.2 — currently states "Cross-reference each calculation section to the corresponding drawing using the drawing number and revision" but does not specify a format or tracking mechanism | Systematic procedural alignment lens shows that the cross-reference instruction is procedurally clear but lacks specificity on the expected output format (table, header notation, appendix); given that 6 downstream deliverables consume this package, a structured cross-reference mechanism would improve traceability | Procedure.md | Procedure.md#Steps — Step 8.2 | | PROPOSAL: Specify a cross-reference table format in the calculation package template | TBD |
| D-004 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Expand 40-year facility consideration to address electrical system lifecycle implications — Guidance mentions "40-Year Facility: Alberta Climate" but focuses on heating and lighting with no mention of electrical equipment longevity, panel replacement cycles, or conductor insulation lifespan | Grounded quality realization lens shows that the 40-year horizon is acknowledged but its implications for electrical design decisions (conductor oversizing for thermal cycling, panel board spare capacity, equipment accessibility for replacement) are not explored | Guidance.md | Guidance.md#Considerations — 40-Year Facility: Alberta Climate | | PROPOSAL: Add electrical lifecycle considerations to the 40-year facility section addressing conductor longevity, panel accessibility, and equipment replacement access | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Binding Foundational Mandate | 0 | NO_ITEMS | |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Authoritative Steering | 1 | HAS_ITEMS | 8-foot LED wattage assumption range |
| X:guiding:completeness | guiding | completeness | Total Directive Documentation | 0 | NO_ITEMS | |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Accuracy | 0 | NO_ITEMS | |
| X:applying:necessity | applying | necessity | Required Execution Evidence | 1 | HAS_ITEMS | Panel configuration documentation |
| X:applying:sufficiency | applying | sufficiency | Competent Performance Evidence | 0 | NO_ITEMS | |
| X:applying:completeness | applying | completeness | Exhaustive Performance Record | 0 | NO_ITEMS | |
| X:applying:consistency | applying | consistency | Dependable Execution Measure | 0 | NO_ITEMS | |
| X:judging:necessity | judging | necessity | Binding Assessment Threshold | 1 | HAS_ITEMS | Short circuit rating |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 0 | NO_ITEMS | |
| X:judging:sufficiency | judging | sufficiency | Qualified Adjudication Evidence | 0 | NO_ITEMS | |
| X:judging:consistency | judging | consistency | Consistent Adjudication Logic | 0 | NO_ITEMS | |
| X:reviewing:necessity | reviewing | necessity | Critical Audit Evidence | 1 | HAS_ITEMS | Input log as audit evidence |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Inspection Framing | 0 | NO_ITEMS | |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Documentation | 0 | NO_ITEMS | |
| X:reviewing:consistency | reviewing | consistency | Dependable Audit Coherence | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Specification | Datasheet | Tighten 8-foot LED fixture wattage assumption — REQ-004-08-05 states "ASSUMPTION: ~60-80 W each" which is a 33% range; for load schedule purposes this range is too broad to produce a single connected load value | Sufficient authoritative steering lens shows that the assumed wattage range for office/utility/parts room fixtures spans 60-80 W, which creates ambiguity in the connected load schedule; the Electrical Engineer should narrow this to a single planning value or document the conservative (high) assumption | Specification.md | Specification.md#REQ-004-08-05 | | PROPOSAL: Adopt 80 W as the conservative planning value or narrow assumption based on product selection; record in Datasheet | TBD |
| X-002 | X:applying:necessity | MissingSlot | Specification | Specification | Add requirement for panel configuration documentation — Procedure Step 4.4 directs determination of panel arrangement but no Specification requirement captures this as a deliverable output | Required execution evidence lens shows that the panel board configuration (number of panels, main vs. sub-panel arrangement) is a significant design output that feeds DEL-004-06 directly, but it appears only as a procedural step, not as a required deliverable element | Specification.md; Procedure.md | Specification.md#Requirements (no panel configuration requirement); Procedure.md#Steps — Step 4.4 | | PROPOSAL: Add REQ for panel configuration determination and documentation as a calculation package output | TBD |
| X-003 | X:judging:necessity | MissingSlot | Specification | Specification | Add short-circuit current / available fault current consideration — the calculation package addresses load sizing and voltage drop but does not mention short-circuit analysis or equipment interrupting ratings | Binding assessment threshold lens reveals that overcurrent protection device selection (REQ-004-08-16) requires knowledge of available fault current to ensure devices have adequate interrupting capacity; this is a standard CEC requirement for service entrance design that is absent from both Specification and Procedure | Specification.md; Procedure.md | Specification.md#Requirements (absent); Procedure.md#Steps (absent) | | PROPOSAL: Add REQ for available fault current determination at service entrance and verification that overcurrent devices are rated accordingly | TBD |
| X-004 | X:reviewing:necessity | Normalization | Procedure | Procedure | Standardize the term "Input Log" — Procedure Step 1.7 introduces "Input Log" and Step 8.3/8.4 introduces "Assumptions and Open Items register" as apparently distinct documents; clarify whether these are the same or different artifacts | Critical audit evidence lens shows that the calculation package audit trail depends on clear identification of tracking artifacts; the Procedure introduces two similar-sounding documents without clarifying their relationship, which could lead to duplication or omission | Procedure.md | Procedure.md#Steps — Step 1.7; Step 8.3; Step 8.4 | | PROPOSAL: Clarify in Procedure whether the Input Log and Assumptions/Open Items register are distinct documents or sections of the same artifact | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Evidentiary Basis | 0 | NO_ITEMS | |
| E:guiding:information | guiding | information | Comprehensive Steering Clarity | 1 | HAS_ITEMS | Mezzanine loads |
| E:guiding:knowledge | guiding | knowledge | Sovereign Professional Mastery | 0 | NO_ITEMS | |
| E:guiding:wisdom | guiding | wisdom | Holistic Governance Vision | 0 | NO_ITEMS | |
| E:applying:data | applying | data | Complete Execution Record | 0 | NO_ITEMS | |
| E:applying:information | applying | information | Actionable Work Narrative | 0 | NO_ITEMS | |
| E:applying:knowledge | applying | knowledge | Skilled Execution Mastery | 0 | NO_ITEMS | |
| E:applying:wisdom | applying | wisdom | Prudent Execution Awareness | 0 | NO_ITEMS | |
| E:judging:data | judging | data | Definitive Judgment Record | 1 | HAS_ITEMS | Conflict on heating system |
| E:judging:information | judging | information | Decisive Verdict Framing | 0 | NO_ITEMS | |
| E:judging:knowledge | judging | knowledge | Qualified Verdict Mastery | 0 | NO_ITEMS | |
| E:judging:wisdom | judging | wisdom | Holistic Verdict Prudence | 0 | NO_ITEMS | |
| E:reviewing:data | reviewing | data | Complete Inspection Record | 1 | HAS_ITEMS | Verification table gap |
| E:reviewing:information | reviewing | information | Framed Oversight Narrative | 0 | NO_ITEMS | |
| E:reviewing:knowledge | reviewing | knowledge | Qualified Oversight Mastery | 0 | NO_ITEMS | |
| E:reviewing:wisdom | reviewing | wisdom | Holistic Oversight Prudence | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | WeakStatement | Datasheet | Specification | Clarify mezzanine electrical load scope — Datasheet Construction section mentions "overhead mezzanine above parts room, utility room, and wash bay — electrical loads to be accounted for" but no Specification requirement addresses mezzanine-specific loads (lighting, receptacles, or equipment above the mezzanine) | Comprehensive steering clarity lens reveals that the mezzanine is identified as having electrical loads in the Datasheet but neither the Specification requirements nor the Procedure load schedule itemize what those loads are; the mezzanine area likely needs its own lighting and possibly receptacle circuits | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Construction — Mezzanine row; Specification.md#Requirements (no mezzanine requirement); Procedure.md#Steps — Step 3.1 (no mezzanine line item) | | PROPOSAL: Add mezzanine electrical loads as a distinct line item in the Specification requirements and Procedure load schedule | TBD |
| E-002 | E:judging:data | Conflict | Specification | Specification | Heating system and forced-air makeup air unit appear in Procedure Step 3.1 load schedule but have no corresponding Specification requirement — the Procedure directs calculation of loads for which no requirement exists | Definitive judgment record lens reveals a gap between what the Procedure directs the engineer to calculate (heating, MUA loads) and what the Specification requires; this creates a judgment inconsistency where the Procedure scope exceeds the Specification scope | Specification.md; Procedure.md | Specification.md#Requirements (absent for heating/MUA); Procedure.md#Steps — Step 3.1 (lists heating and MUA); Procedure.md#Steps — Step 1.4 (coordination with Mechanical) | Specification.md#Scope vs. Procedure.md#Steps — Step 3.1 | PROPOSAL: Add heating/MUA circuit requirements to Specification to match Procedure scope, or explicitly exclude from Specification with rationale | TBD |
| E-003 | E:reviewing:data | VerificationGap | Specification | Specification | Add verification row for conductor/conduit sizing per circuit — Specification Verification table has a row for "All circuit conductors and protection sized per CEC" but this is a single aggregate check; individual circuit verification (branch, feeder, sub-feeder) is not itemized | Complete inspection record lens shows that the Verification table aggregates all conductor sizing into a single check, which may not provide adequate granularity for the P.Eng. QC review; the Procedure breaks this into separate steps (Step 6.1-6.4) but the Specification verification does not mirror this granularity | Specification.md; Procedure.md | Specification.md#Verification — "All circuit conductors" row; Procedure.md#Steps — Step 6.1, 6.2, 6.3, 6.4; Procedure.md#Verification — "All circuit conductors and protection sized per CEC" | | PROPOSAL: Consider breaking Specification verification into branch circuit, feeder, and dedicated equipment sub-checks to match Procedure granularity | TBD |

---

## Structural Matrices (K, G, T) — Coverage Note

Matrices K, G, and T are structural transforms (transposes and truncations) of matrices D, B, and B respectively. Their cell values are inherited from the source matrices and do not introduce new semantic content. Per the CHIRALITY_FRAMEWORK, these matrices serve algebraic construction purposes (K and G are inputs to Matrix X; T is an input to Matrix E). Lensing is performed on the derived matrices X and E rather than on the structural intermediates, as the derived matrices capture the full semantic integration.

All cells of K, G, and T are accounted for through the lensing of their derived products (X and E).
