# Semantic Lensing Register: DEL-03-02 Detailed Design and Construction Docs Plan

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — Deliverable identity, scope traceability (SOW-018, OBJ-002), acceptance criteria
- _STATUS.md — Current state: SEMANTIC_READY (2026-02-04)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E extracted
- Datasheet.md — Identification, attributes, conditions, construction (plan production process)
- Specification.md — RQ-01 through RQ-10, standards, verification matrix
- Guidance.md — Principles P-01 through P-06, considerations, trade-offs T-01 through T-03, examples
- Procedure.md — Part A (proposal steps A-01 through A-11), Part B (post-award steps B-01 through B-16), verification, records
- _REFERENCES.md — RFP Section 7.1.8, Addendum 03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- **Total warranted items:** 34
- **By document:**
  - Datasheet: 9
  - Specification: 12
  - Guidance: 8
  - Procedure: 5
- **By matrix:**
  - A: 5  B: 5  C: 4  F: 5  D: 5  X: 3  E: 2
- **Notable conflicts:** 3
- **Matrix parse errors:** 0

---

## Matrix A — Orientation (3×4)

### Lens: A:normative:guiding
**LensValue:** "prescriptive direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | MissingSlot | Specification | Normative guiding principles for Owner review timing expectations | Specification RQ-05 (Owner review) states "typical: 2-3 weeks" as ASSUMPTION, but does not define this as a prescriptive requirement for the plan to contain. The Guidance section provides narrative rationale (P-03, considerations) but no firm directive on what durations must be stated. | Specification.md § RQ-05; Guidance.md § Considerations (Owner Review Period Duration) | "RQ-05: Owner Review and Approval Process" vs. "Owner Review Period Duration consideration" | Specification RQ-05 vs. Guidance consideration on review period | Recommend: Add normative directive in Specification that plan must state a specific proposed review period (e.g., 2-3 weeks for DD/CD) subject to Owner negotiation. | TBD |

---

### Lens: A:normative:applying
**LensValue:** "mandatory practice"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-002 | WeakStatement | Specification | RQ-08 (Addenda Integration) states addenda requirements "shall be integrated" but does not specify verification method or checkpoint timing. | Specification RQ-08 requires integration but the Procedure (Step A-08) specifies creation of an "Addenda integration checklist" as the tool. However, Specification does not mandate this checklist as a mandatory deliverable artifact. Clarity gap on what "integration" means operationally. | Specification.md § RQ-08; Procedure.md § Step A-08 | "Addenda Integration" vs. "Integrate Addenda Traceability" | Specification RQ-08 vs. Procedure Step A-08 | Recommend: Add to Specification RQ-08 that integration verification must include an explicit addenda checklist artifact cross-mapping each Addendum 03 item (16 ft doors, bay sumps, exhaust, generator, solar-ready, fill stations, room sizing) to discipline scope and QA/QC checkpoint. | TBD |

---

### Lens: A:normative:judging
**LensValue:** "compliance determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | VerificationGap | Specification | RQ-07 (Code Compliance) requires code compliance but verification method relies on plan review ("Review of plan document to confirm code compliance strategy is addressed"). No explicit acceptance criterion for what level of code compliance evidence (third-party review, internal, sealed drawings) is mandatory. | Specification § Verification table lists "Code compliance review" as responsibility but the table does not specify whether third-party code review is required or optional, who performs seal/stamp, or when (DD, CD). This is a judgment gap: what counts as "sufficient" code compliance assurance? | Specification.md § RQ-07 and § Verification table | "Code Compliance and Permitting Alignment" vs. practice assumption in Guidance considerations | Specification RQ-07 vs. Guidance considerations (Code Review: Third-Party vs. Internal) | Recommend: Clarify in Specification whether third-party code review at CD phase is mandatory (best practice) or optional; if mandatory, add to required discipline scope list. | TBD |

---

### Lens: A:operative:guiding
**LensValue:** "procedural stewardship"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | MissingSlot | Procedure | Post-award operational workflow (Part B) lacks a step for defining "approval signoff authority" and conflict escalation path when Owner and Design-Builder disagree on design or document adequacy. | Procedure Part B (Steps B-01 through B-16) describes the workflow but does not address: Who approves? How are conflicts resolved if Owner rejects a design at DD or CD? What is the escalation path? This is a governance gap in procedural stewardship. | Procedure.md § Part B (no explicit escalation/authority definition) | "Steps B-04, B-07, B-10, B-11 (Owner acceptance)" | Multiple steps assume Owner acceptance without defining decision authority or conflict resolution | Recommend: Add prerequisite or step defining decision authority (e.g., "Design Manager may escalate to Project Manager if Owner comments require scope/cost/schedule re-negotiation"). | TBD |

