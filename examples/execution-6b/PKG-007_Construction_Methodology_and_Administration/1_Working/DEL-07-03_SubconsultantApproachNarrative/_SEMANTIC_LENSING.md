# Semantic Lensing Register: DEL-07-03 Subconsultant Approach Narrative

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-007_Construction_Methodology_and_Administration/1_Working/DEL-07-03_SubconsultantApproachNarrative
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-07-03_SubconsultantApproachNarrative/_CONTEXT.md
- _STATUS.md — DEL-07-03_SubconsultantApproachNarrative/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-07-03_SubconsultantApproachNarrative/_SEMANTIC.md (8 matrices parsed; 7 in scope per protocol: A, B, C, F, D, X, E)
- Datasheet.md — DEL-07-03_SubconsultantApproachNarrative/Datasheet.md
- Specification.md — DEL-07-03_SubconsultantApproachNarrative/Specification.md
- Guidance.md — DEL-07-03_SubconsultantApproachNarrative/Guidance.md
- Procedure.md — DEL-07-03_SubconsultantApproachNarrative/Procedure.md
- _REFERENCES.md — DEL-07-03_SubconsultantApproachNarrative/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 14
- By document:
  - Datasheet: 2
  - Specification: 5
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 3  B: 2  C: 2  F: 2  D: 1  X: 2  E: 2
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | APEGA/AAA licensing requirement is assumption-based |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Six-discipline requirement well covered across all docs |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for APEGA/AAA verification |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | RFP page 21 inspection and certification obligations well documented |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Step A-F procedure is clear and well-sequenced |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Escalation timeframes stated in Guidance but absent from Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | V-001 through V-015 checks are adequate |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Cross-document checks in Step E are thorough |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | OBJ-002 and OBJ-006 alignment described in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Experience alignment principle P-004 addresses this |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scoring context in Datasheet and Guidance adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Peer review step F covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify APEGA P.Eng. and AAA registration requirement: currently labeled "ASSUMPTION -- standard provincial requirement" in Standards table. Either confirm as normative requirement with cited authority or explicitly flag as TBD pending legal review. | The Standards table lists APEGA and AAA as "Normative -- implied by Alberta regulatory context" but qualifies this as an ASSUMPTION. For a prescriptive direction lens, the normative status of professional licensing should be unambiguous -- it is either required or it is not. The assumption label creates uncertainty about whether this is a deliverable requirement or merely informational. | Specification.md | Standards table, APEGA row | -- | Specification.md (Standards table) | TBD |
| A-002 | A:normative:judging | VerificationGap | Specification | Specification | Add verification check for professional licensing: confirm all named discipline consultants hold valid APEGA P.Eng. (engineers) or AAA registration (architect) at time of proposal submission. | Specification R-001 requires each discipline position to include "the assigned firm or individual, their primary role, and a brief statement of relevant experience" but does not include verification of professional registration. Since APEGA/AAA is listed as normative in the Standards table, a compliance determination mechanism is needed. | Specification.md | R-001 Verification; Standards table | -- | Specification.md (Verification table) | TBD |
| A-003 | A:operative:applying | MissingSlot | Procedure | Procedure | Add escalation timeframes to Step C: Guidance EX-002 states "PM escalates any coordination conflicts to the Design-Builder principal within 24 hours" and "unresolved within 48 hours" but Procedure Step C item 1 only says "escalation path for coordination conflicts" without specifying timeframes. | Guidance provides specific operational timeframes (24-hour and 48-hour escalation windows) that are absent from the Procedure. Procedure Step C should carry forward these timeframes or reference Guidance for them so they are not lost in execution. | Procedure.md; Guidance.md | Procedure Step C item 1; Guidance EX-002 | -- | Procedure.md (Step C) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Geotechnical report date discrepancy investigation dates vs report date |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | USG1123 data elements thoroughly documented |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | 18-borehole coverage, stratigraphy, bearing values all documented |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | USG1123 parameter values consistent across all four documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | RFP scoring context and evaluation weights documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | DEC-013 context and OSR §10.3.2 context well established |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Addendum 03 references appear in Procedure but not in Datasheet or Specification |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging on geotech sufficiency is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Foundation design principles well conveyed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Structural/civil review protocol adequately described |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | All three foundation system options documented |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Geotech knowledge base consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | DEC-013 risk acceptance rationale present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Level 1/2/3 detail guidance in Guidance C-002 adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Trade-offs T-001 through T-003 in Guidance cover key tensions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | DEC-013 reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add Addendum 03 as a source in the Datasheet References table. Procedure Step C references "Addendum 03 §1.17" (solar-ready provisions) and "Addendum 03 §1.8" (apparatus bay sump), but Datasheet and Specification do not list Addendum 03 among their sources. | Addendum 03 contains project-specific interface requirements (solar-ready electrical, apparatus bay sump integration) that are referenced in Procedure Step C but lack traceability from Datasheet. An essential fact source is missing from the data record. | Datasheet.md; Procedure.md | Datasheet References table; Procedure Step C items 3 bullet 2 and bullet 4 | -- | Datasheet.md (References table) | TBD |
| B-002 | B:information:completeness | MissingSlot | Specification | Specification | Add Addendum 03 to the Specification Standards table as a normative reference, with applicable sections (§1.8 apparatus bay sump, §1.17 solar-ready provisions) noted. These interface requirements affect R-004 (interface coordination approach). | Procedure Step C names specific Addendum 03 sections as inputs to interface coordination, but Specification R-004 does not acknowledge Addendum 03 as a source for interface requirements. The comprehensive account of normative inputs is incomplete in Specification. | Specification.md; Procedure.md | Specification Standards table; Specification R-004; Procedure Step C item 3 | -- | Specification.md (Standards table; R-004) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Foundation | 0 | NO_ITEMS | CCDC 14-2013, ABC, RFP §7.3.4 all present |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy Threshold | 1 | HAS_ITEMS | Specification R-001 verification is checklist-only, lacks measurable threshold |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Standards table in Specification covers applicable codes |
| C:normative:consistency | normative | consistency | Regulatory Conformance Integrity | 0 | NO_ITEMS | Regulatory references consistent across documents |
| C:operative:necessity | operative | necessity | Critical Execution Imperative | 0 | NO_ITEMS | Procedure Steps A-F cover critical execution path |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability Baseline | 1 | HAS_ITEMS | R-001 "brief statement of relevant experience" lacks minimum threshold |
| C:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Procedure is comprehensive with 15 verification checks |
| C:operative:consistency | operative | consistency | Integrated Operational Alignment | 0 | NO_ITEMS | Step E cross-document checks maintain alignment |
| C:evaluative:necessity | evaluative | necessity | Essential Worth Recognition | 0 | NO_ITEMS | OBJ-002 and OBJ-006 scoring context present |
| C:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Merit Sufficiency | 0 | NO_ITEMS | Guidance P-004 addresses experience alignment |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Trade-offs cover page budget, specificity, and risk |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Coherence | 0 | NO_ITEMS | Consistent evaluation framing across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen R-001 verification: currently "All six discipline categories present and addressed in narrative." Consider adding: each named firm must include at minimum (a) firm name, (b) lead individual name, (c) primary role, (d) brief relevant experience. These elements are stated in R-001 body text but the Verification line only checks for presence, not content adequacy. | Under the "Mandated Adequacy Threshold" lens, the verification criterion for R-001 tests only for presence of the six categories, not whether each entry meets the minimum content standard described in R-001's own body text. The adequacy threshold is implicit rather than enforceable. | Specification.md | R-001 body text vs. R-001 Verification line | -- | Specification.md (R-001 Verification) | TBD |
| C-002 | C:operative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for what constitutes "relevant experience" in P-004. The principle says "relevant prior experience on similar municipal facilities (fire halls, public works operations centres, multi-use municipal buildings)" but does not explain how evaluators or the team should judge sufficiency -- e.g., minimum number of comparable projects, recency, geographic relevance, or scale. | The "Demonstrated Capability Baseline" lens highlights that the documents prescribe experience alignment but provide no threshold for what makes experience "sufficient." Without guidance on minimum expectations, the team cannot reliably assess whether consultant credentials meet the standard. | Guidance.md | P-004: Experience Alignment Strengthens OBJ-006 | -- | Guidance.md (P-004) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Conformance Basis | 0 | NO_ITEMS | RFP §7.3.4 requirements fully traced to R-001 through R-006 |
| F:normative:sufficiency | normative | sufficiency | Prescribed Compliance Capacity | 0 | NO_ITEMS | DEC-013 sufficiency framework adequate |
| F:normative:completeness | normative | completeness | Total Regulatory Dominion | 1 | HAS_ITEMS | Fire protection engineering scope boundary unclear |
| F:normative:consistency | normative | consistency | Harmonized Mandate Uniformity | 0 | NO_ITEMS | Mandate language consistent |
| F:operative:necessity | operative | necessity | Indispensable Operational Capacity | 0 | NO_ITEMS | Team assembly prerequisites clear |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Operational Proficiency | 0 | NO_ITEMS | Step B geotech review protocol is detailed |
| F:operative:completeness | operative | completeness | Absolute Operational Comprehension | 0 | NO_ITEMS | Procedure covers all operational aspects |
| F:operative:consistency | operative | consistency | Systematic Delivery Integrity | 0 | NO_ITEMS | Cross-document consistency checks adequate |
| F:evaluative:necessity | evaluative | necessity | Vital Value Discernment | 1 | HAS_ITEMS | No explicit scoring weight allocation guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Value Fitness | 0 | NO_ITEMS | Guidance trade-offs cover value considerations |
| F:evaluative:completeness | evaluative | completeness | Absolute Value Accounting | 0 | NO_ITEMS | Both scoring objectives addressed |
| F:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Evaluation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:completeness | TBD_Question | Specification | Specification | Clarify whether fire protection engineering is within the Mechanical consultant's scope or requires a separate specialty consultant. Specification R-006 ASSUMPTION lists "fire protection engineering (if separate from mechanical consultant's scope)" and Datasheet lists it under Mechanical, but Guidance C-003 Option 1 lists it as a potential separate specialty. A definitive scope assignment is needed. | Under the "Total Regulatory Dominion" lens, fire protection engineering is a regulated discipline in Alberta. The documents give contradictory signals about whether it is included in the Mechanical scope or is a separate specialty. This ambiguity could result in a regulatory gap if neither party assumes responsibility. The question requires human/team input to resolve. | Specification.md; Guidance.md; Datasheet.md | Specification R-006 ASSUMPTION; Guidance C-003; Datasheet Conditions "Required Disciplines" row | -- | Human ruling required (team scope decision) | TBD |
| F-002 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add guidance on how the 3-point Construction Methodology sub-score and the 15-point Team Qualifications score should be balanced in narrative emphasis. Currently Guidance states both scoring objectives but does not explain how to weight narrative attention between them given limited page budget. | Under the "Vital Value Discernment" lens, the narrative serves two scoring functions with different point values (3 pts vs 15 pts). Without guidance on relative emphasis, the team may under-invest in the higher-value dimension. The trade-off T-001 discusses page budget but not scoring weight allocation. | Guidance.md | Purpose section; T-001 | -- | Guidance.md (new consideration or addition to T-001) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Prescriptive Authority | 0 | NO_ITEMS | RFP §7.3.4 as prescriptive authority is settled |
| D:normative:applying | normative | applying | Compulsory Regulatory Execution | 0 | NO_ITEMS | Regulatory obligations well-documented |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | DEC-013 provides definitive geotech ruling |
| D:normative:reviewing | normative | reviewing | Settled Governance Verification | 0 | NO_ITEMS | Verification table in Specification adequate |
| D:operative:guiding | operative | guiding | Settled Operational Steering | 0 | NO_ITEMS | Procedure steps provide clear operational steering |
| D:operative:applying | operative | applying | Settled Delivery Competence | 0 | NO_ITEMS | Team assembly and review process settled |
| D:operative:judging | operative | judging | Settled Performance Adjudication | 0 | NO_ITEMS | V-001 to V-015 provide performance checks |
| D:operative:reviewing | operative | reviewing | Settled Process Verification | 1 | HAS_ITEMS | Step E lacks a verification check for geotechnical monitoring service classification |
| D:evaluative:guiding | evaluative | guiding | Purposeful Merit Steering | 0 | NO_ITEMS | Guidance principles steer toward merit |
| D:evaluative:applying | evaluative | applying | Settled Worth Realization | 0 | NO_ITEMS | Examples EX-001 to EX-004 support worth realization |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | Scoring context established |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Reappraisal | 0 | NO_ITEMS | Step F peer review covers quality reappraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:reviewing | VerificationGap | Procedure | Procedure | Add a verification check (or add to Step E cross-check matrix) confirming that any proposed geotechnical monitoring service is classified as construction quality control and not as additional investigation, with explicit DEC-013 compliance noted. Currently R-006 and Guidance C-003 discuss this distinction qualitatively, but Procedure Step E cross-checks do not verify it. | Under the "Settled Process Verification" lens, the distinction between construction-phase geotechnical monitoring and additional investigation is critical to DEC-013 compliance. Specification R-006 notes this distinction; Guidance C-003 Option 1 elaborates. However, Procedure Step E's cross-check matrix does not include a specific pass/fail check for this classification. A process verification gap exists. | Procedure.md; Specification.md; Guidance.md | Procedure Step E cross-check table; Specification R-006 Note on geotechnical monitoring; Guidance C-003 Option 1 | -- | Procedure.md (Step E cross-check table) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Directional Mandate | 0 | NO_ITEMS | RFP §7.3.4 directive is commanding and clear |
| X:guiding:sufficiency | guiding | sufficiency | Guided Sufficiency Benchmark | 0 | NO_ITEMS | USG1123 sufficiency framework is guided |
| X:guiding:completeness | guiding | completeness | Comprehensive Directional Domain | 0 | NO_ITEMS | Scope includes/excludes well defined |
| X:guiding:consistency | guiding | consistency | Unified Directional Harmony | 0 | NO_ITEMS | Direction consistent across documents |
| X:applying:necessity | applying | necessity | Mandatory Implementation Activation | 1 | HAS_ITEMS | No explicit trigger or gate for when Step B must be complete relative to proposal timeline |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Execution Threshold | 0 | NO_ITEMS | Procedure completion checks adequate |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Coverage | 0 | NO_ITEMS | Steps A-F cover full implementation |
| X:applying:consistency | applying | consistency | Harmonized Execution Integrity | 0 | NO_ITEMS | Execution steps consistent |
| X:judging:necessity | judging | necessity | Binding Adjudicative Verdict | 0 | NO_ITEMS | DEC-013 provides binding verdict on geotech scope |
| X:judging:sufficiency | judging | sufficiency | Definitive Sufficiency Verdict | 0 | NO_ITEMS | Sufficiency determination protocol adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 0 | NO_ITEMS | Verification checks cover full scope |
| X:judging:consistency | judging | consistency | Confirmed Adjudicative Integrity | 0 | NO_ITEMS | Adjudicative criteria consistent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Reassessment Validation | 1 | HAS_ITEMS | No provision for what happens if USG1123 applicability cannot be confirmed |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Reassessment Threshold | 0 | NO_ITEMS | Step B output requirements clear |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Reassessment Audit | 0 | NO_ITEMS | Step E cross-checks are comprehensive |
| X:reviewing:consistency | reviewing | consistency | Validated Reassessment Harmony | 0 | NO_ITEMS | Review processes harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a milestone or timeline gate for Step B completion relative to the proposal development schedule. Step B is listed as a prerequisite for Step D but no calendar or relative deadline is specified. For mandatory implementation activation, the team needs to know when the geotechnical sufficiency memo must be in hand. | Under the "Mandatory Implementation Activation" lens, Step B's completion is critical-path for Step D (narrative drafting) but lacks a temporal gate. If the structural/civil consultant delays the USG1123 review, the narrative cannot be drafted, creating schedule risk. A deadline or milestone trigger is needed. | Procedure.md | Step B "When" clause; Prerequisites table | -- | Procedure.md (Step B timing) | TBD |
| X-002 | X:reviewing:necessity | MissingSlot | Multi | Guidance | Add contingency guidance for the scenario where the structural/civil consultant cannot confirm USG1123 applicability to the current building program per §2.2. Currently all documents assume the sufficiency determination will be positive (per DEC-013), but no document describes the reassessment path if the consultant determines the report is not applicable -- other than a brief mention in Procedure Step B item 4 ("escalate immediately to PM"). Add to Guidance a consideration for this contingency: who decides, what is the timeline, and what happens to DEC-013. | Under the "Mandatory Reassessment Validation" lens, the documents treat the USG1123 sufficiency determination as a foregone conclusion aligned with DEC-013. However, DEC-013 is a project decision, not a technical finding. If the structural/civil consultant determines USG1123 is inapplicable, the path forward is underspecified beyond "escalate to PM." A contingency protocol is missing. | Procedure.md; Guidance.md; Specification.md | Procedure Step B item 4; Specification R-003 item 6; Guidance P-006 | -- | Guidance.md (new consideration C-005 or addition to P-006) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Irrevocable Regulatory Command | 0 | NO_ITEMS | Regulatory commands (RFP, ABC, CCDC 14) established |
| E:normative:sufficiency | normative | sufficiency | Definitive Adequacy Standard | 0 | NO_ITEMS | Adequacy standards defined |
| E:normative:completeness | normative | completeness | Total Governance Jurisdiction | 1 | HAS_ITEMS | Contract form (CCDC 14 + Appendix J) implications not traced to subconsultant agreements |
| E:normative:consistency | normative | consistency | Definitive Governance Integrity | 0 | NO_ITEMS | Governance references consistent |
| E:operative:necessity | operative | necessity | Binding Operational Mobilization | 0 | NO_ITEMS | Team mobilization requirements present |
| E:operative:sufficiency | operative | sufficiency | Confirmed Delivery Adequacy | 0 | NO_ITEMS | Delivery adequacy checks in procedure |
| E:operative:completeness | operative | completeness | Total Operational Jurisdiction | 0 | NO_ITEMS | Operational scope coverage complete |
| E:operative:consistency | operative | consistency | Confirmed Operational Coherence | 0 | NO_ITEMS | Operations coherent across documents |
| E:evaluative:necessity | evaluative | necessity | Binding Worth Determination | 1 | HAS_ITEMS | No verification that narrative addresses both scoring dimensions |
| E:evaluative:sufficiency | evaluative | sufficiency | Confirmed Worth Sufficiency | 0 | NO_ITEMS | Worth sufficiency addressed through guidance trade-offs |
| E:evaluative:completeness | evaluative | completeness | Total Worth Jurisdiction | 0 | NO_ITEMS | Both OBJ-002 and OBJ-006 addressed |
| E:evaluative:consistency | evaluative | consistency | Definitive Worth Coherence | 0 | NO_ITEMS | Worth framing consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Multi | Datasheet | Normalize CCDC 14 reference across documents: Specification Standards table cites "CCDC 14-2013 + Appendix J" while Datasheet does not list CCDC 14 in its References table. Since the Design-Builder's obligation to manage subconsultants derives from CCDC 14, the Datasheet should include this reference for traceability. | Under the "Total Governance Jurisdiction" lens, the contract form (CCDC 14-2013) is the legal basis for Design-Builder subconsultant management obligations. Specification references it but Datasheet omits it. For total governance jurisdiction, all governance instruments should be traceable from the Datasheet's reference inventory. | Datasheet.md; Specification.md | Datasheet References table; Specification Standards table (CCDC 14-2013 row) | -- | Datasheet.md (References table) | TBD |
| E-002 | E:evaluative:necessity | VerificationGap | Specification | Specification | Add a verification check confirming the narrative explicitly addresses both scoring dimensions: Construction Methodology (OBJ-002, 3 pts) and Team Qualifications (OBJ-006, 15 pts). Currently no V-check ensures both evaluation objectives are demonstrably served by the final narrative content. | Under the "Binding Worth Determination" lens, the deliverable serves two scoring objectives with different point values. The Verification table (V-001 to V-015) checks content completeness but does not verify that the narrative is structured to serve both scoring dimensions. A binding worth determination requires confirmation that evaluation objectives are addressed. | Specification.md; Guidance.md | Specification Verification table; Guidance Purpose section | -- | Specification.md (Verification table) | TBD |

---

*End of Semantic Lensing Register*
