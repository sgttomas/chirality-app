# Guidance: DEL-09-01 Risk Register and Mitigation Plan

## Purpose

The Risk Register and Mitigation Plan exists to:

1. **Demonstrate proactive risk awareness** — Show the evaluation team that the Design-Build proponent has thoroughly analyzed potential threats to successful project delivery and proposal competitiveness

2. **Build evaluator confidence** — Provide transparent, grounded risk identification and credible mitigation strategies that increase confidence in the team's ability to deliver on commitments

3. **Support internal decision-making** — Inform design decisions, pricing assumptions, schedule development, and resource allocation by making risks explicit and actionable

4. **Fulfill RFP expectations** — Address implicit and explicit risk management expectations embedded in the RFP requirements and evaluation criteria (OBJ-008: Manage risk & unknowns transparently)

5. **Enable quality assurance** — Provide Quality Management Plan procedures that ensure design, construction, commissioning, and documentation meet project standards and owner expectations

**Source:** _CONTEXT.md Description and Acceptance Criteria; Decomposition §6 OBJ-008, §8 DEL-09-01

### Downstream Use

This deliverable supports:

- **Proposal Evaluation (Primary):** Risk register and QMP contribute to Project Delivery Plan scoring (10 points per Decomposition §15)
- **Schedule Development (DEL-08-01):** Risk register identifies schedule risk factors and informs schedule contingencies
- **Pricing Development (DEL-05-03):** Risk register informs pricing assumptions, allowances, and contingencies
- **Site Due Diligence Summary (DEL-09-02):** Risk register references technical reports analyzed in due diligence summary
- **Construction Administration (PKG-06):** QMP procedures inform construction methodology and reporting plans
- **Commissioning Plan (DEL-06-01):** QMP commissioning procedures align with commissioning/closeout narrative

**Process Governance [D-002]:**
- **PM** leads risk identification and owns final risk register
- **Technical Leads** (by discipline) assess risks in their areas
- **Consensus** on scoring/mitigation expected; PM arbitrates disputes
- **Escalation** to Proposal Manager for conflicts affecting proposal strategy

**Source:** ASSUMPTION — Logical downstream relationships based on deliverable interdependencies (not explicitly tracked per _DEPENDENCIES.md); _CONTEXT.md Responsible (PM + Technical Leads) [D-002 governance clarification]

## Principles

### Risk Management Principles

1. **Source Fidelity Over Speculation**
   - All material risks must be grounded in accessible sources: RFP, addenda, reference reports (geotechnical, wetland, environmental, grading, flood, adjacent development)
   - When a risk is inferred rather than explicitly stated, label it **ASSUMPTION** with clear rationale
   - If information needed to assess a risk is unavailable, mark the risk or mitigation **TBD** rather than guessing

   **Evaluator Expectation [E-001]:** Risks directly cited from RFP/addenda/reference reports (PRESCRIPTIVE) are prioritized; inferred risks labeled ASSUMPTION with clear rationale are acceptable if mitigation is credible; unsourced speculation is penalized by evaluators.

   **Rationale:** Risk register must be credible to evaluators; unsupported speculation undermines confidence and violates acceptance criteria "ties back to addenda clarifications and reference reports" (_CONTEXT.md)

2. **Transparency Over Concealment**
   - Identify risks honestly, including uncomfortable truths (e.g., survey unavailability, open issues, scope ambiguities)
   - Mitigation strategies should acknowledge uncertainty and propose monitoring/contingencies rather than claiming false certainty

   **Rationale:** Evaluators value transparency and realism; concealing known risks creates liability exposure and damages trust

3. **Actionability Over Abstraction**
   - Each mitigation strategy must be assignable to a specific role (PM, Technical Lead, Estimator, etc.)
   - Mitigation actions should be concrete (e.g., "Request survey immediately after award" not "Manage survey risk")
   - Include monitoring approach and trigger points for contingency activation

   **Mitigation Strategy Decision Matrix [A-004]:**
   | Risk Score | Strategy Type | Application |
   |------------|---------------|-------------|
   | < 8 | Accept & Monitor | Monitoring alone; no active mitigation required |
   | 8-14 | Preventive Action (reduce P) | For permitting/procurement risks where early engagement changes probability |
   | 8-14 | Contingency Allowance (reduce I) | For cost/site risks where allowance absorbs impact |
   | ≥ 15 | Detailed Mitigation Plan | Requires both preventive + contingency; executive oversight |
   | Any | Avoid (scope change) | For design risks where removal is feasible |

   **Multi-Owner Risks [F-004]:** For cross-functional risks where primary and secondary owners must coordinate: Primary owner leads mitigation and monitors status; secondary owners listed as stakeholders with defined coordination points (e.g., "Primary: PM; Stakeholders: Design Lead (design changes), Estimator (cost changes)")

   **Rationale:** Deliverable must demonstrate that risks are **managed**, not merely **acknowledged**; per SOW-026, mitigation plans must be part of the risk register