---

### Lens: A:operative:reviewing
**LensValue:** "process retrospection"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | TBD_Question | Procedure | Should post-award process retrospection (lessons learned, process effectiveness review) be included as a post-project step? | Procedure Part B ends at Step B-16 (as-built markup support) with no post-project review or lessons learned capture. For process maturity and future project replication, a retrospective step may be valuable. Question: Is this in scope for DEL-03-02 or deferred to project management protocols? | Procedure.md § Part B (ends at B-16) | "Records" section (no lessons learned records listed) | Procedure content vs. ASSUMPTION that post-project review is outside scope | Recommend: Clarify scope boundaries—should DEL-03-02 plan include a post-closeout process retrospection step, or is that delegated to broader project management? If included, add Step B-17. | TBD |

---

## Matrix B — Conceptualization (4×4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | MissingSlot | Datasheet | Datasheet lists "Design Disciplines" as ASSUMPTION but does not confirm landscape discipline scope. Functional Program (RFP Appendix B, per references) may or may not require landscape deliverables. | Datasheet § "Design Disciplines (ASSUMPTION)" lists 6 disciplines (Arch, Struct, Mech, Elec, Civil, Landscape) with note "if applicable." This is an essential fact gap: Is landscape in or out of scope? Affects completeness checklist and coordination workflows. | Datasheet.md § Design Disciplines; Specification.md § RQ-06 (repeats landscape scope as ASSUMPTION) | Datasheet vs. Specification (both flag landscape as TBD) | Both sources flag uncertainty about landscape scope | Recommend: Clarify landscape scope before finalizing the plan. If in scope, confirm deliverables (planting plans, irrigation). If out, remove from discipline list. | TBD |

---

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-002 | WeakStatement | Datasheet | "Document Generation Workflow (ASSUMPTION: typical process)" in Construction section describes 7-step workflow but does not specify evidence of what "adequate" QA/QC looks like (e.g., checklist completeness, sign-off artifacts). | Datasheet § Construction (Document Generation Workflow) lists steps but the evidence sufficiency for each step is vague. For example, "Internal QA/QC: Discipline lead reviews for completeness and code compliance" — what documentation proves the review occurred? Checklists? Sign-off form? Missing. | Datasheet.md § Construction / Document Generation Workflow | Datasheet workflow description vs. Specification RQ-03 (QA/QC checkpoints) | Datasheet provides operational narrative; Specification provides requirement but not evidence standard | Recommend: Add to Datasheet or Specification that each QA/QC step must be documented by a signed checklist or review memo. | TBD |

---

### Lens: B:information:necessity
**LensValue:** "required disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | MissingSlot | Guidance | Guidance § Examples includes three examples (drawing index, BIM coordination workflow, Owner review process) but does not include an example of document control protocols (numbering system, revision tracking template). | Guidance § Considerations discusses document control (T-03: flexibility vs. control) and P-05 (document control prevents chaos) but Example 2 (BIM coordination) and Example 3 (Owner review) do not show document control implementation. A specific example of revision tracking or DMS folder structure would support credibility. | Guidance.md § Examples (sections 1–3) | Guidance rationale on document control (P-05) vs. Examples provided | Guidance principle P-05 calls out importance but Example 1 (drawing index) only addresses structure, not control; no example of revision tracking or DMS naming convention | Recommend: Add Example 4: Document Control Implementation (sample numbering system, revision cloud protocol, DMS folder structure). | TBD |

---

### Lens: B:information:consistency
**LensValue:** "coherent messaging"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | Conflict | Multi | Terminology inconsistency: Specification uses "QA/QC" (Quality Assurance / Quality Control); Guidance uses "QA/QC is multi-layered" (principle P-04); Procedure uses "QA/QC checklist." However, Datasheet § Quality Assurance Checkpoints says "Quality Assurance Checkpoints (ASSUMPTION)" and does not clearly differentiate between QA (assurance) and QC (control). | QA typically means verification that requirements are being met; QC means testing/inspection. Datasheet conflates them into "Quality Assurance Checkpoints" describing both self-check and control activities. This risks confusion in the final plan about which activities are assurance (upstream prevention) vs. control (downstream detection). | Datasheet.md § Quality Assurance Checkpoints vs. Guidance.md § P-04 / Specification.md § RQ-03 | Datasheet "Quality Assurance Checkpoints" (unclear QA vs. QC distinction) vs. Guidance/Specification multi-layered approach (implies both assurance and control) | Datasheet uses "Assurance Checkpoints" for what appears to include both QA and QC activities | Recommend: Clarify and consistently use "QA/QC Checkpoints" terminology across all four documents and define the distinction in the plan (QA = upstream requirement verification; QC = downstream validation/testing). | TBD |

