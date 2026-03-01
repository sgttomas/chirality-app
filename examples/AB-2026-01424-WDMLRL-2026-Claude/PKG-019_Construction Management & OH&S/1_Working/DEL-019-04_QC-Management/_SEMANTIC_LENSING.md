# Semantic Lensing Register: DEL-019-04 Construction Quality Control

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-019_Construction Management & OH&S/1_Working/DEL-019-04_QC-Management
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-019-04_QC-Management/_CONTEXT.md
- _STATUS.md — DEL-019-04_QC-Management/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-019-04_QC-Management/_SEMANTIC.md
- Datasheet.md — DEL-019-04_QC-Management/Datasheet.md
- Specification.md — DEL-019-04_QC-Management/Specification.md
- Guidance.md — DEL-019-04_QC-Management/Guidance.md
- Procedure.md — DEL-019-04_QC-Management/Procedure.md
- _REFERENCES.md — DEL-019-04_QC-Management/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 3
  - Specification: 9
  - Guidance: 5
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | QC Plan approval authority ambiguity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Alberta OHS Act clause gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Safety Code editions TBD |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately addressed |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase A-B-C provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are sufficiently operational |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative QC performance metrics defined |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit via weekly reporting and verification tables adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1-P6 principles cover value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | QC evaluation weighting (5%) documented in Datasheet |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Deficiency holdback mechanism documented |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Settled Integrity Review addressed via CCC process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Procedure | Specification | Clarify QC Plan approval authority: specify whether approval is internal (Project Manager), external (County), or both | Procedure Step A3 notes approval authority is "TBD — not explicitly stated in accessible sources"; this creates ambiguity about who must approve before construction can begin | Procedure.md | Steps > Phase A > A3. Obtain QC Plan Approval | — | PROPOSAL: Specification REQ-QC-01 should define the approval chain | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Add specific Alberta OHS Act clause references for Prime Contractor QC obligations; current text references the Act without identifying applicable sections | The Standards table in Specification lists Alberta OHS Act with "specific clause location TBD"; mandatory practice cannot be verified against unstated clauses | Specification.md | Standards table — Alberta Occupational Health and Safety Act row | — | PROPOSAL: Obtain and cite specific OHS Act sections (e.g., Part 37 re Prime Contractors) | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Identify specific editions of applicable Alberta Safety Codes for compliance verification; REQ-QC-10 currently references codes generically | Compliance determination requires known code edition baselines; current "specific applicable code editions are TBD" leaves judging incomplete | Specification.md | REQ-QC-10; Standards table — Alberta Safety Codes Act row | — | PROPOSAL: QC Plan author or design team to enumerate applicable code editions | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add quantitative QC performance metrics or KPIs (e.g., deficiency closure rate targets, inspection completion percentage targets) to enable performance assessment | No quantitative performance thresholds are defined; performance assessment relies solely on binary completion checks (done/not done) without measuring QC program effectiveness | Specification.md | entire document scanned | — | PROPOSAL: Specification or Guidance to define target KPIs | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 0 | NO_ITEMS | Essential facts adequately captured in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Testing acceptance criteria absent |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Documentation section in Specification enumerates record types |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | No measurement standards for inspection/test results |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Reporting signals through weekly meetings defined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for QC activities adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive account of QC scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally consistent in messaging |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance provides adequate foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 1 | HAS_ITEMS | QC Manager qualification requirements absent |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Comprehensive coverage across four documents |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs provide discernment framework |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment framework via conflict table and trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided through document set |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning reflected in Guidance principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria (pass/fail thresholds) for testing protocols in REQ-QC-05; currently requires tests be "documented" but does not define what constitutes adequate evidence of compliance | Without defined acceptance criteria, test results cannot be evaluated as sufficient evidence of quality; Procedure A6 defers to IFC specifications but no acceptance criteria are stated in Specification | Specification.md; Procedure.md | REQ-QC-05; Phase A > A6 | — | PROPOSAL: Specification to include reference to acceptance criteria per material/system type, or require QC Plan to define them | TBD |
| B-002 | B:data:consistency | MissingSlot | Specification | Specification | Add requirement for standardized measurement methods or reference standards for inspection and testing (e.g., ASTM, CSA test methods) to ensure reliable, repeatable measurements | No measurement standards are specified for QC inspections or testing; this risks inconsistent measurement approaches across inspectors or test events | Specification.md | Standards table; REQ-QC-05 | — | PROPOSAL: Specification Standards table to reference applicable test method standards once IFC specifications are available | TBD |
| B-003 | B:knowledge:sufficiency | MissingSlot | Specification | Specification | Add qualification or competency requirements for QC Manager (e.g., relevant experience, certifications, training) | REQ-QC-11 requires a QC Manager be assigned but specifies no qualifications; competent expertise is assumed but not defined, risking assignment of unqualified personnel | Specification.md | REQ-QC-11 | — | PROPOSAL: Specification to define minimum QC Manager qualifications or require proposal to state them | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Obligation | 0 | NO_ITEMS | Binding obligations clearly stated in Specification requirements |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Conformance | 1 | HAS_ITEMS | Conformance demonstration for subcontractor QC unclear |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Scope | 0 | NO_ITEMS | Regulatory scope adequately identified with appropriate TBDs |
| C:normative:consistency | normative | consistency | Invariant Adjudication | 0 | NO_ITEMS | Adjudication standards consistent across documents |
| C:operative:necessity | operative | necessity | Operational Criticality | 0 | NO_ITEMS | Critical operational steps defined in Procedure |
| C:operative:sufficiency | operative | sufficiency | Proficient Execution | 0 | NO_ITEMS | Execution steps are sufficiently detailed |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 0 | NO_ITEMS | Process coverage spans pre-construction through completion |
| C:operative:consistency | operative | consistency | Methodical Uniformity | 1 | HAS_ITEMS | Inspection report format not standardized |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Judgment | 0 | NO_ITEMS | Merit judgment framework present in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation | 0 | NO_ITEMS | Valuation basis via deficiency holdback documented |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Worth assessment framework adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Quality Judgment | 0 | NO_ITEMS | Quality judgment principles stated in Guidance P1-P6 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for REQ-QC-07 (Subcontractor QC Oversight) that specifies how subcontractor conformance is demonstrated beyond "subcontractor inspection records" | REQ-QC-07 verification states "subcontractor inspection records; reference to subcontractor performance evaluations" but does not define what constitutes demonstrated conformance for subcontractor work specifically | Specification.md | REQ-QC-07; Verification table | — | PROPOSAL: Define whether subcontractor work requires same inspection/sign-off rigor as direct Proponent work | TBD |
| C-002 | C:operative:consistency | Normalization | Multi | Guidance | Standardize inspection report format across documents; Procedure references "inspection report form" (B3) but no standard form or template is defined or referenced in any document | Methodical uniformity requires a consistent inspection report format; without one, different inspectors may produce incompatible records | Procedure.md; Specification.md | Phase B > B3; Documentation section | — | PROPOSAL: QC Plan to include or reference a standard inspection report template | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Definitive Statutory Mandate | 0 | NO_ITEMS | Statutory mandates identified (OHS Act, Safety Codes) with TBD details |
| F:normative:sufficiency | normative | sufficiency | Substantiated Compliance Threshold | 1 | HAS_ITEMS | Compliance thresholds not quantified |
| F:normative:completeness | normative | completeness | Total Prescriptive Coverage | 0 | NO_ITEMS | Prescriptive coverage adequate for current document maturity |
| F:normative:consistency | normative | consistency | Harmonized Compliance Standard | 0 | NO_ITEMS | Standards listed consistently across documents |
| F:operative:necessity | operative | necessity | Foundational Process Imperative | 0 | NO_ITEMS | Foundational processes defined in Procedure |
| F:operative:sufficiency | operative | sufficiency | Verified Procedural Competence | 1 | HAS_ITEMS | No procedural competence verification for inspection personnel |
| F:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Operational coverage is comprehensive |
| F:operative:consistency | operative | consistency | Integrated Procedural Discipline | 0 | NO_ITEMS | Procedure steps are internally consistent |
| F:evaluative:necessity | evaluative | necessity | Irreducible Quality Standard | 1 | HAS_ITEMS | Minimum quality standard not explicitly defined |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Appraisal | 0 | NO_ITEMS | Worth appraisal framework in place via holdback mechanism |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Merit Accounting | 0 | NO_ITEMS | Merit accounting through deficiency tracking adequate |
| F:evaluative:consistency | evaluative | consistency | Coherent Value Integrity | 0 | NO_ITEMS | Value integrity consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-QC-01 to define minimum QC Plan content requirements beyond the general list; current language "shall address construction oversight, material quality control, reporting, and communication processes" is broad and could be interpreted at varying levels of detail | Substantiated compliance threshold requires clear minimum content requirements; the current high-level description may result in an insufficient QC Plan that technically satisfies the requirement | Specification.md | REQ-QC-01 | — | PROPOSAL: Align minimum content list with Procedure A2 detailed list, or reference Procedure A2 as the authoritative content specification | TBD |
| F-002 | F:operative:sufficiency | MissingSlot | Procedure | Specification | Add requirement or procedure step for verifying that personnel conducting inspections (QC Manager or delegates) are competent to perform the specific inspections required | Verified procedural competence requires confirmation that inspection personnel are qualified; no qualification check or competency verification step exists in Procedure or Specification | Procedure.md; Specification.md | entire document scanned | — | PROPOSAL: Add competency verification as a prerequisite in Procedure or a requirement in Specification | TBD |
| F-003 | F:evaluative:necessity | WeakStatement | Guidance | Guidance | Clarify what constitutes the irreducible quality standard (minimum acceptable quality level) for this project; Guidance P1 discusses prevention over detection but does not define the baseline quality threshold | Without an explicit minimum quality standard, there is no clear floor against which to measure QC program performance; "final work meets specification requirements" (Specification REQ-QC-06) references specifications not yet available | Guidance.md; Specification.md | P1 — Prevention over detection; REQ-QC-06 | — | PROPOSAL: Guidance to articulate the minimum quality baseline once IFC specifications are available | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Governance Course | 0 | NO_ITEMS | Governance course established through QC Plan and Prime Contractor structure |
| D:normative:applying | normative | applying | Enforced Compliance Protocol | 0 | NO_ITEMS | Compliance enforcement via inspection hold points and deficiency tracking |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 1 | HAS_ITEMS | No explicit pass/fail criteria for final conformance determination |
| D:normative:reviewing | normative | reviewing | Definitive Compliance Review | 0 | NO_ITEMS | CCC process provides definitive review mechanism |
| D:operative:guiding | operative | guiding | Grounded Workflow Direction | 0 | NO_ITEMS | Procedure provides grounded workflow direction |
| D:operative:applying | operative | applying | Settled Work Deployment | 0 | NO_ITEMS | Work deployment steps defined in Procedure |
| D:operative:judging | operative | judging | Conclusive Capability Finding | 0 | NO_ITEMS | Capability findings via verification checks in Procedure |
| D:operative:reviewing | operative | reviewing | Systematic Routine Verification | 0 | NO_ITEMS | Routine verification via weekly reporting cycle |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Orientation | 0 | NO_ITEMS | Quality orientation settled through Guidance principles |
| D:evaluative:applying | evaluative | applying | Committed Worth Deployment | 0 | NO_ITEMS | Worth deployment via QC program implementation |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Verdict | 1 | HAS_ITEMS | No escalation path for disputed quality verdicts |
| D:evaluative:reviewing | evaluative | reviewing | Settled Integrity Review | 0 | NO_ITEMS | Integrity review via CCC and guarantee period |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add explicit pass/fail criteria for overall QC program conformance determination at construction completion; currently REQ-QC-06 requires "final work meets specification requirements" without defining how the conclusive conformance verdict is rendered | A conclusive conformance verdict requires defined pass/fail criteria; the current framework relies on zero open deficiencies but does not address how disputed conformance findings are resolved | Specification.md | REQ-QC-06; Verification table | — | PROPOSAL: Define the conformance determination process including who has authority to render the final verdict | TBD |
| D-002 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on escalation and dispute resolution process when QC findings are contested by subcontractors or when there is disagreement about whether a deficiency has been adequately remediated | No escalation or dispute resolution pathway is described for contested QC verdicts; this could delay deficiency closure and CCC issuance | Guidance.md | entire document scanned | — | PROPOSAL: Guidance Considerations section to address QC dispute resolution | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Steering Principle | 0 | NO_ITEMS | Steering principles articulated in Guidance |
| X:guiding:sufficiency | guiding | sufficiency | Competent Leadership Guidance | 0 | NO_ITEMS | Leadership guidance adequate through PM/QCM roles |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Mastery | 0 | NO_ITEMS | Directional coverage comprehensive |
| X:guiding:consistency | guiding | consistency | Harmonized Leadership Alignment | 0 | NO_ITEMS | Leadership alignment consistent across documents |
| X:applying:necessity | applying | necessity | Obligatory Practice Commitment | 1 | HAS_ITEMS | County notification lead time undefined |
| X:applying:sufficiency | applying | sufficiency | Proficient Implementation Basis | 0 | NO_ITEMS | Implementation basis adequate |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Record retention format undefined |
| X:applying:consistency | applying | consistency | Coherent Execution Standard | 1 | HAS_ITEMS | Inconsistent scope description between Specification and Datasheet |
| X:judging:necessity | judging | necessity | Binding Determination Basis | 0 | NO_ITEMS | Determination basis through requirements and RFP references |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Standard | 1 | HAS_ITEMS | Inspection request submission chain ambiguous |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all requirement areas |
| X:judging:consistency | judging | consistency | Reliable Benchmark Criterion | 0 | NO_ITEMS | Benchmark criteria consistent where defined |
| X:reviewing:necessity | reviewing | necessity | Fundamental Assurance Finding | 0 | NO_ITEMS | Assurance findings through verification tables |
| X:reviewing:sufficiency | reviewing | sufficiency | Proficient Assurance Review | 0 | NO_ITEMS | Assurance review process adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Record | 1 | HAS_ITEMS | Third-party testing lab qualification not addressed |
| X:reviewing:consistency | reviewing | consistency | Harmonized Assurance Standard | 0 | NO_ITEMS | Assurance standards consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | WeakStatement | Procedure | Procedure | Define the minimum County notification lead time for inspections; currently stated as "TBD (not specified in accessible sources)" in Procedure B1 and Guidance trade-offs | This is an obligatory practice (County attendance is mandatory per REQ-QC-03) but the notification lead time needed to achieve it is undefined, risking non-compliance through insufficient notice | Procedure.md; Guidance.md | Phase B > B1; Trade-offs table — County notification lead time | — | PROPOSAL: Define a specific lead time (e.g., 48 hours minimum) or require QC Plan to establish it based on County PM input | TBD |
| X-002 | X:applying:completeness | MissingSlot | Procedure | Procedure | Define QC record retention format and storage location; Procedure C4 and Records table both note format is "TBD" | An exhaustive implementation record requires knowing how and where records are stored; currently undefined, risking inaccessibility during guarantee period | Procedure.md | Phase C > C4; Records table | — | PROPOSAL: Procedure to specify minimum retention format requirements (at least digital backup) | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Datasheet | Align scope description terminology: Datasheet "Attributes" table describes "Program scope" while Specification "Scope > Included" uses a different enumeration; ensure consistent scope boundaries | The Datasheet scope attribute and the Specification Included scope list are expressed differently, which could cause confusion about what is in/out of scope | Datasheet.md; Specification.md | Attributes table — Program scope; Scope > Included | — | PROPOSAL: Datasheet scope attribute to reference Specification scope section or use identical language | TBD |
| X-004 | X:judging:sufficiency | Conflict | Multi | Guidance | Resolve inspection request submission chain: CONF-001 in Guidance identifies ambiguity between RFP §3.1 (coordinate through County PM) and §3.3.2 (Proponent submits inspection requests); this is already flagged but remains TBD | Justified adjudication requires a settled submission chain; Guidance CONF-001 correctly identifies this but human ruling has not been rendered, blocking definitive procedure | Guidance.md; Procedure.md | Conflict Table > CONF-001; Phase B > B2 Note | Guidance.md#CONF-001 (RFP §3.1 vs. §3.3.2) | PROPOSAL: Accept Guidance proposed authority (Proponent submits, County PM is notified) | TBD |
| X-005 | X:reviewing:completeness | VerificationGap | Procedure | Specification | Add qualification or accreditation requirements for third-party testing laboratories when testing is outsourced; Procedure B5 notes testing "may be performed by QC Manager or qualified third-party lab (TBD)" | Exhaustive assurance records require that testing sources are qualified; no requirement or verification exists for third-party lab accreditation | Procedure.md; Specification.md | Phase B > B5; entire Specification scanned | — | PROPOSAL: Specification to require third-party labs be accredited (e.g., ISO 17025 or equivalent) if used | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Reference Datum | 1 | HAS_ITEMS | CCDC 14-2013 text not accessible |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering information coherent across documents |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Mastery | 0 | NO_ITEMS | Governance knowledge adequately integrated |
| E:guiding:wisdom | guiding | wisdom | Visionary Governance Discernment | 0 | NO_ITEMS | Governance discernment reflected in principles and trade-offs |
| E:applying:data | applying | data | Evidenced Work Record | 0 | NO_ITEMS | Work record structures defined in Procedure Records table |
| E:applying:information | applying | information | Informed Practice Intelligence | 0 | NO_ITEMS | Practice intelligence adequately informed |
| E:applying:knowledge | applying | knowledge | Accomplished Craft Proficiency | 1 | HAS_ITEMS | No training/onboarding requirement for QC procedures |
| E:applying:wisdom | applying | wisdom | Principled Craft Judgment | 0 | NO_ITEMS | Craft judgment principles in Guidance P1-P6 |
| E:judging:data | judging | data | Proven Evidential Finding | 1 | HAS_ITEMS | Deficiency severity classification absent |
| E:judging:information | judging | information | Contextualized Assessment Report | 0 | NO_ITEMS | Assessment reporting contextualized through weekly reports |
| E:judging:knowledge | judging | knowledge | Masterful Evaluative Proficiency | 0 | NO_ITEMS | Evaluative framework adequate for document maturity level |
| E:judging:wisdom | judging | wisdom | Wise Principled Adjudication | 0 | NO_ITEMS | Principled adjudication reflected in conflict handling approach |
| E:reviewing:data | reviewing | data | Evidenced Audit Confirmation | 0 | NO_ITEMS | Audit confirmation through verification tables |
| E:reviewing:information | reviewing | information | Comprehensive Review Intelligence | 0 | NO_ITEMS | Review intelligence comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | Accomplished Verification Mastery | 1 | HAS_ITEMS | No internal QC program audit/self-assessment mechanism |
| E:reviewing:wisdom | reviewing | wisdom | Principled Verification Wisdom | 0 | NO_ITEMS | Verification wisdom reflected in Guidance considerations |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | TBD_Question | Datasheet | Datasheet | Obtain and reference the CCDC 14-2013 contract text to confirm QC-related contract clauses (e.g., inspection rights, deficiency obligations, guarantee provisions); currently referenced but text is "location TBD" | Authoritative reference datum requires accessible source text; the CCDC 14-2013 is listed as the governing contract form but its specific QC provisions have not been verified against the actual document | Datasheet.md; Specification.md | References table — CCDC 14-2013; Standards table | — | PROPOSAL: Obtain CCDC 14-2013 and verify/update QC-related provisions in Specification | TBD |
| E-002 | E:applying:knowledge | RationaleGap | Procedure | Guidance | Add guidance on QC program onboarding: how are new inspection personnel, subcontractors, or project team members trained on the QC procedures and expectations | Accomplished craft proficiency requires a mechanism for knowledge transfer; no onboarding or training step exists in Procedure, and Guidance does not address how QC knowledge is disseminated to the team | Procedure.md; Guidance.md | entire document scanned | — | PROPOSAL: Guidance to address QC training/orientation; Procedure to include an onboarding step | TBD |
| E-003 | E:judging:data | MissingSlot | Specification | Specification | Add deficiency severity classification scheme (e.g., critical/major/minor) with differentiated response timelines and escalation triggers | The Deficiency Log fields (Procedure A5) and REQ-QC-06 treat all deficiencies equally; a severity classification would enable prioritized response and proven evidential findings by category | Specification.md; Procedure.md | REQ-QC-06; Phase A > A5 | — | PROPOSAL: Specification to define severity categories; Procedure to differentiate response paths | TBD |
| E-004 | E:reviewing:knowledge | VerificationGap | Procedure | Procedure | Add a periodic QC program self-assessment or internal audit step to verify the QC program itself is being executed as designed | No mechanism exists to verify the QC program is being followed consistently; verification checks are per-step but there is no programmatic self-assessment to achieve accomplished verification mastery | Procedure.md | entire document scanned | — | PROPOSAL: Add a periodic (e.g., monthly) QC program self-audit step in Phase B | TBD |

---
