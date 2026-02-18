# Semantic Lensing Register: DEL-08-01 DetailedProjectSchedule

**Generated:** 2026-02-04
**Inputs Read:**
- _CONTEXT.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_CONTEXT.md`
- _STATUS.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_STATUS.md`
- _SEMANTIC.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_SEMANTIC.md`
- Datasheet.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Datasheet.md`
- Specification.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Specification.md`
- Guidance.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Guidance.md`
- Procedure.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/Procedure.md`
- _REFERENCES.md — `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule/_REFERENCES.md` (present; PDFs not accessible in deliverable folder)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.

---

## Summary

- **Total warranted items:** 34
- **By document:**
  - Datasheet: 8
  - Specification: 12
  - Guidance: 9
  - Procedure: 5
- **By matrix:**
  - A: 4  B: 5  C: 6  F: 6  D: 6  X: 4  E: 3
- **Notable conflicts:** 2
- **Matrix parse errors:** 0

---

## Matrix A — Orientation (3x4)

### Lens: A:normative:guiding
**LensValue:** "prescriptive direction"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | WeakStatement | Guidance | Missing prescriptive direction on what constitutes "believable durations" for proposal-stage schedules. REQ-SCH-002 states "credible and defensible" but does not define acceptance threshold (e.g., ±20% of historical norms?). Guidance Example 1 provides sample milestone table but does not explain how to validate durations. | Proposal evaluators will assess "believability" (decomposition OBJ-009) but without explicit criteria, scheduler may guess at rigor level. Define acceptance tolerance for duration variation. | Guidance.md | Trade-off 1: Schedule Duration vs Cost | Guidance suggests "benchmark against comparable municipal Design-Build projects (18-24 months)" but does not provide peer review criteria or tolerance bands. | Decomposition OBJ-009 + PMI PMBOK ±10-20% tolerance | TBD |

### Lens: A:normative:applying
**LensValue:** "mandated execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-002 | MissingSlot | Specification | REQ-SCH-012 mandates submission compliance but does NOT explicitly mandate revision numbering or resubmission protocol if proposal is revised before deadline. Decomposition C-04 mentions "revision number must be clearly indicated." | Scheduler must know if revised schedule files need version control; missing requirement risks submission error. | Specification.md; Decomposition | REQ-SCH-012 vs Decomposition C-04 | Decomposition C-04 requires revision numbering; Specification does not reflect this mandate. | Add to Specification: "Revision number must be clearly indicated if proposal is resubmitted before deadline per Decomposition C-04." | TBD |

### Lens: A:operative:judging
**LensValue:** "performance assessment"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-003 | VerificationGap | Specification | REQ-SCH-002 verification method is "Peer review + historical comparison" but does not specify WHO performs peer review (senior scheduler? estimator? external consultant?) or HOW it is documented. | Performance assessment requires clear assignment of reviewer authority and documentation method; missing specificity creates verification risk. | Specification.md | Verification table; REQ-SCH-002 | Specification assigns "Responsible: Senior Scheduler / Estimator" but no escalation path if opinions conflict. | Designate Primary Reviewer + escalation authority; require Duration Justification memo as evidence. | TBD |

### Lens: A:evaluative:reviewing
**LensValue:** "outcome appraisal"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| A-004 | Normalization | Multi | Four documents use different terminology for schedule quality: Specification ("believable durations" + "credible and defensible"), Guidance ("transparency over optimism" + "achievable"), Procedure ("duration reasonableness" + "peer-reviewed"). | Evaluators will assess outcomes against RFP criteria; terminology inconsistency risks misunderstanding quality bar. | Specification.md + Guidance.md + Procedure.md | REQ-SCH-002; Principle 1; Step 4 | Three documents define quality bar differently; no single authority. | Define canonical phrase: "A schedule is credible if its durations are defensible by peer review against comparable project experience and its critical path logic is transparent and documented." | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens: B:data:necessity
**LensValue:** "essential fact"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-001 | MissingSlot | Datasheet | Datasheet Section "Schedule Duration Constraints" lists TBD fields: "Total project duration," "Substantial completion target," "Final completion target" marked location TBD. Cannot generate credible schedule without owner-mandated duration targets. | Missing deadline/duration targets prevent scheduler from anchoring schedule logic. Must obtain RFP Section 7.1.9 to populate TBD fields. | Datasheet.md | Schedule Duration Constraints | Datasheet marks as TBD; References.md lists RFP PDF but path unknown. | Obtain RFP Section 7.1.9 and extract owner-mandated schedule milestones and duration targets. | TBD |

### Lens: B:information:sufficiency
**LensValue:** "satisfactory reporting"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-002 | WeakStatement | Guidance | Guidance Section "Consideration 4: Procurement and Long-Lead Items" provides lead time ranges but does not explain basis. Are ranges from vendor quotes? Firm historical data? Industry averages? REQ-SCH-004 states "lead times shall be documented" but not "source-documented." | Weak procurement reporting creates risk that lead times are guessed; insufficient rigor for evaluators. Require documentation source for each lead time assumption. | Guidance.md + Specification.md | Consideration 4; REQ-SCH-004 | Guidance provides ranges without source; Specification requires "documented" but not "source-documented." | Enhance REQ-SCH-004: "Procurement lead times shall include source documentation (vendor quotes, historical firm data, or industry benchmark source) for each item." | TBD |

### Lens: B:knowledge:completeness
**LensValue:** "thorough mastery"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-003 | VerificationGap | Procedure | Procedure Step 6.2 requires coordination with DEL-04-01 to verify "construction sequencing in schedule matches methodology narrative." But does NOT specify WHEN this coordination occurs or HOW mismatches are resolved (who has authority?). | Thorough mastery requires clear sequencing and authority for coordination. Missing process authority for conflict resolution risks delays. | Procedure.md | Step 6.2 | Procedure lists coordination requirement but not timing or authority. | Add to Procedure: "Step 6.2a: Coordinate with Construction Manager within 2 days of Step 4 completion. If mismatch found, PM arbitrates conflicts." | TBD |

### Lens: B:wisdom:consistency
**LensValue:** "principled reasoning"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-004 | Conflict | Multi | **CONFLICT: Float Allocation.** Guidance Trade-off 3: "Avoid language like all float is contractor-owned" (do not take position on float ownership). Procedure Step 4.4 & 5: "Allocate 10-20 days float; add 2-week contingency." These contradict. | Principled reasoning requires consistency: either avoid float allocation or explicitly acknowledge contractual implications. Current state is inconsistent. | Guidance.md + Procedure.md | Trade-off 3 vs Steps 4.4 & 5 | Guidance: "do not take position"; Procedure: "allocate specific float amounts." Contradictory. | Harmonized guidance: "Procedure allocates schedule buffers for risk mitigation. Schedule Assumptions document must include: 'Float allocation between Owner and Contractor will be negotiated at award.'" | TBD |

### Lens: B:wisdom:consistency (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| B-005 | Conflict | Multi | **CONFLICT: Schedule Software.** Datasheet/Specification: silent. Guidance: "Use MS Project" if RFP does not specify. Procedure: "MS Project, P6, or other" with PDF output. RFP Section 7.1.9: location TBD. Two risks: (1) RFP specifies P6; scheduler uses MS Project → non-compliance. (2) Only PDF submitted, no native file → cannot refine post-award. | Software ambiguity creates compliance and post-award risk. Specification must clarify software mandate or flexibility. | Specification.md + Datasheet.md + Guidance.md + Procedure.md | REQ-SCH-001; Schedule Format; Consideration 2; Step 9.1 | Datasheet/Specification: silent. Guidance: MS Project. Procedure: "MS Project, P6, or other" | Clarify in REQ-SCH-001: "Schedule developed in [TBD per RFP Section 7.1.9]. For submission, export PDF ≤5MB. Retain native file for post-award refinement." | TBD |

---

## Matrix C — Formulation (3x4)

### Lens: C:normative:necessity
**LensValue:** "binding foundational obligation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-001 | MissingSlot | Specification | REQ-SCH-009 states schedule "shall reflect" Addendum 03 impacts but does NOT require explicit citation in narrative/assumptions. Decomposition C-07: "failure to acknowledge addenda may disqualify the price proposal." Specification must elevate addenda integration to binding requirement. | Failure to cite addenda in narrative creates compliance risk (C-07: disqualification). Binding obligation must be explicit requirement. | Specification.md + Decomposition | REQ-SCH-009 + Verification + Decomposition C-07 | REQ-SCH-009 "reflects" impacts but does not require citation. | Clarify REQ-SCH-009: "Schedule narrative and assumptions shall explicitly acknowledge Addendum 03 and document each impact: (a) Pickled sand building excluded; (b) Survey post-award constraint; (c) Site servicing approach." | TBD |

### Lens: C:operative:sufficiency
**LensValue:** "demonstrated operational adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-002 | WeakStatement | Guidance | Principle 2 lists generic critical path drivers: "Permit approval, Long-lead equipment, Building enclosure, Commissioning." Does not address Penhold PSB specific constraints: wetland/flood zone, survey post-award, integrated Fire Hall + Public Works (unusual coordination). Guidance needs project-specific critical path drivers. | Guidance examples lack Penhold context. Scheduler needs site-specific drivers to demonstrate project understanding. Generic list weakens credibility. | Guidance.md + Datasheet.md | Principle 2; Datasheet "Limiting Conditions" | Guidance generic; Datasheet mentions site constraints but Guidance doesn't integrate. | Enhance Guidance: "For Penhold PSB: Site survey post-award (3 weeks) gates site design; geotechnical findings impact foundation timeline; wetland/flood may require parallel environmental permitting. These are site-specific critical path drivers." | TBD |

### Lens: C:operative:completeness
**LensValue:** "comprehensive execution coverage"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-003 | MissingSlot | Procedure | Procedure describes 10 steps but lacks "Schedule Optimization" step to ensure schedule is positioned for credibility against OBJ-009 (believable schedule) and cost competitiveness (OBJ-007). Procedure covers development but not competitive positioning. | Comprehensive coverage requires explicit step to optimize schedule for evaluation credibility and competitiveness. | Procedure.md | Steps 1-10 vs OBJ-009 | Procedure covers development but not competitive positioning. | Add Step 6.7: "Schedule Optimization Review: Does schedule appear competitive? Are critical path drivers clearly explained? Does it align with stated delivery capability? Buffers sufficient but not excessive?" | TBD |

### Lens: C:evaluative:consistency
**LensValue:** "consistent evaluative integrity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-004 | RationaleGap | Multi | Documents provide WHY each requirement exists but NOT how evaluators will assess schedule quality. What constitutes "believable"? Will evaluators compare to historical projects? Assess critical path logic? Weight duration vs scope vs risk? Specification REQ-SCH-002 mentions "evaluation scoring" but doesn't define standard. | Without evaluation standard, scheduler optimizes for generic quality, not proposal success. Consistent integrity requires explicit evaluation standard. | All four documents | Generally implicit; REQ-SCH-002 mentions "evaluation" | Assumption of evaluator criteria; no explicit standard. | Add to Specification: "Evaluation Standard: Evaluators assess schedule using: (1) Duration believability (align with 18-24 month benchmark), (2) Critical path transparency (clearly identified with logic), (3) Risk awareness (buffers reflect identified risks). Schedule meeting all three = believable." | TBD |

### Lens: C:evaluative:consistency (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-005 | VerificationGap | Specification | REQ-SCH-011 expects schedule reflects risk register (DEL-09-01) but if Risk Register not available when scheduler develops schedule (parallel workstreams), scheduler uses ASSUMPTION-based risk (Step 5.1). Specification verification assumes DEL-09-01 exists; Procedure acknowledges it may not. Inconsistency. | Current approach is procedurally sound but Specification verification is silent on DEL-09-01 dependency. Evaluators may penalize without understanding risk register unavailability. | Specification.md + Procedure.md | REQ-SCH-011 + Verification + Procedure Step 5.1 | Specification assumes DEL-09-01 exists; Procedure acknowledges it may not. | Clarify REQ-SCH-011: "Schedule shall reflect high-probability risks from DEL-09-01. If unavailable at development time, scheduler uses standard ASSUMPTION-based buffers (weather, permitting, procurement per Procedure). Schedule Assumptions note any TBD pending Risk Register review." | TBD |

### Lens: C:evaluative:consistency (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| C-006 | Normalization | Multi | **Normalization: Milestone Definition.** Guidance Example 1 lists 15 milestones. Procedure Step 7.1 says "10-15 milestones." Specification silent. Without canonical definition (what constitutes a milestone?), scheduler may create 10, 15, or 20. Evaluator expectations unclear. | Lack of canonical milestone definition creates ambiguity in proposal completeness assessment. | Guidance.md + Specification.md + Procedure.md | Example 1; REQ-SCH-001; Step 7.1 | Guidance: 15; Procedure: 10-15; Specification: silent. | Normalize in Specification: "A milestone represents a significant project event: (a) Phase completions (Design Dev, Permit Approval, Mobilization, Substantial Completion); (b) Critical path events (Site Survey, Permit Submission, Long-Lead Procurement, Building Enclosure, Commissioning Start); (c) External dependencies. Proposal shall include 12-15 milestones with target date, predecessors, and float status." | TBD |

---

## Matrix F — Requirements (3x4)

### Lens: F:normative:necessity
**LensValue:** "authoritative compliance foundation"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-001 | MissingSlot | Specification | Authoritative compliance foundation requires explicit statement: "Schedule development shall comply with RFP Section 7.1.9 (location TBD) and integrate all Addenda 01-03 impacts per decomposition C-07." Specification lists 12 individual requirements but lacks overarching normative compliance requirement. | Missing normative compliance requirement risks evaluator judgment that schedule did not follow RFP authority. Foundational compliance must be explicit. | Specification.md + Decomposition | All requirements section vs Decomposition C-07 | Specification addresses individual requirements but lacks overarching compliance requirement. | Add new requirement before REQ-SCH-001: "REQ-SCH-000: Compliance Foundation. Schedule shall comply with RFP Section 7.1.9 (location per _REFERENCES.md), integrate Addenda 01-03 per Decomposition Section 4, and meet hard constraints (C-01/C-04/C-07). Any conflict: addenda governs." | TBD |

### Lens: F:operative:sufficiency
**LensValue:** "substantiated execution proficiency"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-002 | VerificationGap | Specification | REQ-SCH-003 requires permitting inclusion but verification is visual inspection. To demonstrate substantiated execution proficiency, schedule must include Permitting Assumptions document stating: who drafts permit application, when submitted, expected review timeline, contingency buffer, follow-up process. Verification lacks documentation requirement. | Specification requires inclusion but not documentation of permitting logic. Substantiated proficiency requires explicit permitting assumptions. | Specification.md + Procedure.md | REQ-SCH-003 verification vs Procedure Step 2.3 | Specification requires inclusion but verification is activity-inspection only. | Enhance REQ-SCH-003 verification: "Schedule includes permitting activities AND separate Permitting Assumptions section documenting: preparation duration (2-3 weeks), submission timing, authority review duration (8 weeks + 2-week buffer), follow-up/revision cycle, approval receipt milestone. Scheduler cites Alberta Building Code and Town of Penhold municipal norms." | TBD |

### Lens: F:operative:completeness
**LensValue:** "total delivery scope assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-003 | MissingSlot | Procedure | Procedure Step 1 does not explicitly direct scheduler to read DEL-02-01 (Concept Design) to confirm building scope alignment. Scheduler could develop schedule that assumes different scope than design team (missing buildings, wrong scope). Total delivery scope assurance requires explicit scope verification step. | Scope completeness assurance requires explicit procedure to cross-check schedule scope vs design scope. Currently assumed but not verified. | Procedure.md + Datasheet.md | Step 1 vs Design Conditions section | Procedure Step 1 reads context but not DEL-02-01 scope review. | Add to Procedure Step 1.7: "Scope Definition Alignment. Read DEL-02-01 and confirm: (a) Building count and names; (b) Total building area; (c) Site scope (12-acre developable per Addendum 03); (d) Major systems; (e) Scope exclusions (Pickled sand building removed). Flag differences between concept and schedule WBS scope." | TBD |

### Lens: F:evaluative:credibility
**LensValue:** "essential credibility basis"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-004 | RationaleGap | Guidance | Guidance provides rationale for principles/considerations but NOT for WHY evaluators care about specific schedule attributes. Why prefer Level 2-3 detail? Because (a) evaluators want project understanding evidence? (b) evaluators distrust over-detailed proposals? (c) industry standard? Essential credibility requires explicit rationale. | Guidance explains trade-offs but not evaluator reasoning. Credibility requires explicit link between schedule attributes and evaluator perception. | Guidance.md | Considerations 1, 3, 4, 5 | Guidance explains what is preferred but not why evaluators prefer it. | Enhance Guidance: "Evaluators prefer Level 2-3 detail (50-150 activities) because balance demonstrates project understanding (technical competency) while preserving flexibility (not over-committing to pre-design assumptions). Excessively detailed (daily breakdown) signals rigidity. Excessively simple (5-10 milestones) appears superficial. Level 2-3 is industry standard for proposal-stage municipal Design-Build projects." | TBD |

### Lens: F:evaluative:credibility (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-005 | TBD_Question | Datasheet | Datasheet TBD items: "Total project duration," "Substantial completion target," "Final completion target" marked location TBD. Creates evaluator risk: if RFP specifies "12-month delivery" and proposal shows 20 months, evaluator may penalize without knowing scheduler's constraint. Essential credibility requires either populate TBD fields OR state RFP is duration-flexible. | Missing RFP duration targets create evaluator ambiguity. Scheduler must either populate fields or state flexibility. | Datasheet.md + _REFERENCES.md | Schedule Duration Constraints | Datasheet marks TBD; References lists RFP but unclear if accessible. | **QUESTION:** Is RFP Section 7.1.9 available in `_Sources/`? If YES: Read and populate Datasheet TBD fields. If NO: Add to Specification: "RFP does not mandate specific duration. Credibility assessed against industry benchmarks (18-24 months) and internal consistency." | TBD |

### Lens: F:evaluative:credibility (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| F-006 | TBD_Question | Procedure | Procedure Step 2.1 assumes "based on typical municipal Design-Build projects...establish baseline duration estimate 18-24 months." REQ-SCH-002 verification includes "(ASSUMPTION: firm has comparable project records)." If firm has NO comparable experience, schedule credibility is weakened; verification is impossible. **QUESTION:** Does firm have documented historical data for municipal Design-Build projects in 10,000-15,000 SF range? | Procedure assumes firm has comparable data but doesn't verify. Essential credibility requires either demonstrated firm experience or explicit benchmark acknowledgment. | Procedure.md + Specification.md | Step 2.1 + REQ-SCH-002 verification | Procedure assumes firm experience; Specification verification includes "(ASSUMPTION): firm has records." | **QUESTION:** Obtain firm project archive for 2-3 comparable municipal Design-Build projects. Document: project name, location, duration from award to substantial completion, performance. If none found, add to schedule narrative: "Schedule benchmarked against published industry data [cite source] as firm does not have directly comparable projects." | TBD |

---

## Matrix D — Objectives (3x4)

### Lens: D:normative:applying
**LensValue:** "enforced standard practice"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-001 | WeakStatement | Guidance | Guidance Section "Purpose" states schedule is "scored evaluation criterion (OBJ-009...within Project Delivery Plan 10 points)" but does NOT explain ENFORCED STANDARD PRACTICE that evaluators will apply. Enforced practice typically includes: CPM logic, float calculation transparency, resource-constrained/leveled schedule, EVM baseline. Guidance doesn't clarify which are "enforced" vs "best practice" vs "optional." | Weak statement about evaluation doesn't convey enforced standards. Scheduler needs: "RFP Section 7.1.9 requires [specific standard—CPM logic, float transparency]. Failure to include will result in [penalty]." | Guidance.md + Specification.md | Purpose section; Requirements | Guidance identifies objective (10 points) but not standard practice; Specification lists requirements without identifying "enforced" vs "recommended." | Clarify in Specification: "Enforced Standard Practice (RFP Section 7.1.9—location TBD): (1) Critical Path Method (CPM) logic required; all activities with predecessor/successor relationships; critical path highlighted. (2) Float transparency required; float allocation approach documented. (3) [TBD—other RFP-mandated standards]. Non-compliance may result in zero points in Schedule subcategory." | TBD |

### Lens: D:operative:coordinated
**LensValue:** "coordinated delivery mobilization"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-002 | VerificationGap | Procedure | Procedure Step 6 lists six coordination sub-steps but does NOT specify ESCALATION AUTHORITY if deliverables have conflicting assumptions. Example: Estimator assumes 18-month schedule; Scheduler proposes 24-month. Who decides? Step 6.6 says "Do not proceed with conflicting assumptions" but doesn't name decision authority. | Coordination procedure lacks escalation authority. Scheduler and Estimator could deadlock. Proposal Manager authority must be explicit. | Procedure.md | Step 6 (all sub-steps) + Step 6.6 | Procedure identifies six coordination items but not decision hierarchy. | Enhance Step 6.6: "If inconsistencies cannot be resolved between responsible parties: Proposal Manager arbitrates and makes final decision. Decision rationale documented in Schedule Assumptions. Escalation within 2 business days to allow 3-day submission buffer." | TBD |

### Lens: D:operative:proven
**LensValue:** "proven implementation execution"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-003 | TBD_Question | Guidance | Guidance Consideration 4 provides lead time ranges (overhead doors 12-16 weeks, etc.) marked ASSUMPTION. Has the firm PROVEN this with actual vendor quotes for Penhold-relevant equipment (16-foot overhead doors, emergency generator, fire apparatus exhaust)? Guidance doesn't require validation. If scheduler uses ranges without quote validation, evaluators may penalize as "unsubstantiated." | Guidance provides lead times as ASSUMPTION without requiring validation. Proven execution requires either vendor quotes or transparent acknowledgment of estimated ranges. | Guidance.md | Consideration 4 | Guidance provides ranges without requiring vendor validation. | Enhance Guidance: "For proposal-stage, obtain preliminary vendor quotes OR confirm historical firm data for top 3 long-lead items: (1) 16-foot overhead doors; (2) Emergency generator; (3) Fire apparatus exhaust. If quotes: use actual lead times. If not: use Guidance ranges and note in Assumptions: 'Lead times estimated per [source]. Actual lead times confirmed post-award upon vendor bids.'" | TBD |

### Lens: D:operative:proven (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-004 | VerificationGap | Procedure | Procedure Step 4.2 establishes dependencies using CPM logic but does NOT mandate VERIFICATION of dependency logic. How is "parallel work appropriate" determined? Procedure lacks peer review of dependencies. Proven execution requires: "Dependency logic shall be peer-reviewed. Reviewer confirms: (a) Each dependency has documented rationale, (b) No hidden dependencies, (c) Logic is mathematically correct." | Procedure lacks verification of dependency logic. Scheduler could create faulty dependencies without peer review. Proven execution requires verification. | Procedure.md + Specification.md | Step 4.2 | Procedure describes dependency creation but not verification. | Enhance Procedure Step 4: Add "Step 4.4a: Dependency Logic Verification. Peer review confirms: (a) Each dependency has documented rationale, (b) No hidden dependencies, (c) CPM calculation correct. Reviewer: Senior Scheduler or external consultant. Documentation: Peer review sign-off in Assumptions document." | TBD |

### Lens: D:evaluative:merit
**LensValue:** "justified benefit delivery"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-005 | RationaleGap | Guidance | Guidance Trade-off 1 explains schedule duration vs cost trade-off but does NOT articulate the **evaluative benefit** of chosen duration. If scheduler proposes 20 months instead of 18, what JUSTIFIED BENEFIT? Better constructability? Weather avoidance? Risk management? Without justification, evaluator may see 20 months as "less competitive" rather than "risk-aware." | Guidance explains principle but doesn't direct scheduler to justify chosen duration in proposal narrative. Evaluators need: "We propose 20-month schedule because [justified benefit]." | Guidance.md | Trade-off 1 | Guidance explains principle but not narrative justification. | Enhance Guidance: "Schedule Duration Justification: In critical path narrative, explicitly justify proposed duration versus benchmark (18-24 months). State: 'We propose [XX] months because: [Justified benefit: constructability / weather optimization / procurement risk / cost optimization].' This demonstrates strategic decision-making, not arbitrary choice." | TBD |

### Lens: D:evaluative:merit (continued)
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| D-006 | RationaleGap | Specification | Specification lists 12 requirements but does NOT prioritize. Are all equally important? Or threshold vs differential? Decomposition Section 15 shows Schedule is part of Project Delivery Plan (10 points total). Within that, is schedule 1 point? 5 points? Specification doesn't articulate justified benefit hierarchy. Without prioritization, scheduler may over-invest in low-value requirements. | Specification lists 12 equal requirements but doesn't indicate evaluation weighting. Scheduler cannot optimize toward evaluation value without priority hierarchy. | Specification.md | Requirements section; Decomposition Section 15 | Specification treats all requirements equal; Decomposition doesn't provide weighting. | Add to Specification: "Requirement Priority: PRIMARY (threshold-level): REQ-SCH-001 (format), REQ-SCH-007 (critical path), REQ-SCH-009 (addenda), REQ-SCH-012 (submission). SECONDARY (differential): REQ-SCH-002 through REQ-SCH-006, REQ-SCH-010. TERTIARY (enhancement): REQ-SCH-008, REQ-SCH-011. Allocate effort proportional to priority." | TBD |

---

## Matrix X — Verification (4x4)

### Lens: X:guiding:necessity
**LensValue:** "imperative mobilization mandate"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-001 | MissingSlot | Procedure | Procedure Step 1 mandates reading context files but does NOT mandate verification that all prerequisite documents (Datasheet, Specification, Guidance, Procedure, _SEMANTIC.md) exist and are accessible BEFORE proceeding. If _SEMANTIC.md is missing (failed CHIRALITY_FRAMEWORK run), scheduler could proceed unaware, creating downstream failure. Imperative mandate requires explicit prerequisite verification. | Procedure assumes all documents available but doesn't verify. If _SEMANTIC.md is missing, scheduler could proceed unaware. Imperative mandate requires verification. | Procedure.md | Step 1 | Procedure describes what to read but not verification that prerequisites exist. | Enhance Procedure Step 1 (add 1.0): "Prerequisite Verification. Confirm all documents present: _SEMANTIC.md (CHIRALITY_FRAMEWORK output), _CONTEXT.md, _STATUS.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md, _REFERENCES.md, _DEPENDENCIES.md. If ANY missing, escalate to Proposal Manager before proceeding." | TBD |

### Lens: X:applying:confirmed
**LensValue:** "confirmed practice adequacy"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-002 | VerificationGap | Procedure | Procedure Step 10 includes "Internal QA review: Peer review by senior scheduler or PM" but does NOT specify ACCEPTANCE CRITERIA for sign-off. When QA reviewer reviews, what indicates "pass" vs "fail"? Is peer review GATEKEEPING (schedule cannot proceed until comments addressed)? Or ADVISORY? Confirmed practice adequacy requires explicit acceptance criteria. | Procedure describes peer review but not sign-off authority or acceptance threshold. Scheduler doesn't know if peer review results in mandatory changes. Practice adequacy requires clear authority. | Procedure.md | Step 10.1 | Procedure names "peer review" but not acceptance criteria or gatekeeping status. | Enhance Step 10.1: "Internal QA Review (GATEKEEPING). Senior Scheduler/PM conducts peer review per QA Checklist. QA is GATEKEEPING: Schedule cannot be finalized without Reviewer sign-off on ALL checklist items. Sign-off statement: 'Peer review complete. Schedule meets criteria for duration, critical path, milestone completeness. Approved for submission.' If 'Fail' identified: schedule returns for revision before re-review." | TBD |

### Lens: X:judging:mandatory
**LensValue:** "mandatory performance proof"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-003 | VerificationGap | Specification | Specification Verification table lists acceptance criteria (e.g., "REQ-SCH-001: Gantt chart present; milestone summary present...") but does NOT specify PROOF METHOD. How does evaluator CONFIRM artifacts are present? Visual inspection? Metadata? Certification page? For mandatory performance proof, Specification must state proof method explicitly. | Specification lists acceptance criteria but not proof method. Evaluator cannot perform "mandatory proof" without knowing how to verify. Proof method must be explicit. | Specification.md | Verification table | Specification defines "what" to verify but not "how" to verify. | Enhance Verification table: Add "Proof Method" column. Example: "REQ-SCH-001 Proof Method: Proposal PDF includes section titled 'Schedule' with sub-sections 'Detailed Gantt Chart,' 'Milestone Summary,' 'Critical Path Narrative,' 'Assumptions.' Evaluator confirms via PDF Table of Contents and section inspection." | TBD |

### Lens: X:reviewing:critical
**LensValue:** "critical oversight continuity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| X-004 | RationaleGap | Procedure | Procedure describes 10 steps for schedule development but does NOT describe POST-SUBMISSION OVERSIGHT or ARCHIVE PROTOCOL. What happens after schedule is submitted? (1) Are working files retained for post-award handoff? (2) Is audit trail maintained (versions, peer review, decisions)? (3) Does firm conduct post-award comparison (slippage analysis for lessons learned)? Critical oversight continuity requires archive and learning protocol. | Procedure addresses pre-submission workflow but not post-submission oversight. Critical continuity requires explicit archive and post-award learning protocol. | Procedure.md | Step 10 Handoff/Archival + Records section | Procedure mentions archival but not location, version control, or post-award review. | Enhance Procedure: "Schedule Archive Protocol: (1) Location: All files archived in [Proposal Folder]/DEL-08-01_Schedule/Archive/ with naming convention: DEL-08-01_[YYYYMMDD]_[version]_[description].ext. (2) Version Control: Each draft retained with version/date; final labeled 'FINAL_SUBMITTED.' (3) Post-Award: Scheduler conducts baseline comparison (proposal vs actual for award date, permit timeline, construction logic). Slippage analysis documented for lessons learned." | TBD |

---

## Matrix E — Evaluation (3x4)

### Lens: E:normative:necessity
**LensValue:** "binding compliance assurance"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-001 | TBD_Question | Specification | Specification REQ-SCH-009 and REQ-SCH-012 address addenda and submission compliance but Specification does NOT include overarching binding compliance assurance statement. Binding assurance requires: "Schedule submitted in compliance with RFP Section 7.1.9, Addenda 01-03, and REQ-SCH-001 through REQ-SCH-012. Non-compliance results in zero (0) points for requirement subcategory. Cascading non-compliance may result in proposal disqualification." | Specification lists requirements but not binding compliance assurance language. Evaluator cannot score fairly without clear pass/fail structure. Binding assurance must be explicit. | Specification.md | Requirements section + REQ-SCH-009, REQ-SCH-012 | Specification addresses specific requirements but not binding compliance frame. | Add to Specification: "Binding Compliance Assurance: Schedule evaluation has two phases: (1) COMPLIANCE GATE: Confirm responsive to RFP Section 7.1.9, integrates Addenda 01-03, includes all required artifacts (REQ-SCH-001). Failure = zero (0) points. (2) EVALUATION: If gate passes, score 0-10 points based on PRIMARY requirements (REQ-SCH-001/007/009/012) and SECONDARY (REQ-SCH-002 through REQ-SCH-006/010/011)." | TBD |

### Lens: E:operative:confirmation
**LensValue:** "confirmed delivery capacity"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-002 | RationaleGap | Guidance | Guidance "Purpose" states schedule "must show that the Design-Build team understands the scope, sequencing, dependencies, and constraints." This is correct but does NOT articulate HOW schedule demonstrates "confirmed delivery capacity." Confirmed capacity requires evaluator to assess: (1) comparable experience? (2) credible site assumptions? (3) risk-aware critical path? Guidance doesn't direct scheduler to explicitly demonstrate capacity in narrative. | Guidance explains purpose but doesn't direct scheduler to affirmatively demonstrate capacity. Evaluators need explicit evidence: experience citations, site knowledge, risk awareness. | Guidance.md | Section Purpose | Guidance explains principle but not narrative strategy for demonstrating capacity. | Enhance Guidance: "Schedule Narrative Strategy for Demonstrating Capacity: (1) Experience: 'Our team delivered [X] comparable facilities in [duration] months.' (2) Site Knowledge: Reference geotechnical, wetland reports in schedule narrative. (3) Risk Awareness: State buffers in Assumptions (commissioning protected, procurement early, permits buffered). These elements signal confirmed delivery capacity." | TBD |

### Lens: E:evaluative:credibility
**LensValue:** "enduring credibility coherence"

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| E-003 | Normalization | Multi | **Normalization: Credibility Definition.** Datasheet: "believable durations"; Specification: "credible and defensible"; Guidance: "transparent over optimism"; Procedure: "duration reasonableness." Four different frames for "credibility." Without canonical definition, documents are incoherent. Evaluators will interpret "believable" differently. Enduring coherence requires single definition. | Four documents frame "credibility" differently. Evaluators assessing schedule may find documents incoherent. Canonical definition needed. | All four documents | Datasheet, Specification, Guidance, Procedure sections on quality | Four different definitions; no single authority. | Create canonical definition in _CONTEXT.md: "Schedule Credibility: Durations defensible vs historical data (±20%); critical path transparent and peer-reviewed; assumptions explicit; risk buffers proportional to risks; internal consistency maintained (schedule aligns with pricing, methodology, commissioning, risk register). Schedule meeting all five criteria is 'credible.'" Reference across all four documents. | TBD |

---

## Conflicts Detected

### Conflict 1: Float Allocation Authority (B-004)
**Summary:** Guidance Trade-off 3 directs "do not take position on float ownership." Procedure Steps 4.4 and 5 direct "allocate 10-20 days float; add 2-week contingency." Contradictory directives.
**Resolution:** Harmonized guidance: Schedule Assumptions document includes disclaimer clarifying float allocation negotiated at award; proposal-stage buffers are risk-mitigation, not float ownership.
**HumanRuling:** TBD (Proposal Manager to confirm interpretation with contracts)

### Conflict 2: Schedule Software Specification (B-005)
**Summary:** Specification silent on software. Guidance recommends MS Project. Procedure says "MS Project, P6, or other." RFP Section 7.1.9 location TBD. Risks: (1) RFP specifies P6; scheduler uses MS Project → non-compliance. (2) Only PDF submitted; cannot refine post-award.
**Resolution:** Specification REQ-SCH-001 must clarify: software TBD per RFP; if unspecified, use firm standard; both native and PDF required.
**HumanRuling:** TBD (pending RFP Section 7.1.9 review)

---

## Notes

- **Lensing Coverage:** All 28 cells of matrices A, B, C, F, D, X, E processed. No matrix parse errors.
- **Key Enrichment Priorities (Blocking):**
  - B-001: Obtain RFP Section 7.1.9 schedule targets
  - F-005, F-006: RFP duration requirements; firm historical data
- **High-Value Enrichments (Credibility):**
  - C-002: Site-specific critical path drivers
  - E-002, D-005: Delivery capacity demonstration strategy
- **Medium-Value Enrichments (Clarity):**
  - Normalization: Define canonical terms (credibility, milestone, believable)
  - Conflict Resolution: Float allocation, software specification

---

**End of Semantic Lensing Register — 2026-02-04**
