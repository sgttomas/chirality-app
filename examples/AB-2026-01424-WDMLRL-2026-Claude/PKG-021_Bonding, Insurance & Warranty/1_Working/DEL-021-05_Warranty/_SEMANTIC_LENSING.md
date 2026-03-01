# Semantic Lensing Register: DEL-021-05 Guarantee Period Obligations

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-021_Bonding, Insurance & Warranty/1_Working/DEL-021-05_Warranty
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-021-05_Warranty/_CONTEXT.md (Deliverable Overview, Scope Definition, Linked Items, Success Criteria)
- _STATUS.md — DEL-021-05_Warranty/_STATUS.md (Status: SEMANTIC_READY, Phase: Initialization, Progress: 0%)
- _SEMANTIC.md — DEL-021-05_Warranty/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully)
- Datasheet.md — DEL-021-05_Warranty/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-021-05_Warranty/Specification.md (Scope, Requirements REQ-021-05-01 through REQ-021-05-06, Standards, Verification, Documentation)
- Guidance.md — DEL-021-05_Warranty/Guidance.md (Purpose, Principles P-1 through P-5, Considerations C-1 through C-7, Trade-offs T-1/T-2, Conflict Table OI-001 through OI-005)
- Procedure.md — DEL-021-05_Warranty/Procedure.md (Prerequisites, Steps Phase 1-3, Verification, Records)
- _REFERENCES.md — DEL-021-05_Warranty/_REFERENCES.md (Primary References, Related Documentation)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document (AppliesToDoc):
  - Datasheet: 3
  - Specification: 8
  - Guidance: 2
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 2  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Warranty period end-trigger prescriptive direction is weak |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Defect classification not mandated but assumed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for deficiency holdback reconciliation completeness |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit lens: documents address audit via Procedure verification table |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Inspection schedule procedural direction is assumption-only |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution well-covered in Procedure Steps Phase 1-3 |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment addressed via Procedure Step 2.4 monitoring |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit addressed through Procedure verification table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation articulated in Guidance Purpose and Principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered by Guidance trade-offs T-1 and T-2 |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination covered through holdback mechanism |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by inspection and approval process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Specification | Clarify whether warranty period end is triggered by calendar expiry alone, final inspection, or Owner written release | The warranty period end trigger is marked TBD in Datasheet Conditions and flagged as OI-005 in Guidance, but no normative prescriptive direction exists in Specification to resolve it; this affects enforceability of the final holdback release | Datasheet.md, Guidance.md | Datasheet.md#Conditions > Period End; Guidance.md#Conflict Table > OI-005 | | Specification REQ-021-05-01 or new REQ | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add normative requirement establishing defect classification criteria (safety-critical / functional / cosmetic) or explicitly state that RFP treats all defects uniformly under 10-day rule | Defect classification is referenced as ASSUMPTION in Datasheet, Procedure Step 2.1, and Guidance C-6 / OI-001, but no normative requirement establishes or rejects a classification framework; mandatory practice is absent | Specification.md, Datasheet.md | Specification.md#Requirements (absent); Datasheet.md#Defect Classification | | Specification (new REQ or note under REQ-021-05-02) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for Deficiency Holdback Ledger reconciliation -- specify what constitutes a fully reconciled ledger (e.g., zero unresolved items, Owner sign-off on each release) | REQ-021-05-04 requires holdback records but Verification table row for REQ-021-05-04 says "Reconcile Deficiency Holdback ledger" without defining pass/fail criteria for compliance determination | Specification.md | Specification.md#Verification > REQ-021-05-04 | | Specification Verification table | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen inspection schedule from ASSUMPTION to confirmed prerequisite or explicitly gate it on Owner agreement at CCC | Procedure Step 1.5 and the entire inspection cadence in Phase 2 depend on an assumption-level schedule; procedural direction for inspections lacks normative backing, creating execution ambiguity | Procedure.md | Procedure.md#Steps > Phase 1 > Step 1.5 | | Procedure Step 1.5 (after human ruling on OI-002) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Contractor contact info is essential fact but sourcing is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes provide adequate evidence with RFP source citations |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Record retention period is incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement values (10-day, 2-year) consistent across all docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (CCC date, deficiency notifications) well-defined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each process step is adequate in Procedure |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Comprehensive account provided across four documents |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of guarantee mechanism well-articulated in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicit in PM role assignment |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Thorough mastery supported by detailed Procedure steps |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across Guidance principles and Procedure steps |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Emergency vs. standard deficiency judgment criteria not explicit |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance provided in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided by Guidance Purpose section |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning articulated in Guidance Principles P-1 through P-5 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Procedure | Procedure | TBD: Identify source and timing for obtaining Contractor warranty-period contact information (key personnel, emergency contacts) -- is this a contract execution deliverable (DEL-021-04) or a CCC-phase deliverable? | Procedure Step 1.2 requires Contractor contact info but Prerequisites list it as "TBD -- to be obtained from Contractor at or before CCC"; no upstream deliverable is assigned to produce this essential fact | Procedure.md | Procedure.md#Prerequisites > Required Reference Materials; Procedure.md#Steps > Step 1.2 | | Procedure Prerequisites or _DEPENDENCIES.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Specification | Specification | Add record retention period requirement or explicitly delegate to project-level retention policy | Record retention period is "TBD (post-project)" in every row of the Procedure Records table and flagged as OI-004 in Guidance; comprehensive record-keeping requires a defined retention period | Specification.md, Procedure.md | Specification.md#Documentation > Record Retention; Procedure.md#Records (all rows) | | Specification REQ-021-05-05 (add retention period clause) | TBD |
| B-003 | B:wisdom:necessity | MissingSlot | Guidance | Guidance | Add guidance on distinguishing emergency from standard deficiency conditions -- criteria or examples for when "serious damage, injury, or loss of life" threshold is met | Essential discernment for classifying a deficiency as emergency is needed; RFP 2.10.5 states the threshold but Guidance C-4 only addresses notification, not the judgment criteria for triggering emergency authorization | Guidance.md | Guidance.md#Considerations > C-4 | | Guidance (new consideration or expand C-4) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Compliance Clarity | 1 | HAS_ITEMS | CCDC 14-2013 compliance requirements not accessible |
| C:normative:sufficiency | normative | sufficiency | Mandated Competence Validation | 0 | NO_ITEMS | Competence validation addressed through PM role and verification table |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Alberta OH&S applicability during warranty remediation is unconfirmed |
| C:normative:consistency | normative | consistency | Invariant Regulatory Discipline | 0 | NO_ITEMS | Regulatory discipline consistently applied via RFP references |
| C:operative:necessity | operative | necessity | Critical Operational Acumen | 0 | NO_ITEMS | Operational acumen requirements met through detailed procedure steps |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Process Capability | 0 | NO_ITEMS | Process capability demonstrated through phased procedure design |
| C:operative:completeness | operative | completeness | Total Operational Traceability | 0 | NO_ITEMS | Traceability supported by deficiency log, holdback ledger, register |
| C:operative:consistency | operative | consistency | Methodical Procedural Coherence | 0 | NO_ITEMS | Procedure steps are methodical and internally coherent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Merit recognition addressed through Guidance Purpose and P-5 |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Appraisal | 0 | NO_ITEMS | Quality appraisal justified through inspection and approval process |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Value accounting addressed via holdback ledger and trade-offs |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Alignment | 0 | NO_ITEMS | Worth alignment consistent with Guidance Principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | TBD: Obtain and review executed CCDC 14-2013 contract warranty clauses to confirm whether they impose additional or different obligations beyond RFP 2.10-2.11 | Authoritative compliance clarity requires knowledge of all governing normative sources; CCDC 14-2013 is listed as a standard but its text is unavailable, and REQ-021-05-06 Note acknowledges this gap; compliance determination cannot be complete without it | Specification.md | Specification.md#Standards > CCDC 14-2013 row; Specification.md#Requirements > REQ-021-05-06 Note | | DEL-021-04 (Contract Execution) as source | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Clarify applicability of Alberta OH&S legislation to warranty-period remediation work and add as a confirmed or excluded standard | Exhaustive regulatory coverage requires addressing all applicable legislation; Alberta OH&S is listed as "ASSUMPTION: likely applicable; location TBD" in Standards table, which is insufficient for compliance planning | Specification.md | Specification.md#Standards > Alberta OH&S legislation row | | Specification Standards table | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Compliance Imperative | 0 | NO_ITEMS | Binding compliance requirements well-established from RFP |
| F:normative:sufficiency | normative | sufficiency | Mandated Proof Threshold | 1 | HAS_ITEMS | Proof threshold for remediation acceptance not defined |
| F:normative:completeness | normative | completeness | Absolute Compliance Documentation | 1 | HAS_ITEMS | Documentation format requirements absent |
| F:normative:consistency | normative | consistency | Invariant Governance Standard | 0 | NO_ITEMS | Governance standards consistently referenced |
| F:operative:necessity | operative | necessity | Essential Execution Readiness | 0 | NO_ITEMS | Execution readiness addressed through Prerequisites section |
| F:operative:sufficiency | operative | sufficiency | Sufficient Process Evidence | 0 | NO_ITEMS | Process evidence requirements articulated in Procedure verification |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Coverage | 0 | NO_ITEMS | Workflow coverage comprehensive in Procedure Phase 1-3 |
| F:operative:consistency | operative | consistency | Disciplined Process Uniformity | 0 | NO_ITEMS | Process uniformity maintained through consistent step structure |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 1 | HAS_ITEMS | No quality standard for what constitutes acceptable remediation |
| F:evaluative:sufficiency | evaluative | sufficiency | Proven Valuation Competence | 0 | NO_ITEMS | Valuation competence addressed through holdback mechanism |
| F:evaluative:completeness | evaluative | completeness | Total Quality Documentation | 0 | NO_ITEMS | Quality documentation requirements in Specification Documentation section |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality coherence maintained across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for what constitutes Owner approval of remediation -- e.g., visual inspection, functional test, or documented sign-off | Mandated proof threshold: REQ-021-05-02 requires rectification and Owner approval per RFP 2.10.3, but neither the Specification verification table nor the Procedure defines what evidence constitutes sufficient proof that a remediation is "approved by the Owner" | Specification.md, Procedure.md | Specification.md#Verification > REQ-021-05-02; Procedure.md#Steps > Step 2.4 | | Specification Verification table and/or Procedure Step 2.4 | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement or guidance for documentation format standards (e.g., template references, minimum content requirements) for warranty artifacts | Absolute compliance documentation: REQ-021-05-05 lists required artifacts but notes "exact format TBD"; no format standard exists for any of the seven anticipated artifacts, which could lead to inconsistent or incomplete records | Specification.md | Specification.md#Requirements > REQ-021-05-05 Detail | | Specification REQ-021-05-05 or Procedure appendix | TBD |
| F-003 | F:evaluative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria defining what constitutes acceptable remediation quality -- reference to original contract documents, manufacturer specs, or equivalent standard | Fundamental quality imperative: RFP 2.10.3 states defects "shall be rectified and approved by the Owner in accordance with the Contract Documents" but neither Specification nor Procedure defines the quality standard against which remediation is measured | Specification.md | Specification.md#Requirements > REQ-021-05-01 Detail; Specification.md#Verification > REQ-021-05-01 | | Specification (expand REQ-021-05-01 verification criteria) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Regulatory Direction | 0 | NO_ITEMS | Regulatory direction resolved through RFP citation chain |
| D:normative:applying | normative | applying | Enforced Proof Implementation | 1 | HAS_ITEMS | Holdback valuation methodology not enforced |
| D:normative:judging | normative | judging | Binding Conformance Verdict | 0 | NO_ITEMS | Conformance verdict mechanism established through verification table |
| D:normative:reviewing | normative | reviewing | Confirmed Oversight Benchmark | 0 | NO_ITEMS | Oversight benchmark established through audit provisions |
| D:operative:guiding | operative | guiding | Confirmed Operational Course | 0 | NO_ITEMS | Operational course confirmed through three-phase procedure |
| D:operative:applying | operative | applying | Verified Actionable Execution | 0 | NO_ITEMS | Actionable execution verified through step-by-step procedure |
| D:operative:judging | operative | judging | Resolved Performance Scope | 0 | NO_ITEMS | Performance scope resolved through verification checks per step |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Stability | 0 | NO_ITEMS | Procedural stability confirmed through consistent structure |
| D:evaluative:guiding | evaluative | guiding | Confirmed Merit Priority | 1 | HAS_ITEMS | Consequential damages documentation guidance incomplete |
| D:evaluative:applying | evaluative | applying | Confirmed Quality Practice | 0 | NO_ITEMS | Quality practice confirmed through inspection and approval cycle |
| D:evaluative:judging | evaluative | judging | Resolved Merit Verdict | 0 | NO_ITEMS | Merit verdict resolved through holdback release mechanism |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Worth Equilibrium | 0 | NO_ITEMS | Worth equilibrium confirmed through P-5 holdback transparency principle |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Datasheet | Specification | Add requirement or method for estimating the value of outstanding deficiencies for holdback retention purposes (RFP 2.11.1 says "amount equal to the estimated value") | Enforced proof implementation: the holdback retention is quantitative but no methodology is specified for how the Owner estimates deficiency value; Datasheet lists "estimated value" attribute but Specification and Procedure do not operationalize valuation | Datasheet.md, Specification.md | Datasheet.md#Conditions > Performance Conditions; Specification.md#Requirements > REQ-021-05-04 | | Specification REQ-021-05-04 or Procedure Step 1.4 | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add guidance on documenting consequential damages (expenses, losses beyond direct remediation cost) per RFP 2.10.8 and P-4 | Confirmed merit priority: Guidance P-4 states "The Project Manager should document any consequential damages in addition to direct remediation costs" but no further guidance exists on how to identify, quantify, or record consequential damages; this is a value-priority gap | Guidance.md | Guidance.md#Principles > P-4 | | Guidance (expand P-4 or add new Consideration) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Readiness Verity | 0 | NO_ITEMS | Readiness foundations established through prerequisites |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Governance Path | 0 | NO_ITEMS | Governance path substantiated through RFP citation chain |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Account | 0 | NO_ITEMS | Governance account comprehensive across four documents |
| X:guiding:consistency | guiding | consistency | Unified Governance Perspective | 0 | NO_ITEMS | Governance perspective unified across documents |
| X:applying:necessity | applying | necessity | Confirmed Execution Evidence | 1 | HAS_ITEMS | Execution evidence for Owner-performed work not addressed |
| X:applying:sufficiency | applying | sufficiency | Grounded Execution Competence | 0 | NO_ITEMS | Execution competence grounded in PM role and procedure |
| X:applying:completeness | applying | completeness | Total Execution Documentation | 0 | NO_ITEMS | Execution documentation requirements in Specification and Procedure |
| X:applying:consistency | applying | consistency | Reliable Execution Standard | 0 | NO_ITEMS | Execution standard reliable and consistent across procedure steps |
| X:judging:necessity | judging | necessity | Binding Assessment Reality | 0 | NO_ITEMS | Assessment reality bound through verification table |
| X:judging:sufficiency | judging | sufficiency | Grounded Verdict Capability | 0 | NO_ITEMS | Verdict capability grounded in defined criteria |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 0 | NO_ITEMS | Adjudication record requirements in Procedure and Specification |
| X:judging:consistency | judging | consistency | Harmonized Assessment Standard | 0 | NO_ITEMS | Assessment standards harmonized across documents |
| X:reviewing:necessity | reviewing | necessity | Critical Audit Steadiness | 1 | HAS_ITEMS | Mid-period audit/review point not established |
| X:reviewing:sufficiency | reviewing | sufficiency | Grounded Audit Assurance | 0 | NO_ITEMS | Audit assurance grounded in verification checks |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Documentation | 0 | NO_ITEMS | Audit documentation requirements comprehensive |
| X:reviewing:consistency | reviewing | consistency | Reliable Assurance Perspective | 0 | NO_ITEMS | Assurance perspective reliable across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add procedure step or sub-step for documenting and verifying Owner-performed emergency or default remediation work (costs, scope, contractor notification) | Confirmed execution evidence: Procedure Step 2.3 addresses emergency work and Step 2.4 addresses Contractor failure, but neither establishes a verification checkpoint for work performed by the Owner itself (as opposed to the Contractor), including cost documentation for recovery | Procedure.md | Procedure.md#Steps > Step 2.3; Procedure.md#Steps > Step 2.4 | | Procedure Step 2.3 or 2.4 (add verification sub-step) | TBD |
| X-002 | X:reviewing:necessity | RationaleGap | Multi | Guidance | Add rationale for whether a formal mid-period status review (e.g., at 12 months) should be conducted to assess overall warranty administration health, separate from physical inspections | Critical audit steadiness: the documents provide for physical inspections at scheduled intervals but do not address an administrative/management review of the warranty administration process itself during the 2-year period; a review checkpoint would support audit steadiness | Guidance.md, Procedure.md | Guidance.md#Considerations (absent); Procedure.md#Steps (absent) | | Guidance (new Consideration) and/or Procedure (new step in Phase 2) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Basis | 0 | NO_ITEMS | Directive basis well-established through RFP and Decomposition references |
| E:guiding:information | guiding | information | Unified Directive Communication | 0 | NO_ITEMS | Directive communication unified across documents |
| E:guiding:knowledge | guiding | knowledge | Integrated Leadership Mastery | 0 | NO_ITEMS | Leadership mastery requirements implicit in PM role |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Judgment | 0 | NO_ITEMS | Leadership judgment supported by Guidance Principles |
| E:applying:data | applying | data | Verified Implementation Record | 0 | NO_ITEMS | Implementation record requirements established in Specification Documentation |
| E:applying:information | applying | information | Actionable Practice Clarity | 0 | NO_ITEMS | Practice clarity provided by detailed Procedure steps |
| E:applying:knowledge | applying | knowledge | Applied Implementation Expertise | 0 | NO_ITEMS | Implementation expertise supported by Procedure detail |
| E:applying:wisdom | applying | wisdom | Principled Practice Discernment | 0 | NO_ITEMS | Practice discernment supported by Guidance trade-offs |
| E:judging:data | judging | data | Proven Adjudication Record | 1 | HAS_ITEMS | Cross-reference between notification dates and deadline dates not explicit |
| E:judging:information | judging | information | Coherent Verdict Communication | 0 | NO_ITEMS | Verdict communication addressed through notification process |
| E:judging:knowledge | judging | knowledge | Calibrated Ruling Expertise | 0 | NO_ITEMS | Ruling expertise calibrated through verification checks |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Insight | 0 | NO_ITEMS | Adjudication insight supported by Guidance principles and trade-offs |
| E:reviewing:data | reviewing | data | Verified Audit Evidence | 1 | HAS_ITEMS | Terminology normalization needed for "guarantee period" vs "warranty period" |
| E:reviewing:information | reviewing | information | Transparent Audit Narrative | 0 | NO_ITEMS | Audit narrative transparent through structured documentation |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Audit Mastery | 0 | NO_ITEMS | Audit mastery supported by comprehensive procedure and verification |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Discernment | 0 | NO_ITEMS | Audit discernment supported by Guidance principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:judging:data | Normalization | Datasheet | Multi | Standardize Deficiency Holdback Ledger field names between Datasheet Construction table and Procedure Step 1.4 -- Procedure lists "Date Owner written instruction issued" and "Target rectification date" fields that do not appear in Datasheet | Proven adjudication record: the Deficiency Holdback Ledger is described in Datasheet Construction as an anticipated artifact and operationalized in Procedure Step 1.4 with specific field names, but the field list is more detailed in Procedure than in Datasheet; a normalization pass would ensure traceability between descriptive and operational views | Datasheet.md, Procedure.md | Datasheet.md#Construction > Deliverable Artifacts; Procedure.md#Steps > Step 1.4 | | Datasheet (align artifact description with Procedure fields) | TBD |
| E-002 | E:reviewing:data | Normalization | Multi | Guidance | Add terminology note clarifying that "guarantee period" (RFP term) and "warranty period" (common usage in documents) are synonymous and establishing which term is preferred | Verified audit evidence: the documents use "guarantee period" (from RFP) and "warranty period" interchangeably -- e.g., Datasheet uses both "Guarantee Period Duration" and "Post-CCC Warranty Period" as separate attributes; Guidance P-1 uses both within the same paragraph; this inconsistency could cause confusion in audit or external review | Datasheet.md, Guidance.md, Specification.md, Procedure.md | Datasheet.md#Attributes (rows 1-2); Guidance.md#Principles > P-1 | | Guidance (vocabulary note) and all documents (consistent usage) | TBD |
