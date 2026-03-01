# Semantic Lensing Register: DEL-010-01 Foundation Construction

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-010_Foundation Construction/1_Working/DEL-010-01_Foundation-Construction/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-010-01_Foundation-Construction/_CONTEXT.md (all sections)
- _STATUS.md — DEL-010-01_Foundation-Construction/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-010-01_Foundation-Construction/_SEMANTIC.md (all matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-010-01_Foundation-Construction/Datasheet.md (all sections)
- Specification.md — DEL-010-01_Foundation-Construction/Specification.md (all sections)
- Guidance.md — DEL-010-01_Foundation-Construction/Guidance.md (all sections)
- Procedure.md — DEL-010-01_Foundation-Construction/Procedure.md (all sections)
- _REFERENCES.md — DEL-010-01_Foundation-Construction/_REFERENCES.md (read; 2 references listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 4
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 5  D: 4  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 8
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction for cold-weather concrete |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory practice for deficiency response timeline |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for code compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit adequately covered by inspection coordination requirements |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Weak procedural direction for topsoil disposal |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps are well-specified in Procedure.md |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment addressed through verification tables in Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit addressed by County representative inspection requirements |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Missing value orientation for cost-benefit of early geotech mobilization |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application adequately framed by variable-price structure |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination implicitly addressed through pricing framework |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by inspection and cylinder break protocols |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Procedure | Specification | Add prescriptive requirement for cold-weather concrete protection specifying minimum temperature thresholds and protection duration | Procedure.md Step 14 and Step 15 reference cold-weather protection as ASSUMPTION but no normative threshold is stated in Specification.md; this could change implementation decisions in Alberta winter construction. | Procedure.md; Specification.md | Procedure.md#Step 14: Concrete Placement; Specification.md#REQ-010-01-003 | — | PROPOSAL: Specification.md REQ-010-01-003 or new REQ | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for deficiency response timeline (10 days per RFP section 2.10.6) to Specification requirements | Datasheet.md records the 10-day deficiency response obligation from RFP section 2.10.6, but Specification.md has no corresponding requirement. This mandatory practice is not captured normatively. | Datasheet.md; Specification.md | Datasheet.md#Contractual Conditions; Specification.md#Requirements (entire section scanned) | — | PROPOSAL: New REQ in Specification.md | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-010-01-004 Structural Load Capacity specifying measurable pass/fail criteria (e.g., concrete strength, bearing capacity) | REQ-010-01-004 lists load categories but verification is "Structural engineer review; foundation design package compliance; TBD inspection protocol." The inspection protocol remains TBD, leaving compliance determination undefined. | Specification.md | Specification.md#REQ-010-01-004 | — | PROPOSAL: Specification.md Verification table | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Clarify topsoil disposal/stockpile direction in Step 6.3: specify whether County or Proponent determines disposal location, and reference civil design PKG-005 explicitly as the authority | Step 6.3 says "Stockpile or dispose of stripped topsoil per project specifications (TBD -- confirm with Owner and civil design PKG-005)." The procedural direction is materially vague for field execution. | Procedure.md | Procedure.md#Step 6: Topsoil Stripping | — | PROPOSAL: Procedure.md Step 6.3 | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for prioritizing early geotechnical mobilization in terms of cost-benefit, explaining the financial exposure of delayed geotech on foundation pricing and schedule | Guidance.md P-3 states foundation is on critical path but does not explain the cost implications of delayed geotech relative to total project value. This value orientation would help the GC make scheduling trade-offs. | Guidance.md | Guidance.md#P-3: Foundation is on the Critical Path | — | PROPOSAL: Guidance.md Principles section | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing essential fact: frost depth for Alberta site |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence adequacy is reasonable given early-stage TBDs |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Record retention periods are TBD throughout |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements are consistently sourced from RFP and App B |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (gates, triggers) are well-defined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for this stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive within available source material |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Inconsistent naming: "service pit" vs "service trench" |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of geotech-gated scope is clear |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicitly addressed |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery requirements not applicable at this stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment adequately guided by Guidance.md trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment framework provided through Guidance.md |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight addressed through Guidance.md considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: What is the design frost depth for the project site (SW 14-44-21-W4)? This is an essential fact for foundation depth determination that should be populated when the geotech report (PKG-008) is available. | Foundation depth depends on frost penetration depth, which is not recorded anywhere in the production documents. This is an essential datum for any Alberta foundation design. | Datasheet.md | Datasheet.md#Site Conditions | — | PROPOSAL: Geotechnical report (PKG-008) | TBD |
| B-002 | B:data:completeness | TBD_Question | Procedure | Procedure | Record TBD: Confirm specific retention periods for all foundation construction records per Camrose County records management requirements and Alberta regulatory requirements | Procedure.md Records table lists all retention periods as "Project duration + TBD." This leaves the comprehensive record requirement incomplete. Without defined retention, records may be prematurely destroyed. | Procedure.md | Procedure.md#Records | — | PROPOSAL: Camrose County records management policy; Alberta Safety Codes retention requirements | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "service pit" vs "service trench" — the RFP and Appendix B use both terms; production documents should settle on a single canonical term with a note on the alias | Datasheet.md uses "service pit/trench," Guidance.md C-5 uses "Service Pit," Procedure.md Step 3.2 says "Service pit / service trench," and the Guidance Conflict Table says "service trench per App B." This inconsistency could cause confusion in field coordination. | Datasheet.md; Guidance.md; Procedure.md | Datasheet.md#Building Foundation Program; Guidance.md#C-5; Procedure.md#Step 3; Guidance.md#Conflict Table | — | PROPOSAL: Guidance.md to establish canonical term | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Imperative | 1 | HAS_ITEMS | Authoritative imperative for P.Eng. sign-off acceptance criteria missing |
| C:normative:sufficiency | normative | sufficiency | Substantiated Compliance | 0 | NO_ITEMS | Compliance substantiation addressed through verification table |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Standards list may be incomplete |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Standards are consistently referenced |
| C:operative:necessity | operative | necessity | Essential Operational Threshold | 0 | NO_ITEMS | Operational thresholds well-defined through gates |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Working Capability | 0 | NO_ITEMS | Working capability addressed through prerequisites |
| C:operative:completeness | operative | completeness | Integral Process Coverage | 0 | NO_ITEMS | Process coverage is comprehensive in Procedure.md |
| C:operative:consistency | operative | consistency | Reliable Process Uniformity | 0 | NO_ITEMS | Process uniformity is consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Recognition | 0 | NO_ITEMS | Value recognition framed by variable-price structure |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Assessment | 0 | NO_ITEMS | Merit assessment framework adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Accounting | 1 | HAS_ITEMS | No accounting of schedule float or contingency value |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-010-01-002 specifying what constitutes "engineer of record sign-off" (e.g., signed as-built certification, field memo, or stamped confirmation) | REQ-010-01-002 verification says "engineer of record sign-off (TBD)." The authoritative imperative of design compliance lacks a defined acceptance mechanism. | Specification.md | Specification.md#REQ-010-01-002 | — | PROPOSAL: Specification.md Verification table | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add reference to National Building Code of Canada (NBC) as adopted by Alberta, and confirm whether CSA A23.3 or ACI 318 governs — the Standards table lists both with ASSUMPTION status | The Exhaustive Regulatory Scope lens reveals that the Standards table relies heavily on ASSUMPTIONs for concrete standards. The actual governing standard for reinforced concrete in Alberta (CSA A23.3 vs ACI 318) needs confirmation. | Specification.md | Specification.md#Standards | — | PROPOSAL: Structural engineer of record to confirm applicable standard | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a consideration for schedule contingency/float between foundation completion and PKG-011 mobilization, quantifying the risk exposure of zero-float handoff | Guidance.md P-3 identifies critical-path risk but provides no quantified accounting of schedule float or buffer. Comprehensive value accounting requires understanding the schedule contingency (or lack thereof) between foundation completion and downstream work. | Guidance.md | Guidance.md#P-3: Foundation is on the Critical Path | — | PROPOSAL: Guidance.md Considerations section | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Compliance Foundation | 1 | HAS_ITEMS | Binding compliance gap: lien holdback requirement not in Specification |
| F:normative:sufficiency | normative | sufficiency | Evidenced Governance Sufficiency | 0 | NO_ITEMS | Governance sufficiency addressed through contract framework |
| F:normative:completeness | normative | completeness | Total Regulatory Obligation Map | 1 | HAS_ITEMS | Obligation map incomplete: performance/labour bond not in Specification |
| F:normative:consistency | normative | consistency | Coherent Compliance Alignment | 1 | HAS_ITEMS | Compliance alignment gap between Datasheet and Specification |
| F:operative:necessity | operative | necessity | Core Execution Prerequisite | 0 | NO_ITEMS | Prerequisites comprehensively listed in Procedure.md |
| F:operative:sufficiency | operative | sufficiency | Verified Operational Competence | 1 | HAS_ITEMS | Verification gap for subgrade compaction acceptance criteria |
| F:operative:completeness | operative | completeness | Complete Process Readiness | 0 | NO_ITEMS | Process readiness adequately covered |
| F:operative:consistency | operative | consistency | Systematic Performance Coherence | 0 | NO_ITEMS | Performance coherence maintained |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | Worth criteria framed by variable-price mechanism |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Benchmark | 1 | HAS_ITEMS | Missing quality benchmark: concrete strength target |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Benefit Inventory | 0 | NO_ITEMS | Benefit inventory adequate for this stage |
| F:evaluative:consistency | evaluative | consistency | Stable Valuation Discipline | 0 | NO_ITEMS | Valuation discipline consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement for lien holdback compliance (10% per Alberta Prompt Payment and Construction Lien Act, per RFP section 2.13.2) — this binding compliance obligation is in Datasheet but absent from Specification | Datasheet.md records the 10% lien holdback and bond requirements. These binding compliance obligations have no corresponding normative requirement in Specification.md. | Datasheet.md; Specification.md | Datasheet.md#Contractual Conditions; Specification.md#Requirements (entire section scanned) | — | PROPOSAL: New REQ in Specification.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for performance bond (50%) and labour/material payment bond (50%) per RFP section 2.12 — these obligations are in Datasheet but absent from Specification | Datasheet.md records 50% performance bond and 50% labour/material payment bond requirements. These form part of the total regulatory obligation map but have no Specification requirement. | Datasheet.md; Specification.md | Datasheet.md#Contractual Conditions; Specification.md#Requirements (entire section scanned) | — | PROPOSAL: New REQ in Specification.md or note that these are project-wide (not deliverable-specific) | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Guidance | Normalize the listing of supported objectives: Datasheet cites OBJ-001, OBJ-002, OBJ-006; Specification cites OBJ-002 at REQ-010-01-009 only; Guidance cites OBJ-001, OBJ-002, OBJ-006 sporadically. Establish a consistent cross-reference approach. | Coherent compliance alignment requires consistent referencing of which project objectives each requirement traces to. The objective references are scattered and incomplete across documents. | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Identification; Specification.md#REQ-010-01-009; Guidance.md#P-3, P-4 | — | PROPOSAL: Guidance.md or Datasheet.md to maintain master objective-to-requirement traceability | TBD |
| F-004 | F:operative:sufficiency | VerificationGap | Procedure | Specification | Add measurable acceptance criteria for subgrade compaction (e.g., minimum percentage of Standard Proctor density) — currently "TBD per geotechnical report" with no interim standard stated | Procedure.md Step 10 requires compaction testing but acceptance criteria are entirely TBD. Verified operational competence requires a defined threshold, even if provisional pending geotech. | Procedure.md; Specification.md | Procedure.md#Step 10: Subgrade Compaction Testing; Specification.md#REQ-010-01-002 | — | PROPOSAL: Specification.md REQ-010-01-002 or new REQ; geotechnical report (PKG-008) for actual values | TBD |
| F-005 | F:evaluative:sufficiency | TBD_Question | Specification | Specification | Record TBD: What is the minimum specified concrete compressive strength (f'c) for the foundation? This quality benchmark is referenced implicitly by Procedure.md Step 16 (cylinder break results) but never stated. | Procedure.md Step 16 requires cylinder break results to meet "specified strength" but no specified strength value appears anywhere in the production documents. This is a fundamental quality benchmark that must be populated. | Specification.md; Procedure.md | Specification.md#REQ-010-01-004; Procedure.md#Step 16 | — | PROPOSAL: Foundation Design Package (DEL-002-11) to specify; Specification.md to record | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Directed Compliance Anchor | 0 | NO_ITEMS | Compliance anchors well-established |
| D:normative:applying | normative | applying | Enforced Governance Fulfillment | 1 | HAS_ITEMS | Governance fulfillment gap: no mechanism for scope change governance |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling addressed through inspection protocol |
| D:normative:reviewing | normative | reviewing | Settled Governance Assurance | 0 | NO_ITEMS | Governance assurance addressed |
| D:operative:guiding | operative | guiding | Operational Readiness Direction | 1 | HAS_ITEMS | Readiness direction gap: weather/seasonal constraints |
| D:operative:applying | operative | applying | Validated Execution Delivery | 0 | NO_ITEMS | Execution delivery well-structured |
| D:operative:judging | operative | judging | Settled Performance Verdict | 1 | HAS_ITEMS | Performance verdict: no final acceptance criteria for foundation handoff |
| D:operative:reviewing | operative | reviewing | Confirmed Process Integrity | 0 | NO_ITEMS | Process integrity confirmed through documentation requirements |
| D:evaluative:guiding | evaluative | guiding | Settled Value Orientation | 0 | NO_ITEMS | Value orientation settled through variable-price mechanism |
| D:evaluative:applying | evaluative | applying | Realized Quality Standard | 0 | NO_ITEMS | Quality standard framed adequately |
| D:evaluative:judging | evaluative | judging | Definitive Benefit Ruling | 1 | HAS_ITEMS | Missing criteria for when foundation rework vs acceptance is warranted |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Retrospection | 0 | NO_ITEMS | Quality retrospection addressed through records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add requirement or mechanism for governing scope changes discovered during construction (e.g., unexpected subgrade conditions requiring design modifications), specifying the change order and approval process under CCDC 14-2013 | Guidance.md C-1 identifies the risk of unexpected conditions and says to escalate, but no requirement in Specification.md establishes the change governance mechanism. Enforced governance fulfillment requires a defined process. | Specification.md; Guidance.md | Specification.md#Requirements (entire section scanned); Guidance.md#C-1 | — | PROPOSAL: Specification.md new REQ or reference to CCDC 14-2013 change provisions | TBD |
| D-002 | D:operative:guiding | MissingSlot | Guidance | Guidance | Add a consideration for seasonal/weather constraints on foundation construction in Alberta (frost, spring thaw, construction season window) and how these interact with the December 31, 2026 deadline | The operational readiness direction does not address seasonal constraints. Alberta foundation construction has a limited warm-season window; proceeding in winter requires significant cold-weather measures. This affects scheduling and cost. | Guidance.md | Guidance.md#Considerations (entire section scanned) | — | PROPOSAL: Guidance.md new Consideration C-7 | TBD |
| D-003 | D:operative:judging | VerificationGap | Procedure | Specification | Add formal acceptance criteria for the PKG-011 handoff: define what constitutes a "ready" foundation for superstructure (e.g., concrete strength achieved, as-built within tolerance, all inspections cleared, all documentation transmitted) | Procedure.md Step 20 lists handoff deliverables but does not define acceptance criteria for when the foundation is formally accepted as complete and ready for PKG-011. The settled performance verdict for foundation completion is undefined. | Procedure.md | Procedure.md#Step 20: Handoff to PKG-011 | — | PROPOSAL: Specification.md new acceptance criteria; Procedure.md Step 20 to reference | TBD |
| D-004 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on decision criteria for foundation rework vs acceptance when deviations are found (e.g., as-built dimensions outside tolerance, cylinder breaks marginally below spec): when is rework warranted vs engineered acceptance? | Procedure.md Step 19 says "Document any deviations from the design and submit to the structural engineer of record for acceptance" but Guidance.md provides no framework for evaluating when rework vs acceptance is appropriate. This definitive benefit ruling gap leaves the GC without decision support. | Procedure.md; Guidance.md | Procedure.md#Step 19; Guidance.md#Trade-offs (entire section scanned) | — | PROPOSAL: Guidance.md new Trade-off T-4 | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Purposeful Readiness Mandate | 1 | HAS_ITEMS | Readiness mandate gap: no pre-mobilization readiness checklist |
| X:guiding:sufficiency | guiding | sufficiency | Justified Preparedness Scope | 0 | NO_ITEMS | Preparedness scope justified through prerequisites |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Coverage | 0 | NO_ITEMS | Guidance coverage comprehensive |
| X:guiding:consistency | guiding | consistency | Coherent Guidance Alignment | 0 | NO_ITEMS | Guidance alignment coherent |
| X:applying:necessity | applying | necessity | Enforced Delivery Prerequisite | 0 | NO_ITEMS | Delivery prerequisites well-enforced through gates |
| X:applying:sufficiency | applying | sufficiency | Competent Fulfillment Proof | 1 | HAS_ITEMS | Fulfillment proof gap for concrete placement |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Archive | 1 | HAS_ITEMS | Delivery archive: no document register template |
| X:applying:consistency | applying | consistency | Uniform Delivery Standard | 0 | NO_ITEMS | Delivery standards consistent |
| X:judging:necessity | judging | necessity | Determined Outcome Basis | 0 | NO_ITEMS | Outcome bases defined through verification tables |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment Proof | 1 | HAS_ITEMS | Judgment proof gap for drainage verification |
| X:judging:completeness | judging | completeness | Complete Adjudication Record | 0 | NO_ITEMS | Adjudication records addressed |
| X:judging:consistency | judging | consistency | Coherent Verdict Alignment | 0 | NO_ITEMS | Verdict alignment coherent |
| X:reviewing:necessity | reviewing | necessity | Essential Assurance Validation | 1 | HAS_ITEMS | Assurance validation: conflict on service pit scope |
| X:reviewing:sufficiency | reviewing | sufficiency | Proven Assurance Competence | 0 | NO_ITEMS | Assurance competence addressed |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Archive | 0 | NO_ITEMS | Assurance archive addressed through Records table |
| X:reviewing:consistency | reviewing | consistency | Uniform Assurance Coherence | 0 | NO_ITEMS | Assurance coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Procedure | Procedure | Add a pre-mobilization readiness checklist consolidating all PRE-01 through PRE-09 confirmations into a single verifiable gate document with sign-off fields | Procedure.md lists 9 prerequisites but has no consolidated checklist or sign-off mechanism. The purposeful readiness mandate requires a single verifiable checkpoint before mobilization. | Procedure.md | Procedure.md#Prerequisites | — | PROPOSAL: Procedure.md new subsection under Prerequisites | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add verification requirement for concrete placement adequacy: specify that slump, air content, and temperature at placement must be within approved mix design tolerances, with reject criteria | REQ-010-01-010 requires concrete batch records and Procedure.md Step 14 lists what to record, but Specification.md has no requirement stating what constitutes acceptable concrete at placement (slump limits, air content range, temperature bounds). | Specification.md; Procedure.md | Specification.md#REQ-010-01-010; Procedure.md#Step 14 | — | PROPOSAL: Specification.md new REQ or expand REQ-010-01-003/REQ-010-01-004 | TBD |
| X-003 | X:applying:completeness | WeakStatement | Specification | Procedure | Clarify the document register requirement in REQ-010-01-010: specify whether a formal document register (list/index of all produced artifacts) is required as a deliverable artifact, or only the individual documents | REQ-010-01-010 verification says "Document register review at completion" but neither the requirement text nor Procedure.md defines what the document register consists of or its format. This is vague for the exhaustive delivery archive. | Specification.md | Specification.md#REQ-010-01-010 | — | PROPOSAL: Procedure.md Records section; Specification.md Documentation section | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Add verification method for REQ-010-01-005 drainage/grading: specify what "post-construction drainage inspection" entails (visual, surveyed grades, flow test) and who accepts | REQ-010-01-005 verification says "post-construction drainage inspection (ASSUMPTION)." The substantiated judgment proof for drainage compliance is undefined. | Specification.md | Specification.md#REQ-010-01-005 | — | PROPOSAL: Specification.md Verification table row for REQ-010-01-005 | TBD |
| X-005 | X:reviewing:necessity | Conflict | Multi | NA | Resolve service pit scope boundary: is the service pit structural work within PKG-010 (Foundation Construction) or PKG-011 (Building Structure and Envelope)? This affects the assurance validation scope of this deliverable. | Guidance.md CF-010-01 flags this conflict. The service pit appears in Datasheet.md as a foundation attribute, Specification.md REQ-010-01-004 references it as a structural load, and Procedure.md Step 3.2 includes it in embedded items review. But Guidance.md proposes treating it as PKG-011 scope. The production documents are internally inconsistent on whether this is in-scope. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet.md#Building Foundation Program; Specification.md#REQ-010-01-004; Guidance.md#CF-010-01; Procedure.md#Step 3 | Guidance.md#CF-010-01 (proposes PKG-011); Datasheet.md#Building Foundation Program (lists as attribute); Specification.md#REQ-010-01-004 (includes in structural loads) | PROPOSAL: Owner/project manager to confirm; structural drawings to clarify | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Documented Readiness Authority | 1 | HAS_ITEMS | Readiness authority: Datasheet missing explicit readiness criteria summary |
| E:guiding:information | guiding | information | Coherent Preparedness Brief | 0 | NO_ITEMS | Preparedness brief adequately covered by Guidance.md |
| E:guiding:knowledge | guiding | knowledge | Proficient Directional Mastery | 0 | NO_ITEMS | Directional mastery addressed through Guidance.md principles and considerations |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 0 | NO_ITEMS | Directional foresight addressed through Guidance.md trade-offs |
| E:applying:data | applying | data | Verified Delivery Evidence | 1 | HAS_ITEMS | Delivery evidence: Datasheet anticipated artifacts incomplete |
| E:applying:information | applying | information | Clear Execution Status Report | 0 | NO_ITEMS | Execution status reporting addressed through Procedure.md gates |
| E:applying:knowledge | applying | knowledge | Competent Delivery Mastery | 0 | NO_ITEMS | Delivery mastery adequately framed |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Execution judgment addressed through Guidance.md |
| E:judging:data | judging | data | Documented Judgment Record | 0 | NO_ITEMS | Judgment records addressed through inspection reports and test results |
| E:judging:information | judging | information | Authoritative Verdict Account | 0 | NO_ITEMS | Verdict accounts covered by verification tables |
| E:judging:knowledge | judging | knowledge | Proficient Adjudication Expertise | 0 | NO_ITEMS | Adjudication expertise requirements addressed |
| E:judging:wisdom | judging | wisdom | Principled Ruling Wisdom | 0 | NO_ITEMS | Ruling wisdom framed by Guidance.md trade-offs |
| E:reviewing:data | reviewing | data | Documented Assurance Record | 1 | HAS_ITEMS | Normalization needed for Datasheet status field |
| E:reviewing:information | reviewing | information | Clear Assurance Status Report | 0 | NO_ITEMS | Assurance status reporting addressed |
| E:reviewing:knowledge | reviewing | knowledge | Competent Assurance Mastery | 0 | NO_ITEMS | Assurance mastery addressed |
| E:reviewing:wisdom | reviewing | wisdom | Principled Assurance Wisdom | 0 | NO_ITEMS | Assurance wisdom addressed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | WeakStatement | Datasheet | Datasheet | Add a readiness criteria summary to the Datasheet identifying the key data points that must be populated before construction can proceed (i.e., which TBD fields are construction gates vs nice-to-have) | Datasheet.md contains many TBD fields (foundation type, subgrade conditions, deleterious material). The documented readiness authority lens reveals no way to distinguish which TBDs are blocking gates vs informational. | Datasheet.md | Datasheet.md#Building Foundation Program; Datasheet.md#Site Conditions | — | PROPOSAL: Datasheet.md new section or annotation | TBD |
| E-002 | E:applying:data | RationaleGap | Datasheet | Datasheet | Add the variable-price contract supplement to the Datasheet Anticipated Artifacts section as a required artifact, explaining that this is the binding document establishing the negotiated foundation cost | Datasheet.md Anticipated Artifacts section lists construction documentation but not the variable-price contract supplement that Procedure.md Step 2 requires. This is a critical delivery evidence artifact. Procedure.md Records table includes it but Datasheet.md does not. | Datasheet.md; Procedure.md | Datasheet.md#Anticipated Artifacts; Procedure.md#Records | — | PROPOSAL: Datasheet.md Anticipated Artifacts | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Multi | Normalize the document status field: Datasheet.md header says "INITIALIZED" but _STATUS.md says "SEMANTIC_READY." Ensure Datasheet, Specification, Guidance, and Procedure headers reflect the current lifecycle state. | All four production documents show "Status: INITIALIZED" in their headers, but _STATUS.md records the current state as "SEMANTIC_READY." This inconsistency in the documented assurance record could confuse downstream consumers. | Datasheet.md; Specification.md; Guidance.md; Procedure.md; _STATUS.md | Datasheet.md header; Specification.md header; Guidance.md header; Procedure.md header; _STATUS.md | Datasheet.md header (INITIALIZED); _STATUS.md (SEMANTIC_READY) | PROPOSAL: Update production document headers to match _STATUS.md, or note that headers reflect authoring-time state | TBD |
