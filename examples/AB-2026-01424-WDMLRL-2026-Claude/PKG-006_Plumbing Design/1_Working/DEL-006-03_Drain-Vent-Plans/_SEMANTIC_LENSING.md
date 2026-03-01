# Semantic Lensing Register: DEL-006-03 Drain & Vent Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-03_Drain-Vent-Plans/_CONTEXT.md
- _STATUS.md — DEL-006-03_Drain-Vent-Plans/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-006-03_Drain-Vent-Plans/_SEMANTIC.md (all matrices parsed: A, B, C, F, D, X, E)
- Datasheet.md — DEL-006-03_Drain-Vent-Plans/Datasheet.md (present)
- Specification.md — DEL-006-03_Drain-Vent-Plans/Specification.md (present)
- Guidance.md — DEL-006-03_Drain-Vent-Plans/Guidance.md (present)
- Procedure.md — DEL-006-03_Drain-Vent-Plans/Procedure.md (present)
- _REFERENCES.md — DEL-006-03_Drain-Vent-Plans/_REFERENCES.md (present; R-01, R-06, SOW-0016, OBJ-001/003/004)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 13
  - Guidance: 4
  - Procedure: 4
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 4
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific code edition not confirmed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp requirement is clear; code-specific practices TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification for code compliance requirements is generic |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately addressed across docs |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Service pit drain routing lacks procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps in Procedure cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantitative acceptance criteria for slope verification |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit points covered in Procedure verification table |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed through Guidance trade-offs |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application covered implicitly through design-build context |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination deferred to engineering judgment appropriately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by internal review step |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific edition of National Plumbing Code of Canada (or Alberta Plumbing Code) governs this design; current language says "ASSUMPTION: likely applicable; location TBD" | The prescriptive direction lens reveals that the governing code edition is stated as an assumption rather than a confirmed requirement, which could change design decisions | Specification.md | Standards table, REQ-006-03-023 | -- | Plumbing Engineer to confirm with Safety Codes authority | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm whether Alberta Building Code or Alberta Plumbing Code (standalone) applies; current Standards table lists both NPC and ABC as "ASSUMPTION: likely applicable" | Mandatory practice cannot be reliably applied when the governing code is unconfirmed | Specification.md | Standards table | -- | Safety Codes authority (Alberta) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific verification method for REQ-006-03-023 and REQ-006-03-024 (code compliance for drain pipe sizing and slope); current verification says only "Plumbing Safety Code inspection" without internal design verification step | Compliance determination requires a design-phase verification method, not just a construction-phase inspection | Specification.md | Verification table, REQ-006-03-020 to 024 | -- | Plumbing Engineer | TBD |
| A-004 | A:operative:guiding | RationaleGap | Guidance | Guidance | Add rationale for service pit/trench drain routing decision (septic vs. oil/water separator vs. separate collection); current text identifies the question but does not provide enough direction for the designer to proceed | The procedural direction for service pit drainage is identified as TBD but lacks sufficient guidance for the Plumbing Engineer to make an initial design decision | Guidance.md | Considerations > Service Pit Drain | -- | Plumbing Engineer + Environmental regulatory review | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Procedure | Add a verification check for drain pipe slope compliance against code minimums (e.g., field measurement of installed slopes); current Procedure verification table checks "Drain pipe sizing meets code" but does not specifically address slope measurement verification | Performance assessment for slopes requires a measurable check, not just a calculation review | Procedure.md | Verification table | -- | Plumbing Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Pipe materials TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Drawing scale and sheet count TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Vent system attributes largely TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units and references consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (scope, intent) adequately communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for design initiation |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Old North Shop existing conditions not documented |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across docs are coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Engineering fundamentals well represented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Deferred to Plumbing Engineer appropriately |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Thoroughness appropriate for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs appropriately surfaced in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment deferred to Plumbing Engineer appropriately |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view adequate for current stage |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add pipe material specifications (drain and vent) once determined by Plumbing Engineer; currently listed as "TBD" in System Parameters | Essential facts about pipe materials are missing; these are necessary design parameters for the drawing set | Datasheet.md | System Parameters table (Pipe material drain, Pipe material vent) | -- | Plumbing Engineer | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add drawing scale and sheet count once determined; both are listed as "TBD" in Drawing Set Scope | Adequate evidence for drawing production planning requires scale and sheet count to be established | Datasheet.md | Drawing Set Scope table (Drawing sheet count, Drawing scale) | -- | Plumbing Engineer | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add vent stack locations, vent termination details, and air admittance valve decisions once determined; all three are "TBD" in Vent System Elements | Comprehensive record of vent system elements is incomplete; all three vent attributes are TBD | Datasheet.md | Vent System Elements table | -- | Plumbing Engineer | TBD |
| B-004 | B:information:completeness | TBD_Question | Multi | Procedure | Record TBD: Existing drain/vent infrastructure in Old North Shop needs site investigation data before renovation scope can be fully designed; Procedure Step 1.3 identifies this but no information source is recorded | Comprehensive account of existing conditions is needed for the washroom renovation scope; field investigation has not occurred | Procedure.md; Guidance.md | Step 1.3; Considerations > Renovation of Old North Shop Washroom | -- | Plumbing Engineer (site investigation) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Basis | 1 | HAS_ITEMS | Oil/water separation regulatory requirement unconfirmed |
| C:normative:sufficiency | normative | sufficiency | Certified Conformance Adequacy | 0 | NO_ITEMS | Conformance adequacy pathway defined |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Environmental regulations for shop drainage not addressed |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Standards referenced consistently |
| C:operative:necessity | operative | necessity | Essential Process Knowledge | 0 | NO_ITEMS | Process knowledge adequate for current stage |
| C:operative:sufficiency | operative | sufficiency | Competent Operational Capacity | 0 | NO_ITEMS | Operational capacity appropriately scoped |
| C:operative:completeness | operative | completeness | Thorough Execution Coverage | 1 | HAS_ITEMS | Mezzanine drainage provision underspecified |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process discipline consistent across docs |
| C:evaluative:necessity | evaluative | necessity | Fundamental Value Appraisal | 0 | NO_ITEMS | Value orientation addressed in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Merit Assessment | 0 | NO_ITEMS | Merit assessment deferred appropriately |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Valuation | 0 | NO_ITEMS | Valuation scope appropriate |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Determine whether Alberta Environmental Protection regulations require oil/water separation for service pit drainage and shop floor drains before routing to septic | The obligatory compliance basis for service pit drainage is unknown; regulatory requirements for oil-bearing wastewater in an industrial shop may mandate separation equipment | Specification.md; Guidance.md | REQ-006-03-032; Considerations > Service Pit Drain; Trade-offs table row 4 | -- | Plumbing Engineer + Alberta Environmental authority | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add environmental regulatory requirements (if any) for shop floor drainage handling to Standards table; currently only plumbing code and building code are listed | Total regulatory coverage requires addressing environmental discharge regulations for an industrial maintenance shop, which are not currently referenced | Specification.md | Standards table | -- | Plumbing Engineer + Environmental regulatory review | TBD |
| C-003 | C:operative:completeness | WeakStatement | Specification | Specification | Strengthen REQ-006-03-033 regarding mezzanine drainage; current language says "ASSUMPTION: review required; conceptual drawing does not show upper-level fixtures" without a clear requirement or disposition | Thorough execution coverage requires a definitive statement on whether mezzanine/upper-level drainage is in or out of scope, rather than an open assumption | Specification.md | REQ-006-03-033 | -- | Plumbing Engineer + Architect | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Regulatory Baseline Imperative | 1 | HAS_ITEMS | Baseline code edition unconfirmed |
| F:normative:sufficiency | normative | sufficiency | Validated Mandate Threshold | 0 | NO_ITEMS | Mandate thresholds adequately framed |
| F:normative:completeness | normative | completeness | Exhaustive Mandate Authority | 1 | HAS_ITEMS | Cleanout spacing requirements absent |
| F:normative:consistency | normative | consistency | Systematic Mandate Coherence | 0 | NO_ITEMS | Mandates coherent across docs |
| F:operative:necessity | operative | necessity | Operational Capability Foundation | 1 | HAS_ITEMS | Frost depth data dependency not tracked |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Competence | 0 | NO_ITEMS | Execution competence adequately scoped |
| F:operative:completeness | operative | completeness | Total Procedural Mastery | 0 | NO_ITEMS | Procedural coverage comprehensive |
| F:operative:consistency | operative | consistency | Uniform Execution Discipline | 0 | NO_ITEMS | Execution discipline consistent |
| F:evaluative:necessity | evaluative | necessity | Grounded Quality Foundation | 1 | HAS_ITEMS | No quality criteria for drawing production |
| F:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Quality Judgment | 0 | NO_ITEMS | Quality judgment deferred to engineer |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth Mastery | 0 | NO_ITEMS | Worth mastery appropriate for stage |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Normalization | Multi | Guidance | Normalize code references: Specification uses "National Plumbing Code of Canada (or applicable Alberta edition)" and "Alberta Safety Codes Act -- Plumbing discipline" while Procedure uses "National Plumbing Code of Canada (applicable Alberta edition)" and "Alberta Safety Codes Act (Plumbing)"; align terminology | Regulatory baseline imperative requires consistent code naming across documents to avoid ambiguity about which code governs | Specification.md; Procedure.md | Standards table; Tools and Standards table | -- | Plumbing Engineer | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add explicit requirement for cleanout locations and spacing per plumbing code; REQ-006-03-004 mentions "cleanouts" in passing but no specific requirement addresses cleanout spacing, access, or sizing | Exhaustive mandate authority requires cleanout requirements to be explicitly stated since they are code-mandated elements | Specification.md | Requirements > System Coverage Requirements | -- | Plumbing Engineer | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite entry for frost depth data from geotechnical report; Procedure lists "Geotechnical report" as a prerequisite but does not specify frost depth as the critical parameter needed for drain burial depth design | Operational capability foundation requires frost depth data to be identified as the specific needed input, since drain burial depth depends on it and Alberta climate is a stated constraint | Procedure.md | Prerequisites > Documents and Information Required | -- | Plumbing Engineer | TBD |
| F-004 | F:evaluative:necessity | VerificationGap | Specification | Specification | Add drawing quality/completeness acceptance criteria (e.g., minimum content checklist items for IFC review); current verification for REQ-006-03-004 says "Drawing content review against checklist" but no checklist is defined or referenced | Grounded quality foundation requires that the acceptance checklist referenced in verification actually exists or is defined within the deliverable set | Specification.md | Verification table, REQ-006-03-004 | -- | Plumbing Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Governance Directive | 0 | NO_ITEMS | Governance directives well established |
| D:normative:applying | normative | applying | Validated Obligatory Action | 1 | HAS_ITEMS | Preliminary design content requirements underspecified |
| D:normative:judging | normative | judging | Decisive Conformance Authority | 0 | NO_ITEMS | Conformance authority adequately defined |
| D:normative:reviewing | normative | reviewing | Settled Compliance Inspection | 1 | HAS_ITEMS | Safety Code inspection coordination unclear |
| D:operative:guiding | operative | guiding | Established Workflow Readiness | 0 | NO_ITEMS | Workflow readiness adequately addressed |
| D:operative:applying | operative | applying | Validated Performance Delivery | 0 | NO_ITEMS | Performance delivery steps clear |
| D:operative:judging | operative | judging | Definitive Process Verdict | 0 | NO_ITEMS | Process verdict points identified |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Integrity | 0 | NO_ITEMS | Procedural integrity checks present |
| D:evaluative:guiding | evaluative | guiding | Established Merit Direction | 1 | HAS_ITEMS | No guidance on drawing set quality expectations |
| D:evaluative:applying | evaluative | applying | Validated Worth Deployment | 0 | NO_ITEMS | Worth deployment deferred to engineer |
| D:evaluative:judging | evaluative | judging | Definitive Merit Authority | 0 | NO_ITEMS | Merit authority delegated appropriately |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Merit Standard | 0 | NO_ITEMS | Merit standard deferred to IFC review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Clarify what constitutes the "preliminary plumbing design" for County approval (REQ-006-03-002); Procedure Step 2.5 describes content but Specification requirement does not specify minimum content for the preliminary submission | Validated obligatory action requires that the preliminary design submission scope be defined in the requirement, not just in the procedure | Specification.md; Procedure.md | REQ-006-03-002; Step 2.5 | -- | Plumbing Engineer + County requirements | TBD |
| D-002 | D:normative:reviewing | WeakStatement | Procedure | Specification | Clarify Safety Code inspection sequencing: Procedure Step 4.3 notes "County representative to be present at all inspections (SOW-0084)" but does not specify which inspections are required for the drain/vent work or when they occur in the construction sequence | Settled compliance inspection requires clear identification of inspection hold points for the drain/vent installation | Procedure.md | Steps > Phase 4; Verification table | -- | Plumbing Engineer + Safety Codes authority | TBD |
| D-003 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add guidance on expected drawing set quality level (e.g., level of detail for IFC vs. preliminary, industry-standard drawing conventions for plumbing) to orient the Plumbing Engineer on County expectations | Established merit direction requires that quality expectations for the drawing set be articulated, not left entirely implicit | Guidance.md | entire document scanned | -- | Plumbing Engineer + County | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Readiness Basis | 1 | HAS_ITEMS | Coordinate reference system TBD |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directive Competence | 0 | NO_ITEMS | Directive competence adequate |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Authority | 0 | NO_ITEMS | Guidance authority comprehensive for current stage |
| X:guiding:consistency | guiding | consistency | Coherent Directive Alignment | 1 | HAS_ITEMS | Inconsistent terminology for septic |
| X:applying:necessity | applying | necessity | Validated Execution Basis | 1 | HAS_ITEMS | Fixture unit load data dependency missing |
| X:applying:sufficiency | applying | sufficiency | Competent Implementation Evidence | 0 | NO_ITEMS | Implementation evidence adequate |
| X:applying:completeness | applying | completeness | Thorough Implementation Record | 0 | NO_ITEMS | Implementation record coverage appropriate |
| X:applying:consistency | applying | consistency | Consistent Implementation Measure | 0 | NO_ITEMS | Implementation measures consistent |
| X:judging:necessity | judging | necessity | Binding Determination Finding | 1 | HAS_ITEMS | Emergency shower flow rate not specified |
| X:judging:sufficiency | judging | sufficiency | Informed Compliance Verdict | 0 | NO_ITEMS | Compliance verdicts adequately framed |
| X:judging:completeness | judging | completeness | Comprehensive Verdict Authority | 0 | NO_ITEMS | Verdict authority comprehensive |
| X:judging:consistency | judging | consistency | Reliable Judgment Coherence | 1 | HAS_ITEMS | Conflict on septic tank terminology |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 0 | NO_ITEMS | Audit foundation established |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Audit Competence | 0 | NO_ITEMS | Audit competence adequate |
| X:reviewing:completeness | reviewing | completeness | Thorough Audit Mastery | 0 | NO_ITEMS | Audit mastery appropriate for stage |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Alignment | 0 | NO_ITEMS | Audit alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Datasheet | Datasheet | Add coordinate reference system (e.g., grid line references or tie-in to architectural coordinate system) once established; currently "TBD" in Drawing Set Scope | Foundational readiness basis requires a coordinate reference to align drain/vent plans with architectural and structural drawings | Datasheet.md | Drawing Set Scope table (Coordinate reference) | -- | Plumbing Engineer + Architect | TBD |
| X-002 | X:guiding:consistency | Normalization | Datasheet | Guidance | Normalize "septic holding tank" vs. "septic tank" terminology: Datasheet uses "Septic holding tank connection" and "Septic holding tank capacity" but also "Existing septic tank"; Specification uses "septic holding tank" consistently; align across all docs | Coherent directive alignment requires consistent terminology for the septic system to avoid confusion between "septic tank" (existing, to be removed) and "septic holding tank" (new, 2,000 US gal) | Datasheet.md; Specification.md | System Parameters; REQ-006-03-015, REQ-006-03-016 | -- | Plumbing Engineer | TBD |
| X-003 | X:applying:necessity | VerificationGap | Procedure | Specification | Add prerequisite or verification step for plumbing fixture unit load data from DEL-006-06 (Plumbing Fixture Schedule) before pipe sizing commences; Procedure lists it as prerequisite but no verification confirms the data has been received | Validated execution basis for pipe sizing depends on fixture unit loads; receipt of this input should be verified before Step 2.3 | Procedure.md | Prerequisites table (Plumbing fixture list/schedule); Step 2.3 | -- | Plumbing Engineer | TBD |
| X-004 | X:judging:necessity | WeakStatement | Guidance | Specification | Clarify emergency shower drain sizing requirements: Guidance notes "specific flow rate and sizing considerations" but neither Specification nor Datasheet specifies the flow rate or trap size for the emergency shower drain | Binding determination finding requires that the emergency shower drain be verifiable against a stated flow rate or sizing criterion | Guidance.md; Specification.md | Considerations > Emergency Shower Drain and Trap; REQ-006-03-012 | -- | Plumbing Engineer (per ANSI Z358.1 or applicable standard) | TBD |
| X-005 | X:judging:consistency | Conflict | Specification | Specification | Resolve terminology: REQ-006-03-016 says "The existing septic tank shall be removed" while Guidance Principle 3 says "The existing septic tank is to be removed and replaced with the new tank" and the Conflict Table CONF-006-03-02 notes the RFP says "potentially removal and relocate existing septic tank" vs. decomposition SOW-0043 "remove existing septic tank" | Reliable judgment coherence is impaired by the unresolved language between RFP "potentially" and the decomposition's definitive removal; this conflict is already noted but has HumanRuling=TBD | Specification.md; Guidance.md | REQ-006-03-016; Principle 3; Conflict Table CONF-006-03-02 | Specification.md#REQ-006-03-016 vs. Guidance.md#Principle-3 vs. RFP s3.4 | Decomposition SOW-0043 + SOW-0205 (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Governance Record | 1 | HAS_ITEMS | Trap primer requirements not recorded |
| E:guiding:information | guiding | information | Coherent Governance Signal | 0 | NO_ITEMS | Governance signals coherent |
| E:guiding:knowledge | guiding | knowledge | Authoritative Counsel Mastery | 0 | NO_ITEMS | Counsel mastery adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Insight | 0 | NO_ITEMS | Governance insight appropriate |
| E:applying:data | applying | data | Verified Implementation Record | 1 | HAS_ITEMS | As-built coordination not in Spec |
| E:applying:information | applying | information | Direct Implementation Account | 0 | NO_ITEMS | Implementation account direct and clear |
| E:applying:knowledge | applying | knowledge | Thorough Deployment Proficiency | 0 | NO_ITEMS | Deployment proficiency adequate |
| E:applying:wisdom | applying | wisdom | Informed Deployment Wisdom | 0 | NO_ITEMS | Deployment wisdom appropriately scoped |
| E:judging:data | judging | data | Documented Adjudication Finding | 1 | HAS_ITEMS | Verification grouping too coarse |
| E:judging:information | judging | information | Transparent Assessment Account | 0 | NO_ITEMS | Assessment account transparent |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Expertise | 0 | NO_ITEMS | Adjudication expertise adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Insight | 0 | NO_ITEMS | Adjudication insight appropriate |
| E:reviewing:data | reviewing | data | Documented Inspection Record | 1 | HAS_ITEMS | Revision tracking not addressed |
| E:reviewing:information | reviewing | information | Comprehensive Inspection Account | 0 | NO_ITEMS | Inspection account comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | Thorough Inspection Expertise | 0 | NO_ITEMS | Inspection expertise adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Wisdom | 0 | NO_ITEMS | Inspection wisdom appropriate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Guidance | Guidance | Add rationale for trap primer or trap seal maintenance provisions for intermittent-use drains (emergency shower, infrequently used floor drains); Guidance mentions "trap primers or trap seal maintenance provisions may be required" but does not provide enough direction | Substantiated governance record requires that the trap maintenance question be articulated with enough rationale for the Plumbing Engineer to make a design decision | Guidance.md | Considerations > Emergency Shower Drain and Trap | -- | Plumbing Engineer | TBD |
| E-002 | E:applying:data | RationaleGap | Procedure | Guidance | Add guidance note on as-built drawing coordination; Procedure Records table mentions "As-built survey coordination record" but no corresponding requirement exists in Specification and no guidance explains what as-built differences to expect or how to handle them | Verified implementation record requires that the as-built coordination expectation be grounded in a requirement or guidance rationale | Procedure.md | Records table (As-built survey coordination record) | -- | Plumbing Engineer + Surveyor | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Break out verification for REQ-006-03-010 through REQ-006-03-017 individually rather than as a group "REQ-006-03-010 to 017"; each system element has a distinct verification condition | Documented adjudication finding requires that each requirement's verification be individually traceable, not grouped into a single line | Specification.md | Verification table (REQ-006-03-010 to 017 row) | -- | Plumbing Engineer | TBD |
| E-004 | E:reviewing:data | Normalization | Specification | Specification | Add drawing revision tracking requirement or reference to revision control procedure; Specification Documentation table lists artifacts as "To be produced" but does not address how revisions will be numbered, tracked, or distributed | Documented inspection record requires that drawing revisions be trackable for audit purposes, especially given the preliminary-to-IFC workflow and possible permit-driven revisions | Specification.md | Documentation table | -- | Plumbing Engineer + Project Manager | TBD |
