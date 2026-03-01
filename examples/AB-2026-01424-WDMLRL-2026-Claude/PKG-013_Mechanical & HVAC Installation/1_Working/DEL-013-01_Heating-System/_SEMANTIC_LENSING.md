# Semantic Lensing Register: DEL-013-01 High-Recovery Heating System

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-01_Heating-System/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-013-01_Heating-System/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements, Related Deliverables)
- _STATUS.md — DEL-013-01_Heating-System/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-013-01_Heating-System/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-013-01_Heating-System/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-013-01_Heating-System/Specification.md (Scope, Requirements REQ-001 through REQ-010, Standards, Verification, Documentation)
- Guidance.md — DEL-013-01_Heating-System/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-013-01_Heating-System/Procedure.md (Prerequisites, Steps Phases 1-5, Verification, Records)
- _REFERENCES.md — DEL-013-01_Heating-System/_REFERENCES.md (Primary References, Related Documentation, Standards)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document (AppliesToDoc):
  - Datasheet: 2
  - Specification: 14
  - Guidance: 3
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific code sections not enumerated |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Manufacturer installation specs TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ inspection criteria underspecified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 4.2 covers AHJ inspection; adequate |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Phase sequencing dependency on design |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure phases 1-5 provide adequate execution steps |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Performance criteria numeric values TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure provides adequate audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes value context for OBJ-001, OBJ-004 |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by commissioning acceptance and cost/benefit in Trade-offs |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Verification table provides quality check structure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta Safety Codes sections apply (e.g., gas code, mechanical code, electrical code) beyond the general reference to "Alberta Safety Codes" | REQ-003 references "Alberta Safety Codes" generically; prescriptive direction requires identifying which specific codes govern this installation to avoid ambiguity during compliance determination | Specification.md | REQ-003: Code-Compliant Installation | — | PROPOSAL: Mechanical Engineer to identify applicable code sections during design phase (DEL-003-07) | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement referencing manufacturer installation specifications as a mandatory practice once equipment is selected | REQ-003 lists "Manufacturer installation specifications" as applicable but no standalone requirement addresses mandatory adherence to manufacturer installation procedures as a normative practice | Specification.md | REQ-003: Code-Compliant Installation; Standards table | — | PROPOSAL: Add after equipment selection (DEL-003-07) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria defining what constitutes passing vs. failing the Safety Code inspection (scope of inspection, inspector qualifications, documentation required) | REQ-003 verification references "Safety Code inspection sign-off" but does not specify what the AHJ will inspect or what constitutes a pass; compliance determination lens reveals this gap | Specification.md | REQ-003 Verification; Verification table row for REQ-003 | — | PROPOSAL: AHJ determines scope; document expected inspection points | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit hold points or gate reviews between Phase 1 (Design Receipt) and Phase 2 (Procurement) to enforce the design-before-procurement principle stated in Guidance | Procedural direction should formalize the gate between design receipt and procurement as a hold point with sign-off, not just a narrative sequence | Procedure.md | Phase 1 / Phase 2 transition | — | PROPOSAL: Mechanical Engineer approval as formal gate | TBD |
| A-005 | A:operative:judging | TBD_Question | Specification | Specification | Record TBD: What are the quantitative performance acceptance criteria for heating output (BTU/h or kW), temperature uniformity, and recovery efficiency? | Performance assessment requires numeric thresholds; REQ-010 states capacity is TBD pending DEL-003-06; no interim acceptance criteria framework exists | Specification.md | REQ-010: Heating Capacity; Verification table row for REQ-010 | — | PROPOSAL: Mechanical Engineer (DEL-003-06/07) to define | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Key parameters TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Equipment not yet selected |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet is structured and covers known parameters |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Datasheet values are consistent with Specification and Guidance |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | BMS protocol undefined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate contextual framing |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive narrative |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are coherent on key messages |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles section establishes fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs and Considerations demonstrate expertise-level context |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Covered by comprehensive document set |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Fuel source decision unresolved |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic view of system role |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Heating capacity (BTU/h or kW), fuel/energy source confirmation, and electrical circuit sizing are essential facts that remain undefined | Three essential data points in the Datasheet are marked TBD; these are foundational facts required for procurement and installation | Datasheet.md | Attributes table: Heating Capacity, Fuel/Energy Source, Electrical Supply | — | PROPOSAL: DEL-003-06 (Mechanical Calculation Package) and DEL-003-07 (Mechanical Specification) | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add equipment weight, dimensions, and noise rating to Attributes once equipment is selected; these are needed for structural and acoustic adequacy assessments | Adequate evidence for equipment fit (REQ-005) requires physical parameters not currently in the Datasheet; dimensional drawings are mentioned in Procedure Step 1.2 but not captured as Datasheet attributes | Datasheet.md | Attributes table | — | PROPOSAL: Populate from equipment submittal after selection | TBD |
| B-003 | B:information:necessity | MissingSlot | Multi | Specification | Add requirement or TBD placeholder for BMS communication protocol (e.g., BACnet, Modbus, LON) and define minimum point list | Essential signal for controls integration: REQ-008 requires BMS integration but no protocol or point list is specified anywhere; Guidance Consideration D flags this as TBD but no Specification requirement captures it | Specification.md; Guidance.md | REQ-008: Controls Integration; Consideration D | — | PROPOSAL: Design team to specify BMS protocol in PKG-003/PKG-004 design phase | TBD |
| B-004 | B:wisdom:necessity | Conflict | Multi | Guidance | Surface the fuel source ambiguity as a formal design decision requiring resolution before procurement | Essential discernment: natural gas is assumed but not confirmed; Datasheet states "ASSUMPTION: natural gas"; Guidance Trade-off 3 and CONF-001 both flag this; the conflict between RFP gas tie-in reference and absence of explicit fuel assignment remains unresolved | Datasheet.md; Guidance.md | Datasheet Attributes: Fuel/Energy Source; Guidance Trade-off 3; CONF-001 | Datasheet.md#Attributes ("natural gas assumed"); Guidance.md#CONF-001 ("no explicit fuel assignment") | PROPOSAL: Mechanical Engineer confirms fuel source in DEL-003-07 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Obligation Threshold | 1 | HAS_ITEMS | ASHRAE standard numbers TBD |
| C:normative:sufficiency | normative | sufficiency | Certified Acceptability Basis | 1 | HAS_ITEMS | Acceptance basis depends on design outputs |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Standards table in Specification is comprehensive given current knowledge |
| C:normative:consistency | normative | consistency | Harmonized Conformance Benchmark | 0 | NO_ITEMS | Conformance references are consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Procedure prerequisites establish operational foundation adequately |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Functional Fitness | 0 | NO_ITEMS | Procedure verification table demonstrates fitness checks |
| C:operative:completeness | operative | completeness | Integrated Process Mastery | 1 | HAS_ITEMS | Integrated test scope may be incomplete |
| C:operative:consistency | operative | consistency | Reproducible Methodical Practice | 0 | NO_ITEMS | Procedure steps are sequenced and reproducible |
| C:evaluative:necessity | evaluative | necessity | Fundamental Merit Perception | 0 | NO_ITEMS | Value proposition is clear in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Professional Appraisal | 0 | NO_ITEMS | Trade-offs provide professional appraisal context |
| C:evaluative:completeness | evaluative | completeness | Holistic Appraisal Authority | 0 | NO_ITEMS | Guidance covers system-level value holistically |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Value alignment is principled and consistent with OBJ-001/OBJ-004 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Replace "ASHRAE Standards (HVAC systems)" with specific ASHRAE standard numbers (e.g., ASHRAE 90.1, ASHRAE 62.1) once mechanical design identifies applicable standards | The authoritative obligation threshold lens requires specific binding references; "ASHRAE standards" is too vague to serve as an enforceable normative obligation | Specification.md | Standards table: ASHRAE Standards row | — | PROPOSAL: Mechanical Engineer to specify applicable ASHRAE standards in DEL-003-07 | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-001 defining minimum thermal recovery efficiency percentage or COP that qualifies equipment as "high-recovery" | Certified acceptability basis requires a quantitative threshold for what constitutes "high-recovery"; REQ-001 verification references equipment documentation but no numeric acceptance threshold exists | Specification.md | REQ-001: System Type; Verification table row for REQ-001 | — | PROPOSAL: Mechanical Engineer to define recovery efficiency threshold in DEL-003-07 | TBD |
| C-003 | C:operative:completeness | VerificationGap | Procedure | Procedure | Add air balance verification as a specific test within Step 4.4 (Integrated HVAC System Test) to confirm building pressure is maintained within acceptable limits during simultaneous operation | Integrated process mastery requires confirming that all subsystem interactions produce a balanced result; Step 4.4 tests individual pairings but does not explicitly verify overall building air balance | Procedure.md | Phase 4, Step 4.4: Integrated HVAC System Test | — | PROPOSAL: Mechanical Engineer to define air balance acceptance criteria | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Imposed Regulatory Minimum | 1 | HAS_ITEMS | Minimum performance standards not quantified |
| F:normative:sufficiency | normative | sufficiency | Verified Regulatory Competence | 0 | NO_ITEMS | Verification matrix covers regulatory competence checks |
| F:normative:completeness | normative | completeness | Total Certification Mastery | 1 | HAS_ITEMS | Missing certification requirement |
| F:normative:consistency | normative | consistency | Disciplined Conformance Gauge | 0 | NO_ITEMS | Conformance approach is consistent |
| F:operative:necessity | operative | necessity | Validated Operational Readiness | 1 | HAS_ITEMS | Readiness criteria not fully formalized |
| F:operative:sufficiency | operative | sufficiency | Substantiated Process Capability | 0 | NO_ITEMS | Process steps substantiate capability |
| F:operative:completeness | operative | completeness | Exhaustive Operational Accounting | 0 | NO_ITEMS | Procedure Records table is comprehensive |
| F:operative:consistency | operative | consistency | Dependable Workflow Coherence | 0 | NO_ITEMS | Workflow is coherent and dependable |
| F:evaluative:necessity | evaluative | necessity | Warranted Value Comprehension | 0 | NO_ITEMS | Value is comprehended via Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Verdict | 1 | HAS_ITEMS | Energy efficiency value not quantified |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 0 | NO_ITEMS | Merit accounting is covered at appropriate level |
| F:evaluative:consistency | evaluative | consistency | Transparent Worth Rationale | 0 | NO_ITEMS | Worth rationale is transparent in Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify REQ-010 with placeholder for minimum heating output threshold (BTU/h or kW) and design temperature basis once DEL-003-06 is issued | Imposed regulatory minimum lens: REQ-010 states "sufficient heating capacity" without a numeric minimum; this vagueness makes verification subjective | Specification.md | REQ-010: Heating Capacity | — | PROPOSAL: DEL-003-06 Mechanical Calculation Package | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for gas-fitter certification and gas permit (if gas-fired) as a normative requirement, or flag as conditional on fuel source confirmation | Total certification mastery lens: if the system is gas-fired, Alberta requires certified gas-fitter installation and gas permits; this is not captured as a standalone requirement | Specification.md | Standards table; REQ-003 | — | PROPOSAL: Add conditional requirement pending fuel source confirmation | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a formal pre-installation readiness checklist that consolidates all Site Prerequisites into a single sign-off document with responsible parties and dates | Validated operational readiness lens: Procedure lists Site Prerequisites but does not formalize them as a single consolidated readiness gate with sign-off | Procedure.md | Prerequisites: Site Prerequisites | — | PROPOSAL: Mechanical Contractor to use consolidated checklist | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale explaining the expected energy efficiency benefit of high-recovery vs. conventional heating in terms of operating cost reduction or energy savings percentage | Substantiated worth verdict lens: Guidance states the system "enables the heat-recovery loop" but does not quantify the value proposition; a later enrichment pass should add expected benefit framing | Guidance.md | Purpose; Principle 1 | — | PROPOSAL: Mechanical Engineer to provide estimated recovery efficiency during design | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Mandatory Course | 0 | NO_ITEMS | Guidance Principle 5 and Specification REQ-003/004 settle the mandatory course |
| D:normative:applying | normative | applying | Enforced Compliance Fulfillment | 1 | HAS_ITEMS | Compliance enforcement mechanism underspecified |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Verification table provides conformance ruling structure |
| D:normative:reviewing | normative | reviewing | Compulsory Compliance Closure | 0 | NO_ITEMS | Safety Code inspection and commissioning report close compliance loop |
| D:operative:guiding | operative | guiding | Verified Methodical Steering | 0 | NO_ITEMS | Procedure Phase 1 provides methodical steering via design review |
| D:operative:applying | operative | applying | Confirmed Practical Delivery | 1 | HAS_ITEMS | Delivery confirmation mechanism underspecified |
| D:operative:judging | operative | judging | Resolved Capability Verdict | 0 | NO_ITEMS | Procedure Step 4.5 covers performance verdict |
| D:operative:reviewing | operative | reviewing | Confirmed Systematic Dependability | 0 | NO_ITEMS | Records section provides dependability evidence chain |
| D:evaluative:guiding | evaluative | guiding | Resolved Purposeful Merit | 0 | NO_ITEMS | Guidance Purpose resolves merit context |
| D:evaluative:applying | evaluative | applying | Finalized Benefit Delivery | 0 | NO_ITEMS | Commissioning confirms benefit delivery |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Verdict | 1 | HAS_ITEMS | Owner acceptance criteria not defined |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Inspection | 0 | NO_ITEMS | Procedure verification checks cover quality inspection |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Normalization | Multi | Guidance | Clarify who enforces compliance with manufacturer installation specifications during installation -- is it the Mechanical Engineer, a third-party inspector, or the Mechanical Contractor's QC? | Enforced compliance fulfillment lens: REQ-003 requires compliance with manufacturer specs but no document identifies who verifies this during installation (as distinct from the AHJ Safety Code inspection) | Specification.md; Procedure.md | REQ-003; Phase 3 steps | — | PROPOSAL: Define responsible party in Guidance or Specification | TBD |
| D-002 | D:operative:applying | MissingSlot | Specification | Specification | Add a formal substantial completion definition or milestone criteria that confirms when DEL-013-01 installation is complete and ready for commissioning | Confirmed practical delivery lens: no document defines what "substantial completion" means for this deliverable specifically; Procedure moves from installation to commissioning without a formal completion gate | Specification.md; Procedure.md | Phase 3 to Phase 4 transition | — | PROPOSAL: Define in Specification or Procedure | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add section describing Owner acceptance criteria or Owner's expected performance outcomes for the heating system beyond code compliance | Conclusive merit verdict lens: documents address contractor obligations and code compliance but do not describe the Owner's (Camrose County) specific expectations for heating system performance or satisfaction criteria at handover | Guidance.md | entire document scanned | — | PROPOSAL: Confirm with Owner/Project Manager what acceptance criteria apply beyond code | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanded Foundational Activation | 0 | NO_ITEMS | Procedure prerequisites establish activation foundations |
| X:guiding:sufficiency | guiding | sufficiency | Validated Directional Competence | 1 | HAS_ITEMS | Design team competence validation not addressed |
| X:guiding:completeness | guiding | completeness | Comprehensive Governance Record | 0 | NO_ITEMS | Documentation section in Specification covers governance records |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Transparency | 0 | NO_ITEMS | Documents are directionally consistent |
| X:applying:necessity | applying | necessity | Obligatory Action Foundation | 0 | NO_ITEMS | Prerequisites and IFC drawing requirement establish action foundation |
| X:applying:sufficiency | applying | sufficiency | Substantiated Delivery Justification | 1 | HAS_ITEMS | Submittal approval process verification gap |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Record | 0 | NO_ITEMS | Documentation table in Specification is comprehensive |
| X:applying:consistency | applying | consistency | Coherent Delivery Assurance | 0 | NO_ITEMS | Delivery assurance is coherent across docs |
| X:judging:necessity | judging | necessity | Binding Determination Foundation | 1 | HAS_ITEMS | Pass/fail criteria underspecified |
| X:judging:sufficiency | judging | sufficiency | Justified Determination Evidence | 0 | NO_ITEMS | Verification table provides evidence framework |
| X:judging:completeness | judging | completeness | Exhaustive Determination Record | 0 | NO_ITEMS | Records section covers determination records |
| X:judging:consistency | judging | consistency | Dependable Adjudication Coherence | 0 | NO_ITEMS | Adjudication approach is consistent |
| X:reviewing:necessity | reviewing | necessity | Obligatory Assurance Foundation | 1 | HAS_ITEMS | Warranty terms not captured |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Assurance Evidence | 0 | NO_ITEMS | Commissioning report provides assurance evidence |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Review | 1 | HAS_ITEMS | Guarantee period obligations underspecified |
| X:reviewing:consistency | reviewing | consistency | Dependable Assurance Transparency | 0 | NO_ITEMS | Assurance approach is transparent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | Normalization | Procedure | Guidance | Clarify terminology: Procedure references "Mechanical Engineer" as both the design reviewer and the commissioning authority, but does not distinguish between the P.Eng. of record and the Mechanical Contractor's engineer | Validated directional competence lens: "Mechanical Engineer" is used ambiguously in Procedure (design review vs. commissioning vs. sign-off roles); this risks confusion about who holds authority at each stage | Procedure.md; Specification.md | Phase 1, Step 1.2; Verification table | — | PROPOSAL: Define role terms in Guidance or a terminology note | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add verification step for equipment submittal approval -- confirm that submittal review and approval is documented before procurement proceeds | Substantiated delivery justification lens: Procedure Step 1.2 describes the submittal process but the Specification Verification table does not include submittal approval as a formal verification milestone | Specification.md | Verification table; Documentation table | — | PROPOSAL: Add to Verification table | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add explicit pass/fail criteria for the commissioning test (REQ-009) -- define what constitutes a failed commissioning test and the remediation path | Binding determination foundation lens: REQ-009 verification references "Commissioning report signed by Mechanical Contractor" but does not define what test results constitute a pass or fail | Specification.md | REQ-009: Performance Testing; Verification table row for REQ-009 | — | PROPOSAL: Define in commissioning plan (part of DEL-003-07 or commissioning scope) | TBD |
| X-004 | X:reviewing:necessity | MissingSlot | Specification | Specification | Add requirement or documentation artifact for warranty registration and warranty terms for installed equipment | Obligatory assurance foundation lens: Procedure Step 5.3 mentions "Warranty registration and terms" under O&M manuals but no Specification requirement mandates warranty documentation; this is an assurance gap | Specification.md; Procedure.md | Documentation table; Step 5.3 | — | PROPOSAL: Add warranty requirement to Specification | TBD |
| X-005 | X:reviewing:completeness | RationaleGap | Guidance | Guidance | Add guidance on the R-01 Section 2.10 Guarantee Period (10-day rectification obligation) and its implications for the heating system -- explain what this means for the Mechanical Contractor's post-commissioning obligations | Exhaustive assurance review lens: Procedure Step 5.4 references R-01 Section 2.10 but Guidance does not explain the guarantee period's implications or how it affects the heating system deliverable specifically | Guidance.md; Procedure.md | Guidance: entire document scanned; Procedure: Step 5.4 | — | PROPOSAL: Add to Guidance as a new Consideration | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Validated Directive Repository | 0 | NO_ITEMS | Reference documents are listed and traceable |
| E:guiding:information | guiding | information | Authoritative Orientation Signal | 0 | NO_ITEMS | Guidance provides authoritative orientation |
| E:guiding:knowledge | guiding | knowledge | Validated Governance Mastery | 1 | HAS_ITEMS | Governance of design-build interface |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Guidance Trade-offs and Considerations demonstrate foresight |
| E:applying:data | applying | data | Verified Execution Repository | 1 | HAS_ITEMS | As-built documentation scope |
| E:applying:information | applying | information | Substantiated Execution Account | 0 | NO_ITEMS | Procedure steps provide execution account |
| E:applying:knowledge | applying | knowledge | Demonstrated Execution Mastery | 0 | NO_ITEMS | Procedure demonstrates mastery of execution sequence |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 0 | NO_ITEMS | Procedure includes forward-looking deficiency rectification |
| E:judging:data | judging | data | Proven Adjudication Repository | 0 | NO_ITEMS | Verification and Records tables serve as adjudication repository |
| E:judging:information | judging | information | Grounded Judgment Account | 1 | HAS_ITEMS | Commissioning data requirements |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Mastery | 0 | NO_ITEMS | Verification structure demonstrates adjudication mastery |
| E:judging:wisdom | judging | wisdom | Principled Judgment Panorama | 0 | NO_ITEMS | Guidance Conflict Table provides principled judgment structure |
| E:reviewing:data | reviewing | data | Verified Inspection Repository | 0 | NO_ITEMS | Records table provides inspection repository |
| E:reviewing:information | reviewing | information | Grounded Audit Account | 0 | NO_ITEMS | Documentation artifacts support audit account |
| E:reviewing:knowledge | reviewing | knowledge | Verified Oversight Mastery | 1 | HAS_ITEMS | Oversight responsibility assignment |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Foresight | 0 | NO_ITEMS | Procedure addresses post-commissioning obligations |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | Normalization | Multi | Guidance | Standardize the use of "Mechanical Engineer" vs. "design team" vs. "Mechanical Contractor" when referring to design governance authority across all four documents | Validated governance mastery lens: documents use "Mechanical Engineer" (Specification, Procedure), "design team" (Guidance Consideration D), and "Mechanical Engineer (DEL-003-07)" (Datasheet) inconsistently when describing the design authority governing equipment selection and installation | Specification.md; Guidance.md; Datasheet.md; Procedure.md | Specification: REQ-003, Standards; Guidance: Consideration D; Datasheet: Attributes; Procedure: Phase 1 | — | PROPOSAL: Define canonical term in Guidance and apply consistently | TBD |
| E-002 | E:applying:data | VerificationGap | Specification | Specification | Add as-built drawing submission as a formal verification requirement (not just a documentation artifact) with acceptance criteria | Verified execution repository lens: as-built drawings are listed in the Documentation table but not in the Verification table; there is no formal acceptance criterion for as-built accuracy | Specification.md | Documentation table: As-built drawings; Verification table | — | PROPOSAL: Add to Verification table with acceptance criteria | TBD |
| E-003 | E:judging:information | WeakStatement | Procedure | Procedure | Strengthen Step 4.5 to require specific data points to be recorded (e.g., supply air temperature, return air temperature, recovery efficiency, airflow rate) rather than generic "performance data" | Grounded judgment account lens: Step 4.5 references "Record all performance data" without specifying which data points constitute a grounded judgment basis; this vagueness risks incomplete commissioning records | Procedure.md | Phase 4, Step 4.5: Performance Verification | — | PROPOSAL: Mechanical Engineer to define required data points in commissioning plan | TBD |
| E-004 | E:reviewing:knowledge | Conflict | Specification | Specification | Resolve whether the Mechanical Contractor or the Mechanical Engineer has final sign-off authority on commissioning acceptance | Verified oversight mastery lens: Specification Verification table assigns commissioning sign-off to "Mechanical Contractor" (REQ-009) while Procedure Step 5.1 submits the report to "Mechanical Engineer and Project Manager" for acceptance, creating ambiguity about who has final authority | Specification.md; Procedure.md | Specification: Verification table REQ-009; Procedure: Step 5.1 | Specification.md#Verification ("Mechanical Contractor") ; Procedure.md#Step-5.1 ("Mechanical Engineer and Project Manager") | PROPOSAL: Define in Specification that Mechanical Engineer accepts commissioning report | TBD |
