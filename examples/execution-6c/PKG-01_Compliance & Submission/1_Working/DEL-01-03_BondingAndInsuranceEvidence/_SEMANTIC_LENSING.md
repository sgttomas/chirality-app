# Semantic Lensing Register: DEL-01-03 Bonding and Insurance Evidence

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — DEL-01-03_BondingAndInsuranceEvidence/_CONTEXT.md (deliverable identity, acceptance criteria, scope traceability)
- _STATUS.md — DEL-01-03_BondingAndInsuranceEvidence/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-01-03_BondingAndInsuranceEvidence/_SEMANTIC.md (matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-01-03_BondingAndInsuranceEvidence/Datasheet.md (identification, attributes, conditions, construction, references)
- Specification.md — DEL-01-03_BondingAndInsuranceEvidence/Specification.md (scope, REQ-01 through REQ-07, standards, verification)
- Guidance.md — DEL-01-03_BondingAndInsuranceEvidence/Guidance.md (purpose, principles, considerations, trade-offs, examples)
- Procedure.md — DEL-01-03_BondingAndInsuranceEvidence/Procedure.md (prerequisites, steps 1-6, verification checkpoints, records)
- _REFERENCES.md — DEL-01-03_BondingAndInsuranceEvidence/_REFERENCES.md (RFP source reference)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- Total warranted items: 48
- By document:
  - Datasheet: 8
  - Specification: 18
  - Guidance: 7
  - Procedure: 11
  - Multi: 4
- By matrix:
  - A: 8  B: 9  C: 7  F: 6  D: 5  X: 8  E: 5
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "regulatory direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | TBD_Question | Datasheet | TBD: What are the specific regulatory directions from RFP §5.3.1 governing bonding and insurance at proposal stage? | The regulatory direction lens reveals that the foundational regulatory source (RFP §5.3.1) has not been extracted. All four documents reference it but none contain its actual content. This is the root TBD driving most downstream gaps. | Datasheet.md | Attributes > Agreement to Bond > Format | — | RFP §5.3.1 (PDF extraction needed) | TBD |
| A-002 | MissingSlot | Specification | Specification lacks a governing regulatory requirement statement that anchors REQ-01 through REQ-07 to a specific regulatory regime (e.g., Alberta Public Procurement Act or Municipal Government Act provisions on bonding). | The "regulatory direction" lens expects an explicit regulatory anchor beyond the RFP itself; no statute or regulation is cited as the upstream authority for the RFP's bonding requirement. | Specification.md | Standards > Governing Codes and Standards | — | Proposal Manager to identify governing statute | TBD |

---

### Lens: A:normative:applying
**LensValue:** "mandatory compliance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | WeakStatement | Specification | REQ-06 is conditional ("If required by RFP §5.3.1") but the condition cannot be resolved because RFP §5.3.1 is TBD. This leaves the mandatory/optional status of insurance evidence unresolved. | Under "mandatory compliance" lens, every requirement should have a clear mandatory/optional determination. REQ-06 is suspended in ambiguity. | Specification.md | Requirements > REQ-06 | — | RFP §5.3.1 extraction | TBD |

---

### Lens: A:normative:judging
**LensValue:** "conformance determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | VerificationGap | Specification | Verification method for REQ-02 (Surety Licensing) states "Surety company verification (Alberta regulatory database)" but does not specify which regulatory database or authority. The acceptance criteria reference "Financial Services Regulatory Authority of Alberta" — but this body may not exist under that name. | Conformance determination requires a concrete authority against which to judge. The named authority needs verification. | Specification.md | Verification > Verification Methods (REQ-02) | — | Proposal Manager to confirm correct Alberta regulatory body name | TBD |

---

### Lens: A:normative:reviewing
**LensValue:** "obligation verification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | MissingSlot | Procedure | No procedure step explicitly verifies that all bonding/insurance obligations from the RFP have been identified and checked off. Step 1 says "extract" from RFP but there is no verification that extraction is complete (no obligation register or checklist against the RFP). | Obligation verification lens expects a systematic check that all obligations have been captured — not just extraction but confirmation of completeness. | Procedure.md | Steps > Step 1: Verify RFP Requirements | — | Proposal Manager | TBD |

---

### Lens: A:operative:guiding
**LensValue:** "procedural steering"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:operative:applying
**LensValue:** "execution practice"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:operative:judging
**LensValue:** "performance assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-006 | MissingSlot | Procedure | Procedure verification checkpoints define acceptance criteria but do not define performance metrics (e.g., how many days before deadline should Agreement to Bond be obtained; what constitutes "timely" coordination with surety). | Performance assessment lens looks for measurable performance indicators. The procedure has binary pass/fail but no performance benchmarks. | Procedure.md | Verification > Process Verification Checkpoints | — | Proposal Manager | TBD |

---

### Lens: A:operative:reviewing
**LensValue:** "process audit"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:evaluative:guiding
**LensValue:** "value orientation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: A:evaluative:applying
**LensValue:** "merit demonstration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-007 | RationaleGap | Guidance | Guidance explains why bonding matters (risk mitigation, credibility) but does not explain how the quality or strength of the Agreement to Bond letter itself can demonstrate merit to evaluators (e.g., naming a well-known surety, including capacity figures, providing validity period beyond minimum). | Merit demonstration lens looks for guidance on how to exceed minimum compliance and convey strength. Guidance addresses compliance but not competitive differentiation through bonding evidence quality. | Guidance.md | Purpose; Considerations > For the Proposal Manager | — | Proposal Manager | TBD |

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
| A-008 | MissingSlot | Procedure | Step 6 Final QC checklist is comprehensive for compliance but lacks a quality appraisal dimension — e.g., does the Agreement to Bond letter read professionally? Is the bond cost inclusion statement clearly written? Is the insurance summary appropriately scoped? | Quality appraisal lens looks beyond compliance to presentation quality. The QC checklist is pass/fail on content but silent on communication quality. | Procedure.md | Steps > Step 6: Final QC and Acceptance | — | Proposal Manager | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | TBD_Question | Datasheet | TBD: What are the specific bond amounts or percentages required? What insurance types and minimum coverage amounts are required? What certificate requirements apply? | Essential facts lens reveals that the most critical data points (bond amounts, insurance types, coverage minimums) are all TBD in the Datasheet. These are the essential facts the deliverable must contain. | Datasheet.md | Attributes > Agreement to Bond > Bond Amounts; Attributes > Insurance Approach Summary | — | RFP §5.3.1 extraction | TBD |
| B-002 | MissingSlot | Datasheet | Datasheet does not include a "Validity Period" attribute for the Agreement to Bond, even though Guidance (Example 1) and Procedure (Step 2) both reference a validity period of 60-90 days. | An essential fact for a proposal-stage bonding commitment is how long it remains valid. This is referenced in other documents but absent from the Datasheet attribute table. | Datasheet.md | Attributes > Agreement to Bond | — | Datasheet enrichment | TBD |

---

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | WeakStatement | Datasheet | Bond Types Required is listed as "Performance bond, labor and material payment bond" but marked ASSUMPTION. Adequacy of evidence cannot be confirmed because the source (RFP §5.3.1) is TBD. | Adequate evidence lens asks whether the stated facts are grounded in sufficient source material. The bond types are assumption-based, not evidence-based. | Datasheet.md | Attributes > Agreement to Bond > Bond Types Required | — | RFP §5.3.1 | TBD |

---

### Lens: B:data:completeness
**LensValue:** "exhaustive record"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | MissingSlot | Datasheet | Datasheet does not list project-specific identification attributes needed for the Agreement to Bond letter: RFP number, project name, Owner name, anticipated contract value range. These appear in Guidance Example 1 and Procedure Step 2 but not in the Datasheet. | Exhaustive record lens expects the Datasheet to capture all factual attributes. Project identification data needed for the surety letter is absent from the attribute tables. | Datasheet.md | Attributes > Agreement to Bond | — | Datasheet enrichment | TBD |

---

### Lens: B:data:consistency
**LensValue:** "uniform datum"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | Normalization | Multi | Bond cost percentage range is stated as "1-3% of contract value" in Guidance (Principle 2) and Procedure (Step 3), but Datasheet says "Percentage of contract value" without a range, and Specification says nothing about percentage. The range should be normalized as a single canonical reference. | Uniform datum lens detects the same concept stated at different levels of specificity across documents. A canonical reference point is needed to prevent drift. | Guidance.md; Procedure.md; Datasheet.md | Guidance > Principle 2; Procedure > Step 3; Datasheet > Bond Cost Inclusion > Cost Basis | — | Datasheet as canonical source | TBD |

---

### Lens: B:information:necessity
**LensValue:** "required disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-006 | TBD_Question | Specification | TBD: Does the RFP require disclosure of the surety company's bonding capacity or financial rating? REQ-05 requires "surety capacity" confirmation but does not specify whether financial rating (e.g., A.M. Best rating) must be disclosed. | Required disclosure lens asks what information must be revealed to the Owner. Surety financial strength disclosure requirements are unaddressed. | Specification.md | Requirements > REQ-05 | — | RFP §5.3.1 | TBD |

---

### Lens: B:information:sufficiency
**LensValue:** "satisfactory reporting"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:information:completeness
**LensValue:** "comprehensive account"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-007 | MissingSlot | Guidance | Guidance does not provide a comprehensive account of what happens if the Agreement to Bond is deficient or rejected by the Owner — e.g., can it be cured during a clarification period, or is it an automatic disqualification? | Comprehensive account lens expects the guidance to address failure scenarios, not just success paths. The high-risk compliance flag makes this gap significant. | Guidance.md | Purpose; Considerations | — | RFP review or Proposal Manager judgment | TBD |

---

### Lens: B:information:consistency
**LensValue:** "coherent communication"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:necessity
**LensValue:** "foundational understanding"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-008 | RationaleGap | Guidance | Guidance explains bonding purpose (risk mitigation, credibility) but does not provide foundational understanding of how Alberta surety regulations work — e.g., what makes a surety "licensed," what regulatory body oversees sureties, what happens if a surety defaults. | Foundational understanding lens expects the Guidance to equip the user with enough background knowledge to navigate the domain. The current Guidance assumes surety knowledge. | Guidance.md | Principles > Principle 3 | — | Guidance enrichment | TBD |

---

### Lens: B:knowledge:sufficiency
**LensValue:** "competent expertise"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:completeness
**LensValue:** "thorough mastery"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:consistency
**LensValue:** "reliable doctrine"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:necessity
**LensValue:** "principled imperative"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:sufficiency
**LensValue:** "prudent adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-009 | RationaleGap | Guidance | Guidance Trade-off 2 (Insurance Detail vs. Simplicity) advises prudent restraint but does not articulate the prudential threshold — at what point does providing more insurance detail cross from "prudent" to "overcommitting"? No criteria for this judgment are given. | Prudent adequacy lens looks for calibrated judgment guidance. The trade-off is identified but the decision criteria are vague ("if RFP specifies... meet precisely; if vague... brief summary"). | Guidance.md | Trade-offs > Trade-off 2 | — | Proposal Manager judgment | TBD |

---

### Lens: B:wisdom:completeness
**LensValue:** "integral judgment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:consistency
**LensValue:** "steadfast discernment"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "compulsory conformance threshold"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | TBD_Question | Specification | TBD: What is the compulsory conformance threshold for the Agreement to Bond? Is there a minimum bond value, minimum surety rating, or minimum validity period that constitutes the threshold for compliance vs. non-compliance? | The conformance threshold is undefined because RFP §5.3.1 has not been extracted. Without a threshold, pass/fail determination cannot be made. | Specification.md | Requirements > REQ-01; Verification > Acceptance Gate | — | RFP §5.3.1 | TBD |

---

### Lens: C:normative:sufficiency
**LensValue:** "defensible compliance substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | WeakStatement | Specification | REQ-01 acceptance criteria is "Agreement to Bond document present in submission package" — this tests presence but not substantive compliance. A deficient or non-conforming letter could pass this test. | Defensible compliance substantiation requires acceptance criteria that verify content quality, not just document presence. | Specification.md | Requirements > REQ-01 > Acceptance Criteria | — | Specification enrichment | TBD |

---

### Lens: C:normative:completeness
**LensValue:** "comprehensive mandatory coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | MissingSlot | Specification | No requirement addresses the Agreement to Bond validity period, even though Guidance Example 1 and Procedure Step 2 both specify "60-90 days post-submission." If this is mandatory, it should be a requirement. | Comprehensive mandatory coverage lens reveals a gap: validity period is operationally referenced but not specified as a requirement. | Specification.md | Requirements | Guidance.md#Examples > Example 1; Procedure.md#Steps > Step 2 | Specification enrichment | TBD |

---

### Lens: C:normative:consistency
**LensValue:** "invariant compliance alignment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | Normalization | Multi | The term "licensed to operate in Alberta" is used in Datasheet (Conditions), Specification (REQ-02), Guidance (Principle 3), and Procedure (Step 2). However, the specific licensing authority is named differently: Specification says "Financial Services Regulatory Authority of Alberta" while other documents say "Alberta regulatory authority" generically. These should be aligned to a single canonical name. | Invariant compliance alignment requires consistent terminology for the same concept across all documents. | Specification.md; Datasheet.md; Guidance.md; Procedure.md | Specification > REQ-02; Datasheet > Conditions; Guidance > Principle 3; Procedure > Step 2 | — | Confirmed regulatory body name | TBD |

---

### Lens: C:operative:necessity
**LensValue:** "obligatory operational readiness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-005 | MissingSlot | Procedure | Procedure Prerequisites lists upstream dependencies but does not include a readiness checklist — e.g., confirming surety relationship is active, confirming estimator has preliminary contract value range, confirming RFP §5.3.1 has been read. | Obligatory operational readiness lens expects explicit pre-start conditions, not just dependency awareness. The prerequisites are descriptive rather than actionable checkpoints. | Procedure.md | Prerequisites > Dependencies | — | Procedure enrichment | TBD |

---

### Lens: C:operative:sufficiency
**LensValue:** "demonstrable execution capacity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:operative:completeness
**LensValue:** "end-to-end process coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-006 | MissingSlot | Procedure | Procedure covers production of the deliverable (Steps 1-6) but does not address what happens after acceptance — specifically, how the deliverable is handed off to DEL-01-02 assembly, how bond cost figures are communicated to the estimator for DEL-05-02, or how changes are propagated if bond costs change late. | End-to-end process coverage lens reveals that the procedure ends at "mark complete" but does not cover the downstream handoff and change management loop. | Procedure.md | Steps > Step 5; Traceability and Handoffs | — | Procedure enrichment | TBD |

---

### Lens: C:operative:consistency
**LensValue:** "stable procedural coherence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-007 | Normalization | Procedure | Step 4 says "If not required, skip this step and proceed to Step 5" but should say "proceed to Step 5" (since the next step is Step 5 regardless). Minor procedural clarity issue: the conditional skip language is slightly ambiguous about which step follows. | Stable procedural coherence lens catches small inconsistencies in procedural flow language. | Procedure.md | Steps > Step 4 | — | Procedure enrichment | TBD |

---

### Lens: C:evaluative:necessity
**LensValue:** "foundational credibility imperative"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:sufficiency
**LensValue:** "substantiated credibility measure"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:completeness
**LensValue:** "exhaustive credibility accounting"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:consistency
**LensValue:** "coherent credibility standard"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "non-negotiable conformance baseline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | WeakStatement | Specification | REQ-02 (Surety Licensing) is marked ASSUMPTION with source "standard for Alberta public sector projects; requires confirmation from RFP §5.3.1." If this is non-negotiable, it needs authoritative sourcing; if it is an assumption, the requirement should be flagged as provisional. | Non-negotiable conformance baseline lens requires that baseline requirements are grounded in authority, not assumption. REQ-02 straddles the line. | Specification.md | Requirements > REQ-02 | — | RFP §5.3.1 or Alberta legislation | TBD |

---

### Lens: F:normative:sufficiency
**LensValue:** "threshold-satisfying regulatory evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | VerificationGap | Specification | REQ-04 (Bond Cost Documentation) requires identification of "basis for bond cost estimation" but acceptance criteria ("Statement includes bond percentage or fixed cost; source basis") do not specify a minimum evidentiary threshold — e.g., must a surety quote be attached, or is a proponent self-statement sufficient? | Threshold-satisfying regulatory evidence lens asks whether the evidence standard is rigorous enough to satisfy a regulatory reviewer. The acceptance criteria may be too permissive. | Specification.md | Requirements > REQ-04 > Acceptance Criteria | — | Proposal Manager / RFP review | TBD |

---

### Lens: F:normative:completeness
**LensValue:** "total obligation fulfillment scope"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | TBD_Question | Specification | TBD: Does RFP §5.3.1 impose obligations beyond bonding and insurance — e.g., parent company guarantee, letter of credit, or other financial security instruments? The current scope assumes only bonding and insurance, but total obligation fulfillment requires confirming no obligations are missed. | Total obligation fulfillment scope lens asks whether the requirement set is exhaustive relative to the RFP's actual demands. | Specification.md | Scope > Inclusions | — | RFP §5.3.1 | TBD |

---

### Lens: F:normative:consistency
**LensValue:** "cross-document regulatory coherence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | Conflict | Multi | Datasheet states Agreement to Bond format is "Letter from surety company or broker confirming capacity" (TBD from RFP §5.3.1). Specification REQ-01 says "Agreement to Bond from a licensed surety." Guidance Example 1 says "Surety may provide letter directly or may authorize surety broker to issue letter on their behalf." There is potential ambiguity about whether a broker-issued letter satisfies REQ-01 which specifies "from a licensed surety." | Cross-document regulatory coherence lens detects a potential inconsistency in who may issue the letter. If the RFP requires a direct surety letter, a broker letter may not comply. | Datasheet.md; Specification.md; Guidance.md | Datasheet > Attributes > Format; Specification > REQ-01; Guidance > Example 1 | Datasheet#Attributes > Format vs. Specification#REQ-01 vs. Guidance#Example 1 | RFP §5.3.1 to determine acceptability of broker-issued letters | TBD |

---

### Lens: F:operative:necessity
**LensValue:** "prerequisite capability demonstration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-005 | MissingSlot | Datasheet | Datasheet does not include an attribute for "Surety Prequalification Status" or "Surety Relationship Status" — i.e., whether the proponent has an existing surety relationship or needs to establish one. This affects timeline and capability demonstration. | Prerequisite capability demonstration lens reveals that the proponent's surety readiness status is not captured as a factual attribute, though Procedure Step 2 branches on it. | Datasheet.md | Attributes > Agreement to Bond | — | Datasheet enrichment | TBD |

---

### Lens: F:operative:sufficiency
**LensValue:** "credible operational preparedness"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:operative:completeness
**LensValue:** "exhaustive capability assurance"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:operative:consistency
**LensValue:** "enduring procedural reliability"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:necessity
**LensValue:** "imperative credibility substantiation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:sufficiency
**LensValue:** "defensible worth attestation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-006 | RationaleGap | Guidance | Guidance Trade-off 1 discusses surety cost competitiveness but does not provide guidance on what constitutes a "defensible" bond cost estimate — e.g., should the proponent be able to justify the rate if challenged by the Owner, and what evidence supports defensibility (surety quote, market benchmark, historical rate)? | Defensible worth attestation lens looks for guidance on how to substantiate the bond cost figure's credibility. Trade-off 1 addresses the cost decision but not its defensibility. | Guidance.md | Trade-offs > Trade-off 1 | — | Guidance enrichment | TBD |

---

### Lens: F:evaluative:completeness
**LensValue:** "integral credibility fulfillment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:consistency
**LensValue:** "persistent quality alignment"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix D — Objectives (3x4)

### Lens: D:normative:guiding
**LensValue:** "settled regulatory mandate"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:normative:applying
**LensValue:** "enforced evidentiary adherence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | VerificationGap | Specification | REQ-05 (Bond Types Coverage) verification method is "Agreement to Bond content review" — but this is a subjective review without specified pass/fail criteria for what counts as adequate coverage of bond types. | Enforced evidentiary adherence lens expects verification methods to enforce standards, not just review. REQ-05 verification lacks enforcement criteria. | Specification.md | Verification > Verification Methods (REQ-05) | — | Specification enrichment | TBD |

---

### Lens: D:normative:judging
**LensValue:** "definitive compliance boundary"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | WeakStatement | Specification | The Acceptance Gate states "All requirements verified; no discrepancies with Appendix H pricing" but does not define what constitutes a "discrepancy" — e.g., is a rounding difference a discrepancy? Is a different line-item allocation (but same total) a discrepancy? | Definitive compliance boundary lens requires a clear boundary between pass and fail. The acceptance gate language is insufficiently precise. | Specification.md | Verification > Acceptance Gate | — | Proposal Manager to define tolerance | TBD |

---

### Lens: D:normative:reviewing
**LensValue:** "reconfirmed alignment assurance"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:operative:guiding
**LensValue:** "structured readiness pathway"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:operative:applying
**LensValue:** "established performance method"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:operative:judging
**LensValue:** "conclusive capacity determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | TBD_Question | Datasheet | TBD: What is the anticipated contract value range for bonding capacity purposes? The Agreement to Bond must confirm "sufficient" capacity, but no contract value estimate or range is stated in any document. | Conclusive capacity determination requires knowing the capacity target. Without a contract value range, the surety cannot confirm adequate capacity and the deliverable cannot be assessed for sufficiency. | Datasheet.md | Attributes > Agreement to Bond > Bond Amounts | — | Estimator / Commercial Lead | TBD |

---

### Lens: D:operative:reviewing
**LensValue:** "confirmed procedural integrity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:guiding
**LensValue:** "principled quality mandate"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:applying
**LensValue:** "active credibility justification"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:judging
**LensValue:** "conclusive quality settlement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-004 | MissingSlot | Guidance | Guidance does not include criteria for what constitutes a "high-quality" vs. "minimally acceptable" Agreement to Bond letter. No quality settlement framework exists for the key artifact. | Conclusive quality settlement lens looks for quality benchmarks. Guidance provides examples but no quality grading or settlement criteria. | Guidance.md | Examples > Example 1 | — | Guidance enrichment | TBD |

---

### Lens: D:evaluative:reviewing
**LensValue:** "confirmed enduring merit"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-005 | MissingSlot | Procedure | No procedure step addresses post-submission monitoring — e.g., if the surety withdraws capacity or the bond cost changes after submission but before award, there is no process for managing this risk. | Confirmed enduring merit lens asks whether the deliverable's value persists through the proposal evaluation period. There is no process for maintaining validity after submission. | Procedure.md | Steps; Records | — | Proposal Manager | TBD |

---

## Matrix X — Verification (4x4)

### Lens: X:guiding:necessity
**LensValue:** "foundational readiness directive"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | MissingSlot | Procedure | Procedure does not include a foundational readiness check that confirms the team understands the bonding and insurance domain sufficiently before starting. For teams unfamiliar with surety processes, Step 2 may be difficult to execute without foundational knowledge. | Foundational readiness directive lens expects verification that prerequisite knowledge is in place before execution begins. No knowledge-readiness check exists. | Procedure.md | Prerequisites | — | Procedure enrichment (link to Guidance foundational content) | TBD |

---

### Lens: X:guiding:sufficiency
**LensValue:** "validated preparedness guidance"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:guiding:completeness
**LensValue:** "full-scope compliance framework"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | MissingSlot | Specification | Specification does not include a compliance framework overview that maps each RFP obligation to a specific requirement and verification method in a single view. The verification table exists but is disconnected from the RFP obligation source (which is TBD). | Full-scope compliance framework lens expects a traceable framework from source obligation to requirement to verification. The current structure has requirements and verification but the source obligation linkage is incomplete. | Specification.md | Standards; Verification | — | Specification enrichment (after RFP extraction) | TBD |

---

### Lens: X:guiding:consistency
**LensValue:** "harmonized compliance orientation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:applying:necessity
**LensValue:** "prerequisite evidence discipline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | VerificationGap | Specification | REQ-03 (Bond Cost Inclusion) verification method includes "pricing document cross-check" but does not specify what constitutes adequate cross-check evidence — e.g., must both documents be reviewed side-by-side, must figures be within a tolerance, must the cross-check be documented? | Prerequisite evidence discipline lens asks whether the verification process produces verifiable evidence of its own execution. The cross-check has no evidence standard. | Specification.md | Verification > Verification Methods (REQ-03) | — | Specification enrichment | TBD |

---

### Lens: X:applying:sufficiency
**LensValue:** "credible conformance attestation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:applying:completeness
**LensValue:** "comprehensive conformance execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | VerificationGap | Procedure | Procedure Step 6 QC Checklist item "No missing information or TBD items remain (or flagged for resolution)" is self-referential — the procedure itself contains multiple TBDs. There is no mechanism to verify that TBDs flagged for resolution have actually been resolved before submission. | Comprehensive conformance execution lens reveals that the verification mechanism for TBD resolution is incomplete. TBDs can be "flagged" indefinitely without a forcing function. | Procedure.md | Steps > Step 6: Final QC and Acceptance | — | Proposal Manager | TBD |

---

### Lens: X:applying:consistency
**LensValue:** "dependable assurance protocol"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:necessity
**LensValue:** "binding capability verdict"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-005 | WeakStatement | Specification | Acceptance Gate authority is "Proposal Manager" but no escalation path is defined for cases where the Proposal Manager cannot resolve a deficiency (e.g., surety refuses to issue letter, bond costs cannot be reconciled). | Binding capability verdict lens expects a definitive authority structure including escalation. The single-authority model may be insufficient for complex failure scenarios. | Specification.md | Verification > Acceptance Gate | — | Proposal Manager / organizational escalation path | TBD |

---

### Lens: X:judging:sufficiency
**LensValue:** "evidenced conformance adjudication"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:completeness
**LensValue:** "total conformance adjudication"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-006 | MissingSlot | Specification | No requirement addresses addenda integration verification — the Guidance notes (Considerations > For the Team, item 3) that addenda acknowledgment failure may disqualify the price proposal. But there is no REQ checking that addenda affecting bonding/insurance have been integrated. | Total conformance adjudication lens reveals that addenda integration — a disqualification risk noted in Guidance — has no corresponding verification requirement. | Specification.md | Requirements | Guidance.md#Considerations > For the Team | Specification enrichment | TBD |

---

### Lens: X:judging:consistency
**LensValue:** "invariant capability standard"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:reviewing:necessity
**LensValue:** "fundamental compliance revalidation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-007 | MissingSlot | Procedure | No procedure step addresses revalidation of the deliverable if upstream conditions change — e.g., if the contract value estimate changes significantly, the Agreement to Bond capacity confirmation may need to be updated and bond costs recalculated. | Fundamental compliance revalidation lens expects a process for re-checking compliance when inputs change. The procedure is single-pass with no revalidation loop. | Procedure.md | Steps | — | Procedure enrichment | TBD |

---

### Lens: X:reviewing:sufficiency
**LensValue:** "sufficient integrity reconfirmation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:reviewing:completeness
**LensValue:** "full-scope integrity audit"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-008 | MissingSlot | Specification | No requirement mandates a full-scope integrity audit of the deliverable before submission — i.e., a holistic review that checks not just individual requirements but the coherence of the entire deliverable package (Agreement to Bond + Bond Cost Statement + Insurance Summary) as an integrated whole. | Full-scope integrity audit lens expects a requirement for holistic review beyond component-level verification. The verification table is requirement-by-requirement but no integrative check exists. | Specification.md | Verification | — | Specification enrichment | TBD |

---

### Lens: X:reviewing:consistency
**LensValue:** "sustained coherence monitoring"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix E — Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "absolute evidentiary mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | WeakStatement | Datasheet | Datasheet Conditions > Limiting Conditions states "Failure to include Agreement to Bond may result in proposal disqualification" — the word "may" weakens what should be an absolute statement given the high-risk compliance flag. If this is truly a mandatory gate, the Datasheet should state "will result in disqualification." | Absolute evidentiary mandate lens expects definitive language for mandatory items. The hedging language ("may") undermines the seriousness of the compliance risk. | Datasheet.md | Conditions > Limiting Conditions | — | RFP §5.3.1 to confirm mandatory vs. discretionary disqualification | TBD |

---

### Lens: E:normative:sufficiency
**LensValue:** "justified compliance substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | VerificationGap | Specification | REQ-06 (Insurance Approach Summary) verification method is "RFP requirement verification; document inspection" but the RFP requirement itself is TBD. The verification method cannot be executed until the RFP requirement is known. This creates a suspended verification — present in form but non-functional. | Justified compliance substantiation lens reveals that the insurance verification method is procedurally complete but substantively empty due to the RFP TBD. | Specification.md | Verification > Verification Methods (REQ-06) | — | RFP §5.3.1 extraction to enable verification | TBD |

---

### Lens: E:normative:completeness
**LensValue:** "fully adjudicated obligation architecture"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:normative:consistency
**LensValue:** "permanent cross-document conformance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-003 | Normalization | Multi | The "as required" qualifier for the Insurance Approach Summary appears in _CONTEXT.md, Datasheet, Specification (REQ-06), Guidance, and Procedure (Step 4). The conditional trigger is consistently stated but the condition itself (whether the RFP requires it) is unresolved in all documents. This should be normalized once the RFP is read: either remove the conditional and make it mandatory, or confirm it is optional and adjust all documents. | Permanent cross-document conformance lens identifies a cascading TBD that affects all four documents identically. Resolution will require synchronized updates. | _CONTEXT.md; Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple sections | — | RFP §5.3.1 resolution | TBD |

---

### Lens: E:operative:necessity
**LensValue:** "decisive readiness infrastructure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-004 | MissingSlot | Procedure | Procedure does not establish a decision point or timeline for when the deliverable must be started relative to the proposal deadline. Guidance mentions "1-2 weeks" for surety processing but the Procedure does not translate this into a start-no-later-than milestone. | Decisive readiness infrastructure lens expects the procedure to define temporal readiness constraints. The timeline is advisory in Guidance but not procedurally enforced. | Procedure.md | Prerequisites; Notes | Guidance.md#Considerations > For the Proposal Manager | Procedure enrichment | TBD |

---

### Lens: E:operative:sufficiency
**LensValue:** "substantiated capability demonstration"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:completeness
**LensValue:** "comprehensive capability closure"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:consistency
**LensValue:** "stable operational coherence"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:necessity
**LensValue:** "non-negotiable credibility foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-005 | RationaleGap | Guidance | Guidance Purpose section explains why bonding matters to the Owner but does not explicitly connect the deliverable's credibility to the proponent's overall proposal scoring. If bonding evidence is evaluated (not just pass/fail), the guidance should address how to maximize credibility impact. | Non-negotiable credibility foundation lens asks whether the guidance establishes credibility as a scored dimension or merely a compliance gate. The distinction affects how much effort to invest in quality vs. minimum compliance. | Guidance.md | Purpose | — | RFP evaluation criteria review | TBD |

---

### Lens: E:evaluative:sufficiency
**LensValue:** "justified trust substantiation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:completeness
**LensValue:** "exhaustive merit governance"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:consistency
**LensValue:** "perpetual credibility governance"

#### Warranted items
_No warranted items identified for this lens._
