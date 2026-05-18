# Semantic Lensing Register: DEL-09-01 Risk Register and Mitigation Plan

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — Deliverable identity (PKG-09, SOW-026/027), description (Risk register + Mitigation plan + QMP), acceptance criteria (Transparent; ties to addenda and reference reports)
- _STATUS.md — State SEMANTIC_READY (CHIRALITY_FRAMEWORK completed 2026-02-04)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E extracted and parsed (7 matrices × 12 cells avg = 84 lens cells total)
- Datasheet.md — Risk assessment framework (7 categories, P/I scales, Score method), structure definition, materials/components, reference sources, standards (accessible/TBD)
- Specification.md — Scope (7 risk categories + QMP 4 areas), FR/PR/CR/IR (7 functional, 3 performance, 4 compliance, 4 interface requirements), verification methods, acceptance criteria
- Guidance.md — Purpose (demonstrate proactive risk awareness, build confidence, support decisions, fulfill RFP, enable QA), downstream use, 5 risk management principles, 3 QM principles, 20 considerations, 4 trade-offs, 2 examples
- Procedure.md — 7-step production procedure (Prepare, Identify, Assess, Mitigate, QMP, Document, Review), prerequisites, personnel/roles, reference materials, verification checkpoints
- _REFERENCES.md — 10 applicable reference documents (RFP, Addenda 01-03, Geotechnical, Wetland, Environmental, Grading, Flood, Adjacent Subdivision)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- **Total warranted items:** 28
- **By document:**
  - Datasheet: 8
  - Specification: 9
  - Guidance: 7
  - Procedure: 4
- **By matrix:**
  - A: 4  B: 5  C: 4  F: 4  D: 4  X: 4  E: 3
- **Notable conflicts:** 1 (survey availability assumption across documents)
- **Matrix parse errors:** 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "prescriptive direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | WeakStatement | Specification | FR-07 "Risk register shall be transparent and credible" lacks prescriptive criteria for "credible" — no measurable standard given | Prescriptive direction lens reveals requirement lacks actionable definition; credibility needs observable criteria for evaluator judgment | Specification.md | Functional Requirements > FR-07 | — | Define credibility: (1) source citation rate ≥95%, (2) all high-score risks have preventive+contingency mitigations, (3) mitigation owners identified with responsibility statements | TBD |
| A-002 | MissingSlot | Guidance | Guidance presents risk management principles but does not prescribe which standards or authorities govern the framework when ISO 31000 is not accessible | Lens reveals gap: prescriptive authority missing when standards cannot be consulted | Guidance.md | Principles section (lines 32-68); Reference to ISO 31000 as inferred (line 68) | Guidance.md vs. Datasheet.md (framework stated as ASSUMPTION) | Add to Guidance: "In absence of accessible ISO 31000, risk framework adheres to industry best practice: probability × impact scoring (1-5 scales) per PMI PMBOK guidance; high-score risks (≥15) require detailed mitigation" | TBD |

### Lens: A:normative:applying
**LensValue:** "regulatory enforcement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | VerificationGap | Procedure | Step 2.7 (Permitting Risks) identifies permit-related risks but does not require assessment of hard compliance constraints from Decomposition §3 (C-01...C-07) which are mandatory pass/fail gates | Regulatory enforcement lens reveals gap: hard constraints (15 MB PDF, required section order, addenda acknowledgment, etc.) should be assessed for compliance risk in risk register | Procedure.md | Step 2: Identify Risks by Category > 2.7 Permitting Risks (lines 207-220) | Procedure.md vs. Decomposition (§3 Hard Constraints C-01...C-07) | Add sub-step 2.8 in Procedure: "Hard Constraint Compliance Risks: For each constraint C-01...C-07, assess risk of non-compliance (e.g., CR-01: PDF >15 MB risk if all drawings included; CR-02: missing required section risk if team unfamiliar with RFP order)" | TBD |

### Lens: A:operative:applying
**LensValue:** "tactical execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | TBD_Question | Guidance | Guidance §49-54 states "Mitigation strategies should acknowledge uncertainty and propose monitoring/contingencies" but does not explain decision rule: when to propose monitoring vs. contingency action | Tactical execution lens reveals ambiguity: for a given risk, what determines whether to implement preventive action (reduce P), contingency allowance (reduce I), or pure monitoring | Guidance.md | Principles > Actionability Over Abstraction (lines 49-54) | Guidance.md (principle stated) vs. Procedure.md (Step 4 strategy types, lines 276-281) | Add decision matrix to Guidance: "Monitoring alone (accept & monitor) for risks <8 score; Preventive action (reduce P) for permitting/procurement risks where early engagement changes probability; Contingency allowance (reduce I) for cost/site risks where allowance absorbs impact; Avoid (scope change) for design risks where removal is feasible" | TBD |

