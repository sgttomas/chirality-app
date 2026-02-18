# Semantic Lensing Register: DEL-04-03 Cold Storage -- Floor & Foundation (DB Proposed)

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-004_Cold Storage Building (Unheated, 60'x100')/1_Working/DEL-04-03_Cold Storage - Floor & Foundation (DB Proposed)/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-04-03 context (Name, Package, Discipline, Scope Coverage SOW-0303/SOW-0304, DEC-002/DEC-003)
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (92 cells total)
- Datasheet.md -- Present (Identification, Attributes, Conditions, Construction, References)
- Specification.md -- Present (Scope, Requirements REQ-01 through REQ-13, Standards, Verification, Documentation)
- Guidance.md -- Present (Purpose, Principles, Considerations, Trade-offs, Examples, Conflict Table)
- Procedure.md -- Present (Purpose, Prerequisites, Steps Phase A and B, Verification, Records)
- _REFERENCES.md -- Present (OSR, Geotechnical Investigation Report)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 4
  - Procedure: 2
  - Multi: 4
- By matrix:
  - A: 5  B: 5  C: 3  F: 3  D: 3  X: 5  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Design life not stated for ancillary building |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Seismic design practice gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC edition not specified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately covered by REQ-13 sealed documents and geotech certification |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase A/B provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Compaction testing frequency incomplete |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered through Verification tables in Spec and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit addressed via geotech certification and sealed document checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Design life for ancillary building missing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit criteria implicitly addressed through cost-effectiveness guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination addressed through trade-offs in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by Procedure verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: What is the design life for the ancillary cold storage building? Main building = 50 years but ancillary not stated. | Datasheet notes "TBD" for design life of ancillary building; this parameter governs foundation durability, material selection, and lifecycle cost assessment but has no stated value. | Datasheet.md | Attributes > Building Context > "Design life (ancillary)" | -- | PROPOSAL: Owner to confirm | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement or note addressing seismic design loads for the cold storage building foundation per Seismic Site Class C. | Guidance mentions seismic site class C and states structural design must incorporate seismic loads, but Specification has no requirement addressing seismic design. REQ-01 mentions "code-compliant" generically but no explicit seismic requirement exists. | Specification.md | Requirements (all REQ scanned) | -- | PROPOSAL: Specification | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify which edition of the Alberta Building Code (ABC) governs; current Standards table says "current edition" with "ASSUMPTION: likely applicable; location TBD." | The governing code edition is unresolved. Specification Standards table flags ABC as assumption. Compliance determination cannot be definitive without knowing the governing code edition. | Specification.md | Standards table > "Alberta Building Code" | -- | PROPOSAL: Owner/DB to confirm ABC edition | TBD |
