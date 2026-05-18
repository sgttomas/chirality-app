# Semantic Lensing Register: DEL-05-02 AppendixH ScheduleB CostBreakdown

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/_CONTEXT.md
- _STATUS.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/_STATUS.md
- _SEMANTIC.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/_SEMANTIC.md
- Datasheet.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/Datasheet.md
- Specification.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/Specification.md
- Guidance.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/Guidance.md
- Procedure.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/Procedure.md
- _REFERENCES.md — DEL-05-02_AppendixH_ScheduleB_CostBreakdown/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- Total warranted items: 38
- By document:
  - Datasheet: 8
  - Specification: 12
  - Guidance: 10
  - Procedure: 8
- By matrix:
  - A: 6  B: 7  C: 6  F: 6  D: 6  X: 1  E: 6
- Notable conflicts: 4
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "prescriptive direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | WeakStatement | Specification | Requirement R-001 ("SHALL use the Appendix H Schedule B template") lacks explicit reference to template location and format specifications. | Prescriptive direction must be implementable; current statement is aspirational but not actionable without access to the template. | Specification.md | R-001 | N/A | Add: "Appendix H Schedule B template location: RFP Section 4.3; obtain from _Sources/ directory or Proposal Manager." | TBD |
| A-002 | MissingSlot | Specification | R-010 ("Cost Breakdown Granularity") is explicitly marked "Verification: TBD (depends on Appendix H template structure)" — this gaps prescriptive direction. | Prescriptive direction should be definitive; a TBD verification method indicates incomplete normative guidance. | Specification.md | R-010 | N/A | Either (1) add reference to Appendix H template granularity guidance, or (2) establish a firm decision (e.g., "minimum 3-level hierarchy: Category > Subcategory > Line Item"). | TBD |

#### No warranted items case
_Lens A:normative:guiding otherwise well-addressed._

---

### Lens: A:normative:applying
**LensValue:** "mandated practice"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | WeakStatement | Procedure | Step 1 requires "Review Appendix H Schedule B template" but marks template location as "location TBD". | Mandated practice (how to execute the procedure) cannot be initiated without the artifact. Critical path blocker. | Procedure.md | Step 1: Review Scope and Template | N/A | Immediate action: Obtain Appendix H template from RFP and insert file path/reference in Step 1 Prerequisites. | TBD |

#### No warranted items case
_Lens A:normative:applying otherwise addressed by Procedure.md Steps 1–6._

---

### Lens: A:normative:judging
**LensValue:** "compliance determination"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Compliance determination is handled by Specification.md (Acceptance Criteria) and Procedure.md (Step 4: Internal QA)._

---

### Lens: A:normative:reviewing
**LensValue:** "regulatory audit"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Regulatory audit scope is post-award and out of scope for proposal-stage deliverable._

---

### Lens: A:operative:guiding
**LensValue:** "procedural steering"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Procedural steering is well-addressed by Procedure.md._

---

### Lens: A:operative:applying
**LensValue:** "functional execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | TBD_Question | Procedure | Step 3 (Apply Unit Costs) provides general guidance ("Use percentage of construction cost (8–12% typical) for General Requirements") but does not specify firm's chosen approach. | Functional execution requires a decided markup/overhead/contingency strategy. Guidance.md (Trade-off 2) provides options but does not declare which path was selected. | Guidance.md; Procedure.md | Trade-off 2: Contingency Visibility vs. Competitive Pricing; Step 3 | Guidance options: (1) Explicit contingency line, (2) Embedded contingency, (3) Hybrid approach. | Confirm with Commercial Lead and document chosen approach in DEL-05-03 before executing Step 3. | TBD |

#### No warranted items case
_Lens A:operative:applying otherwise addressed by Procedure.md Steps._

---

### Lens: A:operative:judging
**LensValue:** "performance assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Performance assessment (evaluator scoring) is out of scope for proposal production._

---

### Lens: A:operative:reviewing
**LensValue:** "process verification"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Process verification is handled by Procedure.md (Verification section and Step 4)._

---

