# Semantic Lensing Register: DEL-002-04 Structural Sections & Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-04_Structural-Sections/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-04_Structural-Sections/_CONTEXT.md
- _STATUS.md — DEL-002-04_Structural-Sections/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-04_Structural-Sections/_SEMANTIC.md (7 matrices parsed: A, B, C, F, D, X, E)
- Datasheet.md — DEL-002-04_Structural-Sections/Datasheet.md
- Specification.md — DEL-002-04_Structural-Sections/Specification.md
- Guidance.md — DEL-002-04_Structural-Sections/Guidance.md
- Procedure.md — DEL-002-04_Structural-Sections/Procedure.md
- _REFERENCES.md — DEL-002-04_Structural-Sections/_REFERENCES.md (read; R-01 and R-04 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 6
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 4  X: 5  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 7
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0 (4 conflicts already captured in Guidance.md Conflict Table; not duplicated here)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition not specified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp requirement well covered; construction method gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ code edition confirmation gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway addressed in Procedure Steps 14-16 |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Section cut schedule coordination is procedural but lacks checkpoint |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 5-13 provide adequate practical execution direction |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Spec and Procedure cover performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | Internal QC checklist referenced but not defined |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Trade-offs section in Guidance provides value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Drawing count vs. clarity trade-off addressed in Guidance T-01 |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality appraisal embedded in verification steps |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC checklist and P.Eng. review cover quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta Building Code edition governs this deliverable; current text says "applicable Alberta building codes" without edition | The prescriptive direction lens highlights that normative guidance requires specificity. R-010 uses "applicable Alberta building codes ... in force at time of design" and the Standards table notes "Not reviewed -- text not available; ASSUMPTION: applicable." Without a named edition, compliance determination is ambiguous. | Specification.md | R-010, Standards table | -- | Structural Engineer to confirm with AHJ | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for concrete construction method selection (cast-in-place vs. tilt-up vs. precast) as a mandatory design decision preceding detail production | Mandatory practice lens reveals that the construction method -- which fundamentally determines detail types -- has no corresponding requirement in Specification. Guidance P-03 and Procedure Step 4 reference it, but no normative requirement exists. | Specification.md | Requirements section (entire) | -- | Structural Engineer + Design-Builder (PROPOSAL) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for R-010 (Code Compliance) that identifies which code edition was applied and how clause-level compliance was confirmed | Compliance determination lens shows R-010 verification says "Review by P.Eng. of record; inspection by Authority Having Jurisdiction (AHJ)" which is generic. No mechanism to record which code edition was actually applied or verify clause-level compliance. | Specification.md | Verification table, R-010 row | -- | P.Eng. of record (PROPOSAL) | TBD |
| A-004 | A:operative:guiding | VerificationGap | Procedure | Procedure | Add a hold-point or checkpoint after Step 1 (section cut schedule) confirming the schedule is agreed before detail drawing begins in Phase 2 | Procedural direction lens highlights that Step 1 produces an "agreed section cut schedule" but Phase 2 has no prerequisite gate confirming that agreement is documented. An unconfirmed schedule could cause rework. | Procedure.md | Step 1, Phase 2 header | -- | Structural Engineer (PROPOSAL) | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Define the internal QC checklist content (Step 14 references it as output but no template or minimum items are listed beyond the narrative) | Process audit lens reveals Step 14 outputs an "Internal QC checklist (completed)" but the checklist items are described only in narrative form. A structured checklist template would make the audit repeatable. | Procedure.md | Step 14 | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service pit depth is essential fact, missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Steel plate dimensions lack adequate evidence |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Standards editions not recorded |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional values stated consistently across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (bay widths, ceiling height, crane capacity) present and consistent |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for structural elements provided adequately |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope, exclusions, and relationships well documented |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency: gantry vs. crane |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering fundamentals assumed via P.Eng. requirement |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. licensure addresses competence |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope of expertise adequately bounded by Standards table |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of structural system consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict Table in Guidance provides human-decision escalation |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable relationships mapped in Datasheet Construction |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning approach consistent across trade-offs and conflict items |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: service pit depth -- essential fact absent from all sources. Confirm with County operations team what minimum pit clearance is required for equipment servicing | Essential fact lens: service pit depth is a critical dimension for structural sections. Datasheet lists "exact depth TBD," Specification R-005 says "Depth shall be determined," Procedure Step 3 lists it as open question. No source provides this fact. | Datasheet.md; Specification.md; Procedure.md | Datasheet Attributes (Service pit row); Specification R-005; Procedure Step 3 | -- | County operations team + Structural Engineer (PROPOSAL) | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: steel plate embedment dimensions (thickness, plan size, anchor type) -- insufficient evidence in any source to determine plate specifications | Adequate evidence lens: Datasheet lists "Steel plate embedments" with "multiple locations per floor plan" but no sizing data. Specification R-008 notes "dimensions and thickness are TBD." Guidance C-03 enumerates five unresolved design questions about plates. | Datasheet.md; Specification.md; Guidance.md | Datasheet Attributes (Steel plate row); Specification R-008 Note; Guidance C-03 | -- | Structural Engineer + County (PROPOSAL) | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add specific code editions and clause references to the Standards table (currently marked as "ASSUMPTION: likely applicable" with no edition identified) | Comprehensive record lens: Datasheet Standards (Inferred) table lists 5 standards, all marked as assumptions without editions. A comprehensive record requires at minimum the edition year and primary applicable clauses. | Datasheet.md | Standards (Inferred -- texts not available) table | -- | Structural Engineer + AHJ (PROPOSAL) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology for overhead crane equipment: use "5-Tonne Overhead Crane" consistently; annotate "Gantry" as the App B alias per Guidance C-04 | Coherent message lens: Datasheet uses "Gantry / Crane" heading with explanation. Guidance C-04 recommends canonical term "5-Tonne Overhead Crane." Specification uses both "overhead cranes on trolley" (R-009) and "crane runway." Procedure uses "crane runway." The terminology is not yet normalized across all documents. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet Gantry/Crane section; Specification R-009; Guidance C-04; Procedure Step 10 | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Threshold | 1 | HAS_ITEMS | Mezzanine live load threshold missing |
| C:normative:sufficiency | normative | sufficiency | Warranted Regulatory Adequacy | 0 | NO_ITEMS | Regulatory adequacy framework present via P.Eng. stamp + AHJ review |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | CSA standard clauses not identified |
| C:normative:consistency | normative | consistency | Standardized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references consistent across documents |
| C:operative:necessity | operative | necessity | Indispensable Functional Capability | 0 | NO_ITEMS | Core production capabilities addressed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Validated Operational Competence | 0 | NO_ITEMS | P.Eng. competence requirement sufficient |
| C:operative:completeness | operative | completeness | Comprehensive Operational Mastery | 1 | HAS_ITEMS | Waterproofing coordination gap |
| C:operative:consistency | operative | consistency | Dependable Process Uniformity | 0 | NO_ITEMS | Process steps consistent in structure and level of detail |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Significance | 0 | NO_ITEMS | Value of deliverable to project objectives stated |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Qualitative Appraisal | 0 | NO_ITEMS | Quality review mechanisms in place |
| C:evaluative:completeness | evaluative | completeness | Definitive Holistic Valuation | 0 | NO_ITEMS | Scope completeness addressed via exclusions list |
| C:evaluative:consistency | evaluative | consistency | Principled Evaluative Consistency | 0 | NO_ITEMS | Evaluation criteria consistent across verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add explicit acceptance criterion for mezzanine design live load value (e.g., minimum kPa/psf per NBCC Table 4.1.5.3 storage occupancy) once the load is established | Enforceable Compliance Threshold lens: R-006 requires the mezzanine to support "heavy items including oil totes and pumping equipment" but no numeric threshold is stated. Verification table for R-006 says "design live load noted on drawings or in calculation package" but does not define what value would satisfy the requirement. Without a threshold, compliance cannot be enforced. | Specification.md | R-006; Verification table R-006 row | -- | Structural Engineer + Owner (PROPOSAL) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add clause-level references for CSA A23.3 and CSA S16 applicable to this deliverable's structural elements once standard texts are available | Exhaustive Regulatory Coverage lens: Standards table lists CSA A23.3 and CSA S16 as "ASSUMPTION: applicable" without identifying which clauses govern the specific structural elements (e.g., concrete shear wall design, crane runway fatigue, mezzanine connection capacity). Regulatory coverage is incomplete without clause-level identification. | Specification.md | Standards table | -- | Structural Engineer (PROPOSAL) | TBD |
| C-003 | C:operative:completeness | RationaleGap | Guidance | Guidance | Add rationale for waterproofing and drainage interface responsibilities: clarify which discipline owns the waterproofing design and how structural sections must accommodate it | Comprehensive Operational Mastery lens: Guidance P-04 notes the service pit "must include provision for waterproofing membrane interface details (typically coordinated with architectural or civil)" but does not clarify responsibility boundaries. Procedure Step 7 mentions "waterproofing interface" as a drawing element but not who provides the design input. Complete operational mastery requires clear discipline responsibility. | Guidance.md; Procedure.md | Guidance P-04; Procedure Step 7 | -- | Design-Builder to assign discipline responsibility (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Conformance Assurance | 1 | HAS_ITEMS | County approval gate not verified |
| F:normative:sufficiency | normative | sufficiency | Verified Prescriptive Authority | 0 | NO_ITEMS | P.Eng. authority chain established |
| F:normative:completeness | normative | completeness | Exhaustive Mandate Fulfillment | 1 | HAS_ITEMS | R-011 coordination verification weak |
| F:normative:consistency | normative | consistency | Harmonized Prescriptive Rigor | 0 | NO_ITEMS | Requirements consistently cite RFP sources |
| F:operative:necessity | operative | necessity | Verified Functional Imperative | 1 | HAS_ITEMS | Crane supplier dependency unresolved |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Competence | 0 | NO_ITEMS | Procedure demonstrates competent sequencing |
| F:operative:completeness | operative | completeness | Exhaustive Operational Authority | 0 | NO_ITEMS | Steps cover all identified structural elements |
| F:operative:consistency | operative | consistency | Systematic Performance Reliability | 0 | NO_ITEMS | Step structure is consistent (output defined for each) |
| F:evaluative:necessity | evaluative | necessity | Definitive Merit Recognition | 0 | NO_ITEMS | Project objectives (OBJ-001, OBJ-003) linked to deliverable |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Judgment | 0 | NO_ITEMS | Trade-offs substantiated with rationale |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal Authority | 1 | HAS_ITEMS | No drawing completeness acceptance criterion |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Coherence | 0 | NO_ITEMS | Evaluation criteria consistent between Spec and Procedure verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Procedure | Add verification step confirming County approval of DEL-002-01 is documented before Phase 2 detail drawing commences (R-012 verification says "project record" but Procedure has no explicit gate) | Obligatory Conformance Assurance lens: R-012 requires County approval of preliminary design before IFC, and verification says "County approval of DEL-002-01 documented prior to IFC issue." But Procedure lists this only as a prerequisite table entry, not as a Phase 1 hold-point with a verification action. The assurance mechanism is weak. | Specification.md; Procedure.md | Specification Verification R-012; Procedure Prerequisites table | -- | Structural Engineer + Project Manager (PROPOSAL) | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Strengthen verification approach for R-011 (multi-discipline coordination): add specific acceptance criteria such as "all structural penetrations >X diameter have corresponding sleeves shown" or "BIM clash detection report attached" | Exhaustive Mandate Fulfillment lens: R-011 verification says "BIM/CAD overlay or discipline cross-check during IFC issue; penetration sleeves shown." This is aspirational but lacks measurable pass/fail criteria. Exhaustive mandate fulfillment requires verifiable acceptance thresholds. | Specification.md | Verification table R-011 row | -- | Design-Builder coordination lead (PROPOSAL) | TBD |
| F-003 | F:operative:necessity | TBD_Question | Multi | Guidance | Record TBD: crane supplier/manufacturer identity and runway requirements -- this external dependency blocks final detailing of crane support structure but no fallback or provisional design approach is documented | Verified Functional Imperative lens: Procedure lists "Crane supplier/manufacturer information" as a prerequisite and Step 3 reiterates it. Guidance P-05 explains the dependency. However, no document provides a fallback strategy if the crane supplier is not confirmed before the drawing deadline. The functional imperative (producing IFC drawings by Dec 2026) may be at risk. | Procedure.md; Guidance.md | Procedure Prerequisites (Crane supplier row); Guidance P-05 | -- | Design-Builder procurement (PROPOSAL) | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add a drawing completeness acceptance criterion: define what constitutes a "complete" DEL-002-04 set (e.g., minimum sheet types, all section cuts from DEL-002-03 have corresponding sheets, all R-001 through R-012 elements present) | Comprehensive Appraisal Authority lens: Specification Documentation section lists anticipated artifacts and sheet types (ASSUMPTION) but does not define an acceptance criterion for completeness. Without a definition of "complete," appraisal of the deliverable's readiness is subjective. | Specification.md | Documentation section | -- | Structural Engineer (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Commanding Conformance Directive | 1 | HAS_ITEMS | Geotechnical report dependency |
| D:normative:applying | normative | applying | Enforced Compulsory Protocol | 0 | NO_ITEMS | P.Eng. stamp protocol enforced in Procedure Step 16 |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 1 | HAS_ITEMS | No single conformance sign-off gate |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Inspection | 0 | NO_ITEMS | AHJ inspection addressed in verification |
| D:operative:guiding | operative | guiding | Resolved Methodological Guidance | 1 | HAS_ITEMS | Two-stage issue approach not proceduralized |
| D:operative:applying | operative | applying | Validated Effective Implementation | 0 | NO_ITEMS | Implementation steps validated by outputs at each step |
| D:operative:judging | operative | judging | Definitive Execution Evaluation | 0 | NO_ITEMS | Verification checklist covers execution evaluation |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Stability | 0 | NO_ITEMS | Workflow sequence logical and stable |
| D:evaluative:guiding | evaluative | guiding | Confirmed Worthiness Direction | 0 | NO_ITEMS | Purpose section in Guidance establishes worthiness |
| D:evaluative:applying | evaluative | applying | Validated Quality Implementation | 0 | NO_ITEMS | QC process in Steps 14-16 validates quality |
| D:evaluative:judging | evaluative | judging | Definitive Value Ruling | 0 | NO_ITEMS | P.Eng. stamp is the definitive value ruling |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Inspection | 1 | HAS_ITEMS | Guarantee period record retention lacks verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | RationaleGap | Guidance | Guidance | Add guidance on how geotechnical report findings should inform structural section details (e.g., soil bearing capacity affects service pit wall design, foundation interface details) | Commanding Conformance Directive lens: Procedure lists geotechnical report as a prerequisite and Datasheet notes "normal ground conditions assumed." However, Guidance does not explain how geotech findings translate into section detail decisions. The conformance directive (design to actual site conditions) lacks interpretive guidance. | Guidance.md; Datasheet.md; Procedure.md | Guidance (entire -- no geotech interpretation section); Datasheet Conditions (Foundation pricing row); Procedure Prerequisites (Geotech row) | -- | Structural Engineer (PROPOSAL) | TBD |
| D-002 | D:normative:judging | VerificationGap | Specification | Specification | Add a single conformance sign-off record: a checklist or sign-off sheet confirming all 12 requirements (R-001 through R-012) have been verified before IFC stamp | Definitive Conformance Ruling lens: Verification table lists individual verification approaches per requirement, but there is no aggregating sign-off mechanism to confirm all requirements are satisfied collectively. A definitive ruling requires a single point of conformance confirmation. | Specification.md | Verification table (entire) | -- | P.Eng. of record (PROPOSAL) | TBD |
| D-003 | D:operative:guiding | RationaleGap | Guidance | Guidance | Expand Trade-off T-02 (Early vs. Late Detail Finalization) into an actionable decision framework: specify which elements can proceed and which must wait for external inputs, with a suggested phasing plan | Resolved Methodological Guidance lens: Guidance T-02 describes the early-vs-late trade-off in general terms but does not resolve it into a recommended phasing approach. Procedure Step 3 lists open questions but does not sequence them against the Phase 2 drawing steps. Methodological guidance is not fully resolved. | Guidance.md; Procedure.md | Guidance T-02; Procedure Step 3, Phase 2 steps | -- | Structural Engineer (PROPOSAL) | TBD |
| D-004 | D:evaluative:reviewing | WeakStatement | Procedure | Procedure | Clarify record retention requirement: "min. 2 years post-CCC" is cited from R-01 section 2.10 but the guarantee period length is stated as assumption; confirm actual contractual guarantee period | Resolved Merit Inspection lens: Procedure Records table states retention for "project duration + Guarantee Period (min. 2 years post-CCC) per R-01 section 2.10." The phrase "min. 2 years" suggests uncertainty about the actual guarantee period. If the contract specifies a different period, records could be prematurely disposed. | Procedure.md | Records table | -- | Contract administrator (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Critical Directional Assurance | 0 | NO_ITEMS | Guidance provides critical direction for all key elements |
| X:guiding:sufficiency | guiding | sufficiency | Justified Guidance Competence | 1 | HAS_ITEMS | Guidance Examples section empty |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Authority | 0 | NO_ITEMS | Guidance covers all identified structural elements with principles and considerations |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Stability | 0 | NO_ITEMS | Guidance internally consistent |
| X:applying:necessity | applying | necessity | Validated Practical Imperative | 1 | HAS_ITEMS | Cross-reference management not proceduralized |
| X:applying:sufficiency | applying | sufficiency | Justified Implementation Scope | 0 | NO_ITEMS | Implementation scope justified by requirement traceability |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Revision management not addressed |
| X:applying:consistency | applying | consistency | Reliable Implementation Harmony | 0 | NO_ITEMS | Step outputs consistent in form |
| X:judging:necessity | judging | necessity | Binding Decisional Certainty | 1 | HAS_ITEMS | No verification of foundation interface |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudicative Scope | 0 | NO_ITEMS | Verification scope covers all requirements |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Record | 0 | NO_ITEMS | Verification table is comprehensive |
| X:judging:consistency | judging | consistency | Stable Adjudicative Coherence | 0 | NO_ITEMS | Verification approaches consistent in rigor |
| X:reviewing:necessity | reviewing | necessity | Critical Examination Certainty | 1 | HAS_ITEMS | Multi-discipline review scope unclear |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Examination Adequacy | 0 | NO_ITEMS | Examination steps adequate in Procedure |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Coverage | 0 | NO_ITEMS | Examination covers all phases |
| X:reviewing:consistency | reviewing | consistency | Stable Examination Alignment | 0 | NO_ITEMS | Review alignment stable across QC and P.Eng. stages |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Guidance | Guidance | Populate Examples section with reference to comparable project types or detail precedent sources, or explicitly state that no examples are available and what should be consulted | Justified Guidance Competence lens: Guidance Examples section states "TBD -- No example drawings are available in accessible sources." For guidance to be competently justified, the absence should be explicitly managed -- either by pointing to external resources the Structural Engineer should consult or by noting this as a known limitation. | Guidance.md | Examples section | -- | Structural Engineer (PROPOSAL) | TBD |
| X-002 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add a step or sub-step for managing cross-references between DEL-002-04 and companion deliverables (DEL-002-05 through DEL-002-09): confirm all cross-reference callouts are bidirectional and consistent | Validated Practical Imperative lens: Procedure Steps 7-12 each mention cross-references to companion deliverables but no step consolidates cross-reference verification. Given that sections may appear in this deliverable or in dedicated deliverables, a cross-reference reconciliation step is a practical imperative. | Procedure.md | Steps 7-12 (cross-reference mentions); Step 14 (QC) | -- | Structural Engineer (PROPOSAL) | TBD |
| X-003 | X:applying:completeness | MissingSlot | Multi | Specification | Add revision management requirement: define how drawing revisions are tracked, numbered, and reconciled across the PKG-002 set (currently no requirement or procedure step addresses revision control) | Exhaustive Implementation Record lens: Procedure Step 17 mentions "IFC revision designation (e.g., Rev. 0 IFC)" but no requirement in Specification governs revision numbering, revision tracking, or revision history documentation. For an exhaustive implementation record, revision management must be defined. | Specification.md; Procedure.md | Procedure Step 17; Specification (entire -- no revision management requirement) | -- | Structural Engineer + Project Manager (PROPOSAL) | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add verification approach for foundation interface condition: confirm that top-of-foundation elevation and interface details shown in structural sections match DEL-002-02 Foundation Plan | Binding Decisional Certainty lens: Guidance C-05 explicitly states the foundation interface "must be explicitly cross-referenced between the two deliverables." Specification has no requirement or verification entry for this interface. Without this verification, a binding decision on interface completeness cannot be made. | Specification.md; Guidance.md | Specification Verification table (no entry); Guidance C-05 | -- | Structural Engineer (PROPOSAL) | TBD |
| X-005 | X:reviewing:necessity | WeakStatement | Procedure | Procedure | Clarify scope of multi-discipline coordination review (Step 15): specify which specific interfaces must be reviewed per discipline (e.g., mechanical -- duct penetrations through structural walls; electrical -- conduit sleeves; plumbing -- floor drains in service pit) | Critical Examination Certainty lens: Step 15 says "Distribute draft drawing set to Architectural, Mechanical, Electrical, and Plumbing disciplines" but does not specify what each discipline is expected to review or what constitutes a satisfactory response. Examination certainty requires defined scope. | Procedure.md | Step 15 | -- | Design-Builder coordination lead (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Orientation Foundation | 1 | HAS_ITEMS | Datasheet missing elevation data |
| E:guiding:information | guiding | information | Contextualized Orientation Signal | 0 | NO_ITEMS | Context signals (building geometry, structural system, key components) present |
| E:guiding:knowledge | guiding | knowledge | Authoritative Orientation Mastery | 0 | NO_ITEMS | Guidance demonstrates authoritative understanding of structural detail requirements |
| E:guiding:wisdom | guiding | wisdom | Principled Orientation Vision | 0 | NO_ITEMS | Principles P-01 through P-06 provide principled vision |
| E:applying:data | applying | data | Demonstrated Execution Foundation | 1 | HAS_ITEMS | No loading data for steel plate embedments |
| E:applying:information | applying | information | Contextualized Execution Account | 0 | NO_ITEMS | Procedure steps contextualize execution adequately |
| E:applying:knowledge | applying | knowledge | Authoritative Execution Capability | 0 | NO_ITEMS | P.Eng. requirement ensures authoritative capability |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Trade-offs provide principled judgment framework |
| E:judging:data | judging | data | Demonstrated Verdict Foundation | 0 | NO_ITEMS | Verification data requirements defined in pass conditions |
| E:judging:information | judging | information | Contextualized Verdict Account | 0 | NO_ITEMS | Verification approaches contextualized per requirement |
| E:judging:knowledge | judging | knowledge | Authoritative Verdict Mastery | 0 | NO_ITEMS | P.Eng. and AHJ authority established |
| E:judging:wisdom | judging | wisdom | Principled Verdict Discernment | 0 | NO_ITEMS | Conflict escalation to human ruling preserves principled discernment |
| E:reviewing:data | reviewing | data | Verified Audit Foundation | 1 | HAS_ITEMS | Transmittal record content not defined |
| E:reviewing:information | reviewing | information | Contextualized Audit Account | 0 | NO_ITEMS | Records table provides audit context |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Audit Mastery | 0 | NO_ITEMS | QC and P.Eng. review provide authoritative audit |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Discernment | 0 | NO_ITEMS | Audit principles embedded in verification approach |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Add reference elevations to Datasheet Attributes: top-of-slab elevation, mezzanine floor elevation, crane runway beam elevation (relative to a project datum) to provide orientation foundation data for section drawings | Verified Orientation Foundation lens: Datasheet Attributes provide horizontal dimensions (bay widths, footprint) and clear height (35 ft) but no vertical elevation data. Structural sections require reference elevations. Specification and Procedure reference these implicitly (crane runway elevation in Step 6, mezzanine floor level) but no numeric elevation values exist in any document. | Datasheet.md | Attributes -- Building Geometry table | -- | Structural Engineer (PROPOSAL) | TBD |
| E-002 | E:applying:data | WeakStatement | Datasheet | Datasheet | Clarify steel plate embedment loading basis: state what equipment types and wheel/track loads the plates must resist, so that the execution data foundation for plate design is explicit | Demonstrated Execution Foundation lens: Datasheet states "steel plates embedded at strategic locations for tracked/packer heavy equipment" and Guidance C-03 notes key design questions are unresolved. The equipment types that drive plate design (compactor, motor grader, etc.) are referenced indirectly but the loading basis is absent. Execution cannot be demonstrated without design input data. | Datasheet.md; Guidance.md | Datasheet Attributes (Steel plate row); Guidance C-03 | -- | County operations team (PROPOSAL) | TBD |
| E-003 | E:reviewing:data | Normalization | Procedure | Procedure | Define minimum content for the drawing transmittal record (Step 17): specify what information must be captured (e.g., sheet list, revision status, recipient, date, method of transmission) to ensure audit foundation data is complete | Verified Audit Foundation lens: Procedure Records table lists "Drawing transmittal record" as "Evidence of IFC issue date and recipients" but Step 17 says only "transmittal record" without defining content. For the audit foundation to be verified, the minimum content of this record should be explicit. | Procedure.md | Records table (Drawing transmittal record row); Step 17 | -- | Project Manager (PROPOSAL) | TBD |
