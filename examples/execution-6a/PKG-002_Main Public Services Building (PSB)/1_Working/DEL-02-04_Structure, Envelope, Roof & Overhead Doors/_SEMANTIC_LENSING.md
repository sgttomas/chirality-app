# Semantic Lensing Register: DEL-02-04 Structure, Envelope, Roof & Overhead Doors

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-04_Structure, Envelope, Roof & Overhead Doors/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-02-04 context (ID, scope SOW-0201/0215-0217/0220-0221, objectives OBJ-001/OBJ-006)
- _STATUS.md — Current state: SEMANTIC_READY (last updated 2026-02-17)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E parsed (92 cells total)
- Datasheet.md — Present; identification, attributes, conditions, construction sections
- Specification.md — Present; scope, requirements R-01 through R-20, standards, verification, documentation
- Guidance.md — Present; purpose, principles P-01 through P-06, considerations C-01 through C-08, trade-offs T-01 through T-04
- Procedure.md — Present; Part A (steps A-1 through A-7), Part B (steps B-1 through B-9), verification, records
- _REFERENCES.md — Present; lists OSR, RFP 2024_004, Addendum 03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 11
  - Guidance: 5
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 5  C: 4  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 7
  - MissingSlot: 8
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Envelope assembly specifics TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Car wash hardware spec weak on product standard |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC access status location TBD across docs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers audit adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Part A steps well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Slab design load parameters missing |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure verification table adequate |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Step A-7 and B-series provide audit coverage |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | P-01 through P-06 provide value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No quantified lifecycle cost basis |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-01 through T-04 adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered by verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Clarify "TBD -- DB to propose" for envelope assemblies with minimum performance criteria (thermal resistance, air barrier class) | Datasheet lists envelope assemblies as "TBD -- DB to propose" with only an ASSUMPTION note about cold climate. Without minimum prescriptive thresholds the DB has no performance floor to design against. | Datasheet.md | Envelope > Specific envelope assemblies | -- | Specification.md or Datasheet.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Add product standard reference for "car wash grade hardware" (e.g., DASMA rating, stainless steel grade, or equivalent industry benchmark) | R-14 requires "car wash grade hardware" but no referenced product standard or test method is cited. This term is colloquial and may be interpreted differently by different suppliers. | Specification.md | R-14: Overhead Doors -- Hardware Grade | -- | Specification.md | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | TBD | Record TBD: Obtain Alberta Building Code edition year and confirm specific structural load tables applicable to Penhold, AB | Multiple documents reference "Alberta Building Code" but it is listed as "location TBD" in both Datasheet (References) and Specification (Standards). The specific edition year is not stated, preventing compliance determination. | Specification.md; Datasheet.md | Standards table; References table | -- | External: AHJ / DB structural engineer | TBD |
| A-004 | A:operative:applying | MissingSlot | Datasheet | Datasheet | Add vehicle axle load and point load design parameters for bay floor slab design | C-02 in Guidance notes heavy equipment loads and states floor slab design load parameters are ASSUMPTION/TBD. These factual parameters (axle loads for Type 1 engines, aerial trucks, graders, dump trucks) belong in Datasheet but are absent. | Datasheet.md | Interior Flooring -- Main Building | -- | Datasheet.md | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Guidance | Guidance | Add lifecycle cost comparison framework or reference methodology for 50-year material selection decisions | P-01 states design decisions should be evaluated against 50-year life, not just first cost. However, no quantified methodology, reference benchmark, or evaluation framework is provided to support merit application of this principle. | Guidance.md | P-01: 50-Year Lifecycle as a Design Driver | -- | Guidance.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing thermal performance data |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotechnical report not directly read |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Door count not enumerated |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (50-yr life, solar-ready, car wash hardware) present |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | Person door requirements underspecified |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope in/out adequately delineated |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | No contradictory information signals found |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural design philosophy stated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | DB responsibility for expertise clearly assigned |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 1 | HAS_ITEMS | Vapour barrier strategy incomplete |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs provide essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Resolution guidance in trade-offs adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add minimum thermal resistance values (effective R-value) for envelope assemblies appropriate to Penhold, AB climate zone | Datasheet records envelope material intent as "weather-tight; low-maintenance" but contains no thermal performance data. For a 50-year cold climate building, thermal resistance is an essential fact for structural/envelope design. | Datasheet.md | Envelope > Envelope material intent | -- | Datasheet.md | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Multi | TBD | Record TBD: Confirm whether Geotechnical Investigation Report (RFP Appendix D) has been directly reviewed by the DB structural engineer and whether additional investigation is needed | Datasheet references geotechnical data as a condition; Guidance C-08 flags early evaluation of report adequacy; Procedure A-1 requires review. However, the report itself is noted as "not directly read" in the Datasheet references. Evidence sufficiency for foundation design cannot be confirmed from available documents alone. | Datasheet.md; Procedure.md | Datasheet > Conditions > Geotechnical data; Procedure > Step A-1 | -- | DB structural engineer | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add total overhead door count and per-bay assignment (e.g., 4 fire bays + 4 PW bays = 8 overhead doors) to Datasheet | Datasheet specifies door size (16x16), hardware grade, and operators, but does not state the total number of overhead doors or their bay assignments. This is a comprehensive record gap that the door schedule depends on. | Datasheet.md | Overhead Doors -- Main Building | -- | Datasheet.md | TBD |
| B-004 | B:information:sufficiency | WeakStatement | Specification | Specification | Strengthen R-16 person door requirement with specific count basis, accessibility standard reference, and hardware grade | R-16 states "adequate person doors shall be provided to meet Alberta Building Code." The word "adequate" is vague and the verification is "door schedule reviewed against ABC requirements." No minimum count, specific accessibility standard (e.g., barrier-free path of travel), or hardware specification is provided. | Specification.md | R-16: Person Doors | -- | Specification.md | TBD |
| B-005 | B:knowledge:completeness | MissingSlot | Guidance | Guidance | Add consideration for vapour barrier continuity strategy in cold climate envelope design, including condensation risk at thermal bridge locations | Guidance P-06 addresses weather-tightness and mentions freeze-thaw, ice damming, and condensation. Procedure A-3 mentions "air/vapour barrier continuity." However, Guidance does not provide a dedicated consideration for vapour barrier strategy despite this being a critical knowledge domain for cold climate envelope assemblies. | Guidance.md | P-06: Weather-Tightness Is Non-Negotiable | -- | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Obligation | 1 | HAS_ITEMS | Seismic load category unstated |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Conformance | 1 | HAS_ITEMS | Envelope conformance path missing |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 0 | NO_ITEMS | R-01 through R-20 cover regulatory scope |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Discipline | 0 | NO_ITEMS | No conflicting regulatory references found |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 1 | HAS_ITEMS | No explicit fire response time constraint |
| C:operative:sufficiency | operative | sufficiency | Competent Execution Capacity | 0 | NO_ITEMS | DB responsibility and prerequisites adequate |
| C:operative:completeness | operative | completeness | Integrated Process Coverage | 1 | HAS_ITEMS | Missing envelope mock-up/testing step |
| C:operative:consistency | operative | consistency | Disciplined Operational Uniformity | 0 | NO_ITEMS | Procedure steps consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Basis | 0 | NO_ITEMS | 50-year lifecycle value basis established |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Judgment | 0 | NO_ITEMS | Trade-offs provide defensible basis |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Assessment | 0 | NO_ITEMS | Durability narrative covers holistic view |
| C:evaluative:consistency | evaluative | consistency | Principled Appraisal Coherence | 0 | NO_ITEMS | Consistent valuation logic across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement or explicit statement regarding seismic design category for Penhold, AB (even if low seismicity, the design basis should state the applicable seismic hazard parameters) | R-02 addresses snow, lateral, and wind loads but does not explicitly mention seismic loads. While Penhold, AB is in a low seismicity zone, the authoritative obligation lens highlights that the seismic design category should be explicitly stated in the structural design basis, not assumed. | Specification.md | R-02: Structural Loads | -- | Specification.md | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for envelope thermal and air barrier performance (e.g., design review against energy code, field air barrier testing, or thermographic inspection) | The Verification table includes R-08 (weather-tightness) with "envelope air/water barrier details reviewed at design milestones; site inspection during construction." However, there is no verification for thermal performance or air barrier effectiveness against energy code requirements. Demonstrated conformance requires measurable verification. | Specification.md | Verification table > R-08 | -- | Specification.md | TBD |
| C-003 | C:operative:necessity | RationaleGap | Guidance | Guidance | Add consideration for overhead door opening speed and response time requirements for emergency apparatus deployment | P-02 states "door failures can interrupt emergency response" and R-15 addresses secondary mechanisms. However, no consideration addresses the operational necessity of door opening speed (time from activation to full open) for fire apparatus deployment. For a volunteer fire hall this is a critical operational readiness factor. | Guidance.md | P-02: Operational Continuity Drives Structural and Door Design | -- | Guidance.md | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add step for envelope assembly mock-up or field testing requirement at construction phase (e.g., water penetration test at representative wall section before full installation) | Procedure Part B covers structural, door, and flooring construction verification but does not include an envelope assembly testing or mock-up step. For a 50-year building in a cold climate, integrated process coverage should include field verification of envelope performance before full-scale installation. | Procedure.md | Part B -- Implementation Procedure | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Regulatory Command | 0 | NO_ITEMS | Requirements R-01 through R-20 enforceable |
| F:normative:sufficiency | normative | sufficiency | Warranted Compliance Threshold | 1 | HAS_ITEMS | Solar loading allowance not formalized |
| F:normative:completeness | normative | completeness | Total Prescriptive Accounting | 1 | HAS_ITEMS | Missing fire-resistance rating requirement |
| F:normative:consistency | normative | consistency | Systematic Prescriptive Alignment | 0 | NO_ITEMS | Requirements consistently sourced |
| F:operative:necessity | operative | necessity | Essential Execution Preparedness | 1 | HAS_ITEMS | Missing hold point for geotechnical sign-off |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Competence | 0 | NO_ITEMS | DB competence requirements stated |
| F:operative:completeness | operative | completeness | Complete Operational Mastery | 0 | NO_ITEMS | Part A + Part B steps comprehensive |
| F:operative:consistency | operative | consistency | Coherent Operational Standard | 0 | NO_ITEMS | Steps consistently reference source requirements |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Evaluation Foundation | 0 | NO_ITEMS | Evaluation criteria linked to RFP scoring |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal Standard | 1 | HAS_ITEMS | No scoring weight or rubric reference |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Evaluative Mastery | 0 | NO_ITEMS | Durability narrative evaluation covered |
| F:evaluative:consistency | evaluative | consistency | Systematic Evaluative Discipline | 0 | NO_ITEMS | Evaluation approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Formalize solar loading allowance as a minimum structural requirement (e.g., "roof structure shall accommodate minimum [TBD] psf additional dead load for future solar panels") rather than leaving as Guidance example only | Guidance provides an illustrative ASSUMPTION of 3-5 psf for solar loading. R-10 requires the roof to be "solar-capable" but does not state a minimum loading allowance. The warranted compliance threshold for solar readiness is not quantified in any requirement. | Specification.md; Guidance.md | R-10: Roof -- Solar-Ready Capability; Example: Solar Loading Allowance | -- | Specification.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for fire-resistance rating of structural elements and envelope assemblies per Alberta Building Code occupancy classification | R-20 requires general code compliance, but no specific requirement addresses fire-resistance ratings for structural members or envelope assemblies. For total prescriptive accounting of a building housing fire apparatus and equipment, fire-resistance rating should be an explicit requirement, not subsumed under general compliance. | Specification.md | Requirements section (after R-20) | -- | Specification.md | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit hold point in Step B-6 requiring written geotechnical engineer sign-off on subgrade/granular base before foundation pour may proceed | Step B-6 mentions geotechnical certification but does not establish a formal hold point (stop work until sign-off received). R-05 requires geotechnical services including subgrade certification. Essential execution preparedness requires this to be a gated milestone. | Procedure.md | Step B-6: Construction Phase -- Structural and Envelope | -- | Procedure.md | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add reference to RFP evaluation scoring weights for durability (RFP Section 7.1.4) and adaptability (RFP Section 7.1.5) so the DB understands relative importance of these criteria | R-07 and R-09 are labeled "proposal evaluation criterion" but no scoring weight or rubric is referenced in Guidance or Specification. The DB needs to understand relative priority to make justified material selection trade-offs. | Guidance.md; Specification.md | T-01 through T-04; R-07, R-09 | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Sovereign Prescriptive Authority | 0 | NO_ITEMS | Authority hierarchy clear |
| D:normative:applying | normative | applying | Resolved Compliance Duty | 1 | HAS_ITEMS | Post-disaster exemption unconfirmed |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 0 | NO_ITEMS | Verification table provides verdict path |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Examination | 0 | NO_ITEMS | AHJ review process documented |
| D:operative:guiding | operative | guiding | Resolved Procedural Orientation | 0 | NO_ITEMS | Part A workflow clear |
| D:operative:applying | operative | applying | Confirmed Operational Proficiency | 0 | NO_ITEMS | DB team requirements stated |
| D:operative:judging | operative | judging | Resolved Performance Verdict | 1 | HAS_ITEMS | No acceptance criteria for deflection limits |
| D:operative:reviewing | operative | reviewing | Systematic Operational Examination | 0 | NO_ITEMS | B-series steps systematic |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Compass | 0 | NO_ITEMS | P-01 through P-06 resolve value direction |
| D:evaluative:applying | evaluative | applying | Enacted Worth Standard | 0 | NO_ITEMS | Trade-off resolutions enacted |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Judgment | 1 | HAS_ITEMS | No O&M cost projection method |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Evaluative Rigor | 0 | NO_ITEMS | RFP evaluation framework referenced |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification milestone or tracking mechanism for AHJ confirmation of post-disaster exemption (R-03) -- currently only states "written confirmation during permit process" without specifying when this must be obtained or what happens if denied | R-03 labels the post-disaster exemption as an ASSUMPTION requiring AHJ confirmation. Verification states "written confirmation from AHJ during permit process." However, there is no contingency or deadline stated. If the exemption is denied, the structural design basis changes significantly. The compliance duty remains unresolved until confirmed. | Specification.md | R-03: Post-Disaster Importance Category; Verification table | -- | Specification.md + Procedure.md | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add specific deflection limits or reference to applicable code deflection criteria in R-02 (e.g., L/240 for snow, L/360 for live load) to enable resolved performance verdict | R-02 states "within acceptable deflection limitations" but does not define what those limitations are. The verification approach states "structural engineer's sealed drawings and calculations confirming load design" but does not specify pass/fail criteria for deflection. A performance verdict requires defined acceptance thresholds. | Specification.md | R-02: Structural Loads | -- | Specification.md | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on expected methodology for projecting O&M costs over 50-year lifecycle to support material selection merit judgments in the durability narrative | The durability narrative (Step A-6; RFP Section 7.1.4) requires the DB to address component lifecycle and replacement schedules over 50 years. However, no methodology or framework for projecting O&M costs is provided. Without this, the conclusive merit judgment on material selection alternatives lacks a defensible quantitative basis. | Guidance.md | P-01: 50-Year Lifecycle as a Design Driver; Example: Durability Narrative Structure | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Paramount Directive Foundation | 0 | NO_ITEMS | Core directives well-founded |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Governance Competence | 0 | NO_ITEMS | Source tracing adequate |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 1 | HAS_ITEMS | No acoustic performance directive |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Discipline | 0 | NO_ITEMS | Directives internally consistent |
| X:applying:necessity | applying | necessity | Confirmed Mandatory Practice | 1 | HAS_ITEMS | No mandatory coordination meeting step |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Practice Competence | 0 | NO_ITEMS | Practice steps sufficient |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Coverage | 0 | NO_ITEMS | Implementation steps comprehensive |
| X:applying:consistency | applying | consistency | Dependable Implementation Standard | 0 | NO_ITEMS | Standards consistently applied |
| X:judging:necessity | judging | necessity | Binding Determination Finding | 1 | HAS_ITEMS | No binding acceptance for roof drainage |
| X:judging:sufficiency | judging | sufficiency | Substantiated Competence Finding | 0 | NO_ITEMS | Competence verification adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Verification table covers all 20 requirements |
| X:judging:consistency | judging | consistency | Principled Adjudication Consistency | 0 | NO_ITEMS | Verification approaches consistent in style |
| X:reviewing:necessity | reviewing | necessity | Systematic Oversight Examination | 0 | NO_ITEMS | Review milestones defined |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Review Adequacy | 0 | NO_ITEMS | Review approach adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Review | 1 | HAS_ITEMS | No post-occupancy review step |
| X:reviewing:consistency | reviewing | consistency | Harmonized Oversight Discipline | 0 | NO_ITEMS | Review discipline consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | TBD_Question | Specification | Specification | Record TBD: Determine whether acoustic performance requirements for structure/envelope (e.g., STC rating for walls between fire hall and public works, or exterior noise attenuation) are needed for this deliverable or assigned elsewhere | No requirement or consideration addresses acoustic performance of the building envelope or party walls. For a building housing fire apparatus (sirens, air horns, diesel engines) adjacent to office/shared spaces, acoustic separation may be a necessary directive. This may be covered by DEL-02-01 (architectural program) but is not explicitly cross-referenced. | Specification.md; Guidance.md | entire document scanned | -- | DEL-02-01 or Specification.md | TBD |
| X-002 | X:applying:necessity | Normalization | Procedure | Procedure | Add explicit interdisciplinary coordination meeting step in Part A between DEL-02-04 and dependent deliverables (DEL-02-02, DEL-02-03, DEL-02-05, DEL-02-07) before Step A-7 consistency review | Step A-7 performs a consistency review cross-checking against DEL-02-02, -03, -05, and -07. However, there is no step requiring a coordination meeting or formal interface exchange with those deliverable teams. The consistency review is after-the-fact; a mandatory coordination practice during development would prevent rather than detect misalignment. | Procedure.md | Step A-7: Internal Consistency Review | -- | Procedure.md | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add quantified acceptance criteria for roof drainage (R-11), e.g., minimum slope percentage, maximum ponding area, or drainage test method | R-11 requires "adequate drainage away from the structure." Verification states "roof drainage plan/details reviewed at 60% and 100% design." No quantified acceptance criterion exists for what constitutes adequate drainage. A binding determination requires measurable pass/fail criteria. | Specification.md | R-11: Roof -- Drainage; Verification table | -- | Specification.md | TBD |
| X-004 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add post-occupancy envelope and roof performance review step (e.g., 1-year post-substantial-completion inspection for water ingress, drainage function, door operation) | Procedure B-9 covers commissioning and closeout at substantial completion. However, many envelope and roof defects manifest only after seasonal cycling (first winter, first spring melt). No post-occupancy review or warranty inspection step is included. For exhaustive oversight, a seasonal review within the warranty period should be documented. | Procedure.md | Step B-9: Commissioning and Closeout | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Absolute Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandates addressed by R-01 through R-20 |
| E:normative:sufficiency | normative | sufficiency | Confirmed Prescriptive Sufficiency | 1 | HAS_ITEMS | Insulation requirement gap |
| E:normative:completeness | normative | completeness | Exhaustive Prescriptive Completeness | 0 | NO_ITEMS | Requirement set comprehensive for scope |
| E:normative:consistency | normative | consistency | Harmonized Prescriptive Regime | 0 | NO_ITEMS | No prescriptive conflicts detected |
| E:operative:necessity | operative | necessity | Confirmed Execution Baseline | 0 | NO_ITEMS | Execution baseline established |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Threshold | 1 | HAS_ITEMS | Construction tolerance standards missing |
| E:operative:completeness | operative | completeness | Total Operational Coverage | 0 | NO_ITEMS | Operations coverage complete |
| E:operative:consistency | operative | consistency | Dependable Operational Consistency | 0 | NO_ITEMS | Operational procedures consistent |
| E:evaluative:necessity | evaluative | necessity | Intrinsic Quality Imperative | 0 | NO_ITEMS | Quality imperative clear (50-year life) |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Merit Threshold | 0 | NO_ITEMS | Merit thresholds addressed in trade-offs |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Appraisal Completeness | 1 | HAS_ITEMS | Missing maintenance cost projection |
| E:evaluative:consistency | evaluative | consistency | Systematic Merit Governance | 0 | NO_ITEMS | Merit governance consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | VerificationGap | Specification | Specification | Add requirement or verification criterion for building envelope insulation values meeting Alberta energy code minimum (NECB or equivalent applicable standard) | No requirement in R-01 through R-20 addresses thermal insulation performance. R-08 covers weather-tightness (water/moisture) but not thermal performance. R-20 references general code compliance, but confirmed prescriptive sufficiency requires explicit insulation verification against the energy code. | Specification.md | R-08: Building Envelope -- Weather-Tightness; R-20: Code Compliance | -- | Specification.md | TBD |
| E-002 | E:operative:sufficiency | WeakStatement | Specification | Specification | Add construction tolerance standards for key structural and envelope elements (e.g., bay clear height tolerance, slab flatness/levelness per ACI 117 or equivalent) | R-06 requires "minimum 16 ft clear overhead door height." Verification states "dimensional check on structural drawings; confirmed at 60% and 100% design milestones." However, no construction tolerance is specified for the as-built clear height. Similarly, bay floor slab flatness is not specified. Without tolerances, the demonstrated operational threshold is ambiguous. | Specification.md | R-06: Structural Objectives -- Bay Clear Heights; R-17: Flooring -- Bay Areas | -- | Specification.md | TBD |
| E-003 | E:evaluative:completeness | Normalization | Multi | Guidance | Standardize terminology for durability assessment: "durability/lifecycle strategy" (Datasheet, Procedure), "durability narrative" (Guidance), "durability/ease of repair" (RFP §7.1.4 as cited) -- adopt single canonical term across documents | Three different phrasings are used for the same artifact across documents. This normalization issue could cause confusion about whether these refer to the same deliverable artifact or distinct items. | Datasheet.md; Guidance.md; Procedure.md | Datasheet > Anticipated Artifacts; Guidance > Example: Durability Narrative Structure; Procedure > Step A-6 | -- | Guidance.md (vocabulary note) | TBD |

---

*End of Semantic Lensing Register*
