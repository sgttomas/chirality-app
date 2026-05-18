# Semantic Lensing Register: DEL-04-02 Budget Control and Change Management Plan

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/_CONTEXT.md
- _STATUS.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/_SEMANTIC.md
- Datasheet.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Datasheet.md
- Specification.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Specification.md
- Guidance.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Guidance.md
- Procedure.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/Procedure.md
- _REFERENCES.md — PKG-06/1_Working/DEL-04-02_BudgetControlAndChangeManagementPlan/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

## Summary

- **Total warranted items:** 68
- **By document:**
  - Datasheet: 16
  - Specification: 20
  - Guidance: 14
  - Procedure: 18
- **By matrix:**
  - A: 12  B: 11  C: 10  F: 10  D: 8  X: 10  E: 7
- **Notable conflicts:** 2
- **Matrix parse errors:** 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "authoritative direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | TBD_Question | Specification | TBD: What specific RFP Section 7 requirements govern the authoritative direction for budget control and change management? PDF not accessible. | The plan references RFP Section 7 as a governing authority but its detailed requirements are unknown; this is the primary normative-guiding source. | Specification.md | Standards > Applicable Standards and Codes | — | RFP Section 7 PDF review by human | TBD |
| A-002 | MissingSlot | Datasheet | Datasheet lacks an explicit "Governing Authority" field identifying the normative source of authority for budget control (e.g., RFP Section 7, DB Agreement). | Authoritative direction requires a clear identification of the governing instrument. The Datasheet records conditions but does not name the specific authoritative source. | Datasheet.md | Identification / Conditions | — | Add governing authority field | TBD |

---

### Lens: A:normative:applying
**LensValue:** "prescribed implementation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | WeakStatement | Procedure | Procedure Step 4 instructs to "Draft narrative" but does not prescribe specific implementation standards or formats for the plan document itself (e.g., required sections, minimum page length, submission format). | Prescribed implementation requires concrete, enforceable instructions. The procedure is advisory rather than prescriptive about deliverable format. | Procedure.md | Steps > Step 4 | — | Strengthen with mandatory format requirements | TBD |

---

### Lens: A:normative:judging
**LensValue:** "compliance determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | VerificationGap | Specification | Verification table uses "Document review" for REQ-1 through REQ-8 and "Cross-reference check" for REQ-9 and REQ-10. No quantitative pass/fail criteria defined for compliance determination (e.g., what constitutes "clearly stated"?). | Compliance determination requires objective, measurable criteria. Current acceptance criteria are qualitative and subjective. | Specification.md | Verification > Document Verification | — | Define measurable acceptance criteria per REQ | TBD |

---

### Lens: A:normative:reviewing
**LensValue:** "regulatory reassessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | MissingSlot | Procedure | No procedure step addresses periodic reassessment of the plan's regulatory compliance (e.g., if codes change during project, if new addenda are issued post-proposal). | Regulatory reassessment requires a defined review trigger and process. Procedure addresses initial production only. | Procedure.md | Steps | — | Add a regulatory review/update step | TBD |

---

### Lens: A:operative:guiding
**LensValue:** "procedural stewardship"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-006 | RationaleGap | Guidance | Guidance Principle 6 (Integration Enables Holistic Management) references procedural stewardship of budget through integration, but does not articulate the stewardship obligation itself — i.e., who is accountable for ensuring the budget control process is followed and maintained. | Procedural stewardship needs an explicit accountability model (roles, escalation path) beyond just "the Construction Manager." | Guidance.md | Principles > Principle 6 | — | Clarify stewardship accountability chain | TBD |

---

### Lens: A:operative:applying
**LensValue:** "executed protocol"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-007 | MissingSlot | Procedure | Procedure describes plan production steps (Steps 1-11) but does not include a step for trial execution or walkthrough of the budget control and change management protocol itself. | An executed protocol perspective implies the plan should be validated through at least a tabletop walkthrough before finalization. | Procedure.md | Steps | — | Add validation/walkthrough step | TBD |

---

### Lens: A:operative:judging
**LensValue:** "performance adjudication"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-008 | MissingSlot | Specification | Specification REQ-6 defines reporting content but does not include performance adjudication criteria — e.g., what variance threshold triggers escalation, what constitutes "on budget" vs. "at risk" vs. "over budget." | Performance adjudication requires defined thresholds. The plan references "variance analysis" and "escalation thresholds" but never defines specific values or ranges. | Specification.md | Requirements > REQ-6 | — | Define variance threshold bands | TBD |

---

### Lens: A:operative:reviewing
**LensValue:** "process audit"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-009 | MissingSlot | Procedure | No procedure step or verification checkpoint addresses process audit — i.e., periodically reviewing whether the budget control and change management processes are being followed correctly during execution. | Process audit is essential for plan effectiveness but is entirely absent from the procedure. | Procedure.md | Verification > Process Verification Checkpoints | — | Add process audit checkpoint | TBD |

