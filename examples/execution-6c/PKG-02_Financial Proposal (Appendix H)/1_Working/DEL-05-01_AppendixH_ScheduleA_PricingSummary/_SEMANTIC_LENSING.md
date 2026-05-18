# Semantic Lensing Register: DEL-05-01 AppendixH ScheduleA PricingSummary

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/_CONTEXT.md`
- _STATUS.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/_STATUS.md`
- _SEMANTIC.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/_SEMANTIC.md`
- Datasheet.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/Datasheet.md`
- Specification.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/Specification.md`
- Guidance.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/Guidance.md`
- Procedure.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/Procedure.md`
- _REFERENCES.md — `PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/_REFERENCES.md`

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- Total warranted items: 62
- By document:
  - Datasheet: 16
  - Specification: 18
  - Guidance: 13
  - Procedure: 10
  - Multi: 5
- By matrix:
  - A: 11  B: 12  C: 9  F: 9  D: 7  X: 9  E: 5
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "regulatory direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | TBD_Question | Specification | TBD: Are there Alberta municipal procurement regulations (beyond RFP terms) that impose additional pricing disclosure requirements on Schedule A? | The Specification references CCDC 14-2013 and Alberta Prompt Payment Act but does not address whether Alberta procurement statutes impose formatting or disclosure requirements beyond the RFP template. | Specification.md | Standards > Contractual Standards | - | Consult Alberta procurement law or Owner RFP Authority | TBD |
| A-002 | WeakStatement | Guidance | P-05 Tax Separation references "procurement and tax regulations" generically without identifying specific applicable statutes or codes | Guidance invokes regulatory rationale for tax separation but provides no specific regulation citation, making "regulatory direction" vague and unverifiable. | Guidance.md | Principles > P-05: Tax Separation | - | - | TBD |

---

### Lens: A:normative:applying
**LensValue:** "mandatory compliance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | MissingSlot | Procedure | Procedure lacks an explicit compliance-check step verifying that the completed Schedule A satisfies all mandatory compliance requirements (R-01 through R-07) as a unified gate before signature | Steps 4, 5, 6, and 9 address individual checks but there is no single mandatory-compliance gate that systematically maps every Specification requirement to a pass/fail check. Step 9 approximates this but does not reference all R-IDs. | Procedure.md | Steps > Step 9: Final Quality Check | - | - | TBD |

---

### Lens: A:normative:judging
**LensValue:** "conformance assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | VerificationGap | Specification | R-01.3 (dollar symbol consistency) has verification method "Visual inspection: currency symbols present" but no criteria for what constitutes a conformance failure (e.g., missing symbol on one line vs all lines) | Conformance assessment requires clear pass/fail criteria; current statement is vague on threshold. | Specification.md | Requirements > R-01: Form and Format Requirements | - | - | TBD |

---

### Lens: A:normative:reviewing
**LensValue:** "audit oversight"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | MissingSlot | Procedure | No procedure step addresses post-submission audit trail or record retention for demonstrating compliance if challenged by Owner during evaluation | Procedure covers pre-submission verification but lacks guidance on how to respond to evaluation committee inquiries or demonstrate compliance post-submission. Audit oversight perspective reveals this gap. | Procedure.md | Records > Supporting Records | - | - | TBD |

---

### Lens: A:operative:guiding
**LensValue:** "procedural instruction"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:operative:applying
**LensValue:** "practical execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-006 | TBD_Question | Procedure | TBD: What specific tools/software will be used to fill the Schedule A template (fillable PDF, Word recreation, Excel)? Step 1 lists alternatives but defers decision. | Practical execution requires a defined tool/method; current TBD in Tools and Systems section leaves the execution path ambiguous. | Procedure.md | Prerequisites > Tools and Systems | - | Estimator / Commercial Lead to decide | TBD |

---

### Lens: A:operative:judging
**LensValue:** "performance measurement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-007 | MissingSlot | Specification | No requirement addresses timing performance (e.g., Schedule A must be completed N days before submission deadline to allow QA review) | Performance measurement perspective reveals absence of timing or cycle-time requirements despite Procedure noting "24 hours before submission" as risk mitigation. This is guidance-level only and not a requirement. | Specification.md; Procedure.md | Specification: Requirements (absent); Procedure: Notes | - | - | TBD |

---

### Lens: A:operative:reviewing
**LensValue:** "process examination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-008 | MissingSlot | Procedure | No explicit independent reviewer role is required in the procedure steps; Step 9 mentions "second reviewer" only in Guidance Notes, not as a mandatory step | Process examination reveals that QA review is recommended in Guidance but not enforced in Procedure; Procedure Gate 5 references "Proposal Manager or QA Lead" but Step 9 does not mandate independent review. | Procedure.md; Guidance.md | Procedure: Steps > Step 9; Guidance: Notes | - | - | TBD |

---

### Lens: A:evaluative:guiding
**LensValue:** "value orientation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-009 | RationaleGap | Guidance | Guidance discusses competitive positioning (Trade-offs section) but does not provide a value framework for how to weigh the 35-point price score against technical score components | Value orientation lens reveals that the trade-off discussion is qualitative but lacks any structured decision framework for balancing price vs technical merit. | Guidance.md | Trade-offs > Competitive Positioning vs Risk Coverage | - | - | TBD |

---

### Lens: A:evaluative:applying
**LensValue:** "merit determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-010 | TBD_Question | Datasheet | TBD: What is the specific evaluation formula for the price score (35 points)? Datasheet states "Lowest compliant price receives highest score" (ASSUMPTION) but actual formula is not extracted from RFP. | Merit determination requires knowing how price translates to score; current ASSUMPTION may be incorrect if formula is proportional rather than binary. | Datasheet.md | Conditions > Evaluation Context | - | Consult RFP Section 8.3 page 26 for exact formula | TBD |

---

### Lens: A:evaluative:judging
**LensValue:** "worth adjudication"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:evaluative:reviewing
**LensValue:** "quality appraisal"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-011 | MissingSlot | Datasheet | Datasheet Notes section lists TBDs but does not include a quality appraisal summary indicating which attributes are confirmed vs which remain TBD/ASSUMPTION | Quality appraisal lens reveals that the Datasheet mixes confirmed facts and assumptions without a clear status indicator per attribute. | Datasheet.md | Notes | - | - | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | TBD_Question | Datasheet | TBD: Currency is stated as "Canadian dollars ($)" with ASSUMPTION tag. Is this explicitly stated in the RFP or must it be verified? | Essential fact lens: currency is a fundamental pricing attribute but is currently an assumption, not a verified fact. | Datasheet.md | Attributes > Pricing Structure | - | Verify against RFP text | TBD |
| B-002 | MissingSlot | Datasheet | Datasheet does not include the proposal validity period (irrevocability duration) as an attribute despite Conditions noting "irrevocable offer during validity period" | The validity period duration is an essential pricing fact that affects financial exposure but is not captured as an attribute. | Datasheet.md | Attributes > Pricing Structure; Conditions > Mandatory Pricing Requirements | - | - | TBD |

---

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | WeakStatement | Datasheet | Evaluation method field states "Lowest compliant price receives highest score" tagged as ASSUMPTION with partial source (RFP Section 8.6 page 28 tie-breaker only) | Adequate evidence lens: the evaluation method is a critical attribute but the evidence cited (tie-breaker provision) does not fully support the stated evaluation method. | Datasheet.md | Conditions > Evaluation Context | - | Extract actual evaluation formula from RFP Section 8.3 | TBD |

---

### Lens: B:data:completeness
**LensValue:** "full record"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | MissingSlot | Datasheet | Datasheet Scope Inclusions table does not list all Addendum 03 requirements individually (e.g., room sizing ranges from section 1.21 are mentioned only in Guidance but not in Datasheet) | Full record lens: Datasheet should be the comprehensive factual record of scope; some Addendum 03 requirements are documented only in Guidance considerations. | Datasheet.md; Guidance.md | Datasheet: Scope Inclusions; Guidance: Considerations | - | - | TBD |

---

### Lens: B:data:consistency
**LensValue:** "uniform measurement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | Normalization | Multi | Terminology inconsistency: Datasheet uses "Additional Option" and notes Schedule B uses "Additional Item"; Specification and Procedure both use both terms without normalizing to a single canonical term | Uniform measurement lens: inconsistent terminology for the same pricing elements across documents creates ambiguity risk. Datasheet Notes section acknowledges this but does not establish a canonical term. | Datasheet.md; Specification.md; Procedure.md | Datasheet: Notes; Specification: R-02.4, R-07; Procedure: Step 2, Step 3 | Datasheet.md#Notes vs Specification.md#R-02.4 | Adopt "Additional Option" for Schedule A context, "Additional Item" for Schedule B context, and note equivalence once | TBD |

---

### Lens: B:information:necessity
**LensValue:** "required disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-006 | TBD_Question | Specification | TBD: Does the RFP require disclosure of cost estimating methodology or assumptions within Schedule A itself, or only in Schedule B / pricing narrative? | Required disclosure lens: Specification R-01.1 mandates template use but does not clarify whether any additional disclosures (beyond template fields) are required within Schedule A. | Specification.md | Requirements > R-01 | - | Verify against RFP Appendix H template | TBD |

---

### Lens: B:information:sufficiency
**LensValue:** "satisfactory explanation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-007 | WeakStatement | Guidance | Guidance Example 1 (Addenda Acknowledgment) uses "Addendum 01 to Addendum 03" format but does not confirm whether this matches the exact template blank format ("Addendum ___ to ___") | Satisfactory explanation lens: the example may not exactly match what the template requires; if the template has two blanks, guidance should confirm the exact fill-in format. | Guidance.md | Examples > Example 1 | - | - | TBD |

---

### Lens: B:information:completeness
**LensValue:** "comprehensive account"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-008 | MissingSlot | Guidance | Guidance does not include a comprehensive account of all addenda impacts on pricing (only Addendum 03 is detailed; Addenda 01 and 02 are dismissed as "no pricing impact" without documenting what was reviewed to reach that conclusion) | Comprehensive account lens: for a complete addenda integration record, Guidance should briefly state what each addendum addressed and why it has no pricing impact. | Guidance.md | Principles > P-03; Considerations | - | - | TBD |

---

### Lens: B:information:consistency
**LensValue:** "coherent reporting"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-009 | Conflict | Multi | Datasheet states "Cold storage building" is "60' x 100' unheated structure for seasonal equipment" (sourced from RFP page 36) but no document confirms whether this dimension was modified by any addendum | Coherent reporting lens: if Addendum 03 modified building specifications, the cold storage dimensions should be confirmed as unchanged; currently only Datasheet states dimensions with no addenda cross-check. | Datasheet.md; Guidance.md | Datasheet: Scope Inclusions; Guidance: Considerations | Datasheet.md#Scope Inclusions vs Addendum 03 | Verify cold storage building dimensions are unchanged by addenda | TBD |

---

### Lens: B:knowledge:necessity
**LensValue:** "critical understanding"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-010 | RationaleGap | Guidance | Guidance does not explain the critical understanding of why Schedule A uses 7 lines specifically or how the line item structure relates to the Owner's evaluation methodology | Critical understanding lens: the deliverable team needs to understand why the pricing structure is what it is (beyond "template fidelity") to make informed decisions about gray areas like FF&E. | Guidance.md | Purpose; Principles > P-01 | - | - | TBD |

---

### Lens: B:knowledge:sufficiency
**LensValue:** "competent grasp"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:completeness
**LensValue:** "thorough expertise"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:consistency
**LensValue:** "reliable reasoning"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:necessity
**LensValue:** "essential judgment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-011 | TBD_Question | Guidance | TBD: What is the team's risk appetite for the competitive positioning trade-off? Guidance identifies the trade-off but defers entirely to commercial lead without providing decision criteria or thresholds. | Essential judgment lens: the trade-off section provides options but no framework for essential judgment calls (e.g., what margin of contingency is minimum acceptable). | Guidance.md | Trade-offs > Competitive Positioning vs Risk Coverage | - | Commercial Lead / Proposal Manager | TBD |

---

### Lens: B:wisdom:sufficiency
**LensValue:** "prudent capacity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:completeness
**LensValue:** "integral discernment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:consistency
**LensValue:** "principled conviction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-012 | Normalization | Guidance | Guidance addresses FF&E treatment in Trade-offs (Conflict-01) and in Considerations but does not consolidate a principled position statement on how to handle scope items that are "optional" but not one of the 6 named options | Principled conviction lens: the handling of non-template optional items (FF&E and potentially others) needs a consistent principle, not just case-by-case trade-off analysis. | Guidance.md | Trade-offs > Base Scope vs Additional Options; Conflict Table > Conflict-01 | - | - | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "obligatory compliance threshold"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | MissingSlot | Specification | No requirement establishes the minimum compliance threshold for Schedule A (e.g., is partial completion of pricing lines acceptable or must all 7 lines have dollar values?) | Obligatory compliance threshold lens: R-01.2 says lines "shall be completed with dollar values or marked if not priced" but does not define whether marking a line "not priced" is compliant or triggers disqualification. | Specification.md | Requirements > R-01.2 | - | Consult RFP evaluation criteria | TBD |

---

### Lens: C:normative:sufficiency
**LensValue:** "defensible compliance assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | VerificationGap | Procedure | Procedure Step 9 Final Quality Check table lacks a compliance assurance record (e.g., signed-off checklist with requirement IDs) that could serve as defensible evidence of compliance | Defensible compliance assurance lens: the procedure produces a checklist but does not require it to be documented as a formal record with traceability to each Specification requirement ID. | Procedure.md | Steps > Step 9: Final Quality Check; Records > Supporting Records | - | - | TBD |

---

### Lens: C:normative:completeness
**LensValue:** "holistic regulatory coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | TBD_Question | Specification | TBD: Does the Town of Penhold have any local bylaws or procurement policies that impose additional requirements on pricing submissions beyond those in the RFP? | Holistic regulatory coverage lens: Specification cites RFP, CCDC 14-2013, and Alberta Prompt Payment Act but does not confirm that no other regulatory instruments apply. | Specification.md | Standards > Contractual Standards | - | Consult RFP Authority or Town procurement policy | TBD |

---

### Lens: C:normative:consistency
**LensValue:** "stable compliance coherence"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:operative:necessity
**LensValue:** "essential operational prerequisite"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | WeakStatement | Procedure | Step 2 prerequisite "DEL-05-02 (Schedule B) substantially complete" uses vague qualifier "substantially" without defining what constitutes sufficient completion to proceed | Essential operational prerequisite lens: the gating condition for proceeding with Schedule A is unclear; "substantially complete" could mean 80% or 100% of values finalized. | Procedure.md | Prerequisites > Dependencies; Steps > Step 2 | - | - | TBD |

---

### Lens: C:operative:sufficiency
**LensValue:** "defensible operational capacity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-005 | MissingSlot | Procedure | No step addresses what to do if Schedule B values change after Schedule A has been populated (revision/update procedure) | Defensible operational capacity lens: the procedure covers linear completion but not iterative revision, which is common in proposal development. | Procedure.md | Steps | - | - | TBD |

---

### Lens: C:operative:completeness
**LensValue:** "comprehensive operational coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-006 | MissingSlot | Procedure | No step addresses coordination with DEL-05-03 (Pricing Narrative) to ensure pricing assumptions documented in the narrative are consistent with Schedule A values | Comprehensive operational coverage lens: Procedure covers Schedule B reconciliation but not Pricing Narrative coordination, despite Guidance and Specification identifying this interface. | Procedure.md | Steps; Specification.md: Interfaces | - | - | TBD |

---

### Lens: C:operative:consistency
**LensValue:** "consistent operational discipline"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:necessity
**LensValue:** "essential valuation baseline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-007 | TBD_Question | Datasheet | TBD: What is the Owner's affordability limit or budget expectation for this project? Datasheet notes "Not disclosed by Owner; negotiation permitted if over limit" but this is a critical valuation baseline for competitive pricing. | Essential valuation baseline lens: without knowing the Owner's budget range, the pricing team lacks a baseline against which to evaluate competitiveness. | Datasheet.md | Conditions > Evaluation Context | - | May not be obtainable; document as unknown constraint | TBD |

---

### Lens: C:evaluative:sufficiency
**LensValue:** "justified valuation competence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-008 | WeakStatement | Specification | R-02.3 requires bond costs "shall be included within the base contract price" but verification method states "Confirm inclusion in General Requirements or as separate line in Schedule B" -- this is verification of Schedule B, not Schedule A | Justified valuation competence lens: the verification method for this requirement does not directly verify Schedule A compliance; it verifies the input (Schedule B) rather than the output (Schedule A). | Specification.md | Requirements > R-02.3 | - | - | TBD |

---

### Lens: C:evaluative:completeness
**LensValue:** "comprehensive valuation coverage"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:consistency
**LensValue:** "consistent valuation discipline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-009 | Normalization | Multi | The concept of "lump sum fixed price" appears in Datasheet (Conditions > Contractual Conditions), Specification (Standards > Financial), Guidance (P-04), but with slightly different phrasing each time: "Fixed-price lump sum contract" vs "total proposed fixed fee" vs "lump-sum fixed-price Design-Build contract" | Consistent valuation discipline lens: the canonical pricing basis terminology should be normalized across documents. | Datasheet.md; Specification.md; Guidance.md | Datasheet: Standards; Specification: Financial Standards; Guidance: P-04 | Datasheet.md#Standards vs Specification.md#Financial Standards vs Guidance.md#P-04 | Adopt RFP's exact wording as canonical | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "foundational prescriptive assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | VerificationGap | Specification | R-04.3 states "Failure to acknowledge addenda may result in price proposal disqualification" with verification "Compliance check (pass/fail)" but no specific pass/fail criteria or recovery action if fail is detected pre-submission | Foundational prescriptive assurance lens: the most critical compliance requirement lacks a defined recovery path. | Specification.md | Requirements > R-04.3 | - | - | TBD |

---

### Lens: F:normative:sufficiency
**LensValue:** "validated prescriptive justification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | WeakStatement | Specification | R-05.2 "If Proponent is a corporation, Schedule A shall be executed under corporate seal" -- verification is "Verify seal presence for corporate proponents" but no guidance on what constitutes a valid seal or whether digital seals are acceptable | Validated prescriptive justification lens: the requirement is prescriptive but the justification/validation method is incomplete for modern execution methods. | Specification.md | Requirements > R-05.2 | - | Consult RFP Section 5.2 for seal requirements | TBD |

---

### Lens: F:normative:completeness
**LensValue:** "exhaustive prescriptive coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | MissingSlot | Specification | No requirement addresses what happens if the proponent identifies an error in the RFP Schedule A template itself (e.g., line item description mismatch) | Exhaustive prescriptive coverage lens: requirements cover form compliance but not error handling for template defects. | Specification.md | Requirements > R-01 | - | - | TBD |

---

### Lens: F:normative:consistency
**LensValue:** "dependable prescriptive alignment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:operative:necessity
**LensValue:** "irreducible operational foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | TBD_Question | Procedure | TBD: What is the minimum lead time required between Schedule B finalization and submission deadline to complete Steps 1-10? Procedure Notes estimate "minimum 0.5 day" but this is tagged TBD. | Irreducible operational foundation lens: the minimum time to execute the procedure is a foundational operational parameter that remains undefined. | Procedure.md | Notes | - | Estimator / Proposal Manager to confirm | TBD |

---

### Lens: F:operative:sufficiency
**LensValue:** "validated operational proficiency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-005 | MissingSlot | Procedure | No step validates that the person performing Schedule A completion has operational proficiency (e.g., familiarity with RFP requirements, access to all source documents, authority to enter pricing values) | Validated operational proficiency lens: procedure assumes competence but does not verify prerequisites for the person executing. | Procedure.md | Prerequisites | - | - | TBD |

---

### Lens: F:operative:completeness
**LensValue:** "integral operational completeness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-006 | MissingSlot | Procedure | Procedure does not include a step for verifying that the PDF file size constraint (under 15 MB total proposal) is met after Schedule A is assembled into the proposal PDF | Integral operational completeness lens: R-01.4 requires 15 MB limit but the procedure's Step 10 (PDF assembly) does not include a file size verification action. | Procedure.md | Steps > Step 10; Specification.md: R-01.4 | - | - | TBD |

---

### Lens: F:operative:consistency
**LensValue:** "dependable operational alignment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:necessity
**LensValue:** "irreducible evaluation foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-007 | TBD_Question | Datasheet | TBD: Is the 35-point price evaluation score calculated using a linear formula (e.g., lowest price / proponent price x 35) or a different method? The exact formula is needed to evaluate pricing strategy. | Irreducible evaluation foundation lens: the evaluation formula is the foundation of how pricing merit is determined and is currently an unverified assumption. | Datasheet.md | Conditions > Evaluation Context | - | Extract from RFP Section 8.3 page 26 | TBD |

---

### Lens: F:evaluative:sufficiency
**LensValue:** "validated evaluation justification"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:completeness
**LensValue:** "integral evaluation completeness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-008 | MissingSlot | Specification | Post-Submission Verification section is tagged as ASSUMPTION and is not formulated as requirements; these evaluation-phase checks should either be requirements or explicitly excluded from scope | Integral evaluation completeness lens: the Specification contains a "Post-Submission Verification" section that is not requirement-level and blurs the boundary between what the proponent controls and what the evaluator does. | Specification.md | Verification > Post-Submission Verification | - | - | TBD |

---

### Lens: F:evaluative:consistency
**LensValue:** "steadfast evaluation alignment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-009 | Conflict | Multi | Specification R-03.3 notes "Exception for Option 4" regarding monthly monitoring fee in Schedule B vs Schedule A, and Guidance Conflict-02 proposes excluding monitoring fee from Schedule A line 1-5. Procedure Step 2 notes "excluding monthly monitoring fee" but Step 3 says "clarify monitoring fee treatment" -- inconsistent resolution across documents. | Steadfast evaluation alignment lens: three documents address the monitoring fee treatment differently, with no single authoritative resolution. | Specification.md; Guidance.md; Procedure.md | Specification: R-03.3; Guidance: Conflict-02; Procedure: Steps 2, 3 | Specification.md#R-03.3 vs Guidance.md#Conflict-02 vs Procedure.md#Step 2-3 | Guidance Conflict-02 proposed resolution (installation only in Schedule A) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens: D:normative:guiding
**LensValue:** "authoritative compliance framework"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | Normalization | Specification | The compliance framework is distributed across R-01 (form), R-04 (addenda), R-05 (submission), and R-06 (scope exclusions) but there is no summary compliance matrix within the Specification that maps all mandatory compliance requirements to their authority source | Authoritative compliance framework lens: the Specification requirements are well-structured individually but lack an overarching compliance framework view. | Specification.md | Requirements sections R-01 through R-07 | - | - | TBD |

---

### Lens: D:normative:applying
**LensValue:** "binding enforcement legitimacy"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:normative:judging
**LensValue:** "definitive compliance determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | VerificationGap | Specification | R-06.2 "Base contract pricing shall reflect 12-acre functional site development" has verification method "Verify site scope assumptions in pricing narrative (DEL-05-03)" -- this verifies a different deliverable, not Schedule A itself | Definitive compliance determination lens: the verification method for this requirement is delegated to another deliverable (DEL-05-03), making definitive compliance determination for DEL-05-01 impossible within its own boundary. | Specification.md | Requirements > R-06.2 | - | - | TBD |

---

### Lens: D:normative:reviewing
**LensValue:** "systematic compliance verification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | MissingSlot | Procedure | Procedure Verification section (Quality Gates) lists 5 gates but does not include a systematic mapping showing which Specification requirements (R-01 through R-07) are covered by which gate | Systematic compliance verification lens: without explicit mapping of requirements to gates, it is unclear whether all requirements are systematically verified. | Procedure.md | Verification > Process Verification | - | - | TBD |

---

### Lens: D:operative:guiding
**LensValue:** "structured execution framework"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:operative:applying
**LensValue:** "confirmed workflow delivery"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-004 | WeakStatement | Procedure | Step 10 "Deliver to PDF Assembly Process" assumes proposal assembly lead is "likely Proposal Manager for DEL-01-02" but does not confirm the handoff point or deliverable format acceptance criteria | Confirmed workflow delivery lens: the final delivery step uses uncertain language ("likely") for a critical handoff that confirms workflow completion. | Procedure.md | Steps > Step 10 | - | - | TBD |

---

### Lens: D:operative:judging
**LensValue:** "calibrated execution scope assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-005 | TBD_Question | Guidance | TBD: Should the pricing team assess whether all 6 additional options are worth pricing, or is the assumption that all must be priced? RFP may not require all options to have non-zero values. | Calibrated execution scope assessment lens: the scope of execution (all 7 lines vs selective pricing) needs explicit calibration. | Guidance.md | Trade-offs > Base Scope vs Additional Options | - | Consult RFP requirements for optional items | TBD |

---

### Lens: D:operative:reviewing
**LensValue:** "systematic procedural audit"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:guiding
**LensValue:** "purposeful appraisal framework"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-006 | RationaleGap | Guidance | Guidance Purpose section explains why the deliverable exists but does not frame the purposeful appraisal criteria that the Owner's evaluation committee will use to judge pricing merit beyond the 35-point score | Purposeful appraisal framework lens: Guidance explains proponent purpose but not evaluator perspective, which would inform strategic pricing decisions. | Guidance.md | Purpose | - | - | TBD |

---

### Lens: D:evaluative:applying
**LensValue:** "realized appraisal legitimacy"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:judging
**LensValue:** "definitive merit determination"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:reviewing
**LensValue:** "systematic worth verification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-007 | MissingSlot | Datasheet | Datasheet does not include a summary of how the 35-point price evaluation contributes to overall proposal worth (100 points), nor how additional option pricing affects total evaluation | Systematic worth verification lens: Datasheet captures the 35-point weight as an attribute but does not show the full evaluation structure that would enable systematic worth verification. | Datasheet.md | Conditions > Evaluation Context | - | - | TBD |

---

## Matrix X -- Verification (4x4)

### Lens: X:guiding:necessity
**LensValue:** "foundational directive architecture"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | RationaleGap | Guidance | Guidance does not provide a foundational directive for verification philosophy (e.g., whether verification should be exhaustive, risk-based, or minimal compliance) | Foundational directive architecture lens: the verification approach needs a guiding rationale that informs how deeply each check should be performed. | Guidance.md | (absent -- no verification philosophy section) | - | - | TBD |

---

### Lens: X:guiding:sufficiency
**LensValue:** "validated guidance capacity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:guiding:completeness
**LensValue:** "exhaustive directional coverage"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:guiding:consistency
**LensValue:** "harmonized directional discipline"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:applying:necessity
**LensValue:** "mandated implementation foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | VerificationGap | Specification | R-02.1 verification method "Cross-check against OSR scope summary" does not specify how to verify that all OSR requirements are included in the base price when Schedule A only shows a single lump sum number | Mandated implementation foundation lens: the lump-sum nature of Schedule A means verification of scope coverage cannot be done from Schedule A alone; verification depends on Schedule B, creating a verification dependency gap. | Specification.md | Requirements > R-02.1 | - | - | TBD |

---

### Lens: X:applying:sufficiency
**LensValue:** "adequate implementation assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | WeakStatement | Procedure | Step 3 action item 2 states "ASSUMPTION: No decimal cents required; round to nearest dollar" -- this formatting assumption affects implementation adequacy and is not validated against the RFP template | Adequate implementation assurance lens: rounding convention is an implementation detail that could cause reconciliation mismatches if Schedule B uses different precision. | Procedure.md | Steps > Step 3 | - | Verify against RFP template format | TBD |

---

### Lens: X:applying:completeness
**LensValue:** "exhaustive implementation coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | MissingSlot | Specification | No requirement addresses the Schedule A signature block fields beyond signature and seal (e.g., date, witness, title, proponent legal name, address) -- these may be required by the template | Exhaustive implementation coverage lens: the Specification covers signature and seal but the RFP template likely has additional execution fields that need to be completed. | Specification.md | Requirements > R-05.1, R-05.2 | - | Verify against RFP Appendix H pages 57-58 | TBD |

---

### Lens: X:applying:consistency
**LensValue:** "harmonized implementation discipline"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:necessity
**LensValue:** "binding assessment foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-005 | Conflict | Multi | Specification Verification section and Procedure Verification section both define verification checklists but with different structures and different item counts; Specification has 8 pre-submission items and 4 post-submission items, while Procedure has 5 quality gates and 7 step-9 checklist items | Binding assessment foundation lens: two verification structures exist without clear primacy, which could lead to items being checked in one but not the other. | Specification.md; Procedure.md | Specification: Verification > Pre-Submission; Procedure: Verification > Process Verification + Step 9 | Specification.md#Pre-Submission Verification vs Procedure.md#Process Verification | Specification requirements are authoritative; Procedure should implement all Specification verification items | TBD |

---

### Lens: X:judging:sufficiency
**LensValue:** "justified assessment adequacy"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:completeness
**LensValue:** "exhaustive assessment scope"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-006 | MissingSlot | Specification | No verification item addresses R-07 (Optional Items Pricing Requirements) in the Pre-Submission Verification Checklist -- R-07.1 through R-07.4 have no corresponding verification entry | Exhaustive assessment scope lens: the verification checklist does not cover all requirement groups; R-07 optional items verification is absent. | Specification.md | Verification > Pre-Submission Verification Checklist | - | - | TBD |

---

### Lens: X:judging:consistency
**LensValue:** "stable assessment alignment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:reviewing:necessity
**LensValue:** "essential verification assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-007 | VerificationGap | Procedure | Gate 2 (Reconciliation) requires "Estimator + QA reviewer" but no preceding step ensures the QA reviewer has been assigned or is available | Essential verification assurance lens: verification assurance depends on reviewer availability, which is not procedurally assured. | Procedure.md | Verification > Process Verification > Gate 2 | - | - | TBD |

---

### Lens: X:reviewing:sufficiency
**LensValue:** "sufficient validation justification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-008 | WeakStatement | Specification | Post-Submission Verification section is labeled "ASSUMPTION" with statement "Evaluation Committee will verify" -- this section presents assumptions about Owner behavior as quasi-requirements without validation justification | Sufficient validation justification lens: the section exists to inform but is presented without sufficient justification that these are actual Owner verification steps vs the proponent's assumptions about them. | Specification.md | Verification > Post-Submission Verification | - | - | TBD |

---

### Lens: X:reviewing:completeness
**LensValue:** "exhaustive validation coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-009 | MissingSlot | Procedure | Procedure Output Verification (Deliverable Acceptance) lists 7 acceptance items but does not include validation of R-02.4 (additional options priced as incremental scope only) or R-07.1 through R-07.4 (option-specific requirements) | Exhaustive validation coverage lens: the output verification checklist is incomplete; several requirements lack corresponding acceptance check entries. | Procedure.md | Verification > Output Verification | - | - | TBD |

---

### Lens: X:reviewing:consistency
**LensValue:** "consistent validation discipline"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix E -- Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "authoritative governance mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | TBD_Question | Specification | TBD: Does CCDC 14-2013 impose any requirements on how pricing is presented in pre-contract documents (i.e., does the contract standard have anything to say about Schedule A format)? | Authoritative governance mandate lens: CCDC 14-2013 is cited as the governing contract form but its requirements on pre-contract pricing presentation are not examined. | Specification.md | Standards > Contractual Standards | - | Review CCDC 14-2013 pricing provisions | TBD |

---

### Lens: E:normative:sufficiency
**LensValue:** "substantiated regulatory sufficiency"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:normative:completeness
**LensValue:** "exhaustive regulatory completeness"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:normative:consistency
**LensValue:** "uniform regulatory coherence"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:necessity
**LensValue:** "foundational execution mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | TBD_Question | Procedure | TBD: Is there a mandate for who must review and approve Schedule A values before signature (e.g., does the proponent's corporate governance require board or officer approval for commitments above a certain threshold)? | Foundational execution mandate lens: the procedure identifies signature authority but does not address internal governance mandates for pricing approval. | Procedure.md | Steps > Step 8; Prerequisites | - | Proponent's internal governance policy | TBD |

---

### Lens: E:operative:sufficiency
**LensValue:** "substantiated operational sufficiency"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:completeness
**LensValue:** "exhaustive operational completeness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-003 | MissingSlot | Datasheet | Datasheet does not include the submission deadline date (August 30, 2024 @ 2:00 PM MST) as an attribute despite it being a critical operational parameter referenced in Specification R-05.3 | Exhaustive operational completeness lens: the submission deadline is a foundational operational fact that belongs in the Datasheet but is only captured in Specification. | Datasheet.md; Specification.md | Datasheet: Attributes (absent); Specification: R-05.3 | - | - | TBD |

---

### Lens: E:operative:consistency
**LensValue:** "harmonized operational coherence"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:necessity
**LensValue:** "foundational worth mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-004 | RationaleGap | Guidance | Guidance does not articulate a foundational statement on what constitutes "worth" in the context of this pricing deliverable beyond competitive scoring (e.g., does pricing quality also affect technical score perception, Owner confidence, negotiation leverage?) | Foundational worth mandate lens: the pricing deliverable's worth extends beyond the 35-point score but Guidance only addresses the scoring dimension. | Guidance.md | Purpose; Trade-offs | - | - | TBD |

---

### Lens: E:evaluative:sufficiency
**LensValue:** "substantiated worth sufficiency"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:completeness
**LensValue:** "exhaustive worth completeness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-005 | MissingSlot | Datasheet | Datasheet does not capture the full evaluation scoring structure (65 points technical + 35 points price = 100 total) with breakdown of technical score components, which would contextualize the pricing deliverable's evaluative completeness | Exhaustive worth completeness lens: Datasheet notes 35/100 for price but does not show what the other 65 points comprise, which is relevant context for understanding pricing's relative evaluative weight. | Datasheet.md | Conditions > Evaluation Context | - | - | TBD |

---

### Lens: E:evaluative:consistency
**LensValue:** "uniform worth coherence"

#### Warranted items
_No warranted items identified for this lens._

---

*End of Semantic Lensing Register*
