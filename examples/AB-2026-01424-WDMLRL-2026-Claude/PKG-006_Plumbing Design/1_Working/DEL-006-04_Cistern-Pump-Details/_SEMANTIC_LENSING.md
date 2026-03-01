# Semantic Lensing Register: DEL-006-04 Cistern & Pump Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-04_Cistern-Pump-Details/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-04_Cistern-Pump-Details/_CONTEXT.md
- _STATUS.md — DEL-006-04_Cistern-Pump-Details/_STATUS.md (State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-006-04_Cistern-Pump-Details/_SEMANTIC.md (Audit: PASS, 2026-02-26)
- Datasheet.md — DEL-006-04_Cistern-Pump-Details/Datasheet.md
- Specification.md — DEL-006-04_Cistern-Pump-Details/Specification.md
- Guidance.md — DEL-006-04_Cistern-Pump-Details/Guidance.md
- Procedure.md — DEL-006-04_Cistern-Pump-Details/Procedure.md
- _REFERENCES.md — DEL-006-04_Cistern-Pump-Details/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 25
- By document (AppliesToDoc):
  - Datasheet: 5
  - Specification: 9
  - Guidance: 2
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 6  B: 4  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition not identified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Fill connection terminology |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for code compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequate for current stage |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Bulk fill pump flow rate TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps well-articulated in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Pump head verification gap |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit adequately covered |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Cistern sizing rationale gap |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit considerations addressed in Guidance trade-offs |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Addressed in Guidance trade-offs table |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicable edition of National Plumbing Code of Canada as adopted in Alberta and any provincial amendments | The prescriptive direction lens reveals that R-007 requires code compliance but neither Specification nor Datasheet identifies the specific code edition. Guidance defers to the Plumbing Engineer. Without the edition, compliance determination cannot be anchored. | Specification.md, Datasheet.md | Specification.md#Standards, Datasheet.md#Conditions | -- | PROPOSAL: Plumbing Engineer of Record | TBD |
| A-002 | A:normative:applying | Normalization | Multi | Guidance | Normalize terminology: "cistern filling connection" vs "fill connection" vs "filling connection" -- adopt single canonical term across all documents | Mandatory practice lens reveals inconsistent terminology for the same physical connection: Datasheet uses "cistern filling connection", Specification R-004 uses "cistern filling connection", Procedure uses "fill connection (2.5")". Inconsistency risks construction ambiguity. | Datasheet.md, Specification.md, Procedure.md | Datasheet.md#Distribution Pump System, Specification.md#R-004, Procedure.md#Step 4 (4.4) | -- | PROPOSAL: Guidance vocabulary note | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criterion for R-007 specifying which code edition was used for compliance determination | Compliance determination lens shows that the Verification table for R-007 says "Reference to applicable Alberta Safety Codes and NPC edition noted" but does not require the specific edition to be recorded on drawings. Without this, compliance cannot be verified against a specific standard. | Specification.md | Specification.md#Verification (R-007 row) | -- | PROPOSAL: Specification normative | TBD |
| A-004 | A:operative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: Determine bulk fill pump required flow rate based on Owner operational requirements (fill truck capacity, target fill time) | Procedural direction lens reveals that Datasheet lists bulk fill connection size as TBD and Procedure Step 2.4 explicitly notes flow rate is "TBD based on Owner operational requirements." This is a necessary design input that has no value anywhere in the documents. | Datasheet.md, Procedure.md | Datasheet.md#Bulk Water Fill System, Procedure.md#Step 2 (2.4) | -- | PROPOSAL: Owner / Plumbing Engineer | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add verification criterion for pump performance at design TDH (not just rated flow) to R-003 acceptance criterion | Performance assessment lens reveals that R-003 acceptance criterion states "Rated flow >= 100 LPM at design head" but the requirement text itself says only "minimum flow rate of 100 litres per minute." The verification table references "design head" but the requirement does not establish what TDH value must be met. | Specification.md | Specification.md#R-003, Specification.md#Verification (R-003 row) | -- | PROPOSAL: Specification normative | TBD |
| A-006 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for why 50,000 L is treated as a floor vs. a target; document basis-of-design methodology for cistern volume adequacy | Value orientation lens reveals that Guidance states "treat 50,000 L as a floor, not a target" and recommends assessing against demand, but does not provide a methodology or reference for how to determine if 50,000 L is adequate. The basis-of-design reasoning is deferred to DEL-006-07 but not anchored here. | Guidance.md | Guidance.md#Principles > Cistern Sizing | -- | PROPOSAL: Guidance directional | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Pressure tank TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Cistern material absent |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing bulk fill pump attributes |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Numeric values consistent where stated |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts comprehensive for current stage |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Fire hose pump identity conflict |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery scope adequate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment addressed in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add attribute row for pressure tank / hydropneumatic tank with capacity, pre-charge pressure, and connection size (currently all TBD) | Essential fact lens: Datasheet lists "Pressure tank / hydropneumatic tank" as TBD. Specification R-008 references pump schedule but pressure tank is not covered by any requirement. Guidance identifies it as likely required. This is an essential design datum with no defined attributes. | Datasheet.md | Datasheet.md#Distribution Pump System (Pressure tank row) | -- | PROPOSAL: Plumbing Engineer | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add cistern material/type attribute (concrete, fiberglass, polyethylene, steel) -- currently absent from Datasheet | Adequate evidence lens: Guidance discusses cistern material options extensively but Datasheet has no attribute row for cistern material or type. This is a necessary design parameter for procurement and structural coordination. | Datasheet.md, Guidance.md | Datasheet.md#Cistern System, Guidance.md#Considerations > Cistern Material and Type | -- | PROPOSAL: Plumbing Engineer | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add bulk fill pump attributes (flow rate, head, power, connection size) -- all currently absent or TBD | Comprehensive record lens: Datasheet Bulk Water Fill System section lists the bulk fill pump as "high volume pump" but provides no performance attributes. Specification R-005 requires the system but does not specify performance parameters. Procedure Step 2.4 notes flow rate TBD. | Datasheet.md | Datasheet.md#Bulk Water Fill System | -- | PROPOSAL: Plumbing Engineer / Owner | TBD |
| B-004 | B:information:consistency | Conflict | Multi | TBD | Clarify whether "fire hose pump" (SOW-0062, 70A circuit) is the same as or distinct from the 100 LPM internal distribution pump (SOW-0042) | Coherent message lens: Datasheet notes a 70A circuit for pressure washer reel; Guidance CONF-002 identifies that the "fire hose pump" circuit may or may not correspond to the distribution pump. This unresolved identity creates an incoherent signal across electrical and plumbing documents. | Datasheet.md, Guidance.md | Datasheet.md#Pressure Washer / Water Tap System, Guidance.md#Conflict Table > CONF-002 | Guidance.md#CONF-002 (fire hose pump vs. distribution pump), Datasheet.md#Distribution Pump System | PROPOSAL: Plumbing Engineer + Electrical Engineer joint determination | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Mandate Basis | 1 | HAS_ITEMS | Cistern location conflict |
| C:normative:sufficiency | normative | sufficiency | Regulatory Acceptance Threshold | 0 | NO_ITEMS | Acceptance thresholds present in Verification table |
| C:normative:completeness | normative | completeness | Exhaustive Obligation Scope | 1 | HAS_ITEMS | Freeze protection not in requirements |
| C:normative:consistency | normative | consistency | Harmonized Conformance Standard | 0 | NO_ITEMS | Conformance standards consistent where stated |
| C:operative:necessity | operative | necessity | Critical Operational Baseline | 0 | NO_ITEMS | Operational baselines established |
| C:operative:sufficiency | operative | sufficiency | Verified Process Adequacy | 0 | NO_ITEMS | Process adequacy verified through procedure steps |
| C:operative:completeness | operative | completeness | Total Execution Coverage | 0 | NO_ITEMS | Execution coverage comprehensive in Procedure |
| C:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Process discipline consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Merit Criterion | 1 | HAS_ITEMS | Water quality classification missing |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation Basis | 0 | NO_ITEMS | Valuation basis adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Account | 0 | NO_ITEMS | Worth account covered in trade-offs |
| C:evaluative:consistency | evaluative | consistency | Principled Appraisal Coherence | 0 | NO_ITEMS | Appraisal coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Conflict | Multi | TBD | Resolve cistern location: conceptual drawing shows cistern in utility room area but 50,000 L volume may not physically fit as shown. Confirm with Structural and Architectural coordination. | Enforceable mandate basis lens: The mandate (50,000 L minimum) and the conceptual layout (utility room placement) may be physically incompatible. This is already captured as CONF-001 in Guidance but has no corresponding requirement or acceptance criterion addressing resolution. | Datasheet.md, Specification.md, Guidance.md | Datasheet.md#Cistern System (location row), Specification.md#R-009, Guidance.md#Conflict Table > CONF-001 | Guidance.md#CONF-001 (App B-Plumb layout vs. RFP 50,000 L requirement) | PROPOSAL: Plumbing Engineer + Structural Engineer + Architect joint resolution | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement for freeze protection of cistern, piping, and bulk fill connection in Alberta climate conditions | Exhaustive obligation scope lens: Guidance identifies freeze protection as "a significant design consideration that is not addressed in the RFP source documents." No corresponding requirement exists in Specification. For a rural Alberta site, freeze protection is an obligation that should be captured normatively. | Specification.md, Guidance.md | Specification.md#Requirements (entire section scanned -- no freeze protection requirement), Guidance.md#Considerations > Freeze Protection | -- | PROPOSAL: Plumbing Engineer | TBD |
| C-003 | C:evaluative:necessity | WeakStatement | Guidance | Guidance | Clarify water quality classification: state definitively whether cistern water is potable or non-potable, and document cross-connection control requirements if any fixture requires potable water | Fundamental merit criterion lens: Guidance states "ASSUMPTION: cistern water is non-potable service water" but then notes "If any fixture is intended for potable use... the Plumbing Engineer must address cross-connection control." The assumption is not confirmed and the conditional language leaves a material design decision unresolved. | Guidance.md | Guidance.md#Considerations > Water Quality | -- | PROPOSAL: Plumbing Engineer / Owner determination | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Compliance Foundation | 1 | HAS_ITEMS | Overflow requirement missing |
| F:normative:sufficiency | normative | sufficiency | Codified Compliance Benchmark | 0 | NO_ITEMS | Benchmarks present |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Control system requirement weak |
| F:normative:consistency | normative | consistency | Uniform Regulatory Discipline | 0 | NO_ITEMS | Regulatory discipline uniform |
| F:operative:necessity | operative | necessity | Verified Operational Imperative | 0 | NO_ITEMS | Operational imperatives verified |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Operational Competence | 0 | NO_ITEMS | Competence demonstrated |
| F:operative:completeness | operative | completeness | Exhaustive Operational Record | 0 | NO_ITEMS | Operational record exhaustive |
| F:operative:consistency | operative | consistency | Methodical Performance Stability | 0 | NO_ITEMS | Performance stability addressed |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Quality Imperative | 0 | NO_ITEMS | Quality imperatives present |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Substantiation | 1 | HAS_ITEMS | Guarantee period verification gap |
| F:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Constancy | 0 | NO_ITEMS | Quality constancy maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement for cistern overflow protection (overflow outlet, drainage path, and overfill prevention during bulk delivery) | Obligatory compliance foundation lens: Guidance explicitly identifies overflow and drain provisions as necessary ("overflow into the building... would be a design deficiency") and R-002 mentions overflow generally, but no dedicated requirement establishes overflow capacity, discharge location, or coordination with civil drainage. | Specification.md, Guidance.md | Specification.md#R-002, Guidance.md#Considerations > Overflow and Drain Provisions | -- | PROPOSAL: Specification normative | TBD |
| F-002 | F:normative:completeness | WeakStatement | Specification | Specification | Strengthen R-002 "all necessary plumbing" language by enumerating required connection types (inlet, outlet, overflow, drain, vent, man-way, level sensor ports) | Exhaustive regulatory coverage lens: R-002 states the cistern shall have "all necessary plumbing, including inlets, outlets, overflow, drain, venting, and access provisions." The word "including" makes this an illustrative rather than exhaustive list. Level sensor ports and man-way access are absent from the enumeration but are operationally necessary. | Specification.md | Specification.md#R-002 | -- | PROPOSAL: Specification normative | TBD |
| F-003 | F:evaluative:sufficiency | VerificationGap | Specification | Procedure | Add verification approach for guarantee period compliance (construction period + 2 years post-CCC) -- confirm equipment warranty coverage meets contract requirement | Defensible quality substantiation lens: Datasheet Conditions lists "Guarantee period: Construction period + 2 years post-CCC" but no requirement in Specification addresses warranty/guarantee provisions for pump equipment, and no verification step confirms equipment warranty meets the contract guarantee period. | Datasheet.md, Specification.md | Datasheet.md#Conditions (Guarantee period row), Specification.md#Verification (entire table scanned) | -- | PROPOSAL: Procedure operational check | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Regulatory Direction | 0 | NO_ITEMS | Regulatory direction established |
| D:normative:applying | normative | applying | Codified Enforcement Practice | 0 | NO_ITEMS | Enforcement practices codified |
| D:normative:judging | normative | judging | Binding Conformance Ruling | 1 | HAS_ITEMS | Safety Code permit verification |
| D:normative:reviewing | normative | reviewing | Standardized Compliance Inspection | 0 | NO_ITEMS | Compliance inspection covered |
| D:operative:guiding | operative | guiding | Settled Workflow Directive | 0 | NO_ITEMS | Workflow directives settled |
| D:operative:applying | operative | applying | Established Performance Execution | 1 | HAS_ITEMS | Coordination confirmation method |
| D:operative:judging | operative | judging | Evidenced Performance Verdict | 0 | NO_ITEMS | Performance verdicts evidenced |
| D:operative:reviewing | operative | reviewing | Systematic Operational Review | 0 | NO_ITEMS | Operational review systematic |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Guidance | 0 | NO_ITEMS | Quality guidance settled |
| D:evaluative:applying | evaluative | applying | Justified Quality Realization | 1 | HAS_ITEMS | Assumption tracking gap |
| D:evaluative:judging | evaluative | judging | Definitive Merit Reckoning | 0 | NO_ITEMS | Merit reckoning adequate |
| D:evaluative:reviewing | evaluative | reviewing | Sustained Merit Examination | 0 | NO_ITEMS | Merit examination sustained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Procedure | Procedure | Add verification step confirming Safety Code permit application was submitted and accepted prior to construction (references PKG-009) | Binding conformance ruling lens: Procedure Step 7.4 mentions submitting to safety authority but the Verification table in Procedure does not include a pass criterion for permit acceptance. The permit is a binding conformance gate. | Procedure.md | Procedure.md#Step 7 (7.4), Procedure.md#Verification | -- | PROPOSAL: Procedure operational check | TBD |
| D-002 | D:operative:applying | WeakStatement | Procedure | Procedure | Clarify what constitutes "written confirmation of coordination responses" in Step 3.2 -- specify minimum documentation form (email, signed coordination drawing, RFI response) | Established performance execution lens: Procedure Step 3.2 requires "written confirmation of coordination responses" but does not define what form this documentation must take. In a design-build context, the form of coordination confirmation is consequential for contract administration. | Procedure.md | Procedure.md#Step 3 (3.2) | -- | PROPOSAL: Procedure operational | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Specification | Guidance | Add rationale documenting which requirements are sourced from RFP vs. derived by engineering assumption, and the basis for each assumption | Justified quality realization lens: Multiple requirements in Specification are marked "ASSUMPTION" (R-008, R-010, R-011) and Standards lists assumptions. The production documents track the label but do not provide a consolidated rationale for why each assumption was adopted or what would change if the assumption proved wrong. | Specification.md | Specification.md#R-008, R-010, R-011, Standards | -- | PROPOSAL: Guidance directional | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Essential Governance Awareness | 0 | NO_ITEMS | Governance awareness present |
| X:guiding:sufficiency | guiding | sufficiency | Guided Adequacy Evidence | 1 | HAS_ITEMS | Upstream prerequisite status |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Record | 0 | NO_ITEMS | Governance record exhaustive |
| X:guiding:consistency | guiding | consistency | Coherent Governance Alignment | 0 | NO_ITEMS | Governance alignment coherent |
| X:applying:necessity | applying | necessity | Required Execution Foundation | 1 | HAS_ITEMS | Geotech dependency |
| X:applying:sufficiency | applying | sufficiency | Adequate Implementation Evidence | 0 | NO_ITEMS | Implementation evidence adequate |
| X:applying:completeness | applying | completeness | Complete Implementation Record | 0 | NO_ITEMS | Implementation record complete |
| X:applying:consistency | applying | consistency | Standardized Implementation Measure | 1 | HAS_ITEMS | Pipe size units |
| X:judging:necessity | judging | necessity | Essential Conformance Verdict | 0 | NO_ITEMS | Conformance verdicts present |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicative Basis | 0 | NO_ITEMS | Adjudicative basis sufficient |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Record | 0 | NO_ITEMS | Adjudicative record exhaustive |
| X:judging:consistency | judging | consistency | Consistent Adjudicative Measure | 0 | NO_ITEMS | Adjudicative measures consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Scrutiny Foundation | 1 | HAS_ITEMS | County approval verification |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Oversight Evidence | 0 | NO_ITEMS | Oversight evidence adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Record | 0 | NO_ITEMS | Oversight record exhaustive |
| X:reviewing:consistency | reviewing | consistency | Consistent Oversight Alignment | 0 | NO_ITEMS | Oversight alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Procedure | Guidance | Add guidance on how to proceed when upstream prerequisites (DEL-006-01, DEL-008-01, DEL-002) are not yet available -- document risk of proceeding without geotech or structural confirmation | Guided adequacy evidence lens: Procedure Prerequisites table lists seven upstream deliverables as required, but provides no guidance on sequencing risk if any are unavailable. For a design-build project, parallel design tracks are common, and the documents should address what happens if prerequisites are incomplete. | Procedure.md | Procedure.md#Prerequisites > Upstream Information Required | -- | PROPOSAL: Guidance directional | TBD |
| X-002 | X:applying:necessity | TBD_Question | Procedure | Datasheet | Record TBD: Confirm whether geotechnical investigation (DEL-008-01) has been completed; if cistern is below-grade, geotech is required before design can be finalized | Required execution foundation lens: Procedure Step 2.2 states "If below-grade: obtain geotech report (DEL-008-01) before finalizing design." The cistern installation type (above-grade vs. below-grade) is undetermined, and geotech status is unknown. This is a foundational execution prerequisite. | Procedure.md, Datasheet.md | Procedure.md#Step 2 (2.2), Datasheet.md#Cistern System (location row) | -- | PROPOSAL: Project Manager | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Guidance | Normalize pipe size notation: some locations use "2.5 inch", others "2.5"", others "2.5'" -- adopt single notation convention | Standardized implementation measure lens: Datasheet uses '2.5 inch' in one place and '2.5"' in another. Specification uses '2.5 inches (2.5")'. Procedure uses '2.5"' and '2.5 inch'. While these are clearly the same value, inconsistent notation across construction documents risks field confusion. | Datasheet.md, Specification.md, Procedure.md | Datasheet.md#Cistern System, Specification.md#R-004, Procedure.md#Step 1 (1.1) | -- | PROPOSAL: Guidance vocabulary note | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add verification step for County approval of preliminary design (Step 6) with documented acceptance record before proceeding to IFC | Essential scrutiny foundation lens: Procedure Step 6 describes County approval process but the Verification table does not include a pass criterion for County preliminary design approval. This is a contractual gate per RFP Section 3.3.2. | Procedure.md | Procedure.md#Step 6, Procedure.md#Verification | -- | PROPOSAL: Procedure operational check | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Directive Record | 0 | NO_ITEMS | Directive records authoritative |
| E:guiding:information | guiding | information | Clear Governance Transmission | 0 | NO_ITEMS | Governance transmission clear |
| E:guiding:knowledge | guiding | knowledge | Integrated Steering Mastery | 0 | NO_ITEMS | Steering mastery integrated |
| E:guiding:wisdom | guiding | wisdom | Prudent Governance Discernment | 0 | NO_ITEMS | Governance discernment prudent |
| E:applying:data | applying | data | Verified Execution Evidence | 1 | HAS_ITEMS | Interface information gap |
| E:applying:information | applying | information | Clear Execution Communication | 0 | NO_ITEMS | Execution communication clear |
| E:applying:knowledge | applying | knowledge | Proficient Deployment Mastery | 0 | NO_ITEMS | Deployment mastery adequate |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Execution judgment prudent |
| E:judging:data | judging | data | Evidenced Conformance Record | 1 | HAS_ITEMS | Pressure tank verification |
| E:judging:information | judging | information | Unambiguous Verdict Communication | 0 | NO_ITEMS | Verdict communication unambiguous |
| E:judging:knowledge | judging | knowledge | Integrated Adjudicative Mastery | 0 | NO_ITEMS | Adjudicative mastery integrated |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative wisdom principled |
| E:reviewing:data | reviewing | data | Verified Inspection Record | 0 | NO_ITEMS | Inspection records adequate |
| E:reviewing:information | reviewing | information | Clear Oversight Transmission | 0 | NO_ITEMS | Oversight transmission clear |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Oversight Mastery | 0 | NO_ITEMS | Oversight mastery integrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Discernment | 0 | NO_ITEMS | Oversight discernment principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Datasheet | Datasheet | Normalize interface table: add DEL-006-07 (Plumbing Calculation Package) as an explicit interface since Guidance and Procedure both reference it as the destination for cistern sizing and pump TDH calculations | Verified execution evidence lens: Datasheet Interface Information table lists four interfaces but omits DEL-006-07 which is referenced in Guidance (cistern sizing basis) and Procedure (Steps 2.1, 2.3). This interface is necessary for verified execution traceability. | Datasheet.md, Guidance.md, Procedure.md | Datasheet.md#Interface Information, Guidance.md#Principles > Cistern Sizing, Procedure.md#Step 2 (2.1, 2.3) | -- | PROPOSAL: Datasheet descriptive | TBD |
| E-002 | E:judging:data | MissingSlot | Specification | Specification | Add requirement and verification row for pressure tank (if included in design) -- currently Specification Documentation table lists it as TBD but no requirement governs its inclusion/exclusion decision | Evidenced conformance record lens: Specification Documentation table lists "Pressure tank details: TBD -- if hydropneumatic pressurization is included." Neither a requirement nor a verification criterion governs the decision to include or exclude the pressure tank. This is a conformance gap -- there is no record basis for judging whether the pressure tank decision was correctly made. | Specification.md | Specification.md#Documentation (Pressure tank details row), Specification.md#Requirements (entire section scanned) | -- | PROPOSAL: Specification normative | TBD |