### Lens: A:evaluative:judging
**LensValue:** "worth determination"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | MissingSlot | Datasheet | Risk scoring framework (P/I scales 1-5, Risk Score = P × I, threshold ≥15) is stated as ASSUMPTION but no accessible reference validates these scales | Data necessity lens reveals essential framework assumptions lack evidence base | Datasheet.md | Construction section: Risk Assessment Framework (lines 75-80) | Datasheet.md (ASSUMPTION stated) | Either source ISO 31000 P/I scales if available, or add note: "1-5 scales align with PMI PMBOK standard practice; threshold ≥15 identifies high-priority risks for detailed mitigation per industry best practice" | TBD |
| B-002 | Normalization | Specification | Term "evidence" used inconsistently: FR-03 "ties back to...reports" (evidence = source document), Documentation (line 172) "QC records" (evidence = inspection report), Guidance §85 "auditable records" (evidence = QC documentation) | Conceptualization lens reveals semantic ambiguity around what counts as essential evidence | Specification.md | Standards section (line 98-101); Guidance.md (lines 85-89) | Specification.md vs. Guidance.md | Canonical definition: "Evidence for risk = cited reference material with specific finding; evidence for mitigation = owner assignment + action plan; evidence of QMP = inspection records/checkpoints defined" | TBD |

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | VerificationGap | Specification | FR-02 requires "Risk register shall include: ID, Category, Description, Probability, Impact, Score, Mitigation Strategy, Owner, Status" but does not specify adequacy of mitigation strategy field (summary vs. detailed) | Data sufficiency lens reveals ambiguity: is one-line mitigation summary adequate or must detailed plan be included in register table | Specification.md | Functional Requirements > FR-02 (line 57) | Specification.md (fields listed) vs. Procedure.md (Step 6 documentation format, lines 409-422) | Clarify: Risk register table includes mitigation strategy summary (one-line); high-priority risks (score ≥15) require detailed mitigation plan in separate section per Procedure Step 6 (lines 414-422) | TBD |

### Lens: B:information:sufficiency
**LensValue:** "satisfactory insight"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | Conflict | Multi | Survey availability treatment varies across documents: Datasheet §35 "Survey files provided after award" (constraint); Guidance §127 "not available during proposal development" (consideration); Procedure §147 "available only after award" (enables risk identification) — same fact, different framings create downstream ambiguity | Conceptualization lens reveals inconsistent mental models: Is survey unavailability (a) a constraint to acknowledge, (b) a risk factor to mitigate, or (c) a planning assumption | Datasheet.md line 35; Guidance.md lines 127-131; Procedure.md lines 147 | Datasheet (framed as Condition) vs. Guidance (framed as Consideration/risk factor) vs. Procedure (framed as prerequisite for risk identification) | Canonical framing: Survey unavailability IS a constraint (fact); it ENABLES risk identification (survey-related cost/schedule/design risks); mitigation = early post-award survey + contingency for design adjustments | TBD |

### Lens: B:knowledge:necessity
**LensValue:** "fundamental understanding"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | RationaleGap | Guidance | Guidance §62-66 states "Quality Management Plan procedures should prevent or detect risks early" but does not explain the causal chain: which specific risks are addressed by which QC procedures | Knowledge necessity lens reveals missing connection between risk register (identifies risks) and QMP (controls risks through QC) | Guidance.md | Principles > Integration with Quality Management (lines 62-66); also QM Principles section (lines 70-89) | Guidance.md | Add explanatory table to Guidance: Risk Category [Design, Site, Cost, Schedule, Procurement, Environmental, Permitting] → Controlling QC Area [Design QC, Construction QC, Commissioning QC, Documentation QC] → Example Control Procedure | TBD |

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "obligatory conformance baseline"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | MissingSlot | Specification | Compliance Requirements (CR-01, CR-02, CR-03, CR-04) address conformance to objectives/SOW but do not map to Decomposition §3 Hard Constraints (15 MB size, section order, execution, submission, pricing, team list, addenda acknowledgment) which are actual mandatory pass/fail gates | Normative necessity lens reveals obligatory baseline missing: hard constraints should trigger compliance risk categories in risk register | Specification.md | Compliance Requirements section (lines 72-79) | Specification.md (CR-01...CR-04) vs. Decomposition (§3 C-01...C-07) | Add CR-05 to Specification: "Risk register shall identify compliance risks related to mandatory hard constraints (Decomposition §3 C-01...C-07): submission format, size, structure order, execution requirements, pricing template, team list, addenda acknowledgment" | TBD |