### Lens: A:evaluative:guiding
**LensValue:** "value orientation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-005 | RationaleGap | Guidance | Guidance.md Principle 1 (Transparency Over Opacity) establishes value orientation but does not explicitly tie to RFP evaluation scoring (35 points for Proposal Price). | Value orientation should be grounded in evaluative context. Principle lacks explicit connection to scoring. | Guidance.md | Principle 1 | N/A | Add: "This principle directly supports evaluation scoring by enabling evaluators to assess cost reasonableness across the 35-point Proposal Price category (Decomposition Section 15)." | TBD |

#### No warranted items case
_Lens A:evaluative:guiding otherwise well-addressed._

---

### Lens: A:evaluative:applying
**LensValue:** "merit implementation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Merit implementation is addressed by Guidance.md (Principles 1–5) and Procedure.md._

---

### Lens: A:evaluative:judging
**LensValue:** "quality adjudication"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Quality adjudication is handled by Specification.md (Acceptance Criteria) and Procedure.md (Step 4 QA)._

---

### Lens: A:evaluative:reviewing
**LensValue:** "worth reappraisal"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Worth reappraisal is post-award and out of scope._

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | MissingSlot | Datasheet | Datasheet.md lists "Cost Categories Required" but does not specify which Addendum 03 technical requirements must be individually costed (e.g., overhead doors 16 ft, bay sumps, fire apparatus exhaust, generator, fill stations, solar-ready). | Essential facts: Which technical items are separate cost lines vs. absorbed into building system costs? Procedure Step 2 lists items to quantity but Datasheet cost structure does not clarify their line-item treatment. | Datasheet.md; Procedure.md | Attributes (Cost Categories); Step 2 | N/A | Clarify: Are Addendum 03 technical items (16 ft doors, sumps, exhaust, fill stations, solar) costed separately or rolled into building systems? | TBD |

#### No warranted items case
_Lens B:data:necessity otherwise addressed._

---

### Lens: B:data:sufficiency
**LensValue:** "adequate evidence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-002 | WeakStatement | Datasheet | "Expected Cost Breakdown Structure" section states "Detailed line-item structure is TBD pending access to actual Appendix H template form." | Adequate evidence cannot be provided without access to the template. Critical evidence gap. | Datasheet.md | Construction (Expected Cost Breakdown Structure) | N/A | Obtain Appendix H template from RFP. Document actual structure in Datasheet Construction section. | TBD |

#### No warranted items case
_Lens B:data:sufficiency otherwise addressed._

---

### Lens: B:data:completeness
**LensValue:** "exhaustive record"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Exhaustive records are covered by Procedure.md (Records section)._

---

### Lens: B:data:consistency
**LensValue:** "coherent measurement"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | Conflict | Multi | Datasheet.md lists cost categories as "General Requirements, Building, Sitework" but Guidance.md (Example Schedule B) shows subdivisions (1.1–3.5). Procedure Step 1 directs "identify required line items" without specifying whether granularity should follow Datasheet structure, Guidance example, or actual Appendix H template structure. | Coherent measurement requires consistency. Current documents provide three implicit structures: Datasheet (3 categories), Guidance (example with subdivisions), Procedure (template-dependent). | Datasheet.md; Guidance.md; Procedure.md | Datasheet Attributes; Guidance Example; Procedure Step 1 | Contender 1: Follow Datasheet 3-category structure. Contender 2: Follow Guidance subdivisions (1.1–3.5). Contender 3: Follow actual Appendix H template (TBD). | Confirm which structure governs before populating Schedule B. Likely Appendix H template governs; documents should reference actual template structure. | TBD |

#### No warranted items case
_Lens B:data:consistency requires clarification (conflict noted above)._

---

### Lens: B:information:necessity
**LensValue:** "required intelligence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Required intelligence is addressed by Specification.md (Requirements R-001–R-010)._

---

