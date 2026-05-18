# Semantic Lensing Register: DEL-05-03 Pricing Narrative and Assumptions

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — DEL-05-03 identity, PKG-02 Financial Proposal, SOW-028 traceability, OBJ-007
- _STATUS.md — Current state SEMANTIC_READY (2026-02-04)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E parsed (7 matrices, 28 cells total)
- Datasheet.md — Identification, attributes, conditions, construction, references
- Specification.md — Requirements R-1 through R-10, scope boundaries, verification methods, standards
- Guidance.md — Purpose, principles 1-5, considerations 1-5, trade-offs 1-3, examples 1-4, conflict table
- Procedure.md — Steps 1-8 production workflow, prerequisites, verification checkpoints, records
- _REFERENCES.md — RFP 2024_004, Addenda 01-03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- **Total warranted items:** 18
- **By document:**
  - Datasheet: 3
  - Specification: 5
  - Guidance: 4
  - Procedure: 4
  - Multi: 2
- **By matrix:**
  - A: 3  B: 3  C: 2  F: 2  D: 3  X: 3  E: 2
- **Notable conflicts:** 1 (FF&E treatment scope boundary between Specification and Datasheet)
- **Matrix parse errors:** 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:applying
**LensValue:** "binding pricing basis"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | TBD_Question | Datasheet | Key Narrative Elements lists six TBD items: "Detailed allowance values and justifications," "Market pricing date," "Labor and material availability assumptions," "Site logistics and access assumptions," "Procurement lead time assumptions," "Contingency approach and magnitude." | Without these essential facts, binding pricing basis is a scaffold only. These must be populated by estimator before enrichment can conclude. | Datasheet.md | Construction > Key Narrative Elements (TBD section) | — | Estimator / Commercial Lead supplies: 1) Site servicing allowance value (per Addendum 03), 2) Market pricing date, 3) Labor/material availability basis, 4) Site access assumptions, 5) Long-lead procurement items and timelines, 6) Contingency percentage and rationale. | TBD |
| A-002 | VerificationGap | Specification | R-1 (Addenda acknowledgement) requires narrative to "explicitly acknowledge" addenda and "summarize impacts," but verification method only states "Document review" + pass/fail gate. Acceptance criteria not defined: must all three addenda be named? must pricing impacts be quantified or can they be stated as TBD? | Mandatory compliance (risk of disqualification per C-07) requires testable pass/fail threshold. Current verification is procedural, not criterial. | Specification.md | R-1: "Addenda Integration and Acknowledgement" | — | Define R-1 acceptance criteria: "Three addenda (01, 02, 03) explicitly named; Addendum 03 impacts documented (site area 12-acre basis, pickled sand building excluded, FF&E treatment clarified, technical requirements listed, allowance approach stated); all statements traceable to addendum text or Decomposition §4." | TBD |
| A-003 | Normalization | Multi | Datasheet Content Structure (Section 1 Introduction through Section 8 Pricing Assumptions) and Procedure Step 3 (sub-steps 3.1 through 3.8) describe same 8-section narrative structure but with slightly different naming conventions and ordering emphasis. | Two representations risk implementation divergence. Procedure author may follow different structure than Datasheet architecture intended. Canonical structure needed. | Datasheet.md | Construction > Content Structure | Procedure.md | Steps > Step 3 (all sub-steps) | Adopt Datasheet content structure as authoritative and canon. Update Procedure Step 3 preamble to state: "Use Content Structure from Datasheet.md, Sections 1–8, as definitive narrative organization." | TBD |

### Lens: A:operative:applying
**LensValue:** "cost assembly execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | WeakStatement | Procedure | Procedure Steps 3.1–3.8 describe narrative drafting but not the actual cost assembly execution (how estimate is built, what cost databases/market data feed Schedule A/B). Step 3 uses existing schedules as reference but does not address: if schedules are not finalized, how does estimator draft narrative without knowing final numbers? | Procedure assumes Schedule A/B exist and are stable when narrative drafting begins, but Prerequisite Dependencies show Schedule A/B status as "Draft or in progress." This creates a chicken-egg dependency that is not resolved. | Procedure.md | Prerequisites > Dependencies | Step 3 > Cross-reference to Schedules | Clarify dependency handling: (1) If Schedules A/B are NOT available at Step 3 start, draft narrative with TBD placeholders and defer Step 4 cross-reference to when schedules are finalized. (2) Create a gating rule: Procedure Step 2 prerequisite check must confirm Schedule A/B status before proceeding. | TBD |