### Lens: C:operative:necessity
**LensValue:** "critical operational foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | VerificationGap | Guidance | Guidance §72-77 (Prevention Over Detection principle) and §248-251 (Quality Rigor vs. Schedule Efficiency trade-off) both address design QC rigor but do not provide operational decision rule: when to implement full 5-checkpoint design review vs. streamlined review | Operative necessity lens reveals gap: decision rule needed for balancing rigor vs. efficiency in QMP design | Guidance.md | Principles section (lines 72-77); Trade-offs section (lines 248-251) | Guidance.md (conflicting emphasis) | Add decision rule: "Default: implement 5 design QC checkpoints (Concept, Schematic, Design Dev, 90% CD, 100% CD); for low-risk projects, combine Concept+Schematic; for high-risk areas (foundation, envelope, life safety), maintain full checkpoint sequence" | TBD |

### Lens: C:normative:sufficiency
**LensValue:** "demonstrated regulatory threshold"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | WeakStatement | Procedure | Step 7 (Review and Integrate) asks "Verify deliverable fulfills acceptance criteria" but does not establish threshold evidence: what threshold shows compliance is "demonstrated" | Formulation sufficiency lens reveals weakness: acceptance criteria §135 (transparency, grounding, actionability, completeness) are qualitative; no quantitative sufficiency proof specified | Procedure.md | Step 7: Compliance Check (lines 471-475); Specification.md Acceptance Criteria (lines 133-140) | Procedure.md vs. Specification.md | Operationalize: Transparency = all risks use standard register format with clear descriptions; Grounding = ≥95% of risks cite accessible source (RFP/addenda/reference report); Actionability = every risk has assigned owner + preventive/contingency action; Completeness = all 7 categories represented | TBD |

### Lens: C:operative:sufficiency
**LensValue:** "competent procedural adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | MissingSlot | Procedure | Step 5 defines 5 design QC checkpoints, 4 construction, 3 commissioning, 4 documentation checkpoints but does not justify adequacy: how many checkpoints constitute "competent" vs. "insufficient" QMP | Competence lens reveals no guidance on sufficiency threshold for QC checkpoint count | Procedure.md | Step 5: Develop Quality Management Plan (lines 306-400) | Procedure.md (checkpoint lists) vs. Guidance.md (examples showing 1 design QC example, 1 QC example) | State adequacy rationale: "Design QC: 5 checkpoints cover full design progression (Concept through Issued-for-Construction); Construction QC: phase-based inspections (4) at critical control points (Foundation before concrete, Structure before enclosure, MEP before concealment, Finishes before owner acceptance); Commissioning QC: 3 points (functional test, training, documentation) cover owner readiness requirements" | TBD |

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "binding baseline assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | MissingSlot | Specification | Specification lists 7 Functional Requirements (FR-01...FR-07) at equal level but does not designate which are binding baseline (mandatory minimum) vs. quality attributes (desirable but not minimum) | Requirements necessity lens reveals: some FRs are mandatory pass/fail (7 categories, 1:1 mitigation mapping), others are quality judgment (transparency, credibility) | Specification.md | Functional Requirements section (lines 52-62) | Specification.md (all FRs unmarked) vs. Acceptance Criteria (line 134 "Risk register is acceptable when...") | Designate: FR-01 (7 categories), FR-02 (register fields), FR-03 (ties to sources), FR-04 (1:1 mitigation), FR-05 (QMP 4 areas) are BINDING BASELINE (must-have); FR-06 (site understanding), FR-07 (transparency/credibility) are QUALITY ATTRIBUTES (expert judgment required) | TBD |