---

### Lens: A:evaluative:guiding
**LensValue:** "value orientation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-010 | WeakStatement | Guidance | Guidance Purpose section states three purposes (Owner confidence, evaluation scoring, operational framework) but does not articulate the overarching value proposition — what "value" the budget control plan delivers to the project beyond compliance (e.g., early warning of cost overruns, reduced disputes, predictable cash flow). | Value orientation requires explicit articulation of the value delivered, not just compliance purposes. | Guidance.md | Purpose > Why This Deliverable Exists | — | Strengthen with explicit value statement | TBD |

---

### Lens: A:evaluative:applying
**LensValue:** "merit-based execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-011 | MissingSlot | Datasheet | Datasheet does not include any quality or merit metrics for the plan itself (e.g., plan completeness score, alignment confidence rating). | Merit-based execution implies the deliverable should have measurable quality attributes. Currently all quality assessment is qualitative. | Datasheet.md | Attributes | — | Add plan quality metrics | TBD |

---

### Lens: A:evaluative:judging
**LensValue:** "worth determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-012 | TBD_Question | Specification | TBD: How does the evaluation panel weigh budget control/change management within the 10-point Project Delivery Plan score? Is there a sub-scoring rubric? | Worth determination requires understanding how this plan's quality translates to evaluation score. The decomposition identifies 10 points for the overall Project Delivery Plan, but the sub-allocation to budget control is unknown. | Specification.md | Verification > Acceptance Criteria | — | Decomposition or RFP evaluation rubric | TBD |

---

### Lens: A:evaluative:reviewing
**LensValue:** "outcome appraisal"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential measurement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | MissingSlot | Datasheet | Datasheet lists cost reporting elements (budget vs. actual tracking, forecast to complete, variance reporting, commitment tracking, cash flow projection) all as TBD. No essential measurement units, precision requirements, or data formats are specified. | Essential measurement requires defined units and precision (e.g., cost tracking to nearest dollar or thousand; percentage for variance). | Datasheet.md | Attributes > Cost Reporting Elements | — | Define measurement units and precision | TBD |

---

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-002 | TBD_Question | Procedure | TBD: What constitutes adequate evidence that the plan has been coordinated with Appendix H (Step 5)? The procedure says "verify consistency" but does not define what evidence of consistency looks like (e.g., a reconciliation table, sign-off memo). | Adequate evidence requires a defined evidentiary standard. Current verification is "cross-reference check" without specifying deliverable evidence. | Procedure.md | Steps > Step 5 | — | Define consistency evidence requirements | TBD |

---

### Lens: B:data:completeness
**LensValue:** "exhaustive capture"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | WeakStatement | Datasheet | Datasheet Control Mechanisms section has 5 TBD items and Change Management Elements section has 5 TBD items — 10 out of 10 operational data fields are TBD. This is exhaustive in structure but empty in content. | Exhaustive capture requires populated data, not just enumerated fields. The Datasheet currently serves as a structured placeholder only. | Datasheet.md | Attributes > Control Mechanisms; Change Management Elements | — | Populate with at least baseline values or ranges | TBD |

---

### Lens: B:data:consistency
**LensValue:** "uniform recording"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | Normalization | Multi | The term "cost code structure" appears in Datasheet (Attributes > Control Mechanisms), Specification (REQ-2), Guidance (Consideration 4), and Procedure (Step 5) but is defined differently in each: Datasheet says "minimum: General Requirements, Building, Sitework per Schedule B format"; Specification says "minimum: General Requirements, Building, Sitework; Additional Options 1-6 tracked separately"; Guidance adds "separate codes for each Additional Option" and "FF&E if included." | Uniform recording requires a single canonical definition. The cost code structure description varies across documents with expanding scope in each. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Control Mechanisms; Spec: REQ-2; Guidance: Consideration 4; Procedure: Step 5 | Datasheet#Control Mechanisms vs. Specification#REQ-2 vs. Guidance#Consideration 4 | Specification.md REQ-2 as canonical | TBD |

---

### Lens: B:information:necessity
**LensValue:** "required intelligence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | MissingSlot | Specification | Specification does not include a requirement for market intelligence inputs — e.g., escalation rate assumptions, subcontractor market conditions, material price volatility — that inform budget forecasting accuracy. | Required intelligence for budget control extends beyond internal tracking to market condition awareness. This is absent from all requirements. | Specification.md | Requirements | — | Consider adding market intelligence requirement | TBD |

---