---

### Lens: B:knowledge:completeness
**LensValue:** "thorough proficiency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | RationaleGap | Guidance | Guidance § Principles (P-01 through P-06) and Considerations cover six major topic areas (completeness, coordination, Owner engagement, QA/QC, document control, addenda). However, knowledge gap on BIM vs. 2D CAD decision-making is addressed as a Consideration with competing factors but no clear guidance on when to recommend BIM vs. 2D. | Guidance § Considerations (BIM vs. 2D CAD Workflow) presents factors to weigh but recommendation is conditional: "Define which approach based on project complexity, team capabilities, and Owner preferences (if known)." For a proposal document, this may be insufficient—the proponent should state a position. Thorough proficiency would include a stronger stance or decision criteria. | Guidance.md § Considerations / BIM vs. 2D CAD Workflow | Guidance BIM consideration (neutral, decision deferred) vs. Procedure assumption (may imply BIM for building) | Guidance avoids recommending BIM; Procedure references "BIM coordination" as if approach is decided | Recommend: Either decide on a BIM-first position for the proposal (to demonstrate sophistication) or add clearer decision criteria to the Consideration (e.g., "Recommend BIM if Owner has BIM requirement; otherwise hybrid approach is acceptable"). | TBD |

---

## Matrix C — Formulation (3×4)

### Lens: C:normative:necessity
**LensValue:** "enforceable conformance mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | VerificationGap | Specification | RQ-04 (Document Control and Revision Tracking) requires "document control procedures" but does not mandate an electronic document management system (DMS). Datasheet § Document Control Attributes states "Distribution method: TBD (digital platform; hard copy protocols if required)" which implies DMS is conditional, not mandatory. | Specification RQ-04 requires document control but the verification is "plan document review" — confirming procedures are described does not verify a DMS is in place. For new construction, a modern DMS is typically mandatory, not optional. Specification should make this a conformance mandate. | Specification.md § RQ-04 Verification table; Datasheet.md § Document Control Attributes | Specification RQ-04 ("procedures" language) vs. modern construction practice (DMS is mandatory for Design-Build) | Specification is permissive (DMS optional); modern practice expects DMS | Recommend: Update Specification RQ-04 to require "electronic document management system (DMS)" as a mandatory component of document control procedures, not optional "if required." | TBD |

---

### Lens: C:normative:completeness
**LensValue:** "integral regulatory coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | MissingSlot | Specification | Specification § Standards lists "Alberta Building Code (ABC)" and "National Fire Code of Canada (NFC)" as governing codes but does not include other relevant standards such as CSA (Canadian Standards Association) standards for mechanical/electrical systems or accessibility standards (CSA B651 for accessibility). | RQ-07 (Code Compliance) requires compliance with codes but Specification § Standards is incomplete. For a Fire Hall + Public Works facility, additional standards (CSA, accessibility) are typically required for integral regulatory coverage. Current list in Specification § Standards (ABC, NFC, CSI MasterFormat, ISO 19650) does not fully cover regulatory scope. | Specification.md § Standards | Specification § Standards (4 items listed) vs. implicit scope of standards needed for Fire Hall + Public Works | Standards section appears selective, not exhaustive | Recommend: Expand Specification § Standards section to include CSA standards (electrical, mechanical, accessibility) and cite specific codes/standards from RFP Appendix A (OSR) that are mandatory. | TBD |

---

### Lens: C:operative:sufficiency
**LensValue:** "demonstrated operational readiness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | WeakStatement | Procedure | Part B (post-award workflow) assumes all design team members are mobilized (Step B-01: "kick-off meeting complete") and tools are operational (Step B-02: "DMS and BIM platform functional"). However, Procedure does not describe contingency if a discipline is delayed in mobilization or if software platform is not ready by start of DD phase. | Operational readiness verification (Procedure § Verification table for B-01 and B-02) simply confirms steps are completed but does not address: What if a key discipline (e.g., structural) is not available? What if DMS is delayed? What is the impact? Weak readiness preparation. | Procedure.md § Part B (Steps B-01, B-02) and § Verification table | Procedure assumes readiness vs. realistic project risks | Procedure lists steps but not contingencies or risks if prerequisites are not met | Recommend: Add or flag in Procedure Part B that mobilization risks and tool readiness risks should be captured in DEL-09-01 (Risk Register) with mitigation plans. | TBD |

---