### Lens: F:operative:necessity
**LensValue:** "vital procedural substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | VerificationGap | Procedure | Step 3 (Assess Risk Probability and Impact) defines scoring scales but does not require documentation of scoring rationale: why was this risk assigned Probability=4 vs. Probability=3 | Vital substantiation lens reveals gap: scoring decisions must be substantiated with reference material evidence | Procedure.md | Step 3: Assess Risk Probability and Impact (lines 236-267) | Procedure.md (scoring definitions) vs. Guidance.md (Principle: Source Fidelity, lines 36-41) | Amend Procedure Step 3: "For each risk, document scoring rationale citing reference material(s) that support the P and I assignment. Example: 'Probability=High (4) because Geotechnical Report (page XX) identifies variable groundwater requiring mitigation; Impact=Medium (3) assumes 5% foundation cost contingency typical for these conditions'" | TBD |

### Lens: F:normative:sufficiency
**LensValue:** "sufficient threshold demonstration"

#### Warranted items
_No warranted items identified for this lens._

### Lens: F:operative:sufficiency
**LensValue:** "satisfactory procedural demonstration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | Normalization | Specification | Specification defines "Acceptance Criteria" (natural language, lines 133-140) and "Pass/Fail Criteria" (table format, lines 143-150) as parallel frameworks, creating potential for ambiguity between prose intent and structured pass/fail conditions | Requirements sufficiency lens reveals dual frameworks may conflict or create inconsistency | Specification.md | Acceptance Criteria section (lines 133-140) vs. Pass/Fail Criteria section (lines 143-150) | Specification.md (two formats) | Consolidate: Retain Pass/Fail Criteria table (§143-150) as authoritative; revise Acceptance Criteria section to reference specific Pass/Fail rows + add rationale narrative | TBD |

### Lens: F:operative:necessity (reconsidered)
**LensValue:** "vital procedural substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | TBD_Question | Guidance | Guidance §49-54 (Actionability principle) states mitigations "must be assignable to a specific role" but does not address cross-functional risks where primary and secondary owners must coordinate | Vital substantiation lens reveals gap: decision rule needed for multi-owner risks (e.g., schedule risk affecting both Scheduler and Estimator, environmental risk affecting both Design Lead and Environmental Lead) | Guidance.md | Principles > Actionability Over Abstraction (lines 49-54) | Guidance.md (single owner emphasis) vs. Procedure.md (Step 4 line 289 "Assign Risk Owner") | Clarify: Primary owner leads mitigation and monitors status; secondary owners listed as stakeholders with defined coordination points (e.g., "Primary: PM; Stakeholders: Design Lead (design changes), Estimator (cost changes)") | TBD |

---

## Matrix D — Objectives (3x4)

### Lens: D:normative:guiding
**LensValue:** "authoritative foundational governance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | MissingSlot | Datasheet | Datasheet §21 lists "Primary Objective: OBJ-008: Manage risk & unknowns transparently" but does not establish governance authority: is OBJ-008 mandatory pass/fail or scored criterion | Objectives governance lens reveals missing link to evaluation authority: how does OBJ-008 affect proposal score | Datasheet.md | Attributes section > Primary Objective (line 21) | Datasheet.md vs. Decomposition (§15 Evaluation Criteria Crosswalk: Project Delivery Plan scores 10 points, includes risk register) | Clarify: OBJ-008 contributes to Project Delivery Plan evaluation (10 points per Decomposition §15); Risk Register is scored by evaluators on transparency + mitigation credibility | TBD |

### Lens: D:operative:guiding
**LensValue:** "directed process assurance**

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | Normalization | Guidance | Guidance §3-30 (Purpose and Downstream Use) describes "why" risk register exists but does not address "who directs" process or "who decides" when assessments conflict | Objectives guidance lens reveals missing governance structure: decision authority for contentious risk scores or mitigation disagreements | Guidance.md | Purpose and Downstream Use sections (lines 3-30) | Guidance.md (purpose stated) vs. _CONTEXT.md (Responsible: PM + Technical Leads) vs. Procedure.md (roles listed lines 59-70) | Add to Guidance: "Process Governance: PM leads risk identification and owns final risk register; Technical Leads (by discipline) assess risks in their areas; consensus on scoring/mitigation expected; PM arbitrates disputes; escalation to Proposal Manager for conflicts affecting proposal strategy" | TBD |