### Lens: A:evaluative:judging
**LensValue:** "defensibility of assumptions"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | WeakStatement | Guidance | Guidance Principle 1 (Source Fidelity Over Optimism) states "Every pricing assumption should be traceable to a source" and "If an assumption is based on judgment, label it explicitly." However, "explicitly labeled" is vague. What is the labeling standard/marker format? | Defensibility of assumptions requires clear, consistent labeling so evaluators can distinguish facts from judgments. Current guidance provides principle but not implementation standard. | Guidance.md | Principles > Principle 1 (Application subsection) | — | Propose standard labeling: Use prefix "[FACT: source]" or "[ASSUMPTION: judgment/rationale]" (e.g., "[FACT: Geotech Report Section 4.2 indicates rock at 3m+]" vs. "[ASSUMPTION: Labor availability per regional construction union data, pending validation]"). Define this standard in Guidance or Specification. | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | TBD_Question | Datasheet | Datasheet Attributes lists "Evaluation Weight: Part of 35-point Proposal Price category" but does not clarify: does pricing narrative have a separate sub-score within the 35 points, or is it evaluated holistically with Schedules A/B as a single price package? Is narrative quality independently scored? | Essential fact needed to understand evaluator expectations for narrative completeness and rigor. If narrative is scored separately from schedules, level of detail and defensibility required may differ. | Datasheet.md | Attributes > Evaluation Weight | RFP 2024_004 | Evaluation criteria section | Verify RFP evaluation rubric: Does it score "Price" as 35 points total (undifferentiated between narrative and schedules), or is there a sub-rubric (e.g., Schedules 20 pts, Narrative 15 pts)? | TBD |
| B-002 | MissingSlot | Specification | No requirement mandates identification of what evidence is available vs. unavailable for pricing (e.g., vendor quotes obtained? geotechnical data status? subcontractor pricing firm?). Adequacy of evidence depends on what data estimator actually possesses. | Datasheet should record data availability status to establish evidence baseline. Currently, narrative assumes evidence exists but does not inventory it. | Specification.md | Requirements > R-7 (Pricing Assumptions Transparency) | — | Add to Specification R-7: "Evidence inventory: Document which pricing assumptions are based on firm evidence (vendor quotes, site reports, standards) vs. preliminary estimates vs. professional judgment. For each major cost category (general requirements, building, sitework, options), state evidence availability status." | TBD |
| B-003 | RationaleGap | Guidance | Guidance Consideration 2 (Market Conditions and Escalation) addresses escalation assumptions but notes "RFP contract terms (location TBD)" — i.e., whether contract is fixed-price, GMP, or cost-plus. Contract type fundamentally shapes how assumptions and allowances should be framed. Without this, guidance is incomplete. | RFP contract terms are essential context for framing pricing assumptions. Without knowing if escalation is fixed or adjustable, assumption strategy is undefined. | Guidance.md | Considerations > Consideration 2 under Caution | RFP 2024_004 | Contract terms section (location TBD) | Resolve: Verify RFP contract type. If fixed-price, escalation must be built into base price. If GMP or cost-plus, escalation may be handled through adjustment clauses. Update Guidance Consideration 2 accordingly. | TBD |