4. **Proportionality in Risk Assessment**
   - Focus effort on material risks that could affect proposal score or project delivery success
   - Use probability × impact scoring to prioritize attention (high-score risks require detailed mitigation; low-score risks may be monitored only)

   **Rationale:** Risk register must be useful as a management tool, not exhaustive to the point of obscuring critical risks

5. **Integration with Quality Management**
   - Quality Management Plan procedures should prevent or detect risks early (e.g., design QC prevents design risks; construction QC detects defects before they cascade)
   - QMP should be viewed as a preventive risk control, not a separate activity

   **Risk-to-QC Control Mapping [B-005]:**
   | Risk Category | Controlling QC Area | Example Control Procedure |
   |---------------|---------------------|---------------------------|
   | Design | Design QC | Drawing coordination review at 90% CD; code compliance check |
   | Site | Construction QC | Foundation inspection before concrete pour; geotechnical observation |
   | Cost | Documentation QC | Cost reconciliation review; change order documentation |
   | Schedule | Construction QC | Progress verification at milestones; critical path monitoring |
   | Procurement | Documentation QC | Submittal review; delivery verification |
   | Environmental | Construction QC | Environmental compliance inspection; erosion control monitoring |
   | Permitting | Design QC + Documentation QC | Code compliance verification; permit application completeness |

   **Rationale:** Quality management is fundamentally about risk reduction; SOW-027 QMP requirement supports SOW-026 risk management requirement

**Prescriptive Authority Fallback [A-002]:** In absence of accessible ISO 31000, risk framework adheres to industry best practice: probability × impact scoring (1-5 scales) per PMI PMBOK guidance; high-score risks (≥15) require detailed mitigation. When ISO 31000 or other standard texts are unavailable, framework authority derives from established industry practice rather than standard citation.

**Source:** ASSUMPTION — Principles derived from ISO 31000 risk management philosophy and design-build proposal best practices; standard texts not accessible [A-002 prescriptive authority clarification]

### Quality Management Principles

1. **Prevention Over Detection**
   - Design QC procedures should catch errors before they propagate to construction documents
   - Construction QC procedures should verify conformance before work is concealed
   - Commissioning QC should validate function before owner acceptance

   **Design QC Checkpoint Decision Rule [C-002]:**
   - **Default:** Implement 5 design QC checkpoints (Concept, Schematic, Design Development, 90% CD, 100% CD)
   - **Low-risk projects:** May combine Concept + Schematic checkpoints
   - **High-risk areas (foundation, envelope, life safety):** Maintain full checkpoint sequence; do not compress

   **Rationale:** Early detection reduces rework cost and schedule impact; aligns with OBJ-005 (Demonstrate durability / ease of maintenance) by ensuring quality during execution

2. **Independence of Review**
   - QC checks should be performed by personnel other than the originator when feasible
   - Critical verifications (e.g., structural calculations, code compliance) should involve independent technical review

   **Rationale:** ASSUMPTION — Industry best practice to reduce confirmation bias and error propagation; specific requirement not stated in accessible sources **[RFP §10.2.2 QC/inspections clause details TBD]**

3. **Documentation of Quality Evidence**
   - QC activities should produce auditable records (inspection reports, test results, review checklists)
   - Documentation QC ensures that closeout documentation is complete and accurate

   **Rationale:** Supports commissioning, warranty, and future maintenance; aligns with DEL-06-01 closeout requirements and 12-month warranty baseline (Decomposition §8 DEL-06-01)

## Considerations

**Consideration Status [X-002]:** The 20 considerations listed below are **exemplars** of factor types (Site, Design, Cost, Schedule, Procurement, Compliance, QM factors); they are NOT mandatory requirements. Specification Scope (7 categories, FR-01...FR-07) defines mandatory requirements; team should address considerations relevant to their project risk profile.

### Factors to Weigh During Risk Register Development

#### Site and Environmental Factors

