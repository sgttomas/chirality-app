# Semantic Lensing Register: DEL-018-02 Site Grading & Landscaping

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-018-02_Grading-Landscape/_CONTEXT.md §Deliverable Identity, §Context Summary
- _STATUS.md — DEL-018-02_Grading-Landscape/_STATUS.md §Status Record (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-018-02_Grading-Landscape/_SEMANTIC.md §Matrix A through §Matrix E (all matrices parsed)
- Datasheet.md — DEL-018-02_Grading-Landscape/Datasheet.md §Identification, §Attributes, §Conditions, §Construction, §References
- Specification.md — DEL-018-02_Grading-Landscape/Specification.md §Scope, §Requirements, §Standards, §Verification, §Documentation
- Guidance.md — DEL-018-02_Grading-Landscape/Guidance.md §Purpose, §Principles, §Considerations, §Trade-offs, §Conflict Table
- Procedure.md — DEL-018-02_Grading-Landscape/Procedure.md §Prerequisites, §Steps, §Verification, §Records
- _REFERENCES.md — DEL-018-02_Grading-Landscape/_REFERENCES.md §Reference Map, §Reference Detail, §Cross-References

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 3
  - Specification: 9
  - Guidance: 4
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 2  C: 3  F: 3  D: 2  X: 5  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Compaction standard TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Fine grading tolerances not specified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | REQ-03 verification method undefined |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | County inspection coordination adequately covered |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Rough/fine grading scope boundary with County bulk earthwork unclear |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table covers performance assessment adequately |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section covers process audit adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance §Purpose addresses value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section covers merit application adequately |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guarantee period and downstream dependencies provide worth context |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Compaction testing and inspection provide quality appraisal framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-06 by specifying the compaction standard or explicitly requiring the civil engineer to define it as a prerequisite to testing, rather than deferring with "TBD pending civil specification" | REQ-06 states compaction "to a standard appropriate for the intended use" with standard TBD. Under prescriptive direction, this is too vague to enforce — no pass/fail criterion exists. | Specification.md | §Requirements REQ-06 | — | PROPOSAL: Require civil specification DEL-005-07 to issue compaction acceptance criteria before testing commences | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add fine grading tolerance requirements (e.g., elevation tolerance in mm/ft from design grade) or explicitly require these from the civil specification as a prerequisite | Mandatory practice requires quantified acceptance criteria. Fine grading tolerances are mentioned as TBD in Procedure B-2 but never appear in the Specification as a requirement. | Specification.md | §Requirements (absent — would follow REQ-04) | — | PROPOSAL: Civil specification DEL-005-07 must define tolerances; Specification should reference them as binding | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Define verification method for REQ-03 (neighboring property drainage protection) — currently states "TBD — method to be defined in civil specification DEL-005-07" | Compliance determination requires a defined method. REQ-03 has no actionable verification method — only a TBD reference to a future civil specification. | Specification.md | §Requirements REQ-03 Verification | — | PROPOSAL: Require pre- and post-grading drainage assessment from civil engineer | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Clarify in Step B-1 the handoff criteria between County bulk cut/fill and Contractor fine grading — define what "confirm the extent of County-performed bulk earthwork" means operationally (survey check? written sign-off?) | Practical execution requires clear scope boundaries. The Procedure references County bulk earthwork but the confirmation method is unspecified, risking scope disputes during execution. | Procedure.md | §Steps Phase B, Step B-1 | — | PROPOSAL: Require documented sign-off from County confirming bulk earthwork complete to specified tolerances before Contractor fine grading begins | TBD |

---

## Matrix B — Conceptualization (4x4) — Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Specific grading elevations are TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations are adequate across documents |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Landscape scope data incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references are consistent where specified |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Critical path signals adequately documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for current design stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive for available information |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Construction knowledge base is adequate |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implied through civil/landscape engineer references |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No knowledge gaps beyond design-dependent TBDs |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs and principles provide discernment guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance adequate in Guidance document |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided via dependencies and context |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across Guidance principles |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record essential grading elevation data (design elevations, slope percentages, drainage invert elevations) once civil grading plan DEL-005-02 is issued — currently all TBD | Essential facts for grading execution (elevations, slopes) are entirely absent because the civil design is not yet issued. The Datasheet correctly marks these TBD but they are essential for execution. | Datasheet.md | §Attributes (Specific Grading Elevations, Grading Slopes) | — | PROPOSAL: Civil engineer (PKG-005) to provide via DEL-005-02 | TBD |
| B-002 | B:data:completeness | TBD_Question | Datasheet | Datasheet | Record landscape scope data (species, areas, quantities, materials) once landscape plans DEL-007-02 and DEL-007-03 are issued — currently marked TBD | Comprehensive record of landscape scope cannot be established until landscape design is complete. Datasheet correctly marks this TBD but the data gap blocks landscape execution planning. | Datasheet.md | §Attributes (Landscape Scope) | — | PROPOSAL: Landscape architect (PKG-007) to provide via DEL-007-02/03 | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Foundation | 1 | HAS_ITEMS | Safety code applicability unconfirmed |
| C:normative:sufficiency | normative | sufficiency | Mandated Acceptance Threshold | 1 | HAS_ITEMS | Compaction acceptance threshold undefined |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Environmental regulatory requirements unaddressed |
| C:normative:consistency | normative | consistency | Uniform Compliance Standard | 0 | NO_ITEMS | Compliance standards consistently referenced where known |
| C:operative:necessity | operative | necessity | Critical Execution Baseline | 0 | NO_ITEMS | Execution baseline adequately established in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Competence | 0 | NO_ITEMS | Competence requirements implied through professional qualifications |
| C:operative:completeness | operative | completeness | Comprehensive Process Record | 0 | NO_ITEMS | Records section covers required documentation |
| C:operative:consistency | operative | consistency | Repeatable Process Discipline | 0 | NO_ITEMS | Process steps are sequenced and repeatable |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | Critical path status and downstream enabling provide worth basis |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Threshold | 0 | NO_ITEMS | Merit is justified through dependency chain |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Assessment | 0 | NO_ITEMS | Value assessment covered by Guidance §Purpose |
| C:evaluative:consistency | evaluative | consistency | Principled Value Calibration | 0 | NO_ITEMS | Value principles consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Confirm applicability of Alberta Safety Codes Act — currently listed as "ASSUMPTION: likely applicable (location TBD in accessible sources)". Either confirm with citation or explicitly mark as a required determination | Compulsory compliance foundation requires confirmed regulatory applicability. The Safety Codes Act is listed as an assumption rather than a confirmed applicable standard. | Specification.md | §Standards (Alberta Safety Codes Act row) | — | PROPOSAL: Confirm with project legal/regulatory review | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Define compaction acceptance threshold (e.g., minimum Proctor density percentage) or explicitly require it from DEL-005-07 as a gating prerequisite for compaction testing | Mandated acceptance threshold requires a quantified pass/fail criterion. REQ-06 verification states "standard TBD" with no threshold defined. Compaction testing cannot produce a pass/fail result without this. | Specification.md | §Requirements REQ-06; §Verification REQ-06 row | — | PROPOSAL: Civil specification DEL-005-07 must define; add explicit prerequisite in Specification | TBD |
| C-003 | C:normative:completeness | MissingSlot | Specification | Guidance | Add consideration of environmental regulatory requirements applicable to grading at an active landfill site (e.g., Alberta EPEA, landfill operating approval conditions that may restrict earthwork) | Exhaustive regulatory scope should include environmental regulations. The site is an active landfill (Datasheet §Conditions), but no environmental regulatory requirements are identified in the Standards table. Landfill sites in Alberta typically operate under EPEA approvals that may condition earthwork activities. | Specification.md; Datasheet.md | Specification §Standards (absent); Datasheet §Conditions (Site Context) | — | PROPOSAL: Confirm with County whether landfill operating approval imposes conditions on earthwork | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Strict Conformance Imperative | 0 | NO_ITEMS | Conformance imperatives clearly stated for IFC plan compliance |
| F:normative:sufficiency | normative | sufficiency | Proven Regulatory Satisfaction | 1 | HAS_ITEMS | No mechanism to prove drainage requirement satisfaction |
| F:normative:completeness | normative | completeness | Total Regulatory Command | 0 | NO_ITEMS | Regulatory scope is complete for known requirements |
| F:normative:consistency | normative | consistency | Coherent Obligation Integrity | 1 | HAS_ITEMS | Scope boundary terminology inconsistency |
| F:operative:necessity | operative | necessity | Essential Capability Requirement | 1 | HAS_ITEMS | Equipment capability requirements absent |
| F:operative:sufficiency | operative | sufficiency | Verified Method Adequacy | 0 | NO_ITEMS | Methods adequately described for current stage |
| F:operative:completeness | operative | completeness | Total Performance Coverage | 0 | NO_ITEMS | Performance coverage adequate across procedure phases |
| F:operative:consistency | operative | consistency | Reliable Performance Standard | 0 | NO_ITEMS | Performance expectations consistent |
| F:evaluative:necessity | evaluative | necessity | Core Value Imperative | 0 | NO_ITEMS | Core values addressed through principles |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Adequacy | 0 | NO_ITEMS | Worth justification adequate |
| F:evaluative:completeness | evaluative | completeness | Complete Worth Accounting | 0 | NO_ITEMS | Worth accounting complete for project context |
| F:evaluative:consistency | evaluative | consistency | Coherent Worth Alignment | 0 | NO_ITEMS | Worth alignment consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Define quantitative drainage verification method for REQ-02 — "visual inspection during and after precipitation event" is weather-dependent and non-repeatable; add an engineered verification method (e.g., survey-confirmed slope percentages) | Proven regulatory satisfaction requires a repeatable, objective verification method. REQ-02 verification relies on visual observation during a precipitation event, which is not reliably schedulable and produces subjective results. | Specification.md | §Requirements REQ-02 Verification; §Verification REQ-02 row | — | PROPOSAL: Civil engineer to define engineered drainage verification criteria (e.g., minimum slope percentages confirmed by survey) | TBD |
| F-002 | F:normative:consistency | Normalization | Multi | Guidance | Normalize scope boundary terminology: "grade and landscape the proposed lot" (SOW-0076/Specification) vs. "proposed lot expansion area" (Datasheet/Procedure) vs. "expansion area" (Procedure) — these may refer to the same area but the terms are not explicitly equated | Coherent obligation integrity requires consistent terminology for the work area. Three different terms are used across documents for what appears to be the same physical area, risking scope interpretation disputes. | Specification.md; Datasheet.md; Procedure.md | Specification §Scope In Scope; Datasheet §Attributes (Grading Area); Procedure §Steps B-1 | — | PROPOSAL: Define canonical term in Guidance or Datasheet and use consistently | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add equipment capability requirements or constraints for grading execution (e.g., equipment weight limits given subgrade conditions, equipment access constraints at active landfill site) | Essential capability requirement should address equipment needed or constrained for grading at an active landfill site. No equipment requirements or constraints appear in any document despite the site being an active landfill with access considerations. | Procedure.md | §Steps Phase A (absent) | — | PROPOSAL: Address in pre-construction meeting agenda (Step A-1) or as a Procedure prerequisite | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Binding Directive | 0 | NO_ITEMS | Binding directives adequately resolved through IFC plan references |
| D:normative:applying | normative | applying | Closed Mandate Implementation | 0 | NO_ITEMS | Implementation mandates adequately closed through requirements |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | Landscape conformance ruling authority unclear |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Examination | 0 | NO_ITEMS | Compliance examination adequately resolved through inspection protocol |
| D:operative:guiding | operative | guiding | Resolved Method Direction | 0 | NO_ITEMS | Method direction adequate in Procedure |
| D:operative:applying | operative | applying | Verified Task Accomplishment | 1 | HAS_ITEMS | Task completion criteria for landscaping undefined |
| D:operative:judging | operative | judging | Comprehensive Capability Verdict | 0 | NO_ITEMS | Capability verdict framework adequate through verification table |
| D:operative:reviewing | operative | reviewing | Confirmed Process Stability | 0 | NO_ITEMS | Process stability confirmed through records requirements |
| D:evaluative:guiding | evaluative | guiding | Resolved Principled Guidance | 0 | NO_ITEMS | Principles adequately resolve guidance direction |
| D:evaluative:applying | evaluative | applying | Justified Value Enactment | 0 | NO_ITEMS | Value enactment justified through dependency chain rationale |
| D:evaluative:judging | evaluative | judging | Definitive Value Reckoning | 0 | NO_ITEMS | Value reckoning addressed through quality framework |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Integrity | 0 | NO_ITEMS | Quality integrity resolved through inspection and records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Clarify who has authority to issue definitive conformance ruling for landscape installation — REQ-05 verification states "Landscape architect or Owner representative site review (TBD)" leaving the ruling authority ambiguous | Definitive conformance ruling requires an identified authority. REQ-05 verification lists two possible authorities ("or") without resolving which is authoritative, and adds "(TBD)" indicating this is unresolved. | Specification.md | §Requirements REQ-05 Verification; §Verification REQ-05 row | — | PROPOSAL: Confirm with County whether Landscape Architect or Owner representative (or both) must sign off on landscape conformance | TBD |
| D-002 | D:operative:applying | MissingSlot | Specification | Specification | Define landscape completion criteria — what constitutes "complete" for landscaping work (e.g., planting survival period, establishment criteria, seasonal deferral provisions) | Verified task accomplishment for landscaping requires defined completion criteria. No completion criteria exist for landscape work beyond conformance to IFC plans. Given Alberta climate and the December 2026 deadline, planting establishment criteria and seasonal deferral provisions are needed. | Specification.md; Guidance.md | Specification §Requirements REQ-05; Guidance §Trade-offs T-03 | — | PROPOSAL: Landscape specification DEL-007-04 should define; Specification should reference as binding | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Authority | 0 | NO_ITEMS | Directive authority adequately founded in RFP and IFC plan references |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Steering Competence | 0 | NO_ITEMS | Steering competence substantiated through professional qualifications |
| X:guiding:completeness | guiding | completeness | Complete Directive Command | 1 | HAS_ITEMS | Erosion control directive absent |
| X:guiding:consistency | guiding | consistency | Coherent Directive Standard | 0 | NO_ITEMS | Directive standards coherent across documents |
| X:applying:necessity | applying | necessity | Critical Execution Requirement | 1 | HAS_ITEMS | Stormwater management during construction not addressed |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Delivery Competence | 0 | NO_ITEMS | Delivery competence adequately demonstrated through procedure |
| X:applying:completeness | applying | completeness | Complete Implementation Record | 1 | HAS_ITEMS | Photographic documentation requirements incomplete |
| X:applying:consistency | applying | consistency | Measured Delivery Coherence | 0 | NO_ITEMS | Delivery measurements coherent where specified |
| X:judging:necessity | judging | necessity | Essential Judgment Foundation | 1 | HAS_ITEMS | Hold/witness point requirements absent |
| X:judging:sufficiency | judging | sufficiency | Evidenced Assessment Adequacy | 0 | NO_ITEMS | Assessment evidence requirements adequate for known items |
| X:judging:completeness | judging | completeness | Thorough Judgment Catalogue | 0 | NO_ITEMS | Judgment catalogue is thorough for current stage |
| X:judging:consistency | judging | consistency | Calibrated Verdict Coherence | 0 | NO_ITEMS | Verdict criteria consistent where defined |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Guarantee period inspection/deficiency process undefined |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Integrity Review | 0 | NO_ITEMS | Integrity review substantiated through compaction testing and inspections |
| X:reviewing:completeness | reviewing | completeness | Complete Assurance Catalogue | 0 | NO_ITEMS | Assurance catalogue complete for current scope |
| X:reviewing:consistency | reviewing | consistency | Standardized Assurance Coherence | 0 | NO_ITEMS | Assurance standards coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add guidance on interim erosion and sediment control during grading — the site will be exposed between grading completion and surface construction; no erosion control directive exists for this interim period | Complete directive command should address erosion control. Guidance T-03 mentions erosion control only in the context of late-season landscaping, but the interim period between grading completion and surface construction (DEL-018-03/04) also requires erosion control. No directive exists for this exposure window. | Guidance.md | §Trade-offs T-03 (partial mention only); §Considerations (absent) | — | PROPOSAL: Add Consideration C-07 addressing interim erosion and sediment control requirements | TBD |
| X-002 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add step or consideration for stormwater management during active grading operations — exposed graded surfaces at an active landfill site may require temporary drainage control to prevent sediment-laden runoff | Critical execution requirement should include stormwater management during construction. No procedure step addresses temporary stormwater or sediment control during the grading phase despite the active landfill context and positive drainage requirements. | Procedure.md | §Steps Phase B (absent) | — | PROPOSAL: Add temporary stormwater control step between B-3 and B-4, or address in pre-construction meeting agenda A-1 | TBD |
| X-003 | X:applying:completeness | RationaleGap | Procedure | Procedure | Add requirement for photographic documentation of pre-grading conditions, in-progress grading, and completed grading — Procedure mentions "photographic and written record" only for pre-grading surface condition but not for completion | Complete implementation record should include photographic evidence throughout. Procedure §Records lists "Pre-grading surface condition documentation" with photos, but no photographic record requirement exists for completed grading or in-progress conditions. | Procedure.md | §Records (Pre-grading surface condition documentation) | — | PROPOSAL: Extend photographic documentation requirement to all phases | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Define mandatory hold points or witness points for grading inspections — the Specification requires County representative presence at "all inspections" (REQ-08) but does not define which inspection stages are mandatory hold points vs. witness points | Essential judgment foundation requires defined hold/witness points. REQ-08 mandates County representative presence at all inspections but does not distinguish mandatory hold points (work stops until inspection occurs) from witness points (notification given; work may proceed if inspector does not attend). | Specification.md | §Requirements REQ-08; §Verification REQ-08 row | — | PROPOSAL: Define hold points (e.g., pre-compaction grade check, final grade acceptance) vs. witness points in Specification or Procedure | TBD |
| X-005 | X:reviewing:necessity | RationaleGap | Guidance | Guidance | Add guidance on guarantee period obligations — Datasheet identifies a 2-year guarantee period but no document explains what deficiency inspection, maintenance, or correction obligations apply during this period for grading and landscaping work | Essential audit foundation should address post-completion review obligations. The 2-year guarantee period (Datasheet §Conditions) creates ongoing obligations but no document explains the review/correction process during this period. This is particularly relevant for landscaping (plant survival) and grading (settlement). | Datasheet.md; Guidance.md | Datasheet §Conditions (Guarantee Period); Guidance (absent) | — | PROPOSAL: Add Guidance consideration addressing guarantee period inspection and deficiency correction process; reference CCDC 14-2013 provisions | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Evidence | 0 | NO_ITEMS | Guidance evidence is authoritative with RFP and decomposition citations |
| E:guiding:information | guiding | information | Contextualized Directive Clarity | 0 | NO_ITEMS | Directive clarity is contextualized adequately |
| E:guiding:knowledge | guiding | knowledge | Integrated Steering Mastery | 0 | NO_ITEMS | Steering mastery integrated across Guidance principles and considerations |
| E:guiding:wisdom | guiding | wisdom | Principled Guidance Foresight | 0 | NO_ITEMS | Foresight addressed through trade-offs and climate considerations |
| E:applying:data | applying | data | Verified Execution Evidence | 1 | HAS_ITEMS | As-built survey scope unclear |
| E:applying:information | applying | information | Actionable Performance Report | 0 | NO_ITEMS | Performance reporting adequately addressed through records |
| E:applying:knowledge | applying | knowledge | Proven Execution Command | 0 | NO_ITEMS | Execution command proven through phased procedure |
| E:applying:wisdom | applying | wisdom | Grounded Execution Judgment | 0 | NO_ITEMS | Execution judgment grounded in Guidance trade-offs |
| E:judging:data | judging | data | Substantiated Evaluation Record | 0 | NO_ITEMS | Evaluation records substantiated through verification table |
| E:judging:information | judging | information | Contextual Assessment Report | 0 | NO_ITEMS | Assessment reporting addressed through inspection protocols |
| E:judging:knowledge | judging | knowledge | Proven Assessment Mastery | 0 | NO_ITEMS | Assessment mastery demonstrated through multi-party verification |
| E:judging:wisdom | judging | wisdom | Principled Evaluation Wisdom | 1 | HAS_ITEMS | Conflict resolution process for inspection disagreements not defined |
| E:reviewing:data | reviewing | data | Verified Assurance Evidence | 0 | NO_ITEMS | Assurance evidence verified through testing and survey records |
| E:reviewing:information | reviewing | information | Contextual Assurance Report | 0 | NO_ITEMS | Assurance reporting adequately addressed |
| E:reviewing:knowledge | reviewing | knowledge | Proven Assurance Command | 0 | NO_ITEMS | Assurance command proven through records and inspection framework |
| E:reviewing:wisdom | reviewing | wisdom | Principled Assurance Judgment | 0 | NO_ITEMS | Assurance judgment principled through CCDC framework reference |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Multi | Datasheet | Clarify as-built survey scope boundary — the as-built survey (DEL-008-04) is listed as both a verification method for this deliverable and a separate deliverable; clarify what data DEL-018-02 must produce independently vs. what DEL-008-04 provides | Verified execution evidence requires clear responsibility for data production. The as-built survey is referenced as verification evidence for REQ-01 and REQ-04 but is a separate deliverable (DEL-008-04). The boundary between what DEL-018-02 must verify independently and what it can rely on DEL-008-04 to provide is unclear. | Specification.md; Procedure.md; Datasheet.md | Specification §Verification REQ-01, REQ-04; Procedure §Steps E-5; Datasheet §Construction (As-built survey) | — | PROPOSAL: Clarify in Datasheet that DEL-008-04 provides formal survey; DEL-018-02 performs field-level grade checks during execution | TBD |
| E-002 | E:judging:wisdom | Conflict | Guidance | Guidance | Resolve conflict between Guidance CON-002 (landscaping scope boundary between PKG-018 and PKG-007) and the lack of a defined dispute resolution mechanism if the landscape architect and General Contractor disagree on conformance during inspection | Principled evaluation wisdom requires a defined path for resolving professional disagreements during conformance assessment. Guidance CON-002 identifies the scope boundary ambiguity, and REQ-05 verification authority is TBD, creating a compounded risk: if a dispute arises during landscape inspection, no resolution mechanism exists. | Guidance.md; Specification.md | Guidance §Conflict Table CON-002; Specification §Requirements REQ-05 | Guidance.md#Conflict Table CON-002; Specification.md#Requirements REQ-05 | PROPOSAL: Define dispute resolution mechanism referencing CCDC 14-2013 dispute provisions | TBD |