### Lens: B:information:sufficiency
**LensValue:** "satisfactory explanation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | WeakStatement | Specification | R-5 (Additional Options 1–6 pricing basis) requires narrative to "explain the pricing basis" but Detail section states "TBD — specific scope descriptions and pricing assumptions for each option require estimator input." No interim framework provided; requirement is fully deferred. | Satisfactory explanation requires at minimum a structured template for each of the six options. Current state is a blank check to estimator with no guidance on what constitutes sufficient explanation. | Specification.md | R-5 and Detail note | — | Create in Specification or Guidance: Template for each Additional Option with required fields: [Option Name] | [Scope description] | [Basis (market quote? estimate? allowance?)] | [Contingency/margin] | [Monitoring fee separation, if applicable]. Use template as scaffolding for estimator. | TBD |
| B-005 | Normalization | Guidance | Guidance has 5 Principles, 5 Considerations, and 3 Trade-offs that sometimes overlap in scope (e.g., Principle 3 "Allowances are Transparency Tools" and Trade-off 3 "Allowances (Flexibility) vs. Fixed Pricing (Certainty)" address the same topic; Principle 4 "Exclusions Must Be Explicit" and Consideration 5 "Consistency with Design Concept" both address clarity but from different angles). | Overlapping content may confuse which guidance applies to which decision. Principles, Considerations, and Trade-offs should have demarcated scopes to reduce ambiguity. | Guidance.md | Principles; Considerations; Trade-offs sections | — | Add a preamble to Guidance explaining scope demarcation: Principles = normative direction (must apply), Considerations = contextual factors (may apply), Trade-offs = competing concerns requiring judgment (balance case-by-case). Reorganize so content does not repeat across sections. | TBD |

### Lens: B:knowledge:consistency
**LensValue:** "stable reasoning"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-006 | RationaleGap | Guidance | Guidance Principle 1 (Source Fidelity Over Optimism) and Trade-off 2 (Conservative Assumptions vs. Competitive Pricing) both address the tension between conservative/transparent vs. aggressive/optimistic pricing, but use different vocabulary and frameworks. Principle 1 frames it as "fidelity over optimism"; Trade-off 2 frames it as "conservative vs. aggressive." | Stable reasoning requires a single, consistent framing of this key tension. Current guidance presents two perspectives that may create conflicting guidance if an estimator defaults to different principles. | Guidance.md | Principle 1 (Application) vs. Trade-off 2 (Guidance section) | — | Consolidate into a single, authoritative statement: "Conservatism principle: When in doubt, state conservative assumptions and identify them as risks in the risk register. Transparency enables evaluators to assess risk. Aggressive assumptions must be explicitly marked as such and justified by market data or project experience." Place this in Principle 1 and cross-reference from Trade-off 2. | TBD |

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:completeness
**LensValue:** "exhaustive scope boundary mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | Conflict | Multi | Specification R-4 (FF&E Treatment) states FF&E "may be included as an additional item, **not** in base cost" per Addendum 03. Status note says "OI-004 remains open — estimator must decide scope and pricing treatment." However, Datasheet Conditions lists "FF&E may be included as an additional item, **not** in base cost" as mandatory. Two documents frame this differently: one as an open decision (Specification), one as a fixed mandate (Datasheet). | Scope boundary for FF&E is ambiguous. Until OI-004 is closed, the narrative author will not know whether to include an FF&E section or exclude it entirely. This creates delivery risk. | Specification.md | R-4 status note and Datasheet.md | Conditions > FF&E Treatment | Specification.md#R-4; Datasheet.md#Conditions | Close OI-004 immediately: Estimator/PM decision required. Option A: FF&E priced as separate Schedule A line item (specify scope). Option B: FF&E excluded with rationale. Option C: FF&E included in base cost (justify deviation from Addendum 03). Once decided, update both Specification R-4 and Datasheet Conditions to be consistent. | TBD |

