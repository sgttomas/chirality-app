# Semantic Lensing Register: DEL-10-01 Risk Register and Mitigation Plan

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-010_Due_Diligence_and_Risk_Management/1_Working/DEL-10-01_RiskRegisterAndMitigationPlan
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-10-01 identity, description, scope (SOW-0028), objective alignment (OBJ-008)
- _STATUS.md -- Current state: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- 7 matrices parsed (A, B, C, F, D, X, E); 92 cells total
- Datasheet.md -- Risk register column schema, 26 risk entries across 6 categories, conditions, references, TBD items
- Specification.md -- 13 requirements (R-001 through R-013), verification matrix, standards
- Guidance.md -- 6 principles, 5 considerations, 3 trade-offs, examples, conflict table
- Procedure.md -- 6-step production procedure, prerequisites, verification checks, records
- _REFERENCES.md -- Package references, source documents, cross-references (DEL-10-02, DEL-01-06)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 8
  - Specification: 7
  - Guidance: 4
  - Procedure: 4
- By matrix:
  - A: 4  B: 4  C: 3  F: 3  D: 3  X: 3  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Risk rating scale lacks prescriptive definition in Datasheet |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Register Status column has no entries showing Active/Mitigated/Closed |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | R-001 through R-013 provide adequate compliance criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No verification check for R-013 proposal positioning |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-6 provides thorough procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Workshop and compilation steps are well-specified |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks (V-001 through V-012) are comprehensive |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No periodic re-review cycle defined for register updates |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | OBJ-008 value alignment is well-addressed in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | T-002 trade-off between transparency and positioning is appropriate |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Credibility review (Step 6.2) addresses worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA checklist and Proposal Manager review are adequate |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Clarify how L x I Risk Level composite ratings are assigned (e.g., define the mapping from Low/Medium/High x Low/Medium/High/Critical to Green/Amber/Red) | Datasheet Attributes states "Risk Level (L x I)" but the mapping from combined Likelihood x Impact to a risk level color/category is only defined in Procedure Step 2.3. The Datasheet itself lacks the prescriptive definition, creating ambiguity for anyone reading it standalone. | Datasheet.md; Procedure.md | Datasheet: Attributes table, row "Risk Rating Scale"; Procedure: Step 2.3 | -- | Datasheet.md | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add Status column values (Active/Mitigated/Closed) to each risk entry in the register tables | Specification R-002 requires a Status column for each entry, and the column schema in Construction section defines it, but the actual register entries in Datasheet omit the Status column entirely from all six category tables. | Datasheet.md | Datasheet: Construction > Risk Register -- Current Entries (all six category tables) | -- | Specification.md (R-002) | TBD |