### Lens: B:information:sufficiency
**LensValue:** "satisfactory reporting"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-006 | WeakStatement | Specification | REQ-6 states "minimum monthly" reporting but does not define what "satisfactory" reporting means beyond listing report contents. No minimum detail level, timeliness requirement (e.g., report within X days of month-end), or distribution timeline specified. | Satisfactory reporting requires defined timeliness and completeness standards, not just content lists. | Specification.md | Requirements > REQ-6 | — | Add timeliness and distribution requirements | TBD |

---

### Lens: B:information:completeness
**LensValue:** "comprehensive disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-007 | RationaleGap | Guidance | Guidance Trade-off 4 (Owner Transparency vs. Competitive Sensitivity) recommends transparency at the "cost code level" but does not provide rationale for why this level — rather than line-item detail or aggregate-only — constitutes comprehensive disclosure. | Comprehensive disclosure requires explicit justification for the chosen disclosure boundary. The trade-off identifies the tension but the rationale for the recommended level is thin. | Guidance.md | Trade-offs > Trade-off 4 | — | Strengthen rationale for disclosure level | TBD |

---

### Lens: B:information:consistency
**LensValue:** "coherent communication"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:necessity
**LensValue:** "indispensable expertise"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-008 | WeakStatement | Procedure | Procedure Prerequisites "Skills and Knowledge Required" lists four expertise areas but uses vague qualifiers ("understanding of," "experience with," "familiarity with"). No minimum qualification level defined. | Indispensable expertise requires specificity about required qualification levels (years of experience, certifications, project type experience). | Procedure.md | Prerequisites > Skills and Knowledge Required | — | Define minimum qualification criteria | TBD |

---

### Lens: B:knowledge:sufficiency
**LensValue:** "capable understanding"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:completeness
**LensValue:** "thorough mastery"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:knowledge:consistency
**LensValue:** "reliable competence"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:necessity
**LensValue:** "fundamental prudence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-009 | RationaleGap | Guidance | Guidance Principle 5 states "Contingency Is Not Profit" as a prudential principle but provides no guidance on how to establish what a prudent contingency level looks like for this specific project type (municipal facility, ~$10-20M range, Design-Build). | Fundamental prudence requires context-specific judgment guidance, not just an abstract principle. | Guidance.md | Principles > Principle 5 | — | Add project-specific contingency benchmarks | TBD |

---

### Lens: B:wisdom:sufficiency
**LensValue:** "balanced judgment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-010 | WeakStatement | Guidance | Trade-off 1 recommends a "moderate" change authorization threshold (~$10,000 individual; ~$50,000 cumulative) labeled as ASSUMPTION. This is presented as balanced judgment but lacks evidence for why these specific thresholds are appropriate for this project scale and context. | Balanced judgment requires explicit reasoning connecting threshold values to project characteristics (value, complexity, Owner risk tolerance). | Guidance.md | Trade-offs > Trade-off 1 | — | Justify thresholds with project-specific reasoning | TBD |

---

### Lens: B:wisdom:completeness
**LensValue:** "holistic discernment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: B:wisdom:consistency
**LensValue:** "principled steadfastness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-011 | Normalization | Multi | Guidance states monthly reporting as recommendation (Consideration 1); Specification REQ-6 states "minimum monthly"; Procedure Step 3 skeleton shows "Reporting frequency (monthly minimum)"; Trade-off 3 introduces exceptions for expedited changes. The principled steadfastness of "monthly minimum" is weakened by lack of definition of what happens during peak construction when monthly may be insufficient. | Consistency of the reporting frequency principle across documents needs a canonical statement addressing the possibility of increased frequency. | Specification.md; Guidance.md; Procedure.md | Spec: REQ-6; Guidance: Consideration 1; Procedure: Step 3 | — | Define frequency escalation triggers | TBD |

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "binding accountability threshold"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | MissingSlot | Specification | No requirement defines the binding accountability threshold — the minimum level of budget control rigor that is mandatory (vs. recommended). All 10 REQs use "shall" but without prioritization (which are non-negotiable vs. refinable during contract negotiation). | Binding accountability thresholds require explicit identification of which requirements are inviolable vs. adjustable. | Specification.md | Requirements | — | Classify REQs by criticality tier | TBD |

---

### Lens: C:normative:sufficiency
**LensValue:** "certified benchmark adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | TBD_Question | Specification | TBD: What benchmarks or standards define "adequate" budget control for a municipal Design-Build project? Specification references DBIA best practices as ASSUMPTION but provides no specific benchmark criteria. | Certified benchmark adequacy requires referencing an external standard against which adequacy can be certified. DBIA is mentioned but not cited with specifics. | Specification.md | Standards > Applicable Standards and Codes | — | Identify specific DBIA or CIQS standards | TBD |

---