1. **Developable Area Constraint (12 acres functional / 20 acres total)**
   - **Consideration:** 8 acres in flood fringe (dog park/storm pond) are not available for building development
   - **Risk Implication:** Site layout must fit within 12-acre constraint; flood mitigation affects grading and drainage design
   - **Mitigation Consideration:** Confirm flood fringe setbacks with reference to flood zone mapping; consider grading design implications for storm water management
   - **Source:** Decomposition §4 Addendum 03; _REFERENCES.md Flood Zone Mapping relevance

2. **Geotechnical Conditions**
   - **Consideration:** Soil bearing capacity, groundwater, frost depth, and foundation design requirements affect foundation cost and schedule
   - **Risk Implication:** Unforeseen geotechnical conditions could increase foundation cost or delay schedule
   - **Mitigation Consideration:** Base foundation design on Geotechnical Investigation Report findings; consider foundation contingency allowance if conditions are variable
   - **Source:** _REFERENCES.md Geotechnical Investigation Report relevance

3. **Wetland Setbacks**
   - **Consideration:** Wetland buffer zones may constrain site layout and require environmental permitting
   - **Risk Implication:** Site layout non-compliance with wetland setbacks could delay permitting or require redesign
   - **Mitigation Consideration:** Incorporate wetland setback requirements from Wetland Assessment into site concept early; engage environmental permitting authority during design
   - **Source:** _REFERENCES.md Wetland Assessment relevance

4. **Environmental Assessment Findings**
   - **Consideration:** Potential contamination identified in Desktop Environmental Assessment could require remediation or special handling
   - **Risk Implication:** Contamination remediation could increase cost and schedule; failure to address could delay permitting
   - **Mitigation Consideration:** Review Environmental Assessment findings for remediation requirements; include remediation allowance in cost estimate if contamination is probable
   - **Source:** _REFERENCES.md Environmental Assessment relevance

5. **Site Grading Complexity**
   - **Consideration:** Earthwork quantities, drainage design, and site preparation complexity affect cost and schedule
   - **Risk Implication:** Underestimating earthwork quantities or drainage complexity could lead to cost overruns
   - **Mitigation Consideration:** Base grading design on Site Grading reference; coordinate with adjacent subdivision design to understand drainage interfaces
   - **Source:** _REFERENCES.md Site Grading and Adjacent Subdivision Design relevance

6. **Survey Availability After Award Only**
   - **Consideration:** Detailed survey files are not available during proposal development; concept design must rely on reference grading and site plan
   - **Risk Implication:** Site conditions discovered after award could differ from assumed conditions, affecting design and cost
   - **Mitigation Consideration:** Clearly state survey assumptions in pricing narrative (DEL-05-03); plan for immediate survey after award as prerequisite to detailed design; include survey verification as design milestone in schedule (DEL-08-01)
   - **Source:** Decomposition §4 Addendum 03; _REFERENCES.md Addendum 03 relevance; §9 SOW-024

#### Design and Program Factors

7. **Program Dimension Flexibility**
   - **Consideration:** Addendum 01 confirms that functional program intentionally omits many room dimensions to allow innovation; spaces must at minimum meet building code
   - **Risk Implication:** Underestimating required room sizes could lead to non-compliance or functional inadequacy; over-sizing rooms increases cost
   - **Mitigation Consideration:** Reference Addendum 03 sample room size ranges where provided; apply code minimums plus operational clearances for other spaces; validate room sizes with operational workflow assumptions
   - **Source:** Decomposition §4 Addendum 01 and 03; _REFERENCES.md Addendum 01 and 03 relevance

8. **Removed Pickled Sand Storage Building**
   - **Consideration:** Pickled Sand Storage building was removed from RFP scope per Addendum 03 (to be issued as separate RFP later)
   - **Risk Implication:** Low risk — scope reduction decreases cost and complexity
   - **Mitigation Consideration:** Ensure pricing and concept design do not include removed scope; confirm removal in compliance matrix (DEL-01-01)
   - **Source:** Decomposition §4 Addendum 03; §12 OI-002 CLOSED (Resolved)

