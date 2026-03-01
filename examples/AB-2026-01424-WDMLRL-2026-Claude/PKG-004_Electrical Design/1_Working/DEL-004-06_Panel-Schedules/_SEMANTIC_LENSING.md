# Semantic Lensing Register: DEL-004-06 Panel Schedules

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-004_Electrical Design/1_Working/DEL-004-06_Panel-Schedules/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-004-06_Panel-Schedules/_CONTEXT.md
- _STATUS.md — DEL-004-06_Panel-Schedules/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-004-06_Panel-Schedules/_SEMANTIC.md
- Datasheet.md — DEL-004-06_Panel-Schedules/Datasheet.md
- Specification.md — DEL-004-06_Panel-Schedules/Specification.md
- Guidance.md — DEL-004-06_Panel-Schedules/Guidance.md
- Procedure.md — DEL-004-06_Panel-Schedules/Procedure.md
- _REFERENCES.md — DEL-004-06_Panel-Schedules/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 3
  - Specification: 8
  - Guidance: 4
  - Procedure: 9
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Service voltage prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | CEC clause-level practice gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Alberta Safety Codes compliance verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure includes P.Eng. review and Alberta inspection |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Load balance procedure gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure covers execution steps adequately |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover assessment |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | Version control procedure gap |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P5 addresses spare capacity value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance covers merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately covered by existing trade-off structure |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA checks in Procedure verification table |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm service voltage (120/208V, 120/240V, or 347/600V) from utility provider. | Service voltage is TBD throughout all documents. This is a foundational prescriptive parameter that governs panel header data, breaker configurations, and conductor sizing. Without it, the prescriptive direction for the entire panel schedule is incomplete. | Datasheet.md; Guidance.md | Datasheet#Attributes -- Building and Service Characteristics; Guidance#Conflict Table CF-004-06-01 | -- | PROPOSAL: Electrical Engineer to confirm with utility provider | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-004-06-10 to cite specific CEC Part I edition and any Alberta amendments, or record TBD for clause-level references. | REQ-004-06-10 states compliance with CEC Part I but notes the assumption that "clause-level requirements not confirmed from accessible sources." Mandatory practice under this lens requires identifying the applicable code edition so practitioners know which rules to apply. | Specification.md | Specification#REQ-004-06-10 -- Alberta Safety Code Compliance | -- | PROPOSAL: Electrical Engineer to confirm applicable CEC edition | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for determining compliance with specific CEC Part I clauses (e.g., motor load sizing rules, panel clearance requirements). | The Verification table maps REQ-004-06-10 to "Design review by P.Eng.; Alberta Safety Codes inspection" but does not specify which CEC clauses will be verified or how compliance is determined beyond a general review. Under the compliance determination lens, the method is too high-level to confirm specific code compliance. | Specification.md | Specification#Verification | -- | PROPOSAL: Electrical Engineer to define clause-level verification checklist | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add procedural step or guidance for how three-phase load balancing is to be performed and documented during panel schedule development. | Guidance P2 states the engineer "shall distribute single-phase loads across the three phases to minimize imbalance" but no corresponding procedural step in Procedure.md describes how to perform or document the balancing. Under the procedural direction lens, this is a gap between the directional document and the operational document. | Procedure.md | Procedure#Steps -- Phase 2 | -- | PROPOSAL: Electrical Engineer to define balancing procedure | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add version control and reissue procedure for panel schedule revisions between preliminary and IFC. | Guidance C7 notes "Version control and reissue procedures should be established" but Procedure.md does not include any version control or revision tracking steps. Under the process audit lens, there is no auditable trail for how revisions between preliminary and IFC are managed. | Procedure.md; Guidance.md | Procedure#entire document scanned; Guidance#C7 -- Design-Build Context | -- | PROPOSAL: Proponent's project manager to define revision protocol | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Ceiling fan load data missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Load quantities for some items are TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Service pit loads absent from Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Load ratings stated consistently where known |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Utility fault current not recorded |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate in Guidance considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Guidance provides comprehensive account of design considerations |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding is present in Guidance principles |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements covered by P.Eng. requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment framework in Guidance is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided through Guidance considerations C1-C7 |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add ceiling fan load data (wattage, voltage) to Known Loads table; currently listed with quantity 6 but all electrical parameters are TBD. | Under the essential fact lens, ceiling fans (6 units) are listed in the Datasheet load table but have no wattage, voltage, or amperage data. The Specification (REQ-004-06-05) does not mention ceiling fans at all despite them being listed in the Datasheet. This is an essential data point needed for circuit sizing. | Datasheet.md | Datasheet#Attributes -- Known Loads to be Scheduled | -- | PROPOSAL: Electrical Engineer to determine ceiling fan specs | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Multi | Datasheet | Record TBD: Obtain exact quantities for overhead doors, exhaust fans, and receptacles per type from finalized architectural/electrical drawings. | Multiple load entries in the Datasheet show "TBD" or "Multiple (see App B drawing)" for quantities. Under the adequate evidence lens, the evidence base for circuit count calculations is incomplete. Quantities must be confirmed before the panel schedule can be finalized. | Datasheet.md | Datasheet#Attributes -- Known Loads to be Scheduled | -- | PROPOSAL: Electrical Engineer to finalize quantities from design drawings | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add service pit lighting and ventilation loads to the Known Loads table. | Guidance C5 identifies service pit lighting and ventilation as loads that "should be included in the panel schedule." However, the Datasheet Known Loads table does not list service pit lighting or ventilation as separate entries. Under the comprehensive record lens, this is an omission from the descriptive record of known loads. | Datasheet.md; Guidance.md | Datasheet#Attributes -- Known Loads to be Scheduled; Guidance#C5 -- Service Trench / Service Pit Lighting and Ventilation | -- | PROPOSAL: Electrical Engineer to confirm service pit loads | TBD |
| B-004 | B:information:necessity | TBD_Question | Procedure | Datasheet | Record TBD: Obtain utility service fault current and service entrance location from utility provider. Add to Datasheet Conditions or Attributes. | Procedure Step 1.2 identifies utility fault current and service entrance location as design inputs with status TBD. Under the essential signal lens, these are necessary information signals that feed into panel ratings and protective device coordination but are not yet recorded in the Datasheet. | Procedure.md; Datasheet.md | Procedure#Prerequisites -- Design Inputs Required; Datasheet#Conditions | -- | PROPOSAL: Electrical Engineer to obtain from utility provider | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Governing Criterion | 1 | HAS_ITEMS | Phase imbalance limit not specified |
| C:normative:sufficiency | normative | sufficiency | Stipulated Competence Threshold | 0 | NO_ITEMS | P.Eng. requirement establishes competence threshold |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Ceiling fans absent from Specification requirements |
| C:normative:consistency | normative | consistency | Codified Conformance Standard | 0 | NO_ITEMS | Conformance standard references consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Imperative | 0 | NO_ITEMS | Critical operational steps are covered in Procedure |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Working Capacity | 0 | NO_ITEMS | Procedure demonstrates adequate working capacity |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 1 | HAS_ITEMS | Cross-discipline coordination lacks specificity |
| C:operative:consistency | operative | consistency | Dependable Process Uniformity | 0 | NO_ITEMS | Process steps are uniform and sequenced |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Judgment | 0 | NO_ITEMS | Covered by Guidance purpose and principles |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Appraisal | 0 | NO_ITEMS | Trade-offs provide substantiated appraisal |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting is adequate for current stage |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value principles are consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify whether a specific phase imbalance limit applies (e.g., percentage threshold per CEC Part I or utility requirements) or record TBD. | Guidance P2 states "distribute single-phase loads across the three phases to minimize imbalance" and the Procedure verification table checks "Phase imbalance within acceptable limit (per CEC Part I or Electrical Engineer's criteria)" but no specific enforceable criterion (numeric threshold) is stated in the Specification. Under the Enforceable Governing Criterion lens, the lack of a specific limit makes the requirement unenforceable as written. | Specification.md; Guidance.md; Procedure.md | Specification#REQ-004-06-01; Guidance#P2 -- Three-Phase Load Balance; Procedure#Verification | -- | PROPOSAL: Electrical Engineer to define acceptable limit | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement for ceiling fan circuits (6 units per Datasheet) to the Requirements section. | The Datasheet lists 6 ceiling fans in the Known Loads table. REQ-004-06-05 (Lighting Circuits) covers high bay and LED strip lights but does not mention ceiling fans. REQ-004-06-08 covers exhaust fans. Under the Exhaustive Regulatory Scope lens, ceiling fans fall through a gap in the requirements enumeration. | Specification.md; Datasheet.md | Specification#REQ-004-06-05 -- Lighting Circuits; Datasheet#Attributes -- Known Loads to be Scheduled | -- | PROPOSAL: Electrical Engineer to classify and add ceiling fan requirement | TBD |
| C-003 | C:operative:completeness | WeakStatement | Procedure | Procedure | Strengthen Step 2.5 cross-discipline coordination by specifying what information is exchanged and what confirmation record is produced for each discipline. | Procedure Step 2.5 lists disciplines to coordinate with but uses general language ("Verify with other discipline leads"). Under the Thorough Operational Coverage lens, the step lacks specificity about what exact data is to be confirmed, what form the confirmation takes, and how disagreements are resolved. | Procedure.md | Procedure#Steps -- Step 2.5 Cross-Discipline Coordination Check | -- | PROPOSAL: Project manager to define coordination protocol | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Conformity Obligation | 1 | HAS_ITEMS | Spare capacity requirement is assumption-only |
| F:normative:sufficiency | normative | sufficiency | Mandated Qualification Standard | 0 | NO_ITEMS | P.Eng. qualification clearly mandated |
| F:normative:completeness | normative | completeness | Comprehensive Regulatory Mastery | 0 | NO_ITEMS | Regulatory framework identified though not clause-level |
| F:normative:consistency | normative | consistency | Integrated Regulatory Harmony | 0 | NO_ITEMS | Standards references harmonized across documents |
| F:operative:necessity | operative | necessity | Critical Capability Assurance | 1 | HAS_ITEMS | Equipment spec procurement timing gap |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Proficiency | 0 | NO_ITEMS | Procedure steps provide sufficient execution guidance |
| F:operative:completeness | operative | completeness | Total Execution Mastery | 0 | NO_ITEMS | Execution coverage is adequate |
| F:operative:consistency | operative | consistency | Stable Execution Alignment | 0 | NO_ITEMS | Process steps align with requirements |
| F:evaluative:necessity | evaluative | necessity | Anchored Value Imperative | 1 | HAS_ITEMS | No cost/schedule impact assessment for spare capacity decision |
| F:evaluative:sufficiency | evaluative | sufficiency | Sound Merit Substantiation | 0 | NO_ITEMS | Merit substantiation in Guidance trade-offs is sound |
| F:evaluative:completeness | evaluative | completeness | Holistic Merit Authority | 0 | NO_ITEMS | Holistic view provided |
| F:evaluative:consistency | evaluative | consistency | Unified Merit Coherence | 0 | NO_ITEMS | Merit reasoning is coherent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-004-06-12 (Spare Capacity) to either state a minimum spare capacity percentage or explicitly record it as TBD pending Electrical Engineer's determination. | REQ-004-06-12 is entirely assumption-based ("ASSUMPTION: commonly 20-25% spare capacity") with no binding requirement stated. Under the Absolute Conformity Obligation lens, this requirement cannot be enforced because no specific obligation is defined. The RFP does not state a spare requirement, so this should be either a design decision (documented as such) or a TBD requiring human ruling. | Specification.md | Specification#REQ-004-06-12 -- Spare Capacity | -- | PROPOSAL: Electrical Engineer or County to define spare capacity target | TBD |
| F-002 | F:operative:necessity | RationaleGap | Guidance | Guidance | Add rationale and recommended timeline for obtaining critical equipment specifications (crane, welding, exhaust fan) to support panel schedule development. | Procedure Prerequisites lists multiple TBD equipment specifications (crane, welding, exhaust fans, overhead doors) but neither Guidance nor Procedure explains the priority order, acceptable risk of proceeding without them, or fallback approach if specs arrive late. Under the Critical Capability Assurance lens, the absence of a procurement timing rationale risks late-stage panel revisions. | Guidance.md; Procedure.md | Guidance#C2 -- Crane Power Requirements; Procedure#Prerequisites -- Design Inputs Required | -- | PROPOSAL: Electrical Engineer to define equipment spec procurement timeline | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale for the spare capacity trade-off that addresses lifecycle cost impact, future equipment likelihood, and County expectations. | Guidance Trade-offs table lists spare capacity options (10% vs. 25%+) but the consideration column provides only a general statement. Under the Anchored Value Imperative lens, there is insufficient rationale to anchor the value decision for the County. The industrial maintenance use case suggests high probability of future equipment additions but no analysis supports this. | Guidance.md | Guidance#Trade-offs | -- | PROPOSAL: Electrical Engineer to quantify spare capacity rationale | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Directive Authority | 0 | NO_ITEMS | Directive authority established through RFP and code references |
| D:normative:applying | normative | applying | Definitive Compliance Execution | 1 | HAS_ITEMS | Old North Shop scope ambiguity |
| D:normative:judging | normative | judging | Conclusive Conformity Verdict | 0 | NO_ITEMS | Verification table supports conformity verdicts |
| D:normative:reviewing | normative | reviewing | Definitive Compliance Inspection | 0 | NO_ITEMS | P.Eng. review and Alberta inspection covered |
| D:operative:guiding | operative | guiding | Assured Operational Pathway | 1 | HAS_ITEMS | Preliminary-to-IFC transition pathway unclear |
| D:operative:applying | operative | applying | Confirmed Task Fulfillment | 0 | NO_ITEMS | Task fulfillment criteria established |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 0 | NO_ITEMS | Performance assessment covered in Procedure verification |
| D:operative:reviewing | operative | reviewing | Systematic Process Inspection | 0 | NO_ITEMS | Process inspection steps in Procedure are systematic |
| D:evaluative:guiding | evaluative | guiding | Definitive Merit Bearing | 0 | NO_ITEMS | Merit bearing established through OBJ-003 and OBJ-005 linkage |
| D:evaluative:applying | evaluative | applying | Confirmed Value Enactment | 1 | HAS_ITEMS | No acceptance criteria for County preliminary approval |
| D:evaluative:judging | evaluative | judging | Conclusive Value Authority | 0 | NO_ITEMS | Value authority rests with Electrical Engineer and County |
| D:evaluative:reviewing | evaluative | reviewing | Definitive Merit Review | 0 | NO_ITEMS | Review process defined in Procedure |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Normalization | Specification | Multi | Clarify scope boundary regarding Old North Shop: confirm whether panel schedules cover new addition only or also include any renovation scope. Align terminology across documents. | Specification exclusions state "Panel schedules for the Old North Shop renovation scope, unless explicitly directed" with an ASSUMPTION tag. The Datasheet and Procedure do not address this boundary at all. Under the Definitive Compliance Execution lens, scope ambiguity about what is included vs. excluded risks either over-delivery or under-delivery. | Specification.md | Specification#Scope -- What This Deliverable Excludes | -- | PROPOSAL: County to confirm scope boundary | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add a step or decision gate describing how the Electrical Engineer transitions from preliminary panel schedule to final IFC, including what triggers the transition and what must be complete. | Procedure Phase 1 ends at Step 1.7 (Incorporate County Feedback) and Phase 2 begins at Step 2.1 (Obtain Outstanding Equipment Specifications) but there is no explicit transition gate or readiness criteria between them. Under the Assured Operational Pathway lens, the pathway from preliminary to IFC lacks a defined decision point. | Procedure.md | Procedure#Steps -- between Phase 1 and Phase 2 | -- | PROPOSAL: Electrical Engineer and project manager to define gate criteria | TBD |
| D-003 | D:evaluative:applying | VerificationGap | Specification | Specification | Add acceptance criteria for County preliminary approval (REQ-004-06-13) specifying what the County is expected to evaluate and what constitutes approval. | REQ-004-06-13 requires County approval of preliminary design but neither the Specification nor the Procedure defines what the County is evaluating, what format the submission takes, or what constitutes approval (written sign-off, email, meeting minutes). Under the Confirmed Value Enactment lens, value cannot be confirmed if acceptance criteria for the approval gate are undefined. | Specification.md; Procedure.md | Specification#REQ-004-06-13 -- Preliminary Design County Approval; Procedure#Step 1.6 | -- | PROPOSAL: County project team to define approval criteria | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Authority Signal | 0 | NO_ITEMS | Authority signals established through RFP and code references |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Authority Basis | 1 | HAS_ITEMS | Standards not accessible |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Record | 0 | NO_ITEMS | Directive record is adequate for current stage |
| X:guiding:consistency | guiding | consistency | Coherent Directive Measure | 0 | NO_ITEMS | Directives are coherent across documents |
| X:applying:necessity | applying | necessity | Mandatory Fulfillment Fact | 1 | HAS_ITEMS | Verification cross-references incomplete for service pit loads |
| X:applying:sufficiency | applying | sufficiency | Sufficient Fulfillment Evidence | 0 | NO_ITEMS | Evidence base is sufficient for current stage |
| X:applying:completeness | applying | completeness | Exhaustive Fulfillment Record | 0 | NO_ITEMS | Fulfillment records defined in Procedure |
| X:applying:consistency | applying | consistency | Consistent Fulfillment Measure | 1 | HAS_ITEMS | Naming inconsistency |
| X:judging:necessity | judging | necessity | Critical Determination Finding | 0 | NO_ITEMS | Critical determination points defined |
| X:judging:sufficiency | judging | sufficiency | Sufficient Determination Basis | 1 | HAS_ITEMS | Load balance verification criterion missing |
| X:judging:completeness | judging | completeness | Exhaustive Determination Record | 0 | NO_ITEMS | Determination records defined in Procedure |
| X:judging:consistency | judging | consistency | Dependable Determination Alignment | 0 | NO_ITEMS | Determination methods aligned |
| X:reviewing:necessity | reviewing | necessity | Critical Examination Finding | 0 | NO_ITEMS | Critical examination points defined |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Examination Basis | 1 | HAS_ITEMS | Internal cross-check record lacks defined format |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Examination Record | 0 | NO_ITEMS | Examination records defined |
| X:reviewing:consistency | reviewing | consistency | Dependable Examination Alignment | 0 | NO_ITEMS | Examination methods aligned |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | TBD_Question | Multi | Guidance | Record TBD: Obtain or confirm access to CEC Part I (CSA C22.1) current edition and Alberta Safety Codes Act for use during design. | The Specification Standards table marks both CEC Part I and Alberta Safety Codes as "ASSUMPTION: applicable; not accessible in sources." Procedure References marks CEC Part I as "location TBD." Under the Sufficient Authority Basis lens, the authority basis for code compliance is stated but not substantiated with accessible standards text. | Specification.md; Procedure.md | Specification#Standards; Procedure#References Required | -- | PROPOSAL: Electrical Engineer to obtain applicable standards | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification cross-reference for service pit lighting and ventilation circuits (identified in Guidance C5 but absent from Specification requirements and verification table). | Guidance C5 identifies service pit lighting and ventilation as panel schedule loads with an assumption that they are in scope. However, there is no corresponding requirement in the Specification and therefore no verification entry. Under the Mandatory Fulfillment Fact lens, a recognized load has no verification pathway. | Specification.md; Guidance.md | Specification#Verification; Guidance#C5 -- Service Trench / Service Pit Lighting and Ventilation | -- | PROPOSAL: Electrical Engineer to add service pit requirement or confirm exclusion | TBD |
| X-003 | X:applying:consistency | Normalization | Multi | Multi | Normalize building name terminology: documents use "New North Shop," "New North Shop addition," and "maintenance shop addition" interchangeably. Establish a single canonical name. | The Specification uses "New North Shop addition," the Guidance uses "New North Shop addition," the Procedure uses "New North Shop," and the Datasheet uses "Industrial maintenance shop addition." Under the Consistent Fulfillment Measure lens, inconsistent naming risks confusion in circuit descriptions and panel labels that will carry through to construction documents. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet#Attributes -- Building Type; Specification#Scope; Guidance#Purpose; Procedure#Purpose | -- | PROPOSAL: Establish canonical building name in Guidance and use consistently | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Procedure | Specification | Add a specific pass/fail criterion for load balance verification (e.g., maximum percentage imbalance between phases). | Procedure verification table states "Phase imbalance within acceptable limit (per CEC Part I or Electrical Engineer's criteria)" but no specific numeric criterion is provided anywhere. Under the Sufficient Determination Basis lens, a verification check without a defined threshold cannot produce a deterministic pass/fail result. | Procedure.md | Procedure#Verification -- Load balance acceptable | -- | PROPOSAL: Electrical Engineer to define phase imbalance threshold | TBD |
| X-005 | X:reviewing:sufficiency | WeakStatement | Procedure | Procedure | Define the expected format and content of the "Internal Cross-Check Record" listed in the Records table. | Procedure Records table lists "Internal Cross-Check Record" described as "Notes from Steps 1.5 and 2.4" retained by "Electrical Engineer." Under the Sufficient Examination Basis lens, the record format is undefined -- it could be a formal checklist, informal notes, or nothing at all. Without a defined format, the sufficiency of the examination basis cannot be assessed. | Procedure.md | Procedure#Records | -- | PROPOSAL: Electrical Engineer to define cross-check record template | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Steering Record | 1 | HAS_ITEMS | Conflict on service voltage |
| E:guiding:information | guiding | information | Coherent Steering Narrative | 0 | NO_ITEMS | Steering narrative is coherent in Guidance |
| E:guiding:knowledge | guiding | knowledge | Integrated Steering Mastery | 0 | NO_ITEMS | Knowledge integration is adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Steering Foresight | 1 | HAS_ITEMS | No foresight for future building expansion |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Records section lacks distribution list confirmation |
| E:applying:information | applying | information | Contextualized Execution Account | 0 | NO_ITEMS | Execution context is adequate |
| E:applying:knowledge | applying | knowledge | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution mastery is sufficient |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment criteria established |
| E:judging:data | judging | data | Substantiated Adjudication Record | 0 | NO_ITEMS | Adjudication records defined |
| E:judging:information | judging | information | Coherent Assessment Account | 0 | NO_ITEMS | Assessment accounts are coherent |
| E:judging:knowledge | judging | knowledge | Integrated Assessment Mastery | 0 | NO_ITEMS | Assessment mastery is adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Foresight | 0 | NO_ITEMS | Adjudication framework is principled |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 1 | HAS_ITEMS | Equipment specification log undefined |
| E:reviewing:information | reviewing | information | Comprehensive Audit Account | 0 | NO_ITEMS | Audit account is comprehensive |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Audit Mastery | 0 | NO_ITEMS | Audit mastery is adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight is adequate |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Conflict | Guidance | Guidance | Surface service voltage conflict for human ruling: RFP requires three-phase but does not specify voltage level; App B legend implies 120V/240V loads but main service voltage is undetermined. Guidance CF-004-06-01 already captures this but Datasheet and Specification do not cross-reference the conflict. | Guidance Conflict Table CF-004-06-01 identifies the service voltage conflict. However, the Datasheet lists "Service Voltage: TBD" without referencing the conflict, and Specification REQ-004-06-01 does not acknowledge the open question. Under the Substantiated Steering Record lens, the steering data is incomplete because the conflict is documented in one document but not cross-referenced in the others that depend on its resolution. | Guidance.md; Datasheet.md; Specification.md | Guidance#Conflict Table CF-004-06-01; Datasheet#Attributes -- Service Voltage; Specification#REQ-004-06-01 | Guidance.md#Conflict Table CF-004-06-01; Datasheet.md#Attributes -- Service Voltage | PROPOSAL: Electrical Engineer to resolve after utility confirmation | TBD |
| E-002 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add consideration for future building expansion or phased load growth and its impact on panel sizing and spare capacity. | Guidance addresses spare capacity (P5, Trade-offs) and current design considerations (C1-C7) but does not discuss the possibility of future building phases or expansion of the maintenance shop that could affect main panel sizing. Under the Principled Steering Foresight lens, the absence of forward-looking analysis for a facility with a long service life is a gap in principled foresight. | Guidance.md | Guidance#Principles -- P5; Guidance#Trade-offs | -- | PROPOSAL: Electrical Engineer and County to discuss future expansion plans | TBD |
| E-003 | E:applying:data | VerificationGap | Procedure | Procedure | Add a step confirming that IFC panel schedule distribution (Step 2.7) is documented with a transmittal or distribution record that verifies receipt by all listed parties. | Procedure Step 2.7 lists distribution recipients but the Records table does not include a transmittal record or distribution confirmation. Under the Verified Execution Record lens, the execution of document distribution is not recorded in a way that can be verified after the fact. | Procedure.md | Procedure#Steps -- Step 2.7 Issue for Construction; Procedure#Records | -- | PROPOSAL: Proponent's project manager to define distribution record | TBD |
| E-004 | E:reviewing:data | Normalization | Procedure | Procedure | Define the expected format and content of the "Equipment Specification Log" listed in the Records table. | Procedure Records table lists "Equipment Specification Log" described as "Log of equipment specs received and incorporated" retained by "Electrical Engineer." Under the Substantiated Audit Record lens, no template, format, or minimum required fields are specified, making the audit record unstandardized. | Procedure.md | Procedure#Records | -- | PROPOSAL: Electrical Engineer to define equipment spec log template | TBD |