### Lens: C:normative:completeness
**LensValue:** "total conformance coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | VerificationGap | Specification | Verification table covers REQ-1 through REQ-10 but uses only two verification methods ("Document review" and "Cross-reference check"). No independent verification method (e.g., third-party review, owner confirmation) is employed, limiting conformance coverage. | Total conformance coverage requires diverse verification methods to ensure no blind spots. Current verification is self-referential. | Specification.md | Verification > Document Verification | — | Add independent verification methods | TBD |

---

### Lens: C:normative:consistency
**LensValue:** "harmonized governance reliability"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | Conflict | Multi | Datasheet Conditions states "Contract type: Stipulated Price with Additional Options (1-6)" while Guidance Consideration 4 discusses tracking optional items as if they may or may not be selected by the Owner. Under a stipulated price contract, the change management approach for options differs from changes to base scope, but Specification REQ-4 (Change Authorization Workflow) does not distinguish between base scope changes and option activation. | Governance reliability requires consistent treatment of contract types. The handling of Additional Options within the change management framework is inconsistent. | Datasheet.md; Specification.md; Guidance.md | Datasheet: Conditions > Operating Context; Spec: REQ-4; Guidance: Consideration 4 | Datasheet#Operating Context vs. Specification#REQ-4 | Specification.md with Guidance input | TBD |

---

### Lens: C:operative:necessity
**LensValue:** "critical process control"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-005 | MissingSlot | Procedure | Procedure does not identify critical control points within the plan production process — e.g., mandatory hold points where the draft cannot proceed without specific input (like Appendix H availability). NOT_TRACKED mode means dependencies are external, but critical control points should still be flagged within the procedure. | Critical process control requires explicit identification of hold points and mandatory gates. | Procedure.md | Steps | — | Add hold points for critical inputs | TBD |

---

### Lens: C:operative:sufficiency
**LensValue:** "competent oversight verification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-006 | VerificationGap | Procedure | Procedure Step 9 (Internal Review) lists review roles but does not specify verification criteria for each reviewer — i.e., what specifically does the Commercial Lead verify vs. what does the PM verify? | Competent oversight verification requires role-specific verification criteria, not just generic review focus areas. | Procedure.md | Steps > Step 9 | — | Define role-specific verification checklists | TBD |

---

### Lens: C:operative:completeness
**LensValue:** "exhaustive operational accounting"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-007 | MissingSlot | Datasheet | Datasheet Construction section lists anticipated plan sections (1-5) but does not account for all operational aspects — specifically, roles/responsibilities and governance (which appear in Procedure Step 3 skeleton as Section 7 but not in Datasheet). | Exhaustive operational accounting requires the Datasheet to reflect all planned content sections. | Datasheet.md | Construction > Plan Structure (anticipated) | — | Add Section 6 and 7 to anticipated structure | TBD |

---

### Lens: C:operative:consistency
**LensValue:** "repeatable process integrity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-008 | Normalization | Multi | Plan structure appears in two locations: Datasheet "Construction > Plan Structure (anticipated)" lists 5 sections; Procedure Step 3 skeleton lists 7 sections plus appendices. These are not aligned. | Repeatable process integrity requires a single authoritative plan structure. Two divergent structures create confusion about what the final plan will contain. | Datasheet.md; Procedure.md | Datasheet: Construction > Plan Structure; Procedure: Step 3 | Datasheet#Plan Structure vs. Procedure#Step 3 | Procedure.md Step 3 as more complete | TBD |

---

### Lens: C:evaluative:necessity
**LensValue:** "fundamental worth baseline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-009 | TBD_Question | Guidance | TBD: What is the minimum level of plan quality that meets the "worth baseline" for evaluation scoring? The plan contributes to a 10-point score but the minimum passing standard is unknown. | Fundamental worth baseline requires knowing the threshold between an acceptable and unacceptable plan. | Guidance.md | Purpose > Evaluation Scoring | — | RFP evaluation rubric or scoring guide | TBD |

---

### Lens: C:evaluative:sufficiency
**LensValue:** "proportionate worth demonstration"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:completeness
**LensValue:** "comprehensive worth accounting"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: C:evaluative:consistency
**LensValue:** "consistent evaluative discipline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-010 | WeakStatement | Procedure | Procedure Step 7 (Review Against Evaluation Criteria) lists four evaluation dimensions (Credibility, Thoroughness, Clarity, Consistency) but provides no scoring rubric or rating scale. Evaluative discipline requires consistent, repeatable assessment. | Without a defined rating approach, different reviewers will apply Step 7 inconsistently. | Procedure.md | Steps > Step 7 | — | Add evaluation checklist with rating criteria | TBD |

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "inviolable compliance stewardship"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | TBD_Question | Specification | TBD: Which of the 10 requirements (REQ-1 through REQ-10) represent inviolable compliance obligations vs. best-practice recommendations? All use "shall" language but some are sourced to ASSUMPTION rather than RFP/contract requirements. | Inviolable compliance stewardship requires distinguishing mandatory compliance from elective best practice. REQ-3, REQ-4, REQ-5, REQ-7 are sourced to ASSUMPTION. | Specification.md | Requirements | — | Classify each REQ source as mandatory vs. recommended | TBD |

