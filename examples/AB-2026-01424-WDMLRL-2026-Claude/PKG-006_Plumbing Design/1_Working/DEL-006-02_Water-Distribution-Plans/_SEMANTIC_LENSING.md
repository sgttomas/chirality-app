# Semantic Lensing Register: DEL-006-02 Water Distribution Plans

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-006_Plumbing Design/1_Working/DEL-006-02_Water-Distribution-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-02_Water-Distribution-Plans/_CONTEXT.md
- _STATUS.md — DEL-006-02_Water-Distribution-Plans/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-006-02_Water-Distribution-Plans/_SEMANTIC.md
- Datasheet.md — DEL-006-02_Water-Distribution-Plans/Datasheet.md
- Specification.md — DEL-006-02_Water-Distribution-Plans/Specification.md
- Guidance.md — DEL-006-02_Water-Distribution-Plans/Guidance.md
- Procedure.md — DEL-006-02_Water-Distribution-Plans/Procedure.md
- _REFERENCES.md — DEL-006-02_Water-Distribution-Plans/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 12
  - Guidance: 5
  - Procedure: 4
- By matrix:
  - A: 4  B: 3  C: 4  F: 5  D: 3  X: 6  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Hot water heating scope unresolved as prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Pipe material TBD -- mandatory practice cannot be applied |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standards list incomplete for compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit trail format defined for regulatory audit readiness |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction for drawing production |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are sequenced with clear actions |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure verification table covers step-level checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure addresses process audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section establishes value orientation adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance provides merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table in Specification addresses worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Code review checklist and P.Eng. stamp serve as quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Guidance | Resolve hot water provision scope: RFP does not explicitly require a water heater, yet washroom/laundry expansion implies hot water need. Confirm whether water heating is in scope of DEL-006-02 or a separate deliverable. | Prescriptive direction for the distribution network cannot be finalized without knowing if hot water piping is in scope. CF-001 in Guidance.md already flags this but no ruling exists. | Guidance.md, Specification.md | Guidance.md#Conflict Table CF-001; Specification.md#REQ-004, REQ-005 | Guidance.md#CF-001 Source A (no explicit heater) vs. Source B (implied hot water need) | Plumbing Engineer / County | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Specification | Confirm pipe material selection (currently TBD in Datasheet.md Construction section). Mandatory practice for potable water distribution requires a specified material. | Without a confirmed material, mandatory practice requirements (code compliance, installation standards) cannot be applied. | Datasheet.md | Datasheet.md#Construction | NA | Plumbing Engineer per DEL-006-08 | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Specify applicable code editions and clause references in the Standards table. Currently all entries are "ASSUMPTION: likely applicable" with "Location TBD". | Compliance determination requires specific, edition-identified standards. The current Standards table provides anticipated applicability only, which is insufficient for formal compliance judgment. | Specification.md | Specification.md#Standards | NA | Plumbing Engineer | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a defined format or template reference for the code review checklist (Step 8) and coordination review log (Step 7). Currently referenced by name only with no template or structure specified. | Regulatory audit readiness requires defined checklist formats so that audit evidence is consistent and traceable. | Procedure.md | Procedure.md#Step 8, Step 7, Records | NA | Project Manager / Plumbing Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Fixture flow rate data absent |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | RFP-sourced parameters are traceable in Datasheet |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Insulation and freeze protection parameters missing |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Unit inconsistency between cistern and septic values |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Scope boundaries are signaled between deliverables |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Cross-references to sibling deliverables provide context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Drawing sheet anticipated content is enumerated |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across docs are coherent re: cistern-fed design |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Cistern-first design principle is explained in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs table shows engineering judgment applied |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for INITIALIZED stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict Table in Guidance exercises discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off options present balanced judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Adequate for current stage |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add individual fixture flow rate demands (or reference to DEL-006-07 calculation outputs) for each fixture/tap in the Fixture and Tap Locations table. | Essential facts for pipe sizing are missing. The Datasheet lists fixture locations but not the flow rates that are the essential data for distribution design. | Datasheet.md | Datasheet.md#Fixture and Tap Locations | NA | Plumbing Engineer via DEL-006-07 | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add freeze protection design parameters: design temperature, insulation R-value or type, heat tracing wattage (if applicable). Currently "TBD" in Construction table. | The comprehensive record of system parameters is incomplete without freeze protection data, which Guidance identifies as a key consideration for Alberta climate. | Datasheet.md | Datasheet.md#Construction (Insulation row) | NA | Plumbing Engineer | TBD |