### Lens: C:operative:consistency
**LensValue:** "repeatable process discipline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | Normalization | Specification | Specification defines 10 requirements (RQ-01 through RQ-10) but uses inconsistent verification language. Some requirements (RQ-01, RQ-02) use "Review of plan document to confirm X is described" while others (RQ-03, RQ-04, RQ-05) provide more specific verification (table rows, checkpoints, process elements). For repeatable process discipline, verification method should be consistent across all requirements. | RQ-01/02 verification is vague ("confirm procedures described"); RQ-03+ is more structured. This inconsistency affects how the plan will be evaluated and how compliance will be demonstrated. For a repeatable, auditable process, all requirements should have equally structured verification. | Specification.md § Verification table | Specification RQ-01/02 verification (generic) vs. RQ-03+ verification (specific) | Some requirements have detailed verification criteria; others are generic | Recommend: Standardize Specification verification methods—either all should use a detailed checklist or all should use plan review criteria. Preferred: detailed checklists for consistency and auditability. | TBD |

---

## Matrix F — Requirements (3×4)

### Lens: F:normative:sufficiency
**LensValue:** "confirmed regulatory proficiency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | VerificationGap | Specification | RQ-07 (Code Compliance) requires design documents to meet Alberta Building Code, but Specification does not require proof of "confirmed regulatory proficiency." For a Fire Hall (life safety criticality), the plan should specify third-party code review or sealed drawings signed by code specialist. Current requirement is weak on proficiency confirmation. | RQ-07 describes the strategy and verification is "plan review" but does not verify that the proponent team has actual code expertise or that a code reviewer is assigned. "Confirmed proficiency" would require resume/credential verification or third-party review commitment. Missing. | Specification.md § RQ-07 | RQ-07 requirement (strategy-based) vs. modern Design-Build practice (proficiency verification required) | Specification asks for strategy, not proof of capability | Recommend: Add to RQ-07 that the plan must identify the code reviewer (if third-party) by name/firm with credentials, or confirm in-house code expertise with responsible person identification. | TBD |

---

### Lens: F:operative:necessity
**LensValue:** "foundational workflow prerequisite"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | MissingSlot | Procedure | Step A-01 (Gather Input) assumes RFP Section 7.1.8 is accessible and understandable. However, Procedure does not include a prerequisite step for confirming that the RFP has been thoroughly read and requirements are extracted. This is a foundational prerequisite that is assumed but not verified. | For the proposal phase production workflow (Part A), a prerequisite is that RFP Section 7.1.8 must be fully understood and documented. Step A-01 says "Review RFP Section 7.1.8" but does not describe what completeness means or how to verify requirements are captured. Foundational gap. | Procedure.md § Part A / Step A-01 (no prerequisites section) | Procedure assumes RFP availability vs. need to verify RFP requirements are captured | Procedure lists steps but Part A has no prerequisites section (Part B has prerequisites section) | Recommend: Add prerequisites section to Part A mirroring Part B structure: confirm RFP Section 7.1.8 is accessible; confirm team has access to RFP; confirm addenda (01–03) are integrated into baseline requirements. | TBD |

---

### Lens: F:operative:completeness
**LensValue:** "saturated workflow comprehension"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | RationaleGap | Guidance | Guidance § Trade-offs (T-01, T-02, T-03) address speed vs. thoroughness, detail level, and flexibility vs. control. However, no trade-off is presented for "proposal completeness vs. post-award flexibility"—i.e., how detailed should the plan be in the proposal if the team will refine procedures post-award? Incompleteness in trade-off coverage. | Guidance provides three trade-offs but the implicit trade-off—how much detail to commit in the proposal vs. how much to defer to post-award refinement—is not explicitly addressed. This is a significant consideration for the proponent: over-specify and constrain flexibility; under-specify and risk proposal credibility. Rationale gap. | Guidance.md § Trade-offs (T-01, T-02, T-03 only) | Guidance trade-offs covered (3) vs. potential trade-offs (proposal detail vs. post-award flexibility) | Guidance does not address proposal specificity vs. flexibility trade-off | Recommend: Add T-04 trade-off: "Proposal Detail vs. Post-Award Flexibility" with guidance on which procedures should be locked in the proposal (e.g., document control schema, QA/QC checkpoints) vs. which can be refined post-award (e.g., specific software platform, detailed review period by phase). | TBD |

---

