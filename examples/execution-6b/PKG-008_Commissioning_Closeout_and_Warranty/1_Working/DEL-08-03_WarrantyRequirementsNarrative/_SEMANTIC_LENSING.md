# Semantic Lensing Register: DEL-08-03 Warranty Requirements Narrative

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-03_WarrantyRequirementsNarrative
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-08-03, PKG-008, Commissioning / Narrative, SOW-0032, OBJ-002
- _STATUS.md — SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md — 8 matrices parsed (A, B canonical; C, F, D, K, X, E derived); 7 used as lenses per protocol (A, B, C, F, D, X, E)
- Datasheet.md — present; read in full
- Specification.md — present; read in full
- Guidance.md — present; read in full
- Procedure.md — present; read in full
- _REFERENCES.md — present; read in full

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 12
- By document:
  - Datasheet: 3
  - Specification: 5
  - Guidance: 3
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 3  B: 2  C: 2  F: 2  D: 1  X: 1  E: 1
- By type:
  - Conflict: 0
  - VerificationGap: 3
  - MissingSlot: 3
  - WeakStatement: 2
  - RationaleGap: 1
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0 (CON-01 and CON-02 already captured in Guidance.md Conflict Table; no new conflicts found)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Warranty coordinator triage tiers in Procedure Step 3.9 go beyond RFP; not flagged as voluntary enhancement in Specification |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | CCDC 14-2013 base GC 12.5 text not accessible; implications for completeness |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Verification table in Specification covers all 10 requirements adequately |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No acceptance criteria for verifying SC source-language accuracy in final narrative artifact |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step guidance |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Step 3 drafting actions are well-specified |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Master Verification Checklist in Procedure covers performance criteria |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | V-1 through V-8 verification points provide systematic audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-003 and P-004 address value orientation well |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance examples EX-001 through EX-004 demonstrate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Scoring context in Guidance Notes and Procedure Step 6 is adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Step 7 quality check is thorough |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | VerificationGap | Specification | Specification | Add verification criterion for R-08 / T-002 interaction: if the narrative commits to tiered response times (immediate / 10 working days / 20 working days per Procedure Step 3.9 and Guidance T-002), Specification should note this as a voluntary enhancement beyond the GC 12.5.10 minimum floor | Procedure Step 3.9 and Guidance T-002 propose a tiered emergency response commitment (immediate for safety-critical, 10 working days for priority, 20 working days for routine). Specification R-08 only verifies the 20-working-day floor. If the narrative adopts the tiered commitment, there is no verification criterion to confirm that the voluntary enhancement is accurately stated and does not inadvertently create binding obligations beyond SC55 | Specification.md; Procedure.md; Guidance.md | Specification.md#R-08; Procedure.md#Step 3 section 9; Guidance.md#T-002 | -- | Specification.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Multi | TBD | Record TBD: obtain or summarize CCDC 14-2013 GC 12.5 base warranty provisions to confirm SC54-SC55 modifications are complete and no additional base GC 12.5 obligations are being inadvertently omitted | All four documents reference CCDC 14-2013 GC 12.5 as the base warranty article modified by SC54-SC55, but the full text is noted as "not directly accessible" (Datasheet.md Construction table, Specification.md Standards table, Procedure.md Prerequisites). Without confirming the base text, there is a risk that SC54-SC55 modifications may not account for all existing GC 12.5 provisions | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Construction; Specification.md#Standards; Procedure.md#Required References | -- | RFP / Contract source | TBD |
| A-003 | A:normative:reviewing | VerificationGap | Specification | Specification | Add a verification criterion to Specification Review Checklist: confirm that the final narrative artifact uses SC54-SC55 source-language phrases verbatim where required by P-001 (e.g., "wear and tear of normal use" not "normal wear and tear"; "deemed to take effect from the time that the defect has been corrected" not "restarts") | Guidance P-001 establishes a principle of accuracy to SC source language with specific phrase requirements. Procedure Step 7 checks terminology consistency. However, Specification.md Verification Table does not include an explicit verification method for source-language fidelity as a discrete check. The Review Checklist partially covers this (e.g., R-02, R-07, R-08 items mention specific phrases) but there is no single verification criterion that systematically validates P-001 compliance across the entire narrative | Specification.md; Guidance.md | Specification.md#Review Checklist; Guidance.md#P-001 | -- | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing factual parameter for word count range |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source evidence is well-cited across all documents |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Warranty coordinator contact details not specified as a Datasheet attribute |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Numeric values (12 months, 20 working days, 2 pts) are consistent across all four docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (warranty start trigger, defect definition, cost allocation) are all present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each SC provision is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Coverage of SC54-SC55 is thorough |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are consistent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding of warranty framework is well-demonstrated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Guidance examples demonstrate competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Thorough treatment across all provisions |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | CON-01 and CON-02 demonstrate appropriate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs T-001 through T-003 show adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic treatment of warranty landscape is present |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Specification | Specification | Clarify R-10 word count range: Specification R-10 does not specify a word count; Datasheet Documentation section says "300-600 words" (ASSUMPTION); Procedure Step 2 says "400-600 words" (ASSUMPTION). Reconcile or remove the inconsistent ASSUMPTION ranges, or explicitly label as non-binding guidance in Specification | Datasheet.md states "Estimated length: 300-600 words (ASSUMPTION)" while Procedure.md Step 2 states "approximately 400-600 words (ASSUMPTION)." These are labeled as assumptions but are inconsistent (300 vs 400 lower bound). If R-10 is silent on length, the inconsistent assumptions across Datasheet and Procedure may create confusion | Datasheet.md; Procedure.md; Specification.md | Datasheet.md#Documentation; Procedure.md#Step 2; Specification.md#R-10 | -- | Specification.md (or human decision to remove word count assumptions) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add attribute for "Warranty coordinator" role designation and contact availability requirement (24/7 per Guidance C-003 and Procedure Step 3.9) to Datasheet Attributes table | Guidance C-003 and Procedure Step 3.9 commit to a "designated warranty coordinator with 24/7 contact availability." This operational parameter is not recorded in the Datasheet Attributes table, which tracks all key factual parameters. This is a factual identifier that belongs in the Datasheet | Datasheet.md; Guidance.md; Procedure.md | Datasheet.md#Attributes; Guidance.md#C-003; Procedure.md#Step 3 section 9 | -- | Datasheet.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | binding regulatory obligation | 0 | NO_ITEMS | SC54-SC55 binding obligations are comprehensively captured |
| C:normative:sufficiency | normative | sufficiency | certified compliance adequacy | 1 | HAS_ITEMS | Acceptance criteria gap for P-001 compliance |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 1 | HAS_ITEMS | GC 12.5.4.4 remedy obligation sub-clause treatment |
| C:normative:consistency | normative | consistency | harmonized compliance integrity | 0 | NO_ITEMS | Compliance references are harmonized across documents |
| C:operative:necessity | operative | necessity | operational capability baseline | 0 | NO_ITEMS | Operational prerequisites are well-specified in Procedure |
| C:operative:sufficiency | operative | sufficiency | demonstrated process readiness | 0 | NO_ITEMS | Procedure prerequisites and steps are sufficient |
| C:operative:completeness | operative | completeness | thorough operational coverage | 0 | NO_ITEMS | 8-step procedure with 8 verification points is thorough |
| C:operative:consistency | operative | consistency | stable operational discipline | 0 | NO_ITEMS | Procedure is internally consistent |
| C:evaluative:necessity | evaluative | necessity | foundational quality criterion | 0 | NO_ITEMS | Quality criteria are established via P-001 through P-007 |
| C:evaluative:sufficiency | evaluative | sufficiency | substantiated merit assurance | 0 | NO_ITEMS | Merit is substantiated through examples and trade-offs |
| C:evaluative:completeness | evaluative | completeness | comprehensive quality accounting | 0 | NO_ITEMS | Quality accounting is comprehensive |
| C:evaluative:consistency | evaluative | consistency | principled quality coherence | 0 | NO_ITEMS | Quality principles are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | MissingSlot | Procedure | Procedure | Add a verification sub-check in V-7 (Step 7) specifically for P-001 source-language accuracy: a checklist of the four critical phrases from P-001 that must appear verbatim in the final narrative | Procedure Step 7 checks "terminology consistency" but does not enumerate the specific P-001 phrases that must be verified verbatim (e.g., "wear and tear of normal use," "deemed to take effect from the time that the defect has been corrected," "without undue delay," "twenty (20) working days"). Without explicit enumeration, there is a risk of inadvertent paraphrasing that weakens compliance | Procedure.md; Guidance.md | Procedure.md#Step 7 V-7; Guidance.md#P-001 | -- | Procedure.md | TBD |
| C-002 | C:normative:completeness | Normalization | Multi | Guidance | Normalize the treatment of GC 12.5.4.4 across documents: Specification R-06 references "GC 12.5.4.3 and .4" but does not clearly distinguish what .4 adds beyond .3; Datasheet lists inspection right under GC 12.5.4.3 and remedy obligation partially under GC 12.5.4.3 and partially under "GC 12.5.4.3 and .4"; clarify in Guidance what GC 12.5.4.4 specifically covers vs GC 12.5.4.3 | GC 12.5.4.3 and GC 12.5.4.4 are cited together in Specification R-06 and Datasheet but the distinct content of .4 versus .3 is not clearly delineated. Specification R-06 Source says "GC 12.5.4.3 -- inspection right stated within; GC 12.5.4.4 -- remedy obligation continuation." This distinction is not carried into Guidance or Datasheet consistently | Specification.md; Datasheet.md; Guidance.md | Specification.md#R-06; Datasheet.md#Attributes (Owner exhaustive inspection right) | -- | Guidance.md (vocabulary clarification) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandated conformance assurance | 0 | NO_ITEMS | Conformance assurance is addressed through R-01 through R-10 and Verification Table |
| F:normative:sufficiency | normative | sufficiency | verified regulatory sufficiency | 1 | HAS_ITEMS | Scoring rubric alignment gap |
| F:normative:completeness | normative | completeness | total regulatory documentation | 0 | NO_ITEMS | Documentation requirements are complete |
| F:normative:consistency | normative | consistency | uniform conformance standard | 0 | NO_ITEMS | Conformance standards are uniform across docs |
| F:operative:necessity | operative | necessity | essential capability requirement | 0 | NO_ITEMS | Capability requirements are well-defined |
| F:operative:sufficiency | operative | sufficiency | verified execution capacity | 0 | NO_ITEMS | Execution capacity is addressed |
| F:operative:completeness | operative | completeness | exhaustive operational documentation | 0 | NO_ITEMS | Operational documentation is exhaustive |
| F:operative:consistency | operative | consistency | coherent execution uniformity | 1 | HAS_ITEMS | Approval authority naming inconsistency |
| F:evaluative:necessity | evaluative | necessity | essential quality imperative | 0 | NO_ITEMS | Quality imperatives are established |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated value adequacy | 0 | NO_ITEMS | Value adequacy is substantiated through examples |
| F:evaluative:completeness | evaluative | completeness | holistic quality documentation | 0 | NO_ITEMS | Quality documentation is holistic |
| F:evaluative:consistency | evaluative | consistency | principled value integrity | 0 | NO_ITEMS | Value integrity is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale in Guidance for how the 2-point shared scoring across DEL-08-01, DEL-08-02, DEL-08-03 should be weighted or prioritized in terms of narrative investment; currently the scoring weight is stated but no guidance on relative emphasis among the three deliverables is provided | Datasheet states "2 pts (shared within PKG-008 sub-criterion across DEL-08-01, DEL-08-02, DEL-08-03)." Procedure Step 6 references the scoring rubric. However, Guidance does not explain how to allocate narrative effort across the three deliverables sharing these 2 points, nor whether the warranty narrative should emphasize differentiation or compliance | Datasheet.md; Guidance.md; Procedure.md | Datasheet.md#Identification (Evaluation Points); Guidance.md#Notes (Scoring Context); Procedure.md#Step 6 | -- | Guidance.md | TBD |
| F-002 | F:operative:consistency | Normalization | Multi | Guidance | Normalize reviewer role terminology: Procedure Step 8 requires approval from "Quality Lead" and "Legal / Contract Advisor"; Procedure Prerequisites names "Quality Lead; Legal / Contract Advisor" under reviewers. These roles are not mentioned in Specification, Guidance, or Datasheet. Add a brief vocabulary note in Guidance confirming these are the designated review authorities | Procedure introduces "Quality Lead" and "Legal / Contract Advisor" as required reviewers and approval authorities. These roles do not appear in Datasheet (Responsible Party = PM only), Specification, or Guidance. The terminology gap means a reader of Specification or Guidance alone would not know who reviews the narrative | Procedure.md; Datasheet.md | Procedure.md#Prerequisites (Tools and Collaboration); Procedure.md#Step 8; Datasheet.md#Identification (Responsible Party) | -- | Guidance.md and Datasheet.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative compliance directive | 0 | NO_ITEMS | Compliance directives are authoritative and clear |
| D:normative:applying | normative | applying | enforced compliance implementation | 0 | NO_ITEMS | Implementation guidance is enforced through R-01--R-10 |
| D:normative:judging | normative | judging | conclusive conformance ruling | 0 | NO_ITEMS | Acceptance criteria provide conclusive ruling basis |
| D:normative:reviewing | normative | reviewing | systematic compliance assurance | 0 | NO_ITEMS | Master Verification Checklist provides systematic assurance |
| D:operative:guiding | operative | guiding | settled operational steering | 1 | HAS_ITEMS | Missing guidance on interim maintenance responsibility |
| D:operative:applying | operative | applying | confirmed operational execution | 0 | NO_ITEMS | Execution steps are confirmed and clear |
| D:operative:judging | operative | judging | conclusive performance judgment | 0 | NO_ITEMS | Performance judgment criteria are conclusive |
| D:operative:reviewing | operative | reviewing | systematic process verification | 0 | NO_ITEMS | V-1 through V-8 provide systematic verification |
| D:evaluative:guiding | evaluative | guiding | purposeful quality direction | 0 | NO_ITEMS | Quality direction is purposeful |
| D:evaluative:applying | evaluative | applying | confirmed merit realization | 0 | NO_ITEMS | Merit realization is confirmed through examples |
| D:evaluative:judging | evaluative | judging | definitive quality ruling | 0 | NO_ITEMS | Quality ruling criteria are definitive |
| D:evaluative:reviewing | evaluative | reviewing | principled quality examination | 0 | NO_ITEMS | Quality examination is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Guidance | Guidance | Strengthen CON-02 proposed resolution language: currently states "Design-Builder maintains until permit issued is the prudent assumption" but does not specify what "maintains" means operationally (routine maintenance only? defect repairs? emergency response?). Clarify the scope of interim responsibility to reduce ambiguity | CON-02 identifies the interim responsibility gap between commissioning completion and occupancy permit issuance but the proposed authority resolution uses vague language ("maintains"). Under the "settled operational steering" lens, the guidance should provide more specific direction on what maintenance activities fall within this interim period | Guidance.md | Guidance.md#Conflict Table CON-02; Guidance.md#C-005 | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | commanding foundational imperative | 0 | NO_ITEMS | Foundational imperatives are well-established |
| X:guiding:sufficiency | guiding | sufficiency | sufficient directive certification | 0 | NO_ITEMS | Directives are sufficiently certified |
| X:guiding:completeness | guiding | completeness | exhaustive directive coverage | 0 | NO_ITEMS | Directive coverage is exhaustive |
| X:guiding:consistency | guiding | consistency | coherent directive harmony | 0 | NO_ITEMS | Directives are coherently harmonized |
| X:applying:necessity | applying | necessity | required implementation enforcement | 0 | NO_ITEMS | Implementation enforcement is addressed |
| X:applying:sufficiency | applying | sufficiency | adequate implementation assurance | 0 | NO_ITEMS | Implementation assurance is adequate |
| X:applying:completeness | applying | completeness | total implementation coverage | 1 | HAS_ITEMS | Missing Specification requirement for warranty summary schedule |
| X:applying:consistency | applying | consistency | consistent implementation discipline | 0 | NO_ITEMS | Implementation discipline is consistent |
| X:judging:necessity | judging | necessity | essential adjudicative determination | 0 | NO_ITEMS | Adjudicative determinations are essential and present |
| X:judging:sufficiency | judging | sufficiency | sufficient adjudicative validation | 0 | NO_ITEMS | Adjudicative validation is sufficient |
| X:judging:completeness | judging | completeness | exhaustive adjudicative accounting | 0 | NO_ITEMS | Adjudicative accounting is exhaustive |
| X:judging:consistency | judging | consistency | coherent adjudicative uniformity | 0 | NO_ITEMS | Adjudicative uniformity is coherent |
| X:reviewing:necessity | reviewing | necessity | essential oversight assurance | 0 | NO_ITEMS | Oversight assurance is essential and present |
| X:reviewing:sufficiency | reviewing | sufficiency | sufficient oversight evidence | 0 | NO_ITEMS | Oversight evidence is sufficient |
| X:reviewing:completeness | reviewing | completeness | exhaustive oversight accounting | 0 | NO_ITEMS | Oversight accounting is exhaustive |
| X:reviewing:consistency | reviewing | consistency | uniform oversight coherence | 0 | NO_ITEMS | Oversight coherence is uniform |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:completeness | MissingSlot | Specification | Specification | Add a requirement (or sub-requirement under R-09) for the warranty summary schedule recommended in Guidance C-004: "product/system, manufacturer name, warranty period start/end, contact information, and claim procedure" as a required element of the O&M Manual warranty section | Guidance C-004 recommends including a warranty summary schedule in the O&M Manual with specific fields (product/system, manufacturer name, warranty period start/end, contact information, claim procedure). Specification R-09 requires manufacturer warranty collection and O&M Manual inclusion but does not specify the format or required fields of the warranty summary schedule. This is a coverage gap for total implementation: the recommendation exists in Guidance but has no corresponding normative requirement in Specification | Specification.md; Guidance.md | Specification.md#R-09; Guidance.md#C-004 | -- | Specification.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | sovereign compliance mandate | 0 | NO_ITEMS | Compliance mandate is sovereign and well-articulated |
| E:normative:sufficiency | normative | sufficiency | certified regulatory adequacy | 0 | NO_ITEMS | Regulatory adequacy is certified through verification |
| E:normative:completeness | normative | completeness | exhaustive regulatory completeness | 0 | NO_ITEMS | Regulatory completeness is exhaustive |
| E:normative:consistency | normative | consistency | harmonized regulatory uniformity | 0 | NO_ITEMS | Regulatory uniformity is harmonized |
| E:operative:necessity | operative | necessity | critical operational imperative | 0 | NO_ITEMS | Operational imperatives are addressed |
| E:operative:sufficiency | operative | sufficiency | verified operational adequacy | 1 | HAS_ITEMS | Procedure acceptance criteria missing explicit cross-doc consistency check |
| E:operative:completeness | operative | completeness | total operational completeness | 0 | NO_ITEMS | Operational completeness is total |
| E:operative:consistency | operative | consistency | consistent operational coherence | 0 | NO_ITEMS | Operational coherence is consistent |
| E:evaluative:necessity | evaluative | necessity | sovereign quality imperative | 0 | NO_ITEMS | Quality imperatives are sovereign |
| E:evaluative:sufficiency | evaluative | sufficiency | certified quality sufficiency | 0 | NO_ITEMS | Quality sufficiency is certified |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality completeness | 0 | NO_ITEMS | Quality completeness is exhaustive |
| E:evaluative:consistency | evaluative | consistency | unified quality integrity | 0 | NO_ITEMS | Quality integrity is unified |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:sufficiency | VerificationGap | Procedure | Procedure | Add an explicit acceptance criterion (item 8 or sub-item) in Procedure Acceptance Criteria requiring verification that all Datasheet attribute values match the final narrative content (e.g., "12 months," "occupancy permit," "twenty (20) working days," "wear and tear of normal use") | Procedure Step 5 includes V-5 cross-checks between documents, but the Acceptance Criteria list (7 items) does not include an explicit criterion for Datasheet-to-narrative attribute consistency. Under the "verified operational adequacy" lens, the acceptance gate should confirm that the factual parameters in Datasheet are faithfully reflected in the final artifact | Procedure.md; Datasheet.md | Procedure.md#Acceptance Criteria; Procedure.md#Step 5 V-5 | -- | Procedure.md | TBD |