| B-003 | B:data:consistency | Normalization | Datasheet | Datasheet | Normalize measurement units: cistern volume is given in litres (50,000 L) while septic tank capacity is given in US Gallons (2,000 US Gal). Recommend consistent metric units throughout or explicit dual-unit notation. | Reliable measurement requires consistent unit conventions. Mixed imperial/metric units risk conversion errors in design and construction. | Datasheet.md | Datasheet.md#Key System Parameters | NA | Project team convention | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Threshold | 1 | HAS_ITEMS | Emergency shower standard not confirmed |
| C:normative:sufficiency | normative | sufficiency | Justified Conformance Basis | 1 | HAS_ITEMS | REQ-002 tepid water conformance basis incomplete |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Standards coverage is anticipatory, not exhaustive |
| C:normative:consistency | normative | consistency | Harmonized Compliance Standard | 0 | NO_ITEMS | No internal contradictions in normative requirements |
| C:operative:necessity | operative | necessity | Critical Procedural Foundation | 0 | NO_ITEMS | Procedure prerequisites table is populated |
| C:operative:sufficiency | operative | sufficiency | Substantiated Operational Competence | 0 | NO_ITEMS | Steps are detailed with outputs |
| C:operative:completeness | operative | completeness | Total Workflow Accounting | 1 | HAS_ITEMS | No step for freeze protection design |
| C:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Steps are sequentially consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Objectives linkage to OBJ-001/003/004 is present |
| C:evaluative:sufficiency | evaluative | sufficiency | Proven Fitness Appraisal | 0 | NO_ITEMS | Trade-offs adequately appraise fitness |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Portrait | 0 | NO_ITEMS | Adequate for current stage |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value propositions are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-002 Notes: replace "ASSUMPTION: emergency shower supply shall comply with ANSI Z358.1 or equivalent" with a confirmed standard identity once the Plumbing Engineer determines the applicable Alberta standard. | The compulsory compliance threshold for emergency shower supply remains an assumption rather than a binding requirement. Worker safety requirements should not rest on unconfirmed assumptions. | Specification.md | Specification.md#REQ-002 | NA | Plumbing Engineer | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for tepid water requirement in REQ-002 verification: specify temperature range, flow rate, and duration that constitute compliant emergency shower supply. | Justified conformance basis for emergency shower cannot be evaluated without measurable acceptance criteria. The verification approach says "flow rate and tepid water compliance verified by calculation or specification" but defines no thresholds. | Specification.md | Specification.md#Verification (REQ-002 row) | NA | Plumbing Engineer per applicable standard | TBD |
| C-003 | C:normative:completeness | WeakStatement | Specification | Specification | Resolve "ASSUMPTION: likely applicable" status for all five standards in the Standards table. Replace with confirmed applicability or record as TBD_Question with a plan to confirm. | Exhaustive regulatory coverage cannot be claimed when all cited standards are marked as assumptions with "Location TBD". | Specification.md | Specification.md#Standards | NA | Plumbing Engineer | TBD |
| C-004 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a procedure step (between Step 5 and Step 6, or within Step 6) for freeze protection design: determine which piping runs require insulation and/or heat tracing, document strategy, and coordinate with PKG-004 if heat tracing is selected. | Total workflow accounting is incomplete without a discrete step for freeze protection, which Guidance.md identifies as a key Alberta-climate consideration. | Procedure.md | Procedure.md#Steps (between Step 5 and Step 6) | NA | Plumbing Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Regulatory Command | 1 | HAS_ITEMS | No explicit requirement for freeze protection |
| F:normative:sufficiency | normative | sufficiency | Defensible Acceptance Criteria | 1 | HAS_ITEMS | Multiple verification approaches lack measurable criteria |
| F:normative:completeness | normative | completeness | Absolute Governance Inventory | 1 | HAS_ITEMS | No requirement addressing drawing revision control |
| F:normative:consistency | normative | consistency | Disciplined Conformance Logic | 0 | NO_ITEMS | Requirements do not contradict each other |
| F:operative:necessity | operative | necessity | Mandatory Readiness Input | 1 | HAS_ITEMS | CAD/BIM platform not confirmed |
| F:operative:sufficiency | operative | sufficiency | Competent Practice Stewardship | 0 | NO_ITEMS | Procedure steps are competently structured |
| F:operative:completeness | operative | completeness | Total Procedural Mastery | 0 | NO_ITEMS | Adequate for INITIALIZED stage |
| F:operative:consistency | operative | consistency | Consistent Operational Alignment | 0 | NO_ITEMS | No procedural inconsistencies detected |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Evidence | 1 | HAS_ITEMS | No quality gate between draft and IFC |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Judgment | 0 | NO_ITEMS | Trade-offs in Guidance provide justified judgment |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Authority | 0 | NO_ITEMS | Adequate for current stage |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Measure | 0 | NO_ITEMS | Quality measures are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add a requirement (REQ-012 or similar) for freeze protection of water supply piping in unheated or exposed areas, referencing Alberta climate conditions and applicable code provisions. | Freeze protection is identified as a key concern in Guidance.md (Alberta Climate section) and Datasheet.md (Insulation TBD), but no corresponding normative requirement exists in Specification.md. An obligatory regulatory command is absent for a safety-critical design parameter. | Specification.md, Guidance.md | Specification.md#Requirements (absent); Guidance.md#Considerations - Alberta Climate | NA | Plumbing Engineer | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-007 (Drawing Set Completeness): define what "complete and fully coordinated" means in testable terms (e.g., all SOW items traceable, all fixture connections shown, all coordination markups resolved). | Defensible acceptance criteria require measurable thresholds. REQ-007 verification says "completeness checklist review" but no checklist content or pass/fail criteria are defined. | Specification.md | Specification.md#REQ-007, Verification (REQ-007 row) | NA | Plumbing Engineer | TBD |
| F-003 | F:normative:completeness | MissingSlot | Specification | Specification | Add a requirement for drawing revision control: specify that all IFC sheets shall include revision number, date, description of change, and approval signature in the revision block. | The Specification notes "revision control and title block data consistent with the project drawing standard (TBD)" in the Documentation section but does not formalize this as a normative requirement. Absolute governance inventory is incomplete without it. | Specification.md | Specification.md#Documentation | NA | Project Manager | TBD |
| F-004 | F:operative:necessity | TBD_Question | Procedure | Procedure | Confirm CAD/BIM platform selection (Step 2 item 4 notes "TBD -- coordinate with project team; ASSUMPTION: AutoCAD or Revit MEP"). Record confirmed platform as a mandatory readiness input. | A mandatory readiness input for drawing production is unconfirmed. Platform choice affects file formats, coordination workflows (BIM clash detection), and deliverable format. | Procedure.md | Procedure.md#Step 2 | NA | Project Manager / Plumbing Engineer | TBD |
| F-005 | F:evaluative:necessity | VerificationGap | Specification | Procedure | Add a formal quality gate (internal review hold point) between draft drawing completion (Step 6) and interdisciplinary coordination issue (Step 7). Currently the Procedure moves directly from "Draft drawing set (internal review stage)" output to coordination review without a defined internal QA check. | Fundamental quality evidence requires a formal internal review before external coordination. Without a defined quality gate, the draft may be issued for coordination with unchecked errors. | Procedure.md | Procedure.md#Step 6, Step 7 | NA | Plumbing Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Directive Authority | 1 | HAS_ITEMS | Bulk fill scope boundary unresolved |
| D:normative:applying | normative | applying | Enforced Compliance Benchmark | 0 | NO_ITEMS | REQ-008 and REQ-009 establish compliance benchmarks |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | P.Eng. stamp serves as conclusive conformance ruling |
| D:normative:reviewing | normative | reviewing | Systematic Governance Scrutiny | 0 | NO_ITEMS | Safety Code Officer inspection provides governance scrutiny |
| D:operative:guiding | operative | guiding | Actionable Preparation Steering | 1 | HAS_ITEMS | Drawing numbering convention unresolved |
| D:operative:applying | operative | applying | Resolved Task Deployment | 0 | NO_ITEMS | Steps are actionable and sequenced |
| D:operative:judging | operative | judging | Conclusive Capability Finding | 0 | NO_ITEMS | Verification table provides capability checks |
| D:operative:reviewing | operative | reviewing | Settled Procedure Scrutiny | 0 | NO_ITEMS | Records section supports procedure scrutiny |
| D:evaluative:guiding | evaluative | guiding | Purposeful Quality Bearing | 1 | HAS_ITEMS | No explicit quality objectives for drawing set |
| D:evaluative:applying | evaluative | applying | Settled Worth Realization | 0 | NO_ITEMS | Objectives OBJ-001/003/004 linkage is clear |
| D:evaluative:judging | evaluative | judging | Definitive Quality Decree | 0 | NO_ITEMS | P.Eng. review constitutes quality decree |
| D:evaluative:reviewing | evaluative | reviewing | Settled Merit Benchmark | 0 | NO_ITEMS | Adequate for current stage |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Specification | Specification | Resolve bulk water fill scope boundary (CF-002): clarify whether distribution piping to the bulk fill connection is shown in DEL-006-02 or DEL-006-04. Update REQ-006 to reflect the definitive scope split. | Definitive directive authority for the drawing set requires an unambiguous scope boundary. CF-002 in Guidance.md flags this but no ruling exists, leaving REQ-006 ambiguous ("shall show, or reference by cross-drawing"). | Specification.md, Guidance.md | Specification.md#REQ-006; Guidance.md#Conflict Table CF-002 | Specification.md#REQ-006 (DEL-006-02 shows distribution) vs. Guidance.md#CF-002 (DEL-006-04 covers cistern/pump details) | Plumbing Engineer at preliminary design | TBD |
| D-002 | D:operative:guiding | Normalization | Procedure | Procedure | Resolve drawing numbering convention: Procedure Step 2 and Guidance.md both note "ASSUMPTION: P-100 series" but this is unconfirmed. Record confirmed convention or escalate to project team. | Actionable preparation steering requires a settled drawing numbering convention before drawing production begins. Currently an unresolved assumption. | Procedure.md, Guidance.md | Procedure.md#Step 2; Guidance.md#Considerations - Drawing Numbering | NA | Project Manager | TBD |
| D-003 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add explicit quality objectives for the drawing set (e.g., target coordination review cycle count, maximum unresolved RFIs at IFC, constructability review participation). Link to OBJ-003 (complete IFC documentation). | Purposeful quality bearing requires stated quality targets. The Guidance links to OBJ-001/003/004 but does not translate those into drawing-set-specific quality objectives that can guide the Plumbing Engineer's work. | Guidance.md | Guidance.md#Purpose | NA | Project Manager / Plumbing Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Binding Preparatory Directive | 1 | HAS_ITEMS | No verification of prerequisite completion |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Competence | 0 | NO_ITEMS | Guidance trade-offs provide steering |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Mastery | 0 | NO_ITEMS | Guidance covers key considerations |
| X:guiding:consistency | guiding | consistency | Harmonized Guidance Orientation | 0 | NO_ITEMS | Guidance is internally consistent |
| X:applying:necessity | applying | necessity | Obligatory Activation Basis | 1 | HAS_ITEMS | No hold point verifying DEL-006-01 approval before IFC |
| X:applying:sufficiency | applying | sufficiency | Justified Deployment Threshold | 1 | HAS_ITEMS | REQ-010 coordination verification lacks specificity |
| X:applying:completeness | applying | completeness | Exhaustive Execution Record | 0 | NO_ITEMS | Documentation table lists all artifacts |
| X:applying:consistency | applying | consistency | Stable Execution Coherence | 0 | NO_ITEMS | Execution approach is consistent |
| X:judging:necessity | judging | necessity | Binding Competence Determination | 1 | HAS_ITEMS | No pressure test acceptance criteria |
| X:judging:sufficiency | judging | sufficiency | Justified Competence Ruling | 0 | NO_ITEMS | P.Eng. stamp provides competence ruling |
| X:judging:completeness | judging | completeness | Exhaustive Competence Assessment | 1 | HAS_ITEMS | No verification of SOW coverage completeness |
| X:judging:consistency | judging | consistency | Coherent Competence Measure | 0 | NO_ITEMS | Competence measures are coherent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Scrutiny Foundation | 1 | HAS_ITEMS | No defined review cycle for Specification requirements |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Oversight Appraisal | 0 | NO_ITEMS | Code review and P.Eng. stamp provide oversight |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Oversight Account | 0 | NO_ITEMS | Records section is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Stable Oversight Indicator | 0 | NO_ITEMS | Oversight approach is stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | VerificationGap | Procedure | Procedure | Add a verification check confirming that all prerequisites in the Prerequisites table are satisfied (or formally waived) before proceeding past Step 1. Currently prerequisites are listed but no formal gate verifies their completion. | Binding preparatory directive requires verification that prerequisites are met. The Prerequisites table lists 11 items but no step formally checks their status before drawing production begins. | Procedure.md | Procedure.md#Prerequisites | NA | Project Manager | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Procedure | Add a formal hold point in Procedure (before Step 9) verifying that DEL-006-01 County approval has been received. REQ-011 requires IFC drawings to be based on approved preliminary design, but no explicit gate in the procedure enforces this. | Obligatory activation basis for IFC issue (DEL-006-01 approval) has a requirement (REQ-011) but no procedural enforcement mechanism. Step 4 notes the requirement but the verification check only says "County approval confirmed in writing" without specifying a hold point. | Specification.md, Procedure.md | Specification.md#REQ-011; Procedure.md#Step 4, Verification (Step 4 row) | NA | Project Manager | TBD |
| X-003 | X:applying:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-010 verification approach: specify what "coordinated with" means in verifiable terms (e.g., clash detection completed with zero category-A clashes, or coordination sign-off obtained from each discipline lead). | Justified deployment threshold for interdisciplinary coordination is weak. Verification says "coordination review meeting" and "clash detection review (if BIM used -- TBD)" without defining pass/fail criteria. | Specification.md | Specification.md#Verification (REQ-010 row) | NA | Plumbing Engineer | TBD |
| X-004 | X:judging:necessity | MissingSlot | Specification | Specification | Add pressure testing acceptance criteria: specify test pressure, hold duration, and acceptable pressure drop for the installed water distribution system. Reference applicable code clause. | Binding competence determination for the installed system requires pressure test criteria. Procedure Step 6 mentions "pressure testing requirements" in construction notes, but no acceptance criteria exist in the Specification. | Specification.md, Procedure.md | Specification.md#Requirements (absent); Procedure.md#Step 6 item 5 | NA | Plumbing Engineer per applicable code | TBD |
| X-005 | X:judging:completeness | VerificationGap | Specification | Specification | Add a verification approach for SOW traceability: confirm that every SOW item (SOW-0041, 0042, 0044, 0048, 0049, 0050) is traceable to specific drawing sheet content. Procedure Step 3 verification mentions this but Specification does not formalize it. | Exhaustive competence assessment requires verifiable SOW-to-drawing traceability. The Procedure verification for Step 3 mentions SOW traceability but this is not reflected as a formal verification requirement in the Specification. | Specification.md, Procedure.md | Specification.md#Verification (no SOW traceability row); Procedure.md#Verification (Step 3 row) | NA | Plumbing Engineer | TBD |
| X-006 | X:reviewing:necessity | RationaleGap | Specification | Guidance | Add rationale for when and how Specification requirements should be reviewed and updated during design development (e.g., after DEL-006-01 approval, after hydraulic calculations, before IFC). Currently requirements are stated but no review cadence is defined. | Mandatory scrutiny foundation requires a defined review cycle so that requirements remain current as the design evolves through preliminary to IFC stages. | Specification.md | Specification.md#Requirements (general) | NA | Plumbing Engineer / Project Manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Steering Record | 1 | HAS_ITEMS | Guidance Examples section has no design examples |
| E:guiding:information | guiding | information | Coherent Steering Account | 0 | NO_ITEMS | Guidance narrative is coherent |
| E:guiding:knowledge | guiding | knowledge | Expert Guidance Authority | 0 | NO_ITEMS | Guidance reflects appropriate engineering knowledge |
| E:guiding:wisdom | guiding | wisdom | Prudent Guidance Insight | 0 | NO_ITEMS | Conflict Table and trade-offs show prudent insight |
| E:applying:data | applying | data | Verified Execution Evidence | 1 | HAS_ITEMS | No drawing register template referenced |
| E:applying:information | applying | information | Contextual Execution Account | 0 | NO_ITEMS | Procedure steps provide contextual account |
| E:applying:knowledge | applying | knowledge | Expert Execution Authority | 0 | NO_ITEMS | Procedure reflects expert execution sequence |
| E:applying:wisdom | applying | wisdom | Prudent Execution Insight | 0 | NO_ITEMS | Procedure notes and caveats show prudent insight |
| E:judging:data | judging | data | Verified Competence Record | 0 | NO_ITEMS | Verification table provides competence record structure |
| E:judging:information | judging | information | Contextual Competence Ruling | 0 | NO_ITEMS | Verification approaches include relevant context |
| E:judging:knowledge | judging | knowledge | Expert Assessment Authority | 0 | NO_ITEMS | P.Eng. stamp embodies expert assessment authority |
| E:judging:wisdom | judging | wisdom | Prudent Assessment Insight | 0 | NO_ITEMS | Adequate for current stage |
| E:reviewing:data | reviewing | data | Verified Oversight Record | 1 | HAS_ITEMS | Inspection report format undefined |
| E:reviewing:information | reviewing | information | Contextual Audit Account | 0 | NO_ITEMS | Records table provides audit account structure |
| E:reviewing:knowledge | reviewing | knowledge | Expert Oversight Authority | 0 | NO_ITEMS | Safety Code Officer and P.Eng. provide oversight authority |
| E:reviewing:wisdom | reviewing | wisdom | Prudent Oversight Insight | 0 | NO_ITEMS | Adequate for current stage |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Guidance | Guidance | Populate the Examples section with at least a reference to comparable cistern-fed industrial shop plumbing designs or standard plumbing plan exemplars, if available. Currently states "No design examples are available in the source documents." | Verified steering record requires data-level evidence to support guidance. The Examples section acknowledges the absence but does not indicate whether comparable designs will be sought during design development. | Guidance.md | Guidance.md#Examples | NA | Plumbing Engineer | TBD |
| E-002 | E:applying:data | Normalization | Procedure | Procedure | Reference a specific drawing register template or format in Step 2 output ("Drawing register; drawing standard confirmed"). Currently no template or standard format is identified. | Verified execution evidence requires a defined artifact format. The Procedure calls for a "drawing register" as an output but provides no template, format, or required fields, risking inconsistent execution across team members. | Procedure.md | Procedure.md#Step 2 | NA | Project Manager | TBD |
| E-003 | E:reviewing:data | MissingSlot | Procedure | Procedure | Add format or template requirements for inspection reports listed in the Records table. Currently "Copies of all completed inspection reports" is listed with no format definition. | Verified oversight record requires defined data artifacts. Inspection reports are listed as a required record but no format, content requirements, or responsible party for format definition is specified. | Procedure.md | Procedure.md#Records (Inspection reports row) | NA | Project Manager / PKG-009 | TBD |