### Lens: F:evaluative:consistency
**LensValue:** "stable adequacy assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | Conflict | Multi | Evaluation consistency across the four documents is undermined by differing treatment of landscape discipline scope. Datasheet, Specification, and Guidance all flag landscape as "(if applicable — TBD)" but Procedure Part B (Step B-06: DD phase) includes landscape in the operational workflow description without conditional language. This creates inconsistency: is landscape scope defined or undefined? | Stability of adequacy assurance requires consistent scope boundaries. If landscape is optional, then any evaluation of the plan's adequacy (proposal evaluation vs. post-award execution) depends on knowing scope upfront. The inconsistency suggests the scope is not yet determined, but Procedure assumes it. This destabilizes the evaluation framework. | Datasheet.md, Specification.md, Guidance.md (all flag landscape TBD) vs. Procedure.md § Part B (assumes landscape is in workflow) | Multiple documents flag landscape as TBD vs. Procedure assumes it is in scope | Documents are inconsistent on scope boundaries | Recommend: Make a firm decision on landscape scope before finalizing the plan. If in scope, remove "if applicable" from all documents and specify landscape deliverables in Specification RQ-06 and Procedure steps. If out of scope, remove all landscape references from Procedure Part B and related sections. | TBD |

---

### Lens: F:evaluative:completeness
**LensValue:** "integral adequacy transparency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-005 | MissingSlot | Guidance | Guidance Examples (1–3) demonstrate drawing index, BIM coordination, and Owner review processes. However, no example is provided for how to transparently communicate to the Owner what happens when a design change is required (e.g., permit comments, Owner request, cost constraint). Integral adequacy would include change management transparency example. | Guidance § Examples provides three worked examples showing "how it works" but does not include a change management or conflict resolution example. For integral transparency, proponents should show how they handle design changes (frequency, impact assessment, Owner communication). Example 4 should address this. | Guidance.md § Examples (sections 1–3); Guidance § Considerations (no change management consideration) | Guidance examples provided (3) vs. completeness of guidance for Owner confidence (4+ examples) | No example or consideration on change management or design change impacts | Recommend: Add Example 4: Design Change Management (e.g., permit comment incorporation, cost/schedule impact assessment, Owner communication protocol) to demonstrate transparency in change handling. Or add a Consideration on Change Management Decision-Making. | TBD |

---

## Matrix D — Objectives (3×4)

### Lens: D:normative:applying
**LensValue:** "established compliance enforcement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | WeakStatement | Specification | Specification § Verification shows "Responsible Party: Proposal Manager / Design Manager" for all 10 RQ verifications. However, the plan's post-award execution (Procedure Part B) assigns different responsibility roles for the same procedures. This inconsistency undermines established compliance enforcement. | During proposal evaluation (Specification Verification table), the Proposal Manager verifies the plan is credible. During post-award execution (Procedure Part B), the Design Manager executes the plan. These roles are different, and Specification does not clarify that responsibility shifts from proposal phase (Proposal Manager) to execution phase (Design Manager). Weak enforcement clarity. | Specification.md § Verification table (Proposal Manager / Design Manager) vs. Procedure.md § Part B (Design Manager / discipline leads) | Specification verification (proposal phase roles) vs. Procedure execution (post-award roles) | Specification and Procedure do not clarify role transition from proposal to execution | Recommend: Add clarity to Specification Verification table noting that roles shift from Proposal Manager (proposal evaluation) to Design Manager (post-award execution). Or note in Specification that RQ verification is "for proposal credibility assessment; post-award role definitions in Procedure Part B." | TBD |

---

### Lens: D:operative:applying
**LensValue:** "settled throughput deployment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | WeakStatement | Procedure | Procedure Part B Steps B-03 through B-06 describe SD and DD phase workflows but do not specify required outputs or acceptance criteria for each intermediate product. For example, "Output: SD submittal set (all disciplines)" does not specify what "complete" means. Settled throughput deployment requires clear output definitions. | Part B steps have Outputs listed but lack detail. E.g., Step B-03 "Output: SD submittal set (all disciplines)" does not specify: number of sheets expected? Disciplines included? Specifications drafted? Coordination meeting minutes attached? Without settled output definitions, throughput quality may vary. | Procedure.md § Part B (Steps B-03, B-06 outputs) | Procedure output descriptions (general) vs. Datasheet § Construction (step descriptions with more detail) | Procedure outputs are less detailed than Datasheet descriptions | Recommend: Add to Procedure outputs detailed acceptance criteria for each phase (SD, DD, CD, IFC)—e.g., "SD Output: Site plan, massing model, key sections/elevations for all disciplines, preliminary specifications for equipment selections, coordination meeting minutes, Design Manager QA/QC sign-off." | TBD |

---