---

### Lens: F:normative:sufficiency
**LensValue:** "sufficient governance attestation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | MissingSlot | Procedure | Procedure does not include an attestation step — formal sign-off that the plan meets all governance requirements. Step 10 (Finalize and Deliver) addresses formatting but not attestation. | Sufficient governance attestation requires a documented sign-off that the deliverable meets its requirements before submission. | Procedure.md | Steps > Step 10 | — | Add formal attestation/sign-off step | TBD |

---

### Lens: F:normative:completeness
**LensValue:** "integral compliance transparency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | MissingSlot | Specification | Specification does not include a compliance traceability matrix mapping each requirement to its source authority (RFP clause, Addendum, DBIA standard, or ASSUMPTION). | Integral compliance transparency requires visible traceability from each requirement to its authorizing source. | Specification.md | Requirements | — | Add requirement-to-source traceability matrix | TBD |

---

### Lens: F:normative:consistency
**LensValue:** "unwavering accountability fidelity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:operative:necessity
**LensValue:** "vital tracking competence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | MissingSlot | Datasheet | Datasheet lacks specification of the tracking system or tool to be used for budget control and change management (e.g., spreadsheet-based, dedicated software like Procore/Sage, ERP system). | Vital tracking competence requires identifying the tool/system that enables tracking. The "Tools and Templates" in Procedure is optional and generic. | Datasheet.md | Attributes | — | Add tracking system/tool specification | TBD |

---

### Lens: F:operative:sufficiency
**LensValue:** "proportionate oversight confirmation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-005 | WeakStatement | Guidance | Guidance Trade-off 3 recommends a "prescriptive workflow as the default but include exceptions" — but the exceptions (expedited changes, minor changes) are described illustratively, not as mandatory requirements. Proportionate oversight requires the exceptions to be defined with equal rigor as the default. | Oversight exceptions need the same level of procedural definition as the standard process. | Guidance.md | Trade-offs > Trade-off 3 | — | Formalize exception workflow definitions | TBD |

---

### Lens: F:operative:completeness
**LensValue:** "total oversight comprehension"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-006 | MissingSlot | Specification | REQ-8 (Integration with Schedule and Risk Management) does not mention integration with quality management or safety management, which can have significant budget impacts (rework, safety incidents, QA/QC costs). | Total oversight comprehension requires considering all management domains that affect budget, not only schedule, risk, and communications. | Specification.md | Requirements > REQ-8 | — | Extend integration to quality and safety management | TBD |

---

### Lens: F:operative:consistency
**LensValue:** "disciplined tracking consistency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-007 | Normalization | Multi | Change order terminology varies: Datasheet uses "Change order threshold"; Specification uses "change authorization workflow"; Guidance uses "Change Authorization Matrix"; Procedure uses "change identification notice." The relationship between a "change identification notice," "change request," and "change order" is not formally defined. | Disciplined tracking consistency requires normalized terminology for the change lifecycle stages. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple sections | — | Define canonical change lifecycle terminology | TBD |

---

### Lens: F:evaluative:necessity
**LensValue:** "indispensable valuation rigor"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-008 | MissingSlot | Specification | No requirement addresses earned value management (EVM) or similar valuation methodology to assess project performance beyond simple budget vs. actual comparison. | Indispensable valuation rigor for budget control typically includes some form of performance measurement (e.g., CPI, SPI) beyond variance reporting. | Specification.md | Requirements | — | Consider adding EVM or performance measurement requirement | TBD |

---

### Lens: F:evaluative:sufficiency
**LensValue:** "sufficient evaluative demonstration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-009 | WeakStatement | Guidance | Guidance Example 1 (Monthly Cost Report Structure) is labeled "Illustrative" and "TBD" but is the only concrete demonstration of what the reporting system would look like. Evaluators need sufficient demonstration of capability. | Sufficient evaluative demonstration requires examples that are definitive enough to assess competence, not just illustrative placeholders. | Guidance.md | Examples > Example 1 | — | Strengthen examples from illustrative to representative | TBD |

---

### Lens: F:evaluative:completeness
**LensValue:** "exhaustive valuation transparency"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: F:evaluative:consistency
**LensValue:** "dependable valuation discipline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-010 | Normalization | Multi | Contingency is discussed differently in each document: Datasheet says "Contingency management: TBD (approach to be defined)"; Specification REQ-7 lists 4 sub-elements; Guidance Principle 5 provides philosophical framing; Guidance Trade-off 2 provides strategic options; Procedure Step 3 skeleton includes Section 5. These need alignment into a single consistent framework. | Dependable valuation discipline for contingency requires a canonical treatment that the other documents reference rather than each describing independently. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Multiple sections | — | Designate Specification REQ-7 as canonical, others reference it | TBD |