| A-004 | A:operative:applying | VerificationGap | Procedure | Procedure | Add compaction testing frequency for subgrade (not just structural fill) in Step B3. Currently only fill testing frequency is stated (1 test per lift per 500 m2). | Procedure Step B3 specifies compaction testing frequency for structural fill but does not specify testing frequency for the initial exposed subgrade compaction. | Procedure.md | Steps > Phase B > Step B3 | -- | PROPOSAL: Procedure | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale explaining how design life assumptions affect foundation and floor system selection for the ancillary building. | Guidance discusses cost-effectiveness and geotechnical constraints but does not address how the unknown design life of the ancillary building should influence the DB's system selection or lifecycle cost assessment. | Guidance.md | Considerations / Trade-offs | -- | PROPOSAL: Guidance | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Floor load design basis missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Borehole applicability to cold storage footprint |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Radon mitigation not in Specification |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement data from geotech report consistently referenced across documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Equipment/vehicle loads not characterized |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for foundation selection is adequately provided across Guidance and Datasheet |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of soil conditions is comprehensive across Datasheet |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging on geotech constraints is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of frost design, bearing strata, and sulphate exposure is consistently communicated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements (geotech, structural P.Eng.) adequately specified |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 1 | HAS_ITEMS | Post-and-frame structural basis not elaborated |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of geotech principles is coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment points (frost risk, cost balance) are well surfaced in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance in Guidance trade-offs is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight provided through Examples and Trade-offs in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles (geotech governs, cost-effectiveness, one foundation type) are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add expected floor live loads (equipment/vehicle loads) for the cold storage building to enable floor system design. | The Datasheet describes the building use as "seasonal equipment/materials/supplies storage" but no floor live load design basis (kPa or psf) is stated anywhere in the 4 documents. This is an essential fact for floor system sizing. | Datasheet.md | Attributes > Building Context | -- | PROPOSAL: DB structural engineer to establish; Owner to confirm equipment types | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Specification | Clarify whether existing borehole data (BH101-BH116) is sufficient for the cold storage building footprint or whether additional investigation is expected. | Datasheet and Specification note boreholes from the main site but REQ-03 includes an ASSUMPTION that the cold storage footprint is on the same site. The statement hedges but does not clearly direct the DB on when additional investigation is required vs. optional. | Specification.md | REQ-03 > ASSUMPTION | -- | PROPOSAL: Specification (clarify trigger for additional investigation) | TBD |
| B-003 | B:data:completeness | MissingSlot | Specification | Specification | Add radon mitigation requirement or explicit exclusion for the cold storage building. Guidance mentions radon sump recommendation but Specification has no REQ for it. | Guidance and Procedure both reference radon mitigation (sump + collection system per Geotech Report section 7.1 item 5), but no requirement in Specification addresses radon. This is either a missing requirement or a conscious exclusion that should be documented. | Specification.md; Guidance.md | Specification: entire Requirements section scanned; Guidance: Considerations > Floor Option Assessment | -- | PROPOSAL: Specification or explicit exclusion note | TBD |
| B-004 | B:information:necessity | TBD_Question | Multi | Datasheet | Record TBD: What specific equipment types and vehicle weights will operate inside the cold storage building? This determines floor load design. | Multiple documents reference "equipment storage" and "service vehicle loads" for apron design (REQ-06) but no specific vehicle or equipment weights are provided. Both floor and apron design require this input. | Datasheet.md; Specification.md | Datasheet: Attributes > Building Context > Use; Specification: REQ-06 | -- | PROPOSAL: Owner to provide equipment inventory or load class | TBD |
| B-005 | B:knowledge:completeness | RationaleGap | Guidance | Guidance | Add discussion of post-and-frame/pole shed structural code compliance path, since this is the Owner-cited example but its ABC compliance basis is marked as ASSUMPTION. | Guidance Considerations mention post-and-frame construction and note its ABC compliance as an ASSUMPTION. For an Owner-cited example, the Guidance should explain the structural code compliance pathway or flag it as requiring confirmation during design. | Guidance.md | Considerations > Foundation Option Assessment > Post-and-Frame | -- | PROPOSAL: Guidance | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Requirement Basis | 1 | HAS_ITEMS | Settlement tolerance not in Spec for piles |
| C:normative:sufficiency | normative | sufficiency | Regulatory Adequacy Threshold | 0 | NO_ITEMS | Regulatory adequacy thresholds for concrete, compaction, frost depth are all stated |
| C:normative:completeness | normative | completeness | Mandated Scope Assurance | 1 | HAS_ITEMS | Scope boundary with DEL-03-02 drainage |
| C:normative:consistency | normative | consistency | Regulatory Alignment Integrity | 0 | NO_ITEMS | Regulatory references are consistent across docs (same geotech report sections, same OSR sections) |
| C:operative:necessity | operative | necessity | Critical Execution Prerequisite | 0 | NO_ITEMS | Prerequisites listed in Procedure are comprehensive for both phases |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Execution Readiness | 0 | NO_ITEMS | Readiness criteria addressed through Prerequisites section |
| C:operative:completeness | operative | completeness | Exhaustive Process Accounting | 0 | NO_ITEMS | Process steps cover full lifecycle from proposal through closeout |
| C:operative:consistency | operative | consistency | Stable Process Discipline | 0 | NO_ITEMS | Process discipline maintained through consistent geotech certification requirements |
| C:evaluative:necessity | evaluative | necessity | Essential Worth Foundation | 1 | HAS_ITEMS | Evaluation scoring criteria absent |
| C:evaluative:sufficiency | evaluative | sufficiency | Competent Worth Verification | 0 | NO_ITEMS | Worth verification delegated to proposal evaluation process |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Assessment | 0 | NO_ITEMS | Trade-off table in Guidance provides holistic assessment framework |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Coherence | 0 | NO_ITEMS | Worth principles (cost-effectiveness, geotech compliance) consistently threaded |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add settlement tolerance criterion for pile-supported foundations (REQ-10 addresses void space but not settlement limits). Shallow footings have 25 mm SLS limit per Procedure Step A5; piles have no stated limit. | Specification REQ-10 addresses void space under pile-supported structures but does not state a settlement tolerance for pile foundations. Procedure Step A5 mentions 25 mm for shallow footings. This creates an asymmetric enforceable basis depending on foundation type. | Specification.md; Procedure.md | Specification: REQ-10; Procedure: Step A5 | -- | PROPOSAL: Specification | TBD |
| C-002 | C:normative:completeness | Normalization | Multi | Multi | Clarify scope boundary between DEL-04-03 (drainage around cold storage building) and DEL-03-02 (site grading/drainage). REQ-12 and Procedure Step B7 address drainage at the building, but site civil drainage is out of scope per Specification. | Specification REQ-12 requires positive drainage around the cold storage building and Procedure Step B7 details execution. But Specification Out of Scope says "Site civil earthworks and grading (covered by DEL-03-02)." The boundary between building-perimeter drainage (this deliverable) and site drainage (DEL-03-02) is not explicitly delineated. | Specification.md; Procedure.md | Specification: Scope > Out of Scope; REQ-12; Procedure: Step B7 | -- | PROPOSAL: Specification scope clarification | TBD |
| C-003 | C:evaluative:necessity | MissingSlot | Specification | Guidance | Add note on how the proposal will be evaluated/scored for the floor and foundation selection. The evaluation criteria that the Owner will use are not referenced. | Guidance discusses what the evaluator is "likely to score favourably" but no document references actual RFP evaluation criteria or weighting for the foundation/floor proposal. This is an essential worth foundation that the DB needs to optimize their proposal. | Guidance.md | Considerations > Foundation Option Assessment; Trade-offs | -- | PROPOSAL: Guidance (reference evaluation criteria if available) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Conformance Foundation | 0 | NO_ITEMS | Conformance foundation is well-established through REQ-01 to REQ-13 |
| F:normative:sufficiency | normative | sufficiency | Codified Compliance Benchmark | 1 | HAS_ITEMS | Concrete slab thickness not specified |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Regulatory coverage is comprehensive; standards table lists all applicable codes |
| F:normative:consistency | normative | consistency | Integrated Conformance Standard | 0 | NO_ITEMS | Standards references are consistent across documents |
| F:operative:necessity | operative | necessity | Foundational Operational Proof | 1 | HAS_ITEMS | Proof roll acceptance criteria missing |
| F:operative:sufficiency | operative | sufficiency | Verified Procedural Competence | 0 | NO_ITEMS | Procedural competence requirements (P.Eng., geotech) adequately specified |
| F:operative:completeness | operative | completeness | Comprehensive Procedural Mastery | 0 | NO_ITEMS | Procedure covers full scope from proposal through construction |
| F:operative:consistency | operative | consistency | Principled Procedural Uniformity | 0 | NO_ITEMS | Procedural steps are internally consistent |
| F:evaluative:necessity | evaluative | necessity | Indispensable Merit Basis | 0 | NO_ITEMS | Merit basis established through cost-effectiveness principle and geotech compliance |
| F:evaluative:sufficiency | evaluative | sufficiency | Verified Valuation Capacity | 1 | HAS_ITEMS | Lifecycle cost comparison not structured |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Valuation Scope | 0 | NO_ITEMS | Valuation scope covered through trade-off table in Guidance |
| F:evaluative:consistency | evaluative | consistency | Integrated Valuation Standard | 0 | NO_ITEMS | Valuation standards consistent (cost-effectiveness framed throughout) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Add minimum concrete slab thickness requirement or explicitly delegate to DB structural engineer. REQ-08 specifies subgrade prep but not slab thickness. | Specification REQ-07 and REQ-08 detail concrete mix and subgrade prep but no requirement states minimum slab thickness for the grade-supported slab or aprons. This is a codified compliance benchmark that is absent. | Specification.md | REQ-07, REQ-08 | -- | PROPOSAL: Specification or delegate to structural engineer with minimum stated | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Specification | Add acceptance criteria for proof roll (Step B3 says "observe and respond to soft/yielding areas" but provides no pass/fail criterion). | Procedure Step B3 mentions proof rolling but the acceptance criterion is qualitative ("observe and respond") rather than quantitative. This makes verification of this foundational operational step ambiguous. | Procedure.md | Steps > Phase B > Step B3 | -- | PROPOSAL: Specification (add proof roll acceptance criterion) | TBD |
| F-003 | F:evaluative:sufficiency | MissingSlot | Guidance | Guidance | Add structured lifecycle cost comparison framework for foundation and floor options to support DB's cost-effectiveness argument. | Guidance Trade-offs discuss cost qualitatively ("lower cost," "higher cost") but no structured comparison framework (e.g., estimated relative cost ranges, lifecycle factors) is provided. The Owner explicitly values cost-effectiveness (Principle 4). | Guidance.md | Trade-offs | -- | PROPOSAL: Guidance | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Compliance Authority | 0 | NO_ITEMS | Compliance authority clearly established through geotech report and ABC references |
| D:normative:applying | normative | applying | Enforced Conformance Practice | 1 | HAS_ITEMS | Concrete curing specification absent |
| D:normative:judging | normative | judging | Authoritative Coverage Ruling | 0 | NO_ITEMS | Coverage ruling adequately addressed through verification tables |
| D:normative:reviewing | normative | reviewing | Statutory Alignment Verification | 0 | NO_ITEMS | Statutory alignment verified through sealed documents requirement |
| D:operative:guiding | operative | guiding | Evidence-Grounded Method Guidance | 0 | NO_ITEMS | Method guidance well-grounded in geotech evidence throughout |
| D:operative:applying | operative | applying | Settled Competence Deployment | 0 | NO_ITEMS | Competence deployment addressed through P.Eng. and geotech retention requirements |
| D:operative:judging | operative | judging | Settled Capability Judgment | 0 | NO_ITEMS | Capability judgment addressed through verification checks |
| D:operative:reviewing | operative | reviewing | Systematic Uniformity Review | 1 | HAS_ITEMS | Internal consistency review checklist incomplete |
| D:evaluative:guiding | evaluative | guiding | Settled Worth Direction | 0 | NO_ITEMS | Worth direction settled through cost-effectiveness principle |
| D:evaluative:applying | evaluative | applying | Enacted Appraisal Deployment | 0 | NO_ITEMS | Appraisal deployment addressed through trade-offs and examples |
| D:evaluative:judging | evaluative | judging | Definitive Merit Ruling | 1 | HAS_ITEMS | No evaluation scoring weights referenced |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Coherence Review | 0 | NO_ITEMS | Quality coherence review addressed through proposal consistency check (Step A7) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add concrete curing requirements or reference to curing standard. Procedure Step B6 says "Cure concrete per specification" but no specification requirement addresses curing. | Procedure Step B6 states "Cure concrete per specification" but Specification REQ-07 does not include curing requirements. This creates a circular reference with no enforceable curing standard. | Specification.md; Procedure.md | Specification: REQ-07; Procedure: Step B6 | -- | PROPOSAL: Specification REQ-07 | TBD |
| D-002 | D:operative:reviewing | MissingSlot | Procedure | Procedure | Add cross-deliverable consistency check with DEL-04-04 (electrical/ventilation) to Step A7 internal consistency review. | Procedure Step A7 lists consistency checks with DEL-04-01, DEL-04-02, and DEL-03-02 but omits DEL-04-04 (Cold Storage Electrical & Ventilation). Floor penetrations, conduit routing, or ventilation openings could affect floor/foundation design. | Procedure.md | Steps > Phase A > Step A7 | -- | PROPOSAL: Procedure | TBD |
| D-003 | D:evaluative:judging | TBD_Question | Multi | Guidance | Record TBD: What are the RFP evaluation scoring criteria and weights for the cold storage foundation/floor proposal? Guidance references evaluator preferences but no scoring framework is cited. | Guidance states the evaluator is "likely to score proposals favourably" for certain attributes, but no actual evaluation criteria or weighting from the RFP are referenced. The DB needs this to optimize proposal merit. | Guidance.md | Principles > Principle 4; Trade-offs | -- | PROPOSAL: Reference RFP evaluation criteria if accessible | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Guidance Foundation | 0 | NO_ITEMS | Guidance foundation well-established through 5 principles |
| X:guiding:sufficiency | guiding | sufficiency | Verified Governance Readiness | 1 | HAS_ITEMS | Screw pile torque-to-capacity correlation not addressed |
| X:guiding:completeness | guiding | completeness | Total Governance Scope | 0 | NO_ITEMS | Governance scope comprehensive across standards, geotech, and OSR |
| X:guiding:consistency | guiding | consistency | Unified Governance Integrity | 0 | NO_ITEMS | Governance references unified across documents |
| X:applying:necessity | applying | necessity | Mandatory Deployment Condition | 1 | HAS_ITEMS | Screw pile installation verification gap |
| X:applying:sufficiency | applying | sufficiency | Verified Deployment Adequacy | 0 | NO_ITEMS | Deployment adequacy addressed through verification tables |
| X:applying:completeness | applying | completeness | Total Deployment Coverage | 1 | HAS_ITEMS | Concrete joint spacing not specified |
| X:applying:consistency | applying | consistency | Standardized Deployment Discipline | 0 | NO_ITEMS | Deployment discipline consistent across Procedure steps |
| X:judging:necessity | judging | necessity | Binding Adjudication Basis | 1 | HAS_ITEMS | Conflict between geotech warning and OSR pole shed example |
| X:judging:sufficiency | judging | sufficiency | Sufficient Verdict Standard | 0 | NO_ITEMS | Verdict standards for each REQ adequately paired with verification approaches |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all 13 requirements |
| X:judging:consistency | judging | consistency | Principled Verdict Integrity | 0 | NO_ITEMS | Verdict principles consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Verification timing gap for proposal-stage vs post-award |
| X:reviewing:sufficiency | reviewing | sufficiency | Verified Examination Benchmark | 0 | NO_ITEMS | Examination benchmarks stated for compaction, mix design, etc. |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Coverage | 0 | NO_ITEMS | Audit coverage spans proposal through closeout |
| X:reviewing:consistency | reviewing | consistency | Unified Audit Discipline | 0 | NO_ITEMS | Audit discipline unified across Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add verification approach for screw pile installation capacity (e.g., torque-to-capacity correlation or load testing). Specification verification table for REQ-02 references only embedment depth, not installed capacity confirmation. | Specification verification for REQ-02 (frost design) checks pile embedment length but does not address how installed pile capacity will be verified. Screw pile capacity depends on installation torque and soil conditions at the helix, not just depth. | Specification.md | Verification > REQ-02 | -- | PROPOSAL: Specification verification table | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add screw pile installation monitoring requirements (torque monitoring, advancement rate) to verification approach or reference to Procedure Step B5. | Procedure Step B5 mentions matching helix pitch to advancement rate and geotech review of designs, but Specification verification table for REQ-02 does not reference installation monitoring as a verification method. The deployment condition for screw piles lacks a mandatory verification linkage. | Specification.md; Procedure.md | Specification: Verification > REQ-02; Procedure: Step B5 | -- | PROPOSAL: Specification | TBD |
| X-003 | X:applying:completeness | WeakStatement | Procedure | Specification | Add concrete control joint spacing requirement or reference standard for saw-cut joints. Procedure Step B6 says "Saw-cut control joints" but no spacing or timing is specified. | Procedure Step B6 mentions saw-cutting control joints but provides no spacing, timing, or standard reference. Specification REQ-07/REQ-08 do not address joint layout either. Without this, the deployment coverage for concrete placement is incomplete. | Procedure.md; Specification.md | Procedure: Step B6; Specification: REQ-07, REQ-08 | -- | PROPOSAL: Specification or Procedure | TBD |
| X-004 | X:judging:necessity | Conflict | Multi | NA | Surface conflict: Geotech Report warns against unheated on-grade/shallow-foundation construction; OSR cites pole shed (typically shallow-founded) as cost-effective example. Guidance CONF-001 captures this. Confirm CONF-001 human ruling is obtained before proposal finalization. | This is the central adjudication challenge for this deliverable. Guidance Conflict Table CONF-001 correctly identifies this tension and proposes interpretation, but human ruling is TBD. The binding adjudication basis depends on resolution. | Guidance.md; Datasheet.md | Guidance: Conflict Table > CONF-001; Datasheet: Conditions > "No foundation type prescribed" | Guidance.md#Conflict Table > CONF-001 (Geotech Report section 5 item 2) vs Datasheet.md#Conditions > OSR section 10.3.6 | PROPOSAL: Per Guidance CONF-001 proposed interpretation | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add verification distinction between proposal-stage and post-award verification. Current verification table mixes both phases without clear timing markers. | Specification verification table does not consistently distinguish between proposal-stage verification (document review) and post-award verification (field testing). Some entries imply both but timing is not explicit, which could create audit gaps. | Specification.md | Verification (entire table) | -- | PROPOSAL: Specification | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Obligatory Governance Foundation | 0 | NO_ITEMS | Governance foundation well-established through 13 requirements |
| E:normative:sufficiency | normative | sufficiency | Codified Governance Adequacy | 0 | NO_ITEMS | Governance adequacy addressed through standards and verification |
| E:normative:completeness | normative | completeness | Total Regulatory Oversight | 1 | HAS_ITEMS | Air entrainment target not quantified |
| E:normative:consistency | normative | consistency | Mandated Governance Integrity | 0 | NO_ITEMS | Governance integrity maintained across documents |
| E:operative:necessity | operative | necessity | Essential Procedural Command | 0 | NO_ITEMS | Procedural command adequately established through Phase A/B steps |
| E:operative:sufficiency | operative | sufficiency | Validated Execution Threshold | 1 | HAS_ITEMS | Vapour barrier lap/seal specification missing |
| E:operative:completeness | operative | completeness | Exhaustive Operational Governance | 0 | NO_ITEMS | Operational governance comprehensive through Procedure |
| E:operative:consistency | operative | consistency | Integrated Operational Discipline | 0 | NO_ITEMS | Operational discipline integrated across steps |
| E:evaluative:necessity | evaluative | necessity | Indispensable Quality Foundation | 0 | NO_ITEMS | Quality foundation established through geotech-backed requirements |
| E:evaluative:sufficiency | evaluative | sufficiency | Verified Quality Standard | 0 | NO_ITEMS | Quality standards verified through mix design and certification requirements |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Governance | 1 | HAS_ITEMS | Drainage terminology inconsistent |
| E:evaluative:consistency | evaluative | consistency | Harmonized Quality Discipline | 0 | NO_ITEMS | Quality discipline harmonized across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | MissingSlot | Specification | Specification | Add specific air entrainment target percentage or range for concrete. REQ-07 references CAN/CSA A23.1-2014 section 4.3.3 and Table 4 but does not state the required air content. | Specification REQ-07 requires air entrainment per CAN/CSA A23.1-2014 but does not specify the target air content percentage. Without stating or deriving the value from the standard (which is flagged as "not directly accessed"), the regulatory oversight for this parameter is incomplete. | Specification.md | REQ-07 > Sub-requirements > Air entrainment | -- | PROPOSAL: Specification REQ-07 (state target or confirm standard reference is sufficient) | TBD |
| E-002 | E:operative:sufficiency | MissingSlot | Datasheet | Specification | Add vapour barrier minimum thickness, lap width, and sealing method requirements. Currently only standard reference (CAN/CGSB-51.34-M) is cited. | Datasheet, Specification REQ-08, and Procedure Step B4 all reference the vapour barrier standard but none specify minimum thickness, lap width, or sealing method. The execution threshold for this element relies entirely on an external standard that is flagged as "not directly accessed." | Datasheet.md; Specification.md; Procedure.md | Datasheet: Subgrade Preparation > Vapour barrier; Specification: REQ-08 sub-req 5; Procedure: Step B4 | -- | PROPOSAL: Specification or Datasheet | TBD |
| E-003 | E:evaluative:completeness | Normalization | Multi | Multi | Normalize drainage slope requirement: Specification REQ-12 says "3% over first 3.0 m"; Datasheet says "min 2% slope away from slab; no ponding" (citing Geotech section 7.1 item 9 for slab drainage vs section 5.1.2 for foundation drainage). Clarify which requirement applies where. | Specification REQ-12 states "3% over first 3.0 m from building" while Datasheet Grade-Supported Slab Subgrade Preparation says "Min 2% slope away from slab." These appear to reference different geotech sections (5.1.2 vs 7.1 item 9) and may apply to different contexts (foundation perimeter vs slab surface drainage), but the distinction is not made clear. This risks inconsistent application. | Specification.md; Datasheet.md | Specification: REQ-12; Datasheet: Grade-Supported Slab Subgrade Preparation > Drainage | Specification.md#REQ-12 (3% per Geotech 5.1.2) vs Datasheet.md#Subgrade Prep > Drainage (2% per Geotech 7.1 item 9) | PROPOSAL: Clarify in both Specification and Datasheet which slope applies to which context | TBD |