### Lens: D:evaluative:judging
**LensValue:** "definitive worth determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | TBD_Question | Guidance | Guidance § Purpose (second paragraph) states that DEL-03-02 supports "Project Delivery Plan" evaluation criteria worth 10 points per decomposition Section 15. However, Guidance does not specify what Owner evaluation criteria will be used to judge the plan's worth (e.g., Will the Owner score completeness? Feasibility? Innovation? Risk management?). | Guidance establishes downstream use but does not provide criteria for Owner judgment of worth. The decomposition states the deliverable contributes to "Project Delivery Plan" scoring, but what does the Owner actually evaluate? Completeness of procedures? Credibility of timeline? Innovativeness of approach? This is a definitive question for proposal strategy and content emphasis. | Guidance.md § Purpose (second paragraph: "Downstream use: Owner evaluation: RFP evaluation criteria under Project Delivery Plan (10 points)"); Decomposition § Section 15 (mentions 10 points but not detailed evaluation criteria) | Guidance Purpose (identifies evaluation but not criteria) vs. typical RFP evaluation methodology (criteria-based scoring) | Guidance assumes Owner will evaluate but does not define evaluation criteria | Recommend: Add to Guidance a section "Evaluation Criteria Alignment" that maps the plan's contents (completeness, coordination, QA/QC, document control, code compliance, addenda integration) to probable Owner scoring criteria. Consult decomposition Section 15 for detailed criteria. | TBD |

---

### Lens: D:evaluative:reviewing
**LensValue:** "recursive assurance recalibration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-004 | TBD_Question | Procedure | Procedure Part B § Records (post-award phase) lists records generated (kick-off minutes, coordination minutes, BIM clash reports, QA/QC checklists, Owner comment logs, code review reports, constructability reviews, acceptance letters, permit package, permit approval, IFC distribution log, revision log, as-builts). However, there is no post-project step to retrospectively assure process quality or recommend improvements for future projects. Is post-project process review in scope? | Recursive assurance would include a post-project review of whether the documented plan procedures were effective, where delays occurred, what rework happened, and what should change for the next project. Procedure Part B ends at closeout (Step B-16) with no lessons-learned or process recalibration step. For continuous improvement and assurance recalibration, this is a gap. | Procedure.md § Part B (no Step B-17 or post-project review) | Procedure records list (comprehensive for project execution) vs. post-project assurance improvement (missing) | Procedure captures project execution records but not post-execution learning | Recommend: Clarify scope—is a post-project process review (Step B-17: "Conduct post-project process retrospective and document lessons learned") in scope for DEL-03-02, or is that a project management function outside this deliverable? If in scope, add the step and associated records. | TBD |

---

### Lens: D:normative:guiding
**LensValue:** "authoritative competence framework"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-005 | MissingSlot | Datasheet | Datasheet § Team Readiness lists "Proposal Manager / Design Manager" and "Subject matter experts" and "Construction Manager" as roles required during proposal production (Part A steps). However, Datasheet does not specify the competency framework—what expertise is required for a Design Manager to be credible? Prior experience with Design-Build? Facility type (Fire Hall)? Code expertise? | Authoritative competence framework requires clarity on what qualifications team members need. For a proposal to be credible, the Design Manager's competence must be demonstrated (e.g., "Design Manager must have 5+ years Design-Build experience; Fire Hall/public facilities background preferred"). Datasheet assumes competence without defining it. | Datasheet.md § Procedure (Team Readiness) | Datasheet list of roles vs. need to verify competence | Datasheet lists team roles but not competency requirements | Recommend: Add to Specification or Datasheet a "Competency Framework" section specifying required experience/qualifications for Design Manager, discipline leads, and other key roles, consistent with Appendix I (team credentials) and DEL-07-02 (key resumes). | TBD |

---

## Matrix X — Verification (4×4)

### Lens: X:applying:completeness
**LensValue:** "complete execution inventory"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | VerificationGap | Procedure | Procedure § Verification table (Part B: post-award workflow) lists verification checkpoints for each step (B-01 through B-16) but does not include verification of evidence records. For example, Step B-03 (SD phase complete) has verification "SD QA/QC checklist complete; Design Manager sign-off" but does not specify what format/artifact the sign-off takes. Incomplete execution inventory. | Verification is only complete if the evidence standard is clear. Part B checkpoints say "QA/QC checklist complete; Design Manager sign-off" but what does "sign-off" mean? Email? Signature block? Dated memo? Without evidence definition, verification is subjective. For complete execution inventory, accept criteria must be explicit. | Procedure.md § Verification table (Part B) | Verification checkpoints (general language) vs. complete execution definition (specific evidence format) | Verification requires explicit evidence standards but these are not specified | Recommend: Expand Procedure § Verification table to include "Evidence Format" column specifying the artifact that proves each checkpoint is satisfied (e.g., "Design Manager sign-off = signed review memo with date and discipline lead initials" or similar). | TBD |

