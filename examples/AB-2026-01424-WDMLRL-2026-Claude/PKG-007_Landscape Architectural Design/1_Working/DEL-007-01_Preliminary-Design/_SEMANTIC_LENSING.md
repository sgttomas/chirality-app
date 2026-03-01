# Semantic Lensing Register: DEL-007-01 Preliminary Landscape Design

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-007_Landscape Architectural Design/1_Working/DEL-007-01_Preliminary-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-007-01_Preliminary-Design/_CONTEXT.md (Deliverable Identity, Scope of Work Reference, Context Information)
- _STATUS.md — DEL-007-01_Preliminary-Design/_STATUS.md (State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-007-01_Preliminary-Design/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-007-01_Preliminary-Design/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md — DEL-007-01_Preliminary-Design/Specification.md (Scope, Requirements REQ-007-01-001 through REQ-007-01-007, Standards, Verification)
- Guidance.md — DEL-007-01_Preliminary-Design/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-007-01_Preliminary-Design/Procedure.md (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md — DEL-007-01_Preliminary-Design/_REFERENCES.md (Source Documents, Decomposition References)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 25
- By document:
  - Datasheet: 3
  - Specification: 11
  - Guidance: 4
  - Procedure: 5
  - Multi: 2
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Landscape-specific code standards not enumerated |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Topsoil stripping stated as assumption not mandate |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance deferred to IFC stage with no preliminary gate check |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Audit cycle addressed adequately by procedure verification |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-6 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Presentation format left entirely TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Internal review step covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification table in Procedure covers process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit success criteria for value of preliminary design |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance adequately addresses merit |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | County approval gate serves as worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal review in Step 4 covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify which specific Alberta landscape/site codes and municipal bylaws apply to this deliverable. The Standards table lists several as "location TBD." | The prescriptive-direction lens reveals that the normative framework for landscape design rests on assumptions rather than identified applicable codes. Without confirmed standards, prescriptive direction is incomplete. | Specification.md | Standards | -- | PROPOSAL: Landscape Architect to confirm applicable codes with Camrose County at preliminary approval meeting | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-007-01-004 language: clarify whether topsoil stripping is a confirmed requirement or an assumption requiring confirmation, and under what conditions it applies. | Under the mandatory-practice lens, REQ-007-01-004 uses "acknowledge the requirement" but the Datasheet notes it as "assumed required per Decomposition D-010." The normative status of this practice is ambiguous. | Specification.md; Datasheet.md | REQ-007-01-004; Conditions (Topsoil stripping) | -- | PROPOSAL: Specification is authoritative for requirement status | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add a preliminary-stage compliance check for REQ-007-01-006 (code alignment). Current verification defers entirely to IFC stage (PKG-009). | Compliance-determination lens shows that code alignment verification has no gate at the preliminary stage; the only check is at IFC. A preliminary compliance screening would catch conflicts earlier. | Specification.md | Verification (REQ-007-01-006) | -- | PROPOSAL: Specification governs verification approach | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify minimum content requirements for the preliminary design presentation in Step 3 or as a checklist. Current phrasing defers format entirely to Landscape Architect discretion with only an ASSUMPTION about typical elements. | Under the practical-execution lens, the Procedure leaves the deliverable artifact format as fully TBD. A practitioner executing this step has no normative minimum content list, only assumptions from Guidance. | Procedure.md | Step 3 (3.2) | -- | PROPOSAL: Procedure governs execution content | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Guidance | Guidance | Add explicit success criteria or evaluation framework for what constitutes a sufficient preliminary design (beyond County approval/rejection). | Value-orientation lens reveals no articulated criteria for evaluating the quality or sufficiency of the preliminary design beyond the binary County approval gate. Guidance Principles focus on constraints, not positive value targets. | Guidance.md | Principles; entire document scanned | -- | PROPOSAL: Guidance is appropriate for value-orientation content | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Soil/vegetation data gap |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence (RFP, site maps) is acknowledged |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Geotechnical data dependency noted but not tracked as data gap in Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | No conflicting measurements identified |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential coordination signals identified in Procedure |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided in Guidance Considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive account of available information |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of site and project articulated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure prerequisites cover expertise requirements |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Appropriate for preliminary stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | No guidance on when to escalate vs. proceed with assumptions |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided through Guidance Considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add a "Data Gaps / TBD Inputs" section listing essential site-specific data not yet available: soil conditions, vegetation community baseline, microclimate data, and utility routing. | Essential-fact lens reveals that Guidance Considerations mentions missing soil, vegetation, and microclimate data, but neither the Datasheet nor Specification tracks these as formal data gaps. Without a consolidated gap register, essential facts may be overlooked. | Guidance.md; Datasheet.md | Considerations (Site character and context); entire Datasheet scanned | -- | PROPOSAL: Datasheet for data gap tracking | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add geotechnical/survey data dependency status (DEL-008-01, DEL-008-02) as a tracked data input in the Datasheet, not only as a Procedure prerequisite. | Comprehensive-record lens shows geotechnical and survey data dependencies appear in Procedure prerequisites but not in the Datasheet's descriptive record. The Datasheet should comprehensively record all data inputs, including pending ones. | Procedure.md; Datasheet.md | Prerequisites (Geotechnical and survey data); entire Datasheet scanned | -- | PROPOSAL: Datasheet for data input tracking | TBD |
| B-003 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Add guidance on escalation criteria: when should the Landscape Architect proceed with documented assumptions versus when must they halt and seek external input before continuing. | Essential-discernment lens reveals that the documents contain many TBD and ASSUMPTION items but provide no framework for discriminating between assumptions safe to proceed with and those requiring resolution before work continues. | Guidance.md; Procedure.md | entire Guidance scanned; Step 1 (1.4) | -- | PROPOSAL: Guidance for decision-making rationale | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Governing Obligation | 1 | HAS_ITEMS | Obligation hierarchy not explicit |
| C:normative:sufficiency | normative | sufficiency | Warranted Validation | 0 | NO_ITEMS | Validation approach is present in Specification Verification |
| C:normative:completeness | normative | completeness | Comprehensive Regulatory Coverage | 1 | HAS_ITEMS | Regulatory coverage incomplete for landscape-specific codes |
| C:normative:consistency | normative | consistency | Harmonized Conformity | 0 | NO_ITEMS | No conformity inconsistencies detected |
| C:operative:necessity | operative | necessity | Operational Readiness | 0 | NO_ITEMS | Prerequisites adequately address readiness |
| C:operative:sufficiency | operative | sufficiency | Capable Performance | 0 | NO_ITEMS | Steps provide capable performance framework |
| C:operative:completeness | operative | completeness | Thorough Fulfillment | 0 | NO_ITEMS | Procedure steps are thorough for preliminary stage |
| C:operative:consistency | operative | consistency | Methodical Reliability | 0 | NO_ITEMS | Steps are methodical and sequenced |
| C:evaluative:necessity | evaluative | necessity | Foundational Benchmark | 1 | HAS_ITEMS | No benchmark for preliminary design adequacy |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Assessment | 0 | NO_ITEMS | Trade-offs provide defensible assessment basis |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Appraisal | 0 | NO_ITEMS | Value covered through objectives alignment |
| C:evaluative:consistency | evaluative | consistency | Principled Consistency | 0 | NO_ITEMS | Principles are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Specification | Guidance | Add rationale explaining the priority ordering among requirements (REQ-007-01-001 through REQ-007-01-007). Which obligations take precedence if they conflict (e.g., drainage vs. driving surface design)? | Governing-Obligation lens reveals seven requirements with no stated priority or hierarchy. If requirements conflict during design, the practitioner has no guidance on which obligation governs. | Specification.md | Requirements (REQ-007-01-001 through REQ-007-01-007) | -- | PROPOSAL: Guidance for rationale; Specification for any normative priority statement | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for Alberta Land Stewardship Act and AALA practice standards, or confirm these are not applicable. Currently listed as assumptions with "location TBD." | Comprehensive-Regulatory-Coverage lens shows the Standards table includes assumed-applicable standards (Alberta Land Stewardship Act, AALA standards) with no verification path. Regulatory completeness requires confirming or excluding these. | Specification.md | Standards | -- | PROPOSAL: Specification for verification of applicable standards | TBD |
| C-003 | C:evaluative:necessity | MissingSlot | Specification | Specification | Add acceptance criteria defining what constitutes a sufficient preliminary design (e.g., minimum content elements, level of detail, review criteria) beyond County approval. | Foundational-Benchmark lens reveals no measurable benchmark for preliminary design adequacy. The only gate is County approval, which is an external judgment with no internal criteria to guide production quality. | Specification.md; Guidance.md | Verification (REQ-007-01-001); Principles (Approval-gate first) | -- | PROPOSAL: Specification for acceptance criteria | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Verified Imperative | 1 | HAS_ITEMS | Source verification incomplete for assumed standards |
| F:normative:sufficiency | normative | sufficiency | Justified Adherence | 0 | NO_ITEMS | Adherence justification present through source citations |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Regime | 0 | NO_ITEMS | Compliance regime appropriate for preliminary stage |
| F:normative:consistency | normative | consistency | Stable Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are consistent |
| F:operative:necessity | operative | necessity | Execution Mandate | 1 | HAS_ITEMS | County PM submission channel TBD |
| F:operative:sufficiency | operative | sufficiency | Proficient Capability | 0 | NO_ITEMS | Prerequisites identify needed capabilities |
| F:operative:completeness | operative | completeness | Exhaustive Delivery Assurance | 1 | HAS_ITEMS | No delivery checklist for completeness |
| F:operative:consistency | operative | consistency | Rigorous Process Stability | 0 | NO_ITEMS | Process steps are stable and sequenced |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Value Clarity | 0 | NO_ITEMS | Purpose section provides value clarity |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth | 0 | NO_ITEMS | Worth substantiated through objectives alignment |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Authority | 0 | NO_ITEMS | Appropriate for preliminary stage |
| F:evaluative:consistency | evaluative | consistency | Principled Value Precision | 1 | HAS_ITEMS | Terminology inconsistency in scope references |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification approach for the assumed standards (Alberta Land Stewardship Act / MGA, AALA practice standards). Either confirm applicability and add verification, or explicitly exclude with rationale. | Verified-Imperative lens reveals that standards listed as ASSUMPTION in the Standards table have no verification path. Imperatives cannot be verified if their applicability is unconfirmed. | Specification.md | Standards | -- | PROPOSAL: Specification for standards verification | TBD |
| F-002 | F:operative:necessity | TBD_Question | Procedure | Procedure | Record TBD: Confirm County PM identity and submission channel/format requirements for DEL-007-01 delivery. | Execution-Mandate lens reveals that the submission process depends on a County PM contact and submission channel that are both identified as TBD. The execution mandate cannot be fulfilled without this information. | Procedure.md | Step 5 (5.1); Prerequisites (County project manager identified) | -- | PROPOSAL: Project team to confirm at contract award | TBD |
| F-003 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add a delivery checklist or completeness gate-check before submission (Step 5), listing minimum artifacts and content elements that must be present. | Exhaustive-Delivery-Assurance lens reveals no checklist or enumerated completeness criteria before submission. The internal review (Step 4) checks for consistency but not for artifact completeness. | Procedure.md | Step 4; Step 5 | -- | PROPOSAL: Procedure for completeness check | TBD |
| F-004 | F:evaluative:consistency | Normalization | Multi | Guidance | Normalize the term for the landscape scope boundary. Documents variously refer to "proposed lot," "expansion area," "expansion footprint," and "site area" without a defined canonical term. | Principled-Value-Precision lens reveals inconsistent terminology for the geographic scope of work across documents, which could lead to drift in interpreting what area the design covers. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Site Area; Specification: In Scope; Guidance: Considerations (Planting and restoration intent); Procedure: Step 3 | -- | PROPOSAL: Guidance to define canonical term; all docs to adopt | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Directive | 0 | NO_ITEMS | Binding directives (County approval gate) are clear |
| D:normative:applying | normative | applying | Compulsory Conformance | 0 | NO_ITEMS | Conformance requirements stated |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 1 | HAS_ITEMS | No mechanism for preliminary compliance ruling |
| D:normative:reviewing | normative | reviewing | Concluded Compliance Audit | 0 | NO_ITEMS | Audit concludes at County approval |
| D:operative:guiding | operative | guiding | Resolved Process Direction | 0 | NO_ITEMS | Process direction is resolved in Procedure |
| D:operative:applying | operative | applying | Demonstrated Delivery | 1 | HAS_ITEMS | Delivery demonstration criteria unclear |
| D:operative:judging | operative | judging | Settled Performance Verdict | 0 | NO_ITEMS | County approval serves as verdict |
| D:operative:reviewing | operative | reviewing | Confirmed Process Integrity | 0 | NO_ITEMS | Internal review confirms process integrity |
| D:evaluative:guiding | evaluative | guiding | Settled Value Direction | 0 | NO_ITEMS | Value direction established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Grounded Value Realization | 0 | NO_ITEMS | Value realization through objectives alignment |
| D:evaluative:judging | evaluative | judging | Definitive Merit Judgment | 0 | NO_ITEMS | County approval provides merit judgment |
| D:evaluative:reviewing | evaluative | reviewing | Principled Quality Review | 1 | HAS_ITEMS | No quality criteria for review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add a preliminary-stage compliance determination mechanism: who confirms that the preliminary design does not contravene Alberta codes before County submission? Currently deferred to IFC stage. | Definitive-Compliance-Ruling lens reveals that the compliance ruling for REQ-007-01-006 is entirely deferred to the IFC stage (PKG-009). There is no provision for even a preliminary compliance screening before the design is submitted to County. | Specification.md | Verification (REQ-007-01-006) | -- | PROPOSAL: Specification for preliminary compliance check | TBD |
| D-002 | D:operative:applying | WeakStatement | Specification | Specification | Clarify what artifacts constitute "delivery" for REQ-007-01-001. The Documentation table lists presentation format as TBD. Define minimum deliverable content to demonstrate delivery. | Demonstrated-Delivery lens reveals that the concept of delivery is ambiguous: the Specification Documentation table says format is TBD and at Landscape Architect's discretion. Without defining minimum content, demonstrated delivery cannot be objectively assessed. | Specification.md | Documentation; REQ-007-01-001 | -- | PROPOSAL: Specification for delivery content definition | TBD |
| D-003 | D:evaluative:reviewing | RationaleGap | Guidance | Guidance | Add quality review criteria or a rubric for evaluating the preliminary design during internal review (Step 4). Current guidance focuses on constraint compliance, not quality assessment. | Principled-Quality-Review lens reveals that internal review (Step 4) focuses on checking requirement consistency and scope compliance but has no quality criteria. There is no framework for the team to assess whether the design is good, only whether it is rule-compliant. | Guidance.md; Procedure.md | entire Guidance scanned; Step 4 | -- | PROPOSAL: Guidance for quality review framework | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Advisory | 0 | NO_ITEMS | Foundational advisory provided through Guidance Principles |
| X:guiding:sufficiency | guiding | sufficiency | Competent Stewardship | 0 | NO_ITEMS | Stewardship roles identified |
| X:guiding:completeness | guiding | completeness | Holistic Directive Mastery | 0 | NO_ITEMS | Directive coverage appropriate for preliminary stage |
| X:guiding:consistency | guiding | consistency | Harmonized Orientation | 1 | HAS_ITEMS | Scope-extent terminology inconsistent |
| X:applying:necessity | applying | necessity | Validated Competence | 1 | HAS_ITEMS | No validation mechanism for Landscape Architect competence claims |
| X:applying:sufficiency | applying | sufficiency | Evidenced Proficiency | 0 | NO_ITEMS | Proficiency expectations set in prerequisites |
| X:applying:completeness | applying | completeness | Exhaustive Implementation | 0 | NO_ITEMS | Appropriate for preliminary scope |
| X:applying:consistency | applying | consistency | Reliable Enactment | 0 | NO_ITEMS | Procedure provides reliable enactment path |
| X:judging:necessity | judging | necessity | Decisive Adjudication | 1 | HAS_ITEMS | Scope-extent conflict lacks adjudication mechanism |
| X:judging:sufficiency | judging | sufficiency | Substantiated Ruling | 0 | NO_ITEMS | Rulings substantiated through source citations |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication | 0 | NO_ITEMS | Adjudication scope appropriate |
| X:judging:consistency | judging | consistency | Coherent Ruling Standard | 0 | NO_ITEMS | Ruling standards are coherent |
| X:reviewing:necessity | reviewing | necessity | Conclusive Inspection | 0 | NO_ITEMS | Procedure Verification provides inspection framework |
| X:reviewing:sufficiency | reviewing | sufficiency | Proficient Examination | 0 | NO_ITEMS | Examination steps are adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Scrutiny | 1 | HAS_ITEMS | Verification lacks cross-deliverable completeness check |
| X:reviewing:consistency | reviewing | consistency | Standardized Assurance | 0 | NO_ITEMS | Assurance approach is standardized across checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Multi | Guidance | Establish a canonical geographic scope term (e.g., "expansion area") and define it once in Guidance or Datasheet, then use consistently across all documents. See also F-004. | Harmonized-Orientation lens confirms the terminology inconsistency identified under F-004. The terms "proposed lot" (R-01 SOW-0076), "expansion area" (Datasheet, Guidance), "expansion footprint" (Guidance), and "site area" (Datasheet) are used interchangeably without a defined canonical term. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Site Area, Conditions; Specification: In Scope; Guidance: Considerations; Procedure: Step 3 | -- | PROPOSAL: Guidance to define; all docs to adopt | TBD |
| X-002 | X:applying:necessity | WeakStatement | Specification | Specification | Clarify the Landscape Architect's professional obligation within REQ-007-01-006 at the preliminary stage. Current phrasing ("to the extent it governs site conditions") is ambiguous about the scope of professional responsibility. | Validated-Competence lens reveals that REQ-007-01-006 uses qualifying language ("to the extent it governs site conditions") that creates ambiguity about the boundary of the Landscape Architect's code-compliance responsibility at the preliminary stage. | Specification.md | REQ-007-01-006 | -- | PROPOSAL: Specification for requirement clarity | TBD |
| X-003 | X:judging:necessity | TBD_Question | Guidance | Guidance | Record TBD: Determine the mechanism and timeline for resolving CONF-007-01-001 (scope extent of landscape treatment). Who decides, and by when must this be resolved? | Decisive-Adjudication lens reveals that CONF-007-01-001 identifies the scope-extent ambiguity but provides no adjudication mechanism, timeline, or escalation path for resolution. The conflict could persist unresolved through the preliminary stage. | Guidance.md | Conflict Table (CONF-007-01-001) | -- | PROPOSAL: Human ruling required; suggest resolution at County preliminary approval meeting | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Procedure | Procedure | Add a verification check confirming alignment between DEL-007-01 and peer preliminary deliverables (DEL-001-01, DEL-005-01) at interface points before County submission. | Comprehensive-Scrutiny lens reveals that Procedure Step 4.3 mentions confirming consistency with other preliminary deliverables but no corresponding entry exists in the Verification table. This cross-deliverable check has no formal verification mechanism. | Procedure.md | Step 4 (4.3); Verification | -- | PROPOSAL: Procedure for verification table update | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Factual Basis | 0 | NO_ITEMS | Factual basis adequately cited to RFP and decomposition |
| E:guiding:information | guiding | information | Coherent Strategic Briefing | 0 | NO_ITEMS | Guidance provides coherent strategic briefing |
| E:guiding:knowledge | guiding | knowledge | Mastered Leadership Insight | 0 | NO_ITEMS | Leadership insight appropriate for preliminary stage |
| E:guiding:wisdom | guiding | wisdom | Visionary Prudent Leadership | 0 | NO_ITEMS | Prudent leadership reflected in principles and trade-offs |
| E:applying:data | applying | data | Evidenced Execution Record | 1 | HAS_ITEMS | Records section missing record of TBD/assumption disposition |
| E:applying:information | applying | information | Transparent Performance Report | 0 | NO_ITEMS | Performance reporting addressed through records |
| E:applying:knowledge | applying | knowledge | Confirmed Implementation Craft | 0 | NO_ITEMS | Implementation approach described in Procedure |
| E:applying:wisdom | applying | wisdom | Seasoned Applied Judgment | 0 | NO_ITEMS | Applied judgment reflected in trade-offs |
| E:judging:data | judging | data | Binding Evidentiary Record | 1 | HAS_ITEMS | No requirement for County approval to be in specific evidentiary format |
| E:judging:information | judging | information | Coherent Verdict Account | 0 | NO_ITEMS | County approval record covers verdict |
| E:judging:knowledge | judging | knowledge | Mastered Judicial Authority | 0 | NO_ITEMS | Judicial authority (County) identified |
| E:judging:wisdom | judging | wisdom | Principled Judicial Foresight | 0 | NO_ITEMS | Foresight on downstream impacts addressed |
| E:reviewing:data | reviewing | data | Verified Audit Repository | 1 | HAS_ITEMS | No central register for TBD items and assumptions |
| E:reviewing:information | reviewing | information | Transparent Audit Account | 0 | NO_ITEMS | Audit transparency adequate through procedure checks |
| E:reviewing:knowledge | reviewing | knowledge | Mastered Inspection Craft | 0 | NO_ITEMS | Inspection approach adequate for preliminary stage |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight reflected in downstream dependency awareness |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | MissingSlot | Procedure | Procedure | Add a "TBD/Assumption Disposition Record" to the Records section tracking the status and resolution of all TBD items and ASSUMPTION flags across the four documents. | Evidenced-Execution-Record lens reveals numerous TBD and ASSUMPTION items scattered across all four documents but no consolidated record tracking their disposition. Without this, the execution record is incomplete. | Procedure.md | Records | -- | PROPOSAL: Procedure for records tracking | TBD |
| E-002 | E:judging:data | WeakStatement | Specification | Specification | Strengthen the County approval verification (REQ-007-01-001) by specifying the required form of approval evidence (e.g., signed letter, email confirmation, meeting minutes) rather than "written or documented approval." | Binding-Evidentiary-Record lens reveals that the verification for REQ-007-01-001 accepts "written or documented" approval without specifying what constitutes adequate evidence. This vagueness could lead to disputes about whether approval was actually obtained. | Specification.md; Procedure.md | Verification (REQ-007-01-001); Step 6 (6.1) | -- | PROPOSAL: Specification for evidentiary standard | TBD |
| E-003 | E:reviewing:data | MissingSlot | Datasheet | Datasheet | Add a consolidated TBD/Assumption register as an appendix or section in the Datasheet, collecting all unresolved items from the four documents with their source, status, and resolution target. | Verified-Audit-Repository lens reveals that TBD items and ASSUMPTION flags appear across Datasheet (topsoil stripping), Specification (standards applicability), Guidance (scope extent, utility routing), and Procedure (County PM, geotechnical data) with no central register. An audit repository requires a single point of reference for unresolved items. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire documents scanned | -- | PROPOSAL: Datasheet for consolidated tracking | TBD |