9. **Addendum 03 Technical Requirements**
   - **Consideration:** Addendum 03 introduced multiple technical clarifications: 16 ft overhead doors, bay sumps, fire apparatus exhaust, generator supporting ICP, fill stations, solar-ready roof/orientation
   - **Risk Implication:** Missing any of these requirements in concept or cost estimate could lead to non-compliance or underpricing
   - **Mitigation Consideration:** Cross-check concept design (DEL-02-01) and cost breakdown (DEL-05-02) against Addendum 03 requirement list; use compliance matrix (DEL-01-01) to track incorporation
   - **Source:** Decomposition §4 Addendum 03; _REFERENCES.md Addendum 03 relevance; §9 SOW-010

#### Cost and Pricing Factors

10. **Site Servicing Allowance Treatment**
    - **Consideration:** Addendum 03 clarifies that allowance approach is permitted for site servicing; tie-ins to municipal infrastructure are not required to be priced in proposal
    - **Risk Implication:** Low risk — allowance approach reduces pricing uncertainty
    - **Mitigation Consideration:** Document allowance assumptions clearly in pricing narrative (DEL-05-03); ensure Schedule B (DEL-05-02) includes allowance line item with transparent basis
    - **Source:** Decomposition §4 Addendum 03; §12 OI-003 CLOSED (Resolved)

11. **FF&E Treatment (Open Issue)**
    - **Consideration:** Open Issue OI-004 asks "Define what to include as FF&E additional item (optional) and where it is priced"
    - **Risk Implication:** Unclear FF&E scope could lead to pricing inconsistency or evaluator confusion
    - **Mitigation Consideration:** Include FF&E treatment ambiguity as a cost risk; propose to handle FF&E as separate additional item (not in base cost per Addendum 03 guidance); define scope clearly in pricing narrative (DEL-05-03)
    - **Source:** Decomposition §12 OI-004 OPEN; §4 Addendum 03 (FF&E may be included as additional item, not in base cost)

12. **Bond Costs**
    - **Consideration:** Agreement to Bond is mandatory; bond costs must be included in proposal price
    - **Risk Implication:** Underestimating bond costs or failing to include could affect competitiveness or compliance
    - **Mitigation Consideration:** Obtain bond cost estimate from surety; include in Schedule A/B; confirm inclusion in bonding evidence deliverable (DEL-01-03)
    - **Source:** Decomposition §3 C-04 (bond requirements); §8 DEL-01-03; §9 SOW-004

#### Schedule and Procurement Factors

13. **Permitting Delays**
    - **Consideration:** Building permit, development permit, utility permits, and environmental permits are required; approval timelines vary
    - **Risk Implication:** Permitting delays could push construction start date and affect substantial completion milestone
    - **Mitigation Consideration:** Include realistic permitting durations in schedule (DEL-08-01); identify critical path permit dependencies; propose concurrent permitting where feasible
    - **Source:** ASSUMPTION — Standard design-build project risk; specific permitting requirements referenced in RFP risk themes **[RFP section reference TBD]**

14. **Procurement Lead Times**
    - **Consideration:** Long-lead items (e.g., structural steel, mechanical equipment, fire apparatus exhaust systems, generator) may have extended delivery times
    - **Risk Implication:** Underestimating lead times could delay construction or require expediting costs
    - **Mitigation Consideration:** Identify long-lead items in schedule (DEL-08-01); propose early procurement strategy; include procurement milestone in critical path narrative
    - **Source:** ASSUMPTION — Standard design-build project risk; specific long-lead items inferred from project scope (fire hall + public works building)

15. **Subtrade Availability**
    - **Consideration:** Subtrade availability varies by market conditions and project timing
    - **Risk Implication:** Subtrade unavailability or pricing volatility could affect cost or schedule
    - **Mitigation Consideration:** Engage key subtrades early for pricing and availability confirmation; list committed subtrades in Appendix I (DEL-07-03); include subtrade coordination in risk register
    - **Source:** ASSUMPTION — Standard design-build project risk; Appendix I requirement per Decomposition §9 SOW-007

#### Compliance and Submission Factors

16. **Proposal Format and Size (15 MB Limit)**
    - **Consideration:** Proposal must be single PDF under 15 MB including all drawings and mandatory content
    - **Risk Implication:** Exceeding 15 MB limit or incorrect format could result in non-compliance and disqualification
    - **Mitigation Consideration:** Monitor PDF size during assembly; optimize images and drawings for file size; perform pre-submission compliance check per DEL-01-02
    - **Source:** Decomposition §3 C-01 (hard constraint); §8 DEL-01-02