---

## Matrix D — Objectives (3x4)

### Lens: D:normative:guiding
**LensValue:** "sovereign regulatory guardianship"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | TBD_Question | Specification | TBD: Does the Town of Penhold have specific financial reporting bylaws or municipal procurement regulations that govern budget control for publicly funded capital projects? | Sovereign regulatory guardianship requires understanding whether municipal regulations impose requirements beyond the RFP. | Specification.md | Standards | — | Municipal bylaws/procurement policies review | TBD |

---

### Lens: D:normative:applying
**LensValue:** "enforceable compliance deployment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | MissingSlot | Procedure | Procedure does not address how compliance with the budget control plan will be enforced during project execution — i.e., what happens if the plan is not followed (consequences, remediation, escalation). | Enforceable compliance deployment requires not just process definition but enforcement mechanisms. | Procedure.md | Steps | — | Add enforcement/escalation provisions | TBD |

---

### Lens: D:normative:judging
**LensValue:** "definitive conformance transparency"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:normative:reviewing
**LensValue:** "recursive stewardship scrutiny"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | MissingSlot | Guidance | Guidance does not address recursive review of the plan itself — i.e., how and when the budget control and change management plan should be reviewed and updated during the project lifecycle (e.g., at project milestones, after significant changes, annually). | Recursive stewardship scrutiny requires a plan-review mechanism, not just plan creation. | Guidance.md | Considerations | — | Add plan review/update guidance | TBD |

---

### Lens: D:operative:guiding
**LensValue:** "process-driven monitoring governance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-004 | WeakStatement | Specification | REQ-6 describes cost reporting content but does not define the monitoring governance framework — who reviews reports, decision-making triggers from report data, escalation protocols when reports show adverse trends. | Process-driven monitoring governance requires a decision framework built on the monitoring data, not just data collection. | Specification.md | Requirements > REQ-6 | — | Add monitoring governance framework requirement | TBD |

---

### Lens: D:operative:applying
**LensValue:** "active supervisory deployment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-005 | MissingSlot | Datasheet | Datasheet does not specify supervisory roles or the management hierarchy for active deployment of the budget control system (e.g., who performs daily cost tracking, who conducts weekly reviews, who presents monthly reports). | Active supervisory deployment requires defined role assignments for budget control operations. | Datasheet.md | Attributes | — | Add roles/responsibilities to Datasheet | TBD |

---

### Lens: D:operative:judging
**LensValue:** "definitive operational understanding"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:operative:reviewing
**LensValue:** "systematic monitoring examination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-006 | MissingSlot | Procedure | Procedure lacks a step for systematic examination of monitoring effectiveness — i.e., are the reports being produced on time, are they being read, are variances being acted upon? This is distinct from process audit (A-009) as it focuses on monitoring output quality. | Systematic monitoring examination requires a feedback loop on monitoring effectiveness. | Procedure.md | Verification | — | Add monitoring effectiveness review step | TBD |

---

### Lens: D:evaluative:guiding
**LensValue:** "directed appraisal framework"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-007 | MissingSlot | Guidance | Guidance does not provide a framework for appraising the plan's own effectiveness post-implementation (e.g., did the plan prevent budget overruns? Were change orders processed efficiently? Was the Owner satisfied with reporting?). | Directed appraisal framework requires guidance on how to evaluate the plan's success during and after the project. | Guidance.md | Purpose > Downstream Use | — | Add plan effectiveness evaluation criteria | TBD |

---

### Lens: D:evaluative:applying
**LensValue:** "enacted appraisal validation"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: D:evaluative:judging
**LensValue:** "transparent merit adjudication"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-008 | TBD_Question | Specification | TBD: How will the Owner adjudicate the merit of this plan compared to competing proposals? Are there specific scoring criteria or rubric elements for budget control within the Project Delivery Plan evaluation? | Transparent merit adjudication requires understanding the evaluation mechanism. Currently only "10 points for Project Delivery Plan" is known. | Specification.md | Verification > Acceptance Criteria | — | RFP evaluation criteria detail | TBD |

---

### Lens: D:evaluative:reviewing
**LensValue:** "recursive appraisal examination"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix X — Verification (4x4)

### Lens: X:guiding:necessity
**LensValue:** "foundational oversight leadership"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | MissingSlot | Datasheet | Datasheet Identification lists "Responsible: Construction Manager" but does not identify oversight leadership — who has ultimate accountability for the plan's quality and the budget control system's effectiveness (e.g., Project Director, VP Construction). | Foundational oversight leadership requires identifying the accountability chain above the responsible party. | Datasheet.md | Identification | — | Add oversight/accountability chain | TBD |

