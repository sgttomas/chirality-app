# Semantic Lensing Register: DEL-013-03 Forced-Air Makeup System

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-03_Makeup-Air/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-013-03_Makeup-Air/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements, Related Deliverables)
- _STATUS.md — DEL-013-03_Makeup-Air/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-013-03_Makeup-Air/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-013-03_Makeup-Air/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-013-03_Makeup-Air/Specification.md (Scope, Requirements REQ-013-03-01 through -12, Standards, Verification, Documentation)
- Guidance.md — DEL-013-03_Makeup-Air/Guidance.md (Purpose, Principles P1-P5, Considerations C1-C6, Trade-offs T1-T3)
- Procedure.md — DEL-013-03_Makeup-Air/Procedure.md (Prerequisites PRE-01 through -11, Steps Phases 1-6, Verification, Records)
- _REFERENCES.md — DEL-013-03_Makeup-Air/_REFERENCES.md (Primary References R-01, R-04; Related Documentation; Drawing References; Standard References; Approval Documents)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 3  F: 5  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 7
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Makeup air scope source ambiguity (RFP 3.4 vs App B) |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code-specific installation standards not enumerated |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ inspection criteria not specified beyond pass/fail |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit trail addressed in Procedure records |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Vibration isolation treated as assumption, not directive |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure phases well-structured with clear execution steps |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative acceptance thresholds for pressurization |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure covers audit trail adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose and Principles articulate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section covers merit-based decision points |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table links to requirements adequately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality checks present in Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Guidance | Clarify whether forced-air makeup is a named RFP section 3.4 design requirement or derives solely from App B. Record human ruling on CFT-013-03-01. | Guidance.md Conflict Table already flags this (CFT-013-03-01) but the Specification scope statement does not acknowledge the ambiguity. A prescriptive-direction lens reveals a gap in how the normative authority for this deliverable is grounded. | Guidance.md, Specification.md | Guidance.md#Conflict Table; Specification.md#Scope | Guidance.md CFT-013-03-01 (App B source) vs RFP section 3.4 (omission) | App B as co-governing source (PROPOSAL per Guidance CFT-013-03-01) | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add explicit reference to specific Alberta mechanical code sections or ASHRAE clauses governing MUA installation (e.g., ASHRAE 62.1 minimum ventilation rates, Alberta Building Code Part 6 HVAC provisions). Currently Standards table lists applicable codes at a high level without specific section references. | Under a mandatory-practice lens, practitioners need specific code section references to confirm compliance, not just general code names. | Specification.md | Specification.md#Standards | — | Mechanical Engineer / AHJ (PROPOSAL) | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen REQ-013-03-03 acceptance criterion from "No excessive pressurization; controls respond correctly" to include a measurable pressure differential threshold (e.g., Pa range) or reference to design specification. | "Excessive" is subjective. Under a compliance-determination lens, the absence of a numeric or referenced threshold makes pass/fail determination ambiguous. | Specification.md | Specification.md#Verification (REQ-013-03-03 row) | — | Mechanical Engineer (PROPOSAL) | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Elevate Step 3.1 vibration isolation from ASSUMPTION to a prerequisite confirmed against manufacturer requirements. Add a check to confirm vibration isolation is specified in DEL-003-07 or manufacturer manual. | Vibration isolation is flagged as an assumption in parenthetical text. Under a procedural-direction lens, this should be a directed requirement confirmed from the manufacturer's installation manual, not left as optional. | Procedure.md | Procedure.md#Phase 3, Step 3.1 | — | MUA Manufacturer Installation Manual (PROPOSAL) | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for REQ-013-03-03 pressurization check (e.g., maximum allowable pressure differential in Pa at overhead door locations). Currently criterion is "No excessive pressurization" without a measurable threshold. | Performance-assessment lens requires measurable criteria. The Specification verification table and Procedure Step 5.6 both lack a numeric target for the pressurization check. | Specification.md, Procedure.md | Specification.md#Verification (REQ-013-03-03); Procedure.md#Phase 5, Step 5.6 | — | Mechanical Engineer / DEL-003-06 Calculation Package (PROPOSAL) | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Airflow rate (CFM/L/s) not yet established |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence basis adequate for current project stage; TBDs acknowledged |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Equipment location not recorded |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement approaches consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key integration signals identified in Dependencies |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate given design-build stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Comprehensive across 4 documents |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency: MUA vs makeup air unit |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles capture fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise assumptions reasonable for mechanical contractor |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage thorough for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs section captures essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Decision deferral to mechanical engineer is adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view covered via Guidance considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: What is the required MUA supply airflow rate (CFM or L/s)? Source: DEL-003-06 Mechanical Calculation Package. This is the essential design fact that drives equipment selection, duct sizing, and heating capacity. | Under an essential-fact lens, the single most critical data point — the design airflow rate — is TBD across all four documents. While acknowledged as TBD pending DEL-003-06, the Datasheet should explicitly register this as a blocking TBD with the source to resolve it. | Datasheet.md | Datasheet.md#Capacity & Performance ("Required supply volume: TBD") | — | DEL-003-06 Mechanical Calculation Package (PROPOSAL) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add design outdoor air temperature for heating sizing (Alberta design conditions). This parameter is referenced implicitly in REQ-013-03-05 and Guidance P2 but never recorded as a Datasheet attribute. | Under a comprehensive-record lens, the outdoor design temperature is a fundamental MUA sizing parameter that should appear in the Datasheet alongside the airflow rate TBD. Its absence means heating capacity cannot be independently verified. | Datasheet.md, Specification.md | Datasheet.md#Capacity & Performance (absent); Specification.md#REQ-013-03-05 ("Alberta cold-climate design conditions") | — | DEL-003-06 or ASHRAE climate data (PROPOSAL) | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: documents use "MUA", "makeup air unit", "forced-air makeup", "makeup air system", and "forced-air makeup air system" interchangeably. Establish a canonical term and abbreviation in Guidance or Datasheet vocabulary section. | Under a coherent-message lens, terminology drift across documents creates potential for misinterpretation, especially in integration contexts with other deliverables. The Datasheet uses "MUA" as a designation but the term is not consistently applied. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | Datasheet.md#Equipment ("MUA"); Specification.md#Scope ("MUA"); Guidance.md title ("Forced-Air Makeup System"); Procedure.md#Purpose ("forced-air makeup air (MUA)") | — | Datasheet equipment designation (PROPOSAL) | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Baseline Obligation | 1 | HAS_ITEMS | Minimum ventilation rate obligation not grounded in specific standard |
| C:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Threshold | 0 | NO_ITEMS | Regulatory thresholds deferred to design phase appropriately |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 1 | HAS_ITEMS | Fire/smoke damper requirements absent |
| C:normative:consistency | normative | consistency | Harmonized Compliance Regime | 0 | NO_ITEMS | Compliance references consistent across documents |
| C:operative:necessity | operative | necessity | Core Operational Capability | 0 | NO_ITEMS | Core capabilities well-defined in Specification requirements |
| C:operative:sufficiency | operative | sufficiency | Competent Execution Assurance | 0 | NO_ITEMS | Procedure provides competent execution guidance |
| C:operative:completeness | operative | completeness | Exhaustive Process Fulfillment | 1 | HAS_ITEMS | Filter maintenance/replacement not in Procedure |
| C:operative:consistency | operative | consistency | Standardized Operational Discipline | 0 | NO_ITEMS | Procedure steps follow consistent format and discipline |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Significance | 0 | NO_ITEMS | Value significance articulated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Assessment | 0 | NO_ITEMS | Merit assessment adequate for design-build context |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Appraisal | 0 | NO_ITEMS | Trade-offs provide worth appraisal framework |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add specific minimum outdoor air ventilation rate requirement per ASHRAE 62.1 or Alberta Building Code for the facility's occupancy classification. REQ-013-03-04 requires "adequate quality" but does not cite a minimum ventilation standard. | Under an Enforceable Baseline Obligation lens, the normative baseline for air quality (REQ-013-03-04) lacks a citable enforceable standard. "Adequate quality" is not enforceable without a referenced minimum ventilation rate. | Specification.md | Specification.md#REQ-013-03-04; Specification.md#Standards (ASHRAE 62.1 listed as "ASSUMPTION: likely applicable") | — | ASHRAE 62.1 or Alberta Building Code mechanical provisions (PROPOSAL) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add fire/smoke damper requirements for ductwork penetrating fire-rated assemblies. No mention of fire dampers appears in any production document, yet supply ductwork routes through multiple spaces likely separated by fire-rated construction. | Under a Total Compliance Coverage lens, fire/smoke damper requirements are a standard code obligation for HVAC ductwork penetrating rated assemblies. Their complete absence from all four documents is a compliance gap. | Specification.md, Procedure.md | Specification.md (entire document scanned — no mention of fire dampers); Procedure.md (entire document scanned — no mention) | — | Alberta Building Code fire separation requirements; mechanical engineer (PROPOSAL) | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a step or prerequisite for intake filter installation and initial filter specification, and note filter maintenance schedule in closeout/O&M section. Step 6.3 mentions filter maintenance in training but no filter installation step exists in Phases 2-4. | Under an Exhaustive Process Fulfillment lens, intake filtration is implicitly assumed (Step 6.3 references "Filter maintenance schedule") but no step installs the filters, no filter spec is referenced, and no acceptance criterion exists for filter installation. | Procedure.md | Procedure.md#Phase 6, Step 6.3 ("Filter maintenance schedule (ASSUMPTION: MUA unit has intake filters)"); Procedure.md Phases 2-4 (absence) | — | MUA manufacturer manual / DEL-003-07 (PROPOSAL) | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Foundation | 1 | HAS_ITEMS | P.Eng. stamp requirement not cross-referenced to Specification |
| F:normative:sufficiency | normative | sufficiency | Validated Conformance Adequacy | 1 | HAS_ITEMS | No hold/witness points defined for AHJ inspections |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Accounting | 0 | NO_ITEMS | Regulatory accounting adequate for current stage |
| F:normative:consistency | normative | consistency | Coherent Prescriptive Alignment | 0 | NO_ITEMS | Prescriptive requirements aligned across documents |
| F:operative:necessity | operative | necessity | Irreducible Procedural Baseline | 1 | HAS_ITEMS | Duct leakage testing absent |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Execution Readiness | 0 | NO_ITEMS | Execution readiness prerequisites well-structured |
| F:operative:completeness | operative | completeness | Total Procedural Accounting | 1 | HAS_ITEMS | Condensate drain requirement absent |
| F:operative:consistency | operative | consistency | Systematic Execution Coherence | 0 | NO_ITEMS | Procedure steps systematically coherent |
| F:evaluative:necessity | evaluative | necessity | Irreducible Merit Criterion | 0 | NO_ITEMS | Merit criteria present in verification table |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Threshold | 1 | HAS_ITEMS | Supply air temperature acceptance threshold missing |
| F:evaluative:completeness | evaluative | completeness | Conclusive Value Accounting | 0 | NO_ITEMS | Value accounting adequate through verification matrix |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Alignment | 0 | NO_ITEMS | Quality alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Specification | Guidance | Add rationale explaining why REQ-013-03-10 requires P.Eng.-stamped IFC drawings specifically for this deliverable's installation, and how this relates to the design-build delivery model where the contractor's engineer produces the drawings. The requirement is stated but the rationale for enforcement is implicit. | Under a Mandatory Compliance Foundation lens, the P.Eng. stamp requirement in REQ-013-03-10 is stated as mandatory but the Guidance document does not explain the regulatory basis (Alberta Safety Codes Act requirement for engineered systems) or how it interacts with the design-build model. | Specification.md, Guidance.md | Specification.md#REQ-013-03-10; Guidance.md#P5 (partial — mentions P.Eng. stamp but as procedural, not rationale) | — | Alberta Safety Codes Act / APEGA regulations (PROPOSAL) | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Procedure | Procedure | Define hold points and witness points for AHJ inspections in Procedure Phase 5. Step 5.2 says "Request and obtain" inspections but does not specify which installation stages require inspection holds (e.g., rough-in inspection before concealment, final inspection before commissioning). | Under a Validated Conformance Adequacy lens, the Procedure lacks mandatory hold points that would prevent work from proceeding past a required inspection. This risks ductwork concealment before rough-in inspection. | Procedure.md | Procedure.md#Phase 5, Step 5.2 | — | AHJ requirements for Camrose County jurisdiction (PROPOSAL) | TBD |
| F-003 | F:operative:necessity | MissingSlot | Specification | Specification | Add a requirement for duct leakage testing per applicable standard (e.g., SMACNA leakage class). No duct leakage testing requirement exists in Specification or Procedure, yet supply ductwork integrity is fundamental to system performance. | Under an Irreducible Procedural Baseline lens, duct leakage testing is a standard industry practice for supply air systems that directly affects system performance (airflow delivery to terminals). Its complete absence is a procedural gap. | Specification.md, Procedure.md | Specification.md (entire document scanned — no duct leakage test requirement); Procedure.md Phase 5 (no duct leakage test step) | — | SMACNA duct construction standards / mechanical engineer (PROPOSAL) | TBD |
| F-004 | F:operative:completeness | MissingSlot | Specification | Specification | Add requirement for condensate management (drain pan, drain line) for the MUA heating coil, particularly for shoulder-season operation where cooling of moist intake air could produce condensation. Datasheet and Specification are silent on condensate. | Under a Total Procedural Accounting lens, condensate management is a standard element for MUA units with heating coils operating in cold climates. Its absence from all documents means there is no installation guidance for drain connections. | Specification.md, Datasheet.md | Specification.md (entire document scanned); Datasheet.md#Equipment (no condensate reference) | — | MUA manufacturer manual / DEL-003-07 (PROPOSAL) | TBD |
| F-005 | F:evaluative:sufficiency | VerificationGap | Specification | Specification | Add a quantitative acceptance threshold for supply air temperature in REQ-013-03-05 verification (e.g., minimum supply air temperature in degrees C at design outdoor conditions). Current criterion is "Supply air at or above design temperature" without stating what the design temperature is. | Under a Defensible Quality Threshold lens, the supply air temperature acceptance criterion references "design temperature" but no design temperature is specified in any document. Without a numeric target, the verification is not defensible. | Specification.md | Specification.md#Verification (REQ-013-03-05 row: "Supply air at or above design temperature before entering occupied space") | — | DEL-003-06 Calculation Package / mechanical engineer (PROPOSAL) | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Prescriptive Course | 0 | NO_ITEMS | Prescriptive course established through requirements and Guidance principles |
| D:normative:applying | normative | applying | Compulsory Adequacy Enactment | 1 | HAS_ITEMS | Owner training not in Specification requirements |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 0 | NO_ITEMS | Verification table provides conformance determination framework |
| D:normative:reviewing | normative | reviewing | Mandated Alignment Examination | 0 | NO_ITEMS | Alignment examination addressed through AHJ inspection and commissioning |
| D:operative:guiding | operative | guiding | Established Operational Pathway | 0 | NO_ITEMS | Operational pathway well-defined in Procedure phases |
| D:operative:applying | operative | applying | Confirmed Task Delivery | 0 | NO_ITEMS | Task delivery confirmed through verification table |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 1 | HAS_ITEMS | No integrated system performance test requirement |
| D:operative:reviewing | operative | reviewing | Settled Operational Examination | 0 | NO_ITEMS | Operational examination covered by commissioning report |
| D:evaluative:guiding | evaluative | guiding | Purposeful Quality Direction | 0 | NO_ITEMS | Quality direction established in Guidance principles |
| D:evaluative:applying | evaluative | applying | Confirmed Quality Enactment | 0 | NO_ITEMS | Quality enactment addressed through submittal review and TAB |
| D:evaluative:judging | evaluative | judging | Definitive Worth Verdict | 0 | NO_ITEMS | Worth verdict framework present through CCC and commissioning |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Examination | 1 | HAS_ITEMS | No post-occupancy performance review mentioned |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add a requirement for Owner/facilities staff training on MUA system operation and maintenance. Procedure Step 6.3 includes training as a closeout step, but no corresponding requirement exists in Specification. | Under a Compulsory Adequacy Enactment lens, the Procedure delivers training (Step 6.3) but the Specification does not mandate it as a requirement. This means training could be omitted without violating Specification requirements. | Specification.md, Procedure.md | Specification.md#Requirements (absent); Procedure.md#Phase 6, Step 6.3 | — | OBJ-004 / Owner expectations (PROPOSAL) | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add an integrated system performance test requirement that verifies MUA operation in conjunction with DEL-013-01 (heating), DEL-013-02 (air exchanger), DEL-013-04 (equipment exhaust), and DEL-013-05 (welding exhaust) operating simultaneously. Procedure Step 5.6 partially addresses this but it is not a formal Specification requirement. | Under a Conclusive Performance Verdict lens, the MUA system's performance can only be conclusively verified when all interacting ventilation systems operate simultaneously. REQ-013-03-09 covers controls integration but no requirement mandates a full integrated system test. | Specification.md, Procedure.md | Specification.md#Requirements (REQ-013-03-09 partial); Procedure.md#Phase 5, Step 5.6 (partial — pressurization check only) | — | Mechanical Engineer / commissioning specification (PROPOSAL) | TBD |
| D-003 | D:evaluative:reviewing | RationaleGap | Guidance | Guidance | Add a consideration for post-commissioning performance monitoring or seasonal performance review. The system operates under varying conditions (winter heating load vs. shoulder season) and a single commissioning test may not capture all operating modes. | Under a Resolved Merit Examination lens, the Guidance document does not address how the system's merit/worth will be evaluated after initial commissioning. Given Alberta's extreme seasonal variation, a single-point commissioning test may not demonstrate year-round performance. | Guidance.md | Guidance.md#Considerations (absent); Guidance.md#Trade-offs (no seasonal performance mention) | — | Owner / commissioning authority (PROPOSAL) | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Directional Truth | 1 | HAS_ITEMS | Wash bay area unclear in distribution scope |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Guidance Capacity | 0 | NO_ITEMS | Guidance capacity adequate for current design stage |
| X:guiding:completeness | guiding | completeness | Total Directional Mastery | 0 | NO_ITEMS | Directional coverage complete across Guidance sections |
| X:guiding:consistency | guiding | consistency | Coherent Directional Stability | 0 | NO_ITEMS | Directional guidance consistent across documents |
| X:applying:necessity | applying | necessity | Compulsory Delivery Realization | 1 | HAS_ITEMS | Electrical disconnect requirement scattered |
| X:applying:sufficiency | applying | sufficiency | Validated Implementation Proficiency | 0 | NO_ITEMS | Implementation guidance sufficient for mechanical contractor |
| X:applying:completeness | applying | completeness | Comprehensive Fulfillment Inventory | 0 | NO_ITEMS | Fulfillment inventory complete in Procedure steps |
| X:applying:consistency | applying | consistency | Harmonized Delivery Reliability | 0 | NO_ITEMS | Delivery steps consistent and sequenced |
| X:judging:necessity | judging | necessity | Binding Determination Finding | 1 | HAS_ITEMS | REQ-013-03-04 verification method insufficient |
| X:judging:sufficiency | judging | sufficiency | Substantiated Adjudication Basis | 0 | NO_ITEMS | Adjudication basis adequate through verification table |
| X:judging:completeness | judging | completeness | Total Adjudication Accounting | 1 | HAS_ITEMS | No verification for ductwork insulation requirement |
| X:judging:consistency | judging | consistency | Coherent Adjudication Stability | 0 | NO_ITEMS | Adjudication criteria consistent across verification items |
| X:reviewing:necessity | reviewing | necessity | Compulsory Oversight Foundation | 0 | NO_ITEMS | Oversight foundation present through AHJ and engineer review |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Oversight Adequacy | 0 | NO_ITEMS | Oversight adequacy addressed through commissioning report |
| X:reviewing:completeness | reviewing | completeness | Total Oversight Accounting | 1 | HAS_ITEMS | Warranty period obligations absent |
| X:reviewing:consistency | reviewing | consistency | Coherent Oversight Uniformity | 0 | NO_ITEMS | Oversight uniformity maintained across verification items |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | WeakStatement | Specification | Specification | Clarify in REQ-013-03-06 whether "all facility areas" explicitly includes the wash bay, as the wash bay has unique ventilation requirements (moisture, drainage) that may affect MUA distribution design. Datasheet lists wash bay in ASSUMPTION parenthetical but Specification does not confirm. | Under a Cardinal Directional Truth lens, the scope of "all facility areas" in REQ-013-03-06 is ambiguous regarding the wash bay. The Datasheet includes "wash bay" in a parenthetical assumption, but the Specification requirement does not enumerate the served areas, creating directional uncertainty for duct design. | Specification.md, Datasheet.md | Specification.md#REQ-013-03-06 ("all facility areas"); Datasheet.md#Capacity & Performance ("ASSUMPTION: includes main shop, repair bays, welding area, wash bay") | — | Mechanical design drawings / DEL-003-02 (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | Normalization | Procedure | Multi | Consolidate electrical disconnect requirement. Procedure Step 4.2 mentions "Disconnect switch located per code" but this is embedded in the electrical connection step. Consider adding disconnect switch as a Datasheet equipment attribute and a Specification requirement for lockout/tagout provisions. | Under a Compulsory Delivery Realization lens, the electrical disconnect is a safety-critical installation element mentioned only in passing within one Procedure step. It warrants a normative requirement in Specification and a recorded attribute in Datasheet. | Procedure.md, Datasheet.md, Specification.md | Procedure.md#Phase 4, Step 4.2; Datasheet.md#Equipment (absent); Specification.md#Requirements (absent) | — | Alberta Electrical Code / Alberta OHS (PROPOSAL) | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen REQ-013-03-04 verification method from "Intake location inspection; visual confirmation" to include intake separation distance measurement from exhaust outlets per applicable standard or engineering specification. Visual confirmation alone is insufficient for a safety-critical air quality requirement. | Under a Binding Determination Finding lens, the verification method for air quality (REQ-013-03-04) relies solely on visual inspection ("Intake location free of contamination sources"). This is insufficient to make a binding determination about intake-exhaust separation adequacy. | Specification.md | Specification.md#Verification (REQ-013-03-04 row) | — | ASHRAE 62.1 or mechanical engineer intake separation analysis (PROPOSAL) | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification row for ductwork insulation. Step 3.6 in Procedure installs insulation per DEL-003-07, but no Specification requirement or verification criterion exists for insulation type, thickness, or vapor barrier. | Under a Total Adjudication Accounting lens, ductwork insulation is installed in Procedure Step 3.6 but has no corresponding Specification requirement and no verification criterion. Insulation quality directly affects condensation prevention and energy performance. | Specification.md, Procedure.md | Specification.md#Verification (absent); Procedure.md#Phase 3, Step 3.6 | — | DEL-003-07 Mechanical Specification / energy code (PROPOSAL) | TBD |
| X-005 | X:reviewing:completeness | MissingSlot | Specification | Specification | Add warranty period and deficiency correction obligations to Documentation or a new Warranty section. No production document addresses post-commissioning warranty obligations or deficiency liability period. | Under a Total Oversight Accounting lens, the oversight cycle is incomplete without warranty provisions. The RFP likely contains warranty requirements (common in design-build contracts per CCDC 14), but no production document for this deliverable references a warranty period or deficiency correction obligation. | Specification.md | Specification.md#Documentation (absent); Specification.md (entire document scanned) | — | CCDC 14-2013 contract terms / RFP (PROPOSAL) | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record well-established with source citations |
| E:guiding:information | guiding | information | Coherent Advisory Intelligence | 1 | HAS_ITEMS | No noise/acoustic guidance for MUA unit |
| E:guiding:knowledge | guiding | knowledge | Authoritative Directional Mastery | 0 | NO_ITEMS | Directional mastery adequate in Guidance principles |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 0 | NO_ITEMS | Foresight captured in trade-offs section |
| E:applying:data | applying | data | Substantiated Delivery Record | 0 | NO_ITEMS | Delivery record framework established in Procedure records table |
| E:applying:information | applying | information | Coherent Execution Intelligence | 0 | NO_ITEMS | Execution intelligence adequate in Procedure steps |
| E:applying:knowledge | applying | knowledge | Proficient Delivery Mastery | 0 | NO_ITEMS | Delivery expertise appropriate for qualified mechanical contractor |
| E:applying:wisdom | applying | wisdom | Principled Delivery Foresight | 0 | NO_ITEMS | Delivery foresight addressed through prerequisites and sequencing |
| E:judging:data | judging | data | Substantiated Verdict Record | 1 | HAS_ITEMS | CCC issuance criteria not specified |
| E:judging:information | judging | information | Coherent Adjudication Intelligence | 0 | NO_ITEMS | Adjudication intelligence present in verification table |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Mastery | 0 | NO_ITEMS | Adjudication expertise deferred to engineer and AHJ appropriately |
| E:judging:wisdom | judging | wisdom | Principled Determination Foresight | 0 | NO_ITEMS | Determination foresight addressed through commissioning approach |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 0 | NO_ITEMS | Audit record framework in Procedure records table |
| E:reviewing:information | reviewing | information | Coherent Examination Intelligence | 0 | NO_ITEMS | Examination intelligence adequate |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Examination Mastery | 0 | NO_ITEMS | Examination competence deferred to qualified parties |
| E:reviewing:wisdom | reviewing | wisdom | Principled Examination Foresight | 1 | HAS_ITEMS | Lessons learned / continuous improvement absent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | RationaleGap | Guidance | Guidance | Add a consideration for MUA unit noise and acoustic impact on the occupied shop space. Large MUA units can generate significant noise; acoustic treatment, duct silencers, or unit placement considerations may be warranted for worker comfort and communication safety. | Under a Coherent Advisory Intelligence lens, the Guidance document addresses thermal, air quality, pressurization, and sequencing concerns but omits acoustic impact. In a 35' high-bay shop with overhead cranes, MUA noise is a practical consideration for worker safety (communication near equipment). | Guidance.md | Guidance.md#Considerations (absent — no acoustic/noise consideration) | — | Mechanical engineer / occupational health standards (PROPOSAL) | TBD |
| E-002 | E:judging:data | WeakStatement | Specification | Specification | Clarify CCC (Construction Completion Certificate) issuance criteria in Documentation table. Currently listed as "Owner-issued CCC upon final inspection acceptance" but does not specify what constitutes final inspection acceptance or who signs off. | Under a Substantiated Verdict Record lens, the CCC is the final deliverable acceptance artifact but its issuance criteria are vaguely stated. The Documentation table references "final inspection acceptance" without specifying whether this means AHJ sign-off, Owner witness test, commissioning report acceptance, or all of the above. | Specification.md | Specification.md#Documentation (CCC row: "Owner-issued CCC upon final inspection acceptance") | — | RFP section 2.14.3 / Owner (PROPOSAL) | TBD |
| E-003 | E:reviewing:wisdom | TBD_Question | Guidance | Guidance | TBD: Does the Owner (Camrose County) require a lessons-learned or performance feedback mechanism for major mechanical systems post-commissioning? If so, add a consideration in Guidance for how the MUA system's actual performance should be evaluated against design intent after the first heating season. | Under a Principled Examination Foresight lens, no document addresses how the MUA system will be evaluated for long-term adequacy after project closeout. Given TBD design parameters and multiple assumptions, a post-installation performance review could validate or correct design decisions. | Guidance.md | Guidance.md (entire document scanned — no post-commissioning review consideration) | — | Owner / project delivery requirements (PROPOSAL) | TBD |
