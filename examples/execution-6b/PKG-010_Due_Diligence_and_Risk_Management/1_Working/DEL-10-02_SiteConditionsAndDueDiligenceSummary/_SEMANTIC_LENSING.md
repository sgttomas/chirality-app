# Semantic Lensing Register: DEL-10-02 Site Conditions and Due Diligence Summary

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-010_Due_Diligence_and_Risk_Management/1_Working/DEL-10-02_SiteConditionsAndDueDiligenceSummary
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-10-02 identity, scope (SOW-0026, SOW-0027), objective (OBJ-008)
- _STATUS.md -- Current state: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- 7 matrices parsed (A, B, C, F, D, X, E); 92 cells total
- Datasheet.md -- present; read in full
- Specification.md -- present; read in full
- Guidance.md -- present; read in full
- Procedure.md -- present; read in full
- _REFERENCES.md -- present; read in full

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 4
  - Specification: 6
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 3  B: 4  C: 2  F: 3  D: 1  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 1
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0 (3 existing conflicts already captured in Guidance Conflict Table)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Flood fringe regulatory reference gap |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | DEC-013 is well stated across docs |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Wetland setback compliance unclear |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit path is covered via Verification table |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-6 provide clear direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps well-defined |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table addresses all 11 requirements |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No post-submission audit or lessons-learned step |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | OBJ-008 alignment is clearly stated in Guidance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance EX-001 through EX-003 demonstrate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-001 through T-004 cover this |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Step 6 technical review covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add a requirement or standards entry identifying the specific Alberta provincial regulation governing flood fringe development (e.g., Alberta Water Act, municipal land use bylaw flood overlay). Currently "flood fringe" is described but the prescriptive regulatory source is not cited. | The narrative describes flood fringe constraints as factual conditions but does not trace them to a specific regulatory instrument. A prescriptive direction lens reveals that readers cannot determine which regulation governs permitted uses in the fringe. | Specification.md; Guidance.md | Specification: Standards table; Guidance: C-004 | -- | Specification (Standards table) | TBD |
| A-002 | A:normative:judging | WeakStatement | Guidance | Guidance | Clarify C-002 wetland setback guidance: "Provincial regulations typically require a 30-100 m buffer" is too wide a range to support a compliance determination. Add TBD marker for the specific applicable setback once Appendix D is accessed. | The compliance determination lens reveals that the 30-100 m range is too vague to judge whether the civil site layout (DEL-02-02) actually complies. Without a specific value or at minimum a stated assumption, compliance cannot be assessed. | Guidance.md | C-002 (Wetland Assessment -- Setback requirement) | -- | Guidance (narrow range or mark TBD with specific follow-up) | TBD |
| A-003 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Consider adding a post-submission review step or lessons-learned checkpoint after Step 6 to capture whether TBD items were resolved and what assumptions remained open at submission time. | The process audit lens identifies that the procedure ends at technical review sign-off (Step 6) with no mechanism to record which TBDs persisted into the submitted proposal. This gap means post-award teams may not know which assumptions need verification. | Procedure.md | After Step 6 (Technical Lead Review and Sign-Off) | -- | Procedure | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key factual values marked TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Reference study accessibility |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Flood zone mapping source unclear |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Numeric values (20/12/8 acres) are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (DEC-013, flood split, survey timing) are clear |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides rich context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope coverage is well-bounded |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for environmental assessment |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Geotechnical, wetland, environmental understanding is structured |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Author responsibilities table assigns disciplines |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage across all five study domains is addressed |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-doc consistency checks are explicit in Procedure Step 5b |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T-001 through T-004 demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | DEC-013 rationale is well-articulated |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance links all studies to downstream consumers |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning across trade-offs is internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | All six reference studies in the "Reference Studies" table have "specific findings TBD." Identify which TBD items are blocking (required before narrative draft can proceed) vs. which can be populated during Step 2-3 of Procedure. Add a priority/blocking indicator column to the Reference Studies table. | The essential fact lens highlights that the Datasheet records six reference studies all marked TBD for content. While this is correct given that PDFs have not been accessed, there is no signal distinguishing which TBDs block production and which are refinements. | Datasheet.md | Conditions > Reference Studies (Owner-Provided) | -- | Datasheet | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | The "Flood Zone Mapping" entry in the Reference Studies table lists source as "RFP reference (source TBD)." Clarify whether the flood zone map is within Appendix D, Appendix F, municipal mapping, or a separate document. Procedure Step 1.3 asks to locate this but the Datasheet should record the best-known source. | The adequate evidence lens identifies that the flood zone mapping source is uniquely uncertain compared to other reference studies. The Datasheet cannot confirm whether adequate evidence for R-006 is obtainable without knowing where the map resides. | Datasheet.md | Conditions > Reference Studies table -- Flood Zone Mapping row | -- | Datasheet | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add the 2021 geotechnical report date and number of boreholes (when known) to the Reference Studies table. Guidance C-001 identifies "report scope limitations" (borehole count, location, coverage) as a key consideration, but the Datasheet does not have a slot for this metadata. | The comprehensive record lens reveals that while Guidance asks the narrative author to address report scope limitations, the Datasheet has no structured field to capture the report's coverage parameters (date, borehole count, spatial coverage). | Datasheet.md; Guidance.md | Datasheet: Reference Studies table; Guidance: C-001 (Report scope limitations) | -- | Datasheet | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize the environmental assessment naming: Guidance C-003 uses "Desktop Environmental Assessment" and the Datasheet uses "Desktop Environmental Assessment (Ghostpine)." The Conflict Table CONF-10-02-003 already flags the "Ghostpine" ambiguity. Adopt a consistent interim label across all four documents pending resolution. | The coherent message lens identifies that "Ghostpine" appears inconsistently -- sometimes included as a parenthetical, sometimes omitted. This naming inconsistency could propagate into the final narrative. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple locations referencing the environmental assessment | -- | Guidance (vocabulary note) + all docs | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 0 | NO_ITEMS | Regulatory requirements are identified where known |
| C:normative:sufficiency | normative | sufficiency | Warranted Conformance | 1 | HAS_ITEMS | Sufficiency of single geotech report |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 0 | NO_ITEMS | Standards table covers applicable references |
| C:normative:consistency | normative | consistency | Uniform Compliance Standard | 0 | NO_ITEMS | Standards are consistently referenced |
| C:operative:necessity | operative | necessity | Foundational Process Need | 0 | NO_ITEMS | Prerequisites table is thorough |
| C:operative:sufficiency | operative | sufficiency | Competent Practice Basis | 0 | NO_ITEMS | Author responsibilities and review roles are clear |
| C:operative:completeness | operative | completeness | Comprehensive Operational Scope | 0 | NO_ITEMS | Steps 1-6 cover full production workflow |
| C:operative:consistency | operative | consistency | Disciplined Process Alignment | 0 | NO_ITEMS | Steps align with requirement IDs |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth Criterion | 0 | NO_ITEMS | OBJ-008 provides the worth criterion |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Basis | 1 | HAS_ITEMS | ASMP-04 defensibility |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Assessment | 0 | NO_ITEMS | Trade-offs cover all major dimensions |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | R-001 requires summarizing geotech findings but does not specify a verification criterion for whether the 2021 report's spatial coverage is sufficient for the proposed building footprint. Add a verification note that the reviewer should confirm whether borehole locations cover the proposed building area. | The warranted conformance lens asks whether the evidence basis is adequate for the normative claim. R-001 requires summarizing the 2021 report findings but does not ask the reviewer to assess whether the report's coverage (borehole locations vs. building footprint) is sufficient. | Specification.md | Requirements: R-001; Verification: R-001 | -- | Specification | TBD |
| C-002 | C:evaluative:sufficiency | WeakStatement | Datasheet | Guidance | ASMP-04 states "Phase 1 desktop environmental assessment (Ghostpine) found no recognized environmental conditions requiring Phase 2 investigation" and labels this an ASSUMPTION. Guidance T-003 notes this is "typical for undeveloped/agricultural land" but provides no fallback if the assumption is wrong. Add a brief statement of the consequence and escalation path if Phase 1 findings upon access reveal RECs. | The defensible merit basis lens asks whether assumptions are defensible. ASMP-04 is labeled as an assumption but reads as a conclusion. If Phase 1 findings upon actual review reveal RECs, there is no documented escalation path in either the Datasheet assumption log or the Guidance trade-off. | Datasheet.md; Guidance.md | Datasheet: ASSUMPTION Log ASMP-04; Guidance: T-003 | -- | Guidance (add escalation path under T-003) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Threshold | 1 | HAS_ITEMS | Missing explicit acceptance criteria for "adequate" geotech summary |
| F:normative:sufficiency | normative | sufficiency | Substantiated Compliance Basis | 0 | NO_ITEMS | Requirements cite sources |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Standards table covers applicable references |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Discipline | 1 | HAS_ITEMS | Terminology normalization needed |
| F:operative:necessity | operative | necessity | Critical Execution Prerequisite | 0 | NO_ITEMS | Prerequisites table is thorough |
| F:operative:sufficiency | operative | sufficiency | Viable Execution Capacity | 0 | NO_ITEMS | Author responsibilities defined |
| F:operative:completeness | operative | completeness | Total Operational Integration | 0 | NO_ITEMS | Handoff table provides integration |
| F:operative:consistency | operative | consistency | Stable Operational Coherence | 0 | NO_ITEMS | Steps and verification align |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Imperative | 0 | NO_ITEMS | OBJ-008 is the worth imperative |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Value Justification | 0 | NO_ITEMS | Trade-offs provide justification |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Accounting | 1 | HAS_ITEMS | Missing cost implication accounting structure |
| F:evaluative:consistency | evaluative | consistency | Coherent Appraisal Standard | 0 | NO_ITEMS | Appraisal approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | R-010 requires that "each major finding is accompanied by a corresponding design or cost implication statement" but the verification method says "Reviewer assesses" without defining what constitutes a complete set of "major findings." Add a checklist or enumeration of the major findings that must each have an implication (e.g., bearing capacity, water table, wetland setback, flood fringe placement, grading cut/fill). | The mandatory compliance threshold lens reveals that R-010's verification is subjective ("reviewer assesses") without a defined threshold for what counts as complete coverage. A reviewer could pass this requirement while missing a key finding-implication link. | Specification.md | Requirements: R-010; Verification: R-010 | -- | Specification | TBD |
| F-002 | F:normative:consistency | Normalization | Multi | Guidance | The term "geotechnical report" appears in multiple forms: "2021 Geotechnical Investigation Report" (Datasheet formal), "2021 geotechnical report" (Guidance informal), "geotech report" (implied in Procedure shorthand). Procedure Step 5b mentions checking terminology consistency but does not define the canonical term. Add a vocabulary note in Guidance defining the canonical reference name. | The harmonized regulatory discipline lens identifies that the key reference document is named inconsistently. For a proposal document, inconsistent naming of a primary source undermines professional credibility. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple locations | -- | Guidance (vocabulary note) + all docs | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Specification | Specification | R-010 requires design or cost implication statements but there is no requirement specifically addressing the synthesis section ("Design and Cost Implications") as a distinct artifact. The Datasheet Narrative Structure lists this section but no Specification requirement ensures it exists as a standalone synthesis rather than being scattered through section-level comments. Consider adding a requirement for a dedicated synthesis section. | The comprehensive value accounting lens asks whether all value dimensions are captured. The synthesis section is described in the Datasheet narrative structure but has no corresponding requirement ensuring it appears as an integrated whole. | Specification.md; Datasheet.md | Specification: Requirements table (no synthesis-section requirement); Datasheet: Narrative Structure table | -- | Specification | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Direction | 0 | NO_ITEMS | Standards table provides direction |
| D:normative:applying | normative | applying | Resolved Compliance Enactment | 0 | NO_ITEMS | Requirements are enacted through verification |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Verification table supports conformance ruling |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Oversight | 0 | NO_ITEMS | Step 6 review provides oversight mechanism |
| D:operative:guiding | operative | guiding | Resolved Procedural Guidance | 0 | NO_ITEMS | Procedure provides resolved procedural guidance |
| D:operative:applying | operative | applying | Resolved Operational Delivery | 0 | NO_ITEMS | Steps 1-6 resolve delivery sequence |
| D:operative:judging | operative | judging | Resolved Performance Judgment | 1 | HAS_ITEMS | Cross-doc check timing |
| D:operative:reviewing | operative | reviewing | Systematic Process Assurance | 0 | NO_ITEMS | Verification table provides systematic checks |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Direction | 0 | NO_ITEMS | OBJ-008 provides clear value direction |
| D:evaluative:applying | evaluative | applying | Justified Merit Enactment | 0 | NO_ITEMS | Examples EX-001 through EX-003 demonstrate merit application |
| D:evaluative:judging | evaluative | judging | Definitive Value Appraisal | 0 | NO_ITEMS | Trade-offs provide value appraisal framework |
| D:evaluative:reviewing | evaluative | reviewing | Assured Quality Consistency | 0 | NO_ITEMS | Step 6 review covers quality consistency |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:judging | VerificationGap | Procedure | Procedure | Step 5b cross-document consistency checks require DEL-02-02, DEL-02-03, and DEL-10-01 drafts, but Prerequisites only states "Draft required for Step 5 cross-check" without specifying what happens if those drafts are not yet available. Add a fallback action (e.g., defer cross-check, record as open item, schedule follow-up) to ensure performance judgment is not silently skipped when dependencies are unavailable. | The resolved performance judgment lens asks whether the procedure ensures a conclusive performance assessment. If prerequisite deliverable drafts are unavailable, Step 5b cannot be executed, but no fallback is documented. The judgment would be silently incomplete. | Procedure.md | Prerequisites > Related Deliverables table; Steps > Step 5b | -- | Procedure | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Authority | 0 | NO_ITEMS | Guidance provides foundational authority |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Guidance Basis | 0 | NO_ITEMS | Principles P-001 through P-006 are well-substantiated |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Scope | 0 | NO_ITEMS | Considerations C-001 through C-005 cover all study domains |
| X:guiding:consistency | guiding | consistency | Principled Guidance Alignment | 0 | NO_ITEMS | Principles are internally consistent |
| X:applying:necessity | applying | necessity | Essential Enactment Foundation | 1 | HAS_ITEMS | Missing enactment link for ASMP-02 |
| X:applying:sufficiency | applying | sufficiency | Defensible Execution Capacity | 0 | NO_ITEMS | Author responsibilities ensure execution capacity |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Scope | 0 | NO_ITEMS | Steps cover all scope items |
| X:applying:consistency | applying | consistency | Coherent Execution Discipline | 0 | NO_ITEMS | Steps align with requirements consistently |
| X:judging:necessity | judging | necessity | Binding Foundational Verdict | 1 | HAS_ITEMS | R-011 verification gap |
| X:judging:sufficiency | judging | sufficiency | Substantiated Adjudication Basis | 0 | NO_ITEMS | Verification approaches are substantiated |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 0 | NO_ITEMS | All 11 requirements have verification entries |
| X:judging:consistency | judging | consistency | Principled Adjudication Coherence | 0 | NO_ITEMS | Verification methods are coherent with requirement types |
| X:reviewing:necessity | reviewing | necessity | Essential Assurance Verification | 1 | HAS_ITEMS | No formal acceptance gate |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Assurance Basis | 0 | NO_ITEMS | Step 6 review is well-defined |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Scope | 0 | NO_ITEMS | Verification table covers all requirements |
| X:reviewing:consistency | reviewing | consistency | Disciplined Assurance Alignment | 0 | NO_ITEMS | Review process is disciplined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | TBD_Question | Datasheet | Datasheet | ASMP-02 states "Wetland boundary does not preclude the 12-acre buildable area identified in Addendum 03" but there is no verification mechanism in either the Specification or Procedure to confirm this assumption once Appendix D is accessed. Add a verification step or link ASMP-02 to Step 3 (wetland extraction) with an explicit check: "Confirm wetland boundary does not encroach on 12-acre functional site." | The essential enactment foundation lens asks whether each foundational claim has an enactment path. ASMP-02 is a critical site assumption but has no procedure step or verification check that would confirm or invalidate it. It could pass through to the final narrative unverified. | Datasheet.md; Procedure.md | Datasheet: ASSUMPTION Log ASMP-02; Procedure: Step 3 (wetland extraction targets) | -- | Procedure (add ASMP-02 verification to Step 3) | TBD |
| X-002 | X:judging:necessity | VerificationGap | Specification | Specification | R-011 (cross-document consistency with DEL-02-02 and DEL-02-03) has verification method "Cross-document review" with responsible party "Technical Lead" but no specific acceptance criterion defining what constitutes a "contradiction" vs. an acceptable difference. Add acceptance criteria (e.g., building footprint placement, foundation type selection, bearing capacity value must match). | The binding foundational verdict lens asks whether the verification provides a definitive ruling. R-011 verification is described in general terms ("flag any discrepancy") without defining what constitutes a discrepancy requiring resolution vs. an acceptable variation. | Specification.md | Requirements: R-011; Verification: R-011 | -- | Specification | TBD |
| X-003 | X:reviewing:necessity | MissingSlot | Procedure | Specification | There is no formal acceptance gate or sign-off record format defined in the Specification Documentation table. The Procedure references "Technical Lead Sign-Off Record" as "Email or document comment" but neither the Specification nor the Procedure defines what constitutes formal acceptance (e.g., all TBDs acknowledged, all verifications passed, all conflicts either resolved or in Conflict Table). | The essential assurance verification lens identifies that while Step 6 describes a review, there is no defined acceptance gate with pass/fail criteria. A reviewer could sign off without explicitly confirming all verifications passed. | Procedure.md; Specification.md | Procedure: Step 6; Records table; Specification: Documentation table | -- | Specification (add acceptance criteria for sign-off) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Imperative Governance Foundation | 0 | NO_ITEMS | Governance foundation is solid via DEC-013, standards, requirements |
| E:normative:sufficiency | normative | sufficiency | Warranted Governance Capacity | 0 | NO_ITEMS | Governance capacity adequate for proposal-stage deliverable |
| E:normative:completeness | normative | completeness | Exhaustive Governance Breadth | 1 | HAS_ITEMS | Permitting responsibility gap |
| E:normative:consistency | normative | consistency | Principled Governance Stability | 0 | NO_ITEMS | Governance is principled and stable |
| E:operative:necessity | operative | necessity | Core Operational Foundation | 0 | NO_ITEMS | Operational foundation is solid |
| E:operative:sufficiency | operative | sufficiency | Substantiated Operational Viability | 0 | NO_ITEMS | Viability is substantiated by author roles and step sequence |
| E:operative:completeness | operative | completeness | Integral Operational Breadth | 0 | NO_ITEMS | Operational scope covers all required domains |
| E:operative:consistency | operative | consistency | Disciplined Operational Coherence | 0 | NO_ITEMS | Operational coherence maintained |
| E:evaluative:necessity | evaluative | necessity | Foundational Value Assurance | 0 | NO_ITEMS | Value assurance via OBJ-008 linkage |
| E:evaluative:sufficiency | evaluative | sufficiency | Warranted Value Substantiation | 0 | NO_ITEMS | Value substantiation is adequate |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Value Breadth | 1 | HAS_ITEMS | Downstream value chain incomplete |
| E:evaluative:consistency | evaluative | consistency | Principled Value Discipline | 0 | NO_ITEMS | Value discipline is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | RationaleGap | Guidance | Guidance | C-002 mentions "Permitting implications: Provincial environmental approval may be needed if construction activities affect the wetland area" and asks whether this is the Owner's responsibility or the proponent's. This question is raised but never answered or assigned to a resolution path. Add this as a TBD decision item requiring human ruling, or add to the Conflict Table. | The exhaustive governance breadth lens reveals that wetland permitting responsibility is an open governance question that affects both scope and cost. It is mentioned in Guidance but not tracked as an open item requiring resolution. | Guidance.md | C-002 (Wetland Assessment -- Permitting implications) | -- | Guidance (add to Conflict Table or create decision item) | TBD |
| E-002 | E:evaluative:completeness | Normalization | Multi | Guidance | The Guidance Downstream Use table lists DEL-05-02 (Structural Durability) as a consumer: "Durability strategy for foundations and slabs addresses soil corrosivity, frost depth, and water table conditions documented here." However, "soil corrosivity" is not mentioned anywhere in the Datasheet, Specification, or Procedure. If this is a relevant site condition, it should be added to the Datasheet conditions and potentially to an extraction target in Procedure Step 2. If it is not relevant, remove from Guidance. | The comprehensive value breadth lens identifies an asymmetry in downstream value delivery. The Guidance claims DEL-10-02 provides soil corrosivity data to DEL-05-02, but no other document in this deliverable mentions soil corrosivity or includes it as an extraction target. | Guidance.md; Datasheet.md; Procedure.md | Guidance: Downstream Use table (DEL-05-02 entry); Datasheet: Conditions; Procedure: Step 2 extraction targets | -- | Guidance + Datasheet + Procedure (normalize or remove) | TBD |