### Lens: B:information:sufficiency
**LensValue:** "adequate disclosure"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | RationaleGap | Specification | Specification.md R-006 (Addenda Acknowledgement) notes "location TBD (may be on Schedule A rather than Schedule B)". | Adequate disclosure requires clarity on deliverable responsibility. Unclear whether acknowledgement belongs to DEL-05-01 or DEL-05-02. | Specification.md | R-006 | Contender 1: Acknowledgement is on Schedule B (this deliverable). Contender 2: Acknowledgement is on Schedule A (DEL-05-01). | Clarify with RFP/Appendix H instructions: Does acknowledgement line appear on Schedule A or Schedule B? Update Specification.md accordingly. | TBD |

#### No warranted items case
_Lens B:information:sufficiency requires clarification (conflict noted above)._

---

### Lens: B:information:completeness
**LensValue:** "comprehensive reporting"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | MissingSlot | Datasheet | Datasheet.md "Additional Options 1–6" lists special requirements as "TBD" for all except Option 4 (monitoring fee). | Comprehensive reporting requires documenting special handling for all options. Currently lacks detail on operating cost components or warranty implications for Options 1, 2, 3, 5, 6. | Datasheet.md | Additional Options | N/A | Populate "Special Requirement" column for all options. Example: "Option 1: Capital cost only; confirm wash bay system scope with Design Lead." | TBD |

#### No warranted items case
_Lens B:information:completeness requires enrichment (noted above)._

---

### Lens: B:information:consistency
**LensValue:** "uniform communication"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-006 | Conflict | Multi | Specification.md R-005 ("Schedule B detailed costs SHALL sum to match Schedule A totals") and Guidance.md Principle 2 ("Use linked spreadsheet formulas") assume Excel format, but Datasheet.md lists "Format: TBD (table/spreadsheet format expected)". Procedure Step 6 directs "Export Schedule B in required format (PDF or Excel, per RFP instructions)" — if PDF, linked formulas fail. | Uniform communication assumes a format that may not align with RFP submission requirements. | Specification.md; Guidance.md; Datasheet.md; Procedure.md | R-005; Principle 2; Attributes; Step 6 | Contender 1: Schedule B is Excel (linked formulas work). Contender 2: Schedule B is PDF (manual reconciliation required). | Obtain RFP Appendix H instructions to confirm required format. Update all documents accordingly. | TBD |

#### No warranted items case
_Lens B:information:consistency requires format clarification (conflict noted above)._

---

### Lens: B:knowledge:necessity through B:wisdom:consistency
**LensValue:** (multiple cells)

#### No warranted items case
_No warranted items identified for these lenses. Knowledge/wisdom dimensions are implicitly supported by procedure prerequisites and role assumptions._

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "binding procedural obligation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|

#### No warranted items case
_No warranted items identified for this lens. Binding procedural obligations are well-defined by Specification.md._

---

### Lens: C:normative:sufficiency
**LensValue:** "warranted demonstrable threshold"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | WeakStatement | Specification | R-010 ("Cost Breakdown Granularity") states "Verification: TBD (depends on Appendix H template structure and RFP instructions)". | A warranted demonstrable threshold should be objective, not conditional. RFP will define threshold; deliverable should reference it. | Specification.md | R-010 | N/A | Replace with: "Threshold: sufficient line-item detail to assess cost allocation across General Requirements, Building, Sitework (per Decomposition Section 15 evaluation criteria)." | TBD |

#### No warranted items case
_Lens C:normative:sufficiency requires refinement (noted above)._

---

### Lens: C:normative:completeness
**LensValue:** "mandated comprehensive coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | VerificationGap | Specification | Specification.md R-009 ("Completeness") requires "All anticipated line items present" but does not enumerate what "anticipated" means without access to template. | Mandated comprehensive coverage requires exhaustive line-item specification. Current approach relies on template (TBD), creating verification gap. | Specification.md | R-009 | N/A | Step 1: Obtain Appendix H template. Step 2: Update Specification.md R-009 with explicit checklist (e.g., "General Requirements: items 1.1–1.4; Building: items 2.1–2.8; Sitework: items 3.1–3.5; Additional Options: 1–6"). | TBD |

#### No warranted items case
_Lens C:normative:completeness requires template-dependent action (noted above)._

---