17. **Addenda Acknowledgement**
    - **Consideration:** Appendix H includes addenda acknowledgement line; failure to acknowledge addenda may disqualify price proposal
    - **Risk Implication:** Omitting addenda acknowledgement could disqualify price proposal
    - **Mitigation Consideration:** Ensure Appendix H Schedule A (DEL-05-01) includes addenda acknowledgement checkboxes; cross-reference addenda integration in compliance matrix (DEL-01-01)
    - **Source:** Decomposition §3 C-07 (hard constraint); §9 SOW-003

### Quality Management Considerations

18. **Design QC Checkpoints**
    - **Consideration:** Design errors that propagate to construction documents increase rework cost and schedule impact
    - **Trade-off:** More QC checkpoints increase design phase duration but reduce construction phase rework risk
    - **Recommendation:** Implement milestone-based design QC reviews (concept, schematic, design development, construction documents) with interdisciplinary coordination checks
    - **Source:** ASSUMPTION — Standard design-build QC practice; RFP §10.2.2 QC/inspections **[specific clause details TBD]**

19. **Construction QC Inspections**
    - **Consideration:** Construction defects detected late increase correction cost and schedule impact
    - **Trade-off:** More frequent inspections increase QC labor cost but reduce defect risk and owner dissatisfaction
    - **Recommendation:** Implement phase-based construction QC inspections (foundation, structure, envelope, MEP rough-in, finishes) aligned with critical hold points
    - **Source:** ASSUMPTION — Standard construction QC practice; RFP §10.2.2 QC/inspections **[specific clause details TBD]**

20. **Commissioning QC Requirements**
    - **Consideration:** Incomplete or ineffective commissioning leads to operational deficiencies and warranty claims
    - **Trade-off:** Comprehensive commissioning increases closeout duration but ensures owner operational readiness
    - **Recommendation:** Align commissioning QC with DEL-06-01 commissioning/training/closeout narrative; include functional testing verification, training effectiveness checks, O&M documentation completeness verification
    - **Source:** Decomposition §8 DEL-06-01 (commissioning/training/closeout); §9 SOW-022

## Trade-offs

### Risk Identification Depth vs. Proposal Brevity

- **Competing Concern:** Comprehensive risk identification demonstrates thoroughness, but overly detailed risk registers can overwhelm evaluators or create perception of excessive uncertainty
- **Resolution Approach:** Prioritize material risks (high probability × impact scores); consolidate low-score risks into summary categories; use clear risk descriptions (1-2 sentences max) with mitigation summaries in register table, detailed mitigation plans in appendix
- **Source:** ASSUMPTION — Proposal writing best practice; balance between transparency (acceptance criteria) and evaluator readability

### Mitigation Cost vs. Risk Tolerance

- **Competing Concern:** More aggressive mitigation strategies (e.g., higher contingencies, earlier procurement, more QC checkpoints) reduce risk but increase cost; cost increases reduce price competitiveness (35 points for Proposal Price per Decomposition §15)
- **Resolution Approach:** Use risk prioritization to allocate mitigation budget efficiently; implement low-cost/high-impact mitigations first (e.g., early engagement, coordination protocols); reserve costly mitigations (e.g., large contingencies) for high-score risks only
- **Source:** ASSUMPTION — Risk-cost optimization principle; Decomposition §15 Evaluation Criteria (35 points for price)

### Transparency vs. Competitive Positioning

- **Competing Concern:** Transparent risk disclosure builds evaluator confidence but could reveal weaknesses or uncertainties that competitors do not disclose
- **Resolution Approach:** Disclose known material risks honestly (per acceptance criteria "transparent") but emphasize mitigation credibility and team capability to manage risks; frame risks as "challenges we are prepared to address" rather than "problems we cannot solve"

**Risk Register Scope Guidance [E-002]:** Risk Register contributes to Project Delivery Plan (10 points per Decomposition §15); evaluator expectation is TRANSPARENT (not exhaustive) identification + CREDIBLE (not elaborate) mitigation. Target 15-25 risks total, prioritized by score; detailed mitigation plans only for high-score risks (≥15).

- **Source:** ASSUMPTION — Proposal strategy consideration; _CONTEXT.md acceptance criteria requires transparency; Decomposition §15 Evaluation Criteria (35 points for price, 10 points for Project Delivery Plan) [E-002 evaluation balance clarification]

### Quality Rigor vs. Schedule Efficiency

