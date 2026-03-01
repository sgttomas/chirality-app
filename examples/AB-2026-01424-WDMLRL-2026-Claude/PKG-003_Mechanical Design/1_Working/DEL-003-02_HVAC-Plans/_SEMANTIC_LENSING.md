# Semantic Lensing Register: DEL-003-02 HVAC Layout Plans

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-003_Mechanical Design/1_Working/DEL-003-02_HVAC-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-003-02_HVAC-Plans/_CONTEXT.md
- _STATUS.md — DEL-003-02_HVAC-Plans/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-003-02_HVAC-Plans/_SEMANTIC.md
- Datasheet.md — DEL-003-02_HVAC-Plans/Datasheet.md
- Specification.md — DEL-003-02_HVAC-Plans/Specification.md
- Guidance.md — DEL-003-02_HVAC-Plans/Guidance.md
- Procedure.md — DEL-003-02_HVAC-Plans/Procedure.md
- _REFERENCES.md — DEL-003-02_HVAC-Plans/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 12
  - Guidance: 3
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Applicable codes listed as ASSUMPTION without confirmation |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp practice clear; code application scope weak |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Compliance verification method relies on P.Eng. review without explicit acceptance criteria for code-specific items |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 7 and Step 8 address review adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | CAD/BIM tooling referenced but no firm-specific standard identified |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure addresses performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal QA checklist (Step 7) and P.Eng. review (Step 8) in place |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit statement of how layout quality is measured beyond completeness |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance trade-off tables address merit of design options |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table provides pass criteria |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA checklist in Procedure addresses quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicability of ASHRAE 62.1, ASHRAE 90.1, AMCA 210, and CSA W117.2 to this project; obtain Alberta-specific code edition references | Multiple standards listed as "ASSUMPTION: applicable; location TBD" without confirmed applicability; prescriptive direction requires confirmed regulatory basis | Specification.md | Standards table | — | Mechanical Engineer / Authority Having Jurisdiction | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify what "all applicable Alberta Building Codes, regulations, and Alberta Safety Codes" means by listing specific code sections that govern HVAC layout for industrial occupancy | REQ-008 uses broad language "all applicable" without identifying specific code sections, making mandatory practice ambiguous for compliance checking | Specification.md | REQ-008 — Code Compliance | — | Mechanical Engineer | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for code compliance verification beyond "drawing notes to reference applicable codes; engineer's stamp confirms compliance" | REQ-008 verification relies solely on P.Eng. stamp and drawing notes; no checklist of specific code provisions to verify against | Specification.md | Verification table, REQ-008 row | — | Mechanical Engineer | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add reference to firm-specific CAD/BIM standards or note that firm standards are external to this deliverable set | Procedure lists "Firm's HVAC drawing standards / CAD standards" as a required reference but no further detail exists in any document; practical execution depends on this input | Procedure.md | Prerequisites — Tools and Resources | — | Mechanical Engineer | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add a statement on how layout quality is evaluated beyond system completeness (e.g., constructability, maintainability, clarity of drawing communication) | Guidance provides design rationale and trade-offs but does not address what constitutes a high-quality layout from the Owner's or constructor's perspective | Guidance.md | Purpose | — | Mechanical Engineer | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key design parameters remain TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Outdoor design temperature missing |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Operating hours and occupant count absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Stated values (dimensions, fan count) are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW traceability present throughout |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided in Guidance principles |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All seven system types accounted for across documents |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for heating system |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance provides adequate domain knowledge context |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-off discussion in Guidance demonstrates competent framing |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage across all system types is thorough |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is internally consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance principles demonstrate appropriate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off tables show adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-discipline coordination addressed in Guidance and Procedure |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain air exchanger volume/capacity, MUA capacity, equipment exhaust fan size/quantity, and service pit ventilation type from Mechanical Engineer (DEL-003-06) | Multiple essential system parameters listed as TBD in Datasheet; these are necessary facts for layout production | Datasheet.md | System Parameters table | — | Mechanical Engineer / DEL-003-06 | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain outdoor design temperature for Alberta central region (climate data) and occupant count | Outdoor design temperature and occupancy count are listed as TBD; adequate evidence for HVAC sizing depends on these values | Datasheet.md | Operating Environment table | — | Mechanical Engineer / Climate data source | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add operating hours for the maintenance shop facility | Operating hours listed as TBD with no source; comprehensive record requires this for ventilation rate determination | Datasheet.md | Operating Environment table | — | Owner (Camrose County) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: "high-recovery heating system" vs. "high recovery heating system" vs. "heat-recovery unit heaters" — adopt one canonical term and define it | Datasheet uses "High-recovery heating system", Specification uses "high-recovery heating system", Guidance uses "high recovery heating system" and also introduces "heat-recovery unit heaters" as an interpretation; inconsistent naming risks drift | Datasheet.md, Specification.md, Guidance.md | Datasheet: HVAC Systems table; Specification: REQ-001; Guidance: P-2 | — | Mechanical Engineer | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforced Foundational Standard | 1 | HAS_ITEMS | Foundational code standards not yet confirmed |
| C:normative:sufficiency | normative | sufficiency | Certified Prescriptive Adequacy | 0 | NO_ITEMS | Specification provides adequate prescriptive structure |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 1 | HAS_ITEMS | Mezzanine ventilation requirement not in Specification |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references consistent where stated |
| C:operative:necessity | operative | necessity | Essential Operational Capability | 0 | NO_ITEMS | Procedure captures essential workflow |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Working Competence | 0 | NO_ITEMS | Steps are sufficiently detailed |
| C:operative:completeness | operative | completeness | Total Operational Mastery | 0 | NO_ITEMS | Procedure covers full workflow from input to IFC issue |
| C:operative:consistency | operative | consistency | Reliable Process Uniformity | 0 | NO_ITEMS | Process steps are logically sequenced and consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Guidance Purpose section articulates deliverable value |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Standing | 0 | NO_ITEMS | Trade-offs and considerations provide adequate justification |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Assessment | 1 | HAS_ITEMS | No discussion of energy efficiency value implications |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning is internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-008 by specifying the edition year or version of applicable codes (e.g., "National Building Code of Canada 2020 Alberta Edition") rather than "location TBD" | The enforced foundational standard cannot be fully grounded when the specific code editions are not identified; "location TBD" appears for multiple codes | Specification.md | REQ-008 — Code Compliance; Standards table | — | Mechanical Engineer / AHJ | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement for mezzanine ventilation (referenced in Guidance C-5 as potentially requiring ventilation per safety codes for stored petroleum products) | Guidance C-5 identifies mezzanine ventilation as a potential safety code requirement; Specification has no corresponding REQ for mezzanine ventilation | Specification.md, Guidance.md | Specification: entire Requirements section scanned; Guidance: C-5 Mezzanine Ventilation | — | Mechanical Engineer | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add discussion of energy efficiency implications of HVAC layout decisions (referenced standard ASHRAE 90.1 is listed but no energy efficiency rationale appears in Guidance) | ASHRAE 90.1 is listed as an applicable standard but no Guidance principle or consideration addresses energy efficiency trade-offs for layout decisions | Guidance.md, Specification.md | Guidance: entire document scanned; Specification: Standards table (ASHRAE 90.1 row) | — | Mechanical Engineer | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Compliance Baseline | 1 | HAS_ITEMS | Baseline incomplete without confirmed code editions |
| F:normative:sufficiency | normative | sufficiency | Qualified Regulatory Acceptance | 0 | NO_ITEMS | P.Eng. stamp pathway provides adequate acceptance route |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Mastery | 1 | HAS_ITEMS | Confined space regulation for service pit not identified |
| F:normative:consistency | normative | consistency | Disciplined Compliance Alignment | 0 | NO_ITEMS | Compliance references are aligned where stated |
| F:operative:necessity | operative | necessity | Fundamental Performance Requirement | 1 | HAS_ITEMS | No requirement for air curtain / vestibule heating at overhead doors |
| F:operative:sufficiency | operative | sufficiency | Capable Working Sufficiency | 0 | NO_ITEMS | Procedure provides capable working pathway |
| F:operative:completeness | operative | completeness | Complete Functional Coverage | 0 | NO_ITEMS | Functional systems coverage is complete (7 systems + wash bay) |
| F:operative:consistency | operative | consistency | Systematic Operational Coherence | 0 | NO_ITEMS | Operational steps are coherent and sequenced |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 0 | NO_ITEMS | Quality checks present in Procedure verification |
| F:evaluative:sufficiency | evaluative | sufficiency | Competent Worth Justification | 0 | NO_ITEMS | Guidance trade-offs justify design approach |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 1 | HAS_ITEMS | No quality metric for drawing legibility or scale adequacy |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality approach consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify whether Alberta Occupational Health and Safety (OHS) regulations for confined spaces apply to the service pit ventilation design and, if so, add as a normative reference | REQ-007 requires service pit ventilation but does not cite confined space regulations; Guidance P-5 flags this as "confined-space-adjacent" requiring forced ventilation; authoritative compliance baseline requires the applicable regulation to be identified | Specification.md, Guidance.md | Specification: REQ-007; Guidance: P-5 | — | Mechanical Engineer / AHJ | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add a requirement or TBD for identifying the specific Alberta confined space ventilation regulation applicable to the service pit | Guidance P-5 references "Alberta confined space ventilation requirements (ASSUMPTION: applicable code — location TBD)" but no Specification requirement captures this normative obligation | Specification.md, Guidance.md | Specification: entire Requirements section; Guidance: P-5 | — | Mechanical Engineer / AHJ | TBD |
| F-003 | F:operative:necessity | MissingSlot | Specification | Specification | Add requirement or design decision placeholder for air curtains or vestibule heating at overhead door locations (referenced as TBD in Guidance C-2) | Guidance C-2 identifies overhead door infiltration as a significant design issue and mentions air curtains as a possible provision; no Specification requirement addresses this; if air curtains are required they must appear on the HVAC layout | Specification.md, Guidance.md | Specification: entire Requirements section; Guidance: C-2 | — | Mechanical Engineer | TBD |
| F-004 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add verification criteria for drawing scale suitability and drawing legibility (REQ-011 says "Drawing scale suitable for construction use" but verification is only "reviewer confirms completeness") | REQ-011 includes drawing scale as a requirement but no measurable acceptance criterion exists for scale suitability; exhaustive quality accounting requires measurable verification | Specification.md | REQ-011 — Drawing Set Completeness; Verification table, REQ-011 row | — | Mechanical Engineer | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandate pathway clear (P.Eng. stamp + code compliance) |
| D:normative:applying | normative | applying | Settled Compulsory Practice | 1 | HAS_ITEMS | Gas supply discipline boundary unsettled |
| D:normative:judging | normative | judging | Conclusive Regulatory Ruling | 0 | NO_ITEMS | Regulatory ruling pathway through P.Eng. review is established |
| D:normative:reviewing | normative | reviewing | Formal Compliance Assurance | 0 | NO_ITEMS | P.Eng. stamp and County approval provide assurance pathway |
| D:operative:guiding | operative | guiding | Directed Functional Priority | 0 | NO_ITEMS | Functional priorities stated in Guidance principles |
| D:operative:applying | operative | applying | Settled Practical Delivery | 1 | HAS_ITEMS | Preliminary design approval gate unclear |
| D:operative:judging | operative | judging | Conclusive Performance Evaluation | 0 | NO_ITEMS | Verification table provides evaluation framework |
| D:operative:reviewing | operative | reviewing | Settled Process Verification | 0 | NO_ITEMS | Procedure verification checks are settled |
| D:evaluative:guiding | evaluative | guiding | Settled Value Priority | 0 | NO_ITEMS | Value priorities established through Guidance |
| D:evaluative:applying | evaluative | applying | Demonstrated Quality Enactment | 1 | HAS_ITEMS | Coordination sign-off mechanism not specified |
| D:evaluative:judging | evaluative | judging | Conclusive Value Determination | 0 | NO_ITEMS | Verification criteria provide value determination basis |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Assurance | 0 | NO_ITEMS | QA checklist and P.Eng. review provide assurance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Resolve gas supply piping discipline boundary: is gas piping within the building Mechanical (PKG-003) or Plumbing (PKG-006) scope? | Guidance CONF-003 explicitly flags this as an unresolved conflict; compulsory practice cannot be settled until the scope boundary is declared | Guidance.md, Specification.md | Guidance: Conflict Table CONF-003; Specification: Scope Exclusions table | Guidance.md#Conflict Table CONF-003, Specification.md#What This Deliverable Excludes | Mechanical Engineer + Plumbing Engineer / Project Manager | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Procedure | Add a verification check or hold point confirming that DEL-003-01 (Preliminary Mechanical Design) County approval has been received before Step 2 proceeds to IFC-level work | Procedure Step 1 describes confirming County approval but the verification table does not include a pass criterion for this gate; practical delivery depends on this upstream approval | Procedure.md | Steps: Step 1; Verification table | — | Project Manager | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Procedure | Procedure | Add a defined format or template for the coordination review comment log (Procedure Step 5) to ensure discipline sign-offs are recorded consistently | Procedure Step 5 mentions "coordination review comment log" but no format or required fields are specified; demonstrated quality enactment requires a traceable coordination record | Procedure.md | Steps: Step 5; Records table | — | Mechanical Engineer | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Mandated Guidance Foundation | 0 | NO_ITEMS | Guidance foundation adequately established |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Directive Evidence | 0 | NO_ITEMS | RFP and Appendix B provide adequate directive evidence |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Coverage | 1 | HAS_ITEMS | No guidance on how to handle addenda-driven scope changes |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Alignment | 0 | NO_ITEMS | Directives are aligned across documents |
| X:applying:necessity | applying | necessity | Essential Implementation Need | 1 | HAS_ITEMS | Crane clearance envelope data source not identified |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Competence | 0 | NO_ITEMS | Practice steps are sufficiently detailed |
| X:applying:completeness | applying | completeness | Thorough Implementation Coverage | 0 | NO_ITEMS | Implementation steps cover all systems |
| X:applying:consistency | applying | consistency | Uniform Practice Discipline | 0 | NO_ITEMS | Practice steps are uniform and disciplined |
| X:judging:necessity | judging | necessity | Essential Adjudication Basis | 1 | HAS_ITEMS | No acceptance criterion for ductwork/equipment crane clearance |
| X:judging:sufficiency | judging | sufficiency | Sufficient Judgment Evidence | 0 | NO_ITEMS | Verification table provides sufficient judgment basis |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Coverage | 1 | HAS_ITEMS | Wash bay equipment rating not in verification |
| X:judging:consistency | judging | consistency | Coherent Adjudication Standard | 0 | NO_ITEMS | Adjudication criteria are coherent |
| X:reviewing:necessity | reviewing | necessity | Essential Verification Basis | 0 | NO_ITEMS | Verification basis established |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Audit evidence pathway via records is sufficient |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Coverage | 1 | HAS_ITEMS | No review step for cross-referencing with DEL-003-04 exhaust detail |
| X:reviewing:consistency | reviewing | consistency | Stable Audit Consistency | 0 | NO_ITEMS | Audit approach is stable and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add a consideration for how RFP addenda (R-02 and subsequent) should be tracked and integrated into the HVAC layout design process | Procedure Step 2d references checking addenda, but Guidance has no corresponding consideration for how addenda-driven scope changes should be evaluated and incorporated; exhaustive directive coverage requires this | Guidance.md, Procedure.md | Guidance: entire Considerations section; Procedure: Step 2d | — | Project Manager / Mechanical Engineer | TBD |
| X-002 | X:applying:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Identify source for crane clearance envelope dimensions (two 5-tonne overhead cranes) — confirm whether this comes from PKG-002 Structural or from Owner equipment specification | Guidance C-1 and Procedure Step 4 both reference crane clearance as critical for equipment placement, but Datasheet does not record crane envelope dimensions as a design input; essential implementation data is missing | Datasheet.md, Guidance.md | Datasheet: Building Context table; Guidance: C-1 | — | Structural Engineer (PKG-002) / Owner | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add a verification criterion for crane clearance: "No HVAC equipment or ductwork shall encroach on the crane travel envelope as defined by PKG-002 structural drawings" | Procedure verification table includes "Crane clearance — compare HVAC layout against structural crane envelope drawings — no conflicts identified" but Specification has no corresponding normative requirement to verify against | Specification.md, Procedure.md | Specification: entire Requirements section; Procedure: Verification table, Crane clearance row | — | Mechanical Engineer / Structural Engineer | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification criterion for wash bay HVAC equipment environmental rating (Guidance C-3 requires equipment "rated for humid/wash-down environments" but no verification exists) | Guidance C-3 states wash bay equipment must be "rated for humid/wash-down environments" and "protected from direct water contact"; Specification REQ-012 only verifies "ventilation supply and exhaust shown" without rating verification | Specification.md, Guidance.md | Specification: Verification table, REQ-012 row; Guidance: C-3 | — | Mechanical Engineer | TBD |
| X-005 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add a QA check step for cross-referencing HVAC layout against DEL-003-03 (Ductwork) and DEL-003-04 (Exhaust System Plans) to confirm consistency between companion deliverables | Procedure Step 7 QA checklist verifies systems against this deliverable's requirements but does not include cross-referencing against companion package deliverables DEL-003-03 and DEL-003-04; exhaustive review coverage requires companion consistency check | Procedure.md | Steps: Step 7 | — | Mechanical Engineer | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Steering Record | 1 | HAS_ITEMS | Appendix B conceptual locations not cross-referenced in Datasheet |
| E:guiding:information | guiding | information | Contextualized Steering Signal | 0 | NO_ITEMS | SOW cross-references provide adequate steering signals |
| E:guiding:knowledge | guiding | knowledge | Authoritative Guidance Mastery | 0 | NO_ITEMS | Guidance demonstrates domain mastery |
| E:guiding:wisdom | guiding | wisdom | Principled Guidance Prudence | 0 | NO_ITEMS | Guidance trade-offs demonstrate prudent reasoning |
| E:applying:data | applying | data | Verified Implementation Record | 1 | HAS_ITEMS | Ceiling fan scope conflict unresolved |
| E:applying:information | applying | information | Contextualized Practice Signal | 0 | NO_ITEMS | Practice signals are adequately contextualized |
| E:applying:knowledge | applying | knowledge | Mastered Execution Competence | 0 | NO_ITEMS | Procedure steps demonstrate execution competence |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment is sound |
| E:judging:data | judging | data | Substantiated Judgment Record | 1 | HAS_ITEMS | REQ-001 verification lacks measurable spatial criterion |
| E:judging:information | judging | information | Contextualized Assessment Signal | 0 | NO_ITEMS | Assessment signals adequately contextualized in Verification tables |
| E:judging:knowledge | judging | knowledge | Mastered Assessment Expertise | 0 | NO_ITEMS | Assessment framework demonstrates adequate expertise |
| E:judging:wisdom | judging | wisdom | Principled Assessment Wisdom | 0 | NO_ITEMS | Assessment approach is principled |
| E:reviewing:data | reviewing | data | Confirmed Audit Record | 1 | HAS_ITEMS | Record retention requirements not fully specified |
| E:reviewing:information | reviewing | information | Contextualized Audit Signal | 0 | NO_ITEMS | Audit signals present through records table |
| E:reviewing:knowledge | reviewing | knowledge | Mastered Audit Competence | 0 | NO_ITEMS | Audit competence demonstrated through QA steps |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Prudence | 0 | NO_ITEMS | Audit approach is principled and appropriately cautious |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Add a column or note in Datasheet Building Context or HVAC Systems tables recording the Appendix B conceptual equipment locations (e.g., "MUA — north wall per App B", "Welding exhaust — NE corner per App B") as a baseline reference | Guidance and Specification reference Appendix B conceptual locations but Datasheet does not record these as baseline data points; authoritative steering record requires the conceptual positions to be captured as data for layout comparison | Datasheet.md, Specification.md | Datasheet: HVAC Systems table; Specification: REQ-003, REQ-005 | — | Mechanical Engineer | TBD |
| E-002 | E:applying:data | Conflict | Multi | TBD | Resolve ceiling fan scope ownership: confirm whether ceiling fans are primarily documented on HVAC layout or electrical plans, and which deliverable is the primary record | Guidance CONF-002 flags that ceiling fans appear in App B-Elec (electrical scope) but SOW-0040 is assigned to Mechanical scope in decomposition; both documents reference this but ownership of the primary drawing record is unsettled | Guidance.md, Specification.md, Datasheet.md | Guidance: Conflict Table CONF-002; Specification: REQ-006; Datasheet: HVAC Systems table | Guidance.md#Conflict Table CONF-002 (R-04 App B-Elec vs. Decomposition SOW-0040) | Mechanical Engineer + Electrical Engineer / Project Manager | TBD |
| E-003 | E:judging:data | WeakStatement | Specification | Specification | Strengthen REQ-001 verification: "Layout confirms heating units cover all occupied areas" lacks a measurable criterion for what "cover" means (e.g., distance from heating unit, BTU/sq ft coverage, or zone-by-zone confirmation) | REQ-001 verification is "Layout confirms heating units cover all occupied areas" — this is subjective without a measurable spatial or thermal coverage criterion; judgment record requires substantiation | Specification.md | REQ-001 — System Coverage: Heating; Verification table, REQ-001 row | — | Mechanical Engineer | TBD |
| E-004 | E:reviewing:data | RationaleGap | Procedure | Guidance | Add retention period and format requirements for QA records (IFC drawing set, coordination comment log, internal QA checklist) — current Records table lists "Retained By" but not retention duration or format | Procedure Records table specifies who retains each record but not for how long or in what format; confirmed audit record requires retention policy to be established | Procedure.md | Records table | — | Project Manager / Owner | TBD |