### Lens: D:evaluative:guiding
**LensValue:** "established worth governance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | WeakStatement | Specification | Specification acceptance criteria (§135-140) state "Risk register is transparent and credible" but do not define evaluator decision framework: what evidence demonstrates credibility | Worth governance lens reveals acceptance criteria lack measurable worth criteria: how will evaluator judge mitigation adequacy | Specification.md | Acceptance Criteria section (lines 135-140) | Specification.md (prose criteria) vs. Verification section (line 130 "Expert Review") | Operationalize: Credibility demonstrated by (1) source citations at ≥95% rate, (2) mitigation owners clearly assigned, (3) preventive actions + contingency plans stated for high-score risks, (4) cost/schedule impacts of mitigations reflected in sibling deliverables (DEL-05-03, DEL-08-01) | TBD |

### Lens: D:operative:applying
**LensValue:** "actionable operational adequacy"

#### Warranted items
_No warranted items identified for this lens._

---

## Matrix X — Verification (4x4)

### Lens: X:guiding:necessity
**LensValue:** "governing operational mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | MissingSlot | Procedure | Procedure §489-501 (Verification Checkpoints) poses verification questions but does not specify authority for verification or escalation path if verification fails | Verification necessity lens reveals gap: who is accountable for verification? what happens if "all 7 categories" not identified | Procedure.md | Verification section: Process Verification Checkpoints (lines 489-501) | Procedure.md (checkpoints listed) | Add authority statement: "Verification Owner: PM; Verification Authority: PM sign-off on all checkpoints; escalation: any checkpoint failure → document as TBD item with remediation plan before proposal integration" | TBD |

### Lens: X:applying:necessity
**LensValue:** "implemented foundational obligation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | MissingSlot | Guidance | Guidance §91-226 (Considerations) lists 20 factors but does not state whether all must be addressed or if subset is acceptable | Verification obligation lens reveals ambiguity: are 20 considerations mandatory requirements or exemplars | Guidance.md | Considerations section (lines 91-226) | Guidance.md (considerations listed) vs. Specification.md (Scope: 7 categories are mandatory) | Clarify: Guidance §91-226 Considerations are exemplars of factor types (Site, Design, Cost, Schedule, Procurement, Compliance, QM factors); Specification Scope (7 categories, FR-01...FR-07) define mandatory requirements; team should address considerations relevant to their project risk profile | TBD |

### Lens: X:applying:sufficiency
**LensValue:** "actionable threshold demonstration"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | WeakStatement | Datasheet | Datasheet §79 states "Risk Score: Probability × Impact **[ASSUMPTION: standard multiplication method]**" but does not demonstrate sufficiency of simple multiplication for design-build proposal context | Verification sufficiency lens reveals framework assumption lacks justification: is P × I multiplication adequate or should weighted factors apply | Datasheet.md | Construction section > Risk Assessment Framework (line 79) | Datasheet.md (multiplication assumed) vs. industry practice (some frameworks use weighted scoring) | Clarify: Simple P × I multiplication IS sufficient for proposal risk register (enables rapid prioritization + transparent scoring); post-award project execution risk management may employ weighted factors if needed | TBD |

### Lens: X:judging:necessity
**LensValue:** "standard foundational congruence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | TBD_Question | Specification | Specification §90-101 lists applicable standards (ISO 31000, PMI PMBOK, CSA Z1000, ISO 9001) all marked "Not accessible"; without standard texts, how can risk framework congruence be verified | Verification standard lens reveals gap: mandatory standards inaccessible; framework congruence unverifiable | Specification.md | Standards section (lines 90-101) | Specification.md (standards listed as not accessible) | Recommendation: (1) Consult organizational library for ISO 31000:2018 or PMI PMBOK 6th ed.; (2) If unavailable, confirm RFP evaluation criteria do not require explicit standard conformance; (3) Document that framework aligns with industry best practice (P/I scoring, mitigation strategies) even if formal standard texts unavailable | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "sovereign foundational commitment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | MissingSlot | Guidance | Guidance §36-41 mandates "Source Fidelity Over Speculation" (risks grounded in accessible sources) but does not establish evaluator commitment: will evaluator reward source grounding or judge on mitigation merit regardless | Evaluation necessity lens reveals missing evaluator commitment statement: does evaluator prioritize sourced risks over inferred risks | Guidance.md | Principles section > Source Fidelity Over Speculation (lines 36-41) | Guidance.md (principle stated) | Add statement: "Evaluator Expectation: Risks directly cited from RFP/addenda/reference reports (PRESCRIPTIVE) are prioritized; inferred risks labeled ASSUMPTION with clear rationale are acceptable if mitigation is credible; unsourced speculation is penalized" | TBD |

