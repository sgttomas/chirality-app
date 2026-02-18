# Semantic Lensing Register: DEL-04-03 Electrical Energy Efficiency

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-004_Sustainability_and_Energy/1_Working/DEL-04-03_ElectricalEnergyEfficiency
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-04-03_ElectricalEnergyEfficiency/_CONTEXT.md
- _STATUS.md -- DEL-04-03_ElectricalEnergyEfficiency/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-04-03_ElectricalEnergyEfficiency/_SEMANTIC.md
- Datasheet.md -- DEL-04-03_ElectricalEnergyEfficiency/Datasheet.md
- Specification.md -- DEL-04-03_ElectricalEnergyEfficiency/Specification.md
- Guidance.md -- DEL-04-03_ElectricalEnergyEfficiency/Guidance.md
- Procedure.md -- DEL-04-03_ElectricalEnergyEfficiency/Procedure.md
- _REFERENCES.md -- DEL-04-03_ElectricalEnergyEfficiency/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 4
  - Specification: 8
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 3  B: 3  C: 2  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition TBDs weaken prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Addendum 03 solar provisions well covered; VFD application lacks mandatory framing |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Compliance pathways adequately described across docs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit trail provisions for code-edition confirmations |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-7 provides thorough procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps well articulated in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Review steps in Procedure Step 7 adequately cover process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-EEE-04 lifecycle cost framing covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off tables in Guidance demonstrate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | TCO arguments and payback estimates address worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Review steps and verification criteria address quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Clarify which edition of NECB, Alberta Building Code, CEC, and IES standards is applicable; replace "edition TBD by AHJ" with a concrete baseline assumption (e.g., "NECB 2020 or as confirmed by AHJ") | Multiple standards listed with "edition TBD" weakens prescriptive direction; an evaluator or implementer cannot determine which normative baseline applies | Datasheet.md | Attributes table (rows: Primary code framework, Lighting standard); Conditions table; Standards table in Specification.md | -- | Electrical Lead / AHJ | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Add mandatory language for VFD application on variable-load motors (R-EEE-05 currently states "Selection criteria" but does not require VFDs; Procedure Step 3.2 recommends them) | Specification R-EEE-05 describes motor efficiency standard selection but VFDs are only "consider" in Procedure; for variable-load fans and pumps, VFD is standard mandatory practice for energy efficiency | Specification.md; Procedure.md | R-EEE-05 (Specification); Step 3.2 (Procedure) | -- | Electrical Engineer | TBD |
| A-003 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a verification step or checklist item in Step 7 to confirm that all code-edition ASSUMPTIONs have been resolved or formally deferred before narrative finalization | Multiple code-edition TBDs exist (NECB, IES, CEC, ABC) but no review step specifically addresses their resolution or escalation; regulatory audit cannot be performed against unresolved standards | Procedure.md | Step 7: Review and Approval | -- | Design Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing quantitative LPD targets |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence levels appropriate given proposal stage |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Cold Storage electrical load data absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement approaches consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Utility rate assumption missing for lifecycle cost |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Sufficient context provided for proposal stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of scope elements is comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of electrical EE well demonstrated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise level appropriate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery adequately demonstrated |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment shown in trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequate in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view adequately presented |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Specification | Specification | Add NECB Lighting Power Density (LPD) limit targets (W/m2) for each major zone type as essential factual data in the narrative requirements or Datasheet | Guidance C-EEE-01 discusses IES vs. NECB LPD trade-off but no document provides the actual LPD numeric limits the design must meet; this is an essential fact for compliance verification | Specification.md; Guidance.md | R-EEE-01 (Specification); C-EEE-01 (Guidance) | -- | Electrical Engineer / NECB reference | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a Cold Storage electrical load summary (estimated connected load, number of circuits, lighting fixture count estimate) to Datasheet Conditions or Construction section | Cold Storage is addressed in Guidance (C-EEE-03) and Procedure (Step 2 fixture table) but Datasheet has only a brief exclusion note; no factual load data recorded for the 20-year building | Datasheet.md | Conditions table (Cold Storage exclusion row) | -- | Electrical Engineer | TBD |
| B-003 | B:information:necessity | TBD_Question | Guidance | Guidance | Record TBD: What is the assumed electrical utility rate ($/kWh) for lifecycle cost analysis? Source from local utility (Fortis Alberta or equivalent) or Owner | Guidance P-EEE-04 and trade-off tables reference energy cost reduction and payback periods but no utility rate is stated; this essential input is needed for any quantitative lifecycle cost argument | Guidance.md | P-EEE-04: Lifecycle Cost Justifies Efficiency Investment; T-EEE-01 | -- | Electrical Engineer / Owner | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | CEC not covered in Specification requirements |
| C:normative:sufficiency | normative | sufficiency | Compliance Adequacy | 0 | NO_ITEMS | Compliance adequacy well established for Addendum 03 |
| C:normative:completeness | normative | completeness | Exhaustive Compliance | 0 | NO_ITEMS | Compliance coverage is thorough for proposal stage |
| C:normative:consistency | normative | consistency | Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are consistent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites well documented in Procedure |
| C:operative:sufficiency | operative | sufficiency | Operational Competence | 0 | NO_ITEMS | Competence requirements adequately covered |
| C:operative:completeness | operative | completeness | Comprehensive Implementation | 0 | NO_ITEMS | Implementation coverage is comprehensive |
| C:operative:consistency | operative | consistency | Process Uniformity | 1 | HAS_ITEMS | Terminology inconsistency for motor standards |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Merit arguments well presented |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Appraisal | 0 | NO_ITEMS | Appraisal is defensible at proposal stage |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Valuation includes capital, operating, maintenance |
| C:evaluative:consistency | evaluative | consistency | Value Consistency | 0 | NO_ITEMS | Value arguments consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add a requirement (or note under R-EEE-06 or new R-EEE-08) addressing CEC Part I compliance for metering, wiring methods, and service entrance provisions as they relate to the energy efficiency narrative | CEC Part I is listed in Specification Standards table and Procedure Prerequisites but has no corresponding Specification requirement; the regulatory imperative for wiring compliance is unstated | Specification.md | Standards table; Requirements section (no CEC-specific requirement) | -- | Electrical Engineer | TBD |
| C-002 | C:operative:consistency | Normalization | Multi | Guidance | Normalize motor efficiency standard terminology: Datasheet uses "NEMA Premium Efficiency or Canadian equivalent (CSA equivalent)"; Specification R-EEE-05 uses "recognized motor efficiency standard"; Procedure uses "NEMA Premium or CSA C390 equivalent (IE3 category)"; Guidance does not specify a standard name. Align on a single canonical reference across all docs | Three different phrasings for the same motor efficiency standard creates ambiguity about whether NEMA Premium, CSA C390, or IE3 is the baseline; risks procurement specification drift | Datasheet.md; Specification.md; Procedure.md | Attributes table (Datasheet); R-EEE-05 (Specification); Step 3.2 (Procedure) | -- | Electrical Lead | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Threshold | 0 | NO_ITEMS | Thresholds adequately identified |
| F:normative:sufficiency | normative | sufficiency | Calibrated Regulatory Scope | 1 | HAS_ITEMS | Alberta-specific provisions uncalibrated |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Regulatory coverage is thorough for scope |
| F:normative:consistency | normative | consistency | Principled Regulatory Alignment | 0 | NO_ITEMS | Alignment is principled across docs |
| F:operative:necessity | operative | necessity | Critical Process Foundation | 0 | NO_ITEMS | Process foundations well established |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Readiness | 1 | HAS_ITEMS | Readiness verification gap for DEL-02-05 dependency |
| F:operative:completeness | operative | completeness | Total Implementation Mastery | 0 | NO_ITEMS | Implementation coverage comprehensive |
| F:operative:consistency | operative | consistency | Harmonized Process Discipline | 0 | NO_ITEMS | Process discipline consistent |
| F:evaluative:necessity | evaluative | necessity | Foundational Value Criterion | 0 | NO_ITEMS | Value criteria well founded |
| F:evaluative:sufficiency | evaluative | sufficiency | Evidenced Merit Sufficiency | 1 | HAS_ITEMS | Energy savings estimates lack methodology disclosure |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Accounting | 0 | NO_ITEMS | Value accounting covers capital, operating, maintenance |
| F:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value arguments coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify whether Alberta Building Code has energy-specific amendments beyond NECB (e.g., NECB adoption pathway, provincial energy performance requirements); add a Conditions row or Attributes note | Datasheet lists "NECB or applicable provincial equivalent; Alberta Building Code" as separate items but does not clarify the relationship (ABC adopts NECB with amendments? or separate code?); scope boundary for regulatory sufficiency is unclear | Datasheet.md | Attributes table (Primary code framework) | -- | AHJ / Electrical Engineer | TBD |
| F-002 | F:operative:sufficiency | VerificationGap | Procedure | Procedure | Add a gate check or dependency tracking mechanism in Step 1 or Step 6 to verify that DEL-02-05, DEL-04-01, and DEL-04-02 have reached minimum "draft-stable" before narrative assembly begins | Procedure Notes mention that Steps 2-5 should begin when drafts are available and Step 6 requires draft-stable, but no formal verification step confirms readiness; execution could proceed with insufficient upstream inputs | Procedure.md | Step 1; Step 6; Notes section | -- | Design Manager | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add a note in trade-off tables (T-EEE-01, T-EEE-03) disclosing the basis for energy savings percentage estimates and payback period estimates (e.g., source: industry benchmarks, manufacturer data, engineering judgment) | Trade-off tables cite specific percentage savings (60-70%, 40-50%) and payback periods (8-10 years, 12-15 years) but do not disclose whether these are from manufacturer data, ASHRAE benchmarks, or engineering judgment; evidenced merit requires transparent methodology | Guidance.md | T-EEE-01; T-EEE-03 | -- | Electrical Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Prescriptive Resolution | 0 | NO_ITEMS | Prescriptive direction adequately resolved |
| D:normative:applying | normative | applying | Bounded Mandatory Action | 0 | NO_ITEMS | Mandatory actions well bounded |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance determination framework in place |
| D:normative:reviewing | normative | reviewing | Unified Compliance Audit | 0 | NO_ITEMS | Audit approach unified across review steps |
| D:operative:guiding | operative | guiding | Grounded Process Direction | 0 | NO_ITEMS | Process direction well grounded in Procedure |
| D:operative:applying | operative | applying | Confirmed Practical Delivery | 1 | HAS_ITEMS | Delivery confirmation for Cold Storage |
| D:operative:judging | operative | judging | Conclusive Performance Judgment | 0 | NO_ITEMS | Performance judgment criteria established |
| D:operative:reviewing | operative | reviewing | Disciplined Process Review | 0 | NO_ITEMS | Review discipline adequate |
| D:evaluative:guiding | evaluative | guiding | Anchored Value Orientation | 0 | NO_ITEMS | Value orientation anchored in lifecycle cost |
| D:evaluative:applying | evaluative | applying | Substantiated Merit Practice | 1 | HAS_ITEMS | Emergency lighting strategy merit gap |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 0 | NO_ITEMS | Worth judgments appropriately framed |
| D:evaluative:reviewing | evaluative | reviewing | Integrated Quality Appraisal | 0 | NO_ITEMS | Quality appraisal integrated across review steps |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:applying | VerificationGap | Specification | Specification | Add verification criteria for Cold Storage lighting provisions under R-EEE-01 or as a separate note; currently no verification method addresses Cold Storage zone explicitly | Specification R-EEE-01 verification refers to "major space types in the Public Services Building" but Cold Storage is a separate building; Guidance C-EEE-03 and Procedure Step 2.1 include Cold Storage fixtures but Specification verification does not confirm Cold Storage coverage | Specification.md | R-EEE-01 Verification; Verification table (R-EEE-01 row) | -- | Electrical Engineer | TBD |
| D-002 | D:evaluative:applying | MissingSlot | Specification | Specification | Add requirement or verification note addressing emergency/egress lighting energy efficiency approach (LED emergency fixtures, generator-backed lighting circuits) as distinct from general lighting | Guidance P-EEE-01 identifies emergency egress lighting reliability as primary design constraint and Datasheet Conditions mention generator-backed sub-circuits, but no Specification requirement addresses the energy efficiency approach for emergency/egress lighting specifically; this is a substantive merit gap for a 24/7 fire hall | Specification.md; Guidance.md | P-EEE-01 (Guidance); Conditions table row: Generator electrical interface (Datasheet) | -- | Electrical Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Anchor | 0 | NO_ITEMS | Foundational directives well anchored |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Adequacy | 0 | NO_ITEMS | Directional adequacy justified |
| X:guiding:completeness | guiding | completeness | Holistic Directive Coverage | 0 | NO_ITEMS | Directive coverage holistic |
| X:guiding:consistency | guiding | consistency | Steady Directive Coherence | 0 | NO_ITEMS | Directives coherent |
| X:applying:necessity | applying | necessity | Validated Practice Foundation | 1 | HAS_ITEMS | Acceptance criteria gap for metering |
| X:applying:sufficiency | applying | sufficiency | Confirmed Practice Adequacy | 1 | HAS_ITEMS | Sensor technology selection unverified |
| X:applying:completeness | applying | completeness | Exhaustive Practice Coverage | 0 | NO_ITEMS | Practice coverage exhaustive for scope |
| X:applying:consistency | applying | consistency | Uniform Practice Discipline | 0 | NO_ITEMS | Practice discipline uniform |
| X:judging:necessity | judging | necessity | Decisive Adjudication Threshold | 1 | HAS_ITEMS | No quantitative acceptance threshold for energy savings |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment Standard | 0 | NO_ITEMS | Judgment standards substantiated |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope adequate |
| X:judging:consistency | judging | consistency | Consistent Adjudication Standard | 0 | NO_ITEMS | Adjudication standards consistent |
| X:reviewing:necessity | reviewing | necessity | Systematic Review Foundation | 1 | HAS_ITEMS | Cross-discipline sign-off mechanism missing in verification table |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Review Adequacy | 0 | NO_ITEMS | Review adequacy substantiated |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Coverage | 0 | NO_ITEMS | Review coverage exhaustive |
| X:reviewing:consistency | reviewing | consistency | Dependable Review Consistency | 0 | NO_ITEMS | Review consistency dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for R-EEE-07 metering that specify minimum number of sub-meter points (e.g., minimum 4 zones) and confirm meter communication protocol requirement (e.g., Modbus or equivalent) | Specification R-EEE-07 verification says "confirm major operational zones identified" but does not state a minimum zone count or protocol requirement; Procedure Step 5.2 specifies 5 zones and Modbus but Specification verification does not validate these specifics | Specification.md; Procedure.md | R-EEE-07 Verification (Specification); Step 5.2 (Procedure) | -- | Electrical Engineer | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add verification criterion under R-EEE-02 confirming that sensor technology selection (PIR vs. ultrasonic vs. dual-technology) is justified per zone characteristics (e.g., bay height, temperature range, occupancy pattern) | R-EEE-02 verification states "sensor technology selected" but does not require justification for the selection; in apparatus bays (high-bay, vehicle movement) and Cold Storage (cold temperature), sensor type selection is a non-trivial design decision | Specification.md | R-EEE-02 Verification | -- | Electrical Engineer | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add a quantitative or qualitative acceptance threshold for overall electrical energy reduction (e.g., "narrative shall demonstrate minimum X% reduction vs. code baseline" or "narrative shall include estimated kWh reduction summary") | Specification requirements describe what the narrative must contain but no requirement or verification criterion sets a threshold for the energy savings outcome; without a threshold, adjudication of narrative quality is subjective | Specification.md | Requirements section (entire); Verification table (entire) | -- | Electrical Engineer / Design Manager | TBD |
| X-004 | X:reviewing:necessity | MissingSlot | Specification | Specification | Add a verification row or note in the Verification table confirming that cross-discipline sign-off from DEL-02-05, DEL-04-01, and DEL-04-02 authors is a verification requirement (currently only described in Procedure Step 7.2) | Specification Verification table lists verification methods and timing but does not include cross-discipline confirmation as a formal verification step; Procedure Step 7.2 describes it but Specification should own the requirement | Specification.md; Procedure.md | Verification table (Specification); Step 7.2 (Procedure) | -- | Design Manager | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Authoritative Compliance Foundation | 0 | NO_ITEMS | Foundation adequately authoritative |
| E:normative:sufficiency | normative | sufficiency | Validated Regulatory Sufficiency | 0 | NO_ITEMS | Sufficiency validated at proposal stage |
| E:normative:completeness | normative | completeness | Absolute Regulatory Completeness | 1 | HAS_ITEMS | Exterior lighting regulatory gap |
| E:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Integrity harmonized across docs |
| E:operative:necessity | operative | necessity | Grounded Operational Foundation | 0 | NO_ITEMS | Foundation well grounded |
| E:operative:sufficiency | operative | sufficiency | Confirmed Operational Adequacy | 0 | NO_ITEMS | Adequacy confirmed |
| E:operative:completeness | operative | completeness | Total Operational Coverage | 0 | NO_ITEMS | Operational coverage is total for scope |
| E:operative:consistency | operative | consistency | Dependable Operational Uniformity | 1 | HAS_ITEMS | IP rating inconsistency |
| E:evaluative:necessity | evaluative | necessity | Essential Value Foundation | 0 | NO_ITEMS | Value foundation essential and present |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Adequacy | 0 | NO_ITEMS | Adequacy substantiated |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Value Completeness | 0 | NO_ITEMS | Value completeness comprehensive |
| E:evaluative:consistency | evaluative | consistency | Dependable Value Integrity | 0 | NO_ITEMS | Integrity dependable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | RationaleGap | Guidance | Guidance | Add a Consideration (C-EEE-06 or equivalent) addressing exterior/site lighting regulatory requirements: dark-sky compliance rationale, municipal bylaw requirements for exterior lighting, and light trespass considerations | Guidance P-EEE-03 zone table mentions exterior lighting as "motion-triggered, dark-sky compliant; cold-start capable" but provides no consideration section explaining dark-sky compliance rationale or municipal regulatory context; Procedure Step 2 includes exterior fixtures but Guidance lacks the regulatory rationale | Guidance.md; Procedure.md | P-EEE-03 zone table (Guidance); Step 2.1 fixture table (Procedure) | -- | Electrical Engineer | TBD |
| E-002 | E:operative:consistency | Normalization | Multi | Datasheet | Normalize IP rating specification: Guidance C-EEE-02 states "minimum IP54 or IP65 for wet/wash-down zones"; Procedure Step 2.1 fixture table uses "IP54+" for apparatus bays; Guidance EX-EEE-01 uses "minimum IP54 rated". Clarify whether IP54 or IP65 is the baseline for apparatus bay wash-down zones with bay sumps | Inconsistent IP rating references across Guidance and Procedure could lead to under-specification for wash-down zones where bay sumps are present (Addendum 03 requirement); the distinction between IP54 and IP65 is material for wet environments | Guidance.md; Procedure.md | C-EEE-02 (Guidance); EX-EEE-01 (Guidance); Step 2.1 (Procedure) | -- | Electrical Engineer | TBD |

---

*End of Semantic Lensing Register*