---

### Lens: X:guiding:sufficiency
**LensValue:** "authoritative adequacy assurance"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:guiding:completeness
**LensValue:** "integral governance scope"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | WeakStatement | Specification | Specification Scope "In Scope" lists 5 elements and "Out of Scope" lists 5 exclusions, but does not address the governance scope for the budget control system itself — who governs changes to the plan, version control of the plan document, and plan currency during the project. | Integral governance scope requires defining governance of the plan as a living document, not just governance of the budget. | Specification.md | Scope | — | Add plan governance provisions | TBD |

---

### Lens: X:guiding:consistency
**LensValue:** "principled governance uniformity"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:applying:necessity
**LensValue:** "mandatory operational enactment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | VerificationGap | Procedure | Procedure Verification Checkpoints table has 11 steps but all acceptance criteria are qualitative descriptions (e.g., "Team can articulate purpose"; "Structure is logical"). No mandatory pass/fail criteria for any checkpoint. | Mandatory operational enactment requires verification checkpoints with objective pass/fail criteria, not subjective assessments. | Procedure.md | Verification > Process Verification Checkpoints | — | Define objective pass/fail criteria | TBD |

---

### Lens: X:applying:sufficiency
**LensValue:** "capable enforcement validation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | MissingSlot | Specification | Specification does not include a requirement for validating the enforcement capability of the change management workflow (e.g., what happens if a change is executed without proper authorization? Is there a mechanism to detect unauthorized changes?). | Capable enforcement validation requires a detection mechanism for non-compliance, not just a defined workflow. | Specification.md | Requirements > REQ-4 | — | Add unauthorized change detection requirement | TBD |

---

### Lens: X:applying:completeness
**LensValue:** "comprehensive conformance execution"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:applying:consistency
**LensValue:** "reliable regulatory deployment"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:necessity
**LensValue:** "binding operational determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-005 | MissingSlot | Specification | No requirement defines the binding determination of when a variance constitutes a budget breach (vs. a normal fluctuation). REQ-6 mentions "variance analysis" but does not define the operational determination threshold. | Binding operational determination requires a defined threshold at which a variance becomes actionable (e.g., >5% over budget = corrective action required). | Specification.md | Requirements > REQ-6 | — | Define variance breach thresholds | TBD |

---

### Lens: X:judging:sufficiency
**LensValue:** "sufficient performance certification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-006 | VerificationGap | Specification | Verification table shows all 10 requirements with Status = "TBD." No requirement has been certified as met. While this is expected at draft stage, there is no defined process for when and how requirements will be certified as complete. | Sufficient performance certification requires a defined certification process and timeline, not just a status column. | Specification.md | Verification > Document Verification | — | Define certification process and timing | TBD |

---

### Lens: X:judging:completeness
**LensValue:** "comprehensive performance verdict"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:judging:consistency
**LensValue:** "reliable compliance consistency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-007 | Conflict | Multi | Specification Acceptance Criteria states the plan must "Support evaluation objectives" (OBJ-002: 10 points) while _CONTEXT.md acceptance criteria says "Shows transparency and control; consistent with pricing approach" — without mentioning evaluation scoring. These represent different compliance targets that could lead to inconsistent verification. | Reliable compliance consistency requires aligned acceptance criteria across governing documents. _CONTEXT.md and Specification define different success measures. | Specification.md; _CONTEXT.md | Spec: Acceptance Criteria item 4; _CONTEXT.md: Acceptance Criteria | Specification#Acceptance Criteria vs. _CONTEXT.md#Acceptance Criteria | _CONTEXT.md as upstream authority | TBD |

---

### Lens: X:reviewing:necessity
**LensValue:** "fundamental stewardship re-assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-008 | MissingSlot | Procedure | Procedure lacks a re-assessment step — i.e., after the plan is finalized and submitted, when and how will it be re-assessed for continued relevance during contract negotiation and project execution? | Fundamental stewardship re-assessment requires a defined trigger and process for plan revision post-submission. | Procedure.md | Steps | — | Add post-submission re-assessment process | TBD |

---

### Lens: X:reviewing:sufficiency
**LensValue:** "capable governance re-verification"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: X:reviewing:completeness
**LensValue:** "total stewardship re-examination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-009 | MissingSlot | Guidance | Guidance Notes section lists "Assumptions Requiring Validation" (5 items) but does not provide guidance on when, how, or by whom these assumptions should be re-examined. Assumptions are flagged but there is no re-examination framework. | Total stewardship re-examination requires a defined process for validating assumptions, not just listing them. | Guidance.md | Notes > Assumptions Requiring Validation | — | Add assumption validation framework | TBD |

