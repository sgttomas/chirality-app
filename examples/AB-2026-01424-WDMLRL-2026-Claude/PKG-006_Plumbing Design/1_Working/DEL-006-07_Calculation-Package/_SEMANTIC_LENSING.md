# Semantic Lensing Register: DEL-006-07 Plumbing Calculation Package

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-07_Calculation-Package/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-07_Calculation-Package/_CONTEXT.md (Deliverable identity, description, anticipated artifacts)
- _STATUS.md — DEL-006-07_Calculation-Package/_STATUS.md (Status: SEMANTIC_READY as of 2026-02-26)
- _SEMANTIC.md — DEL-006-07_Calculation-Package/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed successfully; audit PASS)
- Datasheet.md — DEL-006-07_Calculation-Package/Datasheet.md (Identification, attributes, conditions, construction, references)
- Specification.md — DEL-006-07_Calculation-Package/Specification.md (Scope, requirements REQ-001 through REQ-012, standards, verification)
- Guidance.md — DEL-006-07_Calculation-Package/Guidance.md (Purpose, principles, considerations, trade-offs, conflict table CFT-001 through CFT-003)
- Procedure.md — DEL-006-07_Calculation-Package/Procedure.md (Prerequisites, steps 1-9, verification, records)
- _REFERENCES.md — DEL-006-07_Calculation-Package/_REFERENCES.md (R-01, R-06, SOW-0016, OBJ-003, OBJ-004)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 30
- By document:
  - Datasheet: 5
  - Specification: 12
  - Guidance: 3
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 4  F: 5  D: 3  X: 6  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards citations lack edition specificity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code compliance matrix artifact is TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification for REQ-003 bulk fill flow rate has no acceptance value |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit trail mechanism defined for assumption changes |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps provide adequate execution direction |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers pass criteria |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No intermediate review gates between procedure steps |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance principles articulate value orientation adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by verification table |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | P.Eng. review in Step 9 serves as quality appraisal gate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify NPC edition and Alberta Safety Code Plumbing Order edition in Standards table; replace ASSUMPTION tags with confirmed editions or explicit TBD-with-resolution-path | All five standards entries in the Standards table are marked ASSUMPTION with no edition numbers; this weakens the prescriptive direction for the entire calculation package | Specification.md | Standards | -- | PROPOSAL: Plumbing Engineer to confirm with Safety Codes Officer | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add verification approach for code compliance matrix completeness (REQ-010) beyond "matrix included in calculation package" | REQ-010 verification says "Code compliance matrix included" but does not state how completeness of the matrix itself is verified (e.g., which code sections must appear) | Specification.md | Verification (REQ-010) | -- | PROPOSAL: Plumbing Engineer defines matrix scope | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Add acceptance threshold for REQ-003 bulk water fill pump flow rate; current verification states "flow rate TBD" | Compliance cannot be determined for REQ-003 because no target flow rate is specified; the verification approach references TBD without a resolution path | Specification.md | REQ-003 / Verification (REQ-003) | -- | PROPOSAL: Human ruling on target flow rate per CFT-002 in Guidance.md | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Multi | Procedure | Add a procedure step or verification check for tracking assumption changes through design iterations (assumption audit trail) | Documents reference many ASSUMPTION-tagged items but no mechanism exists to audit whether assumptions are later confirmed, changed, or invalidated during design progression | Procedure.md; Datasheet.md | entire document scanned | -- | PROPOSAL: Add assumption tracking step in Procedure Step 1 or Step 9 | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add intermediate review/hold points between major procedure steps (e.g., after Step 2 Water Demand before proceeding to Step 3 Supply Sizing) | The procedure defines 9 sequential steps but no intermediate review gates; an error in early steps (e.g., demand analysis) propagates undetected through all subsequent sizing | Procedure.md | Steps | -- | PROPOSAL: Add hold-point after Step 2 and Step 5 at minimum | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Occupancy count missing from Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available data from R-01 and R-06 is adequately recorded |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Fixture schedule cross-reference gap |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Unit inconsistency (metric/imperial) |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (cistern volume, pump rate, septic size) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for off-grid design is well-framed in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Information coverage is adequate at this stage |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across documents are coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Off-grid and industrial design understanding articulated in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. competence requirement is stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Appropriate for design-phase; mastery emerges during engineering |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict table and trade-offs demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section demonstrates adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance principles |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add building occupancy count or user count as a key sizing parameter (currently absent; needed for fixture unit calculations) | Occupancy count is an essential fact for NPC fixture unit sizing referenced in Procedure Step 2 and Specification REQ-012, but it does not appear in Datasheet attributes | Datasheet.md | Attributes / Plumbing Systems -- Key Sizing Parameters | -- | PROPOSAL: Plumbing Engineer determines with Architect | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add cross-reference to DEL-006-06 fixture schedule data once available; current fixture list in Datasheet is drawn only from R-06 drawing | Datasheet lists fixtures from R-06 but does not reference the co-developed fixture schedule (DEL-006-06) noted in Procedure prerequisites; comprehensive record requires both sources | Datasheet.md | Fixtures and Equipment Identified on Drawings | -- | PROPOSAL: Link to DEL-006-06 when available | TBD |
| B-003 | B:data:consistency | Normalization | Multi | Datasheet | Normalize unit system: cistern is 50,000 L (metric), septic is 2,000 US gallons (imperial), pump is 100 LPM (metric), fill connection is 2.5 inches (imperial); document a unit convention or provide dual units consistently | Mixed metric and imperial units across all documents risk conversion errors during engineering; the inconsistency originates from R-01 but should be normalized in the calculation package | Datasheet.md; Specification.md | Attributes; REQ-001 through REQ-004 | -- | PROPOSAL: Adopt consistent dual-unit presentation in Datasheet | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforced Regulatory Baseline | 1 | HAS_ITEMS | Regulatory baseline not enforceable without confirmed code editions |
| C:normative:sufficiency | normative | sufficiency | Certified Obligatory Justification | 1 | HAS_ITEMS | Certification path underspecified |
| C:normative:completeness | normative | completeness | Universal Compliance Coverage | 1 | HAS_ITEMS | Compliance scope boundary unclear for Old North Shop |
| C:normative:consistency | normative | consistency | Harmonized Compliance Discipline | 0 | NO_ITEMS | Compliance approach is internally consistent |
| C:operative:necessity | operative | necessity | Indispensable Operational Method | 0 | NO_ITEMS | Procedure steps cover essential methods |
| C:operative:sufficiency | operative | sufficiency | Validated Competent Execution | 0 | NO_ITEMS | Steps provide sufficient execution guidance |
| C:operative:completeness | operative | completeness | Exhaustive Functional Coverage | 1 | HAS_ITEMS | Vent termination clearances not addressed in Procedure |
| C:operative:consistency | operative | consistency | Standardized Coordinated Workflow | 0 | NO_ITEMS | Workflow is standardized and coordinated |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Significance | 0 | NO_ITEMS | Merit basis established through P.Eng. stamp and code compliance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Competence Appraisal | 0 | NO_ITEMS | Competence appraisal addressed via P.Eng. review |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Integrity | 0 | NO_ITEMS | Valuation integrity supported by trade-offs section |
| C:evaluative:consistency | evaluative | consistency | Disciplined Valuation Consistency | 0 | NO_ITEMS | Consistent valuation approach across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Which edition of the National Plumbing Code of Canada applies? Which Alberta Safety Code Plumbing Order is in force for this project? Resolution path: Safety Codes Officer at permit pre-application | The enforced regulatory baseline cannot be established until the governing code editions are confirmed; all code references are currently ASSUMPTION-tagged | Specification.md | Standards | -- | PROPOSAL: Safety Codes Officer confirmation required | TBD |
| C-002 | C:normative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for P.Eng. certification path: clarify whether the P.Eng. stamps the calculation package only, or also the IFC drawings, and what the certification scope covers relative to this deliverable | Guidance states P.Eng. certification supports OBJ-003 but does not explain the certification boundary (calc package vs. drawings vs. both); this affects what "certified obligatory justification" means for this deliverable | Guidance.md | Purpose | -- | PROPOSAL: Plumbing Engineer to clarify P.Eng. scope | TBD |
| C-003 | C:normative:completeness | Conflict | Multi | Specification | Resolve whether DEL-006-07 compliance coverage extends to Old North Shop washroom/locker room/laundry plumbing or only New North Shop addition | CFT-001 in Guidance.md identifies this scope conflict; if compliance coverage is meant to be universal for PKG-006, the Specification scope exclusions and Procedure prerequisites must be updated | Specification.md; Guidance.md | Scope (What This Deliverable Excludes); Conflict Table CFT-001 | Specification.md#What This Deliverable Excludes; Guidance.md#Conflict Table CFT-001 | PROPOSAL: Per CFT-001 proposed authority -- include Old North Shop unless separate deliverable defined | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add explicit step or sub-step for vent termination clearance verification (clearances from air intakes, roof penetration height) referenced in Procedure Step 6.3 as TBD | Step 6.3 mentions vent termination but marks specific requirements as TBD; the procedure does not include a verification check for termination clearances in the Verification table | Procedure.md | Step 6 -- Vent Stack Sizing; Verification | -- | PROPOSAL: Add vent clearance check to Verification table | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Rigorous Proof Obligation | 1 | HAS_ITEMS | Emergency shower standard not confirmed |
| F:normative:sufficiency | normative | sufficiency | Validated Prescriptive Boundary | 1 | HAS_ITEMS | Scope boundary for Old North Shop remains unvalidated |
| F:normative:completeness | normative | completeness | Absolute Regulatory Accounting | 1 | HAS_ITEMS | Laundry services plumbing not accounted for |
| F:normative:consistency | normative | consistency | Systematic Compliance Coherence | 0 | NO_ITEMS | Requirements are internally coherent |
| F:operative:necessity | operative | necessity | Vital Procedural Capability | 0 | NO_ITEMS | Procedure covers vital capabilities |
| F:operative:sufficiency | operative | sufficiency | Proficient Procedural Breadth | 1 | HAS_ITEMS | Pressure washer reel model dependency unaddressed |
| F:operative:completeness | operative | completeness | Exhaustive Capability Documentation | 0 | NO_ITEMS | Documentation artifacts are enumerated |
| F:operative:consistency | operative | consistency | Standardized Execution Clarity | 0 | NO_ITEMS | Execution steps are clear and standardized |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Quality Evidence | 1 | HAS_ITEMS | No quality metric for calculation accuracy |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Quality Assurance | 0 | NO_ITEMS | QA through P.Eng. review is stated |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Accounting | 0 | NO_ITEMS | Worth accounting covered by trade-offs |
| F:evaluative:consistency | evaluative | consistency | Systematic Worth Benchmark | 0 | NO_ITEMS | Worth benchmarking consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm which emergency shower standard applies (ANSI Z358.1 or Alberta OHS equivalent) and obtain specific minimum flow rate and duration values for verification | REQ-007 verification references "applicable safety standards" with ASSUMPTION tag; rigorous proof obligation requires a specific numeric threshold for flow and pressure | Specification.md | REQ-007; Standards | -- | PROPOSAL: Plumbing Engineer to confirm with OH&S authority | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen the scope exclusion for Old North Shop to either definitively exclude or include it, with rationale; current language ("scope TBD as to whether included or separate deliverable") is insufficiently prescriptive | The prescriptive boundary of the deliverable remains ambiguous at the scope definition level; this propagates uncertainty into requirements coverage | Specification.md | Scope -- What This Deliverable Excludes | -- | PROPOSAL: Resolve via CFT-001 human ruling | TBD |
| F-003 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for laundry services plumbing if Old North Shop locker room with laundry (SOW-0074) falls within scope; currently no REQ addresses laundry hot/cold supply or drain | If the scope is resolved to include Old North Shop renovation, laundry services plumbing calculations are not covered by any existing requirement (REQ-001 through REQ-012) | Specification.md | Requirements | -- | PROPOSAL: Contingent on CFT-001 resolution | TBD |
| F-004 | F:operative:sufficiency | TBD_Question | Procedure | Procedure | Record TBD: Identify pressure washer reel model or specify minimum performance parameters (flow rate, operating pressure) to enable supply sizing in Step 3 and Step 4 | Procedure Step 2.2 and Step 4.4 reference pressure washer reel sizing but note "specific model not identified in RFP" and "depends on pressure washer reel model"; procedural breadth requires this input | Procedure.md | Step 2.2; Step 4.4 | -- | PROPOSAL: Design-Builder to select or specify model | TBD |
| F-005 | F:evaluative:necessity | MissingSlot | Specification | Specification | Add an acceptance criterion for calculation accuracy or independent check methodology (e.g., peer review, independent spot-check of critical calculations) | No quality metric exists for the intrinsic accuracy of the calculations themselves beyond P.Eng. stamp; the verification table checks parameter coverage but not calculation correctness | Specification.md | Verification | -- | PROPOSAL: P.Eng. to define QA/QC standard for calculations | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Proof Directive | 0 | NO_ITEMS | Proof directive is well-established through OBJ-003 linkage |
| D:normative:applying | normative | applying | Compulsory Compliance Implementation | 1 | HAS_ITEMS | Implementation gap for septic authority approval |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance approach is clear |
| D:normative:reviewing | normative | reviewing | Settled Compliance Inspection | 0 | NO_ITEMS | Compliance inspection addressed through permit process |
| D:operative:guiding | operative | guiding | Resolved Workflow Governance | 0 | NO_ITEMS | Workflow governance is resolved |
| D:operative:applying | operative | applying | Resolved Task Performance | 0 | NO_ITEMS | Task performance expectations are clear |
| D:operative:judging | operative | judging | Definitive Capability Determination | 1 | HAS_ITEMS | IFC cross-reference check lacks specificity |
| D:operative:reviewing | operative | reviewing | Settled Workflow Inspection | 0 | NO_ITEMS | Step 9 review process addresses workflow inspection |
| D:evaluative:guiding | evaluative | guiding | Principled Quality Direction | 0 | NO_ITEMS | Quality direction established in Guidance principles |
| D:evaluative:applying | evaluative | applying | Resolved Worthiness Assurance | 0 | NO_ITEMS | Worthiness assurance addressed through P.Eng. review |
| D:evaluative:judging | evaluative | judging | Definitive Significance Ruling | 1 | HAS_ITEMS | Cistern fill frequency significance not flagged for Owner |
| D:evaluative:reviewing | evaluative | reviewing | Settled Merit Inspection | 0 | NO_ITEMS | Merit inspection via P.Eng. stamp is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification approach for septic holding tank regulatory approval (Alberta Environment / AER); REQ-004 verification mentions "authority approval" but Specification does not define what constitutes evidence of approval | Compulsory compliance implementation for the septic system requires regulatory authority approval, but the verification approach does not specify the approval artifact or acceptance evidence | Specification.md | REQ-004; Verification (REQ-004) | -- | PROPOSAL: Define expected approval artifact (permit, letter, etc.) | TBD |
| D-002 | D:operative:judging | WeakStatement | Procedure | Procedure | Strengthen Step 9.4 IFC cross-reference check: specify which drawing dimensions and pipe sizes must match which calculation outputs (e.g., supply line diameters, drain slopes, fixture connections) | Step 9.4 says "cross-reference the calculation package against the IFC plumbing drawing set to confirm consistency" but does not specify which parameters to compare; definitive capability determination requires explicit cross-check items | Procedure.md | Step 9.4 | -- | PROPOSAL: Add cross-reference checklist to Step 9 | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add explicit statement in Trade-off 1 that cistern fill frequency results should be formally communicated to the Owner as an operational planning deliverable, not just documented internally | Trade-off 1 mentions characterizing operational implications of cistern volume but does not specify that the fill frequency analysis should be transmitted to the Owner as a distinct communication; significance ruling requires clear Owner notification path | Guidance.md | Trade-offs -- Trade-off 1 | -- | PROPOSAL: Plumbing Engineer to confirm Owner communication protocol | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Foundational Requirement | 1 | HAS_ITEMS | Foundation requirement for simultaneous demand factor unanchored |
| X:guiding:sufficiency | guiding | sufficiency | Validated Evidentiary Guidance | 0 | NO_ITEMS | Evidentiary guidance is validated through R-01/R-06 references |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Accounting | 1 | HAS_ITEMS | SOW items not fully traced to requirements |
| X:guiding:consistency | guiding | consistency | Stable Directive Coherence | 0 | NO_ITEMS | Directives are coherent across documents |
| X:applying:necessity | applying | necessity | Mandatory Execution Evidence | 1 | HAS_ITEMS | No evidence requirement for pump curve documentation |
| X:applying:sufficiency | applying | sufficiency | Validated Implementation Scope | 0 | NO_ITEMS | Implementation scope is validated |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Record | 0 | NO_ITEMS | Records section in Procedure is comprehensive |
| X:applying:consistency | applying | consistency | Reliable Implementation Measure | 1 | HAS_ITEMS | Septic capacity stated inconsistently |
| X:judging:necessity | judging | necessity | Binding Performance Finding | 0 | NO_ITEMS | Performance findings tied to verification table |
| X:judging:sufficiency | judging | sufficiency | Validated Compliance Evidence | 1 | HAS_ITEMS | Compliance evidence for drainage slopes lacks pass criterion |
| X:judging:completeness | judging | completeness | Comprehensive Compliance Accounting | 0 | NO_ITEMS | Compliance accounting covered by code compliance matrix artifact |
| X:judging:consistency | judging | consistency | Stable Compliance Benchmark | 0 | NO_ITEMS | Benchmarks are stable |
| X:reviewing:necessity | reviewing | necessity | Critical Audit Finding | 0 | NO_ITEMS | No critical audit findings at this stage |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Audit Evidence | 1 | HAS_ITEMS | Assumption documentation audit criterion is vague |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Documentation | 0 | NO_ITEMS | Audit documentation is comprehensive for current stage |
| X:reviewing:consistency | reviewing | consistency | Stable Audit Benchmark | 0 | NO_ITEMS | Audit benchmarks are stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | WeakStatement | Specification | Specification | Define the simultaneous demand scenario as an explicit requirement or reference the Guidance trade-off; current REQ-008 says "simultaneous use assumptions (ASSUMPTION: simultaneous demand factor TBD)" without anchoring the method | The simultaneous demand factor is foundational to supply sizing (REQ-002, REQ-008) and pressure calculations but is stated as TBD with no resolution method specified in the requirement itself | Specification.md | REQ-008 | -- | PROPOSAL: Plumbing Engineer to define and document in Step 2.3 | TBD |
| X-002 | X:guiding:completeness | Normalization | Multi | Specification | Add explicit SOW-to-REQ traceability table; SOW-0041 through SOW-0050 are referenced in individual requirements but no consolidated mapping exists | Comprehensive directive accounting requires traceable linkage from each SOW item to at least one requirement; currently traceability is embedded in individual REQ source fields but not consolidated | Specification.md; Datasheet.md | Requirements; References | -- | PROPOSAL: Add traceability matrix to Specification or Datasheet | TBD |
| X-003 | X:applying:necessity | VerificationGap | Specification | Procedure | Add explicit requirement to document pump curve data as evidence for REQ-002 verification; current verification says "pump curve analysis" but does not require the curve to be included in the package | Mandatory execution evidence for pump selection requires the pump performance curve to be part of the calculation package record; the Records table in Procedure lists "Equipment Performance Data Sheets" but Specification verification does not mandate inclusion of the actual curve | Specification.md; Procedure.md | Verification (REQ-002); Records | -- | PROPOSAL: Add pump curve to required records | TBD |
| X-004 | X:applying:consistency | Normalization | Datasheet | Datasheet | Normalize septic tank capacity presentation: Datasheet states "2,000 US gallons" while Specification REQ-004 states "2,000 US gallon (approximately 7,571 L)"; add the metric equivalent consistently in Datasheet | The metric conversion is provided in Specification but not in Datasheet; this inconsistency in the primary data record could cause confusion | Datasheet.md | Attributes -- Plumbing Systems | -- | PROPOSAL: Add metric equivalent in Datasheet | TBD |
| X-005 | X:judging:sufficiency | VerificationGap | Procedure | Specification | Add specific pass criterion for drainage slope verification (e.g., minimum slope per pipe diameter per NPC table reference) to the Verification table | Procedure Step 5.2 references minimum slopes per NPC but the Verification table in Procedure only says "slope and pipe sizing calculations" without a quantitative pass criterion for slope | Procedure.md | Verification; Step 5.2 | -- | PROPOSAL: Add NPC table reference for minimum slopes once code edition confirmed | TBD |
| X-006 | X:reviewing:sufficiency | VerificationGap | Procedure | Procedure | Strengthen the "Assumptions documented" verification check: define what constitutes a complete assumption record (e.g., assumption ID, source, status, confirmation date) rather than just "all assumptions listed" | The verification check says "All engineering and Design-Builder assumptions listed in design assumption sub-artifact" but does not define the required fields for each assumption entry; audit sufficiency requires structured assumption records | Procedure.md | Verification | -- | PROPOSAL: Define assumption record schema in Step 1.3 | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Factual Authority | 1 | HAS_ITEMS | Datasheet status field is stale |
| E:guiding:information | guiding | information | Coherent Leadership Narrative | 0 | NO_ITEMS | Guidance provides a coherent leadership narrative |
| E:guiding:knowledge | guiding | knowledge | Authoritative Governance Command | 0 | NO_ITEMS | Governance command established through P.Eng. authority |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Insight | 0 | NO_ITEMS | Strategic insight present in Guidance trade-offs |
| E:applying:data | applying | data | Validated Action Documentation | 1 | HAS_ITEMS | Mud sump volume not in Datasheet parameters |
| E:applying:information | applying | information | Comprehensive Action Narrative | 0 | NO_ITEMS | Action narrative in Procedure is comprehensive |
| E:applying:knowledge | applying | knowledge | Proficient Action Command | 0 | NO_ITEMS | Action command is proficient |
| E:applying:wisdom | applying | wisdom | Integrated Action Wisdom | 0 | NO_ITEMS | Wisdom integrated through Guidance considerations |
| E:judging:data | judging | data | Decisive Conformance Record | 1 | HAS_ITEMS | Booster pump/pressure tank decision not recorded |
| E:judging:information | judging | information | Consistent Assessment Narrative | 0 | NO_ITEMS | Assessment narrative is consistent |
| E:judging:knowledge | judging | knowledge | Proficient Ruling Command | 0 | NO_ITEMS | Ruling command is proficient |
| E:judging:wisdom | judging | wisdom | Comprehensive Judgment Wisdom | 0 | NO_ITEMS | Judgment wisdom expressed in conflict table |
| E:reviewing:data | reviewing | data | Validated Inspection Record | 1 | HAS_ITEMS | Guarantee period reference not in Specification |
| E:reviewing:information | reviewing | information | Comprehensive Inspection Narrative | 0 | NO_ITEMS | Inspection narrative is comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Inspection Command | 0 | NO_ITEMS | Inspection command is proficient |
| E:reviewing:wisdom | reviewing | wisdom | Disciplined Inspection Wisdom | 0 | NO_ITEMS | Inspection wisdom is disciplined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Conflict | Datasheet | Datasheet | Update Datasheet status field from "OPEN (as of 2026-02-25)" to match _STATUS.md current status "SEMANTIC_READY (as of 2026-02-26)" | Datasheet Identification table shows "Deliverable Status: OPEN (as of 2026-02-25)" while _STATUS.md shows status has progressed to SEMANTIC_READY; factual authority requires current data | Datasheet.md; _STATUS.md | Identification; Status Log | Datasheet.md#Identification; _STATUS.md#Status Log | PROPOSAL: Update Datasheet to match _STATUS.md | TBD |
| E-002 | E:applying:data | MissingSlot | Datasheet | Datasheet | Add mud sump volume as a key sizing parameter in Datasheet (currently absent; REQ-006 verification requires "sump volume calculation" and Procedure Step 5.3 references motor-scraper wash volumes) | The mud sump is a significant infrastructure element requiring sizing but its target volume is not listed in Datasheet key sizing parameters; only the discharge point is noted | Datasheet.md | Attributes -- Plumbing Systems | -- | PROPOSAL: Add as TBD parameter pending engineering | TBD |
| E-003 | E:judging:data | RationaleGap | Guidance | Guidance | Add a consideration or decision record for whether a booster pump or pressure tank is needed for the cistern-fed system; Procedure Step 4.5 flags this as an ASSUMPTION but Guidance does not address the decision rationale | The booster pump/pressure tank decision affects system configuration and cost but is only mentioned as a parenthetical ASSUMPTION in Procedure; Guidance should frame the decision rationale | Procedure.md; Guidance.md | Step 4.5; entire document scanned | -- | PROPOSAL: Add as Consideration 6 in Guidance | TBD |
| E-004 | E:reviewing:data | VerificationGap | Specification | Specification | Add reference to the 2-year guarantee period (R-01 section 2.10) in Specification context; the calculation package serves as the design record during the guarantee period but Specification does not mention this downstream use | Datasheet Conditions references "Guarantee period: Construction period + 2 years post-CCC" and Guidance Purpose item 4 references it, but Specification has no corresponding note about the calculation package's role during the guarantee period | Datasheet.md; Guidance.md; Specification.md | Conditions; Purpose; entire document scanned | -- | PROPOSAL: Add note in Specification Scope or Documentation section | TBD |