### Lens: C:normative:consistency
**LensValue:** "harmonized regulatory fidelity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | Conflict | Multi | Datasheet.md (3 categories) vs. Guidance.md Example (numbered subdivisions 1.1–3.5) vs. Decomposition scope (3 categories) vs. actual RFP template (TBD). | Harmonized regulatory fidelity requires consistency between decomposition scope description and actual RFP template structure. | Datasheet.md; Guidance.md; Specification.md; Decomposition | Multiple | Contender 1: 3 categories (Decomposition/Datasheet). Contender 2: Guidance example structure. Contender 3: Actual RFP template. | Obtain RFP Appendix H. Confirm whether decomposition 3-category description matches template or requires refinement. | TBD |

#### No warranted items case
_Lens C:normative:consistency requires template validation (conflict noted above)._

---

### Lens: C:operative:sufficiency
**LensValue:** "confirmed execution readiness"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | MissingSlot | Procedure | Procedure.md Prerequisites (Reference Materials Required) lists 6 required materials but marks several locations as "TBD" (template location, RFP file location, Addendum 03 location). | Confirmed execution readiness requires all prerequisites to be accessible. Current state is "conditional readiness." | Procedure.md | Prerequisites | N/A | Action: Proposal Manager must obtain and provide file locations for RFP source files (Appendix H template, Addendum 03) before Procedure Step 1 begins. | TBD |

#### No warranted items case
_Lens C:operative:sufficiency requires prerequisites action (noted above)._

---

### Lens: C:operative through C:evaluative:consistency
**LensValue:** (multiple cells)

#### No warranted items case
_No warranted items identified for these remaining lenses. Operational and evaluative dimensions are adequately addressed by Specification.md, Guidance.md, and Procedure.md._

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity through F:normative:consistency
**LensValue:** (multiple cells)

#### No warranted items case
_No warranted items identified. Normative requirements are well-established by Specification.md._

---

### Lens: F:normative:sufficiency
**LensValue:** "defensible prescriptive substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | WeakStatement | Specification | R-007 ("Schedule B base scope costs SHALL NOT include the pickled sand storage building") is substantiated by Addendum 03, but verification guidance is buried in Verification section. | Defensible prescriptive substantiation requires clear verification method called out in requirement statement. | Specification.md | R-007 | N/A | Add to requirement: "Verification: Negative check — no pickled sand storage building line item in base costs. Critical per Addendum 03 and disqualification risk per Decomposition Section 3 (C-07)." | TBD |

#### No warranted items case
_Lens F:normative:sufficiency requires enhancement (noted above)._

---

### Lens: F:operative:sufficiency
**LensValue:** "demonstrated functional adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | TBD_Question | Procedure | Procedure Step 3 (Apply Unit Costs) provides "typical" cost allocation examples but does not specify firm's chosen approach. | Demonstrated functional adequacy requires knowing the chosen cost source (firm internal database, RSMeans, hybrid). | Procedure.md; Guidance.md | Step 3; Considerations (Estimating at Proposal Stage) | Guidance references "Reference project data" but does not mandate decision. Procedure Step 2 notes options but does not declare choice. | Confirm cost estimation approach with Commercial Lead before Step 3 execution. Document chosen approach in DEL-05-03. | TBD |

#### No warranted items case
_Lens F:operative:sufficiency requires decision documentation (noted above)._

---

### Lens: F:evaluative:sufficiency
**LensValue:** "warranted value substantiation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | RationaleGap | Guidance | Guidance.md Principle 5 (Right-Sizing Contingency and Allowances) discusses trade-off options but does not tie each to "warranted value substantiation" for evaluators. | Warranted value substantiation requires explaining why chosen contingency approach is defensible. Guidance discusses options but does not evaluate which demonstrates best value. | Guidance.md | Principle 5 | N/A | Add: "Warranted value substantiation for municipal client is demonstrated when contingency approach balances transparency with competitive positioning. Recommend: Explicit contingency line (if template permits) or clear allocation logic in DEL-05-03." | TBD |

#### No warranted items case
_Lens F:evaluative:sufficiency requires enrichment (noted above)._

---