### Lens: C:operative:sufficiency
**LensValue:** "sufficient operational pricing capacity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | MissingSlot | Procedure | Prerequisites > Tools and Templates lists generic tools (word processor, cross-reference log, addenda checklist) but does not address whether estimator has sufficient operational capacity (access to cost databases, vendor quote systems, subcontractor pricing networks, RS Means or similar rate sources). | Sufficient operational pricing capacity is prerequisite to credible cost assembly but is not checked in Procedure. If estimator lacks access to market data tools, pricing will be speculative. Procedure should acknowledge or verify this prerequisite. | Procedure.md | Prerequisites > Tools and Templates section | — | Add prerequisite check: "Estimator has access to: (1) RS Means or equivalent cost database, (2) Recent competitive quotes for major building systems (HVAC, structural, electrical), (3) Subcontractor pricing network for local Alberta market, (4) Labor rate source (union or non-union, regional average)." If not available, note as constraint and estimate accordingly. | TBD |

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "irreducible obligation governing cost disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | TBD_Question | Specification | R-1 cites C-07 (Decomposition §3) as the disqualification risk for missing addenda acknowledgement. However, Specification notes "Specific RFP section references require validation against source PDF (location TBD pending access)." Until RFP §2.9 and C-07 are validated, the irreducible obligation is not fully confirmed from primary source. | Irreducible obligation should be grounded in RFP text, not decomposition interpretation. Source validation is needed. | Specification.md | Requirements > R-1; Standards > Note | RFP 2024_004 | §2.9 | Validate: Does RFP §2.9 or contract terms explicitly state that failure to acknowledge addenda disqualifies the proposal? If yes, R-1 is irreducible. If no, reframe R-1 as best practice. | TBD |
| F-002 | VerificationGap | Specification | Verification Responsibility table shows "Final QA: **TBD** (proposal review process owner)." This leaves unassigned the ultimate authority for verifying that narrative achieves cost disclosure fidelity per RFP and evaluation criteria. Without named accountability, final verification may not occur. | An irreducible obligation requires that someone, with authority, is accountable for verification. TBD means no one currently owns this. | Specification.md | Verification > Verification Responsibility | — | Assign Final QA: Identify and name the final QA authority (suggest: Proposal Manager or Commercial Director). This person is accountable for sign-off that narrative meets RFP requirements and evaluation criteria before submission. | TBD |

---

## Matrix D — Objectives (3x4)

### Lens: D:normative:guiding
**LensValue:** "resolved authoritative direction for cost disclosure obligations"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | WeakStatement | Specification | Multiple requirements (R-7, R-8, R-9) are sourced as "ASSUMPTION based on standard estimating practice" or "ASSUMPTION based on standard proposal quality requirements." Authoritative direction requires confirmed RFP clauses, not assumptions about standard practice. Until RFP is validated, these requirements are provisional. | Resolved authoritative direction requires grounding in RFP source authority, not assumptions. Current approach is scaffolding that assumes RFP alignment but does not verify it. | Specification.md | Requirements > R-7, R-8, R-9 (Source citations) | RFP 2024_004 | Relevant evaluation/submission sections | Validate RFP source for each ASSUMPTION-sourced requirement. If RFP clause does not exist, reframe as "best practice recommendation" rather than "requirement." Mark confidence level for each source citation. | TBD |

### Lens: D:operative:judging
**LensValue:** "adjudicated variance resolution ensuring workflow completeness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | MissingSlot | Procedure | Procedure Step 4 states "If narrative states an allowance but Schedule B does not include it → add to Schedule B or revise narrative." However, the procedure does not specify who decides and what authority they have: Does Estimator decide unilaterally? Does Proposal Manager have veto? What if Schedule B is owned by a different team member? | Variance adjudication requires clear decision authority and escalation path. Without it, discrepancies could remain unresolved or create conflicting changes to Schedules A/B. | Procedure.md | Steps > Step 4: "Action" section (resolution instructions) | — | Clarify authority: Estimator proposes resolution; Proposal Manager adjudicates (has final authority over narrative-vs-schedules conflicts). If resolution requires design change (e.g., allowance scope affects concept), escalate to PKG-04 lead for input. Document decision in cross-reference log. | TBD |

### Lens: D:evaluative:judging
**LensValue:** "adjudicated assumption defensibility ensuring holistic coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | VerificationGap | Specification | Specification verification table checks individual requirements (R-1 through R-10) but does not include a "holistic assumption defensibility" check: Do the assumptions collectively form a coherent, defensible, and internally consistent cost picture? Evaluators will assess not just individual requirements but overall narrative credibility. | Holistic coverage requires system-level verification beyond item-by-item checks. Procedure Step 7 mentions "credibility" review but without defined criteria. | Specification.md | Verification > Verification Methods section | — | Add verification checkpoint for Step 7 (Final Review): "Holistic coherence test: Does the narrative tell a coherent story about cost drivers, assumptions, and trade-offs? Are contradictions between sections identified and resolved? Does narrative support the price in Schedules A/B?" Define "coherence" rubric or examples. | TBD |

---

## Matrix X — Verification (4x4)