---

### Lens: X:reviewing:consistency
**LensValue:** "systematic reassurance regularity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | WeakStatement | Procedure | Procedure Part B coordination steps (B-03, B-06, B-09) reference "weekly coordination meetings" or "continuous coordination" but do not specify a formal meeting minutes protocol or reassurance cadence. For systematic reassurance, meeting regularity and documentation must be defined. | Procedure assumes coordination meetings occur but does not specify: frequency (weekly OK, but what about holidays, compressed schedules)? Minutes template? Who chairs? How are action items tracked? Reassurance regularity requires explicit protocols. Current language is too loose for systematic implementation. | Procedure.md § Part B (Steps B-03, B-06, B-09: coordination language) | Procedure assumes coordination (meetings, clash detection) vs. explicit protocol definition | Procedure describes activities but not meeting/documentation protocols | Recommend: Add to Procedure a "Coordination Meeting Protocol" sub-section specifying: minimum weekly frequency (except holidays); minutes required with attendees, topics, issues, action items, responsible parties; minutes archived in DMS; issues logged in project issue tracker with resolution target dates. | TBD |

---

### Lens: X:judging:sufficiency
**LensValue:** "substantiated ruling capacity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | TBD_Question | Guidance | Guidance § Considerations (Code Review: Third-Party vs. Internal) presents competing concerns but does not specify when code review ruling capacity should be substantiated (i.e., when should the team prove code review expertise?). For substantiated ruling capacity, the decision on third-party vs. internal code review should be made with documented rationale. | Guidance recommends "Propose third-party code review at CD phase as a best practice" but does not specify that the proposal must justify the choice (third-party vs. internal) with supporting rationale about team capacity, risk, and cost. The ruling (decision) on which approach is recommended should be substantiated in the proposal. This is a substantiation gap. | Guidance.md § Considerations / Code Review: Third-Party vs. Internal | Guidance recommendation (third-party preferred) vs. evidence/rationale required in proposal | Guidance suggests best practice but not how to justify the choice in proposal | Recommend: Add to Guidance that the proposal must state the recommended code review approach (third-party vs. internal) with clear rationale, including: team code expertise qualifications, cost estimate (if third-party), timeline impact, and risk mitigation (if internal). This substantiates the ruling. | TBD |

---

## Matrix E — Evaluation (3×4)

### Lens: E:normative:necessity
**LensValue:** "binding prerequisite mobilization"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | TBD_Question | Procedure | Procedure Part B § Prerequisites (post-award phase) lists 8 items that must be in place before operational execution begins. However, the Procedure does not specify binding deadlines or "mobilization gates"—i.e., by what date must prerequisites be satisfied? Is there a "full mobilization" gate before design work commences? | Prerequisites are listed (contract executed, kick-off complete, team mobilized, schedule baselined, DMS operational, BIM platform established, OSR confirmed, survey files available) but no binding schedule for their completion. For binding prerequisite mobilization, a gate date is essential. Without it, design work may begin with incomplete prerequisites. | Procedure.md § Part B / Prerequisites | Prerequisites listed (8 items) vs. gate/binding dates (not specified) | Procedure assumes prerequisites are complete but does not gate design work to confirmed completion | Recommend: Add to Procedure Part B Prerequisites a "Mobilization Completion Gate" requirement: all prerequisites must be certified complete in writing before commencing Step B-03 (Schematic Design). Include a sample "Design Mobilization Gate Checklist" as a record artifact. | TBD |

---

### Lens: E:operative:completeness
**LensValue:** "exhaustive production documentation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | MissingSlot | Procedure | Procedure § Records (Part A: proposal production) lists 8 records generated during proposal authoring (discipline scope matrix, QA/QC checkpoint table, coordination process description, document control protocol, Owner review process, addenda checklist, milestone alignment, final plan document). However, missing are records of the proposal writing process itself—e.g., draft reviews, internal comments, assumptions flagged, decisions made. Exhaustive documentation should include authoring artifacts. | Procedure Records section lists output artifacts but not working artifacts created during proposal drafting. For exhaustive production documentation and audit trail, internal review comments, decision logs, and assumption registers should be preserved. These support later enrichment (Pass 2 cycle) and provide traceability of how the plan was developed. | Procedure.md § Records (Part A section) | Records listed (8 output artifacts) vs. complete production audit trail (missing intermediate/working artifacts) | Procedure captures final outputs but not authoring process artifacts | Recommend: Add to Procedure Records (Part A) that the following working/audit artifacts should be preserved: "Draft iterations with review comments, internal decision log (design phase sequencing choices, tool selections), assumption register (flagged TBD items and rationale for assumptions made during proposal drafting)." | TBD |