- **Competing Concern:** More rigorous QC processes reduce defect risk but increase design and construction phase durations; schedule efficiency affects project delivery timeline (Decomposition §8 DEL-08-01 schedule evaluation)
- **Resolution Approach:** Implement "lean QC" — focus QC effort on high-risk/high-impact areas (e.g., structural, envelope, life safety systems); use parallel QC reviews where feasible to avoid serializing workflow; balance rigor with practical delivery timeline
- **Source:** ASSUMPTION — Quality-schedule trade-off inherent in design-build delivery; Decomposition §15 Evaluation Criteria includes Project Delivery Plan (10 points, includes schedule)

## Examples

### Example Risk Register Entry (Site Risk Category)

| Risk ID | Category | Description | Probability | Impact | Score | Mitigation Strategy | Owner | Status |
|---------|----------|-------------|-------------|--------|-------|---------------------|-------|--------|
| **SR-02** | Site | Geotechnical conditions (bearing capacity, groundwater, frost depth) differ from Geotechnical Investigation Report assumptions, requiring foundation redesign or additional measures | 3 (Medium) | 4 (High) | 12 | **Preventive:** Base foundation design on conservative interpretation of Geotechnical Report; include geotechnical engineer review of foundation design. **Contingency:** Include 5% foundation cost contingency for unforeseen conditions; plan for supplementary geotechnical investigation if conditions encountered differ significantly. **Monitoring:** Construction observation by geotechnical engineer during excavation and foundation installation. | Structural Engineer + PM | Active |

**Source:** ASSUMPTION — Example structure based on industry-standard risk register format; specific risk derived from _REFERENCES.md Geotechnical Investigation Report relevance

### Example Quality Management Plan Procedure (Design QC)

**Design QC Checkpoint: Construction Document Review (90% CD Stage)**

- **Purpose:** Verify construction documents are complete, coordinated, code-compliant, and constructible before final issue
- **Scope:** Architectural, structural, mechanical, electrical, civil drawings and specifications
- **Process:**
  1. Interdisciplinary coordination review (clash detection, interface verification)
  2. Code compliance review (building code, fire code, accessibility)
  3. Constructibility review (sequencing feasibility, material availability, installation practicality)
  4. Specification-drawing consistency check
- **Participants:** Lead Architect (coordinator), discipline leads (reviewers), PM (constructibility)
- **Deliverable:** QC review report with action items; action items must be resolved before 100% CD issue
- **Timeline:** 2-week review period at 90% CD milestone
- **Success Criteria:** No major coordination conflicts, code violations, or constructibility issues identified at 100% CD stage

**Source:** ASSUMPTION — Example procedure based on standard design-build QC practice; specific checkpoint timing inferred from typical design schedule

## Conflict Table (for human ruling)

**Conflict 1: Survey Availability — Constraint vs. Risk [B-004]**

| Contender | Document | Framing |
|-----------|----------|---------|
| Datasheet.md §35 | "Survey files provided after award only" | Operating Condition |
| Guidance.md §127-131 | "Detailed survey files are not available during proposal development" | Risk Consideration |
| Procedure.md §147 | "Survey files available only after award" | Planning Assumption |

**Resolution (Canonical Framing):** Survey unavailability IS a constraint (fact); it ENABLES risk identification (survey-related cost/schedule/design risks); mitigation = early post-award survey + contingency for design adjustments. Treat as both constraint (document in Datasheet) AND risk factor (identify survey-related risks in Procedure Step 2.2).

*Additional conflicts identified during Pass 2 (Cross-Reference Check) or Pass 3 (Semantic Lensing Enrichment) will be recorded here.*

## Notes

- This guidance document is a draft scaffold created by the 4_DOCUMENTS agent
- All considerations and trade-offs are labeled **ASSUMPTION** when derived from industry practice rather than accessible sources
- Examples are illustrative; actual risk register entries and QMP procedures should be developed by PM + Technical Leads based on project-specific analysis
- **Pass 1:** Initial generation completed
- **Pass 2:** Cross-reference consistency check completed (no changes required)
- **Pass 3:** Semantic lensing enrichment completed — incorporated 9 warranted items: A-002 (prescriptive authority fallback), A-004 (mitigation decision matrix), B-005 (risk-to-QC mapping), C-002 (design QC decision rule), D-002 (process governance), E-001 (evaluator expectation), E-002 (risk register scope), F-004 (multi-owner risks), X-002 (consideration status clarification)

---

**Document Generated:** 2026-02-04
**Agent:** 4_DOCUMENTS (Type 2 Specialist)
**Pass:** 3 (Semantic Lensing Enrichment Complete)
