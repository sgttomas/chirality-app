# Semantic Lensing Register: DEL-014-05 Emergency Shower

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-05_Emergency-Shower
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-05_Emergency-Shower/_CONTEXT.md
- _STATUS.md — DEL-014-05_Emergency-Shower/_STATUS.md (State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-05_Emergency-Shower/_SEMANTIC.md
- Datasheet.md — DEL-014-05_Emergency-Shower/Datasheet.md
- Specification.md — DEL-014-05_Emergency-Shower/Specification.md
- Guidance.md — DEL-014-05_Emergency-Shower/Guidance.md
- Procedure.md — DEL-014-05_Emergency-Shower/Procedure.md
- _REFERENCES.md — DEL-014-05_Emergency-Shower/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 3
  - Specification: 12
  - Guidance: 2
  - Procedure: 6
  - Multi: 1
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 9
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 1 new (F-001 standards hierarchy); 2 pre-existing in Guidance Conflict Table (CF-001 tepid water, CF-002 unit type) confirmed as adequately represented
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards referenced as ASSUMPTION lack confirmed applicability |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Pipe material/size TBD affects mandatory practice definition |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Acceptance criteria for some requirements are weak |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection and audit steps well-covered in Procedure and Specification |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear step-by-step direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | No explicit installer qualification requirement |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Commissioning test in Procedure Step 9 covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered via Safety Code inspections |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section establishes life-safety value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No explicit quality grading or merit criteria for unit selection |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-1 through T-3 in Guidance address worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Confirm applicability of ANSI/ISEA Z358.1 and Alberta OH&S Code Part 16 -- currently marked ASSUMPTION throughout all documents. Obtain authoritative confirmation and update Standards table accordingly. | Multiple requirements (REQ-ES-004 through REQ-ES-010) depend on standards whose applicability is assumed but not confirmed. This creates uncertainty in prescriptive direction. | Specification.md | ## Standards | -- | Plumbing designer or Alberta OH&S authority | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add confirmed values for pipe material, pipe size, finish/material, activation mechanism, signage type, accessibility clearance dimension once IFC design is available. | Datasheet Attributes table has 8+ TBD entries. Mandatory practice cannot be fully defined until these are resolved. | Datasheet.md | ## Attributes | -- | IFC plumbing drawings | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Strengthen REQ-ES-004 acceptance criterion: specify the numeric minimum flow rate rather than "sufficient to meet the applicable standard requirement." | REQ-ES-004 uses "sufficient to meet the applicable standard requirement" without stating the numeric threshold inline. Verification table says ">= minimum required LPM (TBD per standard)." Compliance determination requires a concrete value. | Specification.md | ### REQ-ES-004 -- Water Flow Rate | -- | Plumbing designer to confirm numeric value | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add a prerequisite or note specifying required installer qualifications (e.g., licensed plumber under Alberta Safety Codes Act). | Procedure lists prerequisites for permits, drawings, and equipment but does not state who is qualified to perform the installation. Practical execution depends on qualified personnel. | Procedure.md | ## Prerequisites | -- | Alberta Safety Codes Act requirements | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Specification | Specification | Add equipment selection criteria or minimum quality tier for the emergency shower unit (e.g., listed manufacturer, corrosion-resistant materials, expected service life). | REQ-ES-001 requires compliance with codes but provides no merit criteria for selecting among compliant units. Merit application under this lens suggests documenting minimum quality expectations. | Specification.md | ### REQ-ES-001 -- Unit Supply and Compliance | -- | Plumbing designer or Owner preference | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Water supply pressure is TBD -- essential operating fact missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence from conceptual drawings is adequate for current stage |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet has significant TBD gaps |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement parameters identified in Verification tables are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Upstream dependency status signaling mechanism not defined |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequately established through cross-references |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope inclusions/exclusions well documented in Specification |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents present coherent messaging about scope and requirements |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance establishes fundamental understanding of emergency shower purpose and constraints |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Adequate expertise requirements implied through code compliance |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of relevant knowledge domains is appropriate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 1 | HAS_ITEMS | Terminology inconsistency for unit type |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs and conflict table provide appropriate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Conflict table defers appropriately to human judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective on dependencies and constraints |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across Guidance principles and trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add water supply pressure requirement or design basis once IFC design is available. Currently TBD. | Water supply pressure is an essential operating fact for verifying the unit can deliver the required flow rate. Without it, REQ-ES-004 verification cannot be fully planned. | Datasheet.md | ## Attributes, row "Water supply pressure" | -- | IFC plumbing design | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add electrical interface requirement row to Attributes table (alarm, indicator light, or confirmation that no electrical interface is needed). | Specification exclusions mention "Electrical work, if any alarm or indicator light is required" but Datasheet does not record whether an electrical interface exists. This leaves a gap in the comprehensive record. | Datasheet.md; Specification.md | Datasheet ## Attributes; Specification ## What This Deliverable Excludes | -- | Plumbing designer | TBD |
| B-003 | B:information:necessity | RationaleGap | Procedure | Guidance | Add guidance note explaining how the construction team will know DEL-014-01 (cistern/distribution) is ready before commencing emergency shower work. Define the upstream-ready signal or handoff protocol. | Procedure prerequisites require DEL-014-01 to be roughed-in and pressure tested, but no mechanism is described for confirming this status. The essential signal for sequencing is missing. | Procedure.md | ## Prerequisites, row "DEL-014-01" | -- | Project management team | TBD |
| B-004 | B:knowledge:consistency | Normalization | Multi | Guidance | Standardize terminology for the unit type across documents. Datasheet uses "Emergency shower (combination shower/eyewash ASSUMPTION)"; Specification says "combination shower/eyewash ASSUMPTION" in scope but requirements text uses "emergency shower" alone; Procedure uses both. Recommend a single defined term with the ASSUMPTION clearly flagged in one place. | Inconsistent naming could cause confusion during procurement. Under the coherent understanding lens, terminology should be uniform. | Datasheet.md; Specification.md; Procedure.md | Datasheet ## Attributes row "Unit type"; Specification ## Scope; Procedure Step 6 | -- | Resolve via CF-002 ruling | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Regulatory Obligation | 1 | HAS_ITEMS | Enforceability weakened by unconfirmed standards |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Compliance Adequacy | 0 | NO_ITEMS | Verification table provides adequate compliance demonstration path |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Potential gap in National Plumbing Code requirements |
| C:normative:consistency | normative | consistency | Harmonized Compliance Standard | 0 | NO_ITEMS | Standards table is internally consistent |
| C:operative:necessity | operative | necessity | Critical Operational Readiness | 0 | NO_ITEMS | Prerequisites table and Step 9 commissioning address operational readiness |
| C:operative:sufficiency | operative | sufficiency | Verified Execution Competence | 0 | NO_ITEMS | Verification checks in Procedure are sufficient |
| C:operative:completeness | operative | completeness | Comprehensive Operational Delivery | 0 | NO_ITEMS | Steps 1-10 cover full delivery lifecycle |
| C:operative:consistency | operative | consistency | Disciplined Operational Uniformity | 0 | NO_ITEMS | Procedure follows consistent structure throughout |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Recognition | 0 | NO_ITEMS | Guidance Purpose section establishes foundational worth |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Appraisal | 0 | NO_ITEMS | Trade-offs section provides defensible rationale |
| C:evaluative:completeness | evaluative | completeness | Thorough Value Assessment | 1 | HAS_ITEMS | No lifecycle cost or total cost of ownership consideration |
| C:evaluative:consistency | evaluative | consistency | Calibrated Quality Standard | 0 | NO_ITEMS | Quality expectations consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen enforceability: for each requirement currently marked ASSUMPTION, add a resolution path and timeline (e.g., "To be confirmed by plumbing designer at IFC stage; if not confirmed by [milestone], escalate to Owner"). | Under the "Enforceable Regulatory Obligation" lens, requirements whose basis is entirely ASSUMPTION lack enforceability. A resolution path would strengthen them. | Specification.md | ## Requirements (multiple REQ-ES entries) | -- | Project management team | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement or note addressing National Plumbing Code of Canada requirements specifically (currently listed in Standards table as "ASSUMPTION: Likely applicable" but no requirement references it). | The Standards table lists NPC as likely applicable but no requirement in the Requirements section traces to it. Under the exhaustive regulatory coverage lens, this is a gap. | Specification.md | ## Standards; ## Requirements | -- | Plumbing designer | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a note in Trade-offs or Considerations addressing lifecycle cost implications (maintenance, annual testing labor, replacement parts) for the Owner post-handover. | Under thorough value assessment, the documents focus on installation cost trade-offs (T-1, T-2) but do not address ongoing maintenance/testing costs that affect total value. This is relevant for Owner orientation. | Guidance.md | ## Trade-offs | -- | Owner / facility manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Statutory Foundation | 1 | HAS_ITEMS | Statutory foundation incomplete due to unconfirmed codes |
| F:normative:sufficiency | normative | sufficiency | Mandated Conformance Threshold | 1 | HAS_ITEMS | Numeric thresholds TBD |
| F:normative:completeness | normative | completeness | Complete Jurisdictional Compliance | 0 | NO_ITEMS | Jurisdictional scope addressed in Standards table |
| F:normative:consistency | normative | consistency | Traceable Regulatory Coherence | 0 | NO_ITEMS | Source references are consistent and traceable |
| F:operative:necessity | operative | necessity | Essential Execution Prerequisite | 1 | HAS_ITEMS | Missing prerequisite for water quality verification |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capability Adequacy | 0 | NO_ITEMS | Capability demonstration addressed via commissioning tests |
| F:operative:completeness | operative | completeness | Total Execution Coverage | 0 | NO_ITEMS | Steps cover full execution scope |
| F:operative:consistency | operative | consistency | Stable Process Coherence | 0 | NO_ITEMS | Process steps are coherent and sequenced properly |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Imperative | 0 | NO_ITEMS | Life-safety merit imperative well-established |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal Capacity | 0 | NO_ITEMS | Appraisal methods defined in Verification tables |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 1 | HAS_ITEMS | No accounting for downtime risk if unit fails post-handover |
| F:evaluative:consistency | evaluative | consistency | Principled Worth Benchmark | 0 | NO_ITEMS | Worth benchmarks consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Conflict | Specification | Specification | Confirm which standard governs if ANSI/ISEA Z358.1 and Alberta OH&S Code Part 16 differ on requirements (e.g., tepid water range, flow rate, flush duration). Specification REQ-ES-001 says "if Alberta OH&S Code Part 16 specifies a different or additional standard, that requirement shall govern" -- but this hierarchy is stated only once and not reinforced in other requirements. | Under the Mandatory Statutory Foundation lens, a clear hierarchy of authority between potentially conflicting standards is needed. The hierarchy statement in REQ-ES-001 should be referenced or restated where specific numeric thresholds are cited. | Specification.md | ### REQ-ES-001; ### REQ-ES-004; ### REQ-ES-005 | Specification.md#REQ-ES-001 (Alberta governs) vs. Specification.md#REQ-ES-004 and #REQ-ES-005 (cite ANSI/ISEA Z358.1 values as ASSUMPTION) | Plumbing designer / Alberta OH&S authority | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add specific numeric acceptance threshold for water temperature verification -- currently states "16-38C (ASSUMPTION; confirm per standard)" in Procedure Verification table. The Specification REQ-ES-005 should state the definitive range once standards are confirmed. | Under Mandated Conformance Threshold, the tepid water temperature range is stated as ASSUMPTION in multiple places. A confirmed, authoritative numeric range is needed for verification to be meaningful. | Specification.md; Procedure.md | Specification ### REQ-ES-005; Procedure ## Verification row "Water temperature" | -- | Applicable standard (once confirmed) | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a prerequisite or step verifying that the non-potable water quality is acceptable for emergency shower use (per Guidance C-2). | Guidance C-2 raises the question of water quality acceptability but neither Specification requirements nor Procedure prerequisites include a verification step for it. Under Essential Execution Prerequisite, this is a gap. | Guidance.md; Procedure.md | Guidance ## Considerations C-2; Procedure ## Prerequisites | -- | Plumbing designer | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a note addressing the consequence of emergency shower failure or unavailability (e.g., regulatory shutdown risk, worker safety exposure) to strengthen the rationale for redundancy or backup planning. | Under Exhaustive Value Accounting, the documents do not account for the operational risk if the emergency shower becomes non-functional (e.g., cistern empty, pump failure). Guidance P-3 mentions the dependency but does not quantify or address the consequence. | Guidance.md | ## Principles P-3 | -- | Owner / OH&S officer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Legislative Direction | 0 | NO_ITEMS | Legislative direction established via RFP and Safety Codes references |
| D:normative:applying | normative | applying | Enforced Compliance Execution | 1 | HAS_ITEMS | No hold point defined for code-critical steps |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Safety Code inspections provide conformance rulings |
| D:normative:reviewing | normative | reviewing | Mandated Compliance Assurance | 0 | NO_ITEMS | Inspection reports and County representative presence provide assurance |
| D:operative:guiding | operative | guiding | Readiness Governance Pathway | 1 | HAS_ITEMS | No explicit go/no-go gate between installation and commissioning |
| D:operative:applying | operative | applying | Verified Hands-On Deployment | 0 | NO_ITEMS | Procedure Steps 4-6 provide detailed hands-on deployment guidance |
| D:operative:judging | operative | judging | Delivery Capability Adjudication | 0 | NO_ITEMS | Commissioning test serves as delivery adjudication |
| D:operative:reviewing | operative | reviewing | Systematic Process Confirmation | 0 | NO_ITEMS | Verification table in Procedure provides systematic confirmation |
| D:evaluative:guiding | evaluative | guiding | Principled Worth Direction | 0 | NO_ITEMS | Guidance Principles P-1 through P-5 establish worth direction |
| D:evaluative:applying | evaluative | applying | Settled Worth Realization | 0 | NO_ITEMS | Trade-offs guide worth realization decisions |
| D:evaluative:judging | evaluative | judging | Conclusive Value Ruling | 1 | HAS_ITEMS | No post-commissioning performance monitoring period defined |
| D:evaluative:reviewing | evaluative | reviewing | Systematic Merit Assurance | 0 | NO_ITEMS | Owner orientation step provides handover of merit assurance to Owner |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Procedure | Procedure | Define an explicit hold point after rough-in inspection (Step 5) before unit installation (Step 6) can proceed -- currently implied by "Re-inspection required before proceeding" but not formally designated as a hold point. | Under Enforced Compliance Execution, the transition from rough-in to unit installation is a code-critical gate. Formalizing it as a hold point strengthens enforceability. | Procedure.md | ### Step 5 -- Rough-In Inspection, substep 5.4 | -- | Project management team | TBD |
| D-002 | D:operative:guiding | VerificationGap | Procedure | Procedure | Add an explicit readiness checkpoint between final Safety Code inspection (Step 8) and commissioning flow test (Step 9) confirming all prerequisites are met (DEL-014-01 operational, DEL-014-04 clear, inspection passed). | Under Readiness Governance Pathway, the transition from inspection to commissioning should have a formal gate. Steps 8 and 9 are sequential but the go/no-go is not explicit. | Procedure.md | ### Step 8; ### Step 9 | -- | Project management team | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Specification | Guidance | Add guidance on whether a post-commissioning monitoring period is required before the emergency shower is considered fully accepted (e.g., a 30-day operational period before final acceptance). | Under Conclusive Value Ruling, the documents go from commissioning test directly to Owner orientation with no defined period to confirm sustained performance. For life-safety equipment, a monitoring period may be warranted. | Specification.md; Guidance.md | Specification ## Verification; Guidance ## Considerations | -- | Owner / contract terms | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Preparedness Mandate | 0 | NO_ITEMS | Preparedness mandates established in prerequisites |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Preparatory Guidance | 0 | NO_ITEMS | Guidance provides sufficient preparatory context |
| X:guiding:completeness | guiding | completeness | Total Stewardship Documentation | 1 | HAS_ITEMS | Documentation list may be incomplete |
| X:guiding:consistency | guiding | consistency | Aligned Governance Metric | 0 | NO_ITEMS | Governance metrics are aligned across documents |
| X:applying:necessity | applying | necessity | Critical Implementation Basis | 0 | NO_ITEMS | Implementation basis established via IFC drawings dependency |
| X:applying:sufficiency | applying | sufficiency | Sufficient Deployment Proof | 0 | NO_ITEMS | Deployment proof addressed via inspection reports and test records |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | As-built requirement could be strengthened |
| X:applying:consistency | applying | consistency | Repeatable Delivery Measure | 0 | NO_ITEMS | Measurement methods are repeatable and clearly described |
| X:judging:necessity | judging | necessity | Definitive Fitness Finding | 0 | NO_ITEMS | Fitness findings will come from Safety Code inspections and commissioning |
| X:judging:sufficiency | judging | sufficiency | Sufficient Fitness Assessment | 0 | NO_ITEMS | Assessment methods sufficient for scope |
| X:judging:completeness | judging | completeness | Comprehensive Fitness Record | 0 | NO_ITEMS | Records section covers expected documentation |
| X:judging:consistency | judging | consistency | Uniform Judgment Measure | 0 | NO_ITEMS | Judgment measures are uniform across Verification tables |
| X:reviewing:necessity | reviewing | necessity | Critical Assurance Validation | 0 | NO_ITEMS | Assurance validation addressed via County representative presence at inspections |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Assurance Evidence | 1 | HAS_ITEMS | Warranty verification method is weak |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Audit | 0 | NO_ITEMS | Audit trail established through records requirements |
| X:reviewing:consistency | reviewing | consistency | Stable Assurance Benchmark | 0 | NO_ITEMS | Benchmarks are stable across verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add a documentation requirement for the thermostatic mixing valve (if installed): manufacturer data, settings, and maintenance instructions. Currently the Documentation section lists 6 items but does not explicitly include the mixing valve. | Under Total Stewardship Documentation, if a thermostatic mixing valve is installed per CF-001, its documentation should be explicitly required for Owner maintenance. | Specification.md | ## Documentation | -- | Plumbing designer (once CF-001 resolved) | TBD |
| X-002 | X:applying:completeness | WeakStatement | Specification | Specification | Strengthen as-built documentation requirement: specify that as-built drawings must include pipe sizes, materials, valve locations, and clearance zone dimensions -- not just "final unit location, supply pipe routing, and drain connection." | Under Exhaustive Implementation Record, the as-built requirement (Documentation item 4) is general. Adding specific required content ensures the record is complete. | Specification.md | ## Documentation, item 4 | -- | Project management team | TBD |
| X-003 | X:reviewing:sufficiency | VerificationGap | Specification | Specification | Add a verification method for REQ-ES-012 (Warranty) beyond "CCDC 14-2013 guarantee period obligations in place." Specify what documentary evidence confirms warranty is in effect (e.g., signed warranty certificate, contractor letter). | Under Sufficient Assurance Evidence, the warranty verification row in the Specification Verification table is procedurally vague. Concrete evidence requirements would strengthen assurance. | Specification.md | ## Verification, row "REQ-ES-012 (Warranty)" | -- | Contract administrator | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Stewardship Record | 0 | NO_ITEMS | Records requirements cover stewardship data needs |
| E:guiding:information | guiding | information | Coherent Stewardship Signal | 0 | NO_ITEMS | Information flow is coherent through document cross-references |
| E:guiding:knowledge | guiding | knowledge | Informed Stewardship Mastery | 0 | NO_ITEMS | Knowledge requirements adequate for current stage |
| E:guiding:wisdom | guiding | wisdom | Principled Stewardship Vision | 0 | NO_ITEMS | Guidance Principles provide principled vision |
| E:applying:data | applying | data | Substantiated Delivery Record | 0 | NO_ITEMS | Delivery records addressed in Procedure Records section |
| E:applying:information | applying | information | Situated Execution Intelligence | 0 | NO_ITEMS | Execution context adequately situated in Procedure |
| E:applying:knowledge | applying | knowledge | Verified Execution Proficiency | 0 | NO_ITEMS | Verification of execution addressed via inspections and tests |
| E:applying:wisdom | applying | wisdom | Prudent Delivery Judgment | 0 | NO_ITEMS | Guidance trade-offs support prudent delivery judgment |
| E:judging:data | judging | data | Substantiated Suitability Record | 1 | HAS_ITEMS | Equipment submittal review criteria not specified |
| E:judging:information | judging | information | Informed Suitability Verdict | 0 | NO_ITEMS | Information for suitability verdict available through submittals and inspections |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Mastery | 0 | NO_ITEMS | Adjudication authority clear (Safety Code authority, County representative) |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Conflict table preserves human adjudication wisdom |
| E:reviewing:data | reviewing | data | Verified Audit Record | 0 | NO_ITEMS | Audit records addressed through inspection reports |
| E:reviewing:information | reviewing | information | Comprehensive Audit Intelligence | 0 | NO_ITEMS | Audit information requirements adequate |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Audit Mastery | 0 | NO_ITEMS | Audit authority clearly assigned |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Wisdom | 1 | HAS_ITEMS | No lessons-learned or close-out review mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:judging:data | Normalization | Specification | Specification | Specify the criteria for reviewing the equipment submittal (Specification Verification table row REQ-ES-001): what specific data points must the submittal contain to confirm compliance (e.g., listed standard, flow rate, temperature range, materials of construction)? | Under Substantiated Suitability Record, the verification method "Review equipment submittal/data sheet against applicable standard" does not define what data points constitute a passing review. This could lead to inconsistent suitability judgments. | Specification.md | ## Verification, row "REQ-ES-001 (Unit compliance)" | -- | Plumbing designer | TBD |
| E-002 | E:reviewing:wisdom | Normalization | Procedure | Procedure | Add a close-out review step or note after Step 10 capturing lessons learned, deficiency resolution log, and confirmation that all records have been submitted to the Owner. | Under Principled Oversight Wisdom, the Procedure ends at Owner Orientation (Step 10) with no formal close-out review. For life-safety equipment, a documented close-out ensures nothing is overlooked. | Procedure.md | ## Steps (after Step 10) | -- | Project management team | TBD |
