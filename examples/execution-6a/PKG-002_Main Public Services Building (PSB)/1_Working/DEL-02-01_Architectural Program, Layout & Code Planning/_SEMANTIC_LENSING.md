# Semantic Lensing Register: DEL-02-01 Architectural Program, Layout & Code Planning

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-01_Architectural Program, Layout & Code Planning/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-02-01_Architectural Program, Layout & Code Planning/_CONTEXT.md
- _STATUS.md — DEL-02-01_Architectural Program, Layout & Code Planning/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-02-01_Architectural Program, Layout & Code Planning/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-02-01_Architectural Program, Layout & Code Planning/Datasheet.md
- Specification.md — DEL-02-01_Architectural Program, Layout & Code Planning/Specification.md
- Guidance.md — DEL-02-01_Architectural Program, Layout & Code Planning/Guidance.md
- Procedure.md — DEL-02-01_Architectural Program, Layout & Code Planning/Procedure.md
- _REFERENCES.md — DEL-02-01_Architectural Program, Layout & Code Planning/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 4
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Occupancy classification TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Professional seal timing assumption unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC not accessible; compliance determination incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately addressed via AHJ coordination |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Functional Program availability blocks procedural start |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No performance metrics for design quality beyond checklist |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by verification checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed in Guidance P-1 through P-6 |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered through scoring reference in Procedure A-6 |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination addressed through trade-offs T-1 through T-3 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal addressed through verification table in Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Specification | Clarify occupancy classification (Assembly / business / industrial) -- currently listed as ASSUMPTION with "exact classification TBD at design" | Occupancy classification drives code-minimum room sizes, egress, and accessibility provisions. Leaving it as TBD weakens all downstream prescriptive direction. | Datasheet.md | Attributes > Building Program Overview (Occupancy type row) | -- | Alberta Building Code + AHJ | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify whether professional seal (REQ-02-01-013) is required at proposal stage or only at design milestones -- currently stated as ASSUMPTION | The seal requirement is mandatory practice, but the timing assumption affects whether proposal-stage documents must carry seals. Ambiguity could cause non-compliance. | Specification.md | REQ-02-01-013 -- Professional Seals | -- | RFP Section 7.2; Architects Act (Alberta) | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Obtain Alberta Building Code text to confirm specific accessibility clauses applicable to this occupancy type | Without the ABC text, compliance determination for accessibility (REQ-02-01-006) cannot be completed. The Specification and Procedure reference it but note it as "external -- not directly accessible." | Specification.md; Procedure.md | REQ-02-01-006; Standards table; Prerequisites | -- | Alberta Building Code (external) | TBD |
| A-004 | A:operative:guiding | TBD_Question | Procedure | Procedure | Record TBD: Confirm location and accessibility of Functional Program (Appendix B) before Step A-2 can proceed | Functional Program is listed as "location TBD" across all four documents. It governs room list and areas, making it a blocking prerequisite for procedural direction. | Procedure.md | Prerequisites > Information Required Before Starting | -- | RFP Appendix B | TBD |
| A-005 | A:operative:judging | MissingSlot | Specification | Specification | Add measurable performance criteria for design quality beyond pass/fail checklist verification (e.g., adjacency efficiency, circulation ratio) | Specification verification is all document-review-based. No quantitative performance assessment criteria exist for the architectural program quality itself. | Specification.md | Verification table | -- | Design-Builder (Architect) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Total program area is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Multiple space sizes listed as TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Functional Program not accessible |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Inconsistent area reference for bunker gear |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (Owner intent, integration requirement) are clear |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided across Guidance and Datasheet |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account is comprehensive given accessible sources |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of program requirements is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed through professional seal requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery addressed through Guidance principles and considerations |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment addressed through trade-offs and considerations |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately supported by Guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight present in Guidance P-6 and trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add total building program area (aggregate ft2) once Functional Program is reviewed -- currently "TBD" | Total program area is an essential fact for building sizing. It is listed as TBD in the Datasheet, blocking meaningful layout verification. | Datasheet.md | Attributes > Building Program Overview (Total program areas row) | -- | Functional Program (Appendix B) | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Populate TBD area values for Kitchen/Breakroom, Meeting Room, PW PPE/Locker Room, Executive/Regular Offices, Utility rooms | Multiple spaces in the Datasheet Space Program table have "TBD (from Functional Program)" for size. Without these, evidence is inadequate for layout. | Datasheet.md | Attributes > Space Program -- Key Spaces | -- | Functional Program (Appendix B) | TBD |
| B-003 | B:data:completeness | MissingSlot | Multi | Datasheet | Add complete room list from Functional Program (Appendix B) once accessible -- current list is partial | The Datasheet room list is drawn from OSR and Addendum 03 samples only. The Functional Program (Appendix B) governs the full room list but was not accessible. Comprehensive record is incomplete. | Datasheet.md; Specification.md | Datasheet: Space Program; Specification: REQ-02-01-004 | -- | Functional Program (Appendix B) | TBD |
| B-004 | B:data:consistency | Conflict | Guidance | Guidance | Resolve whether "Fire Gear Storage (200-350 ft2)" in Addendum 03 sec1.21 is the same space as the bunker gear locker room requiring 40 lockers -- Guidance flags this as ambiguous | Datasheet lists "Fire Gear Storage" at 200-350 ft2 for 40 bunker gear lockers; Guidance C-3 flags that the locker room would need to be larger. This data inconsistency could lead to undersized space. | Datasheet.md; Guidance.md | Datasheet: Space Program (Fire Gear Storage row); Guidance: C-3 Bunker Gear Locker Room Sizing | Datasheet.md#Space-Program (200-350 ft2); Guidance.md#C-3 (larger needed for 40 lockers) | Addendum 03 sec1.21 vs sec1.13; Owner confirmation needed | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Regulatory Threshold | 1 | HAS_ITEMS | Accessibility code thresholds not yet determinable |
| C:normative:sufficiency | normative | sufficiency | Regulatory Substantiation | 0 | NO_ITEMS | Substantiation approach present in verification table |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Coverage | 1 | HAS_ITEMS | Standards table marks multiple codes as not accessible |
| C:normative:consistency | normative | consistency | Codified Conformance Standard | 0 | NO_ITEMS | Standards consistently referenced across documents |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 1 | HAS_ITEMS | Site plan coordination prerequisite is assumption-only |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Competence | 0 | NO_ITEMS | Competence addressed through seal and design-builder role |
| C:operative:completeness | operative | completeness | Thorough Process Execution | 0 | NO_ITEMS | Procedure steps are thorough for proposal stage |
| C:operative:consistency | operative | consistency | Reliable Process Alignment | 0 | NO_ITEMS | Process alignment consistent between Procedure and Specification |
| C:evaluative:necessity | evaluative | necessity | Inherent Worth Criterion | 0 | NO_ITEMS | Worth criteria addressed through RFP scoring reference |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Value Assessment | 0 | NO_ITEMS | Value assessment present in Guidance trade-offs |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Accounting | 0 | NO_ITEMS | Merit accounting covered by P-1 through P-6 and T-1 through T-3 |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence maintained across Guidance principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for how occupancy classification will be determined and confirmed -- REQ-02-01-006 references ABC but classification is TBD | The binding regulatory threshold for accessibility depends on occupancy classification (Assembly / business / industrial). Without a confirmed classification, the accessibility requirements cannot be fully specified or verified. | Specification.md; Datasheet.md | REQ-02-01-006; Datasheet: Occupancy type | -- | Alberta Building Code; AHJ | TBD |
| C-002 | C:normative:completeness | RationaleGap | Specification | Guidance | Add rationale for why NMS (National Master Specification) format is listed as "Recommended" rather than mandatory -- clarify whether Owner requires NMS or accepts alternatives | The Standards table lists NMS as document format standard but notes it as "Recommended format per RFP sec7.2." If compliance coverage is to be exhaustive, the mandatory/optional status of this standard should be clarified. | Specification.md | Standards table (NMS row) | -- | RFP Section 7.2 | TBD |
| C-003 | C:operative:necessity | WeakStatement | Procedure | Procedure | Strengthen site plan coordination from ASSUMPTION to formal prerequisite or coordination requirement with DEL-03-01 | Procedure Prerequisites lists site plan coordination with DEL-03-01 as "ASSUMPTION" only. This is an operational prerequisite for confirming building footprint -- it should be a declared dependency or formal coordination step. | Procedure.md | Prerequisites > Upstream Coordination | -- | Design-Builder (PM) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Compulsory Compliance Foundation | 1 | HAS_ITEMS | Foundation requires occupancy classification resolution |
| F:normative:sufficiency | normative | sufficiency | Adequate Regulatory Basis | 0 | NO_ITEMS | Regulatory basis adequate for accessible sources |
| F:normative:completeness | normative | completeness | Total Regulatory Scope Mastery | 0 | NO_ITEMS | Scope mastery limited only by inaccessible external codes |
| F:normative:consistency | normative | consistency | Systematic Normative Coherence | 0 | NO_ITEMS | Normative coherence maintained |
| F:operative:necessity | operative | necessity | Validated Operational Awareness | 1 | HAS_ITEMS | Structural grid coordination not validated |
| F:operative:sufficiency | operative | sufficiency | Sufficient Procedural Capability | 0 | NO_ITEMS | Procedural capability sufficient given role definition |
| F:operative:completeness | operative | completeness | Complete Operational Mastery | 0 | NO_ITEMS | Operational mastery appropriately scoped for proposal stage |
| F:operative:consistency | operative | consistency | Disciplined Operational Framework | 0 | NO_ITEMS | Framework consistent between Procedure and Specification |
| F:evaluative:necessity | evaluative | necessity | Foundational Value Comprehension | 0 | NO_ITEMS | Value comprehension addressed in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Value Appraisal | 0 | NO_ITEMS | Value appraisal grounded through Owner intent discussion |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Mastery | 1 | HAS_ITEMS | Lifecycle cost consideration missing from worth analysis |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Alignment | 0 | NO_ITEMS | Merit alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification step for occupancy classification determination prior to completing accessibility and egress requirements | REQ-02-01-006 requires accessibility compliance but the occupancy classification (which determines applicable code provisions) is stated as ASSUMPTION/TBD. No verification step confirms classification before downstream requirements are finalized. | Specification.md | REQ-02-01-006; Verification table (REQ-02-01-006 row) | -- | AHJ; Alberta Building Code | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add explicit coordination step with structural lead (DEL-02-04) for bay grid confirmation as a required input to Step A-3 | Procedure Step A-3 develops building layout but does not include a formal coordination step with DEL-02-04 structural lead for bay grid preferences, despite Guidance P-6 noting structural grid drives layout efficiency. This is a validated operational awareness gap. | Procedure.md | Steps > Phase A > Step A-3 | -- | Design-Builder (PM); DEL-02-04 lead | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add lifecycle cost consideration narrative to Guidance -- C-1 trade-off mentions lifecycle basis but no framework for lifecycle cost comparison is provided | Guidance C-1 states two-storey "may be cost-advantageous on a total lifecycle basis" but no lifecycle cost evaluation framework or criteria are provided. For comprehensive worth mastery, a brief lifecycle cost consideration methodology would strengthen the evaluation basis. | Guidance.md | C-1: Two-Storey vs. Single-Storey Trade-off | -- | Design-Builder (cost estimator) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Directive | 1 | HAS_ITEMS | CCDC 14-2013 listed but role not explained |
| D:normative:applying | normative | applying | Binding Practice Fulfillment | 0 | NO_ITEMS | Binding practices covered through requirements |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance ruling pathway clear through AHJ |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Inspection | 0 | NO_ITEMS | Inspection pathway addressed in Procedure Phase B |
| D:operative:guiding | operative | guiding | Confirmed Procedural Stewardship | 1 | HAS_ITEMS | No design review gate between steps |
| D:operative:applying | operative | applying | Enacted Capability Deployment | 0 | NO_ITEMS | Capability deployment covered through procedure steps |
| D:operative:judging | operative | judging | Settled Performance Evaluation | 0 | NO_ITEMS | Performance evaluation addressed in verification checks |
| D:operative:reviewing | operative | reviewing | Disciplined Process Inspection | 0 | NO_ITEMS | Process inspection covered by verification table |
| D:evaluative:guiding | evaluative | guiding | Principled Value Authority | 0 | NO_ITEMS | Value authority established through Guidance principles |
| D:evaluative:applying | evaluative | applying | Enacted Merit Deployment | 1 | HAS_ITEMS | RFP scoring criteria not mapped to requirements |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | Worth ruling addressed through trade-off analysis |
| D:evaluative:reviewing | evaluative | reviewing | Principled Quality Inspection | 0 | NO_ITEMS | Quality inspection covered adequately |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | RationaleGap | Specification | Guidance | Add brief explanation of how CCDC 14-2013 contract form affects architectural deliverable requirements (e.g., design milestone definitions, document submission obligations) | CCDC 14-2013 is listed in the Standards table as the governing contract form, but no rationale explains how it shapes deliverable obligations for this architectural program. An authoritative compliance directive requires understanding why the standard applies. | Specification.md | Standards table (CCDC 14-2013 row) | -- | RFP Section 5.4 | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add internal design review gate or quality check between Phase A steps (e.g., after Step A-3 layout, before proceeding to A-4 accessibility) | Procedure Phase A steps proceed sequentially without explicit internal review gates. Confirmed procedural stewardship requires checkpoints to confirm prior step output is adequate before proceeding. | Procedure.md | Steps > Phase A | -- | Design-Builder (Architect) | TBD |
| D-003 | D:evaluative:applying | Normalization | Specification | Specification | Map RFP scoring criteria (e.g., 15 points for Adaptability sec7.1.5) to specific REQ- numbers so that merit deployment is traceable | Procedure Step A-6 references RFP sec7.1.5 scoring criterion (15 points) but the Specification requirements do not cross-reference scoring weights. For enacted merit deployment, traceability from evaluation criteria to requirements would strengthen the deliverable. | Specification.md; Procedure.md | Procedure: Step A-6; Specification: REQ-02-01-011 | -- | RFP scoring criteria | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Governing Foundational Mandate | 0 | NO_ITEMS | Foundational mandate established through RFP/OSR references |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Governance Capability | 0 | NO_ITEMS | Governance capability established through professional requirements |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Purview | 0 | NO_ITEMS | Governance purview adequate for scope |
| X:guiding:consistency | guiding | consistency | Coherent Governance Codification | 0 | NO_ITEMS | Governance codification consistent |
| X:applying:necessity | applying | necessity | Mobilized Compliance Resource | 1 | HAS_ITEMS | Verification milestones not tied to contract milestones |
| X:applying:sufficiency | applying | sufficiency | Adequate Enacted Competence | 0 | NO_ITEMS | Competence adequately enacted through DB role |
| X:applying:completeness | applying | completeness | Total Deployed Realization | 0 | NO_ITEMS | Realization covered through artifact list |
| X:applying:consistency | applying | consistency | Reliable Applied Standard | 0 | NO_ITEMS | Applied standards consistently referenced |
| X:judging:necessity | judging | necessity | Decisive Foundational Verdict | 1 | HAS_ITEMS | No acceptance criteria for expansion concept "credibility" |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicated Evidence | 0 | NO_ITEMS | Evidence sufficiency addressed through verification methods |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Finding | 0 | NO_ITEMS | Finding exhaustiveness appropriate for proposal stage |
| X:judging:consistency | judging | consistency | Uniform Adjudicative Principle | 1 | HAS_ITEMS | Verification methods not uniform -- mix of review and cross-check |
| X:reviewing:necessity | reviewing | necessity | Audited Foundational Compliance | 0 | NO_ITEMS | Compliance audit pathway established |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Inspected Evidence | 0 | NO_ITEMS | Evidence inspection sufficient |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Coverage | 0 | NO_ITEMS | Inspection coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Uniform Oversight Standard | 0 | NO_ITEMS | Oversight standard consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Normalization | Specification | Specification | Normalize verification milestone names (e.g., "Building Design Development" vs "60% Detailed Design" vs "100% Detailed Design") to align with contract milestone terminology from CCDC 14-2013 or RFP | Specification verification table uses three different milestone labels without defining them or mapping them to contract milestones. This inconsistency in milestone naming could cause confusion about when verifications are due. | Specification.md | Verification table (Milestone column) | -- | CCDC 14-2013; RFP milestone definitions | TBD |
| X-002 | X:judging:necessity | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-02-01-011 expansion concept -- "credibility" is subjective | REQ-02-01-011 verification says "Expansion concept document reviewed for credibility." The word "credibility" is not defined, making a decisive foundational verdict impossible. Needs objective criteria. | Specification.md | Verification table (REQ-02-01-011 row) | -- | Design-Builder (Architect) | TBD |
| X-003 | X:judging:consistency | Normalization | Specification | Specification | Standardize verification method descriptions -- some say "reviewed" while others say "cross-checked" or "confirmed" without distinguishing what each entails | Verification methods in the Specification table use varied terms (reviewed, cross-checked, confirmed, checked) without defining the rigor level of each. For uniform adjudicative principle, consistent terminology would improve clarity. | Specification.md | Verification table (Verification Method column) | -- | Design-Builder QA/QC | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Absolute Compliance Authority | 0 | NO_ITEMS | Compliance authority established through AHJ and code references |
| E:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Standard | 1 | HAS_ITEMS | Egress requirements not substantiated |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Realization | 0 | NO_ITEMS | Regulatory realization appropriate for proposal stage |
| E:normative:consistency | normative | consistency | Codified Regulatory Doctrine | 0 | NO_ITEMS | Regulatory doctrine consistent across documents |
| E:operative:necessity | operative | necessity | Verified Operational Foundation | 0 | NO_ITEMS | Operational foundation verified through prerequisite checks |
| E:operative:sufficiency | operative | sufficiency | Verified Operational Sufficiency | 0 | NO_ITEMS | Operational sufficiency adequate |
| E:operative:completeness | operative | completeness | Complete Process Realization | 0 | NO_ITEMS | Process realization complete for proposal scope |
| E:operative:consistency | operative | consistency | Systematic Operational Norm | 0 | NO_ITEMS | Operational norms systematic |
| E:evaluative:necessity | evaluative | necessity | Sovereign Worth Foundation | 0 | NO_ITEMS | Worth foundation established through Owner intent |
| E:evaluative:sufficiency | evaluative | sufficiency | Proven Value Standing | 0 | NO_ITEMS | Value standing supported by Guidance |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Worth Actualization | 1 | HAS_ITEMS | No explicit Owner satisfaction criteria |
| E:evaluative:consistency | evaluative | consistency | Coherent Worth Doctrine | 0 | NO_ITEMS | Worth doctrine coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | VerificationGap | Specification | Specification | Add egress requirements or cross-reference to applicable code provisions for single-storey and two-storey configurations | Specification mentions egress in REQ-02-01-010 (two-storey) as needing "second floor egress planning" but no requirement or verification exists for egress compliance in either configuration. For substantiated regulatory standard, egress must be addressed. | Specification.md; Guidance.md | REQ-02-01-010; Guidance C-1 (egress row in trade-off table) | -- | Alberta Building Code | TBD |
| E-002 | E:evaluative:completeness | VerificationGap | Specification | Specification | Add Owner review/acceptance step in verification table -- no requirement captures Owner satisfaction with architectural program before proceeding to design development | The verification table covers document-review and cross-check methods but does not include an Owner acceptance milestone. For exhaustive worth actualization, the Owner's evaluation of the architectural program should be a formal verification point. | Specification.md; Procedure.md | Specification: Verification table; Procedure: Phase B Step B-1 | -- | Owner / Project Committee | TBD |