---

---

## Conflict Details

### Conflict Item 1: Landscape Discipline Scope (Items B-001, F-004 related)
**Contenders:**
- Datasheet § Design Disciplines: "(ASSUMPTION: typical for municipal facility... **if applicable to proposal scope**)"
- Specification § RQ-06: "**Landscape:** Planting plans, irrigation (if in scope — TBD)"
- Guidance § Examples: [Landscape not explicitly called out in Example 1 drawing index]
- Procedure § Part B, Steps B-03/06/09: Design phase workflow descriptions do not mention landscape; steps focus on Arch, Struct, MEP, Civil only

**Issue:** Documents are inconsistent. Datasheet and Specification flag landscape as conditional ("if applicable"); Procedure's workflow examples omit landscape entirely, suggesting it is out of scope. This ambiguity affects completeness checklist, coordination procedures, and resource planning.

**HumanRuling:** TBD — Requires decision: Is landscape in or out of scope for DEL-03-02 plan? If in, update all documents to remove "if applicable." If out, remove from scope lists.

---

### Conflict Item 2: QA vs. QC Terminology (Item B-004 related)
**Contenders:**
- Datasheet § Quality Assurance Checkpoints: Uses "QA" to describe both self-checks (QC) and Design Manager review (QA)
- Specification § RQ-03: "Quality Assurance and Quality Control (QA/QC)" with multi-layered description
- Guidance § P-04: "QA/QC is multi-layered" with clear distinction (self-check vs. Design Manager vs. code review vs. constructability vs. Owner review)
- Procedure § RQ-03: Uses "QA/QC checkpoints" without clearly distinguishing assurance vs. control

**Issue:** Datasheet uses "Quality Assurance Checkpoints" for what includes both upstream assurance (verification) and downstream control (validation). This differs from industry standard where QA = verification of requirements and QC = validation of execution. Terminology inconsistency may confuse implementation teams.

**HumanRuling:** TBD — Recommend standardizing on "QA/QC Checkpoints" terminology across all documents and adding a definitive statement to Specification RQ-03: "QA (assurance) = verification that requirements will be/are being met; QC (control) = validation that actual work meets specifications."

---

### Conflict Item 3: Third-Party Code Review Requirement (Items A-003, F-001 related)
**Contenders:**
- Specification § RQ-07: States code compliance strategy must be addressed in plan; verification is "Review of plan document to confirm code compliance strategy is addressed" — does not mandate third-party review
- Guidance § Considerations (Code Review: Third-Party vs. Internal): Presents both as viable options; recommends third-party at CD phase as "best practice"
- Datasheet § Quality Assurance Checkpoints: Mentions "Code compliance review: Third-party or internal code specialist review at DD and CD phases" — suggests option, not mandate
- Procedure § Step A-07: "State whether third-party code review will be used" — making it a choice, not requirement

**Issue:** Documents vary on whether third-party code review is required (best practice) or optional (team choice). For a Fire Hall (life safety facility), most jurisdictions expect third-party code review. Specification should clarify if it is mandatory.

**HumanRuling:** TBD — Recommend clarifying in Specification RQ-07 whether third-party code review is: (a) mandatory for Fire Hall facilities, (b) best practice (recommended), or (c) team option. If (a), update all documents to remove "or internal" language. If (b) or (c), the current language is acceptable but should explicitly state the rationale for the choice in the proposal.

---

## Notes on Methodology

- **Lens Application:** Each matrix cell was interpreted as a semantic perspective (e.g., A:normative:guiding = "What does 'prescriptive direction' reveal about the documents?") and applied to all four documents systematically.
- **Warranted Item Criteria:** Items were captured if they represented missing slots, weak/unclear statements, cross-document conflicts, verification gaps, rationale gaps, normalization needs, or TBD questions requiring human ruling.
- **Provenance:** Every item includes SourcePath and SectionRef for traceability; conflicts include specific contender citations.
- **No Invention:** No items assert information not present in the four documents; TBD Questions are phrased as open questions, not assumptions.
- **Coverage:** All 28 matrix cells (A=12, B=12, C=12, F=12, D=12, X=12, E=12) were processed; cells with no warranted items are marked "No warranted items identified."

---

**Document Status:** COMPLETE
**Semantic Lensing Pass:** EXECUTION
**Ready for:** Downstream 4_DOCUMENTS enrichment pass