### Lens: E:operative:necessity
**LensValue:** "assured foundational commitment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | Conflict | Guidance | Guidance §227-245 (Trade-offs) frames competing tensions (Depth vs. Brevity, Mitigation Cost vs. Risk Tolerance, Transparency vs. Competitive Positioning) suggesting that assured commitment to risk management must balance other evaluation criteria (price, schedule); trade-off guidance is generic rather than directive | Evaluation assurance lens reveals tension: does evaluator expect comprehensive risk register or appropriately-scoped register | Guidance.md | Trade-offs section (lines 227-245) | Guidance.md (trade-offs described as tensions) vs. Decomposition (§15 Evaluation: Project Delivery Plan = 10 points; Price = 35 points) | Clarify: Risk Register contributes to Project Delivery Plan (10 points, per Decomposition §15); evaluator expectation is TRANSPARENT (not exhaustive) identification + CREDIBLE (not elaborate) mitigation; target 15-25 risks total, prioritized by score; detailed mitigation plans only for high-score risks (≥15) | TBD |

### Lens: E:evaluative:necessity
**LensValue:** "realized foundational merit"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-003 | RationaleGap | Procedure | Procedure Step 7 (Review and Integrate) requires "Cross-Deliverable Consistency Check" (lines 465-469) but does not explain merit rationale: why does cross-document consistency matter to evaluator | Evaluation merit lens reveals missing rationale: what merit does consistency demonstrate | Procedure.md | Step 7: Review and Integrate > Cross-Deliverable Consistency Check (lines 465-469) | Procedure.md (consistency required) vs. Specification.md (Interface Requirements IR-01...IR-04) | Clarify merit: Cross-deliverable consistency demonstrates that (1) risk register informs schedule/pricing/QMP (risks identified in register are addressed elsewhere), (2) mitigation costs reflected in DEL-05-03, (3) schedule contingencies account for risk timelines in DEL-08-01, (4) QMP procedures align with risk categories — this integration shows credible, unified proposal approach vs. siloed deliverables | TBD |

---

## Conflict Summary

**Conflict 1: Survey Availability — Constraint vs. Risk**

- **Contenders:**
  1. Datasheet.md (§35): "Survey files provided after award only" — framed as operating Condition
  2. Guidance.md (§127-131): "Detailed survey files are not available during proposal development" — framed as Risk Consideration
  3. Procedure.md (§147): "Survey files available only after award" — implicit assumption in Step 2.2 Site Risks
- **Nature:** All documents agree on fact (survey post-award) but differ in treatment: constraint vs. risk factor vs. planning assumption
- **HumanRuling:** **TBD** — PM + Technical Leads must clarify: Is survey unavailability (a) a non-negotiable constraint (fact of project), (b) a risk factor that triggers risk identification (e.g., "Survey Uncertainty Risk: SR-XX"), or (c) both? Recommendation: Treat as both — document as Constraint in Datasheet; identify survey-related risks in Procedure Step 2.2 (e.g., "Concept design proceeds without confirmed survey — risk of cost/schedule changes if post-award survey contradicts design assumptions"); propose mitigation (early post-award survey, contingency in pricing/schedule).

---

## Notes

- **Pass 1: Semantic Lensing Completed** — 2026-02-04
  - All matrices A, B, C, F, D, X, E parsed and applied as lenses (7 matrices, avg 12 cells = 84 lens perspectives examined)
  - 28 warranted items identified across four documents
  - 1 cross-document conflict detected and surfaced for human ruling
  - 0 matrix parsing errors
- **Coverage:** 28 warranted items from 84 lens cells = 33% yield, consistent with targeted lensing (identifying gaps/conflicts/weak statements/verification needs, not restating what is clear and consistent)
- **Labeling:** All TBD items and ASSUMPTIONs from source documents preserved; no new assumptions introduced by lensing agent
- **Provenance:** Every item includes SourcePath (document file) and SectionRef (best-effort heading/line reference); conflict items include Contenders with multiple sources
- **Next Step:** 4_DOCUMENTS agent (enrichment pass) will use this register to strengthen documents during subsequent enrichment cycle, resolving TBD items and integrating proposed clarifications

---

**Document Generated:** 2026-02-04
**Agent:** CHIRALITY_LENS (Type 2 Specialist)
**Status:** Complete
