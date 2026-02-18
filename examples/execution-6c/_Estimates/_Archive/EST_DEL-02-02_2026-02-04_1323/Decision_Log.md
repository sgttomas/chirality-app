# Decision Log
## EST_DEL-02-02_2026-02-04_1323

**Deliverable:** DEL-02-02 DesignBriefNarrative
**Package:** PKG-04 Design Proposal (Concept + Design Brief)

---

## Decisions

### D-001: Contracting Basis
**Decision:** Estimate assumes professional services on fixed-price proposal basis with internal Design-Build team.

**Trigger:** No contract structure specified in deliverable documents.

**Evidence:** _CONTEXT.md identifies "Lead Architect / Designer" as responsible party; RFP is a Design-Build procurement.

**Impacted WBS/CBS:** All line items

**Estimate Impact:** Moderate - fixed-price basis means effort variability absorbed by contractor.

**Override:** Provide specific contracting terms or rate agreements in `_CONFIG.md`.

---

### D-002: Location and Productivity
**Decision:** Professional services productivity based on Central Alberta consulting market; no site visits required.

**Trigger:** No explicit productivity factors provided.

**Evidence:** RFP identifies Penhold, Alberta location; DEL-02-02 is a narrative document not requiring site presence.

**Impacted WBS/CBS:** E (Engineering & Design)

**Estimate Impact:** Low - narrative deliverable has predictable effort patterns.

**Override:** Provide regional productivity factors in rate tables.

---

### D-003: Pricing Hierarchy - Allowances Used
**Decision:** All line items priced using ALLOWANCE method. No quotes or rate tables available.

**Trigger:** `_RateTables/` directory empty; no vendor quotes referenced for professional services.

**Evidence:** Filesystem check of `execution-6/_Estimates/_RateTables/` returned empty.

**Impacted WBS/CBS:** All line items

**Estimate Impact:** High - all costs are estimated allowances with LOW-MEDIUM confidence.

**Override:** Provide professional services rate tables or historical proposal costs.

---

### D-004: Indirects Model - Embedded
**Decision:** Overhead and profit embedded in professional hourly rates; no separate indirects line items for document deliverable.

**Trigger:** Deliverable is professional services (document production), not construction.

**Evidence:** DEL-02-02 output is "Design Brief narrative" per _CONTEXT.md; no field work involved.

**Impacted WBS/CBS:** PM (indirect component)

**Estimate Impact:** Low - standard consulting practice.

**Override:** Specify separate OH&P rates if required by cost structure.

---

### D-005: Contingency Method - PCT_BY_BUCKET
**Decision:** Apply percentage-based contingency: 15% on Engineering, 10% on PM.

**Trigger:** Default contingency method per AGENT_ESTIMATING.md; no risk-based method data available.

**Evidence:** No historical data on proposal effort variability; allowance-based pricing warrants higher contingency.

**Impacted WBS/CBS:** CONT (Contingency)

**Estimate Impact:** CAD 3,900 contingency on CAD 27,000 base (14.4% blended rate).

**Override:** Provide risk register with quantified ranges for RISK_BASED method.

---

### D-006: Escalation Mode - NONE
**Decision:** No escalation applied to estimate.

**Trigger:** Pricing date (2026-02) aligns with expected execution period.

**Evidence:** Proposal deadline originally Aug 2024; estimate prepared for immediate execution context.

**Impacted WBS/CBS:** N/A

**Estimate Impact:** None

**Override:** Set `escalation_mode = EXPLICIT` in `_CONFIG.md` with escalation factors.

---

### D-007: Currency Selection - CAD
**Decision:** All estimates in Canadian Dollars (CAD).

**Trigger:** Task specification mandated CAD.

**Evidence:** User instruction: "Currency: CAD"

**Impacted WBS/CBS:** All line items

**Estimate Impact:** None - single currency snapshot.

**Override:** N/A (currency specified by task).

---

### D-008: CBS Mapping - Engineering & Design
**Decision:** DEL-02-02 mapped to CBS "Engineering & Design (E)" as primary bucket, with supporting PM allocation.

**Trigger:** Deliverable type is "Narrative Document" requiring professional design services.

**Evidence:** _CONTEXT.md Type: "Narrative Document"; Responsible: "Lead Architect / Designer"

**Impacted WBS/CBS:** E, PM

**Estimate Impact:** Determines cost bucket allocation for project-level rollups.

**Override:** Provide explicit CBS mapping rules in `_CONFIG.md`.

---

### D-009: Effort Allocation by Discipline
**Decision:** Effort allocated across 5 disciplines plus coordination based on content requirements:
- Architectural: 40% (primary author, site/building integration)
- Civil: 10%
- Structural: 10%
- Mechanical: 15% (apparatus exhaust, HVAC complexity)
- Electrical/IT: 15% (generator, solar-ready, IT requirements)
- Coordination/QA: 10%

**Trigger:** Five discipline briefs required per RFP 7.1.2; varying complexity per discipline.

**Evidence:** Specification.md REQ-001 lists all 5 discipline briefs; Mechanical/Electrical have Addendum 03 complexity (exhaust, generator, solar).

**Impacted WBS/CBS:** E (all engineering line items)

**Estimate Impact:** Drives discipline-level cost breakdown.

**Override:** Provide actual discipline effort data from similar proposals.

---

### D-010: Durability Narrative Premium
**Decision:** Durability/Maintenance narrative (Section 8 of deliverable) allocated 20% premium effort due to 15-point scoring impact.

**Trigger:** Guidance.md emphasizes this is highest-value category after price (15 points).

**Evidence:** RFP Section 8.3 scoring; Guidance.md Principle 2; Procedure.md Step 5b recommends 1450-1750 words.

**Impacted WBS/CBS:** E (Architectural line item)

**Estimate Impact:** +CAD 2,000 for enhanced durability narrative development.

**Override:** Provide historical data on durability narrative effort.

---

*Generated by ESTIMATING agent*
*Snapshot: EST_DEL-02-02_2026-02-04_1323*
*Date: 2026-02-04*