| A-003 | A:normative:reviewing | VerificationGap | Specification | Specification | Add verification method and responsible party for R-013 (Proposal Positioning Alignment) to the Verification table | R-013 states "Proposal Manager review confirms tone and positioning" but the Verification table row for R-013 shows "Proposal Manager" at "Final review" stage without specifying the method (e.g., checklist, sign-off, narrative review). Other requirements have more specific methods. | Specification.md | Specification: Verification table, row R-013 | -- | Specification.md | TBD |
| A-004 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a note or step describing when and how the register is updated post-submission (post-award lifecycle review cycle, frequency, triggers) | Procedure Records section mentions "Update monthly during design and construction" under Post-Award Records but does not define a process audit or re-review step. The six-step procedure ends at proposal lock with no re-entry protocol. | Procedure.md | Procedure: Records > Post-Award Records | -- | Procedure.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing specific geotechnical parameters |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Reference reports not directly accessed |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Risk Level column missing from register tables |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Likelihood and Impact scales are consistently defined |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Risk descriptions provide adequate signal |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Source citations provide adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Category summaries in Guidance are comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for apparatus bay |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Risk management philosophy is well-grounded |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Team role assignments demonstrate competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Six categories cover appropriate risk domain |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-document understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | DEC-013 risk acceptance demonstrates discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs are well-reasoned |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Considerations cover site, design, cost, permitting, procurement |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-001 through P-006 are internally consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | TBD: Obtain specific geotechnical parameters (soil bearing capacity, groundwater depth, frost depth) from the 2021 Geotechnical Investigation Report to ground RISK-SIT-04 in factual data | Datasheet TBD Items lists "Specific geotechnical findings (soil bearing capacity, groundwater depth, frost depth) from 2021 report -- not directly accessed." These essential facts would materially change the risk assessment for RISK-SIT-04 but are absent. | Datasheet.md | Datasheet: TBD Items (bullet 2) | -- | 2021 Geotechnical Investigation Report | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Strengthen source citations for RISK-SIT-01 through RISK-SIT-06 by noting which specific Decomposition v2.3 subsections provide the referenced findings, or explicitly mark as "secondary source: Decomposition v2.3 summary" | Five of six Site/Environmental risk entries reference reports that are "location TBD" and "not directly accessed." The adequacy of evidence for these entries rests entirely on Decomposition v2.3 summaries, which is disclosed but could be made more explicit in each entry. | Datasheet.md | Datasheet: Construction > Category: Site/Environmental | -- | Datasheet.md | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Risk Level (L x I composite) column to all six category register tables to match the column schema defined in the same document | The column schema in Datasheet Construction section defines "Risk Level" as "Combined L x I rating (e.g., High-Critical = red)" but the actual register tables omit this column. They show Likelihood and Impact separately but do not include the computed Risk Level column. | Datasheet.md | Datasheet: Construction > Risk Register -- Column Schema vs. Current Entries tables | -- | Datasheet.md (internal consistency) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: Datasheet uses "fire bay" in fill station context (RISK-SIT-06 refers to "1 fire bay, 1 PW bay" in Addendum 03 context) while Procedure Step 5.4 defines canonical form as "apparatus bay (not fire bay)" | Procedure Step 5.4 terminology table says "apparatus bay" is canonical and "fire bay" should only be used in fill station context. However, Datasheet RISK-DES-01 description refers to disciplines generically and does not use the term, while the Addendum 03 items in Specification R-004 use neither. Minor normalization gap. | Datasheet.md; Procedure.md | Datasheet: entire register; Procedure: Step 5.4 Terminology Consistency table | -- | Procedure.md (terminology table) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory compliance acuity | 1 | HAS_ITEMS | ISO 31000 cited as ASSUMPTION without confirming applicability |
| C:normative:sufficiency | normative | sufficiency | justified regulatory baseline | 0 | NO_ITEMS | Regulatory baseline from RFP and Addenda is well-justified |
| C:normative:completeness | normative | completeness | total regulatory coverage | 1 | HAS_ITEMS | CCDC 14-2013 not directly accessed |
| C:normative:consistency | normative | consistency | harmonized compliance integrity | 0 | NO_ITEMS | Authority order (Addendum 03 > base RFP) is clearly stated |
| C:operative:necessity | operative | necessity | critical operational competence | 0 | NO_ITEMS | Team role assignments map competences to categories |
| C:operative:sufficiency | operative | sufficiency | proven execution capability | 0 | NO_ITEMS | Workshop process demonstrates execution capability |
| C:operative:completeness | operative | completeness | thorough operational accounting | 0 | NO_ITEMS | Six-step procedure is thorough |
| C:operative:consistency | operative | consistency | dependable process coherence | 0 | NO_ITEMS | Steps are sequenced logically |
| C:evaluative:necessity | evaluative | necessity | intrinsic merit discernment | 0 | NO_ITEMS | P-001 project specificity principle covers merit discernment |
| C:evaluative:sufficiency | evaluative | sufficiency | warranted quality appraisal | 1 | HAS_ITEMS | No quality criteria for the narrative artifact itself |
| C:evaluative:completeness | evaluative | completeness | comprehensive merit accounting | 0 | NO_ITEMS | T-001 trade-off addresses completeness vs. manageability |
| C:evaluative:consistency | evaluative | consistency | principled valuation coherence | 0 | NO_ITEMS | Guidance principles are internally coherent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Specification | Guidance | Add rationale for why ISO 31000:2018 is cited as applicable by assumption when the RFP does not require it; clarify whether it is a process guide or a compliance obligation | Specification Standards table lists ISO 31000:2018 with "ASSUMPTION: Applicable by industry convention; not cited by RFP." There is no explanation of what specific ISO 31000 elements the register intends to follow, or whether non-conformance to ISO 31000 would be considered a gap. | Specification.md | Specification: Standards table, row ISO 31000:2018 | -- | Guidance.md | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Clarify access status and applicability of CCDC 14-2013 with Appendix J for risk allocation; note which specific supplementary conditions affect risk register content | Specification Standards table lists CCDC 14-2013 as "Risk allocation framework for Design-Build delivery" with "Location TBD -- not directly accessed." If this standard defines risk allocation between Owner and DB contractor, its content could materially shape risk entries (e.g., who bears foundation risk). | Specification.md | Specification: Standards table, row CCDC 14-2013 | -- | Specification.md | TBD |
| C-003 | C:evaluative:sufficiency | VerificationGap | Specification | Specification | Add quality criteria or acceptance standard for the Risk Mitigation Narrative artifact (e.g., minimum length, section structure validation, readability standard) beyond the five-element check in R-009 | R-009 requires five identifiable elements in the narrative but does not define how to evaluate the quality or depth of each element. The Verification table says "Review narrative for five elements; confirm each is present" which is a presence check, not a quality appraisal. | Specification.md | Specification: Requirements > R-009; Verification table row R-009 | -- | Specification.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | compulsory regulatory command | 0 | NO_ITEMS | R-001 through R-006 establish compulsory coverage |
| F:normative:sufficiency | normative | sufficiency | defensible regulatory standing | 1 | HAS_ITEMS | AHJ permitting timeline is assumed not verified |
| F:normative:completeness | normative | completeness | absolute regulatory scope | 1 | HAS_ITEMS | Alberta OH&S cited but no risk entries address construction safety |
| F:normative:consistency | normative | consistency | principled regulatory alignment | 0 | NO_ITEMS | Authority hierarchy is consistent |
| F:operative:necessity | operative | necessity | essential performance insight | 0 | NO_ITEMS | Performance insight is embedded in risk assessments |
| F:operative:sufficiency | operative | sufficiency | validated execution competence | 0 | NO_ITEMS | Mitigation strategies demonstrate execution competence |
| F:operative:completeness | operative | completeness | total operational mastery | 0 | NO_ITEMS | Six-step procedure covers full operational scope |
| F:operative:consistency | operative | consistency | principled operational stability | 0 | NO_ITEMS | Process is stable and well-sequenced |
| F:evaluative:necessity | evaluative | necessity | foundational value perception | 0 | NO_ITEMS | OBJ-008 alignment provides value foundation |
| F:evaluative:sufficiency | evaluative | sufficiency | defensible appraisal practice | 0 | NO_ITEMS | Risk rating scales provide defensible appraisal basis |
| F:evaluative:completeness | evaluative | completeness | absolute merit comprehension | 1 | HAS_ITEMS | No risk entries for construction-phase safety hazards |
| F:evaluative:consistency | evaluative | consistency | principled merit alignment | 0 | NO_ITEMS | Merit alignment with OBJ-008 is principled |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for the assumed AHJ review timeline (4-8 weeks) cited in C-004; explain basis for this estimate and note it as a key schedule risk assumption requiring early validation | Guidance C-004 states "AHJ review timelines in Penhold/Red Deer County jurisdiction are TBD but should be assumed at 4-8 weeks minimum." This assumption is not grounded in any cited source and could materially affect RISK-SCH-02 and RISK-PER-01 schedule risk assessments. | Guidance.md | Guidance: Considerations > C-004 | -- | Guidance.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Datasheet | Datasheet | Consider adding a construction-phase safety risk entry (e.g., risks from working with apparatus bay direct exhaust installations, sump construction, or overhead door installation at 16 ft height) if Alberta OH&S is cited as applicable | Specification Standards table cites "Alberta OH&S Legislation" as applicable for "Safety risk context for construction phase" (marked ASSUMPTION). However, no risk entries in any category address construction-phase worker safety hazards. If OH&S is scoped in, at least one safety risk entry would be expected. | Specification.md; Datasheet.md | Specification: Standards table, row Alberta OH&S; Datasheet: entire register scanned | -- | Specification.md | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Datasheet | Datasheet | Consider adding a risk entry addressing the risk that the proposal itself may fail to score well on OBJ-008 if register quality is insufficient (a meta-risk on deliverable effectiveness) | Guidance Purpose section identifies three audiences and OBJ-008 scoring. Specification R-013 requires credible positioning. However, no risk entry in the register addresses the meta-risk that the deliverable itself may be evaluated as insufficient, which is a real proposal-stage risk. This is a judgment call on whether meta-risks belong in the register. | Guidance.md; Specification.md | Guidance: Purpose; Specification: R-013 | -- | NA | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative regulatory guidance | 0 | NO_ITEMS | Guidance P-002 provides authoritative Addendum 03 direction |
| D:normative:applying | normative | applying | established compliance method | 1 | HAS_ITEMS | Cross-document consistency method needs timing |
| D:normative:judging | normative | judging | definitive conformance judgment | 0 | NO_ITEMS | Verification matrix provides conformance judgment criteria |
| D:normative:reviewing | normative | reviewing | systematic enforcement examination | 0 | NO_ITEMS | Step 6 QA provides systematic examination |
| D:operative:guiding | operative | guiding | confirmed operational guidance | 0 | NO_ITEMS | Procedure prerequisites and steps provide operational guidance |
| D:operative:applying | operative | applying | established implementation capability | 1 | HAS_ITEMS | Workshop time allocation may be insufficient |
| D:operative:judging | operative | judging | confirmed performance evaluation | 0 | NO_ITEMS | V-001 through V-012 confirm performance evaluation framework |
| D:operative:reviewing | operative | reviewing | systematic operational examination | 0 | NO_ITEMS | Step 5 cross-document review is systematic |
| D:evaluative:guiding | evaluative | guiding | established merit guidance | 0 | NO_ITEMS | Guidance examples (EX-001 through EX-003) establish merit direction |
| D:evaluative:applying | evaluative | applying | established quality practice | 0 | NO_ITEMS | QA checklist demonstrates quality practice |
| D:evaluative:judging | evaluative | judging | definitive value judgment | 1 | HAS_ITEMS | Contingency reserve approach defers to DEL-01-06 without criteria |
| D:evaluative:reviewing | evaluative | reviewing | systematic merit review | 0 | NO_ITEMS | Proposal Manager review provides merit review |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Procedure | Procedure | Add timing guidance for when Step 5 cross-document consistency review should occur relative to DEL-10-02, DEL-01-06, and DEL-09-01 availability; note dependency on those deliverables being at least draft-complete | Procedure Step 5 requires cross-checking against DEL-10-02, DEL-01-06, and DEL-09-01 but does not specify when these deliverables will be available or what to do if they are not yet drafted. The compliance method exists but its execution timing is undefined. | Procedure.md | Procedure: Step 5 (all subsections) | -- | Procedure.md | TBD |
| D-002 | D:operative:applying | RationaleGap | Procedure | Guidance | Add rationale for workshop time allocations in Step 1.2 (e.g., why Design gets 30-40 min but Procurement gets 15-20 min); note whether allocations are proportional to risk significance or can be adjusted | Procedure Step 1.2 assigns specific time ranges per category but does not explain the basis. For a project where Site/Environmental risk is arguably the highest-severity cluster (per Guidance C-001), giving it the same time as Design may be insufficient. | Procedure.md | Procedure: Step 1.2, Risk Identification Workshop table | -- | Guidance.md | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Guidance | Guidance | Add guidance on what criteria the PM should use to evaluate whether the contingency reserve referenced in DEL-01-06 is adequate relative to the risk profile identified in this register | Guidance T-003 discusses contingency reserve quantification and defers to DEL-01-06 for dollar amounts. However, no guidance exists on how the PM should judge whether the contingency reserve is proportionate to the risk profile. This is a value judgment that needs at least directional guidance. | Guidance.md | Guidance: Trade-offs > T-003 | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | imperative governance stewardship | 0 | NO_ITEMS | Governance structure is clear (PM + Technical Leads) |
| X:guiding:sufficiency | guiding | sufficiency | substantiated guidance framework | 0 | NO_ITEMS | Guidance document provides substantiated framework |
| X:guiding:completeness | guiding | completeness | holistic governance authority | 0 | NO_ITEMS | Authority hierarchy (Addendum 03 > RFP) is holistic |
| X:guiding:consistency | guiding | consistency | harmonized directional integrity | 1 | HAS_ITEMS | Residual risk format inconsistency |
| X:applying:necessity | applying | necessity | indispensable practice rigor | 1 | HAS_ITEMS | Category column missing from register tables |
| X:applying:sufficiency | applying | sufficiency | proven practice adequacy | 0 | NO_ITEMS | Mitigation practices are adequate |
| X:applying:completeness | applying | completeness | thorough practice documentation | 0 | NO_ITEMS | Practice documentation is thorough |
| X:applying:consistency | applying | consistency | stable practice alignment | 0 | NO_ITEMS | Practice steps are aligned |
| X:judging:necessity | judging | necessity | binding determination authority | 0 | NO_ITEMS | PM has determination authority for sign-off |
| X:judging:sufficiency | judging | sufficiency | warranted adjudication standing | 0 | NO_ITEMS | Verification methods are warranted |
| X:judging:completeness | judging | completeness | total adjudication scope | 1 | HAS_ITEMS | No verification for narrative tone consistency across categories |
| X:judging:consistency | judging | consistency | principled adjudication integrity | 0 | NO_ITEMS | Adjudication criteria are principled and consistent |
| X:reviewing:necessity | reviewing | necessity | indispensable audit discipline | 0 | NO_ITEMS | V-001 through V-012 provide audit discipline |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated review standing | 0 | NO_ITEMS | Review standing is substantiated |
| X:reviewing:completeness | reviewing | completeness | total review comprehension | 0 | NO_ITEMS | QA checklist covers all requirements |
| X:reviewing:consistency | reviewing | consistency | principled review coherence | 0 | NO_ITEMS | Review process is coherent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Datasheet | Datasheet | Standardize residual risk notation format: some entries use "Low-Medium" (Likelihood-Impact), others use "Low-Low," but the format is not explicitly defined; add a note to the column schema clarifying the notation convention | Datasheet register entries use compound residual risk ratings (e.g., "Medium-Medium," "Low-Medium," "Low-High," "Low-Low") but the Column Schema section only says "Likelihood/Impact after mitigation" without specifying the notation format (dash-separated? slash-separated?). This is a minor normalization gap. | Datasheet.md | Datasheet: Construction > Risk Register -- Column Schema, row "Residual Risk"; Current Entries tables | -- | Datasheet.md | TBD |
| X-002 | X:applying:necessity | Conflict | Datasheet | Datasheet | Resolve: Datasheet Column Schema defines 10 columns including "Category" and "Status" but actual register tables omit both Category column (implicit from section headers) and Status column entirely. Either add the columns to tables or update schema to reflect the actual table structure. | Datasheet Column Schema says register entries include Category and Status columns. The actual tables organize by category section headers (so Category is implicit) but Status is completely absent. This is an internal conflict within Datasheet between schema definition and actual data. | Datasheet.md | Datasheet: Construction > Risk Register -- Column Schema vs. Current Entries | Datasheet.md#Column Schema; Datasheet.md#Current Entries | Specification.md (R-002) | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Procedure | Add a verification step ensuring that the narrative category summaries (R-009 element c) are consistent in tone and depth across all six categories, not just checking for presence | Specification R-009 requires six category summaries but verification is limited to presence check. Procedure Step 4.2 section (c) provides a template for Site/Environmental but no equivalent guidance for the other five categories. An uneven narrative could undermine OBJ-008 credibility. | Specification.md; Procedure.md | Specification: R-009; Procedure: Step 4.2 section (c) | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | absolute compliance authority | 0 | NO_ITEMS | Compliance framework is authoritative |
| E:normative:sufficiency | normative | sufficiency | warranted regulatory adequacy | 1 | HAS_ITEMS | NBCC cited but no risk entries reference building code compliance |
| E:normative:completeness | normative | completeness | total regulatory jurisdiction | 0 | NO_ITEMS | Regulatory scope is comprehensive for proposal stage |
| E:normative:consistency | normative | consistency | principled compliance integrity | 0 | NO_ITEMS | Compliance principles are internally consistent |
| E:operative:necessity | operative | necessity | essential execution authority | 0 | NO_ITEMS | Execution authority is clear |
| E:operative:sufficiency | operative | sufficiency | proven operational standing | 0 | NO_ITEMS | Operational standing is demonstrated |
| E:operative:completeness | operative | completeness | total execution accounting | 1 | HAS_ITEMS | No accounting for risk register maintenance burden |
| E:operative:consistency | operative | consistency | principled execution integrity | 0 | NO_ITEMS | Execution is principled |
| E:evaluative:necessity | evaluative | necessity | definitive merit authority | 0 | NO_ITEMS | PM + Proposal Manager provide merit authority |
| E:evaluative:sufficiency | evaluative | sufficiency | warranted merit standing | 0 | NO_ITEMS | Merit standing is warranted by process |
| E:evaluative:completeness | evaluative | completeness | total value jurisdiction | 1 | HAS_ITEMS | No guidance on how register value is communicated to evaluators |
| E:evaluative:consistency | evaluative | consistency | principled merit integrity | 0 | NO_ITEMS | Merit integrity is maintained |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Specification | Specification | Align NBCC citation with risk register content: either add a risk entry addressing building code compliance risk (e.g., RISK-DES-06 for code interpretation uncertainty) or remove NBCC from Standards table if it is not directly relevant to the risk register | Specification Standards table cites NBCC as "Design risk context (code compliance risks)" with ASSUMPTION tag. However, no risk entry in the Datasheet register explicitly addresses building code compliance as a risk. If NBCC is relevant enough to cite as a standard, there should be at least a corresponding risk consideration. | Specification.md; Datasheet.md | Specification: Standards table, row NBCC; Datasheet: entire register scanned | -- | Specification.md | TBD |
| E-002 | E:operative:completeness | VerificationGap | Procedure | Procedure | Add a note on estimated effort/time to maintain the risk register post-award (e.g., monthly update cycle of X hours; who facilitates the update session) to ensure the living document commitment is operationally feasible | Procedure Records section commits to "Update monthly during design and construction" but does not estimate the effort required. For a 26-entry register, monthly updates could be significant. Without effort estimation, the commitment may not be executed consistently. | Procedure.md | Procedure: Records > Post-Award Records | -- | Procedure.md | TBD |
| E-003 | E:evaluative:completeness | MissingSlot | Guidance | Guidance | Add guidance on how the risk register and narrative should be formatted or excerpted for the proposal submission package (e.g., executive summary, visual risk matrix chart, narrative placement within proposal structure) | Guidance Purpose identifies the Evaluation Committee as a primary audience and Procedure Step 6.3 says "Lock final versions for proposal PDF assembly." However, no guidance exists on how the register should be presented to evaluators -- whether as a full appendix, executive summary, or integrated within the proposal narrative. This is a presentation/packaging gap that could affect OBJ-008 scoring. | Guidance.md; Procedure.md | Guidance: Purpose; Procedure: Step 6.3 | -- | Guidance.md | TBD |

---

*End of Semantic Lensing Register for DEL-10-01.*