### Lens: X:applying:necessity
**LensValue:** "essential enactment prerequisite for pricing substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | VerificationGap | Procedure | Procedure Step 5 requires cross-check against "Concept design (DEL-02-01)," "Construction methodology (DEL-04-01)," "Schedule (DEL-08-01)," and other deliverables. However, prerequisite check does not confirm these deliverables are available. If they are not ready, Step 5 blocks. Current guidance says "if dependencies not met, defer Step 5" but this is vague about timing and handoff. | Essential enactment prerequisite verification should confirm inputs are available and specify what to do if they are not. Current Step 5 instruction creates potential scheduling bottleneck without mitigation. | Procedure.md | Steps > Step 5 opening; Prerequisites | — | Clarify: (1) Step 5 can proceed with draft/preliminary versions of related deliverables. (2) If related deliverables unavailable, document assumption ("pricing assumes X per preliminary concept") and flag for validation in enrichment Phase 2. (3) Define trigger for deferral: if deliverable not available by end of Step 3, defer Step 5 to enrichment pass. | TBD |
| X-002 | TBD_Question | Procedure | Procedure Step 1 says "Confirm access to Addenda 01, 02, 03 and site due diligence reports in _Sources/" but verification checkpoint only checks "accessible" not "accessed and reviewed." Is prerequisite complete when documents are merely available, or must evidence exist that they were read? | Prerequisite verification should confirm actual use, not just availability. If documents are accessible but not read, pricing assumptions may lack grounding. | Procedure.md | Steps > Step 1; Verification > Process Verification Checkpoints | — | Add verification: "Estimator confirms: (1) Addenda 01-03 read and impacts noted in working summary, (2) Geotechnical and site reports reviewed for assumptions relevant to pricing. Evidence: dated notes or checkmarks in access log." | TBD |
| X-003 | MissingSlot | Procedure | Procedure does not include bidirectional cross-check: (1) Narrative items missing from Schedules A/B (which Step 4 covers), OR (2) Schedule line items missing from narrative (reverse direction). Only unidirectional check is performed. | Exhaustive implementation coverage requires checking both directions to ensure no cost category is orphaned from narrative explanation. | Procedure.md | Steps > Step 4 | — | Add to Step 4 verification: "(1) Forward check: narrative items all appear in Schedule B (current procedure). (2) Reverse check: Schedule B line items all addressed in narrative or explicitly excluded with rationale. Flag any orphaned schedule items that lack narrative justification." | TBD |

### Lens: X:judging:sufficiency
**LensValue:** "adequate adjudicative standard for assumption substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | WeakStatement | Specification | R-7 verification method states "Document review + cross-check to schedule/due diligence" but does not define adjudicative standard for judging assumption quality (e.g., must each assumption cite a source? must ranges be provided for uncertain values? what is acceptable margin of error for estimates?). | Adequate adjudicative standard requires defined criteria for evaluator to assess assumption defensibility. Current verification is procedural, not criterial. | Specification.md | R-7 under Verification Methods | — | Define standard: "Each assumption must state: (1) Value or range, (2) Source (quote, report, standard, or professional judgment), (3) Confidence level (firm/preliminary/estimated), (4) If uncertain, adjustment trigger (what post-award information will finalize?)." Assess against these four criteria. | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "irreducible authoritative imperative governing cost disclosure fidelity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | TBD_Question | Specification | The irreducible authoritative imperative depends on RFP evaluation structure: Is pricing narrative scored as a sub-category of the 35-point "Price" category, or is it only a compliance support document? If sub-scored, disclosure fidelity is irreducible; if support-only, it may be advisory. R-1 cites disqualification risk (irreducible weight) but R-7–R-10 are ASSUMPTIONS. | Until RFP evaluation rubric is validated, the true normative weight and imperative level of the narrative is uncertain. This affects how rigorously fidelity must be achieved. | Specification.md | Requirements > R-1, R-7–R-10 | RFP 2024_004 | Evaluation criteria section | Verify: Does RFP separately score narrative quality (and if so, how many points)? Or is narrative evaluated holistically with schedules as single 35-point package? Update Specification imperative language accordingly (must vs. should). | TBD |