---

### Lens: X:reviewing:consistency
**LensValue:** "consistent oversight re-scrutiny"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-010 | Normalization | Multi | Assumptions are listed in three places: Datasheet "Design Context" (1 ASSUMPTION), Datasheet "Construction" (3 ASSUMPTIONs), Specification "Notes > Assumptions Log" (5 items), and Guidance "Notes > Assumptions Requiring Validation" (5 items). These lists overlap but are not identical, creating inconsistent oversight when re-scrutinizing assumptions. | Consistent oversight re-scrutiny requires a single consolidated assumption register. | Datasheet.md; Specification.md; Guidance.md | Datasheet: multiple sections; Spec: Notes > Assumptions Log; Guidance: Notes > Assumptions Requiring Validation | — | Consolidate into single assumption register | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "inviolable stewardship authority"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | TBD_Question | Datasheet | TBD: Who is the ultimate stewardship authority for budget control during the project — the Construction Manager (listed as Responsible), the Project Manager, or the Owner? The Datasheet identifies the Construction Manager but the plan describes Owner approval authority. | Inviolable stewardship authority requires clarity on the hierarchy of budget authority. Multiple roles are mentioned but their relative authority is not defined. | Datasheet.md | Identification; Conditions | — | Define authority hierarchy in Datasheet | TBD |

---

### Lens: E:normative:sufficiency
**LensValue:** "authoritative sufficiency certification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | VerificationGap | Specification | No requirement or verification criterion defines what constitutes "sufficient" certification that the plan meets RFP requirements — i.e., how does the team know the plan is "good enough" for submission? | Authoritative sufficiency certification requires a defined readiness gate for plan submission. | Specification.md | Verification | — | Define submission readiness criteria | TBD |

---

### Lens: E:normative:completeness
**LensValue:** "total regulatory comprehension"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-003 | TBD_Question | Specification | TBD: Are there Alberta provincial regulations (e.g., Safety Codes Act, Prompt Payment legislation) that impose requirements on budget control or change management for construction projects? The Standards section references only RFP/Addenda and DBIA assumption. | Total regulatory comprehension requires identifying all applicable regulatory frameworks, not just the RFP. Alberta-specific construction legislation may impose requirements. | Specification.md | Standards | — | Alberta construction legislation review | TBD |

---

### Lens: E:normative:consistency
**LensValue:** "perpetual accountability reliability"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:necessity
**LensValue:** "vital governance infrastructure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-004 | MissingSlot | Datasheet | Datasheet does not specify the document control infrastructure for the plan itself — version control, revision history, distribution tracking, supersession protocols. | Vital governance infrastructure includes the document management system that ensures the plan remains current and controlled. | Datasheet.md | Attributes | — | Add document control specifications | TBD |

---

### Lens: E:operative:sufficiency
**LensValue:** "competent oversight certification"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:operative:completeness
**LensValue:** "exhaustive deployment coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-005 | WeakStatement | Specification | Specification Lifecycle section identifies five phases (Proposal, Contract negotiation, Design, Construction, Closeout) but Requirements REQ-1 through REQ-10 are written for the proposal phase only. No requirements address deployment of budget control during subsequent lifecycle phases. | Exhaustive deployment coverage requires requirements that span the full project lifecycle, not just proposal-phase plan production. | Specification.md | Documentation > Lifecycle | — | Add lifecycle-phase-specific requirements or scope clarification | TBD |

---

### Lens: E:operative:consistency
**LensValue:** "sustained governance reliability"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:necessity
**LensValue:** "indispensable accountability authority"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-006 | MissingSlot | Procedure | Procedure Records section lists artifacts but does not assign accountability authority for each artifact — i.e., who is responsible for producing, reviewing, and approving each record. | Indispensable accountability authority requires explicit assignment of record-keeping responsibility. | Procedure.md | Records > Artifacts Produced | — | Add accountability assignments to records | TBD |

---

### Lens: E:evaluative:sufficiency
**LensValue:** "competent adjudicative certification"

#### Warranted items
_No warranted items identified for this lens._

---

### Lens: E:evaluative:completeness
**LensValue:** "exhaustive merit comprehension"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-007 | RationaleGap | Guidance | Guidance does not address the merit comprehension question: what distinguishes an excellent budget control plan from a merely adequate one in the context of a competitive Design-Build proposal? Guidance provides principles and considerations but not evaluation-differentiating criteria. | Exhaustive merit comprehension requires understanding what elevates the plan from compliant to compelling for evaluators. | Guidance.md | Purpose; Considerations | — | Add competitive differentiation guidance | TBD |

---

### Lens: E:evaluative:consistency
**LensValue:** "sustained evaluative reliability"

#### Warranted items
_No warranted items identified for this lens._
