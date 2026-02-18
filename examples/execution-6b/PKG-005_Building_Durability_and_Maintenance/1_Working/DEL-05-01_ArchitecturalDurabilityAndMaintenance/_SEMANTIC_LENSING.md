# Semantic Lensing Register: DEL-05-01 Architectural Durability and Maintenance

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-01_ArchitecturalDurabilityAndMaintenance
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-01, PKG-005, Durability/Narrative, Architect responsible
- _STATUS.md -- Current state SEMANTIC_READY, last updated 2026-02-17
- _SEMANTIC.md -- All 8 matrices parsed (A, B canonical; C, F, D, K, X, E derived); K excluded from lensing per protocol (not in required set A, B, C, F, D, X, E)
- Datasheet.md -- Present; read in full
- Specification.md -- Present; read in full
- Guidance.md -- Present; read in full
- Procedure.md -- Present; read in full
- _REFERENCES.md -- Present; read in full

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 14
- By document:
  - Datasheet: 2
  - Specification: 5
  - Guidance: 2
  - Procedure: 1
  - Multi: 4
- By matrix:
  - A: 3  B: 2  C: 1  F: 2  D: 1  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 4
  - WeakStatement: 2
  - RationaleGap: 2
  - Normalization: 1
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Sump discharge strategy lacks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Mandatory practices well-documented across docs |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | NBCC/ABC compliance basis assumed, not confirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification sections provide adequate audit framework |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step sequence |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps well-covered in Procedure A1-A7 |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative performance thresholds for cladding impact resistance |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal review step (A6) provides process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | OBJ-005 scoring guidance well-articulated in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered through trade-off analysis |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scoring scale and criteria documented |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | V-006 scoring alignment check covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Specification | Clarify sump discharge strategy: Guidance C-005 notes sump discharge is "TBD" (holding tank, grease trap, or municipal connection) but no requirement in Specification captures this as a mandatory decision point with acceptance criteria | Bay sump discharge destination affects architectural floor design (drainage slopes, sealant at edges) and regulatory compliance (wastewater discharge permitting); leaving this unresolved risks downstream design conflict | Guidance.md; Specification.md | Guidance.md#C-005; Specification.md#R-007 | -- | Specification (add requirement for sump discharge decision) | TBD |
| A-002 | A:normative:judging | TBD_Question | Specification | Specification | Add confirmation of applicable building code editions (NBCC and ABC): Specification Standards table lists NBCC and ABC as "ASSUMPTION: applicable; location TBD" -- confirm specific edition years and confirm jurisdiction authority for Penhold | Building code compliance is foundational to the durability strategy; without confirmed editions, compliance determination cannot be completed | Specification.md | Specification.md#Standards | -- | Owner / AHJ confirmation required | TBD |
| A-003 | A:operative:judging | MissingSlot | Specification | Specification | Add quantitative or referenced performance threshold for exterior cladding impact resistance (e.g., ASTM impact test standard or rated impact resistance class) | R-002 requires "impact resistance relative to apparatus bay and operational vehicle areas" but provides no measurable threshold or test standard reference, making performance assessment subjective | Specification.md | Specification.md#R-002 | -- | Architect to propose threshold | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing overhead door count for main building |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations are thorough across Datasheet |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Main building person door requirements absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistently cited with sources |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (design lives, scoring weight) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Operational context well-developed |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Zone-by-zone accounts comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging consistent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fire/PW operational understanding demonstrated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Material expertise evident in Guidance examples |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage is thorough across scope areas |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent between docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off analyses demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls (e.g., lifecycle cost) well-reasoned |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Whole-building thinking articulated in P-004 |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add total count of main building overhead doors to Confirmed Requirements table (currently only size and hardware grade are specified; the total number of apparatus bay doors and PW bay doors is not recorded as an essential fact) | The number of overhead doors is a cost and durability multiplier (hardware, springs, weather seals); Datasheet records Cold Storage door count (two) but not main building door count | Datasheet.md | Datasheet.md#Confirmed Requirements by Element | -- | Architect / program confirmation | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add main building person door requirements (quantity, hardware grade, weather sealing standard) to Confirmed Requirements table; currently only Cold Storage person doors are documented | Person doors are architectural durability components subject to the same operational environment (salt, freeze-thaw) as overhead doors; their absence from Datasheet is a gap in the comprehensive record | Datasheet.md | Datasheet.md#Confirmed Requirements by Element | -- | Architect / RFP review | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | prescriptive mandate | 0 | NO_ITEMS | Prescriptive mandates well-documented from RFP/OSR |
| C:normative:sufficiency | normative | sufficiency | justified conformance | 0 | NO_ITEMS | Conformance justifications present with source citations |
| C:normative:completeness | normative | completeness | exhaustive compliance scope | 0 | NO_ITEMS | Compliance scope covered across all 11 requirements |
| C:normative:consistency | normative | consistency | harmonized regulatory integrity | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | demonstrated capability | 0 | NO_ITEMS | Capability demonstration covered in verification |
| C:operative:completeness | operative | completeness | thorough operational coverage | 0 | NO_ITEMS | Operational coverage thorough across zones |
| C:operative:consistency | operative | consistency | disciplined process alignment | 1 | HAS_ITEMS | Maintenance interval assumptions inconsistent |
| C:evaluative:necessity | evaluative | necessity | intrinsic value criterion | 0 | NO_ITEMS | Value criteria linked to OBJ-005 scoring |
| C:evaluative:sufficiency | evaluative | sufficiency | substantiated merit judgment | 0 | NO_ITEMS | Merit judgments substantiated with trade-off analysis |
| C:evaluative:completeness | evaluative | completeness | comprehensive value assessment | 0 | NO_ITEMS | Value assessment covers lifecycle cost, operations, maintenance |
| C:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Value reasoning coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:operative:consistency | Normalization | Multi | Guidance | Normalize maintenance interval assumptions: Guidance C-002 states "3-5 year resealing cycles" for apparatus bay flooring; Guidance T-002 states "recoating every 7-10 years" for epoxy; Procedure Step A5 maintenance table states "Re-seal/recoat every 3-10 years (ASSUMPTION)" combining both ranges into one ambiguous entry | The merged "3-10 years" range in Procedure conflates two different maintenance strategies (basic sealed concrete vs. epoxy-coated); this inconsistency could mislead the narrative author about actual intervals | Guidance.md; Procedure.md | Guidance.md#C-002; Guidance.md#T-002; Procedure.md#Step A5 | Guidance.md#C-002 (3-5 yr sealed); Guidance.md#T-002 (7-10 yr epoxy) | Guidance (clarify in considerations; Procedure should differentiate) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory compliance basis | 0 | NO_ITEMS | Mandatory basis established from RFP/OSR |
| F:normative:sufficiency | normative | sufficiency | defensible regulatory sufficiency | 1 | HAS_ITEMS | ASTM standards TBD weakens defensibility |
| F:normative:completeness | normative | completeness | total regulatory documentation | 0 | NO_ITEMS | Regulatory documentation comprehensive |
| F:normative:consistency | normative | consistency | coherent mandate discipline | 0 | NO_ITEMS | Mandates coherently tracked |
| F:operative:necessity | operative | necessity | critical operational foundation | 0 | NO_ITEMS | Operational foundations documented |
| F:operative:sufficiency | operative | sufficiency | verified process competence | 0 | NO_ITEMS | Process competence verification in place |
| F:operative:completeness | operative | completeness | exhaustive process documentation | 0 | NO_ITEMS | Process documentation thorough |
| F:operative:consistency | operative | consistency | aligned execution discipline | 0 | NO_ITEMS | Execution discipline consistent |
| F:evaluative:necessity | evaluative | necessity | foundational quality criterion | 0 | NO_ITEMS | Quality criteria linked to evaluation scoring |
| F:evaluative:sufficiency | evaluative | sufficiency | proportionate quality evidence | 1 | HAS_ITEMS | No lifecycle cost data framework for substantiation |
| F:evaluative:completeness | evaluative | completeness | exhaustive quality accounting | 0 | NO_ITEMS | Quality accounting covers all scope areas |
| F:evaluative:consistency | evaluative | consistency | principled quality alignment | 0 | NO_ITEMS | Quality alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification criterion for ASTM or equivalent material testing standards: Specification Standards table lists "ASTM Standards" as "ASSUMPTION: applicable; specific standards TBD" but no verification criterion confirms which ASTM standards must be cited in the narrative | Without identified testing standards (e.g., ASTM C666 for freeze-thaw, ASTM D4060 for abrasion), the defensibility of material performance claims in the narrative cannot be independently verified | Specification.md | Specification.md#Standards | -- | Architect to identify applicable ASTM standards | TBD |
| F-002 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add lifecycle cost comparison framework or worked example for roofing options: Guidance T-001 asserts Option A (long-life membrane) is preferred over Option B but provides no quantified lifecycle cost comparison or template for the estimator to populate | The claim that "total lifecycle cost of Option B over 50 years is typically higher than Option A" lacks quantitative substantiation; providing even a template with placeholder values would make the merit judgment defensible | Guidance.md | Guidance.md#T-001 | -- | Estimator / Architect | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | anchored regulatory direction | 0 | NO_ITEMS | Regulatory direction well-anchored to OSR/RFP |
| D:normative:applying | normative | applying | resolved obligatory practice | 0 | NO_ITEMS | Obligatory practices resolved in Specification |
| D:normative:judging | normative | judging | conclusive compliance ruling | 0 | NO_ITEMS | Compliance rulings deferred to verification; appropriate |
| D:normative:reviewing | normative | reviewing | resolved regulatory examination | 0 | NO_ITEMS | Regulatory examination framework present |
| D:operative:guiding | operative | guiding | grounded operational guidance | 0 | NO_ITEMS | Operational guidance well-grounded in P-001 through P-006 |
| D:operative:applying | operative | applying | validated practical delivery | 0 | NO_ITEMS | Practical delivery steps validated in Procedure |
| D:operative:judging | operative | judging | conclusive performance verdict | 1 | HAS_ITEMS | Missing performance verdict for secondary door opening |
| D:operative:reviewing | operative | reviewing | resolved operational review | 0 | NO_ITEMS | Operational review covered in Step A6 |
| D:evaluative:guiding | evaluative | guiding | established value guidance | 0 | NO_ITEMS | Value guidance established through OBJ-005 mapping |
| D:evaluative:applying | evaluative | applying | grounded merit implementation | 0 | NO_ITEMS | Merit implementation grounded in examples EX-001 through EX-004 |
| D:evaluative:judging | evaluative | judging | conclusive worth judgment | 0 | NO_ITEMS | Worth judgments concluded in trade-off recommendations |
| D:evaluative:reviewing | evaluative | reviewing | resolved quality appraisal | 0 | NO_ITEMS | Quality appraisal resolved through V-006 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:judging | VerificationGap | Specification | Specification | Add verification criterion for secondary bay door opening mechanism (Addendum 03 section 1.15): R-006 mentions secondary opening requirement but V-001 through V-006 do not include acceptance criteria confirming the mechanism is operable during power failure | The secondary opening mechanism is a life-safety-adjacent requirement for a fire hall (apparatus must egress during power outage); performance verdict requires testable acceptance criteria | Specification.md | Specification.md#R-006; Specification.md#Verification | -- | Architect / Electrical Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational directive benchmark | 0 | NO_ITEMS | Directive benchmarks established from RFP/OSR |
| X:guiding:sufficiency | guiding | sufficiency | credible directive adequacy | 0 | NO_ITEMS | Directives adequate |
| X:guiding:completeness | guiding | completeness | comprehensive guidance scope | 0 | NO_ITEMS | Guidance scope comprehensive |
| X:guiding:consistency | guiding | consistency | harmonized directive coherence | 0 | NO_ITEMS | Directives coherent |
| X:applying:necessity | applying | necessity | validated practice foundation | 1 | HAS_ITEMS | Missing validation of decontamination area drainage |
| X:applying:sufficiency | applying | sufficiency | demonstrated practice adequacy | 0 | NO_ITEMS | Practice adequacy demonstrated |
| X:applying:completeness | applying | completeness | thorough implementation coverage | 1 | HAS_ITEMS | SCBA room requirements incomplete |
| X:applying:consistency | applying | consistency | coherent implementation discipline | 0 | NO_ITEMS | Implementation consistent |
| X:judging:necessity | judging | necessity | binding adjudication standard | 0 | NO_ITEMS | Adjudication standards present in verification |
| X:judging:sufficiency | judging | sufficiency | substantiated adjudication | 1 | HAS_ITEMS | V-005 cross-reference check cannot be executed until dependencies ready |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 0 | NO_ITEMS | Adjudication scope matches requirements scope |
| X:judging:consistency | judging | consistency | principled adjudication integrity | 0 | NO_ITEMS | Adjudication principles consistent |
| X:reviewing:necessity | reviewing | necessity | foundational review criterion | 0 | NO_ITEMS | Review criteria present |
| X:reviewing:sufficiency | reviewing | sufficiency | credible review adequacy | 0 | NO_ITEMS | Review adequacy acceptable |
| X:reviewing:completeness | reviewing | completeness | comprehensive review coverage | 0 | NO_ITEMS | Review coverage comprehensive |
| X:reviewing:consistency | reviewing | consistency | harmonized review integrity | 0 | NO_ITEMS | Review integrity harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification criterion for decontamination area drainage and chemical resistance: R-004 lists decontamination area requirements (full moisture resistance, chemical-resistant, drain-capable) but no verification item specifically confirms drainage capacity or chemical resistance standard for this high-risk zone | Decontamination area serves post-incident contamination washdown; validating drainage and chemical resistance is essential for practice foundation -- this is a high-consequence zone with specific chemical exposure risks | Specification.md | Specification.md#R-004; Specification.md#Verification | -- | Architect | TBD |
| X-002 | X:applying:completeness | MissingSlot | Multi | Specification | Add SCBA room environmental requirements to R-004 or as a new requirement: Datasheet lists SCBA room (150-200 sq ft, compressed air equipment, special storage environment) but Specification R-004 interior finishes table does not include SCBA room as a zone, and no requirement addresses its finish or environmental control needs | SCBA room houses breathing apparatus requiring clean, controlled conditions; its absence from the interior finishes specification means implementation coverage is incomplete for this room | Datasheet.md; Specification.md | Datasheet.md#Room Size Ranges; Specification.md#R-004 | -- | Architect | TBD |
| X-003 | X:judging:sufficiency | WeakStatement | Multi | Procedure | Strengthen V-005 (cross-deliverable consistency) with interim check approach: V-005 acceptance criteria state "Once DEL-02-01 and DEL-05-02 are advanced, verify consistency" but provide no interim mechanism if those deliverables are not yet available at time of DEL-05-01 completion | Without an interim consistency check mechanism, the substantiation of this adjudication depends entirely on timing of other deliverables; the verification may never be executed if dependencies lag | Specification.md; Procedure.md | Specification.md#V-005; Procedure.md#V-005 | -- | Proposal Manager | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | authoritative compliance benchmark | 0 | NO_ITEMS | Compliance benchmarks authoritative |
| E:normative:sufficiency | normative | sufficiency | demonstrated regulatory adequacy | 0 | NO_ITEMS | Regulatory adequacy demonstrated |
| E:normative:completeness | normative | completeness | exhaustive regulatory fulfillment | 0 | NO_ITEMS | Regulatory fulfillment exhaustive |
| E:normative:consistency | normative | consistency | disciplined regulatory coherence | 0 | NO_ITEMS | Regulatory coherence disciplined |
| E:operative:necessity | operative | necessity | validated operational benchmark | 0 | NO_ITEMS | Operational benchmarks validated |
| E:operative:sufficiency | operative | sufficiency | demonstrated operational competence | 1 | HAS_ITEMS | Overhead door spring life assumption weakly supported |
| E:operative:completeness | operative | completeness | exhaustive operational coverage | 0 | NO_ITEMS | Operational coverage exhaustive |
| E:operative:consistency | operative | consistency | disciplined operational integrity | 0 | NO_ITEMS | Operational integrity maintained |
| E:evaluative:necessity | evaluative | necessity | authoritative quality benchmark | 1 | HAS_ITEMS | Missing fire-resistance rating integration |
| E:evaluative:sufficiency | evaluative | sufficiency | demonstrated quality sufficiency | 0 | NO_ITEMS | Quality sufficiency demonstrated |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality fulfillment | 0 | NO_ITEMS | Quality fulfillment exhaustive |
| E:evaluative:consistency | evaluative | consistency | integrated quality integrity | 0 | NO_ITEMS | Quality integrity integrated |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:sufficiency | VerificationGap | Procedure | Procedure | Add verification or confirmation step for overhead door spring life assumption: Procedure Step A5 maintenance table states "Replace springs when worn (ASSUMPTION: 5-10 year life at daily use for fire apparatus bays)" but no step in the procedure requires confirming this assumption with manufacturer data | Overhead door springs in a fire hall are a critical operational component (response egress); a 5-10 year assumption without manufacturer validation could lead to premature failure or unnecessary replacement scheduling -- demonstrated competence requires validated data | Procedure.md | Procedure.md#Step A5 | -- | Architect / Door manufacturer | TBD |
| E-002 | E:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale for how fire-resistance rating of cladding and interior finishes integrates with the durability strategy: OSR section 11.3 requires "non-combustible" materials; Specification R-002 references non-combustibility; but Guidance does not explain how fire-resistance classification (e.g., NBCC combustibility testing) interacts with durability material selections | Non-combustibility is an authoritative quality benchmark that constrains material selection; without rationale explaining how this constraint interacts with durability choices (e.g., ruling out certain high-durability but combustible cladding options), the quality benchmark is present but not integrated into the guidance reasoning | Specification.md; Guidance.md | Specification.md#R-002; Guidance.md#Principles | -- | Architect | TBD |

---

**End of Semantic Lensing Register**
