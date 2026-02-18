# Semantic Lensing Register: DEL-03-04 Mechanical Design Brief

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-04_MechanicalDesignBrief
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-03-04_MechanicalDesignBrief/_CONTEXT.md (DEL-03-04; PKG-003; Mechanical Design Brief)
- _STATUS.md — DEL-03-04_MechanicalDesignBrief/_STATUS.md (current state: SEMANTIC_READY; last updated 2026-02-17)
- _SEMANTIC.md — DEL-03-04_MechanicalDesignBrief/_SEMANTIC.md (8 matrices: A, B, C, F, D, K, X, E parsed successfully)
- Datasheet.md — DEL-03-04_MechanicalDesignBrief/Datasheet.md (present; read in full)
- Specification.md — DEL-03-04_MechanicalDesignBrief/Specification.md (present; read in full)
- Guidance.md — DEL-03-04_MechanicalDesignBrief/Guidance.md (present; read in full)
- Procedure.md — DEL-03-04_MechanicalDesignBrief/Procedure.md (present; read in full)
- _REFERENCES.md — DEL-03-04_MechanicalDesignBrief/_REFERENCES.md (present; read in full)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 3  B: 4  C: 2  F: 2  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 4
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0 (3 conflicts already identified in Guidance Conflict Table; no new conflicts discovered)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive language for ASHRAE 110 reference in C-002 |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Verification timing lacks specificity |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Addendum 03 compliance well-covered across all documents |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Missing audit trail mechanism for code edition tracking |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Step 3 and Step 4 cover practical execution well |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Specification covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Step 5 cross-discipline review and Step 6 compliance check cover process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-001 through P-005 provide clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance Examples EX-001 through EX-003 demonstrate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | EX-003 strong vs. weak brief comparison serves worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Design Manager QC checklist in Procedure Step 5 covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen C-002 language: replace "consult ASHRAE 110 or equivalent" with a definitive code reference or explicitly mark as TBD with a resolution path | C-002 uses vague "consult ASHRAE 110 or equivalent; actual code provision location TBD" which could leave CO prevention standard ambiguous for detailed design | Specification.md | § R-D: Code Compliance, Req C-002 | -- | Specification governs requirements | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add specific timing milestones to Verification table entries (e.g., "Draft review" should specify at which procedure step or calendar milestone this occurs) | Verification table uses timing labels "Pre-submission" and "Draft review" without tying them to Procedure step numbers or calendar milestones, making enforcement ambiguous | Specification.md | § Verification | -- | Specification governs verification | TBD |
| A-003 | A:normative:reviewing | MissingSlot | Datasheet | Datasheet | Add a row to the References table noting the specific edition of ABC/NBCC that governs, or explicitly record "edition TBD" with resolution trigger | Code editions are referenced generically ("Alberta Building Code," "NBCC") across all documents without identifying the applicable edition; this creates audit risk if editions change between proposal and construction | Datasheet.md | § References | -- | Datasheet governs factual parameters | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | ASHRAE design temperature sourced as assumption |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes and Conditions tables provide adequate evidence |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing explicit natural gas utility availability datum |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units and values consistent across documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Oil/water separator regulatory requirement unconfirmed |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each system selection adequately provided in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Six brief topics and seven Addendum 03 items comprehensively tracked |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for bay door mechanism |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | System selection rationale demonstrates fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs T-001 through T-004 demonstrate competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Zone-by-zone coverage thorough across Guidance and Procedure |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict Table in Guidance demonstrates essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off judgments adequately presented |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable coordination (DEL-04-02, DEL-05-03) shows holistic awareness |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-001 through P-005 show principled reasoning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify ASHRAE design temperature: either obtain certified value for Penhold specifically or explicitly state "Red Deer proxy, approximately -33C, to be confirmed with ASHRAE data for project site" | Datasheet Conditions table states "approximately -33C for Red Deer region" as an ASSUMPTION proxy; this is the foundational heating design parameter and approximation may be insufficient for detailed design sizing | Datasheet.md | § Conditions, Climate row | -- | Datasheet governs factual parameters | TBD |
| B-002 | B:data:completeness | TBD_Question | Datasheet | Datasheet | Add a Conditions row for natural gas utility availability at site (confirmed/unconfirmed/TBD) with resolution path | Generator fuel selection (T-002) and heating plant selection depend on whether natural gas is available at the site; this datum is referenced as TBD across Guidance and Procedure but not recorded as a formal data point in Datasheet | Datasheet.md | § Conditions | -- | Datasheet governs factual parameters; civil/utility coordination needed | TBD |
| B-003 | B:information:necessity | TBD_Question | Guidance | Guidance | Add explicit TBD note in C-003 Plumbing section: "Confirm whether Alberta Environment requires oil/water separator for bay sump discharge; consult AHJ during detailed design" | Oil/water separator requirement is noted as an ASSUMPTION in Guidance C-003 but lacks a clear resolution trigger; this is a regulatory requirement that could significantly affect plumbing design and cost | Guidance.md | § C-003: Plumbing Systems, Bay floor sumps | -- | Guidance for interpretation; regulatory answer from AHJ | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize bay door secondary opening mechanism terminology across all documents: use "bay door secondary opening mechanism" consistently; avoid mixing "hand-crank," "secondary operator," "manual backup" without linking to the standard term | Guidance CONF-02 uses "secondary opening mechanism," C-005 uses "manual hand-crank operator," "hydraulic backup accumulator," and "gravity-release mechanism"; Procedure Step 3 uses "secondary door opening type"; Specification M-007 uses "secondary opening mechanism" -- terms should be normalized to a single preferred term with alternatives listed once | Guidance.md, Procedure.md, Specification.md | § CONF-02 (Guidance), § M-007 (Specification), § Step 3 (Procedure) | -- | Guidance governs terminology | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 0 | NO_ITEMS | Addendum 03 items handled as non-negotiable imperatives |
| C:normative:sufficiency | normative | sufficiency | justified compliance | 1 | HAS_ITEMS | Fire pump need is unresolved |
| C:normative:completeness | normative | completeness | exhaustive mandate | 0 | NO_ITEMS | All seven Addendum 03 mandates exhaustively tracked |
| C:normative:consistency | normative | consistency | harmonized compliance | 0 | NO_ITEMS | Addendum 03 governs-over-RFP rule consistently applied |
| C:operative:necessity | operative | necessity | operational necessity | 0 | NO_ITEMS | Operations-fit design principle covers operational necessities |
| C:operative:sufficiency | operative | sufficiency | proven competence | 0 | NO_ITEMS | System selection rationales demonstrate proven competence |
| C:operative:completeness | operative | completeness | thorough implementation | 0 | NO_ITEMS | Step-by-step procedure provides thorough implementation path |
| C:operative:consistency | operative | consistency | repeatable discipline | 1 | HAS_ITEMS | Checklist status tracking not fully formalized |
| C:evaluative:necessity | evaluative | necessity | intrinsic significance | 0 | NO_ITEMS | Purpose sections in Guidance and Procedure establish significance |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible merit | 0 | NO_ITEMS | Trade-offs and examples provide defensible merit |
| C:evaluative:completeness | evaluative | completeness | comprehensive valuation | 0 | NO_ITEMS | EX-003 strong vs. weak comparison provides comprehensive valuation framework |
| C:evaluative:consistency | evaluative | consistency | principled worth | 0 | NO_ITEMS | Principles consistently applied across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add a verification row for fire pump determination: "Fire pump necessity confirmed based on municipal water pressure data (TBD from civil coordination); responsible party: Mechanical Engineer + Civil Engineer" | Guidance C-004 identifies fire pump as "TBD in detailed design" if municipal water pressure is insufficient, but Specification Verification table has no verification entry for fire pump determination; this is a potential code compliance item that should be tracked | Specification.md | § Verification | -- | Specification governs verification | TBD |
| C-002 | C:operative:consistency | MissingSlot | Procedure | Procedure | Add a formal checklist artifact template in Step 1 or as an appendix, with defined status values (Draft/Complete/Reviewed) and a tracking mechanism for Addendum 03 items across procedure steps | Procedure Step 1 directs creation of a "Mechanical Brief Authoring Checklist" with status columns but does not provide the actual template or define how status is tracked between Steps 1-7; this weakens repeatable discipline | Procedure.md | § Step 1 | -- | Procedure governs process | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandated regulatory basis | 0 | NO_ITEMS | Addendum 03 + RFP provide clear mandated regulatory basis |
| F:normative:sufficiency | normative | sufficiency | qualified regulatory proof | 1 | HAS_ITEMS | Standard edition specifics unresolved |
| F:normative:completeness | normative | completeness | total prescriptive coverage | 0 | NO_ITEMS | All prescriptive requirements enumerated in Specification R-A through R-D |
| F:normative:consistency | normative | consistency | coherent regulatory alignment | 0 | NO_ITEMS | Addendum 03 governs-over-RFP rule provides coherent alignment |
| F:operative:necessity | operative | necessity | grounded functional capacity | 0 | NO_ITEMS | Zone-by-zone functional capacity well grounded |
| F:operative:sufficiency | operative | sufficiency | demonstrated proficiency | 0 | NO_ITEMS | Trade-offs and rationale demonstrate proficiency |
| F:operative:completeness | operative | completeness | exhaustive operational command | 0 | NO_ITEMS | Six brief topics + seven Addendum items provide exhaustive operational scope |
| F:operative:consistency | operative | consistency | systematic operational coherence | 1 | HAS_ITEMS | Cross-deliverable scope boundary language varies |
| F:evaluative:necessity | evaluative | necessity | grounded value foundation | 0 | NO_ITEMS | P-001 through P-005 ground value foundation |
| F:evaluative:sufficiency | evaluative | sufficiency | credible value demonstration | 0 | NO_ITEMS | Examples and trade-offs credibly demonstrate value |
| F:evaluative:completeness | evaluative | completeness | exhaustive value accounting | 0 | NO_ITEMS | Lifecycle cost, reliability, and replacement cycle coverage adequate |
| F:evaluative:consistency | evaluative | consistency | integral value consistency | 0 | NO_ITEMS | Value propositions consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen Standards table: for each standard with "location TBD," add a resolution trigger (e.g., "edition to be confirmed at detailed design kickoff") so that regulatory proof is traceable | Five of eight entries in the Specification Standards table have "location TBD" for the specific edition; this pattern of deferred specificity could weaken regulatory proof if not tracked | Specification.md | § Standards | -- | Specification governs standards | TBD |
| F-002 | F:operative:consistency | Normalization | Multi | Guidance | Normalize scope boundary language: Specification uses "excludes" list, Guidance uses "belongs to DEL-04-02/DEL-05-03," Procedure uses "does not duplicate"; recommend a single canonical phrasing for scope boundaries used consistently across all three documents | Scope boundaries between DEL-03-04, DEL-04-02, and DEL-05-03 are stated differently in Specification (Scope Exclusions), Guidance (Purpose paragraph 3), and Procedure (Purpose paragraph, Step 4 drafting tips); while semantically aligned, the varying phrasing could cause drift | Specification.md, Guidance.md, Procedure.md | § Scope (Specification), § Purpose (Guidance), § Purpose and Step 4 (Procedure) | -- | Guidance for interpretation | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | binding regulatory directive | 0 | NO_ITEMS | Addendum 03 treated as binding directive throughout |
| D:normative:applying | normative | applying | enforced compliance practice | 0 | NO_ITEMS | Procedure enforcement via checklists and reviews adequate |
| D:normative:judging | normative | judging | definitive conformance ruling | 0 | NO_ITEMS | Verification table provides conformance rulings |
| D:normative:reviewing | normative | reviewing | systematic compliance verification | 1 | HAS_ITEMS | Missing verification for R-D code compliance requirements |
| D:operative:guiding | operative | guiding | grounded method governance | 0 | NO_ITEMS | Procedure Steps 1-7 provide grounded method governance |
| D:operative:applying | operative | applying | settled performance capability | 0 | NO_ITEMS | System selections demonstrate settled capability |
| D:operative:judging | operative | judging | definitive performance ruling | 0 | NO_ITEMS | Verification table covers performance ruling |
| D:operative:reviewing | operative | reviewing | settled procedural inspection | 1 | HAS_ITEMS | No independent QA review step distinct from authoring team |
| D:evaluative:guiding | evaluative | guiding | principled value direction | 0 | NO_ITEMS | Principles P-001 through P-005 provide principled direction |
| D:evaluative:applying | evaluative | applying | established merit practice | 0 | NO_ITEMS | Examples and trade-offs establish merit practice |
| D:evaluative:judging | evaluative | judging | definitive worth ruling | 0 | NO_ITEMS | EX-003 strong vs. weak comparison provides worth ruling |
| D:evaluative:reviewing | evaluative | reviewing | assured quality inspection | 0 | NO_ITEMS | Design Manager QC checklist in Procedure Step 5 provides quality inspection |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:reviewing | VerificationGap | Specification | Specification | Add verification rows for R-D requirements (C-001, C-002, C-003): e.g., "Brief references Alberta Building Code as governing framework -- verified by Design Manager" | Specification Verification table covers R-A (Addendum 03 items), R-B (RFP topics), R-C (design life), and cross-discipline coordination, but has no explicit verification entries for R-D Code Compliance requirements (C-001, C-002, C-003) | Specification.md | § Verification | -- | Specification governs verification | TBD |
| D-002 | D:operative:reviewing | RationaleGap | Procedure | Procedure | Add rationale in Step 5 or Step 6 for why no independent QA reviewer (outside the authoring team) is included, or add such a step if warranted for proposal quality assurance | Procedure Step 5 cross-discipline review is performed by team members who are also contributors; there is no independent quality assurance step by a reviewer outside the project team; for a scored proposal deliverable, this may leave quality inspection under-assured | Procedure.md | § Step 5 and Step 6 | -- | Procedure governs process | TBD |