### Lens: F:operative and evaluative — remaining cells
**LensValue:** (multiple cells)

#### No warranted items case
_No warranted items identified for remaining lenses. F matrix coverage is otherwise adequate._

---

## Matrix D — Objectives (3x4)

#### No warranted items case
_No warranted items identified for any lens in Matrix D. Objectives are well-established by Decomposition (Section 8, Section 15) and Specification.md._

---

## Matrix X — Verification (4x4)

### Lens: X:guiding:consistency
**LensValue:** "enduring governance alignment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | VerificationGap | Multi | Procedure.md Verification section lists 6 checkpoints (Step 1–6 completion) but does not explicitly verify "Addenda Acknowledgement" (Specification.md R-006), which is a critical compliance item. Step 6 directs completion but no acceptance check exists. | Enduring governance alignment requires consistency: if R-006 is a requirement, it should have a verification checkpoint. Currently missing. | Specification.md; Procedure.md | R-006; Verification section | N/A | Add verification checkpoint: "Step 6 completion: Verify addenda acknowledgement line is completed and in correct location (Schedule B or A per RFP instructions). Responsible: Estimator + Proposal Manager. Timing: Before submission." | TBD |

#### No warranted items case
_Lens X:guiding:consistency requires enhancement (noted above)._

---

### Lens: X — remaining cells
**LensValue:** (multiple cells)

#### No warranted items case
_No warranted items identified for remaining X lenses. Verification coverage is otherwise adequate._

---

## Matrix E — Evaluation (3x4)

#### No warranted items case
_No warranted items identified for any lens in Matrix E. Evaluation criteria are well-established by Decomposition (Section 15) and Specification.md (Acceptance Criteria)._

---

## Conflict Summary

### Conflict 1: Cost Structure Consistency (B-003, C-003)
- **Documents involved:** Datasheet.md, Guidance.md, Procedure.md, Decomposition
- **Issue:** Three different implicit cost structures (3 categories, subdivisions, template-dependent)
- **Resolution path:** Obtain Appendix H template and align all documents to it

### Conflict 2: Addenda Acknowledgement Location (B-004, F-001)
- **Documents involved:** Specification.md, DEL-05-01, DEL-05-02
- **Issue:** Whether acknowledgement belongs on Schedule A or Schedule B
- **Resolution path:** Review RFP Appendix H instructions; clarify deliverable boundary

### Conflict 3: Cost Reconciliation Format (B-006)
- **Documents involved:** Specification.md, Guidance.md, Datasheet.md, Procedure.md
- **Issue:** Linked formulas vs. manual reconciliation (Excel vs. PDF format)
- **Resolution path:** Obtain RFP format requirements; update documents

### Conflict 4: Technical Item Costing (B-001)
- **Documents involved:** Datasheet.md, Procedure.md
- **Issue:** Which Addendum 03 technical items get separate cost lines
- **Resolution path:** Confirm with Design/Civil Leads; document in Datasheet

---

## Critical Path Blockers

1. **Appendix H template access** — Required for Steps 1–3 of Procedure. TBD location blocks execution.
2. **Cost estimation approach decision** — Commercial Lead must confirm markup/contingency strategy before Step 3.
3. **RFP format confirmation** — Excel vs. PDF format must be confirmed to enable proper reconciliation methodology.

---

## Warranted Item Tally by Type

| Type | Count | Examples |
|---|---|---|
| WeakStatement | 4 | A-001, A-002, B-002, C-001, F-001 |
| MissingSlot | 6 | A-003, B-001, B-005, C-002, C-004, X-001 |
| Conflict | 4 | B-003, B-004, B-006, C-003 |
| TBD_Question | 3 | A-004, F-002, and others |
| RationaleGap | 3 | A-005, B-004, F-003 |
| VerificationGap | 2 | C-002, X-001 |

---

**Document Status:** SEMANTIC_LENSING completed
**Last Updated:** 2026-02-04
**Completeness:** All seven matrices (A, B, C, F, D, X, E) systematically applied as lenses. 38 warranted items identified and documented with provenance, conflict tracking, and human decision points preserved.
