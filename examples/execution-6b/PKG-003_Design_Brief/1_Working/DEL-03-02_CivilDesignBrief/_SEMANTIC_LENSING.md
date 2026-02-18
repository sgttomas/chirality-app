# Semantic Lensing Register: DEL-03-02 Civil Design Brief

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-02_CivilDesignBrief
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-03-02_CivilDesignBrief/_CONTEXT.md (DEL-03-02, PKG-003, SOW-0011, OBJ-004)
- _STATUS.md -- DEL-03-02_CivilDesignBrief/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-03-02_CivilDesignBrief/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md -- DEL-03-02_CivilDesignBrief/Datasheet.md (present, read)
- Specification.md -- DEL-03-02_CivilDesignBrief/Specification.md (present, read)
- Guidance.md -- DEL-03-02_CivilDesignBrief/Guidance.md (present, read)
- Procedure.md -- DEL-03-02_CivilDesignBrief/Procedure.md (present, read)
- _REFERENCES.md -- DEL-03-02_CivilDesignBrief/_REFERENCES.md (present, read)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 3
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 3  B: 3  C: 2  F: 2  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 4
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards section has TBD thresholds |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | ABC vs NBCC dual-listing ambiguity |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Verification table covers all 15 requirements with pass criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 5 checklist is comprehensive |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-6 provide clear sequencing |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps include actionable detail |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing page-length/quality targets in Specification |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Verification summary V-CDB-01 through V-CDB-06 present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles P-CDB-01 through P-CDB-07 provide value direction |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Examples EX-CDB-01 through EX-CDB-03 demonstrate quality application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | OBJ-004 scoring link present in _CONTEXT.md and Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Step 5 quality review and Design Coordinator approval present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta Environment stormwater thresholds apply, or explicitly mark as TBD with the responsible party for resolution | Specification Standards table lists "Alberta Environment (AEP) -- Stormwater Management" with thresholds noted as "TBD pending detailed design." Without at least a named regulation or guideline edition, prescriptive direction is incomplete -- the brief author lacks a concrete standard to reference. | Specification.md | Standards table, row "Alberta Environment (AEP)" | -- | Civil Engineer to confirm applicable AEP guideline | TBD |
| A-002 | A:normative:applying | Normalization | Specification | Guidance | Clarify the relationship between ABC and NBCC references: state which is the governing code for civil/site design elements (parking minimums, accessible parking) and which is the referenced national standard | Specification Standards table lists both "Alberta Building Code (ABC)" and "National Building Code of Canada (NBCC)" as applicable. ABC adopts NBCC with amendments. Listing both without clarifying which governs for civil design elements creates ambiguity in mandatory practice. | Specification.md | Standards table | -- | Civil Engineer / Proposal Manager | TBD |
| A-003 | A:operative:judging | MissingSlot | Specification | Specification | Add a qualitative or quantitative pass criterion for brief narrative quality (e.g., minimum substantive rationale depth, or evaluator readability standard) to complement the topic-presence checklist | Verification table checks only for presence of content ("section present," "statement present"). There is no mechanism to assess whether the rationale is substantive enough to score well on OBJ-004. Guidance mentions evaluators expect "substantive professional reasoning" but Specification has no corresponding assessment criterion. | Specification.md | Verification table | -- | Proposal Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing fire apparatus dimensions |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet cites source for every attribute |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing parking count range |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Site area figures (12/20 acres) consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | RFP topic list clearly enumerated in all docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations C-CDB-01 through C-CDB-07 provide thorough context |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | DEL-10-02 cross-reference absent from Procedure |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cash allowance treatment described consistently |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Geotechnical, wetland, and environmental references well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Civil Engineer role clearly assigned with required expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Seven topical areas comprehensively developed |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Cross-document understanding of cash allowance is aligned |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off table T-CDB-01 through T-CDB-05 present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs identify evaluation considerations |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers climate, operations, cost, compliance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-CDB-01 through P-CDB-07 provide consistent reasoning framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Add essential factual parameters: largest fire apparatus turning radius requirement and NFPA lane width minimums (or equivalent Alberta standard) to inform civil access design | Datasheet documents Cold Storage footprint (60x100 ft), site acreage, and building orientation but omits the fire apparatus dimensional parameters (turning radius, lane width) that drive the street access and on-site circulation design. Guidance C-CDB-02 asks "Width and turning radius adequate for the largest apparatus?" but the factual basis is not recorded. | Datasheet.md | Attributes table; Conditions table | -- | Civil Engineer / Fire Department | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add an attribute row for anticipated parking count range or the basis for determining it (e.g., staffing levels, ABC code minimum ratios) | Guidance C-CDB-01 asks "How many spaces are proposed and what drives the quantity?" and marks the count as "TBD pending design team determination." Datasheet does not record even an estimated range or the formula inputs (staffing, shift overlap, visitor demand). This essential fact is needed for the brief author. | Datasheet.md | Attributes table | -- | Civil Engineer / Architect | TBD |
| B-003 | B:information:completeness | MissingSlot | Procedure | Procedure | Add DEL-10-02 (Site Conditions and Due Diligence Summary) to the Prerequisites table as a Coordination Input, consistent with Specification Documentation and Datasheet References | Specification Documentation section and Datasheet References both list DEL-10-02 as requiring consistent site-condition language. However, Procedure Prerequisites table omits DEL-10-02 entirely. The Civil Engineer may not realize they need to cross-check with this document. | Procedure.md | Prerequisites table | -- | Proposal Manager | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Baseline | 1 | HAS_ITEMS | Road authority access permit requirements weak |
| C:normative:sufficiency | normative | sufficiency | Regulatory Justification | 0 | NO_ITEMS | Specification provides source for each requirement |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 0 | NO_ITEMS | All 7 RFP topics covered; Addendum 03 items addressed |
| C:normative:consistency | normative | consistency | Codified Conformance | 0 | NO_ITEMS | Requirement IDs and verification IDs are consistent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table is comprehensive |
| C:operative:sufficiency | operative | sufficiency | Proficient Execution | 0 | NO_ITEMS | Steps contain actionable detail |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 1 | HAS_ITEMS | Target page lengths not in Specification |
| C:operative:consistency | operative | consistency | Harmonized Reliability | 0 | NO_ITEMS | Procedure steps correspond to Specification requirements |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Guidance explains why brief exists and value to evaluators |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal | 0 | NO_ITEMS | Examples demonstrate adequate vs inadequate quality |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Principles cover operations, climate, cost, compliance, coordination |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation | 0 | NO_ITEMS | Principles are internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen R-CDB-08 or Standards table to specify which road authority governs access permits for Waskasoo Avenue North (Alberta Transportation vs Town of Penhold) and what documentation is needed | Specification R-CDB-08 mentions "coordination with Town road authority" but the Standards table lists "Alberta Transportation / Road Authority -- Access Management" with "ASSUMPTION: Road authority access permit required; specific requirements TBD." The enforceable baseline for access permitting is ambiguous -- it is unclear whether the road is provincial or municipal jurisdiction. | Specification.md | R-CDB-08; Standards table row "Alberta Transportation" | -- | Civil Engineer | TBD |
| C-002 | C:operative:completeness | RationaleGap | Guidance | Guidance | Add rationale for why Procedure Step 2 target page lengths (0.5-1.5 pages per section) are appropriate for OBJ-004 scoring, or note that these are guidelines only and the Civil Engineer should calibrate to content depth needed | Procedure Step 2 sub-steps include target page lengths (e.g., "0.5-1 page" for parking, "0.75-1.5 pages" for access) but these appear only in Procedure, not Specification. Guidance does not explain the rationale for these targets or how they relate to evaluator expectations. If the targets are important, they need rationale; if they are advisory only, this should be stated. | Procedure.md; Guidance.md | Procedure Step 2 (all sub-steps); Guidance entire document scanned | -- | Proposal Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Regulatory Basis | 0 | NO_ITEMS | All requirements trace to RFP, Addendum 03, or Decomposition |
| F:normative:sufficiency | normative | sufficiency | Validated Compliance Threshold | 1 | HAS_ITEMS | Town development standards absent |
| F:normative:completeness | normative | completeness | Total Compliance Command | 0 | NO_ITEMS | 15 requirements cover all 7 RFP topics plus cross-cutting concerns |
| F:normative:consistency | normative | consistency | Uniform Code Discipline | 0 | NO_ITEMS | Requirement numbering and format consistent |
| F:operative:necessity | operative | necessity | Critical Process Foundation | 0 | NO_ITEMS | Prerequisite inputs well-defined |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Civil Engineer role and qualification expectations clear |
| F:operative:completeness | operative | completeness | Total Operational Mastery | 0 | NO_ITEMS | Steps 1-6 cover full lifecycle from assignment to integration |
| F:operative:consistency | operative | consistency | Integrated Dependability | 0 | NO_ITEMS | Verification points at each step |
| F:evaluative:necessity | evaluative | necessity | Fundamental Value Acuity | 0 | NO_ITEMS | OBJ-004 link established |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth | 1 | HAS_ITEMS | No evaluator scoring criteria referenced |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Synthesis | 0 | NO_ITEMS | Trade-offs table addresses major design choices |
| F:evaluative:consistency | evaluative | consistency | Calibrated Value Integrity | 0 | NO_ITEMS | Consistent value framework across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | TBD_Question | Specification | Specification | Identify and record applicable Town of Penhold development standards (parking bylaws, stormwater management bylaws, access/road standards) or explicitly state they are TBD pending confirmation with the Town, with responsibility assigned | Specification Standards table lists "Town of Penhold Development Standards / Bylaws" but marks all specific requirements as "ASSUMPTION: Local municipal standards apply; specific requirements TBD -- confirm with Town." Without the actual bylaw numbers or standard edition, the validated compliance threshold is unachievable at draft stage. The brief may inadvertently omit a local requirement. | Specification.md | Standards table, row "Town of Penhold Development Standards" | -- | Civil Engineer / Proposal Manager | TBD |
| F-002 | F:evaluative:sufficiency | VerificationGap | Specification | Specification | Add a requirement or verification step that maps brief content to OBJ-004 evaluation criteria (from RFP evaluation matrix), confirming the brief is calibrated to what evaluators will score | Guidance states the brief "contributes to OBJ-004 (Design Brief, 5 pts)" and evaluators expect "substantive professional reasoning." However, Specification has no requirement referencing the actual OBJ-004 evaluation criteria or scoring rubric. The brief could satisfy all 15 R-CDB requirements yet still score poorly if the evaluation criteria emphasize aspects not captured in the requirements. | Specification.md; Guidance.md | Specification Verification table; Guidance Purpose section | -- | Proposal Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Regulatory Directive | 0 | NO_ITEMS | RFP Section 7.1.2(2) clearly directs all topics |
| D:normative:applying | normative | applying | Enacted Compliance Practice | 0 | NO_ITEMS | Requirements R-CDB-01 through R-CDB-15 enact RFP direction |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Verification table provides clear pass criteria |
| D:normative:reviewing | normative | reviewing | Formal Standards Inspection | 0 | NO_ITEMS | Step 5 checklist provides formal review mechanism |
| D:operative:guiding | operative | guiding | Settled Process Direction | 0 | NO_ITEMS | 6-step procedure is well-sequenced |
| D:operative:applying | operative | applying | Proven Effective Delivery | 0 | NO_ITEMS | Procedure steps are executable |
| D:operative:judging | operative | judging | Confirmed Capability Verdict | 0 | NO_ITEMS | V-CDB-01 through V-CDB-06 confirm capability at each gate |
| D:operative:reviewing | operative | reviewing | Systematic Reliability Review | 1 | HAS_ITEMS | No explicit re-review cycle if brief fails Step 5 |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Compass | 0 | NO_ITEMS | Guidance Purpose establishes value direction clearly |
| D:evaluative:applying | evaluative | applying | Enacted Merit | 0 | NO_ITEMS | Examples EX-CDB-01 and EX-CDB-02 demonstrate enacted quality |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 1 | HAS_ITEMS | No grading scale for brief quality |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Merit Standard | 0 | NO_ITEMS | Design Coordinator approval serves as merit gate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:reviewing | MissingSlot | Procedure | Procedure | Add a rework/iteration path to Step 5: if the quality check fails, describe the corrective action (return to Step 2 or Step 4, re-review, etc.) before the brief can proceed to Step 6 | Procedure Step 5 states "All checklist items pass. Brief approved for integration." but does not describe what happens if items fail. A systematic reliability review requires a defined rework loop. Currently, a failed check has no procedural path -- the Civil Engineer would not know whether to revise and re-submit to Step 5 or escalate. | Procedure.md | Step 5 | -- | Proposal Manager | TBD |
| D-002 | D:evaluative:judging | VerificationGap | Specification | Guidance | Add guidance on how to distinguish a "substantive" rationale from a merely "present" one (e.g., a substantive rationale must explain the why, reference at least one site condition, and connect to operational need) | Specification verification pass criteria use language like "substantive content" and "substantive rationale" but neither Specification nor Guidance defines what "substantive" means operationally. This makes the worth determination subjective. Guidance's negative example (EX-CDB-03) shows what is insufficient but does not define the threshold for adequacy. | Specification.md; Guidance.md | Specification Verification R-CDB-01; Guidance Examples section | -- | Proposal Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Mandated Essential Standard | 0 | NO_ITEMS | RFP Section 7.1.2(2) is the mandated standard |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directive Authority | 0 | NO_ITEMS | All requirements trace to authoritative sources |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 0 | NO_ITEMS | 7 RFP topics plus Addendum 03 items covered |
| X:guiding:consistency | guiding | consistency | Aligned Prescriptive Stability | 0 | NO_ITEMS | Direction is consistent across docs |
| X:applying:necessity | applying | necessity | Essential Enactment Proof | 1 | HAS_ITEMS | Verification for Cold Storage siting is weak |
| X:applying:sufficiency | applying | sufficiency | Adequate Implementation Proof | 0 | NO_ITEMS | Verification methods are appropriate to requirements |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | No verification for cross-consistency with DEL-01-06 beyond cash allowance |
| X:applying:consistency | applying | consistency | Standardized Reliable Practice | 0 | NO_ITEMS | Verification format is standardized |
| X:judging:necessity | judging | necessity | Binding Threshold Verdict | 1 | HAS_ITEMS | R-CDB-11 sump routing verification weak |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudicative Finding | 0 | NO_ITEMS | Pass criteria stated for each requirement |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 0 | NO_ITEMS | All 15 requirements have verification entries |
| X:judging:consistency | judging | consistency | Coherent Adjudicative Standard | 0 | NO_ITEMS | Consistent verification format |
| X:reviewing:necessity | reviewing | necessity | Mandatory Baseline Review | 0 | NO_ITEMS | Step 5 checklist provides mandatory review |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Checklist items match requirements |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 1 | HAS_ITEMS | No verification for Appendix D references |
| X:reviewing:consistency | reviewing | consistency | Principled Audit Protocol | 0 | NO_ITEMS | Audit protocol is principled and repeatable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Strengthen R-CDB-13 verification pass criterion from "Cold Storage placement explained" to require that the rationale addresses relationship to apparatus circulation, drainage routing, and utility routing (the three aspects named in the requirement) | R-CDB-13 requires rationale for Cold Storage siting covering "relationship to apparatus circulation, drainage, and utility routing" but the verification pass criterion says only "Cold Storage placement explained." The verification does not test whether all three named aspects are addressed, allowing a brief to mention Cold Storage placement without covering drainage or utility implications. | Specification.md | Verification table, R-CDB-13 row | -- | Civil Engineer | TBD |
| X-002 | X:applying:completeness | VerificationGap | Multi | Specification | Add a verification row for cross-consistency with DEL-01-06 (Pricing Narrative) beyond cash allowance -- specifically confirming that site servicing scope split (base vs. allowance) descriptions are textually aligned | Specification R-CDB-04 verification says "Statement present; consistent with DEL-01-06." However, DEL-01-06 is also listed in Datasheet References and Specification Documentation as requiring "consistent cash allowance treatment." The verification only checks for a cash allowance statement's presence and DEL-01-06 consistency on that point. The scope split description (base scope vs. allowance scope) in Guidance C-CDB-07 is more detailed than what R-CDB-04 requires. A brief could satisfy R-CDB-04 while still having an inconsistent scope description with DEL-01-06. | Specification.md; Datasheet.md | Specification Verification R-CDB-04; Datasheet References table row "DEL-01-06" | -- | Proposal Manager | TBD |
| X-003 | X:judging:necessity | WeakStatement | Specification | Specification | Strengthen R-CDB-11 verification pass criterion from "Sump drainage routing mentioned" to "Sump drainage routing described with identified discharge point (sanitary sewer or approved alternative)" | R-CDB-11 requires the brief to "identify how apparatus bay and PW bay sumps are integrated into the site drainage approach." The verification pass criterion is "Sump drainage routing mentioned" -- a low bar that could be satisfied by a single sentence without identifying the actual discharge connection. This is a binding threshold for a requirement that has regulatory implications (sump water discharge to sanitary vs. storm). | Specification.md | Verification table, R-CDB-11 row | -- | Civil Engineer | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Specification | Specification | Add verification items confirming that the brief references Appendix D reports (geotechnical, wetland, environmental) in appropriate sections, not just the geotechnical basis in R-CDB-06 | R-CDB-06 verifies the geotechnical basis statement (2021 report). However, Appendix D also includes the Wetland Assessment and the Environmental Assessment, both listed in Specification Standards and referenced extensively in Guidance (P-CDB-02, P-CDB-04, C-CDB-03, C-CDB-04, C-CDB-05). No requirement or verification entry checks that the wetland and environmental reports are appropriately referenced in the brief. These are separate documents with separate constraints. | Specification.md | Verification table; Standards table | -- | Civil Engineer | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Verified Enforceable Baseline | 0 | NO_ITEMS | Enforceable baseline is well-established for most items |
| E:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Proof | 0 | NO_ITEMS | Requirements trace to authoritative sources |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Reach | 1 | HAS_ITEMS | Erosion/sediment control not a requirement |
| E:normative:consistency | normative | consistency | Systematic Regulatory Discipline | 0 | NO_ITEMS | Requirement and verification system is disciplined |
| E:operative:necessity | operative | necessity | Confirmed Operational Threshold | 0 | NO_ITEMS | Prerequisites establish operational threshold |
| E:operative:sufficiency | operative | sufficiency | Evidenced Operational Competence | 0 | NO_ITEMS | Civil Engineer qualification expectations clear |
| E:operative:completeness | operative | completeness | Total Operational Coverage | 0 | NO_ITEMS | Steps 1-6 cover full production lifecycle |
| E:operative:consistency | operative | consistency | Harmonized Process Discipline | 0 | NO_ITEMS | Procedure aligns with Specification structure |
| E:evaluative:necessity | evaluative | necessity | Confirmed Intrinsic Worth | 0 | NO_ITEMS | Guidance establishes why each element matters |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Authority | 0 | NO_ITEMS | Trade-offs and examples substantiate value choices |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Value Fulfillment | 1 | HAS_ITEMS | Landscaping rationale absent |
| E:evaluative:consistency | evaluative | consistency | Integrated Value Discipline | 0 | NO_ITEMS | Value framework is internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | RationaleGap | Multi | Guidance | Add rationale in Guidance for why erosion and sediment control during construction (referenced in Guidance C-CDB-05 and Procedure Step 2.5) is not captured as a Specification requirement, or add a corresponding requirement | Guidance C-CDB-05 mentions "Erosion control during construction: silt fences, erosion blankets, temporary seeding per Alberta Environment requirements" and Procedure Step 2.5 directs the Civil Engineer to "Address erosion control during construction." However, there is no corresponding Specification requirement (R-CDB-xx) for erosion control. If it is expected in the brief, it should be a requirement with verification; if it is optional guidance, the rationale for omission should be stated. | Specification.md; Guidance.md; Procedure.md | Specification Requirements table (absent); Guidance C-CDB-05; Procedure Step 2.5 | -- | Civil Engineer | TBD |
| E-002 | E:evaluative:completeness | Normalization | Multi | Guidance | Clarify whether "landscaping" is within the scope of the Civil Design Brief or is addressed elsewhere; Procedure Step 2.7 mentions it in base scope but no other section develops the topic | Procedure Step 2.7 (Site Servicing Approach) lists "landscaping" as part of the base scope definition ("on-site utility distribution, site grading, drainage infrastructure, paving, and landscaping"). However, landscaping is not mentioned in any Specification requirement, Guidance consideration, or Datasheet construction topic. This creates a minor normalization gap -- is the Civil Engineer expected to address landscaping rationale or not? | Procedure.md; Specification.md; Guidance.md; Datasheet.md | Procedure Step 2.7; entire documents scanned for "landscaping" | -- | Civil Engineer / Proposal Manager | TBD |