### Lens: E:evaluative:sufficiency
**LensValue:** "demonstrably sufficient value justification across all assessment domains"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | MissingSlot | Guidance | Guidance Examples 1–4 provide illustrative scaffolds for addenda acknowledgement, allowances, exclusions, and value alternatives. However, no example demonstrates sufficient value justification for the most complex section: R-7 (Pricing Assumptions Transparency). The assumptions section lacks demonstrated standard for what constitutes "sufficiently justified" pricing. | Missing example for assumptions section means the sufficiency bar for this critical section is not demonstrated to the drafting author. Estimator may under-justify or over-justify without clear guidance. | Guidance.md | Examples section (Examples 1–4) | — | Add Example 5: "Pricing Assumptions (R-7) — Market Conditions and Escalation" showing: (1) Pricing date stated, (2) Escalation rate justified by reference, (3) Labor assumption sourced to regional data, (4) Contingency magnitude stated with rationale. Format as table with Value | Source | Confidence | Adjustment Trigger. | TBD |

---

## Notable Observations

### Dominant Pattern: TBD and Open Decisions
- **8 items flagged as TBD** requiring estimator input (allowance values, market conditions, FF&E scope decision, labor/material assumptions, site logistics, procurement lead times, contingency approach)
- **2 items flagged as OI (open issue):** OI-004 (FF&E treatment) and implicit gaps in RFP source validation
- **Estimator has clear path to resolution** but timeline and coordination dependencies are not fully resolved

### Dominant Pattern: RFP Source Validation Needed
- **Multiple requirements** sourced as "ASSUMPTION based on standard practice" rather than validated against RFP text
- **RFP section references** marked "location TBD" indicating RFP has not been systematically analyzed for relevant clauses
- **Validation of these sources** is essential before narrative production can be fully confident in requirements

### Dominant Pattern: Process Clarity Needed
- **Variance adjudication:** Who decides when narrative and Schedules A/B conflict? (A-004, D-002)
- **Dependency handling:** What happens when prerequisite deliverables (DEL-02-01, DEL-04-01, DEL-08-01) are not ready? (X-001)
- **Final authority:** Who is the Final QA authority? (F-002)
- **Holistic verification:** How is overall narrative coherence assessed? (D-003)

### No Severe Conflicts Detected
- **1 conflict identified:** FF&E treatment scope boundary (C-001) — Specification and Datasheet frame it differently, but this is resolvable by closing OI-004
- **No document contradictions:** Datasheet, Specification, Guidance, and Procedure are internally consistent; gaps are mostly incompleteness, not contradiction

### Readiness for Enrichment
**Status: READY WITH CAVEATS**

The four documents form a coherent framework for producing DEL-05-03. The SEMANTIC_LENSING register identifies 18 warranted items that should be addressed during the 4_DOCUMENTS enrichment pass:

1. **Estimator inputs** (8 items) — Populate TBD values for allowances, market conditions, contingency, site logistics, procurement timelines
2. **Decision closure** (1 item, OI-004) — Decide FF&E treatment (priced separately, excluded, or in base)
3. **RFP source validation** (3 items) — Confirm RFP clauses support ASSUMPTION-sourced requirements
4. **Process clarification** (4 items) — Clarify decision authority, dependency handling, final QA role, holistic verification approach
5. **Standards definition** (2 items) — Define acceptance criteria for compliance threshold (A-002), assumption labeling format (A-005)

---

## Enrichment Recommendations

1. **Immediate actions (before enrichment):**
   - Close OI-004 (FF&E scope decision)
   - Validate RFP sections for cost disclosure obligations (R-1 through R-10 sources)
   - Name Final QA authority for Specification Verification Responsibility

2. **During enrichment pass:**
   - Estimator populates TBD values in Datasheet Key Narrative Elements
   - Procedure Step 2 updated with prerequisite dependency gating rules
   - Standards added to Specification: compliance threshold criteria (R-1), assumption labeling format (proposed in A-005)
   - Guidance Example 5 added for Pricing Assumptions section (R-7)
   - Procedure Step 5 updated with guidance on handling unavailable related deliverables

3. **Cross-reference validation:**
   - Step 4 (narrative vs. Schedules A/B) performed with bidirectional checking (forward + reverse)
   - Step 5 (cross-deliverable consistency) deferred to Phase 2 if upstream deliverables not ready

---

**Lensing register completed. Ready for 4_DOCUMENTS enrichment pass.**