---

## Matrix K -- Transpose of D (4x3)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| K:guiding:normative | guiding | normative | binding regulatory directive | 0 | NO_ITEMS | Same cell value as D:normative:guiding; no additional items warranted from transposed perspective |
| K:guiding:operative | guiding | operative | grounded method governance | 0 | NO_ITEMS | Same cell value as D:operative:guiding; covered |
| K:guiding:evaluative | guiding | evaluative | principled value direction | 0 | NO_ITEMS | Same cell value as D:evaluative:guiding; covered |
| K:applying:normative | applying | normative | enforced compliance practice | 0 | NO_ITEMS | Same cell value as D:normative:applying; covered |
| K:applying:operative | applying | operative | settled performance capability | 0 | NO_ITEMS | Same cell value as D:operative:applying; covered |
| K:applying:evaluative | applying | evaluative | established merit practice | 0 | NO_ITEMS | Same cell value as D:evaluative:applying; covered |
| K:judging:normative | judging | normative | definitive conformance ruling | 0 | NO_ITEMS | Same cell value as D:normative:judging; covered |
| K:judging:operative | judging | operative | definitive performance ruling | 0 | NO_ITEMS | Same cell value as D:operative:judging; covered |
| K:judging:evaluative | judging | evaluative | definitive worth ruling | 0 | NO_ITEMS | Same cell value as D:evaluative:judging; covered |
| K:reviewing:normative | reviewing | normative | systematic compliance verification | 0 | NO_ITEMS | Same cell value as D:normative:reviewing; item D-001 already captured |
| K:reviewing:operative | reviewing | operative | settled procedural inspection | 0 | NO_ITEMS | Same cell value as D:operative:reviewing; item D-002 already captured |
| K:reviewing:evaluative | reviewing | evaluative | assured quality inspection | 0 | NO_ITEMS | Same cell value as D:evaluative:reviewing; covered |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational prescriptive authority | 0 | NO_ITEMS | Addendum 03 and RFP provide foundational prescriptive authority |
| X:guiding:sufficiency | guiding | sufficiency | warranted directive adequacy | 1 | HAS_ITEMS | Generator runtime assumption lacks directive authority |
| X:guiding:completeness | guiding | completeness | total directive coverage | 0 | NO_ITEMS | All six RFP topics + seven Addendum items = total directive coverage |
| X:guiding:consistency | guiding | consistency | integrated directive alignment | 0 | NO_ITEMS | Documents aligned on directive hierarchy (Addendum 03 > RFP) |
| X:applying:necessity | applying | necessity | critical applied standard | 1 | HAS_ITEMS | Missing acceptance criteria for ventilation rates |
| X:applying:sufficiency | applying | sufficiency | proven applied conformance | 0 | NO_ITEMS | Procedure Step 4 Addendum 03 inline completion check proves conformance |
| X:applying:completeness | applying | completeness | exhaustive applied scope | 1 | HAS_ITEMS | Mechanical room ventilation underspecified |
| X:applying:consistency | applying | consistency | stable applied discipline | 0 | NO_ITEMS | Consistent application discipline across procedure steps |
| X:judging:necessity | judging | necessity | binding adjudicative standard | 0 | NO_ITEMS | Verification hooks in Specification provide binding adjudicative standards |
| X:judging:sufficiency | judging | sufficiency | justified adjudicative basis | 0 | NO_ITEMS | Verification approach descriptions provide justified basis |
| X:judging:completeness | judging | completeness | exhaustive adjudicative coverage | 0 | NO_ITEMS | All requirement groups (R-A through R-D) have verification coverage |
| X:judging:consistency | judging | consistency | principled adjudicative coherence | 0 | NO_ITEMS | Adjudicative approach consistent across requirement groups |
| X:reviewing:necessity | reviewing | necessity | critical verification standard | 1 | HAS_ITEMS | No verification for cross-reference accuracy |
| X:reviewing:sufficiency | reviewing | sufficiency | proven verification adequacy | 0 | NO_ITEMS | Verification table adequate for main requirements |
| X:reviewing:completeness | reviewing | completeness | exhaustive verification scope | 0 | NO_ITEMS | Combined Specification verification + Procedure V-001 through V-009 provide exhaustive scope |
| X:reviewing:consistency | reviewing | consistency | aligned verification integrity | 0 | NO_ITEMS | Verification approaches consistent between Specification and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add rationale in C-005 or Conflict Table for why 72-hour runtime is the assumed target (e.g., cite Functional Program row 30.0 context, standard emergency services practice, or Owner input) so the assumption has a defensible basis | CONF-01 identifies the 72-hour generator runtime as an assumption but the directive basis is described as "partially obscured" from a prior analysis; the assumption lacks sufficient directive authority to be defensible without explicit rationale | Guidance.md | § C-005, § Conflict Table CONF-01 | -- | Guidance for interpretation | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add a verification entry: "Ventilation rates for each zone are either specified as design-phase TBD with code reference, or stated as minimum rates per ASHRAE 62.1/62.2 -- verified by Mechanical Engineer during Step 3" | Guidance C-002 states ventilation rates as "TBD in detailed design" for multiple zones (apparatus bays, PW bays, bunker gear room) but Specification has no verification hook confirming that rate determination is tracked as a design-phase deliverable | Specification.md | § Verification | -- | Specification governs verification | TBD |
| X-003 | X:applying:completeness | MissingSlot | Guidance | Guidance | Add explicit mechanical room ventilation entry in C-002 zone listing: state whether combustion air provision per code is the sole ventilation strategy or whether additional cooling ventilation is needed for equipment heat rejection | Guidance C-002 lists mechanical room ventilation last and with minimal detail ("Fresh combustion air for gas-fired boiler; mechanical ventilation may double as boiler combustion air per code provisions"); no mention of equipment heat rejection or cooling for the mechanical room itself | Guidance.md | § C-002: Ventilation Strategy by Zone, Mechanical room | -- | Guidance for interpretation | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add a verification step or checklist item in Step 5 or Step 6: "Confirm all cross-deliverable references (DEL-02-04, DEL-04-02, DEL-05-03, DEL-03-02, DEL-03-03, DEL-03-05) are accurate and consistent with current versions of those deliverables" | Datasheet References table and Specification Documentation table list multiple cross-deliverable references; Procedure Step 5 checks cross-discipline coordination but does not explicitly verify that referenced deliverable IDs, names, and relationship descriptions are accurate | Procedure.md | § Step 5 | -- | Procedure governs process | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | sovereign compliance foundation | 0 | NO_ITEMS | Addendum 03 + RFP + ABC provide sovereign compliance foundation |
| E:normative:sufficiency | normative | sufficiency | substantiated compliance proof | 1 | HAS_ITEMS | NFPA 1581 reference unsubstantiated |
| E:normative:completeness | normative | completeness | absolute regulatory coverage | 0 | NO_ITEMS | All regulatory requirements enumerated across R-A through R-D |
| E:normative:consistency | normative | consistency | unified regulatory coherence | 0 | NO_ITEMS | Regulatory hierarchy (Addendum 03 > RFP) consistently applied |
| E:operative:necessity | operative | necessity | mandatory performance foundation | 0 | NO_ITEMS | Zone-by-zone performance requirements provide mandatory foundation |
| E:operative:sufficiency | operative | sufficiency | verified operational sufficiency | 0 | NO_ITEMS | Verification table + Procedure V-items verify sufficiency |
| E:operative:completeness | operative | completeness | absolute operational coverage | 0 | NO_ITEMS | All six topics + seven Addendum items = absolute operational coverage |
| E:operative:consistency | operative | consistency | unified operational discipline | 0 | NO_ITEMS | Consistent operational discipline across documents |
| E:evaluative:necessity | evaluative | necessity | sovereign value standard | 1 | HAS_ITEMS | Evaluator perspective underrepresented |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated merit proof | 0 | NO_ITEMS | Examples and trade-offs substantiate merit |
| E:evaluative:completeness | evaluative | completeness | absolute value coverage | 0 | NO_ITEMS | Life-cycle, operations-fit, and simplicity values covered |
| E:evaluative:consistency | evaluative | consistency | unified value integrity | 0 | NO_ITEMS | Value propositions unified across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Guidance | Guidance | Normalize NFPA 1581 reference: either add NFPA 1581 to Specification Standards table and Datasheet References table, or remove the specific citation from Guidance C-002 and replace with a generic "fire service gear storage best practices (standard TBD)" | Guidance C-002 (bunker gear room ventilation) references "NFPA 1581 or equivalent fire service gear storage best practices" but this standard does not appear in either the Specification Standards table or the Datasheet References table; this creates an inconsistency in the standards register | Guidance.md | § C-002, Bunker gear storage room | -- | Specification for standards; Datasheet for references | TBD |
| E-002 | E:evaluative:necessity | MissingSlot | Guidance | Guidance | Add a brief consideration or note in Guidance Purpose or Principles addressing how the brief should be written to score well with the evaluation committee (e.g., "The brief should demonstrate responsiveness to Addendum 03 in a way visible to evaluators scanning for keyword compliance") | Guidance Purpose identifies three audiences (Evaluation Committee, Owner, Design-Build Team) but the Considerations and Principles sections focus almost exclusively on technical design decisions; there is no guidance on writing for evaluator scoring perspective, which is the primary value driver for this proposal deliverable (OBJ-004, 5 pts) | Guidance.md | § Purpose, § Principles | -- | Guidance for interpretation | TBD |
